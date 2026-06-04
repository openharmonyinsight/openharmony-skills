---
name: arkweb-security-patch-review
description: Review merged ArkWeb security patches for correctness, vulnerability coverage, and regression risk.
descriptionZH: ArkWeb 代码审查技能。审查给定 patch 是否已经真实合入。
tags: [ArkWeb, review, security]
---

# ArkWeb Security Review

用于 `arkweb-security-patch-reviewer` 和 `arkweb-security-patch-judge`。

审查阻塞边界、手工改写是否可放行、非 active issue 如何处理，先读本 skill 内的 [references/patch-landing-review-contract.md](references/patch-landing-review-contract.md)。不要引用其它 skill 的脚本或 md。

## 审查重点

1. active batch 中给定 patch 是否已经真实合入到当前工程目标 git 子仓。
2. 最终变更是否覆盖给定 patch 的目标修改文件和关键 diff 语义。
3. 是否存在未解冲突、空 diff、合错仓/合错文件、范围外改动或明显遗漏关键 hunk 的情况。
4. 手工改写是否仍在 `modified_files[]` 或合入报告允许范围内。

## 阻塞边界

代码审查阶段只裁决 active batch 中“给定 patch 是否合入”。以下情况才能作为阻塞问题：

- 给定 patch 未应用，或最终 diff 为空。
- 关键 hunk、关键文件或关键语义缺失。
- 改动越过 `modified_files[]` 或合入报告允许范围。
- 合错仓、合错文件，或目标子仓不匹配。
- 存在未解决冲突。

以下情况不是本阶段问题，不得作为阻塞或 `fail` 原因：

- `git apply` 因上下文漂移失败后，在 `modified_files[]` 范围内完成最小手工改写。
- 手工改写带来的语义漂移担忧，但没有具体证据证明给定 patch 的关键语义缺失。
- 尚未进入编译阶段导致的编译或运行证据缺失。

如果要判阻塞，必须直接指向“给定 patch 没有合入”的证据，例如缺失的 hunk、缺失的关键文件、未解冲突或合入到错误仓库。

批量模式中，`terminal_failed` 和 `deferred_for_archive` issue 已经退出 active batch。代码审查只能在总览中把它们列为归档/遗留项，不能计入 `blocked_issues`，不能输出需要回到「冲突解决」的 issues，也不能因为这些 issue 让整批 fail。只要 `pending_current_stage` 为空且仍有 `ready_for_next` issue，审查裁决必须放行 ready 批次进入「编译验证」。

## 审查范围硬性限制

- 只审查本次 patch 实际修改的文件，文件列表应来自合入报告、冲突解决报告、编译修复报告或明确的本次 patch diff。
- 审查前必须读取自动合入阶段输出的 `06_merge_result.md`；批量模式还必须逐个 issue 读取 `issues/{issue_id}/06_merge_result.md`。自动合入 `pass` 后这些文件应当已经存在；如果缺失，必须标记为 `artifact_missing:06_merge_result`，不能假设 patch 已合入。
- 批量模式必须逐个 issue 审查，读取 `issues/{issue_id}/06_merge_result.md`、`issues/{issue_id}/07_conflict_resolution.md`、`issues/{issue_id}/10_build_fix.md` 和当前工程目标子仓中属于该 issue 的 git diff。
- 批量模式禁止使用 git worktree；不同 issue 的改动、风险和结论不得混写。
- 工作区里的其它历史脏改、未跟踪文件、SDK、toolchain、构建产物、`src/out`、`.ace-outputs` 和无关删除必须忽略。
- 不得因为无关脏改给出 fail，不得要求清理无关文件，不得把无关脏改加入本次修复建议。
- 如果无法确认某个文件是否属于本次 patch，必须把它列为“待确认”，不能默认纳入审查范围。

## 输出

单 issue 模式审查步骤写入 `.ace-outputs/{runId}/08_code_review.md`。

批量模式每个 active issue 写入 `.ace-outputs/{runId}/issues/{issue_id}/08_code_review.md`，总览写入 `.ace-outputs/{runId}/08_code_review.md`。总览只能汇总，不得替代每个 active issue 的独立审查结论。非 active 的 `terminal_failed` / `deferred_for_archive` issue 只列入归档清单。

## 稳定脚本优先

优先使用内置脚本生成代码审查产物，不要在运行时拼接临时 Python/Node/Shell 脚本：

```bash
python3 skills/arkweb-security-patch-review/scripts/generate_code_review.py \
  --run-root <context.projectRoot>/.ace-outputs/<runId>
```

脚本会读取 `batch_status.json`、`06_merge_result.json` 和 `issues/{issue_id}/06_merge_result.json`，为每个 active issue 写入 `issues/{issue_id}/08_code_review.md`，并写入根级 `08_code_review.md` 和 `08_code_review.json`。脚本只聚合 active/ready/pending issue；`terminal_failed` 和 `deferred_for_archive` 只进入归档清单，不参与 `verdict`。

脚本执行后，agent 回复只允许包含：

- 一句结果摘要；
- 产物路径；
- 最后一个完整 JSON 代码块。

不要在回复中粘贴脚本源码、完整工具输出、大段 `06_merge_result` 内容或完整 diff。详细证据只写入 `08_code_review.md/json`。

审查步骤和裁决步骤都必须在回复末尾输出最后一个完整 JSON 代码块。不要输出只有 `remaining_issues` 的半截 JSON；`next_state` 和 `issues` 不能省略。

```json
{
  "verdict": "pass|fail",
  "next_state": "编译验证|冲突解决",
  "issues": [],
  "summary": "一句话总结"
}
```

JSON 判定规则：

- active batch 无阻塞、`pending_current_stage=[]` 且存在 `ready_for_next` issue 时，输出 `verdict=pass`、`next_state=编译验证`、`issues=[]`。
- 只有 active batch 中存在给定 patch 未真实合入且需要回到最小手工写入的证据时，输出 `verdict=fail`、`next_state=冲突解决`，并在 `issues[]` 中列出具体 active issue 阻塞证据。
- `terminal_failed` / `deferred_for_archive` issue 只能写入归档清单，不得写入 JSON `issues[]`，不得影响 `verdict`。
