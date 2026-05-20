# 异常类

## class ArgumentParseException

```cangjie
public class ArgumentParseException <: Exception {
    public init()
    public init(message: String)
}
```

功能：参数解析异常类。当参数解析出错（如：不识别的选项、缺少值的选项）时，抛出此异常。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个不带异常信息的实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造异常实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。
