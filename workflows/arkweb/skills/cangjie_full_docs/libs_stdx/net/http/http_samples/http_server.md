# server

> **注意：**
>
> 以下示例仅用于展示服务端写法，可编译并运行（部分用例需用户自行提供有效证书文件），但无法展示处理请求的效果。如需查看运行效果，需用户自行提供客户端对示例服务端发起请求。

## Hello 仓颉

示例：

<!-- compile -->
```cangjie
import stdx.net.http.ServerBuilder

main() {
    // 1. 构建 Server 实例
    let server = ServerBuilder().addr("127.0.0.1").port(8080).build()
    // 2. 注册 HttpRequestHandler
    server.distributor.register("/index", {
        httpContext => httpContext.responseBuilder.body("Hello 仓颉!")
    })
    // 3. 启动服务
    server.serve()
}
```

## 通过 request distributor 注册处理器

示例：

<!-- compile -->
```cangjie
import stdx.net.http.{ServerBuilder, HttpRequestHandler, FuncHandler}

main() {
    // 1. 构建 Server 实例
    let server = ServerBuilder().addr("127.0.0.1").port(8080).build()
    // 注册三个不同的 HttpRequestHandler，该服务端可根据请求路径自动分发、处理请求。
    var a: HttpRequestHandler = FuncHandler({
        httpContext => httpContext.responseBuilder.body("index")
    })
    var b: HttpRequestHandler = FuncHandler({
        httpContext => httpContext.responseBuilder.body("id")
    })
    var c: HttpRequestHandler = FuncHandler({
        httpContext => httpContext.responseBuilder.body("help")
    })
    server.distributor.register("/index", a)
    server.distributor.register("/id", b)
    server.distributor.register("/help", c)
    // 2. 启动服务
    server.serve()
}
```

## 自定义 request distributor 与处理器

示例：

<!-- compile -->
```cangjie
import stdx.net.http.*
import std.collection.HashMap

// 自定义请求分发器
class NaiveDistributor <: HttpRequestDistributor {
    let map = HashMap<String, HttpRequestHandler>()
    public func register(path: String, handler: HttpRequestHandler): Unit {
        map.add(path, handler)
    }

    public func distribute(path: String): HttpRequestHandler {
        if (path == "/index") {
            return PageHandler()
        }
        return NotFoundHandler()
    }
}

// 返回一个简单的 HTML 页面
class PageHandler <: HttpRequestHandler {
    public func handle(httpContext: HttpContext): Unit {
        httpContext.responseBuilder.body("<html></html>")
    }
}

main() {
    // 1. 构建 Server 实例并接入自定义分发器
    let server = ServerBuilder().addr("127.0.0.1").port(8080).distributor(NaiveDistributor()).build()
    // 2. 启动服务
    server.serve()
}
```

## 自定义 server 网络配置

示例：

<!-- compile -->
```cangjie
import std.io.*
import std.fs.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}
import stdx.net.http.*

main() {
    // 1. 自定义配置
    // TCP 配置
    var transportCfg = TransportConfig()
    transportCfg.readBufferSize = 8192
    // TLS 配置，需要传入配套的证书与私钥文件路径，此处证书和私钥文件需要用户自行提供
    let pem0 = String.fromUtf8(readToEnd(File("/certPath", Read)))
    let pem02 = String.fromUtf8(readToEnd(File("/keyPath", Read)))
    var tlsConfig = TlsServerConfig(X509Certificate.decodeFromPem(pem0), PrivateKey.decodeFromPem(pem02))
    tlsConfig.supportedAlpnProtocols = ["h2"]
    // 2. 构建 Server 实例
    let server = ServerBuilder()
        .addr("127.0.0.1")
        .port(8080)
        .transportConfig(transportCfg)
        .tlsConfig(tlsConfig)
        .headerTableSize(10 * 1024)
        .maxRequestHeaderSize(1024 * 1024)
        .build()
    // 3. 注册 HttpRequestHandler
    server.distributor.register("/index", {
        httpContext => httpContext.responseBuilder.body("Hello 仓颉!")
    })
    // 4. 启动服务
    server.serve()
}
```

## response 中的 chunked 与 trailer

示例：

<!-- compile -->
```cangjie
import stdx.net.http.*
import std.io.*
import std.collection.HashMap

func checksum(chunk: Array<UInt8>): Int64 {
    var sum = 0
    for (i in chunk) {
        if (i == UInt8(UInt32(r'\n'))) {
            sum += 1
        }
    }
    return sum / 2
}

main() {
    // 1. 构建 Server 实例
    let server = ServerBuilder().addr("127.0.0.1").port(8080).build()
    // 2. 注册 HttpRequestHandler
    server
        .distributor
        .register(
            "/index",
            {
                httpContext =>
                let responseBuilder = httpContext.responseBuilder
                // 设置响应头 transfer-encoding 和 trailer
                responseBuilder.header("transfer-encoding", "chunked")
                responseBuilder.header("trailer", "checkSum")
                // 用 HttpResponseWriter 分段发送响应体
                let writer = HttpResponseWriter(httpContext)
                var sum = 0
                for (_ in 0..10) {
                    let chunk = Array<UInt8>(10, repeat: 0)
                    sum += checksum(chunk)
                    writer.write(chunk)
                }
                // 发送响应 trailer，trailer 部分在响应体之后发送
                responseBuilder.trailer("checkSum", "${sum}")
            }
        )
    // 3. 启动服务
    server.serve()
}
```

## 处理重定向 request

示例：

<!-- compile -->
```cangjie
import stdx.net.http.*

main() {
    // 1. 构建 Server 实例
    let server = ServerBuilder().addr("127.0.0.1").port(8080).build()
    // 2. 注册用于重定向的 HttpRequestHandler
    server.distributor.register("/redirecta", RedirectHandler("/movedsource", 308))
    server.distributor.register("/redirectb", RedirectHandler("http://www.example.com", 308))
    // 3. 启动服务
    server.serve()
}
```

## tls 证书热加载

示例：

<!-- compile -->
```cangjie
import std.io.*
import std.fs.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}
import stdx.net.http.*

//该程序需要用户配置存在且合法的文件路径才能执行
main() {
    // 1. TLS 配置，其中 TLS 证书和私钥文件用户需自行提供
    let pem0 = String.fromUtf8(readToEnd(File("/certPath", Read)))
    let pem02 = String.fromUtf8(readToEnd(File("/keyPath", Read)))
    var tlsConfig = TlsServerConfig(X509Certificate.decodeFromPem(pem0), PrivateKey.decodeFromPem(pem02))
    tlsConfig.supportedAlpnProtocols = ["http/1.1"]
    let pem = String.fromUtf8(readToEnd(File("/rootCerPath", Read)))
    tlsConfig.verifyMode = CustomCA(X509Certificate.decodeFromPem(pem))
    // 2. 构建 Server 实例，并启动服务
    let server = ServerBuilder().addr("127.0.0.1").port(8080).tlsConfig(tlsConfig).build()
    spawn {
        server.serve()
    }
    // 3. 更新 TLS 证书和私钥，之后建立的连接将使用新的证书和私钥进行认证和加密
    server.updateCert("/newCerPath", "/newKeyPath")
    // 4. 更新 CA，双向认证时使用，之后建立的连接将使用新的 CA 进行认证
    server.updateCA("/newRootCerPath")
}
```

## server push

仅用于 HTTP/2

client:

示例：

<!-- compile -->
```cangjie
import std.io.*
import std.fs.*
import std.collection.ArrayList
import stdx.net.tls.*
import stdx.crypto.x509.X509Certificate
import stdx.net.http.*

main() {
    // 1. TLS 配置，其中 TLS 证书文件用户需自行提供
    var tlsConfig = TlsClientConfig()
    let pem = String.fromUtf8(readToEnd(File("/rootCerPath", Read)))
    tlsConfig.verifyMode = CustomCA(X509Certificate.decodeFromPem(pem))
    tlsConfig.alpnProtocolsList = ["h2"]
    // 2. 构建 Client 实例
    let client = ClientBuilder().tlsConfig(tlsConfig).build()
    // 3. 发送请求，接收响应
    let response = client.get("https://127.0.0.1.8080/index.html")
    // 4. 接收服务端推送的响应，此例中相当于请求 client.get("http://127.0.0.1.8080/picture.png") 的响应
    let pushResponses: Option<ArrayList<HttpResponse>> = response.getPush()
    client.close()
}
```

server:

示例：

<!-- compile -->
```cangjie
import std.io.*
import std.fs.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}
import stdx.net.http.*

main() {
    // 1. TLS 配置，其中 TLS 证书文件用户需自行提供
    let pem0 = String.fromUtf8(readToEnd(File("/certPath", Read)))
    let pem02 = String.fromUtf8(readToEnd(File("/keyPath", Read)))
    var tlsConfig = TlsServerConfig(X509Certificate.decodeFromPem(pem0), PrivateKey.decodeFromPem(pem02))
    tlsConfig.supportedAlpnProtocols = ["h2"]
    // 2. 构建 Server 实例
    let server = ServerBuilder().addr("127.0.0.1").port(8080).tlsConfig(tlsConfig).build()
    // 3. 注册原 request 的 handler
    server
        .distributor
        .register(
            "/index.html",
            {
                httpContext =>
                let pusher = HttpResponsePusher.getPusher(httpContext)
                match (pusher) {
                    case Some(pusher) => pusher.push("/picture.png", "GET", httpContext.request.headers)
                    case None => ()
                }
            }
        )
    // 4. 注册服务端推送请求对应的 handler
    server.distributor.register("/picture.png", {
        httpContext => httpContext.responseBuilder.body("picture.png")
    })
    // 4. 启动服务
    server.serve()
}
```
