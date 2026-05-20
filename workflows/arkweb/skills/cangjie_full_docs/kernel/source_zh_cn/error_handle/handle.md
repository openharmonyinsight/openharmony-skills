# throw 和处理异常

上文介绍了如何自定义异常，接下来学习如何抛出和处理异常。

- 由于异常是 `class` 类型，只需要按 class 对象的构建方式去创建异常即可。如表达式 `FatherException()` 即创建了一个类型为 `FatherException` 的异常。
- 仓颉语言提供 `throw` 关键字，用于抛出异常。用 `throw` 来抛出异常时，`throw` 之后的表达式必须是 `Exception` 的子类型（同为异常的 `Error` 不可以手动 `throw` ），如 `throw ArithmeticException("I am an Exception!")` （被执行到时）会抛出一个算术运算异常。
- `throw` 关键字抛出的异常需要被捕获处理。若异常没有被捕获，则由系统调用默认的异常处理函数。

  > **注意：**
  >
  > 开发者可以调用如下 `Thread` 类的静态函数，对未捕获的 `Exception` 注册自定义的异常处理函数：
  >
  > - `public static func handleUncaughtExceptionBy(exHandler: (Thread, Exception) -> Unit): Unit`

异常处理由 `try` 表达式完成，可分为：

- 不涉及资源自动管理的普通 try 表达式。
- 会进行资源自动管理 try-with-resources 表达式。

## 普通 try 表达式

普通 try 表达式包括三个部分：try 块，catch 块和 finally 块。

- try 块，以关键字 `try` 开始，后面紧跟一个由表达式与声明组成的块（用一对花括号括起来，定义了新的局部作用域，可以包含任意表达式和声明，后简称“块”），try 后面的块内可以抛出异常，并被紧随的 catch 块所捕获并处理（如果不存在 catch 块或未被捕获，则在执行完 finally 块后，该异常继续被抛出）。

- catch 块，一个普通 try 表达式可以包含零个或多个 catch 块（当没有 catch 块时必须有 finally 块）。每个 catch 块以关键字 `catch` 开头，后跟一条 `catchPattern` 和一个块，`catchPattern` 通过模式匹配的方式匹配待捕获的异常。一旦匹配成功，则交由其后跟随的块进行处理，并且忽略它后面的其他 catch 块。当某个 catch 块可捕获的异常类型均可被定义在它前面的某个 catch 块所捕获时，会在此 catch 块处报“catch 块不可达”的 warning。

- finally 块，以关键字 `finally` 开始，后面紧跟一个块。原则上，finally 块中主要实现一些“善后”的工作，如释放资源等，且要尽量避免在 finally 块中再抛异常。并且无论异常是否发生（即无论 try 块中是否抛出异常），finally 块内的内容都会被执行（若异常未被处理，执行完 finally 块后，继续向外抛出异常）。一个 try 表达式在包含 catch 块时可以不包含 finally 块，否则必须包含 finally 块。

`try` 后面紧跟的块以及每个 `catch` 块的作用域互相独立。

下面是一个只有 try 块和 catch 块的简单示例：

<!-- verify -->

```cangjie
main() {
    try {
        throw NegativeArraySizeException("I am an Exception!")
    } catch (e: NegativeArraySizeException) {
        println(e)
        println("NegativeArraySizeException is caught!")
    }
    println("This will also be printed!")
}
```

执行结果为：

```text
NegativeArraySizeException: I am an Exception!
NegativeArraySizeException is caught!
This will also be printed!
```

`catchPattern` 中引入的变量作用域级别与 `catch` 后面的块中变量作用域级别相同，在 catch 块中再次引入相同名字会触发重定义错误。例如：

<!-- compile.error -->

```cangjie
main() {
    try {
        throw NegativeArraySizeException("I am an Exception!")
    } catch (e: NegativeArraySizeException) {
        println(e)
        let e = 0 // Error, redefinition
        println(e)
        println("NegativeArraySizeException is caught!")
    }
    println("This will also be printed!")
}
```

下面是带有 finally 块的 try 表达式的简单示例：

<!-- verify -->

```cangjie
main() {
    try {
        throw NegativeArraySizeException("NegativeArraySizeException")
    } catch (e: NegativeArraySizeException) {
        println("Exception info: ${e}.")
    } finally {
        println("The finally block is executed.")
    }
}
```

执行结果为：

```text
Exception info: NegativeArraySizeException: NegativeArraySizeException.
The finally block is executed.
```

try 表达式可以出现在任何允许使用表达式的地方。try 表达式的类型的确定方式，与 `if`、`match` 表达式等多分支语法结构的类型的确定方式相似，为 finally 分支除外的所有分支的类型的最小公共父类型。例如下面代码中的 try 表达式和变量 `x` 的类型均为 E 和 D 的最小公共父类型 D；finally 分支中的 `C()` 并不参与公共父类型的计算（若参与，则最小公共父类型会变为 `C`）。

另外，当 `try` 表达式的值没有被使用时，其类型为 `Unit`，不要求各分支的类型有最小公共父类型。

<!-- compile -->

```cangjie
open class C { }
open class D <: C { }
class E <: D { }
main () {
    let x = try {
        E()
    } catch (e: Exception) {
        D()
    } finally {
        C()
    }
    0
}
```

## try-with-resources 表达式

try-with-resources 表达式主要是为了自动释放非内存资源。不同于普通 try 表达式，try-with-resources 表达式中的 catch 块和 finally 块均是可选的，并且 try 关键字其后的块之间可以插入一个或者多个 `ResourceSpecification` 用来申请一系列的资源（`ResourceSpecification` 并不会影响整个 try 表达式的类型）。这里所讲的资源对应到语言层面即指对象，因此 `ResourceSpecification` 其实就是实例化一系列的对象（多个实例化之间使用“,”分隔）。使用 try-with-resources 表达式的例子如下所示：

<!-- compile -->

```cangjie
class Worker <: Resource {
    var hasTools: Bool = false
    let name: String

    public init(name: String) {
        this.name = name
    }
    public func getTools() {
        println("${name} picks up tools from the warehouse.")
        hasTools = true
    }

    public func work() {
        if (hasTools) {
            println("${name} does some work with tools.")
        } else {
            println("${name} doesn't have tools, does nothing.")
        }
    }

    public func isClosed(): Bool {
        if (hasTools) {
            println("${name} hasn't returned the tool.")
            false
        } else {
            println("${name} has no tools")
            true
        }
    }
    public func close(): Unit {
        println("${name} returns the tools to the warehouse.")
        hasTools = false
    }
}

main() {
    try (r = Worker("Tom")) {
        r.getTools()
        r.work()
    }
    try (r = Worker("Bob")) {
        r.work()
    }
    try (r = Worker("Jack")) {
        r.getTools()
        throw Exception("Jack left, because of an emergency.")
    }
}
```

程序输出结果为：

```text
Tom picks up tools from the warehouse.
Tom does some work with tools.
Tom hasn't returned the tool.
Tom returns the tools to the warehouse.
Bob doesn't have tools, does nothing.
Bob has no tools
Jack picks up tools from the warehouse.
Jack hasn't returned the tool.
Jack returns the tools to the warehouse.
An exception has occurred:
Exception: Jack left, because of an emergency.
         at test.main()(xxx/xx.cj:xx)
```

`try` 关键字和 `{}` 之间引入的名字，其作用域与 `{}` 中引入的变量作用域级别相同，在 `{}` 中再次引入相同名字会触发重定义错误。

<!-- compile.error -->

```cangjie
class R <: Resource {
    public func isClosed(): Bool {
        true
    }
    public func close(): Unit {
        print("R is closed")
    }
}

main() {
    try (r = R()) {
        println("Get the resource")
        let r = 0 // Error, redefinition
        println(r)
    }
}
```

try-with-resources 表达式中的 `ResourceSpecification` 的类型必须实现 Resource 接口：

<!-- run -->

```cangjie
interface Resource {
    func isClosed(): Bool  // 离开 try-with-resources 作用域时，判断是否需要调用 close 函数释放资源
    func close(): Unit  // 在 isClosed 返回 false 的场景下释放资源。
}
```

需要说明的是，try-with-resources 表达式中一般没有必要再包含 catch 块和 finally 块，也不建议开发者再手动释放资源（逻辑冗余）。但是，如果需要显式地捕获 try 块或资源申请和释放过程中可能抛出的异常并处理，仍可在 try-with-resources 表达式中包含 catch 块和 finally 块：

<!-- verify -->

```cangjie
class R <: Resource {
    public func isClosed(): Bool {
        true
    }
    public func close(): Unit {
        print("R is closed")
    }
}

main() {
    try (r = R()) {
        println("Get the resource")
    } catch (e: Exception) {
        println("Exception happened when executing the try-with-resources expression")
    } finally {
        println("End of the try-with-resources expression")
    }
}
```

程序输出结果如下：

```text
Get the resource
End of the try-with-resources expression
```

try-with-resources 表达式的类型是 `Unit`。

## CatchPattern 进阶介绍

大多数时候，只想捕获某一类型和其子类型的异常，这时候使用 CatchPattern 的**类型模式**来处理；但有时也需要所有异常做统一处理（如此处不该出现异常，出现了就统一报错），这时可以使用 CatchPattern 的**通配符模式**来处理。

类型模式在语法上有两种格式：

- `Identifier: ExceptionClass`。此格式可以捕获类型为 `ExceptionClass` 及其子类的异常，并将捕获到的异常实例转换成 `ExceptionClass`，然后与 `Identifier` 定义的变量进行绑定，接着就可以在 catch 块中通过 Identifier 定义的变量访问捕获到的异常实例。
- `Identifier: ExceptionClass_1 | ExceptionClass_2 | ... | ExceptionClass_n`。此格式可以通过连接符 `|` 将多个异常类进行拼接，连接符 `|` 表示“或”的关系：可以捕获类型为 `ExceptionClass_1` 及其子类的异常，或者捕获类型为 `ExceptionClass_2` 及其子类的异常，依次类推，或捕获类型为 `ExceptionClass_n` 及其子类的异常（假设 n 大于 1）。当待捕获异常的类型属于上述“或”关系中的任一类型或其子类型时，此异常将被捕获。但是由于无法静态地确定被捕获异常的类型，所以被捕获异常的类型会被转换成由 `|` 连接的所有类型的最小公共父类，并将异常实例与 `Identifier` 定义的变量进行绑定。因此在此类模式下，catch 块内只能通过 `Identifier` 定义的变量访问 `ExceptionClass_i（1 <= i <= n）` 的最小公共父类中的成员变量和成员函数。当然，也可以使用通配符代替类型模式中的 `Identifier`，差别仅在于通配符不会进行绑定操作。

示例如下：

<!-- verify -->

```cangjie
main(): Int64 {
    try {
        throw IllegalArgumentException("This is an Exception!")
    } catch (e: OverflowException) {
        println(e.message)
        println("OverflowException is caught!")
    } catch (e: IllegalArgumentException | NegativeArraySizeException) {
        println(e.message)
        println("IllegalArgumentException or NegativeArraySizeException is caught!")
    } finally {
        println("finally is executed!")
    }
    return 0
}
```

执行结果：

```text
This is an Exception!
IllegalArgumentException or NegativeArraySizeException is caught!
finally is executed!
```

关于“被捕获异常的类型是由 `|` 连接的所有类型的最小公共父类”的示例：

<!-- verify -->

```cangjie
open class Father <: Exception {
    var father: Int32 = 0
}

class ChildOne <: Father {
    var childOne: Int32 = 1
}

class ChildTwo <: Father {
    var childTwo: Int32 = 2
}

main() {
    try {
        throw ChildOne()
    } catch (e: ChildTwo | ChildOne) {
        println("${e is Father}")
    }
}
```

执行结果：

```text
true
```

**通配符模式**的语法是 `_`，它可以捕获同级 try 块内抛出的任意类型的异常，等价于类型模式中的 `e: Exception`，即捕获 Exception 子类所定义的异常。示例如下：

<!-- compile -->

```cangjie
// Catch with wildcardPattern.
try {
    throw OverflowException()
} catch (_) {
    println("catch an exception!")
}
```
