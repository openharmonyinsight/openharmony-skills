# ArkUI Header Optimization Skill Evals

Use [`evals.json`](evals.json) as the seed set for benchmark iterations.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-arkui-header-optimization-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-screening-and-strategy/`.
4. Save per-run outputs under `with_skill/outputs/` and `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate results and review assertion deltas.

## Minimum success criteria

- At least one eval checks the screening workflow (extract-includes.py + manual classification).
- At least one eval checks forward declaration correctness for pointer/RefPtr vs value/base-class.
- At least one eval checks enum splitting strategy for multi-consumer headers.
- At least one eval checks PIMPL decision logic (avoid for hot paths, prefer simpler strategies first).
- At least one eval checks NEVER rule compliance (hub headers, conditional includes).
- At least one eval uses an English prompt to verify bilingual triggering.
- Assertions measure ACE Engine-specific behavior, not generic C++ optimization knowledge.

## Current coverage map

- `0`: screening workflow, strategy priority order, step-by-step verification.
- `1`: forward declaration with RefPtr, include relocation to .cpp, RefPtr pitfall awareness.
- `2`: split-enums strategy, namespace placement, consumer migration.
- `3`: PIMPL decision tree, hot-path avoidance, ACE Engine PIMPL pattern.
- `4`: NEVER rule — hub headers (ace_type.h, frame_node.h).
- `5`: NEVER rule — conditionally-guarded includes, `#ifdef OHOS_BUILD_ENABLE_*`.
