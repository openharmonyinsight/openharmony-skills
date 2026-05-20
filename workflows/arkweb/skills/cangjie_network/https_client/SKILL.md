---
name: cangjie-network-https-client
description: "仓颉 HTTPS 客户端编程用法。"
---

# 仓颉语言 HTTPS 客户端编程 Skill

## 1. 概述

- HTTPS = HTTP + TLS，在 HTTP 客户端基础上添加 TLS 加密层
- 依赖 `stdx.net.http` 和 `stdx.net.tls`，关于扩展标准库 `stdx` 的配置用法，请参阅 `cangjie-stdx` Skill
- 核心流程：配置 `TlsClientConfig` → 传入 `ClientBuilder.tlsConfig()` → 发送 HTTPS 请求

---

## 2. 快速入门（TrustAll 模式）

> **⚠️ 警告**：`TrustAll` 模式跳过证书验证，**仅限开发测试环境使用**，生产环境请使用 `Default` 或 `CustomCA` 模式。

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import std.io.StringReader

main() {
    // 1. 配置 TLS（跳过证书验证，仅测试用）
    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = TrustAll

    // 2. 构建 HTTPS 客户端
    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    // 3. 发送 HTTPS 请求
    let resp = client.get("https://127.0.0.1:8443/api")
    println("Status: ${resp.status}")
    println("Body: ${StringReader(resp.body).readToEnd()}")

    // 4. 关闭客户端
    client.close()
}
```

---

## 3. TlsClientConfig 配置详解

### 3.1 完整配置属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `verifyMode` | `CertificateVerifyMode` | `Default` | 证书验证模式 |
| `domain` | `?String` | `None` | 服务端主机名（SNI），通常自动从 URL 获取 |
| `alpnProtocolsList` | `Array<String>` | `[]` | ALPN 协议列表（设置 `["h2"]` 启用 HTTP/2） |
| `clientCertificate` | `?(X509Certificate, PrivateKey)` | `None` | 客户端证书和私钥（双向认证时使用） |
| `cipherSuitesV1_2` | `?Array<CipherSuite>` | `None` | TLS 1.2 密码套件 |
| `cipherSuitesV1_3` | `?Array<CipherSuite>` | `None` | TLS 1.3 密码套件 |
| `minVersion` | `TlsVersion` | `V1_2` | 最低 TLS 版本 |
| `maxVersion` | `TlsVersion` | `V1_3` | 最高 TLS 版本 |
| `securityLevel` | `Int32` | `2` | 安全级别（0-5） |
| `signatureAlgorithms` | `?Array<SignatureAlgorithm>` | `None` | 签名算法偏好 |
| `keylogCallback` | `?(String) -> Unit` | `None` | TLS 密钥日志回调（调试用） |

### 3.2 证书验证模式（CertificateVerifyMode）

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `Default` | 使用系统 CA 验证服务端证书 | **生产环境**（默认） |
| `CustomCA(certs)` | 使用自定义 CA 列表验证 | 自签名证书或私有 CA |
| `TrustAll` | 信任所有证书，不验证 | **仅限开发测试** |

---

## 4. 生产环境配置

### 4.1 使用系统 CA（Default 模式）

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import std.io.StringReader

main() {
    // Default 模式使用系统内置的 CA 证书验证服务端
    var tlsConfig = TlsClientConfig()
    // verifyMode 默认就是 Default，无需显式设置

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    let resp = client.get("https://www.example.com/api")
    println(StringReader(resp.body).readToEnd())

    client.close()
}
```

### 4.2 使用自定义 CA 证书（CustomCA 模式）

适用于自签名证书或内部私有 CA 的场景：

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.X509Certificate
import std.io.*
import std.fs.*

main() {
    // 加载自定义 CA 证书
    let caPem = String.fromUtf8(readToEnd(File("./ca.crt", Read)))
    let caCerts = X509Certificate.decodeFromPem(caPem)

    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = CustomCA(caCerts)

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    let resp = client.get("https://myserver.example.com/api")
    println(StringReader(resp.body).readToEnd())

    client.close()
}
```

---

## 5. 启用 HTTP/2

HTTP/2 需要 TLS + ALPN `h2` 配置。如果握手失败，自动回退 HTTP/1.1。

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import std.io.StringReader

main() {
    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = TrustAll
    // 设置 ALPN 协议协商 HTTP/2
    tlsConfig.alpnProtocolsList = ["h2"]

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    let resp = client.get("https://127.0.0.1:8443/api")
    println("Status: ${resp.status}")
    println("Body: ${StringReader(resp.body).readToEnd()}")

    client.close()
}
```

> **说明**：不支持通过 `Upgrade: h2c` 从 HTTP/1.1 升级到 HTTP/2。

---

## 6. 双向 TLS 认证（客户端证书）

当服务端要求客户端提供证书时，需配置客户端证书和私钥：

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}
import std.io.*
import std.fs.*

main() {
    // 加载 CA 证书（用于验证服务端）
    let caPem = String.fromUtf8(readToEnd(File("./ca.crt", Read)))
    let caCerts = X509Certificate.decodeFromPem(caPem)

    // 加载客户端证书和私钥
    let clientPem = String.fromUtf8(readToEnd(File("./client.crt", Read)))
    let clientKey = String.fromUtf8(readToEnd(File("./client.key", Read)))
    let clientCert = X509Certificate.decodeFromPem(clientPem)
    let clientPrivateKey = PrivateKey.decodeFromPem(clientKey)

    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = CustomCA(caCerts)
    // 设置客户端证书（双向认证）
    tlsConfig.clientCertificate = (clientCert, clientPrivateKey)

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    let resp = client.get("https://secure.example.com/api")
    println(StringReader(resp.body).readToEnd())

    client.close()
}
```

---

## 7. HTTP/2 Server Push 接收

当服务端使用 HTTP/2 Server Push 主动推送资源时，客户端可通过 `resp.getPush()` 获取推送的响应：

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.X509Certificate
import std.io.*
import std.fs.*
import std.collection.ArrayList

main() {
    let caPem = String.fromUtf8(readToEnd(File("./ca.crt", Read)))
    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = CustomCA(X509Certificate.decodeFromPem(caPem))
    tlsConfig.alpnProtocolsList = ["h2"]

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .enablePush(true)   // 启用接收服务端推送（默认 true）
        .build()

    // 发送主请求
    let resp = client.get("https://127.0.0.1:8443/index.html")
    println("Main response status: ${resp.status}")
    println("Main body: ${StringReader(resp.body).readToEnd()}")

    // 获取服务端推送的响应
    let pushResponses: Option<ArrayList<HttpResponse>> = resp.getPush()
    match (pushResponses) {
        case Some(pushList) =>
            for (pushResp in pushList) {
                println("Pushed resource status: ${pushResp.status}")
                println("Pushed body: ${StringReader(pushResp.body).readToEnd()}")
            }
        case None =>
            println("Server push not available")
    }

    client.close()
}
```

> **说明**：使用 `ClientBuilder().enablePush(false)` 可禁用接收服务端推送。

---

## 8. 自定义 TCP + TLS 连接

可以同时自定义 TCP 连接函数和 TLS 配置：

```cangjie
import std.net.{TcpSocket, SocketAddress}
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.X509Certificate
import std.io.*
import std.fs.*

main() {
    // TLS 配置
    let caPem = String.fromUtf8(readToEnd(File("./ca.crt", Read)))
    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = CustomCA(X509Certificate.decodeFromPem(caPem))
    tlsConfig.alpnProtocolsList = ["h2"]

    // 自定义 TCP 连接函数
    let customConnector = {
        sa: SocketAddress =>
        let socket = TcpSocket(sa)
        socket.connect()
        return socket
    }

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .connector(customConnector)
        .enablePush(false)
        .build()

    let resp = client.get("https://example.com/api")
    let buf = Array<UInt8>(1024, repeat: 0)
    let len = resp.body.read(buf)
    println(String.fromUtf8(buf.slice(0, len)))

    client.close()
}
```

---

## 9. 高级 TLS 配置

### 9.1 限制 TLS 版本

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import std.io.StringReader

main() {
    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = TrustAll
    // 仅允许 TLS 1.3
    tlsConfig.minVersion = V1_3
    tlsConfig.maxVersion = V1_3
    tlsConfig.alpnProtocolsList = ["h2"]

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    let resp = client.get("https://127.0.0.1:8443/api")
    println(StringReader(resp.body).readToEnd())

    client.close()
}
```

### 9.2 TLS 密钥日志（调试用）

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import std.io.StringReader

main() {
    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = TrustAll
    // 设置密钥日志回调（可用于 Wireshark 解密）
    tlsConfig.keylogCallback = { label, keylog => println("KEYLOG: ${keylog}") }

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    let resp = client.get("https://127.0.0.1:8443/api")
    println(StringReader(resp.body).readToEnd())

    client.close()
}
```

---

## 10. 异常类型

| 异常 | 说明 |
|------|------|
| `TlsException` | TLS 握手或通信异常（证书无效、OpenSSL 未安装等） |
| `HttpException` | HTTP 通用异常 |
| `ConnectionException` | TCP 连接异常 |
| `HttpTimeoutException` | 请求超时 |

> **注意**：如果未安装 OpenSSL 3 或安装了低版本，运行时会抛出 `TlsException: Can not load openssl library or function xxx`。

---

## 11. 关键规则速查

| 规则 | 说明 |
|------|------|
| 启用 HTTPS | `ClientBuilder().tlsConfig(tlsConfig)` |
| 系统 CA 验证 | `tlsConfig.verifyMode = Default`（默认值） |
| 自定义 CA | `tlsConfig.verifyMode = CustomCA(certs)` |
| 跳过验证（测试） | `tlsConfig.verifyMode = TrustAll`（**仅测试用**） |
| 启用 HTTP/2 | `tlsConfig.alpnProtocolsList = ["h2"]`；握手失败自动回退 HTTP/1.1 |
| 双向认证 | `tlsConfig.clientCertificate = (cert, privateKey)` |
| Server Push | `resp.getPush()` 获取推送响应；`enablePush(false)` 禁用 |
| TLS 版本限制 | `tlsConfig.minVersion` / `tlsConfig.maxVersion` |
| 密钥日志 | `tlsConfig.keylogCallback` 用于调试 |
| OpenSSL 依赖 | 需安装 OpenSSL 3，详见 `cangjie-tls` Skill |
| 释放连接 | body 读完后连接自动归还；使用完毕调用 `client.close()` |
