# 接口

## interface DatagramSocket

```cangjie
public interface DatagramSocket <: Resource & ToString {
    prop localAddress: SocketAddress
    prop remoteAddress: ?SocketAddress
    mut prop receiveTimeout: ?Duration
    mut prop sendTimeout: ?Duration
    func receiveFrom(buffer: Array<Byte>): (SocketAddress, Int64)
    func sendTo(address: SocketAddress, payload: Array<Byte>): Unit
}
```

功能：[DatagramSocket](net_package_interfaces.md#interface-datagramsocket) 是一种接收和读取数据包的套接字。

一个数据包通常有有限的大小，可能为空。不同的数据包套接字类型有不同的数据包最大值。例如 `UDP` 套接字一次可以处理最大 64KB 的数据包。
数据包传输不是一种可靠的传输，不保证传输顺序。数据包大小在发送端决定，例如：一端发送了 10 字节和 15 字节的报文，对端将收到相同大小的对应报文，10 字节和 15 字节。

父类型：

- [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop localAddress

```cangjie
prop localAddress: SocketAddress
```

功能：读取 `Socket` 将要或已经被绑定的本地地址。

类型：[SocketAddress](net_package_classes.md#class-socketaddress)

异常：

- [SocketException](net_package_exceptions.md#class-socketexception) - 当 `Socket` 已经被关闭或无可用的本地地址（本地地址未配置并且套接字未连接）时，抛出异常。

### prop receiveTimeout

```cangjie
mut prop receiveTimeout: ?Duration
```

功能：设置和读取 `receiveFrom` 超时时间，无超时时间设置为 `None`。

如果设置的时间过小将会设置为最小时钟周期值；过大时将设置为最大超时时间（2<sup>63</sup>-1 纳秒）；默认值为 `None`。

类型：?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当超时时间小于 0 时，抛出异常。

### prop remoteAddress

```cangjie
prop remoteAddress: ?SocketAddress
```

功能：读取 `Socket` 已经连接的远端地址，当 `Socket` 未连接时返回 None。

类型：?[SocketAddress](net_package_classes.md#class-socketaddress)

异常：

- [SocketException](net_package_exceptions.md#class-socketexception) - 当 `Socket` 已经被关闭时，抛出异常。

### prop sendTimeout

```cangjie
mut prop sendTimeout: ?Duration
```

功能：设置和读取 `sendTo` 超时时间，默认设置为 `None`。

如果设置的时间过小将会设置为最小时钟周期值；过大时将设置为最大超时时间（2<sup>63</sup>-1 纳秒）；默认值为 `None`。

类型：?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当超时时间小于 0 时，抛出异常。

### func receiveFrom(Array\<Byte>)

```cangjie
func receiveFrom(buffer: Array<Byte>): (SocketAddress, Int64)
```

功能：阻塞式等待收取报文到 `buffer` 中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 存储报文内容的缓存空间，`buffer` 应当有一个合适的大小，否则可能导致收取报文时报文被截断，并且返回的报文大小值大于 `buffer` 的大小。

返回值：

- ([SocketAddress](net_package_classes.md#class-socketaddress), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 报文发送地址和收取到的报文大小（可能为 0，或大于参数 `buffer` 大小）。

异常：

- [SocketException](net_package_exceptions.md#class-socketexception) - 当本机缓存过小无法读取报文时，抛出异常。
- [SocketTimeoutException](net_package_exceptions.md#class-sockettimeoutexception) - 当读取超时时，抛出异常。

### func sendTo(SocketAddress, Array\<Byte>)

```cangjie
func sendTo(address: SocketAddress, payload: Array<Byte>): Unit
```

功能：发送报文到指定的远端地址，当对端无足够缓存时，此操作可能被阻塞，报文可能被丢弃。

参数：

- address: [SocketAddress](net_package_classes.md#class-socketaddress) - 需要发送到的远端地址。
- payload: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 需要发送的报文内容。

## interface ServerSocket

```cangjie
public interface ServerSocket <: Resource & ToString {
    prop localAddress: SocketAddress
    func accept(): StreamingSocket
    func accept(timeout!: ?Duration): StreamingSocket
    func bind(): Unit
}
```

功能：提供服务端的 `Socket` 需要的接口。

父类型：

- [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop localAddress

```cangjie
prop localAddress: SocketAddress
```

功能：读取 `Socket` 将要或已经被绑定的本地地址。

类型：[SocketAddress](net_package_classes.md#class-socketaddress)

异常：

- [SocketException](net_package_exceptions.md#class-socketexception) - 当 `Socket` 已经被关闭时，抛出异常。

### func accept()

```cangjie
func accept(): StreamingSocket
```

功能：接受一个客户端套接字的连接请求，阻塞式等待连接请求。

返回值：

- [StreamingSocket](net_package_interfaces.md#interface-streamingsocket) - 连接成功的客户端套接字。

### func accept(?Duration)

```cangjie
func accept(timeout!: ?Duration): StreamingSocket
```

功能：接受一个客户端套接字的连接请求，阻塞式等待连接请求。

参数：

- timeout!: ?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 等待连接超时的时间。

返回值：

- [StreamingSocket](net_package_interfaces.md#interface-streamingsocket) - 连接成功的客户端套接字。

异常：

- [SocketTimeoutException](net_package_exceptions.md#class-sockettimeoutexception) - 当等待连接请求超时，抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当超时时间小于 0 时，抛出异常。

### func bind()

```cangjie
func bind(): Unit
```

功能：绑定套接字。

当没有设置 `reuse` 属性，本地端口、地址、文件路径已被占用或者上次绑定套接字的连接失败后需要 `close` 套接字。不支持多次重试此操作后可执行 `accept()` 操作。

异常：

- [SocketException](net_package_exceptions.md#class-socketexception) - 当因系统原因绑定失败时，抛出异常。

## interface StreamingSocket

```cangjie
public interface StreamingSocket <: IOStream & Resource & ToString {
    prop localAddress: SocketAddress
    prop remoteAddress: SocketAddress
    mut prop readTimeout: ?Duration
    mut prop writeTimeout: ?Duration
}
```

功能：双工流模式下的运行的 `Socket`，可被读写。

[StreamingSocket](net_package_interfaces.md#interface-streamingsocket) 可以被绑定 (`bind`) 和连接 (`connect`)，用户可以通过属性设置绑定和连接的远端和本地地址。
[StreamingSocket](net_package_interfaces.md#interface-streamingsocket) 可以有序分包传输字节流。我们会使用一段缓存空间存储读写的字节流。读取接口 (`read()`) 默认在无数据到来时阻塞式等待，直到下一次数据到达或超时。写操作 (`write()`) 会写入缓存中的数据并在后续被发出，如果缓存不足，或者写入速度快于转发速度，写操作将会阻塞等待缓存空闲，或超时。
读写字符始终保持有序，但不保证传输过程中的分包策略及大小与发包时一致。例如：一端发送 10 字节报文后，又发送了 15 字节报文，对端可能分别收到 10 字节 和 15 字节报文，也可能一次性收到 25 字节的一个报文。
当收到一段异常报文时，将返回报文长度为 -1 。

父类型：

- [IOStream](../../io/io_package_api/io_package_interfaces.md#interface-iostream)
- [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop localAddress

```cangjie
prop localAddress: SocketAddress
```

功能：读取 `Socket` 将要或已经被绑定的本地地址。

类型：[SocketAddress](net_package_classes.md#class-socketaddress)

异常：

- [SocketException](net_package_exceptions.md#class-socketexception) - 当 `Socket` 已经被关闭或无可用的本地地址（本地地址未配置并且套接字未连接）时，抛出异常。

### prop readTimeout

```cangjie
mut prop readTimeout: ?Duration
```

功能：设置和读取读超时时间。

如果设置的时间过小将会设置为最小时钟周期值；过大时将设置为最大超时时间（2<sup>63</sup>-1 纳秒）；默认值为 `None`。

类型：?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当超时时间小于 0 时，抛出异常。

### prop remoteAddress

```cangjie
prop remoteAddress: SocketAddress
```

功能：读取 `Socket` 将要或已经连接的远端地址。

类型：[SocketAddress](net_package_classes.md#class-socketaddress)

异常：

- [SocketException](net_package_exceptions.md#class-socketexception) - 当 `Socket` 已经被关闭时，抛出异常。

### prop writeTimeout

```cangjie
mut prop writeTimeout: ?Duration
```

功能：设置和读取写超时时间。

如果设置的时间过小将会设置为最小时钟周期值；过大时将设置为最大超时时间（2<sup>63</sup>-1 纳秒）；默认值为 `None`。

类型：?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当超时时间小于 0 时，抛出异常。
