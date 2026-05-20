# 创建线程

当开发者希望并发执行某一段代码时，只需创建一个仓颉线程即可。要创建一个新的仓颉线程，可以使用关键字 `spawn` 并传递一个无形参的 `lambda` 表达式，该 `lambda` 表达式即为在新线程中执行的代码。

下方示例代码中，主线程和新线程均会尝试打印一些文本：

<!-- run -->

```cangjie
main(): Int64 {
    spawn { =>
        println("New thread before sleeping")
        sleep(100 * Duration.millisecond) // sleep for 100ms.
        println("New thread after sleeping")
    }

    println("Main thread")

    return 0
}
```

在上面的例子中，新线程会在主线程结束时一起停止，无论这个新线程是否已完成运行。上方示例的输出每次可能略有不同，有可能会输出类似如下的内容：

```text
New thread before sleeping
Main thread

```

`sleep()` 函数会让当前线程睡眠指定的时长，之后再恢复执行，其时间由指定的 Duration 类型决定。`sleep()` 详细介绍请参见[线程睡眠指定时长](./sleep.md)章节。
