# oh-gc CLI — GitCode命令行工具

`oh-gc` 是[GitCode](https://gitcode.com)的命令行工具，模仿GitHub CLI (`gh`)。从终端管理认证、issues、pull requests、发布和仓库配置。

**安装包:** `npm install -g @oh-gc/cli` (需要 Node.js 18+)

## 前置条件

使用任何命令前：

1. **Token已配置？** 运行 `oh-gc auth:status`
   - 如果未登录 → `oh-gc auth:login` (提示输入GitCode个人访问令牌)
   - Token获取位置: `./assets/config.json`
2. **仓库上下文？** 选择以下方式之一：
   - 在包含`gitcode.com`远程仓库的git仓库内（远程仓库名可通过`oh-gc repo:set-remote <name>`配置），或者
   - 使用`--repo owner/repo`标志指定任意仓库

## 全局标志

所有命令支持：
- `--json` — 输出原始JSON而非格式化表格
- `--help` — 显示命令帮助

## 仓库标志

大多数操作仓库的命令支持`--repo`标志，允许在不进入git克隆的情况下指定目标仓库：

- `--repo owner/repo` — 以OWNER/REPO格式指定目标仓库

这适用于：
- 操作未在本地克隆的仓库
- 跨仓库操作（例如从fork向上游仓库创建PR）
- 需要与多个仓库交互的CI/CD脚本

```bash
# 列出任意仓库的issues
oh-gc issue:list --repo openharmony/arkui_ace_engine

# 不克隆仓库直接创建issue
oh-gc issue:create --repo owner/repo --title "Bug report"

# 查看其他仓库的PR
oh-gc pr:view 123 --repo owner/repo

# 跨仓库PR（fork到上游）
oh-gc pr:create --repo upstream-owner/repo --head my-feature --base main
```

## 命令参考

### 认证

```bash
oh-gc auth:login          # 使用个人访问令牌登录（交互式提示）
oh-gc auth:logout         # 移除已存储的令牌
oh-gc auth:status         # 显示当前用户信息
```

令牌存储位置：`./assets/config.json`

### Issues

```bash
# 列出
oh-gc issue:list                              # 打开的issues（默认）
oh-gc issue:list --state closed               # 已关闭的issues
oh-gc issue:list --state all                  # 所有issues
oh-gc issue:list --assignee alice             # 按指派人过滤
oh-gc issue:list --search "login bug"         # 按关键词搜索
oh-gc issue:list --limit 50                   # 最大结果数（默认：30）

# 查看
oh-gc issue:view 12                           # 显示issue详情+最近评论

# 创建
oh-gc issue:create                            # 交互模式
oh-gc issue:create --title "Bug" --body "..."         # 使用标志
oh-gc issue:create --repo owner/repo --title "Bug"    # 在其他仓库上
oh-gc issue:create --assignee alice --labels "bug,P0" # 带元数据

# 评论
oh-gc issue:comment 12                        # 交互式提示
oh-gc issue:comment 12 --body "Confirmed"     # 使用标志

# 关闭/重新打开
oh-gc issue:close 12                          # 关闭issue
oh-gc issue:reopen 12                         # 重新打开已关闭的issue

# 标签
oh-gc issue:labels 12 bug,feature             # 添加标签
oh-gc issue:labels 12 bug --remove            # 移除标签
```

### Pull Requests

```bash
# 列出
oh-gc pr:list                                 # 打开的PRs（默认）
oh-gc pr:list --state merged                  # 已合并的PRs
oh-gc pr:list --state all                     # 所有PRs
oh-gc pr:list --author alice                  # 按作者过滤
oh-gc pr:list --reviewer bob                  # 按评审人过滤
oh-gc pr:list --assignee carol                # 按指派人过滤
oh-gc pr:list --limit 50                      # 最大结果数（默认：30）

# 查看
oh-gc pr:view 5                               # 显示PR详情

# 创建
oh-gc pr:create                               # 交互模式
oh-gc pr:create --title "Fix bug" --base main         # 从当前分支
oh-gc pr:create --head feature --base main --draft    # 草稿PR
oh-gc pr:create --repo owner/repo --head my-feature   # 跨仓库PR

# 更新
oh-gc pr:update 5 --title "New title"         # 更新标题
oh-gc pr:update 5 --body "New description"    # 更新描述
oh-gc pr:update 5 --state closed              # 关闭PR
oh-gc pr:update 5 --state open                # 重新打开PR
oh-gc pr:update 5 --draft                     # 标记为草稿
oh-gc pr:update 5 --labels "bug,wip"          # 设置标签

# 关闭/重新打开
oh-gc pr:close 5                              # 关闭PR
oh-gc pr:reopen 5                             # 重新打开已关闭的PR

# 差异
oh-gc pr:diff 5                               # 显示带颜色的完整差异
oh-gc pr:diff 5 --name-only                   # 仅显示变更的文件名
oh-gc pr:diff 5 --color never                 # 无颜色（用于管道）

# 合并
oh-gc pr:merge 5                              # 合并提交（默认）
oh-gc pr:merge 5 --method squash              # Squash合并
oh-gc pr:merge 5 --method rebase              # Rebase合并

# 评论
oh-gc pr:comment 5 --body "LGTM!"                                    # 通用评论
oh-gc pr:comment 5 --body "Fix this" --path src/main.ts --line 10    # 行内评论
oh-gc pr:comment 5 --repo owner/repo --body "Note"                   # 在其他仓库上

# 列出/删除评论
oh-gc pr:comments 5                                   # 列出所有评论
oh-gc pr:comments 5 --comment-type diff_comment       # 仅差异/行内评论
oh-gc pr:comments 5 --comment-type pr_comment         # 仅通用评论
oh-gc pr:comments 5 --delete 12345                    # 按note_id删除

# 提交
oh-gc pr:commits 5                            # 列出PR中的提交

# 评审人
oh-gc pr:reviewers 5 alice,bob                # 指定评审人
oh-gc pr:reviewers 5 alice --append           # 添加到现有评审人
oh-gc pr:reviewers 5 alice --remove           # 移除评审人

# 测试人员
oh-gc pr:testers 5 alice,bob                  # 指定测试人员
oh-gc pr:testers 5 alice --append             # 添加到现有测试人员
oh-gc pr:testers 5 alice --remove             # 移除测试人员

# 评审和测试批准
oh-gc pr:review 5                             # 批准PR评审
oh-gc pr:review 5 --force                     # 强制批准
oh-gc pr:test 5                               # 标记测试通过
oh-gc pr:test 5 --force                       # 强制标记

# 标签
oh-gc pr:labels 5 bug,enhancement             # 添加标签
oh-gc pr:labels 5 bug --remove                # 移除标签

# 关联issues
oh-gc pr:link 5 1,2,3                         # 关联issues到PR
oh-gc pr:link 5 1,2 --remove                  # 取消关联issues

# 操作日志
oh-gc pr:logs 5                               # 显示PR操作历史
```

### 发布

```bash
oh-gc release:create                          # 使用package.json中的版本
oh-gc release:create v1.0.0                   # 指定版本
oh-gc release:create --prerelease             # 标记为预发布
oh-gc release:create v1.0.0 --notes "..."     # 自定义发布说明
```

### 仓库配置

```bash
oh-gc repo:get-remote                         # 显示oh-gc使用的远程仓库
oh-gc repo:set-remote upstream                # 使用不同的远程仓库
oh-gc repo:view                               # 查看仓库信息
oh-gc repo:update --description "..."         # 更新仓库设置
oh-gc repo:transfer <new-owner>               # 转移仓库所有权
```

远程仓库覆盖配置存储在仓库根目录的`.gitcode/oh-gc-config.json`中。

### 搜索

```bash
oh-gc search:repos "keyword"                  # 搜索仓库
oh-gc search:issues "keyword"                 # 跨仓库搜索issues
oh-gc search:code "keyword"                   # 跨仓库搜索代码
```

### 用户

```bash
oh-gc user:view                               # 查看您的个人资料
oh-gc user:view alice                         # 查看其他用户的个人资料
oh-gc user:emails                             # 列出您的邮箱地址
oh-gc user:followers                          # 列出您的关注者
oh-gc user:following                          # 列出您关注的用户
```

### 分支

```bash
oh-gc branch:list                             # 列出所有分支
oh-gc branch:list --protected                 # 仅列出受保护的分支
oh-gc branch:get <name>                       # 获取分支详情
oh-gc branch:protect <name>                   # 设置分支保护规则
```

### 提交

```bash
oh-gc commit:list                             # 列出提交
oh-gc commit:list --sha main                  # 列出特定分支的提交
oh-gc commit:get <sha>                        # 获取提交详情
oh-gc commit:diff <sha>                       # 查看提交差异
oh-gc commit:compare <base> <head>            # 比较两个提交或分支
```

### 文件

```bash
oh-gc file:get <path>                         # 获取文件内容（base64编码）
oh-gc file:raw <path> --ref main              # 获取原始文件内容
oh-gc file:list                               # 列出仓库文件
```

### 协作者

```bash
oh-gc collaborator:list                       # 列出仓库协作者
oh-gc collaborator:add <username>             # 添加协作者
oh-gc collaborator:remove <username>          # 移除协作者
oh-gc collaborator:permission <username>      # 获取协作者权限级别
```

### 标签

```bash
oh-gc label:list                              # 列出仓库标签
oh-gc label:get <name>                        # 获取标签详情
oh-gc label:create                            # 创建新标签
oh-gc label:update <name>                     # 更新标签
oh-gc label:delete <name>                     # 删除标签
```

### 里程碑

```bash
oh-gc milestone:list                          # 列出里程碑
oh-gc milestone:get <number>                  # 获取里程碑详情
oh-gc milestone:create                        # 创建新里程碑
oh-gc milestone:update <number>               # 更新里程碑
oh-gc milestone:delete <number>               # 删除里程碑
```

### Webhooks

```bash
oh-gc hook:list                               # 列出仓库webhooks
oh-gc hook:get <id>                           # 获取webhook详情
oh-gc hook:create                             # 创建webhook
oh-gc hook:delete <id>                        # 删除webhook
```

### Tags

```bash
oh-gc tag:list                                # 列出仓库tags
oh-gc tag:protect <name>                      # 保护tag
```

### 组织

```bash
oh-gc org:list                                # 列出您的组织
oh-gc org:view <org>                          # 获取组织详情
oh-gc org:members <org>                       # 列出组织成员
oh-gc org:repos <org>                         # 列出组织仓库
```

## 工作流：完整的PR生命周期

从代码变更到合并PR的完整工作流：

```
步骤1：创建PR
  oh-gc pr:create --title "Add feature X" --base main
  → 输出PR编号（例如 #42）

步骤2：分配人员
  oh-gc pr:reviewers 42 alice,bob
  oh-gc pr:testers 42 carol

步骤3：添加元元数据
  oh-gc pr:labels 42 feature,v2.0
  oh-gc pr:link 42 15,16           # 关联相关issues

步骤4：评审循环
  oh-gc pr:diff 42                 # 评审人检查差异
  oh-gc pr:comments 42             # 检查现有反馈
  oh-gc pr:comment 42 --body "LGTM"
  oh-gc pr:review 42               # 批准评审
  oh-gc pr:test 42                 # 标记测试通过

步骤5：合并
  oh-gc pr:merge 42 --method squash
```

## 工作流：Issue分类

```
步骤1：查找issues
  oh-gc issue:list --search "crash"
  oh-gc issue:list --state all --assignee alice

步骤2：检查
  oh-gc issue:view 15

步骤3：响应
  oh-gc issue:comment 15 --body "Investigating, likely related to #12"

步骤4：创建后续任务
  oh-gc issue:create --title "Fix crash on login" --labels "bug,P0" --assignee bob
```

## 工作流：跨仓库PR（Fork → Upstream）

用于向不拥有的仓库做贡献：

```
步骤1：从fork向上游仓库创建PR
  oh-gc pr:create --repo upstream-owner/repo --head my-feature --base master --title "Fix bug"

步骤2：在上游仓库上管理
  oh-gc pr:view 42 --json    # 检查状态
```

注意：`--repo`标志针对上游仓库。`--head`分支从您的fork解析。

## 决策树

```
用户想要与GitCode交互
  ↓
已登录？（oh-gc auth:status）
  ↓ 否 → oh-gc auth:login
  ↓ 是
在带有gitcode.com远程仓库的git仓库内？
  ↓ 否 → 使用--repo标志，或cd到仓库
  ↓ 是
用户想要做什么？
  ├─ 列出/查看issues      → oh-gc issue:list / issue:view
  ├─ 创建issue           → oh-gc issue:create
  ├─ 更新issue           → oh-gc issue:update
  ├─ 关闭/重新打开issue     → oh-gc issue:close / issue:reopen
  ├─ 在issue上评论       → oh-gc issue:comment
  ├─ 管理issue标签    → oh-gc issue:labels
  ├─ 列出/查看PRs          → oh-gc pr:list / pr:view
  ├─ 创建PR              → oh-gc pr:create
  ├─ 更新PR              → oh-gc pr:update
  ├─ 关闭/重新打开PR        → oh-gc pr:close / pr:reopen
  ├─ 查看PR差异         → oh-gc pr:diff
  ├─ 在PR上评论          → oh-gc pr:comment（通用）或 --path --line（行级）
  ├─ 分配评审人       → oh-gc pr:reviewers
  ├─ 分配测试人员         → oh-gc pr:testers
  ├─ 批准评审         → oh-gc pr:review
  ├─ 标记测试通过       → oh-gc pr:test
  ├─ 管理标签          → oh-gc pr:labels
  ├─ 关联issues到PR      → oh-gc pr:link
  ├─ 合并PR               → oh-gc pr:merge
  ├─ 查看PR历史        → oh-gc pr:logs
  ├─ 创建发布         → oh-gc release:create
  ├─ 搜索仓库/issues    → oh-gc search:repos / search:issues / search:code
  ├─ 查看用户资料      → oh-gc user:view:view
  ├─ 管理分支        → oh-gc branch:list / branch:get / branch:protect
  ├─ 查看提交/文件     → oh-gc commit:list / file:get
  ├─ 管理协作者   → oh-gc collaborator:list / add / remove
  ├─ 管理标签          → oh-gc label:list / create / update / delete
  ├─ 管理里程碑      → oh-gc milestone:list / create / update
  ├─ 管理webhooks        → oh-gc hook:list /:list / create / delete
  └─ 配置远程仓库       → oh-gc repo:set-remote / repo:get-remote
```

## 错误处理

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| "Not logged in" | 未配置令牌 | `oh-gc auth:login` |
| "Authentication failed" | 令牌过期或无效 | 使用新令牌重新运行 `oh-gc auth:login` |
| "Remote not found" | 不在git仓库内或远程仓库缺失 | `cd` 到仓库，检查 `git remote -v` |
| "Not a GitCode repository" | 远程仓库URL不是 `gitcode.com` | 添加gitcode.com远程仓库 |
| "Could not connect" | 网络问题或代理未设置 | 检查网络；如果使用代理，设置 `https_proxy` 环境变量 |
| "Rate limit exceeded" | API调用过多 | 等待并重试 |
| "API error 405" | 错误的HTTP方法（内部） | 更新oh-gc到最新版本 |

## 提示

- 使用 `--json` 将输出通过管道传递给 `jq` 用于脚本：`oh-gc pr:list --json | jq '.[].title'`
- 使用 `--repo owner/repo` 在不先克隆的情况下操作任意仓库
- 交互模式（无标志）会提示输入必填字段 — 适用于一次性操作
- `oh-gc pr:comments --comment-type diff_comment` 仅过滤代码评审评论
- `oh-gc pr:reviewers --append` 添加评审人而不替换现有的
- `oh-gc pr:update --state closed` 是在不合并的情况下关闭PR的方式
