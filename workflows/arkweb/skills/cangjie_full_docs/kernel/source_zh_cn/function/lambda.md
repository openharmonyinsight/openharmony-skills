# Lambda 表达式

## Lambda 表达式定义

Lambda 表达式是一种匿名函数（即没有函数名的函数），其核心设计目的是在程序中快速定义简短的函数逻辑，无需显式声明函数名称。这一概念起源于数学中的 λ 演算（lambda calculus），后被引入多种编程语言（如 C++、Python、C# 等），用于简化代码并提升灵活性。仓颉编程语言中也引入了 Lambda 表达式，具体使用介绍将在本小节展开介绍。

Lambda 表达式的语法为如下形式： `{ p1: T1, ..., pn: Tn => expressions | declarations }`。

其中，`=>` 之前为参数列表，多个参数之间使用 `,` 分隔，每个参数名和参数类型之间使用 `:` 分隔。`=>` 之前也可以没有参数。`=>` 之后为 Lambda 表达式体，是一组表达式或声明序列。Lambda 表达式的参数名的作用域与函数的相同，为 Lambda 表达式的函数体部分，其作用域级别可视为与 Lambda 表达式的函数体内定义的变量等同。

<!-- compile -->

```cangjie
let f1 = { a: Int64, b: Int64 => a + b }

var display = { =>   // Parameterless lambda expression.
    println("Hello")
    println("World")
}
```

Lambda 表达式不管有没有参数，都不可以省略 `=>`，除非其作为[尾随 lambda](./function_call_desugar.md#尾随-lambda)。例如：

<!-- compile -->

```cangjie
var display = { => println("Hello") }

func f2(lam: () -> Unit) {}
let f2Res = f2 { println("World") } // OK to omit the =>
```

Lambda 表达式中参数的类型标注可缺省。以下情形中，若参数类型省略，编译器会尝试进行类型推断，当编译器无法推断出类型时会编译报错：

- Lambda 表达式赋值给变量时，其参数类型根据变量类型推断；
- Lambda 表达式作为函数调用表达式的实参使用时，其参数类型根据函数的形参类型推断。

<!-- compile -->

```cangjie
// The parameter types are inferred from the type of the variable sum1
var sum1: (Int64, Int64) -> Int64 = { a, b => a + b }

var sum2: (Int64, Int64) -> Int64 = { a: Int64, b => a + b }

func f(a1: (Int64) -> Int64): Int64 {
    a1(1)
}

main(): Int64 {
    // The parameter type of lambda is inferred from the type of function f
    f({ a2 => a2 + 10 })
}
```

Lambda 表达式中不支持声明返回类型，其返回类型总是从上下文中推断出来，若无法推断则报错。

- 若上下文明确指定了 Lambda 表达式的返回类型，则其返回类型为上下文指定的类型。

    - Lambda 表达式赋值给变量时，其返回类型根据变量类型推断返回类型：

      <!-- compile -->

      ```cangjie
      let f: () -> Unit = { => println(10) }
      ```

    - Lambda 表达式作为参数使用时，其返回类型根据使用处所在的函数调用的形参类型推断：

      <!-- compile -->

      ```cangjie
      func f(a1: (Int64) -> Int64): Int64 {
        a1(1)
      }

      main(): Int64 {
        f({ a2: Int64 => a2 + 10 })
      }
      ```

    - Lambda 表达式作为返回值使用时，其返回类型根据使用处所在函数的返回类型推断：

      <!-- compile -->

      ```cangjie
      func f(): (Int64) -> Int64 {
        { a: Int64 => a }
      }
      ```

- 若上下文中类型未明确，与推导函数的返回值类型类似，编译器会根据 Lambda 表达式体中所有 return 表达式 `return xxx` 中 xxx 的类型，以及 Lambda 表达式体的类型，来共同推导出 Lambda 表达式的返回类型。

    - `=>` 右侧的内容与普通函数体的规则一样，返回类型为 `Int64`:

      <!-- compile -->

      ```cangjie
      let sum1 = { a: Int64, b: Int64 => a + b }
      ```

    - `=>` 的右侧为空，返回类型为 `Unit`:

      <!-- compile -->

      ```cangjie
      let f = { => }
      ```

## Lambda 表达式调用

Lambda 表达式支持立即调用，例如：

<!-- compile -->

```cangjie
let r1 = { a: Int64, b: Int64 => a + b }(1, 2) // r1 = 3
let r2 = { => 123 }()                          // r2 = 123
```

Lambda 表达式也可以赋值给一个变量，使用变量名进行调用，例如：

<!-- compile -->

```cangjie
func f() {
    var g = { x: Int64 => println("x = ${x}") }
    g(2)
}
```
