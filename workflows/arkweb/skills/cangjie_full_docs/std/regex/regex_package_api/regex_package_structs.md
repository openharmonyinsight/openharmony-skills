# 结构体

## struct MatchData

```cangjie
public struct MatchData {}
```

功能：存储正则表达式匹配结果，并提供对正则匹配结果进行查询的函数。

### func groupCount()

```cangjie
public func groupCount(): Int64
```

功能：获取捕获组的个数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 捕获组的个数。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    let iter = r.lazyFindAll("2024-10-24&2025-01-01", group: true)
    while (true) {
        match (iter.next()) {
            case Some(md) => println("found: `${md.matchString()}` and groupCount: ${md.groupCount()}")
            case None => break
        }
    }
}
```

运行结果：

```text
found: `2024-10-24` and groupCount: 3
found: `2025-01-01` and groupCount: 3
```

### func groupNumber() <sup>(deprecated)</sup>

```cangjie
public func groupNumber(): Int64
```

功能：获取捕获组的个数。

> **注意：**
>
> 未来版本即将废弃，使用 [groupCount()](#func-groupcount) 替代。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 捕获组的个数。

### func matchPosition()

```cangjie
public func matchPosition(): Position
```

功能：获取上一次匹配到的子字符串在输入字符串中起始位置和末尾位置的索引。

返回值：

- [Position](#struct-position) - 匹配结果位置信息。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    let iter = r.lazyFindAll("2024-10-24&2025-01-01", group: true)
    while (true) {
        match (iter.next()) {
            case Some(md) =>
                println("found: ${md.matchString()} and groupCount: ${md.groupCount()}")
                let pos = md.matchPosition(0)
                println(" pos: [${pos.start}, ${pos.end}]")
            case None => break
        }
    }
}
```

运行结果：

```text
found: 2024-10-24 and groupCount: 3
 pos: [0, 10]
found: 2025-01-01 and groupCount: 3
 pos: [11, 21]
```

### func matchPosition(Int64)

```cangjie
public func matchPosition(group: Int64): Position
```

功能：根据给定的索引获取上一次匹配中该捕获组匹配到的子字符串在输入字符串中的位置信息。

参数：

- group: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定组。

返回值：

- [Position](#struct-position) - 对应捕获组的位置信息。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当未开启捕获组提取，或 group 小于 0 或者大于 groupCount 时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    let iter = r.lazyFindAll("2024-10-24&2025-01-01", group: true)
    while (true) {
        match (iter.next()) {
            case Some(md) =>
                println("found: ${md.matchString()} and groupCount: ${md.groupCount()}")
                /* 月份的捕获组索引为 2 */
                let pos = md.matchPosition(2)
                println(" month: [${pos.start}, ${pos.end}]")
            case None => break
        }
    }
}
```

运行结果：

```text
found: 2024-10-24 and groupCount: 3
 month: [5, 7]
found: 2025-01-01 and groupCount: 3
 month: [16, 18]
```

### func matchPosition(String)

```cangjie
public func matchPosition(group: String): Position
```

功能：根据给定的命名捕获组名称取上一次匹配中该捕获组匹配到的子字符串在输入字符串中的位置信息。

参数：

- group: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定命名捕获组的名称。

返回值：

- [Position](#struct-position) - 对应捕获组的位置信息。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当未开启捕获组提取，或 捕获组名称不存在，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    let iter = r.lazyFindAll("2024-10-24&2025-01-01", group: true)
    while (true) {
        match (iter.next()) {
            case Some(md) =>
                println("found: ${md.matchString()} and groupCount: ${md.groupCount()}")
                let pos = md.matchPosition("year")
                println(" year: [${pos.start}, ${pos.end}]")
            case None => break
        }
    }
}
```

运行结果：

```text
found: 2024-10-24 and groupCount: 3
 year: [0, 4]
found: 2025-01-01 and groupCount: 3
 year: [11, 15]
```

### func matchString()

```cangjie
public func matchString(): String
```

功能：获取上一次匹配到的子字符串，结果与调用 matchString(0) 相同。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 匹配到的子字符串。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r1 = Regex("ab")
    let r2 = Regex("ab", IgnoreCase)
    match (r1.find("aB")) {
        case Some(r) => println(r.matchString())
        case None => println("None")
    }
    match (r2.find("aB")) {
        case Some(r) => println(r.matchString())
        case None => println("None")
    }
}
```

运行结果：

```text
None
aB
```

### func matchString(Int64)

```cangjie
public func matchString(group: Int64): String
```

功能：根据给定的索引获取上一次匹配中该捕获组匹配到的子字符串。

捕获组的索引从 1 开始，索引为 0 表示获取整个正则表达式的匹配结果。

参数：

- group: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定组。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 匹配到的子字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当未开启捕获组提取，或 group 小于 0 或者大于 groupCount 时，抛出异常。

### func matchString(String)

```cangjie
public func matchString(group: String): String
```

功能：根据给定的命名捕获组名称获取上一次匹配中该捕获组匹配到的子字符串。

参数：

- group: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定命名捕获组的名称。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 匹配到的子字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当未开启捕获组提取，或捕获组名称不存在，抛出异常。

## struct Position

```cangjie
public struct Position {
    public let end: Int64
    public let start: Int64
}
```

功能：用来存储位置信息，表示的是一个前闭后开区间。

### let end

```cangjie
public let end: Int64
```

功能：区间结束位置。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### let start

```cangjie
public let start: Int64
```

功能：区间开始位置。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)
