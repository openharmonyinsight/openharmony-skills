---
name: gitcode-pr
description: GitCode 仓库 PR 提交流程。可作为独立 subagent 运行。覆盖：创建 Issue、分支、提交、创建 PR、合并。
---

# GitCode PR 提交流程

## 运行模式

### 模式 A：Subagent 模式（推荐）

作为独立 subagent 被 `arkweb-architect` 调用时，文件列表和提交信息已在 task 描述中提供，直接执行。

**输入格式（从 task 描述中解析）：**
```
## 待提交文件
{文件路径列表}

## 提交信息
- Issue 标题：docs: {feature-name} — {description}
- Commit message: docs: {description}\n\n- {change_1}\n- {change_2}\n\nCo-Authored-By:Agent\nSigned-off-by: {git config user.name} <{git config user.email}>
- PR body: 方案概述 + 评审记录 + Closes #{issue_number}
- 分支名：docs/{feature-name}

## 仓库配置
- 仓库：zhufenghao/AI-assisted-design
- 本地路径：{project_root}
- Token：从环境变量读取（优先 `GITCODE_TOKEN`，回退 `GITLAB_TOKEN`）
```

**输出：** Issue + PR 创建结果 → 回复 URL 和状态

### 模式 B：交互模式

在主 session 中直接调用，每步确认后执行。

---

## 概述

所有代码提交到 GitCode 仓库必须遵循 **Issue → 分支 → 提交 → PR** 流程，禁止直接 push 到 master。

## 仓库配置

| 仓库 | GitCode 路径 | 本地路径 |
|------|-------------|---------|
| AI 辅助设计 | `zhufenghao/AI-assisted-design` | `{project_root}` |
| AI Dashboard | `zhufenghao/ai-dashboard` | `{project_root}` |
| 鸿蒙知识库 | `openharmony-ai-design/oh-ai-full-design` | 见 memory |

### API 配置

- **Token:** 优先 ，回退 （环境变量或  文件）
- **API 基础路径:** `https://gitcode.com/api/v5`
- **认证方式:** `PRIVATE-TOKEN` header
- **调用工具:** 必须使用 **Python 3 `urllib`**（见下方说明）

### 变量定义

| 变量 | 含义 | 取值方式 |
|------|------|---------|
| `FORK_OWNER` | fork 仓库的 owner（GitCode 用户名） | 从 git remote URL 中解析：`git remote get-url origin` → 提取 owner 部分（如 `git@gitcode.com:{FORK_OWNER}/chromium_src.git`） |

> **推荐使用 Python 3 `urllib` 调用 GitCode repos API。** 部分环境的 curl（如 7.81.0）在 HTTPS 模式下可能无法正确发送 `PRIVATE-TOKEN` header 到 GitCode 的 `/repos` 路径（HTTP/2 网关兼容性问题）。如果 Python 3 不可用，可使用 `curl --http1.1` 强制 HTTP/1.1 作为降级方案。

## 标准 API 调用模板

所有 GitCode API 调用使用以下 Python 模板：

```bash
python3 -c "
import urllib.request, json, os

token = os.environ.get('GITCODE_TOKEN') or os.environ.get('GITLAB_TOKEN') or exit('Error: set GITCODE_TOKEN or GITLAB_TOKEN')
base = 'https://gitcode.com/api/v5/repos/{owner}/{repo}'

# --- 按需替换以下部分 ---
url = f'{base}/issues'
data = json.dumps({'title': 'TITLE', 'body': 'BODY'}).encode()
method = 'POST'
# --- 替换结束 ---

req = urllib.request.Request(url, data=data, method=method)
req.add_header('PRIVATE-TOKEN', token)
req.add_header('Content-Type', 'application/json')
try:
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    print(json.dumps(result, ensure_ascii=False, indent=2))
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:500]}')
"
```

## 多仓库 PR 协调规则

ArkWeb 项目涉及 3 个仓库的协同提交，必须遵循以下规则：

### 仓库清单

| 仓库 | 上游原仓 | fork 仓库 | 本地路径 | 默认 base |
|------|---------|----------|---------|----------|
| chromium_src | `openharmony-tpc/chromium_src` | `{FORK_OWNER}/chromium_src` | `{SKILL_HOME}/src` | `132_trunk` |
| web_webview | `openharmony/web_webview` | `{FORK_OWNER}/web_webview` | `{SKILL_HOME}/deps_code/webview` | `master` |
| arkui_ace_engine | `openharmony/arkui_ace_engine` | `{FORK_OWNER}/arkui_ace_engine` | `{SKILL_HOME}/deps_code/arkui_ace_engine` | `master` |

### Issue 分组规则

**同一层级的仓库共用一个 Issue，不同层级使用独立 Issue：**

| 层级 | 仓库 | Issue 创建位置 |
|------|------|---------------|
| 引擎层 | chromium_src（独立） | `openharmony-tpc/chromium_src` |
| 框架层 | web_webview + arkui_ace_engine（共用） | `openharmony/web_webview`（在 web_webview 仓库创建，ace_engine PR 中引用同一 Issue 链接） |

### PR 方向规则

**所有 PR 必须从 fork 指向上游原仓，禁止 fork 内部自合并：**

```
正确：
  {FORK_OWNER}/chromium_src:feat/xxx  →  openharmony-tpc/chromium_src:132_trunk
  {FORK_OWNER}/web_webview:feat/xxx   →  openharmony/web_webview:master
  {FORK_OWNER}/arkui_ace_engine:feat/xxx → openharmony/arkui_ace_engine:master

错误：
  {FORK_OWNER}/chromium_src:feat/xxx  →  {FORK_OWNER}/chromium_src:master
```

### PR 模板强制读取规则

**创建 PR body 之前，必须先读取目标仓库的 PR 模板文件。** 不同仓库的模板路径和格式不同：

| 仓库 | 模板路径 |
|------|---------|
| chromium_src | `.gitcode/PULL_REQUEST_TEMPLATE.zh-CN.md` |
| web_webview | `.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md` |
| arkui_ace_engine | `.gitcode/PULL_REQUEST_TEMPLATE.md` |

模板读取失败或未找到时，使用本 skill 中的默认模板。

### 标准提交流程顺序

```
1. 在每个仓库创建分支 → 提交代码 → push 到 fork 远程
2. 创建 Issue（按分组规则）
3. 读取每个仓库的 PR 模板
4. 填充模板 + 关联 Issue + 设计文档索引
5. 创建跨仓库 PR（fork → 上游原仓）
6. 互相在 PR body 中引用关联 PR 链接
```

## 标准流程

### Step 0: 创建 Issue（前置必须）

**创建 PR 前必须先创建 Issue。** Issue 是 PR 的追溯入口，不可跳过。

```
Issue 创建规则：
- 按上述「Issue 分组规则」确定在哪个仓库创建
- 同一层级的仓库共用一个 Issue
- 不同层级使用独立 Issue
- Issue body 应包含：需求描述、涉及仓库列表、关联 PR（创建后回填）
```

```bash
python3 -c "
import urllib.request, json, os

token = os.environ.get('GITCODE_TOKEN') or os.environ.get('GITLAB_TOKEN') or exit('Error: set GITCODE_TOKEN or GITLAB_TOKEN')
url = 'https://gitcode.com/api/v5/repos/{owner}/{repo}/issues'
data = json.dumps({'title': ISSUE_TITLE, 'body': ISSUE_BODY}).encode()

req = urllib.request.Request(url, data=data, method='POST')
req.add_header('PRIVATE-TOKEN', token)
req.add_header('Content-Type', 'application/json')
resp = urllib.request.urlopen(req, timeout=15)
result = json.loads(resp.read().decode())
print(f'Issue #{result[\"number\"]}: {result[\"html_url\"]}')
"
```

**Issue 命名规范：**
- 文档类：`docs: {简要描述}`
- 功能类：`feat: {简要描述}`
- 修复类：`fix: {简要描述}`
- 重构类：`refactor: {简要描述}`

### Step 2: 创建分支并提交

```bash
cd {本地仓库路径}
git checkout master && git pull origin master
git checkout -b {type}/{short-description}
git add -A

# 获取 git 配置的署名信息
SIGN_OFF=$(git config user.name && echo " <$(git config user.email)>")

git commit -m "{type}: {subject}

- {detail_1}
- {detail_2}

Co-Authored-By:Agent
Signed-off-by: ${SIGN_OFF}"

git push -u origin {type}/{short-description}
```

**分支命名规范：** `docs/xxx` / `feat/xxx` / `fix/xxx` / `refactor/xxx`

**Commit message 规范（Conventional Commits）：**
```
type: subject

- 详细变更项 1
- 详细变更项 2

Co-Authored-By:Agent
Signed-off-by: {user.name} <{user.email}>
```

**必填项：**
- `Co-Authored-By:Agent` — 固定格式，无尖括号无邮箱
- `Signed-off-by:` — 使用 `git config user.name` 和 `git config user.email` 的值

### Step 3: 创建 PR

创建 PR 前必须读取仓库的 PR 模板，用实际内容填充后作为 body 提交。

**PR body 组成规则：**

1. **读取模板**：从仓库本地路径读取 PR 模板文件（按优先级查找）：
   - `.gitcode/PULL_REQUEST_TEMPLATE.zh-CN.md`
   - `.gitcode/PULL_REQUEST_TEMPLATE.md`
   - `.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md`
   - `.gitee/PULL_REQUEST_TEMPLATE.md`
   - `.github/PULL_REQUEST_TEMPLATE.md`
   - `PULL_REQUEST_TEMPLATE.md`
   - 若以上均不存在，使用默认模板（见下方）

2. **填充模板**：将模板中的占位项替换为实际内容：
   - 关联 Issue → `Closes #N`
   - 修改描述 → 需求概述 + 涉及仓库 + 变更摘要
   - 入库必检项 → 按实际情况填写
   - 检视闭环 → 是/否

3. **附加设计文档索引**：在 body 末尾附加本次工作流产出的设计文档清单，格式如下：

```markdown
---

## 设计文档

- 需求提案：[proposal.md]({DOCS_REPO_URL}/blob/master/docs/features/{feature-name}/proposal.md)
- 需求基线：[{date}-{feature}-requirement.md]({DOCS_REPO_URL}/blob/master/docs/features/{feature-name}/{date}-{feature}-requirement.md)
- 架构设计：[{date}-{feature}-design.md]({DOCS_REPO_URL}/blob/master/docs/features/{feature-name}/{date}-{feature}-design.md)
- 方案评审：[{date}-{feature}-brainstorm.md]({DOCS_REPO_URL}/blob/master/docs/features/{feature-name}/{date}-{feature}-brainstorm.md)
- 设计评审：[{date}-{feature}-review.md]({DOCS_REPO_URL}/blob/master/docs/features/{feature-name}/{date}-{feature}-review.md)
- 统一规格：[spec.md]({DOCS_REPO_URL}/blob/master/docs/features/{feature-name}/spec.md)
- 代码分析：[{date}-{feature}-analysis.md]({DOCS_REPO_URL}/blob/master/analysis/{date}-{feature}-analysis.md)
- Committer 检视：[{date}-{feature}-committer-review.md]({DOCS_REPO_URL}/blob/master/docs/features/{feature-name}/{date}-{feature}-committer-review.md)
```

> `{DOCS_REPO_URL}` 为 `AI-assisted-design` 仓库的 GitCode Web URL（如 `https://gitcode.com/zhufenghao/AI-assisted-design`）。如果设计文档不在 GitCode 仓库中，使用本地绝对路径。

**默认模板（无仓库模板时使用）：**

```markdown
### 关联的issue：
Closes #N

### 修改描述：
{需求概述}

涉及仓库：{仓库名列表}

### 入库必检项
是否涉及非兼容变更: {是/否}
TDD自验结果: {Pass/Fail/不涉及}
XTS自验结果: {Pass/Fail/不涉及}
检视意见是否都已闭环: {是/否}
```

**调用示例：**

```bash
python3 -c "
import urllib.request, json, os

token = os.environ.get('GITCODE_TOKEN') or os.environ.get('GITLAB_TOKEN') or exit('Error: set GITCODE_TOKEN or GITLAB_TOKEN')
url = 'https://gitcode.com/api/v5/repos/{owner}/{repo}/pulls'

# body 内容由模板填充 + 设计文档索引组合而成
body = TEMPLATE_CONTENT + '\n\n---\n\n## 设计文档\n' + DOCS_INDEX

data = json.dumps({
    'title': 'PR标题',
    'head': '源分支名',
    'base': '132_trunk',  // chromium_src 用 132_trunk，其他仓库用 master
    'body': body
}).encode()

req = urllib.request.Request(url, data=data, method='POST')
req.add_header('PRIVATE-TOKEN', token)
req.add_header('Content-Type', 'application/json')
resp = urllib.request.urlopen(req, timeout=30)
result = json.loads(resp.read().decode())
print(f'PR #{result[\"number\"]}: {result[\"html_url\"]}')
"
```

**注意事项：**
- **跨仓库 PR（fork → 上游）**：POST 到**上游原仓**的 `/pulls` 端点，`head` 参数必须带 owner 前缀，格式为 `{fork_owner}:{branch_name}`。切勿 POST 到 fork 仓库自身，否则会创建 fork 内部自合并 PR。
- 关联 Issue 在 body 中写 `Closes #N`
- 端点是 `/pulls`，不是 `/merge_requests`
- 创建 PR 可能较慢（后端需计算 diff），timeout 设为 30 秒
- body 内容必须包含模板填充 + 设计文档索引两部分
- **504 Backend timeout 时先查询再重试**：超时可能已在服务端创建成功，先查 `GET /pulls?state=open&head={branch}` 确认，避免重复创建

### Step 4: 合并 PR

**Subagent 模式：** 不自动合并，等待主 session 决策 4 确认。

**交互模式：** 如果用户要求合并：
```bash
python3 -c "
import urllib.request, json, os

token = os.environ.get('GITCODE_TOKEN') or os.environ.get('GITLAB_TOKEN') or exit('Error: set GITCODE_TOKEN or GITLAB_TOKEN')
url = 'https://gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{pr_number}/merge'

req = urllib.request.Request(url, method='PUT')
req.add_header('PRIVATE-TOKEN', token)
req.add_header('Content-Type', 'application/json')
resp = urllib.request.urlopen(req, timeout=30)
result = json.loads(resp.read().decode())
print(f'PR merged: {result.get(\"state\", \"merged\")}')
"
```

## GitCode API 速查

| 操作 | 方法 | 端点 |
|------|------|------|
| 创建 Issue | POST | `/repos/{owner}/{repo}/issues` |
| 关闭 Issue | PATCH | `/repos/{owner}/{repo}/issues/{number}` |
| 创建 PR | POST | `/repos/{owner}/{repo}/pulls` |
| 关闭 PR | PATCH | `/repos/{owner}/{repo}/pulls/{number}` |
| 获取 PR | GET | `/repos/{owner}/{repo}/pulls/{number}` |
| 合并 PR | PUT | `/repos/{owner}/{repo}/pulls/{number}/merge` |

**关闭 Issue/PR 注意事项：**
- 使用 `PATCH` 方法，不是 `PUT`
- 参数为 `state_event: close`（不是 `state: closed`）
- `state_event` 只接受 `close` 或 `reopen`

## 错误处理

- **404 on `/pulls`**: 确认使用 `repos/{owner}/{repo}/pulls`
- **409**: 同一分支已有 PR，检查现有 PR
- **400 body不能为空**: Issue 创建时 body 至少填 "test"
- **504 Backend timeout**: PR 创建超时，重试即可（可能已创建成功，先查询再重试）
- **405 Method Not Allowed**: 检查 HTTP 方法是否正确（关闭操作用 PATCH，不是 PUT）
- **Token 失效**: 检查  或  环境变量是否设置

## 自动化检查清单

- [ ] 分支名符合规范
- [ ] Commit message 使用 Conventional Commits
- [ ] Commit message 包含 Co-Authored-By:Agent
- [ ] Commit message 包含 Signed-off-by: (取自 git config)
- [ ] API 调用使用 Python urllib（不使用 curl）
- [ ] Issue 已创建且内容完整（按分层规则，同层共用 Issue）
- [ ] PR 描述中包含 Issue 链接或 `Closes #N`
- [ ] PR body 使用了仓库的 PR 模板（已读取模板文件，非自定义格式）
- [ ] PR body 包含设计文档索引（链接到 AI-assisted-design 仓库）
- [ ] PR 方向正确：fork → 上游原仓（非 fork 内部自合并）
- [ ] `head` 参数使用 `{fork_owner}:{branch}` 格式（跨仓库 PR）
- [ ] 多仓库 PR 之间互相引用了关联 PR 链接
- [ ] 没有直接 push 到 master

## Subagent 回复格式

```
✅ gitcode-pr 完成
📋 Issue: #{number} — {title}
🔀 PR: #{number} — {title}
🔗 PR URL: {url}
📂 分支: {branch_name}
📊 状态: {open/merged}
```
