# 调用函数

函数调用的形式为 `f(arg1, arg2, ..., argn)`。其中，`f` 是要调用的函数的名字，`arg1` 到 `argn` 是 `n` 个调用时的参数（称为实参），要求每个实参的类型必须是对应参数类型的子类型。实参可以有 0 个或多个，当实参个数为 0 时，调用方式为 `f()`。

根据函数定义时参数是非命名参数还是命名参数的差异，函数调用时传实参的方式也有所不同：对于非命名参数，它对应的实参是一个表达式；对于命名参数，它对应的实参需要使用 `p: e` 的形式，其中 `p` 是命名参数的名字，`e` 是表达式（即传递给参数 `p` 的值）。

非命名参数调用举例：

<!-- verify -->

```cangjie
func add(a: Int64, b: Int64) {
    return a + b
}

main() {
    let x = 1
    let y = 2
    let r = add(x, y)
    println("The sum of x and y is ${r}")
}
```

执行结果为：

```text
The sum of x and y is 3
```

命名参数调用举例：

<!-- verify -->

```cangjie
func add(a: Int64, b!: Int64) {
    return a + b
}

main() {
    let x = 1
    let y = 2
    let r = add(x, b: y)
    println("The sum of x and y is ${r}")
}
```

执行结果为：

```text
The sum of x and y is 3
```

对于多个命名参数，调用时的传参顺序可以和定义时的参数顺序不同。例如，下例中调用 `add` 函数时 `b` 可以出现在 `a` 之前：

<!-- verify -->

```cangjie
func add(a!: Int64, b!: Int64) {
    return a + b
}

main() {
    let x = 1
    let y = 2
    let r = add(b: y, a: x)
    println("The sum of x and y is ${r}")
}
```

执行结果为：

```text
The sum of x and y is 3
```

对于拥有默认值的命名参数，调用时如果没有传实参，那么此参数将使用默认值作为实参的值。例如，下例中调用 `add` 函数时没有为参数 `b` 传实参，那么参数 `b` 的值等于其定义时的默认值 `2`：

<!-- verify -->

```cangjie
func add(a: Int64, b!: Int64 = 2) {
    return a + b
}

main() {
    let x = 1
    let r = add(x)
    println("The sum of x and y is ${r}")
}
```

执行结果为：

```text
The sum of x and y is 3
```

对于拥有默认值的命名参数，调用时也可以为其传递新的实参，此时命名参数的值等于新的实参的值，即定义时的默认值将失效。例如，下例中调用 `add` 函数时为参数 `b` 传了新的实参值 `20`，那么参数 `b` 的值就等于 `20`：

<!-- verify -->

```cangjie
func add(a: Int64, b!: Int64 = 2) {
    return a + b
}

main() {
    let x = 1
    let r = add(x, b: 20)
    println("The sum of x and y is ${r}")
}
```

执行结果为：

```text
The sum of x and y is 21
```
