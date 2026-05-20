# 异常类

## class ExpectationFailedException

```cangjie
public open class ExpectationFailedException <: PrettyException {}
```

功能：在测试执行期间违反了 mock 配置期间设置的一个或多个期望。

父类型：

- [PrettyException](#class-prettyexception)

## class MockFrameworkException

```cangjie
public class MockFrameworkException <: PrettyException {}
```

功能：框架异常信息，用户使用 API 不满足框架要求时，抛出该异常。

父类型：

- [PrettyException](#class-prettyexception)

## class MockFrameworkInternalError

```cangjie
public class MockFrameworkInternalError <: PrettyException {}
```

功能：框架异常信息，用户不应期望该异常被抛出。

父类型：

- [PrettyException](#class-prettyexception)

## class PrettyException

```cangjie
public abstract class PrettyException <: Exception & PrettyPrintable {}
```

功能：支持 [PrettyPrintable](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-prettyprintable) 的异常类型，可以较好得打印异常信息。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)
- [PrettyPrintable](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-prettyprintable)

### func pprint(PrettyPrinter)

```cangjie
public func pprint(to: PrettyPrinter): PrettyPrinter
```

功能：支持较好得颜色打印、缩进格式打印异常信息。

参数：

- to: [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) - 增加颜色和缩进的打印器。

返回值：

- [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) - 增加颜色和缩进的打印器。

## class UnhandledCallException

```cangjie
public class UnhandledCallException <: PrettyException {}
```

功能：提供的[桩](../unittest_mock_samples/mock_framework_basics.md#配置-api)均未处理该调用。

父类型：

- [PrettyException](#class-prettyexception)

## class UnnecessaryStubbingException

```cangjie
public class UnnecessaryStubbingException <: PrettyException {}
```

功能：指示被测试的代码从未触发[桩](../unittest_mock_samples/mock_framework_basics.md#配置-api)。

父类型：

- [PrettyException](#class-prettyexception)

## class UnstubbedInvocationException

```cangjie
public class UnstubbedInvocationException <: PrettyException {}
```

功能：未提供与此调用匹配的[桩](../unittest_mock_samples/mock_framework_basics.md#配置-api)。

父类型：

- [PrettyException](#class-prettyexception)

## class VerificationFailedException

```cangjie
public class VerificationFailedException <: PrettyException {}
```

功能：验证失败时，框架所抛出的异常。

父类型：

- [PrettyException](#class-prettyexception)
