# 终止线程

可以通过 `Future<T>` 的 `cancel()` 方法向对应的线程发送终止请求，该方法不会停止线程执行。开发者需要使用 `Thread` 的 `hasPendingCancellation` 属性来检查线程是否存在终止请求。

一般而言，如果线程存在终止请求，那么开发者可以实施相应的线程终止逻辑。因此，如何终止线程都交由开发者自行处理，如果开发者忽略终止请求，那么线程继续执行直到正常结束。

示例代码如下：

<!-- verify -->

```cangjie
import std.sync.SyncCounter

main(): Unit {
    let syncCounter = SyncCounter(1)
    let fut = spawn {
        syncCounter.waitUntilZero()  // block until the syncCounter becomes zero
        if (Thread.currentThread.hasPendingCancellation) {  // Check cancellation request
            println("cancelled")
            return
        }
        println("hello")
    }
    fut.cancel()    // Send cancellation request
    syncCounter.dec()
    fut.get() // Join thread
}
```

输出结果如下：

```text
cancelled
```
