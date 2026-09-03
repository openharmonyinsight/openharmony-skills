---
name: ohos-propose
description: Use when drafting, refreshing, or baselining a proposal.md, or when a new OH requirement or change enters the workflow. Do NOT use to make requirement changes without revising the baseline — always reopen the clarification and baseline cycle for post-spec changes.
license: MIT
---

# OHOS Propose

## Overview

起草/刷新 `proposal.md` 并冻结需求基线。proposal 是交付件依赖图的**根**(spec/design/plan 的上游),基线不稳则下游全摇晃。

**Core principle:** 先澄清再基线;基线需需求方/Owner/SIG 明确确认,不是 AI 自评。

## Prerequisites

- Part of the OHOS SDD workflow — see `using-ohos-sdd` for discovery and profile routing
- `manifest.md` tracks feature metadata including `profile` (repo classification)
- `{{ASSET_ROOT}}` is a build-time placeholder for the plugin's shared asset directory
- Slash command: `/ohos-propose` (draft or baseline proposal)

## 核心规则

1. 读 {{ASSET_ROOT}}/templates/proposal.md + manifest.md + {{ASSET_ROOT}}/workflow/workflow.md 依赖图
2. target_release 写 proposal frontmatter(不在 manifest,P2 已迁)
3. proposal 主文档只写“需求输入 + 需求基线”；澄清过程不得默认展开成归档正文
4. 先定义"不涉及项"(N/A 维度),避免实现期扩写
5. 填写 Agent Scope Guard:只约束探索阶段允许的仓/模块、禁止项、知识源授权和越界处理;精确实现文件范围留给 execution-plan/task
6. Agent 发现需访问未列仓/模块、禁止项或新知识源时立即停止,先更新 proposal 范围和基线,不得自行扩范围
7. 标准及以上复杂度仍需逐项澄清(可 invoke ohos-clarify)，但过程默认留在对话和 check evidence；仅 complex/critical 或澄清阻断、争议决策、跨 SIG/多仓协调时启用“澄清与决策记录”附录
8. 基线结论 = 通过/条件通过/不通过;需需求方/Owner/SIG 确认证据，确认人和确认依据写入基线信息
9. 若 manifest.profile ≠ none,按 {{ASSET_ROOT}}/workflow/profile-application.md 应用 profile 命中声明(读 profile 正文 + 追加专项检查)
10. 澄清未完成时保持 `phase_status: clarifying`;proposal 候选版本完成后置为 `phase_status: awaiting_approval`,输出范围/非目标/AC 摘要并明确请求“批准 Define”,然后停止
11. 候选基线固定后运行 `ohos-sdd approval-digest <change>` 生成 `baseline_digest`；仅当用户/Owner/SIG 明确回复“批准 Define”“确认以上范围并批准”或提供授权评审证据时,才写入 `phase_status: approved` 和完整 `approval`（含该摘要）；同时将需求输入表“Define 阶段状态”更新为 `Approved`。回答澄清问题、“没有补充”、“看起来可以”、`ReadyForReview` 或 AI 自评均不是批准
12. 未获得明确批准不得生成 spec.md、不得调用 `ohos-spec`;收到修改意见时置为 `changes_requested`,回到本 Skill 修改后重新请求批准
13. 产出:proposal.md(+ manifest.md 元数据)

## Rationalizations

| 念头 | 现实 |
|---|---|
| "需求很清楚不用澄清" | 标准及以上必须逐项澄清 |
| "先写 spec 再补 proposal" | proposal 是根,先基线 |
| "target_release 写 manifest" | P2 已迁 proposal frontmatter |
| "AI 自评基线通过" | 需求方/Owner/SIG 确认证据 |
| "先多搜几个仓再说" | 未列仓/模块属于越界,先更新 Agent Scope Guard 并重新确认基线 |
| "用户把问题答完了" | 澄清完成只进入 AwaitingApproval,不等于批准 Define |
| "用户说没有补充" | 没有补充不是审批语句,仍须明确请求批准 Define |

## Verification Checklist

- [ ] target_release 在 proposal frontmatter(id+status)
- [ ] 不涉及项已显式 N/A
- [ ] Agent Scope Guard 已明确允许仓/模块、禁止项、知识源授权和越界处理
- [ ] Proposal 未复制 Plan/Task 的精确实现文件清单
- [ ] 主文档只保存需求输入和基线结论，无常态化澄清过程日志
- [ ] 标准及以上:澄清逐项关闭；条件附录仅在触发时启用且争议项已关闭
- [ ] 基线结论有需求方/Owner/SIG 确认
- [ ] 需求输入表“Define 阶段状态”与 frontmatter `phase_status` 一致
- [ ] proposal 候选完成后已置为 AwaitingApproval、请求批准并停止
- [ ] 进入下游前 `phase_status: approved`,且 approval.status/approver/evidence/approved_at/baseline_digest 完整，`baseline_digest` 与当前需求基线一致
- [ ] `ohos-sdd validate . --level A` proposal(required)存在

## 输出

`proposal.md`(+ `manifest.md`)。仅在 Define 明确批准后进入下游 `ohos-spec`(见 `{{ASSET_ROOT}}/workflow/workflow.md` 依赖图);否则输出审批请求并结束当前轮次。
