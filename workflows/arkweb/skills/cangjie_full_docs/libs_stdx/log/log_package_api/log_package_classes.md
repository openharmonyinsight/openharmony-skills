# 类

## class Logger

```cangjie
public abstract class Logger <: Resource {
}
```

功能：此抽象类提供基础的日志打印和管理功能。

父类型：

- Resource

### prop level

```cangjie
public open mut prop level: LogLevel
```

功能：获取和修改日志打印级别。

类型：[LogLevel](log_package_structs.md#struct-loglevel)

### func debug(String, Array\<Attr>)

```cangjie
public func debug(message: String, attrs: Array<Attr>): Unit
```

功能：打印 [DEBUG](log_package_structs.md#static-const-debug) 级别的日志的便捷函数。

参数：

- message: String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func debug(() -> String, Array\<Attr>)

```cangjie
public func debug(message: () -> String, attrs: Array<Attr>): Unit
```

功能：打印 [DEBUG](log_package_structs.md#static-const-debug) 级别的日志的便捷函数。

参数：

- message: () -> String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func enabled(LogLevel)

```cangjie
public func enabled(level: LogLevel): Bool
```

功能：确定是否记录指定日志级别的日志消息。

这个函数允许调用者提前判断日志是否会被丢弃，以避免耗时的日志消息参数计算。

参数：

- level: [LogLevel](log_package_structs.md#struct-loglevel) - 日志级别。

返回值：

- Bool - 如果指定的日志级别处于使能状态，则返回 `true`；否则，返回 `false`。

### func error(String, Array\<Attr>)

```cangjie
public func error(message: String, attrs: Array<Attr>): Unit
```

功能：打印 [ERROR](log_package_structs.md#static-const-error) 级别的日志的便捷函数。

参数：

- message: String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func error(() -> String, Array\<Attr>)

```cangjie
public func error(message: () -> String, attrs: Array<Attr>): Unit
```

功能：打印 [ERROR](log_package_structs.md#static-const-error) 级别的日志的便捷函数。

参数：

- message: () -> String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func fatal(String, Array\<Attr>)

```cangjie
public func fatal(message: String, attrs: Array<Attr>): Unit
```

功能：打印 [FATAL](log_package_structs.md#static-const-fatal) 级别的日志的便捷函数。

参数：

- message: String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func fatal(() -> String, Array\<Attr>)

```cangjie
public func fatal(message: () -> String, attrs: Array<Attr>): Unit
```

功能：打印 [FATAL](log_package_structs.md#static-const-fatal) 级别的日志的便捷函数。

参数：

- message: () -> String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func info(String, Array\<Attr>)

```cangjie
public func info(message: String, attrs: Array<Attr>): Unit
```

功能：打印 [INFO](log_package_structs.md#static-const-info) 级别的日志的便捷函数。

参数：

- message: String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func info(() -> String, Array\<Attr>)

```cangjie
public func info(message: () -> String, attrs: Array<Attr>): Unit
```

功能：打印 [INFO](log_package_structs.md#static-const-info) 级别的日志的便捷函数。

参数：

- message: () -> String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func log(LogLevel, String, Array\<Attr>)

```cangjie
public open func log(level: LogLevel, message: String, attrs: Array<Attr>): Unit
```

功能：打印日志的通用函数，需指定日志级别。

参数：

- level: [LogLevel](log_package_structs.md#struct-loglevel) - 日志级别。
- message: String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func log(LogLevel, () -> String, Array\<Attr>)

```cangjie
public open func log(level: LogLevel, message: () -> String, attrs: Array<Attr>): Unit
```

功能：打印日志的通用函数，需指定日志级别。

参数：

- level: [LogLevel](log_package_structs.md#struct-loglevel) - 日志级别。
- message: () -> String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func log(LogRecord)

```cangjie
public open func log(record: LogRecord): Unit
```

功能：打印日志的通用函数。

参数：

- record: [LogRecord](log_package_classes.md#class-logrecord) - 日志级别。

### func trace(String, Array\<Attr>)

```cangjie
public func trace(message: String, attrs: Array<Attr>): Unit
```

功能：打印 [TRACE](log_package_structs.md#static-const-trace) 级别的日志的便捷函数。

参数：

- message: String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func trace(() -> String, Array\<Attr>)

```cangjie
public func trace(message: () -> String, attrs: Array<Attr>): Unit
```

功能：打印 [TRACE](log_package_structs.md#static-const-trace) 级别的日志的便捷函数。

参数：

- message: () -> String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func warn(String, Array\<Attr>)

```cangjie
public func warn(message: String, attrs: Array<Attr>): Unit
```

功能：打印 [WARN](log_package_structs.md#static-const-warn) 级别的日志的便捷函数。

参数：

- message: String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func warn(() -> String, Array\<Attr>)

```cangjie
public func warn(message: () -> String, attrs: Array<Attr>): Unit
```

功能：打印 [WARN](log_package_structs.md#static-const-warn) 级别的日志的便捷函数。

参数：

- message: () -> String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func withAttrs(Array\<Attr>)

```cangjie
public open func withAttrs(attrs: Array<Attr>): Logger
```

功能：创建当前对象的副本，新的副本会包含指定的属性。

参数：

- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对属性。

返回值：

- [Logger](#class-logger) - [Logger](#class-logger) 类的对象实例。

## class LogRecord

```cangjie
public class LogRecord {
    public init(time: DateTime, level: LogLevel, msg: String, attrs: Array<Attr>)
}
```

功能：日志消息的“负载”。

记录结构作为参数传递给 [Logger](#class-logger) 类的 [log](#func-loglogrecord) 方法。日志提供者处理这些结构以显示日志消息。记录是由日志对象自动创建，因此日志用户看不到。

### init(DateTime, LogLevel, String, Array\<Attr>)

```cangjie
public init(time: DateTime, level: LogLevel, msg: String, attrs: Array<Attr>)
```

功能：创建一个 [LogRecord](log_package_classes.md#class-logrecord) 实例，指定时间戳，日志打印级别，日志消息和日志数据键值对。

参数：

- time: DateTime - 记录日志时的时间戳
- level: [LogLevel](log_package_structs.md#struct-loglevel) - 日志级别。
- msg: String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### prop attrs

```cangjie
public mut prop attrs: Array<Attr>
```

功能：获取或设置日志数据键值对。

类型：Array\<[Attr](log_package_types.md#type-attr)>

### prop level

```cangjie
public prop level: LogLevel
```

功能：获取日志打印级别，只有级别小于等于该值的日志会被打印。

类型：[LogLevel](log_package_structs.md#struct-loglevel)

### prop message

```cangjie
public mut prop message: String
```

功能：获取或设置日志消息。

类型：String

### prop time

```cangjie
public prop time: DateTime
```

功能：获取日志打印时的时间戳。

类型：DateTime

### func clone()

```cangjie
public func clone(): LogRecord
```

功能：创建当前对象的副本。

返回值：

- [LogRecord](log_package_classes.md#class-logrecord) - 当前对象的副本。

## class LogWriter

```cangjie
public abstract class LogWriter {
}
```

功能：[LogWriter](log_package_classes.md#class-logwriter) 提供了将仓颉对象序列化成日志输出目标的能力。

[LogWriter](log_package_classes.md#class-logwriter) 需要和 interface [LogValue](log_package_interfaces.md#interface-logvalue) 搭配使用，[LogWriter](log_package_classes.md#class-logwriter) 可以通过 writeValue 系列方法来将实现了 [LogValue](log_package_interfaces.md#interface-logvalue) 接口的类型写入到日志输出目标中。

### func endArray()

```cangjie
public func endArray(): Unit
```

功能：结束序列化当前的 [LogValue](log_package_interfaces.md#interface-logvalue) 数组。

异常：

- IllegalStateException - 当前 writer 没有匹配的 startArray 时。

### func endObject()

```cangjie
public func endObject(): Unit
```

功能：结束序列化当前的 [LogValue](log_package_interfaces.md#interface-logvalue) object。

异常：

- IllegalStateException - 当前 writer 的状态不应该结束一个 [LogValue](log_package_interfaces.md#interface-logvalue) object 时。

### func startArray()

```cangjie
public func startArray(): Unit
```

功能：开始序列化一个新的 [LogValue](log_package_interfaces.md#interface-logvalue) 数组，每一个 startArray 都必须有一个 endArray 对应。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 [LogValue](log_package_interfaces.md#interface-logvalue) array 时。

### func startObject()

```cangjie
public func startObject(): Unit
```

功能：开始序列化一个新的 [LogValue](log_package_interfaces.md#interface-logvalue) object，每一个 startObject 都必须有一个 endObject 对应。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 [LogValue](log_package_interfaces.md#interface-logvalue) object 时。

### func writeBool(Bool)

```cangjie
public func writeBool(v: Bool): Unit
```

功能：向日志输出目标中写入 Bool 值。

参数：

- v: Bool - 待写入的 Bool 值。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。

### func writeFloat(Float64)

```cangjie
public func writeFloat(v: Float64): Unit
```

功能：向日志输出目标中写入 Float64 值。

参数：

- v: Float64 - 待写入的 Float64 值。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。

### func writeDateTime(DateTime)

```cangjie
public func writeDateTime(v: DateTime): Unit
```

功能：向日志输出目标中写入 DateTime 值。

参数：

- v: DateTime - 待写入的 DateTime 值。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。

### func writeDuration(Duration)

```cangjie
public func writeDuration(v: Duration): Unit
```

功能：向日志输出目标中写入 Duration 值。

参数：

- v: Duration - 待写入的 Duration 值。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。

### func writeException(Exception)

```cangjie
public func writeException(v: Exception): Unit
```

功能：向日志输出目标中写入 Exception 值。

参数：

- v: Exception - 待写入的 Exception 值。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时，抛出该异常。

### func writeInt(Int64)

```cangjie
public func writeInt(v: Int64): Unit
```

功能：向日志输出目标中写入 Int64 值。

参数：

- v: Int64 - 待写入的 Int64 值。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。

### func writeKey(String)

```cangjie
public func writeKey(v: String): Unit
```

功能：向日志输出目标中写入 name。

参数：

- v: String - 待写入的 Key 值。

异常：

- IllegalStateException - 当前 writer 的状态不应写入参数 `name` 指定字符串时。

### func writeNone()

```cangjie
public func writeNone(): Unit
```

功能：向日志输出目标中写入 None，具体写成什么格式由 Logger 的提供者自行决定。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。

### func writeString(String)

```cangjie
public func writeString(v: String): Unit
```

功能：向日志输出目标中写入 String 值。

参数：

- v: String  - 待写入的 String 值。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。

### func writeValue(LogValue)

```cangjie
public func writeValue(v: LogValue): Unit
```

功能：将实现了 [LogValue](log_package_interfaces.md#interface-logvalue) 接口的类型写入到日志输出目标中。该接口会调用 [LogValue](log_package_interfaces.md#interface-logvalue) 的 [writeTo](log_package_interfaces.md#func-writetologwriter) 方法向日志输出目标中写入数据。

log 包已经为基础类型 Int64、Float64、Bool、String 类型扩展实现了 [LogValue](log_package_interfaces.md#interface-logvalue)，并且为 DateTime、Duration、 Collection 类型 Array、HashMap 和 TreeMap 以及 Option\<T> 扩展实现了 [LogValue](log_package_interfaces.md#interface-logvalue)。

参数：

- v: [LogValue](log_package_interfaces.md#interface-logvalue) - 待写入的 [LogValue](log_package_interfaces.md#interface-logvalue) 值。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。

## class NoopLogger

```cangjie
public class NoopLogger <: Logger {
    public init()
}
```

功能：[Logger](#class-logger) 的 NO-OP（无操作）实现，会丢弃所有的日志。

父类型：

- [Logger](#class-logger)

### init()

```cangjie
public init()
```

功能：创建一个 [NoopLogger](log_package_classes.md#class-nooplogger) 实例。

### prop level

```cangjie
public mut prop level: LogLevel
```

功能：永远只能获取到 OFF 日志打印级别，设置日志打印级别不会生效。

类型：[LogLevel](log_package_structs.md#struct-loglevel)

### func close()

```cangjie
public func close(): Unit
```

功能：NOOP 实现。

### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：NOOP 实现。

返回值：

- Bool - 是否关闭。

### func log(LogLevel, String, Array\<Attr>)

```cangjie
public func log(level: LogLevel, message: String, attrs: Array<Attr>): Unit
```

功能：NOOP 实现。

参数：

- level: [LogLevel](log_package_structs.md#struct-loglevel) - 日志级别。
- message: String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func log(LogLevel, () -> String, Array\<Attr>)

```cangjie
public func log(level: LogLevel, message: () -> String, attrs: Array<Attr>): Unit
```

功能：NOOP 实现。

参数：

- level: [LogLevel](log_package_structs.md#struct-loglevel) - 日志级别。
- message: () -> String - 日志消息。
- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

### func log(LogRecord)

```cangjie
public func log(record: LogRecord): Unit
```

功能：NOOP 实现。

参数：

- record: [LogRecord](log_package_classes.md#class-logrecord) - 日志级别。

### func withAttrs(Array\<Attr>)

```cangjie
public func withAttrs(attrs: Array<Attr>): Logger
```

功能：NOOP 实现。

参数：

- attrs: Array\<[Attr](log_package_types.md#type-attr)> - 日志数据键值对。

返回值：

- [Logger](#class-logger) - Logger