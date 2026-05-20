# 结构体

## struct CipherSuite

```cangjie
public struct CipherSuite <: ToString & Equatable<CipherSuite>
```

功能：TLS 中的密码套件。

父类型：

- ToString
- Equatable\<[CipherSuite](#struct-ciphersuite)>

### static prop allSupported

```cangjie
public static prop allSupported: Array<CipherSuite>
```

功能：返回所有支持的密码套件。

返回值：存放密码套件的数组。

类型：Array\<[CipherSuite](tls_package_structs.md#struct-ciphersuite)>

### func toString()

```cangjie
public func toString(): String
```

功能：返回密码套件名称。

返回值：

- String - 密码套件名称。

### operator func !=(CipherSuite)

```cangjie
public operator func !=(that: CipherSuite): Bool
```

功能：判断两个密码套件是否不等。

参数：

- that: [CipherSuite](tls_package_structs.md#struct-ciphersuite) - 被比较的密码套件对象。

返回值：

- Bool - 若不等，则返回 `true`；反之，返回 `false`。

### operator func ==(CipherSuite)

```cangjie
public operator func ==(that: CipherSuite): Bool
```

功能：判断两个密码套件是否相等。

参数：

- that: [CipherSuite](tls_package_structs.md#struct-ciphersuite) - 被比较的密码套件对象。

返回值：

- Bool - 若相等，则返回 `true`；反之，返回 `false`。

## struct TlsClientConfig

```cangjie
public struct TlsClientConfig {
    public var keylogCallback: ?(TlsSocket, String) -> Unit = None
    public var verifyMode: CertificateVerifyMode = CertificateVerifyMode.Default
    public init()
}
```

功能：客户端配置。

### var keylogCallback

```cangjie
public var keylogCallback: ?(TlsSocket, String) -> Unit = None
```

功能：握手过程的回调函数，提供 TLS 初始秘钥数据，用于调试和解密记录使用。

类型：?([TlsSocket](tls_package_classes.md#class-tlssocket), String) -> Unit

### var verifyMode

```cangjie
public var verifyMode: CertificateVerifyMode = CertificateVerifyMode.Default
```

功能：设置或获取证书的认证模式，默认为 `Default`。

类型：[CertificateVerifyMode](tls_package_enums.md#enum-certificateverifymode)

### prop alpnProtocolsList

```cangjie
public mut prop alpnProtocolsList: Array<String>
```

功能：要求的应用层协议名称。若列表为空，则客户端将不协商应用层协议。

类型：Array\<String>

异常：

- IllegalArgumentException - 列表元素有 '\0' 字符时，抛出异常。

### prop cipherSuitesV1_2

```cangjie
public mut prop cipherSuitesV1_2: ?Array<String>
```

功能：基于 TLS 1.2 协议下的加密套。

类型：?Array\<String>

异常：

- IllegalArgumentException - 列表元素有 '\0' 字符时，抛出异常。

### prop cipherSuitesV1_3

```cangjie
public mut prop cipherSuitesV1_3: ?Array<String>
```

功能：基于 TLS 1.3 协议下的加密套。

类型：?Array\<String>

异常：

- IllegalArgumentException - 列表元素有 '\0' 字符时，抛出异常。

### prop clientCertificate

```cangjie
public mut prop clientCertificate: ?(Array<X509Certificate>, PrivateKey)
```

功能：客户端证书和私钥。

类型：?(Array\<[X509Certificate](../../../crypto/x509/x509_package_api/x509_package_classes.md#class-x509certificate)>, PrivateKey)

### prop domain

```cangjie
public mut prop domain: ?String
```

功能：读写要求的服务端主机地址（SNI），`None` 表示不要求。

类型：?String

异常：

- IllegalArgumentException - 参数有 '\0' 字符时，抛出异常。

### prop maxVersion

```cangjie
public mut prop maxVersion: TlsVersion
```

功能：支持的 TLS 最大的版本。

> **注意**
>
> 当仅设置`maxVersion`，而未设置`minVersion`，或设置的`maxVersion`低于`minVersion`，将会在握手阶段抛出 [TlsException](tls_package_exceptions.md#class-tlsexception)。

类型：[TlsVersion](tls_package_enums.md#enum-tlsversion)

### prop minVersion

```cangjie
public mut prop minVersion: TlsVersion
```

功能：支持的 TLS 最小版本。

> **注意**
> 当仅设置`minVersion`，而未设置`maxVersion`，或设置的`minVersion`高于`maxVersion`，将会在握手阶段抛出 [TlsException](tls_package_exceptions.md#class-tlsexception)。

类型：[TlsVersion](tls_package_enums.md#enum-tlsversion)

### prop securityLevel

```cangjie
public mut prop securityLevel: Int32
```

功能：指定客户端的安全级别，默认值为 2，可选参数值在 0-5 内，参数值含义参见 openssl-SSL_CTX_set_security_level 说明。

类型：Int32

### prop signatureAlgorithms

```cangjie
public mut prop signatureAlgorithms: ?Array<SignatureAlgorithm>
```

功能：指定保序的签名和哈希算法。在值为 `None` 或者列表为空时，客户端会使用默认的列表。指定列表后，客户端可能不会发送不合适的签名算法。
参见 [RFC5246 7.4.1.4.1 (TLS 1.2)](https://www.rfc-editor.org/rfc/rfc5246.html#section-7.4.1.4.1) 章节， [RFC8446 4.2.3. (TLS 1.3)](https://www.rfc-editor.org/rfc/rfc8446.html#section-4.2.3) 章节。

类型：?Array\<[SignatureAlgorithm](tls_package_enums.md#enum-signaturealgorithm)>

### init()

```cangjie
public init()
```

功能：构造 [TlsClientConfig](tls_package_structs.md#struct-tlsclientconfig)。

## struct TlsServerConfig

```cangjie
public struct TlsServerConfig {
    public var clientIdentityRequired: TlsClientIdentificationMode = Disabled
    public var keylogCallback: ?(TlsSocket, String) -> Unit = None
    public var verifyMode: CertificateVerifyMode = CertificateVerifyMode.Default
    public init(certChain: Array<X509Certificate>, certKey: PrivateKey)
}
```

功能：服务端配置。

### var clientIdentityRequired

```cangjie
public var clientIdentityRequired: TlsClientIdentificationMode = Disabled
```

功能：设置或获取服务端要求客户端的认证模式，默认值为不要求客户端认证服务端证书，也不要求客户端发送本端证书。

类型：[TlsClientIdentificationMode](tls_package_enums.md#enum-tlsclientidentificationmode)

### var keylogCallback

```cangjie
public var keylogCallback: ?(TlsSocket, String) -> Unit = None
```

功能：握手过程的回调函数，提供 TLS 初始秘钥数据，用于调试和解密记录使用。

类型：?([TlsSocket](tls_package_classes.md#class-tlssocket), String) -> Unit

### var verifyMode

```cangjie
public var verifyMode: CertificateVerifyMode = CertificateVerifyMode.Default
```

功能：设置或获取证书的认证模式，默认认证系统证书

类型：[CertificateVerifyMode](tls_package_enums.md#enum-certificateverifymode)

### prop cipherSuitesV1_2

```cangjie
public mut prop cipherSuitesV1_2: Array<String>
```

功能：基于 TLS 1.2 协议下的加密套。

类型：Array\<String>

异常：

- IllegalArgumentException - 列表元素有 '\0' 字符时，抛出异常。

### prop cipherSuitesV1_3

```cangjie
public mut prop cipherSuitesV1_3: Array<String>
```

功能：基于 TLS 1.3 协议下的加密套。

类型：Array\<String>

异常：

- IllegalArgumentException - 列表元素有 '\0' 字符时，抛出异常。

### prop dhParameters

```cangjie
public mut prop dhParameters: ?DHParameters
```

功能：指定服务端的 DH 密钥参数，默认为 `None`， 默认情况下使用 openssl 自动生成的参数值。

类型：?[DHParameters](../../../crypto/x509/x509_package_api/x509_package_interfaces.md#interface-dhparameters)

### prop maxVersion

```cangjie
public mut prop maxVersion: TlsVersion
```

功能：支持的 TLS 最大版本。

> **注意**
>
> 当仅设置`maxVersion`，而未设置`minVersion`，或设置的`maxVersion`低于`minVersion`，将会在握手阶段抛出 [TlsException](tls_package_exceptions.md#class-tlsexception)。

类型：[TlsVersion](tls_package_enums.md#enum-tlsversion)

### prop minVersion

```cangjie
public mut prop minVersion: TlsVersion
```

功能：支持的 TLS 最小版本。

> **注意**
> 当仅设置`minVersion`，而未设置`maxVersion`，或设置的`minVersion`高于`maxVersion`，将会在握手阶段抛出 [TlsException](tls_package_exceptions.md#class-tlsexception)。

类型：[TlsVersion](tls_package_enums.md#enum-tlsversion)

### prop securityLevel

```cangjie
public mut prop securityLevel: Int32
```

功能：指定服务端的安全级别，默认值为 2，可选参数值在 [0,5] 内，参数值含义参见 [openssl-SSL_CTX_set_security_level](https://www.openssl.org/docs/man1.1.1/man3/SSL_CTX_set_security_level.html) 说明。
功能：指定服务端的安全级别，默认值为 2，可选参数值在 0-5 内，参数值含义参见 openssl-SSL_CTX_set_security_level 说明。

类型：Int32

异常：

- IllegalArgumentException - 当配置值不在 0-5 范围内时，抛出异常。

### prop serverCertificate(Array\<X509Certificate>, PrivateKey)

```cangjie
public mut prop serverCertificate(Array<X509Certificate>, PrivateKey)
```

功能：服务端证书和对应的私钥文件。

类型：(Array\<[X509Certificate](../../../crypto/x509/x509_package_api/x509_package_classes.md#class-x509certificate)>, PrivateKey)。

### prop supportedAlpnProtocols

```cangjie
public mut prop supportedAlpnProtocols: Array<String>
```

功能：应用层协商协议，若客户端尝试协商该协议，服务端将与选取其中相交的协议名称。若客户端未尝试协商协议，则该配置将被忽略。

类型：Array\<String>

异常：

- IllegalArgumentException - 列表元素有 '\0' 字符时，抛出异常。

### init(Array\<X509Certificate>, PrivateKey)

```cangjie
public init(certChain: Array<X509Certificate>, certKey: PrivateKey)
```

功能：构造 [TlsServerConfig](tls_package_structs.md#struct-tlsserverconfig) 对象。

参数：

- certChain: Array\<[X509Certificate](../../../crypto/x509/x509_package_api/x509_package_classes.md#class-x509certificate)> - 证书对象。
- certKey: [PrivateKey](../../../crypto/x509/x509_package_api/x509_package_interfaces.md#interface-privatekey) - 私钥对象。

## struct TlsSession

```cangjie
public struct TlsSession <: Equatable<TlsSession> & ToString & Hashable
```

功能：此结构体表示已建立的客户端会话。此结构体实例用户不可创建，其内部结构对用户不可见。

当客户端 TLS 握手成功后，将会生成一个会话，当连接因一些原因丢失后，客户端可以通过这个会话 id 复用此次会话，省略握手流程。

父类型：

- Equatable\<[TlsSession](#struct-tlssession)>
- ToString
- Hashable

### func hashCode()

```cangjie
public override func hashCode(): Int64
```

功能：生成会话 id 的哈希值。

返回值：

- Int64 - 会话 id 的哈希值。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成会话 id 的字符串。

返回值：

- String - [TlsSession](tls_package_structs.md#struct-tlssession)（会话 id 字符串）。

### operator func !=(TlsSession)

```cangjie
public override operator func !=(other: TlsSession): Bool
```

功能：判断会话 id 是否不同。

参数：

- other: [TlsSession](tls_package_structs.md#struct-tlssession) - 待比较的会话对象。

返回值：

- Bool - 若会话 id 不同，则返回 `true`，否则返回 `false`。

### operator func ==(TlsSession)

```cangjie
public override operator func ==(other: TlsSession): Bool
```

功能：判断会话 id 是否相同。

参数：

- other: [TlsSession](tls_package_structs.md#struct-tlssession) - 待比较的会话对象。

返回值：

- Bool - 若会话 id 相同，则返回 `true`，否则返回 `false`。
