---
name: cangjie-extension
description: 仓颉语言扩展。当需要了解仓颉语言的直接扩展(extend)、接口扩展、泛型扩展、扩展中的访问规则、孤儿规则、导出与导入规则等特性时，应使用此 Skill。
descriptionZH: 仓颉语言扩展。当需要了解仓颉语言的直接扩展(extend)、接口扩展、泛型扩展、扩展中的访问规则、孤儿规则、导出与导入规则等特性时，应使用此 Skill。
tags:
  - 仓颉
  - 扩展
---

# 仓颉语言扩展 Skill

## 1. 扩展概述

### 1.1 目的
扩展为当前包中任何可见类型添加新功能 — 函数、元组和接口除外。

### 1.2 可添加的内容
- 成员函数
- 运算符重载函数
- 成员属性（带 `get`/`set`）
- 接口实现

### 1.3 不能做的事
1. 添加成员变量（存储属性）
2. 定义无实现体的函数/属性
3. 对扩展成员使用 `open`、`override` 或 `redef`
4. 访问被扩展类型的 `private` 成员

### 1.4 两个类别
- **直接扩展**：不涉及接口 — 仅添加函数/属性
- **接口扩展**：为类型实现一个或多个接口

---

## 2. 直接扩展

### 2.1 基本语法与示例
```cangjie
extend String {
    public func printSize() {
        println("the size is ${this.size}")
    }
}

main() {
    let a = "123"
    a.printSize()  // 输出：the size is 3
}
```

### 2.2 为类型添加属性和运算符
```cangjie
class Boo {
    var boo: Int64 = 2
}

extend Boo {
    public prop x: Int64 {     // 添加成员属性
        get() { 123 }
    }

    public operator func -(): Int64 { // 添加运算符重载
        -x
    }
}
```

### 2.3 扩展泛型类型 — 两种形式

**形式 A：扩展完全实例化的泛型类型：**
```cangjie
class Foo<T> where T <: ToString {}

extend Foo<Int64> { ... }   // 仅适用于 Foo<Int64>
```

**形式 B：带新类型参数的泛型扩展：**
```cangjie
class MyList<T> {}

extend<T> MyList<T> { ... }
extend<T, R> MyList<(T, R)> { ... }
```
- `extend` 后声明的每个类型参数**须**在被扩展类型中使用
```cangjie
// ❌ 错误示例
extend MyList {}              // Error: 泛型类型须带类型实参
extend<T, R> MyList<T> {}     // Error: R 未被使用
```

### 2.4 扩展中的额外泛型约束
- 可添加 `where` 子句限制扩展成员的可用条件：
```cangjie
class Pair<T1, T2> {
    var first: T1
    var second: T2
    public init(a: T1, b: T2) {
        first = a
        second = b
    }
}

interface Eq<T> {
    func equals(other: T): Bool
}

// 仅当 T1、T2 支持判等时，Pair 才有 equals 方法
extend<T1, T2> Pair<T1, T2> where T1 <: Eq<T1>, T2 <: Eq<T2> {
    public func equals(other: Pair<T1, T2>): Bool {
        first.equals(other.first) && second.equals(other.second)
    }
}
```

---

## 3. 接口扩展

### 3.1 基本语法
```cangjie
interface PrintSizeable {
    func printSize(): Unit
}

extend<T> Array<T> <: PrintSizeable {
    public func printSize() {
        println("The size is ${this.size}")
    }
}

main() {
    let a: PrintSizeable = Array<Int64>()
    a.printSize()  // 输出：The size is 0
}
```

### 3.2 实现多个接口
使用 `&` 在一个扩展中实现多个接口：
```cangjie
interface I1 { func f1(): Unit }
interface I2 { func f2(): Unit }
interface I3 { func f3(): Unit }
class Foo {}

extend Foo <: I1 & I2 & I3 {
    public func f1(): Unit {}
    public func f2(): Unit {}
    public func f3(): Unit {}
}
```

### 3.3 已满足的接口成员
若类型已有所需成员，扩展体可为空：
```cangjie
interface Sizeable {
    prop size: Int64
}

extend<T> Array<T> <: Sizeable {}  // Array 已有 prop size

main() {
    let a: Sizeable = Array<Int64>()
    println(a.size)  // 输出：0
}
```
**不能**重新实现已存在的成员

### 3.4 接口继承与检查顺序
- 父接口扩展先检查，然后子接口
- 子接口的默认实现**覆盖**父接口的
- 两个无关接口提供同一成员的冲突默认实现 → **编译错误**
```cangjie
interface I1 {
    func foo(): Unit { println("I1 foo") }
}
interface I2 <: I1 {
    func foo(): Unit { println("I2 foo") }
}
class A {}

extend A <: I1 {}  // 先检查
extend A <: I2 {}  // 后检查，I2.foo 覆盖 I1.foo

main() {
    A().foo()  // 输出：I2 foo
}
```

### 3.5 接口扩展中的泛型约束
```cangjie
// 当 T1、T2 可判等时，让 Pair 实现 Eq 接口
extend<T1, T2> Pair<T1, T2> <: Eq<Pair<T1, T2>> where T1 <: Eq<T1>, T2 <: Eq<T2> {
    public func equals(other: Pair<T1, T2>): Bool {
        first.equals(other.first) && second.equals(other.second)
    }
}
```

---

## 4. 访问规则

### 4.1 扩展级修饰符
- **扩展本身不能有修饰符**
```cangjie
public class A {}
public extend A {}  // ❌ Error: 扩展前不能有修饰符
```

### 4.2 成员级修饰符
允许：`static`、`public`、`protected`、`internal`、`private`、`mut`

| 修饰符 | 作用域 |
|--------|--------|
| `private` | 仅在扩展块内 |
| `internal` | 当前包及子包（默认） |
| `protected` | 当前模块 |
| `public` | 全局可见 |
| `static` | 仅通过类型名访问 |
| `mut` | 结构体扩展中的可变函数 |

**不允许**用于扩展成员的修饰符：`open`、`override`、`redef`

### 4.3 扩展 struct 的 `mut` 函数
```cangjie
struct Counter {
    var count: Int64 = 0
}

extend Counter {
    public mut func increment() {
        count += 1
    }
}

main() {
    var c = Counter()  // 须为 var 才能调用 mut 函数
    c.increment()
    println(c.count)   // 输出：1
}
```

### 4.4 孤儿规则
不能为**接口和类型均来自不同包**的情况实现接口。扩展须与被扩展类型或接口（含接口继承链上的所有接口）在**同一个包**中。
```cangjie
// package a
public class Foo {}
```
```cangjie
// package b
public interface Bar {}
```
```cangjie
// package c
import a.Foo
import b.Bar
extend Foo <: Bar {}  // ❌ Error: 孤儿扩展
// 须在 package a 或 package b 中为 Foo 实现 Bar
```

### 4.5 `this` 和 `super`
- 扩展实例成员**可以**使用 `this`（可省略）
- 扩展实例成员**不能**使用 `super`
```cangjie
class A {
    var v = 0
}
extend A {
    func f() {
        print(this.v)  // OK
        print(v)       // OK，省略 this
    }
}
```

### 4.6 不能访问 `private` 成员
扩展不能读写被扩展类型的 `private` 成员。`protected` 及以上可访问
```cangjie
class A {
    private var v1 = 0
    protected var v2 = 0
}
extend A {
    func f() {
        print(v1)  // ❌ Error: 不能访问 private 成员
        print(v2)  // OK
    }
}
```

### 4.7 不能遮蔽
- 扩展**不能**重定义类型上已有的成员
- 扩展**不能**重定义同一类型的另一个扩展中的成员
```cangjie
class A {
    func f() {}
}
extend A {
    func f() {}  // ❌ Error: 不能遮蔽已有成员
}

// 两个扩展之间也不能遮蔽
extend A {
    func g() {}
}
extend A {
    func g() {}  // ❌ Error
}
```

### 4.8 跨扩展可见性（同一包）
- 同一包中允许同一类型的多个扩展
- 一个扩展中的非 `private` 成员可从另一个扩展调用
- `private` 成员仅限于其自己的扩展块
```cangjie
class Foo {}

extend Foo {
    private func f() {}
    func g() {}          // 默认 internal
}

extend Foo {
    func h() {
        g()  // OK: 可访问其他扩展的非 private 成员
        f()  // ❌ Error: f 是 private
    }
}
```

### 4.9 泛型扩展可见性规则
- **相同约束** → 互相可见
- **子集约束** → 较宽松扩展的成员对较严格扩展可见，反之不可
- **无关约束** → 互相不可见
```cangjie
open class A {}
class B <: A {}
class E<X> {}

interface I1 { func f1(): Unit }
interface I2 { func f2(): Unit }

extend<X> E<X> <: I1 where X <: B {   // 扩展 1（更严格）
    public func f1(): Unit {
        f2()  // OK: 较宽松扩展的成员可见
    }
}

extend<X> E<X> <: I2 where X <: A {   // 扩展 2（更宽松）
    public func f2(): Unit {
        f1()  // ❌ Error: 较严格扩展的成员不可见
    }
}
```

### 4.10 导出规则

#### 直接扩展
- 与被扩展类型**同包**时，当类型和所有泛型约束均为导出类型时导出
- **不同包**时，永不导出

#### 接口扩展（与类型同包）
- 随类型一起导出，**无论**接口的访问级别如何

#### 接口扩展（与类型不同包）
- 导出由所实现接口和泛型约束中**最低访问级别**决定
- 仅接口中声明的成员被导出

### 4.11 导入规则
- 扩展**隐式导入** — 无需显式 `import` 扩展本身
- **直接扩展**：导入被扩展类型自动导入其导出的直接扩展
- **接口扩展**：须同时导入被扩展类型**和**接口才能访问扩展成员
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
public interface I { func g(): Unit }
extend Foo <: I {
    public func g() { this.f() }  // OK
}
```
```cangjie
// package c — 使用扩展
package c
import a.Foo
import b.I

func test() {
    let a = Foo()
    a.f()  // OK：直接扩展随 Foo 导入
    a.g()  // OK：已导入 Foo 和 I
}
```
