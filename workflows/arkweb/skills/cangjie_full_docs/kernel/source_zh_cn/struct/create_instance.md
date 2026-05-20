# 创建 struct 实例

定义了 `struct` 类型后，即可通过调用 `struct` 的构造函数来创建 `struct` 实例。在 `struct` 定义之外，通过 `struct` 类型名调用构造函数创建该类型实例，并可以通过实例访问满足可见性修饰符（如`public`）的实例成员变量和实例成员函数。例如，下例中定义了一个 `Rectangle` 类型的变量 `r`，通过 `r.width` 和 `r.height` 可分别访问 `r` 中 `width` 和 `height` 的值，通过 `r.area()` 可以调用 `r` 的成员函数 `area`。

<!-- compile -->

```cangjie
struct Rectangle {
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
let r = Rectangle(10, 20)
let width = r.width   // width = 10
let height = r.height // height = 20
let a = r.area()      // a = 200
```

如果希望通过 `struct` 实例去修改成员变量的值，需要将 `struct` 类型的变量定义为可变变量，并且被修改的成员变量也必须是可变成员变量（使用 `var` 定义）。举例如下：

<!-- run -->

```cangjie
struct Rectangle {
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
    var r = Rectangle(10, 20) // r.width = 10, r.height = 20
    r.width = 8               // r.width = 8
    r.height = 24             // r.height = 24
    let a = r.area()          // a = 192
}
```

在赋值或传参时，会对 `struct` 实例进行复制（成员变量为引用类型时，仅复制引用而不会复制引用的对象），生成新的实例，对其中一个实例的修改并不会影响另外一个实例。以赋值为例，下面的例子中，将 `r1` 赋值给 `r2` 之后，修改 `r1` 的 `width` 和 `height` 的值，并不会影响 `r2` 的 `width` 和 `height` 值。

<!-- run -->

```cangjie
struct Rectangle {
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
    var r1 = Rectangle(10, 20) // r1.width = 10, r1.height = 20
    var r2 = r1                // r2.width = 10, r2.height = 20
    r1.width = 8               // r1.width = 8
    r1.height = 24             // r1.height = 24
    let a1 = r1.area()         // a1 = 192
    let a2 = r2.area()         // a2 = 200
}
```
