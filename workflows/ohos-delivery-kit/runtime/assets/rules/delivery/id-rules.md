# ID Rules

## 稳定 ID 格式

| 对象 | 格式 | 示例 |
|------|------|------|
| 仓库目录 | `<repo-name>` | `arkui` |
| 变更目录（正式） | `<req-id>` | `REQ-12345` |
| 变更目录（草稿） | `draft-<yyyymmdd>-<english-slug>` | `draft-20260522-arkui-focus` |
| Task | `TASK-<N>` | `TASK-1`、`TASK-2`、`TASK-10` |

> Task ID 使用正整数编号，不要求补零（`TASK-1` 而非 `TASK-001`）。
> 校验器 `TASK_RE = \bTASK-\d+\b` 匹配任意位数数字。

## 约束

R-ID-001: 正式目录位于 `codespec/changes/<repo-name>/<req-id>/`，`repo-name` 优先取 Git `origin` URL 的仓名（去掉 `.git`），无 `origin` 时取工作树根目录名；`req-id` 由开发者提供，其格式为字母、数字和内部连字符，且必须以字母或数字开头和结尾。`issue-<digits>`（不区分大小写）为保留的旧格式，不可用作 `req-id`。
R-ID-002: `english-slug` 仅用于草稿目录，使用小写英文、数字和连字符；连字符只可分隔非空片段，且总长度不超过 40 字符。正式目录叶子必须与 `proposal.md` frontmatter 的 `req:` 完全相同，不保留 slug。
R-ID-003: ID 和路径中不得包含 `target_release`
R-ID-004: `<repo-name>/<req-id>` 在 `codespec/changes/` 范围内唯一
