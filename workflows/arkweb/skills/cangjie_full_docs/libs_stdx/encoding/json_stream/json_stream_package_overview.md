# stdx.encoding.json.stream

## 功能介绍

json.stream 包主要用于仓颉对象和 JSON 数据流之间的互相转换。

本包提供了 JsonWriter 和 JsonReader 类，JsonWriter 用于提供仓颉对象转 JSON 数据流的序列化能力；JsonReader 用于提供 JSON 数据流转仓颉对象的反序列化能力。

当前实现中支持和 JSON 数据流互转的类型有：

- 基础数据类型：String、Int8、Int16、Int32、Int64、Float16、Float32、Float64、UInt8、UInt16、UInt32、UInt64。

- 集合类型：Array\<T>、ArrayList\<T>、HashMap\<String, T>。

- 其它类型：Option\<T>、BigInt、Decimal。

## API 列表

### 接口

| 接口名 | 功能 |
|-------| ------|
|[JsonDeserializable\<T>](./json_stream_package_api/encoding_json_stream_package_interfaces.md#interface-jsondeserializablet)| 此接口用于实现从 [JsonReader](./json_stream_package_api/encoding_json_stream_package_classes.md#class-jsonreader) 中读取一个仓颉对象。 |
|[JsonSerializable](./json_stream_package_api/encoding_json_stream_package_interfaces.md#interface-jsonserializable)| 为类型提供序列化到 JSON 数据流的接口。 |

### 类

|  类名 | 功能  |
| ------------ | ------------ |
| [JsonReader](./json_stream_package_api/encoding_json_stream_package_classes.md#class-jsonreader) | 此类提供 JSON 数据流转仓颉对象的反序列化能力。 |
| [JsonWriter](./json_stream_package_api/encoding_json_stream_package_classes.md#class-jsonwriter) | 构造函数，构造一个将数据写入 out 的实例。 |

### 枚举

|  枚举名 | 功能  |
| ------------ | ------------ |
| [JsonToken](./json_stream_package_api/encoding_json_stream_package_enums.md#enum-jsontoken) | 表示 JSON 编码的字符串中的结构、名称或者值类型。 |

### 结构体

|            结构体名          |           功能           |
| --------------------------- | ------------------------ |
| [WriteConfig](./json_stream_package_api/encoding_json_stream_package_structs.md#struct-writeconfig) | 用于表示 [JsonWriter](./json_stream_package_api/encoding_json_stream_package_classes.md#class-jsonwriter) 的序列化格式配置。 |
