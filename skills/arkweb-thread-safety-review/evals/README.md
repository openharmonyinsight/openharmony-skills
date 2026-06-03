# ArkWeb Thread Safety Skill Evals

Use `evals.json` as the first benchmark seed set for `arkweb-thread-safety-review`.

## Scope

These evals are derived from the skill's `examples/` directory. They check whether the agent can:

- report each `standard_rule1` through `standard_rule10` violation only when clear current-file evidence exists;
- keep the output in the strict JSON schema required by `SKILL.md`;
- avoid false positives for value-transfer and insufficient-evidence cases;
- include rule id, rule level, evidence, minimal fix direction, and team attribution for every violation.

## Current Coverage

- `standard_rule1_bad` through `standard_rule10_bad`: one positive violation case for each standard rule.
- `no_violation_id_transfer`: WebContents/RenderFrameHost accessed on UI while only a stable id crosses threads.
- `no_violation_uncertain_thread`: suspicious Audio API without entry-thread or object-thread evidence.

## Grading Notes

For positive cases, a passing run should produce JSON with at least one matching violation and no non-standard rule ids. For no-violation cases, a passing run should produce valid JSON with `summary.total_violations` equal to `0` and an empty `violations` array.

The `source_example` field points to the original example material used to derive each eval. Keep the example and eval expectations aligned when either side changes.
