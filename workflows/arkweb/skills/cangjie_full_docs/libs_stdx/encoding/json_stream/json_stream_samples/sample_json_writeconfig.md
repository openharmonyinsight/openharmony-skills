# WriteConfig 使用示例

示例：

<!-- verify -->
```cangjie
import stdx.encoding.json.stream.{JsonWriter, WriteConfig, JsonSerializable}
import std.io.ByteBuffer

main() {
    /* 构造 JsonWriter */
    let buffer = ByteBuffer()
    let writer = JsonWriter(buffer)

    /* 设置 JSON 写格式配置 */
    let fmtCfg = WriteConfig.pretty
    writer.writeConfig = fmtCfg

    /* 写 JSON  */
    writer.writeValue(MyObj())

    /* 打印 JSON 序列化字符串 */
    println(String.fromUtf8(buffer.bytes()))
}

class MyObj <: JsonSerializable {
    public func toJson(w: JsonWriter): Unit {
        w.startObject()
        w.writeName("Name").writeValue("zhangsan")
        w.writeName("Age").writeValue(18)
        w.writeName("Scores").writeValue([88.8, 99.9])
        w.writeName("Class")
        w.startObject()
        w.writeName("Name").writeValue("Class A")
        w.writeName("Students Number").writeValue(33)
        w.endObject()
        w.endObject()
        w.flush()
    }
}
```

运行结果：

```text
{
    "Name": "zhangsan",
    "Age": 18,
    "Scores": [
        88.8,
        99.9
    ],
    "Class": {
        "Name": "Class A",
        "Students Number": 33
    }
}
```