# 异常类

## class CryptoException

```cangjie
public class CryptoException <: Exception {
    public init()
    public init(message: String)
}
```

功能：此类为摘要和加解密出现错误时抛出的异常。

父类型：

- Exception

### init()

```cangjie
public init()
```

功能：无参构造函数，构造[CryptoException](digest_package_exceptions.md#class-cryptoexception)异常。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造 [CryptoException](digest_package_exceptions.md#class-cryptoexception) 异常类对象。

参数：

- message: String - 异常信息。
