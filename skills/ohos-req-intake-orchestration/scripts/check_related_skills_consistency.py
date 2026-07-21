#!/usr/bin/env python3
"""Check Phase 0 Intake Bundle related-skill declarations."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from install_related_skills import ORCHESTRATOR, REQUIRED_SKILLS


def split_frontmatter(text: str) -> tuple[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return "", text
    for idx, line in enumerate(lines[1:], start=1):
        if line == "---":
            return "\n".join(lines[1:idx]), "\n".join(lines[idx + 1 :])
    return "", text


def names_in_body(body: str) -> set[str]:
    return {
        name
        for name in re.findall(r"ohos-req-[a-z0-9-]+", body)
        if name != ORCHESTRATOR
    }


def names_in_frontmatter(frontmatter: str) -> set[str]:
    names = set()
    for line in frontmatter.splitlines():
        match = re.match(r"\s*-\s+name:\s*(ohos-req-[a-z0-9-]+)\s*$", line)
        if match:
            names.add(match.group(1))
    return names


def print_diff(label: str, left: set[str], right: set[str]) -> bool:
    if left == right:
        print(f"OK   [{label}] ({len(left)} skills)")
        return True
    print(f"MISMATCH [{label}]")
    print("  only in left:", " ".join(sorted(left - right)))
    print("  only in right:", " ".join(sorted(right - left)))
    return False


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    orch_skill = script_dir.parent / "SKILL.md"
    if not orch_skill.is_file():
        print(f"FATAL: {orch_skill} not found", file=sys.stderr)
        return 2

    frontmatter, body = split_frontmatter(orch_skill.read_text(encoding="utf-8"))
    body_names = names_in_body(body)
    declared_names = names_in_frontmatter(frontmatter)
    required_names = {name for name, _, _ in REQUIRED_SKILLS}

    print("Bundle: ohos-phase0-intake")
    print(
        f"body={len(body_names)} declared={len(declared_names)} "
        f"install={len(required_names)}"
    )
    ok = True
    ok &= print_diff("body vs declared", body_names, declared_names)
    ok &= print_diff("declared vs install-array", declared_names, required_names)

    if ok:
        print("Result: CONSISTENT")
        return 0

    print("Result: INCONSISTENT - 三处名称需保持同步：")
    print("  1) SKILL.md frontmatter metadata.related-skills")
    print("  2) 编排器正文 spawn/调用点的 ohos-req-* 引用")
    print("  3) install_related_skills.py REQUIRED_SKILLS 数组")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
