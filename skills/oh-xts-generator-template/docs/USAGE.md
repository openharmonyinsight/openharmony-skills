# 使用方式详解

> **oh-xts-generator-template** - 完整使用指南

## 快速导航

- [使用方式对比](#使用方式对比)
- [方式1：通用模板](#方式1通用模板推荐新手)
- [方式2：子系统配置](#方式2子系统配置推荐)
- [方式3：自定义配置](#方式3自定义配置)
- [常见使用场景](#常见使用场景)
- [常见问题](#常见问题)

---

## 使用方式对比

| 使用方式 | 适用场景 | 配置需求 | 灵活性 |
|---------|---------|---------|-------|
| **方式1：通用模板** | 新手、简单任务 | 无 | 低 |
| **方式2：子系统配置** | 大多数任务 | 子系统配置文件 | 中 |
| **方式3：自定义配置** | 高级用户、特殊需求 | 每次使用时指定 | 高 |

### 选择建议

- **新手** → 方式1（通用模板）
- **大多数情况** → 方式2（子系统配置）【推荐】
- **特殊需求** → 方式3（自定义配置）

---

## 方式1：通用模板（推荐新手）

### 适用场景

- ✅ 新手首次使用
- ✅ 子系统没有配置文件
- ✅ 快速生成测试用例
- ✅ 简单的 API 测试

### 使用格式

```markdown
请使用 oh-xts-generator-template 为以下 API 生成测试用例：

子系统: {子系统名称}
API: {API名称}
定义文件: {API声明文件路径}
```

### 使用示例

**示例1：为 ArkUI Component 生成测试**

```markdown
请使用 oh-xts-generator-template 为以下 API 生成测试用例：

子系统: ArkUI
API: Component.onClick()
定义文件: interface/sdk-js/api/@ohos.arkui.d.ts
```

### 优缺点

**优点**:
- ✅ 简单直接，无需了解配置系统
- ✅ 适合快速生成测试用例

**缺点**:
- ❌ 无法利用子系统特有规则

### 输出说明

使用通用模板时，技能会：
1. 使用通用配置（`references/subsystems/_common.md`）
2. **同步生成测试设计文档**：`{测试文件名}.design.md`

---

## 方式2：子系统配置（推荐）

### 适用场景

- ✅ 大多数测试生成任务【推荐】
- ✅ 子系统已有配置文件
- ✅ 需要利用子系统特有规则

### 使用格式

```markdown
请使用 oh-xts-generator-template 为 {子系统名称} 子系统生成测试用例：

子系统: {子系统名称}
配置文件: {配置文件路径}
API: {API名称}
```

### 使用示例

**示例1：使用 ArkUI 子系统配置**

```markdown
请使用 oh-xts-generator-template 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
```

**示例2：使用 ArkTS 子系统配置（特殊规则）**

```markdown
请使用 oh-xts-generator-template 为 ArkTS 子系统生成测试用例：

子系统: ArkTS
配置文件: references/subsystems/ArkTS/_common.md
API: ArkTS 特有语法
```

### 配置文件查找

```
用户指定路径 → 子系统配置路径 → 通用配置（兜底）
```

### 优缺点

**优点**:
- ✅ 利用子系统特有规则
- ✅ 配置可重用，提高一致性

**缺点**:
- ❌ 需要子系统配置文件

---

## 方式3：自定义配置

### 适用场景

- ✅ 高级用户
- ✅ 子系统没有配置文件且不想创建
- ✅ 有特殊的测试需求

### 使用格式

```markdown
请使用 oh-xts-generator-template 生成测试用例，使用自定义配置：

子系统: {子系统名称}
自定义配置:
  Kit包: @kit.{KitName}
  测试路径: {测试路径}
  API声明: {API声明文件路径}
  {其他配置项}

API: {API名称}
```

### 自定义配置项

| 配置项 | 类型 | 必需 | 说明 |
|-------|------|------|------|
| `Kit包` | string | ✅ | 子系统的 Kit 包名 |
| `测试路径` | string | ✅ | 测试用例的存放路径 |
| `API声明` | string | ✅ | API 声明文件的路径 |
| `测试级别` | string | ❌ | 默认测试级别（Level0-Level4） |
| `测试类型` | string | ❌ | 默认测试类型 |
| `特殊规则` | list | ❌ | 子系统特有的测试规则 |
| `代码模板` | string | ❌ | 自定义代码模板 |

### 使用示例

```markdown
请使用 oh-xts-generator-template 生成测试用例，使用自定义配置：

子系统: CustomSubsystem
自定义配置:
  Kit包: @kit.CustomKit
  测试路径: test/xts/acts/custom/
  API声明: interface/sdk-js/api/@ohos.custom.d.ts

API: customAPI.method()
```

---

## 常见使用场景

### 场景1：为新 API 生成测试

**推荐方式**: 方式2（子系统配置）

```markdown
请使用 oh-xts-generator-template 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onAppear()

要求:
- 生成参数测试
- 生成错误码测试
```

### 场景2：补充缺失的测试用例

**推荐方式**: 方式2（子系统配置）+ 覆盖分析

```markdown
请使用 oh-xts-generator-template 分析 ArkUI 子系统的测试覆盖情况：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
测试套路径: test/xts/acts/arkui/uitest/

要求:
- 分析哪些 API 还没有测试覆盖
- 为未覆盖的 API 生成测试用例
- 输出测试覆盖统计
```

### 场景3：批量生成测试用例

**推荐方式**: 方式2（子系统配置）+ 列表

```markdown
请使用 oh-xts-generator-template 为以下 API 批量生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md

API 列表:
1. Component.onClick()
2. Component.onAppear()
3. Component.onDisAppear()
```

---

## 常见问题

### Q1: 哪种使用方式最好？

**A**: 没有绝对的"最好"，只有"最适合"：
- **新手**：推荐方式1（通用模板）
- **大多数情况**：推荐方式2（子系统配置）【推荐】
- **特殊需求**：推荐方式3（自定义配置）

### Q2: 如何指定测试套路径？

**A**: 添加"测试套路径"参数：

```markdown
请使用 oh-xts-generator-template 为 ArkUI 子系统生成测试用例：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
API: Component.onClick()
测试套路径: test/xts/acts/arkui/uitest/
```

### Q3: 如何分析测试覆盖情况？

**A**: 添加"测试覆盖分析"要求：

```markdown
请使用 oh-xts-generator-template 分析 ArkUI 子系统的测试覆盖情况：

子系统: ArkUI
配置文件: references/subsystems/ArkUI/_common.md
测试套路径: test/xts/acts/arkui/uitest/

要求:
- 分析测试覆盖情况
- 输出测试覆盖统计
```

### Q4: 如果子系统没有配置文件怎么办？

**A**: 有三种选择：

**选项1：使用通用模板（方式1）**
**选项2：使用自定义配置（方式3）**
**选项3：创建子系统配置文件**（推荐长期使用）

> 📌 **创建配置文件见**：[docs/CONFIG.md](./CONFIG.md)

### Q5: 生成的测试用例在哪里？

**A**: 取决于测试套路径：
- **默认路径**: `test/xts/acts/{子系统}/{测试套}/`
- **指定路径**: 使用时指定的"测试套路径"

> 📌 **更多问题见**：[docs/TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

---

## 常用参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `子系统` | 子系统名称 | `ArkTS`, `Ability`, `testfwk` |
| `配置文件` | 配置文件路径 | `references/subsystems/testfwk/_common.md` |
| `API` | API 名称 | `Component.onClick()` |
| `定义文件` | API 声明文件 | `interface/sdk-js/api/@ohos.UiTest.d.ts` |
| `测试套路径` | 测试套路径 | `test/xts/acts/arkui/uitest/` |
| `测试级别` | 测试级别 | `Level0` - `Level4` |
| `测试类型` | 测试类型 | `Function`, `Performance`, `Reliability`, `Security` |

---

**文档版本**: 2.0.0
**创建日期**: 2026-02-05
**最后更新**: 2026-02-11
**维护者**: oh-xts-generator-template Team
