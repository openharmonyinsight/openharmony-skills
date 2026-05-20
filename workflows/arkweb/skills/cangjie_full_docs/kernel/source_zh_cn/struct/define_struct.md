# 定义 struct 类型

`struct` 类型的定义以关键字 `struct` 开头，后跟 `struct` 的名字，接着是定义在一对花括号中的 `struct` 定义体。`struct` 定义体中可以定义一系列的成员变量、成员属性（参见[属性](../class_and_interface/prop.md)）、静态初始化器、构造函数和成员函数。

<!-- compile -->

```cangjie
struct Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func area() {
        width * height
    }
}
```

上例中定义了名为 `Rectangle` 的 `struct` 类型，它有两个 `Int64` 类型的成员变量 `width` 和 `height`，一个有两个 `Int64` 类型参数的构造函数（使用关键字 `init` 定义，函数体中通常是对成员变量的初始化），以及一个成员函数 `area`（返回 `width` 和 `height` 的乘积）。

> **注意：**
>
> `struct` 只能定义在源文件的顶层作用域。

## struct 成员变量

`struct` 成员变量分为实例成员变量和静态成员变量（使用 `static` 修饰符修饰），二者访问上的区别在于实例成员变量只能通过 `struct` 实例（说 `a` 是 `T` 类型的实例，指的是 `a` 是一个 `T` 类型的值）访问，静态成员变量只能通过 `struct` 类型名访问。

实例成员变量定义时可以不设置初值（但必须标注类型，如上例中的 `width` 和 `height`），也可以设置初值，例如：

<!-- compile -->

```cangjie
struct Rectangle {
    let width = 10
    let height = 20
}
```

## struct 静态初始化器

`struct` 支持定义静态初始化器，并在静态初始化器中通过赋值表达式来对静态成员变量进行初始化。

静态初始化器以关键字组合 `static init` 开头，后跟无参参数列表和函数体，且不能被访问修饰符修饰。函数体中必须完成对所有未初始化的静态成员变量的初始化，否则编译报错。

<!-- compile -->

```cangjie
struct Rectangle {
    static let degree: Int64
    static init() {
        degree = 180
    }
}
```

一个 `struct` 中最多允许定义一个静态初始化器，否则报重定义错误。

<!-- compile.error -->

```cangjie
struct Rectangle {
    static let degree: Int64
    static init() {
        degree = 180
    }
    static init() { // Error, redefinition with the previous static init function
        degree = 180
    }
}
```

## struct 构造函数

`struct` 支持两类构造函数：普通构造函数和主构造函数。

普通构造函数以关键字 `init` 开头，后跟参数列表和函数体，函数体中必须完成对所有未初始化的实例成员变量的初始化（如果参数名和成员变量名无法区分，可以在成员变量前使用 `this` 加以区分，`this` 表示 `struct` 的当前实例），否则编译报错。

<!-- compile.error -->

```cangjie
struct Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64, height: Int64) { // Error, 'height' is not initialized in the constructor
        this.width = width
    }
}
```

一个 `struct` 中可以定义多个普通构造函数，但它们必须构成重载（参见[函数重载](../function/function_overloading.md)），否则报重定义错误。

<!-- compile.error -->

```cangjie
struct Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64) {
        this.width = width
        this.height = width
    }

    public init(width: Int64, height: Int64) { // OK: overloading with the first init function
        this.width = width
        this.height = height
    }

    public init(height: Int64) { // Error, redefinition with the first init function
        this.width = height
        this.height = height
    }
}
```

除了可以定义若干普通的以 `init` 为名字的构造函数外，`struct` 内还可以定义（最多）一个主构造函数。主构造函数的名字和 `struct` 类型名相同，它的参数列表中可以有两种形式的形参：普通形参和成员变量形参（需要在参数名前加上 `let` 或 `var`），成员变量形参同时扮演定义成员变量和构造函数参数的功能。

使用主构造函数通常可以简化 `struct` 的定义，例如，上述包含一个 `init` 构造函数的 `Rectangle` 可以简化为如下定义：

<!-- compile -->

```cangjie
struct Rectangle {
    public Rectangle(let width: Int64, let height: Int64) {}
}
```

主构造函数的参数列表中也可以定义普通形参，例如：

<!-- compile -->

```cangjie
struct Rectangle {
    public Rectangle(name: String, let width: Int64, let height: Int64) {}
}
```

如果 `struct` 定义中不存在自定义构造函数（包括主构造函数），并且所有实例成员变量都有初始值，则会自动为其生成一个无参构造函数（调用此无参构造函数会创建一个所有实例成员变量的值均等于其初值的对象）；否则，不会自动生成此无参构造函数。例如，对于如下 `struct` 定义，注释中给出了自动生成的无参构造函数：

<!-- compile -->

```cangjie
struct Rectangle {
    let width: Int64 = 10
    let height: Int64 = 10
    /* Auto-generated memberwise constructor:
    public init() {
    }
    */
}
```

## struct 成员函数

`struct` 成员函数分为实例成员函数和静态成员函数（使用 `static` 修饰符修饰），二者的区别在于：实例成员函数只能通过 `struct` 实例访问，静态成员函数只能通过 `struct` 类型名访问；静态成员函数中不能访问实例成员变量，也不能调用实例成员函数，但在实例成员函数中可以访问静态成员变量以及静态成员函数。

下例中，`area` 是实例成员函数，`typeName` 是静态成员函数。

<!-- compile -->

```cangjie
struct Rectangle {
    let width: Int64 = 10
    let height: Int64 = 20

    public func area() {
        this.width * this.height
    }

    public static func typeName(): String {
        "Rectangle"
    }
}
```

实例成员函数中可以通过 `this` 访问实例成员变量，例如：

<!-- compile -->

```cangjie
struct Rectangle {
    let width: Int64 = 1
    let height: Int64 = 1

    public func area() {
        this.width * this.height
    }
}
```

## struct 成员的访问修饰符

`struct` 的成员包括成员变量、成员属性、构造函数、成员函数、操作符函数（详见[操作符重载](../function/operator_overloading.md)），这些成员可使用四种访问修饰符：`private`、`internal`、`protected` 和 `public`，缺省的修饰符是 `internal`。

- `private` 表示在 `struct` 定义内可见。
- `internal` 表示仅当前包及子包（包括子包的子包，详见[包](../package/toplevel_access.md)章节）内可见。
- `protected` 表示当前模块（详见[包](../package/toplevel_access.md)章节）可见。
- `public` 表示模块内外均可见。

下面的例子中，`width` 是 `public` 修饰的成员，在类外可以访问，`height` 是缺省访问修饰符的成员，仅在当前包及子包可见，其他包无法访问。

<!-- compile.error -->

```cangjie
package a
public struct Rectangle {
    public var width: Int64
    var height: Int64
    private var area: Int64

    public init(width: Int64, height: Int64, area: Int64) {
        this.width = width
        this.height = height
        this.area = area
    }
}

func samePkgFunc() {
    var r = Rectangle(10, 20, 40)
    r.width = 8               // OK: public 'width' can be accessed here
    r.height = 24             // OK: 'height' has no modifier and can be accessed here
    r.area = 30               // Error, private 'area' can't be accessed here
}
```

<!-- compile.error -->
<!-- cfg="-p b --output-type=staticlib" -->
<!-- cfg="liba.a" -->

```cangjie
package b
import a.*

main() {
    r.width = 8     // OK: public 'width' can be accessed here
    r.height = 24   // Error, no modifier 'height' can't be accessed here
    r.area = 30     // Error, private 'area' can't be accessed here
}
```

## 禁止递归 struct

递归和互递归定义的 `struct` 均是非法的。例如：

<!-- compile.error -->

```cangjie
struct R1 { // Error, 'R1' recursively references itself
    let other: R1
}
struct R2 { // Error, 'R2' and 'R3' are mutually recursive
    let other: R3
}
struct R3 { // Error, 'R2' and 'R3' are mutually recursive
    let other: R2
}
```
