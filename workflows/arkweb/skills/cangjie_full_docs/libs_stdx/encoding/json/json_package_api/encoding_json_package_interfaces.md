# 接口

## interface ToJson

```cangjie
public interface ToJson {
    static func fromJson(jv: JsonValue): DataModel
    func toJson(): JsonValue
}
```

功能：用于实现 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 和 [DataModel](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodel) 的相互转换。

### static func fromJson(JsonValue)

```cangjie
static func fromJson(jv: JsonValue): DataModel
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转化为对象 [DataModel](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodel)。

参数：

- jv: [JsonValue](encoding_json_package_classes.md#class-jsonvalue) - 待转换的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

返回值：

- [DataModel](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodel) - 转换后的 [DataModel](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodel)。

### func toJson()

```cangjie
func toJson(): JsonValue
```

功能：将自身转化为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

返回值：

- [JsonValue](encoding_json_package_classes.md#class-jsonvalue) - 转换后的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果转换失败，抛出异常。

### extend DataModel <: ToJson

```cangjie
extend DataModel <: ToJson
```

功能：为 [DataModel](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodel) 类型实现 ToJson 接口。

父类型：

- [ToJson](#interface-tojson)

#### static func fromJson(JsonValue)

```cangjie
public static func fromJson(jv: JsonValue): DataModel
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转化为对象 [DataModel](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodel)。

参数：

- jv: [JsonValue](encoding_json_package_classes.md#class-jsonvalue) - 待转换的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

返回值：

- [DataModel](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodel) - 转换后的 [DataModel](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodel)。

#### func toJson()

```cangjie
public func toJson(): JsonValue
```

功能：将自身转化为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

返回值：

- [JsonValue](encoding_json_package_classes.md#class-jsonvalue) - 转换后的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果转换失败，抛出异常。