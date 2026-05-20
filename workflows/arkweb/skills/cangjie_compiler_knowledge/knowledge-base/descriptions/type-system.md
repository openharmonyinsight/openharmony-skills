---
keyword: type-system
synonyms: [类型系统, type system, 类型检查, type checking, 类型安全, type safety, 子类型, subtype]
related: [type-inference, generic, class, interface, 类型转换, type conversion]
category: compiler-feature
---

# 类型系统 (Type System)

## 中文描述
仓颉采用静态强类型系统,在编译期进行类型检查。支持类型推断、泛型、子类型关系、类型转换等特性,确保类型安全。

## English Description
Cangjie uses a static strong type system with compile-time type checking. Supports type inference, generics, subtype relationships, type conversions, etc., ensuring type safety.

## 使用场景
- 编译期类型检查
- 类型推断
- 子类型判断
- 类型转换验证

## 相关实现
- 核心类型检查器在 Sema/TypeChecker.cpp
- 类型兼容性检查在 Sema/TypeCheckType.cpp
- 类型推断在 Sema/TypeInference.cpp
- 关键类: TypeChecker, TypeManager, SubtypeChecker

## 概念关系图谱

- **同义词**: 类型系统, type system, 类型检查, type checking, 类型安全, type safety, 子类型, subtype
- **相关概念**: type-inference, generic, class, interface, 类型转换, type conversion
- **相关模块**: 无

## 常见问题

### type-system 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 type-system？

请参考下面的代码示例部分。

### type-system 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

