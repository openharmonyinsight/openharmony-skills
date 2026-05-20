---
name: cangjie-network-http-client
description: "仓颉 HTTP 客户端编程用法。"
---

# 仓颉语言 HTTP 客户端编程 Skill

## 1. 概述

- 依赖 `stdx.net.http`，关于扩展标准库 `stdx` 的配置用法，请参阅 `cangjie-stdx` Skill
- 支持 HTTP/1.0、1.1、2.0（RFC 9110/9112/9113/9218/7541）
- 核心模式：`ClientBuilder` 构建 → `Client` 发送请求 → 读取响应 → `close()` 释放

---

## 2. 快速入门

```cangjie
import stdx.net.http.*
import std.io.StringReader

main() {
    // 1. 构建 Client
    let client = ClientBuilder().build()

    // 2. 发送 GET 请求
    let resp = client.get("http://example.com/hello")

    // 3. 读取响应体
    let body = StringReader(resp.body).readToEnd()
    println("Status: ${resp.status}")
    println("Body: ${body}")

    // 4. 关闭客户端，释放所有连接
    client.close()
}
```

---

## 3. ClientBuilder 配置

### 3.1 完整配置接口

| 方法 | 签名 | 说明 |
|------|------|------|
| `build` | `build(): Client` | 构建 Client 实例 |
| `tlsConfig` | `tlsConfig(TlsClientConfig): ClientBuilder` | TLS 配置（启用 HTTPS，详见 `cangjie-https-client` Skill） |
| `httpProxy` | `httpProxy(String): ClientBuilder` | HTTP 代理（格式：`"http://host:port"`） |
| `httpsProxy` | `httpsProxy(String): ClientBuilder` | HTTPS 代理 |
| `noProxy` | `noProxy(): ClientBuilder` | 不使用代理（忽略环境变量） |
| `cookieJar` | `cookieJar(?CookieJar): ClientBuilder` | Cookie 管理器（默认启用） |
| `autoRedirect` | `autoRedirect(Bool): ClientBuilder` | 自动跟随重定向（默认 true，304 不重定向） |
| `readTimeout` | `readTimeout(Duration): ClientBuilder` | 读超时（默认 15 秒） |
| `writeTimeout` | `writeTimeout(Duration): ClientBuilder` | 写超时（默认 15 秒） |
| `poolSize` | `poolSize(Int64): ClientBuilder` | HTTP/1.1 连接池大小（同一 host:port 最大连接数，默认 10） |
| `logger` | `logger(Logger): ClientBuilder` | 自定义日志（需线程安全） |
| `connector` | `connector((SocketAddress) -> StreamingSocket): ClientBuilder` | 自定义 TCP 连接函数 |

**HTTP/2 专用配置：**

| 方法 | 说明 |
|------|------|
| `enablePush(Bool)` | 是否接收服务端推送（默认 true） |
| `headerTableSize(UInt32)` | Hpack 动态表初始值（默认 4096） |
| `maxConcurrentStreams(UInt32)` | 最大并发流数 |
| `initialWindowSize(UInt32)` | 初始流控窗口大小（默认 65535） |
| `maxFrameSize(UInt32)` | 最大帧大小（默认 16384） |
| `maxHeaderListSize(UInt32)` | 最大头部列表大小 |

### 3.2 配置示例

```cangjie
import stdx.net.http.*
import std.time.*

main() {
    let client = ClientBuilder()
        .readTimeout(Duration.second * 30)
        .writeTimeout(Duration.second * 10)
        .poolSize(20)
        .autoRedirect(true)
        .build()

    let resp = client.get("http://example.com/api")
    println(resp.status)
    client.close()
}
```

---

## 4. Client 常用方法

### 4.1 快捷请求方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `get` | `get(String): HttpResponse` | GET 请求 |
| `post` | `post(String, String): HttpResponse` | POST 请求（字符串体） |
| `post` | `post(String, Array<UInt8>): HttpResponse` | POST 请求（字节体） |
| `post` | `post(String, InputStream): HttpResponse` | POST 请求（流式体） |
| `put` | `put(String, String): HttpResponse` | PUT 请求（字符串体） |
| `put` | `put(String, Array<UInt8>): HttpResponse` | PUT 请求（字节体） |
| `put` | `put(String, InputStream): HttpResponse` | PUT 请求（流式体） |
| `delete` | `delete(String): HttpResponse` | DELETE 请求 |
| `head` | `head(String): HttpResponse` | HEAD 请求 |
| `options` | `options(String): HttpResponse` | OPTIONS 请求 |
| `send` | `send(HttpRequest): HttpResponse` | 发送自定义请求 |
| `close` | `close(): Unit` | 关闭客户端，释放所有连接 |

### 4.2 快捷方法示例

```cangjie
import stdx.net.http.*
import std.io.StringReader

main() {
    let client = ClientBuilder().build()

    // GET
    let getResp = client.get("http://example.com/users")
    println(StringReader(getResp.body).readToEnd())

    // POST
    let postResp = client.post("http://example.com/users",
        "{\"name\": \"仓颉\"}")
    println(postResp.status)

    // PUT
    let putResp = client.put("http://example.com/users/1",
        "{\"name\": \"更新\"}")
    println(putResp.status)

    // DELETE
    let delResp = client.delete("http://example.com/users/1")
    println(delResp.status)

    client.close()
}
```

---

## 5. HttpRequestBuilder 自定义请求

### 5.1 完整接口

| 方法 | 签名 | 说明 |
|------|------|------|
| `url` | `url(String): HttpRequestBuilder` | 设置请求 URL |
| `url` | `url(URL): HttpRequestBuilder` | 设置请求 URL（URL 对象） |
| `method` | `method(String): HttpRequestBuilder` | 设置 HTTP 方法 |
| `get`/`post`/`put`/`delete`... | `get(): HttpRequestBuilder` 等 | 便捷方法设置 HTTP 方法 |
| `header` | `header(String, String): HttpRequestBuilder` | 添加请求头 |
| `addHeaders` | `addHeaders(HttpHeaders): HttpRequestBuilder` | 批量添加请求头 |
| `setHeaders` | `setHeaders(HttpHeaders): HttpRequestBuilder` | 替换全部请求头 |
| `body` | `body(String): HttpRequestBuilder` | 设置字符串请求体 |
| `body` | `body(Array<UInt8>): HttpRequestBuilder` | 设置字节数组请求体 |
| `body` | `body(InputStream): HttpRequestBuilder` | 设置流式请求体 |
| `trailer` | `trailer(String, String): HttpRequestBuilder` | 添加 Trailer |
| `version` | `version(Protocol): HttpRequestBuilder` | 指定协议版本 |
| `readTimeout` | `readTimeout(Duration): HttpRequestBuilder` | 请求级读超时（覆盖 Client 级别） |
| `writeTimeout` | `writeTimeout(Duration): HttpRequestBuilder` | 请求级写超时（覆盖 Client 级别） |
| `priority` | `priority(Int64, Bool): HttpRequestBuilder` | HTTP/2 优先级（urgency 0-7, incremental） |
| `build` | `build(): HttpRequest` | 构建 HttpRequest 实例 |

### 5.2 自定义请求示例

```cangjie
import stdx.net.http.*
import std.io.StringReader

main() {
    let client = ClientBuilder().build()

    // 构建自定义 POST 请求
    let req = HttpRequestBuilder()
        .post()
        .url("http://example.com/api/data")
        .header("Content-Type", "application/json")
        .header("Authorization", "Bearer token123")
        .body("{\"key\": \"value\", \"count\": 42}")
        .build()

    let resp = client.send(req)
    println("Status: ${resp.status}")
    println("Body: ${StringReader(resp.body).readToEnd()}")

    client.close()
}
```

### 5.3 请求级超时

可以为单个请求设置不同于 Client 默认值的超时：

```cangjie
import stdx.net.http.*
import std.time.*

main() {
    let client = ClientBuilder()
        .readTimeout(Duration.second * 15)
        .build()

    // 这个请求使用更长的超时
    let req = HttpRequestBuilder()
        .get()
        .url("http://example.com/slow-api")
        .readTimeout(Duration.second * 60)
        .build()

    let resp = client.send(req)
    println(resp.status)

    client.close()
}
```

---

## 6. 响应（HttpResponse）处理

### 6.1 HttpResponse 属性

| 属性/方法 | 类型 | 说明 |
|-----------|------|------|
| `status` | `UInt16` | 状态码（200、404 等） |
| `headers` | `HttpHeaders` | 响应头 |
| `body` | `InputStream` | 响应体（流式读取） |
| `bodySize` | `Option<Int64>` | 响应体大小（未知时为 None） |
| `trailers` | `HttpHeaders` | Trailer 头 |
| `version` | `Protocol` | 协议版本 |
| `close()` | `Unit` | 关闭未读完的 body 释放资源 |

### 6.2 读取响应体

```cangjie
import stdx.net.http.*
import std.io.StringReader

main() {
    let client = ClientBuilder().build()
    let resp = client.get("http://example.com/data")

    // 方式一：使用 StringReader 一次性读取全部字符串
    let body = StringReader(resp.body).readToEnd()
    println(body)

    client.close()
}
```

**逐块读取大文件：**

```cangjie
import stdx.net.http.*

main() {
    let client = ClientBuilder().build()
    let resp = client.get("http://example.com/large-file")

    // 逐块读取
    let buf = Array<UInt8>(4096, repeat: 0)
    var len = resp.body.read(buf)
    while (len > 0) {
        // 处理 buf[0..len]
        println("Read ${len} bytes")
        len = resp.body.read(buf)
    }
    // body 读完后返回 0，连接自动归还连接池

    client.close()
}
```

> **重要**：HTTP/1.1 的 `body` 必须完全读取后连接才能被复用。如不需要 body，调用 `resp.close()` 释放资源。

### 6.3 读取响应头

```cangjie
import stdx.net.http.*
import std.io.StringReader

main() {
    let client = ClientBuilder().build()
    let resp = client.get("http://example.com/api")

    // 获取单个响应头
    let contentType = resp.headers.getFirst("content-type") ?? "unknown"
    println("Content-Type: ${contentType}")

    // 遍历所有响应头
    for ((name, values) in resp.headers) {
        println("${name}: ${values.toArray()}")
    }

    // 读取 body 以释放连接
    StringReader(resp.body).readToEnd()
    client.close()
}
```

---

## 7. Cookie 管理

### 7.1 自动 Cookie 管理

`ClientBuilder` 默认启用 `CookieJar`，自动处理 `Set-Cookie` 和 `Cookie` 头：

```cangjie
import stdx.net.http.*
import std.io.StringReader

main() {
    // 默认启用 CookieJar，自动管理 Cookie
    let client = ClientBuilder().build()

    // 第一次请求：服务端通过 Set-Cookie 设置 Cookie
    let resp1 = client.get("http://example.com/login")
    StringReader(resp1.body).readToEnd()

    // 第二次请求：客户端自动携带已存储的 Cookie
    let resp2 = client.get("http://example.com/profile")
    println(StringReader(resp2.body).readToEnd())

    client.close()
}
```

### 7.2 禁用 Cookie

```cangjie
import stdx.net.http.*

main() {
    // 传 None 禁用 Cookie 管理
    let client = ClientBuilder().cookieJar(None).build()
    let resp = client.get("http://example.com/api")
    // 不会自动处理 Set-Cookie 或发送 Cookie 头
    client.close()
}
```

### 7.3 Cookie 类构造

```cangjie
Cookie(name: String, value: String,
    maxAge: Int64,          // 过期秒数
    domain: String,         // 域名
    path: String)           // 路径
```

- `toSetCookieString()` — 生成 `Set-Cookie` 头值（服务端用）
- `CookieJar.toCookieString(cookies)` — 生成 `Cookie` 头值
- `CookieJar.parseSetCookieHeader(resp)` — 解析响应中的 `Set-Cookie` 头

---

## 8. 代理配置

```cangjie
import stdx.net.http.*
import std.io.StringReader

main() {
    // HTTP 代理
    let client = ClientBuilder()
        .httpProxy("http://proxy.example.com:8080")
        .build()

    // 所有 HTTP 请求通过代理转发
    let resp = client.get("http://target.example.com/api")
    println(StringReader(resp.body).readToEnd())

    client.close()
}
```

```cangjie
import stdx.net.http.*

main() {
    // HTTPS 代理
    let client = ClientBuilder()
        .httpsProxy("http://proxy.example.com:8443")
        .build()

    let resp = client.get("https://secure.example.com/api")
    client.close()
}
```

> **说明**：默认使用系统环境变量 `http_proxy` / `https_proxy` 的值。使用 `noProxy()` 忽略环境变量代理设置。

---

## 9. 分块上传（Chunked）与 Trailer

```cangjie
import stdx.net.http.*
import std.io.*
import std.fs.*

main() {
    let client = ClientBuilder().build()

    let req = HttpRequestBuilder()
        .put()
        .url("http://example.com/upload")
        .header("Transfer-Encoding", "chunked")
        .header("Trailer", "checksum")
        .body(FileBody("./data.bin"))
        .trailer("checksum", "abc123")
        .build()

    let resp = client.send(req)
    println(resp.status)
    client.close()
}

// 自定义 InputStream 实现流式上传
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

> **注意**：HTTP/1.1 中如果有 body，必须设置 `Content-Length` 或 `Transfer-Encoding: chunked` 其中之一。使用 `String` 或 `Array<UInt8>` 设置 body 时，库会自动补充 `Content-Length`。

---

## 10. 自定义 TCP 连接

```cangjie
import std.net.{TcpSocket, SocketAddress}
import stdx.net.http.*
import std.io.StringReader

main() {
    // 自定义 TCP 连接函数
    let customConnector = {
        sa: SocketAddress =>
        let socket = TcpSocket(sa)
        socket.connect()
        return socket
    }

    let client = ClientBuilder()
        .connector(customConnector)
        .build()

    let resp = client.get("http://example.com/hello")
    println(StringReader(resp.body).readToEnd())
    client.close()
}
```

---

## 11. 日志

```cangjie
import stdx.log.*
import stdx.net.http.*

main() {
    let client = ClientBuilder().build()

    // 开启 DEBUG 级别日志
    client.logger.level = LogLevel.DEBUG

    let resp = client.get("http://example.com/api")
    client.close()
}
```

---

## 12. 异常类型

| 异常 | 说明 |
|------|------|
| `HttpException` | HTTP 通用异常（连接池满、协议错误等） |
| `HttpTimeoutException` | 请求超时或读响应体超时 |
| `HttpStatusException` | 响应状态异常 |
| `ConnectionException` | TCP 连接异常（读数据时对端已关闭） |
| `UrlSyntaxException` | URL 格式错误 |

---

## 13. 关键规则速查

| 规则 | 说明 |
|------|------|
| 读取响应体 | 使用 `StringReader(resp.body).readToEnd()` 读取字符串，或逐块 `resp.body.read(buf)` |
| 释放连接 | body 读完后连接自动归还连接池；不需要 body 时调用 `resp.close()` |
| 关闭客户端 | 使用完毕后调用 `client.close()` 释放所有连接 |
| 连接池限制 | HTTP/1.1 默认同一 host 最多 10 个连接，超出抛 `HttpException` |
| Content-Length | 使用 `String` / `Array<UInt8>` 设置 body 时自动补充；使用自定义 `InputStream` 时需手动设置 |
| 自动重定向 | 默认启用，304 状态码不重定向 |
| Cookie 管理 | 默认启用 `CookieJar`，自动处理 `Set-Cookie` / `Cookie` 头 |
| 代理 | 默认使用环境变量 `http_proxy` / `https_proxy`；`noProxy()` 禁用 |
| TRACE 请求 | 协议规定 TRACE 请求不能携带 body |
| 请求级超时 | `HttpRequestBuilder.readTimeout()` / `writeTimeout()` 覆盖 Client 级别设置 |
| HTTPS/TLS | HTTPS 配置、证书验证、HTTP/2 启用、Server Push 等，详见 `cangjie-https-client` Skill |
