---
name: harmonyos-evolution
description: 当构建成功后需要记录重难点，或构建失败时需要查询已知问题时，使用此 Skill 管理 Evolution.md 文件。此 Skill
  负责追踪并分析构建失败日志，将重难点解决方案沉淀至 Evolution.md，打造专属知识库，拒绝重复踩坑。只有在构建成功后才能将新问题添加到
  Evolution.md。
descriptionZH: 当构建成功后需要记录重难点，或构建失败时需要查询已知问题时，使用此 Skill 管理 Evolution.md 文件。此
  Skill 负责追踪并分析构建失败日志，将重难点解决方案沉淀至 Evolution.md，打造专属知识库，拒绝重复踩坑。只有在构建成功后才能将新问题添加到
  Evolution.md。
tags:
  - 鸿蒙
  - 问题追踪
  - Evolution
  - HarmonyOS
---

# 鸿蒙应用迭代和进化机制 Skill

## 目的

追踪并分析构建失败日志，将重难点解决方案沉淀至 Evolution.md，打造专属知识库，避免重复踩坑。

## ⚠️ 重要原则

**只有在构建成功后才能更新 Evolution.md**

- 修复方案必须先验证（构建成功）
- 构建失败的方案不能记录（说明方案错误）
- 用户自行构建成功后，才能确认问题解决有效

## 📝 Evolution.md 位置

Evolution.md 位于 skills 目录中：`skills/utils/Evolution.md`

> **重要**: Evolution.md 位于 skills 目录中，这样当技能迁移到其他项目时，历史问题记录也会一起迁移。

## 🔍 查询已知问题

当构建失败时，首先使用本 Skill 查询 Evolution.md 中是否有相同问题的记录。

### 查询流程

1. **读取 Evolution.md 文件**
2. **搜索报错中的关键词**（如错误类型、相关API名称）
3. **对比错误描述是否匹配**
4. **如果匹配，直接应用已记录的解决方案**
5. **不要再进行 L3 搜索**，直接修复

### 查询示例

```
用户报错: error: undeclared identifier 'toUInt32'
↓
Step 1: 检查 Evolution.md（使用本 Skill）
    ✓ 搜索关键词: "toUInt32", "类型转换", "未定义标识符"
    ✓ 找到记录 #14: 类型转换方法不存在
    ✓ 解决方案: 使用 UInt32(e) 替代 ch.toUInt32()
    ✓ 直接应用修复，跳过 L3 搜索
↓
重新构建 → ✅ BUILD SUCCESSFUL
✓ 构建成功，方案验证有效
```

## 📝 记录新问题

**每次构建成功后，必须执行以下操作**：

1. 将本次开发过程中遇到的**重难点**整理成几点
2. 写入 skills 目录下的 `Evolution.md` 文件（即 `skills/utils/Evolution.md`）
3. 记录内容包括：问题描述、错误代码、原因分析、解决方案、正确代码示例

### Evolution.md 预期格式

```markdown
# Evolution - 项目重难点记录

## 项目: [项目名称]
### 构建日期: YYYY-MM-DD

## 重难点记录

### 1. [问题标题]
**问题描述**: [描述]
**错误代码**: ```cangjie [代码] ```
**原因分析**: [说明]
**解决方案**: [说明]
**正确语法**: ```cangjie [代码] ```

### 2. [问题标题]
**日期**: MM-DD
**现象**: [错误信息]
**原因**: [原因说明]
**解决方案**: [解决方案]
**正确语法**: ```cangjie [代码] ```
```

### 记录示例

```markdown
### 14. 类型转换方法不存在
**日期**: 02-25
**现象**: `error: undeclared identifier 'toUInt32'`, `error: undeclared identifier 'toInt64'`
**原因**: 仓颉语言中类型转换使用 `T(e)` 语法，而不是 `e.toT()` 方法调用
**解决方案**: 使用类型构造函数进行转换
**正确语法**:
```cangjie
// 错误
let charValue = ch.toUInt32()
let intPart = absValue.toInt64()

// 正确
let charValue = UInt32(ch)
let intPart = Int64(absValue)
```

**支持的数值类型转换**:
- `Int64(e)`, `Int32(e)`, `Int16(e)`, `Int8(e)`
- `UInt64(e)`, `UInt32(e)`, `UInt16(e)`, `UInt8(e)`
- `Float64(e)`, `Float32(e)`, `Float16(e)`

**Rune 转换**:
```cangjie
let x: Rune = 'a'
let r1 = UInt32(x)  // Rune 到 UInt32
let r2 = Rune(65)   // Int64 到 Rune
```
```

## 🚨 构建失败处理流程

当构建失败时，必须严格按照以下优先级流程处理：

```
获得详细报错信息
    ↓
Step 1: 检查 Evolution.md (优先级最高) - 使用本 Skill
    ↓
    ├─ 找到相同问题 → 应用已验证的解决方案 → 重新构建
    │
    └─ 未找到/无法解决 → 继续 Step 2
         ↓
Step 2: L3 本地文档搜索 - 使用 harmonyos-doc-search-guide skill
    ↓
    ├─ 找到解决方案 → 修复代码 → 重新构建 → 构建成功则更新 Evolution.md（使用本 Skill）
    │
    │                             ↓
    │                        构建失败则重新判断报错信息是否充足，重新修正方案
    │
    └─ 未找到 → 明确告知"该功能可能不支持"
```

### Step 1 - 检查 Evolution.md 的执行要点

1. 使用本 Skill 读取 `Evolution.md` 文件
2. 搜索报错中的关键词（如错误类型、相关API名称）
3. 对比错误描述是否匹配
4. 如果匹配，直接应用已记录的解决方案
5. **不要再进行 L3 搜索**，直接修复

### Step 2 - 记录新问题的执行要点

1. 仅在构建成功后，才将新问题添加到 Evolution.md
2. 如果构建失败，说明方案错误，不能记录，需要重新根据报错信息寻找解决方案
3. 使用本 Skill 将问题记录到 Evolution.md

## 📋 常见问题类型

以下是一些常见的问题类型，可以在 Evolution.md 中查找：

### 类型转换问题
- `toUInt32`, `toInt64` 等方法不存在
- 使用 `UInt32(e)` 替代 `e.toUInt32()`

### UI组件问题
- `@Component` 的 `build` 方法只能编写 UI 组件语法
- 不支持三元运算符，使用 `if` 表达式
- `.onClick` 事件语法格式错误

### 字符串处理问题
- `String[Int64]` 下标访问返回 `UInt8` 类型
- `String.isEmpty` 不是属性，使用 `.size == 0`

### 布局问题
- `.height(100.percent)` 导致子元素占满全部空间
- 使用 `.layoutWeight()` 替代 `.height()` 进行灵活布局

### 导入问题
- `Entry/Component/State` 未声明
- 需要添加正确的导入语句

## 工作流程

1. **需求分析**（已完成）- 使用 `harmonyos-requirement-analysis` skill
2. **使用 skill-B skills**（已完成）- 先使用 `skills/` 中的仓颉语言 skills
3. **L1 查询**（已完成）- 如需进一步查询，使用 `harmonyos-vec-retriever-guide` skill
4. **L3 查询**（已完成）- 如需本地文档搜索，使用 `harmonyos-doc-search-guide` skill
5. **构建**（已完成）- 使用 `harmonyos-build` skill 进行项目构建
6. **迭代进化**（本 Skill）- 使用本 Skill 记录和解决问题

## ✅ 最佳实践

1. **构建成功后才记录** - 只有构建成功的问题解决方案才能记录
2. **详细记录** - 包含问题描述、错误代码、原因分析、解决方案、正确代码示例
3. **关键词搜索** - 使用错误类型、API名称等关键词便于后续查找
4. **分类整理** - 按项目、日期等维度整理，便于查找
5. **及时更新** - 每次构建成功后及时更新，避免遗忘
