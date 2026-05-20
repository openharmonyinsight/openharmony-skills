# 异常类

## class InvalidDataException

```cangjie
public class InvalidDataException <: Exception {
    public init()
    public init(message: String)
}
```

功能：[InvalidDataException](time_package_exceptions.md#class-invaliddataexception) 表示加载时区时的异常。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个 [InvalidDataException](time_package_exceptions.md#class-invaliddataexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据参数 `message` 指定的异常信息，构造一个 [InvalidDataException](time_package_exceptions.md#class-invaliddataexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 预定义消息。

## class TimeParseException

```cangjie
public class TimeParseException <: Exception {
    public init()
    public init(message: String)
}
```

功能：[TimeParseException](time_package_exceptions.md#class-timeparseexception) 表示解析时间字符串时的异常。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个 [TimeParseException](time_package_exceptions.md#class-timeparseexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据参数 `message` 指定的异常信息，构造一个 [TimeParseException](time_package_exceptions.md#class-timeparseexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 预定义消息。
