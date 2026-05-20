---
name: cangjie-const
description: 仓颉语言 const 变量与 const 函数。当需要了解仓颉语言的 const 变量定义、const 表达式、const
  函数、编译时求值、const init 构造函数等特性时，应使用此 Skill。
descriptionZH: 仓颉语言 const 变量与 const 函数。当需要了解仓颉语言的 const 变量定义、const 表达式、const
  函数、编译时求值、const init 构造函数等特性时，应使用此 Skill。
tags:
  - 仓颉
  - const
---

# 仓颉语言 const 变量与 const 函数 Skill

## 1. const 变量

### 1.1 基本语法
```cangjie
const G = 6.674e-11
```
- 使用 `const` 修饰符声明，表示编译时常量，深度不可变
- 不能省略初始化器
- 可用于全局、局部或静态成员（不可在扩展中）

### 1.2 与 let/var 的区别
- `let`：不可变，只能赋值一次，运行时绑定
- `var`：可变，可多次赋值
- `const`：编译时常量，深度不可变，初始化表达式必须是 const 表达式

---

## 2. const 表达式

可在编译时求值的表达式，包括：
1. 数值类型、`Bool`、`Unit`、`Rune`、`String`（不包含插值字符串）的字面量
2. 所有元素都是 const 表达式的 `Array` 字面量（不能是 `Array` 类型，可以使用 `VArray` 类型）和元组字面量
3. `const` 变量、`const` 函数形参、`const` 函数中的局部变量
4. `const` 函数，包含使用 `const` 声明的函数名、符合 `const` 函数要求的 `lambda`、以及这些函数返回的函数表达式
5. `const` 函数调用（包含 `const` 构造函数），该函数的表达式必须是 const 表达式，所有实参必须都是 const 表达式
6. 所有参数都是 const 表达式的 `enum` 构造器调用，和无参数的 `enum` 构造器
7. 数值类型、`Bool`、`Unit`、`Rune`、`String` 类型的算术表达式、关系表达式、位运算表达式，所有操作数都必须是 const 表达式
8. `if`、`match`、`try`、`throw`、`return`、`is`、`as` — 这些表达式内的表达式必须都是 const 表达式
9. const 表达式的成员访问（不包含属性的访问），元组的索引访问
10. `const init` 和 `const` 函数中的 `this` 和 `super` 表达式
11. `const` 表达式的 `const` 实例成员函数调用，且所有实参必须都是 const 表达式

---

## 3. const 函数

### 3.1 基本语法
```cangjie
const func distance(a: Point, b: Point) {
    let dx = a.x - b.x
    let dy = a.y - b.y
    (dx ** 2 + dy ** 2) ** 0.5
}
```
- 用 `const` 修饰符声明
- 在 `const` 上下文中 → 编译时求值；在非 `const` 上下文中 → 运行时求值

### 3.2 规则
1. `const` 函数声明必须使用 `const` 修饰
2. 全局 `const` 函数和 `static const` 函数中只能访问 `const` 声明的外部变量（包含 `const` 全局变量、`const` 静态成员变量）。`const init` 函数和 `const` 实例成员函数除了能访问 `const` 声明的外部变量，还可以访问当前类型的实例成员变量
3. `const` 函数中的表达式都必须是 const 表达式（`const init` 函数除外）
4. `const` 函数中可以使用 `let`、`const` 声明新的局部变量，但不支持 `var`
5. `const` 函数中的参数类型和返回类型没有特殊规定。如果该函数调用的实参不符合 const 表达式要求，那这个函数调用不能作为 const 表达式使用，但仍然可以作为普通表达式使用
6. `const` 函数不一定都会在编译时执行，例如可以在非 `const` 函数中运行时调用
7. `const` 函数与非 `const` 函数重载规则一致
8. 数值类型、`Bool`、`Unit`、`Rune`、`String` 类型和 `enum` 支持定义 `const` 实例成员函数
9. 对于 `struct` 和 `class`，只有定义了 `const init` 才能定义 `const` 实例成员函数。`class` 中的 `const` 实例成员函数不能是 `open` 的。`struct` 中的 `const` 实例成员函数不能是 `mut` 的

### 3.3 接口中的 const 函数
- 接口中的 `const` 函数，实现类型必须也用 `const` 函数才算实现接口
- 接口中的非 `const` 函数，实现类型使用 `const` 或非 `const` 函数都算实现接口
- 接口中的 `const` 函数与接口的 `static` 函数一样，只有在该接口作为泛型约束的时候，受约束的泛型变元或变量才能使用这些 `const` 函数

```cangjie
interface I {
    const func f(): Int64
    const static func f2(): Int64
}

class A <: I {
    public const func f() { 0 }
    public const static func f2() { 1 }
    const init() {}
}

const func g<T>(i: T) where T <: I {
    return i.f() + T.f2()
}
```

---

## 4. const init

如果一个 `struct` 或 `class` 定义了 `const` 构造器，那么这个 `struct`/`class` 实例可以用在 const 表达式中。

### 4.1 基本语法
```cangjie
struct Point {
    const Point(let x: Float64, let y: Float64) {}
}
```

### 4.2 规则
- **class 规则**：不能具有 `var` 声明的实例成员变量；如果当前类型具有父类，当前的 `const init` 必须调用父类的 `const init`（可以显式调用或者隐式调用无参 `const init`），如果父类没有 `const init` 则报错
- 当前类型的实例成员变量如果有初始值，初始值必须要是 const 表达式，否则不允许定义 `const init`
- `const init` 内可以使用赋值表达式 `=` 对实例成员变量赋值，除此以外不能有其他赋值表达式（如 `+=`、`-=`）
- `const init` 与 `const` 函数的区别是 `const init` 内允许对实例成员变量进行赋值（需要使用赋值表达式）

### 4.3 完整示例
```cangjie
struct Point {
    const Point(let x: Float64, let y: Float64) {}
}

const func distance(a: Point, b: Point) {
    let dx = a.x - b.x
    let dy = a.y - b.y
    (dx ** 2 + dy ** 2) ** 0.5
}

main() {
    const a = Point(3.0, 0.0)
    const b = Point(0.0, 4.0)
    const d = distance(a, b)
    println(d) // 输出 5.000000
}
```
