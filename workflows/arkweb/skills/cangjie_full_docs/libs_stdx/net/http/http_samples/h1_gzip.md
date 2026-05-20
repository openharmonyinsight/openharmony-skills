# h1_gzip

服务端使用 gzip 压缩报文示例

示例：

<!-- verify -->
```cangjie
import stdx.compress.zlib.*
import stdx.net.http.*
import std.collection.*
import std.io.*
import std.sync.*

main() {
    // 1. 启动服务器监听
    let port = startServer()

    // 2. 构造 http 请求
    let request = HttpRequestBuilder()
        .get()
        .url("http://127.0.0.1:${port}/hello")
        .header("Accept-Encoding", "gzip")
        .build()

    // 3. 发送 http 请求并获取相应
    let client = ClientBuilder().build()
    let rsp = client.send(request)

    // 4. 使用 gzip 解压 body
    let body = DecompressInputStream(rsp.body, wrap: GzipFormat)
    println("Rsp body: ${String.fromUtf8(readToEnd(body))}")

    0
}

func startServer(): UInt16 {
    let server = ServerBuilder().addr("127.0.0.1").port(0).build()
    server
        .distributor
        .register("/hello") {
            ctx =>
            // 1. 设置响应头
            ctx.responseBuilder.header("Transfer-Encoding", "chunked")
            ctx.responseBuilder.header("Content-Encoding", "gzip")

            // 2. 获取 body 输入流
            let rawBody = ByteBuffer()
            "hello gzip".toArray() |> rawBody.write

            // 3. 使用 gzip 压缩输入流
            let body = CompressInputStream(rawBody, wrap: GzipFormat)
            ctx.responseBuilder.body(body)
        }
    let serverOn = SyncCounter(1)
    server.afterBind({=> serverOn.dec()})

    spawn {server.serve()}
    serverOn.waitUntilZero()
    return server.port
}

func readToEnd(input: InputStream): Array<Byte> {
    let buf = Array<Byte>(200, repeat: 0)
    let result = ArrayList<Byte>()
    var len = input.read(buf)
    while (len > 0) {
        result.add(all: buf[0..len])
        len = input.read(buf)
    }
    return result.toArray()
}
```

运行结果：

```text
Rsp body: hello gzip
```
