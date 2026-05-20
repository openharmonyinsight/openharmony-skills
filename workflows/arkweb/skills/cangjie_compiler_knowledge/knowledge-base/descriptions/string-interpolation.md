---
keyword: string interpolation
synonyms: [string]
related: [rune, char, 字符, character, 文本, text]
category: compiler-feature
---

# String Interpolation

## 中文描述
String 是仓颉的字符串类型,支持 UTF-8 编码、字符串字面量、字符串插值、多行字符串等特性。字符串是不可变的引用类型。

## English Description
String is Cangjie's string type, supporting UTF-8 encoding, string literals, string interpolation, multi-line strings, etc. Strings are immutable reference types.

## 使用场景
- 待补充

## 相关实现
- 相关模块: ast, basic, chir, codegen, conditionalcompilation
- 主要类: StdString, CStringTy, IntegratedString, StringConvertor, CStringType
- 主要函数: DemangleStringName, UIntToString, DemangleCStringType, SkipString, SkipString

## 代码示例

### 示例 1: DemangleStringName
文件: `demangler/Demangler.h:239`

```cpp
// 代码示例待提取
```

### 示例 2: UIntToString
文件: `demangler/Demangler.h:243`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: string
- **相关概念**: rune, char, 字符, character, 文本, text
- **相关模块**: ast, basic, chir, codegen, conditionalcompilation, demangler, driver, include, incrementalcompilation, lex

## 常见问题

### string interpolation 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 string interpolation？

请参考上面的代码示例部分。

### string interpolation 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
