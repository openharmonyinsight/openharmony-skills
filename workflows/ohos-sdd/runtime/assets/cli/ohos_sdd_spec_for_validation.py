#!/usr/bin/env python3
"""Profile-extendable spec-for-validation support for the ohos-sdd CLI.

This module owns the common lifecycle, default projection/rendering, source
consistency, evidence, and Profile routing. Profile adapters extend only domain
differences such as internal-detail patterns or exceptional projection rules.
"""

import hashlib
import importlib
import os
import re
import sys
from datetime import datetime, timezone

AC_ID_PATTERN = r"AC-\d+(?:\.\d+)*"
RULE_SECTIONS = ("规则定义", "业务规则", "功能规则", "异常/豁免规则", "异常规则", "恢复契约")
API_CONTRACT_SECTIONS = ("统一/补齐 API", "新增 API", "变更/废弃 API")
DEVELOPER_VERIFICATION_COLUMN_TITLES = (
    "推荐验证通道", "开发自验证", "开发验证方式", "自验证类型",
)
DEVELOPER_SELF_VERIFICATION = re.compile(
    r"SpecTest|unittest|unit\s*test|\bUT\b|单元测试", re.IGNORECASE)
GENERAL_INTERNAL_DETAIL_PATTERNS = (
    r"(?:^|[`(])(?:frameworks|interfaces|adapter|test|examples|build|tools)/",
    r"\b(?:BUILD\.gn|bundle\.json|context-references)\b",
    r"\b(?:Stage\s*\d+|当前源码|源码位置|内部实现|调用链|虚函数|基类)\b",
)
COMMON_FORBIDDEN_TOKENS = (
    "## 上下文和现状", "## 关键设计决策", "## 构建系统影响", "context-references",
    "BUILD.gn", "bundle.json", ".cpp`", ".h`",
)
_SECTION_NUMERALS = {
    1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九",
    10: "十", 11: "十一", 12: "十二", 13: "十三", 14: "十四", 15: "十五",
}


def _read(change_dir, fname):
    path = os.path.join(change_dir, fname)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _sha256_text(text):
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _ac_set(text):
    """AC identifiers allow one or more numeric segments, for example AC-1.2.3."""
    return set(re.findall(AC_ID_PATTERN, text or ""))


def _find_profiles_dir(start_dir):
    directory = os.path.abspath(start_dir)
    while True:
        for candidate in (os.path.join(directory, "runtime", "assets", "profiles"),
                          os.path.join(directory, "profiles")):
            if os.path.isdir(candidate):
                return candidate
        parent = os.path.dirname(directory)
        if parent == directory:
            break
        directory = parent
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in (os.path.join(here, "..", "profiles"),
                os.path.join(here, "..", "..", "profiles"),
                os.path.join(here, "..", "shared", "ohos-sdd", "profiles"),
                os.path.join(here, "..", "..", "shared", "ohos-sdd", "profiles")):
        candidate = os.path.normpath(rel)
        if os.path.isdir(candidate):
            return candidate
    return None


def _normalize_heading(value):
    value = (value or "").strip()
    wrappers = (("**", "**"), ("__", "__"), ("`", "`"))
    changed = True
    while changed:
        changed = False
        for begin, end in wrappers:
            if value.startswith(begin) and value.endswith(end) and len(value) > len(begin) + len(end):
                value = value[len(begin):-len(end)].strip()
                changed = True
    number = r"(?:\d+(?:\.\d+)*|[一二三四五六七八九十百]+)"
    for pattern in (rf"^[（(]\s*{number}\s*[）)]\s*", rf"^第\s*{number}\s*[章节部分]\s*",
                    rf"^{number}\s*[、.．:：]\s*", rf"^{number}\s+"):
        value = re.sub(pattern, "", value, count=1)
    return value.strip()


def _canonical_heading(value, allowed):
    normalized = _normalize_heading(value)
    for heading in allowed:
        if normalized == heading:
            return heading
        if normalized.startswith(heading):
            suffix = normalized[len(heading):].lstrip()
            if suffix.startswith(("（", "(", "：", ":", "-", "—")):
                return heading
    return None


def _section_markers(text, allowed):
    markers = []
    offset = 0
    for line in (text or "").splitlines(keepends=True):
        stripped = line.rstrip("\r\n")
        heading_match = re.match(r"^(#{2,3})\s+(.+?)\s*$", stripped)
        if heading_match:
            markers.append((offset, len(heading_match.group(1)),
                            _canonical_heading(heading_match.group(2), allowed)))
        else:
            bold_match = re.match(r"^\s*(\*\*|__)(.+?)\1\s*$", stripped)
            if bold_match:
                canonical = _canonical_heading(bold_match.group(2), allowed)
                if canonical:
                    markers.append((offset, 2, canonical))
        offset += len(line)
    return markers


def _markdown_section_blocks(text, allowed):
    markers = _section_markers(text, allowed)
    selected = []
    covered_until = -1
    for index, (start, level, canonical) in enumerate(markers):
        if not canonical or start < covered_until:
            continue
        end = len(text or "")
        for next_start, next_level, _next_canonical in markers[index + 1:]:
            if next_level <= level:
                end = next_start
                break
        selected.append((canonical, (text or "")[start:end].rstrip()))
        covered_until = end
    return selected


def _demote_headings(block):
    return re.sub(r"^(#{2,5})(\s+)", lambda match: "#" + match.group(1) + match.group(2),
                  block, flags=re.MULTILINE)


def _internal_detail_hits(text, patterns):
    return [pattern for pattern in patterns if re.search(pattern, text or "", re.IGNORECASE)]


def _filter_internal_table_rows(block, patterns):
    """Drop implementation-specific rows while preserving public rule/API rows."""
    output = []
    table_headers = []
    table_data_rows = 0
    saw_table = False
    in_table = False
    for line in (block or "").splitlines():
        stripped = line.strip()
        is_table = stripped.startswith("|") and stripped.endswith("|")
        is_separator = is_table and all(
            re.fullmatch(r":?-{3,}:?", cell.strip() or "")
            for cell in stripped[1:-1].split("|"))
        if is_table:
            saw_table = True
            if not in_table or is_separator:
                table_headers.append(line)
                in_table = True
                continue
            if _internal_detail_hits(line, patterns):
                continue
            table_data_rows += 1
            output.extend(table_headers)
            table_headers = []
            output.append(line)
            continue
        table_headers = []
        in_table = False
        if not _internal_detail_hits(line, patterns):
            output.append(line)
    if saw_table and table_data_rows == 0:
        return ""
    return "\n".join(output).strip()


def _project_named_sections(spec, allowed, patterns, filter_internal=False):
    projected = []
    for _heading, block in _markdown_section_blocks(spec, allowed):
        block = _demote_headings(block)
        if filter_internal:
            block = _filter_internal_table_rows(block, patterns)
        if block:
            projected.append(block)
    return "\n\n".join(projected)


def _project_nfr(spec, patterns):
    blocks = _markdown_section_blocks(spec, ("非功能性需求", "多设备适配声明", "全局特性影响"))
    projected = []
    for _heading, block in blocks:
        output = []
        for line in _demote_headings(block).splitlines():
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                cells = [cell.strip() for cell in stripped[1:-1].split("|")]
                if len(cells) < 2:
                    continue
                if all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells):
                    output.append("|---|---|")
                elif not _internal_detail_hits("|".join(cells[:2]), patterns):
                    output.append("| " + " | ".join(cells[:2]) + " |")
                continue
            if not _internal_detail_hits(line, patterns):
                output.append(line)
        text = "\n".join(output).strip()
        if text:
            projected.append(text)
    return "\n\n".join(projected)


def _remove_developer_verification_columns(block):
    """Remove whole developer-only table columns without rewriting source text."""
    output = []
    excluded = set()
    in_table = False
    for line in (block or "").splitlines():
        stripped = line.strip()
        is_table = stripped.startswith("|") and stripped.endswith("|")
        if not is_table:
            excluded = set()
            in_table = False
            output.append(line)
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        is_separator = all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)
        if not in_table and not is_separator:
            excluded = {
                index for index, cell in enumerate(cells)
                if any(title in cell for title in DEVELOPER_VERIFICATION_COLUMN_TITLES)
            }
            in_table = True
        kept = [cell for index, cell in enumerate(cells) if index not in excluded]
        if kept:
            output.append("| " + " | ".join(kept) + " |")
    return "\n".join(output).strip()


def _external_spec_projection(spec, patterns, include_nfr=True):
    overview = _project_named_sections(spec, ("概述",), patterns)
    stories = _project_named_sections(spec, ("用户故事",), patterns)
    if not stories:
        raise ValueError("spec.md 未找到可投影的对外行为章节")
    rules = _project_named_sections(spec, RULE_SECTIONS, patterns, filter_internal=True)
    api_contracts = _project_named_sections(
        spec, API_CONTRACT_SECTIONS, patterns, filter_internal=True)
    compatibility = _project_named_sections(
        spec, ("兼容性声明",), patterns, filter_internal=True)
    requirements = "\n\n".join(part for part in (overview, stories) if part)
    projected = ("## 一、需求目标与规格 `[源: spec.md]`\n\n" + requirements +
            "\n\n## 二、规则定义 `[源: spec.md]`\n\n" +
            (rules or "- spec.md 未提供可投影的对外行为规则。") +
            "\n\n## 三、API 变更分析 `[源: spec.md]`\n\n" +
            (api_contracts or "- spec.md 未声明可投影的对外 API 变更。") +
            "\n\n## 四、兼容性声明 `[源: spec.md]`\n\n" +
            (compatibility or "- spec.md 未声明兼容性变化。"))
    if include_nfr:
        projected += ("\n\n## 五、非功能性需求 `[源: spec.md]`\n\n" +
                      (_project_nfr(spec, patterns) or
                       "- spec.md 未声明用户可观察的非功能性要求。"))
    return projected


def _story_ids(text):
    return set(re.findall(r"^#{2,6}\s+(US-\d+(?:\.\d+)*)\s*[:：]", text or "", re.MULTILINE))


def _normalized_projection(text):
    return re.sub(r"\s+", " ", text or "").strip()


def _design_test_constraints(design):
    for _heading, block in _markdown_section_blocks(design, ("测试交接约束", "测试输入约束")):
        return _remove_developer_verification_columns(_demote_headings(block))
    return ("未提供独立的测试输入约束。生成 Agent 必须结合 `spec.md` 的对外行为和实际"
            "可观察表面完成验证点分析；如缺少可观察能力，回修 `design.md`。")


def _analysis_definitions(config):
    raw = config.get("analysis") or []
    if isinstance(raw, dict):
        raw = [raw]
    if not isinstance(raw, list):
        raise ValueError("spec_for_validation.analysis 必须为列表")
    definitions = []
    for index, entry in enumerate(raw, 1):
        if not isinstance(entry, dict):
            raise ValueError("spec_for_validation.analysis 每项必须为映射")
        title = str(entry.get("title") or "").strip()
        items = entry.get("items") or []
        if isinstance(items, str):
            items = [items]
        if not title or not isinstance(items, list) or not all(str(item).strip() for item in items):
            raise ValueError("spec_for_validation.analysis 每项必须声明 title 和非空 items")
        definitions.append({
            "id": str(entry.get("id") or index).strip(),
            "title": title,
            "items": tuple(str(item).strip() for item in items),
        })
    return tuple(definitions)


def _analysis_table(items):
    rows = ["| 分析点 | 涉及性 | 对外预期/差异 | 关联 AC | 验证点 | 测试侧验证方式 | N/A 理由 |",
            "|---|---|---|---|---|---|---|"]
    rows.extend(f"| {item} | 待确认 | 待确认 | 待确认 | 待确认 | 待确认 | 待确认 |" for item in items)
    return "\n".join(rows)


def _ac_verification_table(spec):
    rows = ["| AC | 对外预期 | 验证点 | 测试侧验证方式 |", "|---|---|---|---|"]
    rows.extend(f"| {ac} | 见对外行为规格 | 待确认 | 待确认 |" for ac in sorted(_ac_set(spec)))
    return "\n".join(rows)


def _section_number(index):
    return _SECTION_NUMERALS.get(index, str(index))


def _analysis_sections_markdown(definitions):
    sections = []
    for index, definition in enumerate(definitions, 8):
        sections.append(
            f"## {_section_number(index)}、{definition['title']}\n\n"
            "> 每项必须填写 `是/否/N/A`。`是`必须关联 AC 和验证点；"
            "`否/N/A`必须说明理由。\n\n" + _analysis_table(definition["items"]))
    return "\n\n".join(sections)


def _between(text, begin, end):
    start = (text or "").find(begin)
    finish = (text or "").find(end)
    if start == -1 or finish == -1 or finish < start:
        return ""
    return text[start + len(begin):finish].strip("\n")


def _replace_between(text, begin, end, content):
    start = (text or "").find(begin)
    finish = (text or "").find(end)
    if start == -1 or finish == -1 or finish < start:
        return text
    return ((text or "")[:start + len(begin)] + "\n" + content.strip("\n") + "\n" +
            (text or "")[finish:])


def _normalize_preserved_analysis_headings(text, definitions):
    expected = [("七", "AC 到验证点追溯")]
    expected.extend((_section_number(index), definition["title"])
                    for index, definition in enumerate(definitions, 8))
    pending_number = _section_number(8 + len(definitions))
    normalized = re.sub(r"测试交接待确认项", "测试输入待确认项", text or "")
    expected.append((pending_number, "测试输入待确认项"))
    for number, title in expected:
        normalized = re.sub(
            rf"^##\s+(?:(?:[一二三四五六七八九十]+|\d+)[、.．]\s*)?{re.escape(title)}\s*$",
            f"## {number}、{title}", normalized, flags=re.MULTILINE)
    return normalized


def _markdown_table_rows(text):
    rows = []
    for line in (text or "").splitlines():
        stripped = line.strip()
        if not (stripped.startswith("|") and stripped.endswith("|")):
            continue
        cells = [cell.strip() for cell in stripped[1:-1].split("|")]
        if cells and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells):
            continue
        rows.append(cells)
    return rows


def _spec_overview_metadata(spec):
    blocks = _markdown_section_blocks(spec, ("概述",))
    if not blocks:
        return {}
    rows = _markdown_table_rows(blocks[0][1])
    return {cells[0]: cells[1] for cells in rows if len(cells) >= 2 and cells[0] != "属性"}


def _meaningful_cell(value):
    value = (value or "").strip()
    return bool(value) and not any(token in value for token in ("待确认", "{{", "[填写"))


def _analysis_rows_complete(analysis, items, spec_acs):
    rows = {cells[0]: cells for cells in _markdown_table_rows(analysis) if cells}
    issues = []
    for item in items:
        cells = rows.get(item)
        if not cells or len(cells) < 7:
            issues.append(f"缺少或损坏分析行:{item}")
            continue
        involvement = cells[1]
        if involvement not in {"是", "否", "N/A"}:
            issues.append(f"{item} 涉及性必须为 是/否/N/A")
            continue
        if any(not _meaningful_cell(cell) for cell in cells[1:7]):
            issues.append(f"{item} 仍有空值或占位符")
            continue
        if involvement == "是":
            linked = _ac_set(cells[3])
            if not linked or not linked.issubset(spec_acs):
                issues.append(f"{item} 必须关联 spec 中的 AC")
        elif not _meaningful_cell(cells[6]):
            issues.append(f"{item} 为 否/N/A 时必须说明理由")
    return issues


def _ac_verification_complete(analysis, spec_acs):
    rows = {cells[0]: cells for cells in _markdown_table_rows(analysis)
            if cells and re.fullmatch(AC_ID_PATTERN, cells[0])}
    issues = []
    if set(rows) != spec_acs:
        issues.append(f"AC 验证点集合不完整:spec={sorted(spec_acs)},rows={sorted(rows)}")
    for ac in sorted(spec_acs):
        cells = rows.get(ac)
        if cells and len(cells) >= 4:
            if not _meaningful_cell(cells[2]) or not _meaningful_cell(cells[3]):
                issues.append(f"{ac} 缺少验证点或测试侧验证方式")
    return issues


class BaseSpecForValidationAdapter:
    """Common projection, rendering, validation, and approval policy."""

    def __init__(self, parse_frontmatter, config):
        self.parse_frontmatter = parse_frontmatter
        self.config = config
        self.analysis_definitions = _analysis_definitions(config)

    def internal_detail_patterns(self):
        return GENERAL_INTERNAL_DETAIL_PATTERNS

    def forbidden_tokens(self):
        return COMMON_FORBIDDEN_TOKENS

    def external_spec_projection(self, spec):
        return _external_spec_projection(spec, self.internal_detail_patterns())

    def nfr_source_projection(self, spec):
        return (_project_nfr(spec, self.internal_detail_patterns()) or
                "- spec.md 未声明用户可观察的非功能性要求。")

    def can_preserve_analysis(self, old_artifact):
        return True

    def normalize_preserved_analysis(self, preserved):
        return _normalize_preserved_analysis_headings(preserved, self.analysis_definitions)

    def refresh_preserved_generated_regions(self, preserved, spec, design):
        regions = (
            ("<!-- GENERATED:NFR-SPEC:BEGIN -->", "<!-- GENERATED:NFR-SPEC:END -->",
             self.nfr_source_projection(spec)),
            ("<!-- GENERATED:AC-VERIFICATION:BEGIN -->",
             "<!-- GENERATED:AC-VERIFICATION:END -->", _ac_verification_table(spec)),
            ("<!-- GENERATED:DESIGN-CONSTRAINTS:BEGIN -->",
             "<!-- GENERATED:DESIGN-CONSTRAINTS:END -->", _design_test_constraints(design)),
        )
        refreshed = preserved
        for begin, end, content in regions:
            refreshed = _replace_between(refreshed, begin, end, content)
        return refreshed

    def completion_issues(self, analysis, spec_acs):
        pending = (bool(re.search(r"^\s*-\s*待确认\s*[:：]", analysis, re.MULTILINE)) or
                   bool(re.search(r"\|\s*待确认\s*(?=\|)", analysis)) or
                   any(token in analysis for token in ("{{", "[填写")))
        issues = ["仍有待确认或模板占位符"] if pending else []
        issues.extend(_ac_verification_complete(analysis, spec_acs))
        for definition in self.analysis_definitions:
            issues.extend(_analysis_rows_complete(analysis, definition["items"], spec_acs))
        return issues

    def render(self, change_dir, template_path, spec, design, profile, manifest,
               preserve_analysis=False, old_artifact=""):
        with open(template_path, encoding="utf-8") as fh:
            template = fh.read()
        preserved = _between(old_artifact, "<!-- TEST-ANALYSIS:BEGIN -->",
                             "<!-- TEST-ANALYSIS:END -->")
        subprofiles = manifest.get("subprofiles") or []
        if isinstance(subprofiles, str):
            subprofiles = [] if subprofiles.strip() in ("", "[]") else [subprofiles]
        pending_number = _section_number(8 + len(self.analysis_definitions))
        approval_number = _section_number(9 + len(self.analysis_definitions))
        metadata = _spec_overview_metadata(spec)
        generated_date = datetime.now(timezone.utc).date().isoformat()
        replacements = {
            "{{SOURCE_SPEC_HASH}}": _sha256_text(spec),
            "{{SOURCE_DESIGN_HASH}}": _sha256_text(design),
            "{{SUBPROFILE}}": str(subprofiles[0]) if subprofiles else "none",
            "{{PROFILE}}": profile,
            "{{PROFILE_TITLE}}": str(self.config.get("title") or "测试输入规格"),
            "{{GENERATED_AT}}": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "{{GENERATED_DATE}}": generated_date,
            "{{REQUIREMENT_ID}}": str(manifest.get("id") or "未声明"),
            "{{REQUIREMENT_NAME}}": str(metadata.get("需求名称") or
                                       metadata.get("特性名称") or "未声明需求"),
            "{{FEATURE_ID}}": str(metadata.get("特性编号") or "未声明"),
            "{{REQUIREMENT_SOURCE}}": str(metadata.get("需求来源") or "未声明"),
            "{{PROPOSER}}": str(metadata.get("提出人") or "未声明"),
            "{{PRIORITY}}": str(metadata.get("优先级") or "未声明"),
            "{{TARGET_VERSION}}": str(metadata.get("目标版本") or "未声明"),
            "{{SIG}}": str(metadata.get("SIG归属") or metadata.get("SIG 归属") or "未声明"),
            "{{SOURCE_STATUS}}": str(metadata.get("状态") or "Approved"),
            "{{COMPLEXITY}}": str(metadata.get("复杂度") or "未声明"),
            "{{EXTERNAL_SPEC}}": self.external_spec_projection(spec),
            "{{NFR_SOURCE}}": self.nfr_source_projection(spec),
            "{{DESIGN_CONSTRAINTS}}": _design_test_constraints(design),
            "{{AC_VERIFICATION}}": _ac_verification_table(spec),
            "{{PROFILE_ANALYSIS_SECTIONS}}": _analysis_sections_markdown(self.analysis_definitions),
            "{{PENDING_SECTION_HEADING}}": f"{pending_number}、测试输入待确认项",
            "{{APPROVAL_SECTION_HEADING}}": f"{approval_number}、来源与审批",
        }
        rendered = template
        for key, value in replacements.items():
            rendered = rendered.replace(key, value)
        if preserve_analysis and preserved and self.can_preserve_analysis(old_artifact):
            preserved = self.normalize_preserved_analysis(preserved)
            preserved = self.refresh_preserved_generated_regions(preserved, spec, design)
            begin = "<!-- TEST-ANALYSIS:BEGIN -->"
            end = "<!-- TEST-ANALYSIS:END -->"
            rendered = (rendered[:rendered.index(begin) + len(begin)] + "\n" + preserved + "\n" +
                        rendered[rendered.index(end):])
        return rendered

    def checks(self, spec, design, artifact, require_complete=True):
        checks = []

        def add(ok, item, issue=""):
            checks.append((ok, item, issue))

        analysis = _between(artifact, "<!-- TEST-ANALYSIS:BEGIN -->",
                            "<!-- TEST-ANALYSIS:END -->")
        external_spec = _between(artifact, "<!-- GENERATED:EXTERNAL-SPEC:BEGIN -->",
                                 "<!-- GENERATED:EXTERNAL-SPEC:END -->")
        nfr_source = _between(artifact, "<!-- GENERATED:NFR-SPEC:BEGIN -->",
                              "<!-- GENERATED:NFR-SPEC:END -->")
        generated_content = "\n".join((
            external_spec,
            nfr_source,
            _between(artifact, "<!-- GENERATED:DESIGN-CONSTRAINTS:BEGIN -->",
                     "<!-- GENERATED:DESIGN-CONSTRAINTS:END -->"),
            analysis,
        ))
        found = [token for token in self.forbidden_tokens() if token in generated_content]
        internal_hits = _internal_detail_hits(generated_content, self.internal_detail_patterns())
        internal_issues = found + internal_hits
        add(not internal_issues, "Spec for Validation 无内部实现信息",
            "命中禁止内容:" + ", ".join(internal_issues) if internal_issues else "")
        missing_stories = sorted(_story_ids(spec) - _story_ids(external_spec))
        add(not missing_stories, "Spec for Validation 用户故事完整",
            "未投影来源用户故事:" + ", ".join(missing_stories) if missing_stories else "")
        expected_external = self.external_spec_projection(spec)
        projection_changed = (_normalized_projection(external_spec) !=
                              _normalized_projection(expected_external))
        add(not projection_changed, "Spec for Validation 来源规格投影未改写",
            "GENERATED:EXTERNAL-SPEC 区域只能由 CLI 刷新，不得摘要、删减或手工改写"
            if projection_changed else "")
        if "<!-- GENERATED:NFR-SPEC:BEGIN -->" in artifact:
            nfr_changed = (_normalized_projection(nfr_source) !=
                           _normalized_projection(self.nfr_source_projection(spec)))
            add(not nfr_changed, "Spec for Validation 非功能性需求来源投影未改写",
                "GENERATED:NFR-SPEC 区域只能由 CLI 刷新，不得摘要、删减或手工改写"
                if nfr_changed else "")
        developer_verify = DEVELOPER_SELF_VERIFICATION.findall(artifact)
        add(not developer_verify, "Spec for Validation 无开发自验证信息",
            "测试输入产物不得包含开发侧自验证类型" if developer_verify else "")
        if require_complete:
            spec_acs = _ac_set(spec)
            completeness_issues = self.completion_issues(analysis, spec_acs)
            add(not completeness_issues, "Profile 专项分析与验证点完整",
                "; ".join(completeness_issues))
        return checks

    def source_edge_issues(self, spec, design, artifact):
        spec_issues = []
        if DEVELOPER_SELF_VERIFICATION.search(artifact):
            spec_issues.append("spec-for-validation 不得包含开发侧自验证类型、用例、命令或结果")
        external_spec = _between(artifact, "<!-- GENERATED:EXTERNAL-SPEC:BEGIN -->",
                                 "<!-- GENERATED:EXTERNAL-SPEC:END -->")
        expected = self.external_spec_projection(spec)
        if _normalized_projection(external_spec) != _normalized_projection(expected):
            spec_issues.append("GENERATED:EXTERNAL-SPEC 来源投影被摘要、删减或手工改写")
        if "<!-- GENERATED:NFR-SPEC:BEGIN -->" in artifact:
            nfr_source = _between(artifact, "<!-- GENERATED:NFR-SPEC:BEGIN -->",
                                  "<!-- GENERATED:NFR-SPEC:END -->")
            if (_normalized_projection(nfr_source) !=
                    _normalized_projection(self.nfr_source_projection(spec))):
                spec_issues.append("GENERATED:NFR-SPEC 来源投影被摘要、删减或手工改写")
        missing_stories = sorted(_story_ids(spec) - _story_ids(external_spec))
        if missing_stories:
            spec_issues.append("用户故事投影不完整:" + ", ".join(missing_stories))
        return spec_issues, []

    @staticmethod
    def approval_complete(artifact):
        rows = {cells[0]: cells[1] for cells in _markdown_table_rows(artifact) if len(cells) >= 2}
        accepted = {"approved", "pass", "通过", "同意"}
        dev = rows.get("开发/Spec Owner 结论", "").strip().lower()
        test = rows.get("测试 Owner 结论", "").strip().lower()
        return dev in accepted and test in accepted


class SpecForValidationService:
    """spec-for-validation application service with optional Profile extensions."""

    def __init__(self, parse_frontmatter):
        self.parse_frontmatter = parse_frontmatter

    def _doc_status(self, text):
        frontmatter = self.parse_frontmatter(text or "")
        status = str(frontmatter.get("status") or "").strip()
        if status:
            return status.lower()
        match = re.search(r"^\|\s*(?:状态|Status)\s*\|\s*([^|]+?)\s*\|", text or "", re.MULTILINE)
        return match.group(1).strip().lower() if match else ""

    def _is_approved(self, text):
        return self._doc_status(text) in {"approved", "baselined"}

    def _manifest_profile(self, change_dir):
        frontmatter = self.parse_frontmatter(_read(change_dir, "manifest.md") or "")
        return str(frontmatter.get("profile") or "").strip(), frontmatter

    def _profile_frontmatter(self, profiles_dir, base_profile):
        source_path = os.path.join(profiles_dir, base_profile, "profile.md")
        dist_path = os.path.join(profiles_dir, base_profile + ".md")
        profile_path = source_path if os.path.isfile(source_path) else dist_path
        if not os.path.isfile(profile_path):
            return {}
        with open(profile_path, encoding="utf-8") as fh:
            return self.parse_frontmatter(fh.read())

    def legacy_issues(self, change_dir, profiles_dir=None):
        """Return migration blockers left by the spec-for-test rename."""
        issues = []
        legacy_artifact = os.path.join(change_dir, "spec-for-test.md")
        current_artifact = os.path.join(change_dir, "spec-for-validation.md")
        legacy_evidence = os.path.join(
            change_dir, "evidence", "checks", "check-spec-for-test.md")
        current_evidence = os.path.join(
            change_dir, "evidence", "checks", "check-spec-for-validation.md")

        if os.path.isfile(legacy_artifact):
            if os.path.isfile(current_artifact):
                issues.append(
                    "spec-for-test.md 与 spec-for-validation.md 同时存在；"
                    "请确认唯一事实源并删除旧文件")
            else:
                issues.append(
                    "检测到旧产物 spec-for-test.md；请迁移为 spec-for-validation.md")
        if os.path.isfile(legacy_evidence):
            if os.path.isfile(current_evidence):
                issues.append(
                    "check-spec-for-test.md 与 check-spec-for-validation.md 同时存在；"
                    "请删除旧 evidence 并重新运行 check")
            else:
                issues.append(
                    "检测到旧 evidence check-spec-for-test.md；"
                    "请删除旧 evidence 并运行 spec-for-validation check")

        test_spec = _read(change_dir, "test-spec.md") or ""
        if re.search(
                r"(?<![A-Za-z0-9_.-])spec-for-test\.md(?![A-Za-z0-9_.-])",
                test_spec):
            issues.append(
                "test-spec.md 仍引用 spec-for-test.md；请改为 spec-for-validation.md")

        profile, _manifest = self._manifest_profile(change_dir)
        if profile:
            profiles_dir = profiles_dir or _find_profiles_dir(change_dir)
            if profiles_dir:
                profile_fm = self._profile_frontmatter(
                    profiles_dir, profile.split("/", 1)[0])
                has_legacy = "spec_for_test" in profile_fm
                has_current = "spec_for_validation" in profile_fm
                if has_legacy and has_current:
                    issues.append(
                        f"profile={profile} 同时声明 spec_for_test 与 spec_for_validation；"
                        "请删除旧键 spec_for_test")
                elif has_legacy:
                    issues.append(
                        f"profile={profile} 使用旧键 spec_for_test；"
                        "请迁移为 spec_for_validation")
        return issues

    def require_no_legacy(self, change_dir, profiles_dir=None):
        issues = self.legacy_issues(change_dir, profiles_dir)
        if issues:
            raise ValueError("legacy 迁移阻塞: " + "; ".join(issues))

    @staticmethod
    def _default_template_path(profiles_dir):
        return os.path.join(os.path.dirname(os.path.abspath(profiles_dir)),
                            "templates", "spec-for-validation.md")

    def _adapter(self, change_dir, profiles_dir=None):
        profile, manifest = self._manifest_profile(change_dir)
        if not profile:
            raise ValueError("manifest.profile 未声明")
        base_profile = profile.split("/", 1)[0]
        profiles_dir = profiles_dir or _find_profiles_dir(change_dir)
        if not profiles_dir:
            raise ValueError("找不到 Profile 目录")
        profile_fm = self._profile_frontmatter(profiles_dir, base_profile)
        has_legacy = "spec_for_test" in profile_fm
        has_current = "spec_for_validation" in profile_fm
        if has_legacy and has_current:
            raise ValueError(
                f"profile={profile} 同时声明 spec_for_test 与 spec_for_validation；"
                "请删除旧键 spec_for_test")
        if has_legacy:
            raise ValueError(
                f"profile={profile} 使用旧键 spec_for_test；请迁移为 spec_for_validation")
        config = profile_fm.get("spec_for_validation")
        if not isinstance(config, dict):
            raise ValueError(f"profile={profile} 未声明支持 Spec for Validation")
        if not str(config.get("playbook") or "").strip():
            raise ValueError(f"profile={profile} 的 spec_for_validation 配置缺少 playbook")

        adapter_class = BaseSpecForValidationAdapter
        adapter_name = str(config.get("adapter") or "").strip()
        if adapter_name:
            safe_adapter = re.sub(r"[^A-Za-z0-9_]", "_", adapter_name.replace("-", "_"))
            if safe_adapter != adapter_name.replace("-", "_"):
                raise ValueError(f"profile={profile} 的 Spec for Validation adapter 名称非法")
            module_name = f"ohos_sdd_spec_for_validation_{safe_adapter}"
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError as exc:
                if exc.name != module_name:
                    raise
                raise ValueError(
                    f"profile={profile} 未提供 Spec for Validation adapter:{adapter_name}") from exc
            adapter_class = getattr(module, "ProfileAdapter", None)
            if adapter_class is None:
                raise ValueError(f"profile={profile} 的 Spec for Validation adapter 缺少 ProfileAdapter")

        template_path = os.path.abspath(self._default_template_path(profiles_dir))
        template_override = str(config.get("template_override") or "").strip()
        if template_override:
            profile_assets = os.path.abspath(os.path.join(profiles_dir, base_profile))
            template_path = os.path.abspath(os.path.join(profile_assets, template_override))
            if os.path.commonpath((profile_assets, template_path)) != profile_assets:
                raise ValueError(f"profile={profile} 的 Spec for Validation template_override 路径越界")
        if not os.path.isfile(template_path):
            raise ValueError(f"找不到 Spec for Validation 模板:{template_path}")
        return adapter_class(self.parse_frontmatter, config), template_path, profile, manifest

    def contract_template_checks(self, root, artifact_id):
        """Validate the global template and all opt-in Profile extensions.
        兼容新仓布局(root/runtime/assets/...)和发布布局(root/...)。"""
        checks = []
        def _resolve(*segs):
            """兼容新仓(root/runtime/assets/...)和发布布局(root/...)。
            tools/cli/ 自动扁平化为 cli/（发布布局历史路径兼容）。"""
            for prefix in ("runtime/assets", ""):
                p = os.path.join(root, prefix, *segs)
                if os.path.exists(p):
                    return p
            # tools/cli/ → cli/ 扁平化兼容
            if segs and segs[0] == "tools" and len(segs) > 1:
                for prefix in ("runtime/assets", ""):
                    p = os.path.join(root, prefix, *segs[1:])
                    if os.path.exists(p):
                        return p
            return os.path.join(root, *segs)  # 回退路径(保持报错信息可读)

        global_template = _resolve("templates", "spec-for-validation.md")
        global_ok = os.path.isfile(global_template) and os.path.getsize(global_template) > 0
        checks.append((global_ok, f"{artifact_id}.template",
                       "" if global_ok else f"全局模板缺失或为空:{global_template}"))
        supported_profiles = []
        profiles_root = _resolve("profiles")
        if os.path.isdir(profiles_root):
            for profile_name in sorted(os.listdir(profiles_root)):
                profile_dir = os.path.join(profiles_root, profile_name)
                profile_md = os.path.join(profile_dir, "profile.md")
                if not os.path.isfile(profile_md):
                    continue
                with open(profile_md, encoding="utf-8") as fh:
                    profile_fm = self.parse_frontmatter(fh.read())
                has_legacy = "spec_for_test" in profile_fm
                has_current = "spec_for_validation" in profile_fm
                if has_legacy:
                    issue = ("同时声明 spec_for_test 与 spec_for_validation；请删除旧键 spec_for_test"
                             if has_current else
                             "使用旧键 spec_for_test；请迁移为 spec_for_validation")
                    checks.append((False, f"{artifact_id}.profile-config:{profile_name}", issue))
                    continue
                config = profile_fm.get("spec_for_validation")
                if not isinstance(config, dict):
                    continue
                issues = []
                playbook = str(config.get("playbook") or "").strip()
                playbook_path = ""
                if playbook:
                    for prefix in ("runtime/assets", ""):
                        pp = os.path.join(root, prefix, playbook)
                        if os.path.isfile(pp):
                            playbook_path = pp
                            break
                    if not playbook_path:
                        playbook_path = os.path.join(root, playbook)
                if not playbook or not os.path.isfile(playbook_path):
                    issues.append(f"playbook 缺失:{playbook}")
                adapter = str(config.get("adapter") or "").strip()
                if adapter:
                    adapter_path = _resolve("tools", "cli",
                        f"ohos_sdd_spec_for_validation_{adapter.replace('-', '_')}.py")
                    if not os.path.isfile(adapter_path):
                        issues.append(f"adapter 缺失:{adapter}")
                override = str(config.get("template_override") or "").strip()
                if override:
                    profile_assets = os.path.abspath(profile_dir)
                    override_path = os.path.abspath(os.path.join(profile_assets, override))
                    if (os.path.commonpath((profile_assets, override_path)) != profile_assets or
                            not os.path.isfile(override_path)):
                        issues.append(f"template_override 无效:{override}")
                try:
                    _analysis_definitions(config)
                except ValueError as exc:
                    issues.append(str(exc))
                label = f"{artifact_id}.profile-config:{profile_name}"
                checks.append((not issues, label, "; ".join(issues)))
                if not issues:
                    supported_profiles.append(profile_name)
        checks.append((bool(supported_profiles), f"{artifact_id}.profile-support",
                       "" if supported_profiles else "没有 Profile 声明有效的 spec_for_validation 增量配置"))
        return checks

    def render(self, change_dir, profiles_dir=None, preserve_analysis=False):
        spec = _read(change_dir, "spec.md")
        design = _read(change_dir, "design.md")
        if spec is None or design is None:
            raise ValueError("需要 spec.md 和 design.md")
        if not self._is_approved(spec) or not self._is_approved(design):
            raise ValueError("spec.md 和 design.md 必须均为 Approved/Baselined")
        adapter, template_path, profile, manifest = self._adapter(change_dir, profiles_dir)
        return adapter.render(
            change_dir=change_dir, template_path=template_path, spec=spec, design=design,
            profile=profile, manifest=manifest, preserve_analysis=preserve_analysis,
            old_artifact=_read(change_dir, "spec-for-validation.md") or "")

    def checks(self, change_dir, require_complete=True, profiles_dir=None):
        checks = []
        spec = _read(change_dir, "spec.md")
        design = _read(change_dir, "design.md")
        artifact = _read(change_dir, "spec-for-validation.md")

        def add(ok, item, issue=""):
            checks.append((ok, item, issue))

        adapter = None
        try:
            adapter, _template_path, _profile, _manifest = self._adapter(change_dir, profiles_dir)
            add(True, "Profile Spec for Validation 支持")
        except ValueError as exc:
            add(False, "Profile Spec for Validation 支持", str(exc))
        add(bool(spec and self._is_approved(spec)), "Spec Approved",
            "spec.md 缺失或未 Approved/Baselined")
        add(bool(design and self._is_approved(design)), "Design Approved",
            "design.md 缺失或未 Approved/Baselined")
        add(bool(artifact), "spec-for-validation 存在", "spec-for-validation.md 缺失")
        if not artifact:
            return checks
        frontmatter = self.parse_frontmatter(artifact)
        add(frontmatter.get("artifact") == "spec-for-validation", "交付件类型",
            "frontmatter.artifact 必须为 spec-for-validation")
        add(frontmatter.get("source_spec_hash") == _sha256_text(spec), "Spec 来源一致",
            "source_spec_hash 与当前 spec.md 不一致")
        add(frontmatter.get("source_design_hash") == _sha256_text(design), "Design 来源一致",
            "source_design_hash 与当前 design.md 不一致")
        add(_ac_set(artifact) == _ac_set(spec), "AC 集合一致",
            f"spec={sorted(_ac_set(spec))}, spec-for-validation={sorted(_ac_set(artifact))}")
        if adapter is not None:
            checks.extend(adapter.checks(spec, design, artifact, require_complete=require_complete))
        if require_complete:
            add(self._doc_status(artifact) in {"readyforreview", "ready_for_review", "approved"},
                "交付件状态", "状态必须为 ReadyForReview 或 Approved")
        return checks

    @staticmethod
    def write_evidence(change_dir, checks):
        target_dir = os.path.join(change_dir, "evidence", "checks")
        os.makedirs(target_dir, exist_ok=True)
        target = os.path.join(target_dir, "check-spec-for-validation.md")
        passed = all(ok for ok, _item, _issue in checks)
        lines = ["# Spec for Validation 检查", "", f"- 结论: {'PASS' if passed else 'FAIL'}",
                 f"- 时间: {datetime.now(timezone.utc).isoformat(timespec='seconds')}", "",
                 "| 检查项 | 结论 | 证据/问题 |", "|---|---|---|"]
        for ok, item, issue in checks:
            lines.append(f"| {item} | {'PASS' if ok else 'FAIL'} | {issue or '满足'} |")
        with open(target, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        return target, passed

    def source_edge_issues(self, change_dir, spec, design):
        artifact = _read(change_dir, "spec-for-validation.md")
        if artifact is None:
            return None
        frontmatter = self.parse_frontmatter(artifact)
        spec_issues = []
        design_issues = []
        adapter = None
        try:
            adapter, _template_path, _profile, _manifest = self._adapter(change_dir)
        except ValueError as exc:
            spec_issues.append(str(exc))
        if not (spec and self._is_approved(spec)):
            spec_issues.append("spec.md 缺失或未 Approved/Baselined")
        if frontmatter.get("source_spec_hash") != _sha256_text(spec):
            spec_issues.append("source_spec_hash 与当前 spec.md 不一致")
        if _ac_set(artifact) != _ac_set(spec):
            spec_issues.append(
                f"AC 集合不一致:spec={sorted(_ac_set(spec))},artifact={sorted(_ac_set(artifact))}")
        if not (design and self._is_approved(design)):
            design_issues.append("design.md 缺失或未 Approved/Baselined")
        if frontmatter.get("source_design_hash") != _sha256_text(design):
            design_issues.append("source_design_hash 与当前 design.md 不一致")
        if adapter is not None:
            extra_spec, extra_design = adapter.source_edge_issues(spec, design, artifact)
            spec_issues.extend(extra_spec)
            design_issues.extend(extra_design)
        return spec_issues, design_issues

    def archive_ready(self, change_dir):
        artifact = _read(change_dir, "spec-for-validation.md")
        if artifact is None:
            return True
        evidence = _read(change_dir, os.path.join("evidence", "checks", "check-spec-for-validation.md"))
        try:
            adapter, _template_path, _profile, _manifest = self._adapter(change_dir)
        except ValueError:
            return False
        approved = self._doc_status(artifact) == "approved" and adapter.approval_complete(artifact)
        evidence_ok = bool(evidence and "- 结论: PASS" in evidence)
        current_ok = all(ok for ok, _item, _issue in self.checks(change_dir, require_complete=True))
        return approved and evidence_ok and current_ok

    @staticmethod
    def _parse_args(argv):
        if not argv:
            return None, None, None
        action = argv[0]
        change = None
        profiles = None
        index = 1
        while index < len(argv):
            if argv[index] == "--profiles" and index + 1 < len(argv):
                profiles = argv[index + 1]
                index += 2
            elif not argv[index].startswith("-") and change is None:
                change = argv[index]
                index += 1
            else:
                index += 1
        return action, change, profiles

    def command(self, argv):
        action, change, profiles = self._parse_args(argv)
        if action not in {"generate", "refresh", "check"} or not change:
            print("usage: ohos-sdd spec-for-validation <generate|refresh|check> <change-dir>",
                  file=sys.stderr)
            return 2
        if not os.path.isdir(change):
            print(f"spec-for-validation: change dir not found:{change}", file=sys.stderr)
            return 2
        try:
            self.require_no_legacy(change, profiles)
        except ValueError as exc:
            print(f"spec-for-validation: {exc}", file=sys.stderr)
            return 2
        if action in {"generate", "refresh"}:
            target = os.path.join(change, "spec-for-validation.md")
            if action == "generate" and os.path.exists(target):
                print("spec-for-validation generate: spec-for-validation.md 已存在，请使用 refresh", file=sys.stderr)
                return 2
            profiles = profiles or _find_profiles_dir(change)
            if not profiles:
                print("spec-for-validation: 找不到 Profile 目录", file=sys.stderr)
                return 2
            try:
                rendered = self.render(change, profiles, preserve_analysis=(action == "refresh"))
            except ValueError as exc:
                print(f"spec-for-validation {action}: {exc}", file=sys.stderr)
                return 1
            with open(target, "w", encoding="utf-8") as fh:
                fh.write(rendered)
            checks = self.checks(change, require_complete=True, profiles_dir=profiles)
            evidence, _passed = self.write_evidence(change, checks)
            print(f"已{('生成' if action == 'generate' else '刷新')}:{target}")
            print(f"草稿检查证据:{evidence}")
            print("当前产物为 Draft；在 Profile 定义的分析、审批准备和状态完成前，证据为 FAIL 属预期")
            print("下一步:按 ohos-spec-for-validation skill 和命中的 Profile 完成测试输入分析，再运行 check")
            return 0

        checks = self.checks(change, require_complete=True, profiles_dir=profiles)
        evidence, passed = self.write_evidence(change, checks)
        for ok, item, issue in checks:
            print(f"[{'OK' if ok else 'FAIL'}] {item}{(': ' + issue) if issue else ''}")
        print(f"检查证据:{evidence}")
        return 0 if passed else 1
