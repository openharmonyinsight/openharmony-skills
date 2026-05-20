# 枚举

## enum CertificateVerifyMode

```cangjie
public enum CertificateVerifyMode {
    | CustomCA(Array<X509Certificate>)
    | Default
    | TrustAll
}
```

功能：对证书验证的处理模式。

> **说明：**
>
> CustomCA 模式可使用用户配置的证书地址，适用于用户证书无法设置为系统证书的场景。
>
> 证书认证模式，TCP 连接建立成功后，客户端和服务端可交换证书，Default 模式使用系统证书。
>
> 在开发测试阶段，可使用 TrustAll 模式，该模式表示本端不作对对端证书的校验。此模式本端信任任意建立连接对象，一般仅在开发测试阶段使用。

### CustomCA(Array\<X509Certificate>)

```cangjie
CustomCA(Array<X509Certificate>)
```

功能：表示根据提供的 CA 列表与系统 CA 进行验证。

### Default

```cangjie
Default
```

功能：表示默认验证模式，根据系统 CA 验证证书。

### TrustAll

```cangjie
TrustAll
```

功能：表示信任所有证书。

## enum SignatureAlgorithm

```cangjie
public enum SignatureAlgorithm <: ToString & Equatable<SignatureAlgorithm> {
    | SignatureAndHashAlgorithm(SignatureType, HashType)
    | SignatureScheme(SignatureSchemeType)
}
```

功能：签名算法类型，签名算法用于确保传输数据的身份验证、完整性和真实性。

父类型：

- ToString
- Equatable\<[SignatureAlgorithm](../../../crypto/x509/x509_package_api/x509_package_enums.md#enum-signaturealgorithm)>

### SignatureAndHashAlgorithm(SignatureType, HashType)

```cangjie
SignatureAndHashAlgorithm(SignatureType, HashType)
```

功能：表明哪个签名和哈希算法对会被用于数字签名，自 TLS 1.2 及以后版本，包含签名和哈希算法类型。

### SignatureScheme(SignatureSchemeType)

```cangjie
SignatureScheme(SignatureSchemeType)
```

功能：签名方案，自 TLS 1.3 及以后版本，业界更为推荐的指定签名算法的方式。

### func toString()

```cangjie
public func toString():String
```

功能：转换签名算法的字符串表示。

返回值：

- String - 签名算法名称。

### operator func !=(SignatureAlgorithm)

```cangjie
public operator func !=(other: SignatureAlgorithm) : Bool
```

功能：判断签名算法类型是否不同。

参数：

- other: [SignatureAlgorithm](tls_package_enums.md#enum-signaturealgorithm) - 对比的签名算法类型。

返回值：

- Bool - 不相同返回 `true`；否则，返回 `false`。

### operator func ==(SignatureAlgorithm)

```cangjie
public operator func ==(other: SignatureAlgorithm) : Bool
```

功能：判断签名算法类型是否相同。

参数：

- other: [SignatureAlgorithm](tls_package_enums.md#enum-signaturealgorithm) - 对比的签名算法类型。

返回值：

- Bool - 相同返回 `true`；否则，返回 `false`。

## enum SignatureSchemeType

```cangjie
public enum SignatureSchemeType <: ToString & Equatable<SignatureSchemeType> {
    | RSA_PKCS1_SHA256
    | RSA_PKCS1_SHA384
    | RSA_PKCS1_SHA512
    | ECDSA_SECP256R1_SHA256
    | ECDSA_SECP384R1_SHA384
    | ECDSA_SECP521R1_SHA512
    | RSA_PSS_RSAE_SHA256
    | RSA_PSS_RSAE_SHA384
    | RSA_PSS_RSAE_SHA512
    | ED25519
    | ED448
    | RSA_PSS_PSS_SHA256
    | RSA_PSS_PSS_SHA384
    | RSA_PSS_PSS_SHA512
}
```

功能：加密算法类型，用于保护网络通信的安全性和隐私性。

父类型：

- ToString
- Equatable\<[SignatureSchemeType](#enum-signatureschemetype)>

### ECDSA_SECP256R1_SHA256

```cangjie
ECDSA_SECP256R1_SHA256
```

功能：创建一个 `ECDSA_SECP256R1_SHA256` 类型的枚举实例，表示加密算法类型使用 `ECDSA_SECP256R1_SHA256`。

### ECDSA_SECP384R1_SHA384

```cangjie
ECDSA_SECP384R1_SHA384
```

功能：创建一个 `ECDSA_SECP384R1_SHA384` 类型的枚举实例，表示加密算法类型使用 `ECDSA_SECP384R1_SHA384`。

### ECDSA_SECP521R1_SHA512

```cangjie
ECDSA_SECP521R1_SHA512
```

功能：创建一个 `ECDSA_SECP521R1_SHA512` 类型的枚举实例，表示加密算法类型使用 `ECDSA_SECP521R1_SHA512`。

### ED25519

```cangjie
ED25519
```

功能：创建一个 `ED25519` 类型的枚举实例，表示加密算法类型使用 ED25519。

### ED448

```cangjie
ED448
```

功能：创建一个 `ED448` 类型的枚举实例，表示加密算法类型使用 ED448。

### RSA_PKCS1_SHA256

```cangjie
RSA_PKCS1_SHA256
```

功能：创建一个 `RSA_PKCS1_SHA256` 类型的枚举实例，表示加密算法类型使用 `RSA_PKCS1_SHA256`。

### RSA_PKCS1_SHA384

```cangjie
RSA_PKCS1_SHA384
```

功能：创建一个 `RSA_PKCS1_SHA384` 类型的枚举实例，表示加密算法类型使用 `RSA_PKCS1_SHA384`。

### RSA_PKCS1_SHA512

```cangjie
RSA_PKCS1_SHA512
```

功能：创建一个 `RSA_PKCS1_SHA512` 类型的枚举实例，表示加密算法类型使用 `RSA_PKCS1_SHA512`。

### RSA_PSS_PSS_SHA256

```cangjie
RSA_PSS_PSS_SHA256
```

功能：创建一个 `RSA_PSS_PSS_SHA256` 类型的枚举实例，表示加密算法类型使用 `RSA_PSS_PSS_SHA256`。

### RSA_PSS_PSS_SHA384

```cangjie
RSA_PSS_PSS_SHA384
```

功能：创建一个 `RSA_PSS_PSS_SHA384` 类型的枚举实例，表示加密算法类型使用 `RSA_PSS_PSS_SHA384`。

### RSA_PSS_PSS_SHA512

```cangjie
RSA_PSS_PSS_SHA512
```

功能：创建一个 `RSA_PSS_PSS_SHA512` 类型的枚举实例，表示加密算法类型使用 `RSA_PSS_PSS_SHA512`。

### RSA_PSS_RSAE_SHA256

```cangjie
RSA_PSS_RSAE_SHA256
```

功能：创建一个 `RSA_PSS_RSAE_SHA256` 类型的枚举实例，表示加密算法类型使用 `RSA_PSS_RSAE_SHA256`。

### RSA_PSS_RSAE_SHA384

```cangjie
RSA_PSS_RSAE_SHA384
```

功能：创建一个 `RSA_PSS_RSAE_SHA384` 类型的枚举实例，表示加密算法类型使用 `RSA_PSS_RSAE_SHA384`。

### RSA_PSS_RSAE_SHA512

```cangjie
RSA_PSS_RSAE_SHA512
```

功能：创建一个 `RSA_PSS_RSAE_SHA512` 类型的枚举实例，表示加密算法类型使用 `RSA_PSS_RSAE_SHA384`。

### func toString()

```cangjie
public func toString(): String
```

功能：加密算法类型的字符串表示。

如 `RSA_PKCS1_SHA256` 的字符串表示为 "rsa_pkcs1_sha256"。

返回值：

- String - 加密算法类型的字符串表示。

### operator func !=(SignatureSchemeType)

```cangjie
public operator func !=(other: SignatureSchemeType): Bool
```

功能：判断两者是否为不同加密算法类型。

参数：

- other: [SignatureSchemeType](tls_package_enums.md#enum-signatureschemetype) - 对比的加密算法类型。

返回值：

- Bool - 不相同返回 true；否则，返回 false。

### operator func ==(SignatureSchemeType)

```cangjie
public operator func ==(other: SignatureSchemeType): Bool
```

功能：判断两者是否为同一加密算法类型。

参数：

- other: [SignatureSchemeType](tls_package_enums.md#enum-signatureschemetype) - 对比的加密算法类型。

返回值：

- Bool - 相同返回 true；否则，返回 false。

## enum SignatureType

```cangjie
public enum SignatureType <: ToString & Equatable<SignatureType> {
    | DSA
    | ECDSA
    | RSA
}
```

功能：签名算法类型，用于认证真实性。参见 [RFC5246 7.4.1.4.1](https://www.rfc-editor.org/rfc/rfc5246.html#section-7.4.1.4.1) 章节。

父类型：

- ToString
- Equatable\<[SignatureType](#enum-signaturetype)>

### DSA

```cangjie
DSA
```

功能：创建一个 `DSA` 类型的枚举实例，表示采用数字签名算法。

### ECDSA

```cangjie
ECDSA
```

功能：创建一个 `ECDSA` 类型的枚举实例，表示采用椭圆曲线数字签名算法。

### RSA

```cangjie
RSA
```

功能：创建一个 `RSA` 类型的枚举实例，表示采用 RSA 加密算法。

### func toString()

```cangjie
public func toString(): String
```

功能：转换为签名算法的字符串表示。

返回值：

- String - 签名算法的名称。

### operator func !=(SignatureType)

```cangjie
public operator func !=(other: SignatureType) : Bool
```

功能：判断两者是否为不同的签名算法。

参数：

- other: [SignatureType](tls_package_enums.md#enum-signaturetype) - 对比的签名算法类型。

返回值：

- Bool - 不相同返回 `true`；否则，返回 `false`。

### operator func ==(SignatureType)

```cangjie
public operator func ==(other: SignatureType) : Bool
```

功能：判断两者是否为相同的签名算法。

参数：

- other: [SignatureType](tls_package_enums.md#enum-signaturetype) - 对比的签名算法类型。

返回值：

- Bool - 相同返回 `true`；否则，返回 `false`。

## enum TlsClientIdentificationMode

```cangjie
public enum TlsClientIdentificationMode {
    | Disabled
    | Optional
    | Required
}
```

功能：服务端对客户端证书的认证模式。

### Disabled

```cangjie
Disabled
```

功能：表示服务端不校验客户端证书，客户端可以不发送证书和公钥，即单向认证。

### Optional

```cangjie
Optional
```

功能：表示服务端校验客户端证书，但客户端可以不提供证书及公钥，不提供时则单向认证，提供时则为双向认证。

### Required

```cangjie
Required
```

功能：表示服务端校验客户端证书，并且要求客户端必须提供证书和公钥，即双向认证。

## enum TlsVersion

```cangjie
public enum TlsVersion <: ToString {
    | V1_2
    | V1_3
    | Unknown
}
```

功能：TLS 协议版本。

父类型：

- ToString

### Unknown

```cangjie
Unknown
```

功能：表示未知协议版本。

### V1_2

```cangjie
V1_2
```

功能：表示 TLS 1.2 版本。

### V1_3

```cangjie
V1_3
```

功能：表示 TLS 1.3 版本。

### func toString()

```cangjie
public override func toString(): String
```

功能：返回当前 [TlsVersion](tls_package_enums.md#enum-tlsversion) 的字符串表示。

返回值：

- String - 当前 [TlsVersion](tls_package_enums.md#enum-tlsversion) 的字符串表示。