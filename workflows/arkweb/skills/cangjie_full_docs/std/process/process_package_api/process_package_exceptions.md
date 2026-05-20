# 异常类

## class ProcessException

```cangjie
public class ProcessException <: IOException {
    public init(message: String)
}
```

功能：`process` 包的异常类。

父类型：

- [IOException](../../io/io_package_api/io_package_exceptions.md#class-ioexception)

### init(String)

```cangjie
public init(message: String)
```

功能：创建 [ProcessException](process_package_exceptions.md#class-processexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常提示信息。
