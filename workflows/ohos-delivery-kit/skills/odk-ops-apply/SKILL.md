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

Once the scope is confirmed, apply the host-only exception in the delivery-level and product guides.
Target builds require the build-name menu. Runtime target confirmation and firmware preparation are conditional on the explicit validation scope; build-only requires neither.

<!-- ODK:reference contracts/skill-guides/delivery/build-products.md -->
Read `contracts/skill-guides/delivery/build-products.md`. Apply its implementation
scope preflight before invoking `opsx:apply`. Resolve missing or invalid scopes
in old plans and determine the commands required by the confirmed scope. For
target work, reuse the plan's actual `产品选择确认`; recover a real prior answer
or ask if it is missing. A configured default or generated command does not
confirm it. Apply command changes through native planning before updating the
ODK command snapshot.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/workflow-state.md -->
Before apply, read fresh native apply instructions for the selected change and
store. Use `task_map` and the native source locations to compare affected native
Task instructions with the confirmed scope and ODK verification commands. Pause
apply if an affected mapping is unresolved or a native command conflicts with
the confirmed scope or ODK command.

When a native verification command must change, update the authoritative
native task definition in place through OpenSpec planning and
reopen affected Tasks whose verification no longer applies. Refresh the native
capture and reconcile the ODK plan from it, updating the scope, commands and
verification status together and preserving historical evidence. Follow
`contracts/skill-guides/router/workflow-state.md` for normal planning and
reapproval after a native definition change. Resume apply only after approval
and a fresh check that the commands agree. Repeat this gate before the next
Task if the scope or commands change during implementation.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/delivery/device-verification.md -->
Reconcile the plan's verification scope, product and confirmation before invoking
apply. For `device` or `emulator`, read `contracts/skill-guides/delivery/device-verification.md`
and pass its scope-specific preparation, target binding, deployment and unverified-result
rules as native Task completion criteria. When a Task uses runtime Red, apply the
guide's baseline sequence before running Red and its rebuild and target reuse
sequence after the fix. Host-only and build-only skip runtime preparation.
<!-- /ODK:reference -->

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

0. List the approved execution plan's Tasks, then confirm and record the execution mode before invoking OpenSpec.

<!-- ODK:reference contracts/skill-guides/delivery/execution-mode.md -->
After listing the Tasks, apply the shared execution-mode selection and recording
procedure in `contracts/skill-guides/delivery/execution-mode.md` before executing or delegating the first Task.
<!-- /ODK:reference -->

1. Invoke OpenSpec `/opsx:apply` to implement its native tracked tasks. Include the mode-specific completion criteria for each mapped ODK Task. In 逐步实现 mode, after verification and self-review, apply actual risk escalation for R1/R2 and record `Task review: 不适用（逐步实现模式：免三席审查）` as a standalone Actual Result entry before accepting native completion. Skip Task reviewer dispatch and apply the existing-verdict checks if evidence already exists. R0 keeps its usual exemption. In the other modes, include `odk-task-review` in completion criteria: run it after that Task's verification and before accepting completion or advancing to the next ODK Task. Supply the Task baseline/current diff, AC/decision locations and verification paths. Apply `contracts/skill-guides/delivery/task-review.md`, including actual risk escalation and the existing evidence layout. On a blocking verdict, keep/reopen the mapped native tasks as pending through the feedback procedure; do not keep an independent ODK Done state. Read/revise native targets in place and refresh native instructions after task completion. Capture the native state again before reconciling ODK.
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
