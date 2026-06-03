# Manual Landing Contract

Conflict resolution in this workflow means minimal equivalent manual landing
after `git apply` fails, lacks 3-way blobs, or sees context drift.

Success requires all of:

- changes are limited to `modified_files[]` plus explicitly recorded issue-local
  adaptation files
- issue-filtered diff is non-empty
- the upstream security or functional semantics are present
- `manual_applied=true` or `semantic_landed=true`
- current blockers are cleared

`manual_attempted=true` only means the manual path was tried. It is not success
unless `manual_applied=true` or `semantic_landed=true`.

When manual landing is skipped, write `manual_attempted=false` and a concrete
`manual_skip_reason`.

Do not carry old `patch_apply_failed:*`, `no_real_file_change`, or
`worktree_add_failed` blockers after a later successful manual landing.
