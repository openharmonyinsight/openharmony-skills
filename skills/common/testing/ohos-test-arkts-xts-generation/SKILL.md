---
name: ohos-test-arkts-xts-generation
description: >
  OpenHarmony ArkTS XTS测试用例生成器。解析.d.ts API定义，生成符合Hypium框架的测试用例，支持覆盖率分析、编译验证和Demo+UiTest生成。
  支持ArkTS-Dyn（动态）和ArkTS-Sta（静态）两种语法模式，覆盖12-Phase完整工作流。
  Use when: (1) 用户提到XTS测试、ArkTS测试用例生成、API覆盖率扫描,
  (2) 用户需要为@kit.* SDK生成测试,
  (3) 用户提到APICoverageDetector、未覆盖API、测试补充,
  (4) 用户需要批量生成测试或分批执行,
  (5) 用户需要为UI组件生成Demo+UiTest测试,
  (6) 验证已有测试代码质量或编译测试套,
  (7) 用户要求编译指定的测试套（如"编译xxx"、"build xxx"、"重新编译"）,
  (8) 用户提到编译失败、编译错误、SDK补齐后重新编译。
  Trigger keywords: XTS, ArkTS-Dyn, ArkTS-Sta, test generation, API coverage, APICoverageDetector,
  Hypium, batch generation, .ets files, @tc annotation, test design documents, .d.ts files,
  coverage analysis, UiTest, Demo, 未覆盖API, 编译, build, compile, 重新编译, 编译验证,
  async_build, cleanup_group, build.sh, 测试套编译
metadata:
  author: openharmony
  scope: common
  stage: testing
  domain: arkts
  capability: xts-generation
  version: 0.4.0
  status: draft
  tags:
    - xts
    - arkts
    - test-generation
    - coverage-analysis
  related-skills:
    - name: ohos-test-xts-code-quality
      min_version: "2.0.12"
      required: true
      probes:
        - "{dir}/scripts/main.py --help 2>&1 | grep -q -- '--rules'"
        - "{dir}/scripts/main.py --help 2>&1 | grep -q -- '--sta-mode'"
    - name: ohos-dev-arkts-static-specification-reference
      min_version: "0.1.0"
      required: false
    - name: arkts-skill
      min_version: "1.0.0"
      required: false
      probes:
        - "test -f {dir}/scripts/search_docs.py"
    - name: demo-pipeline
      min_version: "1.0.0"
      required: false
  allowed-tools:
    - Read
    - Write
    - Edit
    - Grep
    - Glob
    - Bash
---

# ohos-test-arkts-xts-generation

> OpenHarmony ArkTS XTS 测试用例生成器

## 配置加载（优先级最高）

**所有相对路径以 `{skill_root}` 为起点**，具体值从 `{skill_root}/.oh-xts-config.json` 的 `skill_root` 字段读取（不存在则从 `.oh-xts-config.example.json` 自动初始化，详见 `prompts/phase-1-config-loading.md` 步骤 0）。

核心字段：`platform`（`wsl`/`windows`/`linux`）、`skill_root`、`OH_ROOT`（源码根目录）、`scan_tool_root`（APICoverageDetector 路径，无效时向用户确认：更新路径 / 提供扫描结果 / 跳过扫描）。

**脚本工具**（`{skill_root}/scripts/`）：

| 脚本 | 用途 | 调用时机 |
|------|------|---------|
| `async_coverage_scan.py` | 异步覆盖率扫描（自动清理旧残留、PID 检查） | Phase 2、10 |
| `extract_uncovered.py` | 提取未覆盖 API（8维度判断、双输出） | Phase 2、3 |
| `compare_uncovered.py` | 覆盖率 before/after 对比 | Phase 10 |
| `manage_scan_env.py` | 扫描环境准备（`setup`/`sync`/`teardown`） | Phase 2、10 |
| `validate_test_context.py` | 生成上下文检查（5/9 项） | Phase 7A |
| `register_test.py` | List.test.ets 注册 | Phase 6 |
| `phase_tracker.py` | Phase 状态追踪 | 每个 Phase |
| `batch_manager.py` | 分批执行管理 | Phase 3-5 |

**必需依赖技能**：

| 依赖技能 | 用途 | 触发时机 |
|---------|------|---------|
| `ohos-test-xts-code-quality` | 代码质量深度扫描（17 条规则：R002-R023 合规 + R201-R205 技术） | Phase 7 步骤 B 必选 |
| `ohos-dev-arkts-static-specification-reference` | ArkTS 静态语法规范校验 | Phase 7 步骤 A，仅静态项目（ArkTS-Sta）时 |
| `arkts-skill` | ArkTS 动态语法/API 按需检索（search_docs.py） | Phase 3 常见模式查表（`arkts_api_pattern_rules.md`），特殊场景 `search_docs.py` 兜底查询；Phase 8 编译错误修复 |
| `demo-pipeline` | Demo 被测应用生成（UI 类测试点） | Phase 5A Step 1，仅存在 UI 类用例时 |

## Initialization

1. 读取 `{skill_root}/.oh-xts-config.json` 获取配置（不存在则自动初始化，见上方配置加载）
2. **会话恢复**：读取 `{skill_root}/.task_summary/` 下最新的 `session_issues_*.md`，向用户汇报上次未解决问题，询问继续还是新任务
3. 判断用户意图：
   - **编译任务**（用户提到"编译"、"build"、"重新编译"、"编译验证"等）→ 直接进入 Phase 8 独立编译模式，跳过 Phase 1-7
   - **测试生成任务**（默认）→ 从 Phase 1 开始完整流程
3. 读取 `{skill_root}/prompts/system.md` 获取系统提示词
4. 所有后续文件引用均使用 `{skill_root}` + 相对路径格式
5. 详细初始化步骤（ETS 版本选择、子系统确定、模块加载、语法类型判断等）→ `prompts/phase-1-config-loading.md`

**模块加载原则**：仅加载当前阶段需要的模块，不要一次性加载所有模块。参考各 Phase prompt 文件开头的指令部分。

**语法类型**：支持 ArkTS-Dyn（动态，默认）和 ArkTS-Sta（静态）。通过目标工程的 `build-profile.json5` 中 `arkTSVersion` 字段判断。两者在 API 可用性、测试目录、编译工具链上有差异，详细处理逻辑见 `prompts/phase-1-config-loading.md` 步骤 9。

## Architecture Overview

```
用户输入 → L1_Analysis（理解API）→ L2_Generation（生成测试）→ L3_Validation（验证+编译）→ 输出
                ↑                          ↑
          references/subsystems/     references/conventions/（框架规范）
```

## Workflow

### 入口判定

| 用户意图 | 入口 Phase | 说明 |
|---------|-----------|------|
| 首次使用 / 配置异常 | **Phase 0** | 加载 `prompts/phase-0-init-config.md`，交互式引导配置 |
| 编译/重新编译测试套 | **Phase 8（独立编译模式）** | 跳过 Phase 1-7，直接加载 `prompts/phase-8-build.md` |
| 生成测试用例（完整流程） | Phase 1 | 从 Phase 1 开始，Phase 0-11 完整 12-Phase 流程 |

**编译模式触发关键词**：编译、build、compile、重新编译、编译验证、编译失败、SDK补齐后重新编译

根据用户是否提供覆盖率报告、以及是否为新增接口，各阶段执行方式有所不同，差异已在各 Phase 文件中说明：

**重要**：所有 Prompt File 路径均使用 `{skill_root}/` 前缀，其中 `skill_root` 从配置文件读取。

**Flow 判定规则**（Phase 1 步骤 0 中检测，优先级从高到低）：

| 优先级 | 条件 | Flow | 说明 |
|--------|------|------|------|
| 1 | 用户明确说明"新增接口"/"新 API"/"new API" | **Flow C** | 新增接口，生成前覆盖率必为 0，跳过 before 扫描 |
| 2 | 用户提供了覆盖率报告（CSV/XLSX/JSON/MD） | **Flow A** | 基于用户报告解析覆盖缺口 |
| 3 | 以上均不满足 | **Flow B** | 标准 APICoverageDetector 扫描 |

| Phase | Name | Prompt File | Flow A | Flow B | Flow C | 并行 |
|-------|------|-------------|--------|--------|--------|------|
| 0 | Init Config | `prompts/phase-0-init-config.md` | 仅首次 | 仅首次 | 仅首次 | — |
| 1 | Task Config & Subsystem | `prompts/phase-1-config-loading.md` | 相同 | 相同 | 相同（额外检测 new_api_mode） | — |
| 2 | Initial Coverage Scan | `prompts/phase-2-coverage.md` | 仅 `extract_uncovered.py` 精准筛选 | APICoverageDetector 精确扫描 + `extract_uncovered.py` 精准筛选 | **跳过**（默认覆盖率为 0） | — |
| 3 | Targeted API Info Parsing | `prompts/phase-3-api-parsing.md` | 仅解析报告中的未覆盖项 | 仅解析 Phase 2 识别的未覆盖项 | 直接解析用户提供的全部新增 API | ✅ 多 d.ts |
| 4 | Generate Test Design | `prompts/phase-4-design.md` | 仅设计报告中的未覆盖项 | 设计全部目标 API 的测试 | 设计全部新增 API 的测试 | ✅ 多 API 组 |
| 5A | Generate Demo (UI类用例) | `prompts/phase-5-demo-generation.md` | 用例分类 + Demo 生成（仅UI类用例） | 用例分类 + Demo 生成（仅UI类用例） | 相同 | ✅ 多页面 |
| 5 | Generate Test Cases (非UI类) | `prompts/phase-5-generation.md` | 依据设计文档生成非UI类用例 | 依据设计文档生成非UI类用例 | 相同 | ✅ 多文件 |
| 5B | Generate UiTest (UI类用例) | `prompts/phase-5-uitest-generation.md` | 依据设计文档生成UiTest代码（仅UI类用例） | 依据设计文档生成UiTest代码（仅UI类用例） | 相同 | ✅ 与 5A/5 并行 |
| 6 | Register Test Suites | `prompts/phase-6-registration.md` | 相同 | 相同 | 相同 | — |
| 7 | Format & Validate | `prompts/phase-7-validation.md` | 步骤A + 步骤B | 步骤A + 步骤B | 步骤A + 步骤B | — |
| 8 | Build Verification | `prompts/phase-8-build.md` | 推荐 | 推荐 | 推荐 | — |
| 9 | Device Test Execution | `prompts/phase-9-test-execution.md` | 可选 | 可选 | 可选 | ✅ 与 10 并行 |
| 10 | Coverage Verification | `prompts/phase-10-coverage.md` | 可选 | 必须（before/after 对比） | 必须（**仅 after 扫描**，无 before baseline） | ✅ 与 9 并行 |
| 11 | Output Results | `prompts/phase-11-output.md` | 相同 | 相同 | 覆盖率表标注"生成前: 0（新增接口）" | — |

**Phase 5 执行顺序**：
1. Phase 5A（Step 0 用例分类 + Step 1 Demo 生成）— 仅存在 UI 类用例时执行
2. Phase 5（非 UI 类测试代码）和 Phase 5B（UiTest 测试代码）和 Phase 5A Step 1（Demo 代码生成）— **代码生成阶段可并行**，均从 Phase 4 设计文档的控件 ID 清单读取
3. 编译阶段：Demo 和 UiTest 测试代码一起进入编译——同 HAP 作为同一编译单元；辅助包通过编译 group 整体编译

### Phase Tracker

使用 `scripts/phase_tracker.py` 追踪每个 Phase 的执行状态，确保按序执行、关键 Phase 不可跳过。

**强制 Phase**：Phase 4（测试设计文档）和 Phase 7（格式验证）**不可跳过**。

```bash
# 每个 Phase 开始前必须执行 check（确认前置 Phase 已完成）
python {skill_root}/scripts/phase_tracker.py check 5 --output .coverage_data

# Phase 完成后标记（可附加输出文件路径）
python {skill_root}/scripts/phase_tracker.py complete 4 --output-file path/to/design.md --output .coverage_data
```

其他子命令：`init`（初始化）、`start`（标记开始）、`skip`（跳过非强制 Phase，需 `--reason`）、`status`（查看状态）、`report`（生成检查清单）。详细用法见 `scripts/phase_tracker.py --help`。

**每个 Phase 开始前必须执行 `check` 命令**，确认前置 Phase 已完成。若前置 Phase 为 pending 或 in_progress，则阻止当前 Phase 开始。

### Phase 内联指导

> 每个Phase仅列核心目标，详细步骤见对应 `prompts/phase-N-xxx.md`。

| Phase | 核心目标 | 关键约束/输出 |
|-------|---------|-------------|
| 2 | 识别未覆盖 API | Flow A: `extract_uncovered.py`；Flow B: APICoverageDetector 扫描；Flow C: 跳过。输出: `uncovered_apis.json`。APICoverageDetector 支持 Windows/WSL，Linux 需用户提供扫描结果或跳过。详细用法见 `docs/ASYNC_COVERAGE_SCAN.md` |
| 3 | 从 .d.ts 提取 API 完整签名 | 信息源优先级: .d.ts > 子系统配置 > 参考示例。支持多文件并行 |
| 4 | 生成 `.design.md` 测试设计文档 | **不可跳过**。定义用例列表、控件 ID（UI 类）。UI 类判定: 组件创建/属性/事件/动效 → Phase 5A/5B |
| 5 | 生成非 UI 类 .test.ets | 仅用 .d.ts 声明接口；必须 @tc 注解；cleanup 必须处理异常；遵循 P0/P1/P2 测试价值分级和停止扩展信号 |
| 5A | 生成 Demo 应用（UI 类） | 触发: Phase 4 存在 UI 类用例。三方控件 ID 契约必须一致。依赖 `demo-pipeline` |
| 5B | 生成 UiTest（UI 类） | 与 5A 可并行；Demo + UiTest 同 HAP 编译 |
| 7 | 格式验证 | **不可跳过**。A: `validate_test_context.py`；B: `ohos-test-xts-code-quality`；Sta: `ohos-dev-arkts-static-specification-reference` |
| 8 | 编译验证 | 支持独立模式；`async_build.sh` 异步编译；失败自动修复（≤3次） |
| 10 | 覆盖率对比 | Flow A/B: before→after 对比；Flow C: 仅 after 扫描 |

## Module Loading

> **重要提示**：详细的加载规则已嵌入到每个 Phase 的描述文件中。
> 
> SKILL.md 仅提供概念性说明：
> - MANDATORY：必须完整阅读的文件（前置加载）
> - 按需加载：根据任务条件加载
> - Do NOT Load：禁止加载的模块

每个 Phase 的具体加载规则请参考对应 prompt 文件开头的指令部分。

## Configuration Architecture

```
Priority: User Custom > Module Config > Subsystem Config > Core Config

Core:      references/subsystems/_common.md          (shared mandatory + default rules)
Subsystem: references/subsystems/{Subsystem}/_common.md  (differential rules)
Module:    references/subsystems/{Subsystem}/{Module}.md  (module-specific rules)

Note: 覆盖率扫描环境通过文件复制方式自动准备
```

## 执行原则

1. 每个 Phase 开始前，读取对应的 prompt 文件获取详细指令
2. 严格按 Phase 顺序执行；强制 Phase（4、7）不可跳过
3. 每个 Phase 完成后，更新 `phase_tracker` 状态
4. 懒加载模块：仅读取当前 Phase 所需的参考文档和按需模块
5. 遇到错误时，读取错误处理指南进行恢复（`references/error_handling.md` 或 `{knowledge_root}/common/xts_experience/03_standards/02_error_handling_guide.md`）
6. 每完成 2-3 个 Phase，向用户简要汇报进度
7. **编译模式判定**：Phase 8 编译前，检查 `Test.json` 的 `test-file-name`；包含多个 HAP 时使用 group 编译；同批次多个测试套也使用 group 编译
8. **hdc 环境**：Phase 9 开始前，自动检测 hdc 可用性；不在 PATH 时从 prebuilts 添加
9. **必读标记**：当 Phase prompt 中标注 `[必读]` 条件满足时，**必须先读取知识库文档再执行任何修复/操作**；禁止跳过文档进行试错
10. **Issue 日志**：遇到问题时立即追加记录到 `session_issues_{日期}.md`（见「会话连续性」章节），禁止延迟到任务结束时才记录

## Anti-Patterns

### NEVER 使用未在.d.ts中声明的接口
- **原因**：编译环境中不存在该接口，代码无法编译
- **正确做法**：仅使用.d.ts中明确声明的接口和参数

### NEVER 修改BUILD.gn、build-profile.json5等项目配置文件
- **原因**：会影响其他开发者的编译环境
- **正确做法**：仅在指定目录创建测试文件

### NEVER 跳过Phase 7验证
- **原因**：未验证的测试可能包含资源泄漏、无效断言、格式错误
- **后果**：这些问题流入下游，修复成本指数级增长

### NEVER 在测试用例中省略@tc注解
- **原因**：测试报告系统无法识别没有@tc的用例元数据
- **正确做法**：每个测试用例必须有标准@tc块

### NEVER 硬编码系统路径或设备信息
- **原因**：不同设备/环境下路径不同，硬编码导致测试不可移植
- **正确做法**：使用框架提供的接口获取路径和设备信息

### NEVER 在cleanup步骤中忽略异常
- **原因**：资源未释放会影响后续测试执行
- **正确做法**：cleanup中的异常必须捕获并记录，不能静默忽略

### NEVER 为@throws声明以外的错误码构造测试
- **原因**：401 是 SDK 公共错误码（不在 @throws 中声明），动态模式下入参类型错误、入参个数异常时自动抛出；17xxxxxx 等业务错误码在 @throws 中声明。两者来源不同，不可混淆
- **正确做法**：ArkTS-Dyn 模式下，401 测试（传 null/错误类型/参数缺失）和 @throws 声明的业务错误码测试**都应生成**；ArkTS-Sta 模式下，401 不应测试（编译时已拦截类型错误，401 不会到达运行时）。禁止凭空编造 @throws 中未声明的业务错误码

### NEVER 跳过 Phase 4 测试设计文档
- **原因**：没有设计文档，Demo/UiTest/测试代码之间的控件 ID 契约无法保证，用例缺乏可追溯性
- **正确做法**：Phase 4 在所有模式下（Flow A/B/C、ArkTS-Sta）都必须生成设计文档（`.design.md`），Phase 5 基于设计文档生成代码
- **后果**：跳过会导致控件 ID 不一致、测试意图无法追溯。且无法通过 Phase 7 的 A.10/A.11 检查项

### NEVER 跳过 Phase 2 before/after 覆盖率对比
- **原因**：没有 before baseline 无法量化测试用例的覆盖率贡献
- **正确做法**：Phase 2 执行 `extract_uncovered.py` 生成 before baseline，Phase 10 执行 `compare_uncovered.py` 对比

### NEVER 不经备份直接修改 prebuilts 文件
- **原因**：prebuilts 中的 SDK 和编译工具版本是编译环境的核心依赖，误删或覆盖将导致编译环境不可用
- **正确做法**：先备份 `cp -r {目标路径} {目标路径}.bak.$(date +%Y%m%d_%H%M%S)`，再修改
- **后果**：环境损坏后恢复耗时长，影响其他开发者

### NEVER 为已废弃接口生成测试用例
- **原因**：标记 @deprecated 的接口已被弃用，测试价值低且维护成本高
- **正确做法**：跳过 @deprecated 接口（除非用户明确要求），依据 .d.ts 中的 @useinstead 使用新接口替代
- **后果**：生成废弃接口测试浪费资源，且废弃接口可能在后续版本被移除

### NEVER 在新生成的代码中调用已废弃接口
- **原因**：废弃接口在后续版本可能被移除，生成的测试将无法维护
- **正确做法**：参考历史代码时若发现 @deprecated 接口，在新生成的代码中使用已知的新接口替代（不修改历史代码）
- **后果**：依赖废弃接口的测试用例在 SDK 升级后编译失败

### NEVER 在ArkTS-Sta项目中使用 as any 类型断言
- **原因**：`as any` 是动态语法特性，ArkTS-Sta 静态编译模式下不通过
- **正确做法**：使用具体的类型声明或类型守卫（type guard）。参考 `ohos-dev-arkts-static-specification-reference` 技能转换语法
- **后果**：静态编译失败，错误码 `ESE0143` 或 `ESE0046`

### NEVER 直接调用APICoverageDetector可执行文件
- **原因**：直接调用跳过了环境准备（文件复制、arkts_config.json 配置）和残留文件清理
- **正确做法**：使用 `scripts/async_coverage_scan.py` 或 `scripts/manage_scan_env.py` 封装脚本
- **后果**：扫描结果不准确或扫描失败

### NEVER 在多版本模式下并行编译动态和静态测试套
- **原因**：ets1.1 和 ets1.2 的 hvigor 版本不兼容，并行编译会导致编译失败
- **正确做法**：串行编译 — 先完成 ets1.1 全流程（生成→注册→验证→编译通过），再切换 prebuilts 环境编译 ets1.2
- **后果**：编译环境冲突，两个版本都无法通过

### NEVER 跳过 prebuilts 环境切换直接编译静态版本
- **原因**：未切换 prebuilts 时使用的是动态 SDK 的 hvigor（5.x），无法编译静态语法（ets1.2）
- **正确做法**：按「多版本串行生成模式」的 prebuilts 切换流程操作，编译前验证 hvigor 版本
- **后果**：编译失败，错误信息指向类型不兼容

### NEVER 在静态版本测试中设计传 null/undefined 触发 401 的用例
- **原因**：ArkTS-Sta（ets1.2）在编译时已检查参数类型，null/undefined 不会到达运行时的 401 错误码
- **正确做法**：静态版本跳过 ERROR_401 类型测试，仅保留参数功能测试
- **后果**：测试用例编译失败

### NEVER 延迟创建 session_issues 日志
- **原因**：延迟记录会导致 issue 上下文丢失（错误信息、Phase 状态、当时的环境），无法追溯
- **正确做法**：Phase 1 步骤 0 立即创建 `session_issues_{日期}.md`，遇到问题时立即追加记录
- **后果**：任务结束时无法准确复盘问题和优化

## Quick Reference

| Subsystem | Kit | Test Path | Config Path |
|-----------|-----|-----------|-------------|
| testfwk | @kit.TestKit | test/xts/acts/testfwk/ | references/subsystems/testfwk/ |
| ArkUI | @kit.ArkUI | test/xts/acts/arkui/ | references/subsystems/ArkUI/ |
| ArkWeb | @kit.ArkWeb | test/xts/acts/arkweb/ | references/subsystems/ArkWeb/ |
| multimedia | @kit.MediaKit | test/xts/acts/multimedia/ | references/subsystems/multimedia/ |
| ability | @kit.AbilityKit | test/xts/acts/ability/ | references/subsystems/ability/ |

## 分批执行模式（Batch Mode）

当未覆盖 API 数量较多时，支持分批生成测试用例。分批决策依据（API数量>20、复杂度高、跨模块、Context紧张→倾向分批）和分批经验（同模块同批、UI/非UI分开）详见 `prompts/batch-mode.md`。

**覆盖率结果标签**（Phase 11 输出必须标注）：

| 标签 | 含义 | 触发条件 |
|------|------|---------|
| `coverage verified` | before/after 对比完成，覆盖率提升已量化 | Flow A/B Phase 10 正常完成 |
| `coverage report provided` | 用户提供了覆盖率报告 | Flow A 用户提供报告 |
| `coverage scan skipped` | 扫描不可用，用户确认跳过 | Phase 2 用户选择跳过 |
| `coverage: new API (baseline=0)` | 新增接口，生成前覆盖率为 0 | Flow C |

**NEVER 将 `coverage scan skipped` 标注为 `coverage verified`**。

> **会话连续性**：Issue 日志初始化和会话恢复已内嵌于 `prompts/phase-1-config-loading.md`（步骤 0）和 `prompts/phase-11-output.md`（会话收尾）。

## Documentation

> **注意**：`{skill_root}/docs/` 下的文件供**人类用户参考**，Agent 在执行期间**不加载**这些文件。如需特定知识（如异步扫描流程），请加载对应的 prompt 文件（如 `prompts/phase-2-coverage.md`）。
