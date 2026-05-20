---
name: cangjie-stdx-json
description: "仓颉 stdx JSON 编解码用法。"
---

# 仓颉语言 JSON 编解码 Skill

## 1. 概述

仓颉通过扩展标准库（stdx）提供两个 JSON 包：

| 包 | 导入 | 适用场景 |
|---|---|---|
| **JSON 数据层** | `import stdx.encoding.json.*` | 解析/构建 JSON 值，适合简单读写 |
| **JSON 流式处理** | `import stdx.encoding.json.stream.*` | 流式处理，自定义类型与 JSON 互转，适合复杂场景 |

> 使用前需配置好 stdx，详见 `cangjie-stdx` Skill

---

## 2. JSON 数据层（stdx.encoding.json）

### 2.1 JsonValue 类型体系

| 类 | 对应 JSON | 获取值 |
|---|---|---|
| `JsonObject` | `{...}` | `get(key): Option<JsonValue>`、`operator[](key): JsonValue` |
| `JsonArray` | `[...]` | `get(index): Option<JsonValue>`、`operator[](index): JsonValue` |
| `JsonString` | `"..."` | `getValue(): String` |
| `JsonInt` | 整数 | `getValue(): Int64` |
| `JsonFloat` | 浮点数 | `getValue(): Float64` |
| `JsonBool` | `true/false` | `getValue(): Bool` |
| `JsonNull` | `null` | — |

通过 `kind(): JsonKind` 方法可判断类型，`JsonKind` 枚举值：`JsObject`、`JsArray`、`JsString`、`JsInt`、`JsFloat`、`JsBool`、`JsNull`。

### 2.2 解析 JSON 字符串

```cangjie
import stdx.encoding.json.*

main() {
    let str = ##"{"name": "Alice", "age": 30, "scores": [90, 85]}"##
    let jv = JsonValue.fromStr(str)

    // 访问对象字段
    let obj = jv.asObject()
    let name = obj["name"].asString().getValue()    // "Alice"
    let age = obj["age"].asInt().getValue()          // 30

    // 访问数组元素
    let scores = obj["scores"].asArray()
    let first = scores[0].asInt().getValue()         // 90
    println("${name}, ${age}, ${first}")
}
```

- `JsonValue.fromStr(s)` 将字符串解析为 `JsonValue`，失败抛出 `JsonException`
- `asObject()` / `asArray()` / `asInt()` 等向下转换，类型不符抛出 `JsonException`

### 2.3 构建 JSON

```cangjie
import stdx.encoding.json.*

main() {
    let obj = JsonObject()
    obj.put("name", JsonString("Bob"))
    obj.put("age", JsonInt(25))
    obj.put("active", JsonBool(true))

    let arr = JsonArray()
    arr.add(JsonInt(1))
    arr.add(JsonInt(2))
    obj.put("tags", arr)

    println(obj.toString())
    // {"name":"Bob","age":25,"active":true,"tags":[1,2]}

    println(obj.toJsonString())
    // 带缩进换行的格式化输出
}
```

### 2.4 类型判断与安全访问

```cangjie
import stdx.encoding.json.*

main() {
    let str = ##"{"value": 42}"##
    let jv = JsonValue.fromStr(str)
    let obj = jv.asObject()

    // 使用 get() 返回 Option，安全访问
    match (obj.get("value")) {
        case Some(v) => println(v.asInt().getValue())   // 42
        case None => println("key not found")
    }

    // 使用 containsKey 检查
    if (obj.containsKey("value")) {
        println(obj["value"].asInt().getValue())
    }

    // 使用 kind() 进行类型分发
    let val = obj["value"]
    match (val.kind()) {
        case JsInt => println("整数: ${val.asInt().getValue()}")
        case JsString => println("字符串: ${val.asString().getValue()}")
        case _ => println("其他类型")
    }
}
```

---

## 3. JSON 流式处理（stdx.encoding.json.stream）

适合自定义类型与 JSON 的互转，通过 `JsonWriter` 序列化、`JsonReader` 反序列化。

### 3.1 JsonWriter 序列化

```cangjie
import stdx.encoding.json.stream.*
import std.io.{ByteBuffer, readToEnd}

main() {
    let buf = ByteBuffer()
    let writer = JsonWriter(buf)

    writer.startObject()
    writer.writeName("name").writeValue("Alice")
    writer.writeName("age").writeValue(30)
    writer.writeName("scores")
    writer.startArray()
    writer.writeValue(90)
    writer.writeValue(85)
    writer.endArray()
    writer.endObject()
    writer.flush()

    println(String.fromUtf8(readToEnd(buf)))
    // {"name":"Alice","age":30,"scores":[90,85]}
}
```

### 3.2 JsonReader 反序列化

```cangjie
import stdx.encoding.json.stream.*
import std.io.ByteBuffer

main() {
    let jsonStr = ##"{"name":"Alice","age":30}"##
    var buf = ByteBuffer()
    unsafe { buf.write(jsonStr.rawData()) }
    let reader = JsonReader(buf)

    reader.startObject()
    while (let Some(token) <- reader.peek()) {
        if (token == EndObject) {
            break
        }
        let key = reader.readName()
        match (key) {
            case "name" =>
                let name: String = reader.readValue<String>()
                println("name = ${name}")
            case "age" =>
                let age: Int64 = reader.readValue<Int64>()
                println("age = ${age}")
            case _ => reader.skip()
        }
    }
    reader.endObject()
}
```

- `peek(): Option<JsonToken>` 查看下一个 token 类型，不消耗
- `readName()` 读取字段名，`readValue<T>()` 读取值（`T` 须实现 `JsonDeserializable<T>`）
- `skip()` 跳过当前值

### 3.3 自定义类型序列化（JsonSerializable）

实现 `JsonSerializable` 接口使自定义类型支持 `writeValue`：

```cangjie
import stdx.encoding.json.stream.*
import std.io.{ByteBuffer, readToEnd}

class Image <: JsonSerializable {
    var width: Int64 = 0
    var height: Int64 = 0
    var title: String = ""

    public func toJson(w: JsonWriter): Unit {
        w.startObject()
        w.writeName("width").writeValue(width)
        w.writeName("height").writeValue(height)
        w.writeName("title").writeValue(title)
        w.endObject()
    }
}

main() {
    let img = Image()
    img.width = 800
    img.height = 600
    img.title = "仓颉示例"

    let buf = ByteBuffer()
    let writer = JsonWriter(buf)
    writer.writeValue(img)
    writer.flush()
    println(String.fromUtf8(readToEnd(buf)))
    // {"width":800,"height":600,"title":"仓颉示例"}
}
```

### 3.4 自定义类型反序列化（JsonDeserializable）

实现 `JsonDeserializable<T>` 接口使自定义类型支持 `readValue<T>()`：

```cangjie
import stdx.encoding.json.stream.*
import std.io.ByteBuffer

class User <: JsonDeserializable<User> {
    var name: String = ""
    var age: Int64 = 0

    public static func fromJson(r: JsonReader): User {
        let u = User()
        r.startObject()
        while (let Some(token) <- r.peek()) {
            if (token == EndObject) {
                break
            }
            match (r.readName()) {
                case "name" => u.name = r.readValue<String>()
                case "age" => u.age = r.readValue<Int64>()
                case _ => r.skip()
            }
        }
        r.endObject()
        return u
    }
}

main() {
    let jsonStr = ##"{"name":"Bob","age":25}"##
    var buf = ByteBuffer()
    unsafe { buf.write(jsonStr.rawData()) }
    let reader = JsonReader(buf)
    let user = reader.readValue<User>()
    println("${user.name}, ${user.age}")   // Bob, 25
}
```

### 3.5 WriteConfig 格式控制

```cangjie
import stdx.encoding.json.stream.*
import std.io.{ByteBuffer, readToEnd}

main() {
    let buf = ByteBuffer()
    let writer = JsonWriter(buf)

    // 使用 pretty 格式（带换行和 4 空格缩进）
    writer.writeConfig = WriteConfig.pretty

    writer.startObject()
    writer.writeName("key").writeValue("value")
    writer.endObject()
    writer.flush()
    println(String.fromUtf8(readToEnd(buf)))
    // {
    //     "key": "value"
    // }
}
```

| 预设 | 说明 |
|------|------|
| `WriteConfig.compact` | 紧凑格式，无空格换行（默认） |
| `WriteConfig.pretty` | 格式化输出，4 空格缩进 |

可自定义属性：`newline`、`indent`、`useSpaceAfterSeparators`、`htmlSafe`、`dateTimeFormat`。

### 3.6 readValue 内置支持类型

`readValue<T>()` 和 `writeValue(v)` 已内置支持以下类型（无需自行实现接口）：

| 类别 | 类型 |
|------|------|
| 整数 | `Int8` ~ `Int64`，`UInt8` ~ `UInt64` |
| 浮点 | `Float16`~`Float64` |
| 布尔 | `Bool` |
| 字符串 | `String` |
| 集合 | `Array<T>`、`ArrayList<T>`、`HashMap<String, T>` |
| 可选 | `Option<T>` |
| 其他 | `BigInt`、`Decimal`、`DateTime`（RFC 3339 格式） |

---

## 4. 数据层与流式处理的选择

| 场景 | 推荐 |
|------|------|
| 解析未知结构的 JSON | `JsonValue.fromStr()` + `kind()` 判断 |
| 简单读取已知字段 | `JsonValue.fromStr()` + `asObject()["key"]` |
| 手动构建 JSON 输出 | `JsonObject` / `JsonArray` + `put` / `add` |
| 自定义类型 ↔ JSON 互转 | `JsonSerializable` / `JsonDeserializable<T>` + 流式 API |
| 大数据量流式处理 | `JsonReader` / `JsonWriter` |

---

## 5. 注意事项

| 要点 | 说明 |
|------|------|
| **stdx 配置** | JSON 包属于 stdx，需先下载配置（详见 `cangjie-stdx` Skill） |
| **异常处理** | `fromStr()` 解析失败、类型转换不匹配均抛出 `JsonException` |
| **`operator[]` vs `get()`** | `operator[]` 键/索引不存在时抛异常；`get()` 返回 `Option`，更安全 |
| **JsonReader 状态** | `startObject/endObject`、`startArray/endArray` 须严格配对 |
| **flush** | `JsonWriter` 写完后须调用 `flush()` 确保数据输出 |
| **转义字符** | `fromStr` 支持 JSON 标准转义：`\b`、`\f`、`\n`、`\r`、`\t`、`\uXXXX`、`\\`、`\"`、`\/` |
