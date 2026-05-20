---
name: cangjie-collections-array
description: "仓颉 Array 类型用法。"
---

# 仓颉标准库 Array 类型 Skill

## 1. 概述

`Array<T>` 是仓颉核心包 `std.core` 中的 **struct** 类型，**无需导入** 即可直接使用。

- **固定大小** — 创建后长度不可变，但元素值可修改
- **值类型** — 但内部通过引用共享数据，`let arr2 = arr1` 后两者**共享**底层存储，修改会互相可见
- `T` 可以是任意类型

---

## 2. 构造

```cangjie
// 字面量构造（最常用）
let arr = [1, 2, 3, 4, 5]

// 空数组
let empty = Array<Int64>()

// 指定大小 + 重复值
let zeros = Array<Int64>(5, repeat: 0)  // [0, 0, 0, 0, 0]

// 指定大小 + 初始化函数
let arr2 = Array<Int64>(5, {i => i * 2})  // [0, 2, 4, 6, 8]
```

### 构造函数签名

| 构造函数 | 说明 |
|----------|------|
| `init()` | 创建空数组 |
| `init(size: Int64, repeat!: T)` | 创建指定大小数组，所有元素为 `repeat` 值 |
| `init(size: Int64, initElement: (Int64) -> T)` | 创建指定大小数组，元素由函数生成 |

- `size < 0` 时抛出 `NegativeArraySizeException`

---

## 3. 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `size` | `Int64` | 元素个数（通过 `Collection` 扩展提供） |
| `first` | `Option<T>` | 首元素，空数组返回 `None` |
| `last` | `Option<T>` | 尾元素，空数组返回 `None` |

```cangjie
let arr = [10, 20, 30]
println(arr.size)   // 3
println(arr.first)  // Some(10)
println(arr.last)   // Some(30)

let empty = Array<Int64>()
println(empty.first) // None
```

---

## 4. 元素访问与修改

### 4.1 下标访问

```cangjie
let arr = [10, 20, 30]
let v = arr[0]   // 10
arr[2] = 99      // [10, 20, 99]
```

- 索引从 `0` 开始，类型为 `Int64`
- 越界抛出 `IndexOutOfBoundsException`

### 4.2 安全访问 `get`

```cangjie
func get(index: Int64): Option<T>
```

```cangjie
let arr = [10, 20, 30]
arr.get(1)   // Some(20)
arr.get(10)  // None（不抛异常）
```

### 4.3 交换元素 `swap`

```cangjie
func swap(i: Int64, j: Int64): Unit
```

```cangjie
var arr = [1, 2, 3]
arr.swap(0, 2)  // [3, 2, 1]
```

---

## 5. 切片与分割

### 5.1 范围下标切片

```cangjie
let arr = [0, 1, 2, 3, 4, 5]
let sub = arr[1..4]    // [1, 2, 3]（引用，非拷贝）
let sub2 = arr[2..=4]  // [2, 3, 4]（闭区间）
```

> **注意**：范围下标返回的是原数组的引用切片，修改会反映到原数组。

### 5.2 范围赋值

```cangjie
var arr = [0, 1, 2, 3, 4, 5]
arr[1..3] = [10, 11]   // [0, 10, 11, 3, 4, 5]
```

### 5.3 `slice` — 获取切片

```cangjie
func slice(start: Int64, len: Int64): Array<T>
```

```cangjie
let arr = [0, 1, 2, 3, 4]
let s = arr.slice(1, 3) // [1, 2, 3]（从索引 1 开始取 3 个元素，引用）
```

### 5.4 `splitAt` — 在指定位置分割

```cangjie
func splitAt(index: Int64): (Array<T>, Array<T>)
```

```cangjie
let arr = [0, 1, 2, 3, 4]
let (left, right) = arr.splitAt(2) // left=[0, 1], right=[2, 3, 4]
```

---

## 6. 拼接与重复

### 6.1 `concat` — 拼接

```cangjie
func concat(other: Array<T>): Array<T>
```

```cangjie
let a = [1, 2]
let b = [3, 4]
let c = a.concat(b) // [1, 2, 3, 4]
```

### 6.2 `repeat` — 重复

```cangjie
func repeat(times: Int64): Array<T>
```

```cangjie
let arr = [1, 2].repeat(3) // [1, 2, 1, 2, 1, 2]
```

---

## 7. 拷贝

### 7.1 `clone` — 深拷贝

```cangjie
func clone(): Array<T>
func clone(range: Range<Int64>): Array<T>
```

```cangjie
let arr = [1, 2, 3]
let copy = arr.clone()        // [1, 2, 3]，独立副本
let partial = arr.clone(1..3) // [2, 3]
```

### 7.2 `copyTo` — 拷贝到目标数组

```cangjie
func copyTo(dst: Array<T>): Unit
func copyTo(dst: Array<T>, srcStart: Int64, srcLen: Int64, dstStart: Int64): Unit
```

```cangjie
let src = [1, 2, 3]
let dst = Array<Int64>(5, repeat: 0)
src.copyTo(dst)                    // dst = [1, 2, 3, 0, 0]
src.copyTo(dst, 0, 2, 3)          // dst = [1, 2, 3, 1, 2]（从 src[0] 取 2 个放到 dst[3]）
```

---

## 8. 填充与反转

### 8.1 `fill` — 用指定值填充全部元素

```cangjie
func fill(value: T): Unit
```

```cangjie
var arr = [1, 2, 3]
arr.fill(0) // [0, 0, 0]
```

### 8.2 `reverse` — 原地反转

```cangjie
func reverse(): Unit
```

```cangjie
var arr = [1, 2, 3, 4, 5]
arr.reverse() // [5, 4, 3, 2, 1]
```

---

## 9. 映射与扁平化

### 9.1 `map` — 元素映射

```cangjie
func map<R>(transform: (T) -> R): Array<R>
```

```cangjie
let arr = [1, 2, 3]
let strs = arr.map { v => v.toString() }  // ["1", "2", "3"]
let doubled = arr.map { v => v * 2 }      // [2, 4, 6]
```

### 9.2 `flatten` — 扁平化二维数组

```cangjie
// 仅对 Array<Array<T>> 可用
func flatten(): Array<T>
```

```cangjie
let arr2d = [[1, 2], [3, 4], [5]]
let flat = arr2d.flatten() // [1, 2, 3, 4, 5]
```

---

## 10. 搜索与查找（需要 T <: Equatable<T>）

以下方法需要元素类型 `T` 实现 `Equatable<T>` 接口。

### 10.1 `contains` — 判断是否包含元素

```cangjie
func contains(element: T): Bool
```

```cangjie
[1, 2, 3].contains(2)  // true
[1, 2, 3].contains(5)  // false
```

### 10.2 `indexOf` — 查找元素/子数组位置

```cangjie
func indexOf(element: T): Option<Int64>
func indexOf(element: T, fromIndex: Int64): Option<Int64>
func indexOf(subArray: Array<T>): Option<Int64>
```

```cangjie
[10, 20, 30, 20].indexOf(20)      // Some(1)
[10, 20, 30, 20].indexOf(20, 2)   // Some(3)  — 从索引 2 开始搜索
[1, 2, 3, 4].indexOf([2, 3])      // Some(1)  — 子数组位置
[1, 2, 3].indexOf(99)             // None
```

### 10.3 `lastIndexOf` — 查找最后出现位置

```cangjie
func lastIndexOf(element: T): Option<Int64>
func lastIndexOf(subArray: Array<T>): Option<Int64>
```

```cangjie
[1, 2, 3, 2, 1].lastIndexOf(2) // Some(3)
```

### 10.4 `removePrefix` / `removeSuffix`

```cangjie
func removePrefix(prefix: Array<T>): Array<T>
func removeSuffix(suffix: Array<T>): Array<T>
```

```cangjie
[1, 2, 3, 4].removePrefix([1, 2]) // [3, 4]
[1, 2, 3, 4].removeSuffix([3, 4]) // [1, 2]
[1, 2, 3].removePrefix([9, 8])    // [1, 2, 3]（无匹配，返回原数组）
```

### 10.5 `trimStart` / `trimEnd`

```cangjie
func trimStart(elements: Array<T>): Array<T>
func trimStart(predicate: (T) -> Bool): Array<T>
func trimEnd(elements: Array<T>): Array<T>
func trimEnd(predicate: (T) -> Bool): Array<T>
```

```cangjie
[0, 0, 1, 2, 0].trimStart([0])           // [1, 2, 0]
[0, 0, 1, 2, 0].trimEnd([0])             // [0, 0, 1, 2]
[0, 1, 2, 3].trimStart { v => v < 2 }    // [2, 3]
```

---

## 11. 相等比较（需要 T <: Equatable<T>）

```cangjie
let a = [1, 2, 3]
let b = [1, 2, 3]
let c = [1, 2, 4]
a == b  // true
a != c  // true
```

---

## 12. 转为字符串（需要 T <: ToString）

```cangjie
func toString(): String
```

```cangjie
[1, 2, 3].toString() // "[1, 2, 3]"
```

---

## 13. 迭代

```cangjie
func iterator(): Iterator<T>
func isEmpty(): Bool
func toArray(): Array<T>
```

```cangjie
let arr = [10, 20, 30]

// for-in 遍历
for (v in arr) {
    println(v)
}

// 使用迭代器
var it = arr.iterator()
while (true) {
    match (it.next()) {
        case Some(v) => println(v)
        case None => break
    }
}
```

---

## 14. 排序（使用 std.sort）

Array 本身不提供排序方法，需导入 `std.sort`：

```cangjie
import std.sort.*

var arr = [3, 1, 4, 1, 5, 9]
sort(arr)                        // 原地升序：[1, 1, 3, 4, 5, 9]
sort(arr) { a, b => b - a }     // 自定义降序
```

---

## 15. 常见用法总结

```cangjie
// 1. 创建固定大小数组
let buffer = Array<Byte>(1024, repeat: 0)

// 2. 字面量 + 修改
var scores = [90, 85, 78]
scores[1] = 95

// 3. 遍历并映射
let names = ["Alice", "Bob"]
let upper = names.map { n => n.toAsciiUpper() }

// 4. 查找元素
if (let Some(idx) <- arr.indexOf(target)) {
    println("Found at ${idx}")
}

// 5. 拼接数组
let combined = arr1.concat(arr2)

// 6. 二维数组扁平化
let matrix = [[1, 2], [3, 4]]
let flat = matrix.flatten() // [1, 2, 3, 4]

// 7. 拷贝后独立修改
let copy = arr.clone()
copy[0] = 999  // 不影响原数组

// 8. 分割数组
let (head, tail) = data.splitAt(3)
```
