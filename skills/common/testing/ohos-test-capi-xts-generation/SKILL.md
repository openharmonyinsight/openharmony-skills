---
name: ohos-test-capi-xts-generation
description: >
  OpenHarmony CAPI XTS测试用例生成器。解析.h头文件，生成C++ N-API封装和ETS/ArkTS测试代码，支持N-API三重校验和编译验证。
  生成架构：C API (.h) → N-API 封装 (C++) → JS 接口 (index.d.ts) → ETS/ArkTS 测试 (.test.ets)。
  Use when: (1) 用户提到CAPI、C测试、Native测试、原生测试、头文件解析,
  (2) 用户需要生成N-API封装测试（不是gtest）,
  (3) 用户提到覆盖率报告、补充测试、缺失测试,
  (4) 用户提到新增接口、新API、new API,
  (5) 用户需要编译或验证CAPI测试套,
  (6) 用户提到异步编译、后台编译、编译验证,
  (7) 用户提到XTS测试、OpenHarmony测试、子系统测试,
  (8) 用户要求编译指定的测试套（如"编译xxx"、"build xxx"、"重新编译"）,
  (9) 用户提到编译失败、编译错误、重新编译。
  Trigger keywords: CAPI, N-API, napi, .h文件, 头文件解析, Native测试, C测试,
  原生测试, 编译, build, compile, 覆盖率报告, 未覆盖API, 测试套编译, XTS,
  async_build, cleanup_group, N-API封装, 三重校验, 新增接口, new API
metadata:
  author: openharmony
  scope: common
  stage: testing
  domain: capi
  capability: xts-generation
  version: 0.2.0
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
    - Edit
    - Grep
    - Glob
    - Bash
---

# ohos-test-capi-xts-generation

> OpenHarmony CAPI XTS 测试用例生成器 — 方式2（N-API 封装测试）

## 配置加载（优先级最高）

读取 `{skill_root}/.oh-capi-xts-config.json` 获取 `OH_ROOT`（源码根目录）。配置文件不存在时，提示用户设置 `OH_ROOT`。

CAPI 头文件路径：`{OH_ROOT}/interface/sdk_c/`

**脚本工具**（`{skill_root}/scripts/`）：

| 脚本 | 用途 | 调用时机 |
|------|------|---------|
| `verify_napi_triple.sh` | N-API 三重校验自动化检查 | Phase 6 |
| `check_test_suite_structure.sh` | 测试套结构完整性检查 | Phase 6 |
| `auto_fix_napi_triple.sh` | N-API 三重校验自动修复 | Phase 6 校验失败时 |
| `async_build.sh` | 异步编译（后台执行） | Phase 7 |
| `async_build_manager.py` | 异步编译状态管理 | Phase 7 |
| `cleanup_group.sh` | 清理编译残留 | Phase 7 编译前 |

**依赖技能**：

| 依赖技能 | 用途 | 触发时机 |
|---------|------|---------|
| `check-test-code-quality` | 代码质量深度扫描 | Phase 6 验证阶段 |

## Initialization

1. 读取 `{skill_root}/.oh-capi-xts-config.json` 获取 `OH_ROOT`
2. 读取 `{skill_root}/prompts/system.md` 获取系统提示词
3. 判断用户意图：
   - **编译任务**（用户提到"编译"、"build"、"重新编译"等）→ 直接进入 Phase 7 独立编译模式，跳过 Phase 1-6
   - **测试生成任务**（默认）→ 从 Phase 1 开始完整流程
4. 判断 Flow 类型：
   - 用户提到"新增接口"/"新 API"/"new API" → **Flow C**
   - 用户提供了覆盖率报告（CSV/XLSX/JSON/MD）→ **Flow A**
   - 以上均不满足 → 默认 **Flow C**（CAPI 无 APICoverageDetector 扫描工具，无法执行标准扫描）

**模块加载原则**：仅加载当前阶段需要的模块，不要一次性加载所有模块。参考各 Phase prompt 文件开头的加载指令。

## Architecture Overview

```
用户输入(.h) → L1_Analysis（解析头文件）→ L2_Generation（生成N-API封装+ETS测试）→ L3_Validation（三重校验+编译）→ 输出
                 ↑                              ↑
           references/subsystems/        modules/conventions/（测试框架规范）
```

**生成架构**：

```
C API (.h) → N-API 封装 (C++) → JS 接口 (index.d.ts) → ETS/ArkTS 测试 (.test.ets)
```

**测试用例命名格式**：`SUB_[Subsystem]_[Module]_[API]_[Type]_[Sequence]`

Types: PARAM / ERROR / RETURN / BOUNDARY / MEMORY

## Workflow

### 入口判定

| 用户意图 | 入口 Phase | 说明 |
|---------|-----------|------|
| 编译/重新编译测试套 | **Phase 7（独立编译模式）** | 跳过 Phase 1-6，直接加载 `prompts/phase-7-build.md` |
| 生成测试用例（完整流程） | Phase 1 | Phase 1-9 完整流程 |

**编译模式触发关键词**：编译、build、compile、重新编译、编译验证、编译失败

### Flow 判定规则（Phase 1 步骤 0 中检测，优先级从高到低）

| 优先级 | 条件 | Flow | 说明 |
|--------|------|------|------|
| 1 | 用户明确说明"新增接口"/"新 API"/"new API" | **Flow C** | 新增接口，直接解析全部目标 API |
| 2 | 用户提供了覆盖率报告（CSV/XLSX/JSON/MD） | **Flow A** | 基于用户报告解析覆盖缺口 |
| 3 | 以上均不满足 | **Flow C** | CAPI 无扫描工具，默认按新增接口处理 |

### Phase 总览

| Phase | Name | Prompt File | Module（技术细节） | Flow A | Flow C |
|-------|------|-------------|-------------------|--------|--------|
| 1 | Config & Subsystem | `prompts/phase-1-config.md` | `references/subsystems/_common.md` | 相同 | 相同 |
| 2 | Header File Parsing | `prompts/phase-2-header-parse.md` | `modules/L1_Analysis/parser/unified_api_parser_c.md` | 相同 | 相同 |
| 3 | Coverage / Style Scan | `prompts/phase-3-coverage.md` | `modules/L1_Analysis/analyzer/coverage_analyzer.md` | Style scan only | **跳过** |
| **4** | **Generate Test Design** | **`prompts/phase-4-design.md`** | — | 仅未覆盖项 | 全部目标 API |
| 5 | Generate Test Cases | `prompts/phase-5-generation.md` | `modules/L2_Generation/generator/test_generation_c.md` + `test_patterns_napi_ets.md` | 依据设计文档 | 依据设计文档 |
| **6** | **N-API Triple Verification** | **`prompts/phase-6-verification.md`** | `modules/L2_Generation/generator/verification_common.md`（按需参考） | 相同 | 相同 |
| 7 | Build Verification | `prompts/phase-7-build.md` | `modules/L3_Validation/builder/build_workflow_c.md`（按需参考） | 推荐 | 推荐 |
| 8 | Test Execution | `prompts/phase-8-test-execution.md` | — | 可选 | 可选 |
| 9 | Output Results | `prompts/phase-9-output.md` | — | 相同 | 相同 |

### Phase 内联指导

> 以下为关键 Phase 的简短指导，帮助在不加载完整 prompt 文件的情况下做出初步决策。详细步骤和加载规则请加载对应 `prompts/phase-X-*.md` 文件。

#### Phase 1: Determine Subsystem Config

- **核心目标**：确定子系统配置、加载子系统特定规则
- **Prompt File**：`prompts/phase-1-config.md`
- **MANDATORY**：读取 `references/subsystems/_common.md`
- **Do NOT load** 子系统配置（除非用户明确指定子系统名）

#### Phase 2: Header File Parsing

- **核心目标**：从 .h 头文件中提取 C API 的完整签名（函数名、参数类型、返回值、宏定义）
- **Prompt File**：`prompts/phase-2-header-parse.md`
- **MANDATORY**：读取 `modules/L1_Analysis/parser/unified_api_parser_c.md`
- **Info Source Priority**：`.h` 头文件（最高）→ 子系统配置 → 参考示例
- **Do NOT load** `project_parser.md`（除非明确需要）

#### Phase 3: Coverage / Style Scan

- **核心目标**：Flow A 提取代码风格；Flow C 跳过
- **Prompt File**：`prompts/phase-3-coverage.md`
- **Flow A MANDATORY**：读取 `modules/L1_Analysis/analyzer/coverage_analyzer.md`
- **Flow C**：跳过（新增接口无覆盖率数据）
- **Do NOT load** 其他 module

#### Phase 4: Generate Test Design Document

- **核心目标**：生成 `.design.md` 文件，定义每个 API 的测试用例列表、SUB_ 编号、N-API 函数名映射
- **Prompt File**：`prompts/phase-4-design.md`
- **自包含**：prompt 文件已包含完整的测试类型判定、用例字段定义、N-API 封装设计规则
- **不可跳过**：所有模式下（Flow A/C）都必须生成设计文档
- **关键输出**：`{TestFileName}.design.md`

#### Phase 5: Generate Test Cases

- **核心目标**：基于 Phase 4 设计文档，生成 N-API 封装（C++）+ 类型声明（index.d.ts）+ ETS 测试代码
- **Prompt File**：`prompts/phase-5-generation.md`
- **MANDATORY**：读取 `modules/L2_Generation/generator/test_generation_c.md` + `test_patterns_napi_ets.md`
- **仅使用 .h 中声明的接口** — 禁止猜测或使用未声明的 API
- **Do NOT load** `test_patterns_napi_ets_advance.md`（除非处理回调/异步/句柄类 API）

**Generated Artifacts**：

| Artifact | Path |
|----------|------|
| C++ N-API wrapper | `entry/src/main/cpp/NapiTest.cpp` |
| TypeScript declaration | `entry/src/main/cpp/types/libentry/index.d.ts` |
| ETS test cases | `entry/src/ohosTest/ets/test/*.test.ets` |

#### Phase 6: N-API Triple Verification

- **核心目标**：验证 C++ / TypeScript / ETS 三层之间的函数注册、名称映射、类型转换一致性
- **Prompt File**：`prompts/phase-6-verification.md`
- **按需参考**：`modules/L2_Generation/generator/verification_common.md`（校验细节不明确时）
- **不可跳过**：跳过会导致运行时 crash、函数未注册、类型不匹配
- **自动化脚本**：
  ```bash
  bash scripts/verify_napi_triple.sh ${TARGET_PATH}
  bash scripts/check_test_suite_structure.sh ${TARGET_PATH}
  ```
- **自动修复**（校验失败时）：`bash scripts/auto_fix_napi_triple.sh ${TARGET_PATH}`

#### Phase 7: Build Verification

- **核心目标**：编译测试套，验证代码在目标编译环境中可通过
- **Prompt File**：`prompts/phase-7-build.md`
- **按需参考**：`modules/L3_Validation/builder/build_workflow_c.md`（编译流程细节不明确时）
- **支持独立模式**：用户仅要求编译时，跳过 Phase 1-6 直接进入
- **异步编译**：使用 `scripts/async_build.sh` 后台编译
- **编译失败处理**：加载 `references/error_handling.md`，自动分析错误日志，修复后重试（最多 3 次）
- **Do NOT load** `linux_compile_env_setup_c.md`（除非明确设置编译环境）

#### Phase 8: Test Execution（可选）

- **核心目标**：在真机上执行测试并分析失败用例
- **Prompt File**：`prompts/phase-8-test-execution.md`
- **可选**：无设备时跳过
- **与 ArkTS phase-9 执行流程一致**：WSL 原生 / Windows PowerShell / 手动模式

#### Phase 9: Output Results

- **核心目标**：输出生成报告（任务信息、文件清单、用例统计、测试结果）
- **Prompt File**：`prompts/phase-9-output.md`
- **无额外模块加载**

## Module Loading

> **重要提示**：每个 Phase 的详细加载规则嵌入在对应 `prompts/phase-X-*.md` 文件中。
>
> SKILL.md 仅提供概念性说明：
> - **MANDATORY**：必须完整阅读的文件（前置加载）
> - **按需加载**：根据任务条件加载
> - **Do NOT Load**：禁止加载的模块

每个 Phase 的具体加载规则请参考对应 prompt 文件开头的 📚/⚙️/🚫 部分。

**目录职责**：
- `prompts/`：Phase 编排层（加载规则、执行步骤、Flow 差异）
- `modules/`：技术细节（代码模式、解析规则、校验清单）
- `references/`：子系统配置、测试模式参考、错误处理指南
- `scripts/`：自动化脚本
- `template_project/`：新工程模板

## Configuration Architecture

```
Priority: User Custom > Module Config > Subsystem Config > Core Config

Core:      references/subsystems/_common.md          (shared mandatory + default rules)
Subsystem: references/subsystems/{Subsystem}/_common.md  (differential rules)
Module:    references/subsystems/{Subsystem}/{Module}.md  (module-specific rules)
```

## Anti-Patterns

### NEVER 使用未在.h头文件中声明的接口
- **原因**：N-API封装的C++函数签名必须与.h声明完全匹配，未声明的函数在编译时找不到符号
- **后果**：链接阶段 `undefined reference` 错误

### NEVER 跳过Phase 6（N-API三重校验）
- **原因**：C++/TypeScript/ETS三层之间的函数注册、名称映射、类型转换任一不匹配都会导致运行时崩溃
- **后果**：运行时 crash、函数未注册、类型不匹配——修复成本远高于预防

### NEVER 跳过Phase 4（测试设计文档）
- **原因**：没有设计文档，SUB_编号可能冲突，N-API函数名映射无据可查，测试覆盖率无法审计
- **后果**：跳过会导致编号重复、函数映射混乱，且无法通过 Phase 6 的三重校验

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
- **正确做法**：统一使用`nm_modname = "entry"`

### NEVER 在Flow A模式下创建新工程
- **原因**：Flow A是覆盖率报告驱动模式，明确目标是补充已有工程的缺失测试
- **正确做法**：仅在已有工程中补充测试用例，如果报告对应的工程不存在应向用户确认

### NEVER 在N-API封装中忽略内存所有权转移
- **原因**：C API返回的指针/缓冲区可能需要调用者释放（如`OH_*Create`系列），也可能由系统管理（如`OH_*Get`系列）。混淆所有权会导致内存泄漏或 use-after-free
- **正确做法**：检查 .h 中函数文档的内存语义。需要释放的指针，在 N-API 封装中注册 `napi_finalize` 回调自动释放；不需要释放的，仅传递引用

### NEVER 为没有错误码定义的C API构造ERROR测试
- **原因**：C API通过返回值（int 错误码）或输出参数返回错误，如果 .h 中未定义错误码枚举或宏，构造错误码测试无规范依据
- **正确做法**：仅对 .h 中明确定义了错误码的 API 生成 ERROR 类型测试

## Thinking Framework: Before You Generate

在 Phase 5 生成任何 N-API 封装和测试代码之前，对每个目标 C API 问自己以下问题：

### C API 特性分析

| 问题 | 为什么重要 | 影响生成策略 |
|------|----------|-------------|
| **是否分配内存？** | 返回指针/缓冲区的 C API（如 `OH_*Create`、`*Alloc`）需要配对释放 | N-API 封装需要 `napi_finalize` 回调释放内存；测试需验证无泄漏 |
| **是否有输出参数？** | C API 常通过 `int*`、`char**` 等输出参数返回结果 | N-API 封装需要将输出参数转换为 JS 返回值；参数方向（in/out/inout）影响 `napi_get_value_*` / `napi_create_*` 选择 |
| **是否接受回调函数？** | 回调型 API（如 `OH_*SetCallback`）需要将 JS 函数转为 C 函数指针 | N-API 封装需要 `napi_create_threadsafe_function` 或全局引用保存回调 |
| **是否返回句柄/资源？** | 返回不透明句柄（如 `OH_*Handle`）的 API 需要生命周期管理 | N-API 封装使用 `napi_wrap` 将句柄绑定到 JS 对象；测试需验证创建-销毁配对 |
| **是否线程安全？** | 部分 C API 有调用线程限制 | N-API 封装可能需要 `napi_threadsafe_function` 跨线程调度 |
| **参数中是否有枚举值？** | 枚举参数在 N-API 层需要 `napi_get_value_int32` 后转换为 C 枚举类型 | ETS 测试传入 number，N-API 层做类型转换和边界检查 |
| **是否有依赖初始化？** | 部分 API 要求先调用 init/create 才能使用 | 测试需要 `beforeAll` 管理初始化/销毁；`afterAll` 清理资源 |

### N-API 封装决策树

```
C API 返回值类型是什么？
├── int（错误码）
│   ├── 有输出参数？ → N-API 返回输出参数转换后的 JS 值，错误码通过 napi_throw_error 抛出
│   └── 无输出参数？ → N-API 返回 undefined，错误码非零时 napi_throw_error
├── 指针（分配的内存/句柄）
│   ├── 需要调用者释放？ → napi_wrap + napi_finalize 自动释放
│   └── 不需要释放？ → napi_create_external 传递引用
├── 基本类型（int/float/bool）
│   └── 直接 napi_create_int32 / napi_create_double / napi_get_boolean
└── void
    └── N-API 返回 undefined

参数中是否有回调函数？
├── 是 → 需要回调的 API：
│        napi_create_function 或 napi_create_threadsafe_function
│        测试需验证回调触发、参数传递、异常回调
└── 否 → 标准参数转换（napi_get_value_*）
```

### 用例数量估算

| API 类型 | 建议用例数 | 覆盖维度 |
|----------|-----------|---------|
| 简单 get/set 属性 | 3-5 | 正常值 + 边界值 + 空指针 |
| 带输出参数的 API | 5-8 | 正常调用 + 输出参数验证 + 空指针 + 错误码 |
| 内存分配型 API（Create/Alloc） | 5-8 | 正常创建 + 销毁 + 重复销毁 + 内存泄漏检查 |
| 回调型 API | 5-8 | 正常回调 + 参数校验 + 多次注册 + 注销 |
| 句柄操作型 API | 5-8 | 正常操作 + 无效句柄 + 已销毁句柄 + 并发访问 |
| 系统能力 API | 8-12 | 各参数组合 + 错误码 + 边界值 + 并发/状态 |

### 测试价值优先级

在 Phase 4 设计阶段，按以下优先级决定 API 的测试深度：

| 优先级 | API 特征 | 测试策略 |
|--------|---------|---------|
| **P0 必测** | 内存管理 API（Create/Alloc/Destroy/Free） | 完整覆盖 + 内存泄漏检查 + 配对释放验证 |
| **P0 必测** | 句柄生命周期 API（Open/Close/Get/Release） | 完整覆盖 + 无效句柄测试 + 资源泄漏检查 |
| **P1 重点** | 有错误码定义的 API | 错码测试 + 参数无效场景 |
| **P1 重点** | 回调型 API | 回调触发 + 参数传递 + 异常回调 + 多次注册 |
| **P2 基础** | 简单数据读写 API | 正常值 + 边界值 |
| **跳过** | 无行为声明（纯类型定义、typedef、宏定义） | 不生成测试 |

**停止扩展信号** — 以下情况停止增加用例：
- 参数组合产生的用例不增加**行为覆盖**（只是换了个合法值）
- ERROR 用例的错误码在 .h 中未定义
- BOUNDARY 用例的边界值无文档依据

## Common Failure Patterns

### 编译失败：undefined reference
- **症状**：`undefined reference to 'OH_xxx'`
- **根因**：N-API 封装中使用了 .h 未声明的函数，或链接配置缺少依赖库
- **修复路径**：检查 NapiTest.cpp 中调用的 C 函数是否在 .h 中有声明 → 检查 CMakeLists.txt 是否添加了对应的 `-lxxx` 链接

### 编译失败：napi 函数未注册
- **症状**：ETS 侧调用 `testNapi.xxx()` 时运行时报 `is not a function`
- **根因**：`napi_property_descriptor` 中缺少该函数的注册，或函数名拼写不一致
- **修复路径**：运行 `scripts/verify_napi_triple.sh` → 检查 NapiTest.cpp 的 `Init` 函数中 descriptor 列表 → 与 index.d.ts 声明对比

### 编译失败：类型不匹配
- **症状**：C++ 编译报 `cannot convert from 'napi_value' to 'int'` 等
- **根因**：N-API 封装中参数类型转换错误（如用 `napi_get_value_string_utf8` 获取 int）
- **修复路径**：对照 .h 中的函数签名 → 检查 N-API 封装中每个参数的 `napi_get_value_*` 调用与 C 类型是否匹配

### 三重校验失败：C++ / d.ts / ETS 不一致
- **症状**：`verify_napi_triple.sh` 报告 mismatch
- **根因**：三层的函数名、参数数量、类型任一不匹配
- **修复路径**：运行 `scripts/auto_fix_napi_triple.sh` 自动修复 → 手动检查修复结果

### 测试运行时 crash
- **症状**：测试执行时 Native 层 crash（SIGSEGV/SIGABRT）
- **根因**：空指针解引用、use-after-free、N-API 封装中忘记处理 `napi_null` 输入
- **修复路径**：检查 N-API 封装中是否对所有指针参数做了 null 检查 → 检查 `napi_finalize` 是否正确释放了资源

### 创建新工程后编译失败
- **症状**：新工程无法编译，缺少 CMakeLists.txt、module.json5 等文件
- **根因**：未从模板复制完整工程结构，手动创建遗漏了关键文件
- **修复路径**：删除当前工程 → 从 `template_project/capi_test_template/` 完整复制 → 仅修改测试内容

## Generation Strategy

优先级：**补充已有工程 > 创建新工程**

1. 用户指定目标测试套 → 直接在该工程中补充用例
2. 分析后发现可添加到已有工程 → 在已有工程中补充用例
3. 用户未指定且无合适已有工程 → 创建新工程（必须先从 `template_project/capi_test_template/` 复制完整模板）
