# 枚举

## enum AnnotationKind

```cangjie
public enum AnnotationKind {
    | Type
    | Parameter
    | Init
    | MemberProperty
    | MemberFunction
    | MemberVariable
    | EnumConstructor
    | GlobalFunction
    | GlobalVariable
    | Extension
    | ...
}
```

功能：表示自定义注解希望支持的位置。

### EnumConstructor

```cangjie
EnumConstructor
```

功能：枚举构造器声明。

### Extension

```cangjie
Extension
```

功能：扩展声明。

### GlobalFunction

```cangjie
GlobalFunction
```

功能：全局函数声明。

### GlobalVariable

```cangjie
GlobalVariable
```

功能：全局变量声明。

### Init

```cangjie
Init
```

功能：构造函数声明。

### MemberFunction

```cangjie
MemberFunction
```

功能：成员函数声明。

### MemberProperty

```cangjie
MemberProperty
```

功能：成员属性声明。

### MemberVariable

```cangjie
MemberVariable
```

功能：成员变量声明。

### Parameter

```cangjie
Parameter
```

功能：成员函数/构造函数中的参数（不包括枚举构造器的参数）。

### Type

```cangjie
Type
```

功能：类型声明（class、struct、enum、interface）。

## enum Endian

```cangjie
public enum Endian {
    | Big
    | Little
}
```

功能：枚举类型 [Endian](core_package_enums.md#enum-endian) 表示运行平台的端序，分为大端序和小端序。

### Big

```cangjie
Big
```

功能：表示大端序。

### Little

```cangjie
Little
```

功能：表示小端序。

### static prop Platform

```cangjie
public static prop Platform: Endian
```

功能：获取所在运行平台的端序。

类型：[Endian](core_package_enums.md#enum-endian)

异常：

- [UnsupportedException](core_package_exceptions.md#class-unsupportedexception) - 当所运行平台返回的端序无法识别时，抛出异常。

示例：

<!-- verify -->
```cangjie
main() {
    let e = Endian.Platform
    match (e) {
        case Big => println("BigEndian")
        case Little => println("LittleEndian")
    }
}
```

运行结果：

```text
LittleEndian
```

## enum Option\<T>

```cangjie
public enum Option<T> {
    | Some(T)
    | None
}
```

功能：[Option](core_package_enums.md#enum-optiont)\<T> 是对 `T` 类型的封装，表示可能有值也可能无值。

它包含两个构造器：[Some](#somet) 和 [None](#none)。其中，[Some](#somet) 会携带一个参数，表示有值；[None](#none) 不带参数，表示无值。当需要表示某个类型可能有值，也可能没有值的时候，可选择使用 [Option](core_package_enums.md#enum-optiont) 类型。

[Option](core_package_enums.md#enum-optiont) 类型的另一种写法是在类型名前加 `?`，即对于任意类型 `Type`，`?Type` 等价于 [Option](core_package_enums.md#enum-optiont)\<Type>。

### None

```cangjie
None
```

功能：构造一个不带参数的 [Option](core_package_enums.md#enum-optiont)\<T> 实例，表示无值。

### Some(T)

```cangjie
Some(T)
```

功能：构造一个携带参数的 [Option](core_package_enums.md#enum-optiont)\<T> 实例，表示有值。

### func filter((T)->Bool)

```cangjie
public func filter(predicate: (T) -> Bool): Option<T>
```

功能：提供 [Option](core_package_enums.md#enum-optiont) 类型的“过滤”功能。

参数：

- predicate: (T) -> [Bool](core_package_intrinsics.md#bool) - 过滤函数。

返回值：

- Option\<T> - 如果 [Option](core_package_enums.md#enum-optiont) 值是 [Some](#somet)(v)，并且 v 满足 `predicate(v) = true` 时，返回 [Some](#somet)(v)， 否则返回 [None](#none)。

### func flatMap\<R>((T) -> Option\<R>)

```cangjie
public func flatMap<R>(transform: (T) -> Option<R>): Option<R>
```

功能：提供从 [Option](core_package_enums.md#enum-optiont)\<T> 类型到 [Option](core_package_enums.md#enum-optiont)\<R> 类型的映射函数，如果当前实例值是 [Some](#somet)，执行 transform 函数，并且返回结果，否则返回 [None](#none)。

参数：

- transform: (T) -> [Option](core_package_enums.md#enum-optiont)\<R> - 映射函数。

返回值：

- [Option](core_package_enums.md#enum-optiont)\<R> - 如果当前实例值是 [Some](#somet)，执行 transform 函数并返回，否则返回 [None](#none)。

### func getOrDefault(() -> T)

```cangjie
public func getOrDefault(other: () -> T): T
```

功能：获得值或返回默认值。如果 [Option](core_package_enums.md#enum-optiont) 值是 [Some](#somet)，则返回类型为 `T` 的实例，如果 [Option](core_package_enums.md#enum-optiont) 值是 [None](#none)，则调用入参，返回类型 `T` 的值。

参数：

- other: () -> T - 默认函数，如果当前实例的值是 [None](#none)，调用该函数得到类型为 `T` 的实例，并将其返回。

返回值：

- T - 如果当前实例的值是 [Some](#somet)\<T>，则返回当前实例携带的类型为 `T` 的实例，如果 [Option](core_package_enums.md#enum-optiont) 值是 [None](#none)，调用入参指定的函数，得到类型为 `T` 的实例，并将其返回。

示例：

<!-- verify -->
```cangjie
main() {
    var value1: Option<Int64> = Some(2)
    println(value1.getOrDefault({=> 0}))

    var value2: Option<Int64> = None
    println(value2.getOrDefault({=> 0}))
}
```

运行结果：

```text
2
0
```

### func getOrThrow(() -> Exception)

```cangjie
public func getOrThrow(exception: ()->Exception): T
```

功能：获得值或抛出指定异常。

参数：

- exception: () ->[Exception](core_package_exceptions.md#class-exception) - 异常函数，如果当前实例值是 [None](#none)，将执行该函数并将其返回值作为异常抛出。

返回值：

- T - 如果当前实例值是 [Some](#somet)\<T>，返回类型为 `T` 的实例。

异常：

- [Exception](core_package_exceptions.md#class-exception) - 如果当前实例是 [None](#none)，抛出异常函数返回的异常。

### func getOrThrow()

```cangjie
public func getOrThrow(): T
```

功能：获得值或抛出异常。

返回值：

- T - 如果当前实例值是 [Some](#somet)\<T>，返回类型为 `T` 的实例。

异常：

- [NoneValueException](core_package_exceptions.md#class-nonevalueexception) - 如果当前实例是 [None](#none)，抛出异常。

### func isNone()

```cangjie
public func isNone(): Bool
```

功能：判断当前实例值是否为 [None](#none)。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果当前实例值是 [None](#none)，则返回 true，否则返回 false。

### func isSome()

```cangjie
public func isSome(): Bool
```

功能：判断当前实例值是否为 [Some](#somet)。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果当前实例值是 [Some](#somet)，则返回 true，否则返回 false。

### func map\<R>((T)->R)

```cangjie
public func map<R>(transform: (T)-> R): Option<R>
```

功能：提供从 [Option](#enum-optiont)\<T> 类型到 [Option](#enum-optiont)\<R> 类型的映射函数，如果当前实例值是 [Some](#somet)，执行 transform 函数，并且返回 [Some](#somet) 封装的结果，否则返回 [None](#none)。

参数：

- transform: (T)-> R - 映射函数。

返回值：

- [Option](core_package_enums.md#enum-optiont)\<R> - 如果当前实例值是 [Some](#somet)，执行 transform 函数，并且返回 [Option](#enum-optiont)\<R> 类型的结果，否则返回 [None](#none)。

### extend\<T> Option\<Option\<T>>

```cangjie
extend<T> Option<Option<T>>
```

功能：为 Option\<Option\<T>> 类型扩展实现某些功能。

#### func flatten()

```cangjie
public func flatten(): Option<T>
```

功能：将 [Option](core_package_enums.md#enum-optiont)\<[Option](core_package_enums.md#enum-optiont)\<T>> 类型展开，如果当前实例是 [Some](#somet)([Option](core_package_enums.md#enum-optiont)\<T>.[Some](#somet)(v)), 展开后的结果为 [Some](#somet)(v)。

返回值：

- [Option](core_package_enums.md#enum-optiont)\<T> - [Option](core_package_enums.md#enum-optiont)\<[Option](core_package_enums.md#enum-optiont)\<T>> 类型展开后的结果。

### extend\<T> Option\<T> <: Equatable\<Option\<T>> where T <: Equatable\<T>

```cangjie
extend<T> Option<T> <: Equatable<Option<T>> where T <: Equatable<T>
```

功能：为 [Option](core_package_enums.md#enum-optiont)\<T> 枚举扩展 [Equatable](core_package_interfaces.md#interface-equatablet)\<[Option](core_package_enums.md#enum-optiont)\<T>> 接口，支持判等操作。

父类型：

- [Equatable](core_package_interfaces.md#interface-equatablet)\<[Option](#enum-optiont)\<T>>

#### operator func !=(Option\<T>)

```cangjie
public operator func !=(that: Option<T>): Bool
```

功能：判断当前实例与参数指向的 [Option](core_package_enums.md#enum-optiont)\<T> 实例是否不等。

参数：

- that: [Option](core_package_enums.md#enum-optiont)\<T> - 待比较的 [Option](core_package_enums.md#enum-optiont)\<T> 实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果不相等，则返回 true，否则返回 false。

#### operator func ==(Option\<T>)

```cangjie
public operator func ==(that: Option<T>): Bool
```

功能：判断当前实例与参数指向的 [Option](core_package_enums.md#enum-optiont)\<T> 实例是否相等。

如果两者同为 None，则相等；如果两者为 Some(v1) 和 Some(v2)，且 v1 和 v2 相等，则相等。

参数：

- that: [Option](core_package_enums.md#enum-optiont)\<T> - 待比较的 [Option](core_package_enums.md#enum-optiont)\<T> 实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果相等，则返回 true，否则返回 false。

### extend\<T> Option\<T> <: Hashable where T <: Hashable

```cangjie
extend<T> Option<T> <: Hashable where T <: Hashable
```

功能：为 [Option](core_package_enums.md#enum-optiont) 类型扩展 [Hashable](core_package_interfaces.md#interface-hashable) 接口。

[Some](#somet)\<T> 的哈希值等于 `T` 的值对应的哈希值，[None](#none) 的哈希值等于 [Int64](core_package_intrinsics.md#int64)(0)。

父类型：

- [Hashable](core_package_interfaces.md#interface-hashable)

#### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取哈希值。

返回值：

- [Int64](core_package_intrinsics.md#int64) - 哈希值。

### extend\<T> Option\<T> <: ToString where T <: ToString

```cangjie
extend<T> Option<T> <: ToString where T <: ToString
```

功能：为 [Option](core_package_enums.md#enum-optiont)\<T> 枚举实现 [ToString](core_package_interfaces.md#interface-tostring) 接口，支持转字符串操作。

父类型：

- [ToString](core_package_interfaces.md#interface-tostring)

#### func toString()

```cangjie
public func toString(): String
```

功能：将 [Option](core_package_enums.md#enum-optiont) 转换为可输出的字符串，字符串内容为 "Some(${T.toString()})" 或 "None"。

返回值：

- [String](core_package_structs.md#struct-string) - 转化后的字符串。

## enum Ordering

```cangjie
public enum Ordering {
    | LT
    | GT
    | EQ
}
```

功能：[Ordering](core_package_enums.md#enum-ordering) 表示比较大小的结果，它包含三种情况：小于，大于和等于。

### EQ

```cangjie
EQ
```

功能：构造一个 [Ordering](core_package_enums.md#enum-ordering) 实例，表示等于。

### GT

```cangjie
GT
```

功能：构造一个 [Ordering](core_package_enums.md#enum-ordering) 实例，表示大于。

### LT

```cangjie
LT
```

功能：构造一个 [Ordering](core_package_enums.md#enum-ordering) 实例，表示小于。

### extend Ordering <: Comparable

```cangjie
extend Ordering <: Comparable<Ordering>
```

功能：为 [Ordering](core_package_enums.md#enum-ordering) 类型其扩展 [Comparable](core_package_interfaces.md#interface-comparablet)\<[Ordering](core_package_enums.md#enum-ordering)> 接口，支持比较操作。

父类型：

- [Comparable](core_package_interfaces.md#interface-comparablet)\<[Ordering](#enum-ordering)>

#### func compare(Ordering)

```cangjie
public func compare(that: Ordering): Ordering
```

功能：判断当前 [Ordering](core_package_enums.md#enum-ordering) 实例与参数指定的 [Ordering](core_package_enums.md#enum-ordering) 实例的大小关系。

[Ordering](core_package_enums.md#enum-ordering) 枚举的大小关系为：GT > EQ > LT。

参数：

- that: [Ordering](core_package_enums.md#enum-ordering) - 待比较的 [Ordering](core_package_enums.md#enum-ordering) 实例。

返回值：

- [Ordering](core_package_enums.md#enum-ordering) - 如果大于，返回 GT；如果等于，返回 EQ；如果小于，返回 LT。

### extend Ordering <: Hashable

```cangjie
extend Ordering <: Hashable
```

功能：为 [Ordering](core_package_enums.md#enum-ordering) 类型其扩展 [Hashable](core_package_interfaces.md#interface-hashable) 接口，支持计算哈希值。

父类型：

- [Hashable](core_package_interfaces.md#interface-hashable)

#### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取哈希值，GT 的哈希值是 3，EQ 的哈希值是 2，LT 的哈希值是 1。

返回值：

- [Int64](core_package_intrinsics.md#int64) - 哈希值。

### extend Ordering <: ToString

```cangjie
extend Ordering <: ToString
```

功能：为 [Ordering](core_package_enums.md#enum-ordering) 类型其扩展 [ToString](core_package_interfaces.md#interface-tostring) 接口，支持转字符串操作。

父类型：

- [ToString](core_package_interfaces.md#interface-tostring)

#### func toString()

```cangjie
public func toString(): String
```

功能：将 [Ordering](core_package_enums.md#enum-ordering) 转换为可输出的字符串。

转换结果如下：

- GT: "[Ordering](core_package_enums.md#enum-ordering).GT"。
- LT: "[Ordering](core_package_enums.md#enum-ordering).ET"。
- EQ: "[Ordering](core_package_enums.md#enum-ordering).EQ"。

返回值：

- [String](core_package_structs.md#struct-string) - 转化后的字符串。
