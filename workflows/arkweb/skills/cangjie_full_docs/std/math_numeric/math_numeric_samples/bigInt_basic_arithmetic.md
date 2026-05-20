# BigInt 基础数学运算示例

以下为通过不同构造函数初始化 `BigInt` 对象，并进行基础数学运算的示例：
<!-- verify -->

```cangjie
import std.math.numeric.*

main() {
    let int1: BigInt = BigInt.parse("123456789")
    let int2: BigInt = BigInt.parse("987654321")

    println("${int1} + ${int2} = ${int1 + int2}")
    println("${int1} - ${int2} = ${int1 - int2}")
    println("${int1} * ${int2} = ${int1 * int2}")
    println("${int1} / ${int2} = ${int1 / int2}")
    let (quo, mod) = int1.divAndMod(int2)
    println("${int1} / ${int2} = ${quo} .. ${mod}")

    return 0
}
```

运行结果：

```text
123456789 + 987654321 = 1111111110
123456789 - 987654321 = -864197532
123456789 * 987654321 = 121932631112635269
123456789 / 987654321 = 0
123456789 / 987654321 = 0 .. 123456789
```
