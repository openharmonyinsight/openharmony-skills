# 异常类

## class TlsException

```cangjie
public class TlsException <: Exception {
    public init()
    public init(message: String)
}
```

功能：TLS 处理出现错误时抛出的异常。

父类型：

- Exception

### init()

```cangjie
public init()
```

功能：创建 [TlsException](tls_package_exceptions.md#class-tlsexception) 实例，异常提示消息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 TlsException 实例。

参数：

- message: String - 异常信息。
