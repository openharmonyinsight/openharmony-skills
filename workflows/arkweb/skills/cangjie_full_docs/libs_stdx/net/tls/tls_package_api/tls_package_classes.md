# 类

## class TlsSessionContext

```cangjie
public class TlsSessionContext <: Equatable<TlsSessionContext> & ToString

```

功能：该类表示 TLS 会话上下文，给客户端提供信息，确保客户端所连接的服务端仍为相同实例，用于连接复用时，验证客户端合法性。

> **说明：**
>
> 当客户端尝试恢复会话时，双方都必须确保他们正在恢复与合法对端的会话。

父类型：

- Equatable\<[TlsSessionContext](#class-tlssessioncontext)>
- ToString

### static func fromName(String)

```cangjie
public static func fromName(name: String): TlsSessionContext
```

功能：通过名称创建 [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) 实例。

通过 [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) 保存的名称获取 [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) 对象。该名称用于区分 TLS 服务器，因此客户端依赖此名称来避免意外，尝试恢复与错误的服务器的连接。这里不一定使用加密安全名称，因为底层实现可以完成这项工作。从此函数返回的具有相同名称的两个 TlsSessionContext 可能不相等，并且不保证可替换。尽管它们是从相同的名称创建的，因此服务器实例应该在整个生命周期内创建一个 TlsSessionContext ，并且在每次 [TlsSocket](tls_package_classes.md#class-tlssocket).server() 调用中使用它。

参数：

- name: String - 会话上下文名称。

返回值：

- [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) - 会话上下文。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成会话上下文名称字符串。

返回值：

- String - [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext)（会话上下文名称字符串）。

### operator func !=(TlsSessionContext)

```cangjie
public override operator func !=(other: TlsSessionContext): Bool
```

功能：判断两 [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) 实例名称是否不同。

参数：

- other: [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) - 被比较的会话上下文对象。

返回值：

- Bool - 若 [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) 对象不同，返回 `true`；否则，返回 `false`。

### operator func ==(TlsSessionContext)

```cangjie
public override operator func ==(other: TlsSessionContext): Bool
```

功能：判断两 [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) 实例名称是否相同。

参数：

- other: [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) - 被比较的会话上下文对象。

返回值：

- Bool - 若 [TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) 对象相同，返回 `true`；否则，返回 `false`。

## class TlsSocket

```cangjie
public class TlsSocket <: StreamingSocket & ToString &Equatable<TlsSocket> & Hashable
```

功能：[TlsSocket](tls_package_classes.md#class-tlssocket) 用于在客户端及服务端间创建加密传输通道。

父类型：

- StreamingSocket
- Equatable\<[TlsSocket](#class-tlssocket)>
- Hashable
- ToString

### prop alpnProtocolName

```cangjie
public prop alpnProtocolName: ?String
```

功能：读取协商到的应用层协议名称。

类型：?String

异常：

- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当套接字未完成 TLS 握手或本端 TLS 套接字已关闭时，抛出异常。
- IllegalMemoryException - 当内存申请失败时，抛出异常。

### prop cipherSuite

```cangjie
public prop cipherSuite: CipherSuite
```

功能：握手后协商到的加密套。

> **说明：**
>
> 密码套件包含加密算法，用于消息认证的散列函数，密钥交换算法。

类型：[CipherSuite](tls_package_structs.md#struct-ciphersuite)

异常：

- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当套接字未完成 TLS 握手或本端 TLS 套接字已关闭时，抛出异常。

### prop clientCertificate

```cangjie
public prop clientCertificate: ?Array<X509Certificate>
```

功能：客户端提供的客户端证书。在客户端获取时为本端证书，在服务端获取时为对端证书。

> **注意：**
>
> 获取对端证书时，如果对端没有发送证书，该接口可能获取失败，返回 None，详见 [peerCertificate](./tls_package_classes.md#prop-peercertificate)。

类型：?Array<[X509Certificate](../../../crypto/x509/x509_package_api/x509_package_classes.md#class-x509certificate)>

异常：

- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当套接字未完成 TLS 握手或本端 TLS 套接字已关闭时，抛出异常。

### prop domain

```cangjie
public prop domain: ?String
```

功能：读取协商到的服务端主机名称。

异常：

- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当套接字未完成 TLS 握手或本端 TLS 套接字已关闭时，抛出异常。

类型：?String

### prop localAddress

```cangjie
public override prop localAddress: SocketAddress
```

功能：读取 [TlsSocket](tls_package_classes.md#class-tlssocket) 的本地地址。

类型：SocketAddress

异常：

- SocketException - 本端建连的底层 TCP 套接字关闭，抛出异常。
- [TlsException](tls_package_exceptions.md#class-tlsexception) - 本端配置为 TLS 的套接字已关闭时，抛出异常。

### prop peerCertificate

```cangjie
public prop peerCertificate: ?Array<X509Certificate>
```

功能：获取对端证书。在客户端获取时同 [serverCertificate](./tls_package_classes.md#prop-servercertificate)，在服务端获取时同 [clientCertificate](./tls_package_classes.md#prop-clientcertificate)。

> **注意：**
>
> - 如果握手时没有要求对端发送证书，此处将无法获取对端证书，返回 None。
>
> - 通过 session 机制恢复连接时，双方都不发送证书，该接口行为如下：
>
>     - 在服务端，如果被恢复的原始连接建立时获取了对端证书，服务端将缓存对端证书，并在此处获取到缓存的证书；
>     - 在客户端，不缓存原始连接的对端证书，此处将无法获取对端证书，返回 None。

类型：?Array<[X509Certificate](../../../crypto/x509/x509_package_api/x509_package_classes.md#class-x509certificate)>

异常：

- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当套接字未完成 TLS 握手或本端 TLS 套接字已关闭时，抛出异常。

### prop readTimeout

```cangjie
public override mut prop readTimeout: ?Duration
```

功能：读写 [TlsSocket](tls_package_classes.md#class-tlssocket) 的读超时时间。

类型：?Duration

异常：

- SocketException - 本端建连的底层 TCP 套接字关闭，抛出异常。
- [TlsException](tls_package_exceptions.md#class-tlsexception) - 本端配置为 TLS 的套接字已关闭时，抛出异常。
- IllegalArgumentException - 设定的读超时时间为负值时，抛出异常。

### prop remoteAddress

```cangjie
public override prop remoteAddress: SocketAddress
```

功能：读取 [TlsSocket](tls_package_classes.md#class-tlssocket) 的远端地址。

类型：SocketAddress

异常：

- SocketException - 本端建连的底层 TCP 套接字关闭，抛出异常。
- [TlsException](tls_package_exceptions.md#class-tlsexception) - 本端配置为 TLS 的套接字已关闭时，抛出异常。

### prop serverCertificate

```cangjie
public prop serverCertificate: Array<X509Certificate>
```

功能：服务器证书链由服务器提供或在服务器配置中预先配置。在服务端获取时为本端证书，在客户端获取时为对端证书。

>**注意：**
>
> 获取对端证书时，如果对端没有发送证书，该接口可能获取失败，返回 None，详见 [peerCertificate](./tls_package_classes.md#prop-peercertificate)。

类型：Array<[X509Certificate](../../../crypto/x509/x509_package_api/x509_package_classes.md#class-x509certificate)>

异常：

- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当套接字未完成 TLS 握手或本端 TLS 套接字已关闭时，抛出异常。

### prop session

```cangjie
public prop session: ?TlsSession
```

功能：读取 TLS 会话 id ，客户端会在握手成功后捕获当前会话的 id ，可使用该 id 重用该会话，省去 TLS 建立连接的时间。连接建立未成功时，返回 None。

>**说明：**
>
> 服务端不做捕获因此始终为 None。

类型：?[TlsSession](tls_package_structs.md#struct-tlssession)

异常：

- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当套接字未完成 TLS 握手，抛出异常。

### prop socket

```cangjie
public prop socket: StreamingSocket
```

功能：[TlsSocket](tls_package_classes.md#class-tlssocket) 创建所使用的 StreamingSocket。

类型：StreamingSocket

异常：

- [TlsException](tls_package_exceptions.md#class-tlsexception) - 本端配置为 TLS 套接字已关闭时，抛出异常。

### prop tlsVersion

```cangjie
public prop tlsVersion: TlsVersion
```

功能：读取协商到的 TLS 版本。

类型：[TlsVersion](tls_package_enums.md#enum-tlsversion)

异常：

- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当套接字未完成 TLS 握手或本端 TLS 套接字已关闭时，抛出异常。

### prop writeTimeout

```cangjie
public override mut prop writeTimeout: ?Duration
```

功能：读写 [TlsSocket](tls_package_classes.md#class-tlssocket) 的写超时时间。

类型：?Duration

异常：

- SocketException - 本端建连的底层 TCP 套接字关闭，抛出异常。
- [TlsException](tls_package_exceptions.md#class-tlsexception) - 本端配置为 TLS 的套接字已关闭时，抛出异常。
- IllegalArgumentException - 设定的写超时时间为负值时，抛出异常。

### static func client(StreamingSocket, ?TlsSession, TlsClientConfig)

```cangjie
public static func client(
    socket: StreamingSocket,
    session!: ?TlsSession = None,
    clientConfig!: TlsClientConfig = TlsClientConfig()
): TlsSocket
```

功能：根据传入的 StreamingSocket 实例创建指定地址的客户端 TLS 套接字，该套接字可用于客户端 TLS 握手及会话。

参数：

- socket: StreamingSocket - 已连接到服务端的客户端 TCP 套接字。
- session!: ?[TlsSession](tls_package_structs.md#struct-tlssession) - TLS 会话 id，若存在可用的 TLS 会话， 则可通过该 id 恢复历史 TLS 会话，省去 TLS 建立连接时间，但使用该会话依然可能协商失败。默认为 `None`。
- clientConfig!: [TlsClientConfig](tls_package_structs.md#struct-tlsclientconfig) - 客户端配置，默认为 [TlsClientConfig](tls_package_structs.md#struct-tlsclientconfig)()。

返回值：

- [TlsSocket](tls_package_classes.md#class-tlssocket) - 构造出的 [TlsSocket](tls_package_classes.md#class-tlssocket) 实例。

### static func server(StreamingSocket, ?TlsSessionContext, TlsServerConfig)

```cangjie
public static func server(
    socket: StreamingSocket,
    sessionContext!: ?TlsSessionContext = None,
    serverConfig!: TlsServerConfig
): TlsSocket
```

功能：根据传入的 StreamingSocket 实例创建指定地址的服务端 TLS 套接字，该套接字可用于服务端 TLS 握手及会话。

参数：

- socket: StreamingSocket - TCP 连接建立完成后接受到套接字。
- sessionContext!: ?[TlsSessionContext](tls_package_classes.md#class-tlssessioncontext) - TLS 会话 id， 若存在可用的 TLS 会话， 则可通过该 id 恢复历史 TLS 会话，省去 TLS 建立连接时间，但使用该会话依然可能协商失败。默认为 None。
- serverConfig!: [TlsServerConfig](tls_package_structs.md#struct-tlsserverconfig) - 服务端配置，默认为 [TlsServerConfig](tls_package_structs.md#struct-tlsserverconfig)()。

返回值：

- [TlsSocket](tls_package_classes.md#class-tlssocket) - 构造出的 [TlsSocket](tls_package_classes.md#class-tlssocket) 实例。

### func close()

```cangjie
public func close(): Unit
```

功能：关闭套接字。

异常：

- SocketException - 底层连接无法关闭时，抛出异常。

### func handshake(?Duration)

```cangjie
public func handshake(timeout!: ?Duration = None): Unit
```

功能：TLS 握手。不支持重新协商握手，因此只能被调用一次。调用对象可以为客户端或者服务端的 [TlsSocket](tls_package_classes.md#class-tlssocket)。

参数：

- timeout!: ?Duration - 握手超时时间，默认为 None 不对超时时间进行设置，此时采用默认 30s 的超时时间。

异常：

- SocketException - 本端建连的底层 TCP 套接字关闭，抛出异常。
- SocketTimeoutException - 底层 TCP 套接字连接超时时，抛出异常。
- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当握手已经开始或者已经结束，抛出异常；或当握手阶段出现系统错误时，抛出异常。
- IllegalArgumentException - 设定的握手超时时间为负值时，抛出异常。

### func hashCode()

```cangjie
public override func hashCode(): Int64
```

功能：返回 TLS 套接字对象的哈希值。

返回值：

- Int64 - 对 TLS 套接字对象进行哈希计算后得到的结果。

### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：返回套接字是否关闭的状态。

返回值：

- Bool - 连接断开返回 true；否则，返回 false。

### func read(Array\<Byte>)

```cangjie
public override func read(buffer: Array<Byte>): Int64
```

功能：[TlsSocket](tls_package_classes.md#class-tlssocket) 读取数据。

参数：

- buffer: Array\<Byte> - 存储读取到的数据内容的数组。

返回值：

- Int64 - 读取到的数据内容字节数。

异常：

- SocketException - 本端建连的底层 TCP 套接字关闭，抛出异常。
- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当 `buffer` 为空，或者 [TlsSocket](tls_package_classes.md#class-tlssocket) 未连接，或读取数据出现系统错误等。

### func toString()

```cangjie
public func toString(): String
```

功能：套接字的字符串表示，字符串内容为当前套接字状态。

> **说明：**
>
> 例如：当前套接字处于可开始进行握手状态时，该接口将返回字符串 "[TlsSocket](tls_package_classes.md#class-tlssocket)(TcpSocket(\${本端地址} -> \${对端地址}), ready for handshake)"

返回值：

- String - 该 TLS 连接字符串。

### func write(Array\<Byte>)

```cangjie
public func write(buffer: Array<Byte>): Unit
```

功能：[TlsSocket](tls_package_classes.md#class-tlssocket) 发送数据。

参数：

- buffer: Array\<Byte> - 存储将要发送的数据内容数组。

异常：

- SocketException - 本端建连的底层 TCP 套接字关闭，抛出异常。
- [TlsException](tls_package_exceptions.md#class-tlsexception) - 当套接字已关闭，或者 [TlsSocket](tls_package_classes.md#class-tlssocket) 未连接，或写入数据出现系统错误等。

### operator func !=(TlsSocket)

```cangjie
public override operator func !=(other: TlsSocket): Bool
```

功能：判断两 [TlsSocket](tls_package_classes.md#class-tlssocket) 是否引用不同实例。

参数：

- other: [TlsSocket](tls_package_classes.md#class-tlssocket) - 对比的 TLS 套接字。

返回值：

- Bool - 对比的套接字不同返回 `true`；否则，返回 `false`。

### operator func ==(TlsSocket)

```cangjie
public override operator func ==(other: TlsSocket): Bool
```

功能：判断两 [TlsSocket](tls_package_classes.md#class-tlssocket) 是否引用同一实例。

参数：

- other: [TlsSocket](tls_package_classes.md#class-tlssocket) - 对比的 TLS 套接字。

返回值：

- Bool - 对比的套接字相同返回 `true`；否则，返回 `false`。
