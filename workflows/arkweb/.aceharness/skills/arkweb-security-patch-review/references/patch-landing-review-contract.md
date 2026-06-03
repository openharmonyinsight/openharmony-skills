# Patch Landing Review Contract

The review stage only answers whether the active batch patch is truly landed.
It does not judge future tests, unrelated dirty files, or non-active issues.

Blocking evidence is limited to:

- patch absent or final issue-filtered diff empty
- key hunk, key file, or key semantic missing
- unresolved conflict remains
- change landed in the wrong repo or wrong file
- required change exceeds the issue allowed file scope

Non-blocking facts:

- `git apply` failed first, then minimal manual landing succeeded in scope
- manual rewrite differs textually from upstream but preserves recorded
  semantics
- build has not run yet
- terminal/deferred issues already removed from active batch
- unrelated worktree dirty files, SDK/toolchain outputs, `src/out`, or
  `.ace-outputs`

If `pending_current_stage` is empty and at least one active issue is
`ready_for_next`, review should pass the ready batch forward.
