---
name: odk-ms-validation
description: "Use when MatrixSpec is installed AND the user wants /matspec.validation to produce ODK review evidence. Falls back to odk-review if unavailable."
license: MIT
---

# ODK MS Validation

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

Invoke MatrixSpec `/matspec.validation` for validation execution. Redirect output to ODK archive format in `codespec/changes/<repo-name>/<proposal-id>/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- `codespec/changes/<repo-name>/<proposal-id>/execution-plan.md` must exist (run `{{CMD_PREFIX}}ms-tasks` first).
- If MatrixSpec is unavailable, use the fallback chain declared in `adapters/matrixspec.yaml` and clearly report the degradation.

## Steps

<!-- ODK:reference contracts/skill-guides/delivery/feedback.md -->
Read `contracts/skill-guides/delivery/feedback.md`. In every output mode, record
findings in the existing plan, identify owning artifacts, invalidate affected
results and return required backfill/reverification to the coordinator. A native
validation report alone does not close an ODK baseline deviation.
<!-- /ODK:reference -->

For configuration-dependent steps, use the effective-configuration command defined in `using-odk`; do not merge installation files independently. Stop on config errors. Existing execution-plan commands remain authoritative until explicitly changed.

1. Invoke MatrixSpec `/matspec.validation` for 6-dimension validation execution.
2. When MatrixSpec tries to write to `matspec/changes/`, apply `using-odk-bridge` Output Redirection Rules instead.
3. Process output per active mode:
   - strict: Transform to ODK review format. Add ODK consistency check dimension (spec-compliance, code-quality, verification mapping). Write validation results as evidence to `codespec/changes/<repo-name>/<proposal-id>/evidence/reviews/`.
   - passthrough: Copy to `codespec/changes/<repo-name>/<proposal-id>/validation.md` unchanged.
   - merge: Use MatrixSpec 6-dimension format, append ODK consistency check dimension.
4. Return PASS or actionable finding IDs with backfill/reverification status. A report approval is not needed to run checks; unresolved material scope/design decisions remain open for the user.
5. If the next action is a GitCode commit, push, or PR, resolve the design-docs repository address (priority: `codespec/profile.yaml` if present → `odk_config_ext.yaml` → `odk_config.yaml`; do not warn if `codespec/profile.yaml` is absent) and remind the user to submit `codespec/` documents to that separate design-docs repository. If no address can be resolved, report “待开发者填写”; never guess or automatically push across repositories. Actual submission uses `odk-submit-design-docs` to generate `metadata_tracking.yaml` and validate the five-base-file bundle plus required conditional evidence.

## Output

- Written to `codespec/changes/<repo-name>/<proposal-id>/validation.md` and `codespec/changes/<repo-name>/<proposal-id>/evidence/reviews/`
- Report any findings requiring human attention
- Include the GitCode design-docs reminder and developer-provided `design_docs_repository` address or “待开发者填写”
