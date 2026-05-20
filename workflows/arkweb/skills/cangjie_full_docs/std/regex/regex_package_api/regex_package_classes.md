# 类

## class Matcher <sup>(deprecated)</sup>

```cangjie
public class Matcher {
    public init(regex: Regex, input: String)
}
```

功能：正则匹配器，用于扫描输入序列并进行匹配。

> **注意：**
>
> 未来版本即将废弃，使用 [Regex](#class-regex) 替代。

### init(Regex, String)

```cangjie
public init(regex: Regex, input: String)
```

功能：使用传入的正则表达式和输入序列创建 [Matcher](#class-matcher-deprecated) 实例。

参数：

- regex: [Regex](regex_package_classes.md#class-regex) - 正则表达式。
- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 输入序列。

### func allCount()

```cangjie
public func allCount(): Int64
```

功能：获取正则表示式的匹配结果总数。

默认是从头到尾匹配的结果，使用了 setRegion 后只会在设置的范围内查找。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 匹配结果总数。

### func find()

```cangjie
public func find(): Option<MatchData>
```

功能：自当前字符串偏移位置起，查找第一个匹配到的子序列。

find 调用一次，当前偏移位置为最新一次匹配到的子序列后第一个字符位置，下次调用时，find 从当前位置开始匹配。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)> - 匹配到结果返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>，如果匹配不到，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>.None。

异常：

- [RegexException](regex_package_exceptions.md#class-regexexception) - 当存在匹配但提取匹配信息失败时，抛出异常。

### func find(Int64)

```cangjie
public func find(index: Int64): Option<MatchData>
```

功能：重置该匹配器索引位置，从 index 对应的位置处开始对输入序列进行匹配，返回匹配到的子序列。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)> - 匹配到结果返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>，如果匹配不到，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>.None。

异常：

- [IndexOutOfBoundsException](../../core/core_package_api/core_package_exceptions.md#class-indexoutofboundsexception) - 当 index 小于 0，或 index 大于等于输入序列的 size 时，抛出异常。
- [RegexException](regex_package_exceptions.md#class-regexexception) - 当存在匹配但提取匹配信息失败时，抛出异常。

### func findAll()

```cangjie
public func findAll(): Option<Array<MatchData>>
```

功能：对整个输入序列进行匹配，查找所有匹配到的子序列。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[MatchData](regex_package_structs.md#struct-matchdata)>> - 如果匹配到结果，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[MatchData](regex_package_structs.md#struct-matchdata)>>；如果匹配不到，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[MatchData](regex_package_structs.md#struct-matchdata)>>.None。

异常：

- [RegexException](regex_package_exceptions.md#class-regexexception) - 当存在匹配但提取匹配信息失败时，抛出异常。

### func fullMatch()

```cangjie
public func fullMatch(): Option<MatchData>
```

功能：对整个输入序列进行匹配。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)> - 如果全部匹配成功，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>；否则返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>.None。

异常：

- [RegexException](regex_package_exceptions.md#class-regexexception) - 当存在匹配但提取匹配信息失败时，抛出异常。

### func getString()

```cangjie
public func getString(): String
```

功能：获取匹配序列。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 匹配序列。

### func matchStart()

```cangjie
public func matchStart(): Option<MatchData>
```

功能：对输入序列的头部进行匹配。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)> - 如果匹配成功，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>；否则返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>.None。

异常：

- [RegexException](regex_package_exceptions.md#class-regexexception) - 当存在匹配但提取匹配信息失败时，抛出异常。

### func region()

```cangjie
public func region(): Position
```

功能：返回匹配器的区域设置。

返回值：

- [Position](regex_package_structs.md#struct-position) - 匹配器的区域设置。

### func replace(String)

```cangjie
public func replace(replacement: String): String
```

功能：自当前字符串偏移位置起，匹配到的第一个子序列替换为目标字符串，并将当前索引位置设置到匹配子序列的下一个位置。

参数：

- replacement: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定替换字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 替换后字符串。

### func replace(String, Int64)

```cangjie
public func replace(replacement: String, index: Int64): String
```

功能：从输入序列的 index 位置起匹配正则，将匹配到的第一个子序列替换为目标字符串。

参数：

- replacement: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定替换字符串。
- index: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 匹配开始位置。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 替换后字符串。

异常：

- [IndexOutOfBoundsException](../../core/core_package_api/core_package_exceptions.md#class-indexoutofboundsexception) - 当 index 小于 0，或 index 大于等于输入序列的 size 时，抛出异常。

### func replaceAll(String)

```cangjie
public func replaceAll(replacement: String): String
```

功能：将输入序列中所有与正则匹配的子序列替换为给定的目标字符串。

参数：

- replacement: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定替换字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 替换后的字符串。

### func replaceAll(String, Int64)

```cangjie
public func replaceAll(replacement: String, limit: Int64): String
```

功能：将输入序列中与正则匹配的前 limit 个子序列替换为给定的替换字符串。

参数：

- replacement: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定替换字符串。
- limit: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 替换次数。如果 limit 等于 0，返回原来的序列；如果 limit 为负数，将尽可能多次的替换。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 替换后字符串。

### func resetRegion()

```cangjie
public func resetRegion(): Matcher
```

功能：重置匹配器开始位置和结束位置。

返回值：

- [Matcher](#class-matcher-deprecated) - 匹配器自身。

### func resetString(String)

```cangjie
public func resetString(input: String): Matcher
```

功能：重设匹配序列，并重置匹配器。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 新的匹配序列。

返回值：

- [Matcher](#class-matcher-deprecated) - 匹配器自身。

### func setRegion(Int64, Int64)

```cangjie
public func setRegion(beginIndex: Int64, endIndex: Int64): Matcher
```

功能：设置匹配器可搜索区域的位置信息，具体位置由指定的 begin 和 end 决定。

参数：

- beginIndex: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 区域开始位置。
- endIndex: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 区域结束位置。

返回值：

- [Matcher](#class-matcher-deprecated) - 匹配器自身。

异常：

- [IndexOutOfBoundsException](../../core/core_package_api/core_package_exceptions.md#class-indexoutofboundsexception) - 当 beginIndex 小于 0，或 beginIndex 大于输入序列的 size 时，抛出异常；当 endIndex 小于 0，或 endIndex 大于输入序列的 size 时，抛出异常；当 beginIndex 大于 endIndex 时，抛出异常。

### func split()

```cangjie
public func split(): Array<String>
```

功能：将给定的输入序列根据正则尽可能的分割成多个子序列。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 子序列数组。

### func split(Int64)

```cangjie
public func split(limit: Int64): Array<String>
```

功能：将给定的输入序列根据正则尽可能的分割成多个子序列 （最多分割成 limit 个子串）。

参数：

- limit: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 最多分割的子串个数。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 如果 limit>0，返回最多 limit 个子串；如果 limit<=0，返回最大可分割数个子串。

## class Regex

```cangjie
public class Regex {
    public init(pattern: String, flags: Array<RegexFlag>)
    public init(pattern: String, option: RegexOption)
}
```

功能：用来指定编译类型并创建正则表达式实例。

正则匹配规则详见 [regex 规则集](../regex_package_overview.md#regex-规则集)。

### init(String, Array\<RegexFlag>)

```cangjie
public init(pattern: String, flags: Array<RegexFlag>)
```

功能：创建 [Regex](regex_package_classes.md#class-regex) 实例。

参数：

- pattern: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 正则表达式。
- flags: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[RegexFlag](regex_package_enums.md#enum-regexflag)> - 正则匹配的模式列表。

异常：

- [RegexException](regex_package_exceptions.md#class-regexexception) - 当初始化失败时，抛出异常。

### init(String, RegexOption) <sup>(deprecated)</sup>

```cangjie
public init(pattern: String, option: RegexOption)
```

功能：使用指定的模式创建一个 [Regex](regex_package_classes.md#class-regex) 实例。

> **注意：**
>
> 未来版本即将废弃，使用 [init(String, Array\<RegexFlag>)](#initstring-arrayregexflag) 替代。

参数：

- pattern: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 正则表达式。
- option: [RegexOption](#class-regexoption-deprecated) - 正则匹配的模式。

异常：

- [RegexException](regex_package_exceptions.md#class-regexexception) - 当初始化失败时，抛出异常。

### func find(String, Bool)

```cangjie
public func find(input: String, group!: Bool = false): Option<MatchData>
```

功能：查找第一个匹配到的子序列。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待匹配序列。
- group!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 指定是否开启捕获组的提取。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)> - 匹配到结果返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>，如果匹配不到，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[MatchData](regex_package_structs.md#struct-matchdata)>.None。

异常：

- [RegexException](regex_package_exceptions.md#class-regexexception) - 当存在匹配但提取匹配信息失败时，抛出异常。

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

### func findAll(String, Bool)

```cangjie
public func findAll(input: String, group!: Bool = false): Array<MatchData>
```

功能：对整个输入序列进行匹配，查找所有匹配到的子序列。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待匹配序列。
- group!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 指定是否开启捕获组的提取。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[MatchData](regex_package_structs.md#struct-matchdata)> - 存储匹配结果的数组，如果未匹配到，数组为空。

异常：

- [RegexException](regex_package_exceptions.md#class-regexexception) - 当存在匹配但提取匹配信息失败时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex("ab")
    let arr = r.findAll("ababaaab")
    let iter = arr.iterator()
    println(arr.size)
    while (true) {
        match (iter.next()) {
            case Some(i) => println(i.matchString())
            case None => break
        }
    }
}
```

运行结果：

```text
3
ab
ab
ab
```

### func getNamedGroups()

```cangjie
public func getNamedGroups(): Map<String, Int64>
```

功能：获取命名捕获组的名称与索引映射。

返回值：

- [Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v)\<[String](../../core/core_package_api/core_package_structs.md#struct-string), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> - 命名捕获组的名称与索引映射。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    let arr = r.findAll("2024-10-24&2025-01-01", group: true)
    for (md in arr) {
        println("found: `${md.matchString()}` and groupCount: ${md.groupCount()}")
        for ((name, index) in r.getNamedGroups()) {
            println(" ${name} => ${index}")
        }
    }
}
```

运行结果：

```text
found: `2024-10-24` and groupCount: 3
 day => 3
 month => 2
 year => 1
found: `2025-01-01` and groupCount: 3
 day => 3
 month => 2
 year => 1
```

### func lazyFindAll(String, Bool)

```cangjie
public func lazyFindAll(input: String, group!: Bool = false): Iterator<MatchData>
```

功能：对整个输入序列进行匹配，获取匹配的迭代器。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待匹配序列。
- group!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 指定是否开启捕获组的提取。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<[MatchData](regex_package_structs.md#struct-matchdata)> - 匹配的迭代器。

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
                println("found: `${md.matchString()}` and groupCount: ${md.groupCount()}")
                for ((name, index) in r.getNamedGroups()) {
                    println(" ${name} => ${index}")
                }
            case None => break
        }
    }
}
```

运行结果：

```text
found: `2024-10-24` and groupCount: 3
 day => 3
 month => 2
 year => 1
found: `2025-01-01` and groupCount: 3
 day => 3
 month => 2
 year => 1
```

### func matcher(String) <sup>(deprecated)</sup>

```cangjie
public func matcher(input: String): Matcher
```

功能：创建匹配器。

> **注意：**
>
> 未来版本即将废弃。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要匹配的字符串。

返回值：

- [Matcher](#class-matcher-deprecated) - 创建的匹配器。

### func matches(String)

```cangjie
public func matches(input: String): Bool
```

功能：判断入参 input 与正则表达式是否存在匹配。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要匹配的字符串。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果存在匹配，返回 true，否则返回 false。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    println(r.matches("2024-10-24&2025-01-01"))
}
```

运行结果：

```text
true
```

### func replace(String, String)

```cangjie
public func replace(input: String, replacement: String): String
```

功能：自当前字符串起始位置开始，匹配到的第一个子序列替换为目标字符串。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待匹配序列。
- replacement: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定替换字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 替换后字符串。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    println(r.replace("2024-10-24&2025-01-01", "time"))
}
```

运行结果：

```text
time&2025-01-01
```

### func replace(String, String, Int64)

```cangjie
public func replace(input: String, replacement: String, index: Int64): String
```

功能：从输入序列的 index 位置起匹配正则，将匹配到的第一个子序列替换为目标字符串。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待匹配序列。
- replacement: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定替换字符串。
- index: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 匹配开始位置。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 替换后字符串。

异常：

- [IndexOutOfBoundsException](../../core/core_package_api/core_package_exceptions.md#class-indexoutofboundsexception) - 当 index 小于 0，或 index 大于等于输入序列的 size 时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    println(r.replace("2024-10-24&2025-01-01", "time", 10))
}
```

运行结果：

```text
2024-10-24&time
```

### func replaceAll(String, String)

```cangjie
public func replaceAll(input: String, replacement: String): String
```

功能：将输入序列中所有与正则匹配的子序列替换为给定的目标字符串。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待匹配序列。
- replacement: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定替换字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 替换后的字符串。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    println(r.replaceAll("2024-10-24&2025-01-01", "time"))
}
```

运行结果：

```text
time&time
```

### func replaceAll(String, String, Int64)

```cangjie
public func replaceAll(input: String, replacement: String, limit: Int64): String
```

功能：将输入序列中与正则匹配的前 limit 个子序列替换为给定的替换字符串。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待匹配序列。
- replacement: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定替换字符串。
- limit: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 替换次数。如果 limit 等于 0，返回原来的序列；如果 limit 为负数，将尽可能多次的替换。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 替换后字符串。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    println(r.replaceAll("2019-4-5&2024-10-24&2025-01-01", "time", 10))
}
```

运行结果：

```text
2019-4-5&time&time
```

### func split(String)

```cangjie
public func split(input: String): Array<String>
```

功能：将给定的输入序列根据正则尽可能的分割成多个子序列。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待匹配序列。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 子序列数组。

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex("&")
    for (subStr in r.split("2019-4-5&2024-10-24&2025-01-01")) {
        println(subStr)
    }
}
```

运行结果：

```text
2019-4-5
2024-10-24
2025-01-01
```

### func split(String, Int64)

```cangjie
public func split(input: String, limit: Int64): Array<String>
```

功能：将给定的输入序列根据正则尽可能的分割成多个子序列 （最多分割成 limit 个子串）。

参数：

- input: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待匹配序列。
- limit: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 最多分割的子串个数。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 如果 limit>0，返回最多 limit 个子串；如果 limit<=0，返回最大可分割数个子串。

### func string()

```cangjie
public func string(): String
```

功能：获取正则的输入序列。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 输入序列。

## class RegexOption <sup>(deprecated)</sup>

```cangjie
public class RegexOption <: ToString {
    public init()
}
```

功能：用于指定正则匹配的模式。

> **注意：**
>
> 未来版本即将废弃，使用 [RegexFlag](regex_package_enums.md#enum-regexflag) 替代。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### init()

```cangjie
public init()
```

功能：创建一个 [RegexOption](#class-regexoption-deprecated) 实例， 匹配模式为普通模式（NORMAL）。

### func ignoreCase()

```cangjie
public func ignoreCase(): RegexOption
```

功能：修改 [RegexOption](#class-regexoption-deprecated)，修改匹配模式为忽略大小写（IGNORECASE）。

返回值：

- [RegexOption](#class-regexoption-deprecated) - 修改后的 [RegexOption](#class-regexoption-deprecated)。

### func multiLine()

```cangjie
public func multiLine(): RegexOption
```

功能：修改 [RegexOption](#class-regexoption-deprecated)，修改匹配模式为多行文本模式（MULTILINE）。

返回值：

- [RegexOption](#class-regexoption-deprecated) - 修改后的 [RegexOption](#class-regexoption-deprecated)。

### func toString()

```cangjie
public func toString(): String
```

功能：获取 [RegexOption](#class-regexoption-deprecated) 当前表示的正则匹配模式。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 正则匹配模式。
