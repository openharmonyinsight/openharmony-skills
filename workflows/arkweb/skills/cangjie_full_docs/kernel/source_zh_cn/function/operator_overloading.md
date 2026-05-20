# 操作符重载

如果希望在某个类型上支持此类型默认不支持的操作符，可以使用操作符重载实现。

如果需要在某个类型上重载某个操作符，可以通过为类型定义一个函数名为此操作符的函数的方式实现，这样，在该类型的实例使用该操作符时，就会自动调用此操作符函数。

操作符函数定义与普通函数定义相似，区别如下：

- 定义操作符函数时需要在 `func` 关键字前面添加 `operator` 修饰符；
- 操作符函数的参数个数需要匹配对应操作符的要求（详见附录[操作符](../Appendix/operator.md)）；
- 操作符函数只能定义在 class、interface、struct、enum 和 extend 中；
- 操作符函数具有实例成员函数的语义，所以禁止使用 `static` 修饰符；
- 操作符函数不能为泛型函数。

另外，需要注意的是，被重载后的操作符不改变它们固有的优先级和结合性（详见附录[操作符](../Appendix/operator.md)）。

## 操作符重载函数定义和使用

定义操作符函数有两种方式：

1. 对于可以直接包含函数定义的类型 (包括 `struct`、`enum`、`class` 和 `interface` )，可以直接在其内部定义操作符函数的方式实现操作符的重载。
2. 使用 `extend` 的方式为其添加操作符函数，从而实现操作符在这些类型上的重载。对于无法直接包含函数定义的类型（是指除 `struct`、`class`、`enum` 和 `interface` 之外其他的类型）或无法改变其实现的类型，比如第三方定义的 `struct`、`class`、`enum` 和 `interface`，只能采用这种方式（参见[扩展](../extension/extend_overview.md)）。

操作符函数对参数类型的约定如下：

1. 对于一元操作符，操作符函数没有参数，对返回值的类型没有要求。

2. 对于二元操作符，操作符函数只有一个参数，对返回值的类型没有要求。

   如下示例中介绍了一元操作符和二元操作符的定义和使用：

   `-` 实现对一个 `Point` 实例中两个成员变量 `x` 和 `y` 取负值，然后返回一个新的 `Point` 对象，`+` 实现对两个 `Point` 实例中两个成员变量 `x` 和 `y` 分别求和，然后返回一个新的 `Point` 对象。

    <!-- run -overloadOperater -->

    ```cangjie
    open class Point {
        var x: Int64 = 0
        var y: Int64 = 0
        public init (a: Int64, b: Int64) {
            x = a
            y = b
        }

        public operator func -(): Point {
            Point(-x, -y)
        }
        public operator func +(right: Point): Point {
            Point(this.x + right.x, this.y + right.y)
        }
    }
    ```

   接下来，就可以在 `Point` 的实例上直接使用一元 `-` 操作符和二元 `+` 操作符：

    <!-- run -overloadOperater -->

    ```cangjie
    main() {
        let p1 = Point(8, 24)
        let p2 = -p1      // p2 = Point(-8, -24)
        let p3 = p1 + p2  // p3 = Point(0, 0)
    }
    ```

3. 索引操作符（`[]`）分为取值 `let a = arr[i]` 和赋值 `arr[i] = a` 两种形式，它们通过是否存在特殊的命名参数 value 来区分不同的重载。索引操作符重载不要求同时重载两种形式，可以只重载赋值不重载取值，反之亦可。

   索引操作符取值形式 `[]` 内的参数序列对应操作符重载的非命名参数，可以是 1 个或多个，可以是任意类型。不可以有其他命名参数。返回类型可以是任意类型。

    <!-- compile -->

    ```cangjie
    class A {
        operator func [](arg1: Int64, arg2: String): Int64 {
            return 0
        }
    }

    func f() {
        let a = A()
        let b: Int64 = a[1, "2"]
        // b == 0
    }
    ```

   索引操作符赋值形式 `[]` 内的参数序列对应操作符重载的非命名参数，可以是 1 个或多个，可以是任意类型。`=` 右侧的表达式对应操作符重载的命名参数，有且只能有一个命名参数，该命名参数的名称必须是 value, 不能有默认值，value 可以是任意类型。返回类型必须是 Unit 类型。

   需要注意的是，value 只是一种特殊的标记，在索引操作符赋值时并不需要使用命名参数的形式调用。

    <!-- compile -->

    ```cangjie
    class A {
        operator func [](arg1: Int64, arg2: String, value!: Int64): Unit {
            return
        }
    }

    func f() {
        let a = A()
        a[1, "2"] = 0
    }
    ```

   特别的，除 `enum` 外的不可变类型不支持重载索引操作符赋值形式。

4. 函数调用操作符（`()`）重载函数，输入参数和返回值类型可以是任意类型。示例如下：

    <!-- compile -->

    ```cangjie
    open class A {
        public init() {}

        public operator func ()(): Unit {}
    }

    func test1() {
        let a = A() // OK, A() is call the constructor of A
        a()         // OK, a() is to call the operator () overloading function
    }
    ```

   不能使用 `this` 或 `super` 调用 `()` 操作符重载函数。示例如下：

    <!-- compile.error -->

    ```cangjie
    open class A {
        public init() {}
        public init(x: Int64) {
            this() // OK, this() calls the constructor of A
        }

        public operator func ()(): Unit {}

        public func foo() {
            this()  // Error, this() calls the constructor of A.
            super() // Error
        }
    }

    class B <: A {
        public init() {
            super() // OK, super()  calls the constuctor of the super class
        }

        public func goo() {
            super() // Error
        }
    }
    ```

   对于枚举类型，当构造器形式和 `()` 操作符重载函数形式都满足时，优先匹配构造器形式。示例如下：

    <!-- compile -->

    ```cangjie
    enum E {
        Y | X | X(Int64)

        public operator func ()(p: Int64) {}
        public operator func ()(p: Float64) {}
    }

    main() {
        let e = X(1)    // OK, X(1) is to call the constructor X(Int64)
        X(1.0)          // OK, X(1.0) is to call the operator () overloading function
        let e1 = X
        e1(1)           // OK, e1(1) is to call the operator () overloading function
        Y(1)            // OK, Y(1) is to call the operator () overloading function
    }
    ```

## 可以被重载的操作符

下表列出了所有可以被重载的操作符（优先级从高到低）：

| Operator            | Description           |
|:--------------------|:----------------------|
| `()`                | Function call         |
| `[]`                | Indexing              |
| `!`                 | NOT                   |
| `-`                 | Negative              |
| `**`                | Power                 |
| `*`                 | Multiply              |
| `/`                 | Divide                |
| `%`                 | Remainder             |
| `+`                 | Add                   |
| `-`                 | Subtract              |
| `<<`                | Bitwise left shift    |
| `>>`                | Bitwise right shift   |
| `<`                 | Less than             |
| `<=`                | Less than or equal    |
| `>`                 | Greater than          |
| `>=`                | Greater than or equal |
| `==`                | Equal                 |
| `!=`                | Not equal             |
| `&`                 | Bitwise AND           |
| `^`                 | Bitwise XOR           |
| <code>&vert;</code> | Bitwise OR            |

**注意事项：**

- 一旦在某个类型上重载了除关系操作符（`<`、`<=`、`>`、`>=`、`==` 和 `!=`）之外的其他二元操作符，并且操作符函数的返回类型与左操作数的类型一致或是其子类型，那么此类型支持对应的复合赋值操作符。当操作符函数的返回类型与左操作数的类型不一致且不是其子类型时，在使用对应的复合赋值符号时将报类型不匹配错误。

<!-- compile.error -->

```cangjie
open class MyClass {
    var x: Int64 = 0
    public init (a: Int64) {
        x = a
    }

    public operator func +(right: MyClass): Int64 { // The above rules are not met
        this.x + right.x
    }
}

main() {
    var a = MyClass(5)
    var b = MyClass(3)
    a += b; // Error, type incompatible in this compound assignment expression
}
```

- 仓颉编程语言不支持自定义操作符，即不允许定义除上表中所列 `operator` 之外的其他操作符函数。
- 对于类型 `T`，如果 `T` 已默认支持上述某些可重载操作符，那么通过扩展方式再次为其实现相同签名的操作符函数将报重定义错误。例如：为数值类型重载其已支持的同签名算术操作符、位操作符或关系操作符，为 `Rune` 重载同签名的关系操作符，或为 `Bool` 类型重载同签名的逻辑操作符、判等或不等操作符，均会报重定义错误。

<!-- compile.error -->

```cangjie
extend Int64 {
    public operator func +(x: Int64, y: Int64): Int64 { // Error, invalid number of parameters for operator '+'
        x + y
    }
}
```
