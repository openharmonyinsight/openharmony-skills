# Implementation quality decisions

Use this guide while choosing a code Task's implementation, before marking it
Done, and during code-quality review. Inspect the relevant code and diff within
the authorized scope. A quality check is required; a rewrite is a decision.

## Check the affected paths

Read [the change-impact guide](change-impact.md) before editing a code Task and
when reviewing its completion. Detect usable LSP/AST capabilities for the actual
project; supplement them with the guide's plan, search, TDD and review checks.
Without usable semantic tools, use that same fallback without adding dependencies.
Carry the affected paths, evidence and unresolved checks in Task/review handoffs.

## Inspect the choice in context

- Establish the language/runtime version, applicable repository conventions and
  nearby patterns from the Task's declared context. Prefer an existing suitable
  helper or idiom; do not copy an inefficient pattern merely because it exists.
- For a new or changed public symbol (installed header or exported API), confirm
  the symbol is exported through the repository's visibility/version files
  (`.map`/`.symdef`/`__attribute__((visibility("default")))`) and that error
  handling follows the neighbors' convention (e.g. `CHECK_ENV`/`CHECK_ARG` +
  `napi_set_last_error` + `HILOG_*`, rather than a bare `RETURN_STATUS_IF_FALSE`),
  and that a new scope/handle reuses the repository's ownership idiom (RAII guard
  vs manual open/close).
- Look for hard-to-follow expressions, avoidable duplication, repeated work,
  growing-data copies, allocations in loops, and error/ownership paths made
  harder by the chosen representation. Focus on risks present in this change.
- For potential cost issues, distinguish fixed expressions from accumulating
  loops, bounded small input from growing input, and startup/cold code from
  frequent calls or a demonstrated hot path. Use known workload constraints;
  state a missing fact when it matters rather than inventing it.
- A long string expression is a review signal, not a universal defect. Consider
  compiler/runtime behavior and readability before choosing concatenation,
  formatting, append/join or a builder. Do not impose a fragment-count ban,
  require raw buffers, or assume a language has a particular buffer API.

## Decide and verify

- **Keep** when the code is suitable for its constraints. Explain a disputed
  choice with the relevant code, repository convention or workload fact.
- **Change** when a concrete readability, correctness, resource or maintenance
  problem justifies it. Preserve behavior and scope, and rerun affected tests.
  Buffer-based rewrites still need appropriate bounds, encoding and ownership.
- **Needs evidence** when a material performance decision depends on unknown
  workload or runtime behavior. Name the missing fact or a useful comparison.
  Use analytical allocation/copy/complexity reasoning where it is sufficient;
  measure when claiming actual speed or memory gains. Do not benchmark every
  concatenation or block unrelated work on speculative optimization.

Use the repository's existing lint/test commands when applicable. A language
check can identify a known inefficient pattern; a warning or the number of plus
operators does not establish the best replacement. Report unavailable or
unexecuted checks without claiming they passed or silently adding dependencies.

Record material risks, choices and supporting file/command references briefly in
the Task's existing `Actual Result`; do not generate a separate quality report
for every Task. Review may use the existing code-quality template. Unresolved
blocking issues use [the feedback procedure](feedback.md); changed design or
acceptance constraints still belong in their owning artifacts.
Apply [the specification boundary](../spec/contract-boundary.md): a better
implementation with the same contract leaves spec unchanged, while affected
verification is rerun and recorded in the plan/evidence.

## Review roles and completion

- **Implementer:** after verification, self-review the actual diff against the
  Task's requirements and the choices above. Repair issues within scope before
  reporting. Hand back the changed-file list or complete diff range, verification
  commands/results and remaining concerns. A passing test or an implementer's
  `Done` report is input to review, not the coordinator's acceptance.
- **Coordinator:** own review assignment and acceptance. For delegated code Tasks, use
  the execution workflow's task reviewer; for R1/R2 Tasks under
  [the Task review contract](task-review.md), use its fixed one-seat or three-seat
  review instead of adding seats beyond that contract. Inline execution keeps
  per-Task self-review and the configured final review, without requiring a new
  reviewer for every small Task. Implementers and assigned reviewers do not
  dispatch additional reviewers on their own.
- **Reviewer:** when coordinating an ODK review, use one fresh-context reviewer
  when delegation is available and permitted. An already assigned reviewer does
  the review itself; without permitted delegation, make a separate pass and
  disclose self-review. Pass requirements, relevant constraints, the complete
  relevant diff (including uncommitted/untracked files) and raw test evidence by
  path. Form a code-based judgment before considering a preferred verdict;
  author explanations remain claims. Review is read-only on the source and plan.
  Return **spec compliance** and **code quality** as separate conclusions, plus
  concrete findings, file/line evidence and checks that could not be completed.
  One reviewer may assess both dimensions; separate reports are optional.
  A Task-level reviewer under `task-review.md` is one of the fixed seats and never
  dispatches another reviewer.
- **Repair and re-review:** the coordinator routes findings through the existing
  feedback procedure and returns code fixes to the implementer. After affected
  checks run, review the fix and affected artifact diffs against the open
  findings; include new breakage in that fix's scope. Reuse unchanged evidence;
  run an additional focused check when a specific doubt remains. Neither
  self-review nor green functional tests replace a required review conclusion.
  Keep blocking findings and affected completion states open until repaired and
  reverified. A native workflow's deferred/parked finding does not waive an ODK
  blocking requirement. If progress stops, report the unresolved cause under the
  feedback procedure rather than silently accepting it or repeating indefinitely.
- **Change closeout:** after Task checks, the existing configured handoff reviews
  the whole implemented change for cross-Task consistency and then validates it.
  Task approvals do not replace that final review. Reuse its reviewer instead of
  scheduling a duplicate final review, and honor explicit review-hook settings
  and user limits. Review completion does not itself authorize publishing.

## Reassess without following a suggested answer

Functional tests prove the exercised behavior, not readability, language idiom
or performance. Review those separately. A question such as "would a buffer be
better?" is a reason to re-examine the code, not evidence that the answer is yes.
If the judgment changes, identify the newly considered fact or reasoning; do not
invent a measurement. Retain a supported judgment or explain uncertainty when
appropriate. Honor an explicit style choice as a preference without presenting
it as a proven optimization.
