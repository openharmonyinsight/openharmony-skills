# Power GitCode API Reference

## API 基础信息

- Base URL: `https://api.gitcode.com/api/v5`
- 认证方式: Bearer Token (Header) 或 access_token (Query Param)
- Token 来源: 环境变量 `gitcode_password` 或 `gitcode_token`

## PR 接口

| 操作 | 方法 | 路径 |
|------|------|------|
| 创建 PR | POST | `/repos/{owner}/{repo}/pulls` |
| 获取 PR 详情 | GET | `/repos/{owner}/{repo}/pulls/{number}` |
| 获取 PR commits | GET | `/repos/{owner}/{repo}/pulls/{number}/commits` |
| 获取 PR 修改文件 | GET | `/repos/{owner}/{repo}/pulls/{number}/files` |
| 获取 PR 评论 | GET | `/repos/{owner}/{repo}/pulls/{number}/comments` |
| 发表 PR 评论 | POST | `/repos/{owner}/{repo}/pulls/{number}/comments` |

### PR 评论参数
- `body` (必填) - 评论内容
- `path` (可选) - 文件的相对路径，用于代码行评论
- `position` (可选) - 代码所在行数，用于代码行评论

| 添加 PR 标签 | POST | `/repos/{owner}/{repo}/pulls/{number}/labels` |
| 移除 PR 标签 | DELETE | `/repos/{owner}/{repo}/pulls/{number}/labels/{label}` |
| 分配测试人员 | POST | `/repos/{owner}/{repo}/pulls/{number}/testers` |
| 合并 PR | PUT | `/repos/{owner}/{repo}/pulls/{number}/merge` |

### 合并方式
- `merge` - 普通合并
- `squash` - 压缩合并
- `rebase` - 变基合并

## Issue 接口

| 操作 | 方法 | 路径 |
|------|------|------|
| 创建 Issue | POST | `/repos/{owner}/issues` (body 含 repo 字段) |
| 获取 Issue 详情 | GET | `/repos/{owner}/{repo}/issues/{number}` |
| 添加 Issue 标签 | POST | `/repos/{owner}/{repo}/issues/{number}/labels` |

### Issue 响应字段
- `id` - Issue ID
- `html_url` - 网页链接
- `number` - Issue 编号
- `state` - 状态
- `title` - 标题
- `body` - 内容
- `user` - 创建者
- `labels` - 标签列表
- `issue_state` - Issue 状态
- `comments` - 评论数
- `priority` - 优先级
- `issue_type` - Issue 类型
- `created_at` / `updated_at` / `finished_at` - 时间戳

## PR-Issue 关联接口

| 操作 | 方法 | 路径 |
|------|------|------|
| PR 关联的 Issue | GET | `/repos/{owner}/{repo}/pulls/{number}/issues` |
| Issue 关联的 PR | GET | `/repos/{owner}/{repo}/issues/{number}/pull_requests` |

## 仓库接口

| 操作 | 方法 | 路径 |
|------|------|------|
| Fork 仓库 | POST | `/repos/{owner}/{repo}/forks` |
| 创建 Release | POST | `/repos/{owner}/{repo}/releases` |
| 创建标签 | POST | `/repos/{owner}/{repo}/labels` |
| 检查仓库公开性 | GET | `/repos/{owner}/{repo}` |

## 模板路径

- Issue 模板: `.gitcode/ISSUE_TEMPLATE/` (支持 .md 和 .yml)
- PR 模板: `.gitcode/PULL_REQUEST_TEMPLATE/` (支持 .md)
- 语言选择: 文件名含 zh/cn/chinese 优先中文，含 en/english 优先英文
