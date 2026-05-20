# WeakRef 用于缓存

以下使用 `WeakRef` 实现了一个缓存，假设某个数据的计算非常耗时，我们希望将其计算结果缓存起来，但又不希望过量缓存导致 OOM ，那么我们可以使用弱引用。

<!-- verify -->
```cangjie
import std.ref.{WeakRef, CleanupPolicy}

public interface Cacheable<T> {
    static func reCalculate() : T
}

public class Data <: Cacheable<Data> {
    public var number: Int64

    init(n : Int64) {
                number = n
    }

    public static func reCalculate(): Data {
        // 模拟运算
        println("re-calculations!")
        let data = Data(321)
        return data
    }
}

public class Cache<T> where T <: Object & Cacheable<T> {
    private var cache : WeakRef<T>

    public init(data: T) {
        cache = WeakRef<T>(data, CleanupPolicy.DEFERRED) // 这里我们选用 DEFERRED 策略，因为我们希望 Data 保存的尽量久。
    }

    public func getData(): T {
        match(cache.value) {
            case Some(x) => x
            case None =>
                // 如果 GC 释放了缓存中的数据则重新运算
                let data = T.reCalculate()
                cache = WeakRef<T>(data, CleanupPolicy.DEFERRED)
                data
        }
    }

    public func clear() : Unit {
        cache.clear()
    }
}

main () {
    let data = Data(123)
    var c = Cache<Data>(data)
    println(c.getData().number) // 直接从缓存中读取数据，不需要重新运算
    println(c.getData().number) // 直接从缓存中读取数据，不需要重新运算
    c.clear()                   // 清空缓存
    println(c.getData().number) // 重新运算
    return 0
}
```

运行结果：

```text
123
123
re-calculations!
321
```
