# 短命令行参数解析 <sup>(deprecated)</sup>

示例：

<!-- verify -->
```cangjie
import std.argopt.*

main() {
    let shortArgs: Array<String> = ["-a123", "-bofo", "-cccc"]
    let shortArgName: String = "a:b:c"
    let longArgName: Array<String> = Array<String>()
    let ao: ArgOpt = ArgOpt(shortArgs, shortArgName, longArgName)
    println(ao.getArg("-a") ?? "None")
    println(ao.getArg("-b") ?? "None")
    println(ao.getArg("-c") ?? "None")
}
```

运行结果：

```text
123
ofo
None
```
