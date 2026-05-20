# 类

## class DateTimeFormat

```cangjie
public class DateTimeFormat {
    public static const RFC1123: String = "www, dd MMM yyyy HH:mm:ss z"
    public static const RFC3339: String = "yyyy-MM-ddTHH:mm:ssOOOO"
    public static const RFC822: String = "ww dd MMM yy HH:mm:ss z"
    public static const RFC850: String = "wwww, dd-MMM-yy HH:mm:ss z"
}
```

功能：提供时间格式的功能，用于解析和生成 [DateTime](../time_package_api/time_package_structs.md#struct-datetime) 。

### static const RFC1123

```cangjie
public static const RFC1123: String = "www, dd MMM yyyy HH:mm:ss z"
```

功能：提供 RFC1123 时间格式，时间字符串格式为 `www, dd MMM yyyy HH:mm:ss z`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const RFC3339

```cangjie
public static const RFC3339: String = "yyyy-MM-ddTHH:mm:ssOOOO"
```

功能：提供 RFC3339 时间格式，时间字符串格式为 `yyyy-MM-ddTHH:mm:ssOOOO`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const RFC822

```cangjie
public static const RFC822: String = "ww dd MMM yy HH:mm:ss z"
```

功能：提供 RFC822 时间格式，时间字符串格式为 `ww dd MMM yy HH:mm:ss z`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const RFC850

```cangjie
public static const RFC850: String = "wwww, dd-MMM-yy HH:mm:ss z"
```

功能：提供 RFC850 时间格式，时间字符串格式为 `wwww, ww-MMM-yy HH:mm:ss z`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop format: String <sup>(deprecated)</sup>

```cangjie
public prop format: String
```

功能：DateTimeFormat 实例的字符串格式。

> **注意：**
>
> 未来版本即将废弃不再使用。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static func of(String) <sup>(deprecated)</sup>

```cangjie
public static func of(format: String): DateTimeFormat
```

功能：根据字符串创建具体的 DateTimeFormat 类型实例。

字符串的具体格式见[时间字符串格式](../time_package_overview.md#时间字符串格式)。

> **注意：**
>
> 未来版本即将废弃不再使用。

参数：

- format: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串格式。

返回值：

- [DateTimeFormat](#class-datetimeformat) - 时间格式。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当入参格式不符合[时间字符串格式](../time_package_overview.md#时间字符串格式)中字母数量的规定时，抛出异常。

## class TimeZone

```cangjie
public class TimeZone <: ToString & Equatable<TimeZone> {
    public static let Local: TimeZone
    public static let UTC: TimeZone
    public init(id: String, offset: Duration)
}
```

功能：TimeZone 表示时区，记录了某一地区在不同时间较零时区的时间偏移，提供了从系统加载时区、自定义时区等功能。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)
- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[TimeZone](#class-timezone)>

### static let Local

```cangjie
public static let Local: TimeZone
```

功能：获取本地时区。

`Local` 从系统环境变量 TZ 中获取时区 ID，并根据该时区 ID 从系统时区文件中加载时区。其行为与函数 [load](#static-func-loadstring) 相同。

环境变量 TZ 的取值为标准时区 ID 格式（各操作系统遵循相同规范），例如“Asia/Shanghai”。

若环境变量 TZ 未设置或者为空，加载本地时区的规则如下：

- 在 Linux/Unix like 系统上：加载系统路径“/etc/localtime”链接，时区名与“/etc/localtime”指向的相对路径名相同，例如“Asia/Shanghai”。
- 如果上一条执行失败或者在 Windows 系统上，返回 ID 为 “UTC&偏移量” 的时区，例如“Asia/Shanghai”对应的时区为“UTC+08:00”。

类型：[TimeZone](time_package_classes.md#class-timezone)

### static let UTC

```cangjie
public static let UTC: TimeZone
```

功能：获取 UTC 时区。

类型：[TimeZone](time_package_classes.md#class-timezone)

### prop id

```cangjie
public prop id: String
```

功能：获取当前 [TimeZone](time_package_classes.md#class-timezone) 实例所关联的时区 ID。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### init(String, Duration)

```cangjie
public init(id: String, offset: Duration)
```

功能：使用指定的时区 ID 和偏移量构造一个自定义 [TimeZone](time_package_classes.md#class-timezone) 实例。

参数：

- id: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 时区 ID。使用“/”作为分隔符，例如“Asia/Shanghai”，各操作系统使用相同规范。
- offset: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 相对 UTC 时区的偏移量，精度为秒，向东为正、向西为负。取值范围为 (-25 * [Duration](../../core/core_package_api/core_package_structs.md#struct-duration).hour, 26 * [Duration](../../core/core_package_api/core_package_structs.md#struct-duration).hour)。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当输入 `id` 为空字符串，或 `offset` 超出有效区间时，抛出异常。

### static func load(String)

```cangjie
public static func load(id: String): TimeZone
```

功能：从系统中加载参数 `id` 指定的时区。

> **说明：**
>
> - 在 Linux 、 macOS 系统中，若存在环境变量 CJ_TZPATH，则使用环境变量指定的路径加载时区文件（若存在多个通过分隔符 “:” 分开的环境变量值，则按照分隔路径的先后顺序依次查找时区文件，并加载第一个找到的时区文件），否则从系统时区文件目录（Linux 和 macOS 为 "/usr/share/zoneinfo"）加载时区。
> - 在 Windows 系统中，用户需下载[时区文件](https://www.iana.org/time-zones)并编译，设置环境变量 CJ_TZPATH 指向 zoneinfo 目录（若存在多个通过分隔符 “;” 分开的环境变量值，则按照分隔路径的先后顺序依次查找时区文件，并加载第一个找到的时区文件），否则会导致异常。

参数：

- id: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 时区 ID。

返回值：

- [TimeZone](time_package_classes.md#class-timezone) - 时区。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当参数 `id` 为空，或长度超过 4096 字节，或不符合标准时区 ID 格式时，抛出异常。
- [InvalidDataException](time_package_exceptions.md#class-invaliddataexception) - 当时区文件加载失败（找不到文件，文件解析失败等）时，抛出异常。

### static func loadFromPaths(String, Array\<String>)

```cangjie
public static func loadFromPaths(id: String, tzpaths: Array<String>): TimeZone
```

功能：根据参数 `tzpaths` 指定的时区文件目录，加载参数 `id` 指定的时区。

加载时区时，将从第一个被读取成功的时区文件路径中加载时区。时区文件格式需要满足[时区信息格式](https://datatracker.ietf.org/doc/html/rfc8536)。

参数：

- id: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 时区 ID。
- tzpaths: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 时区文件路径数组。

返回值：

- [TimeZone](time_package_classes.md#class-timezone) - 加载的时区。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 `id` 为空，或长度超过 4096 字节，或不符合标准时区 ID 格式时，抛出异常。
- [InvalidDataException](time_package_exceptions.md#class-invaliddataexception) - 当时区文件加载失败（找不到文件，文件解析失败等）时，抛出异常。

### static func loadFromTZData(String, Array\<UInt8>)

```cangjie
public static func loadFromTZData(id: String, data: Array<UInt8>): TimeZone
```

功能：使用指定的时区 ID 和时区数据构造一个自定义 [TimeZone](time_package_classes.md#class-timezone) 实例。`id` 可以是任何合法字符串，`data` 需要满足 IANA 时区文件格式，加载成功时获得 [TimeZone](time_package_classes.md#class-timezone) 实例，否则抛出异常。

参数：

- id: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 时区 ID。
- data: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 满足[时区信息格式](https://datatracker.ietf.org/doc/html/rfc8536)的数据。

返回值：

- [TimeZone](time_package_classes.md#class-timezone) - 加载的时区。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 `id` 为空时，抛出异常。
- [InvalidDataException](time_package_exceptions.md#class-invaliddataexception) - 如果 `data` 解析失败，则抛出异常。

### func toString()

```cangjie
public func toString(): String
```

功能：获取本 [TimeZone](time_package_classes.md#class-timezone) 实例时区 ID 的字符串表示。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 时区 ID 的字符串表示。

### operator func !=(TimeZone)

```cangjie
public operator func !=(r: TimeZone): Bool
```

功能：判断当前 [TimeZone](time_package_classes.md#class-timezone) 实例的引用是否不等于 `r` 的引用。

参数：

- r: [TimeZone](time_package_classes.md#class-timezone) - [TimeZone](time_package_classes.md#class-timezone) 实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - `true` 或 `false`。当前 [TimeZone](time_package_classes.md#class-timezone) 实例的引用不等于 `r` 的引用时，返回 `true`；否则，返回 `false`。

### operator func ==(TimeZone)

```cangjie
public operator func ==(r: TimeZone): Bool
```

功能：判断当前 [TimeZone](time_package_classes.md#class-timezone) 实例的引用是否等于 `r` 的引用。

参数：

- r: [TimeZone](time_package_classes.md#class-timezone) - [TimeZone](time_package_classes.md#class-timezone) 实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - `true` 或 `false`。当前 [TimeZone](time_package_classes.md#class-timezone) 实例的引用等于 `r` 的引用时，返回 `true`；否则，返回 `false`。
