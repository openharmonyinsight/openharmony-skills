# Batch State Contract

Batch mode must run in the current target git subrepo. Do not create or switch to git worktrees.

## Planning

Use `scripts/plan_batch.mjs` before applying patches:

```bash
node skills/arkweb-security-patch-merge/scripts/plan_batch.mjs \
  --archive-dir <archive-run-dir> \
  --project-root <context.codebase> \
  --output-dir <context.projectRoot>/.ace-outputs/<runId>
```

The script writes:

- `00_batch_plan.json`
- `00_batch_plan.md`

The plan is based on `modified_files[]` and normalized patch `diff_paths[]`.

## Overlap Rules

- Track `file -> issue_ids[]`.
- For each duplicated file, choose the numeric smallest issue id as `winner_issue_id`.
- Different duplicated file groups choose winners independently.
- If an issue is a loser in any duplicated file group, the whole issue exits `active_batch`.
- Losers become `deferred_for_archive` / `terminal_failed` and do not enter conflict resolution, build, or submit in this run.

`active_batch` is:

```text
issues without duplicate files + duplicated-file winners - duplicated-file losers
```

## Stage Status

Per issue status must be one of:

- `ready_for_next`
- `pending_current_stage`
- `terminal_failed`
- `deferred_for_archive`

Top-level verdict:

- `pass`: no `pending_current_stage` and at least one `ready_for_next`
- `conditional_pass`: at least one issue still needs current-stage conflict/build-fix work
- `fail`: no issue can continue, or the whole batch has unrecoverable infrastructure failure

Ready issues must wait for the unified stage exit. They cannot jump ahead while other issues remain pending in the same stage.
