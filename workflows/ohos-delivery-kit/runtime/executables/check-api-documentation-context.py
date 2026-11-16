#!/usr/bin/env python3
"""Validate API documentation subagent output against its bounded context.

The checker is deliberately structural: it verifies API identity closure,
exact confirmed-value coverage in both documentation languages, forbidden
documentation terminology, and the configured Chinese/ASCII spacing style. It
does not claim to understand natural-language semantics.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from api_document_style import (  # noqa: E402
    DOCUMENT_STYLE_CHINESE_ENGLISH_SPACING,
    DOCUMENT_STYLE_DUPLICATION_ENABLED,
    DOCUMENT_STYLE_DUPLICATION_MIN_TOKENS,
    FORBIDDEN_DOCUMENTATION_TERMS,
    YamlScalarError,
    api_documentation_style_issues,
    chinese_english_spacing_issue,
    device_differences_restated_in_default_behavior,
    parse_yaml_scalar,
)

# Preserve the historical private names used by regression tests and callers.
_FORBIDDEN_DOCUMENTATION_TERMS = FORBIDDEN_DOCUMENTATION_TERMS
_DOCUMENT_STYLE_CHINESE_ENGLISH_SPACING = DOCUMENT_STYLE_CHINESE_ENGLISH_SPACING
_chinese_english_spacing_issue = chinese_english_spacing_issue


class SimpleYamlError(ValueError):
    """A constrained YAML document could not be parsed."""


@dataclass(frozen=True)
class SourceLine:
    number: int
    indent: int
    text: str


_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]+(.*))?$")
_PLACEHOLDER_RE = re.compile(
    r"(?:^|[\s|])(?:TBD|TODO)(?:$|[\s|])|待确认|待定|待补充|待实现|待验证|"
    r"<[^>\n]+>|\[(?:[^\]\n]*(?:待|TBD|TODO)[^\]\n]*)\]",
    re.IGNORECASE,
)
_DESCRIPTION_ELEMENTS = (
    "function",
    "scenario",
    "effect",
    "similarAPIs",
    "defaultBehavior",
    "constraints",
    "activation",
    "notes",
)
_DESCRIPTION_LABEL_RE = re.compile(
    r"^(?:function|scenario|effect|similar\s*APIs|default\s*behavior|"
    r"constraints|activation|notes|功能|含义|使用场景|使用效果|相似\s*API|"
    r"默认行为|约束|生效条件|注意事项)\s*[:：]",
    re.IGNORECASE,
)
_VERSION_ONLY_NOTES_RE = re.compile(
    r"^(?:(?:available|supported)\s+since\s+[0-9][\w.+-]*|"
    r"since\s+[0-9][\w.+-]*|"
    r"自\s*[0-9][\w.+-]*\s*(?:起可用|起支持)|"
    r"从\s*[0-9][\w.+-]*\s*(?:开始)?(?:可用|支持))"
    r"\s*[.。]?$",
    re.IGNORECASE,
)
_STRUCTURED_FACT_OWNER_FIELDS = {"deviceDifferences"}

_STRUCTURAL_FACT_NAMES = {
    "since", "syscap", "permission", "permissions", "platform",
    "applicationmodel", "application-model", "kit", "library",
    "declaration", "parameter-type", "return-type", "error-code",
    "errorcode",
}


def _strip_comment(raw: str) -> str:
    quote: str | None = None
    escaped = False
    for index, char in enumerate(raw):
        if quote is not None:
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
            return raw[:index].rstrip()
    return raw.rstrip()


def _scalar(value: str, line: SourceLine) -> Any:
    text = value.strip()
    if not text:
        return None
    if text == "[]":
        return []
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
        try:
            return parse_yaml_scalar(text)
        except YamlScalarError as error:
            raise SimpleYamlError(
                f"line {line.number}: invalid quoted scalar: {text}"
            ) from error
    if text in {"null", "Null", "NULL"}:
        return None
    if text in {"true", "True"}:
        return True
    if text in {"false", "False"}:
        return False
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return text


def _load_lines(path: Path) -> list[SourceLine]:
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise SimpleYamlError(f"cannot read {path}: {error}") from error

    result: list[SourceLine] = []
    for number, raw in enumerate(raw_lines, start=1):
        line = _strip_comment(raw)
        if not line.strip() or line.strip() in {"---", "..."}:
            continue
        stripped = line.lstrip(" ")
        if not stripped:
            continue
        if line[: len(line) - len(stripped)].strip():
            raise SimpleYamlError(f"line {number}: tabs are not supported in indentation")
        result.append(SourceLine(number, len(line) - len(stripped), stripped))
    return result


def _parse_mapping(
    lines: list[SourceLine],
    index: int,
    indent: int,
    path: str,
    first_line: SourceLine | None = None,
) -> tuple[dict[str, Any], int]:
    result: dict[str, Any] = {}
    pending: SourceLine | None = first_line
    while True:
        if pending is not None:
            line = pending
            pending = None
        else:
            if index >= len(lines):
                break
            line = lines[index]
            if line.indent < indent:
                break
            if line.indent > indent:
                raise SimpleYamlError(
                    f"{path}: line {line.number}: unexpected indentation {line.indent}; expected {indent}"
                )
            index += 1

        match = _KEY_RE.match(line.text)
        if match is None:
            raise SimpleYamlError(
                f"{path}: line {line.number}: expected 'key: value', got '{line.text}'"
            )
        key, value = match.group(1), match.group(2)
        if key in result:
            raise SimpleYamlError(f"{path}: line {line.number}: duplicate key '{key}'")

        if value is not None and value.strip():
            result[key] = _scalar(value, line)
            continue

        if index < len(lines) and lines[index].indent > indent:
            child_indent = lines[index].indent
            if lines[index].text.startswith("- ") and child_indent == indent + 2:
                result[key], index = _parse_sequence(
                    lines, index, child_indent, path
                )
            else:
                result[key], index = _parse_block(
                    lines, index, child_indent, path
                )
        else:
            result[key] = None
    return result, index


def _parse_sequence(
    lines: list[SourceLine], index: int, indent: int, path: str
) -> tuple[list[Any], int]:
    result: list[Any] = []
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise SimpleYamlError(
                f"{path}: line {line.number}: unexpected indentation {line.indent}; expected {indent}"
            )
        if not (line.text == "-" or line.text.startswith("- ")):
            raise SimpleYamlError(
                f"{path}: line {line.number}: expected sequence item, got '{line.text}'"
            )

        content = line.text[1:].strip()
        index += 1
        if not content:
            if index < len(lines) and lines[index].indent > indent:
                value, index = _parse_block(
                    lines, index, lines[index].indent, path
                )
                result.append(value)
            else:
                result.append(None)
            continue

        if _KEY_RE.match(content):
            virtual = SourceLine(line.number, indent + 2, content)
            item, index = _parse_mapping(
                lines, index, indent + 2, path, first_line=virtual
            )
            result.append(item)
        else:
            result.append(_scalar(content, line))
    return result, index


def _parse_block(
    lines: list[SourceLine], index: int, indent: int, path: str
) -> tuple[Any, int]:
    if index >= len(lines):
        return None, index
    line = lines[index]
    if line.indent != indent:
        raise SimpleYamlError(
            f"{path}: line {line.number}: unexpected indentation {line.indent}; expected {indent}"
        )
    if line.text == "-" or line.text.startswith("- "):
        return _parse_sequence(lines, index, indent, path)
    return _parse_mapping(lines, index, indent, path)


def parse_constrained_yaml(path: Path) -> dict[str, Any]:
    lines = _load_lines(path)
    if not lines:
        return {}
    if lines[0].indent != 0:
        raise SimpleYamlError(f"{path}: line {lines[0].number}: document must start at indent 0")
    value, index = _parse_block(lines, 0, 0, str(path))
    if index != len(lines):
        raise SimpleYamlError(
            f"{path}: line {lines[index].number}: unexpected top-level content"
        )
    if not isinstance(value, dict):
        raise SimpleYamlError(f"{path}: top-level value must be a mapping")
    return value


def _text(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return ""
    return str(value).strip()


def _normalized(value: Any) -> str:
    return " ".join(_text(value).split())


def _tokens(value: Any) -> list[str]:
    text = _normalized(value).casefold()
    tokens = re.findall(r"[A-Za-z0-9_]+|\s+|[\u3400-\u9fff\uf900-\ufaff]", text)
    # Keep CJK as characters and ASCII words as tokens; drop separators.
    return [token for token in tokens if not token.isspace()]


def _longest_common_run(left: list[str], right: list[str]) -> int:
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


def _description_values(api: dict[str, Any], language: str) -> list[tuple[str, str]]:
    description = api.get("description")
    if not isinstance(description, dict):
        return []
    values = description.get(language)
    if not isinstance(values, dict):
        return []
    return [
        (str(element), str(value))
        for element, value in values.items()
        if isinstance(value, str) and _meaningful(value)
    ]


def _tag_values(api: dict[str, Any], language: str) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    parameters = api.get("parameters")
    if isinstance(parameters, list):
        for parameter in parameters:
            if not isinstance(parameter, dict):
                continue
            descriptions = parameter.get("description")
            if isinstance(descriptions, dict):
                value = descriptions.get(language)
                if isinstance(value, str) and _meaningful(value):
                    name = str(parameter.get("name") or "<parameter>")
                    result.append((f"parameter {name}", value))
    return_type = api.get("returnType")
    if isinstance(return_type, dict):
        descriptions = return_type.get("description")
        if isinstance(descriptions, dict):
            value = descriptions.get(language)
            if isinstance(value, str) and _meaningful(value):
                result.append(("returnType", value))
    return result




def _contains_normalized_value(text: str, value: str) -> bool:
    """Match a scalar with language-aware boundaries.

    Python `\w` includes CJK characters, so the generic negative lookarounds
    reject natural Chinese prose. ASCII-like values use word boundaries; values
    containing CJK characters are matched as exact substrings in normalized
    text, where punctuation and whitespace already delimit the phrase.
    """

    if not value:
        return True
    if re.search(r"[\u3400-\u9fff\uf900-\ufaff]", value):
        # CJK values are checked as normalized literals. re.escape() would turn
        # spaces and ASCII punctuation into backslash sequences and break a
        # literal containment check even when the documentation is correct.
        return value in text
    escaped = re.escape(value)
    if re.fullmatch(r"[A-Za-z0-9_]+", value):
        # CJK characters are not identifier word-characters for this boundary.
        # This accepts “限额为100。” while still rejects 100 inside 1000.
        return re.search(
            rf"(?<![A-Za-z0-9_]){escaped}(?![A-Za-z0-9_])", text
        ) is not None
    return re.search(rf"(?<!\w){escaped}(?!\w)", text, flags=re.UNICODE) is not None


def _duplicated_documentation_issues(api: dict[str, Any], label: str) -> list[str]:
    if not DOCUMENT_STYLE_DUPLICATION_ENABLED:
        return []
    issues: list[str] = []
    for language in ("en", "zh"):
        descriptions = _description_values(api, language)
        tags = _tag_values(api, language)
        threshold = DOCUMENT_STYLE_DUPLICATION_MIN_TOKENS.get(language, 8)
        for element, description_value in descriptions:
            description_tokens = _tokens(description_value)
            for tag_name, tag_value in tags:
                common = _longest_common_run(description_tokens, _tokens(tag_value))
                if common >= threshold:
                    issues.append(
                        f"{label}: {language} documentation duplicates "
                        f"{threshold}-or-more-token clause between description.{element} "
                        f"and {tag_name}"
                    )
    return issues


def _meaningful(value: Any) -> bool:
    text = _normalized(value)
    return bool(text) and not _PLACEHOLDER_RE.search(text)


def _string_list(value: Any, field: str, path: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{path}: {field} must be a non-empty list of strings")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not _meaningful(item):
            raise ValueError(f"{path}: {field} entries must be non-empty strings")
        if item in result:
            raise ValueError(f"{path}: {field} contains duplicate item '{item}'")
        result.append(item)
    return result


def _mapping_list(value: Any, field: str, path: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValueError(f"{path}: {field} must be a list")
    result: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError(f"{path}: {field} entries must be mappings")
        result.append(item)
    return result


def _required_string(mapping: dict[str, Any], key: str, label: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not _meaningful(value):
        raise ValueError(f"{label} requires a non-empty, resolved {key}")
    return value


def _validate_context(
    path: Path,
) -> tuple[
        list[str],
        list[dict[str, Any]],
        list[dict[str, Any]],
        dict[str, list[dict[str, Any]]],
    ]:
    data = parse_constrained_yaml(path)
    if data.get("schemaVersion") != "1.0.0":
        raise ValueError(f"{path}: schemaVersion must be 1.0.0")

    api_ids = _string_list(data.get("apiIds"), "apiIds", str(path))
    structured_facts: dict[str, list[dict[str, Any]]] = {}
    api_id_set = set(api_ids)

    facts = _mapping_list(data.get("confirmedFacts"), "confirmedFacts", str(path))
    for index, fact in enumerate(facts, start=1):
        label = f"{path}: confirmedFacts[{index}]"
        api_id = _required_string(fact, "apiId", label)
        fact_name = _required_string(fact, "fact", label)
        _required_string(fact, "source", label)
        normalized_fact = fact_name.casefold().replace("_", "-").replace(" ", "-")
        if normalized_fact in _STRUCTURAL_FACT_NAMES:
            raise ValueError(
                f"{label}: structural contract fact '{fact_name}' belongs in the "
                "API skeleton, not documentation-context.yaml"
            )
        if api_id not in api_id_set:
            raise ValueError(f"{label}: apiId '{api_id}' is not declared in apiIds")
        owner_field = fact.get("ownerField")
        if owner_field is not None and not isinstance(owner_field, str):
            raise ValueError(f"{label}: ownerField must be a string")
        if owner_field is not None and owner_field not in _STRUCTURED_FACT_OWNER_FIELDS:
            raise ValueError(
                f"{label}: unsupported structured ownerField '{owner_field}'"
            )
        values = fact.get("values")
        if not isinstance(values, dict):
            raise ValueError(f"{label}: values must be a mapping")
        for language in ("en", "zh"):
            value = values.get(language)
            if not isinstance(value, (str, int, float, bool)):
                raise ValueError(f"{label}: values.{language} must be a scalar")
            if not _meaningful(value):
                raise ValueError(
                    f"{label}: values.{language} must be non-empty and resolved"
                )
        if set(values) != {"en", "zh"}:
            raise ValueError(f"{label}: values must contain exactly en and zh")
        if any(
            other is not fact
            and other.get("apiId") == api_id
            and other.get("fact") == fact_name
            for other in facts
        ):
            raise ValueError(
                f"{label}: duplicate fact '{fact_name}' for API '{api_id}'"
            )

    requirements = _mapping_list(
        data.get("documentationRequirements"), "documentationRequirements", str(path)
    )
    fact_keys = {
        (fact.get("apiId"), fact.get("fact")) for fact in facts if isinstance(fact, dict)
    }
    for index, requirement in enumerate(requirements, start=1):
        label = f"{path}: documentationRequirements[{index}]"
        api_id = _required_string(requirement, "apiId", label)
        fact_name = _required_string(requirement, "fact", label)
        _required_string(requirement, "requirement", label)
        if api_id not in api_id_set:
            raise ValueError(f"{label}: api_id '{api_id}' is not declared in apiIds")
        if (api_id, fact_name) not in fact_keys:
            raise ValueError(
                f"{label}: no confirmed fact '{fact_name}' for API '{api_id}'"
            )

    missing_requirements = sorted(fact_keys - {
        (item.get("apiId"), item.get("fact"))
        for item in requirements
        if isinstance(item, dict)
    })
    if missing_requirements:
        api, fact = missing_requirements[0]
        raise ValueError(
            f"{path}: confirmed fact '{fact}' for API '{api}' has no documentationRequirement"
        )

    for fact in facts:
        owner_field = fact.get("ownerField")
        if owner_field in _STRUCTURED_FACT_OWNER_FIELDS:
            structured_facts.setdefault(str(fact.get("apiId")), []).append(fact)

    return api_ids, facts, requirements, structured_facts


def _validate_documentation_fields(
    api: dict[str, Any], label: str
) -> list[str]:
    issues: list[str] = []

    description = api.get("description")
    if not isinstance(description, dict):
        return [f"{label}: missing description"]
    for language in ("en", "zh"):
        values = description.get(language)
        if not isinstance(values, dict):
            issues.append(f"{label}: missing description.{language}")
            continue
        for element in _DESCRIPTION_ELEMENTS:
            value = values.get(element)
            if not isinstance(value, str) or not _meaningful(value):
                issues.append(
                    f"{label}: missing or unresolved description.{language}.{element}"
                )
                continue
            if _DESCRIPTION_LABEL_RE.match(value):
                issues.append(
                    f"{label}: description.{language}.{element} must be plain prose "
                    "without an element-name label"
                )
            if element == "notes" and _VERSION_ONLY_NOTES_RE.fullmatch(value):
                issues.append(
                    f"{label}: description.{language}.notes must not restate API "
                    "availability; use the structured since field and @since marker"
                )

    parameters = api.get("parameters")
    if parameters is None or parameters == []:
        parameters = []
    if not isinstance(parameters, list):
        issues.append(f"{label}: parameters must be a list when present")
        parameters = []
    names: set[str] = set()
    for index, parameter in enumerate(parameters, start=1):
        if not isinstance(parameter, dict):
            issues.append(f"{label}: parameters[{index}] must be a mapping")
            continue
        name = parameter.get("name")
        if not isinstance(name, str) or not _meaningful(name):
            issues.append(f"{label}: parameters[{index}].name must be a non-empty string")
        elif name in names:
            issues.append(f"{label}: duplicate parameter name '{name}'")
        else:
            names.add(name)
        descriptions = parameter.get("description")
        if not isinstance(descriptions, dict):
            issues.append(f"{label}: parameters[{index}].description must contain en and zh")
            continue
        for language in ("en", "zh"):
            value = descriptions.get(language)
            if not isinstance(value, str) or not _meaningful(value):
                issues.append(
                    f"{label}: parameters[{index}].description.{language} is missing or unresolved"
                )

    return_type = api.get("returnType")
    if return_type not in (None, []):
        if not isinstance(return_type, dict):
            issues.append(f"{label}: returnType must be a mapping when present")
        else:
            descriptions = return_type.get("description")
            if not isinstance(descriptions, dict):
                issues.append(f"{label}: returnType.description must contain en and zh")
            else:
                for language in ("en", "zh"):
                    value = descriptions.get(language)
                    if not isinstance(value, str) or not _meaningful(value):
                        issues.append(
                            f"{label}: returnType.description.{language} is missing or unresolved"
                        )

    error_codes = api.get("errorCodes")
    if error_codes is None or error_codes == []:
        error_codes = []
    if not isinstance(error_codes, list):
        issues.append(f"{label}: errorCodes must be a list when present")
        error_codes = []
    codes: set[Any] = set()
    for index, error_code in enumerate(error_codes, start=1):
        if not isinstance(error_code, dict):
            issues.append(f"{label}: errorCodes[{index}] must be a mapping")
            continue
        code = error_code.get("code")
        if not isinstance(code, (str, int, float, bool)) or not _meaningful(code):
            issues.append(
                f"{label}: errorCodes[{index}].code must be a non-empty scalar"
            )
        elif code in codes:
            issues.append(f"{label}: duplicate error code '{code}'")
        else:
            codes.add(code)
        descriptions = error_code.get("description")
        if not isinstance(descriptions, dict):
            issues.append(f"{label}: errorCodes[{index}].description must contain en and zh")
            continue
        for language in ("en", "zh"):
            value = descriptions.get(language)
            if not isinstance(value, str) or not _meaningful(value):
                issues.append(
                    f"{label}: errorCodes[{index}].description.{language} is missing or unresolved"
                )

    return issues


def _language_text(api: dict[str, Any], language: str) -> str:
    chunks: list[str] = []
    description = api.get("description")
    if isinstance(description, dict):
        values = description.get(language)
        if isinstance(values, dict):
            chunks.extend(_text(value) for value in values.values())

    parameters = api.get("parameters")
    if isinstance(parameters, list):
        for parameter in parameters:
            if not isinstance(parameter, dict):
                continue
            descriptions = parameter.get("description")
            if isinstance(descriptions, dict):
                chunks.append(_text(descriptions.get(language)))

    return_type = api.get("returnType")
    if isinstance(return_type, dict):
        descriptions = return_type.get("description")
        if isinstance(descriptions, dict):
            chunks.append(_text(descriptions.get(language)))

    error_codes = api.get("errorCodes")
    if isinstance(error_codes, list):
        for error_code in error_codes:
            if not isinstance(error_code, dict):
                continue
            descriptions = error_code.get("description")
            if isinstance(descriptions, dict):
                chunks.append(_text(descriptions.get(language)))

    return " ".join(chunks)


def _validate_output(
    path: Path,
    expected_api_ids: list[str],
    facts: list[dict[str, Any]],
    structured_facts: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    data = parse_constrained_yaml(path)
    issues: list[str] = []
    if data.get("schemaVersion") != "1.0.0":
        issues.append(f"{path}: schemaVersion must be 1.0.0")

    apis = data.get("apis")
    if not isinstance(apis, list) or not apis:
        raise ValueError(f"{path}: apis must be a non-empty list")

    by_id: dict[str, dict[str, Any]] = {}
    for index, api in enumerate(apis, start=1):
        label = f"{path}: apis[{index}]"
        if not isinstance(api, dict):
            issues.append(f"{label} must be a mapping")
            continue
        api_id = api.get("apiId")
        if not isinstance(api_id, str) or not _meaningful(api_id):
            issues.append(f"{label}: apiId must be a non-empty string")
            continue
        if api_id in by_id:
            issues.append(f"{path}: duplicate API ID '{api_id}'")
            continue
        by_id[api_id] = api
        label = f"{api_id} ({path})"
        issues.extend(_validate_documentation_fields(api, label))
        issues.extend(_duplicated_documentation_issues(api, label))
        issues.extend(api_documentation_style_issues(api, label))
        issues.extend(
            device_differences_restated_in_default_behavior(
                api, prefix=f"{label}: "
            )
        )

    expected = set(expected_api_ids)
    actual = set(by_id)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        issues.append(f"{path}: API IDs missing from output: {', '.join(missing)}")
    if extra:
        issues.append(f"{path}: extra API IDs in output: {', '.join(extra)}")

    for fact in facts:
        api_id = fact.get("apiId")
        fact_name = fact.get("fact")
        values = fact.get("values")
        api = by_id.get(api_id)
        if api is None or not isinstance(values, dict):
            continue
        if fact.get("ownerField") in _STRUCTURED_FACT_OWNER_FIELDS:
            continue
        for language in ("en", "zh"):
            value = _normalized(values.get(language))
            if not _contains_normalized_value(
                _normalized(_language_text(api, language)), value
            ):
                issues.append(
                    f"{path}: API '{api_id}' {language} documentation does not contain "
                    f"confirmed fact '{fact_name}' value '{value}'"
                )

    return by_id, issues


def _device_differences_text(api: dict[str, Any]) -> str:
    chunks: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            for item in value.values():
                collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, (str, int, float, bool)):
            chunks.append(str(value))

    collect(api.get("deviceDifferences"))
    return " ".join(chunks)


def _structured_device_fact_issues(
    skeleton: dict[str, dict[str, Any]],
    output: dict[str, dict[str, Any]],
    structured_facts: dict[str, list[dict[str, Any]]],
    path: Path,
) -> list[str]:
    issues: list[str] = []
    for api_id, api_facts in structured_facts.items():
        for fact in api_facts:
            values = fact.get("values")
            if not isinstance(values, dict):
                continue
            skeleton_api = skeleton.get(api_id)
            if skeleton_api is None:
                continue
            skeleton_text = _normalized(skeleton_api.get("deviceDifferencesText"))
            fact_name = fact.get("fact") or "device-difference"
            for language in ("en", "zh"):
                value = _normalized(values.get(language))
                if not _contains_normalized_value(skeleton_text, value):
                    issues.append(
                        f"{path}: API '{api_id}' {language} {fact_name} fact "
                        f"is not covered by skeleton deviceDifferences value '{value}'"
                    )
    return issues


def _skeleton_entry(api: dict[str, Any], label: str) -> dict[str, Any]:
    parameters = api.get("parameters")
    if not isinstance(parameters, list):
        parameters = []
    parameter_names = [
        str(parameter.get("name"))
        for parameter in parameters
        if isinstance(parameter, dict) and _meaningful(parameter.get("name"))
    ]
    error_codes = api.get("errorCodes")
    if not isinstance(error_codes, list):
        error_codes = []
    error_code_values = [
        str(error_code.get("code"))
        for error_code in error_codes
        if isinstance(error_code, dict) and _meaningful(error_code.get("code"))
    ]
    return_type = api.get("returnType")
    has_return_type = isinstance(return_type, dict) and bool(return_type)
    return {
        "apiId": str(api.get("id") or api.get("apiId") or ""),
        "parameters": parameter_names,
        "hasReturnType": has_return_type,
        "errorCodes": error_code_values,
        "label": label,
        "deviceDifferencesText": _device_differences_text(api),
        "deviceDifferencesItems": (
            api.get("deviceDifferences", {}).get("items", [])
            if isinstance(api.get("deviceDifferences"), dict)
            else []
        ),
    }


def _parse_skeleton(path: Path) -> dict[str, dict[str, Any]]:
    data = parse_constrained_yaml(path)
    apis = data.get("apis")
    if not isinstance(apis, list) or not apis:
        raise ValueError(f"{path}: apis must be a non-empty list")
    result: dict[str, dict[str, Any]] = {}
    for index, api in enumerate(apis, start=1):
        if not isinstance(api, dict):
            raise ValueError(f"{path}: apis[{index}] must be a mapping")
        entry = _skeleton_entry(api, f"apis[{index}] ({path})")
        api_id = entry["apiId"]
        if not _meaningful(api_id):
            raise ValueError(f"{path}: apis[{index}].id must be non-empty")
        if api_id in result:
            raise ValueError(f"{path}: duplicate API ID '{api_id}'")
        result[str(api_id)] = entry
    return result


def _skeleton_closure_issues(
    skeleton: dict[str, dict[str, Any]], output: dict[str, dict[str, Any]], path: Path
) -> list[str]:
    issues: list[str] = []
    for api_id, skeleton_entry in skeleton.items():
        output_api = output.get(api_id)
        if output_api is None:
            continue
        label = f"{api_id} ({path})"
        output_parameters = output_api.get("parameters")
        if not isinstance(output_parameters, list):
            output_parameters = []
        output_names = [
            str(parameter.get("name"))
            for parameter in output_parameters
            if isinstance(parameter, dict) and _meaningful(parameter.get("name"))
        ]
        expected_parameters = list(skeleton_entry["parameters"])
        if output_names != expected_parameters:
            issues.append(
                f"{label}: parameter names do not match skeleton: "
                f"expected {expected_parameters}, got {output_names}"
            )
        if bool(skeleton_entry["hasReturnType"]):
            output_return = output_api.get("returnType")
            if not isinstance(output_return, dict):
                issues.append(
                    f"{label}: returnType documentation block missing from output"
                )
            else:
                descriptions = output_return.get("description")
                if not isinstance(descriptions, dict):
                    issues.append(
                        f"{label}: returnType.description must contain en and zh"
                    )
                else:
                    for language in ("en", "zh"):
                        value = descriptions.get(language)
                        if not isinstance(value, str) or not _meaningful(value):
                            issues.append(
                                f"{label}: returnType.description.{language} is missing or unresolved"
                            )
        expected_errors = [str(value) for value in skeleton_entry["errorCodes"]]
        output_errors_raw = output_api.get("errorCodes")
        if not isinstance(output_errors_raw, list):
            output_errors_raw = []
        output_errors = [
            str(error_code.get("code"))
            for error_code in output_errors_raw
            if isinstance(error_code, dict) and _meaningful(error_code.get("code"))
        ]
        if output_errors != expected_errors:
            issues.append(
                f"{label}: errorCodes identity does not match skeleton: "
                f"expected {expected_errors}, got {output_errors}"
            )
    return issues


def run(
    context_path: Path,
    output_path: Path,
    skeleton_path: Path,
) -> tuple[int, str]:
    try:
        api_ids, facts, _requirements, structured_facts = _validate_context(
            context_path
        )
        by_id, issues = _validate_output(
            output_path, api_ids, facts, structured_facts
        )
        skeleton = _parse_skeleton(skeleton_path)
        missing = sorted(set(skeleton) - set(by_id))
        extra = sorted(set(by_id) - set(skeleton))
        if missing:
            issues.append(
                f"{output_path}: API IDs missing from output: {', '.join(missing)}"
            )
        if extra:
            issues.append(
                f"{output_path}: API IDs not declared in skeleton: {', '.join(extra)}"
            )
        issues.extend(_skeleton_closure_issues(skeleton, by_id, output_path))
        issues.extend(
            _structured_device_fact_issues(
                skeleton, by_id, structured_facts, output_path
            )
        )
        for api_id, skeleton_api in skeleton.items():
            output_api = by_id.get(api_id)
            if not isinstance(output_api, dict):
                continue
            # The output normally omits contract fields; combine the skeleton's
            # structured differences with output prose for duplication checks.
            combined = dict(output_api)
            combined["deviceDifferences"] = {
                "enabled": True,
                "items": skeleton_api.get("deviceDifferencesItems", []),
            }
            issues.extend(
                device_differences_restated_in_default_behavior(
                    combined, prefix=f"{api_id} ({output_path}): "
                )
            )
    except (ValueError, SimpleYamlError) as error:
        return 1, f"error: {error}\n"

    if issues:
        return 1, "error:\n" + "\n".join(f"- {issue}" for issue in issues) + "\n"
    return 0, "PASS: API documentation output matches the context API set, covers all confirmed facts, closes against the skeleton, and contains no forbidden documentation terms\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", required=True, help="documentation-context.yaml")
    parser.add_argument("--output", required=True, help="api-doc-output.yaml")
    parser.add_argument(
        "--skeleton",
        required=True,
        help="language-specific API skeleton used to enforce documentation closure",
    )
    args = parser.parse_args(argv)
    status, message = run(
        Path(args.context), Path(args.output), Path(args.skeleton)
    )
    print(message, end="")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
