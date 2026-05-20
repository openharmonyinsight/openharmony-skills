# 类

## class SecureRandom

```cangjie
public class SecureRandom {
    public init(priv!: Bool = false)
}
```

功能：用于生成加密安全的伪随机数。

和 Random 相比，主要有三个方面不同：

- 随机数种子： Random 使用系统时钟作为默认的种子，时间戳一样，结果就相同；[SecureRandom](crypto_package_classes.md#class-securerandom) 使用操作系统或者硬件提供的随机数种子，生成的是真随机数。

- 随机数生成： Random 使用了梅森旋转伪随机生成器；[SecureRandom](crypto_package_classes.md#class-securerandom) 则使用了 openssl 库提供的 [MD5](../../digest/digest_package_api/digest_package_classes.md#class-md5) 等随机算法，使用熵源生成真随机数；如果硬件支持，还可以使用硬件随机数生成器来生成安全性更强的随机数。
- 安全性： Random 不能用于加密安全的应用或者隐私数据的保护，可以使用 [SecureRandom](crypto_package_classes.md#class-securerandom)。

使用示例见 [SecureRandom 使用](../crypto_samples/sample_secure_random.md)。

### init(Bool)

```cangjie
public init(priv!: Bool = false)
```

功能：创建 [SecureRandom](crypto_package_classes.md#class-securerandom) 实例，可指定是否使用更加安全的加密安全伪随机生成器，加密安全伪随机生成器可用于会话密钥和证书私钥等加密场景。

参数：

- priv!: Bool - 设置为 true 表示使用加密安全伪随机生成器。

### func nextBits(UInt64)

```cangjie
public func nextBits(bits: UInt64): UInt64
```

功能：生成一个指定位长的随机整数。

参数：

- bits: UInt64 - 要生成的随机数的位数，取值范围 (0, 64]。

返回值：

- UInt64 - 生成的用户指定位长的随机数。

异常：

- IllegalArgumentException - 如果 `bits` 等于 0，或大于 64，超过所能截取的 UInt64 长度，则抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextBool()

```cangjie
public func nextBool(): Bool
```

功能：获取一个随机的 Bool 类型实例。

返回值：

- Bool - 一个随机的 Bool 类型实例。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextBytes(Array\<Byte>)

```cangjie
public func nextBytes(bytes: Array<Byte>): Unit
```

功能：生成随机数替换入参数组中的每个元素。

参数：

- bytes: Array\<Byte> - 被替换的数组。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextBytes(Int32)

```cangjie
public func nextBytes(length: Int32): Array<Byte>
```

功能：获取一个指定长度的随机字节的数组。

参数：

- length: Int32 - 要生成的随机字节数组的长度。

返回值：

- Array\<Byte> - 一个随机字节数组。

异常：

- IllegalArgumentException - 当参数 length 小于等于 0，抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextFloat16()

```cangjie
public func nextFloat16(): Float16
```

功能：获取一个 Float16 类型且在区间 [0.0, 1.0) 内的随机数。

返回值：

- Float16 - 一个 Float16 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextFloat32()

```cangjie
public func nextFloat32(): Float32
```

功能：获取一个 Float32 类型且在区间 [0.0, 1.0) 内的随机数。

返回值：

- Float32 - 一个 Float32 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextFloat64()

```cangjie
public func nextFloat64(): Float64
```

功能：获取一个 Float64 类型且在区间 [0.0, 1.0) 内的随机数。

返回值：

- Float64 - 一个 Float64 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextGaussianFloat16(Float16, Float16)

```cangjie
public func nextGaussianFloat16(mean!: Float16 = 0.0, sigma!: Float16 = 1.0): Float16
```

功能：默认获取一个 Float16 类型且符合均值为 0.0 标准差为 1.0 的高斯分布的随机数，其中均值是期望值，可解释为位置参数，决定了分布的位置，标准差可解释为尺度参数，决定了分布的幅度。

参数：

- mean!: Float16 - 均值。
- sigma!: Float16 - 标准差。

返回值：

- Float16 - 一个 Float16 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextGaussianFloat32(Float32, Float32)

```cangjie
public func nextGaussianFloat32(mean!: Float32 = 0.0, sigma!: Float32 = 1.0): Float32
```

功能：默认获取一个 Float32 类型且符合均值为 0.0 标准差为 1.0 的高斯分布的随机数，其中均值是期望值，可解释为位置参数，决定了分布的位置，标准差可解释为尺度参数，决定了分布的幅度。

参数：

- mean!: Float32 - 均值。
- sigma!: Float32 - 标准差。

返回值：

- Float32 - 一个 Float32 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextGaussianFloat64(Float64, Float64)

```cangjie
public func nextGaussianFloat64(mean!: Float64 = 0.0, sigma!: Float64 = 1.0): Float64
```

功能：默认获取一个 Float64 类型且符合均值为 0.0 标准差为 1.0 的高斯分布的随机数，其中均值是期望值，可解释为位置参数，决定了分布的位置，标准差可解释为尺度参数，决定了分布的幅度。

参数：

- mean!: Float64 - 均值。
- sigma!: Float64 - 标准差。

返回值：

- Float64 - 一个 Float64 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextInt16()

```cangjie
public func nextInt16(): Int16
```

功能：获取一个 Int16 类型的随机数。

返回值：

- Int16 - 一个 Int16 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextInt32()

```cangjie
public func nextInt32(): Int32
```

功能：获取一个 Int32 类型的随机数。

返回值：

- Int32 - 一个 Int32 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextInt16(Int16)

```cangjie
public func nextInt16(max: Int16): Int16
```

功能：获取一个 Int16 类型且在区间 [0, max) 内的随机数。

参数：

- max: Int16 - 区间最大值。

返回值：

- Int16 - 一个 Int16 类型的随机数。

异常：

- IllegalArgumentException - 当 max 为非正数时，抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextInt32(Int32)

```cangjie
public func nextInt32(max: Int32): Int32
```

功能：获取一个 Int32 类型且在区间 [0, max) 内的随机数。

参数：

- max: Int32 - 区间最大值。

返回值：

- Int32 - 一个 Int32 类型的随机数。

异常：

- IllegalArgumentException - 当 max 为非正数时，抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextInt64()

```cangjie
public func nextInt64(): Int64
```

功能：获取一个 Int64 类型的随机数。

返回值：

- Int64 - 一个 Int64 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextInt64(Int64)

```cangjie
public func nextInt64(max: Int64): Int64
```

功能：获取一个 Int64 类型且在区间 [0, max) 内的随机数。

参数：

- max: Int64 - 区间最大值。

返回值：

- Int64 - 一个 Int64 类型的随机数。

异常：

- IllegalArgumentException - 当 max 为非正数时，抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextInt8()

```cangjie
public func nextInt8(): Int8
```

功能：获取一个 Int8 类型的随机数。

返回值：

- Int8 - 一个 Int8 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextInt8(Int8)

```cangjie
public func nextInt8(max: Int8): Int8
```

功能：获取一个 Int8 类型且在区间 [0, max) 内的随机数。

参数：

- max: Int8 - 区间最大值。

返回值：

- Int8 - 一个 Int8 类型的随机数。

异常：

- IllegalArgumentException - 当 max 为非正数时，抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextUInt16()

```cangjie
public func nextUInt16(): UInt16
```

功能：获取一个 UInt16 类型的随机数。

返回值：

- UInt16 - 一个 UInt16 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextUInt16(UInt16)

```cangjie
public func nextUInt16(max: UInt16): UInt16
```

功能：获取一个 UInt16 类型且在区间 [0, max) 内的随机数。

参数：

- max: UInt16 - 区间最大值。

返回值：

- UInt16 - 一个 UInt16 类型的随机数。

异常：

- IllegalArgumentException - 当 max 为 0 时，抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextUInt32()

```cangjie
public func nextUInt32(): UInt32
```

功能：获取一个 UInt32 类型的随机数。

返回值：

- UInt32 - 一个 UInt32 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextUInt32(UInt32)

```cangjie
public func nextUInt32(max: UInt32): UInt32
```

功能：获取一个 UInt32 类型且在区间 [0, max) 内的随机数。

参数：

- max: UInt32 - 区间最大值。

返回值：

- UInt32 - 一个 UInt32 类型的随机数。

异常：

- IllegalArgumentException - 当 max 为 0 时，抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextUInt64()

```cangjie
public func nextUInt64(): UInt64
```

功能：获取一个 UInt64 类型的随机数。

返回值：

- UInt64 - 一个 UInt64 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextUInt64(UInt64)

```cangjie
public func nextUInt64(max: UInt64): UInt64
```

功能：获取一个 UInt64 类型且在区间 [0, max) 内的随机数。

参数：

- max: UInt64 - 区间最大值。

返回值：

- UInt64 - 一个 UInt64 类型的随机数。

异常：

- IllegalArgumentException - 当 max 为 0 时，抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextUInt8()

```cangjie
public func nextUInt8(): UInt8
```

功能：获取一个 UInt8 类型的随机数。

返回值：

- UInt8 - 一个 UInt8 类型的随机数。

异常：

- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

### func nextUInt8(UInt8)

```cangjie
public func nextUInt8(max: UInt8): UInt8
```

功能：获取一个 UInt8 类型且在区间 [0, max) 内的随机数。

参数：

- max: UInt8 - 区间最大值。

返回值：

- UInt8 - 一个 UInt8 类型的随机数。

异常：

- IllegalArgumentException - 当 max 为 0 时，抛出异常。
- [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) - 当生成器不能正确生成随机数或生成随机数失败时，抛出异常。

## class SM4

```cangjie
public class SM4 <: BlockCipher {
    public init(
        optMode: OperationMode,
        key: Array<Byte>,
        iv!: Array<Byte> = Array<Byte>(),
        paddingMode!: PaddingMode = PaddingMode.PKCS7Padding,
        aad!: Array<Byte> = Array<Byte>(),
        tagSize!: Int64 = 16
    )
}
```

功能：提供国密 SM4 对称加解密。

目前 SM4 支持 的加解密工作模式由 [OperationMode](crypto_package_structs.md#struct-operationmode) 定义，目前支持 ECB、CBC、OFB、CFB、CTR、GCM 模式。

不同的工作模式可能对应的加解密实现不同，安全性也不同。需要选择和场景适配的加解密工作模式。

iv 初始化向量在 GCM 模式下可以设置推荐长度是 12 字节，在 CBC、OFB、CFB、CTR 模式下 iv 长度是 16 字节，在 ECB 模式下 iv 可以不设置。

paddingMode 填充模式模式由 [PaddingMode](crypto_package_structs.md#struct-paddingmode) 定义， 目前支持 NoPadding 非填充、PKCS7Padding PKCS7 填充。默认是 PKCS7 填充。

paddingMode 设置对 ECB 和 CBC 有效，ECB 和 CBC 分组加解密需要分组长度等于 blockSize。会根据填充模式进行填充。 paddingMode 设置对 OFB、CFB、CTR、GCM 工作模式无效，这些工作模式均无需填充。

如果选择 NoPadding 模式，即不填充。则在 ECB 和 CBC 工作模式下用户需要对数据是否可以分组负责，如果数据不能分组，或者最后一组数据长度不足 blockSize 则会报错。

aad 附加数据，仅在 GCM 模式下使用，由用户填充，参与摘要计算，默认为空。

tagSize 设置摘要长度，仅在 GCM 模式下使用，默认值为 SM4_GCM_TAG_SIZE 16 字节，最小不能低于 12 字节，最大不能超过 16 字节。

如果是 GCM 工作模式。加密结果的后 tagSize 字节是摘要数据。

使用示例见 [SM4 使用](../crypto_samples/sample_crypto.md)。

> **注意：**
>
> GCM 模式需要 OpenSSL 3.2 或者以上版本。

父类型：

- BlockCipher

### init(OperationMode, Array\<Byte>, Array\<Byte>, PaddingMode, Array\<Byte>, Int64)

```cangjie
public init(
    optMode: OperationMode,
    key: Array<Byte>,
    iv!: Array<Byte> = Array<Byte>(),
    paddingMode!: PaddingMode = PaddingMode.PKCS7Padding,
    aad!: Array<Byte> = Array<Byte>(),
    tagSize!: Int64 = 16
)
```

功能：创建 [SM4](crypto_package_classes.md#class-sm4) 实例，可指定在不同工作模式下参数。

参数：

- optMode: [OperationMode](crypto_package_structs.md#struct-operationmode) - 设置加解密工作模式。
- key: Array\<Byte> - 密钥，长度为 16 字节。
- iv!: Array\<Byte> - 初始化向量。
- paddingMode!: [PaddingMode](crypto_package_structs.md#struct-paddingmode) - 设置填充模式。
- aad!: Array\<Byte> - 设置附加数据。
- tagSize!: Int64 - 设置摘要长度。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 参数设置不正确，实例化失败。

### prop aad

```cangjie
public prop aad: Array<Byte>
```

功能：附加数据。

类型：Array\<Byte>

### prop algorithm

```cangjie
public prop algorithm: String
```

功能：获取分组加解密算法的算法名称。

类型：String

### prop blockSize

```cangjie
public prop blockSize: Int64
```

功能：分组长度，单位字节。

类型：Int64

### prop keySize

```cangjie
public prop keySize: Int64
```

功能：密钥长度。

类型：Int64

### prop key

```cangjie
public prop key: Array<Byte>
```

功能：密钥。

类型：Array\<Byte>

### prop optMode

```cangjie
public prop optMode: OperationMode
```

功能：工作模式。

类型：[OperationMode](crypto_package_structs.md#struct-operationmode)

### prop paddingMode

```cangjie
public prop paddingMode: PaddingMode
```

功能：填充模式。

类型：[PaddingMode](crypto_package_structs.md#struct-paddingmode)

### prop iv

```cangjie
public prop iv: Array<Byte>
```

功能：初始化向量。

类型：Array\<Byte>

### prop ivSize

```cangjie
public prop ivSize: Int64
```

功能：初始化向量长度。

类型：Int64

### prop tagSize

```cangjie
public prop tagSize: Int64
```

功能：摘要长度。

类型：Int64

### func encrypt(Array\<Byte>)

```cangjie
public func encrypt(input: Array<Byte>): Array<Byte>
```

功能：加密一段数据数据。

参数：

- input: Array\<Byte> - 输入字节序列。

返回值：

- Array\<Byte> - 加密后的结果。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 加密失败，抛出异常。

### func encrypt(Array\<Byte>, Array\<Byte>)

```cangjie
public func encrypt(input: Array<Byte>, to!: Array<Byte>): Int64
```

功能：加密一段数据数据，指定输出数组长度会影响加解密结果。一般而言选填充模式，指定的密文数组长度不能小于明文数组长度加上一个 blockSize。

参数：

- input: Array\<Byte> - 待进行加密的数据。
- to!: Array\<Byte> - 输出数组。

返回值：

- Int64 - 输出长度。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 加密失败，抛出异常。
- IllegalArgumentException - 当 to 的 size = 0 时，抛出异常。

### func encrypt(InputStream, OutputStream)

```cangjie
public func encrypt(input: InputStream, output: OutputStream): Unit
```

功能：对输入流进行加密，一般如果数据过大无法一次对其加密，可以对数据流进行加密。

参数：

- input:InputStream  - 待加密的输入数据流。
- output: OutputStream - 解密后的输出数据流。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 加密失败，抛出异常。

### func decrypt(Array\<Byte>)

```cangjie
public func decrypt(input: Array<Byte>): Array<Byte>
```

功能：解密一段数据数据。

参数：

- input: Array\<Byte> - 输入字节序列。

返回值：

- Array\<Byte> - 解密后的结果。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解密失败，抛出异常。

### func decrypt(Array\<Byte>, Array\<Byte>)

```cangjie
public func decrypt(input: Array<Byte>,  to!: Array<Byte>): Int64
```

功能：解密一段数据数据，指定输出数组长度会影响加解密结果。一般而言，指定的明文数组长度不能小于密文数组长度减去一个 blockSize。

参数：

- input: Array\<Byte> - 待进行解密的数据。
- to!: Array\<Byte> - 输出数组。

返回值：

- Int64 - 输出长度。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解密失败，抛出异常。
- IllegalArgumentException - 当 to 的 size = 0 时，抛出异常。

### func decrypt(InputStream, OutputStream)

```cangjie
public func decrypt(input: InputStream, output: OutputStream): Unit
```

功能：对输入流进行解密，一般如果数据过大无法一次对其解密，可以对数据流进行解密。

参数：

- input:InputStream  - 待解密的输入数据流。
- output: OutputStream - 解密后的输出数据流。

异常：

- [CryptoException](../../digest/digest_package_api/digest_package_exceptions.md#class-cryptoexception) - 解密失败，抛出异常。
