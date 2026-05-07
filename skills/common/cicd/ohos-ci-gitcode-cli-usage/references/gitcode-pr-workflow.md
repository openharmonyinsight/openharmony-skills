# GitCode PR 自动化工作流程

本文档描述如何将本地代码改动提交到个人 fork，并通过 `oh-gc` 创建到 GitCode 上游仓库的 PR。

## 参数优先原则

不要依赖固定 remote 名称或固定环境变量。Agent 应按以下优先级获取信息：

| 信息 | 优先来源 | 兜底来源 |
| --- | --- | --- |
| 认证信息 | `oh-gc auth status` 与 `~/.config/gitcode-cli/config.json` | 用户明确提供的临时 token |
| 上游仓库 | `--repo owner/repo` 参数 | 当前仓库的 GitCode remote |
| 源分支 | 当前 git 分支 | 用户指定的分支名 |
| fork 用户 | `oh-gc auth status` 中的登录用户 | `--head owner:branch` 参数中的 owner |
| 目标分支 | `--base branch` 参数 | 仓库默认分支或用户指定分支 |

`gitcode` 和 `personal` 可以作为 remote 名称示例，但不是强制规范。跨仓 PR 创建时优先使用显式参数：

```bash
oh-gc pr create \
    --repo openharmony/arkui_ace_engine \
    --head myfork:my-feature \
    --base master \
    --title "Fix issue"
```

## 安全规则

不要把 Token 写入 remote URL、提交到 git 历史记录、输出到日志或复制到 PR 描述中。

推荐认证方式：

```bash
oh-gc auth status
oh-gc auth login
```

Token 存储位置为 `~/.config/gitcode-cli/config.json`，由 `oh-gc auth login` 管理。只有在用户明确要求非交互自动化时，才临时使用用户提供的 token；不要把 token 写入脚本、remote URL 或仓库文件。

remote URL 保持无 Token 形式：

```text
https://gitcode.com/{username}/{repo}.git
```

## 前置检查

执行 PR 自动化前先确认：

1. `oh-gc --version` 符合当前 Skill 要求。
2. `oh-gc auth status` 能获取当前登录用户。
3. `git status --porcelain` 确认待提交文件范围。
4. `git branch --show-current` 确认源分支。
5. 通过用户输入、`--repo` 参数或 GitCode remote 确认上游仓库。
6. 通过用户输入、`--base` 参数或仓库默认分支确认目标分支。

## PR 模板规则

创建 PR 时必须先在目标仓库工作区查询模板，不要写死 PR body。

模板查找路径按优先级：

1. `.gitcode/PULL_REQUEST_TEMPLATE.md`
2. `.github/PULL_REQUEST_TEMPLATE.md`
3. `docs/PULL_REQUEST_TEMPLATE.md`

如果没有模板，向用户确认是否使用临时 body。不要擅自生成与目标仓库模板不一致的格式。

```bash
TEMPLATE_FILE=""
for candidate in \
    .gitcode/PULL_REQUEST_TEMPLATE.md \
    .github/PULL_REQUEST_TEMPLATE.md \
    docs/PULL_REQUEST_TEMPLATE.md
do
    if [ -f "$candidate" ]; then
        TEMPLATE_FILE="$candidate"
        break
    fi
done

if [ -z "$TEMPLATE_FILE" ]; then
    echo "No PR template found; ask the user before creating a custom body."
    exit 1
fi
```

## 一键执行脚本骨架

以下脚本展示自动化骨架。`TARGET_REPO`、`HEAD_OWNER`、`BASE_BRANCH` 等本地变量应来自用户参数、`oh-gc auth status`、当前 git 分支或本地 GitCode remote 推导；不要要求固定环境变量。

```bash
# 1. 检查工具和认证
oh-gc --version
oh-gc auth status

# 2. 根据当前仓库和用户输入确认目标
CURRENT_BRANCH=$(git branch --show-current)
TARGET_REPO="openharmony/arkui_ace_engine"
HEAD_OWNER="myfork"
HEAD_BRANCH="$CURRENT_BRANCH"
BASE_BRANCH="master"

# 3. 查找 PR 模板
TEMPLATE_FILE=""
for candidate in \
    .gitcode/PULL_REQUEST_TEMPLATE.md \
    .github/PULL_REQUEST_TEMPLATE.md \
    docs/PULL_REQUEST_TEMPLATE.md
do
    if [ -f "$candidate" ]; then
        TEMPLATE_FILE="$candidate"
        break
    fi
done

if [ -z "$TEMPLATE_FILE" ]; then
    echo "No PR template found; ask the user before creating a custom body."
    exit 1
fi

# 4. 提交改动
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit"
else
    git add -A
    git commit -s -m "具体的改动说明"
fi

# 5. 推送到 fork remote。personal 只是示例 remote 名称，可替换为实际 fork remote。
GIT_LFS_SKIP_SMUDGE=1 git push -u personal "$HEAD_BRANCH" --no-verify

# 6. 按模板创建 PR
ISSUE_NUMBER="#12345"
PR_BODY=$(sed "s/\\*\\*IssueNo\\*\\*:/\\*\\*IssueNo\\*\\*: $ISSUE_NUMBER/" "$TEMPLATE_FILE")

oh-gc pr create \
    --repo "$TARGET_REPO" \
    --head "$HEAD_OWNER:$HEAD_BRANCH" \
    --base "$BASE_BRANCH" \
    --title "PR标题" \
    --body "$PR_BODY"
```

## 详细步骤

### Step 1: 检查 `oh-gc`

```bash
which oh-gc || npm install -g @oh-gc/cli@0.7.5
oh-gc --version
```

如果 npm 全局路径不在 `PATH` 中，先修正 `PATH`，不要在文档中固定某个用户目录下的 `oh-gc` 路径。

### Step 2: 检查认证

```bash
oh-gc auth status
oh-gc auth login
```

优先使用 `oh-gc auth login` 管理 `~/.config/gitcode-cli/config.json`。不要在示例中直接手写 JSON 覆盖配置文件。

### Step 3: 确认仓库与分支

优先使用显式参数：

```bash
TARGET_REPO="openharmony/arkui_ace_engine"
HEAD_OWNER="myfork"
HEAD_BRANCH="$(git branch --show-current)"
BASE_BRANCH="master"
```

如果用户没有给出 `TARGET_REPO`，可从当前仓库的 GitCode remote 推导：

```bash
git remote -v
```

remote 名称不固定。找到 `gitcode.com/{owner}/{repo}.git` 形式的 remote 后，再确认解析出的 `owner/repo` 是否为目标上游仓库。

### Step 4: 提交代码

提交前确认待提交范围：

```bash
git status --porcelain
git diff --stat
```

Commit message 使用仓库要求的格式，通常可用 `git commit -s` 生成 `Signed-off-by`：

```bash
git add <changed-files>
git commit -s -m "具体的改动说明"
```

### Step 5: 推送到 fork

```bash
GIT_LFS_SKIP_SMUDGE=1 git push -u personal "$(git branch --show-current)" --no-verify
```

`personal` 只是 fork remote 的示例名称。实际 remote 名称由当前仓库配置或用户指定决定。

### Step 6: 创建 Issue

如果目标仓库要求 PR 关联 Issue，先创建或确认 Issue：

```bash
oh-gc issue create \
    --repo "$TARGET_REPO" \
    --title "Issue标题" \
    --body "Issue描述内容"
```

记录返回的 Issue 编号，用于填充 PR 模板。

### Step 7: 创建 PR

必须基于目标仓库模板生成 `--body`：

```bash
TEMPLATE_FILE=".gitcode/PULL_REQUEST_TEMPLATE.md"
ISSUE_NUMBER="#12345"
PR_BODY=$(sed "s/\\*\\*IssueNo\\*\\*:/\\*\\*IssueNo\\*\\*: $ISSUE_NUMBER/" "$TEMPLATE_FILE")

oh-gc pr create \
    --repo "$TARGET_REPO" \
    --head "$HEAD_OWNER:$HEAD_BRANCH" \
    --base "$BASE_BRANCH" \
    --title "PR标题" \
    --body "$PR_BODY"
```

参数说明：

| 参数 | 说明 |
| --- | --- |
| `--repo` | 上游目标仓库，格式为 `owner/repo` |
| `--head` | 源分支，格式为 `{fork_owner}:{branch_name}` |
| `--base` | 目标分支 |
| `--title` | PR 标题 |
| `--body` | 基于目标仓库 PR 模板生成的描述 |

## 常见问题

### 推送失败：Permission denied

原因：没有直接推送到上游仓库的权限。

处理：确认 fork remote，并推送到个人 fork。

### 推送失败：LFS object not found

原因：LFS 对象同步问题。

处理：使用 `GIT_LFS_SKIP_SMUDGE=1` 跳过 LFS 验证。

### `oh-gc: command not found`

原因：npm 全局 bin 目录不在 `PATH` 中。

处理：

```bash
export PATH="$PATH:$(npm prefix -g)/bin"
```

### 认证失败

原因：Token 过期、无效或未登录。

处理：

```bash
oh-gc auth login
oh-gc auth status
```

## AI Agent 执行指南

对于 AI Agent，执行此工作流时应：

1. 先运行 `oh-gc --version` 和 `oh-gc auth status`。
2. 从用户参数、认证信息、当前分支和 GitCode remote 推导目标仓库、fork owner、源分支和目标分支。
3. 提交前展示或检查 `git status --porcelain` 与 `git diff --stat`。
4. 查找目标仓库 PR 模板，并基于模板生成 PR body。
5. 使用 `oh-gc pr create --repo ... --head owner:branch --base ...` 创建 PR。
6. 返回 GitCode PR 链接给用户。

## 完整示例

```bash
# 场景：将 overlay_manager.cpp 的改动提交并创建 PR

oh-gc --version
oh-gc auth status

TARGET_REPO="openharmony/arkui_ace_engine"
HEAD_OWNER="myfork"
HEAD_BRANCH="$(git branch --show-current)"
BASE_BRANCH="master"

TEMPLATE_FILE=""
for candidate in \
    .gitcode/PULL_REQUEST_TEMPLATE.md \
    .github/PULL_REQUEST_TEMPLATE.md \
    docs/PULL_REQUEST_TEMPLATE.md
do
    if [ -f "$candidate" ]; then
        TEMPLATE_FILE="$candidate"
        break
    fi
done

if [ -z "$TEMPLATE_FILE" ]; then
    echo "No PR template found; ask the user before creating a custom body."
    exit 1
fi

git add frameworks/core/components_ng/pattern/overlay/overlay_manager.cpp
git commit -s -m "移除overlay_manager.cpp中未使用的头文件dynamic_module_helper.h"

GIT_LFS_SKIP_SMUDGE=1 git push -u personal "$HEAD_BRANCH" --no-verify

ISSUE_NUMBER="#12345"
PR_BODY=$(sed "s/\\*\\*IssueNo\\*\\*:/\\*\\*IssueNo\\*\\*: $ISSUE_NUMBER/" "$TEMPLATE_FILE")

oh-gc pr create \
    --repo "$TARGET_REPO" \
    --head "$HEAD_OWNER:$HEAD_BRANCH" \
    --base "$BASE_BRANCH" \
    --title "移除 overlay_manager.cpp 中未使用的头文件" \
    --body "$PR_BODY"
```
