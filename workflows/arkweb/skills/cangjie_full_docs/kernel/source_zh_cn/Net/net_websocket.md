# WebSocket 编程

在网络编程中，WebSocket 是一种常用的应用层协议。与 HTTP 一样，它也基于 TCP 协议之上，并且常用于 web 服务端应用开发。

不同于 HTTP 的是， WebSocket 只需要客户端和服务端进行一次握手，即可创建长久的连接，并且进行双向的数据传输。即基于 WebSocket 实现的服务端可以主动传输数据给客户端，从而实现实时通讯。

WebSocket 是一个独立的协议，它与 HTTP 的关联在于，它的握手被 HTTP 服务端解释为一个升级请求。因此，仓颉将 WebSocket 包含在 http 包中。

仓颉将 WebSocket 协议通信机制抽象为 WebSocket 类，提供方法将一个 http/1.1 或 http/2.0 服务端句柄升级到 WebSocket 协议实例，通过返回的 WebSocket 实例进行 WebSocket 通信，例如数据报文的读写。

在仓颉中，WebSocket 所传输的数据基本单元称为帧，帧分为两类，一类为传输控制信息的帧，即 Close Frame 用于关闭连接， Ping Frame 用于实现 Keep-Alive ， Pong Frame 是 Ping Frame 的响应类型，另一类是传输应用数据的帧，应用数据帧支持分段传输。

仓颉的帧由三个属性构成，其中 fin 和 frameType 共同说明了帧是否分段和帧的类型，payload 为帧的载荷，除此之外开发者无需关心其他属性即可进行报文传输。

如下示例展示了 WebSocket 的握手以及消息收发过程：创建 HTTP 客户端和服务端，分别发起 WebSocket 升级（或握手），握手成功后开始帧的读写。

> **说明：**
>
> net、encoding、log 等库已从仓颉 SDK 移到 stdx 模块，使用前需要下载软件包，并在 cjpm.toml 中配置。

<!-- verify -->

```cangjie
import stdx.net.http.*
import stdx.encoding.url.*
import std.time.*
import std.sync.*
import std.collection.*
import stdx.log.*

let server = ServerBuilder()
                        .addr("127.0.0.1")
                        .port(0)
                        .build()

// client：
main() {
    // 1 启动服务器
    spawn { startServer() }
    sleep(Duration.millisecond * 200)

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

    println("subProtocol: ${websocket.subProtocol}")      // fool1
    println(respHeaders.getFirst("rsp") ?? "") // echo

    // 3 消息收发
    // 发送 hello
    websocket.write(TextWebFrame, "hello".toArray())
    // 收
    let data = ArrayList<UInt8>()
    var frame = websocket.read()
    while(true) {
        match(frame.frameType) {
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
            case PingWebFrame =>
                websocket.writePongFrame(frame.payload)
            case _ => ()
        }
        frame = websocket.read()
    }
    println("data size: ${data.size}")      // 4097
    println("last item: ${String.fromUtf8(data.toArray()[4096])}")        // a


    // 4 关闭 websocket，
    // 收发 CloseFrame
    websocket.writeCloseFrame(status: 1000)
    let websocketFrame = websocket.read()
    println("close frame type: ${websocketFrame.frameType}")      // CloseWebFrame
    println("close frame payload: ${websocketFrame.payload}")     // 3, 232
    // 关闭底层连接
    websocket.closeConn()

    server.close()
}

func startServer() {
    // 1 注册 handler
    server.distributor.register("/webSocket", handler1)
    server.logger.level = LogLevel.OFF
    server.serve()
}

// server:
func handler1(ctx: HttpContext): Unit {
    // 2 完成 websocket 握手，获取 websocket 实例
    let websocketServer = WebSocket.upgradeFromServer(ctx, subProtocols: ArrayList<String>(["foo", "bar", "foo1"]),
        userFunc: {request: HttpRequest =>
            let value = request.headers.getFirst("test") ?? ""
            let headers = HttpHeaders()
            headers.add("rsp", value)
            headers
        })
    // 3 消息收发
    // 收 hello
    let data = ArrayList<UInt8>()
    var frame = websocketServer.read()
    while(true) {
        match(frame.frameType) {
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
            case PingWebFrame =>
                websocketServer.writePongFrame(frame.payload)
            case _ => ()
        }
        frame = websocketServer.read()
    }
    println("data: ${String.fromUtf8(data.toArray())}")    // hello
    // 发 4097 个 a
    websocketServer.write(TextWebFrame, Array<UInt8>(4097, repeat: 97))

    // 4 关闭 websocket，
    // 收发 CloseFrame
    let websocketFrame = websocketServer.read()
    println("close frame type: ${websocketFrame.frameType}")   // CloseWebFrame
    println("close frame payload: ${websocketFrame.payload}")     // 3, 232
    websocketServer.write(CloseWebFrame, websocketFrame.payload)
    // 关闭底层连接
    websocketServer.closeConn()
}
```

该示例运行结果如下：

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
