---
keyword: value
synonyms: []
related: []
category: compiler-feature
---

# Value

## 中文描述
value 是仓颉编译器中的一个重要概念。

## English Description
value is an important concept in the Cangjie compiler.

## 使用场景
- 待补充

## 相关实现
- 相关模块: chir, codegen, include, lex, option
- 主要类: LeftValueInfo, ConstValue, TypeValue, ValueRange, ValueAnalysis
- 主要函数: SetValue, SetWrappingValue, SetSaturatingValue, GetValue, GetAbsValue

## 代码示例

### 示例 1: SetValue
文件: `include/cangjie/AST/Identifier.h:140`

```cpp
// 代码示例待提取
```

### 示例 2: SetWrappingValue
文件: `include/cangjie/AST/IntLiteral.h:84`

```cpp
// 代码示例待提取
```


## 概念关系图谱

- **同义词**: 无
- **相关概念**: 无
- **相关模块**: chir, codegen, include, lex, option, parse, sema, unittests

## 常见问题

### value 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 value？

请参考上面的代码示例部分。

### value 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。
