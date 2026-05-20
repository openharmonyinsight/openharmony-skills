# stdx.encoding.json

## 功能介绍

json 包用于对 JSON 数据的处理，实现 String, JsonValue, DataModel 之间的相互转换。

JsonValue 是对 JSON 数据格式的封装，包括 object, array, string, number, true, false 和 null。

DataModel 详细信息可参考：[serialization 包文档](../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodel)。

JSON 语法规则可参考：[介绍 JSON](https://www.json.org/json-zh.html)。

JSON 数据转换标准可参考：[ECMA-404 The JSON Data Interchange Standard](https://www.ecma-international.org/publications-and-standards/standards/ecma-404/)。

## API 列表

### 接口

| 接口名  | 功能  |
| ------------ | ------------ |
| [ToJson](./json_package_api/encoding_json_package_interfaces.md#interface-tojson) | 用于实现 JsonValue 和 DataModel 的相互转换。 |

### 类

|  类名 | 功能  |
| ------------ | ------------ |
| [JsonArray](./json_package_api/encoding_json_package_classes.md#class-jsonarray) | 创建空 JsonArray。 |
| [JsonBool](./json_package_api/encoding_json_package_classes.md#class-jsonbool) | 将指定的 Bool 类型实例封装成 JsonBool 实例。 |
| [JsonFloat](./json_package_api/encoding_json_package_classes.md#class-jsonfloat) | 将指定的 Float64 类型实例封装成 JsonFloat 实例。 |
| [JsonInt](./json_package_api/encoding_json_package_classes.md#class-jsonint) | 将指定的 Int64 类型实例封装成 JsonInt 实例。 |
| [JsonNull](./json_package_api/encoding_json_package_classes.md#class-jsonnull) | 将 JsonNull 转换为字符串。 |
| [JsonObject](./json_package_api/encoding_json_package_classes.md#class-jsonobject) | 创建空 JsonObject。 |
| [JsonString](./json_package_api/encoding_json_package_classes.md#class-jsonstring) | 将指定的 String 类型实例封装成 JsonString 实例。 |
| [JsonValue](./json_package_api/encoding_json_package_classes.md#class-jsonvalue) | 此类为 JSON 数据层, 主要用于 JsonValue 和 String 数据之间的互相转换。 |

### 枚举

|  枚举名 | 功能  |
| ------------ | ------------ |
| [JsonKind](./json_package_api/encoding_json_package_enums.md#enum-jsonkind) | 表示 JsonValue 的具体类型。 |

### 异常类

| 异常类名  | 功能  |
| ------------ | ------------ |
|[JsonException](./json_package_api/encoding_json_package_exceptions.md#class-jsonexception)| 用于 JsonValue 类型使用时出现异常的场景。 |
