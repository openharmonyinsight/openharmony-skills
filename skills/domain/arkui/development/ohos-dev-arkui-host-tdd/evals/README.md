# OHOS Dev ArkUI Host TDD evals

These evals are split by reproducibility boundary. Do not combine the two suites into a single
`9/9` claim unless both suites were executed under the recorded conditions and the compact
evidence set below is retained.

## Suites

| File | Cases | Expectations | Environment |
|---|---:|---:|---|
| `evals.json` | 8 (`0`, `2`–`8`) | 54 | Hermetic, repository fixtures only |
| `integration_evals.json` | 1 (`1`) | 5 | Pinned writable OpenHarmony Host workspace |

The hermetic source fixture is pinned to ace_engine revision
`3d648d632141678368bde7a0376cf80f67f6e3e4`. Source hashes and captured artifact states are in
`fixtures/ace-engine-host-routing/`. The captured binaries and discovery output are deliberately
treated as data, not as live build or test evidence.

## Required tools and model settings

- Codex CLI available as `codex`.
- Model: `gpt-5.6-sol`.
- Reasoning effort: `high`.
- Approval mode: `never` for eval agents.
- One fresh Codex process per case and arm.
- Hermetic cases use a read-only sandbox.
- The integration case uses a workspace-write sandbox only after environment preparation returns
  `ready: true`. Run Codex from this eval directory; the manifest carries absolute Host binary and
  XML paths, so the OpenHarmony aggregate root need not be a trusted Git working directory.

Run the definition check first:

```bash
python3 scripts/validate_evals.py
```

It must report exactly 9 unique cases and 59 expectations, with every declared static fixture
present.

## Hermetic forward eval

Create an artifact directory outside the skill tree, then run each case in a fresh process:

```bash
artifact_dir=/tmp/host-tdd-eval-$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "$artifact_dir"

for id in 0 2 3 4 5 6 7 8; do
  python3 scripts/run_eval.py \
    --suite hermetic --case "$id" --arm with \
    --artifact-dir "$artifact_dir" \
    --output "$artifact_dir/with-$id.txt"
done
```

Agents must use only the declared fixture files. Accessing an external OpenHarmony checkout,
running a build, or executing a gtest invalidates a hermetic run.

## Isolated baseline

The baseline must be run while `ohos-dev-arkui-host-tdd` is genuinely unavailable to the fresh
agent. Omitting `$ohos-dev-arkui-host-tdd` from the prompt is insufficient because implicit skill
selection can still load it.

Before baseline execution:

1. Move or disable every installed copy of the target skill outside all Codex discovery roots.
2. Keep unrelated skills, including the build skill, unchanged.
3. Confirm a fresh Codex process does not list or resolve `ohos-dev-arkui-host-tdd`.
4. Record the disabled path and restoration action in the run metadata.

Then run:

```bash
for id in 0 2 3 4 5 6 7 8; do
  python3 scripts/run_eval.py \
    --suite hermetic --case "$id" --arm baseline --baseline-isolated \
    --artifact-dir "$artifact_dir" \
    --output "$artifact_dir/baseline-$id.txt"
done
```

Restore the target skill immediately after the baseline arm, even if a case fails.

## Host integration eval

The integration case is not portable without an OpenHarmony Host workspace and current build
artifacts. Prepare it explicitly:

```bash
python3 scripts/prepare_host_integration.py \
  --oh-root /path/to/openharmony \
  --artifact-dir "$artifact_dir" \
  --output "$artifact_dir/environment.json"
```

Preparation requires:

- ace_engine at the pinned revision with a clean working tree;
- a terminal, attributed, successful `host_product/ace_engine_test` build performed after that
  source state;
- executable stripped and `exe.unstripped` drawable binaries with matching Build IDs;
- retained `build_state.json` provenance.

If the manifest says `ready: false`, report `BLOCKED_ENVIRONMENT`; do not run the case and do not
score it as pass or fail. If it says `ready: true`, run each arm separately:

```bash
python3 scripts/run_eval.py \
  --suite integration --case 1 --arm with \
  --artifact-dir "$artifact_dir" \
  --output "$artifact_dir/with-1.txt"

# Disable the target skill as described above before this command.
python3 scripts/run_eval.py \
  --suite integration --case 1 --arm baseline --baseline-isolated \
  --artifact-dir "$artifact_dir" \
  --output "$artifact_dir/baseline-1.txt"
```

Use a distinct XML path per arm, or archive the first XML before starting the second arm.

In a nested managed Codex environment, the child workspace-write app-server may be unable to
initialize inside the outer sandbox. If that happens before the eval agent starts, retain and mark
the attempt invalid, then rerun the same runner through an approved outer execution. The child
eval must still use its declared workspace-write sandbox; do not count the bootstrap failure as a
case pass or failure.

## Grading and report rules

Grade only the final user-visible output plus retained command/XML evidence. Do not award credit
for hidden reasoning. For each expectation, store exactly:

Installed Skill instructions selected by an eval agent are procedural context, not undeclared
task fixtures or an external OpenHarmony workspace. Do not fail an input-scope requirement solely
because an installed Skill was read unless that requirement explicitly prohibits it. Repository
or workspace reads outside declared fixtures remain subject to the case constraints.

```json
{"text": "...", "passed": true, "evidence": "..."}
```

A case passes only when every expectation passes. Store per-arm grading under
`grading/with-<id>.json` and `grading/baseline-<id>.json`.

Use a fresh independent grader for each case. For example:

```bash
python3 scripts/grade_eval.py \
  --suite hermetic --case 0 \
  --with-output "$artifact_dir/with-0.txt" \
  --baseline-output "$artifact_dir/baseline-0.txt" \
  --output-dir "$artifact_dir/grading"
```

For integration case 1, point `--with-output` and `--baseline-output` at their distinct arm
directories so the grader also reads each arm's manifest and XML.

Keep generated prompts, full transcripts, grader raw output, per-run metadata, and command logs in
the external working artifact directory while grading. The compact repository evidence set is:

- final `with-*` and `baseline-*` answers;
- integration manifests and XML;
- validated per-arm grading JSON;
- one combined run-provenance record containing prompt/output/command-audit hashes and concise
  action summaries;
- baseline-isolation evidence.

Do not commit generated prompts, full transcripts, per-run metadata, command logs, or grader
scratch unless a disputed score specifically requires them. Prompts and these intermediate files
are reproducible from the eval definitions and harness scripts.

The report must include:

- skill revision, eval-definition hash, fixture revision, model, effort, and sandbox;
- baseline isolation evidence;
- separate hermetic and integration totals;
- per-case and per-expectation results;
- commands, exit codes, XML statistics, and artifact hashes for integration execution;
- invalid, blocked, or contaminated runs without converting them into failures or passes;
- raw `with-*` and `baseline-*` outputs and grading JSON paths;
- a leakage caveat: these prompts are regression evals derived from known failure modes, so they
  measure rubric adherence and safety regression, not held-out generalization.

Behavioral gain may be claimed only when the with-skill arm passes more expectations than the
isolated baseline. A tie is `no demonstrated gain`. Never describe a regression suite result as
held-out generalization.
