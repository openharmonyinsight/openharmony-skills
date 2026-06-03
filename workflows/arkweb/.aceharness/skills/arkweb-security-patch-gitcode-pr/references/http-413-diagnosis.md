# HTTP 413 Diagnosis

For `HTTP 413`, `Request Entity Too Large`, `pack exceeds`, or other remote
large-pack rejection, stop blind retries.

Record:

```bash
git status --short --branch
git diff --cached --name-status
git diff --cached --stat
git rev-list --objects --no-object-names <upstream>/<target>..HEAD | wc -l
git diff --name-status <upstream>/<target>..HEAD
```

`<upstream>/<target>` means the manifest/upstream remote and target branch for
the target subrepo, for example `tpc/master`. The personal fork remote is the
push destination only. A large `personal/master..HEAD` count by itself is not a
valid preflight blocker when `tpc/master..HEAD` is the intended minimal submit
range and contains only the current issue commit.

Also inspect staged file sizes and forbidden paths:

```bash
git diff --cached --name-only
git diff --cached --name-only | while IFS= read -r f; do
  [ -e "$f" ] && du -h "$f"
done
```

Usual root cause is that the branch contains unrelated history, generated
outputs, archives, SDK/toolchain files, or batch/global files. Recreate from a
clean branch and stage only the current issue submit scope.

LFS pre-push failures:

- If `git push` fails with `Unable to find source for object ...` from Git LFS,
  first check whether the current issue submit scope contains any LFS-tracked
  file.
- When the issue commit changes no LFS-tracked file, this is a fork/baseline LFS
  hook problem, not a patch scope problem. Retry that push once with
  `GIT_LFS_SKIP_PUSH=1` and record both attempts.
- If the issue commit changes an LFS-tracked file, do not skip LFS upload.
  Fetch or restore the missing LFS object, then retry.
