# OpenHarmony C++ Skill Evals

Use [`evals.json`](evals.json) as the seed set for the first benchmark iteration.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-cpp-style-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-scaffold-base-class/`.
4. Save per-run outputs under `with_skill/outputs/` and `old_skill/outputs/` or `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate the iteration with the `skill-creator` benchmark script and generate the review viewer.

## Minimum success criteria

- At least one eval checks generated `.h/.cpp` scaffolding.
- At least one eval checks production implementation choices around ownership, member naming, and leaf-class semantics.
- At least one eval checks public API comment repair without unrelated signature churn.
- At least one eval checks review-mode findings.
- At least one eval checks that third-party or upstream code is treated as an exception boundary.
- At least one eval checks explicit validation requests and scoped bundled-tool guidance.
- At least one eval checks structured evaluation output.
- Assertions measure OpenHarmony-specific deltas instead of generic C++ quality.

## Current coverage map

- `0`: new inheritable class scaffold, file naming, include guards, API comments, base-class semantics.
- `1`: review findings for header hygiene, virtual defaults, lambda capture, and ownership style.
- `2`: production implementation with non-owning listener interfaces, deleted copy or move, `final`, member naming, and no generic abstraction.
- `3`: public API comment repair focused on behavior, ownership, lifetime, and return semantics.
- `4`: third-party boundary handling so OpenHarmony rules are not over-applied to imported code.
- `5`: explicit strict validation request, scoped formatting or clang-tidy guidance, and remaining manual checks.

See [`../references/evaluation-framework.md`](../references/evaluation-framework.md) for the grading and benchmark rules.
