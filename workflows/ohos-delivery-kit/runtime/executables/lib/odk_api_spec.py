#!/usr/bin/env python3
"""Small parser for the API metadata subset used by ODK validation.

This intentionally does not require PyYAML. It parses the top-level contract
fields, source/file blocks, API list entries, scalar API fields, documentation
fields, nested list membership, and the documentation fields needed by the
declaration-diff closure gate. Other nested type structures remain opaque text
and are validated by the API repository schemas during generation.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

try:  # Source and runtime both place sibling modules in the same directory.
    from api_document_style import (
        DEFAULT_API_DOCUMENT_STYLE,
        YamlScalarError,
        device_differences_restated_in_default_behavior,
        parse_yaml_scalar,
    )
except ImportError:  # Import when scripts/lib is loaded as a package from repo root.
    from scripts.lib.api_document_style import (
        DEFAULT_API_DOCUMENT_STYLE,
        YamlScalarError,
        device_differences_restated_in_default_behavior,
        parse_yaml_scalar,
    )


API_METADATA_SCHEMA_VERSION = "1.0.0"
_API_METADATA_SCHEMA_VERSION = (1, 0, 0)
_SEMANTIC_VERSION_RE = re.compile(r"^([0-9]+)\.([0-9]+)\.([0-9]+)$")


def api_metadata_schema_version_issue(value: Any) -> str | None:
    """Classify a metadata schema version without pretending compatibility."""

    text = str(value or "").strip()
    match = _SEMANTIC_VERSION_RE.fullmatch(text)
    if not match:
        return "API metadata: schemaVersion must be MAJOR.MINOR.PATCH"
    version = tuple(int(part) for part in match.groups())
    if version > _API_METADATA_SCHEMA_VERSION:
        return (
            "API metadata: schemaVersion is newer than this ODK skill; "
            "upgrade ODK before continuing"
        )
    if version < _API_METADATA_SCHEMA_VERSION:
        return (
            "API metadata: schemaVersion is older than this ODK skill; "
            "regenerate the current language-specific API metadata"
        )
    return None


def _scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        try:
            return parse_yaml_scalar(value)
        except YamlScalarError as error:
            raise ValueError(f"invalid YAML scalar: {value}") from error
    if value in ("null", "Null", "NULL"):
        return None
    if value in ("true", "True"):
        return True
    if value in ("false", "False"):
        return False
    return value


def _strip_comment(line: str) -> str:
    quote: str | None = None
    escaped = False
    for index, char in enumerate(line):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
            continue
        if char == "#":
            return line[:index].rstrip()
    return line.rstrip()


def _parse_mapping_block(lines: list[str], indent: int) -> dict[str, Any]:
    result: dict[str, Any] = {}
    pattern = re.compile(rf"^ {' ' * (indent - 1)}([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")
    for raw in lines:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        match = pattern.fullmatch(line)
        if match:
            result[match.group(1)] = _scalar(match.group(2))
    return result


def _parse_description(lines: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {"en": {}, "zh": {}}
    language: str | None = None
    in_description = False
    for raw in lines:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if line == "    description:":
            in_description = True
            language = None
            continue
        if in_description and re.match(r"^    \S", line):
            break
        if not in_description:
            continue
        en = re.fullmatch(r"\s{6}en:\s*(.*)", line)
        zh = re.fullmatch(r"\s{6}zh:\s*(.*)", line)
        if en:
            language = "en"
            continue
        if zh:
            language = "zh"
            continue
        field = re.fullmatch(r"\s{8}([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
        if field and language:
            result[language][field.group(1)] = _scalar(field.group(2))
    return result


def _parse_parameters(lines: list[str]) -> list[Any] | None:
    """Parse parameter names and localized descriptions for diff closure."""

    start: int | None = None
    for index, raw in enumerate(lines):
        line = _strip_comment(raw)
        inline = re.fullmatch(r"    parameters:\s*\[(.*)\]\s*", line)
        if inline:
            content = inline.group(1).strip()
            return [_scalar(value) for value in content.split(",")] if content else []
        if line == "    parameters:":
            start = index + 1
            break
    if start is None:
        return None

    values: list[Any] = []
    current: dict[str, Any] | None = None
    nested_type: str | None = None
    for raw in lines[start:]:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if re.match(r"^    \S", line):
            break
        item = re.fullmatch(r"^      -\s+(.*)$", line)
        if item:
            current = {}
            nested_type = None
            values.append(current)
            first = re.fullmatch(
                r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", item.group(1)
            )
            if first:
                current[first.group(1)] = _scalar(first.group(2))
            continue
        field = re.fullmatch(r"^        ([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if field and current is not None:
            key, value = field.groups()
            nested_type = None
            if key == "description":
                current["description"] = {}
            elif key in ("type", "cType") and not value.strip():
                current[key] = {}
                nested_type = key
            else:
                current[key] = _scalar(value)
            continue
        nested_field = re.fullmatch(
            r"^          ([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line
        )
        if nested_type and nested_field and current is not None:
            type_value = current.setdefault(nested_type, {})
            if isinstance(type_value, dict):
                type_value[nested_field.group(1)] = _scalar(nested_field.group(2))
            continue
        language = re.fullmatch(r"^          (en|zh):\s*(.*)$", line)
        if language and current is not None:
            description = current.setdefault("description", {})
            if isinstance(description, dict):
                description[language.group(1)] = _scalar(language.group(2))
    return values


def _parse_string_list_field(
    lines: list[str], field: str
) -> list[Any] | None:
    """Parse a constrained string-list field in inline or block form."""

    marker = f"    {field}:"
    in_block = False
    values: list[Any] = []
    for raw in lines:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        inline = re.fullmatch(rf"    {re.escape(field)}:\s*\[(.*)\]\s*", line)
        if inline:
            content = inline.group(1).strip()
            return [_scalar(value) for value in content.split(",")] if content else []
        if line == marker:
            in_block = True
            continue
        if in_block and re.match(r"^    \S", line):
            break
        if not in_block:
            continue
        item = re.fullmatch(r"^\s{6}-\s+(.*)$", line)
        if item:
            values.append(_scalar(item.group(1)))
    return values if in_block else None


def _parse_return_type(lines: list[str]) -> dict[str, Any] | None:
    """Parse return metadata, including its localized description."""

    start: int | None = None
    for index, raw in enumerate(lines):
        line = _strip_comment(raw)
        inline = re.fullmatch(r"    returnType:\s+(.*)$", line)
        if inline:
            return {"text": _scalar(inline.group(1))}
        if line == "    returnType:":
            start = index + 1
            break
    if start is None:
        return None

    result: dict[str, Any] = {}
    for raw in lines[start:]:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if re.match(r"^    \S", line):
            break
        field = re.fullmatch(r"^      ([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if field:
            key, value = field.groups()
            if key == "description":
                result["description"] = {}
            else:
                result[key] = _scalar(value)
            continue
        language = re.fullmatch(r"^        (en|zh):\s*(.*)$", line)
        if language:
            description = result.setdefault("description", {})
            if isinstance(description, dict):
                description[language.group(1)] = _scalar(language.group(2))
    return result


def _parse_error_codes(lines: list[str]) -> list[Any] | None:
    """Parse error-code entries and localized descriptions for diff closure."""

    start: int | None = None
    for index, raw in enumerate(lines):
        line = _strip_comment(raw)
        inline = re.fullmatch(r"    errorCodes:\s*\[(.*)\]\s*", line)
        if inline:
            content = inline.group(1).strip()
            return [_scalar(value) for value in content.split(",")] if content else []
        if line == "    errorCodes:":
            start = index + 1
            break
    if start is None:
        return None

    values: list[Any] = []
    current: dict[str, Any] | None = None
    for raw in lines[start:]:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if re.match(r"^    \S", line):
            break
        item = re.fullmatch(r"^      -\s+(.*)$", line)
        if item:
            current = {}
            values.append(current)
            first = re.fullmatch(
                r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", item.group(1)
            )
            if first:
                current[first.group(1)] = _scalar(first.group(2))
            continue
        field = re.fullmatch(r"^        ([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if field and current is not None:
            key, value = field.groups()
            if key == "description":
                current["description"] = {}
            else:
                current[key] = _scalar(value)
            continue
        language = re.fullmatch(r"^          (en|zh):\s*(.*)$", line)
        if language and current is not None:
            description = current.setdefault("description", {})
            if isinstance(description, dict):
                description[language.group(1)] = _scalar(language.group(2))
    return values


def _parse_members(lines: list[str]) -> list[Any] | None:
    """Parse the constrained block-list or scalar form of enum members."""

    start: int | None = None
    for index, raw in enumerate(lines):
        line = _strip_comment(raw)
        inline = re.fullmatch(r"    members:\s*\[(.*)\]\s*", line)
        if inline:
            content = inline.group(1).strip()
            return [_scalar(value) for value in content.split(",")] if content else []
        if line == "    members:":
            start = index + 1
            break
    if start is None:
        return None

    values: list[Any] = []
    for raw in lines[start:]:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if re.match(r"^    \S", line):
            break
        item = re.fullmatch(r"^\s{6}-\s+(.*)$", line)
        if item:
            values.append(_scalar(item.group(1)))
    return values


def _parse_platform(lines: list[str]) -> dict[str, dict[str, Any]] | None:
    """Parse the constrained platform mapping used by declaration markers."""

    if not any(line.rstrip() == "    platform:" for line in lines):
        return None
    result: dict[str, dict[str, Any]] = {}
    current: str | None = None
    in_platform = False
    for raw in lines:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if line == "    platform:":
            in_platform = True
            continue
        if in_platform and re.match(r"^    \S", line):
            break
        if not in_platform:
            continue
        capability = re.fullmatch(r"\s{6}([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
        if capability:
            current = capability.group(1)
            result[current] = {}
            continue
        field = re.fullmatch(r"\s{8}([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
        if field and current:
            result[current][field.group(1)] = _scalar(field.group(2))
    return result


def _parse_permissions(lines: list[str]) -> list[Any] | None:
    """Parse `permissions: []` or the constrained permission list."""

    in_permissions = False
    values: list[Any] = []
    for raw in lines:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        inline = re.fullmatch(r"    permissions:\s*\[(.*)\]\s*$", line)
        if inline:
            content = inline.group(1).strip()
            return [_scalar(value) for value in content.split(",")] if content else []
        if line == "    permissions:":
            in_permissions = True
            continue
        if in_permissions and re.match(r"^    \S", line):
            break
        if not in_permissions:
            continue
        item = re.fullmatch(r"\s{6}-\s+(.*)", line)
        if item:
            text = item.group(1).strip()
            mapping = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", text)
            if mapping:
                values.append({mapping.group(1): _scalar(mapping.group(2))})
            else:
                values.append(_scalar(text))
            continue
        field = re.fullmatch(r"\s{8}([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
        if field and values and isinstance(values[-1], dict):
            values[-1][field.group(1)] = _scalar(field.group(2))
    return values if in_permissions else None


def _parse_device_differences(lines: list[str]) -> dict[str, Any]:
    """Parse the constrained deviceDifferences block needed by style gates."""

    result: dict[str, Any] = {"items": []}
    in_block = False
    current: dict[str, Any] | None = None
    for raw in lines:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if line.rstrip() == "    deviceDifferences:":
            in_block = True
            current = None
            result = {"items": []}
            continue
        if in_block and re.match(r"^    \S", line):
            break
        if not in_block:
            continue
        field = re.fullmatch(r"      ([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
        if field:
            key, value = field.groups()
            if key != "items":
                result[key] = _scalar(value)
            current = None
            continue
        item = re.fullmatch(r"        -\s+(.*)", line)
        if item:
            current = {}
            result["items"].append(current)
            mapping = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", item.group(1))
            if mapping:
                current[mapping.group(1)] = _scalar(mapping.group(2))
            continue
        item_field = re.fullmatch(r"          ([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
        if item_field and current is not None:
            current[item_field.group(1)] = _scalar(item_field.group(2))
    return result

def _parse_top_level_block(
    lines: list[str], start: int, name: str
) -> tuple[dict[str, Any], int]:
    block: list[str] = []
    index = start + 1
    while index < len(lines):
        line = _strip_comment(lines[index])
        if line.strip() and not line.startswith("  "):
            break
        if line.strip():
            block.append(line)
        index += 1
    return _parse_mapping_block(block, 2), index


_API_MAPPING_FIELDS = {
    "propertyType", "constType", "newType", "typeExpression", "keyType",
    "valueType", "decoratorType", "aliasedType", "cType",
}


def _parse_api_mapping_field(lines: list[str], field: str) -> dict[str, Any] | None:
    """Parse one API-level mapping field without conflating it with YAML null."""

    marker = f"    {field}:"
    in_block = False
    result: dict[str, Any] = {}
    nested_key: str | None = None
    for raw in lines:
        line = _strip_comment(raw)
        if not line.strip():
            continue
        if line == marker:
            in_block = True
            continue
        if in_block and re.match(r"^    \S", line):
            break
        if not in_block:
            continue
        entry = re.fullmatch(r"^      ([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if entry:
            key, value = entry.groups()
            nested_key = None
            if value.strip():
                result[key] = _scalar(value)
            else:
                result[key] = {}
                nested_key = key
            continue
        nested = re.fullmatch(r"^        ([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if nested and nested_key is not None:
            container = result[nested_key]
            if isinstance(container, dict):
                container[nested.group(1)] = _scalar(nested.group(2))
    return result if in_block else None


def parse_api_spec(path: str | Path) -> dict[str, Any]:
    """Parse the constrained language-specific API metadata subset used by ODK."""

    raw_lines = Path(path).read_text(encoding="utf-8").splitlines()
    for raw_line in raw_lines:
        line = _strip_comment(raw_line)
        if re.search(r":\s*[|>](?:[+-]?[0-9]*)?\s*$", line):
            raise ValueError(
                "block scalars are not supported; use a quoted single-line YAML scalar"
            )
        if "\t" in raw_line:
            raise ValueError("tabs are not supported; use spaces")
    result: dict[str, Any] = {"apis": []}
    in_apis = False
    current: dict[str, Any] | None = None
    current_lines: list[str] = []
    index = 0

    def close_current() -> None:
        nonlocal current, current_lines
        if current is not None:
            current["description"] = _parse_description(current_lines)
            permissions = _parse_permissions(current_lines)
            if permissions is not None:
                current["permissions"] = permissions
            members = _parse_members(current_lines)
            if members is not None:
                current["members"] = members
            platform = _parse_platform(current_lines)
            if platform is not None:
                current["platform"] = platform
            if any(line.rstrip() == "    deviceDifferences:" for line in current_lines):
                current["deviceDifferences"] = _parse_device_differences(current_lines)
            for mapping_field in _API_MAPPING_FIELDS:
                mapping = _parse_api_mapping_field(current_lines, mapping_field)
                if mapping is not None:
                    current[mapping_field] = mapping
            for list_field in ("decoratorForm", "targetTypes"):
                values = _parse_string_list_field(current_lines, list_field)
                if values is not None:
                    current[list_field] = values
            parameters = _parse_parameters(current_lines)
            if parameters is not None:
                current["parameters"] = parameters
            return_type = _parse_return_type(current_lines)
            if return_type is not None:
                current["returnType"] = return_type
            error_codes = _parse_error_codes(current_lines)
            if error_codes is not None:
                current["errorCodes"] = error_codes
            current["_raw"] = "\n".join(current_lines)
            result["apis"].append(current)
        current = None
        current_lines = []

    while index < len(raw_lines):
        raw = raw_lines[index]
        line = _strip_comment(raw)
        if not line.strip():
            index += 1
            continue

        if not in_apis:
            top = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
            if top:
                name, value = top.groups()
                if value:
                    result[name] = _scalar(value)
                    index += 1
                    continue
                if name == "apis":
                    in_apis = True
                    index += 1
                    continue
                block, index = _parse_top_level_block(raw_lines, index, name)
                result[name] = block
                continue
            index += 1
            continue

        if re.match(r"^\S", line):
            close_current()
            in_apis = False
            top = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", line)
            if top:
                name, value = top.groups()
                if value:
                    result[name] = _scalar(value)
                elif name == "apis":
                    in_apis = True
                else:
                    # The parser returns the index of the next top-level key.
                    # Incrementing here would skip that key after `apis`.
                    block, index = _parse_top_level_block(raw_lines, index, name)
                    result[name] = block
                    continue
            index += 1
            continue

        item = re.match(r"^  -\s+(.*)$", line)
        if item:
            close_current()
            current = {}
            current_lines = [line]
            first = re.fullmatch(r"([A-Za-z][A-Za-z0-9_-]*):\s*(.*)", item.group(1))
            if first:
                current[first.group(1)] = _scalar(first.group(2))
            index += 1
            continue

        if current is not None:
            current_lines.append(line)
            field = re.fullmatch(r"^    ([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
            if field:
                # `parameters:` and `returnType:` are structurally present even
                # when their value begins on following nested lines.
                current[field.group(1)] = _scalar(field.group(2))
                if field.group(2):
                    current["_has_" + field.group(1)] = True
                else:
                    current["_has_" + field.group(1)] = True
        index += 1

    close_current()
    return result


def _placeholder(value: Any) -> bool:
    text = str(value or "").strip()
    if not text:
        return True
    return bool(
        re.search(
            r"\b(?:TBD|TODO)\b|待确认|待定|待补充|待填写|待实现|待验证",
            text,
            flags=re.IGNORECASE,
        )
        or re.fullmatch(r"<[^>\n]+>|\[[^<>\n]+\]", text, flags=re.IGNORECASE)
    )


def _non_applicable(value: Any, language: str) -> bool:
    text = str(value or "").strip()
    if language == "en":
        return text == "N/A"
    return text == "不适用"


_DESCRIPTION_LABEL_RE = re.compile(
    r"^(?:function|scenario|effect|similar\s*APIs|default\s*behavior|"
    r"constraints|activation|notes|功能|含义|使用场景|使用效果|相似\s*API|"
    r"默认行为|约束|生效条件|注意事项)\s*[:：]",
    re.IGNORECASE,
)


def _notes_restate_since(value: Any, since: Any) -> bool:
    version = str(since or "").strip()
    text = str(value or "").strip()
    if not version or not text:
        return False
    escaped = re.escape(version)
    patterns = (
        rf"(?:available|supported)\s+since\s+{escaped}",
        rf"since\s+{escaped}",
        rf"自\s*{escaped}\s*(?:起可用|起支持)",
        rf"从\s*{escaped}\s*(?:开始)?(?:可用|支持)",
    )
    return any(
        re.fullmatch(pattern + r"\s*[.。]?", text, flags=re.IGNORECASE)
        is not None
        for pattern in patterns
    )


def _notes_restate_error_codes(value: Any, api: dict[str, Any]) -> bool:
    return_type = api.get("returnType")
    if not isinstance(return_type, dict) or return_type.get("semantic") != "error-code":
        return False
    error_codes = api.get("errorCodes")
    if not isinstance(error_codes, list) or len(error_codes) < 2:
        return False
    constants = [
        str(error_code.get("constant") or "").strip()
        for error_code in error_codes
        if isinstance(error_code, dict)
    ]
    constants = [constant for constant in constants if constant]
    if len(constants) < 2:
        return False
    text = str(value or "").casefold()
    return all(
        re.search(
            rf"(?<![A-Za-z0-9_]){re.escape(constant.casefold())}(?![A-Za-z0-9_])",
            text,
        )
        is not None
        for constant in constants
    )


def _documentation_tokens(value: Any) -> list[str]:
    text = re.sub(r"\s+", " ", str(value or "").casefold())
    tokens = re.findall(r"[A-Za-z0-9_]+|\s+|[\u3400-\u9fff\uf900-\ufaff]", text)
    return [token for token in tokens if not token.isspace()]


def _longest_common_token_run(left: list[str], right: list[str]) -> int:
    if not left or not right:
        return 0
    previous = [0] * (len(right) + 1)
    best = 0
    for left_token in left:
        current = [0] * (len(right) + 1)
        for index, right_token in enumerate(right, start=1):
            if left_token == right_token:
                current[index] = previous[index - 1] + 1
                best = max(best, current[index])
        previous = current
    return best


def _localized_text(value: Any, language: str) -> str:
    if isinstance(value, dict):
        text = value.get(language)
        return str(text or "")
    return ""


def _documentation_duplication_issues(
    api: dict[str, Any],
    min_tokens: dict[str, int] | None = None,
) -> list[str]:
    thresholds = min_tokens or DEFAULT_API_DOCUMENT_STYLE.duplication_min_tokens
    label = api.get("id") or api.get("name") or "unnamed"
    description = api.get("description")
    if not isinstance(description, dict):
        return []

    parameters = api.get("parameters")
    if not isinstance(parameters, list):
        parameters = []
    return_type = api.get("returnType")
    if not isinstance(return_type, dict):
        return_type = {}

    issues: list[str] = []
    for language in ("en", "zh"):
        values = description.get(language)
        if not isinstance(values, dict):
            continue
        tag_values: list[tuple[str, str]] = []
        for index, parameter in enumerate(parameters, start=1):
            if not isinstance(parameter, dict):
                continue
            name = str(parameter.get("name") or f"parameter[{index}]")
            text = _localized_text(parameter.get("description"), language)
            if text.strip():
                tag_values.append((f"parameter {name}", text))
        return_text = _localized_text(return_type.get("description"), language)
        if return_text.strip():
            tag_values.append(("returnType", return_text))

        for element, value in values.items():
            if value is None or str(value).strip() == "":
                continue
            left_tokens = _documentation_tokens(value)
            for tag_name, tag_text in tag_values:
                common = _longest_common_token_run(
                    left_tokens, _documentation_tokens(tag_text)
                )
                threshold = thresholds.get(language, 8)
                if common >= threshold:
                    issues.append(
                        f"API metadata API '{label}': description.{language}.{element} "
                        f"duplicates {threshold}-or-more-token clause with {tag_name}"
                    )
    return issues


_REQUIRED_FIELD_TYPES: dict[str, dict[str, str]] = {
    "method": {"parameters": "list", "returnType": "mapping"},
    "function": {"parameters": "list", "returnType": "mapping"},
    "callSignature": {"parameters": "list", "returnType": "mapping"},
    "constructor": {"parameters": "list"},
    "constructSignature": {"parameters": "list", "newType": "mapping"},
    "property": {"propertyType": "mapping"},
    "const": {"constType": "mapping"},
    "enum": {"members": "list"},
    "enumMember": {
        "value": "scalar", "valueType": "scalar", "ownerEnum": "scalar"
    },
    "typeAlias": {"typeExpression": "mapping", "aliasKind": "scalar"},
    "accessor": {"accessorKind": "scalar", "propertyType": "mapping"},
    "indexSignature": {
        "keyName": "scalar", "keyType": "mapping", "valueType": "mapping"
    },
    "annotation": {"members": "list"},
    "decorator": {
        "decoratorForm": "list",
        "targetTypes": "list",
        "decoratorType": "mapping",
    },
    "callback": {"parameters": "list", "returnType": "mapping"},
    "struct": {"isOpaque": "boolean"},
    "union": {"members": "list"},
    "typedef": {"aliasedType": "mapping", "typedefKind": "scalar"},
    "macro": {"expression": "scalar"},
    "variable": {"cType": "mapping", "isConst": "boolean"},
}


def _required_fields(api: dict[str, Any]) -> list[str]:
    kind = api.get("kind")
    if kind in {"method", "function", "callSignature"}:
        return ["parameters", "returnType"]
    if kind == "constructor":
        return ["parameters"]
    if kind == "constructSignature":
        return ["parameters", "newType"]
    if kind == "property":
        return ["propertyType"]
    if kind == "const":
        return ["constType"]
    if kind == "enum":
        return ["members"]
    if kind == "enumMember":
        return ["value", "valueType", "ownerEnum"]
    if kind == "typeAlias":
        return ["typeExpression", "aliasKind"]
    if kind == "accessor":
        return ["accessorKind", "propertyType"]
    if kind == "indexSignature":
        return ["keyName", "keyType", "valueType"]
    if kind == "annotation":
        return ["members"]
    if kind == "decorator":
        return ["decoratorForm", "targetTypes", "decoratorType"]
    if kind == "callback":
        return ["parameters", "returnType"]
    if kind == "struct":
        return ["isOpaque"]
    if kind == "union":
        return ["members"]
    if kind == "typedef":
        return ["aliasedType", "typedefKind"]
    if kind == "macro":
        return ["expression"]
    if kind == "variable":
        return ["cType", "isConst"]
    return []


def _type_issue(
    api: dict[str, Any], field: str, expected: str, label: str
) -> str | None:
    value = api.get(field)
    # Required fields must have the target type; YAML null is not a list,
    # mapping, boolean, or non-empty scalar merely because the key exists.
    if expected == "list" and not isinstance(value, list):
        return f"API metadata API '{label}': {field} must be a list"
    if expected == "mapping" and not isinstance(value, dict):
        return f"API metadata API '{label}': {field} must be a mapping"
    if expected == "boolean" and not isinstance(value, bool):
        return f"API metadata API '{label}': {field} must be a boolean"
    if (
        expected == "scalar"
        and api.get("_has_" + field) is True
        and (value is None or isinstance(value, (dict, list)))
    ):
        return f"API metadata API '{label}': {field} must be a non-empty scalar"
    return None


def _nested_type_issues(
    value: Any, field: str, label: str, allowed_kinds: set[str]
) -> list[str]:
    if not isinstance(value, dict):
        return [f"API metadata API '{label}': {field} must be a mapping"]

    issues: list[str] = []
    text = value.get("text")
    if not isinstance(text, str) or not text.strip() or _placeholder(text):
        issues.append(
            f"API metadata API '{label}': {field}.text "
            "is missing, empty, or unresolved"
        )
    kind = value.get("kind")
    if kind is not None and kind not in allowed_kinds:
        issues.append(
            f"API metadata API '{label}': {field}.kind '{kind}' is invalid"
        )
    return issues


def _optional_boolean_issue(
    container: dict[str, Any], field_name: str, field_path: str, label: str
) -> str | None:
    value = container.get(field_name)
    if value is not None and not isinstance(value, bool):
        return f"API metadata API '{label}': {field_path} must be a boolean"
    return None


def _nested_description_issues(
    value: Any, field: str, label: str
) -> list[str]:
    if not isinstance(value, dict):
        return [f"API metadata API '{label}': {field} must contain en and zh"]
    issues: list[str] = []
    for language in ("en", "zh"):
        text = value.get(language)
        if (
            not isinstance(text, str)
            or not text.strip()
            or _placeholder(text)
        ):
            issues.append(
                f"API metadata API '{label}': {field}.{language} "
                "is missing or unresolved"
            )
    return issues


_API_ANGLE_PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")


def arkts_api_mode(api: dict) -> str:
    """Return the effective ArkTS API mode; omission means dynamic-only."""

    mode = api.get("apiMode")
    if isinstance(mode, str) and mode in {"static", "dynamic", "dynamic&static"}:
        return str(mode)
    if api.get("_has_apiMode") is True:
        return "invalid"
    return "dynamic"


def arkts_static_metadata_issues(metadata: dict) -> list[str]:
    """Require each ArkTS API mode to match its declaration evidence."""

    issues: list[str] = []
    apis = metadata.get("apis")
    if not isinstance(apis, list):
        return issues

    for index, api in enumerate(apis, start=1):
        if not isinstance(api, dict):
            continue
        label = api.get("id") or api.get("name") or f"API[{index}]"
        mode = arkts_api_mode(api)
        if mode not in {"static", "dynamic", "dynamic&static"}:
            continue

        file_path = str(api.get("filePath") or "").replace("\\", "/")
        declaration = str(api.get("declaration") or "")
        since = str(api.get("since") or "")
        if (
            _API_ANGLE_PLACEHOLDER_RE.search(file_path)
            # Generic types are declaration syntax, not unresolved fields.
            or _API_ANGLE_PLACEHOLDER_RE.fullmatch(declaration)
            or _API_ANGLE_PLACEHOLDER_RE.search(since)
        ):
            continue

        static_file = file_path.endswith(".static.d.ets")
        arkts_file = file_path.endswith(".d.ets")
        use_static = "'use static'" in declaration
        staticonly_marker = bool(
            re.search(r"\bstaticonly\b", since, flags=re.IGNORECASE)
        )
        static_marker = bool(re.search(r"\bstatic\b", since, flags=re.IGNORECASE))
        dynamic_static_marker = bool(
            re.search(r"\bdynamic\s*&\s*static\b", since, flags=re.IGNORECASE)
        )

        if mode == "static":
            if static_file:
                if not staticonly_marker:
                    issues.append(
                        f"API metadata API '{label}': static apiMode in a "
                        ".static.d.ets file requires a since value containing "
                        "staticonly"
                    )
            elif arkts_file:
                if not static_marker:
                    issues.append(
                        f"API metadata API '{label}': static apiMode in a .d.ets "
                        "file requires a since value containing static"
                    )
            else:
                issues.append(
                    f"API metadata API '{label}': static apiMode requires a "
                    ".d.ets or .static.d.ets filePath"
                )
            if use_static:
                issues.append(
                    f"API metadata API '{label}': static apiMode declaration "
                    "must not contain the file-level 'use static' directive"
                )
        else:
            if static_file:
                issues.append(
                    f"API metadata API '{label}': {mode} apiMode must not use a "
                    ".static.d.ets filePath"
                )
            if use_static:
                issues.append(
                    f"API metadata API '{label}': {mode} apiMode declaration "
                    "must not contain 'use static'"
                )
            if mode == "dynamic" and (
                static_marker or staticonly_marker or dynamic_static_marker
            ):
                issues.append(
                    f"API metadata API '{label}': dynamic apiMode since must not "
                    "contain a static or dynamic&static marker"
                )
            if mode == "dynamic&static" and not dynamic_static_marker:
                issues.append(
                    f"API metadata API '{label}': dynamic&static apiMode since "
                    "must contain dynamic&static"
                )

        if mode in {"static", "dynamic&static"}:
            if re.search(r"\b(?:any|Any)\b", declaration):
                issues.append(
                    f"API metadata API '{label}': {mode} apiMode declaration must "
                    "not use any"
                )
            if "|" in declaration:
                issues.append(
                    f"API metadata API '{label}': {mode} apiMode declaration must "
                    "not use union types"
                )
    return issues


def api_spec_structural_issues(data: dict[str, Any]) -> list[str]:
    """Check metadata structure shared by ArkTS and C contracts."""

    issues: list[str] = []
    schema_issue = api_metadata_schema_version_issue(data.get("schemaVersion"))
    if schema_issue:
        issues.append(schema_issue)
    language = data.get("language")
    if language not in ("arkts", "c"):
        issues.append("API metadata: language must be arkts or c")

    source = data.get("source")
    if not isinstance(source, dict):
        issues.append("API metadata: source block missing")
    else:
        for field in ("repository", "branch", "commit", "path"):
            if not str(source.get(field) or "").strip():
                issues.append(f"API metadata: source.{field} missing or empty")
        commit = str(source.get("commit") or "")
        if commit and not re.fullmatch(r"[0-9a-fA-F]{7,40}", commit):
            issues.append("API metadata: source.commit must be a 7-40 digit hex SHA")
    header = data.get("file", data.get("header"))
    if not isinstance(header, dict):
        issues.append("API metadata: file/header block missing")
    elif not str(header.get("path") or "").strip():
        issues.append("API metadata: file/header.path missing or empty")

    apis = data.get("apis")
    if not isinstance(apis, list) or not apis:
        issues.append("API metadata: apis must be a non-empty list")
        return issues

    ids: list[str] = []
    arkts_kinds = {
        "namespace", "class", "interface", "struct", "method", "function",
        "constructor", "property", "const", "enum", "enumMember", "typeAlias",
        "accessor", "callSignature", "constructSignature", "indexSignature",
        "annotation", "decorator",
    }
    c_kinds = {
        "function", "struct", "union", "enum", "enumMember", "typedef",
        "callback", "macro", "variable",
    }
    allowed_kinds = arkts_kinds if language == "arkts" else c_kinds

    for index, api in enumerate(apis, start=1):
        if not isinstance(api, dict):
            issues.append(f"API metadata API[{index}]: entry must be a mapping")
            continue
        api_id = str(api.get("id") or "")
        label = api_id or f"API[{index}]"
        ids.append(api_id)
        for field in (
            "kind", "id", "name", "qualifiedName", "declaration",
            "filePath", "startLine", "endLine",
        ):
            if api.get(field) is None or str(api.get(field, "")).strip() == "":
                issues.append(f"API metadata API '{label}': missing {field}")
                continue
            if _placeholder(api.get(field)):
                issues.append(
                    f"API metadata API '{label}': unresolved {field}"
                )
        kind = api.get("kind")
        if kind not in allowed_kinds:
            issues.append(
                f"API metadata API '{label}': kind '{kind}' is invalid for language {language}"
            )
        if language == "arkts":
            api_mode = api.get("apiMode")
            has_api_mode = api.get("_has_apiMode") is True or api_mode is not None
            if has_api_mode and api_mode not in {
                "static", "dynamic", "dynamic&static"
            }:
                issues.append(
                    f"API metadata API '{label}': apiMode must be static, dynamic, "
                    "or dynamic&static"
                )
        elif api.get("_has_apiMode") is True:
            issues.append(
                f"API metadata API '{label}': apiMode is not allowed for C metadata"
            )
        required_fields = _required_fields(api)
        for field in required_fields:
            if api.get("_has_" + field) is not True:
                issues.append(
                    f"API metadata API '{label}': kind '{kind}' missing {field}"
                )
            type_issue = _type_issue(
                api, field, _REQUIRED_FIELD_TYPES.get(str(kind), {}).get(field, ""), label
            )
            if type_issue:
                issues.append(type_issue)

        for field, expected in (
            ("permissions", "list"),
            ("parameters", "list"),
            ("returnType", "mapping"),
            ("errorCodes", "list"),
        ):
            if field in required_fields:
                continue
            if api.get(field) is not None:
                type_issue = _type_issue(api, field, expected, label)
                if type_issue:
                    issues.append(type_issue)

        permissions = api.get("permissions")
        if isinstance(permissions, list):
            for index, permission in enumerate(permissions, start=1):
                if not isinstance(permission, str) or not permission.strip():
                    issues.append(
                        f"API metadata API '{label}': permissions[{index}] "
                        "must be a non-empty string"
                    )

        parameters = api.get("parameters")
        if isinstance(parameters, list):
            type_field = "type" if language == "arkts" else "cType"
            allowed_type_kinds = (
                {
                    "primitive", "reference", "union", "intersection", "tuple",
                    "object", "function", "promise", "void", "literal", "other",
                    "array",
                }
                if language == "arkts"
                else {
                    "primitive", "pointer", "array", "struct", "enum", "union",
                    "function-pointer", "void", "other",
                }
            )
            for index, parameter in enumerate(parameters, start=1):
                if not isinstance(parameter, dict):
                    issues.append(
                        f"API metadata API '{label}': parameters[{index}] "
                        "must be a mapping"
                    )
                    continue
                if not str(parameter.get("name") or "").strip():
                    issues.append(
                        f"API metadata API '{label}': parameters[{index}].name "
                        "missing or empty"
                    )
                issues.extend(
                    _nested_type_issues(
                        parameter.get(type_field),
                        f"parameters[{index}].{type_field}",
                        label,
                        allowed_type_kinds,
                    )
                )
                required_issue = _optional_boolean_issue(
                    parameter, "required", f"parameters[{index}].required", label
                )
                if required_issue:
                    issues.append(required_issue)
                if language == "c":
                    if parameter.get("direction") not in {
                        "input", "output", "input-output"
                    }:
                        issues.append(
                            f"API metadata API '{label}': "
                            f"parameters[{index}].direction must be input, "
                            "output, or input-output"
                        )
                    for field in ("isPointer", "isConst"):
                        boolean_issue = _optional_boolean_issue(
                            parameter, field, f"parameters[{index}].{field}", label
                        )
                        if boolean_issue:
                            issues.append(boolean_issue)

        return_type = api.get("returnType")
        if isinstance(return_type, dict):
            text = return_type.get("text")
            if not isinstance(text, str) or not text.strip() or _placeholder(text):
                issues.append(
                    f"API metadata API '{label}': returnType.text "
                    "is missing, empty, or unresolved"
                )
            if language == "c":
                semantic = return_type.get("semantic")
                if semantic not in {
                    "void", "primitive", "error-code", "pointer", "handle",
                    "boolean", "other",
                }:
                    issues.append(
                        f"API metadata API '{label}': returnType.semantic must be "
                        "void, primitive, error-code, pointer, handle, boolean, "
                        "or other"
                    )
                for field in ("isConst", "isPointer"):
                    boolean_issue = _optional_boolean_issue(
                        return_type, field, f"returnType.{field}", label
                    )
                    if boolean_issue:
                        issues.append(boolean_issue)

        error_codes = api.get("errorCodes")
        if isinstance(error_codes, list):
            for index, error_code in enumerate(error_codes, start=1):
                if not isinstance(error_code, dict):
                    issues.append(
                        f"API metadata API '{label}': errorCodes[{index}] "
                        "must be a mapping"
                    )

        device_differences = api.get("deviceDifferences")
        if device_differences is not None:
            if not isinstance(device_differences, dict):
                issues.append(
                    f"API metadata API '{label}': deviceDifferences must be a mapping"
                )
            else:
                items = device_differences.get("items")
                if not isinstance(items, list):
                    issues.append(
                        f"API metadata API '{label}': deviceDifferences.items "
                        "must be a list"
                    )
                else:
                    for index, item in enumerate(items, start=1):
                        if not isinstance(item, dict) or not item:
                            issues.append(
                                f"API metadata API '{label}': "
                                f"deviceDifferences.items[{index}] must be a "
                                "non-empty mapping"
                            )
        if api.get("startLine") is not None and api.get("endLine") is not None:
            try:
                if int(api["startLine"]) > int(api["endLine"]):
                    issues.append(f"API metadata API '{label}': invalid line range")
            except (TypeError, ValueError):
                issues.append(f"API metadata API '{label}': startLine/endLine must be integers")
        if kind == "typeAlias" and api.get("aliasKind") == "object":
            issues.append(
                f"API metadata API '{label}': object typeAlias is rejected; use interface"
            )
        if language == "c" and kind in {"class", "namespace"}:
            issues.append(
                f"API metadata API '{label}': C metadata must not model C++ class/namespace"
            )
        if language == "arkts":
            for field in ("since", "syscap", "permissions", "platform", "applicationModel"):
                if api.get(field) is None:
                    issues.append(
                        f"API metadata API '{label}': missing ArkTS field {field}"
                    )
            platform = api.get("platform")
            if platform is not None and not isinstance(platform, dict):
                issues.append(
                    f"API metadata API '{label}': platform must be a mapping"
                )
            if isinstance(platform, dict):
                for capability in ("crossplatform", "atomicservice", "form"):
                    values = platform.get(capability)
                    if not isinstance(values, dict) or not isinstance(
                        values.get("enabled"), bool
                    ):
                        issues.append(
                            f"API metadata API '{label}': platform.{capability}.enabled must be boolean"
                        )
            if api.get("applicationModel") not in {
                "stage-only", "fa-only", "fa-and-stage", "both"
            }:
                issues.append(
                    f"API metadata API '{label}': invalid applicationModel"
                )
        elif language == "c":
            for field in ("since", "syscap", "permissions"):
                if api.get(field) is None:
                    issues.append(
                        f"API metadata API '{label}': missing C field {field}"
                    )

        if kind == "decorator" and isinstance(api.get("decoratorForm"), str):
            forms = [api["decoratorForm"]]
        elif kind == "decorator" and isinstance(api.get("decoratorForm"), list):
            forms = api["decoratorForm"]
        else:
            forms = []
        if "factory" in forms:
            for field in ("parameters", "returnType"):
                if api.get(field) is None:
                    issues.append(
                        f"API metadata API '{label}': factory decorator missing {field}"
                    )

    duplicates = sorted(value for value, count in Counter(ids).items() if count > 1)
    if duplicates:
        issues.append("API metadata: duplicate API IDs: " + ", ".join(duplicates))

    id_set = set(ids)
    for api in apis:
        if not isinstance(api, dict):
            continue
        parent = api.get("parentId")
        if parent is not None and str(parent) not in id_set:
            issues.append(f"API metadata API '{api.get('id')}': dangling parentId {parent}")

    enum_ids = {
        api.get("id")
        for api in apis
        if isinstance(api, dict) and api.get("kind") == "enum"
    }
    enum_members_by_owner: dict[str, set[str]] = {}
    for api in apis:
        if not isinstance(api, dict) or api.get("kind") != "enumMember":
            continue
        owner = str(api.get("ownerEnum") or "")
        enum_members_by_owner.setdefault(owner, set()).add(str(api.get("id")))
        if owner not in enum_ids:
            issues.append(f"API metadata API '{api.get('id')}': ownerEnum does not resolve")

    for api in apis:
        if not isinstance(api, dict) or api.get("kind") != "enum":
            continue
        api_id = str(api.get("id") or "")
        members = api.get("members")
        if isinstance(members, str):
            members = [members]
        if not isinstance(members, list):
            issues.append(
                f"API metadata API '{api_id}': enum members must be a list"
            )
            continue
        declared = {str(value) for value in members}
        owned = enum_members_by_owner.get(api_id, set())
        if declared != owned:
            issues.append(
                f"API metadata API '{api_id}': enum membership mismatch"
            )
    return issues


def api_documentation_duplication_issues(
    data: dict[str, Any],
    min_tokens: dict[str, int] | None = None,
) -> list[str]:
    """Report heuristic documentation duplication using configured thresholds."""

    if not DEFAULT_API_DOCUMENT_STYLE.duplication_enabled:
        return []
    issues: list[str] = []
    apis = data.get("apis")
    if not isinstance(apis, list):
        return issues
    for api in apis:
        if not isinstance(api, dict):
            continue
        issues.extend(_documentation_duplication_issues(api, min_tokens))
    return issues


def api_description_issues(data: dict[str, Any]) -> list[str]:
    """Require complete, explicit bilingual API documentation."""

    issues: list[str] = []
    elements = (
        "function", "scenario", "effect", "similarAPIs",
        "defaultBehavior", "constraints", "activation", "notes",
    )
    if not isinstance(data.get("apis"), list) or not data.get("apis"):
        return ["API metadata: apis must be a non-empty list"]

    for api in data.get("apis", []):
        if not isinstance(api, dict):
            continue
        label = api.get("id") or api.get("name") or "unnamed"
        description = api.get("description")
        if not isinstance(description, dict):
            issues.append(f"API metadata API '{label}': missing description")
            continue
        for language in ("en", "zh"):
            values = description.get(language)
            if not isinstance(values, dict):
                issues.append(f"API metadata API '{label}': missing description.{language}")
                continue
            for element in elements:
                value = values.get(element)
                if value is None or str(value).strip() == "":
                    issues.append(
                        f"API metadata API '{label}': missing description.{language}.{element}"
                    )
                    continue
                if _placeholder(value):
                    issues.append(
                        f"API metadata API '{label}': unresolved description.{language}.{element}"
                    )
                if _DESCRIPTION_LABEL_RE.match(str(value)):
                    issues.append(
                        f"API metadata API '{label}': description.{language}.{element} "
                        "must be plain prose without an element-name label"
                    )
                if element == "notes" and _notes_restate_since(value, api.get("since")):
                    issues.append(
                        f"API metadata API '{label}': description.{language}.notes "
                        "must not restate since; use the structured since field"
                    )
                if element == "notes" and _notes_restate_error_codes(value, api):
                    issues.append(
                        f"API metadata API '{label}': description.{language}.notes "
                        "must not restate errorCodes; use returnType and errorCodes"
                    )

        parameters = api.get("parameters")
        if isinstance(parameters, list):
            for index, parameter in enumerate(parameters, start=1):
                if not isinstance(parameter, dict):
                    continue
                issues.extend(
                    _nested_description_issues(
                        parameter.get("description"),
                        f"parameters[{index}].description",
                        label,
                    )
                )

        return_type = api.get("returnType")
        if isinstance(return_type, dict):
            issues.extend(
                _nested_description_issues(
                    return_type.get("description"), "returnType.description", label
                )
            )

        error_codes = api.get("errorCodes")
        if isinstance(error_codes, list):
            for index, error_code in enumerate(error_codes, start=1):
                if not isinstance(error_code, dict):
                    continue
                issues.extend(
                    _nested_description_issues(
                        error_code.get("description"),
                        f"errorCodes[{index}].description",
                        label,
                    )
                )

        issues.extend(
            device_differences_restated_in_default_behavior(
                api, prefix=f"API metadata API '{label}': "
            )
        )
    return issues
