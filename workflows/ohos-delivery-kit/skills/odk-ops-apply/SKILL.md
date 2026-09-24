---
name: odk-ops-apply
description: "Use when OpenSpec is installed AND the user wants /opsx:apply to implement tasks and backfill execution-plan code scope. Falls back to odk-implement if unavailable."
license: MIT
---

# ODK OPS Apply

## Purpose

Invoke OpenSpec `/opsx:apply` to implement tasks from the execution plan, apply code changes, and backfill execution-plan 代码范围映射.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `spec.md` and `execution-plan.md` must exist in `codespec/changes/<repo-name>/<proposal-id>/`.
- `execution-plan.md` must be approved by the user — do NOT implement before plan approval. If the plan is not yet approved, stop and ask the user to review and approve it first.
- If OpenSpec is unavailable, use the fallback chain declared in `adapters/openspec.yaml` and clearly report the degradation.

## Steps

1. Invoke OpenSpec `/opsx:apply` to implement tasks from the execution plan.
2. After code generation, backfill `execution-plan.md` 代码范围映射 with actual files modified or created.
3. Update `execution-plan.md` task checkboxes as tasks complete.
4. Verify AC-Task traceability: every AC has at least one completed task, every task links back to an AC.
5. After all Tasks are Done, automatically follow the handoff below; do not require separate review/validate commands from the user.

## Output

<!-- ODK:reference contracts/skill-guides/delivery/handoff.md -->
When implementation is complete, read and follow `{{ASSET_ROOT}}/contracts/skill-guides/delivery/handoff.md`: automatically review and validate, remind and wait for the user to trigger source PR submission, prepare metadata from the actual PR, then ask separately about design-docs. No automatic merge.
<!-- /ODK:reference -->

- Code changes applied to the codebase.
- `execution-plan.md` 代码范围映射 updated with actual implementation files.
- Task progress recorded in `execution-plan.md`.
- GitCode design-docs reminder with the developer-provided `design_docs_repository` address or “待开发者填写”.
