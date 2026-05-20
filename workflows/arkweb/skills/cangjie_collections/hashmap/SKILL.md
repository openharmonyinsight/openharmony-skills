---
name: cangjie-collections-hashmap
description: "仓颉 HashMap 类型用法。"
---

# 仓颉标准库 HashMap 类型 Skill

## 1. 概述

`HashMap<K, V>` 是 `std.collection` 包中的 **class** 类型，使用前需导入：

```cangjie
import std.collection.*
```

- **哈希表实现** — 平均 O(1) 的插入、删除、查找
- **引用类型** — `let map2 = map1` 后两者共享数据，修改互相可见
- **无序** — 不保证元素的遍历顺序
- 实现接口：`Map<K, V>`
- **约束**：`K` 必须实现 `Hashable` 和 `Equatable<K>`；`V` 无约束

---

## 2. 构造

```cangjie
import std.collection.*

// 空 HashMap（默认容量 16）
let map = HashMap<String, Int64>()

// 指定初始容量
let map2 = HashMap<String, Int64>(100)

// 从键值对数组构造
let map3 = HashMap<String, Int64>([("a", 1), ("b", 2), ("c", 3)])

// 从键值对集合构造
let map4 = HashMap<String, Int64>(otherCollection)

// 指定大小 + 初始化函数
let map5 = HashMap<Int64, Int64>(5, {i => (i, i * i)})
// {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### 构造函数签名

| 构造函数 | 说明 |
|----------|------|
| `init()` | 空 HashMap，默认容量 16 |
| `init(capacity: Int64)` | 空 HashMap，指定容量。`capacity < 0` 抛 `IllegalArgumentException` |
| `init(elements: Array<(K, V)>)` | 从键值对数组构造，重复键时后者覆盖前者 |
| `init(elements: Collection<(K, V)>)` | 从键值对集合构造，重复键时后者覆盖前者 |
| `init(size: Int64, initElement: (Int64) -> (K, V))` | 指定大小 + 初始化函数。`size < 0` 抛 `IllegalArgumentException` |

---

## 3. 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `size` | `Int64` | 键值对个数 |
| `capacity` | `Int64` | 当前内部容量 |

```cangjie
let map = HashMap<String, Int64>([("a", 1), ("b", 2)])
println(map.size)      // 2
println(map.capacity)  // >= 2
```

---

## 4. 添加与更新

### 4.1 `add` — 添加单个键值对

```cangjie
func add(key: K, value: V): Option<V>
```

- 键不存在：插入新键值对，返回 `None`
- 键已存在：用新值替换旧值，返回旧值 `Some(oldValue)`

```cangjie
let map = HashMap<String, Int64>()
map.add("a", 1)          // None（新增）
map.add("a", 99)         // Some(1)（替换，返回旧值 1）
println(map["a"])         // 99
```

### 4.2 `add` — 批量添加

```cangjie
func add(all!: Collection<(K, V)>): Unit
```

```cangjie
map.add(all: [("b", 2), ("c", 3)])
map.add(all: otherMap)
```

### 4.3 下标赋值

```cangjie
map["key"] = value   // 键存在则更新，不存在则新增
```

```cangjie
let map = HashMap<String, Int64>()
map["x"] = 10   // 新增
map["x"] = 20   // 更新
```

---

## 5. 查询

### 5.1 下标访问

```cangjie
let v = map["key"]   // 返回 V 类型值
```

- 键不存在抛出 `NoneValueException`

### 5.2 安全访问 `get`

```cangjie
func get(key: K): Option<V>
```

```cangjie
let map = HashMap<String, Int64>([("a", 1)])
map.get("a")    // Some(1)
map.get("xyz")  // None（不抛异常）
```

### 5.3 `contains` — 键是否存在

```cangjie
func contains(key: K): Bool
func contains(all!: Collection<K>): Bool
```

```cangjie
let map = HashMap<String, Int64>([("a", 1), ("b", 2)])
map.contains("a")                    // true
map.contains("xyz")                  // false
map.contains(all: ["a", "b"])       // true
map.contains(all: ["a", "c"])       // false（c 不存在）
```

### 5.4 `keys` / `values` / `toArray`

```cangjie
func keys(): EquatableCollection<K>   // 所有键
func values(): Collection<V>          // 所有值
func toArray(): Array<(K, V)>         // 所有键值对数组
```

```cangjie
let map = HashMap<String, Int64>([("a", 1), ("b", 2)])
let allKeys = map.keys()       // 包含 "a", "b"
let allValues = map.values()   // 包含 1, 2
let pairs = map.toArray()     // [("a", 1), ("b", 2)]（顺序不保证）
```

### 5.5 `entryView` — 获取条目引用视图

```cangjie
func entryView(key: K): MapEntryView<K, V>
```

- 返回指定键的引用视图，键不存在时返回空视图

---

## 6. 删除

### 6.1 按键删除

```cangjie
func remove(key: K): Option<V>
```

- 返回被删除的值；键不存在返回 `None`

```cangjie
let map = HashMap<String, Int64>([("a", 1), ("b", 2)])
let removed = map.remove("a")   // Some(1)
let nothing = map.remove("xyz") // None
```

### 6.2 批量删除

```cangjie
func remove(all!: Collection<K>): Unit
```

```cangjie
map.remove(all: ["a", "b"])
```

### 6.3 条件删除

```cangjie
func removeIf(predicate: (K, V) -> Bool): Unit
```

```cangjie
let map = HashMap<String, Int64>([("a", 1), ("b", 20), ("c", 3)])
map.removeIf { k, v => v > 10 }  // 删除 v > 10 的条目 → {"a": 1, "c": 3}
```

- 在 `predicate` 中修改 HashMap 会抛 `ConcurrentModificationException`

### 6.4 清空

```cangjie
func clear(): Unit
```

```cangjie
map.clear()  // size = 0
```

---

## 7. 遍历

```cangjie
func iterator(): HashMapIterator<K, V>
```

```cangjie
let map = HashMap<String, Int64>([("a", 1), ("b", 2), ("c", 3)])

// for-in 解构遍历（推荐）
for ((k, v) in map) {
    println("${k}: ${v}")
}

// 仅遍历键
for (k in map.keys()) {
    println(k)
}

// 仅遍历值
for (v in map.values()) {
    println(v)
}
```

> **注意**：遍历顺序不保证。如需有序遍历，考虑使用 `TreeMap<K, V>`。

---

## 8. 容量管理

```cangjie
func reserve(additional: Int64): Unit
```

```cangjie
map.reserve(100)  // 扩容以容纳更多元素
```

- `additional <= 0` 或剩余容量足够时不执行扩容
- 扩容后容量约为原来的 1.5 倍（不保证精确值）
- 当溢出 `Int64.Max` 时抛 `OverflowException`

---

## 9. 判空

```cangjie
func isEmpty(): Bool
```

```cangjie
HashMap<String, Int64>().isEmpty()  // true
```

---

## 10. 拷贝

```cangjie
func clone(): HashMap<K, V>
```

```cangjie
let map = HashMap<String, Int64>([("a", 1)])
let copy = map.clone()
copy["a"] = 999
println(map["a"])  // 1（不受影响）
```

---

## 11. 相等比较（需要 V <: Equatable<V>）

```cangjie
let a = HashMap<String, Int64>([("x", 1), ("y", 2)])
let b = HashMap<String, Int64>([("y", 2), ("x", 1)])
let c = HashMap<String, Int64>([("x", 1), ("y", 3)])

a == b  // true（键值对完全相同，不关心顺序）
a != c  // true
```

---

## 12. 转为字符串（需要 K <: ToString, V <: ToString）

```cangjie
func toString(): String
```

```cangjie
HashMap<String, Int64>([("a", 1), ("b", 2)]).toString()
// "[(a, 1), (b, 2)]"（顺序不保证）
```

---

## 13. 常见用法总结

```cangjie
import std.collection.*

// 1. 基本键值存储
let config = HashMap<String, String>()
config["host"] = "127.0.0.1"
config["port"] = "8080"

// 2. 安全取值
if (let Some(v) <- map.get("key")) {
    process(v)
}

// 3. 先检查再操作
if (map.contains("key")) {
    let v = map["key"]  // 安全，已确认键存在
}

// 4. 统计词频
let freq = HashMap<String, Int64>()
for (word in words) {
    let count = freq.get(word) ?? 0
    freq[word] = count + 1
}

// 5. 遍历并收集
let entries = ArrayList<String>()
for ((k, v) in map) {
    entries.add("${k}=${v}")
}
let result = String.join(entries.toArray(), delimiter: "&")

// 6. 从键值对数组批量构建
let headers = HashMap<String, String>([
    ("Content-Type", "application/json"),
    ("Authorization", "Bearer token123")
])

// 7. 条件过滤
map.removeIf { k, v => v == 0 }

// 8. 合并两个 Map
let merged = map1.clone()
merged.add(all: map2)  // map2 中的键覆盖 map1
```

---

## 14. 注意事项

| 要点 | 说明 |
|------|------|
| **键的要求** | `K` 必须实现 `Hashable` + `Equatable<K>`。常见可用类型：`String`、`Int64`、所有整数类型、`Bool`、`Rune` 等 |
| **线程安全** | `HashMap` **非线程安全**。多线程场景请使用 `ConcurrentHashMap`（`std.collection.concurrent`） |
| **键不存在** | 下标 `map["key"]` 在键不存在时抛 `NoneValueException`；安全方式用 `map.get("key")` |
| **遍历顺序** | 不保证顺序。需要有序遍历请使用 `TreeMap<K, V>` |
| **性能** | 平均 O(1) 查找/插入/删除。极端哈希冲突时退化为 O(n) |
