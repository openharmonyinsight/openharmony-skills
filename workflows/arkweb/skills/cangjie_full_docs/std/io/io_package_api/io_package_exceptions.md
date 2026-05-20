# 异常类

## class ContentFormatException

```cangjie
public class ContentFormatException <: Exception {
    public init()
    public init(message: String)
}
```

功能：提供字符格式相关的异常处理。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：创建 [ContentFormatException](io_package_exceptions.md#class-contentformatexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [ContentFormatException](io_package_exceptions.md#class-contentformatexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常提示信息。

## class IOException

```cangjie
public open class IOException <: Exception {
    public init()
    public init(message: String)
}
```

功能：提供 IO 流相关的异常处理。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：创建 [IOException](io_package_exceptions.md#class-ioexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [IOException](io_package_exceptions.md#class-ioexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常提示信息。
