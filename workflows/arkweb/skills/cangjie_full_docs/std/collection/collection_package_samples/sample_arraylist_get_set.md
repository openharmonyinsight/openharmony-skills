# ArrayList 的 get/set 函数

此用例展示了如何使用 get 方法获取 ArrayList 中对应索引的值，以及如何修改值。

代码如下：

<!-- verify -->

```cangjie
import std.collection.*

main() {
    var list = ArrayList<Int64>([97, 100]) // list: [97, 100]

    // 修改值
    list[1] = 120 // list: [97, 120]

    // 获取值
    var b = list.get(1)
    print("b=${b.getOrThrow()}")
    return 0
}
```

运行结果：

```text
b=120
```
