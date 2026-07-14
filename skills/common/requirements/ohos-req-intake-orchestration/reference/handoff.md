---
feature_id: ""
rr_id: ""          # RR单号：从 01-requirement.md 继承，全链路追踪
generated_by: ""
date: ""
status: Draft
---

# Handoff 契约 — Phase 0 → Phase 1-9 交接

> 本文档是 Phase 0（需求导入）到 Phase 1-9（需求实现）的唯一交接点。
> 由 `ohos-intake` 流程结束时自动生成，由 `ohos-delivery` 启动时读取验证。

## Phase 0 完成状态

| 检查项 | 状态 | 路径 |
|--------|------|------|
| 01-requirement.md status=Clarified | ✅/⚠️/❌ | `{docs_dir}/01-requirement.md` |
| 02-feasibility.md 存在 | ✅/⚠️/❌ | `{docs_dir}/02-feasibility.md` |
| 03-decision.md status=Accepted | ✅/⚠️/❌ | `{docs_dir}/03-decision.md` |
| 04-feature.md Gate=Ready/Conditional Ready | ✅/⚠️/❌ | `{docs_dir}/04-feature.md` |
| 拆分结果已用户确认 | ✅/⚠️/❌ | 04-feature.md §五 |
| IR.md 存在 | ✅/⚠️/❌ | `{docs_dir}/IR.md` |
| proposal 文件存在 | ✅/⚠️/❌ | `{docs_dir}/05-proposal*.md` |
| SR 文件存在（GA-Approved 后） | ✅/⚠️/❌ | `{docs_dir}/SR-*.md` |

## Gate 状态

| 字段 | 值 |
|------|-----|
| Gate 结论 | Ready / Conditional Ready / Not Ready |
| 决策状态 | Accepted / PendingDecision |
| IR 状态 | Accepted |
| 条件项（Conditional Ready 时） | [列出条件项、Owner、关闭时点] |

## Phase 0 产物路径

| 产物 | 路径 |
|------|------|
| requirement | `{docs_dir}/01-requirement.md` |
| feasibility | `{docs_dir}/02-feasibility.md` |
| decision | `{docs_dir}/03-decision.md` |
| feature | `{docs_dir}/04-feature.md` |
| IR | `{docs_dir}/IR.md` |
| SR | `{docs_dir}/SR-*.md`（每个 proposal 一个） |

## 关键决策摘要

| 决策 | 结论 | 来源 |
|------|------|------|
| RR单号 | [RR单号，全链路追踪] | 01-requirement.md |
| 选定方案 | [方案名称一句话] | 03-decision.md §五 |
| Gate 结论 | [Ready/Conditional/Not Ready] | 04-feature.md §八 |
| 拆分方式 | [按仓+领域/按功能点/单一] | 04-feature.md §五 |

## Proposal 清单

| Proposal | 文件 | 拆分方式 | 估算工作量 | Owner | GA 状态 | SR 文件 |
|----------|------|----------|-----------|-------|---------|---------|
| [PROP-01] | `05-proposal-01.md` | [方式] | [X 人月，≤5] | [Owner] | GA-Approved / 待GA | `SR-01.md` |
| [PROP-02] | `05-proposal-02.md` | [方式] | [Y 人月，≤5] | [Owner] | GA-Approved / 待GA | `SR-02.md` |

## Phase 1-9 启动前置检查

> `ohos-delivery` 启动时必须验证以下全部通过：

- [ ] handoff.md 存在且可读取
- [ ] IR.md 文件存在
- [ ] 04-feature.md 存在且 Gate ≠ Not Ready
- [ ] 04-feature.md 拆分结果已经用户确认
- [ ] 03-decision.md 存在且 status=Accepted
- [ ] 03-decision.md §四 遗留问题由用户评审会议输入（非占位）
- [ ] 03-decision.md §四 每条遗留项负责人/解决动作/计划关闭时间齐全（任一缺失→阻断交接）
- [ ] 每个 proposal 估算工作量 ≤5 人月
- [ ] 至少一个 proposal 文件存在
- [ ] GA-Approved 的 proposal 均有对应 SR 文件

**任一检查不通过 → 阻断启动，提示用户回到 Phase 0 或手动补齐。**

## 交接说明

- Phase 1-9 以 `05-proposal*.md` 为入口，IR 和 feature 作为参考上下文
- Phase 0 产物（01-04/IR/SR）在 Phase 1-9 中被引用但不修改（除非澄清增量更新 proposal）
- Phase 1.6 立项决策可复用 04-feature.md 作为决策材料
- Phase 2.8 SIG 评审可复用 04-feature.md 作为评审输入

## 状态流转

| handoff.md status | 含义 | 允许动作 |
|-------------------|------|----------|
| Draft | Phase 0 流程进行中 | 仅 ohos-intake 可更新 |
| Ready | Phase 0 完成，所有前置检查通过 | ohos-delivery 可启动 |
| ConditionalReady | Phase 0 有条件完成 | ohos-delivery 可启动，但需标注条件项 |
| Blocked | Phase 0 前置检查不通过 | 禁止启动 ohos-delivery |
