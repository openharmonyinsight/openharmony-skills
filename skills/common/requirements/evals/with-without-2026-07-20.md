# OHOS Phase 0 Intake Bundle With/Without Eval Report

Date: 2026-07-20

Head commit: `78d46457f826d3bc66c3e0f8f54728cbd577f77c`

## Scope

This report covers the 10-skill OHOS Phase 0 intake bundle:

| Skill | Cases | With Skill | Without Skill |
|---|---:|---:|---:|
| `ohos-req-requirement-intake` | 6 | 6/6 | 2/6 |
| `ohos-req-feasibility-analysis` | 3 | 3/3 | 1/3 |
| `ohos-req-arch-decision` | 3 | 3/3 | 1/3 |
| `ohos-req-feature-baseline` | 4 | 4/4 | 1/4 |
| `ohos-req-review-gate` | 5 | 5/5 | 2/5 |
| `ohos-req-value-decision` | 5 | 5/5 | 2/5 |
| `ohos-req-feature-to-ir` | 4 | 4/4 | 1/4 |
| `ohos-req-intake-orchestration` | 5 | 5/5 | 1/5 |
| `ohos-req-proposal-to-sr` | 6 | 6/6 | 2/6 |
| `ohos-req-value-ppt-gen` | 3 | 3/3 | 0/3 |
| **Total** | **44** | **44/44** | **13/44** |

## Method

The with-skill path uses each skill's `SKILL.md` plus directly referenced templates and rules. The without-skill baseline uses the same prompt text and repository README requirements, but no skill instructions.

Structured cases come from each `ohos-req-*/evals/evals.json`. PPT cases come from `ohos-req-value-ppt-gen/evals/cases.yaml` and its prompt/expected files.

## Required Coverage

The intake orchestration and gate cases cover:

- `Ready`
- `Conditional Ready`
- `Not Ready`
- evidence-limited feasibility
- single-proposal fast path
- multi-proposal split confirmation
- role-blocked handoff

## Key Differences

| Area | With Skill | Without Skill |
|---|---|---|
| Traceability | Preserves `rr_id` and FR/AC identifiers across requirement, IR, proposal, SR, and handoff. | Often omits `rr_id` propagation or renumbers AC items. |
| Gate routing | Distinguishes `Ready`, `Conditional Ready`, and `Not Ready`; writes conditions into IR. | Often treats `Conditional Ready` as failure or drops condition metadata. |
| Human decisions | Blocks at feasibility clarification, ADR decision, split confirmation, and value decision. | Often infers decisions and proceeds without required user confirmation. |
| Evidence limits | Allows conditional completion only with disclaimer, unverified list, Owner, action, and Phase 2 close time. | Either blocks forever or presents unverified code as confirmed. |
| Platform scripts | Uses Python standard-library scripts; Bash wrappers are optional for Linux/macOS. | Relies on shell snippets and Unix utilities, which are not Windows-native. |
| PPT output | Uses `deckbuilder.Deck`, fixed 8-page review structure, logo, and required takeaways. | Commonly hand-builds `python-pptx`, misses takeaways, or overflows tables. |

## Executable Verification

The following commands were run on macOS:

```bash
python3 skills/common/requirements/ohos-req-intake-orchestration/scripts/test_related_skills_consistency.py
bash skills/common/requirements/ohos-req-intake-orchestration/scripts/test_related_skills_consistency.sh
python3 skills/common/requirements/ohos-req-intake-orchestration/scripts/install_related_skills.py --check
python3 skills/common/requirements/ohos-req-intake-orchestration/scripts/install_related_skills.py --check-probes
```

Results:

- Python consistency test: 7 passed, 0 failed
- Bash wrapper consistency test: 7 passed, 0 failed
- Install preflight: `Installed: 10/10`, `Result: READY`
- Probe preflight: `Probe result: PASS`, `Result: READY`

PPT smoke checks:

```bash
python3 examples/requirement_review_example.py
python3 examples/requirement_review_oneshot.py
python3 scripts/deckbuilder.py
```

Results:

- `requirement_review_example.py`: saved 8-slide deck
- `requirement_review_oneshot.py`: saved 8-slide deck
- `deckbuilder.py`: saved 4-slide demo deck

Generated `.pptx` files were removed after verification and are not part of the PR.

## Conclusion

With-skill evaluation satisfies the repository entry requirement for all submitted cases. The without-skill baseline demonstrates the expected failure modes around traceability, gate routing, human decision points, evidence-limited feasibility, platform portability, and PPT layout discipline.
