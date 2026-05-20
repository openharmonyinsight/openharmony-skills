---
name: cangjie-network-https-server
description: "仓颉 HTTPS 服务端编程用法。"
---

# 仓颉语言 HTTPS 服务端编程 Skill

## 1. 概述

- HTTPS = HTTP + TLS，在 HTTP 服务端基础上添加 TLS 加密层
- 依赖 `stdx.net.http` 和 `stdx.net.tls`，关于扩展标准库 `stdx` 的配置用法，请参阅 `cangjie-stdx` Skill
- 核心流程：加载证书/私钥 → 配置 `TlsServerConfig` → 传入 `ServerBuilder.tlsConfig()` → 启动 HTTPS 服务

---

## 2. 快速入门

```cangjie
import std.io.*
import std.fs.*
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}

main() {
    // 1. 加载证书和私钥
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let key = String.fromUtf8(readToEnd(File("./server.key", Read)))

    // 2. 配置 TLS
    var tlsConfig = TlsServerConfig(
        X509Certificate.decodeFromPem(pem),
        PrivateKey.decodeFromPem(key)
    )

    // 3. 构建并启动 HTTPS 服务
    let server = ServerBuilder()
        .addr("127.0.0.1")
        .port(8443)
        .tlsConfig(tlsConfig)
        .build()

    server.distributor.register("/", {
        ctx => ctx.responseBuilder.body("Hello HTTPS!")
    })
    server.serve()
}
```

---

## 3. TlsServerConfig 配置详解

### 3.1 构造函数

```cangjie
TlsServerConfig(certificate: X509Certificate, privateKey: PrivateKey)
```

必须提供服务端证书链和对应私钥。

### 3.2 完整配置属性

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `supportedAlpnProtocols` | `Array<String>` | `[]` | 支持的 ALPN 协议（设置 `["h2"]` 启用 HTTP/2） |
| `clientIdentityRequired` | `TlsClientIdentificationMode` | `Disabled` | 客户端证书认证模式 |
| `verifyMode` | `CertificateVerifyMode` | `Default` | 证书验证模式（双向认证时验证客户端证书） |
| `cipherSuitesV1_2` | `?Array<CipherSuite>` | `None` | TLS 1.2 密码套件 |
| `cipherSuitesV1_3` | `?Array<CipherSuite>` | `None` | TLS 1.3 密码套件 |
| `minVersion` | `TlsVersion` | `V1_2` | 最低 TLS 版本 |
| `maxVersion` | `TlsVersion` | `V1_3` | 最高 TLS 版本 |
| `securityLevel` | `Int32` | `2` | 安全级别（0-5） |
| `dhParameters` | `?DhParameters` | `None` | DH 密钥交换参数 |

### 3.3 证书验证模式（CertificateVerifyMode）

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `Default` | 使用系统 CA 验证 | 验证客户端证书（默认） |
| `CustomCA(certs)` | 使用自定义 CA 列表验证 | 自签名客户端证书 |
| `TrustAll` | 信任所有证书 | **仅限开发测试** |

### 3.4 客户端认证模式（TlsClientIdentificationMode）

| 模式 | 说明 |
|------|------|
| `Disabled` | 不要求客户端证书（单向认证，默认） |
| `Optional` | 客户端可选提供证书 |
| `Required` | 客户端必须提供证书（双向认证/mTLS） |

---

## 4. 启用 HTTP/2

HTTP/2 需要 TLS + ALPN `h2` 配置。如果握手失败，自动回退 HTTP/1.1。

```cangjie
import std.io.*
import std.fs.*
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}

main() {
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let key = String.fromUtf8(readToEnd(File("./server.key", Read)))
    var tlsConfig = TlsServerConfig(
        X509Certificate.decodeFromPem(pem),
        PrivateKey.decodeFromPem(key)
    )
    // 设置 ALPN 协议启用 HTTP/2
    tlsConfig.supportedAlpnProtocols = ["h2"]

    let server = ServerBuilder()
        .addr("127.0.0.1")
        .port(8443)
        .tlsConfig(tlsConfig)
        // HTTP/2 专用配置
        .headerTableSize(10 * 1024)
        .maxConcurrentStreams(100)
        .build()

    server.distributor.register("/", {
        ctx => ctx.responseBuilder.body("HTTP/2 over HTTPS!")
    })
    server.serve()
}
```

> **说明**：使用 `["http/1.1"]` 仅启用 HTTPS 而不启用 HTTP/2。不支持通过 `Upgrade: h2c` 从 HTTP/1.1 升级到 HTTP/2。

---

## 5. 证书热更新

运行时无需重启服务即可更新 TLS 证书，更新后新建连接将使用新证书：

```cangjie
import std.io.*
import std.fs.*
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}

main() {
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let key = String.fromUtf8(readToEnd(File("./server.key", Read)))
    var tlsConfig = TlsServerConfig(
        X509Certificate.decodeFromPem(pem),
        PrivateKey.decodeFromPem(key)
    )
    tlsConfig.supportedAlpnProtocols = ["h2"]

    let server = ServerBuilder()
        .addr("127.0.0.1")
        .port(8443)
        .tlsConfig(tlsConfig)
        .build()

    server.distributor.register("/", {
        ctx => ctx.responseBuilder.body("HTTPS!")
    })

    // 后台启动服务
    spawn { server.serve() }

    // 热更新证书和私钥（通过文件路径）
    server.updateCert("./new_server.crt", "./new_server.key")

    // 热更新 CA（双向认证场景，通过文件路径）
    server.updateCA("./new_ca.crt")
}
```

### 5.1 Server 证书热更新接口

| 方法 | 签名 | 说明 |
|------|------|------|
| `updateCert` | `updateCert(String, String): Unit` | 通过文件路径更新证书和私钥 |
| `updateCert` | `updateCert(Array<X509Certificate>, PrivateKey): Unit` | 通过对象更新证书和私钥 |
| `updateCA` | `updateCA(String): Unit` | 通过文件路径更新 CA 证书 |
| `updateCA` | `updateCA(Array<X509Certificate>): Unit` | 通过对象更新 CA 证书 |

---

## 6. 双向 TLS 认证（mTLS）

双向认证要求客户端也提供证书，服务端验证客户端身份：

```cangjie
import std.io.*
import std.fs.*
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}

main() {
    // 加载服务端证书和私钥
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let key = String.fromUtf8(readToEnd(File("./server.key", Read)))
    // 加载用于验证客户端证书的 CA
    let caPem = String.fromUtf8(readToEnd(File("./ca.crt", Read)))

    var tlsConfig = TlsServerConfig(
        X509Certificate.decodeFromPem(pem),
        PrivateKey.decodeFromPem(key)
    )
    // 要求客户端提供证书（Required = 必须提供，Optional = 可选提供）
    tlsConfig.clientIdentityRequired = Required
    // 使用自定义 CA 验证客户端证书
    tlsConfig.verifyMode = CustomCA(X509Certificate.decodeFromPem(caPem))

    let server = ServerBuilder()
        .addr("127.0.0.1")
        .port(8443)
        .tlsConfig(tlsConfig)
        .build()

    server.distributor.register("/secure", {
        ctx =>
        // 在 handler 中获取客户端证书信息
        let clientCert = ctx.clientCertificate
        match (clientCert) {
            case Some(certs) =>
                ctx.responseBuilder.body("mTLS OK, client cert count: ${certs.size}")
            case None =>
                ctx.responseBuilder.status(401).body("No client certificate")
        }
    })

    server.serve()
}
```

---

## 7. HTTP/2 Server Push

仅用于 HTTP/2 协议（需 TLS + ALPN `h2`），允许服务端主动推送关联资源给客户端：

```cangjie
import std.io.*
import std.fs.*
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}

main() {
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let key = String.fromUtf8(readToEnd(File("./server.key", Read)))
    var tlsConfig = TlsServerConfig(
        X509Certificate.decodeFromPem(pem),
        PrivateKey.decodeFromPem(key)
    )
    tlsConfig.supportedAlpnProtocols = ["h2"]

    let server = ServerBuilder()
        .addr("127.0.0.1")
        .port(8443)
        .tlsConfig(tlsConfig)
        .build()

    // 主请求 handler：主动推送关联资源
    server.distributor.register("/index.html", {
        ctx =>
        let pusher = HttpResponsePusher.getPusher(ctx)
        match (pusher) {
            case Some(p) =>
                // 推送 CSS 和 JS 资源
                p.push("/style.css", "GET", ctx.request.headers)
                p.push("/app.js", "GET", ctx.request.headers)
            case None => ()  // 非 HTTP/2 或推送被禁用
        }
        ctx.responseBuilder.body("<html><head><link rel='stylesheet' href='/style.css'><script src='/app.js'></script></head></html>")
    })

    // 被推送资源的 handler
    server.distributor.register("/style.css", {
        ctx =>
        ctx.responseBuilder
            .header("Content-Type", "text/css")
            .body("body { font-family: sans-serif; }")
    })
    server.distributor.register("/app.js", {
        ctx =>
        ctx.responseBuilder
            .header("Content-Type", "application/javascript")
            .body("console.log('loaded');")
    })

    server.serve()
}
```

---

## 8. 高级 TLS 配置

### 8.1 限制 TLS 版本

```cangjie
import std.io.*
import std.fs.*
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}

main() {
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let key = String.fromUtf8(readToEnd(File("./server.key", Read)))
    var tlsConfig = TlsServerConfig(
        X509Certificate.decodeFromPem(pem),
        PrivateKey.decodeFromPem(key)
    )
    // 仅允许 TLS 1.3
    tlsConfig.minVersion = V1_3
    tlsConfig.maxVersion = V1_3
    tlsConfig.supportedAlpnProtocols = ["h2"]

    let server = ServerBuilder()
        .addr("127.0.0.1")
        .port(8443)
        .tlsConfig(tlsConfig)
        .build()

    server.distributor.register("/", {
        ctx => ctx.responseBuilder.body("TLS 1.3 only!")
    })
    server.serve()
}
```

### 8.2 完整网络配置（TLS + TCP）

```cangjie
import std.io.*
import std.fs.*
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}

main() {
    // TCP 传输层配置
    var transportCfg = TransportConfig()
    transportCfg.readBufferSize = 8192

    // TLS 配置
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let key = String.fromUtf8(readToEnd(File("./server.key", Read)))
    var tlsConfig = TlsServerConfig(
        X509Certificate.decodeFromPem(pem),
        PrivateKey.decodeFromPem(key)
    )
    tlsConfig.supportedAlpnProtocols = ["h2"]

    let server = ServerBuilder()
        .addr("127.0.0.1")
        .port(8443)
        .transportConfig(transportCfg)
        .tlsConfig(tlsConfig)
        .headerTableSize(10 * 1024)
        .maxRequestHeaderSize(1024 * 1024)
        .build()

    server.distributor.register("/", {
        ctx => ctx.responseBuilder.body("HTTPS with custom config!")
    })
    server.serve()
}
```

---

## 9. 异常类型

| 异常 | 说明 |
|------|------|
| `TlsException` | TLS 握手或通信异常（证书无效、OpenSSL 未安装等） |
| `HttpException` | HTTP 通用异常 |
| `ConnectionException` | TCP 连接异常 |

> **注意**：如果未安装 OpenSSL 3 或安装了低版本，运行时会抛出 `TlsException: Can not load openssl library or function xxx`。

---

## 10. 关键规则速查

| 规则 | 说明 |
|------|------|
| 证书加载 | `X509Certificate.decodeFromPem(pemString)` 和 `PrivateKey.decodeFromPem(keyString)` |
| 启用 HTTPS | `ServerBuilder().tlsConfig(tlsConfig)` |
| 启用 HTTP/2 | `tlsConfig.supportedAlpnProtocols = ["h2"]`；握手失败自动回退 HTTP/1.1 |
| 仅 HTTPS | `tlsConfig.supportedAlpnProtocols = ["http/1.1"]` |
| 证书热更新 | `server.updateCert(certPath, keyPath)` / `server.updateCA(caPath)` |
| 双向认证 | `tlsConfig.clientIdentityRequired = Required` + `tlsConfig.verifyMode = CustomCA(caCerts)` |
| 获取客户端证书 | Handler 中通过 `ctx.clientCertificate` 获取 |
| Server Push | `HttpResponsePusher.getPusher(ctx)` 获取推送器，仅 HTTP/2 可用 |
| TLS 版本限制 | `tlsConfig.minVersion` / `tlsConfig.maxVersion` |
| OpenSSL 依赖 | 需安装 OpenSSL 3，详见 `cangjie-tls` Skill |
