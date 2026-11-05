---
name: odk-sp-implement
description: "Use when Superpowers is installed AND the user wants TDD 失败/通过循环（Red/Green）+ subagent 驱动执行的 execution-plan.md。ODK 保持可追溯性；Superpowers 执行失败/通过循环。 Falls back to odk-implement if unavailable."
license: MIT
---

# ODK SP Implement

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and use the effective
contract. It takes precedence over standard-only artifact lists below; native
OpenSpec schemas remain standard/critical and lite uses the base flow.
<!-- /ODK:reference -->

## Purpose

Use after `execution-plan.md` has been approved and the user wants implementation to begin. ODK keeps traceability; Superpowers performs the TDD and subagent-driven implementation.

## Prerequisites

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `spec.md` exists with numbered ACs.
- `execution-plan.md` exists with Task IDs, AC-Task traceability, file-level scope, and verification commands.
- The user has approved implementation.
- If Superpowers skills are unavailable, use the fallback chain declared in `adapters/superpowers.yaml` and clearly report the degradation.

## Confirm the build product before execution

First apply the host-only exception in the delivery-level and product guides.
Only target-build/device plans require the menu and firmware selection below.

<!-- ODK:reference contracts/skill-guides/delivery/build-products.md -->
Read `contracts/skill-guides/delivery/build-products.md` before delegating any
Task. Reuse the approved plan's actual product choice and `产品选择确认`; if
that evidence is absent, recover a real prior user answer or ask once before
compilation. A configured default or a generated command does not confirm it.
<!-- /ODK:reference -->

## Steps

<!-- ODK:reference contracts/skill-guides/delivery/feedback.md -->
Read `contracts/skill-guides/delivery/feedback.md`. Apply the same finding
disposition, owning-artifact backfill and invalidation/reverification contract
to delegated Tasks. Record current Verification Final Status with Actual Result.
<!-- /ODK:reference -->

Before an applicable, explicitly confirmed device flash invokes `device_flash_skill`, read `contracts/skill-guides/router/configured-skills.md`; install it from matching config comment links if missing in the current agent, verify availability, then resume. Apply the same product, daily-strategy, selected-device and overwrite-confirmation conditions as `odk-implement`; pending installation blocks device preparation.

0. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list and list all Tasks as an explicit inventory before starting implementation. All task types — code modification, test writing, configuration update, and verification — are equally mandatory. No task type may be skipped without explicit user consent.
1. Read the active `codespec/changes/<repo-name>/<proposal-id>/spec.md` AC list and `execution-plan.md` 代码范围映射.
2. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list, file scope, and each Task's「任务间接口」（Produces/Consumes）—align cross-task naming and signatures to it.
3. Invoke Superpowers `test-driven-development` before editing implementation code.
4. Execute the approved Task list using Superpowers `subagent-driven-development` when available; otherwise use `executing-plans`.
5. For each Task:
   - Write or update failing tests first.
   - Run the targeted verification command and confirm the expected failure.
   - Implement the minimal code required for the Task.
   - Run the targeted verification command and confirm it passes. For the build and test steps, read the `## 构建与验证环境` table from `execution-plan.md` — use the Task's `验证命令` field to determine whether to build, start the emulator (arm64_virt only), and run tests, exactly as `odk-implement` does. Reuse the product explicitly confirmed during planning; missing confirmation must be resolved before the first build. Reuse that choice for subsequent Tasks unless the user requests a switch; if it changes, re-resolve it in the table and remaining Task commands and clear the emulator command when switching away from arm64_virt. Daily flash via `device_flash_skill` only applies when the confirmed product is `rk3568` — skip for all other products including arm64_virt.
   - Keep changes within the Task file scope unless the user approves an execution-plan update.
   - Backfill the Task's `Actual Result` and anti-fake completion evidence in `execution-plan.md`.
   - Mark the Task as completed in `execution-plan.md`: change all `- [ ]` checkboxes to `- [x]` in the Task's Steps section. If the Task list table has a `状态` column, update it to `Done`; otherwise add the column first.
6. After all Tasks are attempted, produce an **Execution Summary**:
   - List every Task with status: ✅ 已完成（Done） / ❌ 阻塞（Blocked） / ⚠️ 跳过（Skipped，附原因）
   - If any Task is incomplete, inform the user and do NOT suggest moving to review — wait for user direction
7. After implementation, update `execution-plan.md` 代码范围映射 and AC-Task 验证状态 with actual files, tests, and commit references.
8. Route missing ACs, design deviations and changed verification assumptions through the feedback procedure; update affected original artifacts before claiming closure. Resolve only new scope/design decisions not already authorized with the user.
9. After all Tasks are Done, automatically follow the handoff below; do not require separate review/validate commands from the user.

## Output

<!-- ODK:reference contracts/skill-guides/delivery/handoff.md -->
When implementation is complete, read and follow `contracts/skill-guides/delivery/handoff.md`: automatically review and validate using the skills listed in `pre_commit_reviews` (config), remind and wait for the user to trigger source PR submission, prepare `metadata_tracking.yaml` from the actual PR, invoke any `post_commit_reviews` skills after PR URL is confirmed, then ask separately about design-docs. No automatic merge.
<!-- /ODK:reference -->

Report:

- **Execution Summary:** every Task listed with status (✅ Done / ❌ Blocked / ⚠️ Skipped) and reason for any incomplete Tasks
- Tasks completed and status changes written to `execution-plan.md`
- Tests or verification commands run
- Code mapping rows updated in `execution-plan.md` 代码范围映射
- Any deviations from `execution-plan.md`
- GitCode design-docs reminder with the developer-provided `design_docs_repository` address or “待开发者填写”

If any Task is incomplete, report the gaps and stop; do not start the automatic handoff.
