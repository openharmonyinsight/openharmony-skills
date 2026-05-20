# stdx.net.tls

## 功能介绍

tls 包用于进行安全加密的网络通信，提供创建 TLS 服务器、基于协议进行 TLS 握手、收发加密数据、恢复 TLS 会话等能力。

本包支持 TLS 1.2 及 TLS 1.3 传输层安全协议通信。

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

> **注意：**
>
> 如果未安装`OpenSSL 3`软件包或者安装低版本的软件包，程序可能无法使用并抛出相关异常 TlsException: Can not load openssl library or function xxx.。

## API 列表

### 类

| 类名                                                                                | 功能                                                                                                                                                       |
| ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [TlsSessionContext](./tls_package_api/tls_package_classes.md#class-tlssessioncontext) | 服务端启用 session 特性恢复会话，存储 session 用于对客户端进行验证类型。                                  |
| [TlsSocket](./tls_package_api/tls_package_classes.md#class-tlssocket)               | 用于在客户端及服务端间创建加密传输通道。                                                                                                                   |

### 枚举

| 枚举名                                                                                                 | 功能                                                               |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| [CertificateVerifyMode](./tls_package_api/tls_package_enums.md#enum-certificateverifymode)                   | 证书认证模式。 |
| [SignatureAlgorithm](./tls_package_api/tls_package_enums.md#enum-signaturealgorithm)                   | 签名算法类型，签名算法用于确保传输数据的身份验证、完整性和真实性。 |
| [SignatureSchemeType](./tls_package_api/tls_package_enums.md#enum-signatureschemetype)                 | 加密算法类型，用于保护网络通信的安全性和隐私性。                   |
| [SignatureType](./tls_package_api/tls_package_enums.md#enum-signaturetype)                             | 签名算法类型，用于认证真实性。                                     |
| [TlsClientIdentificationMode](./tls_package_api/tls_package_enums.md#enum-tlsclientidentificationmode) | 服务端对客户端证书的认证模式。                                     |
| [TlsVersion](./tls_package_api/tls_package_enums.md#enum-tlsversion) | TLS 协议版本。                                     |

### 结构体

| 结构体名                                                                           | 功能               |
| ---------------------------------------------------------------------------------- | ------------------ |
| [CipherSuite](./tls_package_api/tls_package_structs.md#struct-ciphersuite)         | TLS 中的密码套件。 |
| [TlsClientConfig](./tls_package_api/tls_package_structs.md#struct-tlsclientconfig) | 客户端配置。       |
| [TlsServerConfig](./tls_package_api/tls_package_structs.md#struct-tlsserverconfig) | 服务端配置。       |
| [TlsSession](./tls_package_api/tls_package_structs.md#struct-tlssession) | 当客户端 TLS 握手成功后，将会生成一个会话，当连接因一些原因丢失后，客户端可以通过这个会话 id 复用此次会话，省略握手流程。       |

### 异常类

| 类名                                                                           | 功能               |
| ---------------------------------------------------------------------------------- | ------------------ |
| [TlsException](./tls_package_api/tls_package_exceptions.md#class-tlsexception)         | TLS 处理出现错误时抛出的异常类型。 |
