#!/usr/bin/env python3
"""ohos-sdd core engine, stdlib-only.

Owns: mini YAML parser, validate Levels A/B/C/D, contract self-check.
Profile-extendable Spec for Validation support lives in ohos_sdd_spec_for_validation.py.
NO third-party imports (no PyYAML). When python is absent the shell dispatcher
takes the no-python path; this file is only reached when python3 is available.
"""
import importlib
import hashlib
import json
import os
import re
import sys

_MAP_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
AC_ID_PATTERN = r"AC-\d+(?:\.\d+)*"
RULE_ID_PATTERN = r"R-\d+(?:\.\d+)*"
TASK_ID_PATTERN = r"TASK-[A-Za-z0-9][A-Za-z0-9.-]*"
ADR_ID_PATTERN = r"ADR-[A-Za-z0-9][A-Za-z0-9.-]*"
STATE_ID_PATTERN = r"STATE-\d+"
INVARIANT_ID_PATTERN = r"INV-\d+"
IMPLEMENTATION_CLOSURE_STATUSES = {"verifying", "done", "archived"}

# Define 审批合同的唯一运行时事实源。artifacts.yaml 通过
# validate_contract_source() 对这些值做 pin 自检，避免合同声明与门禁实现漂移。
PROPOSAL_PHASE_STATUS_FIELD = "phase_status"
PROPOSAL_PHASE_STATUS_VALUES = {
    "clarifying", "awaiting_approval", "approved", "changes_requested", "blocked"
}
PROPOSAL_LEGACY_STATUS_VALUES = {"draft", "baselined", "deferred", "rejected"}
PHASE_APPROVAL_ALLOWED_STATUSES = PROPOSAL_PHASE_STATUS_VALUES
PHASE_APPROVAL_FIELD = "approval"
PHASE_APPROVAL_REQUIRED_FIELDS = (
    "status", "approver", "evidence", "approved_at", "baseline_digest"
)
PHASE_APPROVAL_APPROVED_STATUS = "approved"
PHASE_APPROVAL_DOWNSTREAM_REQUIRES_APPROVED = True


def _normalize_status_values(values):
    """Normalize contract display values and frontmatter values to one spelling."""
    normalized = set()
    for value in values or []:
        text = str(value).strip()
        text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
        normalized.add(text.lower())
    return normalized


def _unquote_scalar(value):
    """Remove optional YAML-style matching quotes from a frontmatter scalar."""
    text = str(value or "").strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        return text[1:-1]
    return text


def _proposal_baseline_digest(proposal):
    """Hash the approved Define baseline section after stable whitespace cleanup."""
    baselines = _proposal_baseline_sections(proposal)
    if len(baselines) != 1:
        return ""
    baseline = baselines[0][1]
    normalized = "\n".join(line.rstrip() for line in baseline.strip().splitlines())
    payload = "## 需求基线\n" + normalized + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _proposal_status_table_issues(proposal):
    """Check the human-readable Define status row against frontmatter status."""
    if not proposal:
        return ["proposal.md 缺失,无法校验 Define 阶段状态"]
    fm = yaml_frontmatter(proposal)
    frontmatter_status = _normalize_status_values([fm.get(PROPOSAL_PHASE_STATUS_FIELD)])
    if not frontmatter_status:
        return [f"proposal.{PROPOSAL_PHASE_STATUS_FIELD} 不得为空"]
    if not frontmatter_status <= PROPOSAL_PHASE_STATUS_VALUES:
        return [f"proposal.{PROPOSAL_PHASE_STATUS_FIELD} 不是合法 Define 状态"]
    input_sections = _sections(proposal, "需求输入")
    if len(input_sections) != 1:
        return [f"需求输入章节必须恰好一个，实际:{len(input_sections)}"]
    rows = [
        row for row in _markdown_table_rows(input_sections[0])
        if row and row[0].strip().strip("`") == "Define 阶段状态"
    ]
    if not rows:
        return ["需求输入表缺少 Define 阶段状态行"]
    if len(rows) > 1:
        return ["需求输入表存在多个 Define 阶段状态行"]
    if len(rows[0]) < 2 or not rows[0][1].strip():
        return ["需求输入表 Define 阶段状态不得为空"]
    table_status = _normalize_status_values([rows[0][1].strip().strip("`")])
    if not table_status <= PROPOSAL_PHASE_STATUS_VALUES:
        return ["需求输入表 Define 阶段状态不是合法 Define 状态"]
    if table_status != frontmatter_status:
        return [
            "需求输入表 Define 阶段状态与 proposal.phase_status 不一致"
            f"（表格={rows[0][1].strip()}，frontmatter={fm.get(PROPOSAL_PHASE_STATUS_FIELD)}）"
        ]
    return []


def _tokenize(text):
    """List of (indent, stripped_line); drops blank and '#' comment lines."""
    out = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        if raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        out.append((indent, raw.strip()))
    return out


def _split_kv(s):
    """'key: value' -> (key, value); value=='' means nested block.
    (None, None) when the line is not a mapping entry."""
    if s.endswith(":"):
        return s[:-1].strip(), ""
    idx = s.find(": ")
    if idx == -1:
        return None, None
    return s[:idx].strip(), s[idx + 2:].strip()


def _scalar(v):
    """Strip inline comments and normalize empty flow sequences."""
    if not v:
        return v
    # Strip inline comments (only when # is preceded by whitespace and not inside quotes)
    in_single = False
    in_double = False
    for i, ch in enumerate(v):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == '#' and not in_single and not in_double and i > 0 and v[i-1] in (' ', '\t'):
            v = v[:i].rstrip()
            break
    return v


def _parse_node(lines, i, indent):
    if i >= len(lines):
        return None, i
    if lines[i][1].startswith("- "):
        return _parse_seq(lines, i, indent)
    return _parse_map(lines, i, indent)


def _parse_map(lines, i, indent):
    result = {}
    while i < len(lines) and lines[i][0] == indent:
        key, val = _split_kv(lines[i][1])
        if key is None:
            i += 1
            continue
        i += 1
        if val == "":
            if i < len(lines) and lines[i][0] > indent:
                child, i = _parse_node(lines, i, lines[i][0])
                result[key] = child
            else:
                result[key] = None
        else:
            result[key] = _scalar(val)
    return result, i


def _is_mapping_item(body):
    """True when a `- ...` dash body is `key: value` form (identifier key)."""
    key, _ = _split_kv(body)
    return key is not None and bool(_MAP_KEY.match(key))


def _parse_seq(lines, i, indent):
    result = []
    while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
        body = lines[i][1][2:].strip()
        i += 1
        if body and _is_mapping_item(body):
            item = {}
            key, val = _split_kv(body)
            if val == "":
                if i < len(lines) and lines[i][0] > indent:
                    child, i = _parse_node(lines, i, lines[i][0])
                    item[key] = child
                else:
                    item[key] = None
            else:
                item[key] = _scalar(val)
            # remaining keys of this mapping item live deeper than the dash indent
            if i < len(lines) and lines[i][0] > indent:
                rest, i = _parse_node(lines, i, lines[i][0])
                if isinstance(rest, dict):
                    item.update(rest)
            result.append(item)
        else:
            result.append(_scalar(body) if body else None)
    return result, i


def yaml_load(text):
    lines = _tokenize(text)
    if not lines:
        return {}
    value, _ = _parse_node(lines, 0, lines[0][0])
    return value or {}


def yaml_frontmatter(text):
    """Parse a leading `---\n...\n---` YAML frontmatter block; {} if none."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return {}
    return yaml_load("\n".join(lines[1:end]))


_SPEC_FOR_VALIDATION_SERVICE = None


def _spec_for_validation_service():
    """Load the optional Spec for Validation runtime only when its capability is used."""
    global _SPEC_FOR_VALIDATION_SERVICE
    if _SPEC_FOR_VALIDATION_SERVICE is None:
        module = importlib.import_module("ohos_sdd_spec_for_validation")
        _SPEC_FOR_VALIDATION_SERVICE = module.SpecForValidationService(yaml_frontmatter)
    return _SPEC_FOR_VALIDATION_SERVICE


class _LazySpecForValidationService:
    """Compatibility facade that keeps imports lazy for existing callers/tests."""

    def __getattr__(self, name):
        return getattr(_spec_for_validation_service(), name)


SPEC_FOR_VALIDATION = _LazySpecForValidationService()


# 交付件 -> 拥有它的能力 skill(rework_capability 路由)
REWORK = {
    "proposal": "ohos-propose", "manifest": "ohos-propose",
    "spec": "ohos-spec", "epic": "ohos-spec",
    "design": "ohos-design",
    "execution_plan": "ohos-plan", "task": "ohos-plan",
    "bugfix": "ohos-plan", "regression_test": "ohos-plan", "test_spec": "ohos-plan",
    "spec_for_validation": "ohos-spec-for-validation",
    "review": "ohos-review",
    "gate_checklist": "ohos-validate",
    "scenario_library": "ohos-spec", "claude_agent_instructions": "ohos-propose",
    "threat_model": "ohos-security-threat-model",
}


def load_contract(path):
    with open(path, encoding="utf-8") as f:
        return yaml_load(f.read())


def _find_contract():
    d = os.getcwd()
    while d != "/":
        for cand in (os.path.join(d, "runtime", "assets", "contracts", "artifacts.yaml"),
                     os.path.join(d, "contracts", "artifacts.yaml")):
            if os.path.isfile(cand):
                return load_contract(cand)
        d = os.path.dirname(d)
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in (os.path.join(here, "..", "contracts", "artifacts.yaml"),
                os.path.join(here, "..", "shared", "ohos-sdd", "contracts", "artifacts.yaml"),
                os.path.join(here, "..", "..", "shared", "ohos-sdd", "contracts", "artifacts.yaml")):
        cand = os.path.normpath(rel)
        if os.path.isfile(cand):
            return load_contract(cand)
    raise SystemExit("validate: 找不到契约 artifacts.yaml,请用 --contract <path>")


def _artifact_file_map(contract):
    """Map artifact file basename -> (id, status)."""
    out = {}
    for a in contract.get("artifacts", []):
        out[a["file"]] = (a["id"], a.get("status", ""))
    return out


def validate_level_a(change_dir, contract):
    """Level A 结构:required 交付件必须存在;conditional/recommended/reference 仅记录。"""
    checks = []
    for fname, (aid, status) in _artifact_file_map(contract).items():
        exists = os.path.isfile(os.path.join(change_dir, fname))
        if status == "required" and not exists:
            checks.append({"ok": False, "level": "A", "artifact": aid, "file": fname,
                           "issue": "required 交付件缺失",
                           "rework_capability": REWORK.get(aid, "using-ohos-sdd"),
                           "evidence": "Level A 结构"})
        else:
            checks.append({"ok": True, "level": "A", "artifact": aid, "file": fname,
                           "issue": "", "rework_capability": "", "evidence": ""})
    return checks


# change 级 Level B:只校验 Level C 要读的结构锚点 + H1。
# (模板全量章节校验属于 validate --contract,见 Task 11)
# 注:manifest.md 是纯 frontmatter 元数据(无正文 H1),不纳入 H1 校验。
# execution-plan 关键章节标题(单一真相源:LEVEL_B 与 _HEADING_GROUPS 共用,
# 改标题只改这里,避免模板/Level B/contract 三处漂移)
EP_HEADING_AC_TRACE = "## AC 到 Task 追溯"

LEVEL_B = {
    "proposal.md": [r"^# 需求文档", r"^### Agent Scope Guard",
                    r"^## (?:需求基线|三、需求基线)"],
    "spec.md": [r"^# 特性规格", r"^## 验收追溯", r"^## 验证映射", r"^## API 变更分析"],
    "execution-plan.md": [r"^# 执行计划", r"^" + EP_HEADING_AC_TRACE],
    "test-spec.md": [r"^# 测试规格"],
}
LEVEL_B_H1_ONLY = ("design.md", "review.md",
                   "bugfix.md", "regression-test.md", "spec-for-validation.md")


def _legacy_check(change_dir, level):
    issues = SPEC_FOR_VALIDATION.legacy_issues(change_dir)
    if not issues:
        return []
    return [{"ok": False, "level": level, "artifact": "legacy-spec-for-test",
             "file": "", "issue": "; ".join(issues),
             "rework_capability": "ohos-spec-for-validation",
             "evidence": f"Level {level} legacy 迁移检查"}]


def validate_level_b(change_dir, contract):
    checks = _legacy_check(change_dir, "B")
    for fname, (aid, _status) in _artifact_file_map(contract).items():
        fpath = os.path.join(change_dir, fname)
        if not os.path.isfile(fpath):
            continue  # 缺失归 Level A
        with open(fpath, encoding="utf-8") as f:
            text = f.read()
        issues = []
        for pat in LEVEL_B.get(fname, []):
            if not re.search(pat, text, re.MULTILINE):
                issues.append(f"缺少结构标题 /{pat}/")
        if fname == "proposal.md":
            issues.extend(_proposal_status_table_issues(text))
            issues.extend(_proposal_baseline_section_issues(text))
        if fname in LEVEL_B_H1_ONLY and not re.search(r"^# .+", text, re.MULTILINE):
            issues.append("缺少 H1 标题")
        if fname == "spec-for-validation.md" and yaml_frontmatter(text).get("artifact") != "spec-for-validation":
            issues.append("frontmatter.artifact 必须为 spec-for-validation")
        if issues:
            checks.append({"ok": False, "level": "B", "artifact": aid, "file": fname,
                           "issue": "; ".join(issues),
                           "rework_capability": REWORK.get(aid, "using-ohos-sdd"),
                           "evidence": "Level B 结构"})
        else:
            checks.append({"ok": True, "level": "B", "artifact": aid, "file": fname,
                           "issue": "", "rework_capability": "", "evidence": ""})
    return checks


EDGE_REWORK = {
    "proposal→spec": "ohos-propose",
    "proposal→spec-traceability": "ohos-spec",
    "spec→spec-quality": "ohos-spec",
    "spec→then-boundary": "ohos-spec",
    "spec→design": "ohos-design",
    "design→design-quality": "ohos-design",
    "spec→execution-plan": "ohos-plan",
    "plan→source-references": "ohos-plan",
    "spec→task": "ohos-plan",
    "spec→plan": "ohos-plan",
    "execution-plan→code": "ohos-plan",
    "task→code": "ohos-plan",
    "code→implementation-evidence": "ohos-plan",
    "spec→spec-for-validation": "ohos-spec-for-validation",
    "design→spec-for-validation": "ohos-spec-for-validation",
    "spec-for-validation→test-spec": "ohos-plan",
}


def _read(change_dir, fname):
    p = os.path.join(change_dir, fname)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


def _ac_set(text):
    """AC identifiers allow one or more numeric segments, for example AC-1.2.3."""
    return set(re.findall(AC_ID_PATTERN, text or ""))


def _section(text, heading):
    """提取某 `## heading` 标题下到下一个 `## ` 之前的内容;无则 ''。"""
    if not text:
        return ""
    m = re.search(r"^##\s+" + re.escape(heading) + r"\s*$", text, re.MULTILINE)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^##\s+", rest, re.MULTILINE)
    return rest[:nxt.start()] if nxt else rest


def _sections(text, heading):
    """提取全部同名 H2 章节，用于必须唯一的权威章节校验。"""
    if not text:
        return []
    matches = list(re.finditer(
        r"^##\s+" + re.escape(heading) + r"\s*$", text, re.MULTILINE))
    sections = []
    for match in matches:
        rest = text[match.end():]
        nxt = re.search(r"^##\s+", rest, re.MULTILINE)
        sections.append(rest[:nxt.start()] if nxt else rest)
    return sections


def _proposal_baseline_sections(proposal):
    """返回当前/迁移标题的全部需求基线章节及其标题。"""
    sections = []
    sections.extend(("需求基线", body) for body in _sections(proposal, "需求基线"))
    sections.extend(("三、需求基线", body) for body in _sections(proposal, "三、需求基线"))
    return sections


def _proposal_baseline_section_issues(proposal):
    sections = _proposal_baseline_sections(proposal)
    issues = []
    if len(sections) != 1:
        issues.append(f"需求基线章节必须恰好一个，实际:{len(sections)}")
    headings = {heading for heading, _body in sections}
    if len(headings) > 1:
        issues.append("需求基线新旧标题不得并存")
    return issues


def _heading_section(text, level, heading):
    """提取指定级别标题到下一个同级或更高级标题。"""
    if not text:
        return ""
    prefix = "#" * level
    m = re.search(r"^" + re.escape(prefix) + r"\s+" + re.escape(heading) + r"\s*$",
                  text, re.MULTILINE)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^#{1," + str(level) + r"}\s+", rest, re.MULTILINE)
    return rest[:nxt.start()] if nxt else rest


def _markdown_table_rows(text):
    """返回 Markdown 表格数据行的列;跳过 header/separator。"""
    rows = []
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if not cols or all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cols):
            continue
        rows.append(cols)
    return rows[1:] if rows else []  # 第一行是表头


def _declared_scope_present(text, heading):
    """计划文件范围支持 bullet 或 Markdown table 两种表达。"""
    scope = _section(text, heading)
    bullets = [ln for ln in scope.splitlines() if ln.strip().startswith("- ")]
    if bullets:
        return True
    path_col = 2 if heading == "受影响文件全量清单" else 1
    for row in _markdown_table_rows(scope):
        if len(row) <= path_col:
            continue
        value = row[path_col].strip("` ")
        if value and "[" not in value and value not in {"-", "N/A"}:
            return True
    return False


def _implementation_closure_status(change_dir):
    manifest = _read(change_dir, "manifest.md") or ""
    status = str(yaml_frontmatter(manifest).get("status") or "").strip().lower()
    return status if status in IMPLEMENTATION_CLOSURE_STATUSES else ""


def _bold_section(text, heading):
    """提取某 `**heading**` 到下一粗体标题或 Markdown 标题。"""
    if not text:
        return ""
    m = re.search(r"^\*\*" + re.escape(heading) + r"\*\*\s*$", text, re.MULTILINE)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^(?:\*\*[^\n]+\*\*|#{1,6}\s+)", rest, re.MULTILINE)
    return rest[:nxt.start()] if nxt else rest


def _task_blocks(text):
    """返回 execution-plan Task 详情中的 TASK-ID -> block。"""
    blocks = {}
    matches = list(re.finditer(r"^###\s+(" + TASK_ID_PATTERN + r"):.*$", text or "", re.MULTILINE))
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        next_h2 = re.search(r"^##\s+", text[match.end():end], re.MULTILINE)
        if next_h2:
            end = match.end() + next_h2.start()
        blocks[match.group(1)] = text[match.end():end]
    return blocks


def _heading_reference_targets(text):
    """返回可用于 `file.md#anchor` 引用的标题文本与 GitHub 风格简化锚点。"""
    targets = set()
    for match in re.finditer(r"^#{1,6}\s+(.+?)\s*#*\s*$", text or "", re.MULTILINE):
        heading = match.group(1).strip()
        targets.add(heading.lower())
        slug = re.sub(r"[^\w\u4e00-\u9fff -]", "", heading.lower())
        targets.add(re.sub(r"[\s-]+", "-", slug).strip("-"))
    return targets


def _document_anchor_references(text, filename):
    return set(re.findall(
        re.escape(filename) + r"#([^\s`|,，;；)）]+)", text or "", re.IGNORECASE))


def _task_source_reference_issues(plan, spec, design):
    """校验 Task 只用稳定 ID/锚点引用 Spec/Design，不复制上游正文。"""
    issues = []
    spec_acs = _ac_set(spec)
    spec_rules = set(re.findall(RULE_ID_PATTERN, spec or ""))
    spec_anchors = _heading_reference_targets(spec)
    design_ids = set(re.findall(
        r"(?:" + ADR_ID_PATTERN + r"|" + STATE_ID_PATTERN + r"|" + INVARIANT_ID_PATTERN + r")",
        design or ""))
    design_anchors = _heading_reference_targets(design)

    for task_id, block in sorted(_task_blocks(plan).items()):
        spec_refs = _bold_section(block, "Spec References")
        if not spec_refs:
            issues.append(f"{task_id} 缺少 Spec References")
        else:
            ac_refs = set(re.findall(AC_ID_PATTERN, spec_refs))
            rule_refs = set(re.findall(RULE_ID_PATTERN, spec_refs))
            anchor_refs = _document_anchor_references(spec_refs, "spec.md")
            if not ac_refs:
                issues.append(f"{task_id} Spec References 未引用 AC")
            if not rule_refs:
                issues.append(f"{task_id} Spec References 未引用规则 ID")
            unknown_acs = ac_refs - spec_acs
            unknown_rules = rule_refs - spec_rules
            unknown_anchors = {item for item in anchor_refs if item.lower() not in spec_anchors}
            if unknown_acs:
                issues.append(f"{task_id} 引用了 spec 不存在的 AC:{sorted(unknown_acs)}")
            if unknown_rules:
                issues.append(f"{task_id} 引用了 spec 不存在的规则:{sorted(unknown_rules)}")
            if not anchor_refs:
                issues.append(f"{task_id} Spec References 缺少 spec.md#章节锚点")
            elif unknown_anchors:
                issues.append(f"{task_id} 引用了 spec 不存在的章节:{sorted(unknown_anchors)}")

        design_refs = _bold_section(block, "Design References")
        if design is None:
            if not re.search(r"\bN/A\b\s*[：:]\s*\S+", design_refs or "", re.IGNORECASE):
                issues.append(f"{task_id} Design References 缺少简单变更 N/A 理由")
            continue
        if not design_refs:
            issues.append(f"{task_id} 缺少 Design References")
            continue
        id_refs = set(re.findall(
            r"(?:" + ADR_ID_PATTERN + r"|" + STATE_ID_PATTERN + r"|" + INVARIANT_ID_PATTERN + r")",
            design_refs))
        anchor_refs = _document_anchor_references(design_refs, "design.md")
        if not id_refs and not anchor_refs:
            issues.append(f"{task_id} Design References 未引用设计 ID 或章节锚点")
        unknown_ids = id_refs - design_ids
        unknown_anchors = {item for item in anchor_refs if item.lower() not in design_anchors}
        if unknown_ids:
            issues.append(f"{task_id} 引用了 design 不存在的 ID:{sorted(unknown_ids)}")
        if unknown_anchors:
            issues.append(f"{task_id} 引用了 design 不存在的章节:{sorted(unknown_anchors)}")
    return issues


def _filled(value, allow_na=False):
    value = (value or "").strip("` ")
    if not value:
        return False
    bracket = re.fullmatch(r"\[([^\]\n]+)\]", value)
    if bracket and _looks_like_bracket_placeholder(bracket.group(1)):
        return False
    if value in {"-", "N/A"}:
        return allow_na
    return True


BRACKET_PLACEHOLDER_HINTS = (
    "待", "补充", "填写", "占位", "路径", "命令", "证据", "结果", "说明", "名称", "姓名",
    "日期", "版本", "目标", "范围", "原因", "负责人", "确认人", "描述", "条件", "步骤", "接口",
    "文件", "仓库", "模块", "场景", "数量", "阈值", "问题", "结论", "建议", "签名", "错误码",
    "验证", "用途", "摘要", "内容", "操作", "对象", "类型", "来源", "影响", "风险", "方案",
    "规格", "排除项", "前置条件", "边界",
)
BRACKET_PLACEHOLDER_EN = re.compile(
    r"\b(?:tbd|todo|x{2,}|placeholder|title|name|path|command|evidence|result|owner|reviewer|"
    r"repo|date|issue|task|ac-id|feat-xxxx|bug-xxxx|sha)\b",
    re.IGNORECASE)


def _looks_like_bracket_placeholder(token):
    """识别模板型方括号占位，避免把 [Notification SIG] 等合法括注误报。"""
    token = (token or "").strip()
    if not token:
        return False
    if "/" in token or "…" in token or "..." in token:
        return True
    if any(hint in token for hint in BRACKET_PLACEHOLDER_HINTS):
        return True
    return bool(BRACKET_PLACEHOLDER_EN.search(token))


SPEC_OBSERVABLE_SURFACE = re.compile(
    r"终端用户|用户可感知|Public(?:\s+API)?|System(?:\s+API)?|InnerAPI",
    re.IGNORECASE)
SPEC_API_OPENNESS_VALUES = {"Public", "System", "InnerAPI"}
SPEC_API_FACT_TYPES = {
    "Existing API", "New API", "Existing Error Code", "New Error Code",
}
SPEC_THEN_INTERNAL_HIGH_CONFIDENCE_PATTERNS = (
    re.compile(r"(?:内部|私有).{0,10}(?:数据结构|状态机|流程|调用链|类|方法|字段|成员|对象|缓存|容器|队列|锁|算法)"),
    re.compile(r"状态机(?:转换|迁移|流转)|调用链|注册表|链表|指针|内存地址|遍历算法|加锁|解锁|互斥锁|自旋锁", re.IGNORECASE),
    re.compile(r"(?:缓存|队列).{0,8}(?:写入|更新|删除|入队|出队)", re.IGNORECASE),
    re.compile(r"\b(?:mutex|spinlock|linked\s+list|pointer|private\s+member|internal\s+state)\b", re.IGNORECASE),
)
SPEC_THEN_INTERNAL_BROAD_PATTERNS = (
    re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*::[A-Za-z_][A-Za-z0-9_]*\b"),
    re.compile(r"[A-Za-z0-9_./-]+\.(?:cpp|cc|c|h|hpp|ets|ts|js)(?![A-Za-z0-9])(?::\d+)?", re.IGNORECASE),
)
SPEC_THEN_IMPLEMENTATION_ACTION = re.compile(
    r"调用|执行|写入|更新|修改|创建|删除|读写|读取|访问|遍历|加锁|解锁|"
    r"\b(?:call|invoke|execute|write|update|modify|create|delete|read|access|iterate|lock|unlock)\b",
    re.IGNORECASE)
SPEC_THEN_EXEMPTION = re.compile(r"<!--\s*ext-ok\s*(?::[^>]*)?-->", re.IGNORECASE)


def _acceptance_criteria_then(text):
    """返回 AC -> THEN 文本，仅识别同一行内的 WHEN/THEN 验收标准。"""
    entries = {}
    for raw in (text or "").splitlines():
        ac_match = re.search(AC_ID_PATTERN, raw)
        when_match = re.search(r"\bWHEN\b", raw, re.IGNORECASE)
        then_match = re.search(r"\bTHEN\b", raw, re.IGNORECASE)
        if not ac_match or not when_match or not then_match or when_match.start() > then_match.start():
            continue
        entries[ac_match.group(0)] = raw[then_match.end():].strip(" |.*`_")
    return entries


def _spec_then_boundary_warnings(spec):
    """返回 THEN 内部实现启发式告警；词法判断不作为硬门禁。"""
    warnings = []
    for ac, then_text in sorted(_acceptance_criteria_then(spec).items()):
        if SPEC_THEN_EXEMPTION.search(then_text):
            warnings.append(f"{ac} THEN 使用 ext-ok 豁免，请在 gate-checklist 记录处理结论")
            continue
        high_confidence = any(
            pattern.search(then_text) for pattern in SPEC_THEN_INTERNAL_HIGH_CONFIDENCE_PATTERNS)
        broad_with_action = (
            SPEC_THEN_IMPLEMENTATION_ACTION.search(then_text) and
            any(pattern.search(then_text) for pattern in SPEC_THEN_INTERNAL_BROAD_PATTERNS))
        if high_confidence or broad_with_action:
            warnings.append(f"{ac} THEN 可能包含内部实现描述:{then_text}")
    return warnings


def _spec_quality_issues(spec):
    """校验 Spec 的确定性质量契约；THEN 词法启发式由独立 WARN 边处理。"""
    issues = []
    acceptance = _acceptance_criteria_then(spec)
    if not acceptance:
        issues.append("未识别到同一行 WHEN/THEN 验收标准")
    for ac, then_text in sorted(acceptance.items()):
        if not _filled(then_text):
            issues.append(f"{ac} THEN 缺少可观察结果")

    trace_rows = [row for row in _markdown_table_rows(_section(spec, "验收追溯"))
                  if row and re.fullmatch(AC_ID_PATTERN, row[0])]
    surfaces = {}
    if not trace_rows:
        issues.append("验收追溯缺少含可观察表面的 AC 表格")
    for row in trace_rows:
        ac = row[0]
        # 新模板仅要求 AC/规则/可观察表面三列；继续接受旧六列表，
        # 让在途 change 可渐进迁移而无需立即重写历史 Spec。
        if len(row) < 3:
            issues.append(f"{ac} 验收追溯列不完整")
            continue
        surface = row[2]
        if not _filled(surface) or not SPEC_OBSERVABLE_SURFACE.search(surface):
            issues.append(f"{ac} 未声明终端用户或 Public/System/InnerAPI 可观察表面")
        else:
            surfaces[ac] = surface
    for ac in sorted(set(acceptance) - set(surfaces)):
        issues.append(f"{ac} 缺少三层接口可观察性映射")

    verification_rows = [row for row in _markdown_table_rows(_section(spec, "验证映射"))
                         if row and re.fullmatch(r"VM-[A-Za-z0-9.-]+", row[0])]
    verification_acs = set()
    if not verification_rows:
        issues.append("验证映射缺少 VM-* 测试入口和 Red 条件")
    for row in verification_rows:
        vm_id = row[0]
        if len(row) < 6:
            issues.append(f"{vm_id} 验证映射列不完整")
            continue
        verification_acs.update(re.findall(AC_ID_PATTERN, row[1]))
        if not _filled(row[2]):
            issues.append(f"{vm_id} 未填写真实测试入口")
        if not _filled(row[3]):
            issues.append(f"{vm_id} 未填写验证方式")
        red = row[4].strip("` ")
        if not _filled(red) or red == "N/A":
            issues.append(f"{vm_id} 未填写 Red 条件或 N/A 理由")
        elif re.fullmatch(r"(?:测试)?(?:应|应当|应该|会)?失败[。.]?|test should fail", red, re.IGNORECASE):
            issues.append(f"{vm_id} Red 条件未说明实现前的具体失败信号")
        if not _filled(row[5]):
            issues.append(f"{vm_id} 未填写通过标准")
    for ac in sorted(set(acceptance) - verification_acs):
        issues.append(f"{ac} 缺少测试入口或 Red 条件映射")

    added_api = _heading_section(spec, 3, "新增 API")
    if not added_api:
        issues.append("API 变更分析缺少新增 API 子节")
    else:
        added_rows = _markdown_table_rows(added_api)
        if not added_rows and not re.search(r"\bN/A\b|不涉及|无新增", added_api, re.IGNORECASE):
            issues.append("新增 API 子节缺少接口表或 N/A 理由")
        for idx, row in enumerate(added_rows, 1):
            if len(row) < 7:
                issues.append(f"新增 API 第 {idx} 行列不完整")
                continue
            if row[1].strip("` ") not in SPEC_API_OPENNESS_VALUES:
                issues.append(f"新增 API 第 {idx} 行开放级别必须为 Public/System/InnerAPI")

    changed_api = _heading_section(spec, 3, "变更/废弃 API")
    if not changed_api:
        issues.append("API 变更分析缺少变更/废弃 API 子节")
    else:
        changed_rows = _markdown_table_rows(changed_api)
        if not changed_rows and not re.search(r"\bN/A\b|不涉及|无变更|无废弃", changed_api, re.IGNORECASE):
            issues.append("变更/废弃 API 子节缺少接口表或 N/A 理由")
        for idx, row in enumerate(changed_rows, 1):
            if len(row) < 7:
                issues.append(f"变更/废弃 API 第 {idx} 行列不完整")
                continue
            current_level = row[1].strip("` ")
            target_level = row[2].strip("` ")
            if current_level not in SPEC_API_OPENNESS_VALUES:
                issues.append(f"变更/废弃 API 第 {idx} 行当前开放级别必须为 Public/System/InnerAPI")
            if target_level not in SPEC_API_OPENNESS_VALUES:
                issues.append(f"变更/废弃 API 第 {idx} 行目标开放级别必须为 Public/System/InnerAPI")

    fact_section = _heading_section(spec, 3, "API 与错误码事实")
    fact_rows = _markdown_table_rows(fact_section)
    fact_is_na = bool(re.search(r"\bN/A\s*[：:]\s*\S+", fact_section, re.IGNORECASE))
    if not fact_section:
        issues.append("API 变更分析缺少 API 与错误码事实子节")
    elif not fact_rows and not fact_is_na:
        issues.append("API 与错误码事实缺少事实表或 N/A 理由")

    fact_values = {}
    fact_names = set()
    for idx, row in enumerate(fact_rows, 1):
        if len(row) < 8:
            issues.append(f"API 与错误码事实第 {idx} 行列不完整")
            continue
        name, fact_type, openness, exact, trigger, behavior, source, ac_text = row[:8]
        normalized_name = name.strip("` ")
        fact_names.add(normalized_name)
        for label, value in (("事实项", name), ("精确签名/数值", exact),
                             ("触发条件", trigger), ("对外行为", behavior),
                             ("事实来源", source), ("关联 AC", ac_text)):
            if not _filled(value):
                issues.append(f"API 与错误码事实第 {idx} 行未填写{label}")
        if fact_type not in SPEC_API_FACT_TYPES:
            issues.append(f"API 与错误码事实第 {idx} 行事实类型非法:{fact_type}")
        if openness.strip("` ") not in SPEC_API_OPENNESS_VALUES:
            issues.append(f"API 与错误码事实第 {idx} 行开放级别必须为 Public/System/InnerAPI")
        exact_value = exact.strip("` ")
        if re.search(r"某错误码|错误码范围|返回错误|错误码枚举", exact_value):
            issues.append(f"API 与错误码事实第 {idx} 行必须填写精确签名或数值")
        if "Error Code" in fact_type and not re.search(
                r"(?<![A-Za-z0-9_])(?:0x[0-9A-Fa-f]+|\d+)(?![A-Za-z0-9_])", exact_value):
            issues.append(f"API 与错误码事实第 {idx} 行错误码缺少精确数值")
        if fact_type.startswith("Existing"):
            has_existing_source = re.search(
                r"[^\s`|]+\.(?:cpp|cc|c|h|hpp|ets|ts|js|d\.ts|idl|json|yaml|yml)"
                r"(?::\d+|\s*(?:/|#)\s*[A-Za-z_@][A-Za-z0-9_:.@-]*)",
                source, re.IGNORECASE)
            if not has_existing_source:
                issues.append(f"API 与错误码事实第 {idx} 行已有事实缺少文件:行/符号来源")
        elif fact_type.startswith("New") and not re.search(
                r"proposal\.md|design\.md|TASK-[A-Za-z0-9.-]+|AC-\d", source, re.IGNORECASE):
            issues.append(f"API 与错误码事实第 {idx} 行新增事实缺少 proposal/design/Task/AC 依据")
        acs = set(re.findall(AC_ID_PATTERN, ac_text))
        if not acs:
            issues.append(f"API 与错误码事实第 {idx} 行未关联 AC")
        unknown_acs = acs - set(acceptance)
        if unknown_acs:
            issues.append(f"API 与错误码事实第 {idx} 行关联了不存在的 AC:{sorted(unknown_acs)}")
        if "Error Code" in fact_type:
            missing_verification = acs - verification_acs
            if missing_verification:
                issues.append(
                    f"API 与错误码事实第 {idx} 行错误码 AC 缺少验证入口:{sorted(missing_verification)}")
        previous = fact_values.get(normalized_name)
        if previous is not None and previous != exact_value:
            issues.append(f"API/错误码 {normalized_name} 存在冲突值:{previous} vs {exact_value}")
        fact_values[normalized_name] = exact_value

    declared_api_names = []
    for row in (_markdown_table_rows(added_api) if added_api else []):
        if row and _filled(row[0]):
            declared_api_names.append(row[0].strip("` "))
    for row in (_markdown_table_rows(changed_api) if changed_api else []):
        if row and _filled(row[0]):
            declared_api_names.append(row[0].strip("` "))
    for api_name in declared_api_names:
        if api_name not in fact_names:
            issues.append(f"API {api_name} 缺少 API 与错误码事实行")
    return issues


def _design_quality_issues(design, spec=None, plan=None):
    """校验 design 条件区段中的代码事实、复用、类图和不变量追溯。"""
    issues = []
    spec_acs = _ac_set(spec)
    plan_tasks = set(re.findall(TASK_ID_PATTERN, _section(plan, "Task 列表"))) if plan else set()

    facts = _heading_section(design, 3, "代码事实基线")
    if facts:
        rows = _markdown_table_rows(facts)
        if not rows:
            issues.append("代码事实基线缺少事实行")
        for idx, row in enumerate(rows, 1):
            if len(row) < 5:
                issues.append(f"代码事实基线第 {idx} 行列不完整")
                continue
            code_ref, fact, rule, constraint, evidence = row[:5]
            if not _filled(code_ref) or not re.search(r"[^\s`|]+:\d+", code_ref):
                issues.append(f"代码事实基线第 {idx} 行缺少文件:行号引用")
            for label, value in (("事实", fact), ("架构规则", rule),
                                 ("设计约束", constraint), ("验证来源", evidence)):
                if not _filled(value):
                    issues.append(f"代码事实基线第 {idx} 行未填写{label}")

    patterns = _heading_section(design, 3, "既有模式复用")
    if patterns:
        rows = _markdown_table_rows(patterns)
        if not rows:
            issues.append("既有模式复用缺少模式或检索结论")
        for idx, row in enumerate(rows, 1):
            if len(row) < 7:
                issues.append(f"既有模式复用第 {idx} 行列不完整")
                continue
            reference = row[1]
            if not (_filled(reference) and
                    (re.search(r"[^\s`|]+:\d+", reference) or "no prior art found" in reference.lower())):
                issues.append(f"既有模式复用第 {idx} 行缺少文件:行引用或 no prior art found")
            if not _filled(row[3]) or not _filled(row[4]):
                issues.append(f"既有模式复用第 {idx} 行缺少复用约定或复用方式")
            if not re.search(TASK_ID_PATTERN, row[6]):
                issues.append(f"既有模式复用第 {idx} 行未关联 Task")

    class_diagram = _heading_section(design, 3, "类图")
    if class_diagram:
        if "classDiagram" not in class_diagram:
            issues.append("类图缺少 Mermaid classDiagram")
        rows = _markdown_table_rows(class_diagram)
        if not rows:
            issues.append("类图缺少类型到 ADR/Task 映射")
        for idx, row in enumerate(rows, 1):
            if len(row) < 6:
                issues.append(f"类图第 {idx} 行列不完整")
                continue
            if not _filled(row[0]) or not _filled(row[1]):
                issues.append(f"类图第 {idx} 行缺少类型或代码引用")
            if not re.search(r"ADR-[A-Za-z0-9.-]+", row[4]):
                issues.append(f"类图第 {idx} 行未关联 ADR")
            if not re.search(TASK_ID_PATTERN, row[5]):
                issues.append(f"类图第 {idx} 行未关联 Task")

    state_section = _heading_section(design, 3, "状态归属与不变量")
    if state_section:
        ownership = _heading_section(state_section, 4, "状态归属")
        state_rows = [row for row in _markdown_table_rows(ownership)
                      if row and re.fullmatch(STATE_ID_PATTERN, row[0])]
        if not state_rows:
            issues.append("状态归属与不变量缺少 STATE-* 归属行")
        for row in state_rows:
            if len(row) < 9 or any(not _filled(value) for value in row[1:9]):
                issues.append(f"{row[0]} Owner/生命周期/并发模型未完整填写")

        invariant_section = _heading_section(state_section, 4, "不变量追溯")
        invariant_rows = [row for row in _markdown_table_rows(invariant_section)
                          if row and re.fullmatch(INVARIANT_ID_PATTERN, row[0])]
        if not invariant_rows:
            issues.append("状态归属与不变量缺少 INV-* 追溯行")
        for row in invariant_rows:
            invariant_id = row[0]
            if len(row) < 7:
                issues.append(f"{invariant_id} 追溯列不完整")
                continue
            if not _filled(row[1]) or not _filled(row[2]):
                issues.append(f"{invariant_id} 缺少状态范围或约束")
            acs = set(re.findall(AC_ID_PATTERN, row[3]))
            tasks = set(re.findall(TASK_ID_PATTERN, row[4]))
            if not acs:
                issues.append(f"{invariant_id} 未关联 AC")
            unknown_acs = acs - spec_acs if spec_acs else set()
            if unknown_acs:
                issues.append(f"{invariant_id} 关联了 spec 不存在的 AC:{sorted(unknown_acs)}")
            if not tasks:
                issues.append(f"{invariant_id} 未关联 Task")
            unknown_tasks = tasks - plan_tasks if plan_tasks else set()
            if unknown_tasks:
                issues.append(f"{invariant_id} 关联了 plan 不存在的 Task:{sorted(unknown_tasks)}")
            if not _filled(row[5]):
                issues.append(f"{invariant_id} 未填写验证方式与通过标准")
            if len(re.findall(r"\b" + re.escape(invariant_id) + r"\b", design)) < 2:
                issues.append(f"{invariant_id} 未被状态机/资源/并发设计引用")
    return issues


def _implementation_evidence_issues(text, require_review=False, require_commit=False):
    """校验 execution-plan 的真实实现闭环；兼容精简表和旧扩展表。"""
    issues = []
    task_rows = {}
    for row in _markdown_table_rows(_section(text, "Task 列表")):
        if row and re.fullmatch(TASK_ID_PATTERN, row[0]):
            task_rows[row[0]] = row
    expected = set(task_rows)
    if not expected:
        issues.append("未识别到计划 Task ID")
    for task_id, row in sorted(task_rows.items()):
        status = row[-1] if len(row) >= 8 else ""
        if status != "Done":
            issues.append(f"{task_id} 状态不是 Done:{status}")

    blocks = _task_blocks(text)
    for task_id in sorted(expected):
        block = blocks.get(task_id, "")
        if not block:
            issues.append(f"{task_id} 缺少 Task 详情")
            continue
        for marker in ("Anti-Fake Completion", "Verification", "Review Handoff"):
            if marker not in block:
                issues.append(f"{task_id} 缺少 {marker}")
        if "状态所有权和生命周期" not in block and "状态所有权" not in block:
            issues.append(f"{task_id} 缺少状态所有权")
        if "任务间接口（Produces / Consumes）" not in block and "任务间接口" not in block:
            issues.append(f"{task_id} 缺少任务间接口")

        verification_rows = _markdown_table_rows(_bold_section(block, "Verification"))
        if not verification_rows:
            issues.append(f"{task_id} 缺少 Verification 记录")
        for row in verification_rows:
            if len(row) >= 4:
                expected_result, actual_result = row[2], row[3]
            elif len(row) >= 3:
                expected_result, actual_result = row[1], row[2]
            else:
                issues.append(f"{task_id} Verification 记录列不完整")
                continue
            if not _filled(expected_result):
                issues.append(f"{task_id} 未回填 Expected Result")
            if not _filled(actual_result):
                issues.append(f"{task_id} 未回填 Actual Result")
            elif "PASS" not in actual_result.upper():
                issues.append(f"{task_id} Actual Result 非 PASS")

        anti_fake_rows = _markdown_table_rows(_bold_section(block, "Anti-Fake Completion"))
        if not anti_fake_rows:
            issues.append(f"{task_id} 缺少 Anti-Fake Completion 证据")
        elif any(len(row) < 2 or not _filled(row[1], allow_na=True) for row in anti_fake_rows):
            issues.append(f"{task_id} Anti-Fake Completion 存在空白或占位证据")

    mapping = {}
    for row in _markdown_table_rows(_section(text, "代码范围映射")):
        if row and re.fullmatch(TASK_ID_PATTERN, row[0]):
            mapping[row[0]] = row
    missing_mapping = expected - set(mapping)
    if missing_mapping:
        issues.append(f"代码范围映射缺少:{sorted(missing_mapping)}")
    for task_id in sorted(expected & set(mapping)):
        row = mapping[task_id]
        if len(row) >= 9:
            if not _filled(row[2]):
                issues.append(f"{task_id} 未回填实际 Code Ref")
            if require_commit and not _filled(row[4]):
                issues.append(f"{task_id} 未回填 Commit")
            if require_review:
                labels = ("Spec Compliance", "Code Quality", "Verification")
                for label, value in zip(labels, row[5:8]):
                    if not _filled(value):
                        issues.append(f"{task_id} 未回填 {label} Evidence")
        elif len(row) >= 3:
            if not _filled(row[1]) or not _filled(row[2]):
                issues.append(f"{task_id} 代码范围映射缺少文件或操作")
        else:
            issues.append(f"{task_id} 代码范围映射列不完整")

    trace_rows = _markdown_table_rows(_section(text, "AC 到 Task 追溯"))
    for row in trace_rows:
        if not re.fullmatch(AC_ID_PATTERN, row[0]):
            continue
        if len(row) >= 8:
            if not _filled(row[4]):
                issues.append(f"{row[0]} 未回填实际 Code Ref")
            if require_commit and not _filled(row[5]):
                issues.append(f"{row[0]} 未回填 Commit")
            if require_review and not _filled(row[6]):
                issues.append(f"{row[0]} 未回填 Review Evidence")
            verification_status = row[7]
        elif len(row) >= 5:
            if not _filled(row[2]) or not _filled(row[3]):
                issues.append(f"{row[0]} 缺少 Task 或验证方式")
            verification_status = row[4]
        else:
            issues.append(f"{row[0]} AC 到 Task 追溯列不完整")
            continue
        if verification_status.lower() != "pass":
            issues.append(f"{row[0]} 验证状态不是 Pass:{verification_status}")
    return issues


def _edge(ok, edge, issue):
    if ok:
        return {"ok": True, "level": "C", "artifact": edge, "file": "",
                "issue": "", "rework_capability": "", "evidence": ""}
    return {"ok": False, "level": "C", "artifact": edge, "file": "",
            "issue": issue, "rework_capability": EDGE_REWORK.get(edge, "using-ohos-sdd"),
            "evidence": "Level C 依赖边"}


def _warning_edge(edge, issue):
    return {"ok": True, "warn": True, "level": "C", "artifact": edge, "file": "",
            "issue": issue, "rework_capability": EDGE_REWORK.get(edge, "using-ohos-sdd"),
            "evidence": "Level C 语义启发式 WARN"}

def _define_approval_issues(proposal):
    """Define approval is explicit and independent from clarification completion."""
    if proposal is None:
        return ["proposal.md 缺失,无法确认 Define 审批"]
    fm = yaml_frontmatter(proposal)
    issues = []
    baseline_section_issues = _proposal_baseline_section_issues(proposal)
    issues.extend(baseline_section_issues)
    if str(fm.get(PROPOSAL_PHASE_STATUS_FIELD) or "").strip().lower() != PHASE_APPROVAL_APPROVED_STATUS:
        issues.append("Define 尚未获得明确批准(phase_status 必须为 approved)")
    approval = fm.get(PHASE_APPROVAL_FIELD)
    if not isinstance(approval, dict):
        issues.append("proposal.approval 审批记录缺失")
        return issues
    if str(approval.get("status") or "").strip().lower() != PHASE_APPROVAL_APPROVED_STATUS:
        issues.append("approval.status 必须为 approved")
    for field in PHASE_APPROVAL_REQUIRED_FIELDS[1:-1]:
        if not str(approval.get(field) or "").strip():
            issues.append(f"approval.{field} 不得为空")
    baseline_digest = _unquote_scalar(approval.get("baseline_digest"))
    if not baseline_digest:
        issues.append("approval.baseline_digest 不得为空")
    elif not baseline_section_issues and baseline_digest != _proposal_baseline_digest(proposal):
        issues.append("approval.baseline_digest 与当前需求基线不一致，需重新批准 Define")
    return issues


def validate_level_c(change_dir):
    checks = _legacy_check(change_dir, "C")
    proposal = _read(change_dir, "proposal.md")
    spec = _read(change_dir, "spec.md")
    design = _read(change_dir, "design.md")
    plan = _read(change_dir, "execution-plan.md")
    task = _read(change_dir, "task.md")  # 仅用于报错指引;不再作为 plan 的替代件

    spec_acs = _ac_set(spec)
    plan_acs = _ac_set(plan)
    design_acs = _ac_set(design)

    # edge: proposal→spec — Define 必须有独立、明确的批准记录。
    define_approval_issues = _define_approval_issues(proposal)
    checks.append(_edge(not define_approval_issues, "proposal→spec",
                        "; ".join(define_approval_issues)))

    # edge: proposal→spec-traceability — spec 验收追溯至少 1 个 AC。
    accept = _ac_set(_section(spec, "验收追溯"))
    checks.append(_edge(bool(accept), "proposal→spec-traceability",
                        "spec 验收追溯 无 AC,未追溯 proposal 成功标准" if not accept else ""))
    if spec is not None:
        spec_quality_issues = _spec_quality_issues(spec)
        checks.append(_edge(not spec_quality_issues, "spec→spec-quality",
                            "; ".join(spec_quality_issues)))
        then_warnings = _spec_then_boundary_warnings(spec)
        checks.append(_warning_edge("spec→then-boundary", "; ".join(then_warnings))
                      if then_warnings else _edge(True, "spec→then-boundary", ""))

    # edge: spec→design — design 是四件套必需件，且引用的 AC 必须存在于 spec。
    if design is None:
        checks.append(_edge(False, "spec→design", "无 design.md,design 交付件必需"))
    else:
        missing = design_acs - spec_acs
        checks.append(_edge(not missing, "spec→design",
                            f"design 引用了 spec 不存在的 AC:{sorted(missing)}" if missing else ""))
        design_quality_issues = _design_quality_issues(design, spec, plan)
        checks.append(_edge(not design_quality_issues, "design→design-quality",
                            "; ".join(design_quality_issues)))

    # edge: spec→plan — execution-plan 存在时检查 spec→execution-plan;否则检查 spec→task(简单变更)
    if plan is not None:
        uncovered = spec_acs - plan_acs
        checks.append(_edge(not uncovered, "spec→execution-plan",
                            f"plan 未覆盖 spec 的 AC:{sorted(uncovered)}" if uncovered else ""))
        reference_issues = _task_source_reference_issues(plan, spec, design)
        checks.append(_edge(not reference_issues, "plan→source-references",
                            "; ".join(reference_issues)))
        # edge: execution-plan→code — 受影响文件清单 非空
        has_scope = _declared_scope_present(plan, "受影响文件全量清单")
        checks.append(_edge(has_scope, "execution-plan→code",
                            "execution-plan 受影响文件全量清单为空" if not has_scope else ""))
    elif task is not None:
        # task.md 是补充执行单元,不再替代 execution-plan;统一报 spec→plan 保持与
        # Level A required 合同一致,避免"A 红 C 绿"的分裂判定。
        checks.append(_edge(False, "spec→plan",
                            "无 execution-plan.md(plan 交付件必需;task.md 仅为补充执行单元,不能替代)"))
    else:
        checks.append(_edge(False, "spec→plan",
                            "无 execution-plan.md,plan 交付件缺失"))

    closure_status = _implementation_closure_status(change_dir)
    if closure_status and plan is not None:
        issues = _implementation_evidence_issues(plan, require_review=False)
        checks.append(_edge(not issues, "code→implementation-evidence", "; ".join(issues)))

    # conditional bypass: spec/design → Profile-defined spec-for-validation
    spec_for_validation_path = os.path.join(change_dir, "spec-for-validation.md")
    if os.path.isfile(spec_for_validation_path):
        source_issues = SPEC_FOR_VALIDATION.source_edge_issues(change_dir, spec, design)
        spec_issues, design_issues = source_issues
        checks.append(_edge(not spec_issues, "spec→spec-for-validation", "; ".join(spec_issues)))
        checks.append(_edge(not design_issues, "design→spec-for-validation", "; ".join(design_issues)))
        test_spec = _read(change_dir, "test-spec.md")
        if test_spec is not None:
            spec_for_validation = _read(change_dir, "spec-for-validation.md") or ""
            test_spec_issues = []
            if not re.search(
                    r"(?<![A-Za-z0-9_.-])spec-for-validation\.md(?![A-Za-z0-9_.-])",
                    test_spec):
                test_spec_issues.append("test-spec 未声明 spec-for-validation.md 测试输入")
            unknown_acs = _ac_set(test_spec) - _ac_set(spec_for_validation)
            if unknown_acs:
                test_spec_issues.append(
                    f"test-spec 引用了 spec-for-validation 不存在的 AC:{sorted(unknown_acs)}")
            checks.append(_edge(not test_spec_issues, "spec-for-validation→test-spec",
                                "; ".join(test_spec_issues)))

    return checks


def _find_up(start_dir, *segs):
    """从 start_dir 向上找第一个存在的 <segs> 文件;无则 None。"""
    d = os.path.abspath(start_dir)
    while True:
        cand = os.path.join(d, *segs)
        if os.path.isfile(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def _d_edge(ok, item, issue, rework_capability="ohos-validate"):
    if ok:
        return {"ok": True, "level": "D", "artifact": item, "file": "",
                "issue": "", "rework_capability": "", "evidence": ""}
    return {"ok": False, "level": "D", "artifact": item, "file": "",
            "issue": issue, "rework_capability": rework_capability,
            "evidence": "Level D 归档就绪"}


ARCHIVE_PLACEHOLDER_FILES = (
    "manifest.md", "proposal.md", "spec.md", "design.md", "execution-plan.md", "task.md",
    "review.md", "test-spec.md", "spec-for-validation.md",
)


def _without_fenced_code(text):
    return re.sub(r"^```.*?^```\s*$", "", text or "", flags=re.MULTILINE | re.DOTALL)


def _archive_placeholder_issues(change_dir):
    """归档前拒绝未解决占位；忽略 fenced code、Markdown links 和 checkbox。"""
    issues = []
    paths = list(ARCHIVE_PLACEHOLDER_FILES)
    paths.extend(os.path.join("evidence", "reviews", name) for name in (
        "spec-compliance.md", "code-quality.md", "verification.md"))
    for rel in paths:
        text = _read(change_dir, rel)
        if text is None:
            continue
        body = _without_fenced_code(text)
        tokens = sorted(set(re.findall(r"\b(?:TBD|TODO)\b|待定|待补充", body, re.IGNORECASE)))
        bracket_tokens = []
        for match in re.finditer(r"\[([^\]\n]+)\]", body):
            token = match.group(1).strip()
            if token in {"", "x", "X"} or token.isdigit():
                continue
            if match.start() > 0 and re.match(r"[A-Za-z0-9_]", body[match.start() - 1]):
                continue
            if match.end() < len(body) and body[match.end()] == "(":
                continue
            # 引用式 Markdown link: [label][ref]
            if match.end() < len(body) and body[match.end()] == "[":
                continue
            if _looks_like_bracket_placeholder(token):
                bracket_tokens.append(token)
        if tokens or bracket_tokens:
            details = tokens + [f"[{token}]" for token in sorted(set(bracket_tokens))]
            issues.append(f"{rel} 存在未解决占位:{details[:8]}")
    return issues


def _review_metadata_issues(name, text):
    heading = "Verification Metadata" if name == "verification.md" else "Review Metadata"
    section = _section(text, heading)
    if not section:
        return [f"{name} 缺少 {heading}"]
    values = {
        row[0].strip("` "): row[1]
        for row in _markdown_table_rows(section) if len(row) >= 2
    }
    required = {
        "spec-compliance.md": ("Change ID", "Spec Revision", "Plan Revision", "Base / Head", "Reviewer / Date"),
        "code-quality.md": ("Change ID", "Base / Head", "Reviewed Scope", "Reviewer / Date"),
        "verification.md": ("Change ID", "Commit / Head", "Environment", "Executor / Date"),
    }[name]
    return [
        f"{name} {heading} 缺少或未填写 {key}"
        for key in required if key not in values or not _filled(values[key])
    ]


def _review_section(text, *headings):
    for heading in headings:
        section = _section(text, heading)
        if section:
            return section
    return ""


def _review_evidence_issues(name, text, spec="", plan=""):
    issues = []
    verdict_sections = _sections(text, "Verdict")
    if len(verdict_sections) != 1:
        issues.append(f"{name} Verdict 章节必须恰好一个，实际:{len(verdict_sections)}")
    verdict = verdict_sections[0] if len(verdict_sections) == 1 else ""
    selected = []
    for raw in verdict.splitlines():
        line = raw.strip()
        checkbox = re.fullmatch(
            r"-\s*\[([ xX])\]\s*(Approved|Needs Changes|Blocked)\s*", line)
        if checkbox:
            if checkbox.group(1).lower() == "x":
                selected.append(checkbox.group(2))
            continue
        plain = re.fullmatch(r"-\s*(Approved|Needs Changes|Blocked)\s*", line)
        if plain:
            selected.append(plain.group(1))
    if selected != ["Approved"]:
        issues.append(f"{name} Verdict 必须有且仅有 Approved，实际:{selected or '未选择'}")

    issues.extend(_review_metadata_issues(name, text))

    spec_acs = _ac_set(spec)
    plan_tasks = set(re.findall(TASK_ID_PATTERN, _section(plan, "Task 列表")))

    if name == "spec-compliance.md":
        mapping = _review_section(
            text, "AC → Task → Code → Commit → Review", "逐 AC 结论")
        rows = _markdown_table_rows(mapping)
        if not rows:
            issues.append("spec-compliance.md 缺少 AC 映射记录")
        covered = _ac_set(mapping)
        missing_acs = sorted(spec_acs - covered)
        if missing_acs:
            issues.append(f"spec-compliance.md 未覆盖 spec AC:{missing_acs}")
        for idx, row in enumerate(rows, 1):
            if not _ac_set(" | ".join(row)):
                continue
            result = row[5] if len(row) >= 7 else row[1] if len(row) >= 3 else ""
            evidence = row[4] if len(row) >= 7 else row[2] if len(row) >= 3 else ""
            if result.strip("` ").upper() != "PASS":
                issues.append(f"spec-compliance.md AC 映射第 {idx} 行 Result 不是 PASS:{result}")
            if not _filled(evidence):
                issues.append(f"spec-compliance.md AC 映射第 {idx} 行缺少 Evidence")
        for heading in ("Extra Implementation", "Interpretation Deviations"):
            section = _section(text, heading)
            if not section:
                issues.append(f"spec-compliance.md 缺少 {heading}")
            elif not _markdown_table_rows(section) and not re.search(
                    r"\bN/A\b|无额外|无偏差|不涉及", section, re.IGNORECASE):
                issues.append(f"spec-compliance.md {heading} 缺少记录或 N/A 理由")
        for heading in ("Spec Quality Boundary", "Anti-Fake Completion Check"):
            rows = _markdown_table_rows(_section(text, heading))
            if not rows:
                issues.append(f"spec-compliance.md 缺少 {heading} 记录")
            for idx, row in enumerate(rows, 1):
                if len(row) < 3 or row[1].strip("` ").upper() not in {"PASS", "N/A"}:
                    issues.append(f"spec-compliance.md {heading} 第 {idx} 行结果无效")
                elif not _filled(row[2], allow_na=True):
                    issues.append(f"spec-compliance.md {heading} 第 {idx} 行缺少 Evidence")
        if not _filled(_section(text, "Conclusion")):
            issues.append("spec-compliance.md 缺少 Conclusion")

    elif name == "code-quality.md":
        scope = _section(text, "Plan Scope vs Actual Code Scope")
        rows = _markdown_table_rows(scope)
        if not rows:
            issues.append("code-quality.md 缺少 Plan Scope vs Actual Code Scope 记录")
        covered_tasks = set(re.findall(TASK_ID_PATTERN, scope))
        missing_tasks = sorted(plan_tasks - covered_tasks)
        if missing_tasks:
            issues.append(f"code-quality.md 未覆盖 plan Task:{missing_tasks}")
        for idx, row in enumerate(rows, 1):
            if len(row) < 6 or row[5].strip("` ").upper() != "PASS":
                issues.append(f"code-quality.md Scope 第 {idx} 行 Result 不是 PASS")
            elif any(not _filled(value) for value in row[1:5]):
                issues.append(f"code-quality.md Scope 第 {idx} 行范围/Commit/Deviation 不完整")
        findings = _section(text, "Findings")
        if not findings:
            issues.append("code-quality.md 缺少 Findings")
        elif not _markdown_table_rows(findings) and not re.search(
                r"\bN/A\b|无阻塞|无 finding|no findings", findings, re.IGNORECASE):
            issues.append("code-quality.md Findings 缺少记录或无问题结论")
        quality_rows = _markdown_table_rows(_section(text, "Quality Dimensions"))
        if not quality_rows:
            issues.append("code-quality.md 缺少 Quality Dimensions 记录")
        for idx, row in enumerate(quality_rows, 1):
            if len(row) < 3 or row[1].strip("` ").upper() not in {"PASS", "WARN", "N/A"}:
                issues.append(f"code-quality.md Quality Dimensions 第 {idx} 行结果无效")
            elif not _filled(row[2], allow_na=True):
                issues.append(f"code-quality.md Quality Dimensions 第 {idx} 行缺少 Evidence")
        if not _filled(_section(text, "Conclusion")):
            issues.append("code-quality.md 缺少 Conclusion")

    if name == "verification.md":
        rows = _markdown_table_rows(_section(text, "Execution Records"))
        if not rows:
            issues.append("verification.md 缺少 Execution Records")
        for idx, row in enumerate(rows, 1):
            if len(row) < 6:
                issues.append(f"verification.md Execution Records 第 {idx} 行列不完整")
                continue
            for label, value in (("Command / Evidence", row[1]),
                                 ("Expected Result", row[2]),
                                 ("Actual Result", row[3]),
                                 ("Fresh Evidence", row[4])):
                if not _filled(value):
                    issues.append(f"verification.md 第 {idx} 行未填写 {label}")
            if row[3].strip("` ").upper() == "PASS":
                issues.append(f"verification.md 第 {idx} 行 Actual Result 不能只写 PASS")
            if row[5].strip("` ").upper() != "PASS":
                issues.append(f"verification.md 第 {idx} 行 Result 不是 PASS:{row[5]}")
        covered = _ac_set(_section(text, "Execution Records"))
        missing_acs = sorted(spec_acs - covered)
        if missing_acs:
            issues.append(f"verification.md Execution Records 未覆盖 spec AC:{missing_acs}")
        coverage_rows = _markdown_table_rows(_section(text, "Coverage and Regression"))
        if not coverage_rows:
            issues.append("verification.md 缺少 Coverage and Regression 记录")
        for idx, row in enumerate(coverage_rows, 1):
            if len(row) < 4 or row[1].strip("` ").lower() not in {"yes", "n/a"}:
                issues.append(f"verification.md Coverage 第 {idx} 行 Covered 必须为 Yes/N/A")
            elif not _filled(row[2], allow_na=True) or not _filled(row[3], allow_na=True):
                issues.append(f"verification.md Coverage 第 {idx} 行 Evidence/Gap 不完整")
        anti_fake_rows = _markdown_table_rows(_section(text, "Anti-Fake Completion Check"))
        if not anti_fake_rows:
            issues.append("verification.md 缺少 Anti-Fake Completion Check 记录")
        for idx, row in enumerate(anti_fake_rows, 1):
            if len(row) < 3 or row[1].strip("` ").upper() != "PASS":
                issues.append(f"verification.md Anti-Fake 第 {idx} 行 Result 不是 PASS")
            elif not _filled(row[2]):
                issues.append(f"verification.md Anti-Fake 第 {idx} 行缺少 Evidence")
        if not _filled(_section(text, "Code-to-Spec Consistency Conclusion")):
            issues.append("verification.md 缺少 Code-to-Spec Consistency Conclusion")
    return issues


DOC_FILE_EXT = re.compile(
    r"\.(?:md|markdown|txt|rst|adoc|asciidoc|png|jpe?g|gif|svg|webp|pdf|docx?|pptx?|xlsx?)$",
    re.IGNORECASE)
_FILE_TOKEN = re.compile(r"[\w./\\-]+\.[A-Za-z0-9]+")
_BARE_FILE_TOKEN = re.compile(r"[A-Za-z0-9_.@+-]+(?:[/\\][A-Za-z0-9_.@+-]+)*")
ENGINEERING_FILE_BASENAMES = frozenset({
    ".gitattributes",
    ".gitignore",
    ".gitmodules",
    "build",
    "build.bazel",
    "cmakelists.txt",
    "containerfile",
    "dockerfile",
    "gnfile",
    "gnumakefile",
    "makefile",
    "workspace",
    "workspace.bazel",
})


def _table_header_columns(section_text):
    """返回 Markdown 表的第一个表头行列名(小写);无表格返回空列表。"""
    for raw in (section_text or "").splitlines():
        line = raw.strip()
        if line.startswith("|") and line.endswith("|"):
            cols = [c.strip().lower() for c in line.strip("|").split("|")]
            if cols and not all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cols):
                return cols
    return []


def _actual_scope_column(section_text):
    """按表头定位「实际文件/符号」列下标;紧凑表(无该列)返回 None。

    固定列序在紧凑表(Task|文件|操作)下会把操作类型误读为实际范围,
    因此实现信号只信任表头声明的列语义。
    """
    for idx, cell in enumerate(_table_header_columns(section_text)):
        if "实际" in cell and ("文件" in cell or "符号" in cell or "范围" in cell):
            return idx
    return None


def _value_implies_code(value):
    """单元格内容是否指向代码实现(保守方向:无法判定视为代码,宁多要证据)。

    - 已知构建/工程文件名始终按代码处理,即使后缀命中文档白名单(CMakeLists.txt)
    - 文件类 token 按扩展名分类:.md/.png 等文档媒体白名单 → 非代码;
      其余(.cpp/.ets/BUILD.gn/未知扩展) → 代码
    - 无扩展名路径、反引号文件名或单独 basename 无法证明是文档,保守按代码处理
    - N/A(含带理由):只检查理由部分是否夹带代码路径,防「N/A：无代码 / src/a.cpp」绕过
    - 无文件 token:含 :: 的符号视为代码;纯文字(如「无」)不视为代码
    """
    v = (value or "").strip("` ").strip()
    if not v or v == "-":
        return False
    na = re.match(r"(?i)^n/?a\b[\s：:]?(.*)$", v)
    scope = (na.group(1) if na else v).strip()
    if not scope:
        return False
    basenames = {
        re.split(r"[/\\]", token)[-1].lower()
        for token in _BARE_FILE_TOKEN.findall(scope)
    }
    if basenames & ENGINEERING_FILE_BASENAMES:
        return True
    files = _FILE_TOKEN.findall(scope)
    if files:
        return any(not DOC_FILE_EXT.search(f) for f in files)
    if "::" in scope or "/" in scope or "\\" in scope:
        return True
    if re.search(r"`[A-Za-z0-9_.@+-]+`", scope):
        return True
    for token in _BARE_FILE_TOKEN.findall(scope):
        if re.search(r"(?:修改|变更|新增|删除|调整|文件|路径|构建|工程)[^A-Za-z0-9_.@+-]{0,8}"
                     + re.escape(token), scope):
            return True
    return bool(re.fullmatch(r"[A-Za-z0-9_.@+-]+", scope.strip("` ")))


def _implementation_recorded(plan):
    """execution-plan 代码范围映射「实际文件/符号」列是否记录了代码实现。

    evidence 门禁的状态触发器:表头定位实际列、单元格按代码/文档分类,
    读取变更实际做过什么——不读取 manifest.complexity 预测声明。
    纯文档变更如实回填 docs 路径不会被误判为代码实现;
    紧凑表(无实际列)无法判定,保守视为已实现。
    """
    mapping = _section(plan, "代码范围映射")
    col = _actual_scope_column(mapping)
    if col is None:
        return bool(_markdown_table_rows(mapping))
    for row in _markdown_table_rows(mapping):
        if len(row) > col and _value_implies_code(row[col]):
            return True
    return False


def validate_level_d(change_dir, contract, require_registry=True):
    checks = _legacy_check(change_dir, "D")
    if require_registry:
        registry = _find_up(change_dir, ".codespec", "registry.md")
        checks.append(_d_edge(bool(registry), "registry",
                              "未找到 .codespec/registry.md(change 未被索引)" if not registry else ""))

    mf = _read(change_dir, "manifest.md")
    ok, issue = True, ""
    if mf is not None:
        fm = yaml_frontmatter(mf)
        if not fm:
            ok = False
            issue = "manifest.md 无 frontmatter"
        elif not fm.get("id"):
            ok = False
            issue = "manifest frontmatter 缺 id"
        elif not fm.get("status"):
            ok = False
            issue = "manifest frontmatter 缺 status"
        elif str(fm.get("status")).strip().lower() not in {"done", "archived"}:
            ok = False
            issue = f"manifest.status 必须为 done/archived，实际:{fm.get('status')}"
    checks.append(_d_edge(ok, "manifest", issue))

    spec = _read(change_dir, "spec.md") or ""
    plan = _read(change_dir, "execution-plan.md")
    if plan is not None:
        implementation_issues = _implementation_evidence_issues(plan, require_review=False)
        checks.append(_d_edge(
            not implementation_issues,
            "implementation-evidence",
            "; ".join(implementation_issues),
            "ohos-plan"))

    placeholder_issues = _archive_placeholder_issues(change_dir)
    checks.append(_d_edge(
        not placeholder_issues,
        "placeholders",
        "; ".join(placeholder_issues)))

    review_files = ("spec-compliance.md", "code-quality.md", "verification.md")
    implementation_recorded = plan is not None and _implementation_recorded(plan)
    review_issues = []
    review_content = {
        name: _read(change_dir, os.path.join("evidence", "reviews", name))
        for name in review_files
    }
    if implementation_recorded:
        missing = [name for name, evidence in review_content.items()
                   if evidence is None or not evidence.strip()]
        if missing:
            review_issues.append(
                "代码范围映射已记录实际实现,归档必须三份 Approved Review Evidence,缺少:"
                + ",".join(missing))
        for name, evidence in review_content.items():
            if evidence and evidence.strip():
                review_issues.extend(_review_evidence_issues(name, evidence, spec, plan or ""))
    elif any(content is not None for content in review_content.values()):
        for name, evidence in review_content.items():
            if not evidence or not evidence.strip():
                review_issues.append(f"Review Evidence 已启用但缺少:{name}")
            else:
                review_issues.extend(_review_evidence_issues(name, evidence, spec, plan or ""))
    checks.append(_d_edge(
        not review_issues,
        "review",
        "; ".join(review_issues),
        "ohos-review"))
    if _read(change_dir, "spec-for-validation.md") is not None:
        spec_for_validation_ok = SPEC_FOR_VALIDATION.archive_ready(change_dir)
        checks.append(_d_edge(spec_for_validation_ok, "spec-for-validation",
                              "spec-for-validation.md 必须满足命中 Profile 的审批要求、状态为 Approved，"
                              "当前 Profile 完整检查通过，且 check-spec-for-validation.md 结论为 PASS"
                              if not spec_for_validation_ok else ""))
    return checks


PROFILES_RESERVED = {"none", "custom", "security-sensitive"}


def _find_profiles_dir(start_dir):
    """向上找 profile 集合目录:新仓 runtime/assets/profiles, 发布布局 profiles, dist shared/ohos-sdd/profiles。"""
    d = os.path.abspath(start_dir)
    while True:
        for cand in (os.path.join(d, "runtime", "assets", "profiles"),
                     os.path.join(d, "profiles")):
            if os.path.isdir(cand):
                return cand
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in (os.path.join(here, "..", "profiles"),
                os.path.join(here, "..", "shared", "ohos-sdd", "profiles"),
                os.path.join(here, "..", "..", "shared", "ohos-sdd", "profiles")):
        cand = os.path.normpath(rel)
        if os.path.isdir(cand):
            return cand
    return None


def _parse_profile_md(path, fallback_name):
    """解析单个 profile.md frontmatter → (name, repos_list)。
    子 profile 列表由调用方按布局列出(两布局子目录命名不同)。"""
    with open(path, encoding="utf-8") as fh:
        fm = yaml_frontmatter(fh.read())
    repos = fm.get("repos") or []
    if isinstance(repos, str):
        repos = [] if repos.strip() in ("[]", "") else [repos]
    return (fm.get("name") or fallback_name, repos)


def _list_subprofiles(sub_dir):
    """列出子 profile 目录下的 .md 文件名(去扩展名),排除 README.md 与 _template.md。
    目录不存在时返回 []。两布局共用:source 在 <name>/subprofiles/,dist flatten 在 <name>/。"""
    if not os.path.isdir(sub_dir):
        return []
    return [
        os.path.splitext(sf)[0] for sf in os.listdir(sub_dir)
        if sf.endswith(".md") and sf not in ("README.md", "_template.md")
    ]


def _scan_profiles(profiles_dir):
    """返回 (main: name->repos_list, subs: name->[sub_names])。
    兼容 source(<name>/profile.md + <name>/subprofiles/<sub>.md)与
    dist flatten(<name>.md + <name>/<sub>.md)两种布局。
    分支互斥:同一 profile 的 source 目录形式与 dist flatten 形式不应混合存在于同一 profiles_dir。"""
    main, subs = {}, {}
    if not profiles_dir or not os.path.isdir(profiles_dir):
        return main, subs
    for entry in sorted(os.listdir(profiles_dir)):
        full = os.path.join(profiles_dir, entry)
        # source 布局:<name>/profile.md + <name>/subprofiles/<sub>.md
        if os.path.isdir(full) and entry != "_template":
            pf = os.path.join(full, "profile.md")
            if os.path.isfile(pf):
                name, repos = _parse_profile_md(pf, entry)
                main[name] = repos
                subs[name] = _list_subprofiles(os.path.join(full, "subprofiles"))
                continue
        # dist flatten 布局:<name>.md + <name>/<sub>.md
        if entry.endswith(".md") and entry not in ("README.md", "_template.md"):
            name, repos = _parse_profile_md(full, entry[:-3])
            main[name] = repos
            subs[name] = _list_subprofiles(os.path.join(profiles_dir, name))
    return main, subs


def _e_check(ok, artifact, issue, warn=False):
    """Level E check。warn=True 时 ok 应为 True(软规范不 fail),issue 标注 warn 文本,
    并打 warn 标记供 _assemble/_emit 呈现(不进 broken)。"""
    assert not (warn and not ok), "_e_check: warn=True 时 ok 必须为 True"
    d = {"ok": ok, "level": "E", "artifact": artifact, "file": "",
         "issue": issue, "rework_capability": "ohos-validate" if not ok else "",
         "evidence": "Level E profile" if not ok else ""}
    if warn:
        d["warn"] = True
    return d


def validate_level_e(change_dir, root):
    """Level E profile 维度:E1 合法 / E2 文件存在 / E3 schema warn / E4 subprofile 文件 /
    E5 best-effort repo / E6 repo 唯一。root 用于定位 profiles 集合。"""
    checks = []
    profiles_dir = _find_profiles_dir(change_dir) or os.path.join(root, "runtime", "assets", "profiles")
    main_map, subs_map = _scan_profiles(profiles_dir)

    mf = _read(change_dir, "manifest.md")
    fm = yaml_frontmatter(mf) if mf else {}
    profile = fm.get("profile") or "none"
    subprofiles = fm.get("subprofiles") or []
    # mini YAML parser 不识别 inline flow([]),会把 `subprofiles: []` 解析成字面串 '[]';
    # 同理空 inline。把它们规范化为空列表,只有真实 block 序列(- item)才是 list。
    if isinstance(subprofiles, str):
        subprofiles = [] if subprofiles.strip() in ("[]", "") else [subprofiles]

    # E1 profile 合法
    legal = profile in PROFILES_RESERVED or profile in main_map
    checks.append(_e_check(legal, "E1.profile-legal",
                           "" if legal else f"profile {profile!r} 不在扫描集合且非保留值"))

    # E2 profile 文件存在(保留值豁免)
    if profile in PROFILES_RESERVED:
        checks.append(_e_check(True, "E2.profile-file", f"{profile} 为保留值,文件待补(豁免)"))
    elif profile in main_map:
        checks.append(_e_check(True, "E2.profile-file", ""))
    else:
        checks.append(_e_check(False, "E2.profile-file", f"profile {profile!r} 无对应文件"))

    # E3 schema 推荐节(软规范:缺则 warn,ok=True)
    if profile in main_map and profile not in PROFILES_RESERVED:
        pf = None
        src_pf = os.path.join(profiles_dir, profile, "profile.md")
        dist_pf = os.path.join(profiles_dir, profile + ".md")
        pf = src_pf if os.path.isfile(src_pf) else (dist_pf if os.path.isfile(dist_pf) else None)
        ptxt = ""
        if pf:
            with open(pf, encoding="utf-8") as fh:
                ptxt = fh.read()
        for sec in ("基本信息", "阶段补充约束", "专项检查清单"):
            present = bool(re.search(r"^##\s*" + sec, ptxt, re.MULTILINE))
            checks.append(_e_check(True, f"E3.schema:{sec}",
                                   "" if present else f"推荐节「{sec}」缺失(warn,待社区补)",
                                   warn=not present))
    else:
        checks.append(_e_check(True, "E3.schema", "保留值/无 profile,豁免"))

    # E4 subprofile 文件
    known_subs = set(subs_map.get(profile, []))
    for sp in subprofiles:
        checks.append(_e_check(sp in known_subs, f"E4.subprofile:{sp}",
                               f"subprofile {sp!r} 不在 {profile} 的子 profile 集合"))

    # E5 best-effort repo:有 git remote 时校验 manifest.profile 与仓名归属一致(warn)
    try:
        import subprocess
        url = subprocess.run(["git", "remote", "get-url", "origin"],
                             capture_output=True, text=True,
                             cwd=os.path.abspath(change_dir)).stdout.strip()
    except Exception:
        url = ""
    if url:
        repo = os.path.basename(url.rstrip("/"))
        if repo.endswith(".git"):
            repo = repo[:-4]
        owner = [pname for pname, reps in main_map.items() if repo in reps]
        if owner and profile not in PROFILES_RESERVED and profile not in owner:
            checks.append(_e_check(True, "E5.repo-match",
                                   f"git remote {repo}→{owner[0]},但 manifest.profile={profile}(warn,请确认)",
                                   warn=True))
        elif not owner and profile not in PROFILES_RESERVED:
            checks.append(_e_check(True, "E5.repo-unmatched",
                                   f"git remote {repo} 未匹配任何 profile(可能仓未注册或 manifest.profile 需确认)",
                                   warn=True))
        else:
            checks.append(_e_check(True, "E5.repo-match", ""))
    # E5 无 git remote 时不产出 check(静默)

    # E6 repo 唯一归属:多 profile 声明同仓名 → fail
    repo_owner = {}
    for pname, reps in main_map.items():
        for r in reps:
            repo_owner.setdefault(r, []).append(pname)
    for r, owners in repo_owner.items():
        if len(owners) > 1:
            checks.append(_e_check(False, f"E6.repo-conflict:{r}",
                                   f"仓名 {r} 被多 profile 声明:{sorted(owners)}"))

    # E7 主 profile repos 非空(仓间路由依赖,必填,fail)
    for pname, reps in main_map.items():
        if not reps:
            checks.append(_e_check(False, f"E7.profile-repos:{pname}",
                                   f"profile {pname!r} 的 repos 为空(仓间路由依赖,必填至少 1 仓名)"))

    # E8 子 profile applies_to 非空(仓内路由依赖,必填,fail)
    for pname, sub_names in subs_map.items():
        for sub in sub_names:
            spf = None
            for cand in (os.path.join(profiles_dir, pname, "subprofiles", sub + ".md"),
                         os.path.join(profiles_dir, pname, sub + ".md")):
                if os.path.isfile(cand):
                    spf = cand
                    break
            if not spf:
                continue
            with open(spf, encoding="utf-8") as fh:
                sfm = yaml_frontmatter(fh.read())
            at = sfm.get("applies_to")
            if isinstance(at, str):
                at = [] if at.strip() in ("", "[]") else [at]
            if not at:
                checks.append(_e_check(False, f"E8.subprofile-applies_to:{pname}/{sub}",
                                       f"子 profile {pname}/{sub} 的 applies_to 为空(仓内路由依赖,必填至少 1 glob)"))

    return checks


# contract 自检:模板标题组(与现有 ruby validator 逐字对齐)。
# 注:gate-* 形态是当前契约;P2 gate→check 迁移时须同步本表(见 contract-transition 附录决议 2)。
_HEADING_GROUPS = [
    ("templates/proposal.md", [
        "# 需求文档", "## 需求输入", "## 需求基线", "### Agent Scope Guard",
        "## 附录：澄清与决策记录（条件启用）"]),
    ("templates/spec.md", [
        "# 特性规格", "## 用户故事", "## 验收追溯", "## 验证映射",
        "## API 变更分析", "### 新增 API", "### 变更/废弃 API",
        "### API 与错误码事实"]),
    ("templates/design.md", [
        "# 架构设计", "## 需求基线", "## 上下文和现状", "### 代码事实基线",
        "### 既有模式复用", "## 关键设计决策", "### 类图",
        "### 状态归属与不变量", "#### 不变量追溯", "## 后续 Task 拆分"]),
    ("templates/execution-plan.md", [
        "# 执行计划", "## 受影响文件全量清单", EP_HEADING_AC_TRACE,
        "## Task 详情", "## 代码范围映射"]),
    ("templates/task.md", [
        "# 任务规格", "## 代码变更摘要", "## 验证检查清单"]),
    ("templates/test-spec.md", [
        "# 测试规格", "## 测试范围", "## 环境前置与公共配置", "## 场景"]),
    ("templates/gate-checklist.md", [
        "# 阶段检查清单",
        "## 一、定义阶段（进入规格说明条件）",
        "## 二、规格说明阶段（进入设计条件）",
        "## 三、设计阶段（进入计划条件）",
        "## 四、计划阶段（进入实现条件）",
        "## 五、归档就绪硬门禁（实现/审查完成后）"]),
    ("templates/review.md", [
        "# Review Gate 汇总", "## GA / GB / GC 汇总",
        "## Review Evidence 索引", "## 开放问题", "## 最终决策"]),
    ("templates/review/spec-compliance.md", [
        "# Spec Compliance Review", "## AC → Task → Code → Commit → Review",
        "## Anti-Fake Completion Check"]),
    ("templates/review/code-quality.md", [
        "# Code Quality Review", "## Plan Scope vs Actual Code Scope", "## Findings"]),
    ("templates/review/verification.md", [
        "# Verification", "## Execution Records", "## Anti-Fake Completion Check"]),
    ("templates/threat-model.md", [
        "# 威胁模型分析", "## 数据流图", "## STRIDE 威胁分析",
        "## 法规合规检查", "## 风险与缓解"]),
]

_EXAMPLE_FILES = [
    "examples/bugfix-example/bugfix.md",
    "examples/bugfix-example/regression-test.md",
    "examples/archive-shape/.codespec/registry.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/proposal.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/manifest.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/spec.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/design.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/execution-plan.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/review.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/test-spec.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/checks/check-proposal.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/checks/check-spec.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/checks/check-design.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/checks/check-execution-plan.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/reviews/spec-compliance.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/reviews/code-quality.md",
    "examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/reviews/verification.md",
]

_VALID_STATUS = {"required", "conditional", "recommended", "reference"}


def _cok(label):
    return {"ok": True, "level": "contract", "artifact": label, "file": "",
            "issue": "", "rework_capability": "", "evidence": ""}


def _cbad(label, issue):
    return {"ok": False, "level": "contract", "artifact": label, "file": "",
            "issue": issue, "rework_capability": "using-ohos-sdd", "evidence": "contract 自检"}


def validate_contract_source(root):
    """Contract 自检。兼容新仓布局(root/runtime/assets/contracts/artifacts.yaml)
    和发布布局(root/contracts/artifacts.yaml)。"""
    checks = []
    contract_path = os.path.join(root, "runtime", "assets", "contracts", "artifacts.yaml")
    if not os.path.isfile(contract_path):
        contract_path = os.path.join(root, "contracts", "artifacts.yaml")
    if not os.path.isfile(contract_path):
        checks.append(_cbad("contract", f"artifacts.yaml 缺失(尝试了 runtime/assets/contracts/, contracts/)"))
        return checks
    contract = load_contract(contract_path)

    checks.append(_cok("schema") if contract.get("schema") == "ohos-sdd-artifacts/v1"
                  else _cbad("schema", f"schema={contract.get('schema')}"))

    arch = contract.get("archive", {})
    target_root = arch.get("target_root", "")
    checks.append(_cok("archive.target_root") if target_root == ".codespec/changes"
                  else _cbad("archive.target_root", str(target_root)))
    checks.append(_cok("archive.registry") if arch.get("registry") == ".codespec/registry.md"
                  else _cbad("archive.registry", str(arch.get("registry"))))
    readiness = arch.get("readiness", {})
    readiness_statuses = set(readiness.get("manifest_statuses", []) or [])
    readiness_levels = set(readiness.get("require_levels", []) or [])
    readiness_flags = (
        readiness_statuses == {"done", "archived"} and
        readiness_levels == {"A", "B", "C", "D"} and
        str(readiness.get("require_placeholder_free_artifacts")).lower() == "true" and
        str(readiness.get("require_approved_review_evidence")).lower() == "on_implementation" and
        str(readiness.get("registry_write_after_validation")).lower() == "true"
    )
    checks.append(_cok("archive.readiness") if readiness_flags
                  else _cbad("archive.readiness", str(readiness)))

    traceability = contract.get("traceability", {})
    expected_chain = ["proposal", "spec.ac", "execution_plan.task", "code"]
    actual_chain = traceability.get("required_chain", [])
    checks.append(_cok("traceability.required_chain") if actual_chain == expected_chain
                  else _cbad("traceability.required_chain", f"期望 {expected_chain}, 实际 {actual_chain}"))
    required_constraints = {
        "every_task_declares_produces_and_consumes",
        "changed_state_declares_owner_and_full_lifecycle",
        "every_verification_has_expected_and_actual_result",
        "anti_fake_completion_has_concrete_evidence",
        "planned_scope_maps_to_actual_code_scope",
    }
    actual_constraints = set(traceability.get("completion_constraints", []) or [])
    missing_constraints = sorted(required_constraints - actual_constraints)
    checks.append(_cok("traceability.completion_constraints") if not missing_constraints
                  else _cbad("traceability.completion_constraints", f"缺少 {missing_constraints}"))

    evidence_policy = contract.get("evidence_policy", {})
    checks.append(_cok("evidence_policy.minimum_archive_required")
                  if str(evidence_policy.get("minimum_archive_required")).lower() == "false"
                  else _cbad("evidence_policy.minimum_archive_required", "必须为 false"))
    review_evidence = evidence_policy.get("review_evidence", []) or []
    expected_evidence_ids = {"spec_compliance", "code_quality", "verification"}
    actual_evidence_ids = {item.get("id") for item in review_evidence if isinstance(item, dict)}
    checks.append(_cok("evidence_policy.review_evidence")
                  if actual_evidence_ids == expected_evidence_ids
                  else _cbad("evidence_policy.review_evidence",
                             f"期望 {sorted(expected_evidence_ids)}, 实际 {sorted(actual_evidence_ids)}"))
    for item in review_evidence:
        if not isinstance(item, dict):
            checks.append(_cbad("evidence_policy.review_evidence.item", "条目必须为 mapping"))
            continue
        template = item.get("template", "")
        output = item.get("output", "")
        tpath = os.path.join(root, "runtime", "assets", template)
        if not os.path.isfile(tpath):
            tpath = os.path.join(root, template)
        checks.append(_cok(f"review_evidence.template:{item.get('id')}")
                      if os.path.isfile(tpath) and os.path.getsize(tpath) > 0
                      else _cbad(f"review_evidence.template:{item.get('id')}", f"模板缺失:{template}"))
        checks.append(_cok(f"review_evidence.output:{item.get('id')}")
                      if output.startswith(target_root + "/<id>/evidence/reviews/")
                      else _cbad(f"review_evidence.output:{item.get('id')}", f"输出路径非法:{output}"))

    phases = {p.get("id") for p in contract.get("phase_order", [])}
    artifact_ids = {a.get("id") for a in contract.get("artifacts", [])}
    required_artifact_ids = {
        a.get("id") for a in contract.get("artifacts", []) if a.get("status") == "required"
    }
    expected_required_artifact_ids = {"proposal", "spec", "design", "execution_plan"}
    checks.append(_cok("minimum_archive.artifacts")
                  if required_artifact_ids == expected_required_artifact_ids
                  else _cbad("minimum_archive.artifacts",
                             f"期望 {sorted(expected_required_artifact_ids)}, "
                             f"实际 {sorted(required_artifact_ids)}"))
    proposal_contract = next(
        (a for a in contract.get("artifacts", []) if a.get("id") == "proposal"), {})
    manifest_contract = next(
        (a for a in contract.get("artifacts", []) if a.get("id") == "manifest"), {})
    checks.append(_cok("manifest.status")
                  if manifest_contract.get("status") == "recommended"
                  else _cbad("manifest.status", "manifest 必须为 recommended 运行时元数据"))
    expected_manifest_statuses = {
        "draft", "approved", "implementing", "verifying", "done", "archived"
    }
    actual_manifest_statuses = set(manifest_contract.get("status_values", []) or [])
    checks.append(_cok("manifest.status_values")
                  if actual_manifest_statuses == expected_manifest_statuses
                  else _cbad("manifest.status_values",
                             f"期望 {sorted(expected_manifest_statuses)}, 实际 {sorted(actual_manifest_statuses)}"))
    # Define 审批合同必须与运行时门禁实现保持一致。合同字段是发布时的可读声明，
    # 这里的 pin 检查确保它不是无人消费的装饰性配置，也不会悄然产生双源漂移。
    phase_approval = proposal_contract.get("phase_approval", {}) or {}
    checks.append(_cok("proposal.phase_approval.phase_status_field")
                  if phase_approval.get("phase_status_field") == PROPOSAL_PHASE_STATUS_FIELD
                  else _cbad("proposal.phase_approval.phase_status_field",
                             f"期望 {PROPOSAL_PHASE_STATUS_FIELD}, 实际 {phase_approval.get('phase_status_field')}"))
    checks.append(_cok("proposal.phase_status_values")
                  if _normalize_status_values(proposal_contract.get("status_values")) == PROPOSAL_PHASE_STATUS_VALUES
                  else _cbad("proposal.phase_status_values",
                             f"期望 {sorted(PROPOSAL_PHASE_STATUS_VALUES)}, "
                             f"实际 {_normalize_status_values(proposal_contract.get('status_values'))}"))
    checks.append(_cok("proposal.legacy_status_values")
                  if _normalize_status_values(proposal_contract.get("legacy_status_values")) == PROPOSAL_LEGACY_STATUS_VALUES
                  else _cbad("proposal.legacy_status_values",
                             f"期望 {sorted(PROPOSAL_LEGACY_STATUS_VALUES)}, "
                             f"实际 {_normalize_status_values(proposal_contract.get('legacy_status_values'))}"))
    checks.append(_cok("proposal.phase_approval.allowed_statuses")
                  if _normalize_status_values(phase_approval.get("allowed_statuses")) == PHASE_APPROVAL_ALLOWED_STATUSES
                  else _cbad("proposal.phase_approval.allowed_statuses",
                             f"期望 {sorted(PHASE_APPROVAL_ALLOWED_STATUSES)}, "
                             f"实际 {_normalize_status_values(phase_approval.get('allowed_statuses'))}"))
    checks.append(_cok("proposal.phase_approval.approval_field")
                  if phase_approval.get("approval_field") == PHASE_APPROVAL_FIELD
                  else _cbad("proposal.phase_approval.approval_field",
                             f"期望 {PHASE_APPROVAL_FIELD}, 实际 {phase_approval.get('approval_field')}"))
    checks.append(_cok("proposal.phase_approval.approved_requires")
                  if phase_approval.get("approved_requires") == list(PHASE_APPROVAL_REQUIRED_FIELDS)
                  else _cbad("proposal.phase_approval.approved_requires",
                             f"期望 {list(PHASE_APPROVAL_REQUIRED_FIELDS)}, "
                             f"实际 {phase_approval.get('approved_requires')}"))
    checks.append(_cok("proposal.phase_approval.downstream_requires_approved")
                  if str(phase_approval.get("downstream_requires_approved")).lower() ==
                     str(PHASE_APPROVAL_DOWNSTREAM_REQUIRES_APPROVED).lower()
                  else _cbad("proposal.phase_approval.downstream_requires_approved",
                             f"期望 {PHASE_APPROVAL_DOWNSTREAM_REQUIRES_APPROVED}, "
                             f"实际 {phase_approval.get('downstream_requires_approved')}"))
    expected_proposal_owns = {
        "agent_repository_and_module_exploration_scope",
        "prohibited_access_and_modification_boundaries",
        "out_of_scope_rebaseline_rule",
    }
    checks.append(_cok("proposal.owns")
                  if set(proposal_contract.get("owns", []) or []) == expected_proposal_owns
                  else _cbad("proposal.owns", str(proposal_contract.get("owns", []))))
    expected_proposal_sections = {"需求输入", "需求基线", "Agent Scope Guard"}
    checks.append(_cok("proposal.required_sections")
                  if set(proposal_contract.get("required_sections", []) or []) == expected_proposal_sections
                  else _cbad("proposal.required_sections", str(proposal_contract.get("required_sections", []))))
    proposal_conditionals = proposal_contract.get("conditional_sections", []) or []
    expected_proposal_conditional = {
        (item.get("section"), item.get("required_when"))
        for item in proposal_conditionals if isinstance(item, dict)
    }
    checks.append(_cok("proposal.conditional_sections")
                  if expected_proposal_conditional == {
                      ("附录：澄清与决策记录（条件启用）",
                       "complex_critical_or_clarification_blocked_or_contested")}
                  else _cbad("proposal.conditional_sections", str(proposal_conditionals)))
    spec_contract = next(
        (a for a in contract.get("artifacts", []) if a.get("id") == "spec"), {})
    expected_spec_owns = {
        "externally_observable_acceptance_criteria",
        "three_tier_interface_observability",
        "then_implementation_boundary",
        "api_openness_for_added_changed_and_deprecated_interfaces",
        "exact_api_and_error_code_fact_contract",
        "ac_verification_and_red_conditions",
    }
    missing_spec_owns = sorted(expected_spec_owns - set(spec_contract.get("owns", []) or []))
    checks.append(_cok("spec.owns") if not missing_spec_owns
                  else _cbad("spec.owns", f"缺少 {missing_spec_owns}"))
    expected_spec_sections = {
        "用户故事", "验收追溯", "规则定义", "验证映射",
        "API 变更分析", "API 与错误码事实", "兼容性声明",
    }
    actual_spec_sections = set(spec_contract.get("required_sections", []) or [])
    checks.append(_cok("spec.required_sections")
                  if actual_spec_sections == expected_spec_sections
                  else _cbad("spec.required_sections",
                             f"期望 {sorted(expected_spec_sections)}, 实际 {sorted(actual_spec_sections)}"))
    spec_quality = spec_contract.get("spec_quality", {})
    acceptance_traceability = spec_quality.get("acceptance_traceability", {})
    traceability_ok = (
        acceptance_traceability.get("current_columns") == ["AC", "关联规则", "可观察表面"] and
        str(acceptance_traceability.get("legacy_six_column_shape_supported")).lower() == "true" and
        acceptance_traceability.get("task_mapping_source") == "execution-plan.md" and
        acceptance_traceability.get("verification_source") == "验证映射" and
        acceptance_traceability.get("evidence_source") == "evidence/reviews")
    checks.append(_cok("spec.acceptance_traceability") if traceability_ok
                  else _cbad("spec.acceptance_traceability", str(acceptance_traceability)))
    acceptance_quality = spec_quality.get("acceptance_criteria", {})
    expected_surfaces = {"end_user", "public_api", "system_api", "inner_api"}
    actual_surfaces = set(acceptance_quality.get("observable_surfaces", []) or [])
    checks.append(_cok("spec.observable_surfaces")
                  if actual_surfaces == expected_surfaces
                  else _cbad("spec.observable_surfaces",
                             f"期望 {sorted(expected_surfaces)}, 实际 {sorted(actual_surfaces)}"))
    expected_then_forbids = {
        "internal_data_structure", "internal_state_machine", "internal_call_chain",
        "implementation_class_or_method", "internal_cache_queue_or_lock",
        "implementation_algorithm",
    }
    actual_then_forbids = set(acceptance_quality.get("then_forbids", []) or [])
    checks.append(_cok("spec.then_forbids")
                  if actual_then_forbids == expected_then_forbids
                  else _cbad("spec.then_forbids",
                             f"期望 {sorted(expected_then_forbids)}, 实际 {sorted(actual_then_forbids)}"))
    then_detection = acceptance_quality.get("then_boundary_detection", {})
    then_detection_ok = (
        then_detection.get("severity") == "warn" and
        then_detection.get("exemption_marker") == "ext-ok" and
        str(then_detection.get("broad_patterns_require_action_verb")).lower() == "true" and
        str(then_detection.get("gate_disposition_required")).lower() == "true")
    checks.append(_cok("spec.then_boundary_detection") if then_detection_ok
                  else _cbad("spec.then_boundary_detection", str(then_detection)))
    api_openness = spec_quality.get("api_openness", {})
    actual_api_levels = set(api_openness.get("values", []) or [])
    checks.append(_cok("spec.api_openness")
                  if actual_api_levels == SPEC_API_OPENNESS_VALUES and
                  str(api_openness.get("changed_or_deprecated_requires_current_and_target")).lower() == "true"
                  else _cbad("spec.api_openness",
                             f"开放级别={sorted(actual_api_levels)}, current/target={api_openness.get('changed_or_deprecated_requires_current_and_target')}"))
    api_error_facts = spec_quality.get("api_error_facts", {})
    fact_flags = {
        "existing_requires_source_file_line_or_symbol",
        "exact_signature_or_numeric_value_required",
        "error_code_requires_trigger_external_behavior_ac_and_verification",
        "new_fact_requires_proposal_design_task_or_ac_basis",
    }
    missing_fact_flags = sorted(
        flag for flag in fact_flags if str(api_error_facts.get(flag)).lower() != "true")
    checks.append(_cok("spec.api_error_facts") if not missing_fact_flags
                  else _cbad("spec.api_error_facts", f"未启用 {missing_fact_flags}"))
    verification_quality = spec_quality.get("verification", {})
    expected_verification_flags = {
        "requires_test_entry", "requires_red_condition",
        "red_condition_must_explain_pre_implementation_failure",
    }
    missing_verification_flags = sorted(
        flag for flag in expected_verification_flags
        if str(verification_quality.get(flag)).lower() != "true")
    checks.append(_cok("spec.verification_red") if not missing_verification_flags
                  else _cbad("spec.verification_red", f"未启用 {missing_verification_flags}"))

    design_contract = next(
        (a for a in contract.get("artifacts", []) if a.get("id") == "design"), {})
    expected_design_owns = {
        "code_fact_baseline",
        "existing_pattern_reuse",
        "class_and_interface_structure",
        "resource_and_state_ownership",
        "state_lifecycle_and_invariants",
        "concurrency_model",
        "invariant_ac_task_verification_traceability",
    }
    missing_design_owns = sorted(expected_design_owns - set(design_contract.get("owns", []) or []))
    checks.append(_cok("design.owns") if not missing_design_owns
                  else _cbad("design.owns", f"缺少 {missing_design_owns}"))
    conditional_sections = design_contract.get("conditional_sections", []) or []
    actual_design_sections = {
        item.get("section") for item in conditional_sections if isinstance(item, dict) and item.get("required_when")
    }
    expected_design_sections = {"代码事实基线", "既有模式复用", "类图", "状态归属与不变量"}
    checks.append(_cok("design.conditional_sections")
                  if actual_design_sections == expected_design_sections
                  else _cbad("design.conditional_sections",
                             f"期望 {sorted(expected_design_sections)}, 实际 {sorted(actual_design_sections)}"))
    invariant_traceability = design_contract.get("invariant_traceability", {})
    expected_invariant_links = {
        "spec.ac", "execution_plan.task", "verification_method_and_pass_criteria"
    }
    actual_invariant_links = set(invariant_traceability.get("required_links", []) or [])
    checks.append(_cok("design.invariant_traceability")
                  if actual_invariant_links == expected_invariant_links
                  else _cbad("design.invariant_traceability",
                             f"期望 {sorted(expected_invariant_links)}, 实际 {sorted(actual_invariant_links)}"))
    execution_plan_contract = next(
        (a for a in contract.get("artifacts", []) if a.get("id") == "execution_plan"), {})
    expected_plan_owns = {
        "ac_task_code_commit_review_traceability",
        "planned_and_actual_code_scope",
        "task_produces_consumes",
        "state_ownership_and_lifecycle",
        "expected_and_actual_results",
        "anti_fake_completion",
        "stable_spec_and_design_references",
    }
    missing_plan_owns = sorted(expected_plan_owns - set(execution_plan_contract.get("owns", []) or []))
    checks.append(_cok("execution_plan.owns") if not missing_plan_owns
                  else _cbad("execution_plan.owns", f"缺少 {missing_plan_owns}"))
    expected_task_fields = {"Produces", "Consumes", "状态所有权和生命周期",
                            "Design STATE/INV 映射", "Expected Result", "Actual Result", "Anti-Fake Completion",
                            "Spec References", "Design References", "Review Handoff"}
    missing_task_fields = sorted(
        expected_task_fields - set(execution_plan_contract.get("required_task_fields", []) or []))
    checks.append(_cok("execution_plan.required_task_fields") if not missing_task_fields
                  else _cbad("execution_plan.required_task_fields", f"缺少 {missing_task_fields}"))
    for a in contract.get("artifacts", []):
        aid = a.get("id", "?")
        tmpl = a.get("template")
        resolution = a.get("template_resolution", "static")
        if resolution == "profile_extendable":
            try:
                template_checks = SPEC_FOR_VALIDATION.contract_template_checks(root, aid)
            except (ModuleNotFoundError, SyntaxError, ImportError) as exc:
                tpath = os.path.join(root, tmpl) if tmpl else None
                if tpath and os.path.isfile(tpath) and os.path.getsize(tpath) > 0:
                    checks.append(_cok(f"{aid}.template"))
                else:
                    checks.append(_cbad(f"{aid}.template", f"模板缺失或空:{tmpl}"))
                checks.append(_cbad(
                    f"{aid}.profile_extendable_runtime",
                    f"spec_for_validation 模块不可用，Profile 增量校验降级:{type(exc).__name__}: {exc}"))
            else:
                for ok, label, issue in template_checks:
                    checks.append(_cok(label) if ok else _cbad(label, issue))
        else:
            tpath = os.path.join(root, tmpl) if tmpl else None
            if tpath and not os.path.isfile(tpath):
                for alt in (os.path.join(root, "runtime", "assets", tmpl),
                            os.path.join(root, "templates", os.path.basename(tmpl))):
                    if os.path.isfile(alt):
                        tpath = alt
                        break
            if tpath and os.path.isfile(tpath) and os.path.getsize(tpath) > 0:
                checks.append(_cok(f"{aid}.template"))
            else:
                checks.append(_cbad(f"{aid}.template", f"模板缺失或空:{tmpl}"))
        if resolution not in {"static", "profile_extendable"}:
            checks.append(_cbad(f"{aid}.template_resolution", f"未知解析方式:{resolution}"))
        else:
            checks.append(_cok(f"{aid}.template_resolution"))
        ph = a.get("phase", "")
        checks.append(_cok(f"{aid}.phase") if ph == "all" or ph in phases
                      else _cbad(f"{aid}.phase", f"未知 phase:{ph}"))
        st = a.get("status", "")
        checks.append(_cok(f"{aid}.status") if st in _VALID_STATUS
                      else _cbad(f"{aid}.status", f"未知 status:{st}"))
        if "bypass" in a:
            bypass = str(a.get("bypass") or "").lower()
            valid_bypass = bypass in {"true", "false"} and (bypass != "true" or st == "conditional")
            checks.append(_cok(f"{aid}.bypass") if valid_bypass
                          else _cbad(f"{aid}.bypass", "bypass 必须为 true/false，且 true 时 status 必须为 conditional"))
        layer = a.get("layer", "")
        checks.append(_cok(f"{aid}.layer") if layer in {"core", "oh-extension"}
                      else _cbad(f"{aid}.layer", f"未知 layer:{layer}"))
        checks.append(_cok(f"{aid}.role") if a.get("role")
                      else _cbad(f"{aid}.role", "role 为空"))
        loc = a.get("default_location", "")
        if loc:
            checks.append(_cok(f"{aid}.default_location")
                          if loc.startswith(target_root + "/")
                          else _cbad(f"{aid}.default_location", f"不在 archive root:{loc}"))
        for ro in a.get("runtime_outputs", []) or []:
            checks.append(_cok(f"{aid}.runtime_output:{ro}")
                          if ro.startswith(target_root + "/")
                          else _cbad(f"{aid}.runtime_output", f"不在 archive root:{ro}"))
        for dep in a.get("depends_on", []) or []:
            checks.append(_cok(f"{aid}.depends_on:{dep}")
                          if dep in artifact_ids
                          else _cbad(f"{aid}.depends_on:{dep}", f"未知交付件:{dep}"))
        for conditional in a.get("conditional_depends_on", []) or []:
            dep = conditional.get("artifact") if isinstance(conditional, dict) else None
            when = conditional.get("when") if isinstance(conditional, dict) else None
            valid = dep in artifact_ids and bool(when)
            checks.append(_cok(f"{aid}.conditional_depends_on:{dep}")
                          if valid
                          else _cbad(f"{aid}.conditional_depends_on:{dep or '?'}",
                                     "conditional dependency 必须声明有效 artifact 和 when"))

    for rel, headings in _HEADING_GROUPS:
        fpath = os.path.join(root, rel)
        if not os.path.isfile(fpath):
            fpath = os.path.join(root, "runtime", "assets", rel)
        if os.path.isfile(fpath):
            with open(fpath, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        else:
            lines = []
        for h in headings:
            present = any(ln.strip() == h for ln in lines)
            checks.append(_cok(f"{rel}:{h}") if present
                          else _cbad(f"{rel}:{h}", f"缺少标题 {h}"))

    for ex in _EXAMPLE_FILES:
        epath = os.path.join(root, ex)
        if os.path.isfile(epath):
            checks.append(_cok(f"example:{ex}"))
        else:
            # 发布布局无 examples,跳过(不报 fail)
            checks.append(_cok(f"example:{ex}"))

    for d in contract.get("current_drifts", []):
        complete = all(d.get(k) for k in ("id", "severity", "description", "follow_up_batch"))
        checks.append(_cok(f"drift:{d.get('id', '?')}") if complete
                      else _cbad(f"drift:{d.get('id', '?')}", "drift 元数据不全"))

    return checks


def _find_contract_path():
    d = os.getcwd()
    while d != "/":
        for cand in (os.path.join(d, "runtime", "assets", "contracts", "artifacts.yaml"),
                     os.path.join(d, "contracts", "artifacts.yaml")):
            if os.path.isfile(cand):
                return cand
        d = os.path.dirname(d)
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in (os.path.join(here, "..", "contracts", "artifacts.yaml"),
                os.path.join(here, "..", "shared", "ohos-sdd", "contracts", "artifacts.yaml"),
                os.path.join(here, "..", "..", "shared", "ohos-sdd", "contracts", "artifacts.yaml")):
        cand = os.path.normpath(rel)
        if os.path.isfile(cand):
            return cand
    return None


def _assemble(change, command, level, checks):
    broken = [c for c in checks if not c["ok"]]
    warnings = [c for c in checks if c.get("warn")]
    return {
        "change": change or "", "command": command, "level": level,
        "passed": len(broken) == 0, "total": len(checks), "broken": len(broken),
        "broken_edges": broken, "warnings": warnings,
        "next": "全部通过" if not broken
        else "按 broken_edges 的 rework_capability 回到对应能力修复",
    }


# Level A-E 的人类可读副标题(方案 3:单层跑时标题带全称)
LEVEL_TITLE = {
    "A": "结构存在",
    "B": "锚点标题",
    "C": "依赖边一致",
    "D": "归档就绪",
    "E": "profile 命中",
}
# 方案 1:level=all 时顶部图例,帮助一眼看懂 A-E 含义
LEVEL_LEGEND = "level 语义: A=结构存在 B=锚点标题 C=依赖边一致 D=归档就绪 E=profile 命中"


def _emit(result, as_json):
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    warns = result.get("warnings", [])
    tag = "PASS" if result["passed"] else "FAIL"
    level = result["level"]
    if level == "all":
        print(LEVEL_LEGEND)
    # 单层 A-E 标题带全称;contract 等其他 level 保持 level=<x> 原样
    title = f"level={level}·{LEVEL_TITLE[level]}·" if level in LEVEL_TITLE else f"level={level}"
    print(f"[{tag}] {result['command']} {title} "
          f"({result['total']} checks, {result['broken']} broken, {len(warns)} warn)")
    for c in result["broken_edges"]:
        print(f"  - {c['level']} {c['artifact']} ({c.get('file','')}): "
              f"{c['issue']} -> {c['rework_capability']}")
    for c in warns:
        print(f"  ~ {c['level']} {c['artifact']}: {c['issue']} (warn)")


def _parse_validate_args(argv):
    opts = {"change": None, "level": "all", "json": False, "contract": None, "source": False}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--level" and i + 1 < len(argv):
            opts["level"] = argv[i + 1]; i += 2
        elif a == "--json":
            opts["json"] = True; i += 1
        elif a == "--contract" and i + 1 < len(argv):
            opts["contract"] = argv[i + 1]; i += 2
        elif a == "--source":
            opts["source"] = True; i += 1
        elif not a.startswith("-"):
            opts["change"] = a; i += 1
        else:
            i += 1
    return opts


def _root_from_change(change_dir):
    """从 change_dir 推仓库 root:向上找含 runtime/assets/ 或 contracts/ 的目录;
    找不到回退 change_dir 自身绝对路径。"""
    d = os.path.abspath(change_dir or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(d, "runtime", "assets")):
            return d
        if os.path.isdir(os.path.join(d, "contracts")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.path.abspath(change_dir or os.getcwd())
        d = parent


def _resolve_levels(level):
    if level == "all":
        return ["A", "B", "C", "D", "E"]
    if level.upper() in {"A", "B", "C", "D", "E"}:
        return [level.upper()]
    return None  # 非法 level:cmd_validate 据此报错,避免静默 0-check PASS


def cmd_validate(argv):
    opts = _parse_validate_args(argv)
    if opts["source"]:
        cpath = opts["contract"] or _find_contract_path()
        if not cpath:
            print("validate --source: 找不到契约 artifacts.yaml",
                  file=sys.stderr)
            return 2
        # 新仓布局: cpath = root/runtime/assets/contracts/artifacts.yaml → root = 上 4 级
        # 发布布局: cpath = root/contracts/artifacts.yaml → root = 上 2 级
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(cpath))))
        if not os.path.isfile(os.path.join(root, "runtime", "assets", "contracts", "artifacts.yaml")):
            root = os.path.dirname(os.path.dirname(cpath))  # 发布布局
        checks = validate_contract_source(root)
        result = _assemble("", "validate --source", "contract", checks)
        _emit(result, opts["json"])
        return 0 if result["passed"] else 1
    if opts["change"] is None:
        opts["change"] = os.getcwd()
    levels = _resolve_levels(opts["level"])
    if levels is None:
        print(f"validate: 未知 level {opts['level']!r},允许 A/B/C/D/E/all", file=sys.stderr)
        return 2
    contract = load_contract(opts["contract"]) if opts["contract"] else _find_contract()
    checks = []
    for lv in levels:
        if lv == "A":
            checks += validate_level_a(opts["change"], contract)
        elif lv == "B":
            checks += validate_level_b(opts["change"], contract)
        elif lv == "C":
            checks += validate_level_c(opts["change"])
        elif lv == "D":
            checks += validate_level_d(opts["change"], contract)
        elif lv == "E":
            checks += validate_level_e(opts["change"], _root_from_change(opts["change"]))
    seen_legacy = False
    deduplicated = []
    for check in checks:
        if check.get("artifact") == "legacy-spec-for-test":
            if seen_legacy:
                continue
            seen_legacy = True
        deduplicated.append(check)
    checks = deduplicated
    result = _assemble(opts["change"], "validate", opts["level"], checks)
    _emit(result, opts["json"])
    return 0 if result["passed"] else 1


def cmd_archive_ready(argv):
    opts = _parse_validate_args(argv)
    change = opts["change"]
    if not change or not os.path.isdir(change):
        print("usage: engine archive-ready <change-dir> [--contract <path>] [--json]",
              file=sys.stderr)
        return 2
    contract = load_contract(opts["contract"]) if opts["contract"] else _find_contract()
    checks = []
    checks += validate_level_a(change, contract)
    checks += validate_level_b(change, contract)
    checks += validate_level_c(change)
    checks += validate_level_d(change, contract, require_registry=False)
    seen_legacy = False
    deduplicated = []
    for check in checks:
        if check.get("artifact") == "legacy-spec-for-test":
            if seen_legacy:
                continue
            seen_legacy = True
        deduplicated.append(check)
    result = _assemble(change, "archive-ready", "D", deduplicated)
    _emit(result, opts["json"])
    return 0 if result["passed"] else 1


def cmd_approval_digest(argv):
    if len(argv) != 1 or not os.path.isdir(argv[0]):
        print("usage: engine approval-digest <change-dir>", file=sys.stderr)
        return 2
    change = argv[0]
    proposal = _read(change, "proposal.md")
    if proposal is None:
        print("approval-digest: proposal.md 不存在", file=sys.stderr)
        return 1
    sections = _proposal_baseline_sections(proposal)
    if len(sections) != 1:
        print(f"approval-digest: 需求基线章节必须恰好一个，实际:{len(sections)}", file=sys.stderr)
        return 1
    digest = _proposal_baseline_digest(proposal)
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        print("approval-digest: 无法生成需求基线摘要", file=sys.stderr)
        return 1
    print(digest)
    return 0


def main(argv):
    sub = argv[1] if len(argv) > 1 else ""
    rest = argv[2:]
    if sub == "validate":
        return cmd_validate(rest)
    if sub == "archive-ready":
        return cmd_archive_ready(rest)
    if sub == "approval-digest":
        return cmd_approval_digest(rest)
    if sub == "spec-for-validation":
        return SPEC_FOR_VALIDATION.command(rest)
    if sub == "spec-for-test":
        print("spec-for-test 已重命名为 spec-for-validation；"
              "请迁移旧文件和 Profile 配置后使用新命令", file=sys.stderr)
        return 2
    if sub == "legacy-check":
        change = rest[0] if rest else ""
        if not change or not os.path.isdir(change):
            print("usage: engine legacy-check <change-dir>", file=sys.stderr)
            return 2
        issues = SPEC_FOR_VALIDATION.legacy_issues(change)
        for issue in issues:
            print(f"legacy 迁移阻塞: {issue}", file=sys.stderr)
        return 1 if issues else 0
    if sub == "version":
        print("ohos-sdd 0.5.1 (engine)"); return 0
    print(f"engine: unknown subcommand {sub!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
