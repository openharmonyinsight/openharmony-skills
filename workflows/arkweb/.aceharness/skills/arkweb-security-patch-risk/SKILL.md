---
name: arkweb-security-patch-risk
description: Assess residual risk after ArkWeb security patch merge, review, and build verification.
descriptionZH: ArkWeb 风险记录技能。记录安全、兼容性、稳定性、性能、ROM 和回滚风险，风险项不阻塞提交。
tags: [ArkWeb, risk, release]
---

# ArkWeb Risk Assessment

用于 `arkweb-security-patch-risk-assessor`。

## 输出

单 issue 模式写入 `.ace-outputs/{runId}/11_risk_assessment.md`。

批量模式必须逐个 issue 评估，读取 `issues/{issue_id}/06_merge_result.md`、`issues/{issue_id}/08_code_review.md`、`issues/{issue_id}/09_build_verification.md` 以及输入归档目录的 `03_impact_decision.md/json`。每个 issue 写入 `.ace-outputs/{runId}/issues/{issue_id}/11_risk_assessment.md`，总览写入 `.ace-outputs/{runId}/11_risk_assessment.md`。

必须包含：

1. 安全风险是否闭环。
2. 兼容性、稳定性、性能、ROM、构建风险。
3. 回滚建议。
4. 是否存在前序产物证明的 patch 未合入或编译误报。
5. 编译门槛状态：`build_completed`、`build_status`、`exit_code`、`nonblocking_unrelated_build_failure`、`submit_eligible`。

## 规则

- 风险项只记录，不阻塞提交上库。
- 不得把未知项、人工跟踪项或非当前步骤事项作为 fail 原因。
- 给定 patch 已真实合入，且本地编译通过，或编译命令完整退出后失败已证明与本次 patch 无关并记录为非阻塞编译风险时，必须允许提交上库。
- 编译进程中断、超时、无真实退出码、后台进程失联、重跑仍未完成、build.log 不可信、`build_completed=false` 或 `submit_eligible=false` 不属于非阻塞编译风险；这种情况必须阻止提交并进入结果归档。
- “编译失败与本次 patch 无关”必须建立在一次可信的完整编译退出结果上；没有完整退出码时不能做无关放行。
- 只有前序产物证明给定 patch 未真实合入，或与本次 patch 相关的编译失败却被误报为通过/无关，才允许输出阻塞结论；这种阻塞表示前序产物不可信，应进入结果归档记录证据，不得建议回到自动合入或编译验证形成循环。
- 批量模式不得把多个 issue 的风险混成一个统一结论；每个 issue 必须独立记录风险摘要。
- 批量模式必须保留 overlap 信息：如果多个 issue 修改同一文件，自动合入阶段应已按 issue_id 数值升序为每个重复文件组选择 winner。winner issue 属于 active batch，风险评估必须正常记录其合入/编译/提交风险；非 winner issue 应已标记 `deferred_for_archive` 并退出 active batch，风险评估中只说明这些 issue 未进入本轮合入/编译/提交，最终由结果归档列为遗留，不得建议把多个 issue 合成一个提交。
- 评估必须基于当前 issue 的产物和当前工程目标子仓中属于该 issue 的 diff；历史脏改不属于当前 issue 风险。

## 最终裁决 JSON

回复末尾必须输出完整 JSON 代码块，字段固定为：

```json
{
  "verdict": "pass|conditional_pass|fail",
  "next_state": "提交上库|结果归档",
  "issues": [],
  "summary": "一句话总结"
}
```

不得用 Supervisor 风格的“当前阶段结论 / 是否建议继续迭代 / 下一步指导意见”替代最终 JSON。
