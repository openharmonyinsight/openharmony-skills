# 仓颉并发编程示例

## spawn 的使用

主线程和新线程同时尝试打印一些文本。

代码如下：

<!-- run -->
```cangjie
main(): Int64 {
    spawn {
        => for (i in 0..10) {
            println("New thread, number = ${i}")
            sleep(100 * Duration.millisecond) /* 睡眠 100 毫秒 */
        }
    }

    for (i in 0..5) {
        println("Main thread, number = ${i}")
        sleep(100 * Duration.millisecond) /* 睡眠 100 毫秒 */
    }
    return 0
}
```

运行结果：

```text
Main thread, number = 0
New thread, number = 0
Main thread, number = 1
New thread, number = 1
Main thread, number = 2
New thread, number = 2
Main thread, number = 3
New thread, number = 3
Main thread, number = 4
New thread, number = 4
New thread, number = 5
```

> **注意：**
>
> 上述打印信息仅做参考，实际结果受运行时序影响，呈现随机性。
>
> 由于主线程不会等待新线程执行结束，因此程序退出时新线程并未执行结束。

## Future 的 get 的使用

主线程等待创建线程执行完再执行。

代码如下：

<!-- verify -->
```cangjie
main(): Int64 {
    let fut: Future<Unit> = spawn {
        => for (i in 0..10) {
            println("New thread, number = ${i}")
            /* 睡眠 100 毫秒 */
            sleep(100 * Duration.millisecond)
        }
    }

    /* 等待线程完成 */
    fut.get()

    for (i in 0..5) {
        println("Main thread, number = ${i}")
        /* 睡眠 100 毫秒 */
        sleep(100 * Duration.millisecond)
    }
    return 0
}
```

运行结果：

```text
New thread, number = 0
New thread, number = 1
New thread, number = 2
New thread, number = 3
New thread, number = 4
New thread, number = 5
New thread, number = 6
New thread, number = 7
New thread, number = 8
New thread, number = 9
Main thread, number = 0
Main thread, number = 1
Main thread, number = 2
Main thread, number = 3
Main thread, number = 4
```

## 取消仓颉线程

子线程接收主线程发送的取消请求。

<!-- verify -->
```cangjie
main(): Unit {
    /* 创建线程 */
    let future = spawn {
        while (true) {
            if (Thread.currentThread.hasPendingCancellation) {
                return 0
            }
        }
        return 1
    }
    /* 发起线程取消请求 */
    future.cancel()
    let res = future.get()
    println(res)
}
```

运行结果：

```text
0
```
