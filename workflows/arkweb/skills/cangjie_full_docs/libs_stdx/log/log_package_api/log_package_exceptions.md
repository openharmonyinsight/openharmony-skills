# 异常类

## class LogException

```cangjie
public open class LogException <: Exception {
    public init()
    public init(message: String)
}
```

功能：用于处理 log 相关的异常。

父类型：

- Exception

### init()

```cangjie
public init()
```

功能：无参构造函数。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [LogException](log_package_exceptions.md#class-logexception) 实例。

参数：

- message: String - 异常信息。

### func getClassName()

```cangjie
protected override func getClassName(): String
```

功能：获得类名。

返回值：

- String - 类名。