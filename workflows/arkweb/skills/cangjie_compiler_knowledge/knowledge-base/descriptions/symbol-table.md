---
keyword: symbol-table
synonyms: [符号表, symbol, 符号, 标识符表, identifier table]
related: [scope, name-resolution, sema]
category: compiler-data-structure
---

# 符号表 (Symbol Table)

## 中文描述

符号表是编译器的核心数据结构，用于存储和查询标识符（变量、函数、类等）的信息。编译器在语义分析阶段构建符号表，记录每个标识符的类型、作用域、定义位置等元数据，用于名称解析和类型检查。

符号表的主要功能：
- 存储标识符的声明信息（名称、类型、属性）
- 管理标识符的作用域和可见性
- 支持快速查找标识符定义
- 检测重复定义和未定义标识符
- 记录符号的使用位置（用于 IDE 功能）

符号表通常采用层次结构，每个作用域对应一个符号表，形成符号表栈或符号表树。

## English Description

Symbol table is a core compiler data structure used to store and query information about identifiers (variables, functions, classes, etc.). The compiler builds the symbol table during semantic analysis, recording metadata such as type, scope, and definition location for each identifier, used for name resolution and type checking.

Main functions of symbol table:
- Store identifier declaration information (name, type, attributes)
- Manage identifier scope and visibility
- Support fast identifier definition lookup
- Detect duplicate definitions and undefined identifiers
- Record symbol usage locations (for IDE features)

Symbol tables typically use a hierarchical structure, with each scope corresponding to a symbol table, forming a symbol table stack or tree.

## 使用场景

- 名称解析：查找标识符的定义
- 类型检查：获取标识符的类型信息
- 作用域管理：处理标识符的可见性
- 错误检测：检测重复定义、未定义标识符
- IDE 支持：提供符号跳转、自动补全等功能

## 相关实现

- **主要模块**: `src/Sema/`
- **核心类**:
  - `Symbol` - 符号基类
  - `SymbolApi` - 符号 API
  - `Collector` - 符号收集器
  - `ScopeManager` - 作用域管理器
- **关键文件**:
  - `src/AST/Symbol.h` - 符号定义
  - `src/Sema/ScopeManager.h` - 作用域和符号表管理
- **依赖模块**: AST, Basic
- **被依赖**: Sema, TypeChecker

## 概念关系图谱

- **同义词**: 符号表, symbol, 符号, 标识符表, identifier table
- **相关概念**: scope, name-resolution, sema
- **相关模块**: 无

## 常见问题

### symbol-table 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 symbol-table？

请参考下面的代码示例部分。

### symbol-table 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

