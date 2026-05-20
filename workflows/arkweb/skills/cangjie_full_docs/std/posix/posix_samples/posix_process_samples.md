# 进程相关信息操作

下面是进程相关信息操作示例，以下示例不支持 Windows 平台。

代码如下:

<!-- run -->

```cangjie
import std.posix.*

main(): Int64 {
    var result = nice(200)
    print("${result}")
    var result1 = kill(0, SIGCHLD)
    println(result1)
    var result2 = killpg(0, SIGURG)
    println("result ==> ${result2}")
    if (isatty(0) && isatty(1) && isatty(2)) {
        print("true01 ")
    } else {
        print("false01 ")
    }
    if (isatty(-23) || isatty(4) || isatty(455) || isatty(43332)) {
        print("true02 ")
    } else {
        println("false02")
    }
    return 0
}
```

运行结果：

```text
190
result ==> 0
true01 false02
```
