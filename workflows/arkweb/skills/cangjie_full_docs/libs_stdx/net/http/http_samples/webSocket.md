# webSocket

示例：

<!-- verify -->
```cangjie
import stdx.net.http.*
import stdx.encoding.url.*
import std.time.*
import std.sync.*
import std.collection.*
import stdx.log.*

let server = ServerBuilder().addr("127.0.0.1").port(0).build()

main() {
    // 1 启动服务器
    startServer()

    let client = ClientBuilder().build()
    let u = URL.parse("ws://127.0.0.1:${server.port}/webSocket")

    let subProtocol = ArrayList<String>(["foo1", "bar1"])
    let headers = HttpHeaders()
    headers.add("test", "echo")

    // 2 完成 WebSocket 握手，获取 WebSocket 实例
    let websocket: WebSocket
    let respHeaders: HttpHeaders
    (websocket, respHeaders) = WebSocket.upgradeFromClient(client, u, subProtocols: subProtocol, headers: headers)
    client.close()

    println("subProtocol: ${websocket.subProtocol}")
    println(respHeaders.getFirst("rsp") ?? "")

    // 3 消息收发
    // 发送 hello
    websocket.write(TextWebFrame, "hello".toArray())
    // 接收消息
    let data = ArrayList<UInt8>()
    var frame = websocket.read()
    while (true) {
        match (frame.frameType) {
            case ContinuationWebFrame =>
                data.add(all: frame.payload)
                if (frame.fin) {
                    break
                }
            case TextWebFrame | BinaryWebFrame =>
                if (!data.isEmpty()) {
                    throw Exception("invalid frame")
                }
                data.add(all: frame.payload)
                if (frame.fin) {
                    break
                }
            case CloseWebFrame =>
                websocket.write(CloseWebFrame, frame.payload)
                break
            case PingWebFrame => websocket.writePongFrame(frame.payload)
            case _ => ()
        }
        frame = websocket.read()
    }
    println("data size: ${data.size}")
    println("last item: ${String.fromUtf8(data.toArray()[4096])}")

    // 4 关闭 websocket，
    // 收发 CloseFrame
    websocket.writeCloseFrame(status: 1000)
    let websocketFrame = websocket.read()
    println("close frame type: ${websocketFrame.frameType}")
    println("close frame payload: ${websocketFrame.payload}")

    // 关闭底层连接
    websocket.closeConn()

    server.close()
}

func startServer() {
    // 1 注册 handler
    server.distributor.register("/webSocket", handler1)
    server.logger.level = LogLevel.OFF
    let serverOn = SyncCounter(1)
    server.afterBind({=> serverOn.dec()})
    spawn {server.serve()}
    serverOn.waitUntilZero()
}

// server:
func handler1(ctx: HttpContext): Unit {
    // 2 完成 websocket 握手，获取 websocket 实例
    let websocketServer = WebSocket.upgradeFromServer(
        ctx,
        subProtocols: ArrayList<String>(["foo", "bar", "foo1"]),
        userFunc: {
            request: HttpRequest =>
            let value = request.headers.getFirst("test") ?? ""
            let headers = HttpHeaders()
            headers.add("rsp", value)
            headers
        }
    )
    // 3 消息收发
    // 接收 hello
    let data = ArrayList<UInt8>()
    var frame = websocketServer.read()
    while (true) {
        match (frame.frameType) {
            case ContinuationWebFrame =>
                data.add(all: frame.payload)
                if (frame.fin) {
                    break
                }
            case TextWebFrame | BinaryWebFrame =>
                if (!data.isEmpty()) {
                    throw Exception("invalid frame")
                }
                data.add(all: frame.payload)
                if (frame.fin) {
                    break
                }
            case CloseWebFrame =>
                websocketServer.write(CloseWebFrame, frame.payload)
                break
            case PingWebFrame => websocketServer.writePongFrame(frame.payload)
            case _ => ()
        }
        frame = websocketServer.read()
    }
    println("data: ${String.fromUtf8(data.toArray())}")

    // 发 4097 个 a
    websocketServer.write(TextWebFrame, Array<UInt8>(4097, repeat: 97))

    // 4 关闭 websocket，
    // 收发 CloseFrame
    let websocketFrame = websocketServer.read()
    println("close frame type: ${websocketFrame.frameType}")
    println("close frame payload: ${websocketFrame.payload}")
    websocketServer.write(CloseWebFrame, websocketFrame.payload)
    // 关闭底层连接
    websocketServer.closeConn()
}
```

运行结果：

```text
subProtocol: foo1
echo
data: hello
data size: 4097
last item: a
close frame type: CloseWebFrame
close frame payload: [3, 232]
close frame type: CloseWebFrame
close frame payload: [3, 232]
```
