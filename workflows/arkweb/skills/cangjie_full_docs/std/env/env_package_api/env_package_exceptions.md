# 异常类

## class EnvException

```cangjie
public class EnvException <: Exception {
    public init(message: String)
}
```

功能：`env` 包的异常类。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init(String)

```cangjie
public init(message: String)
```

功能：创建 [EnvException](../../process/process_package_api/process_package_exceptions.md#class-processexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常提示信息。
