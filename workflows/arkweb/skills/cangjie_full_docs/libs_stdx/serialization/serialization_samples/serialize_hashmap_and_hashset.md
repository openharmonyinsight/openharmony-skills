# HashSet 和 HashMap 序列化
<!-- verify -->

```cangjie
import std.collection.*
import stdx.serialization.serialization.*
import stdx.encoding.json.*

main(): Unit {
    let s: HashSet<Values> = HashSet<Values>([Values(3), Values(5), Values(7)])
    let seris: DataModel = s.serialize()
    println(seris.toJson().toJsonString())
    println("===========")
    let m: HashMap<String, Values> = HashMap<String, Values>([("1", Values(3)), ("2", Values(6)), ("3", Values(9))])
    let serim: DataModel = m.serialize()
    print(serim.toJson().toJsonString())
}

class Values <: Hashable & Equatable<Values> & Serializable<Values> {
    var m_data: Int64

    init(m_data: Int64) {
        this.m_data = m_data
    }

    public func hashCode(): Int64 {
        return this.m_data
    }

    public operator func ==(right: Values): Bool {
        return this.m_data == right.m_data
        
    }

    public operator func !=(right: Values): Bool {
        return this.m_data != right.m_data
    }

    /* 实现 Serializable 接口的序列化方法 */
    public func serialize(): DataModel {
        return DataModelStruct().add(field<Int64>("m_data", m_data))
    }

    /* 实现反序列化方法 */
    public static func deserialize(dm: DataModel): Values {
        let dms: DataModelStruct = match (dm) {
            case data: DataModelStruct => data
            case _ => throw Exception("this data is not DataModelStruct")
        }
        let result = Values(0)
        result.m_data = Int64.deserialize(dms.get("m_data"))
        return result
    }
}
```

运行结果如下：

```text
[
  {
    "m_data": 3
  },
  {
    "m_data": 5
  },
  {
    "m_data": 7
  }
]
===========
{
  "1": {
    "m_data": 3
  },
  "2": {
    "m_data": 6
  },
  "3": {
    "m_data": 9
  }
}
```
