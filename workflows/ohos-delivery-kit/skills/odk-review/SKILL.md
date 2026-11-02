---
name: odk-review
description: "Use when reviewing implemented ODK changes against ACs and code-quality risks, automatically after implementation or on explicit request. Review records are optional; zero plugin dependencies."
license: MIT
---

# ODK Review

## Existing artifacts first

<!-- ODK:reference contracts/skill-guides/router/document-updates.md -->
Before this skill's interview, template loading, delegation or writes, read
`contracts/skill-guides/router/document-updates.md`. Read every existing target's
full frontmatter and body first; revise it in place and preserve confirmed
content, stable IDs and evidence. Create a target only when it does not exist.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and use the effective
contract. It takes precedence over standard-only artifact lists below; native
OpenSpec schemas remain standard/critical and lite uses the base flow.
<!-- /ODK:reference -->

## Prerequisites

- `spec.md` with AC list
- `execution-plan.md` with Task list and code scope
- Implementation code exists; uncommitted changes can be reviewed before PR approval.

## Input

1. Read `proposal.md` goals/success criteria, `spec.md` ACs and verification mapping, applicable `design.md` decisions, and `execution-plan.md` Task list, code scope and existing findings. Read related validation/security artifacts when affected; honor lite's optional design.
2. Read actual implementation files, relevant diff and test/evidence inputs.
3. Read review templates from `templates/review/` as applicable checklists.

<!-- ODK:reference contracts/skill-guides/delivery/feedback.md -->
Read `contracts/skill-guides/delivery/feedback.md`. Review both implementation
and baseline completeness; route findings to their owning artifacts, record
dispositions in the existing plan and invalidate/reverify affected results.
<!-- /ODK:reference -->

## Steps

1. Review actual implementation files and the full relevant diff (including untracked files) against each AC. Inspect correctness, failure paths, tests and regressions. Use templates as checklists, not as a substitute for examining code. Do not commit merely to start review.

2. Challenge missing ACs, design deviations and verification assumptions as well as implementation bugs. Apply the feedback procedure: report cause/impact and file references, identify affected artifacts, and update the plan's problem dispositions. The authorized repair coordinator backfills the owning artifacts; a report-only explanation cannot close a real baseline deviation. Reuse evidence only for unchanged inputs; do not claim unexecuted checks passed.

3. If `design.md` contains `### DFX 故障模式处置`, check every disposition row referencing an AC against fault-injection/error-path evidence; a missing or happy-path-only verification is an unresolved deviation (archive blocks on non-Pass FM ACs). Record it via the review template's `## DFX 故障模式覆盖` section when written.

4. Return PASS only when required ACs/checks pass, blocking findings are resolved and affected artifact diffs have been reviewed against the final implementation. Otherwise return actionable findings with disposition IDs and remaining backfill/reverification. In the automatic handoff, the coordinator owns repairs, source-PR confirmation and the later design-docs reminder; do not ask a second publishing question here. Standalone review never authorizes a source or document push.

## Output

Write optional process evidence to `codespec/changes/<repo-name>/<proposal-id>/evidence/reviews/`.

Do not generate `reviews/` or `gates/` in the minimal archive root by default. These records are process evidence, not formal archive artifacts.

Report whether all ACs are covered and identify unresolved deviations. Optional review documents may be written when requested; a separate approval of a generated report is not required to run validation.

Keep document submission separate from review completion; source PR and design-docs publication each require the user's authorization.

When called by the automatic implementation handoff, return findings to that coordinator; it invokes `{{CMD_PREFIX}}validate` next. A standalone review can suggest validation but must not start source submission on its own.
