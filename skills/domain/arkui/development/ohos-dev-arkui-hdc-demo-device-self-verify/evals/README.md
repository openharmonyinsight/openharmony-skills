# ArkUI HDC Demo Device Self Verify Evals

Use [`evals.json`](evals.json) as the benchmark seed set.

## Minimum success criteria

- Multiple connected targets block all mutation until an explicit connect-key is selected.
- HAP/HSP package shape selects the correct dependency-aware install route.
- Native library replacement verifies the real path, rollback, `sync`, and runtime loading.
- Black-screen or missing UI-tree evidence produces a blocker rather than a false pass.
- The common `ohos-dev-hdc-command-usage` dependency is indexed before the ArkUI workflow starts.
- Mid-run reverse SSH or HDC loss stops mutation and triggers layered recovery guidance.

## Current coverage map

- `0`: multiple targets, explicit `-t`, HAP launch, ArkUI evidence.
- `1`: HAP/HSP dependency-aware installation.
- `2`: guarded native library replacement and load proof.
- `3`: locked/black-screen blocker handling.
- `4`: required HDC skill dependency installation/indexing.
- `5`: interrupted run recovery, hardware/image checks, and fresh evidence after reconnection.
