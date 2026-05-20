# 接口

## interface DHParameters

```cangjie
public interface DHParameters <: Key {
    override func encodeToPem(): PemEntry
    static func decodeDer(blob: DerBlob): DHParameters
    static func decodeFromPem(text: String): DHParameters
}
```

功能：提供 DH 密钥参数接口。

父类型：

- [Key](#interface-key)

### static func decodeDer(DerBlob)

```cangjie
static func decodeDer(blob: DerBlob): DHParameters
```

功能：将 DH 密钥参数从 DER 格式解码。

> **说明：**
>
> - DH（Diffie-Hellman）密钥交换协议是一种确保共享 KEY 安全穿越不安全网络的方法。
> - DER 和 PEM 是两种常见的编码格式。

参数：

- blob: [DerBlob](x509_package_structs.md#struct-derblob) - DER 格式的 DH 密钥参数对象。

返回值：

- [DHParameters](x509_package_interfaces.md#interface-dhparameters) - 由 DER 格式解码出的 DH 密钥参数。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 当 DER 格式的 DH 密钥参数内容不正确，无法解析时抛出异常。

### static func decodeFromPem(String)

```cangjie
static func decodeFromPem(text: String): DHParameters
```

功能：将 DH 密钥参数从 PEM 格式解码。

> **说明：**
>
> PEM 是用 ASCLL(BASE64) 编码的证书。

参数：

- text: String - PEM 格式的 DH 密钥参数字符流。

返回值：

- [DHParameters](x509_package_interfaces.md#interface-dhparameters) - 由 PEM 格式解码出的 DH 密钥参数。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 字符流不符合 PEM 格式，或文件头不符合 DH 密钥参数头标准（"-----BEGIN DH PARAMETERS-----"）时抛出异常。

### func encodeToPem()

```cangjie
override func encodeToPem(): PemEntry
```

功能：将 DH 密钥参数编码为 PEM 格式。

返回值：

- [PemEntry](x509_package_structs.md#struct-pementry) - DH 密钥参数数据 PEM 格式编码生成的对象。

## interface Key

```cangjie
public interface Key <: ToString {
    func encodeToDer(): DerBlob
    func encodeToPem(): PemEntry
    static func decodeDer(encoded: DerBlob): Key
    static func decodeFromPem(text: String): Key
}
```

功能：提供密钥接口。公钥用于签名验证或加密，私钥用于签名或解密，公钥和私钥必须相互匹配并形成一对。该类为密钥类，无具体实现，供 [PrivateKey](x509_package_interfaces.md#interface-privatekey)/[PublicKey](x509_package_interfaces.md#interface-publickey) 及用户扩展接口。

父类型：

- ToString

### static func decodeDer(DerBlob)

```cangjie
static func decodeDer(encoded: DerBlob): Key
```

功能：将密钥从 DER 格式解码。

参数：

- encoded: [DerBlob](x509_package_structs.md#struct-derblob) - DER 格式的对象。

返回值：

- [Key](x509_package_interfaces.md#interface-key) - 由 DER 格式解码出的密钥。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 当 DER 格式的私钥内容不正确，无法解析时抛出异常。

### static func decodeFromPem(String)

```cangjie
static func decodeFromPem(text: String): Key
```

功能：将密钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的字符流。

返回值：

- [Key](x509_package_interfaces.md#interface-key) - 由 PEM 格式解码出的密钥。

### func encodeToDer()

```cangjie
func encodeToDer(): DerBlob
```

功能：将密钥编码为 DER 格式。

返回值：

- [DerBlob](x509_package_structs.md#struct-derblob) - 密钥数据 DER 格式编码生成的对象。

### func encodeToPem()

```cangjie
func encodeToPem(): PemEntry
```

功能：将密钥编码为 PEM 格式。

返回值：

- [PemEntry](x509_package_structs.md#struct-pementry) - 密钥数据 PEM 格式编码生成的对象。

## interface PrivateKey

```cangjie
public interface PrivateKey <: Key {
    static func decodeDer(blob: DerBlob): PrivateKey
    static func decodeFromPem(text: String): PrivateKey
    static func decodeDer(blob: DerBlob, password!: ?String): PrivateKey
    static func decodeFromPem(text: String, password!: ?String): PrivateKey
    func encodeToDer(password!: ?String): DerBlob
    override func encodeToPem(): PemEntry
    func encodeToPem(password!: ?String): PemEntry
}
```

功能：提供私钥接口。

父类型：

- [Key](#interface-key)

### static func decodeDer(DerBlob)

```cangjie
static func decodeDer(blob: DerBlob): PrivateKey
```

功能：将私钥从 DER 格式解码。

参数：

- blob: [DerBlob](x509_package_structs.md#struct-derblob) - DER 格式的私钥对象。

返回值：

- [PrivateKey](x509_package_interfaces.md#interface-privatekey) - 由 DER 格式解码出的私钥。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 当 DER 格式的私钥内容不正确，无法解析时抛出异常。

### static func decodeDer(DerBlob, ?String)

```cangjie
static func decodeDer(blob: DerBlob, password!: ?String): PrivateKey
```

功能：将 DER 格式的私钥解密解码成 [PrivateKey](x509_package_interfaces.md#interface-privatekey) 对象，密码为 None 时则不解密。

参数：

- blob: [DerBlob](x509_package_structs.md#struct-derblob) - DER 格式的私钥。
- password!: ?String - 解密密码。

返回值：

- [PrivateKey](x509_package_interfaces.md#interface-privatekey) - 解密解码后的私钥对象。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 解密解码失败，或者`password`为空字符串。

### static func decodeFromPem(String)

```cangjie
static func decodeFromPem(text: String): PrivateKey
```

功能：将私钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的私钥字符流。

返回值：

- [PrivateKey](x509_package_interfaces.md#interface-privatekey) - 由 PEM 格式解码出的私钥。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 字符流不符合 PEM 格式，或文件头不符合公钥头标准时抛出异常。

### static func decodeFromPem(String, ?String)

```cangjie
static func decodeFromPem(text: String, password!: ?String): PrivateKey
```

功能：将 PEM 格式的私钥解密解码成 [PrivateKey](x509_package_interfaces.md#interface-privatekey) 对象，密码为 None 时则不解密。

参数：

- text: String - PEM 格式的私钥。
- password!: ?String - 解密密码。

返回值：

- [PrivateKey](x509_package_interfaces.md#interface-privatekey) - 解密解码后的私钥对象。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 解密解码失败，或者`password`为空字符串。

### func encodeToDer(?String)

```cangjie
func encodeToDer(password!: ?String): DerBlob
```

功能：将私钥加密编码成 DER 格式，密码为 None 时则不加密。

参数：

- password!: ?String - 加密密码。

返回值：

- [DerBlob](x509_package_structs.md#struct-derblob) - 加密后的 DER 格式的私钥。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 加密失败，或者`password`为空字符串。

### func encodeToPem()

```cangjie
override func encodeToPem(): PemEntry
```

功能：将私钥编码成 PEM 格式。

返回值：

- [PemEntry](x509_package_structs.md#struct-pementry) - 编码后的 PEM 格式的私钥。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 编码失败。

### func encodeToPem(?String)

```cangjie
func encodeToPem(password!: ?String): PemEntry
```

功能：将私钥加密编码成 PEM 格式，密码为 None 时则不加密。

参数：

- password!: ?String - 加密密码。

返回值：

- [PemEntry](x509_package_structs.md#struct-pementry) - 加密后的 PEM 格式的私钥。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 加密失败，或者`password`为空字符串。

## interface PublicKey

```cangjie
public interface PublicKey <: Key {
    override func encodeToPem(): PemEntry
    static func decodeDer(blob: DerBlob): PublicKey
    static func decodeFromPem(text: String): PublicKey
}
```

功能：公钥接口。

父类型：

- [Key](#interface-key)

### static func decodeDer(DerBlob)

```cangjie
static func decodeDer(blob: DerBlob): PublicKey
```

功能：将公钥从 DER 格式解码。

参数：

- blob: [DerBlob](x509_package_structs.md#struct-derblob) - DER 格式的公钥对象。

返回值：

- [PublicKey](x509_package_interfaces.md#interface-publickey) - 由 DER 格式解码出的公钥。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 当 DER 格式的公钥内容不正确，无法解析时抛出异常。

### static func decodeFromPem(String)

```cangjie
static func decodeFromPem(text: String): PublicKey
```

功能：将公钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的公钥字符流。

返回值：

- [PublicKey](x509_package_interfaces.md#interface-publickey) - 由 PEM 格式解码出的公钥。

异常：

- [X509Exception](x509_package_exceptions.md#class-x509exception) - 字符流不符合 PEM 格式，或文件头不符合公钥头标准时抛出异常。

### func encodeToPem()

```cangjie
override func encodeToPem(): PemEntry
```

功能：将公钥编码为 PEM 格式。

返回值：

- [PemEntry](x509_package_structs.md#struct-pementry) - 公钥数据 PEM 格式编码生成的对象。