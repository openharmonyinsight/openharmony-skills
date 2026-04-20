---
name: oh-capi-xts-gen
description: |
  OpenHarmony CAPI N-API 封装测试用例生成器（方式2）。自动解析 .h 头文件，生成 C++ N-API 封装和 ETS/ArkTS 测试代码。

  **触发此技能的场景**：
  - 用户提到 CAPI、C 测试、Native 测试、原生测试、.h 文件解析
  - 用户需要生成 N-API 封装测试（不是 gtest）
  - 用户提到覆盖率报告、补充测试、缺失测试
  - 用户需要编译或验证 CAPI 测试套
  - 用户提到异步编译、后台编译、编译验证
  - 用户提到 XTS 测试、OpenHarmony 测试、子系统测试

  **核心功能**：
  1. 头文件解析 → 提取 API 信息
  2. 测试用例生成 → C++ N-API 封装 + ETS 测试代码
  3. 编译验证 → 异步编译 + 错误修复
  4. 代码验证 → N-API 三重校验 + 格式检查

  **支持子系统**：multimedia、bundlemanager、ability、arkui、hilog 等

  **当用户提供覆盖率报告时**：自动切换到覆盖率报告驱动模式（高效精准）
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# oh-capi-xts-gen

OpenHarmony CAPI XTS 测试用例生成器 — 方式2（N-API 封装测试）

## Architecture Overview

```
用户输入(.h) → L1_Analysis（解析头文件）→ L2_Generation（生成N-API封装+ETS测试）→ L3_Validation（三重校验+编译）→ 输出
                ↑                              ↑
          references/subsystems/        modules/conventions/（测试框架规范）
```

## Quick File Index

| 我要做什么 | 看哪个文件 |
|-----------|-----------|
| 解析 .h 头文件 | `modules/L1_Analysis/parser/unified_api_parser_c.md` |
| 读取文档 | `modules/L1_Analysis/parser/doc_reader.md` |
| 解析工程配置 | `modules/L1_Analysis/parser/project_parser.md` |
| 分析覆盖率 | `modules/L1_Analysis/analyzer/coverage_analyzer.md` |
| 生成 C++ N-API 封装 | `modules/L2_Generation/generator/test_generation_c.md` |
| N-API 基础模式 | `modules/L2_Generation/generator/test_patterns_napi_ets.md` |
| N-API 高级模式 | `modules/L2_Generation/generator/test_patterns_napi_ets_advance.md` |
| N-API API 参考 | `modules/L2_Generation/generator/napi_api_reference.md` |
| 工程配置模板 | `modules/L2_Generation/generator/project_config_templates.md` |
| 测试套结构检查 | `modules/L2_Generation/generator/test_suite_structure_checklist.md` |
| 三重校验 | `modules/L2_Generation/generator/verification_common.md` |
| 编译测试套 | `modules/L3_Validation/builder/build_workflow_c.md` |
| 编译环境配置 | `modules/L3_Validation/builder/linux_compile_env_setup_c.md` |
| Linux 编译流程 | `modules/L3_Validation/builder/linux_compile_workflow_c.md` |
| 提取测试套名称 | `modules/L3_Validation/builder/quick_reference_extract_suite_name.md` |

## Prerequisites

读取 OH_ROOT 路径：`.opencode/skills/oh-capi-xts-gen/.oh-capi-xts-config.json`

CAPI 头文件路径：`{OH_ROOT}/interface/sdk_c/`

## Universal Constraints

1. 严格按照 `.h` 头文件声明的接口生成 N-API 封装和测试用例
2. 每个测试用例必须包含标准 `@tc` 注释块
3. hypium 导入语句必须符合规范
4. 测试用例命名使用小驼峰 camelCase
5. 禁止修改工程目录中的非测试文件
6. N-API 三重校验步骤不可跳过

## Test Case Naming Format

```
SUB_[Subsystem]_[Module]_[API]_[Type]_[Sequence]
```

Types: PARAM / ERROR / RETURN / BOUNDARY / MEMORY

Examples: `SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001`, `SUB_BUNDLEMANAGER_BUNDLE_OH_NativeBundle_GetMetadata_RETURN_001`

## Generation Architecture

```
C API (.h) → N-API 封装 (C++) → JS 接口 (index.d.ts) → ETS/ArkTS 测试 (.test.ets)
```

## Workflow

### Branch Selection

| Branch | Trigger | Phase 3 | Generation Target |
|--------|---------|---------|-------------------|
| **Flow A** | User provides coverage report (trigger: 覆盖率报告、补充测试、缺失测试) | Style scan only — extract code style from existing tests, do NOT re-analyze coverage | 补充已有工程 — generate only missing tests per coverage report, never create new project |
| **Flow B** | No coverage report (default) | Full coverage analysis — scan all existing tests, analyze method/param/error-code coverage, generate gap report | 优先补充已有工程 > 创建新工程（must copy from `template_project/capi_test_template/`） |

### Flow A: Coverage-Report-Driven

```
Phase 1 (Config) → Phase 2 (Header Parse) → Phase 3 (Style Scan Only) → Phase 4 (Generate) → Phase 5 (Verify) → Phase 6 (Build) → Phase 7 (Output)
```

1. Parse coverage report to extract missing test items
2. Scan existing test files for code style only (naming patterns, comment style, test structure)
3. Generate tests directly per report's missing items (do NOT re-analyze existing coverage)
4. Supplement tests in existing project, never create new project

### Flow B: Standard Process (Default)

```
Phase 1 (Config) → Phase 2 (Header Parse) → Phase 3 (Full Coverage) → Phase 4 (Generate) → Phase 5 (Verify) → Phase 6 (Build) → Phase 7 (Output)
```

Flow B performs full coverage analysis in Phase 3 (scans all existing test files, generates gap report). Flow A only performs style scan when coverage report already exists.

### Phase Details

| Phase | Name | Key Module | Mandatory |
|-------|------|------------|-----------|
| 1 | Determine Subsystem Config | `references/subsystems/_common.md` + subsystem config | Yes |
| 2 | Header File Parsing | `modules/L1_Analysis/parser/unified_api_parser_c.md` | Yes |
| 3 | Coverage Analysis / Style Scan | `modules/L1_Analysis/analyzer/coverage_analyzer.md` | Yes |
| 4 | Generate Test Cases | `modules/L2_Generation/generator/test_generation_c.md` + `test_patterns_napi_ets.md` | Yes |
| 5 | N-API Triple Verification | `modules/L2_Generation/generator/verification_common.md` | **MANDATORY — NEVER SKIP** |
| 6 | Build Verification | `modules/L3_Validation/builder/build_workflow_c.md` | Recommended |
| 7 | Output Results | — | Yes |

Phase 1 config loading order: Core → Subsystem → Module (priority: User Custom > Module Config > Subsystem Config > Core Config)

Phase 2 info source priority: `.h` header (highest) → subsystem config → reference examples

Phase 4 generated artifacts:

| Artifact | Path |
|----------|------|
| C++ N-API wrapper | `entry/src/main/cpp/NapiTest.cpp` |
| TypeScript declaration | `entry/src/main/cpp/types/libentry/index.d.ts` |
| ETS test cases | `entry/src/ohosTest/ets/test/*.test.ets` |
| Build config | BUILD.gn, Test.json, etc. |

## Module Loading (Reference Injection Map)

Load modules based on the triggered usage pattern. **Only load what's needed for the current phase.**

| Phase | Always Load | Conditionally Load |
|-------|-------------|-------------------|
| 1 | `references/subsystems/_common.md` | `references/subsystems/{Subsystem}/_common.md`, `{Module}.md` |
| 2 | `modules/L1_Analysis/parser/unified_api_parser_c.md` | `modules/L1_Analysis/parser/doc_reader.md`, `modules/L1_Analysis/parser/project_parser.md` |
| 3 | `modules/L1_Analysis/analyzer/coverage_analyzer.md` | — |
| 4 | `modules/L2_Generation/generator/test_generation_c.md`, `modules/L2_Generation/generator/test_patterns_napi_ets.md` | `modules/L2_Generation/generator/test_patterns_napi_ets_advance.md`（回调/异步/句柄类 API）, `modules/L2_Generation/generator/project_config_templates.md`（新建工程）, `modules/L2_Generation/generator/napi_api_reference.md`（不常用 napi 函数） |
| 5 | `modules/L2_Generation/generator/verification_common.md` | `modules/L2_Generation/generator/test_suite_structure_checklist.md` |
| 6 | `modules/L3_Validation/builder/build_workflow_c.md` | `modules/L3_Validation/builder/linux_compile_env_setup_c.md`（环境配置）, `modules/L3_Validation/builder/linux_compile_workflow_c.md`（Linux 详细流程）, `modules/L3_Validation/builder/quick_reference_extract_suite_name.md`（提取测试套名称） |
| 7 | — | — |
| Error handling | `references/error_handling.md` | All phases |

## Configuration Architecture

```
Priority: User Custom > Module Config > Subsystem Config > Core Config

Core:      references/subsystems/_common.md          (shared mandatory + default rules)
Subsystem: references/subsystems/{Subsystem}/_common.md  (differential rules)
Module:    references/subsystems/{Subsystem}/{Module}.md  (module-specific rules)
```

## Key Constraints

1. **Verification is mandatory** — Phase 5 (N-API 三重校验) can never be skipped
2. **Strict API adherence** — Only use interfaces declared in `.h` header files
3. **Module name must be `entry`** — `nm_modname = "entry"`, ETS imports from `libentry.so`
4. **No project config modification** — Only create test files in designated directories
5. **Template copy required** — Creating new test suite must copy from `template_project/capi_test_template/`
6. **@tc annotation required** — Every test case must have standard `@tc` block
7. **Error handling uses `napi_throw_error`** — Do not return error objects from N-API functions

## Mandatory Phase 5: N-API Triple Verification

This phase is the **core quality gate**. Skipping it will cause runtime crashes, missing function registrations, and type mismatches between C++, TypeScript, and ETS.

### Self-Verification Method (perform after generating all files)

After generating NapiTest.cpp, index.d.ts, and .test.ets files, you MUST perform the following cross-checks before considering generation complete. For each check, list the extracted items and confirm they match.

#### Check 1: C++ Registration Completeness

Extract all `static napi_value` function definitions from NapiTest.cpp, then verify each one appears in the `napi_property_descriptor desc[]` array in `Init`. Report any missing registrations.

#### Check 2: TypeScript ↔ C++ Consistency

Extract all JS function names (the first string parameter) from `napi_property_descriptor desc[]`, then verify each one has a matching `export const` in `index.d.ts`. Report any missing declarations.

#### Check 3: ETS ↔ TypeScript Consistency

Extract all `testNapi.xxx` calls from .test.ets files, then verify each `xxx` has a matching `export const` in `index.d.ts`. Report any undefined references.

#### Output Format

After completing all checks, output a summary:

```
=== N-API Triple Verification ===
C++ functions defined: N
C++ functions registered: N (missing: none)
TypeScript declarations: N (missing: none)
ETS testNapi calls: N (undefined: none)
Result: PASS
```

If any check fails, fix the generated files immediately before proceeding.

### Automated Verification Scripts (run if target path exists)

```bash
bash scripts/verify_napi_triple.sh ${TARGET_PATH}
bash scripts/check_test_suite_structure.sh ${TARGET_PATH}
```

## Generation Strategy

优先级：**补充已有工程 > 创建新工程**

1. 用户指定目标测试套 → 直接在该工程中补充用例
2. 分析后发现可添加到已有工程 → 在已有工程中补充用例
3. 用户未指定且无合适已有工程 → 创建新工程（必须先复制模板）

## Supported Subsystems

| Subsystem | Config Path | Key Notes |
|-----------|------------|------------|
| multimedia | `references/subsystems/multimedia/` | Camera include 用 `<ohcamera/xxx.h>` |
| bundlemanager | `references/subsystems/bundlemanager/` | |
| ability | `references/subsystems/ability/` | |
| hilog | `references/subsystems/hilog/` | |

## Test Suite Structure

```
{测试套名称}/
├── AppScope/app.json5
├── BUILD.gn
├── Test.json
├── build-profile.json5
├── oh-package.json5
├── signature/openharmony.p7b
├── entry/
│   └── src/
│       ├── main/
│       │   ├── cpp/
│       │   │   ├── NapiTest.cpp
│       │   │   ├── CMakeLists.txt
│       │   │   └── types/libentry/index.d.ts
│       │   ├── ets/entryability/EntryAbility.ts
│       │   ├── module.json5
│       │   └── syscap.json
│       └── ohosTest/
│           └── ets/test/*.test.ets
```

---

**版本**: 2.2.0 | **更新日期**: 2026-04-08 | **兼容性**: OpenHarmony API 10+
