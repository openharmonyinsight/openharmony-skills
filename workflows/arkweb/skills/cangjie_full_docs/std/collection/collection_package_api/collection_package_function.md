# 函数

## func all\<T>((T) -> Bool)

```cangjie
public func all<T>(predicate: (T) -> Bool): (Iterable<T>) -> Bool
```

功能：判断迭代器所有元素是否都满足条件。

参数：

- predicate: (T) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 给定的条件。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回一个判断全部满足条件的函数。

## func any\<T>((T) -> Bool)

```cangjie
public func any<T>(predicate: (T) -> Bool): (Iterable<T>) -> Bool
```

功能：判断迭代器是否存在任意一个满足条件的元素。

参数：

- predicate: (T) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 给定的条件。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回一个判断存在任意一个满足条件的函数。

## func at\<T>(Int64)

```cangjie
public func at<T>(n: Int64): (Iterable<T>) -> Option<T>
```

功能：获取迭代器指定位置的元素。

参数：

- n: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 给定的个数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回获取对应位置元素的函数，若迭代器为空则该函数返回 None。

## func collectArray\<T>(Iterable\<T>)

```cangjie
public func collectArray<T>(it: Iterable<T>): Array<T>
```

功能：将一个迭代器转换成 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt) 类型。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 返回一个数组。

## func collectArrayList\<T>(Iterable\<T>)

```cangjie
public func collectArrayList<T>(it: Iterable<T>): ArrayList<T>
```

功能：将一个迭代器转换成 [ArrayList](collection_package_class.md#class-arraylistt) 类型。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [ArrayList](collection_package_class.md#class-arraylistt)\<T> - 返回一个 [ArrayList](collection_package_class.md#class-arraylistt)。

## func collectHashMap\<K, V>(Iterable\<(K, V)>) where K <: Hashable & Equatable\<K>

```cangjie
public func collectHashMap<K, V>(it: Iterable<(K, V)>): HashMap<K, V> where K <: Hashable & Equatable<K>
```

功能：将一个迭代器转换成 [HashMap](collection_package_class.md#class-hashmapk-v-where-k--hashable--equatablek) 类型。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<(K, V)> - 给定的迭代器。

返回值：

- [HashMap](collection_package_class.md#class-hashmapk-v-where-k--hashable--equatablek)\<K, V> - 返回一个 [HashMap](collection_package_class.md#class-hashmapk-v-where-k--hashable--equatablek)。

## func collectHashSet\<T>(Iterable\<T>) where T <: Hashable & Equatable\<T>

```cangjie
public func collectHashSet<T>(it: Iterable<T>): HashSet<T> where T <: Hashable & Equatable<T>
```

功能：将一个迭代器转换成 [HashSet](collection_package_class.md#class-hashsett-where-t--hashable--equatablet) 类型。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [HashSet](collection_package_class.md#class-hashsett-where-t--hashable--equatablet)\<T> - 返回一个 [HashSet](collection_package_class.md#class-hashsett-where-t--hashable--equatablet)。

## func collectString\<T>(String) where T <: ToString

```cangjie
public func collectString<T>(delimiter!: String = ""): (Iterable<T>) -> String where T <: ToString
```

功能：将一个对应元素实现了 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 接口的迭代器转换成 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型。

参数：

- delimiter!: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串拼接分隔符。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [String](../../core/core_package_api/core_package_structs.md#struct-string) - 返回一个转换函数。

## func concat\<T>(Iterable\<T>)

```cangjie
public func concat<T>(other: Iterable<T>): (Iterable<T>) -> Iterator<T>
```

功能：串联两个迭代器。

参数：

- other: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 要串联在后面的迭代器。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个串联函数。

## func contains\<T>(T) where T <: Equatable\<T>

```cangjie
public func contains<T>(element: T): (Iterable<T>) -> Bool where T <: Equatable<T>
```

功能：获得一个针对特定元素的查找函数。

参数：

- element: T - 要查找的元素。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回一个查找函数。

示例：

<!-- verify -->
```cangjie
import std.collection.*

main() {
    var searchFunc = contains<Int64>(6) // 获得查找元素 6 的函数
    let arr = ArrayList.of([1, 2, 3, 4, 5, 6])
    let i = arr.iterator()
    var result = searchFunc(i) // 调用函数
    println(result)
    searchFunc = contains<Int64>(7) // 获得查找元素 7 的函数
    result = searchFunc(i) // 调用函数
    println(result)
    return 0
}
```

运行结果：

```text
true
false
```

## func count\<T>(Iterable\<T>)

```cangjie
public func count<T>(it: Iterable<T>): Int64
```

功能：统计迭代器包含元素数量。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回迭代器包含元素数量。

## func enumerate\<T>(Iterable\<T>)

```cangjie
public func enumerate<T>(it: Iterable<T>): Iterator<(Int64, T)>
```

功能：用于获取带索引的迭代器。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<([Int64](../../core/core_package_api/core_package_intrinsics.md#int64), T)> - 返回一个带索引的迭代器。

## func filter\<T>((T) -> Bool)

```cangjie
public func filter<T>(predicate: (T) -> Bool): (Iterable<T>) -> Iterator<T>
```

功能：筛选出满足条件的元素。

参数：

- predicate: (T) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 给定的条件。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个筛选函数。

## func filterMap\<T, R>((T) -> ?R)

```cangjie
public func filterMap<T, R>(transform: (T) -> ?R): (Iterable<T>) -> Iterator<R>
```

功能：同时进行筛选操作和映射操作，返回一个新的迭代器。

参数：

- transform: (T) -> ?R - 给定的映射函数。函数返回值为 Some 对应 filter 的 predicate 为 true，反之表示 false。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<R> - 返回一个筛选和映射的函数。

## func first\<T>(Iterable\<T>)

```cangjie
public func first<T>(it: Iterable<T>): Option<T>
```

功能：获取头部元素。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回头部元素，若为空则返回 None。

## func flatMap\<T, R>((T) -> Iterable\<R>)

```cangjie
public func flatMap<T, R>(transform: (T) -> Iterable<R>): (Iterable<T>) -> Iterator<R>
```

功能：创建一个带 [flatten](collection_package_function.md#func-flattent-riterablet-where-t--iterabler) 功能的映射。

参数：

- transform: (T) -> [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<R> - 给定的映射函数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<R> - 返回一个带 [flatten](collection_package_function.md#func-flattent-riterablet-where-t--iterabler) 功能的映射函数。

## func flatten\<T, R>(Iterable\<T>) where T <: Iterable\<R>

```cangjie
public func flatten<T, R>(it: Iterable<T>): Iterator<R> where T <: Iterable<R>
```

功能：将嵌套的迭代器展开一层。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<R> - 返回展开一层后的迭代器。

## func fold\<T, R>(R, (R, T) -> R)

```cangjie
public func fold<T, R>(initial: R, operation: (R, T) -> R): (Iterable<T>) -> R
```

功能：使用指定初始值，从左向右计算。

参数：

- initial: R - 给定的 R 类型的初始值。
- operation: (R, T) -> R - 给定的计算函数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> R - 返回一个折叠函数。

## func forEach\<T>((T) -> Unit)

```cangjie
public func forEach<T>(action: (T) -> Unit): (Iterable<T>) -> Unit
```

功能：遍历所有元素，指定给定的操作。

参数：

- action: (T) -> [Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 给定的操作函数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 返回一个执行遍历操作的函数。

## func inspect\<T>((T) -> Unit)

```cangjie
public func inspect<T>(action: (T)->Unit): (Iterable<T>) ->Iterator<T>
```

功能：迭代器每次调用 next() 对当前元素执行额外操作（不会消耗迭代器中元素）。

参数：

- action: (T) -> [Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 给定的操作函数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个能对迭代器每个元素执行额外操作的函数。

## func isEmpty\<T>(Iterable\<T>)

```cangjie
public func isEmpty<T>(it: Iterable<T>): Bool
```

功能：判断迭代器是否为空。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回迭代器是否为空。

## func last\<T>(Iterable\<T>)

```cangjie
public func last<T>(it: Iterable<T>): Option<T>
```

功能：获取尾部元素。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回尾部元素，若为空则返回 None。

## func map\<T, R>((T) -> R)

```cangjie
public func map<T, R>(transform: (T) -> R): (Iterable<T>) -> Iterator<R>
```

功能：创建一个映射。

参数：

- transform: (T) ->R - 给定的映射函数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<R> - 返回一个映射函数。

## func max\<T>(Iterable\<T>) where T <: Comparable\<T>

```cangjie
public func max<T>(it: Iterable<T>): Option<T> where T <: Comparable<T>
```

功能：筛选最大的元素。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回最大的元素，若为空则返回 None。

## func min\<T>(Iterable\<T>) where T <: Comparable\<T>

```cangjie
public func min<T>(it: Iterable<T>): Option<T> where T <: Comparable<T>
```

功能：筛选最小的元素。

参数：

- it: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 给定的迭代器。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回最小的元素，若为空则返回 None。

## func none\<T>((T) -> Bool)

```cangjie
public func none<T>(predicate: (T) -> Bool): (Iterable<T>) -> Bool
```

功能：判断迭代器中所有元素是否都不满足条件。

参数：

- predicate: (T) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 给定的条件。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回一个判断都不满足条件的函数。

## func reduce\<T>((T, T) -> T)

```cangjie
public func reduce<T>(operation: (T, T) -> T): (Iterable<T>) -> Option<T>
```

功能：使用第一个元素作为初始值，从左向右计算。

参数：

- operation: (T, T) -> T - 给定的操作函数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回一个归并函数。

## func skip\<T>(Int64)

```cangjie
public func skip<T>(count: Int64): (Iterable<T>) -> Iterator<T>
```

功能：从迭代器跳过特定个数。

当 count 小于 0 时，抛出异常。当 count 等于 0 时，相当没有跳过任何元素，返回原迭代器。当 count 大于 0 并且 count 小于迭代器的大小时，跳过 count 个元素后，返回含有剩下的元素的新迭代器。当 count 大于等于迭代器的大小时，跳过所有元素，返回空迭代器。

参数：

- count: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 要跳过的个数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个跳过指定数量元素的函数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 count < 0 时，抛出异常。

## func step\<T>(Int64)

```cangjie
public func step<T>(count: Int64): (Iterable<T>) -> Iterator<T>
```

功能：迭代器每次调用 next() 跳过特定个数。

当 count 小于等于 0 时，抛出异常。当 count 大于 0 时，每次调用 next() 跳过 count 次，直到迭代器为空。

参数：

- count: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 每次调用 next() 要跳过的个数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回改变迭代器每次调用 next() 跳过特定个数的函数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 count <= 0 时，抛出异常。

## func take\<T>(Int64)

```cangjie
public func take<T>(count: Int64): (Iterable<T>) -> Iterator<T>
```

功能：从迭代器取出特定个数。

当 count 小于 0 时，抛出异常。当 count 等于 0 时，不取元素，返回空迭代器。当 count 大于 0 小于迭代器的大小时，取前 count 个元素，返回新迭代器。当 count 大于等于迭代器的大小时，取所有元素，返回原迭代器。

参数：

- count: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 要取出的个数。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个取出指定数量元素的函数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 count < 0 时，抛出异常。

## func zip\<T, R>(Iterable\<R>)

```cangjie
public func zip<T, R>(other: Iterable<R>): (Iterable<T>) -> Iterator<(T, R)>
```

功能：将两个迭代器合并成一个（长度取决于短的那个迭代器）。

参数：

- other: [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<R> - 要合并的其中一个迭代器。

返回值：

- ([Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T>) -> [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<(T, R)> - 返回一个合并函数。
