# Review, test and validation feedback

Use this procedure for findings from implementation tests, review, document
validation, CI and bridge tools, including standalone invocations. Read existing
targets in full under [document-updates](../router/document-updates.md) first.
Review reports are optional; the delivery artifacts must describe the final
agreed behavior, design, implementation and verification.

## Review both implementation and its baseline

Read the proposal's goals/success criteria, spec ACs, applicable design decisions,
plan and any relevant existing validation/security artifacts. Follow the effective
contract: lite does not acquire a mandatory design or new optional documents.
Inspect actual code/diff, tests and evidence. Check whether ACs themselves omit
required boundaries, failures or compatibility behavior; AC coverage alone is not
proof that the requirement is complete. Check design feasibility, state ownership,
interfaces and relevant risks against the implementation. Report concrete issues,
their effects, file/section references and a reproducible check or evidence gap.

## Route each finding by root cause

| Root cause | Update before claiming closure |
| --- | --- |
| Implementation violates an agreed AC | Fix code and a relevant regression test; update plan results. Preserve the AC rather than weakening it to fit the implementation. |
| Requirement/AC missing or inconsistent | Revise spec and verification mapping, then affected design/Tasks. Revise proposal only when goals, scope, success criteria or risk decisions change. |
| Design decision changed or proved incorrect | Revise design decisions/constraints and affected spec interfaces/errors/compatibility, then plan and code. A note only in a review report does not update the baseline. |
| Task scope, verification method or environment incorrect | Correct plan, commands and affected validation scenarios; rerun the checks that depended on that assumption. |

Update existing spec-for-validation/threat-model and other dependent artifacts
when affected. Preserve IDs, confirmed content and historical evidence. Record
why an assessed upstream artifact needs no change instead of editing every file.
Routine corrections within the authorized scope do not need another approval.
Obtain a decision only for a material scope/behavior change or unresolved design
choice not already authorized; keep that finding open meanwhile.

## Keep the disposition in execution-plan.md

When a finding exists, add/reuse one `## 问题闭环` table in the existing plan:

| 问题 ID | 来源 | 问题与根因 | 关联 AC/Task | 阻塞 | 受影响交付件 | 处理与回填 | 复验依据 | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

- Use stable `F-<digits>` IDs and the actual source (review/test/validate/CI).
  Link existing AC/Task IDs; an artifact-only issue may use `N/A（具体理由）`.
- `阻塞` is `是` or `否`. Missing required behavior, failed required checks and
  unresolved correctness/design deviations are blocking.
- `受影响交付件` lists existing change-relative file paths separated by `、` or
  commas, for example `spec.md、execution-plan.md`. Put section/AC references in
  `处理与回填`, with the actual changes and the reason unaffected baselines remain
  valid. Include the plan even for a code-only correction because its evidence
  changes. Do not invent a new document or mark it updated without reading it.
- `状态`: `Open` until repaired and rechecked; `Resolved` after backfill and
  verification; `Accepted` only for a nonblocking item with the user's existing
  acceptance, reason and scope recorded in `处理与回填`. A false positive can be
  Resolved with evidence explaining why no implementation change is needed.
- `复验依据` identifies the relevant command/test or manual check, outcome and
  evidence location for the current code/doc inputs and environment. A bare
  "Pass" is not enough. Optional review reports link these IDs rather than
  becoming a second disposition authority.

With no findings, omit the section or leave its header-only table; do not invent
a dummy "no issue" row. Older plans gain it on their first finding. An absent
table does not prove that a review was executed or that no issues exist.

## Invalidate, repair, reverify

When behavior, code, assumptions or verification inputs change, reopen affected
findings/Tasks, set affected ACs to Blocked (or Fail for an observed failure), and
set affected Verification `Final Status` to Blocked. Mark affected previous
approvals/review conclusions pending. Retain earlier Red/Verify output in
`Actual Result`; append the new result and its input/environment context.
Unchanged independent evidence can be reused.

For each required Verification row, `Final Status` is `Pass`, `Fail` or `Blocked`;
it describes whether the **expected result** was verified on the current inputs.
A negative test expecting an error may Pass. Historical TDD failures remain in
Actual Result without forcing a final Fail. Old plans must backfill the column
from valid evidence or rerun verification; never fill Pass solely to satisfy the
validator. Complete Tasks only after their required checks pass.

After repair, rerun affected tests and review the changed code **and artifact
diffs**, then rerun archive validation on the final document set. The handoff
coordinator owns this loop; called skills return findings without recursively
calling each other. Standalone operations return the same dispositions and
remaining work within the user's requested scope.

All required AC rows and Verification rows must Pass, all Tasks must be complete,
and blocking findings must be Resolved before archive/document submission. A
nonblocking Accepted item does not waive an AC, Task or required test. Structural
validation checks declared states/references; semantic review must confirm the
backfill and evidence actually support the conclusion.

For OpenSpec, reopen/correct native tasks or delta artifacts first, then refresh
the ODK projection and task_map under [native state ownership](../router/openspec-state.md).
Apply the feedback contract in every bridge output mode. PR/CI findings reopen
local readiness too; an existing PR does not authorize a merge or silently waive
the document backfill. Publishing still follows the existing user authorization.

## Synchronize PR-backed source before restoring publication readiness

After a post-PR review, CI, online test or hook causes a source repair, local
repair/test completion alone does not restore publication readiness. Return to
the source handoff's scoped commit/push/update steps: review and verify the fix,
commit only the authorized business source, tests and fixtures, push to the
existing PR's confirmed source branch, and query that same PR again. Reuse the
existing authorization for this PR; stop only the dependent publication when
the repair/push is outside that authorization or the push/query fails. Preserve
unrelated user changes and codespec documents rather than sweeping them in.

Query the actual PR host for its current full source-head SHA, and fetch that
commit into the business checkout if necessary. Before refreshing metadata and
again before copying a PR-backed document bundle, execute the installed check:

```sh
python3 runtime/executables/lib/odk_source_state.py \
  --repo <business-worktree-root> --published-head <fresh-PR-source-SHA> \
  --scope <reviewed-source-file> --scope <reviewed-test-file>
```

Source checkout entry: `scripts/lib/odk_source_state.py`. Pass every individual
reviewed business source/test/fixture path relative to that repository, including
new/deleted files, using the actual reviewed diff and plan code mapping. Do not
narrow the scope to obtain a passing result. Exclude codespec and unrelated user
files, and do not rely on those unrelated changes as verification evidence. Check
each changed repository against its own actual PR head. An empty scope is an
error, not evidence of publication.

Require exit 0 and `ready=true`: business HEAD must equal the freshly queried
head, the scoped index/worktree must have no unpublished changes (including new
or ignored source), and source blob contents/modes must match that commit. The
check is read-only and offline; it cannot authenticate an invented/stale SHA or
replace querying the actual host, review or tests. SHA equality alone is not enough
when the worktree still contains the fix. On failure, keep publication pending;
do not mark metadata fresh or submit the document bundle.

On a new source head, invalidate affected post-review/CI/online-test conclusions
and rerun the applicable checks under their existing authorization. Do not reuse
results for the old source version. Record the confirmed head, source-check result
and revalidation in the existing plan's evidence/dispositions, then refresh
metadata from that same PR. If source changes again, repeat the check and affected
verification before publication. Standalone submission with genuinely no source
PR retains the existing `pull_requests: []` mode; unrelated historical metadata
records must not be fabricated or relabeled as this current PR.
