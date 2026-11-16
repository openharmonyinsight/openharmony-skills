"""Deterministic 0.14 API Markdown contract upgrade helpers.

The upgrade assistant intentionally does not guess contract facts. It extracts
facts already confirmed in proposal.md and the legacy spec.md API section,
accepts developer-confirmed missing facts through a JSON file, renders the
language-specific API metadata contract, and reports every unresolved field.
"""

from __future__ import annotations

import json
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from odk_document import (
        markdown_tables,
        normalize_cell,
        section_texts,
        tables_with_columns,
    )
    from api_document_style import api_documentation_style_issues
    from odk_api_spec import (
        api_description_issues,
        api_documentation_duplication_issues,
        api_spec_structural_issues,
        parse_api_spec,
    )
except ImportError:  # Package import from repository root.
    from scripts.lib.odk_document import (
        markdown_tables,
        normalize_cell,
        section_texts,
        tables_with_columns,
    )
    from scripts.lib.api_document_style import api_documentation_style_issues
    from scripts.lib.odk_api_spec import (
        api_description_issues,
        api_documentation_duplication_issues,
        api_spec_structural_issues,
        parse_api_spec,
    )


SCHEMA_VERSION = "1.0.0"
API_CONTRACT_VERSION = "1.0.0"
LEGACY_COMMON_SECTION = "公共规格属性"
LEGACY_API_SECTION = "逐 API 规格"
LEGACY_API_HEADING = re.compile(r"^#{4}\s+API:\s*(.+?)\s*$", re.MULTILINE)
_DESCRIPTION_LABELS = {
    "含义/功能": "function",
    "使用场景": "scenario",
    "使用后效果": "effect",
    "相似接口差异": "similarAPIs",
    "缺省配置": "defaultBehavior",
    "规格限制": "constraints",
    "生效机制": "activation",
    "注意事项": "notes",
}
_LANGUAGE_NAMES = {
    "arkts": "ArkTS",
    "c": "C",
}
API_SPEC_FACT_ROWS = (
    "@since",
    "@syscap",
    "权限",
    "跨平台 / 元服务 / 卡片支持",
    "FA / Stage 模型",
    "设备支持与行为差异",
)


@dataclass
class UpgradeResult:
    """The rendered upgrade result and unresolved fact report."""

    metadata_by_language: dict[str, dict[str, Any]]
    spec_section: str
    legacy_format: str = "odk-014"
    missing: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    facts: dict[str, dict[str, Any]] = field(default_factory=dict)
    validation_issues: dict[str, list[str]] = field(default_factory=dict)

    @property
    def ready(self) -> bool:
        return not self.missing and not self.conflicts and not any(
            self.validation_issues.values()
        )


def _clean(value: Any) -> str:
    return normalize_cell(value).replace("*", "").replace("`", "").strip()


def _table_by_columns(text: str, columns: list[str]) -> list[dict[str, str]]:
    tables = tables_with_columns(text, columns)
    return tables[0] if tables else []


def _proposal_attributes(proposal: str) -> dict[str, str]:
    sections = section_texts(proposal, "API 设计属性")
    if not sections:
        return {}
    table = _table_by_columns(sections[0], ["属性", "值"])
    return {
        _clean(row.get("属性")): _clean(row.get("值"))
        for row in table
    }


def _common_attributes(spec: str) -> dict[str, str]:
    sections = section_texts(spec, LEGACY_COMMON_SECTION)
    if not sections:
        return {}
    table = _table_by_columns(sections[0], ["规格项", "值"])
    return {
        _clean(row.get("规格项")): _clean(row.get("值"))
        for row in table
    }


def _detected_languages(proposal_attrs: dict[str, str], common: dict[str, str]) -> list[str]:
    values = " ".join(
        proposal_attrs.get(name, "") + " " + common.get(name, "")
        for name in ("编程语言", "语言")
    )
    languages: list[str] = []
    if "arkts" in values.casefold():
        languages.append("arkts")
    if re.search(r"(?<![A-Za-z])C(?![A-Za-z])", values):
        languages.append("c")
    return languages


def _api_chunks(spec: str) -> list[tuple[str, str]]:
    section = section_texts(spec, LEGACY_API_SECTION)
    if not section:
        return []
    text = section[0]
    matches = list(LEGACY_API_HEADING.finditer(text))
    chunks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunks.append((match.group(1), text[match.end():end]))
    return chunks


def _spec_table(chunk: str) -> dict[str, str]:
    table = _table_by_columns(chunk, ["规格项", "值"])
    return {_clean(row.get("规格项")): _clean(row.get("值")) for row in table}


def _description_tables(chunk: str) -> dict[str, str]:
    table = _table_by_columns(chunk, ["要素", "内容"])
    result: dict[str, str] = {}
    for row in table:
        label = _clean(row.get("要素"))
        if label in _DESCRIPTION_LABELS:
            result[_DESCRIPTION_LABELS[label]] = _clean(row.get("内容"))
    return result


def _device_differences(
    chunk: str,
    language_facts: dict[str, Any],
    language: str,
    api_id: str,
    missing: list[str],
) -> dict[str, Any] | None:
    fact = language_facts.get("deviceDifferences")
    if isinstance(fact, dict):
        return fact

    tables = tables_with_columns(
        chunk, ["设备类型", "行为表现", "差异原因", "差异描述"]
    )
    if not tables:
        return None
    rows = tables[0]
    has_difference = any(
        not (
            "功能正常" in _clean(row.get("行为表现"))
            or "实现一致" in _clean(row.get("行为表现"))
        )
        for row in rows
    )
    if not has_difference:
        return {"enabled": False, "items": []}
    missing.append(f"{language}.apis.{api_id}.deviceDifferences")
    return None


def _normalise_na(value: str, language: str) -> str:
    text = value.strip()
    if text in {"无", "不涉及", "—", "-"}:
        return "不适用" if language == "zh" else "N/A"
    return text


def _signature_parts(declaration: str, language: str) -> tuple[str, str, str]:
    text = declaration.strip().rstrip(";")
    match = re.match(r"^(?:export\s+)?(?:declare\s+)?(.+?)\s*\(", text)
    if match:
        owner_name = match.group(1).strip()
        if language == "c":
            owner_name = owner_name.split()[-1]
        name = owner_name.split(".")[-1].split("::")[-1]
        qualified_name = owner_name
    else:
        owner_name = text.strip()
        name = owner_name
        qualified_name = owner_name
    slug = re.sub(r"[^A-Za-z0-9]+", "-", qualified_name).strip("-").casefold()
    return name, qualified_name, f"api.{slug}" if slug else "api.unnamed"


def _language_facts(facts: dict[str, Any], language: str) -> dict[str, Any]:
    value = facts.get(language, {})
    return value if isinstance(value, dict) else {}


def _english_description(
    language_facts: dict[str, Any], api_id: str
) -> dict[str, str]:
    english = language_facts.get("english", {})
    if not isinstance(english, dict):
        return {}
    value = english.get(api_id, {})
    if not isinstance(value, dict):
        return {}
    description = value.get("description", {})
    return description if isinstance(description, dict) else {}


def _line_range(
    language_facts: dict[str, Any],
    api_id: str,
    language: str,
    missing: list[str],
) -> tuple[int | None, int | None]:
    english = language_facts.get("english", {})
    api_english = english.get(api_id, {}) if isinstance(english, dict) else {}
    if not isinstance(api_english, dict):
        api_english = {}
    start = api_english.get("startLine", language_facts.get("startLine"))
    end = api_english.get("endLine", language_facts.get("endLine"))
    valid = (
        isinstance(start, int)
        and not isinstance(start, bool)
        and isinstance(end, int)
        and not isinstance(end, bool)
        and start > 0
        and end >= start
    )
    if not valid:
        missing.append(f"{language}.apis.{api_id}.startLine/endLine")
        return None, None
    return start, end


def _source_block(
    language: str,
    language_facts: dict[str, Any],
    file_path: str,
    missing: list[str],
) -> dict[str, Any]:
    repository = "interface_sdk-js" if language == "arkts" else "interface_sdk_c"
    branch = str(language_facts.get("branch") or "").strip()
    commit = str(language_facts.get("commit") or "").strip()
    source_path = str(language_facts.get("sourcePath") or "").strip() or file_path
    if not branch:
        missing.append(f"{language}.source.branch")
    if not commit:
        missing.append(f"{language}.source.commit")
    if not source_path:
        missing.append(f"{language}.source.path")
    return {
        "repository": repository,
        "branch": branch or "<missing>",
        "commit": commit or "<missing>",
        "path": source_path or "<missing>",
    }


def _file_path(
    language: str,
    common: dict[str, str],
    language_facts: dict[str, Any],
    missing: list[str],
) -> str:
    value = str(language_facts.get("filePath") or "").strip()
    if not value:
        declaration_value = common.get("是否新增声明文件", "")
        quoted = re.search(r"`([^`]+)`", declaration_value)
        if quoted:
            value = quoted.group(1)
    if not value:
        missing.append(f"{language}.filePath")
        value = "<missing>"
    return value


def _platform(
    common: dict[str, str],
    language_facts: dict[str, Any],
    missing: list[str],
) -> dict[str, dict[str, Any]]:
    fact = language_facts.get("platform")
    if isinstance(fact, dict):
        return {
            capability: {"enabled": bool(fact.get(capability, False))}
            for capability in ("crossplatform", "atomicservice", "form")
        }
    value = common.get("跨平台/元服务/卡片", "").strip()
    if value in {"否", "不涉及", "均不支持"}:
        return {
            capability: {"enabled": False}
            for capability in ("crossplatform", "atomicservice", "form")
        }
    missing.append("arkts.platform")
    return {
        capability: {"enabled": False}
        for capability in ("crossplatform", "atomicservice", "form")
    }


def _application_model(
    common: dict[str, str],
    language_facts: dict[str, Any],
    missing: list[str],
) -> str:
    fact = str(language_facts.get("applicationModel") or "").strip()
    if fact in {"stage-only", "fa-only", "fa-and-stage", "both"}:
        return fact
    value = common.get("FA/Stage 模型", "").strip().casefold()
    if "faandstagemodel" in value:
        return "fa-and-stage"
    if "famodelonly" in value:
        return "fa-only"
    if "stagemodelonly" in value:
        return "stage-only"
    if "fa" in value and "stage" in value:
        return "fa-and-stage"
    if "fa" in value:
        return "fa-only"
    if "stage" in value:
        return "stage-only"
    missing.append("arkts.applicationModel")
    return "both"


def _permissions(
    common: dict[str, str],
    language_facts: dict[str, Any],
    language: str,
    missing: list[str],
) -> list[str]:
    fact = language_facts.get("permissions")
    if isinstance(fact, list) and all(isinstance(item, str) for item in fact):
        return [item for item in fact if item.strip()]
    value = common.get("权限", "").strip()
    if not value or value in {"无", "不涉及", "—", "-"}:
        return []
    if "ohos.permission." in value:
        return [
            part.strip()
            for part in re.split(r"[;；,，]", value)
            if "ohos.permission." in part
        ]
    missing.append(f"{language}.permissions")
    return []


def _return_type(
    language: str,
    spec: dict[str, str],
    language_facts: dict[str, Any],
    api_id: str,
    missing: list[str],
) -> dict[str, Any]:
    text = spec.get("返回值", "").strip()
    if not text or text in {"无", "不涉及", "—", "-"}:
        text = "void"
    english = language_facts.get("english", {})
    return_english = ""
    return_chinese = ""
    if isinstance(english, dict):
        api_english = english.get(api_id, {})
        if isinstance(api_english, dict):
            return_fact = api_english.get("returnType")
            if isinstance(return_fact, dict):
                return_english = str(return_fact.get("en") or "").strip()
                return_chinese = str(return_fact.get("zh") or "").strip()
            else:
                return_english = str(return_fact or "").strip()
    if not return_english:
        missing.append(f"{language}.apis.{api_id}.returnType.description.en")
        return_english = "<missing>"
    if not return_chinese:
        missing.append(f"{language}.apis.{api_id}.returnType.description.zh")
        return_chinese = "<missing>"
    result: dict[str, Any] = {
        "text": text,
        "description": {
            "en": return_english,
            "zh": return_chinese,
        },
    }
    if language == "c":
        if text == "void":
            result["semantic"] = "void"
        elif text == "int32_t" and spec.get("错误码", "").strip() not in {"", "无", "不涉及", "—", "-"}:
            result["semantic"] = "error-code"
        else:
            result["semantic"] = "primitive"
    return result


def _split_parameters(text: str) -> list[str]:
    values: list[str] = []
    current = ""
    depth = 0
    for char in text:
        if char in "([{<":
            depth += 1
        elif char in ")]}>":
            depth -= 1
        if char == "," and depth == 0:
            values.append(current.strip())
            current = ""
            continue
        current += char
    if current.strip():
        values.append(current.strip())
    return values


def _parameters(
    language: str,
    declaration: str,
    language_facts: dict[str, Any],
    api_id: str,
    missing: list[str],
) -> list[dict[str, Any]]:
    text = declaration.strip().rstrip(";")
    open_index = text.find("(")
    close_index = text.rfind(")")
    if open_index < 0 or close_index < open_index:
        return []
    inside = text[open_index + 1 : close_index].strip()
    if not inside or inside == "void":
        return []

    parameter_facts = language_facts.get("parameters")
    if not isinstance(parameter_facts, dict):
        english = language_facts.get("english", {})
        api_english = (
            english.get(api_id, {}) if isinstance(english, dict) else {}
        )
        fallback = (
            api_english.get("parameters", {})
            if isinstance(api_english, dict)
            else {}
        )
        if isinstance(fallback, dict):
            parameter_facts = fallback
    if not isinstance(parameter_facts, dict):
        parameter_facts = {}

    result: list[dict[str, Any]] = []
    for raw_parameter in _split_parameters(inside):
        parameter_name = ""
        type_text = ""
        required = True
        if language == "arkts":
            match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)(\?)?\s*:\s*(.+)$", raw_parameter)
            if match:
                parameter_name = match.group(1)
                required = not match.group(2)
                type_text = match.group(3).strip()
        else:
            match = re.match(r"^(.*?)([A-Za-z_][A-Za-z0-9_]*)$", raw_parameter.strip())
            if match and match.group(1).strip():
                type_text = match.group(1).strip()
                parameter_name = match.group(2)
        if not parameter_name or not type_text:
            missing.append(f"{language}.apis.{api_id}.parameters")
            continue

        fact = parameter_facts.get(parameter_name, {})
        if not isinstance(fact, dict):
            fact = {}
        en = str(fact.get("en") or "").strip()
        zh = str(fact.get("zh") or "").strip()
        if not en:
            missing.append(
                f"{language}.apis.{api_id}.parameters.{parameter_name}.description.en"
            )
            en = "<missing>"
        if not zh:
            missing.append(
                f"{language}.apis.{api_id}.parameters.{parameter_name}.description.zh"
            )
            zh = "<missing>"

        parameter: dict[str, Any] = {
            "name": parameter_name,
            "type" if language == "arkts" else "cType": {
                "text": type_text,
            },
            "required": required,
            "description": {"en": en, "zh": zh},
        }
        if language == "c":
            parameter["direction"] = str(fact.get("direction") or "input")
            parameter["isPointer"] = "*" in type_text
            parameter["isConst"] = type_text.startswith("const")
        result.append(parameter)
    return result


def _error_codes(
    spec: dict[str, str],
    language_facts: dict[str, Any],
    language: str,
    api_id: str,
    missing: list[str],
) -> list[dict[str, Any]]:
    value = spec.get("错误码", "").strip()
    if not value or value in {"无", "不涉及", "—", "-"}:
        return []
    entries = re.findall(r"([0-9]+)[：:]\s*([^；;]+)", value)
    if not entries:
        missing.append(f"{language}.apis.{api_id}.errorCodes")
        return []
    english = language_facts.get("english", {})
    api_english = english.get(api_id, {}) if isinstance(english, dict) else {}
    error_english = (
        api_english.get("errorCodes", {}) if isinstance(api_english, dict) else {}
    )
    result: list[dict[str, Any]] = []
    for code, condition in entries:
        condition = condition.strip()
        detail = error_english.get(code, {}) if isinstance(error_english, dict) else {}
        constant = str(detail.get("constant") or "").strip() if isinstance(detail, dict) else ""
        description = str(detail.get("description") or "").strip() if isinstance(detail, dict) else ""
        if not constant:
            missing.append(f"{language}.apis.{api_id}.errorCodes[{code}].constant")
            constant = f"<missing-{code}>"
        if not description:
            missing.append(f"{language}.apis.{api_id}.errorCodes[{code}].description.en")
            description = "<missing>"
        result.append(
            {
                "constant": constant,
                "code": int(code),
                "condition": condition,
                "description": {"en": description, "zh": condition},
            }
        )
    return result


def _description(
    language: str,
    legacy: dict[str, str],
    language_facts: dict[str, Any],
    api_id: str,
    missing: list[str],
) -> dict[str, dict[str, str]]:
    zh = {
        element: _normalise_na(legacy.get(element, "无"), "zh")
        for element in _DESCRIPTION_LABELS.values()
    }
    en = _english_description(language_facts, api_id)
    for element in _DESCRIPTION_LABELS.values():
        if not str(en.get(element) or "").strip():
            missing.append(f"{language}.apis.{api_id}.description.en.{element}")
            en[element] = "<missing>"
    return {"en": en, "zh": zh}


def _effective_common_attributes(
    common: dict[str, str], spec: dict[str, str]
) -> dict[str, str]:
    """Apply per-API legacy overrides to the common specification attributes."""

    effective = dict(common)
    for key, common_value in common.items():
        override = spec.get(key, "").strip()
        if override and override != common_value:
            effective[key] = override
    return effective


def _legacy_access_level(
    proposal_attrs: dict[str, str],
    effective_common: dict[str, str],
    language: str,
    api_id: str,
    missing: list[str],
) -> str:
    value = (
        effective_common.get("API 类型")
        or proposal_attrs.get("API 类型")
        or "public"
    ).casefold()
    if value in {"public", "system"}:
        return value
    missing.append(f"{language}.apis.{api_id}.accessLevel")
    return "public"


def _metadata_api(
    language: str,
    declaration: str,
    chunk: str,
    spec: dict[str, str],
    legacy_description: dict[str, str],
    common: dict[str, str],
    proposal_attrs: dict[str, str],
    language_facts: dict[str, Any],
    missing: list[str],
) -> dict[str, Any]:
    name, qualified_name, api_id = _signature_parts(declaration, language)
    api_facts = _merge_ohos_sdd_api_facts(language_facts, api_id)
    effective_common = _effective_common_attributes(common, spec)
    file_path = _file_path(language, effective_common, api_facts, missing)
    access_level = _legacy_access_level(
        proposal_attrs, effective_common, language, api_id, missing
    )
    api_mode = str(api_facts.get("apiMode") or "").strip()
    static_api = (
        api_mode in {"static", "dynamic&static"}
        or (language == "arkts" and file_path.endswith(".static.d.ets"))
    )
    since = str(
        api_facts.get("since") or effective_common.get("@since") or ""
    ).strip()
    if not since:
        missing.append(f"{language}.apis.{api_id}.since")
        since = "<missing>"
    if language == "arkts" and static_api:
        if api_mode == "dynamic&static":
            marker = "dynamic&static"
        elif file_path.endswith(".static.d.ets"):
            marker = "staticonly"
        else:
            marker = "static"
        if marker not in since:
            since = f"{since} {marker}"
    start_line, end_line = _line_range(
        api_facts, api_id, language, missing
    )
    syscap = str(
        api_facts.get("syscap") or effective_common.get("@syscap") or ""
    ).strip()
    api: dict[str, Any] = {
        "kind": "method" if language == "arkts" else "function",
        "id": api_id,
        "parentId": None,
        "name": name,
        "qualifiedName": qualified_name,
        "declaration": declaration,
        "filePath": file_path,
        "startLine": start_line,
        "endLine": end_line,
        "accessLevel": access_level,
        "since": since,
        "syscap": syscap or "<missing>",
        "permissions": _permissions(
            effective_common, api_facts, language, missing
        ),
        "description": _description(
            language, legacy_description, api_facts, api_id, missing
        ),
        "parameters": _parameters(
            language, declaration, api_facts, api_id, missing
        ),
        "returnType": _return_type(
            language, spec, api_facts, api_id, missing
        ),
        "errorCodes": _error_codes(
            spec, api_facts, language, api_id, missing
        ),
    }
    if not syscap:
        missing.append(f"{language}.apis.{api_id}.syscap")
    device_differences = _device_differences(
        chunk, api_facts, language, api_id, missing
    )
    if device_differences is not None:
        api["deviceDifferences"] = device_differences
    if language == "arkts":
        api["platform"] = _platform(effective_common, api_facts, missing)
        api["applicationModel"] = _application_model(
            effective_common, api_facts, missing
        )
        if static_api:
            api["apiMode"] = "static"
    else:
        api["isVariadic"] = "..." in declaration
        api["callingConvention"] = "cdecl"
    return api


def _metadata(
    language: str,
    common: dict[str, str],
    proposal_attrs: dict[str, str],
    chunks: list[tuple[str, str]],
    facts: dict[str, Any],
    missing: list[str],
) -> dict[str, Any]:
    language_facts = _language_facts(facts, language)
    file_path = _file_path(language, common, language_facts, missing)
    apis = [
        _metadata_api(
            language,
            declaration,
            chunk,
            _spec_table(chunk),
            _description_tables(chunk),
            common,
            proposal_attrs,
            language_facts,
            missing,
        )
        for declaration, chunk in chunks
    ]
    metadata: dict[str, Any] = {
        "schemaVersion": SCHEMA_VERSION,
        "apiContractVersion": API_CONTRACT_VERSION,
        "language": language,
        "source": _source_block(
            language, language_facts, file_path, missing
        ),
    }
    kit = common.get("涉及 Kit", "") or proposal_attrs.get("涉及 Kit", "")
    if language == "arkts":
        file_block = {
            "path": f"interface_sdk-js/{file_path}",
            "license": "Apache-2.0",
        }
        if kit:
            file_block["kit"] = kit
        metadata["file"] = file_block
    else:
        header_block = {
            "path": f"interface_sdk_c/{file_path}",
            "license": "Apache-2.0",
        }
        if kit:
            header_block["kit"] = kit
        metadata["header"] = header_block
    metadata["apis"] = apis
    return metadata


def _yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def _render_mapping(value: dict[str, Any], indent: int = 0) -> list[str]:
    prefix = " " * indent
    lines: list[str] = []
    for key, item in value.items():
        if isinstance(item, dict):
            if item:
                lines.append(f"{prefix}{key}:")
                lines.extend(_render_mapping(item, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {{}}")
        elif isinstance(item, list):
            if not item:
                lines.append(f"{prefix}{key}: []")
            else:
                lines.append(f"{prefix}{key}:")
                for entry in item:
                    if isinstance(entry, dict):
                        if not entry:
                            lines.append(f"{prefix}  - {{}}")
                            continue
                        entry_lines = _render_mapping(entry, indent + 4)
                        first = entry_lines[0]
                        lines.append(prefix + "  - " + first.lstrip())
                        lines.extend(entry_lines[1:])
                    else:
                        lines.append(f"{prefix}  - {_yaml_scalar(entry)}")
        else:
            lines.append(f"{prefix}{key}: {_yaml_scalar(item)}")
    return lines


def render_metadata(metadata: dict[str, Any]) -> str:
    return "\n".join(_render_mapping(metadata)) + "\n"


def _markdown_table_cell(value: Any) -> str:
    text = str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", "<br>")


def render_spec_section(
    metadata_by_language: dict[str, dict[str, Any]],
    legacy_format: str = "odk-014",
) -> str:
    files = [
        "arkts-api-spec.yaml" if language == "arkts" else "c-api-spec.yaml"
        for language in metadata_by_language
    ]
    language_names = [_LANGUAGE_NAMES[language] for language in metadata_by_language]
    legacy_label = (
        "ohos-sdd/v1 API 链升级助手" if legacy_format == "ohos-sdd-v1"
        else "0.14 API 链升级助手"
    )
    fact_source = (
        "ohos-sdd/v1 proposal/spec + 开发者确认"
        if legacy_format == "ohos-sdd-v1"
        else "0.14 proposal/spec + 开发者确认"
    )
    apis = [api for metadata in metadata_by_language.values() for api in metadata["apis"]]
    fact_rows = "\n".join(
        f"| {fact} | 各 API metadata | {fact_source} | 已确认 |"
        for fact in API_SPEC_FACT_ROWS
    )
    overview_rows = "\n".join(
        "| "
        + " | ".join(
            _markdown_table_cell(api[field])
            for field in ("id", "kind", "declaration", "since")
        )
        + " | 已确认 |"
        for api in apis
    )
    return f"""## API 规格定义

> 本变更的 API 契约由 { '、'.join(files) } 定义。本章节只提供概览和确认指引，
> 不是逐 API 规格真相源。

契约文件：`{'`、`'.join(files)}`

| 项 | 值 |
|---|---|
| Schema 版本 | {SCHEMA_VERSION} |
| API 契约版本 | {API_CONTRACT_VERSION} |
| API 数量 | {len(apis)} |
| 确认状态 | 已确认 |

### API 概览

| API ID | 类型 | 完整签名 | @since | 确认状态 |
|--------|------|----------|--------|----------|
{overview_rows}

### API 事实溯源与待确认项

| API 事实 | 结果 | 来源 | 状态 |
|----------|------|------|------|
| 语言 | { ' / '.join(language_names) } | {legacy_label} | 已确认 |
{fact_rows}
"""


def validate_rendered_metadata(rendered: str) -> list[str]:
    """Run the complete metadata checks against the exact rendered YAML."""

    with tempfile.TemporaryDirectory(prefix="odk-api-upgrade-") as temporary:
        path = Path(temporary) / "api-spec.yaml"
        path.write_text(rendered, encoding="utf-8")
        parsed = parse_api_spec(path)
    issues = api_spec_structural_issues(parsed)
    if parsed.get("apiContractVersion") != API_CONTRACT_VERSION:
        issues.append(
            "API metadata: apiContractVersion must be "
            f"{API_CONTRACT_VERSION}"
        )
    issues.extend(api_description_issues(parsed))
    issues.extend(api_documentation_duplication_issues(parsed))
    for api in parsed.get("apis", []):
        if isinstance(api, dict):
            label = api.get("id") or api.get("name") or "unnamed"
            issues.extend(api_documentation_style_issues(api, str(label)))
    return issues


def _validate_metadata(metadata: dict[str, Any]) -> list[str]:
    return validate_rendered_metadata(render_metadata(metadata))


def _detect_ohos_sdd_format(spec: str) -> bool:
    return (
        "## API 变更分析" in spec
        and "## 接口规格" in spec
        and "### 接口定义" in spec
    )


def _ohos_sdd_api_tables(spec: str) -> dict[str, list[dict[str, str]]]:
    section = section_texts(spec, "API 变更分析")
    if not section:
        return {}
    result: dict[str, list[dict[str, str]]] = {}
    subsections = {
        "ArkTS API": section_texts(section[0], "ArkTS API"),
        "Native C-API": section_texts(section[0], "Native C-API"),
    }
    for name, bodies in subsections.items():
        if not bodies:
            continue
        table = tables_with_columns(bodies[0], ["API 名称", "功能描述"])
        result[name] = table[0] if table else []
    return result


def _ohos_sdd_signature_by_name(
    spec: str, name: str, language: str = "arkts"
) -> str | None:
    section = section_texts(spec, "接口规格")
    if not section:
        return None
    text = section[0]
    signature_label = (
        "函数签名 (ArkTS)" if language == "arkts" else "函数签名 (CAPI)"
    )
    match_name = re.match(
        r"([A-Za-z_][A-Za-z0-9_]*)", name.rsplit(".", 1)[-1]
    )
    if match_name is None:
        return None
    pattern = re.compile(
        rf"^\*\*{re.escape(match_name.group(1))}(?:\s*—.*?)?\*\*\s*$",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        following = text[match.end():match.end() + 2500]
        signature_rows = tables_with_columns(following, ["属性", "值"])
        if signature_rows:
            for row in signature_rows[0]:
                label = _clean(row.get("属性", ""))
                if label.startswith(signature_label):
                    value = str(row.get("值") or "").strip()
                    match = re.search(r"`([^`]+)`", value)
                    return match.group(1) if match else value
    return None


def _ohos_sdd_language_blocks(spec: str) -> dict[str, list[str]]:
    section = section_texts(spec, "接口规格")
    if not section:
        return {}
    text = section[0]
    blocks: dict[str, list[str]] = {"arkts": [], "c": []}
    current: str | None = None
    for line in text.splitlines():
        if line.strip() == "### 接口定义":
            current = None
            continue
        if current is not None and line.startswith("## "):
            current = None
        match = re.search(r"\*\*.*?\*\*(?:\s*—.*)?", line)
        if match:
            current = "arkts"
            blocks[current].append(line)
        elif current is not None:
            blocks[current].append(line)
    return blocks


def _ohos_sdd_api_name(value: str) -> str:
    text = _clean(value)
    match = re.search(r"`([^`]+)`", text)
    if match:
        return match.group(1)
    return text.split(" ", 1)[0].split("(", 1)[0]


def _ohos_sdd_signature(value: str) -> str:
    text = _clean(value)
    match = re.search(r"`([^`]+)`", text)
    return match.group(1) if match else text


def _ohos_sdd_access_level(
    row: dict[str, str], api_id: str, missing: list[str]
) -> str:
    value = _clean(row.get("开放范围", "")).casefold()
    if re.fullmatch(r"public(?:\s+api)?", value):
        return "public"
    if re.fullmatch(r"system(?:\s+api)?", value):
        return "system"
    missing.append(f"{api_id}.accessLevel")
    return "public"


def _ohos_sdd_description(
    language: str,
    description: str,
    language_facts: dict[str, Any],
    api_id: str,
    missing: list[str],
) -> dict[str, dict[str, str]]:
    english = language_facts.get("english", {})
    api_english = english.get(api_id, {}) if isinstance(english, dict) else {}
    supplied = (
        api_english.get("description", {})
        if isinstance(api_english, dict)
        else {}
    )
    if not isinstance(supplied, dict):
        supplied = {}

    zh: dict[str, str] = {}
    en: dict[str, str] = {}
    for element in _DESCRIPTION_LABELS.values():
        # ohos-sdd/v1 exposes only the function description. Other elements are
        # explicitly non-applicable rather than copies of that description.
        zh[element] = (
            _normalise_na(description, "zh")
            if element == "function"
            else "不适用"
        )
        value = str(supplied.get(element) or "").strip()
        if not value:
            missing.append(f"{language}.apis.{api_id}.description.en.{element}")
            value = "<missing>"
        en[element] = value
    return {"en": en, "zh": zh}


def build_upgrade(
    proposal: str,
    spec: str,
    facts: dict[str, Any] | None = None,
    languages: list[str] | None = None,
    *,
    legacy_format: str = "auto",
) -> UpgradeResult:
    """Build current API metadata from a supported legacy API chain."""

    facts = facts or {}
    proposal_attrs = _proposal_attributes(proposal)
    detected_format = (
        "ohos-sdd-v1" if _detect_ohos_sdd_format(spec) else "odk-014"
    )
    if legacy_format == "auto":
        legacy_format = detected_format

    if legacy_format == "ohos-sdd-v1":
        return _build_ohos_sdd_v1(
            proposal, spec, facts, languages, legacy_format
        )

    common = _common_attributes(spec)
    detected = languages or _detected_languages(proposal_attrs, common)
    chunks = _api_chunks(spec)
    missing: list[str] = []
    conflicts: list[str] = []
    if not detected:
        missing.append("language")
        detected = []
    if not chunks:
        missing.append("apis")
    if len(detected) > 1:
        conflicts.append(
            "legacy chain declares multiple languages; run the assistant once per "
            "language with --language and language-specific spec facts"
        )

    metadata_by_language = {
        language: _metadata(
            language, common, proposal_attrs, chunks, facts, missing
        )
        for language in detected
    }
    spec_section = render_spec_section(metadata_by_language, legacy_format)
    validation_issues = {
        language: _validate_metadata(metadata)
        for language, metadata in metadata_by_language.items()
    }
    return UpgradeResult(
        metadata_by_language=metadata_by_language,
        spec_section=spec_section,
        missing=sorted(set(missing)),
        conflicts=conflicts,
        facts=facts,
        validation_issues=validation_issues,
        legacy_format=legacy_format,
    )


def _merge_ohos_sdd_api_facts(
    language_facts: dict[str, Any], api_id: str
) -> dict[str, Any]:
    apis = language_facts.get("apis", {})
    api_fact = apis.get(api_id, {}) if isinstance(apis, dict) else {}
    if not isinstance(api_fact, dict):
        api_fact = {}
    merged = {
        key: value for key, value in language_facts.items() if key != "apis"
    }
    for key in (
        "since", "syscap", "platform", "applicationModel",
        "permissions", "deviceDifferences", "returnType",
        "parameters", "startLine", "endLine", "apiMode",
    ):
        if key in api_fact:
            merged[key] = api_fact[key]
    english = merged.get("english", {})
    if not isinstance(english, dict):
        english = {}
    api_english = api_fact.get("english", {})
    if isinstance(api_english, dict) and "description" in api_english:
        english[api_id] = api_english
    elif isinstance(api_english, dict):
        for api_id_value, value in api_english.items():
            english[api_id_value] = value
    merged["english"] = english
    return merged


def _ohos_sdd_arkts_return_type(
    api_id: str,
    api_language_facts: dict[str, Any],
    missing: list[str],
) -> dict[str, Any]:
    """Build an ArkTS return type only from confirmed facts."""

    fact = api_language_facts.get("returnType")
    if not isinstance(fact, dict):
        fact = {}
    text = str(fact.get("text") or "").strip()
    english = str(fact.get("en") or "").strip()
    chinese = str(fact.get("zh") or "").strip()
    if not text:
        missing.append(f"arkts.apis.{api_id}.returnType.text")
        text = "<missing>"
    if not english:
        missing.append(f"arkts.apis.{api_id}.returnType.description.en")
        english = "<missing>"
    if not chinese:
        missing.append(f"arkts.apis.{api_id}.returnType.description.zh")
        chinese = "<missing>"
    return {
        "text": text,
        "description": {"en": english, "zh": chinese},
    }


def _ohos_sdd_permissions(
    language: str,
    api_id: str,
    api_language_facts: dict[str, Any],
    missing: list[str],
) -> list[str]:
    fact = api_language_facts.get("permissions")
    if isinstance(fact, list) and all(isinstance(item, str) for item in fact):
        return [item for item in fact if item.strip()]
    missing.append(f"{language}.apis.{api_id}.permissions")
    return []


def _ohos_sdd_device_differences(
    language: str,
    api_id: str,
    api_language_facts: dict[str, Any],
    missing: list[str],
) -> dict[str, Any] | None:
    fact = api_language_facts.get("deviceDifferences")
    if isinstance(fact, dict):
        return fact
    missing.append(f"{language}.apis.{api_id}.deviceDifferences")
    return None


def _ohos_sdd_c_parameters(
    api_id: str,
    api_language_facts: dict[str, Any],
    missing: list[str],
) -> list[dict[str, Any]]:
    fact = api_language_facts.get("parameters")
    if not isinstance(fact, list):
        missing.append(f"c.apis.{api_id}.parameters")
        return []
    result: list[dict[str, Any]] = []
    for index, item in enumerate(fact, start=1):
        if not isinstance(item, dict):
            missing.append(f"c.apis.{api_id}.parameters[{index}]")
            continue
        name = str(item.get("name") or "").strip()
        c_type = item.get("cType")
        direction = str(item.get("direction") or "").strip()
        description = item.get("description")
        if not name:
            missing.append(f"c.apis.{api_id}.parameters[{index}].name")
        if not isinstance(c_type, dict) or not str(c_type.get("text") or "").strip():
            missing.append(f"c.apis.{api_id}.parameters[{index}].cType.text")
        if direction not in {"input", "output", "input-output"}:
            missing.append(
                f"c.apis.{api_id}.parameters[{index}].direction"
            )
        if not isinstance(description, dict):
            missing.append(
                f"c.apis.{api_id}.parameters[{index}].description"
            )
            description = {}
        en = str(description.get("en") or "").strip()
        zh = str(description.get("zh") or "").strip()
        if not en:
            missing.append(
                f"c.apis.{api_id}.parameters[{index}].description.en"
            )
        if not zh:
            missing.append(
                f"c.apis.{api_id}.parameters[{index}].description.zh"
            )
        if not name or not isinstance(c_type, dict):
            continue
        normalized_type = {
            "text": str(c_type.get("text") or "<missing>"),
        }
        for field in ("kind", "isConst", "isPointer", "pointerDepth"):
            if field in c_type:
                normalized_type[field] = c_type[field]
        result.append(
            {
                "name": name,
                "cType": normalized_type,
                "required": item.get("required", True),
                "direction": direction or "input",
                "description": {
                    "en": en or "<missing>",
                    "zh": zh or "<missing>",
                },
            }
        )
    return result


def _ohos_sdd_c_return_type(
    language: str,
    api_id: str,
    api_language_facts: dict[str, Any],
    missing: list[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build C return and value types only from confirmed facts."""

    fact = api_language_facts.get("returnType")
    if not isinstance(fact, dict):
        fact = {}
    text = str(fact.get("text") or "").strip()
    semantic = str(fact.get("semantic") or "").strip()
    kind = str(fact.get("kind") or "").strip()
    english = str(fact.get("en") or "").strip()
    chinese = str(fact.get("zh") or "").strip()
    if not text:
        missing.append(f"{language}.apis.{api_id}.returnType.text")
        text = "<missing>"
    if semantic not in {
        "void", "primitive", "error-code", "pointer", "handle", "boolean", "other"
    }:
        missing.append(f"{language}.apis.{api_id}.returnType.semantic")
        semantic = "<missing>"
    if kind not in {"primitive", "pointer", "handle", "other"}:
        missing.append(f"{language}.apis.{api_id}.cType.kind")
        kind = "<missing>"
    if not english:
        missing.append(f"{language}.apis.{api_id}.returnType.description.en")
        english = "<missing>"
    if not chinese:
        missing.append(f"{language}.apis.{api_id}.returnType.description.zh")
        chinese = "<missing>"
    return_type = {
        "text": text,
        "semantic": semantic,
        "description": {"en": english, "zh": chinese},
    }
    c_type = {"text": text, "kind": kind, "isConst": False}
    return return_type, c_type


def _build_ohos_sdd_v1(
    proposal: str,
    spec: str,
    facts: dict[str, Any],
    languages: list[str] | None,
    legacy_format: str,
) -> UpgradeResult:
    """Convert the ohos-sdd/v1 API analysis and interface specification."""

    api_tables = _ohos_sdd_api_tables(spec)
    detected: list[str] = []
    if api_tables.get("ArkTS API"):
        detected.append("arkts")
    if api_tables.get("Native C-API"):
        detected.append("c")
    if languages:
        detected = [language for language in languages if language in detected]
    if not languages:
        languages = []
    missing: list[str] = []
    conflicts: list[str] = []
    if not detected:
        missing.append("language")
        detected = []
    if len(detected) > 1 and len(languages) != 1:
        conflicts.append(
            "ohos-sdd/v1 declares multiple languages; run once per language "
            "with --language arkts or --language c"
        )

    metadata_by_language: dict[str, dict[str, Any]] = {}
    for language in detected:
        language_facts = _language_facts(facts, language)
        file_path = _file_path(language, {}, language_facts, missing)
        source = _source_block(language, language_facts, file_path, missing)
        language_table = (
            api_tables.get("ArkTS API", [])
            if language == "arkts"
            else api_tables.get("Native C-API", [])
        )
        apis: list[dict[str, Any]] = []
        for row in language_table:
            api_name = _ohos_sdd_api_name(row.get("API 名称", ""))
            declaration = _ohos_sdd_signature(row.get("API 名称", ""))
            description = _clean(row.get("功能描述", "API"))
            qualified_name = api_name
            name = qualified_name.rsplit(".", 1)[-1]
            api_id = "api." + re.sub(
                r"[^A-Za-z0-9]+", "-", qualified_name
            ).strip("-").casefold()
            api_language_facts = _merge_ohos_sdd_api_facts(
                language_facts, api_id
            )
            if language == "arkts":
                declaration = (
                    _ohos_sdd_signature_by_name(spec, api_name) or declaration
                )
            start_line, end_line = _line_range(
                api_language_facts, api_id, language, missing
            )
            if language == "c":
                c_function_signature = _ohos_sdd_signature_by_name(
                    spec, api_name, language
                )
                name = qualified_name
                api_id = "api." + re.sub(
                    r"[^A-Za-z0-9]+", "-", qualified_name
                ).strip("-").casefold()
            if language == "c":
                c_return_type, c_type = _ohos_sdd_c_return_type(
                    language, api_id, api_language_facts, missing
                )
                c_kind = (
                    "function"
                    if c_function_signature
                    and re.search(r"\(.*\)", c_function_signature)
                    else "variable"
                )
                api = {
                    "kind": c_kind,
                    "id": api_id,
                    "parentId": None,
                    "name": name,
                    "qualifiedName": qualified_name,
                    "declaration": (
                        c_function_signature or declaration
                        if c_kind == "function"
                        else declaration
                    ),
                    "filePath": file_path,
                    "startLine": start_line,
                    "endLine": end_line,
                    "accessLevel": _ohos_sdd_access_level(
                        row, f"c.apis.{api_id}", missing
                    ),
                    "since": api_language_facts.get("since", "<missing>"),
                    "syscap": api_language_facts.get("syscap", "<missing>"),
                    "permissions": _ohos_sdd_permissions(
                        language, api_id, api_language_facts, missing
                    ),
                    "description": _ohos_sdd_description(
                        language, description, api_language_facts, api_id, missing
                    ),
                }
                if c_kind == "function":
                    api["parameters"] = _ohos_sdd_c_parameters(
                        api_id, api_language_facts, missing
                    )
                    api["returnType"] = c_return_type
                    api["isVariadic"] = False
                    api["callingConvention"] = "cdecl"
                else:
                    api["cType"] = c_type
                    api["isConst"] = False
                differences = _ohos_sdd_device_differences(
                    language, api_id, api_language_facts, missing
                )
                if differences is not None:
                    api["deviceDifferences"] = differences
                if api_language_facts.get("since") is None:
                    missing.append(f"c.apis.{api_id}.since")
                if api_language_facts.get("syscap") is None:
                    missing.append(f"c.apis.{api_id}.syscap")
            else:
                api = {
                    "kind": "method",
                    "id": api_id,
                    "parentId": None,
                    "name": name,
                    "qualifiedName": qualified_name,
                    "declaration": declaration,
                    "filePath": file_path,
                    "startLine": start_line,
                    "endLine": end_line,
                    "accessLevel": _ohos_sdd_access_level(
                        row, f"arkts.apis.{api_id}", missing
                    ),
                    "since": api_language_facts.get("since", "<missing>"),
                    "syscap": api_language_facts.get("syscap", "<missing>"),
                    "permissions": _ohos_sdd_permissions(
                        language, api_id, api_language_facts, missing
                    ),
                    "platform": {
                        "crossplatform": {"enabled": False},
                        "atomicservice": {"enabled": False},
                        "form": {"enabled": False},
                    },
                    "applicationModel": "both",
                    "description": _ohos_sdd_description(
                        language, description, api_language_facts, api_id, missing
                    ),
                    "parameters": _parameters(
                        language,
                        declaration,
                        api_language_facts,
                        api_id,
                        missing,
                    ),
                    "returnType": _ohos_sdd_arkts_return_type(
                        api_id, api_language_facts, missing
                    ),
                    "errorCodes": [],
                }
                differences = _ohos_sdd_device_differences(
                    language, api_id, api_language_facts, missing
                )
                if differences is not None:
                    api["deviceDifferences"] = differences
                if api_language_facts.get("since") is None:
                    missing.append(f"arkts.apis.{api_id}.since")
                if api_language_facts.get("syscap") is None:
                    missing.append(f"arkts.apis.{api_id}.syscap")
                platform = api_language_facts.get("platform")
                if not isinstance(platform, dict):
                    missing.append(f"arkts.apis.{api_id}.platform")
                else:
                    api["platform"] = {
                        capability: {
                            "enabled": bool(platform.get(capability, False))
                        }
                        for capability in (
                            "crossplatform", "atomicservice", "form"
                        )
                    }
                application_model = api_language_facts.get("applicationModel")
                if application_model not in {
                    "stage-only", "fa-only", "fa-and-stage", "both"
                }:
                    missing.append(
                        f"arkts.apis.{api_id}.applicationModel"
                    )
                else:
                    api["applicationModel"] = application_model
            apis.append(api)

        metadata: dict[str, Any] = {
            "schemaVersion": SCHEMA_VERSION,
            "apiContractVersion": API_CONTRACT_VERSION,
            "language": language,
            "source": source,
        }
        if language == "arkts":
            metadata["file"] = {
                "path": f"interface_sdk-js/{file_path}",
                "license": "Apache-2.0",
            }
        else:
            metadata["header"] = {
                "path": f"interface_sdk_c/{file_path}",
                "license": "Apache-2.0",
            }
        metadata["apis"] = apis
        metadata_by_language[language] = metadata

    spec_section = render_spec_section(metadata_by_language, legacy_format)
    validation_issues = {
        language: _validate_metadata(metadata)
        for language, metadata in metadata_by_language.items()
    }
    return UpgradeResult(
        metadata_by_language=metadata_by_language,
        spec_section=spec_section,
        missing=sorted(set(missing)),
        conflicts=conflicts,
        facts=facts,
        validation_issues=validation_issues,
        legacy_format=legacy_format,
    )


def render_report(result: UpgradeResult, write: bool = False) -> str:
    lines = [
        f"# {result.legacy_format} API chain upgrade report",
        "",
        "## Summary",
        "",
        f"- Schema version: {SCHEMA_VERSION}",
        f"- API contract version: {API_CONTRACT_VERSION}",
        f"- Languages: {', '.join(result.metadata_by_language) or 'unknown'}",
        f"- APIs: {sum(len(metadata['apis']) for metadata in result.metadata_by_language.values())}",
        f"- Missing facts: {len(result.missing)}",
        f"- Conflicts: {len(result.conflicts)}",
        f"- Validation issues: {sum(len(values) for values in result.validation_issues.values())}",
        f"- Mode: {'write' if write else 'dry-run'}",
        "",
    ]
    if result.missing:
        lines.extend(["## Missing facts", ""])
        lines.extend(f"- `{item}`" for item in result.missing)
        lines.append("")
    if result.conflicts:
        lines.extend(["## Conflicts", ""])
        lines.extend(f"- {item}" for item in result.conflicts)
        lines.append("")
    validation_issues = [
        issue
        for issues in result.validation_issues.values()
        for issue in issues
    ]
    if validation_issues:
        lines.extend(["## Validation issues", ""])
        lines.extend(f"- {issue}" for issue in validation_issues)
        lines.append("")
    if result.ready:
        lines.extend(
            [
                "## Result",
                "",
                "All extracted and developer-confirmed facts are complete. "
                "The language-specific metadata files pass the current structural "
                "contract.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Result",
                "",
                "The upgrade is blocked. Do not write API metadata until every missing fact and conflict is resolved.",
                "",
            ]
        )
    return "\n".join(lines)


def replace_api_spec_section(spec_text: str, new_section: str) -> str:
    """Replace only the top-level API specification section."""

    lines = spec_text.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == "## API 规格定义":
            start = index
            break
    if start is None:
        # ohos-sdd/v1 has no generated overview yet. Append it without altering
        # unrelated top-level sections; subsequent runs replace it in place.
        return spec_text.rstrip() + "\n\n" + new_section.strip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        stripped = lines[index].lstrip()
        if stripped.startswith("#") and not stripped.startswith("###"):
            end = index
            break
    replaced = new_section.splitlines() + [""]
    return "\n".join(lines[:start] + replaced + lines[end:]) + "\n"
