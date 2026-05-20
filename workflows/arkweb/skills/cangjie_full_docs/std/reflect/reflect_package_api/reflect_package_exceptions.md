# 异常类

## class IllegalSetException

```cangjie
public class IllegalSetException <: ReflectException {
    public init()
    public init(message: String)
}
```

功能：[IllegalSetException](reflect_package_exceptions.md#class-illegalsetexception) 为对不可变类型进行更改异常。

父类型：

- [ReflectException](#class-reflectexception)

### init()

```cangjie
public init()
```

功能：创建 [IllegalSetException](reflect_package_exceptions.md#class-illegalsetexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [IllegalSetException](reflect_package_exceptions.md#class-illegalsetexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。

## class IllegalTypeException

```cangjie
public class IllegalTypeException <: ReflectException {
    public init()
    public init(message: String)
}
```

功能：[IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) 为类型不匹配异常。

父类型：

- [ReflectException](#class-reflectexception)

### init()

```cangjie
public init()
```

功能：创建 [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。

## class InfoNotFoundException

```cangjie
public class InfoNotFoundException <: ReflectException {
    public init()
    public init(message: String)
}
```

功能：[InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) 为无法找到对应信息异常。

父类型：

- [ReflectException](#class-reflectexception)

### init()

```cangjie
public init()
```

功能：创建 [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。

## class InvocationTargetException

```cangjie
public class InvocationTargetException <: ReflectException {
    public init()
    public init(message: String)
}
```

功能：[InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) 为调用函数包装异常。

父类型：

- [ReflectException](#class-reflectexception)

### init()

```cangjie
public init()
```

功能：创建 [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。

## class MisMatchException

```cangjie
public class MisMatchException <: ReflectException {
    public init()
    public init(message: String)
}
```

功能：[MisMatchException](reflect_package_exceptions.md#class-mismatchexception) 为调用对应函数抛出异常。

父类型：

- [ReflectException](#class-reflectexception)

### init()

```cangjie
public init()
```

功能：创建 [MisMatchException](reflect_package_exceptions.md#class-mismatchexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [MisMatchException](reflect_package_exceptions.md#class-mismatchexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。

## class ReflectException

```cangjie
public open class ReflectException <: Exception {
    public init()
    public init(message: String)
}
```

功能：[ReflectException](reflect_package_exceptions.md#class-reflectexception) 为 Reflect 包的基异常类。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：创建 [ReflectException](reflect_package_exceptions.md#class-reflectexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [ReflectException](reflect_package_exceptions.md#class-reflectexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。
