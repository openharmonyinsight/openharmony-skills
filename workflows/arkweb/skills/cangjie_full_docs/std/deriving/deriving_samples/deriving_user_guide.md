# Deriving 示例

一个简单示例：

<!-- verify -->

```cangjie
import std.deriving.*

@Derive[ToString]
class User {
    User(
        let name: String,
        let id: Int
    ) {}
}

main() {
    println(User("id0", 0))
}
```

运行结果：

```text
User(name: id0, id: 0)
```

当 `@Derive[ToString]` 应用于类或结构体时， Deriving 会收集和使用类或结构体的可变和不可变字段，包括在主构造函数中指定的字段，并自动实现 `ToString` 的方法。当 `@Derive[ToString]` 应用于枚举时， Deriving 将收集枚举的构造函数参数。静态字段和属性将不会被收集和使用，另外， Deriving 收集的字段不允许存在私有字段，否则将抛出编译错误。

收集到的字段用于 Deriving 时，其类型需要实现目标接口，以便将字段结果组合在一起。例如，当处理 `ToString` 时，生成的代码将在所有收集到的字段上调用 `toString` ，然后将结果与对应的字段名称连接成一个字符串。如果其中一个字段的类型不支持 `ToString` ，则会抛出编译错误并且 Deriving 无法完成。

> **注意**
>
> 标记为派生的类应该是最终的：它不应该是开放的、抽象的或 `sealed` 的。

有些字段可能具有特殊含义，它们的值没有多大意义，则可通过在这些字段上应用 `@DeriveExclude` 来排除这些字段：

<!-- compile -->
```cangjie
import std.deriving.*

@Derive[ToString]
class User {
    User(let name: String) {}

    @DeriveExclude
    let lazyHashCode = 0 // it will not be printed because it's excluded
}
main(){}
```

默认情况 Deriving 仅使能字段，对于属性则需要通过 `@DeriveInclude` 来显式使能：

<!-- verify -->
```cangjie
import std.deriving.*

@Derive[ToString]
class User {
    User(let id: Int) {}

    @DeriveInclude
    prop name: String {
        get() {
            "id0"
        }
    }
}

main() {
    println(User(0))
}
```

运行结果：

```text
User(id: 0, name: id0)
```

请注意，因为属性 `name` 是在 `id` 之后声明的，因此打印的顺序为先 `id` 后 `name` 。

如果需要更改打印的顺序，可以使用 `@DeriveOrder` ：

<!-- verify -->
```cangjie
import std.deriving.*

@Derive[ToString]
@DeriveOrder[name, id]
class User {
    User(let id: Int) {}

    @DeriveInclude
    prop name: String {
        get() {
            "id${id}"
        }
    }
}

main() {
    println(User(0))
}
```

运行结果：

```text
User(name: id0, id: 0)
```

## 常见的 Deriving 语法

`@Derive` 宏支持以逗号分隔的接口名称列表。此外，该宏可以重复多次被调用，但所有 `@Derive` 宏调用都应位于声明的顶部，而其他宏（如 `@DeriveOrder` ）应始终位于其后。

支持的接口列表的顺序没有影响。

<!-- compile -->
```cangjie
import std.deriving.*

@Derive[ToString, Hashable]
@Derive[Equatable]
@DeriveOrder[currency, price, quantity]
struct Order {
    let currency = 1
    let price = 100
    let quantity = 200
}
main(){}
```

当 Deriving 多个相交的接口时，例如，`Comparable` 还包括 `Equatable` ，则允许两者同时存在，等同于仅有范围最广的一个：

```cangjie
@Derive[Comparable] // does also generate Equatable
```

等同于：

```cangjie
@Derive[Comparable, Equatable]
```

## 包含和排除

默认情况下会处理所有字段，包括定义为主构造函数参数的字段。
当需要排除某个字段时，可以对其应用 `@DeriveExclude` ：

<!-- compile -->
```cangjie
import std.deriving.*

@Derive[ToString]
struct S {
    S(let id: Int) {
        key = "s_${id}"
    }

    @DeriveExclude
    let key: String
}
main(){}
```

默认情况下不处理属性，需要通过 `@DeriveInclude` 包含属性。

<!-- compile -->
```cangjie
import std.deriving.*

@Derive[ToString]
struct S {
    S(let id: Int) {}

    @DeriveInclude
    prop key: String {
        get() {
            "s_${id}"
        }
    }
}
main(){}
```

被 Deriving 的字段和属性都不能是 `private` 的。因此，`private` 的字段或者属性应被除外或者使其为包内可见属性。

> **注意**
>
> 静态的字段和属性始终会被忽略，因此它们都不能被 `@DeriveInclude` 和 `@DeriveExclude` 修饰。

## 支持的接口

当前仅支持如下接口:

- `ToString`
- `Hashable`
- `Equatable`
- `Comparable`

暂不支持用户自定义的接口。

## 变更顺序

在对由多个字段组成的复杂类型的实例进行排序和比较时，测试字段的顺序通常很重要。默认情况下，所有字段都按声明顺序考虑。可以使用 `@DeriveOrder` 宏修改顺序。

<!-- verify -->

```cangjie
import std.deriving.*
import std.sort.*

@Derive[Comparable, ToString]
struct Floor {
    Floor(
        let level: Int,
        let building: Int
    ) {}
}

main() {
    let floors = [
        Floor(1, 2),
        Floor(3, 2),
        Floor(2, 1)
    ]
    sort(floors)
    for (f in floors) {
        println(f)
    }
}
```

上述示例将打印以下内容，看起来顺序没有很大影响。

```text
Floor(level: 1, building: 2)
Floor(level: 2, building: 1)
Floor(level: 3, building: 2)
```

但是当我实现 `Comparable` 时，不同的顺序将影响结果。

<!-- verify -->
```cangjie
import std.deriving.*
import std.sort.*

@Derive[Comparable, ToString]
@DeriveOrder[building, level] // 相比上面示例多了这一行代码
struct Floor {
    Floor(
        let level: Int,
        let building: Int
    ) {}
}
main() {
    let floors = [
        Floor(1, 2),
        Floor(3, 2),
        Floor(2, 1)
    ]
    sort(floors)
    for (f in floors) {
        println(f)
    }
}
```

此时，结果将首先按 `building` 排序，然后按 `level` 排序：

```text
Floor(building: 1, level: 2)
Floor(building: 2, level: 1)
Floor(building: 2, level: 3)
```

## 泛型

实现泛型类型的接口通常需要应用约束，以便类型仅在某些条件下实现接口。例如：

<!-- compile -->
```cangjie
class Cell<T> {
    Cell(let value: T) {}
}
main(){}
```

此时可能希望仅当单元格的值可打印时才能够打印该单元格。为了实现它，编写一个带有约束的扩展：

<!-- compile -->
```cangjie
class Cell<T> {
    Cell(let value: T) {}
}

extend<T> Cell<T> <: ToString where T <: ToString {
    public func toString(): String {
        "Cell(value = ${value})"
    }
}
main(){}
```

当使用 Deriving 时，它会默认尝试对所有泛型参数应用约束，因此以下内容与上面的扩展相同：

<!-- compile -->
```cangjie
import std.deriving.*

@Derive[ToString]
class Cell<T> {
    Cell(let value: T) {}
}
main(){}
```

然而在某些情况下，默认行为并不符合期望。此时，可使用 `@Derive` 内部的 `where` 来覆盖默认约束：

<!-- compile -->
```cangjie
import std.deriving.*

interface PrintableCellValue <: ToString { /*...*/ }

@Derive[ToString where T <: PrintableCellValue]
class Cell<T> {}
main(){}
```

请注意，在上面的示例中，自定义约束仅适用于 `ToString` ，因此如果需要对所有接口进行约束，则应单独为每个接口重复此动作。

<!-- compile -->
```cangjie
import std.deriving.*

interface PrintableCellValue <: ToString { /*...*/ }

@Derive[ToString where T <: PrintableCellValue]
@Derive[Hashable where T <: PrintableCellValue & Hashable]
class Cell<T> {}
main(){}
```

## 性能说明

由于 Deriving 是基于仓颉宏的，不涉及任何反射，因此 Deriving 实现的运行时性能与手写相当。但是，Deriving 涉及编译时的代码转换，因此它会影响编译时间。
