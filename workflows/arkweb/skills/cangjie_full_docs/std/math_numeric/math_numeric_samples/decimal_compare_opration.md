# Decimal 大小比较示例

以下为初始化多个 `Decimal` 对象，相互之间大小比较的示例：
<!-- verify -->

```cangjie
import std.math.*
import std.math.numeric.*

main() {
    let decimal1 = Decimal.parse("12345.6789")
    let decimal2 = Decimal.parse("987.654321")
    println("${decimal1} > ${decimal2} = ${decimal1 > decimal2}")
    println("${decimal1} < ${decimal2} = ${decimal1 < decimal2}")
    println("${decimal1} == ${decimal2} = ${decimal1 == decimal2}")
    println("${decimal1} != ${decimal2} = ${decimal1 != decimal2}")
    println("${decimal1} <= ${decimal2} = ${decimal1 <= decimal2}")
    println("${decimal1} >= ${decimal2} = ${decimal1 >= decimal2}")
    println("${decimal1}.compare(${decimal2}) = ${decimal1.compare(decimal2)}")
    return 0
}
```

运行结果：

```text
12345.6789 > 987.654321 = true
12345.6789 < 987.654321 = false
12345.6789 == 987.654321 = false
12345.6789 != 987.654321 = true
12345.6789 <= 987.654321 = false
12345.6789 >= 987.654321 = true
12345.6789.compare(987.654321) = Ordering.GT
```
