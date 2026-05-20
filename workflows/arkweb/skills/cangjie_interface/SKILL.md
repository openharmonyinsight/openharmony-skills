---
name: cangjie-interface
description: 仓颉语言接口。当需要了解仓颉语言的接口定义、接口实现(单个/多个)、接口继承、默认实现(实例/静态)、sealed接口、泛型成员、Any类型、属性(prop)在接口中的使用、菱形继承解决方案等特性时，应使用此
  Skill。
descriptionZH: 仓颉语言接口。当需要了解仓颉语言的接口定义、接口实现(单个/多个)、接口继承、默认实现(实例/静态)、sealed接口、泛型成员、Any类型、属性(prop)在接口中的使用、菱形继承解决方案等特性时，应使用此
  Skill。
tags:
  - 仓颉
  - 接口
---

# 仓颉语言接口 Skill

## 1. 接口定义

### 1.1 基本语法
- `interface I { ... }` — 定义抽象类型，不包含数据，定义类型的行为
- 成员可包含：成员函数、操作符重载函数、成员属性（prop）
- 成员隐式 `public`（不允许额外访问修饰符）。实现者须使用 `public`
- `interface` 隐式 `open`（`open` 修饰符可选）

### 1.2 接口定义与实现示例
```cangjie
interface Flyable {
    func fly(): Unit
}

class Bird <: Flyable {
    public func fly(): Unit {
        println("Bird flying")
    }
}

class Airplane <: Flyable {
    public func fly(): Unit {
        println("Airplane flying")
    }
}

// 接口作为参数类型，实现多态
func fly(item: Flyable): Unit {
    item.fly()
}

main() {
    fly(Bird())      // 输出：Bird flying
    fly(Airplane())  // 输出：Airplane flying
}
```

### 1.3 `sealed interface`
- `sealed interface` — 仅同包内可继承/实现/扩展
- `sealed` 隐含 `public`/`open` 语义
- 继承 `sealed` 接口的子接口仍可被 `sealed` 修饰或不使用 `sealed`
- 若继承 `sealed` 接口的子接口被 `public` 修饰且不被 `sealed` 修饰，则该子接口可在包外被继承/实现/扩展
```cangjie
package A
sealed interface Shape {
    func area(): Float64
}

class Circle <: Shape {
    var radius: Float64
    public init(r: Float64) { radius = r }
    public func area(): Float64 { 3.14159 * radius * radius }
}

// 包外不能实现 Shape（sealed），但可通过非 sealed 的 public 子接口间接实现
```

---

## 2. 接口实现

### 2.1 基本实现
- `class Foo <: I { ... }` — 须实现 `I` 的所有成员。`Foo` 成为 `I` 的子类型
- 多接口：`class C <: I1 & I2 { ... }`（无顺序要求）
```cangjie
interface Addable {
    func add(other: Int64): Int64
}
interface Subtractable {
    func sub(other: Int64): Int64
}

class MyInt <: Addable & Subtractable {
    var value = 0
    public func add(other: Int64): Int64 { value + other }
    public func sub(other: Int64): Int64 { value - other }
}
```

### 2.2 可实现接口的类型
- 除 Tuple、VArray 和函数类型外的所有类型

### 2.3 三种实现途径
1. 在类型定义处声明实现
2. 通过扩展实现接口（详见 `cangjie-extension` Skill）
3. 语言内置实现

### 2.4 实现规则
- **函数**：名称、参数列表、返回类型须相同。例外：若接口返回类型为 `class`，实现者可返回其子类
- **`mut` 函数**：接口中声明的 `mut` 函数，`class` 实现时**忽略** `mut` 修饰（class 实例成员函数始终可修改实例状态），`struct` 实现时**须**匹配 `mut` 修饰符
- **属性**：`mut` 修饰符须匹配；类型须相同
- 实现时函数或属性定义前的 `override`/`redef` 修饰符可选（无论接口中是否有默认实现）

### 2.5 返回子类型示例
```cangjie
open class Base {}
class Sub <: Base {}

interface I {
    func f(): Base
}

class C <: I {
    public func f(): Sub {  // 允许返回 Base 的子类型
        Sub()
    }
}
```

### 2.6 `mut` 函数实现示例
```cangjie
interface Resettable {
    mut func reset(): Unit
}

struct Counter <: Resettable {
    var count: Int64 = 0
    public mut func reset(): Unit {  // struct 须匹配 mut
        count = 0
    }
}

class Logger <: Resettable {
    var entries = 0
    public func reset(): Unit {  // class 忽略 mut
        entries = 0
    }
}
```

---

## 3. 接口继承

### 3.1 基本规则
- 接口可继承一个或多个接口（不能继承类）：`interface I3 <: I1 & I2 { ... }`
- 可添加新成员。实现 `I3` 须实现 `I1`、`I2`、`I3` 的所有成员
```cangjie
interface Addable {
    func add(other: Int64): Int64
}
interface Subtractable {
    func sub(other: Int64): Int64
}

// Calculable 继承了 Addable 和 Subtractable，并添加新成员
interface Calculable <: Addable & Subtractable {
    func mul(other: Int64): Int64
    func div(other: Int64): Int64
}

class MyInt <: Calculable {
    var value = 0
    public func add(other: Int64): Int64 { value + other }
    public func sub(other: Int64): Int64 { value - other }
    public func mul(other: Int64): Int64 { value * other }
    public func div(other: Int64): Int64 { value / other }
}

main() {
    let myInt = MyInt()
    // MyInt 同时是 Calculable、Addable、Subtractable 的子类型
    let add: Addable = myInt
    let calc: Calculable = myInt
}
```

### 3.2 子接口覆盖父接口成员
- 父接口成员**有**默认实现 → 子接口不允许仅写声明，须给出新的默认实现
- 父接口成员**无**默认实现 → 子接口允许仅写声明，也允许定义默认实现
- `override`（实例函数）/ `redef`（静态函数）修饰符可选
```cangjie
interface I1 {
    func f(a: Int64): Int64 { a }          // 有默认实现
    func f1(a: Int64): Unit                // 无默认实现
}

interface I2 <: I1 {
    func f(a: Int64): Int64 { a + 1 }      // 须提供新的默认实现
    func f1(a: Int64): Unit {}      // 可以仅声明，也可提供默认实现
}
```

---

## 4. 默认实现

### 4.1 实例成员默认实现
- 接口成员可有默认实现
- 实现类型可继承默认实现，也可提供自己的实现
```cangjie
interface SayHi {
    func say(): String { "hi" }
}

class A <: SayHi {}  // 继承默认实现

class B <: SayHi {
    public func say(): String { "hi, B" }  // 覆盖默认实现
}
```

### 4.2 静态成员默认实现
- 有默认实现的静态成员可通过接口名和实现者名访问
- 无默认实现的静态成员不能通过接口名直接访问
- 通常在泛型约束中使用静态成员：`func f<T>() where T <: I { T.staticFunc() }`
```cangjie
interface NamedType {
    static func typename(): String {
        "interface NamedType"
    }
}

class A <: NamedType {}

main() {
    println(NamedType.typename())  // 输出：interface NamedType
    println(A.typename())          // 输出：interface NamedType
}
```

### 4.3 在泛型约束中使用静态成员
```cangjie
interface NamedType {
    static func typename(): String
}

class A <: NamedType {
    public static func typename(): String { "A" }
}
class B <: NamedType {
    public static func typename(): String { "B" }
}

func printTypeName<T>() where T <: NamedType {
    println("the type is ${T.typename()}")
}

main() {
    printTypeName<A>()  // 输出：the type is A
    printTypeName<B>()  // 输出：the type is B
}
```

### 4.4 菱形继承解决
- 若多个继承接口提供同一成员的冲突默认实现，实现者**须**提供自己的实现
```cangjie
interface SayHi {
    func say(): String { "hi" }
}
interface SayHello {
    func say(): String { "hello" }
}

// 两个接口都有 say 的默认实现，产生冲突
class Foo <: SayHi & SayHello {
    public func say(): String { "Foo" }  // 须自行实现，否则编译错误
}
```

---

## 5. 泛型成员
- 接口可定义具有 `open` 语义的泛型实例/静态函数
- 实现时泛型参数名称可不同
```cangjie
import std.collection.ArrayList

interface M {
    func foo<T>(a: T): T
    static func toString<T>(b: ArrayList<T>): String where T <: ToString
}

class C <: M {
    public func foo<S>(a: S): S { a }  // 泛型参数名可不同
    public static func toString<T>(b: ArrayList<T>) where T <: ToString {
        var res = ""
        for (s in b) {
            res += s.toString()
        }
        res
    }
}
```

---

## 6. `Any` 类型
- 内置接口：`interface Any {}`
- 所有接口默认继承 `Any`；所有非接口类型默认实现 `Any`
- 每个类型都是 `Any` 的子类型
```cangjie
main() {
    var any: Any = 1
    any = 2.0
    any = "hello, world!"
}
```

---

## 7. 属性（prop）在接口中的使用

### 7.1 抽象属性
- 在接口中可声明抽象属性（无实现）
- 实现类型须提供实现
```cangjie
interface HasName {
    prop name: String
    mut prop id: Int64
}

class User <: HasName {
    var _id: Int64 = 0
    public prop name: String {
        get() { "User" }
    }
    public mut prop id: Int64 {
        get() { _id }
        set(v) { _id = v }
    }
}
```

### 7.2 默认实现属性
- 接口中的属性也可提供默认实现
- 实现类型可继承或覆盖

### 7.3 实现规则
- 若接口属性有 `mut`，实现类型也须有 `mut`，类型须相同

---

## 8. 接口成员访问修饰符
- 接口成员默认 `public`，不可声明额外的访问修饰符
- 实现类型中对应成员**须**使用 `public`
```cangjie
interface I {
    func f(): Unit
}

open class C <: I {
    protected func f() {}  // ❌ Error: 须为 public
}
```
