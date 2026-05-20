# ArrayList 的 remove/clear/slice 函数

此用例展示了 ArrayList 的 remove/clear/slice 函数的使用方法。

代码如下：

<!-- verify -->

```cangjie
import std.collection.*

main() {
    var list: ArrayList<Int64> = ArrayList<Int64>([97, 100, 99]) // Function call syntactic sugar of variable-length
    list.remove(at: 1) // list: [97, 99]
    var b = list.get(1)
    print("b=${b.getOrThrow()},")
    list.clear()
    list.add(11) // list: [11]
    var arr: Array<Int64> = [1, 2, 3]
    list.add(all: arr, at: 0) // list: [1, 2, 3, 11]
    var g = list.get(0)
    print("g=${g.getOrThrow()},")
    let r: Range<Int64> = 1..=2 : 1
    var sublist: ArrayList<Int64> = list.slice(r) // sublist: [2, 3]
    var m = sublist.get(0)
    print("m=${m.getOrThrow()}")
    return 0
}
```

运行结果：

```text
b=99,g=1,m=2
```
