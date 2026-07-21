#!/usr/bin/env python3
"""Validate one ODK change directory against runtime/assets/contracts/artifacts.yaml.

This is stricter than validate-artifacts-structural.sh:
- required artifacts must exist
- required sections must be present exactly as Markdown headings
- conditional sections are reported as warnings when absent
- spec ACs must be traceable into execution-plan and code mapping
- optional evidence directories, if present, must contain files

It intentionally avoids external dependencies.
"""

from __future__ import annotations

import re
import sys
from argparse import ArgumentParser
from pathlib import Path

RUNTIME_ROOT = Path(__file__).resolve().parents[2]
ASSET_ROOT = RUNTIME_ROOT / "assets"
sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from odk_yaml import parse_contract_artifacts  # noqa: E402


AC_RE = re.compile(r"\bAC-\d+(?:\.\d+)?\b")
TASK_RE = re.compile(r"\bTASK-\d+\b")
PLACEHOLDER_RE = re.compile(
    r"^\s*(?:"
    r"|[-—]+"
    r"|TBD"
    r"|TODO"
    r"|N/?A"
    r"|待定"
    r"|待补充"
    r"|待实现"
    r"|待验证"
    r"|\[[^\]]+\]"
    r")\s*$",
    re.IGNORECASE,
)
ARCHIVE_MARKER_RE = re.compile(
    r"\b(?:TBD|TODO)\b|(?<![\u4e00-\u9fff])(?:待定|待补充|待实现|待验证)(?![\u4e00-\u9fff])",
    re.IGNORECASE,
)
BRACKET_PLACEHOLDER_RE = re.compile(
    r"\[(?:[^\]\n]*(?:引用|标题|角色|功能|价值|条件|填写|描述|说明|编号|名称|路径|模块|文件|命令|证据|结果|待|TBD|TODO)[^\]\n]*)\]",
    re.IGNORECASE,
)
ARCHIVE_READY_CLAIM_RE = re.compile(r"\b(?:PASS|Ready)\b|通过|可归档|归档就绪", re.IGNORECASE)
LEGACY_TARGET_RELEASE_RE = re.compile(
    r"^OpenHarmony-\d+\.\d+(?:-(?:Release|Beta|Alpha|Dev))?$",
    re.IGNORECASE,
)
TARGET_RELEASE_RE = re.compile(r"^\d+\.\d+(?:-(?:Release|Beta|Alpha|Dev))?$", re.IGNORECASE)


class Reporter:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.warned = 0

    def pass_(self, message: str) -> None:
        print(f"  PASS {message}")
        self.passed += 1

    def fail(self, message: str) -> None:
        print(f"  FAIL {message}")
        self.failed += 1

    def warn(self, message: str) -> None:
        print(f"  WARN {message}")
        self.warned += 1


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def read_frontmatter(path: Path) -> dict[str, str]:
    """Read simple YAML frontmatter key:value pairs (no external deps)."""
    if not path.is_file():
        return {}
    lines = read_text(path).splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if match:
            raw = match.group(2)
            # strip inline YAML comment ("value # comment" -> "value"); unquoted values only
            if not (raw.lstrip().startswith('"') or raw.lstrip().startswith("'")):
                raw = re.sub(r"\s+#.*$", "", raw)
            result[match.group(1)] = raw.strip().strip('"').strip("'")
    return result


def headings(text: str) -> set[str]:
    result: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if match:
            result.add(match.group(1).strip())
    return result


def section_text(text: str, title: str) -> str:
    lines = text.splitlines()
    start = None
    start_level = 0

    for idx, line in enumerate(lines):
        match = re.match(r"^(#{2,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        if match.group(2).strip() == title:
            start = idx + 1
            start_level = len(match.group(1))
            break

    if start is None:
        return ""

    end = len(lines)
    for idx in range(start, len(lines)):
        match = re.match(r"^(#{2,6})\s+(.+?)\s*$", lines[idx])
        if match and len(match.group(1)) <= start_level:
            end = idx
            break

    return "\n".join(lines[start:end])


def normalize_cell(value: str) -> str:
    return value.replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ").strip()


def split_table_row(line: str) -> list[str]:
    return [normalize_cell(cell) for cell in line.strip().strip("|").split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.match(r"^:?-{3,}:?$", cell.strip()) for cell in cells)


def markdown_tables(text: str) -> list[list[dict[str, str]]]:
    """Return Markdown pipe tables as row dictionaries.

    The parser intentionally supports the simple pipe-table shape used by ODK
    templates. It does not attempt to handle escaped pipes inside cells.
    """

    lines = text.splitlines()
    tables: list[list[dict[str, str]]] = []
    idx = 0

    while idx < len(lines) - 1:
        if not lines[idx].lstrip().startswith("|"):
            idx += 1
            continue

        header = split_table_row(lines[idx])
        separator = split_table_row(lines[idx + 1])
        if not is_separator_row(separator) or len(separator) != len(header):
            idx += 1
            continue

        idx += 2
        rows: list[dict[str, str]] = []
        while idx < len(lines) and lines[idx].lstrip().startswith("|"):
            cells = split_table_row(lines[idx])
            if len(cells) == len(header) and not is_separator_row(cells):
                rows.append(dict(zip(header, cells)))
            idx += 1
        tables.append(rows)

    return tables


def table_with_columns(text: str, required_columns: list[str]) -> list[dict[str, str]]:
    for table in markdown_tables(text):
        if not table:
            continue
        columns = set(table[0].keys())
        if all(column in columns for column in required_columns):
            return table
    return []


def meaningful(value: str) -> bool:
    return bool(value.strip()) and not PLACEHOLDER_RE.match(value)


def unresolved_markers(text: str) -> list[str]:
    markers: list[str] = []
    in_fence = False

    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        line_markers: list[str] = []
        line_markers.extend(match.group(0) for match in ARCHIVE_MARKER_RE.finditer(line))
        for match in BRACKET_PLACEHOLDER_RE.finditer(line):
            end = match.end()
            if end < len(line) and line[end] == "(":
                continue
            line_markers.append(match.group(0))

        if line_markers:
            markers.append(f"L{line_no}: {', '.join(line_markers)}")

    return markers


def sorted_ids(ids: set[str]) -> list[str]:
    def key(value: str) -> tuple[int, ...]:
        nums = re.findall(r"\d+", value)
        return tuple(int(num) for num in nums)

    return sorted(ids, key=key)


def validate_dir_name(change_dir: Path, reporter: Reporter) -> None:
    name = change_dir.name
    if re.match(r"^(issue-\d+-[a-z0-9-]+|draft-\d{8}-[a-z0-9-]+)$", name):
        reporter.pass_(f"change directory name is valid: {name}")
    else:
        reporter.fail(f"change directory name is invalid: {name}")


def validate_target_release(change_dir: Path, reporter: Reporter) -> None:
    proposal = change_dir / "proposal.md"
    frontmatter = read_frontmatter(proposal)
    value = frontmatter.get("target_release", "").strip()
    if not value:
        reporter.warn("proposal.md: target_release empty — set the target release version (e.g. 7.1)")
        return
    if LEGACY_TARGET_RELEASE_RE.match(value):
        migrated = re.sub(r"(?i)^OpenHarmony-", "", value)
        migrated = re.sub(r"(?i)-Release$", "", migrated)
        reporter.warn(
            f"proposal.md: target_release '{value}' uses legacy format — please unify to "
            f"'{migrated}' (R-OH-003: <major>.<minor>, e.g. 7.1)"
        )
        return
    if TARGET_RELEASE_RE.match(value):
        reporter.pass_(f"proposal.md: target_release '{value}' matches R-OH-003 format")
        return
    reporter.warn(
        f"proposal.md: target_release '{value}' does not match R-OH-003 (<major>.<minor>, "
        f"e.g. 7.1; or 7.1-Beta). Branch names (master/dev) are not release versions."
    )


def validate_required_artifacts(
    change_dir: Path,
    artifacts: dict[str, dict[str, object]],
    reporter: Reporter,
) -> dict[str, str]:
    files: dict[str, str] = {}

    print("\nLevel A: Artifact Files")
    for name, data in artifacts.items():
        if data.get("required") == "false":
            continue
        file_name = str(data.get("file", ""))
        if not file_name:
            continue
        files[name] = file_name
        path = change_dir / file_name
        if path.is_file():
            reporter.pass_(f"{file_name} exists")
        else:
            reporter.fail(f"{file_name} missing")

    return files


def validate_sections(
    change_dir: Path,
    artifacts: dict[str, dict[str, object]],
    files: dict[str, str],
    reporter: Reporter,
) -> None:
    print("\nLevel B: Required Sections")
    for name, file_name in files.items():
        path = change_dir / file_name
        if not path.is_file():
            continue
        present = headings(read_text(path))

        required = artifacts[name].get("required_sections", [])
        for section in required:  # type: ignore[assignment]
            if section in present:
                reporter.pass_(f"{file_name}: required section present: {section}")
            else:
                reporter.fail(f"{file_name}: required section missing: {section}")

        conditional = artifacts[name].get("conditional_sections", [])
        for section in conditional:  # type: ignore[assignment]
            if section in present:
                reporter.pass_(f"{file_name}: conditional section present: {section}")
            else:
                reporter.warn(f"{file_name}: conditional section absent: {section}")


def validate_present_optional_sections(
    change_dir: Path,
    artifacts: dict[str, dict[str, object]],
    reporter: Reporter,
) -> None:
    print("\nLevel B2: Optional Artifact Sections (when present)")
    for name, data in artifacts.items():
        if data.get("required") != "false":
            continue
        file_name = str(data.get("file", ""))
        if not file_name:
            continue
        path = change_dir / file_name
        if not path.is_file():
            continue  # optional artifact: absence is allowed; only check when present
        required = data.get("required_sections", [])
        if not required:
            continue
        present = headings(read_text(path))
        for section in required:  # type: ignore[assignment]
            if section in present:
                reporter.pass_(f"{file_name} (present optional): section present: {section}")
            else:
                reporter.fail(f"{file_name} (present optional): required section missing: {section}")


def validate_traceability(change_dir: Path, reporter: Reporter) -> None:
    spec_path = change_dir / "spec.md"
    plan_path = change_dir / "execution-plan.md"
    if not spec_path.is_file() or not plan_path.is_file():
        return

    print("\nLevel C: Traceability")

    spec = read_text(spec_path)
    plan = read_text(plan_path)

    spec_acs = set(AC_RE.findall(spec))
    if spec_acs:
        reporter.pass_(f"spec.md defines {len(spec_acs)} AC ids")
    else:
        reporter.fail("spec.md defines no AC ids")
        return

    verification = section_text(spec, "验证映射")
    verification_rows = table_with_columns(verification, ["AC", "验证方式"])
    if not verification_rows:
        reporter.fail("spec.md verification mapping table missing or empty")
    else:
        verification_acs = set()
        missing_methods: list[str] = []
        for row in verification_rows:
            row_acs = set(AC_RE.findall(row.get("AC", "")))
            verification_acs.update(row_acs)
            if row_acs and not meaningful(row.get("验证方式", "")):
                missing_methods.extend(sorted_ids(row_acs))
        missing = [ac for ac in sorted_ids(spec_acs) if ac not in verification_acs]
        if missing:
            reporter.fail("spec.md verification mapping missing AC ids: " + ", ".join(missing))
        elif missing_methods:
            reporter.fail("spec.md verification mapping has empty methods for: " + ", ".join(sorted_ids(set(missing_methods))))
        else:
            reporter.pass_("spec.md verification mapping covers all AC ids with methods")

    plan_trace = section_text(plan, "AC 到 Task 追溯")
    if not plan_trace:
        reporter.fail("execution-plan.md missing AC 到 Task 追溯 section body")
    else:
        trace_rows = table_with_columns(plan_trace, ["AC", "Task", "验证方式"])
        trace_acs = set()
        trace_tasks_from_rows: set[str] = set()
        missing_trace_methods: list[str] = []
        for row in trace_rows:
            row_acs = set(AC_RE.findall(row.get("AC", "")))
            trace_acs.update(row_acs)
            trace_tasks_from_rows.update(TASK_RE.findall(row.get("Task", "")))
            if row_acs and not meaningful(row.get("验证方式", "")):
                missing_trace_methods.extend(sorted_ids(row_acs))
        missing = [ac for ac in sorted_ids(spec_acs) if ac not in trace_acs]
        if missing:
            reporter.fail("execution-plan.md trace table missing AC ids: " + ", ".join(missing))
        elif missing_trace_methods:
            reporter.fail(
                "execution-plan.md trace table has empty verification methods for: "
                + ", ".join(sorted_ids(set(missing_trace_methods)))
            )
        elif not trace_tasks_from_rows:
            reporter.fail("execution-plan.md trace table has no Task mappings")
        else:
            reporter.pass_("execution-plan.md trace table covers all spec AC ids with verification methods")

    # Code mapping moved from spec.md to execution-plan.md (#90 方案 D); AC→code→Task coverage is verified by the execution-plan trace table check above.

    plan_tasks = set(TASK_RE.findall(plan))
    if plan_tasks:
        reporter.pass_(f"execution-plan.md defines {len(plan_tasks)} Task ids")
    else:
        reporter.fail("execution-plan.md defines no Task ids")

    trace_tasks = set(TASK_RE.findall(plan_trace))
    detail_headings = set(re.findall(r"^###\s+(TASK-\d+)\b", plan, flags=re.MULTILINE))
    missing_details = [task for task in sorted_ids(trace_tasks) if task not in detail_headings]
    if missing_details:
        reporter.fail("execution-plan.md missing Task detail sections: " + ", ".join(missing_details))
    elif trace_tasks:
        reporter.pass_("all traced Task ids have detail sections")

    task_list = section_text(plan, "Task 列表")
    task_rows = table_with_columns(task_list, ["TASK ID", "AC 映射", "完成判据", "验证命令"])
    if not task_rows:
        reporter.fail("execution-plan.md Task 列表 table missing or empty")
    else:
        task_ids = set()
        incomplete_tasks: list[str] = []
        for row in task_rows:
            ids = set(TASK_RE.findall(row.get("TASK ID", "")))
            task_ids.update(ids)
            for task_id in ids:
                if (
                    not meaningful(row.get("AC 映射", ""))
                    or not meaningful(row.get("完成判据", ""))
                    or not meaningful(row.get("验证命令", ""))
                ):
                    incomplete_tasks.append(task_id)
        missing_task_rows = [task for task in sorted_ids(trace_tasks) if task not in task_ids]
        if missing_task_rows:
            reporter.fail("execution-plan.md Task 列表 missing traced Task ids: " + ", ".join(missing_task_rows))
        elif incomplete_tasks:
            reporter.fail("execution-plan.md Task 列表 has incomplete rows: " + ", ".join(sorted_ids(set(incomplete_tasks))))
        else:
            reporter.pass_("execution-plan.md Task 列表 covers traced Tasks with ACs and verification commands")

    task_details = section_text(plan, "Task 详情")
    incomplete_detail_sections: list[str] = []
    for task_id in sorted_ids(trace_tasks):
        pattern = re.compile(
            rf"^###\s+{re.escape(task_id)}\b.*?$([\s\S]*?)(?=^###\s+TASK-\d+\b|\Z)",
            flags=re.MULTILINE,
        )
        match = pattern.search(task_details)
        detail = match.group(1) if match else ""
        files_rows = table_with_columns(detail, ["操作", "文件", "说明"])
        verification_rows = table_with_columns(detail, ["Command / Evidence", "Expected Result", "Actual Result"])
        if not files_rows or not verification_rows:
            incomplete_detail_sections.append(task_id)
            continue
        if any(not meaningful(row.get("文件", "")) for row in files_rows):
            incomplete_detail_sections.append(task_id)
            continue
        if any(not meaningful(row.get("Command / Evidence", "")) or not meaningful(row.get("Expected Result", "")) for row in verification_rows):
            incomplete_detail_sections.append(task_id)
    if incomplete_detail_sections:
        reporter.fail("execution-plan.md Task details missing Files/Verification evidence: " + ", ".join(incomplete_detail_sections))
    elif trace_tasks:
        reporter.pass_("execution-plan.md Task details include file scopes and expected verification")


def validate_optional_evidence(change_dir: Path, reporter: Reporter) -> None:
    print("\nOptional Evidence")
    for rel in ("evidence/reviews", "evidence/gates"):
        path = change_dir / rel
        if not path.exists():
            reporter.warn(f"{rel} absent (optional)")
            continue
        if not path.is_dir():
            reporter.fail(f"{rel} exists but is not a directory")
            continue
        files = [child for child in path.iterdir() if child.is_file()]
        if files:
            reporter.pass_(f"{rel} contains {len(files)} evidence file(s)")
        else:
            reporter.fail(f"{rel} exists but contains no evidence files")


def validate_archive_placeholders(
    change_dir: Path,
    artifacts: dict[str, dict[str, object]],
    files: dict[str, str],
    reporter: Reporter,
) -> bool:
    print("\nLevel D: Archive Readiness")
    unresolved = False

    for name, file_name in files.items():
        path = change_dir / file_name
        if not path.is_file():
            continue

        text = read_text(path)
        sections = list(artifacts[name].get("required_sections", []))  # type: ignore[arg-type]
        file_markers: list[str] = []
        for section in sections:
            body = section_text(text, str(section))
            file_markers.extend(unresolved_markers(body))

        if file_markers:
            unresolved = True
            reporter.fail(f"{file_name}: unresolved archive placeholders: " + "; ".join(file_markers[:8]))
        else:
            reporter.pass_(f"{file_name}: no unresolved placeholders in required sections")

    return unresolved


def validate_archive_spec_mapping(change_dir: Path, reporter: Reporter) -> None:
    # Code mapping (AC→file+Task+verification status) moved from spec.md to execution-plan.md (#90 方案 D).
    plan_path = change_dir / "execution-plan.md"
    if not plan_path.is_file():
        return

    plan = read_text(plan_path)
    ac_task = section_text(plan, "AC 到 Task 追溯")
    rows = table_with_columns(ac_task, ["AC", "Task", "验证状态（Pass/Fail/Blocked）"])
    if not rows:
        reporter.fail("execution-plan.md AC-to-Task traceability table missing required archive columns")
        return

    incomplete: list[str] = []
    invalid_status: list[str] = []
    for row in rows:
        acs = sorted_ids(set(AC_RE.findall(row.get("AC", "")))) or ["<unknown AC>"]
        if (
            not meaningful(row.get("Task", ""))
            or not meaningful(row.get("验证状态（Pass/Fail/Blocked）", ""))
        ):
            incomplete.extend(acs)
            continue
        status = row.get("验证状态（Pass/Fail/Blocked）", "").strip().lower()
        if status not in {"pass", "fail", "blocked"}:
            invalid_status.extend(acs)

    if incomplete:
        reporter.fail("execution-plan.md AC-to-Task traceability has archive-empty rows: " + ", ".join(sorted_ids(set(incomplete))))
    elif invalid_status:
        reporter.fail("execution-plan.md AC-to-Task traceability has invalid verification status: " + ", ".join(sorted_ids(set(invalid_status))))
    else:
        reporter.pass_("execution-plan.md AC-to-Task traceability archive fields are complete")

    # Archive closure: each traced Task must have a non-empty file in 代码范围映射 (AC→code→Task loop).
    code_scope = section_text(plan, "代码范围映射")
    scope_rows = table_with_columns(code_scope, ["TASK ID", "文件"]) if code_scope else []
    task_to_file: dict[str, str] = {}
    for sr in scope_rows:
        for tid in TASK_RE.findall(sr.get("TASK ID", "")):
            task_to_file[tid] = sr.get("文件", "").strip()
    traced_tasks: set[str] = set()
    for row in rows:
        traced_tasks.update(TASK_RE.findall(row.get("Task", "")))
    tasks_without_file = [t for t in traced_tasks if t not in task_to_file or not meaningful(task_to_file.get(t, ""))]
    if tasks_without_file:
        reporter.fail("execution-plan.md 代码范围映射 missing file for traced Tasks: " + ", ".join(sorted(set(tasks_without_file))))
    else:
        reporter.pass_("execution-plan.md 代码范围映射 covers all traced Tasks with files")


def validate_archive_actual_results(change_dir: Path, reporter: Reporter) -> None:
    plan_path = change_dir / "execution-plan.md"
    if not plan_path.is_file():
        return

    plan = read_text(plan_path)
    task_details = section_text(plan, "Task 详情")
    detail_tasks = set(re.findall(r"^###\s+(TASK-\d+)\b", task_details, flags=re.MULTILINE))
    missing_actual: list[str] = []

    for task_id in sorted_ids(detail_tasks):
        pattern = re.compile(
            rf"^###\s+{re.escape(task_id)}\b.*?$([\s\S]*?)(?=^###\s+TASK-\d+\b|\Z)",
            flags=re.MULTILINE,
        )
        match = pattern.search(task_details)
        detail = match.group(1) if match else ""
        rows = table_with_columns(detail, ["Command / Evidence", "Expected Result", "Actual Result"])
        if not rows or any(not meaningful(row.get("Actual Result", "")) for row in rows):
            missing_actual.append(task_id)

    if missing_actual:
        reporter.fail("execution-plan.md Verification tables have empty Actual Result: " + ", ".join(missing_actual))
    elif detail_tasks:
        reporter.pass_("execution-plan.md Verification tables have Actual Result filled")


def validate_archive_evidence_claims(change_dir: Path, unresolved_required: bool, reporter: Reporter) -> None:
    if not unresolved_required:
        reporter.pass_("evidence readiness claims are consistent with required artifacts")
        return

    evidence_root = change_dir / "evidence"
    if not evidence_root.is_dir():
        reporter.warn("evidence absent while required artifacts still have unresolved archive markers")
        return

    conflicting: list[str] = []
    for path in evidence_root.rglob("*.md"):
        text = read_text(path)
        if ARCHIVE_READY_CLAIM_RE.search(text):
            conflicting.append(str(path.relative_to(change_dir)))

    if conflicting:
        reporter.fail("evidence claims readiness while required artifacts have unresolved markers: " + ", ".join(conflicting))
    else:
        reporter.pass_("evidence does not claim readiness while required artifacts have unresolved markers")


def validate_archive_readiness(
    change_dir: Path,
    artifacts: dict[str, dict[str, object]],
    files: dict[str, str],
    reporter: Reporter,
) -> None:
    unresolved_required = validate_archive_placeholders(change_dir, artifacts, files, reporter)
    validate_archive_spec_mapping(change_dir, reporter)
    validate_archive_actual_results(change_dir, reporter)
    validate_archive_evidence_claims(change_dir, unresolved_required, reporter)


def main(argv: list[str]) -> int:
    parser = ArgumentParser(description="Validate one ODK change directory against ODK runtime assets.")
    parser.add_argument("change_dir", help="ODK change directory, for example .codespec/changes/issue-123-demo")
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Enable strict final-readiness checks: unresolved placeholders, filled code mapping, and Actual Result evidence.",
    )
    args = parser.parse_args(argv[1:])

    change_dir = Path(args.change_dir).resolve()
    reporter = Reporter()

    if not change_dir.is_dir():
        print(f"Change directory does not exist: {change_dir}", file=sys.stderr)
        return 1

    artifacts = parse_contract_artifacts(str(ASSET_ROOT / "contracts" / "artifacts.yaml"))

    mode = "archive" if args.archive else "draft"
    print(f"Validating ODK artifact contract ({mode} mode): {change_dir}")
    print("\nLevel A: Change Directory")
    validate_dir_name(change_dir, reporter)
    validate_target_release(change_dir, reporter)
    files = validate_required_artifacts(change_dir, artifacts, reporter)
    validate_sections(change_dir, artifacts, files, reporter)
    validate_present_optional_sections(change_dir, artifacts, reporter)
    validate_traceability(change_dir, reporter)
    validate_optional_evidence(change_dir, reporter)
    if args.archive:
        validate_archive_readiness(change_dir, artifacts, files, reporter)

    print("\nSummary:")
    print(f"  Passed:   {reporter.passed}")
    print(f"  Warnings: {reporter.warned}")
    print(f"  Failed:   {reporter.failed}")

    return 0 if reporter.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
