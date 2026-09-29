---
name: odk-review
description: "Use when reviewing implemented ODK changes against ACs and code-quality risks, automatically after implementation or on explicit request. Review records are optional; zero plugin dependencies."
license: MIT
---

# ODK Review

## Prerequisites

- `spec.md` with AC list
- `execution-plan.md` with Task list and code scope
- Implementation code exists; uncommitted changes can be reviewed before PR approval.

## Input

1. Read `spec.md` AC list
2. Read `execution-plan.md` Task list and code scope
3. Read review templates from `{{ASSET_ROOT}}/templates/review/`

## Steps

1. Review actual implementation files and the full relevant diff (including untracked files) against each AC. Inspect correctness, failure paths, tests and regressions. Use templates as checklists, not as a substitute for examining code. Do not commit merely to start review.

2. Reuse existing implementation evidence for unchanged inputs; correct missing or inaccurate code mapping/AC-Task status rather than regenerating it. Report concrete findings with file references and verification gaps; do not claim unexecuted checks passed.

3. Return PASS or actionable findings to the caller. In the automatic handoff, the coordinator owns source-PR confirmation and the later design-docs reminder; do not ask a second publishing question here. Standalone review never authorizes a source or document push.

## Output

Write optional process evidence to `codespec/changes/<repo-name>/<proposal-id>/evidence/reviews/`.

Do not generate `reviews/` or `gates/` in the minimal archive root by default. These records are process evidence, not formal archive artifacts.

Report whether all ACs are covered and identify unresolved deviations. Optional review documents may be written when requested; a separate approval of a generated report is not required to run validation.

Keep document submission separate from review completion; source PR and design-docs publication each require the user's authorization.

When called by the automatic implementation handoff, return findings to that coordinator; it invokes `{{CMD_PREFIX}}validate` next. A standalone review can suggest validation but must not start source submission on its own.
