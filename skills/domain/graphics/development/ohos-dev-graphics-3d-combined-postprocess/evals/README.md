# OpenHarmony Graphics3D Combined Post-Process Skill Evals

Use [`evals.json`](evals.json) as the seed set for the first benchmark iteration.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-graphics-3d-combined-postprocess-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-film-grain-full-implementation/`.
4. Save per-run outputs under `with_skill/outputs/` and `old_skill/outputs/` or `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate the iteration with the `skill-creator` benchmark script and generate the review viewer.

## Pass threshold

- Each eval: at least **80%** of expectations must pass for the eval to count as passed.
- Overall: at least **6 out of 7** evals must pass for the skill iteration to be accepted.
- Any eval that fails on a dual-path conversion expectation (Step 5 + Step 6 both called) or index consistency expectation (shader-C++ index match) is a **critical failure** regardless of other expectations — these are the skill's core value proposition.

## Minimum success criteria

- At least one eval checks a complete 22-step implementation of a basic single-pass effect (≤4 parameters, factors[] only).
- At least one eval checks parameter splitting between factors[] and userFactors[] for effects with >4 parameters.
- At least one eval checks that multi-pass effects are correctly rejected from the Combined system.
- At least one eval checks that index-full scenarios are correctly rejected (indices 0-7 all occupied).
- At least one eval checks shader-C++ index mismatch diagnosis and cross-file consistency verification.
- At least one eval checks systematic debugging across all three modules (LumeRender, Lume3D, LumeScene).
- At least one eval checks review-mode findings for configuration struct violations and architectural boundary issues.
- Assertions measure OpenHarmony Graphics3D-specific deltas instead of generic rendering knowledge.

## Current coverage map

- `0`: successful 22-step implementation of basic single-pass effect (2 parameters, Film Grain), factors[] only, index 3 available — validates all 3 modules (LumeRender 8 steps + Lume3D 5 steps + LumeScene 9 steps), dual-path conversion, shader-C++ index consistency.
- `1`: >4 parameter effect requiring factors[] + userFactors[] split, dual-path conversion, shader signature with userFactor.
- `2`: multi-pass effect boundary check — SSAO must be rejected from Combined system.
- `3`: shader compilation error diagnosis — index mismatch across shader constants, C++ enums, and DataStore conversion.
- `4`: systematic runtime debugging checklist — effect not applied, dual-path verification, GPU uniform validation.
- `5`: review-mode findings for BloomConfiguration — multi-pass incompatibility, index overflow, parameter count issues.
- `6`: index-full rejection — all indices 0-7 occupied, must reject Film Grain and warn about out-of-range index consequences.

## Eval design rationale

| Eval | Skill capability tested | Why it matters |
|------|------------------------|----------------|
| 0 | End-to-end workflow execution | Validates the skill guides a complete 22-step implementation without skipping steps |
| 1 | Parameter allocation decision | Tests the decision tree for >4 parameters and userFactors integration |
| 2 | Applicability boundary recognition | Ensures the skill correctly rejects out-of-scope multi-pass effects |
| 3 | Prohibited practice: index mismatch | Tests troubleshooting for the most common shader-C++ consistency error |
| 4 | Cross-module debugging | Validates systematic diagnosis across LumeRender → Lume3D → LumeScene chain |
| 5 | Review-mode architectural judgment | Tests recognition of fundamental architectural incompatibilities |
| 6 | Index capacity boundary | Tests rejection when all Combined slots are occupied and warns about out-of-range consequences |
