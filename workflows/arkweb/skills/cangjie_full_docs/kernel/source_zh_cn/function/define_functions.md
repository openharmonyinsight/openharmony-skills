# 定义函数

仓颉使用关键字 `func` 来表示函数定义的开始，`func` 之后依次是函数名、参数列表、可选的函数返回值类型、函数体。其中，函数名可以是任意的合法标识符，参数列表定义在一对圆括号内（多个参数间使用逗号分隔），参数列表和函数返回值类型（如果存在）之间使用冒号分隔，函数体定义在一对花括号内。

函数定义举例：

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    return a + b
}
```

上例中定义了一个名为 `add` 的函数，其参数列表由两个 `Int64` 类型的参数 `a` 和 `b` 组成，函数返回值类型为 `Int64`，函数体中将 `a` 和 `b` 相加并返回。

下面依次对函数定义中的参数列表、函数返回值类型和函数体作进一步介绍。

## 参数列表

一个函数可以拥有 0 个或多个参数，这些参数均定义在函数的参数列表中。根据函数调用时是否需要给定参数名，可以将参数列表中的参数分为两类：非命名参数和命名参数。

非命名参数的定义方式是 `p: T`，其中 `p` 表示参数名，`T` 表示参数 `p` 的类型，参数名和其类型间使用冒号连接。例如，上例中 `add` 函数的两个参数 `a` 和 `b` 均为非命名参数。

命名参数的定义方式是 `p!: T`，与非命名参数的不同是在参数名 `p` 之后多了一个 `!`。可以将上例中 `add` 函数的两个非命名参数修改为命名参数，如下所示：

<!-- compile -->

```cangjie
func add(a!: Int64, b!: Int64): Int64 {
    return a + b
}
```

命名参数还可以设置默认值，通过 `p!: T = e` 方式将参数 `p` 的默认值设置为表达式 `e` 的值。例如，可以将上述 `add` 函数的两个参数的默认值都设置为 `1`：

<!-- compile -->

```cangjie
func add(a!: Int64 = 1, b!: Int64 = 1): Int64 {
    return a + b
}
```

> **注意：**
>
> 只能为命名参数设置默认值，不能为非命名参数设置默认值。

参数列表中可以同时定义非命名参数和命名参数，但是需要注意的是，非命名参数只能定义在命名参数之前，也就意味着命名参数之后不能再出现非命名参数。例如，下例中 `add` 函数的参数列表定义是不合法的：

<!-- compile.error -->

```cangjie
func add(a!: Int64, b: Int64): Int64 { // Error, named parameter 'a' must be defined after non-named parameter 'b'
    return a + b
}
```

非命名参数和命名参数的主要差异在于调用时的不同，具体可参见下文[调用函数](./call_functions.md)中的介绍。

函数参数均为不可变变量，在函数定义内不能对其赋值。

<!-- compile.error -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    a = a + b // Error
    return a
}
```

函数参数作用域从定义处起至函数体结束：

<!-- compile.error -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    var a_ = a // OK
    var b = b  // Error, redefinition of declaration 'b'
    return a
}
```

## 函数返回值类型

函数返回值类型是函数被调用后得到的值的类型。函数定义时，返回值类型是可选的：可以显式地定义返回值类型（返回值类型定义在参数列表和函数体之间），也可以不定义返回值类型，交由编译器推导确定。

当显式地定义了函数返回值类型时，就要求函数体的类型（关于如何确定函数体的类型可参见下节[函数体](./define_functions.md#函数体)）、函数体中所有 `return e` 表达式中 `e` 的类型是返回值类型的子类型。例如，对于上述 `add` 函数，显式地定义了它的返回值类型为 `Int64`；如果将函数体中的 `return a + b` 修改为 `return (a, b)`，则会因为类型不匹配而报错：

<!-- compile.error -->

```cangjie
// Error, the type of the expression after return does not match the return type of the function
func add(a: Int64, b: Int64): Int64 {
    return (a, b)
}
```

在函数定义时如果未显式定义返回值类型，编译器将根据函数体的类型以及函数体中所有的 `return` 表达式来共同推导出函数的返回值类型。例如，下例中 `add` 函数的返回值类型虽然被省略，但编译器可以根据 `return a + b` 推导出 `add` 函数的返回值类型是 `Int64`：

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64) {
    return a + b
}
```

> **注意：**
>
> 函数的返回值类型并不是任何情况下都可以被推导出来的，如果返回值类型推导失败，编译器会报错。
>
> 指定返回类型为 Unit 时，编译器会在函数体中所有可能返回的地方自动插入表达式 return ()，使得函数的返回类型总是为 Unit。

## 函数体

函数体中定义了函数被调用时执行的操作，通常包含一系列的变量定义和表达式，也可以包含新的函数定义（即嵌套函数）。如下 `add` 函数的函数体中首先定义了 `Int64` 类型的变量 `r`（初始值为 `0`），接着将 `a + b` 的值赋值给 `r`，最后将 `r` 的值返回：

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64) {
    var r = 0
    r = a + b
    return r
}
```

在函数体的任意位置都可以使用 `return` 表达式来终止函数的执行并返回。`return` 表达式有两种形式：`return` 和 `return expr`（`expr` 是一个表达式）。

对于 `return expr`，要求 `expr` 的类型与函数定义中的返回值类型保持一致。例如，下例中会因为 `return 100` 中 `100` 类型（`Int64`）和函数 `foo` 的返回值类型（`String`）不同而报错。

<!-- compile.error -->

```cangjie
// Error, cannot convert an integer literal to type 'Struct-String'
func foo(): String {
    return 100
}
```

对于 `return`，其等价于 `return ()`，所以要求函数的返回值类型为 `Unit`。

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64) {
    var r = 0
    r = a + b
    return r
}

func foo(): Unit {
    add(1, 2)
    return
}
```

> **注意：**
>
> `return` 表达式作为一个整体，其类型并不由后面跟随的表达式决定，而是 `Nothing` 类型。

在函数体内定义的变量属于局部变量的一种（如上例中的 `r` 变量），它的作用域从其定义之后开始到函数体结束。

对于一个局部变量，允许在其外层作用域中定义同名变量，并且在此局部变量的作用域内，局部变量会“遮盖”外层作用域的同名变量。例如：

<!-- compile -->

```cangjie
let r = 0
func add(a: Int64, b: Int64) {
    var r = 0
    r = a + b
    return r
}
```

上例中，`add` 函数之前定义了 `Int64` 类型的全局变量 `r`，同时 `add` 函数体内定义了同名的局部变量 `r`，那么在函数体内，所有使用变量 `r` 的地方（如 `r = a + b`），用到的将是局部变量 `r`，即（在函数体内）局部变量 `r` “遮盖”了全局变量 `r`。

[函数返回值类型](./define_functions.md#函数返回值类型)中提到函数体也是有类型的，函数体的类型是函数体内最后一“项”的类型：若最后一项为表达式，则函数体的类型是此表达式的类型，若最后一项为变量定义或函数声明，或函数体为空，则函数体的类型为 `Unit`。例如：

<!-- compile -->

```cangjie
func add(a: Int64, b: Int64): Int64 {
    a + b
}
```

上例中，因为函数体的最后一“项”是 `Int64` 类型的表达式（即 `a + b`），所以函数体的类型也是 `Int64`，与函数定义的返回值类型相匹配。又如，下例中函数体的最后一项是 `print` 函数调用，所以函数体的类型是 `Unit`，同样与函数定义的返回值类型相匹配：

<!-- compile -->

```cangjie
func foo(): Unit {
    let s = "Hello"
    print(s)
}
```
