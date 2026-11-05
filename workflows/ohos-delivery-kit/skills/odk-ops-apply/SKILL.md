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

## Confirm the build product before invoking the bridge

First apply the host-only exception in the delivery-level and product guides.
Only target-build/device plans require the menu and firmware selection below.

<!-- ODK:reference contracts/skill-guides/delivery/build-products.md -->
Read `contracts/skill-guides/delivery/build-products.md`. Before invoking
opsx:apply, verify the plan's actual product choice and `产品选择确认`. Recover
a real prior user answer or ask once when confirmation is missing, including
old plans. A configured default or a generated command does not confirm it.
<!-- /ODK:reference -->

## Steps

1. Invoke OpenSpec `/opsx:apply` to implement its native tracked tasks. Read/revise native targets in place and refresh native instructions after task completion. Capture the native state again before reconciling ODK.
2. Read the existing ODK plan, reconcile task_map against native tasks, and backfill `execution-plan.md` 代码范围映射 with actual files modified or created.
3. Synchronize `execution-plan.md` progress from the native tasks and actual verification evidence, including per-row Final Status. Follow `contracts/skill-guides/delivery/feedback.md` for findings: correct/reopen native tasks or delta artifacts first, then reconcile ODK backfill and dispositions. Keep blocked tasks pending; do not maintain an independent completion state.
4. Verify AC-Task traceability: every AC's required tasks are complete and verification passes. Tasks link to ACs, or use a justified N/A for document/infrastructure work that does not close an AC.
5. Only after native state is `all_done` and the ODK projection is reconciled, automatically follow the handoff below; do not require separate review/validate commands from the user.

## Output

<!-- ODK:reference contracts/skill-guides/delivery/handoff.md -->
When implementation is complete, read and follow `contracts/skill-guides/delivery/handoff.md`: automatically review and validate, remind and wait for the user to trigger source PR submission, prepare `metadata_tracking.yaml` from the actual PR, then ask separately about design-docs. No automatic merge.
<!-- /ODK:reference -->

- Code changes applied to the codebase.
- `execution-plan.md` 代码范围映射 updated with actual implementation files.
- Task progress recorded in `execution-plan.md`.
- GitCode design-docs reminder with the developer-provided `design_docs_repository` address or “待开发者填写”.
