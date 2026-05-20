# 泛型类

[泛型接口](./generic_interface.md)中介绍了泛型接口的定义和使用，本节介绍泛型类的定义和使用。如 `Map` 的键值对就是使用泛型类来定义的。

`Map` 类型中的键值对 `Node` 类型就可以使用泛型类来定义：

<!-- compile -->

```cangjie
open class Node<K, V> where K <: Hashable & Equatable<K> {
    var key: Option<K> = Option<K>.None
    var value: Option<V> = Option<V>.None

    init() {}

    init(key: K, value: V) {
        this.key = Option<K>.Some(key)
        this.value = Option<V>.Some(value)
    }
}
```

由于键与值的类型有可能不相同，且可以为任意满足条件的类型，所以 `Node` 需要两个类型形参 `K` 与 `V` ，`K <: Hashable, K <: Equatable<K>` 是对于键类型的约束，意为 `K` 要实现 `Hashable` 与 `Equatable<K>` 接口，也就是 `K` 需要满足的条件。对于泛型约束，详见[泛型约束](./generic_constraint.md)章节。

由于泛型类的静态成员变量的内存是共享的，因此，静态成员变量或属性的类型声明和表达式中不能引用类型参数或包含未实例化泛型类型表达式。另外，静态变量或属性初始化表达式中不能调用泛型类的静态成员函数或属性。

<!-- compile.error -->

```cangjie
class A<T> {}
class B<T> {
    static func foo() {1}
    static var err1: A<T> = A<T>() // Error, static member cannot depend on generic parameter 'Generics-T'
    static prop err2: A<T> { // Error, static member cannot depend on generic parameter 'Generics-T'
        get() {
            A<T>() // Error, static member cannot depend on generic parameter 'Generics-T'
        }
    }
    static var vfoo = foo() // Error, it's equal to 'static var vfoo = B<T>.foo()', implicit reference to generic 'T'.
    static var ok: Int64 = 1
}

main() {
    B<Int32>.ok = 2
    println(B<Int64>.ok) // 2
}
```
