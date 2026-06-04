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

## 稳定脚本优先

优先使用内置脚本生成风险评估产物，不要在运行时拼接临时 Python/Node/Shell 脚本：

```bash
python3 skills/arkweb-security-patch-risk/scripts/generate_risk_assessment.py \
  --run-root <context.projectRoot>/.ace-outputs/<runId>
```

脚本会读取 `batch_status.json`、`09_build_verification.md` 和各 issue 的 `03_impact_decision.json` / `06_merge_result.json`，写入根级 `11_risk_assessment.md/json` 和 issue 级 `11_risk_assessment.md/json`。脚本只把 active/ready issue 纳入提交候选；`terminal_failed` / `deferred_for_archive` 只进入归档清单。

脚本执行后，agent 回复只允许包含：

- 一行产物路径说明；
- 一行脚本执行结果摘要。

不要在回复中粘贴完整前序产物、大段风险表、完整 JSON 文件、工具输出或脚本源码。详细证据只写入 `11_risk_assessment.md/json`。最终回复禁止使用 Supervisor 阶段审阅话术，例如“当前阶段结论 / 是否建议继续迭代 / 下一步指导意见”。
最终回复也禁止使用“总体建议 / 当前状态机 / 阶段应视为 / 建议先 / 建议下一步 / 除非你准备”等审阅或指导类措辞；不要评价状态机，不要提出流程建议，只报告脚本产物。
最终回复禁止输出 JSON 代码块；状态机裁决只由后续「风险评估裁决」步骤读取 `11_risk_assessment.json` 完成。

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

## 裁决产物

脚本和产物必须写入完整 `11_risk_assessment.json`，字段固定为：

```json
{
  "verdict": "pass|conditional_pass|fail",
  "next_state": "提交上库|结果归档",
  "issues": [],
  "summary": "一句话总结"
}
```

不得在最终回复中输出上述 JSON；不得用 Supervisor 风格的“当前阶段结论 / 是否建议继续迭代 / 下一步指导意见”替代产物。
