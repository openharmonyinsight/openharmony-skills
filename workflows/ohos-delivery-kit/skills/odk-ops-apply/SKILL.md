---
name: odk-ops-apply
description: "Use when OpenSpec is installed AND the user wants /opsx:apply to implement tasks and backfill execution-plan code scope. Falls back to odk-implement if unavailable."
license: MIT
---

# ODK OPS Apply

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

## Native OpenSpec state

<!-- ODK:reference contracts/skill-guides/router/openspec-state.md -->
Read `contracts/skill-guides/router/openspec-state.md` before invoking OpenSpec.
Keep the native workspace and task file authoritative; capture native CLI state
and reconcile existing ODK artifacts without replacing either side.
<!-- /ODK:reference -->

## Purpose

Invoke OpenSpec `/opsx:apply` to implement tasks from the execution plan, apply code changes, and backfill execution-plan 代码范围映射.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `spec.md` and `execution-plan.md` must exist in `codespec/changes/<repo-name>/<proposal-id>/`.
- `execution-plan.md` must be approved by the user — do NOT implement before plan approval. If the plan is not yet approved, stop and ask the user to review and approve it first.
- If OpenSpec is unavailable, use the fallback chain declared in `adapters/openspec.yaml` and clearly report the degradation.
- If proposal.md `API/SDK` = 「是」, a valid the applicable API metadata files and Task-1 declaration-generation task must exist. Do not implement API changes from `spec.md` Markdown or OpenSpec delta text.

## Confirm the build product before invoking the bridge

First apply the host-only exception in the delivery-level and product guides.
Target builds require the build-name menu. Runtime target confirmation and firmware preparation are conditional on the explicit validation scope; build-only requires neither.

<!-- ODK:reference contracts/skill-guides/delivery/build-products.md -->
Read `contracts/skill-guides/delivery/build-products.md`. Before invoking
opsx:apply, verify the plan's actual product choice and `产品选择确认`. Recover
a real prior user answer or ask once when confirmation is missing, including
old plans. A configured default or a generated command does not confirm it.
<!-- /ODK:reference -->

Also reconcile `验证范围`, `验证产品` and `验证目标确认` before native runtime steps.
Do not infer device identity from a concrete or abstract build name. Apply
`odk-implement`'s scope-specific emulator/device preparation, artifact provenance,
target compatibility and selected-device/overwrite confirmation rules to native
Task completion criteria. Build-only runs no runtime preparation. Re-resolve
commands and invalidate affected evidence on build/target/device changes.

## Steps

<!-- ODK:reference contracts/skill-guides/delivery/implementation-quality.md -->
Read `contracts/skill-guides/delivery/implementation-quality.md` before invoking
apply and include its quality check in native code-Task completion criteria.
Self-review the actual diff before accepting completion, and follow the guide's
role boundaries for delegated work and configured final review. If a finding
requires a repair, reopen/correct the native task through the feedback procedure,
rerun affected checks and review the fix, recapture native state and then
reconcile ODK; do not invent an independent Done state.
<!-- /ODK:reference -->

1. Invoke OpenSpec `/opsx:apply` to implement its native tracked tasks. Include `odk-task-review` in completion criteria for each mapped ODK Task: run it after that Task's verification and before accepting completion or advancing to the next ODK Task. Supply the Task baseline/current diff, AC/decision locations and verification paths. Apply `contracts/skill-guides/delivery/task-review.md`, including actual risk escalation and the existing evidence layout. On a blocking verdict, keep/reopen the mapped native tasks as pending through the feedback procedure; do not keep an independent ODK Done state. Read/revise native targets in place and refresh native instructions after task completion. Capture the native state again before reconciling ODK.
2. If `API/SDK=是`, ensure Task-1 is the declaration-generation task and execute it first exactly as `odk-implement`: read the applicable API metadata files, generate `.d.ts` / `.d.ets` / `.h`, and archive the en/zh declaration diffs. Do not infer API facts from Markdown or OpenSpec delta text.
3. Read the existing ODK plan, reconcile task_map against native tasks, and backfill `execution-plan.md` 代码范围映射 with actual files modified or created.
4. Synchronize `execution-plan.md` progress from the native tasks and actual verification evidence, including per-row Final Status. Follow `contracts/skill-guides/delivery/feedback.md` for findings: correct/reopen native tasks or delta artifacts first, then reconcile ODK backfill and dispositions. Keep blocked tasks pending; do not maintain an independent completion state.
5. Verify AC-Task traceability: every AC's required tasks are complete and verification passes. Tasks link to ACs, or use a justified N/A for document/infrastructure work that does not close an AC.
6. Only after native state is `all_done` and the ODK projection is reconciled, automatically follow the handoff below; do not require separate review/validate commands from the user.

## Output

<!-- ODK:reference contracts/skill-guides/delivery/handoff.md -->
When implementation is complete, read and follow `contracts/skill-guides/delivery/handoff.md`: automatically review and validate, remind and wait for the user to trigger source PR submission, prepare `metadata_tracking.yaml` from the actual PR, then ask separately about design-docs. No automatic merge.
<!-- /ODK:reference -->

- Code changes applied to the codebase.
- `execution-plan.md` 代码范围映射 updated with actual implementation files.
- Task progress recorded in `execution-plan.md`.
- GitCode design-docs reminder with the developer-provided `design_docs_repository` address or “待开发者填写”.
