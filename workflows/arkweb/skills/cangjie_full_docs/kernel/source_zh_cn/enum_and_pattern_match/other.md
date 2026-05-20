# 其他使用模式的地方

模式除了可以在 `match` 表达式中使用外，还可以使用在变量定义和 `for in` 表达式中，例如，等号左侧是个模式，`for` 关键字和 `in` 关键字之间是个模式。同时， `if` 表达式和 `while` 表达式中的条件也可以使用模式，具体详见 [“let pattern” 的“条件”示例](../basic_programming_concepts/expression.md#涉及-let-pattern-的条件示例)。

但是，并不是所有的模式都能使用在变量定义和 `for in` 表达式中，只有 `irrefutable` 的模式才能在这两处被使用，所以只有通配符模式、绑定模式、`irrefutable` tuple 模式和 `irrefutable` enum 模式是允许的。

1. 变量定义和 `for in` 表达式中使用通配符模式的例子如下：

    <!-- verify -->

    ```cangjie
    main() {
        let _ = 100
        for (_ in 1..5) {
            println("0")
        }
    }
    ```

   上例中，变量定义时使用了通配符模式，表示定义了一个没有名字的变量（当然此后也就没办法对其进行访问），`for in` 表达式中使用了通配符模式，表示不会将 `1..5` 中的元素与某个变量绑定（当然循环体中就无法访问 `1..5` 中元素值）。编译执行上述代码，输出结果为：

    ```text
    0
    0
    0
    0
    ```

2. 变量定义和 `for in` 表达式中使用绑定模式的例子如下：

    <!-- verify -->

    ```cangjie
    main() {
        let x = 100
        println("x = ${x}")
        for (i in 1..5) {
            println(i)
        }
    }
    ```

   上例中，变量定义中的 `x` 以及 `for in` 表达式中的 `i` 都是绑定模式。编译执行上述代码，输出结果为：

    ```text
    x = 100
    1
    2
    3
    4
    ```

3. 变量定义和 `for in` 表达式中使用 `irrefutable` tuple 模式的例子如下：

    <!-- verify -->

    ```cangjie
    main() {
        let (x, y) = (100, 200)
        println("x = ${x}")
        println("y = ${y}")
        for ((i, j) in [(1, 2), (3, 4), (5, 6)]) {
            println("Sum = ${i + j}")
        }
    }

    ```

   上例中，变量定义时使用了 tuple 模式，表示对 `(100, 200)` 进行解构并分别和 `x` 与 `y` 进行绑定，效果上相当于定义了两个变量 `x` 和 `y`。`for in` 表达式中使用了 tuple 模式，表示依次将 `[(1, 2), (3, 4), (5, 6)]` 中的 tuple 类型的元素取出，然后解构并分别和 `i` 与 `j` 进行绑定，循环体中输出 `i + j` 的值。编译执行上述代码，输出结果为：

    ```text
    x = 100
    y = 200
    Sum = 3
    Sum = 7
    Sum = 11
    ```

4. 变量定义和 `for in` 表达式中使用 `irrefutable` enum 模式的例子如下：

    <!-- verify -->

    ```cangjie
    enum RedColor {
        Red(Int64)
    }
    main() {
        let Red(red) = Red(0)
        println("red = ${red}")
        for (Red(r) in [Red(10), Red(20), Red(30)]) {
            println("r = ${r}")
        }
    }
    ```

   上例中，变量定义时使用了 enum 模式，表示对 `Red(0)` 进行解构并将构造器的参数值（即 `0`）与 `red` 进行绑定。`for in` 表达式中使用了 enum 模式，表示依次将 `[Red(10), Red(20), Red(30)]` 中的元素取出，然后解构并将构造器的参数值与 `r` 进行绑定，循环体中输出 `r` 的值。编译执行上述代码，输出结果为：

    ```text
    red = 0
    r = 10
    r = 20
    r = 30
    ```
