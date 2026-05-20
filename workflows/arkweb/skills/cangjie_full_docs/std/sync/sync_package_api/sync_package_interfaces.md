# 接口

## interface Condition

```cangjie
public interface Condition {
    func notify(): Unit
    func notifyAll(): Unit
    func wait(): Unit
    func wait(timeout!: Duration): Bool
    func waitUntil(predicate: () -> Bool): Unit
    func waitUntil(predicate: () -> Bool, timeout!: Duration): Bool
}
```

功能：提供使线程阻塞并等待来自另一个线程的信号以恢复执行的功能的接口。

这是一种利用共享变量进行线程同步的机制，当一些线程因等待共享变量的某个条件成立而挂起时，另一些线程改变共享的变量，使条件成立，
然后执行唤醒操作。这使得挂起的线程被唤醒后可以继续执行。

### func notify()

```cangjie
func notify(): Unit
```

功能：唤醒一个等待在关联互斥体上的线程。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

### func notifyAll()

```cangjie
func notifyAll(): Unit
```

功能：唤醒所有等待在关联互斥体上的线程。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

### func wait()

```cangjie
func wait(): Unit
```

功能：当前线程挂起，直到对应的 `notify` 函数被调用。

> **说明：**
>
> 线程在进入等待时会释放对应的互斥锁，被唤醒后再次持有互斥锁。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

### func wait(Duration)

```cangjie
func wait(timeout!: Duration): Bool
```

功能：当前线程挂起，直到对应的 `notify` 函数被调用，或者挂起时间超过 `timeout`。

> **说明：**
>
> 线程在进入等待时会释放对应的互斥锁，被唤醒后再次持有互斥锁。

参数：

- timeout!: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 挂起时间，其默认值为 [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果 [Monitor <sup>(deprecated)</sup>](sync_package_classes.md#class-monitor-deprecated) 被其他线程唤醒，返回 `true`；如果超时，则返回 `false`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 `timeout` 小于等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero)，抛出异常。
- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

### func waitUntil(()->Bool)

```cangjie
func waitUntil(predicate: () -> Bool): Unit
```

功能：当前线程挂起，直到对应的 `notify` 函数被调用且 `predicate` 结果为 `true`。

> **说明：**
>
> - 线程在进入等待时会释放对应的互斥锁，被唤醒后再次持有互斥锁。
> - 此方法会先判断 `predicate` 结果是否为 `true`，若是则直接返回，否则将当前线程挂起。

参数：

- predicate: () -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 等待为真的条件。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

### func waitUntil(() -> Bool, Duration)

```cangjie
func waitUntil(predicate: () -> Bool, timeout!: Duration): Bool
```

功能：当前线程挂起，直到对应的 `notify` 函数被调用且 `predicate` 结果为 `true`，或者挂起时间超过 `timeout`。

> **说明：**
>
> - 线程在进入等待时会释放对应的互斥锁，被唤醒后再次持有互斥锁。
> - 此方法会先判断 `predicate` 结果是否为 `true`，若是则直接返回 `true`，否则将当前线程挂起。

参数：

- predicate: () -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 等待为真的条件。
- timeout!: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 挂起时间，其默认值为 [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果 [Monitor <sup>(deprecated)</sup>](sync_package_classes.md#class-monitor-deprecated) 被其他线程唤醒且 `predicate` 结果为 `true`，返回 `true`；如果超时，则返回 `false`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 `timeout` 小于等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero)，抛出异常。
- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

## interface IReentrantMutex <sup>(deprecated)</sup>

```cangjie
public interface IReentrantMutex {
    func lock(): Unit
    func tryLock(): Bool
    func unlock(): Unit
}
```

功能：提供实现可重入互斥锁的接口。

> **注意：**
>
> - 未来版本即将废弃，使用 [Lock](#interface-lock) 替代。
> - 开发者在实现该接口时需要保证底层互斥锁确实支持嵌套锁，否则在嵌套使用时，将会产生死锁问题。

### func lock()

```cangjie
func lock(): Unit
```

功能：锁定互斥体。

如果互斥体已被锁定，则阻塞当前线程。

### func tryLock()

```cangjie
func tryLock(): Bool
```

功能：尝试锁定互斥体。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果互斥体已被锁定，则返回 false；反之，则锁定互斥体并返回 true。

### func unlock()

```cangjie
func unlock(): Unit
```

功能：解锁互斥体。

如果互斥体被重复加锁了 N 次，那么需要调用 N 次该函数来完全解锁。一旦互斥体被完全解锁，如果有其他线程阻塞在此锁上，则唤醒其中一个线程。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

## interface Lock

```cangjie
public interface Lock {
    func lock(): Unit
    func tryLock(): Bool
    func unlock(): Unit
}
```

功能：提供实现可重入互斥锁的接口。

> **注意：**
>
> 开发者在实现该接口时需要保证底层互斥锁确实支持嵌套锁，否则在嵌套使用时，将会产生死锁问题。

### func lock()

```cangjie
func lock(): Unit
```

功能：锁定互斥体。

如果互斥体已被锁定，则阻塞当前线程。

### func tryLock()

```cangjie
func tryLock(): Bool
```

功能：尝试锁定互斥体。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果互斥体已被锁定，则返回 false；反之，则锁定互斥体并返回 true。

### func unlock()

```cangjie
func unlock(): Unit
```

功能：解锁互斥体。

如果互斥体被重复加锁了 N 次，那么需要调用 N 次该函数来完全解锁。一旦互斥体被完全解锁，如果有其他线程阻塞在此锁上，则唤醒其中一个线程。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

## interface UniqueLock

```cangjie
public interface UniqueLock <: Lock {
    func condition(): Condition
}
```

功能：提供实现独占锁的接口。

父类型：

- [Lock](#interface-lock)

### func condition()

```cangjie
func condition(): Condition
```

功能：创建一个与该 [Lock](#interface-lock) 相关的 [Condition](#interface-condition)。

可能被用来实现 “单 Lock 多等待队列” 的并发原语。

返回值：

- [Condition](#interface-condition) - 创建的与该 [Lock](#interface-lock) 相关的 [Condition](#interface-condition) 实例。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。
