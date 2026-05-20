---
keyword: type
synonyms: []
related: []
category: compiler-feature
---

# Type

## 中文描述
type 是仓颉编译器中的一个重要概念。

## English Description
type is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, basic, chir, codegen, conditionalcompilation
- 主要类: TypeCheckCache, Type, InvalidType, RefType, ThisType
- 主要函数: GetReturnType, DemangleClassType, DemangleCFuncType, DemangleCStringType, DemangleGenericType

## 代码示例

### 示例 1: GetReturnType
文件: `demangler/Demangler.h:134`

```cpp
// 代码示例待提取
```

### 示例 2: DemangleClassType
文件: `demangler/Demangler.h:213`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: ast, basic, chir, codegen, conditionalcompilation, demangler, driver, frontend, include, incrementalcompilation

## 常见问题

### type 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 type？

请参考上面的代码示例部分。

### type 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
