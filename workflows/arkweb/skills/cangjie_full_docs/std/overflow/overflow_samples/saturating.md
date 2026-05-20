# 饱和策略的示例

下面是饱和策略的示例，示例中尝试运算 UInt16.Max 乘 16，运算结果超过 UInt16 的最大值，发生上溢，故返回 UInt16 的最大值。

<!-- verify -->

```cangjie
import std.overflow.*
import std.math.*

main() {
    let a: UInt16 = UInt16.Max
    println(a.saturatingMul(16))
}
```

运行结果：

```text
65535
```
