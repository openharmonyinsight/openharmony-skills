# ACE Engine Build Skill Evals

Use [`evals.json`](evals.json) as the seed set for benchmark iterations.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-arkui-ace-engine-build-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-fast-rebuild-source-only/`.
4. Save per-run outputs under `with_skill/outputs/` and `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate results and review assertion deltas.

## Minimum success criteria

- At least one eval checks --fast-rebuild safety (source-only change → safe).
- At least one eval checks BUILD.gn change detection (must NOT use --fast-rebuild).
- At least one eval checks test build with mandatory coverage flag.
- At least one eval checks SDK build constraints (no --build-target, correct output path).
- At least one eval checks test list build workflow (sequential, stop-on-error, disk management).
- At least one eval checks check_fast_rebuild.sh usage and the three-stage verification.
- Assertions measure ACE Engine build system specifics, not generic build tool knowledge.

## Current coverage map

- `0`: source-only fast rebuild, build command structure, component target.
- `1`: BUILD.gn change → full build required, stale ninja warning.
- `2`: test build with coverage, target naming convention (simple name, not GN path).
- `3`: SDK build, no --build-target, out/sdk/ output path.
- `4`: test list build, sequential execution, disk space management, resume from failure.
- `5`: check_fast_rebuild.sh, three-stage safety check, default to full build.
