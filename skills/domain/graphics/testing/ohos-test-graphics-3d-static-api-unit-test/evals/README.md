# Graphics 3D Static API Unit Test Skill Evals

Use [`evals.json`](evals.json) as the seed set for benchmarking the skill.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-test-graphics-3d-static-api-unit-test-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-camera-basic-tests/`.
4. Save per-run outputs under `with_skill/outputs/` and `old_skill/outputs/` or `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate the iteration with the `skill-creator` benchmark script and generate the review viewer.

## Pass threshold

- Each eval: at least **80%** of expectations must pass for the eval to count as passed.
- Overall: at least **6 out of 7** evals must pass for the skill iteration to be accepted.
- Any eval that fails on a Destroy()-related or annotation-related expectation is a **critical failure** regardless of other expectations passing — these are the skill's core value proposition.

## Minimum success criteria

- At least one eval checks complete test file generation for a new ETS wrapper class.
- At least one eval checks error path coverage with appropriate test levels.
- At least one eval checks property roundtrip test pattern.
- At least one eval checks review-mode findings for convention violations.
- At least one eval checks BUILD.gn configuration guidance for new test modules.
- At least one eval checks diagnosis of resource cleanup and assertion issues.
- At least one eval checks test strategy table application for a method type not explicitly exemplified in the skill.
- Assertions measure OpenHarmony-specific test deltas (annotations, HWTEST_F, Destroy(), namespace) instead of generic GTest quality.

## Current coverage map

- `0`: new CameraETS test file generation — file naming, class naming, annotations, HWTEST_F, namespace, Destroy(), includes.
- `1`: SceneETS::Load error path tests — multiple scenarios, sequential numbering, test levels (Level1 vs Level2), EXPECT_FALSE.
- `2`: MaterialETS property roundtrip — setter→getter pattern, EXPECT_EQ, EXPECT (not ASSERT), Destroy().
- `3`: review findings — missing annotations, wrong macro (TEST vs HWTEST_F), wrong class name suffix, missing _Number, ASSERT vs EXPECT, missing Destroy(), missing namespace, missing include.
- `4`: BUILD.gn configuration — sources, include_dirs, new target, group deps, platform defines, LIB_ENGINE_CORE macro.
- `5`: diagnosis and fix — missing Destroy() causing crashes, ASSERT skipping cleanup, per-object vs engine-level cleanup responsibility.
- `6`: strategy table application — Reset() method (not explicitly exemplified), test level selection (Level1 for happy-path, Level2 for error paths), full convention compliance.

## Eval design rationale

| Eval | Skill aspect tested | Why it matters |
|------|---------------------|----------------|
| 0 | Basic test generation | Most common use case; validates all mandatory conventions in one output |
| 1 | Error path coverage | Tests understanding of test levels and sequential numbering |
| 2 | Property roundtrip | Tests domain-specific setter/getter pattern |
| 3 | Review mode | Tests ability to identify violations in existing code |
| 4 | BUILD.gn setup | Tests environment configuration knowledge |
| 5 | Diagnosis | Tests understanding of Destroy() rule and ASSERT vs EXPECT trap |
| 6 | Strategy table extension | Tests whether the agent correctly applies the test strategy table to method types not shown in examples |
