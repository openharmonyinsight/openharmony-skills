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
from datetime import date
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

from odk_yaml import (  # noqa: E402
    parse_api_spec_contract,
    parse_contract_artifacts,
    parse_metadata_tracking,
    parse_resource_contract,
)
from odk_document import (  # noqa: E402
    PLACEHOLDER_RE, BRACKET_PLACEHOLDER_RE, _visible_markdown, atx_heading, headings,
    section_texts, section_text, require_unique_section, normalize_cell, split_table_row,
    is_separator_row, parsed_markdown_tables, markdown_tables, table_has_columns,
    tables_with_columns, table_with_columns, unique_table_with_columns,
    require_unique_table_with_columns, meaningful,
)
from odk_repository import parse_git_remote, metadata_repository_url, metadata_pr_url_matches  # noqa: E402
from odk_diff import valid_unified_diff  # noqa: E402
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
    r"\b(?:TBD|TODO)\b|(?<![\u4e00-\u9fff])(?:待定|待补充|待实现|待验证)(?![\u4e00-\u9fff])",
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
API_COMMON_SECTION = api_contract_scalar("common_section")
API_PER_API_SECTION = api_contract_scalar("per_api_section")
API_COMMON_VALUE_RULES = dict(
    item.split("=", 1) for item in api_contract_list("common_value_rules")
)
API_COMMON_REQUIRED_ITEMS = api_contract_list("common_required_items")
API_REQUIRED_SPEC_ITEMS = api_contract_list("per_api_required_spec_items")
API_DESCRIPTION_ELEMENTS = [
    tuple(item.split("=", 1)) for item in api_contract_list("api_description_elements")
]
API_SUPPORTED_DEVICE_COLUMNS = api_contract_list("supported_device_columns")
API_DEVICE_DIFFERENCE_COLUMNS = api_contract_list("device_difference_columns")

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


def read_frontmatter(path: Path) -> Frontmatter:
    """Read simple YAML frontmatter key:value pairs (no external deps)."""
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
    for line in lines[1:]:
        if trim_yaml_whitespace(line) == "---":
            closed = True
            break
        if "\x00" in line:
            return Frontmatter("frontmatter contains NUL")
        if re.match(r'''^[ \t]*(?:req|req_id|"req"|"req_id"|'req'|'req_id')[ \t]*:''', line):
            return Frontmatter("legacy identity field; migrate to proposal_id")
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)[ \t\r]*:[ \t\r]*(.*)$", line)
        if match:
            key = match.group(1)
            if key == "proposal_id" and key in result:
                result[key] = INVALID_PROPOSAL_ID_SCALAR
                continue
            raw = match.group(2)
            value = parse_simple_yaml_scalar(raw)
            result[key] = value if value is not None else trim_yaml_whitespace(raw)
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
    return value if value in {"是", "否"} else value or None


def api_common_value_complete(item: str, value: str) -> bool:
    if not meaningful(value) or ANGLE_PLACEHOLDER_RE.search(value) or re.search(
        r"\b(?:TBD|TODO)\b|待确认|待定|待补充|待实现|待验证",
        value,
        flags=re.IGNORECASE,
    ):
        return False

    normalized = " ".join(normalized_table_key(value).split())
    rule = API_COMMON_VALUE_RULES.get(item)
    annotation = r"(?:\s*[（(].+[）)])?"
    if rule and re.search(r"或|任选|二选一|未确定|未决", normalized):
        return False
    if rule == "boolean-decision":
        return bool(
            re.fullmatch(
                r"(?:是|否)(?:(?:\s*[：:].+)|(?:\s*[（(].+[）)]))?",
                normalized,
            )
        )
    if rule == "api-visibility":
        return normalized in {"Public", "System"}
    if rule == "language":
        return normalized in {"ArkTS", "C", "两者"}
    if rule == "system-capability":
        return bool(
            re.fullmatch(r"SystemCapability(?:\.[A-Za-z][A-Za-z0-9_]*)+", normalized)
            or re.fullmatch(r"不适用\s*[（(].+[）)]", normalized)
        )
    if rule == "api-version":
        return bool(
            re.fullmatch(r"\d+(?:\.\d+){0,2}" + annotation, normalized)
            or re.fullmatch(r"不适用\s*[（(].+[）)]", normalized)
        )
    if rule == "permission":
        return bool(
            re.fullmatch(r"无" + annotation, normalized)
            or re.fullmatch(
                r"ohos\.permission\.[A-Z][A-Z0-9_.]*(?:\s*[,，、;；+]\s*"
                r"ohos\.permission\.[A-Z][A-Z0-9_.]*)*" + annotation,
                normalized,
            )
            or re.fullmatch(r"服务侧校验\s*[：:]\s*\S.{2,}", normalized)
        )
    if rule == "device-support":
        parts = re.split(r"[（(]", normalized, maxsplit=1)
        status_text = parts[0].strip()
        if len(parts) > 1 and re.search(r"[是否]", parts[1].replace("是否", "")):
            return False
        statuses = [part.strip() for part in re.split(r"[/／]", status_text)]
        return len(statuses) in {1, 3} and all(status in {"是", "否"} for status in statuses)
    if rule == "application-model":
        marker = r"@(?:famodelonly|stagemodelonly|FaAndStageModel)"
        markers = re.findall(marker, normalized)
        if normalized.startswith("不适用"):
            return not markers and bool(re.fullmatch(r"不适用\s*[（(].+[）)]", normalized))
        return len(markers) == 1 and bool(re.fullmatch(rf"{marker}{annotation}", normalized))
    return True


def api_heading_signature(line: str) -> str | None:
    """Return an opaque signature, including empty; None means no API heading."""
    heading = atx_heading(line)
    if heading is None or heading[0] != 4 or not heading[1].startswith("API:"):
        return None
    return heading[1][len("API:"):].strip()


def api_entry_blocks(per_api_text: str) -> list[tuple[str, str]]:
    lines = per_api_text.splitlines()
    matches = [(index, signature) for index, line in enumerate(lines)
               if (signature := api_heading_signature(line)) is not None]
    entries: list[tuple[str, str]] = []
    for index, (start, signature) in enumerate(matches):
        end = matches[index + 1][0] if index + 1 < len(matches) else len(lines)
        entries.append((signature, "\n".join(lines[start + 1:end])))
    return entries


def table_rows_by_key(
    text: str,
    columns: list[str],
    key_column: str,
) -> dict[str, list[dict[str, str]]]:
    rows = unique_table_with_columns(text, columns) or []
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        result.setdefault(normalized_table_key(row.get(key_column, "")), []).append(row)
    return result


def supported_device_table_issues(rows: list[dict[str, str]]) -> list[str]:
    """Return decision errors for one per-API supported-device table."""
    issues: list[str] = []
    device_names: set[str] = set()
    for row in rows:
        device_name = normalized_table_key(row.get("设备类型", ""))
        version = normalized_table_key(row.get("起始版本", ""))
        support = normalized_table_key(row.get("是否支持", ""))
        if device_name in device_names:
            issues.append(f"duplicate supported device: {device_name}")
        device_names.add(device_name)
        if support not in {"是", "否"}:
            issues.append(f"supported device '{device_name}' must state 是 or 否")
        if not (
            re.fullmatch(r"\d+(?:\.\d+){0,2}", version)
            or re.fullmatch(r"不适用\s*[（(].+[）)]", version)
        ):
            issues.append(f"supported device '{device_name}' has invalid starting version")
    return issues


def validate_api_spec_contract(change_dir: Path, reporter: Reporter) -> None:
    proposal_path = change_dir / "proposal.md"
    spec_path = change_dir / "spec.md"
    if not proposal_path.is_file() or not spec_path.is_file():
        return

    involvement = api_sdk_involvement(_visible_markdown(read_text(proposal_path)))
    spec_sections = section_texts(_visible_markdown(read_text(spec_path)), API_SPEC_SECTION)
    issues: list[str] = []

    if involvement not in {"是", "否"}:
        reporter.fail(
            f"proposal.md: {API_TRIGGER_DIMENSION} must state 是 or 否 in {API_PROPOSAL_SECTION}"
        )
        return

    if len(spec_sections) != 1:
        reporter.fail(f"spec.md: {API_SPEC_SECTION} section must appear exactly once")
        return
    spec_section = spec_sections[0]

    if involvement == "否":
        visible = "\n".join(
            line
            for line in _visible_markdown(spec_section).splitlines()
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

    common_sections = section_texts(spec_section, API_COMMON_SECTION)
    if not common_sections:
        issues.append(f"spec.md: {API_COMMON_SECTION} subsection missing")
    elif len(common_sections) != 1:
        issues.append(f"spec.md: {API_COMMON_SECTION} subsection must appear exactly once")
    else:
        common_tables = tables_with_columns(common_sections[0], ["规格项", "值"])
        if len(common_tables) != 1:
            issues.append(f"spec.md: {API_COMMON_SECTION} must contain exactly one specification table")
        else:
            common_rows = table_rows_by_key(common_sections[0], ["规格项", "值"], "规格项")
            for item in API_COMMON_REQUIRED_ITEMS:
                matches = common_rows.get(item, [])
                if not matches:
                    issues.append(f"spec.md: {API_COMMON_SECTION} missing item: {item}")
                elif len(matches) > 1:
                    issues.append(f"spec.md: {API_COMMON_SECTION} duplicate item: {item}")
                elif not meaningful(matches[0].get("值", "")):
                    issues.append(f"spec.md: {API_COMMON_SECTION} item has empty value: {item}")
                elif not api_common_value_complete(item, matches[0].get("值", "")):
                    issues.append(f"spec.md: {API_COMMON_SECTION} unresolved template choice: {item}")

    per_api_sections = section_texts(spec_section, API_PER_API_SECTION)
    if not per_api_sections:
        issues.append(f"spec.md: {API_PER_API_SECTION} subsection has no API entries")
    elif len(per_api_sections) != 1:
        issues.append(f"spec.md: {API_PER_API_SECTION} subsection must appear exactly once")
    per_api_text = per_api_sections[0] if len(per_api_sections) == 1 else ""
    entries = api_entry_blocks(per_api_text)
    if not entries and per_api_sections:
        issues.append(f"spec.md: {API_PER_API_SECTION} subsection has no API entries")

    signatures: set[str] = set()
    for raw_signature, block in entries:
        signature = canonical_api_signature(raw_signature)
        if not api_signature_complete(raw_signature):
            issues.append(f"spec.md: incomplete API signature: {raw_signature}")
        if signature in signatures:
            issues.append(f"spec.md: duplicate API signature: {raw_signature}")
        signatures.add(signature)

        spec_tables = tables_with_columns(block, ["规格项", "值"])
        if len(spec_tables) != 1:
            issues.append(f"spec.md API '{raw_signature}': must contain exactly one specification table")
        else:
            spec_rows = table_rows_by_key(block, ["规格项", "值"], "规格项")
            for item in API_REQUIRED_SPEC_ITEMS:
                matches = spec_rows.get(item, [])
                if not matches:
                    issues.append(f"spec.md API '{raw_signature}': missing specification item: {item}")
                elif len(matches) > 1:
                    issues.append(f"spec.md API '{raw_signature}': duplicate specification item: {item}")
                elif not meaningful(matches[0].get("值", "")):
                    issues.append(f"spec.md API '{raw_signature}': empty specification item: {item}")

        description_tables = tables_with_columns(block, ["要素类别", "要素", "内容"])
        if len(description_tables) != 1:
            issues.append(f"spec.md API '{raw_signature}': must contain exactly one API description table")
        description_rows = description_tables[0] if len(description_tables) == 1 else []
        descriptions: dict[tuple[str, str], list[dict[str, str]]] = {}
        for row in description_rows:
            key = (
                normalized_table_key(row.get("要素类别", "")),
                normalized_table_key(row.get("要素", "")),
            )
            descriptions.setdefault(key, []).append(row)
        for category, element in API_DESCRIPTION_ELEMENTS:
            matches = descriptions.get((category, element), [])
            label = f"{category}/{element}"
            if not matches:
                issues.append(
                    f"spec.md API '{raw_signature}': missing API description element: {label}"
                )
            elif len(matches) > 1:
                issues.append(
                    f"spec.md API '{raw_signature}': duplicate API description element: {label}"
                )
            elif not meaningful(matches[0].get("内容", "")):
                issues.append(f"spec.md API '{raw_signature}': empty API description element: {label}")

        supported_tables = tables_with_columns(block, API_SUPPORTED_DEVICE_COLUMNS)
        if len(supported_tables) != 1:
            issues.append(f"spec.md API '{raw_signature}': must contain exactly one supported-device table")
        supported = supported_tables[0] if len(supported_tables) == 1 else []
        if not supported or any(
            not meaningful(row.get(column, ""))
            for row in supported
            for column in API_SUPPORTED_DEVICE_COLUMNS
        ):
            issues.append(f"spec.md API '{raw_signature}': supported-device table missing or empty")
        else:
            issues.extend(
                f"spec.md API '{raw_signature}': {issue}"
                for issue in supported_device_table_issues(supported)
            )

        difference_tables = tables_with_columns(block, API_DEVICE_DIFFERENCE_COLUMNS)
        if len(difference_tables) != 1:
            issues.append(f"spec.md API '{raw_signature}': must contain exactly one device-difference table")
        differences = difference_tables[0] if len(difference_tables) == 1 else []
        if not differences or any(
            not meaningful(row.get(column, ""))
            for row in differences
            for column in API_DEVICE_DIFFERENCE_COLUMNS
        ):
            issues.append(f"spec.md API '{raw_signature}': device-difference table missing or empty")

    if issues:
        for issue in issues:
            reporter.fail(issue)
    else:
        reporter.pass_("spec.md per-API specification contract is complete")


def validate_api_declaration_diffs(change_dir: Path, reporter: Reporter, *, archive: bool) -> None:
    """Require archived en/zh API declaration diffs when API/SDK is involved."""
    proposal_path = change_dir / "proposal.md"
    if not proposal_path.is_file():
        return
    involvement = api_sdk_involvement(_visible_markdown(read_text(proposal_path)))
    if involvement != "是":
        return
    missing = [
        name
        for name in ("task1-api-declaration-en.diff", "task1-api-declaration-zh.diff")
        if not (change_dir / "evidence" / name).is_file()
    ]
    if missing:
        draft_warn_archive_fail(
            reporter,
            archive,
            "API declaration diff evidence missing under evidence/: " + ", ".join(missing),
        )
        return
    invalid = []
    for language in ("en", "zh"):
        path = change_dir / "evidence" / f"task1-api-declaration-{language}.diff"
        try:
            valid = valid_unified_diff(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError):
            valid = False
        if not valid:
            invalid.append(path.name)
    if invalid:
        draft_warn_archive_fail(reporter, archive,
            "API declaration diff evidence must contain nonempty valid unified diffs: " + ", ".join(invalid))
    else:
        reporter.pass_("API declaration diff evidence (en/zh) is archived")


def validate_proposal_tables(proposal: str, reporter: Reporter, *, archive: bool) -> None:
    """Validate required device-variation and external-dependency proposal tables."""

    issues: list[str] = []
    device_section = section_text(proposal, DEVICE_VARIATION_SECTION)
    device_tables = tables_with_columns(device_section, DEVICE_VARIATION_COLUMNS)
    if not device_tables:
        issues.append(f"{DEVICE_VARIATION_SECTION} table missing required columns")
    else:
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


def parse_eight_dim_involvement(proposal: str, dimension: str) -> str | None:
    """Return 是/否 from one 不涉及项确认 dimension row, or None if the row is absent."""

    section = section_text(proposal, "不涉及项确认")
    if not section:
        return None
    rows = table_with_columns(section, ["维度", "是否涉及"])
    # New artifacts use 国际化. Read the previous label only when the canonical
    # row is absent, so upgrading the validator cannot silently disable old gates.
    labels = (dimension, "国际化/无障碍") if dimension == I18N_TRIGGER_DIMENSION else (dimension,)
    for label in labels:
        for row in rows:
            if row.get("维度", "").strip() != label:
                continue
            cell = row.get("是否涉及", "").strip()
            if not cell:
                return None
            first = cell.split()[0]
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

        # API text has its own explicit placeholder policy. Do not reinterpret
        # source identifiers or quoted literals with generic prose heuristics.
        api_signature = api_heading_signature(line)
        if api_signature is not None:
            if not api_signature_complete(api_signature):
                markers.append(f"L{line_no}: unresolved API signature placeholder")
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
    if "req" in frontmatter or "req_id" in frontmatter:
        reporter.fail("proposal.md: legacy identity field; migrate to proposal_id")
        return
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
        for section in required:  # type: ignore[assignment]
            try:
                body = require_unique_section(text, str(section))
            except ValueError as error:
                reporter.fail_once(f"{file_name}: {error}")
                continue
            if body is not None:
                reporter.pass_(f"{file_name}: required section present: {section}")
            else:
                reporter.fail(f"{file_name}: required section missing: {section}")

        conditional = artifacts[name].get("conditional_sections", [])
        for section in conditional:  # type: ignore[assignment]
            try:
                body = require_unique_section(text, str(section))
            except ValueError as error:
                reporter.fail_once(f"{file_name}: {error}")
                continue
            if section in RESOURCE_SECTIONS.values():
                continue  # trigger-aware checks live in validate_resource_constraints
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


def validate_traceability(change_dir: Path, reporter: Reporter) -> None:
    spec_path = change_dir / "spec.md"
    plan_path = change_dir / "execution-plan.md"
    if not spec_path.is_file() or not plan_path.is_file():
        return

    print("\nLevel C: Traceability")

    spec = read_text(spec_path)
    plan = read_text(plan_path)

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
        _extract_goal_refs("\n".join(current_us), defined_goals, covered_goal_refs, invalid_refs) if False else _extract_goal_refs("\n".join(current_us), defined_goals, covered_goals, invalid_refs)

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


def validate_i18n_constraints(change_dir: Path, reporter: Reporter, archive_mode: bool) -> None:
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
    validate_archive_actual_results(change_dir, reporter)
    validate_archive_evidence_claims(change_dir, unresolved_required, reporter)


def main(argv: list[str]) -> int:
    parser = ArgumentParser(
        description="Validate one ODK change directory against the active artifacts contract.",
        epilog=("PASS means document-contract completeness only. API signatures are opaque "
                "documentation, not checked by a C/ArkTS compiler. Language/toolchain validation is NOT VERIFIED; "
                "run the target repository's SDK/build checks separately. Exit codes remain 0/1."),
    )
    parser.add_argument("change_dir", help="ODK change directory, for example codespec/changes/arkui/12345")
    parser.add_argument(
        "--archive",
        action="store_true",
        help="Enable strict final-readiness checks: unresolved placeholders, filled code mapping, and Actual Result evidence.",
    )
    parser.add_argument(
        "--design-docs-submit",
        action="store_true",
        help="Require the five base design-docs files plus conditional evidence and enforce archive-equivalent final-readiness checks.",
    )
    args = parser.parse_args(argv[1:])

    change_dir = Path(args.change_dir).resolve()
    reporter = Reporter()

    if not change_dir.is_dir():
        print(f"Change directory does not exist: {change_dir}", file=sys.stderr)
        return 1

    artifacts = parse_contract_artifacts(str(CONTRACT_PATH))
    strict_delivery = args.archive or args.design_docs_submit

    mode = "archive" if args.archive else ("design-docs-submit" if args.design_docs_submit else "draft")
    print(f"Validating ODK artifact contract ({mode} mode): {change_dir}")
    print("\nLevel A: Change Directory")
    validate_dir_name(change_dir, reporter)
    validate_target_release(change_dir, reporter)
    files = validate_required_artifacts(change_dir, artifacts, reporter)
    validate_metadata_tracking(change_dir, reporter, required=args.design_docs_submit)
    validate_sections(change_dir, artifacts, files, reporter)
    validate_api_spec_contract(change_dir, reporter)
    validate_api_declaration_diffs(change_dir, reporter, archive=strict_delivery)
    proposal_path = change_dir / "proposal.md"
    if proposal_path.is_file():
        validate_proposal_tables(read_text(proposal_path), reporter, archive=strict_delivery)
    validate_present_optional_sections(change_dir, artifacts, reporter)
    validate_ac_ids(change_dir, reporter, strict_delivery)
    validate_traceability(change_dir, reporter)
    validate_goal_us_coverage(change_dir, reporter)
    validate_dfx_constraints(change_dir, reporter, strict_delivery)
    validate_dfx_ac_gate(change_dir, reporter, strict_delivery)
    validate_dfx_export_table(change_dir, reporter)
    validate_dfx_ad_library_basis(change_dir, reporter)
    validate_optional_evidence(change_dir, reporter)
    print("\nResource Constraints")
    validate_resource_constraints(change_dir, reporter, archive=strict_delivery)
    print("\ni18n Constraints")
    validate_i18n_constraints(change_dir, reporter, strict_delivery)
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
