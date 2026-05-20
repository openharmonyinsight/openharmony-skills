# 使用 Json Stream 进行反序列化

示例：

<!-- verify -->
```cangjie
import stdx.encoding.json.stream.*
import std.io.*
import std.collection.*

class A <: JsonDeserializable<A> {
    var key1: Option<String> = None
    var key2: Bool = false
    var key3: Float64 = 0.0
    var key4: String = ""
    var key5: Array<Int64> = Array<Int64>()
    var key6: HashMap<String, String> = HashMap<String, String>()

    public static func fromJson(r: JsonReader): A {
        var res = A()
        while (let Some(v) <- r.peek()) {
            match (v) {
                case BeginObject =>
                    r.startObject()
                    while (r.peek() != EndObject) {
                        let n = r.readName()
                        match (n) {
                            case "key1" => res.key1 = r.readValue<Option<String>>()
                            case "key2" => res.key2 = r.readValue<Bool>()
                            case "key3" => res.key3 = r.readValue<Float64>()
                            case "key4" => res.key4 = r.readValue<String>()
                            case "key5" => res.key5 = r.readValue<Array<Int64>>()
                            case "key6" => res.key6 = r.readValue<HashMap<String, String>>()
                            case _ => ()
                        }
                    }
                    r.endObject()
                    break
                case _ => throw Exception()
            }
        }
        return res
    }

    func toString(): String {
        return "${key1}\n${key2}\n${key3}\n${key4}\n${key5}\n${key6}"
    }
}

main() {
    let jsonStr = ##"{"key1": null, "key2": true, "key3": 123.456, "key4": "string", "key5": [123, 456], "key6": {"key7": " ", "key8": "\\a"}}"##
    var bas = ByteBuffer()
    unsafe { bas.write(jsonStr.rawData()) }
    var reader = JsonReader(bas)
    var obj = A.fromJson(reader)
    println(obj.toString())
}
```

运行结果：

```text
None
true
123.456000
string
[123, 456]
[(key7,  ), (key8, \a)]
```
