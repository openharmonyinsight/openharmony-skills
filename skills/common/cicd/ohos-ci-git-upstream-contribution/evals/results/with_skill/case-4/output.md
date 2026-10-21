应使用**独立 worktree 及其独立索引**提交。不要在原工作区执行普通 `git commit`：即使只运行 `git add guide.md`，也会把已暂存的 `unrelated.cpp` 一起提交。

以下仅为方案，未执行。占位路径需替换为仓库外的实际绝对路径，功能分支名应尚未使用。

1. 在原工作区记录状态，并导出 `guide.md` 相对 HEAD 的完整改动，包含已暂存和未暂存两部分：

```sh
git status --short --untracked-files=all
git rev-parse HEAD
git diff --cached --binary
git diff --binary

git diff HEAD --binary -- guide.md > /absolute/path/guide-only.patch
```

最后一条只导出 `guide.md`，不会包含 `unrelated.cpp` 或未跟踪的 `notes.txt`。前面的完整差异用于事后核对原状态。

2. 从明确的目标分支创建隔离工作区：

```sh
git worktree add -b docs/guide-only /absolute/path/guide-worktree upstream/main
```

这里使用本地已有的 `upstream/main`；若后续需要更新远端引用，应另行执行 fetch，本方案不涉及网络。

3. 在新 worktree 中检查并应用补丁：

```sh
cd /absolute/path/guide-worktree
git apply --check --index /absolute/path/guide-only.patch
git apply --index /absolute/path/guide-only.patch

git status --short
git diff --cached --name-only
git diff --cached -- guide.md
git diff --cached --check
```

确认暂存文件清单**只有 `guide.md`**，内容正是本次改动，并完成仓库要求的文档检查。若补丁检查失败，停止应用，在隔离目录处理目标分支差异，不修改原工作区。

4. 审阅通过后，仅在隔离 worktree 提交：

```sh
git commit --signoff -m '<符合仓库规范的提交标题>'
git diff-tree --no-commit-id --name-only -r HEAD
git log --oneline upstream/main..HEAD
git diff upstream/main...HEAD -- guide.md
```

使用现有真实 Git 身份；若仓库要求关联 Issue，补充真实 Issue URL，不能虚构。

5. 返回原工作区，重新核对第一步的状态和两份差异。

整个过程不在原工作区执行 `add`、`commit`、`stash`、`reset` 或取消暂存。原 `guide.md` 的暂存／未暂存划分、`unrelated.cpp` 的暂存状态及 `notes.txt` 都保持原样；隔离分支提交成功后，原工作区中的这些改动也不会自动清除。
