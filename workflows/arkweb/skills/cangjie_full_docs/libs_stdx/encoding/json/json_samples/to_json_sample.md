# JsonValue 与 DataModel 的转换

下面是 JSON 字符串与自定义类型间的转换的示例。该用例为 Person 类型实现了 Serializable 接口，随后进行了从 JSON 字符串到自定义类型的转换和从自定义类型到 JSON 字符串的转换。

示例：

<!-- verify -->
```cangjie
import stdx.serialization.serialization.*
import stdx.encoding.json.*

class Person <: Serializable<Person> {
    var name: String = ""
    var age: Int64 = 0
    var loc: Option<Location> = Option<Location>.None

    public func serialize(): DataModel {
        return DataModelStruct()
            .add(field<String>("name", name))
            .add(field<Int64>("age", age))
            .add(field<Option<Location>>("loc", loc))
    }

    public static func deserialize(dm: DataModel): Person {
        var dms = match (dm) {
            case data: DataModelStruct => data
            case _ => throw Exception("this data is not DataModelStruct")
        }
        var result = Person()
        result.name = String.deserialize(dms.get("name"))
        result.age = Int64.deserialize(dms.get("age"))
        result.loc = Option<Location>.deserialize(dms.get("loc"))
        return result
    }
}

class Location <: Serializable<Location> {
    var country: String = ""
    var province: String = ""

    public func serialize(): DataModel {
        return DataModelStruct().add(field<String>("country", country)).add(field<String>("province", province))
    }

    public static func deserialize(dm: DataModel): Location {
        var dms = match (dm) {
            case data: DataModelStruct => data
            case _ => throw Exception("this data is not DataModelStruct")
        }
        var result = Location()
        result.country = String.deserialize(dms.get("country"))
        result.province = String.deserialize(dms.get("province"))
        return result
    }
}

main() {
    var js = ##"{
    "name": "A",
    "age": 30,
    "loc": {
        "country": "China",
        "province": "Beijing"
    }
}"##

    /* 实现从 JSON 字符串到自定义类型的转换 */
    var jv = JsonValue.fromStr(js)
    var dm = DataModel.fromJson(jv)
    var A = Person.deserialize(dm)
    println("name == ${A.name}")
    println("age == ${A.age}")
    println("country == ${A.loc.getOrThrow().country}")
    println("province == ${A.loc.getOrThrow().province}")
    println("====================")

    /* 实现从自定义类型到 JSON 字符串的转换 */
    dm = A.serialize()
    var jo = dm.toJson().asObject()
    println(jo.toJsonString())
}
```

运行结果：

```text
name == A
age == 30
country == China
province == Beijing
====================
{
  "name": "A",
  "age": 30,
  "loc": {
    "country": "China",
    "province": "Beijing"
  }
}
```
