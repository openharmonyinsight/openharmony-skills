---
name: cangjie-network-websocket
description: "仓颉 WebSocket 编程用法。"
---

# 仓颉语言 WebSocket 编程 Skill

## 1. 概述

- 依赖包 `stdx.net.http`，关于扩展标准库 `stdx` 的配置用法，请参阅 `cangjie-stdx` Skill
- 帧类型：**控制帧**（`CloseWebFrame`、`PingWebFrame`、`PongWebFrame`）、**数据帧**（`TextWebFrame`、`BinaryWebFrame`、`ContinuationWebFrame`）
- 帧属性：`fin`（是否最后一帧）、`frameType`、`payload`

---

## 2. 服务端升级

```cangjie
import stdx.net.http.*
import std.collection.ArrayList
import std.sync.*

main() {
    let server = ServerBuilder().addr("127.0.0.1").port(8080).build()

    server.distributor.register("/ws", {
        ctx =>
        let ws = WebSocket.upgradeFromServer(
            ctx,
            subProtocols: ArrayList<String>(["proto1"]),
            userFunc: { req =>
                let headers = HttpHeaders()
                headers.add("rsp", "ok")
                headers
            }
        )
        // 读取消息
        let frame = ws.read()
        println(String.fromUtf8(frame.payload))
        // 发送消息
        ws.write(TextWebFrame, "echo".toArray())
        // 关闭
        ws.writeCloseFrame(status: 1000)
        let _ = ws.read()  // 读取关闭响应
        ws.closeConn()
    })

    server.serve()
}
```

---

## 3. 客户端升级

```cangjie
import stdx.net.http.*
import stdx.encoding.url.*
import std.collection.*

main() {
    let client = ClientBuilder().build()
    let url = URL.parse("ws://127.0.0.1:8080/ws")
    let (ws, headers) = WebSocket.upgradeFromClient(
        client, url,
        subProtocols: ArrayList<String>(["proto1"]),
        headers: HttpHeaders()
    )

    // 发送
    ws.write(TextWebFrame, "hello".toArray())
    // 接收
    let frame = ws.read()
    println(String.fromUtf8(frame.payload))

    // 关闭流程：发送 CloseFrame → 读取 CloseFrame → 关闭底层连接
    ws.writeCloseFrame(status: 1000)
    let _ = ws.read()
    ws.closeConn()
    client.close()
}
```

---

## 4. 消息接收循环（处理分片）

```cangjie
import stdx.net.http.*
import std.collection.ArrayList

// 在 WebSocket 连接建立后，用于接收可能分片的消息
func receiveMessage(ws: WebSocket): ArrayList<UInt8> {
    let data = ArrayList<UInt8>()
    var frame = ws.read()
    while (true) {
        match (frame.frameType) {
            case TextWebFrame | BinaryWebFrame =>
                data.add(all: frame.payload)
                if (frame.fin) { break }
            case ContinuationWebFrame =>
                data.add(all: frame.payload)
                if (frame.fin) { break }
            case CloseWebFrame =>
                ws.write(CloseWebFrame, frame.payload)
                break
            case PingWebFrame => ws.writePongFrame(frame.payload)
            case _ => ()
        }
        frame = ws.read()
    }
    return data
}
```

---

## 5. 关键规则速查

1. WebSocket 关闭需三步：`writeCloseFrame` → `read` 关闭响应 → `closeConn`
2. 大消息可能分片传输，需循环接收并检查 `frame.fin` 标志
3. 收到 `PingWebFrame` 应回复 `writePongFrame`
4. `subProtocols` 用于子协议协商
