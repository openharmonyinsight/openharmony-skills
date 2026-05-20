# Regex 示例

## Regex 匹配大小写

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

## Regex 匹配多行

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let rule = ##"^(\w+)\s(\d+)*$"##
    let input: String = """
Joe 164
Sam 208
Allison 211
Gwen 171
"""

    let r = Regex(rule, MultiLine)
    var arr = r.findAll(input)
    for (md in arr) {
        println(md.matchString())
    }
}
```

运行结果：

```text
Joe 164
Sam 208
Allison 211
Gwen 171
```

## Regex 匹配 Unicode

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let printMatchData: (MatchData) -> Unit = {
        md =>
        println("found: `${md.matchString()}`")
        let pos = md.matchPosition()
        println("[${pos.start}, ${pos.end})")
    }

    let unicodePattern = "(?:[\u{2460}\u{2461}\u{2462}\u{2463}\u{2464}\u{2465}\u{2466}\u{2467}\u{2468}]{2,4})"
    let unicodeInput = "\u{2460}\u{2461}  \u{2464}\u{2465}"

    println("#Unicode disabled: ")
    try {
        for (md in Regex(unicodePattern).lazyFindAll(unicodeInput)) {
            printMatchData(md)
        }
    } catch (e: IllegalArgumentException) {
        println(e)
    }
    println("\n#Unicode enabled: ")
    for (md in Regex(unicodePattern, Unicode).lazyFindAll(unicodeInput)) {
        printMatchData(md)
    }

    println("\n#Unicode enabled with literals: ")
    let unicodeLiteralPattern = "(?:[①②③④⑤⑥⑦⑧⑨]{2,4})"
    let unicodeLiteralInput = "①②  ⑤⑥"
    for (md in Regex(unicodeLiteralPattern, Unicode).lazyFindAll(unicodeLiteralInput)) {
        printMatchData(md)
    }
}
```

运行结果：

```text
#Unicode disabled: 
IllegalArgumentException: Invalid utf8 byte sequence.

#Unicode enabled: 
found: `①②`
[0, 6)
found: `⑤⑥`
[8, 14)

#Unicode enabled with literals: 
found: `①②`
[0, 6)
found: `⑤⑥`
[8, 14)
```

## Regex 和 MatchData 的使用

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex(#"a\wa"#)
    for (md in r.findAll("1aba12ada555")) {
        println(md.matchString())
        let pos = md.matchPosition()
        println("[${pos.start}, ${pos.end})")
    }
}
```

运行结果：

```text
aba
[1, 4)
ada
[6, 9)
```

## Regex 中 replace/replaceAll 函数

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    let r = Regex("\\d")

    /* 用 X 替换第一个数字 */
    println(r.replace("a1b1c2d3f4", "X"))

    /* 用 X 替换 index 为 2 之后出现的第一个数字 */
    println(r.replace("a1b1c2d3f4", "X", 2))

    /* 用 X 替换所有数字 */
    println(r.replaceAll("a1b1c2d3f4", "X"))

    /* 用 X 替换 index 为 2 之后出现的所有数字 */
    println(r.replaceAll("a1b1c2d3f4", "X", 2))

    /* 用 X 替换所有数字 */
    println(r.replaceAll("a1b1c2d3f4", "X", -1))
}
```

运行结果：

```text
aXb1c2d3f4
a1bXc2d3f4
aXbXcXdXfX
aXbXc2d3f4
aXbXcXdXfX
```

## MatchData 中捕获组的使用

示例：

<!-- verify -->
```cangjie
import std.regex.*

main(): Unit {
    var r = Regex(#"(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})"#)
    for (md in r.lazyFindAll("2024-10-24&2025-01-01", group: true)) {
        println("# found: `${md.matchString()}` and groupCount: ${md.groupCount()}")
        if (md.groupCount() > 0) {
            for (i in 0..=md.groupCount()) {
                println("group[${i}] : ${md.matchString(i)}")
                let pos = md.matchPosition(i)
                println("position : [${pos.start}, ${pos.end})")
            }
        }
        for ((name, index) in r.getNamedGroups()) {
            let pos = md.matchPosition(name)
            println("${name} 是第 ${index} 组, position: [${pos.start}, ${pos.end}), 捕获: ${md.matchString(name)}")
        }
    }
}
```

运行结果：

```text
# found: `2024-10-24` and groupCount: 3
group[0] : 2024-10-24
position : [0, 10)
group[1] : 2024
position : [0, 4)
group[2] : 10
position : [5, 7)
group[3] : 24
position : [8, 10)
day 是第 3 组, position: [8, 10), 捕获: 24
month 是第 2 组, position: [5, 7), 捕获: 10
year 是第 1 组, position: [0, 4), 捕获: 2024
# found: `2025-01-01` and groupCount: 3
group[0] : 2025-01-01
position : [11, 21)
group[1] : 2025
position : [11, 15)
group[2] : 01
position : [16, 18)
group[3] : 01
position : [19, 21)
day 是第 3 组, position: [19, 21), 捕获: 01
month 是第 2 组, position: [16, 18), 捕获: 01
year 是第 1 组, position: [11, 15), 捕获: 2025
```
