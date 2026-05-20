---
keyword: name-resolution
synonyms: [名称解析, 符号解析, symbol resolution, identifier resolution, 标识符解析, lookup]
related: [symbol-table, scope, sema, type-checking]
category: compiler-algorithm
---

# 名称解析 (Name Resolution)

## 中文描述

名称解析是编译器将标识符引用（如变量名、函数名）关联到其定义的过程。编译器根据作用域规则，在符号表中查找标识符，解析其类型和定义位置。名称解析是语义分析的核心步骤，为类型检查提供基础。

名称解析的主要任务：
- 解析标识符引用到声明
- 处理作用域规则（词法作用域、块作用域）
- 处理名称遮蔽（shadowing）
- 解析限定名（qualified names，如 `package.Class.method`）
- 处理导入的符号
- 检测未定义标识符错误

名称解析算法通常采用作用域链查找，从当前作用域开始，逐层向外查找，直到找到匹配的定义或到达全局作用域。

## English Description

Name resolution is the compiler process of associating identifier references (such as variable names, function names) with their definitions. The compiler looks up identifiers in the symbol table according to scope rules, resolving their types and definition locations. Name resolution is a core step in semantic analysis, providing the foundation for type checking.

Main tasks of name resolution:
- Resolve identifier references to declarations
- Handle scope rules (lexical scope, block scope)
- Handle name shadowing
- Resolve qualified names (e.g., `package.Class.method`)
- Handle imported symbols
- Detect undefined identifier errors

Name resolution algorithms typically use scope chain lookup, starting from the current scope and searching outward layer by layer until a matching definition is found or the global scope is reached.

## 使用场景

- 解析变量引用到变量定义
- 解析函数调用到函数声明
- 解析类型名到类型定义
- 处理导入的符号
- 解析成员访问表达式
- 处理泛型类型参数

## 相关实现

- **主要模块**: `src/Sema/`
- **核心类**:
  - `NameReferenceExpr` - 名称引用表达式
  - `ScopeManager` - 作用域管理器
  - `LookUpImpl` - 查找实现
- **关键函数**:
  - `ResolveIdentifier()` - 解析标识符
  - `LookupName()` - 查找名称
  - `ResolveMemberAccess()` - 解析成员访问
- **关键文件**:
  - `src/Sema/LookUpImpl.cpp` - 名称查找实现
  - `src/Sema/ScopeManager.h` - 作用域管理
- **依赖模块**: AST, Symbol Table
- **被依赖**: TypeChecker, Sema

## 概念关系图谱

- **同义词**: 名称解析, 符号解析, symbol resolution, identifier resolution, 标识符解析, lookup
- **相关概念**: symbol-table, scope, sema, type-checking
- **相关模块**: 无

## 常见问题

### name-resolution 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 name-resolution？

请参考下面的代码示例部分。

### name-resolution 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

