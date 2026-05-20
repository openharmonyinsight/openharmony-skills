---
name: cangjie-pattern-match
description: 仓颉语言模式匹配。当需要了解 match
  表达式、模式类型（常量/通配符/绑定/元组/类型/枚举）、模式嵌套、模式守卫(where)、穷举性、模式可反驳性、if-let 条件匹配、while-let
  循环匹配、模式在变量定义和 for-in 中的使用等特性时，应使用此 Skill
descriptionZH: 仓颉语言模式匹配。当需要了解 match
  表达式、模式类型（常量/通配符/绑定/元组/类型/枚举）、模式嵌套、模式守卫(where)、穷举性、模式可反驳性、if-let 条件匹配、while-let
  循环匹配、模式在变量定义和 for-in 中的使用等特性时，应使用此 Skill
tags:
  - 仓颉
  - 模式匹配
---

# 仓颉语言模式匹配 Skill

## 1. match 表达式

### 1.1 有匹配值的 match

```cangjie
match (expr) {
    case pattern1 => exprs // 不需要用 {} 包裹
    case pattern2 => exprs // 不需要用 {} 包裹
    case _ => exprs // 不需要用 {} 包裹
}
```

**规则：**
- `=>` 后是 **exprs**（1~N 个表达式），多个时各占一行，**不需要用 `{}` 包裹**
- 每个 case 分支的值与类型由 exprs 最后一个表达式决定，运行时匹配并执行的那个 case 分支值就是 match 表达式的值
- 变量/函数作用域从定义处到下一个 `case` 前结束
- 可用 `|` 连接多个同类模式
- 按**从上到下**顺序匹配，首个匹配执行后退出（**无穿透**）
- 须**穷举**所有可能值，否则编译错误，常用 `_` 兜底
- 非穷举枚举（`...` 构造器）须用 `_` 或绑定模式覆盖（详见 `cangjie-enum` Skill）

```cangjie
main() {
    let opt: ?Int64 = 42 // Option<Int64>，枚举类型
    let result = match (opt) {
        case Some(x) => // 枚举模式
            let doubled = x * 2
            println("doubled = ${doubled}")
            doubled   // 所执行分支最后一个表达式的值，就是 match 表达式的值
        case None => 0
    }
    println(result)  // 84
}
```

```cangjie
// ❌ 错误：case 分支不使用 {} 包裹
// match (x) {
//     case 1 => { println("one"); 1 }
// }

// ✅ 正确：直接写多行表达式
match (x) {
    case 1 =>
        println("one")
        1
    case _ => 0
}
```

### 1.2 无匹配值的 match

每个 `case` 接受 `Bool` 表达式（非模式），`_` 表示 `true`，不支持模式守卫：

```cangjie
let x = -1
match {
    case x > 0 => print("positive")
    case x < 0 => print("negative")  // 匹配
    case _ => print("zero")
}
```

### 1.3 模式守卫（`where`）

模式后添加 `where condition`（`Bool` 类型），case 仅在模式匹配**且**守卫为 `true` 时匹配。**注意**：仓颉使用 `where`，而非 `if`：

```cangjie
enum RGBColor {
    | Red(Int16) | Green(Int16) | Blue(Int16)
}

main() {
    let c = RGBColor.Green(-100)
    let cs = match (c) {
        case Green(g) where g < 0 => "Green = 0"  // 匹配
        case Green(g) => "Green = ${g}"
        case Red(r) where r < 0 => "Red = 0"
        case Red(r) => "Red = ${r}"
        case Blue(b) where b < 0 => "Blue = 0"
        case Blue(b) => "Blue = ${b}"
    }
    println(cs)  // Green = 0
}
```

### 1.4 match 表达式类型

- **有上下文类型**：每个分支体须为期望类型的子类型
- **无上下文类型**：类型为所有分支体的**最小公共父类型**
- **值未使用**：类型为 `Unit`，无公共父类型要求

---

## 2. 模式类型

### 2.1 常量模式
- 整数、浮点、字符、布尔、字符串字面量（无插值）和 `Unit` 字面量
- 须与匹配目标**同类型**，值相等时匹配
- 多个常量可用 `|` 组合
- `Rune` 值可用 `Rune` 字面量或单字符字符串字面量匹配
- `Byte` 值可用 ASCII 字符串字面量匹配

```cangjie
let score = 80
let level = match (score) {
    case 0 | 10 | 20 | 30 | 40 | 50 => "D"
    case 60 => "C"
    case 70 | 80 => "B"
    case 90 | 100 => "A"
    case _ => "invalid"
}
println(level) // B
```

### 2.2 通配符模式（`_`）
匹配**任意值**，通常用作最后一个 case 兜底。

### 2.3 绑定模式（`id`）
- 匹配任意值并**绑定**到不可变变量 `id`，作用域到该 case 结束
- **不能与 `|`** 连接使用；若 `id` 是枚举构造器名则视为枚举模式

```cangjie
match (x) {
    case 0 => "zero"
    case n => "x = ${n}"  // n 绑定 x 的值
}
```

### 2.4 元组模式
`(p_1, p_2, ..., p_n)`（`n ≥ 2`），每个位置匹配时整体匹配。同一模式内不允许重复绑定名。

```cangjie
match (("Alice", 24)) {
    case ("Bob", age) => "Bob is ${age}"
    case ("Alice", age) => "Alice is ${age}"  // 匹配
    case (_, _) => "someone"
}
```

### 2.5 类型模式
`_: Type`（无绑定）或 `id: Type`（有绑定），检查运行时类型是否为 `Type` 的子类型，匹配时转换并可选绑定。

```cangjie
open class Base {
    var a: Int64
    public init() { a = 10 }
}
class Derived <: Base {
    public init() { a = 20 }
}

match (Derived()) {
    case b: Base => b.a    // 匹配：Derived 是 Base 子类型，r = 20
    case _ => 0
}
```

### 2.6 枚举模式
- `C`（无参）或 `C(p_1, ..., p_n)`（有参），类型前缀可省略
- 构造器名匹配且嵌套模式匹配时整体匹配
- 须覆盖所有构造器或用 `_`；含绑定变量时不能用 `|`

```cangjie
enum TimeUnit {
    | Year(UInt64) | Month(UInt64)
}

match (Year(2)) {
    case Year(n) => "${n * 12} months"   // 匹配
    case Month(n) => "${n} months"
}
```

### 2.7 模式嵌套
元组和枚举模式可**任意深度嵌套**：

```cangjie
enum TimeUnit { | Year(UInt64) | Month(UInt64) }
enum Command  { | SetTimeUnit(TimeUnit) | Quit }

match ((SetTimeUnit(Year(2024)), true)) {
    case (SetTimeUnit(Year(y)), true) => println("year ${y}")  // 匹配
    case _ => ()
}
```

---

## 3. 模式可反驳性

| 模式 | 可反驳性 | 规则 |
|------|----------|------|
| 常量 | 始终**可反驳** | 可能不匹配 |
| 通配符 `_` | 始终**不可反驳** | 总匹配 |
| 绑定 `id` | 始终**不可反驳** | 总匹配 |
| 类型 `id: Type` | 始终**可反驳** | 运行时类型可能不匹配 |
| 元组 `(p1,...,pn)` | **所有** pi 不可反驳时不可反驳 | 一个可反驳 → 整体可反驳 |
| 枚举 `C(p1,...,pn)` | 仅一个有参构造器**且**所有 pi 不可反驳时不可反驳 | 多构造器 → 始终可反驳 |

---

## 4. 其他模式匹配语法/场景

### 4.1 变量定义与 for-in

```cangjie
let (x, y) = (100, 200) // 元组解构
for ((i, j) in [(1, 2), (3, 4)]) { println(i + j) } // for-in 元组解构
```

**适用于不可反驳模式**

### 4.2 if-let 条件匹配

在 `if` 条件中使用 `let pattern <- expression` 语法糖，匹配成功进入 `if` 分支，绑定变量**仅在 `if` 分支内可用**。`<-` 右侧表达式优先级不能低于 `..`，必要时用 `()` 包裹。

#### 基本用法

```cangjie
enum Msg {
    | Text(String) | Quit
}

main() {
    let m: Msg = Text("hello")
    if (let Text(s) <- m) {
        println(s)           // hello
    } else {
        println("not text")
    }
}
```

#### 多条件组合（`&&`）

`&&` 可连接多个 `let` 模式或与布尔表达式混合，前面绑定的变量可在后续条件中使用：

```cangjie
enum Expr {
    | Num(Int64) | Error
}

main() {
    let a = Num(42)
    let b = Num(10)

    // 两个 let 模式同时匹配
    if (let Num(x) <- a && let Num(y) <- b) {
        println("sum = ${x + y}")  // sum = 52
    }

    // let 模式 + 布尔条件
    if (let Num(n) <- a && n > 0) {
        println("positive: ${n}")  // positive: 42
    }
}
```

#### 或条件（`||`）

`||` 连接时，模式中**不能有变量绑定**，只能使用通配符 `_`：

```cangjie
let a = Num(1)
let b: Expr = Error
if (let Num(_) <- a || let Num(_) <- b) {
    println("至少一个是 Num")  // 匹配
}
```

#### 限制与常见错误

- `||` 连接的模式不能绑定变量
- `&&` 右侧须为 `let pattern` 或 `Bool` 表达式
- 绑定变量不能在绑定它的 `let` 左侧使用
- 绑定变量不能在 `else` 分支使用
- 条件中使用 `&&` 做额外检查，**不用 `where`**（`where` 仅用于 match 模式守卫）

```cangjie
// ❌ 错误示例
// if (let Num(a) <- x || a > 1) {}     // || 连接的模式不能绑定变量
// if (a > 3 && let Num(a) <- x) {}     // a 在绑定前使用
// if (let Num(a) <- x where a > 3) {}  // 应使用 && 而非 where
// if (let Num(a) <- x && a > 0) {
//     println(a)
// } else {
//     println(a)  // ❌ a 不能在 else 分支使用
// }
```

### 4.3 while-let 循环匹配

在 `while` 条件中使用 `let pattern <- expression`，匹配成功时执行循环体，失败时退出循环。条件规则与 if-let 相同。

```cangjie
enum State {
    | Active(Int64) | Done
}

main() {
    var s: State = Active(1)
    while (let Active(n) <- s) {
        println(n)
        s = if (n < 3) { Active(n + 1) } else { Done }
    }
    // 输出：1 2 3
}
```

等价的 match 解糖形态：
```cangjie
while (true) {
    match (s) {
        case Active(n) =>
            println(n)
            s = if (n < 3) { Active(n + 1) } else { Done }
        case _ => break
    }
}
```

---

## 5. 完整可运行示例

```cangjie
enum Shape {
    | Circle(Float64)
    | Rect(Float64, Float64)
    | Triangle(Float64, Float64)
}

main() {
    let shapes = [Circle(5.0), Rect(3.0, 4.0), Triangle(3.0, 6.0)]

    for (shape in shapes) {
        let area = match (shape) {
            case Circle(r) => 3.14159 * r * r
            case Rect(w, h) => w * h
            case Triangle(b, h) => b * h / 2.0
        }
        match {
            case area > 50.0 => println("Large: ${area}")
            case area > 10.0 => println("Medium: ${area}")
            case _ => println("Small: ${area}")
        }
    }
}
