# 类

`class` 类型是面向对象编程中的经典概念，仓颉中同样支持使用 `class` 来实现面向对象编程。`class` 与 `struct` 的主要区别在于：`class` 是引用类型，`struct` 是值类型，它们在赋值或传参时行为是不同的；`class` 之间可以继承，但 `struct` 之间不能继承。

本节依次介绍如何定义 `class` 类型，如何创建对象，以及 `class` 的继承。

## class 定义

`class` 类型的定义以关键字 `class` 开头，后跟 `class` 的名字，接着是定义在一对花括号中的 `class` 定义体。`class` 定义体中可以定义一系列的成员变量、成员属性（参见[属性](prop.md)）、静态初始化器、构造函数、成员函数和操作符函数（详见[操作符重载](../function/operator_overloading.md)）。

<!-- compile -->

```cangjie
class Rectangle {
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

上例中定义了名为 `Rectangle` 的 `class` 类型，它有两个 `Int64` 类型的成员变量 `width` 和 `height`，一个有两个 `Int64` 类型参数的构造函数，以及一个成员函数 `area`（返回 `width` 和 `height` 的乘积）。

> **注意：**
>
> `class` 只能定义在源文件的顶层作用域。

使用 `abstract` 修饰的类为抽象类，与普通类不同的是，在抽象类中除了可以定义普通的函数，还允许声明抽象函数（没有函数体）。抽象类定义时的 `open` 修饰符是可选的，也可以使用 `sealed` 修饰符修饰抽象类。`sealed` 修饰符表示该抽象类只能在本包被继承，详见 [class 的继承小节](#class-的继承)。下例中在抽象类 `AbRectangle` 中定义了抽象函数 `foo`。

<!-- compile -->

```cangjie
abstract class AbRectangle {
    public func foo(): Unit
}
```

> **注意：**
>
> - 抽象类中禁止定义 `private` 的抽象函数；
> - 不能为抽象类创建实例；
> - 抽象类的非抽象子类必须实现父类中的所有抽象函数。

### class 成员变量

`class` 成员变量分为实例成员变量和静态成员变量，静态成员变量使用 `static` 修饰符修饰，没有静态初始化器时必须有初值，只能通过类型名访问，参考如下示例：

<!-- compile -->

```cangjie
class Rectangle {
    let width = 10
    static let height = 20
}

let l = Rectangle.height // l = 20
```

实例成员变量定义时可以不设置初值（但必须标注类型），也可以设置初值，只能通过对象（即类的实例）访问，参考如下示例：

<!-- compile -->

```cangjie
class Rectangle {
    let width = 10
    let height: Int64
    init(h: Int64) {
        height = h
    }
}
let rec = Rectangle(20)
let l = rec.height // l = 20
```

### class 静态初始化器

`class` 支持定义静态初始化器，并在静态初始化器中通过赋值表达式来对静态成员变量进行初始化。

静态初始化器以关键字组合 `static init` 开头，后跟无参参数列表和函数体，且不能被访问修饰符修饰。函数体中必须完成对所有未初始化的静态成员变量的初始化，否则编译报错。

<!-- compile -->

```cangjie
class Rectangle {
    static let degree: Int64
    static init() {
        degree = 180
    }
}
```

一个 `class` 中最多允许定义一个静态初始化器，否则报重定义错误。

<!-- compile.error -->

```cangjie
class Rectangle {
    static let degree: Int64
    static init() {
        degree = 180
    }
    static init() { // Error, redefinition with the previous static init function
        degree = 180
    }
}
```

### class 构造函数

和 `struct` 一样，`class` 中也支持定义普通构造函数和主构造函数。

普通构造函数以关键字 `init` 开头，后跟参数列表和函数体，函数体中必须完成所有未初始化实例成员变量的初始化，否则编译报错。

<!-- compile.error -->

```cangjie
class Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64, height: Int64) { // Error, 'height' is not initialized in the constructor
        this.width = width
    }
}
```

一个类中可以定义多个普通构造函数，但它们必须构成重载（参见[函数重载](../function/function_overloading.md)），否则报重定义错误。

<!-- compile.error -->

```cangjie
class Rectangle {
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

除了可以定义若干普通的以 `init` 为名字的构造函数外，`class` 内还可以定义（最多）一个主构造函数。主构造函数的名字和 `class` 类型名相同，它的参数列表中可以有两种形式的形参：普通形参和成员变量形参（需要在参数名前加上 `let` 或 `var`），成员变量形参同时具有定义成员变量和构造函数参数的功能。

使用主构造函数通常可以简化 `class` 的定义，例如，上述包含一个 `init` 构造函数的 `Rectangle` 可以简化为如下定义：

<!-- compile -->

```cangjie
class Rectangle {
    public Rectangle(let width: Int64, let height: Int64) {}
}
```

主构造函数的参数列表中也可以定义普通形参，例如：

<!-- compile -->

```cangjie
class Rectangle {
    public Rectangle(name: String, let width: Int64, let height: Int64) {}
}
```

创建类的实例时调用的构造函数，将根据以下顺序执行类中的表达式：

1. 先初始化主构造函数之外定义的有缺省值的变量；
2. 如果构造函数体内未显式调用父类构造函数或本类其他构造函数，则调用父类的无参构造函数 `super()`，如果父类没有无参构造函数，则报错；
3. 执行构造函数体内的代码。

<!-- verify -->

```cangjie
func foo(x: Int64): Int64 {
    println("I'm foo, got ${x}")
    x
}

open class A {
    init() {
        println("I'm A")
    }
}

class B <: A {
    var x = foo(0)
    init() {
        x = foo(1)
        println("init B finished")
    }
}

main() {
    B()
    0
}
```

上述例子中，调用 `B` 的构造函数时，首先初始化有缺省值的变量 `x`，此时 `foo(0)` 被调用；之后调用父类的无参构造函数，此时 `A` 的构造函数被调用；接下来执行构造函数体内的代码，此时 `foo(1)` 被调用，并打印字符串。因此上例的输出为：

```text
I'm foo, got 0
I'm A
I'm foo, got 1
init B finished
```

如果 `class` 定义中不存在自定义构造函数（包括主构造函数），并且所有实例成员变量都有初始值，则会自动为其生成一个无参构造函数（调用此无参构造函数会创建一个所有实例成员变量的值均等于其初值的对象）；否则，不会自动生成此无参构造函数。例如，对于如下 `class` 定义，编译器会为其自动生成一个无参构造函数：

<!-- compile -->

```cangjie
class Rectangle {
    let width = 10
    let height = 20

    /* Auto-generated parameterless constructor:
    public init() {

    }
    */
}

// Invoke the auto-generated parameterless constructor
let r = Rectangle() // r.width = 10，r.height = 20
```

### class 终结器

`class` 支持定义终结器，当类的实例被垃圾回收时，会触发该函数。终结器的函数名固定为 `~init`，通常用于释放系统资源。如下示例中的 `unsafe`，详见 [unsafe 小节](../FFI/cangjie-c.md)：

<!-- compile -->

```cangjie
class C {
    var p: CString

    init(s: String) {
        p = unsafe { LibC.mallocCString(s) }
        println(s)
    }
    ~init() {
        unsafe { LibC.free(p) }
    }
}
```

使用终结器有些限制条件，需要开发者注意：

1. 终结器没有参数，没有返回类型，没有泛型类型参数，没有任何修饰符，也不可以被显式调用。
2. 带有终结器的类不可被 `open` 修饰，只有非 `open` 的类可以拥有终结器。
3. 一个类最多只能定义一个终结器。
4. 终结器不可以定义在扩展中。
5. 终结器被触发的时机是不确定的。
6. 终结器可能在任意一个线程上执行。
7. 多个终结器的执行顺序是不确定的。
8. 终结器向外抛出未捕获异常属于未定义行为。
9. 终结器中创建线程或者使用线程同步功能属于未定义行为。
10. 终结器执行结束之后，如果这个对象还可以被继续访问，则属于未定义行为。
11. 如果对象在初始化过程中抛出异常，这样未完整初始化的对象的终结器不会执行。
12. 依赖终结器的同步行为属于未定义行为。例如，下例中 `main` 函数通过 `while (Test.t0 != 0)` 等待 `Test` 类中的终结器修改 `t0` 的值，属于未定义行为。

    <!-- run -->

    ```cangjie
    import std.collection.ArrayList
    import std.runtime.gc

    class Test {
        public static var t0 : Int32 = 0
        public init () {
            t0++
        }
        ~init () {
            t0--
        }
    }

    var list: ArrayList<Test> = ArrayList<Test>()

    func foo() : Int32 {
        let o1 = Test()
        list.add(o1)
        if (Test.t0 != 1) {
            return 1
        }
        list.remove(at: 0)
        return 0
    }

    main(): Int64 {
        var i : Int64 = 0
        while (i < 100) {
            if (foo() != 0) {
                print("fail: obj is freed before gc!")
                return 1
            }
            gc(heavy: true) // blocking gc expected
            // wait ~init() to be executed
            while (Test.t0 != 0) {  // error, this is undefined behavior
                continue
            }
            i++
        }
        return 0
    }
    ```

### class 成员函数

`class` 成员函数同样分为实例成员函数和静态成员函数（使用 `static` 修饰符修饰），实例成员函数只能通过对象访问，静态成员函数只能通过 `class` 类型名访问；静态成员函数中不能访问实例成员变量，也不能调用实例成员函数，但在实例成员函数中可以访问静态成员变量以及静态成员函数。

下例中，`area` 是实例成员函数，`typeName` 是静态成员函数。

<!-- compile -->

```cangjie
class Rectangle {
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

根据是否有函数体，实例成员函数又可以分为抽象成员函数和非抽象成员函数。抽象成员函数没有函数体，只能定义在抽象类或接口（详见[接口](interface.md)）中。需要注意的是，抽象实例成员函数默认具有 `open` 的语义，`open` 修饰符是可选的，且必须使用 `public` 或 `protected` 进行修饰。

非抽象函数必须有函数体，在函数体中可以通过 `this` 访问实例成员变量，例如：

<!-- compile -->

```cangjie
class Rectangle {
    let width: Int64 = 10
    let height: Int64 = 20

    public func area() {
        this.width * this.height
    }
}
```

### class 成员的访问修饰符

对于 `class` 的成员（包括成员变量、成员属性、构造函数、成员函数），可以使用的访问修饰符有 4 种访问修饰符修饰：`private`、`internal`、`protected` 和 `public`，缺省的含义是 `internal`。

- `private` 表示在 `class` 定义内可见。
- `internal` 表示仅当前包及子包（包括子包的子包，详见[包](../package/toplevel_access.md)）内可见。
- `protected` 表示当前模块（详见[包](../package/toplevel_access.md)）及当前类的子类可见。
- `public` 表示模块内外均可见。

<!-- compile.error -error-->

```cangjie
package a

public open class Rectangle {
    public var width: Int64
    protected var height: Int64
    private var area: Int64
    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
        this.area = this.width * this.height
    }
    init(width: Int64, height: Int64, multiple: Int64) {
        this.width = width
        this.height = height
        this.area = width * height * multiple
    }
}

func samePkgFunc() {
    var r = Rectangle(10, 20) // OK: constructor 'Rectangle' can be accessed here
    r.width = 8               // OK: public 'width' can be accessed here
    r.height = 24             // OK: protected 'height' can be accessed here
    r.area = 30               // Error, private 'area' cannot be accessed here
}
```

<!-- compile.error -error-->

```cangjie
package b
import a.*

public class Cuboid <: Rectangle {
    private var length: Int64
    public init(width: Int64, height: Int64, length: Int64) {
        super(width, height)
        this.length = length
    }
    public func volume() {
        this.width * this.height * this.length // OK: protected 'height' can be accessed here
    }
}

main() {
    var r = Rectangle(10, 20, 2) // Error, Rectangle has no `public` constructor with three parameters
    var c = Cuboid(20, 20, 20)
    c.width = 8               // OK: public 'width' can be accessed here
    c.height = 24             // Error, protected 'height' cannot be accessed here
    c.area = 30               // Error, private 'area' cannot be accessed here
}
```

## This 类型

在类内部，支持 `This` 类型占位符，代指当前类的类型。它只能被作为实例成员函数的返回类型来使用，当使用子类对象调用在父类中定义的返回 `This` 类型的函数时，该函数调用的类型会被识别为子类类型，而非定义所在的父类类型。

如果实例成员函数没有声明返回类型，并且只存在返回 `This` 类型表达式时，当前函数的返回类型会推断为 `This`。示例如下：

<!-- compile -->

```cangjie
open class C1 {
    func f(): This {  // its type is `() -> C1`
        return this
    }

    func f2() { // its type is `() -> C1`
        return this
    }

    public open func f3(): C1 {
        return this
    }
}
class C2 <: C1 {
    // member function f is inherited from C1, and its type is `() -> C2` now
    public override func f3(): This { // OK
        return this
    }
}

main() {
    var obj1: C2 = C2()
    var obj2: C1 = C2()

    var x = obj1.f()    // During compilation, the type of x is C2
    var y = obj2.f()    // During compilation, the type of y is C1
}
```

## 创建对象

定义了 `class` 类型后，即可通过调用其构造函数来创建对象（通过 `class` 类型名调用构造函数）。例如，下例中通过 `Rectangle(10, 20)` 创建 `Rectangle` 类型的对象并赋值给变量 `r`。创建对象之后，可以通过对象访问（`public` 修饰的）实例成员变量和实例成员函数。例如，下例中通过 `r.width` 和 `r.height` 可分别访问 `r` 中 `width` 和 `height` 的值，通过 `r.area()` 可以调用成员函数 `area`。

<!-- compile -->

```cangjie
class Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func area() {
        this.width * this.height
    }
}

main() {
    let r = Rectangle(10, 20) // r.width = 10, r.height = 20
    let width = r.width       // width = 10
    let height = r.height     // height = 20
    let a = r.area()          // a = 200
}
```

如果希望通过对象去修改成员变量的值（不鼓励这种方式，最好还是通过成员函数去修改），需要将 `class` 类型中的成员变量定义为可变成员变量（即使用 `var` 定义）。举例如下：

<!-- run -->

```cangjie
class Rectangle {
   public var width: Int64
   public var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }
    public func area() {
        width * height
    }
}

main() {
    let r = Rectangle(10, 20) // r.width = 10, r.height = 20
    r.width = 8               // r.width = 8
    r.height = 24             // r.height = 24
    let a = r.area()          // a = 192
}
```

不同于 `struct`，对象在赋值或传参时，不会将对象进行复制，多个变量指向的是同一个对象，通过一个变量去修改对象中成员的值，其他变量中对应的成员变量也会被修改。以赋值为例，下面的例子中，将 `r1` 赋值给 `r2` 之后，修改 `r1` 的 `width` 和 `height` 的值，`r2` 的 `width` 和 `height` 值也同样会被修改。

<!-- run -->

```cangjie
class Rectangle {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }
     public func area() {
        this.width * this.height
    }
}
main() {
    var r1 = Rectangle(10, 20) // r1.width = 10, r1.height = 20
    var r2 = r1                // r2.width = 10, r2.height = 20
    r1.width = 8               // r1.width = 8
    r1.height = 24             // r1.height = 24
    let a1 = r1.area()         // a1 = 192
    let a2 = r2.area()         // a2 = 192
}
```

## class 的继承

像大多数支持 `class` 的编程语言一样，仓颉中的 `class` 同样支持继承。如果类 B 继承类 A，则称 A 为父类，B 为子类。子类将继承父类中除 `private` 成员和构造函数以外的所有成员。

抽象类总是可被继承的，故抽象类定义时的 `open` 修饰符是可选的，也可以使用 `sealed` 修饰符修饰抽象类，表示该抽象类只能在本包被继承。但非抽象的类可被继承是有条件的：定义时必须使用修饰符 `open` 修饰。当带 `open` 修饰的实例成员被 class 继承时，该 `open` 的修饰符也会被继承。当非 `open` 修饰的类中存在 `open` 修饰的成员时，编译器会给出告警。

可以在子类定义处通过 `<:` 指定其继承的父类，但要求父类必须是可继承的。例如，下面的例子中，`class` A 使用 `open` 修饰，是可以被类 B 继承的，但是因为类 B 是不可继承的，所以 C 在继承 B 的时候会报错。

<!-- compile.error -->

```cangjie
open class A {
    let a: Int64 = 10
}

class B <: A { // OK: 'B' Inheritance 'A'
    let b: Int64 = 20
}

class C <: B { // Error, 'B' is not inheritable
    let c: Int64 = 30
}
```

`class` 仅支持单继承，因此下面这样一个类继承两个类的代码是不合法的（`&` 是类实现多个接口时的语法，详见[接口](interface.md)）。

<!-- compile.error -->

```cangjie
open class A {
    let a: Int64 = 10
}

open class B {
    let b: Int64 = 20
}

class C <: A & B { // Error, 'C' can only inherit one class
    let c: Int64 = 30
}
```

因为类是单继承的，所以任何类都最多只能有一个直接父类。对于定义时指定了父类的 `class`，它的直接父类就是定义时指定的类，对于定义时未指定父类的 `class`，它的直接父类是 `Object` 类型。`Object` 是所有类的父类（注意，`Object` 没有直接父类，并且 `Object` 中不包含任何成员）。

因为子类是继承自父类的，所以子类的对象天然可以当做父类的对象使用，但是反之不然。例如，下例中 B 是 A 的子类，那么 B 类型的对象可以赋值给 A 类型的变量，但是 A 类型的对象不能赋值给 B 类型的变量。

<!-- compile -->

```cangjie
open class A {
    let a: Int64 = 10
}

class B <: A {
    let b: Int64 = 20
}

let a: A = B() // OK: subclass objects can be assigned to superclass variables
```

<!-- compile.error -->

```cangjie
open class A {
    let a: Int64 = 10
}

class B <: A {
    let b: Int64 = 20
}

let b: B = A() // Error, superclass objects can not be assigned to subclass variables
```

`class` 定义的类型不允许继承类型本身。

<!-- compile.error -->

```cangjie
class A <: A {}  // Error, 'A' inherits itself
```

抽象类可以使用 `sealed` 修饰符，表示被修饰的类定义只能在本定义所在的包内被其他类继承。`sealed` 已经蕴含了 `public`/`open` 的语义，因此定义 sealed abstract class 时若提供 `public`/`open` 修饰符，编译器将会告警。`sealed` 的子类可以不是 `sealed` 类，仍可被 `open`/`sealed` 修饰，或不使用任何继承性修饰符。若 `sealed` 类的子类被 `open` 修饰，则其子类可在包外被继承。`sealed` 的子类可以不被 `public` 修饰。

<!-- compile -->

```cangjie
package A

public sealed abstract class C1 {}   // Warning, redundant modifier, 'sealed' implies 'public'
sealed open abstract class C2 {}     // Warning, redundant modifier, 'sealed' implies 'open'
sealed abstract class C3 {}          // OK, 'public' is optional when 'sealed' is used

class S1 <: C1 {}  // OK
public open class S2 <: C1 {}   // OK
public sealed abstract class S3 <: C1 {}  // OK
open class S4 <: C1 {}   // OK
```

<!-- compile.error -->

```cangjie
package B
import A.*

class SS1 <: S2 {}  // OK
class SS2 <: S3 {}  // Error, S3 is sealed class, cannot be inherited here
sealed class SS3 {} // Error, 'sealed' cannot be used on non-abstract class
```

### 父类构造函数调用

子类的 `init` 构造函数可以使用 `super(args)` 的形式调用父类构造函数，或使用 `this(args)` 的形式调用本类其他构造函数，但两者之间只能调用一个。如果调用，必须在构造函数体内的第一个表达式处，在此之前不能有任何表达式或声明。

<!-- compile -->

```cangjie
open class A {
    A(let a: Int64) {}
}

class B <: A {
    let b: Int64
    init(b: Int64) {
        super(30)
        this.b = b
    }

    init() {
        this(20)
    }
}
```

子类的主构造函数中，可以使用 `super(args)` 的形式调用父类构造函数，但不能使用 `this(args)` 的形式调用本类其他构造函数。

如果子类的构造函数没有显式调用父类构造函数，也没有显式调用其他构造函数，编译器会在该构造函数体的开始处插入直接父类的无参构造函数的调用。如果此时父类没有无参构造函数，则会编译报错。

<!-- compile.error -->

```cangjie
open class A {
    let a: Int64
    init() {
        a = 100
    }
}

open class B <: A {
    let b: Int64
    init(b: Int64) {
        // OK, `super()` added by compiler
        this.b = b
    }
}

open class C <: B {
    let c: Int64
    init(c: Int64) {  // Error, there is no non-parameter constructor in super class
        this.c = c
    }
}
```

### 覆盖和重定义

子类中可以覆盖（override）父类中的同名非抽象实例成员函数，即在子类中为父类中的某个实例成员函数定义新的实现。覆盖时，要求父类中的成员函数使用 `open` 修饰，子类中的同名函数使用 `override` 修饰，其中 `override` 是可选的。例如，下面的例子中，子类 B 中的函数 `f` 覆盖了父类 A 中的函数 `f`。

<!-- verify -->

```cangjie
open class A {
    public open func f(): Unit {
        println("I am superclass")
    }
}

class B <: A {
    public override func f(): Unit {
        println("I am subclass")
    }
}

main() {
    let a: A = A()
    let b: A = B()
    a.f()
    b.f()
}
```

对于被覆盖的函数，调用时将根据变量的运行时类型（由实际赋给该变量的对象决定）确定调用的版本（即所谓的动态派发）。例如，上例中 `a` 的运行时类型是 A，因此 `a.f()` 调用的是父类 A 中的函数 `f`；`b` 的运行时类型是 B（编译时类型是 A），因此 `b.f()` 调用的是子类 B 中的函数 `f`。所以程序会输出：

```text
I am superclass
I am subclass
```

对于静态函数，子类中可以重定义父类中的同名非抽象静态函数，即在子类中为父类中的某个静态函数定义新的实现。重定义时，要求子类中的同名静态函数使用 `redef` 修饰，其中 `redef` 是可选的。例如，下面的例子中，子类 D 中的函数 `foo` 重定义了父类 C 中的函数 `foo`。

<!-- verify -->

```cangjie
open class C {
    public static func foo(): Unit {
        println("I am class C")
    }
}

class D <: C {
    public redef static func foo(): Unit {
        println("I am class D")
    }
}

main() {
    C.foo()
    D.foo()
}
```

对于被重定义的函数，调用时将根据 `class` 的类型决定调用的版本。例如，上例中 `C.foo()` 调用的是父类 C 中的函数 `foo`，`D.foo()` 调用的是子类 D 中的函数 `foo`。

```text
I am class C
I am class D
```

如果抽象函数或 `open` 修饰的函数有命名形参，那么实现函数或 `override` 修饰的函数也需要保持同样的命名形参。

<!-- compile.error -->

```cangjie
open class A {
    public open func f(a!: Int32): Int32 {
        a + 1
    }
}

class B <: A {
    public override func f(a!: Int32): Int32 { // OK
        a + 2
    }
}

class C <: A {
    public override func f(b!: Int32): Int32 { // Error
        b + 3
    }
}

main() {
    B().f(a: 0)
    C().f(b: 0)
}
```

还需要注意的是，当实现或重定义的函数为泛型函数时，子类型函数的类型变元约束需要比父类型中对应函数更宽松或相同。

<!-- compile.error -->

```cangjie
open class A {}
open class B <: A {}
open class C <: B {}

open class Base {
    public open func foo<T>(a: T): Unit where T <: B {}
    public open func bar<T>(a: T): Unit where T <: B {}
    public static func f<T>(a: T): Unit where T <: B {}
    public static func g<T>(): Unit where T <: B {}
}

class D <: Base {
    public override func foo<T>(a: T): Unit where T <: C {} // Error, stricter constraint
    public override func bar<T>(a: T): Unit where T <: C {} // Error, stricter constraint
    public redef static func f<T>(a: T): Unit where T <: C {} // Error, stricter constraint
    public redef static func g<T>(): Unit where T <: C {} // Error, stricter constraint
}

class E <: Base {
    public override func foo<T>(a: T): Unit where T <: A {} // OK: looser constraint
    public override func bar<V>(a: V): Unit where V <: A {} // OK: looser constraint, names of generic parameters do not matter
    public redef static func f<T>(a: T): Unit where T <: A {} // OK: looser constraint
    public redef static func g<T>(): Unit where T <: A {} // OK: looser constraint
}

class F <: Base {
    public override func foo<T>(a: T): Unit where T <: B {} // OK: same constraint
    public override func bar<V>(a: V): Unit where V <: B {} // OK: same constraint
    public redef static func f<T>(a: T): Unit where T <: B {} // OK: same constraint
    public redef static func g<T>(): Unit where T <: B {} // OK: same constraint
}
```
