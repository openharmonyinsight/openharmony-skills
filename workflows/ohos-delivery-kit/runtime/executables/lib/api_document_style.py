"""Shared API documentation style rules for process and archive gates."""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")
_CJK_ASCII_SPACE_RE = re.compile(
    r"[\u3400-\u9fff\uf900-\ufaff][ ]+[A-Za-z0-9]"
    r"|[A-Za-z0-9][ ]+[\u3400-\u9fff\uf900-\ufaff]"
)
_CJK_ASCII_ADJACENT_RE = re.compile(
    r"[\u3400-\u9fff\uf900-\ufaff][A-Za-z0-9]"
    r"|[A-Za-z0-9][\u3400-\u9fff\uf900-\ufaff]"
)
_FORBIDDEN_TERMS_RELATIVE_PATH = "contracts/api/forbidden-terms.yaml"
_DOCUMENT_STYLE_RELATIVE_PATH = "contracts/api/document-style.yaml"
_SEMANTIC_VERSION_RE = re.compile(
    r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)$"
)
_PLACEHOLDER_RE = re.compile(
    r"(?:^|[\s|])(?:TBD|TODO)(?:$|[\s|])|待确认|待定|待补充|待实现|待验证|"
    r"<[^>\n]+>|\[(?:[^\]\n]*(?:待|TBD|TODO)[^\]\n]*)\]",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ApiDocumentStyle:
    """The active machine-readable API documentation style contract."""

    forbidden_terms: tuple[str, ...]
    chinese_english_spacing: bool
    document_style_ruleset_version: str
    forbidden_terms_ruleset_version: str
    source_of_truth: str
    duplication_enabled: bool
    duplication_min_tokens: dict[str, int]


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


class YamlScalarError(ValueError):
    """A constrained quoted YAML scalar could not be decoded."""


def parse_yaml_scalar(text: str) -> Any:
    """Decode the quoted YAML scalar forms supported by API contracts.

    Both process and archive validators use this function so a metadata value
    has one meaning regardless of which gate reads it.
    """
    value = text.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError as error:
            raise YamlScalarError(f"invalid double-quoted scalar: {value}") from error
        if not isinstance(decoded, str):
            raise YamlScalarError(f"quoted YAML scalar must decode to a string: {value}")
        return decoded
    raise YamlScalarError(f"not a quoted scalar: {value}")


def _scalar(value: str) -> Any:
    text = value.strip()
    if not text:
        return None
    if len(text) >= 2 and text[0] == text[-1] and text[0] == "'":
        return text[1:-1]
    if len(text) >= 2 and text.startswith('"') and text.endswith('"'):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if text in {"null", "Null", "NULL"}:
        return None
    if text in {"true", "True"}:
        return True
    if text in {"false", "False"}:
        return False
    return text


def _parse_style_contract(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    in_terms = False
    terms: list[Any] = []
    in_duplication = False
    in_min_tokens = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = _strip_comment(raw)
        if not line.strip():
            continue
        top_level = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", line)
        if top_level:
            key, value = top_level.groups()
            data[key] = _scalar(value)
            in_terms = key == "terms" and value.strip() == ""
            in_duplication = key == "duplication" and value.strip() == ""
            in_min_tokens = False
            if in_duplication:
                data["duplication"] = {}
            continue
        if in_terms:
            item = re.fullmatch(r"\s+-\s+(.*)", line)
            if item:
                terms.append(_scalar(item.group(1)))
                continue
        if in_min_tokens:
            nested = re.fullmatch(r"\s{4}([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", line)
            if nested:
                data["duplication"]["minTokens"][nested.group(1)] = _scalar(
                    nested.group(2)
                )
                continue
        if in_duplication:
            nested = re.fullmatch(r"\s{2}([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)", line)
            if nested:
                key, value = nested.groups()
                if key == "minTokens" and value.strip() == "":
                    data["duplication"]["minTokens"] = {}
                    in_min_tokens = True
                    continue
                data["duplication"][key] = _scalar(value)
                continue
        raise ValueError(f"{path}: unsupported API style syntax: {line.strip()}")
    if terms:
        data["terms"] = terms
    return data


def _root() -> Path:
    # Source: scripts/lib/api_document_style.py -> repository root.
    # Installed: runtime/executables/lib/api_document_style.py -> runtime root.
    return Path(__file__).resolve().parents[2]


def load_api_document_style(root: Path | None = None) -> ApiDocumentStyle:
    base = root or _root()
    candidates = (
        base / "core" / _FORBIDDEN_TERMS_RELATIVE_PATH,
        base / "runtime" / "assets" / _FORBIDDEN_TERMS_RELATIVE_PATH,
        base / "assets" / _FORBIDDEN_TERMS_RELATIVE_PATH,
    )
    terms_path = next((candidate for candidate in candidates if candidate.is_file()), None)
    if terms_path is None:
        raise ValueError(
            "API documentation forbidden terms file is missing; expected one of: "
            + ", ".join(str(candidate) for candidate in candidates)
        )
    terms_data = _parse_style_contract(terms_path)
    if terms_data.get("schemaVersion") != "1.0.0":
        raise ValueError(f"{terms_path}: schemaVersion must be 1.0.0")
    terms_ruleset_version = terms_data.get("rulesetVersion")
    if (
        not isinstance(terms_ruleset_version, str)
        or _SEMANTIC_VERSION_RE.fullmatch(terms_ruleset_version) is None
    ):
        raise ValueError(
            f"{terms_path}: rulesetVersion must be MAJOR.MINOR.PATCH"
        )
    source_of_truth = terms_data.get("sourceOfTruth")
    if not isinstance(source_of_truth, str) or not source_of_truth.strip():
        raise ValueError(f"{terms_path}: sourceOfTruth must be a non-empty string")
    terms = terms_data.get("terms")
    if not isinstance(terms, list) or not terms:
        raise ValueError(f"{terms_path}: terms must be a non-empty list")
    normalized_terms: list[str] = []
    for term in terms:
        if not isinstance(term, str) or not term.strip():
            raise ValueError(f"{terms_path}: terms entries must be non-empty strings")
        normalized_terms.append(term)

    candidates = (
        base / "core" / _DOCUMENT_STYLE_RELATIVE_PATH,
        base / "runtime" / "assets" / _DOCUMENT_STYLE_RELATIVE_PATH,
        base / "assets" / _DOCUMENT_STYLE_RELATIVE_PATH,
    )
    style_path = next((candidate for candidate in candidates if candidate.is_file()), None)
    if style_path is None:
        raise ValueError(
            "API document style file is missing; expected one of: "
            + ", ".join(str(candidate) for candidate in candidates)
        )
    style_data = _parse_style_contract(style_path)
    if style_data.get("schemaVersion") != "1.0.0":
        raise ValueError(f"{style_path}: schemaVersion must be 1.0.0")
    style_ruleset_version = style_data.get("rulesetVersion")
    if (
        not isinstance(style_ruleset_version, str)
        or _SEMANTIC_VERSION_RE.fullmatch(style_ruleset_version) is None
    ):
        raise ValueError(
            f"{style_path}: rulesetVersion must be MAJOR.MINOR.PATCH"
        )
    style_source = style_data.get("sourceOfTruth")
    if not isinstance(style_source, str) or not style_source.strip():
        raise ValueError(f"{style_path}: sourceOfTruth must be a non-empty string")
    if style_source != source_of_truth:
        raise ValueError(
            f"{style_path}: sourceOfTruth must match {terms_path}: {source_of_truth}"
        )
    spacing = style_data.get("chineseEnglishSpacing")
    if not isinstance(spacing, bool):
        raise ValueError(
            f"{style_path}: chineseEnglishSpacing must be a boolean (false or true)"
        )
    duplication = style_data.get("duplication")
    if not isinstance(duplication, dict):
        raise ValueError(f"{style_path}: duplication block is missing")
    duplication_enabled = duplication.get("enabled")
    if not isinstance(duplication_enabled, bool):
        raise ValueError(f"{style_path}: duplication.enabled must be a boolean")
    min_tokens = duplication.get("minTokens")
    if not isinstance(min_tokens, dict):
        raise ValueError(f"{style_path}: duplication.minTokens block is missing")
    normalized_min_tokens: dict[str, int] = {}
    for language in ("en", "zh"):
        value = min_tokens.get(language)
        if not isinstance(value, int) or isinstance(value, bool) or value < 2:
            raise ValueError(
                f"{style_path}: duplication.minTokens.{language} "
                "must be an integer of at least 2"
            )
        normalized_min_tokens[language] = value
    return ApiDocumentStyle(
        tuple(normalized_terms),
        spacing,
        str(style_ruleset_version),
        str(terms_ruleset_version),
        source_of_truth,
        duplication_enabled,
        normalized_min_tokens,
    )


DEFAULT_API_DOCUMENT_STYLE = load_api_document_style()
FORBIDDEN_DOCUMENTATION_TERMS = DEFAULT_API_DOCUMENT_STYLE.forbidden_terms
DOCUMENT_STYLE_CHINESE_ENGLISH_SPACING = (
    DEFAULT_API_DOCUMENT_STYLE.chinese_english_spacing
)
DOCUMENT_STYLE_RULESET_VERSION = (
    DEFAULT_API_DOCUMENT_STYLE.document_style_ruleset_version
)
FORBIDDEN_TERMS_RULESET_VERSION = (
    DEFAULT_API_DOCUMENT_STYLE.forbidden_terms_ruleset_version
)
DOCUMENT_STYLE_SOURCE_OF_TRUTH = DEFAULT_API_DOCUMENT_STYLE.source_of_truth
DOCUMENT_STYLE_DUPLICATION_ENABLED = (
    DEFAULT_API_DOCUMENT_STYLE.duplication_enabled
)
DOCUMENT_STYLE_DUPLICATION_MIN_TOKENS = dict(
    DEFAULT_API_DOCUMENT_STYLE.duplication_min_tokens
)


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


def _meaningful(value: Any) -> bool:
    text = _normalized(value)
    return bool(text) and not _PLACEHOLDER_RE.search(text)


def contains_forbidden_term(text: str, term: str) -> bool:
    normalized = _normalized(text).casefold()
    target = term.casefold()
    if _CJK_RE.search(target):
        return target in normalized
    return re.search(
        rf"(?<![A-Za-z0-9_]){re.escape(target)}(?![A-Za-z0-9_])",
        normalized,
    ) is not None


def chinese_english_spacing_issue(value: Any, enabled: bool) -> str | None:
    text = _normalized(value)
    if not _CJK_RE.search(text):
        return None
    pattern = _CJK_ASCII_ADJACENT_RE if enabled else _CJK_ASCII_SPACE_RE
    if pattern.search(text):
        if enabled:
            return "must place one space between Chinese and ASCII text (chineseEnglishSpacing=true)"
        return "must not place whitespace between Chinese and ASCII text (chineseEnglishSpacing=false)"
    return None


def text_style_issues(
    value: Any,
    label: str,
    field: str,
    style: ApiDocumentStyle = DEFAULT_API_DOCUMENT_STYLE,
) -> list[str]:
    """Apply forbidden-term and spacing rules to one documentation value."""

    if not isinstance(value, str) or not _meaningful(value):
        return []
    issues: list[str] = []
    for term in style.forbidden_terms:
        if contains_forbidden_term(value, term):
            issues.append(
                f"{label}: {field} contains forbidden documentation term '{term}'"
            )
    spacing_issue = chinese_english_spacing_issue(
        value, style.chinese_english_spacing
    )
    if spacing_issue:
        issues.append(f"{label}: {field} {spacing_issue}")
    return issues



def _device_differences_text(api: dict[str, Any]) -> str:
    differences = api.get("deviceDifferences")
    if not isinstance(differences, dict):
        return ""
    chunks: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            for item in value.values():
                collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, (str, int, float, bool)):
            chunks.append(_text(value))

    collect(differences)
    return " ".join(chunks)


def _compact_behavior_text(value: Any) -> str:
    """Normalize prose for conservative containment and near-containment checks."""

    text = _normalized(value).casefold()
    return re.sub(r"\W+", "", text, flags=re.UNICODE)


def _restates_device_behavior(source: str, target: str) -> bool:
    """Return whether target repeats a device-specific behavior clause.

    Exact containment catches direct copies. A high source-coverage match with a
    long consecutive match catches small paraphrases while avoiding a loose
    bag-of-words match whose tokens merely appear in unrelated prose.
    """

    source_text = _compact_behavior_text(source)
    target_text = _compact_behavior_text(target)
    if len(source_text) < 4 or not target_text:
        return False
    if source_text in target_text:
        return True
    matcher = SequenceMatcher(None, source_text, target_text, autojunk=False)
    matching_blocks = [block for block in matcher.get_matching_blocks() if block.size]
    if not matching_blocks:
        return False
    matched = sum(block.size for block in matching_blocks)
    longest = max(block.size for block in matching_blocks)
    return matched / len(source_text) >= 0.8 and longest / len(source_text) >= 0.5


def _api_documentation_fields(api: dict[str, Any]):
    """Yield human-facing API documentation fields with stable labels."""

    description = api.get("description")
    if isinstance(description, dict):
        for language, values in description.items():
            if not isinstance(values, dict):
                continue
            for element, value in values.items():
                yield f"description.{language}.{element}", value

    parameters = api.get("parameters")
    if isinstance(parameters, list):
        for index, parameter in enumerate(parameters, start=1):
            if not isinstance(parameter, dict):
                continue
            values = parameter.get("description")
            if isinstance(values, dict):
                for language, value in values.items():
                    yield f"parameters[{index}].description.{language}", value

    for field, owner in (
        ("returnType", "returnType"),
        ("errorCodes", "errorCodes"),
    ):
        value = api.get(field)
        if not isinstance(value, dict):
            if not isinstance(value, list):
                continue
            for index, item in enumerate(value, start=1):
                if not isinstance(item, dict):
                    continue
                values = item.get("description")
                if not isinstance(values, dict):
                    continue
                for language, description in values.items():
                    yield f"{owner}[{index}].description.{language}", description
            continue
        values = value.get("description")
        if isinstance(values, dict):
            for language, description in values.items():
                yield f"{owner}.description.{language}", description


def device_differences_restated_in_default_behavior(
    api: dict[str, Any],
    prefix: str = "",
) -> list[str]:
    """Reject per-device behavior duplicated in any API documentation field."""

    issues: list[str] = []
    differences = api.get("deviceDifferences")
    if not isinstance(differences, dict) or differences.get("enabled") is not True:
        return issues

    items = differences.get("items")
    if not isinstance(items, list):
        return issues

    # diffDescription and diffPerformanceDesc own the behavior. diffReason is a
    # source rationale rather than behavior, so it is intentionally excluded.
    behavior_texts: set[str] = set()
    device_specific_values: set[str] = set()
    device_names: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            continue
        performance = item.get("diffPerformance")
        if performance not in {"IMPLEMENT_DIFF", "FUNCTION_DIFF"}:
            continue
        device = _normalized(item.get("deviceModelName"))
        if device:
            device_names.add(device.casefold())
        for key in ("diffDescription", "diffPerformanceDesc", "zhDiffDescription"):
            value = _normalized(item.get(key))
            if not value:
                continue
            behavior_texts.add(value)
            for token in re.findall(r"[0-9]+(?:[.][0-9]+)?", value):
                device_specific_values.add(token)

    for field, value in _api_documentation_fields(api):
        if not _meaningful(value):
            continue
        normalized = _normalized(value).casefold()
        duplicated_behavior = any(
            _restates_device_behavior(behavior, normalized)
            for behavior in behavior_texts
        )
        duplicated_numbers = sorted(
            number for number in device_specific_values
            if re.search(rf"(?<![0-9.]){re.escape(number)}(?![0-9.])", normalized)
        )
        duplicated_devices = sorted(
            name for name in device_names if name in normalized
        )
        if duplicated_behavior or (duplicated_numbers and duplicated_devices):
            issues.append(
                f"{prefix}{field} duplicates per-device values owned by "
                "deviceDifferences; use N/A / 不适用 unless a uniform value exists"
            )
    return issues

def api_documentation_style_issues(
    api: dict[str, Any],
    label: str,
    style: ApiDocumentStyle = DEFAULT_API_DOCUMENT_STYLE,
) -> list[str]:
    """Check all API documentation fields with the shared style rules."""

    issues: list[str] = []

    description = api.get("description")
    if isinstance(description, dict):
        for language, values in description.items():
            if not isinstance(values, dict):
                continue
            for element, value in values.items():
                issues.extend(
                    text_style_issues(
                        value, label, f"description.{language}.{element}", style
                    )
                )

    parameters = api.get("parameters")
    if isinstance(parameters, list):
        for parameter_index, parameter in enumerate(parameters, start=1):
            if not isinstance(parameter, dict):
                continue
            descriptions = parameter.get("description")
            if not isinstance(descriptions, dict):
                continue
            for language, value in descriptions.items():
                issues.extend(
                    text_style_issues(
                        value,
                        label,
                        f"parameters[{parameter_index}].description.{language}",
                        style,
                    )
                )

    return_type = api.get("returnType")
    if isinstance(return_type, dict):
        descriptions = return_type.get("description")
        if isinstance(descriptions, dict):
            for language, value in descriptions.items():
                issues.extend(
                    text_style_issues(
                        value,
                        label,
                        f"returnType.description.{language}",
                        style,
                    )
                )

    error_codes = api.get("errorCodes")
    if isinstance(error_codes, list):
        for error_index, error_code in enumerate(error_codes, start=1):
            if not isinstance(error_code, dict):
                continue
            descriptions = error_code.get("description")
            if not isinstance(descriptions, dict):
                continue
            for language, value in descriptions.items():
                issues.extend(
                    text_style_issues(
                        value,
                        label,
                        f"errorCodes[{error_index}].description.{language}",
                        style,
                    )
                )

    return issues
