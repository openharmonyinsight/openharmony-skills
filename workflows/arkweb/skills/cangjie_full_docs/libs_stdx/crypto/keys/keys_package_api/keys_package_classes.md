# 类

## class ECDSAPrivateKey

```cangjie
public class ECDSAPrivateKey <: PrivateKey {
    public init(curve: Curve)
}
```

功能：ECDSA 私钥类，提供生成 ECDSA 私钥能力，ECDSA 的私钥支持签名操作，同时支持 PEM 和 DER 格式的编码解码。使用示例见 [ECDSA 密钥示例](../keys_samples/sample_keys.md#ecdsa-密钥示例)。

父类型：

- [PrivateKey](../../x509/x509_package_api/x509_package_interfaces.md#interface-privatekey)

### init(Curve)

```cangjie
public init(curve: Curve)
```

功能：init 初始化生成私钥。

参数：

- curve: [Curve](keys_package_enums.md#enum-curve) - 椭圆曲线类型。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 初始化失败，抛出异常。

### static func decodeDer(DerBlob)

```cangjie
public static func decodeDer(blob: DerBlob): ECDSAPrivateKey
```

功能：将私钥从 DER 格式解码。

参数：

- blob: [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 二进制格式的私钥对象。

返回值：

- [ECDSAPrivateKey](keys_package_classes.md#class-ecdsaprivatekey) - 解码出的 ECDSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败，抛出异常。

### static func decodeDer(DerBlob, ?String)

```cangjie
public static func decodeDer(blob: DerBlob, password!: ?String): ECDSAPrivateKey
```

功能：将加密的私钥从 DER 格式解码。

参数：

- blob: [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 二进制格式的私钥对象。
- password!: ?String - 解密私钥需要提供的密码，密码为 None 时则不解密。

返回值：

- [ECDSAPrivateKey](keys_package_classes.md#class-ecdsaprivatekey) - 解码出的 ECDSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、解密失败或者参数密码为空字符串，抛出异常。

### static func decodeFromPem(String)

```cangjie
public static func decodeFromPem(text: String): ECDSAPrivateKey
```

功能：将私钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的私钥字符流。

返回值：

- [ECDSAPrivateKey](keys_package_classes.md#class-ecdsaprivatekey) - 解码出的 ECDSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、字符流不符合 PEM 格式或文件头不符合私钥头标准时，抛出异常。

### static func decodeFromPem(String, ?String)

```cangjie
public static func decodeFromPem(text: String, password!: ?String): ECDSAPrivateKey
```

功能：将私钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的私钥字符流。
- password!: ?String - 解密私钥需要提供的密码，密码为 None 时则不解密。

返回值：

- [ECDSAPrivateKey](keys_package_classes.md#class-ecdsaprivatekey) - 解码出的 ECDSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、解密失败、参数密码为空字符串、字符流不符合 PEM 格式或文件头不符合私钥头标准时，抛出异常。

### func encodeToDer()

```cangjie
public override func encodeToDer(): DerBlob
```

功能：将私钥编码为 DER 格式。

返回值：

- [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 编码后的 Der 格式私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func encodeToDer(?String)

```cangjie
public func encodeToDer(password!: ?String): DerBlob
```

功能：使用 AES-256-CBC 加密私钥，将私钥编码为 DER 格式。

参数：

- password!: ?String - 加密私钥需要提供的密码，密码为 None 时则不加密。

返回值：

- [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 编码后的 DER 格式私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败、加密失败或者参数密码为空字符串，抛出异常。

### func encodeToPem()

```cangjie
public override func encodeToPem(): PemEntry
```

功能：将私钥编码为 PEM 格式。

返回值：

- [PemEntry](../../x509/x509_package_api/x509_package_structs.md#struct-pementry) - 私钥 PEM 格式的对象。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func sign(Array\<Byte>)

```cangjie
public func sign(digest: Array<Byte>): Array<Byte>
```

功能：sign 对数据的摘要结果进行签名。

参数：

- digest: Array\<Byte> - 数据的摘要结果。

返回值：

- Array\<Byte> - 签名后的数据。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 签名失败，抛出异常。

### func toString()

```cangjie
public override func toString(): String
```

功能：输出私钥种类。

返回值：

- String - 密钥类别描述。

## class ECDSAPublicKey

```cangjie
public class ECDSAPublicKey <: PublicKey {
    public init(pri: ECDSAPrivateKey)
}
```

功能：ECDSA 公钥类，提供生成 ECDSA 公钥能力，ECDSA 公钥支持验证签名操作，支持 PEM 和 DER 格式的编码解码。使用示例见 [ECDSA 密钥示例](../keys_samples/sample_keys.md#ecdsa-密钥示例)。

父类型：

- [PublicKey](../../x509/x509_package_api/x509_package_interfaces.md#interface-publickey)

### init(ECDSAPrivateKey)

```cangjie
public init(pri: ECDSAPrivateKey)
```

功能：init 初始化公钥，从私钥中获取对应的公钥。

参数：

- pri: [ECDSAPrivateKey](keys_package_classes.md#class-ecdsaprivatekey) - ECDSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 初始化失败，抛出异常。

### static func decodeDer(DerBlob)

```cangjie
public static func decodeDer(blob: DerBlob): ECDSAPublicKey
```

功能：将公钥从 DER 格式解码。

参数：

- blob: [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 二进制格式的公钥对象。

返回值：

- [ECDSAPublicKey](keys_package_classes.md#class-ecdsapublickey) - 解码出的 ECDSA 公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### static func decodeFromPem(String)

```cangjie
public static func decodeFromPem(text: String): ECDSAPublicKey
```

功能：将公钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的公钥字符流。

返回值：

- [ECDSAPublicKey](keys_package_classes.md#class-ecdsapublickey) - 解码出的 ECDSA 公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、字符流不符合 PEM 格式或文件头不符合公钥头标准时，抛出异常。

### func encodeToDer()

```cangjie
public override func encodeToDer(): DerBlob
```

功能：将公钥编码为 DER 格式。

返回值：

- [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 编码后的 Der 格式公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func encodeToPem()

```cangjie
public override func encodeToPem(): PemEntry
```

功能：将公钥编码为 PEM 格式。

返回值：

- [PemEntry](../../x509/x509_package_api/x509_package_structs.md#struct-pementry) 对象。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func toString()

```cangjie
public override func toString(): String
```

功能：输出公钥种类。

返回值：

- String - 密钥类别描述。

### func verify(Array\<Byte>, Array\<Byte>)

```cangjie
public func verify(digest: Array<Byte>, sig: Array<Byte>): Bool
```

功能：verify 验证签名结果。

参数：

- digest: Array\<Byte> - 数据的摘要结果。
- sig: Array\<Byte> - 数据的签名结果。

返回值：

- Bool - 返回 true 表示验证成功，false 失败。

## class RSAPrivateKey

```cangjie
public class RSAPrivateKey <: PrivateKey{
    public init(bits: Int32)
    public init(bits: Int32, e: BigInt)
}
```

功能：RSA 私钥类，提供生成 RSA 私钥能力，RSA 私钥支持签名和解密操作，支持 PEM 和 DER 格式的编码解码，符合 PKCS1 标准。使用示例见 [RSA 密钥示例](../keys_samples/sample_keys.md#rsa-密钥示例)。

父类型：

- [PrivateKey](../../x509/x509_package_api/x509_package_interfaces.md#interface-privatekey)

### init(Int32)

```cangjie
public init(bits: Int32)
```

功能：init 初始化生成私钥，公钥指数默认值为 65537，业界推荐。公钥指数 e 的大小直接影响了 RSA 算法的安全性和加密效率。通常情况下，e 的值越小，加密速度越快，但安全性越低。

参数：

- bits: Int32 - 密钥长度，需要大于等于 512 位，并且小于等于 16384 位。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 密钥长度不符合要求或初始化失败，抛出异常。

### init(Int32, BigInt)

```cangjie
public init(bits: Int32, e: BigInt)
```

功能：init 初始化生成私钥，允许用户指定公共指数。

参数：

- bits: Int32 - 密钥长度，需要大于等于 512 位，并且小于等于 16384 位，推荐使用的密钥长度不小于 3072 位。
- e: BigInt - 公钥公共指数，范围是 [3, 2^256-1] 的奇数。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 密钥长度不符合要求、公钥公共指数值不符合要求或初始化失败，抛出异常。

### static func decodeDer(DerBlob)

```cangjie
public static func decodeDer(blob: DerBlob): RSAPrivateKey
```

功能：将私钥从 DER 格式解码。

参数：

- blob: [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 二进制格式的私钥对象。

返回值：

- [RSAPrivateKey](keys_package_classes.md#class-rsaprivatekey) - 解码出的 RSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败，抛出异常。

### static func decodeDer(DerBlob, ?String)

```cangjie
public static func decodeDer(blob: DerBlob, password!: ?String): RSAPrivateKey
```

功能：将加密的私钥从 DER 格式解码。

参数：

- blob: [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 二进制格式的私钥对象。
- password!: ?String - 解密私钥需要提供的密码，密码为 None 时则不解密。

返回值：

- [RSAPrivateKey](keys_package_classes.md#class-rsaprivatekey) - 解码出的 RSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、解密失败或者参数密码为空字符串，抛出异常。

### static func decodeFromPem(String)

```cangjie
public static func decodeFromPem(text: String): RSAPrivateKey
```

功能：将私钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的私钥字符流。

返回值：

- [RSAPrivateKey](keys_package_classes.md#class-rsaprivatekey) - 解码出的 RSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、解密失败、字符流不符合 PEM 格式或文件头不符合私钥头标准时，抛出异常。

### static func decodeFromPem(String, ?String)

```cangjie
public static func decodeFromPem(text: String, password!: ?String): RSAPrivateKey
```

功能：将私钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的私钥字符流。
- password!: ?String - 解密私钥需要提供的密码，密码为 None 时则不解密。

返回值：

- [RSAPrivateKey](keys_package_classes.md#class-rsaprivatekey) - 解码出的 RSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、解密失败、参数密码为空字符串、字符流不符合 PEM 格式或文件头不符合私钥头标准时，抛出异常。

### func decrypt(InputStream, OutputStream, PadOption)

```cangjie
public func decrypt(input: InputStream, output: OutputStream, padType!: PadOption): Unit
```

功能：decrypt 解密出原始数据。

参数：

- input: InputStream - 加密的数据。
- output: OutputStream - 解密后的数据。
- padType!: [PadOption](keys_package_enums.md#enum-padoption) - 填充模式，可以选择 PKCS1 或 OAEP 模式，不支持 PSS 模式，在对安全场景要求较高的情况下，推荐使用 OAEP 填充模式。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 设置填充模式失败或解密失败，抛出异常。

### func encodeToDer()

```cangjie
public override func encodeToDer(): DerBlob
```

功能：将私钥编码为 DER 格式。

返回值：

- [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 编码后的 DER 格式私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func encodeToDer(?String)

```cangjie
public func encodeToDer(password!: ?String): DerBlob
```

功能：使用 AES-256-CBC 加密私钥，将私钥编码为 DER 格式。

参数：

- password!: ?String - 加密私钥需要提供的密码，密码为 None 时则不加密。

返回值：

- [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 编码后的 DER 格式私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败、加密失败或者参数密码为空字符串，抛出异常。

### func encodeToPem()

```cangjie
public override func encodeToPem(): PemEntry
```

功能：将私钥编码为 PEM 格式。

返回值：

- [PemEntry](../../x509/x509_package_api/x509_package_structs.md#struct-pementry) - 私钥 PEM 格式的对象。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func sign(Digest, Array\<Byte>, PadOption)

```cangjie
public func sign(hash: Digest, digest: Array<Byte>, padType!: PadOption): Array<Byte>
```

功能：对数据的摘要结果进行签名。

参数：

- hash: Digest - 摘要方法，获取 digest 结果使用的摘要方法。
- digest: Array\<Byte> - 数据的摘要结果。
- padType!: [PadOption](keys_package_enums.md#enum-padoption) - 填充模式，可以选择 PKCS1 或 PSS 模式，不支持 OAEP 模式，在对安全场景要求较高的情况下，推荐使用 PSS 填充模式。

返回值：

- Array\<Byte> - 签名后的数据。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 设置摘要方法失败、设置填充模式失败或签名失败，抛出异常。

### func toString()

```cangjie
public override func toString(): String
```

功能：输出私钥种类。

返回值：

- String - 密钥类别描述。

## class RSAPublicKey

```cangjie
public class RSAPublicKey <: PublicKey {
    public init(pri: RSAPrivateKey)
}
```

功能：RSA 公钥类，提供生成 RSA 公钥能力，RSA 公钥支持验证签名和加密操作，支持 PEM 和 DER 格式的编码解码。使用示例见 [RSA 密钥示例](../keys_samples/sample_keys.md#rsa-密钥示例)。

父类型：

- [PublicKey](../../x509/x509_package_api/x509_package_interfaces.md#interface-publickey)

### init(RSAPrivateKey)

```cangjie
public init(pri: RSAPrivateKey)
```

功能：init 初始化公钥，从私钥中获取对应的公钥。

参数：

- pri: [RSAPrivateKey](keys_package_classes.md#class-rsaprivatekey) - RSA 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 初始化失败，抛出异常。

### static func decodeDer(DerBlob)

```cangjie
public static func decodeDer(blob: DerBlob): RSAPublicKey
```

功能：将公钥从 DER 格式解码。

参数：

- blob: [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 二进制格式的公钥对象。

返回值：

- [RSAPublicKey](keys_package_classes.md#class-rsapublickey) - 解码出的 RSA 公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败，抛出异常。

### static func decodeFromPem(String)

```cangjie
public static func decodeFromPem(text: String): RSAPublicKey
```

功能：将公钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的公钥字符流。

返回值：

- [RSAPublicKey](keys_package_classes.md#class-rsapublickey) - 解码出的 RSA 公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、字符流不符合 PEM 格式或文件头不符合公钥头标准时，抛出异常。

### func encodeToDer()

```cangjie
public override func encodeToDer(): DerBlob
```

功能：将公钥编码为 DER 格式。

返回值：

- [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 编码后的 Der 格式公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func encodeToPem()

```cangjie
public override func encodeToPem(): PemEntry
```

功能：将公钥编码为 PEM 格式。

返回值：

- [PemEntry](../../x509/x509_package_api/x509_package_structs.md#struct-pementry) 对象。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func encrypt(InputStream, OutputStream, PadOption)

```cangjie
public func encrypt(input: InputStream, output: OutputStream, padType!: PadOption): Unit
```

功能：encrypt 给一段数据进行加密。

参数：

- input: InputStream - 需要加密的数据。
- output: OutputStream - 加密后的数据。
- padType!: [PadOption](keys_package_enums.md#enum-padoption) - 填充模式，可以选择 PKCS1 或 OAEP 模式，不支持 PSS 模式，在对安全场景要求较高的情况下，推荐使用 OAEP 填充模式。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 设置填充模式失败或加密失败，抛出异常。

### func toString()

```cangjie
public override func toString(): String
```

功能：输出公钥种类。

返回值：

- String - 密钥类别描述。

### func verify(Digest, Array\<Byte>, Array\<Byte>, PadOption)

```cangjie
public func verify(hash: Digest, digest: Array<Byte>, sig: Array<Byte>, padType!: PadOption): Bool
```

功能：verify 验证签名结果。

参数：

- hash: Digest  - 摘要方法，获取 digest 结果使用的摘要方法。
- digest: Array\<Byte> - 数据的摘要结果。
- sig: Array\<Byte> - 数据的签名结果。
- padType!: [PadOption](keys_package_enums.md#enum-padoption) - 填充模式，可以选择 PKCS1 或 PSS 模式，不支持 OAEP 模式，在对安全场景要求较高的情况下，推荐使用 PSS 填充模式。

返回值：

- Bool - 返回 true 表示验证成功，false 失败。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 设置填充模式失败或验证失败，抛出异常。

## class SM2PrivateKey

```cangjie
public class SM2PrivateKey <: PrivateKey {
    public init()
}
```

功能：SM2 私钥类，提供生成 SM2 私钥能力，SM2 私钥支持签名和解密操作，支持 PEM 和 DER 格式的编码解码，符合 PKCS1 标准。使用示例见 [SM2 密钥示例](../keys_samples/sample_keys.md#sm2-密钥示例)。

父类型：

- [PrivateKey](../../x509/x509_package_api/x509_package_interfaces.md#interface-privatekey)

### init()

```cangjie
public init()
```

功能：init 初始化生成私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 初始化失败，抛出异常。

### static func decodeDer(DerBlob)

```cangjie
public static func decodeDer(blob: DerBlob): SM2PrivateKey
```

功能：将私钥从 DER 格式解码。

参数：

- blob: [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 二进制格式的私钥对象。

返回值：

- [SM2PrivateKey](keys_package_classes.md#class-sm2privatekey) - 解码出的 SM2 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败，抛出异常。

### static func decodeDer(DerBlob, ?String)

```cangjie
public static func decodeDer(blob: DerBlob, password!: ?String): SM2PrivateKey
```

功能：将加密的私钥从 DER 格式解码。

参数：

- blob: [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 二进制格式的私钥对象。
- password!: ?String - 解密私钥需要提供的密码，密码为 None 时则不解密。

返回值：

- [SM2PrivateKey](keys_package_classes.md#class-sm2privatekey) - 解码出的 SM2 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、解密失败或者参数密码为空字符串，抛出异常。

### static func decodeFromPem(String)

```cangjie
public static func decodeFromPem(text: String): SM2PrivateKey
```

功能：将私钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的私钥字符流。

返回值：

- [SM2PrivateKey](keys_package_classes.md#class-sm2privatekey) - 解码出的 SM2 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、解密失败、字符流不符合 PEM 格式或文件头不符合私钥头标准时，抛出异常。

### static func decodeFromPem(String, ?String)

```cangjie
public static func decodeFromPem(text: String, password!: ?String): SM2PrivateKey
```

功能：将私钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的私钥字符流。
- password!: ?String - 解密私钥需要提供的密码，密码为 None 时则不解密。

返回值：

- [SM2PrivateKey](keys_package_classes.md#class-sm2privatekey) - 解码出的 SM2 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、解密失败、参数密码为空字符串、字符流不符合 PEM 格式或文件头不符合私钥头标准时，抛出异常。

### func decrypt(Array\<Byte>)

```cangjie
public func decrypt(input: Array<Byte>): Array<Byte>
```

功能：decrypt 解密出原始数据，待解密密文需要遵循 ASN.1 编码规则。

参数：

- input: Array\<Byte> - 加密的数据。

返回值：

- Array\<Byte> - 解密后的数据。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解密失败，抛出异常。

### func encodeToDer()

```cangjie
public func encodeToDer(): DerBlob
```

功能：将私钥编码为 DER 格式。

返回值：

- [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 编码后的 DER 格式私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func encodeToDer(?String)

```cangjie
public func encodeToDer(password!: ?String): DerBlob
```

功能：使用 AES-256-CBC 加密私钥，将私钥编码为 DER 格式。

参数：

- password!: ?String - 加密私钥需要提供的密码，密码为 None 时则不加密。

返回值：

- [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 编码后的 DER 格式公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败、加密失败或者参数密码为空字符串，抛出异常。

### func encodeToPem(?String)

```cangjie
public func encodeToPem(password!: ?String): PemEntry
```

功能：将加密的私钥编码为 PEM 格式。

参数：

- password!: ?String - 加密私钥需要提供的密码，密码为 None 时则不加密。

返回值：

- [PemEntry](../../x509/x509_package_api/x509_package_structs.md#struct-pementry) - 私钥 PEM 格式的对象。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败、加密失败或者参数密码为空字符串，抛出异常。

### func encodeToPem()

```cangjie
public func encodeToPem(): PemEntry
```

功能：将私钥编码为 PEM 格式。

返回值：

- [PemEntry](../../x509/x509_package_api/x509_package_structs.md#struct-pementry) - 私钥 PEM 格式的对象。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func sign(Array\<Byte>)

```cangjie
public func sign(data: Array<Byte>): Array<Byte>
```

功能：sign 对数据进行签名，SM2 采用 [SM3](../../digest/digest_package_api/digest_package_classes.md#class-sm3) 数据摘要算法。

参数：

- data: Array\<Byte> - 数据。

返回值：

- Array\<Byte> - 签名后的数据。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 签名失败，抛出异常。

### func toString()

```cangjie
public override func toString(): String
```

功能：输出私钥种类。

返回值：

- String - 密钥类别描述。

## class SM2PublicKey

```cangjie
public class SM2PublicKey <: PublicKey {
    public init(pri: SM2PrivateKey)
}
```

功能：SM2 公钥类，提供生成 SM2 公钥能力，SM2 公钥支持验证签名和加密操作，支持 PEM 和 DER 格式的编码解码。使用示例见 [SM2 密钥示例](../keys_samples/sample_keys.md#sm2-密钥示例)。

父类型：

- [PublicKey](../../x509/x509_package_api/x509_package_interfaces.md#interface-publickey)

### init(SM2PrivateKey)

```cangjie
public init(pri: SM2PrivateKey)
```

功能：init 初始化公钥，从私钥中获取对应的公钥。

参数：

- pri: [SM2PrivateKey](keys_package_classes.md#class-sm2privatekey) - SM2 私钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 初始化失败，抛出异常。

### static func decodeDer(DerBlob)

```cangjie
public static func decodeDer(blob: DerBlob): SM2PublicKey
```

功能：将公钥从 DER 格式解码。

参数：

- blob: [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 二进制格式的公钥对象。

返回值：

- [SM2PublicKey](keys_package_classes.md#class-sm2publickey) - 解码出的 SM2 公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败，抛出异常。

### static func decodeFromPem(String)

```cangjie
public static func decodeFromPem(text: String): SM2PublicKey
```

功能：将公钥从 PEM 格式解码。

参数：

- text: String - PEM 格式的公钥字符流。

返回值：

- [SM2PublicKey](keys_package_classes.md#class-sm2publickey) - 解码出的 SM2 公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解码失败、字符流不符合 PEM 格式或文件头不符合公钥头标准时，抛出异常。

### func encodeToDer()

```cangjie
public func encodeToDer(): DerBlob
```

功能：将公钥编码为 DER 格式。

返回值：

- [DerBlob](../../x509/x509_package_api/x509_package_structs.md#struct-derblob) - 编码后的 Der 格式公钥。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func encodeToPem()

```cangjie
public func encodeToPem(): PemEntry
```

功能：将公钥编码为 PEM 格式。

返回值：

- [PemEntry](../../x509/x509_package_api/x509_package_structs.md#struct-pementry) 对象。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 编码失败，抛出异常。

### func encrypt(Array\<Byte>)

```cangjie
public func encrypt(input: Array<Byte>): Array<Byte>
```

功能：encrypt 给一段数据进行加密，输出密文遵循 ASN.1 编码规则。

参数：

- input: Array\<Byte> - 需要加密的数据。

返回值：

- Array\<Byte> - 加密后的数据。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 加密失败，抛出异常。

### func toString()

```cangjie
public override func toString(): String
```

功能：输出公钥种类。

返回值：

- String - 密钥类别描述。

### func verify(Array\<Byte>, Array\<Byte>)

```cangjie
public func verify(data: Array<Byte>, sig: Array<Byte>): Bool
```

功能：verify 验证签名结果。

参数：

- data: Array\<Byte> - 数据。
- sig: Array\<Byte> - 数据的签名结果。

返回值：

- Bool - 返回 true 表示验证成功，false 失败。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 设置填充模式失败或验证失败，抛出异常。
