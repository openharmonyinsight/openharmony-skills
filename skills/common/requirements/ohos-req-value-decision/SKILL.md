---
name: ohos-req-value-decision
description: Use after review meeting to record decision and close or route the requirements intake review flow. Triggers: 评审决策纪要, 评审结论回流, value decision, 评审接纳, 评审不接纳, 评审退回, 下次重新上会. Do NOT use for feature/proposal baseline and built-in gate checks (ohos-req-feature-proposal-baseline).
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: value-decision
  version: 0.4.0
  status: draft
  tags:
    - sdd
    - requirements
    - review
    - decision
    - gate
---

# 评审决策纪要回流

**Announce at start:** "我正在使用 ohos-req-value-decision skill 记录评审决策纪要。"

## 定位

requirements Step 14 — 评审会议后的决策纪要回流。在 Feature/Proposal 基线内建 Gate 和可选 value-ppt-gen 之后执行，是需求导入评审流程的收尾步骤。

```
feature-proposal-baseline(Step 10-12, 内建 Gate) → value-ppt-gen(可选) → [评审会议] → value-decision(Step 14)
                                                                                  ├─ 接纳 → 评审流程完成
                                                                                  ├─ 不接纳 → 关闭/归档
                                                                                  └─ 下次重新上会 → 退回对应 Step
```

## 适用边界

- ✅ 适用：requirements Step 14（评审会议后决策纪要生成与路由）
- ❌ 不适用：Feature/Proposal 基线生成和 Review Ready Gate（用 ohos-req-feature-proposal-baseline）

## 输入

- 评审会议纪要（用户提供）
- 01-requirement.md ~ 04-feature.md（现有产物）
- 04-feature.md 中的 Gate 结论和条件项摘要

## 决策歧义处理规则

评审会议纪要中的结论表述可能不标准。以下规则将非标准表述映射为三选一决策：

| 会议纪要原文 | 映射结论 | 理由 |
|-------------|---------|------|
| "接纳"/"通过"/"同意" | Accepted | 明确通过 |
| "不接纳"/"不通过"/"否决"/"驳回" | Rejected | 明确否决 |
| "下次重新上会"/"有条件通过"/"基本同意但需修改" | PendingRe-review | 需要修改后重审 |
| "原则上同意" | **要求用户明确** | "原则上同意"是歧义表述，必须追问：是接纳（修改意见在后续阶段处理）还是下次重新上会（修改后重审）？不可自行推断 |
| 无法判断结论 | **要求用户明确** | 不可凭模糊表述自行决策路由方向 |

> Before mapping a conclusion, ask yourself: "Did the user explicitly state one of the three outcomes, or am I inferring it?" If inferring, ask the user to clarify.

> Before choosing the rollback Step, ask yourself: which is the lowest-numbered doc requiring modification? Am I tracing each modification requirement to its source document?

> Before extracting review opinions, ask yourself: does each opinion have both a handling method and an owner? If not, mark [待补充] rather than leaving blank.

## 流程

1. 读取 `04-feature.md` 的 `decision_gate.gate`。若 Gate 为 `Not Ready`，必须硬阻断 Accepted/评审完成状态，只允许生成 rollback 路由到 Feature/Proposal 基线（target_step=10，target_skill=`ohos-req-feature-proposal-baseline`），并停止读取会议结论。
2. 读取评审会议纪要。**如果用户未提供会议纪要，禁止凭空生成决策记录** — 追问用户。
3. 按上表将结论映射为 Accepted / Rejected / PendingRe-review。遇歧义表述时追问用户明确。
4. 提取评审意见：每条意见必须有**处理方式**和**负责人**。缺失时标记 `[待补充]` 并在自检环节提示。
5. 根据 conclusions 路由：
   - **Accepted**：生成 value-decision-record.md（status: Accepted），评审流程完成
   - **Rejected**：生成 value-decision-record.md（status: Rejected），关闭/归档
   - **PendingRe-review**：生成 value-decision-record.md（status: PendingRe-review），标注需退回的 Step 和修改要求
5. 更新 04-feature.md 的评审状态（如有修改）

## 退回 Step 判定规则

PendingRe-review 时需标注退回哪个 Step。判定依据：

| 修改要求涉及的文档 | 退回 Step | 理由 |
|-------------------|----------|------|
| 01-requirement.md 需修改 | Step 1 | 需求基线变更，下游 02-04 全部需级联更新 |
| 02-feasibility.md 需修改 | Step 5 | 可行性结论变更影响 03/04 |
| 03-arch-decision-record.md 需修改 | Step 7 | 方案变更影响 04 |
| 04-feature.md 需修改 | Step 10 | Feature 内容调整 |
| 多个文档需修改 | 退回**最低编号** Step | 从源头修复，避免中间文档不一致 |

## 输出契约

### JSON Schema（机读）

```json
{
  "schema_version": "1.0",
  "skill": "ohos-req-value-decision",
  "feature_id": "<FEAT-YYYYMMDD-NNN>",
  "rr_id": "<从 01-requirement.md frontmatter 继承>",
  "review_date": "YYYY-MM-DD",
  "participants": ["张三", "李四"],
  "decision": "Accepted | Rejected | PendingRe-review",
  "review_opinions": [
    {"id": "R-1", "opinion": "补充性能基线数据", "handling": "Phase 2补充", "owner": "李四"}
  ],
  "modifications": [
    {"doc": "01-requirement.md", "requirement": "补充用户场景量化数据"}
  ],
  "routing": {
    "action": "proceed | close | rollback",
    "target_step": "null | 1 | 5 | 7 | 10",
    "target_skill": "null | ohos-req-requirement-intake | ohos-req-feasibility-analysis | ohos-req-arch-decision | ohos-req-feature-proposal-baseline"
  },
  "next_action": "需求导入评审流程完成 | 关闭/归档 | 退回 Step X"
}
```

### 字段语义

- `decision`：仅取 `"Accepted" | "Rejected" | "PendingRe-review"`，不可使用其他值
- `routing.action`：`proceed`（接纳→放行）/ `close`（不接纳→关闭）/ `rollback`（退回）
- `routing.target_step`：仅 rollback 时有值，取修改要求涉及文档对应的最低编排 Step（01→1，02→5，03→7，04→10）
- `review_opinions[].handling` + `review_opinions[].owner`：每条意见必须两个字段同时存在，缺失时填 `[待补充]`

## 决策纪要格式

按 JSON Schema 输出。Markdown 人读版仅含：评审日期、参与人、结论(status)、Feature ID、RR单号、评审意见表(编号/意见/处理方式/负责人)、修改要求(如有)、路由结论。

## NEVER

- **禁止在未提供评审会议纪要时凭空生成决策记录**：决策结论必须来自用户提供的评审会议纪要，AI 不得替用户做决策
- **禁止将"原则上同意"直接映射为 Accepted**：这是歧义表述，必须追问用户明确是接纳还是下次重新上会
- **禁止将 PendingRe-review 的退回 Step 留空**：必须按退回 Step 判定规则标注具体 Step 编号
- **禁止在 review_opinions 中省略 handling 或 owner 字段**：缺失时填 `[待补充]`，不可留空或省略

## 错误处理

| 场景 | 行为 |
|------|------|
| 未提供评审会议纪要 | 追问用户："请提供评审会议纪要，我需要从中提取决策结论和评审意见。" |
| 结论表述歧义（如"原则上同意"） | 追问用户："评审结论'原则上同意'是接纳（修改意见在后续阶段处理）还是下次重新上会（修改后重审）？" |
| 评审意见缺少处理方式或负责人 | 该字段填 `[待补充]`，在自检环节提示用户补全 |
| 04-feature.md Gate 结论为 Not Ready | 硬阻断 Accepted/评审完成状态；生成或回传 rollback 到 Feature/Proposal 基线（target_step=10），提示用户先修复 Gate 阻塞项 |

## 自检

- [ ] 决策结论明确（Accepted/Rejected/PendingRe-review），非歧义推断
- [ ] Gate=Not Ready 时未生成 Accepted/流程完成状态，且 routing.target_step=10
- [ ] 评审意见每条有处理方式和负责人（缺失标 [待补充]）
- [ ] PendingRe-review 时有明确修改要求和退回 Step 编号
- [ ] 退回 Step 为修改要求涉及的文档中最低编号
- [ ] value-decision-record.md 已生成
- [ ] JSON 输出 schema_version 1.0 字段完整
- [ ] routing.target_skill 与 target_step 一致

## 输出

- 路径：`{docs_dir}/value-decision-record.md`
- 回传：结论 + 评审意见数 + 路由动作 + 退回 Step（如有）
