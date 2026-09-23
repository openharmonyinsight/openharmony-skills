"""ODK Markdown extraction and legacy document placeholder policy.

Pure helpers: no contract loading, filesystem access, or language validation.
"""
from __future__ import annotations

import re


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


BRACKET_PLACEHOLDER_RE = re.compile(
    r"\[(?:[^\]\n]*(?:引用|标题|角色|功能|价值|条件|填写|描述|说明|编号|名称|路径|模块|文件|命令|证据|结果|对象|模式|策略|事件|待|TBD|TODO)[^\]\n]*)\]",
    re.IGNORECASE,
)


def _visible_markdown(text: str) -> str:
    """Remove template guidance and fenced examples from user evidence."""
    text = re.sub(r"<!--[\s\S]*?(?:-->|\Z)", "", text)
    lines = text.splitlines()
    visible: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    fence_indent: str | None = None
    for index, line in enumerate(lines):
        if fence_character is None:
            opening = re.match(r"^([ \t]*)(`{3,}|~{3,})", line)
            if opening:
                indent = opening.group(1)
                marker = opening.group(2)
                nested = len(indent.expandtabs(4)) > 3
                if nested:
                    close_pattern = re.compile(
                        rf"^{re.escape(indent)}{re.escape(marker[0])}{{{len(marker)},}}[ \t]*$"
                    )
                    if not any(close_pattern.match(candidate) for candidate in lines[index + 1 :]):
                        visible.append(line)
                        continue
                fence_character = marker[0]
                fence_length = len(marker)
                fence_indent = indent if nested else None
                visible.append("")
                continue
            visible.append(line)
            continue
        close_indent = re.escape(fence_indent) if fence_indent is not None else r"[ \t]{0,3}"
        if re.match(rf"^{close_indent}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$", line):
            fence_character = None
            fence_length = 0
            fence_indent = None
        visible.append("")
    return "\n".join(visible)


def atx_heading(line: str) -> tuple[int, str] | None:
    """Parse an ATX heading, including CommonMark indentation/closing hashes."""
    match = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+(.*)|[ \t]*)$", line)
    if not match:
        return None
    title = match.group(2) or ""
    title = re.sub(r"(?:^|[ \t]+)#+[ \t]*$", "", title).strip()
    return len(match.group(1)), title


def headings(text: str) -> set[str]:
    result: set[str] = set()
    for line in _visible_markdown(text).splitlines():
        match = atx_heading(line)
        if match:
            result.add(match[1])
    return result


def section_texts(text: str, title: str) -> list[str]:
    lines = _visible_markdown(text).splitlines()
    matches: list[tuple[int, int]] = []
    for idx, line in enumerate(lines):
        match = atx_heading(line)
        if match and match[1] == title:
            matches.append((idx + 1, match[0]))

    sections: list[str] = []
    for start, start_level in matches:
        end = len(lines)
        for idx in range(start, len(lines)):
            match = atx_heading(lines[idx])
            if match and match[0] <= start_level:
                end = idx
                break
        sections.append("\n".join(lines[start:end]))
    return sections


def section_text(text: str, title: str) -> str:
    sections = section_texts(text, title)
    return sections[0] if len(sections) == 1 else ""


def normalize_cell(value: str) -> str:
    return value.replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ").strip()


def split_table_row(line: str) -> list[str]:
    source = line.strip()
    cells: list[str] = []
    cell: list[str] = []
    index = 0
    ended_with_delimiter = False
    while index < len(source):
        char = source[index]
        if char == "\\":
            end = index
            while end < len(source) and source[end] == "\\":
                end += 1
            slash_count = end - index
            if end < len(source) and source[end] == "|" and slash_count % 2 == 1:
                cell.extend("\\" * (slash_count // 2))
                cell.append("|")
                index = end + 1
                ended_with_delimiter = False
                continue
            cell.extend("\\" * slash_count)
            index = end
            ended_with_delimiter = False
            continue
        if char == "|":
            cells.append(normalize_cell("".join(cell)))
            cell = []
            ended_with_delimiter = True
        else:
            cell.append(char)
            ended_with_delimiter = False
        index += 1
    cells.append(normalize_cell("".join(cell)))
    if source.startswith("|"):
        cells.pop(0)
    if ended_with_delimiter and cells:
        cells.pop()
    return cells


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.match(r"^:?-{3,}:?$", cell.strip()) for cell in cells)


def parsed_markdown_tables(text: str) -> list[tuple[list[str], list[dict[str, str]]]]:
    """Return Markdown pipe-table headers and row dictionaries.

    The parser supports the pipe-table shape used by ODK templates, including
    escaped pipes in cells and the valid form without leading/trailing pipes.
    """

    lines = _visible_markdown(text).splitlines()
    tables: list[tuple[list[str], list[dict[str, str]]]] = []
    idx = 0

    while idx < len(lines) - 1:
        if "|" not in lines[idx] or "|" not in lines[idx + 1]:
            idx += 1
            continue

        header = split_table_row(lines[idx])
        separator = split_table_row(lines[idx + 1])
        if not is_separator_row(separator) or len(separator) != len(header):
            idx += 1
            continue

        idx += 2
        rows: list[dict[str, str]] = []
        while idx < len(lines) and "|" in lines[idx]:
            cells = split_table_row(lines[idx])
            if len(cells) == len(header) and not is_separator_row(cells):
                rows.append(dict(zip(header, cells)))
            idx += 1
        tables.append((header, rows))

    return tables


def markdown_tables(text: str) -> list[list[dict[str, str]]]:
    """Return Markdown pipe tables as row dictionaries."""
    return [rows for _, rows in parsed_markdown_tables(text)]


def table_has_columns(text: str, required_columns: list[str]) -> bool:
    """Check if text contains a markdown table with the required column names (even if no data rows)."""
    for header, _ in parsed_markdown_tables(text):
        if all(column in header for column in required_columns):
            return True
    return False


def tables_with_columns(text: str, required_columns: list[str]) -> list[list[dict[str, str]]]:
    matches: list[list[dict[str, str]]] = []
    for header, rows in parsed_markdown_tables(text):
        if all(column in header for column in required_columns):
            matches.append(rows)
    return matches


def table_with_columns(text: str, required_columns: list[str]) -> list[dict[str, str]]:
    tables = tables_with_columns(text, required_columns)
    return tables[0] if len(tables) == 1 else []


def unique_table_with_columns(
    text: str, required_columns: list[str]
) -> list[dict[str, str]] | None:
    tables = tables_with_columns(text, required_columns)
    return tables[0] if len(tables) == 1 else None


def meaningful(value: str) -> bool:
    return bool(value.strip()) and not PLACEHOLDER_RE.match(value)
