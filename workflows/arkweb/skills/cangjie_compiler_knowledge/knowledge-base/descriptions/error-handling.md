---
keyword: error-handling
synonyms: [异常, exception, 错误处理, error handling, try, catch, throw, finally]
related: [option, result, 异常类型, exception type]
category: language-feature
---

# 错误处理 (Error Handling)

## 中文描述
仓颉提供基于异常的错误处理机制,使用 try-catch-finally 语句捕获和处理异常。支持异常类型层次结构、异常传播、资源清理等特性。

## English Description
Cangjie provides exception-based error handling mechanism using try-catch-finally statements to catch and handle exceptions. Supports exception type hierarchy, exception propagation, resource cleanup, etc.

## 使用场景
- 异常捕获和处理
- 错误传播
- 资源清理(finally)
- 自定义异常类型

## 相关实现
- try/catch/finally 解析在 Parse/ParseExpr.cpp
- 异常类型检查在 Sema/TypeCheckExpr/
- 关键类: TryExpr, CatchClause, ExceptionType, ThrowExpr

## 概念关系图谱

- **同义词**: 异常, exception, 错误处理, error handling, try, catch, throw, finally
- **相关概念**: option, result, 异常类型, exception type
- **相关模块**: 无

## 常见问题

### error-handling 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 error-handling？

请参考下面的代码示例部分。

### error-handling 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

