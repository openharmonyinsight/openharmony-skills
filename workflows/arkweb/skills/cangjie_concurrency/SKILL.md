---
name: cangjie-concurrency
description: 仓颉语言并发编程。当需要了解仓颉语言的M:N线程模型、spawn创建线程、sleep、原子操作(Atomic)、互斥锁(Mutex)、条件变量(Condition)、synchronized、Future、线程取消、ThreadLocal等特性时，应使用此
  Skill。
descriptionZH: 仓颉语言并发编程。当需要了解仓颉语言的M:N线程模型、spawn创建线程、sleep、原子操作(Atomic)、互斥锁(Mutex)、条件变量(Condition)、synchronized、Future、线程取消、ThreadLocal等特性时，应使用此
  Skill。
tags:
  - 仓颉
  - 并发
---

# 仓颉语言并发编程 Skill

## 1. 并发概述

### 1.1 线程模型
- 仓颉使用**抢占式线程模型**
- 两种线程概念：**语言线程**和**原生线程**
- 仓颉线程是**用户空间轻量级线程**，采用 **M:N 线程模型** — M 个语言线程调度到 N 个原生（OS）线程上，M ≠ N 是可能的
- 每个原生线程选择一个就绪的仓颉线程执行。若仓颉线程阻塞（如等待互斥锁），原生线程挂起它并选择下一个就绪线程

### 1.2 跨语言注意事项
- 调用阻塞的**外部函数**（如 `socket_read`）时，**整个原生线程**被阻塞，阻止其调度其他仓颉线程 — 降低吞吐量

---

## 2. 创建线程

### 2.1 `spawn` 关键字
- **语法**：`spawn { => ... }` — 创建新的仓颉线程
- 接受**无参 Lambda 表达式**作为线程体
- 新线程与创建线程并发运行
- **重要**：主线程退出时新线程会被杀死，即使未完成

### 2.2 示例
```cangjie
main(): Int64 {
    spawn { =>
        println("New thread before sleeping")
        sleep(100 * Duration.millisecond)
        println("New thread after sleeping")
    }
    println("Main thread")
    return 0
}
```

---

## 3. 线程睡眠

### 3.1 `sleep()` 函数
- **签名**：`func sleep(dur: Duration): Unit`
- 阻塞当前线程至少 `dur` 时长
- **规则**：若 `dur <= Duration.Zero`，线程仅**让出**执行资源而不睡眠

---

## 4. 同步机制

### 4.1 原子操作

#### 支持的类型
- **整数原子**：`AtomicInt8`、`AtomicInt16`、`AtomicInt32`、`AtomicInt64`、`AtomicUInt8`、`AtomicUInt16`、`AtomicUInt32`、`AtomicUInt64`
- **布尔原子**：`AtomicBool`
- **引用原子**：`AtomicReference<T>`（仅引用类型）

#### 整数原子操作（9 种）
| 操作 | 说明 |
|------|------|
| `load()` | 读取值 |
| `store(val)` | 写入值 |
| `swap(val)` | 交换，返回旧值 |
| `compareAndSwap(old, new)` | CAS：若当前值 == old，设为 new；返回 `Bool` |
| `fetchAdd(val)` | 加法，返回旧值 |
| `fetchSub(val)` | 减法，返回旧值 |
| `fetchAnd(val)` | 按位与，返回旧值 |
| `fetchOr(val)` | 按位或，返回旧值 |
| `fetchXor(val)` | 按位异或，返回旧值 |

#### 布尔 & 引用原子操作（4 种）
仅 `load`、`store`、`swap`、`compareAndSwap`

#### 关键规则
- 交换/算术操作返回**修改前**的值
- `AtomicReference` CAS 比较对象同一性（同一对象），非值相等
- 内存序：当前仅支持**顺序一致性**

### 4.2 可重入互斥锁（`Mutex`）

#### 类声明
```cangjie
public class Mutex <: UniqueLock {
    public init()
    public func lock(): Unit
    public func unlock(): Unit
    public func tryLock(): Bool
    public func condition(): Condition
}
```

#### 规则
1. 访问共享数据前**须获取锁**
2. 完成后**须释放锁**
3. **可重入**：已持有 Mutex 的线程可再次获取而不死锁
4. `unlock()` 次数须与 `lock()` 次数匹配才能完全释放
5. 未持有锁时调用 `unlock()` 抛出 `IllegalSynchronizationStateException`
6. `tryLock()` 返回 `Bool` — 不保证获取锁；须检查返回值

### 4.3 条件变量（`Condition`）

#### 接口
```cangjie
public interface Condition {
    func wait(): Unit
    func wait(timeout!: Duration): Bool
    func waitUntil(predicate: ()->Bool): Unit
    func waitUntil(predicate: ()->Bool, timeout!: Duration): Bool
    func notify(): Unit
    func notifyAll(): Unit
}
```

#### 创建
- 通过 `Mutex` 的 `mtx.condition()` 创建
- 一个 Mutex 可创建**多个** `Condition` 实例
- **重要**：`mtx.condition()` **必须在 mutex 被锁定的状态下调用**，如果在未锁定状态下调用，会抛出 `IllegalSynchronizationStateException`

#### 正确创建 Condition 的方式

```cangjie
import std.sync.*

// ✅ 正确：在 synchronized 块中创建 Condition
let mtx = Mutex()
var cond: Condition = synchronized(mtx) {
    mtx.condition()
}

// ✅ 正确：手动加锁后创建
let mtx2 = Mutex()
mtx2.lock()
let cond2 = mtx2.condition()
mtx2.unlock()

// ❌ 错误：未锁定状态下调用 condition()
// let mtx3 = Mutex()
// let cond3 = mtx3.condition()  // 抛出 IllegalSynchronizationStateException
```

#### `wait()` 行为（4 步）
1. 将当前线程加入锁的等待队列
2. 阻塞当前线程并**完全释放**锁（记录重入计数）
3. 等待另一个线程的 `notify()` 或 `notifyAll()` 信号
4. 唤醒时以相同重入状态重新获取锁

#### 规则
- **`mtx.condition()` 须在锁定状态下调用**，否则抛出 `IllegalSynchronizationStateException`
- 调用 `wait()`、`notify()`、`notifyAll()` 前**须持有绑定的锁**
- Condition 须与**创建它的锁**一起使用
- **虚假唤醒**是允许的 — 始终在循环中包装 `wait()`
- `wait(timeout)` 超时精度不保证（依赖 OS）

#### 完整的生产者-消费者示例

```cangjie
import std.sync.*

var ready = false
let mtx = Mutex()
// 在 synchronized 块中创建 Condition
let cond = synchronized(mtx) { mtx.condition() }

main() {
    // 消费者线程
    let consumer = spawn { =>
        synchronized(mtx) {
            while (!ready) { // 可避免虚假唤醒
                cond.wait()  // 等待通知
            }
            println("Consumer: data is ready!")
        }
    }

    // 生产者线程
    let producer = spawn { =>
        sleep(Duration.second) // 模拟生产耗时
        synchronized(mtx) {
            ready = true
            cond.notifyAll() // 唤醒所有等待线程
        }
        println("Producer: notified!")
    }

    consumer.get()
    producer.get()
}
```

### 4.4 `synchronized` 关键字

#### 语法
```cangjie
synchronized(lockInstance) {
    // 临界区 — 自动加锁/解锁
}
```

#### 规则
1. 进入块时自动获取锁
2. 退出时自动释放锁 — 包括通过 `break`、`continue`、`return`、`throw` 退出
3. 可与任何 `Lock` 实例（包括 `Mutex`）一起使用
4. `synchronized` 是一个**表达式**，返回块的值

### 4.5 线程局部变量（`ThreadLocal<T>`）

#### 类声明
```cangjie
public class ThreadLocal<T> {
    public init()
    public func get(): Option<T>   // 未设置时返回 None
    public func set(value: Option<T>): Unit  // 传 None 以删除
}
```
- 来自 `core` 包（无需特殊导入）
- 每个线程有独立存储；线程间互不干扰

---

## 5. 终止线程

### 5.1 取消模型（协作式）
- **`Future<T>.cancel()`**：发送取消请求。**不会**强制停止线程
- **`Thread.currentThread.hasPendingCancellation`**：检查是否有取消请求
- 开发者负责实现取消逻辑
- 若取消请求被忽略，线程继续正常运行

### 5.2 `SyncCounter`
- 用于线程协调：`SyncCounter(n)`，配合 `dec()` 和 `waitUntilZero()` 使用
- 来自 `std.sync` 包
```cangjie
import std.sync.*

main() {
    let counter = SyncCounter(3)
    for (i in 0..3) {
        spawn { =>
            // 执行工作...
            counter.dec()     // 完成后计数减 1
        }
    }
    counter.waitUntilZero()   // 等待所有线程完成
}
```

---

## 6. 访问线程

### 6.1 `Future<T>` — 线程句柄

#### 类声明
```cangjie
public class Future<T> {
    public func get(): T
    public func get(timeout: Duration): T
    public func tryGet(): Option<T>
}
```

#### 返回类型
- `spawn` 返回 `Future<T>`，其中 `T` 匹配 Lambda 返回类型

#### 方法
| 方法 | 行为 |
|------|------|
| `get()` | 阻塞直到线程完成；返回结果。重新抛出线程中的异常 |
| `get(timeout)` | 带超时阻塞；超时抛出 `TimeoutException`。若 `timeout <= Duration.Zero`，行为同 `get()` |
| `tryGet()` | 非阻塞；线程未完成时返回 `Option<T>.None`；重新抛出异常 |

#### 关键规则
- `get()` 的位置决定并发性：放在其他工作前串行化执行；放在之后允许并行

### 6.2 `Thread` 类

#### 声明
```cangjie
class Thread {
    static prop currentThread: Thread
    prop id: Int64
    prop hasPendingCancellation: Bool
}
```

#### 规则
- `Thread` **不能直接实例化**
- 通过 `Future<T>.thread` 或 `Thread.currentThread` 获取
- `id` 是每个线程的唯一整数标识符
