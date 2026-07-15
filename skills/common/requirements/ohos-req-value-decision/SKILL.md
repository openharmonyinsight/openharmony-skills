---
name: ohos-req-value-decision
description: Use after review meeting to record decision and route to next step. Triggers: 评审决策纪要, 评审结论回流, value decision, 评审接纳, 评审不接纳, 评审退回, 下次重新上会. Do NOT use for feature baseline (ohos-req-feature-baseline), review gate checks (ohos-req-review-gate), or IR generation (ohos-req-feature-to-ir).
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: value-decision
  version: 0.2.0
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

Phase 0 Step 0.6 — 评审会议后的决策纪要回流。在 review-gate（0.5）和 value-ppt-gen 之后、feature-to-ir（0.7）之前。

```
review-gate(0.5) → value-ppt-gen → [评审会议] → value-decision(0.6) → (接纳) → feature-to-ir(0.7)
                                                ├─ 不接纳 → 关闭/归档
                                                └─ 下次重新上会 → 退回对应 Step
```

## 适用边界

- ✅ 适用：Phase 0 Step 0.6（评审会议后决策纪要生成与路由）
- ❌ 不适用：Feature 评审就绪门禁（用 ohos-req-review-gate）、Feature 基线生成（用 ohos-req-feature-baseline）、IR 生成（用 ohos-req-feature-to-ir）

## 输入

- 评审会议纪要（用户提供）
- 01-requirement.md ~ 04-feature.md（现有产物）
- decision_gate_{id}_{ts}.json（review-gate 产出）

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

## 流程

1. 读取评审会议纪要。**如果用户未提供会议纪要，禁止凭空生成决策记录** — 追问用户。
2. 按上表将结论映射为 Accepted / Rejected / PendingRe-review。遇歧义表述时追问用户明确。
3. 提取评审意见：每条意见必须有**处理方式**和**负责人**。缺失时标记 `[待补充]` 并在自检环节提示。
4. 根据 conclusions 路由：
   - **Accepted**：生成 value-decision-record.md（status: Accepted），放行 feature-to-ir
   - **Rejected**：生成 value-decision-record.md（status: Rejected），关闭/归档
   - **PendingRe-review**：生成 value-decision-record.md（status: PendingRe-review），标注需退回的 Step 和修改要求
5. 更新 04-feature.md 的评审状态（如有修改）

## 退回 Step 判定规则

PendingRe-review 时需标注退回哪个 Step。判定依据：

| 修改要求涉及的文档 | 退回 Step | 理由 |
|-------------------|----------|------|
| 01-requirement.md 需修改 | Step 0.1 | 需求基线变更，下游 02-04 全部需级联更新 |
| 02-feasibility.md 需修改 | Step 0.2 | 可行性结论变更影响 03/04 |
| 03-arch-decision-record.md 需修改 | Step 0.3 | 方案变更影响 04 |
| 04-feature.md 需修改 | Step 0.4 | Feature 内容调整 |
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
    "target_step": "0.7 | null | 0.1",
    "target_skill": "ohos-req-feature-to-ir | null | ohos-req-requirement-intake"
  },
  "next_action": "可进入 feature-to-ir (Step 0.7) | 关闭/归档 | 退回 Step 0.X"
}
```

### 字段语义

- `decision`：仅取 `"Accepted" | "Rejected" | "PendingRe-review"`，不可使用其他值
- `routing.action`：`proceed`（接纳→放行）/ `close`（不接纳→关闭）/ `rollback`（退回）
- `routing.target_step`：仅 rollback 时有值，取最低编号 Step
- `review_opinions[].handling` + `review_opinions[].owner`：每条意见必须两个字段同时存在，缺失时填 `[待补充]`

### Markdown 模板（人读）

```markdown
# 评审决策纪要

| 字段 | 内容 |
|------|------|
| 评审日期 | YYYY-MM-DD |
| 参与人 | [列表] |
| 结论 | 接纳 / 不接纳 / 下次重新上会 |
| Feature ID | FEAT-XXXXX |
| RR单号 | [从 01-requirement.md 继承] |

## 评审意见

| 编号 | 意见 | 处理方式 | 负责人 |
|------|------|---------|--------|
| R-1 | [意见] | [处理] | [负责人] |

## 修改要求（下次重新上会时）

- [修改项1]
- [修改项2]

## 路由结论

- 接纳 → 可进入 feature-to-ir (Step 0.7)
- 不接纳 → 关闭/归档
- 下次重新上会 → 退回 [Step X]
```

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
| review-gate JSON 显示 Not Ready | 提示用户："review-gate 判定为 Not Ready，通常不应进入评审会议。请确认是否已通过 Gate。" |

## 自检

- [ ] 决策结论明确（Accepted/Rejected/PendingRe-review），非歧义推断
- [ ] 评审意见每条有处理方式和负责人（缺失标 [待补充]）
- [ ] PendingRe-review 时有明确修改要求和退回 Step 编号
- [ ] 退回 Step 为修改要求涉及的文档中最低编号
- [ ] value-decision-record.md 已生成
- [ ] JSON 输出 schema_version 1.0 字段完整
- [ ] routing.target_skill 与 target_step 一致

## 输出

- 路径：`{docs_dir}/value-decision-record.md`
- 回传：结论 + 评审意见数 + 路由动作 + 退回 Step（如有）
