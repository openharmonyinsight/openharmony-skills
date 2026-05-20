# 结构体

## struct DerBlob

```cangjie
public struct DerBlob <: Equatable<DerBlob> & Hashable {
    public init(content: Array<Byte>)
}
```

功能：Crypto 支持配置二进制证书流，用户读取二进制证书数据并创建 [DerBlob](x509_package_structs.md#struct-derblob) 对象后可将其解析成 [X509Certificate](x509_package_classes.md#class-x509certificate) / [X509CertificateRequest](x509_package_classes.md#class-x509certificaterequest) / [PublicKey](x509_package_interfaces.md#interface-publickey) / [PrivateKey](x509_package_interfaces.md#interface-privatekey) 对象。

父类型：

- Equatable\<[DerBlob](#struct-derblob)>
- Hashable

### prop body

```cangjie
public prop body: Array<Byte>
```

功能：[DerBlob](x509_package_structs.md#struct-derblob) 对象中的字符序列。

类型：Array\<Byte>

### prop size

```cangjie
public prop size: Int64
```

功能：[DerBlob](x509_package_structs.md#struct-derblob) 对象中字符序列的大小。

类型：Int64

### init(Array\<Byte>)

```cangjie
public init(content: Array<Byte>)
```

功能：构造 [DerBlob](x509_package_structs.md#struct-derblob) 对象。

参数：

- content: Array\<Byte> - 二进制字符序列。

### func hashCode()

```cangjie
public override func hashCode(): Int64
```

功能：返回 [DerBlob](x509_package_structs.md#struct-derblob) 对象哈希值。

返回值：

- Int64 - 对 [DerBlob](x509_package_structs.md#struct-derblob) 对象进行哈希计算后得到的结果。

### operator func !=(DerBlob)

```cangjie
public override operator func !=(other: DerBlob): Bool
```

功能：判不等。

参数：

- other: [DerBlob](x509_package_structs.md#struct-derblob) - 被比较的 [DerBlob](x509_package_structs.md#struct-derblob) 对象。

返回值：

- Bool - 若对象不同，返回 true；否则，返回 false。

### operator func ==(DerBlob)

```cangjie
public override operator func ==(other: DerBlob): Bool
```

功能：判等。

参数：

- other: [DerBlob](x509_package_structs.md#struct-derblob) - 被比较的 [DerBlob](x509_package_structs.md#struct-derblob) 对象。

返回值：

- Bool - 若对象相同，返回 true；否则，返回 false。

## struct ExtKeyUsage

```cangjie
public struct ExtKeyUsage <: ToString {
    public static let AnyKey: UInt16 = 0
    public static let ServerAuth: UInt16 = 1
    public static let ClientAuth: UInt16 = 2
    public static let EmailProtection: UInt16 = 3
    public static let CodeSigning: UInt16 = 4
    public static let OCSPSigning: UInt16 = 5
    public static let TimeStamping: UInt16 = 6
    public init(keys: Array<UInt16>)
}
```

功能：数字证书扩展字段中通常会包含携带扩展密钥用法说明，目前支持的用途有：ServerAuth、ClientAuth、EmailProtection、CodeSigning、OCSPSigning、TimeStamping。

父类型：

- ToString

### static let AnyKey

```cangjie
public static let AnyKey: UInt16 = 0
```

功能：表示应用于任意用途。

类型：UInt16

### static let ClientAuth

```cangjie
public static let ClientAuth: UInt16 = 2
```

功能：表示用于 SSL 的客户端验证。

类型：UInt16

### static let CodeSigning

```cangjie
public static let CodeSigning: UInt16 = 4
```

功能：表示用于代码签名。

类型：UInt16

### static let EmailProtection

```cangjie
public static let EmailProtection: UInt16 = 3
```

功能：表示用于电子邮件的加解密、签名等。

类型：UInt16

### static let OCSPSigning

```cangjie
public static let OCSPSigning: UInt16 = 5
```

功能：用于对 OCSP 响应包进行签名。

类型：UInt16

### static let ServerAuth

```cangjie
public static let ServerAuth: UInt16 = 1
```

功能：表示用于 SSL 的服务端验证。

类型：UInt16

### static let TimeStamping

```cangjie
public static let TimeStamping: UInt16 = 6
```

功能：用于将对象摘要值与时间绑定。

类型：UInt16

### init(Array\<UInt16>)

```cangjie
public init(keys: Array<UInt16>)
```

功能：构造指定用途的扩展密钥用法，需要注意同一个密钥可以有多种用途。

参数：

- keys: Array\<UInt16> - 密钥。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成扩展密钥用途字符串。

返回值：

- String - 证书扩展密钥用途字符串。

## struct KeyUsage

```cangjie
public struct KeyUsage <: ToString {
    public static let DigitalSignature: UInt16 = 0x0080
    public static let NonRepudiation: UInt16 = 0x0040
    public static let KeyEncipherment: UInt16 = 0x0020
    public static let DataEncipherment: UInt16 = 0x0010
    public static let KeyAgreement: UInt16 = 0x0008
    public static let CertSign: UInt16 = 0x0004
    public static let CRLSign: UInt16 = 0x0002
    public static let EncipherOnly: UInt16 = 0x0001
    public static let DecipherOnly: UInt16 = 0x0100
    public init(keys: UInt16)
}
```

功能：数字证书扩展字段中通常会包含携带公钥的用法说明，目前支持的用途有：DigitalSignature、NonRepudiation、KeyEncipherment、DataEncipherment、KeyAgreement、CertSign、CRLSign、EncipherOnly、DecipherOnly。

父类型：

- ToString

### static let CRLSign

```cangjie
public static let CRLSign: UInt16 = 0x0002
```

功能：表示私钥可用于对 CRL 签名，而公钥可用于验证 CRL 签名。

类型：UInt16

### static let CertSign

```cangjie
public static let CertSign: UInt16 = 0x0004
```

功能：表示私钥用于证书签名，而公钥用于验证证书签名，专用于 CA 证书。

类型：UInt16

### static let DataEncipherment

```cangjie
public static let DataEncipherment: UInt16 = 0x0010
```

功能：表示公钥用于直接加密数据。

类型：UInt16

### static let DecipherOnly

```cangjie
public static let DecipherOnly: UInt16 = 0x0100
```

功能：表示证书中的公钥在密钥协商过程中，仅仅用于解密计算，配合 key Agreement 使用才有意义。

类型：UInt16

### static let DigitalSignature

```cangjie
public static let DigitalSignature: UInt16 = 0x0080
```

功能：表示私钥可以用于除了签发证书、签发 CRL 和非否认性服务的各种数字签名操作，而公钥用来验证这些签名。

类型：UInt16

### static let EncipherOnly

```cangjie
public static let EncipherOnly: UInt16 = 0x0001
```

功能：表示证书中的公钥在密钥协商过程中，仅仅用于加密计算，配合 key Agreement 使用才有意义。

类型：UInt16

### static let KeyAgreement

```cangjie
public static let KeyAgreement: UInt16 = 0x0008
```

功能：表示密钥用于密钥协商。

类型：UInt16

### static let KeyEncipherment

```cangjie
public static let KeyEncipherment: UInt16 = 0x0020
```

功能：表示密钥用来加密传输其他的密钥。

类型：UInt16

### static let NonRepudiation

```cangjie
public static let NonRepudiation: UInt16 = 0x0040
```

功能：表示私钥可以用于进行非否认性服务中的签名，而公钥用来验证签名。

类型：UInt16

### init(UInt16)

```cangjie
public init(keys: UInt16)
```

功能：构造指定用途的扩展密钥用法，需要注意同一个密钥可以有多种用途。

参数：

- keys: UInt16 - 密钥的用法，建议使用本结构中所提供的密钥用法变量通过按位或的方式传入参数。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成密钥用途字符串。

返回值：

- String - 证书密钥用途字符串。

## struct Pem

```cangjie
public struct Pem <: Collection<PemEntry> & ToString {
    public Pem(private let items: Array<PemEntry>)
}
```

功能：结构体 [Pem](x509_package_structs.md#struct-pem) 为条目序列，可以包含多个 [PemEntry](x509_package_structs.md#struct-pementry)。

父类型：

- Collection\<[PemEntry](#struct-pementry)>
- ToString

### prop size

```cangjie
public override prop size: Int64
```

功能：条目序列的数量。

类型：Int64

### Pem(Array\<PemEntry>)

```cangjie
public Pem(private let items: Array<PemEntry>)
```

功能：构造 [Pem](x509_package_structs.md#struct-pem) 对象。

参数：

- items: Array\<[PemEntry](x509_package_structs.md#struct-pementry)> - 多个 [PemEntry](x509_package_structs.md#struct-pementry) 对象。

### static func decode(String)

```cangjie
public static func decode(text: String): Pem
```

功能：将 PEM 文本解码为条目序列。

参数：

- text: String - PEM 字符串。

返回值：

- [Pem](x509_package_structs.md#struct-pem) - PEM 条目序列。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 数据为空时，或解码失败抛出异常。

### func encode()

```cangjie
public func encode(): String
```

功能：返回 PEM 格式的字符串。行结束符将根据当前操作系统生成。

返回值：

- String - PEM 格式的字符串。

### func isEmpty()

```cangjie
public override func isEmpty(): Bool
```

功能：判断 PEM 文本解码为条目序列是否为空。

返回值：

- Bool - PEM 文本解码为条目序列为空返回 true；否则，返回 false。

### func iterator()

```cangjie
public override func iterator(): Iterator<PemEntry>
```

功能：生成 PEM 文本解码为条目序列的迭代器。

返回值：

- Iterator\<[PemEntry](x509_package_structs.md#struct-pementry)> - PEM 文本解码为条目序列的迭代器。

### func toString()

```cangjie
public override func toString(): String
```

功能：返回一个字符串，字符串内容是包含每个条目序列的标签。

返回值：

- String - 包含每个条目序列的标签的字符串。

## struct PemEntry

```cangjie
public struct PemEntry <: ToString {
    public static let LABEL_CERTIFICATE = "CERTIFICATE"
    public static let LABEL_X509_CRL = "X509 CRL"
    public static let LABEL_CERTIFICATE_REQUEST = "CERTIFICATE REQUEST"
    public static let LABEL_PRIVATE_KEY = "PRIVATE KEY"
    public static let LABEL_EC_PRIVATE_KEY = "EC PRIVATE KEY"
    public static let LABEL_ENCRYPTED_PRIVATE_KEY = "ENCRYPTED PRIVATE KEY"
    public static let LABEL_RSA_PRIVATE_KEY = "RSA PRIVATE KEY"
    public static let LABEL_SM2_PRIVATE_KEY = "SM2 PRIVATE KEY"
    public static let LABEL_PUBLIC_KEY = "PUBLIC KEY"
    public static let LABEL_EC_PARAMETERS = "EC PARAMETERS"
    public static let LABEL_DH_PARAMETERS = "DH PARAMETERS"
    public PemEntry(
        public let label: String,
        public let headers: Array<(String, String)>,
        public let body: ?DerBlob
    )
    public init(label: String, body: DerBlob)
}
```

功能：PEM 文本格式经常用于存储证书和密钥，PEM 编码结构包含以下几个部分：

第一行是 “-----BEGIN”，标签和 “-----” 组成的 utf8 编码的字符串；
中间是正文，是实际二进制内容经过 base64 编码得到的可打印字符串，详细的 PEM 编码规范可参考 [RFC 7468](https://www.rfc-editor.org/rfc/rfc7468.html)；
最后一行是 “-----END”，标签和 “-----” 组成的 utf8 编码的字符串，详见 [RFC 1421](https://www.rfc-editor.org/rfc/rfc1421.html)。
在旧版的 PEM 编码标准中在第一行和正文之间还包含条目头。

为了支持不同的用户场景，我们提供了 [PemEntry](x509_package_structs.md#struct-pementry) 和 [Pem](x509_package_structs.md#struct-pem) 类型，[PemEntry](x509_package_structs.md#struct-pementry) 用于存储单个 PEM 基础结构。

父类型：

- ToString

### static let LABEL_CERTIFICATE

```cangjie
public static let LABEL_CERTIFICATE = "CERTIFICATE"
```

功能：记录条目类型为证书。

类型：String

### static let LABEL_CERTIFICATE_REQUEST

```cangjie
public static let LABEL_CERTIFICATE_REQUEST = "CERTIFICATE REQUEST"
```

功能：记录条目类型为证书签名请求。

类型：String

### static let LABEL_DH_PARAMETERS

```cangjie
public static let LABEL_DH_PARAMETERS = "DH PARAMETERS"
```

功能：记录条目类型为 DH 密钥参数。

类型：String

### static let LABEL_EC_PARAMETERS

```cangjie
public static let LABEL_EC_PARAMETERS = "EC PARAMETERS"
```

功能：记录条目类型为椭圆曲线参数。

类型：String

### static let LABEL_EC_PRIVATE_KEY

```cangjie
public static let LABEL_EC_PRIVATE_KEY = "EC PRIVATE KEY"
```

功能：记录条目类型为椭圆曲线私钥。

类型：String

### static let LABEL_ENCRYPTED_PRIVATE_KEY

```cangjie
public static let LABEL_ENCRYPTED_PRIVATE_KEY = "ENCRYPTED PRIVATE KEY"
```

功能：记录条目类型为 PKCS #8 标准加密的私钥。

类型：String

### static let LABEL_PRIVATE_KEY

```cangjie
public static let LABEL_PRIVATE_KEY = "PRIVATE KEY"
```

功能：记录条目类型为 PKCS #8 标准未加密的私钥。

类型：String

### static let LABEL_PUBLIC_KEY

```cangjie
public static let LABEL_PUBLIC_KEY = "PUBLIC KEY"
```

功能：记录条目类型为公钥。

类型：String

### static let LABEL_RSA_PRIVATE_KEY

```cangjie
public static let LABEL_RSA_PRIVATE_KEY = "RSA PRIVATE KEY"
```

功能：记录条目类型为 RSA 私钥。

类型：String

### static let LABEL_SM2_PRIVATE_KEY

```cangjie
public static let LABEL_SM2_PRIVATE_KEY = "SM2 PRIVATE KEY"
```

功能：记录条目类型为 SM2 私钥。

类型：String

### static let LABEL_X509_CRL

```cangjie
public static let LABEL_X509_CRL = "X509 CRL"
```

功能：记录条目类型为证书吊销列表。

类型：String

### PemEntry(String, Array\<(String, String)>, ?DerBlob)

```cangjie
public PemEntry(
    public let label: String,
    public let headers: Array<(String, String)>,
    public let body: ?DerBlob
)
```

功能：构造 [PemEntry](x509_package_structs.md#struct-pementry) 对象。

参数：

- label: String - 标签。
- headers: Array\<(String, String)> - 条目头。
- body: ?[DerBlob](x509_package_structs.md#struct-derblob) - 二进制内容。

### let body

```cangjie
public let body: ?DerBlob
```

功能：[PemEntry](x509_package_structs.md#struct-pementry) 实例的二进制内容。

类型：?[DerBlob](x509_package_structs.md#struct-derblob)

### let headers

```cangjie
public let headers: Array<(String, String)>
```

功能：[PemEntry](x509_package_structs.md#struct-pementry) 实例的条目头。

类型：Array\<(String, String)>

### let label

```cangjie
public let label: String
```

功能：[PemEntry](x509_package_structs.md#struct-pementry) 实例的标签。

类型：String

### init(String, DerBlob)

```cangjie
public init(label: String, body: DerBlob)
```

功能：构造 [PemEntry](x509_package_structs.md#struct-pementry) 对象。

参数：

- label: String - 标签
- body: [DerBlob](x509_package_structs.md#struct-derblob) - 二进制内容

### func encode()

```cangjie
public func encode(): String
```

功能：返回 PEM 格式的字符串。行结束符将根据当前操作系统生成。

返回值：

- String - PEM 格式的字符串。

### func header(String)

```cangjie
public func header(name: String): Iterator<String>
```

功能：通过条目头名称，找到对应条目内容。

参数：

- name: String - 条目头名称。

返回值：

- Iterator\<String> - 条目头名称对应内容的迭代器。

### func toString()

```cangjie
public override func toString(): String
```

功能：返回 PEM 对象的标签和二进制内容的长度。

返回值：

- String - PEM 对象的标签和二进制内容的长度。

## struct SerialNumber

```cangjie
public struct SerialNumber <: Equatable<SerialNumber> & Hashable & ToString {
    public init(length!: UInt8 = 16)
}
```

功能：结构体 [SerialNumber](x509_package_structs.md#struct-serialnumber) 为数字证书的序列号，是数字证书中的一个唯一标识符，用于标识数字证书的唯一性。根据规范，证书序列号的长度不应超过 20 字节。详见 [rfc5280](https://www.rfc-editor.org/rfc/rfc5280)。

父类型：

- Equatable\<[SerialNumber](#struct-serialnumber)>
- Hashable
- ToString

### init(UInt8)

```cangjie
public init(length!: UInt8 = 16)
```

功能：生成指定长度的随机序列号。

参数：

- length!: UInt8 - 序列号长度，单位为字节，类型为 UInt8，默认值为 16。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - length 等于 0 或大于 20 时，抛出异常。

### func hashCode()

```cangjie
public override func hashCode(): Int64
```

功能：返回证书序列号哈希值。

返回值：

- Int64 - 对证书序列号对象进行哈希计算后得到的结果。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成证书序列号字符串，格式为 16 进制。

返回值：

- String - 证书序列号字符串。

### operator func !=(SerialNumber)

```cangjie
public override operator func !=(other: SerialNumber): Bool
```

功能：判不等。

参数：

- other: [SerialNumber](x509_package_structs.md#struct-serialnumber) - 被比较的证书序列号对象。

返回值：

- Bool - 若序列号不同，返回 true；否则，返回 false。

### operator func ==(SerialNumber)

```cangjie
public override operator func ==(other: SerialNumber): Bool
```

功能：判等。

参数：

- other: [SerialNumber](x509_package_structs.md#struct-serialnumber) - 被比较的证书序列号对象。

返回值：

- Bool - 若序列号相同，返回 true；否则，返回 false。

## struct Signature

```cangjie
public struct Signature <: Equatable<Signature> & Hashable {
}
```

功能：数字证书的签名，用来验证身份的正确性。

父类型：

- Equatable\<[Signature](#struct-signature)>
- Hashable

### prop signatureValue

```cangjie
public prop signatureValue: DerBlob
```

功能：返回证书签名的二进制。

类型：[DerBlob](x509_package_structs.md#struct-derblob)

### func hashCode()

```cangjie
public override func hashCode(): Int64
```

功能：返回证书签名哈希值。

返回值：

- Int64 - 对证书签名对象进行哈希计算后得到的结果。

### operator func !=(Signature)

```cangjie
public override operator func !=(other: Signature): Bool
```

功能：判不等。

参数：

- other: [Signature](x509_package_structs.md#struct-signature) - 被比较的证书签名。

返回值：

- Bool - 若证书签名不同，返回 true；否则，返回 false。

### operator func ==(Signature)

```cangjie
public override operator func ==(other: Signature): Bool
```

功能：判等。

参数：

- other: [Signature](x509_package_structs.md#struct-signature) - 被比较的证书签名。

返回值：

- Bool - 若证书签名相同，返回 true；否则，返回 false。

## struct VerifyOption

```cangjie
public struct VerifyOption {
    public var time: DateTime = DateTime.now()
    public var dnsName: String = ""
    public var roots: Array<X509Certificate> = X509Certificate.systemRootCerts()
    public var intermediates: Array<X509Certificate> = Array<X509Certificate>()
}
```

功能：用于为 `x509` 证书验证函数 [verify](./x509_package_classes.md#func-verifyverifyoption) 提供配置选项。

### var dnsName

```cangjie
public var dnsName: String = ""
```

功能：校验域名，默认为空，只有设置域名时才会进行此处校验。

类型：String

### var intermediates

```cangjie
public var intermediates: Array<X509Certificate> = Array<X509Certificate>()
```

功能：中间证书链，默认为空。

类型：Array\<[X509Certificate](x509_package_classes.md#class-x509certificate)>

### var roots

```cangjie
public var roots: Array<X509Certificate> = X509Certificate.systemRootCerts()
```

功能：根证书链，默认为系统根证书链。

类型：Array\<[X509Certificate](x509_package_classes.md#class-x509certificate)>

### var time

```cangjie
public var time: DateTime = DateTime.now()
```

功能：校验时间，默认为创建选项的时间。

类型：DateTime

## struct X509CertificateInfo

```cangjie
public struct X509CertificateInfo {
    public var serialNumber: SerialNumber
    public var notBefore: DateTime
    public var notAfter: DateTime
    public var subject: ?X509Name
    public var dnsNames: Array<String>
    public var emailAddresses: Array<String>
    public var IPAddresses: Array<IP>
    public var keyUsage: ?KeyUsage
    public var extKeyUsage: ?ExtKeyUsage

    public init(
        serialNumber!: ?SerialNumber = None,
        notBefore!: ?DateTime = None,
        notAfter!: ?DateTime = None,
        subject!: ?X509Name = None,
        dnsNames!: Array<String> = Array<String>(),
        emailAddresses!: Array<String> = Array<String>(),
        IPAddresses!: Array<IP> = Array<IP>(),
        keyUsage!: ?KeyUsage = None,
        extKeyUsage!: ?ExtKeyUsage = None
    )
}
```

功能：[X509CertificateInfo](x509_package_structs.md#struct-x509certificateinfo) 结构包含了证书信息，包括证书序列号、有效期、实体可辨识名称、域名、email 地址、[IP](x509_package_type.md#type-ip) 地址、密钥用法和扩展密钥用法。

### var IPAddresses

```cangjie
public var IPAddresses: Array<IP>
```

功能：记录证书的 [IP](x509_package_type.md#type-ip) 地址。

类型：Array\<[IP](./x509_package_type.md#type-ip)>

### var dnsNames

```cangjie
public var dnsNames: Array<String>
```

功能：记录证书的 DNS 域名。

类型：Array\<String>

### var emailAddresses

```cangjie
public var emailAddresses: Array<String>
```

功能：记录证书的 email 地址。

类型：Array\<String>

### var extKeyUsage

```cangjie
public var extKeyUsage: ?ExtKeyUsage
```

功能：记录证书的扩展密钥用法。

类型：?[ExtKeyUsage](./x509_package_structs.md#struct-extkeyusage)

### var keyUsage

```cangjie
public var keyUsage: ?KeyUsage
```

功能：记录证书的密钥用法。

类型：?[KeyUsage](./x509_package_structs.md#struct-keyusage)

### var notAfter

```cangjie
public var notAfter: DateTime
```

功能：记录证书有效期的结束日期。

类型：DateTime

### var notBefore

```cangjie
public var notBefore: DateTime
```

功能：记录证书有效期的起始日期。

类型：DateTime

### var serialNumber

```cangjie
public var serialNumber: SerialNumber
```

功能：记录证书的序列号。

类型：[SerialNumber](x509_package_structs.md#struct-serialnumber)

### var subject

```cangjie
public var subject: ?X509Name
```

功能：记录证书实体可辨识名称。

类型：?[X509Name](x509_package_classes.md#class-x509name)

### init(?SerialNumber, ?DateTime, ?DateTime, ?X509Name, Array\<String>, Array\<String>, Array\<IP>, ?KeyUsage, ?ExtKeyUsage)

```cangjie
public init(
    serialNumber!: ?SerialNumber = None,
    notBefore!: ?DateTime = None,
    notAfter!: ?DateTime = None,
    subject!: ?X509Name = None,
    dnsNames!: Array<String> = Array<String>(),
    emailAddresses!: Array<String> = Array<String>(),
    IPAddresses!: Array<IP> = Array<IP>(),
    keyUsage!: ?KeyUsage = None,
    extKeyUsage!: ?ExtKeyUsage = None
)
```

功能：构造 [X509CertificateInfo](x509_package_structs.md#struct-x509certificateinfo) 对象。

参数：

- serialNumber!: ?[SerialNumber](x509_package_structs.md#struct-serialnumber) - 数字证书序列号，默认值为 None，使用默认值时默认的序列号长度为 128 比特。
- notBefore!: ?DateTime - 数字证书有效期开始时间，默认值为 None，使用默认值时默认的时间为 [X509CertificateInfo](x509_package_structs.md#struct-x509certificateinfo) 创建的时间。
- notAfter!: ?DateTime - 数字证书有效期截止时间，默认值为 None，使用默认值时默认的时间为 notBefore 往后 1 年的时间。
- subject!: ?[X509Name](x509_package_classes.md#class-x509name) - 数字证书使用者信息，默认值为 None。
- dnsNames!: Array\<String> - 域名列表，需要用户保证输入域名的有效性，默认值为空的字符串数组。
- emailAddresses!: Array\<String> - email 地址列表，需要用户保证输入 email 的有效性，默认值为空的字符串数组。
- IPAddresses!: Array\<[IP](x509_package_type.md#type-ip)> - [IP](x509_package_type.md#type-ip) 地址列表，默认值为空的 [IP](x509_package_type.md#type-ip) 数组。
- keyUsage!: ?[KeyUsage](x509_package_structs.md#struct-keyusage) - 密钥用法，默认值为 None。
- extKeyUsage!: ?[ExtKeyUsage](x509_package_structs.md#struct-extkeyusage) - 扩展密钥用法，默认值为 None。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 输入的 [IP](x509_package_type.md#type-ip) 地址列表中包含无效的 [IP](x509_package_type.md#type-ip) 地址，则抛出异常。

## struct X509CertificateRequestInfo

```cangjie
public struct X509CertificateRequestInfo {
    public var subject: ?X509Name
    public var dnsNames: Array<String>
    public var emailAddresses: Array<String>
    public var IPAddresses: Array<IP>

    public init(
        subject!: ?X509Name = None,
        dnsNames!: Array<String> = Array<String>(),
        emailAddresses!: Array<String> = Array<String>(),
        IPAddresses!: Array<IP> = Array<IP>()
    )
}
```

功能：[X509CertificateRequestInfo](x509_package_structs.md#struct-x509certificaterequestinfo) 结构包含了证书请求信息，包括证书实体可辨识名称、域名、email 地址和 [IP](x509_package_type.md#type-ip) 地址。

### var IPAddresses

```cangjie
public var IPAddresses: Array<IP>
```

功能：记录证书签名请求的 [IP](x509_package_type.md#type-ip) 地址。

类型：Array\<[IP](./x509_package_type.md#type-ip)>

### var dnsNames

```cangjie
public var dnsNames: Array<String>
```

功能：记录证书签名请求的 DNS 域名。

类型：Array\<String>

### var emailAddresses

```cangjie
public var emailAddresses: Array<String>
```

功能：记录证书签名请求的 email 地址。

类型：Array\<String>

### var subject

```cangjie
public var subject: ?X509Name
```

功能：记录证书签名请求的实体可辨识名称。

### init(?X509Name, Array\<String>, Array\<String>, Array\<IP>)

```cangjie
public init(
    subject!: ?X509Name = None,
    dnsNames!: Array<String> = Array<String>(),
    emailAddresses!: Array<String> = Array<String>(),
    IPAddresses!: Array<IP> = Array<IP>()
)
```

功能：构造 [X509CertificateRequestInfo](x509_package_structs.md#struct-x509certificaterequestinfo) 对象。

参数：

- subject!: ?[X509Name](x509_package_classes.md#class-x509name) - 数字证书的使用者信息，默认值为 None。
- dnsNames!: Array\<String> - 域名列表，需要用户保证输入域名的有效性，默认值为空的字符串数组。
- emailAddresses!: Array\<String> - email 地址列表，需要用户保证输入 email 的有效性，默认值为空的字符串数组。
- IPAddresses!: Array\<[IP](x509_package_type.md#type-ip)> - [IP](x509_package_type.md#type-ip) 地址列表，默认值为空的 [IP](x509_package_type.md#type-ip) 数组。

异常：

- [X509Exception](./x509_package_exceptions.md#class-x509exception) - 输入的 [IP](x509_package_type.md#type-ip) 地址列表中包含无效的 [IP](x509_package_type.md#type-ip) 地址，则抛出异常。
