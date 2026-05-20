# 抛出异常策略的示例

下面是抛出异常策略的示例，示例中尝试运算 Int64.Max + 1，发生溢出，抛出 OverflowException。

<!-- run.error -->

```cangjie
import std.overflow.*
import std.math.*

main() {
    let a: Int64 = Int64.Max
    println(a.throwingAdd(1))
}
```

运行结果：

```text
An exception has occurred:
OverflowException: add
```
