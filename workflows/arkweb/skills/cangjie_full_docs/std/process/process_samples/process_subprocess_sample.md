# 子进程相关操作

下面是子进程相关操作示例，以下示例不支持 Windows 平台。

代码如下：

<!-- compile -->

```cangjie
import std.process.*
import std.io.*
import std.fs.*

// 以Linux平台相关命令举例说明, 以下用例需要提前创建 “/root/code/Process/test” 目录
main(): Int64 {
    let sleepProcess: SubProcess = launch("sleep", "10s", workingDirectory: Path("/root/code/Process/test"))
    println(sleepProcess.pid)
    println(sleepProcess.name)
    println(sleepProcess.command)
    sleepProcess.terminate(force: true)
    let rtnCode = sleepProcess.wait()
    println("sleepProcess rtnCode: ${rtnCode}")

    let echoProcess: SubProcess = launch("echo", "hello cangjie!", stdOut: ProcessRedirect.Pipe)
    let strReader: StringReader<InputStream> = StringReader(echoProcess.stdOutPipe)
    println(strReader.readToEnd())
    return 0
}
```

运行结果可能如下：

```text
65953
sleep
sleep
sleepProcess rtnCode: 9
hello cangjie!
```
