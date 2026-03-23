---
name: oh-xts-generator-template
description: OpenHarmony XTS 测试用例通用生成模板。支持各子系统测试用例生成，API 定义解析，测试覆盖率分析，代码规范检查。触发关键词：XTS、测试生成、用例生成、测试用例。
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# oh-xts-generator-template

> **OpenHarmony XTS 测试用例通用生成模板**

## 技能概述

oh-xts-generator-template 是一个通用的 OpenHarmony XTS 测试用例生成模板，采用四层模块化架构，支持各子系统定制化配置。

### 核心功能
- **API 定义解析**：解析 `.d.ts` 文件，提取接口、方法、参数、返回值
- **API 语法类型过滤和验证**：根据任务类型（动态/静态）过滤 API，验证测试用例使用的 API 是否支持目标语法类型
- **智能测试生成**：根据测试策略自动生成符合 XTS 规范的测试用例
- **测试设计文档同步生成**：在生成测试用例的同时，同步生成结构化的测试设计文档
- **⚠️ 格式化和验证（强制）**：检查语法规范，验证断言方法，确保测试用例质量
- **测试覆盖分析**：分析现有测试文件，识别已覆盖和未覆盖的API
- **覆盖率报告驱动生成**：直接基于覆盖率报告中的缺失项生成测试用例（高效模式）
- **编译验证支持**：提供 Linux/Windows 环境下的编译指南

### 适用场景
- 为新 API 生成完整的测试套件
- 分析现有测试的覆盖情况
- 各子系统定制化测试生成
- **基于覆盖率报告补充缺失测试**（推荐 - 高效精准）

## 前置配置

### OH_ROOT 路径配置（必需）

在使用本技能前，必须在技能目录下的 `.oh-xts-config.json` 文件中配置 `OH_ROOT` 路径：

**配置文件位置**：`.opencode/skills/oh-xts-generator-template/.oh-xts-config.json`

**配置格式**：
```json
{
  "OH_ROOT": "/path/to/openharmony/root"
}
```

**配置说明**：
- `OH_ROOT`：OpenHarmony 工程根目录的绝对路径
- 该路径用于读取工程文件、API 声明文件（`.d.ts`）、测试文件等
- 必须确保路径存在且可访问

⚠️ **重要**：使用技能前务必检查该配置是否正确设置，否则技能将无法正常工作。

## 快速开始

> 📖 **详细使用方式**: [docs/USAGE.md](./docs/USAGE.md)

### 三种使用方式概览

| 方式 | 适用场景 | 链接 |
|------|---------|------|
| 方式1：通用模板 | 新手、简单任务 | [USAGE.md](./docs/USAGE.md#方式1通用模板推荐新手) |
| 方式2：子系统配置 | 大多数任务（推荐） | [USAGE.md](./docs/USAGE.md#方式2子系统配置推荐) |
| 方式3：自定义配置 | 高级用户、特殊需求 | [USAGE.md](./docs/USAGE.md#方式3自定义配置) |

### 覆盖率报告驱动模式

当用户提供测试覆盖率报告时，系统将自动切换到**覆盖率报告驱动模式**，此模式具有以下特点：

**优势**：
- **高效**：跳过覆盖率分析步骤，直接基于报告中的缺失项生成用例
- **精准**：严格按照覆盖率报告中列出的未覆盖 API、参数组合和场景生成测试
- **快速**：显著缩短生成时间，特别是对于大型 API 集合

**工作方式**：
1. 解析用户提供的覆盖率报告
2. 提取报告中标记的缺失测试项
3. 仅扫描现有测试文件以获取代码风格（不进行覆盖率分析）
4. 直接生成缺失项的测试用例

**覆盖率报告格式要求**：
报告应包含以下信息：
- 未覆盖的 API 名称
- 缺失的参数组合
- 缺失的测试场景（如边界值、错误码等）
- 测试类型（PARAM、ERROR、RETURN、BOUNDARY）

**从覆盖率报告提取错误码的规范**：

1. **读取错误码列**：例如 "401/17000002/17000007"
2. **从 @throws 标记验证**：检查 .d.ts 文件中的 @throws 标记
3. **确定实际的错误码**：根据参数类型和触发条件确定具体错误码
4. **生成测试时明确声明**：
   ```markdown
   - **预期结果**: 抛出错误码 401  # 明确
   - **断言方法**: `expect(e.code).assertEqual(ErrorCode)`  # 正确
   ```

> 💡 **提示**：如果已有覆盖率报告，直接提供报告内容将获得最佳的效率和精准度

### API 语法类型过滤（新增）

#### 概述

当任务明确说明是 arkts-dynamic 或 arkts-static 语法任务时，系统会：

1. **自动过滤 API**：根据语法类型过滤 API，只生成支持目标语法的测试用例
2. **自动验证**：验证生成的测试用例使用的 API 是否支持目标语法类型
3. **防止错误**：避免使用不支持目标语法的 API，防止编译错误

#### 工具和文档

| 工具/文档 | 路径 | 说明 |
|-----------|------|------|
| API 语法类型检查脚本 | `scripts/check_syntax_type.js` | 编译前验证测试用例使用的 API |
| API 语法类型过滤文档 | `modules/L2_Analysis/unified_api_parser.md` 第十章 | API 语法类型过滤详细说明 |
| 检查脚本使用指南 | `scripts/check_syntax_type_usage.md` | 检查脚本的使用示例和常见问题 |

#### 使用示例

```bash
# 编译前检查 API 语法类型
cd /mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode_static/entry/src/main/src/test/

node ~/.opencode/skills/oh-xts-generator-template/scripts/check_syntax_type.js \
  --syntax-type static \
  --test-dir ./

# 检查通过后再编译
if [ $? -eq 0 ]; then
  echo "检查通过，开始编译..."
  ./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTestErrorCodeStaticTest
fi
```

## 核心工作流程

### 工作流程分支

本技能支持两种工作流程，根据用户输入自动选择：

#### 流程 A：覆盖率报告驱动（当用户提供覆盖率报告时）
1. **确定子系统配置** - 加载核心配置和子系统差异化配置
    ├─ 检查是否存在子系统配置文件
    ├─ 加载通用配置 (_common.md)
    ├─ 加载子系统配置 ({Subsystem}/_common.md)
    └─ 加载模块配置 ({Subsystem}/{Module}.md)（如需）
2. **解析覆盖率报告** - 从用户提供的覆盖率报告中提取缺失测试项
    ├─ 识别未覆盖的 API 和参数组合
    ├─ 提取缺失的测试场景
    └─ 分析需补充的测试类型（PARAM、ERROR、RETURN、BOUNDARY）
3. **API 信息解析** - 解析 .d.ts 文件，提取缺失测试项的接口、方法、参数信息
    ├─ 读取 API 声明文件 (.d.ts)
    ├─ 查找并解析 API 文档
    └─ 综合分析
 4. **扫描代码风格** - 快速扫描现有测试文件，仅提取代码风格（跳过覆盖率分析）
    └─ [使用 analysis-agent subagent - 仅代码风格模式]
5. **生成测试用例和测试设计文档** - 基于覆盖率报告的缺失项，同时生成测试用例和测试设计文档
    ├─ 应用子系统特有规则
    ├─ 使用子系统特有模板
    ├─ 应用已有用例的代码风格
    ├─ **严格遵循 API 声明文件中的接口定义**
    ├─ 在生成每个测试用例的同时，同步输出对应的测试设计文档条目
    └─ 最后统一输出完整的测试设计文档文件
6. **注册测试套** - 在 List.test.ets 中注册新增测试文件（如需）
    ├─ 添加 import 语句
    └─ 在 testsuite() 函数中调用
7. **⚠️ 格式化和验证（强制步骤）** - 检查语法规范，验证断言方法，确保测试用例质量
     ├─ **完成条件**：所有语法错误已修复，断言方法正确，代码符合规范
     ├─ **检查项**：
     │  ├─ ArkTS 语法规范性（动态/静态）
     │  ├─ @tc 注释块完整性
     │  ├─ hypium 导入语句正确性
     │  ├─ 测试用例命名规范
     │  └─ 断言方法正确性
     └─ [使用 validation-agent subagent]
        ├─ 生成动态 XTS 用例时遵循动态语法规范，详细指南：[# ArkTS动态语法检查规则全集](./references/ArkTS_Dynamic_Syntax_Rules.md)
        └─ 生成静态 XTS 用例时遵循静态语法规范，需要调用专门的 `arkts-static-spec` 技能进行语法规范校验：
            ├─ 使用方式：`请使用 arkts-static-spec 进行语法规范校验`
            └─ 详细指南：[ArkTS 静态语言语法规范指南](./docs/ARKTS_STATIC_GUIDE.md)
8. 编译验证（重要）
    ├─ 检测运行环境（Linux/Windows）
    ├─ 根据环境选择编译方案
    ├─ Linux 环境：使用 subagent 执行编译，监听进程，自动修复语法错误
    ├─ Windows 环境：根据关键词自动选择动态或静态编译模式
    └─ **详细编译流程**：参见注意事项第7条"编译环境检测"
9. 输出更新文件列表、测试设计文档和覆盖率对比

#### 流程 B：标准流程（用户未提供覆盖率报告时）
1. **确定子系统配置** - 加载核心配置和子系统差异化配置
    ├─ 检查是否存在子系统配置文件
    ├─ 加载通用配置 (_common.md)
    ├─ 加载子系统配置 ({Subsystem}/_common.md)
    └─ 加载模块配置 ({Subsystem}/{Module}.md)（如需）
2. **API 信息解析** - 解析 .d.ts 文件，提取接口、方法、参数信息
    ├─ 读取 API 声明文件 (.d.ts)
    ├─ 查找并解析 API 文档
    └─ 综合分析
 3. **测试覆盖分析** - 扫描现有测试文件，分析代码风格和覆盖率
    └─ [使用 analysis-agent subagent]
4. **生成测试用例和测试设计文档** - 应用子系统特有规则，同时生成测试用例和测试设计文档
    ├─ 应用子系统特有规则
    ├─ 使用子系统特有模板
    ├─ 应用已有用例的代码风格
    ├─ **严格遵循 API 声明文件中的接口定义**
    ├─ 在生成每个测试用例的同时，同步输出对应的测试设计文档条目
    └─ 最后统一输出完整的测试设计文档文件
5. **注册测试套** - 在 List.test.ets 中注册新增测试文件（如需）
    ├─ 添加 import 语句
    └─ 在 testsuite() 函数中调用
6. **⚠️ 格式化和验证（强制步骤）** - 检查语法规范，验证断言方法，确保测试用例质量
     ├─ **完成条件**：所有语法错误已修复，断言方法正确，代码符合规范
     ├─ **检查项**：
     │  ├─ ArkTS 语法规范性（动态/静态）
     │  ├─ @tc 注释块完整性
     │  ├─ hypium 导入语句正确性
     │  ├─ 测试用例命名规范
     │  └─ 断言方法正确性
     └─ [使用 validation-agent subagent]
        ├─ 生成动态 XTS 用例时遵循动态语法规范，详细指南：[# ArkTS动态语法检查规则全集](./references/ArkTS_Dynamic_Syntax_Rules.md)
        └─ 生成静态 XTS 用例时遵循静态语法规范，需要调用专门的 `arkts-static-spec` 技能进行语法规范校验：
            ├─ 使用方式：`请使用 arkts-static-spec 进行语法规范校验`
            └─ 详细指南：[ArkTS 静态语言语法规范指南](./docs/ARKTS_STATIC_GUIDE.md)
7. 编译验证（重要）
    ├─ 检测运行环境（Linux/Windows）
    ├─ 根据环境选择编译方案
    ├─ Linux 环境：使用 subagent 执行编译，监听进程，自动修复语法错误
    ├─ Windows 环境：根据关键词自动选择动态或静态编译模式
    └─ **详细编译流程**：参见注意事项第7条"编译环境检测"
8. 输出更新文件列表、测试设计文档和覆盖率对比

## 配置扩展

**配置文件查找路径**：
```
.opencode/skills/oh-xts-generator-template/references/subsystems/
```

**支持的子系统**：
- `testfwk` - 测试框架
- `storage` - 存储管理
- `multimedia` - 多媒体
- `arkts` - ArkTS 语言特性
- 其他自定义子系统

> 📖 **详细配置说明**: [docs/CONFIG.md](./docs/CONFIG.md)

### 配置优先级

```
用户自定义配置 > 模块配置 > 子系统配置 > 核心配置
```

### 配置架构说明 ⭐ **重要**

> **配置设计原则**：核心配置 + 最小化差异化

#### 配置层级说明

| 层级 | 文件 | 说明 |
|------|------|------|
| **核心配置** | `references/subsystems/_common.md` | 核心强制规范 + 默认规范 + 扩展接口 |
| **子系统配置** | `references/subsystems/{Subsystem}/_common.md` | 基础信息 + 子系统差异化配置 + 特殊规则|
| **模块配置**|`references/subsystems/{Subsystem}/{Module}.md` | 基础信息 + 子系统差异化配置 + 模块差异化配置 + 特殊规则|
| **用户自定义配置** | 用户提供的配置 | 覆盖子系统配置和核心配置 |

## 输出规范

### 测试用例编号(`@tc.number`)
格式：`SUB_[子系统]_[模块]_[API]_[类型]_[序号]`，类型包括 PARAM、ERROR、RETURN、BOUNDARY

### 测试设计文档规范
- 文件命名：`{测试文件名}.design.md`

## 重要注意事项

### 1. ⚠️ 格式化和验证步骤（强制 - 不可跳过）

**重要提示**：格式化和验证是测试用例生成的**核心强制步骤**，**绝不可跳过**！

**为什么此步骤不可跳过？**
- ✅ 确保生成的测试用例符合 XTS 规范
- ✅ 避免编译阶段才发现语法错误
- ✅ 保证测试用例质量和可维护性
- ✅ 提高测试执行成功率

**完成条件检查清单**：
- [ ] 所有语法错误已修复
- [ ] @tc 注释块完整且格式正确
- [ ] hypium 导入语句正确
- [ ] 测试用例命名符合规范（小驼峰）
- [ ] 断言方法使用正确
- [ ] ArkTS 语法符合规范（动态/静态）

**常见问题**：
- ❌ 直接跳到编译步骤（编译不会捕获所有问题）
- ❌ 认为此步骤是可选的
- ❌ 忽略验证结果中的警告
- ❌ 不完整执行 validation-agent 检查

### 2. @tc 注释块规范（强制）
所有测试用例必须添加标准的 `@tc` 注释块，包括 name、number、desc 等字段。详见：[测试框架规范](./references/subsystems/_common.md)

### 3. hypium 导入规范（强制）
详见：[Hypium 测试框架基础 - 导入语句规范](./modules/L1_Framework/hypium_framework.md#四导入语句规范)

### 4. 工程文件修改限制（强制）
严格禁止修改工程目录中的配置文件，只能在指定测试目录创建测试文件

### 5. API 声明严格遵循（强制）
必须严格按照 `.d.ts` 文件声明的接口生成测试用例，禁止使用未声明的接口

### 6. 编译相关
- Linux 环境必须使用 `./test/xts/acts/build.sh` 脚本编译
- 编译前确认 BUILD.gn 中的编译目标

| 环境 | 推荐方式 | 入口文档 |
|------|---------|---------|
| Linux | ./test/xts/acts/build.sh 脚本 | [Linux 编译工作流](../modules/L4_Build/build_workflow_linux.md) |
| Windows | DevEco Studio IDE | [Windows 编译工作流](../modules/L4_Build/build_workflow_windows.md) |

#### 5.1 Linux 环境编译

**基础要求**：
- 使用 `./test/xts/acts/build.sh` 脚本编译，**不要使用 `hvigorw`**
- 环境检测：`uname -s`

**编译流程**：
1. **预编译清理**（强制）：
   - 使用 `~/.opencode/skills/oh-xts-generator-template/scripts/cleanup_group.sh` 脚本
   - 清理目的：确保编译结果包含所有最新代码
   - ⚠️ 安全注意事项：见第 3.1 节清理操作安全说明

2. **静态测试套预置条件**（编译静态套时）：
   - 校验 hvigor 版本：`"6.0.0-arkts1.2-ohosTest-25072102"`
   - 版本匹配：跳过工具替换；版本不匹配：执行替换流程
   - 工具替换：清理 SDK 缓存 → 清理旧工具 → 下载新工具 → 移动到预置目录

3. **编译执行**：
   - 使用 general subagent 执行（避免主流程中断）
   - 监听编译进程直至完成
   - **语法错误**：自动分析并修复，重试编译
   - **配置错误**：暂停并向用户确认后才修改

#### 5.2 Windows 环境编译

根据关键词自动选择编译模式：

##### 7.2.1 ArkTS 动态 XTS 编译（默认）
- **编译方式**：DevEco Studio IDE 或 `hvigorw.bat`
- **编译目标**：`Build → Build OhosTest Hap(s)`
- **参考文档**：`modules/L4_Build/build_workflow_windows.md` 第三章

##### 7.2.2 ArkTS 静态 XTS 编译（arkts-sta）
- **适用场景**：基于 ArkTS 静态强类型语法的 XTS 测试 工程
- **触发关键词**：当用户提到以下任一关键词时自动启用：
  - **技术术语**：`arkts-sta`、`ArkTS静态`、`arkts static`、`ArkTS static`
  - **通用表述**：`静态xts`、`静态 XTS`、`static arkts`、`static xts`
  - **操作描述**：`编译静态`、`静态编译`、`静态工程编译`、`Windows静态编译`
- **编译方式**：PowerShell 脚本或 `hvigorw.bat` 命令行工具
- **Java 环境**：**必需**配置 JAVA_HOME 环境变量
- **编译特点**：
  - 严格的静态类型检查
  - 所有类型必须有显式注解
  - 禁止使用 any 类型
  - 所有字段必须初始化
  - **类型强校验**：入参类型不匹配时直接编译报错，不会运行时抛出401错误码
  - **编译时类型验证**：所有类型错误在编译阶段暴露，提高代码质量
  - **无运行时类型异常**：消除了因类型错误导致的运行时崩溃
- **类型校验策略**：
  - 编译器检查所有类型注解的正确性
  - 函数参数类型必须与声明完全匹配
  - 返回值类型必须与声明一致
  - 泛型类型参数必须在编译时确定
- **参考文档**：`modules/L4_Build/build_workflow_windows.md` 第十章

> **⚠️ 重要提示**：
> - 默认使用动态编译模式
> - 仅在用户明确提到静态相关关键词时启用静态编译模式
> - 静态编译需要配置 Java 环境变量（JAVA_HOME）

> 📖 **详细的编译文档**: [modules/L4_Build/](./modules/L4_Build/)

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
- Q8: ArkTS 静态语法校验问题
- Q9: 如何调用 arkts-static-spec 技能
- Q10: 如何使用覆盖率报告驱动模式

## 参考文档

### 详细文档

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

