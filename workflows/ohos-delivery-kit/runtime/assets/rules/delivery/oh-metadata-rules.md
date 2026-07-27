# OH Metadata Rules

## target_release

R-OH-001: `target_release` 是版本事实唯一来源
R-OH-002: 文档正文引用 `target_release`，不复制为新的事实源

R-OH-003: `target_release` 是**发布版本号**，不是分支名
- 格式：`<major>.<minor>`（Release 为默认，无需后缀），如 `7.0`、`7.1`
- 可选 stage 后缀（仅非默认版本用）：`<major>.<minor>-<Beta|Alpha|Dev>`，如 `7.1-Beta`
- Release 是默认值：首选 `7.0`，`7.0-Release` 也合法但冗余
- **反例**：`master`、`dev`、`beta` 等分支名不是发布版本，不得作为 `target_release`（分支回答"在哪开发"，版本回答"随哪期交付"）
- 旧格式 `OpenHarmony-<major>.<minor>-<stage>`（如 `OpenHarmony-6.0-Release`）已废弃：`OpenHarmony-` 前缀冗余、stage 默认 Release 无需显式。存量归档沿用旧格式时由 `validate-artifacts-contract.py` 给出 warning，提示统一为 `<major>.<minor>`。

R-OH-004: `target_release` 可按发布惯例**委婉推断**（半自动，不强制）
- OpenHarmony 每年一个大版本（`x.0`）+ 一个小版本（`x.1`）。按月份窗口判断当前推断目标：
  - 7–10 月（年中/下半年）→ 小版本窗口
  - 11–12 月 + 1–6 月（年底/上半年）→ 大版本窗口
- 维护表 `release_calendar`（每年更新一行）：

  | 年份 | 大版本 | 小版本 |
  |------|--------|--------|
  | 2025 | 6.0 | 6.1 |
  | 2026 | 7.0 | 7.1 |
  | 2027 | 8.0 | 8.1 |

  > 维护点：每年新增一行。表为显式数据，不耦合进 ODK 代码；OH 实际发版节奏若调整，更新此表即可。
- 推断仅供 `odk-init` 提示参考：向用户呈现为「按惯例推断是 X，请明确输入实际目标版本」，**不替用户自动填入**——最终值由用户明确给出（可覆盖，如提前为下个版本铺路）。validator 不强制 `target_release` 等于推断值。
