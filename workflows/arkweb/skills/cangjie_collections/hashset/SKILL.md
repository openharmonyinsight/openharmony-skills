---
name: cangjie-collections-hashset
description: "仓颉 HashSet 类型用法。"
---

# 仓颉标准库 HashSet

## 1. 概述

`HashSet<T>` 是 `std.collection` 包中用 **class** 实现的哈希集合，使用前需导入：

```cangjie
import std.collection.*
```

- **哈希表实现** — 基于 HashMap 实现，平均 O(1) 的插入、删除、查找
- **引用类型** — `let set2 = set1` 后两者共享数据，修改互相可见
- **无序** — 不保证元素的遍历顺序
- **元素唯一** — 不允许重复元素，添加已有元素时无效果
- 实现接口：`Set<T>`
- **约束**：`T` 必须实现 `Hashable` 和 `Equatable<T>`

---

## 2. 构造

```cangjie
import std.collection.*

// 空 HashSet（默认容量 16）
let set = HashSet<String>()

// 指定初始容量
let set2 = HashSet<String>(100)

// 从数组构造
let set3 = HashSet<Int64>([0, 1, 2])

// 从集合构造
let set4 = HashSet<Int64>(otherCollection)

// 指定大小 + 初始化函数
let set5 = HashSet<Int64>(5, {i => i * i})
// {0, 1, 4, 9, 16}
```

### 构造函数签名

| 构造函数 | 说明 |
|----------|------|
| `init()` | 空 HashSet，默认容量 16 |
| `init(capacity: Int64)` | 空 HashSet，指定容量。`capacity < 0` 抛 `IllegalArgumentException` |
| `init(elements: Array<T>)` | 从数组构造，重复元素自动去重 |
| `init(elements: Collection<T>)` | 从集合构造，重复元素自动去重 |
| `init(size: Int64, initElement: (Int64) -> T)` | 指定大小 + 初始化函数。`size < 0` 抛 `IllegalArgumentException` |

---

## 3. 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `size` | `Int64` | 元素个数 |
| `capacity` | `Int64` | 当前内部容量（不一定等于 size） |

```cangjie
let set = HashSet<Int64>([1, 2, 3])
println(set.size)      // 3
println(set.capacity)  // >= 3
```

---

## 4. 添加元素

### 4.1 `add` — 添加单个元素

```cangjie
func add(element: T): Bool
```

- 元素不存在：添加成功，返回 `true`
- 元素已存在：不添加，返回 `false`

```cangjie
let set = HashSet<String>()
set.add("apple")    // true（新增）
set.add("banana")   // true（新增）
set.add("apple")    // false（已存在，不添加）
println(set.size)   // 2
```

### 4.2 `add` — 批量添加

```cangjie
func add(all!: Collection<T>): Unit
```

```cangjie
set.add(all: ["orange", "peach"])
set.add(all: otherSet)
```

- 已存在的元素不会被重复添加

---

## 5. 查询

### 5.1 `contains` — 元素是否存在

```cangjie
func contains(element: T): Bool
func contains(all!: Collection<T>): Bool
```

```cangjie
let set = HashSet<String>(["apple", "banana", "orange"])
set.contains("apple")                    // true
set.contains("grape")                    // false
set.contains(all: ["apple", "banana"])  // true
set.contains(all: ["apple", "grape"])   // false（grape 不存在）
```

### 5.2 `toArray` — 转为数组

```cangjie
func toArray(): Array<T>
```

```cangjie
let set = HashSet<Int64>([1, 2, 3])
let arr = set.toArray()  // [1, 2, 3]（顺序不保证）
```

### 5.3 无下标访问

HashSet 是无序集合，**不支持下标访问**（无索引概念）。

---

## 6. 删除

### 6.1 按元素删除

```cangjie
func remove(element: T): Bool
```

- 元素存在：移除成功，返回 `true`
- 元素不存在：返回 `false`

```cangjie
let set = HashSet<String>(["apple", "banana", "orange"])
set.remove("apple")   // true
set.remove("grape")   // false（不存在）
```

### 6.2 批量删除

```cangjie
func remove(all!: Collection<T>): Unit
```

```cangjie
set.remove(all: ["banana", "orange"])
```

### 6.3 条件删除

```cangjie
func removeIf(predicate: (T) -> Bool): Unit
```

```cangjie
let set = HashSet<Int64>([1, 2, 3, 4, 5, 6])
set.removeIf { v => v % 2 == 0 }  // 删除偶数 → {1, 3, 5}
```

- 在 `predicate` 中修改 HashSet 会抛 `ConcurrentModificationException`

### 6.4 清空

```cangjie
func clear(): Unit
```

```cangjie
set.clear()  // size = 0
```

---

## 7. 集合运算

HashSet 支持集合的交集、并集、差集运算，返回新的 HashSet。

### 7.1 交集 `&`

```cangjie
operator func &(other: ReadOnlySet<T>): HashSet<T>
```

```cangjie
let a = HashSet<Int64>([1, 2, 3, 4])
let b = HashSet<Int64>([3, 4, 5, 6])
let intersection = a & b  // {3, 4}
```

### 7.2 并集 `|`

```cangjie
operator func |(other: ReadOnlySet<T>): HashSet<T>
```

```cangjie
let a = HashSet<Int64>([1, 2, 3])
let b = HashSet<Int64>([3, 4, 5])
let union = a | b  // {1, 2, 3, 4, 5}
```

### 7.3 差集 `-`

```cangjie
operator func -(other: ReadOnlySet<T>): HashSet<T>
```

```cangjie
let a = HashSet<Int64>([1, 2, 3, 4])
let b = HashSet<Int64>([3, 4, 5, 6])
let diff = a - b  // {1, 2}
```

### 7.4 子集判断

```cangjie
func subsetOf(other: ReadOnlySet<T>): Bool
```

```cangjie
let a = HashSet<Int64>([1, 2])
let b = HashSet<Int64>([1, 2, 3, 4])
a.subsetOf(b)  // true
b.subsetOf(a)  // false
```

### 7.5 保留交集元素 `retain`

```cangjie
func retain(all!: Set<T>): Unit
```

```cangjie
let a = HashSet<Int64>([1, 2, 3, 4])
let b = HashSet<Int64>([2, 4, 6])
a.retain(all: b)  // a = {2, 4}（原地修改）
```

---

## 8. 遍历

```cangjie
func iterator(): Iterator<T>
```

```cangjie
let set = HashSet<String>(["apple", "banana", "orange"])

// for-in 遍历（推荐）
for (item in set) {
    println(item)
}
```

> **注意**：遍历顺序不保证。

---

## 9. 容量管理

```cangjie
func reserve(additional: Int64): Unit
```

```cangjie
set.reserve(100)  // 扩容以容纳更多元素
```

- `additional <= 0` 或剩余容量足够时不执行扩容
- 扩容后容量约为原来的 1.5 倍（不保证精确值）
- 当溢出 `Int64.Max` 时抛 `OverflowException`

---

## 10. 判空

```cangjie
func isEmpty(): Bool
```

```cangjie
HashSet<String>().isEmpty()  // true
```

---

## 11. 拷贝

```cangjie
func clone(): HashSet<T>
```

```cangjie
let set = HashSet<Int64>([1, 2, 3])
let copy = set.clone()
copy.add(4)
println(set.size)  // 3（不受影响）
```

---

## 12. 相等比较

```cangjie
let a = HashSet<Int64>([1, 2, 3])
let b = HashSet<Int64>([3, 2, 1])
let c = HashSet<Int64>([1, 2, 4])

a == b  // true（元素完全相同，不关心顺序）
a != c  // true
```

---

## 13. 转为字符串（需要 T <: ToString）

```cangjie
func toString(): String
```

```cangjie
HashSet<Int64>([1, 2, 3]).toString()
// "[1, 2, 3]"（顺序不保证）
```

---

## 14. 常见用法总结

```cangjie
import std.collection.*

// 1. 去重
let nums = [1, 2, 2, 3, 3, 3]
let unique = HashSet<Int64>(nums)  // {1, 2, 3}

// 2. 成员检查
let allowedUsers = HashSet<String>(["alice", "bob", "charlie"])
if (allowedUsers.contains(username)) {
    grant()
}

// 3. 集合运算
let frontendSkills = HashSet<String>(["HTML", "CSS", "JavaScript"])
let backendSkills = HashSet<String>(["Java", "SQL", "JavaScript"])
let common = frontendSkills & backendSkills    // {"JavaScript"}
let allSkills = frontendSkills | backendSkills  // {"HTML", "CSS", "JavaScript", "Java", "SQL"}
let onlyFrontend = frontendSkills - backendSkills  // {"HTML", "CSS"}

// 4. 条件过滤
let scores = HashSet<Int64>([55, 60, 75, 80, 95])
scores.removeIf { s => s < 60 }  // 删除不及格的分数

// 5. 批量添加与删除
let set = HashSet<String>()
set.add(all: ["a", "b", "c"])
set.remove(all: ["a", "c"])  // {"b"}

// 6. 子集判断
let required = HashSet<String>(["read", "write"])
let granted = HashSet<String>(["read", "write", "execute"])
if (required.subsetOf(granted)) {
    allow()
}

// 7. 遍历
for (item in set) {
    println(item)
}

// 8. 转为数组
let arr = set.toArray()
```

---

## 15. 注意事项

| 要点 | 说明 |
|------|------|
| **元素的要求** | `T` 必须实现 `Hashable` + `Equatable<T>`。常见可用类型：`String`、`Int64`、所有整数类型、`Bool`、`Rune` 等 |
| **线程安全** | `HashSet` **非线程安全**。多线程场景需自行加锁保护 |
| **无下标访问** | HashSet 无序，不支持索引访问。需要按索引访问请先 `toArray()` |
| **遍历顺序** | 不保证顺序 |
| **元素不可修改** | 元素一旦存入不可修改（无下标赋值） |
| **性能** | 基于 HashMap 实现，平均 O(1) 查找/插入/删除 |
| **集合运算** | 支持 `&`（交集）、`|`（并集）、`-`（差集）运算符，返回新 HashSet |
