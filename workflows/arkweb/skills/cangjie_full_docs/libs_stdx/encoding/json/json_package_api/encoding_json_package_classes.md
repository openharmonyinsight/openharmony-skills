# 类

## class JsonArray

```cangjie
public class JsonArray <: JsonValue {
    public init()
    public init(list: ArrayList<JsonValue>)
    public init(list: Array<JsonValue>)
}
```

功能：此类为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 实现子类，主要用于封装数组类型的 JSON 数据。

父类型：

- [JsonValue](#class-jsonvalue)

示例：

使用示例见 [JsonArray 使用示例](../json_samples/json_array_sample.md)。

### init()

```cangjie
public init()
```

功能：创建空 [JsonArray](encoding_json_package_classes.md#class-jsonarray)。

### init(ArrayList\<JsonValue>)

```cangjie
public init(list: ArrayList<JsonValue>)
```

功能：将指定的 ArrayList 类型实例封装成 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 实例。

参数：

- list: ArrayList\<[JsonValue](encoding_json_package_classes.md#class-jsonvalue)> - 用于创建 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 的 ArrayList。

### init(Array\<JsonValue>)

```cangjie
public init(list: Array<JsonValue>)
```

功能：将指定的 Array 类型实例封装成 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 实例。

参数：

- list: Array\<[JsonValue](encoding_json_package_classes.md#class-jsonvalue)> - 用于创建 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 的 Array。

### func add(JsonValue)

```cangjie
public func add(jv: JsonValue): JsonArray
```

功能：向 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 中加入 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 数据。

参数：

- jv: [JsonValue](encoding_json_package_classes.md#class-jsonvalue) - 需要加入的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

返回值：

- [JsonArray](encoding_json_package_classes.md#class-jsonarray) - 加入数据后的 [JsonArray](encoding_json_package_classes.md#class-jsonarray)。

### func get(Int64)

```cangjie
public func get(index: Int64): Option<JsonValue>
```

功能：获取 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 中指定索引的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)，并用 Option\<[JsonValue](encoding_json_package_classes.md#class-jsonvalue)> 封装。

参数：

- index: Int64 - 指定的索引。

返回值：

- Option\<[JsonValue](encoding_json_package_classes.md#class-jsonvalue)> - 对应索引的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 数据的封装形式。

### func getItems()

```cangjie
public func getItems(): ArrayList<JsonValue>
```

功能：获取 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 中的 items 数据。

返回值：

- ArrayList\<[JsonValue](encoding_json_package_classes.md#class-jsonvalue)> - [JsonArray](encoding_json_package_classes.md#class-jsonarray) 的 items 数据。

### func kind()

```cangjie
public func kind(): JsonKind
```

功能：返回当前 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsArray）。

返回值：

- [JsonKind](encoding_json_package_enums.md#enum-jsonkind) - 当前 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsArray）。

### func size()

```cangjie
public func size(): Int64
```

功能：获取 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 中 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 的数量。

返回值：

- Int64 - [JsonArray](encoding_json_package_classes.md#class-jsonarray) 中 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 的数量。

### func toJsonString()

```cangjie
public func toJsonString(): String
```

功能：将 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 转换为 JSON 格式的 (带有空格换行符) 的字符串。

返回值：

- String - 转换后的 JSON 格式字符串。

### func toJsonString(Int64, Bool, String)

```cangjie
public func toJsonString(depth: Int64, bracketInNewLine!: Bool = false, indent!: String = "  "): String
```

功能：将 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 转换为 JSON 格式的字符串。该函数将指定初始的缩进深度、第一个括号后是否换行以及缩进字符串。

参数：

- depth: Int64 - 指定的缩进深度。
- bracketInNewLine!: Bool - 第一个括号是否换行，如果为 `true`，第一个括号将另起一行并且按照指定的深度缩进。
- indent!: String - 指定的缩进字符串，缩进字符串中只允许空格和制表符的组合，默认为两个空格。

返回值：

- String - 转换后的 JSON 格式字符串。

异常：

- IllegalArgumentException - 如果 depth 为负数，或 indent 中存在 ' ' 和 '\t' 以外的字符，则抛出异常。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [JsonString](encoding_json_package_classes.md#class-jsonstring) 转换为字符串。

返回值：

- String - 转换后的字符串。

### operator func [](Int64)

```cangjie
public operator func [](index: Int64): JsonValue
```

功能：获取 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 中指定索引的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

参数：

- index: Int64 - 指定的索引。

返回值：

- [JsonValue](encoding_json_package_classes.md#class-jsonvalue) - 对应索引的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果 index 不是 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 的有效索引，抛出异常。

## class JsonBool

```cangjie
public class JsonBool <: JsonValue {
    public init(bv: Bool)
}
```

功能：此类为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 实现子类，主要用于封装 true 或者 false 的 JSON 数据。

父类型：

- [JsonValue](#class-jsonvalue)

### init(Bool)

```cangjie
public init(bv: Bool)
```

功能：将指定的 Bool 类型实例封装成 [JsonBool](encoding_json_package_classes.md#class-jsonbool) 实例。

参数：

- bv: Bool - Bool 类型。

### func getValue()

```cangjie
public func getValue(): Bool
```

功能：获取 [JsonBool](encoding_json_package_classes.md#class-jsonbool) 中 value 的实际值。

返回值：

- Bool - value 的实际值。

### func kind()

```cangjie
public func kind(): JsonKind
```

功能：返回当前 [JsonBool](encoding_json_package_classes.md#class-jsonbool) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsBool）。

返回值：

- [JsonKind](encoding_json_package_enums.md#enum-jsonkind) - 当前 [JsonBool](encoding_json_package_classes.md#class-jsonbool) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsBool）。

### func toJsonString()

```cangjie
public func toJsonString(): String
```

功能：将 [JsonBool](encoding_json_package_classes.md#class-jsonbool) 转换为 JSON 格式的 (带有空格换行符) 字符串。

返回值：

- String - 转换后的 JSON 格式字符串。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [JsonBool](encoding_json_package_classes.md#class-jsonbool) 转换为字符串。

返回值：

- String - 转换后的字符串。

## class JsonFloat

```cangjie
public class JsonFloat <: JsonValue {
    public init(fv: Float64)
    public init(v: Int64)
}
```

功能：此类为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 实现子类，主要用于封装浮点类型的 JSON 数据。

父类型：

- [JsonValue](#class-jsonvalue)

### init(Float64)

```cangjie
public init(fv: Float64)
```

功能：将指定的 Float64 类型实例封装成 [JsonFloat](encoding_json_package_classes.md#class-jsonfloat) 实例。

参数：

- fv: Float64 - Float64 类型。

### init(Int64)

```cangjie
public init(v: Int64)
```

功能：将指定的 Int64 类型实例封装成 [JsonFloat](encoding_json_package_classes.md#class-jsonfloat) 实例。

参数：

- v: Int64 - Int64 类型。

### func getValue()

```cangjie
public func getValue(): Float64
```

功能：获取 [JsonFloat](encoding_json_package_classes.md#class-jsonfloat) 中 value 的实际值。

返回值：

- Float64 - value 的实际值。

### func kind()

```cangjie
public func kind(): JsonKind
```

功能：返回当前 [JsonFloat](encoding_json_package_classes.md#class-jsonfloat) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsFloat）。

返回值：

- [JsonKind](encoding_json_package_enums.md#enum-jsonkind) - 当前 [JsonFloat](encoding_json_package_classes.md#class-jsonfloat) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsFloat）。

### func toJsonString()

```cangjie
public func toJsonString(): String
```

功能：将 [JsonFloat](encoding_json_package_classes.md#class-jsonfloat) 转换为 JSON 格式的 (带有空格换行符) 字符串。

返回值：

- String - 转换后的 JSON 格式字符串。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [JsonFloat](encoding_json_package_classes.md#class-jsonfloat) 转换为字符串。

返回值：

- String - 转换后的字符串。

## class JsonInt

```cangjie
public class JsonInt <: JsonValue {
    public init(iv: Int64)
}
```

功能：此类为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 实现子类，主要用于封装整数类型的 JSON 数据。

父类型：

- [JsonValue](#class-jsonvalue)

### init(Int64)

```cangjie
public init(iv: Int64)
```

功能：将指定的 Int64 类型实例封装成 [JsonInt](encoding_json_package_classes.md#class-jsonint) 实例。

参数：

- iv: Int64 - 用于创建 [JsonInt](encoding_json_package_classes.md#class-jsonint) 的 Int64。

### func getValue()

```cangjie
public func getValue(): Int64
```

功能：获取 [JsonInt](encoding_json_package_classes.md#class-jsonint) 中 value 的实际值。

返回值：

- Int64 - value 的实际值。

### func kind()

```cangjie
public func kind(): JsonKind
```

功能：返回当前 [JsonInt](encoding_json_package_classes.md#class-jsonint) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsInt）。

返回值：

- [JsonKind](encoding_json_package_enums.md#enum-jsonkind) - 当前 [JsonInt](encoding_json_package_classes.md#class-jsonint) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsInt）。

### func toJsonString()

```cangjie
public func toJsonString(): String
```

功能：将 [JsonInt](encoding_json_package_classes.md#class-jsonint) 转换为 JSON 格式的 (带有空格换行符) 字符串。

返回值：

- String - 转换后的 JSON 格式字符串。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [JsonInt](encoding_json_package_classes.md#class-jsonint) 转换为字符串。

返回值：

- String - 转换后的字符串。

## class JsonNull

```cangjie
public class JsonNull <: JsonValue
```

功能：此类为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 实现子类，主要用于封装 null 的 JSON 数据。

父类型：

- [JsonValue](#class-jsonvalue)

### func kind()

```cangjie
public func kind(): JsonKind
```

功能：返回当前 [JsonNull](encoding_json_package_classes.md#class-jsonnull) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsNull）。

返回值：

- [JsonKind](encoding_json_package_enums.md#enum-jsonkind) - 当前 [JsonNull](encoding_json_package_classes.md#class-jsonnull) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsNull）。

### func toJsonString()

```cangjie
public func toJsonString(): String
```

功能：将 [JsonNull](encoding_json_package_classes.md#class-jsonnull) 转换为 JSON 格式的 (带有空格换行符) 字符串。

返回值：

- String - 转换后的 JSON 格式字符串。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [JsonNull](encoding_json_package_classes.md#class-jsonnull) 转换为字符串。

返回值：

- String - 转换后的字符串。

## class JsonObject

```cangjie
public class JsonObject <: JsonValue {
    public init()
    public init(map: HashMap<String, JsonValue>)
}
```

功能：此类为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 实现子类，主要用于封装 object 类型的 JSON 数据。

父类型：

- [JsonValue](#class-jsonvalue)

### init()

```cangjie
public init()
```

功能：创建空 [JsonObject](encoding_json_package_classes.md#class-jsonobject)。

### init(HashMap\<String, JsonValue>)

```cangjie
public init(map: HashMap<String, JsonValue>)
```

功能：将指定的 HashMap 类型实例封装成 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 实例。

参数：

- map: HashMap\<String, [JsonValue](encoding_json_package_classes.md#class-jsonvalue)> - data 数据。

### func containsKey(String)

```cangjie
public func containsKey(key: String): Bool
```

功能：判断 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 中是否存在 key。

参数：

- key: String - 指定的 key。

返回值：

- Bool - 存在返回 true，不存在返回 false。

### func get(String)

```cangjie
public func get(key: String): Option<JsonValue>
```

功能：获取 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 中 key 对应的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)，并用 Option\<[JsonValue](encoding_json_package_classes.md#class-jsonvalue)> 封装。

参数：

- key: String - 指定的 key。

返回值：

- Option\<[JsonValue](encoding_json_package_classes.md#class-jsonvalue)> - key 对应的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 的封装形式。

### func getFields()

```cangjie
public func getFields(): HashMap<String, JsonValue>
```

功能：获取 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 中的 fields 数据。

返回值：

- HashMap\<String, [JsonValue](encoding_json_package_classes.md#class-jsonvalue)> - [JsonObject](encoding_json_package_classes.md#class-jsonobject) 的 fields 数据。

### func kind()

```cangjie
public func kind(): JsonKind
```

功能：返回当前 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsObject）。

返回值：

- [JsonKind](encoding_json_package_enums.md#enum-jsonkind) - 当前 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsObject）。

### func put(String, JsonValue)

```cangjie
public func put(key: String, v: JsonValue): Unit
```

功能：向 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 中加入 key-[JsonValue](encoding_json_package_classes.md#class-jsonvalue) 数据。

参数：

- key: String - 需要加入的 key。
- v: [JsonValue](encoding_json_package_classes.md#class-jsonvalue) - 对应 key 的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

### func size()

```cangjie
public func size(): Int64
```

功能：获取 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 中 fields 存入 string-[JsonValue](encoding_json_package_classes.md#class-jsonvalue) 的数量。

返回值：

- Int64 - [JsonObject](encoding_json_package_classes.md#class-jsonobject) 中 fields 的大小。

### func toJsonString()

```cangjie
public func toJsonString(): String
```

功能：将 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 转换为 JSON 格式的 (带有空格换行符) 字符串。

返回值：

- String - 转换后的 JSON 格式字符串。

### func toJsonString(Int64, Bool, String)

```cangjie
public func toJsonString(depth: Int64, bracketInNewLine!: Bool = false, indent!: String = "  "): String
```

功能：将 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 转换为 Json 格式的字符串。该函数将指定初始的缩进深度、第一个括号后是否换行以及缩进字符串。

参数：

- depth: Int64 - 缩进深度。
- bracketInNewLine!: Bool - 第一个括号是否换行，如果为 `true`，第一个括号将另起一行并且按照指定的深度缩进。
- indent!: String - 指定的缩进字符串，缩进字符串中只允许空格和制表符的组合，默认为两个空格。

返回值：

- String - 转换后的 JSON 格式字符串。

异常：

- IllegalArgumentException - 如果 depth 为负数，或 indent 中存在 ' ' 和 '\t' 以外的字符，则抛出异常。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 转换为字符串。

返回值：

- String - 转换后的字符串。

### operator func [](String)

```cangjie
public operator func [](key: String): JsonValue
```

功能：获取 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 中 key 对应的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

参数：

- key: String - 指定的 key。

返回值：

- [JsonValue](encoding_json_package_classes.md#class-jsonvalue) - key 对应的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果 key 不是 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 的有效键，抛出异常。

## class JsonString

```cangjie
public class JsonString <: JsonValue {
    public init(sv: String)
}
```

功能：此类为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 实现子类，主要用于封装字符串类型的 JSON 数据。

父类型：

- [JsonValue](#class-jsonvalue)

### init(String)

```cangjie
public init(sv: String)
```

功能：将指定的 String 类型实例封装成 [JsonString](encoding_json_package_classes.md#class-jsonstring) 实例。

参数：

- sv: String - String 类型。

### func getValue()

```cangjie
public func getValue(): String
```

功能：获取 [JsonString](encoding_json_package_classes.md#class-jsonstring) 中 value 的实际值。

返回值：

- String - value 的实际值。

### func kind()

```cangjie
public func kind(): JsonKind
```

功能：返回当前 [JsonString](encoding_json_package_classes.md#class-jsonstring) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsString）。

返回值：

- [JsonKind](encoding_json_package_enums.md#enum-jsonkind) - 当前 [JsonString](encoding_json_package_classes.md#class-jsonstring) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型（JsString）。

### func toJsonString()

```cangjie
public func toJsonString(): String
```

功能：将 [JsonString](encoding_json_package_classes.md#class-jsonstring) 转换为 JSON 格式的 (带有空格换行符) 字符串。

返回值：

- String - 转换后的 JSON 格式字符串。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [JsonString](encoding_json_package_classes.md#class-jsonstring) 转换为字符串。

返回值：

- String - 转换后的字符串。

## class JsonValue

```cangjie
sealed abstract class JsonValue <: ToString
```

功能：此类为 JSON 数据层，主要用于 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 和 String 数据之间的互相转换。

抽象类 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 提供了 String 类型和具体的 JSON 类型相互转换的接口，以及具体的 JSON 类型判断功能。

父类型：

- ToString

示例：

使用示例见[JsonValue 和 String 互相转换](../json_samples/json_value_sample.md)。

### static func fromStr(String)

```cangjie
public static func fromStr(s: String): JsonValue
```

功能：将字符串数据解析为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。对于整数，支持前导 '0b'，'0o'，'0x'（不区分大小写），分别表示二进制，八进制和十六进制。字符串解析失败时将打印错误字符及其行数和列数，其中列数从错误字符所在行的非空格字符起开始计算。

JSON 在解析 String 转换为 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 时，转义字符 \\ 之后只能对应 JSON 支持的转义字符（b、f、n、r、t、u、\\、\"、\/），其中 \\u 的格式为：\\uXXXX，X 为十六进制数，例：\\u0041 代表字符 'A'。

参数：

- s: String - 传入字符串，暂不支持 "?" 和特殊字符。

返回值：

- [JsonValue](encoding_json_package_classes.md#class-jsonvalue) - 转换后的 [JsonValue](encoding_json_package_classes.md#class-jsonvalue)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果内存分配失败，或解析字符串出错，抛出异常。

示例：

```cangjie
import stdx.encoding.json.*

main() {
    println(JsonString("\b | \f | \n | \r | \t | A | \\ | \" | /").toString())
    println(JsonValue.fromStr("\"\\b\"").toString())
    println(JsonValue.fromStr("\"\\f\"").toString())
    println(JsonValue.fromStr("\"\\n\"").toString())
    println(JsonValue.fromStr("\"\\r\"").toString())
    println(JsonValue.fromStr("\"\\t\"").toString())
    println(JsonValue.fromStr("\"\\u0041\"").toString())
    println(JsonValue.fromStr("\"\\\\\"").toString())
    println(JsonValue.fromStr("\"\\\"\"").toString())
    println(JsonValue.fromStr("\"\\/\"").toString())
}
```

运行结果如下：

```text
"\b | \f | \n | \r | \t | A | \\ | \" | /"
"\b"
"\f"
"\n"
"\r"
"\t"
"A"
"\\"
"\""
"/"
```

### func asArray()

```cangjie
public func asArray(): JsonArray
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转换为 [JsonArray](encoding_json_package_classes.md#class-jsonarray) 格式。

返回值：

- [JsonArray](encoding_json_package_classes.md#class-jsonarray) - 转换后的 [JsonArray](encoding_json_package_classes.md#class-jsonarray)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果转换失败，抛出异常。

### func asBool()

```cangjie
public func asBool(): JsonBool
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转换为 [JsonBool](encoding_json_package_classes.md#class-jsonbool) 格式。

返回值：

- [JsonBool](encoding_json_package_classes.md#class-jsonbool) - 转换后的 [JsonBool](encoding_json_package_classes.md#class-jsonbool)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果转换失败，抛出异常。

### func asFloat()

```cangjie
public func asFloat(): JsonFloat
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转换为 [JsonFloat](encoding_json_package_classes.md#class-jsonfloat) 格式。

返回值：

- [JsonFloat](encoding_json_package_classes.md#class-jsonfloat) - 转换后的 [JsonFloat](encoding_json_package_classes.md#class-jsonfloat)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果转换失败，抛出异常。

### func asInt()

```cangjie
public func asInt(): JsonInt
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转换为 [JsonInt](encoding_json_package_classes.md#class-jsonint) 格式。

返回值：

- [JsonInt](encoding_json_package_classes.md#class-jsonint) - 转换后的 [JsonInt](encoding_json_package_classes.md#class-jsonint)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果转换失败，抛出异常。

### func asNull()

```cangjie
public func asNull(): JsonNull
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转换为 [JsonNull](encoding_json_package_classes.md#class-jsonnull) 格式。

返回值：

- [JsonNull](encoding_json_package_classes.md#class-jsonnull) - 转换后的 [JsonNull](encoding_json_package_classes.md#class-jsonnull)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果转换失败，抛出异常。

### func asObject()

```cangjie
public func asObject(): JsonObject
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转换为 [JsonObject](encoding_json_package_classes.md#class-jsonobject) 格式。

返回值：

- [JsonObject](encoding_json_package_classes.md#class-jsonobject) - 转换后的 [JsonObject](encoding_json_package_classes.md#class-jsonobject)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果转换失败，抛出异常。

### func asString()

```cangjie
public func asString(): JsonString
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转换为 [JsonString](encoding_json_package_classes.md#class-jsonstring) 格式。

返回值：

- [JsonString](encoding_json_package_classes.md#class-jsonstring) - 转换后的 [JsonString](encoding_json_package_classes.md#class-jsonstring)。

异常：

- [JsonException](encoding_json_package_exceptions.md#class-jsonexception) - 如果转换失败，抛出异常。

### func kind()

```cangjie
public func kind(): JsonKind
```

功能：返回当前 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型。

返回值：

- [JsonKind](encoding_json_package_enums.md#enum-jsonkind) - 当前 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 所属的 [JsonKind](encoding_json_package_enums.md#enum-jsonkind) 类型。

### func toJsonString()

```cangjie
public func toJsonString(): String
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转换为 JSON 格式的 (带有空格换行符) 字符串。

返回值：

- String - 转换后的 JSON 格式字符串。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [JsonValue](encoding_json_package_classes.md#class-jsonvalue) 转换为字符串。

返回值：

- String - 转换后的字符串。
