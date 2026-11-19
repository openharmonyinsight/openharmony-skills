# Durable workflow checkpoints

Every base/bridge entry and delivery action uses this protocol through
phase-flow.md. The coordinator calls `lib/odk_workflow.py` from the executable
directory selected by the resource check (source: `scripts/lib/odk_workflow.py`).
It owns `<change>/.workflow.json`; do not edit that file manually. Its stable
sibling lock serializes cooperating writers; temporary file, fsync and atomic
replacement publish complete checkpoints. Errors are blocking, never fail-open.
`.sessions.json` remains a call log and is not completion or approval evidence.
Checkpoint state, CLI JSON output, patch/verification JSON and native archive
evidence use UTF-8, independent of the host locale. Preserve that encoding when
preparing input files.

## Enter or resume

1. Resolve the existing change and read `status <change>` **before executing
   phase work or hooks**, including after a new session or client restart.
   Read the existing target documents using document-updates.md. Restore the
   actual pending action from the checkpoint, not the last conversational hint.
   For init, validate the requested identity first, reserve the change directory
   for checkpoint infrastructure, and prepare its invocation before hooks or
   seeding proposal.md. Use the confirmed slug/release as its stable action ID.
   An empty directory with an init checkpoint is resumable, not a reason to
   delete it or overwrite another change.
2. Resolve delivery level, dependencies, current user authorization and hook
   configuration. Call `prepare` for one applicable canonical phase. Composite
   bridges prepare constituent phases separately. Use a stable `--action` for
   Task/build/test/review identities, such as `TASK-2`; its key is
   `implement:TASK-2`. Nested aliases share the caller's invocation instead of
   preparing duplicate hook runs. Separate actual build/test actions have their
   own action IDs; a repair retry keeps the identity and records another attempt.
3. Declare every relevant fixed upstream file with `--input`, required artifact
   with `--output`, and mutable source/test file with `--watch`. Declare a native
   Markdown task checklist with `--native-task` (which also adds it to watch).
   Inputs must exist and cannot also be mutable outputs. Watched files may be
   created or deleted. Paths are relative to the change directory; input/watch
   paths may reach business source files outside it. Enumerate actual files,
   including relevant configuration/build inputs; do not use directories or
   assume a changed file outside the declared set will be detected.
4. Add `--depends-on <key>` for each already checkpointed upstream invocation;
   it must be current and succeeded. Do not depend on a still-running caller.
   For an older change with no upstream checkpoints, read and validate the actual
   upstream documents and declare them as inputs. Missing checkpoints are
   `untracked`, not failure and never proof of completion. Do not regenerate
   existing artifacts or restart the whole chain merely to create checkpoints.
5. In interactive artifact phases use `--approval-required`. Record an actual
   confirmation with `approve --key ... --reference <message/evidence locator>`
   only after the phase and hooks succeed. In an explicitly authorized autonomous
   flow, perform the required self-checks without inventing a manual approval.
   The checkpoint records consent evidence; it never grants new authority or
   replaces the current user's endpoint, publication or device safeguards.

Example (all arguments after the script name):

```sh
status <change>
prepare <change> --phase spec --input proposal.md --output spec.md --approval-required
start <change> --key spec
snapshot <change> --key spec --token <returned-token>
# Save the JSON snapshot, then execute verification against those exact files.
finish <change> --key spec --token <returned-token> --result succeeded --verified-file <saved-json> --evidence evidence/workflow/spec-pre-0.txt
```

`prepare` returns configured pre-hooks, body and post-hooks in execution order,
with status, generation and the first unfinished step. Its exit code alone is
not readiness: inspect `status` and `stale_reasons`. Repeated preparation with
the same definition and unchanged files leaves the checkpoint unchanged.

## Record each boundary

- Immediately before **each** actual pre-hook, phase body or post-hook, call
  `start`. It marks only the first pending step running and returns an attempt
  token. Execute that returned step; never skip ahead or run successful hooks
  again just because the process or conversation changed.
- Save actual checker/hook output under a separate immutable evidence path for
  that step/attempt, such as `evidence/workflow/spec-1-post-0-attempt-2.txt`.
  After any intended edits, **before executing verification**, call
  `snapshot --key ... --token ...` and save its JSON to an immutable file.
  For a read-only checker hook, capture before invoking it. For an action that
  produces files, finish its edits first, then capture and verify the resulting
  files. Pass that same receipt as `--verified-file` to a successful `finish`.
  The receipt binds all declared inputs/outputs/watched files to this generation
  and attempt. Missing, partial, older-attempt or changed-file receipts are
  rejected under the writer lock. Never recapture after a failed comparison and
  reuse old test output: capture first and rerun the affected verification.
  After execution call `finish` with the returned token, `--result
  succeeded|failed|blocked`, `--evidence <file>` and an actionable `--reason`
  for failure/blocking. Success requires existing evidence and, from the body
  onward, all declared artifacts. It records file hashes, never infers semantic
  correctness from file presence. Artifact-body success additionally requires
  its existing phase validator; save that command's output as evidence.
- Only all steps succeeded, current file/evidence hashes, current upstream
  generations and any required approval make an invocation `succeeded`.
  Body success with a failed/pending post-hook is not phase completion.
  A post-hook that changes artifacts or watched source invalidates the earlier
  body verification: reconcile and prepare a new generation instead of accepting
  the old passing result. A human edit after a failed hook has the same effect.
  Reuse already completed Tasks from the plan only after checking their actual
  completion and verification evidence; do not replace Task status from logs.
- If execution stops while `running`, its outcome is **unknown**. Do not repeat
  a potentially completed remote/side-effect action. Reconcile actual files,
  returned URLs/device state and external results first. If it actually succeeded,
  record `finish` with its saved token and real evidence. If it needs retry, use
  `retry --key ... --reason <reconciliation> --evidence <proof>`; this retains
  earlier successful steps and makes only the interrupted/failed step pending.
  A fresh process can read the token from `status`; tokens identify attempts,
  not user authorization. Waiting for an external result remains blocked.

## Shared artifact backfill

Execution legitimately updates `execution-plan.md` that the planning phase
produced: Task status, checked Steps, actual files/results and verification
evidence. Initialization also yields a proposal stub that propose subsequently
fills. These authorized downstream edits need an explicit handoff rather than
silently refreshing every upstream result or reapproving an unchanged contract.

Declare the shared artifact as the downstream invocation's `--output` and name
its producer in `--depends-on`. Review the full diff and confirm that the
approved planning/behavior contract has not changed. Capture a verification
receipt and verify the updated artifact, then finish the **phase body** with
`--backfill-from <producer-key> --reason <actual backfill and unchanged contract>`.
For example, finish the implement body with `--backfill-from plan` when recording
Task completion. The flag is repeatable when more than one direct producer owns
the same artifact. Earlier Tasks that only observed the file are not producers;
avoid declaring the entire growing plan as an output of every completed Task.
For a coordinator wrapping multiple Tasks, preserve an immutable copy of the
approved planning contract under evidence before implementation. Nested Tasks
declare that copy as a fixed `--input` and watch their own mutable source files,
with separate verification evidence, while the coordinator
owns the growing execution-plan output and its dependency on `plan`. Task-to-Task
dependencies refer to their actual produced files/results, not the shared progress
log. After the Tasks, verify the completed plan and backfill through the caller's
implement-body finish. This avoids treating later Task progress as a change to
an earlier Task's verification inputs.

The helper requires a successful phase body, real evidence, a current verification
receipt, the declared direct dependency's original generation, and shared output
hashes matching the baseline observed at start. It atomically records old/new
hashes, downstream action, attempt, reason and evidence alongside both checkpoints.
It preserves the producer's generation and original approval reference, whose
original content hashes remain recorded. Changed upstream inputs, hook order,
evidence, unshared outputs or generations still invalidate the dependency.
The backfill evidence itself is also hash-checked on later queries; deletion or
modification makes the producer and dependent work stale.
Without this explicit flag, a shared file edit remains stale as before.

For a native task file outside the change, both producer and consumer declare
`--native-task <relative-path>` instead of trying to write it through `--output`.
Backfill and recovery can hand off its watched hash only when the task-definition
hash is unchanged. That hash normalizes only checklist `[ ]`/`[x]`/`[X]` markers
in lists, including nested/ordered lists, outside code fences, indented code and
HTML literal blocks. Indentation is relative to the containing list
item; tabs affect columns without rewriting source bytes. Names, IDs, descriptions,
ordering, commands and all other bytes remain significant. A changed/deleted
definition requires the normal planning/reapproval flow. Ordinary watched source
files never gain this exception. Edit native tasks through their native owner;
the helper only reads and records hashes outside the change directory.

If that phase body stops after only partial shared-file edits, reconcile it using
`retry --key ... --backfill-from <producer-key> --reason ... --evidence ...`.
This retains the original producer generation/output basis across attempts and
permits only that invocation to continue with its acknowledged partial outputs.
It does not accept the producer's new artifact globally: other consumers remain
blocked by its stale output. Finish the remaining body, capture before checking,
then use successful `finish --backfill-from ...` to accept the verified backfill.
Changed producer inputs/evidence/configuration/generation still block recovery;
missing reconciliation evidence also blocks the resumed invocation.

When a post-hook has failed, or later review finds a repair, its earlier successful
body must be verified again. After reconciling any running side effects, repeat
the same full `prepare` definition with `--restart-reason ...`,
`--backfill-from <producer-key>` and `--evidence <reconciliation-file>`.
This starts a new invocation generation and preserves the prior attempts/results
in history. Its pre-hooks and body may use only the scoped shared-artifact recovery;
the original producer stays stale to other consumers until a successful verified
body accepts the backfill. Original producer hashes/generations and all unrelated
dependencies must still match. It cannot change the invocation's declared scope.
If another repair is needed before acceptance, subsequent generations inherit
the unfinished step's original output/watched basis, never its unaccepted partial
file hashes. The basis advances only after a successful global backfill.
Finish the body with `--backfill-from ...`, then rerun its post-hooks. Reuse already
completed remote/device operations only after checking their actual results; a
new verification generation does not authorize repeating those side effects.

This is a coordinator-recorded contract-preservation decision, not automatic
semantic analysis. Do not use it to retain approval after changing requirements,
Task goals/dependencies/scope, verification commands or design decisions. Follow
the normal feedback and reapproval flow for those changes. Original planning
evidence continues to prove its original baseline; the recorded downstream
verification proves the backfilled artifact, without fabricating new user consent.

## Finalize a native archive

Native archive is a separate user-authorized OpenSpec operation. Before it,
capture native `all_done`, reconcile ODK and finish the applicable verification.
After a successful native archive, save the CLI's complete JSON result once in
an immutable file under the change, then run:

```sh
finalize-native-archive <change> --archive-result evidence/native-archive.json --reason "Verified authorized native archive"
```

This command does not execute archive, merge specs, publish or infer authority.
It verifies the existing binding's change/store/resolved root, final `all_done`
manifest/digest, all snapshot blobs, the archive result and the moved native
files. All declarations within that native workspace must match a captured task;
partial matches fail without updating checkpoints. Every checkpoint declaring
those tasks must already record the exact final task bytes; finalization cannot
replace missing verification with the native completion flag. Declare the
complete native task set before archive;
later consumers reuse those same logical paths. A new task declaration in the
already archived workspace is rejected rather than accepting its missing baseline
or reporting it finalized. Other live native workspaces do not affect idempotence.
A fresh capture records the resolved native root,
including an external selected store. Legacy default-store captures can use
their recorded project root; a selected-store capture without a resolved root
must be refreshed before archive rather than guessing its location.

After verification, one atomic state update binds the native logical paths to
their existing immutable task snapshots. Definitions, attempts, evidence,
generations, dependency links and approvals remain untouched. Pending work stays
pending, and unrelated stale inputs/evidence stay stale. Root `status` reports
`native_archives`; subsequent checks read the reported final snapshot instead
of invoking an already archived workspace. This lets review/validation and the
separate document-delivery flow continue without reapproving the same plan.

All snapshot/manifest/binding/archive-result evidence remains hash-checked.
Tampering or recreating the original native workspace makes the affected chain
stale. Repeated finalization with the same intact proof is idempotent. The moved
native archive directory can later be relocated or removed: its verified final
capture remains the historical input. Do not use finalization for a plain task
deletion, a different archive, changed task bytes or a reopened native change.
Those require their actual owner/reconciliation flow, never a fabricated result.

## Changed inputs and safe recovery

`status` compares fixed inputs, tracked artifacts/source files, successful-step
evidence, hook order and dependency generations. Any mismatch reports `stale`;
`start` and `approve` refuse it. Re-read changed content, preserve human edits,
identify affected dependents and verify any interrupted side effects. Then call
the same `prepare` with the full current file/dependency set and
`--restart-reason <what changed and was reconciled>`. This creates a new
generation with pending steps and retains the previous generation and attempt
history. A running attempt must be reconciled through `finish`/`retry` first.
Only affected invocations and their dependents need rechecking; unchanged
independent invocations remain usable. Never delete artifacts or the checkpoint
to make stale results appear current.
Dependency results are cached only within one top-level query. A later query
always rereads files/configuration, so the cache cannot hide new changes.

The checkpoint stores relative paths. Moving the entire change directory (for
example draft → formal proposal ID) retains progress when referenced files have
the same relative paths and contents. Do not edit its historical paths during
linking; if an actual relative input path changes, reconcile that invocation.

No saved state can reconstruct evidence that was never recorded. On old changes,
validate existing artifacts, recover real approval/completion evidence and
checkpoint the verified work. Ask only for confirmations that cannot be recovered;
do not mark old work successful merely because documents or session entries exist.

## Guard document writes

For every ODK artifact edit, obtain its SHA-256 with
`fingerprint <change> --target <relative-file>` after reading its full contents.
Write a JSON list of unique `{"old": "existing fragment", "new": "replacement"}`
edits to a temporary file, then call
`patch <change> --target <relative-file> --expected <sha256> --edits-file <file>`.
It preserves other bytes and file permissions, rejects whole-document replacement
and ambiguous fragments, and refuses a changed baseline. Reread and merge after
rejection; never bypass it with truncate/copy/full-template replacement. Review
the resulting diff for lost human decisions, IDs or evidence.

For a missing artifact use
`create <change> --target <relative-file> --content-file <file>`; it publishes
atomically and cannot replace an existing file. These commands operate only
inside the selected change directory and reject symlink targets. Native bridge
files remain under their owner's supported edit API and require the same
read-before-edit and baseline reconciliation rules. Watch their actual files.
All cooperating ODK writers use this helper's lock. An unrelated external editor
does not honor that lock; pause concurrent external writes while publishing a
patch. Hash rechecks catch edits observed before publication but are not an
OS-level transaction with arbitrary external editors.
