# 函数

## func sort\<T, K>(Array\<T>, (T) -> K, Bool, Bool) where K <: Comparable\<K>

```cangjie
public func sort<T, K>(data: Array<T>, key!: (T) -> K, stable!: Bool = false, descending!: Bool = false): Unit where K <: Comparable<K>
```

功能：对数组按照指定的键（键与键之间可比较）进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

用户需传入数组元素到键的映射函数。

参数：

- data: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 需要排序的数组。
- key!: (T) -> K - 元素到键的映射函数。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

示例：

<!-- verify -->
```cangjie
import std.sort.*

class Rectangle <: ToString {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func toString(): String {
        return "#width: ${this.width}, height: ${this.height}"
    }
}

main() {
    /* 按照宽降序排序 */
    var arr = [Rectangle(4, 8), Rectangle(6, 7), Rectangle(2, 6)]
    sort<Rectangle, Int64>(
        arr,
        key: {
            r: Rectangle => return r.width
        },
        stable: true,
        descending: true
    )
    println(arr)
    return 0
}
```

运行结果：

```text
[#width: 6, height: 7, #width: 4, height: 8, #width: 2, height: 6]
```

## func sort\<T, K>(ArrayList\<T>, (T) -> K, Bool, Bool) where K <: Comparable\<K>

```cangjie
public func sort<T, K>(data: ArrayList<T>, key!: (T) -> K, stable!: Bool = false, descending!: Bool = false): Unit where K <: Comparable<K>
```

功能：对 `ArrayList` 按照指定的键（键与键之间可比较）进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

用户需传入 `ArrayList` 元素到键的映射函数。

参数：

- data: [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<T> - 需要排序的 `ArrayList`。
- key!: (T) -> K - 元素到键的映射函数。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

示例：

<!-- verify -->
```cangjie
import std.sort.*
import std.collection.*

class Rectangle <: ToString {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func toString(): String {
        return "#width: ${this.width}, height: ${this.height}"
    }
}

main() {
    /* 按照宽降序排序 */
    var arr = ArrayList<Rectangle>([Rectangle(4, 8), Rectangle(6, 7), Rectangle(2, 6)])
    sort<Rectangle, Int64>(
        arr,
        key: {
            r: Rectangle => return r.width
        },
        stable: true,
        descending: true
    )
    println(arr)
    return 0
}
```

运行结果：

```text
[#width: 6, height: 7, #width: 4, height: 8, #width: 2, height: 6]
```

## func sort\<T, K>(List\<T>, (T) -> K, Bool, Bool) where K <: Comparable\<K>

```cangjie
public func sort<T, K>(data: List<T>, key!: (T) -> K, stable!: Bool = false, descending!: Bool = false): Unit where K <: Comparable<K>
```

功能：对 `List` 按照指定的键（键与键之间可比较）进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

用户需传入 `List` 元素到键的映射函数。

参数：

- data: [List](../../collection/collection_package_api/collection_package_interface.md#interface-listt)\<T> - 需要排序的 `List`。
- key!: (T) -> K - 元素到键的映射函数。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

## func sort\<T>(Array\<T>, (T, T) -> Bool, Bool, Bool)

```cangjie
public func sort<T>(data: Array<T>, lessThan!: (T, T) -> Bool, stable!: Bool = false, descending!: Bool = false): Unit
```

功能：对数组按照比较函数进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

用户需传入自定义的比较函数 `lessThan`。如果 `lessThan` 的返回值为 `true`，排序后 `t1` 在 `t2` 前；如果 `lessThan` 的返回值为`false`，又会分为两种情况，如果 `t1` 和 `t2` 不相等，排序后 `t1` 在 `t2` 后，如果相等，`t1` 与 `t2` 的前后位置关系与是否是稳定排序有关，稳定则较排序前保持不变，否则有可能发生改变。

参数：

- data: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 需要排序的数组。
- lessThan!: (T, T) ->[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 传入的比较函数。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

示例：

<!-- verify -->
```cangjie
import std.sort.*

class Rectangle <: ToString {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func toString(): String {
        return "#width: ${this.width}, height: ${this.height}"
    }
}

main() {
    /* 按照面积降序排序 */
    var arr = [Rectangle(4, 8), Rectangle(6, 7), Rectangle(2, 6)]
    sort<Rectangle>(
        arr,
        lessThan: {
            r1: Rectangle, r2: Rectangle =>
            let r1Value: Int64 = r1.width * r1.height
            let r2Value: Int64 = r2.width * r2.height
            return r1Value < r2Value
        },
        stable: true,
        descending: true
    )
    println(arr)
    return 0
}
```

运行结果：

```text
[#width: 6, height: 7, #width: 4, height: 8, #width: 2, height: 6]
```

## func sort\<T>(Array\<T>, (T, T) -> Ordering, Bool, Bool)

```cangjie
public func sort<T>(data: Array<T>, by!: (T, T) -> Ordering, stable!: Bool = false, descending!: Bool = false): Unit
```

功能：对数组按照比较函数进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

用户需传入自定义的比较函数 `by`。如果 `by` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).GT，排序后 `t1` 在 `t2` 后；如果 `by` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).LT，排序后 `t1` 在 `t2` 前；如果 `by` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).EQ，排序后 `t1` 与 `t2` 的位置与是否是稳定排序有关，稳定则较排序前保持不变，否则有可能发生改变。

参数：

- data: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 需要排序的数组。
- by!: (T, T) ->[Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) - 传入的比较函数。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

示例：

<!-- verify -->
```cangjie
import std.sort.*

class Rectangle <: ToString {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func toString(): String {
        return "#width: ${this.width}, height: ${this.height}"
    }
}

main() {
    /* 按照面积降序排序 */
    var arr = [Rectangle(4, 8), Rectangle(6, 7), Rectangle(2, 6)]
    sort<Rectangle>(
        arr,
        by: {
            r1: Rectangle, r2: Rectangle =>
            let r1Value: Int64 = r1.width * r1.height
            let r2Value: Int64 = r2.width * r2.height
            if (r1Value > r2Value) {
                return Ordering.GT
            } else if (r1Value == r2Value) {
                return Ordering.EQ
            } else {
                return Ordering.LT
            }
        },
        stable: true,
        descending: true
    )
    println(arr)
    return 0
}
```

运行结果：

```text
[#width: 6, height: 7, #width: 4, height: 8, #width: 2, height: 6]
```

## func sort\<T>(Array\<T>, Bool, Bool) where T <: Comparable\<T>

```cangjie
public func sort<T>(data: Array<T>, stable!: Bool = false, descending!: Bool = false): Unit where T <: Comparable<T>
```

功能：对数组进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

参数：

- data: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 需要排序的数组。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

示例：

<!-- verify -->
```cangjie
import std.sort.*

class Rectangle <: Comparable<Rectangle> & ToString {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func compare(r: Rectangle) {
        let tValue: Int64 = this.width * this.height
        let rValue: Int64 = r.width * r.height
        if (tValue > rValue) {
            return Ordering.GT
        } else if (tValue == rValue) {
            return Ordering.EQ
        } else {
            return Ordering.LT
        }
    }

    public func toString(): String {
        return "#width: ${this.width}, height: ${this.height}"
    }
}

main() {
    /* 按照面积降序排序 */
    var arr = [Rectangle(4, 8), Rectangle(6, 7), Rectangle(2, 6)]
    sort<Rectangle>(arr, stable: true, descending: true)
    println(arr)
    return 0
}
```

运行结果：

```text
[#width: 6, height: 7, #width: 4, height: 8, #width: 2, height: 6]
```

## func sort\<T>(ArrayList\<T>, (T, T) -> Bool, Bool, Bool)

```cangjie
public func sort<T>(data: ArrayList<T>, lessThan!: (T, T) -> Bool, stable!: Bool = false, descending!: Bool = false): Unit
```

功能：对 `ArrayList` 按照比较函数进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

用户需传入自定义的比较函数 `lessThan`。如果 `lessThan` 的返回值为 `true`，排序后 `t1` 在 `t2` 前；如果 `lessThan` 的返回值为`false`，又会分为两种情况，如果 `t1` 和 `t2` 不相等，排序后 `t1` 在 `t2` 后，如果相等，`t1` 与 `t2` 的前后位置关系与是否是稳定排序有关，稳定则较排序前保持不变，否则有可能发生改变。

参数：

- data: [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<T> - 需要排序的 `ArrayList`。
- lessThan!: (T, T) ->[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 传入的比较函数。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

示例：

<!-- verify -->
```cangjie
import std.sort.*
import std.collection.*

class Rectangle <: ToString {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func toString(): String {
        return "#width: ${this.width}, height: ${this.height}"
    }
}

main() {
    /* 按照面积降序排序 */
    var arr = ArrayList<Rectangle>([Rectangle(4, 8), Rectangle(6, 7), Rectangle(2, 6)])
    sort<Rectangle>(
        arr,
        lessThan: {
            r1: Rectangle, r2: Rectangle =>
            let r1Value: Int64 = r1.width * r1.height
            let r2Value: Int64 = r2.width * r2.height
            return r1Value < r2Value
        },
        stable: true,
        descending: true
    )
    println(arr)
    return 0
}
```

运行结果：

```text
[#width: 6, height: 7, #width: 4, height: 8, #width: 2, height: 6]
```

## func sort\<T>(ArrayList\<T>, (T, T) -> Ordering, Bool, Bool)

```cangjie
public func sort<T>(data: ArrayList<T>, by!: (T, T) -> Ordering, stable!: Bool = false, descending!: Bool = false): Unit
```

功能：对 `ArrayList` 按照比较函数进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

用户需传入自定义的比较函数 `by`。如果 `by` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).GT，排序后 `t1` 在 `t2` 后；如果 `by` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).LT，排序后 `t1` 在 `t2` 前；如果 `by` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).EQ，排序后 `t1` 与 `t2` 的位置与是否是稳定排序有关，稳定则较排序前保持不变，否则有可能发生改变。

参数：

- data: [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<T> - 需要排序的 `ArrayList`。
- by!: (T, T) ->[Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) - 传入的比较函数。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

示例：

<!-- verify -->
```cangjie
import std.sort.*
import std.collection.*

class Rectangle <: ToString {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func toString(): String {
        return "#width: ${this.width}, height: ${this.height}"
    }
}

main() {
    /* 按照面积降序排序 */
    var arr = ArrayList<Rectangle>([Rectangle(4, 8), Rectangle(6, 7), Rectangle(2, 6)])
    sort<Rectangle>(
        arr,
        by: {
            r1: Rectangle, r2: Rectangle =>
            let r1Value: Int64 = r1.width * r1.height
            let r2Value: Int64 = r2.width * r2.height
            if (r1Value > r2Value) {
                return Ordering.GT
            } else if (r1Value == r2Value) {
                return Ordering.EQ
            } else {
                return Ordering.LT
            }
        },
        stable: true,
        descending: true
    )
    println(arr)
    return 0
}
```

运行结果：

```text
[#width: 6, height: 7, #width: 4, height: 8, #width: 2, height: 6]
```

## func sort\<T>(ArrayList\<T>, Bool, Bool) where T <: Comparable\<T>

```cangjie
public func sort<T>(data: ArrayList<T>, stable!: Bool = false, descending!: Bool = false): Unit where T <: Comparable<T>
```

功能：对 `ArrayList` 进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

参数：

- data: [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<T> - 需要排序的 `ArrayList`。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

示例：

<!-- verify -->
```cangjie
import std.sort.*
import std.collection.*

class Rectangle <: Comparable<Rectangle> & ToString {
    var width: Int64
    var height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func compare(r: Rectangle) {
        let tValue: Int64 = this.width * this.height
        let rValue: Int64 = r.width * r.height
        if (tValue > rValue) {
            return Ordering.GT
        } else if (tValue == rValue) {
            return Ordering.EQ
        } else {
            return Ordering.LT
        }
    }

    public func toString(): String {
        return "#width: ${this.width}, height: ${this.height}"
    }
}

main() {
    /* 按照面积降序排序 */
    var arr = ArrayList<Rectangle>([Rectangle(4, 8), Rectangle(6, 7), Rectangle(2, 6)])
    sort<Rectangle>(arr, stable: true, descending: true)
    println(arr)
    return 0
}
```

运行结果：

```text
[#width: 6, height: 7, #width: 4, height: 8, #width: 2, height: 6]
```

## func sort\<T>(List\<T>, (T, T) -> Bool, Bool, Bool)

```cangjie
public func sort<T>(data: List<T>, lessThan!: (T, T) -> Bool, stable!: Bool = false, descending!: Bool = false): Unit
```

功能：对 `List` 按照比较函数进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

用户需传入自定义的比较函数 `lessThan`。如果 `lessThan` 的返回值为 `true`，排序后 `t1` 在 `t2` 前；如果 `lessThan` 的返回值为`false`，又会分为两种情况，如果 `t1` 和 `t2` 不相等，排序后 `t1` 在 `t2` 后，如果相等，`t1` 与 `t2` 的前后位置关系与是否是稳定排序有关，稳定则较排序前保持不变，否则有可能发生改变。

参数：

- data: [List](../../collection/collection_package_api/collection_package_interface.md#interface-listt)\<T> - 需要排序的 `List`。
- lessThan!: (T, T) ->[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 传入的比较函数。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

## func sort\<T>(List\<T>, (T, T) -> Ordering, Bool, Bool)

```cangjie
public func sort<T>(data: List<T>, by!: (T, T) -> Ordering, stable!: Bool = false, descending!: Bool = false): Unit
```

功能：对 `List` 按照比较函数进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

用户需传入自定义的比较函数 `by`。如果 `by` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).GT，排序后 `t1` 在 `t2` 后；如果 `by` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).LT，排序后 `t1` 在 `t2` 前；如果 `by` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).EQ，排序后 `t1` 与 `t2` 的位置与是否是稳定排序有关，稳定则较排序前保持不变，否则有可能发生改变。

参数：

- data: [List](../../collection/collection_package_api/collection_package_interface.md#interface-listt)\<T> - 需要排序的 `List`。
- by!: (T, T) ->[Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) - 传入的比较函数。
- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

## func sort\<T>(List\<T>, Bool, Bool) where T <: Comparable\<T>

```cangjie
public func sort<T>(data: List<T>, stable!: Bool = false, descending!: Bool = false): Unit where T <: Comparable<T>
```

功能：对 `List` 进行排序。可根据入参指定是否要进行稳定排序，是升序还是降序。

参数：

- data: [List](../../collection/collection_package_api/collection_package_interface.md#interface-listt)\<T> - 需要排序的 `List`。

- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序，默认为否。
- descending!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用降序排序，默认为否。

## func stableSort\<T>(Array\<T>) where T <: Comparable\<T> <sup>(deprecated)</sup>

```cangjie
public func stableSort<T>(data: Array<T>): Unit where T <: Comparable<T>
```

功能：对数组进行稳定升序排序。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-bool-bool-where-t--comparablet) 替代。

参数：

- data: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 需要排序的数组。

## func stableSort\<T>(Array\<T>, (T, T) -> Ordering) <sup>(deprecated)</sup>

```cangjie
public func stableSort<T>(data: Array<T>, comparator: (T, T) -> Ordering): Unit
```

功能：对数组进行稳定排序。

用户可传入自定义的比较函数 `comparator`，如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).GT，排序后 `t1` 在 `t2` 后；如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).LT，排序后 `t1` 在 `t2` 前；如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).EQ，排序后 `t1` 与 `t2` 的位置较排序前保持不变。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-t-t---ordering-bool-bool) 替代。

参数：

- data: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 需要排序的数组。
- comparator: (T, T) ->[Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) - 用户传入的比较函数。

## func unstableSort\<T>(Array\<T>) where T <: Comparable\<T> <sup>(deprecated)</sup>

```cangjie
public func unstableSort<T>(data: Array<T>): Unit where T <: Comparable<T>
```

功能：对数组进行不稳定升序排序。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-bool-bool-where-t--comparablet)  替代。

参数：

- data: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 需要排序的数组。

## func unstableSort\<T>(Array\<T>, (T, T) -> Ordering) <sup>(deprecated)</sup>

```cangjie
public func unstableSort<T>(data: Array<T>, comparator: (T, T) -> Ordering): Unit
```

功能：对数组进行不稳定排序。

用户可传入自定义的比较函数 `comparator`，如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).GT，排序后 `t1` 在 `t2` 后；如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).LT，排序后 `t1` 在 `t2` 前；如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).EQ，排序后 `t1` 与 `t2` 的位置较排序前保持不变。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-t-t---ordering-bool-bool) 替代。

参数：

- data: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 需要排序的数组。
- comparator: (T, T) ->[Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) - 用户传入的比较函数。
