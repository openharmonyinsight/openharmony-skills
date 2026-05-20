---
keyword: type-inference
synonyms: [类型推断, type inference, 类型推导, type deduction, infer, 推断]
related: [type, generic, lambda, var, 类型系统]
category: compiler-feature
---

# 类型推断 (Type Inference)

## 中文描述
类型推断是编译器根据上下文自动推导变量或表达式类型的能力。在仓颉语言中,类型推断用于 var 声明、lambda 表达式参数、泛型类型参数等场景,减少冗余的类型标注。

## English Description
Type inference is the compiler's ability to automatically deduce the type of variables or expressions from context. In Cangjie language, type inference is used for var declarations, lambda expression parameters, generic type arguments, etc., reducing redundant type annotations.

## 使用场景
- var 变量声明的类型推断
- lambda 表达式参数类型推断
- 泛型类型参数推断
- 函数返回类型推断
- 表达式类型推断

## 相关实现
- 类型推断算法在 Sema/TypeInference.cpp
- 约束求解(constraint solving)
- 统一算法(unification algorithm)
- 类型变量(type variables)

## 概念关系图谱

- **同义词**: 类型推断, type inference, 类型推导, type deduction, infer, 推断
- **相关概念**: type, generic, lambda, var, 类型系统
- **相关模块**: 无

## 常见问题

### type-inference 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 type-inference？

请参考下面的代码示例部分。

### type-inference 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

