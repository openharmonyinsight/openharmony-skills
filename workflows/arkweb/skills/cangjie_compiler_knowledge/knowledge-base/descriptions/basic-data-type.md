---
keyword: basic-data-type
synonyms: [基础数据类型, basic data types, primitive types, int, float, bool, rune, 整数, 浮点, 布尔, 字符, 原始类型]
related: [type-system, const, string, literal]
category: language-feature
---

# 基础数据类型 (Basic Data Types)

## 中文描述

基础数据类型是仓颉语言提供的内置原始类型，是构建复杂数据结构的基础。仓颉支持以下基础数据类型：

**整数类型**：
- `Int8`, `Int16`, `Int32`, `Int64` - 有符号整数
- `UInt8`, `UInt16`, `UInt32`, `UInt64` - 无符号整数
- `Int` - 平台相关的有符号整数（通常是 Int64）
- `UInt` - 平台相关的无符号整数（通常是 UInt64）

**浮点类型**：
- `Float32` - 32 位浮点数（IEEE 754 单精度）
- `Float64` - 64 位浮点数（IEEE 754 双精度）
- `Float` - 默认浮点类型（通常是 Float64）

**布尔类型**：
- `Bool` - 布尔值，取值为 `true` 或 `false`

**字符类型**：
- `Rune` - Unicode 字符（UTF-32 编码点）

**特殊类型**：
- `Unit` - 空类型，类似于其他语言的 void
- `Nothing` - 底类型，表示永不返回

## English Description

Basic data types are the built-in primitive types provided by the Cangjie language, which are the foundation for building complex data structures. Cangjie supports the following basic data types:

**Integer Types**:
- `Int8`, `Int16`, `Int32`, `Int64` - Signed integers
- `UInt8`, `UInt16`, `UInt32`, `UInt64` - Unsigned integers
- `Int` - Platform-dependent signed integer (usually Int64)
- `UInt` - Platform-dependent unsigned integer (usually UInt64)

**Floating-Point Types**:
- `Float32` - 32-bit floating-point (IEEE 754 single precision)
- `Float64` - 64-bit floating-point (IEEE 754 double precision)
- `Float` - Default floating-point type (usually Float64)

**Boolean Type**:
- `Bool` - Boolean value, either `true` or `false`

**Character Type**:
- `Rune` - Unicode character (UTF-32 code point)

**Special Types**:
- `Unit` - Empty type, similar to void in other languages
- `Nothing` - Bottom type, represents never returns

## 使用场景

- 声明变量和函数参数
- 数值计算和逻辑运算
- 字符和字符串处理
- 类型转换和类型检查
- 作为泛型类型参数

## 相关实现

- **主要模块**: `src/Parse/`, `src/Sema/`, `src/AST/`
- **核心类**:
  - `TypeNode` - 类型节点基类
  - `Type` - 类型系统基类
  - `IntType` - 整数类型
  - `FloatType` - 浮点类型
  - `BoolType` - 布尔类型
  - `RuneType` - 字符类型
- **关键文件**:
  - `src/Parse/ParseType.cpp` - 类型表达式解析
  - `src/Sema/TypeChecker.cpp` - 类型检查
  - `src/AST/Types.cpp` - 类型系统实现
- **关键函数**:
  - `ParseType()` - 解析类型表达式
  - `TypeCheck()` - 类型检查
  - `ConvertType()` - 类型转换
- **相关特性**: type-system, const, string, generic

## 概念关系图谱

- **同义词**: 基础数据类型, basic data types, primitive types, int, float, bool, rune, 整数, 浮点, 布尔, 字符, 原始类型
- **相关概念**: type-system, const, string, literal
- **相关模块**: 无

## 常见问题

### basic-data-type 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 basic-data-type？

请参考下面的代码示例部分。

### basic-data-type 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

