# CLAUDE.md — OpenHarmony AI Agent 指令

> 本文件供 Claude Code / Cursor 等 AI 编码工具自动读取。放置在仓根目录即可生效。

## 项目概述

OpenHarmony 是面向全场景的开源分布式操作系统。项目采用多仓协作模式，包含数百个 Git 仓库，由多个 SIG（Special Interest Group）分工治理。

核心原则：**Spec 是真相来源，代码是实现细节。** 所有变更必须先有 Spec，再由 AI 辅助实现。

## 技术栈

| 层级 | 语言 | 框架/工具 |
|------|------|----------|
| 应用层 / 框架层 | ArkTS (TypeScript 扩展) | ArkUI 声明式框架 |
| 系统服务层 | C/C++ | SAF (System Ability Framework) |
| 构建系统 | GN + Ninja | bundle.json 部件声明 |
| 测试框架 | ArkTS / C++ | Hypium / gtest / XTS |

## 项目结构

OpenHarmony 采用 **子系统 (Subsystem) → 部件 (Component) → 模块 (Module)** 三层组织模型：

```
子系统 (Subsystem)
├── bundle.json             # 部件清单
└── 部件A (Component)
    ├── bundle.json         # 部件声明
    ├── BUILD.gn            # GN 构建入口
    ├── src/                # 源码
    ├── interfaces/         # 对外接口
    │   ├── inner_api/      # 内部 API
    │   └── kits/           # 公开 API
    └── test/               # 测试
```

## SDD 工作流（4 阶段主流程）

所有变更遵循规范驱动开发流程：

```
Phase 1: 定义      → proposal.md（需求澄清与基线，一份文档从进入到基线）
Phase 2: 规格说明  → spec.md（特性规格）
Phase 3: 设计      → design.md（架构设计）
Phase 4: 计划      → execution-plan.md + task.md

后续执行与交付：review.md + 验证 + 合入 + 复盘
```

### 按复杂度裁剪

| 复杂度 | 定义 | 设计 | Spec | 实现 | 审查 |
|--------|------|------|------|------|------|
| **简单** (单仓小修) | proposal.md (核心字段) | 跳过 | spec.md (核心 AC) | task.md (1-2 Tasks) | review.md (仅决策) |
| **标准** (单/双仓特性) | proposal.md (全量) | design.md (关键决策) | spec.md (全量) | execution-plan + task.md | review.md (规范+质量) |
| **复杂** (多仓/SIG) | proposal.md + epic.md | design.md (全量+扩展) | spec.md (全量+场景库) | 全量 Plan + 多 task.md | review.md (全量) |
| **关键** (安全/性能) | 同复杂 | design.md (全量+安全/性能专项) | spec.md (全量+合规) | 全量 Plan + 专家 | review.md (全量+专项) |

公共模板位于 `templates/`：proposal.md, spec.md, design.md, execution-plan.md, task.md, epic.md, bugfix.md, test-spec.md, regression-test.md, review.md, scenario-library.md, gate-checklist.md。Profile 专属模板位于 `profiles/<name>/templates/`。

## 硬规则

- **Approved 才能流转** — 当前阶段未完成，不得进入下一阶段
- **计划之前不得实现** — Plan 未通过前，不得修改生产代码
- **实现不得扩范围** — AI 只能修改 Plan 和 Task 列出的文件
- **先定义不涉及项** — 需求阶段先明确 N/A 维度
- **先符合 Spec，再谈代码质量** — 规范符合性审查先于代码质量审查
- **证据先于声明** — 没有运行过验证命令，就不能声称"通过了"

## 编码规范

### ArkTS

- **命名**: 类/接口/枚举用 PascalCase；函数/变量用 camelCase；常量用 UPPER_SNAKE_CASE
- **类型**: 必须添加类型注解，禁止使用 `any`
- **异步**: 必须使用 `async/await` 或 `Promise`
- **模块**: 使用 ES Module (`import/export`)，禁止 CommonJS

### C/C++

- **风格**: 遵循 Google C++ Style Guide
- **内存**: 必须使用智能指针，禁止裸 `new/delete`
- **RAII**: 所有资源管理必须遵循 RAII 原则

### 通用

- **错误码**: 遵循 OH 统一错误码规范
- **日志**: 使用 HiLog，禁止 `console.log` 或 `printf`
- **国际化**: 禁止硬编码用户可见字符串

## 约束和禁止事项

### 禁止（红线）

- **禁止** 未经 Spec 审批修改 Public API 签名
- **禁止** 跨层直接调用（应用层直接调用内核层接口）
- **禁止** 反向依赖（下层依赖上层）
- **禁止** 新增依赖时不更新 bundle.json
- **禁止** 异步操作缺少错误处理
- **禁止** 硬编码路径、密钥、凭证
- **禁止** 跨子系统直接引用内部类

### 必须

- **必须** 遵循四层架构的单向依赖规则
- **必须** 在 bundle.json 中声明所有外部依赖
- **必须** 为新增 Public API 添加 SysCap 声明
- **必须** 在涉及跨进程通信时使用 IPC/SAF 机制

## 上下文工程

SDD 工作流由 `skills/` 下的 skill 体系驱动，统一入口 `using-ohos-sdd`（元路由，按阶段分发）：

| Skill | 用途 |
|-------|------|
| `using-ohos-sdd` | 元路由：识别当前阶段，分发到对应能力 skill |
| `ohos-propose` | Define：proposal.md 需求澄清与基线 |
| `ohos-spec` | Specify：spec.md 特性规格 |
| `ohos-design` | Design：design.md 架构设计 |
| `ohos-plan` | Plan：execution-plan.md + task.md |
| `ohos-review` | GA/GB/GC 阶段审查 |
| `ohos-validate` | A–E 分级校验 |
| `ohos-clarify` | 需求澄清与不涉及项确认 |

四层架构等开发规则见 `rules/`。

## Specs 目录

规格文件存放在 `.codespec/changes/` 目录下。顶层 `.codespec/` 下可放置 `profile.yaml`（子系统 profile 声明）和 `registry.md`（全局索引）。

```
.codespec/changes/issue-<number>-<slug>/
├── proposal.md              # YAML frontmatter 承载 target_release
├── manifest.md
├── lineage.md               # [可选] 新设计/存量设计判断依据
├── design.md
├── spec.md
├── execution-plan.md
├── task/                    # [可选] 独立 task 文件
└── evidence/
    ├── checks/
    └── reviews/
```
