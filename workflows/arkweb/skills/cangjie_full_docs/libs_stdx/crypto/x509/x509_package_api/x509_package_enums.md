# 枚举

## enum PublicKeyAlgorithm

```cangjie
public enum PublicKeyAlgorithm <: Equatable<PublicKeyAlgorithm> & ToString {
    RSA | DSA | ECDSA | UnknownPublicKeyAlgorithm
}
```

功能：数字证书中包含的公钥信息，目前支持的种类有：RSA、DSA、ECDSA。

父类型：

- Equatable\<[PublicKeyAlgorithm](#enum-publickeyalgorithm)>
- ToString

### DSA

```cangjie
DSA
```

功能：DSA 公钥算法。

### ECDSA

```cangjie
ECDSA
```

功能：ECDSA 公钥算法。

### RSA

```cangjie
RSA
```

功能：RSA 公钥算法。

### UnknownPublicKeyAlgorithm

```cangjie
UnknownPublicKeyAlgorithm
```

功能：未知公钥算法。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成证书携带的公钥算法名称字符串。

返回值：

- String - 证书携带的公钥算法名称字符串。

### operator func !=(PublicKeyAlgorithm)

```cangjie
public override operator func !=(other: PublicKeyAlgorithm): Bool
```

功能：判不等。

参数：

- other: [PublicKeyAlgorithm](x509_package_enums.md#enum-publickeyalgorithm) - 被比较的公钥算法。

返回值：

- Bool - 若公钥算法不同，返回 true；否则，返回 false。

### operator func ==(PublicKeyAlgorithm)

```cangjie
public override operator func ==(other: PublicKeyAlgorithm): Bool
```

功能：判等。

参数：

- other: [PublicKeyAlgorithm](x509_package_enums.md#enum-publickeyalgorithm) - 被比较的公钥算法。

返回值：

- Bool - 若公钥算法相同，返回 true；否则，返回 false。

## enum SignatureAlgorithm

```cangjie
public enum SignatureAlgorithm <: Equatable<SignatureAlgorithm> & ToString {
    | MD2WithRSA | MD5WithRSA | SHA1WithRSA | SHA256WithRSA | SHA384WithRSA
    | SHA512WithRSA | DSAWithSHA1 | DSAWithSHA256 | ECDSAWithSHA1 | ECDSAWithSHA256
    | ECDSAWithSHA384 | ECDSAWithSHA512 | UnknownSignatureAlgorithm
}
```

功能：证书签名算法（[Signature](x509_package_structs.md#struct-signature) Algorithm）是用于数字证书签名的算法，它是一种将数字证书中的公钥和其他信息进行加密的算法，以确保数字证书的完整性和真实性。

目前支持签名算法的种类包括：MD2WithRSA 、MD5WithRSA 、SHA1WithRSA 、SHA256WithRSA 、SHA384WithRSA、SHA512WithRSA、DSAWithSHA1、DSAWithSHA256、ECDSAWithSHA1、ECDSAWithSHA256、ECDSAWithSHA384 和 ECDSAWithSHA512。

父类型：

- Equatable\<[SignatureAlgorithm](#enum-signaturealgorithm)>
- ToString

### DSAWithSHA1

```cangjie
DSAWithSHA1
```

功能：DSAwithSHA1 签名算法。

### DSAWithSHA256

```cangjie
DSAWithSHA256
```

功能：DSAwithSHA256 签名算法。

### ECDSAWithSHA1

```cangjie
ECDSAWithSHA1
```

功能：ECDSAwithSHA1 签名算法。

### ECDSAWithSHA256

```cangjie
ECDSAWithSHA256
```

功能：ECDSAwithSHA256 签名算法。

### ECDSAWithSHA384

```cangjie
ECDSAWithSHA384
```

功能：ECDSAwithSHA384 签名算法。

### ECDSAWithSHA512

```cangjie
ECDSAWithSHA512
```

功能：ECDSAwithSHA512 签名算法。

### MD2WithRSA

```cangjie
MD2WithRSA
```

功能：MD2withRSA 签名算法。

### MD5WithRSA

```cangjie
MD5WithRSA
```

功能：MD5withRSA 签名算法。

### SHA1WithRSA

```cangjie
SHA1WithRSA
```

功能：SHA1withRSA 签名算法。

### SHA256WithRSA

```cangjie
SHA256WithRSA
```

功能：SHA256withRSA 签名算法。

### SHA384WithRSA

```cangjie
SHA384WithRSA
```

功能：SHA384withRSA 签名算法。

### SHA512WithRSA

```cangjie
SHA512WithRSA
```

功能：SHA512withRSA 签名算法。

### UnknownSignatureAlgorithm

```cangjie
UnknownSignatureAlgorithm
```

功能：未知签名算法。

### func toString()

```cangjie
public override func toString(): String
```

功能：生成证书签名算法名称字符串。

返回值：

- String - 证书签名算法名称字符串。

### operator func != (SignatureAlgorithm)

```cangjie
public override operator func !=(other: SignatureAlgorithm): Bool
```

功能：判不等。

参数：

- other: [SignatureAlgorithm](./x509_package_enums.md#enum-signaturealgorithm) - 被比较的签名算法。

返回值：

- Bool - 若签名算法不同，返回 true；否则，返回 false。

### operator func == (SignatureAlgorithm)

```cangjie
public override operator func ==(other: SignatureAlgorithm): Bool
```

功能：判等。

参数：

- other: [SignatureAlgorithm](./x509_package_enums.md#enum-signaturealgorithm) - 被比较的签名算法。

返回值：

- Bool - 若签名算法相同，返回 true；否则，返回 false。
