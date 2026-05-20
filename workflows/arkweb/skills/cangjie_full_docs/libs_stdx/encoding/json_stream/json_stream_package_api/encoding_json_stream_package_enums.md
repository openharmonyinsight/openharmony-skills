# 枚举

## enum JsonToken

```cangjie
public enum JsonToken <: Equatable<JsonToken> & Hashable{
    | JsonNull
    | JsonBool
    | JsonNumber
    | JsonString
    | BeginArray
    | EndArray
    | BeginObject
    | EndObject
    | Name
}
```

功能：表示 JSON 编码的字符串中的结构、名称或者值类型。

[JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 通常和 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek()搭配使用，通过对返回值的判断来决定具体的处理方式。

父类型：

- Equatable\<[JsonToken](#enum-jsontoken)>
- Hashable

### BeginArray

```cangjie
BeginArray
```

功能：表示 JSON 中 array 的开始。如果 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek() 返回的是该类型，可以使用 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).startArray() 读取。

### BeginObject

```cangjie
BeginObject
```

功能：表示 JSON 中 object 的开始。如果 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek() 返回的是该类型，可以使用 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).startObject() 读取。

### EndArray

```cangjie
EndArray
```

功能：表示 JSON 中 array 的结束。如果 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek() 返回的是该类型，可以使用 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).endArray() 读取。

### EndObject

```cangjie
EndObject
```

功能：表示 JSON 中 object 的结束。如果 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek() 返回的是该类型，可以使用 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).endObject() 读取。

### JsonBool

```cangjie
JsonBool
```

功能：表示 JSON 的 bool 类型。如果 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek() 返回的是该类型，可以使用 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).readValue\<Bool>() 读取。

### JsonNull

```cangjie
JsonNull
```

功能：表示 JSON 的 null 类型。如果 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek() 返回的是该类型，可以使用 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).readValue\<Option\<T>>() 读取。

### JsonNumber

```cangjie
JsonNumber
```

功能：表示 JSON 的 number 类型。如果 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek() 返回的是该类型，可以使用 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).readValue\<Float64>() 读取。

### JsonString

```cangjie
JsonString
```

功能：表示 JSON 的 string 类型。如果 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek() 返回的是该类型，可以使用 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).readValue\<String>() 读取。

### Name

```cangjie
Name
```

功能：表示 object 中的 name。如果 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).peek() 返回的是该类型，可以使用 [JsonReader](encoding_json_stream_package_classes.md#class-jsonreader).readName() 读取。

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 对象的 hashCode 值。

返回值：

- Int64 - hashCode 值。

### operator func !=(JsonToken)

```cangjie
public operator func !=(that: JsonToken): Bool
```

功能：判不等。

参数：

- that: [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) - 被比较的 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 对象

返回值：

- Bool - 当前实例与 that 不相等返回 true，否则返回 false

### operator func ==(JsonToken)

```cangjie
public operator func ==(that: JsonToken): Bool
```

功能：判等。

参数：

- that: [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) - 被比较的 [JsonToken](encoding_json_stream_package_enums.md#enum-jsontoken) 对象

返回值：

- Bool - 当前实例与 that 相等返回 true，否则返回 false
