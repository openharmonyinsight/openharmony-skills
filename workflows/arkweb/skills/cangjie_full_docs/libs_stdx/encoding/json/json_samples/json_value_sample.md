# JsonValue 和 String 互相转换

下面是 JsonValue 和 String 互相转换的示例。该示例使用 JsonValue.fromStr 将一个 JSON 字符串转换为 JsonValue，随后以两种格式打印了该 JsonValue 对象。

示例：

<!-- verify -->
```cangjie
import stdx.encoding.json.*

main() {
    var str = ##"[true,"kjjjke\"eed",{"sdfd":"ggggg","eeeee":[341,false,{"nnnn":55.87}]},3422,22.341,false,[22,22.22,true,"ddd"],43]"##
    var jv: JsonValue = JsonValue.fromStr(str)
    var res = jv.toString()
    var prettyres = jv.toJsonString()
    println(res)
    println(prettyres)
}
```

运行结果：

```text
[true,"kjjjke\"eed",{"sdfd":"ggggg","eeeee":[341,false,{"nnnn":55.87}]},3422,22.341,false,[22,22.22,true,"ddd"],43]
[
  true,
  "kjjjke\"eed",
  {
    "sdfd": "ggggg",
    "eeeee": [
      341,
      false,
      {
        "nnnn": 55.87
      }
    ]
  },
  3422,
  22.341,
  false,
  [
    22,
    22.22,
    true,
    "ddd"
  ],
  43
]
```
