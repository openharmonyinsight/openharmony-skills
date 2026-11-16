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

## Phase flow and next step

<!-- ODK:reference contracts/skill-guides/router/phase-flow.md -->
Before phase work, read `contracts/skill-guides/router/phase-flow.md` and apply
its configured pre_hook/post_hook order. At every completion or pause, show
the next pending action and configured hooks; omit the reminder only when
the entire applicable workflow is complete. The coordinator owns this flow.
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
- If proposal.md `API/SDK` = 「是」, the applicable API metadata files exists and is valid, and the approved plan's Task-1 generates API declarations.
- The user has approved implementation.
- If Superpowers skills are unavailable, use the fallback chain declared in `adapters/superpowers.yaml` and clearly report the degradation.

## Confirm the build product before execution

First apply the host-only exception in the delivery-level and product guides.
Target builds require the build-name menu. Runtime target confirmation and firmware preparation are conditional on the explicit validation scope; build-only requires neither.

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

<!-- ODK:reference contracts/skill-guides/delivery/implementation-quality.md -->
Before delegating code Tasks, read `contracts/skill-guides/delivery/implementation-quality.md`
and include its quality check and role boundaries in the Task brief. Require
implementer self-review, then reuse the native task reviewer for separate
spec-compliance and code-quality conclusions before accepting completion. The
implementer does not dispatch its own reviewer; the coordinator owns assignment,
repairs and re-review. Refactor for a concrete reason, rerun affected tests and
backfill the existing Actual Result. Native deferred findings cannot waive ODK
blocking requirements. Leave whole-change review to the configured handoff;
do not add duplicate review seats. Without task delegation, use the guide's
inline self-review and final-review route and disclose the actual review mode.
<!-- /ODK:reference -->

Before an applicable, explicitly confirmed device flash invokes `device_flash_skill`, read `contracts/skill-guides/router/configured-skills.md`; install it from matching config comment links if missing in the current agent, verify availability, then resume. Apply `odk-implement`'s `验证范围=device`, `验证产品=rk3568`, configured-skill, daily-strategy, actual selected-device and overwrite-confirmation conditions; the build name is not a device identity. Pending installation blocks preparation.

0. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list and list all Tasks as an explicit inventory before starting implementation. All task types — code modification, test writing, configuration update, and verification — are equally mandatory. No task type may be skipped without explicit user consent.
1. Read the active `codespec/changes/<repo-name>/<proposal-id>/spec.md` AC list and `execution-plan.md` 代码范围映射.
2. Read `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` Task list, file scope, and each Task's「任务间接口」（Produces/Consumes）—align cross-task naming and signatures to it.
3. If `API/SDK=是`, execute Task-1 before implementation tasks: generate `.d.ts` / `.d.ets` / `.h` from the applicable API metadata files and archive the en/zh declaration diffs, exactly as `odk-implement` does.
4. Invoke Superpowers `test-driven-development` before editing implementation code.
5. Execute the approved Task list using Superpowers `subagent-driven-development` when available; otherwise use `executing-plans`. Adapt native task review to `odk-task-review` before any reviewer dispatch: R1 uses the single `all` role; R2 uses scope for spec compliance and arch/security for code quality, with exactly the fixed three seats. Project the native spec/quality conclusions from those verified reports instead of dispatching another native reviewer. R0 follows the ODK exemption. Scope native execution to implementation and its applicable task reviews; return control to ODK before native whole-branch review or branch finishing. The configured ODK handoff owns final whole-change review, validation and the separately authorized publishing flow.
6. For each Task:
   - Write or update failing tests first.
   - Run the targeted verification command and confirm the expected failure.
   - Implement the minimal code required for the Task.
   - Run targeted verification using the plan's separate `编译产品`, `验证范围`, `验证产品` and `验证目标确认`, following `odk-implement`'s a–d. Build names may be concrete or abstract and are also the directory name under out/. `build-only` never prepares a runtime; `emulator`/`device` use the separately confirmed validation target. Fill missing confirmations first. Re-resolve commands and invalidate affected evidence after switches. Locate artifacts from explicit directories or actual outputs under out/<编译产品>, verify target compatibility, and never substitute the validation product in output paths. Daily auto-flash requires validation product rk3568, a configured skill, selected-device and overwrite confirmation.
   - Keep changes within the Task file scope unless the user approves an execution-plan update.
   - Backfill the Task's `Actual Result` and anti-fake completion evidence in `execution-plan.md`.
   - Accept delegated code-Task completion only after the mapped task-review reports supply both required native conclusions and blocking findings are resolved. Self-review or an implementer's Done report alone is insufficient. After a fix, collect affected verification evidence and re-review the fix plus affected artifact diffs under the feedback procedure.
   - Before accepting the Task, invoke `odk-task-review` for the gate in `contracts/skill-guides/delivery/task-review.md`. Pass the Task's `风险等级`, full Task baseline/current diff including untracked files, related ACs/decisions and verification paths. The skill probes `python3 <executables>/lib/odk_host_capabilities.py --host <host>`, uses fixed arch/scope/security seats for R2 or one five-dimension seat for R1, and records the R0 reason without dispatch. Serial fallback writes `independent: false` in `evidence/reviews/task-<n>/verdict.md`. Update the Task-list risk cell and Actual Result on escalation; unresolved Critical/High marks the Task `❌ Blocked` and blocks the next Task. Use the skill's finding validation and bounded fix re-review. Native review conclusions remain input claims; do not dispatch duplicate seats if an existing reviewer can run the required ODK role on the same snapshot and return all required evidence.
   - Only after the applicable checks and review above pass, mark the Task as completed in `execution-plan.md`: change all `- [ ]` checkboxes to `- [x]` in the Task's Steps section. If the Task list table has a `状态` column, update it to `Done`; otherwise add the column first.
7. After all Tasks are attempted, produce an **Execution Summary**:
   - List every Task with status: ✅ 已完成（Done） / ❌ 阻塞（Blocked） / ⚠️ 跳过（Skipped，附原因）
   - If any Task is incomplete, inform the user and do NOT suggest moving to review — wait for user direction
8. After implementation, update `execution-plan.md` 代码范围映射 and AC-Task 验证状态 with actual files, tests, and commit references.
9. Route missing ACs, design deviations, changed scope, and changed verification assumptions through the feedback procedure; update affected original artifacts before claiming closure. Resolve only new scope/design decisions not already authorized with the user.
10. After all Tasks are Done, automatically follow the handoff below; do not require separate review/validate commands from the user.

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
