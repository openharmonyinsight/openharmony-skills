"""Capture native OpenSpec state without redirecting its workspace or task file."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def cli_json(cli: str, project: Path, args: list[str], store: str | None) -> dict:
    command = [cli, *args, "--json"]
    if store:
        command += ["--store", store]
    result = subprocess.run(command, cwd=project, text=True, capture_output=True, timeout=60)
    if result.returncode:
        raise ValueError(f"OpenSpec {' '.join(args)} failed: {result.stderr.strip() or result.stdout.strip()}")
    try:
        value = json.loads(result.stdout)
    except ValueError as error:
        raise ValueError("OpenSpec returned invalid JSON") from error
    if not isinstance(value, dict):
        raise ValueError("OpenSpec returned a non-object result")
    return value


def capture(project: Path, change: str, target: Path, *, cli: str = "openspec",
            store: str | None = None) -> dict:
    project, target = project.resolve(), target.resolve()
    if not project.is_dir() or not target.is_dir():
        raise ValueError("project and existing ODK change directories are required")
    # Serialize cooperating captures; keep the lock inode stable across calls.
    with (target / ".openspec-binding.lock").open("a+b") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError("OpenSpec capture already running for this ODK change") from error
        return _capture(project, change, target, cli=cli, store=store)


def portable_json(value, project: Path):
    """Remove checkout-specific prefixes, including paths in CLI instructions."""
    if isinstance(value, str):
        if value.startswith(os.sep):
            try:
                return Path(value).resolve().relative_to(project).as_posix()
            except ValueError:
                pass
        if value == str(project):
            return "."
        value = value.replace(str(project) + os.sep, "")
        return re.sub(re.escape(str(project)) + r"(?=$|[\s)\]}'\"，。;:])", ".", value)
    if isinstance(value, list):
        return [portable_json(item, project) for item in value]
    if isinstance(value, dict):
        return {key: portable_json(item, project) for key, item in value.items()}
    return value


def atomic_write(path: Path, content: bytes, *, replace: bool) -> None:
    fd, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if replace:
            os.replace(temporary, path)
        else:
            # Publish a complete immutable blob without replacing an existing one.
            try:
                os.link(temporary, path)
            except FileExistsError:
                if path.read_bytes() != content:
                    raise ValueError(f"existing native evidence changed: {path}")
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _capture(project: Path, change: str, target: Path, *, cli: str, store: str | None) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", change) or ".." in change.split("/"):
        raise ValueError("invalid native change name")
    binding = target / "openspec-binding.json"
    before = binding.read_bytes() if binding.exists() else None
    previous = json.loads(before) if before is not None else {}
    if not isinstance(previous, dict):
        raise ValueError("invalid existing OpenSpec binding")
    identity = {"project": os.path.relpath(project, target), "change": change, "store": store}
    old_project = previous.get("project")
    same_project = isinstance(old_project, str) and (target / old_project).resolve() == project
    if previous and (not same_project or previous.get("change") != change or previous.get("store") != store):
        raise ValueError("existing OpenSpec binding names a different change/project/store; resolve it explicitly")
    status = cli_json(cli, project, ["status", "--change", change], store)
    instructions = cli_json(cli, project, ["instructions", "apply", "--change", change], store)
    # A selected store can live outside the implementation checkout. The CLI's
    # resolved root, not the caller's cwd, owns its native artifact paths.
    native_root = Path(status.get("root", {}).get("path", str(project))).resolve()
    apply_root = instructions.get("root", {}).get("path")
    if apply_root and Path(apply_root).resolve() != native_root:
        raise ValueError("OpenSpec status and apply instructions name different roots")
    state = instructions.get("state")
    if state not in {"blocked", "ready", "in_progress", "all_done"}:
        raise ValueError(f"unsupported OpenSpec apply state: {state!r}")
    context = instructions.get("contextFiles")
    if not isinstance(context, dict):
        raise ValueError("OpenSpec apply instructions have no contextFiles object")
    blobs = {}
    sources = {}
    for artifact, entries in context.items():
        if not re.fullmatch(r"[A-Za-z0-9_-]+", artifact):
            raise ValueError("invalid native artifact id")
        if isinstance(entries, str):
            entries = [entries]  # Older CLI versions returned individual paths.
        if not isinstance(entries, list) or any(not isinstance(p, str) for p in entries):
            raise ValueError(f"invalid context files for {artifact}")
        for index, entry in enumerate(entries):
            source = Path(entry)
            if not source.is_absolute():
                source = native_root / source
            source = source.resolve()
            if not source.is_relative_to(native_root):
                raise ValueError("native context file escapes the selected OpenSpec root")
            if not source.is_file():
                raise ValueError(f"native context file is missing: {source}")
            content = source.read_bytes()
            name = f"{artifact}-{index}.md"
            blobs[name] = content
            sources[name] = {"path": source.relative_to(native_root).as_posix(), "sha256": hashlib.sha256(content).hexdigest()}
    if not blobs and state != "blocked":
        raise ValueError("OpenSpec reports actionable state without context files")
    status = portable_json(portable_json(status, native_root), project)
    instructions = portable_json(portable_json(instructions, native_root), project)
    payload = {"project": ".", "change": change, "store": store,
               "source_root": "selected-openspec-root",
               "status": status, "apply": instructions, "sources": sources}
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    digest = hashlib.sha256(serialized).hexdigest()
    snapshot = target / "evidence/openspec" / digest
    snapshot.mkdir(parents=True, exist_ok=True)
    for name, content in {**blobs, "manifest.json": serialized}.items():
        destination = snapshot / name
        if destination.exists():
            if destination.read_bytes() != content:
                raise ValueError(f"existing native evidence changed: {destination}")
        else:
            atomic_write(destination, content, replace=False)
    updated = {**previous, **identity, "state_owner": "openspec", "state": state,
               "snapshot": str(snapshot.relative_to(target)), "snapshot_sha256": digest}
    after = binding.read_bytes() if binding.exists() else None
    if after != before:
        raise ValueError("OpenSpec binding changed while capturing; reread before updating")
    content = json.dumps(updated, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    if before != content:
        atomic_write(binding, content, replace=True)
    return {**updated, "status": status, "apply": instructions}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change_dir", type=Path, help="Existing ODK archive directory")
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--change", required=True, help="Native OpenSpec change name")
    parser.add_argument("--store")
    parser.add_argument("--cli", default="openspec", help="OpenSpec executable path")
    args = parser.parse_args(argv)
    try:
        result = capture(args.project, args.change, args.change_dir, cli=args.cli, store=args.store)
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        print(f"OpenSpec bridge error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
