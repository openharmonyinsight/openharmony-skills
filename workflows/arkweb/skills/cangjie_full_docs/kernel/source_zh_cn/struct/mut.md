# mut 函数

struct 类型是值类型，其实例成员函数无法修改实例本身。例如，下例中，成员函数 `g` 中不能修改成员变量 `i` 的值。

<!-- compile.error -->

```cangjie
struct Foo {
    var i = 0

    public func g() {
        i += 1  // Error, the value of a instance member variable cannot be modified in an instance member function
    }
}
```

mut 函数是一种可以修改 `struct` 实例本身的特殊的实例成员函数。在 `mut` 函数内部，`this` 的语义是特殊的，这种 `this` 拥有原地修改字段的能力。

> **注意：**
>
> 只允许在 interface、struct 和 struct 的扩展内定义 `mut` 函数（class 是引用类型，实例成员函数不需要加 `mut` 也可以修改实例成员变量，所以禁止在 class 中定义 `mut` 函数）。

## mut 函数定义

mut 函数与普通的实例成员函数相比，多一个 `mut` 关键字来修饰。

例如，下例中在函数 `g` 之前增加 `mut` 修饰符之后，即可在函数体内修改成员变量 `i` 的值。

<!-- compile -->

```cangjie
struct Foo {
    var i = 0

    public mut func g() {
        i += 1  // OK
    }
}
```

`mut` 只能修饰实例成员函数，不能修饰静态成员函数。

<!-- compile.error -->

```cangjie
struct A {
    public mut func f(): Unit {} // OK
    public mut operator func +(rhs: A): A { // OK
        A()
    }
    public mut static func g(): Unit {} // Error, static member functions cannot be modified with 'mut'
}
```

mut 函数中的 `this` 不能被捕获，也不能作为表达式。`mut` 函数中的 lambda 或嵌套函数不能对 struct 的实例成员变量进行捕获。

示例：

<!-- compile.error -->

```cangjie
struct Foo {
    var i = 0

    public mut func f(): Foo {
        let f1 = { => this } // Error, 'this' in mut functions cannot be captured
        let f2 = { => this.i = 2 } // Error, instance member variables in mut functions cannot be captured
        let f3 = { => this.i } // Error, instance member variables in mut functions cannot be captured
        let f4 = { => i } // Error, instance member variables in mut functions cannot be captured
        this // Error, 'this' in mut functions cannot be used as expressions
    }
}
```

## 接口中的 mut 函数

接口中的实例成员函数，也可以使用 `mut` 修饰。

`struct` 类型在实现 `interface` 的函数时必须保持一样的 `mut` 修饰。`struct` 以外的类型实现 `interface` 的函数时不能使用 `mut` 修饰。

示例：

<!-- compile.error -->

```cangjie
interface I {
    mut func f1(): Unit
    func f2(): Unit
}

struct A <: I {
    public mut func f1(): Unit {} // OK: as in the interface, the 'mut' modifier is used
    public func f2(): Unit {} // OK: as in the interface, the 'mut' modifier is not used
}

struct B <: I {
    public func f1(): Unit {} // Error, 'f1' is modified with 'mut' in interface, but not in struct
    public mut func f2(): Unit {} // Error, 'f2' is not modified with 'mut' in interface, but did in struct
}

class C <: I {
    public func f1(): Unit {} // OK
    public func f2(): Unit {} // OK
}
```

当 `struct` 的实例赋值给 `interface` 类型时是拷贝语义，因此 `interface` 的 `mut` 函数并不能修改 `struct` 实例的值。

示例：

<!-- verify -->

```cangjie
interface I {
    mut func f(): Unit
}
struct Foo <: I {
    public var v = 0
    public mut func f(): Unit {
        v += 1
    }
}
main() {
    var a = Foo()
    var b: I = a  
    b.f()  // Calling 'f' via 'b' cannot modify the value of 'a'
    println(a.v) // 0
}
```

程序输出结果为：

```text
0
```

## mut 函数的使用限制

因为 `struct` 是值类型，所以如果一个变量是 `struct` 类型且使用 `let` 声明，那么不能通过这个变量访问该类型的 `mut` 函数。

示例：

<!-- compile.error -->

```cangjie
interface I {
    mut func f(): Unit
}
struct Foo <: I {
    public var i = 0
    public mut func f(): Unit {
        i += 1
    }
}
main() {
    let a = Foo()
    a.f() // Error, 'a' is of type struct and is declared with 'let', the 'mut' function cannot be accessed via 'a'
    var b = Foo()
    b.f() // OK
    let c: I = Foo()
    c.f() // OK, 变量 c 为接口 I 类型，非 struct 类型，此处允许访问。
}
```

为避免逃逸，如果一个变量的类型是 `struct` 类型，那么这个变量不能将该类型使用 `mut` 修饰的函数作为一等公民来使用，只能调用这些 `mut` 函数。

示例：

<!-- compile.error -->

```cangjie
interface I {
    mut func f(): Unit
}

struct Foo <: I {
    var i = 0

    public mut func f(): Unit {
        i += 1
    }
}

main() {
    var a = Foo()
    var fn = a.f // Error, mut function 'f' of 'a' cannot be used as a first class citizen.
    var b: I = Foo()
    fn = b.f // OK
}
```

为避免逃逸，非 `mut` 的实例成员函数（包括 `lambda` 表达式）不能直接访问所在类型的 `mut` 函数，反之可以。

示例：

<!-- compile.error -->

```cangjie
struct Foo {
    var i = 0

    public mut func f(): Unit {
        i += 1
        g() // OK
    }

    public func g(): Unit {
        f() // Error, mut functions cannot be invoked in non-mut functions
    }
}

interface I {
    mut func f(): Unit {
        g() // OK
    }

    func g(): Unit {
        f() // Error, mut functions cannot be invoked in non-mut functions
    }
}
```
