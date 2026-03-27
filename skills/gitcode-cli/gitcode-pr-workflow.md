# GitCode PR 自动化工作流程

本文档描述如何自动将本地代码改动提交并创建 PR 到 GitCode 上游仓库。

## Remote 命名规范

| Remote 名称 | 用途 | URL 格式 |
|-------------|------|----------|
| `gitcode` | 上游原始仓库 | `https://gitcode.com/{org}/{repo}.git` |
| `personal` | 个人 Fork 仓库 | `https://{username}:{token}@gitcode.com/{username}/{repo}.git` |

**重要**：所有仓库统一使用此命名规范，便于自动化脚本识别。

> ⚠️ **安全提示**
>
> 不要将含 Token 的 URL 提交到 git 历史记录中。如果误提交，请立即：
> 1. 撤销相关 commit 或使用 `git filter-branch` / `BFG Repo-Cleaner` 清理历史
> 2. 在 GitCode 设置中**立即重新生成 Token**
>
> 建议做法：
> - 使用环境变量存储 Token，而非硬编码在脚本中
> - 将含 Token 的配置文件添加到 `.gitignore`
> - 使用 `git remote set-url` 时避免在终端历史中留下明文 Token

## 前置条件

在执行此工作流之前，**必须**确认以下信息已配置：

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| `GITCODE_TOKEN` | GitCode 访问令牌 | GitCode → 个人设置 → 访问令牌 |
| `GITCODE_USERNAME` | GitCode 用户名 | 即个人主页路径中的用户名 |
| `UPSTREAM_REPO` | 上游仓库名称 | 从 `git remote get-url gitcode` 解析 |
| `UPSTREAM_BRANCH` | 上游目标分支 | 默认：`master` |

**Fork 地址自动拼接规则**：
- 如果 `personal` remote 不存在，自动根据上游仓库和用户名拼接
- 格式：`https://{username}:{token}@gitcode.com/{username}/{repo_name}.git`
- 例如：上游 `openharmony/arkui_ace_engine` → Fork `{username}/arkui_ace_engine`

## 一键执行脚本

将以下变量替换为实际值后执行：

> ⚠️ **注意**：建议从环境变量读取 Token，避免硬编码。示例：`GITCODE_TOKEN="${GITCODE_TOKEN:-$GITCODE_TOKEN_ENV}"`

```bash
# ===== 配置区 =====
# 建议：从环境变量读取，避免硬编码 Token
GITCODE_TOKEN="${GITCODE_TOKEN:-your_token_here}"
GITCODE_USERNAME="${GITCODE_USERNAME:-your_username}"
UPSTREAM_BRANCH="master"
CURRENT_BRANCH=$(git branch --show-current)

# 自动从 gitcode remote 解析上游仓库信息
UPSTREAM_URL=$(git remote get-url gitcode 2>/dev/null || echo "")
# 解析仓库名: https://gitcode.com/openharmony/arkui_ace_engine.git -> openharmony/arkui_ace_engine
REPO_NAME=$(echo "$UPSTREAM_URL" | sed -E 's|.*/([^/]+/[^/]+)(\.git)?|\1|')
UPSTREAM_REPO="$REPO_NAME"

# 自动拼接 fork 地址
PERSONAL_URL="https://${GITCODE_USERNAME}:${GITCODE_TOKEN}@gitcode.com/${GITCODE_USERNAME}/${REPO_NAME#*/}.git"

# ===== 执行步骤 =====
# 1. 安装 oh-gc CLI（如未安装）
npm install -g @oh-gc/cli 2>/dev/null

# 2. 配置 oh-gc 认证
mkdir -p ~/.config/gitcode-cli
echo "{\"token\": \"$GITCODE_TOKEN\"}" > ~/.config/gitcode-cli/config.json

# 3. 配置 personal remote（如不存在则自动创建）
if ! git remote | grep -q "^personal$"; then
    git remote add personal "$PERSONAL_URL"
else
    git remote set-url personal "$PERSONAL_URL"
fi

# 4. 提交改动（如有未提交的改动）
# 注意：commit message 必须符合 DCO 格式
if git diff --quiet && git diff --cached --quiet; then
    echo "No changes to commit"
else
    git add -A
    git commit -m "具体的改动说明

Co-Authored-By:Agent

Signed-off-by: ${GITCODE_USERNAME} <${GITCODE_USERNAME}@users.noreply.gitcode.com>"
fi

# 5. 推送到 personal fork
GIT_LFS_SKIP_SMUDGE=1 git push -u personal ${CURRENT_BRANCH} --no-verify

# 6. 创建 PR
/home/user/.npm-global/bin/oh-gc pr:create \
    --repo ${UPSTREAM_REPO} \
    --head ${GITCODE_USERNAME}:${CURRENT_BRANCH} \
    --base ${UPSTREAM_BRANCH} \
    --title "PR标题" \
    --body "## Summary
- 改动说明1
- 改动说明2

## Test plan
- [ ] 代码审核通过
- [ ] 编译验证通过

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

## 详细步骤说明

### Step 1: 检查并安装 oh-gc CLI

```bash
# 检查是否已安装
which oh-gc || npm install -g @oh-gc/cli

# 如果 npm 全局路径不在 PATH 中，使用完整路径
OH_GC="/home/user/.npm-global/bin/oh-gc"
```

### Step 2: 配置认证

```bash
# 方式1：使用 oh-gc 登录（交互式）
oh-gc auth:login

# 方式2：直接写入配置文件（非交互式）
mkdir -p ~/.config/gitcode-cli
echo '{"token": "YOUR_TOKEN"}' > ~/.config/gitcode-cli/config.json

# 验证认证状态
oh-gc auth:status
```

### Step 3: 配置 Personal Remote

```bash
# 查看现有 remote
git remote -v

# 从 gitcode remote 自动解析仓库信息
UPSTREAM_URL=$(git remote get-url gitcode)
REPO_NAME=$(echo "$UPSTREAM_URL" | sed -E 's|.*/([^/]+/[^/]+)(\.git)?|\1|')
# REPO_NAME 例如: openharmony/arkui_ace_engine

# 自动拼接 personal fork 地址
PERSONAL_URL="https://${USERNAME}:${TOKEN}@gitcode.com/${USERNAME}/${REPO_NAME#*/}.git"
# PERSONAL_URL 例如: https://your_username:token@gitcode.com/your_username/arkui_ace_engine.git

# 添加或更新 personal remote
if ! git remote | grep -q "^personal$"; then
    git remote add personal "$PERSONAL_URL"
else
    git remote set-url personal "$PERSONAL_URL"
fi
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
ISSUE_NUMBER=$(oh-gc issue:create \
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
# 1. 先查找目标仓库的PR模板
TEMPLATE_FILE=$(find . -name "PULL_REQUEST_TEMPLATE.md" 2>/dev/null | head -1)

# 2. 读取模板内容作为 --body 的基础
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

oh-gc pr:create \
    --repo openharmony/arkui_ace_engine \
    --head your_username:test \
    --base master \
    --title "PR标题" \
    --body "$(cat .gitcode/PULL_REQUEST_TEMPLATE.md | sed "s/\*\*IssueNo\*\*:/\*\*IssueNo\*\*: $ISSUE_NUMBER/" | sed 's/(提交描述)/实际改动描述/')"
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
oh-gc auth:login
```

## AI Agent 执行指南

对于 AI Agent，执行此工作流时应：

1. **预先确认配置信息**（只需首次确认）：
   - GitCode Token
   - GitCode 用户名
   - Fork 仓库地址
   - 用户邮箱（用于 Signed-off-by）

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

# 配置
TOKEN="your_token_here"
USERNAME="your_username"
BRANCH="test"

# 自动解析上游仓库
UPSTREAM_URL=$(git remote get-url gitcode)
REPO_NAME=$(echo "$UPSTREAM_URL" | sed -E 's|.*/([^/]+/[^/]+)(\.git)?|\1|')
UPSTREAM="${REPO_NAME}"  # openharmony/arkui_ace_engine

# 自动拼接 personal fork 地址
PERSONAL_URL="https://${USERNAME}:${TOKEN}@gitcode.com/${USERNAME}/${REPO_NAME#*/}.git"

# 配置 personal remote
git remote set-url personal "$PERSONAL_URL" 2>/dev/null || \
git remote add personal "$PERSONAL_URL"

# 提交
git add frameworks/core/components_ng/pattern/overlay/overlay_manager.cpp
git commit -m "移除overlay_manager.cpp中未使用的头文件dynamic_module_helper.h

Co-Authored-By:Agent

Signed-off-by: your_username <your_email@example.com>"

# 推送到 personal fork
GIT_LFS_SKIP_SMUDGE=1 git push -u personal ${BRANCH} --no-verify

# 创建 PR 到上游
/home/user/.npm-global/bin/oh-gc pr:create \
    --repo ${UPSTREAM} \
    --head ${USERNAME}:${BRANCH} \
    --base master \
    --title "移除overlay_manager.cpp中未使用的头文件dynamic_module_helper.h" \
    --body "## Summary
- 移除 overlay_manager.cpp 中未使用的头文件 dynamic_module_helper.h

```
