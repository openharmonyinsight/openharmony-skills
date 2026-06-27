# OpenHarmony Graphics Stability Code Review Skill Evals

Use [`evals.json`](evals.json) as the seed set for the first benchmark iteration.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-graphics-stability-code-review-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-full-scan-multi-category/`.
4. Save per-run outputs under `with_skill/outputs/` and `old_skill/outputs/` or `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate the iteration with the `skill-creator` benchmark script and generate the review viewer.

## Minimum success criteria

- At least one eval checks full-scan coverage across all 5 stability categories.
- At least one eval checks CRITICAL-severity boundary condition detection (Parcel data as loop condition / array subscript).
- At least one eval checks HIGH-severity resource management detection (fd leak, dlopen/dlclose, deserialization memory leak, JSON unclosed leak).
- At least one eval checks concurrency stability detection (global variable writes without locks in RenderNodeDrawable).
- At least one eval checks graphics stability detection (VulkanCleanupHelper reference counting, Surface/Image thread restrictions, SharedContext mixing, GPU Context on main thread, RSUniRenderThread restrictions).
- At least one eval checks exception handling detection (prohibited try/catch/throw, abnormal branch missing return/handling).
- At least one eval checks specified-rule-only scanning (user-specified rule IDs).
- At least one eval checks category-specific scanning (按分类扫描 prompt format).
- At least one eval checks severity-level filtering (only HIGH and CRITICAL rules).
- At least one eval checks whitelist filtering (test directory) and NOPROTECT annotation exclusion.
- At least one eval checks third-party code boundary handling (third_party/ path recognition).
- At least one eval checks report format compliance (REPORT_TEMPLATE.md and REPORT_TEMPLATE.csv format).
- At least one eval checks PROBLEM_TEMPLATE compliance (RiskFlow, ImpactAnalysis, fix suggestions per finding).
- At least one eval checks subagent parallel review mechanism (category-based organization in report).
- At least one eval checks type conversion and arithmetic overflow boundary conditions.
- Assertions measure stability-specific deltas (rule ID accuracy, severity correctness, risk flow analysis) instead of generic code review quality.

## Current coverage map

- `0`: full-scan multi-category review covering all 5 stability categories in a single code file, report output format compliance, subagent verification, negative case (FdGuard safe code).
- `1`: specified-rule-only scanning (BoundaryCondition_001 and BoundaryCondition_002), safe code exclusion, CRITICAL severity.
- `2`: graphics stability focus (VulkanCleanupHelper Ref(), RS main thread restrictions, GetBackendTexture thread limits, callback process restrictions, RSRenderNodeMap access), negative case (correct Ref() pattern).
- `3`: resource management focus (dlopen/dlclose, fd leak on error paths, socket fd leak, deserialization memory leak, JSON unclosed leak), negative case (FdGuard RAII).
- `4`: whitelist filtering (test directory) and NOPROTECT annotation exclusion, safe code recognition.
- `5`: third-party code boundary handling (third_party/ path), substantive risk reporting vs style enforcement, negative case (SafeConvert with range check).
- `6`: severity-level filtering (only CRITICAL and HIGH rules), MEDIUM rule exclusion verification, negative case (MEDIUM rules should be skipped).
- `7`: exception handling focus (prohibited try/catch/throw, abnormal branch missing return after error log), negative case (SafeMethod with proper return).
- `8`: Surface/Image cross-thread/cross-context operations (GraphicsStability_006/007/008), creation/release thread consistency, negative case (SafePerThreadSurface using BackendTexture).
- `9`: comprehensive full-scan with strict report format compliance, covering all categories with REPORT_TEMPLATE and PROBLEM_TEMPLATE validation, subagent mechanism verification.
- `10`: category-specific scan (BoundaryCondition + GraphicsStability), Parcel data boundary issues (BC_003/004/006/014), graphics stability (GS_001/012), negative case (SafeAllocateFromParcel with validation).
- `11`: RS thread model and GPU Context (GraphicsStability_002/004/005), VulkanCleanupHelper/SharedContext reference count mixing, negative case (correct ternary Ref() pattern).
- `12`: boundary condition type conversion and arithmetic overflow (BC_007/008/011/012/013), negative cases (SafeConvert with range check, SafeCompute with int64_t intermediate).

## Rule coverage summary

| Category | Total Rules | Rule IDs Tested | Coverage |
|----------|-------------|-----------------|----------|
| ExceptionHandling | 2 | 001, 002 | 100% |
| ConcurrencyStability | 1 | 001 | 100% |
| ResourceManagement | 5 | 001, 002, 003, 004, 005 | 100% |
| BoundaryCondition | 14 | 001–010, 011–014 | 100% |
| GraphicsStability | 12 | 001–012 | 100% |
| **Total** | **34** | **All 34 rules** | **100%** |

See [`../references/RULE_INDEX.md`](../references/RULE_INDEX.md) for the complete rule list and [`../references/REPORT_TEMPLATE.md`](../references/REPORT_TEMPLATE.md) for the report format specification.