# 结构体

## struct LogLevel

```cangjie
public struct LogLevel <: ToString & Comparable<LogLevel> {
    public static const OFF: LogLevel = LogLevel("OFF", 0x7FFF_FFFF)
    public static const FATAL: LogLevel = LogLevel("FATAL", 6000)
    public static const ERROR: LogLevel = LogLevel("ERROR", 5000)
    public static const WARN: LogLevel = LogLevel("WARN", 4000)
    public static const INFO: LogLevel = LogLevel("INFO", 3000)
    public static const DEBUG: LogLevel = LogLevel("DEBUG", 2000)
    public static const TRACE: LogLevel = LogLevel("TRACE", 1000)
    public static const ALL: LogLevel = LogLevel("ALL", -0x8000_0000)
    public let name: String
    public let value: Int32
    public const init(name: String, value: Int32)
}
```

功能：[LogLevel](log_package_structs.md#struct-loglevel) 为日志级别结构体。

定义了日志打印的七个级别，级别从高到低分别为 `OFF`、 `FATAL`、`ERROR`、`WARN`、`INFO`、`DEBUG`、`TRACE`、`ALL`。

我们期望只有级别大于等于指定打印级别的日志条目会被打印到输出流中。

父类型：

- ToString
- Comparable\<[LogLevel](#struct-loglevel)>

### static const ALL

```cangjie
public static const ALL: LogLevel = LogLevel("ALL", -0x8000_0000)
```

功能：获取一个日志打印级别的静态常量实例，等级为所有。

### static const DEBUG

```cangjie
public static const DEBUG: LogLevel = LogLevel("DEBUG", 2000)
```

功能：获取一个日志打印级别的静态常量实例，等级为调试。

### static const ERROR

```cangjie
public static const ERROR: LogLevel = LogLevel("ERROR", 5000)
```

功能：获取一个日志打印级别的静态常量实例，等级为错误。

### static const FATAL

```cangjie
public static const FATAL: LogLevel = LogLevel("FATAL", 6000)
```

功能：获取一个日志打印级别的静态常量实例，等级为严重错误。

### static const INFO

```cangjie
public static const INFO: LogLevel = LogLevel("INFO", 3000)
```

功能：获取一个日志打印级别的静态常量实例，等级为通知。

### static const OFF

```cangjie
public static const OFF: LogLevel = LogLevel("OFF", 0x7FFF_FFFF)
```

功能：获取一个日志打印级别的静态常量实例，等级为禁用。

### static const TRACE

```cangjie
public static const TRACE: LogLevel = LogLevel("TRACE", 1000)
```

功能：获取一个日志打印级别的静态常量实例，等级为跟踪。

### static const WARN

```cangjie
public static const WARN: LogLevel = LogLevel("WARN", 4000)
```

功能：获取一个日志打印级别的静态常量实例，等级为警告。

### let name

```cangjie
public let name: String
```

功能：日志级别名。

### let value

```cangjie
public let value: Int32
```

功能：日志级别值。

### const init(String, Int32)

```cangjie
public const init(name: String, value: Int32)
```

功能：常量构造函数，创建 LogLevel 对象。

参数：

- name: String - 日志级别名。
- value: Int32 - 日志级别值。

### func compare(LogLevel)

```cangjie
public func compare(rhs: LogLevel): Ordering
```

功能：判断当前 [LogLevel](log_package_structs.md#struct-loglevel) 类型实例与参数指向的 [LogLevel](log_package_structs.md#struct-loglevel) 类型实例的大小关系。

参数：

- rhs: [LogLevel](log_package_structs.md#struct-loglevel) - 待与当前实例比较的另一个实例。

返回值：

- Ordering - 如果大于，返回 Ordering.GT，如果等于，返回 Ordering.EQ，如果小于，返回 Ordering.LT。

### func toString()

```cangjie
public func toString(): String
```

功能：获取日志级别对应的名称。

返回值：

- String - 当前的日志级别的名称。

### operator func ==(LogLevel)

```cangjie
public operator func ==(rhs: LogLevel): Bool
```

功能：比较日志级别高低。

参数：

- rhs: [LogLevel](log_package_structs.md#struct-loglevel) - 将当前日志级别和 `target` 进行比较。

返回值：

- Bool - 如果当前日志级别等于 `target`，返回 `true`，否则返回 `false`。

### operator func !=(LogLevel)

```cangjie
public operator func !=(rhs: LogLevel): Bool
```

功能：比较日志级别高低。

参数：

- rhs: [LogLevel](log_package_structs.md#struct-loglevel) - 将当前日志级别和 `target` 进行比较。

返回值：

- Bool - 如果当前日志级别不等于 `target`，返回 `true`，否则返回 `false`。

### operator func >=(LogLevel)

```cangjie
public operator func >=(rhs: LogLevel): Bool
```

功能：比较日志级别高低。

参数：

- rhs: [LogLevel](log_package_structs.md#struct-loglevel) - 将当前日志级别和 `target` 进行比较。

返回值：

- Bool - 如果当前日志级别大于等于 `target`，返回 `true`，否则返回 `false`。

### operator func <=(LogLevel)

```cangjie
public operator func <=(rhs: LogLevel): Bool
```

功能：比较日志级别高低。

参数：

- rhs: [LogLevel](log_package_structs.md#struct-loglevel) - 将当前日志级别和 `target` 进行比较。

返回值：

- Bool - 如果当前日志级别小于等于 `target`，返回 `true`，否则返回 `false`。

### operator func >(LogLevel)

```cangjie
public operator func >(rhs: LogLevel): Bool
```

功能：比较日志级别高低。

参数：

- rhs: [LogLevel](log_package_structs.md#struct-loglevel) - 将当前日志级别和 `target` 进行比较。

返回值：

- Bool - 如果当前日志级别大于 `target`，返回 `true`，否则返回 `false`。

### operator func <(LogLevel)

```cangjie
public operator func <(rhs: LogLevel): Bool
```

功能：比较日志级别高低。

参数：

- rhs: [LogLevel](log_package_structs.md#struct-loglevel) - 将当前日志级别和 `target` 进行比较。

返回值：

- Bool - 如果当前日志级别小于 `target`，返回 `true`，否则返回 `false`。
