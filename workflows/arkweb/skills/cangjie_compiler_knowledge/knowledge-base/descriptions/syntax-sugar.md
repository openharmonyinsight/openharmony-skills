---
keyword: syntax-sugar
synonyms: [语法糖, syntactic sugar, sugar, 糖, 语法便利]
related: [desugaring, parser, enum, sema]
category: compiler-feature
---

# 语法糖 (Syntax Sugar)

## 中文描述

语法糖是编程语言提供的便捷语法形式，在编译器内部会被转换为更基础的语法结构。仓颉编译器在解析和语义分析阶段识别语法糖，并通过去糖化过程将其转换为标准形式。

语法糖的主要特点：
- 提供更简洁、易读的语法形式
- 在编译器内部转换为基础语法结构
- 不改变语言的表达能力，只是提供便利
- 简化常见编程模式的书写

仓颉编译器中的语法糖示例：
- 枚举的某些语法形式（由 EnumSugarChecker 处理）
- 运算符重载的语法形式
- 字面量的便捷表示
- 控制流的简化语法

编译器在语义分析阶段识别和检查语法糖的合法性，然后通过去糖化将其转换为标准的 AST 节点，简化后续的类型检查和代码生成。

## English Description

Syntax sugar is a convenient syntax form provided by programming languages, which is internally converted to more basic syntax structures by the compiler. The Cangjie compiler identifies syntax sugar during parsing and semantic analysis, and converts it to standard form through the desugaring process.

Main characteristics of syntax sugar:
- Provides more concise and readable syntax forms
- Converted to basic syntax structures internally in the compiler
- Does not change the language's expressive power, only provides convenience
- Simplifies writing of common programming patterns

Examples of syntax sugar in Cangjie compiler:
- Certain enum syntax forms (handled by EnumSugarChecker)
- Operator overloading syntax forms
- Convenient literal representations
- Simplified control flow syntax

The compiler identifies and checks the legality of syntax sugar during semantic analysis, then converts it to standard AST nodes through desugaring, simplifying subsequent type checking and code generation.

## 使用场景

- 枚举语法糖（简化枚举成员访问）
- 运算符重载语法糖（如 `a + b` 转换为 `a.add(b)`）
- 字面量语法糖（如数组字面量、字符串插值）
- 控制流语法糖（如 for-in 循环）
- 模式匹配语法糖

## 相关实现

- **主要模块**: `src/Sema/`
- **核心类**:
  - `EnumSugarChecker` - 枚举语法糖检查器
  - `SugarAnalyzer` - 语法糖分析器
- **关键文件**:
  - `src/Sema/EnumSugarChecker.cpp` - 枚举语法糖检查
  - `src/Sema/EnumSugarChecker.h` - 枚举语法糖检查器定义
- **依赖模块**: AST, Parser, Sema
- **被依赖**: Desugaring, TypeChecker

## 概念关系图谱

- **同义词**: 语法糖, syntactic sugar, sugar, 糖, 语法便利
- **相关概念**: desugaring, parser, enum, sema
- **相关模块**: 无

## 常见问题

### syntax-sugar 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 syntax-sugar？

请参考下面的代码示例部分。

### syntax-sugar 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

