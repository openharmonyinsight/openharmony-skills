# 异常类

## class UrlSyntaxException

```cangjie
public class UrlSyntaxException <: Exception {
    public init(reason: String)
    public init(input: String, reason: String)
    public init(input: String, reason: String, pos: String)
}
```

功能：URL 解析异常类。

父类型：

- Exception

### init(String)

```cangjie
public init(reason: String)
```

功能：根据错误原因构造 [UrlSyntaxException](url_package_exceptions.md#class-urlsyntaxexception) 实例。

参数：

- reason: String - 解析错误的原因。

### init(String, String)

```cangjie
public init(input: String, reason: String)
```

功能：根据 URL 及错误原因构造 [UrlSyntaxException](url_package_exceptions.md#class-urlsyntaxexception) 实例。

参数：

- input: String - 原生 URL 或其片段。
- reason: String - 解析错误的原因。

### init(String, String, String)

```cangjie
public init(input: String, reason: String, pos: String)
```

功能：根据 URL 字符串，错误原因以及解析失败的部分，构造 [UrlSyntaxException](url_package_exceptions.md#class-urlsyntaxexception) 实例。

参数：

- input: String - 原生 URL 或其片段。
- reason: String - 解析错误的原因。
- pos: String - 给定 URL 字符串中解析失败的部分。
