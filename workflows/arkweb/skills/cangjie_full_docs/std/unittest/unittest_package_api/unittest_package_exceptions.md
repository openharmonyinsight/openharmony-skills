# 异常类

## class AssertException

```cangjie
public class AssertException <: Exception {
    public init()
    public init(message: String)
}
```

功能：[@Expect](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) / [@Assert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏) 检查失败时所抛出的异常。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：构造函数。

### init(String)

```cangjie
public init(message: String)
```

功能：构造函数。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定的异常信息。

## class AssertIntermediateException

```cangjie
public class AssertIntermediateException <: Exception {
    public let expression: String
    public let originalException: Exception
}
```

功能：[@PowerAssert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#powerassert-宏) 检查失败时所抛出的异常。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### let expression

```cangjie
public let expression: String
```

功能：检查的表达式。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### let originalException

```cangjie
public let originalException: Exception
```

功能：原始的类型信息。

类型：[Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)。

### func getOriginalStackTrace()

```cangjie
public func getOriginalStackTrace(): String
```

功能：获取原始的栈信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 栈信息。

## class UnittestCliOptionsFormatException

```cangjie
public class UnittestCliOptionsFormatException <: UnittestException
```

功能：控制台选项格式错误抛出的异常。

父类型：

- [UnittestException](#class-unittestexception)

## class UnittestException

```cangjie
public open class UnittestException <: Exception
```

功能：框架通用异常。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### func getClassName()

```cangjie
protected override open func getClassName(): String
```

功能：获得类名。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 类名字符串。