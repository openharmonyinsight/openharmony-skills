# 使用 Option

在 [Option 类型](../enum_and_pattern_match/option_type.md)中介绍了 Option 类型的定义，因为 Option 类型可以同时表示有值和无值两种状态，而无值在某些情况下也可以理解为一种错误，所以 Option 类型也可以用作错误处理。

例如，在下例中，如果函数 `getOrThrow` 的参数值等于 `Some(v)` 则将 `v` 的值返回，如果参数值等于 `None` 则抛出异常。

<!-- compile -->

```cangjie
func getOrThrow(a: ?Int64) {
    match (a) {
        case Some(v) => v
        case None => throw NoneValueException()
    }
}
```

因为 `Option` 是一种非常常用的类型，所以仓颉为其提供了多种解构方式，以方便 `Option` 类型的使用，具体包括：模式匹配、`getOrThrow` 函数、`coalescing` 操作符（`??`），以及问号操作符（`?`）。下面将对这些方式逐一介绍。

- 模式匹配：因为 Option 类型是一种 enum 类型，所以可以使用上文提到的 enum 的模式匹配来实现对 `Option` 值的解构。例如，下例中函数 `getString` 接受一个 `?Int64` 类型的参数，当参数是 `Some` 值时，返回其中数值的字符串表示，当参数是 `None` 值时，返回字符串 `"none"`。

    <!-- verify -->

    ```cangjie
    func getString(p: ?Int64): String{
        match (p) {
            case Some(x) => "${x}"
            case None => "none"
        }
    }
    main() {
        let a = Some(1)
        let b: ?Int64 = None
        let r1 = getString(a)
        let r2 = getString(b)
        println(r1)
        println(r2)
    }
    ```

   上述代码的执行结果为：

    ```text
    1
    none
    ```

- `coalescing` 操作符（`??`）：对于 `?T` 类型的表达式 `e1`，如果希望 `e1` 的值等于 `None` 时同样返回一个 `T` 类型的值 `e2`，可以使用 `??` 操作符。对于表达式 `e1 ?? e2`，当 `e1` 的值等于 `Some(v)` 时返回 `v` 的值，否则返回 `e2` 的值。举例如下：

    <!-- verify -->

    ```cangjie
    main() {
        let a = Some(1)
        let b: ?Int64 = None
        let r1: Int64 = a ?? 0
        let r2: Int64 = b ?? 0
        println(r1)
        println(r2)
    }
    ```

   上述代码的执行结果为：

    ```text
    1
    0
    ```

- 问号操作符（`?`）：`?` 需要和 `.` 或 `()` 或 `[]` 或 `{}`（特指尾随 lambda 调用的场景）一起使用，用以实现 `Option` 类型对 `.`，`()`，`[]` 和 `{}` 的支持。以 `.` 为例（`()`，`[]` 和 `{}`同理），对于 `?T1` 类型的表达式 `e`，当 `e` 的值等于 `Some(v)` 时，`e?.b` 的值等于 `Option<T2>.Some(v.b)`，否则 `e?.b` 的值等于 `Option<T2>.None`，其中 `T2` 是 `v.b` 的类型。举例如下：

    <!-- compile -->

    ```cangjie
    struct R {
        public var a: Int64
        public init(a: Int64) {
            this.a = a
        }
    }

    let r = R(100)
    let x = Some(r)
    let y = Option<R>.None
    let r1 = x?.a   // r1 = Option<Int64>.Some(100)
    let r2 = y?.a   // r2 = Option<Int64>.None

    class C {
        var item: Int64 = 100
    }
    let c = C()
    let c1 = Option<C>.Some(c)
    let c2 = Option<C>.None
    func test1() {
        c1?.item = 200             // c.item = 200
        c2?.item = 300             // no effect
    }
    ```

   问号操作符（`?`）支持多层访问，以 `a?.b.c?.d` 为例（`()`，`[]` 和 `{}`同理）。表达式 `a` 的类型需要是某个 `Option<T1>` 且 `T1` 包含实例成员 `b`，`b` 的类型中包含实例成员变量 `c` 且 `c` 的类型是某个 `Option<T2>`，`T2` 包含实例成员 `d`；表达式 `a?.b.c?.d` 的类型为 `Option<T3>`，其中 `T3` 是 `T2` 的实例成员 `d` 的类型；当 `a` 的值等于 `Some(va)` 且 `va.b.c` 的值等于 `Some(vc)` 时，`a?.b.c?.d` 的值等于 `Option<T3>.Some(vc.d)`；当 `a` 的值等于 `Some(va)` 且 `va.b.c` 的值等于 `None` 时，`a?.b.c?.d` 的值等于 `Option<T3>.None`（`d` 不会被求值）；当 `a` 的值等于 `None` 时，`a?.b.c?.d` 的值等于 `Option<T3>.None`（`b`，`c` 和 `d` 都不会被求值）。

    <!-- compile -->

    ```cangjie
    class A {
        public var b: B = B()
    }

    class B {
        public var c: Option<C> = C()
        public var c1: Option<C> = Option<C>.None
    }

    class C {
        public var d: Int64 = 100
    }

    main(){
        var a = Some(A())
        let a1 = a?.b.c?.d  // a1 = Option<Int64>.Some(100)
        let a2 = a?.b.c1?.d // a2 = Option<Int64>.None
        a?.b.c?.d = 200     // a.b.c.d = 200
        a?.b.c1?.d = 200    // no effect
    }
    ```

- `getOrThrow` 函数：对于 `?T` 类型的表达式 `e`，可以通过调用 `getOrThrow` 函数实现解构。当 `e` 的值等于 `Some(v)` 时，`getOrThrow()` 返回 `v` 的值，否则抛出异常。举例如下：

    <!-- verify -->

    ```cangjie
    main() {
        let a = Some(1)
        let b: ?Int64 = None
        let r1 = a.getOrThrow()
        println(r1)
        try {
            let r2 = b.getOrThrow()
        } catch (e: NoneValueException) {
            println("b is None")
        }
    }
    ```

   上述代码的执行结果为：

    ```text
    1
    b is None
    ```
