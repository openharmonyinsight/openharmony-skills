# 函数类型

仓颉编程语言中，函数是一等公民（first-class citizens），可以作为函数的参数或返回值，也可以赋值给变量。因此函数本身也有类型，称之为函数类型。

函数类型由函数的参数类型和返回类型组成，参数类型和返回类型之间使用 `->` 连接。参数类型使用圆括号 `()` 括起来，可以有 0 个或多个参数，如果参数超过一个，参数类型之间使用逗号（`,`）分隔。

例如：

<!-- compile -->

```cangjie
func hello(): Unit {
    println("Hello!")
}
```

上述示例定义了一个函数，函数名为 hello，其类型是 `() -> Unit`，表示该函数没有参数，返回类型为 `Unit`。

以下给出另一些示例：

- 示例：函数名为 `display`，其类型是 `(Int64) -> Unit`，表示该函数有一个参数，参数类型为 `Int64`，返回类型为 `Unit`。

    <!-- compile -->

    ```cangjie
    func display(a: Int64): Unit {
        println(a)
    }
    ```

- 示例：函数名为 `add`，其类型是 `(Int64, Int64) -> Int64`，表示该函数有两个参数，两个参数类型均为 `Int64`，返回类型为 `Int64`。

    <!-- compile -->

    ```cangjie
    func add(a: Int64, b: Int64): Int64 {
        a + b
    }
    ```

- 示例：函数名为 `returnTuple`，其类型是 `(Int64, Int64) -> (Int64, Int64)`，两个参数类型均为 `Int64`, 返回类型为元组类型：`(Int64, Int64)`。

    <!-- compile -->

    ```cangjie
    func returnTuple(a: Int64, b: Int64): (Int64, Int64) {
        (a, b)
    }
    ```

## 函数类型的类型参数

可以为函数类型标记显式的类型参数名，下面例子中的 `name` 和 `price` 就是类型参数名。

<!-- run -->

```cangjie
func showFruitPrice(name: String, price: Int64) {
    println("fruit: ${name} price: ${price} yuan")
}

main() {
    let fruitPriceHandler: (name: String, price: Int64) -> Unit
    fruitPriceHandler = showFruitPrice
    fruitPriceHandler("banana", 10)
}
```

另外对于一个函数类型，只允许统一写类型参数名，或者统一不写类型参数名，不能交替存在。

<!-- compile.error -->

```cangjie
let handler: (name: String, Int64) -> Int64   // Error
```

## 函数类型作为参数类型

示例：函数名为 `printAdd`，其类型是 `((Int64, Int64) -> Int64, Int64, Int64) -> Unit`，表示该函数有三个参数，参数类型分别为函数类型 `(Int64, Int64) -> Int64` 和两个 `Int64`，返回类型为 `Unit`。

<!-- compile -->

```cangjie
func printAdd(add: (Int64, Int64) -> Int64, a: Int64, b: Int64): Unit {
    println(add(a, b))
}
```

## 函数类型作为返回类型

函数类型可以作为另一个函数的返回类型。

如下示例中，函数名为 `returnAdd`，其类型是 `() -> (Int64, Int64) -> Int64`，表示该函数无参数，返回类型为函数类型 `(Int64, Int64) -> Int64`。注意，`->` 是右结合的。

<!-- run -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    a + b
}

func returnAdd(): (Int64, Int64) -> Int64 {
    add
}

main() {
    var a = returnAdd()
    println(a(1,2))
}
```

## 函数类型作为变量类型

函数名本身也是表达式，它的类型为对应的函数类型。

<!-- compile -->

```cangjie
func add(p1: Int64, p2: Int64): Int64 {
    p1 + p2
}

let f: (Int64, Int64) -> Int64 = add
```

上述示例中，函数名是 `add`，其类型为 `(Int64, Int64) -> Int64`。变量 `f` 的类型与 `add` 类型相同，`add` 被用来初始化 `f`。

若一个函数在当前作用域中被重载（参见[函数重载](./function_overloading.md)），那么直接使用该函数名作为表达式可能产生歧义，如果产生歧义编译器会报错，例如：

<!-- compile.error -->

```cangjie
func add(i: Int64, j: Int64) {
    i + j
}

func add(i: Float64, j: Float64) {
    i + j
}

main() {
    var f = add   // Error, ambiguous function 'add'
    var plus: (Int64, Int64) -> Int64 = add  // OK
}
```
