# Patch Landing Contract

## Success Conditions

An issue may be `ready_for_next` only when:

- `blockers` is empty
- one of these is true:
  - `apply_ok=true`
  - `manual_applied=true`
  - `semantic_landed=true`
- `final_changed_files[]` contains at least one issue-scoped changed file

`manual_attempted=true` means only that the manual path was attempted. It is not success by itself.

Manual repair success is success. If minimal manual writing lands the upstream security/functional semantics in allowed files, write:

```json
{
  "manual_attempted": true,
  "manual_applied": true,
  "manual_rewrite": true,
  "semantic_landed": true,
  "blockers": []
}
```

If the manual path ran but wrote no issue file or semantic landing is uncertain, write:

```json
{
  "manual_attempted": true,
  "manual_applied": false
}
```

Keep the current blocker and do not mark `ready_for_next`.

## Issue Scoped Diff

Use `scripts/issue_diff_scope.mjs` to compute issue-scoped changes:

```bash
node skills/arkweb-security-patch-merge/scripts/issue_diff_scope.mjs \
  --repo <target-git-repo> \
  --merge-result <issues/{issue_id}/06_merge_result.json>
```

The allowed set is built from:

- `modified_files[]`
- `patch_normalization[].diff_paths[]`
- `local_adaptations[]`
- optional build-fix `compile_fix_files[]`

Do not copy global `git diff --name-status` into every issue.

## Validate Results

Use `scripts/validate_merge_result.mjs` before writing pass/ready status:

```bash
node skills/arkweb-security-patch-merge/scripts/validate_merge_result.mjs \
  <issues/{issue_id}/06_merge_result.json> \
  --batch-status <batch_status.json> \
  --issue-id <issue_id>
```

Treat validation errors as blockers. Typical invalid states:

- `ready_for_next` with blockers
- `ready_for_next` from `manual_attempted` only
- landed state with empty `final_changed_files`
- `final_changed_files` polluted by unrelated global diff such as toolchain deletions
