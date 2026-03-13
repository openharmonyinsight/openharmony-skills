# oh-pr-workflow：OpenHarmony PR 全生命周期工作流

一站式管理 OpenHarmony GitCode 仓库的代码提交、PR 创建、门禁修复、代码检视和检视意见修复。

## 功能

| 模式 | 触发方式 | 说明 |
|------|---------|------|
| 提交代码 | "提交"、"commit" | 标准化 commit（DCO 签名 + Issue 关联） |
| 创建 PR | "创建PR"、"提个PR" | 提交 + 推送 + 创建 Issue + 创建 PR + 触发门禁 |
| 修复门禁告警 | "修复告警"、"修复codecheck" + PR链接 | 从门禁获取缺陷列表并自动修复 |
| Review PR | "review pr" + PR链接 | 拉取 PR 代码到本地进行代码检视 |
| 修复检视意见 | "修复review" + PR链接 | 获取未解决的 review 意见并修复 |

## 安装

### 前置条件（必须）

- Claude Code CLI 已安装
- **GitCode 个人访问令牌已配置**：
  ```bash
  git config --global gitcode.token YOUR_TOKEN
  ```
  令牌获取方式：[GitCode 个人设置](https://gitcode.com/-/profile/personal_access_tokens) → 访问令牌 → 创建新令牌（需要 `api` 和 `read_api` 权限）

  > 这是使用本 skill 的**唯一需要手动配置的步骤**，其余全部自动完成。

### 支持的 Agent

| Agent | 支持方式 |
|-------|---------|
| Claude Code | skill 原生支持，首次使用自动安装 |
| OpenCode | 通过 MCP 工具调用，需运行 setup.sh |

### 自动安装

首次使用 skill 时会**自动检测并安装** GitCode MCP 服务：

- Linux x86_64：直接使用内置二进制，无需额外依赖
- 其他平台：需要 Go 1.22+，从源码自动编译

也可手动安装：
```bash
bash ~/.claude/skills/oh-pr-workflow/gitcode-mcp/setup.sh
```

`setup.sh` 会自动检测已安装的 Agent 并注册：
- 检测到 `claude` CLI → 注册到 `~/.claude.json`
- 检测到 `opencode` CLI → 注册到 `~/.config/opencode/opencode.json`
- 都没检测到 → 输出手动注册命令

安装完成后需**重启 Agent 会话**以加载 MCP 工具。

### 版本管理

`setup.sh` 会自动管理版本：
- 源码变更 → 自动重新编译
- 二进制被官方版本覆盖 → 自动重新安装
- 已是最新 → 跳过

## 使用方式

### 提交代码

```
/oh-pr-workflow 提交
```

自动生成标准化 commit message：
```
type(scope): 描述（≤49字符）

Issue: https://gitcode.com/openharmony/repo/issues/N
Signed-off-by: Name <email>
Co-Authored-By: Agent
```

- 邮箱从 GitCode 账号自动获取并缓存
- Issue 自动从分支 commit 中检测，没有则自动创建

### 创建 PR

```
/oh-pr-workflow 创建PR
/oh-pr-workflow 创建PR --target feature_branch
```

完整流程：提交 → 推送 → 检查重复 PR → 确定 Issue → 创建 PR（使用仓库模板）→ `start build` 触发门禁。

### 修复门禁告警

```
/oh-pr-workflow 修复告警 https://gitcode.com/openharmony/repo/pull/123
```

从 DCP 平台获取 codecheck 缺陷列表，按规则自动修复（花括号、命名、nullptr 等），修复后 squash 进原始 commit 并 force push。

### Review PR

```
/oh-pr-workflow review pr https://gitcode.com/openharmony/repo/pull/123
```

通过 API 获取 PR 的精确 commits、files、patches，拉取到本地分支 `review/pr-{N}` 进行代码检视。Review 完成后保留本地分支供后续查看。

### 修复检视意见

```
/oh-pr-workflow 修复review https://gitcode.com/openharmony/repo/pull/123
```

获取 PR 中未解决的 `diff_comment` 类型评论，自动检测过期意见，展示修复方案并**等待用户确认**后执行。修复后 squash 进原始 commit。

## 目录结构

```
oh-pr-workflow/
├── SKILL.md                          # Skill 定义（触发条件、完整流程）
├── README.md                         # 本文档
├── references/
│   ├── commit-format.md              # Commit message 格式规范
│   └── issue_template.md             # Issue 创建模板
├── scripts/
│   └── fetch_gate_defects.sh         # DCP 门禁缺陷获取脚本
└── gitcode-mcp/                      # GitCode MCP 服务（修改版）
    ├── setup.sh                      # 一键安装脚本
    ├── bin/
    │   └── gitcode-mcp-linux-amd64   # 内置预编译二进制
    ├── main.go
    ├── go.mod / go.sum
    ├── api/                          # API 层（含 FlexInt、user.go 等修改）
    ├── config/
    └── mcp/tools/                    # MCP 工具层（含 GetIntArg、create_pr_comment 等）
```

## GitCode MCP 修改说明

本 skill 包含的 GitCode MCP 基于官方 [gitcode-org-com/gitcode-mcp](https://github.com/gitcode-org-com/gitcode-mcp) 修改，新增/修复了以下内容：

| 改动 | 说明 |
|------|------|
| `FlexInt` 类型 | 兼容 GitCode API 返回 string 类型的数字字段 |
| `json.RawMessage` ID | 兼容 MongoDB ObjectID（非数字 ID） |
| `GetIntArg` 辅助函数 | 兼容 Claude Code 传参类型不一致（float64/string） |
| `PRBranch` 结构体 | PR 的 head/base 返回完整分支信息（ref、sha、repo） |
| `get_authenticated_user` | 新增：获取当前用户邮箱 |
| `list_pr_commits` | 新增：获取 PR 精确 commit 列表 |
| `list_pr_files` | 新增：获取 PR 精确变更文件列表（含 patch） |
| `create_pr_comment` | 新增：创建 PR 评论（触发门禁等） |
