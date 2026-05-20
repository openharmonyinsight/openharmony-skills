# client

> **注意：**
>
> 以下示例仅用于展示客户端写法，可通过编译但无法运行成功。如需查看运行效果，需用户自行提供服务端配合运行。部分用例需用户自行提供有效证书文件。

## Hello World

示例：

<!-- compile -->
```cangjie
import stdx.net.http.*

main() {
    // 1. 构建 client 实例
    let client = ClientBuilder().build()
    // 2. 发送请求，收取响应，其中请求 URL 可根据实际情况修改
    let rsp = client.get("http://example.com/hello")
    // 3. 打印响应内容
    println(rsp)
    // 4. 关闭连接
    client.close()
}
```

## 自定义 client 网络配置

示例：

<!-- compile -->
```cangjie
import std.net.{TcpSocket, SocketAddress}
import std.convert.Parsable
import std.fs.*
import stdx.net.tls.*
import stdx.crypto.x509.X509Certificate
import stdx.net.http.*
import std.io.*

main() {
    // 1. 自定义配置
    // TLS 配置
    var tlsConfig = TlsClientConfig()
    // TLS 证书文件需要用户自行提供
    let pem = String.fromUtf8(readToEnd(File("/rootCerPath", Read)))
    tlsConfig.verifyMode = CustomCA(X509Certificate.decodeFromPem(pem))
    tlsConfig.alpnProtocolsList = ["h2"]
    // TCP 建连配置
    let TcpSocketConnector = {
        sa: SocketAddress =>
        let socket = TcpSocket(sa)
        socket.connect()
        return socket
    }
    // 2. 构建 client 实例
    let client = ClientBuilder().tlsConfig(tlsConfig).enablePush(false).connector(TcpSocketConnector).build()
    // 3. 发送请求，其中请求 URL 可根据实际情况修改
    let rsp = client.get("https://example.com/hello")
    // 4. 读取响应体
    let buf = Array<UInt8>(1024, repeat: 0)
    let len = rsp.body.read(buf)
    println(String.fromUtf8(buf.slice(0, len)))
    // 5. 关闭连接
    client.close()
}
```

## request 中的 chunked 与 trailer

示例：

<!-- compile -->
```cangjie
import std.io.*
import std.fs.*
import stdx.net.http.*

func checksum(chunk: Array<UInt8>): Int64 {
    var sum = 0
    for (i in chunk) {
        if (i == b'\n') {
            sum += 1
        }
    }
    return sum / 2
}

main() {
    // 1. 构建 client 实例
    let client = ClientBuilder().build()
    var requestBuilder = HttpRequestBuilder()
    // 上传的文件需要用户自行提供
    let file = File("./res.jpg", Read)
    let sum = checksum(readToEnd(file))
    let req = requestBuilder
        .method("PUT")
        .url("https://example.com/src/")
        .header("Transfer-Encoding", "chunked")
        .header("Trailer", "checksum")
        .body(FileBody("./res.jpg"))
        .trailer("checksum", sum.toString())
        .build()
    let rsp = client.send(req)
    println(rsp)
    client.close()
}

class FileBody <: InputStream {
    var file: File
    init(path: String) {
        file = File(path, Read)
    }
    public func read(buf: Array<UInt8>): Int64 {
        file.read(buf)
    }
}
```

## 配置代理

示例：

<!-- compile -->
```cangjie
import stdx.net.http.*

main() {
    // 1. 构建 client 实例
    let client = ClientBuilder().httpProxy("http://127.0.0.1:8080").build()
    // 2. 发送请求，所有请求都会被发送至 127.0.0.1 地址的 8080 端口，而不是 example.com
    // 用户可根据实际情况修改代理配置和请求 URL
    let rsp = client.get("http://example.com/hello")
    // 3. 打印响应
    println(rsp)
    // 4. 关闭连接
    client.close()
}
```
