# OpenHarmony Skills

OpenHarmony Skills 仓库，收集面向 OpenHarmony / HarmonyOS 开发、审查、构建、测试和提交流程的可复用技能定义，供 AI 助手按场景调用。

## 简介

本仓库聚焦 OpenHarmony 工程实践，包含代码审查、安全检视、编译构建、问题分析、文档生成、自动化测试、PR 工作流和专项领域开发等技能。

这些技能的目标是把常见任务沉淀为结构化流程，帮助 AI 助手在具体场景下更稳定地执行检查、分析、生成和提交流程。

## 适用场景

- OpenHarmony C++ / ArkTS / ArkUI 代码开发与审查
- 系统服务、安全、并发、内存问题分析
- 编译、构建、CI、日志和错误定位
- API 文档检查、设计文档生成、PRD 分析
- 自动化测试、XTS 测试生成与执行
- GitCode / PR / Issue 工作流处理
- 图形、应用、迁移、运行时等专项场景

## 技能分组

### 1. 代码审查与安全检视

用于代码质量评估、安全风险识别、规范检查和专项 review。

- `ai-generated-business-code-review`：AI 生成业务代码质量审查
- `ai-generated-ut-code-review`：AI 生成单测代码质量审查
- `code-checker`：代码规模、复杂度、循环依赖检查
- `comprehensive-code-review`：综合代码审查
- `cpp-core-guidelines-review`：C++ Core Guidelines 专项审查
- `dsoftbus-security`：分布式软总线安全审查
- `log-coverage-analyzer`：日志覆盖率与日志风险分析
- `oh-distributed-security-design-review`：分布式系统安全设计检视
- `oh-memory-leak-detection`：NAPI 内存泄漏检测
- `openharmony-security-review`：OpenHarmony 系统服务安全审查
- `openharmony-thread-safety-review`：线程安全专项审查

### 2. 构建编译与问题定位

用于编译、构建、性能分析、错误诊断和运行问题定位。

- `afwk-hb-build`：ability_runtime 组件智能编译
- `build-error-analyzer`：构建错误与链接错误分析
- `code-problem-analyzer`：代码行为异常与根因分析
- `compile-analysis`：编译耗时、依赖和单文件编译分析
- `header-optimization`：头文件依赖优化
- `oh-precommit-codecheck`：提交前代码检查
- `oh-stability`：稳定性问题分析
- `openharmony-build`：OpenHarmony 全量或目标编译
- `openharmony-ci`：CI 状态、日志和产物排查
- `openharmony-download`：源码下载与环境准备

### 3. 文档、设计与代码生成

用于文档质量检查、需求分析、接口设计、架构设计和代码骨架生成。

- `api-doc-checker`：API 文档规范与一致性检查
- `appmgr-api-generator`：AppMgr 接口实现链路生成
- `arkts-static-spec`：ArkTS 静态语言规范参考
- `arkui-api-design`：ArkUI API 设计与变更指导
- `generate-interface-uml`：接口 UML / 时序图生成
- `oh-docs-check-zh-cn`：OpenHarmony 中文 API 文档一致性检查
- `oh-interfaces-ipc-to-service`：graphic_2d IPC ToService 通路生成
- `oh-pdd-prd-analysis`：PRD 分析与需求抽取
- `oh-pdd-design-doc-generator`：设计文档生成
- `oh-pdd-code-generator`：代码框架与配置生成

### 4. 测试、自动化与验证

用于自动化测试生成、测试执行、应用调试和测试工程支持。

- `arkts-sta-playground`：ArkTS-Sta 代码片段执行
- `arkui-menu-debug`：ArkUI Menu 问题专项调试
- `arkweb-app-debug`：ArkWeb 应用调试
- `harmonyos-autotest`：HarmonyOS 自动化测试工作流
- `oh-ut-generator`：单元测试生成
- `oh-xts-build-run`：XTS 编译与运行
- `oh-xts-generator-template`：XTS 用例模板生成
- `ohos-app-build-debug`：应用构建、安装、启动和调试
- `openharmony-ut`：OpenHarmony 单测支持
- `xts-generator`：XTS 测试生成

### 5. PR、Issue 与 GitCode 工作流

用于提交代码、创建 Issue / PR、评审和仓库协作流程。

- `audio_pr_create`：GitCode 仓库协作与 PR 操作
- `create-pr`：通用 PR 创建流程
- `gitcode-cli`：使用 `oh-gc` 进行 GitCode 操作
- `gitcode-pr`：GitCode PR 提交流程
- `graphic-2d-PR`：graphic_2d 仓 PR 创建流程
- `oh-graphic-gitcode-pr-creator`：图形子系统 GitCode PR 自动化
- `oh-pr-workflow`：OpenHarmony PR 工作流
- `review-gitcode-pr`：GitCode PR 审查

### 6. OpenHarmony 平台与专项开发

用于特定子系统、专项模块、跨平台适配和领域开发任务。

- `android-to-harmonyos-migration-workflow`：Android 到 HarmonyOS 迁移工作流
- `arkuix-module-adapter`：OHOS 模块跨平台适配
- `cpp-include-sorter`：C/C++ `#include` 自动整理
- `ets-runtime-dev`：`ets_runtime` 开发工作流
- `graphic-2d-format`：graphic_2d 增量格式化
- `oh-add-memory-trace-tags`：内存追踪标签扩展
- `oh-graphic-pixel-tests-generator`：图形像素测试生成
- `openharmony-arkts-layer`：ArkTS 分层开发支持
- `openharmony-cpp`：OpenHarmony C++ 开发规范

## 如何使用

### 下载方式

可通过 `npx` 直接安装整个仓库，或仅安装指定 Skill。

安装整个仓库：

```bash
npx skill add openharmonyinsight/openharmony-skills
```

安装单个 Skill：

```bash
npx skills add openharmonyinsight/openharmony-skills --skill <skill_name>
```

其中 `<skill_name>` 替换为 `skills/` 目录下的具体技能名，例如 `openharmony-security-review`。

### 使用方式

1. 克隆本仓库到本地工作环境。
2. 将 `skills/` 目录作为技能来源提供给你的 AI 助手。
3. 根据任务场景选择或触发相应技能。
4. 如需新增技能，在 `skills/<skill-name>/` 下创建目录并补充 `SKILL.md` 及必要参考资料。

## 仓库结构

```text
openharmony-skills/
├── skills/                          # 技能根目录
│   ├── openharmony-security-review/ # 安全审查
│   │   └── SKILL.md
│   ├── openharmony-build/           # 编译构建
│   │   └── SKILL.md
│   ├── oh-docs-check-zh-cn/         # 文档检查
│   │   └── SKILL.md
│   ├── harmonyos-autotest/          # 自动化测试
│   │   └── SKILL.md
│   └── ...                          # 其他专项技能
└── README.md
```

## 添加新 Skill

1. 在 `skills/` 目录下创建新的技能目录。
2. 编写 `SKILL.md`，明确适用场景、触发条件、执行流程和约束。
3. 如有必要，补充 `references/`、`assets/` 或 `scripts/` 目录。
4. 保持技能命名清晰、职责单一、说明可执行。

## 贡献

欢迎提交新的技能定义或改进现有技能。提交前请确保：

- 遵循现有技能目录结构和命名方式
- 说明技能适用场景、输入条件和预期产出
- 尽量提供结构化流程、检查清单或决策规则
- 引用的脚本、模板和参考资料可以直接复用

## 许可证

请查看 LICENSE 文件了解许可证信息。

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。
