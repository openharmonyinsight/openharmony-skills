# Common Issues

PR 创建过程中的常见问题及解决方案（平台无关）。

## 目录

- [Git 相关问题](#git-相关问题)
- [Commit 相关问题](#commit-相关问题)
- [Push 相关问题](#push-相关问题)
- [PR 创建相关问题](#pr-创建相关问题)
- [审查相关问题](#审查相关问题)

## Git 相关问题

### "fatal: not a git repository"

**问题**：
```bash
$ git status
fatal: not a git repository (or any of the parent directories): .git
```

**原因**：当前目录不在 git 仓库中

**解决方案**：
```bash
# 查找仓库根目录
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo '.')"

# 或导航到 ace_engine 目录
cd /path/to/ace_engine

# 验证
git status
```

### "Changes not staged for commit"

**问题**：
```bash
$ git commit -m "feat: add feature"
On branch feature-branch
Changes not staged for commit:
  modified:   file1.cpp
  modified:   file2.h

no changes added to commit (use "git add" and/or "git commit -a")
```

**原因**：修改的文件未 staged

**解决方案**：
```bash
# 方案 1: 添加所有修改
git add .

# 方案 2: 添加特定文件
git add file1.cpp file2.h

# 方案 3: 交互式添加
git add -i

# 然后提交
git commit -m "feat: add feature"
```

### ".git/index.lock" 错误

**问题**：
```bash
$ git commit
fatal: Unable to create '/path/.git/index.lock': File exists.
```

**原因**：另一个 git 进程正在运行

**解决方案**：
```bash
# 删除锁文件（确保没有其他 git 进程运行）
rm .git/index.lock

# 重试
git commit
```

## Commit 相关问题

### "Aborting commit due to empty commit message"

**问题**：
```bash
$ git commit -m ""
Aborting commit due to empty commit message.
```

**原因**：Commit message 为空

**解决方案**：
```bash
# 使用正确的格式
git commit -m "feat: add feature description"

# 或打开编辑器
git commit

# 或使用 heredoc（多行）
git commit -m "$(cat <<'EOF'
feat: add feature

Detailed description here.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### Commit message 格式错误

**问题**：Commit message 不符合项目规范

**解决方案**：遵循项目规范

```bash
# ❌ 错误示例
git commit -m "Added new feature for grid"

# ✅ 正确示例
git commit -m "feat: add sheet selection to Grid component"
```

参考 [commit-message-guide.md](commit-message-guide.md)

### "nothing to commit"

**问题**：
```bash
$ git commit
On branch feature-branch
Your branch is up to date with 'origin/feature-branch'.

nothing to commit, tree clean
```

**原因**：没有需要提交的修改

**解决方案**：
```bash
# 检查是否有未追踪的文件
git status

# 检查是否有未提交的修改
git diff

# 如果确实没有修改，检查是否在正确的分支
git branch
```

### "Your branch is ahead of origin by N commits"

**问题**：
```bash
$ git status
Your branch is ahead of 'origin/feature-branch' by 3 commits.
```

**原因**：本地有 commit 未推送到远程

**解决方案**：
```bash
# 正常情况：推送 commit
git push

# 如果需要修改 commit 历史（谨慎操作）
git push -f  # 强制推送（仅在必要时）
```

## Push 相关问题

### "failed to push some refs"

**问题**：
```bash
$ git push
To github.com:user/repo.git
 ! [rejected]        feature-branch -> feature-branch (fetch first)
error: failed to push some refs to 'github.com:user/repo.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref.
```

**原因**：远程有本地没有的提交

**解决方案**：
```bash
# 方案 1: rebase（推荐，保持线性历史）
git fetch origin
git rebase origin/feature-branch
git push

# 方案 2: merge（会产生 merge commit）
git pull origin feature-branch
git push

# 方案 3: 强制推送（仅在你的分支且确定要覆盖时）
git push -f
```

### "Permission denied"

**问题**：
```bash
$ git push
fatal: Permission denied to user/repo.git
failed to push some refs to 'github.com:user/repo.git'
```

**原因**：认证失败

**解决方案**：
```bash
# 检查远程 URL
git remote -v

# 如果是 HTTPS，检查 GitHub token
# 如果是 SSH，检查 SSH key

# 更新远程 URL（如需要）
git remote set-url origin git@github.com:user/repo.git

# 使用 gh CLI 认证
gh auth login

# 重试推送
git push
```

### "src refspec master does not match any"

**问题**：
```bash
$ git push origin master
error: src refspec master does not match any
```

**原因**：本地没有 master 分支

**解决方案**：
```bash
# 检查当前分支
git branch

# 推送当前分支
git push -u origin HEAD

# 或推送到正确的分支
git push -u origin feature-branch
```

### 推送大文件失败

**问题**：
```bash
$ git push
error: RPC failed; HTTP 413 curl 22 The requested URL returned error: 413
```

**原因**：文件超过大小限制

**解决方案**：
```bash
# 检查大文件
git rev-list --objects --all |
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
  awk '/^blob/ {print substr($0,6)}' |
  sort -k2 -n -r |
  head -10

# 使用 Git LFS（如需要）
git lfs track "*.bin"
git add .gitattributes
```

## PR/MR 创建相关问题（通用）

### "glab: command not found"

**问题**：
```bash
$ glab mr create
bash: glab: command not found
```

**原因**：GitLab CLI 未安装（可选工具）

**解决方案**：
```bash
# 方案 1：使用 Web 界面（推荐）
# 直接在浏览器中创建 MR
# 访问：https://gitcode.com/openharmony/arkui_ace_engine/merge_requests/new

# 方案 2：安装 glab（可选）
# macOS
brew install glab

# Linux
# 参考：https://gitlab.com/gitlab-org/cli

# 认证
glab auth login
```

### "A merge request already exists"

**问题**：
```bash
$ glab mr create
x A merge request already exists for this branch: !42
```

**原因**：该分支的 MR 已存在

**解决方案**：
```bash
# 查看现有 MR
glab mr list

# 在浏览器中查看
glab mr view 42 --web

# 或直接访问
# https://gitcode.com/openharmony/arkui_ace_engine/merge_requests/42
```

### "Base branch not found"

**问题**：指定的 base branch 不存在

**解决方案**：
```bash
# 列出可用分支
git branch -r | grep upstream

# 常见的 base branch: master, master
# 在 Web 界面创建 MR 时选择正确的 target branch
```

### MR 标题或描述为空

**问题**：MR 创建时标题或描述未正确填写

**解决方案**：
```bash
# 使用 Web 界面创建 MR（推荐）
# 1. 访问 MR 创建页面
# 2. 手动填写标题和描述
# 3. 点击 "Create merge request"

# 或使用 glab
glab mr create --title "MR Title" --description "Description" --web
```

### MR 无法创建（权限问题）

**问题**：
```
403 Forbidden - You don't have permission to create MR
```

**原因**：没有权限直接向目标仓库创建 MR

**解决方案**：
```bash
# 对于 openharmony/arkui_ace_engine，需要：
# 1. Fork 仓库到你的账号
# 2. 推送到你的 fork
# 3. 从你的 fork 创建 MR 到 openharmony/arkui_ace_engine

# 检查 remote 配置
git remote -v

# 应该看到：
# origin    你的fork
# upstream  openharmony/arkui_ace_engine
```
## Summary

- Change 1
- Change 2

## Changes

Detailed changes...

EOF
)"

# 或使用文件
gh pr create --title "PR Title" --body-file pr_description.md
```

### PR 指定审查者

**问题**：需要指定 PR 审查者

**解决方案**：
```bash
# 指定单个审查者
gh pr create --reviewer username

# 指定多个审查者
gh pr create --reviewer user1,user2,user3

# 指定团队审查者
gh pr create --team-reviewer team-name
```

## 审查相关问题

### PR 审查后需要修改

**问题**：PR 审查后有需要修改的地方

**解决方案**：
```bash
# 在分支上进行修改
# ... 编辑代码 ...

# 提交修改
git add .
git commit -m "fix: address review feedback"

# 推送到远程（自动更新 PR）
git push

# 如果需要 amend 到之前的 commit（谨慎使用）
git commit --amend
git push -f  # 需要强制推送
```

### PR 冲突

**问题**：PR 与目标分支有冲突

**解决方案**：
```bash
# 更新目标分支
git fetch origin
git rebase origin/<base-branch>

# 解决冲突
# ... 编辑冲突文件 ...

# 标记冲突已解决
git add .
git rebase --continue

# 推送更新
git push -f  # rebase 后需要强制推送
```

### 关联 Issue

**问题**：PR 需要关联到 Issue

**解决方案**：
```bash
# 在 PR 描述中包含关键词
gh pr create --body "Fixes #12345"

# 或在 commit message 中
git commit -m "feat: add feature

Fixes #12345"
```

## 其他常见问题

### 跟踪错误的远程分支

**问题**：分支跟踪了错误的远程分支

**解决方案**：
```bash
# 检查跟踪状态
git branch -vv

# 设置正确的跟踪分支
git branch --set-upstream-to=origin/correct-branch your-branch

# 或推送时设置
git push -u origin your-branch
```

### 撤销已经推送的 commit

**问题**：需要撤销已经推送的 commit

**解决方案**：
```bash
# 撤销最近的 commit（保留修改）
git revert HEAD
git push

# 或重置到之前的 commit（谨慎使用）
git reset --hard HEAD~1
git push -f
```

### 查找正确的 base branch

**问题**：不确定应该使用哪个 base branch

**解决方案**：
```bash
# 查看远程分支
git branch -r

# 查看默认分支
git remote show origin | grep 'HEAD branch'

# 查看最近的提交
git log --oneline -10

# 查看分支差异
git log --oneline --graph --all
```

## 故障排查流程

### PR 创建失败时的排查步骤

1. **检查 git 状态**
   ```bash
   git status
   git branch -vv
   ```

2. **检查远程连接**
   ```bash
   git remote -v
   git fetch origin
   ```

3. **检查 gh CLI**
   ```bash
   gh --version
   gh auth status
   ```

4. **检查分支状态**
   ```bash
   git log origin/<base-branch>..HEAD --oneline
   ```

5. **尝试手动创建**
   ```bash
   gh pr create --draft
   ```

## 获取帮助

### Git 帮助
```bash
git help <command>
git <command> --help
```

### GitLab CLI 帮助（可选）
```bash
glab help
glab <command> --help
glab mr create --help
```

### 在线资源
- Git Documentation: https://git-scm.com/doc
- GitHub CLI: https://cli.github.com/
- GitLab CLI: https://gitlab.com/gitlab-org/cli
- GitHub Flow: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests
- GitLab Flow: https://docs.gitlab.com/ee/workflow/merge_requests.html

## 快速参考

### 常用命令
```bash
# 查看状态
git status

# 添加和提交
git add .
git commit -m "type: description"

# 推送
git push
git push -u origin branch-name

# 创建 PR（Web 界面 - 推荐）
# 访问相应平台的 PR 创建页面

# 创建 PR（使用 CLI - 可选）
# GitHub
gh pr create
gh pr create --base main
gh pr create --web  # 在浏览器中打开

# GitLab/GitCode
glab mr create
glab mr create --target main
glab mr create --web  # 在浏览器中打开

# 查看 PR
gh pr list       # GitHub: 列出所有 PR
gh pr view       # GitHub: 查看当前分支的 PR
glab mr list     # GitLab: 列出所有 MR
glab mr view     # GitLab: 查看当前分支的 MR
```

### 紧急恢复
```bash
# 撤销最近的 commit（保留修改）
git reset --soft HEAD~1

# 撤销最近的 commit（丢弃修改）
git reset --hard HEAD~1

# 撤销已推送的 commit
git revert HEAD

# 恢复到某个 commit
git reset --hard <commit-hash>
```
