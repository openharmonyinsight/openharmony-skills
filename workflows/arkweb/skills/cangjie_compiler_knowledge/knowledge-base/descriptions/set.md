---
keyword: set
synonyms: []
related: []
category: compiler-feature
---

# Set

## 中文描述
set 是仓颉编译器中的一个重要概念。

## English Description
set is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, basic, chir, codegen, demangler
- 主要类: FeaturesSet, PSet, UnicodeCharSet, TemporarilySetDebugLocInThisScope
- 主要函数: setGenericVec, DemangleData::SetPrivateDeclaration, SetPrivateDeclaration, SetIsClonedSourceCode, SetValue

## 代码示例

### 示例 1: setGenericVec
文件: `demangler/Demangler.h:234`

```cpp
// 代码示例待提取
```

### 示例 2: DemangleData::SetPrivateDeclaration
文件: `demangler/CangjieDemangle.cpp:26`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: ast, basic, chir, codegen, demangler, driver, frontend, include, incrementalcompilation, lex

## 常见问题

### set 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 set？

请参考上面的代码示例部分。

### set 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
