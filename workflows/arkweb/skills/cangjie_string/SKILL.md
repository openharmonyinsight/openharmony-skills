---
name: cangjie-std-string
description: 仓颉标准库 String 类型详细指南。当需要了解 String
  的构造、搜索、替换、分割、拼接、裁剪、大小写转换、编码处理、下标访问、迭代等操作的完整 API 和用法时，应使用此 Skill。
descriptionZH: 仓颉标准库 String 类型详细指南。当需要了解 String
  的构造、搜索、替换、分割、拼接、裁剪、大小写转换、编码处理、下标访问、迭代等操作的完整 API 和用法时，应使用此 Skill。
tags:
  - 仓颉
  - String
---

# 仓颉语言字符串

## 1. 概述

`String` 是仓颉核心包 `std.core` 中的 **struct** 类型，**无需导入** 即可直接使用。

- 不可变值类型（赋值产生副本）
- 仅支持 UTF-8 编码，最大长度为 `UInt32.Max`（约 4 GB）
- 实现接口：`Collection<Byte>`、`Comparable<String>`、`Hashable`、`ToString`

> **注意**：`String` 实现了 `Collection<Byte>`，`for (b in s)` 迭代的是 UTF-8 字节（`Byte` / `UInt8`），而非字符。若要按字符迭代，请使用 `for (r in s.runes())`。

---

## 2. 构造

```cangjie
// 空字符串
let s1 = ""
let s2 = String()
let s3 = String.empty           // 静态常量

// 字符串字面量
let s4 = "Hello, 仓颉!"

// 多行字符串（三引号）
let s5 = """
    第一行
    第二行
    """

// 从 Rune 数组构造
let runes: Array<Rune> = [r'H', r'i']
let s6 = String(runes)          // "Hi"

// 从 Rune 集合构造
let s7 = String(someRuneCollection)

// 从 UTF-8 字节数组构造
let bytes: Array<UInt8> = [72, 101, 108, 108, 111]
let s8 = String.fromUtf8(bytes) // "Hello"（会校验 UTF-8 合法性）
```

---

## 3. 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `size` | `Int64` | UTF-8 编码字节长度（**不是字符数**） |

```cangjie
let s = "Hello"
println(s.size)     // 5

let s2 = "你好"
println(s2.size)    // 6（每个汉字 3 字节 UTF-8）
```

---

## 4. 静态方法

### 4.1 `join` — 拼接字符串数组

```cangjie
static func join(strArr: Array<String>, delimiter!: String = String.empty): String
```

```cangjie
let arr = ["I", "like", "Cangjie"]
let s = String.join(arr, delimiter: " ")
println(s) // "I like Cangjie"

let csv = String.join(["a", "b", "c"], delimiter: ",")
println(csv) // "a,b,c"
```

### 4.2 `fromUtf8` — 从 UTF-8 字节数组构造

```cangjie
static func fromUtf8(utf8Data: Array<UInt8>): String
```

- 校验字节数组是否为合法 UTF-8，非法则抛出 `IllegalArgumentException`

```cangjie
let bytes: Array<UInt8> = [72, 101, 108, 108, 111]
let s = String.fromUtf8(bytes) // "Hello"
```

### 4.3 `fromUtf8Unchecked` — 不校验构造（unsafe）

```cangjie
static func fromUtf8Unchecked(utf8Data: Array<UInt8>): String
```

- 不校验 UTF-8 合法性，性能更好但使用不当会导致未定义行为

### 4.4 `checkUtf8Encoding` — 校验 UTF-8 合法性

```cangjie
static func checkUtf8Encoding(data: Array<UInt8>): Bool
```

```cangjie
let valid = String.checkUtf8Encoding([72, 101]) // true
let invalid = String.checkUtf8Encoding([0xFF, 0xFE]) // false
```

---

## 5. 搜索与检查

### 5.1 `contains` — 包含子串

```cangjie
func contains(str: String): Bool
```

```cangjie
"Hello World".contains("World") // true
"Hello World".contains("world") // false（大小写敏感）
```

### 5.2 `startsWith` / `endsWith` — 前缀/后缀检查

```cangjie
func startsWith(prefix: String): Bool
func endsWith(suffix: String): Bool
```

```cangjie
"hello.cj".startsWith("hello") // true
"hello.cj".endsWith(".cj")     // true
```

### 5.3 `indexOf` — 查找首次出现位置

```cangjie
func indexOf(b: Byte): Option<Int64>
func indexOf(b: Byte, fromIndex: Int64): Option<Int64>
func indexOf(str: String): Option<Int64>
func indexOf(str: String, fromIndex: Int64): Option<Int64>
```

```cangjie
let s = "Hello World"
s.indexOf("World")     // Some(6)
s.indexOf("xyz")       // None
s.indexOf("l")         // Some(2)
s.indexOf("l", 3)      // Some(3)  — 从索引 3 开始搜索
```

### 5.4 `lastIndexOf` — 查找最后出现位置

```cangjie
func lastIndexOf(b: Byte): Option<Int64>
func lastIndexOf(b: Byte, fromIndex: Int64): Option<Int64>
func lastIndexOf(str: String): Option<Int64>
func lastIndexOf(str: String, fromIndex: Int64): Option<Int64>
```

```cangjie
"abcabc".lastIndexOf("abc") // Some(3)
```

### 5.5 `count` — 统计子串出现次数

```cangjie
func count(str: String): Int64
```

```cangjie
"abababab".count("ab") // 4
```

### 5.6 `isEmpty` / `isAscii` / `isAsciiBlank`

```cangjie
func isEmpty(): Bool        // 是否为空串
func isAscii(): Bool        // 是否全为 ASCII 字符
func isAsciiBlank(): Bool   // 是否为空串或仅含 ASCII 空白字符
```

---

## 6. 替换与删除

### 6.1 `replace` — 替换所有匹配子串

```cangjie
func replace(old: String, new: String): String
```

```cangjie
"aabbcc".replace("bb", "XX") // "aaXXcc"
"aaa".replace("a", "bb")     // "bbbbbb"
```

### 6.2 `removePrefix` / `removeSuffix` — 删除前缀/后缀

```cangjie
func removePrefix(prefix: String): String
func removeSuffix(suffix: String): String
```

- 如果字符串不以指定前缀/后缀开头/结尾，返回原字符串

```cangjie
"HelloWorld".removePrefix("Hello") // "World"
"HelloWorld".removeSuffix("World") // "Hello"
"HelloWorld".removePrefix("xyz")   // "HelloWorld"
```

---

## 7. 分割

### 7.1 `split` — 按分隔符分割

```cangjie
func split(str: String, removeEmpty!: Bool = false): Array<String>
func split(str: String, maxSplits: Int64, removeEmpty!: Bool = false): Array<String>
```

```cangjie
"a,b,,c".split(",")                    // ["a", "b", "", "c"]
"a,b,,c".split(",", removeEmpty: true) // ["a", "b", "c"]
"a,b,c,d".split(",", 2)               // ["a", "b", "c,d"]  — 最多分割 2 次
```

### 7.2 `lazySplit` — 惰性分割（返回迭代器）

```cangjie
func lazySplit(str: String, removeEmpty!: Bool = false): Iterator<String>
func lazySplit(str: String, maxSplits: Int64, removeEmpty!: Bool = false): Iterator<String>
```

- 与 `split` 功能相同，但返回 `Iterator<String>`，适合处理大字符串时避免一次性分配

### 7.3 `lines` — 按行分割

```cangjie
func lines(): Iterator<String>
```

```cangjie
let text = "line1\nline2\nline3"
for (line in text.lines()) {
    println(line)
}
// 输出：
// line1
// line2
// line3
```

---

## 8. 裁剪（Trim）

### 8.1 ASCII 空白裁剪

```cangjie
func trimAscii(): String       // 两端裁剪 ASCII 空白
func trimAsciiStart(): String  // 裁剪前导 ASCII 空白
func trimAsciiEnd(): String    // 裁剪尾部 ASCII 空白
```

```cangjie
"  hello  ".trimAscii()      // "hello"
"  hello  ".trimAsciiStart() // "hello  "
"  hello  ".trimAsciiEnd()   // "  hello"
```

### 8.2 自定义裁剪

```cangjie
// 按 Rune 数组裁剪（移除集合中的任意字符）
func trimStart(chars: Array<Rune>): String
func trimEnd(chars: Array<Rune>): String

// 按字符串裁剪（移除前缀/后缀子串的重复出现）
func trimStart(str: String): String
func trimEnd(str: String): String

// 按谓词裁剪（移除满足条件的字符）
func trimStart(predicate: (Rune) -> Bool): String
func trimEnd(predicate: (Rune) -> Bool): String
```

```cangjie
"xxxHelloxxx".trimStart([r'x'])              // "Helloxxx"
"xxxHelloxxx".trimEnd([r'x'])                // "xxxHello"
"123abc456".trimStart { r => r >= r'0' && r <= r'9' } // "abc456"
```

---

## 9. 填充（Pad）

```cangjie
func padStart(totalWidth: Int64, padding!: String = " "): String
func padEnd(totalWidth: Int64, padding!: String = " "): String
```

- `totalWidth` 为目标字节宽度
- 如果原字符串长度已 ≥ `totalWidth`，返回原字符串

```cangjie
"42".padStart(6)           // "    42"
"42".padStart(6, padding: "0") // "000042"
"42".padEnd(6)             // "42    "
"42".padEnd(6, padding: ".")  // "42...."
```

---

## 10. 大小写转换

```cangjie
func toAsciiLower(): String   // 转小写（仅 ASCII 字母）
func toAsciiUpper(): String   // 转大写（仅 ASCII 字母）
func toAsciiTitle(): String   // 首字母大写（仅 ASCII 字母）
```

```cangjie
"Hello World".toAsciiLower() // "hello world"
"Hello World".toAsciiUpper() // "HELLO WORLD"
"hello world".toAsciiTitle() // "Hello World"
```

---

## 11. 比较

```cangjie
func compare(other: String): Ordering   // 字典序比较，返回 Ordering.LT/EQ/GT
func equalsIgnoreAsciiCase(other: String): Bool  // 忽略 ASCII 大小写比较
```

```cangjie
"abc".compare("abd")                     // Ordering.LT
"Hello".equalsIgnoreAsciiCase("hello")   // true
```

### 运算符比较

```cangjie
"abc" == "abc"  // true
"abc" != "def"  // true
"abc" < "abd"   // true（字典序）
"abc" <= "abc"  // true
"abd" > "abc"   // true
"abd" >= "abc"  // true
```

---

## 12. 拼接与重复

### 12.1 `+` 运算符 — 字符串拼接

```cangjie
let s = "Hello" + ", " + "World!" // "Hello, World!"
```

### 12.2 `*` 运算符 — 重复

```cangjie
let s = "ab" * 3  // "ababab"
let line = "-" * 20  // "--------------------"
```

### 12.3 字符串插值 `"${expr}"`

```cangjie
let name = "Cangjie"
let age = 3
let s = "Name: ${name}, Age: ${age}" // "Name: Cangjie, Age: 3"
```

### 12.4 `String.join` — 拼接数组

```cangjie
let parts = ["2024", "06", "15"]
let date = String.join(parts, delimiter: "-") // "2024-06-15"
```

### 12.5 `StringBuilder` — 高效拼接

大量拼接时建议使用 `StringBuilder`：

```cangjie
let sb = StringBuilder()
sb.append("Hello")
sb.append(", ")
sb.append("World!")
let result = sb.toString() // "Hello, World!"
```

---

## 13. 转换

### 13.1 转为字节数组

```cangjie
func toArray(): Array<Byte>      // 返回 UTF-8 字节数组（拷贝）
func rawData(): Array<Byte>      // 返回内部原始数据引用（unsafe）
```

```cangjie
let bytes = "Hi".toArray()   // [72, 105]
```

### 13.2 转为 Rune 数组

```cangjie
func toRuneArray(): Array<Rune>
```

```cangjie
let runes = "Hi你".toRuneArray() // [r'H', r'i', r'你']
```

### 13.3 迭代

```cangjie
func iterator(): Iterator<Byte>   // 按字节迭代
func runes(): Iterator<Rune>      // 按字符（Rune）迭代
```

```cangjie
// 按字符迭代
for (r in "Hello 仓颉".runes()) {
    print(r)
}

// 按字节迭代
for (b in "Hello") {
    print(b)  // 输出 UTF-8 字节值
}
```

### 13.4 `toString`

```cangjie
func toString(): String  // 返回自身
```

### 13.5 `hashCode`

```cangjie
func hashCode(): Int64  // 返回哈希值，可用于 HashMap 等
```

---

## 14. 下标访问与切片

### 14.1 按字节索引

```cangjie
let s = "Hello"
let b: Byte = s[0]         // 72 (H 的 UTF-8 编码)
let opt = s.get(10)         // None（安全访问，不抛异常）
```

> **注意**：`s[i]` 返回的是 `Byte`（UTF-8 编码字节），对于多字节字符（如中文），单个索引不能获取完整字符。

### 14.2 切片

```cangjie
let s = "Hello World"
let sub = s[0..5]   // "Hello"
let sub2 = s[6..11] // "World"
```

> **注意**：切片范围基于字节索引，确保不要在多字节字符中间切断。

---

## 15. `clone`

```cangjie
func clone(): String
```

- 返回字符串的一份拷贝（由于 `String` 是不可变类型，通常不需要手动克隆）

---

## 16. 常见用法总结

```cangjie
// 1. 判断空字符串
if (s.isEmpty()) { ... }

// 2. 安全搜索
if (let Some(idx) <- s.indexOf("key")) {
    println("Found at ${idx}")
}

// 3. 分割与重组
let parts = "a:b:c".split(":")
let joined = String.join(parts, delimiter: "-") // "a-b-c"

// 4. 裁剪用户输入
let input = "  user@example.com  ".trimAscii()

// 5. 路径处理
let filename = "path/to/file.cj"
if (filename.endsWith(".cj")) {
    let name = filename.removeSuffix(".cj")
}

// 6. 按行处理文本
for (line in text.lines()) {
    if (!line.isEmpty()) {
        processLine(line)
    }
}

// 7. 字符串重复
let separator = "=" * 40  // "========================================"

// 8. 大小写不敏感比较
if (cmd.equalsIgnoreAsciiCase("quit")) {
    exit(0)
}
```
