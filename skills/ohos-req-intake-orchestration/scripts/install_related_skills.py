#!/usr/bin/env python3
"""Phase 0 Intake Bundle dependency preflight and installer.

Uses only the Python standard library so it runs on Windows, Linux, and macOS.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


REQUIRED_SKILLS = [
    ("ohos-req-requirement-intake", "0.1.0", True),
    ("ohos-req-feasibility-analysis", "0.1.0", True),
    ("ohos-req-arch-decision", "0.1.0", True),
    ("ohos-req-feature-baseline", "0.1.0", True),
    ("ohos-req-review-gate", "0.1.0", True),
    ("ohos-req-value-decision", "0.1.0", True),
    ("ohos-req-review-ppt-gen", "0.1.0", False),
    ("ohos-req-feature-to-ir", "0.1.0", True),
    ("ohos-req-proposal-to-sr", "0.1.0", True),
]
ORCHESTRATOR = "ohos-req-intake-orchestration"


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def skills_dir() -> Path:
    override = os.environ.get("OHOS_REQ_SKILLS_DIR")
    return Path(override).resolve() if override else script_dir().parents[1]


def source_skills_dir(target: Path) -> Path:
    override = os.environ.get("OHOS_REQ_SKILLS_SOURCE_DIR")
    return Path(override).resolve() if override else target


def read_frontmatter_value(skill_file: Path, key: str) -> str:
    for line in skill_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith(f"{key}:"):
            return stripped.split(":", 1)[1].strip()
    return ""


def version_tuple(version: str) -> tuple[int, int, int]:
    parts = []
    for part in version.split(".")[:3]:
        digits = "".join(ch for ch in part if ch.isdigit())
        parts.append(int(digits or "0"))
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)


def check_bundle(target: Path) -> tuple[int, list[str], list[str]]:
    installed = 0
    missing: list[str] = []
    mismatches: list[str] = []

    for name, min_version, required in REQUIRED_SKILLS:
        skill_file = target / name / "SKILL.md"
        if not skill_file.is_file():
            if required:
                missing.append(name)
            continue

        fm_name = read_frontmatter_value(skill_file, "name")
        if fm_name != name:
            print(f"WARN: directory name '{name}' != frontmatter name '{fm_name}'")

        fm_version = read_frontmatter_value(skill_file, "version")
        if fm_version and version_tuple(fm_version) < version_tuple(min_version):
            mismatches.append(f"{name} (found={fm_version}, required>={min_version})")

        installed += 1

    if (target / ORCHESTRATOR / "SKILL.md").is_file():
        installed += 1

    return installed, missing, mismatches


def print_report(installed: int, missing: list[str], mismatches: list[str]) -> None:
    total = len(REQUIRED_SKILLS) + 1
    print("Bundle: ohos-phase0-intake")
    print(f"Installed: {installed}/{total}")
    for name in missing:
        print(f"  MISSING (required): {name}")
    print(f"Required missing: {len(missing)}")
    for mismatch in mismatches:
        print(f"  VERSION: {mismatch}")
    print(f"Version mismatch: {len(mismatches)}")


def install_missing(target: Path, source: Path, missing: list[str]) -> bool:
    installed_any = False
    for name in missing:
        src = source / name
        dst = target / name
        if not (src / "SKILL.md").is_file():
            print(f"ERROR: cannot install {name}; source not found: {src}", file=sys.stderr)
            return False
        target.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"Installed missing skill: {name}")
        installed_any = True
    if not installed_any:
        print("No missing required skills to install.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="check dependencies only")
    group.add_argument("--install", action="store_true", help="install missing required skills")
    group.add_argument("--check-probes", action="store_true", help="check dependencies and probes")
    args = parser.parse_args()
    mode = "--check"
    if args.install:
        mode = "--install"
    elif args.check_probes:
        mode = "--check-probes"

    target = skills_dir()
    source = source_skills_dir(target)

    installed, missing, mismatches = check_bundle(target)
    print_report(installed, missing, mismatches)

    if mode == "--install" and missing:
        print()
        if not install_missing(target, source, missing):
            return 1
        print()
        installed, missing, mismatches = check_bundle(target)
        print_report(installed, missing, mismatches)

    if mode == "--check-probes":
        print("Probe: related skill directory readable")
        print("Probe result: PASS" if target.is_dir() else "Probe result: FAIL")

    if missing:
        print("Result: NOT READY")
        print()
        print("Install missing skills:")
        print(
            "  OHOS_REQ_SKILLS_SOURCE_DIR=/path/to/skills "
            f"python3 {script_dir() / 'install_related_skills.py'} --install"
        )
        return 1

    if mismatches:
        print("Result: NOT READY (version mismatch)")
        return 1

    print("Result: READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
