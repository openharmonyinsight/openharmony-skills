# 配置扩展机制详解

> **xts-generator** - 配置系统使用指南
> **版本**: 2.0.0
> **更新日期**: 2026-02-05

## 目录

- [一、配置系统概述](#一配置系统概述)
- [二、配置文件结构](#二配置文件结构)
- [三、配置优先级](#三配置优先级)
- [四、已有子系统配置](#四已有子系统配置)
- [五、创建新子系统配置](#五创建新子系统配置)
- [六、配置最佳实践](#六配置最佳实践)
- [七、常见问题](#七常见问题)

---

## 一、配置系统概述

xts-generator 采用**分层配置系统**，支持从通用到特化的多级配置继承。

### 1.1 设计理念

**核心思想**：通过分层配置实现通用性和灵活性的平衡

- **通用配置**：所有子系统共享的基础配置
- **子系统配置**：特定子系统的专有配置
- **用户配置**：使用时指定的临时配置

**优点**：
- ✅ 避免重复定义
- ✅ 统一基础规范
- ✅ 支持个性化定制
- ✅ 易于维护和扩展

### 1.2 配置继承关系

```
┌─────────────────────────────────────────┐
│         通用配置 (_common.md)           │
│    - 测试规范、代码模板、基础规则        │
└─────────────────┬───────────────────────┘
                  │ 继承
┌─────────────────▼───────────────────────┐
│      子系统配置 ({Subsystem}/_common.md) │
│    - 子系统特有规则、模块映射、Kit包     │
└─────────────────┬───────────────────────┘
                  │ 继承
┌─────────────────▼───────────────────────┐
│      模块配置 ({Subsystem}/{Module}.md)  │
│    - 模块特有规则、API列表、测试模板     │
└─────────────────────────────────────────┘
```

---

## 二、配置文件结构

### 2.1 目录结构

```
xts-generator/
└── references/
    └── subsystems/
        ├── _common.md                      # 通用配置（所有子系统共享）
        ├── ArkUI/                          # ArkUI 子系统配置
        │   ├── _common.md                  # ArkUI 子系统通用配置
        │   ├── Component.md                # Component 模块配置
        │   ├── Animator.md                 # Animator 模块配置
        │   └── Router.md                   # Router 模块配置
        ├── ArkWeb/                         # ArkWeb 子系统配置
        │   ├── _common.md                  # ArkWeb 子系统通用配置
        │   ├── Web.md                      # Web 模块配置
        │   └── WebViewController.md        # WebViewController 模块配置
        ├── testfwk/                        # 测试框架子系统配置
        │   ├── _common.md                  # 测试框架通用配置
        │   ├── uitest.md                   # UiTest 模块
        │   ├── JsUnit.md                   # JsUnit 模块
        │   └── perftest.md                 # PerfTest 模块
        └── {SubsystemName}/                # 其他子系统
            ├── _common.md                  # 子系统通用配置
            └── {ModuleName}.md             # 模块配置
```

### 2.2 配置文件类型

#### 类型1：通用配置 (`_common.md`)

**位置**: `references/subsystems/_common.md`

**作用**: 所有子系统共享的基础配置

**内容**:
- 测试用例编号格式
- 测试级别定义
- 测试类型定义
- 通用测试规则
- 通用代码模板
- @tc 注释块规范

**关键配置项**:
```markdown
### 测试用例编号格式
格式: `SUB_[子系统]_[模块]_[API]_[类型]_[序号]`

### 测试级别
- Level0: 冒烟测试 - 基本功能
- Level1: 基础测试 - 常用输入
- Level2: 主要测试 - 常用+错误场景
- Level3: 常规测试 - 所有功能
- Level4: 罕见测试 - 极端场景

### 测试类型
- Function: 功能测试
- Performance: 性能测试
- Reliability: 可靠性测试
- Security: 安全测试
```

#### 类型2：子系统通用配置 (`{Subsystem}/_common.md`)

**位置**: `references/subsystems/{SubsystemName}/_common.md`

**作用**: 特定子系统的通用配置

**内容**:
- 子系统信息（名称、Kit包、测试路径）
- API Kit 映射
- 模块映射配置
- 子系统特有测试规则
- 子系统通用代码模板

#### 类型3：模块配置 (`{Subsystem}/{Module}.md`)

**位置**: `references/subsystems/{SubsystemName}/{ModuleName}.md`

**作用**: 特定模块的配置

**内容**:
- 模块信息（所属子系统、模块名称、API声明文件）
- 模块概述
- 模块特有 API 列表
- 模块特有测试规则
- 模块特有代码模板

---

## 三、配置优先级

### 3.1 优先级规则

```
用户自定义配置（使用时指定）
    ↓ 优先级最高
子系统配置 ({Subsystem}/_common.md, {Subsystem}/{Module}.md)
    ↓ 优先级中等
通用配置 (_common.md)
    ↓ 优先级最低（默认值）
```

### 3.2 优先级示例

**场景**: 为 ArkUI 子系统生成测试用例

**通用配置** (`_common.md`):
- 测试用例编号格式: `SUB_[子系统]_[模块]_[API]_[类型]_[序号]`

**子系统配置** (`ArkUI/_common.md`):
- 测试路径: `test/xts/acts/arkui/test/`

**用户配置** (使用时指定):
- 测试路径: `test/xts/acts/arkui_custom/`

**最终配置**:
- 测试用例编号格式: 使用通用配置
- 测试路径: 使用用户配置（覆盖子系统配置）

### 3.3 配置覆盖规则

| 配置项 | 通用配置 | 子系统配置 | 用户配置 | 最终值 |
|-------|---------|-----------|---------|--------|
| 测试路径 | `test/xts/acts/` | `test/xts/acts/arkui/` | `test/xts/acts/arkui_custom/` | `test/xts/acts/arkui_custom/` |
| Kit包名 | - | `@kit.ArkUI` | `@kit.ArkUI` | `@kit.ArkUI` |
| 编号格式 | `SUB_...` | - | - | `SUB_...` |
| 测试规则 | 基础规则 | ArkUI规则 | - | ArkUI规则（覆盖） |

---

## 四、已有子系统配置

### 4.1 ArkUI 子系统

**位置**: `references/subsystems/ArkUI/`

**配置文件**:
- `_common.md` - ArkUI 子系统通用配置
- `Component.md` - Component 模块配置
- `Animator.md` - Animator 模块配置
- `Router.md` - Router 模块配置

**使用方式**:
```
子系统: ArkUI
API: Component.onClick()
```

### 4.2 ArkWeb 子系统

**位置**: `references/subsystems/ArkWeb/`

**配置文件**:
- `_common.md` - ArkWeb 子系统通用配置
- `Web.md` - Web 模块配置
- `WebViewController.md` - WebViewController 模块配置

**使用方式**:
```
子系统: ArkWeb
API: Web.runJavaScript()
```

### 4.3 测试框架(testfwk)子系统

**位置**: `references/subsystems/testfwk/`

**配置文件**:
- `_common.md` - 测试框架(testfwk)通用配置
- `uitest.md` - UiTest 模块
- `JsUnit.md` - JsUnit 模块
- `perftest.md` - PerfTest 模块

**使用方式**:
```
子系统: 测试框架(testfwk)
模块: UiTest
API: Driver.create()
```

### 4.4 ArkTS 子系统

**位置**: `references/subsystems/ArkTS/`

**特殊规则**: string 空字符串是合法参数，不会抛出错误码 401

**使用方式**:
```
子系统: ArkTS
API: ArkTS 特有语法
```

---

## 五、创建新子系统配置

### 5.1 创建步骤

#### 步骤1：创建子系统目录

```bash
mkdir -p references/subsystems/{SubsystemName}
```

**示例**:
```bash
mkdir -p references/subsystems/Multimedia
```

#### 步骤2：创建子系统通用配置

创建文件: `references/subsystems/{SubsystemName}/_common.md`

**最小模板**:
```markdown
# {子系统名称} 子系统通用配置

> **子系统信息**
> - 名称: {子系统英文名}
> - Kit包: @kit.{KitName}
> - 测试路径: test/xts/acts/{子系统}/
> - 版本: 1.0.0
> - 更新日期: 2026-02-05

## 一、子系统通用配置

### 1.1 API Kit 映射

```typescript
import { APIName } from '@kit.{KitName}';
```

### 1.2 测试路径规范

- 测试用例目录: `test/xts/acts/{子系统}/test/`

### 1.3 模块映射配置

| 模块名称 | API 声明文件 | 说明 |
|---------|-------------|------|
| Module1 | @ohos.module1.d.ts | 模块1说明 |
| Module2 | @ohos.module2.d.ts | 模块2说明 |

## 二、子系统通用测试规则

[适用于该子系统所有模块的测试规则]

## 三、参考资料

- [子系统官方文档](${OH_ROOT}/docs/...)
- [API 参考文档](${OH_ROOT}/docs/...)
```

#### 步骤3：创建模块配置（可选）

创建文件: `references/subsystems/{SubsystemName}/{ModuleName}.md`

**最小模板**:
```markdown
# {模块名称} 模块配置

> **模块信息**
> - 所属子系统: {子系统名称}
> - 模块名称: {模块名称}
> - API 声明文件: @ohos.{模块}.d.ts
> - 版本: 1.0.0

## 一、模块特有配置

### 1.1 模块概述

[模块概述说明]

### 1.2 通用配置继承

本模块继承 {子系统名称} 子系统通用配置：
- **测试路径规范**: 见 `../_common.md` 第 1.2 节
- **通用测试规则**: 见 `../_common.md` 第 2 节

## 二、模块特有 API 列表

| API名称 | 说明 | 优先级 |
|---------|------|--------|
| API1 | API说明 | LEVEL0 |
```

### 5.2 快速创建脚本

**示例1：创建 Multimedia 子系统**

```bash
#!/bin/bash
SUBSYSTEM="Multimedia"
KIT="Multimedia"

# 1. 创建目录
mkdir -p references/subsystems/$SUBSYSTEM

# 2. 创建子系统通用配置
cat > references/subsystems/$SUBSYSTEM/_common.md << EOF
# $SUBSYSTEM 子系统通用配置

> **子系统信息**
> - 名称: $SUBSYSTEM
> - Kit包: @kit.$KIT
> - 测试路径: test/xts/acts/$(echo $SUBSYSTEM | tr '[:upper:]' '[:lower:]')/
> - 版本: 1.0.0

## 一、子系统通用配置

### 1.1 模块映射配置

| 模块名称 | API 声明文件 | 说明 |
|---------|-------------|------|
| Audio | @ohos.multimedia.audio.d.ts | 音频模块 |
| Image | @ohos.multimedia.image.d.ts | 图像模块 |
EOF

echo "✅ $SUBSYSTEM 子系统配置创建完成"
```

---

## 六、配置最佳实践

### 6.1 命名规范

#### 子系统名称
- ✅ 使用大驼峰命名（PascalCase）
- ✅ 与官方文档保持一致
- ✅ 示例：`ArkUI`, `ArkWeb`, `Multimedia`

#### 模块名称
- ✅ 使用大驼峰命名（PascalCase）
- ✅ 与 API 声明文件中的接口名保持一致
- ✅ 示例：`Component`, `Animator`, `Router`

#### 配置文件名称
- ✅ 通用配置：`_common.md`（下划线开头）
- ✅ 模块配置：`{ModuleName}.md`（大驼峰命名）

### 6.2 内容组织原则

#### 通用配置 (`_common.md`)
- 详尽：包含所有基础规范
- 完整：提供完整示例
- 清晰：说明所有字段的含义

#### 子系统配置 (`{Subsystem}/_common.md`)
- 适中：说明子系统的特殊规则
- 引用：引用通用配置的相关章节
- 聚焦：避免重复通用配置

#### 模块配置 (`{Subsystem}/{Module}.md`)
- 精简：列出模块的 API
- 引用：引用子系统配置的相关章节
- 特化：只包含模块特有的内容

### 6.3 引用规范

**标准格式**:
```markdown
详见 `{子系统}/_common.md` 第 {章节号} 节
```

**示例**:
```markdown
详见 `ArkUI/_common.md` 第 1.2 节
```

**配置继承说明**:
```markdown
### 1.3 通用配置继承

本模块继承 {子系统名称} 子系统通用配置：
- **测试路径规范**: 见 `../_common.md` 第 1.2 节
- **通用测试规则**: 见 `../_common.md` 第 2 节
```

### 6.4 版本管理

#### 版本信息格式

```markdown
> **子系统信息**
> - 名称: {子系统英文名}
> - Kit包: @kit.{KitName}
> - 测试路径: test/xts/acts/{子系统}/
> - 版本: 1.0.0
> - 更新日期: 2026-02-05
```

#### 版本历史记录

```markdown
## 六、版本历史

- **v1.0.0** (2026-02-05):
  - 初始版本
  - 包含基础配置
- **v1.1.0** (2026-02-06):
  - 新增 XXX 模块配置
  - 优化测试规则
```

---

## 七、常见问题

### Q1: 如何确定是否需要创建新的子系统配置？

**A**:

**需要创建**:
- ✅ 子系统有独特的 Kit 包（如 `@kit.ArkUI`）
- ✅ 子系统有特殊的测试规则
- ✅ 子系统包含多个模块，需要模块级配置

**不需要创建**:
- ❌ 子系统完全遵循通用配置
- ❌ 只是为个别 API 生成测试用例

### Q2: 子系统配置和模块配置有什么区别？

**A**:

| 配置类型 | 作用范围 | 文件位置 | 内容 |
|---------|---------|---------|------|
| **子系统配置** | 整个子系统 | `{Subsystem}/_common.md` | 子系统通用规则、模块映射表 |
| **模块配置** | 特定模块 | `{Subsystem}/{Module}.md` | 模块特有规则、API列表 |

### Q3: 如何处理配置冲突？

**A**: 配置优先级规则：

```
用户自定义配置 > 子系统配置 > 通用配置
```

子系统配置可以覆盖通用配置，在子系统配置中明确定义自己的规则。

### Q4: 配置文件应该多详细？

**A**:

- **通用配置**: 详尽，包含所有基础规范和完整示例
- **子系统配置**: 适中，说明特殊规则和引用通用配置
- **模块配置**: 精简，列出 API 和特有规则，引用上级配置

### Q5: 如何维护配置一致性？

**A**:

1. **统一命名规范**：PascalCase 命名
2. **统一文件结构**：相同的章节结构
3. **统一引用方式**：标准引用格式
4. **版本管理**：每次修改都更新版本号

---

**文档版本**: 2.0.0
**创建日期**: 2026-02-05
**最后更新**: 2026-02-05
**维护者**: xts-generator Team

## 更新历史

- **v2.0.0** (2026-02-05): 重新整理文件结构，删除重复内容
  - 简化配置文件类型说明，删除重复示例
  - 精简已有子系统配置章节
  - 优化创建新子系统配置步骤
  - 删除冗余的最佳实践说明
  - 添加快速创建脚本示例

- **v1.0.0** (2026-02-05): 初始版本
