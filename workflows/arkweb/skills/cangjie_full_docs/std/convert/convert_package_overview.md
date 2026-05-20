# std.convert

## 功能介绍

convert 包提供从字符串转到特定类型的 Convert 系列函数。

例如字符串 "true" 到布尔类型 `true` 的转换以及字符串 "123" 到整数类型 `123` 的转换等。

convert 包提供格式化能力，主要为将仓颉类型实例转换为格式化字符串。

定义了接口 Formattable，用于规定统一的格式化方法，并为 Int8、Int16 等一系列仓颉类型实现了该接口，用户也可以自行为其他类型实现该接口以获取格式化功能。

将仓颉类型转换为字符串时，可根据格式化参数规定字符串格式，如宽度、对齐方式等。（在 Formattable 接口定义的方法中，格式化参数将作为函数入参。）

格式化参数的详细语法说明如下：

```text
format_spec := [flags][width][.precision][specifier]
flags := '-' | '+' | '#' | '0'
width := integer
precision := integer
specifier := 'b' | 'B' | 'o' | 'O' | 'x' | 'X' | 'e' | 'E' | 'g' | 'G'
```

参数 flags：

- '-' 适用于 Int，UInt，Rune 和 Float，表示左对齐。

    代码如下:

    ```cangjie
    import std.convert.*

    main() {
        var c : Int32 = -20
        print("\"${c.format("-10")}\"")
    }
    ```

    运行结果：

    ```text
    "-20       "
    ```

- '+' 适用于 Int，UInt 和 Float，如果数值为正数则打出 '+' 符号，如果数值为负数则忽略。

    代码如下:

    ```cangjie
    import std.convert.*

    main() {
        var c: Int32 = 20
        print("\"${c.format("+10")}\"")
    }
    ```

    运行结果：

    ```text
    "       +20"
    ```

- '#' 是针对进制打印的，对于二进制打印会补充一个 '0b' 或者 '0B'，对于八进制打印会补充一个 '0o' 或者 '0O'，对于十六进制会补充 '0x' 或者 '0X'。

    代码如下:

    ```cangjie
    import std.convert.*

    main() {
        var c: Int32 = 1
        print("\"${c.format("#10x")}\"")
    }
    ```

    运行结果：

    ```text
    "       0x1"
    ```

- '0' 适用于 Int，UInt 和 Float，在空位补充 0。

    代码如下:

    ```cangjie
    import std.convert.*

    main() {
        var c: Int32 = -20
        print("\"${c.format("010")}\"")
    }
    ```

    运行结果：

    ```text
    "-000000020"
    ```

参数 width 宽度：

- 宽度为正整数，适用于 Int，UInt，Rune 和 Float，宽度前有负号则表示左对齐，没有负号则是右对齐，如果数值小于数值本身的长度，不会发生截断。
  如果前缀有 `+` 或 `-` 符号会占用一个字符位，如果前缀有 `0x` 或 `0o` 等会占用两个字符位。

    代码如下:

    ```cangjie
    import std.convert.*

    main() {
        var c: Int32 = 20
        println("\"${c.format("1")}\"")
        println("\"${c.format("+4")}\"")
    }
    ```

    运行结果：

    ```text
    "20"
    " +20"
    ```

参数 precision 精度:

- 精度为正整数，适用于 Int，UInt 和 Float。
  对于浮点数表示小数点后的有效数字位数，如果不指定，那么则打印六位小数，如果小于数值本身有效数字的长度，那就四舍五入，如果大于就补全，补全的不一定是 0。

- 对于整数类型，不指定或者指定的数字小于数值本身的长度，则无效果，如果大于数值本身的长度，则在前面补全'0'。

    代码如下:

    ```cangjie
    import std.convert.*

    main() {
        var e: Float32 = 1234.1
        println("\"${e.format("20.20")}\"")
        var c: Int32 = -20
        println("\"${c.format("10.8")}\"")
    }
    ```

    运行结果：

    ```text
    "1234.09997558593750000000"
    " -00000020"
    ```

参数 specifier:

- 'b' | 'B' | 'o' | 'O' | 'x' | 'X' 适用于 Int 和 UInt 类型。

  'b' | 'B' : 表示二进制格式打印

  'o' | 'O' : 表示八进制格式打印

  'x' | 'X' : 表示十六进制格式打印

    代码如下:

    ```cangjie
    import std.convert.*

    main() {
        var a = 20
        println("\"${a.format("b")}\"")
        println("\"${a.format("o")}\"")
        println("\"${a.format("x")}\"")
        println("\"${a.format("X")}\"")
        println("\"${a.format("#X")}\"")
    }
    ```

    运行结果：

    ```text
    "10100"
    "24"
    "14"
    "14"
    "0X14"
    ```

- 'e' | 'E' | 'g' | 'G' 适用于 Float 类型。

  'e' | 'E' : 科学计数法，小写和大写

  'g' | 'G' : general，用十进制或者科学计数法表示，会选择精简的表示方式进行打印

    代码如下:

    ```cangjie
    import std.convert.*

    main() {
        var f: Float32 = 1234.1
        var c: Float32 = 123412341234.1
        println("\"${f.format("20.2e")}\"")
        println("\"${f.format("20G")}\"")
        println("\"${c.format("20G")}\"")
        println("\"${f.format("20")}\"")
        println("\"${c.format("20")}\"")
    }
    ```

    运行结果：

    ```text
    "            1.23e+03"
    "              1234.1"
    "         1.23412E+11"
    "         1234.099976"
    " 123412340736.000000"
    ```

## API 列表

### 接口

|              接口名          |           功能           |
| --------------------------- | ------------------------ |
| [Formattable](./convert_package_api/convert_package_interfaces.md#interface-formattable) | 该接口定义了格式化函数，即根据格式化参数将指定类型实例转换为对应格式的字符串。 |
| [Parsable\<T>](./convert_package_api/convert_package_interfaces.md#interface-parsablet) | 将字符串解析为特定类型的接口。 |
| [RadixConvertible\<T>](./convert_package_api/convert_package_interfaces.md#interface-radixconvertiblet) | 将指定字符串解析为特定类型的接口。 |
