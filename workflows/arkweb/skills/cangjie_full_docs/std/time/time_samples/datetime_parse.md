# DateTime 与 String 类型的转换

该示例演示了如何通过格式化字符串 `pattern`，对时间进行格式化打印，以及从格式化字符串中解析时间。

> **说明：**
>
> 示例中使用 [TimeZone.load](../time_package_api/time_package_classes.md#static-func-loadstring) 函数加载时区信息，在不同平台上加载时区信息有不同的依赖，用户需按其要求进行设置。

<!-- verify -->

```cangjie
import std.time.*

main() {
    let pattern = "yyyy/MM/dd HH:mm:ssSSS OO"
    let datetime = DateTime.of(
        year: 2024,
        month: May,
        dayOfMonth: 22,
        hour: 12,
        minute: 34,
        second: 56,
        nanosecond: 789000000,
        timeZone: TimeZone.load("Asia/Shanghai")
    )
    let str = datetime.format(pattern)
    println(str)
    println(DateTime.parse(str, pattern))
}
```

运行结果：

```text
2024/05/22 12:34:56789000000 +08:00
2024-05-22T12:34:56.789+08:00
```
