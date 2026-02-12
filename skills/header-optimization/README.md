# 头文件优化技能

通过系统性依赖减少和实现重构，优化 ace_engine 中 C++ 头文件编译效率的完整技能。

## 快速开始

```
用户: "优化头文件 frameworks/core/components_ng/pattern/button/button_pattern.h"

Claude: 我将使用 header-optimization 技能来优化这个头文件。让我先分析当前的依赖关系...

[分析和优化步骤...]

结果:
- 头文件引用从 7 个减少到 1 个（减少 86%）
- 将 12 个内联方法移至 cpp 文件
- 头文件大小减少 72%
- 所有更改已使用 git add 暂存
```

## 本技能功能

通过以下方式优化 C++ 头文件：

1. **内联提取** - 将方法实现（3+ 行）从头文件移至 cpp 文件
2. **头文件消除** - 移除未使用的头文件依赖
3. **前置声明** - 用前置声明替换完整头文件引用
4. **头文件拆分** - 将常量/枚举提取到独立头文件
5. **PIMPL 模式** - 在有益时隐藏实现细节
6. **模板优化** - 显式模板实例化

## 核心约束

- ✅ 仅修改结构，永不修改业务逻辑
- ✅ 独立编译验证（无需完整构建）
- ✅ 直接编辑文件（最小化新文件）
- ✅ 成功优化后进行 git 暂存
- ❌ 永不修改 test_header.cpp（只读参考）

## 技能内容

### 核心文档
- **SKILL.md** - 主要技能指令（触发时由 Claude 读取）
- **README.md** - 本文件

### 参考文档 (`references/`)
- **patterns.md** - 常见重构模式及示例
- **pimp-guide.md** - 完整的 PIMPL 模式指南
- **forward-declaration.md** - 前置声明最佳实践

### 示例 (`examples/`)
- **before-after/** - 优化前后对比
- **pimpl-example/** - 完整 PIMPL 实现示例
- **split-header/** - 头文件拆分演示

### 实用脚本 (`scripts/`)
- **analyze-includes.sh** - 分析头文件依赖的 Bash 脚本
- **extract-includes.py** - 详细头文件分析的 Python 脚本

## 使用方法

### 基本优化

```
用户: "Optimize frameworks/core/components_ng/pattern/button/button_pattern.h"
```

### 仅分析

```
用户: "Analyze header file X but don't modify it (只分析不进行修改)"
```

Claude 将生成详细报告和建议，而不修改文件。

### test_header.cpp 分析

```
用户: "Analyze test_header.cpp dependencies"
```

Claude 将从 test_header.cpp 提取头文件并进行优化。

## 技能结构

```
header-optimization/
├── SKILL.md                    # 主要技能指令
├── README.md                   # 本文件
├── references/                 # 详细参考文档
│   ├── patterns.md
│   ├── pimp-guide.md
│   └── forward-declaration.md
├── examples/                   # 可运行示例
│   ├── README.md
│   ├── before-after/
│   ├── pimpl-example/
│   └── split-header/
└── scripts/                    # 实用脚本
    ├── analyze-includes.sh
    └── extract-includes.py
```

## 开发

### 创建技能

本技能使用技能开发工作流创建：

1. **理解** - 确定具体用例 - 优化 ace_engine 头文件
2. **规划** - 确定所需资源：
   - 带工作流的 SKILL.md
   - 详细技术的 references/
   - 模式的 examples/
   - 分析的 scripts/
3. **结构** - 在 plugin skills/ 下创建目录
4. **内容** - 编写 SKILL.md 和支持资源
5. **验证** - 检查结构、触发器、组织

### 验证清单

- [x] SKILL.md 存在且包含有效的 YAML 前置元数据
- [x] 前置元数据包含 `name` 和 `description` 字段
- [x] 描述使用第三人称（"This skill should be used when..."）
- [x] 描述包含具体触发短语
- [x] SKILL.md 主体使用祈使/不定式形式
- [x] 内容专注且精简（约 1,800 词）
- [x] 详细内容移至 references/
- [x] 在 examples/ 中提供示例
- [x] 实用脚本在 scripts/
- [x] 渐进式披露（元数据 → SKILL.md → references）

### 测试技能

安装后，使用以下命令测试：

```
用户: "Use header-optimization skill to analyze button_pattern.h"
```

验证：
- 技能在触发时加载
- 分析彻底
- 建议具体
- 根据需要使用参考/示例

## 触发短语

技能触发短语如：
- "optimize header files"
- "reduce header dependencies"
- "优化头文件"
- "减少头文件依赖"
- "analyze compilation efficiency"
- "分析编译效率"
- 提及 test_header.cpp 分析

## 集成

本技能与以下内容集成：

- **compile-analysis skill** - 用于编译命令提取和测量
- **ace_engine project** - 为 OpenHarmony ACE Engine 代码库优化

## 最佳实践

### 对于 Claude（使用技能）

1. **从分析开始** - 始终在修改前分析
2. **遵循步骤** - 按顺序实现（1-6）
3. **验证编译** - 使用 compile-analysis 进行独立编译
4. **测量影响** - 报告优化前后指标
5. **暂存更改** - 成功优化后 git add
6. **遵守约束** - 永不修改 test_header.cpp，永不做完整构建

### 对于用户（调用技能）

1. **提供明确目标** - 指定头文件或 test_header.cpp
2. **指定模式** - 仅分析或完全优化
3. **审查建议** - 应用更改前检查分析
4. **验证结果** - 优化后测试编译

## 渐进式披露

本技能使用三级加载：

1. **元数据（始终）** - 名称 + 描述（约 100 词）
2. **SKILL.md（触发时）** - 核心工作流（约 1,800 词）
3. **参考资料（按需）** - 详细文档（约 6,000+ 词）

这保持了低上下文使用，同时提供全面指导。

## 维护

### 更新时机

- 发现新的优化技术
- ace_engine 模式变更
- 用户反馈识别问题
- 构建系统变更影响编译

### 更新流程

1. 确定需要更新的内容
2. 更新 SKILL.md 以更改工作流
3. 更新 references/ 以获取详细内容
4. 如果模式变更，添加新示例
5. 使用真实头文件测试
6. 使用 skill-reviewer 验证

## 贡献

要改进此技能：

1. 使用真实的 ace_engine 头文件测试
2. 记录发现的问题
3. 提出改进 SKILL.md 的建议
4. 向 examples/ 添加新示例
5. 用新模式更新 references
6. 增强脚本以获得更好的分析

## 支持

如有问题或疑问：
- 检查 examples/ 中的类似案例
- 查阅 references/ 获取详细指导
- 使用 scripts/ 进行分析
- 查看 ace_engine CLAUDE.md 了解上下文

---

**技能版本**: 1.0.0
**最后更新**: 2025-01-27
**目标项目**: OpenHarmony ACE Engine
