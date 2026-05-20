# UNIX 使用示例

<!-- verify -->

```cangjie
import std.net.*
import std.sync.*
import std.fs.*

let SOCKET_PATH = "/tmp/tmpsock"
let barrier = Barrier(2)

func runUnixServer() {
    try (serverSocket = UnixServerSocket(bindAt: SOCKET_PATH)) {
        serverSocket.bind()
        barrier.wait()

        try (client = serverSocket.accept()) {
            client.write("hello".toArray())
        }
    }
}

main(): Int64 {
    let fut = spawn {
        runUnixServer()
    }
    barrier.wait()
    try (socket = UnixSocket(SOCKET_PATH)) {
        socket.connect()

        let buf = Array<Byte>(5, repeat: 0)
        socket.read(buf)

        println(String.fromUtf8(buf)) // hello
    }
    fut.get()
    remove(SOCKET_PATH)
    return 0
}
```

运行结果：

```text
hello
```
