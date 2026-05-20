# Atomic、Monitor 和 Timer 的使用

## Atomic 的使用

示例：

在多线程程序中，使用原子操作实现计数：

<!-- verify -->
```cangjie
import std.sync.*
import std.time.*
import std.collection.*

let count = AtomicInt64(0)

main(): Int64 {
    let list = ArrayList<Future<Int64>>()

    /* 创建 1000 个线程 */
    for (_ in 0..1000) {
        let fut = spawn {
            sleep(Duration.millisecond) /* 睡眠 1 毫秒 */
            count.fetchAdd(1)
        }
        list.add(fut)
    }

    /* 等待所有线程完成 */
    for (f in list) {
        f.get()
    }

    var val = count.load()
    println("count = ${val}")
    return 0
}
```

运行结果：

```text
count = 1000
```

## Monitor <sup>(deprecated)</sup> 的使用

> **注意：**
>
> 未来版本即将废弃，使用 [Condition](../sync_package_api/sync_package_interfaces.md#interface-condition) 替代。

示例:

在不同线程中，使用 `Monitor` 实现挂起和唤醒线程：

<!-- verify -->
```cangjie
import std.sync.*

var mon = Monitor()
var flag: Bool = true

main(): Int64 {
    let fut = spawn {
        mon.lock()
        while (flag) {
            println("New thread: before wait")
            mon.wait()
            println("New thread: after wait")
        }
        mon.unlock()
    }

    /* 睡眠 10 毫秒，以确保新线程可以执行 */
    sleep(10 * Duration.millisecond)

    mon.lock()
    println("Main thread: set flag")
    flag = false
    mon.unlock()

    println("Main thread: notify")
    mon.lock()
    mon.notifyAll()
    mon.unlock()

    /* 等待新线程完成 */
    fut.get()
    return 0
}
```

运行结果：

```text
New thread: before wait
Main thread: set flag
Main thread: notify
New thread: after wait
```

## Mutex 的使用

示例:

在不同线程中，使用 `Mutex` 锁和解锁：

<!-- verify -->
```cangjie
import std.sync.*

var mt = Mutex()
var con = synchronized(mt) { mt.condition() }
var flag: Bool = true

main(): Int64 {
    let fut = spawn {
        mt.lock()
        while (flag) {
            println("New thread: before wait")
            con.wait()
            println("New thread: after wait")
        }
        mt.unlock()
    }
    /* 睡眠 10 毫秒，以确保新线程可以执行 */
    sleep(10 * Duration.millisecond)
    mt.lock()
    println("Main thread: set flag")
    flag = false
    mt.unlock()

    println("Main thread: notify")
    mt.lock()
    con.notifyAll()
    mt.unlock()

    /* 等待新线程完成 */
    fut.get()
    return 0
}
```

运行结果：

```text
New thread: before wait
Main thread: set flag
Main thread: notify
New thread: after wait
```

## Condition 的使用

示例：

使用 `Condition` 实现挂起和唤醒线程：

<!-- verify -->
```cangjie
import std.sync.{Mutex, Condition, AtomicBool}

var mutex = Mutex()
var flag = AtomicBool(true)

main(): Int64 {
    let condition: Condition
    synchronized(mutex) {
        condition = mutex.condition() // 在持有锁的情况下生成 Condition 实例
    }

    let fut = spawn {
        synchronized(mutex) {
            println("New thread: before wait")
            condition.waitUntil {=> !flag.load()} // 挂起当前线程，等待直到 flag 值为 true
            println("New thread: after wait")
        }
    }

    /* 睡眠 10 毫秒，以确保新线程可以执行 */
    sleep(10 * Duration.millisecond)

    synchronized(mutex) { // 等待子线程挂起
        println("Main thread: set flag")
        flag.store(false) // 修改 flag 值
        println("Main thread: notify")
        condition.notifyAll() // 唤醒等待中的子线程
    }

    /* 等待新线程完成 */
    fut.get()
    return 0
}
```

运行结果：

```text
New thread: before wait
Main thread: set flag
Main thread: notify
New thread: after wait
```

## Timer 的使用

示例:

使用 `Timer` 创建一次性和重复性任务：

<!-- verify -->
```cangjie
import std.sync.*

main(): Int64 {
    let count = AtomicInt8(0)

    Timer.once(50 * Duration.millisecond) {
        =>
        println("run only once")
        count.fetchAdd(1)
    }

    let timer = Timer.repeat(
        100 * Duration.millisecond,
        200 * Duration.millisecond,
        {
            =>
            println("run repetitively")
            count.fetchAdd(10)
        }
    )

    sleep(Duration.second)
    timer.cancel()
    sleep(500 * Duration.millisecond)
    println("count = ${count.load()}")
    0
}
```

运行结果：

```text
run only once
run repetitively
run repetitively
run repetitively
run repetitively
run repetitively
count = 51
```
