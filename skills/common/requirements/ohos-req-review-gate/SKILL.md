---
name: ohos-req-review-gate
description: Use when performing the Phase 0 Step 0.5 Review Ready Gate on a 04-feature.md, especially when the user says "evaluate gate", "review readiness", "feature ready?", "should we generate IR", or when the ohos-intake main session needs a structured Ready / Conditional Ready / Not Ready judgment instead of doing the check inline. Reads 01-04, runs seven fixed checks plus a conditional-items check, and returns a machine-readable JSON summary plus a human-readable table that the main session can route on.
metadata:
  author: openharmony
  scope: common
  stage: requirements
  domain: sdd
  capability: review-gate
  version: 0.1.0
  status: draft
  tags:
    - sdd
    - requirements
---

# OHOS Review Ready Gate (结构化判定)

**Announce at start:** "我正在使用 ohos-review-gate skill 对 04-feature.md 执行 Review Ready Gate。"

## 定位

`ohos-feature` skill 在生成 `04-feature.md` 时已嵌入 8 项"评审就绪检查"清单（检查项定义见本 skill 下文「Gate 检查项」）。本 skill 把这套检查从"主 session 凭印象判断"升级为**独立 subagent 结构化判定**，输出**机器可读的 JSON 决策结果**和**人类可读的表格**。

主 session 不再自己读 01-04 推算 Gate 结论，而是**只读取本 skill 的 JSON 输出**做路由。

## 适用边界

- ✅ 适用：Phase 0 Step 0.5（Feature 评审就绪）
- ❌ 不适用：决策 0（立项评审）、决策 1（方案确认）、决策 1.5（SIG 评审）、决策 2（Phase 4 评审）、决策 3（代码审查）、Phase 5 Step 5.2（设计待解决问题门禁）——这些由主 session / 后续 phase 流程承载
- 后续如果其他决策点也需要物化，可参考本 skill 的 JSON 输出契约复制推广

## 输入

- `{docs_dir}/01-requirement.md`
- `{docs_dir}/02-feasibility.md`
- `{docs_dir}/03-decision.md`
- `{docs_dir}/04-feature.md`
- `reference/feature-checklist.md`（检查项定义来源）

`04-feature.md` 不存在时**直接判定为 Not Ready**，并返回错误说明（不试图推断）。

## Gate 检查项（8 项固定 + 3 项结构一致性 + 1 项遗留问题闭环 = 12 项；条件项为独立字段）

8 项固定检查对应 `feature.md` §1-§5（拆分决策与工作量约束同属 §5）+ 技术方向（引用 03-decision.md）+ 影响性分析（模板外补充章节），避免规则两套。3 项结构一致性检查为本 skill 新增，确保跨文档数据传播完整。1 项遗留问题闭环检查确保 03-decision.md §6 由用户评审会议输入且闭环可追溯。逐项读取 `04-feature.md` 对应章节，按以下规则判定：

**固定检查项（8 项）**：

| 检查项 | 要求 | 判定方法 |
|--------|------|----------|
| 概述与价值 | 有核心诉求和业务价值描述 | §1 章节存在且非占位符 |
| 范围明确 | 目标和非目标已列出 | §2 章节存在且非占位符 |
| AC 完整 | 有可观察指标和验证方式 | §3 至少 1 条 AC 行非占位符 |
| 受影响范围 | 明确跨仓模块、Owner/SIG | §4 至少 1 条影响范围行非占位符 |
| 拆分决策 | 有拆分结论和 proposal 边界 | §5 章节存在且非占位符 |
| 工作量约束 | 每个 proposal ≤5 人月（如已拆分） | §5 每个 proposal 工作量 ≤5 |
| 技术方向 | 有选定方案（引用 decision.md） | 选定方案引用 03-decision.md（feature 模板无对应章节） |
| 影响性分析 | 5方影响类型已分析 | 影响性分析章节（模板外补充）5 行均非占位符 |

**结构一致性检查项（3 项新增，仅做 Ready/Conditional/Not Ready 决策判定，不重复校验内容）**：

> **职责边界：** `ohos-feature` skill 在生成期做模块覆盖完整性/术语一致性的逐项校验和修复；本 skill 只做最终的 Ready/Conditional/Not Ready 决策判定，引用 feature skill 的校验结果（不重复执行校验逻辑）。条件项传播完整性为本 skill 独有（feature skill 不涉及 02/03 的条件项跨文档追溯）。

| 检查项 | 要求 | 判定方法 |
|--------|------|----------|
| 模块覆盖完整性 | 04 §4声明覆盖了所有涉及模块（引用 feature skill 校验结论） | 读取 04 §4"模块覆盖检查"结论字段；结论=pass→pass；结论=warn或缺失→warn（block_reasons: "模块覆盖检查未通过或未执行"） |
| 影响类型术语一致性 | 04 §4影响类型标签无漂移（引用 feature skill 校验结论） | 读取 04 §4"术语一致性检查"结论字段；结论=pass→pass；结论=warn或缺失→warn |
| 条件项传播完整性 | §5拆分前置条件覆盖 02 §6 和 03 §6 全部条件项 | 提取02/03中所有条件项编号，验证每个出现在04 §5；缺失→warn |

**遗留问题闭环检查项（1 项新增）**：

| 检查项 | 要求 | 判定方法 |
|--------|------|----------|
| 遗留问题闭环 | 03-decision.md §6 遗留问题由用户评审会议输入且每条负责人/解决动作/计划关闭时间齐全 | 读取03 §6：①含占位标注`[待用户评审会议后填写]`→fail（block_reasons:"03-decision.md §6遗留问题未由用户评审会议输入"）；②任一遗留项缺少负责人/解决动作/计划关闭时间→fail（block_reasons:"遗留项三字段不全"）；③无遗留项（用户认定无需遗留）或全部齐全→pass |

**条件项检查（独立字段）**：
- `04-feature.md` 中所有标记为"⚠️"或"未通过/未知"的项必须都有 Owner 和关闭时点，否则提升为失败项

## 流程

1. 读取 `04-feature.md`（不存在 → 直接 `Not Ready` + 错误原因）。
2. 读取 §1-§5 及影响性分析补充章节的内容，**只引用必要的摘要**（不嵌入 01-04 全文）。
3. 对每项检查按上表规则判定 `pass` / `warn` / `fail`。
4. 收集所有 `warn` 项作为条件项（必须含 Owner、关闭动作、关闭时点，否则升级为 `fail`）。
5. 汇总得到 Gate 结论：
   - `Ready`：无 `fail`，无 `warn`
   - `Conditional Ready`：无 `fail`，有 `warn` 且每条都有 Owner/动作/时点
   - `Not Ready`：有 `fail`，**或**有 `warn` 但缺少 Owner/动作/时点
6. 同时写两份产物：
   - `tmp/decision_gate_{feature_id}_{timestamp}.json`（机读）
   - `tmp/decision_gate_{feature_id}_{timestamp}.md`（人读摘要）
7. 回传主 session：路径 + 结论 + 失败/条件项计数。**不复读 01-04 内容。**

## 输出契约

### JSON Schema（机读）

```json
{
  "schema_version": "1.0",
  "skill": "ohos-review-gate",
  "feature_id": "<FEAT-YYYYMMDD-NNN>",
  "docs_dir": "<绝对路径>",
  "timestamp": "2026-07-01T23:30:00+08:00",
  "feature_md_exists": true,
  "checks": [
    {"id": "overview_value", "name": "概述与价值", "status": "pass", "evidence": "§1章节存在，含一句话核心诉求", "section_ref": "§1"},
    {"id": "scope", "name": "范围明确", "status": "pass", "evidence": "...", "section_ref": "§2"},
    {"id": "ac_complete", "name": "AC 完整", "status": "warn", "evidence": "§3有 5 条 AC，其中 AC-04 缺验证方式", "section_ref": "§3"},
    {"id": "affected_scope", "name": "受影响范围", "status": "pass", "evidence": "...", "section_ref": "§4"},
    {"id": "split_decision", "name": "拆分决策", "status": "pass", "evidence": "...", "section_ref": "§5"},
    {"id": "effort_constraint", "name": "工作量约束", "status": "pass", "evidence": "每个 proposal ≤5 人月", "section_ref": "§5"},
    {"id": "tech_direction", "name": "技术方向", "status": "pass", "evidence": "...", "section_ref": "技术方向(03-decision.md)"},
    {"id": "impact_analysis", "name": "影响性分析", "status": "pass", "evidence": "5方影响类型已分析", "section_ref": "影响性分析(模板外补充)"},
     {"id": "module_coverage", "name": "模块覆盖完整性", "status": "pass", "evidence": "04§4覆盖02§2.1全部仓库", "section_ref": "02§2.1→04§4"},
     {"id": "term_consistency", "name": "影响类型术语一致性", "status": "pass", "evidence": "影响类型标签一致", "section_ref": "02§2.1→04§4"},
     {"id": "condition_propagation", "name": "条件项传播完整性", "status": "pass", "evidence": "04§5覆盖02/03全部条件项", "section_ref": "02§6+03§6→04§5"},
     {"id": "followup_closure", "name": "遗留问题闭环", "status": "pass", "evidence": "03§6遗留项由用户输入且三字段齐全", "section_ref": "03§6"}
  ],
  "conditions": [
    {"check_id": "ac_complete", "desc": "AC-04 缺验证方式", "owner": "<TBD or name>", "close_action": "<动作>", "close_at": "<时间点 or TBD>"}
  ],
  "summary": {"pass": 11, "warn": 0, "fail": 0},
  "gate": "Conditional Ready",
  "next_action": "生成 IR（Conditional Ready 允许），但 IR 必须引用条件项清单",
  "block_reasons": []
}
```

### 字段语义

- `gate`：仅取 `"Ready" | "Conditional Ready" | "Not Ready"`
- `summary.pass` / `summary.warn` / `summary.fail`：12 项检查的统计
- `conditions`：所有 `warn` 项 + 关闭信息（Owner/动作/时点），如 Owner/动作/时点缺失，由本 skill 自动从 warn 升级为 fail
- `next_action`：主 session 路由提示（如"生成 IR"、"阻塞回 Step 0.4 补全"、"阻塞：feature.md 不存在"）
- `block_reasons`：升级为 fail 的条件项描述（仅在 gate=Not Ready 时非空）

### Markdown 摘要（人读）

```
# Review Ready Gate 判定 — {feature_id}

时间: {timestamp}
docs_dir: {docs_dir}

## Gate 结论: {Ready | Conditional Ready | Not Ready}

## 检查项汇总

| # | 检查项 | 状态 | 证据 |
|---|--------|------|------|
| 1 | 概述与价值 | ✅/⚠️/❌ | ... |
| 2 | 范围明确 | ✅/⚠️/❌ | ... |
| ... | ... | ... | ... |

## 条件项（Conditional Ready 时列出）

| 来源 | 描述 | Owner | 关闭动作 | 关闭时点 |
|------|------|-------|---------|---------|
| §3 | AC-04 缺验证方式 | <name> | 补 AC 验证列 | Phase 2 启动前 |

## 下一步
- Ready → 执行 ohos-feat-to-ir 生成 IR
- Conditional Ready → 执行 ohos-feat-to-ir，但 IR.md 末尾「条件项清单」补充章节必须填写
- Not Ready → 回 Step 0.4 补全；feature.md 不存在时直接到 Step 0.4
```

## 与主 Session 的契约

主 session 在 Phase 0 Step 0.5 时：

```
1. spawn ohos-review-gate subagent，task 仅含 docs_dir 绝对路径（不嵌 01-04 全文）
2. 等待 subagent 回传路径
3. 读 tmp/decision_gate_*.json（≤100 行结构化数据，符合 Token 经济性规则）
4. 根据 gate 字段路由：
   - "Ready"           → spawn ohos-feat-to-ir
   - "Conditional Ready" → spawn ohos-feat-to-ir（task 中追加 conditions 摘要）
   - "Not Ready"       → 阻塞；如 block_reasons 非空，用其内容生成 AskUserQuestion
```

## NEVER

- **禁止主 session 自行读 01-04 推算 Gate**: 必须通过 spawn 独立 subagent 执行，本 skill 的 JSON 输出是唯一 Gate 结论
- **禁止在 Gate 输出 JSON 中添加 schema 外字段**: schema_version 1.0 固定字段不可增删，主 session 仅消费 gate/conditions/block_reasons 字段
- **禁止在 04-feature.md 不存在时尝试从 01-03 推断 Gate 结论**: 必须直接判定 Not Ready 并返回错误说明

## 错误处理

| 场景 | 行为 |
|------|------|
| 04-feature.md 不存在 | 返回 `feature_md_exists: false`、`gate: "Not Ready"`、`block_reasons: ["04-feature.md 不存在，请先执行 ohos-feature"]` |
| 04-feature.md 存在但 8 项表格完全空白 | 视为 Not Ready，所有 8 项均记 fail |
| 02/03 缺失但 04 存在 | 仅依据 04 判定 8 项固定检查；3 项结构一致性检查退化规则：02缺失时 module_coverage / term_consistency / condition_propagation 均判 `warn`；03缺失时 condition_propagation 判 `warn` + followup_closure 判 `fail`（block_reasons: "03-decision.md 缺失，遗留问题闭环无法验证"）；02+03同时缺失时 4 项均判 `warn`/`fail` |
| JSON 写入失败 | 回传错误，主 session 退化为人工 Gate |

## 自检

- [ ] 8 项检查与 `feature.md` §1-§5 + 技术方向/影响性分析完全对齐，无新增无删减
- [ ] 3 项结构一致性检查已执行（模块覆盖/术语一致性/条件项传播）
- [ ] 1 项遗留问题闭环检查已执行（03 §6 用户输入+三字段齐全）
- [ ] 条件项 Owner/动作/时点缺失时自动升级为 fail
- [ ] JSON 字段与 schema_version 一致
- [ ] Markdown 摘要表行数 = 12（8固定+3结构+1遗留）
- [ ] 不嵌入 01-04 全文到 task
- [ ] 回传 ≤ 15 行

## 输出

- 路径：
  - `tmp/decision_gate_{feature_id}_{timestamp}.json`
  - `tmp/decision_gate_{feature_id}_{timestamp}.md`
- 回传：JSON 路径、Gate 结论、pass/warn/fail 计数、block_reasons 数量
