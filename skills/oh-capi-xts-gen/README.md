# oh-capi-xts-gen

> **OpenHarmony CAPI XTS 测试用例生成模板**

专门为 OpenHarmony CAPI (Native C API) XTS 测试用例生成设计的模板，支持各子系统 C 语言 API 测试用例的自动化生成。

## ⭐ 核心特性

### CAPI 测试方式支持

OpenHarmony CAPI 支持两种测试方式，本技能专门用于生成方式2（N-API 封装测试）：

- **方式1**: Native C 测试（使用 gtest/HWTEST_F）- 不再使用
- **方式2**: N-API 封装测试（⭐ **新生成测试用例必需使用此方式**）

### 核心功能

- ✅ **头文件解析**：解析 `.h` 头文件，提取函数、参数、返回值、宏定义
- ✅ **智能测试生成**：根据 C 语言特性自动生成符合 XTS C 规范的测试用例
- ✅ **测试设计文档同步生成**：在生成测试用例的同时，同步生成结构化的测试设计文档
- ✅ **格式化和验证（强制）**：检查 C 代码规范，验证断言方法，确保测试用例质量
- ✅ **测试覆盖分析**：分析现有测试文件，识别已覆盖和未覆盖的 API
- ✅ **覆盖率报告驱动生成**：直接基于覆盖率报告中的缺失项生成测试用例（高效模式）
- ✅ **编译验证支持**：提供 Linux/Windows 环境下的编译指南
- ✅ **oh-package.json5 配置处理**：读取、修改和扩展项目配置文件

## 快速开始

## 前置配置

### OH_ROOT 路径配置（必需）

在使用本技能前，必须在技能目录下的 `.oh-capi-xts-config.json` 文件中配置 `OH_ROOT` 路径：

**配置文件位置**：`.opencode/skills/oh-capi-xts-gen/.oh-capi-xts-config.json`

**配置格式**：
```json
{
  "OH_ROOT": "/path/to/openharmony/root"
}
```

**配置说明**：
- `OH_ROOT`：OpenHarmony 工程根目录的绝对路径
- 该路径用于读取工程文件、API 头文件（`.h`）、测试文件等
- 必须确保路径存在且可访问
- 使用 `{OH_ROOT}` 占位符表示，实际使用时需替换为配置文件中定义的 OH_ROOT 值

**示例**：
```json
{
  "OH_ROOT": "/path/to/openharmony/root"
}
```

## 使用方式

### 三种使用方式

| 方式 | 适用场景 | 说明 |
|------|---------|------|
| **方式1：通用模板** | 新手、简单任务 | 最简单的使用方式，只需指定子系统和 API |
| **方式2：子系统配置** | 大多数任务（推荐） | 使用子系统默认配置，减少配置工作 |
| **方式3：自定义配置** | 高级用户、特殊需求 | 完全自定义配置，包括头文件路径、测试路径等 |

---

### 方式1：通用模板（推荐新手）

#### 基本用法

```
请使用 oh-capi-xts-gen 为以下 API 生成测试用例：

子系统: HiLog
API: HiLogPrint
```

#### 输出说明

系统将自动：
1. 解析头文件提取 API 信息
2. 扫描现有测试文件获取代码风格
3. 生成测试用例和测试设计文档
4. 注册测试套（如需要）
5. 格式化和验证
6. 提供编译指导

---

### 方式2：子系统配置（推荐）

#### 使用子系统默认配置

```
请使用 oh-capi-xts-gen 为以下 API 生成测试用例：

子系统: HiLog
模块: log
API: HiLogPrint
```

#### 指定多个 API

```
请使用 oh-capi-xts-gen 为以下 API 生成测试用例：

子系统: HiLog
模块: log
APIs:
  - HiLogPrint
  - HiLogPrintArgs
  - HiLogIsLoggable
```

---

### 方式3：自定义配置

#### 自定义头文件路径

```
请使用 oh-capi-xts-gen 生成测试用例，使用自定义配置：

子系统: CustomSubsystem
自定义配置:
  Kit包: @kit.CustomKit
  测试路径: test/xts/acts/custom/
  头文件: foundation/custom/interfaces/native/innerkits/include/custom.h

API: CustomAPI_Function()
```

#### 自定义测试规则

```
请使用 oh-capi-xts-gen 生成测试用例，使用自定义配置：

子系统: CustomSubsystem
自定义配置:
  测试路径: test/xts/acts/custom/
  头文件: foundation/custom/interfaces/native/innerkits/include/custom.h
  特殊规则:
    - 不测试内存泄漏
    - 仅测试正常情况

API: CustomAPI_Function()
```

---

## 覆盖率报告驱动模式（推荐）

### 使用覆盖率报告

```
请使用 oh-capi-xts-gen 生成测试用例，基于以下覆盖率报告：

子系统: HiLog
覆盖率报告:
  未覆盖的 API:
    - HiLogPrintArgs
    - HiLogIsLoggable
  缺失的参数组合:
    - HiLogPrint: (LOG_CORE, LOG_DEBUG, nullptr, "%s")
    - HiLogPrint: (LOG_CORE, LOG_INFO, "TEST_TAG", nullptr)
  缺失的测试场景:
    - HiLogPrint: 边界值测试
    - HiLogPrint: 超长字符串测试
```

### 覆盖率报告格式说明

覆盖率报告应包含：

1. **未覆盖的 API**：没有测试用例的 API 列表
2. **缺失的参数组合**：已覆盖 API 但缺少某些参数组合的测试
3. **缺失的测试场景**：已覆盖参数但缺少某些测试场景（边界值、错误码等）
4. **测试类型**：PARAM、ERROR、RETURN、BOUNDARY、MEMORY

### 覆盖率报告驱动模式优势

**优势**：
- **高效**：跳过覆盖率分析步骤，直接基于报告中的缺失项生成用例
- **精准**：严格按照覆盖率报告中列出的未覆盖 API、参数组合和场景生成测试
- **快速**：显著缩短生成时间，特别是对于大型 API 集合

---

## 高级用法

### 指定测试类型

```
请使用 oh-capi-xts-gen 生成以下类型的测试用例：

子系统: HiLog
API: HiLogPrint
测试类型:
  - PARAM
  - ERROR
  - BOUNDARY
```

### 指定测试用例数量

```
请使用 oh-capi-xts-gen 生成测试用例：

子系统: HiLog
API: HiLogPrint
测试数量: 10
```

### 修改现有测试

```
请使用 oh-capi-xts-gen 修改以下测试用例：

子系统: HiLog
测试文件: test/xts/acts/hilog/entry/src/main/src/test/HiLogPrintTest.cpp
修改内容:
  - 添加边界值测试
  - 修复错误码测试
```

---

## 测试设计文档生成

### 自动生成

每次生成测试用例时，系统会自动生成对应的测试设计文档。

文档位置：`[测试文件名].design.md`

### 文档内容

测试设计文档包含：
- 测试用例列表
- 测试用例详情（编号、名称、描述、类型、状态）
- 测试覆盖率统计
- 测试建议

---

## 编译验证

### Linux 环境

系统会自动：
1. 检测编译环境
2. 使用 `./test/xts/acts/build.sh` 编译
3. 监听编译进程
4. 自动修复语法错误
5. 重试编译

### Windows 环境

系统会提供：
1. DevEco Studio 编译指导
2. 命令行编译指导
3. 编译错误修复建议

---

## 输出说明

### 1. 测试用例文件

```
test/xts/acts/[子系统]/entry/src/main/src/test/[测试文件名].cpp
```

### 2. 测试设计文档

```
test/xts/acts/[子系统]/entry/src/main/src/test/[测试文件名].design.md
```

### 3. 更新文件列表

```
更新的文件：
- [测试文件名].cpp
- [测试文件名].design.md
- List.test.ets（如需要）
```

### 4. 覆盖率对比

```
覆盖率对比：
- 已覆盖 API: [数量]
- 未覆盖 API: [数量]
- 覆盖率: [百分比]%
```

---

## 常见问题

### Q1: 如何指定测试路径？

**A**: 在自定义配置中指定：

```
自定义配置:
  测试路径: test/xts/acts/custom/
```

### Q2: 如何指定头文件路径？

**A**: 在自定义配置中指定：

```
自定义配置:
  头文件: foundation/custom/interfaces/native/innerkits/include/custom.h
```

### Q3: 如何生成特定类型的测试？

**A**: 指定测试类型：

```
测试类型:
  - PARAM
  - ERROR
  - BOUNDARY
```

### Q4: 如何使用覆盖率报告？

**A**: 提供覆盖率报告，系统会自动切换到覆盖率报告驱动模式：

```
覆盖率报告:
  未覆盖的 API: [...]
  缺失的参数组合: [...]
  缺失的测试场景: [...]
```

### Q5: 如何修改已生成的测试用例？

**A**: 提供测试文件路径和修改内容：

```
修改现有测试：
测试文件: [...]
修改内容: [...]
```

---

## 最佳实践

### 1. 使用覆盖率报告驱动模式

如果已有覆盖率报告，直接提供报告内容，效率和精准度最高。

### 2. 先生成后修改

先生成基础测试用例，然后根据需求进行修改。

### 3. 充分利用子系统配置

对于常见子系统，使用子系统配置可以减少配置工作。

### 4. 重视测试设计文档

测试设计文档有助于理解测试用例的设计思路和覆盖率情况。

### 5. 及时编译验证

生成测试用例后，及时编译验证，发现和修复问题。

## 文档

### 详细文档

### 子模块文档

- **[conventions](modules/conventions/)** - 框架层（核心框架和测试规范）
- **[L1_Analysis](modules/L1_Analysis/)** - 分析层（API 解析和覆盖率分析）
- **[L2_Generation](modules/L2_Generation/)** - 生成层（测试用例生成）
- **[L3_Validation](modules/L3_Validation/)** - 构建层（编译验证支持）

### L2_Generation 子模块详细内容

- **[test_generation_c.md](modules/L2_Generation/generator/test_generation_c.md)** - 测试生成核心文档
- **[test_patterns_napi_ets.md](modules/L2_Generation/generator/test_patterns_napi_ets.md)** - N-API 封装和 ETS 测试公共模式
- **[test_patterns_napi_ets_advance.md](modules/L2_Generation/generator/test_patterns_napi_ets_advance.md)** - N-API 高级模式（回调/异步/句柄）
- **[napi_api_reference.md](modules/L2_Generation/generator/napi_api_reference.md)** - N-API 常用 API 参考
- **[project_config_templates.md](modules/L2_Generation/generator/project_config_templates.md)** - 工程配置模板
- **[verification_common.md](modules/L2_Generation/generator/verification_common.md)** - 三重校验和编译前工程结构校验
- **[test_suite_structure_checklist.md](modules/L2_Generation/generator/test_suite_structure_checklist.md)** - 测试套结构检查清单

## 目录结构

```
oh-capi-xts-gen/
├── SKILL.md                        # 技能主文件
├── README.md                       # 技能说明（本文件）
├── skill_config.json               # 技能详细配置
├── .oh-capi-xts-config.json        # OH_ROOT 配置文件
├── docs/                          # 文档
│   ├── DESIGN_DOC_GUIDE.md         # 设计文档指南
│   └── C_API_COMMON_TESTING_RULES.md # C API 测试规则
├── modules/                       # 子模块
│   ├── conventions/              # 框架层
│   │   └── hypium_framework_c.md  # C语言测试框架
│   ├── L1_Analysis/               # 分析层
│   │   ├── parser/
│   │   │   ├── unified_api_parser_c.md  # API 解析器
│   │   │   ├── project_parser.md        # 工程配置解析器
│   │   │   └── doc_reader.md            # 文档读取器
│   │   └── analyzer/
│   │       └── coverage_analyzer.md     # 测试覆盖分析器
│   ├── L2_Generation/             # 生成层
│   │   └── generator/
│   │       ├── test_generation_c.md          # 测试生成核心
│   │       ├── test_patterns_napi_ets.md      # N-API/ETS 公共模式
│   │       ├── test_patterns_napi_ets_advance.md # N-API 高级模式
│   │       ├── napi_api_reference.md          # N-API 参考
│   │       ├── project_config_templates.md    # 工程配置模板
│   │       ├── verification_common.md         # 三重校验
│   │       └── test_suite_structure_checklist.md # 测试套结构检查
│   └── L3_Validation/             # 构建层
│       └── builder/
│           ├── build_workflow_c.md           # 跨平台编译工作流
│           ├── linux_compile_workflow_c.md   # Linux 编译流程
│           ├── linux_compile_env_setup_c.md  # Linux 编译环境配置
│           └── quick_reference_extract_suite_name.md # 测试套名称提取
├── scripts/                       # 自动化脚本
│   ├── verify_napi_triple.sh      # N-API 三重校验脚本
│   ├── check_test_suite_structure.sh # 测试套结构检查脚本
│   ├── async_build.sh             # 异步编译脚本
│   ├── async_build_manager.py     # 异步编译管理器
│   └── cleanup_group.sh           # 清理工具
├── examples/                      # 子系统示例
├── template_project/              # 测试套工程模板
│   └── capi_test_template/        # 完整的 OpenHarmony CAPI 测试工程模板
└── references/                    # 参考资料
    └── subsystems/                # 子系统配置
        ├── _common.md             # 通用配置
        ├── hilog/                 # HiLog 子系统配置
        ├── multimedia/            # Multimedia 子系统配置
        │   └── camera/            # Camera 模块配置
        ├── bundlemanager/         # BundleManager 子系统配置
        │   └── zlib/              # Zlib 模块配置
        └── ability/               # Ability 子系统配置
```

## 重要说明

### ⭐ 强制要求：N-API 封装测试

**新生成测试用例必须使用方式2：N-API 封装测试**

本技能专门用于生成方式2（N-API 封装测试）的测试用例：
- ✅ 将 C 函数封装为 N-API 接口
- ✅ 使用 `napi_value` 和 `napi_env` 参数
- ✅ 返回 `napi_value` 类型供 ETS/ArkTS 调用
- ❌ 不生成直接调用 C 函数的测试（方式1）

### 支持的 CAPI 测试套

本技能支持以下 CAPI 测试套作为参考：

#### ArkUI CAPI 测试套
- **路径**: `{OH_ROOT}/test/xts/acts/arkui/ace_c_arkui_test_api20`
- **类型**: 完整的 CAPI 测试套
- **特点**: 包含多个动态库（libnativefunc.so、libnativerender.so）的 N-API 封装测试

#### BundleManager CAPI 测试套
- **路径**: `{OH_ROOT}/test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsbmsgetabilityresourcendkenterprisetest`
- **类型**: 完整的 CAPI 测试套
- **特点**: 使用 libentry.so 进行 N-API 封装测试

### 模块化架构

本技能采用**四层模块化架构**，根据任务需求动态加载相应模块：

| 任务类型 | 必需模块 | 说明 |
|---------|---------|------|
| **基础测试生成** | conventions + L2_Generation | 直接加载框架和生成模块 |
| **覆盖率报告驱动** | conventions + L2_Generation | 跳过分析层，直接生成用例 |
| **标准流程（有覆盖率分析）** | conventions + L1_Analysis + L2_Generation | 完整流程，包含覆盖率分析 |
| **编译验证** | conventions + L3_Validation | 加载构建模块进行编译验证 |
| **格式化和验证** | conventions + L2_Generation | 使用生成模块的规范进行验证 |

## 版本信息

- **版本**: 1.0.0
- **创建日期**: 2026-03-06
- **更新日期**: 2026-03-10
- **兼容性**: OpenHarmony API 10+

---

## 许可证

本技能基于 Apache License 2.0 许可证开源。
