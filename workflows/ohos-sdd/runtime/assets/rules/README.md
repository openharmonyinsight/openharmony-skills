# OpenHarmony SDD Rules

> 本目录是 OpenHarmony SDD 流程的规则源。AI Agent 在 Define、Specify、Design、Plan 以及 Post-Plan 的实现和验证阶段，应按任务类型加载相关规则，并在输出文档中记录 Rule ID、适用性、设计结论和验证证据。

## 目录职责

| 目录 | 职责 | 使用阶段 |
|------|------|----------|
| `architecture/` | 分层、子系统边界、IPC/SAF、API、部件构建、错误日志等架构规则 | `spec.md`、`design.md`、`execution-plan.md`、AI 实现、GC 审查 |

## 使用方式

1. 在 `Specify / Design` 阶段识别适用规则。
2. 在 `spec.md` 和 `design.md` 中记录规则适用性、设计结论和验证方式。
3. 在 `execution-plan.md` 或 Task Spec 中把适用规则拆到具体文件和实现约束。
4. 在 GB / GC 审查中检查规则是否被设计、代码和测试证据覆盖。

## 规则文件格式

每个规则文件应包含以下信息：

| 字段 | 说明 |
|------|------|
| Rule ID | 稳定规则编号，供模板、门禁和 AI Agent 引用 |
| Applies To | 适用阶段和变更类型 |
| Must | 必须满足的约束 |
| Must Not | 明确禁止的行为 |
| Evidence | 需要留下的设计、代码、测试或评审证据 |
| Check | 人工或自动化检查方式 |

## 与其他目录的关系

| 目录 | 关系 |
|------|------|
| `skills/` | SDD 流程 skill（ohos-*）通过 design.md 的 Rule ID 引用本目录规则，不重复维护规则正文 |
| `templates/` | 模板记录规则适用性、结论和证据，不承载完整规则正文 |
| `docs/` | 文档解释流程和背景，可引用本目录作为规范源 |
| `templates/gate-checklist.md` | 质量门禁按 Rule ID 检查设计、实现和验证是否闭环 |
