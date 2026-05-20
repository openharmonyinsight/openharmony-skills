---
name: cangjie-network-tls-build
description: "仓颉 TLS 构建与证书配置说明。"
---

# 仓颉 TLS 项目编译构建指南

## 1. 概述

使用 `stdx.net.tls`（以及 `stdx.crypto.*` 和涉及 https 的 `stdx.net.http`）需要：

1. **安装 OpenSSL 3** — 提供 `ssl` 和 `crypto` 动态库
2. **下载 stdx** — 从 <https://gitcode.com/Cangjie/cangjie_stdx/releases> 下载对应平台的扩展标准库
3. **配置 cjpm.toml** — 通过 `bin-dependencies` 引用 stdx 库

> 关于 stdx 的下载安装和通用配置，请参阅 `cangjie-stdx-config` Skill。
> 关于 TLS API 用法，请参阅 `cangjie-tls` Skill。

---

## 2. OpenSSL 3 安装

### 2.1 Linux

**方式一：包管理器安装（推荐）**

```bash
# Ubuntu 22.04+ / Debian
sudo apt install libssl-dev

# CentOS / RHEL
sudo dnf install openssl-devel
```

确保系统安装目录下存在以下动态库文件：
- `libssl.so`、`libssl.so.3`
- `libcrypto.so`、`libcrypto.so.3`

**方式二：源码编译安装**

下载 OpenSSL 3.x.x 源码编译安装，确保安装目录下包含上述动态库文件。

- 如果安装在自定义目录，将库文件所在目录添加到环境变量：

```bash
export LD_LIBRARY_PATH=/path/to/openssl/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/to/openssl/lib:$LIBRARY_PATH
```

### 2.2 macOS

**方式一：Homebrew 安装（推荐）**

```bash
brew install openssl@3
```

确保系统安装目录下存在 `libssl.dylib`、`libssl.3.dylib`、`libcrypto.dylib` 和 `libcrypto.3.dylib`。

**方式二：源码编译安装**

下载 OpenSSL 3.x.x 源码编译安装，如果安装在自定义目录：

```bash
export DYLD_LIBRARY_PATH=/path/to/openssl/lib:$DYLD_LIBRARY_PATH
export LIBRARY_PATH=/path/to/openssl/lib:$LIBRARY_PATH
```

### 2.3 Windows

1. 从源码编译安装 OpenSSL 3.x.x（x64 架构），或下载第三方预编译的 OpenSSL 3.x.x 开发包
2. 确保安装目录下包含以下库文件：
   - `libssl.dll.a`（或 `libssl.lib`）、`libssl-3-x64.dll`
   - `libcrypto.dll.a`（或 `libcrypto.lib`）、`libcrypto-3-x64.dll`
3. 配置环境变量：
   - 将 `.dll.a`（或 `.lib`）文件所在目录添加到 `LIBRARY_PATH`
   - 将 `.dll` 文件所在目录添加到 `PATH`

### 2.4 验证安装

```bash
openssl version
# 应输出 OpenSSL 3.x.x
```

---

## 3. cjpm.toml 配置

### 3.1 动态库配置（推荐开发阶段使用）

**Linux x86_64**：

```toml
[package]
  name = "my-tls-app"
  version = "1.0.0"
  output-type = "executable"

[dependencies]

[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

**Linux aarch64**：

```toml
[target.aarch64-unknown-linux-gnu]
  [target.aarch64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

**macOS aarch64**：

```toml
[target.aarch64-apple-darwin]
  [target.aarch64-apple-darwin.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

**macOS x86_64**：

```toml
[target.x86_64-apple-darwin]
  [target.x86_64-apple-darwin.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

**Windows x86_64**：

```toml
[target.x86_64-w64-mingw32]
  [target.x86_64-w64-mingw32.bin-dependencies]
    path-option = ["D:\\path\\to\\stdx\\dynamic\\stdx"]
```

### 3.2 静态库配置（推荐生产部署使用）

使用 crypto 和 net 包的静态库时，需要额外添加 `compile-option`，因为 OpenSSL 静态库依赖系统符号。

**Linux（静态库 + crypto/net）**：

```toml
[package]
  name = "my-tls-app"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-ldl"

[dependencies]

[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

**macOS（静态库）**：

macOS 下使用静态库无需额外 `compile-option`：

```toml
[package]
  name = "my-tls-app"
  version = "1.0.0"
  output-type = "executable"

[target.aarch64-apple-darwin]
  [target.aarch64-apple-darwin.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

**Windows（静态库 + crypto/net）**：

```toml
[package]
  name = "my-tls-app"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-lcrypt32"

[target.x86_64-w64-mingw32]
  [target.x86_64-w64-mingw32.bin-dependencies]
    path-option = ["D:\\path\\to\\stdx\\static\\stdx"]
```

### 3.3 静态库额外配置速查

| 平台 | compile-option | 原因 |
|------|----------------|------|
| Linux | `-ldl` | OpenSSL 静态库依赖 `libdl` |
| Windows | `-lcrypt32` | OpenSSL 依赖 Windows 证书存储 API |
| macOS | 无需额外配置 | — |

---

## 4. 构建与运行

### 4.1 基本流程

```bash
# 1. 初始化项目
cjpm init --name my-tls-app

# 2. 编辑 cjpm.toml，添加 bin-dependencies 配置（参见上方）

# 3. 编写代码（import stdx.net.tls.*）

# 4. 构建
cjpm build

# 5. 运行
cjpm run
```

> **说明**：`cjpm run` 会自动配置动态库依赖路径，无需额外设置环境变量。

### 4.2 独立部署运行（动态库）

如果不通过 `cjpm run` 而是直接执行可执行文件，需手动设置动态库搜索路径：

| 操作系统 | 环境变量 | 示例 |
|----------|----------|------|
| Linux | `LD_LIBRARY_PATH` | `export LD_LIBRARY_PATH=/path/to/stdx/dynamic/stdx:$LD_LIBRARY_PATH` |
| macOS | `DYLD_LIBRARY_PATH` | `export DYLD_LIBRARY_PATH=/path/to/stdx/dynamic/stdx:$DYLD_LIBRARY_PATH` |
| Windows | `PATH` | 将 stdx 动态库目录和 OpenSSL DLL 目录添加到 `PATH` |

### 4.3 静态库部署

静态库编译的产物无需设置动态库搜索路径，可直接运行：

```bash
cjpm build
./target/release/bin/my-tls-app
```

---

## 5. 完整示例

### 5.1 TLS 客户端项目

**项目结构**：

```text
my-tls-client/
├── cjpm.toml
└── src/
    └── main.cj
```

**cjpm.toml**（Linux x86_64 动态库）：

```toml
[package]
  name = "my-tls-client"
  version = "1.0.0"
  output-type = "executable"

[dependencies]

[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

**src/main.cj**：

```cangjie
import std.net.TcpSocket
import stdx.net.tls.*

main() {
    var config = TlsClientConfig()
    config.verifyMode = TrustAll

    try (socket = TcpSocket("127.0.0.1", 8443)) {
        socket.connect()
        try (tls = TlsSocket.client(socket, clientConfig: config)) {
            tls.handshake()
            tls.write("Hello TLS!\n".toArray())

            let buf = Array<Byte>(1024, repeat: 0)
            let n = tls.read(buf)
            println(String.fromUtf8(buf[..n]))
        }
    }
}
```

**构建运行**：

```bash
cjpm build && cjpm run
```

### 5.2 HTTPS 客户端项目

**cjpm.toml**（Linux x86_64 静态库，生产部署）：

```toml
[package]
  name = "my-https-client"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-ldl"

[dependencies]

[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

**src/main.cj**：

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import std.io.*

main() {
    var tlsConfig = TlsClientConfig()
    // 生产环境使用 Default 模式（系统 CA 验证）

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    let resp = client.get("https://www.example.com/")
    println("Status: ${resp.status}")
    println("Body: ${StringReader(resp.body).readToEnd()}")

    client.close()
}
```

**构建部署**：

```bash
cjpm build
# 静态库产物可直接部署运行，无需动态库依赖
./target/release/bin/my-https-client
```

---

## 6. 常见问题

### 6.1 运行时报 TlsException

- **现象**：`TlsException: Can not load openssl library or function xxx`
- **原因**：未安装 OpenSSL 3 或安装了低版本
- **解决**：安装 OpenSSL 3（参见第 2 节），确认 `openssl version` 输出为 3.x.x

### 6.2 编译时找不到 stdx 库

- **现象**：编译报错找不到 `stdx.net.tls` 包
- **原因**：`cjpm.toml` 中 `bin-dependencies` 的 `path-option` 路径不正确
- **解决**：确认路径指向 stdx 解压目录下的 `dynamic/stdx` 或 `static/stdx` 子目录

### 6.3 静态库链接报错

- **现象**：链接阶段报 undefined reference 错误
- **原因**：缺少平台特定的链接选项
- **解决**：Linux 添加 `compile-option = "-ldl"`，Windows 添加 `compile-option = "-lcrypt32"`

### 6.4 独立运行时找不到动态库

- **现象**：直接执行可执行文件报 `cannot open shared object file`
- **原因**：未设置动态库搜索路径
- **解决**：设置 `LD_LIBRARY_PATH`（Linux）或 `DYLD_LIBRARY_PATH`（macOS），或改用静态库编译

---

## 7. 快速参考

| 需求 | 做法 |
|------|------|
| 安装 OpenSSL 3 | Linux: `apt install libssl-dev`，macOS: `brew install openssl@3`，Windows: 下载预编译包 |
| 动态库配置 | `path-option = ["/path/to/stdx/dynamic/stdx"]` |
| 静态库配置 | `path-option = ["/path/to/stdx/static/stdx"]` |
| Linux 静态库额外选项 | `compile-option = "-ldl"` |
| Windows 静态库额外选项 | `compile-option = "-lcrypt32"` |
| 构建运行 | `cjpm build && cjpm run` |
| 独立部署（动态库） | 设置 `LD_LIBRARY_PATH` / `DYLD_LIBRARY_PATH` / `PATH` |
| 独立部署（静态库） | 直接运行 `./target/release/bin/<name>` |
| 验证 OpenSSL | `openssl version`（应为 3.x.x） |
