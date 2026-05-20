# 类

## class Client

```cangjie
public class Client
```

功能：发送 Http request、随时关闭等。用户可以通过 Client 实例发送 HTTP/1.1 或 HTTP/2 请求。

> **说明：**
>
> [Client](http_package_classes.md#class-client) 文档中未明确说明支持版本的配置，在 HTTP/1.1 与 HTTP/2 都会生效。

### prop autoRedirect

```cangjie
public prop autoRedirect: Bool
```

功能：客户端是否会自动进行重定向，304 状态码默认不重定向。

类型：Bool

### prop connector

```cangjie
public prop connector: (SocketAddress) -> StreamingSocket
```

功能：客户端调用此函数获取到服务器的连接。

类型：(SocketAddress) -> StreamingSocket

### prop cookieJar

```cangjie
public prop cookieJar: ?CookieJar
```

功能：用于存储客户端所有 [Cookie](http_package_classes.md#class-cookie)，如果配置为 None，则不会启用 [Cookie](http_package_classes.md#class-cookie)。

类型：?[CookieJar](http_package_interfaces.md#interface-cookiejar)

### prop enablePush

```cangjie
public prop enablePush: Bool
```

功能：客户端 HTTP/2 是否支持服务器推送，默认值为 true。

类型：Bool

### prop headerTableSize

```cangjie
public prop headerTableSize: UInt32
```

功能：获取客户端 HTTP/2 Hpack 动态表的初始值，默认值为 4096。

类型：UInt32

### prop httpProxy

```cangjie
public prop httpProxy: String
```

功能：获取客户端 http 代理，默认使用系统环境变量 http_proxy 的值，用字符串表示，格式为：`"http://host:port"`，例如：`"http://192.168.1.1:80"`。

类型：String

### prop httpsProxy

```cangjie
public prop httpsProxy: String
```

功能：获取客户端 https 代理，默认使用系统环境变量 https_proxy 的值，用字符串表示，格式为：`"http://host:port"`，例如：`"http://192.168.1.1:443"`。

类型：String

### prop initialWindowSize

```cangjie
public prop initialWindowSize: UInt32
```

功能：获取客户端 HTTP/2 流控窗口初始值，默认值为 65535 ，取值范围为 0 至 2^31 - 1。

类型：UInt32

### prop logger

```cangjie
public prop logger: Logger
```

功能：获取客户端日志记录器，设置 logger.level 将立即生效，记录器应该是线程安全的。

类型：[Logger](../../../log/log_package_api/log_package_classes.md#class-logger)

### prop maxConcurrentStreams

```cangjie
public prop maxConcurrentStreams: UInt32
```

功能：获取客户端 HTTP/2 初始最大并发流数量，默认值为 2^31 - 1。

类型：UInt32

### prop maxFrameSize

```cangjie
public prop maxFrameSize: UInt32
```

功能：获取客户端 HTTP/2 初始最大帧大小。默认值为 16384. 取值范围为 2^14 至 2^24 - 1。

类型：UInt32

### prop maxHeaderListSize

```cangjie
public prop maxHeaderListSize: UInt32
```

功能：获取客户端支持的 HTTP/2 最大头部（Header）大小。这个大小指的是响应头部中所有头部字段（Header Field）的最大允许长度之和，其中包括所有字段名称（name）的长度、字段值（value）的长度以及每个字段自动添加的伪头开销（通常每个字段会有 32 字节的开销，这包括了 HTTP/2 协议本身为头部字段添加的伪头部信息）。默认情况下，这个最大长度被设置为 UInt32.Max。

类型：UInt32

### prop poolSize

```cangjie
public prop poolSize: Int64
```

功能：配置 HTTP/1.1 客户端使用的连接池的大小，亦可表示对同一个主机（host:port）同时存在的连接数的最大值。

类型：Int64

### prop readTimeout

```cangjie
public prop readTimeout: Duration
```

功能：获取客户端设定的读取整个响应的超时时间，默认值为 15 秒。

类型：Duration

### prop writeTimeout

```cangjie
public prop writeTimeout: Duration
```

功能：获取客户端设定的写请求的超时时间，默认值为 15 秒。

类型：Duration

### func close()

```cangjie
public func close(): Unit
```

功能：关闭客户端建立的所有连接，调用后不能继续发送请求。

### func connect(String, HttpHeaders, Protocol)

```cangjie
public func connect(url: String, header!: HttpHeaders = HttpHeaders(), version!: Protocol = HTTP1_1): (HttpResponse, ?StreamingSocket)
```

功能：发送 CONNECT 请求与服务器建立隧道，返回建连成功后的连接，连接由用户负责关闭。服务器返回 2xx 表示建连成功，否则建连失败（不支持自动重定向，3xx 也视为失败）。

参数：

- url: String - 请求的 url。
- header!: [HttpHeaders](http_package_classes.md#class-httpheaders) - 请求头，默认为空请求头。
- version!: [Protocol](http_package_enums.md#enum-protocol) - 请求的协议，默认为 [HTTP1_1](./http_package_enums.md#enum-protocol)。

返回值：

- ([HttpResponse](http_package_classes.md#class-httpresponse), ?StreamingSocket) - 返回元组类型，其中 [HttpResponse](http_package_classes.md#class-httpresponse) 实例表示服务器返回的响应体，Option\<StreamingSocket> 实例表示请求成功时返回 headers 之后连接。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func delete(String)

```cangjie
public func delete(url: String): HttpResponse
```

功能：请求方法为 DELETE 的便捷请求函数。

参数：

- url: String - 请求的 url。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func get(String)

```cangjie
public func get(url: String): HttpResponse
```

功能：请求方法为 GET 的便捷请求函数。

参数：

- url: String - 请求的 url。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func getTlsConfig()

```cangjie
public func getTlsConfig(): ?TlsClientConfig
```

功能：获取客户端设定的 TLS 层配置。

返回值：

- ?[TlsClientConfig](../../tls/tls_package_api/tls_package_structs.md#struct-tlsclientconfig) - 客户端设定的 TLS 层配置，如果没有设置则返回 None。

### func head(String)

```cangjie
public func head(url: String): HttpResponse
```

功能：请求方法为 HEAD 的便捷请求函数。

参数：

- url: String - 请求的 url。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func options(String)

```cangjie
public func options(url: String): HttpResponse
```

功能：请求方法为 OPTIONS 的便捷请求函数。

参数：

- url: String - 请求的 url。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func post(String, Array\<UInt8>)

```cangjie
public func post(url: String, body: Array<UInt8>): HttpResponse
```

功能：请求方法为 POST 的便捷请求函数。

参数：

- url: String - 请求的 url。
- body: Array\<UInt8> - 请求体。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func post(String, InputStream)

```cangjie
public func post(url: String, body: InputStream): HttpResponse
```

功能：请求方法为 POST 的便捷请求函数。

参数：

- url: String - 请求的 url。
- body: InputStream - 请求体。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func post(String, String)

```cangjie
public func post(url: String, body: String): HttpResponse
```

功能：请求方法为 POST 的便捷请求函数。

参数：

- url: String - 请求的 url。
- body: String - 请求体。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func put(String, Array\<UInt8>)

```cangjie
public func put(url: String, body: Array<UInt8>): HttpResponse
```

功能：请求方法为 PUT 的便捷请求函数。

参数：

- url: String - 请求的 url。
- body: Array\<UInt8> - 请求体。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func put(String, InputStream)

```cangjie
public func put(url: String, body: InputStream): HttpResponse
```

功能：请求方法为 PUT 的便捷请求函数。

参数：

- url: String - 请求的 url。
- body: InputStream - 请求体。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func put(String, String)

```cangjie
public func put(url: String, body: String): HttpResponse
```

功能：请求方法为 PUT 的便捷请求函数。

参数：

- url: String - 请求的 url。
- body: String - 请求体。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当参数 url 不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 解析规范时，抛出异常。
- IllegalArgumentException - 当被编码的字符不符合 UTF-8 的字节序列规则时，抛出异常。
- 其余同 func send。

### func send(HttpRequest)

```cangjie
public func send(req: HttpRequest): HttpResponse
```

功能：通用请求函数，发送 [HttpRequest](http_package_classes.md#class-httprequest) 到 url 中的服务器，接收 [HttpResponse](http_package_classes.md#class-httpresponse)。

> **注意：**
>
> - 对于 HTTP/1.1，如果请求中有 body 要发，那么需要保证 Content-Length 和 Transfer-Encoding: chunked 必有且只有一个，以 chunked 形式发时，每段 chunk 最大为 8192 字节；如果用户发送的 body 为自己实现的 InputStream 类，则需要自己保证 Content-Length 和 Transfer-Encoding: chunked 设置且只设置了一个；如果用户采用默认的 body 发送，Content-Length 和 Transfer-Encoding: chunked 都缺失时，我们会为其补上 Content-Length header，值为 body.size；
> - 用户如果设置了 Content-Length，则需要保证其正确性：如果所发 body 的内容大于等于 Content-Length 的值，我们会发送长度为 Content-Length 值的数据；如果所发 body 的内容小于 Content-Length 的值，此时如果 body 是默认的 body，则会抛出 [HttpException](http_package_exceptions.md#class-httpexception)，如果 body 是用户自己实现的 InputStream 类，其行为便无法保证（可能会造成服务器端的读 request 超时或者客户端的收 response 超时）；
> - 升级函数通过 [WebSocket](http_package_classes.md#class-websocket) 的 upgradeFromClient 或 [Client](http_package_classes.md#class-client) 的 [upgrade](http_package_funcs.md#func-upgradehttpcontext) 接口发出，调用 client 的其他函数发送 [upgrade](http_package_funcs.md#func-upgradehttpcontext) 请求会抛出异常；
> - 协议规定 TRACE 请求无法携带内容，故用户发送带有 body 的 TRACE 请求时会抛出异常；
> - HTTP/1.1 默认对同一个服务器的连接数不超过 10 个。response 的 body 需要用户调用 `body.read(buf: Array<Byte>)` 函数去读。body 被读完后，连接才能被客户端对象复用，否则请求相同的服务器也会新建连接。新建连接时如果连接数超出限制则会抛出 [HttpException](http_package_exceptions.md#class-httpexception)；
> - body.read 函数将 body 读完之后返回 0，如果读的时候连接断开会抛出 [ConnectionException](http_package_exceptions.md#class-connectionexception)；
> - HTTP/1.1 的升级请求如果收到 101 响应，则表示切换协议，此连接便不归 client 管理；
> - 下文的快捷请求函数的注意点与 send 相同。

参数：

- req: [HttpRequest](http_package_classes.md#class-httprequest) - 发送的请求。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 服务端返回处理该请求的响应。

异常：

- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 请求中 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 错误时抛此异常。
- SocketException - Socket 连接出现错误时抛此异常。
- [ConnectionException](http_package_exceptions.md#class-connectionexception) - 从连接中读数据时对端已关闭连接抛此异常。
- SocketTimeoutException - Socket 连接超时抛此异常。
- [TlsException](../../tls/tls_package_api/tls_package_exceptions.md#class-tlsexception) - Tls 连接建立失败或通信异常抛此异常。
- [HttpException](http_package_exceptions.md#class-httpexception) - 当用户未使用 http 库提供的 API 升级 [WebSocket](http_package_classes.md#class-websocket) 时抛此异常。
- [HttpTimeoutException](http_package_exceptions.md#class-httptimeoutexception) - 请求超时或读 [HttpResponse](http_package_classes.md#class-httpresponse).body 超时抛此异常。

### func upgrade(HttpRequest)

```cangjie
public func upgrade(req: HttpRequest): (HttpResponse, ?StreamingSocket)
```

功能：发送请求并升级协议，用户设置请求头，返回升级后的连接（如果升级成功），连接由用户负责关闭。

> **说明：**
>
> - 服务器返回 101 表示升级成功，获取到了 StreamingSocket；
> - 必选请求头：
>     - Upgrade:  protocol-name ["/" protocol-version]；
>     - Connection: Upgrade（在请求头包含 Upgrade 字段时会自动添加）；
> - 不支持 HTTP/1.0、HTTP/2；
> - 不支持 HTTP/1.1 CONNECT 方法的 [HttpRequest](http_package_classes.md#class-httprequest)。

参数：

- req: [HttpRequest](http_package_classes.md#class-httprequest) - 升级时发送的请求。

返回值：

- ([HttpResponse](http_package_classes.md#class-httpresponse),?StreamingSocket) - 返回一个元组，[HttpResponse](http_package_classes.md#class-httpresponse) 实例表示服务器返回的响应，?StreamingSocket 实例表示获取的底层连接，升级失败时为 None。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) -
    - 请求报文或响应报文不符合协议；
    - 请求报文不含 Upgrade 头；
    - 发送 CONNECT 请求；
    - 发送带 body 的 TRACE 请求；
- SocketException，[ConnectionException](http_package_exceptions.md#class-connectionexception) - Socket 连接出现异常或被关闭；
- SocketTimeoutException - Socket 连接超时；
- [TlsException](../../tls/tls_package_api/tls_package_exceptions.md#class-tlsexception) - Tls 连接建立失败或通信异常。

## class ClientBuilder

```cangjie
public class ClientBuilder {
    public init()
}
```

功能：用于 [Client](http_package_classes.md#class-client) 实例的构建，[Client](http_package_classes.md#class-client) 没有公开的构造函数，用户只能通过 [ClientBuilder](http_package_classes.md#class-clientbuilder) 得到 [Client](http_package_classes.md#class-client) 实例。[ClientBuilder](http_package_classes.md#class-clientbuilder) 文档中未明确说明支持版本的配置，在 HTTP/1.1 与 HTTP/2 都会生效。

> **说明：**
>
> 该类提供了一系列配置参数的函数，配置完成后调用 [build](./http_package_classes.md#func-build) 函数构造出 [Client](./http_package_classes.md#class-client) 实例。配置函数中说明了参数的取值范围，但配置函数本身不做参数合法性校验，[build](./http_package_classes.md#func-build) 时统一进行校验。

### init()

```cangjie
public init()
```

功能：创建新的 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例。

### func autoRedirect(Bool)

```cangjie
public func autoRedirect(auto: Bool): ClientBuilder
```

功能：配置客户端是否会自动进行重定向。重定向会请求 Location 头的资源，协议规定，Location 只能包含一个 URI 引用 Location = URI-reference，详见 [RFC 9110 10.2.2.](https://httpwg.org/specs/rfc9110.html#rfc.section.10.2.2)。304 状态码默认不重定向。

参数：

- auto: Bool - 默认值为 true，即开启自动重定向。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func build()

```cangjie
public func build(): Client
```

功能：构造 [Client](http_package_classes.md#class-client) 实例。

此处会对各参数的值进行检查，如果取值非法，将抛出异常。各参数的取值范围详见设置参数相关的函数。

返回值：

- [Client](http_package_classes.md#class-client) - 用当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例中的配置构建的 [Client](http_package_classes.md#class-client) 实例。

异常：

- IllegalArgumentException - 配置项有非法参数时抛出此异常。

### func connector((SocketAddress) -> StreamingSocket)

```cangjie
public func connector(c: (SocketAddress) -> StreamingSocket): ClientBuilder
```

功能：客户端调用此函数获取到服务器的连接。

参数：

- c: (SocketAddress) ->StreamingSocket - 入参为 SocketAddress 实例，返回值类型为 StreamingSocket 的函数类型。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func cookieJar(?CookieJar)

```cangjie
public func cookieJar(cookieJar: ?CookieJar): ClientBuilder
```

功能：用于存储客户端所有 [Cookie](http_package_classes.md#class-cookie)。

参数：

- cookieJar: ?[CookieJar](http_package_interfaces.md#interface-cookiejar) - 默认使用一个空的 [CookieJar](http_package_interfaces.md#interface-cookiejar)，如果配置为 None 则不会启用 [Cookie](http_package_classes.md#class-cookie)。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func enablePush(Bool)

```cangjie
public func enablePush(enable: Bool): ClientBuilder
```

功能：配置客户端 HTTP/2 是否支持服务器推送。

参数：

- enable: Bool - 默认值 true。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func headerTableSize(UInt32)

```cangjie
public func headerTableSize(size: UInt32): ClientBuilder
```

功能：配置客户端 HTTP/2 Hpack 动态表初始值。

参数：

- size: UInt32 - 默认值 4096。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func httpProxy(String)

```cangjie
public func httpProxy(addr: String): ClientBuilder
```

功能：设置客户端 http 代理，默认使用系统环境变量 http_proxy 的值。

参数：

- addr: String - 格式为：`"http://host:port"`，例如：`"http://192.168.1.1:80"`。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func httpsProxy(String)

```cangjie
public func httpsProxy(addr: String): ClientBuilder
```

功能：设置客户端 https 代理，默认使用系统环境变量 https_proxy 的值。

参数：

- addr: String - 格式为：`"http://host:port"`，例如：`"http://192.168.1.1:443"`。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func initialWindowSize(UInt32)

```cangjie
public func initialWindowSize(size: UInt32): ClientBuilder
```

功能：配置客户端 HTTP/2 流控窗口初始值。

参数：

- size: UInt32 - 默认值 65535 ， 取值范围为 0 至 2^31 - 1。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func logger(Logger)

```cangjie
public func logger(logger: Logger): ClientBuilder
```

功能：设定客户端的 logger，默认 logger 级别为 INFO，logger 内容将写入 Console.stdout。

参数：

- logger: [Logger](../../../log/log_package_api/log_package_classes.md#class-logger) - 需要是线程安全的，默认使用内置线程安全 logger。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func maxConcurrentStreams(UInt32)

```cangjie
public func maxConcurrentStreams(size: UInt32): ClientBuilder
```

功能：配置客户端 HTTP/2 初始最大并发流数量。

参数：

- size: UInt32 - 默认值为 2^31 - 1。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func maxFrameSize(UInt32)

```cangjie
public func maxFrameSize(size: UInt32): ClientBuilder
```

功能：配置客户端 HTTP/2 初始最大帧大小。

参数：

- size: UInt32 - 默认值为 16384。取值范围为 2^14 至 2^24 - 1。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func maxHeaderListSize(UInt32)

```cangjie
public func maxHeaderListSize(size: UInt32): ClientBuilder
```

功能：获取客户端支持的 HTTP/2 最大头部（Header）大小。这个大小指的是响应头部中所有头部字段（Header Field）的最大允许长度之和，其中包括所有字段名称（name）的长度、字段值（value）的长度以及每个字段自动添加的伪头开销（通常每个字段会有 32 字节的开销，这包括了 HTTP/2 协议本身为头部字段添加的伪头部信息）。默认情况下，这个最大长度被设置为 UInt32.Max。

参数：

- size: UInt32 - 客户端接收的 HTTP/2 响应 headers 最大长度。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func noProxy()

```cangjie
public func noProxy(): ClientBuilder
```

功能：调用此函数后，客户端不使用任何代理。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func poolSize(Int64)

```cangjie
public func poolSize(size: Int64): ClientBuilder
```

功能：配置 HTTP/1.1 客户端使用的连接池的大小，亦可表示对同一个主机（host:port）同时存在的连接数的最大值。

参数：

- size: Int64 - 默认 10，poolSize 需要大于 0。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 如果传参小于等于 0，则会抛出该异常。

### func readTimeout(Duration)

```cangjie
public func readTimeout(timeout: Duration): ClientBuilder
```

功能：设定客户端读取一个响应的最大时长。

参数：

- timeout: Duration - 默认 15s，Duration.Max 代表不限制，如果传入负的 Duration 将被替换为 Duration.Zero。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func tlsConfig(TlsClientConfig)

```cangjie
public func tlsConfig(config: TlsClientConfig): ClientBuilder
```

功能：设置 TLS 层配置，默认不对其进行设置。

参数：

- config: [TlsClientConfig](../../tls/tls_package_api/tls_package_structs.md#struct-tlsclientconfig) - 设定支持 tls 客户端需要的配置信息。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

### func writeTimeout(Duration)

```cangjie
public func writeTimeout(timeout: Duration): ClientBuilder
```

功能：设定客户端发送一个请求的最大时长。

参数：

- timeout: Duration - 默认 15 秒，Duration.Max 代表不限制，如果传入负的 Duration 将被替换为 Duration.Zero。

返回值：

- [ClientBuilder](http_package_classes.md#class-clientbuilder) - 当前 [ClientBuilder](http_package_classes.md#class-clientbuilder) 实例的引用。

## class Cookie

```cangjie
public class Cookie {
    public init(name: String, value: String, expires!: ?DateTime = None, maxAge!: ?Int64 = None,
        domain!: String = "", path!: String = "", secure!: Bool = false, httpOnly!: Bool = false)
}
```

功能：HTTP 本身是无状态的，server 为了知道 client 的状态，提供个性化的服务，便可以通过 [Cookie](http_package_classes.md#class-cookie) 来维护一个有状态的会话。

> **说明：**
>
> - 用户首次访问某站点时，server 通过 `Set-Cookie` header 将 name/value 对，以及 attribute-value 传给用户代理；用户代理随后对该站点的请求中便可以将 name/value 加入到 Cookie header 中；
> - [Cookie](http_package_classes.md#class-cookie) 类提供了构建 [Cookie](http_package_classes.md#class-cookie) 对象，并将 [Cookie](http_package_classes.md#class-cookie) 对象转成 `Set-Cookie` header 值的函数，提供了获取 [Cookie](http_package_classes.md#class-cookie) 对象各属性值的函数；
> - [Cookie](http_package_classes.md#class-cookie) 的各个属性的要求和作用见 [RFC 6265](https://httpwg.org/specs/rfc6265.html)；
> - 下文中 cookie-name，cookie-value，expires-av 等名字采用 [RFC 6265](https://httpwg.org/specs/rfc6265.html) 中的术语，详情请见协议。

### prop cookieName

```cangjie
public prop cookieName: String
```

功能：获取 [Cookie](http_package_classes.md#class-cookie) 对象的 cookie-name 值。

类型：String

### prop cookieValue

```cangjie
public prop cookieValue: String
```

功能：获取 [Cookie](http_package_classes.md#class-cookie) 对象的 cookie-value 值。

类型：String

### prop domain

```cangjie
public prop domain: String
```

功能：获取 [Cookie](http_package_classes.md#class-cookie) 对象的 domain-av 值。

类型：String

### prop expires

```cangjie
public prop expires: ?DateTime
```

功能：获取 [Cookie](http_package_classes.md#class-cookie) 对象的 expires-av 值。

类型：?DateTime

### prop httpOnly

```cangjie
public prop httpOnly: Bool
```

功能：获取 [Cookie](http_package_classes.md#class-cookie) 对象的 httpOnly-av 值。

类型：Bool

### prop maxAge

```cangjie
public prop maxAge: ?Int64
```

功能：获取 [Cookie](http_package_classes.md#class-cookie) 对象的 max-age-av 值。

类型：?Int64

### prop others

```cangjie
public prop others: ArrayList<String>
```

功能：获取未被解析的属性。

类型：ArrayList\<String>

### prop path

```cangjie
public prop path: String
```

功能：获取 [Cookie](http_package_classes.md#class-cookie) 对象的 path-av 值。

类型：String

### prop secure

```cangjie
public prop secure: Bool
```

功能：获取 [Cookie](http_package_classes.md#class-cookie) 对象的 secure-av 值。

类型：Bool

### init(String, String, ?DateTime, ?Int64, String, String, Bool, Bool)

```cangjie
public init(name: String, value: String, expires!: ?DateTime = None, maxAge!: ?Int64 = None,
    domain!: String = "", path!: String = "", secure!: Bool = false, httpOnly!: Bool = false)
```

功能：[Cookie](http_package_classes.md#class-cookie) 构造器。该构造器会检查传入的各项属性是否满足协议要求，如果不满足则会产生 IllegalArgumentException。具体要求见 [RFC 6265 4.1.1.](https://httpwg.org/specs/rfc6265.html#sane-set-cookie-syntax)。

> **注意：**
>
> [Cookie](http_package_classes.md#class-cookie) 各属性中只有 cookie-name，cookie-value 是必需的，必须传入 name，value 参数，但 value 参数可以传入空字符串。

参数：

- name: String - cookie-name 属性。

    ```cangjie
    name         = token
    token        = 1*tchar
    tchar        = "!" / "#" / "$" / "%" / "&" / "'" / "*"
                   / "+" / "-" / "." / "^" / "_" / "`" / "|" / "~"
                   / DIGIT / ALPHA
    ```

- value: String - cookie-value 属性。

    ```cangjie
    value        = *cookie-octet / ( DQUOTE *cookie-octet DQUOTE )
    cookie-octet = %x21 / %x23-2B / %x2D-3A / %x3C-5B / %x5D-7E
                ; US-ASCII characters excluding CTLs,
                ; whitespace DQUOTE, comma, semicolon,
                ; and backslash
    ```

- expires!: ?DateTime - 设置 [Cookie](http_package_classes.md#class-cookie) 的过期时间，默认为 None，时间必须在 1601 年之后。
- maxAge!: ?Int64 - [Cookie](http_package_classes.md#class-cookie) 的最大生命周期，默认为 None，如果 [Cookie](http_package_classes.md#class-cookie) 既有 expires 属性，也有 maxAge，则表示该 [Cookie](http_package_classes.md#class-cookie) 只维护到会话结束（维护到 [Client](http_package_classes.md#class-client) 关闭之前，[Client](http_package_classes.md#class-client) 关闭之后设置了过期的 [Cookie](http_package_classes.md#class-cookie) 也不再维护）。

    ```cangjie
    max-age-av     = "Max-Age=" non-zero-digit *DIGIT
    non-zero-digit = %x31-39
                    ; digits 1 through 9
    DIGIT          = %x30-39
                    ; digits 0 through 9
    ```

- domain!: String - 默认为空字符串，表示该收到该 [Cookie](http_package_classes.md#class-cookie) 的客户端只会发送该 [Cookie](http_package_classes.md#class-cookie) 给原始服务器。如果设置了合法的 domain，则收到该 [Cookie](http_package_classes.md#class-cookie) 的客户端只会发送该 [Cookie](http_package_classes.md#class-cookie) 给所有该 domain 的子域（且满足其他属性条件要求才会发）。

    ```cangjie
    domain          = <subdomain> | " "
    <subdomain>   ::= <label> | <subdomain> "." <label>
    <label>       ::= <letter> [ [ <ldh-str> ] <let-dig> ]
    <ldh-str>     ::= <let-dig-hyp> | <let-dig-hyp> <ldh-str>
    <let-dig-hyp> ::= <let-dig> | "-"
    <let-dig>     ::= <letter> | <digit>
    <letter>      ::= any one of the 52 alphabetic characters A through Z in upper case and a through z in lower case
    <digit>       ::= any one of the ten digits 0 through 9
    RFC 1035 2.3.1.
    而 RFC 1123 2.1. 放松了对 label 首字符必须是 letter 的限制
    因此，对 domain 的要求为：
    1、总长度小于等于 255，由若干个 label 组成
    2、label 与 label 之间通过 "." 分隔，每个 label 长度小于等于 63
    3、label 的开头和结尾必须是数字或者字母，label 的中间字符必须是数字、字母或者 "-"
    ```

- path!: String - 默认为空字符串，客户端会根据 url 计算出默认的 path 属性，见 RFC 6265 5.1.4.。 收到该 [Cookie](http_package_classes.md#class-cookie) 的客户端只会发送该 [Cookie](http_package_classes.md#class-cookie) 给所有该 path 的子目录（且满足其他属性条件要求才会发）。

    ```cangjie
    path            = <any RUNE except CTLs or ";">
    RUNE            = <any [USASCII] character>
    CTLs            = <controls>
    ```

- secure!: Bool - 默认为 false，如果设置为 true，该 [Cookie](http_package_classes.md#class-cookie) 只会在安全协议请求中发送。
- httpOnly!: Bool - 默认为 false，如果设置为 true，该 [Cookie](http_package_classes.md#class-cookie) 只会在 HTTP 协议请求中发送。

异常：

- IllegalArgumentException - 传入的参数不符合协议要求时抛出异常。

### func toSetCookieString()

```cangjie
public func toSetCookieString(): String
```

功能：提供将 [Cookie](http_package_classes.md#class-cookie) 转成字符串形式的函数，方便 server 设置 `Set-Cookie` header。

> **注意：**
>
> - [Cookie](http_package_classes.md#class-cookie) 各属性（包含 name，value）在对象创建时就被检查了，因此 toSetCookieString() 函数不会产生异常；
> - [Cookie](http_package_classes.md#class-cookie) 必需的属性是 cookie-pair 即 cookie-name "=" cookie-value，cookie-value 可以为空字符串，toSetCookieString() 函数只会将设置过的属性写入字符串，即只有 "cookie-name=" 是必有的，其余部分是否存在取决于是否设置。

返回值：

- String - 字符串对象，用于设置 `Set-Cookie` header。

## class FileHandler

```cangjie
public class FileHandler <: HttpRequestHandler {
    public init(path: String, handlerType!: FileHandlerType = DownLoad, bufferSize!: Int64 = 64 * 1024)
}
```

功能：用于处理文件下载或者文件上传。

文件下载：

- 构造 [FileHandler](http_package_classes.md#class-filehandler) 时需要传入待下载文件的路径，目前一个 [FileHandler](http_package_classes.md#class-filehandler) 只能处理一个文件的下载；
- 下载文件只能使用 GET 请求，其他请求返回 400 状态码；
- 文件如果不存在，将返回 404 状态码。

文件上传：

- 构造 [FileHandler](http_package_classes.md#class-filehandler) 时需要传入一个存在的目录路径，上传到服务端的文件将保存在这个目录中；
- 上传文件时只能使用 POST 请求，其他请求返回 400 状态码；
- 上传数据的 http 报文必须是 `multipart/form-data` 格式的，`Content-Type` 头字段的值为 `multipart/form-data; boundary=----XXXXX`；
- 上传文件的文件名存放在 `form-data` 数据报文中，报文数据格式为 `Content-Disposition: form-data; name="xxx"; filename="xxxx"`，文件名是 `filename` 字段的值；
- 目前 form-data 中必须包含 filename 字段；
- 如果请求报文不正确，将返回 400 状态码；
- 如果出现其他异常，例如文件处理异常，将返回 500 状态码。

父类型：

- [HttpRequestHandler](http_package_interfaces.md#interface-httprequesthandler)

### init(String, FileHandlerType, Int64)

```cangjie
public init(path: String, handlerType!: FileHandlerType = DownLoad, bufferSize!: Int64 = 64 * 1024)
```

功能：[FileHandler](http_package_classes.md#class-filehandler) 的构造函数。

参数：

- path: String - [FileHandler](http_package_classes.md#class-filehandler) 构造时需要传入的文件或者目录路径字符串，上传模式中只能传入存在的目录路径；路径中存在../时，用户需要确认标准化后的绝对路径是期望传入的路径。
- handlerType!: [FileHandlerType](http_package_enums.md#enum-filehandlertype) - 构造 [FileHandler](http_package_classes.md#class-filehandler) 时指定当前 [FileHandler](http_package_classes.md#class-filehandler) 的工作模式，默认为 DownLoad 下载模式。
- bufferSize!: Int64 - 内部从网络读取或者写入的缓冲区大小，默认值为 64*1024（64k），若小于 4096，则使用 4096 作为缓冲区大小。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 当 path 不存在时，抛出异常。
- IllegalArgumentException - 参数错误时抛出异常，如 path 为空或者包含空字符串等。

### func handle(HttpContext)

```cangjie
public func handle(ctx: HttpContext): Unit
```

功能：根据请求对响应数据进行处理。

参数：

- ctx: [HttpContext](http_package_classes.md#class-httpcontext) - Http 请求上下文。

## class FuncHandler

```cangjie
public class FuncHandler <: HttpRequestHandler {
    public FuncHandler(let handler: (HttpContext) -> Unit)
}
```

功能：[HttpRequestHandler](http_package_interfaces.md#interface-httprequesthandler) 接口包装类，把单个函数包装成 [HttpRequestHandler](http_package_interfaces.md#interface-httprequesthandler)。

父类型：

- [HttpRequestHandler](http_package_interfaces.md#interface-httprequesthandler)

### FuncHandler((HttpContext) -> Unit)

```cangjie
public FuncHandler(let handler: (HttpContext) -> Unit)
```

功能：[FuncHandler](http_package_classes.md#class-funchandler) 的构造函数。

参数：

- handler: ([HttpContext](http_package_classes.md#class-httpcontext)) -> Unit - 是调用 handle 的处理函数。

### func handle(HttpContext)

```cangjie
public func handle(ctx: HttpContext): Unit
```

功能：处理 Http 请求。

参数：

- ctx: [HttpContext](http_package_classes.md#class-httpcontext) - Http 请求上下文。

## class HttpContext

```cangjie
public class HttpContext
```

功能：Http 请求上下文，作为 [HttpRequestHandler](http_package_interfaces.md#interface-httprequesthandler).handle 函数的参数在服务端使用。

### prop clientCertificate

```cangjie
public prop clientCertificate: ?Array<X509Certificate>
```

功能：获取 Http 客户端证书。

类型：?Array\<[X509Certificate](../../../crypto/x509/x509_package_api/x509_package_classes.md#class-x509certificate)>

### prop request

```cangjie
public prop request: HttpRequest
```

功能：获取 Http 请求。

类型：[HttpRequest](http_package_classes.md#class-httprequest)

### prop responseBuilder

```cangjie
public prop responseBuilder: HttpResponseBuilder
```

功能：获取 Http 响应构建器。

类型：[HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder)

### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：使用 HTTP/1.1 协议时，判断 socket 是否已关闭；使用 HTTP/2 协议时，判断 HTTP/2 流是否已关闭。

返回值：

- Bool - 如果 HTTP/1.1 的 socket 或 HTTP/2 的流已关闭，返回 true，否则返回 false。

## class HttpHeaders

```cangjie
public class HttpHeaders <: Iterable<(String, Collection<String>)>
```

功能：此类用于表示 Http 报文中的 header 和 trailer，定义了相关增、删、改、查操作。

> **说明：**
>
> - header 和 trailer 为键值映射集，由若干 field-line 组成，每一个 field-line 包含一个键 (field -name) 和若干值 (field-value)。
> - field-name 由 token 字符组成，不区分大小写，在该类中将转为小写保存。
> - field-value 由 vchar，SP 和 HTAB 组成，vchar 表示可见的 US-ASCII 字符，不得包含前后空格，不得为空值。
> - 详见 [rfc 9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-fields)。

示例：

```text
Example-Field: Foo, Bar
key: Example-Field, value: Foo, Bar
field-name = token
token = 1*tchar
tchar = "!" / "#" / "$" / "%" / "&" / "'" / "*"
/ "+" / "-" / "." / "^" / "_" / "`" / "|" / "~"
/ DIGIT / ALPHA
; any VCHAR, except delimiters
```

父类型：

- Iterable\<(String, Collection\<String>)>

### func add(String, String)

```cangjie
public func add(name: String, value: String): Unit
```

功能：添加指定键值对。如果 name 已经存在，将在其对应的值列表中添加 value；如果 name 不存在，则添加 name 字段及其值 value。

参数：

- name: String - [HttpHeaders](http_package_classes.md#class-httpheaders) 的字段名称。
- value: String - [HttpHeaders](http_package_classes.md#class-httpheaders) 的字段值。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 如果传入的 name/value 包含不合法元素，将抛出此异常。

### func del(String)

```cangjie
public func del(name: String): Unit
```

功能：删除指定 name 对应的键值对。

参数：

- name: String - 删除的字段名称。

### func get(String)

```cangjie
public func get(name: String): Collection<String>
```

功能：获取指定 name 对应的 value 值。

参数：

- name: String - 字段名称，不区分大小写。

返回值：

- Collection\<String> - name 对应的 value 集合，如果指定 name 不存在，返回空集合。

### func getFirst(String)

```cangjie
public func getFirst(name: String): ?String
```

功能：获取指定 name 对应的第一个 value 值。

参数：

- name: String - 字段名称，不区分大小写。

返回值：

- ?String - name 对应的第一个 value 值，如果指定 name 不存在，返回 None。

### func isEmpty()

```cangjie
public func isEmpty(): Bool
```

功能：判断当前实例是否为空，即没有任何键值对。

返回值：

- Bool - 如果当前实例为空，返回 true，否则返回 false。

### func iterator()

```cangjie
public func iterator(): Iterator<(String, Collection<String>)>
```

功能：获取迭代器，可用于遍历所有键值对。

返回值：

- Iterator\<(String, Collection\<String>)> - 该键值集的迭代器。

### func set(String, String)

```cangjie
public func set(name: String, value: String): Unit
```

功能：设置指定键值对。如果 name 已经存在，传入的 value 将会覆盖之前的值。

参数：

- name: String - [HttpHeaders](http_package_classes.md#class-httpheaders) 的字段名称。
- value: String - [HttpHeaders](http_package_classes.md#class-httpheaders) 的字段值。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 如果传入的 name/values 包含不合法元素，将抛出此异常。

## class HttpRequest

```cangjie
public class HttpRequest <: ToString
```

功能：此类为 Http 请求类。

客户端发送请求时，需要构造一个 [HttpRequest](http_package_classes.md#class-httprequest) 实例，再编码成字节报文发出。

服务端处理请求时，需要把收到的请求解析成 [HttpRequest](http_package_classes.md#class-httprequest) 实例，并传给 handler 处理函数。

父类型：

- ToString

### prop body

```cangjie
public prop body: InputStream
```

功能：获取 body。

> **注意：**
>
> - body 不支持并发读取；
> - 默认 InputStream 实现类的 read 函数不支持多次读取。

类型：InputStream

### prop bodySize

```cangjie
public prop bodySize: Option<Int64>
```

功能：获取请求 body 长度。

- 如果未设置 body，则 bodySize 为 Some(0)；
- 如果 body 长度已知，即通过 Array\<UInt8> 或 String 传入 body，或传入的 InputStream 有确定的 length (length >= 0)，则 bodySize 为 Some(Int64)；
- 如果 body 长度未知，即通过用户自定义的 InputStream 实例传入 body 且 InputStream 实例没有确定的 length (length < 0)，则 bodySize 为 None。

类型：Option\<Int64>

### prop isPersistent

```cangjie
public prop isPersistent: Bool
```

功能：表示该请求是否为长连接，即请求 header 是否不包含 `Connection: close`。包含 `Connection: close` 为 false，否则为 true。

- 对于服务端，isPersistent 为 false 表示处理完该请求应该关闭连接。
- 对于客户端，isPersistent 为 false 表示如果收到响应后服务端未关闭连接，客户端应主动关闭连接。

类型：Bool

### prop form

```cangjie
public prop form: Form
```

功能：获取请求中的表单信息。

- 如果请求方法为 POST，PUT，PATCH，且 content-type 包含 application/x-www-form-urlencoded，获取请求 body 部分，用 form 格式解析；
- 如果请求方法不为 POST，PUT，PATCH，获取请求 url 中 query 部分。

> **注意：**
>
> - 如果用该接口读取了 body，body 已被消费完，后续将无法通过 body.read 读取 body；
> - 如果 form 不符合 [Form](../../../encoding/url/url_package_api/url_package_classes.md#class-form) 格式，抛 [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) 异常。

类型：[Form](../../../encoding/url/url_package_api/url_package_classes.md#class-form)

### prop headers

```cangjie
public prop headers: HttpHeaders
```

功能：获取 headers，headers 详述见 [HttpHeaders](http_package_classes.md#class-httpheaders) 类，获取后，可通过调用 [HttpHeaders](http_package_classes.md#class-httpheaders) 实例成员函数，修改该请求的 headers。

类型：[HttpHeaders](http_package_classes.md#class-httpheaders)

### prop method

```cangjie
public prop method: String
```

功能：获取 method，如 "GET", "POST"，request 实例的 method 无法修改。

类型：String

### prop readTimeout

```cangjie
public prop readTimeout: ?Duration
```

功能：表示该请求的请求级读超时时间。None 表示没有设置；Some(Duration) 表示设置了读超时时间。

类型：?Duration

### prop remoteAddr

```cangjie
public prop remoteAddr: String
```

功能：用于服务端，获取对端地址，即客户端地址，格式为 ip: port，用户无法设置，自定义的 request 对象调用该属性返回 ""，服务端 handler 中调用该属性返回客户端地址。

类型：String

### prop trailers

```cangjie
public prop trailers: HttpHeaders
```

功能：获取 trailers，trailers 详述见 [HttpHeaders](http_package_classes.md#class-httpheaders) 类，获取后，可通过调用 [HttpHeaders](http_package_classes.md#class-httpheaders) 实例成员函数，修改该请求的 trailers。

类型：[HttpHeaders](http_package_classes.md#class-httpheaders)

### prop url

```cangjie
public prop url: URL
```

功能：获取 url，表示客户端访问的 url。

类型：[URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url)

### prop version

```cangjie
public prop version: Protocol
```

功能：获取 http 版本，如 HTTP1_1 和 HTTP2_0，request 实例的 version 无法修改。

类型：[Protocol](http_package_enums.md#enum-protocol)

### prop writeTimeout

```cangjie
public prop writeTimeout: ?Duration
```

功能：表示该请求的请求级写超时时间，None 表示没有设置；Some(Duration) 表示设置了写超时时间。

类型：?Duration

### func toString()

```cangjie
public override func toString(): String
```

功能：把请求转换为字符串，包括 start line，headers，body size，trailers。
例如：`"GET /path HTTP/1.1\r\nhost: www.example.com\r\n\r\nbody size: 5\r\nbar: foo\r\n"`。

返回值：

- String - 请求的字符串表示。

## class HttpRequestBuilder

```cangjie
public class HttpRequestBuilder {
    public init()
    public init(request: HttpRequest)
}
```

功能：[HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 类用于构造 [HttpRequest](http_package_classes.md#class-httprequest) 实例。

### init()

```cangjie
public init()
```

功能：构造一个新 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder)。

### init(HttpRequest)

```cangjie
public init(request: HttpRequest)
```

功能： 通过 request 构造一个具有 request 属性的 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder)。由于 body 成员是一个 InputStream，对原始的 request 的 body 的操作会影响到复制得到的 [HttpRequest](http_package_classes.md#class-httprequest) 的 body。[HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 的 headers 和 trailers 是入参 request 的深拷贝。其余元素都是入参 request 的浅拷贝（因为是不可变对象，无需深拷贝）。

参数：

- request: [HttpRequest](http_package_classes.md#class-httprequest) - 传入的 [HttpRequest](http_package_classes.md#class-httprequest) 对象。

### func addHeaders(HttpHeaders)

```cangjie
public func addHeaders(headers: HttpHeaders): HttpRequestBuilder
```

功能：向请求 header 添加参数 [HttpHeaders](http_package_classes.md#class-httpheaders) 中的键值对。

参数：

- headers: [HttpHeaders](http_package_classes.md#class-httpheaders) - 传入的 header 对象。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func addTrailers(HttpHeaders)

```cangjie
public func addTrailers(trailers: HttpHeaders): HttpRequestBuilder
```

功能：向请求 trailer 添加参数 [HttpHeaders](http_package_classes.md#class-httpheaders) 中的键值对。

参数：

- trailers: [HttpHeaders](http_package_classes.md#class-httpheaders) - 传入的 trailer 对象。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func body(Array\<UInt8>)

```cangjie
public func body(body: Array<UInt8>): HttpRequestBuilder
```

功能：设置请求 body。如果已经设置过，调用该函数将替换原 body。

参数：

- body: Array\<UInt8> - 字节数组形式的请求体。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func body(InputStream)

```cangjie
public func body(body: InputStream): HttpRequestBuilder
```

功能：设置请求 body。如果已经设置过，调用该函数将替换原 body。

参数：

- body: InputStream - 流形式的请求体。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func body(String)

```cangjie
public func body(body: String): HttpRequestBuilder
```

功能：设置请求 body，如果已经设置过，调用该函数将替换原 body 调用该函数设置请求 body，则 body 将以内置的 InputStream 实现类表示，其大小已知。

参数：

- body: String - 字符串形式的请求体。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func build()

```cangjie
public func build(): HttpRequest
```

功能：根据 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例生成一个 [HttpRequest](http_package_classes.md#class-httprequest) 实例。

返回值：

- [HttpRequest](http_package_classes.md#class-httprequest) - 根据当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例构造出来的 [HttpRequest](http_package_classes.md#class-httprequest) 实例。

### func connect()

```cangjie
public func connect(): HttpRequestBuilder
```

功能：构造 method 为 "CONNECT" 的请求的便捷函数。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func delete()

```cangjie
public func delete(): HttpRequestBuilder
```

功能：构造 method 为 "DELETE" 的请求的便捷函数。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func get()

```cangjie
public func get(): HttpRequestBuilder
```

功能：构造 method 为 "GET" 的请求的便捷函数。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func head()

```cangjie
public func head(): HttpRequestBuilder
```

功能：构造 method 为 "HEAD" 的请求的便捷函数。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func header(String, String)

```cangjie
public func header(name: String, value: String): HttpRequestBuilder
```

功能：向请求 header 添加指定键值对，规则同 [HttpHeaders](http_package_classes.md#class-httpheaders) 类的 add 函数。

参数：

- name: String - 请求头的 key。
- value: String - 请求头的 value。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 如果传入的 name 或 value 包含不合法元素，将抛出此异常。

### func method(String)

```cangjie
public func method(method: String): HttpRequestBuilder
```

功能：设置请求 method，默认请求 method 为 "GET"。

参数：

- method: String - 请求方法，必须由 token 字符组成，如果传入空字符串，method 值将自动设置为 "GET"。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 参数 method 非法时抛出此异常。

### func options()

```cangjie
public func options(): HttpRequestBuilder
```

功能：构造 method 为 "OPTIONS" 的请求的便捷函数。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func post()

```cangjie
public func post(): HttpRequestBuilder
```

功能：构造 method 为 "POST" 的请求的便捷函数。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func priority(Int64, Bool)

```cangjie
public func priority(urg: Int64, inc: Bool): HttpRequestBuilder
```

功能：设置 priority 头的便捷函数，调用此函数后，将生成 priority 头，形如："priority: urgency=x, i"。如果通过设置请求头的函数设置了 priority 字段，调用此函数无效。如果多次调用此函数，以最后一次为准。

参数：

- urg: Int64 - 表示请求优先级，取值范围为 [0, 7]，0 表示最高优先级。
- inc: Bool - 表示请求是否需要增量处理，为 true 表示希望服务器并发处理与之同 urg 同 inc 的请求，为 false 表示不希望服务器并发处理。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

异常：

- [HttpException](./http_package_exceptions.md#class-httpexception) - 当参数 urg 取值非法，即不在 [0, 7] 范围内时，抛出异常。

### func put()

```cangjie
public func put(): HttpRequestBuilder
```

功能：构造 method 为 "PUT" 的请求的便捷函数。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func readTimeout(Duration)

```cangjie
public func readTimeout(timeout: Duration): HttpRequestBuilder
```

功能：设置此请求的读超时时间。如果传入的 Duration 为负，则会自动转为 0。如果用户设置了此读超时时间，那么该请求的读超时以此为准；如果用户没有设置，那么该请求的读超时以 [Client](http_package_classes.md#class-client) 为准。

参数：

- timeout: Duration - 用户设置的此请求的读超时时间。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func setHeaders(HttpHeaders)

```cangjie
public func setHeaders(headers: HttpHeaders): HttpRequestBuilder
```

功能：设置请求 header，如果已经设置过，调用该函数将替换原 header。

参数：

- headers: [HttpHeaders](http_package_classes.md#class-httpheaders) - 传入的 header 对象。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func setTrailers(HttpHeaders)

```cangjie
public func setTrailers(trailers: HttpHeaders): HttpRequestBuilder
```

功能：设置请求 trailer，如果已经设置过，调用该函数将替换原 trailer。

参数：

- trailers: [HttpHeaders](http_package_classes.md#class-httpheaders) - 传入的 trailer 对象。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func trace()

```cangjie
public func trace(): HttpRequestBuilder
```

功能：构造 method 为 "TRACE" 的请求的便捷函数。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func trailer(String, String)

```cangjie
public func trailer(name: String, value: String): HttpRequestBuilder
```

功能：向请求 trailer 添加指定键值对，规则同 [HttpHeaders](http_package_classes.md#class-httpheaders) 类的 add 函数。

参数：

- name: String - 请求头的 key。
- value: String - 请求头的 value。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 如果传入的 name 或 value 包含不合法元素，将抛出此异常。

### func url(String)

```cangjie
public func url(rawUrl: String): HttpRequestBuilder
```

功能：设置请求 url，默认 url 为空的 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 对象。

参数：

- rawUrl: String - 待解析成 url 对象的字符串，该字符串格式详见 [URL.parse](../../../encoding/url/url_package_api/url_package_classes.md#static-func-parsestring) 函数。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

异常：

- IllegalArgumentException - 当被编码的字符不符合 UTF8 的字节序列规则时，抛出异常。
- [UrlSyntaxException](../../../encoding/url/url_package_api/url_package_exceptions.md#class-urlsyntaxexception) - 当传入字符串不符合 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 格式时，抛出异常。

### func url(URL)

```cangjie
public func url(url: URL): HttpRequestBuilder
```

功能：设置请求 url，默认 url 为空的 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 对象，即 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url).parse("")。

参数：

- url: [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) - URL 对象。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func version(Protocol)

```cangjie
public func version(version: Protocol): HttpRequestBuilder
```

功能：设置请求的 http 协议版本，默认为 UnknownProtocol("")，客户端会根据 tls 配置自动选择协议。

参数：

- version: [Protocol](http_package_enums.md#enum-protocol) - 协议版本。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

### func writeTimeout(Duration)

```cangjie
public func writeTimeout(timeout: Duration): HttpRequestBuilder
```

功能：设置此请求的写超时时间。如果传入的 Duration 为负，则会自动转为 0。如果用户设置了此写超时时间，那么该请求的写超时以此为准；如果用户没有设置，那么该请求的写超时以 [Client](http_package_classes.md#class-client) 为准。

参数：

- timeout: Duration - 用户设置的此请求的写超时时间。

返回值：

- [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) - 当前 [HttpRequestBuilder](http_package_classes.md#class-httprequestbuilder) 实例的引用。

## class HttpResponse

```cangjie
public class HttpResponse <: ToString
```

功能：Http 响应类。

此类定义了 http 中响应 Response 的相关接口，客户端用该类读取服务端返回的响应。

父类型：

- ToString

### prop body

```cangjie
public prop body: InputStream
```

功能：获取 body。

> **注意：**
>
> - body 不支持并发读取；
> - 默认 InputStream 实现类的 read 函数不支持多次读取。

类型：InputStream

### prop bodySize

```cangjie
public prop bodySize: Option<Int64>
```

功能：获取响应 body 长度。

> - 如果未设置 body，则 bodySize 为 Some(0)；
> - 如果 body 长度已知，即通过 Array\<UInt8> 或 String 传入 body，或传入的 InputStream 有确定的 length (length >= 0)，则 bodySize 为 Some(Int64)；
> - 如果 body 长度未知，即通过用户自定义的 InputStream 实例传入 body 且 InputStream 实例没有确定的 length (length < 0)，则 bodySize 为 None。

类型：Option\<Int64>

### prop isPersistent

```cangjie
public prop isPersistent: Bool
```

功能：表示该响应是否为长连接，即响应 header 是否不包含 `Connection: close`。包含 `Connection: close` 为 false，否则为 true。

对于服务端，isPersistent 为 false 表示处理完该请求应关闭连接；

对于客户端，isPersistent 为 false 表示读完响应体后客户端应主动关闭连接。

类型：Bool

### prop headers

```cangjie
public prop headers: HttpHeaders
```

功能：获取 headers，headers 详述见 [HttpHeaders](http_package_classes.md#class-httpheaders) 类，获取后，可通过调用 [HttpHeaders](http_package_classes.md#class-httpheaders) 实例成员函数，修改该请求的 headers。

类型：[HttpHeaders](http_package_classes.md#class-httpheaders)

### prop request

```cangjie
public prop request: Option<HttpRequest>
```

功能：获取该响应对应的请求，默认为 None。

类型：Option\<[HttpRequest](http_package_classes.md#class-httprequest)>

### prop status

```cangjie
public prop status: UInt16
```

功能：获取响应的状态码，默认值为 200。状态码由 100~599 的三位数字组成，状态码所反映的具体信息可参考 [RFC 9110](https://httpwg.org/specs/rfc9110.html#status.codes)。

类型：UInt16

### prop trailers

```cangjie
public prop trailers: HttpHeaders
```

功能：获取 trailers，trailers 详述见 [HttpHeaders](http_package_classes.md#class-httpheaders) 类，获取后，可通过调用 [HttpHeaders](http_package_classes.md#class-httpheaders) 实例成员函数，修改该请求的 trailers。

类型：[HttpHeaders](http_package_classes.md#class-httpheaders)

### prop version

```cangjie
public prop version: Protocol
```

功能：获取响应的协议版本，默认值为 [HTTP1_1](./http_package_enums.md#enum-protocol)。

类型：[Protocol](http_package_enums.md#enum-protocol)

### func close()

```cangjie
public func close(): Unit
```

功能：如果用户不再需要未读完的 body 数据，可以调用此接口关闭连接以释放资源。如果是 HTTP/2 协议，会发送一个 Reset 帧关闭对应的流。

> **注意：**
>
> 如果使用者已读完 body，无需调用此接口再释放资源。

### func toString()

```cangjie
public override func toString(): String
```

功能：把响应转换为字符串，包括 status-line，headers，body size， trailers。

例如：HTTP/1.1 200 OK\r\ncontent-length: 5\r\n\r\nbody size: 5\r\nbar: foo\r\n。

返回值：

- String - 响应的字符串表示。

### extend HttpResponse

```cangjie
extend HttpResponse
```

功能：为 HttpResonse 扩展 HTTP/2.0 特有的方法。

#### func getPush()

```cangjie
public func getPush(): Option<ArrayList<HttpResponse>>
```

功能：获取服务器推送的响应，返回 None 代表未开启服务器推送功能，返回空 ArrayList 代表无服务器推送的响应。

返回值：

- Option\<ArrayList\<[HttpResponse](http_package_classes.md#class-httpresponse)>> - 服务器推送的响应列表。

## class HttpResponseBuilder

```cangjie
public class HttpResponseBuilder {
    public init()
}
```

功能：用于构造 [HttpResponse](http_package_classes.md#class-httpresponse) 实例。

### init()

```cangjie
public init()
```

功能：构造一个新 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder)。

### func addHeaders(HttpHeaders)

```cangjie
public func addHeaders(headers: HttpHeaders): HttpResponseBuilder
```

功能：向响应 header 添加参数 [HttpHeaders](http_package_classes.md#class-httpheaders) 中的键值对。

参数：

- headers: [HttpHeaders](http_package_classes.md#class-httpheaders) - 传入的 header 对象。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

### func addTrailers(HttpHeaders)

```cangjie
public func addTrailers(trailers: HttpHeaders): HttpResponseBuilder
```

功能：向响应 trailer 添加参数 [HttpHeaders](http_package_classes.md#class-httpheaders) 中的键值对。

参数：

- trailers: [HttpHeaders](http_package_classes.md#class-httpheaders) - 传入的 trailer 对象。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

### func body(Array\<UInt8>)

```cangjie
public func body(body: Array<UInt8>): HttpResponseBuilder
```

功能：设置响应 body，如果已经设置过，调用该函数将替换原 body。

参数：

- body: Array\<UInt8> - 字节数组形式的响应体。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

### func body(InputStream)

```cangjie
public func body(body: InputStream): HttpResponseBuilder
```

功能：设置响应 body，如果已经设置过，调用该函数将替换原 body 调用该函数设置请求 body。

参数：

- body: InputStream - 流形式的响应体。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

### func body(String)

```cangjie
public func body(body: String): HttpResponseBuilder
```

功能：设置响应 body，如果已经设置过，调用该函数将替换原 body 调用该函数设置请求 body。

参数：

- body: String - 字符串形式的响应体。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

### func build()

```cangjie
public func build(): HttpResponse
```

功能：根据 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例生成一个 [HttpResponse](http_package_classes.md#class-httpresponse) 实例。

返回值：

- [HttpResponse](http_package_classes.md#class-httpresponse) - 根据当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例构造出来的 [HttpResponse](http_package_classes.md#class-httpresponse) 实例。

### func header(String, String)

```cangjie
public func header(name: String, value: String): HttpResponseBuilder
```

功能：向响应 header 添加指定键值对，规则同 [HttpHeaders](http_package_classes.md#class-httpheaders) 类的 add 函数。

参数：

- name: String - 响应头的 key。
- value: String - 响应头的 value。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 如果传入的 name 或 value 包含不合法元素，将抛出此异常。

### func request(HttpRequest)

```cangjie
public func request(request: HttpRequest): HttpResponseBuilder
```

功能：设置响应对应的请求。

参数：

- request: [HttpRequest](http_package_classes.md#class-httprequest) - 响应对应的请求。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

### func setHeaders(HttpHeaders)

```cangjie
public func setHeaders(headers: HttpHeaders): HttpResponseBuilder
```

功能：设置响应 header，如果已经设置过，调用该函数将替换原 header。

参数：

- headers: [HttpHeaders](http_package_classes.md#class-httpheaders) - 传入的 header 对象。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

### func setTrailers(HttpHeaders)

```cangjie
public func setTrailers(trailers: HttpHeaders): HttpResponseBuilder
```

功能：设置响应 trailer，如果已经设置过，调用该函数将替换原 trailer。

参数：

- trailers: [HttpHeaders](http_package_classes.md#class-httpheaders) - 传入的 trailer 对象。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

### func status(UInt16)

```cangjie
public func status(status: UInt16): HttpResponseBuilder
```

功能：设置 http 响应状态码。

参数：

- status: UInt16 - 传入的状态码的值。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 如果设置响应状态码不在 100~599 这个区间内，则抛出此异常。

### func trailer(String, String)

```cangjie
public func trailer(name: String, value: String): HttpResponseBuilder
```

功能：向响应 trailer 添加指定键值对，规则同 [HttpHeaders](http_package_classes.md#class-httpheaders) 类的 add 函数。

参数：

- name: String - 响应头的 key。
- value: String - 响应头的 value。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 如果传入的 name 或 value 包含不合法元素，将抛出此异常。

### func version(Protocol)

```cangjie
public func version(version: Protocol): HttpResponseBuilder
```

功能：设置 http 响应协议版本。

参数：

- version: [Protocol](http_package_enums.md#enum-protocol) - 协议版本。

返回值：

- [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) - 当前 [HttpResponseBuilder](http_package_classes.md#class-httpresponsebuilder) 实例的引用。

## class HttpResponsePusher

```cangjie
public class HttpResponsePusher
```

功能：HTTP/2 服务器推送。

> **说明：**
>
> 如果服务器收到请求后，认为客户端后续还需要某些关联资源，可以将其提前推送到客户端；
> 服务端推送包括推送请求和推送响应；
> 启用服务端推送需要先调用 push 函数发送推送请求，并向服务器注册该请求对应的 handler，用以生成推送响应；
> 客户端可设置拒绝服务端推送；
> 不允许嵌套推送，即不允许在推送请求对应的 handler 中再次推送。嵌套推送情况下，服务端将不执行推送，并打印日志进行提示。

### static func getPusher(HttpContext)

```cangjie
public static func getPusher(ctx: HttpContext): ?HttpResponsePusher
```

功能：获取 [HttpResponsePusher](http_package_classes.md#class-httpresponsepusher) 实例，如果客户端拒绝推送，将返回 None。

参数：

- ctx: [HttpContext](#class-httpcontext) - Http 请求上下文。

返回值：

- ?[HttpResponsePusher](http_package_classes.md#class-httpresponsepusher) - 获得的 [HttpResponsePusher](http_package_classes.md#class-httpresponsepusher)。

### func push(String, String, HttpHeaders)

```cangjie
public func push(path: String, method: String, header: HttpHeaders): Unit
```

功能：向客户端发送推送请求，path 为请求地址，method 为请求方法，header 为请求头。

参数：

- path: String - 推送的请求地址。
- method: String - 推送的请求方法。
- header: [HttpHeaders](#class-httpheaders) - 推送的请求头。

## class HttpResponseWriter

```cangjie
public class HttpResponseWriter {
    public HttpResponseWriter(let ctx: HttpContext)
}
```

功能：HTTP response 消息体 Writer，支持用户控制消息体的发送过程。

> **说明：**
>
> 第一次调用 write 函数时，将立即发送 header 和通过参数传入的 body，此后每次调用 write，发送通过参数传入的 body。
> 对于 HTTP/1.1，如果设置了 transfer-encoding: chunked，用户每调用一次 write，将发送一个 chunk。
> 对于 HTTP/2，用户每调用一次 write，将把指定数据封装并发出。

### HttpResponseWriter(HttpContext)

```cangjie
public HttpResponseWriter(let ctx: HttpContext)
```

功能：构造一个 [HttpResponseWriter](http_package_classes.md#class-httpresponsewriter) 实例。

参数：

- ctx: [HttpContext](#class-httpcontext) - Http 请求上下文。

### func write(Array\<Byte>)

```cangjie
public func write(buf: Array<Byte>): Unit
```

功能：发送 buf 中数据到客户端。

参数：

- buf: Array\<Byte> - 要发送的数据。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 请求方法为 "HEAD" 或响应状态码为 "1XX\204\304"。
- [HttpException](http_package_exceptions.md#class-httpexception) - 连接关闭。
- [HttpException](http_package_exceptions.md#class-httpexception) - response 协议版本为 HTTP/1.0。
- [HttpException](http_package_exceptions.md#class-httpexception) - 响应连接已升级为 [WebSocket](http_package_classes.md#class-websocket)。

## class NotFoundHandler

```cangjie
public class NotFoundHandler <: HttpRequestHandler
```

功能：便捷的 Http 请求处理器，`404 Not Found` 处理器。

父类型：

- [HttpRequestHandler](http_package_interfaces.md#interface-httprequesthandler)

### func handle(HttpContext)

```cangjie
public func handle(ctx: HttpContext): Unit
```

功能：处理 Http 请求，回复 404 响应。

参数：

- ctx: [HttpContext](http_package_classes.md#class-httpcontext) - Http 请求上下文。

## class OptionsHandler

```cangjie
public class OptionsHandler <: HttpRequestHandler
```

功能：便捷的 Http 处理器，用于处理 OPTIONS 请求。固定返回 "Allow: OPTIONS，GET，HEAD，POST，PUT，DELETE" 响应头。

父类型：

- [HttpRequestHandler](http_package_interfaces.md#interface-httprequesthandler)

### func handle(HttpContext)

```cangjie
public func handle(ctx: HttpContext): Unit
```

功能：处理 Http OPTIONS 请求。

参数：

- ctx: [HttpContext](http_package_classes.md#class-httpcontext) - Http 请求上下文。

## class ProtocolService

```cangjie
public abstract class ProtocolService
```

功能：Http 协议服务实例，为单个客户端连接提供 Http 服务，包括对客户端 request 报文的解析、 request 的分发处理、 response 的发送等。

## class RedirectHandler

```cangjie
public class RedirectHandler <: HttpRequestHandler {
    public init(url: String, code: UInt16)
}
```

功能：便捷的 Http 处理器，用于回复重定向响应。

父类型：

- [HttpRequestHandler](http_package_interfaces.md#interface-httprequesthandler)

### init(String, UInt16)

```cangjie
public init(url: String, code: UInt16)
```

功能：[RedirectHandler](http_package_classes.md#class-redirecthandler) 的构造函数。

参数：

- url: String - 重定向响应中 Location 头部的 url。
- code: UInt16 - 重定向响应的响应码。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - url 为空或响应码不是除 304 以外的 3XX 状态码时抛出异常。

### func handle(HttpContext)

```cangjie
public func handle(ctx: HttpContext): Unit
```

功能：处理 Http 请求，回复重定向响应。

参数：

- ctx: [HttpContext](http_package_classes.md#class-httpcontext) - Http 请求上下文。

## class Server

```cangjie
public class Server
```

功能：提供 HTTP 服务的 [Server](http_package_classes.md#class-server) 类。

> **说明：**
>
> - 启动服务，在指定地址及端口等待用户连接、服务用户的 http request；
> - 关闭服务，包括关闭所有已有连接；
> - 提供注册处理 http request 的 handler 的机制，根据注册信息分发 request 到相应的 handler；
> - 提供 tls 证书热机制；
> - 提供 shutdown 回调机制；
> - 通过 [Logger](../../../log/log_package_api/log_package_classes.md#class-logger).level 开启、关闭日志打印，包括按照用户要求打印相应级别的日志；
> - [Server](http_package_classes.md#class-server) 文档中未明确说明支持版本的配置，在 HTTP/1.1 与 HTTP/2 都会生效。

### prop addr

```cangjie
public prop addr: String
```

功能：获取服务端监听地址。

类型：String

### prop distributor

```cangjie
public prop distributor: HttpRequestDistributor
```

功能：获取请求分发器，请求分发器会根据 url 将请求分发给对应的 handler。

类型：[HttpRequestDistributor](http_package_interfaces.md#interface-httprequestdistributor)

### prop enableConnectProtocol

```cangjie
public prop enableConnectProtocol: Bool
```

功能：HTTP/2 专用，用来限制对端发送的报文是否支持通过 connect 方法升级协议，true 表示支持。

类型：Bool

### prop headerTableSize

```cangjie
public prop headerTableSize: UInt32
```

功能：获取服务端 HTTP/2 Hpack 动态表的初始值，默认值为 4096。

类型：UInt32

### prop httpKeepAliveTimeout

```cangjie
public prop httpKeepAliveTimeout: Duration
```

功能：HTTP/1.1 专用，获取服务器设定的保持长连接的超时时间。

类型：Duration

### prop initialWindowSize

```cangjie
public prop initialWindowSize: UInt32
```

功能：HTTP/2 专用，用来限制对端发送的报文 stream 初始流量窗口大小。默认值为 65535 ，取值范围为 0 至 2^31 - 1。

类型：UInt32

### prop listener

```cangjie
public prop listener: ServerSocket
```

功能：获取服务器绑定 socket。

类型：ServerSocket

### prop logger

```cangjie
public prop logger: Logger
```

功能：获取服务器日志记录器，设置 logger.level 将立即生效，记录器应该是线程安全的。

类型：[Logger](../../../log/log_package_api/log_package_classes.md#class-logger)

### prop maxConcurrentStreams

```cangjie
public prop maxConcurrentStreams: UInt32
```

功能：HTTP/2 专用，用来限制连接同时处理的最大请求数量。

类型：UInt32

### prop maxFrameSize

```cangjie
public prop maxFrameSize: UInt32
```

功能：HTTP/2 专用，用来限制对端发送的报文一个帧的最大长度。默认值为 16384. 取值范围为 2^14 至 2^24 - 1。

类型：UInt32

### prop maxHeaderListSize

```cangjie
public prop maxHeaderListSize: UInt32
```

功能：获取客户端支持的 HTTP/2 最大头部（Header）大小。这个大小指的是响应头部中所有头部字段（Header Field）的最大允许长度之和，其中包括所有字段名称（name）的长度、字段值（value）的长度以及每个字段自动添加的伪头开销（通常每个字段会有 32 字节的开销，这包括了 HTTP/2 协议本身为头部字段添加的伪头部信息）。默认情况下，这个最大长度被设置为 UInt32.Max。

类型：UInt32

### prop maxRequestBodySize

```cangjie
public prop maxRequestBodySize: Int64
```

功能：获取服务器设定的读取请求的请求体最大值，仅对于 HTTP/1.1 且未设置 "Transfer-Encoding: chunked" 的请求生效。

类型：Int64

### prop maxRequestHeaderSize

```cangjie
public prop maxRequestHeaderSize: Int64
```

功能：获取服务器设定的读取请求的请求头最大值。仅对 HTTP/1.1 生效，HTTP/2 中有专门的配置 maxHeaderListSize。

类型：Int64

### prop port

```cangjie
public prop port: UInt16
```

功能：获取服务端监听端口。

类型：UInt16

### prop protocolServiceFactory

```cangjie
public prop protocolServiceFactory: ProtocolServiceFactory
```

功能：获取协议服务工厂，服务协议工厂会生成每个协议所需的服务实例。

类型：[ProtocolServiceFactory](http_package_interfaces.md#interface-protocolservicefactory)

### prop readHeaderTimeout

```cangjie
public prop readHeaderTimeout: Duration
```

功能：获取服务器设定的读取请求头的超时时间。

类型：Duration

### prop readTimeout

```cangjie
public prop readTimeout: Duration
```

功能：获取服务器设定的读取整个请求的超时时间。

类型：Duration

### prop servicePoolConfig

```cangjie
public prop servicePoolConfig: ServicePoolConfig
```

功能：获取协程池配置实例。

类型：[ServicePoolConfig](http_package_structs.md#struct-servicepoolconfig)

### prop transportConfig

```cangjie
public prop transportConfig: TransportConfig
```

功能：获取服务器设定的传输层配置。

类型：[TransportConfig](http_package_structs.md#struct-transportconfig)

### prop writeTimeout

```cangjie
public prop writeTimeout: Duration
```

功能：获取服务器设定的写响应的超时时间。

类型：Duration

### func afterBind(() -> Unit)

```cangjie
public func afterBind(f: ()-> Unit): Unit
```

功能：注册服务器启动时的回调函数，服务内部 ServerSocket 实例 bind 之后，accept 之前将调用该函数。重复调用将覆盖之前注册的函数。

参数：

- f: () -> Unit - 回调函数，入参为空，返回值为 Unit 类型。

### func close()

```cangjie
public func close(): Unit
```

功能：关闭服务器，服务器关闭后将不再对请求进行读取与处理，重复关闭将只有第一次生效（包括 close 和 closeGracefully）。

### func closeGracefully()

```cangjie
public func closeGracefully(): Unit
```

功能：关闭服务器，服务器关闭后将不再对请求进行读取，当前正在进行处理的服务器待处理结束后进行关闭。

### func getTlsConfig()

```cangjie
public func getTlsConfig(): ?TlsServerConfig
```

功能：获取服务器设定的 TLS 层配置。

返回值：

- ?[TlsServerConfig](../../tls/tls_package_api/tls_package_structs.md#struct-tlsserverconfig) - 服务端设定的 TLS 层配置，如果没有设置则返回 None。

### func onShutdown(() -> Unit)

```cangjie
public func onShutdown(f: () -> Unit): Unit
```

功能：注册服务器关闭时的回调函数，服务器关闭时将调用该回调函数，重复调用将覆盖之前注册的函数。

参数：

- f: () -> Unit - 回调函数，入参为空，返回值为 Unit 类型。

### func serve()

```cangjie
public func serve(): Unit
```

功能：启动服务端进程，不支持重复启动。

h1 request 检查和处理：

- request-line 不符合 RFC 9112 中 request-line = method SP request-target SP HTTP-version 的规则，将会返回 400 响应；
- method 由 tokens 组成，且大小写敏感；request-target 为能够被解析的 url；HTTP-version 为 HTTP/1.0 或 HTTP/1.1 ，否则将会返回 400 响应；
- headers name 和 value 需符合特定规则，详见 [HttpHeaders](http_package_classes.md#class-httpheaders) 类说明，否则返回 400 响应；
- 当 headers 的大小超出 server 设定的 maxRequestHeaderSize 时将自动返回 431 响应；
- headers 中必须包含 "host" 请求头，且值唯一，否则返回 400 响应 headers 中不允许同时存在 "content-length" 与 "transfer-encoding" 请求头，否则返回 400 响应；
- 请求头 "transfer-encoding" 的 value 经过 "," 分割后最后一个 value 必须为 "chunked"，且之前的 value 不允许存在 "chunked"，否则返回 400 响应；
- 请求头 "content-length" 其 value 必须能解析为 Int64 类型，且不能为负值，否则返回 400 响应，当其 value 值超出 server 设定 maxRequestBodySize，将返回 413 响应；
- headers 中若不存在 "content-length" 和 "transfer-encoding: chunked" 时默认不存在 body；
- 请求头 "trailer" 中，value 不允许存在 "transfer-encoding"，"trailer"，"content-length"；
- 请求头 "expect" 中，value 中存在非 "100-continue" 的值，将会返回 417 响应；
- HTTP/1.0 默认短连接，若想保持长连接需要包含请求头 "connection: keep-alive" 与 "keep-alive: timeout = XX, max = XX"，将会自动保持 timeout 时长的连接。HTTP/1.1 默认长连接，当解析 request 失败则关闭连接；
- 仅允许在 chunked 模式下存在 trailer，且 trailer 中条目的 name 必须被包含在 "trailer" 请求头中，否则将自动删除。

h1 response 检查和处理：

- 若用户不对 response 进行配置，将会自动返回 200 响应；
- 若接收到的 request 包含请求头 "connection: close" 而配置 response 未添加响应头 "connection" 或响应头 "connection" 的 value 不包含 "close"，将自动添加 "connection: close"，若接收到的 request 不包含请求头 "connection: close" 且响应头不存在 "connection: keep-alive"，将会自动添加；
- 如果 headers 包含逐跳响应头："proxy-connection"，"keep-alive"，"te"，"transfer-encoding"，"upgrade"，将会在响应头 "connection" 自动添加这些头作为 value；
- 将自动添加 "date" 响应头，用户提供的 "date" 将被忽略；
- 若请求方法为 "HEAD" 或响应状态码为 "1XX\204\304"，body 将配置为空；
- 若已知提供 body 的长度时，将会与响应头 "content-length" 进行比较，若不存在响应头 "content-length"，将自动添加此响应头，其 value 值为 body 长度。若响应头 "content-length" 长度大于 body 长度，将会在 handler 中抛出 [HttpException](http_package_exceptions.md#class-httpexception)，若小于 body 长度，将对 body 进行截断处理，发送的 body 长度将为 "content-length" 的值；
- response 中 "set-cookie" header 将分条发送，其他 headers 同名条目将合成一条发送；
- 在处理包含请求头："expect: 100-continue" 的 request 时，在调用 request 的 body.read() 时将会自动发送状态码为 100 的响应给客户端。不允许用户主动发送状态码为 100 的 response，若进行发送则被认定为服务器异常。

启用 h2 服务：tlsConfig 中 supportedAlpnProtocols 需包含 "h2"，此后如果 tls 层 alpn 协商结果为 h2，则启用 h2 服务。

h2 request 检查和处理：

- headers name 和 value 需符合特定规则，详见 [HttpHeaders](http_package_classes.md#class-httpheaders) 类说明，此外 name 不能包含大写字符，否则发送 RST 帧关闭流，即无法保证返回响应；
- trailers name 和 value 需符合同样规则，否则关闭流；
- headers 不能包含 "connection"，"transfer-encoding"，"keep-alive"，"upgrade"，"proxy-connection"，否则关闭流；
- 如果有 "te" header，其值只能为 "trailers"，否则关闭流；
- 如果有 "host" header 和 ":authority" pseudo header，"host" 值必须与 ":authority" 一致，否则关闭流；
- 如果有 "content-length" header，需符合 "content-length" 每个值都能解析为 Int64 类型，且如果有多个值，必须相等，否则关闭流；
- 如果有 "content-length" header，且有 body 大小，则 content-length 值与 body 大小必须相等，否则关闭流；
- 如果有 "trailer" header，其值不能包含 "transfer-encoding"，"trailer"，"content-length"，否则关闭流；
- 仅在升级 [WebSocket](http_package_classes.md#class-websocket) 场景下支持 CONNECT 方法，否则关闭流；
- pseudo headers 中，必须包含 ":method"、":scheme"、":path"，其中 ":method" 值必须由 tokens 字符组成，":scheme" 值必须为 "https"，":path" 不能为空，否则关闭流；
- trailer 中条目的 name 必须被包含在 "trailer" 头中，否则将自动删除；
- request headers 大小不能超过 maxHeaderListSize，否则关闭连接。

h2 response 检查和处理：

- 如果 HEAD 请求的响应包含 body，将自动删除；
- 将自动添加 "date" field，用户提供的 "date" 将被忽略；
- 如果 headers 包含 "connection"，"transfer-encoding"，"keep-alive"，"upgrade"，"proxy-connection"，将自动删除；
- response 中 "set-cookie" header 将分条发送，其他 headers 同名条目将合成一条发送；
- 如果 headers 包含 "content-length"，且 method 不为 "HEAD"，"content-length" 将被删除；
- 如果 method 为 "HEAD"，则：
    - headers 包含 "content-length"，但 "content-length" 不合法（无法被解析为 Int64 值，或包含多个不同值），如果用户调用 [HttpResponseWriter](http_package_classes.md#class-httpresponsewriter) 类的 write 函数，将抛出 [HttpException](http_package_exceptions.md#class-httpexception)，如果用户 handler 已经结束，将打印日志；
    - headers 包含 "content-length"，同时 response.body.length 不为 -1，"content-length" 值与 body.length 不符，同 6.1 处理；
    - headers 包含 "content-length"，同时 response.body.length 为 -1，或 body.length 与 "content-length" 值一致，则保留 "content-length" header；
- trailer 中条目必须被包含在 "trailer" 头中，否则将自动删除；
- 如果 handler 中抛出异常，且用户未调用 write 发送部分响应，将返回 500 响应。如果用户已经调用 write 发送部分响应，将发送 RST 帧关闭 stream。

h2 server 发完 response 之后，如果 stream 状态不是 CLOSED，会发送带 NO_ERROR 错误码的 RST 帧关闭 stream，避免已经处理完毕的 stream 继续占用服务器资源。

h2 流量控制：

- connection 流量窗口初始值为 65535，每次收到 DATA 帧将返回一个 connection 层面的 WINDOW-UPDATE，发送 DATA 时，如果 connection 流量窗口值为负数，将阻塞至其变为正数；
- stream 流量窗口初始值可由用户设置，默认值为 65535，每次收到 DATA 帧将返回一个 stream 层面的 WINDOW-UPDATE，发送 DATA 时，如果 stream 流量窗口值为负数，将阻塞至其变为正数。

h2 请求优先级：

- 支持按 urgency 处理请求，h2 服务默认并发处理请求，当并发资源不足时，请求将按 urgency 处理，优先级高的请求优先处理。

默认 [ProtocolServiceFactory](http_package_interfaces.md#interface-protocolservicefactory) 协议选择：

- 如果连接是 tcp，使用 HTTP/1.1 server；
- 如果连接是 tls，根据 alpn 协商结果确定 http 协议版本，如果协商结果为 "http/1.0"，"http/1.1" 或 ""，使用 HTTP/1.1 server，如果协商结果为 "h2"，使用 HTTP/2 server，否则不处理此次请求，打印日志关连接。

异常：

- SocketException - 当端口监听失败时，抛出异常。

### func updateCA(Array\<X509Certificate>)

```cangjie
public func updateCA(newCa: Array<X509Certificate>): Unit
```

功能：对 CA 证书进行热更新。

参数：

- newCa: Array\<[X509Certificate](../../../crypto/x509/x509_package_api/x509_package_classes.md#class-x509certificate)> - CA 证书。

异常：

- IllegalArgumentException - 参数包含空字符时抛出异常。
- [HttpException](http_package_exceptions.md#class-httpexception) - 服务端未配置 tlsConfig 时抛出异常。

### func updateCA(String)

```cangjie
public func updateCA(newCaFile: String): Unit
```

功能：对 CA 证书进行热更新。

参数：

- newCaFile: String - CA 证书文件。

异常：

- IllegalArgumentException - 参数包含空字符时抛出异常。
- [HttpException](http_package_exceptions.md#class-httpexception) - 服务端未配置 tlsConfig 时抛出异常。

### func updateCert(Array\<X509Certificate>, PrivateKey)

```cangjie
public func updateCert(certChain: Array<X509Certificate>, certKey: PrivateKey): Unit
```

功能：对 TLS 证书进行热更新。

参数：

- certChain: Array\<[X509Certificate](../../../crypto/x509/x509_package_api/x509_package_classes.md#class-x509certificate)> - 证书链。
- certKey: [PrivateKey](../../../crypto/x509/x509_package_api/x509_package_interfaces.md#interface-privatekey) - 证书匹配的私钥。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 服务端未配置 tlsConfig 时抛出异常。

### func updateCert(String, String)

```cangjie
public func updateCert(certificateChainFile: String, privateKeyFile: String): Unit
```

功能：对 TLS 证书进行热更新。

参数：

- certificateChainFile: String - 证书链文件。
- privateKeyFile: String - 证书匹配的私钥文件。

异常：

- IllegalArgumentException - 参数包含空字符时抛出异常。
- [HttpException](http_package_exceptions.md#class-httpexception) - 服务端未配置 tlsConfig 时抛出异常。

## class ServerBuilder

```cangjie
public class ServerBuilder {
    public init()
}
```

功能：提供 [Server](http_package_classes.md#class-server) 实例构建器。

支持通过如下参数构造一个 Http [Server](http_package_classes.md#class-server)：

- 地址、端口；
- 线程安全的 logger；
- [HttpRequestDistributor](http_package_interfaces.md#interface-httprequestdistributor)，用于注册 handler、分发 request；
- HTTP/2 的 settings；
- shutdown 回调；
- transport：listener、连接及其配置；
- protocol service：http 协议解析服务；

除地址端口、shutdown 回调外，均提供默认实现，用户在构造 server 过程中可不指定其他构建参数。
[ServerBuilder](http_package_classes.md#class-serverbuilder) 文档中未明确说明支持版本的配置，在 HTTP/1.1 与 HTTP/2 都会生效。

> **说明：**
>
> 该类提供了一系列配置参数的函数，配置完成后调用 [build](./http_package_classes.md#func-build-3) 函数构造出 [Server](./http_package_classes.md#class-server) 实例。配置函数中说明了参数的取值范围，但配置函数本身不做参数合法性校验，[build](./http_package_classes.md#func-build-3) 时统一进行校验。

### init()

```cangjie
public init()
```

功能：创建 [ServerBuilder](http_package_classes.md#class-serverbuilder) 实例。

### func addr(String)

```cangjie
public func addr(addr: String): ServerBuilder
```

功能：设置服务端监听地址，若 listener 被设定，此值被忽略。

格式需符合 IPAddress 中相关规定。

参数：

- addr: String - 地址值。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func afterBind(()->Unit)

```cangjie
public func afterBind(f: ()->Unit): ServerBuilder
```

功能：注册服务器启动时的回调函数，服务内部 ServerSocket 实例 bind 之后，accept 之前将调用该函数。重复调用将覆盖之前注册的函数。

参数：

- f: () ->Unit - 回调函数，入参为空，返回值为 Unit 类型。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func build()

```cangjie
public func build(): Server
```

功能：根据设置的参数构建 [Server](http_package_classes.md#class-server) 实例。

此处会对各参数的值进行检查，如果取值非法，将抛出异常。各参数的取值范围详见设置参数相关的函数。

返回值：

- [Server](http_package_classes.md#class-server) - 生成的 [Server](http_package_classes.md#class-server) 实例。

异常：

- IllegalArgumentException - 当设置的参数非法时，抛出异常。
- IllegalFormatException 格式错误时，抛出异常。

### func distributor(HttpRequestDistributor)

```cangjie
public func distributor(distributor: HttpRequestDistributor): ServerBuilder
```

功能：设置请求分发器，请求分发器会根据 url 将请求分发给对应的 handler。不设置时使用默认请求分发器。

参数：

- distributor: [HttpRequestDistributor](http_package_interfaces.md#interface-httprequestdistributor) - 自定义请求分发器实例。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func enableConnectProtocol(Bool)

```cangjie
public func enableConnectProtocol(flag: Bool): ServerBuilder
```

功能：HTTP/2 专用，设置本端是否接收 CONNECT 请求，默认 false。

参数：

- flag: Bool - 本端是否接收 CONNECT 请求。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func headerTableSize(UInt32)

```cangjie
public func headerTableSize(size: UInt32): ServerBuilder
```

功能：设置服务端 HTTP/2 Hpack 动态表的初始值，默认值为 4096。

参数：

- size: UInt32 - 本端对响应头编码时使用的最大 `table size`

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func httpKeepAliveTimeout(Duration)

```cangjie
public func httpKeepAliveTimeout(timeout: Duration): ServerBuilder
```

功能：HTTP/1.1 专用，设定服务端连接保活时长，该时长内客户端未再次发送请求，服务端将关闭长连接，默认不进行限制。

参数：

- timeout: Duration - 设定保持长连接的超时时间，如果传入负的 Duration 将被替换为 Duration.Zero。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func initialWindowSize(UInt32)

```cangjie
public func initialWindowSize(size: UInt32): ServerBuilder
```

功能：HTTP/2 专用，设置当前服务器上每个流的接收报文的初始流量窗口大小，默认值为 65535。取值范围为 0 至 2^31 - 1。

参数：

- size: UInt32 - 本端一个 stream 上接收报文的初始流量窗口大小。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func listener(ServerSocket)

```cangjie
public func listener(listener: ServerSocket): ServerBuilder
```

功能：服务端调用此函数对指定 socket 进行绑定监听。

参数：

- listener: ServerSocket - 所绑定的 socket。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func logger(Logger)

```cangjie
public func logger(logger: Logger): ServerBuilder
```

功能：设定服务器的 logger，默认 logger 级别为 INFO，logger 内容将写入 Console.stdout。

参数：

- logger: [Logger](../../../log/log_package_api/log_package_classes.md#class-logger) - 需要是线程安全的，默认使用内置线程安全 logger。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func maxConcurrentStreams(UInt32)

```cangjie
public func maxConcurrentStreams(size: UInt32): ServerBuilder
```

功能：HTTP/2 专用，设置本端同时处理的最大请求数量，限制对端并发发送请求的数量，默认值为 100。

参数：

- size: UInt32 - 本端同时处理的最大请求数量。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func maxFrameSize(UInt32)

```cangjie
public func maxFrameSize(size: UInt32): ServerBuilder
```

功能：HTTP/2 专用，设置本端接收的一个帧的最大长度，用来限制对端发送帧的长度，默认值为 16384. 取值范围为 2^14 至 2^24 - 1。

参数：

- size: UInt32 - 本端接收的一个帧的最大长度。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func maxHeaderListSize(UInt32)

```cangjie
public func maxHeaderListSize(size: UInt32): ServerBuilder
```

功能：获取客户端支持的 HTTP/2 最大头部（Header）大小。这个大小指的是响应头部中所有头部字段（Header Field）的最大允许长度之和，其中包括所有字段名称（name）的长度、字段值（value）的长度以及每个字段自动添加的伪头开销（通常每个字段会有 32 字节的开销，这包括了 HTTP/2 协议本身为头部字段添加的伪头部信息）。默认情况下，这个最大长度被设置为 UInt32.Max。

参数：

- size: UInt32 - 本端接收的报文头最大长度。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func maxRequestBodySize(Int64)

```cangjie
public func maxRequestBodySize(size: Int64): ServerBuilder
```

功能：设置服务端允许客户端发送单个请求的请求体最大长度，请求体长度超过该值时，将返回状态码为 413 的响应。默认值为 2M。仅对于 HTTP/1.1 且未设置 "Transfer-Encoding: chunked" 的请求生效。

参数：

- size: Int64 - 设定允许接收请求的请求体大小最大值，值为 0 代表不作限制。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

异常：

- IllegalArgumentException - 当入参 size < 0 时，抛出异常。

### func maxRequestHeaderSize(Int64)

```cangjie
public func maxRequestHeaderSize(size: Int64): ServerBuilder
```

功能：设定服务端允许客户端发送单个请求的请求头最大长度，请求头长度超过该值时，将返回状态码为 431 的响应；仅对 HTTP/1.1 生效，HTTP/2 中有专门的配置 maxHeaderListSize。

参数：

- size: Int64 - 设定允许接收请求的请求头大小最大值，值为 0 代表不作限制。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

异常：

- IllegalArgumentException - 当入参 size < 0 时，抛出异常。

### func onShutdown(() -> Unit)

```cangjie
public func onShutdown(f: () -> Unit): ServerBuilder
```

功能：注册服务器关闭时的回调函数，服务器关闭时将调用该回调函数，重复调用将覆盖之前注册的函数。

参数：

- f: () ->Unit - 回调函数，入参为空，返回值为 Unit 类型。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func port(UInt16)

```cangjie
public func port(port: UInt16): ServerBuilder
```

功能：设置服务端监听端口，若 listener 被设定，此值被忽略。

参数：

- port: UInt16 - 端口值。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func protocolServiceFactory(ProtocolServiceFactory)

```cangjie
public func protocolServiceFactory(factory: ProtocolServiceFactory): ServerBuilder
```

功能：设置协议服务工厂，服务协议工厂会生成每个协议所需的服务实例，不设置时使用默认工厂。

参数：

- factory: [ProtocolServiceFactory](http_package_interfaces.md#interface-protocolservicefactory) - 自定义工厂实例。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func readHeaderTimeout(Duration)

```cangjie
public func readHeaderTimeout(timeout: Duration): ServerBuilder
```

功能：设定服务端读取客户端发送一个请求的请求头最大时长，超过该时长将不再进行读取并关闭连接，默认不进行限制。

参数：

- timeout: Duration - 设定的读请求头超时时间，如果传入负的 Duration 将被替换为 Duration.Zero。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func readTimeout(Duration)

```cangjie
public func readTimeout(timeout: Duration): ServerBuilder
```

功能：设定服务端读取一个请求的最大时长，超过该时长将不再进行读取并关闭连接，默认不进行限制。

参数：

- timeout: Duration - 设定读请求的超时时间，如果传入时间为负值将被替换为 Duration.Zero。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func servicePoolConfig(ServicePoolConfig)

```cangjie
public func servicePoolConfig(cfg: ServicePoolConfig): ServerBuilder
```

功能：服务过程中使用的协程池相关设置，具体说明见 [ServicePoolConfig](http_package_structs.md#struct-servicepoolconfig) 结构体。

参数：

- cfg: [ServicePoolConfig](http_package_structs.md#struct-servicepoolconfig) - 协程池相关设置。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func tlsConfig(TlsServerConfig)

```cangjie
public func tlsConfig(config: TlsServerConfig): ServerBuilder
```

功能：设置 TLS 层配置，默认不对其进行设置。

参数：

- config: [TlsServerConfig](../../tls/tls_package_api/tls_package_structs.md#struct-tlsserverconfig) - 设定支持 tls 服务所需要的配置信息。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func transportConfig(TransportConfig)

```cangjie
public func transportConfig(config: TransportConfig): ServerBuilder
```

功能：设置传输层配置，默认配置详见 [TransportConfig](http_package_structs.md#struct-transportconfig) 结构体说明。

参数：

- config: [TransportConfig](http_package_structs.md#struct-transportconfig) - 设定的传输层配置信息。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

### func writeTimeout(Duration)

```cangjie
public func writeTimeout(timeout: Duration): ServerBuilder
```

功能：设定服务端发送一个响应的最大时长，超过该时长将不再进行写入并关闭连接，默认不进行限制。

参数：

- timeout: Duration - 设定写响应的超时时间，如果传入时间为负值将被替换为 Duration.Zero。

返回值：

- [ServerBuilder](http_package_classes.md#class-serverbuilder) - 当前 [ServerBuilder](http_package_classes.md#class-serverbuilder) 的引用。

## class WebSocket

```cangjie
public class WebSocket
```

功能：提供 [WebSocket](http_package_classes.md#class-websocket) 服务的相关类，提供 [WebSocket](http_package_classes.md#class-websocket) 连接的读、写、关闭等函数。用户通过 upgradeFrom 函数以获取 [WebSocket](http_package_classes.md#class-websocket) 连接。

- 调用 `read()` 读取一个 [WebSocketFrame](http_package_classes.md#class-websocketframe)，用户可通过 [WebSocketFrame](http_package_classes.md#class-websocketframe).frameType 来知晓帧的类型，通过 [WebSocketFrame](http_package_classes.md#class-websocketframe).fin 来知晓是否是分段帧。
- 调用 `write(frameType: WebSocketFrameType, byteArray: Array<UInt8>)`，传入 message 的类型和 message 的 byte 来发送 [WebSocket](http_package_classes.md#class-websocket) 信息，如果写的是控制帧，则不会分段发送，如果写的是数据帧（Text、Binary），则会将 message 按底层 buffer 的大小分段（分成多个 fragment）发送。

详细说明见下文接口说明，接口行为以 RFC 6455 为准。

### prop logger

```cangjie
public prop logger: Logger
```

功能：日志记录器。

类型：[Logger](../../../log/log_package_api/log_package_classes.md#class-logger)

### prop subProtocol

```cangjie
public prop subProtocol: String
```

功能：获取与对端协商到的 subProtocol，协商时，客户端提供一个按偏好排名的 subProtocols 列表，服务器从中选取一个或零个子协议。

类型：String

### static func upgradeFromClient(Client, URL, Protocol, ArrayList\<String>, HttpHeaders)

```cangjie
public static func upgradeFromClient(client: Client, url: URL,
 version!: Protocol = HTTP1_1,
 subProtocols!: ArrayList<String> = ArrayList<String>(),
 headers!: HttpHeaders = HttpHeaders()): (WebSocket, HttpHeaders)
```

功能：提供客户端升级到 [WebSocket](http_package_classes.md#class-websocket) 协议的函数。

> **说明：**
>
> 客户端的升级流程为：传入 client 对象，url 对象，构建升级请求，请求服务器后验证其响应，如果握手成功，则返回 [WebSocket](http_package_classes.md#class-websocket) 对象用于 [WebSocket](http_package_classes.md#class-websocket) 通讯，并返回 101 响应头的 [HttpHeaders](http_package_classes.md#class-httpheaders) 对象给用户。暂不支持 extensions。如果子协议协商成功，用户可通过调用返回的 [WebSocket](http_package_classes.md#class-websocket) 的 subProtocol 查看子协议。

参数：

- client: [Client](http_package_classes.md#class-client) - 用于请求的 client 对象。
- url: [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) - 用于请求的 url 对象，[WebSocket](http_package_classes.md#class-websocket) 升级时要注意 url 的 scheme 为 ws 或 wss。
- version!: [Protocol](http_package_enums.md#enum-protocol) - 创建 socket 使用的 HTTP 版本，只支持  [HTTP1_1](./http_package_enums.md#enum-protocol) 和  [HTTP2_0](./http_package_enums.md#enum-protocol) 向 [WebSocket](http_package_classes.md#class-websocket) 升级。
- subProtocols!: ArrayList\<String> - 用户配置的子协议列表，按偏好排名，默认为空。若用户配置了，则会随着升级请求发送给服务器。
- headers!: [HttpHeaders](http_package_classes.md#class-httpheaders) - 需要随着升级请求一同发送的非升级必要头，如 cookie 等。

返回值：

- ([WebSocket](http_package_classes.md#class-websocket), HttpHeaders) - 升级成功，则返回 [WebSocket](http_package_classes.md#class-websocket) 对象用于通讯和 101 响应的头。

异常：

- SocketException - 底层连接错误时抛出异常。
- [HttpException](http_package_exceptions.md#class-httpexception) - 握手时 HTTP 请求过程中出现错误时抛出异常。
- [WebSocketException](http_package_exceptions.md#class-websocketexception) - 升级失败，升级响应验证不通过时抛出异常。

### static func upgradeFromServer(HttpContext, ArrayList\<String>, ArrayList\<String>, (HttpRequest) -> HttpHeaders)

```cangjie
public static func upgradeFromServer(ctx: HttpContext, subProtocols!: ArrayList<String> = ArrayList<String>(),
                                        origins!: ArrayList<String> = ArrayList<String>(),
                                        userFunc!:(HttpRequest) -> HttpHeaders = {_: HttpRequest => HttpHeaders()}): WebSocket
```

功能：提供服务端升级到 [WebSocket](http_package_classes.md#class-websocket) 协议的函数，通常在 handler 中使用。

服务端升级的流程为：收到客户端发来的升级请求，验证请求，如果验证通过，则回复 101 响应并返回 [WebSocket](http_package_classes.md#class-websocket) 对象用于 [WebSocket](http_package_classes.md#class-websocket) 通讯。

- 用户通过 subProtocols，origins 参数来配置其支持的 subprotocol 和 origin 白名单，subProtocols 如果不设置，则表示不支持子协议，origins 如果不设置，则表示接受所有 origin 的握手请求；
- 用户通过 userFunc 来自定义处理升级请求的行为，如处理 cookie 等，传入的 userFunc 要求返回一个 [HttpHeaders](http_package_classes.md#class-httpheaders) 对象，其会通过 101 响应回给客户端（升级失败的请求则不会）；
- 暂不支持 [WebSocket](http_package_classes.md#class-websocket) 的 extensions，因此如果握手过程中出现 extensions 协商则会抛 [WebSocketException](http_package_exceptions.md#class-websocketexception)；
- 只支持 HTTP1_1 和 HTTP2_0 向 [WebSocket](http_package_classes.md#class-websocket) 升级。

参数：

- ctx: [HttpContext](http_package_classes.md#class-httpcontext) - Http 请求上下文，将传入给 handler 的直接传给 upgradeFromServer 即可。
- subProtocols!: ArrayList\<String> - 用户配置的子协议列表，默认值为空，表示不支持。如果用户配置了，则会选取升级请求中最靠前的作为升级后的 [WebSocket](http_package_classes.md#class-websocket) 的子协议，用户可通过调用返回的 [WebSocket](http_package_classes.md#class-websocket) 的 subProtocol 查看子协议。
- origins!: ArrayList\<String> - 用户配置的同意握手的 origin 的白名单，如果不配置，则同意来自所有 origin 的握手，如果配置了，则只接受来自配置 origin 的握手。
- userFunc!: ([HttpRequest](http_package_classes.md#class-httprequest)) ->[HttpHeaders](http_package_classes.md#class-httpheaders) - 用户配置的自定义处理升级请求的函数，该函数返回一个 [HttpHeaders](http_package_classes.md#class-httpheaders)。

返回值：

- [WebSocket](http_package_classes.md#class-websocket) - 升级得到的 [WebSocket](http_package_classes.md#class-websocket) 实例。

### func closeConn()

```cangjie
public func closeConn(): Unit
```

功能：提供关闭底层 [WebSocket](http_package_classes.md#class-websocket) 连接的函数。

> **说明：**
>
> 直接关闭底层连接。正常的关闭流程需要遵循协议规定的握手流程，即先发送 Close 帧给对端，并等待对端回应的 Close 帧。握手流程结束后方可关闭底层连接。

### func read()

```cangjie
public func read(): WebSocketFrame
```

功能：从连接中读取一个帧，如果连接上数据未就绪会阻塞，非线程安全（即对同一个 [WebSocket](http_package_classes.md#class-websocket) 对象不支持多线程读）。

read 函数返回一个 [WebSocketFrame](http_package_classes.md#class-websocketframe) 对象，用户可以调用 [WebSocketFrame](http_package_classes.md#class-websocketframe) 的 frameType，fin 属性确定其帧类型和是否是分段帧调用。通过 [WebSocketFrame](http_package_classes.md#class-websocketframe) 的 payload 函数得到原始二进制数据数组：Array\<UInt8>

- 分段帧的首帧为 fin == false，frameType == TextWebFrame 或 BinaryWebFrame 中间帧 fin == false，frameType == ContinuationWebFrame 尾帧 fin == true， frameType == ContinuationWebFrame；
- 非分段帧为     fin == true， frameType != ContinuationWebFrame。

> **注意：**
>
> - 数据帧（Text，Binary）可以分段，用户需要多次调用 read 将所有分段帧读完（以下称为接收到完整的 message），再将分段帧的 payload 按接收序拼接 Text 帧的 payload 为 UTF-8 编码，用户在接收到完整的 message 后，调用 String.fromUtf8 函数将拼接后的 payload 转成字符串 Binary 帧的 payload 的意义由使用其的应用确定，用户在接收到完整的 message 后，将拼接后的 payload 传给上层应用；
> - 控制帧（Close，Ping，Pong）不可分段；
> - 控制帧本身不可分段，但其可以穿插在分段的数据帧之间。分段的数据帧之间不可出现其他数据帧，如果用户收到穿插的分段数据帧，则需要当作错误处理；
> - 客户端收到 masked 帧，服务器收到 unmasked 帧，断开底层连接并抛出异常；
> - rsv1、rsv2、rsv3 位被设置（暂不支持 extensions，因此 rsv 位必须为 0），断开底层连接并抛出异常；
> - 收到无法理解的帧类型（只支持 Continuation，Text，Binary，Close，Ping，Pong），断开底层连接并抛出异常；
> - 收到分段或 payload 长度大于 125 bytes 的控制帧（Close，Ping，Pong），断开底层连接并抛出异常；
> - 收到 payload 长度大于 20M 的帧，断开底层连接并抛出异常；
> - closeConn 关闭连接后继续调用读，抛出异常。

返回值：

- [WebSocketFrame](http_package_classes.md#class-websocketframe) - 读到的 [WebSocketFrame](http_package_classes.md#class-websocketframe) 对象。

异常：

- SocketException - 底层连接错误。
- [WebSocketException](http_package_exceptions.md#class-websocketexception) - 收到不符合协议规定的帧，此时会给对端发送 Close 帧说明错误信息，并断开底层连接。
- [ConnectionException](http_package_exceptions.md#class-connectionexception) - 从连接中读数据时对端已关闭连接抛此异常。

### func write(WebSocketFrameType, Array\<UInt8>, Int64)

```cangjie
public func write(frameType: WebSocketFrameType, byteArray: Array<UInt8>, frameSize!: Int64 = FRAMESIZE): Unit
```

功能：发送数据，非线程安全（即对同一个 [WebSocket](http_package_classes.md#class-websocket) 对象不支持多线程写）。

> **注意：**
>
> write 函数将数据以 [WebSocket](http_package_classes.md#class-websocket) 帧的形式发送给对端；
>
> - 如果发送数据帧（Text，Binary），传入的 byteArray 如果大于 frameSize（默认 4 * 1024 bytes），我们会将其分成小于等于 frameSize 的 payload 以分段帧的形式发送，否则不分段；
> - 如果发送控制帧（Close，Ping，Pong），传入的 byteArray 的大小需要小于等于 125 bytes，Close 帧的前两个字节为状态码，可用的状态码见 RFC 6455 7.4. Status Codes 协议规定，Close 帧发送之后，禁止再发送数据帧，如果发送则会抛出异常；
> - 用户需要自己保证其传入的 byteArray 符合协议，如 Text 帧的 payload 需要是 UTF-8 编码，如果数据帧设置了 frameSize，那么需要大于 0，否则抛出异常；
> - 发送数据帧时，frameSize 小于等于 0，抛出异常；
> - 用户发送控制帧时，传入的数据大于 125 bytes，抛出异常；
> - 用户传入非 Text，Binary，Close，Ping，Pong 类型的帧类型，抛出异常；
> - 发送 Close 帧时传入非法的状态码，或 reason 数据超过 123 bytes，抛出异常；
> - 发送完 Close 帧后继续发送数据帧，抛出异常；
> - closeConn 关闭连接后调用写，抛出异常。

参数：

- frameType: [WebSocketFrameType](http_package_enums.md#enum-websocketframetype) - 所需发送的帧的类型。
- byteArray: Array\<UInt8> - 所需发送的帧的 payload（二进制形式）。
- frameSize!: Int64 - 分段帧的大小，默认为 4 * 1024 bytes，frameSize 不会对控制帧生效（控制帧设置了无效）。

异常：

- SocketException - 底层连接错误时抛出异常。
- [WebSocketException](http_package_exceptions.md#class-websocketexception) - 传入非法的帧类型，或者数据时抛出异常。

### func writeCloseFrame(?UInt16, String)

```cangjie
public func writeCloseFrame(status!: ?UInt16 = None, reason!: String = ""): Unit
```

功能：发送 Close 帧。

> **注意：**
>
> 协议规定，Close 帧发送之后，禁止再发送数据帧。如果用户不设置 status，那么 reason 不会被发送（即有 reason 必有 status）；控制帧的 payload 不超过 125 bytes，Close 帧的前两个 bytes 为 status，因此 reason 不能超过 123 bytes，closeConn 关闭连接后调用写，抛出异常。

参数：

- status!: ?UInt16 - 发送的 Close 帧的状态码，默认为 None，表示不发送状态码和 reason。
- reason!: String - 关闭连接的说明，默认为空字符串，发送时会转成 UTF-8，不保证可读，debug 用。

异常：

- [WebSocketException](http_package_exceptions.md#class-websocketexception) - 传入非法的状态码，或 reason 数据超过 123 bytes 时抛出异常。

### func writePingFrame(Array\<UInt8>)

```cangjie
public func writePingFrame(byteArray: Array<UInt8>): Unit
```

功能：提供发送 Ping 帧的快捷函数，closeConn 关闭连接后调用写，抛出异常。

参数：

- byteArray: Array\<UInt8> - 所需发送的帧的 payload（二进制形式）。

异常：

- SocketException - 底层连接错误时抛出异常。
- [WebSocketException](http_package_exceptions.md#class-websocketexception) - 传入的数据大于 125 bytes，抛出异常。

### func writePongFrame(Array\<UInt8>)

```cangjie
public func writePongFrame(byteArray: Array<UInt8>): Unit
```

功能：提供发送 Pong 帧的快捷函数，closeConn 关闭连接后调用写，抛出异常。

参数：

- byteArray: Array\<UInt8> - 所需发送的帧的 payload（二进制形式）。

异常：

- SocketException - 底层连接错误时抛出异常。
- [WebSocketException](http_package_exceptions.md#class-websocketexception) - 传入的数据大于 125 bytes，抛出异常。

## class WebSocketFrame

```cangjie
public class WebSocketFrame
```

功能：[WebSocket](http_package_classes.md#class-websocket) 用于读的基本单元。

[WebSocketFrame](http_package_classes.md#class-websocketframe) 提供了三个属性，其中 fin 和 frameType 共同说明了帧是否分段和帧的类型。payload 为帧的载荷。

- 分段帧的首帧为 fin == false，frameType == TextWebFrame 或 BinaryWebFrame；
- 中间帧 fin == false，frameType == ContinuationWebFrame；
- 尾帧 fin == true， frameType == ContinuationWebFrame；
- 非分段帧为     fin == true， frameType != ContinuationWebFrame；
- 用户仅能通过 [WebSocket](http_package_classes.md#class-websocket) 对象的 read 函数得到 [WebSocketFrame](http_package_classes.md#class-websocketframe)。数据帧可分段，如果用户收到分段帧，则需要多次调用 read 函数直到收到完整的 message，并将所有分段的 payload 按接收顺序拼接。

> **注意：**
>
> 由于控制帧可以穿插在分段帧之间，用户在拼接分段帧的 payload 时需要单独处理控制帧。分段帧之间仅可穿插控制帧，如果用户在分段帧之间接收到其他数据帧，则需要当作错误处理。

### prop fin

```cangjie
public prop fin: Bool
```

功能：获取 [WebSocketFrame](http_package_classes.md#class-websocketframe) 的 fin 属性，fin 与 frameType 共同说明了帧是否分段和帧的类型。

类型：Bool

### prop frameType

```cangjie
public prop frameType: WebSocketFrameType
```

功能：获取 [WebSocketFrame](http_package_classes.md#class-websocketframe) 的帧类型，fin 与 frameType 共同说明了帧是否分段和帧的类型。

类型：[WebSocketFrameType](http_package_enums.md#enum-websocketframetype)

### prop payload

```cangjie
public prop payload: Array<UInt8>
```

功能：获取 [WebSocketFrame](http_package_classes.md#class-websocketframe) 的帧载荷。如果是分段数据帧，用户需要在接收到完整的 message 后，将所有分段的 payload 按接收序拼接。

类型：Array\<UInt8>
