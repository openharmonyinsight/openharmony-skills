# 直接扩展

一个简单的扩展语法结构示例如下：

<!-- verify -printSize -->

```cangjie
extend String {
    public func printSize() {
        println("the size is ${this.size}")
    }
}
```

如上例所示，扩展使用 `extend` 关键字声明，其后跟着被扩展的类型 `String` 和扩展的功能。

当为 `String` 扩展了 `printSize` 函数之后，就能在当前 `package` 内对 `String` 的实例访问该函数，就像是 `String` 本身具备该函数。

<!-- verify -printSize -->

```cangjie
main() {
    let a = "123"
    a.printSize() // the size is 3
}
```

编译执行上述代码，输出结果为：

<!-- verify -printSize -->

```text
the size is 3
```

被扩展类型是泛型类型时，有两种扩展语法可以对泛型类型扩展功能。

一种是针对特定泛型实例化类型进行扩展，关键字 `extend` 后允许带一个任意实例化完全的泛型类型。为这些类型增加的功能只有在类型完全匹配时才能使用，且泛型类型的类型实参必须符合泛型类型定义处的约束要求。

例如下面所示的 `Foo<T>`：

<!-- compile.error -->

```cangjie
class Foo<T> where T <: ToString {}

extend Foo<Int64> {} // OK

class Bar {}
extend Foo<Bar> {} // Error, generics type arguments do not match the constraint of 'Class-Foo<Generics-T>'
```

另一种是在 `extend` 后面引入泛型形参的泛型扩展。泛型扩展可以用来扩展未实例化或未完全实例化的泛型类型。在 `extend` 后声明的泛型形参必须被直接或间接使用在被扩展的泛型类型上。为这些类型增加的功能只有在类型和约束完全匹配时才能使用。

例如下面所示的 `MyList<T>`：

<!-- compile.error -->

```cangjie
class MyList<T> {
    public let data: Array<T> = Array<T>()
}

extend<T> MyList<T> {}          // OK
extend<R> MyList<R> {}          // OK
extend<T, R> MyList<(T, R)> {}  // OK
extend MyList {}                // Error, generic type should be used with type argument
extend<T, R> MyList<T> {}       // Error, type parameter 'R' must be used in extended type
extend<T, R> MyList<T, R> {}    // Error, type argument's number does not match type parameter's number
```

对于泛型类型的扩展，可以在其中声明额外的泛型约束，来实现一些有限情况下才能使用的函数。

例如可以定义一个叫 Pair 的类型，这个类型可以方便地存储两个元素（类似于 Tuple）。希望 Pair 类型可以容纳任何类型，因此两个泛型变元不应该有任何约束，这样才能保证 Pair 能容纳所有类型。但同时又希望当两个元素可以判等的时候，让 Pair 也可以判等，这时就可以用扩展来实现这个功能。

如下面的代码所示，使用扩展语法，约束了 T1 和 T2 在支持 equals 的情况下，Pair 也可以实现 equals 函数。

<!-- verify -->

```cangjie
class Pair<T1, T2> {
    var first: T1
    var second: T2
    public init(a: T1, b: T2) {
        first = a
        second = b
    }
}

interface Eq<T> {
    func equals(other: T): Bool
}

extend<T1, T2> Pair<T1, T2> where T1 <: Eq<T1>, T2 <: Eq<T2> {
    public func equals(other: Pair<T1, T2>) {
        first.equals(other.first) && second.equals(other.second)
    }
}

class Foo <: Eq<Foo> {
    public func equals(other: Foo): Bool {
        true
    }
}

main() {
    let a = Pair(Foo(), Foo())
    let b = Pair(Foo(), Foo())
    println(a.equals(b)) // true
}
```

编译执行上述代码，输出结果为：

```text
true
```
