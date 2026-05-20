# 返回 `Option` 策略的示例

下面是返回 `Option` 策略的示例，示例中尝试运算 Int64.Max 的平方，发生溢出，返回 None。

<!-- verify -->

```cangjie
import std.overflow.*
import std.math.*

main() {
    let a: Int64 = Int64.Max
    println(a.checkedPow(UInt64(2)))
}
```

运行结果：

```text
None
```
