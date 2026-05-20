---
name: cangjie-collections-arraylist
description: "仓颉 ArrayList 类型用法。"
---

# 仓颉标准库 ArrayList 类型 Skill

## 1. 概述

`ArrayList<T>` 是 `std.collection` 包中的 **class** 类型，使用前需导入：

```cangjie
import std.collection.*
```

- **动态数组** — 可自动扩容，无需预先指定大小
- **引用类型** — `let list2 = list1` 后两者共享数据，修改互相可见
- 实现接口：`List<T>`（继承 `Collection<T>`、`Iterable<T>`）
- `T` 可以是任意类型

---

## 2. 构造

```cangjie
import std.collection.*

// 空 ArrayList（默认容量 16）
let list = ArrayList<Int64>()

// 指定初始容量
let list2 = ArrayList<Int64>(100)

// 从 Array 字面量构造
let list3 = ArrayList<Int64>([1, 2, 3])

// 从其他 Collection 构造
let list4 = ArrayList<Int64>(otherCollection)

// 指定大小 + 初始化函数
let list5 = ArrayList<Int64>(5, {i => i * 10})  // [0, 10, 20, 30, 40]

// 使用 of 静态方法（支持变长参数语法）
let list6 = ArrayList.of(1, 2, 3)
```

### 构造函数签名

| 构造函数 | 说明 |
|----------|------|
| `init()` | 空 ArrayList，默认容量 16 |
| `init(capacity: Int64)` | 空 ArrayList，指定容量。`capacity < 0` 抛 `IllegalArgumentException` |
| `init(elements: Collection<T>)` | 包含指定集合所有元素 |
| `init(size: Int64, initElement: (Int64) -> T)` | 指定大小 + 初始化函数。`size < 0` 抛 `IllegalArgumentException` |
| `static func of(elements: Array<T>): ArrayList<T>` | 从数组创建 |

---

## 3. 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `size` | `Int64` | 元素个数 |
| `capacity` | `Int64` | 当前容量 |
| `first` | `?T` | 首元素，空时为 `None` |
| `last` | `?T` | 尾元素，空时为 `None` |

```cangjie
let list = ArrayList<Int64>([10, 20, 30])
println(list.size)      // 3
println(list.capacity)  // >= 3
println(list.first)     // Some(10)
println(list.last)      // Some(30)
```

---

## 4. 元素访问

### 4.1 下标访问

```cangjie
let list = ArrayList<Int64>([10, 20, 30])
let v = list[0]    // 10
list[1] = 99       // [10, 99, 30]
```

- 索引从 `0` 开始，类型为 `Int64`
- 越界抛出 `IndexOutOfBoundsException`

### 4.2 安全访问 `get`

```cangjie
func get(index: Int64): ?T
```

```cangjie
list.get(1)   // Some(99)
list.get(10)  // None（不抛异常）
```

### 4.3 范围下标（切片）

```cangjie
let list = ArrayList<Int64>([0, 1, 2, 3, 4])
let sub = list[1..4]  // ArrayList [1, 2, 3]
```

---

## 5. 添加元素

### 5.1 尾部追加

```cangjie
func add(element: T): Unit
func add(all!: Collection<T>): Unit
```

```cangjie
let list = ArrayList<Int64>()
list.add(1)                          // [1]
list.add(2)                          // [1, 2]
list.add(all: [3, 4, 5])            // [1, 2, 3, 4, 5]
list.add(all: otherArrayList)        // 追加另一个集合的元素
```

### 5.2 在指定位置插入

```cangjie
func add(element: T, at!: Int64): Unit
func add(all!: Collection<T>, at!: Int64): Unit
```

```cangjie
let list = ArrayList<Int64>([1, 2, 3])
list.add(99, at: 1)                  // [1, 99, 2, 3]
list.add(all: [77, 88], at: 0)      // [77, 88, 1, 99, 2, 3]
```

- `at` 越界抛出 `IndexOutOfBoundsException`

---

## 6. 删除元素

### 6.1 按索引删除

```cangjie
func remove(at!: Int64): T
```

```cangjie
let list = ArrayList<Int64>([10, 20, 30, 40])
let removed = list.remove(at: 1)  // removed = 20, list = [10, 30, 40]
```

- 越界抛出 `IndexOutOfBoundsException`

### 6.2 按范围删除

```cangjie
func remove(range: Range<Int64>): Unit
```

```cangjie
let list = ArrayList<Int64>([0, 1, 2, 3, 4])
list.remove(1..3)  // [0, 3, 4]
```

- `range.step` 必须为 1，否则抛 `IllegalArgumentException`

### 6.3 按条件删除

```cangjie
func removeIf(predicate: (T) -> Bool): Unit
```

```cangjie
let list = ArrayList<Int64>([1, 2, 3, 4, 5, 6])
list.removeIf { v => v % 2 == 0 }  // [1, 3, 5]
```

- 在 `predicate` 中修改 ArrayList 会抛 `ConcurrentModificationException`

### 6.4 清空

```cangjie
func clear(): Unit
```

```cangjie
list.clear()  // size = 0
```

---

## 7. 容量管理

ArrayList 在元素超过容量时会自动扩容（重新分配内存 + 复制元素），频繁扩容会影响性能。

### 7.1 构造时预分配

```cangjie
let list = ArrayList<Int64>(1000)  // 预分配容量 1000
```

### 7.2 运行时扩容

```cangjie
func reserve(additional: Int64): Unit
```

```cangjie
list.reserve(500)  // 额外增加 500 的容量
```

- 当 `additional + 已使用容量` 超过 `Int64.Max` 时抛 `OverflowException`

---

## 8. 切片

```cangjie
func slice(range: Range<Int64>): ArrayList<T>
```

```cangjie
let list = ArrayList<Int64>([0, 1, 2, 3, 4])
let sub = list.slice(1..=3)  // [1, 2, 3]（新 ArrayList）
```

- `range.step` 必须为 1，否则抛 `IllegalArgumentException`
- 越界抛 `IndexOutOfBoundsException`

---

## 9. 反转

```cangjie
func reverse(): Unit
```

```cangjie
let list = ArrayList<Int64>([1, 2, 3])
list.reverse()  // [3, 2, 1]
```

---

## 10. 拷贝

```cangjie
func clone(): ArrayList<T>
```

```cangjie
let list = ArrayList<Int64>([1, 2, 3])
let copy = list.clone()
copy[0] = 999
println(list[0])  // 1（不受影响，浅拷贝但各自独立存储）
```

---

## 11. 转换

### 11.1 转为 Array

```cangjie
func toArray(): Array<T>
```

```cangjie
let list = ArrayList<Int64>([1, 2, 3])
let arr: Array<Int64> = list.toArray()  // [1, 2, 3]
```

### 11.2 转为字符串（需要 T <: ToString）

```cangjie
func toString(): String
```

```cangjie
ArrayList<Int64>([1, 2, 3]).toString()  // "[1, 2, 3]"
```

---

## 12. 判空与包含

```cangjie
func isEmpty(): Bool
```

```cangjie
ArrayList<Int64>().isEmpty()  // true
```

### 12.1 `contains`（需要 T <: Equatable<T>）

```cangjie
func contains(element: T): Bool
```

```cangjie
let list = ArrayList<Int64>([1, 2, 3])
list.contains(2)  // true
list.contains(5)  // false
```

---

## 13. 相等比较（需要 T <: Equatable<T>）

```cangjie
let a = ArrayList<Int64>([1, 2, 3])
let b = ArrayList<Int64>([1, 2, 3])
let c = ArrayList<Int64>([1, 2, 4])
a == b  // true
a != c  // true
```

---

## 14. 迭代

```cangjie
func iterator(): Iterator<T>
```

```cangjie
import std.collection.*

let list = ArrayList<String>(["a", "b", "c"])

// for-in 遍历
for (item in list) {
    println(item)
}

// 函数式操作（通过迭代器）
let result = list
    |> filter { s => s != "b" }
    |> map { s => s.toAsciiUpper() }
    |> collectArrayList
// result = ["A", "C"]
```

---

## 15. 排序

### 15.1 使用 std.sort（推荐）

```cangjie
import std.sort.*
import std.collection.*

let list = ArrayList<Int64>([3, 1, 4, 1, 5])
sort(list)  // [1, 1, 3, 4, 5]
```

### 15.2 内置排序方法（已废弃）

```cangjie
// 以下方法已废弃，建议使用 std.sort
list.sort()                                          // 升序（T 须 <: Comparable）
list.sortDescending()                                // 降序
list.sortBy(comparator: { a, b => b - a })          // 自定义比较器
list.sortBy(stable: true, comparator: { a, b => a - b }) // 稳定排序
```

---

## 16. 常见用法总结

```cangjie
import std.collection.*

// 1. 动态收集元素
let results = ArrayList<String>()
for (item in source) {
    if (isValid(item)) {
        results.add(item.toString())
    }
}

// 2. 批量添加
let list = ArrayList<Int64>()
list.add(all: [1, 2, 3])
list.add(all: moreItems)

// 3. 安全访问
if (let Some(v) <- list.get(index)) {
    process(v)
}

// 4. 条件过滤删除
list.removeIf { v => v < 0 }

// 5. 从 Array 创建 → 操作 → 转回 Array
let arr = [3, 1, 2]
let list = ArrayList<Int64>(arr)
sort(list)
let sorted = list.toArray()  // [1, 2, 3]

// 6. 遍历并修改
for (i in 0..list.size) {
    list[i] = list[i] * 2
}

// 7. 预分配避免扩容开销
let bigList = ArrayList<Int64>(10000)
for (i in 0..10000) {
    bigList.add(i)
}
```
