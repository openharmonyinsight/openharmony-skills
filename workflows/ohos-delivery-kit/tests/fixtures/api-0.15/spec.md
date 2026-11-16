## API 规格定义

### Proposal 覆盖矩阵

| Proposal 条目 | 类型 | spec 承接位置 | 状态 |
|---------------|------|----------------|------|
| Add the sample API | goal | AC-1.1 | Covered |
| No unsupported device behavior | non-goal | N/A: internal implementation only | N/A |
| Sample timing assumption | assumption | EB-1.1 | Covered |
| Sample open question | open question | Open-1 | Open |

契约文件：`arkts-api-spec.yaml`

| 项 | 值 |
|---|---|
| Schema 版本 | 1.0.0 |
| API 契约版本 | 1.0.0 |

### API 概览

| API ID | 类型 | 完整签名 | @since | 确认状态 |
|---|---|---|---|---|
| sample.run | method | run(): void | 1.0.0 | 已确认 |

### API 事实溯源与待确认项

| API 事实 | 结果 | 来源 | 状态 |
|----------|------|------|------|
| `@since` | 1.0.0 | sample API version rule | 已确认 |
| `@syscap` | SystemCapability.ArkUI.ArkUI.Full | sample API contract | 已确认 |
| 权限 | 无 | sample API contract | 已确认 |
| 跨平台 / 元服务 / 卡片支持 | 均不支持 | developer confirmation | 已确认 |
| FA / Stage 模型 | FA 与 Stage 均支持 | developer confirmation | 已确认 |
| 设备支持与行为差异 | 待确认 | sample device knowledge | 待确认 |
