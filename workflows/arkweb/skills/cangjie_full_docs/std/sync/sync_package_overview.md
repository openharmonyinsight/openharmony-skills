# std.sync

## 功能介绍

sync 包提供并发编程相关的能力。

随着越来越多的计算机开始使用多核处理器，要充分发挥多核的优势，并发编程也变得越来越重要。

不同编程语言会以不同的方式实现线程。一些编程语言通过调用操作系统 API 来创建线程，意味着每个语言线程对应一个操作系统线程，一般称之为 1:1 的线程模型；也有一些编程语言提供特殊的线程实现，允许多个语言线程在不同数量的操作系统线程的上下文中切换执行，这种也被称为 M:N 的线程模型，即 M 个语言线程在 N 个操作系统线程上调度执行，其中 M 和 N 不一定相等。

仓颉编程语言希望给开发者提供一个友好、高效、统一的并发编程界面，让开发者无需关心操作系统线程、用户态线程等概念上的差异，同时屏蔽底层实现细节，因此我们只提供一个仓颉线程的概念。仓颉线程采用的是 M:N 线程模型的实现，因此本质上它是一种用户态的轻量级线程，支持抢占，且相比操作系统线程内存资源占用更小。

当开发者希望并发执行某一段代码时，只需创建一个仓颉线程即可。

要创建一个新的仓颉线程，可以使用关键字 spawn 并传递一个无形参的 lambda 表达式，该 lambda 表达式即为我们想在新线程中执行的代码。

示例:

通过 `spawn` 关键字创建一个仓颉线程：

<!-- run -->

```cangjie
main () {
    spawn {
        // 在新线程中执行
        println("Thread: ${Thread.currentThread.id}")
    }
    // 在主线程中执行
    println("Thread: ${Thread.currentThread.id}")
    sleep(Duration.second)
    0
}
```

可能的运行结果：

```text
Thread: 1
Thread: 2
```

sync 包主要提供了不同类型的原子操作，可重入互斥锁及其接口，利用共享变量的线程同步机制以及定时器的功能。

原子操作提供了包括整数类型、Bool 类型和引用类型的原子操作。

其中整数类型包括：Int8、Int16、Int32、Int64、UInt8、UInt16、UInt32、UInt64。

整数类型的原子操作支持基本的读(`load`)写(`store`)、交换(`swap`/`compareAndSwap`)以及算术运算(`fetchAdd`/`fetchSub`)等操作，需要注意的是：

- 交换操作和算术操作的返回值是修改前的值。

- `compareAndSwap` 是判断当前原子变量的值是否等于指定值，如果等于，则使用另一值替换；否则不替换。

Bool 类型和引用类型的原子操作只提供读写和交换操作，需要注意的是：

引用类型原子操作只对引用类型有效。

互斥锁 [Lock](./sync_package_api/sync_package_interfaces.md#interface-lock) 在使用的时候存在诸多不便，比如稍不注意会忘了解锁，或者在持有互斥锁的情况下抛出异常不能自动释放持有的锁等。因此，仓颉编程语言提供 `synchronized` 关键字，搭配 [Lock](./sync_package_api/sync_package_interfaces.md#interface-lock) 一起使用，来解决类似的问题。

通过在 `synchronized` 后面加上一个互斥锁实例，对其后面修饰的代码块进行保护，可以使得任意时刻最多只有一个线程可以执行被保护的代码：

- 一个线程在进入 `synchronized` 修饰的代码块之前，会自动获取 `Lock` 实例对应的锁，如果无法获取锁，则当前线程被阻塞。
- 一个线程在退出 `synchronized` 修饰的代码块之前（包括在代码块中使用 `break`、`continue`、`return`、`throw` 等控制转移表达式），会自动释放该 `Lock` 实例的锁。

示例:

在每个 `for` 循环的线程进入 `synchronized` 代码块前，会自动获取 `mtx` 实例对应的锁，在退出代码块前，会释放 `mtx` 实例对应的锁。

<!-- verify -->

```cangjie
import std.sync.Mutex

main () {
    let mtx = Mutex()
    let cnt = Box<Int64>(0)

    for (_ in 0..5) {
        spawn {
            synchronized(mtx) {
                cnt.value ++
                println("count: ${cnt.value}")
            }
        }
    }
    sleep(Duration.second)
    0
}
```

可能的运行结果：

```text
count: 1
count: 2
count: 3
count: 4
count: 5
```

## API 列表

### 常量&变量

|  常量&变量名 | 功能  |
| ------------ | ------------ |
| [DefaultMemoryOrder <sup>(deprecated)</sup>](./sync_package_api/sync_package_constants_vars.md#let-defaultmemoryorder-deprecated) | 默认内存顺序，详见枚举 [MemoryOrder <sup>(deprecated)</sup>](./sync_package_api/sync_package_enums.md#enum-memoryorder-deprecated)。 |

### 接口

|  接口名 | 功能  |
| ------------ | ------------ |
| [Condition](./sync_package_api/sync_package_interfaces.md#interface-condition) | 提供使线程阻塞并等待来自另一个线程的信号以恢复执行的功能的接口。 |
| [IReentrantMutex <sup>(deprecated)</sup>](./sync_package_api/sync_package_interfaces.md#interface-ireentrantmutex-deprecated) | 提供可重入互斥锁接口。 |
| [Lock](./sync_package_api/sync_package_interfaces.md#interface-lock) | 提供实现可重入互斥锁的接口。 |
| [UniqueLock](./sync_package_api/sync_package_interfaces.md#interface-uniquelock) | 提供实现独占锁的接口。 |

### 类

|  类名 | 功能  |
| ------------ | ------------ |
| [AtomicBool](./sync_package_api/sync_package_classes.md#class-atomicbool) | 提供 Bool 类型的原子操作相关函数。 |
| [AtomicInt16](./sync_package_api/sync_package_classes.md#class-atomicint16) | 提供 Int16 类型的原子操作相关函数。 |
| [AtomicInt32](./sync_package_api/sync_package_classes.md#class-atomicint32) | 提供 Int32 类型的原子操作相关函数。 |
| [AtomicInt64](./sync_package_api/sync_package_classes.md#class-atomicint64) | 提供 Int64 类型的原子操作相关函数。 |
| [AtomicInt8](./sync_package_api/sync_package_classes.md#class-atomicint8) | 提供 Int8 类型的原子操作相关函数。 |
| [AtomicOptionReference](./sync_package_api/sync_package_classes.md#class-atomicoptionreferencet-where-t--object) | 提供引用类型原子操作相关函数。 |
| [AtomicReference](./sync_package_api/sync_package_classes.md#class-atomicreferencet-where-t--object) | 引用类型原子操作相关函数。 |
| [AtomicUInt16](./sync_package_api/sync_package_classes.md#class-atomicuint16) | 提供 UInt16 类型的原子操作相关函数。 |
| [AtomicUInt32](./sync_package_api/sync_package_classes.md#class-atomicuint32) | 提供 UInt32 类型的原子操作相关函数。 |
| [AtomicUInt64](./sync_package_api/sync_package_classes.md#class-atomicuint64) | 提供 UInt64 类型的原子操作相关函数。 |
| [AtomicUInt8](./sync_package_api/sync_package_classes.md#class-atomicuint8) | 提供 UInt8 类型的原子操作相关函数。 |
| [Barrier](./sync_package_api/sync_package_classes.md#class-barrier) | 提供协调多个线程一起执行到某一个程序点的功能。 |
| [Monitor <sup>(deprecated)</sup>](./sync_package_api/sync_package_classes.md#class-monitor-deprecated) | 提供使线程阻塞并等待来自另一个线程的信号以恢复执行的功能。 |
| [MultiConditionMonitor <sup>(deprecated)</sup>](./sync_package_api/sync_package_classes.md#class-multiconditionmonitor-deprecated) | 提供对同一个互斥锁绑定多个条件变量的功能。 |
| [Mutex](./sync_package_api/sync_package_classes.md#class-mutex) | 提供可重入锁相关功能。 |
| [ReadWriteLock](./sync_package_api/sync_package_classes.md#class-readwritelock) | 提供可重入读写锁相关功能。 |
| [ReentrantMutex <sup>(deprecated)</sup>](./sync_package_api/sync_package_classes.md#class-reentrantmutex-deprecated) | 提供可重入锁相关功能。 |
| [ReentrantReadMutex <sup>(deprecated)</sup>](./sync_package_api/sync_package_classes.md#class-reentrantreadmutex-deprecated) | 提供可重入读写锁中的读锁类型。 |
| [ReentrantReadWriteMutex <sup>(deprecated)</sup>](./sync_package_api/sync_package_classes.md#class-reentrantreadwritemutex-deprecated) | 提供可重入读写锁相关功能。 |
| [ReentrantWriteMutex <sup>(deprecated)</sup>](./sync_package_api/sync_package_classes.md#class-reentrantwritemutex-deprecated) | 提供可重入读写锁中的写锁类型。 |
| [Semaphore](./sync_package_api/sync_package_classes.md#class-semaphore) | 提供信号量相关功能。 |
| [SyncCounter](./sync_package_api/sync_package_classes.md#class-synccounter) | 提供倒数计数器功能。 |
| [Timer](./sync_package_api/sync_package_classes.md#class-timer) | 提供定时器功能。 |

### 枚举

|  枚举类型 | 功能  |
| ------------ | ------------ |
| [MemoryOrder <sup>(deprecated)</sup>](./sync_package_api/sync_package_enums.md#enum-memoryorder-deprecated) | 内存顺序类型枚举。 |
| [ReadWriteMutexMode <sup>(deprecated)</sup>](./sync_package_api/sync_package_enums.md#enum-readwritemutexmode-deprecated) | 读写锁公平模式枚举。 |
| [CatchupStyle](./sync_package_api/sync_package_enums.md#enum-catchupstyle) | 重复性任务定时器需要使用的追平策略枚举。 |

### 结构体

|  结构体 | 功能  |
| ------------ | ------------ |
| [ConditionID <sup>(deprecated)</sup>](./sync_package_api/sync_package_structs.md#struct-conditionid-deprecated) | 用于表示互斥锁的条件变量，详见 [MultiConditionMonitor](./sync_package_api/sync_package_classes.md#class-multiconditionmonitor-deprecated)。 |

### 异常类

|  异常类名 | 功能  |
| ------------ | ------------ |
| [IllegalSynchronizationStateException](./sync_package_api/sync_package_exceptions.md#class-illegalsynchronizationstateexception) | 此类为非法同步状态异常。 |
