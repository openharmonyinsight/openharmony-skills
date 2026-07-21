# ODK MS Tasks

Use when MatrixSpec is installed AND the user wants /matspec.tasks to drive execution-plan.md. Falls back to odk-plan if unavailable.

## Purpose

Invoke MatrixSpec `/matspec.tasks` for task breakdown generation. Redirect output to ODK archive format in `.codespec/changes/<id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `.codespec/changes/<id>/design.md` must exist (run `{{CMD_PREFIX}}ms-delta-design` first).
- If MatrixSpec is unavailable, use the fallback chain declared in `adapters/matrixspec.yaml` and clearly report the degradation.

## Steps

1. Invoke MatrixSpec `/matspec.tasks` for layered task generation (Data -> Domain -> Application -> Infrastructure -> Interface -> Tests -> Docs -> Verification).
2. When MatrixSpec tries to write to `matspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per active mode:
   - strict: Transform to ODK execution-plan format at `{{ODK_ASSET_ROOT}}/templates/ai/execution-plan.md`. Add AC-Task traceability table, code scope per task (file-level paths), completion criteria.
   - passthrough: Copy to `.codespec/changes/<id>/execution-plan.md` unchanged.
   - merge: Use MatrixSpec layered format, append AC-Task traceability table and code scope column.
4. Confirm with user.

## Output

- Written to `.codespec/changes/<id>/execution-plan.md`
- Report any fields needing human approval
