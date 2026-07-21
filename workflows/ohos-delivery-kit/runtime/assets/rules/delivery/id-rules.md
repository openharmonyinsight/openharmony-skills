# ID Rules

## 稳定 ID 格式

| 对象 | 格式 | 示例 |
|------|------|------|
| 变更目录（已关联 issue） | `issue-<issue-number>-<short-slug>` | `issue-12345-arkui-focus` |
| 变更目录（未关联 issue） | `draft-<yyyymmdd>-<short-slug>` | `draft-20260522-arkui-focus` |
| Task | `TASK-NNN-short-slug` | `TASK-001-focus-logic` |

## 约束

R-ID-001: issue-number 为源码平台（GitCode 等）的 issue ID
R-ID-002: short-slug 使用小写英文、数字和连字符，不超过 40 字符
R-ID-003: ID 和路径中不得包含 `target_release`
R-ID-004: ID 在 `.codespec/` 范围内全局唯一
