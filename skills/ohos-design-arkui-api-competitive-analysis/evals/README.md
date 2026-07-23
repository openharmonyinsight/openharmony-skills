# ArkUI API Competitive Analysis Evals

Use [`evals.json`](evals.json) as the benchmark seed set. It contains 6 factual regression cases and 6 workflow edge cases; each case keeps its grading assertions in the JSON entry.

## Default Flow

1. Create a sibling workspace such as `ohos-design-arkui-api-competitive-analysis-workspace/iteration-1/`.
2. For the first release candidate or a change that affects evidence rules, workflow gates, category coverage, or output semantics, run every prompt in independent `with_skill` and `without_skill` sessions under the same model, platform baselines, date, network access, and tool permissions.
3. Record run conditions and fixture verification dates in `eval_metadata.json`.
4. Save each response under `with_skill/outputs/` or `without_skill/outputs/`, with its `timing.json` and `grading.json`.
5. Grade against the corresponding `expected_output` and `expectations` in `evals.json`.

## Regression Reuse

Do not repeat an unchanged full suite after every documentation-only or narrowly scoped revision. Reuse a prior immutable full-suite baseline when the model, tool permissions, source bundle, platform baselines, prompts, expectations, and unaffected Skill instructions are unchanged. Run only the cases whose triggering, workflow, evidence contract, or report structure may have changed, plus one representative unaffected smoke case when useful.

For every reused result, record the source Skill version, iteration path, commit or file snapshot, model, source-bundle identity, and the reason reuse is valid. For every focused regression, record the changed files, affected cases, and grading results. A focused regression validates only the stated delta; it must not be described as a fresh full-suite pass for the new Skill snapshot.

Run all 12 cases again when any of these conditions changes materially: eval prompts or expectations, category routing, mandatory dimensions, source authority rules, comparator selection, Fact/Claim traceability, report ordering required by graders, model/tool policy, or official source baseline.

Before each iteration, recheck version-sensitive signatures, defaults, units, availability, and behavioral facts against `interface_sdk-js`, Android Developers, and Apple Developer. Update stale assertions or mark unresolved facts as pending instead of requiring outdated answers.

Do not claim a fresh full-suite pass until all 12 with-skill cases have been run for that snapshot, all assertions have been graded, and the without-skill baselines have been retained for comparison. When results are reused, state the exact prior full-suite result and the focused regression scope separately.
