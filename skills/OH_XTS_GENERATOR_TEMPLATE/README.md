# OH_XTS_GENERATOR_TEMPLATE

> **OpenHarmony XTS 测试用例通用生成模板**

## 简介

OH_XTS_GENERATOR_TEMPLATE 是一个通用的 OpenHarmony XTS 测试用例生成模板，设计为**可配置、可扩展**的通用框架，适用于各个子系统的测试用例生成。

### 核心特性

1. **通用测试生成流程** - 提供完整的测试用例生成工作流
2. **模块化架构** - 三层模块化设计（L1/L2/L3），按需加载
3. **分层配置系统** - 通用配置 + 子系统特有配置
4. **灵活扩展机制** - 支持各子系统添加特有配置和模板

### 核心功能

- **API定义解析**: 解析 `.d.ts` 文件，提取接口、方法、参数、返回值、错误码
- **测试覆盖分析**: 分析现有测试文件，识别已覆盖和未覆盖的API
- **智能测试生成**: 根据测试策略自动生成符合 XTS 规范的测试用例
- **代码规范检查**: 确保生成的代码符合 XTS 测试规范
- **编译问题解决**: 提供编译指南和问题排查方案

## 适用场景

- ✅ 为新 API 生成完整的测试套件
- ✅ 分析现有测试的覆盖情况
- ✅ 补充缺失的测试用例
- ✅ 验证测试代码规范性
- ✅ 各子系统定制化测试生成

## 快速开始

### 使用方式1：通用模板（推荐新手）

```
请使用 OH_XTS_GENERATOR_TEMPLATE 为以下 API 生成测试用例：

子系统: ArkUI
API: Component.onClick()
定义文件: interface/sdk-js/api/@ohos.arkui.d.ts
```

### 使用方式2：子系统配置（推荐）

```
请使用 OH_XTS_GENERATOR_TEMPLATE 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
```

### 使用方式3：自定义配置

```
请使用 OH_XTS_GENERATOR_TEMPLATE 生成测试用例，使用自定义配置：

子系统: MySubsystem
自定义配置:
  Kit包: @kit.MyKit
  测试路径: test/xts/acts/mysubsystem/
  API声明: interface/sdk-js/api/@ohos.mysubsystem.d.ts

API: myAPI.method()
```

## 文档结构

### 主文件

- **SKILL.md** - 技能主文件，包含核心功能和工作流程

### 详细文档

- **docs/ARCHITECTURE.md** - 模块化架构详解
- **docs/CONFIG.md** - 配置扩展机制详解
- **docs/USAGE.md** - 使用方式详解

### 参考文档

- **references/subsystems/_common.md** - 通用配置
- **references/subsystems/{Subsystem}/**** - 子系统配置

### 示例文件

- **examples/**** - 子系统配置示例

### 子模块

- **modules/L1_Framework/**** - 框架层文档
- **modules/L2_Analysis/**** - 分析层文档
- **modules/L3_Generation/**** - 生成层文档

## 版本信息

- **当前版本**: 1.11.0
- **创建日期**: 2025-01-31
- **最后更新**: 2026-02-05
- **兼容性**: OpenHarmony API 10+

> 📖 **详细的版本更新记录请查看**: [CHANGELOG.md](./CHANGELOG.md)

## 许可证

Apache License 2.0
