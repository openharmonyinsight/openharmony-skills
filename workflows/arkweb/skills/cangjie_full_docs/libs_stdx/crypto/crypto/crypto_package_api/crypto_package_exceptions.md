# 异常类

## class SecureRandomException

```cangjie
public class SecureRandomException <: Exception {
    public init()
    public init(message: String)
}
```

功能：crypto 包安全随机数的异常类。

父类型：

- Exception

### init()

```cangjie
public init()
```

功能：创建默认的 [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) 实例，异常提示消息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [SecureRandomException](crypto_package_exceptions.md#class-securerandomexception) 实例。

参数：

- message: String - 异常提示信息。
