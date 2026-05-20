# Form 的构造使用

## Form 的构造与其函数 get 的使用

创建 Form 类，并通过 get 获取 key 对应映射的 value。示例中使用 Form 类的函数 get 获取指定 key = 1 的 value 值 2 。

示例：

<!-- verify -->
```cangjie
import stdx.encoding.url.*

main(): Int64 {
    var s = Form("1=2&2=3&1=2&&")
    print(s.get("1").getOrThrow())
    return 0
}
```

运行结果：

```text
2
```

## Form 的构造与重复 key 情况下函数 get 的使用

创建 Form 类，并通过 get 获取 key 对应映射的 value。示例中使用 Form 类的函数 get 获取指定 key = 1 的第一个 value 值 %6AD。value 中的 %6A 被解码为 j，因此得到 value 值 jD 。

示例：

<!-- verify -->
```cangjie
import stdx.encoding.url.*

main(): Int64 {
    var s = Form("2=3&1=%6AD&1=2")
    /* 对于 %6A 解码成 j，重复的 key 调用 get 获取第一个 value 值 jD */
    print(s.get("1").getOrThrow())
    return 0
}
```

运行结果如下：

```text
jD
```

## Form 的构造与其他函数使用

分别调用 add，set，clone，打印输出前后变化。

示例：

<!-- verify -->
```cangjie
import stdx.encoding.url.*

main(): Int64 {
    var f = Form()

    /* 给键 k 增加值 v1 和 v2 */
    f.add("k", "v1")
    f.add("k", "v2")

    /* 调用 get 方法时，获取的是第一个值 */
    println(f.get("k").getOrThrow())

    /* 设定键 k 的值为 v */
    f.set("k", "v")
    println(f.get("k").getOrThrow())
    let clone_f = f.clone()

    /* 给克隆出来的 clone_f 增加键值对 */
    clone_f.add("k1", "v1")

    /* 通过 get 获得值 v1 */
    println(clone_f.get("k1").getOrThrow())

    /* 原来的 f 并没有键 k1，所以值是给的默认值 kkk */
    println(f.get("k1") ?? "kkk")
    return 0
}
```

运行结果如下：

```text
v1
v
v1
kkk
```
