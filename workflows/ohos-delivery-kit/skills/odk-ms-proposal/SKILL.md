# ODK MS Proposal

Use when MatrixSpec is installed AND the user wants /matspec.proposal to drive proposal.md. Falls back to odk-propose if unavailable.

## Purpose

Invoke MatrixSpec `/matspec.proposal` for requirement clarification. Redirect output to ODK archive format in `.codespec/changes/<id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `.codespec/changes/<id>/` skeleton must exist (run `{{CMD_PREFIX}}init` first).
- If MatrixSpec is unavailable, use the fallback chain declared in `adapters/matrixspec.yaml` and clearly report the degradation.

## Steps

1. Invoke MatrixSpec `/matspec.proposal` for requirement clarification and proposal generation.
2. When MatrixSpec tries to write to `matspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per active mode:
   - strict: Transform to ODK proposal template at `{{PLUGIN_ROOT}}/templates/ai/proposal.md` format. Ensure ODK-required fields: target_release frontmatter, non-goals, 8-dimension N/A table, success criteria.
   - passthrough: Copy to `.codespec/changes/<id>/proposal.md` unchanged.
   - merge: Use MatrixSpec format, append ODK 8-dimension N/A table and target_release.
4. Confirm with user.

## Output

- Written to `.codespec/changes/<id>/proposal.md`
- Report any fields needing human approval
