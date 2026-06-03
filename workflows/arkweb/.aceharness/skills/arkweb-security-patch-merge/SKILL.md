---
name: arkweb-security-patch-merge
description: Apply upstream Chromium patches into ArkWeb with deterministic patch normalization, batch planning, issue-scoped diff checks, and controlled manual merge fallback.
descriptionZH: ArkWeb 自动合入技能。优先使用脚本规范化 patch、规划批量 overlap、过滤 issue 级 diff；git apply 失败后在允许范围内执行最小手工写入，手工修复成功即成功。
tags: [ArkWeb, merge, patch, batch]
---

# ArkWeb Patch Merge

用于 `arkweb-security-patch-merge-engineer`。

## Core Flow

1. Resolve the ArkWeb project root from `context.codebase` / `context.automation.repoPath`. `context.projectRoot` is the lightweight workflow output root.
2. Resolve the input archive from `context.requirements`; keep it separate from the project root.
3. Normalize every patch before scanning or applying it.
4. In batch mode, generate the batch plan before applying any issue.
5. Determine the target git subrepo before `git apply`.
6. Try `git apply --check`, then `git apply` or `git apply --3way` as appropriate.
7. If apply fails because of context drift or missing blobs, enter conflict resolution: perform minimal manual writing inside the issue's allowed files.
8. Compute issue-scoped diff, validate `06_merge_result`, and only then mark stage status.

## Required Scripts

Prefer these scripts over hand-written ad hoc logic:

```bash
node skills/arkweb-security-patch-merge/scripts/normalize_patch.mjs <patch-file> --out <normalized-file>
node skills/arkweb-security-patch-merge/scripts/plan_batch.mjs --archive-dir <archive-run-dir> --project-root <context.codebase> --output-dir <context.projectRoot>/.ace-outputs/<runId>
node skills/arkweb-security-patch-merge/scripts/issue_diff_scope.mjs --repo <target-git-repo> --merge-result <issues/{issue_id}/06_merge_result.json>
node skills/arkweb-security-patch-merge/scripts/validate_merge_result.mjs <issues/{issue_id}/06_merge_result.json> --batch-status <batch_status.json> --issue-id <issue_id>
```

If a script reports invalid state, treat that as a blocker and fix the state/report before advancing.

## References

Read only the relevant reference for the task:

- Input/archive and base64 patch handling: `references/input-and-normalization.md`
- Batch overlap and stage status rules: `references/batch-state-contract.md`
- Manual merge success and issue-scoped diff rules: `references/patch-landing-contract.md`
- Build-fix deviation rules: `references/compile-adaptation-contract.md`
- Target git subrepo and manifest mapping: `references/target-subrepo-contract.md`

## Hard Rules

- Manual repair success is success: `manual_applied=true` or `semantic_landed=true` with empty blockers may advance.
- `manual_attempted=true` alone is not success.
- `final_changed_files[]` must be issue-scoped. Never copy global `git diff --name-status` into each issue.
- Do not edit, stage, clean, format, or submit files outside the current issue's allowed patch/adaptation scope.
- Overlap losers do not enter conflict resolution, build, or submit in the current batch.
- Compile fixes may differ from the upstream patch text only when recorded as issue-scoped local adaptations and the upstream semantics remain landed.

## Outputs

Single issue:

- `.ace-outputs/{runId}/06_merge_result.md`
- `.ace-outputs/{runId}/06_merge_result.json`

Batch:

- `.ace-outputs/{runId}/00_batch_plan.md/json`
- `.ace-outputs/{runId}/batch_status.md/json`
- `.ace-outputs/{runId}/issues/{issue_id}/06_merge_result.md/json`

Each issue result must include:

- `issue_id`
- `target_subrepo`
- `patch_normalization[]`
- `modified_files[]`
- `final_changed_files[]`
- `apply_ok`
- `manual_attempted`
- `manual_applied`
- `semantic_landed`
- `local_adaptations[]`
- `blockers[]`
- `stage_status`
