# UDP 使用示例

<!-- verify -->

```cangjie
import std.net.*
import std.sync.*

let SERVER_PORT: UInt16 = 33333
let barrier = Barrier(2)

func runUdpServer() {
    try (serverSocket = UdpSocket(bindAt: SERVER_PORT)) {
        serverSocket.bind()
        barrier.wait()

        let buf = Array<Byte>(3, repeat: 0)

        let (clientAddr, count) = serverSocket.receiveFrom(buf)
        let sender = (clientAddr as IPSocketAddress)?.address.toString() ?? ""

        // Server receive 3 bytes: [1, 2, 3] from 127.0.0.1
        println("Server receive ${count} bytes: ${buf} from ${sender}")
    }
}

main(): Int64 {
    let fut = spawn {
        runUdpServer()
    }
    barrier.wait()

    try (udpSocket = UdpSocket(bindAt: 0)) { // random port
        udpSocket.sendTimeout = Duration.second * 2
        udpSocket.bind()
        udpSocket.sendTo(
            IPSocketAddress("127.0.0.1", SERVER_PORT),
            [1, 2, 3]
        )
    }

    fut.get()

    return 0
}
```

运行结果：

```text
Server receive 3 bytes: [1, 2, 3] from 127.0.0.1
```
