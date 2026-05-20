# 类

## class JsonReader

```cangjie
public class JsonReader {
    public init(inputStream: InputStream)
}
```

功能：此类提供 JSON 数据流转仓颉对象的反序列化能力。

使用示例见[使用 Json Stream 进行反序列化](../json_stream_samples/sample_json_reader.md)

### init(InputStream)

```cangjie
public init(inputStream: InputStream)
```

功能：根据输入流创建一个 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader)， [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader) 从输入流中读取数据时，将跳过非 [JsonString](../../json/json_package_api/encoding_json_package_classes.md#class-jsonstring) 中的空字符（'\0', '\t', '\n', '\r'）。

参数：

- inputStream: InputStream - 输入的 JSON 数据流。

### func endArray()

```cangjie
public func endArray(): Unit
```

功能：从输入流的当前位置跳过空白字符后消耗一个 ']' 字符，[endArray](encoding_json_stream_package_classes.md#func-endarray) 必须有一个 [startArray](encoding_json_stream_package_classes.md#func-startarray) 与之对应。

异常：

- IllegalStateException - 如果输入流的 JSON 数据不符合格式，抛出异常。

### func endObject()

```cangjie
public func endObject(): Unit
```

功能：从输入流的当前位置跳过空白字符后消耗一个 '}' 字符，[endObject](encoding_json_stream_package_classes.md#func-endobject) 必须有一个 [startObject](encoding_json_stream_package_classes.md#func-startobject) 与之对应。

异常：

- IllegalStateException - 如果输入流的 JSON 数据不符合格式，抛出异常。

### func peek()

```cangjie
public func peek(): Option<JsonToken>
```

功能：获取输入流的下一个 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 的类型，不保证下一个 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 的格式一定正确。

例：如果输入流中的下一个字符为 't'，获取的 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 将为 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken).Bool，但调用 readValue\<Bool>() 不一定成功。

返回值：

- Option\<[JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken)> - 获取到的下一个 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 的类型，如果到了输入流的结尾返回 None。

异常：

- IllegalStateException - 如果输入流的下一个字符不在以下范围内：(n, t, f, ", 0~9, -, {, }, [, ])。

### func readName()

```cangjie
public func readName(): String
```

功能：从输入流的当前位置读取一个 name。

返回值：

- String - 读取出的 name 值。

异常：

- IllegalStateException - 如果输入流的 JSON 数据不符合格式，抛出异常。

### func readValue\<T>() where T <: JsonDeserializable\<T>

```cangjie
public func readValue<T>(): T where T <: JsonDeserializable<T>
```

功能：从输入流的当前位置读取一个 value。

> **注意：**
>
> 当泛型 T 是 String 类型时，根据下一个 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 的不同，该函数的返回值将会不同：
>
> - 当下一个 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 是 [JsonString](../../json/json_package_api/encoding_json_package_classes.md#class-jsonstring) 时， 反序列化过程会按照标准 [ECMA-404 The JSON Data Interchange Standard](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/) 对读到的 String 进行转义。
>
> - 当下一个 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 是 [JsonInt](../../json/json_package_api/encoding_json_package_classes.md#class-jsonint) [JsonFloat](../../json/json_package_api/encoding_json_package_classes.md#class-jsonfloat) [JsonBool](../../json/json_package_api/encoding_json_package_classes.md#class-jsonbool) [JsonNull](../../json/json_package_api/encoding_json_package_classes.md#class-jsonnull) 其中一个时，将会读取下一个 `value` 字段的原始字符串并返回。
>
> - 当下一个 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 是其它类型时，调用此接口会抛异常。

返回值：

- T - 读取出的 value 值。

异常：

- IllegalStateException - 如果输入流的 JSON 数据不符合格式，抛出异常。

### func readValueBytes()

```cangjie
public func readValueBytes(): Array<Byte>
```

功能：读取输入流的下一组原始数据(字节数组)，不进行转义等操作。

> **说明：**
>
> readValueBytes 的规则如下：
>
> - 如果 next token 是 value，则读取这个 value 的所有原始字节，直到读取到代表结束的符号，如 ',' '}' ']'。
>
> - 如果 next token 是 Name，读取 (name + value) 这一个组合的原始字节数组。
>
> - 如果 next token 是 BeginArray，读取 Array 内的内的所有原始字节。
>
> - 如果 next token 是 BeginObject，读取 Object 内的内的所有原始字节。
>
> - 如果 next token 是 EndArray 或者 EndObject 或者 None，不做任何操作，返回空的数组，再次执行 peek() 仍返回 EndArray 或者 EndObject 或者 None。

返回值：

- Array\<Byte> - 下一组数据对应的原始字节数据。

异常：

- IllegalStateException - 如果输入流的 JSON 数据不符合格式，抛出异常。

### func skip()

```cangjie
public func skip(): Unit
```

功能：从输入流的当前位置跳过一组数据。

> **说明：**
>
> Skip 的规则如下：
>
> - 如果 next token 是 value，跳过这个 value, 跳过 value 时不检查该 value 格式是否正确。
>
> - 如果 next token 是 Name，跳过 (name + value) 这一个组合。
>
> - 如果 next token 是 BeginArray，跳过这个 array。
>
> - 如果 next token 是 BeginObject，跳过这个 object。
>
> - 如果 next token 是 EndArray 或者 EndObject 或者 None，不做任何操作，peek 仍返回 EndArray 或者 EndObject 或者 None。

异常：

- IllegalStateException - 如果输入流的 JSON 数据不符合格式，抛出异常。

### func startArray()

```cangjie
public func startArray(): Unit
```

功能：从输入流的当前位置跳过空白字符后消耗一个 '[' 字符。

异常：

- IllegalStateException - 如果输入流的 JSON 数据不符合格式，抛出异常。

### func startObject()

```cangjie
public func startObject(): Unit
```

功能：从输入流的当前位置跳过空白字符后消耗一个 '{' 字符。

异常：

- IllegalStateException - 如果输入流的 JSON 数据不符合格式，抛出异常。

## class JsonWriter

```cangjie
public class JsonWriter {
    public var writeConfig = WriteConfig.compact
    public init(out: OutputStream)
}
```

功能：[JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 提供了将仓颉对象序列化到 OutputStream 的能力。

[JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 需要和 interface [JsonSerializable](encoding_json_stream_package_interfaces.md#interface-jsonserializable) 搭配使用，[JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 可以通过 writeValue 来将实现了 [JsonSerializable](encoding_json_stream_package_interfaces.md#interface-jsonserializable) 接口的类型写入到 Stream 中。

> **注意：**
>
> [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 中使用缓存来减少写入 Stream 时的 IO 次数，在结束使用 [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 之前需要调用 flush 函数来确保缓存中的数据全部写入 Stream。

示例：

使用示例见[使用 Json Stream 进行序列化](../json_stream_samples/sample_json_writer.md)

### var writeConfig

```cangjie
public var writeConfig = WriteConfig.compact
```

功能：序列化格式配置。详见 [WriteConfig](./encoding_json_stream_package_structs.md#struct-writeconfig)。

### init(OutputStream)

```cangjie
public init(out: OutputStream)
```

功能：构造函数，构造一个将数据写入 out 的实例。

参数：

- out: OutputStream - 目标流

### func endArray()

```cangjie
public func endArray(): Unit
```

功能：结束序列化当前的 JSON 数组。

异常：

- IllegalStateException - 当前 writer 没有匹配的 startArray 时。

### func endObject()

```cangjie
public func endObject(): Unit
```

功能：结束序列化当前的 JSON object。

异常：

- IllegalStateException - 当前 writer 的状态不应该结束一个 JSON object 时。

### func flush()

```cangjie
public func flush(): Unit
```

功能：将缓存中的数据写入 out，并且调用 out 的 flush 方法。

### func jsonValue(String)

```cangjie
public func jsonValue(value: String): JsonWriter
```

功能：将符合 JSON value 规范的原始字符串写入 stream。

> **注意：**
>
> 此函数不会对值 value 进行转义，也不会为入参添加双引号。如果使用者能够保证输入的值 value 符合数据转换标准[ECMA-404 The JSON Data Interchange Standard](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/)， 建议使用该函数。

返回值：

- [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) - 为方便链式调用，返回值为当前 [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 的引用。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。

### func startArray()

```cangjie
public func startArray(): Unit
```

功能：开始序列化一个新的 JSON 数组，每一个 [startArray](encoding_json_stream_package_classes.md#func-startarray-1) 都必须有一个 [endArray](encoding_json_stream_package_classes.md#func-endarray-1) 对应。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 JSON array 时。

### func startObject()

```cangjie
public func startObject(): Unit
```

功能：开始序列化一个新的 JSON object，每一个 [startObject](encoding_json_stream_package_classes.md#func-startobject-1) 都必须有一个 [endObject](encoding_json_stream_package_classes.md#func-endobject-1) 对应。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 JSON object 时。

### func writeName(String)

```cangjie
public func writeName(name: String): JsonWriter
```

功能：在 object 结构中写入 name。

返回值：

- [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) - 当前 [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 引用。

异常：

- IllegalStateException - 当前 [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 的状态不应写入参数 `name` 指定字符串时。

### func writeNullValue()

```cangjie
public func writeNullValue(): JsonWriter
```

功能：向流中写入 JSON value null。

返回值：

- [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) - 为方便链式调用，返回值为当前 [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 的引用。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时

### func writeValue\<T>(T) where T <: JsonSerializable

```cangjie
public func writeValue<T>(v: T): JsonWriter where T <: JsonSerializable
```

功能：将实现了 [JsonSerializable](encoding_json_stream_package_interfaces.md#interface-jsonserializable) 接口的类型写入到 Stream 中。该接口会调用泛型 T 的 toJson 方法向输出流中写入数据。

json.stream 包已经为基础类型 Int64、UInt64、Float64、Bool、String 类型扩展实现了 [JsonSerializable](encoding_json_stream_package_interfaces.md#interface-jsonserializable)， 并且为 Collection 类型 Array、ArrayList 和 HashMap 扩展实现了 [JsonSerializable](encoding_json_stream_package_interfaces.md#interface-jsonserializable)。

返回值：

- [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) - 返回当前 [JsonWriter](encoding_json_stream_package_classes.md#class-jsonwriter) 的引用。

异常：

- IllegalStateException - 当前 writer 的状态不应该写入 value 时。
