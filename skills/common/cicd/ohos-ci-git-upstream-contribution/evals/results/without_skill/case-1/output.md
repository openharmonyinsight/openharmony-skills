materials/ 为空，以下方案仅依据题面，**暂不执行**。

1. **核对仓库状态与远端**
   只读检查 `git status`、`git remote -v` 和分支历史。以 `origin` 为上游、`personal` 为个人 fork；不从当前 `master` 创建修复分支，避免带入无关提交。

2. **分别从上游目标分支创建隔离工作区**
   后续执行时先获取上游最新引用，再创建两个 worktree，保留当前工作区的未提交文件，不执行 stash、reset 或 clean：
   ```bash
   git fetch origin
   git worktree add -b fix/issue-31 <独立目录-a> origin/release-a
   git worktree add -b fix/issue-32 <独立目录-b> origin/release-b
   ```
   尖括号为执行前需确定的目录占位符。

3. **制作并移植同一个修复**
   在目录 a 中实现最小修复、补充必要测试并提交，记录修复提交 SHA；在目录 b 中 cherry-pick 该提交。若分支差异造成冲突，按 release-b 的代码适配，核对修复语义一致。分别运行对应分支的测试并检查差异，确保没有无关改动。移植后的提交 SHA 可以不同。

4. **推送到 fork，分别发起上游 PR**
   ```bash
   git push personal fix/issue-31
   git push personal fix/issue-32
   ```
   不直接推送 `origin`。两个 PR 的对应关系为：

   | PR 来源 | 上游目标 | 关联 Issue |
   |---|---|---|
   | personal 的 `fix/issue-31` | 上游 `release-a` | 31 |
   | personal 的 `fix/issue-32` | 上游 `release-b` | 32 |

   PR 正文分别写 `Refs #31`、`Refs #32`，附上验证结果，并互相链接说明这是同一修复的两个发布分支版本。Issue 是否关闭，遵循上游流程处理。

当前缺少具体修复内容、仓库地址和测试说明，尚不能给出实际补丁或完整 PR 内容；以上命令均未执行。
