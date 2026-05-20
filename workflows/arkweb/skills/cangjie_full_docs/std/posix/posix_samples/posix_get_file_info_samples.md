# 文件信息相关操作

下面是文件信息相关操作示例，以下示例不支持 Windows 平台。

代码如下:

<!-- verify -->

```cangjie
import std.posix.*

main(): Int64 {
    var result1: Bool = isType("/notdirs", S_IFDIR)
    println("result ==> ${result1}")
    var result2: Bool = isDir("/dev")
    println("result ==> ${result2}")
    var result3 = access("./oscfg.cfg", F_OK)
    println("result ==> ${result3}")
    var result4 = chmod("oscfg.cfg", UInt32(S_IXUSR))
    println("result ==> ${result4}")
    return 0
}
```

运行结果：

```text
result ==> false
result ==> true
result ==> -1
result ==> -1
```
