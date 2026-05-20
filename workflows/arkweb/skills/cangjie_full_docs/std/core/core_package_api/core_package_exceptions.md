# 异常类

## class ArithmeticException

```cangjie
public open class ArithmeticException <: Exception {
    public init()
    public init(message: String)
}
```

功能：算术异常类，发生算术异常时使用。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ArithmeticException](core_package_exceptions.md#class-arithmeticexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [ArithmeticException](core_package_exceptions.md#class-arithmeticexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class Error

```cangjie
public open class Error <: ToString
```

功能：[Error](core_package_exceptions.md#class-error) 是所有错误类的基类。该类不可被继承，不可初始化，但是可以被捕获到。

父类型：

- [ToString](core_package_interfaces.md#interface-tostring)

### prop message

```cangjie
public open prop message: String
```

功能：获取错误信息。

类型：[String](core_package_structs.md#struct-string)

### func getStackTrace()

```cangjie
public func getStackTrace(): Array<StackTraceElement>
```

功能：获取堆栈信息，每一条堆栈信息用一个 [StackTraceElement](core_package_classes.md#class-stacktraceelement) 实例表示，最终返回一个 [StackTraceElement](core_package_classes.md#class-stacktraceelement) 的数组。

返回值：

- [Array](core_package_structs.md#struct-arrayt)\<[StackTraceElement](core_package_classes.md#class-stacktraceelement)> - 堆栈信息数组。

### func getStackTraceMessage()

```cangjie
public open func getStackTraceMessage(): String
```

功能：获取堆栈信息。

返回值：

- [String](core_package_structs.md#struct-string) - 堆栈信息。

### func printStackTrace()

```cangjie
public open func printStackTrace(): Unit
```

功能：向控制台打印堆栈信息。

### func toString()

```cangjie
public open func toString(): String
```

功能：获取当前 [Error](core_package_exceptions.md#class-error) 实例的字符串值，包括类名和错误信息。

返回值：

- [String](core_package_structs.md#struct-string) - 错误信息字符串。

## class Exception

```cangjie
public open class Exception <: ToString {
    public init()
    public init(message: String)
}
```

功能：[Exception](core_package_exceptions.md#class-exception) 是所有异常类的父类。

支持构造一个异常类，设置、获取异常信息，转换为字符串，获取、打印堆栈，设置异常名（用于字符串表示）。

父类型：

- [ToString](core_package_interfaces.md#interface-tostring)

### prop message

```cangjie
public open prop message: String
```

功能：获取异常信息。

类型：[String](core_package_structs.md#struct-string)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Exception](core_package_exceptions.md#class-exception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [Exception](core_package_exceptions.md#class-exception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

### func getStackTrace()

```cangjie
public func getStackTrace(): Array<StackTraceElement>
```

功能：获取堆栈信息，每一条堆栈信息用一个 [StackTraceElement](core_package_classes.md#class-stacktraceelement) 实例表示，最终返回一个 [StackTraceElement](core_package_classes.md#class-stacktraceelement) 的数组。

返回值：

- [Array](core_package_structs.md#struct-arrayt)\<[StackTraceElement](core_package_classes.md#class-stacktraceelement)> - 堆栈信息数组。

### func printStackTrace()

```cangjie
public func printStackTrace(): Unit
```

功能：向控制台打印堆栈信息。

### func toString()

```cangjie
public open func toString(): String
```

功能：获取当前 [Exception](core_package_exceptions.md#class-exception) 实例的字符串值，包括类名和异常信息。

返回值：

- [String](core_package_structs.md#struct-string) - 异常字符串。

## class IllegalArgumentException

```cangjie
public open class IllegalArgumentException <: Exception {
    public init()
    public init(message: String)
}
```

功能：表示参数非法的异常类。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [IllegalArgumentException](core_package_exceptions.md#class-illegalargumentexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [IllegalArgumentException](core_package_exceptions.md#class-illegalargumentexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class IllegalFormatException

```cangjie
public open class IllegalFormatException <: IllegalArgumentException {
    public init()
    public init(message: String)
}
```

功能：表示变量的格式无效或不标准时的异常类。

父类型：

- [IllegalArgumentException](#class-illegalargumentexception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [IllegalFormatException](core_package_exceptions.md#class-illegalformatexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [IllegalFormatException](core_package_exceptions.md#class-illegalformatexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class IllegalMemoryException

```cangjie
public class IllegalMemoryException <: Exception {
    public init()
    public init(message: String)
}
```

功能：表示内存操作错误的异常类。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [IllegalMemoryException](core_package_exceptions.md#class-illegalmemoryexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据指定异常信息构造 [IllegalMemoryException](core_package_exceptions.md#class-illegalmemoryexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class IllegalStateException

```cangjie
public class IllegalStateException <: Exception {
    public init()
    public init(message: String)
}
```

功能：表示状态非法的异常类。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [IllegalStateException](core_package_exceptions.md#class-illegalstateexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [IllegalStateException](core_package_exceptions.md#class-illegalstateexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class IncompatiblePackageException

```cangjie
public class IncompatiblePackageException <: Exception {
    public init()
    public init(message: String)
}
```

功能：表示包不兼容的异常类。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [IncompatiblePackageException](core_package_exceptions.md#class-incompatiblepackageexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [IncompatiblePackageException](core_package_exceptions.md#class-incompatiblepackageexception)实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class IndexOutOfBoundsException

```cangjie
public class IndexOutOfBoundsException <: Exception {
    public init()
    public init(message: String)
}
```

功能：表示索引越界的异常类。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [IndexOutOfBoundsException](core_package_exceptions.md#class-indexoutofboundsexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [IndexOutOfBoundsException](core_package_exceptions.md#class-indexoutofboundsexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class NegativeArraySizeException

```cangjie
public class NegativeArraySizeException <: Exception {
    public init()
    public init(message: String)
}
```

功能：表示数组大小为负数的异常类。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [NegativeArraySizeException](core_package_exceptions.md#class-negativearraysizeexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [NegativeArraySizeException](core_package_exceptions.md#class-negativearraysizeexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class NoneValueException

```cangjie
public class NoneValueException <: Exception {
    public init()
    public init(message: String)
}
```

功能：表示 [Option](core_package_enums.md#enum-optiont)\<T> 实例的值为 `None` 的异常类，通常在 `getOrThrow` 函数中被抛出。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [NoneValueException](core_package_exceptions.md#class-nonevalueexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [NoneValueException](core_package_exceptions.md#class-nonevalueexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class OutOfMemoryError

```cangjie
public class OutOfMemoryError <: Error {}
```

功能：表示内存不足错误的错误类，该类不可被继承，不可初始化，但是可以被捕获到。

父类型：

- [Error](#class-error)

## class OverflowException

```cangjie
public class OverflowException <: ArithmeticException {
    public init()
    public init(message: String)
}
```

功能：表示算术运算溢出的异常类。

父类型：

- [ArithmeticException](#class-arithmeticexception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [OverflowException](core_package_exceptions.md#class-overflowexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据指定异常信息构造 [OverflowException](core_package_exceptions.md#class-overflowexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class SpawnException

```cangjie
public class SpawnException <: Exception {
    public init()
    public init(message: String)
}
```

功能：线程异常类，表示线程处理过程中发生异常。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [SpawnException](core_package_exceptions.md#class-spawnexception) 实例，默认错误信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息构造一个 [SpawnException](core_package_exceptions.md#class-spawnexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class StackOverflowError

```cangjie
public class StackOverflowError <: Error {}
```

功能：表示堆栈溢出错误的错误类，该类不可被继承，不可初始化，但是可以被捕获到。

父类型：

- [Error](#class-error)

### func printStackTrace()

```cangjie
public override func printStackTrace(): Unit
```

功能：向控制台打印堆栈信息。

## class TimeoutException

```cangjie
public class TimeoutException <: Exception {
    public init()
    public init(message: String)
}
```

功能：当阻塞操作超时时引发异常。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [TimeoutException](core_package_exceptions.md#class-timeoutexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据指定异常信息构造 [TimeoutException](core_package_exceptions.md#class-timeoutexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。

## class UnsupportedException

```cangjie
public class UnsupportedException <: Exception {
    public init()
    public init(message: String)
}
```

功能：表示功能未支持的异常类。

父类型：

- [Exception](#class-exception)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [UnsupportedException](core_package_exceptions.md#class-unsupportedexception) 实例，默认异常信息为空。

### init(String)

```cangjie
public init(message: String)
```

功能：根据指定异常信息构造 [UnsupportedException](core_package_exceptions.md#class-unsupportedexception) 实例。

参数：

- message: [String](core_package_structs.md#struct-string) - 异常提示信息。
