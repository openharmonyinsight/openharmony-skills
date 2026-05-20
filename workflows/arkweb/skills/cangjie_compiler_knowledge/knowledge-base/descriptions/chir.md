---
keyword: chir
synonyms: [中间表示, intermediate representation, IR, CHIR, 中间代码]
related: [ast, codegen, optimization, llvm]
category: compiler-module
---

# CHIR (Cangjie High-level Intermediate Representation)

## 中文描述

CHIR 是仓颉编译器的高级中间表示，位于 AST 和 LLVM IR 之间。CHIR 提供了一个平台无关的中间层，用于表示经过语义分析和类型检查后的程序。CHIR 的设计目标是：
- 保留足够的高级语义信息以支持优化
- 简化代码生成的复杂度
- 支持多目标平台的代码生成
- 便于实现编译器优化

CHIR 包含的主要元素：
- 类型化的表达式和语句
- 控制流图（CFG）
- 函数调用图
- 内存操作的显式表示
- 异常处理的结构化表示

## English Description

CHIR is the high-level intermediate representation of the Cangjie compiler, positioned between AST and LLVM IR. CHIR provides a platform-independent intermediate layer for representing programs after semantic analysis and type checking. CHIR's design goals are:
- Retain sufficient high-level semantic information to support optimization
- Simplify code generation complexity
- Support code generation for multiple target platforms
- Facilitate compiler optimizations

Main elements in CHIR:
- Typed expressions and statements
- Control Flow Graph (CFG)
- Function call graph
- Explicit representation of memory operations
- Structured representation of exception handling

## 使用场景

- 语义分析后将 AST 转换为 CHIR
- 在 CHIR 层面进行高级优化（内联、常量折叠等）
- 从 CHIR 生成 LLVM IR 或其他目标代码
- 支持跨平台编译
- 实现增量编译和模块化编译

## 相关实现

- **主要模块**: `src/CHIR/`
- **核心概念**:
  - CHIR 节点类型
  - 控制流图构建
  - 数据流分析
  - 优化 pass
- **依赖模块**: AST, Sema
- **被依赖**: CodeGen
- **相关文件**: `schema/BCHIRFormat.fbs` - CHIR 序列化格式定义

## 代码示例

### 示例 1: AST2CHIRCheckValue
文件: `include/cangjie/CHIR/AST2CHIR/AST2CHIRChecker.h:18`

```cpp
bool AST2CHIRCheckValue(const AST::Node& astNode, const Value& chirNode);
} // namespace Cangjie::CHIR

#endif
```

### 示例 2: DEFINE_CHIR_TYPE_MAPPING
文件: `include/cangjie/CHIR/AST2CHIR/TranslateASTNode/ExceptionTypeMapping.h:29`

```cpp
DEFINE_CHIR_TYPE_MAPPING(CHIR::Apply);
DEFINE_CHIR_TYPE_MAPPING(CHIR::Invoke);
DEFINE_CHIR_TYPE_MAPPING(CHIR::InvokeStatic);
DEFINE_CHIR_TYPE_MAPPING(CHIR::TypeCast);
DEFINE_CHIR_TYPE_MAPPING(CHIR::Allocate);
DEFINE_CHIR_TYPE_MAPPING(CHIR::Spawn);
DEFINE_CHIR_TYPE_MAPPING(CHIR::Intrinsic);
DEFINE_CHIR_TYPE_MAPPING(CHIR::RawArrayAllocate);

template <> struct CHIRNodeMap<UnaryExpression> {
    using Normal = CHIR::UnaryExpression;
    using Exception = CHIR::IntOpWithException;
};
template <> struct CHIRNodeMap<BinaryExpression> {
    using Normal = CHIR::BinaryExpression;
    using Exception = CHIR::IntOpWithException;
};

template <typename T> using CHIRNodeNormalT = typename CHIRNodeMap<T>::Normal;
template <typename T> using CHIRNodeExceptionT = typename CHIRNodeMap<T>::Exception;
```

### 示例 3: DEFINE_CHIR_TYPE_MAPPING
文件: `include/cangjie/CHIR/AST2CHIR/TranslateASTNode/ExceptionTypeMapping.h:30`

```cpp
DEFINE_CHIR_TYPE_MAPPING(CHIR::Invoke);
DEFINE_CHIR_TYPE_MAPPING(CHIR::InvokeStatic);
DEFINE_CHIR_TYPE_MAPPING(CHIR::TypeCast);
DEFINE_CHIR_TYPE_MAPPING(CHIR::Allocate);
DEFINE_CHIR_TYPE_MAPPING(CHIR::Spawn);
DEFINE_CHIR_TYPE_MAPPING(CHIR::Intrinsic);
DEFINE_CHIR_TYPE_MAPPING(CHIR::RawArrayAllocate);

template <> struct CHIRNodeMap<UnaryExpression> {
    using Normal = CHIR::UnaryExpression;
    using Exception = CHIR::IntOpWithException;
};
template <> struct CHIRNodeMap<BinaryExpression> {
    using Normal = CHIR::BinaryExpression;
    using Exception = CHIR::IntOpWithException;
};

template <typename T> using CHIRNodeNormalT = typename CHIRNodeMap<T>::Normal;
template <typename T> using CHIRNodeExceptionT = typename CHIRNodeMap<T>::Exception;
} // namespace Cangjie::CHIR
```

## 概念关系图谱

- **同义词**: 中间表示, intermediate representation, IR, CHIR, 中间代码
- **相关概念**: ast, codegen, optimization, llvm
- **相关模块**: chir, codegen, frontend, frontendtool, include, incrementalcompilation, main-chir-dis.cpp, option, sema, unittests

## 常见问题

### chir 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 chir？

请参考下面的代码示例部分。

### chir 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

