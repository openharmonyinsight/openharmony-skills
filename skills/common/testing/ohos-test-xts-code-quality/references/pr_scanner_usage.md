# pr_scanner.py 使用指南

> 版本: v1.0 | 更新: 2026-04-27

## 概述

`pr_scanner.py` 是 GitCode PR 文件拉取脚本，支持：
- PR 变更文件下载
- Diff 上下文解析（unified diff → new line / hunk info）
- 已有 PR 评论获取（用于结果去重）
- 统一认证（oh-gc CLI > --token > GITCODE_TOKEN 环境变量）

## 快速开始

```bash
# 基本用法（自动检测 oh-gc 认证）
python scripts/pr_scanner.py "https://gitcode.com/openharmony/xts_acts/pull/123" --json

# 使用 Token
python scripts/pr_scanner.py "https://gitcode.com/.../pull/123" --token ghp_xxx --output ./pr_scan/

# 跳过 Diff 或评论获取
python scripts/pr_scanner.py "https://gitcode.com/.../pull/123" --token ghp_xxx --no-diff --no-comments
```

## 完整参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `pr_url` | 是 | - | GitCode PR URL（gitcode.com/{owner}/{repo}/pull/{id}） |
| `--token` | 否 | 自动检测 | GitCode PAT，不提供时自动检测 oh-gc 或 GITCODE_TOKEN |
| `--output` | 否 | 临时目录 | 输出目录（默认创建系统临时目录） |
| `--json` | 否 | false | 以 JSON 格式输出结果 |
| `--no-diff` | 否 | false | 跳过 Diff 上下文获取 |
| `--no-comments` | 否 | false | 跳过已有评论获取 |

## 认证方式（二选一）

### 方式一：oh-gc CLI（推荐）

oh-gc 是 GitCode 官方命令行工具，安装后自动检测认证，无需手动管理 Token。

```bash
# 安装（需要 Node.js 18+）
npm install -g @oh-gc-cli

# 登录认证
oh-gc auth:login
# 输入 GitCode Personal Access Token: ••••••••••
# Token 获取地址: https://gitcode.com/-/profile/personal_access_tokens

# 验证登录状态
oh-gc auth:status
```

安装完成后，本工具会自动检测 `oh-gc`，Diff 获取、评论获取、评论提交均优先通过 oh-gc CLI 执行。

### 方式二：Token 直传

不安装 oh-gc 时，通过 `--token` 参数或 `GITCODE_TOKEN` 环境变量提供认证。

```bash
# 方式 2a: 命令行参数
python scripts/pr_scanner.py "https://gitcode.com/.../pull/123" --token ghp_xxx

# 方式 2b: 环境变量（适合 CI/CD 场景）
export GITCODE_TOKEN=ghp_xxx
python scripts/pr_scanner.py "https://gitcode.com/.../pull/123"
```

Token 获取地址: https://gitcode.com/-/profile/personal_access_tokens

### 认证优先级

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | `oh-gc` CLI | 自动检测安装，复用已有认证 |
| 2 | `--token` 参数 | 显式提供的 Token |
| 3 | `GITCODE_TOKEN` 环境变量 | 系统环境变量 |

> **提示**: 两种方式在功能上完全等价（Diff 上下文感知、评论去重、评论提交均支持）。oh-gc 的优势是认证复用更方便，适合本地开发；Token 直传更适合 CI/CD 等自动化场景。

## 输出格式

### JSON 输出（`--json`）

```json
{
  "owner": "openharmony",
  "repo": "xts_acts",
  "pr_id": "123",
  "pr_title": "fix test case",
  "local_dir": "/tmp/xts_pr_xxx",
  "changed_files": ["entry/src/.../xxx.test.ets"],
  "file_count": 15,
  "auth_method": "oh-gc",
  "diff_files": ["entry/src/.../xxx.test.ets"],
  "diff_file_count": 10,
  "existing_comments_count": 5
}
```

### PRScanResult 对象属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `owner` | str | 仓库 owner |
| `repo` | str | 仓库名 |
| `pr_id` | str | PR 编号 |
| `pr_title` | str | PR 标题 |
| `local_dir` | str | 下载文件本地目录 |
| `changed_files` | list[str] | 变更文件路径列表 |
| `file_contents` | dict | 文件路径→内容映射 |
| `diff_context` | dict | Diff 上下文（parse_unified_diff 结果） |
| `existing_comments` | list[dict] | 已有评论列表 |
| `auth_method` | str | 认证方式（"oh-gc" / "token"） |

### Diff 上下文结构

```python
{
  "path/to/file.test.ets": {
    "hunks": [
      {"header": "@@ -10,3 +10,4 @@", "old_start": 10, "old_count": 3, "new_start": 10, "new_count": 4}
    ],
    "new_added_lines": {11, 13},
    "commentable_lines": [10, 11, 12, 13]
  }
}
```

## Python API

```python
from pr_scanner import PRScanner, parse_unified_diff, deduplicate_issues

scanner = PRScanner(token="your_token")
result = scanner.fetch_pr_files(
    "https://gitcode.com/openharmony/xts_acts/pull/123",
    fetch_diff=True,
    fetch_comments=True,
)

# 检查某行是否为新增行
result.is_pure_new_line("foo.test.ets", 25)

# 获取 hunk 信息
hunk = result.get_hunk_info("foo.test.ets", 25)

# 去重已有评论
new_issues = deduplicate_issues(scan_results, result.existing_comments, result.diff_context)
```

## 独立工具函数

### `parse_unified_diff(diff_text)`

解析 unified diff 文本，返回 per-file 结构。

### `deduplicate_issues(issues, existing_comments, diff_context)`

过滤已有评论报告过的问题和非 Diff 新增行的问题。

### `is_oh_gc_available()`

检测 oh-gc CLI 是否可用。

### `resolve_token(token=None)`

解析认证 Token，返回 (token, auth_method)。

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| "No authentication available" | 无 Token 且无 oh-gc | 安装 oh-gc 或提供 --token |
| "oh-gc pr:diff failed" | oh-gc 认证过期 | 运行 `oh-gc auth login` |
| "Failed to fetch diff" | REST API 不可用 | 检查网络，或使用 oh-gc |
| 下载文件数为 0 | PR 无相关文件 | 确认 PR 包含 .ets/.ts/.js 等文件 |
