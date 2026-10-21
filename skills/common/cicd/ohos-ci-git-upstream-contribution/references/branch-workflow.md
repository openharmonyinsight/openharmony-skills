# 多目标分支与 PR 更新

## 迁移选定未提交改动

先记录源工作区 HEAD、已暂存和未暂存差异，以及选定文件/片段；原工作区仅作读取。为实际目标分支创建独立 worktree，它有单独的索引，避免普通 commit 将原索引中的无关文件一起提交。

1. 对已跟踪的选定改动，用 `git diff HEAD --binary -- <selected-paths>` 导出相对于源 HEAD 的补丁，覆盖这些文件中 staged 与 unstaged 的最终差异。若同一文件包含不属于本任务的 hunk，不整体导出该文件；从差异中构造并核验仅包含已授权 hunk 的补丁，范围不明确时先澄清范围。
2. 选定但尚未被跟踪的新增文件不在上述 diff 中；单独列出，只复制已确认新增文件到隔离 worktree 的相同相对路径，保留必要权限/链接语义。不要复制整个工作目录。已暂存的新增文件会出现在 HEAD diff 中，不重复复制。
3. 在隔离 worktree 应用前运行 `git apply --check --index <patch-file>`，成功后才 `git apply --index <patch-file>`。目标分支不同可能导致冲突；保留补丁，在隔离目录解决并重新检查，不重置源工作区。已有已提交改动另按确认的提交清单 cherry-pick，不把 HEAD 未提交补丁误当完整 PR 差异。
4. 核对隔离目录中的 staged diff、文件清单和内容只包含本任务，再测试、签名提交及推送。原工作区中的修改和原暂存状态保持原样；说明改动已由隔离分支提交，但不会自动清除用户原工作区的对应修改。

不要为了获得“干净索引”自动 unstage、stash 或 reset 用户内容，也不要依赖普通 `git add <selected>` 排除原有 staged 内容。

## 多分支提交

为每个目标建立映射：upstream/base SHA → feature branch → Issue URL → commit SHA → PR URL。默认各分支使用独立 Issue，若仓库允许复用或无需 Issue，按该仓库门禁执行并说明。

每条功能分支从其目标分支创建，不能从包含其它未合入工作的本地 master 起步，否则 PR diff 混入无关变化。干净的隔离 worktree 中可用 `git cherry-pick --no-commit <source-sha>` 重放，再以本分支 Issue 与 `--signoff` 提交；冲突先解决并验证，不继续批量推送失败分支。

提交正文只关联本分支需要的 Issue。GitCode 可能自动关联正文及消息中的 Issue URL 或 `#数字`；不要顺带列其它分支的 Issue，避免门禁出现多 Issue 关联。确需跨分支溯源时遵循仓库规则，可描述来源提交或 PR URL，并回读实际关联结果。

逐分支检查 merge-base、diff、提交和 Issue，不因一个分支测试通过就声称其它分支也通过。一个分支失败时保留其状态，并准确报告其它分支已完成的动作。

## 更新已有 PR

先读取远端 head SHA 与 PR 归属。仓库要求单提交且待改写提交属于本任务、用户已授权更新时，可 amend；保留正确 Issue 与 Signed-off-by，身份变化时核验而非复制他人签名。不要求单提交时可按仓库习惯追加提交。

非快进更新需要改写授权；已有授权不重复询问。执行前核对预期旧 SHA，使用显式 lease：

```sh
git push --force-with-lease=refs/heads/<branch>:<expected-old-sha> <fork-remote> HEAD:refs/heads/<branch>
```

lease 被拒绝说明远端已变化，重新读取和检查，不改用 `--force`。其它目标分支的更新同样在独立 worktree 重放，不 `reset --hard` 用户现有分支。只清理本任务创建且确认无未保存内容的临时 worktree。
