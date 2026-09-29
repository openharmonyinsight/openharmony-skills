"""Opaque API signature document checks, not C/ArkTS language validation."""
from __future__ import annotations

import re


# Explicit document markers, not arbitrary substrings of source identifiers.
_MARKER_WORDS = r"TODO|TBD|待定|待补充|待实现|待验证|待填写|完整签名|参数类型|返回类型"
_WHOLE_PLACEHOLDER = re.compile(
    rf"(?:{_MARKER_WORDS}|N/?A|[-—]+|\[限定名\(参数类型\):返回类型\])",
    re.IGNORECASE,
)
_SIGNATURE_TOKENS = re.compile(
    r"\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'"
    + rf"|(?P<marker>\[(?:{_MARKER_WORDS})\]|<(?:{_MARKER_WORDS})>)",
    re.IGNORECASE,
)


def api_signature_complete(
    signature: str, *, name_style: str = "qualified", language: str | None = None
) -> bool:
    """Check presence/placeholders only; keyword arguments retain compatibility."""
    normalized = canonical_api_signature(signature)
    return bool(normalized) and not (
        _WHOLE_PLACEHOLDER.fullmatch(normalized)
        or any(match.group('marker') for match in _SIGNATURE_TOKENS.finditer(normalized))
    )


def canonical_api_signature(signature: str) -> str:
    source = signature.strip().strip("`")
    punctuation = set("(),:;<>[]{}?|&=*")
    result: list[str] = []
    quote: str | None = None
    escaped = False
    index = 0
    while index < len(source):
        char = source[index]
        if quote is not None:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue
        if char in {'"', "'"}:
            quote = char
            result.append(char)
            index += 1
            continue
        if char.isspace():
            next_index = index + 1
            while next_index < len(source) and source[next_index].isspace():
                next_index += 1
            previous = result[-1] if result else ""
            following = source[next_index] if next_index < len(source) else ""
            if previous and following and previous not in punctuation and following not in punctuation:
                result.append(" ")
            index = next_index
            continue
        result.append(char)
        index += 1
    return "".join(result)
