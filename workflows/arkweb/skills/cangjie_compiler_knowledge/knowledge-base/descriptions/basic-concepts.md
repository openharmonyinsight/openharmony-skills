---
keyword: basic-concepts
synonyms: [基础概念, basic concepts, variable, scope, lifetime, expression, statement, 变量, 作用域, 生命周期, 表达式, 语句]
related: [type-system, declaration, identifier, binding]
category: language-feature
---

# 基础概念 (Basic Concepts)

## 中文描述

基础概念涵盖仓颉语言的核心编程元素，是所有其他语言特性的基础。主要包括：

**变量声明**：
- `let` 声明不可变变量
- `var` 声明可变变量
- 类型注解和类型推断
- 变量初始化

**作用域**：
- 词法作用域（Lexical Scope）
- 块作用域（Block Scope）
- 函数作用域
- 类作用域
- 模块作用域

**生命周期**：
- 变量的生命周期
- 对象的生命周期
- 资源管理（RAII）
- 所有权和借用（如果适用）

**表达式**：
- 字面量表达式
- 标识符表达式
- 运算符表达式（算术、逻辑、比较、位运算）
- 函数调用表达式
- 成员访问表达式
- 索引表达式

**语句**：
- 表达式语句
- 声明语句
- 控制流语句（if, while, for, match）
- 返回语句
- break 和 continue 语句

## English Description

Basic concepts cover the core programming elements of the Cangjie language, which are the foundation for all other language features. Main topics include:

**Variable Declaration**:
- `let` declares immutable variables
- `var` declares mutable variables
- Type annotation and type inference
- Variable initialization

**Scope**:
- Lexical Scope
- Block Scope
- Function scope
- Class scope
- Module scope

**Lifetime**:
- Variable lifetime
- Object lifetime
- Resource management (RAII)
- Ownership and borrowing (if applicable)

**Expressions**:
- Literal expressions
- Identifier expressions
- Operator expressions (arithmetic, logical, comparison, bitwise)
- Function call expressions
- Member access expressions
- Index expressions

**Statements**:
- Expression statements
- Declaration statements
- Control flow statements (if, while, for, match)
- Return statements
- break and continue statements

## 使用场景

- 声明和使用变量
- 理解变量的可见性和生命周期
- 编写表达式和语句
- 控制程序流程
- 管理资源和内存

## 相关实现

- **主要模块**: `src/Lex/`, `src/Parse/`, `src/Sema/`
- **核心类**:
  - `VarDecl` - 变量声明节点
  - `Scope` - 作用域管理
  - `Expr` - 表达式基类
  - `Stmt` - 语句基类
  - `LifetimeAnalyzer` - 生命周期分析器
- **关键文件**:
  - `src/Parse/ParseDecl.cpp` - 声明解析
  - `src/Parse/ParseExpr.cpp` - 表达式解析
  - `src/Parse/ParseStmt.cpp` - 语句解析
  - `src/Sema/` - 作用域和生命周期分析
- **相关特性**: 所有其他语言特性都建立在这些基础概念之上

## 概念关系图谱

- **同义词**: 基础概念, basic concepts, variable, scope, lifetime, expression, statement, 变量, 作用域, 生命周期, 表达式, 语句
- **相关概念**: type-system, declaration, identifier, binding
- **相关模块**: 无

## 常见问题

### basic-concepts 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 basic-concepts？

请参考下面的代码示例部分。

### basic-concepts 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

