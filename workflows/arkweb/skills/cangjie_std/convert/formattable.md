# 仓颉标准库格式化字串 Skill

> 导入：`import std.convert.*`

---

## 1. Formattable 接口

```cangjie
public interface Formattable {
    func format(fmt: String): String
}
```

### 已实现类型

Int8, Int16, Int32, Int64, UInt8, UInt16, UInt32, UInt64, Float16, Float32, Float64, Rune

---

## 2. 格式化参数语法

```text
format_spec := [flags][width][.precision][specifier]
```

### 2.1 flags

| 标志 | 适用类型 | 说明 |
|------|----------|------|
| `-` | Int/UInt/Float/Rune | 左对齐 |
| `+` | Int/UInt/Float | 正数显示 `+` 号 |
| `#` | Int/UInt | 进制前缀（`0b`/`0o`/`0x`） |
| `0` | Int/UInt/Float | 空位补零 |

### 2.2 width — 最小宽度

正整数，不足补空格（默认右对齐），不会截断。

### 2.3 precision — 精度

- **浮点数**：小数点后位数（默认 6 位），四舍五入
- **整数**：不足位数前补 `0`

### 2.4 specifier — 格式说明符

| 说明符 | 适用类型 | 说明 |
|--------|----------|------|
| `b`/`B` | Int/UInt | 二进制 |
| `o`/`O` | Int/UInt | 八进制 |
| `x`/`X` | Int/UInt | 十六进制（小写/大写） |
| `e`/`E` | Float | 科学计数法 |
| `g`/`G` | Float | 自动选择十进制或科学计数法 |

---

## 3. 用法示例

### 3.1 整数格式化

```cangjie
import std.convert.*

main() {
    var a: Int32 = 20

    // 进制转换
    println(a.format("b"))         // "10100"（二进制）
    println(a.format("o"))         // "24"（八进制）
    println(a.format("x"))         // "14"（十六进制）
    println(a.format("#X"))        // "0X14"（带前缀大写十六进制）

    // 宽度与对齐
    println("\"${a.format("10")}\"")    // "        20"（右对齐，宽度10）
    println("\"${a.format("-10")}\"")   // "20        "（左对齐）

    // 正号与补零
    println("\"${a.format("+10")}\"")   // "       +20"
    println("\"${a.format("010")}\"")   // "0000000020"

    // 精度（整数前补零）
    println("\"${a.format(".8")}\"")    // "00000020"
}
```

### 3.2 浮点数格式化

```cangjie
import std.convert.*

main() {
    var f: Float64 = 1234.5

    // 默认 6 位小数
    println(f.format(""))              // "1234.500000"

    // 指定精度
    println(f.format(".2"))            // "1234.50"

    // 宽度 + 精度
    println("\"${f.format("15.2")}\"") // "        1234.50"

    // 科学计数法
    println(f.format(".2e"))           // "1.23e+03"
    println(f.format("G"))            // "1234.5"（G 自动选择精简表示）

    // 补零
    println("\"${f.format("012.2")}\"") // "000001234.50"
}
```

### 3.3 字符格式化

```cangjie
import std.convert.*

main() {
    var c: Rune = 'A'
    println("\"${c.format("5")}\"")    // "    A"（右对齐）
    println("\"${c.format("-5")}\"")   // "A    "（左对齐）
}
```

### 3.4 自定义类型实现 Formattable

```cangjie
import std.convert.*

class Point <: Formattable {
    var x: Float64
    var y: Float64

    init(x: Float64, y: Float64) {
        this.x = x
        this.y = y
    }

    public func format(fmt: String): String {
        "(${x.format(fmt)}, ${y.format(fmt)})"
    }
}

main() {
    let p = Point(3.14159, 2.71828)
    println(p.format(".2"))  // "(3.14, 2.72)"
}
```

---

## 4. 常见用法总结

```cangjie
import std.convert.*

main() {
    // 1. 十六进制地址显示
    let addr: UInt64 = 48879
    println("0x${addr.format("08X")}")           // "0x0000BEEF"

    // 2. 表格对齐输出
    let items = [("Apple", 3), ("Banana", 12), ("Cherry", 150)]
    for ((name, count) in items) {
        let countStr = count.format("-6")
        println("${name}: ${countStr}")
    }

    // 3. 浮点精度控制
    let pi: Float64 = 3.14159265358979
    println("pi ≈ ${pi.format(".4")}")           // "pi ≈ 3.1416"

    // 4. 二进制位查看
    let flags: Int32 = 0xAB
    println(flags.format("010b"))                // "0010101011"
}
```
