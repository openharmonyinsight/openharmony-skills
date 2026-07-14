---
name: ohos-req-value-decision
description: Use after review meeting to record decision and route to next step. Triggers: 评审决策纪要, 评审结论回流, value decision, 评审接纳, 评审不接纳.
metadata:
  author: openharmony
  scope: common
  stage: requirements
  capability: value-decision
  version: 0.1.0
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

## 输入

- 评审会议纪要（用户提供）
- 01-requirement.md ~ 04-feature.md（现有产物）
- decision_gate_{id}_{ts}.json（review-gate 产出）

## 输出

| 产物 | 路径 | 说明 |
|------|------|------|
| value-decision-record.md | {docs_dir}/value-decision-record.md | 评审决策纪要 |

## 流程

1. 读取评审会议纪要和现有 01-04 文档
2. 提取决策结论：接纳 / 不接纳 / 下次重新上会
3. 如有修改意见，记录到决策纪要中
4. 根据结论路由：
   - **接纳**：生成 value-decision-record.md（status: Accepted），放行 feature-to-ir
   - **不接纳**：生成 value-decision-record.md（status: Rejected），关闭/归档
   - **下次重新上会**：生成 value-decision-record.md（status: PendingRe-review），标注需退回的 Step 和修改要求
5. 更新 04-feature.md 的评审状态（如有修改）

## 决策纪要格式

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

## 自检

- [ ] 决策结论明确（接纳/不接纳/下次重新上会）
- [ ] 评审意见每条有处理方式和负责人
- [ ] "下次重新上会"时有明确修改要求
- [ ] value-decision-record.md 已生成

## 输出

- 路径：`{docs_dir}/value-decision-record.md`
- 回传：结论 + 评审意见数 + 路由动作
