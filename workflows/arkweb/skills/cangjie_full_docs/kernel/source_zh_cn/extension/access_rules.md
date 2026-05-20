# 访问规则

## 扩展的修饰符

扩展本身不能使用修饰符修饰。

例如，下面的例子中对 A 的直接扩展前使用了 `public` 修饰，将编译报错。

<!-- compile.error -->

```cangjie
public class A {}

public extend A {}  // Error, expected no modifier before extend
```

扩展成员可使用的修饰符有：`static`、`public`、`protected`、`internal`、`private`、`mut`。

- 使用 `private` 修饰的成员只能在本扩展内使用，外部不可见。
- 使用 `internal` 修饰的成员可以在当前包及子包（包括子包的子包）内使用，这是默认行为。
- 使用 `protected` 修饰的成员在本模块内可以被访问（受导出规则限制）。当被扩展类型是 class 时，该 class 的子类定义体也能访问。
- 使用 `static` 修饰的成员，只能通过类型名访问，不能通过实例对象访问。
- 对 `struct` 类型的扩展可以定义 `mut` 函数。

<!-- compile -->

```cangjie
package p1

public open class A {}

extend A {
    public func f1() {}
    protected func f2() {}
    private func f3() {}
    static func f4() {}
}

main() {
    A.f4()
    var a = A()
    a.f1()
    a.f2()
}
```

扩展内的成员定义不支持使用 `open`、`override`、`redef` 修饰。

<!-- compile.error -->

```cangjie
class Foo {
    public open func f() {}
    static func h() {}
}

extend Foo {
    public override func f() {} // Error
    public open func g() {} // Error
    redef static func h() {} // Error
}
```

## 扩展的孤儿规则

为一个其他 `package` 的类型实现另一个 `package` 的接口，可能造成理解上的困扰。

为了防止一个类型被意外实现不合适的接口，仓颉不允许定义孤儿扩展，即既不与接口（包含接口继承链上的所有接口）定义在同一个包中，也不与被扩展类型定义在同一个包中的接口扩展。

如下代码所示，不能在 `package c` 中，为 `package a` 里的 `Foo` 实现 `package b` 里的 `Bar`。

只能在 `package a` 或者在 `package b` 中为 `Foo` 实现 `Bar`。

<!-- compile.error -->

```cangjie
// package a
public class Foo {}

// package b
public interface Bar {}

// package c
import a.Foo
import b.Bar

extend Foo <: Bar {} // Error
```

## 扩展的访问和遮盖

扩展的实例成员与类型定义处一样可以使用 `this`，`this` 的功能保持一致。同样也可以省略 `this` 访问成员。扩展的实例成员不能使用 `super`。

<!-- compile -->

```cangjie
class A {
    var v = 0
}

extend A {
    func f() {
        print(this.v) // OK
        print(v) // OK
    }
}
```

扩展不能访问被扩展类型中 `private` 修饰的成员。

<!-- compile.error -->

```cangjie
class A {
    private var v1 = 0
    protected var v2 = 0
}

extend A {
    func f() {
        print(v1) // Error
        print(v2) // OK
    }
}
```

扩展不能遮盖被扩展类型的任何成员。

<!-- compile.error -->

```cangjie
class A {
    func f() {}
}

extend A {
    func f() {} // Error
}
```

扩展也不允许遮盖其他扩展增加的任何成员。

<!-- compile.error -->

```cangjie
class A {}

extend A {
    func f() {}
}

extend A {
    func f() {} // Error
}
```

在同一个包内，对同一类型可以扩展多次，并且在扩展中可以直接调用被扩展类型的其他扩展中非 `private` 修饰的函数。

<!-- compile.error -->

```cangjie
class Foo {}

extend Foo { // OK
    private func f() {}
    func g() {}
}

extend Foo { // OK
    func h() {
        g() // OK
        f() // Error
    }
}
```

扩展泛型类型时，可以使用额外的泛型约束。泛型类型的任意两个扩展之间的可见性规则如下：

- 如果两个扩展的约束相同，则两个扩展相互可见，即两个扩展内可以直接使用对方内的函数或属性；
- 如果两个扩展的约束不同，且两个扩展的约束有包含关系，约束更宽松的扩展对约束更严格的扩展可见，反之，不可见；
- 当两个扩展的约束不同时，且两个约束不存在包含关系，则两个扩展均互相不可见。

示例：假设对同一个类型 `E<X>` 的两个扩展分别为扩展 `1` 和扩展 `2` ，`X` 的约束在扩展 `1` 中比扩展 `2` 中更严格，那么扩展 `1` 中的函数和属性对扩展 `2` 均不可见，反之，扩展 `2` 中的函数和属性对扩展 `1` 可见。

<!-- compile.error -->

```cangjie
open class A {}
class B <: A {}
class E<X> {}

interface I1 {
    func f1(): Unit
}
interface I2 {
    func f2(): Unit
}

extend<X> E<X> <: I1 where X <: B {  // extension 1
    public func f1(): Unit {
        f2() // OK
    }
}

extend<X> E<X> <: I2 where X <: A   { // extension 2
    public func f2(): Unit {
        f1() // Error
    }
}
```

## 扩展的导入导出

扩展也是可以被导入和导出的，但是扩展本身不能使用可见性修饰符修饰，扩展的导出有一套特殊的规则。

对于直接扩展，当扩展与被扩展的类型在同一个包中，扩展是否导出，由被扩展类型与泛型约束（如果有）的访问修饰符同时决定，当所有的泛型约束都是导出类型（修饰符与导出规则，详见[顶层声明的可见性](../package/toplevel_access.md)章节）时，该扩展将被导出。当扩展与被扩展类型不在同一个包中时，该扩展不会导出。

如以下代码所示，`Foo` 是导出的，`f1` 函数所在的扩展由于不导出泛型约束，故该扩展不会被导出；`f2` 和 `f3` 函数所在的扩展的泛型约束均被导出，故该扩展被导出；`f4` 函数所在的扩展包含多个泛型约束，且泛型约束中 `I1` 未被导出，故该扩展不会被导出；`f5` 函数所在的扩展包含多个泛型约束，所有的泛型约束均是导出的，故该扩展会被导出。

```cangjie
// package a.b
package a.b

private interface I1 {}
internal interface I2 {}
protected interface I3 {}

extend Int64 <: I1 & I2 & I3 {}

public class Foo<T> {}
// The extension will not be exported
extend<T> Foo<T> where T <: I1 {
    public func f1() {}
}
// The extension will be exported, and only packages that import both Foo and I2 will be able to access it.
extend<T> Foo<T> where T <: I2 {
    public func f2() {}
}
// The extension will be exported, and only packages that import both Foo and I3 will be able to access it.
extend<T> Foo<T> where T <: I3 {
    public func f3() {}
}
// The extension will not be exported. The I1 with the lowest access level determines the export.
extend<T> Foo<T> where T <: I1 & I2 & I3 {
    public func f4() {}
}
// The extension is exported. Only the package that imports Foo, I2, and I3 can access the extension.
extend<T> Foo<T> where T <: I2 & I3 {
    public func f5() {}
}

// package a.c
package a.c
import a.b.*

main() {
    Foo<Int64>().f1() // Cannot access.
    Foo<Int64>().f2() // Cannot access. Visible only for sub-pkg.
    Foo<Int64>().f3() // OK.
    Foo<Int64>().f4() // Cannot access.
    Foo<Int64>().f5() // Cannot access. Visible only for sub-pkg.
}

// package a.b.d
package a.b.d
import a.b.*

main() {
    Foo<Int64>().f1() // Cannot access.
    Foo<Int64>().f2() // OK.
    Foo<Int64>().f3() // OK.
    Foo<Int64>().f4() // Cannot access.
    Foo<Int64>().f5() // OK.
}
```

对于接口扩展则分为两种情况：

1. 当接口扩展与被扩展类型在相同的 `package` 时，扩展会与被扩展类型以及泛型约束（如果有）一起被导出，不受接口类型的访问级别影响，包外不需要导入接口类型也能访问该扩展的成员。
2. 当接口扩展与被扩展类型在不同的 `package` 时，接口扩展是否导出由接口类型以及泛型约束（如果有）里用到的类型中最小的访问级别决定。其他 `package` 必须导入被扩展类型、相应的接口以及约束用到的类型（如果有），才能访问对应接口包含的扩展成员。

如下代码所示，在包 `a` 中，虽然接口访问修饰符为 `private`，但 `Foo` 的扩展仍然会被导出。

```cangjie
// package a
package a

private interface I0 {}

public class Foo<T> {}

// The extension is exported.
extend<T> Foo<T> <: I0 {}
```

当在其他包中为 `Foo` 类型扩展时，扩展是否导出由实现接口和泛型约束的访问修饰符决定。实现接口至少存在一个导出的接口，且所有的泛型约束均可导出时，该扩展将被导出。

```cangjie
// package b
package b

import a.Foo

private interface I1 {}
internal interface I2 {}
protected interface I3 {}
public interface I4 {}

// The extension will not be exported because I1 is not visible outside the file.
extend<T> Foo<T> <: I1 {}

// The extension is exported.
extend<T> Foo<T> <: I2 {}

// The extension is exported.
extend<T> Foo<T> <: I3 {}

// The extension is exported
extend<T> Foo<T> <: I1 & I2 & I3 {}

// The extension will not be exported. The I1 with the lowest access level determines the export.
extend<T> Foo<T> <: I4 where T <: I1 & I2 & I3 {}

// The extension is exported.
extend<T> Foo<T> <: I4 where T <: I2 & I3 {}

// The extension is exported.
extend<T> Foo<T> <: I4 & I3 where T <: I2 {}
```

特别的，接口扩展导出的成员仅限于接口中包含的成员。

<!-- compile.error -access_rules3 -->
<!-- cfg="-p a --output-type=staticlib" -->

```cangjie
// package a
package a

public class Foo {}
```

<!-- compile.error -access_rules3 -->
<!-- cfg="-p b --output-type=staticlib" -->

```cangjie
// package b
package b

import a.Foo

public interface I1 {
    func f1(): Unit
}

public interface I2 {
    func f2(): Unit
}

extend Foo <: I1 & I2 {
    public func f1(): Unit {}
    public func f2(): Unit {}
    public func f3(): Unit {} // f3 will not be exported
}
```

<!-- compile.error -access_rules3 -->
<!-- cfg="-p c --output-type=staticlib" -->
<!-- cfg="liba.a libb.a" -->

```cangjie
// package c
package c

import a.Foo
import b.I1

main() {
    let x: Foo = Foo()
    x.f1() // OK, because f1 is a member of I1.
    x.f2() // error, I2 is not imported
    x.f3() // error, f3 not found
}
```

与扩展的导出类似，扩展的导入也不需要显式地用 `import` 导入，扩展的导入只需要导入被扩展的类型、接口和泛型约束，就可以导入可访问的所有扩展。

如下面的代码所示，在 `package b` 中，只需要导入 `Foo` 就可以使用 `Foo` 对应的扩展中的函数 `f`。

而对于接口扩展，需要同时导入被扩展的类型、扩展的接口和泛型约束（如果有）才能使用。因此在 `package c` 中，需要同时导入 `Foo` 和 `I` 才能使用对应扩展中的函数 `g`。

<!-- compile -->

```cangjie
// package a
package a
public class Foo {}
extend Foo {
    public func f() {}
}
```

```cangjie
// package b
package b
import a.Foo

public interface I {
    func g(): Unit
}
extend Foo <: I {
    public func g() {
        this.f() // OK
    }
}
```

```cangjie
// package c
package c
import a.Foo
import b.I

func test() {
    let a = Foo()
    a.f() // OK
    a.g() // OK
}
```
