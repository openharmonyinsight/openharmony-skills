# UnixDatagram 使用示例

<!-- verify -->

```cangjie
import std.net.*
import std.sync.*
import std.fs.*
import std.random.*
import std.env.*

let barrier = Barrier(2)

func createTempFile(): String {
    let tempDir: Path = getTempDirectory()

    let index: String = Random().nextUInt64().toString()

    return tempDir.join("tmp${index}").toString()
}

func runUnixDatagramServer(serverPath: String, clientPath: String) {
    try (serverSocket = UnixDatagramSocket(bindAt: serverPath)) {
        serverSocket.bind()
        barrier.wait()

        let buf = Array<Byte>(3, repeat: 0)

        let (clientAddr, read) = serverSocket.receiveFrom(buf)

        if (read == 3 && buf == [1, 2, 3]) {
            println("server received")
        }
        if (clientAddr.toString() == clientPath) {
            println("client address correct")
        }
    }
}

main(): Int64 {
    let clientPath = createTempFile()
    let serverPath = createTempFile()
    let fut = spawn {
        runUnixDatagramServer(serverPath, clientPath)
    }
    barrier.wait()

    try (unixSocket = UnixDatagramSocket(bindAt: clientPath)) {
        unixSocket.sendTimeout = Duration.second * 2
        unixSocket.bind()
        unixSocket.connect(serverPath)

        unixSocket.send([1, 2, 3])
    }

    fut.get()

    return 0
}
```

运行结果：

```text
server received
client address correct
```
