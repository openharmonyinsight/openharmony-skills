#!/usr/bin/env python3
"""Validate one ODK change directory against the active artifacts contract.

This is stricter than validate-artifacts-structural.sh:
- required artifacts must exist
- required sections must be present exactly as Markdown headings
- conditional sections are reported as warnings when absent
- spec ACs must be traceable into execution-plan and code mapping
- optional evidence directories, if present, must contain files

It intentionally avoids external dependencies.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
# Source layout: scripts/validate-artifacts-contract.py → ROOT = repo root, contracts at core/contracts/
# Published layout: runtime/executables/validate-artifacts-contract.py → contracts at runtime/assets/contracts/
_SOURCE_CONTRACT = SCRIPT_DIR.parent / "core" / "contracts" / "artifacts.yaml"
_PUBLISHED_CONTRACT = SCRIPT_DIR.parent / "assets" / "contracts" / "artifacts.yaml"
CONTRACT_PATH = _SOURCE_CONTRACT if _SOURCE_CONTRACT.is_file() else _PUBLISHED_CONTRACT

# Lib path: source layout scripts/lib/, published layout runtime/executables/lib/
_SOURCE_LIB = SCRIPT_DIR.parent / "scripts" / "lib"
_PUBLISHED_LIB = SCRIPT_DIR / "lib"
sys.path.insert(0, str(_SOURCE_LIB if _SOURCE_LIB.is_dir() else _PUBLISHED_LIB))

from odk_yaml import parse_contract_artifacts, parse_resource_contract  # noqa: E402


AC_RE = re.compile(r"\bAC-\d+(?:\.\d+)?\b")
AC_DEF_RE = re.compile(r"^\s*[-*]\s+\*\*AC-\d+(?:\.\d+)?:\*\*", re.MULTILINE)
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
    r"\[(?:[^\]\n]*(?:引用|标题|角色|功能|价值|条件|填写|描述|说明|编号|名称|路径|模块|文件|命令|证据|结果|对象|模式|策略|事件|待|TBD|TODO)[^\]\n]*)\]",
    re.IGNORECASE,
)
ARCHIVE_READY_CLAIM_RE = re.compile(r"\b(?:PASS|Ready)\b|通过|可归档|归档就绪", re.IGNORECASE)
LEGACY_TARGET_RELEASE_RE = re.compile(
    r"^OpenHarmony-\d+\.\d+(?:-(?:Release|Beta|Alpha|Dev))?$",
    re.IGNORECASE,
)
TARGET_RELEASE_RE = re.compile(r"^\d+\.\d+(?:-(?:Release|Beta|Alpha|Dev))?$", re.IGNORECASE)
_NOT_APPLICABLE_RE = re.compile(r"不涉及")
_NOT_APPLICABLE_REASON_RE = re.compile(r"不涉及理由[：:]\s*(.+)", re.MULTILINE)
_DFX_INVOLVED_REPOS_RE = re.compile(r"涉及仓库[：:]\s*(.+)", re.MULTILINE)
_DFX_REPO_NAME_RE = re.compile(r"[A-Za-z0-9_./-]+")
_DFX_REPO_STATUS_COLUMNS = ["仓库", "状态", "理由"]
_DFX_REPO_STATUSES = {"READ", "UNREACHABLE", "NO_DFX_KNOWLEDGE"}
_DFX_READ_NO_HIT_REASONS = {"知识库无命中", "知识库无匹配命中"}
DFX_SOURCE_REF_RE = re.compile(
    r"^[^@\s|]+@[0-9a-fA-F]{7,40}:docs/dfx/fmea\.yaml#[^#\s|]+$"
)


RESOURCE_CONTRACT = parse_resource_contract(str(CONTRACT_PATH))


def contract_scalar(key: str) -> str:
    value = RESOURCE_CONTRACT.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{CONTRACT_PATH}: resource_contract.{key} must be a scalar")
    return value


def contract_list(key: str) -> list[str]:
    value = RESOURCE_CONTRACT.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{CONTRACT_PATH}: resource_contract.{key} must be a non-empty list")
    return value


RESOURCE_SECTIONS = dict(item.split("=", 1) for item in contract_list("conditional_sections"))
IMPACT_STATES = set(contract_list("impact_states"))
ACTIVE_WHEN_STATES = set(contract_list("active_when_states"))
DIMENSION_LABELS = dict(item.split("=", 1) for item in contract_list("dimension_labels"))
LABEL_TO_DIMENSION: dict[str, str] = {}
for dim_key, dim_label in DIMENSION_LABELS.items():
    LABEL_TO_DIMENSION[dim_label] = dim_key
    LABEL_TO_DIMENSION[dim_key] = dim_key
PROPOSAL_SECTION = contract_scalar("proposal_section")
PROPOSAL_COLUMNS = contract_list("proposal_columns")
EVIDENCE_ROOT = contract_scalar("evidence_root")



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


def table_has_columns(text: str, required_columns: list[str]) -> bool:
    """Check if text contains a markdown table with the required column names (even if no data rows)."""
    for table in markdown_tables(text):
        if table:
            columns = set(table[0].keys())
            if all(column in columns for column in required_columns):
                return True
        else:
            # Header-only table: parse the header line directly
            for line in text.splitlines():
                if line.lstrip().startswith("|"):
                    header = split_table_row(line)
                    if all(col in header for col in required_columns):
                        return True
    return False


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


def _parse_not_applicable(subsection_text: str) -> bool:
    """Check if the subsection contains '不涉及' text."""
    return bool(_NOT_APPLICABLE_RE.search(subsection_text))


def _parse_not_applicable_reason(subsection_text: str) -> str:
    """Parse the reason annotation from a 不涉及 DFX section.

    Looks for a block-quote line like: > 不涉及理由：仓不可达（arkui_ace_engine）
    Also matches non-block-quote format: 不涉及理由：仓无 DFX 知识
    """
    match = _NOT_APPLICABLE_REASON_RE.search(subsection_text)
    return match.group(1).strip() if match else ""


def _visible_markdown(text: str) -> str:
    """Remove template guidance that must not count as user-supplied evidence."""
    return re.sub(r"<!--[\s\S]*?-->", "", text)


def _parse_dfx_involved_repos(subsection_text: str) -> list[str]:
    """Parse the canonical repository set from ``> 涉及仓库：repo-a, repo-b``."""
    match = _DFX_INVOLVED_REPOS_RE.search(subsection_text)
    if not match:
        return []
    return [
        item.strip().strip("`")
        for item in re.split(r"[,，、;；+]", match.group(1))
        if item.strip().strip("`")
    ]


def _parse_module_impact_repos(design_text: str) -> list[str]:
    """Read the canonical involved repository set from ``## 模块影响``."""
    module_section = section_text(design_text, "模块影响")
    rows = table_with_columns(module_section, ["仓库"])
    repos: list[str] = []
    for row in rows:
        for item in re.split(r"[,，、;；+]", row.get("仓库", "")):
            repo = item.strip().strip("`")
            if repo and repo not in repos:
                repos.append(repo)
    return repos


def validate_dfx_no_hit_closure(
    subsection_text: str,
    module_repos: list[str],
    reporter: Reporter,
    archive_mode: bool,
) -> bool:
    """Validate per-repository closure for a DFX ``不涉及`` conclusion.

    Returns True when the structured contract was handled. Draft keeps legacy
    free-text reasons as a compatibility path; Archive requires this contract.
    """
    involved_repos = _parse_dfx_involved_repos(subsection_text)
    status_rows = table_with_columns(subsection_text, _DFX_REPO_STATUS_COLUMNS)
    structured_present = bool(involved_repos or status_rows)
    if not structured_present and not archive_mode:
        return False

    issues: list[str] = []
    if not involved_repos:
        issues.append("missing 涉及仓库 declaration")
    if not module_repos:
        issues.append("模块影响 table has no repositories")
    if not status_rows:
        issues.append("missing 仓库/状态/理由 closure table")

    invalid_repo_names = [repo for repo in involved_repos if not _DFX_REPO_NAME_RE.fullmatch(repo)]
    if invalid_repo_names:
        issues.append("invalid involved repository names: " + ", ".join(invalid_repo_names))
    duplicate_involved = sorted({repo for repo in involved_repos if involved_repos.count(repo) > 1})
    if duplicate_involved:
        issues.append("duplicate involved repositories: " + ", ".join(duplicate_involved))

    row_repos: list[str] = []
    for index, row in enumerate(status_rows, start=1):
        repo = row.get("仓库", "").strip().strip("`")
        status = row.get("状态", "").strip()
        reason = row.get("理由", "").strip()
        label = repo or f"row {index}"
        if not meaningful(repo) or not _DFX_REPO_NAME_RE.fullmatch(repo):
            issues.append(f"{label}: invalid or missing 仓库")
            continue
        row_repos.append(repo)
        if status not in _DFX_REPO_STATUSES:
            issues.append(f"{repo}: unknown 状态 '{status}'")
        elif status == "UNREACHABLE":
            issues.append(f"{repo}: UNREACHABLE cannot close Archive")
        elif status == "READ" and reason not in _DFX_READ_NO_HIT_REASONS:
            issues.append(f"{repo}: READ no-hit closure has non-canonical reason '{reason}'")
        elif status == "NO_DFX_KNOWLEDGE" and reason != "仓无 DFX 知识":
            issues.append(f"{repo}: NO_DFX_KNOWLEDGE requires a 仓无 DFX 知识 reason")
        if not meaningful(reason):
            issues.append(f"{repo}: missing 理由")

    duplicate_rows = sorted({repo for repo in row_repos if row_repos.count(repo) > 1})
    if duplicate_rows:
        issues.append("duplicate repository closure rows: " + ", ".join(duplicate_rows))

    declared = set(involved_repos)
    canonical = set(module_repos)
    undeclared = sorted(canonical - declared)
    wrongly_declared = sorted(declared - canonical)
    if undeclared:
        issues.append("模块影响 repositories missing from 涉及仓库: " + ", ".join(undeclared))
    if wrongly_declared:
        issues.append("涉及仓库 entries absent from 模块影响: " + ", ".join(wrongly_declared))

    expected = canonical or declared
    actual = set(row_repos)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        issues.append("repositories missing closure: " + ", ".join(missing))
    if extra:
        issues.append("closure rows not declared in 涉及仓库: " + ", ".join(extra))

    if issues:
        draft_warn_archive_fail(
            reporter,
            archive_mode,
            "design.md: incomplete DFX per-repository no-hit closure: " + "; ".join(issues),
        )
    else:
        reporter.pass_("DFX no-hit conclusion has complete per-repository closure")
    return True


def draft_warn_archive_fail(reporter: Reporter, archive: bool, message: str) -> None:
    reporter.fail(message) if archive else reporter.warn(message)


def resource_decision_fields(value: str) -> dict[str, str]:
    """Parse ``确认人=...; 理由=...; 范围=...`` from one table cell."""

    fields: dict[str, str] = {}
    for part in re.split(r"[;；]", value):
        match = re.fullmatch(r"\s*(确认人|理由|范围)\s*[:=：]\s*(.+?)\s*", part)
        if match and meaningful(match.group(2)):
            fields[match.group(1)] = match.group(2).strip()
    return fields


def resource_decisions(value: str) -> list[dict[str, str]]:
    chunks = re.split(r"\s*<br\s*/?>\s*|\n+", value, flags=re.IGNORECASE)
    return [fields for chunk in chunks if (fields := resource_decision_fields(chunk))]


def complete_resource_decision(decision: dict[str, str]) -> bool:
    return set(decision) == {"确认人", "理由", "范围"}


def parse_resource_impact_states(proposal: str) -> tuple[dict[str, str], list[str]]:
    """Return (dimension_key -> state, issues) from proposal 资源开销审视."""

    section = section_text(proposal, PROPOSAL_SECTION)
    rows = table_with_columns(section, PROPOSAL_COLUMNS)
    issues: list[str] = []
    states: dict[str, str] = {}
    if not rows:
        return {}, [f"proposal section {PROPOSAL_SECTION} missing or incomplete impact table"]

    for row in rows:
        label = row.get("维度", "").strip()
        dim_key = LABEL_TO_DIMENSION.get(label)
        if dim_key is None:
            issues.append(f"unknown resource impact dimension: {label or '<empty>'}")
            continue
        if dim_key in states:
            issues.append(f"duplicate resource impact dimension: {label}")
            continue
        state = row.get("状态", "").strip()
        if state not in IMPACT_STATES:
            issues.append(f"{label} has invalid impact state: {state or '<empty>'}")
            continue
        states[dim_key] = state
        if not meaningful(row.get("信号/依据", "")):
            issues.append(f"{label} {state} requires 信号/依据")
        decisions = resource_decisions(row.get("确认人/理由/范围", ""))
        if state in {"not-applicable", "waived"} and (
            not decisions or not all(complete_resource_decision(item) for item in decisions)
        ):
            issues.append(f"{label} {state} requires 确认人/理由/范围")

    expected = set(DIMENSION_LABELS.keys())
    missing = expected - set(states)
    if missing:
        issues.append(
            "resource impact table missing dimensions: "
            + ", ".join(DIMENSION_LABELS[key] for key in sorted(missing))
        )
    return states, issues


def parse_eight_dim_performance_involvement(proposal: str) -> str | None:
    """Return 是/否 from 不涉及项确认「性能」row, or None if the row is absent."""

    section = section_text(proposal, "不涉及项确认")
    if not section:
        return None
    rows = table_with_columns(section, ["维度", "是否涉及"])
    for row in rows:
        if row.get("维度", "").strip() != "性能":
            continue
        cell = row.get("是否涉及", "").strip()
        if not cell:
            return None
        first = cell.split()[0] if cell.split() else cell
        if first.startswith("是"):
            return "是"
        if first.startswith("否"):
            return "否"
        return first
    return None


def check_performance_summary_vs_impact(
    proposal: str,
    states: dict[str, str],
    reporter: Reporter,
    *,
    archive: bool,
) -> None:
    """Cross-check 8-dim 性能 against the performance resource state only."""

    actual = parse_eight_dim_performance_involvement(proposal)
    if actual is None:
        return
    performance_state = states.get("performance")
    expected = "是" if performance_state in {"required", "review-required"} else "否"
    if actual != expected:
        draft_warn_archive_fail(
            reporter,
            archive,
            "不涉及项确认「性能」must be "
            f"{expected} when 性能 state is {performance_state} (got {actual})",
        )


def resource_section_has_meaningful_content(document: str, section: str) -> bool:
    """Accept subsystem-owned schemas while rejecting empty/placeholder sections."""

    body = section_text(document, section)
    if not body.strip():
        return False
    for table in markdown_tables(body):
        for row in table:
            values = list(row.values())
            if values and all(meaningful(value) for value in values):
                return True
    prose = re.sub(r"<!--[\s\S]*?-->", "", body)
    for line in prose.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("|", "#", ">")):
            continue
        if meaningful(stripped):
            return True
    return False


AGENTS_RESOURCE_GATE_KEY = "odk_resource_gate"


def discover_resource_gate(repository: Path) -> Path | None:
    """Return AGENTS.md-declared resource gate path, or None if undeclared."""

    agents = repository / "AGENTS.md"
    if not agents.is_file():
        return None
    try:
        text = agents.read_text(encoding="utf-8")
    except OSError:
        return None
    pattern = re.compile(
        rf"^\s*{AGENTS_RESOURCE_GATE_KEY}\s*[:=]\s*([^\s#]+)\s*(?:#.*)?$",
        re.MULTILINE,
    )
    matches = pattern.findall(text)
    if not matches:
        return None
    if len(matches) > 1:
        raise ValueError(f"{agents}: duplicate {AGENTS_RESOURCE_GATE_KEY} declarations")
    raw = matches[0].strip().strip("`'\"")
    relative = Path(raw)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ValueError(f"{agents}: {AGENTS_RESOURCE_GATE_KEY} must be a repo-relative path")
    candidate = (repository / relative).resolve()
    try:
        candidate.relative_to(repository.resolve())
    except ValueError as exc:
        raise ValueError(
            f"{agents}: {AGENTS_RESOURCE_GATE_KEY} escapes the workspace"
        ) from exc
    return candidate


def find_repository_root(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


RESOURCE_GATE_TIMEOUT_SEC = 300


def run_resource_gate(
    repository: Path,
    gate: Path,
    change_dir: Path,
    *,
    timeout_sec: int = RESOURCE_GATE_TIMEOUT_SEC,
) -> tuple[int, str]:
    """Execute subsystem archive gate; return (exit_code, combined_output).

    Always invoked as: ``<gate> <change-dir> --archive`` with cwd = repository root.
    ``.py`` gates run via the current Python interpreter; non-executable scripts via bash.
    Times out after ``timeout_sec`` (default 300s) and returns exit code 124.
    """

    cmd = [str(gate), str(change_dir), "--archive"]
    if gate.suffix == ".py":
        cmd = [sys.executable, *cmd]
    elif not os.access(gate, os.X_OK):
        cmd = ["bash", *cmd]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(repository),
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired as exc:
        partial = ""
        if exc.stdout:
            partial += exc.stdout if isinstance(exc.stdout, str) else exc.stdout.decode()
        if exc.stderr:
            partial += exc.stderr if isinstance(exc.stderr, str) else exc.stderr.decode()
        msg = (
            f"resource gate timed out after {timeout_sec}s: "
            f"{gate.name} (raise timeout or fix hung gate)\n"
        )
        return 124, partial + msg
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode, output


def validate_resource_constraints(
    change_dir: Path,
    reporter: Reporter,
    *,
    archive: bool,
) -> None:
    """Thin resource checks: impact states, section presence, external archive gate."""

    proposal_path = change_dir / "proposal.md"
    if not proposal_path.is_file():
        return

    proposal = read_text(proposal_path)
    states, state_issues = parse_resource_impact_states(proposal)
    if state_issues:
        draft_warn_archive_fail(
            reporter,
            archive,
            "resource impact states missing or invalid: " + "; ".join(state_issues),
        )
        return

    check_performance_summary_vs_impact(proposal, states, reporter, archive=archive)

    if archive and any(state == "review-required" for state in states.values()):
        reporter.fail(
            "resource archive blocked: review-required dimensions must resolve to "
            "required/waived/not-applicable with rationale"
        )
        return

    active = any(state in ACTIVE_WHEN_STATES for state in states.values())

    if not active:
        conflicts: list[str] = []
        for file_name, section in RESOURCE_SECTIONS.items():
            path = change_dir / file_name
            if path.is_file() and section in headings(read_text(path)):
                conflicts.append(file_name)
        evidence = change_dir / EVIDENCE_ROOT
        if evidence.exists():
            conflicts.append(EVIDENCE_ROOT)
        if conflicts:
            draft_warn_archive_fail(
                reporter,
                archive,
                "resource content conflicts with inactive trigger: " + ", ".join(conflicts),
            )
        else:
            reporter.pass_("resource constraints not triggered")
        return

    missing: list[str] = []
    incomplete: list[str] = []
    for file_name, section in RESOURCE_SECTIONS.items():
        path = change_dir / file_name
        if not path.is_file() or section not in headings(read_text(path)):
            missing.append(section)
            continue
        if not resource_section_has_meaningful_content(read_text(path), section):
            incomplete.append(section)
    if missing:
        draft_warn_archive_fail(
            reporter,
            archive,
            "resource chain active but missing sections: " + ", ".join(missing),
        )
    if incomplete:
        draft_warn_archive_fail(
            reporter,
            archive,
            "resource chain active but sections are empty or placeholder-only: "
            + ", ".join(incomplete),
        )
    if not missing and not incomplete:
        reporter.pass_("resource conditional sections contain meaningful content")

    if not archive:
        return
    if missing or incomplete:
        return

    repository = find_repository_root(change_dir)
    if repository is None:
        reporter.fail("resource archive requires a git repository to resolve odk_resource_gate")
        return
    try:
        gate = discover_resource_gate(repository)
    except ValueError as exc:
        reporter.fail(str(exc))
        return
    if gate is None:
        reporter.fail(
            "resource archive blocked: any dimension is required but AGENTS.md does not "
            f"declare {AGENTS_RESOURCE_GATE_KEY}: <repo-relative-path>"
        )
        return
    if not gate.is_file():
        reporter.fail(f"resource archive blocked: gate file missing: {gate}")
        return

    code, output = run_resource_gate(repository, gate, change_dir)
    if output.strip():
        print(output, end="" if output.endswith("\n") else "\n")
    if code != 0:
        reporter.fail(f"resource gate failed: {gate.relative_to(repository)} exit {code}")
    else:
        reporter.pass_(f"resource gate passed: {gate.relative_to(repository)}")


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
            if section in RESOURCE_SECTIONS.values():
                continue  # trigger-aware checks live in validate_resource_constraints
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
        text = read_text(path)
        present = headings(text)
        for section in required:  # type: ignore[assignment]
            if section in present:
                reporter.pass_(f"{file_name} (present optional): section present: {section}")
                # Also check that section's tables have non-placeholder data rows
                body = section_text(text, str(section))
                all_tables = markdown_tables(body)
                if all_tables:
                    for table in all_tables:
                        non_placeholder_rows = [
                            row for row in table
                            if any(meaningful(v) for v in row.values())
                        ]
                        if not non_placeholder_rows:
                            reporter.warn(f"{file_name} (present optional): section '{section}' table has no non-placeholder data rows")
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

    spec_acs = set(AC_RE.findall("\n".join(AC_DEF_RE.findall(spec))))
    if spec_acs:
        reporter.pass_(f"spec.md defines {len(spec_acs)} AC ids")
    else:
        reporter.fail("spec.md defines no AC ids (looking for '- **AC-N.M:**' definition lines)")
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


def validate_dfx_constraints(change_dir: Path, reporter: Reporter, archive_mode: bool) -> None:
    design_path = change_dir / "design.md"
    if not design_path.is_file():
        return

    print("\nLevel C2: DFX Fault Mode Coverage")

    design = read_text(design_path)
    dfx_section = section_text(design, "DFX 设计")
    if not dfx_section:
        # design.md missing the DFX H2 is reported by the section validator.
        return

    # Try new format (DFX 故障模式分析) first; fall back to legacy format (DFX 约束清单)
    fault_subsection = section_text(dfx_section, "DFX 故障模式分析")
    if not fault_subsection:
        # Try legacy format
        constraint_subsection = section_text(dfx_section, "DFX 约束清单")
        if constraint_subsection:
            draft_warn_archive_fail(
                reporter,
                archive_mode,
                "design.md: uses legacy format with '### DFX 约束清单' — "
                "migrate to '### DFX 故障模式分析' (9-column table)"
            )
            return
        reporter.fail("design.md: ### DFX 故障模式分析 subsection missing under ## DFX 设计")
        return

    # Every hit must include a pinned repository/commit/path/record provenance.
    required_dfx_columns = [
        "分析对象", "故障模式", "故障影响", "故障原因",
        "严酷度", "恢复措施", "关键日志", "大数据打点事件", "来源",
    ]
    visible_fault_subsection = _visible_markdown(fault_subsection)
    if not table_has_columns(visible_fault_subsection, required_dfx_columns):
        missing = [
            c for c in required_dfx_columns
            if not table_has_columns(visible_fault_subsection, [c])
        ]
        reporter.fail(
            f"design.md: DFX 故障模式分析 table missing required columns: {', '.join(missing)}"
        )
        return

    fault_rows = table_with_columns(visible_fault_subsection, required_dfx_columns)

    has_data_rows = False
    invalid_rows: list[str] = []
    for row in fault_rows:
        analysis_obj = row.get("分析对象", "").strip()
        if meaningful(analysis_obj):
            has_data_rows = True
            missing_values = [
                column for column in required_dfx_columns
                if not meaningful(row.get(column, ""))
            ]
            if missing_values:
                invalid_rows.append(f"{analysis_obj}: missing {', '.join(missing_values)}")
                continue
            source_ref = row.get("来源", "").strip()
            if not DFX_SOURCE_REF_RE.fullmatch(source_ref):
                invalid_rows.append(
                    f"{analysis_obj}: invalid 来源 '{source_ref}' "
                    "(expected <repo>@<commit>:docs/dfx/fmea.yaml#<record-id>)"
                )

    if has_data_rows:
        if invalid_rows:
            reporter.fail("design.md: invalid DFX rows: " + "; ".join(invalid_rows))
        else:
            reporter.pass_("DFX fault mode analysis has complete, traceable data rows")
    else:
        # 检查是否有"不涉及"文本
        if _parse_not_applicable(visible_fault_subsection):
            module_repos = _parse_module_impact_repos(design)
            if validate_dfx_no_hit_closure(
                visible_fault_subsection, module_repos, reporter, archive_mode
            ):
                return
            reason = _parse_not_applicable_reason(visible_fault_subsection)
            if reason:
                if "仓不可达" in reason:
                    if archive_mode:
                        reporter.fail(
                            "design.md: DFX 故障模式分析 不涉及（仓不可达）— "
                            "归档时不允许仓不可达，请确认非网络问题后重新分析"
                        )
                    else:
                        reporter.warn(
                            "design.md: DFX 故障模式分析 不涉及（仓不可达）— "
                            "归档前请确认非网络临时问题导致漏查"
                        )
                elif "仓无 DFX 知识" in reason or "仓无FMEA知识" in reason:
                    reporter.pass_(
                        "design.md: DFX 故障模式分析 不涉及（仓无 DFX 知识；"
                        "Draft 兼容，Archive 需逐仓闭包）"
                    )
                elif "无命中" in reason:
                    reporter.pass_(
                        "design.md: DFX 故障模式分析 不涉及（知识库无匹配命中；"
                        "Draft 兼容，Archive 需逐仓闭包）"
                    )
                else:
                    draft_warn_archive_fail(
                        reporter,
                        archive_mode,
                        f"design.md: DFX 故障模式分析 不涉及（理由：{reason}）"
                    )
            else:
                draft_warn_archive_fail(
                    reporter,
                    archive_mode,
                    "design.md: DFX 故障模式分析 不涉及 but missing reason annotation — "
                    "请添加理由注解（如：仓不可达、仓无 DFX 知识、知识库无命中）"
                )
        else:
            draft_warn_archive_fail(
                reporter,
                archive_mode,
                "design.md: DFX 故障模式分析 has no data rows and no 不涉及 — "
                "请填写不涉及并附理由"
            )


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

    # Check required artifacts
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

    # Also check optional (bypass) artifacts when they exist
    for name, data in artifacts.items():
        if data.get("required") != "false":
            continue
        file_name = str(data.get("file", ""))
        if not file_name:
            continue
        path = change_dir / file_name
        if not path.is_file():
            continue  # optional: absence allowed

        text = read_text(path)
        sections = list(data.get("required_sections", []))  # type: ignore[arg-type]
        file_markers: list[str] = []
        for section in sections:
            body = section_text(text, str(section))
            file_markers.extend(unresolved_markers(body))

        if file_markers:
            unresolved = True
            reporter.fail(f"{file_name} (optional): unresolved archive placeholders: " + "; ".join(file_markers[:8]))
        else:
            reporter.pass_(f"{file_name} (optional): no unresolved placeholders in required sections")

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
    parser = ArgumentParser(description="Validate one ODK change directory against the active artifacts contract.")
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

    artifacts = parse_contract_artifacts(str(CONTRACT_PATH))

    mode = "archive" if args.archive else "draft"
    print(f"Validating ODK artifact contract ({mode} mode): {change_dir}")
    print("\nLevel A: Change Directory")
    validate_dir_name(change_dir, reporter)
    validate_target_release(change_dir, reporter)
    files = validate_required_artifacts(change_dir, artifacts, reporter)
    validate_sections(change_dir, artifacts, files, reporter)
    validate_present_optional_sections(change_dir, artifacts, reporter)
    validate_traceability(change_dir, reporter)
    validate_dfx_constraints(change_dir, reporter, args.archive)
    validate_optional_evidence(change_dir, reporter)
    print("\nResource Constraints")
    validate_resource_constraints(change_dir, reporter, archive=args.archive)
    if args.archive:
        validate_archive_readiness(change_dir, artifacts, files, reporter)

    print("\nSummary:")
    print(f"  Passed:   {reporter.passed}")
    print(f"  Warnings: {reporter.warned}")
    print(f"  Failed:   {reporter.failed}")

    return 0 if reporter.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
