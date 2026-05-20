# 类

## class ArrayBlockingQueue\<E>

```cangjie
public class ArrayBlockingQueue<E> {
    public let capacity: Int64
    public init(capacity: Int64)
    public init(capacity: Int64, elements: Collection<E>)
}
```

功能：基于数组实现的 Blocking Queue 数据结构及相关操作函数。

[ArrayBlockingQueue](collection_concurrent_class.md#class-arrayblockingqueuee) 是带阻塞机制且需要用户指定容量上界的并发队列。

### let capacity

```cangjie
public let capacity: Int64
```

功能：此 [ArrayBlockingQueue](collection_concurrent_class.md#class-arrayblockingqueuee) 的容量。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### prop size

```cangjie
public prop size: Int64
```

功能：返回此 [ArrayBlockingQueue](collection_concurrent_class.md#class-arrayblockingqueuee) 的元素个数。

> **注意：**
>
> 此方法不保证并发场景下的原子性，建议在环境中没有其他线程并发地修改 [ArrayBlockingQueue](collection_concurrent_class.md#class-arrayblockingqueuee) 时调用。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init(Int64)

```cangjie
public init(capacity: Int64)
```

功能：构造一个带有传入容量大小的 [ArrayBlockingQueue](collection_concurrent_class.md#class-arrayblockingqueuee)。

参数：

- capacity: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 初始化容量大小。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 capacity 小于等于 0 则抛出异常。

### init(Int64, Collection\<E>) <sup>(deprecated)</sup>

```cangjie
public init(capacity: Int64, elements: Collection<E>)
```

功能：构造一个带有传入容量大小，并带有传入迭代器的 [ArrayBlockingQueue](collection_concurrent_class.md#class-arrayblockingqueuee)。

> **注意：**
>
> 未来版本即将废弃，同等功能替代写法为：创建空队列，再将 elements 中元素依次添加到队列中。

参数：

- capacity: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 初始化容量大小。
- elements: [Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<E> - 初始化迭代器元素。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 capacity 小于等于 0 或小于迭代器元素 elements 的 size 则抛出异常。

### func add(E)

```cangjie
public func add(element: E): Unit
```

功能：阻塞的入队操作，将元素添加到队列尾部。如果队列已满，则阻塞等待。

参数：

- element: E - 要添加的元素。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    var blockArr: ArrayBlockingQueue<Int64> = ArrayBlockingQueue<Int64>(2)
    blockArr.add(10)
    println(blockArr.peek())
}
```

运行结果：

```text
Some(10)
```

### func add(E, Duration)

```cangjie
public func add(element: E, timeout: Duration): Bool
```

功能：阻塞的入队操作，将元素添加到队列尾部，如果队列满了，将等待指定的时间。如果 timeout 为负，则会立即执行入队操作并且返回操作结果。

参数：

- element: E - 要添加的元素。
- timeout: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 等待时间。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加元素返回 true，超出等待时间还未成功添加元素返回 false。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*
import std.sync.*
import std.time.*

main() {
    let blockArr: ArrayBlockingQueue<Int64> = ArrayBlockingQueue<Int64>(2)

    /* 创建新线程，填满阻塞队列，休眠 1 秒后移除阻塞队列队首元素 */
    spawn {
        =>
        blockArr.add(0)
        blockArr.add(1)
        sleep(1000 * Duration.millisecond)
        println("New thread moves out of blocked queue head element.")
        blockArr.remove()
    }

    /* 主线程立即让出执行权，唤醒后阻塞的添加 */
    sleep(-1 * Duration.millisecond)
    println("The main thread is woken up.")
    let isSuccess: Bool = blockArr.add(2, 2000 * Duration.millisecond)
    println(isSuccess)
}
```

运行结果：

```text
The main thread is woken up.
New thread moves out of blocked queue head element.
true
```

### func dequeue() <sup>(deprecated)</sup>

```cangjie
public func dequeue(): E
```

功能：阻塞的出队操作，获得队首元素并删除。

> **注意：**
>
> 未来版本即将废弃，使用 [remove()](#func-remove) 替代。

返回值：

- E - 返回队首元素。

### func dequeue(Duration) <sup>(deprecated)</sup>

```cangjie
public func dequeue(timeout: Duration): Option<E>
```

功能：阻塞的出队操作，获得队首元素并删除，如果队列为空，将等待指定的时间。如果 timeout 为负，则会立即执行出队操作并且返回操作结果。

> **注意：**
>
> 未来版本即将废弃，使用 [remove(Duration)](#func-removeduration) 替代。

参数：

- timeout: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 等待时间。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素。如果超出等待时间还未成功获取队首元素，则返回 None。

### func enqueue(E) <sup>(deprecated)</sup>

```cangjie
public func enqueue(element: E): Unit
```

功能：阻塞的入队操作，将元素添加到队列尾部。

> **注意：**
>
> 未来版本即将废弃，使用 [add(E)](#func-adde) 替代。

参数：

- element: E - 要添加的元素。

### func enqueue(E, Duration) <sup>(deprecated)</sup>

```cangjie
public func enqueue(element: E, timeout: Duration): Bool
```

功能：阻塞的入队操作，将元素添加到队列尾部，如果队列满了，将等待指定的时间。如果 timeout 为负，则会立即执行入队操作并且返回操作结果。

> **注意：**
>
> 未来版本即将废弃，使用 [add(E, Duration)](#func-adde-duration) 替代。

参数：

- element: E - 要添加的元素。
- timeout: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 等待时间。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加元素返回 true，超出等待时间还未成功添加元素返回 false。

### func head() <sup>(deprecated)</sup>

```cangjie
public func head(): Option<E>
```

功能：获取队首元素。

该函数是非阻塞的。

> **注意：**
>
> 未来版本即将废弃，使用 [peek()](#func-peek) 替代。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素，队列为空时返回 None。

### func peek()

```cangjie
public func peek(): Option<E>
```

功能：非阻塞的获取队首元素。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素，队列为空时返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let blockArr: ArrayBlockingQueue<Int64> = ArrayBlockingQueue<Int64>(2)
    blockArr.add(2)
    blockArr.add(3)
    println(blockArr.peek())
}
```

运行结果：

```text
Some(2)
```

### func remove()

```cangjie
public func remove(): E
```

功能：阻塞的出队操作，获得队首元素并删除。如果队列为空，则阻塞等待。

返回值：

- E - 返回队首元素。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let blockArr: ArrayBlockingQueue<Int64> = ArrayBlockingQueue<Int64>(2)
    blockArr.add(2)
    blockArr.add(3)
    println(blockArr.remove())
    println(blockArr.size)
}
```

运行结果：

```text
2
1
```

### func remove(Duration)

```cangjie
public func remove(timeout: Duration): Option<E>
```

功能：阻塞的出队操作，获得队首元素并删除，如果队列为空，将等待指定的时间。如果 timeout 为负，则会立即执行出队操作并且返回操作结果。

参数：

- timeout: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 等待时间。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素。如果超出等待时间还未成功获取队首元素，则返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*
import std.sync.*
import std.time.*

main() {
    let blockArr: ArrayBlockingQueue<Int64> = ArrayBlockingQueue<Int64>(2)

    /* 创建新线程，休眠 1 秒后向队列添加元素 */
    spawn {
        =>
        sleep(1000 * Duration.millisecond)
        println("This new thread adds new elements to the queue.")
        blockArr.add(3)
    }

    /* 主线程立即让出执行权，唤醒后阻塞的取出队首元素 */
    sleep(-1 * Duration.millisecond)
    println("The main thread is woken up.")
    let num: Option<Int64> = blockArr.remove(2000 * Duration.millisecond)
    println(num)
}
```

运行结果：

```text
The main thread is woken up.
This new thread adds new elements to the queue.
Some(3)
```

### func tryAdd(E)

```cangjie
public func tryAdd(element: E): Bool
```

功能：非阻塞的入队操作，将元素添加到队列尾部。

参数：

- element: E - 要添加的元素。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加返回 true；如果队列满了，添加失败返回 false。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let blockArr: ArrayBlockingQueue<Int64> = ArrayBlockingQueue<Int64>(2)
    blockArr.tryAdd(2)
    blockArr.tryAdd(3)
    println(blockArr.size)
}
```

运行结果：

```text
2
```

### func tryDequeue() <sup>(deprecated)</sup>

```cangjie
public func tryDequeue(): Option<E>
```

功能：非阻塞的出队操作，获得队首元素并删除。

> **注意：**
>
> 未来版本即将废弃，使用 [tryRemove()](#func-tryremove) 替代。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素，队列为空时返回 None。

### func tryEnqueue(E) <sup>(deprecated)</sup>

```cangjie
public func tryEnqueue(element: E): Bool
```

功能：非阻塞的入队操作，将元素添加到队列尾部。

> **注意：**
>
> 未来版本即将废弃，使用 [tryAdd(E)](#func-tryadde) 替代。

参数：

- element: E - 要添加的元素。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加返回 true；如果队列满了，添加失败返回 false。

### func tryRemove()

```cangjie
public func tryRemove(): Option<E>
```

功能：非阻塞的出队操作，获得队首元素并删除。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素，队列为空时返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let blockArr: ArrayBlockingQueue<Int64> = ArrayBlockingQueue<Int64>(2)
    blockArr.tryAdd(2)
    println(blockArr.tryRemove())
    println(blockArr.tryRemove())
}
```

运行结果：

```text
Some(2)
None
```

## class ConcurrentHashMap\<K, V> where K <: Hashable & Equatable\<K>

```cangjie
public class ConcurrentHashMap<K, V> <: ConcurrentMap<K, V> & Collection<(K, V)> where K <: Hashable & Equatable<K> {
    public init(concurrencyLevel!: Int64 = 16)
    public init(capacity: Int64, concurrencyLevel!: Int64 = 16)
    public init(elements: Collection<(K, V)>, concurrencyLevel!: Int64 = 16)
    public init(size: Int64, initElement: (Int64) -> (K, V), concurrencyLevel!: Int64 = 16)
}
```

功能：此类用于实现并发场景下线程安全的哈希表 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 数据结构及相关操作函数。

> **提示：**
>
> [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 会在容量不足时进行自动扩容。

构造函数中的参数 concurrencyLevel 表示“并发度”，即：最多允许多少个线程并发修改 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek)。查询键值对的操作是非阻塞的，不受所指定的并发度 concurrencyLevel 的限制。参数 concurrencyLevel 默认等于 16。它只影响 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 在并发场景下的性能，不影响功能。

> **注意：**
>
> 如果用户传入的 concurrencyLevel 小于 16，则并发度会被设置为 16。
>
> concurrencyLevel 并非越大越好，更大的 concurrencyLevel 会导致更大的内存开销（甚至可能导致 out of memory 异常），用户需要在内存开销和运行效率之间进行平衡。

父类型：

- [ConcurrentMap](collection_concurrent_interface.md#interface-concurrentmapk-v)\<K, V>
- [Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<(K, V)>

示例：

使用示例见 [ConcurrentHashMap 使用示例](../collection_concurrent_samples/sample_concurrenthashmap.md)。

### prop size

```cangjie
public prop size: Int64
```

功能：返回键值的个数。

> **注意：**
>
> 此方法不保证并发场景下的原子性，建议在环境中没有其他线程并发地修改 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 时调用。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init(Collection\<(K, V)>, Int64)

```cangjie
public init(elements: Collection<(K, V)>, concurrencyLevel!: Int64 = 16)
```

功能：构造一个带有传入迭代器和指定并发度的 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek)。该构造函数根据传入迭代器元素 elements 的 size 设置 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 的容量。

参数：

- elements: [Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<(K, V)> - 初始化迭代器元素。
- concurrencyLevel!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 用户指定的并发度。

### init(Int64)

```cangjie
public init(concurrencyLevel!: Int64 = 16)
```

功能：构造一个具有默认初始容量（16）和指定并发度（默认等于 16）的 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek)。

参数：

- concurrencyLevel!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 用户指定的并发度。

### init(Int64, (Int64) -> (K, V), Int64)

```cangjie
public init(size: Int64, initElement: (Int64) -> (K, V), concurrencyLevel!: Int64 = 16)
```

功能：构造具有传入大小和初始化函数元素以及指定并发度的 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek)。该构造函数根据参数 size 设置 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 的容量。

参数：

- size: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 初始化函数元素的大小。
- initElement: ([Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) -> (K, V) - 初始化函数元素。
- concurrencyLevel!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 用户指定并发度。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 size 小于 0 则抛出异常。

### init(Int64, Int64)

```cangjie
public init(capacity: Int64, concurrencyLevel!: Int64 = 16)
```

功能：构造一个带有传入容量大小和指定并发度（默认等于 16）的 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek)。

参数：

- capacity: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 初始化容量大小。
- concurrencyLevel!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 用户指定的并发度。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 capacity 小于 0 则抛出异常。

### func add(K, V)

```cangjie
public func add(key: K, value: V): ?V
```

功能：将指定的值 value 与此 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中指定的键 key 关联。如果  [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中已经包含键 key 的关联，则旧值将被替换；如果 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中不包含键 key 的关联，则添加键 key 与值 value 的关联。

参数：

- key: K - 要放置的键。
- value: V - 要关联的值。

返回值：

- ?V - 如果赋值之前 key 存在，则返回旧的值 Some(V)；当赋值前 key 不存在时，返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let map: ConcurrentHashMap<Int64, Int64> = ConcurrentHashMap<Int64, Int64>(3, {value => (value, value)})
    let oldValue = map.add(2, 3)
    println(oldValue)
    let newValue = map.add(3, 3)
    println(newValue)
    let iter = ConcurrentHashMapIterator<Int64, Int64>(map)
    while (true) {
        match (iter.next()) {
            case Some(i) => println("(${i[0]},${i[1]})")
            case None => break
        }
    }
}
```

运行结果：

```text
Some(2)
None
(0,0)
(1,1)
(2,3)
(3,3)
```

### func addIfAbsent(K, V)

```cangjie
public func addIfAbsent(key: K, value: V): ?V
```

功能：当此 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中不存在键 key 时，在 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中添加指定的值 value 与指定的键 key 的关联。如果 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 已经包含键 key，则不执行赋值操作。

参数：

- key: K - 要放置的键。
- value: V - 要分配的值。

返回值：

- ?V - 如果赋值之前 key 存在，则返回当前 key 对应的值 Some(V)，且不执行赋值操作；当赋值前 key 不存在时，返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let map: ConcurrentHashMap<Int64, Int64> = ConcurrentHashMap<Int64, Int64>(3, {value => (value, value)})
    let oldValue = map.addIfAbsent(2, 3)
    println(oldValue)
    let newValue = map.addIfAbsent(3, 3)
    println(newValue)
    let iter = ConcurrentHashMapIterator<Int64, Int64>(map)
    while (true) {
        match (iter.next()) {
            case Some(i) => println("(${i[0]},${i[1]})")
            case None => break
        }
    }
}
```

运行结果：

```text
Some(2)
None
(0,0)
(1,1)
(2,2)
(3,3)
```

### func contains(K)

```cangjie
public func contains(key: K): Bool
```

功能：判断此映射中是否包含指定键 key 的映射。

参数：

- key: K - 传递要判断的 key。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否包含指定键 key 的映射，包含为 true，不包含为 false。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let map: ConcurrentHashMap<Int64, Int64> = ConcurrentHashMap<Int64, Int64>(3, {value => (value, value)})
    map.add(3, 3)
    println(map.contains(3))
    println(map.contains(6))
}
```

运行结果：

```text
true
false
```

### func entryView(K, (MapEntryView\<K, V>) -> Unit)

```cangjie
public func entryView(key: K, fn: (MapEntryView<K, V>) -> Unit): ?V
```

功能：根据指定键 key 获取当前映射中相应的键值对视图 entryView，并调用函数 fn 对该键值对进行增、删、改操作，并返回最终映射中键 key 对应的值。

如果当前映射中不包含键 key，则将获取一个空视图 entryView，如果将其 value 置为非 None 值，则将在当前映射中增加 key-value 键值对。

如果当前映射中包含键 key，则将获取 key-value 的视图，如果将 value 置为 None，则相当于从当前映射中删除该键值对；如果将 value 置为新的非 None 值，则相当于修改当前映射中键 key 对应的值。

注意参数 fn 中不能并发调用函数 [entryView](#func-entryviewk-mapentryviewk-v---unit)、[remove](#func-remove)、[replace](#func-replacek-v)，如：

```cangjie
map.entryView(1) { _ =>
    let f = spawn {
        map.entryView(17) { _ => () }
    }
    f.get()
}
```

> **说明：**
>
> - 该操作具有原子性。
>
> - 回调 fn 调用过程中对 key-value 键值对的修改不会即时更新到当前映射中，等到 entryView 函数调用结束再将修改整体更新到当前映射中。

参数：

- key: K - 待获取其相应视图的键。
- fn: ([MapEntryView](../../collection/collection_package_api/collection_package_interface.md#interface-mapentryviewk-v)\<K, V>) -> [Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 对指定视图进行的自定义操作，可用于对映射中键值对进行增、删、改操作。

返回值：

- ?V - 函数 fn 调用结束后当前映射中键 key 对应的值，如果 key 不存在，返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let map: ConcurrentHashMap<Int64, Int64> = ConcurrentHashMap<Int64, Int64>(2, {value => (value, value)})
    map.add(2, 2)

    /* 当前映射不包含 key 为 3 的键值对，对 entryView.value 设置新值 7，等价于添加新的键值对 (3,7) */
    let num1 = map.entryView(3, {view => view.value = 7})
    println(num1)

    /* 当前映射包含 key 为 2 的键值对，对 entryView.value 设置新值 6，等价更新 key 为 1 的值为 6 */
    let num2 = map.entryView(1, {view => view.value = 6})
    println(num2)

    /* 当前映射包含 key 为 0 的键值对，对 entryView.value 设置新值 None，等价删除 key 为 0 的键值对 */
    let num3 = map.entryView(0, {view => view.value = None})
    println(num3)

    let iter = ConcurrentHashMapIterator<Int64, Int64>(map)
    while (true) {
        match (iter.next()) {
            case Some(i) => println("(${i[0]},${i[1]})")
            case None => break
        }
    }
}
```

运行结果：

```text
Some(7)
Some(6)
None
(1,6)
(2,2)
(3,7)
```

### func get(K)

```cangjie
public func get(key: K): ?V
```

功能：返回此映射中键 key 所关联的值。

参数：

- key: K - 传递 key，获取 value。

返回值：

- ?V - 此映射中键 key 所关联的值。

### func isEmpty()

```cangjie
public func isEmpty(): Bool
```

功能：判断 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 是否为空。

> **注意：**
>
> 此方法不保证并发场景下的原子性，建议在环境中没有其他线程并发地修改 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 时调用。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果是，则返回 true，否则，返回 false。

### func iterator()

```cangjie
public func iterator(): ConcurrentHashMapIterator<K, V>
```

功能：获取 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 的迭代器。

返回值：

- [ConcurrentHashMapIterator](collection_concurrent_class.md#class-concurrenthashmapiteratork-v-where-k--hashable--equatablek)\<K, V> - [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 的迭代器

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let map: ConcurrentHashMap<Int64, Int64> = ConcurrentHashMap<Int64, Int64>(3, {value => (value, value)})
    let iter = map.iterator()
    while (true) {
        match (iter.next()) {
            case Some(i) => println("(${i[0]},${i[1]})")
            case None => break
        }
    }
}
```

运行结果：

```text
(0,0)
(1,1)
(2,2)
```

### func put(K, V) <sup>(deprecated)</sup>

```cangjie
public func put(key: K, value: V): ?V
```

功能：将指定的值 value 与此 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中指定的键 key 关联。如果  [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中已经包含键 key 的关联，则旧值将被替换；如果 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中不包含键 key 的关联，则添加键 key 与值 value 的关联。

> **注意：**
>
> 未来版本即将废弃，使用 [add(K, V)](#func-addk-v) 替代。

参数：

- key: K - 要放置的键。
- value: V - 要关联的值。

返回值：

- ?V - 如果赋值之前 key 存在，则返回旧的值 Some(V)；当赋值前 key 不存在时，返回 None。

### func putIfAbsent(K, V) <sup>(deprecated)</sup>

```cangjie
public func putIfAbsent(key: K, value: V): ?V
```

功能：当此 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中不存在键 key 时，在 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中添加指定的值 value 与指定的键 key 的关联。如果 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 已经包含键 key，则不执行赋值操作。

> **注意：**
>
> 未来版本即将废弃，使用 [addIfAbsent(K, V)](#func-addifabsentk-v) 替代。

参数：

- key: K - 要放置的键。
- value: V - 要分配的值。

返回值：

- ?V - 如果赋值之前 key 存在，则返回当前 key 对应的值 Some(V)，且不执行赋值操作；当赋值前 key 不存在时，返回 None。

### func remove(K)

```cangjie
public func remove(key: K): ?V
```

功能：从此映射中删除指定键 key 的映射（如果存在）。

参数：

- key: K - 传入要删除的 key。

返回值：

- ?V - 如果移除之前 key 存在，则返回 key 对应的值 Some(V)；当移除时 key 不存在时，返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let map: ConcurrentHashMap<Int64, Int64> = ConcurrentHashMap<Int64, Int64>(3, {value => (value, value)})
    let num = map.remove(0)
    println(num)
    let iter = map.iterator()
    while (true) {
        match (iter.next()) {
            case Some(i) => println("(${i[0]},${i[1]})")
            case None => break
        }
    }
}
```

运行结果：

```text
Some(0)
(1,1)
(2,2)
```

### func remove(K, (V) -> Bool) <sup>(deprecated)</sup>

```cangjie
public func remove(key: K, predicate: (V) -> Bool): ?V
```

功能：如果此映射中存在键 key 且 key 所映射的值 v 满足条件 predicate，则从此映射中删除 key 的映射。

> **注意：**
>
> 未来版本即将废弃，使用 [entryView(K, (MapEntryView\<K, V>) -> Unit)](#func-entryviewk-mapentryviewk-v---unit) 替代。

参数：

- key: K - 传入要删除的 key。
- predicate: (V) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 传递一个 lambda 表达式进行判断。

返回值：

- ?V - 如果映射中存在 key，则返回 key 对应的旧值；当映射中不存在 key 时，或者 key 关联的值不满足 predicate 时，返回 None。

### func replace(K, (V) -> Bool, (V) -> V) <sup>(deprecated)</sup>

```cangjie
public func replace(key: K, predicate: (V) -> Bool, eval: (V) -> V): ?V
```

功能：如果 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中存在键 key（假设其关联的值为 v），且 v 满足条件 predicate，则将 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中键 key 关联的值替换为 eval(v) 的计算结果；如果 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中不存在键 key，或者存在键 key 但关联的值不满足 predicate，则不对 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 做任何修改。

> **注意：**
>
> 未来版本即将废弃，使用 [entryView(K, (MapEntryView\<K, V>) -> Unit)](#func-entryviewk-mapentryviewk-v---unit) 替代。

参数：

- key: K - 传入要替换所关联值的键。
- predicate: (V) ->[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 传递一个 lambda 表达式进行判断。
- eval: (V) ->V - 传入计算用于替换的新值的函数。

返回值：

- ?V - 如果 key 存在，则返回 key 对应的旧值 Some(V)；当 key 不存在时，或者 key 关联的值不满足 predicate 时，返回 None。

### func replace(K, (V) -> V) <sup>(deprecated)</sup>

```cangjie
public func replace(key: K, eval: (V) -> V): ?V
```

功能：如果 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中存在键 key（假设其关联的值为 v），则将 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中键 key 关联的值替换为 eval(v) 的计算结果；如果 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中不存在键 key，则不对 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 做任何修改。

> **注意：**
>
> 未来版本即将废弃，使用 [entryView(K, (MapEntryView\<K, V>) -> Unit)](#func-entryviewk-mapentryviewk-v---unit) 替代。

参数：

- key: K - 传入要替换所关联值的键。
- eval: (V) ->V - 传入计算用于替换的新值的函数。

返回值：

- ?V - 如果 key 存在，则返回 key 对应的旧值 Some(V)；当 key 不存在时，返回 None。

### func replace(K, V)

```cangjie
public func replace(key: K, value: V): ?V
```

功能：如果 [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中存在 key，则将  [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中键 key 关联的值替换为 value；如果  [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 中不存在 key，则不对  [ConcurrentHashMap](#class-concurrenthashmapk-v-where-k--hashable--equatablek) 做任何修改。

参数：

- key: K - 传入要替换所关联值的键。
- value: V - 传入要替换成的新值。

返回值：

- ?V - 如果 key 存在，则返回 key 对应的旧值 Some(V)；当 key 不存在时，返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let map: ConcurrentHashMap<Int64, Int64> = ConcurrentHashMap<Int64, Int64>(3, {value => (value, value)})
    let num = map.replace(0, 2)
    println(num)
    let iter = map.iterator()
    while (true) {
        match (iter.next()) {
            case Some(i) => println("(${i[0]},${i[1]})")
            case None => break
        }
    }
}
```

运行结果：

```text
Some(0)
(0,2)
(1,1)
(2,2)
```

### operator func \[](K)

```cangjie
public operator func [](key: K): V
```

功能：运算符重载集合，如果键存在，返回键对应的值；如果不存在，抛出异常。

参数：

- key: K - 传递值进行判断。

返回值：

- V - 与键对应的值。

异常：

- [NoneValueException](../../core/core_package_api/core_package_exceptions.md#class-nonevalueexception) - 关联中不存在键 key。

### operator func \[](K, V)

```cangjie
public operator func [](key: K, value!: V): Unit
```

功能：运算符重载集合，如果键 key 存在，新 value 覆盖旧 value；如果键不存在，添加此键值对。

参数：

- key: K - 传递值进行判断。
- value!: V - 传递要设置的值。

## class ConcurrentHashMapIterator\<K, V> where K <: Hashable & Equatable\<K>

```cangjie
public class ConcurrentHashMapIterator<K, V> <: Iterator<(K, V)> where K <: Hashable & Equatable<K> {
    public init(cmap: ConcurrentHashMap<K, V>)
}
```

功能：此类主要实现 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 的迭代器功能。

> **注意：**
>
> 这里定义的  [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 迭代器：
>
> 1. 不保证迭代结果为并发 [HashMap](../../collection/collection_package_api/collection_package_class.md#class-hashmapk-v-where-k--hashable--equatablek) 某一时刻的 “快照”，建议在环境中没有其他线程并发地修改  [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 时调用；
> 2. 迭代器在迭代过程中，不保证可以感知环境线程对目标  [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek) 的修改。

父类型：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<(K, V)>

### init(ConcurrentHashMap\<K, V>)

```cangjie
public init(cmap: ConcurrentHashMap<K, V>)
```

功能：创建 [ConcurrentHashMapIterator](collection_concurrent_class.md#class-concurrenthashmapiteratork-v-where-k--hashable--equatablek)\<K, V> 实例。

参数：

- cmap: [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek)\<K, V> - 待获取其迭代器的 [ConcurrentHashMap](collection_concurrent_class.md#class-concurrenthashmapk-v-where-k--hashable--equatablek)\<K, V> 实例。

### func next()

```cangjie
public func next(): Option<(K, V)>
```

功能：返回迭代中的下一个元素。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<(K, V)> - [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<(K,V)> 类型。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let map: ConcurrentHashMap<Int64, Int64> = ConcurrentHashMap<Int64, Int64>(3, {value => (value, value)})
    let iter = ConcurrentHashMapIterator<Int64, Int64>(map)
    while (true) {
        match (iter.next()) {
            case Some(i) => println("(${i[0]},${i[1]})")
            case None => break
        }
    }
}
```

运行结果：

```text
(0,0)
(1,1)
(2,2)
```

## class ConcurrentLinkedQueue\<E>

```cangjie
public class ConcurrentLinkedQueue<E> <: Collection<E> {
    public init()
    public init(elements: Collection<E>)
}
```

功能：提供一个线程安全的队列，可以在多线程环境下安全地进行元素的添加和删除操作。

非阻塞队列的目的是为了解决多线程环境下的同步问题，使得多个线程可以并发地进行队列的操作，而不会出现数据冲突或者死锁的问题。

非阻塞队列在多线程编程中非常常见，它可以用于任何需要线程安全队列的场景，例如生产者消费者模型、任务调度、线程池等。

父类型：

- [Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<E>

使用示例：

使用示例见 [ConcurrentLinkedQueue 使用示例](../collection_concurrent_samples/sample_concurrent_linked_queue.md)。

### prop size

```cangjie
public prop size: Int64
```

功能：获取此 [ConcurrentLinkedQueue](collection_concurrent_class.md#class-concurrentlinkedqueuee) 的元素个数。

> **注意：**
>
> 此方法不保证并发场景下的原子性，建议在环境中没有其他线程并发地修改 [ConcurrentLinkedQueue](collection_concurrent_class.md#class-concurrentlinkedqueuee) 时调用。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ConcurrentLinkedQueue](collection_concurrent_class.md#class-concurrentlinkedqueuee) 实例。

### init(Collection\<E>) <sup>(deprecated)</sup>

```cangjie
public init(elements: Collection<E>)
```

功能：根据 [Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<E> 实例构造一个 [ConcurrentLinkedQueue](collection_concurrent_class.md#class-concurrentlinkedqueuee) 实例。

> **注意：**
>
> 未来版本即将废弃，如需实现等效功能，可先创建空队列，再依次将 [Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont) 中元素添加到队列中。

参数：

- elements: [Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<E> - 将该容器中元素放入新构造的 [ConcurrentLinkedQueue](collection_concurrent_class.md#class-concurrentlinkedqueuee)

### func add(E)

```cangjie
public func add(element: E): Bool
```

功能：非阻塞的入队操作，将元素添加到队列尾部。

> **注意：**
>
> 该函数不会返回 false。

参数：

- element: E - 要添加的元素。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加元素则返回 true。

### func dequeue() <sup>(deprecated)</sup>

```cangjie
public func dequeue(): Option<E>
```

功能：获取并删除队首元素。

> **注意：**
>
> 未来版本即将废弃，使用 [remove()](#func-remove-2) 替代。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 成功删除则返回队首元素，队列为空则返回 None。

### func enqueue(E) <sup>(deprecated)</sup>

```cangjie
public func enqueue(element: E): Bool
```

功能：非阻塞的入队操作，将元素添加到队列尾部。

> **注意：**
>
> - 该函数不会返回 false。
> - 未来版本即将废弃，使用 [add(E)](#func-adde-2) 替代。

参数：

- element: E - 要添加的元素。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加元素则返回 true。

### func head() <sup>(deprecated)</sup>

```cangjie
public func head(): Option<E>
```

功能：获取队首元素，不会删除该元素。

> **注意：**
>
> 未来版本即将废弃，使用 [peek()](#func-peek-2) 替代。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 成功获取则返回队首元素，队列为空则返回 None。

### func isEmpty()

```cangjie
public func isEmpty(): Bool
```

功能：判断当前队列是否为空。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当前队列为空返回 true，否则返回 false。

### func iterator()

```cangjie
public func iterator(): Iterator<E>
```

功能：获取当前队列的迭代器，用于遍历当前队列。

> **说明：**
>
> 遍历操作不会删除队列中的元素。
> 遍历操作不保证原子性，如果有其他线程并发修改当前队列，不保遍历得到的元素是当前队列某一时刻的静态切片。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<E> - 当前队列的迭代器。

### func peek()

```cangjie
public func peek(): Option<E>
```

功能：获取队首元素，不会删除该元素。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 成功获取则返回队首元素，队列为空则返回 None。

### func remove()

```cangjie
public func remove(): Option<E>
```

功能：获取并删除队首元素。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 成功删除则返回队首元素，队列为空则返回 None。

### func toArray()

```cangjie
public func toArray(): Array<E>
```

功能：将当前队列中所有元素按顺序存入数组，先入队的元素在数组下标较小的位置。

> **说明：**
>
> 该操作不会删除队列中的元素。
> 该操作不保证原子性，如果有其他线程并发修改当前队列，不保证该操作得到的数组是当前队列某一时刻的静态切片。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<E> - 得到的数组，里面的元素为当前队列中的元素。

## class LinkedBlockingQueue\<E>

```cangjie
public class LinkedBlockingQueue<E> {
    public let capacity: Int64
    public init()
    public init(capacity: Int64)
    public init(capacity: Int64, elements: Array<E>)
    public init(capacity: Int64, elements: Collection<E>)
}
```

功能：实现是带阻塞机制并支持用户指定容量上界的并发队列。

阻塞队列的特点是，当队列满时，尝试向队列中添加元素的线程会被阻塞，直到队列有空余位置；当队列空时，尝试从队列中获取元素的线程会被阻塞，直到队列有可取元素。

### let capacity

```cangjie
public let capacity: Int64
```

功能：返回此 [LinkedBlockingQueue](collection_concurrent_class.md#class-linkedblockingqueuee) 的容量。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### prop size

```cangjie
public prop size: Int64
```

功能：返回此 [LinkedBlockingQueue](collection_concurrent_class.md#class-linkedblockingqueuee) 的元素个数。

> **注意：**
>
> 此方法不保证并发场景下的原子性，建议在环境中没有其他线程并发地修改 [LinkedBlockingQueue](collection_concurrent_class.md#class-linkedblockingqueuee) 时调用。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init()

```cangjie
public init()
```

功能：构造一个具有默认初始容量（[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).Max）的 [LinkedBlockingQueue](collection_concurrent_class.md#class-linkedblockingqueuee)。

### init(Int64)

```cangjie
public init(capacity: Int64)
```

功能：构造一个带有传入容量大小的 [LinkedBlockingQueue](collection_concurrent_class.md#class-linkedblockingqueuee)。

参数：

- capacity: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 初始化容量大小。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 capacity 小于等于 0 则抛出异常。

### init(Int64, Array\<E>) <sup>(deprecated)</sup>

```cangjie
public init(capacity: Int64, elements: Array<E>)
```

功能：构造一个带有传入容量大小，并带有传入数组元素的 [LinkedBlockingQueue](collection_concurrent_class.md#class-linkedblockingqueuee)。

> **注意：**
>
> 未来版本即将废弃，如需实现等效功能，可先创建空队列，再依次将数组中的元素添加到队列中。

参数：

- capacity: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 初始化容量大小。
- elements: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<E> - 初始化数组元素。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 capacity 小于等于 0 或小于数组元素 elements 的 size 则抛出异常。

### init(Int64, Collection\<E>) <sup>(deprecated)</sup>

```cangjie
public init(capacity: Int64, elements: Collection<E>)
```

功能：构造一个带有传入容量大小，并带有传入迭代器的 [LinkedBlockingQueue](collection_concurrent_class.md#class-linkedblockingqueuee)。

> **注意：**
>
> 未来版本即将废弃，如需实现等效功能，可先创建空队列，再依次将 [Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont) 中的元素添加到队列中。

参数：

- capacity: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 初始化容量大小。
- elements: [Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<E> - 初始化迭代器元素。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 capacity 小于等于 0 或小于迭代器元素 elements 的 size 则抛出异常。

### func add(E)

```cangjie
public func add(element: E): Unit
```

功能：阻塞的入队操作，将元素添加到队列尾部。如果队列已满，则阻塞等待。

参数：

- element: E - 要添加的元素。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    var blockArr: LinkedBlockingQueue<Int64> = LinkedBlockingQueue<Int64>(2)
    blockArr.add(10)
    println(blockArr.peek())
}
```

运行结果：

```text
Some(10)
```

### func add(E, Duration)

```cangjie
public func add(element: E, timeout: Duration): Bool
```

功能：阻塞的入队操作，将元素添加到队列尾部，如果队列满了，将等待指定的时间。如果 timeout 为负，则会立即执行入队操作并且返回操作结果。

参数：

- element: E - 要添加的元素。
- timeout: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 等待时间。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加元素返回 true。超出等待时间还未成功添加元素返回 false。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*
import std.sync.*
import std.time.*

main() {
    let blockArr: LinkedBlockingQueue<Int64> = LinkedBlockingQueue<Int64>(2)

    /* 创建新线程，填满阻塞队列，休眠 1 秒后移除阻塞队列队首元素 */
    spawn {
        =>
        blockArr.add(0)
        blockArr.add(1)
        sleep(1000 * Duration.millisecond)
        println("New thread moves out of blocked queue head element.")
        blockArr.remove()
    }

    /* 主线程立即让出执行权，唤醒后阻塞的添加 */
    sleep(-1 * Duration.millisecond)
    println("The main thread is woken up.")
    let isSuccess: Bool = blockArr.add(2, 2000 * Duration.millisecond)
    println(isSuccess)
}
```

运行结果：

```text
The main thread is woken up.
New thread moves out of blocked queue head element.
true
```

### func dequeue() <sup>(deprecated)</sup>

```cangjie
public func dequeue(): E
```

功能：阻塞的出队操作，获得队首元素并删除。

> **注意：**
>
> 未来版本即将废弃，使用 [remove()](#func-remove-1) 替代。

返回值：

- E - 返回队首元素。

### func dequeue(Duration) <sup>(deprecated)</sup>

```cangjie
public func dequeue(timeout: Duration): Option<E>
```

功能：阻塞的出队操作，获得队首元素并删除。如果队列为空，将等待指定的时间。如果 timeout 为负，则会立即执行出队操作并且返回操作结果。

> **注意：**
>
> 未来版本即将废弃，使用 [remove(Duration)](#func-removeduration-1) 替代。

参数：

- timeout: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 等待时间。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素。如果超出等待时间还未成功获取队首元素，则返回 None。

### func enqueue(E) <sup>(deprecated)</sup>

```cangjie
public func enqueue(element: E): Unit
```

功能：阻塞的入队操作，将元素添加到队列尾部。

> **注意：**
>
> 未来版本即将废弃，使用 [add(E)](#func-adde-1) 替代。

参数：

- element: E - 要添加的元素。

### func enqueue(E, Duration) <sup>(deprecated)</sup>

```cangjie
public func enqueue(element: E, timeout: Duration): Bool
```

功能：阻塞的入队操作，将元素添加到队列尾部，如果队列满了，将等待指定的时间。如果 timeout 为负，则会立即执行入队操作并且返回操作结果。

> **注意：**
>
> 未来版本即将废弃，使用 [add(E, Duration)](#func-adde-duration) 替代。

参数：

- element: E - 要添加的元素。
- timeout: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 等待时间。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加元素返回 true。超出等待时间还未成功添加元素返回 false。

### func head() <sup>(deprecated)</sup>

```cangjie
public func head(): Option<E>
```

功能：获取队首元素。

> **注意：**
>
> - 该函数是非阻塞的。
> - 未来版本即将废弃，使用 [peek()](#func-peek-1) 替代。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素，队列为空时返回 None。

### func peek()

```cangjie
public func peek(): Option<E>
```

功能：获取队首元素。

> **注意：**
>
> 该函数是非阻塞的。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素，队列为空时返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let blockArr: LinkedBlockingQueue<Int64> = LinkedBlockingQueue<Int64>(2)
    blockArr.add(2)
    blockArr.add(3)
    println(blockArr.peek())
}
```

运行结果：

```text
Some(2)
```

### func remove()

```cangjie
public func remove(): E
```

功能：阻塞的出队操作，获得队首元素并删除。

返回值：

- E - 返回队首元素。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let blockArr: LinkedBlockingQueue<Int64> = LinkedBlockingQueue<Int64>(2)
    blockArr.add(2)
    blockArr.add(3)
    println(blockArr.remove())
    println(blockArr.size)
}
```

运行结果：

```text
2
1
```

### func remove(Duration)

```cangjie
public func remove(timeout: Duration): Option<E>
```

功能：阻塞的出队操作，获得队首元素并删除。如果队列为空，将等待指定的时间。如果 timeout 为负，则会立即执行出队操作并且返回操作结果。

参数：

- timeout: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 等待时间。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素。如果超出等待时间还未成功获取队首元素，则返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*
import std.sync.*
import std.time.*

main() {
    let blockArr: LinkedBlockingQueue<Int64> = LinkedBlockingQueue<Int64>(2)

    /* 创建新线程，休眠 1 秒后向队列添加元素 */
    spawn {
        =>
        sleep(1000 * Duration.millisecond)
        println("This new thread adds new elements to the queue.")
        blockArr.add(3)
    }

    /* 主线程立即让出执行权，唤醒后阻塞的取出队首元素 */
    sleep(-1 * Duration.millisecond)
    println("The main thread is woken up.")
    let num: Option<Int64> = blockArr.remove(2000 * Duration.millisecond)
    println(num)
}
```

运行结果：

```text
The main thread is woken up.
This new thread adds new elements to the queue.
Some(3)
```

### func tryAdd(E)

```cangjie
public func tryAdd(element: E): Bool
```

功能：非阻塞的入队操作，将元素添加到队列尾部。

参数：

- element: E - 要添加的元素。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加返回 true；如果队列满了，添加失败返回 false。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let blockArr: LinkedBlockingQueue<Int64> = LinkedBlockingQueue<Int64>(2)
    blockArr.tryAdd(2)
    blockArr.tryAdd(3)
    println(blockArr.size)
}
```

运行结果：

```text
2
```

### func tryDequeue() <sup>(deprecated)</sup>

```cangjie
public func tryDequeue(): Option<E>
```

功能：非阻塞的出队操作，获得队首元素并删除。

> **注意：**
>
> 未来版本即将废弃，使用 [tryRemove()](#func-tryremove-1) 替代。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素，队列为空时返回 None。

### func tryEnqueue(E) <sup>(deprecated)</sup>

```cangjie
public func tryEnqueue(element: E): Bool
```

功能：非阻塞的入队操作，将元素添加到队列尾部。

> **注意：**
>
> 未来版本即将废弃，使用 [tryAdd(E)](#func-tryadde-1) 替代。

参数：

- element: E - 要添加的元素。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 成功添加返回 true；如果队列满了，添加失败返回 false。

### func tryRemove()

```cangjie
public func tryRemove(): Option<E>
```

功能：非阻塞的出队操作，获得队首元素并删除。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<E> - 返回队首元素，队列为空时返回 None。

示例：

<!-- verify -->
```cangjie
import std.collection.concurrent.*

main() {
    let blockArr: LinkedBlockingQueue<Int64> = LinkedBlockingQueue<Int64>(2)
    blockArr.tryAdd(3)
    println(blockArr.tryRemove())
    println(blockArr.tryRemove())
}
```

运行结果：

```text
Some(3)
None
```
