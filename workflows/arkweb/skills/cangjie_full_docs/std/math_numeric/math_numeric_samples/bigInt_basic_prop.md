# BigInt 基本属性示例

以下为初始化 `BigInt` 对象的，并查询对象的基本属性的示例：
<!-- verify -->

```cangjie
import std.math.numeric.*

main() {
    let int = BigInt.parse("-123456")
    println("BigInt: ${int}")
    println("BigInt sign: ${int.sign}")
    println("BigInt bitLen: ${int.bitLen}")
    return 0
}
```

运行结果：

```text
BigInt: -123456
BigInt sign: -1
BigInt bitLen: 18
```
