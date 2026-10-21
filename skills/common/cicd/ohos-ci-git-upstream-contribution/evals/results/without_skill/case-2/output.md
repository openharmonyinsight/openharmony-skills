以下假定 `fork` 是你 fork 仓库的远端名。确认当前处于 `fix-a` 分支，且已选好需要纳入 PR 的改动后，执行：

```bash
git switch fix-a
git diff
git add -p
git diff --cached

# 将改动合入原提交，保留原提交说明、Signed-off-by 和 Issue
git commit --amend --no-edit

# 仅当远端分支仍指向刚核对的 head 时，才允许改写
git push \
  --force-with-lease=refs/heads/fix-a:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  fork HEAD:refs/heads/fix-a
```

这样会更新已有 PR，并保持单提交。如果 lease 校验失败，应重新核对远端变化，不要改用 `--force`。以上命令均未执行。
