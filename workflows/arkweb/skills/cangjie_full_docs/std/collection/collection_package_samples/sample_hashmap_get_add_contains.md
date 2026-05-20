# HashMap 的 get/add/contains 函数

此用例展示了 HashMap 的基本使用方法。

代码如下：

<!-- verify -->

```cangjie
import std.collection.*

main() {
    var map: HashMap<String, Int64> = HashMap<String, Int64>()
    map.add("a", 99) // map : [("a", 99)]
    map.add("b", 100) // map : [("a", 99), ("b", 100)]
    var a = map.get("a")
    var bool = map.contains("a")
    print("a=${a.getOrThrow()} ")
    print("bool=${bool.toString()}")
    return 0
}
```

运行结果：

```text
a=99 bool=true
```
