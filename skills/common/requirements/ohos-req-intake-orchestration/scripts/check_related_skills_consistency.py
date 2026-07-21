#!/usr/bin/env python3
"""Check Phase 0 Intake Bundle related-skill declarations."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from install_related_skills import ORCHESTRATOR, REQUIRED_SKILLS

ALLOWED_EXTERNAL_SKILLS = {
    # External handoff package/tool names referenced by the requirement intake docs.
    "ohos-delivery",
    "ohos-delivery-kit",
    "ohos-phase0-intake",
}


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
        for name in re.findall(r"ohos-[a-z0-9-]+", body)
        if name != ORCHESTRATOR and name not in ALLOWED_EXTERNAL_SKILLS
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


def registered_skill_names(skills_dir: Path) -> set[str]:
    return {
        item.name
        for item in skills_dir.iterdir()
        if item.is_dir() and (item / "SKILL.md").is_file()
    }


def iter_reference_files(skills_dir: Path) -> list[Path]:
    files: list[Path] = []
    for skill_dir in sorted(skills_dir.glob("ohos-req-*")):
        skill_file = skill_dir / "SKILL.md"
        if skill_file.is_file():
            files.append(skill_file)
        for ref_dir_name in ("reference", "references"):
            ref_dir = skill_dir / ref_dir_name
            if not ref_dir.is_dir():
                continue
            for ref_file in sorted(ref_dir.rglob("*")):
                if ref_file.suffix in {".md", ".json"} and ref_file.is_file():
                    files.append(ref_file)
    return files


def unresolved_ohos_references(skills_dir: Path) -> list[tuple[Path, str]]:
    registered = registered_skill_names(skills_dir)
    allowed = registered | ALLOWED_EXTERNAL_SKILLS | {ORCHESTRATOR}
    unresolved: list[tuple[Path, str]] = []
    for path in iter_reference_files(skills_dir):
        text = path.read_text(encoding="utf-8")
        for name in sorted(set(re.findall(r"ohos-[a-z0-9-]+", text))):
            if name not in allowed:
                unresolved.append((path.relative_to(skills_dir), name))
    return unresolved


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    skills_dir = script_dir.parents[1]
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
    unresolved = unresolved_ohos_references(skills_dir)
    if unresolved:
        print("UNRESOLVED [ohos-* references]")
        for path, name in unresolved:
            print(f"  {path}: {name}")
        ok = False
    else:
        print("OK   [ohos-* references resolvable]")

    if ok:
        print("Result: CONSISTENT")
        return 0

    print("Result: INCONSISTENT - 名称需保持同步且引用需可解析：")
    print("  1) SKILL.md frontmatter metadata.related-skills")
    print("  2) 编排器正文 spawn/调用点的 ohos-* 引用")
    print("  3) install_related_skills.py REQUIRED_SKILLS 数组")
    print("  4) 各 ohos-req-* skill 文档中的 ohos-* 引用必须指向已注册 skill 或白名单外部工具")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
