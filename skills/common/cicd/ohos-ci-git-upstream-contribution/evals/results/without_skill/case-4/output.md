建议在**基于 `upstream/main` 的独立 worktree** 中提交，将 `guide.md` 已暂存和未暂存的改动合并成补丁。原工作区及其暂存状态保持不动，`unrelated.cpp` 和 `notes.txt` 都不会进入提交。

以下仅为可审阅方案，未执行；`materials/` 为空。

```bash
# 在原仓库目录运行；临时目录位于仓库外
task_tmp=$(mktemp -d)
submit_dir="$task_tmp/worktree"

# 提取 guide.md 相对 HEAD 的全部改动（包含已暂存和未暂存部分）
git diff --binary HEAD -- guide.md > "$task_tmp/guide.patch"

# 从明确的目标分支创建独立提交分支
git worktree add -b submit-guide "$submit_dir" upstream/main

# 先检查补丁是否适用于目标基线，再应用并暂存
git -C "$submit_dir" apply --check --index "$task_tmp/guide.patch"
git -C "$submit_dir" apply --index "$task_tmp/guide.patch"

# 审阅：应只有 guide.md，且内容符合预期
git -C "$submit_dir" status --short
git -C "$submit_dir" diff --cached --name-only
git -C "$submit_dir" diff --cached -- guide.md

# 确认无误后，仅提交 guide.md
git -C "$submit_dir" commit --only -m "更新 guide 文档" -- guide.md

# 核对本次提交涉及的文件
git -C "$submit_dir" show --stat --oneline HEAD
```

**任一步失败就停止，不继续执行后续命令。** 如果补丁因 `upstream/main` 的内容差异而无法应用，只在新 worktree 中解决并重新审阅。

最终提交位于 `submit-guide` 分支；原工作区中 `guide.md` 的部分暂存状态、`unrelated.cpp` 的暂存改动及未跟踪的 `notes.txt` 均保留。不要在原工作区运行 `git add .`、`git commit -a` 或普通的 `git commit`。
