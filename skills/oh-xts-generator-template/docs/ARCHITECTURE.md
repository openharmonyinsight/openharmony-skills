# 模块化架构详解

> **OpenHarmony XTS 测试用例通用生成模板 - 模块化架构**

## 四层模块化架构

本 Template 采用四层模块化架构，可根据任务需求按需加载：

```
xts-generator/
├── modules/
│   ├── L1_Framework/            # 框架层（必须加载）
│   │   ├── hypium_framework.md  # Hypium框架知识
│   │   ├── arkts_standards.md   # ArkTS语法规范
│   │   ├── test_conventions.md  # 测试约定
│   │   └── uitest_framework.md  # UiTest框架（可选）
│   ├── L2_Analysis/             # 分析层（按需加载）
│   │   ├── api_parser.md        # API定义解析
│   │   ├── project_parser.md    # 工程配置解析
│   │   ├── coverage_analyzer.md # 测试覆盖分析
│   │   └── doc_reader.md        # 文档阅读
│   ├── L3_Generation/           # 生成层（按需加载）
│   │   ├── test_generator.md    # 测试生成策略
│   │   ├── design_doc_generator.md # 测试设计文档生成
│   │   ├── templates.md         # 代码模板库
│   │   └── examples/           # 示例文件
│   └── L4_Build/                # 构建层（按需加载）
│       ├── build_workflow_linux.md    # Linux编译工作流
│       ├── build_workflow_windows.md  # Windows编译工作流
│       ├── build_gn_config.md   # BUILD.gn配置
│       ├── linux_compile_env_setup.md  # Linux环境准备
│       ├── linux_prebuild_cleanup.md   # 预编译清理
│       └── linux_compile_troubleshooting.md # 问题排查
└── references/
    └── subsystems/              # 子系统配置 ⭐
        ├── _common.md           # 通用配置
        └── {SubsystemName}/   # 子系统配置
```

## 模块加载说明

| 任务类型 | 必需模块 | 说明 |
|---------|---------|------|
| 基础API测试 | L1_Framework + L3_Generation | 基础测试生成 |
| 测试覆盖分析 | L1_Framework + L2_Analysis | 分析现有测试 |
| 完整测试生成 | 所有模块 | 完整工作流 |

## L1_Framework - 框架层

### hypium_framework.md

Hypium 测试框架的核心知识，包括：
- 测试套件结构
- 断言方法
- 测试生命周期

### arkts_standards.md

ArkTS 语法规范，包括：
- 类型系统
- 对象和属性
- 运算符
- 函数
- 控制流
- 类和接口
- 模块和导入
- 标准库

### test_conventions.md

XTS 测试约定，包括：
- 测试用例命名规范
- 测试级别定义
- 测试类型分类
- 测试粒度划分

### uitest_framework.md

UiTest 测试框架，包括：
- UI组件查找
- UI操作模拟
- UI状态验证

## L2_Analysis - 分析层

### api_parser.md

API 定义解析器，包括：
- .d.ts 文件读取
- 接口/方法/属性提取
- 参数类型和约束提取
- 错误码识别
- API 语法类型判断

### project_parser.md

工程配置解析器，包括：
- build-profile.json5 解析
- 工程语法类型识别
- 兼容性检查

### build_workflow_linux.md

Linux 编译工作流，包括：
- build.sh 脚本使用
- 编译命令格式
- 错误处理

### build_workflow_windows.md

Windows 编译工作流，包括：
- DevEco Studio 编译
- hvigorw.bat 编译
- 测试执行

### coverage_analyzer.md

测试覆盖分析，包括：
- 测试文件扫描
- API 覆盖率计算
- 未覆盖 API 识别

### doc_reader.md

文档阅读器，包括：
- API 文档查找
- 错误码文档提取
- 使用场景分析

## L3_Generation - 生成层

### test_generator.md

测试生成策略，包括：
- 参数测试生成
- 错误码测试生成
- 返回值测试生成
- 边界值测试生成

### code_formatter.md

代码格式化，包括：
- 代码风格统一
- 命名规范检查
- 格式化规则应用

### templates.md

代码模板库，包括：
- 基础测试模板
- 异步API测试模板
- 错误码测试模板
- @tc注释块模板

## 按需加载策略

### 自动加载

- L1_Framework 总是首先加载
- 根据任务类型自动选择 L2_Analysis 和 L3_Generation

### 手动加载

用户可以明确指定需要加载的模块：

```
请使用 xts-generator 生成测试用例：

任务类型: 基础API测试
加载模块: L1_Framework + L3_Generation
```
