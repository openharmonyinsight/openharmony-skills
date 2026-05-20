# env 示例

## 当前进程相关操作

代码如下：

<!-- compile -->

```cangjie
import std.env.*

main(): Int64 {
    println(getProcessId())
    println(getCommand())
    println(getCommandLine().toString())
    println(getWorkingDirectory().toString())
    atExit(printText)
    exit(0)
    return 0
}

func printText(): Unit {
    println("hello cangjie!")
}
```

运行结果可能如下（输出结果中 main 为当前进程执行命令名，回调执行完成后当前进程会退出）：

```text
28481
main
[./main]
/root/code/workpalce/cangjie
hello cangjie!
```

## Console 示例

下面是 Console 示例，示例中接收用户输入的两条信息，并将这些信息通过标准输出原样返回给用户。

<!-- compile -->

```cangjie
import std.env.*

main() {
    getStdOut().write("请输入信息1：")
    var c = getStdIn().readln() // 输入：你好，请问今天星期几？
    var r = c.getOrThrow()
    getStdOut().writeln("输入的信息1为：" + r)

    getStdOut().write("请输入信息2：")
    c = getStdIn().readln() // 输入：你好，请问今天几号？
    r = c.getOrThrow()
    getStdOut().writeln("输入的信息2为：" + r)

    return
}
```

运行结果：

```text
请输入信息1：你好，请问今天星期几？
输入的信息1为：你好，请问今天星期几？
请输入信息2：你好，请问今天几号？
输入的信息2为：你好，请问今天几号？
```
