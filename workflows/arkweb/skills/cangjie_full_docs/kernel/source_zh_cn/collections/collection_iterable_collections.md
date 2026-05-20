# Iterable 和 Collections

前面已经了解过 Range、Array、ArrayList，它们都可以使用 for-in 进行遍历操作。对于开发者自定义的类型，也能实现类似的遍历操作。

Range、Array、ArrayList 都是通过 Iterable 来支持 for-in 语法的。

Iterable 是如下形式（只展示了核心代码）的一个内置 interface。

```cangjie
interface Iterable<T> {
    func iterator(): Iterator<T>
    ...
}
```

iterator 函数要求返回的 Iterator 类型是如下形式（只展示了核心代码）的另一个内置 interface。

```cangjie
interface Iterator<T> <: Iterable<T> {
    mut func next(): Option<T>
    ...
}
```

可以使用 for-in 语法来遍历任何一个实现了 Iterable 接口类型的实例。

假设有这样一段 for-in 代码，如下所示。

<!-- run -->

```cangjie
let list = [1, 2, 3]
for (i in list) {
    println(i)
}
```

它等价于如下形式的 while 代码。

<!-- run -->

```cangjie
let list = [1, 2, 3]
var it = list.iterator()
while (true) {
    match (it.next()) {
        case Some(i) => println(i)
        case None => break
    }
}
```

另外一种常见的遍历 Iterable 类型的方法是在 while 表达式的条件中使用模式匹配，比如上面 while 代码的另一种等价写法是：

<!-- run -->

```cangjie
let list = [1, 2, 3]
var it = list.iterator()
while (let Some(i) <- it.next()) {
    println(i)
}
```

Array、ArrayList、HashSet、HashMap 类型都实现了 Iterable，因此可以将其用在 for-in 或者 while 中。
