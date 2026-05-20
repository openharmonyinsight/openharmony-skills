# 利用 MonoTime 作计时

该示例演示了如何通过 `MonoTime` 类型进行计时。

<!-- run -->

```cangjie
import std.time.*

const count = 10000

main() {
    let start = MonoTime.now()
    for (_ in 0..count) {
        DateTime.now()
    }
    let end = MonoTime.now()
    let result = end - start
    println("total cost: ${result.toNanoseconds()}ns")
}
```

运行结果（以实际结果为准）

```text
total cost: 951159ns
```
