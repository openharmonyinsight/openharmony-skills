# 仓颉编程语言扩展库 API

仓颉编程语言扩展库（stdx）包含若干包，提供相关功能。

标准库为开发者提供了最通用的 API，而扩展库则专注于某一领域。如 compress 包提供压缩与解压缩能力，crypto 包提供加解密相关能力，net 包则专注于提供高效的网络协议解析和网络通信能力。

> **说明：**
>
> 目前，官方提供的扩展库不随仓颉编译器、工具链一起发布，需要用户单独下载。

## 包列表

stdx 含若干包，提供了丰富的扩展功能：

| 包名                                                                           | 功能                                                                                                                                                                                  |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [aspectCJ](./aspectCJ/aspectCJ_package_overview.md)                            | aspectCJ 包提供 Cangjie 中面向切面编程（Aspect Oriented Programming, AOP）相关的能力。                                                                                                |
| [compress.zlib](./compress/zlib/zlib_package_overview.md)                      | compress 包提供压缩解压功能。                                                                                                                                                         |
| [crypto.crypto](./crypto/crypto/crypto_package_overview.md)                    | crypto 包提供安全加密能力。                                                                                                                                                           |
| [crypto.digest](./crypto/digest/crypto_digest_package_overview.md)             | digest 包提供常用的消息摘要算法。                                                                                                                                                     |
| [crypto.keys](./crypto/keys/keys_package_overview.md)                          | keys 包提供非对称加密和签名算法。                                                                                                                                                     |
| [crypto.x509](./crypto/x509/x509_package_overview.md)                          | x509 包提供处理数字证书功能。                                                                                                                                                         |
| [encoding.base64](./encoding/base64/base64_package_overview.md)                | base 包提供字符串的 Base64 编码及解码。                                                                                                                                               |
| [encoding.hex](./encoding/hex/hex_package_overview.md)                         | hex 包提供字符串的 Hex 编码及解码。                                                                                                                                                   |
| [encoding.json](./encoding/json/json_package_overview.md)                      | json 包用于对 json 数据的处理，实现 String, JsonValue, DataModel 之间的相互转换。                                                                                                     |
| [encoding.json.stream](./encoding/json_stream/json_stream_package_overview.md) | json.stream 包主要用于仓颉对象和 JSON 数据流之间的互相转换。                                                                                                                          |
| [encoding.url](./encoding/url/url_package_overview.md)                         | url 包提供了 URL 相关的能力，包括解析 URL 的各个组件，对 URL 进行编解码，合并 URL 或路径等。 。                                                                                       |
| [fuzz](./fuzz/fuzz_package_overview.md)                                        | fuzz 包为开发者提供基于覆盖率反馈的仓颉 fuzz 引擎及对应的接口，开发者可以编写代码对 API 进行测试。                                                                                    |
| [log](./log/log_package_overview.md)                                           | log 包提供了日志记录相关的能力。                                                                                                                                                      |
| [logger](./logger/logger_package_overview.md)                                  | logger  包提供文本格式和 JSON 格式日志打印功能。                                                                                                                                      |
| [net.http](./net/http/http_package_overview.md)                                | http 包提供 HTTP/1.1，HTTP/2，WebSocket 协议的 server、client 端实现。                                                                                                                |
| [net.tls](./net/tls/tls_package_overview.md)                                   | tls 包用于进行安全加密的网络通信，提供创建 TLS 服务器、基于协议进行 TLS 握手、收发加密数据、恢复 TLS 会话等能力。                                                                     |
| [serialization](./serialization/serialization_package_overview.md)             | serialization 包提供了序列化和反序列化能力。                                                                                                                                          |
| [unittest.data](./unittest/data/data_package_overview.md)                      | unittest 模块提供了单元测试扩展能力。                                                                                                                                                 |

## 使用指导

仓颉编程语言扩展库 stdx 二进制包包含静态（static）和 动态 （dynamic） 两部分，请按需引用。

### 二进制产物结构

二进制包解压出来的目录包含 dynamic 和 static 两个目录：

dynamic/stdx 是动态产物，包含动态文件、cjo、bc 文件。

static/stdx 是静态产物，包含静态文件、cjo、bc 文件。

### 包依赖

| 导入库名                                  | 依赖包                                                                                                                                                                                                                         |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |                                                                                                                                                                                                     |
| import stdx.aspectCJ.*                    | stdx.aspectCJ                                                                                                                                                                                                                  |
| import stdx.compress.zlip.*               | stdx.compress.zlib                                                                                                                                                                                                             |
| import stdx.crypto.crypto.*               | stdx.crypto.crypto、stdx.crypto.digest                                                                                                                                               |
| import stdx.crypto.digest.*               | stdx.crypto.digest                                                                                                                                                                   |
| import stdx.crypto.keys.*                 | stdx.crypto.keys、stdx.crypto.x509、stdx.encoding.hex、stdx.crypto.crypto、stdx.crypto.digest、stdx.encoding.base64  |
| import stdx.crypto.x509.*                 | stdx.crypto.x509、stdx.encoding.hex、stdx.crypto.crypto、stdx.crypto.digest、stdx.encoding.base64                      |                                                                                                                                                                                                              |
| import stdx.encoding.hex.*                | stdx.encoding.hex                                                                                                                                                                                                              |
| import stdx.encoding.base64.*             | stdx.encoding.base64                                                                                                                                                                                                           |
| import stdx.encoding.json.*               | stdx.encoding.json、stdx.serialization.serialization                                                                                                                                                                           |
| import stdx.encoding.json.stream.*        | stdx.encoding.json.stream                                                                                                                                                                                                      |
| import stdx.encoding.url.*                | stdx.encoding.url                                                                                                                                                                                                              |
| import stdx.log.*                         | stdx.log                                                                                                                                                                                                                       |
| import stdx.logger.*                      | stdx.logger                                                                                                                                                                                                                    |
| import stdx.serialization.serialization.* | stdx.serialization.serialization                                                                                                                                                                                               |
| import stdx.fuzz.fuzz.*                   | stdx.fuzz.fuzz                                                                                                                                                                                                                 |
| import stdx.net.http .*                   | stdx.net.http、 stdx.net.tls、stdx.logger、stdx.log、stdx.encoding.url、stdx.encoding.json.stream、stdx.crypto.x509、stdx.encoding.hex、stdx.crypto.crypto、stdx.crypto.digest、stdx.encoding.base64 |
| import stdx.net.tls.*                     | stdx.net.tls、stdx.crypto.x509、stdx.encoding.hex、stdx.crypto.crypto、stdx.crypto.digest、stdx.encoding.base64                                                                       |
| import stdx.unittest.data.*               | stdx.encoding.json、stdx.serialization.serialization                                                                                                                                                                           |

代码中导入上述包，用 cjc 命令去编译代码，需要严格按照上述包的依赖的顺序去链接。 如果是用 cjpm 则无需关注。

如果使用静态库，在导入 crypto 和 net 库时，由于需要依赖系统符号，所以 `Windows` 操作系统 需要额外添加 `-lcrypt32`，`Linux` 操作系统 需要额外添加 `-ldl`。

### cjc 使用命令示例

cjc 的介绍和编译请查看 cangjie 用户手册

```cangjie
import stdx.aspectCJ.*
import stdx.compress.zlib.*
import stdx.crypto.crypto.*
import stdx.crypto.digest.*
import stdx.crypto.keys.*
import stdx.crypto.x509.*
import stdx.encoding.hex.*
import stdx.encoding.base64.*
import stdx.encoding.json.*
import stdx.encoding.url.*
import stdx.encoding.json.stream.*
import stdx.net.tls.*
import stdx.net.http.*
import stdx.log.*
import stdx.logger.*
import stdx.serialization.serialization.*
main() {
    0
}
```

Linux 和 mac 的编译命令：

```shell
$ cjc main.cj -L $CANGJIE_STDX_PATH -lstdx.aspectCJ -lstdx.encoding.json -lstdx.serialization.serialization -lstdx.net.http -lstdx.net.tls -lstdx.logger -lstdx.log -lstdx.encoding.url -lstdx.encoding.json.stream -lstdx.crypto.keys -lstdx.crypto.x509 -lstdx.encoding.hex -lstdx.crypto.crypto -lstdx.crypto.digest -lstdx.encoding.base64 -lstdx.compress.zlib -lstdx.compress -ldl --import-path $CANGJIE_STDX_PATH -o main.out
```

windows 编译命令：

```shell
$ cjc main.cj -L $CANGJIE_STDX_PATH -lstdx.aspectCJ -lstdx.encoding.json -lstdx.serialization.serialization -lstdx.net.http -lstdx.net.tls -lstdx.logger -lstdx.log -lstdx.encoding.url -lstdx.encoding.json.stream -lstdx.crypto.keys -lstdx.crypto.x509 -lstdx.encoding.hex -lstdx.crypto.crypto -lstdx.crypto.digest -lstdx.encoding.base64 -lstdx.compress.zlib -lstdx.compress -lcrypt32 --import-path $CANGJIE_STDX_PATH -o main.out
```

CANGJIE_STDX_PATH 是设置的 stdx 路径。

例如在 linux 系统中设置：

```shell
export CANGJIE_STDX_PATH=/target/linux_x86_64_cjnative/dynamic/stdx
```

运行前 Linux 操作系统需要在 LD_LIBRARY_PATH 中设置扩展库的路径，Windows 操作系统需要在 PATH 中设置扩展库的路径，macOS 操作系统需要在 DYLD_LIBRARY_PATH 中设置扩展库的路径。

### cjpm 使用示例

cjpm 的介绍和使用请查看 cjpm 手册。

cjpm.toml 增加如下配置：

```text
[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["${CANGJIE_STDX_PATH}"]
```

上面配置中 x86_64-unknown-linux-gnu 这是表示的系统架构信息，需要通过 cjc -v 获取。并替换成自己获取的系统信息。
CANGJIE_STDX_PATH 是设置的 stdx 路径。
