---
keyword: structure
synonyms: [struct]
related: [class, interface, generic, 成员, member]
category: compiler-feature
---

# Structure

## 中文描述
结构体是仓颉语言中的值类型,用于定义轻量级的数据结构。与类不同,结构体采用值语义,在赋值和传参时会进行拷贝。结构体可以实现接口但不支持继承。

## English Description
Struct is a value type in Cangjie language, used to define lightweight data structures. Unlike classes, structs use value semantics and are copied during assignment and parameter passing. Structs can implement interfaces but do not support inheritance.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, basic, chir, codegen, demangler
- 主要类: DemangleInfo, StdPkgCompare, StdPkgHash, DemangleData, InvertedIndex
- 主要函数: IsStruct, IsStructArray, StructTy, CollectDeclsFromStructDecl, ProcessClassStructVarInits

## 代码示例

### 示例 1: IsStruct
文件: `include/cangjie/AST/Types.h:171`

```cpp
// 代码示例待提取
```

### 示例 2: IsStructArray
文件: `include/cangjie/AST/Types.h:207`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: struct
- **相关概念**: class, interface, generic, 成员, member
- **相关模块**: ast, basic, chir, codegen, demangler, driver, frontend, include, incrementalcompilation, lex

## 常见问题

### structure 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 structure？

请参考上面的代码示例部分。

### structure 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
