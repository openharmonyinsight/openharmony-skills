---
name: ohos-test-capi-xts-generation
description: >
  OpenHarmony CAPI XTS测试用例生成器。解析.h头文件，生成C++ N-API封装和ETS/ArkTS测试代码，支持覆盖率分析和编译验证。
  Use when: (1) 用户提到CAPI、C测试、Native测试、原生测试、头文件解析,
  (2) 用户需要生成N-API封装测试（不是gtest）,
  (3) 用户提到覆盖率报告、补充测试、缺失测试,
  (4) 用户需要编译或验证CAPI测试套,
  (5) 用户提到异步编译、后台编译、编译验证,
  (6) 用户提到XTS测试、OpenHarmony测试、子系统测试。
  Trigger keywords: CAPI, N-API, napi, .h文件, 头文件解析, Native测试, C测试,
  原生测试, 编译, build, compile, 覆盖率报告, 未覆盖API, 测试套编译, XTS,
  async_build, cleanup_group, N-API封装, 三重校验
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
| **生成测试设计文档** | `modules/L2_Generation/generator/design_doc_generator_c.md` |
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
| CAPI 测试模式参考（参数验证、内存释放、边界值） | `references/test_patterns_c.md` |
| 测试设计文档格式模板 | `references/design_doc_guide.md` |
| 编译/运行错误排查 | `references/error_handling.md` |

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
7. 测试设计文档不可跳过 — Phase 4 必须在 Phase 5 代码生成前完成

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
Phase 1 (Config) → Phase 2 (Header Parse) → Phase 3 (Style Scan Only) → Phase 4 (Design Doc) → Phase 5 (Generate) → Phase 6 (Verify) → Phase 7 (Build) → Phase 8 (Output)
```

1. Parse coverage report to extract missing test items
2. Scan existing test files for code style only (naming patterns, comment style, test structure)
3. Generate tests directly per report's missing items (do NOT re-analyze existing coverage)
4. Supplement tests in existing project, never create new project

### Flow B: Standard Process (Default)

```
Phase 1 (Config) → Phase 2 (Header Parse) → Phase 3 (Full Coverage) → Phase 4 (Design Doc) → Phase 5 (Generate) → Phase 6 (Verify) → Phase 7 (Build) → Phase 8 (Output)
```

Flow B performs full coverage analysis in Phase 3 (scans all existing test files, generates gap report). Flow A only performs style scan when coverage report already exists.

### Phase Details

| Phase | Name | Key Module | Mandatory |
|-------|------|------------|-----------|
| 1 | Determine Subsystem Config | `references/subsystems/_common.md` + subsystem config | Yes |
| 2 | Header File Parsing | `modules/L1_Analysis/parser/unified_api_parser_c.md` | Yes |
| 3 | Coverage Analysis / Style Scan | `modules/L1_Analysis/analyzer/coverage_analyzer.md` | Yes |
| **4** | **Generate Test Design Doc** | **`modules/L2_Generation/generator/design_doc_generator_c.md`** | **MANDATORY — NEVER SKIP** |
| 5 | Generate Test Cases | `modules/L2_Generation/generator/test_generation_c.md` + `test_patterns_napi_ets.md` | Yes |
| 6 | N-API Triple Verification | `modules/L2_Generation/generator/verification_common.md` | **MANDATORY — NEVER SKIP** |
| 7 | Build Verification | `modules/L3_Validation/builder/build_workflow_c.md` | Recommended |
| 8 | Output Results | — | Yes |

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

#### Phase 4: Generate Test Design Document

**MANDATORY - READ ENTIRE FILE**: Read [`modules/L2_Generation/generator/design_doc_generator_c.md`](modules/L2_Generation/generator/design_doc_generator_c.md) completely.

**MANDATORY - NEVER SKIP**: This phase must complete before Phase 5 code generation. Design doc serves as the blueprint for test code — without it, test coverage will be incomplete and test IDs will conflict.

**Output**: A `{TestFileName}.design.md` file containing:
- All target API test case designs with unique SUB_ IDs
- Detailed test steps and expected results (no vague descriptions)
- N-API function name mapping for each test case
- Coverage statistics table

**Design Scope**:

| Condition | Design Scope |
|-----------|-------------|
| Flow A (coverage report) | Only uncovered items from report |
| Flow B (no coverage report) | All target APIs from Phase 2 |

**File Location**: Same directory as test files, named `{TestFileName}.design.md`

---

#### Phase 5: Generate Test Cases

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

#### Phase 6: N-API Triple Verification

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

#### Phase 7: Build Verification

**MANDATORY - READ ENTIRE FILE**: Read [`modules/L3_Validation/builder/build_workflow_c.md`](modules/L3_Validation/builder/build_workflow_c.md) (~500 lines).

**Do NOT load** `linux_compile_env_setup_c.md` or `linux_compile_workflow_c.md` unless explicitly setting up environment.

**Conditional Load**:
- `modules/L3_Validation/builder/linux_compile_env_setup_c.md` — only for environment configuration
- `modules/L3_Validation/builder/linux_compile_workflow_c.md` — only for detailed Linux compilation workflow
- `modules/L3_Validation/builder/quick_reference_extract_suite_name.md` — only when extracting test suite names

---

#### Phase 8: Output Results

No module loading required in this phase.

## Configuration Architecture

```
Priority: User Custom > Module Config > Subsystem Config > Core Config

Core:      references/subsystems/_common.md          (shared mandatory + default rules)
Subsystem: references/subsystems/{Subsystem}/_common.md  (differential rules)
Module:    references/subsystems/{Subsystem}/{Module}.md  (module-specific rules)
```

## Key Constraints

1. **Verification is mandatory** — Phase 6 (N-API 三重校验) can never be skipped
2. **Design doc is mandatory** — Phase 4 (测试设计文档) must complete before code generation
2. **Strict API adherence** — Only use interfaces declared in `.h` header files
3. **Module name must be `entry`** — `nm_modname = "entry"`, ETS imports from `libentry.so`
4. **No project config modification** — Only create test files in designated directories
5. **Template copy required** — Creating new test suite must copy from `template_project/capi_test_template/`
6. **@tc annotation required** — Every test case must have standard `@tc` block
7. **Error handling uses `napi_throw_error`** — Do not return error objects from N-API functions

## Anti-Patterns

### NEVER 使用未在.h头文件中声明的接口
- **原因**：N-API封装的C++函数签名必须与.h声明完全匹配，未声明的函数在编译时找不到符号
- **正确做法**：仅使用.h中明确声明的函数签名、参数类型和返回值类型

### NEVER 跳过Phase 6（N-API三重校验）
- **原因**：C++/TypeScript/ETS三层之间的函数注册、名称映射、类型转换任一不匹配都会导致运行时崩溃
- **后果**：运行时crash、函数未注册、类型不匹配——修复成本远高于预防

### NEVER 跳过Phase 4（测试设计文档）
- **原因**：没有设计文档，SUB_编号可能冲突，N-API函数名映射无据可查，测试覆盖率无法审计
- **正确做法**：Phase 4必须在Phase 5前完成，所有模式下（Flow A/B）都必须生成.design.md

### NEVER 在N-API函数中返回错误对象
- **原因**：N-API函数必须返回`napi_value`类型，错误处理应使用`napi_throw_error`抛出异常
- **正确做法**：错误时调用`napi_throw_error(env, nullptr, "error message")`并返回`nullptr`

### NEVER 修改已有工程的非测试文件
- **原因**：修改BUILD.gn、oh-package.json5等配置文件会影响其他开发者的编译环境
- **正确做法**：仅在指定目录创建/修改测试相关文件

### NEVER 在测试用例中省略@tc注解
- **原因**：测试报告系统无法识别没有@tc的用例元数据
- **正确做法**：每个测试用例必须有标准@tc块，包含编号、描述、步骤、预期结果

### NEVER 创建新工程时不从模板复制
- **原因**：CAPI测试套需要完整的工程结构（CMakeLists.txt、module.json5、Test.json等），手动创建容易遗漏关键文件
- **正确做法**：必须从`template_project/capi_test_template/`复制完整模板，再修改测试内容

### NEVER 硬编码模块名（module name）
- **原因**：OpenHarmony N-API要求`nm_modname`必须为`"entry"`，ETS侧从`libentry.so`导入，不一致会导致加载失败
- **正确做法**：统一使用`nm_modname = "entry"`，`oh-package.json5`中`name`字段对应

### NEVER 在Flow A模式下创建新工程
- **原因**：Flow A是覆盖率报告驱动模式，明确目标是补充已有工程的缺失测试
- **正确做法**：仅在已有工程中补充测试用例，如果报告对应的工程不存在应向用户确认

## Phase 6: N-API Triple Verification

**MANDATORY - READ ENTIRE FILE**: Read [`modules/L2_Generation/generator/verification_common.md`](modules/L2_Generation/generator/verification_common.md) (~600 lines) completely.

**MANDATORY - NEVER SKIP**: Skipping causes runtime crashes, missing function registrations, and type mismatches between C++, TypeScript, and ETS.

**Automated Verification Scripts** (run if target path exists):
```bash
bash scripts/verify_napi_triple.sh ${TARGET_PATH}
bash scripts/check_test_suite_structure.sh ${TARGET_PATH}
```

**Auto-Fix Script** (use when verification fails):
```bash
bash scripts/auto_fix_napi_triple.sh ${TARGET_PATH}
```

**编译/运行失败时**：加载 [`references/error_handling.md`](references/error_handling.md)（错误分级、重试策略、6 条 Common Failure Patterns 及排查路径）。

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

**版本**: 2.3.0 | **更新日期**: 2026-06-03 | **兼容性**: OpenHarmony API 10+
