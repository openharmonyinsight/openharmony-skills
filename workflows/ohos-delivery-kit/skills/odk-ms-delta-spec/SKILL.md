---
name: odk-ms-delta-spec
description: "Use when MatrixSpec is installed AND the user wants /matspec.delta-spec (ADDED/MODIFIED/REMOVED delta) for spec.md. Falls back to odk-spec if unavailable."
license: MIT
---

# ODK MS Delta-Spec

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

## Purpose

Invoke MatrixSpec `/matspec.delta-spec` for spec delta generation. Redirect output to ODK archive format in `codespec/changes/<repo-name>/<proposal-id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `codespec/changes/<repo-name>/<proposal-id>/proposal.md` must exist (run `{{CMD_PREFIX}}ms-proposal` first).
- If MatrixSpec is unavailable, use the fallback chain declared in `adapters/matrixspec.yaml` and clearly report the degradation.

## Steps

1. Invoke MatrixSpec `/matspec.delta-spec` for delta-format spec generation (ADDED/MODIFIED/REMOVED).
2. When MatrixSpec tries to write to `matspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per active mode:
   - strict: Transform to ODK spec template at `templates/ai/spec.md` format. Add AC numbering (AC-X.Y per requirement), compatibility declaration, verification mapping.
   - passthrough: Copy to `codespec/changes/<repo-name>/<proposal-id>/spec.md` unchanged.
   - merge: Use MatrixSpec delta format, append ODK sections: AC numbering guidance, compatibility declaration, verification mapping.
4. Confirm with user.

## Output

- Written to `codespec/changes/<repo-name>/<proposal-id>/spec.md`
- Report any fields needing human approval
