---
name: ohos-test-arkts-xts-generation
description: >
  Generate and validate OpenHarmony ArkTS XTS tests, including .d.ts parsing,
  Hypium test design, .ets generation, API coverage analysis with
  APICoverageDetector, batch generation, registration, build verification, and
  existing test quality checks. Use when the task mentions XTS, ArkTS-Dyn,
  ArkTS-Sta, APICoverageDetector, API coverage, Hypium, @tc annotations, test
  design documents, .d.ts files, .ets test files, or batch test generation.
metadata:
  author: openharmony
  scope: common
  stage: testing
  domain: arkts
  capability: xts-generation
  version: 0.1.0
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

例如：
- `prompts/system.md` 表示技能根目录下的 `prompts/system.md`
- `references/conventions/hypium_framework.md` 表示技能根目录下的 `references/conventions/hypium_framework.md`

技能根目录的绝对路径取决于所使用的工具，例如：
- opencode: `{用户主目录}/.opencode/skills/ohos-test-arkts-xts-generation/`
- Claude Code: `{用户主目录}/.claude/skills/ohos-test-arkts-xts-generation/`
- 其他工具: 请参考对应工具的 skill 安装目录

具体路径以 `.oh-xts-config.json` 中 `skill_root` 字段的值为准。

## 配置加载（优先级最高）

**必须首先读取配置文件**：`{skill_root}/.oh-xts-config.json`

配置文件核心字段：`skill_root`（所有相对路径的基准）、`scan_tool_root`（APICoverageDetector 路径，仅 Windows）、平台特定路径（`for_windows.*` / `for_linux.OH_ROOT`）。

首次使用时自动初始化：将 `.oh-xts-config.example.json` 复制为 `.oh-xts-config.json`，从用户消息提取路径或交互式询问。详见 `prompts/phase-1-config-loading.md` 步骤 0。

**工具路径**（基于配置文件和 skill_root）：
- 覆盖率工具: `{scan_tool_root}/`（路径无效时向用户确认：更新路径 / 提供扫描结果 / 跳过扫描）
- 脚本工具: `{skill_root}/scripts/`
- 提示词: `{skill_root}/prompts/`
- 参考配置: `{skill_root}/references/subsystems/`

**脚本工具速查**：

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

## Initialization

1. 读取 `{skill_root}/.oh-xts-config.json` 获取配置（不存在则自动初始化，见上方配置加载）
2. 读取 `{skill_root}/prompts/system.md` 获取系统提示词
3. 所有后续文件引用均使用 `{skill_root}` + 相对路径格式
4. 详细初始化步骤（ETS 版本选择、子系统确定、模块加载、语法类型判断等）→ `prompts/phase-1-config-loading.md`

**模块加载原则**：仅加载当前阶段需要的模块，不要一次性加载所有模块。参考下方 Module Loading 映射表。

**语法类型**：支持 ArkTS-Dyn（动态，默认）和 ArkTS-Sta（静态）。通过目标工程的 `build-profile.json5` 中 `arkTSVersion` 字段判断。两者在 API 可用性、测试目录、编译工具链上有差异，详细处理逻辑见 `prompts/phase-1-config-loading.md` 步骤 9。

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

当未覆盖 API 数量较多时（>20），支持分批生成测试用例（每批 ≤10 API）。详见 `prompts/batch-mode.md`。

## APICoverageDetector 工具

集成于 Phase 2/9，**仅支持 Windows 环境**。Linux 环境需用户提供扫描结果或跳过扫描。路径无效时向用户确认：1）更新路径；2）提供扫描结果（CSV/XLSX）；3）跳过扫描。详细用法见 `docs/ASYNC_COVERAGE_SCAN.md`，扫描流程见 `prompts/phase-2-coverage.md`。

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
