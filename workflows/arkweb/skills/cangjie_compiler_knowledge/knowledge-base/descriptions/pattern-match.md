---
keyword: pattern-match
synonyms: [模式匹配, pattern matching, match, 匹配, case, 分支]
related: [enum, option, exhaustiveness, 穷尽性检查]
category: language-feature
---

# 模式匹配 (Pattern Matching)

## 中文描述
模式匹配是一种强大的控制流机制,允许根据值的结构进行分支。仓颉语言支持多种模式:常量模式、变量模式、元组模式、枚举模式等。编译器会进行穷尽性检查,确保所有可能的情况都被处理。

## English Description
Pattern matching is a powerful control flow mechanism that allows branching based on the structure of values. Cangjie language supports various patterns: constant patterns, variable patterns, tuple patterns, enum patterns, etc. The compiler performs exhaustiveness checking to ensure all possible cases are handled.

## 使用场景
- match 表达式
- 枚举类型的解构
- Option 类型的处理
- 元组解构
- 穷尽性检查(exhaustiveness checking)

## 相关实现
- 模式解析在 Parse/ParsePattern.cpp
- 模式类型检查在 Sema/TypeCheckPattern.cpp
- 穷尽性检查在 Sema/PatternUsefulness.cpp
- 模式编译和代码生成

## 概念关系图谱

- **同义词**: 模式匹配, pattern matching, match, 匹配, case, 分支
- **相关概念**: enum, option, exhaustiveness, 穷尽性检查
- **相关模块**: 无

## 常见问题

### pattern-match 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 pattern-match？

请参考下面的代码示例部分。

### pattern-match 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

