#!/usr/bin/env python3
"""ArkUI-only extensions for the common spec-for-validation adapter."""

import re

from ohos_sdd_spec_for_validation import (
    BaseSpecForValidationAdapter,
    _ac_verification_complete,
    _external_spec_projection,
    _markdown_section_blocks,
    _meaningful_cell,
)

ARKUI_INTERNAL_DETAIL_PATTERNS = (
    r"\b(?:UIContentImpl|UiSessionManager|UiReportStub|ContentChangeManager|TaskExecutor|"
    r"PipelineContext|WeakPtr|PageTranslateNode|WebPattern|TextFieldPattern|Pattern|Manager|"
    r"MarkDirty|LargeStringAshmem|EventHandler|PostTask)\b",
    r"(?:translate\s*容器|snapshot\s*cache|pending\s*callback|注册\s*callback|"
    r"清\s*callback|调用方\s*pid|投递[^|]*任务)",
)

ARKUI_FORMAT_VERSION = "arkui-detailed-v1"
ARKUI_NFR_HEADINGS = (
    "是否涉及性能指标",
    "是否涉及功耗指标",
    "是否涉及稳定性 & 可靠性",
    "是否涉及安全隐私合规",
    "是否涉及 DFX",
)


class ProfileAdapter(BaseSpecForValidationAdapter):
    """Add ArkUI filters and the detailed 2D/NFR/2C template contract."""

    def internal_detail_patterns(self):
        return super().internal_detail_patterns() + ARKUI_INTERNAL_DETAIL_PATTERNS

    def external_spec_projection(self, spec):
        return _external_spec_projection(
            spec, self.internal_detail_patterns(), include_nfr=False)

    def can_preserve_analysis(self, old_artifact):
        frontmatter = self.parse_frontmatter(old_artifact or "")
        return frontmatter.get("format_version") == ARKUI_FORMAT_VERSION

    def normalize_preserved_analysis(self, preserved):
        return preserved

    @staticmethod
    def _detail_section(analysis, heading):
        blocks = _markdown_section_blocks(analysis, (heading,))
        return blocks[0][1] if blocks else ""

    @staticmethod
    def _detail_section_issues(analysis, heading):
        block = ProfileAdapter._detail_section(analysis, heading)
        if not block:
            return [f"缺少详细分析小节:{heading}"]
        match = re.search(r"\*\*是否涉及[：:]\*\*\s*(是|否|N/A|待确认)", block)
        if not match or match.group(1) == "待确认":
            return [f"{heading} 是否涉及必须为 是/否/N/A"]
        involvement = match.group(1)
        if any(token in block for token in ("待确认", "{{", "[填写")):
            return [f"{heading} 仍有未填写细项"]
        if involvement == "是":
            return []
        reason = re.search(r"\*\*不涉及理由[：:]\*\*\s*([^\n]+)", block)
        if not reason or not _meaningful_cell(reason.group(1)) or reason.group(1).strip() == "—":
            return [f"{heading} 选择否/N/A时必须说明不涉及理由"]
        return []

    def completion_issues(self, analysis, spec_acs):
        issues = []
        if re.search(r"^\s*-\s*待确认\s*[:：]", analysis, re.MULTILINE):
            issues.append("测试输入完备性仍有待确认项")
        issues.extend(_ac_verification_complete(analysis, spec_acs))
        detail_headings = []
        for definition in self.analysis_definitions:
            detail_headings.extend(
                f"是否涉及 {item}" if re.match(r"[A-Z]", item) else f"是否涉及{item}"
                for item in definition["items"])
        detail_headings.extend(ARKUI_NFR_HEADINGS)
        for heading in detail_headings:
            issues.extend(self._detail_section_issues(analysis, heading))
        return issues
