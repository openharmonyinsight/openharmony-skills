# 异常类

## class SocketException

```cangjie
public class SocketException <: IOException {
    public init()
    public init(message: String)
}
```

功能：提供套接字相关的异常处理。

父类型：

- [IOException](../../io/io_package_api/io_package_exceptions.md#class-ioexception)

### init()

```cangjie
public init()
```

功能：创建 [SocketException](net_package_exceptions.md#class-socketexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [SocketException](net_package_exceptions.md#class-socketexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常提示信息。

## class SocketTimeoutException

```cangjie
public class SocketTimeoutException <: Exception {
    public init()
    public init(message: String)
}
```

功能：提供套接字操作超时相关的异常处理。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：创建 [SocketTimeoutException](net_package_exceptions.md#class-sockettimeoutexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [SocketTimeoutException](net_package_exceptions.md#class-sockettimeoutexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常提示信息。
