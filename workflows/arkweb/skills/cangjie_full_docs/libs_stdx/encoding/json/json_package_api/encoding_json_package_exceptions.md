# 异常类

## class JsonException

```cangjie
public class JsonException <: Exception {
    public init()
    public init(message: String)
}
```

功能：JSON 包的异常类，用于 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 类型使用时出现异常的场景。

父类型：

- Exception

### init()

```cangjie
public init()
```

功能：构造一个不包含任何异常提示信息的 [JsonException](encoding_json_package_exceptions.md#class-jsonexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据指定的异常提示信息构造 [JsonException](encoding_json_package_exceptions.md#class-jsonexception) 实例。

参数：

- message: String - 指定的异常提示信息。
