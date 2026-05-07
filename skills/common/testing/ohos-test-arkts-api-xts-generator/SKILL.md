---
name: oh-xts-generator
description: OpenHarmony XTS 测试用例通用生成模板。支持各子系统测试用例生成，API 定义解析，测试覆盖率分析，代码规范检查。集成 APICoverageDetector 精确覆盖率扫描工具，支持生成前后覆盖率对比验证。当用户提到 OpenHarmony 测试、XTS 测试、测试用例生成、.d.ts 文件测试、子系统测试覆盖率、APICoverageDetector、覆盖率扫描、测试补充、测试套编译验证、Hypium 测试框架、ArkTS 测试、ArkTS-Dyn/ArkTS-Sta 测试用例、ArkTS dynamic 测试用例、ArkTS static 测试用例、批量生成测试、测试设计文档等场景时，务必使用此技能。即使用户没有明确提到"XTS"关键词，只要涉及 OpenHarmony/HarmonyOS 的 API 测试生成或覆盖率分析，都应触发此技能。
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# oh-xts-generator

> OpenHarmony XTS 测试用例通用生成模板

## 路径说明

**本文档中所有相对路径均以本技能的根目录（skill-root）为起点。**

例如：
- `prompts/system.md` 表示技能根目录下的 `prompts/system.md`
- `references/conventions/hypium_framework.md` 表示技能根目录下的 `references/conventions/hypium_framework.md`

技能根目录的绝对路径取决于所使用的工具，例如：
- opencode: `{用户主目录}/.opencode/skills/oh-xts-generator/`
- Claude Code: `{用户主目录}/.claude/skills/oh-xts-generator/`
- 其他工具: 请参考对应工具的 skill 安装目录

具体路径以 `.oh-xts-config.json` 中 `skill_root` 字段的值为准。

## 配置加载（优先级最高）

**必须首先读取配置文件**：
```
.oh-xts-config.json
```

配置文件包含：
- `skill_root`: 技能根目录的绝对路径（所有相对路径的基准点）
- `scan_tool_root`: APICoverageDetector 工具的绝对路径。**该工具仅支持 Windows 环境**（核心组件为 `.bat` 脚本和 `.exe` 可执行文件）。**推荐放在磁盘根目录**（如 `D:\APICoverageDetector`），因为 XTS 测试目录层级深、文件总量大，工具放在根目录可有效避免 Windows 路径长度超限（260字符）导致扫描失败。不同运行环境的路径参考：
  - **Windows 原生**：`D:\APICoverageDetector`
  - **WSL (Windows Subsystem for Linux)**：`/mnt/d/APICoverageDetector`（工具仍在 Windows 侧，通过 WSL 路径映射访问）
  - **Linux 计算云/远程服务器**：工具不可用，只能让用户提供已有的覆盖率扫描结果
  
  若未配置或路径无效，不应自动猜测路径，而应向用户确认以下选项之一：1）提供正确的工具路径；2）直接提供覆盖率扫描结果；3）跳过覆盖率扫描步骤，直接按用户要求生成测试用例
- `for_windows.xts_acts_path`: Windows平台XTS测试路径
- `for_windows.sdk_path`: Windows平台SDK路径
- `for_windows.deveco_studio_path`: DevEco Studio 安装路径（自动推导 `jbr/` 为 Java 路径、`tools/node/` 为 Node.js 路径）
- `for_windows.hvigor_path_1.1`: Windows平台 Hvigor 工具路径（用于 ArkTS-Dyn 动态语法项目编译）
- `for_windows.hvigor_path_1.2`: Windows平台 Hvigor 工具路径（用于 ArkTS-Sta 静态语法项目编译）
- `for_linux.OH_ROOT`: Linux平台OpenHarmony根目录

**执行顺序**：
1. 读取 `.oh-xts-config.json` 获取 `skill_root`
2. 使用 `skill_root` + 相对路径 定位所有技能文件
3. 使用平台特定路径执行覆盖率扫描和编译验证

## Prerequisites

**配置文件自动初始化**：

首次使用时，如果 `.oh-xts-config.json` 不存在，Phase 1 会自动触发配置初始化流程：
1. 检测配置文件是否存在
2. 不存在则将 `.oh-xts-config.example.json` 复制为 `.oh-xts-config.json`（包含完整字段模板）
3. 从用户消息中提取路径信息自动填充
4. 无法提取时向用户询问必要路径
5. 验证路径有效性

用户也可手动复制 `{skill_root}/.oh-xts-config.example.json` 为 `.oh-xts-config.json` 并填写路径。

**配置加载检查**（配置文件已存在时）：
1. 读取 `{skill_root}/.oh-xts-config.json` 确认 `skill_root` 值
2. 使用 `skill_root` 作为所有文件引用的根路径
3. 验证平台特定路径存在且可访问：
   - Windows: 验证 `for_windows.xts_acts_path`、`for_windows.sdk_path`、`for_windows.hvigor_path_1.1`（和 `hvigor_path_1.2`，如需 ArkTS-Sta 编译）
   - Linux: 验证 `for_linux.OH_ROOT`

**工具路径**（基于配置文件和 skill_root）：
- 覆盖率工具: `{scan_tool_root}/`（从 `.oh-xts-config.json` 的 `scan_tool_root` 字段读取；若路径无效，向用户确认路径、索要覆盖率结果、或跳过扫描步骤）
- 脚本工具: `{skill_root}/scripts/`
- 文档: `{skill_root}/docs/`
- 提示词: `{skill_root}/prompts/`
- 参考配置: `{skill_root}/references/subsystems/`

**脚本工具说明**：

| 脚本 | 用途 | 调用时机 |
|------|------|---------|
| `manage_scan_env.py` | 文件复制到扫描目录 + arkts_config.json 配置 | Phase 2 步骤 1/4、Phase 9 |
| `convert_results.py` | Excel→CSV 批量转换 | Phase 2 步骤 3.5、Phase 9 |
| `validate_test_context.py` | 测试文件生成上下文检查（5/9 项） | Phase 7 步骤 A |
| `compare_coverage.py` | 覆盖率 before/after 对比报告 | Phase 9 |
| `register_test.py` | List.test.ets 注册新测试文件 | Phase 6 |
| `extract_uncovered.py` | 提取未覆盖 API 列表 | Phase 3 |
| `sync_ets_version.py` | 同步 ets_version 到 arkts_config.json | Phase 1 |
| `async_coverage_scan.py` | 异步覆盖率扫描 | Phase 2、Phase 9 |
| `batch_manager.py` | 分批执行管理器（计划/执行/续传） | Phase 3-5 批量模式 |
| `batch_lock.py` | 文件锁（多 subagent 并发写入保护） | batch_manager.py 内部依赖 |

**必需依赖技能**：

| 依赖技能 | 用途 | 触发时机 |
|---------|------|---------|
| `check-test-code-quality` | 代码质量深度扫描（11 条规则） | Phase 7 步骤 B 必选 |
| `arkts-static-spec` | ArkTS 静态语法规范校验 | Phase 7 步骤 A，仅静态项目（ArkTS-Sta）时 |

See `docs/CROSS_PLATFORM_CONFIG.md` for detailed configuration requirements.

## Initialization

**Always read** the system prompt before starting:

```
{skill_root}/prompts/system.md
```

其中 `{skill_root}` 从 `.oh-xts-config.json` 读取。

**初始化步骤**：
1. 检查 `{skill_root}/.oh-xts-config.json` 是否存在 → 不存在则自动初始化（见 Prerequisites）
2. 读取 `{skill_root}/.oh-xts-config.json` 获取配置
3. 读取 `{skill_root}/prompts/system.md` 获取系统提示词
4. 所有后续文件引用均使用 `{skill_root}` + 相对路径格式

步骤 1-9 的详细说明见各 Phase prompt 文件：
- 步骤 1-8（ETS版本选择、配置加载、子系统确定等）→ `prompts/phase-1-config-loading.md`
- 步骤 6-9（模块加载、语法类型确定）→ 见下方

### 步骤 6: 确定需加载的模块

根据子系统类型和任务类型，确定需要加载的 L1-L4 模块（参考 SKILL.md 模块注入映射表）。

**仅加载当前阶段和后续阶段需要的模块，不要一次性加载所有模块。**（一次性加载所有模块会占用大量 context window，降低当前阶段生成质量，且可能导致不同阶段的规则混淆）

### 步骤 7: 确定项目语法类型（仅当用户指定在某个测试工程中添加用例时执行）

**语法类型说明**：

**当前支持的语法类型**：
- **ArkTS-Dyn**：动态语法（`'use strict'`），对应 `{xts_acts_path}\testfwk\uitest\`
  - 支持的API：大部分@ohos.UiTest API（By、On、Driver、UiDriver、Component等）
  - 生成测试用例文件：`{Module}.test.ets`
  
- **ArkTS-Sta**：静态语法（`'use static'`），对应 `{xts_acts_path}\testfwk\uitestStatic\`
  - 支持的API：部分@ohos.UiTest API（仅支持静态语法的API）
  - 生成测试用例文件：`{Module}.test.ets`（静态语法）
  - 注意：部分API（如By、On、UiDriver等）不支持静态语法，需要在生成时过滤掉

**uncovered_apis.json 中的API分类**：

根据 `uncovered_apis.json` 中的 `module` 字段判断API所属的语法类型：
- `module: "ohos.UiTest"` 且 API在 API 定义文件中 → ArkTS-Dyn（动态）
- `module: "ohos.UiTest"` 但 API 不在 API 定义文件中 → 可能是ArkTS-Sta（静态）或未在定义中
- 其他模块（如 `ohos.arkui.advanced`）→ 查看对应ets版本

**处理逻辑**：

1. **Phase 1**: 检查目标测试套的 `build-profile.json5` 中的 `arkTSVersion` 字段
2. **Phase 2**: 根据语法类型和覆盖率报告确定未覆盖API列表
   - 如果是ArkTS-Dyn项目：使用 `uncovered_apis.json` + 过滤掉不支持静态的API
   - 如果是ArkTS-Sta项目：需要从ArkTS-Sta的覆盖率报告中提取未覆盖API
3. **Phase 3-5**: 解析API详细信息并生成测试（按对应的语法类型）
4. **Phase 6**: 将测试文件注册到对应的测试套目录
    - ArkTS-Dyn项目 → `{xts_acts_path}\testfwk\uitest\`
    - ArkTS-Sta项目 → `{xts_acts_path}\testfwk\uitestStatic\`
5. **Phase 7-9**: 验证、编译、覆盖率检查

**关键约束更新**：
- 根据语法类型生成对应语法的测试用例
- 静态语法项目不支持@ohos.UiTest的部分API（如By、On等），需要在生成时跳过或使用特殊处理

## Architecture Overview

```
用户输入 → L1_Analysis（理解API）→ L2_Generation（生成测试）→ L3_Validation（验证+编译）→ 输出
                ↑                          ↑
          references/subsystems/     references/conventions/（框架规范）
```

## Quick File Index

| 我要做什么 | 看哪个文件 |
|-----------|-----------|
| 理解 API 定义 | `modules/L1_Analysis/parser/unified_api_parser.md` |
| 判断语法类型 | `modules/L1_Analysis/parser/unified_api_parser_syntax_filter.md` |
| 了解断言方法 | `references/conventions/hypium_framework.md` |
| 了解 ArkTS 语法 | `references/conventions/arkts_standards.md` |
| 了解命名规范 | `references/conventions/test_conventions.md` |
| 生成测试设计 | `modules/L2_Generation/generator/design_doc_generator.md` |
| 生成测试用例 | `modules/L2_Generation/generator/test_generator.md` |
| 参数/返回值/边界值测试 | `modules/L2_Generation/generator/param_test.md` |
| 错误码测试 | `modules/L2_Generation/generator/error_test.md` |
| HarmonyOS 特有测试场景 | `modules/L2_Generation/generator/HarmonyOS_Test_Design_Spec.md` |
| 查看代码模板 | `modules/L2_Generation/generator/templates.md` |
| 验证测试格式 | `modules/L3_Validation/validator/format_validator.md` |
| 编译测试套（Linux） | `modules/L3_Validation/builder/build_workflow_linux.md` |
| 编译测试套（Windows） | `modules/L3_Validation/builder/build_workflow_windows.md` |
| 处理执行错误 | `references/error_handling.md` |

## Workflow

根据用户是否提供覆盖率报告，各阶段执行方式有所不同，差异已在各 Phase 文件中说明：

**重要**：所有 Prompt File 路径均使用 `{skill_root}/` 前缀，其中 `skill_root` 从配置文件读取。

| Phase | Name | Prompt File | Flow A（有覆盖率报告） | Flow B（无覆盖率报告） |
|-------|------|-------------|----------------------|----------------------|
| 1 | Determine Subsystem Config | `prompts/phase-1-config-loading.md` | 相同 | 相同 |
| 2 | Initial Coverage Scan | `prompts/phase-2-coverage.md` | 仅代码风格扫描 | APICoverageDetector 精确扫描（支持同步/异步） |
| 3 | Targeted API Info Parsing | `prompts/phase-3-api-parsing.md` | 仅解析报告中的未覆盖项 | 仅解析 Phase 2 识别的未覆盖项 |
| 4 | Generate Test Design | `prompts/phase-4-design.md` | 仅设计报告中的未覆盖项 | 设计全部目标 API 的测试 |
| 5 | Generate Test Cases | `prompts/phase-5-generation.md` | 依据设计文档生成 | 依据设计文档生成 |
| 6 | Register Test Suites | `prompts/phase-6-registration.md` | 相同 | 相同 |
| 7 | Format & Validate | `prompts/phase-7-validation.md` | **步骤A: 生成上下文检查 + 步骤B: check-test-code-quality深度扫描** | **步骤A: 生成上下文检查 + 步骤B: check-test-code-quality深度扫描** |
| 8 | Build Verification | `prompts/phase-8-build.md` | 推荐 | 推荐 |
| 9 | Coverage Verification | `prompts/phase-9-coverage.md` | 可选 | 必须（再次扫描对比，支持异步） |
| 10 | Output Results | `prompts/phase-10-output.md` | 相同 | 相同 |

## Module Loading (Reference Injection Map)

Load modules based on the triggered usage pattern. **Only load what's needed for the current phase.**

**所有文件路径均使用 `{skill_root}/` 前缀**，其中 `skill_root` 从配置文件读取。

| Phase | Always Load | Conditionally Load |
|-------|-------------|-------------------|
| 1 | `references/subsystems/_common.md` | `references/subsystems/{Subsystem}/_common.md`, `{Module}.md` |
| 2 | `modules/L1_Analysis/tools/api_coverage_detector.md`, `modules/L1_Analysis/analyzer/coverage_analyzer.md` | `modules/L1_Analysis/analyzer/api_parameter_optional_rules.md`, `scripts/async_coverage_scan.py` (异步扫描模式) |
| 3 | `modules/L1_Analysis/parser/unified_api_parser.md` | `modules/L1_Analysis/parser/unified_api_parser_syntax_filter.md` (if syntax type check needed), `modules/L1_Analysis/parser/project_parser.md` |
| 4 | `modules/L2_Generation/generator/design_doc_generator.md` | — |
| 5 | `modules/L2_Generation/generator/test_generator.md`, `modules/L2_Generation/generator/templates.md`, `modules/L2_Generation/generator/quality_constraints.md` | `modules/L2_Generation/generator/param_test.md` (参数/返回值/边界值测试时), `modules/L2_Generation/generator/error_test.md` (错误码测试时), `modules/L2_Generation/generator/HarmonyOS_Test_Design_Spec.md` (状态机/生命周期/兼容性/安全性等特有场景), `references/conventions/arkts_standards.md` (syntax reference), `references/conventions/test_conventions.md` (naming reference), `modules/L2_Generation/generator/arkts_static_constraints.md` (ArkTS-Sta 静态项目必选，替代全量加载 arkts-static-spec) |
| 6 | — | — |
| 7 | `modules/L3_Validation/validator/format_validator.md` | `check-test-code-quality` skill (步骤B深度扫描), `arkts-static-spec` skill (静态项目语法校验), `references/conventions/hypium_framework.md`, `references/conventions/arkts_standards.md`, `references/conventions/test_conventions.md`, `references/conventions/uitest_framework.md` (if UI test) |
| 8 | `modules/L3_Validation/builder/build_workflow_linux.md` | `modules/L3_Validation/builder/build_workflow_windows.md` → compile/static/automation (if Windows) |
| 9 | `modules/L1_Analysis/tools/api_coverage_detector.md`（Flow B），`modules/L1_Analysis/verifier/coverage_verifier.md`（Flow B），`scripts/async_coverage_scan.py`（异步扫描模式） | Flow A 可选 |
| 10 | — | — |
| Error handling | `references/error_handling.md` | All phases |

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
5. **Design-driven generation** — Phase 4 generates design docs, Phase 5 generates test code based on design docs（确保从测试代码到需求的完整可追溯性）
6. **Conventions shared across phases** — `references/conventions/` is loaded in both Phase 5 (generation) and Phase 7 (validation)（生成和验证使用同一套规范，确保一致性）
7. **Error handling** — When any Phase execution fails or encounters unexpected results, read `references/error_handling.md` for recovery guidance

## Quick Reference

| Subsystem | Kit | Test Path | Config Path |
|-----------|-----|-----------|-------------|
| testfwk | @kit.TestKit | test/xts/acts/testfwk/ | references/subsystems/testfwk/ |
| ArkUI | @kit.ArkUI | test/xts/acts/arkui/ | references/subsystems/ArkUI/ |
| ArkWeb | @kit.ArkWeb | test/xts/acts/arkweb/ | references/subsystems/ArkWeb/ |
| multimedia | @kit.MediaKit | test/xts/acts/multimedia/ | references/subsystems/multimedia/ |
| ability | @kit.AbilityKit | test/xts/acts/ability/ | references/subsystems/ability/ |

## 分批执行模式（Batch Mode）

当未覆盖 API 数量较多时（>20），支持分批生成测试用例。每批最多 10 个 API，按模块分组，同模块尽量同批。使用 `scripts/batch_manager.py` 管理。

在 Phase 1 结束后向用户确认执行模式：

1. **完整流程**（Phase 2-10 一次性执行）— 适合 API 数量 ≤ 20
2. **分批执行**（每批 ≤10 API，逐批执行）— 适合大型子系统
3. **精准增量**（用户手动指定 API 范围）— 适合补充特定 API 测试

### 核心命令

```bash
python {skill_root}/scripts/batch_manager.py plan [--max-apis 10]   # 生成分批计划
python {skill_root}/scripts/batch_manager.py status                  # 查看执行状态
python {skill_root}/scripts/batch_manager.py start <batch_id>        # 开始指定批次
python {skill_root}/scripts/batch_manager.py complete <batch_id>     # 完成批次
python {skill_root}/scripts/batch_manager.py skip <batch_id>         # 跳过批次（保留已生成内容）
python {skill_root}/scripts/batch_manager.py resume                  # 查看下一个待执行批次
```

### 与 Phase 流程的集成

批量模式不改变 Phase 1-10 的定义，仅在 Phase 3-5 的**执行范围**上做分批：

| Phase | 批量模式行为 |
|-------|-------------|
| 1-2 | 不变（配置加载 + 覆盖率扫描） |
| 3 | 仅解析 `batch_manager.py start <id>` 指定的 10 个 API |
| 4 | 仅生成这 10 个 API 的测试设计 |
| 5 | 仅生成这 10 个 API 的测试用例 |
| 6-10 | 每批次执行，或全部批次完成后统一执行 |

数据持久化目录 `batch_workspace/`（含 `batch_plan.json` 分批计划、`completed.json` API 级完成状态、`batch_N_generated_apis.json` 各批次生成详情），并发安全通过 `scripts/batch_lock.py` 文件锁保护。

## APICoverageDetector 工具

集成于 Phase 2/9，用于精确的 API 覆盖率扫描。

| 环境 | 可用性 | 处理方式 |
|------|--------|---------|
| Windows/WSL | 可用 | 从 `scan_tool_root` 读取路径，执行异步扫描 |
| Linux 计算云 | 不可用 | 请用户提供已有的覆盖率扫描结果，或跳过扫描直接生成测试 |

路径无效时向用户确认：1）更新路径；2）提供扫描结果（CSV/XLSX）；3）跳过扫描。

详细文档：`docs/ASYNC_COVERAGE_SCAN.md`

## Documentation

**所有文档路径使用 `{skill_root}/docs/` 前缀**，其中 `skill_root` 从配置文件读取。

| Doc | Path | Purpose |
|-----|------|---------|
| Usage Guide | `docs/USAGE.md` | 3 usage methods with examples |
| Cross-Platform Config | `docs/CROSS_PLATFORM_CONFIG.md` | Cross-platform configuration with hvigor support |
| Config Guide | `docs/CONFIG.md` | Configuration mechanism |
| Troubleshooting | `docs/TROUBLESHOOTING.md` | 11 FAQ items |
| Async Coverage Scan | `docs/ASYNC_COVERAGE_SCAN.md` | APICoverageDetector 工具详解 + 异步扫描流程 |
