# 结构体

## struct HttpStatusCode

```cangjie
public struct HttpStatusCode {
    public static const STATUS_CONTINUE: UInt16 =                        100
    public static const STATUS_SWITCHING_PROTOCOLS: UInt16 =             101
    public static const STATUS_PROCESSING: UInt16 =                      102
    public static const STATUS_EARLY_HINTS: UInt16 =                     103
 
    public static const STATUS_OK: UInt16 =                              200
    public static const STATUS_CREATED: UInt16 =                         201
    public static const STATUS_ACCEPTED: UInt16 =                        202
    public static const STATUS_NON_AUTHORITATIVE_INFO: UInt16 =          203
    public static const STATUS_NO_CONTENT: UInt16 =                      204
    public static const STATUS_RESET_CONTENT: UInt16 =                   205
    public static const STATUS_PARTIAL_CONTENT: UInt16 =                 206
    public static const STATUS_MULTI_STATUS: UInt16 =                    207
    public static const STATUS_ALREADY_REPORTED: UInt16 =                208
    public static const STATUS_IM_USED: UInt16 =                         226
 
    public static const STATUS_MULTIPLE_CHOICES: UInt16 =                300
    public static const STATUS_MOVED_PERMANENTLY: UInt16 =               301
    public static const STATUS_FOUND: UInt16 =                           302
    public static const STATUS_SEE_OTHER: UInt16 =                       303
    public static const STATUS_NOT_MODIFIED: UInt16 =                    304
    public static const STATUS_USE_PROXY: UInt16 =                       305
    public static const STATUS_TEMPORARY_REDIRECT: UInt16 =              307
    public static const STATUS_PERMANENT_REDIRECT: UInt16 =              308
 
    public static const STATUS_BAD_REQUEST: UInt16 =                     400
    public static const STATUS_UNAUTHORIZED: UInt16 =                    401
    public static const STATUS_PAYMENT_REQUIRED: UInt16 =                402
    public static const STATUS_FORBIDDEN: UInt16 =                       403
    public static const STATUS_NOT_FOUND: UInt16 =                       404
    public static const STATUS_METHOD_NOT_ALLOWED: UInt16 =              405
    public static const STATUS_NOT_ACCEPTABLE: UInt16 =                  406
    public static const STATUS_PROXY_AUTH_REQUIRED: UInt16 =             407
    public static const STATUS_REQUEST_TIMEOUT: UInt16 =                 408
    public static const STATUS_CONFLICT: UInt16 =                        409
    public static const STATUS_GONE: UInt16 =                            410
    public static const STATUS_LENGTH_REQUIRED: UInt16 =                 411
    public static const STATUS_PRECONDITION_FAILED: UInt16 =             412
    public static const STATUS_REQUEST_CONTENT_TOO_LARGE: UInt16 =       413
    public static const STATUS_REQUEST_URI_TOO_LONG: UInt16 =            414
    public static const STATUS_UNSUPPORTED_MEDIA_TYPE: UInt16 =          415
    public static const STATUS_REQUESTED_RANGE_NOT_SATISFIABLE: UInt16 = 416
    public static const STATUS_EXPECTATION_FAILED: UInt16 =              417
    public static const STATUS_TEAPOT: UInt16 =                          418
    public static const STATUS_MISDIRECTED_REQUEST: UInt16 =             421
    public static const STATUS_UNPROCESSABLE_ENTITY: UInt16 =            422
    public static const STATUS_LOCKED: UInt16 =                          423
    public static const STATUS_FAILED_DEPENDENCY: UInt16 =               424
    public static const STATUS_TOO_EARLY: UInt16 =                       425
    public static const STATUS_UPGRADE_REQUIRED: UInt16 =                426
    public static const STATUS_PRECONDITION_REQUIRED: UInt16 =           428
    public static const STATUS_TOO_MANY_REQUESTS: UInt16 =               429
    public static const STATUS_REQUEST_HEADER_FIELDS_TOO_LARGE: UInt16 = 431
    public static const STATUS_UNAVAILABLE_FOR_LEGAL_REASONS: UInt16 =   451
 
    public static const STATUS_INTERNAL_SERVER_ERROR: UInt16 =           500
    public static const STATUS_NOT_IMPLEMENTED: UInt16 =                 501
    public static const STATUS_BAD_GATEWAY: UInt16 =                     502
    public static const STATUS_SERVICE_UNAVAILABLE: UInt16 =             503
    public static const STATUS_GATEWAY_TIMEOUT: UInt16 =                 504
    public static const STATUS_HTTP_VERSION_NOT_SUPPORTED: UInt16 =      505
    public static const STATUS_VARIANT_ALSO_NEGOTIATES: UInt16 =         506
    public static const STATUS_INSUFFICIENT_STORAGE: UInt16 =            507
    public static const STATUS_LOOP_DETECTED: UInt16 =                   508
    public static const STATUS_NOT_EXTENDED: UInt16 =                    510
    public static const STATUS_NETWORK_AUTHENTICATION_REQUIRED: UInt16 = 511
}
```

功能：用来表示网页服务器超文本传输协议响应状态的 3 位数字代码。

状态码由 RFC 9110 规范定义，并得到 RFC2518、RFC 3229、RFC 4918、RFC 5842、RFC 7168 与 RFC 8297 等规范扩展。

所有状态码的第一个数字代表了响应的五种状态之一：

- 状态代码的 1xx（信息）指示在完成请求的操作并发送最终响应之前通信连接状态或请求进度的临时响应。
- 状态代码的 2xx（成功）指示客户端的请求已成功接收、理解和接受。
- 状态代码的 3xx（重定向）指示用户代理需要采取进一步的操作才能完成请求。
- 状态代码的 4xx（客户端错误）指示客户端似乎出错。
- 状态代码的 5xx（服务器错误）指示服务器意识到它出错或无法执行请求的方法。

### static const STATUS_ACCEPTED

```cangjie
public static const STATUS_ACCEPTED: UInt16 = 202
```

功能：服务器已接受请求，但尚未处理。

类型：UInt16

### static const STATUS_ALREADY_REPORTED

```cangjie
public static const STATUS_ALREADY_REPORTED: UInt16 = 208
```

功能：消息体将是一个 XML 消息。

类型：UInt16

### static const STATUS_BAD_GATEWAY

```cangjie
public static const STATUS_BAD_GATEWAY: UInt16 = 502
```

功能：作为网关或者代理工作的服务器尝试执行请求时，从上游服务器接收到无效的响应。

类型：UInt16

### static const STATUS_BAD_REQUEST

```cangjie
public static const STATUS_BAD_REQUEST: UInt16 = 400
```

功能：语义有误，当前请求无法被服务器理解；或请求参数有误。

类型：UInt16

### static const STATUS_CONFLICT

```cangjie
public static const STATUS_CONFLICT: UInt16 = 409
```

功能：由于和被请求的资源的当前状态之间存在冲突，请求无法完成。

类型：UInt16

### static const STATUS_CONTINUE

```cangjie
public static const STATUS_CONTINUE: UInt16 = 100
```

功能：这个临时响应是用来通知客户端它的部分请求已经被服务器接收，且仍未被拒绝。

类型：UInt16

> **说明：**
>
> 客户端应当继续发送请求的剩余部分，或者如果请求已经完成，忽略这个响应。
> 服务器必须在请求完成后向客户端发送一个最终响应。

### static const STATUS_CREATED

```cangjie
public static const STATUS_CREATED: UInt16 = 201
```

功能：请求已经被实现，而且有一个新的资源已经依据请求的需要而建立，且其 URI 已经随 Location 头信息返回。

类型：UInt16

### static const STATUS_EARLY_HINTS

```cangjie
public static const STATUS_EARLY_HINTS: UInt16 = 103
```

功能：提前预加载 (css、js) 文档。

类型：UInt16

### static const STATUS_EXPECTATION_FAILED

```cangjie
public static const STATUS_EXPECTATION_FAILED: UInt16 = 417
```

功能：服务器无法满足 Expect 的请求头信息。

类型：UInt16

### static const STATUS_FAILED_DEPENDENCY

```cangjie
public static const STATUS_FAILED_DEPENDENCY: UInt16 = 424
```

功能：由于之前的某个请求发生的错误，导致当前请求失败。

类型：UInt16

### static const STATUS_FORBIDDEN

```cangjie
public static const STATUS_FORBIDDEN: UInt16 = 403
```

功能：服务器已经理解请求，但是拒绝执行。

类型：UInt16

### static const STATUS_FOUND

```cangjie
public static const STATUS_FOUND: UInt16 = 302
```

功能：临时移动。

类型：UInt16

> **说明：**
>
> 请求的资源已被临时的移动到新 URI，客户端应当继续向原有地址发送以后的请求。

### static const STATUS_GATEWAY_TIMEOUT

```cangjie
public static const STATUS_GATEWAY_TIMEOUT: UInt16 = 504
```

功能：从上游服务器（URI 标识出的服务器，例如 HTTP、FTP、LDAP）或者辅助服务器（例如 DNS）收到响应超时。

类型：UInt16

### static const STATUS_GONE

```cangjie
public static const STATUS_GONE: UInt16 = 410
```

功能：被请求的资源在服务器上已经不再可用，而且没有任何已知的转发地址。

类型：UInt16

### static const STATUS_HTTP_VERSION_NOT_SUPPORTED

```cangjie
public static const STATUS_HTTP_VERSION_NOT_SUPPORTED: UInt16 = 505
```

功能：服务器不支持，或者拒绝支持在请求中使用的 HTTP 版本。

类型：UInt16

### static const STATUS_IM_USED

```cangjie
public static const STATUS_IM_USED: UInt16 = 226
```

功能：服务器已完成对资源的请求，并且响应是应用于当前实例的一个或多个实例操作的结果的表示。

类型：UInt16

### static const STATUS_INSUFFICIENT_STORAGE

```cangjie
public static const STATUS_INSUFFICIENT_STORAGE: UInt16 = 507
```

功能：服务器无法存储完成请求所必须的内容。

类型：UInt16

### static const STATUS_INTERNAL_SERVER_ERROR

```cangjie
public static const STATUS_INTERNAL_SERVER_ERROR: UInt16 = 500
```

功能：服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理。

类型：UInt16

### static const STATUS_LENGTH_REQUIRED

```cangjie
public static const STATUS_LENGTH_REQUIRED: UInt16 = 411
```

功能：服务器拒绝在没有定义 Content-Length 头的情况下接受请求。

类型：UInt16

### static const STATUS_LOCKED

```cangjie
public static const STATUS_LOCKED: UInt16 = 423
```

功能：当前资源被锁定。

类型：UInt16

### static const STATUS_LOOP_DETECTED

```cangjie
public static const STATUS_LOOP_DETECTED: UInt16 = 508
```

功能：服务器在处理请求时检测到无限递归。

类型：UInt16

### static const STATUS_METHOD_NOT_ALLOWED

```cangjie
public static const STATUS_METHOD_NOT_ALLOWED: UInt16 = 405
```

功能：请求行中指定的请求函数不能被用于请求响应的资源。

类型：UInt16

### static const STATUS_MISDIRECTED_REQUEST

```cangjie
public static const STATUS_MISDIRECTED_REQUEST: UInt16 = 421
```

功能：请求被指向到无法生成响应的服务器。

类型：UInt16

### static const STATUS_MOVED_PERMANENTLY

```cangjie
public static const STATUS_MOVED_PERMANENTLY: UInt16 = 301
```

功能：永久移动。

类型：UInt16

> **说明：**
>
> 请求的资源已被永久的移动到新 URI，返回信息会包括新的 URI，浏览器会自动定向到新 URI。

### static const STATUS_MULTIPLE_CHOICES

```cangjie
public static const STATUS_MULTIPLE_CHOICES: UInt16 = 300
```

功能：被请求的资源有一系列可供选择的回馈信息，每个都有自己特定的地址和浏览器驱动的商议信息。

类型：UInt16

> **说明：**
>
> 用户或浏览器能够自行选择一个首选的地址进行重定向。

### static const STATUS_MULTI_STATUS

```cangjie
public static const STATUS_MULTI_STATUS: UInt16 = 207
```

功能：DAV 绑定的成员已经在（多状态）响应之前的部分被列举，且未被再次包含。

类型：UInt16

### static const STATUS_NETWORK_AUTHENTICATION_REQUIRED

```cangjie
public static const STATUS_NETWORK_AUTHENTICATION_REQUIRED: UInt16 = 511
```

功能：要求网络认证。

类型：UInt16

### static const STATUS_NON_AUTHORITATIVE_INFO

```cangjie
public static const STATUS_NON_AUTHORITATIVE_INFO: UInt16 = 203
```

功能：服务器已成功处理了请求。

类型：UInt16

> **说明：**
>
> 返回的实体头部元信息不是在原始服务器上有效的确定集合，而是来自本地或者第三方的拷贝。

### static const STATUS_NOT_ACCEPTABLE

```cangjie
public static const STATUS_NOT_ACCEPTABLE: UInt16 = 406
```

功能：请求的资源的内容特性无法满足请求头中的条件，因而无法生成响应实体。

类型：UInt16

### static const STATUS_NOT_EXTENDED

```cangjie
public static const STATUS_NOT_EXTENDED: UInt16 = 510
```

功能：获取资源所需要的策略并没有被满足。

类型：UInt16

### static const STATUS_NOT_FOUND

```cangjie
public static const STATUS_NOT_FOUND: UInt16 = 404
```

功能：请求失败，请求所希望得到的资源未被在服务器上发现。

类型：UInt16

### static const STATUS_NOT_IMPLEMENTED

```cangjie
public static const STATUS_NOT_IMPLEMENTED: UInt16 = 501
```

功能：服务器不支持当前请求所需要的某个功能。

类型：UInt16

### static const STATUS_NOT_MODIFIED

```cangjie
public static const STATUS_NOT_MODIFIED: UInt16 = 304
```

功能：请求的资源未修改，服务器返回此状态码时，不会返回任何资源。

类型：UInt16

> **说明：**
>
> 客户端通常会缓存访问过的资源，通过提供一个头信息指出客户端希望只返回在指定日期之后修改的资源。

### static const STATUS_NO_CONTENT

```cangjie
public static const STATUS_NO_CONTENT: UInt16 = 204
```

功能：服务器成功处理，但未返回内容。

类型：UInt16

### static const STATUS_OK

```cangjie
public static const STATUS_OK: UInt16 = 200
```

功能：请求已经成功，请求所希望的响应头或数据体将随此响应返回。

类型：UInt16

### static const STATUS_PARTIAL_CONTENT

```cangjie
public static const STATUS_PARTIAL_CONTENT: UInt16 = 206
```

功能：服务器已经成功处理了部分 GET 请求。

类型：UInt16

### static const STATUS_PAYMENT_REQUIRED

```cangjie
public static const STATUS_PAYMENT_REQUIRED: UInt16 = 402
```

功能：为了将来可能的需求而预留的状态码。

类型：UInt16

### static const STATUS_PERMANENT_REDIRECT

```cangjie
public static const STATUS_PERMANENT_REDIRECT: UInt16 = 308
```

功能：请求和所有将来的请求应该使用另一个 URI。

类型：UInt16

### static const STATUS_PRECONDITION_FAILED

```cangjie
public static const STATUS_PRECONDITION_FAILED: UInt16 = 412
```

功能：服务器在验证在请求的头字段中给出先决条件时，没能满足其中的一个或多个。

类型：UInt16

### static const STATUS_PRECONDITION_REQUIRED

```cangjie
public static const STATUS_PRECONDITION_REQUIRED: UInt16 = 428
```

功能：客户端发送 HTTP 请求时，必须要满足的一些预设条件。

类型：UInt16

### static const STATUS_PROCESSING

```cangjie
public static const STATUS_PROCESSING: UInt16 = 102
```

功能：处理将被继续执行。

类型：UInt16

### static const STATUS_PROXY_AUTH_REQUIRED

```cangjie
public static const STATUS_PROXY_AUTH_REQUIRED: UInt16 = 407
```

功能：必须在代理服务器上进行身份验证。

类型：UInt16

### static const STATUS_REQUESTED_RANGE_NOT_SATISFIABLE

```cangjie
public static const STATUS_REQUESTED_RANGE_NOT_SATISFIABLE: UInt16 = 416
```

功能：客户端请求的范围无效。

类型：UInt16

> **说明：**
>
> 请求中包含了 `Range` 请求头，并且 `Range` 中指定的任何数据范围都与当前资源的可用范围不重合；
> 同时请求中又没有定义 `If-Range` 请求头。

### static const STATUS_REQUEST_CONTENT_TOO_LARGE

```cangjie
public static const STATUS_REQUEST_CONTENT_TOO_LARGE: UInt16 = 413
```

功能：请求提交的实体数据大小超过了服务器愿意或者能够处理的范围。

类型：UInt16

### static const STATUS_REQUEST_HEADER_FIELDS_TOO_LARGE

```cangjie
public static const STATUS_REQUEST_HEADER_FIELDS_TOO_LARGE: UInt16 = 431
```

功能：请求头字段太大。

类型：UInt16

### static const STATUS_REQUEST_TIMEOUT

```cangjie
public static const STATUS_REQUEST_TIMEOUT: UInt16 = 408
```

功能：请求超时。客户端没有在服务器预备等待的时间内完成一个请求的发送。

类型：UInt16

### static const STATUS_REQUEST_URI_TOO_LONG

```cangjie
public static const STATUS_REQUEST_URI_TOO_LONG: UInt16 = 414
```

功能：求的 URI 长度超过了服务器能够解释的长度。

类型：UInt16

### static const STATUS_RESET_CONTENT

```cangjie
public static const STATUS_RESET_CONTENT: UInt16 = 205
```

功能：服务器成功处理了请求，且没有返回任何内容，希望请求者重置文档视图。

类型：UInt16

### static const STATUS_SEE_OTHER

```cangjie
public static const STATUS_SEE_OTHER: UInt16 = 303
```

功能：对应当前请求的响应可以在另一个 [URL](../../../encoding/url/url_package_api/url_package_classes.md#class-url) 上被找到，而且客户端应当采用 GET 的方式访问那个资源。

类型：UInt16

### static const STATUS_SERVICE_UNAVAILABLE

```cangjie
public static const STATUS_SERVICE_UNAVAILABLE: UInt16 = 503
```

功能：临时的服务器维护或者过载。

类型：UInt16

### static const STATUS_SWITCHING_PROTOCOLS

```cangjie
public static const STATUS_SWITCHING_PROTOCOLS: UInt16 = 101
```

功能：服务器已经理解了客户端的请求，并将通过 Upgrade 消息头通知客户端采用不同的协议来完成这个请求。

类型：UInt16

> **说明：**
>
> 在发送完这个响应最后的空行后，服务器将会切换到在 Upgrade 消息头中定义的那些协议。

### static const STATUS_TEAPOT

```cangjie
public static const STATUS_TEAPOT: UInt16 = 418
```

功能：服务端无法处理请求，一个愚弄客户端的状态码，被称为“我是茶壶”错误码，不应被认真对待。

类型：UInt16

### static const STATUS_TEMPORARY_REDIRECT

```cangjie
public static const STATUS_TEMPORARY_REDIRECT: UInt16 = 307
```

功能：临时重定向。

类型：UInt16

### static const STATUS_TOO_EARLY

```cangjie
public static const STATUS_TOO_EARLY: UInt16 = 425
```

功能：服务器不愿意冒风险来处理该请求。

类型：UInt16

### static const STATUS_TOO_MANY_REQUESTS

```cangjie
public static const STATUS_TOO_MANY_REQUESTS: UInt16 = 429
```

功能：请求过多。

类型：UInt16

### static const STATUS_UNAUTHORIZED

```cangjie
public static const STATUS_UNAUTHORIZED: UInt16 = 401
```

功能：当前请求需要用户验证。

类型：UInt16

### static const STATUS_UNAVAILABLE_FOR_LEGAL_REASONS

```cangjie
public static const STATUS_UNAVAILABLE_FOR_LEGAL_REASONS: UInt16 = 451
```

功能：该请求因法律原因不可用。

类型：UInt16

### static const STATUS_UNPROCESSABLE_ENTITY

```cangjie
public static const STATUS_UNPROCESSABLE_ENTITY: UInt16 = 422
```

功能：请求格式正确，但是由于含有语义错误，无法响应。

类型：UInt16

### static const STATUS_UNSUPPORTED_MEDIA_TYPE

```cangjie
public static const STATUS_UNSUPPORTED_MEDIA_TYPE: UInt16 = 415
```

功能：服务器无法处理请求附带的媒体格式。

类型：UInt16

> **说明：**
>
> 对于当前请求的函数和所请求的资源，请求中提交的实体并不是服务器中所支持的格式。

### static const STATUS_UPGRADE_REQUIRED

```cangjie
public static const STATUS_UPGRADE_REQUIRED: UInt16 = 426
```

功能：服务器拒绝处理客户端使用当前协议发送的请求，但是可以接受其使用升级后的协议发送的请求。

类型：UInt16

### static const STATUS_USE_PROXY

```cangjie
public static const STATUS_USE_PROXY: UInt16 = 305
```

功能：使用代理，所请求的资源必须通过代理访问。

类型：UInt16

### static const STATUS_VARIANT_ALSO_NEGOTIATES

```cangjie
public static const STATUS_VARIANT_ALSO_NEGOTIATES: UInt16 = 506
```

功能：服务器存在内部配置错误。

类型：UInt16

## struct ServicePoolConfig

```cangjie
public struct ServicePoolConfig {
    public let capacity: Int64
    public let queueCapacity: Int64
    public let preheat: Int64
    public init(capacity!: Int64 = 10 ** 4, queueCapacity!: Int64 = 10 ** 4, preheat!: Int64 = 0)
}
```

功能：Http [Server](http_package_classes.md#class-server) 协程池配置。

> **说明：**
>
> HTTP/1.1 [Server](http_package_classes.md#class-server) 每次收到一个请求，将从协程池取出一个协程进行处理，如果任务等待队列已满，将拒绝服务该次请求，并断开连接。
> HTTP/2 [Server](http_package_classes.md#class-server) 处理过程中会从协程池取出若干协程进行处理，如果任务等待队列已满，将阻塞直至有协程空闲。

### let capacity

```cangjie
public let capacity: Int64
```

功能：获取协程池容量。

类型：Int64

### let preheat

```cangjie
public let preheat: Int64
```

功能：获取服务启动时预先启动的协程数量。

类型：Int64

### let queueCapacity

```cangjie
public let queueCapacity: Int64
```

功能：获取缓冲区等待任务的最大数量。

类型：Int64

### init(Int64, Int64, Int64)

```cangjie
public init(
    capacity!: Int64 = 10 ** 4,
    queueCapacity!: Int64 = 10 ** 4,
    preheat!: Int64 = 0
)
```

功能：构造一个 [ServicePoolConfig](http_package_structs.md#struct-servicepoolconfig) 实例。

参数：

- capacity!: Int64 - 协程池容量，默认值为 10000。
- queueCapacity!: Int64 - 缓冲区等待任务的最大数量，默认值为 10000。
- preheat!: Int64 - 服务启动时预先启动的协程数量，默认值为 0。

异常：

- IllegalArgumentException - 当参数 capacity/queueCapacity/preheat 小于 0，或参数 preheat 大于 capacity。

## struct TransportConfig

```cangjie
public struct TransportConfig
```

功能：传输层配置类，服务器建立连接使用的传输层配置。

### prop keepAliveConfig

```cangjie
public mut prop keepAliveConfig: SocketKeepAliveConfig
```

功能：设定和读取传输层连接的消息保活配置，默认配置空闲时间为 45s，发送探测报文的时间间隔为 5s，在连接被认为无效之前发送的探测报文数 5 次，实际时间粒度可能因操作系统而异。

类型：SocketKeepAliveConfig

### prop readBufferSize

```cangjie
public mut prop readBufferSize: ?Int64
```

功能：设定和读取传输层连接的读缓冲区大小，默认值为 None ，若设置的值小于 0，将在服务器进行服务建立连接后抛出 IllegalArgumentException。

> **说明：**
>
> 使用默认值时，实际的缓冲区大小将由操作系统决定。

类型：?Int64

### prop readTimeout

```cangjie
public mut prop readTimeout: Duration
```

功能：设定和读取传输层连接的读超时时间，如果设置的时间小于 0 将置为 0，默认值为 Duration.Max。

类型：Duration

### prop writeBufferSize

```cangjie
public mut prop writeBufferSize: ?Int64
```

功能：设定和读取传输层连接的写缓冲区大小，默认值为 None ，若设置的值小于 0，将在服务器进行服务建立连接后抛出 IllegalArgumentException。

> **说明：**
>
> 使用默认值时，实际的缓冲区大小将由操作系统决定。

类型：?Int64

### prop writeTimeout

```cangjie
public mut prop writeTimeout: Duration
```

功能：设定和读取传输层连接的写超时时间，如果设置的时间小于 0 将置为 0，默认值为 Duration.Max。

类型：Duration
