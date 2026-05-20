# 接口扩展

例如下面的例子，类型 `Array` 本身没有实现接口 `PrintSizeable`，但可以通过扩展的方式为 `Array` 增加额外的成员函数 `printSize`，并实现 `PrintSizeable`。

<!-- verify -PrintSizeable -->

```cangjie
interface PrintSizeable {
    func printSize(): Unit
}

extend<T> Array<T> <: PrintSizeable {
    public func printSize() {
        println("The size is ${this.size}")
    }
}
```

当使用扩展为 `Array` 实现 `PrintSizeable` 之后，就相当于在 `Array` 定义时实现接口 `PrintSizeable`。

因此可以将 `Array` 作为 `PrintSizeable` 的实现类型来使用，代码如下所示。

<!-- verify -PrintSizeable -->

```cangjie
main() {
    let a: PrintSizeable = Array<Int64>()
    a.printSize() // 0
}
```

编译执行上述代码，输出结果为：

<!-- verify -PrintSizeable -->

```text
The size is 0
```

可以在同一个扩展内同时实现多个接口，多个接口之间使用 `&` 分开，接口的顺序没有先后关系。

如下面代码所示，可以在扩展中为 `Foo` 同时实现 `I1`、`I2`、`I3`。

<!-- compile -->

```cangjie
interface I1 {
    func f1(): Unit
}

interface I2 {
    func f2(): Unit
}

interface I3 {
    func f3(): Unit
}

class Foo {}

extend Foo <: I1 & I2 & I3 {
    public func f1(): Unit {}
    public func f2(): Unit {}
    public func f3(): Unit {}
}
```

也可以在接口扩展中声明额外的泛型约束，来实现一些特定约束下才能满足的接口。

例如可以让上面的 `Pair` 类型实现 `Eq` 接口，这样 `Pair` 自己也能成为一个符合 `Eq` 约束的类型，如下代码所示。

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

extend<T1, T2> Pair<T1, T2> <: Eq<Pair<T1, T2>> where T1 <: Eq<T1>, T2 <: Eq<T2> {
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

如果被扩展的类型已经包含接口要求的函数或属性，那么在扩展中不需要并且也不能重新实现这些函数或属性。

例如下面的例子，定义了一个新接口 `Sizeable`，目的是获取某个类型的 `size`，而已经知道 `Array` 中包含了这个函数，因此就可以通过扩展让 `Array` 实现 `Sizeable`，而不需要添加额外的函数。

<!-- verify -->

```cangjie
interface Sizeable {
    prop size: Int64
}

extend<T> Array<T> <: Sizeable {}

main() {
    let a: Sizeable = Array<Int64>()
    println(a.size)
}
```

编译执行上述代码，输出结果为：

```text
0
```

当多个接口扩展实现的接口存在继承关系时，扩展将按照“先检查实现父接口的扩展，再检查子接口的扩展”的顺序进行检查。

例如，接口 `I1` 存在一个子接口 `I2`，且 `I1` 中包含一个默认实现，类型 `A` 的两个扩展分别实现了父子接口，根据以上检查顺序，实现 `I1` 的扩展将会优先检查，然后再检查实现 `I2` 的扩展。

<!-- verify -->

```cangjie
interface I1 {
    func foo(): Unit { println("I1 foo") }
}
interface I2 <: I1 {
    func foo(): Unit { println("I2 foo") }
}

class A {}

extend A <: I1 {} // first check
extend A <: I2 {} // second check

main() {
    A().foo()
}
```

编译执行上述代码，输出结果为：

```text
I2 foo
```

以上例子中，当检查实现 `I1` 的扩展时，会从 `I1` 中继承 `foo` 函数。在检查实现 `I2` 的扩展时，由于 `A` 中已存在一个继承的，且签名相同的默认实现 `foo` ，此时 `foo` 将被覆盖。因此，调用 `A` 的 `foo` 函数时，最终指向 `I2`（子接口）中的实现。

如果同一类型的两个接口扩展实现的接口存在继承冲突，导致无法确定检查顺序时，将会报错。

<!-- compile.error -->

```cangjie
interface I1 {}
interface I2 <: I1 {}
interface I3 {}
interface I4 <: I3 {}

class A {}
extend A <: I1 & I4 {} // error: unable to decide which extension happens first
extend A <: I2 & I3 {} // error: unable to decide which extension happens first
```

如果同一类型的两个接口扩展实现的接口不存在继承关系，将会被同时检查。

<!-- compile.error -->

```cangjie
interface I1 {
    func foo() {}
}
interface I2 {
    func foo() {}
}

class A {}
extend A <: I1 {} // Error, multiple default implementations, need to re-implement 'foo' in 'A'
extend A <: I2 {} // Error, multiple default implementations, need to re-implement 'foo' in 'A'
```

> **注意：**
>
> 当类 A 有个泛型基类 `B<T1,...,Tn>`，`B<T1,...,Tn>` 扩展了一个接口 `I<R1,...,Rn>`，`I<R1,...,Rn>` 带有默认实现的实例或者静态函数（比如 foo），该函数没有在 `B<T1,...,Tn>` 及其扩展中被重写，且类 A 没有直接实现接口 `I<R1,...,Rn>` 时，通过类 A 的实例调用函数 foo 时会产生非预期行为。

<!-- compile -->

```cangjie
interface I<N> {
    func foo(n: N): N {n}
}

open class B<T> {}

extend<T> B<T> <: I<T> {}

class A <: B<Int64>{}

main() {
    A().foo(0) // this call triggers unexpected behaviour
}
```
