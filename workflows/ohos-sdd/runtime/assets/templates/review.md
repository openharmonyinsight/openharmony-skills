# Review Gate 汇总

> 本文件只汇总 `GA / GB / GC` 门禁状态并索引独立 Review Evidence。逐 AC 结论、代码 finding、质量维度和验证执行记录必须分别写入 `evidence/reviews/spec-compliance.md`、`code-quality.md`、`verification.md`，不得在此复制。

## 审查元数据

| 项 | 内容 |
|----|------|
| Review ID | [REV-XXXX] |
| Change ID | [issue/draft id] |
| Base / Head | `[base SHA]` / `[head SHA]` |
| Reviewer / Date | [reviewer] / [date] |

## GA / GB / GC 汇总

| Gate | 范围 | 状态 | 权威证据 | 审批人 / 日期 |
|------|------|------|----------|---------------|
| GA | proposal 需求基线 | Approved/ChangesRequested/Blocked | `proposal.md` + `evidence/checks/check-proposal.md` | [approver] / [date] |
| GB | spec/design/execution-plan 基线 | Approved/ChangesRequested/Blocked | `evidence/checks/check-spec.md`、`check-design.md`、`check-execution-plan.md` | [approver] / [date] |
| GC | 实现、审查与验证闭环 | Approved/ChangesRequested/Blocked | `execution-plan.md` + 下方三份 Review Evidence | [approver] / [date] |

## Review Evidence 索引

| Evidence | Output | Reviewed Scope | Verdict |
|----------|--------|----------------|---------|
| Spec Compliance | `evidence/reviews/spec-compliance.md` | `[spec revision / base..head]` | Approved/Needs Changes/Blocked |
| Code Quality | `evidence/reviews/code-quality.md` | `[commit / PR / diff range]` | Approved/Needs Changes/Blocked |
| Verification | `evidence/reviews/verification.md` | `[commit / environment]` | Approved/Needs Changes/Blocked |

## 开放问题

| ID | Severity | Source | 问题摘要 | 处理方式 | Owner | 状态 |
|----|----------|--------|----------|----------|-------|------|
| [OPEN-1] | Blocker/Major/Minor/Follow-up | `[Evidence#anchor]` | [只写索引摘要，不复制 finding 详情] | Fix/Accept/Track | [Owner] | Open/Resolved/Accepted |

## 最终决策

| 项 | 内容 |
|----|------|
| Decision | Approved / ChangesRequested / Blocked / Superseded |
| Merge / Delivery | Allowed / Not Allowed |
| Recheck Scope | [Evidence 路径与锚点；无则 N/A] |
| Accepted Risks | [开放问题 ID；无则 N/A] |
| Decision Maker / Date | [姓名] / [日期] |

> `Decision: Approved` 仅表示汇总结果；归档和合入仍以三份 Evidence 的唯一 Approved Verdict、实现追溯和 fresh validate 结果为准。
