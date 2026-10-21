方案依据指定技能及其分支规则；本次仅阅读资料，未执行 Git 操作、修改文件或访问远端。

采用两个独立 worktree，分别从上游目标分支创建功能分支，保留当前 master、工作文件和暂存状态。

| 上游 remote / 目标分支 | 功能分支（建议） | 对应 Issue | 推送 remote |
|---|---|---|---|
| `origin/release-a` | `fix/release-a-31` | Issue 31 的完整 URL | `personal` |
| `origin/release-b` | `fix/release-b-32` | Issue 32 的完整 URL | `personal` |

1. **执行前核对**
   - 查看 `git status`、当前 HEAD、staged/unstaged diff、未跟踪文件和 remote URL，确认 `origin` 为上游、`personal` 为 fork。
   - 核对修复涉及的文件、hunk 或已有提交 SHA，排除 master 中无关提交。
   - 查目标仓库贡献说明与 Issue/PR 模板，核实 Issue 31、32 的仓库和分支适用性，并查找已有 PR，避免重复创建。
   - 记录各目标分支 base SHA、现有 Git 身份及实际验证要求。

2. **隔离修复**
   - 更新上游引用后，从 `origin/release-a`、`origin/release-b` 分别建立独立 worktree；不从本地 master 分支创建。
   - 如果修复尚未提交，对选定已跟踪文件导出相对源 HEAD 的补丁，覆盖 staged 与 unstaged 的最终差异：
     ```sh
     git diff HEAD --binary -- <selected-paths>
     ```
     同一文件混有无关 hunk 时，仅提取已确认的修复片段。未跟踪新增文件单独确认并复制，不能整体复制工作目录。
   - 在隔离 worktree 先执行 `git apply --check --index <patch-file>`，通过后再应用。
   - 如果修复已有独立提交，可在隔离 worktree 使用 `git cherry-pick --no-commit <source-sha>` 重放，再按各分支 Issue 重新提交。
   - 不自动 stash、reset、unstage 或清除源工作区修改。

3. **逐分支验证与提交**
   - 核对 merge-base、完整 PR diff、提交范围及隔离索引，确认仅包含本次修复。
   - 分别执行目标分支要求的检查；一个分支通过不代表另一个也通过。
   - 使用现有真实 Git 身份和 `git commit --signoff`。提交正文分别只写：
     - release-a：`Issue: <Issue 31 完整 URL>`
     - release-b：`Issue: <Issue 32 完整 URL>`
   - 每条 PR 的提交消息和正文仅关联自己的 Issue，不顺带写另一 Issue 的 URL 或 `#数字`。两条提交实现同一修复，但因基础分支、Issue 信息不同，SHA 通常不同。

4. **推送与创建 PR**
   - 将功能分支推送至 `personal`，PR 目标分别为上游 `release-a`、`release-b`，head 使用实际 fork owner 与对应功能分支。
   - 按仓库模板填写改动原因、真实检查结果和未验证项。不预填“全部通过”。
   - 创建后回读 head/base、Issue 关联及提交范围，记录各分支的 base SHA、commit SHA 和 PR URL。
   - 若无可用 GitCode CLI/API，则提供可手动提交的 PR 草稿，不用 `gh` 替代。

若遇冲突、身份缺失或远端异常变化，保留当前状态，停止受影响分支的后续提交和推送，并分别报告两条分支的进度。当前缺少具体修复范围、仓库 URL 和验证要求，因此方案中的占位符需在执行前核实。
