# ArrayList 的 add 函数

ArrayList 中添加元素的方法如下：

<!-- verify -->

```cangjie
import std.collection.*

main() {
    var list: ArrayList<Int64> = ArrayList<Int64>(10) // 创建一个容量为 10 的 ArrayList
    var arr: Array<Int64> = [1, 2, 3]
    list.add(all: arr) // list: [1, 2, 3]
    list[1] = 120 // list: [1, 120, 3]
    var b = list.get(2)
    print("b=${b.getOrThrow()},")
    list.add(12, at: 1) // list: [1, 12, 120, 3]
    var c = list.get(2)
    print("c=${c.getOrThrow()},")
    var arr1: Array<Int64> = [1, 2, 3]
    list.add(all: arr1, at: 1) // list: [1, 1, 2, 3, 12, 120, 3]
    var d = list.get(2)
    print("d=${d.getOrThrow()}")
    return 0
}
```

运行结果：

```text
b=3,c=120,d=2
```
