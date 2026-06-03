# Submit Scope Contract

Each Chromium issue must produce one GitCode Issue, one commit, one fork branch,
and one PR. Batch merge/build may happen in-place, but submit is split per
issue.

Allowed submit files for the current issue are the union of:

- `modified_files[]`
- `06_merge_result.final_changed_files[]`
- `06_merge_result.local_adaptations[]`
- `10_build_fix.compile_fix_files[]`
- `10_build_fix.local_adaptations[]`

Generate the file set with:

```bash
node skills/arkweb-security-patch-gitcode-pr/scripts/compute_submit_scope.mjs \
  --merge-result issues/<issue_id>/06_merge_result.json \
  --build-fix issues/<issue_id>/10_build_fix.json > <submit_scope_json>
```

Before commit, stage only the files in this JSON and validate:

```bash
node skills/arkweb-security-patch-gitcode-pr/scripts/preflight_commit_scope.mjs \
  --repo <target-git-repo> \
  --scope <submit_scope_json>
```

Never use `git add -A`, `git add .`, `git add -u`, or `git commit -a`.
Never submit SDK, toolchain, build outputs, archives, `.ace-outputs`, `src/out`,
temporary patches, or unrelated dirty files.

Push range baseline:

- Use the manifest/upstream baseline as the submit range base:
  `<manifest_remote>/<targetBranch>..HEAD`, for example `tpc/master..HEAD`.
- The personal fork remote is only the push destination. Do not use
  `<fork_remote>/<targetBranch>..HEAD`, for example `personal/master..HEAD`, to
  decide whether the current patch branch is a minimal issue submission.
- If the fork target branch is stale or unrelated, record it as fork sync state;
  it is not a reason to mark every ready issue as `submit_failed` when the
  manifest/upstream range is small and the staged diff matches the issue scope.
- For each issue, the allowed commit range after creating the issue commit is
  one new commit on top of the manifest/upstream baseline, unless a local
  adaptation was intentionally split and documented in the same issue result.

If `semantic_landed` is false or blockers remain, stop the current issue. Build
adaptation files may be submitted only when the original patch semantics are
already landed and the adaptation is recorded in the issue artifacts.

Submit queue contains only current ready active issues that passed risk
assessment and satisfy the build gate. Do not create commits, branches, GitCode
Issues, or PRs for `terminal_failed`, `deferred_for_archive`,
`pending_current_stage`, overlap non-winners, or issues that have not passed the
build/risk gate.
