---
name: cangjie-option
description: 仓颉语言 Option 类型。当需要了解 Option<T> 定义与用法、?T 简写、自动包装、模式匹配解构、coalescing
  操作符(??)、问号操作符(?.)、getOrThrow()、if-let 条件解构、while-let 循环解构等特性时，应使用此 Skill
descriptionZH: 仓颉语言 Option 类型。当需要了解 Option<T> 定义与用法、?T 简写、自动包装、模式匹配解构、coalescing
  操作符(??)、问号操作符(?.)、getOrThrow()、if-let 条件解构、while-let 循环解构等特性时，应使用此 Skill
tags:
  - 仓颉
  - Option
---

# 仓颉语言 Option 类型 Skill

## 1. 定义

```cangjie
enum Option<T> {
    | Some(T)
    | None
}
```
- `Some(v)` 表示有值，`None` 表示无值
- `Option` 是泛型枚举，`T` 不同则 `Option` 类型不同（如 `Option<Int64>`、`Option<String>`）

---

## 2. 简写语法 `?T`

- `?Ty` 等价于 `Option<Ty>`
```cangjie
let a: ?Int64 = Some(100)     // 等价于 Option<Int64>
let b: ?String = None          // 等价于 Option<String>
```

---

## 3. 自动包装

当上下文期望 `Option<T>` 时，可直接传 `T` 类型的值，编译器自动用 `Some` 包装（**不是**类型转换）：
```cangjie
let a: Option<Int64> = 100     // 自动包装为 Some(100)
let b: ?Int64 = 100            // 同上
let c: Option<String> = "hi"   // 自动包装为 Some("hi")
```

---

## 4. 显式 `None<T>`

无上下文类型信息时，使用 `None<T>` 显式指定类型：
```cangjie
let a = None<Int64>   // a: Option<Int64>
let b = None<Bool>    // b: Option<Bool>
```

---

## 5. 解构方式

### 5.1 模式匹配（match）

使用 `match` 对 `Option` 值进行解构：
```cangjie
func getString(p: ?Int64): String {
    match (p) {
        case Some(x) => "${x}"
        case None => "none"
    }
}

main() {
    println(getString(Some(1)))       // "1"
    println(getString(None<Int64>))   // "none"
}
```

### 5.2 coalescing 操作符 `??`

`e1 ?? e2`：当 `e1` 为 `Some(v)` 时返回 `v`，否则返回 `e2`。`e2` 具有短路求值特性（`e1` 有值时不求值 `e2`）。
```cangjie
main() {
    let a = Some(1)
    let b: ?Int64 = None
    let r1: Int64 = a ?? 0   // 1
    let r2: Int64 = b ?? 0   // 0
    println("${r1}, ${r2}")   // "1, 0"
}
```

> **注意**：`??` 的优先级低于比较运算符，混合使用时需加括号，详见 `cangjie-basic-data-type` Skill。

### 5.3 问号操作符 `?.`

`?.` 用于安全地对 `Option` 值进行成员访问、函数调用或下标操作。当值为 `Some(v)` 时执行操作并用 `Some` 包装结果，为 `None` 时直接返回 `None`（短路，不求值后续表达式）。

```cangjie
struct R {
    public var a: Int64
    public init(a: Int64) {
        this.a = a
    }
}

main() {
    let x = Some(R(100))
    let y: ?R = None
    let r1 = x?.a   // Some(100)
    let r2 = y?.a   // None
}
```

支持多层链式访问，中间任何一级为 `None` 即短路返回 `None`：
```cangjie
class A {
    public var b: B = B()
}
class B {
    public var c: ?C = C()
}
class C {
    public var d: Int64 = 100
}

main() {
    let a = Some(A())
    let r1 = a?.b.c?.d   // Some(100)
}
```

### 5.4 `getOrThrow()`

`getOrThrow()` 解构 `?T` 表达式：值为 `Some(v)` 时返回 `v`，为 `None` 时抛出 `NoneValueException`。
```cangjie
main() {
    let a = Some(1)
    let r1 = a.getOrThrow()   // 1

    let b: ?Int64 = None
    try {
        let r2 = b.getOrThrow()
    } catch (e: NoneValueException) {
        println("b is None")   // 输出: b is None
    }
}
```

---

## 6. if-let 条件解构

在 `if` 条件中使用 `let` 模式匹配语法糖，成功匹配时进入 `if` 分支，绑定的变量**仅在** `if` 分支内可用。

### 6.1 基本用法

```cangjie
main() {
    let opt: ?Int64 = 42
    // print 42
    if (let Some(v) <- opt) {
        println(v)
    } else {
        println("invalid")
    }
}
```

### 6.2 多条件组合（`&&`）

用 `&&` 连接多个 `let` 模式或与布尔表达式混合：
```cangjie
main() {
    let a = Some(3)
    let d = Some(1)

    // 两个 let 模式同时匹配
    if (let Some(e) <- a && let Some(f) <- d) {
        println("${e} ${f}")   // 输出: 3 1
    }

    // let 模式 + 布尔条件
    if (let Some(f) <- d && f > 0) {
        println(f)   // 输出: 1
    }
}
```

### 6.3 或条件（`||`）

用 `||` 连接时，模式中**不能有变量绑定**，只能使用通配符 `_`
```cangjie
main() {
    let a: ?Int64 = Some(3)
    let d: ?Int64 = None

    if (let Some(_) <- a || let Some(_) <- d) {
        println("至少一个有值")
    }
}
```

---

## 7. while-let 循环解构

在 `while` 条件中使用 `let` 模式，常用于遍历迭代器：

```cangjie
main() {
    let list = [1, 2, 3]
    var it = list.iterator()
    while (let Some(i) <- it.next()) {
        println(i) // 逐行输出 1 2 3
    }
}
```

等价的 `match` 写法，也即是 while-let 语法糖解糖后的形态：
```cangjie
let list = [1, 2, 3]
var it = list.iterator()
while (true) {
    match (it.next()) {
        case Some(i) => println(i)
        case None => break
    }
}
```

---

## 8. 常见用法总结

| 场景 | 推荐方式 | 示例 |
|------|---------|------|
| 提供默认值 | `??` | `let name = getName() ?? "unknown"` |
| 安全访问成员 | `?.` | `let len = buffer?.size()` |
| 条件取值并使用 | `if-let` | `if (let Some(v) <- opt) { use(v) }` |
| 遍历迭代器 | `while-let` | `while (let Some(i) <- it.next()) { ... }` |
| 强制取值（确信有值） | `getOrThrow()` | `let v = opt.getOrThrow()` |
| 分支处理有值/无值 | `match` | `match (opt) { case Some(v) => ... case None => ... }` |

---

## 9. 完整可运行示例

```cangjie
func findUser(id: Int64): ?String {
    if (id == 1) {
        "Alice"       // 自动包装为 Some("Alice")
    } else {
        None
    }
}

func findAge(name: String): ?Int64 {
    if (name == "Alice") {
        30
    } else {
        None
    }
}

main() {
    // ?? 提供默认值
    let name = findUser(1) ?? "unknown"
    println("name = ${name}")   // name = Alice

    // if-let 条件解构
    if (let Some(user) <- findUser(1)) {
        println("找到用户: ${user}")   // 找到用户: Alice
    }

    // if-let + && 组合
    if (let Some(user) <- findUser(1) && let Some(age) <- findAge(user)) {
        println("${user} 年龄 ${age}")   // Alice 年龄 30
    }

    // while-let 遍历
    let ids = [1, 2, 3]
    var it = ids.iterator()
    while (let Some(id) <- it.next()) {
        let display = findUser(id) ?? "未知用户"
        println("id=${id}: ${display}")
    }
    // id=1: Alice
    // id=2: 未知用户
    // id=3: 未知用户

    // match 完整分支
    match (findUser(99)) {
        case Some(u) => println(u)
        case None => println("用户不存在")   // 用户不存在
    }

    // getOrThrow
    let sure = findUser(1).getOrThrow()
    println("sure = ${sure}")   // sure = Alice
}
```
