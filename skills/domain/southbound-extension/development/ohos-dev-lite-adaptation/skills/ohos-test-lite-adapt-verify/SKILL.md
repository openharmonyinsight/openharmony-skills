---
name: ohos-test-lite-adapt-verify
description: >
  OH Lite 芯片适配验证工作流（通用版）。6 阶段编排：环境初始化 → 基线量测 → 分析提案 → 实现改动 →
  编译烧录跑测试验证 → 归档总结。不绑定特定芯片，连接方式可插拔（SSH/Local/Custom），测试策略由用户决定
  （XTS / unit test / manual / custom）。Use when an OpenHarmony Lite adaptation needs runtime verification,
  firmware size baseline/optimization, or a test-run pipeline; triggers include xts验证, 芯片验证, 适配验证,
  固件测试, 跑测试, 验证优化, miniaturization, 量基线, 分析大小, 减体积, 烧录测试, map对比, 提交归档。
metadata:
  author: openharmony
  scope: domain
  stage: testing
  domain: lite
  capability: adapt-verify
  version: 0.1.0
  status: trial
---

# ohos-test-lite-adapt-verify — OH Lite 芯片适配验证工作流

本技能是 **6 个阶段文件的统一编排层**（阶段细节在 `references/phases/` 下按需读取），不重复阶段逻辑，仅负责流程调度和路由。

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 完整验证流程 | "用 ohos-test-lite-adapt-verify 跑一遍 Hi3861 的适配验证"、"从头到尾验证一遍" |
| 单阶段/快捷入口 | "量个基线" / "看看现在多大"、"分析一下 XX 模块"、"帮我改这些"、"跑一下验证" / "烧录测试"、"提交归档"、"重新初始化环境" |
| 测试验证意图 | "xts验证"、"跑测试"、"固件测试"、"验证适配"（阶段4 为主，阶段1-3 可跳过或轻量） |
| 优化意图 | "验证优化"、"miniaturization"、"量基线"、"分析大小"、"减体积"（完整 6 阶段，阶段1-3 是核心） |
| 上游链式调用 | 芯片适配主工作流 P4 编译通过后进入运行时验证；verifying-workflow 用户选择 XTS/编译+烧录+串口类测试策略时 |

**不触发**（明确排除）：只要编译/烧录/串口能力本身（直接用 ohos-ci-lite-deploy-burn，本 skill 是其上的验证编排层）；测试用例代码生成（ohos-test-lite-ut-gen）。

## Scope

```
verifying-workflow (通用验证框架)
  ├── 代码相似度对比
  ├── 编译产物检查
  ├── MAP 分析
  └── [可插拔测试策略] ←── ohos-test-lite-adapt-verify 在这里
        ├── XTS 测试套件（默认）
        ├── 单元测试
        ├── 手动测试
        └── 自定义测试方案
```

**核心原则：用户决定跑什么测试、怎么跑。** 本 skill 不替代 verifying-workflow，
而是在用户选择 XTS（或其他基于编译+烧录+串口捕获的测试方案）时提供完整流水线。

**输入**：目标代码仓（经 ohos-ci-lite-deploy-burn config.json 配置的连接方式）、设备 profile、用户选定的测试策略、（优化路径）模块范围。
**输出**：`xts_test/` 产物目录——基线 MAP 报告、架构图、提案（proposal/design/specs/tasks）、实现报告、verify_result.md（测试统计 + MAP 对比 delta：optimization 必含，test-only 有基线记参考/无基线标 N/A）、lessons.md、代码仓 commit。
**不适用**：非 OpenHarmony Lite 目标的测试；纯编译部署不涉验证（ohos-ci-lite-deploy-burn 直接跑）；测试用例编写（ohos-test-lite-ut-gen）。

### 职责边界（XTS 测试验证 vs 固件体积优化）

本 skill 的 6 阶段流水线同时承载两类不同诉求，执行前先判明用户意图，避免混淆：

| 维度 | XTS 测试验证 | 固件体积优化（miniaturization） |
|------|-------------|------------------------------|
| **目标** | 产出通过/失败报告，确认适配功能正确 | 降低 RAM/ROM 占用，产出优化前后对比 |
| **阶段侧重** | 阶段4 verify（编译→烧录→跑测试→出报告） | 阶段1 explore（量基线）→ 阶段2 analyze（找优化点）→ 阶段3 implement（改代码）→ 阶段4 verify（MAP 对比） |
| **产物** | 测试报告（通过率/失败用例清单） | 优化报告（优化前后大小对比 + MAP 分析 + 改动清单） |
| **是否改代码** | 否（只跑测试验证） | 是（实施优化改动） |
| **触发词** | xts验证、跑测试、固件测试、验证适配 | 验证优化、miniaturization、量基线、分析大小、减体积 |

**判别规则**：
- 用户说"跑 XTS / 验证 / 测试" → 走 XTS 测试验证路径（阶段4 为主，阶段1-3 可跳过或轻量执行）
- 用户说"优化 / 减体积 / miniaturization / 量基线 / 分析大小" → 走固件体积优化路径（完整 6 阶段，阶段1-3 是核心）
- 用户同时要测试 + 优化 → 先优化（阶段1-3-4 改+验体积）→ 再测试（阶段4 跑 XTS），两类产物分别出报告

> 两者共享 ohos-ci-lite-deploy-burn 的编译/烧录/串口能力，但目标产物不同。不准把"体积没变"当"测试通过"，也不准把"测试通过"当"优化完成"。

## Initial Checks（路由前状态检测）

> **入口模式判定**：进入本 skill 先判断是 test-only（仅跑测试，MAP 仅参考）还是 optimization（体积优化闭环，MAP 需改善）。
> 模式由**用户是否要求优化**决定，不由代码是否变动决定：用户要求跑测试/验证——包括"功能我自己改完了，帮我烧板跑 XTS 确认"这类代码有变动但只求验证的场景 → test-only。
> 用户明确要求优化/减体积/对比优化前后收益 → optimization（本工作流阶段 1-3 量基线/提案/实施跑完后的验证闭环）。"改了代码"本身不构成 optimization。


当用户调用本技能时，先检测项目状态，路由到对应阶段（各阶段详情按读取条件进 `references/phases/`）：

**test-only 模式**：完成环境检查（下方第 1 条）后**直接进入 verify**（第 5 条）——基线/提案/tasks 是 optimization 模式的前置，纯测试路径不要求、不补建。

**optimization 模式 / 模式未定**：按依赖逐级路由——

1. **环境未就绪**（无有效连接配置、无设备选择、或 config 未校准）→ **init**
2. **无基线**（`xts_test/reports/baseline_map.md` 不存在）或 **无架构图/优化初稿** → **explore**
3. **无已批准的提案**（`xts_test/proposals/*/tasks` 不存在或用户未确认）→ **analyze**
4. **提案已批准，tasks 未全部完成** → **implement**
5. **tasks 已完成，未验证**（`xts_test/reports/verify_result.md` 不存在或非最新）→ **verify**
6. **已验证通过** → **summary**

同时检查前置依赖：

| 依赖 | 用途 | 必须 |
|------|------|:----:|
| `ohos-ci-lite-deploy-burn` | 编译 / 下载 / 烧录 / 串口捕获 | ✅ |
| `references/devices/<chip>.json`（ohos-ci-lite-deploy-burn 下） | 设备配置（硬件上限、烧录参数等） | ✅ |
| Python ≥ 3.7 | map_analyzer.py 等工具 | ✅ |
| pyserial | 串口通信（本地烧录模式） | 本地模式必须 |

可选工具（有则增强能力，无也不阻塞）：

| 可选工具 | 用途 |
|---------|------|
| openspec (@fission-ai/openspec) | 结构化需求分析、变更管理 |
| node.js | openspec 运行时 |

## Prohibited Practices（禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| **替用户决定测试策略** | init 阶段必须问用户（XTS / Unit / Integration / Manual / Custom），写入 config；verify 按该选择分流，不硬编码测试套件 |
| **覆盖黄金基线** | `xts_test/reports/baseline_map.md` 是 MAP 对比的黄金基线，不可覆盖（除非用户明确要求重新量测） |
| **用户批准提案前就改代码** | analyze 阶段与用户迭代到明确批准（"通过"/"批准"/"可以开始改了"）才进 implement |
| **把"体积没变"当"测试通过"**（或反之） | 测试验证与体积优化两类产物分开出报告，验收标准各按各的 |
| **verify 不通过就带病往下走** | 测试 Fail（optimization）→ 先分类按类别路由：实现缺陷回溯 implement（按已批准 tasks）修正后重跑；环境问题修环境/配置后重跑；用例缺陷修测试方案或报告（需授权）。test-only → 记录失败并报告，不自动进 implement、不改用户代码，需修源码先征用户授权。MAP 无改善（仅 optimization 模式）→ 同样先归因回溯（评估有误→implement；改动未生效/链接配置→修构建环节）。不准跳过进 summary |
| **验证终点停在中间态** | 终点 = 可烧录件烧进板子 + 板上 test 执行 PASS（编译过 / raw 件有符号 / 能烧进去都不是终点） |
| **implement 阶段随手 commit** | 保持 git 工作区可追溯，提交留给 summary 阶段（commit message 按 constraints 格式 + 用户确认） |
| **MAP 改善没对比基线就宣称达标** | optimization 模式 verify 必须跑 map_analyzer compare 基线 vs 新 map，delta 写入 verify_result.md；test-only 有基线记参考值、无基线跳过 |

## ① 文件路由表（阶段渐进披露）

每个阶段的具体执行细节在 `references/phases/` 下，**进入该阶段时才读对应文件，一次只读当前阶段的**：

| 读取条件 | Agent 读取 |
|---------|-----------|
| 路由判定进入阶段 0（环境未就绪 / "重新初始化环境"） | `references/phases/init.md` |
| 进入阶段 1（无基线 / "量个基线" / "看看现在多大"） | `references/phases/explore.md` |
| 进入阶段 2（有初稿无已批准提案 / "分析一下 XX 模块"） | `references/phases/analyze.md` |
| 进入阶段 3（提案已批准 tasks 未完成 / "帮我改这些"） | `references/phases/implement.md` |
| 进入阶段 4（tasks 完成未验证 / "跑一下验证" / "烧录测试"） | `references/phases/verify.md` |
| 进入阶段 5（已验证通过 / "提交归档"） | `references/phases/summary.md` |
| verify 阶段用户策略 = XTS | `references/test-strategies/xts.md` |
| 需要 MAP 分析/对比工具用法 | `ohos-ci-lite-deploy-burn/tools/map_analyzer.py`（analyze / compare） |
| 需要设备配置 / 烧录 / 串口能力 | `ohos-ci-lite-deploy-burn` skill（config.json + references/devices/ + tools/） |

## ② 工作流（6 阶段编排）

```
阶段0  init       环境初始化（工具链、连接方式、设备配置校准）
   │
   ▼
阶段1  explore    量基线 RAM/ROM（全量编译 + map_analyzer）→ 架构图 → 优化初稿
   │   （调用 ohos-ci-lite-deploy-burn 编译 + MAP 分析）
   ▼
阶段2  analyze    深入分析优化点 → 生成提案(design+specs+tasks)，迭代到用户批准
   │
   ▼
┌──────────────────────────────────────────────────┐
│  按 tasks 循环，直到所有 task 验证通过：            │
│                                                  │
│  阶段3  implement  改代码 + 代码规范 checklist     │
│           │                                      │
│           ▼                                      │
│  阶段4  verify     编译→下载→烧录→[用户选择的测试]   │
│    + map_analyzer compare 对比基线（仅 optimization）│
│           │                                      │
│           └ 失败 → 先分类路由 ※                      │
│                ├ 实现缺陷/评估有误 → 回阶段3         │
│                ├ 环境/构建/工具链 → 修环境重跑       │
│                └ 用例缺陷 → 修测试方案/报告          │
└──────────────────────────────────────────────────┘

> ※ 注：MAP 对比与图中「失败 → 先分类路由」回炉**仅适用于 optimization 模式**——实现缺陷回阶段3；环境问题修环境/配置后重跑；用例缺陷修测试方案或报告（编译失败同理：源码缺陷才回阶段3，工具链/构建配置问题修环境重跑）。test-only 模式 MAP 仅参考/跳过，测试不过即记录失败并报告（不回 implement），详见 Initial Checks 入口模式判定。
   │
   ▼
阶段5  summary    归档 + commit + 经验沉淀
```

### 阶段文件清单

| 阶段 | 文件 | 职责 |
|------|------|------|
| 0 | `references/phases/init.md` | 工具链检查、连接配置、设备选择、测试策略选择、config 校准 |
| 1 | `references/phases/explore.md` | 全量编译量基线、MAP 分析、架构图、优化初稿 |
| 2 | `references/phases/analyze.md` | 深入分析、量化、出提案，与用户迭代到批准 |
| 3 | `references/phases/implement.md` | 在目标环境改代码、规范检查、对照文档确认 |
| 4 | `references/phases/verify.md` | 调 ohos-ci-lite-deploy-burn 编译→烧录→**跑测试**→MAP 对比（按入口模式：optimization 必做，test-only 参考/跳过） |
| 5 | `references/phases/summary.md` | 归档、commit（信息约束）、沉淀 lessons |

### 快捷入口

| 用户意图 | 直接跳转到 |
|---------|-----------|
| "重新初始化环境" | 阶段0 init（忽略已有状态），读 `references/phases/init.md` |
| "量个基线" / "看看现在多大" | 阶段1 explore（覆盖旧基线），读 `references/phases/explore.md` |
| "分析一下 XX 模块" | 阶段2 analyze（从探索开始或接续现有初稿），读 `references/phases/analyze.md` |
| "帮我改这些" | 阶段3 implement（需已有 approved proposal），读 `references/phases/implement.md` |
| "跑一下验证" / "烧录测试" | 阶段4 verify（需已有实现），读 `references/phases/verify.md` |
| "提交归档" | 阶段5 summary（需已验证通过），读 `references/phases/summary.md` |

### 约定路径

- **项目根**：agent 当前工作目录（`cwd`），记作 `<PROJECT_ROOT>`。
- **本 skill 产物目录**：`<PROJECT_ROOT>/xts_test/`（默认，init 阶段可由用户改为外部路径）。
- **ohos-ci-lite-deploy-burn**：`skills/ohos-ci-lite-deploy-burn/`
- **设备配置**：`skills/ohos-ci-lite-deploy-burn/references/devices/<chip>.json`

### 使用示例

```bash
# 完整流程（首次）
"用 ohos-test-lite-adapt-verify 跑一遍 Hi3861 的适配验证"
→ 自动路由到 init → explore → analyze → implement → verify → summary

# 从中间阶段进入
"基线已经量过了，直接分析 WiFi 模块"
→ 检测到 baseline 存在 → 路由到 analyze

# 只跑验证（不改代码）
"代码已经改好了，帮我烧录跑 XTS 看看结果"
→ 检测到 tasks 完成 → 路由到 verify

# 换芯片
"换 STM32F407 跑一遍"
→ init 阶段重新选择设备 profile → 后续流程自动使用新配置
```

## 与其他 Skill 的关系

```
designing-workflow (芯片适配主工作流)
  ├── P1~P3: 需求收集 → 代码生成 → 配置生成
  ├── P4: build-verify (编译验证)
  │     └── 编译通过? → 进入 ohos-test-lite-adapt-verify (可选)
  │           └── 用户决定: 是否需要运行时验证?
  └── verifying-workflow (通用验证框架)
        ├── 代码相似度对比
        ├── 编译产物结构检查
        └── [用户选择的验证策略]
              ├── ohos-test-lite-adapt-verify ← 本 skill
              ├── 手动验证
              └── 其他自定义方案

ohos-ci-lite-deploy-burn (编译烧录部署工具)
  └── 被 ohos-test-lite-adapt-verify 的 init/explore/verify 阶段调用
      (作为底层工具，不包含验证逻辑本身)
```

## Exceptions and Fallbacks（异常与兜底）

| 场景 | 处理 |
|------|------|
| **verify 测试有 Fail** | 分析失败原因分类（实现缺陷 / 环境问题 / 用例缺陷）并**按类别路由**。optimization：实现缺陷 → 回 implement（按已批准 tasks）修正后重跑；环境问题 → 修环境/配置（必要时回 init 校准）后重跑，不改产品代码；用例缺陷 → 修测试方案或报告用户（改动需授权），不进 implement。test-only → 记录失败与证据并报告，不自动进 implement，需修源码先征用户授权。不准带 Fail 进 summary |
| **verify MAP 无改善 / 恶化（仅 optimization 模式）** | 先归因再路由：优化点评估有误/实现问题 → 回 implement 排查修正；改动未生效（烧错 bin/构建缓存）→ 修构建或烧录环节重跑；gc-sections 丢段/链接配置 → 修构建配置（build-config），不改产品代码；重跑 verify |
| **同一问题回炉超 3 次** | 咨询 Oracle 或请求用户介入决策，不无限循环 |
| **编译失败（verify 阶段）** | 先分类原因：源码缺陷（optimization → 回 implement 按已批准 tasks 修正）；环境/构建配置/工具链问题 → 修环境或配置（必要时调 cross-toolchain / build-config skill）后重跑，不改产品代码；test-only → 报错并报告用户（含原因分类），不代改用户代码 |
| **openspec / 可选工具不可用** | 手动分析同样有效（提案文档结构手动维护），不阻塞流程 |
| **SSH/连接失败** | 回 init 阶段重配连接（连通性验证是 init 收尾必过项），不带病执行后续阶段 |
| **用户中途要求换测试策略** | 允许——verify 阶段可重新调整 test.strategy，不影响已完成的 init/explore/analyze/implement 工作 |
| **硬件操作需用户在场**（按 RST / 选烧录模式） | 烧录/测试涉及硬件交互时等用户配合，不代替用户按板；串口监听已在抓的不遗漏 |
| **XTS 环境配置未确认**（acts 未解压 / HiBurn 未就位） | init Step 4.5 完成且用户确认前不进 verify |
| **发现本 skill 可改进之处** | 记入 `xts_test/lessons.md` 改进建议（下次迭代落实） |
