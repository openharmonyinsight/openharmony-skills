# 顶层声明的可见性

仓颉编程语言中，可以使用访问修饰符来控制对类型、变量、函数等顶层声明的可见性。仓颉语言有 4 种访问修饰符：`private`、`internal`、`protected`、`public`，在修饰顶层元素时不同访问修饰符的语义如下：

- `private` 表示仅当前文件内可见。不同的文件无法访问这类成员。
- `internal` 表示仅当前包及子包（包括子包的子包）内可见。同一个包内可以不导入就访问这类成员，当前包的子包（包括子包的子包）内可以通过导入来访问这类成员。
- `protected` 表示仅当前模块内可见。同一个包的文件可以不导入就访问这类成员，不同包但是在同一个模块内的其他包可以通过导入访问这些成员，不同模块的包无法访问这些成员。
- `public` 表示模块内外均可见。同一个包的文件可以不导入就访问这类成员，其他包可以通过导入访问这些成员。

| 修饰符         | 文件 | 包及子包 | 模块 | 所有包 |
|-------------|------|----------|------|--------|
| `private`   | Y    | N        | N    | N      |
| `internal`  | Y    | Y        | N    | N      |
| `protected` | Y    | Y        | Y    | N      |
| `public`    | Y    | Y        | Y    | Y      |

不同顶层声明支持的访问修饰符和默认修饰符（默认修饰符是指在省略情况下的修饰符语义，这些默认修饰符也允许显式写出）规定如下：

- `package` 支持使用 `internal`、`protected`、`public`，默认修饰符为 `public`。
- `import` 支持使用全部访问修饰符，默认修饰符为 `private`。
- 其他顶层声明支持使用全部访问修饰符，默认修饰符为 `internal`。

<!-- compile -->

```cangjie
package a

private func f1() { 1 }   // f1 仅在当前文件内可见
func f2() { 2 }           // f2 仅当前包及子包内可见
protected func f3() { 3 } // f3 仅当前模块内可见
public func f4() { 4 }    // f4 当前模块内外均可见
```

仓颉的访问级别排序为 `public > protected > internal > private`。一个声明的访问修饰符不得高于该声明中用到的类型的访问修饰符的级别，参考如下示例：

- 函数声明中的参数与返回值

    <!-- compile.error -->

    ```cangjie
    // a.cj
    package a
    class C {}
    public func f1(a1: C) // Error, public declaration f1 cannot use internal type C.
    {
        return 0
    }
    public func f2(a1: Int8): C // Error, public declaration f2 cannot use internal type C.
    {
        return C()
    }
    public func f3 (a1: Int8) // Error, public declaration f3 cannot use internal type C.
    {
        return C()
    }
    ```

- 变量声明

    <!-- compile.error -->

    ```cangjie
    // a.cj
    package a
    class C {}
    public let v1: C = C() // Error, public declaration v1 cannot use internal type C.
    public let v2 = C() // Error, public declaration v2 cannot use internal type C.
    ```

- 泛型类型的类型实参

    <!-- compile.error -->

    ```cangjie
    // a.cj
    package a
    public class C1<T> {}
    class C2 {}
    public let v1 = C1<C2>() // Error, public declaration v1 cannot use internal type C2.
    ```

- `where` 约束中的类型上界

    <!-- compile.error -->

    ```cangjie
    // a.cj
    package a
    interface I {}
    public class B<T> where T <: I {}  // Error, public declaration B cannot use internal type I.
    ```

值得注意的是：

- `public` 修饰的声明在其初始化表达式或者函数体里面可以使用本包可见的任意类型，包括被 `public` 修饰的类型和不被 `public` 修饰的类型。

    <!-- compile -->

    ```cangjie
    // a.cj
    package a
    class C1 {}
    func f1(a1: C1)
    {
      return 0
    }
    public func f2(a1: Int8) // OK.
    {
      var v1 = C1()
      return 0
    }
    public let v1 = f1(C1()) // OK.
    public class C2 // OK.
    {
      var v2 = C1()
    }
    ```

- `public` 修饰的顶层声明能使用匿名函数，或者任意顶层函数，包括被 `public` 修饰的类型和不被 `public` 修饰的顶层函数。

    <!-- compile -toplevel-->

    ```cangjie
    public var t1: () -> Unit = { => } // OK.
    func f1(): Unit {}
    public let t2 = f1 // OK.

    public func f2() // OK.
    {
      return f1
    }
    ```

- 内置类型诸如 `Rune` 和 `Int64` 等默认的修饰符是 `public`。

    <!-- compile -toplevel-->

    ```cangjie
    var num = 5
    public var t3 = num // OK.
    ```

> **注意：**
>
> 同一个包内，`private` 修饰的同名自定义类型（如 `struct`、`class`、`enum` 和 `interface` 等），在某些场景下不支持，不支持场景由编译器进行报错。

例如在以下程序中，`example1.cj` 与 `example2.cj`文件包名相同，在 `example1.cj` 文件中定义了 `private` 修饰的类 `A`, 在 `example2.cj` 文件中定义了 `private` 修饰的结构体 `A`。

<!-- compile -->

```cangjie
// example1.cj
package test

private class A {}

public class D<T> {
    private let a: A = A()
}
```

<!-- compile -->

```cangjie
// example2.cj
package test

private struct A {}

public class C<T> {
    private let a: A = A()
}
```

运行以上程序，将输出：

```text
error: currently, it is not possible to export two private declarations with the same name
```
