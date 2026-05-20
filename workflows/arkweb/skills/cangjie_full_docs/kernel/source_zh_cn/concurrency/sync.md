# 同步机制

在并发编程中，如果缺少同步机制来保护多个线程共享的变量，很容易会出现数据竞争问题（data race）。

仓颉编程语言提供三种常见的同步机制来确保数据的线程安全：原子操作、互斥锁和条件变量。

## 原子操作 Atomic

仓颉提供整数类型、`Bool` 类型和引用类型的原子操作。

其中整数类型包括： `Int8`、`Int16`、`Int32`、`Int64`、`UInt8`、`UInt16`、`UInt32`、`UInt64`。

整数类型的原子操作支持基本的读写、交换以及算术运算操作：

| 操作             | 功能                                              |
| ---------------- | ------------------------------------------------- |
| `load`           | 读取                                              |
| `store`          | 写入                                              |
| `swap`           | 交换，返回交换前的值                               |
| `compareAndSwap` | 比较再交换，交换成功返回 `true`，否则返回 `false` |
| `fetchAdd`       | 加法，返回执行加操作之前的值                      |
| `fetchSub`       | 减法，返回执行减操作之前的值                      |
| `fetchAnd`       | 与，返回执行与操作之前的值                        |
| `fetchOr`        | 或，返回执行或操作之前的值                        |
| `fetchXor`       | 异或，返回执行异或操作之前的值                    |

需要注意的是：

1. 交换操作和算术操作的返回值是修改前的值。
2. compareAndSwap 是判断当前原子变量的值是否等于 old 值，如果等于，则使用 new 值替换；否则不替换。

以 `Int8` 类型为例，对应的原子操作类型声明如下：

```cangjie
class AtomicInt8 {
    public func load(): Int8
    public func store(val: Int8): Unit
    public func swap(val: Int8): Int8
    public func compareAndSwap(old: Int8, new: Int8): Bool
    public func fetchAdd(val: Int8): Int8
    public func fetchSub(val: Int8): Int8
    public func fetchAnd(val: Int8): Int8
    public func fetchOr(val: Int8): Int8
    public func fetchXor(val: Int8): Int8
}
```

上述每一种原子类型的方法都有一个对应的方法可以接收内存排序参数，目前内存排序参数仅支持顺序一致性。

类似的，其他整数类型对应的原子操作类型有：

```cangjie
class AtomicInt16 {...}
class AtomicInt32 {...}
class AtomicInt64 {...}
class AtomicUInt8 {...}
class AtomicUInt16 {...}
class AtomicUInt32 {...}
class AtomicUInt64 {...}
```

下方示例演示了如何在多线程程序中，使用原子操作实现计数：

<!-- verify -->

```cangjie
import std.sync.AtomicInt64
import std.collection.ArrayList

let count = AtomicInt64(0)

main(): Int64 {
    let list = ArrayList<Future<Int64>>()

    // create 1000 threads.
    for (_ in 0..1000) {
        let fut = spawn {
            sleep(Duration.millisecond) // sleep for 1ms.
            count.fetchAdd(1)
        }
        list.add(fut)
    }

    // Wait for all threads finished.
    for (f in list) {
        f.get()
    }

    let val = count.load()
    println("count = ${val}")
    return 0
}
```

输出结果应为：

```text
count = 1000
```

以下是使用整数类型原子操作的一些其他正确示例：

<!-- compile -->

```cangjie
var obj: AtomicInt32 = AtomicInt32(1)
var x = obj.load() // x: 1, the type is Int32
x = obj.swap(2) // x: 1
x = obj.load() // x: 2
var y = obj.compareAndSwap(2, 3) // y: true, the type is Bool.
y = obj.compareAndSwap(2, 3) // y: false, the value in obj is no longer 2 but 3. Therefore, the CAS operation fails.
x = obj.fetchAdd(1) // x: 3
x = obj.load() // x: 4
```

`Bool` 类型和引用类型的原子操作只提供读写和交换操作：

| 操作             | 功能                                              |
| ---------------- | ------------------------------------------------- |
| `load`           | 读取                                              |
| `store`          | 写入                                              |
| `swap`           | 交换，返回交换前的值                              |
| `compareAndSwap` | 比较再交换，交换成功返回 `true`，否则返回 `false` |

> **注意：**
>
> 引用类型原子操作只对引用类型有效。

原子引用类型是 `AtomicReference`，以下是使用 `Bool` 类型、引用类型原子操作的一些正确示例：

<!-- verify -->

```cangjie
import std.sync.{AtomicBool, AtomicReference}

class A {}

main() {
    var obj = AtomicBool(true)
    var x1 = obj.load() // x1: true, the type is Bool
    println(x1)
    var t1 = A()
    var obj2 = AtomicReference(t1)
    var x2 = obj2.load() // x2 and t1 are the same object
    var y1 = obj2.compareAndSwap(x2, t1) // x2 and t1 are the same object, y1: true
    println(y1)
    var t2 = A()
    var y2 = obj2.compareAndSwap(t2, A()) // x and t1 are not the same object, CAS fails, y2: false
    println(y2)
    y2 = obj2.compareAndSwap(t1, A()) // CAS successes, y2: true
    println(y2)
}
```

编译执行上述代码，输出结果为：

```text
true
true
false
true
```

## 可重入互斥锁 Mutex

可重入互斥锁的作用是对临界区加以保护，使得任意时刻最多只有一个线程能够执行临界区的代码。当一个线程试图获取一个已被其他线程持有的锁时，该线程会被阻塞，直到锁被释放，该线程才会被唤醒，可重入是指线程获取该锁后可再次获得该锁。

使用可重入互斥锁时，必须牢记两条规则：

1. 在访问共享数据之前，必须尝试获取锁；
2. 处理完共享数据后，必须释放锁，以便其他线程可以获得锁。

`Mutex` 提供的主要成员函数如下：

```cangjie
public class Mutex <: UniqueLock {
    // Create a Mutex.
    public init()

    // Locks the mutex, blocks if the mutex is not available.
    public func lock(): Unit

    // Unlocks the mutex. If there are other threads blocking on this
    // lock, then wake up one of them.
    public func unlock(): Unit

    // Tries to lock the mutex, returns false if the mutex is not
    // available, otherwise returns true.
    public func tryLock(): Bool

    // Generate a Condition instance for the mutex.
    public func condition(): Condition
}
```

下方示例演示了如何使用 `Mutex` 来保护对全局共享变量 `count` 的访问，对 `count` 的操作即属于临界区：

<!-- verify -->

```cangjie
import std.sync.Mutex
import std.collection.ArrayList

var count: Int64 = 0
let mtx = Mutex()

main(): Int64 {
    let list = ArrayList<Future<Unit>>()

    // create 1000 threads.
    for (i in 0..1000) {
        let fut = spawn {
            sleep(Duration.millisecond) // sleep for 1ms.
            mtx.lock()
            count++
            mtx.unlock()
        }
        list.add(fut)
    }

    // Wait for all threads finished.
    for (f in list) {
        f.get()
    }

    println("count = ${count}")
    return 0
}
```

输出结果应为：

```text
count = 1000
```

下方示例演示了如何使用 `tryLock`：

<!-- run -->

```cangjie
import std.sync.Mutex


main(): Int64 {
    let mtx: Mutex = Mutex()
    var future: Future<Unit> = spawn {
        mtx.lock()
        println("get the lock, do something")
        sleep(Duration.millisecond * 10)
        mtx.unlock()
    }
    try {
        future.get(Duration.millisecond * 10)
    } catch (e: TimeoutException) {
        if (mtx.tryLock()) {
            println("tryLock success, do something")
            mtx.unlock()
            return 0
        }
        println("tryLock failed, do nothing")
        return 0
    }
    return 0
}
```

一种可能的输出结果如下：

```text
get the lock, do something
```

以下是互斥锁的一些错误示例：

错误示例 1：线程操作临界区后没有解锁，导致其他线程无法获得锁而阻塞。

<!-- compile.error -->
<!-- cfg="libcangjie-std-sync" -->

```cangjie
import std.sync.Mutex

var sum: Int64 = 0
let mutex = Mutex()

main() {
    let foo = spawn { =>
        mutex.lock()
        sum = sum + 1
    }
    let bar = spawn { =>
        mutex.lock()
        sum = sum + 1
    }
    foo.get()
    println("${sum}")
    bar.get() // Because the thread is not unlocked, other threads waiting to obtain the current mutex will be blocked.
}
```

错误示例 2：在本线程没有持有锁的情况下调用 `unlock` 将会抛出异常。

<!-- compile.error -->
<!-- cfg="libcangjie-std-sync" -->

```cangjie
import std.sync.Mutex

var sum: Int64 = 0
let mutex = Mutex()

main() {
    let foo = spawn { =>
        sum = sum + 1
        mutex.unlock() // Error, Unlock without obtaining the lock and throw an exception: IllegalSynchronizationStateException.
    }
    foo.get()
}
```

错误示例 3：`tryLock()` 并不保证获取到锁，可能会造成不在锁的保护下操作临界区和在没有持有锁的情况下调用 `unlock` 抛出异常等行为。

<!-- compile.error -->
<!-- cfg="libcangjie-std-sync" -->

```cangjie
import std.sync.Mutex

var sum: Int64 = 0
let mutex = Mutex()

main() {
    for (i in 0..100) {
        spawn { =>
            mutex.tryLock() // Error, `tryLock()` just trying to acquire a lock, there is no guarantee that the lock will be acquired, and this can lead to abnormal behavior.
            sum = sum + 1
            mutex.unlock()
        }
    }
}
```

另外，`Mutex` 在设计上是一个可重入锁，也就是说：在某个线程已经持有一个 `Mutex` 锁的情况下，再次尝试获取同一个 `Mutex` 锁，永远可以立即获得该 `Mutex` 锁。

> **注意：**
>
> 虽然 `Mutex` 是一个可重入锁，但是调用 `unlock()` 的次数必须和调用 `lock()` 的次数相同，才能成功释放该锁。

下方示例代码演示了 `Mutex` 可重入的特性：

<!-- verify -->

```cangjie
import std.sync.Mutex

var count: Int64 = 0
let mtx = Mutex()

func foo() {
    mtx.lock()
    count += 10
    bar()
    mtx.unlock()
}

func bar() {
    mtx.lock()
    count += 100
    mtx.unlock()
}

main(): Int64 {
    let fut = spawn {
        sleep(Duration.millisecond) // sleep for 1ms.
        foo()
    }

    foo()

    fut.get()

    println("count = ${count}")
    return 0
}
```

输出结果应为：

```text
count = 220
```

在上方示例中，无论是主线程还是新创建的线程，如果在 `foo()` 中已经获得了锁，那么继续调用 `bar()` 的话，在 `bar()` 函数中由于是对同一个 `Mutex` 进行加锁，因此也是能立即获得该锁的，不会出现死锁。

## Condition

`Condition` 是与某个互斥锁绑定的条件变量（也就是等待队列），`Condition` 实例由互斥锁创建，一个互斥锁可以创建多个 `Condition` 实例。`Condition` 可以使线程阻塞并等待来自另一个线程的信号以恢复执行。这是一种利用共享变量进行线程同步的机制，主要提供如下方法：

```cangjie
public class Mutex <: UniqueLock {
    // ...
    // Generate a Condition instance for the mutex.
    public func condition(): Condition
}

public interface Condition {
    // Wait for a signal, blocking the current thread.
    func wait(): Unit
    func wait(timeout!: Duration): Bool

    // Wait for a signal and predicate, blocking the current thread.
    func waitUntil(predicate: ()->Bool): Unit
    func waitUntil(predicate: ()->Bool, timeout!: Duration): Bool

    // Wake up one thread of those waiting on the monitor, if any.
    func notify(): Unit

    // Wake up all threads waiting on the monitor, if any.
    func notifyAll(): Unit
}
```

调用 `Condition` 接口的 `wait`、`notify` 或 `notifyAll` 方法前，需要确保当前线程已经持有绑定的锁。`wait` 方法包含如下动作：

1. 添加当前线程到对应锁的等待队列中；
2. 阻塞当前线程，同时完全释放该锁，并记录锁的重入次数；
3. 等待某个其他线程使用同一个 `Condition` 实例的 `notify` 或 `notifyAll` 方法向该线程发出信号；
4. 当前线程被唤醒后，会自动尝试重新获取锁，且持有锁的重入状态与第 2 步记录的重入次数相同；但是如果尝试获取锁失败，则当前线程会阻塞在该锁上。

`wait` 方法接受一个可选参数 `timeout`。需要注意的是，业界很多常用的常规操作系统不保证调度的实时性，因此无法保证一个线程会被阻塞“精确的 N 纳秒”——可能会观察到与系统相关的不精确情况。此外，当前语言规范明确允许实现产生虚假唤醒——在这种情况下，`wait` 返回值是由实现决定的——可能为 `true` 或 `false`。因此鼓励开发者始终将 `wait` 包在一个循环中：

```cangjie
synchronized (obj) {
  while (<condition is not true>) {
    obj.wait()
  }
}
```

以下是使用 `Condition` 的一个正确示例：

<!-- verify -->

```cangjie
import std.sync.Mutex

let mtx = Mutex()
let condition = synchronized(mtx) {
    mtx.condition()
}
var flag: Bool = true

main(): Int64 {
    let fut = spawn {
        mtx.lock()
        while (flag) {
            println("New thread: before wait")
            condition.wait()
            println("New thread: after wait")
        }
        mtx.unlock()
    }

    // Sleep for 10ms, to make sure the new thread can be executed.
    sleep(10 * Duration.millisecond)

    mtx.lock()
    println("Main thread: set flag")
    flag = false
    mtx.unlock()

    mtx.lock()
    println("Main thread: notify")
    condition.notifyAll()
    mtx.unlock()

    // wait for the new thread finished.
    fut.get()
    return 0
}
```

输出结果应为：

```text
New thread: before wait
Main thread: set flag
Main thread: notify
New thread: after wait
```

`Condition` 对象执行 `wait` 时，必须在锁的保护下进行，否则 `wait` 中释放锁的操作会抛出异常。

以下是使用条件变量的一些错误示例：

<!-- run.error -->

```cangjie
import std.sync.Mutex

let m1 = Mutex()
let c1 = synchronized(m1) {
    m1.condition()
}
let m2 = Mutex()
var flag: Bool = true
var count: Int64 = 0

func foo1() {
    spawn {
        m2.lock()
        while (flag) {
            c1.wait() // Error：The lock used together with the condition variable must be the same lock and in the locked state. Otherwise, the unlock operation in `wait` throws an exception.
        }
        count = count + 1
        m2.unlock()
    }
    m1.lock()
    flag = false
    c1.notifyAll()
    m1.unlock()
}

func foo2() {
    spawn {
        while (flag) {
            c1.wait() // Error：The `wait` of a conditional variable must be called with a lock held.
        }
        count = count + 1
    }
    m1.lock()
    flag = false
    c1.notifyAll()
    m1.unlock()
}

main() {
    foo1()
    foo2()
    c1.wait()
}
```

有时在复杂的线程间同步的场景下需要对同一个锁对象生成多个 `Condition` 实例，以下示例实现了一个长度固定的有界 `FIFO` 队列。当队列为空，`get()` 会被阻塞；当队列已满，`put()` 会被阻塞。

<!-- compile -->

```cangjie
import std.sync.{Mutex, Condition}

class BoundedQueue {
    // Create a Mutex, two Conditions.
    let m: Mutex = Mutex()
    var notFull: Condition
    var notEmpty: Condition

    var count: Int64 // Object count in buffer.
    var head: Int64  // Write index.
    var tail: Int64  // Read index.

    // Queue's length is 100.
    let items: Array<Object> = Array<Object>(100, {i => Object()})

    init() {
        count = 0
        head = 0
        tail = 0

        synchronized(m) {
          notFull  = m.condition()
          notEmpty = m.condition()
        }
    }

    // Insert an object, if the queue is full, block the current thread.
    public func put(x: Object) {
        // Acquire the mutex.
        synchronized(m) {
          while (count == 100) {
            // If the queue is full, wait for the "queue notFull" event.
            notFull.wait()
          }
          items[head] = x
          head++
          if (head == 100) {
            head = 0
          }
          count++

          // An object has been inserted and the current queue is no longer
          // empty, so wake up the thread previously blocked on get()
          // because the queue was empty.
          notEmpty.notify()
        } // Release the mutex.
    }

    // Pop an object, if the queue is empty, block the current thread.
    public func get(): Object {
        // Acquire the mutex.
        synchronized(m) {
          while (count == 0) {
            // If the queue is empty, wait for the "queue notEmpty" event.
            notEmpty.wait()
          }
          let x: Object = items[tail]
          tail++
          if (tail == 100) {
            tail = 0
          }
          count--

          // An object has been popped and the current queue is no longer
          // full, so wake up the thread previously blocked on put()
          // because the queue was full.
          notFull.notify()

          return x
        } // Release the mutex.
    }
}
```

## synchronized 关键字

`Lock` 提供了一种便利灵活的加锁的方式，同时因为它的灵活性，也可能引起忘记解锁，或者在持有锁的情况下抛出异常不能自动释放持有的锁的问题。因此，仓颉编程语言提供一个 `synchronized` 关键字，搭配 `Lock` 一起使用，可以在其后跟随的作用域内自动进行加锁解锁操作，用来解决类似的问题。

下方示例代码演示了如何使用 `synchronized` 关键字来保护共享数据：

<!-- verify -->

```cangjie
import std.sync.Mutex
import std.collection.ArrayList

var count: Int64 = 0
let mtx = Mutex()

main(): Int64 {
    let list = ArrayList<Future<Unit>>()

    // create 1000 threads.
    for (i in 0..1000) {
        let fut = spawn {
            sleep(Duration.millisecond) // sleep for 1ms.
            // Use synchronized(mtx), instead of mtx.lock() and mtx.unlock().
            synchronized(mtx) {
                count++
            }
        }
        list.add(fut)
    }

    // Wait for all threads finished.
    for (f in list) {
        f.get()
    }

    println("count = ${count}")
    return 0
}
```

输出结果应为：

```text
count = 1000
```

通过在 `synchronized` 后面加上一个 `Lock` 实例，对其后面修饰的代码块进行保护，可以使得任意时刻最多只有一个线程可以执行被保护的代码：

1. 一个线程在进入 `synchronized` 修饰的代码块之前，会自动获取 `Lock` 实例对应的锁，如果无法获取锁，则当前线程被阻塞；
2. 一个线程在退出 `synchronized` 修饰的代码块之前，会自动释放该 `Lock` 实例的锁。

对于控制转移表达式（如 `break`、`continue`、`return`、`throw`），在导致程序的执行跳出 `synchronized` 代码块时，也符合上面第 2 条的说明，也就说也会自动释放 `synchronized` 表达式对应的锁。

下方示例演示了在 `synchronized` 代码块中出现 `break` 语句的情况：

<!-- verify -->

```cangjie
import std.sync.Mutex
import std.collection.ArrayList

var count: Int64 = 0
var mtx: Mutex = Mutex()

main(): Int64 {
    let list = ArrayList<Future<Unit>>()
    for (i in 0..10) {
        let fut = spawn {
            while (true) {
                synchronized(mtx) {
                    count = count + 1
                    break
                    println("in thread")
                }
            }
        }
        list.add(fut)
    }

    // Wait for all threads finished.
    for (f in list) {
        f.get()
    }

    synchronized(mtx) {
        println("in main, count = ${count}")
    }
    return 0
}
```

输出结果应为：

```text
in main, count = 10
```

实际上 `in thread` 这行不会被打印，因为 `break` 语句实际上会让程序执行跳出 `while` 循环（在跳出 `while` 循环之前，先跳出 `synchronized` 代码块）。

## 线程局部变量 ThreadLocal

使用 core 包中的 `ThreadLocal` 可以创建并使用线程局部变量，每一个线程都有它独立的一个存储空间来保存这些线程局部变量。因此，在每个线程可以安全地访问他们各自的线程局部变量，而不受其他线程的影响。

```cangjie
public class ThreadLocal<T> {
    /* 构造一个携带空值的仓颉线程局部变量 */
    public init()

    /* 获得仓颉线程局部变量的值 */
    public func get(): Option<T> // 如果值不存在，则返回 Option<T>.None。返回值 Option<T> - 仓颉线程局部变量的值

    /* 通过 value 设置仓颉线程局部变量的值 */
    public func set(value: Option<T>): Unit // 如果传入 Option<T>.None，该局部变量的值将被删除，在线程后续操作中将无法获取。参数 value - 需要设置的局部变量的值。
}
```

下方示例代码演示了如何通过 `ThreadLocal`类来创建并使用各自线程的局部变量：

<!-- run -->

```cangjie

main(): Int64 {
    let tl = ThreadLocal<Int64>()
    let fut1 = spawn {
        tl.set(123)
        println("tl in spawn1 = ${tl.get().getOrThrow()}")
    }
    let fut2 = spawn {
        tl.set(456)
        println("tl in spawn2 = ${tl.get().getOrThrow()}")
    }
    fut1.get()
    fut2.get()
    0
}
```

可能的输出结果如下：

```text
tl in spawn1 = 123
tl in spawn2 = 456
```

或者

```text
tl in spawn2 = 456
tl in spawn1 = 123
```
