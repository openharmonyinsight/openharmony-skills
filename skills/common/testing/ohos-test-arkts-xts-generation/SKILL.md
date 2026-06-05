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
    - ohos-test-capi-xts-generation
    - check-test-code-quality
    - arkts-static-spec
    - demo-pipeline
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

## 路径说明

**本文档中所有相对路径均以本技能的根目录（skill-root）为起点。**

具体路径以 `{skill_root}/.oh-xts-config.json` 中 `skill_root` 字段的值为准。

## 配置加载（优先级最高）

**必须首先读取配置文件**：`{skill_root}/.oh-xts-config.json`

配置文件核心字段：`platform`（运行环境：`wsl`/`windows`/`linux`）、`skill_root`（所有相对路径的基准）、`OH_ROOT`（OpenHarmony 源码根目录，自动推导其他路径）、`scan_tool_root`（APICoverageDetector 路径）。

首次使用时自动初始化：将 `.oh-xts-config.example.json` 复制为 `.oh-xts-config.json`，从用户消息提取路径或交互式询问。详见 `prompts/phase-1-config-loading.md` 步骤 0。

**工具路径**（基于配置文件和 skill_root）：
- 覆盖率工具: `{scan_tool_root}/`（路径无效时向用户确认：更新路径 / 提供扫描结果 / 跳过扫描）
- 脚本工具: `{skill_root}/scripts/`
- 提示词: `{skill_root}/prompts/`
- 参考配置: `{skill_root}/references/subsystems/`
- 组件映射: `{skill_root}/references/component_subsystem_mapping.json`（Phase 1 加载，360+ 组件 → 56 子系统映射）
- 工具模板: `{skill_root}/references/templates/`（Utils_dyn.ets / Utils_sta.ets）

**脚本工具速查**：

| 脚本 | 用途 | 调用时机 |
|------|------|---------|
| `manage_scan_env.py` | 文件复制到扫描目录 + arkts_config.json 配置（支持 `setup`/`sync`/`teardown`/`status`） | Phase 2 步骤 1、Phase 10 增量同步 |
| `validate_test_context.py` | 测试文件生成上下文检查（5/9 项） | Phase 7 步骤 A |
| `register_test.py` | List.test.ets 注册新测试文件 | Phase 6 |
| `extract_uncovered.py` | 提取未覆盖 API 列表（直接读 Excel、8维度判断、双输出文件） | Phase 2 步骤 3、Phase 3 |
| `compare_uncovered.py` | 覆盖率 before/after 对比（对比两次 extract_uncovered 结果） | Phase 10 |
| `sync_ets_version.py` | 同步 ets_version 到 arkts_config.json | Phase 1 |
| `async_coverage_scan.py` | 异步覆盖率扫描（启动前自动清理旧残留文件、统一 PID 检查） | Phase 2、Phase 10 |
| `batch_manager.py` | 分批执行管理器（计划/执行/续传） | Phase 3-5 批量模式 |
| `batch_lock.py` | 文件锁（多 subagent 并发写入保护） | batch_manager.py 内部依赖 |
| `phase_tracker.py` | Phase 执行状态追踪（init/start/complete/skip/check/status/report） | 每个 Phase 开始前检查、Phase 10 输出报告 |

**必需依赖技能**：

| 依赖技能 | 用途 | 触发时机 |
|---------|------|---------|
| `check-test-code-quality` | 代码质量深度扫描（11 条规则） | Phase 7 步骤 B 必选 |
| `arkts-static-spec` | ArkTS 静态语法规范校验 | Phase 7 步骤 A，仅静态项目（ArkTS-Sta）时 |
| `demo-pipeline` | Demo 被测应用生成（UI 类测试点） | Phase 5A Step 1，仅存在 UI 类用例时 |

## Initialization

1. 读取 `{skill_root}/.oh-xts-config.json` 获取配置（不存在则自动初始化，见上方配置加载）
2. 判断用户意图：
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

| Phase | Name | Prompt File | Flow A（有覆盖率报告） | Flow B（无覆盖率报告） | Flow C（新增接口） | 并行 |
|-------|------|-------------|----------------------|----------------------|-------------------|------|
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

### Phase 执行状态追踪

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

> 以下为关键 Phase 的简短指导，帮助在不加载完整 prompt 文件的情况下做出初步决策。详细步骤仍需加载对应 prompt 文件。

#### Phase 2: Initial Coverage Scan
- **核心目标**：识别哪些 API 未被现有测试覆盖
- **Flow A**：直接运行 `extract_uncovered.py` 从覆盖率报告精准筛选未覆盖项
- **Flow B**：运行 APICoverageDetector 全量扫描，再用 `extract_uncovered.py` 8维度判断筛选
- **Flow C**：跳过（新增接口覆盖率为 0）
- **关键输出**：`.coverage_data/uncovered_apis.json` — 未覆盖 API 列表

#### Phase 3: Targeted API Info Parsing
- **核心目标**：从 .d.ts 文件中提取目标 API 的完整签名（参数、返回值、@since、@throws、@deprecated）
- **信息源优先级**：`.d.ts` 声明（最高）→ 子系统配置 → 参考示例 → API 文档
- **支持并行**：多个 .d.ts 文件可并行解析
- **关键输出**：每个 API 的结构化信息（参数类型、可选/必选、错误码、版本标签）

#### Phase 4: Generate Test Design Document
- **核心目标**：生成 `.design.md` 文件，定义每个 API 的测试用例列表、控件 ID（UI 类）、N-API 函数映射
- **不可跳过**：所有模式（Flow A/B/C、ArkTS-Sta）都必须生成设计文档
- **测试类型覆盖**：PARAM（参数测试）、ERROR（错误码测试）、RETURN（返回值测试）、BOUNDARY（边界值测试）
- **UI 类判定**：API 涉及组件创建/属性设置/事件回调/动效 → UI 类，需要 Phase 5A/5B
- **关键输出**：`{TestFileName}.design.md` — 测试设计文档

#### Phase 5: Generate Test Cases
- **核心目标**：基于 Phase 4 设计文档，生成非 UI 类测试代码（.test.ets）
- **仅使用 .d.ts 中声明的接口** — 禁止猜测或使用未声明的 API
- **每个用例必须包含 @tc 注解块** — 测试报告系统依赖此元数据
- **cleanup 必须处理异常** — 资源泄漏会影响后续用例执行
- **支持并行**：多个测试文件可并行生成

#### Phase 5A: Generate Demo (仅 UI 类用例)
- **触发条件**：Phase 4 设计文档中存在 UI 类用例
- **核心目标**：生成可交互的 Demo 应用，暴露控件 ID 供 UiTest 驱动
- **三方契约**：设计文档中预定义的控件 ID ↔ Demo 代码中的控件 ID ↔ UiTest 代码中的控件 ID 必须一致
- **依赖技能**：`demo-pipeline`

#### Phase 5B: Generate UiTest (仅 UI 类用例)
- **核心目标**：生成 UiTest 自动化测试代码，通过控件 ID 驱动 Demo 界面
- **与 Phase 5A 并行**：均从 Phase 4 设计文档读取控件 ID 清单
- **编译单元**：Demo + UiTest 作为同一 HAP 编译

#### Phase 7: Format & Validate
- **核心目标**：验证生成代码的格式、命名、断言、资源释放、@tc 注解完整性
- **不可跳过**：未验证的代码可能包含资源泄漏、无效断言、格式错误
- **步骤 A**：格式和上下文检查（使用 `validate_test_context.py`，5/9 项自动检查）
- **步骤 B**：代码质量深度扫描（使用 `check-test-code-quality` 技能，11 条规则）
- **ArkTS-Sta 额外**：静态语法校验（使用 `arkts-static-spec` 技能）

#### Phase 8: Build Verification
- **核心目标**：编译测试套，验证代码在目标编译环境中可通过
- **支持独立模式**：用户仅要求编译时，跳过 Phase 1-7 直接进入
- **异步编译**：使用 `scripts/async_build.sh` 后台编译
- **编译失败处理**：自动分析错误日志，修复后重试（最多 3 次）

#### Phase 10: Coverage Verification
- **核心目标**：对比 before/after 覆盖率，量化测试用例的覆盖率贡献
- **Flow A/B**：Phase 2 生成 before baseline，Phase 10 生成 after 并用 `compare_uncovered.py` 对比
- **Flow C**：仅执行 after 扫描（无 before baseline），覆盖率表标注"生成前: 0（新增接口）"

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

## Key Constraints

1. **Validation is mandatory** — Phase 7 can never be skipped（跳过会导致无效测试、资源泄漏、编译失败等问题流入下游）
2. **Strict API adherence** — Only use interfaces declared in `.d.ts` files（未声明的接口在编译环境中不存在，生成的代码无法编译）
3. **No project config modification** — Only create test files in designated directories（修改 BUILD.gn 等配置会导致编译环境损坏、影响其他开发者）
4. **@tc annotation required** — Every test case must have standard `@tc` block（缺少 @tc 则测试报告系统无法识别用例元数据）
5. **Design-driven generation** — Phase 4 generates design docs, Phase 5 generates test code based on design docs（确保从测试代码到需求的完整可追溯性）。Phase 4 在所有模式下（Flow A 补充用例、Flow B 标准扫描、Flow C 新增接口、ArkTS-Sta 静态模式）都不可跳过，必须先生成设计文档再生成测试代码。跳过会导致：控件 ID 无从追溯、测试意图不明确、后续维护困难
6. **Conventions shared across phases** — `references/conventions/` is loaded in both Phase 5 (generation) and Phase 7 (validation)（生成和验证使用同一套规范，确保一致性）
7. **Error handling** — When any Phase execution fails or encounters unexpected results, read `references/error_handling.md` for recovery guidance
8. **Demo-UiTest contract** — 控件 ID 在 Phase 4 设计文档中预定义，Demo 生成和 UiTest 测试代码生成均从设计文档读取，三方（设计文档 ↔ Demo ↔ UiTest）必须一致
9. **ETS 版本命名规范** — 目录名、bundleName、hap_name、用例名必须遵循 `references/conventions/ets_version_naming.md` 中的版本差异矩阵，否则 CodeCheck 门禁拦截（门禁使用 `Acts.*Test` 正则校验 hap_name，Static 后缀位置错误会被拦截）
10. **prebuilts 保护** — 修改 `{OH_ROOT}/prebuilts/` 下的任何文件前，必须先创建备份（同级别加 `.bak.{timestamp}` 后缀）
11. **已废弃接口处理** — 若接口在 .d.ts 中标记了 @deprecated，且无特殊要求，跳过该接口不生成用例；新生成的测试代码中禁止调用已废弃接口，参考历史代码发现废弃接口时用已知新接口替代（不修改历史代码）

## Anti-Patterns

### NEVER 使用未在.d.ts中声明的接口
- **原因**：编译环境中不存在该接口，代码无法编译
- **正确做法**：仅使用.d.ts中明确声明的接口和参数

### NEVER 修改BUILD.gn等项目配置文件
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

### NEVER 为没有@throws声明的API构造错误码测试
- **原因**：.d.ts中未声明@throws的API没有定义错误码，构造错误码测试无规范依据
- **正确做法**：仅对.d.ts中明确声明@throws的API生成错误码测试

### NEVER 跳过 Phase 4 测试设计文档
- **原因**：没有设计文档，Demo/UiTest/测试代码之间的控件 ID 契约无法保证，用例缺乏可追溯性
- **正确做法**：Phase 4 在所有模式下（Flow A 补充用例、Flow B 标准扫描、Flow C 新增接口、ArkTS-Sta 静态模式）都必须生成设计文档（`.design.md`），Phase 5 基于设计文档生成代码。无论用例数量多少，都必须先生成设计文档再生成测试代码
- **后果**：跳过会导致控件 ID 不一致、测试意图无法追溯、后续维护困难。且不生成设计文档的测试代码无法通过 Phase 7 验证中的 A.10/A.11 检查项

### NEVER 跳过 Phase 2 before/after 覆盖率对比
- **原因**：没有 before baseline 无法量化测试用例的覆盖率贡献
- **正确做法**：Phase 2 执行 `extract_uncovered.py` 生成 before baseline，Phase 10 执行 `compare_uncovered.py` 对比

### NEVER 不经备份直接修改 prebuilts 文件
- **原因**：prebuilts 中的 SDK 和编译工具版本是编译环境的核心依赖，误删或覆盖将导致编译环境不可用
- **正确做法**：先备份 `cp -r {目标路径} {目标路径}.bak.$(date +%Y%m%d_%H%M%S)`，再修改
- **后果**：环境损坏后恢复耗时长，影响其他开发者

### NEVER 为已废弃接口生成测试用例
- **原因**：标记 @deprecated 的接口已被弃用，测试价值低且维护成本高
- **正确做法**：跳过 @deprecated 接口（除非用户明确要求），参考历史代码时若发现废弃接口，依据 .d.ts 中的 @useinstead 使用新接口替代
- **后果**：生成废弃接口测试浪费资源，且废弃接口可能在后续版本被移除

### NEVER 在新生成的代码中调用已废弃接口
- **原因**：废弃接口在后续版本可能被移除，生成的测试将无法维护
- **正确做法**：参考历史代码时若发现 @deprecated 接口，在新生成的代码中使用已知的新接口替代（不修改历史代码）
- **后果**：依赖废弃接口的测试用例在 SDK 升级后编译失败

## Thinking Framework: Before You Generate

在 Phase 5 生成任何测试代码之前，对每个目标 API 问自己以下问题：

### API 特性分析

| 问题 | 为什么重要 | 影响生成策略 |
|------|----------|-------------|
| **是否有副作用？** | 有副作用的 API 调用顺序不可随意更改 | 测试间需要 cleanup/restore，不能并行 |
| **是否依赖系统状态？** | 依赖蓝牙/WiFi/位置等硬件状态的 API 需要特定环境 | 需要 beforeAll/afterAll 管理状态，断言可能因环境不可用而跳过 |
| **是否有资源分配？** | 打开文件/创建连接/分配内存的 API 必须释放资源 | cleanup 步骤中必须处理异常和释放 |
| **是否是异步/回调？** | 异步 API 返回 Promise 或接受回调，断言时机不同 | 使用 done() 或 async/await，不能同步断言 |
| **是否涉及 UI 组件？** | UI 类 API 需要组件树渲染后才能测试 | 需要 Demo 应用（Phase 5A）+ UiTest（Phase 5B），不能直接单元测试 |
| **是否有 @throws 声明？** | .d.ts 中声明了 @throws 的 API 有明确错误码可测试 | 生成 ERROR 类型测试；未声明的不要构造错误码测试 |
| **是否标记 @deprecated？** | 废弃接口测试价值低，可能在后续版本被移除 | 跳过该接口（除非用户要求），参考 @useinstead 使用新接口 |
| **@since 版本是否匹配目标？** | API 可能在目标 SDK 版本中不存在 | 检查 @since 标签，高于目标版本的 API 不可用 |

### 测试设计决策树

```
API 是否有 @throws？
├── 是 → 生成 ERROR 类型测试（错误码断言）
│        是否有副作用？
│        ├── 是 → 测试间需要 cleanup
│        └── 否 → 可并行执行
└── 否 → 不生成错误码测试
         是否涉及 UI 组件？
         ├── 是 → Phase 5A 生成 Demo + Phase 5B 生成 UiTest
         │        控件 ID 从 Phase 4 设计文档读取
         └── 否 → Phase 5 生成标准 .test.ets
                  是否有资源分配？
                  ├── 是 → cleanup 中必须 try-catch 释放
                  └── 否 → 标准参数/返回值/边界值测试
```

### 用例数量估算

| API 类型 | 建议用例数 | 覆盖维度 |
|----------|-----------|---------|
| 简单 get/set 属性 | 3-5 | 正常值 + 边界值 + 特殊值 |
| 带回调的事件 API | 5-8 | 正常触发 + 参数校验 + 回调异常 + 多次触发 |
| 系统能力 API | 8-12 | 各参数组合 + 错误码 + 边界值 + 并发/状态 |
| UI 组件创建型 | 5-8 | 创建 + 销毁 + 属性设置 + 事件触发 |
| 异步操作 API | 5-8 | 正常完成 + 超时 + 取消 + 并发调用 |

## Common Failure Patterns

### 编译失败：API不存在
- **症状**：`Error: Cannot find name 'xxx'`
- **根因**：使用了目标SDK版本中不存在的API
- **修复**：检查API的@since标签，确认目标版本支持

### 编译失败：静态语法不兼容
- **症状**：`ESE0143 Unresolved reference` 或 `ESE0046 Type not compatible`
- **根因**：ArkTS-Sta项目中使用了动态语法特性
- **修复**：参考 `arkts-static-spec` skill 转换语法

### 覆盖率扫描失败：路径过长
- **症状**：APICoverageDetector在Windows上报路径错误
- **根因**：Windows 260字符路径限制 + XTS深层目录结构
- **修复**：将工具放在磁盘根目录（如 `D:\APICoverageDetector`）

### 覆盖率无变化
- **症状**：Phase 9对比显示0%改进
- **根因**：生成的测试未实际调用未覆盖的API
- **修复**：检查测试代码是否正确导入和调用了目标API

### 测试注册失败
- **症状**：测试文件存在但不被执行
- **根因**：未在List.test.ets中注册新测试文件
- **修复**：使用 `scripts/register_test.py` 注册

### Demo-UiTest控件ID不一致
- **症状**：UiTest运行时找不到控件
- **根因**：Demo中的控件ID与UiTest代码中引用的ID不匹配
- **修复**：三方（设计文档 ↔ Demo ↔ UiTest）必须从Phase 4设计文档读取同一份控件ID

## Quick Reference

| Subsystem | Kit | Test Path | Config Path |
|-----------|-----|-----------|-------------|
| testfwk | @kit.TestKit | test/xts/acts/testfwk/ | references/subsystems/testfwk/ |
| ArkUI | @kit.ArkUI | test/xts/acts/arkui/ | references/subsystems/ArkUI/ |
| ArkWeb | @kit.ArkWeb | test/xts/acts/arkweb/ | references/subsystems/ArkWeb/ |
| multimedia | @kit.MediaKit | test/xts/acts/multimedia/ | references/subsystems/multimedia/ |
| ability | @kit.AbilityKit | test/xts/acts/ability/ | references/subsystems/ability/ |

## 分批执行模式（Batch Mode）

当未覆盖 API 数量较多时，支持分批生成测试用例。详见 `prompts/batch-mode.md`。

**分批决策依据**（并非简单按API数量>20分批）：

| 因素 | 倾向完整流程 | 倾向分批执行 |
|------|------------|------------|
| API数量 | ≤20 | >20 |
| API复杂度 | 简单（单参数） | 复杂（回调/异步/多态） |
| 模块分散度 | 同一模块 | 跨多个模块 |
| Context窗口余量 | 充裕 | 紧张 |
| 用户时间要求 | 不急 | 需要快速看到部分结果 |

**分批经验**：同模块API尽量同批（共享import和helper函数）；UI类API和非UI类API分开（不同的生成流程）。

## APICoverageDetector 工具

集成于 Phase 2/9，**支持 Windows 原生和 WSL 环境**（WSL 通过 `/mnt/d/...` 路径调用 `.exe`）。Linux 计算云/远程服务器不可用，需用户提供扫描结果或跳过扫描。路径无效时向用户确认：1）更新路径；2）提供扫描结果（CSV/XLSX）；3）跳过扫描。详细用法见 `docs/ASYNC_COVERAGE_SCAN.md`，扫描流程见 `prompts/phase-2-coverage.md`。

## Documentation

**所有文档路径使用 `{skill_root}/docs/` 前缀**，其中 `skill_root` 从配置文件读取。

> **注意**：`docs/` 目录下的文件供**人类用户参考**，Agent 在执行期间**不加载**这些文件。如需特定知识（如异步扫描流程），请加载对应的 prompt 文件（如 `prompts/phase-2-coverage.md`）。

| Doc | Path | Purpose |
|-----|------|---------|
| Usage Guide | `docs/USAGE.md` | 3 usage methods with examples |
| Cross-Platform Config | `docs/CROSS_PLATFORM_CONFIG.md` | Cross-platform configuration with hvigor support |
| Config Guide | `docs/CONFIG.md` | Configuration mechanism |
| Troubleshooting | `docs/TROUBLESHOOTING.md` | 11 FAQ items |
| Async Coverage Scan | `docs/ASYNC_COVERAGE_SCAN.md` | APICoverageDetector 工具详解 + 异步扫描流程 |
| Demo Integration Plan | `docs/DEMO_INTEGRATION_PLAN.md` | Demo Pipeline 整合方案（Phase 5A/5B） |
