---
name: ohos-test-capi-xts-generation
description: Use this skill when generating XTS test cases for OpenHarmony C/C++ CAPI via N-API wrapping. Automatically parses .h header files to generate C++ N-API bindings and ETS/ArkTS test code. Triggers include CAPI, C testing, Native testing, .h file parsing, N-API wrapper generation, coverage report driven test supplement, async build verification, and subsystem-level XTS testing.
metadata:
  author: openharmony
  scope: common
  stage: testing
  domain: capi
  capability: xts-generation
  version: 0.1.0
  status: draft
  tags:
    - xts
    - capi
    - napi
    - test-generation
  related-skills:
    - ohos-test-arkts-xts-generation
    - check-test-code-quality
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# ohos-test-capi-xts-generation

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
| 自动修复 N-API 三重校验问题 | `scripts/auto_fix_napi_triple.sh` |

## Prerequisites

读取 OH_ROOT 路径：`.opencode/skills/ohos-test-capi-xts-generation/.oh-capi-xts-config.json`

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

---

#### Phase 1: Determine Subsystem Config

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read
[`references/subsystems/_common.md`](references/subsystems/_common.md) (~150 lines)
completely from start to finish. **NEVER set any range limits when reading this file.**

**Do NOT load** subsystem-specific configs unless user explicitly provides a subsystem name.

**Conditional Load** (only when user specifies a subsystem):
- `references/subsystems/{Subsystem}/_common.md`
- `references/subsystems/{Subsystem}/{Module}.md`

**Configuration Loading Priority**:
```
User Custom > Module Config > Subsystem Config > Core Config
```

---

#### Phase 2: Header File Parsing

**MANDATORY - READ ENTIRE FILE**: Read [`modules/L1_Analysis/parser/unified_api_parser_c.md`](modules/L1_Analysis/parser/unified_api_parser_c.md) (~400 lines) completely.

**Do NOT load** `doc_reader.md` or `project_parser.md` unless explicitly needed.

**Conditional Load**:
- `modules/L1_Analysis/parser/doc_reader.md` — only when parsing API documentation files
- `modules/L1_Analysis/parser/project_parser.md` — only when analyzing existing project structure

**Info Source Priority**: `.h` header (highest) → subsystem config → reference examples

---

#### Phase 3: Coverage Analysis / Style Scan

**MANDATORY - READ ENTIRE FILE**: Read [`modules/L1_Analysis/analyzer/coverage_analyzer.md`](modules/L1_Analysis/analyzer/coverage_analyzer.md) (~600 lines) completely.

**Flow A (Coverage-Report-Driven)**: Perform style scan ONLY — extract code style patterns from existing tests, do NOT re-analyze coverage.

**Flow B (Standard Process)**: Perform full coverage analysis.

**Do NOT load** any additional modules in this phase.

---

#### Phase 4: Generate Test Cases

**MANDATORY - READ ENTIRE FILE**: Read both:
1. [`modules/L2_Generation/generator/test_generation_c.md`](modules/L2_Generation/generator/test_generation_c.md) (~800 lines)
2. [`modules/L2_Generation/generator/test_patterns_napi_ets.md`](modules/L2_Generation/generator/test_patterns_napi_ets.md) (~600 lines)

**Do NOT load** `test_patterns_napi_ets_advance.md` unless dealing with callback/async/handle APIs.

**Conditional Load**:
- `modules/L2_Generation/generator/test_patterns_napi_ets_advance.md` — only for callback/async/handle class APIs
- `modules/L2_Generation/generator/project_config_templates.md` — only when creating new project (includes full directory structure)
- `modules/L2_Generation/generator/napi_api_reference.md` — only when using uncommon N-API functions

**Generated Artifacts**:

| Artifact | Path |
|----------|------|
| C++ N-API wrapper | `entry/src/main/cpp/NapiTest.cpp` |
| TypeScript declaration | `entry/src/main/cpp/types/libentry/index.d.ts` |
| ETS test cases | `entry/src/ohosTest/ets/test/*.test.ets` |
| Build config | BUILD.gn, Test.json, etc. |

---

#### Phase 5: N-API Triple Verification

**MANDATORY - READ ENTIRE FILE**: Read [`modules/L2_Generation/generator/verification_common.md`](modules/L2_Generation/generator/verification_common.md) (~600 lines) completely.

**MANDATORY - NEVER SKIP**: This phase is core quality gate. Skipping will cause:
- Runtime crashes
- Missing function registrations
- Type mismatches between C++, TypeScript, and ETS

**Conditional Load**:
- `modules/L2_Generation/generator/test_suite_structure_checklist.md` — only when validating project structure

**Automated Verification Scripts** (run if target path exists):
```bash
bash scripts/verify_napi_triple.sh ${TARGET_PATH}
bash scripts/check_test_suite_structure.sh ${TARGET_PATH}
```

**Auto-Fix Script** (use when verification fails):
```bash
bash scripts/auto_fix_napi_triple.sh ${TARGET_PATH}
```

---

#### Phase 6: Build Verification

**MANDATORY - READ ENTIRE FILE**: Read [`modules/L3_Validation/builder/build_workflow_c.md`](modules/L3_Validation/builder/build_workflow_c.md) (~500 lines).

**Do NOT load** `linux_compile_env_setup_c.md` or `linux_compile_workflow_c.md` unless explicitly setting up environment.

**Conditional Load**:
- `modules/L3_Validation/builder/linux_compile_env_setup_c.md` — only for environment configuration
- `modules/L3_Validation/builder/linux_compile_workflow_c.md` — only for detailed Linux compilation workflow
- `modules/L3_Validation/builder/quick_reference_extract_suite_name.md` — only when extracting test suite names

---

#### Phase 7: Output Results

No module loading required in this phase.

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

---

**版本**: 2.2.0 | **更新日期**: 2026-04-08 | **兼容性**: OpenHarmony API 10+
