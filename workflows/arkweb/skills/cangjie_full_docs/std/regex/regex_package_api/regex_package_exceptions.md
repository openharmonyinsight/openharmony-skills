# 异常类

## class RegexException

```cangjie
public class RegexException <: Exception {
    public init()
    public init(message: String)
}
```

功能：提供正则的异常处理。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：创建  [RegexException](regex_package_exceptions.md#class-regexexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [RegexException](regex_package_exceptions.md#class-regexexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常提示信息。
