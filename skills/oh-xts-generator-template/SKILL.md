---
name: xts-generator
description: OpenHarmony XTS 测试用例通用生成模板。支持各子系统测试用例生成，API 定义解析，测试覆盖率分析，代码规范检查。触发关键词：XTS、测试生成、用例生成、测试用例。
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# xts-generator

> **OpenHarmony XTS 测试用例通用生成模板**

## 技能概述

xts-generator 是一个通用的 OpenHarmony XTS 测试用例生成模板，设计为**可配置、可扩展**的通用框架，适用于各个子系统的测试用例生成。

### 核心特性

1. **通用测试生成流程** - 提供完整的测试用例生成工作流
2. **模块化架构** - 四层模块化设计（L1/L2/L3/L4），按需加载
3. **分层配置系统** - 通用配置 + 子系统特有配置
4. **灵活扩展机制** - 支持各子系统添加特有配置和模板

### 核心功能

| 功能 | 说明 |
|------|------|
| **API定义解析** | 解析 `.d.ts` 文件，提取接口、方法、参数、返回值、错误码 |
| **测试覆盖分析** | 分析现有测试文件，识别已覆盖和未覆盖的API |
| **智能测试生成** | 根据测试策略自动生成符合 XTS 规范的测试用例 |
| **测试设计文档生成** | 同时生成结构化的测试设计文档，包含测试用例说明、预期结果等 |
| **ArkTS 静态语言语法规范校验** | 校验 ArkTS 静态语言语法规范，包括类型注解、字段初始化、语法兼容性等 |
| **代码规范检查** | 确保生成的代码符合 XTS 测试规范 |
| **编译问题解决** | subagent 执行编译，自动修复语法错误，监听编译完成状态 |

## 适用场景

- ✅ 为新 API 生成完整的测试套件
- ✅ 同时生成测试用例和测试设计文档
- ✅ 分析现有测试的覆盖情况
- ✅ 补充缺失的测试用例和测试设计
- ✅ 验证测试代码规范性
- ✅ 各子系统定制化测试生成

## 快速开始

### 方式1：使用通用模板（推荐新手）

```
请使用 xts-generator 为以下 API 生成测试用例：

子系统: ArkUI
API: Component.onClick()
定义文件: interface/sdk-js/api/@ohos.arkui.d.ts
```

### 方式2：使用子系统配置（推荐）

```
请使用 xts-generator 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
```

### 方式3：自定义配置

```
请使用 xts-generator 生成测试用例，使用自定义配置：

子系统: MySubsystem
自定义配置:
  Kit包: @kit.MyKit
  测试路径: test/xts/acts/mysubsystem/
  API声明: interface/sdk-js/api/@ohos.mysubsystem.d.ts

API: myAPI.method()
```

## 核心工作流程

```
1. 确定子系统配置
    ├─ 检查是否存在子系统配置文件
    ├─ 加载通用配置 (_common.md)
    └─ 加载子系统配置 ({Subsystem}/_common.md)

2. 解析 API 定义 (.d.ts + 文档)
    ├─ 读取 API 声明文件 (.d.ts)
    ├─ 查找并解析 API 文档
    └─ 综合分析

3. 参考已有用例（强制）
    ├─ 扫描指定路径的已有测试文件
    ├─ 分析代码风格和规范
    └─ 提取共性模式

4. 分析现有测试（可选）
    ├─ 扫描测试文件
    ├─ 识别已覆盖的API
    └─ 计算测试覆盖率

5. 生成测试用例
    ├─ 应用子系统特有规则
    ├─ 使用子系统特有模板
    └─ 应用已有用例的代码风格

6. 同步生成测试设计文档（强制）
    ├─ 为每个测试用例生成详细设计说明
    ├─ 包含测试场景、测试步骤、预期结果
    ├─ 生成结构化 Markdown 文档
    └─ 与测试用例文件对应命名

7. 添加 @tc 注释块（强制）
    ├─ @tc.name：小驼峰命名，与 it() 参数一致
    ├─ @tc.number：{describe名}_{序号}
    ├─ @tc.desc：{API名} {错误码/场景} test.
    └─ 验证字段值与 it() 参数的一致性

8. 格式化和验证
    ├─ 应用代码模板
    ├─ 检查语法规范
    │   ├─ 8.1 动态语法检查（生成动态 XTS 用例时）
    │   │   └─ 参考规范文档：`references/ArkTS_Dynamic_Syntax_Rules.md`
    │   └─ 8.2 静态语法检查（生成静态 XTS 用例时）   
    │       ├─ 参考规范文档：`references/arkts-static-spec/`
    │       └─ 检查点：
    |           ├─ 类型注解完整性（禁止 any/unknown）
    |           ├─ 字段初始化（所有字段必须初始化）
    |           ├─ 语法兼容性（禁止 var、禁止对象解构等）
    |           ├─ 类型转换规则（显式转换 vs 隐式转换）
    |           └─ 静态语言特性（对象布局固定、null 安全等）
    ├─ 验证断言方法
    └─ 输出校验结果和修改建议

9. 注册测试套（新增文件时必须）
    ├─ 查找 List.test.ets 文件
    ├─ 添加 import 语句
    └─ 在 testsuite() 函数中调用

10. 编译验证（重要）
    ├─ 检测运行环境（Linux/Windows）
    ├─ 根据环境选择编译方案
    ├─ **Linux 环境编译流程**：
    │   ├─ **预置条件检查（静态测试套编译必需）**：
    │   │   ├─ 检测是否为静态测试套编译
    │   │   ├─ 校验 hvigor 工具版本：
    │   │   │   ├─ 读取版本：`cat ./prebuilts/command-line-tools/hvigor/hvigor/package.json | grep '"version"'`
    │   │   │   ├─ 判断版本：是否为 `"6.0.0-arkts1.2-ohosTest-25072102"`
    │   │   │   └─ 决策：
    │   │   │       ├─ 是静态工具版本 → 跳过清理替换
    │   │   │       └─ 非静态工具版本 → 执行清理替换
    │   │   └─ 如需替换 hvigor 工具：
    │   │       ├─ 说明：prebuilts 中默认配置的是编译动态测试套的编译工具
    │   │       ├─ 清理 SDK 缓存：`rm -rf ./prebuilts/ohos-sdk/linux`
    │   │       ├─ 清理旧工具：`rm -rf ./prebuilts/command-line-tools`
    │   │       ├─ 下载新工具：`git clone https://gitee.com/laoji-fuli/hvigor0702.git -b debug2 command-line-tools`
    │   │       └─ 移动到预置目录：`mv -f command-line-tools ./prebuilts/`
    │   ├─ 使用 general subagent 执行编译任务（避免主流程中断）
    │   ├─ 监听编译进程直至完成（防止编译异常中断）
    │   ├─ 编译成功：输出编译结果
    │   └─ 编译失败：自动修复语法错误并重试
    │       ├─ 分析编译错误日志
    │       ├─ 识别语法问题并修复
    │       └─ 重新触发编译
    └─ **工程配置问题处理**：
        ├─ 检测到工程配置问题时暂停
        ├─ 向用户确认是否需要修改
        └─ 用户确认后才执行配置修改

11. 输出更新文件列表、测试设计文档和覆盖率对比

> 📖 **详细的工作流程说明请查看**: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)

## 配置扩展

### 配置优先级

```
用户自定义配置 > 子系统配置 > 通用配置
```

### 配置文件组织

```
references/subsystems/
├── _common.md           # 全局通用配置
├── {Subsystem}/        # 子系统文件夹
│   ├── _common.md       # 子系统通用配置
│   └── {Module}.md      # 模块配置
```

> 📖 **详细的配置说明请查看**: [docs/CONFIG.md](./docs/.md)

## 输出规范

### 测试用例编号(`@tc.number`)

```
格式: SUB_[子系统]_[模块]_[API]_[类型]_[序号]

类型标识：
- PARAM    参数测试
- ERROR    错误码测试
- RETURN   返回值测试
- BOUNDARY 边界值测试
```

### 测试设计文档规范（强制）

**文件命名规则**：
```
格式: {测试文件名}.design.md
示例: Component.onClick.test.ets -> Component.onClick.test.design.md
```

**文档模板和生成规则**：
- 标准版模板：`modules/L3_Generation/design_doc_generator.md`
- 简化版模板：`modules/L3_Generation/design_doc_templates.md`


### 测试设计文档生成规则

**1. 同步生成原则**
- 生成每个测试用例时，必须同步生成对应的测试设计文档
- 测试设计文档与测试用例一一对应
- 文档内容必须与测试用例实现保持一致

**2. 文档内容完整性**
- 必须包含所有测试场景的详细说明
- 必须包含测试步骤和预期结果
- 必须说明测试环境和前置条件
- 必须记录变更历史

**3. 文档格式规范性**
- 使用 Markdown 格式
- 遵循统一的模板结构
- 使用表格组织关键信息
- 保持版本信息更新

**4. 文档更新机制**
- 测试用例修改时，必须同步更新测试设计文档
- 文档版本号必须递增
- 变更内容必须记录在变更记录中

### 任务完成输出

每次完成任务后，**必须**输出：

```markdown
## 任务完成摘要

### 新增测试文件
- `path/to/file1.test.ets` - 文件说明

### 新增测试设计文档
- `path/to/file1.test.design.md` - 设计文档说明

### 修改文件
- `path/to/file2.ets` - 修改说明

### 测试覆盖统计
- 新增测试用例数：XX 个
- 新增测试设计文档：XX 个
- 覆盖的 API：XX 个
```

> 📖 **完整的使用方式请查看**: [docs/USAGE.md](./docs/USAGE.md)

## 重要注意事项

### 1. @tc 注释块规范（强制）

- 所有测试用例（`it()` 函数）**必须**在前面添加标准的 `@tc` 注释块
- `@tc.name`：必须使用小驼峰命名（camelCase），必须与 `it()` 第一个参数完全一致
  - 详见：[references/subsystems/_common.md](./references/subsystems/_common.md) 命名规范
- `@tc.number`：格式为 `{describe名}_{序号}`，序号从001开始补零对齐
- `@tc.desc`：格式为 `{API名} {错误码/场景} test.`，必须以 `. ` 结尾
- `@tc.type`、`@tc.size`、`@tc.level`：必须与 `it()` 第二个参数中的值一致

### 2. hypium 导入规范（强制）

- 基本导入：`describe, it, expect`（必需）
- 类型导入：`TestType, Level, Size`（必需）
- 条件导入：`beforeAll, afterAll`（根据代码需要）
- 自动检测并补充缺失的导入

### 3. 工程文件修改限制（强制）

- **严格禁止修改**工程目录中的配置文件
- **仅允许修改**：`entry/src/ohosTest/ets/test/` 目录中的测试文件
- **违反限制的后果**：可能导致工程结构被破坏、编译失败

### 3.1 清理操作安全注意事项（强制）

**⚠️ 关键警告**：预编译清理操作必须谨慎执行，避免误删系统编译环境。

**安全清理要求**：
1. **确认当前目录**：执行清理命令前必须确认当前工作目录
   ```bash
   cd {OH_ROOT}/test/xts/acts/testfwk/{test_suite}
   pwd  # 必须确认当前目录
   ```

2. **使用显式路径删除**：删除命令必须使用显式路径（`./` 前缀或绝对路径）
   ```bash
   # ✅ 正确：使用显式相对路径
   rm -rf ./.hvigor ./build ./entry/build ./oh_modules
   rm -f ./oh-package-lock.json5 ./local.properties

   # ❌ 错误：不使用路径前缀（可能误删 OH_ROOT/build）
   rm -rf build
   ```

3. **分步清理验证**：
   - 步骤1：清理测试套缓存并验证
   - 步骤2：清理 OH_ROOT/out 目录
   - 步骤3：验证 OH_ROOT/build 目录安全

4. **禁止操作**：
   - ❌ 在 OH_ROOT 目录执行 `rm -rf build`
   - ❌ 一次性清理多个目录
   - ❌ 不验证当前目录就执行删除

**参考文档**：`modules/L4_Build/linux_prebuild_cleanup.md` 1.3 节

### 4. XTS Wiki 文档参考（强制）

- 生成 XTS 测试用例时，**必须**参考 Wiki 文档中的规范
- Wiki 文档规范 > Template 配置 > 通用模板

### 5. ArkTS 语法类型识别（重要）

- **API 类型判断**：必须读取 `.d.ts` 文件中**最后一段 JSDOC** 的 `@since` 标签
- **工程类型识别**：读取 `build-profile.json5` 检查 `arkTSVersion` 字段
- **兼容性检查**：生成测试用例前，必须检查工程语法类型与 API 类型是否匹配

### 6. ArkTS 静态语言语法规范校验（新增，可选）

**触发条件**：当用户明确要求生成 arkts 静态用例、arkts-static 等静态相关内容时，自动进行语法规范校验

**校验内容**：
1. **类型注解完整性**
   - 禁止使用 `any` 和 `unknown` 类型
   - 所有参数必须显式声明类型

2. **字段初始化**
   - 所有字段必须初始化
   - 构造函数中必须初始化所有字段

3. **语法兼容性**
   - 禁止使用 `var` 声明变量
   - 禁止对象解构
   - 禁止可选链操作符

4. **类型转换规则**
   - 优先使用显式类型转换
   - 严格区分显式转换与隐式转换

5. **静态语言特性**
   - 对象布局固定
   - null 安全机制
   - 类型守卫

**校验输出**：
- 提供详细的校验结果
- 给出具体的修改建议
- 标注不符合规范的代码位置

**规范文档**：
- 规范文档路径：`/mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/references/arkts-static-spec/`
- 包含 16 个 ArkTS 语言规范文件（spec/ 目录）
- 包含 3 个 TypeScript 迁移指南文件（cookbook/ 目录）
- 校验时必须严格按照该目录下的文档内容进行
### 7. 编译环境检测（强制）


#### 7.1.1 Linux 环境编译

- **Linux 环境**：必须使用 `build.sh` 脚本编译，**不要使用 `hvigorw`**

- **环境检测方法**：`uname -s`（Linux）或 `$env:OS`（Windows）

#### 7.1.2 **Linux 编译流程要求**：
- **预编译清理**：**无论是动态还是静态测试套，每次编译前都必须执行预编译清理**
  - 清理目的：确保编译结果包含所有最新代码
  - 清理步骤：参考 `modules/L4_Build/linux_prebuild_cleanup.md`
  - 使用统一的 `cleanup_group.sh` 脚本
  - **⚠️ 安全注意事项**：
     * 必须确认当前目录再执行清理
     * 必须使用显式路径删除（`./` 前缀）
     * 禁止在 OH_ROOT 目录执行 `rm -rf build`
     * 详见注意事项第 3.1 节
- **subagent 执行**：必须使用 general subagent 执行编译任务，避免主流程中断
- **监听机制**：必须监听编译进程直至完成，确保编译状态正确返回
- **错误处理**：
  - **语法错误**：自动分析错误日志，修复语法问题并重试编译
  - **配置错误**：检测到工程配置问题时，暂停编译，向用户确认后才修改
- **编译结果**：必须输出详细的编译结果和错误信息

#### 7.1.3 **静态测试套编译预置条件**：
- **编译前版本校验**（每次编译静态测试套时）：
  - 读取 hvigor 工具版本：`cat ./prebuilts/command-line-tools/hvigor/hvigor/package.json | grep '"version"'`
  - 静态工具版本标识：`"6.0.0-arkts1.2-ohosTest-25072102"`
  - 决策逻辑：
    - 版本匹配 → 跳过工具替换
    - 版本不匹配 → 执行工具替换流程
- **如需替换 hvigor 工具**：
  - 清理 SDK 缓存：`rm -rf ./prebuilts/ohos-sdk/linux`
  - 清理旧工具：`rm -rf ./prebuilts/command-line-tools`
  - 下载静态编译工具：`git clone https://gitee.com/laoji-fuli/hvigor0702.git -b debug2 command-line-tools`
  - 移动到预置目录：`mv -f command-line-tools ./prebuilts/`
  - 执行位置：必须在 `{OH_ROOT}` 目录下执行上述命令
- **预编译清理**（每次编译前强制执行）：
  - **⚠️ 重要**：无论版本是否匹配，都必须在编译前执行预编译清理
  - 清理目的：确保编译结果包含所有最新代码
  - 参考文档：`modules/L4_Build/linux_prebuild_cleanup.md`


#### 7.2 Windows 环境编译

Windows 环境支持两种编译模式，根据用户需求自动选择：

##### 7.2.1 ArkTS 动态 XTS 编译模式（默认）

- **适用场景**：标准的 ArkTS 动态语法 XTS 测试工程
- **编译方式**：DevEco Studio IDE 或 `hvigorw.bat`
- **编译目标**：`Build → Build OhosTest Hap(s)`
- **参考文档**：`modules/L4_Build/build_workflow_windows.md` 第三章

##### 7.2.2 ArkTS 静态 XTS 编译模式（arkts-sta）

- **适用场景**：基于 ArkTS 静态强类型语法的 XTS 测试工程
- **触发关键词**：当用户提到以下关键词时自动启用：
  - "arkts-sta"
  - "arkts静态"
  - "ArkTS静态"
  - "静态xts"
  - "静态 XTS"
  - "静态ArkTS"
  - "静态 ArkTS"
  - "arkts static"
  - "ArkTS static"
  - "static arkts"
  - "static xts"
  - "编译静态"
  - "静态编译"
  - "静态工程编译"
  - "编译arkts-sta"
  - "编译arkts静态"
  - "Windows静态编译"
  - "Windows arkts静态"
- **编译方式**：PowerShell 脚本或 `hvigorw.bat` 命令行工具
- **Java 环境**：**必需**配置 JAVA_HOME 环境变量
- **编译特点**：
  - 严格的静态类型检查
  - 所有类型必须有显式注解
  - 禁止使用 any 类型
  - 所有字段必须初始化
- **参考文档**：`modules/L4_Build/build_workflow_windows.md` 第十章

> **⚠️ 重要提示**：
> - 默认使用动态编译模式
> - 仅在用户明确提到静态相关关键词时启用静态编译模式
> - 静态编译需要配置 Java 环境变量（JAVA_HOME）

**编译模块化架构**（v2.2.0+）：
**Linux 编译**：
- **主工作流**：`modules/L4_Build/build_workflow_linux.md`（主入口，按需加载）
- **动态测试套编译**：`modules/L4_Build/linux_compile_dynamic_suite.md`（按需加载）
- **静态测试套编译**：`modules/L4_Build/linux_compile_static_suite.md`（按需加载）
- **环境准备**：`modules/L4_Build/linux_compile_env_setup.md`（按需加载）
- **预编译清理**：`modules/L4_Build/linux_prebuild_cleanup.md`（按需加载）
- **BUILD.gn 配置**：`modules/L4_Build/build_gn_config.md`（按需加载）
- **问题排查**：`modules/L4_Build/linux_compile_troubleshooting.md`（按需加载）

**Windows 编译**：
- **Windows 动态编译**：`modules/L4_Build/build_workflow_windows.md` 第三章
- **Windows 静态编译**：`modules/L4_Build/build_workflow_windows.md` 第十章

> 📖 **完整的注意事项请查看**: `references/subsystems/_common.md` 第七章和第八章

## 故障排除

> 📖 **详细故障排除指南**: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

**常见问题**：
- Q1: 生成的测试用例无法编译
- Q2: 测试用例命名不符合规范
- Q3: 测试设计文档与测试用例不一致
- Q4: Linux 环境编译失败
- Q5: 测试用例执行失败
- Q6: 子系统配置文件未找到
- Q7: 测试覆盖率分析不准确

> ⚠️ **静态语法检查参考文档**：在进行 ArkTS 静态语言语法规范校验时，请严格参考 `/mnt/data/c00810129/.opencode/skills/oh-xts-generator-template/references/arkts-static-spec` 目录下的规范文档。

## 版本信息

- **当前版本**: 1.20.0
- **创建日期**: 2025-01-31
- **最后更新**: 2026-02-11
- **兼容性**: OpenHarmony API 10+
- **基于**: OH_XTS_GENERATOR v1.7.0

## 版本历史

- **v1.20.0** (2026-02-11): **强化清理操作安全注意事项**
  - **重要更新**：添加清理操作的安全注意事项，避免误删系统编译环境
  - **子模块更新**：
    * `linux_prebuild_cleanup.md` 版本升级至 v2.1.0
      - 新增 1.3 节：清理操作安全注意事项
      - 强调使用显式路径删除（`./` 前缀或绝对路径）
      - 强制要求分步清理，每步验证
      - 更新单个测试套清理为5步严格流程
  - **核心警告**：
     * 禁止在 OH_ROOT 目录执行 `rm -rf build`
     * 删除命令必须使用显式路径
     * 清理后必须验证系统目录完整性
  - **优化效果**：
     * 避免误删系统编译环境（build 目录）
     * 提高清理操作的安全性
     * 降低人为错误风险
  - 版本号升级至 1.20.0

- **v1.19.0** (2026-02-11): **强化预编译清理的强制执行**
  - **重要更新**：无论是动态还是静态测试套，编译前都必须执行预编译清理
  - **核心目的**：确保编译结果包含所有最新代码
  - **子模块更新**：
    * `linux_compile_dynamic_suite.md` 版本升级至 v1.2.0
      - 强化预编译清理的强制性要求
      - 在快速参考和完整示例中添加重要提示
    * `linux_compile_static_suite.md` 版本升级至 v1.4.0
      - 将清理步骤从"按需执行"改为"强制执行"
      - 更新工作流程图，强调清理的必要性
      - 在快速参考和完整示例中添加重要提示
  - **注意事项影响**：不影响其他注意事项的内容
  - **优化效果**：
    * 避免缓存导致编译结果不包含最新代码的问题
    * 提高编译结果的可靠性
    * 统一动态和静态测试套的编译前清理要求
  - 版本号升级至 1.19.0

- **v1.18.0** (2026-02-11):
  - **重要更新**：添加 hvigor 工具版本校验机制
  - **核心工作流程更新**：
    * 更新第10步"编译验证"
    * 优化"预置条件检查"子步骤（静态测试套编译必需）
    * 新增 hvigor 工具版本校验流程
    * 添加版本判断逻辑：`"6.0.0-arkts1.2-ohosTest-25072102"`
    * 优化决策流程：版本匹配则跳过替换，不匹配则执行替换
  - **注意事项更新**：
    * 更新第6条"编译环境检测"内容
    * 更新"静态测试套编译预置条件"小节
    * 明确编译前版本校验的必要性
    * 提供版本读取命令和判断逻辑
    * 说明版本匹配时的处理方式（跳过替换）
  - **优化效果**：
    * 避免不必要的工具替换操作
    - 提高编译流程效率
    - 减少网络请求和磁盘操作
  - 版本号升级至 1.18.0

- **v1.17.0** (2026-02-11):
  - **重要更新**：添加静态测试套编译 hvigor 工具替换流程
  - **核心工作流程更新**：
    * 更新第10步"编译验证"
    * 新增"预置条件检查"子步骤（静态测试套首次编译必需）
    * 添加清理 SDK 缓存命令
    * 添加替换 hvigor 工具流程（清理、下载、移动）
    * 说明 hvigor 工具替换的原因（动态 vs 静态编译工具）
  - **注意事项更新**：
    * 更新第6条"编译环境检测"内容
    * 新增"静态测试套编译预置条件"小节
    * 明确首次编译前必须执行的操作
    * 提供完整的命令序列
    * 说明执行位置和后续编译规则
  - 版本号升级至 1.17.0

- **v1.16.0** (2026-02-11):
  - **重要更新**：Linux 编译流程优化和错误处理机制增强
  - **编译流程更新**：
    * 更新核心工作流程第10步"编译验证"
    * 新增 Linux 环境 subagent 执行机制（避免主流程中断）
    * 新增编译监听机制（确保编译完成）
    * 新增自动语法错误修复功能
    * 新增工程配置问题确认机制
  - **注意事项更新**：
    * 更新第6条"编译环境检测"内容
    * 明确 subagent 执行要求
    * 明确错误处理策略
  * 版本号升级至 1.16.0

- **v1.15.0** (2026-02-10):
  - **重要更新**：语法规范检查步骤拆分和版本升级
  - **工作流程更新**：将第8步"格式化和验证"拆分为两个子步骤
  - **更新范围**：
    * 更新核心工作流程第8步内容
    * 新增第8.1 步骤：动态语法检查（生成动态 XTS 用例时）
      - 参考规范文档：`references/ArkTS_Dynamic_Syntax_Rules.md`
    * 新增第8.2 步骤：静态语法检查（生成静态 XTS 用例时）
      - 参考规范文档：`references/arkts-static-spec/`
    * 版本号升级至 1.15.0

- **v1.14.0** (2026-02-10):
  - **重要更新**：调整工作流程结构，将"格式化和验证"与"注册测试套"合并为新的"格式化和验证"步骤
  - **更新范围**：
    * 更新核心工作流程第8步内容
    * 更新第9步和第10步的序号（将原第9步改为第8步，原第10步改为第9步）
    * 更新注意事项第6条，明确规范文档的完整路径
    * 版本号升级至 1.14.0

## 参考文档

### 详细文档

- **模块化架构详解**: [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- **配置扩展机制**: [docs/CONFIG.md](./docs/CONFIG.md)
- **使用方式详解**: [docs/USAGE.md](./docs/USAGE.md)
- **故障排除**: [docs/TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)

### 子模块文档

- **L1_Framework**: [modules/L1_Framework/](./modules/L1_Framework/)
- **L2_Analysis**: [modules/L2_Analysis/](./modules/L2_Analysis/)
- **L3_Generation**: [modules/L3_Generation/](./modules/L3_Generation/)
- **L4_Build**: [modules/L4_Build/](./modules/L4_Build/)

### 通用配置

- **通用配置**: [references/subsystems/_common.md](./references/subsystems/_common.md)

