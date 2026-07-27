---
name: odk-review
description: "Use when generating ODK review evidence (spec-compliance, code-quality, verification) from templates after implementation. Default standalone, zero plugin dependencies."
license: MIT
---

# ODK Review

## Prerequisites

- `spec.md` with AC list
- `execution-plan.md` with Task list and code scope
- Implementation code exists (committed)

## Input

1. Read `spec.md` AC list
2. Read `execution-plan.md` Task list and code scope
3. Read review templates from `{{ASSET_ROOT}}/templates/review/`

## Steps

1. Generate review documents from templates in `{{ASSET_ROOT}}/templates/review/`.

2. Backfill `execution-plan.md` 代码范围映射 with actual implementation files and update AC-Task 验证状态.

## Output

Write optional process evidence to `.codespec/changes/<id>/evidence/reviews/`.

Do not generate `reviews/` or `gates/` in the minimal archive root by default. These records are process evidence, not formal archive artifacts.

Confirm with the user that all ACs are covered and there are no unresolved deviations.

Suggest next step: run `{{CMD_PREFIX}}validate` to check archive readiness (Level A/B/C/D).
