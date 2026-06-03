# GitCode PR Flow

Submit through a personal fork branch into the configured upstream target
branch. Do not use `git push <remote> HEAD:refs/for/master` as the final
submission path.

Required order:

1. Confirm target git repo, upstream repo, target branch, fork remote, GitCode
   auth, and git `user.name` / `user.email`.
2. Run `scripts/scan_existing_submit_targets.mjs` for the whole ready queue.
   Reuse any existing open PR for the same Chromium issue before creating any
   new commit, branch, GitCode Issue, or PR.
3. If a fork branch already exists for the issue, compare it before pushing.
   If it already has an open PR, reuse the PR. If it has no PR and the branch
   commit differs from the newly prepared isolated commit, stop that issue with
   `submit_failed(branch_exists_commit_mismatch)`; do not create an automatic
   `-r2` branch and do not force-push.
4. Create the isolated commit for the current issue from the manifest/upstream
   baseline and the issue submit scope.
5. Push only after the idempotency checks above have passed.
6. Create or confirm the GitCode Issue in the upstream repo.
7. Create the PR with `--head <fork-owner>:<branch>` and `--base <target>`.
8. Confirm the PR is linked to the GitCode Issue.
9. Comment exactly `start build` on the PR and confirm the comment exists.

Do not implement the batch submission loop as a generated inline script in the
run output. Extend scripts under this skill when reusable behavior is missing.

Commit requirements:

- Chinese first.
- Include full CVE when the inputs have one.
- Include `Signed-off-by:` from the current repo git config via `git commit -s`.
- Include exact line `Co-Authored-By: Agent`.

Cross-repo PR `--head` must use `owner:branch`, not `owner/branch`. Confirm the
fork owner from the fork remote URL; do not assume it equals the login name.
