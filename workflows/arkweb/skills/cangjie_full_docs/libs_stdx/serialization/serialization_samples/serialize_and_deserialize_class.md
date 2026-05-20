# class 序列化和反序列化
<!-- verify -->

```cangjie
import stdx.serialization.serialization.*
import std.math.*
import stdx.encoding.json.*

/* 通过实现 Serializable 接口，来实现对自定义类型的序列化和反序列化功能 */
class Abc <: Serializable<Abc> {
    var name: String = "Abcde"
    var age: Int64 = 555
    var loc: Option<Location> = Option<Location>.None

    /* 实现 Serializable 接口的序列化方法 */
    public func serialize(): DataModel {
        return DataModelStruct()
            .add(field<String>("name", name))
            .add(field<Int64>("age", age))
            .add(field<Option<Location>>("loc", loc))
    }

    /* 实现反序列化方法 */
    public static func deserialize(dm: DataModel): Abc {
        let dms = match (dm) {
            case data: DataModelStruct => data
            case _ => throw Exception("this data is not DataModelStruct")
        }
        let result = Abc()
        result.name = String.deserialize(dms.get("name"))
        result.age = Int64.deserialize(dms.get("age"))
        result.loc = Option<Location>.deserialize(dms.get("loc"))
        return result
    }
}

class Location <: Serializable<Location> {
    var time: Int64 = 666
    var heheh: Rune = 'T'

    /* 实现 Serializable 接口的序列化方法 */
    public func serialize(): DataModel {
        return DataModelStruct().add(field<Int64>("time", time)).add(field<Rune>("heheh", heheh))
    }

    /* 实现反序列化方法 */
    public static func deserialize(dm: DataModel): Location {
        let dms = match (dm) {
            case data: DataModelStruct => data
            case _ => throw Exception("this data is not DataModelStruct")
        }
        let result = Location()
        result.time = Int64.deserialize(dms.get("time"))
        result.heheh = Rune.deserialize(dms.get("heheh"))
        return result
    }
}

main(): Unit {
    let dd = Abc()
    let aa: JsonValue = dd.serialize().toJson()
    let bb: JsonObject = (aa as JsonObject).getOrThrow()
    let v1 = (bb.get("name").getOrThrow() as JsonString).getOrThrow()
    let v2 = (bb.get("age").getOrThrow() as JsonInt).getOrThrow()
    let v3 = bb.get("loc").getOrThrow()
    println(v1.getValue())
    println(v2.getValue())
    println(v3.toString())
    println("===========")
    let aaa = ##"{"age": 123, "loc": { "heheh": "H", "time": 45 }, "name": "zhangsan"}"##
    let bbb = JsonValue.fromStr(aaa)
    let ccc = (bbb as JsonObject).getOrThrow()
    let v4 = (ccc.get("name").getOrThrow() as JsonString).getOrThrow()
    let v5 = (ccc.get("age").getOrThrow() as JsonInt).getOrThrow()
    let v6 = (ccc.get("loc").getOrThrow() as JsonObject).getOrThrow()
    let v7 = (v6.get("time").getOrThrow() as JsonInt).getOrThrow()
    let v8 = (v6.get("heheh").getOrThrow() as JsonString).getOrThrow()
    println(v4.getValue())
    println(v5.getValue())
    println(v7.getValue())
    println(v8.getValue())
}
```

运行结果如下：

```text
Abcde
555
null
===========
zhangsan
123
45
H
```
