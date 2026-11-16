---
name: odk-sp-review
description: "Use when Superpowers is installed AND the user wants requesting-code-review + verification-before-completion to produce ODK review evidence under evidence/reviews/. Falls back to odk-review if unavailable."
license: MIT
---

# ODK SP Review

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

Invoke Superpowers `requesting-code-review` and `verification-before-completion`. Persist results as ODK evidence to `evidence/reviews/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- Implementation code exists; include uncommitted and untracked relevant files in the review.
- `spec.md` with AC list.
- `execution-plan.md` with Task list and code scope.
- If Superpowers skills are unavailable, use the fallback chain declared in `adapters/superpowers.yaml` and clearly report the degradation.

## Steps

<!-- ODK:reference contracts/skill-guides/delivery/feedback.md -->
Read `contracts/skill-guides/delivery/feedback.md`. Review proposal/spec/design/plan
and actual code/evidence together; record findings in the existing plan, backfill
affected artifacts and reverify before returning PASS. Reports alone do not close
baseline deviations. Apply this in every bridge output mode.
<!-- /ODK:reference -->

For configuration-dependent steps, use the effective-configuration command defined in `using-odk`; do not merge installation files independently. Stop on config errors. Existing execution-plan commands remain authoritative until explicitly changed.

<!-- ODK:reference contracts/skill-guides/delivery/implementation-quality.md -->
Read `contracts/skill-guides/delivery/implementation-quality.md` and include its
decision criteria and role boundaries in the review brief. Reuse the native
reviewer; an assigned reviewer does not dispatch another. Give it requirements,
the full relevant diff, constraints and evidence by path. Require separate
spec-compliance and code-quality conclusions before accepting completion; assess
implementation choices before the author's preferred optimization. Route fixes
and scoped re-review through the coordinator instead of treating green tests or
a native deferred finding as closure of an ODK blocking issue.
<!-- /ODK:reference -->

1. Invoke Superpowers `requesting-code-review` with the actual diff and applicable delivery baseline; check missing ACs/design deviations as well as code correctness, tests and error paths.
2. Invoke Superpowers `verification-before-completion` before making any readiness claim.
3. Generate 3 review documents from templates in `templates/review/`, using the Superpowers review and verification results as the primary evidence:
   - **spec-compliance-YYYYMMDD.md** — Check every AC against implementation
   - **code-review-YYYYMMDD.md** — Code quality review; verify code scope matches execution-plan boundaries
   - **verification-YYYYMMDD.md** — Verification evidence; explicit code-vs-spec consistency conclusion
4. Persist to `codespec/changes/<repo-name>/<proposal-id>/evidence/reviews/`.
5. If the next action is a GitCode commit, push, or PR, resolve the design-docs repository address (priority: `codespec/profile.yaml` if present → `odk_config_ext.yaml` → `odk_config.yaml`; do not warn if `codespec/profile.yaml` is absent) and remind the user to submit `codespec/` documents to that separate design-docs repository. If no address can be resolved, report “待开发者填写”; never guess or automatically push across repositories. Actual submission uses `odk-submit-design-docs` to generate `metadata_tracking.yaml` and validate the five-base-file bundle plus required conditional evidence.

## Output

Written to `codespec/changes/<repo-name>/<proposal-id>/evidence/reviews/`. Confirm all ACs are covered with no unresolved deviations, and include the GitCode `design_docs_repository` reminder in the handoff.
