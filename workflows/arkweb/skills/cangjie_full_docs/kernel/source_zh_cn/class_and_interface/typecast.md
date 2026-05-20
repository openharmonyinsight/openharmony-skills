# 类型转换

仓颉不支持不同类型之间的隐式转换（子类型天然是父类型，所以子类型到父类型的转换不是隐式类型转换），类型转换必须显式地进行。下面将依次介绍数值类型之间的转换，`Rune` 到 `UInt32` 和整数类型到 `Rune` 的转换，以及 `is` 和 `as` 操作符。

## 数值类型之间的转换

对于数值类型（包括：`Int8`，`Int16`，`Int32`，`Int64`，`IntNative`，`UInt8`，`UInt16`，`UInt32`，`UInt64`，`UIntNative`，`Float16`，`Float32`，`Float64`），仓颉支持使用 `T(e)` 的方式得到一个值等于 `e`，类型为 `T` 的值。其中，表达式 `e` 的类型和 `T` 可以是上述任意数值类型。

下面的例子展示了数值类型之间的类型转换：

<!-- verify -->

```cangjie
main() {
    let a: Int8 = 10
    let b: Int16 = 20
    let r1 = Int16(a)
    println("The type of r1 is 'Int16', and r1 = ${r1}")
    let r2 = Int8(b)
    println("The type of r2 is 'Int8', and r2 = ${r2}")

    let c: Float32 = 1.0
    let d: Float64 = 1.123456789
    let r3 = Float64(c)
    println("The type of r3 is 'Float64', and r3 = ${r3}")
    let r4 = Float32(d)
    println("The type of r4 is 'Float32', and r4 = ${r4}")

    let e: Int64 = 1024
    let f: Float64 = 1024.1024
    let r5 = Float64(e)
    println("The type of r5 is 'Float64', and r5 = ${r5}")
    let r6 = Int64(f)
    println("The type of r6 is 'Int64', and r6 = ${r6}")
}
```

上述代码的执行结果为：

```text
The type of r1 is 'Int16', and r1 = 10
The type of r2 is 'Int8', and r2 = 20
The type of r3 is 'Float64', and r3 = 1.000000
The type of r4 is 'Float32', and r4 = 1.123457
The type of r5 is 'Float64', and r5 = 1024.000000
The type of r6 is 'Int64', and r6 = 1024
```

> **注意：**
>
> 类型转换时可能发生溢出，若溢出可提前在编译器检测出来，则编译器会直接给出报错，否则根据默认的溢出策略将抛出异常。

## `Rune` 到 `UInt32` 和整数类型到 `Rune` 的转换

`Rune` 到 `UInt32` 的转换使用 `UInt32(e)` 的方式，其中 `e` 是一个 `Rune` 类型的表达式，`UInt32(e)` 的结果是 `e` 的 Unicode scalar value 对应的 `UInt32` 类型的整数值。

整数类型到 `Rune` 的转换使用 `Rune(num)` 的方式，其中 `num` 的类型可以是任意的整数类型，且仅当 `num` 的值落在 `[0x0000, 0xD7FF]` 或 `[0xE000, 0x10FFFF]` （即 Unicode scalar value）中时，返回对应的 Unicode scalar value 表示的字符，否则，编译报错（编译时可确定 `num` 的值）或运行时抛异常。

下面的例子展示了 `Rune` 和 `UInt32` 之间的类型转换：

<!-- verify -->

```cangjie
main() {
    let x: Rune = 'a'
    let y: UInt32 = 65
    let r1 = UInt32(x)
    let r2 = Rune(y)
    println("The type of r1 is 'UInt32', and r1 = ${r1}")
    println("The type of r2 is 'Rune', and r2 = ${r2}")
}
```

上述代码的执行结果为：

```text
The type of r1 is 'UInt32', and r1 = 97
The type of r2 is 'Rune', and r2 = A
```

## `is` 和 `as` 操作符

仓颉支持使用 `is` 操作符来判断某个表达式的类型是否是指定的类型（或其子类型）。具体而言，对于表达式 `e is T`（`e` 可以是任意表达式，`T` 可以是任何类型），当 `e` 的运行时类型是 `T` 的子类型时，`e is T` 的值为 `true`，否则 `e is T` 的值为 `false`。

下面的例子展示了 `is` 操作符的使用：

<!-- verify -->

```cangjie
open class Base {
    var name: String = "Alice"
}
class Derived <: Base {
    var age: UInt8 = 18
}

main() {
    let a = 1 is Int64
    println("Is the type of 1 'Int64'? ${a}")
    let b = 1 is String
    println("Is the type of 1 'String'? ${b}")

    let b1: Base = Base()
    let b2: Base = Derived()
    var x = b1 is Base
    println("Is the type of b1 'Base'? ${x}")
    x = b1 is Derived
    println("Is the type of b1 'Derived'? ${x}")
    x = b2 is Base
    println("Is the type of b2 'Base'? ${x}")
    x = b2 is Derived
    println("Is the type of b2 'Derived'? ${x}")
}
```

上述代码的执行结果为：

```text
Is the type of 1 'Int64'? true
Is the type of 1 'String'? false
Is the type of b1 'Base'? true
Is the type of b1 'Derived'? false
Is the type of b2 'Base'? true
Is the type of b2 'Derived'? true
```

`as` 操作符可以用于将某个表达式的类型转换为指定的类型。因为类型转换有可能会失败，所以 `as` 操作返回的是一个 `Option` 类型。具体而言，对于表达式 `e as T`（`e` 可以是任意表达式，`T` 可以是任何类型），当 `e` 的运行时类型是 `T` 的子类型时，`e as T` 的值为 `Option<T>.Some(e)`，否则 `e as T` 的值为 `Option<T>.None`。

下面的例子展示了 `as` 操作符的使用（注释中标明了 `as` 操作的结果）：

<!-- compile -->

```cangjie
open class Base {
    var name: String = "Alice"
}
class Derived <: Base {
    var age: UInt8 = 18
}

let a = 1 as Int64     // a = Option<Int64>.Some(1)
let b = 1 as String    // b = Option<String>.None

let b1: Base = Base()
let b2: Base = Derived()
let d: Derived = Derived()
let r1 = b1 as Base    // r1 = Option<Base>.Some(b1)
let r2 = b1 as Derived // r2 = Option<Derived>.None
let r3 = b2 as Base    // r3 = Option<Base>.Some(b2)
let r4 = b2 as Derived // r4 = Option<Derived>.Some(b2)
let r5 = d as Base     // r5 = Option<Base>.Some(d)
let r6 = d as Derived  // r6 = Option<Derived>.Some(d)
```
