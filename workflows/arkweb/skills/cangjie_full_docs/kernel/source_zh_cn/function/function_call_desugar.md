# 函数调用语法糖

## 尾随 lambda

尾随 lambda 可以使函数的调用看起来像是语言内置的语法一样，增加语言的可扩展性。

当函数最后一个形参是函数类型，并且函数调用对应的实参是 lambda 时，可以使用尾随 lambda 语法，将 lambda 放在函数调用的尾部，圆括号外面。

例如，下例中定义了一个 `myIf` 函数，它的第一个参数是 `Bool` 类型，第二个参数是函数类型。当第一个参数的值为 `true` 时，返回第二个参数调用后的值，否则返回 `0`。调用 `myIf` 时可以像普通函数一样调用，也可以使用尾随 lambda 的方式调用。

<!-- compile -->

```cangjie
func myIf(a: Bool, fn: () -> Int64) {
    if(a) {
        fn()
    } else {
        0
    }
}

func test() {
    myIf(true, { => 100 }) // General function call

    myIf(true) {        // Trailing closure call
        100
    }
}
```

当函数调用有且只有一个 lambda 实参时，还可以省略 `()`，只写 lambda。

示例：

<!-- compile -->

```cangjie
func f(fn: (Int64) -> Int64) { fn(1) }

func test() {
    f { i => i * i }
}
```

## Flow 表达式

流操作符包括两种：表示数据流向的中缀操作符 `|>` （称为 `pipeline`）和表示函数组合的中缀操作符 `~>` （称为 `composition`）。

### Pipeline 表达式

当需要对输入数据做一系列的处理时，可以使用 `pipeline` 表达式来简化描述。`pipeline` 表达式的语法形式如下：`e1 |> e2`。等价于如下形式的语法糖：`let v = e1; e2(v)` 。

其中 `e2` 是函数类型的表达式，`e1` 的类型是 `e2` 的参数类型的子类型。

示例：

<!-- compile -->

```cangjie
func inc(x: Array<Int64>): Array<Int64> { // Increasing the value of each element in the array by '1'
    let s = x.size
    var i = 0
    for (e in x where i < s) {
        x[i] = e + 1
        i++
    }
    x
}

func sum(y: Array<Int64>): Int64 { // Get the sum of elements in the array
    var s = 0
    for (j in y) {
        s += j
    }
    s
}

let arr: Array<Int64> = [1, 3, 5]
let res = arr |> inc |> sum // res = 12
```

### Composition 表达式

`composition` 表达式表示两个单参函数的组合。`composition` 表达式语法为 `f ~> g`，等价于 `{ x => g(f(x)) }`。

其中 `f` 和 `g` 均为只有一个参数的函数类型的表达式。

`f` 和 `g` 组合，则要求 `f(x)` 的返回类型是 `g(...)` 的参数类型的子类型。

示例 1：

<!-- compile -->

```cangjie
func f(x: Int64): Float64 {
    Float64(x)
}
func g(x: Float64): Float64 {
    x
}

var fg = f ~> g // The same as { x: Int64 => g(f(x)) }
```

示例 2：

<!-- compile -->

```cangjie
func f(x: Int64): Float64 {
    Float64(x)
}

let lambdaComp = {x: Int64 => x} ~> f // The same as { x: Int64 => f({x: Int64 => x}(x)) }
```

示例 3：

<!-- compile -->

```cangjie
func h1<T>(x: T): T { x }
func h2<T>(x: T): T { x }
var hh = h1<Int64> ~> h2<Int64> // The same as { x: Int64 => h2<Int64>(h1<Int64>(x)) }
```

> **注意：**
>
> 表达式 f ~> g 中，会先对 f 求值，然后对 g 求值，最后才会进行函数的组合。

另外，流操作符不能与无默认值的命名形参函数直接一同使用，这是因为无默认值的命名形参函数必须给出命名实参才可以调用。例如：

<!-- compile.error -->

```cangjie
func f(a!: Int64): Unit {}

var a = 1 |> f  // Error
```

如果需要使用，开发者可以通过 lambda 表达式传入 `f` 函数的命名实参：

<!-- compile -->

```cangjie
func f(a!: Int64): Unit {}

var x = 1 |>  { x: Int64 => f(a: x) } // OK
```

由于相同的原因，当 `f` 的参数有默认值时，直接与流运算符一起使用也是错误的，例如：

<!-- compile.error -->

```cangjie
func f(a!: Int64 = 2): Unit {}

var a = 1 |> f // Error
```

但是当命名形参都存在默认值时，不需要给出命名实参也可以调用该函数，函数仅需要传入非命名形参，那么这种函数是可以同流运算符一起使用的，例如：

<!-- compile -->

```cangjie
func f(a: Int64, b!: Int64 = 2): Unit {}

var a = 1 |> f  // OK
```

当然，如果想要在调用 `f` 时，为参数 `b` 传入其他参数，那么也需要借助 lambda 表达式：

<!-- compile -->

```cangjie
func f(a: Int64, b!: Int64 = 2): Unit {}

var a = 1 |> {x: Int64 => f(x,  b: 3)}  // OK
```

## 变长参数

变长参数是一种特殊的函数调用语法糖。当形参最后一个非命名参数是 `Array` 类型时，实参中对应位置可以直接传入参数序列代替 `Array` 字面量（参数个数可以是 0 个或多个）。示例如下：

<!-- verify -->

```cangjie
func sum(arr: Array<Int64>) {
    var total = 0
    for (x in arr) {
        total += x
    }
    return total
}

main() {
    println(sum())
    println(sum(1, 2, 3))
}
```

程序输出：

```text
0
6
```

需要注意，只有最后一个非命名参数可以作为变长参数，命名参数不能使用这个语法糖。

<!-- compile.error -->

```cangjie
func length(arr!: Array<Int64>) {
    return arr.size
}

main() {
    println(length())        // Error, expected 1 argument, found 0
    println(length(1, 2, 3)) // Error, expected 1 argument, found 3
}
```

变长参数可以出现在全局函数、静态成员函数、实例成员函数、局部函数、构造函数、函数变量、lambda、函数调用操作符重载、索引操作符重载的调用处。不支持其他操作符重载、composition、pipeline 这几种调用方式。示例如下：

<!-- verify -->

```cangjie
class Counter {
    var total = 0
    init(data: Array<Int64>) { total = data.size }
    operator func ()(data: Array<Int64>) { total += data.size }
}

main() {
    let counter = Counter(1, 2)
    println(counter.total)
    counter(3, 4, 5)
    println(counter.total)
}
```

程序输出：

```text
2
5
```

函数重载决议总是会优先考虑不使用变长参数就能匹配的函数，只有在所有函数都不能匹配，才尝试使用变长参数解析。示例如下：

<!-- verify -->

```cangjie
func f<T>(x: T) where T <: ToString {
    println("item: ${x}")
}

func f(arr: Array<Int64>) {
    println("array: ${arr}")
}

main() {
    f()
    f(1)
    f(1, 2)
}
```

程序输出：

```text
array: []
item: 1
array: [1, 2]
```

当编译器无法决议时会报错：

<!-- compile.error -->

```cangjie
func f(arr: Array<Int64>) { arr.size }
func f(first: Int64, arr: Array<Int64>) { first + arr.size }

main() {
    println(f(1, 2, 3)) // Error
}
```
