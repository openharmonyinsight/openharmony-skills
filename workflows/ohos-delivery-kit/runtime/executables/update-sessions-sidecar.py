#!/usr/bin/env python3
"""Atomically update the .sessions.json sidecar for an ODK deliverable.

Usage:
    python update-sessions-sidecar.py <change_dir> <deliverable_name> <session_id> <skill_name> <action> [--time <UTC ISO 8601>]

This script reads the existing .sessions.json sidecar, appends the given session
to the deliverable's entry (deduplicating the sessions array, not deduplicating
the log array), writes it back, and prints the mirror data for the AI to use:

    ---SIDECAR WRITTEN---
    <updated sidecar JSON>

    ---MIRROR---
    sessions: "ses_aaa,ses_bbb"
    ## 会话记录

    | Session ID | Skill | 时间(UTC) | 操作 |
    |------------|-------|----------|------|
    | ses_aaa | odk-init | 2026-10-16T10:00:00Z | 生成 |
    | ses_bbb | odk-propose | 2026-10-16T12:00:00Z | 更新 |

The script is fail-open: errors print to stderr and exit(0) so they never block
the AI. The AI should check the output for the mirror data.

Concurrency: the entire read-modify-write is guarded by an exclusive lock on a
sibling ``.sessions.json.lock`` file, and the publish uses a temp file +
``os.replace()`` so a crashed writer cannot corrupt the authoritative source.

Session ID formats accepted across host platforms:
    opencode: ses_<alphanumeric>            e.g. ses_abc123
    codex:    <uuid>                        e.g. 11111111-2222-3333-4444-555555555555
    claude:   <uuid>                        e.g. aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
"""

import json
import os
import sys
import re
import time
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# --- Session ID format: multi-platform -------------------------------------
# opencode: ses_[a-zA-Z0-9_-]+
# codex:    <uuid>
# claude:   <uuid>
_UUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
SESSION_ID_RE = re.compile(
    r"^(?:ses_[a-zA-Z0-9_-]+|" + _UUID + r")$"
)

# Sentinel value the AI passes when the host does not expose a session ID.
# The script skips the update and informs the AI instead of fabricating an ID.
SESSION_UNAVAILABLE = "unavailable"


def fail_open(msg):
    """Print error to stderr, exit 0 (never block the AI)."""
    print(f"[update-sessions-sidecar] WARN: {msg}", file=sys.stderr)
    sys.exit(0)


def now_utc_iso():
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --- Cross-platform exclusive lock -----------------------------------------
def _acquire_lock(lock_path):
    """Acquire an exclusive advisory lock on ``lock_path``.

    Returns an OS-level file descriptor on success, or ``None`` if the lock
    cannot be acquired (timeout / unsupported platform). The caller owns the
    fd and must close it.
    """
    try:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        return None
    try:
        fd = os.open(str(lock_path), os.O_RDWR | os.O_CREAT, 0o644)
    except OSError:
        return None
    try:
        # Ensure the lock file has at least one byte (required by msvcrt.locking).
        os.ftruncate(fd, 1)
        os.lseek(fd, 0, os.SEEK_SET)
    except OSError:
        pass
    try:
        if sys.platform == "win32":
            import msvcrt
            deadline = time.monotonic() + 10  # 10s timeout
            while True:
                try:
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                    return fd
                except OSError:
                    if time.monotonic() > deadline:
                        os.close(fd)
                        return None
                    time.sleep(0.05)
        else:
            import fcntl
            fcntl.flock(fd, fcntl.LOCK_EX)
            return fd
    except (OSError, ImportError):
        try:
            os.close(fd)
        except OSError:
            pass
        return None


def _release_lock(fd):
    """Release and close a lock fd acquired via ``_acquire_lock``."""
    try:
        if sys.platform != "win32":
            import fcntl
            fcntl.flock(fd, fcntl.LOCK_UN)
    except (OSError, ImportError):
        pass
    try:
        os.close(fd)
    except OSError:
        pass


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)
    if len(sys.argv) < 6:
        print("Usage: update-sessions-sidecar.py <change_dir> <deliverable_name> <session_id> <skill_name> <action> [--time <ISO 8601>]", file=sys.stderr)
        sys.exit(1)

    change_dir = Path(sys.argv[1])
    deliverable_name = sys.argv[2]  # e.g. "proposal.md"
    session_id = sys.argv[3]
    skill_name = sys.argv[4]
    action = sys.argv[5]  # e.g. "生成" or "追加" or "更新"

    # Optional: --time <ISO 8601>
    timestamp = now_utc_iso()
    if "--time" in sys.argv:
        idx = sys.argv.index("--time")
        if idx + 1 < len(sys.argv):
            timestamp = sys.argv[idx + 1]

    # --- Host did not expose a session ID: skip, do not fabricate ------------
    if session_id == SESSION_UNAVAILABLE or not session_id.strip():
        print("---SIDECAR SKIPPED---")
        print("Host platform did not expose a session ID; session tracking skipped.")
        print("Inform the user that this deliverable was not recorded in the sidecar.")
        print("---END MIRROR---")
        return

    # Validate session ID format
    if not SESSION_ID_RE.match(session_id):
        fail_open(
            f"session_id '{session_id}' does not match any accepted format "
            f"(opencode: ses_*, codex/claude: <uuid>)"
        )

    sidecar_path = change_dir / ".sessions.json"
    lock_path = sidecar_path.with_name(sidecar_path.name + ".lock")

    # --- ACQUIRE exclusive lock for the whole read-modify-write --------------
    lock_fd = _acquire_lock(lock_path)
    if lock_fd is None:
        fail_open("could not acquire sidecar lock (contention/unsupported); skipping to avoid data loss")
    try:
        _run_update(sidecar_path, deliverable_name, session_id, skill_name, action, timestamp)
    finally:
        if lock_fd is not None:
            _release_lock(lock_fd)


def _run_update(sidecar_path, deliverable_name, session_id, skill_name, action, timestamp):
    """Read-modify-write the sidecar under the caller's lock; publish atomically."""

    # --- READ existing sidecar (never start from scratch) ---
    sidecar = {}
    if sidecar_path.exists():
        try:
            raw = sidecar_path.read_text(encoding="utf-8-sig")
            sidecar = json.loads(raw) if raw.strip() else {}
        except (json.JSONDecodeError, OSError) as e:
            fail_open(f"failed to read existing sidecar: {e}")

    # --- FIND or CREATE deliverable entry ---
    entry = sidecar.get(deliverable_name)
    if not isinstance(entry, dict):
        entry = {"sessions": [], "log": []}
        sidecar[deliverable_name] = entry

    if "sessions" not in entry or not isinstance(entry["sessions"], list):
        entry["sessions"] = []
    if "log" not in entry or not isinstance(entry["log"], list):
        entry["log"] = []

    # --- AUTO-DETERMINE action: first entry = "生成", all subsequent = "更新" ---
    if len(entry["log"]) == 0:
        final_action = "生成"
    else:
        final_action = "更新"
    if action != final_action:
        print(f"[update-sessions-sidecar] NOTE: overriding action '{action}' -> '{final_action}' (log has {len(entry['log'])} existing entry/ies)", file=sys.stderr)

    # --- APPEND to sessions (deduplicated) ---
    if session_id not in entry["sessions"]:
        entry["sessions"].append(session_id)

    # --- APPEND to log (NOT deduplicated) ---
    log_entry = {
        "session": session_id,
        "skill": skill_name,
        "time": timestamp,
        "action": final_action,
    }
    entry["log"].append(log_entry)

    # --- WRITE back atomically (temp file + os.replace) ---
    payload = json.dumps(sidecar, indent=2, ensure_ascii=False) + "\n"
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=str(sidecar_path.parent), prefix=".sessions.", suffix=".tmp"
    )
    try:
        # Write all bytes — os.write may partial-write on some systems.
        data = payload.encode("utf-8")
        written = 0
        while written < len(data):
            n = os.write(tmp_fd, data[written:])
            if n <= 0:
                raise OSError("os.write returned non-positive byte count")
            written += n
        os.close(tmp_fd)
        # Verify the temp file is complete, parseable JSON before publishing.
        # Catches truncation from RLIMIT_FSIZE, disk-full, or partial writes
        # that did not raise OSError (defence-in-depth).
        try:
            with open(tmp_path, "r", encoding="utf-8") as vf:
                json.load(vf)
        except (json.JSONDecodeError, OSError) as ve:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            fail_open(f"sidecar write verification failed (truncated?): {ve}")
        os.replace(tmp_path, sidecar_path)
    except OSError as e:
        try:
            os.close(tmp_fd)
        except OSError:
            pass
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        fail_open(f"failed to write sidecar: {e}")

    # --- OUTPUT mirror data for the AI ---
    print("---SIDECAR WRITTEN---")
    print(json.dumps(sidecar, indent=2, ensure_ascii=False))
    print()
    print("---MIRROR---")

    # frontmatter sessions field (comma-separated)
    sessions_str = ",".join(entry["sessions"])
    print(f'sessions: "{sessions_str}"')
    print()

    # body table
    print("## 会话记录")
    print()
    print("| Session ID | Skill | 时间(UTC) | 操作 |")
    print("|------------|-------|----------|------|")
    for log_item in entry["log"]:
        sid = log_item.get("session", "")
        sk = log_item.get("skill", "")
        tm = log_item.get("time", "")
        ac = log_item.get("action", "")
        print(f"| {sid} | {sk} | {tm} | {ac} |")

    print()
    print("---END MIRROR---")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        fail_open(f"unexpected error: {e}")
