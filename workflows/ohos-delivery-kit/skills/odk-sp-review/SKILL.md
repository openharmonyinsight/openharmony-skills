
# ODK SP Review

Use when Superpowers is installed AND the user wants requesting-code-review + verification-before-completion to produce ODK review evidence under evidence/reviews/. Falls back to odk-review if unavailable.

## Purpose

Invoke Superpowers `requesting-code-review` and `verification-before-completion`. Persist results as ODK evidence to `evidence/reviews/`.

## Preconditions

- Load `using-odk` first.
- Load `using-odk-bridge` for output redirection and mode selection.
- Implementation code exists (committed).
- `spec.md` with AC list.
- `execution-plan.md` with Task list and code scope.
- If Superpowers skills are unavailable, use the fallback chain declared in `adapters/superpowers.yaml` and clearly report the degradation.

## Steps

1. Invoke Superpowers `requesting-code-review` to review the implementation against `spec.md` and `execution-plan.md`.
2. Invoke Superpowers `verification-before-completion` before making any readiness claim.
3. Generate 3 review documents from templates in `{{PLUGIN_ROOT}}/templates/review/`, using the Superpowers review and verification results as the primary evidence:
   - **spec-compliance-YYYYMMDD.md** — Check every AC against implementation
   - **code-review-YYYYMMDD.md** — Code quality review; verify code scope matches execution-plan boundaries
   - **verification-YYYYMMDD.md** — Verification evidence; explicit code-vs-spec consistency conclusion
4. Persist to `.codespec/changes/<id>/evidence/reviews/`.

## Output

Written to `.codespec/changes/<id>/evidence/reviews/`. Confirm all ACs are covered with no unresolved deviations.
