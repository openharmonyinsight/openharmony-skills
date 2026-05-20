---
name: power-gitcode
description: GitCode 平台全能操作技能。
descriptionZH: GitCode 全操作。【触发场景】PR 创建/查看/评论/merge/squash、Issue 创建/查看/标签、gitcode
  链接、第xxx号 PR/Issue、fork/Release、template、commitlint。【注意】PR/Issue 创建返回
  html_url；关联：在 body 写 Issue 链接；commit 必须英文 commitlint。
tags:
  - GitCode
  - PR管理
  - Issue
  - 仓库管理
  - commit
---

# Power GitCode

GitCode 平台全能操作技能。**通过 Bash 调用 Python 脚本执行所有操作，不要自行调用任何 HTTP API。**

## ⚠️ 执行规则（100% 必须遵守）

**收到以下任何输入时，立即用 Bash 执行对应脚本命令：**

| 用户输入 | 必须执行的 Bash 命令 |
|---------|-------------------|
| 任何 PR 链接（如 `https://gitcode.com/Cangjie/cangjie_compiler/pull/1149`） | `python3 skills/power-gitcode/scripts/power-gitcode.py get_pr --owner Cangjie --repo cangjie_compiler --number 1149` |
| 任何 PR 编号（如「第 1149 号 PR」「PR #1149」） | 同上格式，owner/repo 从 URL 中提取 |
| 任何 Issue 链接或编号 | `python3 ... get_issue --owner xxx --repo xxx --number xxx` |
| 「创建 PR」| `python3 ... create_pr --owner xxx --repo xxx --title "..." --body "..." --head "fork用户名:分支名" --base master` |
| 「合并 PR」| `python3 ... merge_pr --owner xxx --repo xxx --number xxx` |
| 「创建 Issue」| `python3 ... create_issue --owner xxx --repo xxx --title "..." --body "..."` |
| 「提交代码」「git commit」| `python3 ... create_commit ...`（详见下方 commitlint 规则）|
| 「fork 仓库」| `python3 ... fork_repo --owner xxx --repo xxx` |
| 「创建 Release」| `python3 ... create_release ...` |
| 「查看 Issue/PR 模板」| `python3 ... list_issue_templates` / `get_pr_template` |

**⚠️ 命令格式（必须严格遵守，否则参数错误）：**

```
python3 skills/power-gitcode/scripts/power-gitcode.py <命令> --owner <所有者> --repo <仓库名> --number <编号>
```

- `--owner`：仓库所有者（不是 URL 中的完整路径）
- `--repo`：仓库名（不含 owner）
- `--number`：数字编号
- **禁止**使用 `--pr-number`，**禁止**把 owner/repo 合并

**正确示例：**
```
python3 skills/power-gitcode/scripts/power-gitcode.py get_pr --owner Cangjie --repo cangjie_compiler --number 1149
```

**错误示例（禁止）：**
```
python3 ... get_pr --repo Cangjie/cangjie_compiler --pr-number 1149   ← 错
python3 ... get_pr --owner Cangjie/cangjie_compiler --number 1149      ← 错
```

**Token 配置：** 环境变量 `gitcode_password` 或 `gitcode_token`（在调用脚本前确保已设置）。

## 能力概览

### PR 操作
- `create_pr` - 创建 PR（返回 `html_url`），**`--head` 格式：`fork用户名:分支名`**
- `get_pr` - 获取 PR 详情
- `get_pr_commits` - 获取 PR 的 commit 列表
- `get_pr_changed_files` - 获取 PR 修改的文件列表
- `get_pr_comments` - 获取 PR 评论（支持分页）
- `post_pr_comment` - 在 PR 上发表评论（支持代码行评论）
- `add_pr_labels` / `remove_pr_labels` - 添加/移除 PR 标签
- `assign_pr_testers` - 分配 PR 测试人员
- `check_pr_mergeable` - 检查 PR 是否可合并
- `merge_pr` - 合并 PR（支持 merge/squash/rebase）
- `update_pr` - **更新 PR 标题/内容/状态/标签/里程碑/草稿状态**

### Issue 操作
- `create_issue` - 创建 Issue（返回 `html_url`）
- `get_issue` - 获取 Issue 详情
- `add_issue_labels` - 给 Issue 添加标签
- `update_issue` - **更新 Issue 标题/内容/状态/负责人/里程碑/标签/优先级**

### 提交操作
- `create_commit` - **在仓库创建提交（必须符合 commitlint 格式：全英文）**

### PR-Issue 关联
- `get_issues_by_pr` - 根据 PR 获取关联的 Issue
- `get_prs_by_issue` - 根据 Issue 获取关联的 PR

### 模板操作
- `get_issue_template` - 获取 Issue 模板内容
- `get_pr_template` - 获取 PR 模板内容
- `list_issue_templates` - 列出所有可用的 Issue 模板
- `parse_issue_template` - 解析模板提取 labels 和 body
- `get_commit_title` - 获取最新 commit 首行（用作 PR 标题）

### 仓库操作
- `fork_repo` - Fork 仓库
- `create_release` - 创建 Release
- `create_label` - 创建标签
- `check_repo_public` - 检查仓库是否公开

## Commitlint 格式要求（必须遵守）

**所有 commit message 必须符合以下格式，全英文：**
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**常用 type：** `feat` `fix` `docs` `style` `refactor` `test` `chore` `perf` `ci` `build`

**示例：**
- `feat(compiler): add linear scan register allocation`
- `fix(runtime): handle null pointer in array access`
- `docs(sema): update TypeChecker class documentation`

**禁止：** 中文 commit message、缺少 type、无 scope（除非全局改动）

## 返回链接

`create_pr` 和 `create_issue` 成功后，**必须将返回的 `html_url` 明确告知用户**。

## 使用示例

```bash
# 创建 PR（fork 仓库提交到上游，fork用户名从 git remote -v 获取）
python3 skills/power-gitcode/scripts/power-gitcode.py create_pr \
  --owner Cangjie --repo cangjie_compiler \
  --title "feat(compiler): add new optimization pass" \
  --head "<fork用户名>:feat/new-pass" --base master \
  --body "Closes #123"  # PR 关联 Issue

# 更新 Issue（修改标题、状态、标签）
python3 skills/power-gitcode/scripts/power-gitcode.py update_issue \
  --owner Cangjie --repo cangjie_compiler --number 456 \
  --title "Bug: fixed memory leak" --state reopen --labels "bug,fixed"

# 更新 PR（修改标题、转为草稿）
python3 skills/power-gitcode/scripts/power-gitcode.py update_pr \
  --owner Cangjie --repo cangjie_compiler --number 789 \
  --title "WIP: refactoring TypeChecker" --draft true

# 获取 PR 详情（当用户提供 PR 链接时）
python3 skills/power-gitcode/scripts/power-gitcode.py get_pr \
  --owner Cangjie --repo cangjie_compiler --number 123

# 在 PR 上针对代码行评论
python3 skills/power-gitcode/scripts/power-gitcode.py post_pr_comment \
  --owner Cangjie --repo cangjie_compiler --number 123 \
  --body "LGTM" --path src/main.cj --position 42
```

## 典型工作流

### 提交 PR 流程（fork 仓库）
1. 通过 `git remote -v` 获取 fork 用户名，**不要猜测**
2. `get_commit_title` 获取 commit 标题作为 PR title
3. `get_pr_template` 获取**上游仓库**的 PR 模板
4. PR body 中写入 Issue 链接（如 `Closes #123`）实现 PR-Issue 关联
5. `create_pr` 创建 PR，**返回 `html_url` 给用户**

### 创建 Issue 流程
1. `list_issue_templates` 查看可用模板
2. `parse_issue_template` 解析选中的模板
3. `create_issue` 按模板格式创建，**返回 `html_url` 给用户**

### 创建 Commit 流程
1. 验证 commit message 符合 commitlint 格式（全英文）
2. 准备文件变更（base64 编码）
3. `create_commit` 执行提交
