# 接口

## interface LogValue

```cangjie
public interface LogValue {
    func writeTo(w: LogWriter): Unit
}
```

功能：为类型提供序列化到日志输出目标的接口。

与 [LogWriter](log_package_classes.md#class-logwriter) 搭配使用， [LogWriter](log_package_classes.md#class-logwriter) 可以通过 writeValue 将实现了 [LogValue](log_package_interfaces.md#interface-logvalue) 接口的类型写入到日志输出目标中。

### func writeTo(LogWriter)

```cangjie
func writeTo(w: LogWriter): Unit
```

功能：将实现了 [LogValue](log_package_interfaces.md#interface-logvalue) 接口的类型写入参数 `w` 指定的 [LogWriter](log_package_classes.md#class-logwriter) 实例中。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend Bool <: LogValue

```cangjie
extend Bool <: LogValue
```

功能：为 Bool 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 Bool 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend Exception <: LogValue

```cangjie
extend Exception <: LogValue
```

功能：为 Exception 类型实现 [LogValue](./log_package_interfaces.md#interface-logvalue) 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 Exception 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend Int64 <: LogValue

```cangjie
extend Int64 <: LogValue
```

功能：为 Int64 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 Int64 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend Float64 <: LogValue

```cangjie
extend Float64 <: LogValue
```

功能：为 Float64 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 Float64 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend String <: LogValue

```cangjie
extend String <: LogValue
```

功能：为 String 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 String 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend DateTime <: LogValue

```cangjie
extend DateTime <: LogValue
```

功能：为 DateTime 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 DateTime 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend Duration <: LogValue

```cangjie
extend Duration <: LogValue
```

功能：为 Duration 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 Duration 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend\<T> Array\<T> <: LogValue where T <: LogValue

```cangjie
extend<T> Array<T> <: LogValue where T <: LogValue
```

功能：为 Array\<T> 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 Array\<T> 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend\<V> HashMap\<String, V> <: LogValue where V <: LogValue

```cangjie
extend<V> HashMap<String, V> <: LogValue where V <: LogValue
```

功能：为 HashMap\<K, V> 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 HashMap\<K, V> 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend\<V> TreeMap\<String, V> <: LogValue where V <: LogValue

```cangjie
extend<V> TreeMap<String, V> <: LogValue where V <: LogValue
```

功能：为 TreeMap\<K, V> 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 TreeMap\<K, V> 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。

### extend\<T> Option\<T> <: LogValue where T <: LogValue

```cangjie
extend<T> Option<T> <: LogValue where T <: LogValue
```

功能：为 Option\<T> 类型实现 LogValue 接口。

父类型：

- [LogValue](#interface-logvalue)

#### func writeTo(LogWriter)

```cangjie
public func writeTo(w: LogWriter): Unit
```

功能：提供 Option\<T> 类型序列化到流的功能。

参数：

- w:  [LogWriter](log_package_classes.md#class-logwriter) - 写入序列化结果的 [LogWriter](log_package_classes.md#class-logwriter) 实例。
