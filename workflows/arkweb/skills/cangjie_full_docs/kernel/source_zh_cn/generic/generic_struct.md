# 泛型结构体

struct 类型的泛型与 class 是类似的，下面可以使用 struct 定义一个类似于二元元组的类型：

<!-- verify -->

```cangjie
struct Pair<T, U> {
    let x: T
    let y: U
    public init(a: T, b: U) {
        x = a
        y = b
    }
    public func first(): T {
        return x
    }
    public func second(): U {
        return y
    }
}

main() {
    var a: Pair<String, Int64> = Pair<String, Int64>("hello", 0)
    println(a.first())
    println(a.second())
}
```

程序输出的结果为：

```text
hello
0
```

在 `Pair` 中提供了 `first` 与 `second` 两个函数来取得元组的第一个与第二个元素。
