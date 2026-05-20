# stdx.net.http

## 功能介绍

http 包提供 HTTP/1.1、HTTP/2 和 WebSocket 协议的 server、client 端实现。

关于协议的详细内容可参考 [RFC 9110](https://httpwg.org/specs/rfc9110.html)、[9112](https://httpwg.org/specs/rfc9112.html)、[9113](https://httpwg.org/specs/rfc9113.html)、[9218](https://httpwg.org/specs/rfc9218.html)、[7541](https://httpwg.org/specs/rfc7541.html) 等。

使用本包需要外部依赖 `OpenSSL 3` 的 `ssl` 和 `crypto` 动态库文件，故使用前需安装相关工具：

- 对于 `Linux` 操作系统，可参考以下方式：
    - 如果系统的包管理工具支持安装 `OpenSSL 3` 开发工具包，可通过这个方式安装，并确保系统安装目录下含有 `libssl.so`、`libssl.so.3`、`libcrypto.so` 和 `libcrypto.so.3` 这些动态库文件，例如 `Ubuntu 22.04` 系统上可使用 `sudo apt install libssl-dev` 命令安装 `libssl-dev` 工具包；
    - 如果无法通过上面的方式安装，可自行下载 `OpenSSL 3.x.x` 源码编译安装软件包，并确保安装目录下含有 `libssl.so`、`libssl.so.3`、`libcrypto.so` 和 `libcrypto.so.3` 这些动态库文件，然后可选择下面任意一种方式来保证系统链接器可以找到这些文件：
        - 在系统未安装 OpenSSL 的场景，安装时选择直接安装到系统路径下；
        - 安装在自定义目录的场景，将这些文件所在目录设置到环境变量 `LD_LIBRARY_PATH` 以及 `LIBRARY_PATH` 中。
- 对于 `Windows` 操作系统，可按照以下步骤：
    - 自行下载 `OpenSSL 3.x.x` 源码编译安装 x64 架构软件包或者自行下载安装第三方预编译的供开发人员使用的 `OpenSSL 3.x.x` 软件包；
    - 确保安装目录下含有 `libssl.dll.a`（或 `libssl.lib`）、`libssl-3-x64.dll`、`libcrypto.dll.a`（或 `libcrypto.lib`）、`libcrypto-3-x64.dll` 这些库文件；
    - 将 `libssl.dll.a`（或 `libssl.lib`）、`libcrypto.dll.a`（或 `libcrypto.lib`）所在的目录路径设置到环境变量 `LIBRARY_PATH` 中，将 `libssl-3-x64.dll`、`libcrypto-3-x64.dll` 所在的目录路径设置到环境变量 `PATH` 中。
- 对于 `macOS` 操作系统，可参考以下方式：
    - 使用 `brew install openssl@3` 安装，并确保系统安装目录下含有 `libcrypto.dylib` 和 `libcrypto.3.dylib` 这两个动态库文件；
    - 如果无法通过上面的方式安装，可自行下载 `OpenSSL 3.x.x` 源码编译安装软件包，并确保安装目录下含有 `libcrypto.dylib` 和 `libcrypto.3.dylib` 这两个动态库文件，然后可选择下面任意一种方式来保证系统链接器可以找到这些文件：
        - 在系统未安装 OpenSSL 的场景，安装时选择直接安装到系统路径下；
        - 安装在自定义目录的场景，将这些文件所在目录设置到环境变量 `DYLD_LIBRARY_PATH` 以及 `LIBRARY_PATH` 中。

如果未安装 `OpenSSL 3`软件包或者安装低版本的软件包，程序可能无法使用并抛出 TLS 相关异常。

### http

用户可以选择 http 协议的版本，如 HTTP/1.1、HTTP/2。http 包的多数 API 并不区分这两种协议版本，只有当用户用到某个版本的特有功能时，才需要做这种区分，如 HTTP/1.1 中的 chunked 的 transfer-encoding，HTTP/2 中的 server push。

http 库默认使用 HTTP/1.1 版本。当开发者需要使用 HTTP/2 协议时，需要为 Client/Server 配置 tls，并且设置 alpn 的值为 `h2`；不支持 HTTP/1.1 通过 `Upgrade: h2c` 协议升级的方式升级到 HTTP/2。

如果创建 HTTP/2 连接握手失败，Client/Server 会自动将协议退回 HTTP/1.1。

- 用户通过 [ClientBuilder](./http_package_api/http_package_classes.md#class-clientbuilder) 构建一个 Client 实例，构建过程可以指定多个参数，如 httpProxy、logger、cookieJar、是否自动 redirect、连接池大小等。

- 用户通过 [ServerBuilder](./http_package_api/http_package_classes.md#class-serverbuilder) 构建一个 Server 实例，构建过程可以指定多个参数，如 addr、port、logger、distributor 等。

用户如果需要自己设置 Logger，需要保证它是线程安全的。

Client、Server 的大多数参数在构建后便不允许修改，如果想要更改，用户需要重新构建一个新的 Client 或 Server 实例；如果该参数支持动态修改，本实现会提供显式的功能，如 Server 端 cert、CA 的热更新。

- 通过 Client 实例，用户可以发送 http request、接收 http response。

- 通过 Server 实例，用户可以配置 request 转发处理器，启动 http server。在 server handler 中，用户可以通过 HttpContext 获取 client 发来的 request 的详细信息，构造发送给 client 的 response。
Server 端根据 Client 端请求，创建对应的 ProtocolService 实例，同一个 Server 实例可同时支持两种协议：HTTP/1.1、HTTP/2。

- 在 client 端，用户通过 HttpRequestBuilder 构造 request，构建过程可以指定多个参数，如 method、url、version、headers、body、trailers 等等；构建之后的 request 不允许再进行修改。

- 在 server 端，用户通过 HttpResponseBuilder 构造 response，构建过程可以指定多个参数，如 status、headers、body、trailers 等等；构建之后的 response 不允许再进行修改。

另外，本实现提供一些工具类，方便用户构造一些常用 response，如 RedirectHandler 构造 redirect response，NotFoundHandler 构造 404 response。

### WebSocket

本实现为 WebSocket 提供 sub-protocol 协商，包括基础的 frame 解码、读取、消息发送、frame 编码、ping、pong、关闭等功能。

用户通过 WebSocket.upgradeFromClient 从一个 HTTP/1.1 或 HTTP/2 Client 实例升级到 WebSocket 协议，之后通过返回的 WebSocket 实例进行 WebSocket 通讯。

用户在一个 server 端的 handler 中，通过 WebSocket.upgradeFromServer 从 HTTP/1.1 或 HTTP/2 协议升级到 WebSocket 协议，之后通过返回的 WebSocket 实例进行 WebSocket 通讯。

按照协议，HTTP/1.1 中，升级后的 WebSocket 连接是建立在 tcp/tls 连接之上；HTTP/2 中，升级后的 WebSocket 连接是建立在 HTTP/2 connection 的一个 stream 之上。HTTP/1.1 中，close 最终会直接关闭 tcp/tls 连接；HTTP/2 中，close 只会关闭 connection 上的一个 stream。

## API 列表

### 函数

|              函数名          |           功能           |
| --------------------------- | ------------------------ |
| [handleError(HttpContext, UInt16)](./http_package_api/http_package_funcs.md#func-handleerrorhttpcontext-uint16) | 便捷的 Http 请求处理函数，用于回复错误请求。  |
| [notFound(HttpContext)](./http_package_api/http_package_funcs.md#func-notfoundhttpcontext) | 便捷的 Http 请求处理函数，用于回复 404 响应。 |
| [upgrade(HttpContext)](./http_package_api/http_package_funcs.md#func-upgradehttpcontext) | 在 handler 内获取 StreamingSocket，可用于支持协议升级和处理 CONNECT 请求。  |

### 接口

|             接口名          |           功能           |
| --------------------------- | ------------------------ |
| [CookieJar](./http_package_api/http_package_interfaces.md#interface-cookiejar) | Client 用来管理 Cookie 的工具。  |
| [HttpRequestDistributor](./http_package_api/http_package_interfaces.md#interface-httprequestdistributor) | Http request 分发器接口，将一个 request 按照 url 中的 path 分发给对应的 HttpRequestHandler 处理。  |
| [HttpRequestHandler](./http_package_api/http_package_interfaces.md#interface-httprequesthandler) | Http request 处理器。  |
| [ProtocolServiceFactory](./http_package_api/http_package_interfaces.md#interface-protocolservicefactory) | Http 服务实例工厂，用于生成 `ProtocolService` 实例。  |

### 类

|              类名          |           功能           |
| --------------------------- | ------------------------ |
| [Client](./http_package_api/http_package_classes.md#class-client) | Client 类，用户可以通过 Client 实例发送 HTTP/1.1 或 HTTP/2 请求。  |
| [ClientBuilder](./http_package_api/http_package_classes.md#class-clientbuilder) | 用于 Client 实例的构建，Client 没有公开的构造函数，用户只能通过 ClientBuilder 得到 Client 实例。ClientBuilder 文档中未明确说明支持版本的配置，在 HTTP/1.1 与 HTTP/2 都会生效。  |
| [Cookie](./http_package_api/http_package_classes.md#class-cookie) | HTTP 本身是无状态的，server 为了知道 client 的状态，提供个性化的服务，便可以通过 Cookie 来维护一个有状态的会话。  |
| [FileHandler](./http_package_api/http_package_classes.md#class-filehandler) | 用于处理文件下载或者文件上传。  |
| [FuncHandler](./http_package_api/http_package_classes.md#class-funchandler) | HttpRequestHandler 接口包装类，把单个函数包装成 HttpRequestHandler。  |
| [HttpContext](./http_package_api/http_package_classes.md#class-httpcontext) | Http 请求上下文，作为 HttpRequestHandler.handle 函数的参数在服务端使用。  |
| [HttpHeaders](./http_package_api/http_package_classes.md#class-httpheaders) | 用于表示 Http 报文中的 header 和 trailer，定义了相关增、删、改、查操作。  |
| [HttpRequest](./http_package_api/http_package_classes.md#class-httprequest) | Http 请求类。  |
| [HttpRequestBuilder](./http_package_api/http_package_classes.md#class-httprequestbuilder) | HttpRequestBuilder 类用于构造 HttpRequest 实例。  |
| [HttpResponse](./http_package_api/http_package_classes.md#class-httpresponse) | Http 响应类。  |
| [HttpResponseBuilder](./http_package_api/http_package_classes.md#class-httpresponsebuilder) | 用于构造 HttpResponse 实例。  |
| [HttpResponsePusher](./http_package_api/http_package_classes.md#class-httpresponsepusher) | HTTP/2 服务器推送。  |
| [HttpResponseWriter](./http_package_api/http_package_classes.md#class-httpresponsewriter) | HTTP response 消息体 Writer，支持用户控制消息体的发送过程。  |
| [NotFoundHandler](./http_package_api/http_package_classes.md#class-notfoundhandler) | 便捷的 Http 请求处理器，`404 Not Found` 处理器。  |
| [OptionsHandler](./http_package_api/http_package_classes.md#class-optionshandler) | 便捷的 Http 处理器，用于处理 OPTIONS 请求。固定返回 "Allow: OPTIONS，GET，HEAD，POST，PUT，DELETE" 响应头。  |
| [ProtocolService](./http_package_api/http_package_classes.md#class-protocolservice) | Http 协议服务实例，为单个客户端连接提供 Http 服务，包括对客户端 request 报文的解析、 request 的分发处理、 response 的发送等。  |
| [RedirectHandler](./http_package_api/http_package_classes.md#class-redirecthandler) | 便捷的 Http 处理器，用于回复重定向响应。  |
| [Server](./http_package_api/http_package_classes.md#class-server) | 提供 HTTP 服务的 Server 类。  |
| [ServerBuilder](./http_package_api/http_package_classes.md#class-serverbuilder) | 提供 Server 实例构建器。  |
| [WebSocket](./http_package_api/http_package_classes.md#class-websocket) | 提供 WebSocket 服务的相关类，提供 WebSocket 连接的读、写、关闭等函数。用户通过 upgradeFrom 函数以获取 WebSocket 连接。  |
| [WebSocketFrame](./http_package_api/http_package_classes.md#class-websocketframe) | WebSocket 用于读的基本单元。  |

### 枚举

|             枚举名          |           功能           |
| --------------------------- | ------------------------ |
| [FileHandlerType](./http_package_api/http_package_enums.md#enum-filehandlertype) | 用于设置 `FileHandler` 是上传还是下载模式。  |
| [Protocol](./http_package_api/http_package_enums.md#enum-protocol) | 定义 HTTP 协议类型枚举。  |
| [WebSocketFrameType](./http_package_api/http_package_enums.md#enum-websocketframetype) | 定义 `WebSocketFrame` 的枚举类型。  |

### 结构体

|            结构体名          |           功能           |
| --------------------------- | ------------------------ |
| [HttpStatusCode](./http_package_api/http_package_structs.md#struct-httpstatuscode) | 用来表示网页服务器超文本传输协议响应状态的 3 位数字代码。  |
| [ServicePoolConfig](./http_package_api/http_package_structs.md#struct-servicepoolconfig) | Http Server 协程池配置。  |
| [TransportConfig](./http_package_api/http_package_structs.md#struct-transportconfig) | 传输层配置类，服务器建立连接使用的传输层配置。  |

### 异常类

|            异常类名          |           功能           |
| --------------------------- | ------------------------ |
| [ConnectionException](./http_package_api/http_package_exceptions.md#class-connectionexception) | Http 的 tcp 连接异常类。  |
| [CoroutinePoolRejectException](./http_package_api/http_package_exceptions.md#class-coroutinepoolrejectexception) | Http 的协程池拒绝请求处理异常类。  |
| [HttpException](./http_package_api/http_package_exceptions.md#class-httpexception) | Http 的通用异常类。  |
| [HttpStatusException](./http_package_api/http_package_exceptions.md#class-httpstatusexception) | Http 的响应状态异常类。  |
| [HttpTimeoutException](./http_package_api/http_package_exceptions.md#class-httptimeoutexception) | Http 的超时异常类。  |
| [WebSocketException](./http_package_api/http_package_exceptions.md#class-websocketexception) | WebSocket 的通用异常类。  |
