# Architecture Rules

> 本目录承载 OpenHarmony SDD 架构类硬约束。AI Agent 在 `Specify`、`Design`、`Plan` 和 Post-Plan 实现阶段必须按影响范围加载对应规则。

## 规则索引

| Rule ID | 文件 | 主题 | 典型触发条件 |
|---------|------|------|--------------|
| OH-ARCH-LAYERING | `layering.md` | 分层架构和依赖方向 | 涉及应用层、框架层、系统服务层、内核层调用关系 |
| OH-ARCH-SUBSYSTEM | `subsystem-boundary.md` | 子系统边界 | 跨子系统、跨仓、跨部件调用 |
| OH-ARCH-IPC-SAF | `ipc-saf.md` | IPC/SAF 通信 | 新增/修改 System Ability、跨进程接口、远端调用 |
| OH-ARCH-API-LEVEL | `api-level.md` | API 分级、权限和兼容性 | 新增/修改 Public/System/Internal API |
| OH-ARCH-COMPONENT-BUILD | `component-build.md` | 部件、bundle.json、BUILD.gn | 新增 target、deps、部件依赖、SysCap |
| OH-ARCH-ERROR-LOG | `error-log.md` | 错误码、日志和诊断 | 新增错误路径、日志、诊断能力、问题定位要求 |

## AI Agent 加载策略

| 阶段 | 必须加载 |
|------|----------|
| Specify | 与行为规格、错误码、兼容性直接相关的规则 |
| Design | 与影响仓、模块、接口相关的所有架构规则 |
| Plan | 与任务文件范围、构建目标和验证方式直接相关的规则 |
| AI 实现 | Plan 或 Task Spec 中列出的 Rule ID |
| GB / GC | 所有关联 Rule ID 的 Evidence 和 Check |

## 输出要求

设计和规格文档中不复制规则全文，只记录：

```md
| Rule ID | 规则文件 | 适用性 | 本设计结论 | 验证方式 | 证据 |
```
