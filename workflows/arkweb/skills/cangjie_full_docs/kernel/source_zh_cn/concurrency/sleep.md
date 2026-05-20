# 线程睡眠指定时长 sleep

`sleep` 函数会阻塞当前运行的线程，该线程会主动睡眠一段时间，之后再恢复执行，其参数类型为 Duration 类型。函数原型为：

```cangjie
func sleep(dur: Duration): Unit // Sleep for at least `dur`.
```

> **注意：**
>
> 如果 `dur` <= Duration.Zero, 那么当前线程只会让出执行资源，并不会进入睡眠。

以下是使用 `sleep` 的示例：

<!-- verify -->

```cangjie
main(): Int64 {
    println("Hello")
    sleep(Duration.second)  // sleep for 1s.
    println("World")
    return 0
}
```

输出结果如下：

```text
Hello
World
```
