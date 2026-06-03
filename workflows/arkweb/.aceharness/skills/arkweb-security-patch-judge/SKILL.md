---
name: arkweb-security-patch-judge
description: Judge ArkWeb state-machine step outputs and produce strict verdict JSON for state transitions.
descriptionZH: ArkWeb 状态机裁决技能。审查各阶段报告并输出严格 verdict/next_state JSON。
tags: [ArkWeb, judge, state-machine]
---

# ArkWeb Security Judge

用于 `arkweb-security-patch-judge`。

裁决 `ArkWeb 本地 Issue 分析归档与上游安全补丁自动合入` 时，先读本 skill 内的 [references/slim-workflow-state-policy.md](references/slim-workflow-state-policy.md)。不要引用其它 skill 的脚本或 md。

## 输出格式

每次裁决必须在回复末尾输出最后一个 JSON 代码块：

```json
{
  "verdict": "pass|conditional_pass|fail",
  "next_state": "合法状态名",
  "issues": [
    {
      "type": "security|design|implementation|test|performance",
      "severity": "critical|major|minor",
      "description": "..."
    }
  ],
  "summary": "一句话总结"
}
```

## 规则

1. `next_state` 必须是当前工作流中存在的状态名。
2. 不要在最终 JSON 之后再输出其它 JSON。
3. `conditional_pass` 不是通用“下一步通过”，必须严格服从当前工作流 YAML 中该状态的 transitions 映射；如果 YAML 把 `conditional_pass` 指向当前状态或修复状态，就必须按映射输出该 `next_state`。
4. 对阻塞问题必须列入 `issues`。
5. 当前 `impactMode=force_affected` 时，影响判定仍应如实评价证据，但流程会按受影响继续进入后续归档与合入流程。
6. 对“ArkWeb 本地 Issue 分析归档与上游安全补丁自动合入”：批量模式必须按阶段统一处理并按 issue 分流。自动合入阶段先判断 patch 修改文件是否重叠；涉及重复文件/overlap 时，按 issue_id 数值升序选择每个重复文件组里最小 issue_id 作为 winner 进入 active batch，不同重复文件组分别选择 winner 并可同时进入 active batch，其它 issue 标记为 `deferred_for_archive` 或 `terminal_failed`，退出 active batch，不进入冲突解决、编译或提交，只在结果归档说明遗留原因。自动合入后若仍有 active issue 需要最小手工写入，整体进入「冲突解决」，已合入 issue 只标记 ready_for_next 并等待；手工修复成功就是合入成功，`manual_applied=true` 或 `semantic_landed=true` 且 blockers 为空时不得因 `git apply` 曾失败而阻塞，`manual_attempted=true` 本身不能证明成功。冲突解决阶段只有在 pending_current_stage 清零后，才把全部 ready_for_next issue 作为 active batch 统一进入「代码审查」，terminal_failed/deferred_for_archive issue 只归档原因并从 active batch 剔除。代码审查中只审查 active batch；若 pending_current_stage 为空且 ready_for_next 非空，必须 pass 进入「编译验证」，不得因为 terminal_failed/deferred_for_archive issue fail 回「冲突解决」。只有 active batch 中仍存在未真实合入且可继续处理的 pending_current_stage issue，才回到「冲突解决」。编译验证阶段只有编译成功才能进入「风险评估」；任何完整非零退出都必须先进入「编译修复」做二次诊断、最小修复或无关归因，不能在编译验证阶段直接放行。编译中断、超时、无真实退出码或日志不可信必须按 build_interrupted/build_incomplete 处理并重跑，不能当作无关失败。只有编译修复阶段证明完整编译失败与本次 patch 无关时，才对该 issue 标记 ready_for_next 并等待统一进入「风险评估」；编译修复 no_progress 只让对应 issue terminal_failed；若 pending 清零且仍有 ready_for_next issue，必须 conditional_pass 进入「风险评估」，不得因为部分 issue terminal_failed 让整批进入「结果归档」。编译修复导致和上游 patch 原文不完全一致时，按 `semantic_landed`、`local_adaptations[]`、`compile_fix_files[]`、`deviation_reason` 和编译结果裁决，不能按字节差异直接失败。不得输出回到「自动合入」的裁决。
7. 本工作流里的“冲突解决”就是 git apply 失败、三方合并缺 blob 或上下文漂移后，在 `modified_files[]` 允许范围内执行最小等价手工写入；受控手工写入本身不得作为失败原因。
8. 裁决 Patch抓取 阶段时，必须实际读取 `02_patch_fetch.json` 中 `patch_files[]` 指向的本地 `.patch/.diff` 文件内容；只有存在标准 diff 信号的文件才算 patch 已抓取成功。HTML 错误页、JSON metadata、空文件或 HTTP/Gerrit/Gitiles 错误响应必须作为阻塞问题列入 `issues`。
