---
keyword: desugaring
synonyms: [去糖化, desugar, 脱糖, sugar elimination, 语法糖消除]
related: [syntax-sugar, parser, sema, ast]
category: compiler-transformation
---

# 去糖化 (Desugaring)

## 中文描述

去糖化是编译器将语法糖转换为基础语法结构的过程。仓颉编译器在语义分析阶段执行去糖化，将便捷的语法形式转换为标准的 AST 节点，简化后续的类型检查和代码生成。

去糖化的主要功能：
- 将语法糖转换为标准语法结构
- 规范化 AST 表示
- 简化类型检查逻辑
- 统一代码生成接口
- 保持语义等价性

去糖化过程通常在语义分析的早期阶段进行，确保后续的编译阶段只需要处理标准的语法结构，而不需要为每种语法糖编写特殊的处理逻辑。

仓颉编译器中的去糖化管理：
- `DesugarManager` - 通用去糖化管理器
- `JavaDesugarManager` - Java 互操作相关的去糖化
- 各种特定的去糖化器（如枚举、运算符重载等）

## English Description

Desugaring is the compiler process of converting syntax sugar to basic syntax structures. The Cangjie compiler performs desugaring during semantic analysis, converting convenient syntax forms to standard AST nodes, simplifying subsequent type checking and code generation.

Main functions of desugaring:
- Convert syntax sugar to standard syntax structures
- Normalize AST representation
- Simplify type checking logic
- Unify code generation interface
- Maintain semantic equivalence

The desugaring process typically occurs in the early stages of semantic analysis, ensuring that subsequent compilation stages only need to handle standard syntax structures without writing special handling logic for each syntax sugar.

Desugaring management in Cangjie compiler:
- `DesugarManager` - General desugaring manager
- `JavaDesugarManager` - Java interop-related desugaring
- Various specific desugarers (e.g., enum, operator overloading, etc.)

## 使用场景

- 语法糖转换（将便捷语法转换为标准形式）
- AST 规范化（统一 AST 节点类型）
- 简化类型检查（减少需要处理的节点类型）
- 统一代码生成（只需为标准节点生成代码）
- 保持编译器架构清晰

## 相关实现

- **主要模块**: `src/Sema/`
- **核心类**:
  - `DesugarManager` - 去糖化管理器
  - `JavaDesugarManager` - Java 去糖化管理器
- **关键文件**:
  - `src/Sema/DesugarManager.h` - 去糖化管理器定义
  - `src/Sema/DesugarManager.cpp` - 去糖化管理器实现
  - `src/Sema/JavaDesugarManager.h` - Java 去糖化管理器
- **依赖模块**: AST, Sema, Syntax Sugar
- **被依赖**: TypeChecker, CodeGen

## 概念关系图谱

- **同义词**: 去糖化, desugar, 脱糖, sugar elimination, 语法糖消除
- **相关概念**: syntax-sugar, parser, sema, ast
- **相关模块**: 无

## 常见问题

### desugaring 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 desugaring？

请参考下面的代码示例部分。

### desugaring 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

