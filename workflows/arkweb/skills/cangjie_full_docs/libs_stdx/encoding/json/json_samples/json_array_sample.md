# JsonArray 使用示例

下面是 JsonArray 使用示例。该示例构造了一个 JsonArray 对象，并向其中添加了一些 JsonValue，最后以两种格式打印了该 JsonArray 对象。

示例：

<!-- verify -->
```cangjie
import stdx.encoding.json.*
import std.collection.*

main() {
    var a: JsonValue = JsonNull()
    var b: JsonValue = JsonBool(true)
    var c: JsonValue = JsonBool(false)
    var d: JsonValue = JsonInt(7363)
    var e: JsonValue = JsonFloat(736423.546)
    var list: ArrayList<JsonValue> = ArrayList<JsonValue>()
    var list2: ArrayList<JsonValue> = ArrayList<JsonValue>()
    var map = JsonObject()
    var map1 = JsonObject()
    map1.put("a", JsonString("jjjjjj"))
    map1.put("b", b)
    map1.put("c", JsonString("hhhhh"))
    list2.add(b)
    list2.add(JsonInt(3333333))
    list2.add(map1)
    list2.add(JsonString("sdfghgfasd"))
    list.add(b)
    list.add(a)
    list.add(map)
    list.add(c)
    list.add(JsonArray(list2))
    list.add(d)
    list.add(JsonString("ddddddd"))
    list.add(e)
    var result: JsonValue = JsonArray(list)
    println("func toString result is:")
    println(result.toString())
    println("func toJsonString result is:")
    println(result.toJsonString())
}
```

运行结果：

```text
func toString result is:
[true,null,{},false,[true,3333333,{"a":"jjjjjj","b":true,"c":"hhhhh"},"sdfghgfasd"],7363,"ddddddd",736423.546]
func toJsonString result is:
[
  true,
  null,
  {},
  false,
  [
    true,
    3333333,
    {
      "a": "jjjjjj",
      "b": true,
      "c": "hhhhh"
    },
    "sdfghgfasd"
  ],
  7363,
  "ddddddd",
  736423.546
]

```
