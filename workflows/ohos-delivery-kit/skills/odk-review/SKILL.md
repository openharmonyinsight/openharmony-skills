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

## Phase flow and next step

<!-- ODK:reference contracts/skill-guides/router/phase-flow.md -->
Before phase work, read `contracts/skill-guides/router/phase-flow.md` and apply
its configured pre_hook/post_hook order. At every completion or pause, show
the next pending action and configured hooks; omit the reminder only when
the entire applicable workflow is complete. The coordinator owns this flow.
<!-- /ODK:reference -->

<!-- ODK:reference contracts/skill-guides/router/delivery-levels.md -->
Read `contracts/skill-guides/router/delivery-levels.md` and use the effective
contract. It takes precedence over standard-only artifact lists below; native
OpenSpec schemas remain standard/critical and lite uses the base flow.
<!-- /ODK:reference -->

## Prerequisites

- `spec.md` with AC list
- `execution-plan.md` with Task list and code scope
- `design.md` must exist under `standard` and `critical` delivery levels; `lite` may omit it (honor lite's optional design, consistent with the validator gate)
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

1. Review actual implementation files and the full relevant diff (including untracked files) against each AC. Inspect correctness, failure paths, tests and regressions. For public-API/ABI changes, additionally confirm symbol export/visibility files are updated (`.map`/`.symdef`), error-code/return conventions match the neighbors, new scopes/handles reuse the repository's ownership idiom, and the single choke point for cross-cutting side effects is not bypassed by scattered gating. Use templates as checklists, not as a substitute for examining code. Do not commit merely to start review.

   Before forming any whole-change conclusion, read every R1/R2 Task's
   `evidence/reviews/task-<n>/verdict.md`. A missing verdict, a non-`PASS` verdict
   or `blocking_findings > 0` makes the whole-change result non-PASS, regardless of
   other evidence. Task verdicts do not cover cross-Task contract consistency or
   final integration; keep those checks in this review.

   <!-- ODK:reference contracts/skill-guides/delivery/implementation-quality.md -->
   Read `contracts/skill-guides/delivery/implementation-quality.md` and inspect
   applicable implementation choices as well as AC coverage. Treat the author's
   rationale and a user's proposed optimization as claims to check against code,
   workload and evidence. Passing tests alone do not establish implementation
   quality or a performance improvement.
   Follow its affected-path check, including relevant callers and unchanged
   implementations. Return any requirement that cannot be verified from the diff
   to the coordinator for resolution before accepting the affected completion.
   <!-- /ODK:reference -->

   Follow the guide's review roles once: the coordinator assigns one fresh,
   read-only reviewer when delegation is available and permitted; an already
   assigned reviewer performs the review itself without spawning another.
   Otherwise make a separate pass and disclose self-review. Pass requirements,
   constraints, the complete relevant diff and raw evidence by path; assess the
   code before the author's preferred verdict. Return separate spec-compliance
   and code-quality conclusions with findings and verification gaps. Do not
   claim independence or require a new tool merely to complete ordinary review.

   Form an independent judgment from the code, diff and raw test evidence; the
   implementer's `Done` report and recorded `Pass` entries are inputs to
   challenge, not conclusions to accept. Author explanations remain claims until
   the code and test output support them. Where self-review is the only option,
   name that mode explicitly in the output so the coordinator can weigh the
   result accordingly.

2. Challenge missing ACs, design deviations and verification assumptions as well as implementation bugs. Apply the feedback procedure and its specification boundary: assess all spec sections for internal design/test implementation details, and distinguish a real contract gap from a changed implementation. Preserve an unchanged spec while requiring affected verification again. Report cause/impact and file references, identify affected artifacts, and return dispositions for the coordinator to record in the plan. The authorized repair coordinator backfills the owning artifacts; a report-only explanation cannot close a real baseline deviation. Reuse evidence only for unchanged inputs; do not claim unexecuted checks passed.

3. **Verification-before-completion check**: before forming any readiness conclusion, challenge every AC's completion claim against concrete evidence. For each AC, identify its implementing Tasks and their applicable verification methods:
   - Locate the actual verification evidence recorded in `execution-plan.md` `Actual Result`. For Tasks using TDD, check the recorded Red failure evidence and passing Verify/Green output. A `Pass` label without supporting evidence is an unresolved evidence gap.
   - For Tasks explicitly using the permitted TDD degradation rule in `{{CMD_PREFIX}}implement`, verify the `TDD degraded: <reason>` declaration is eligible and inspect the reproducible manual check steps, relevant inputs/environment, actual results and evidence location. Do not require Red/Green output for these Tasks. Business-logic changes remain ineligible for degradation, including those delivered via config or data files.
   - Confirm the test or manual check exercises the AC's observable behavior, not just a happy path. An AC requiring a failure/error response must have verification that actually triggered and verified that failure path.
   - Confirm completion evidence applies to the current relevant code, documents and other inputs. Rerun affected checks when those inputs change; preserve historical Red evidence and reuse unchanged independent evidence.
   - For ACs whose completion cannot be confirmed from diff + evidence alone, record a concrete evidence gap finding; do not assume coverage from code presence.

4. If `design.md` contains `### DFX 故障模式处置`, check every disposition row referencing an AC against fault-injection/error-path evidence; a missing or happy-path-only verification is an unresolved deviation (archive blocks on non-Pass FM ACs). Record it via the review template's `## DFX 故障模式覆盖` section when written.

5. Return PASS only when both spec compliance and code quality are approved, all AC completion claims are supported by concrete evidence for their applicable verification methods (Step 3), required ACs/checks pass, blocking findings are resolved and affected artifact diffs have been reviewed against the final implementation. Otherwise return actionable findings with disposition IDs and remaining backfill/reverification. Keep the review read-only; return findings to the repair coordinator for plan backfill and fixes, then review the affected fix scope. In the automatic handoff, the coordinator owns repairs, source-PR confirmation and the later design-docs reminder; do not ask a second publishing question here. Standalone review never authorizes a source or document push.

## Output

Write optional process evidence to `codespec/changes/<repo-name>/<proposal-id>/evidence/reviews/`.

Do not generate `reviews/` or `gates/` in the minimal archive root by default. These records are process evidence, not formal archive artifacts.

Report whether all ACs are covered and identify unresolved deviations. Optional review documents may be written when requested; a separate approval of a generated report is not required to run validation.

Keep document submission separate from review completion; source PR and design-docs publication each require the user's authorization.

When called by the automatic implementation handoff, return findings to that coordinator; it invokes `{{CMD_PREFIX}}validate` next. A standalone review can suggest validation but must not start source submission on its own.
