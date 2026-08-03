#!/usr/bin/env python3
"""Verify and capture the pinned Host environment for integration eval case 1."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


PINNED_ACE_REVISION = "3d648d632141678368bde7a0376cf80f67f6e3e4"
RELATIVE_BINARY = Path(
    "tests/unittest/ace_engine/ImageSet-DrawableDescriptor/drawable_descriptor_test"
)


def run(*command: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_id(path: Path) -> str | None:
    result = run("readelf", "-n", str(path))
    match = re.search(r"Build ID:\s*([0-9a-fA-F]+)", result.stdout)
    return match.group(1).lower() if match else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--oh-root", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.oh_root.resolve()
    ace_root = root / "foundation/arkui/ace_engine"
    out_root = root / "out/host/host_product"
    stripped = out_root / RELATIVE_BINARY
    symbolized = out_root / "exe.unstripped" / RELATIVE_BINARY
    state_path = out_root / "build_state.json"
    xml_path = args.artifact_dir.resolve() / "integration-case-1.xml"
    args.artifact_dir.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    checks: dict[str, object] = {}
    revision = run("/usr/bin/git", "rev-parse", "HEAD", cwd=ace_root)
    checks["ace_revision"] = revision.stdout.strip() if revision.returncode == 0 else None
    status = run("/usr/bin/git", "status", "--porcelain", cwd=ace_root)
    checks["ace_worktree_clean"] = status.returncode == 0 and not status.stdout.strip()
    checks["ace_revision_pinned"] = checks["ace_revision"] == PINNED_ACE_REVISION

    build_state = None
    if state_path.is_file():
        try:
            build_state = json.loads(state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            build_state = None
    checks["build_state_present"] = build_state is not None
    checks["build_product"] = build_state.get("product") if build_state else None
    targets = build_state.get("targets", []) if build_state else []
    if isinstance(targets, str):
        targets = [targets]
    checks["build_targets"] = targets
    checks["build_status"] = build_state.get("status") if build_state else None
    checks["build_exit_code"] = build_state.get("exit_code") if build_state else None
    checks["build_success"] = bool(
        build_state
        and build_state.get("product") == "host_product"
        and "ace_engine_test" in targets
        and build_state.get("status") == "success"
        and build_state.get("exit_code") == 0
    )

    artifacts = {}
    for name, path in (("stripped", stripped), ("exe_unstripped", symbolized)):
        present = path.is_file()
        artifacts[name] = {
            "path": str(path),
            "present": present,
            "executable": present and os.access(path, os.X_OK),
            "size": path.stat().st_size if present else None,
            "mtime_ns": path.stat().st_mtime_ns if present else None,
            "sha256": sha256(path) if present else None,
            "build_id": build_id(path) if present else None,
        }

    checks["artifacts_executable"] = all(
        item["present"] and item["executable"] for item in artifacts.values()
    )
    checks["matching_build_ids"] = bool(
        artifacts["stripped"]["build_id"]
        and artifacts["stripped"]["build_id"] == artifacts["exe_unstripped"]["build_id"]
    )

    ready = all(
        (
            checks["ace_revision_pinned"],
            checks["ace_worktree_clean"],
            checks["build_success"],
            checks["artifacts_executable"],
            checks["matching_build_ids"],
        )
    )
    manifest = {
        "schema_version": 1,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "ready": ready,
        "oh_root": str(root),
        "ace_root": str(ace_root),
        "pinned_ace_revision": PINNED_ACE_REVISION,
        "checks": checks,
        "build_state_path": str(state_path),
        "build_state": build_state,
        "artifacts": artifacts,
        "requested_case": "DrawableDescriptorTest.AnimatedDrawableDescTest044",
        "gtest_filter": "--gtest_filter=DrawableDescriptorTest.AnimatedDrawableDescTest044",
        "xml_output": str(xml_path),
    }
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ready": ready, "output": str(args.output)}, ensure_ascii=False))
    return 0 if ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
