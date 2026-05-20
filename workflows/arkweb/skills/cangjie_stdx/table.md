---
name: cangjie-stdx
description: "仓颉扩展标准库（stdx）使用指南。当需要了解 stdx 提供的面向切面编程、压缩和解压缩、安全加密、消息摘要、非对称加解密和签名、数字证书、编解码（Base64/Hex/JSON/URL）、网络通信（HTTP/TLS）、日志、序列化、模糊测试等功能时，应使用此 Skill"
---

# 仓颉扩展标准库（stdx）使用指南

---

## 1. stdx 概述

stdx 是仓颉编程语言的**扩展标准库**，由官方提供的附加功能集，与标准库的区别是：

- **标准库（std）**：随 SDK 一起发布，开箱即用。
- **扩展标准库（stdx）**：需要**单独下载**并配置，作为三方库使用。

---

## 2. stdx 包功能详解

stdx 包含以下 18 个包，覆盖网络通信、编解码、安全加密、日志、测试等多个领域：

| 包名 | 功能 |
|------|------|
| `stdx.net.http` | HTTP 客户端与服务端 |
| `stdx.net.tls` | TLS 安全传输 |
| `stdx.encoding.json` | JSON 解析与构建 |
| `stdx.encoding.json.stream` | JSON 流式序列化 |
| `stdx.encoding.base64` | Base64 编解码 |
| `stdx.encoding.hex` | 十六进制编解码 |
| `stdx.encoding.url` | URL 解析与编解码 |
| `stdx.crypto.crypto` | 对称加密与安全随机数 |
| `stdx.crypto.digest` | 消息摘要算法 |
| `stdx.crypto.keys` | 非对称加密与签名 |
| `stdx.crypto.x509` | 数字证书处理 |
| `stdx.log` | 抽象日志接口 |
| `stdx.logger` | 日志实现 |
| `stdx.serialization.serialization` | 序列化框架 |
| `stdx.compress.zlib` | 压缩与解压缩 |
| `stdx.aspectCJ` | 面向切面编程 |
| `stdx.fuzz.fuzz` | 模糊测试 |
| `stdx.unittest.data` | 参数化测试数据 |

### 2.1 stdx.net.http — HTTP 客户端与服务端

提供 HTTP/1.1、HTTP/2 协议的 Server 端和 Client 端完整实现，同时支持 WebSocket 协议。主要能力包括：

- **服务端**：通过 `ServerBuilder` 构建 HTTP 服务器，支持路由注册、请求处理器（`HttpRequestHandler`）、请求分发（`HttpRequestDistributor`）、文件上传下载（`FileHandler`）、分块传输编码、HTTPS（集成 TLS）等。
- **客户端**：通过 `ClientBuilder` 构建 HTTP 客户端，支持 GET/POST/PUT/DELETE 等方法、自动重定向、Cookie 管理（`CookieJar`）、HTTP 代理、连接超时配置等。
- **WebSocket**：支持客户端和服务端的 WebSocket 升级，提供文本帧、二进制帧、Ping/Pong 控制帧的收发能力。
- **HTTP/2 特性**：支持 Server Push（`HttpResponsePusher`）和多路复用。

### 2.2 stdx.net.tls — TLS 安全传输

提供 TLS 1.2 和 TLS 1.3 安全加密的网络通信能力，包括：

- 创建 TLS 服务器和客户端（`TlsSocket`），基于协议进行 TLS 握手。
- 收发加密数据，支持双向认证。
- 支持 TLS 会话恢复（`TlsSessionContext`），减少重复握手开销。
- 灵活的证书验证模式（`CertificateVerifyMode`）和签名算法配置。
- 客户端和服务端 TLS 配置通过 `TlsClientConfig` 和 `TlsServerConfig` 结构体指定。
- 通常通过 HTTP 模块的 `tlsConfig()` 方法集成使用，实现 HTTPS。

### 2.3 stdx.encoding.json — JSON 解析与构建

用于 JSON 数据的处理，实现 String、JsonValue、DataModel 之间的相互转换。主要能力包括：

- **解析**：通过 `JsonValue.fromStr(str)` 将 JSON 字符串解析为 `JsonValue` 对象树。
- **构建**：使用 `JsonObject`、`JsonArray`、`JsonString`、`JsonInt`、`JsonFloat`、`JsonBool`、`JsonNull` 等类型构建 JSON 结构。
- **类型判断**：通过 `.kind()` 方法获取 `JsonKind` 枚举，结合 `match` 表达式处理不同 JSON 类型。
- **与序列化框架集成**：通过 `ToJson` 接口实现 JsonValue 与 `DataModel`（序列化中间层）之间的互转，支持 `DataModel.fromJson(jv)` 和 `dm.toJson()`。
- **格式化输出**：`toString()` 输出紧凑格式，`toJsonString()` 输出格式化的 JSON 字符串。

### 2.4 stdx.encoding.json.stream — JSON 流式序列化

提供仓颉对象和 JSON 数据流之间的互相转换能力，适合大数据量场景和自定义类型的 JSON 序列化：

- **JsonWriter**：将仓颉对象序列化为 JSON 数据流，支持链式调用 `.startObject()` `.writeName()` `.writeValue()` `.endObject()` 等方法。支持的值类型包括基本类型、Array、ArrayList、HashMap、Option、BigInt、Decimal 等。
- **JsonReader**：从 JSON 数据流反序列化为仓颉对象，通过 `.startObject()` `.readName()` `.readValue<T>()` `.peek()` `.skip()` 等方法逐步读取。
- **自定义类型**：实现 `JsonSerializable` 接口（`toJson` 方法）和 `JsonDeserializable<T>` 接口（`fromJson` 静态方法），即可支持自定义类型与 JSON 的互转。
- **格式控制**：通过 `WriteConfig` 控制输出格式（紧凑或美化）。

### 2.5 stdx.encoding.base64 — Base64 编解码

提供 Base64 编码与解码功能，将二进制数据转换为由 64 个可打印字符（A-Z、a-z、0-9、+、/）组成的文本格式，适用于在文本协议中安全传输二进制数据。

- `toBase64String(data: Array<Byte>): String` — 将字节数组编码为 Base64 字符串。
- `fromBase64String(str: String): Array<Byte>` — 将 Base64 字符串解码为字节数组。

### 2.6 stdx.encoding.hex — 十六进制编解码

提供十六进制（Hex）编码与解码功能，使用 16 个字符（0-9、A-F，大小写不敏感）表示二进制数据。

- `toHexString(data: Array<Byte>): String` — 将字节数组编码为十六进制字符串。
- `fromHexString(str: String): Array<Byte>` — 将十六进制字符串解码为字节数组。

### 2.7 stdx.encoding.url — URL 解析与编解码

提供 URL 相关的能力，包括解析 URL 的各个组件（scheme、host、port、path、query、fragment）、对 URL 进行编解码、合并 URL 或路径等。

- **URL 类**：通过 `URL.parse(rawUrl)` 解析 URL 字符串，或通过构造函数 `URL(scheme!, hostName!, path!)` 构建 URL 对象。
- **Form 类**：用于处理 URL 查询参数（key-value 形式），支持 `.add(key, value)` 和 `.get(key)` 操作。
- **UserInfo 类**：表示 URL 中的用户信息（用户名和密码）。
- 对包含非 ASCII 字符的 URL 进行百分号编码。

### 2.8 stdx.crypto.crypto — 对称加密与安全随机数

提供安全加密能力，包括：

- **SecureRandom**：密码学安全的随机数生成器，可生成安全随机字节序列。构造函数 `SecureRandom(priv!: Bool = false)` 中 `priv` 参数指定是否使用私有随机源。
- **SM4**：中国国密标准 SM4 对称加密/解密算法，支持 ECB、CBC、CTR、GCM 等操作模式（`OperationMode`），以及 PKCS7Padding、NoPadding 等填充模式（`PaddingMode`）。

### 2.9 stdx.crypto.digest — 消息摘要算法

提供常用的消息摘要（哈希）算法，支持对任意数据计算固定长度的摘要值：

- **MD5**：128 位摘要（注意：已不推荐用于安全场景）。
- **SHA 系列**：SHA1（160 位）、SHA224、SHA256（256 位）、SHA384、SHA512（512 位）。
- **SM3**：中国国密标准哈希算法，256 位摘要。
- **HMAC**：基于哈希的消息认证码，通过 `HMAC(key, algorithm)` 构建，支持所有上述哈希算法。
- 所有算法通用方法：`write(Array<Byte>)` 输入数据、`finish(): Array<Byte>` 获取摘要、`reset()` 重置状态。

### 2.10 stdx.crypto.keys — 非对称加密与签名

提供非对称加密和数字签名算法：

- **RSA**：`RSAPrivateKey(bits)` / `RSAPublicKey(pri)` — 支持公钥加密/私钥解密、私钥签名/公钥验签，支持 OAEP 和 PSS 填充模式。
- **SM2**：`SM2PrivateKey()` / `SM2PublicKey(pri)` — 中国国密非对称加密算法。
- **ECDSA**：`ECDSAPrivateKey(curve)` / `ECDSAPublicKey(pri)` — 椭圆曲线数字签名，支持 P224、P256、P384、P521 等曲线。
- 所有密钥类型支持 PEM 格式的编解码。

### 2.11 stdx.crypto.x509 — 数字证书处理

提供 X509 数字证书的完整处理能力：

- **证书解析**：从 PEM 或 DER 格式解析证书（`X509Certificate.decodeFromPem()` / `.decodeFromDer()`）。
- **证书验证**：验证证书签名和有效期，支持证书链验证。
- **证书创建**：创建自签名证书、构建证书链。
- **证书签名请求（CSR）**：通过 `X509CertificateRequest` 创建和解析 CSR。
- **证书信息**：访问证书的主体（`X509Name`）、颁发者、序列号、有效期、密钥用途（`KeyUsage`/`ExtKeyUsage`）等。

### 2.12 stdx.log — 抽象日志接口

提供一个**抽象**的日志 API，不绑定具体的日志实现，让库开发者可以在不依赖特定日志框架的情况下输出日志：

- **Logger**（抽象类）：提供 `.trace()` `.debug()` `.info()` `.warn()` `.error()` `.fatal()` 等日志方法，每个方法接受消息字符串和可选的键值属性 `Attr`（类型为 `(String, LogValue)` 元组）。
- **日志级别**：`LogLevel.TRACE` < `DEBUG` < `INFO` < `WARN` < `ERROR` < `FATAL` < `OFF`。
- **全局 Logger**：通过 `setGlobalLogger(logger)` 设置，通过 `getGlobalLogger(attrs)` 获取（可附加属性）。
- **惰性求值**：支持 `logger.trace({=> "expensive: ${compute()}"})` 形式，仅在日志级别启用时才计算消息内容。
- **NoopLogger**：空实现，所有方法不执行任何操作。

### 2.13 stdx.logger — 日志实现

提供三种内置的 Logger 实现，均接受 `OutputStream` 参数用于指定输出目标：

- **SimpleLogger**：传统文本格式 — `2025-04-15T10:30:00Z INFO msg key=value`
- **TextLogger**：键值对文本格式 — `time=... level=INFO msg="..." key=value`
- **JsonLogger**：JSON 格式 — `{"time":"...","level":"INFO","msg":"...","key":"value"}`

### 2.14 stdx.serialization.serialization — 序列化框架

提供通用的序列化与反序列化能力，通过中间层 `DataModel` 实现仓颉对象与各种数据格式的互转：

- **Serializable\<T\> 接口**：自定义类型实现 `serialize(): DataModel` 和 `static deserialize(DataModel): T` 方法即可支持序列化。
- **DataModel 类型体系**：`DataModelBool`、`DataModelInt`、`DataModelFloat`、`DataModelString`、`DataModelNull`（基本类型）、`DataModelSeq`（序列/数组）、`DataModelStruct`（结构体/对象）。
- **Field**：`DataModelStruct` 的字段单元，通过 `field<T>(name, data)` 辅助函数创建。
- 与 JSON 包联动：`DataModel.fromJson(jsonValue)` 和 `dataModel.toJson()` 实现与 JSON 的互转。

### 2.15 stdx.compress.zlib — 压缩与解压缩

提供基于 deflate 算法的数据压缩与解压缩功能，支持 deflate-raw 和 gzip 两种格式，采用流式 API：

- **CompressInputStream / CompressOutputStream**：压缩流，将数据压缩后写入或读出。
- **DecompressInputStream / DecompressOutputStream**：解压流，将压缩数据解压后写入或读出。
- **压缩级别**（`CompressLevel`）：`DefaultCompression`（默认平衡）等。
- **数据格式**（`WrapType`）：`DeflateFormat`（deflate-raw 格式）、`GzipFormat`（gzip 格式）。

### 2.16 stdx.aspectCJ — 面向切面编程（AOP）

提供仓颉中面向切面编程（Aspect Oriented Programming）相关的注解能力，通过编译器插件在编译期将切面逻辑织入目标函数：

- **@InsertAtEntry**：在目标函数入口插入指定函数调用。
- **@InsertAtExit**：在目标函数出口插入指定函数调用。
- **@ReplaceFuncBody**：将目标函数体替换为指定函数调用。

需要编译器插件 `libcollect-aspects.so`（收集阶段）和 `libwave-aspects.so`（织入阶段）配合使用。有泛型、可见性、参数类型匹配等约束条件。

### 2.17 stdx.fuzz.fuzz — 模糊测试

提供基于覆盖率反馈的模糊测试（Fuzzing）引擎，用于自动化发现 API 中的潜在缺陷：

- **Fuzzer**：模糊测试引擎，由 `FuzzerBuilder` 构建。
- **FuzzDataProvider**：将变异的字节流转换为标准仓颉类型（Int64、String、Bool、Array\<Byte\> 等），方便编写测试代码。
- **DebugDataProvider**：带调试信息的数据提供者。
- 仅支持 Linux 和 macOS，依赖 LLVM 的 `libclang_rt.fuzzer_no_main.a`。

### 2.18 stdx.unittest.data — 参数化测试数据加载

为参数化单元测试提供外部数据源加载能力，支持从文件加载测试数据并自动反序列化为仓颉对象：

- `json<T>(filePath)` — 从 JSON 文件加载测试数据。
- `csv<T>(filePath, ...)` — 从 CSV 文件加载测试数据（支持自定义分隔符、引号、注释字符等）。
- `tsv<T>(filePath, ...)` — 从 TSV 文件加载测试数据。
- 类型 T 需实现 `Serializable` 接口。

---

## 3. 项目配置、构建与运行

> **项目配置与构建指导**请参考 `cangjie-stdx-config` Skill

---

## 4. 完整示例

### 4.1 HTTP 服务端 + 客户端

**cjpm.toml 配置**（Linux x86_64 动态库，其他平台配置请参考 `cangjie-stdx-config` Skill）：

```toml
[package]
  name = "http_demo"
  version = "1.0.0"
  output-type = "executable"

[dependencies]

[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

**HTTP 服务端**（创建一个简单的 HTTP 服务器并注册多个路由）：

```cangjie
import stdx.net.http.{ServerBuilder, HttpRequestHandler, FuncHandler}

main() {
    // 1. 构建 Server 实例
    let server = ServerBuilder()
                    .addr("127.0.0.1")
                    .port(8080)
                    .build()

    // 2. 注册多个路由处理器
    server.distributor.register("/index", {httpContext =>
        httpContext.responseBuilder.body("Hello 仓颉!")
    })
    server.distributor.register("/id", {httpContext =>
        httpContext.responseBuilder.body("id page")
    })
    server.distributor.register("/help", {httpContext =>
        httpContext.responseBuilder.body("help page")
    })

    // 3. 启动服务
    server.serve()
}
```

**HTTP 客户端**（发送 GET 请求并读取响应）：

```cangjie
import stdx.net.http.*
import std.io.*

main() {
    // 1. 构建 Client 实例
    let client = ClientBuilder().build()

    // 2. 发送 GET 请求
    let rsp = client.get("http://127.0.0.1:8080/index")

    // 3. 读取响应体
    let buf = Array<UInt8>(1024, repeat: 0)
    let len = rsp.body.read(buf)
    println(String.fromUtf8(buf[..len]))

    // 4. 关闭客户端
    client.close()
}
```

### 4.2 JSON 解析与构建

```cangjie
import stdx.encoding.json.*
import std.collection.*

main() {
    // === 从字符串解析 JSON ===
    var str = ##"[true,"kjjjke\"eed",{"sdfd":"ggggg","eeeee":[341,false,{"nnnn":55.87}]},3422,22.341,false,[22,22.22,true,"ddd"],43]"##
    var jv: JsonValue = JsonValue.fromStr(str)

    // 紧凑格式输出
    println(jv.toString())
    // 格式化输出
    println(jv.toJsonString())

    // === 构建 JSON ===
    var obj = JsonObject()
    obj.put("name", JsonString("Alice"))
    obj.put("age", JsonInt(30))
    obj.put("active", JsonBool(true))

    var arr = JsonArray()
    arr.add(JsonInt(1))
    arr.add(JsonInt(2))
    arr.add(JsonString("hello"))
    obj.put("tags", arr)

    println(obj.toJsonString())
}
```

### 4.3 JSON 与自定义类型互转（通过 DataModel 序列化）

```cangjie
import stdx.serialization.serialization.*
import stdx.encoding.json.*

class Location <: Serializable<Location> {
    var country: String = ""
    var province: String = ""

    public func serialize(): DataModel {
        return DataModelStruct()
            .add(field<String>("country", country))
            .add(field<String>("province", province))
    }

    public static func deserialize(dm: DataModel): Location {
        var dms = match (dm) {
            case data: DataModelStruct => data
            case _ => throw Exception("this data is not DataModelStruct")
        }
        var result = Location()
        result.country = String.deserialize(dms.get("country"))
        result.province = String.deserialize(dms.get("province"))
        return result
    }
}

class Person <: Serializable<Person> {
    var name: String = ""
    var age: Int64 = 0
    var loc: Option<Location> = Option<Location>.None

    public func serialize(): DataModel {
        return DataModelStruct()
            .add(field<String>("name", name))
            .add(field<Int64>("age", age))
            .add(field<Option<Location>>("loc", loc))
    }

    public static func deserialize(dm: DataModel): Person {
        var dms = match (dm) {
            case data: DataModelStruct => data
            case _ => throw Exception("this data is not DataModelStruct")
        }
        var result = Person()
        result.name = String.deserialize(dms.get("name"))
        result.age = Int64.deserialize(dms.get("age"))
        result.loc = Option<Location>.deserialize(dms.get("loc"))
        return result
    }
}

main() {
    // JSON 字符串 → Person 对象
    var js = ##"{
    "name": "A",
    "age": 30,
    "loc": {
        "country": "China",
        "province": "Beijing"
    }
}"##

    var jv = JsonValue.fromStr(js)
    var dm = DataModel.fromJson(jv)
    var person = Person.deserialize(dm)
    println("name == ${person.name}")
    println("age == ${person.age}")
    println("country == ${person.loc.getOrThrow().country}")
    println("province == ${person.loc.getOrThrow().province}")
    println("====================")

    // Person 对象 → JSON 字符串
    dm = person.serialize()
    var jo = dm.toJson().asObject()
    println(jo.toJsonString())
}
```

### 4.4 日志记录

```cangjie
import stdx.log.*
import stdx.logger.*
import std.env.*

// 库开发者：使用抽象日志接口
public class PGConnection {
    let objId: Int64 = 1
    let logger = getGlobalLogger(("name", "PGConnection"))

    public func close(): Unit {
        logger.trace("driver conn closed", ("id", objId))
    }
}

main(): Unit {
    // 应用开发者：选择具体日志实现
    let logger = SimpleLogger(getStdOut())
    logger.level = LogLevel.TRACE
    setGlobalLogger(logger)

    // 使用日志
    logger.info("Application started", ("version", "1.0.0"))
    logger.debug("Processing request", ("path", "/api"))
    logger.error("Something went wrong", ("code", 500))

    // 库代码也能正常输出日志
    var conn = PGConnection()
    conn.close()
}
```

**JsonLogger 示例**：

```cangjie
import std.io.{OutputStream, BufferedOutputStream}
import std.env.*
import stdx.log.*
import stdx.logger.*

main() {
    let bo = BufferedOutputStream<OutputStream>(getStdOut())
    let logger = JsonLogger(bo)
    logger.level = LogLevel.TRACE
    setGlobalLogger(logger)

    let appLogger = getGlobalLogger([("name", "main")])
    appLogger.info("Hello, World!", ("k1", [[1, 4], [2, 5], [3]]), ("env", "production"))
    appLogger.debug("Debug info", ("module", "auth"))
    // 输出 JSON 格式日志
}
```

### 4.5 消息摘要（哈希）

```cangjie
import stdx.crypto.digest.*
import stdx.encoding.hex.*

main() {
    var str: String = "helloworld"

    // MD5 摘要
    var md5Instance = MD5()
    md5Instance.write(str.toArray())
    var md5Result = toHexString(md5Instance.finish())
    println("MD5: ${md5Result}")

    // SHA256 摘要
    var sha256Instance = SHA256()
    sha256Instance.write(str.toArray())
    var sha256Result = toHexString(sha256Instance.finish())
    println("SHA256: ${sha256Result}")

    // HMAC-SHA512
    var key: Array<UInt8> = "cangjie".toArray()
    var data: Array<UInt8> = "123456789".toArray()
    var hmac = HMAC(key, HashType.SHA512)
    hmac.write(data)
    var hmacResult = toHexString(hmac.finish())
    println("HMAC-SHA512: ${hmacResult}")
}
```

### 4.6 Gzip 文件压缩与解压缩

```cangjie
import stdx.compress.zlib.*
import std.fs.*

main() {
    // 创建测试数据
    var arr: Array<Byte> = Array<Byte>(1024 * 1024, {i => UInt8(i % 256)})
    File.writeTo("./test.txt", arr)

    // 压缩
    compressFile("./test.txt", "./test.gz")
    println("Compression done.")

    // 解压
    decompressFile("./test.gz", "./test_restored.txt")
    println("Decompression done.")

    // 验证
    if (File.readFrom("./test.txt") == File.readFrom("./test_restored.txt")) {
        println("Verification: success")
    } else {
        println("Verification: failed")
    }

    // 清理
    remove("./test.txt")
    remove("./test.gz")
    remove("./test_restored.txt")
}

func compressFile(srcPath: String, destPath: String): Unit {
    var srcFile = File(srcPath, Read)
    var destFile = File(destPath, Write)
    var compressOut = CompressOutputStream(destFile, wrap: GzipFormat, bufLen: 10000)
    var buf = Array<UInt8>(1024, repeat: 0)
    while (true) {
        var n = srcFile.read(buf)
        if (n > 0) {
            compressOut.write(buf.slice(0, n).toArray())
        } else {
            break
        }
    }
    compressOut.flush()
    compressOut.close()
    srcFile.close()
    destFile.close()
}

func decompressFile(srcPath: String, destPath: String): Unit {
    var srcFile = File(srcPath, Read)
    var destFile = File(destPath, Write)
    var decompressIn = DecompressInputStream(srcFile, wrap: GzipFormat, bufLen: 10000)
    var buf = Array<UInt8>(1024, repeat: 0)
    while (true) {
        var n = decompressIn.read(buf)
        if (n <= 0) { break }
        destFile.write(buf.slice(0, n).toArray())
    }
    decompressIn.close()
    srcFile.close()
    destFile.close()
}
```

### 4.7 Base64 与 Hex 编解码

```cangjie
import stdx.encoding.base64.*
import stdx.encoding.hex.*

main() {
    let data = "Hello, 仓颉!".toArray()

    // Base64 编解码
    let b64Encoded = toBase64String(data)
    println("Base64: ${b64Encoded}")
    let b64Decoded = fromBase64String(b64Encoded).getOrThrow()
    println("Decoded: ${String.fromUtf8(b64Decoded)}")

    // Hex 编解码
    let hexEncoded = toHexString(data)
    println("Hex: ${hexEncoded}")
    let hexDecoded = fromHexString(hexEncoded).getOrThrow()
    println("Decoded: ${String.fromUtf8(hexDecoded)}")
}
```

### 4.8 URL 解析

```cangjie
import stdx.encoding.url.*

main() {
    // 解析 URL
    let url = URL.parse("https://example.com:8080/api/v1?key=value&name=test#section")
    println("scheme: ${url.scheme}")
    println("host: ${url.host}")
    println("port: ${url.port}")
    println("path: ${url.path}")
    println("query: ${url.query}")
    println("fragment: ${url.fragment}")

    // 表单参数处理
    let form = Form()
    form.add("name", "张三")
    form.add("age", "30")
    println("form: ${form.toEncodeString()}")
}
```
