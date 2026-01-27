# ark-layer Skill 结构说明

## 概述

本 skill 采用**渐进式披露**（Progressive Disclosure）原则设计，将原有的 667 行单文件拆分为核心工作流程（SKILL.md）和详细参考材料（references/），帮助开发者快速上手并按需深入了解。

## 目录结构

```
ark-layer/
├── SKILL.md                    # 核心工作流程（342行）
└── references/                 # 详细参考材料
    ├── architecture.md         # 架构设计原则和分层规则（364行）
    ├── service-lifecycle.md    # Service 生命周期详解（480行）
    ├── phases.md              # 多阶段加载系统（478行）
    ├── templates.md           # 代码模板（793行）
    ├── arkts-syntax.md        # ArkTS 语法限制和替代方案（551行）
    ├── scenarios.md           # 特殊场景处理（848行）
    └── faq.md                 # 常见问题 FAQ（807行）
```

## 文件说明

### SKILL.md（核心工作流程）

**目标读者**：所有开发者
**阅读时机**：首次使用或快速查阅

**内容**：
- YAML frontmatter（name, description）
- 项目概述（简化版）
- 核心架构原则（高度概括）
- 你的职责（7个主要职责）
- 快速开始（最小可运行示例）
- 输出格式规范
- 指向 references/ 的导航链接

**特点**：
- < 500 行，易于快速阅读
- 只保留核心工作流程
- 提供明确的导航指引

### references/architecture.md

**目标读者**：需要深入理解架构的开发者
**阅读时机**：设计新功能或审查代码时

**内容**：
- 四层架构模型详解
- 各层职责和规则
- 依赖规则（允许和禁止的依赖）
- 分层验证清单
- 常见违规场景

### references/service-lifecycle.md

**目标读者**：需要实现 Service 的开发者
**阅读时机**：创建或修改 Service 时

**内容**：
- Service 生命周期四个阶段详解
- 构造函数、init、load、unload 的职责
- 依赖关系处理
- 常见场景和最佳实践

### references/phases.md

**目标读者**：需要配置服务加载的开发者
**阅读时机**：配置应用层编排时

**内容**：
- Phase 机制概述
- 四个预定义阶段详解
- 自定义 Phase 创建方法
- 应用层编排完整示例
- 执行流程图

### references/templates.md

**目标读者**：需要生成代码的开发者
**阅读时机**：创建新 Service 或页面时

**内容**：
- 标准 Service 模板（基础版、带依赖版、Infra 层版）
- 应用层编排模板（最小版、完整版）
- 自定义 Phase 模板
- 页面组件模板（基础版、列表版、状态管理版）

### references/arkts-syntax.md

**目标读者**：需要遵守 ArkTS 语法的开发者
**阅读时机**：编写代码或代码审查时

**内容**：
- 严禁使用的语法（展开、解构、throw）
- 每种语法的替代方案
- 常见场景的完整示例
- 实用工具函数
- 检查清单和迁移指南

### references/scenarios.md

**目标读者**：遇到特殊问题的开发者
**阅读时机**：处理复杂场景时

**内容**：
- 10 个特殊场景的详细处理方案
- 每个场景包含问题描述、解决方案、代码示例
- 场景包括：登录前加载数据、复杂依赖、持久化、事件监听、并行依赖、定时刷新、大数据处理、状态共享、错误重试、延迟加载

### references/faq.md

**目标读者**：遇到常见问题的开发者
**阅读时机**：遇到问题时快速查找

**内容**：
- 40+ 个常见问题及解答
- 按主题分类：Service、生命周期、依赖管理、Phase、页面使用、ArkTS 语法、架构设计、错误处理
- 每个问题都有清晰的答案和代码示例

## 使用指南

### 首次使用

1. 阅读 **SKILL.md** 了解核心工作流程
2. 跟随"快速开始"创建第一个 Service
3. 遇到问题时查阅 **references/faq.md**

### 深入学习

1. 理解架构：阅读 **references/architecture.md**
2. 掌握生命周期：阅读 **references/service-lifecycle.md**
3. 学习阶段配置：阅读 **references/phases.md**

### 实际开发

1. 生成代码：参考 **references/templates.md**
2. 检查语法：参考 **references/arkts-syntax.md**
3. 处理特殊场景：参考 **references/scenarios.md**
4. 解决问题：查阅 **references/faq.md**

## 设计原则

### 1. 渐进式披露

- **SKILL.md**：只保留核心内容，快速上手
- **references/**：按需加载的详细文档
- 避免信息过载，提高学习效率

### 2. 模块化

- 每个参考文件独立完整
- 可以单独阅读和理解
- 减少认知负担

### 3. 可导航

- SKILL.md 提供明确的链接指引
- 每个参考文件有"返回主文档"链接
- 便于在文件之间跳转

### 4. 实用性

- 提供大量代码示例
- 包含最佳实践和常见错误
- 给出清晰的解决方案

## 对比原有结构

### 原有结构（单文件）

```
.claude/skills/
└── ark-layer.md  (667行)
```

**问题**：
- 信息过载，难以快速上手
- 详细内容混在一起，查找困难
- 不符合渐进式披露原则

### 新结构（多文件）

```
.claude/skills/ark-layer/
├── SKILL.md              (342行) - 核心工作流程
└── references/           (4322行) - 详细参考材料
    ├── architecture.md
    ├── service-lifecycle.md
    ├── phases.md
    ├── templates.md
    ├── arkts-syntax.md
    ├── scenarios.md
    └── faq.md
```

**优势**：
- ✅ SKILL.md < 500 行，易于快速阅读
- ✅ 详细内容按主题分类，便于查找
- ✅ 符合渐进式披露原则
- ✅ 每个文件独立完整，可单独阅读
- ✅ 提供清晰的导航和链接

## 维护建议

### 更新 SKILL.md

- 保持简洁，只保留核心内容
- 更新指向 references/ 的链接
- 确保快速开始示例始终可用

### 更新 references/

- 每个文件应该独立完整
- 添加新的常见问题到 faq.md
- 添加新的特殊场景到 scenarios.md
- 更新代码模板以反映最佳实践

### 添加新内容

1. 评估是否属于核心内容 → 添加到 SKILL.md
2. 评估是否属于详细参考 → 添加到合适的 references/ 文件
3. 如果是新主题 → 创建新的 references/ 文件
4. 更新 SKILL.md 中的导航链接

## 参考资源

- [anthropics/skills](https://github.com/anthropics/skills) - Claude Skills 仓库
- [skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator) - Skill 创建工具

## 版本历史

- **v1.0** (2025-01-26): 从单文件 ark-layer.md (667行) 重构为渐进式披露结构
  - 创建 SKILL.md (342行)
  - 拆分出 7 个详细参考文件 (4322行)
  - 符合渐进式披露原则

---

**记住**：好的文档应该让开发者能够快速上手，并在需要时深入了解更多细节。
