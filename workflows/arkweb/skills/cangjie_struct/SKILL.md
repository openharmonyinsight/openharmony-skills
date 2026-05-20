---
name: cangjie-struct
description: 仓颉语言结构体。当需要了解仓颉语言的struct定义、构造函数(init/主构造函数)、值语义、成员访问与修改规则、mut函数及其限制等特性时，应使用此
  Skill。
descriptionZH: 仓颉语言结构体。当需要了解仓颉语言的struct定义、构造函数(init/主构造函数)、值语义、成员访问与修改规则、mut函数及其限制等特性时，应使用此
  Skill。
tags:
  - 仓颉
  - 结构体
---

# 仓颉语言 struct 使用指导

## 1. 结构体定义

### 1.1 基本语法
```cangjie
struct Rectangle {
    let width: Int64
    let height: Int64
    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }
    public func area() { width * height }
}
```
- 使用 `struct` 关键字 + 名称 + `{}` 体定义
- **仅可在顶层作用域定义**
- 结构体体内可包含：成员变量、成员属性、静态初始化器、构造函数、成员函数

### 1.2 成员变量
- **实例成员变量**：通过结构体实例访问。可有初始值，也可无初始值（须有类型标注）
- **静态成员变量**：用 `static` 声明，通过结构体类型名访问（非实例）

### 1.3 静态初始化器
- `static init()` — 无参数，不允许访问修饰符
- 须初始化所有未初始化的静态成员变量
- 每个结构体**最多一个**

### 1.4 构造函数

#### 普通构造函数（init）
- `init(params) { ... }`
- 函数体**须**初始化所有未初始化的实例成员变量
- 使用 `this` 消除参数名与成员变量名的歧义
- 多个 `init` 构造函数**仅在构成有效重载时**允许

#### 主构造函数
- 名称 = 结构体类型名。每个结构体**最多一个**
- 参数可以是**普通参数**或**成员变量参数**（前缀 `let`/`var`），后者同时定义成员变量和构造函数参数
```cangjie
struct Rectangle {
    public Rectangle(let width: Int64, let height: Int64) {}
}
```

#### 自动生成的无参构造函数
- 当**无**自定义构造函数（包括主构造函数）**且所有**实例成员变量有初始值时 → 编译器自动生成 `public init()`

### 1.5 成员函数
- **实例成员函数**：通过实例访问。可使用 `this` 访问实例成员变量。也可访问静态成员
- **静态成员函数**（`static func`）：通过类型名访问。**不能**访问实例成员或调用实例函数
- **限制**：同一个结构体中，静态方法和实例方法**不能同名**（即使参数不同）

### 1.6 成员属性（prop）
- `prop name: Type { get() { ... } }` — 只读属性
- `mut prop name: Type { get() { ... } set(v) { ... } }` — 读写属性
- 实例属性通过实例访问，静态属性（`static prop`）通过类型名访问
- 属性的详细规则参见 `cangjie-class` Skill 第 4 节

### 1.7 访问修饰符
| 修饰符 | 可见性 |
|--------|--------|
| `private` | 仅在结构体定义内 |
| `internal`（默认） | 当前包及子包 |
| `protected` | 当前模块 |
| `public` | 全局可见 |

### 1.8 禁止递归结构体
- 直接和间接递归均**不合法**（编译错误）：
```cangjie
struct R1 { let other: R1 }         // 错误：自引用
struct R2 { let other: R3 }         // 错误：相互引用
struct R3 { let other: R2 }
```

---

## 2. 创建结构体实例

### 2.1 创建
- 通过结构体类型名调用构造函数：`let r = Rectangle(10, 20)`
- 通过实例访问成员：`r.width`、`r.area()`

### 2.2 修改实例成员须满足两个条件
1. 持有实例的变量须为 `var`（可变）
2. 被修改的成员变量须声明为 `var`

### 2.3 值语义（赋值/传参时复制）
- 赋值或传递结构体实例会创建**副本**（浅拷贝 — 引用类型成员仅复制引用）
- 修改一个副本**不影响**另一个

---

## 3. `mut` 函数

### 3.1 问题
- 由于结构体是值类型，普通实例成员函数**不能**修改实例的成员变量

### 3.2 解决方案
- `mut` 函数 — 特殊的实例成员函数，**可以**原地修改结构体实例
```cangjie
struct Foo {
    var i = 0
    public mut func g() { i += 1 }  // 合法
}
```

### 3.3 `mut` 允许使用的位置
- 仅在 `interface`、`struct` 和结构体扩展中
- **不能用于 `class`**（类是引用类型，实例函数本身就能修改成员）

### 3.4 `mut` 不能修饰静态函数
```cangjie
public mut static func g(): Unit {} // 错误
```

### 3.5 `mut` 也可修饰运算符函数
```cangjie
public mut operator func +(rhs: A): A { A() }  // 合法
```

### 3.6 `mut` 函数中 `this` 的限制
- `this` **不能被** Lambda 或嵌套函数捕获
- `this` **不能作为表达式使用**（如返回值）
- 实例成员变量**不能被** `mut` 函数内的 Lambda 捕获

### 3.7 接口中的 `mut`
- 接口函数可声明为 `mut`
- **结构体**实现接口时须**精确匹配** `mut` 修饰符（mut↔mut, 非mut↔非mut）
- **类**实现接口时**忽略** `mut`（直接使用普通 `func`）
- 将结构体实例赋给接口类型变量时会**复制**。通过接口变量调用 `mut` 函数修改的是副本，**不影响**原始结构体

### 3.8 `mut` 函数使用限制

#### 规则 1：`let` 声明的结构体变量不能调用 `mut` 函数
```cangjie
let a = Foo()
a.f()    // 错误：a 是 let 声明的结构体
var b = Foo()
b.f()    // 正确：b 是 var
let c: I = Foo()
c.f()    // 正确：c 是接口类型，非结构体类型
```

#### 规则 2：结构体类型变量上的 `mut` 函数不能作为一等公民使用
```cangjie
var a = Foo()
var fn = a.f    // 错误：不能将 mut 函数作为一等公民使用
var b: I = Foo()
fn = b.f        // 正确：b 是接口类型
```

#### 规则 3：非 `mut` 实例成员函数不能调用 `mut` 函数；`mut` 函数**可以**调用非 `mut` 函数
```cangjie
struct Foo {
    var i = 0
    public mut func f(): Unit {
        i += 1
        g()     // 正确：mut 可调用非 mut
    }
    public func g(): Unit {
        f()     // 错误：非 mut 不能调用 mut
    }
}
```
