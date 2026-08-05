# Reviewing Skill-Definition PRs

Use this checklist when the PR changes files in a skills repository (e.g. `openharmony-skills`) — adding or modifying `SKILL.md`, `agents/*.yaml`, `evals/evals.json`, `evals/README.md`, or supporting files. These are not code PRs and require a different review lens.

## Default flow

1. Read the PR title and body — skill PR bodies often contain forward-eval reports, score summaries, and benchmark manifests. These are part of the PR's evidence, not noise.
2. Collect context with `collect_pr_context.py` (same as code PRs).
3. Review each new/modified file against the dimensions below.
4. Assign each file one status: `reviewed`, `mechanical-low-risk`, or `skipped-with-reason`.

## Review dimensions per file type

### SKILL.md

**Frontmatter (`metadata`) completeness:**

- `name` matches the directory name (e.g. `ohos-dev-foo-bar` → `skills/domain/…/ohos-dev-foo-bar/`)
- `description` covers WHAT + WHEN + trigger keywords (repo paths, tool names, error messages)
- `scope` is appropriate: `common` for cross-Domain, `domain` for one-Domain
- `stage` + `domain` + `capability` are set and consistent with directory placement
- `version` exists; `status` (`draft`/`trial`/`stable`) reflects maturity
- **Hard dependencies on other skills**: does SKILL.md invoke `$ohos-dev-foo-bar` or reference another skill's scripts? If so, `related-skills` MUST list them. A runtime dependency that isn't declared means the skill breaks when installed alone.
- `tags` add search value (optional but encouraged)

**Description quality:**

- Does it name concrete repo paths, GN targets, binary names, gtest filters, or CLI flags that an agent can match against?
- Can an agent route to this skill from a user request without guessing?

**Process completeness:**

- Are the steps ordered and executable in sequence?
- Is there a clear routing table or condition table that chooses which branch of the process to follow?
- Are stopping conditions and failure branches explicit, not implicit?
- Are critical paths (build, deploy, sensitive data read) guarded by evidence gates?

**Anti-patterns (Never rules):**

- Are they concrete prohibitions with consequences, not slogans?
- Each "Never" should state what goes wrong if violated (false pass, lost provenance, corrupted artifact, etc.)

**Freedom calibration:**

- Do high-risk steps use exact paths, exact commands, and explicit evidence thresholds?
- Are there any ambiguous instructions left to agent interpretation that would lead to different results on each run?

**Progressive disclosure:**

- Is the main SKILL.md self-contained? (Target ~200-400 lines for runtime)
- Are eval cases, example outputs, and large reference material kept in `evals/` and `references/`?

### agents/openai.yaml (or similar agent configs)

- `display_name` is human-readable and matches the skill's name
- `short_description` is a one-liner summary
- `default_prompt` **must not contradict SKILL.md routing logic**. Check: does it unconditionally suggest actions that the SKILL.md only allows conditionally? (e.g. "build and run" vs "audit first, build only when evidence gates pass")
- If SKILL.md is defense-first, the default prompt should not bypass those defenses

### evals/evals.json

- Each eval `id` is unique
- `prompt` is self-contained (the agent reading it has no session context)
- `expectations` are binary-gradable — each one passes or fails unambiguously
- `files` array: are any fixture files referenced but not included?
- **Version pinning**: If evals depend on a specific repo state (e.g. GN dependency closure of ace_engine@commit X, specific binary artifacts), is the benchmark manifest provided? Without version pinning, evals drift with upstream changes and the recorded score becomes unverifiable.
- Coverage: do the evals cover both positive cases (this works) and negative cases (skill correctly refuses unsafe action)?

### evals/README.md

- Does it describe the evaluation methodology (with-skill vs isolated baseline)?
- Are safety constraints documented (read-only evals, no-build constraints, required permissions)?
- Is the scoring method clear (binary pass/fail per expectation, case passes only when all expectations pass)?

## Deletion / merge PRs (removing skills, folding responsibility upstream)

When a PR deletes one or more skills and merges their responsibility into surviving skills (e.g. `ohos-req-feature-to-ir` + `ohos-req-proposal-to-sr` → `feature-baseline` + `handoff`), use these additional dimensions. Verified on PR 324 — this lens produced the only high-severity findings.

**1. Dangling references to deleted skills are the #1 blocker.** The deleted skill may be gone from git, but surviving skills still route to it. Check EVERY surviving skill that named the deleted skill in `related-skills`, body routing, `next_action`, or templates:

- Grep the whole repo for the deleted skill names (`rg -n "ohos-req-feature-to-ir" skills/`), their artifact names (`IR.md`, `SR.md`), and inherited field names (`rr_id`).
- Run the repo's own consistency scripts — they are the ground truth, not diff reading:
  - `install_related_skills.py --check` / `check_related_skills_consistency.py` / `test_related_skills_consistency.py` (openharmony-skills)
  - A script returning `INCONSISTENT` or a failing test (`8 passed, 1 failed`) IS a high-severity finding; report the exact failing command and its output.
- Verify deletion is real in git (`D` status), not content-cleared (e.g. `proposal.md` moved via `R094` is fine, but a skill that "deleted" its body while keeping the directory is not).

**2. Merged responsibility completeness — each deleted section must land somewhere.** For every numbered section/template of the deleted skill (8 platform evaluations, 6 extension dimensions, RR_MCP push, GA evidence gates, traceability matrices), confirm a surviving file carries it. Map them explicitly (§6.1-6.8 → `feature.md` §6.1-6.8). A hard gate that existed in the deleted skill (e.g. "must be GA-Approved with `gate_a` evidence non-empty") must reappear in the surviving workflow — losing it is a regression, not a cleanup.

**3. Version floors for merged responsibilities.** If the merged duties only exist in a bumped version (v0.4.0), the orchestrator's `min_version` and the install script's version check must be raised to match. Otherwise preflight prints `READY` with an installed old version that lacks the merged responsibilities. Check both the frontmatter `related-skills` min_version AND `REQUIRED_SKILLS` in the install script.

**4. Eval / benchmark migration.** Deleted skills' evals must migrate to the surviving skills or the eval set shrinks. Check `benchmark.json` totals (e.g. `44/44`) against the actual eval set — if 10 cases belonged to deleted skills and weren't migrated, `44/44` no longer describes the PR head. Also check `grading.json` and surviving evals for assertions about the old flow ("Step 0.9.1", "从 SR 读取责任人", "不生成IR").

**5. Runtime contract for legacy artifacts.** If the PR keeps historical artifacts (old `IR.md`/`SR.md` files "preserved by naming convention"), the retention policy must be in the runtime skill contract (SKILL.md/handoff), not only in the PR description — the executing agent can't see the PR description. Require explicit: preserve read-only, not a gate prerequisite, no auto-rename/delete, and a selection rule for mixed directories.

## Commonly missed issues

| Issue | How to detect |
|-------|--------------|
| Hard skill dependency not declared in `related-skills` | Search SKILL.md for `$ohos-` references — every one should be in `related-skills` or explicitly justified as optional |
| `default_prompt` unconditionally suggests a high-risk action | Compare the prompt against the skill's routing table and evidence gates |
| Eval expects a specific GN state but no version is pinned | Check `files: []` in eval definitions; if empty and the eval describes specific file content or binary paths, version pinning is missing |
| Anti-pattern without consequence | Read each "Never" — does it say why? |
| Ambiguous path or command | Search for relative paths, unexpanded placeholders, or "use appropriate flags" — these leave too much to agent interpretation |
| Eval score reported but no supporting artifacts | Check if `evals/reports/` or `evals/artifacts/` exist in the PR diff; if not, the score is unverifiable |

## Delete / consolidation PRs (skill removal + responsibility merge)

When a PR deletes skills and merges their responsibilities into survivors (e.g. PR 324 removed `ohos-req-feature-to-ir`/`ohos-req-proposal-to-sr` into `ohos-req-feature-baseline` + `handoff.md`), review these dimensions beyond the per-file checklist:

- **Residual references live in UNMODIFIED files — the #1 miss.** The deleted skill's name/route is usually still referenced by skills NOT touched by this PR (review-gate `next_action`, value-decision routing, requirement-intake scope, gate templates). Search the whole PR-head tree for the deleted skill name + its artifacts (`IR.md`, `SR.md`, `rr_id 从 IR 继承`). These findings cannot attach to any diff line — they go as PR-level comments.
- **Merge completeness is item-by-item.** For each responsibility the deleted skill owned (assessment items, extension dimensions, push/electronic-flow rules, traceability matrix, owner tables), map it to the survivor — then look for duties that were silently DROPPED (e.g. hard gate "status=GA-Approved + gate_a evidence non-empty" often vanishes). The reverse also bites: survivor templates may keep fields the deleted skill owned, now contradicting the new flow (e.g. proposal template still has an 8-dimension table while the orchestrator says downstream inherits 6).
- **Version lower-bounds must move with the merged duties.** If the new responsibility exists only in survivor v0.4.0, the orchestrator's `min_version` AND the install script's `REQUIRED_SKILLS` must both bump to 0.4.0 — otherwise precheck prints READY with an old skill that lacks the merged duties.
- **Eval migration + benchmark truthfulness.** Deleted skills' eval cases must be migrated into survivors; update `grading.json`/`benchmark.json` counts. A stale "44/44" while 10 cases were deleted is a finding.
- **Downstream prechecks.** Search `workflows/*delivery*/` and other phase skills for references to the deleted artifacts (IR/SR as Phase 1-9 preconditions); the handoff must become the new gate.
- **Historical-artifact policy.** "Keep old IR.md/SR.md read-only, don't rename/delete" belongs in the runtime SKILL.md contract, not only in the PR description — otherwise agents don't know how to treat mixed old/new directories.
- **Consistency tests are the ground truth.** Run `check_related_skills_consistency.py` / `test_related_skills_consistency.py` on PR head; a failing S1 with 4 unresolved references is a high-severity finding, not a nit.

## Script language rewrites (py → sh) — review dimensions

When a PR converts `.py` helper scripts to `.sh` (verified on PR 325: `install_related_skills.py`/`check_related_skills_consistency.py`/`test_related_skills_consistency.py` → `.sh`), each of these is a distinct finding class:

- **Mode flags parsed but never dispatched.** A `MODE` variable assigned from `$1` and never used means `--check`/`--install`/`--check-probes` all run identical logic. Test: run each mode on the same tree and diff the outputs — identical output across modes = finding.
- **Env-var overrides dropped.** Old Python honored `OHOS_REQ_SKILLS_DIR` / `OHOS_REQ_SKILLS_SOURCE_DIR` (or equivalent); the sh port may ignore them. Isolated test: target dir missing a required skill, source dir complete, run `--install` → must actually copy; `Installed: N/7` + `NOT READY` + skill still absent = regression.
- **semver compared as strings.** `[ "$found" \< "$required" ]` misorders `0.10.0` vs `0.3.0`. Isolated test: found=`0.10.0`, required=`0.4.0` → must PASS; a string compare reports mismatch. Require numeric segment comparison.
- **Checker scan-range shrink = fake green.** The .py checker walked all `ohos-req-*` SKILL.md + `reference(s)/**` and validated every reference; the sh port may only compare the orchestrator's body/frontmatter/install arrays. Prove it with a **negative injection test**: append a line like `调用 ohos-req-review-gate` (a deleted skill) to any surviving reference file in a temp copy, run the checker — it MUST exit non-zero / print `INCONSISTENT`. If it still prints `CONSISTENT` exit 0, that is a high-severity fake-green finding. Also confirm it catches real dangling aliases already present in head (e.g. surviving skills routing to `ohos-intake`/`ohos-feature` that no longer exist).

## Eval runner vs real eval schema

When the PR adds a generic eval runner (`run_skill_evals.py`) plus `evals.json` suites, check the runner against the ACTUAL assertion schemas in the repo, not its own unit tests:

- **Field mismatch.** Runner reads `assertion["text"]` but real evals put the regex in `pattern`. Reproduce with a real case (e.g. an output containing `flowchart TD` against a `flowchart|sequenceDiagram` regex) — a valid output graded failed proves the bug.
- **Natural-language `not_contains`.** If `not_contains` entries are prose ("正文中不存在 待确认/TBD/待分析 占位符") and the runner treats the whole sentence as a forbidden literal, output actually containing `TBD` still passes. Require explicit `tokens`/`patterns` lists.
- **Count non-conservation.** `collect` may count YAML cases as manual without adding them to `assertions`, so total ≠ programmatic + manual. Verify totals add up exactly.
- **Runner self-tests are not ground truth.** `unittest` passing on synthetic schemas proves nothing; add at least one end-to-end case from a real evals.json prompt/fixture to output to grade.

## Delete/merge — extra dimensions verified on PR 325 (57-file restructure)

- **py→sh script rewrites often become stubs.** When the PR converts `.py` scripts to `.sh` (e.g. `install_related_skills.py` → `.sh`, `check_related_skills_consistency.py` → `.sh`), verify the new shell script actually implements each public mode. PR 325's `install_related_skills.sh` parsed `MODE` but never used it — `--check`, `--install`, `--check-probes` all printed identical output; env overrides (`OHOS_REQ_SKILLS_DIR`/`OHOS_REQ_SKILLS_SOURCE_DIR`) were ignored; the shell `test_related_skills_consistency.sh` dropped the old S2a/S2b/probe cases. **Isolate-reproduce each mode** in a sandbox (missing dependency + `--install`; found `0.10.0` vs required `0.3.0`) rather than trusting the happy-path output.
- **Bash string `<` is not semver comparison.** `check_related_skills_consistency.sh`-family scripts that compare versions with `[ "$found" \< "$required" ]` misjudge `0.10.0` vs `0.3.0`. Flag any string comparison on versions; the old Python tuple comparison was the correct behavior.
- **"Docs refreshed from user guide" commits introduce nonexistent source paths.** R2 commit `d3baf91` replaced the preflight command path with `{SKILL_HOME}/platform_issues/user_guide/ohos-req-intake-orchestration/scripts/install_related_skills.sh` — `platform_issues/` does not exist in the repo. Any commit message containing "refresh from user guide"/"from docs" → grep the head tree for every path it references; a mandatory preflight pointing at a nonexistent path is a high finding (breaks Step 1 before it starts).
- **New proposal/artifact must match the actual downstream consumer contract.** When a deleted skill's output (IR/SR/handoff) is replaced by a new artifact (e.g. `proposal.md`), verify the new artifact satisfies the real downstream consumer. PR 325's proposal wrote `{docs_dir}/proposals/05-proposal-<slug>.md` while the only in-repo consumer `workflows/ohos-delivery-kit/runtime/assets/contracts/artifacts.yaml` requires `.codespec/changes/<change-id>/proposal.md` with an `Agent Scope Guard` section — a path+filename+schema mismatch means the handoff is broken. Also check the new artifact doesn't inherit the deleted skill's provenance chain (`proposal.md` still read `rr_id` from the deleted `IR.md`).
- **New eval runner must be validated against the repo's real eval schema.** PR 325 added `evals/run_skill_evals.py` whose own unit tests passed but which mis-graded real evals: `regex` branch read `assertion["text"]` while the repo schema puts the regex in `pattern`; `not_contains` assertions written as natural language ("正文中不存在 TBD 占位符") were satisfied by output that actually contained `TBD`; `collect` counted 102 assertions but programmatic+manual summed to 106. When a PR adds an eval runner/grader, run it against the repo's actual `evals.json`/`cases.yaml` (not just its synthetic tests) and check assertion-count conservation.
- **Rewritten consistency scripts can false-green — verify scan scope, don't just trust exit 0.** When the PR rewrites the consistency/install/test scripts (e.g. Python → bash), a passing run (`CONSISTENT` / `READY` / `6 passed, 0 failed`, exit 0) is NOT proof the tree is consistent. Diff the NEW script's scan scope against the OLD implementation: the old Python may have walked every `ohos-req-*` SKILL.md + `reference(s)/**/*.md|json` validating references, while the new bash only compares orchestrator body/frontmatter/install arrays. Verified on PR 325: injecting a deleted skill name (`ohos-req-review-gate`) into `ohos-req-requirement-intake/reference/requirement-fields.md` still produced `Result: CONSISTENT` exit 0, and the head even had real dangling routes (`ohos-req-feasibility-analysis/SKILL.md:28,33,56` → nonexistent `ohos-intake`/`ohos-feature`) that the script reported green. Technique: run the script on PR head, then run an isolated injection repro (add a deleted-skill reference to a survivor file and confirm it is caught); if not caught, that's a high finding.
- **0-hit residual grep ≠ clean.** Grepping the deleted skill names/artifacts (`IR.md`, `SR.md`, `handoff.md`, `rr_id`) to zero is NECESSARY but NOT SUFFICIENT — PR 325 had 0 literal references yet the biggest finding was that the deleted skills' responsibilities (RR_MCP electronic flow, GA evidence gate, SR 1:1 mapping, traceability, Phase 1-9 handoff preconditions) were dropped with no survivor carrying them. A 0-hit result should trigger the responsibility-mapping pass (#2) harder, not a "clean cleanup" conclusion.
