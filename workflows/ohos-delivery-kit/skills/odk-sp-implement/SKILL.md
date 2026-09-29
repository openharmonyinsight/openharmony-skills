---
name: odk-sp-implement
description: "Use when Superpowers is installed AND the user wants TDD + subagent-driven execution of an approved execution-plan.md. ODK keeps traceability; Superpowers runs red/green cycles. Falls back to odk-implement if unavailable."
license: MIT
---

# ODK SP Implement

## Purpose

Use after `execution-plan.md` has been approved and the user wants implementation to begin. ODK keeps traceability; Superpowers performs the TDD and subagent-driven implementation.

## Prerequisites

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `spec.md` exists with numbered ACs.
- `execution-plan.md` exists with Task IDs, AC-Task traceability, file-level scope, and verification commands.
- The user has approved implementation.
- If Superpowers skills are unavailable, use the fallback chain declared in `adapters/superpowers.yaml` and clearly report the degradation.

## Steps

0. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list and list all Tasks as an explicit inventory before starting implementation. All task types — code modification, test writing, configuration update, and verification — are equally mandatory. No task type may be skipped without explicit user consent.
1. Read the active `codespec/changes/<repo-name>/<proposal-id>/spec.md` AC list and `execution-plan.md` 代码范围映射.
2. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list, file scope, and each Task's「任务间接口」（Produces/Consumes）—align cross-task naming and signatures to it.
3. Invoke Superpowers `test-driven-development` before editing implementation code.
4. Execute the approved Task list using Superpowers `subagent-driven-development` when available; otherwise use `executing-plans`.
5. For each Task:
   - Write or update failing tests first.
   - Run the targeted verification command and confirm the expected failure.
   - Implement the minimal code required for the Task.
   - Run the targeted verification command and confirm it passes.
   - Keep changes within the Task file scope unless the user approves an execution-plan update.
   - Backfill the Task's `Actual Result` and anti-fake completion evidence in `execution-plan.md`.
   - Mark the Task as completed in `execution-plan.md`: change all `- [ ]` checkboxes to `- [x]` in the Task's Steps section. If the Task list table has a `状态` column, update it to `Done`; otherwise add the column first.
6. After all Tasks are attempted, produce an **Execution Summary**:
   - List every Task with status: ✅ Done / ❌ Blocked / ⚠️ Skipped (with reason)
   - If any Task is incomplete, inform the user and do NOT suggest moving to review — wait for user direction
7. After implementation, update `execution-plan.md` 代码范围映射 and AC-Task 验证状态 with actual files, tests, and commit references.
8. If implementation reveals missing ACs or changed scope, pause and update `spec.md` / `execution-plan.md` before continuing.
9. After all Tasks are Done, automatically follow the handoff below; do not require separate review/validate commands from the user.

## Output

<!-- ODK:reference contracts/skill-guides/delivery/handoff.md -->
When implementation is complete, read and follow `{{ASSET_ROOT}}/contracts/skill-guides/delivery/handoff.md`: automatically review and validate, remind and wait for the user to trigger source PR submission, prepare metadata from the actual PR, then ask separately about design-docs. No automatic merge.
<!-- /ODK:reference -->

Report:

- **Execution Summary:** every Task listed with status (✅ Done / ❌ Blocked / ⚠️ Skipped) and reason for any incomplete Tasks
- Tasks completed and status changes written to `execution-plan.md`
- Tests or verification commands run
- Code mapping rows updated in `execution-plan.md` 代码范围映射
- Any deviations from `execution-plan.md`
- GitCode design-docs reminder with the developer-provided `design_docs_repository` address or “待开发者填写”

If any Task is incomplete, report the gaps and stop; do not start the automatic handoff.
