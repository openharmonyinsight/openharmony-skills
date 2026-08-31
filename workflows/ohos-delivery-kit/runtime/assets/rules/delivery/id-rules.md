# ID Rules

## 稳定 ID 格式

| 对象 | 格式 | 示例 |
|------|------|------|
| 变更目录（正式） | `<req-id>-<english-slug>` | `REQ-12345-arkui-focus` |
| 变更目录（草稿） | `draft-<yyyymmdd>-<english-slug>` | `draft-20260522-arkui-focus` |
| Task | `TASK-<N>` | `TASK-1`、`TASK-2`、`TASK-10` |

> Task ID 使用正整数编号，不要求补零（`TASK-1` 而非 `TASK-001`）。
> 校验器 `TASK_RE = \bTASK-\d+\b` 匹配任意位数数字。

## 约束

R-ID-001: 正式目录位于 `codespec/changes/` 下，`req-id` 由开发者提供；其格式为字母、数字和内部连字符，且必须以字母或数字开头和结尾。`issue-<digits>`（不区分大小写）为保留的旧格式，不可用作 `req-id`。
R-ID-002: `english-slug` 使用小写英文、数字和连字符；连字符只可分隔非空片段，且总长度不超过 40 字符。正式目录的 `proposal.md` frontmatter 必须提供完全相同的 `req:`，目录必须以精确的 `<req-id>-` 前缀开头。
R-ID-003: ID 和路径中不得包含 `target_release`
R-ID-004: 目录名在 `codespec/` 范围内全局唯一
