# 编码开发 (Development)

代码审查、代码生成、编码规范、编译构建、头文件优化等开发阶段技能。

## Skills

- [ohos-dev-arkts-sta-playground](ohos-dev-arkts-sta-playground/)：通过 ArkTS-Sta Playground HTTP API 执行或编译 ArkTS-Sta 代码片段。
- [ohos-dev-arkts-static-specification-reference](ohos-dev-arkts-static-specification-reference/)：ArkTS 静态语言规范参考与 TypeScript 迁移指南，用于 ArkTS 类型系统、编译期行为、语义规则的查询与验证。
- [ohos-dev-build-execution-diagnosis](ohos-dev-build-execution-diagnosis/)：OpenHarmony 构建执行、增量验证和 build.log 失败诊断。
- [ohos-dev-cpp-coding-style](ohos-dev-cpp-coding-style/)：OpenHarmony C++ 编码规范检查与修复。
- [ohos-dev-gitcode-pr-review](ohos-dev-gitcode-pr-review/)：结合 `oh-gc` 与本地代码上下文执行 GitCode PR 深度评审并准备评论草稿。
- [ohos-dev-hdc-command-usage](ohos-dev-hdc-command-usage/)：HarmonyOS `hdc` 命令使用、设备连接、文件传输、应用安装、日志与常见问题排查。
- [ohos-dev-security-code-review](ohos-dev-security-code-review/)：OpenHarmony C++ 系统服务安全代码审查，覆盖 IPC、并发、敏感日志和权限校验。

## 文档质量检视

| Skill | 说明 |
| --- | --- |
| [ohos-dev-docs-api-reference-review/](ohos-dev-docs-api-reference-review/) | API 参考文档检视 |
| [ohos-dev-docs-code-correctness-review/](ohos-dev-docs-code-correctness-review/) | 文档代码正确性检视 |
| [ohos-dev-docs-dev-guide-review/](ohos-dev-docs-dev-guide-review/) | 开发指南检视 |
| [ohos-dev-docs-pr-diff-review/](ohos-dev-docs-pr-diff-review/) | 文档 PR 改动检视 |
| [ohos-dev-docs-writing-compliance-review/](ohos-dev-docs-writing-compliance-review/) | 文档写作合规检视 |

## 文档检视入口选择

按用户要求的范围选主入口，不因都是文档就同时启动全部技能。

| 请求 | 优先入口 | 补充边界 |
| --- | --- | --- |
| 中文 API 模板、公开/系统 API、错误码文档与 d.ts/实现一致性 | `ohos-dev-chinese-docs-review` | “符合模板并与 d.ts 一致”归此入口 |
| 整篇 API/指南七维质量、声明式规则台账、Excel 报告 | `ohos-design-api-doc-checking` | 位于 `domain/app-framework/design` |
| 明确的目标版本下参数语义、默认值、错误条件或线程/生命周期契约专项 | `ohos-dev-docs-api-reference-review` | 不重复全量模板/声明审计 |
| 指定任务从输入、工程/权限到可观察结果的操作断点 | `ohos-dev-docs-dev-guide-review` | 不代替七维综合评估 |
| 叙述、术语、排版、图表展示和示例风格专项 | `ohos-dev-docs-writing-compliance-review` | 不承担 API 契约或任务链正确性审计 |
| 仅检视 PR 变更（含文档图片） | `ohos-dev-docs-pr-diff-review` | 先限定变更范围，再按上述边界加载所需规则 |

组合时主入口保留覆盖台账，专项只补未覆盖项；同文件、侧别/位置和根因的问题合并依据后计一次。各规则体系分别统计覆盖，不直接相加分母；未安装、未运行或缺少证据的范围明确列为未覆盖。既有技能是可选协作项，不是单独运行新增专项的强制依赖。
