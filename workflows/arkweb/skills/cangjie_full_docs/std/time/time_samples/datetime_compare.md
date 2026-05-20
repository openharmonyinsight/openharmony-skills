# DateTime 比较

该示例选取中国标准时间（CST，时区 ID 为“Asia/Shanghai”）和美国东部夏令时时间（EDT，时区 ID 为“America/New_York”）进行时间比较。

> **说明：**
>
> 示例中使用 [TimeZone.load](../time_package_api/time_package_classes.md#static-func-loadstring) 函数加载时区信息，在不同平台上加载时区信息有不同的依赖，用户需按其要求进行设置。

<!-- verify -->

```cangjie
import std.time.*

main() {
    let tzSH = TimeZone.load("Asia/Shanghai")
    let tzNY = TimeZone.load("America/New_York")
    // 2024-05-25T00:00:00Z
    let shanghai1 = DateTime.of(year: 2024, month: May, dayOfMonth: 25, hour: 8, timeZone: tzSH)
    let new_york1 = DateTime.of(year: 2024, month: May, dayOfMonth: 24, hour: 20, timeZone: tzNY)

    // 2024-05-25T01:00:00Z
    let shanghai2 = DateTime.of(year: 2024, month: May, dayOfMonth: 25, hour: 9, timeZone: tzSH)
    let new_york2 = DateTime.of(year: 2024, month: May, dayOfMonth: 24, hour: 21, timeZone: tzNY)

    println(shanghai1 == new_york1)
    println(shanghai1 != new_york2)
    println(shanghai1 <= new_york2)
    println(shanghai1 < new_york2)
    println(shanghai2 >= new_york1)
    println(shanghai2 > new_york1)
}
```

运行结果：

```text
true
true
true
true
true
true
```
