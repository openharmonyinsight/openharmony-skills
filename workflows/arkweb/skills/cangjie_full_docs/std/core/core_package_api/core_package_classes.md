# 类

## class ArrayIterator\<T>

```cangjie
public class ArrayIterator<T> <: Iterator<T> {
    public init(data: Array<T>)
}
```

功能：数组迭代器，迭代功能详述见 [Iterable](core_package_interfaces.md#interface-iterablee) 和 [Iterator](core_package_classes.md#class-iteratort) 说明。

父类型：

- [Iterator](#class-iteratort)\<T>

### init(Array\<T>)

```cangjie
public init(data: Array<T>)
```

功能：给定一个 [Array](core_package_structs.md#struct-arrayt) 数组实例，创建其对应的迭代器，用来迭代遍历该数组实例中全部对象。

参数：

- data: [Array](core_package_structs.md#struct-arrayt)\<T> - 数组实例。

### func next()

```cangjie
public func next(): Option<T>
```

功能：返回数组迭代器中的下一个值。

返回值：

- [Option](core_package_enums.md#enum-optiont)\<T> - 数组迭代器中的下一个成员，用 [Option](core_package_enums.md#enum-optiont) 封装，迭代到末尾时返回 `None`。

示例：

<!-- verify -->
```cangjie
main() {
    var arr: Array<Int64> = [1, 2, 3, 4]
    var arrIterator: ArrayIterator<Int64> = ArrayIterator(arr)
    var num: Option<Int64>
    while (true) {
        num = arrIterator.next()
        if (num.isNone()) {
            break
        }
        println(num.getOrDefault({=> -1}))
    }
}
```

运行结果：

```text
1
2
3
4
```

## class Box\<T>

```cangjie
public class Box<T> {
    public var value: T
    public init(v: T)
}
```

功能：[Box](core_package_classes.md#class-boxt) 类型提供了为其他类型添加一层 `class` 封装的能力。

如果 `T` 类型本身不具备引用能力，如 `struct` 类型，封装后 [Box](core_package_classes.md#class-boxt)\<T> 类型将可被引用。

### var value

```cangjie
public var value: T
```

功能：获取或修改被包装的值。

类型：T

### init(T)

```cangjie
public init(v: T)
```

功能：给定 `T` 类型实例，构造对应的 [Box](core_package_classes.md#class-boxt)\<T> 实例。

参数：

- v: T - 任意类型实例。

### extend\<T> Box\<T> <: Comparable\<Box\<T>> where T <: Comparable\<T>

```cangjie
extend<T> Box<T> <: Comparable<Box<T>> where T <: Comparable<T>
```

功能：为 [Box](core_package_classes.md#class-boxt)\<T> 类扩展 [Comparable](core_package_interfaces.md#interface-comparablet)\<[Box](core_package_classes.md#class-boxt)\<T>> 接口，提供比较大小的能力。

[Box](core_package_classes.md#class-boxt)\<T> 实例的大小关系与其封装的 `T` 实例大小关系相同。

父类型：

- [Comparable](core_package_interfaces.md#interface-comparablet)\<[Box](#class-boxt)\<T>>

#### func compare(Box\<T>)

```cangjie
public func compare(that: Box<T>): Ordering
```

功能：判断当前 [Box](core_package_classes.md#class-boxt) 实例与另一个 [Box](core_package_classes.md#class-boxt) 实例的大小关系。

参数：

- that: [Box](core_package_classes.md#class-boxt)\<T> - 比较的另外一个 [Box](core_package_classes.md#class-boxt) 对象。

返回值：

- [Ordering](core_package_enums.md#enum-ordering) - 如果当前 [Box](core_package_classes.md#class-boxt) 实例大于 that，返回 [Ordering](core_package_enums.md#enum-ordering).GT，等于返回 [Ordering](core_package_enums.md#enum-ordering).EQ，小于返回 [Ordering](core_package_enums.md#enum-ordering).LT。

示例：

<!-- verify -->
```cangjie
struct Data <: Comparable<Data> {
    var a: Int64 = 0
    var b: Int64 = 0

    public init(a: Int64, b: Int64) {
        this.a = a
        this.b = b
    }

    public func compare(d: Data) {
        let tValue: Int64 = this.a + this.b
        let dValue: Int64 = d.a + d.b
        if (tValue > dValue) {
            return Ordering.GT
        } else if (tValue == dValue) {
            return Ordering.EQ
        } else {
            return Ordering.LT
        }
    }
}

main() {
    var data1: Box<Data> = Box<Data>(Data(12, 12))
    var data2: Box<Data> = Box<Data>(Data(7, 12))
    println(data1.compare(data2))
}
```

运行结果：

```text
Ordering.GT
```

#### operator func !=(Box\<T>)

```cangjie
public operator func !=(that: Box<T>): Bool
```

功能：比较 [Box](core_package_classes.md#class-boxt) 对象是否不相等。

参数：

- that: [Box](core_package_classes.md#class-boxt)\<T> - 比较的另外一个 [Box](core_package_classes.md#class-boxt) 对象。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 当前 [Box](core_package_classes.md#class-boxt) 对象不等于参数 [Box](core_package_classes.md#class-boxt) 对象返回 true，否则返回 false。

#### operator func <(Box\<T>)

```cangjie
public operator func <(that: Box<T>): Bool
```

功能：比较 [Box](core_package_classes.md#class-boxt) 对象的大小。

参数：

- that: [Box](core_package_classes.md#class-boxt)\<T> - 比较的另外一个 [Box](core_package_classes.md#class-boxt) 对象。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 当前 [Box](core_package_classes.md#class-boxt) 对象小于参数 [Box](core_package_classes.md#class-boxt) 对象返回 true，否则返回 false。

#### operator func <=(Box\<T>)

```cangjie
public operator func <=(that: Box<T>): Bool
```

功能：比较 [Box](core_package_classes.md#class-boxt) 对象的大小。

参数：

- that: [Box](core_package_classes.md#class-boxt)\<T> - 比较的另外一个 [Box](core_package_classes.md#class-boxt) 对象。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 当前 [Box](core_package_classes.md#class-boxt) 对象小于等于参数 [Box](core_package_classes.md#class-boxt) 对象返回 true，否则返回 false。

#### operator func ==(Box\<T>)

```cangjie
public operator func ==(that: Box<T>): Bool
```

功能：比较 [Box](core_package_classes.md#class-boxt) 对象是否相等。

参数：

- that: [Box](core_package_classes.md#class-boxt)\<T> - 比较的另外一个 [Box](core_package_classes.md#class-boxt) 对象。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 当前 [Box](core_package_classes.md#class-boxt) 对象等于参数 [Box](core_package_classes.md#class-boxt) 对象返回 true，否则返回 false。

#### operator func >(Box\<T>)

```cangjie
public operator func >(that: Box<T>): Bool
```

功能：比较 [Box](core_package_classes.md#class-boxt) 对象的大小。

参数：

- that: [Box](core_package_classes.md#class-boxt)\<T> - 比较的另外一个 [Box](core_package_classes.md#class-boxt) 对象。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 当前 [Box](core_package_classes.md#class-boxt) 对象大于参数 [Box](core_package_classes.md#class-boxt) 对象返回 true，否则返回 false。

#### operator func >=(Box\<T>)

```cangjie
public operator func >=(that: Box<T>): Bool
```

功能：比较 [Box](core_package_classes.md#class-boxt) 对象的大小。

参数：

- that: [Box](core_package_classes.md#class-boxt)\<T> - 比较的另外一个 [Box](core_package_classes.md#class-boxt) 对象。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 当前 [Box](core_package_classes.md#class-boxt) 对象大于等于参数 [Box](core_package_classes.md#class-boxt) 对象返回 true，否则返回 false。

### extend\<T> Box\<T> <: Hashable where T <: Hashable

```cangjie
extend<T> Box<T> <: Hashable where T <: Hashable
```

功能：为 [Box](core_package_classes.md#class-boxt)\<T> 类扩展 [Hashable](core_package_interfaces.md#interface-hashable) 接口，提供比较大小的能力。

父类型：

- [Hashable](core_package_interfaces.md#interface-hashable)

#### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取 [Box](core_package_classes.md#class-boxt) 对象的哈希值。

实际上该值为 [Box](core_package_classes.md#class-boxt) 中封装的 `T` 类型实例的哈希值。

返回值：

- [Int64](core_package_intrinsics.md#int64) - 当前 [Box](core_package_classes.md#class-boxt) 对象的哈希值。

### extend\<T> Box\<T> <: ToString where T <: ToString

```cangjie
extend<T> Box<T> <: ToString where T <: ToString
```

功能：为 [Box](core_package_classes.md#class-boxt)\<T> 类型扩展 [ToString](core_package_interfaces.md#interface-tostring) 接口，支持转字符串操作。

父类型：

- [ToString](core_package_interfaces.md#interface-tostring)

#### func toString()

```cangjie
public func toString(): String
```

功能：获取 [Box](core_package_classes.md#class-boxt) 对象的字符串表示，字符串内容为当前实例封装的 `T` 类型实例的字符串表示。

返回值：

- [String](core_package_structs.md#struct-string) - 转换后的字符串。

## class Future\<T>

```cangjie
public class Future<T> {}
```

功能：[Future](core_package_classes.md#class-futuret)\<T> 实例代表一个仓颉线程任务，可用于获取仓颉线程的计算结果，向仓颉线程发送取消信号。

`spawn` 表达式的返回类型是 [Future](core_package_classes.md#class-futuret)\<T>，其中 `T` 的类型取决于 `spawn` 表达式中的闭包的返回值类型。

### prop thread

```cangjie
public prop thread: Thread
```

功能：获得对应仓颉线程的 [Thread](core_package_classes.md#class-thread) 实例。

类型：[Thread](core_package_classes.md#class-thread)

### func cancel()

```cangjie
public func cancel(): Unit
```

功能：给当前 [Future](core_package_classes.md#class-futuret) 实例对应的仓颉线程发送取消请求。该方法不会立即停止线程执行，仅发送请求，相应地，[Thread](core_package_classes.md#class-thread) 类的函数 `hasPendingCancellation` 可用于检查线程是否存在取消请求，开发者可以通过该检查来自行决定是否提前终止线程以及如何终止线程。

示例：

<!-- verify -->
```cangjie
main(): Unit {
    /* 创建线程 */
    let future = spawn {
        while (true) {
            if (Thread.currentThread.hasPendingCancellation) {
                return 0
            }
        }
        return 1
    }
    /* 向线程发送取消请求 */
    future.cancel()
    let res = future.get()
    println(res)
}
```

运行结果：

```text
0
```

### func get()

```cangjie
public func get(): T
```

功能：阻塞当前线程，等待并获取当前 [Future](core_package_classes.md#class-futuret)\<T> 对象对应的线程的结果。

返回值：

- T - 当前 [Future](core_package_classes.md#class-futuret)\<T> 实例代表的线程运行结束后的返回值。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    let fut: Future<Int64> = spawn {
        =>
        sleep(1000 * Duration.millisecond) /* 睡眠 1 秒 */
        return 1
    }

    /* 等待线程完成 */
    let result: Int64 = fut.get()
    println(result)
    return 0
}
```

运行结果：

```text
1
```

### func get(Duration)

```cangjie
public func get(timeout: Duration): T
```

功能：阻塞当前线程，等待指定时长并获取当前 [Future](core_package_classes.md#class-futuret)\<T> 对象对应的线程的返回值。

需指定等待的超时时间，如果相应的线程在指定时间内未完成执行，则该函数将抛出异常 [TimeoutException](./core_package_exceptions.md#class-timeoutexception)。如果 timeout <= Duration.Zero，等同于 get()，即不限制等待时长。如果线程抛出异常退出执行，在 get 调用处将继续抛出该异常。

参数：

- timeout: [Duration](./core_package_structs.md#struct-duration) - 等待时间。

返回值：

- T - 返回指定时长后仓颉线程执行结果。

异常：

- [TimeoutException](./core_package_exceptions.md#class-timeoutexception) - 如果相应的线程在指定时间内未完成执行，则该函数将抛出此异常。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    let fut: Future<Int64> = spawn {
        =>
        sleep(1000 * Duration.millisecond) /* 睡眠 1 秒 */
        return 1
    }

    let result: Int64 = fut.get(2000 * Duration.millisecond)
    /* 最大等待时间为 2 秒， 超过该时间抛出 TimeoutException */

    println(result)
    return 0
}
```

运行结果：

```text
1
```

### func tryGet()

```cangjie
public func tryGet(): Option<T>
```

功能：尝试获取执行结果，不会阻塞当前线程。如果相应的线程未完成，则该函数返回 `None`。

返回值：

- [Option](core_package_enums.md#enum-optiont)\<T> - 如果当前仓颉线程未完成返回 `None`，否则返回执行结果。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    let fut: Future<Int64> = spawn {
        =>
        sleep(1000 * Duration.millisecond) /* 睡眠 1 秒 */
        return 1
    }

    /* 主线程等待 4 秒，保证创建线程已经完成 */
    sleep(4000 * Duration.millisecond)

    /* 尝试获取创建线程的运行结果 */
    let result: Option<Int64> = fut.tryGet()
    println(result)
    return 0
}
```

运行结果：

```text
Some(1)
```

## class Iterator\<T>

```cangjie
public abstract class Iterator<T> <: Iterable<T> {
    public init()
}
```

功能：该类表示迭代器，提供 `next` 方法支持对容器内的成员进行迭代遍历。

父类型：

- [Iterable](core_package_interfaces.md#interface-iterablee)\<T>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Iterator](core_package_classes.md#class-iteratort)\<T> 对象。

### func iterator()

```cangjie
public func iterator() : Iterator<T>
```

功能：返回迭代器自身。

返回值：

- [Iterator](core_package_classes.md#class-iteratort)\<T> - 迭代器自身。

### func next()

```cangjie
public func next(): Option<T>
```

功能：获取迭代过程中的下一个元素。

返回值：

- [Option](core_package_enums.md#enum-optiont)\<T> - 迭代过程中的下一个元素。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]
    var iter = arr.iterator() /* 获取容器的迭代器对象 */

    while (true) { /* 使用迭代器进行遍历 */
        match (iter.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
1
2
3
4
5
```

### extend\<T> Iterator\<T>

```cangjie
extend<T> Iterator<T>
```

功能：扩展 [Iterator](core_package_classes.md#class-iteratort)\<T> 类型。

迭代器的方法主要包含中间操作和终止操作。中间操作（如 `skip()`、`map()`）会产生一个新的迭代器。而终止操作（如 `count()`、`all()`）会根据迭代器产生的元素计算结果，而不产生新的迭代器。每种迭代器方法都会消耗迭代器中不同数量的元素，详见各方法描述。

#### func all((T) -> Bool)

```cangjie
public func all(predicate: (T)-> Bool): Bool
```

功能：判断迭代器所有元素是否都满足条件。此方法会重复获取并消耗迭代器中元素直到某个元素不满足条件。

参数：

- predicate: (T) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 给定的条件。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 元素是否都满足条件。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取容器的迭代器对象 */
    var iter = arr.iterator()
    var flag: Bool = iter.all({v: Int64 => v > 0})
    println(flag)
    return 0
}
```

运行结果：

```text
true
```

#### func any((T) -> Bool)

```cangjie
public func any(predicate: (T)-> Bool): Bool
```

功能：判断迭代器是否存在任意一个满足条件的元素。此方法会重复获取并消耗迭代器中元素直到某个元素满足条件。

参数：

- predicate: (T) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 给定的条件。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否存在任意满足条件的元素。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取容器的迭代器对象 */
    var iter = arr.iterator()
    var flag: Bool = iter.any({v: Int64 => v > 4})
    println(flag)
    return 0
}
```

运行结果：

```text
true
```

#### func at(Int64)

```cangjie
public func at(n: Int64): Option<T>
```

功能：获取当前迭代器第 n 个元素，n 从 0 开始计数。此方法会消耗指定元素前的所有元素（包括指定元素）。

参数：

- n: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 给定的元素序号，序号从 0 开始。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回对应位置元素，若 n 大于剩余元素数量则返回 None。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取容器的迭代器对象 */
    var iter = arr.iterator()
    var num: Option<Int64> = iter.at(2)
    println(num)
    return 0
}
```

运行结果：

```text
Some(3)
```

#### func concat(Iterator\<T>)

```cangjie
public func concat(other: Iterator<T>): Iterator<T>
```

功能：串联两个迭代器，当前迭代器在先，参数表示的迭代器在后。

参数：

- other: [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 要串联在后面的迭代器。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回串联后的新迭代器。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr1: Array<Int64> = [1, 2]
    var arr2: Array<Int64> = [3, 4]

    /* 获取容器的迭代器对象 */
    var iter1 = arr1.iterator()
    var iter2 = arr2.iterator()

    /* 合并两个迭代器 */
    var iter = iter1.concat(iter2)

    /* 使用迭代器进行遍历 */
    while (true) {
        match (iter.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
1
2
3
4
```

#### func count()

```cangjie
public func count(): Int64
```

功能：统计当前迭代器包含元素数量。此方法会消耗迭代器中所有元素来计算迭代器中的元素数量。

> **注意：**
>
> 该方法会消耗迭代器，即使用该方法后迭代器内不再包含任何元素。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回迭代器包含元素数量。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2]

    /* 获取容器的迭代器对象 */
    var iter = arr.iterator()
    let len: Int64 = iter.count()
    println(len)

    /* 使用迭代器进行遍历，但是 count 消耗了迭代器中的元素，因此不会打印 */
    while (true) {
        match (iter.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
2
```

#### func enumerate()

```cangjie
public func enumerate(): Iterator<(Int64, T)>
```

功能：用于获取带索引的迭代器。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<([Int64](../../core/core_package_api/core_package_intrinsics.md#int64), T)> - 返回一个带索引的迭代器。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2]

    /* 获取容器的迭代器对象 */
    var iter = arr.iterator()
    var iter1 = iter.enumerate()

    /* 使用迭代器进行遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) =>
                print(i[0].toString() + ' ')
                print(i[1])
                println()
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
0 1
1 2
```

#### func filter((T) -> Bool)

```cangjie
public func filter(predicate: (T)-> Bool): Iterator<T>
```

功能：筛选出满足条件的元素。

参数：

- predicate: (T) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 给定的条件，条件为 `true` 的元素会按顺序出现在返回的迭代器里。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个新迭代器。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取过滤后的迭代器对象 */
    var iter = arr.iterator()
    var iter1 = iter.filter({value: Int64 => value > 2})

    /* 使用迭代器进行遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
3
4
5
```

#### func filterMap\<R>((T) -> Option\<R>)

```cangjie
public func filterMap<R>(transform: (T) -> Option<R>): Iterator<R>
```

功能：同时进行筛选操作和映射操作，返回一个新的迭代器。

参数：

- transform: (T) -> [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 给定的映射函数。函数返回值为 Some 对应 filter 的 predicate 为 true，反之表示 false。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<R> - 返回一个新迭代器。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取过滤后的迭代器对象，对元素进行过滤和映射，映射需返回 Option 类型 */
    var iter = arr.iterator()
    var iter1 = iter.filterMap({
        value: Int64 => if (value > 2) {
            return Some(value + 1)
        } else {
            return None<Int64>
        }
    })

    /* 使用迭代器进行遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
4
5
6
```

#### func first()

```cangjie
public func first(): Option<T>
```

功能：获取当前迭代器的头部元素。此方法会获取并消耗第一个元素。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回头部元素，若为空则返回 None。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取迭代器对象 */
    var iter = arr.iterator()
    var head: Option<Int64> = iter.first()
    println(head)

    return 0
}
```

运行结果：

```text
Some(1)
```

#### func flatMap\<R>((T) -> Iterator\<R>)

```cangjie
public func flatMap<R>(transform: (T) -> Iterator<R>): Iterator<R>
```

功能：创建一个带 [flatten](../../collection/collection_package_api/collection_package_function.md#func-flattent-riterablet-where-t--iterabler) 功能的映射。

参数：

- transform: (T) -> [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<R> - 给定的映射函数。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<R> - 返回一个带 [flatten](../../collection/collection_package_api/collection_package_function.md#func-flattent-riterablet-where-t--iterabler) 功能的映射。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Array<Int64>> = [[1], [2], [3], [4, 5]]

    /* 获取带 flatten 功能的迭代器对象 */
    var iter = arr.iterator()
    var iter1 = iter.flatMap({value => value.iterator()})

    /* 使用迭代器进行展开遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
1
2
3
4
5
```

#### func fold\<R>(R, (R, T) -> R)

```cangjie
public func fold<R>(initial: R, operation: (R, T)->R): R
```

功能：使用指定初始值，从左向右计算。此方法会消耗迭代器中的所有元素。

参数：

- initial: R - 给定的 R 类型的初始值。
- operation: (R, T) -> R - 给定的计算函数。

返回值：

- R - 返回最终计算得到的值。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取迭代器对象，对数组元素进行求和 */
    var iter = arr.iterator()
    var sum: Int64 = iter.fold(0, {total, value => total + value})

    println(sum)
    return 0
}
```

运行结果：

```text
15
```

#### func forEach((T) -> Unit)

```cangjie
public func forEach(action: (T)-> Unit): Unit
```

功能：遍历当前迭代器所有元素，对每个元素执行给定的操作。此方法会消耗迭代器中的所有元素。

参数：

- action: (T) -> [Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 给定的操作函数。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    var iter = arr.iterator()
    iter.forEach({value => println(value)})

    return 0
}
```

运行结果：

```text
1
2
3
4
5
```

#### func inspect((T) -> Unit)

```cangjie
public func inspect(action: (T) -> Unit): Iterator<T>
```

功能：迭代器每次调用 next() 对当前元素执行额外操作（不会消耗迭代器中元素）。

参数：

- action: (T) -> [Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 给定的操作函数。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个新迭代器。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2]

    /* 获取迭代器对象，并为 next 函数附加额外操作 */
    var iter = arr.iterator()
    var iter1 = iter.inspect({value => println("Logging: Processing ${value}")})

    /* 使用迭代器进行展开遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) => println("Processing ${i} !")
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
Logging: Processing 1
Processing 1 !
Logging: Processing 2
Processing 2 !
```

#### func intersperse(T)

```cangjie
public func intersperse(separator: T): Iterator<T>
```

功能：迭代器每两个元素之间插入一个给定的新元素。

参数：

- separator: T - 给定的元素。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个新迭代器。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2]

    /* 获取迭代器对象，每两个元素之间插入一个 0 */
    var iter = arr.iterator()
    var iter1 = iter.intersperse(0)

    /* 使用迭代器进行展开遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
1
0
2
```

#### func isEmpty()

```cangjie
public func isEmpty(): Bool
```

功能：判断当前迭代器是否为空。此方法会调用 [next()](#func-next-1) ，根据其返回值判断当前迭代器是否为空。因此如果当前迭代器不为空，则会消耗一个元素。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回当前迭代器是否为空。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2]

    /* 获取迭代器对象 */
    var iter = arr.iterator()

    /* 判断迭代器中是否有元素，如果有会消耗一个元素 */
    println(iter.isEmpty())

    /* 使用迭代器进行展开遍历 */
    while (true) {
        match (iter.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    println(iter.isEmpty())
    return 0
}
```

运行结果：

```text
false
2
true
```

#### func last()

```cangjie
public func last(): Option<T>
```

功能：获取当前迭代器尾部元素。此方法会获取并消耗迭代器中的所有元素，并返回最后一个元素。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回尾部元素，若为空则返回 None。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2]

    /* 获取迭代器对象 */
    var iter = arr.iterator()
    println(iter.last())
    return 0
}
```

运行结果：

```text
Some(2)
```

#### func map\<R>((T) -> R)

```cangjie
public func map<R>(transform: (T)-> R): Iterator<R>
```

功能：创建一个映射。

参数：

- transform: (T) ->R - 给定的映射函数。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<R> - 返回一个映射。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4]

    /* 获取迭代器对象，并对元素进行映射，获取新的迭代器对象 */
    var iter = arr.iterator()
    var iter1 = iter.map({value => value * 2})

    /* 使用迭代器进行展开遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
2
4
6
8
```

#### func none((T) -> Bool)

```cangjie
public func none(predicate: (T)-> Bool): Bool
```

功能：判断当前迭代器中所有元素是否都不满足条件。此方法会重复获取并消耗迭代器中元素直到某个元素满足条件。

参数：

- predicate: (T) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 给定的条件。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当前迭代器中元素是否都不满足条件。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4]

    /* 获取迭代器对象，并对元素进行映射，获取新的迭代器对象 */
    var iter1 = arr.iterator()
    var iter2 = arr.iterator()

    /* 存在元素大于 2，返回 false */
    var flag1: Bool = iter1.none({value => value > 2})
    println(flag1)

    /* 不存在元素大于 5，返回 true */
    var flag2: Bool = iter2.none({value => value > 5})
    println(flag2)
    return 0
}
```

运行结果：

```text
false
true
```

#### func reduce((T, T) -> T)

```cangjie
public func reduce(operation: (T, T) -> T): Option<T>
```

功能：使用第一个元素作为初始值，从左向右计算。此方法会消耗迭代器中的所有元素。

参数：

- operation: (T, T) -> T - 给定的计算函数。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回计算结果。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取迭代器对象，对数组元素进行求和 */
    var iter = arr.iterator()
    var sum: Option<Int64> = iter.reduce({total, value => total + value})
    println(sum)
    return 0
}
```

运行结果：

```text
Some(15)
```

#### func skip(Int64)

```cangjie
public func skip(count: Int64): Iterator<T>
```

功能：从前往后从当前迭代器跳过特定个数。

当 count 小于 0 时，抛出异常。当 count 等于 0 时，相当没有跳过任何元素，返回原迭代器。当 count 大于 0 并且 count 小于迭代器的大小时，跳过 count 个元素后，返回含有剩下的元素的新迭代器。当 count 大于等于迭代器的大小时，跳过所有元素，返回空迭代器。

参数：

- count: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 要跳过的个数。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个跳过指定数量元素的迭代器。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 count < 0 时，抛出异常。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取迭代器对象，跳过前两个元素 */
    var iter = arr.iterator()
    var iter1 = iter.skip(2)

    /* 使用迭代器进行展开遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
3
4
5
```

#### func step(Int64)

```cangjie
public func step(count: Int64): Iterator<T>
```

功能：迭代器每次调用 next() 跳过特定个数。

当 count 小于等于 0 时，抛出异常。当 count 大于 0 时，每次调用 next() 跳过 count 次，直到迭代器为空。

参数：

- count: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 每次调用 next() 要跳过的个数。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个新迭代器，这个迭代器每次调用 next() 会跳过特定个数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 count <= 0 时，抛出异常。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取迭代器对象，每次调用 next() 会跳过两个元素 */
    var iter = arr.iterator()
    var iter1 = iter.step(2)

    /* 使用迭代器进行展开遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
1
3
5
```

#### func take(Int64)

```cangjie
public func take(count: Int64): Iterator<T>
```

功能：从当前迭代器取出特定个数。

从前往后取出当前迭代器特定个数的元素。当 count 小于 0 时，抛出异常。当 count 等于 0 时，不取元素，返回空迭代器。当 count 大于 0 小于迭代器的大小时，取前 count 个元素，返回新迭代器。当 count 大于等于迭代器的大小时，取所有元素，返回原迭代器。

参数：

- count: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 要取出的个数。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<T> - 返回一个取出指定数量元素的迭代器。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 count < 0 时，抛出异常。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]

    /* 获取迭代器对象，取出前三个元素 */
    var iter = arr.iterator()
    var iter1 = iter.take(3)

    /* 使用迭代器进行展开遍历 */
    while (true) {
        match (iter1.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
1
2
3
```

#### func zip\<R>(Iterator\<R>)

```cangjie
public func zip<R>(it: Iterator<R>): Iterator<(T, R)>
```

功能：将两个迭代器合并成一个（长度取决于短的那个迭代器）。

参数：

- it: [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<R> - 要合并的其中一个迭代器。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<(T, R)> - 返回一个新迭代器。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr1: Array<Int64> = [1, 2, 3, 4]
    var arr2: Array<Int64> = [4, 5, 6]

    /* 获取迭代器对象并合并，新迭代器中的元素为对应索引位置元素的元组 */
    var iter1 = arr1.iterator()
    var iter2 = arr2.iterator()
    var iter = iter1.zip(iter2)

    /* 使用迭代器进行遍历，长度取决于较短的迭代器 */
    while (true) {
        match (iter.next()) {
            case Some(i) => println("The current element is (${i[0]}, ${i[1]})")
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
The current element is (1, 4)
The current element is (2, 5)
The current element is (3, 6)
```

### extend\<T> Iterator\<T> where T <: Comparable\<T>

```cangjie
extend<T> Iterator<T> where T <: Comparable<T>
```

功能：为 [Iterator](core_package_classes.md#class-iteratort)\<T> 类型扩展 [Comparable](core_package_interfaces.md#interface-comparablet)\<T> 接口，支持比较操作。

#### func max()

```cangjie
public func max(): Option<T>
```

功能：筛选最大的元素。此方法会消耗迭代器中的所有元素。

返回值：

- [Option](core_package_enums.md#enum-optiont)\<T> - 返回最大的元素，若为空则返回 None。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4]

    /* 获取迭代器对象，使用 max() 求最大值 */
    var iter = arr.iterator()
    match (iter.max()) {
        case Some(i) => println(i)
        case None => println("None!")
    }
    return 0
}
```

运行结果：

```text
4
```

#### func min()

```cangjie
public func min(): Option<T>
```

功能：筛选最小的元素。此方法会消耗迭代器中的所有元素。

返回值：

- [Option](core_package_enums.md#enum-optiont)\<T> - 返回最小的元素，若为空则返回 None。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4]

    /* 获取迭代器对象，使用 min() 求最小值 */
    var iter = arr.iterator()
    match (iter.min()) {
        case Some(i) => println(i)
        case None => println("None!")
    }
    return 0
}
```

运行结果：

```text
1
```

### extend\<T> Iterator\<T> where T <: Equatable\<T>

```cangjie
extend<T> Iterator<T> where T <: Equatable<T>
```

功能：为 [Iterator](core_package_classes.md#class-iteratort)\<T> 类型扩展 扩展 [Equatable](core_package_interfaces.md#interface-equatablet)\<T> 接口，支持判等操作。

#### func contains(T)

```cangjie
public func contains(element: T): Bool
```

功能：遍历所有元素，判断是否包含指定元素。此方法会重复获取并消耗迭代器中元素直到某个元素与参数 `element` 相等。

参数：

- element: T - 要查找的元素。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否包含指定元素。

示例：

<!-- verify -->
```cangjie
main(): Int64 {
    var arr: Array<Int64> = [1, 2, 3, 4]

    /* 获取迭代器对象，查找是否包含元素 3 */
    var iter = arr.iterator()
    println(iter.contains(3))

    /* 使用迭代器进行遍历，输出剩余元素 */
    while (true) {
        match (iter.next()) {
            case Some(i) => println(i)
            case None => break
        }
    }
    return 0
}
```

运行结果：

```text
true
4
```

## class Object

```cangjie
public open class Object <: Any {
    public const init()
}
```

功能：[Object](core_package_classes.md#class-object) 是所有 `class` 的父类，所有 `class` 都默认继承它。[Object](core_package_classes.md#class-object) 类中不包含任何成员，即 [Object](core_package_classes.md#class-object) 是一个“空”的类。

父类型：

- [Any](core_package_interfaces.md#interface-any)

### init()

```cangjie
public const init()
```

功能：构造一个 `object` 实例。

## class RangeIterator\<T> <: Iterator\<T> where T <: Countable\<T> & Comparable\<T> & Equatable\<T>

```cangjie
public class RangeIterator<T> <: Iterator<T> where T <: Countable<T> & Comparable<T> & Equatable<T> {}
```

功能：[Range](core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet) 类型的迭代器，迭代功能详述见 [Iterable](core_package_interfaces.md#interface-iterablee) 和 [Iterator](core_package_classes.md#class-iteratort) 接口说明。

父类型：

- [Iterator](#class-iteratort)\<T>

### func next()

```cangjie
public func next(): Option<T>
```

功能：获取 [Range](core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet) 迭代器中的下一个值。

返回值：

- [Option](core_package_enums.md#enum-optiont)\<T> - [Range](core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet) 迭代器中的下一个成员，用 [Option](core_package_enums.md#enum-optiont) 封装，迭代到末尾时返回 `None`。

## class StackTraceElement

```cangjie
public open class StackTraceElement {
    public let declaringClass: String
    public let methodName: String
    public let fileName: String
    public let lineNumber: Int64
    public init(declaringClass: String, methodName: String, fileName: String, lineNumber: Int64)
}
```

功能：表示一个异常堆栈的具体信息，包括异常发生的类名、函数名、文件名、行号。

### let declaringClass

```cangjie
public let declaringClass: String
```

功能：获取异常发生的类名。

类型：[String](core_package_structs.md#struct-string)

### let fileName

```cangjie
public let fileName: String
```

功能：获取异常发生的文件名。

类型：[String](core_package_structs.md#struct-string)

### let lineNumber

```cangjie
public let lineNumber: Int64
```

功能：获取异常发生的行号。

类型：[Int64](core_package_intrinsics.md#int64)

### let methodName

```cangjie
public let methodName: String
```

功能：获取异常发生的函数名。

类型：[String](core_package_structs.md#struct-string)

### init(String, String, String, Int64)

```cangjie
public init(declaringClass: String, methodName: String, fileName: String, lineNumber: Int64)
```

功能：构造一个异常堆栈实例，指定类名、函数名、文件名、行号。

参数：

- declaringClass: [String](core_package_structs.md#struct-string) - 类名。
- methodName: [String](core_package_structs.md#struct-string) - 函数名。
- fileName: [String](core_package_structs.md#struct-string) - 文件名。
- lineNumber: [Int64](core_package_intrinsics.md#int64) - 行号。

## class StringBuilder

```cangjie
public class StringBuilder <: ToString {
    public init()
    public init(str: String)
    public init(r: Rune, n: Int64)
    public init(value: Array<Rune>)
    public init(capacity: Int64)
}
```

功能：该类主要用于字符串的构建。

[StringBuilder](core_package_classes.md#class-stringbuilder) 在字符串的构建上效率高于 [String](core_package_structs.md#struct-string)：

- 在功能上支持传入多个类型的值，该类将自动将其转换为 [String](core_package_structs.md#struct-string) 类型对象，并追加到构造的字符串中。
- 在性能上使用动态扩容算法，减少内存申请频率，构造字符串的速度更快，占用内存资源通常更少。

> **注意：**
>
> [StringBuilder](core_package_classes.md#class-stringbuilder) 仅支持 UTF-8 编码的字符数据。

父类型：

- [ToString](core_package_interfaces.md#interface-tostring)

### prop capacity

```cangjie
public prop capacity: Int64
```

功能：获取 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例此时能容纳字符串的长度，该值会随扩容的发生而变大。

类型：[Int64](core_package_intrinsics.md#int64)

### prop size

```cangjie
public prop size: Int64
```

功能：获取 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例中字符串长度。

类型：[Int64](core_package_intrinsics.md#int64)

### init()

```cangjie
public init()
```

功能：构造一个初始容量为 32 的空 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例。

### init(Array\<Rune>)

```cangjie
public init(value: Array<Rune>)
```

功能：使用参数 `value` 指定的字符数组初始化一个 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例，该实例的初始容量为 `value` 大小，初始内容为 `value` 包含的字符内容。

参数：

- value: [Array](core_package_structs.md#struct-arrayt)\<Rune> - 初始化 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例的字符数组。

### init(Int64)

```cangjie
public init(capacity: Int64)
```

功能：使用参数 `capacity` 指定的容量初始化一个空 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例，该实例的初始容量为 `value` 大小，初始内容为若干 `\0` 字符。

参数：

- capacity: [Int64](core_package_intrinsics.md#int64) - 初始化 [StringBuilder](core_package_classes.md#class-stringbuilder) 的字节容量，取值范围为 (0, [Int64.Max](./core_package_intrinsics.md)]。

异常：

- [IllegalArgumentException](core_package_exceptions.md#class-illegalargumentexception) - 当参数 `capacity` 的值小于等于 0 时，抛出异常。

### init(Rune, Int64)

```cangjie
public init(r: Rune, n: Int64)
```

功能：使用 `n` 个 `r` 字符初始化 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例，该实例的初始容量为 `n`，初始内容为 `n` 个 `r` 字符。

参数：

- r: Rune - 初始化 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例的字符。
- n: [Int64](core_package_intrinsics.md#int64) - 字符 `r` 的数量，取值范围为 [0, [Int64.Max](./core_package_intrinsics.md)]。

异常：

- [IllegalArgumentException](core_package_exceptions.md#class-illegalargumentexception) - 当参数 `n` 小于 0 时，抛出异常。

### init(String)

```cangjie
public init(str: String)
```

功能：根据指定初始字符串构造 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例，该实例的初始容量为指定字符串的大小，初始内容为指定字符串。

参数：

- str: [String](core_package_structs.md#struct-string) - 初始化 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例的字符串。

### func append(Array\<Rune>)

```cangjie
public func append(runeArr: Array<Rune>): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入一个 `Rune` 数组中所有字符。

参数：

- runeArr: [Array](core_package_structs.md#struct-arrayt)\<Rune> - 插入的 `Rune` 数组。

### func append(Bool)

```cangjie
public func append(b: Bool): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `b` 的字符串表示。

参数：

- b: [Bool](core_package_intrinsics.md#bool) - 插入的 [Bool](core_package_intrinsics.md#bool) 类型的值。

### func append(CString)

```cangjie
public func append(cstr: CString): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `cstr` 指定 [CString](core_package_intrinsics.md#cstring) 中的内容。

参数：

- cstr: [CString](core_package_intrinsics.md#cstring) - 插入的 [CString](core_package_intrinsics.md#cstring)。

### func append(Float16)

```cangjie
public func append(n: Float16): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [Float16](core_package_intrinsics.md#float16) - 插入的 [Float16](core_package_intrinsics.md#float16) 类型的值。

### func append(Float32)

```cangjie
public func append(n: Float32): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [Float32](core_package_intrinsics.md#float32) - 插入的 [Float32](core_package_intrinsics.md#float32) 类型的值。

### func append(Float64)

```cangjie
public func append(n: Float64): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [Float64](core_package_intrinsics.md#float64) - 插入的 [Float64](core_package_intrinsics.md#float64) 类型的值。

### func append(Int16)

```cangjie
public func append(n: Int16): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [Int16](core_package_intrinsics.md#int16) - 插入的 [Int16](core_package_intrinsics.md#int16) 类型的值。

### func append(Int32)

```cangjie
public func append(n: Int32): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [Int32](core_package_intrinsics.md#int32) - 插入的 [Int32](core_package_intrinsics.md#int32) 类型的值。

### func append(Int64)

```cangjie
public func append(n: Int64): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [Int64](core_package_intrinsics.md#int64) - 插入的 [Int64](core_package_intrinsics.md#int64) 类型的值。

### func append(Int8)

```cangjie
public func append(n: Int8): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [Int8](core_package_intrinsics.md#int8) - 插入的 [Int8](core_package_intrinsics.md#int8) 类型的值。

### func append(Rune)

```cangjie
public func append(r: Rune): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `r` 指定的字符。

参数：

- r: Rune - 插入的字符。

### func append(String)

```cangjie
public func append(str: String): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `str` 指定的字符串。

参数：

- str: [String](core_package_structs.md#struct-string) - 插入的字符串。

### func append(StringBuilder)

```cangjie
public func append(sb: StringBuilder): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `sb` 指定的 [StringBuilder](core_package_classes.md#class-stringbuilder) 中的内容。

参数：

- sb: [StringBuilder](core_package_classes.md#class-stringbuilder) - 插入的 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例。

### func append(UInt16)

```cangjie
public func append(n: UInt16): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [UInt16](core_package_intrinsics.md#uint16) - 插入的 [UInt16](core_package_intrinsics.md#uint16) 类型的值。

### func append(UInt32)

```cangjie
public func append(n: UInt32): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [UInt32](core_package_intrinsics.md#uint32) - 插入的 [UInt32](core_package_intrinsics.md#uint32) 类型的值。

### func append(UInt64)

```cangjie
public func append(n: UInt64): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [UInt64](core_package_intrinsics.md#uint64) - 插入的 [UInt64](core_package_intrinsics.md#uint64) 类型的值。

### func append(UInt8)

```cangjie
public func append(n: UInt8): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `n` 的字符串表示。

参数：

- n: [UInt8](core_package_intrinsics.md#uint8) - 插入的 [UInt8](core_package_intrinsics.md#uint8) 类型的值。

### func append\<T>(Array\<T>) where T <: ToString

```cangjie
public func append<T>(val: Array<T>): Unit where T <: ToString
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `val` 指定的 [Array](core_package_structs.md#struct-arrayt)\<T> 的字符串表示，类型 `T` 需要实现 [ToString](core_package_interfaces.md#interface-tostring) 接口。

参数：

- val: [Array](core_package_structs.md#struct-arrayt)\<T> - 插入的 [Array](core_package_structs.md#struct-arrayt)\<T> 类型实例。

### func append\<T>(T) where T <: ToString

```cangjie
public func append<T>(v: T): Unit where T <: ToString
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `v` 指定 `T` 类型的字符串表示，类型 `T` 需要实现 [ToString](core_package_interfaces.md#interface-tostring) 接口。

参数：

- v: T - 插入的 `T` 类型实例。

### func appendFromUtf8(Array\<Byte>)

```cangjie
public func appendFromUtf8(arr: Array<Byte>): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `arr` 指向的字节数组。

该函数要求参数 `arr` 符合 UTF-8 编码，如果不符合，将抛出异常。

参数：

- arr: [Array](core_package_structs.md#struct-arrayt)\<[Byte](core_package_types.md#type-byte)> - 插入的字节数组。

异常：

- [IllegalArgumentException](core_package_exceptions.md#class-illegalargumentexception) - 当字节数组不符合 utf8 编码规则时，抛出异常。

### func appendFromUtf8Unchecked(Array\<Byte>)

```cangjie
public unsafe func appendFromUtf8Unchecked(arr: Array<Byte>): Unit
```

功能：在 [StringBuilder](core_package_classes.md#class-stringbuilder) 末尾插入参数 `arr` 指向的字节数组。

相较于 `appendFromUtf8` 函数，它并没有针对于字节数组进行 UTF-8 相关规则的检查，所以它所构建的字符串并不一定保证是合法的，甚至出现非预期的异常，如果不是某些场景下的速度考虑，请优先使用安全的 `appendFromUtf8` 函数。

参数：

- arr: [Array](core_package_structs.md#struct-arrayt)\<[Byte](core_package_types.md#type-byte)> - 插入的字节数组。

### func reserve(Int64)

```cangjie
public func reserve(additional: Int64): Unit
```

功能：将 [StringBuilder](core_package_classes.md#class-stringbuilder) 扩容 `additional` 大小。

当 `additional` 小于等于零，或剩余容量大于等于 `additional` 时，不发生扩容；当剩余容量小于 `additional` 时，扩容至当前容量的 1.5 倍（向下取整）与 `size` + `additional` 的最大值。

参数：

- additional: [Int64](core_package_intrinsics.md#int64) - 指定 [StringBuilder](core_package_classes.md#class-stringbuilder) 的扩容大小。

### func reset(Option\<Int64>)

```cangjie
public func reset(capacity!: Option<Int64> = None): Unit
```

功能：清空当前 [StringBuilder](core_package_classes.md#class-stringbuilder)，并将容量重置为 `capacity` 指定的值。

参数：

- capacity!: [Option](core_package_enums.md#enum-optiont)\<[Int64](core_package_intrinsics.md#int64)> - 重置后 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例的容量大小，取值范围为 `None` 和 (`Some(0)`, `Some(Int64.Max)`]，默认值 `None` 表示采用默认大小容量（32）。

异常：

- [IllegalArgumentException](core_package_exceptions.md#class-illegalargumentexception) - 当参数 `capacity` 的值小于等于 0 时，抛出异常。

### func toString()

```cangjie
public func toString(): String
```

功能：获取 [StringBuilder](core_package_classes.md#class-stringbuilder) 实例中的字符串。

> **注意：**
>
> 该函数不会将字符串数据进行拷贝。

返回值：

- [String](core_package_structs.md#struct-string) - [StringBuilder](core_package_classes.md#class-stringbuilder) 实例中的字符串。

## class Thread

```cangjie
public class Thread {}
```

功能：获取线程 ID 及名字、查询线程是否存在取消请求、注册线程未处理异常的处理函数等。

该类型实例无法通过构造得到，仅能通过 [Future](core_package_classes.md#class-futuret) 对象的 `thread` 属性或是 [Thread](core_package_classes.md#class-thread) 类的 `currentThread` 静态属性获取。

### static prop currentThread

```cangjie
public static prop currentThread: Thread
```

功能：获取当前执行线程的 [Thread](core_package_classes.md#class-thread) 对象。

类型：[Thread](core_package_classes.md#class-thread)

### prop hasPendingCancellation

```cangjie
public prop hasPendingCancellation: Bool
```

功能：线程是否存在取消请求，即是否通过 future.cancel() 发送过取消请求，常见使用方为 [Thread](core_package_classes.md#class-thread).currentThread.hasPendingCancellation。

类型：[Bool](core_package_intrinsics.md#bool)

### prop id

```cangjie
public prop id: Int64
```

功能：获取当前执行线程的标识，以 [Int64](core_package_intrinsics.md#int64) 表示，所有存活的线程都有不同标识，但不保证当线程执行结束后复用它的标识。

类型：[Int64](core_package_intrinsics.md#int64)

### prop name

```cangjie
public mut prop name: String
```

功能：获取或设置线程的名称，获取设置都具有原子性。

类型：[String](core_package_structs.md#struct-string)

### static func handleUncaughtExceptionBy((Thread, Exception) -> Unit)

```cangjie
public static func handleUncaughtExceptionBy(exHandler: (Thread, Exception) -> Unit): Unit
```

功能：注册线程未处理异常的处理函数。

当某一线程因异常而提前终止后，如果全局的未处理异常函数被注册，那么将调用该函数并结束线程，在该函数内抛出异常时，将向终端打印提示信息并结束线程，但不会打印异常调用栈信息；如果没有注册全局异常处理函数，那么默认会向终端打印异常调用栈信息。

多次注册处理函数时，后续的注册函数将覆盖之前的处理函数。

当有多个线程同时因异常而终止时，处理函数将被并发执行，因而开发者需要在处理函数中确保并发正确性。

处理函数的参数第一个参数类型为 [Thread](core_package_classes.md#class-thread)，是发生异常的线程，第二个参数类型为 [Exception](core_package_exceptions.md#class-exception)，是线程未处理的异常。

参数：

- exHandler: ([Thread](core_package_classes.md#class-thread), [Exception](core_package_exceptions.md#class-exception)) -> [Unit](core_package_intrinsics.md#unit) - 注册的处理函数。

## class ThreadLocal\<T>

```cangjie
public class ThreadLocal<T> {}
```

功能：该类表示仓颉线程局部变量。

和普通变量相比，线程局部变量有不同的访问语义。当多个线程共享使用同一线程局部变量时，每个线程都有各自的一份值拷贝。线程对变量的访问会读写线程本地的值，而不会影响其他线程中变量的值。

### func get()

```cangjie
public func get(): ?T
```

功能：获得仓颉线程局部变量的值。

返回值：

- ?T - 如果当前线程局部变量不为空值，返回该值，如果为空值，返回 `None`。

### func set(?T)

```cangjie
public func set(value: ?T): Unit
```

功能：通过 value 设置仓颉线程局部变量的值，如果传入 `None`，该局部变量的值将被删除，在线程后续操作中将无法获取。

参数：

- value: ?T - 需要设置的局部变量的值。
