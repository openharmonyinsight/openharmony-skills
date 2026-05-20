# 类

## class X509Certificate

```cangjie
public class X509Certificate <: Equatable<X509Certificate> & Hashable & ToString {
    public init(
        certificateInfo: X509CertificateInfo,
        parent!: X509Certificate,
        publicKey!: PublicKey,
        privateKey!: PrivateKey,
        signatureAlgorithm!: ?SignatureAlgorithm = None
    )
}
```

功能：X509 数字证书是一种用于加密通信的数字证书，它是公钥基础设施（PKI）的核心组件之一。X509 数字证书包含了一个实体的公钥和身份信息，用于验证该实体的身份和确保通信的安全性。

父类型：

- Equatable\<[X509Certificate](#class-x509certificate)>
- Hashable
- ToString

### prop dnsNames

```cangjie
public prop dnsNames: Array<String>
```

功能：解析数字证书备选名称中的域名。

类型：Array\<String>

### prop emailAddresses

```cangjie
public prop emailAddresses: Array<String>
```

功能：解析数字证书备选名称中的 email 地址。

类型：Array\<String>

### prop extKeyUsage

```cangjie
public prop extKeyUsage: ExtKeyUsage
```

功能：解析数字证书中的扩展密钥用法。

类型：[ExtKeyUsage](x509_package_structs.md#struct-extkeyusage)

### prop issuer

```cangjie
public prop issuer: X509Name
```

功能：解析数字证书的颁发者信息。

类型：[X509Name](x509_package_classes.md#class-x509name)

### prop IPAddresses

```cangjie
public prop IPAddresses: Array<IP>
```

功能：解析数字证书备选名称中的 [IP](x509_package_type.md#type-ip) 地址。

类型：Array\<[IP](x509_package_type.md#type-ip)>

### prop keyUsage

```cangjie
public prop keyUsage: KeyUsage
```

功能：解析数字证书中的密钥用法。

类型：[KeyUsage](x509_package_structs.md#struct-keyusage)

### prop notAfter

```cangjie
public prop notAfter: DateTime
```

功能：解析数字证书的有效期截止时间。

类型：DateTime

### prop notBefore

```cangjie
public prop notBefore: DateTime
```

功能：解析数字证书的有效期开始时间。

类型：DateTime

### prop publicKey

```cangjie
public prop publicKey: PublicKey
```

功能：解析数字证书的公钥。

类型：[PublicKey](x509_package_interfaces.md#interface-publickey)

### prop publicKeyAlgorithm

```cangjie
public prop publicKeyAlgorithm: PublicKeyAlgorithm
```

功能：解析数字证书的公钥算法。

类型：[PublicKeyAlgorithm](x509_package_enums.md#enum-publickeyalgorithm)

### prop serialNumber

```cangjie
public prop serialNumber: SerialNumber
```

功能：解析数字证书的序列号。

类型：[SerialNumber](x509_package_structs.md#struct-serialnumber)

### prop signature

```cangjie
public prop signature: Signature
```

功能：解析数字证书的签名。

类型：[Signature](x509_package_structs.md#struct-signature)

### prop signatureAlgorithm

```cangjie
public prop signatureAlgorithm: SignatureAlgorithm
```

功能：解析数字证书的签名算法。

类型：[SignatureAlgorithm](./x509_package_enums.md#enum-signaturealgorithm)

### prop subject

```cangjie
public prop subject: X509Name
```

功能：解析数字证书的使用者信息。

类型：[X509Name](x509_package_classes.md#class-x509name)

### init(X509CertificateInfo, X509Certificate, PublicKey, PrivateKey, ?SignatureAlgorithm)

```cangjie
public init(
    certificateInfo: X509CertificateInfo,
    parent!: X509Certificate,
    publicKey!: PublicKey,
    privateKey!: PrivateKey,
    signatureAlgorithm!: ?SignatureAlgorithm = None
)
```

功能：创建数字证书对象。

参数：

- certificateInfo: [X509CertificateInfo](x509_package_structs.md#struct-x509certificateinfo) - 数字证书配置信息。
- parent!: [X509Certificate](x509_package_classes.md#class-x509certificate) - 颁发者证书。
- publicKey!: [PublicKey](x509_package_interfaces.md#interface-publickey) - 申请人公钥，仅支持 RSA、ECDSA 和 DSA 公钥。
- privateKey!: [PrivateKey](x509_package_interfaces.md#interface-privatekey) - 颁发者私钥，仅支持 RSA、ECDSA 和 DSA 私钥。
- signatureAlgorithm!: ?[SignatureAlgorithm](./x509_package_enums.md#enum-signaturealgorithm) - 证书签名算法，默认值为 None，使用默认值时默认的摘要类型是 [SHA256](../../digest/digest_package_api/digest_package_classes.md#class-sha256)。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 公钥或私钥类型不支持、私钥类型和证书签名算法中的私钥类型不匹配或数字证书信息设置失败时，抛出异常。

### static func decodeFromDer(DerBlob)

```cangjie
public static func decodeFromDer(der: DerBlob): X509Certificate
```

功能：将 DER 格式的数字证书解码。

参数：

- der: [DerBlob](x509_package_structs.md#struct-derblob) - DER 格式的二进制数据。

返回值：

- [X509Certificate](x509_package_classes.md#class-x509certificate) - 由 DER 格式解码出的数字证书。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 数据为空时，或数据不是有效的数字证书 DER 格式时抛出异常。

### static func decodeFromPem(String)

```cangjie
public static func decodeFromPem(pem: String): Array<X509Certificate>
```

功能：将数字证书从 PEM 格式解码。

参数：

- pem: String - PEM 格式的数字证书字符流。

返回值：

- Array\<[X509Certificate](x509_package_classes.md#class-x509certificate)> - 由 PEM 格式解码出的数字证书数组。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 字符流不符合 PEM 格式时，或文件头不符合数字证书头标准时抛出异常。

### func encodeToDer()

```cangjie
public func encodeToDer(): DerBlob
```

功能：将数字证书编码成 Der 格式。

返回值：

- [DerBlob](x509_package_structs.md#struct-derblob) - 编码后的 Der 格式的数字证书。

### func encodeToPem()

```cangjie
public func encodeToPem(): PemEntry
```

功能：将数字证书编码成 PEM 格式。

返回值：

- [PemEntry](x509_package_structs.md#struct-pementry) - 编码后的 PEM 格式的数字证书。

### func hashCode()

```cangjie
public override func hashCode(): Int64
```

功能：返回证书哈希值。

返回值：

- Int64 - 对证书对象进行哈希计算后得到的结果。

### static func systemRootCerts()

```cangjie
public static func systemRootCerts(): Array<X509Certificate>
```

功能：返回操作系统的根证书，支持 Linux，MacOS 和 Windows 平台。

返回值：

- Array\<[X509Certificate](x509_package_classes.md#class-x509certificate)> - 操作系统的根证书链。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成证书名称字符串，包含证书的使用者信息、有效期以及颁发者信息。

返回值：

- String - 证书名称字符串。

### func verify(VerifyOption)

```cangjie
public func verify(verifyOption: VerifyOption): Bool
```

功能：根据验证选项验证当前证书的有效性。

验证优先级：

1. 优先验证有效期；
2. 可选验证 DNS 域名；
3. 最后根据根证书和中间证书验证其有效性。

参数：

- verifyOption: [VerifyOption](x509_package_structs.md#struct-verifyoption) - 证书验证选项。

返回值：

- Bool - 证书有效返回 true，否则返回 false。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 检验过程中失败，比如内存分配异常等内部错误，则抛出异常。

### operator func !=(X509Certificate)

```cangjie
public override operator func !=(other: X509Certificate): Bool
```

功能：判不等。

参数：

- other: [X509Certificate](x509_package_classes.md#class-x509certificate) - 被比较的证书对象。

返回值：

- Bool - 若证书不同，返回 true；否则，返回 false。

### operator func ==(X509Certificate)

```cangjie
public override operator func ==(other: X509Certificate): Bool
```

功能：判等。

参数：

- other: [X509Certificate](x509_package_classes.md#class-x509certificate) - 被比较的证书对象。

返回值：

- Bool - 若证书相同，返回 true；否则，返回 false。

## class X509CertificateRequest

```cangjie
public class X509CertificateRequest <: Hashable & ToString {
    public init(
        privateKey: PrivateKey,
        certificateRequestInfo!: ?X509CertificateRequestInfo = None,
        signatureAlgorithm!: ?SignatureAlgorithm = None
    )
}
```

功能：数字证书签名请求。

父类型：

- Hashable
- ToString

### prop IPAddresses

```cangjie
public prop IPAddresses: Array<IP>
```

功能：解析数字证书签名请求备选名称中的 [IP](x509_package_type.md#type-ip) 地址。

类型：Array\<[IP](x509_package_type.md#type-ip)>

### prop dnsNames

```cangjie
public prop dnsNames: Array<String>
```

功能：解析数字证书签名请求备选名称中的域名。

类型：Array\<String>

### prop emailAddresses

```cangjie
public prop emailAddresses: Array<String>
```

功能：解析数字证书签名请求备选名称中的 email 地址。

类型：Array\<String>

### prop publicKey

```cangjie
public prop publicKey: PublicKey
```

功能：解析数字证书签名请求的公钥。

类型：[PublicKey](x509_package_interfaces.md#interface-publickey)

### prop publicKeyAlgorithm

```cangjie
public prop publicKeyAlgorithm: PublicKeyAlgorithm
```

功能：解析数字证书签名请求的公钥算法。

类型：[PublicKeyAlgorithm](x509_package_enums.md#enum-publickeyalgorithm)

### prop signature

```cangjie
public prop signature: Signature
```

功能：解析数字证书签名请求的签名。

类型：[Signature](x509_package_structs.md#struct-signature)

### prop signatureAlgorithm

```cangjie
public prop signatureAlgorithm: SignatureAlgorithm
```

功能：解析数字证书签名请求的签名算法。

类型：[SignatureAlgorithm](./x509_package_enums.md#enum-signaturealgorithm)

### prop subject

```cangjie
public prop subject: X509Name
```

功能：解析数字证书签名请求的使用者信息。

类型：[X509Name](x509_package_classes.md#class-x509name)

### init(PrivateKey, ?X509CertificateRequestInfo, ?SignatureAlgorithm)

```cangjie
public init(
    privateKey: PrivateKey,
    certificateRequestInfo!: ?X509CertificateRequestInfo = None,
    signatureAlgorithm!: ?SignatureAlgorithm = None
)
```

功能：创建数字证书签名请求对象。

参数：

- privateKey: [PrivateKey](x509_package_interfaces.md#interface-privatekey) - 私钥，仅支持 RSA、ECDSA 和 DSA 私钥。
- certificateRequestInfo!: ?[X509CertificateRequestInfo](x509_package_structs.md#struct-x509certificaterequestinfo) - 数字证书签名信息，默认值为 None。
- signatureAlgorithm!: ?[SignatureAlgorithm](./x509_package_enums.md#enum-signaturealgorithm) - 证书签名算法，默认值为 None，使用默认值时默认的摘要类型是 [SHA256](../../digest/digest_package_api/digest_package_classes.md#class-sha256)。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 私钥类型不支持、私钥类型和证书签名算法中的私钥类型不匹配或数字证书签名信息设置失败时，抛出异常。

### static func decodeFromDer(DerBlob)

```cangjie
public static func decodeFromDer(der: DerBlob): X509CertificateRequest
```

功能：将 DER 格式的数字证书签名请求解码。

参数：

- der: [DerBlob](x509_package_structs.md#struct-derblob) - DER 格式的二进制数据。

返回值：

- [X509CertificateRequest](x509_package_classes.md#class-x509certificaterequest) - 由 DER 格式解码出的数字证书签名请求。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 数据为空时，或数据不是有效的数字证书签名请求 DER 格式时抛出异常。

### static func decodeFromPem(String)

```cangjie
public static func decodeFromPem(pem: String): Array<X509CertificateRequest>
```

功能：将数字证书签名请求从 PEM 格式解码。

参数：

- pem: String - PEM 格式的数字证书签名请求字符流。

返回值：

- Array\<[X509CertificateRequest](x509_package_classes.md#class-x509certificaterequest)> - 由 PEM 格式解码出的数字证书签名请求数组。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 字符流不符合 PEM 格式时，或文件头不符合数字证书签名请求头标准时抛出异常。

### func encodeToDer()

```cangjie
public func encodeToDer(): DerBlob
```

功能：将数字证书签名请求编码成 Der 格式。

返回值：

- [DerBlob](x509_package_structs.md#struct-derblob) - 编码后的 Der 格式的数字证书签名请求。

### func encodeToPem()

```cangjie
public func encodeToPem(): PemEntry
```

功能：将数字证书签名请求编码成 PEM 格式。

返回值：

- [PemEntry](x509_package_structs.md#struct-pementry) - 编码后的 PEM 格式的数字证书签名请求。

### func hashCode()

```cangjie
public override func hashCode(): Int64
```

功能：返回证书签名请求哈希值。

返回值：

- Int64 - 对证书签名请求对象进行哈希计算后得到的结果。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成证书签名请求名称字符串，包含证书签名请求的使用者信息。

返回值：

- String - 证书签名请求名称字符串。

## class X509Name

```cangjie
public class X509Name <: ToString {
    public init(
        countryName!: ?String = None,
        provinceName!: ?String = None,
        localityName!: ?String = None,
        organizationName!: ?String = None,
        organizationalUnitName!: ?String = None,
        commonName!: ?String = None,
        email!: ?String = None
    )
}
```

功能：证书实体可辨识名称（Distinguished Name）是数字证书中的一个重要组成部分，作用是确保证书的持有者身份的真实性和可信度，同时也是数字证书验证的重要依据之一。

[X509Name](x509_package_classes.md#class-x509name) 通常包含证书实体的国家或地区名称（Country Name）、州或省名称（State or Province Name）、城市名称（Locality Name）、组织名称（Organization Name）、组织单位名称（Organizational Unit Name）、通用名称（Common Name）。有时也会包含 email 地址。

父类型：

- ToString

### prop commonName

```cangjie
public prop commonName: ?String
```

功能：返回证书实体的通用名称。

类型：?String

### prop countryName

```cangjie
public prop countryName: ?String
```

功能：返回证书实体的国家或地区名称。

类型：?String

### prop email

```cangjie
public prop email: ?String
```

功能：返回证书实体的 email 地址。

类型：?String

### prop localityName

```cangjie
public prop localityName: ?String
```

功能：返回证书实体的城市名称。

类型：?String

### prop organizationName

```cangjie
public prop organizationName: ?String
```

功能：返回证书实体的组织名称。

类型：?String

### prop organizationalUnitName

```cangjie
public prop organizationalUnitName: ?String
```

功能：返回证书实体的组织单位名称。

类型：?String

### prop provinceName

```cangjie
public prop provinceName: ?String
```

功能：返回证书实体的州或省名称。

类型：?String

### init(?String, ?String, ?String, ?String, ?String, ?String, ?String)

```cangjie
    public init(
        countryName!: ?String = None,
        provinceName!: ?String = None,
        localityName!: ?String = None,
        organizationName!: ?String = None,
        organizationalUnitName!: ?String = None,
        commonName!: ?String = None,
        email!: ?String = None
    )
```

功能：构造 [X509Name](x509_package_classes.md#class-x509name) 对象。

参数：

- countryName!: ?String - 国家或地区名称，默认值为 None。
- provinceName!: ?String - 州或省名称，默认值为 None。
- localityName!: ?String - 城市名称，默认值为 None。
- organizationName!: ?String - 组织名称，默认值为 None。
- organizationalUnitName!: ?String - 组织单位名称，默认值为 None。
- commonName!: ?String - 通用名称，默认值为 None。
- email!: ?String - email 地址，默认值为 None。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 设置证书实体可辨识名称时失败，比如内存分配异常等内部错误，则抛出异常。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成证书实体名称字符串。

返回值：

- String - 证书实体名称字符串，包含实体名称中存在的字段信息。
