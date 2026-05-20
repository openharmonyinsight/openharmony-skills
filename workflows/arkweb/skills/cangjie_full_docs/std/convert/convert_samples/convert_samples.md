# convert 使用示例

## format 使用示例

### 格式化整型

下面是格式化整型示例。

示例：

<!-- verify -->
```cangjie
import std.convert.*

main(): Int64 {
    var a: Int32 = -20
    var res1 = a.format("-10")
    var res2 = a.format("+10")
    var res3 = (-20).format("10")
    var res4 = a.format("-")
    println("\"${res1}\"")
    println("\"${res2}\"")
    println("\"${res3}\"")
    println("\"${res4}\"")
    return 0
}
```

运行结果：

```text
"-20       "
"       -20"
"       -20"
"-20"
```

### 格式化浮点型

下面是格式化浮点型示例。

示例：

<!-- verify -->
```cangjie
import std.convert.*

main(): Int64 {
    var a: Float16 = -0.34
    var b: Float32 = .34
    var c: Float64 = 3_0.3__4_
    var d: Float64 = 20.00

    /* 左对齐 */
    var res1 = a.format("-20")

    /* 右对齐 */
    var res2 = b.format("+20")

    /* 右对齐 */
    var res3 = c.format("10")

    /* 左对齐 */
    var res4 = d.format("-10")

    /* 正常输出 */
    var res5 = d.format("-")

    println("\"${res1}\"")
    println("\"${res2}\"")
    println("\"${res3}\"")
    println("\"${res4}\"")
    println("\"${res5}\"")
    return 0
}
```

运行结果：

```text
"-0.340088           "
"           +0.340000"
" 30.340000"
"20.000000 "
"20.000000"
```

### 格式化字符型

下面是格式化字符型示例。

示例：

<!-- verify -->
```cangjie
import std.convert.*

main(): Int64 {
    var a: Rune = 'a'
    var b: Rune = '-'

    /* 左对齐 */
    var res1 = a.format("-10")

    /* 左对齐 */
    var res2 = b.format("-10")

    /* 右对齐 */
    var res3 = a.format("10")

    /* 右对齐 */
    var res4 = b.format("10")

    println("\"${res1}\"")
    println("\"${res2}\"")
    println("\"${res3}\"")
    println("\"${res4}\"")
    return 0
}
```

运行结果：

```text
"a         "
"-         "
"         a"
"         -"
```

## convert 使用示例

示例：

<!-- verify -->
```cangjie
import std.convert.*

main(): Int64 {
    var strBool_parse: String = "true"
    var strBool_tryParse: String = "false"
    var strChar_parse: String = "'a'"
    var strChar_tryParse: String = "'\\u{00e2}'"
    var strInt8_parse: String = "-128"
    var strInt8_tryParse: String = "127"
    var strInt16_parse: String = "-32768"
    var strInt16_tryParse: String = "32767"
    var strInt32_parse: String = "-2147483648"
    var strInt32_tryParse: String = "2147483647"
    var strInt64_parse: String = "-9223372036854775808"
    var strInt64_tryParse: String = "9223372036854775807"
    var strFloat16_parse: String = "-65504.0"
    var strFloat16_tryParse: String = "65504.0"
    var strFloat32_parse: String = "-3.14159"
    var strFloat32_tryParse: String = "3.14159"
    var strFloat64_parse: String = "-3.1415926"
    var strFloat64_tryParse: String = "3.1415926"
    var strUInt8_parse: String = "255"
    var strUInt8_tryParse: String = "255"
    var strUInt16_parse: String = "65535"
    var strUInt16_tryParse: String = "65535"
    var strUInt32_parse: String = "4294967295"
    var strUInt32_tryParse: String = "4294967295"
    var strUInt64_parse: String = "18446744073709551615"
    var strUInt64_tryParse: String = "18446744073709551615"

    println("After the conversion of parse, \"true\" became ${Bool.parse(strBool_parse)}")
    println("After the conversion of tryParse, \"false\" became ${Bool.tryParse(strBool_tryParse)}")

    println("After the conversion of parse, \"'a'\" became ${Rune.parse(strChar_parse)}")
    println("After the conversion of tryParse, \"'\\u{00e2}'\" became ${Rune.tryParse(strChar_tryParse)}")

    println("After the conversion of parse, \"-128\" became ${Int8.parse(strInt8_parse)}")
    println("After the conversion of tryParse, \"127\" became ${Int8.tryParse(strInt8_tryParse)}")

    println("After the conversion of parse, \"-32768\" became ${Int16.parse(strInt16_parse)}")
    println("After the conversion of tryParse, \"32767\" became ${Int16.tryParse(strInt16_tryParse)}")

    println("After the conversion of parse, \"-2147483648\" became ${Int32.parse(strInt32_parse)}")
    println("After the conversion of tryParse, \"2147483647\" became ${Int32.tryParse(strInt32_tryParse)}")

    println("After the conversion of parse, \"-9223372036854775808\" became ${Int64.parse(strInt64_parse)}")
    println("After the conversion of tryParse, \"9223372036854775807\" became ${Int64.tryParse(strInt64_tryParse)}")

    println("After the conversion of parse, \"-65504.0\" became ${Float16.parse(strFloat16_parse)}")
    println("After the conversion of tryParse, \"65504.0\" became ${Float16.tryParse(strFloat16_tryParse)}")

    println("After the conversion of parse, \"-3.14159\" became ${Float32.parse(strFloat32_parse)}")
    println("After the conversion of tryParse, \"3.14159\" became ${Float32.tryParse(strFloat32_tryParse)}")

    println("After the conversion of parse, \"-3.1415926\" became ${Float64.parse(strFloat64_parse)}")
    println("After the conversion of tryParse, \"3.1415926\" became ${Float64.tryParse(strFloat64_tryParse)}")

    println("After the conversion of parse, \"255\" became ${UInt8.parse(strUInt8_parse)}")
    println("After the conversion of tryParse, \"255\" became ${UInt8.tryParse(strUInt8_tryParse)}")

    println("After the conversion of parse, \"65535\" became ${UInt16.parse(strUInt16_parse)}")
    println("After the conversion of tryParse, \"65535\" became ${UInt16.tryParse(strUInt16_tryParse)}")

    println("After the conversion of parse, \"4294967295\" became ${UInt32.parse(strUInt32_parse)}")
    println("After the conversion of tryParse, \"4294967295\" became ${UInt32.tryParse(strUInt32_tryParse)}")

    println("After the conversion of parse, \"18446744073709551615\" became ${UInt64.parse(strUInt64_parse)}")
    println("After the conversion of tryParse, \"18446744073709551615\" became ${UInt64.tryParse(strUInt64_tryParse)}")
    return 0
}
```

运行结果：

```text
After the conversion of parse, "true" became true
After the conversion of tryParse, "false" became Some(false)
After the conversion of parse, "'a'" became a
After the conversion of tryParse, "'\u{00e2}'" became Some(â)
After the conversion of parse, "-128" became -128
After the conversion of tryParse, "127" became Some(127)
After the conversion of parse, "-32768" became -32768
After the conversion of tryParse, "32767" became Some(32767)
After the conversion of parse, "-2147483648" became -2147483648
After the conversion of tryParse, "2147483647" became Some(2147483647)
After the conversion of parse, "-9223372036854775808" became -9223372036854775808
After the conversion of tryParse, "9223372036854775807" became Some(9223372036854775807)
After the conversion of parse, "-65504.0" became -65504.000000
After the conversion of tryParse, "65504.0" became Some(65504.000000)
After the conversion of parse, "-3.14159" became -3.141590
After the conversion of tryParse, "3.14159" became Some(3.141590)
After the conversion of parse, "-3.1415926" became -3.141593
After the conversion of tryParse, "3.1415926" became Some(3.141593)
After the conversion of parse, "255" became 255
After the conversion of tryParse, "255" became Some(255)
After the conversion of parse, "65535" became 65535
After the conversion of tryParse, "65535" became Some(65535)
After the conversion of parse, "4294967295" became 4294967295
After the conversion of tryParse, "4294967295" became Some(4294967295)
After the conversion of parse, "18446744073709551615" became 18446744073709551615
After the conversion of tryParse, "18446744073709551615" became Some(18446744073709551615)
```
