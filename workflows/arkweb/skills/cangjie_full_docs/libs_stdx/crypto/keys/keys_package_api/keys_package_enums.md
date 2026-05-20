# 枚举

## enum Curve

```cangjie
public enum Curve {
    | P224 | P256 | P384 | P521 | BP256 | BP320 | BP384 | BP512
}
```

功能：枚举类型 [Curve](keys_package_enums.md#enum-curve) 用于选择生成 ECDSA 密钥时使用的椭圆曲线类型。

椭圆曲线是一种数学曲线，常用于加密算法中的密钥生成。在密码学中，椭圆曲线密码算法是一种基于椭圆曲线的公钥密码算法。它的基本思想是利用椭圆曲线上的点集构成一个计算困难性，来实现公钥密码的安全性。

[Curve](keys_package_enums.md#enum-curve) 枚举类型支持 NIST P-224，NIST P-256，NIST P-384，NIST P-521，Brainpool P-256，Brainpool P-320，Brainpool P-384，Brainpool P-512 八种椭圆曲线。

- NIST P-224：基于椭圆曲线的加密算法，使用 224 位的素数作为模数，安全性较高，适用于轻量级应用。

- NIST P-256：基于椭圆曲线的加密算法，使用 256 位的素数作为模数，安全性较高，适用于中等级应用。

- NIST P-384：基于椭圆曲线的加密算法，使用 384 位的素数作为模数，安全性非常高，适用于高级别应用。

- NIST P-521：基于椭圆曲线的加密算法，使用 521 位的素数作为模数，安全性非常高，适用于极高级别应用。

- Brainpool P-256：基于椭圆曲线的加密算法，使用 256 位的素数作为模数，安全性较高，但比 NIST P-256 更快。

- Brainpool P-320：基于椭圆曲线的加密算法，使用 320 位的素数作为模数，安全性非常高，但比 NIST P-384 更快。

- Brainpool P-384：基于椭圆曲线的加密算法，使用 384 位的素数作为模数，安全性非常高，但比 NIST P-384 更快。

- Brainpool P-512：基于椭圆曲线的加密算法，使用 512 位的素数作为模数，安全性非常高，但比 NIST P-521 更快

### BP256

```cangjie
BP256
```

功能：使用 Brainpool P-256 椭圆曲线初始化 [Curve](keys_package_enums.md#enum-curve) 实例。

### BP320

```cangjie
BP320
```

功能：使用 Brainpool P-320 椭圆曲线初始化 [Curve](keys_package_enums.md#enum-curve) 实例。

### BP384

```cangjie
BP384
```

功能：使用 Brainpool P-384 椭圆曲线初始化 [Curve](keys_package_enums.md#enum-curve) 实例。

### BP512

```cangjie
BP512
```

功能：使用 Brainpool P-512 椭圆曲线初始化 [Curve](keys_package_enums.md#enum-curve) 实例。

### P224

```cangjie
P224
```

功能：使用 NIST P-224 椭圆曲线初始化 [Curve](keys_package_enums.md#enum-curve) 实例。

### P256

```cangjie
P256
```

功能：使用 NIST P-256 椭圆曲线初始化 [Curve](keys_package_enums.md#enum-curve) 实例。

### P384

```cangjie
P384
```

功能：使用 NIST P-384 椭圆曲线初始化 [Curve](keys_package_enums.md#enum-curve) 实例。

### P521

```cangjie
P521
```

功能：使用 NIST P-521 椭圆曲线初始化 [Curve](keys_package_enums.md#enum-curve) 实例。

## enum PadOption

```cangjie
public enum PadOption {
    | OAEP(OAEPOption) | PSS(PSSOption) | PKCS1
}
```

功能：用于设置 RSA 的填充模式。

RSA 有三种常用的填充模式：

- OAEP 为最优非对称加密填充，只能用于加密解密；
- PSS 为概率签名方案，只能用于签名和验证；
- PKCS1 是一种普通的填充模式，用于填充数据长度，可以用于加密、解密、签名和验证。

RSA 的 PKCS1 填充模式是在早期的 PKCS #1 v1.5 规范中定义的填充模式，当前对使用 PKCS1 填充模式的攻击较为成熟，容易被攻击者解密或伪造签名，建议采用 PKCS #1 v2 版本中更加安全的 PSS 或 OAEP 填充模式。

### OAEP(OAEPOption)

```cangjie
OAEP(OAEPOption)
```

功能：使用最优非对称加密初始化 [PadOption](keys_package_enums.md#enum-padoption) 实例。

### PKCS1

```cangjie
PKCS1
```

功能：使用 PKCS #1 公钥密码学标准初始化 [PadOption](keys_package_enums.md#enum-padoption) 实例。

### PSS(PSSOption)

```cangjie
PSS(PSSOption)
```

功能：使用概率签名方案初始化 [PadOption](keys_package_enums.md#enum-padoption) 实例。
