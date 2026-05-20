---
keyword: name
synonyms: []
related: []
category: compiler-feature
---

# Name

## 中文描述
name 是仓颉编译器中的一个重要概念。

## English Description
name is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, chir, codegen, conditionalcompilation, demangler
- 主要类: NameReferenceExpr, NameReferenceExpr, CmpTyByName, GetElementByName, StoreElementByName
- 主要函数: GetFunctionName, GetGenericConstraintsName, DemangleQualifiedName, DemanglePackageName, DemangleStringName

## 代码示例

### 示例 1: GetFunctionName
文件: `demangler/Demangler.h:154`

```cpp
// 代码示例待提取
```

### 示例 2: GetGenericConstraintsName
文件: `demangler/Demangler.h:155`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: ast, chir, codegen, conditionalcompilation, demangler, driver, frontend, frontendtool, include, incrementalcompilation

## 常见问题

### name 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 name？

请参考上面的代码示例部分。

### name 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
