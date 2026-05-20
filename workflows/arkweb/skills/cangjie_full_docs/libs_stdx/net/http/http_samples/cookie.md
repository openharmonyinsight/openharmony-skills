# cookie

## Client

示例：

<!-- run -->
```cangjie
import stdx.net.http.*
import stdx.encoding.url.*
import std.net.*
import std.time.*
import std.sync.*

main() {
    // 1、启动 socket 服务器
    let serverSocket = TcpServerSocket(bindAt: 0)
    serverSocket.bind()
    let fut = spawn {
        serverPacketCapture(serverSocket)
    }
    // 客户端一般从 response 中的 Set-Cookie header 中读取 cookie，并将其存入 cookieJar 中，
    // 下次发起 request 时，将其放在 request 的 Cookie header 中发送
    // 2、启动客户端
    let client = ClientBuilder().build()
    let port = (serverSocket.localAddress as IPSocketAddress)?.port ?? throw Exception("Port not found.")
    var u = URL.parse("http://127.0.0.1:${port}/a/b/c")
    var r = HttpRequestBuilder().url(u).build()
    // 3、发送 request
    client.send(r)
    r = HttpRequestBuilder().url(u).build()
    // 4、发送新 request，从 CookieJar 中取出 cookie，并转成 Cookie header 中的值
    // 此时 cookie 2=2 已经过期，因此只发送 1=1 cookie
    client.send(r)
    // 5、关闭客户端
    client.close()
    fut.get()
    serverSocket.close()
}

func serverPacketCapture(serverSocket: TcpServerSocket) {
    let server = serverSocket.accept()
    let buf = Array<UInt8>(500, repeat: 0)
    var i = server.read(buf)
    println(String.fromUtf8(buf[..i]))
    // GET /a/b/c HTTP/1.1
    // host: 127.0.0.1:44649
    // user-agent: CANGJIEUSERAGENT_1_1
    // connection: keep-alive
    // content-length: 0
    //
    // 过期时间为 4 秒的 cookie1
    let cookie1 = Cookie("1", "1", maxAge: 4, domain: "127.0.0.1", path: "/a/b/")
    let setCookie1 = cookie1.toSetCookieString()
    // 过期时间为 2 秒的 cookie2
    let cookie2 = Cookie("2", "2", maxAge: 2, path: "/a/")
    let setCookie2 = cookie2.toSetCookieString()
    // 服务器发送 Set-Cookie 头，客户端解析并将其存进 CookieJar 中
    server.write(
        "HTTP/1.1 204 ok\r\nSet-Cookie: ${setCookie1}\r\nSet-Cookie: ${setCookie2}\r\nConnection: close\r\n\r\n"
            .toArray())

    let server2 = serverSocket.accept()
    i = server2.read(buf)
    // 接收客户端的带 cookie 的请求
    println(String.fromUtf8(buf[..i]))
    // GET /a/b/c HTTP/1.1
    // host: 127.0.0.1:xxxx
    // cookie: 1=1
    // user-agent: CANGJIEUSERAGENT_1_1
    // connection: keep-alive
    // content-length: 0
    //
    server2.write("HTTP/1.1 204 ok\r\nConnection: close\r\n\r\n".toArray())
    server2.close()
}
```

运行结果：

> **注意：**
>
> 请求中 host 字段中的 port 部分是随机分配的，每次运行会打印不同值。

```text
GET /a/b/c HTTP/1.1
host: 127.0.0.1:xxxx
user-agent: CANGJIEUSERAGENT_1_1
connection: keep-alive
content-length: 0


GET /a/b/c HTTP/1.1
host: 127.0.0.1:xxxx
cookie: 1=1
user-agent: CANGJIEUSERAGENT_1_1
connection: keep-alive
content-length: 0
```

## Server

示例：

<!-- run -->
```cangjie
import stdx.net.http.*
import std.net.*
import std.sync.*

main(): Unit {
    let serverOn = SyncCounter(1)
    spawn {
        serverSetCookie(serverOn)
    }
    serverOn.waitUntilZero()
    clientPacketCapture()
}

func serverSetCookie(serverOn: SyncCounter): Unit {
    // 服务器设置 cookie 时将 cookie 放在 Set-Cookie header 中发给客户端
    // 1. 构建 Server 实例
    let server = ServerBuilder().addr("127.0.0.1").port(8080).build()
    server.afterBind({=> serverOn.dec()})
    // 2. 注册 HttpRequestHandler
    server
        .distributor
        .register(
            "/index",
            {
                httpContext =>
                let cookie = Cookie("name", "value")
                httpContext.responseBuilder.header("Set-Cookie", cookie.toSetCookieString()).body("Hello 仓颉!")
            }
        )
    // 3. 启动服务
    server.serve()
}

func clientPacketCapture(): Unit {
    // 创建客户端 socket，并连接到服务端
    let client = TcpSocket("127.0.0.1", 8080)
    client.connect()
    // 发送请求
    let request = "GET /index HTTP/1.1\r\nHost: 127.0.0.1:8080\r\n\r\n".toArray()
    client.write(request)
    // 读取响应，响应中预期包含 “set-cookie: name=value”
    let buf = Array<UInt8>(500, repeat: 0)
    var len = client.read(buf)
    println(String.fromUtf8(buf[..len]))
}
```

运行结果：

> **注意：**
>
> 响应中 date 字段表示当前日期，每次运行会打印不同的结果。

```text
HTTP/1.1 200 OK
set-cookie: name=value
connection: keep-alive
date: xxxx
content-length: 13

Hello 仓颉!
```
