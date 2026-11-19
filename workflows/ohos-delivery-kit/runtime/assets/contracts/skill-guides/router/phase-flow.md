# Phase hooks and next-step reminders

This protocol applies to every ODK phase, base and bridge commands, nested
phases and the delivery handoff. Read it before phase work and apply it again
before every completion, approval request, blocked result or other pause.
The coordinator owns hooks and user-facing reminders; delegated reviewers
return results to it without starting another phase flow.
This protocol refines phase-local fixed next-command suggestions: insert the
actual pending hooks and gates rather than copying a bare command verbatim.

## Persist and restore execution state

Read [workflow-state.md](workflow-state.md) before phase work. Use its packaged
`lib/odk_workflow.py` commands to inspect/prepare the invocation, checkpoint every
pre-hook/body/post-hook boundary, restore the first unfinished step after a new
session, and invalidate changed inputs. The coordinator must persist this state;
conversation context and `.sessions.json` are not execution checkpoints.
Use its guarded patch/create commands for ODK document writes.

## Resolve the actual flow

Use the same installation and executable root as the resource check. After the
entry's update check and resource/config loading, run the installed
`lib/odk_repository.py --phase-hooks <phase-or-odk-command>` (source checkout:
`python3 scripts/lib/odk_repository.py --phase-hooks spec`). This read-only JSON
describes `steps` in execution order and reports `user_config_path`. It never
executes hooks or grants approval. Reload configuration at each new phase;
keep the selected hook list in its durable checkpoint while that invocation is
paused so completed hooks are not repeated. A requested config change invalidates
affected work; reconcile it through the checkpoint protocol before continuing.

The flat string keys are `<phase>_pre_hook` and `<phase>_post_hook`. Each value
is an ordered, space-separated list of skill names, using the same semantics as
configured review skills. Missing keys, `""` and whitespace-only values insert
no hook steps. Do not show empty hook slots, ask about them, or offer to run them.
Defaults live in `odk_config.yaml`; users customize its sibling
`odk_config_ext.yaml`, with the normal per-key override/empty-value rules.

Canonical phases and their normal continuation:

| Phase key | Action and continuation after its post_hook |
| --- | --- |
| `init` | Initialize archive → brainstorm for unresolved decisions, otherwise propose |
| `brainstorm` | Close decisions → return to its caller; standalone → init if needed, otherwise propose |
| `link_proposal` | Bind draft → resume the earliest unfinished phase |
| `propose` | Proposal → spec |
| `spec` | Specification → design, or plan for lite when design is unnecessary |
| `upgrade_api_chain` | Upgrade an explicitly selected legacy API chain → resume the earliest unfinished or invalidated phase |
| `spec_for_validation` | Bypass scenarios → return to caller or earliest unfinished main phase |
| `design` | Architecture → plan |
| `fmea` | Fault analysis → return to design caller, or resume main flow when standalone |
| `security_threat_model` | Threat analysis → return to design caller, or resume main flow when standalone |
| `plan` | Execution plan → implement after required approval/implementation authorization |
| `implement` | All Tasks complete → configured reviews, then validate through the handoff |
| `device_prepare` | Applicable, confirmed device preparation → build/test at the plan's recorded position |
| `build` | One actual build → its next verification step in the approved plan |
| `test` | One actual test action → remaining tests, then task_review |
| `task_review` | Task verdict → repair on findings, otherwise mark Task Done and continue Tasks/handoff |
| `review` | Whole-change review → repair on findings, otherwise validate or return to coordinator |
| `validate` | Validation → fix issues or resume the caller; after pre-PR archive success remind about source CR/MR/PR |
| `source_cr_mr_pr` | Confirm remote source CR/MR/PR → post-commit reviews, CI, online tests, custom post-submission hooks |
| `ci` | Applicable CI action/result → online tests or the next applicable handoff step |
| `online_test` | Applicable online-test action/result → custom post-submission hooks, then metadata |
| `metadata` | Verify local metadata → separate design-docs submission choice |
| `submit_design_docs` | Verify document CR/MR/PR → finish remaining configured hooks and report completion |

Execution mode (see `contracts/skill-guides/delivery/execution-mode.md`) qualifies the
implement → validate chain recorded in the plan's `## 执行模式`: 全自动 advances each
configured gate on default values without re-asking confirmed choices; 逐步实现 skips
task-review dispatch with the recorded marker instead of verdict evidence. Neither mode
waives the explicit confirmations required by build-products.md and
device-version.md; 逐步实现 replaces only the task-review evidence requirement (marker
instead of verdict), leaving every other gate unchanged.

The effective delivery level, actual artifacts, pending findings, caller and
user-authorized endpoint select the next applicable action. The table is not a
mandatory checklist: skip inapplicable phases together with their hooks, and
return from bypass work to its actual caller. Configuration alone does not enable
a skipped phase. `ci_trigger: none` and `online_test_trigger: none` skip the
corresponding phase and hooks; a user declining the action does the same.

Single-phase bridge aliases share their base phase hooks: sp-plan/ms-tasks →
plan; sp-implement/ops-apply → implement; sp-review/ms-validation → review;
ms-proposal → propose; ms-delta-spec → spec; ms-delta-design → design.
`odk-sp-brainstorm` expands to brainstorm → propose → spec → design;
`odk-ops-propose` expands to propose → spec → design → plan. Wrap each constituent
phase, rather than running all pre-hooks before a bulk generation and all
post-hooks afterward. With configured hooks, use native artifact-by-artifact
operations that preserve the bridge's state. If those boundaries are unavailable,
report and use its declared base fallback; if no valid fallback exists, stop and
show the next recovery action. Do not claim hook order was honored around a
single bulk call. Nested base/bridge calls share the
same invocation and run each hook once. Do not restart a phase's hooks when its
hook skill calls back into that same phase; stop a circular hook dependency and
report the configuration key to repair.

## Execute hooks at their boundaries

For every applicable action use this sequence:

1. Resolve the action's prerequisites and existing approval/authorization gates.
   If waiting, show the required user action and the configured hooks that will
   follow it. Do not run the next phase's pre_hook before its gate is satisfied.
2. Invoke the current phase's pre_hook skills in configured order. Before each
   invocation follow [configured-skills.md](configured-skills.md), using its
   exact config key for installation hints. Pass the current change, phase,
   Task/action identity when applicable, and relevant artifact/evidence paths or
   confirmed CR/MR/PR URL. Configuration names skills, not shell commands.
3. Execute the phase body and required checks. A failed/blocked body leaves
   post_hook pending; post_hook is a success hook, not a finally/cleanup handler.
4. Invoke post_hook skills in order after successful phase work and before
   announcing phase completion, requesting artifact approval or handing off.
   Only after all applicable hooks pass is this invocation complete.
5. Emit the reminder below, then continue automatically within existing
   authorization or wait for the stated user action. Automatic transitions
   still show the next step before starting it.

A hook must report success or actionable findings. Failure, missing skill,
pending installation/restart, cancellation or an indeterminate result stops
dependent work. Name the exact hook and key, its reason, and how to resolve and
resume it. Do not skip it, mark the parent complete, run later hooks, or advance
to the next phase. Use the normal feedback procedure for hook findings.

Persist the phase/action identity, selected hooks, completed hook indices, evidence
and current pending step in `.workflow.json` using the workflow-state protocol.
Keep conversation summaries as a convenience, never the authority. Resume at the
first unfinished step; do not rerun successful hooks merely because the user
answered an approval question or a bridge returned. Changed code/artifacts or
hook inputs invalidate affected results and require rechecking those hooks.
Repeated build/test/task-review actions each have their own invocation; retries
after repaired inputs are new invocations. When context/evidence is unavailable,
recover it before repeating an action with side effects; never invent success.

For delivery, wrap the source create/update-and-confirm action with
`source_cr_mr_pr` hooks; then preserve the existing post_commit_reviews → CI →
online tests → post_cr_mr_pr_hooks → metadata → design-docs order. Run
`implement_post_hook` before entering automatic review/validation, and
`validate_post_hook` before the source submission reminder. `metadata` covers
metadata creation/verification, including standalone document submission;
`submit_design_docs_post_hook` runs after the actual document PR is verified.
Wrap each actual device/build/test action in implementation, including bridge
implementation, at its recorded plan position. Existing review/submission hooks
remain distinct ordered actions; include any pending ones in next-step reminders.

`odk-upgrade-api-chain` resolves to the standalone `upgrade_api_chain` phase.
Run it only when the upgrade command is invoked; do not insert migration into a
normal new-change flow. Its hooks use `upgrade_api_chain_pre_hook` and
`upgrade_api_chain_post_hook`, independently of spec hooks. Missing facts keep
the upgrade body pending; after successful migration, resume the first phase
that the report identifies as unfinished or invalidated.

## Always show the next step

Every user-facing phase completion or pause MUST contain a clear `下一步：`
reminder (or its equivalent in the conversation language). A phase result,
question, error, missing prerequisite, declined submission or restart reminder
alone is insufficient. State the **first unfinished action**, the concrete user
input/repair/command needed when waiting, and the immediate continuation. When
configured hooks lie on that continuation, show their actual names and order as
`<phase>.pre_hook → <skill>` / `<phase>.post_hook → <skill>`, including multiple
skills where configured. Do not replace them with a vague “run hooks”.

- Successful body, post_hook pending: next is that post_hook, then the phase
  approval/continuation. Do not announce the phase as fully completed yet.
- Successful phase: next is required document approval or the next applicable
  action, including that action's configured pre_hook before its body and its
  post_hook afterward. If continuing automatically, say it is being started.
- Waiting for approval, product/device choice, a missing dependency, source-PR
  instruction, CI/test choice or design-docs confirmation: next is the specific
  answer/fix, followed by the actual configured hook/action chain. Include this
  reminder in the same message as the question, even when using an input tool.
- Blocked/failed: next is to resolve the named blocker and resume that exact
  pending phase/hook; never suggest advancing as though it passed.
- Nested task/bypass/review/validate completion: next is the coordinator's
  pending action, rather than starting a second independent handoff.
- User defers or limits the endpoint: report what remains and how to resume;
  do not execute beyond the authorized scope or describe deferred work as done.

Examples (display only the configured parts):

```text
下一步：确认 spec.md；确认后执行 design.pre_hook → check-input，再运行 odk-design，随后执行 design.post_hook → check-output。
下一步：修复 spec.post_hook → check-spec 的失败项，再恢复该 hook；通过后确认 spec.md，然后进入 design。
下一步：明确是否提交源码 PR；触发提交后执行 source_cr_mr_pr.pre_hook → check-branch，再创建或更新 PR。
下一步：重启当前客户端以加载 check-input，然后恢复 design.pre_hook → check-input。
```

Omit the reminder only when **all applicable workflow actions and configured
hooks are complete**, with no outstanding confirmation, blocker, deferred
submission or external result required by this change. A single phase passing,
ending the current request, reaching the user's limited endpoint, or submitting
a PR with a pending post_hook does not mean the full workflow is complete.
Completion never implies merging a source or document CR/MR/PR.
