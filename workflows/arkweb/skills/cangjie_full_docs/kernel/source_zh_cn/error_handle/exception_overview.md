# 定义异常

异常是一类特殊的可以被程序员捕获并处理的错误，是程序执行时出现的一系列不正常行为的统称。例如，数组越界、除零错误、计算溢出、非法输入等。为了保证系统的正确性和健壮性，很多软件系统中都包含大量的代码用于错误检测和错误处理。

异常不属于程序的正常功能，一旦发生异常，要求程序必须立即处理，即将程序的控制权从正常功能的执行处转移至处理异常的部分。仓颉编程语言提供了异常处理机制，用于处理程序运行时可能出现的各种异常情况。

在仓颉语言中，异常类包括 `Error` 和 `Exception`：

- `Error` 类描述仓颉语言运行时，系统内部错误和资源耗尽错误。应用程序不应该抛出这种类型错误，如果出现内部错误，只能通知给用户，尽量安全终止程序。
- `Exception` 类描述的是程序运行时的逻辑错误或者 IO 错误导致的异常，例如数组越界或者试图打开一个不存在的文件等，这类异常需要在程序中捕获处理。

开发者不可以通过继承仓颉语言内置的 Error 或其子类来自定义异常，但是可以继承内置的 Exception 或其子类来自定义异常，例如：

<!-- compile -->

```cangjie
open class FatherException <: Exception {
    public init() {
        super("This is FatherException.")
    }
    public init(message: String) {
        super(message)
    }
    public open override func getClassName(): String {
        "FatherException"
    }
}

class ChildException <: FatherException {
    public init() {
        super("This is ChildException.")
    }
    public open override func getClassName(): String {
        "ChildException"
    }
}
```

下表展示了 `Exception` 的主要函数及其说明：

| 函数种类 | 函数及说明                                                                     |
| :------- |:--------------------------------------------------------------------------|
| 构造函数 | `init()` 默认构造函数。                                                          |
| 构造函数 | `init(message: String)`  可以设置异常消息的构造函数。                                   |
| 成员属性 | `open prop message: String`  返回发生异常的详细信息。该消息在异常类构造函数中初始化，默认为空字符串。          |
| 成员函数 | `open func toString(): String`  返回异常类型名以及异常的详细信息，其中，异常的详细信息会默认调用 message。 |
| 成员函数 | `func getClassName(): String`  返回用户定义的类名，子类需要重写该方法以返回子类的名称。               |
| 成员函数 | `func printStackTrace(): Unit` 打印堆栈信息至标准错误流。                              |

下表展示了 `Error` 的主要函数及其说明：

| 函数种类 | 函数及说明                                                   |
| :------- | :----------------------------------------------------------- |
| 成员属性 | `open prop message: String`  返回发生错误的详细信息。该消息在错误发生时，内部初始化，默认为空字符串。 |
| 成员函数 | `open func toString(): String`  返回错误类型名以及错误的详细信息，其中，错误的详细信息会默认调用 message。 |
| 成员函数 | `func printStackTrace(): Unit` 打印堆栈信息至标准错误流。    |
