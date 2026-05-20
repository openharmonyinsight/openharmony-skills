# 任意进程相关操作

下面是任意进程相关操作示例，以下示例不支持 Windows 平台。

代码如下：

<!-- run -->

```cangjie
import std.process.*

main(): Int64 {
    let echoProcess: SubProcess = launch("sleep", "10s")
    let ofProcess: Process = findProcess(echoProcess.pid)
    println(ofProcess.pid)
    println(ofProcess.name)
    println(ofProcess.command)
    ofProcess.terminate(force: true)
    return 0
}
```

运行结果可能如下：

```text
70753
sleep
sleep
```
