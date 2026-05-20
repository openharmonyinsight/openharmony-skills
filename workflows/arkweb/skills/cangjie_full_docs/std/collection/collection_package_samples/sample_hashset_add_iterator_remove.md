# HashSet 的 add/iterator/remove 函数

此用例展示了 HashSet 的基本使用方法。

代码如下：

<!-- verify -->

```cangjie
import std.collection.*
/* 测试 */
main() {
    var set: HashSet<String> = HashSet<String>() // set: []
    set.add("apple") // set: ["apple"]
    set.add("banana") // set: ["apple", "banana"], not in order
    set.add("orange") // set: ["apple", "banana", "orange"], not in order
    set.add("peach") // set: ["apple", "banana", "orange", "peach"], not in order
    var itset = set.iterator()
    while (true) {
        var value = itset.next()
        match (value) {
            case Some(v) =>
                if (!set.contains(v)) {
                    print("Operation failed")
                    return 1
                } else {
                    println(v)
                }
            case None => break
        }
    }
    set.remove("apple") // set: ["banana", "orange", "peach"], not in order
    println(set)
    return 0
}
```

由于 Set 中的顺序不是固定的，因此运行结果可能如下：

```text
apple
banana
orange
peach
[banana, orange, peach]
```
