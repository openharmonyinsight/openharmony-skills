# ODK MS Validation

Use when MatrixSpec is installed AND the user wants /matspec.validation to produce ODK review evidence. Falls back to odk-review if unavailable.

## Purpose

Invoke MatrixSpec `/matspec.validation` for validation execution. Redirect output to ODK archive format in `.codespec/changes/<id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `.codespec/changes/<id>/execution-plan.md` must exist (run `{{CMD_PREFIX}}ms-tasks` first).
- If MatrixSpec is unavailable, use the fallback chain declared in `adapters/matrixspec.yaml` and clearly report the degradation.

## Steps

1. Invoke MatrixSpec `/matspec.validation` for 6-dimension validation execution.
2. When MatrixSpec tries to write to `matspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per active mode:
   - strict: Transform to ODK review format. Add ODK consistency check dimension (spec-compliance, code-quality, verification mapping). Write validation results as evidence to `.codespec/changes/<id>/evidence/reviews/`.
   - passthrough: Copy to `.codespec/changes/<id>/validation.md` unchanged.
   - merge: Use MatrixSpec 6-dimension format, append ODK consistency check dimension.
4. Confirm with user.

## Output

- Written to `.codespec/changes/<id>/validation.md` and `.codespec/changes/<id>/evidence/reviews/`
- Report any findings requiring human attention
