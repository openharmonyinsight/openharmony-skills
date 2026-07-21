# ODK MS Delta-Design

Use when MatrixSpec is installed AND the user wants /matspec.delta-design (delta format) for design.md. Falls back to odk-design if unavailable.

## Purpose

Invoke MatrixSpec `/matspec.delta-design` for design delta generation. Redirect output to ODK archive format in `.codespec/changes/<id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `.codespec/changes/<id>/spec.md` must exist (run `{{CMD_PREFIX}}ms-delta-spec` first).
- If MatrixSpec is unavailable, use the fallback chain declared in `adapters/matrixspec.yaml` and clearly report the degradation.

## Steps

1. Invoke MatrixSpec `/matspec.delta-design` for design generation (background, decisions, data model, interfaces, flows, risks).
2. When MatrixSpec tries to write to `matspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per active mode:
   - strict: Transform to ODK design template at `{{ODK_ASSET_ROOT}}/templates/ai/design.md` format. Add module impact table, verification approach section; inherit `odk-design` security trigger (proposal 安全/权限=是 → expand 安全基础检查, high-risk → `threat-model.md`).
   - passthrough: Copy to `.codespec/changes/<id>/design.md` unchanged.
   - merge: Use MatrixSpec format, append ODK verification approach section.
4. Confirm with user.

## Output

- Written to `.codespec/changes/<id>/design.md`
- Report any fields needing human approval
