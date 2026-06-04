# ArkUI Build Error Analyzer Skill Evals

Use [`evals.json`](evals.json) as the seed set for benchmark iterations.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-arkui-build-error-analyzer-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-extraction-workflow/`.
4. Save per-run outputs under `with_skill/outputs/` and `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate results and review assertion deltas.

## Minimum success criteria

- At least one eval checks the extraction workflow (script usage, last_error.log reading, success detection).
- At least one eval checks symbol export diagnosis (ACE_FORCE_EXPORT + libace.map).
- At least one eval checks header optimization protection (add include to .cpp, not .h).
- At least one eval checks RefPtr forward declaration fix pattern.
- At least one eval checks LTO virtual thunk handling.
- At least one eval checks NEVER rule compliance (no cache clearing, no auto-modifications).
- At least one eval uses an English prompt to verify bilingual triggering.
- Assertions measure ACE Engine-specific error analysis, not generic C++ debugging.

## Current coverage map

- `0`: extraction workflow, last_error.log reading, error categorization, fix recommendation format.
- `1`: undefined symbol — export issue, ACE_FORCE_EXPORT, libace.map fine-grained patterns.
- `2`: header optimization protection — missing include after forward declaration, fix in .cpp not .h.
- `3`: RefPtr incomplete type — special member functions in header, `= default` in .cpp.
- `4`: LTO virtual thunk — dual libace.map patterns, English prompt.
- `5`: NEVER rule — LTO cache clearing refusal, redirect to code analysis.
