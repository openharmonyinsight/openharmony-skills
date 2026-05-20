---
keyword: for-loop
synonyms: [for, 循环, loop, for-in, 迭代, iteration, while, do-while]
related: [iterator, iterable, collections, break, continue]
category: language-feature
---

# 循环 (Loop)

## 中文描述
仓颉支持多种循环结构:for-in 循环用于遍历可迭代对象,while 循环用于条件循环,do-while 循环至少执行一次。循环支持 break 和 continue 控制流。

## English Description
Cangjie supports multiple loop structures: for-in loop for iterating over iterable objects, while loop for conditional loops, do-while loop executes at least once. Loops support break and continue control flow.

## 使用场景
- 遍历集合元素
- 条件循环
- 迭代器模式
- 循环控制(break, continue)

## 相关实现
- for-in 表达式解析在 Parse/ParseExpr.cpp
- 循环语句解析在 Parse/ParseStmt.cpp
- 迭代器检查在 Sema/TypeCheckExpr/
- 关键类: ForExpr, WhileStmt, IterableType

## 概念关系图谱

- **同义词**: for, 循环, loop, for-in, 迭代, iteration, while, do-while
- **相关概念**: iterator, iterable, collections, break, continue
- **相关模块**: 无

## 常见问题

### for-loop 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 for-loop？

请参考下面的代码示例部分。

### for-loop 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

