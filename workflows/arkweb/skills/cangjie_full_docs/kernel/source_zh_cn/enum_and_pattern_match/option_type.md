# Option 类型

`Option` 类型使用 `enum` 定义，它包含两个构造器：`Some` 和 `None`。其中，`Some` 会携带一个参数，表示有值；`None` 不带参数，表示无值。当需要表示某个类型可能有值，也可能没有值时，可以选择使用 `Option` 类型。

`Option` 类型被定义为一个泛型 `enum` 类型，定义如下（这里仅需要知道尖括号中的 `T` 是一个类型形参，当 `T` 为不同类型时会得到不同的 `Option` 类型即可。关于泛型的详细介绍，可参见[泛型](../generic/generic_overview.md)）：

<!-- compile -->

```cangjie
enum Option<T> {
    | Some(T)
    | None
}
```

其中，`Some` 构造器的参数类型就是类型形参 `T`，当 `T` 被实例化为不同的类型时，会得到不同的 `Option` 类型，例如：`Option<Int64>`、`Option<String>`等。

`Option` 类型还有一种简单的写法：在类型名前加 `?`。也就是说，对于任意类型 `Ty`，`?Ty` 等价于 `Option<Ty>`。例如，`?Int64` 等价于 `Option<Int64>`，`?String` 等价于 `Option<String>`。

下面的例子展示了如何定义 `Option` 类型的变量：

<!-- compile -->

```cangjie
let a: Option<Int64> = Some(100)
let b: ?Int64 = Some(100)
let c: Option<String> = Some("Hello")
let d: ?String = None
```

另外，虽然 `T` 和 `Option<T>` 是不同的类型，但是当明确知道某个位置需要的是 `Option<T>` 类型的值时，可以直接传一个 `T` 类型的值，编译器会用 `Option<T>` 类型的 `Some` 构造器将 `T` 类型的值封装成 `Option<T>` 类型的值（注意：这里并不是类型转换）。例如，下面的定义是合法的（等价于上例中变量 `a`，`b` 和 `c` 的定义）：

<!-- compile -->

```cangjie
let a: Option<Int64> = 100
let b: ?Int64 = 100
let c: Option<String> = "100"
```

在上下文没有明确的类型要求时，无法使用 `None` 直接构造出想要的类型，此时应使用 `None<T>` 这样的语法来构造 `Option<T>` 类型的数据，例如：

<!-- compile -->

```cangjie
let a = None<Int64> // a: Option<Int64>
let b = None<Bool> // b: Option<Bool>
```

最后，关于 `Option` 的使用，请参见[使用 Option](../error_handle/use_option.md)。
