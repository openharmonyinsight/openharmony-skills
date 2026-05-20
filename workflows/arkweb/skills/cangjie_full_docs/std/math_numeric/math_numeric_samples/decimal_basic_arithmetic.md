# Decimal 基础数学运算示例

以下为通过不同构造函数初始化 `Decimal` 对象，并进行基础数学运算的示例：
<!-- verify -->

```cangjie
import std.math.*
import std.math.numeric.*

main() {
    let decimal1: Decimal = Decimal.parse("12345.6789")
    let decimal2: Decimal = Decimal(BigInt.parse("987654321"), 6)
    println("${decimal1} + ${decimal2} = ${decimal1 + decimal2}")
    println("${decimal1} - ${decimal2} = ${decimal1 - decimal2}")
    println("${decimal1} * ${decimal2} = ${decimal1 * decimal2}")
    println("${decimal1} / ${decimal2} = ${decimal1 / decimal2}")
    println(
        "${decimal1} / ${decimal2} with precision 10 and rounding mode HalfEven = ${decimal1.divWithPrecision(decimal2, 10, roundingMode: HalfEven)}"
    )
    let (quo, rem) = decimal1.divAndMod(decimal2)
    println("${decimal1} / ${decimal2} = ${quo} .. ${rem}")
    return 0
}
```

运行结果：

```text
12345.6789 + 987.654321 = 13333.333221
12345.6789 - 987.654321 = 11358.024579
12345.6789 * 987.654321 = 12193263.1112635269
12345.6789 / 987.654321 = 12.49999988609375000142382812498220
12345.6789 / 987.654321 with precision 10 and rounding mode HalfEven = 12.49999989
12345.6789 / 987.654321 = 12 .. 493.827048
```
