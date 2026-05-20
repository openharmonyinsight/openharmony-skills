# HTTP 编程

HTTP 作为一种通用的应用层协议，通过请求-响应的机制实现数据传输，客户端发送请求，服务端返回响应。请求和响应的格式是固定的，由报文头和报文体组成。

常用的请求类型为 GET 和 POST，GET 请求只有报文头，用于向服务器请求应用层数据，POST 请求带有报文体，以一个空行与报文头进行分隔，用于向服务器提供应用层数据。

请求-响应的报文头字段内容较多，此处不再一一赘述，仓颉支持 HTTP 1.0/1.1/2.0 等协议版本，开发者可以基于协议 RFC 9110、9112、9113、9218、7541 以及仓颉所提供的 HttpRequestBuilder 和 HttpResponseBuilder 类构造请求及响应报文。

以下示例展示了如何使用仓颉进行客户端和服务端编程，实现的功能是客户端发送请求头为 GET /hello 的请求，服务端返回响应，响应体为 \"Hello Cangjie!\"，代码如下:

> **说明：**
>
> net、log 等库已从仓颉 SDK 移到 stdx 模块，使用前需要下载软件包，并在 cjpm.toml 中配置。

<!-- verify -->

```cangjie
import stdx.net.http.*
import std.time.*
import std.sync.*
import stdx.log.*

// 1. 构建 Server 实例
let server = ServerBuilder()
    .addr("127.0.0.1")
    .port(0)
    .build()

func startServer(): Unit {
    // 2. 注册请求处理逻辑
    server.distributor.register("/hello", {httpContext =>
        httpContext.responseBuilder.body("Hello Cangjie!")
    })
    server.logger.level = LogLevel.OFF
    // 3. 启动服务
    server.serve()
}

func startClient(): Unit {
    // 1. 构建 client 实例
    let client = ClientBuilder().build()
    // 2. 发送 request
    let response = client.get("http://127.0.0.1:${server.port}/hello")
    // 3. 读取response body
    let buffer = Array<Byte>(32, repeat: 0)
    let length = response.body.read(buffer)
    println(String.fromUtf8(buffer[..length]))
    // 4. 关闭连接
    client.close()
}

main () {
    spawn {
        startServer()
    }
    sleep(Duration.second)
    startClient()
}
```

编译执行上述代码，将打印：

```text
Hello Cangjie!
```
