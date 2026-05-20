---
name: cangjie-for
description: 仓颉语言 for-in 迭代。当需要了解 for-in 循环语法、Iterable/Iterator 接口、Range
  区间类型、迭代控制（break/continue/where）、元组解构、自定义迭代器、迭代最优实践等特性时，应使用此 Skill。
descriptionZH: 仓颉语言 for-in 迭代。当需要了解 for-in 循环语法、Iterable/Iterator 接口、Range
  区间类型、迭代控制（break/continue/where）、元组解构、自定义迭代器、迭代最优实践等特性时，应使用此 Skill。
tags:
  - 仓颉
  - 迭代
---

# 仓颉语言 for-in 迭代 Skill

## 1. for-in 基本语法

### 1.1 语法
```cangjie
for (item in sequence) {
    exprs
}
```
- `sequence` 须实现 `Iterable<T>` 接口
- `sequence` 表达式**仅在首次迭代前求值一次**
- 循环表达式类型为 `Unit`，值为 `()`

### 1.2 执行流程
1. 求值 `sequence`，调用 `iterator()` 获取迭代器
2. 调用迭代器 `next()`：返回 `None` 则退出循环，返回 `Some(value)` 则继续
3. 将 `value` 绑定到 `item`，执行循环体
4. 回到步骤 2

### 1.3 迭代变量规则
- 迭代变量 `item` **不可变**（`let` 绑定），不能在循环体中重新赋值
- 若循环体中不使用迭代变量，可用通配符 `_` 占位避免警告：
  ```cangjie
  for (_ in 0..3) {
      println("hello")
  }
  ```

---

## 2. Range 区间类型

### 2.1 区间字面量
- **半开区间**（左闭右开）：`start..end` — 不包含 `end`
- **闭区间**（左闭右闭）：`start..=end` — 包含 `end`
- 可选步长 `: step`，省略时默认为 1；**step 不能为 0**
```cangjie
for (i in 0..5) { print(i) }      // 输出：01234
for (i in 0..=5) { print(i) }     // 输出：012345
for (i in 0..10 : 2) { print(i) } // 输出：02468
```

### 2.2 逆向与步长
- 负步长实现逆序迭代：
```cangjie
for (i in 5..0 : -1) { print(i) }  // 输出：54321
for (i in 10..0 : -3) { print(i) } // 输出：10741
```

### 2.3 空区间
- `step > 0 && start >= end`（半开）或 `step > 0 && start > end`（闭）→ 空区间，循环体不执行
- `step < 0 && start <= end`（半开）或 `step < 0 && start < end`（闭）→ 空区间

### 2.4 Range 类型签名
```cangjie
public struct Range<T> <: Iterable<T> where T <: Countable<T> & Comparable<T> & Equatable<T>
```
- `start: T`、`end: T`、`step: Int64`
- `isEmpty()` 判断是否为空；`iterator()` 返回迭代器

---

## 3. Iterable 与 Iterator 接口

### 3.1 接口定义
```cangjie
interface Iterable<T> {
    func iterator(): Iterator<T>
}

interface Iterator<T> <: Iterable<T> {
    mut func next(): Option<T>
}
```
- `Iterator` 自身扩展 `Iterable`，可直接用于 for-in
- `next()` 返回 `Some(value)` 表示有元素，`None` 表示迭代结束

### 3.2 for-in 脱糖
```cangjie
for (i in list) { println(i) }
```
等价于：
```cangjie
var it = list.iterator()
while (let Some(i) <- it.next()) {
    println(i)
}
```

### 3.3 已实现 Iterable 的内置类型
| 类型 | 元素类型 | 有序 |
|------|---------|:---:|
| `Range<T>` | `T` | ✅ |
| `Array<T>` | `T` | ✅ |
| `ArrayList<T>` | `T` | ✅ |
| `String` | `Rune` | ✅ |
| `HashMap<K, V>` | `(K, V)` | ❌ |
| `HashSet<T>` | `T` | ❌ |

---

## 4. 迭代进阶

### 4.1 元组解构
- 对元素为元组的集合，可直接解构：
```cangjie
let points = [(1, 2), (3, 4), (5, 6)]
for ((x, y) in points) {
    println("x=${x}, y=${y}")
}
```
- HashMap 迭代天然使用元组解构：
```cangjie
import std.collection.*

main() {
    let map = HashMap<String, Int64>([("a", 1), ("b", 2)])
    for ((key, value) in map) {
        println("${key}: ${value}")
    }
}
```

### 4.2 where 子句过滤
- `where` 在循环体执行前过滤，比循环体内 `if` 更简洁：
```cangjie
// ✅ 推荐：where 过滤
for (i in 0..20 where i % 3 == 0) {
    println(i)  // 0, 3, 6, 9, 12, 15, 18
}

// ❌ 不推荐：循环体内 if 判断
for (i in 0..20) {
    if (i % 3 == 0) {
        println(i)
    }
}
```

### 4.3 break / continue
- `break` 提前退出循环，`continue` 跳到下一次迭代
- 二者类型均为 `Nothing`
```cangjie
for (i in 0..100) {
    if (i > 5) { break }
    if (i % 2 == 0) { continue }
    println(i)  // 1, 3, 5
}
```

### 4.4 String 迭代

**注意** String 只实现了 `Iterable<Byte>`，**逐字节而不是逐字符**迭代：

```cangjie
for (ch in "Hi仓颉") {
    println(ch)  // 逐个输出：72 105 228 187 147 233 162 137
}
```

如果需要逐字符（Rune）迭代，可以先调用 `toRuneArray()` 转为字符数组后再使用：

```cangjie
for (ch in "Hi仓颉".toRuneArray()) {
    println(ch)  // 逐个输出：H i 仓 颉
}
```

---

## 5. 自定义可迭代类型

实现 `Iterable<T>` 接口即可获得 for-in 支持：

```cangjie
class Countdown <: Iterable<Int64> {
    let start: Int64
    init(start: Int64) { this.start = start }

    public func iterator(): Iterator<Int64> {
        CountdownIterator(start)
    }
}

class CountdownIterator <: Iterator<Int64> {
    var current: Int64
    init(start: Int64) { current = start }

    public func next(): Option<Int64> {
        if (current > 0) {
            let v = current
            current--
            return Some(v)
        }
        return None
    }
}

main() {
    for (i in Countdown(5)) {
        print("${i} ")  // 输出：5 4 3 2 1
    }
}
```

---

## 6. 最优实践

### 6.1 优先使用 for-in
- for-in 比手动 `while` + `iterator()` 更安全、简洁，且编译器可优化
- 需要索引时可结合 `enumerate()`（若集合支持），否则使用 Range：
  ```cangjie
  let arr = [10, 20, 30]
  for (i in 0..arr.size) {
      println("arr[${i}] = ${arr[i]}")
  }
  ```

### 6.2 Range 计数循环
- 固定次数循环优先用 Range，无需手动维护计数器：
  ```cangjie
  // ✅ 推荐
  for (_ in 0..n) { doSomething() }

  // ❌ 不推荐
  var i = 0
  while (i < n) { doSomething(); i++ }
  ```

### 6.3 where 替代 if
- 过滤场景优先用 `where` 子句，减少嵌套、提升可读性（见 4.2）

### 6.4 注意无序集合
- `HashMap` 和 `HashSet` 迭代顺序不确定，不应依赖遍历顺序

### 6.5 常见错误
```cangjie
// ❌ 错误：试图修改迭代变量
for (i in 0..5) {
    // i = i + 1  // 编译错误，迭代变量不可变
}

// ❌ 错误：step 为 0
// for (i in 0..10 : 0) { }  // 运行时错误

// ❌ 错误：半开区间边界混淆
for (i in 0..5) { print(i) }   // 01234，不包含 5
for (i in 0..=5) { print(i) }  // 012345，包含 5
```
