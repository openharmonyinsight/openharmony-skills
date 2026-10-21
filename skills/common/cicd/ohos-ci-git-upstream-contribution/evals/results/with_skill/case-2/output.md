按指定技能，采用 amend 保持单提交，并用显式 lease 保护刚核对的远端 head。以下仅供审阅，未执行；将 `<fork-remote>` 和文件路径替换为实际值。

先确认当前处于本次 PR 对应分支，检查索引中没有无关改动：

```sh
git branch --show-current
git remote -v
git status --short
git diff
git diff --cached
```

确认改动范围并完成仓库要求的检查后：

```sh
git add -- <本次修改的文件路径>
git diff --cached

# 保留已有提交消息、正确的 Issue 和 Signed-off-by
git commit --amend --no-edit

git show --stat --oneline HEAD
git log -1 --format=full

git push \
  --force-with-lease=refs/heads/fix-a:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  <fork-remote> HEAD:refs/heads/fix-a
```

若索引含无关改动，先在独立 worktree 隔离本次修改，再 amend。若 lease 被拒绝，应重新读取并检查远端变化，不改用 `--force`。推送成功后，已有 PR 会随 `fix-a` 更新，无需新建 PR。
