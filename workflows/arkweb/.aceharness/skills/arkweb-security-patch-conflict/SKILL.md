---
name: arkweb-security-patch-conflict
description: Resolve ArkWeb patch merge conflicts while preserving upstream security fix intent.
descriptionZH: ArkWeb 冲突解决技能。git apply 失败或上下文漂移后，在允许文件范围内执行最小等价手工写入，并保持上游安全修复语义一致。
tags: [ArkWeb, conflict, merge]
---

# ArkWeb Conflict Resolution

用于 `arkweb-security-patch-conflict-resolver`。

遇到手工落地、`manual_attempted` / `manual_applied`、旧 blocker 清理和 issue 过滤 diff 裁决时，先读本 skill 内的 [references/manual-landing-contract.md](references/manual-landing-contract.md)。不要引用其它 skill 的脚本或 md。

## 输出

单 issue 模式写入 `.ace-outputs/{runId}/07_conflict_resolution.md`。

批量模式必须逐个 issue 处理，读取 `.ace-outputs/{runId}/issues/{issue_id}/06_merge_result.md/json` 中记录的目标子仓、`patch_normalization[]`、`modified_files[]` 和 blockers，并在当前工程目标 git 子仓内执行最小等价手工写入；每个 issue 写入 `.ace-outputs/{runId}/issues/{issue_id}/07_conflict_resolution.md`，总览写入 `.ace-outputs/{runId}/07_conflict_resolution.md`。

必须包含：

1. apply 失败/冲突文件和根因。
2. 上游修复意图。
3. ArkWeb 本地差异和适配决策。
4. 最小等价手工写入方案。
5. 与上游 patch 的偏差说明。

## 规则

- 先理解安全修复意图，再改代码。
- 本工作流里的“冲突解决”就是最小手工写入：读取规范化 patch hunks 和当前目标文件，在 `modified_files[]` 范围内做最小等价改动。
- 对 `patch does not apply`、三方合并缺 blob、上下文漂移和空 diff，不能只复述 git apply 失败；必须尝试最小手工写入，除非能证明不可在允许范围内完成。
- 若未执行手工写入，必须写明 `manual_attempted=false` 和 `manual_skip_reason`。
- 手工写入成功后必须写回 `manual_attempted=true`、`manual_rewrite=true`、最终变更文件、关键语义对应关系，并清除旧的 `patch_apply_failed:*`、`no_real_file_change`；旧 `worktree_add_failed` 只作为历史失败记录，不参与当前裁决。
- 手工修复成功就是合入成功：只要最小手工写入真实落地了上游 patch 的安全/功能语义，并且按 issue 过滤后的 diff 包含允许文件，就必须写回 `manual_applied=true`、`semantic_landed=true`，清空当前合入 blocker，并允许该 issue 进入 `ready_for_next`。
- 不能把“尝试过手工”误当成成功。若进入过手工路径但没有实际写入 issue 允许文件，或语义无法确认，必须写 `manual_attempted=true`、`manual_applied=false`，保留最新 blocker，不能进入 `ready_for_next`。
- `final_changed_files` 必须只列出当前 issue 的允许文件和已登记本地适配文件。全局 worktree diff 只能作为诊断输入，不能原样写入该 issue 的结果。
- 只允许修改上游 patch 明确涉及的冲突文件，以及合入/适配报告中明确列出的本次 patch 必需文件。
- 工程中其它未提交代码、未跟踪文件、历史脏改、构建产物和无关删除必须忽略。
- 批量模式禁止使用 git worktree；必须在当前工程目标子仓解决冲突。
- 如果多个 issue 修改同一文件，自动合入阶段应先按 issue_id 数值升序选择最小 issue_id 作为 winner 进入 active batch，其它 issue 标记 `duplicate_file_overlap` 和 `deferred_for_archive`；非 winner issue 不进入冲突解决。不得把非 winner 的重叠文件强行写入 winner issue 的结果。
- 不得清理、暂存、格式化、重写或顺手修复本次 patch 范围外的任何文件。
- 如果冲突需要改动范围外文件才能继续，停止并输出阻塞项，不得自动扩大处理范围。
- 无法确认语义时，不要强行通过，输出阻塞项。
- 批量模式每轮必须记录本轮前后的 fail/pass/blocker 变化和 final diff 变化；如果没有任何 issue 的 blocker 减少、`manual_attempted` 状态变化或 diff 变化，必须输出 `no_progress` 并停止继续空转。
