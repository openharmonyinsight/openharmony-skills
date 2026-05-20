# 同一时间在不同时区的本地时间

该示例演示了如何将一个中国标准时间，转换为同一时间下 UTC 和美国东部夏令时时间。

> **说明：**
>
> 示例中使用 [TimeZone.load](../time_package_api/time_package_classes.md#static-func-loadstring) 函数加载时区信息，在不同平台上加载时区信息有不同的依赖，用户需按其要求进行设置。

<!-- verify -->

```cangjie
import std.time.*

main() {
    let datetime = DateTime.of(year: 2024, month: May, dayOfMonth: 22, hour: 12,
        timeZone: TimeZone.load("Asia/Shanghai"))

    println("CST: ${datetime}")
    println("UTC: ${datetime.inUTC()}")
    println("EDT: ${datetime.inTimeZone(TimeZone.load("America/New_York"))}")
}
```

运行结果：

```text
CST: 2024-05-22T12:00:00+08:00
UTC: 2024-05-22T04:00:00Z
EDT: 2024-05-22T00:00:00-04:00
```
