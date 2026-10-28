---
name: odk-ms-tasks
description: "Use when MatrixSpec is installed AND the user wants /matspec.tasks to drive execution-plan.md. Falls back to odk-plan if unavailable."
license: MIT
---

# ODK MS Tasks

## Purpose

Invoke MatrixSpec `/matspec.tasks` for task breakdown generation. Redirect output to ODK archive format in `codespec/changes/<repo-name>/<proposal-id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `codespec/changes/<repo-name>/<proposal-id>/design.md` must exist (run `{{CMD_PREFIX}}ms-delta-design` first).
- If MatrixSpec is unavailable, use the fallback chain declared in `adapters/matrixspec.yaml` and clearly report the degradation.

## Steps

1. Invoke MatrixSpec `/matspec.tasks` for layered task generation (Data -> Domain -> Application -> Infrastructure -> Interface -> Tests -> Docs -> Verification).
2. When MatrixSpec tries to write to `matspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per active mode:
   - strict: Transform to ODK execution-plan format at `runtime/assets/templates/ai/execution-plan.md`. Add AC-Task traceability table, code scope per task (file-level paths), completion criteria.
   - passthrough: Copy to `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` unchanged.
   - merge: Use MatrixSpec layered format, append AC-Task traceability table and code scope column.
4. Confirm with user.

Before writing `execution-plan.md`, apply `odk-plan`'s build-product and command resolution step (without replacing the active bridge's task decomposition).
<!-- ODK:reference contracts/skill-guides/delivery/device-version.md -->
Read `contracts/skill-guides/delivery/device-version.md` to skip daily selection for QEMU, ask daily versus existing for every other product, and persist the choice and preparation method in `## 构建与验证环境`. Preserve this environment section in every output mode.
<!-- /ODK:reference -->

## Output

- Written to `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md`
- Report any fields needing human approval
