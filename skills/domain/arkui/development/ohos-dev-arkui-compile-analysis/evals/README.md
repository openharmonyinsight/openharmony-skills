# ArkUI Compile Analysis Skill Evals

Use [`evals.json`](evals.json) as the seed set for benchmark iterations.

## Default flow

1. Snapshot the current skill if you need an `old_skill` baseline.
2. Create a sibling workspace `ohos-dev-arkui-compile-analysis-workspace/iteration-1/`.
3. For each eval, create a descriptive directory such as `eval-0-full-analysis-workflow/`.
4. Save per-run outputs under `with_skill/outputs/` and `without_skill/outputs/`.
5. Add `eval_metadata.json`, `timing.json`, and `grading.json` for each run.
6. Aggregate results and review assertion deltas.

## Minimum success criteria

- At least one eval checks the full analysis workflow (analyze_compile.sh orchestration).
- At least one eval checks header dependency analysis (parse_ii.py usage, .ii file decision tree).
- At least one eval checks before/after benchmarking workflow (--save-script, reusable scripts).
- At least one eval checks metric interpretation (thresholds, priority-ordered optimization strategies).
- At least one eval checks cross-skill integration (references header-optimization for actual work).
- At least one eval checks troubleshooting (missing compile rules, new files).
- Assertions measure ACE Engine-specific analysis behavior, not generic compilation knowledge.

## Current coverage map

- `0`: full analysis workflow, analyze_compile.sh orchestration, actual-execution requirement.
- `1`: header dependency tree, parse_ii.py usage, .ii file decision tree, foundation/arkui/ filtering.
- `2`: before/after benchmarking, --save-script, reusable compile scripts, identical conditions.
- `3`: metric interpretation, threshold tables, priority-ordered strategies, high-impact file awareness.
- `4`: cross-skill integration, deep chain analysis, NEVER rules for hub headers.
- `5`: troubleshooting — new file not in build database, path format guidance.
