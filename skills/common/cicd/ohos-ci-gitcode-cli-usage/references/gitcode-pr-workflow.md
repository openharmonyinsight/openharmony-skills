# GitCode PR 自动化工作流程

本文档描述如何自动将本地代码改动提交并创建 PR 到 GitCode 上游仓库。

## Remote 命名建议

| Remote 名称 | 用途 | URL 格式 |
|-------------|------|----------|
| `gitcode` | 上游原始仓库 | `https://gitcode.com/{org}/{repo}.git` |
| `personal` | 个人 Fork 仓库 | `https://gitcode.com/{username}/{repo}.git` |

以上 remote 名称只是示例，便于脚本说明。实际操作应优先使用 `--repo owner/repo`、`--head owner:branch`、`--base branch` 等参数；如果依赖本地 remote 信息，需要先读取 `git remote -v` 并确认目标仓库。

> ⚠️ **安全提示**
>
> 不要把 Token 写入 remote URL、提交到 git 历史记录、输出到日志或复制到 PR 描述中。
> 如果 Token 泄露，请立即在 GitCode 设置中重新生成 Token。
>
> 建议做法：
> - 使用 `oh-gc auth login` 或 `~/.config/gitcode-cli/config.json` 保存认证信息
> - 需要非交互自动化时，也优先通过配置文件或参数传递必要信息
> - remote URL 保持无 Token 形式：`https://gitcode.com/{username}/{repo}.git`

## 前置条件

在执行此工作流之前，**必须**确认以下信息：

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| 认证状态 | GitCode 登录用户 | `oh-gc auth status` |
| 上游仓库 | PR 目标仓库 | `--repo owner/repo` 参数，或从本地 GitCode remote 推导 |
| 源分支 | fork 中的源分支 | 当前分支或 `--head owner:branch` 参数 |
| 目标分支 | 上游目标分支 | `--base branch` 参数或仓库默认分支 |

**Fork 地址自动拼接规则**：
- 如果 `personal` remote 不存在，自动根据上游仓库和用户名拼接
- 格式：`https://gitcode.com/{username}/{repo_name}.git`
- 例如：上游 `openharmony/arkui_ace_engine` → Fork `{username}/arkui_ace_engine`

## 一键执行脚本

将以下变量替换为实际值后执行。不要把实际 Token 保存到脚本、remote URL、提交记录或日志中。

```bash
# ===== 配置区 =====
USERNAME="your_username"              # 可从 oh-gc auth status 获取
UPSTREAM="openharmony/arkui_ace_engine"
BASE_BRANCH="master"
CURRENT_BRANCH=$(git branch --show-current)

# ===== 执行步骤 =====
# 1. 安装 oh-gc CLI（如未安装）
npm install -g @oh-gc/cli@0.7.5 2>/dev/null

# 2. 检查 oh-gc 认证
oh-gc auth status || oh-gc auth login

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

# 4. 提交改动（如有未提交的改动）
# 注意：commit message 必须符合 DCO 格式
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit"
else
    git add -A
    git commit -m "具体的改动说明

Co-Authored-By:Agent

Signed-off-by: ${USERNAME} <${USERNAME}@users.noreply.gitcode.com>"
fi

# 5. 推送到 personal fork
GIT_LFS_SKIP_SMUDGE=1 git push -u personal ${CURRENT_BRANCH} --no-verify

# 6. 基于目标仓库模板创建 PR
ISSUE_NUMBER="#12345"
PR_BODY=$(sed "s/\\*\\*IssueNo\\*\\*:/\\*\\*IssueNo\\*\\*: $ISSUE_NUMBER/" "$TEMPLATE_FILE")

oh-gc pr create \
    --repo ${UPSTREAM} \
    --head ${USERNAME}:${CURRENT_BRANCH} \
    --base ${BASE_BRANCH} \
    --title "PR标题" \
    --body "$PR_BODY"
```

## 详细步骤说明

### Step 1: 检查并安装 oh-gc CLI

```bash
# 检查是否已安装
which oh-gc || npm install -g @oh-gc/cli@0.7.5

# 如果 npm 全局路径不在 PATH 中，使用完整路径
OH_GC="/home/user/.npm-global/bin/oh-gc"
```

### Step 2: 配置认证

```bash
# 方式1：使用 oh-gc 登录（交互式）
oh-gc auth login

# 验证认证状态
oh-gc auth status
```

### Step 3: 配置 Personal Remote

```bash
# 查看现有 remote
git remote -v

# remote 名称不固定；从 git remote -v 中确认 GitCode 上游和 fork remote。
# 也可以跳过 remote 推导，直接在 oh-gc pr create 中使用 --repo 和 --head。
```

### Step 4: 提交代码

**Commit Message 格式要求**（DCO 标准）：

```
具体的改动说明

Co-Authored-By:Agent

Signed-off-by: 用户名 <邮箱>
```

示例：
```bash
git add frameworks/core/components_ng/pattern/overlay/overlay_manager.cpp
git commit -m "移除overlay_manager.cpp中未使用的头文件dynamic_module_helper.h

Co-Authored-By:Agent

Signed-off-by: your_username <your_email@example.com>"
```

### Step 5: 推送到 Personal Fork

```bash
# 跳过 LFS 验证推送
GIT_LFS_SKIP_SMUDGE=1 git push -u personal $(git branch --show-current) --no-verify
```

### Step 6: 创建 Issue（必须）

**重要：创建PR前必须先创建关联的Issue**

```bash
# 创建issue并获取编号
ISSUE_NUMBER=$(oh-gc issue create \
    --repo openharmony/arkui_ace_engine \
    --title "Issue标题" \
    --body "Issue描述内容" | grep -oP '#\d+' | head -1)

echo "Created Issue: $ISSUE_NUMBER"
# 输出示例：Created Issue: #12345
```

参数说明：
- `--repo`: 目标仓库
- `--title`: Issue 标题
- `--body`: Issue 描述

### Step 7: 创建 PR

**重要：使用目标仓库的PR模板，并填入Issue编号**

创建PR时，必须先查找并使用目标仓库的PR模板，在模板基础上修改内容，不要自定义格式。

**模板查找路径**（按优先级）：
1. `.gitcode/PULL_REQUEST_TEMPLATE.md`
2. `.github/PULL_REQUEST_TEMPLATE.md`
3. `docs/PULL_REQUEST_TEMPLATE.md`

```bash
# 1. 先按优先级查找目标仓库的 PR 模板
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

# 2. 读取模板内容作为 --body 的基础；如果没有模板，先向用户确认
```

**示例模板**（`.gitcode/PULL_REQUEST_TEMPLATE.md`）：
```markdown
**IssueNo**:
**Description**: (提交描述)
**Sig**: SIG_ApplicationFramework
**Binary Source**: No(涉及则Yes)

### Feature or Bugfix
- [ ] 需求/Feature
- [ ] 缺陷/Bugfix
### 是否涉及非兼容变更/Whether it involves incompatible changes
- [ ] 是/Yes
- [ ] 否/No
### TDD自验结果/TDD Self-Verification Results
- [ ] 通过/Pass
- [ ] 失败/Fail
- [ ] 不涉及/Not Involved
...
```

**创建PR命令**：
```bash
# 使用之前创建的Issue编号
ISSUE_NUMBER="#12345"  # 从Step 6获取

oh-gc pr create \
    --repo openharmony/arkui_ace_engine \
    --head your_username:test \
    --base master \
    --title "PR标题" \
    --body "$(sed "s/\*\*IssueNo\*\*:/\*\*IssueNo\*\*: $ISSUE_NUMBER/" "$TEMPLATE_FILE")"
```

参数说明：
- `--repo`: 上游目标仓库
- `--head`: 源分支，格式为 `{fork_owner}:{branch_name}`
- `--base`: 目标分支
- `--title`: PR 标题
- `--body`: PR 描述（**必须基于目标仓库的模板修改**）

## 常见问题

### 1. 推送失败：Permission denied

**原因**：没有直接推送到上游仓库的权限

**解决**：必须先 fork 仓库，然后推送到自己的 fork

### 2. 推送失败：LFS object not found

**原因**：LFS 对象同步问题

**解决**：使用 `GIT_LFS_SKIP_SMUDGE=1` 跳过 LFS 验证

### 3. oh-gc: command not found

**原因**：npm 全局 bin 目录不在 PATH 中

**解决**：
```bash
export PATH="$PATH:$(npm prefix -g)/bin"
# 或使用完整路径
/home/user/.npm-global/bin/oh-gc
```

### 4. 认证失败

**原因**：Token 过期或无效

**解决**：重新生成 Token 并更新配置
```bash
oh-gc auth login
```

## AI Agent 执行指南

对于 AI Agent，执行此工作流时应：

1. **预先确认目标信息**：
   - `oh-gc auth status` 显示的 GitCode 用户
   - `--repo` 对应的上游仓库
   - `--head` 对应的 fork owner 与分支
   - `--base` 对应的目标分支

2. **自动检测当前状态**：
   ```bash
   # 检查是否有未提交的改动
   git status --porcelain

   # 检查当前分支
   git branch --show-current

   # 检查 remote 配置
   git remote -v
   ```

3. **生成符合格式的 commit message**

4. **执行推送和创建 PR**

5. **返回 PR 链接给用户**

## 完整示例

```bash
# 场景：将 overlay_manager.cpp 的改动提交并创建 PR

USERNAME="your_username"
BRANCH="test"
UPSTREAM="openharmony/arkui_ace_engine"
oh-gc auth status

# 提交
git add frameworks/core/components_ng/pattern/overlay/overlay_manager.cpp
git commit -m "移除overlay_manager.cpp中未使用的头文件dynamic_module_helper.h

Co-Authored-By:Agent

Signed-off-by: your_username <your_email@example.com>"

# 推送到 personal fork
GIT_LFS_SKIP_SMUDGE=1 git push -u personal ${BRANCH} --no-verify

# 创建 PR 到上游
TEMPLATE_FILE=".gitcode/PULL_REQUEST_TEMPLATE.md"
ISSUE_NUMBER="#12345"
PR_BODY=$(sed "s/\\*\\*IssueNo\\*\\*:/\\*\\*IssueNo\\*\\*: $ISSUE_NUMBER/" "$TEMPLATE_FILE")

oh-gc pr create \
    --repo ${UPSTREAM} \
    --head ${USERNAME}:${BRANCH} \
    --base master \
    --title "移除overlay_manager.cpp中未使用的头文件dynamic_module_helper.h" \
    --body "$PR_BODY"
```
