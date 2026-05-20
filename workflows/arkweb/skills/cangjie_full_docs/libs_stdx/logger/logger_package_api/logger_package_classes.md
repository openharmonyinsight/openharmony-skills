# 类

## class JsonLogger

```cangjie
public class JsonLogger <: Logger {
    public init(output: OutputStream)
}
```

功能：此类实现了输出 `JSON` 格式的日志打印功能，形如 `{"time":"2024-07-27T11:51:59+08:00","level":"INFO","msg":"foo","name":"bar"}`。

父类型：

- [Logger](../../log/log_package_api/log_package_classes.md#class-logger)

### init(OutputStream)

```cangjie
public init(output: OutputStream)
```

功能：创建 [JsonLogger](logger_package_classes.md#class-jsonlogger) 对象。

参数：

- output: OutputStream - 绑定的输出流，日志格式化后将写入该输出流。

### prop level

```cangjie
public mut prop level: LogLevel
```

功能：获取和修改日志打印级别。

类型：[LogLevel](../../log/log_package_api/log_package_structs.md#struct-loglevel)

### func close()

```cangjie
public func close(): Unit
```

功能：关闭 Logger。

### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：判断当前 Logger 是否关闭。

返回值：

- Bool - 是否关闭。

### func log(LogRecord)

```cangjie
public func log(record: LogRecord): Unit
```

功能：打印日志的通用函数。

参数：

- record: [LogRecord](../../log/log_package_api/log_package_classes.md#class-logrecord) - 日志级别。

### func withAttrs(Array\<Attr>)

```cangjie
public func withAttrs(attrs: Array<Attr>): Logger
```

功能：创建当前对象的副本，新的副本会包含指定的属性。

参数：

- attrs: Array\<[Attr](../../log/log_package_api/log_package_types.md#type-attr)> - 日志数据键值对属性。

返回值：

- [Logger](../../log/log_package_api/log_package_classes.md#class-logger) - [Logger](../../log/log_package_api/log_package_classes.md#class-logger) 类的对象实例。

## class SimpleLogger

```cangjie
public class SimpleLogger <: Logger {
    public init(output: OutputStream)
}
```

功能：此类实现了输出文本格式的日志打印功能，形如 `2024-07-27T11:50:47.6616733+08:00 INFO foo  name="bar"`。

父类型：

- [Logger](../../log/log_package_api/log_package_classes.md#class-logger)

### init(OutputStream)

```cangjie
public init(output: OutputStream)
```

功能：创建 [SimpleLogger](logger_package_classes.md#class-simplelogger) 对象。

参数：

- output: OutputStream - 绑定的输出流，日志格式化后将写入该输出流。

### prop level

```cangjie
public mut prop level: LogLevel
```

功能：获取和修改日志打印级别。

类型：[LogLevel](../../log/log_package_api/log_package_structs.md#struct-loglevel)

### func close()

```cangjie
public func close(): Unit
```

功能：关闭 Logger。

### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：判断当前 Logger 是否关闭。

返回值：

- Bool - 是否关闭。

### func log(LogRecord)

```cangjie
public func log(record: LogRecord): Unit
```

功能：打印日志的通用函数。

参数：

- record: [LogRecord](../../log/log_package_api/log_package_classes.md#class-logrecord) - 日志级别。

### func withAttrs(Array\<Attr>)

```cangjie
public func withAttrs(attrs: Array<Attr>): Logger
```

功能：创建当前对象的副本，新的副本会包含指定的属性。

参数：

- attrs: Array\<[Attr](../../log/log_package_api/log_package_types.md#type-attr)> - 日志数据键值对属性。

返回值：

- [Logger](../../log/log_package_api/log_package_classes.md#class-logger) - [Logger](../../log/log_package_api/log_package_classes.md#class-logger) 类的对象实例。

## class TextLogger

```cangjie
public class TextLogger <: Logger {
    public init(output: OutputStream)
}
```

功能：此类实现了输出文本格式的日志打印功能，形如 `time=2024-07-27T11:52:40.3226881+08:00 level="INFO" msg="foo" name="bar"`。

父类型：

- [Logger](../../log/log_package_api/log_package_classes.md#class-logger)

### init(OutputStream)

```cangjie
public init(output: OutputStream)
```

功能：创建 [TextLogger](logger_package_classes.md#class-textlogger) 对象。

参数：

- output: OutputStream - 绑定的输出流，日志格式化后将写入该输出流。

### prop level

```cangjie
public mut prop level: LogLevel
```

功能：获取和修改日志打印级别。

类型：[LogLevel](../../log/log_package_api/log_package_structs.md#struct-loglevel)

### func close()

```cangjie
public func close(): Unit
```

功能：关闭 Logger。

### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：判断当前 Logger 是否关闭。

返回值：

- Bool - 是否关闭。

### func log(LogRecord)

```cangjie
public func log(record: LogRecord): Unit
```

功能：打印日志的通用函数。

参数：

- record: [LogRecord](../../log/log_package_api/log_package_classes.md#class-logrecord) - 日志级别。

### func withAttrs(Array\<Attr>)

```cangjie
public func withAttrs(attrs: Array<Attr>): Logger
```

功能：创建当前对象的副本，新的副本会包含指定的属性。

参数：

- attrs: Array\<[Attr](../../log/log_package_api/log_package_types.md#type-attr)> - 日志数据键值对属性。

返回值：

- [Logger](../../log/log_package_api/log_package_classes.md#class-logger) - [Logger](../../log/log_package_api/log_package_classes.md#class-logger) 类的对象实例。
