# ODK OPS Apply

Use when OpenSpec is installed AND the user wants /opsx:apply to implement tasks and backfill execution-plan code scope. Falls back to odk-implement if unavailable.

## Purpose

Invoke OpenSpec `/opsx:apply` to implement tasks from the execution plan, apply code changes, and backfill execution-plan 代码范围映射.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `spec.md` and `execution-plan.md` must exist in `.codespec/changes/<id>/`.
- If OpenSpec is unavailable, use the fallback chain declared in `adapters/openspec.yaml` and clearly report the degradation.

## Steps

1. Invoke OpenSpec `/opsx:apply` to implement tasks from the execution plan.
2. After code generation, backfill `execution-plan.md` 代码范围映射 with actual files modified or created.
3. Update `execution-plan.md` task checkboxes as tasks complete.
4. Verify AC-Task traceability: every AC has at least one completed task, every task links back to an AC.

## Output

- Code changes applied to the codebase.
- `execution-plan.md` 代码范围映射 updated with actual implementation files.
- Task progress recorded in `execution-plan.md`.
