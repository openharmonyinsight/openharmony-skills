---
name: cangjie-network-socket
description: "仓颉 Socket 编程用法。"
---

# 仓颉语言 Socket 编程

## 1. 网络概述

### 1.1 分层
- **传输层**（`std.net` 包）：TCP（`TcpSocket`）、UDP（`UdpSocket`）、Unix Domain Socket
- **安全层**（`stdx.net.tls` 包）：TLS 1.2/1.3 加密传输

### 1.2 关键规则
- 网络操作在仓颉线程级别是**阻塞**的，但不阻塞 OS 线程（仓颉线程让出）
- 所有 Socket 均实现 `Resource`，可使用 `try-with-resource` 自动清理资源

### 1.3 地址类型
- `SocketAddress`（抽象基类）→ `IPSocketAddress`（IP+端口）、`UnixSocketAddress`（文件路径）
- `IPAddress`（抽象）→ `IPv4Address`、`IPv6Address`
  - `IPAddress.parse(str)` / `IPAddress.tryParse(str)` — 解析地址
  - `IPAddress.resolve(hostname)` — DNS 解析
  - 常用判断：`isLoopback()`、`isPrivate()`、`isMulticast()`

---

## 2. TCP 编程

### 2.1 服务端
- `TcpServerSocket(bindAt: port)` → `bind()` → `accept()`（阻塞等待连接）
- `accept(timeout)` — 带超时的接受连接
- 属性：`backlogSize`、`reuseAddress`、`reusePort`、`receiveBufferSize`、`sendBufferSize`

### 2.2 客户端
- `TcpSocket(host, port)` → `connect()` → `read()`/`write()`
- `connect(timeout)` — 带超时连接
- 超时配置：`readTimeout`、`writeTimeout`（`Duration` 类型）
- TCP 调优：`noDelay`（TCP_NODELAY）、`keepAlive`（`SocketKeepAliveConfig`）、`linger`

### 2.3 完整示例

```cangjie
import std.net.*
import std.sync.*

let SERVER_PORT: UInt16 = 33333
let ready = SyncCounter(1)

func runServer() {
    try (server = TcpServerSocket(bindAt: SERVER_PORT)) {
        server.bind()
        ready.dec()
        try (client = server.accept()) {
            let buf = Array<Byte>(10, repeat: 0)
            let n = client.read(buf)
            println("Server read ${n} bytes: ${buf}")
        }
    }
}

main(): Int64 {
    let fut = spawn { runServer() }
    ready.waitUntilZero()

    try (socket = TcpSocket("127.0.0.1", SERVER_PORT)) {
        socket.connect()
        socket.write([1, 2, 3])
    }
    fut.get()
    return 0
}
```

---

## 3. UDP 编程

- `UdpSocket(bindAt: port)` → `bind()`
- 发送：`sendTo(IPSocketAddress, data)` 或连接后 `send(data)`
- 接收：`receiveFrom(buffer)` → `(SocketAddress, count)`，或连接后 `receive(buffer)`
- 可选 `connect(addr)` 锁定远端地址（之后可用 `send`/`receive`）
- `disconnect()` — 解除连接
- **限制**：单包最大 64KB
- 超时：`receiveTimeout`、`sendTimeout`

```cangjie
import std.net.*
import std.sync.*
import std.time.*

let SERVER_PORT: UInt16 = 33333
let barrier = Barrier(2)

func runUdpServer() {
    try (server = UdpSocket(bindAt: SERVER_PORT)) {
        server.bind()
        barrier.wait()
        let buf = Array<Byte>(3, repeat: 0)
        let (addr, n) = server.receiveFrom(buf)
        println("Received ${n} bytes: ${buf}")
    }
}

main(): Int64 {
    let fut = spawn { runUdpServer() }
    barrier.wait()

    try (sock = UdpSocket(bindAt: 0)) {
        sock.sendTimeout = Duration.second * 2
        sock.bind()
        sock.sendTo(IPSocketAddress("127.0.0.1", SERVER_PORT), [1, 2, 3])
    }
    fut.get()
    return 0
}
```

---

## 4. Socket 选项

### 4.1 通用选项
| 属性 | 说明 |
|------|------|
| `readTimeout` / `writeTimeout` | 读写超时（`Duration` 类型），超时抛 `SocketTimeoutException` |
| `reuseAddress` / `reusePort` | 地址/端口复用 |
| `receiveBufferSize` / `sendBufferSize` | 收发缓冲区大小 |

### 4.2 TCP 专有
| 属性 | 说明 |
|------|------|
| `noDelay` | 禁用 Nagle 算法（降低延迟） |
| `keepAlive` | `SocketKeepAliveConfig(interval, count)` — TCP 保活配置 |
| `linger` | SO_LINGER — 关闭时等待数据发送完毕 |

### 4.3 底层选项访问
- `getSocketOptionIntNative(level, name)` / `setSocketOptionIntNative(level, name, value)`
- `OptionLevel`：`TCP`、`SOCKET` 等
- `SocketOptions`：`TCP_NODELAY`、`SO_KEEPALIVE`、`SO_REUSEADDR` 等常量

```cangjie
import std.net.*
import std.time.*

main() {
    try (sock = TcpSocket("127.0.0.1", 80)) {
        sock.readTimeout = Duration.second
        sock.noDelay = true
        sock.linger = Duration.minute
        sock.keepAlive = SocketKeepAliveConfig(
            interval: Duration.second * 7,
            count: 15
        )
    }
}
```

---

## 5. Unix Domain Socket

- 基于文件路径的进程间通信（IPC），不经过网络栈
- 路径最大 108 字节
- **不支持 Windows**
- 流式：`UnixServerSocket(bindAt: path)` + `UnixSocket(path)`
- 数据报式：`UnixDatagramSocket(bindAt: path)`
- 使用后需手动 `remove(path)` 清理 socket 文件

```cangjie
import std.net.*
import std.sync.*
import std.fs.*

let SOCK_PATH = "/tmp/cj_demo.sock"
let barrier = Barrier(2)

func runServer() {
    try (server = UnixServerSocket(bindAt: SOCK_PATH)) {
        server.bind()
        barrier.wait()
        try (client = server.accept()) {
            client.write("hello".toArray())
        }
    }
}

main(): Int64 {
    let fut = spawn { runServer() }
    barrier.wait()
    try (sock = UnixSocket(SOCK_PATH)) {
        sock.connect()
        let buf = Array<Byte>(5, repeat: 0)
        sock.read(buf)
        println(String.fromUtf8(buf))  // "hello"
    }
    fut.get()
    remove(SOCK_PATH)
    return 0
}
```

---

## 6. 异常类型

| 异常 | 说明 |
|------|------|
| `SocketException` | 通用 Socket 错误 |
| `SocketTimeoutException` | Socket 操作超时 |

---

## 7. 关键规则速查

1. 所有 Socket/Server 使用 `try-with-resource` 自动清理
2. TCP 服务端模式：`TcpServerSocket` → `bind()` → 循环 `accept()`
3. UDP 单包最大 64KB
4. TLS 需要先建立 TCP 连接，再在其上创建 `TlsSocket` 并 `handshake()`
