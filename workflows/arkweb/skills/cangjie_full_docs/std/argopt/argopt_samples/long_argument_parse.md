# 长命令行参数解析 <sup>(deprecated)</sup>

示例：

<!-- verify -->
```cangjie
import std.argopt.*

main() {
    let shortArgs: Array<String> = ["--test1=abc", "--test2=123", "--test3 xyz"]
    let shortArgName: String = ""
    let longArgName: Array<String> = ["--test1=", "test2=", "--test3="]
    let ao: ArgOpt = ArgOpt(shortArgs, shortArgName, longArgName)
    println(ao.getArg("--test1") ?? "None")
    println(ao.getArg("--test2") ?? "None")
    println(ao.getArg("--test3") ?? "None")
}
```

运行结果：

```text
abc
123
None
```
