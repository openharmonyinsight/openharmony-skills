"""One interpretation of the proposal's eight involvement dimensions."""
from __future__ import annotations

import re

if __package__:
    from .odk_document import require_unique_section, require_unique_table_with_columns, meaningful
else:
    from odk_document import require_unique_section, require_unique_table_with_columns, meaningful

DIMENSIONS = dict(perf="性能", security="安全/权限", compatibility="兼容性",
                  **{"api-sdk": "API/SDK", "ipc": "IPC/跨进程", "build": "构建/组件",
                     "i18n": "国际化", "data-migration": "数据迁移"})


def canonical_dimension(label: str) -> str:
    label = label.replace("*", "").replace("`", "").strip()
    return "国际化" if label == "国际化/无障碍" else label


def involvement_value(cell: str) -> str | None:
    match = re.fullmatch(r"(是|否)(?:\s*[（(][^（）()\n]+[）)])?", cell.strip().strip("`*"))
    return match[1] if match else None


def involvement_rows(proposal: str) -> list[dict[str, str]]:
    section = require_unique_section(proposal, "不涉及项确认")
    rows = require_unique_table_with_columns(section or "", ["维度", "是否涉及"])
    return rows or []


def parse_eight_dim_involvement(proposal: str, dimension: str) -> str | None:
    rows = involvement_rows(proposal)
    for row in rows:
        if canonical_dimension(row.get("维度", "")) == dimension:
            return involvement_value(row.get("是否涉及", ""))
    return None


def involvement_errors(proposal: str) -> list[str]:
    try:
        section = require_unique_section(proposal, "不涉及项确认")
        # Use the same table identity as trigger parsing, so a second table
        # missing 依据 cannot make triggers ambiguous while integrity passes.
        rows = require_unique_table_with_columns(section or "", ["维度", "是否涉及"])
    except ValueError as error:
        return [str(error)]
    if not rows:
        return ["requires one nonempty 维度 / 是否涉及 / 依据 table"]
    expected, seen, errors = set(DIMENSIONS.values()), set(), []
    for row in rows:
        label = canonical_dimension(row["维度"])
        if label not in expected:
            errors.append(f"unknown dimension: {label or '<empty>'}")
        if label in seen:
            errors.append(f"duplicate dimension: {label}")
        seen.add(label)
        if involvement_value(row["是否涉及"]) is None:
            errors.append(f"{label} must state 是 or 否 (optional explanation in parentheses)")
        if not meaningful(row.get("依据", "")):
            errors.append(f"{label} requires 依据")
    errors.extend(f"missing dimension: {label}" for label in sorted(expected - seen))
    return errors
