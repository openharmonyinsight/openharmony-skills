---
keyword: concurrency
synonyms: [并发, 协程, coroutine, async, await, spawn, 线程, thread, 并行, parallel]
related: [future, channel, 同步, synchronization, 锁, lock]
category: language-feature
---

# 并发 (Concurrency)

## 中文描述
仓颉提供协程和并发原语支持,使用 spawn 创建协程,支持 async/await 异步编程模式。提供 channel、锁等并发同步机制,确保线程安全。

## English Description
Cangjie provides coroutine and concurrency primitives support, using spawn to create coroutines, supporting async/await asynchronous programming patterns. Provides channel, locks and other concurrency synchronization mechanisms to ensure thread safety.

## 使用场景
- 异步编程
- 并发任务执行
- 协程通信
- 线程安全

## 相关实现
- spawn 表达式解析在 Parse/ParseExpr.cpp
- 并发类型检查在 Sema/TypeCheckExpr/
- 线程代码生成在 CodeGen 模块
- 关键类: SpawnExpr, FutureType, AsyncAnalyzer

## 概念关系图谱

- **同义词**: 并发, 协程, coroutine, async, await, spawn, 线程, thread, 并行, parallel
- **相关概念**: future, channel, 同步, synchronization, 锁, lock
- **相关模块**: include

## 常见问题

### concurrency 是什么？

请参考上面的概念描述部分。

### 如何在代码中使用 concurrency？

请参考下面的代码示例部分。

### concurrency 在编译器的哪个阶段处理？

请查看相关模块部分了解处理流程。

