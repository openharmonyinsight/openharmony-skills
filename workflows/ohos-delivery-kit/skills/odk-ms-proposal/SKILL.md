---
name: odk-ms-proposal
description: "Use when MatrixSpec is installed AND the user wants /matspec.proposal to drive proposal.md. Falls back to odk-propose if unavailable."
license: MIT
---

# ODK MS Proposal

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

## Purpose

Invoke MatrixSpec `/matspec.proposal` for requirement clarification. Redirect output to ODK archive format in `codespec/changes/<repo-name>/<proposal-id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `codespec/changes/<repo-name>/<proposal-id>/` skeleton must exist (run `{{CMD_PREFIX}}init` first).
- If MatrixSpec is unavailable, use the fallback chain declared in `adapters/matrixspec.yaml` and clearly report the degradation.

## Steps

1. Invoke MatrixSpec `/matspec.proposal` for requirement clarification and proposal generation.
2. When MatrixSpec tries to write to `matspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per active mode:
   - strict: Transform to ODK proposal template at `templates/ai/proposal.md` format. Ensure ODK-required fields: target_release frontmatter, non-goals, `1+8 设备差异规格`, `外部依赖`, 8-dimension N/A table, success criteria.
   - passthrough: Copy to `codespec/changes/<repo-name>/<proposal-id>/proposal.md` unchanged.
   - merge: Use MatrixSpec format, append ODK `1+8 设备差异规格`, `外部依赖`, 8-dimension N/A table, and target_release.
4. Confirm with user.

## Output

- Written to `codespec/changes/<repo-name>/<proposal-id>/proposal.md`
- Report any fields needing human approval
