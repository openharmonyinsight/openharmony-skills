# 类

## class ObjectPool\<T> where T <: Object <sup>(deprecated)</sup>

```cangjie
public class ObjectPool<T> where T <: Object {
    public init(newFunc: () -> T, resetFunc!: Option<(T) -> T> = None)
}
```

功能：此类提供了一个并发安全的对象缓存类型，该类型可以储存已经分配内存但未使用的对象。

当一个对象不需要使用时可以将对象存入 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated)，当需要使用对象时再从该 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 中取出。

储存在一个 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 中的对象只能是同一种类型。

在一个 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 对象的生命周期结束前，该 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 对象中存储的对象不会被释放。

> **注意：**
>
> 未来版本即将废弃。

示例：

<!-- verify -->
```cangjie
import std.objectpool.*

class City {
    var id: Int64 = 0
    var name: String = ""
}

func resetCity(c: City): City {
    let city = c
    city.id = 0
    city.name = ""
    return city
}

main() {
    let cityPool = ObjectPool({=> City()}, resetFunc: resetCity)
    let cityA = cityPool.get()
    cityA.id = 30
    cityA.name = "A"
    println("id: ${cityA.id}, name: ${cityA.name}")
    cityPool.put(cityA)
}
```

运行结果：

```text
id: 30, name: A
```

### init(() -> T, Option\<(T) -> T>)

```cangjie
public init(newFunc: () -> T, resetFunc!: Option<(T) -> T> = None)
```

功能：创建新的 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 对象。

参数：

- newFunc: () ->T - 当调用 get 方法时，若从 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 中获取对象失败，则调用 newFn 创建一个新对象，newFunc 应保证并发安全。
- resetFunc!: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<(T) ->T> - 调用 get 方法时会调用 resetFunc 重置对象状态，resetFunc 为 None 表示不重置， resetFunc 应保证并发安全。

### func get()

```cangjie
public func get(): T
```

功能：尝试从 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 中获取对象， 若从 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 中获取对象失败，则调用 newFunc 创建新的对象并返回该对象 get 的对象不使用之后应该通过 put 归还给 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated)。

返回值：

- T - 从 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 中获取到的对象或调用 newFunc 新建的对象。

### func put(T)

```cangjie
public func put(item: T): Unit
```

功能：尝试将对象放入 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 中，不保证一定会将对象放入 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 在对一个对象调用 put 后不应该再对该对象进行任何操作，否则可能导致非预期问题。

参数：

- item: T - 需要放入 [ObjectPool](objectpool_package_classes.md#class-objectpoolt-where-t--object-deprecated) 的对象。
