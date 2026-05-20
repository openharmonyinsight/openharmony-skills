# 结构体

## struct OAEPOption

```cangjie
public struct OAEPOption {
    public init(hash: Digest, mgfHash: Digest, label!: String = "")
}
```

功能：此结构体为 [OAEP](./keys_package_enums.md#enum-padoption)  填充模式需要设置的参数。

### init(Digest, Digest, String)

```cangjie
public init(hash: Digest, mgfHash: Digest, label!: String = "")
```

功能：初始化 OAEP 填充参数。

参数：

- hash: Digest - 摘要方法，用于对 label 进行摘要。
- mgfHash: Digest - 摘要方法，用于设置 MGF1 函数中的摘要方法。
- label!: String - label 是可选参数，默认为空字符串，可以通过设置 label 来区分不同的加密操作。

## struct PSSOption

```cangjie
public struct PSSOption {
    public init(saltLen: Int32)
}
```

功能：此结构体为 [PSS](./keys_package_enums.md#enum-padoption) 填充模式需要设置的参数。

### init(Int32)

```cangjie(Int32)
public init(saltLen: Int32)
```

功能：初始化 PSS 填充参数。

参数：

- saltLen: Int32 - 随机盐长度，长度应大于等于 0，小于等于（RSA 长度 - 摘要长度 - 2），长度单位为字节，长度过长会导致签名失败。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 随机盐长度小于 0，抛出异常。
