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
import bisect
from collections import Counter
import subprocess
import sys
import unicodedata
import json
from argparse import ArgumentParser
from datetime import date, datetime
from pathlib import Path
from typing import Any

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

from odk_yaml import (  # noqa: E402
    parse_api_spec_contract,
    parse_contract_artifacts,
    parse_metadata_tracking,
    parse_resource_contract,
)
from odk_document import (  # noqa: E402
    PLACEHOLDER_RE, BRACKET_PLACEHOLDER_RE, _visible_markdown, atx_heading, headings,
    section_texts, section_texts_with_lines, section_text, require_unique_section,
    normalize_cell, split_table_row,
    is_separator_row, parsed_markdown_tables, markdown_tables, table_has_columns,
    tables_with_columns, table_with_columns, unique_table_with_columns,
    require_unique_table_with_columns, meaningful,
)
from odk_repository import parse_git_remote, metadata_repository_url, metadata_pr_url_matches  # noqa: E402
from odk_diff import unified_diff_sides, valid_unified_diff  # noqa: E402
from odk_contract import compile_contract, DIMENSIONS  # noqa: E402
from odk_involvement import parse_eight_dim_involvement, involvement_errors, involvement_value  # noqa: E402
from odk_plan_environment import environment_errors, SECTION as ENVIRONMENT_SECTION  # noqa: E402
from odk_api_spec import (  # noqa: E402
    arkts_api_mode as _arkts_api_mode,
    arkts_static_metadata_issues,
    api_description_issues,
    api_documentation_duplication_issues,
    api_metadata_schema_version_issue,
    api_spec_structural_issues,
    parse_api_spec,
)
from api_document_style import (  # noqa: E402
    DOCUMENT_STYLE_RULESET_VERSION,
    FORBIDDEN_TERMS_RULESET_VERSION,
    api_documentation_style_issues,
    text_style_issues,
)
# Re-export legacy entry points for callers that load this script as a module.
from odk_api_signature import (  # noqa: E402
    api_signature_complete, canonical_api_signature,
)


# Keep legacy reference extraction for Draft compatibility; validate_ac_ids owns
# definition format severity so a malformed ID cannot disappear from Archive gates.
AC_ID_RE = re.compile(r"AC-(?:[0-9]+|DFX)\.[0-9]+")
AC_DEFINITION_ID_RE = re.compile(r"^[ \t]*[-*][ \t]+\*\*(AC-[^:\n*]*):\*\*", re.MULTILINE)
AC_RE = re.compile(r"\bAC-(?:DFX\.[0-9]+|\d+(?:\.\d+)?)\b")
AC_DEF_RE = re.compile(r"^\s*[-*]\s+\*\*AC-(?:DFX\.[0-9]+|\d+(?:\.\d+)?):\*\*", re.MULTILINE)
TASK_RE = re.compile(r"\bTASK-\d+\b")
ARCHIVE_MARKER_RE = re.compile(
    # Python's Unicode word boundary joins CJK prose to ASCII markers. Protect
    # identifier substrings explicitly while still recognizing 状态TODO.
    r"(?<![A-Za-z0-9_])(?:TBD|TODO)(?![A-Za-z0-9_])"
    r"|(?<![\u4e00-\u9fff])(?:待定|待补充|待实现|待验证)(?![\u4e00-\u9fff])",
    re.IGNORECASE,
)
# Exempt examples immediately following an explicit prohibition. Unquoted
# examples are limited to known archive markers, not arbitrary field values.
# Never skip the whole line/section, which may contain real unfinished work.
PROHIBITED_LITERAL_PATTERN = rf"(?:`[^`\r\n]+`|{ARCHIVE_MARKER_RE.pattern})"
PROHIBITED_LITERAL_LIST_RE = re.compile(
    rf"(?:不得|禁止|请勿)[ \t]*(?:使用|出现)[ \t]*{PROHIBITED_LITERAL_PATTERN}"
    rf"(?:[ \t]*(?:、|，|,|/|或|和|及)[ \t]*{PROHIBITED_LITERAL_PATTERN})*",
    re.IGNORECASE,
)
ANGLE_PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")
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
_DFX_FAULT_COLUMNS = [
    "分析对象", "故障模式", "故障影响", "故障原因",
    "严酷度", "恢复措施", "关键日志", "大数据打点事件", "来源",
]
_DFX_DISPOSITION_COLUMNS = ["编号", "分析对象", "故障模式", "处置", "关联 AC", "验证方式/证据"]
_DFX_DISPOSITIONS = {"新增 AC", "复用 AC", "纳入设计约束", "现有控制覆盖", "本变更不触及"}
_DFX_AC_DISPOSITIONS = {"新增 AC", "复用 AC"}
_DFX_DESIGN_CONSTRAINT_DISPOSITION = "纳入设计约束"
_DFX_CONSTRAINT_REF_RE = re.compile(r"D-\d+|约束|决策|不变量")
_DFX_FM_ID_RE = re.compile(r"^FM-\d+$")
_DFX_AD_ID_RE = re.compile(r"^AD-\d+$")
_PROPOSAL_COVERAGE_SECTION = "Proposal 覆盖矩阵"
_PROPOSAL_COVERAGE_COLUMNS = [
    "Proposal 条目", "类型", "spec 承接位置", "状态",
]
_PROPOSAL_COVERAGE_STATUSES = {"Covered", "N/A", "Open"}
_PROPOSAL_COVERED_REF_RE = re.compile(
    r"\b(?:AC-[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*|BR-\d+|EB-\d+(?:\.\d+)?|"
    r"arkts-api-spec\.yaml|c-api-spec\.yaml)\b"
)
_PROPOSAL_OPEN_REF_RE = re.compile(r"\bOpen-\d+\b")
_PROPOSAL_N_A_REASON_RE = re.compile(r"N/A\s*[:：]\s*(.+)", re.IGNORECASE)

# 66-column library export table header (mirrors the template row in
# core/skills/odk-fmea/references/output-format.md "故障模式库导出表格";
# keep both in sync when the platform import template changes).
_DFX_EXPORT_COLUMNS = [
    "一级对象ID", "一级对象", "一级对象类型", "二级对象ID", "二级对象", "二级对象类型",
    "三级对象ID", "三级对象", "三级对象类型", "四级对象ID", "四级对象", "四级对象类型",
    "五级对象ID", "五级对象", "五级对象类型", "六级对象ID", "六级对象", "六级对象类型",
    "七级对象ID", "七级对象", "七级对象类型", "八级对象ID", "八级对象", "八级对象类型",
    "九级对象ID", "九级对象", "九级对象类型", "十级对象ID", "十级对象", "十级对象类型",
    "故障模式ID", "故障模式", "描述", "严酷度", "发生频度", "可检测度",
    "SIL等级", "故障原因", "故障影响", "改进措施", "典型日志", "引发故障的对象ID",
    "引发故障的对象", "引发故障的行为ID", "引发故障的行为", "受影响的对象ID", "受影响的对象", "所受影响ID",
    "所受影响", "故障检测ID", "故障检测", "事件打点", "故障诊断ID", "故障诊断",
    "故障隔离ID", "故障隔离", "故障恢复ID", "故障恢复", "故障预防ID", "故障预防",
    "使用补偿措施ID", "使用补偿措施", "验证测试要求ID", "验证测试要求", "其他ID", "其他",
]


RESOURCE_CONTRACT = parse_resource_contract(str(CONTRACT_PATH))
API_SPEC_CONTRACT = parse_api_spec_contract(str(CONTRACT_PATH))


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


def api_contract_scalar(key: str) -> str:
    value = API_SPEC_CONTRACT.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{CONTRACT_PATH}: api_spec_contract.{key} must be a scalar")
    return value


def api_contract_list(key: str) -> list[str]:
    value = API_SPEC_CONTRACT.get(key)
    if not isinstance(value, list) or not value:
        raise ValueError(f"{CONTRACT_PATH}: api_spec_contract.{key} must be a non-empty list")
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

API_PROPOSAL_SECTION = api_contract_scalar("proposal_section")
API_TRIGGER_DIMENSION = api_contract_scalar("trigger_dimension")
API_SPEC_SECTION = api_contract_scalar("spec_section")
API_OVERVIEW_SECTION = api_contract_scalar("overview_section")
API_METADATA_SCHEMA_VERSION = api_contract_scalar("metadata_schema_version")
API_CONTRACT_VERSION = api_contract_scalar("api_contract_version")
API_METADATA_LANGUAGES = set(api_contract_list("metadata_languages"))
API_METADATA_BY_LANGUAGE = {
    "arkts": "arkts-api-spec.yaml",
    "c": "c-api-spec.yaml",
}
API_METADATA_FILES = set(api_contract_list("metadata_files"))
if set(API_METADATA_BY_LANGUAGE.values()) != API_METADATA_FILES:
    raise ValueError(
        f"{CONTRACT_PATH}: api_spec_contract.metadata_files must be "
        + ", ".join(sorted(API_METADATA_BY_LANGUAGE.values()))
    )
if set(API_METADATA_BY_LANGUAGE) != API_METADATA_LANGUAGES:
    raise ValueError(
        f"{CONTRACT_PATH}: api_spec_contract metadata files and languages must match"
    )
API_LEGACY_METADATA_FILE = "api-spec.yaml"
API_SPEC_SUMMARY_ONLY = api_contract_scalar("spec_summary_only") == "true"
DEVICE_VARIATION_SECTION = "1+8 设备差异规格"
DEVICE_VARIATION_COLUMNS = ["设备/差异项", "是否存在差异", "差异说明"]
DEVICE_VARIATION_ROWS = (
    "phone",
    "tablet",
    "pc/2in1",
    "wearable",
    "tv",
    "car",
    "default（其他设备）",
    "功能差异（非品类划分）",
)
EXTERNAL_DEPENDENCIES_SECTION = "外部依赖"
EXTERNAL_DEPENDENCIES_COLUMNS = ["子系统", "仓库", "模块/路径", "依赖类型"]

I18N_TRIGGER_DIMENSION = "国际化"
I18N_SECTION = "国际化依赖分析"
I18N_TABLE_COLUMNS = ["调用场景", "i18n API 类型", "依赖类型", "仓路径", "接口/方法", "备注"]
I18N_DEPENDENCY_TYPES = {"仓内封装", "外部依赖"}
I18N_SUMMARY_RE = re.compile(
    r"^\s*\|\s*合计\s*\|\s*\d+\s*个调用点\s*\|\s*仓内[:：]\s*\d+\s*/\s*外部[:：]\s*\d+\s*\|",
    re.IGNORECASE,
)

PROPOSAL_ID_RE = re.compile(r"^[0-9]+$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DRAFT_RE = re.compile(r"^draft-\d{8}-(.+)$")
REPOSITORY_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")
# Session ID formats accepted across host platforms:
#   opencode: ses_<alphanumeric>            e.g. ses_abc123
#   codex:    <uuid>                        e.g. 11111111-2222-3333-4444-555555555555
#   claude:   <uuid>                        e.g. aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
_SESSION_UUID = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
SESSION_ID_RE = re.compile(
    r"^(?:ses_[a-zA-Z0-9_-]+|" + _SESSION_UUID + r")$"
)
MAX_SLUG_LENGTH = 40
INVALID_PROPOSAL_ID_SCALAR = "__invalid_proposal_id_scalar__"
ASCII_YAML_WHITESPACE = " \t\r\n"


class Frontmatter(dict[str, str]):
    """Parsed user fields plus out-of-band parser validity state."""

    def __init__(self, invalid_reason: str | None = None) -> None:
        super().__init__()
        self.invalid_reason = invalid_reason


def trim_yaml_whitespace(value: str) -> str:
    """Trim ASCII/YAML separation whitespace, never Unicode lookalikes."""
    return value.strip(ASCII_YAML_WHITESPACE)


class Reporter:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.warned = 0
        self.messages: list[str] = []

    def pass_(self, message: str) -> None:
        print(f"  PASS {message}")
        self.messages.append(f"PASS {message}")
        self.passed += 1

    def fail(self, message: str) -> None:
        print(f"  FAIL {message}")
        self.messages.append(f"FAIL {message}")
        self.failed += 1

    def fail_once(self, message: str) -> None:
        """Several gates may depend on the same invalid document section."""
        if f"FAIL {message}" not in self.messages:
            self.fail(message)

    def warn(self, message: str) -> None:
        print(f"  WARN {message}")
        self.messages.append(f"WARN {message}")
        self.warned += 1


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_simple_yaml_scalar(raw: str) -> str | None:
    """Parse the simple scalar forms accepted in ODK frontmatter."""
    value = trim_yaml_whitespace(raw)
    if not value or value[0] not in {'"', "'"}:
        if value.startswith("#"):
            return ""
        return trim_yaml_whitespace(re.sub(r"[ \t\r\n]+#.*$", "", value))

    quote = value[0]
    closing = value.find(quote, 1)
    if closing == -1:
        return None
    suffix = trim_yaml_whitespace(value[closing + 1 :])
    if suffix and not suffix.startswith("#"):
        return None
    return trim_yaml_whitespace(value[1:closing])


def read_frontmatter(
    path: Path, *, single_line_keys: tuple[str, ...] = ()
) -> Frontmatter:
    """Read simple YAML pairs; verdicts also reject ambiguous top-level fields."""
    if not path.is_file():
        return Frontmatter()
    # Split only on LF. str.splitlines() also treats VT, FF, NEL and Unicode
    # separators as line boundaries, which would silently normalize invalid
    # frontmatter differently from the shell validator.
    lines = read_text(path).split("\n")
    if not lines or trim_yaml_whitespace(lines[0]) != "---":
        return Frontmatter("invalid opening delimiter")
    result = Frontmatter()
    closed = False
    current_key = ""
    for line in lines[1:]:
        stripped = trim_yaml_whitespace(line)
        if (current_key in single_line_keys and line.startswith((" ", "\t"))
                and stripped and not stripped.startswith("#")):
            # Plain YAML scalars fold indented continuation lines into their
            # value. Taking only the first line could turn PASS FAIL into PASS.
            return Frontmatter(f"{current_key} must be a single-line scalar")
        if stripped == "---":
            closed = True
            break
        if "\x00" in line:
            return Frontmatter("frontmatter contains NUL")
        if re.match(r'''^[ \t]*(?:req|req_id|"req"|"req_id"|'req'|'req_id')[ \t]*:''', line):
            return Frontmatter("legacy identity field; migrate to proposal_id")
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)[ \t\r]*:[ \t\r]*(.*)$", line)
        if match:
            key = match.group(1)
            current_key = key
            if single_line_keys and key in result:
                return Frontmatter(f"duplicate frontmatter field: {key}")
            if key == "proposal_id" and key in result:
                result[key] = INVALID_PROPOSAL_ID_SCALAR
                continue
            raw = match.group(2)
            value = parse_simple_yaml_scalar(raw)
            result[key] = value if value is not None else trim_yaml_whitespace(raw)
        elif stripped and not stripped.startswith("#"):
            if single_line_keys:
                if not line.startswith((" ", "\t")) or not current_key:
                    return Frontmatter("unsupported top-level frontmatter syntax")
                # Only an existing extra metadata field can own nested content.
                # Keep its context across all children, comments and blank lines.
            else:
                current_key = ""
    return result if closed else Frontmatter("missing closing delimiter")


def normalized_table_key(value: str) -> str:
    return value.replace("*", "").replace("`", "").strip()


def api_sdk_involvement(proposal: str) -> str | None:
    sections = section_texts(proposal, API_PROPOSAL_SECTION)
    if len(sections) != 1:
        return None
    tables = tables_with_columns(sections[0], ["维度", "是否涉及"])
    if len(tables) != 1:
        return None
    matches = [
        row
        for row in tables[0]
        if normalized_table_key(row.get("维度", "")) == API_TRIGGER_DIMENSION
    ]
    if len(matches) != 1:
        return None
    value = normalized_table_key(matches[0].get("是否涉及", ""))
    return involvement_value(value) or value or None


def arkts_static_api_involvement(proposal: str) -> str | None:
    sections = section_texts(proposal, "API 设计属性")
    if len(sections) != 1:
        return None
    tables = tables_with_columns(sections[0], ["属性", "值", "说明"])
    if len(tables) != 1:
        return None
    matches = [
        row
        for row in tables[0]
        if normalized_table_key(row.get("属性", "")) == "ArkTS 静态类型 API"
    ]
    if len(matches) != 1:
        return None
    return normalized_table_key(matches[0].get("值", "")) or None


def api_heading_signature(line: str) -> str | None:
    """Return an opaque signature, including empty; None means no API heading."""
    heading = atx_heading(line)
    if heading is None or heading[0] != 4 or not heading[1].startswith("API:"):
        return None
    return heading[1][len("API:"):].strip()


def api_entry_blocks(per_api_text: str) -> list[tuple[str, str]]:
    """Compatibility helper for historical Markdown API heading regressions."""
    lines = per_api_text.splitlines()
    matches = [
        (index, signature)
        for index, line in enumerate(lines)
        if (signature := api_heading_signature(line)) is not None
    ]
    entries: list[tuple[str, str]] = []
    for index, (start, signature) in enumerate(matches):
        end = matches[index + 1][0] if index + 1 < len(matches) else len(lines)
        entries.append((signature, "\n".join(lines[start + 1:end])))
    return entries


def validate_proposal_coverage_matrix(change_dir: Path, reporter: Reporter) -> None:
    """Validate the structural closure contract for proposal-to-spec coverage.

    This gate intentionally does not claim to understand proposal semantics. It
    only verifies that every matrix row uses a concrete status and that Covered
    rows point at a machine-checkable artifact/trace target. Semantic review is
    owned by odk-spec and the reviewer.
    """

    proposal_path = change_dir / "proposal.md"
    spec_path = change_dir / "spec.md"
    if not proposal_path.is_file() or not spec_path.is_file():
        return

    spec = _visible_markdown(read_text(spec_path))
    sections = section_texts(spec, _PROPOSAL_COVERAGE_SECTION)
    if len(sections) != 1:
        reporter.fail(
            f"spec.md: {_PROPOSAL_COVERAGE_SECTION} section must appear exactly once"
        )
        return

    tables = tables_with_columns(sections[0], _PROPOSAL_COVERAGE_COLUMNS)
    if len(tables) != 1:
        reporter.fail(
            f"spec.md: {_PROPOSAL_COVERAGE_SECTION} must contain exactly one table"
        )
        return

    rows = tables[0]
    if not rows:
        reporter.fail(
            f"spec.md: {_PROPOSAL_COVERAGE_SECTION} must contain at least one row"
        )
        return

    issues: list[str] = []
    for index, row in enumerate(rows, start=1):
        item = row.get("Proposal 条目", "")
        item_type = row.get("类型", "")
        mapping = row.get("spec 承接位置", "")
        status = row.get("状态", "").strip()
        label = item.strip() or f"row {index}"

        for field, value in (
            ("Proposal 条目", item),
            ("类型", item_type),
            ("spec 承接位置", mapping),
        ):
            if not meaningful(value):
                issues.append(f"matrix row {index} ({label}) requires {field}")
            elif ANGLE_PLACEHOLDER_RE.search(value) or BRACKET_PLACEHOLDER_RE.search(value):
                issues.append(
                    f"matrix row {index} ({label}) has unresolved placeholder in {field}"
                )

        if status not in _PROPOSAL_COVERAGE_STATUSES:
            issues.append(
                f"matrix row {index} ({label}) status must be one of: "
                + ", ".join(sorted(_PROPOSAL_COVERAGE_STATUSES))
            )
            continue

        if status == "Covered" and not _PROPOSAL_COVERED_REF_RE.search(mapping):
            issues.append(
                f"matrix row {index} ({label}) Covered mapping must reference "
                "AC/BR/EB or a language-specific API metadata file"
            )
        elif status == "N/A":
            reason = _PROPOSAL_N_A_REASON_RE.search(mapping)
            if reason is None or not meaningful(reason.group(1)):
                issues.append(
                    f"matrix row {index} ({label}) N/A mapping must be "
                    "'N/A: <concrete reason>'"
                )
        elif status == "Open" and not _PROPOSAL_OPEN_REF_RE.search(mapping):
            issues.append(
                f"matrix row {index} ({label}) Open mapping must reference Open-N"
            )

    if issues:
        reporter.fail("spec.md Proposal coverage matrix invalid: " + "; ".join(issues))
    else:
        reporter.pass_("spec.md Proposal coverage matrix has complete structural closure")


def arkts_static_proposal_issues(proposal: str, metadata: dict) -> list[str]:
    """Close the proposal static declaration into language-specific metadata."""

    declared = arkts_static_api_involvement(proposal)
    if declared not in {"是", "否"}:
        return [
            "proposal.md API 设计属性: ArkTS 静态类型 API must state 是 or 否 "
            "when arkts-api-spec.yaml exists"
        ]

    apis = metadata.get("apis")
    if not isinstance(apis, list):
        return []
    modes = [
        _arkts_api_mode(api)
        for api in apis
        if isinstance(api, dict)
    ]
    if declared == "是" and not any(mode in {"static", "dynamic&static"} for mode in modes):
        return [
            "proposal.md ArkTS 静态类型 API=是 but arkts-api-spec.yaml contains "
            "no static or dynamic&static API"
        ]
    if declared == "否" and any(mode in {"static", "dynamic&static"} for mode in modes):
        return [
            "proposal.md ArkTS 静态类型 API=否 but arkts-api-spec.yaml contains "
            "static or dynamic&static API"
        ]
    return []


def validate_api_spec_contract(
    change_dir: Path, reporter: Reporter, *, archive: bool
) -> None:
    proposal_path = change_dir / "proposal.md"
    spec_path = change_dir / "spec.md"
    if not proposal_path.is_file() or not spec_path.is_file():
        return

    involvement = api_sdk_involvement(_visible_markdown(read_text(proposal_path)))
    if involvement not in {"是", "否"}:
        reporter.fail(
            f"proposal.md: {API_TRIGGER_DIMENSION} must state 是 or 否 in {API_PROPOSAL_SECTION}"
        )
        return

    spec_sections = section_texts(_visible_markdown(read_text(spec_path)), API_SPEC_SECTION)
    if len(spec_sections) != 1:
        reporter.fail(f"spec.md: {API_SPEC_SECTION} section must appear exactly once")
        return
    spec_section = spec_sections[0]
    visible_spec_section = _visible_markdown(spec_section)
    reporter.pass_(
        "API documentation ruleset: document-style@"
        + DOCUMENT_STYLE_RULESET_VERSION
        + " forbidden-terms@"
        + FORBIDDEN_TERMS_RULESET_VERSION
    )

    existing_metadata_files = sorted(
        name
        for name in [*API_METADATA_FILES, API_LEGACY_METADATA_FILE]
        if (change_dir / name).exists()
    )

    if involvement == "否":
        if existing_metadata_files:
            reporter.fail(
                "API metadata files must not exist when proposal.md API/SDK=否: "
                + ", ".join(existing_metadata_files)
            )
        visible = "\n".join(
            line
            for line in visible_spec_section.splitlines()
            if not line.lstrip().startswith(">")
        )
        reason = re.search(r"不涉及(?:\s*[：:]\s*|\s+)(\S[^\n]*)", visible)
        unresolved = (
            reason
            and (
                ANGLE_PLACEHOLDER_RE.search(reason.group(1))
                or re.search(
                    r"\b(?:TBD|TODO)\b|待确认|待定|待补充|待实现|待验证",
                    reason.group(1),
                    flags=re.IGNORECASE,
                )
            )
        )
        if reason and meaningful(reason.group(1)) and not unresolved:
            reporter.pass_("spec.md API/SDK=否 has an explicit not-applicable reason")
        else:
            reporter.fail("spec.md API/SDK=否 requires an explicit not-applicable reason")
        return

    if API_LEGACY_METADATA_FILE in existing_metadata_files:
        reporter.fail(
            f"{API_LEGACY_METADATA_FILE} is no longer accepted; split it into "
            "arkts-api-spec.yaml and/or c-api-spec.yaml"
        )
        existing_metadata_files.remove(API_LEGACY_METADATA_FILE)
    contract_version_pattern = re.compile(
        r"\|\s*API 契约版本\s*\|\s*"
        + re.escape(API_CONTRACT_VERSION)
        + r"\s*\|"
    )
    if not contract_version_pattern.search(visible_spec_section):
        reporter.fail(
            f"spec.md API 契约版本 must be {API_CONTRACT_VERSION}"
        )

    if not existing_metadata_files:
        draft_warn_archive_fail(
            reporter,
            archive,
            "At least one language-specific API metadata file is required when "
            "proposal.md API/SDK=是: arkts-api-spec.yaml or c-api-spec.yaml",
        )
        return

    metadata_by_file: dict[str, dict] = {}
    issues: list[str] = []
    for file_name in existing_metadata_files:
        path = change_dir / file_name
        try:
            metadata = parse_api_spec(path)
        except (OSError, UnicodeError, ValueError) as error:
            issues.append(f"{file_name}: cannot parse API metadata: {error}")
            continue
        metadata_by_file[file_name] = metadata

        expected_language = next(
            language
            for language, name in API_METADATA_BY_LANGUAGE.items()
            if name == file_name
        )
        if metadata.get("language") != expected_language:
            issues.append(
                f"{file_name}: language must be {expected_language}"
            )
        schema_issue = api_metadata_schema_version_issue(
            metadata.get("schemaVersion")
        )
        if schema_issue:
            issues.append(f"{file_name}: {schema_issue.removeprefix('API metadata: ')}")
        if metadata.get("apiContractVersion") != API_CONTRACT_VERSION:
            issues.append(
                f"{file_name}: apiContractVersion must be {API_CONTRACT_VERSION}"
            )
        if expected_language == "arkts" and not isinstance(metadata.get("file"), dict):
            issues.append(f"{file_name}: ArkTS metadata must use the file block")
        if expected_language == "c" and not isinstance(metadata.get("header"), dict):
            issues.append(f"{file_name}: C metadata must use the header block")
        issues.extend(api_spec_structural_issues(metadata))
        issues.extend(api_description_issues(metadata))
        apis = metadata.get("apis")
        if not isinstance(apis, list):
            apis = []
        if expected_language == "arkts":
            issues.extend(arkts_static_proposal_issues(read_text(proposal_path), metadata))
            issues.extend(arkts_static_metadata_issues(metadata))
        for api_index, api in enumerate(apis, start=1):
            if not isinstance(api, dict):
                continue
            label = api.get("id") or api.get("name") or f"API[{api_index}]"
            issues.extend(
                api_documentation_style_issues(api, f"{file_name}: API '{label}'")
            )
        if file_name not in visible_spec_section:
            issues.append(f"spec.md API overview must reference {file_name}")

    all_api_ids: list[str] = []
    for file_name, metadata in metadata_by_file.items():
        apis = metadata.get("apis")
        if not isinstance(apis, list):
            continue
        all_api_ids.extend(
            str(api.get("id", ""))
            for api in apis
            if isinstance(api, dict) and meaningful(str(api.get("id", "")))
        )
    duplicate_ids = sorted(
        value for value, count in Counter(all_api_ids).items() if count > 1
    )
    if duplicate_ids:
        issues.append(
            "API metadata files contain duplicate API IDs: " + ", ".join(duplicate_ids)
        )

    overview_sections = section_texts(visible_spec_section, API_OVERVIEW_SECTION)
    if len(overview_sections) != 1:
        issues.append(
            f"spec.md: {API_OVERVIEW_SECTION} subsection must appear exactly once"
        )
        overview_ids: set[str] = set()
    else:
        overview_tables = tables_with_columns(
            overview_sections[0], ["API ID", "类型", "完整签名", "@since", "确认状态"]
        )
        if len(overview_tables) != 1:
            issues.append(
                f"spec.md: {API_OVERVIEW_SECTION} must contain exactly one overview table"
            )
            overview_ids = set()
        else:
            overview_ids = {
                normalized_table_key(row.get("API ID", ""))
                for row in overview_tables[0]
                if meaningful(row.get("API ID", ""))
            }
            metadata_ids = {
                normalized_table_key(value) for value in all_api_ids
            }
            missing = sorted(metadata_ids - overview_ids)
            extra = sorted(overview_ids - metadata_ids)
            if missing:
                issues.append(
                    "spec.md API overview missing API IDs from API metadata files: "
                    + ", ".join(missing)
                )
            if extra:
                issues.append(
                    "spec.md API overview contains API IDs absent from API metadata files: "
                    + ", ".join(extra)
                )

    fact_sections = section_texts(
        visible_spec_section, "API 事实溯源与待确认项"
    )
    if len(fact_sections) != 1:
        issues.append(
            "spec.md: API 事实溯源与待确认项 subsection must appear exactly once"
        )
    else:
        fact_tables = tables_with_columns(
            fact_sections[0], ["API 事实", "结果", "来源", "状态"]
        )
        if len(fact_tables) != 1:
            issues.append(
                "spec.md: API 事实溯源与待确认项 must contain exactly one table"
            )
        else:
            required_facts = {
                "@since", "@syscap", "权限", "跨平台 / 元服务 / 卡片支持",
                "FA / Stage 模型", "设备支持与行为差异",
            }
            fact_rows = {
                normalized_table_key(row.get("API 事实", ""))
                for row in fact_tables[0]
                if meaningful(row.get("API 事实", ""))
            }
            missing_facts = sorted(required_facts - fact_rows)
            if missing_facts:
                issues.append(
                    "spec.md API fact provenance missing facts: "
                    + ", ".join(missing_facts)
                )
            for row in fact_tables[0]:
                fact = row.get("API 事实", "")
                result = row.get("结果", "")
                source = row.get("来源", "")
                status = row.get("状态", "")
                if not meaningful(fact):
                    continue
                if status not in {"已确认", "待确认"}:
                    issues.append(
                        f"spec.md API fact '{fact}' status must be 已确认 or 待确认"
                    )
                if not meaningful(source) or ANGLE_PLACEHOLDER_RE.search(source) or BRACKET_PLACEHOLDER_RE.search(source):
                    issues.append(
                        f"spec.md API fact '{fact}' requires a meaningful evidence source"
                    )
                if status == "已确认" and (
                    not meaningful(result)
                    or ANGLE_PLACEHOLDER_RE.search(result)
                    or BRACKET_PLACEHOLDER_RE.search(result)
                    or re.search(r"\b(?:TBD|TODO)\b|待确认|待定|待补充", result, flags=re.IGNORECASE)
                ):
                    issues.append(
                        f"spec.md API fact '{fact}' is marked confirmed but has no resolved result"
                    )

    if API_SPEC_SUMMARY_ONLY:
        if re.search(r"^####\s+API:", visible_spec_section, flags=re.MULTILINE):
            issues.append(
                "spec.md API overview must not contain legacy per-API #### API subsections"
            )
        for legacy in ("公共规格属性", "逐 API 规格"):
            if section_texts(visible_spec_section, legacy):
                issues.append(
                    f"spec.md API overview must not contain legacy subsection: {legacy}"
                )

    duplication_issues: list[str] = []
    for file_name, metadata in metadata_by_file.items():
        duplication_issues.extend(
            f"{file_name}: {issue}"
            for issue in api_documentation_duplication_issues(metadata)
        )
    for issue in duplication_issues:
        draft_warn_archive_fail(
            reporter,
            archive,
            "API documentation duplication heuristic: " + issue,
        )

    if issues:
        for issue in issues:
            reporter.fail(issue)
    elif not duplication_issues:
        reporter.pass_(
            "language-specific API metadata files and spec.md overview are consistent"
        )


def _normalized_path(value: str) -> str:
    return value.replace("\\", "/").strip().strip("/")


def _diff_path_matches(diff_path: str, metadata_path: str) -> bool:
    """Require exact normalized path equivalence, not arbitrary suffix overlap."""

    return _normalized_path(diff_path) == _normalized_path(metadata_path)


def _compact_text(value: str) -> str:
    return re.sub(r"\s+", "", value)


def _declaration_windows(lines: list[str], declaration: str) -> list[tuple[int, int]]:
    """Find every smallest contiguous line window containing the declaration."""

    compact_declaration = _compact_text(declaration).strip(";")
    if not compact_declaration:
        return []
    compact_lines = [_compact_text(line).strip(";") for line in lines]
    # Length-directed matching avoids the historical width/start/join triple
    # loop. A candidate end is possible only when the compact lengths add up to
    # the declaration length; blank lines can create several such ends, so all
    # equal-length candidates are checked and the smallest line width wins.
    prefix_lengths = [0]
    for compact_line in compact_lines:
        prefix_lengths.append(prefix_lengths[-1] + len(compact_line))
    target_length = len(compact_declaration)
    windows: list[tuple[int, int]] = []
    for start in range(len(lines)):
        end = bisect.bisect_left(
            prefix_lengths, prefix_lengths[start] + target_length, lo=start + 1
        )
        while end <= len(lines) and prefix_lengths[end] == prefix_lengths[start] + target_length:
            if "".join(compact_lines[start:end]) == compact_declaration:
                windows.append((start, end - 1))
            end += 1
    if not windows:
        return []
    minimum_width = min(end - start + 1 for start, end in windows)
    return [
        window for window in windows
        if window[1] - window[0] + 1 == minimum_width
    ]


def _declaration_window(lines: list[str], declaration: str) -> tuple[int, int] | None:
    """Compatibility helper for callers that only need the first candidate."""

    windows = _declaration_windows(lines, declaration)
    return windows[0] if windows else None


def _is_single_line_doc_comment(line: str) -> bool:
    text = line.strip()
    return (
        len(text) > 4
        and (text.startswith("/**") or text.startswith("/*!"))
        and text.endswith("*/")
    )


def _declaration_comment_bounds(
    lines: list[str], declaration_start: int, declaration_end: int
) -> tuple[int, int] | None:
    """Return the doc-comment block immediately preceding a declaration."""

    if declaration_start <= 0:
        return None
    close = None
    for index in range(declaration_start - 1, max(0, declaration_start - 40) - 1, -1):
        if lines[index].strip():
            if _is_single_line_doc_comment(lines[index]):
                return index, declaration_end
            close = index if lines[index].strip() == "*/" else None
            break
    if close is None:
        return None

    # Stay inside the comment that ends at `close`. A plain comment, code, or
    # another comment terminator proves that the preceding block is not the
    # declaration's documentation context.
    for index in range(close, max(0, close - 200) - 1, -1):
        line = lines[index].strip()
        if index == close:
            if (line.startswith("/**") or line.startswith("/*!")) and line.endswith("*/"):
                return index, declaration_end
            continue
        if line.startswith("/**") or line.startswith("/*!"):
            return index, declaration_end
        if "*/" in line or not line.startswith("*"):
            return None
    return None


def _declaration_comment_context(lines: list[str], declaration_index: int) -> str | None:
    """Return the doc block immediately preceding a declaration."""

    bounds = _declaration_comment_bounds(lines, declaration_index, declaration_index)
    if bounds is None:
        return None
    # The context is the documentation comment itself; declarations are
    # validated separately and must not become tag continuation prose.
    return "\n".join(
        _clean_comment_line(line) for line in lines[bounds[0]:declaration_index]
    )


def _diff_segment_windows(
    segments: object, declaration: str
) -> list[tuple[dict[str, object], int, int]]:
    """Find declaration windows only within continuous diff segments."""

    if segments is None:
        return []
    candidates: list[tuple[dict[str, object], int, int]] = []
    for segment in segments:  # type: ignore[union-attr]
        lines = segment["lines"]  # type: ignore[index]
        for start, end in _declaration_windows(lines, declaration):  # type: ignore[arg-type]
            candidates.append((segment, start, end))
    return candidates


def _segment_window_changed(
    segment: dict[str, object], window: tuple[int, int]
) -> bool:
    """Return whether a declaration or its immediate doc block changed."""

    lines = segment["lines"]  # type: ignore[index]
    changed: set[int] = segment["changed"]  # type: ignore[index]
    start, end = window
    if any(position in range(start, end + 1) for position in changed):
        return True
    bounds = _declaration_comment_bounds(lines, start, end)  # type: ignore[arg-type]
    if bounds is None:
        return False
    return any(
        position in range(bounds[0], bounds[1] + 1) for position in changed
    )


def _context_owns_identity(context: str | None, value: object) -> bool:
    """Require an explicit owner marker rather than any identity substring."""

    if context is None or value is None:
        return False
    identity = str(value)
    if not identity.strip():
        return False
    pattern = (
        r"(?:API\s*ID|qualifiedName)\s*[:：]\s*"
        + re.escape(identity.strip())
        + r"\s*[.。;；]?\s*"
    )
    for line in context.splitlines():
        if re.fullmatch(pattern, line.strip(), flags=re.IGNORECASE):
            return True
    return False


def _candidate_identity_matches(api: dict, candidate: tuple[object, ...]) -> bool:
    """Bind one declaration window to an explicit API identity or source line."""

    segment = candidate[0]
    start = int(candidate[1])
    context = candidate[3] if len(candidate) > 3 else None
    if any(_context_owns_identity(context, value) for value in (api.get("id"), api.get("qualifiedName"))):
        return True
    try:
        source_line = int(segment.get("start", 0)) + start  # type: ignore[union-attr]
        start_line = int(api.get("startLine"))
        end_line = int(api.get("endLine"))
        return start_line <= source_line <= end_line
    except (TypeError, ValueError):
        return False


def _target_api_changed(api: dict, sides: dict[str, object]) -> bool:
    """Prove the target declaration or its associated doc comment changed."""

    candidates = _target_api_candidates(api, sides)
    for segment, start, end, _context in candidates:
        if _segment_window_changed(segment, (start, end)):  # type: ignore[arg-type]
            return True
    declaration = str(api.get("declaration") or "")
    for segment, start, end, _context in _diff_segment_windows(
        sides.get("oldSegments"), declaration  # type: ignore[arg-type]
    ):
        if _segment_window_changed(segment, (start, end)):  # type: ignore[arg-type]
            return True
    return False


def _selected_target_candidate_changed(
    api: dict,
    sides: dict[str, object],
    selected: tuple[dict[str, object], int, int, str | None],
    *,
    duplicate_signature: bool,
) -> bool:
    """Check only the selected new-side window and its bound old-side evidence."""

    segment, start, end, _context = selected
    if _segment_window_changed(segment, (start, end)):  # type: ignore[arg-type]
        return True

    declaration = str(api.get("declaration") or "")
    old_candidates = _diff_segment_windows(
        sides.get("oldSegments"), declaration  # type: ignore[arg-type]
    )
    if not duplicate_signature:
        return any(
            _segment_window_changed(old_segment, (old_start, old_end))
            for old_segment, old_start, old_end in old_candidates
        )

    for old_segment, old_start, old_end, old_context in [
        (
            old_segment,
            old_start,
            old_end,
            _declaration_comment_context(
                old_segment["lines"], old_start  # type: ignore[index, arg-type]
            ),
        )
        for old_segment, old_start, old_end in old_candidates
    ]:
        if any(
            _context_owns_identity(old_context, value)
            for value in (api.get("id"), api.get("qualifiedName"))
        ) and _segment_window_changed(
            old_segment, (old_start, old_end)  # type: ignore[arg-type]
        ):
            return True
    return False


def _target_api_candidates(
    api: dict, sides: dict[str, object]
) -> list[tuple[dict[str, object], int, int, str | None]]:
    """Return new-side declaration candidates with their doc context."""

    declaration = str(api.get("declaration") or "")
    candidates: list[tuple[dict[str, object], int, int, str | None]] = []
    for segment, start, end in _diff_segment_windows(
        sides.get("newSegments"), declaration
    ):
        lines = segment["lines"]  # type: ignore[index]
        context = _declaration_comment_context(lines, start)  # type: ignore[arg-type]
        candidates.append((segment, start, end, context))
    return candidates


def _selected_target_candidates(
    api: dict, candidates: list[tuple[dict[str, object], int, int, str | None]]
) -> list[tuple[dict[str, object], int, int, str | None]]:
    """Select candidates explicitly owned by the target API."""

    return [
        candidate for candidate in candidates
        if _candidate_identity_matches(api, candidate)
    ]


def _api_permission_values(api: dict) -> list[str]:
    permissions = api.get("permissions")
    if not isinstance(permissions, list):
        return []
    values: list[str] = []
    for permission in permissions:
        if isinstance(permission, str):
            values.append(permission)
        elif isinstance(permission, dict):
            value = permission.get("name") or permission.get("permission") or permission.get("value")
            if value is not None:
                values.append(str(value))
    return [value for value in values if value.strip()]


def _marker_values(context: str, marker: str) -> list[str]:
    """Extract every scalar following the named marker."""

    return [
        match.group(1).strip()
        for match in re.finditer(
            rf"@{re.escape(marker)}\s+([^\n@]+)",
            context,
            flags=re.IGNORECASE,
        )
        if match.group(1).strip()
    ]


def _marker_present(context: str, marker: str, value: str | None = None) -> bool:
    if value is None:
        return re.search(
            rf"@{re.escape(marker)}\b", context, flags=re.IGNORECASE
        ) is not None
    return str(value).strip() in _marker_values(context, marker)


def _since_marker_present(context: str, since: object) -> bool:
    value = str(since or "").strip()
    if not value:
        return False
    if value in _marker_values(context, "since"):
        return True
    escaped = re.escape(value)
    return re.search(
        rf"\[since\s+{escaped}\]", context, flags=re.IGNORECASE
    ) is not None


def _semantic_compact_text(value: Any) -> str:
    """Normalize documentation text for punctuation-agnostic exact coverage.

    Word order and inserted/missing words still matter. Markdown emphasis,
    whitespace, and punctuation differences do not. This is a loss gate, not a
    claim of full natural-language semantic understanding.
    """

    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    return " ".join(re.findall(r"\w+", text, flags=re.UNICODE))


_DECLARATION_DESCRIPTION_LABEL_RE = re.compile(
    r"^(function|scenario|effect|similar\s*APIs|default\s*behavior|"
    r"constraints|activation|notes|功能|含义|使用场景|使用效果|相似\s*API|"
    r"默认行为|约束|生效条件|注意事项)\s*[:：]",
    re.IGNORECASE,
)


def _description_is_not_applicable(value: Any) -> bool:
    text = str(value or "").strip().casefold().rstrip(".。")
    return text in {"n/a", "不适用"}


def _description_covers(context: str, value: Any) -> bool:
    expected = _semantic_compact_text(value)
    if not expected:
        return True
    actual = _semantic_compact_text(context)
    if re.search(r"[\u3400-\u9fff\uf900-\ufaff]", expected):
        # CJK prose has no whitespace word boundaries. A normalized substring
        # check preserves word order while allowing natural Chinese sentences
        # to embed the confirmed metadata phrase.
        return expected in actual
    return re.search(
        rf"(?<!\S){re.escape(expected)}(?!\S)", actual
    ) is not None


def _clean_comment_line(line: str) -> str:
    text = line.strip()
    if _is_single_line_doc_comment(text):
        return text[3:-2].strip()
    if text in {"/**", "/*!", "*/"}:
        return ""
    if text.startswith("*"):
        text = text[1:].strip()
    return text


def _tag_block(
    context: str, tag_name: str, parameter_name: str | None = None
) -> str | None:
    """Return one doc tag and its continuation lines, without other tags."""

    tag_re = re.compile(
        rf"@{re.escape(tag_name)}(?:\[[^\]]*\])?(?:\s|$)", re.IGNORECASE
    )
    param_re = re.compile(
        r"@param(?:\[[^\]]*\])?\s+"
        r"(?:\{[^}]*\}\s*)?(?:\[([^\]]+)\]|([A-Za-z_$][\w$]*))(?=\s|$|[^\w$\]])",
        re.IGNORECASE,
    )
    lines = [_clean_comment_line(line) for line in context.splitlines()]
    for index, line in enumerate(lines):
        tag_match = tag_re.search(line)
        if tag_match is None:
            continue
        tag_line = line[tag_match.start():]
        if parameter_name is not None:
            match = param_re.match(tag_line)
            actual_name = None
            if match:
                actual_name = match.group(1) or match.group(2)
            if actual_name != parameter_name:
                continue
        next_tag = re.search(r"\s+(?=@[A-Za-z])", tag_line)
        tag_text = tag_line[: next_tag.start()] if next_tag else tag_line
        block = [tag_text]
        for continuation in lines[index + 1 :]:
            if not continuation or continuation == "*/":
                break
            if continuation.startswith("@"):
                break
            block.append(continuation)
        return "\n".join(block)
    return None


def _localized_description(value: Any, language: str) -> Any:
    if not isinstance(value, dict):
        return None
    return value.get(language)


def _api_description_closure_issues(
    api: dict, context: str, language: str
) -> list[str]:
    """Require every meaningful metadata description to survive into the doc block."""

    label = api.get("id") or api.get("name") or "unnamed"
    issues: list[str] = []

    labels: set[str] = set()
    for raw_line in context.splitlines():
        line = _clean_comment_line(raw_line)
        match = _DECLARATION_DESCRIPTION_LABEL_RE.match(line)
        if match:
            labels.add(match.group(1))
    for element_label in sorted(labels):
        issues.append(
            f"API declaration description label '{element_label}' is not allowed: {label}"
        )

    description = api.get("description")
    values = description.get(language) if isinstance(description, dict) else None
    if isinstance(values, dict):
        for element in (
            "function", "scenario", "effect", "similarAPIs",
            "defaultBehavior", "constraints", "activation", "notes",
        ):
            expected = values.get(element)
            if expected is None or _description_is_not_applicable(expected):
                continue
            if not _description_covers(context, expected):
                issues.append(
                    f"API declaration description.{language}.{element} "
                    f"missing or mismatched: {label}"
                )

    parameters = api.get("parameters")
    if isinstance(parameters, list):
        for index, parameter in enumerate(parameters, start=1):
            if not isinstance(parameter, dict):
                continue
            name = str(parameter.get("name") or "").strip() or f"parameter[{index}]"
            expected = _localized_description(parameter.get("description"), language)
            if expected is None or _description_is_not_applicable(expected):
                continue
            block = _tag_block(context, "param", name)
            if block is None:
                issues.append(
                    f"API declaration @param missing for parameter {name}: {label}"
                )
            elif not _description_covers(block, expected):
                issues.append(
                    f"API declaration parameter description for {name} "
                    f"missing or mismatched: {label}"
                )

    return_type = api.get("returnType")
    if isinstance(return_type, dict):
        expected = _localized_description(return_type.get("description"), language)
        if expected is not None and not _description_is_not_applicable(expected):
            block = None
            for tag in ("returns", "return", "retval", "result"):
                block = _tag_block(context, tag)
                if block is not None:
                    break
            if block is None:
                issues.append(
                    f"API declaration @returns missing or mismatched: {label}"
                )
            elif not _description_covers(block, expected):
                issues.append(
                    f"API declaration return description missing or mismatched: {label}"
                )

    error_codes = api.get("errorCodes")
    if isinstance(error_codes, list):
        for index, error_code in enumerate(error_codes, start=1):
            if not isinstance(error_code, dict):
                continue
            expected = _localized_description(error_code.get("description"), language)
            if expected is None or _description_is_not_applicable(expected):
                continue
            if not _description_covers(context, expected):
                issues.append(
                    f"API declaration errorCodes[{index}] description "
                    f"missing or mismatched: {label}"
                )

    return issues


def _declaration_comment_format_issues(
    added_lines: list[str], declaration_index: int, label: str
) -> list[str]:
    """Require a doc comment to hug and align with its added declaration."""

    declaration = added_lines[declaration_index]
    declaration_indent = declaration[: len(declaration) - len(declaration.lstrip())]
    close: int | None = None
    single_line_comment = False
    for index in range(declaration_index - 1, -1, -1):
        if added_lines[index].strip():
            if _is_single_line_doc_comment(added_lines[index]):
                close = index
                single_line_comment = True
            elif added_lines[index].strip() == "*/":
                close = index
            break
    if close is None:
        return []
    start: int | None = close if single_line_comment else None
    for index in range(close, -1, -1):
        if "/**" in added_lines[index] or "/*!" in added_lines[index]:
            start = index
            break
    if start is None:
        return []

    issues: list[str] = []
    if any(not line.strip() for line in added_lines[close + 1 : declaration_index]):
        issues.append(
            f"blank line between declaration comment and declaration: {label}"
        )
    if any(not line.strip() for line in added_lines[start + 1 : close]):
        issues.append(f"blank line inside declaration comment: {label}")

    start_line = added_lines[start]
    start_indent = start_line[: len(start_line) - len(start_line.lstrip())]
    if start_indent != declaration_indent:
        issues.append(
            f"API declaration comment opener indent does not match declaration indent: {label}"
        )
    return issues


def _api_diff_marker_issues(
    api: dict,
    diff_sides: dict[str, object],
    language: str,
    diff_language: str,
    *,
    same_signature_count: int = 1,
    claimed_candidate_keys: set[tuple[int, int, int]] | None = None,
) -> list[str]:
    declaration = str(api.get("declaration") or "")
    label = api.get("id") or api.get("name") or "unnamed"
    candidates = _target_api_candidates(api, diff_sides)
    if not candidates:
        return [f"API declaration missing from new-side diff lines: {label}"]

    identity_candidates = _selected_target_candidates(api, candidates)
    if same_signature_count > 1 or len(candidates) > 1:
        if len(identity_candidates) != 1:
            return [
                "API declaration evidence is ambiguous for a duplicate "
                f"signature; include the API id or qualifiedName in its doc comment, or provide a unique source position: {label}"
            ]
        candidates = identity_candidates

    if len(candidates) != 1:
        return [
            "API declaration evidence is ambiguous; include the API id or "
            f"qualifiedName in its doc comment, or provide one changed declaration: {label}"
        ]

    segment, declaration_index, declaration_end, context = candidates[0]
    candidate_key = (id(segment), declaration_index, declaration_end)
    if claimed_candidate_keys is not None and candidate_key in claimed_candidate_keys:
        return [
            "API declaration evidence is already bound to another API; provide "
            f"a separate declaration window: {label}"
        ]
    if not _selected_target_candidate_changed(
        api,
        diff_sides,
        candidates[0],
        duplicate_signature=same_signature_count > 1,
    ):
        return [
            "API declaration evidence does not modify the target API "
            f"declaration or comment: {label}"
        ]
    if context is None:
        return [
            "API declaration marker comment missing or was removed; include "
            f"the complete doc comment and declaration in one continuous hunk: {label}"
        ]

    new_lines: list[str] = segment["lines"]  # type: ignore[index]
    issues = (
        _declaration_comment_format_issues(new_lines, declaration_index, str(label))
        + _declaration_comment_style_issues(context, str(label))
        + _api_description_closure_issues(api, context, diff_language)
        + _api_marker_issues(api, context, language, diff_language, label)
    )
    if not issues and claimed_candidate_keys is not None:
        claimed_candidate_keys.add(candidate_key)
    return issues


def _api_marker_issues(
    api: dict,
    context: str,
    language: str,
    diff_language: str,
    label: object,
) -> list[str]:
    """Check declaration markers for one API-specific comment context."""

    issues: list[str] = []
    if not _since_marker_present(context, api.get("since")):
        issues.append(f"API declaration marker @since missing or mismatched: {label}")
    if not _marker_present(context, "syscap", api.get("syscap")):
        issues.append(f"API declaration marker @syscap missing or mismatched: {label}")

    permissions = _api_permission_values(api)
    if permissions:
        for permission in permissions:
            if not _marker_present(context, "permission", permission):
                issues.append(
                    f"API declaration marker @permission missing value {permission}: {label}"
                )
    elif "@permission" in context.lower():
        issues.append(f"API declaration has unexpected @permission marker: {label}")

    if language == "arkts":
        platform = api.get("platform")
        if isinstance(platform, dict):
            markers = {
                "crossplatform": "@crossplatform",
                "atomicservice": "@atomicservice",
                "form": "@form",
            }
            for field, marker in markers.items():
                enabled = platform.get(field)
                if isinstance(enabled, dict):
                    enabled = enabled.get("enabled")
                marker_name = marker[1:]
                if enabled is True and not _marker_present(context, marker_name):
                    issues.append(f"API declaration marker {marker} missing: {label}")
                if enabled is False and _marker_present(context, marker_name):
                    issues.append(f"API declaration has unexpected {marker} marker: {label}")

        model = str(api.get("applicationModel") or "")
        stage_marker = _marker_present(context, "stagemodelonly")
        fa_marker = _marker_present(context, "famodelonly")
        if model == "stage-only" and not stage_marker:
            issues.append(f"API declaration marker @stagemodelonly missing: {label}")
        if model == "stage-only" and fa_marker:
            issues.append(f"API declaration has unexpected @famodelonly marker: {label}")
        if model == "fa-only" and not fa_marker:
            issues.append(f"API declaration marker @famodelonly missing: {label}")
        if model == "fa-only" and stage_marker:
            issues.append(f"API declaration has unexpected @stagemodelonly marker: {label}")
        if model in {"fa-and-stage", "both"} and (stage_marker or fa_marker):
            issues.append(
                f"API declaration has unexpected model-only marker for {model}: {label}"
            )
    return issues


_STRUCTURAL_DOC_TAG_NAMES = {
    "since", "syscap", "permission", "crossplatform", "atomicservice", "form",
    "stagemodelonly", "famodelonly",
}


def _tag_style_prose(prose: str) -> str:
    """Extract natural language from a documentation tag.

    Parameter names, type expressions, error-code constants, and other contract
    identifiers are not prose. Style rules must apply only to the description
    after the tag payload.
    """

    match = re.match(r"@([A-Za-z]+)(.*)", prose, flags=re.IGNORECASE)
    if match is None:
        return prose
    tag = match.group(1).lower()
    payload = match.group(2).strip()
    if tag in _STRUCTURAL_DOC_TAG_NAMES:
        return ""
    if tag == "param":
        parameter = re.fullmatch(
            r"(?:\[(?:in|out|inout|in-out|input|output)\])?"
            r"(?:(?:\s*\{[^}]*\})?\s*)"
            r"(?:\[?([A-Za-z_$][\w$]*)\]?)\s*(.*)",
            payload,
            flags=re.IGNORECASE,
        )
        if parameter is not None:
            description = parameter.group(2).strip()
            return re.sub(r"^[-—–:]\s*", "", description)
    if tag in {"returns", "return", "retval", "result", "throws", "exception"}:
        description = re.sub(r"^\{[^}]*\}\s*", "", payload)
        return re.sub(r"^[-—–:]\s*", "", description)
    if tag in {"brief", "details", "description", "note", "notes", "remarks"}:
        return re.sub(r"^[-—–:]\s*", "", payload)
    return ""


def _declaration_comment_style_issues(context: str, label: str) -> list[str]:
    """Check prose in the doc block associated with one API declaration.

    The context is already cleaned of JSDoc/Doxygen line decorations. The
    shared style rules apply only to natural-language prose, not to contract
    identifiers carried by documentation tags.
    """

    issues: list[str] = []
    for line_number, line in enumerate(context.splitlines(), start=1):
        if not line or line in {"/**", "/*!", "/"}:
            continue
        prose = _tag_style_prose(line)
        if not prose:
            continue
        if _description_is_not_applicable(prose):
            issues.append(
                f"API declaration comment for {label}: line {line_number} "
                "must omit N/A / 不适用 placeholder prose"
            )
            continue
        issues.extend(
            text_style_issues(
                prose,
                f"API declaration comment for {label}",
                f"line {line_number}",
            )
        )
    return issues


def validate_api_declaration_diffs(
    change_dir: Path, reporter: Reporter, *, archive: bool
) -> None:
    """Require language/repository-specific en/zh declaration diffs.

    ArkTS and C metadata are separate contracts and are delivered in separate API
    declaration repositories, so their diff evidence must not be mixed.
    """

    proposal_path = change_dir / "proposal.md"
    if not proposal_path.is_file():
        return
    involvement = api_sdk_involvement(_visible_markdown(read_text(proposal_path)))
    if involvement != "是":
        return

    metadata_files = sorted(
        name for name in API_METADATA_FILES if (change_dir / name).is_file()
    )
    diff_prefixes = {
        "arkts-api-spec.yaml": "task1-arkts-api-declaration",
        "c-api-spec.yaml": "task1-c-api-declaration",
    }
    required_diffs = [
        f"{diff_prefixes[name]}-{language}.diff"
        for name in metadata_files
        for language in ("en", "zh")
    ]
    legacy_missing = [
        name
        for name in ("task1-api-declaration-en.diff", "task1-api-declaration-zh.diff")
        if (change_dir / "evidence" / name).is_file()
    ]
    if legacy_missing:
        reporter.fail(
            "Mixed-repository API declaration diffs are no longer accepted; split by "
            "language into task1-arkts-api-declaration-en/zh.diff and/or "
            "task1-c-api-declaration-en/zh.diff: " + ", ".join(legacy_missing)
        )

    missing = [
        name
        for name in required_diffs
        if not (change_dir / "evidence" / name).is_file()
    ]
    if missing:
        draft_warn_archive_fail(
            reporter,
            archive,
            "API declaration diff evidence missing under evidence/: " + ", ".join(missing),
        )
        return

    invalid: list[str] = []
    diff_sides_by_diff: dict[str, dict[str, dict[str, object]]] = {}
    for name in required_diffs:
        path = change_dir / "evidence" / name
        try:
            diff_text = path.read_text(encoding="utf-8")
            valid = valid_unified_diff(diff_text)
            if valid:
                diff_sides_by_diff[name] = unified_diff_sides(diff_text)
        except (OSError, UnicodeError):
            valid = False
        if not valid:
            invalid.append(name)
    if invalid:
        draft_warn_archive_fail(
            reporter,
            archive,
            "API declaration diff evidence must contain nonempty valid unified diffs: "
            + ", ".join(invalid),
        )
        return

    metadata_issues: list[str] = []
    if (change_dir / API_LEGACY_METADATA_FILE).exists():
        metadata_issues.append(
            f"{API_LEGACY_METADATA_FILE} is no longer accepted; split it into "
            "arkts-api-spec.yaml and/or c-api-spec.yaml"
        )
    if not metadata_files:
        metadata_issues.append(
            "At least one language-specific API metadata file is required: "
            "arkts-api-spec.yaml or c-api-spec.yaml"
        )

    for metadata_file in metadata_files:
        try:
            metadata = parse_api_spec(change_dir / metadata_file)
        except (OSError, UnicodeError, ValueError) as error:
            metadata_issues.append(f"{metadata_file}: cannot parse API metadata: {error}")
            continue
        expected_language = next(
            language
            for language, name in API_METADATA_BY_LANGUAGE.items()
            if name == metadata_file
        )
        language = metadata.get("language")
        if language != expected_language:
            metadata_issues.append(f"{metadata_file}: language must be {expected_language}")
            continue

        prefix = diff_prefixes[metadata_file]
        metadata_apis = metadata.get("apis")
        if not isinstance(metadata_apis, list):
            metadata_issues.append(
                f"{metadata_file}: API metadata: apis must be a non-empty list"
            )
            continue
        api_entries = [
            api
            for api in metadata_apis
            if isinstance(api, dict)
        ]
        allowed_paths = {
            str(api.get("filePath") or "").strip()
            for api in api_entries
            if str(api.get("filePath") or "").strip()
        }
        signature_counts = Counter(
            (
                str(api.get("filePath") or "").strip(),
                str(api.get("declaration") or ""),
            )
            for api in api_entries
        )
        for diff_language in ("en", "zh"):
            diff_name = f"{prefix}-{diff_language}.diff"
            diff_sides_by_file = diff_sides_by_diff[diff_name]
            claimed_candidate_keys: set[tuple[int, int, int]] = set()
            allowed_diff_paths = {
                diff_path
                for diff_path in diff_sides_by_file
                if any(
                    _diff_path_matches(diff_path, allowed_path)
                    for allowed_path in allowed_paths
                )
            }
            extra_targets = sorted(set(diff_sides_by_file) - allowed_diff_paths)
            if extra_targets:
                metadata_issues.append(
                    f"{diff_language} declaration diff {diff_name} contains unrelated target file(s): "
                    + ", ".join(extra_targets)
                )
            for api in api_entries:
                if not isinstance(api, dict):
                    continue
                label = api.get("id") or api.get("name") or "unnamed"
                file_path = str(api.get("filePath") or "").strip()
                if not file_path:
                    continue
                matching_files = [
                    diff_path
                    for diff_path in diff_sides_by_file
                    if _diff_path_matches(diff_path, file_path)
                ]
                if not matching_files:
                    metadata_issues.append(
                        f"{diff_language} declaration diff {diff_name} missing target file for API {label}: {file_path}"
                    )
                    continue
                issues: list[str] = []
                for diff_path in matching_files:
                    current_issues = _api_diff_marker_issues(
                        api,
                        diff_sides_by_file[diff_path],
                        str(language),
                        diff_language,
                        same_signature_count=signature_counts[
                            (file_path, str(api.get("declaration") or ""))
                        ],
                        claimed_candidate_keys=claimed_candidate_keys,
                    )
                    if not current_issues:
                        issues = []
                        break
                    issues.extend(current_issues)
                for issue in issues:
                    metadata_issues.append(f"{diff_language} {issue}")

    if metadata_issues:
        for issue in metadata_issues:
            draft_warn_archive_fail(reporter, archive, issue)
    else:
        reporter.pass_(
            "language-specific API declaration diff evidence is archived and covers "
            "added declarations, markers, and documentation closure"
        )


def validate_proposal_tables(proposal: str, reporter: Reporter, *, archive: bool, lite: bool = False) -> None:
    """Validate required device-variation and external-dependency proposal tables."""

    issues: list[str] = []
    device_section = section_text(proposal, DEVICE_VARIATION_SECTION)
    device_tables = tables_with_columns(device_section, DEVICE_VARIATION_COLUMNS)
    # Lite explicitly rules out device-dependent scope in compile_contract;
    # it omits only the device matrix, never the dependency declaration below.
    if not lite and not device_tables:
        issues.append(f"{DEVICE_VARIATION_SECTION} table missing required columns")
    elif not lite:
        rows = device_tables[0]
        by_label: dict[str, list[dict[str, str]]] = {}
        for row in rows:
            label = row.get("设备/差异项", "").strip()
            by_label.setdefault(label, []).append(row)
        for label in DEVICE_VARIATION_ROWS:
            matches = by_label.get(label, [])
            if not matches:
                issues.append(f"{DEVICE_VARIATION_SECTION} missing row: {label}")
                continue
            if len(matches) > 1:
                issues.append(f"{DEVICE_VARIATION_SECTION} duplicate row: {label}")
                continue
            row = matches[0]
            verdict = row.get("是否存在差异", "").strip()
            if verdict not in {"是", "否"}:
                issues.append(f"{DEVICE_VARIATION_SECTION} {label} must state 是 or 否")
            if not meaningful(row.get("差异说明", "")):
                issues.append(f"{DEVICE_VARIATION_SECTION} {label} requires 差异说明")
        unknown = sorted(label for label in by_label if label and label not in DEVICE_VARIATION_ROWS)
        if unknown:
            issues.append(f"{DEVICE_VARIATION_SECTION} has unknown rows: {', '.join(unknown)}")

    dependency_section = section_text(proposal, EXTERNAL_DEPENDENCIES_SECTION)
    dependency_tables = tables_with_columns(dependency_section, EXTERNAL_DEPENDENCIES_COLUMNS)
    if not dependency_tables or not dependency_tables[0]:
        issues.append(f"{EXTERNAL_DEPENDENCIES_SECTION} requires at least one dependency or 不涉及 row")
    else:
        dependency_rows = dependency_tables[0]
        not_applicable_rows = [
            index
            for index, row in enumerate(dependency_rows, start=1)
            if row.get("子系统", "").strip() == "不涉及"
        ]
        if not_applicable_rows and len(dependency_rows) != 1:
            issues.append(
                f"{EXTERNAL_DEPENDENCIES_SECTION} 不涉及 row is mutually exclusive with dependency rows"
            )
        for index, row in enumerate(dependency_rows, start=1):
            subsystem = row.get("子系统", "").strip()
            dependency_type = row.get("依赖类型", "").strip()
            if subsystem == "不涉及":
                if not meaningful(dependency_type) or dependency_type in {"不涉及", "无", "无依赖", "无外部依赖"}:
                    issues.append(f"{EXTERNAL_DEPENDENCIES_SECTION} row {index} 不涉及 requires a concrete reason in 依赖类型")
                continue
            for column in EXTERNAL_DEPENDENCIES_COLUMNS:
                if not meaningful(row.get(column, "")):
                    issues.append(f"{EXTERNAL_DEPENDENCIES_SECTION} row {index} requires {column}")

    if issues:
        draft_warn_archive_fail(reporter, archive, "proposal structured tables incomplete: " + "; ".join(issues))
    else:
        reporter.pass_("proposal device-variation and external-dependency tables are complete")


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


def _parse_dfx_involved_repo_declarations(subsection_text: str) -> list[list[str]]:
    """Parse every structured ``涉及仓库`` declaration in the subsection."""
    declarations: list[list[str]] = []
    for match in _DFX_INVOLVED_REPOS_RE.finditer(subsection_text):
        declarations.append([
            item.strip().strip("`")
            for item in re.split(r"[,，、;；+]", match.group(1))
            if item.strip().strip("`")
        ])
    return declarations


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
    involved_declarations = _parse_dfx_involved_repo_declarations(subsection_text)
    status_tables = tables_with_columns(subsection_text, _DFX_REPO_STATUS_COLUMNS)
    involved_repos = involved_declarations[0] if involved_declarations else []
    status_rows = status_tables[0] if status_tables else []
    structured_present = bool(involved_declarations or status_tables)
    if not structured_present and not archive_mode:
        return False

    # Conflicting structured evidence is never a Draft compatibility warning:
    # accepting only the first declaration/table would let later UNKNOWN or
    # extra-repository evidence bypass both Draft and Archive validation.
    multiplicity_issues: list[str] = []
    if len(involved_declarations) > 1:
        multiplicity_issues.append(
            f"multiple 涉及仓库 declarations ({len(involved_declarations)})"
        )
    if len(status_tables) > 1:
        multiplicity_issues.append(
            f"multiple 仓库/状态/理由 closure tables ({len(status_tables)})"
        )
    if multiplicity_issues:
        reporter.fail(
            "design.md: conflicting DFX per-repository no-hit evidence: "
            + "; ".join(multiplicity_issues)
        )
        return True

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
            issues.append(f"{repo}: NO_DFX_KNOWLEDGE reason must be exactly '仓无 DFX 知识'; put additional explanation outside the table")
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


_DEFAULT_AC_ID_PATTERN = rf"^{AC_ID_RE.pattern}$"
AC_REFERENCE_CANDIDATE_RE = re.compile(r"(?<![\w-])AC-[^\s,，、;；]*")


def _get_ac_id_pattern() -> str:
    """Read the configured syntax constraint; retain the canonical ASCII default."""
    try:
        return contract_scalar("ac_id_pattern")
    except (ValueError, KeyError):
        return ""


def ac_reference_candidates(cell: str) -> list[str]:
    """Remove paired Markdown formatting, preserving each complete candidate id.

    Only whitespace and explicit list separators terminate an id. In particular,
    a hyphen, underscore or trailing dot remains in the candidate for fullmatch.
    """
    text = re.sub(r"(`+)([^\n]*?)\1", lambda match: match[2], cell)
    text = re.sub(r"(\*\*|__|~~)([^\n]*?)\1", lambda match: match[2], text)
    return AC_REFERENCE_CANDIDATE_RE.findall(text)


def defined_ac_ids(spec: str) -> set[str]:
    """Shared definition set for traceability and DFX closure; examples are inert."""
    visible = _visible_markdown(spec)
    return set(AC_RE.findall("\n".join(AC_DEF_RE.findall(visible))))


def validate_ac_id_format(change_dir: Path, reporter: Reporter, *, archive: bool) -> None:
    """Check visible definitions and complete ids in verification/Task mappings.

    Draft warns; Archive/design-docs submission fails. The same check is used by
    the existing validate_ac_ids entry point before downstream artifact checks.
    """
    raw = _get_ac_id_pattern()
    try:
        pattern = re.compile(raw or _DEFAULT_AC_ID_PATTERN)
    except re.error:
        draft_warn_archive_fail(
            reporter, archive,
            f"artifacts.yaml resource_contract.ac_id_pattern 包含非法正则 '{raw}'，"
            f"已回退默认 {_DEFAULT_AC_ID_PATTERN}",
        )
        pattern = re.compile(_DEFAULT_AC_ID_PATTERN)

    spec_path = change_dir / "spec.md"
    if spec_path.is_file():
        spec = read_text(spec_path)
        definitions = AC_DEFINITION_ID_RE.findall(_visible_markdown(spec))
        invalid = sorted(set(token for token in definitions if not pattern.fullmatch(token)))
        if invalid:
            draft_warn_archive_fail(
                reporter, archive,
                "spec.md invalid AC identifiers: " + ", ".join(invalid)
                + "; expected AC-<用户故事号>.<序号>; format rule: " + pattern.pattern,
            )
        elif definitions:
            reporter.pass_(f"spec.md AC identifier format valid ({len(definitions)} definitions)")

    sources = (
        ("spec.md", "验证映射", ["AC", "验证方式"]),
        ("execution-plan.md", "AC 到 Task 追溯", ["AC", "Task", "验证方式"]),
    )
    for filename, section, columns in sources:
        path = change_dir / filename
        if not path.is_file():
            continue
        body = section_text(read_text(path), section)
        for row in table_with_columns(body, columns):
            for token in ac_reference_candidates(row.get("AC", "")):
                if not pattern.fullmatch(token):
                    draft_warn_archive_fail(
                        reporter, archive,
                        f"{filename} {section}: AC 编号 '{token}' 不符合格式规则 {pattern.pattern}",
                    )


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

    return parse_eight_dim_involvement(proposal, "性能")


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


def unresolved_markers(text: str, *, start_line: int = 1) -> list[str]:
    markers: list[str] = []
    in_fence = False

    for line_no, line in enumerate(text.splitlines(), start=start_line):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        # API text has its own explicit placeholder policy. Do not reinterpret
        # source identifiers or quoted literals with generic prose heuristics.
        api_signature = api_heading_signature(line)
        if api_signature is not None:
            if not api_signature_complete(api_signature):
                markers.append(f"L{line_no}: unresolved API signature placeholder")
            continue

        line = PROHIBITED_LITERAL_LIST_RE.sub(lambda match: " " * len(match[0]), line)
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


def unresolved_section_markers(text: str, sections: list[str]) -> list[str]:
    markers: list[str] = []
    for section in sections:
        title = str(section)
        for body, start_line in section_texts_with_lines(text, title):
            markers.extend(f"{title} {marker}"
                           for marker in unresolved_markers(body, start_line=start_line))
    return markers


def sorted_ids(ids: set[str]) -> list[str]:
    def key(value: str) -> tuple[int, ...]:
        nums = re.findall(r"\d+", value)
        return tuple(int(num) for num in nums)

    return sorted(ids, key=key)


def validate_slug(slug: str, reporter: Reporter) -> bool:
    """Validate the English slug component shared by formal and draft paths."""
    if len(slug) > MAX_SLUG_LENGTH:
        reporter.fail(f"change directory slug exceeds {MAX_SLUG_LENGTH} characters: {slug}")
        return False
    if not SLUG_RE.fullmatch(slug):
        reporter.fail(
            "change directory slug is invalid (use lowercase letters/digits and single hyphens): "
            f"{slug}"
        )
        return False
    return True


def expected_repository_name(repository_root: Path) -> str:
    """Return the origin repository name, falling back to the checkout basename."""
    try:
        top_level = subprocess.run(
            ["git", "-C", str(repository_root), "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
        if top_level.returncode != 0 or Path(top_level.stdout.strip()).resolve() != repository_root.resolve():
            return repository_root.name
        result = subprocess.run(
            ["git", "-C", str(repository_root), "remote", "get-url", "origin"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        result = None

    if result is not None and result.returncode == 0:
        remote = result.stdout.strip().rstrip("/")
        if remote:
            name = remote.rsplit("/", 1)[-1].rsplit(":", 1)[-1]
            if name.endswith(".git"):
                name = name[:-4]
            if REPOSITORY_NAME_RE.fullmatch(name):
                return name
    return repository_root.name


def repository_origin_url(repository_root: Path) -> str | None:
    """Return origin only when repository_root itself is the Git top level."""

    try:
        top_level = subprocess.run(
            ["git", "-C", str(repository_root), "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
        if top_level.returncode != 0 or Path(top_level.stdout.strip()).resolve() != repository_root.resolve():
            return None
        result = subprocess.run(
            ["git", "-C", str(repository_root), "remote", "get-url", "origin"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None

    return result.stdout.strip() or None


def repository_head_commit(repository_root: Path) -> str | None:
    """Return the full HEAD commit only for the repository rooted at repository_root."""
    try:
        top_level = subprocess.run(
            ["git", "-C", str(repository_root), "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
        if (
            top_level.returncode != 0
            or Path(top_level.stdout.strip()).resolve() != repository_root.resolve()
        ):
            return None
        result = subprocess.run(
            ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    commit = result.stdout.strip()
    return commit.lower() if result.returncode == 0 and re.fullmatch(r"[0-9a-fA-F]{40}", commit) else None


def gitcode_repository_identity(remote: str) -> str | None:
    """Parse supported HTTPS, SSH URL, and SCP-style GitCode remotes."""

    remote = remote.strip().rstrip("/")
    if remote.endswith(".git"):
        remote = remote[:-4]
    match = re.search(
        r"(?:^|@|//)gitcode\.com(?::\d+)?[/:]([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$",
        remote,
        re.IGNORECASE,
    )
    if not match:
        return None
    return f"{match.group(1)}/{match.group(2)}"


def validate_dir_name(change_dir: Path, reporter: Reporter) -> None:
    change_dir = change_dir.resolve()
    repository_segment = change_dir.parent
    changes_dir = repository_segment.parent
    codespec_dir = changes_dir.parent
    repository_root = codespec_dir.parent
    if changes_dir.name != "changes" or codespec_dir.name != "codespec":
        reporter.fail(
            "change directory layout must be exactly codespec/changes/<repo-name>/<proposal-id-or-draft>"
        )
        return

    expected_repo = expected_repository_name(repository_root)
    if repository_segment.name in {".", ".."} or not REPOSITORY_NAME_RE.fullmatch(repository_segment.name):
        reporter.fail(f"repository path segment is invalid: {repository_segment.name}")
        return
    if repository_segment.name != expected_repo:
        reporter.fail(
            "repository path segment must match the current repository name "
            f"'{expected_repo}': {repository_segment.name}"
        )
        return
    reporter.pass_(f"archive repository path is valid: codespec/changes/{expected_repo}")
    name = change_dir.name
    proposal = change_dir / "proposal.md"
    frontmatter = read_frontmatter(proposal)
    if frontmatter.invalid_reason is not None:
        reporter.fail(f"proposal.md: invalid frontmatter ({frontmatter.invalid_reason})")
        return
    proposal_id = trim_yaml_whitespace(frontmatter.get("proposal_id", ""))
    draft_match = DRAFT_RE.fullmatch(name)
    if draft_match and not proposal_id:
        if validate_slug(draft_match.group(1), reporter):
            reporter.pass_(f"change directory name is valid draft path: {name}")
        return

    if not proposal_id:
        reporter.fail("proposal.md: proposal_id frontmatter is required for a formal change directory")
        return
    if not PROPOSAL_ID_RE.fullmatch(proposal_id):
        reporter.fail(f"proposal.md: proposal_id '{proposal_id}' is invalid (formal proposal-id must contain digits only)")
        return

    if name != proposal_id:
        reporter.fail(f"change directory name must exactly match proposal.md proposal_id '{proposal_id}': {name}")
        return
    reporter.pass_(f"change directory name is valid formal proposal_id path: {name}")


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


def validate_sessions_sidecar(change_dir: Path, reporter: Reporter) -> None:
    """Validate the ``.sessions.json`` sidecar (authoritative session tracking source).

    Checks:
    - Valid JSON with expected structure (dict of deliverable → {sessions, log})
    - All session IDs match a multi-platform format:
      opencode ``ses_*``, codex/claude ``<uuid>``
    - Warn on duplicate IDs in ``sessions`` arrays
    - Cross-check frontmatter ``sessions`` field matches sidecar (warn on mismatch)
    """
    print("\nLevel A3b: Session ID Sidecar (.sessions.json)")
    sidecar_path = change_dir / ".sessions.json"
    if not sidecar_path.is_file():
        print("  (.sessions.json not found — skipped; sidecar is optional but recommended)")
        return

    try:
        raw = sidecar_path.read_text(encoding="utf-8-sig")
    except OSError as error:
        reporter.fail(f".sessions.json: cannot read file: {error}")
        return

    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as error:
        reporter.fail(f".sessions.json: invalid JSON: {error}")
        return

    if not isinstance(data, dict):
        reporter.fail(".sessions.json: top-level value must be a JSON object (dict)")
        return

    any_checked = False
    for deliverable_name, entry in data.items():
        if not isinstance(deliverable_name, str) or not deliverable_name.strip():
            reporter.fail(f".sessions.json: empty or non-string deliverable key")
            continue
        if not isinstance(entry, dict):
            reporter.fail(f".sessions.json: '{deliverable_name}' entry must be an object")
            continue

        any_checked = True

        # sessions array validation
        sessions = entry.get("sessions")
        if sessions is None:
            reporter.warn(f".sessions.json: '{deliverable_name}' has no 'sessions' array")
        elif not isinstance(sessions, list):
            reporter.fail(f".sessions.json: '{deliverable_name}' sessions must be a list (array)")
        else:
            invalid = [s for s in sessions if not SESSION_ID_RE.match(str(s).strip())]
            if invalid:
                reporter.fail(
                    f".sessions.json: '{deliverable_name}' sessions contains invalid ID(s): "
                    f"{', '.join(str(s) for s in invalid)}"
                )
            else:
                # Duplicate check
                seen = set()
                duplicates = []
                for sid in sessions:
                    sid_str = str(sid).strip()
                    if sid_str in seen:
                        duplicates.append(sid_str)
                    seen.add(sid_str)
                if duplicates:
                    reporter.warn(
                        f".sessions.json: '{deliverable_name}' sessions has duplicate ID(s): "
                        f"{', '.join(sorted(set(duplicates)))}"
                    )
                else:
                    reporter.pass_(
                        f".sessions.json: '{deliverable_name}' sessions has "
                        f"{len(sessions)} valid session ID(s)"
                    )

                # Cross-check with frontmatter (deliverable .md files only)
                deliverable_path = change_dir / deliverable_name
                if deliverable_name.endswith(".md") and deliverable_path.is_file():
                    frontmatter = read_frontmatter(deliverable_path)
                    if not frontmatter.invalid_reason:
                        fm_sessions_str = frontmatter.get("sessions", "").strip()
                        fm_ids = set(s.strip() for s in fm_sessions_str.split(",") if s.strip())
                        sidecar_ids = set(str(s).strip() for s in sessions)
                        if fm_ids != sidecar_ids:
                            reporter.warn(
                                f".sessions.json: '{deliverable_name}' frontmatter sessions "
                                f"({','.join(sorted(fm_ids)) if fm_ids else 'empty'}) "
                                f"!= sidecar sessions "
                                f"({','.join(sorted(sidecar_ids))})"
                            )

        # log array validation
        log = entry.get("log")
        if log is not None:
            if not isinstance(log, list):
                reporter.fail(f".sessions.json: '{deliverable_name}' log must be a list (array)")
            else:
                for i, record in enumerate(log):
                    if not isinstance(record, dict):
                        reporter.fail(
                            f".sessions.json: '{deliverable_name}' log[{i}] must be an object"
                        )
                        continue
                    rec_session = str(record.get("session", "")).strip()
                    if not SESSION_ID_RE.match(rec_session):
                        reporter.fail(
                            f".sessions.json: '{deliverable_name}' log[{i}] "
                            f"session '{rec_session}' is invalid"
                        )

    if not any_checked:
        print("  (.sessions.json is empty — no deliverable entries found)")


def validate_metadata_tracking(change_dir: Path, reporter: Reporter, required: bool = False) -> None:
    """Validate the design-docs metadata sidecar when present or required."""

    path = change_dir / "metadata_tracking.yaml"
    print("\nLevel A2: Design-docs Metadata")
    if not path.is_file():
        if required:
            reporter.fail("metadata_tracking.yaml missing for design-docs submission")
        return

    try:
        metadata = parse_metadata_tracking(str(path))
    except (OSError, ValueError) as error:
        reporter.fail(f"metadata_tracking.yaml is invalid: {error}")
        return

    initial_failures = reporter.failed
    proposal_id = str(metadata.get("proposal_id", "")).strip()
    if not PROPOSAL_ID_RE.fullmatch(proposal_id):
        reporter.fail("metadata_tracking.yaml: proposal_id must contain digits only")
    elif proposal_id != change_dir.name:
        reporter.fail("metadata_tracking.yaml: proposal_id does not match the change directory")
    else:
        frontmatter_proposal_id = trim_yaml_whitespace(read_frontmatter(change_dir / "proposal.md").get("proposal_id", ""))
        if proposal_id != frontmatter_proposal_id:
            reporter.fail("metadata_tracking.yaml: proposal_id does not match proposal.md")
        else:
            reporter.pass_("metadata_tracking.yaml: proposal_id matches directory and proposal.md")

    target_release = str(metadata.get("target_release", "")).strip()
    proposal_release = trim_yaml_whitespace(
        read_frontmatter(change_dir / "proposal.md").get("target_release", "")
    )
    if not target_release:
        reporter.fail("metadata_tracking.yaml: target_release is required")
    elif target_release != proposal_release:
        reporter.fail("metadata_tracking.yaml: target_release does not match proposal.md")
    else:
        reporter.pass_("metadata_tracking.yaml: target_release matches proposal.md")

    repos = metadata.get("repos")
    if not isinstance(repos, list) or not repos:
        reporter.fail("metadata_tracking.yaml: repos must contain at least one repository")
        return

    repository_root = change_dir.resolve().parent.parent.parent.parent
    origin = repository_origin_url(repository_root)
    current_remote = parse_git_remote(origin) if origin else None
    current_identity = current_remote.repository if current_remote else None
    current_is_gitcode = bool(current_remote and current_remote.host == "gitcode.com")
    current_head = repository_head_commit(repository_root) if current_identity else None

    def is_current_repository(web_repo):
        return bool(current_remote and web_repo
                    and web_repo.repository == current_identity
                    and web_repo.host == current_remote.host
                    and (current_remote.scheme != "https" or web_repo.port == current_remote.port))

    explicit_current = any(
        isinstance(entry, dict)
        and str(entry.get("repo", "")).strip() == current_identity
        and is_current_repository(metadata_repository_url(str(entry.get("repository_url", ""))))
        for entry in repos
    )
    repository_names: set[str] = set()
    repository_keys: set[tuple[str, int, str]] = set()
    current_seen = False
    for index, entry in enumerate(repos, start=1):
        if not isinstance(entry, dict):
            reporter.fail(f"metadata_tracking.yaml: repos[{index}] must be a mapping")
            continue
        unknown_repo_fields = sorted(set(entry) - {"repo", "repository_url", "pull_requests", "issues"})
        if unknown_repo_fields:
            reporter.fail(
                f"metadata_tracking.yaml: repos[{index}] has unknown fields: "
                + ", ".join(unknown_repo_fields)
            )
        repo = str(entry.get("repo", "")).strip()
        repo_is_valid = (
            re.fullmatch(r"(?:[A-Za-z0-9_.-]+/)+[A-Za-z0-9_.-]+", repo) is not None
            and all(part not in {".", ".."} for part in repo.split("/"))
        )
        if not repo_is_valid:
            reporter.fail(
                f"metadata_tracking.yaml: repos[{index}].repo must use organization/repository form"
            )
        else:
            repository_names.add(repo)

        explicit_url = "repository_url" in entry
        repo_url = str(entry.get("repository_url", f"https://gitcode.com/{repo}")).strip()
        web_repo = metadata_repository_url(repo_url)
        if not web_repo or web_repo.repository != repo:
            reporter.fail("metadata_tracking.yaml: repository_url must be a credential-free HTTPS repository URL matching repo")
        # Backward compatibility: an unqualified empty current-origin entry may
        # represent a non-GitCode source, but cannot contain host-specific records.
        legacy_empty_origin = (not explicit_url and repo == current_identity
                               and not explicit_current
                               and not current_is_gitcode and not entry.get("pull_requests")
                               and not entry.get("issues"))
        entry_host = current_remote.host if legacy_empty_origin and current_remote else (web_repo.host if web_repo else "")
        entry_port = (current_remote.port if current_remote and current_remote.scheme == "https" else 443) if legacy_empty_origin else (web_repo.port if web_repo else 443)
        current_entry = bool(current_remote and repo == current_identity and entry_host == current_remote.host
                             and (current_remote.scheme != "https" or entry_port == current_remote.port))
        current_seen |= current_entry
        key = (entry_host, entry_port, repo)
        if key in repository_keys:
            reporter.fail(f"metadata_tracking.yaml: duplicate repo entry: {repo} ({entry_host}:{entry_port})")
        repository_keys.add(key)

        if "pull_requests" not in entry:
            reporter.fail(f"metadata_tracking.yaml: {repo or index} pull_requests is required")
        pull_requests = entry.get("pull_requests", [])
        if not isinstance(pull_requests, list):
            reporter.fail(f"metadata_tracking.yaml: {repo or index} pull_requests must be a list")
            pull_requests = []
        for pr_index, pull_request in enumerate(pull_requests, start=1):
            if not isinstance(pull_request, dict):
                reporter.fail(f"metadata_tracking.yaml: {repo or index} pull request {pr_index} must be a mapping")
                continue
            unknown_pr_fields = sorted(set(pull_request) - {"url", "title", "state", "commit"})
            if unknown_pr_fields:
                reporter.fail(
                    f"metadata_tracking.yaml: {repo or index} pull request {pr_index} "
                    f"has unknown fields: {', '.join(unknown_pr_fields)}"
                )
            missing = [
                key
                for key in ("url", "title", "state", "commit")
                if not str(pull_request.get(key, "")).strip()
            ]
            if missing:
                reporter.fail(
                    f"metadata_tracking.yaml: {repo or index} pull request {pr_index} missing: {', '.join(missing)}"
                )
            state = str(pull_request.get("state", "")).strip()
            if state and state not in {"open", "merged", "closed"}:
                reporter.fail("metadata_tracking.yaml: pull request state must be open, merged, or closed")
            url = str(pull_request.get("url", "")).strip()
            pr_remote = parse_git_remote(url) if url else None
            if url and not explicit_url and pr_remote and pr_remote.host != "gitcode.com":
                reporter.fail(
                    "metadata_tracking.yaml: repository_url is required for non-GitCode pull requests; "
                    "set it to the actual target repository URL and preserve the real PR URL"
                )
            elif url and (not repo_is_valid or not metadata_pr_url_matches(url, repo_url)):
                reporter.fail(
                    "metadata_tracking.yaml: pull request url must be credential-free HTTPS, "
                    "match its repository host and port, and stay within its repository path boundary"
                )
            commit = str(pull_request.get("commit", "")).strip()
            if commit and not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
                reporter.fail("metadata_tracking.yaml: pull request commit must be a full 40-digit hex SHA")
            elif (
                required
                and commit
                and current_entry
                and current_head is None
            ):
                reporter.fail("metadata_tracking.yaml: unable to resolve current repository HEAD")
            elif (
                required
                and commit
                and current_entry
                and current_head is not None
                and commit.lower() != current_head
            ):
                reporter.fail(
                    "metadata_tracking.yaml: current repository pull request commit "
                    "must match git rev-parse HEAD"
                )

        issues = entry.get("issues", [])
        if not isinstance(issues, list):
            reporter.fail(f"metadata_tracking.yaml: {repo or index} issues must be a list")
            issues = []
        if entry_host != "gitcode.com" and issues:
            reporter.fail("metadata_tracking.yaml: non-GitCode current repository cannot use GitCode issues; "
                          "omit issues or use an empty list")
        issue_ids: set[str] = set()
        for issue_index, issue in enumerate(issues, start=1):
            if not isinstance(issue, dict):
                reporter.fail(f"metadata_tracking.yaml: {repo or index} issue {issue_index} must be a mapping")
                continue
            unknown_issue_fields = sorted(
                set(issue) - {"issue", "url", "title", "type", "state", "closed_at"}
            )
            if unknown_issue_fields:
                reporter.fail(
                    f"metadata_tracking.yaml: {repo or index} issue {issue_index} "
                    f"has unknown fields: {', '.join(unknown_issue_fields)}"
                )
            missing = [
                key
                for key in ("issue", "url", "title", "type", "state")
                if not str(issue.get(key, "")).strip()
            ]
            if missing:
                reporter.fail(
                    f"metadata_tracking.yaml: {repo or index} issue {issue_index} "
                    f"missing: {', '.join(missing)}"
                )
            issue_id = str(issue.get("issue", "")).strip()
            if issue_id and not issue_id.isdigit():
                reporter.fail("metadata_tracking.yaml: issue must contain digits only")
            elif issue_id in issue_ids:
                reporter.fail(f"metadata_tracking.yaml: duplicate issue entry: {issue_id}")
            elif issue_id:
                issue_ids.add(issue_id)
            issue_type = str(issue.get("type", "")).strip()
            if issue_type and issue_type not in {"requirement", "bug", "task", "epic"}:
                reporter.fail("metadata_tracking.yaml: issue type must be requirement, bug, task, or epic")
            state = str(issue.get("state", "")).strip()
            if state and state not in {"open", "closed"}:
                reporter.fail("metadata_tracking.yaml: issue state must be open or closed")
            closed_at = str(issue.get("closed_at", "")).strip()
            if closed_at:
                try:
                    date.fromisoformat(closed_at)
                except ValueError:
                    reporter.fail("metadata_tracking.yaml: closed_at must be a valid YYYY-MM-DD date")
                if state != "closed":
                    reporter.fail(
                        "metadata_tracking.yaml: closed_at is only valid when issue state is closed"
                    )
            url = str(issue.get("url", "")).strip()
            expected_issue_url = rf"https://gitcode\.com/{re.escape(repo)}/issues/\d+"
            if url and (not repo_is_valid or not re.fullmatch(expected_issue_url, url)):
                reporter.fail("metadata_tracking.yaml: issue url must match its GitCode repository")
            elif url and issue_id and url.rsplit("/", 1)[-1] != issue_id:
                reporter.fail("metadata_tracking.yaml: issue id must match its GitCode URL")

    if origin and not current_identity:
        reporter.fail(
            "metadata_tracking.yaml: current Git origin must be a supported repository URL (HTTPS/SSH with namespace/repository)"
        )
    elif current_identity and not current_seen:
        reporter.fail(
            "metadata_tracking.yaml: repos must include the current Git origin repository "
            f"{current_identity}"
        )
    elif not current_identity and change_dir.parent.name not in {
        repo.rsplit("/", 1)[-1] for repo in repository_names
    }:
        reporter.fail("metadata_tracking.yaml: repos must include the current business repository")
    elif reporter.failed == initial_failures:
        reporter.pass_("metadata_tracking.yaml matches the design-docs submission contract")


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


def validate_effective_rules(change_dir: Path, artifacts: dict, reporter: Reporter) -> None:
    """Enforce profile additions and explicitly machine-readable conditions."""
    for name, artifact in artifacts.items():
        path = change_dir / str(artifact["file"])
        if not path.is_file():
            continue
        text = read_text(path)
        stories = section_text(text, "用户故事或场景")
        entries = re.findall(
            r"^[ \t]*[-*][ \t]+\*\*AC-(?:DFX\.[0-9]+|[0-9]+(?:\.[0-9]+)?):\*\*"
            r"[^\n]*(?:\n[ \t]{2,}\S[^\n]*)*", _visible_markdown(stories), re.M)
        for dependency in artifact.get("requires", []):
            if dependency in artifacts and not (change_dir / str(artifacts[dependency]["file"])).is_file():
                reporter.fail(f"{path.name}: missing dependency {dependency}")
        for dimension in artifact.get("dimensions", []):
            label = DIMENSIONS.get(dimension)
            if not label:
                reporter.fail(f"unknown profile dimension: {dimension}")
            # required_dimensions selects dimensions for explicit assessment;
            # it cannot assert that every change in a subsystem involves them.
            # The complete eight-dimension table is validated once in main.
        for category in artifact.get("ac_categories", []):
            if not any(category in entry for entry in entries):
                reporter.fail(f"profile AC category missing from user stories: {category}")
        for prohibition in artifact.get("prohibitions", []):
            if prohibition not in section_text(text, "禁止项"):
                reporter.fail(f"profile prohibition missing: {prohibition}")


def conditional_section_exemptions(text: str) -> dict[str, str]:
    """Accept standalone, named declarations outside examples/template comments."""
    reasons: dict[str, tuple[str, str]] = {}

    def replace_comment(match: re.Match[str]) -> str:
        declaration = re.fullmatch(
            r"<!--[ \t]*不涉及[：:][ \t]*([^;；\n]+)[;；][ \t]*理由[：:][ \t]*([^\n]*?)[ \t]*-->",
            match[0],
        )
        if not declaration:
            return match[0]
        section, reason = (value.strip() for value in declaration.groups())
        if not meaningful(reason) or ARCHIVE_MARKER_RE.search(reason) or ANGLE_PLACEHOLDER_RE.search(reason):
            return match[0]
        marker = f"ODK_CONDITIONAL_EXEMPTION_{len(reasons)}"
        reasons[marker] = (section, reason)
        return marker

    marked = re.sub(r"<!--[\s\S]*?-->", replace_comment, text)
    visible = set(line.strip() for line in _visible_markdown(marked).splitlines())
    declarations: dict[str, list[str]] = {}
    for marker, (section, reason) in reasons.items():
        if marker in visible:
            declarations.setdefault(section, []).append(reason)
    return {section: values[0] for section, values in declarations.items() if len(values) == 1}


def _api_contract_version_finding(
    declared: dict[str, str | None], required: str
) -> str:
    lines = [
        "API contract version chain is inconsistent",
        "",
        "| Artifact | Declared | Required |",
        "|---|---:|---:|",
    ]
    for artifact, value in declared.items():
        lines.append(f"| {artifact} | {value or 'missing'} | {required} |")
    lines.extend(
        [
            "",
            "Reason:",
            f"This change contains a mixed API contract chain. ODK 0.15.0 only "
            f"accepts API changes generated with API contract version {required}.",
            "",
            "Action:",
            "Do not manually change the version number.",
            "Restart the full flow from proposal:",
            "",
            "  proposal -> spec -> design -> plan -> implement -> validate",
            "",
            "Migration guide:",
            str(CONTRACT_PATH.parent / "skill-guides/spec/api-metadata-migration.md"),
        ]
    )
    return "\n".join(lines)


def validate_api_contract_version_chain(
    change_dir: Path,
    reporter: Reporter,
    phase: str | None,
) -> None:
    """Require spec/metadata/design/plan API contract versions to agree."""

    proposal_path = change_dir / "proposal.md"
    if not proposal_path.is_file():
        return
    if api_sdk_involvement(_visible_markdown(read_text(proposal_path))) != "是":
        return

    metadata_files = [
        name for name in API_METADATA_FILES if (change_dir / name).is_file()
    ]
    declared: dict[str, str | None] = {}
    metadata_versions: set[str] = set()
    for name in metadata_files:
        try:
            metadata = parse_api_spec(change_dir / name)
        except (OSError, UnicodeError, ValueError) as error:
            declared[name] = f"parse error: {error}"
            continue
        value = str(metadata.get("apiContractVersion") or "").strip()
        declared[name] = value or None
        if value:
            metadata_versions.add(value)

    patterns = {
        "spec.md": re.compile(r"\|\s*API 契约版本\s*\|\s*([^|]+?)\s*\|"),
        # Match the version token only. The design template keeps an inline
        # HTML instruction after this value; that guidance is not part of the
        # contract version and must not enter the version-chain comparison.
        "design.md": re.compile(
            r"\*\*API 契约版本：\*\*\s*([0-9][A-Za-z0-9._+-]*)"
        ),
        "execution-plan.md": re.compile(
            r"\|\s*API Contract Version\s*\|\s*([^|]+?)\s*\|"
        ),
    }

    # Default validate, archive, and design-docs submission are the final gate:
    # every available API-contract artifact must be checked. Earlier phase runs
    # only require artifacts already present in the effective contract.
    if phase == "design":
        required_files = ["spec.md", "design.md"]
    elif phase == "plan":
        required_files = ["spec.md", "design.md", "execution-plan.md"]
    else:
        required_files = [
            name
            for name in ("spec.md", "design.md", "execution-plan.md")
            if (change_dir / name).is_file()
        ]
        if not required_files:
            required_files = ["spec.md"]

    for file_name in required_files:
        path = change_dir / file_name
        if not path.is_file():
            declared[file_name] = None
            continue
        match = patterns[file_name].search(_visible_markdown(read_text(path)))
        value = match.group(1).strip() if match else ""
        declared[file_name] = value or None
        if value:
            metadata_versions.add(value)

    valid = all(
        value == API_CONTRACT_VERSION for value in declared.values()
    )
    if not valid:
        reporter.fail(_api_contract_version_finding(declared, API_CONTRACT_VERSION))
    else:
        reporter.pass_(
            "API contract version chain is consistent across available phase artifacts"
        )


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
        text = read_text(path)
        exemptions = conditional_section_exemptions(text)

        required = artifacts[name].get("required_sections", [])
        conditions = artifacts[name].get("conditions", {})
        substantive = set(artifacts[name].get("profile_sections", [])) | {
            title for title, rule in conditions.items() if rule.get("active")
        }
        for section in required:  # type: ignore[assignment]
            try:
                body = require_unique_section(text, str(section))
            except ValueError as error:
                reporter.fail_once(f"{file_name}: {error}")
                continue
            if body is not None:
                if section in substantive and not meaningful(body):
                    reporter.fail(f"{file_name}: required section empty: {section}")
                else:
                    reporter.pass_(f"{file_name}: required section present: {section}")
            else:
                reporter.fail(f"{file_name}: required section missing: {section}")

        conditional = artifacts[name].get("conditional_sections", [])
        for section in conditional:  # type: ignore[assignment]
            if section in required:
                continue  # One authoritative diagnostic for active/profile sections.
            try:
                body = require_unique_section(text, str(section))
            except ValueError as error:
                reporter.fail_once(f"{file_name}: {error}")
                continue
            if section in RESOURCE_SECTIONS.values():
                continue  # trigger-aware checks live in validate_resource_constraints
            if name == "execution-plan" and section == "问题闭环" and body is None:
                continue  # Absence is the supported no-finding state; not an unresolved condition.
            if body is not None:
                reporter.pass_(f"{file_name}: conditional section present: {section}")
            else:
                if section in exemptions:
                    dimension = {"安全基础检查": "安全/权限", "国际化依赖分析": I18N_TRIGGER_DIMENSION}.get(section)
                    proposal_path = change_dir / "proposal.md"
                    triggered = (dimension and proposal_path.is_file()
                                 and parse_eight_dim_involvement(read_text(proposal_path), dimension) == "是")
                    if triggered:
                        reporter.fail(f"{file_name}: conditional exclusion conflicts with active {dimension}: {section}")
                    else:
                        reporter.pass_(f"{file_name}: conditional section not applicable: {section}; reason: {exemptions[section]}")
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
        for section in required:  # type: ignore[assignment]
            try:
                body = require_unique_section(text, str(section))
            except ValueError as error:
                reporter.fail_once(f"{file_name}: {error}")
                continue
            if body is not None:
                substantive = section in data.get("profile_sections", []) or data.get("conditions", {}).get(section, {}).get("active")
                if substantive and not meaningful(body):
                    reporter.fail(f"{file_name} (present optional): required section empty: {section}")
                    continue
                reporter.pass_(f"{file_name} (present optional): section present: {section}")
                # Also check that section's tables have non-placeholder data rows
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


def validate_ac_ids(change_dir: Path, reporter: Reporter, archive_mode: bool) -> None:
    """Compatibility entry point; the shared format check also validates mappings."""
    validate_ac_id_format(change_dir, reporter, archive=archive_mode)


def validate_spec_verification(change_dir: Path, reporter: Reporter) -> None:
    """Validate the spec's own AC contract without requiring a future plan."""
    spec_path = change_dir / "spec.md"
    if not spec_path.is_file():
        return

    print("\nLevel C: Spec Verification")
    spec = read_text(spec_path)
    spec_acs = defined_ac_ids(spec)
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


def validate_plan_traceability(change_dir: Path, reporter: Reporter) -> None:
    """Validate mappings from an existing plan to the spec's defined ACs."""
    spec_path = change_dir / "spec.md"
    plan_path = change_dir / "execution-plan.md"
    if not spec_path.is_file() or not plan_path.is_file():
        return
    spec_acs = defined_ac_ids(read_text(spec_path))
    if not spec_acs:
        return  # The spec gate already reports the missing definitions.
    print("\nLevel C: Traceability")
    plan = read_text(plan_path)
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


def validate_traceability(change_dir: Path, reporter: Reporter) -> None:
    """Compatibility entry point for callers requesting both traceability gates."""
    validate_spec_verification(change_dir, reporter)
    validate_plan_traceability(change_dir, reporter)


def _dfx_main_table_pairs(design: str) -> list[tuple[str, str]]:
    """Return (分析对象, 故障模式) pairs from DFX main-table data rows."""
    dfx_section = section_text(design, "DFX 设计")
    if not dfx_section:
        return []
    fault_subsection = section_text(dfx_section, "DFX 故障模式分析")
    if not fault_subsection:
        return []
    visible = _visible_markdown(fault_subsection)
    rows = require_unique_table_with_columns(visible, _DFX_FAULT_COLUMNS) or []
    return [
        (row.get("分析对象", "").strip(), row.get("故障模式", "").strip())
        for row in rows
        if meaningful(row.get("分析对象", ""))
    ]


def _strip_subsection(section: str, title: str) -> str:
    """Remove one titled subsection (heading to next same-or-higher level) from section text."""
    out: list[str] = []
    skipping = False
    level = 0
    for line in section.splitlines():
        match = atx_heading(line)
        if match:
            heading_level, heading_title = match
            if skipping and heading_level <= level:
                skipping = False
            if heading_title == title:
                skipping = True
                level = heading_level
        if not skipping:
            out.append(line)
    return "\n".join(out)


def _dfx_ad_entries(design: str) -> tuple[dict[str, tuple[str, str]], list[str]]:
    """AD entries defined by AD layer tables under ## DFX 设计 (disposition
    subsection excluded), located via the unified Markdown table parser so
    indented and border-less tables are handled identically.

    Returns ({AD id: (对象列值, 故障模式值)}, duplicate ids with conflicting content)."""
    dfx_section = section_text(design, "DFX 设计")
    if not dfx_section:
        return {}, []
    visible = _strip_subsection(dfx_section, "DFX 故障模式处置")
    entries: dict[str, tuple[str, str]] = {}
    duplicates: list[str] = []
    for header, rows in parsed_markdown_tables(visible):
        if len(header) < 3 or header[0].strip() != "编号" or "故障模式" not in header:
            continue
        object_column = header[1]  # 结构元素（标准 12 列）或 分析对象（委托回填布局）
        for row in rows:
            rid = row.get("编号", "").strip()
            if not _DFX_AD_ID_RE.match(rid):
                continue
            pair = (row.get(object_column, "").strip(), row.get("故障模式", "").strip())
            if rid in entries:
                if entries[rid] != pair:
                    duplicates.append(rid)
            else:
                entries[rid] = pair
    return entries, sorted(set(duplicates))


GOAL_ID_RE = re.compile(r"\bG-(\d+)\b")
GOAL_DEF_RE = re.compile(r"^\s*[-*]\s+\*\*G-(\d+):\*\*", re.MULTILINE)

# US_GOAL_RE: match **来源目标：** only at the start of a line (after optional whitespace),
# and capture only the rest of THAT line (no cross-line capture via \s).
# [^\S\n] matches spaces and tabs but NOT newlines, keeping the value on one line.
US_GOAL_RE = re.compile(r"^[^\S\n]*\*\*来源目标[：:]\*\*[^\S\n]*([^\n]+)", re.MULTILINE)


def _strip_code_spans(text: str) -> str:
    """Strip CommonMark code spans using proper equal-length backtick fence matching.

    A code span is opened by a backtick string of length N and closed by the
    next backtick string of exactly the same length.  Content may span lines.
    This correctly handles: `x`, ``x`y`z``, `` `x` ``, `` x``y ``z`` ``.

    Reference: CommonMark spec §6.1
    https://spec.commonmark.org/0.31.2/#code-spans
    """
    result: list[str] = []
    i = 0
    while i < len(text):
        if text[i] != "`":
            result.append(text[i])
            i += 1
            continue
        # Count the opening backtick run
        j = i
        while j < len(text) and text[j] == "`":
            j += 1
        fence_len = j - i
        # Search for the closing run of the same length (no longer run in between)
        k = j
        found = False
        while k < len(text):
            if text[k] == "`":
                # Count this backtick run
                m = k
                while m < len(text) and text[m] == "`":
                    m += 1
                run_len = m - k
                if run_len == fence_len:
                    # Matched: replace the whole span with empty string
                    result.append("")
                    i = m
                    found = True
                    break
                else:
                    # Different length — skip this run and continue
                    k = m
            else:
                k += 1
        if not found:
            # No closing fence found — treat backticks as literal
            result.append(text[i:j])
            i = j
    return "".join(result)


def _extract_goal_refs(
    us_text: str,
    defined_goals: set[str],
    covered_goals: set[str],
    invalid_refs: list[str],
) -> None:
    """Parse 来源目标 fields from one US section.

    Processes the text line by line so that:
    1. Indented code blocks (4-space / tab prefix) are skipped entirely —
       their content never participates in field matching.
    2. Each line is stripped of inline code spans INDEPENDENTLY before
       field detection, so cross-paragraph backtick pairing cannot delete
       real fields or manufacture fake ones.
    3. A field is recognised only when **来源目标：** appears at the start
       of the stripped line (after optional non-newline whitespace).  If
       stripping inline code reveals a bare **来源目标：** that was previously
       hidden behind a code-span prefix, the original line is also checked:
       the field must already be at line-start in the ORIGINAL text too.
    """
    US_FIELD_RE = re.compile(r"^[^\S\n]*\*\*来源目标[：:]\*\*[^\S\n]*([^\n]+)")
    in_fence = False
    fence_char: str = ""
    fence_len: int = 0

    for line in us_text.splitlines():
        # Track fenced code blocks (``` or ~~~)
        stripped = line.strip()
        if not in_fence:
            fence_m = re.match(r"^(`{3,}|~{3,})", stripped)
            if fence_m:
                in_fence = True
                fence_char = fence_m.group(1)[0]
                fence_len = len(fence_m.group(1))
                continue
        else:
            close_m = re.match(rf"^[^\S\n]*{re.escape(fence_char)}{{{fence_len},}}[^\S\n]*$", line)
            if close_m:
                in_fence = False
            continue  # inside fence — skip

        # Skip CommonMark indented code blocks (4 spaces or 1 tab)
        if line.startswith("    ") or line.startswith("\t"):
            continue

        # Check field existence in ORIGINAL line first (prevents code-removal
        # from manufacturing a field that wasn't there before stripping).
        # The field marker **来源目标：** must already appear at the start of
        # the line in the original text — not revealed only after code removal.
        if not US_FIELD_RE.match(line):
            continue

        # Now strip inline code spans on this line only, then match the field
        clean_line = _strip_code_spans(line)
        m = US_FIELD_RE.match(clean_line)
        if not m:
            continue

        raw_value = m.group(1)
        for ref in GOAL_ID_RE.findall(raw_value):
            if ref in defined_goals:
                covered_goals.add(ref)
            else:
                invalid_refs.append(f"G-{ref}")
_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)(?:\s+#+)?\s*$", re.MULTILINE)


def _has_visible_heading(text: str, heading_text: str) -> bool:
    """Return True only when heading_text appears as a real ATX heading in visible markdown."""
    visible = _visible_markdown(text)
    for line in visible.splitlines():
        parsed = atx_heading(line)
        if parsed is not None and heading_text in parsed[1]:
            return True
    return False


def validate_goal_us_coverage(change_dir: Path, reporter: Reporter) -> None:
    """Level C: every proposal goal (G-N) must be covered by at least one spec US.

    Triggered only when proposal.md has a visible '用户场景与业务触发' heading
    (skips pure-internal refactors).  Old deliverables without G-N IDs are warned
    but not hard-failed so that existing archives are not broken.
    """
    proposal_path = change_dir / "proposal.md"
    spec_path = change_dir / "spec.md"
    if not proposal_path.is_file() or not spec_path.is_file():
        return

    proposal_raw = read_text(proposal_path)

    # P2-2 fix: use visible heading detection, not plain string contains
    if not _has_visible_heading(proposal_raw, "用户场景与业务触发"):
        return

    print("\nLevel C: Goal → US coverage")

    # Parse visible text only — strips HTML comments and fenced code blocks
    proposal_visible = _visible_markdown(proposal_raw)

    # P2-2 fix: detect duplicate ## 目标 sections (structural error, not old doc)
    goal_sections = section_texts(proposal_visible, "目标")
    if len(goal_sections) > 1:
        reporter.fail(
            f"proposal.md has {len(goal_sections)} '## 目标' sections — expected exactly one; "
            "fix the duplicate headings before goal→US coverage can be checked"
        )
        return
    goal_section = goal_sections[0] if goal_sections else ""

    # P2-2 fix: G-? placeholder means migration is in progress — block archive
    #  word boundary does not work around '?' (non-word char), so match literally
    if re.search(r"G-\?", goal_section):
        reporter.fail(
            "proposal.md 目标 section contains 'G-?' placeholder — "
            "replace with real G-N numbered goals before archiving"
        )
        return

    defined_goals_list = GOAL_DEF_RE.findall(goal_section)

    # P1 fix: no G-N IDs → warn only (backwards compatibility for pre-feature deliverables)
    if not defined_goals_list:
        reporter.warn(
            "proposal.md 目标 section has no G-N goal IDs — goal→US coverage not checked. "
            "Add '- **G-1:** …' numbered entries to enable traceability validation."
        )
        return

    # P2-3 fix: check for duplicate goal IDs
    seen: set[str] = set()
    duplicates: list[str] = []
    for g in defined_goals_list:
        if g in seen:
            duplicates.append(f"G-{g}")
        seen.add(g)
    if duplicates:
        reporter.fail(
            "proposal.md 目标 section has duplicate goal IDs: " + ", ".join(duplicates)
        )
        return
    defined_goals = seen
    reporter.pass_(
        f"proposal.md defines {len(defined_goals)} unique goal ids: "
        + ", ".join(f"G-{g}" for g in sorted(defined_goals, key=int))
    )

    # P2-1 fix: scan visible spec text only
    spec_visible = _visible_markdown(read_text(spec_path))

    # P1 fix: only extract 来源目标 from legitimate ### US-<digits> sections.
    # Reject fake US headings (e.g. '### US-99' inserted under ## Notes) by
    # requiring a real US section under the spec's '## 用户故事或场景' heading.
    us_scope = section_text(spec_visible, "用户故事或场景")
    if not us_scope:
        reporter.fail("spec.md missing '## 用户故事或场景' section — goal→US coverage cannot be checked")
        return

    # P2-2 fix: check spec 来源目标 field VALUES for G-? placeholders too.
    # Only inspect values matched by US_GOAL_RE (real 来源目标 fields), not the
    # whole US section — a literal "G-?" in an AC input example must not trigger.
    # P2-2 fix: check spec 来源目标 field VALUES for G-? placeholders.
    # Use the same line-by-line approach as _extract_goal_refs so that
    # indented code blocks and inline-code-prefix removal cannot manufacture
    # or suppress placeholder detections.
    _placeholder_found = False
    _US_FIELD_RE_PLACEHOLDER = re.compile(r"^[^\S\n]*\*\*来源目标[：:]\*\*[^\S\n]*([^\n]+)")
    for _line in us_scope.splitlines():
        if _line.startswith("    ") or _line.startswith("\t"):
            continue
        if "来源目标" not in _line:
            continue
        _clean = _strip_code_spans(_line)
        _m = _US_FIELD_RE_PLACEHOLDER.match(_clean)
        if _m and "G-?" in _m.group(1):
            _placeholder_found = True
            break
    if _placeholder_found:
        reporter.fail(
            "spec.md US 来源目标 contains 'G-?' placeholder — "
            "replace with real G-N ids from proposal.md before archiving"
        )
        return

    covered_goals: set[str] = set()
    invalid_refs: list[str] = []
    # Split the US scope into US-<digits> sub-sections; only ### headings whose
    # title matches US-<digits> (or US-DFX) are accepted as real user stories.
    US_TITLE_RE = re.compile(r"^US-(\d+)(?:\b|:)", re.MULTILINE)
    us_lines = us_scope.splitlines()
    current_us: list[str] | None = None
    for line in us_lines:
        h = atx_heading(line)
        if h and h[0] == 3:
            title = h[1]
            if US_TITLE_RE.match(title) or title.startswith("US-DFX"):
                if current_us is not None:
                    _extract_goal_refs("\n".join(current_us), defined_goals, covered_goals, invalid_refs)
                current_us = [line]
            else:
                # non-US ### heading ends the current US section
                if current_us is not None:
                    _extract_goal_refs("\n".join(current_us), defined_goals, covered_goals, invalid_refs)
                    current_us = None
        elif current_us is not None:
            current_us.append(line)
    if current_us is not None:
        _extract_goal_refs("\n".join(current_us), defined_goals, covered_goals, invalid_refs)

    # P2-3 fix: reject references to undefined goals
    if invalid_refs:
        reporter.fail(
            "spec.md references goal IDs not defined in proposal.md: "
            + ", ".join(sorted(set(invalid_refs)))
        )
        return

    missing = sorted(defined_goals - covered_goals, key=int)
    if missing:
        reporter.fail(
            "spec.md US entries do not cover proposal goals: "
            + ", ".join(f"G-{g}" for g in missing)
            + " — add '**来源目标：** G-N' to the relevant US sections"
        )
    else:
        reporter.pass_(f"spec.md US entries cover all {len(defined_goals)} proposal goal ids")


def validated_dfx_section(design: str, reporter: Reporter) -> str | None:
    """Fail closed on ambiguous DFX sections or main tables before either gate."""
    try:
        section = require_unique_section(design, "DFX 设计")
        if section is not None:
            for title in ("DFX 故障模式分析", "DFX 故障模式处置", "DFX 约束清单"):
                require_unique_section(section, title)
            fault_section = require_unique_section(section, "DFX 故障模式分析")
            if fault_section is not None:
                try:
                    require_unique_table_with_columns(fault_section, _DFX_FAULT_COLUMNS)
                except ValueError as error:
                    raise ValueError(f"DFX 故障模式分析: {error}") from error
        return section
    except ValueError as error:
        reporter.fail_once(f"design.md: {error}")
        return None


def validate_dfx_ac_gate(change_dir: Path, reporter: Reporter, archive_mode: bool) -> None:
    """Level C3: every DFX fault mode (main-table hit or AD entry) must be dispositioned,
    AC-linked dispositions must reference spec-defined ACs, and archive requires those
    ACs to be traced Pass in execution-plan.md."""
    design_path = change_dir / "design.md"
    if not design_path.is_file():
        return

    design = read_text(design_path)
    dfx_section = validated_dfx_section(design, reporter)
    if dfx_section is None:
        return

    main_pairs = _dfx_main_table_pairs(design)
    ad_entries, ad_duplicates = _dfx_ad_entries(design)
    ad_ids = set(ad_entries)
    if not main_pairs and not ad_ids:
        # 不涉及 branch (or missing subsection — reported by Level C2): gate silent.
        return

    print("\nLevel C3: DFX Fault-Mode → AC Gate")

    disposition_sub = section_text(dfx_section, "DFX 故障模式处置")
    if not disposition_sub:
        draft_warn_archive_fail(
            reporter,
            archive_mode,
            "design.md: DFX fault modes found (main-table hits or AD entries) but "
            "'### DFX 故障模式处置' missing — disposition every entry as "
            "新增 AC / 复用 AC / 现有控制覆盖 / 本变更不触及",
        )
        return

    if not table_has_columns(disposition_sub, _DFX_DISPOSITION_COLUMNS):
        missing = [
            c for c in _DFX_DISPOSITION_COLUMNS
            if not table_has_columns(disposition_sub, [c])
        ]
        reporter.fail(
            "design.md: DFX 故障模式处置 table missing required columns: " + ", ".join(missing)
        )
        return

    rows = table_with_columns(disposition_sub, _DFX_DISPOSITION_COLUMNS)

    issues: list[str] = []
    seen_ids: set[str] = set()
    disposed_pairs: set[tuple[str, str]] = set()
    disposed_ads: set[str] = set()
    linked_acs: set[str] = set()
    design_constraint_tasks: set[str] = set()

    for row in rows:
        if not any(meaningful(str(value)) for value in row.values()):
            continue  # template placeholder row
        rid = row.get("编号", "").strip()
        obj = row.get("分析对象", "").strip()
        mode = row.get("故障模式", "").strip()
        disposition = row.get("处置", "").strip()
        ac_cell = row.get("关联 AC", "").strip()
        evidence = row.get("验证方式/证据", "").strip()

        if not (_DFX_FM_ID_RE.match(rid) or _DFX_AD_ID_RE.match(rid)):
            issues.append(f"{rid or '<empty>'}: 编号 must be FM-n (main-table row) or AD-n (derived entry)")
            continue
        if rid in seen_ids:
            issues.append(f"{rid}: duplicate 编号")
            continue
        seen_ids.add(rid)
        if disposition not in _DFX_DISPOSITIONS:
            issues.append(f"{rid}: invalid 处置 '{disposition}' (expected one of {'/'.join(sorted(_DFX_DISPOSITIONS))})")
            continue
        if not meaningful(evidence):
            issues.append(f"{rid}: 验证方式/证据 empty (fault-injection/error-path method, file:line, or reason required)")
        if disposition in _DFX_AC_DISPOSITIONS:
            acs = sorted_ids(set(AC_RE.findall(ac_cell)))
            if not acs:
                issues.append(f"{rid}: 处置={disposition} requires 关联 AC")
            linked_acs.update(acs)
        if disposition == _DFX_DESIGN_CONSTRAINT_DISPOSITION:
            # Internal control measures land as design decisions/constraints plus a
            # traced Task with verification evidence — not as a new spec AC.
            tasks = sorted(set(TASK_RE.findall(evidence)))
            if not tasks:
                issues.append(f"{rid}: 处置=纳入设计约束 requires a 关联 TASK id in 验证方式/证据")
            if not _DFX_CONSTRAINT_REF_RE.search(evidence):
                issues.append(f"{rid}: 处置=纳入设计约束 requires a design decision/constraint reference (e.g. D-xx / 约束 / 不变量)")
            design_constraint_tasks.update(tasks)
        if _DFX_FM_ID_RE.match(rid):
            if not meaningful(obj) or not meaningful(mode):
                issues.append(f"{rid}: 分析对象/故障模式 must be copied from the main table")
            else:
                disposed_pairs.add((obj, mode))
        else:
            # AD disposition must mirror the AD layer entry's object and fault mode.
            if rid in ad_entries:
                expected = ad_entries[rid]
                if not meaningful(obj) or not meaningful(mode):
                    issues.append(f"{rid}: 处置行分析对象/故障模式 must be copied from the AD layer entry")
                elif (obj, mode) != expected:
                    issues.append(
                        f"{rid}: 处置行分析对象/故障模式与 AD 条目不匹配 "
                        f"(expected {expected[0]} / {expected[1]})"
                    )
            disposed_ads.add(rid)

    if ad_duplicates:
        issues.append("AD entries with duplicate ids and conflicting content: " + ", ".join(ad_duplicates))
    for pair in main_pairs:
        if pair not in disposed_pairs:
            issues.append(f"main-table hit not dispositioned: {pair[0]} / {pair[1]}")
    for obj, mode in sorted(disposed_pairs - set(main_pairs)):
        issues.append(f"disposition row not found in main table: {obj} / {mode}")
    for ad in sorted_ids(ad_ids):
        if ad not in disposed_ads:
            issues.append(f"{ad}: AD entry not dispositioned")
    for ad in sorted_ids(disposed_ads - ad_ids):
        issues.append(f"{ad}: disposition references unknown AD entry")

    if linked_acs:
        spec_acs: set[str] = set()
        spec_path = change_dir / "spec.md"
        if spec_path.is_file():
            spec = read_text(spec_path)
            spec_acs = defined_ac_ids(spec)
        dangling = [ac for ac in sorted_ids(linked_acs) if ac not in spec_acs]
        if dangling:
            issues.append("关联 AC not defined in spec.md: " + ", ".join(dangling))

    if issues:
        reporter.fail("design.md: DFX 故障模式处置 gate: " + "; ".join(issues))
        return

    detail = f"{len(main_pairs)} hit row(s), {len(ad_ids)} AD entr(ies)"
    if linked_acs:
        detail += f", {len(linked_acs)} linked AC(s)"
    if design_constraint_tasks:
        detail += f", {len(design_constraint_tasks)} design-constraint Task(s)"
    reporter.pass_(f"DFX 故障模式处置 complete ({detail})")

    if not (archive_mode and (linked_acs or design_constraint_tasks)):
        return

    plan_path = change_dir / "execution-plan.md"
    if not plan_path.is_file():
        reporter.fail(
            "execution-plan.md missing — FM ACs/design-constraint Tasks cannot be "
            "verified for archive: "
            + ", ".join(sorted_ids(linked_acs) + sorted(design_constraint_tasks))
        )
        return
    plan = read_text(plan_path)
    ac_task = section_text(plan, "AC 到 Task 追溯")
    trace_rows = table_with_columns(ac_task, ["AC", "Task", "验证状态（Pass/Fail/Blocked）"])
    # Aggregate every trace row per AC (and per Task): one AC may span several
    # Tasks and the gate passes only when ALL of its rows are Pass (a later
    # Pass must not mask an earlier Fail/Blocked).
    statuses_by_ac: dict[str, set[str]] = {}
    statuses_by_task: dict[str, set[str]] = {}
    for trace_row in trace_rows:
        status = trace_row.get("验证状态（Pass/Fail/Blocked）", "").strip().lower()
        for ac in AC_RE.findall(trace_row.get("AC", "")):
            statuses_by_ac.setdefault(ac, set()).add(status)
        for task in TASK_RE.findall(trace_row.get("Task", "")):
            statuses_by_task.setdefault(task, set()).add(status)
    not_pass = [
        ac for ac in sorted_ids(linked_acs)
        if statuses_by_ac.get(ac) != {"pass"}
    ]
    if not_pass:
        reporter.fail(
            "FM AC not Pass in execution-plan.md AC-to-Task traceability (archive gate; "
            "all trace rows for the AC must be Pass): " + ", ".join(not_pass)
        )
    elif linked_acs:
        reporter.pass_("FM ACs all Pass in AC-to-Task traceability (archive gate)")

    constraint_not_pass = [
        task for task in sorted(design_constraint_tasks)
        if statuses_by_task.get(task) != {"pass"}
    ]
    if constraint_not_pass:
        reporter.fail(
            "设计约束 Task not Pass in execution-plan.md AC-to-Task traceability "
            "(archive gate): " + ", ".join(constraint_not_pass)
        )
    elif design_constraint_tasks:
        reporter.pass_("design-constraint Tasks all Pass in AC-to-Task traceability (archive gate)")


def validate_dfx_constraints(change_dir: Path, reporter: Reporter, archive_mode: bool) -> None:
    design_path = change_dir / "design.md"
    if not design_path.is_file():
        return

    print("\nLevel C2: DFX Fault Mode Coverage")

    design = read_text(design_path)
    dfx_section = validated_dfx_section(design, reporter)
    if dfx_section is None:
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
    required_dfx_columns = _DFX_FAULT_COLUMNS
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

    fault_rows = require_unique_table_with_columns(visible_fault_subsection, required_dfx_columns) or []

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


def validate_dfx_export_table(change_dir: Path, reporter: Reporter) -> None:
    """Structural WARN for the optional 66-column library export table.

    The export table is not an archive gate object (presence never affects
    archive decisions), but a malformed one cannot be parsed by Markdown or
    the import platform — flag structure drift as a Draft WARN."""
    design_path = change_dir / "design.md"
    if not design_path.is_file():
        return
    design = read_text(design_path)
    dfx_section = section_text(design, "DFX 设计")
    if not dfx_section:
        return
    export_sub = section_text(dfx_section, "故障模式库导出表格")
    if not export_sub:
        return  # absent export table is a valid state

    print("\nLevel C2: Library Export Table (structure)")
    lines = [
        line for line in _visible_markdown(export_sub).splitlines()
        if "|" in line
    ]
    if not lines:
        reporter.warn("design.md: ### 故障模式库导出表格 exists but contains no table")
        return

    issues: list[str] = []
    header = split_table_row(lines[0])
    if len(lines) < 2:
        issues.append("table has no separator row (header only)")
        separator: list[str] = []
    else:
        separator = split_table_row(lines[1])
        if not is_separator_row(separator):
            issues.append("second table row is not a valid separator row — not a parseable Markdown table")
        elif len(separator) != len(header):
            issues.append(
                f"separator row has {len(separator)} columns but header has {len(header)} — table cannot be parsed"
            )
    data_lines = lines[2:] if len(lines) >= 2 else []
    for index, line in enumerate(data_lines, start=3):
        cells = split_table_row(line)
        if is_separator_row(cells):
            continue
        if len(cells) != len(header):
            issues.append(f"data row {index} has {len(cells)} columns (header has {len(header)})")
    if len(header) != 66:
        issues.append(f"expected 66 columns, found {len(header)} (empty columns must be kept as placeholders)")
    elif header != _DFX_EXPORT_COLUMNS:
        missing = [c for c in _DFX_EXPORT_COLUMNS if c not in header]
        extra = [c for c in header if c not in _DFX_EXPORT_COLUMNS]
        detail = []
        if missing:
            detail.append("missing: " + ", ".join(missing[:8]) + ("…" if len(missing) > 8 else ""))
        if extra:
            detail.append("non-contract columns: " + ", ".join(extra[:8]) + ("…" if len(extra) > 8 else ""))
        issues.append("column names/order deviate from the 66-column template (" + "; ".join(detail) + ")")
    if issues:
        reporter.warn("design.md: 故障模式库导出表格 structure: " + "; ".join(issues))
    else:
        reporter.pass_("library export table is a well-formed 66-column table")


def validate_dfx_ad_library_basis(change_dir: Path, reporter: Reporter) -> None:
    """Draft WARN: every AD entry under ## DFX 设计 must carry a library-basis
    annotation (（库依据：…） or （无库依据…）) so derived entries are auditable
    against the generic fault-mode library. Uses the unified table parser so
    indented/border-less AD tables are covered identically."""
    design_path = change_dir / "design.md"
    if not design_path.is_file():
        return
    design = read_text(design_path)
    dfx_section = section_text(design, "DFX 设计")
    if not dfx_section:
        return
    ad_entries, _ = _dfx_ad_entries(design)
    if not ad_entries:
        return
    visible = _visible_markdown(_strip_subsection(dfx_section, "DFX 故障模式处置"))
    missing = []
    for header, rows in parsed_markdown_tables(visible):
        if len(header) < 3 or header[0].strip() != "编号" or "故障原因" not in header:
            continue
        for row in rows:
            rid = row.get("编号", "").strip()
            if _DFX_AD_ID_RE.match(rid) and "库依据" not in row.get("故障原因", ""):
                missing.append(rid)
    if not missing and not any(
        "故障原因" in header for header, _ in parsed_markdown_tables(visible)
    ):
        return  # no AD table with a 故障原因 column found; nothing to annotate

    print("\nLevel C2: AD Library Basis (annotation)")
    if missing:
        reporter.warn(
            "design.md: AD 分层表 rows without library-basis annotation "
            "(append 库依据：<库编号> or 无库依据：本次特有推导 to 故障原因): "
            + ", ".join(sorted(set(missing)))
        )
    else:
        reporter.pass_("AD rows all carry library-basis annotations")


_SKIP_REVIEW_MARKER = "Task review: 不适用（逐步实现模式：免三席审查）"
_STEPWISE_MODE = "逐步实现"


def _section_text(body: str, heading: str) -> str | None:
    """Return the text of the first H2 section, or None when absent."""
    pattern = rf"^##\s+{re.escape(heading)}\s*$"
    match = re.search(pattern, body, re.MULTILINE)
    if not match:
        return None
    rest = body[match.end():]
    nxt = re.search(r"^##\s+", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def _mode_field_values(section: str, name: str, *, multiline: bool = False) -> list[str]:
    visible = _visible_markdown(section)
    matches = list(re.finditer(rf"^\*\*{re.escape(name)}：\*\*[ \t]*(.*)$", visible, re.MULTILINE))
    values = []
    for match in matches:
        value = match[1]
        if multiline:
            rest = visible[match.end():]
            next_field = re.search(r"^\*\*(?:所选模式|选择时间|模式说明)：\*\*", rest, re.MULTILINE)
            value += rest[:next_field.start()] if next_field else rest
        values.append(value.strip())
    return values


def _plan_execution_mode(body: str) -> str | None:
    """Return the confirmed 执行模式 value, or None when absent/unknown/duplicate."""
    try:
        section = require_unique_section(body, "执行模式")
    except ValueError:
        return None
    if section is None:
        return None
    matches = _mode_field_values(section, "所选模式")
    # A single marker line is the contract; zero or several lines are ambiguous
    # (a mode switch keeps its old line as an audit trail, and a copied template
    # may leave the default line behind). Taking the first match could silently
    # skip the three-seat review, so fail closed like the risk-cell prefixes.
    if len(matches) != 1:
        return None
    raw_value = matches[0].strip()
    mode_match = re.fullmatch(
        r"(多子agent检查|全自动|逐步实现)(?:\s*[（(][^()（）]*[）)])?\s*", raw_value
    )
    return mode_match.group(1) if mode_match else None


def _mode_record_errors(body: str, mode: str | None) -> list[str]:
    """Check declared mode records, leaving legacy/ambiguous-mode fallback intact."""
    if mode is None:
        return []
    section = require_unique_section(body, "执行模式") or ""
    errors = []
    times = _mode_field_values(section, "选择时间")
    valid_time = False
    if len(times) == 1:
        value = times[0].strip()
        try:
            # Require a date and time, not an ISO date-only placeholder.
            if len(value) > 10 and value[10] in {"T", "t", " "}:
                datetime.fromisoformat(value.replace("Z", "+00:00").replace("z", "+00:00"))
                valid_time = True
        except ValueError:
            pass
    if not valid_time:
        errors.append("选择时间 must contain one ISO 8601 date and time")
    notes = _mode_field_values(section, "模式说明", multiline=True)
    if len(notes) > 1 or (mode != "多子agent检查" and (len(notes) != 1 or not _mode_note_complete(notes[0]))):
        errors.append("模式说明 must contain one meaningful default-value record or skip reason")
    return errors


def _mode_note_has_placeholder(entry: str) -> bool:
    # A Markdown link label or URL is ordinary content, even if its label
    # contains a word used in named template slots.
    for match in BRACKET_PLACEHOLDER_RE.finditer(entry):
        if not re.match(r"\([^)\n]+\)", entry[match.end():]):
            return True
    return any(
        not re.fullmatch(r"<(?:https?://|mailto:)[^\s<>]+>", match[0], re.IGNORECASE)
        for match in ANGLE_PLACEHOLDER_RE.finditer(entry)
    )


def _mode_note_complete(note: str) -> bool:
    entries = 0
    lines = note.splitlines()
    for index, line in enumerate(lines):
        list_marker = re.match(r"^\s*(?:[-*+]|[0-9]{1,9}[.)])\s+", line)
        entry = (line[list_marker.end():] if list_marker else line).strip(" `*_\t")
        entry = re.sub(r"^\[[ xX]\]\s+", "", entry).strip(" `*_\t")
        if not entry or re.fullmatch(r"(?:[-*_]\s*){3,}", entry):
            continue
        # Check named template slots even when surrounded by otherwise filled text.
        if _mode_note_has_placeholder(entry):
            return False
        value = re.split(r"[：:]", entry, maxsplit=1)[-1].strip(" `*_\t")
        if not value and entry.endswith(("：", ":")):
            following = next((candidate for candidate in lines[index + 1:]
                              if candidate.strip() and not re.fullmatch(r"(?:[-*_]\s*){3,}", candidate.strip())), None)
            if following is None:
                return False
            if list_marker:
                indent = len(line.expandtabs(4)) - len(line.expandtabs(4).lstrip())
                next_indent = len(following.expandtabs(4)) - len(following.expandtabs(4).lstrip())
                if next_indent <= indent:
                    return False  # An empty leaf cannot borrow the next sibling's value.
            continue  # An introduction needs actual following content.
        if not meaningful(entry) or not meaningful(value):
            return False
        entries += 1
    return entries > 0


def _task_detail_blocks(task_details: str) -> tuple[dict[str, list[str]], list[str]]:
    """Share the archive Task-heading grammar and retain duplicate occurrences."""
    details: dict[str, list[str]] = {}
    unassigned: list[str] = []
    current_task = None
    for line in task_details.splitlines():
        heading = atx_heading(line)
        match = TASK_RE.match(heading[1]) if heading and heading[0] == 3 else None
        if match:
            current_task = match[0]
            details.setdefault(current_task, []).append("")
        elif current_task is not None:
            # Keep custom headings in this Task until the next TASK heading.
            details[current_task][-1] += line + "\n"
        else:
            unassigned.append(line)
    return details, unassigned


def _task_section(body: str, task: str) -> str | None:
    """Return the Task 详情 subsection text for an exact TASK-<n> heading."""
    try:
        section = require_unique_section(body, "Task 详情")
    except ValueError:
        return None
    if section is None:
        return None
    details, _ = _task_detail_blocks(_visible_markdown(section))
    blocks = details.get(task, [])
    return blocks[0] if len(blocks) == 1 else None


def _verification_records(value: str) -> list[str]:
    return [
        entry.strip() for entry in re.split(r"<br\s*/?>|\n+", value, flags=re.IGNORECASE)
    ]


def _marker_in_actual_result(block: str, marker: str) -> bool:
    """Require the marker in one complete, unambiguous Verification table."""
    try:
        rows = delivery_table(
            block, ["Command / Evidence", "Expected Result", "Actual Result", "Final Status"],
            preserve_breaks=True,
        )
    except ValueError:
        return False
    return any(marker in _verification_records(row["Actual Result"]) for row in rows)


def _plan_risk_rows(plan: str) -> list[dict[str, str]] | None:
    """Return Task-list rows when the plan declares a 风险等级 column.

    Only the unique ``## Task 列表`` section is inspected: scanning the whole
    document would let an earlier summary table (e.g. a 风险摘要 overview with
    every Task marked R0) shadow the authoritative task rows. Duplicate
    sections and multiple matching tables inside the section raise so the
    caller can fail closed.
    """
    body = require_unique_section(plan, "Task 列表")
    if body is None:
        return None
    return require_unique_table_with_columns(
        _visible_markdown(body), ["TASK ID", "风险等级"]
    )


def validate_task_review_gate(
    change_dir: Path, reporter: Reporter, *, archive: bool
) -> None:
    """Each R1/R2 Task needs a passing, blocking-free verdict before archive."""
    plan_path = change_dir / "execution-plan.md"
    if not plan_path.is_file():
        return
    print("\nLevel B: Task Review Gate")
    try:
        plan_body = read_text(plan_path)
        mode = _plan_execution_mode(plan_body)
        mode_errors = _mode_record_errors(plan_body, mode)
        for error in mode_errors:
            message = f"execution-plan.md execution mode record: {error}"
            if archive:
                reporter.fail(message)
            else:
                reporter.warn(message)
        rows = _plan_risk_rows(plan_body)
    except ValueError as error:
        reporter.fail(f"execution-plan.md task review gate: {error}")
        return
    if rows is None:
        reporter.warn(
            "execution-plan.md: Task 列表 has no 风险等级 column; "
            "task review gate not enforced"
        )
        return

    checked = 0
    problems = len(mode_errors)
    verdict_satisfied = 0
    marker_satisfied = 0
    stepwise = mode == _STEPWISE_MODE
    for row in rows:
        task = (row.get("TASK ID") or "").strip()
        task_match = re.fullmatch(r"TASK-(\d+)", task)
        if not task_match:
            # Traceability extracts TASK-n from surrounding text, so a cell
            # like ``TASK-1（回调）`` is still treated as a valid Task there.
            # Never skip it here; otherwise its review evidence is unchecked.
            problems += 1
            message = (
                "execution-plan.md: TASK ID must be exactly TASK-<n>, "
                f"found {task or 'missing'}"
            )
            if archive:
                reporter.fail(message)
            else:
                reporter.warn(message)
            continue
        rel = f"evidence/reviews/task-{task_match.group(1)}"
        verdict_path = change_dir / rel / "verdict.md"
        label = f"{rel}/verdict.md"

        def issue(message: str) -> None:
            nonlocal problems
            problems += 1
            if archive:
                reporter.fail(f"{label}: {message} ({task})")
            else:
                reporter.warn(f"{label}: {message} ({task})")

        risk_cell = (row.get("风险等级") or "").strip()
        # Accept exactly one level plus an optional parenthesized annotation
        # (``R2（公共接口）``). Escalation notes or alternatives such as
        # ``R1→R2``, ``R0/R2`` and ``R0.5`` stay ambiguous: taking the first
        # prefix would downgrade or even skip the review, so reject them.
        risk_match = re.fullmatch(
            r"R([0-2])(?:\s*[（(][^()（）]*[）)])?\s*", risk_cell, re.IGNORECASE
        )
        if not risk_match:
            # An empty, ambiguous or typo'd risk value must not exempt a Task
            # from review.
            problems += 1
            message = (
                f"execution-plan.md: {task} 风险等级 must be R0/R1/R2, "
                f"found {risk_cell or 'missing'}"
            )
            if archive:
                reporter.fail(message)
            else:
                reporter.warn(message)
            continue
        risk = f"R{risk_match.group(1)}"
        if risk == "R0":
            continue
        checked += 1

        def _validate_verdict_file() -> None:
            frontmatter = read_frontmatter(
                verdict_path,
                single_line_keys=("task_id", "risk", "independent", "verdict", "blocking_findings"),
            )
            if frontmatter.invalid_reason is not None:
                issue(f"invalid frontmatter ({frontmatter.invalid_reason})")
                return
            if (frontmatter.get("task_id") or "").strip() != task:
                issue(f"task_id must be {task}")
            if (frontmatter.get("risk") or "").strip().upper() != risk:
                issue(f"risk must match plan value {risk}")
            if (frontmatter.get("independent") or "").strip().lower() not in {"true", "false"}:
                issue("independent must be true or false")
            verdict = (frontmatter.get("verdict") or "").strip().upper()
            if verdict != "PASS":
                issue(f"verdict must be PASS, found {verdict or 'missing'}")
            blocking = (frontmatter.get("blocking_findings") or "").strip()
            if not re.fullmatch(r"\d+", blocking) or int(blocking) != 0:
                issue(f"blocking_findings must be 0, found {blocking or 'missing'}")
            if risk == "R2":
                for role in ("arch", "scope", "security"):
                    if not (change_dir / rel / f"{role}.md").is_file():
                        issue(f"R2 requires {rel}/{role}.md")

        if verdict_path.is_file():
            problems_before = problems
            _validate_verdict_file()
            if problems == problems_before:
                verdict_satisfied += 1
            continue

        if stepwise:
            section = _task_section(plan_body, task)
            if section is None or not _marker_in_actual_result(section, _SKIP_REVIEW_MARKER):
                problems += 1
                message = (
                    f"execution-plan.md: {task} missing 逐步实现 mode skip marker "
                    f"in Task 详情 Verification Actual Result "
                    f"(expected: {_SKIP_REVIEW_MARKER})"
                )
                if archive:
                    reporter.fail(message)
                else:
                    reporter.warn(message)
            else:
                marker_satisfied += 1
            continue

        issue("missing task review verdict")

    if checked and problems == 0:
        if marker_satisfied and verdict_satisfied:
            reporter.pass_(
                f"{verdict_satisfied} R1/R2 task verdict(s) passed and "
                f"{marker_satisfied} skipped by 逐步实现 mode marker"
            )
        elif marker_satisfied:
            reporter.pass_(f"{checked} R1/R2 task(s) skipped by 逐步实现 mode marker")
        else:
            reporter.pass_(f"{checked} R1/R2 task verdict(s) passed")


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
        # Nested task review evidence (evidence/reviews/task-<n>/) counts too.
        files = [child for child in path.rglob("*") if child.is_file()]
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
        file_markers = unresolved_section_markers(text, sections)

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
        file_markers = unresolved_section_markers(text, sections)

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
    try:
        ac_task = require_unique_section(plan, "AC 到 Task 追溯")
        rows = delivery_table(ac_task or "", ["AC", "Task", "验证状态（Pass/Fail/Blocked）"])
    except ValueError as error:
        reporter.fail(f"execution-plan.md AC-to-Task traceability archive table: {error}")
        return
    if not rows:
        reporter.fail("execution-plan.md AC-to-Task traceability table missing required archive columns")
        return

    incomplete: list[str] = []
    invalid_status: list[str] = []
    not_pass: list[str] = []
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
        elif status != "pass":
            not_pass.extend(acs)

    if incomplete:
        reporter.fail("execution-plan.md AC-to-Task traceability has archive-empty rows: " + ", ".join(sorted_ids(set(incomplete))))
    elif invalid_status:
        reporter.fail("execution-plan.md AC-to-Task traceability has invalid verification status: " + ", ".join(sorted_ids(set(invalid_status))))
    elif not_pass:
        reporter.fail("execution-plan.md AC verification not Pass: " + ", ".join(sorted_ids(set(not_pass))))
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


def delivery_table(
    text: str, columns: list[str], *, preserve_breaks: bool = False
) -> list[dict[str, str]]:
    """Read one unambiguous delivery table without silently dropping bad rows."""
    rows = require_unique_table_with_columns(text, columns, preserve_breaks=preserve_breaks)
    if rows is None:
        raise ValueError("missing table columns: " + ", ".join(columns))
    lines = _visible_markdown(text).splitlines()
    for index, line in enumerate(lines[:-1]):
        header = split_table_row(line)
        if not all(column in header for column in columns):
            continue
        if not is_separator_row(split_table_row(lines[index + 1])):
            continue
        if len(set(header)) != len(header):
            raise ValueError("duplicate table columns")
        for candidate in lines[index + 2:]:
            if "|" not in candidate:
                break
            if len(split_table_row(candidate)) != len(header):
                raise ValueError("malformed table row: " + candidate.strip())
    return rows


def validate_archive_task_completion(change_dir: Path, reporter: Reporter) -> None:
    plan_path = change_dir / "execution-plan.md"
    if not plan_path.is_file():
        return
    plan = read_text(plan_path)
    try:
        body = require_unique_section(plan, "Task 列表")
        rows = delivery_table(body or "", ["TASK ID", "状态"])
    except ValueError as error:
        reporter.fail(f"execution-plan.md Task completion: {error}")
        return
    seen: set[str] = set()
    if not rows:
        reporter.fail("execution-plan.md Task completion: empty Task list")
    for row in rows:
        task = row["TASK ID"].strip()
        if not TASK_RE.fullmatch(task):
            reporter.fail("execution-plan.md Task completion: invalid TASK ID: " + task)
        if task in seen:
            reporter.fail("execution-plan.md duplicate Task in Task 列表: " + task)
        seen.add(task)
        if row["状态"].strip().lower() not in {"done", "complete", "completed", "已完成"}:
            reporter.fail(f"execution-plan.md Task not complete: {task} ({row['状态']})")
    details = section_text(plan, "Task 详情")
    if re.search(r"^[ \t]*(?:[-*+]|[0-9]{1,9}[.)])[ \t]+\[ \](?=[ \t]|$)", details, re.MULTILINE):
        reporter.fail("execution-plan.md unchecked Steps remain in Task 详情")


def _has_archive_verification_result(value: str) -> bool:
    records = _verification_records(value)
    if _SKIP_REVIEW_MARKER in records:
        return any(meaningful(record) for record in records if record != _SKIP_REVIEW_MARKER)
    return meaningful(normalize_cell(value))


def validate_archive_actual_results(change_dir: Path, reporter: Reporter) -> None:
    plan_path = change_dir / "execution-plan.md"
    if not plan_path.is_file():
        return

    plan = read_text(plan_path)
    try:
        task_list = require_unique_section(plan, "Task 列表")
        tasks = delivery_table(task_list or "", ["TASK ID"])
    except ValueError as error:
        reporter.fail(f"execution-plan.md Task list for Verification: {error}")
        tasks = []
    try:
        task_details = require_unique_section(plan, "Task 详情") or ""
    except ValueError as error:
        reporter.fail(f"execution-plan.md Verification: {error}")
        return
    listed_tasks = {row["TASK ID"].strip() for row in tasks}
    # Keep every occurrence: set-based extraction and search() could hide a
    # second, failing detail block behind a first passing block.
    details, unassigned = _task_detail_blocks(task_details)
    missing_details = listed_tasks - details.keys()
    unknown_details = details.keys() - listed_tasks
    duplicate_details = {task for task, blocks in details.items() if len(blocks) != 1}
    if missing_details:
        reporter.fail("execution-plan.md missing Task detail sections: " + ", ".join(sorted_ids(missing_details)))
    if unknown_details:
        reporter.fail("execution-plan.md Task details not in Task 列表: " + ", ".join(sorted_ids(unknown_details)))
    for task in sorted_ids(duplicate_details):
        reporter.fail("execution-plan.md duplicate Task detail: " + task)
    missing_actual: list[str] = []
    not_pass: list[str] = []
    invalid_tables = table_has_columns("\n".join(unassigned), ["Command / Evidence", "Expected Result"])
    if invalid_tables:
        reporter.fail("execution-plan.md unassigned Verification table before first Task detail")

    for task_id, blocks in details.items():
        for detail in blocks:
            try:
                rows = delivery_table(
                    detail, ["Command / Evidence", "Expected Result", "Actual Result", "Final Status"],
                    preserve_breaks=True,
                )
            except ValueError as error:
                reporter.fail(f"execution-plan.md {task_id} Verification Final Status: {error}")
                invalid_tables = True
                continue
            if not rows or any(not _has_archive_verification_result(row["Actual Result"]) for row in rows):
                missing_actual.append(task_id)
            if any(normalize_cell(row["Final Status"]).lower() != "pass" for row in rows):
                not_pass.append(task_id)

    if missing_actual:
        reporter.fail("execution-plan.md Verification tables have empty Actual Result: " + ", ".join(missing_actual))
    if not_pass:
        reporter.fail("execution-plan.md Verification Final Status not Pass: " + ", ".join(not_pass))
    if (listed_tasks and not missing_details and not unknown_details and not duplicate_details
            and not missing_actual and not not_pass and not invalid_tables):
        reporter.pass_("execution-plan.md Verification tables have Actual Result filled")


def validate_delivery_feedback(change_dir: Path, reporter: Reporter, *, archive: bool) -> None:
    """Check declared dispositions, not the semantic truth of a repair claim."""
    plan_path = change_dir / "execution-plan.md"
    if not plan_path.is_file():
        return
    plan = read_text(plan_path)
    try:
        body = require_unique_section(plan, "问题闭环")
        if body is None:
            return  # Legacy/no-finding plans need no additional artifact.
        columns = ["问题 ID", "来源", "问题与根因", "关联 AC/Task", "阻塞", "受影响交付件", "处理与回填", "复验依据", "状态"]
        rows = delivery_table(body, columns)
    except ValueError as error:
        draft_warn_archive_fail(reporter, archive, f"execution-plan.md feedback: {error}")
        return
    known_acs = defined_ac_ids(read_text(change_dir / "spec.md")) if (change_dir / "spec.md").is_file() else set()
    known_tasks = {row["TASK ID"].strip() for row in table_with_columns(section_text(plan, "Task 列表"), ["TASK ID"])}
    seen: set[str] = set()
    issues: list[str] = []
    for row in rows:
        finding = row["问题 ID"].strip()
        if finding in seen:
            issues.append("duplicate feedback ID " + finding)
        seen.add(finding)
        if not re.fullmatch(r"F-[0-9]+", finding):
            issues.append("invalid feedback ID " + finding)
        empty = [column for column in columns if not meaningful(row[column])]
        if empty:
            issues.append(f"{finding}: empty feedback fields: {', '.join(empty)}")
        for column in ("处理与回填", "复验依据"):
            if row[column].strip().lower() in {"pass", "通过", "resolved", "已修复"}:
                issues.append(f"{finding}: feedback {column} needs concrete evidence")
        state = row["状态"].strip().lower()
        blocking = row["阻塞"].strip()
        if blocking not in {"是", "否"}:
            issues.append(f"{finding}: feedback 阻塞 must be 是/否")
        if state not in {"resolved", "accepted"}:
            issues.append(f"{finding}: feedback not closed ({row['状态']})")
        if blocking == "是" and state == "accepted":
            issues.append(f"{finding}: blocking feedback cannot be Accepted")
        links = row["关联 AC/Task"]
        acs, tasks = set(AC_RE.findall(links)), set(TASK_RE.findall(links))
        if not acs and not tasks and not re.fullmatch(r"N/A[（(][^）)]+[）)]", links.strip()):
            issues.append(f"{finding}: feedback needs AC/Task references or N/A(reason)")
        if acs - known_acs or tasks - known_tasks:
            issues.append(f"{finding}: feedback has unknown AC/Task references")
        # Cell contains change-relative Markdown paths, separated by 、 or commas.
        paths = [value.strip().strip('`') for value in re.split(r"[、,，]", row["受影响交付件"])]
        for value in paths:
            target = change_dir / value
            if not value or Path(value).is_absolute() or not target.resolve().is_relative_to(change_dir.resolve()) or not target.is_file():
                issues.append(f"{finding}: feedback artifact missing or outside change: {value}")
    if issues:
        draft_warn_archive_fail(reporter, archive, "execution-plan.md feedback: " + "; ".join(issues))
    else:
        reporter.pass_(f"execution-plan.md feedback dispositions complete ({len(rows)} findings)")


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


def validate_i18n_constraints(change_dir: Path, reporter: Reporter, archive_mode: bool, *, section_checked: bool = False) -> None:
    proposal_path = change_dir / "proposal.md"
    design_path = change_dir / "design.md"
    if not proposal_path.is_file() or not design_path.is_file():
        return

    proposal = _visible_markdown(read_text(proposal_path))
    involvement = parse_eight_dim_involvement(proposal, I18N_TRIGGER_DIMENSION)
    if involvement != "是":
        reporter.pass_("i18n constraints not triggered")
        return

    design = _visible_markdown(read_text(design_path))
    body = section_text(design, I18N_SECTION)
    if not body:
        if section_checked:
            return  # validate_sections already emitted the single required-section failure.
        draft_warn_archive_fail(
            reporter,
            archive_mode,
            f"design.md missing {I18N_SECTION} section while 国际化 = 是",
        )
        return

    issues: list[str] = []
    if not table_has_columns(body, I18N_TABLE_COLUMNS):
        missing = [
            c for c in I18N_TABLE_COLUMNS
            if not table_has_columns(body, [c])
        ]
        issues.append(
            f"{I18N_SECTION} table missing required column: {', '.join(missing)}"
        )
    else:
        rows = table_with_columns(body, I18N_TABLE_COLUMNS)
        has_data_rows = False
        for row in rows:
            scene = row.get("调用场景", "").strip()
            if not meaningful(scene):
                continue
            has_data_rows = True
            dep_type = row.get("依赖类型", "").strip()
            if dep_type not in I18N_DEPENDENCY_TYPES:
                issues.append(f"{I18N_SECTION} row '{scene}' has invalid 依赖类型: {dep_type or '<empty>'}")
            for column in ("仓路径", "接口/方法"):
                value = row.get(column, "").strip()
                if not meaningful(value) or unresolved_markers(value):
                    issues.append(
                        f"{I18N_SECTION} row 'scene' has unresolved {column}: {value or '<empty>'}"
                    )
        if not has_data_rows:
            issues.append(f"{I18N_SECTION} has no data rows (all placeholder/empty)")

        summary_found = any(
            I18N_SUMMARY_RE.match(line)
            for line in body.splitlines()
            if line.lstrip().startswith("|")
        )
        if not summary_found:
            issues.append(f"{I18N_SECTION} missing concrete 合计 summary row (N/X/Y)")

    if issues:
        draft_warn_archive_fail(
            reporter,
            archive_mode,
            "design.md i18n constraints: " + "; ".join(issues),
        )
    else:
        reporter.pass_("design.md i18n dependency analysis has complete, confirmed rows")


def validate_archive_readiness(
    change_dir: Path,
    artifacts: dict[str, dict[str, object]],
    files: dict[str, str],
    reporter: Reporter,
) -> None:
    unresolved_required = validate_archive_placeholders(change_dir, artifacts, files, reporter)
    validate_archive_spec_mapping(change_dir, reporter)
    validate_archive_task_completion(change_dir, reporter)
    validate_archive_actual_results(change_dir, reporter)
    validate_archive_evidence_claims(change_dir, unresolved_required, reporter)


def main(argv: list[str]) -> int:
    parser = ArgumentParser(
        description="Validate one ODK change directory against the active artifacts contract.",
        epilog=("PASS means document-contract completeness only. language-specific API metadata files are structurally "
                "checked, declaration-diff added lines/markers are checked, and non-N/A documentation fields are "
                "checked for normalized coverage in the matching declaration comments; API syntax is not compiled "
                "or semantically type-checked. Language/toolchain validation is NOT VERIFIED; "
                "run the target repository's SDK/build checks separately. Exit codes remain 0/1."),
    )
    parser.add_argument("change_dir", help="ODK change directory, for example codespec/changes/arkui/12345")
    parser.add_argument("--effective-contract", action="store_true", help="Print the merged level/profile contract as JSON without validating artifacts.")
    parser.add_argument("--phase", choices=["define", "specify", "design", "plan"], help="Check the selected artifact and its dependencies; exclude future phases.")
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Require final readiness: no placeholders, all ACs/Verification Pass, Tasks complete, code/evidence backfilled and findings closed.",
    )
    parser.add_argument(
        "--design-docs-submit",
        action="store_true",
        help="Require the five base design-docs files plus conditional evidence and enforce archive-equivalent final-readiness checks.",
    )
    args = parser.parse_args(argv[1:])
    if args.phase and (args.archive or args.design_docs_submit):
        parser.error("--phase cannot weaken archive or design-docs submission validation")

    change_dir = Path(args.change_dir).resolve()
    reporter = Reporter()

    if not change_dir.is_dir():
        print(f"Change directory does not exist: {change_dir}", file=sys.stderr)
        return 1

    try:
        effective = compile_contract(change_dir, CONTRACT_PATH, phase=args.phase, submission=args.design_docs_submit)
    except (ValueError, OSError) as error:
        print(f"Effective contract error: {error}", file=sys.stderr if args.effective_contract else sys.stdout)
        return 1
    if args.effective_contract:
        print(json.dumps(effective, ensure_ascii=False, indent=2))
        return 0
    artifacts = effective["artifacts"]
    strict_delivery = args.archive or args.design_docs_submit

    mode = "archive" if args.archive else ("design-docs-submit" if args.design_docs_submit else "draft")
    print(f"Validating ODK artifact contract ({mode} mode): {change_dir}")
    print(f"Delivery level: {effective['delivery_level']}; profiles: {', '.join(effective['profiles']) or 'none'}")
    print("\nLevel A: Change Directory")
    validate_dir_name(change_dir, reporter)
    validate_target_release(change_dir, reporter)
    validate_sessions_sidecar(change_dir, reporter)
    files = validate_required_artifacts(change_dir, artifacts, reporter)
    validate_metadata_tracking(change_dir, reporter, required=args.design_docs_submit)
    validate_sections(change_dir, artifacts, files, reporter)
    validate_effective_rules(change_dir, artifacts, reporter)
    if "spec" in artifacts:
        if effective["delivery_level"] != "lite":
            validate_proposal_coverage_matrix(change_dir, reporter)
        validate_api_spec_contract(change_dir, reporter, archive=strict_delivery)
        validate_api_contract_version_chain(
            change_dir, reporter, args.phase
        )
        validate_api_declaration_diffs(change_dir, reporter, archive=strict_delivery)
    proposal_path = change_dir / "proposal.md"
    if proposal_path.is_file():
        for issue in involvement_errors(read_text(proposal_path)):
            reporter.fail(f"proposal.md: 不涉及项确认: {issue}")
        validate_proposal_tables(read_text(proposal_path), reporter, archive=strict_delivery,
                                 lite=effective["delivery_level"] == "lite")
    validate_present_optional_sections(change_dir, artifacts, reporter)
    if "spec" in artifacts:
        validate_ac_ids(change_dir, reporter, strict_delivery)
        validate_goal_us_coverage(change_dir, reporter)
        validate_spec_verification(change_dir, reporter)
    if "execution-plan" in artifacts:
        validate_delivery_feedback(change_dir, reporter, archive=strict_delivery)
        plan_path = change_dir / "execution-plan.md"
        if plan_path.is_file():
            plan = read_text(plan_path)
            if effective["delivery_level"] == "lite" or section_texts(plan, ENVIRONMENT_SECTION):
                template = CONTRACT_PATH.parent.parent / "templates/ai/execution-plan.md"
                for issue in environment_errors(plan, read_text(template),
                                                host_only_required=effective["delivery_level"] == "lite"):
                    reporter.fail(f"execution-plan.md: {issue}")
        validate_plan_traceability(change_dir, reporter)
        validate_task_review_gate(change_dir, reporter, archive=strict_delivery)
    if "design" in artifacts:
        validate_dfx_constraints(change_dir, reporter, strict_delivery)
        validate_dfx_ac_gate(change_dir, reporter, strict_delivery)
        validate_dfx_export_table(change_dir, reporter)
        validate_dfx_ad_library_basis(change_dir, reporter)
    validate_optional_evidence(change_dir, reporter)
    print("\nResource Constraints")
    if not args.phase or args.phase == "plan":
        validate_resource_constraints(change_dir, reporter, archive=strict_delivery)
    print("\ni18n Constraints")
    if "design" in artifacts:
        validate_i18n_constraints(change_dir, reporter, strict_delivery, section_checked=True)
    if strict_delivery:
        validate_archive_readiness(change_dir, artifacts, files, reporter)

    # Informational scope, not a new warning/failure or a compiler success claim.
    print("\nVerification scope:")
    print("  Document contract: checked (API signature presence/placeholders/duplicates only)")
    print("  NOT VERIFIED language/toolchain: no target SDK/compiler validation was run; "
          "run the target repository's build checks separately")
    print("\nSummary:")
    print(f"  Passed:   {reporter.passed}")
    print(f"  Warnings: {reporter.warned}")
    print(f"  Failed:   {reporter.failed}")

    return 0 if reporter.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
