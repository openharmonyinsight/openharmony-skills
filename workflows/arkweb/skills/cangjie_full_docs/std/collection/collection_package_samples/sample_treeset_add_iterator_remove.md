# TreeSet 的 add/iterator/remove 函数

此用例展示了 TreeSet 的基本使用方法。

代码如下：

<!-- verify -->

```cangjie
import std.collection.*
/* 测试 */
main() {
    var set: TreeSet<String> = TreeSet<String>()
    set.add("peach")
    set.add("banana")
    set.add("apple")
    set.add("orange")

    var itset = set.iterator()
    for (e in itset) {
        println(e)
    }

    set.remove("banana")
    println(set)
    return 0
}
```

运行结果：

```text
apple
banana
orange
peach
[apple, orange, peach]
```
