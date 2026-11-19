#!/usr/bin/env python3
"""Report the current host's delegation capability for Task-level review.

Fail-closed: an unknown, ambiguous or partially detected host reports no
delegation and serial review. The Task review contract treats this JSON as the
only capability source; it never infers fan-out from the agent brand alone.
"""
from __future__ import annotations

import argparse
import json
import os
import re

# max_parallel is a policy value (fixed three reviewer seats), not the host's
# theoretical limit. R-TE-004 caps same-layer fan-out at 4; the review uses 3.
HOSTS = {
    "claude": {
        "can_delegate": True,
        "max_parallel": 3,
        "can_background": True,
        "supports_nesting": False,
        "mechanism": "Agent/Task tool: launch three read-only agents in one message",
    },
    # Protocol, not delegation, changes across OpenCode majors: 2.x exposes
    # ``subagent`` (agent=general) while 1.x exposes ``task`` with a required
    # ``subagent_type`` and gates background runs behind an env flag. Keep
    # background unconfirmed until the version or the actual tool is known.
    "opencode": {
        "can_delegate": True,
        "max_parallel": 3,
        "can_background": False,
        "supports_nesting": False,
        "protocol": "confirm",
        "mechanism": (
            "confirm the exposed tool: 2.x subagent(agent=general) or "
            "1.x task(subagent_type=general); three read-only calls in one batch"
        ),
    },
    "codex": {
        "can_delegate": True,
        "max_parallel": 3,
        "can_background": False,
        "supports_nesting": False,
        "mechanism": "configured subagent/agent thread: batch three read-only briefs",
    },
}

SERIAL = {
    "can_delegate": False,
    "max_parallel": 1,
    "can_background": False,
    "supports_nesting": False,
    "mechanism": "three sequential read-only passes in the coordinator context",
}

ENV_MARKERS = (
    ("claude", ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_PROJECT_DIR")),
    ("opencode", ("OPENCODE", "OPENCODE_PID", "OPENCODE_CONFIG", "OPENCODE_SESSION_ID")),
    ("codex", ("CODEX_HOME", "CODEX_SANDBOX", "CODEX_THREAD_ID", "CODEX_MANAGED_BY_NPM")),
)


def detect_host(env=None) -> str:
    """Return one unambiguous env-detected host, else an empty string."""
    env = os.environ if env is None else env
    found = [host for host, names in ENV_MARKERS if any(env.get(name) for name in names)]
    return found[0] if len(found) == 1 else ""


def _opencode_capabilities(version: str = "") -> dict:
    caps = {"host": "opencode", **HOSTS["opencode"]}
    match = re.fullmatch(r"\s*v?(\d+)(?:\.\d+){0,2}(?:[-+].*)?\s*", version)
    major = int(match.group(1)) if match else None
    if major is not None and major >= 2:
        caps.update(
            can_background=True,
            protocol="subagent",
            mechanism="subagent tool with agent=general: three calls in one batch",
            reason="OpenCode 2.x delegation protocol",
        )
    elif major == 1:
        caps.update(
            protocol="task",
            mechanism=(
                "task tool with subagent_type=general: three calls in one batch; "
                "background only when OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=true"
            ),
            reason="OpenCode 1.x delegation protocol",
        )
    else:
        caps["reason"] = (
            "OpenCode protocol varies by version; confirm the exposed tool "
            "(2.x subagent / 1.x task), otherwise use serial review"
        )
    return caps


def capabilities(host: str = "", env=None, version: str = "") -> dict:
    resolved = host.strip().lower() or detect_host(env)
    if resolved == "opencode":
        return _opencode_capabilities(version)
    if resolved in HOSTS:
        return {"host": resolved, **HOSTS[resolved], "reason": "host capability table"}
    if resolved == "openclaw":
        return {"host": resolved, **SERIAL, "reason": "host has no delegation; serial review"}
    return {
        "host": resolved or "unknown",
        **SERIAL,
        "reason": "host not recognized or ambiguous; fail-closed to serial review",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="", help="explicit host: claude|codex|opencode|openclaw")
    parser.add_argument(
        "--version", default="", help="host version when known; selects the OpenCode protocol"
    )
    parser.add_argument("--json", action="store_true", help="emit JSON (the only output format)")
    args = parser.parse_args(argv)
    print(json.dumps(capabilities(args.host, version=args.version), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
