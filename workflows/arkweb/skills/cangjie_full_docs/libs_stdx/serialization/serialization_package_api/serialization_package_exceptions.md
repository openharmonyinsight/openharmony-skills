# 异常类

## class DataModelException

```cangjie
public class DataModelException <: Exception {
    public init()
    public init(message: String)
}
```

功能：[DataModel](serialization_package_classes.md#class-datamodel) 的异常类。

父类型：

- Exception

### init()

```cangjie
public init()
```

功能：创建 [DataModelException](serialization_package_exceptions.md#class-datamodelexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [DataModelException](serialization_package_exceptions.md#class-datamodelexception) 实例。

参数：

- message: String - 异常信息提示字符串。
