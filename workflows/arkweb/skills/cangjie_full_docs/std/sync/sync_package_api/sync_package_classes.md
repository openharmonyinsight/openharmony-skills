# 类

## class AtomicBool

```cangjie
public class AtomicBool {
    public init(val: Bool)
}
```

功能：提供 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型的原子操作相关函数。

### init(Bool)

```cangjie
public init(val: Bool)
```

功能：构造一个封装 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 数据类型的原子类型 [AtomicBool](sync_package_classes.md#class-atomicbool) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 原子类型的初始值。

### func compareAndSwap(Bool, Bool)

```cangjie
public func compareAndSwap(old: Bool, new: Bool): Bool
```

功能：CAS（Compare and Swap）操作，采用[默认内存排序方式](sync_package_constants_vars.md#let-defaultmemoryorder-deprecated)。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 与当前原子类型进行比较的值。
- new: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(Bool, Bool, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: Bool, new: Bool, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(Bool, Bool)](#func-compareandswapbool-bool) 替代。

参数：

- old: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 与当前原子类型进行比较的值。
- new: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func load()

```cangjie
public func load(): Bool
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): Bool
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当前原子类型的值。

### func store(Bool)

```cangjie
public func store(val: Bool): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 写入原子类型的值。

### func store(Bool, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: Bool, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(Bool)](#func-storebool) 替代。

参数：

- val: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(Bool)

```cangjie
public func swap(val: Bool): Bool
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 写入前的值。

### func swap(Bool, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: Bool, memoryOrder!: MemoryOrder): Bool
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(Bool)](#func-swapbool) 替代。

参数：

- val: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 写入前的值。

## class AtomicInt16

```cangjie
public class AtomicInt16 {
    public init(val: Int16)
}
```

功能：提供 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型的原子操作相关函数。

### init(Int16)

```cangjie
public init(val: Int16)
```

功能：构造一个封装 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 数据类型的原子类型 [AtomicInt16](sync_package_classes.md#class-atomicint16) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 原子类型的初始值。

### func compareAndSwap(Int16, Int16)

```cangjie
public func compareAndSwap(old: Int16, new: Int16): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与当前原子类型进行比较的值。
- new: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`

### func compareAndSwap(Int16, Int16, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: Int16, new: Int16, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(Int16, Int16)](#func-compareandswapint16-int16) 替代。

参数：

- old: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与当前原子类型进行比较的值。
- new: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func fetchAdd(Int16)

```cangjie
public func fetchAdd(val: Int16): Int16
```

功能：采用默认内存排序方式，将原子类型的值与参数 `val` 进行加操作，将结果写入当前原子类型实例，并返回加操作前的值。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行加操作的值。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行加操作前的值。

### func fetchAdd(Int16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAdd(val: Int16, memoryOrder!: MemoryOrder): Int16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将原子类型的值与参数 `val` 进行加操作。将结果写入当前原子类型实例，并返回加法运算前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAdd(Int16)](#func-fetchaddint16) 替代。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行加操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行加操作前的值。

### func fetchAnd(Int16)

```cangjie
public func fetchAnd(val: Int16): Int16
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行与操作的值。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行与操作前的值。

### func fetchAnd(Int16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAnd(val: Int16, memoryOrder!: MemoryOrder): Int16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAnd(Int16)](#func-fetchandint16) 替代。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行与操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行与操作前的值。

### func fetchOr(Int16)

```cangjie
public func fetchOr(val: Int16): Int16
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行或操作的值。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行或操作前的值。

### func fetchOr(Int16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchOr(val: Int16, memoryOrder!: MemoryOrder): Int16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchOr(Int16)](#func-fetchorint16) 替代。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行或操作前的值。

### func fetchSub(Int16)

```cangjie
public func fetchSub(val: Int16): Int16
```

功能：采用默认内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行减操作的值。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行减操作前的值。

### func fetchSub(Int16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchSub(val: Int16, memoryOrder!: MemoryOrder): Int16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchSub(Int16)](#func-fetchsubint16) 替代。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行减操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行减操作前的值。

### func fetchXor(Int16)

```cangjie
public func fetchXor(val: Int16): Int16
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行异或操作的值。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行异或操作前的值。

### func fetchXor(Int16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchXor(val: Int16, memoryOrder!: MemoryOrder): Int16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchXor(Int16)](#func-fetchxorint16) 替代。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 与原子类型进行异或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 执行异或操作前的值。

### func load()

```cangjie
public func load(): Int16
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): Int16
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-1) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 当前原子类型的值。

### func store(Int16)

```cangjie
public func store(val: Int16): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 写入原子类型的值。

### func store(Int16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: Int16, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(Int16)](#func-storeint16) 替代。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(Int16)

```cangjie
public func swap(val: Int16): Int16
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 写入原子类型的值。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 写入前的值。

### func swap(Int16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: Int16, memoryOrder!: MemoryOrder): Int16
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(Int16)](#func-swapint16) 替代。

参数：

- val: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 写入前的值。

## class AtomicInt32

```cangjie
public class AtomicInt32 {
    public init(val: Int32)
}
```

功能：提供 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型的原子操作相关函数。

### init(Int32)

```cangjie
public init(val: Int32)
```

功能：构造一个封装 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 数据类型的原子类型 [AtomicInt32](sync_package_classes.md#class-atomicint32) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 原子类型的初始值。

### func compareAndSwap(Int32, Int32)

```cangjie
public func compareAndSwap(old: Int32, new: Int32): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与当前原子类型进行比较的值。
- new: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(Int32, Int32, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: Int32, new: Int32, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(Int32, Int32)](#func-compareandswapint32-int32) 替代。

参数：

- old: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与当前原子类型进行比较的值。
- new: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func fetchAdd(Int32)

```cangjie
public func fetchAdd(val: Int32): Int32
```

功能：采用默认内存排序方式，将原子类型的值与参数 `val` 进行加操作，将结果写入当前原子类型实例，并返回加操作前的值。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行加操作的值。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行加操作前的值。

### func fetchAdd(Int32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAdd(val: Int32, memoryOrder!: MemoryOrder): Int32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将原子类型的值与参数 `val` 进行加操作。将结果写入当前原子类型实例，并返回加法运算前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAdd(Int32)](#func-fetchaddint32) 替代。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行加操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行加操作前的值。

### func fetchAnd(Int32)

```cangjie
public func fetchAnd(val: Int32): Int32
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行与操作的值。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行与操作前的值。

### func fetchAnd(Int32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAnd(val: Int32, memoryOrder!: MemoryOrder): Int32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAnd(Int32)](#func-fetchandint32) 替代。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行与操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行与操作前的值。

### func fetchOr(Int32)

```cangjie
public func fetchOr(val: Int32): Int32
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行或操作的值。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行或操作前的值。

### func fetchOr(Int32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchOr(val: Int32, memoryOrder!: MemoryOrder): Int32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchOr(Int32)](#func-fetchorint32) 替代。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行或操作前的值。

### func fetchSub(Int32)

```cangjie
public func fetchSub(val: Int32): Int32
```

功能：采用默认内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行减操作的值。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行减操作前的值。

### func fetchSub(Int32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchSub(val: Int32, memoryOrder!: MemoryOrder): Int32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchSub(Int32)](#func-fetchsubint32) 替代。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行减操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行减操作前的值。

### func fetchXor(Int32)

```cangjie
public func fetchXor(val: Int32): Int32
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行异或操作的值。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行异或操作前的值。

### func fetchXor(Int32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchXor(val: Int32, memoryOrder!: MemoryOrder): Int32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchXor(Int32)](#func-fetchxorint32) 替代。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 与原子类型进行异或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行异或操作前的值。

### func load()

```cangjie
public func load(): Int32
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): Int32
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-2) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 当前原子类型的值。

### func store(Int32)

```cangjie
public func store(val: Int32): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 写入原子类型的值。

### func store(Int32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: Int32, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(Int32)](#func-storeint32) 替代。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(Int32)

```cangjie
public func swap(val: Int32): Int32
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 写入原子类型的值。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 写入前的值。

### func swap(Int32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: Int32, memoryOrder!: MemoryOrder): Int32
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(Int32)](#func-swapint32) 替代。

参数：

- val: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 写入前的值。

## class AtomicInt64

```cangjie
public class AtomicInt64 {
    public init(val: Int64)
}
```

功能：提供 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型的原子操作相关函数。

### init(Int64)

```cangjie
public init(val: Int64)
```

功能：构造一个封装 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 数据类型的原子类型 [AtomicInt64](sync_package_classes.md#class-atomicint64) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 原子类型的初始值。

### func compareAndSwap(Int64, Int64)

```cangjie
public func compareAndSwap(old: Int64, new: Int64): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与当前原子类型进行比较的值。
- new: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(Int64, Int64, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: Int64, new: Int64, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(Int64, Int64)](#func-compareandswapint64-int64) 替代。

参数：

- old: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与当前原子类型进行比较的值。
- new: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func fetchAdd(Int64)

```cangjie
public func fetchAdd(val: Int64): Int64
```

功能：采用默认内存排序方式，将原子类型的值与参数 `val` 进行加操作，将结果写入当前原子类型实例，并返回加操作前的值。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行加操作的值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行加操作前的值。

### func fetchAdd(Int64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAdd(val: Int64, memoryOrder!: MemoryOrder): Int64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将原子类型的值与参数 `val` 进行加操作。将结果写入当前原子类型实例，并返回加法运算前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAdd(Int64)](#func-fetchaddint64) 替代。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行加操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行加操作前的值。

### func fetchAnd(Int64)

```cangjie
public func fetchAnd(val: Int64): Int64
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行与操作的值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行与操作前的值。

### func fetchAnd(Int64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAnd(val: Int64, memoryOrder!: MemoryOrder): Int64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAnd(Int64)](#func-fetchandint64) 替代。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行与操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行与操作前的值。

### func fetchOr(Int64)

```cangjie
public func fetchOr(val: Int64): Int64
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行或操作的值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行或操作前的值。

### func fetchOr(Int64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchOr(val: Int64, memoryOrder!: MemoryOrder): Int64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchOr(Int64)](#func-fetchorint64) 替代。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行或操作前的值。

### func fetchSub(Int64)

```cangjie
public func fetchSub(val: Int64): Int64
```

功能：采用默认内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行减操作的值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行减操作前的值。

### func fetchSub(Int64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchSub(val: Int64, memoryOrder!: MemoryOrder): Int64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchSub(Int64)](#func-fetchsubint64) 替代。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行减操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行减操作前的值。

### func fetchXor(Int64)

```cangjie
public func fetchXor(val: Int64): Int64
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行异或操作的值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行异或操作前的值。

### func fetchXor(Int64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchXor(val: Int64, memoryOrder!: MemoryOrder): Int64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchXor(Int64)](#func-fetchxorint64) 替代。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 与原子类型进行异或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行异或操作前的值。

### func load()

```cangjie
public func load(): Int64
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): Int64
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-3) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前原子类型的值。

### func store(Int64)

```cangjie
public func store(val: Int64): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入原子类型的值。

### func store(Int64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: Int64, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(Int64)](#func-storeint64) 替代。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(Int64)

```cangjie
public func swap(val: Int64): Int64
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入原子类型的值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入前的值。

### func swap(Int64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: Int64, memoryOrder!: MemoryOrder): Int64
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(Int64)](#func-swapint64) 替代。

参数：

- val: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入前的值。

示例：

<!-- verify -->
```cangjie
import std.sync.*

let count = AtomicInt64(1)

main(): Int64 {
    var val1 = 0
    if (count.compareAndSwap(1, 2)) {
        val1 = count.load()
        println("count1 = ${val1}")
    }

    if (count.fetchAdd(2) == val1) {
        var val2 = count.load()
        println("count2 = ${val2}")
    }

    count.store(6)
    var val3 = count.load()
    println("count3 = ${val3}")

    if (count.swap(8) == val3) {
        var val4 = count.load()
        println("count4 = ${val4}")
    }

    return 0
}
```

运行结果：

```text
count1 = 2
count2 = 4
count3 = 6
count4 = 8
```

## class AtomicInt8

```cangjie
public class AtomicInt8 {
    public init(val: Int8)
}
```

功能：提供 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型的原子操作相关函数。

### init(Int8)

```cangjie
public init(val: Int8)
```

功能：构造一个封装 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 数据类型的原子类型 [AtomicInt8](sync_package_classes.md#class-atomicint8) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 原子类型的初始值。

### func compareAndSwap(Int8, Int8)

```cangjie
public func compareAndSwap(old: Int8, new: Int8): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与当前原子类型进行比较的值。
- new: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(Int8, Int8, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: Int8, new: Int8, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(Int8, Int8)](#func-compareandswapint8-int8) 替代。

参数：

- old: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与当前原子类型进行比较的值。
- new: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func fetchAdd(Int8)

```cangjie
public func fetchAdd(val: Int8): Int8
```

功能：采用默认内存排序方式，将原子类型的值与参数 `val` 进行加操作，将结果写入当前原子类型实例，并返回加操作前的值。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行加操作的值。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行加操作前的值。

### func fetchAdd(Int8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAdd(val: Int8, memoryOrder!: MemoryOrder): Int8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将原子类型的值与参数 `val` 进行加操作。将结果写入当前原子类型实例，并返回加法运算前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAdd(Int8)](#func-fetchaddint8) 替代。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行加操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行加操作前的值。

### func fetchAnd(Int8)

```cangjie
public func fetchAnd(val: Int8): Int8
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行与操作的值。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行与操作前的值。

### func fetchAnd(Int8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAnd(val: Int8, memoryOrder!: MemoryOrder): Int8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAnd(Int8)](#func-fetchandint8) 替代。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行与操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行与操作前的值。

### func fetchOr(Int8)

```cangjie
public func fetchOr(val: Int8): Int8
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行或操作的值。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行或操作前的值。

### func fetchOr(Int8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchOr(val: Int8, memoryOrder!: MemoryOrder): Int8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchOr(Int8)](#func-fetchorint8) 替代。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行或操作前的值。

### func fetchSub(Int8)

```cangjie
public func fetchSub(val: Int8): Int8
```

功能：采用默认内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行减操作的值。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行减操作前的值。

### func fetchSub(Int8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchSub(val: Int8, memoryOrder!: MemoryOrder): Int8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchSub(Int8)](#func-fetchsubint8) 替代。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行减操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行减操作前的值。

### func fetchXor(Int8)

```cangjie
public func fetchXor(val: Int8): Int8
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行异或操作的值。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行异或操作前的值。

### func fetchXor(Int8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchXor(val: Int8, memoryOrder!: MemoryOrder): Int8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchXor(Int8)](#func-fetchxorint8) 替代。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 与原子类型进行异或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 执行异或操作前的值。

### func load()

```cangjie
public func load(): Int8
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): Int8
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-4) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 当前原子类型的值。

### func store(Int8)

```cangjie
public func store(val: Int8): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 写入原子类型的值。

### func store(Int8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: Int8, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(Int8)](#func-storeint8) 替代。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(Int8)

```cangjie
public func swap(val: Int8): Int8
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 写入原子类型的值。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 写入前的值。

### func swap(Int8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: Int8, memoryOrder!: MemoryOrder): Int8
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(Int8)](#func-swapint8) 替代。

参数：

- val: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 写入前的值。

## class AtomicOptionReference\<T> where T <: Object

```cangjie
public class AtomicOptionReference<T> where T <: Object {
    public init()
    public init(val: Option<T>)
}
```

功能：提供引用类型原子操作相关函数。

该引用类型必须是 [Object](../../core/core_package_api/core_package_classes.md#class-object) 的子类。

### init()

```cangjie
public init()
```

功能：构造一个空的 [AtomicOptionReference](sync_package_classes.md#class-atomicoptionreferencet-where-t--object) 实例。

### init(Option\<T>)

```cangjie
public init(val: Option<T>)
```

功能：构造一个封装 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> 数据类型的原子类型 [AtomicOptionReference](sync_package_classes.md#class-atomicoptionreferencet-where-t--object) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 原子类型的初始值。

### func compareAndSwap(Option\<T>, Option\<T>)

```cangjie
public func compareAndSwap(old: Option<T>, new: Option<T>): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 与当前原子类型进行比较的值。
- new: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(Option\<T>, Option\<T>, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: Option<T>, new: Option<T>, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(Option\<T>, Option\<T>)](#func-compareandswapoptiont-optiont) 替代。

参数：

- old: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 与当前原子类型进行比较的值。
- new: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func load()

```cangjie
public func load(): Option<T>
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): Option<T>
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-5) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 当前原子类型的值。

### func store(Option\<T>)

```cangjie
public func store(val: Option<T>): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 写入原子类型的值。

### func store(Option\<T>, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: Option<T>, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(Option\<T>)](#func-storeoptiont) 替代。

参数：

- val: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(Option\<T>)

```cangjie
public func swap(val: Option<T>): Option<T>
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 写入原子类型的值。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 写入前的值。

### func swap(Option\<T>, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: Option<T>, memoryOrder!: MemoryOrder): Option<T>
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(Option\<T>)](#func-swapoptiont) 替代。

参数：

- val: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 写入前的值。

## class AtomicReference\<T> where T <: Object

```cangjie
public class AtomicReference<T> where T <: Object {
    public init(val: T)
}
```

功能：引用类型原子操作相关函数。

该引用类型必须是 [Object](../../core/core_package_api/core_package_classes.md#class-object) 的子类。

### init(T)

```cangjie
public init(val: T)
```

功能：构造一个封装 `T` 数据类型的原子类型 [AtomicReference](sync_package_classes.md#class-atomicreferencet-where-t--object) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: T - 原子类型的初始值。

### func compareAndSwap(T, T)

```cangjie
public func compareAndSwap(old: T, new: T): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: T - 与当前原子类型进行比较的值。
- new: T - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(T, T, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: T, new: T, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(T, T)](#func-compareandswapt-t) 替代。

参数：

- old: T - 与当前原子类型进行比较的值。
- new: T - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func load()

```cangjie
public func load(): T
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- T - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): T
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-6) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- T - 当前原子类型的值。

### func store(T)

```cangjie
public func store(val: T): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: T - 写入原子类型的值。

### func store(T, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: T, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(T)](#func-storet) 替代。

参数：

- val: T - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(T)

```cangjie
public func swap(val: T): T
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: T - 写入原子类型的值。

返回值：

- T - 写入前的值。

### func swap(T, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: T, memoryOrder!: MemoryOrder): T
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(T)](#func-swapt) 替代。

参数：

- val: T - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- T - 写入前的值。

## class AtomicUInt16

```cangjie
public class AtomicUInt16 {
    public init(val: UInt16)
}
```

功能：提供 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型的原子操作相关函数。

### init(UInt16)

```cangjie
public init(val: UInt16)
```

功能：构造一个封装 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 数据类型的原子类型 [AtomicUInt16](sync_package_classes.md#class-atomicuint16) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 原子类型的初始值。

### func compareAndSwap(UInt16, UInt16)

```cangjie
public func compareAndSwap(old: UInt16, new: UInt16): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与当前原子类型进行比较的值。
- new: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(UInt16, UInt16, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: UInt16, new: UInt16, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(UInt16, UInt16)](#func-compareandswapuint16-uint16) 替代。

参数：

- old: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与当前原子类型进行比较的值。
- new: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func fetchAdd(UInt16)

```cangjie
public func fetchAdd(val: UInt16): UInt16
```

功能：采用默认内存排序方式，将原子类型的值与参数 `val` 进行加操作，将结果写入当前原子类型实例，并返回加操作前的值。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行加操作的值。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行加操作前的值。

### func fetchAdd(UInt16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAdd(val: UInt16, memoryOrder!: MemoryOrder): UInt16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将原子类型的值与参数 `val` 进行加操作。将结果写入当前原子类型实例，并返回加法运算前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAdd(UInt16)](#func-fetchadduint16) 替代。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行加操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行加操作前的值。

### func fetchAnd(UInt16)

```cangjie
public func fetchAnd(val: UInt16): UInt16
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行与操作的值。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行与操作前的值。

### func fetchAnd(UInt16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAnd(val: UInt16, memoryOrder!: MemoryOrder): UInt16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAnd(UInt16)](#func-fetchanduint16) 替代。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行与操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行与操作前的值。

### func fetchOr(UInt16)

```cangjie
public func fetchOr(val: UInt16): UInt16
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行或操作的值。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行或操作前的值。

### func fetchOr(UInt16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchOr(val: UInt16, memoryOrder!: MemoryOrder): UInt16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchOr(UInt16)](#func-fetchoruint16) 替代。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行或操作前的值。

### func fetchSub(UInt16)

```cangjie
public func fetchSub(val: UInt16): UInt16
```

功能：采用默认内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行减操作的值。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行减操作前的值。

### func fetchSub(UInt16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchSub(val: UInt16, memoryOrder!: MemoryOrder): UInt16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchSub(UInt16)](#func-fetchsubuint16) 替代。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行减操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行减操作前的值。

### func fetchXor(UInt16)

```cangjie
public func fetchXor(val: UInt16): UInt16
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行异或操作的值。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行异或操作前的值。

### func fetchXor(UInt16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchXor(val: UInt16, memoryOrder!: MemoryOrder): UInt16
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchXor(UInt16)](#func-fetchxoruint16) 替代。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 与原子类型进行异或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 执行异或操作前的值。

### func load()

```cangjie
public func load(): UInt16
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): UInt16
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-7) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 当前原子类型的值。

### func store(UInt16)

```cangjie
public func store(val: UInt16): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 写入原子类型的值。

### func store(UInt16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: UInt16, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(UInt16)](#func-storeuint16) 替代。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(UInt16)

```cangjie
public func swap(val: UInt16): UInt16
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 写入原子类型的值。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 写入前的值。

### func swap(UInt16, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: UInt16, memoryOrder!: MemoryOrder): UInt16
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(UInt16)](#func-swapuint16) 替代。

参数：

- val: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 写入前的值。

## class AtomicUInt32

```cangjie
public class AtomicUInt32 {
    public init(val: UInt32)
}
```

功能：提供 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型的原子操作相关函数。

### init(UInt32)

```cangjie
public init(val: UInt32)
```

功能：构造一个封装 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 数据类型的原子类型 [AtomicUInt32](sync_package_classes.md#class-atomicuint32) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 原子类型的初始值。

### func compareAndSwap(UInt32, UInt32)

```cangjie
public func compareAndSwap(old: UInt32, new: UInt32): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与当前原子类型进行比较的值。
- new: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(UInt32, UInt32, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: UInt32, new: UInt32, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(UInt32, UInt32)](#func-compareandswapuint32-uint32) 替代。

参数：

- old: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与当前原子类型进行比较的值。
- new: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func fetchAdd(UInt32)

```cangjie
public func fetchAdd(val: UInt32): UInt32
```

功能：采用默认内存排序方式，将原子类型的值与参数 `val` 进行加操作，将结果写入当前原子类型实例，并返回加操作前的值。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行加操作的值。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行加操作前的值。

### func fetchAdd(UInt32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAdd(val: UInt32, memoryOrder!: MemoryOrder): UInt32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将原子类型的值与参数 `val` 进行加操作。将结果写入当前原子类型实例，并返回加法运算前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAdd(UInt32)](#func-fetchadduint32) 替代。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行加操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行加操作前的值。

### func fetchAnd(UInt32)

```cangjie
public func fetchAnd(val: UInt32): UInt32
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行与操作的值。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行与操作前的值。

### func fetchAnd(UInt32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAnd(val: UInt32, memoryOrder!: MemoryOrder): UInt32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAnd(UInt32)](#func-fetchanduint32) 替代。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行与操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行与操作前的值。

### func fetchOr(UInt32)

```cangjie
public func fetchOr(val: UInt32): UInt32
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行或操作的值。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行或操作前的值。

### func fetchOr(UInt32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchOr(val: UInt32, memoryOrder!: MemoryOrder): UInt32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchOr(UInt32)](#func-fetchoruint32) 替代。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行或操作前的值。

### func fetchSub(UInt32)

```cangjie
public func fetchSub(val: UInt32): UInt32
```

功能：采用默认内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行减操作的值。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行减操作前的值。

### func fetchSub(UInt32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchSub(val: UInt32, memoryOrder!: MemoryOrder): UInt32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchSub(UInt32)](#func-fetchsubuint32) 替代。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行减操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行减操作前的值。

### func fetchXor(UInt32)

```cangjie
public func fetchXor(val: UInt32): UInt32
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行异或操作的值。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行异或操作前的值。

### func fetchXor(UInt32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchXor(val: UInt32, memoryOrder!: MemoryOrder): UInt32
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchXor(UInt32)](#func-fetchxoruint32) 替代。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 与原子类型进行异或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 执行异或操作前的值。

### func load()

```cangjie
public func load(): UInt32
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): UInt32
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-8) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 当前原子类型的值。

### func store(UInt32)

```cangjie
public func store(val: UInt32): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 写入原子类型的值。

### func store(UInt32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: UInt32, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(UInt32)](#func-storeuint32) 替代。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(UInt32)

```cangjie
public func swap(val: UInt32): UInt32
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 写入原子类型的值。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 写入前的值。

### func swap(UInt32, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: UInt32, memoryOrder!: MemoryOrder): UInt32
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(UInt32)](#func-swapuint32) 替代。

参数：

- val: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 写入前的值。

## class AtomicUInt64

```cangjie
public class AtomicUInt64 {
    public init(val: UInt64)
}
```

功能：提供 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型的原子操作相关函数。

### init(UInt64)

```cangjie
public init(val: UInt64)
```

功能：构造一个封装 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 数据类型的原子类型 [AtomicUInt64](sync_package_classes.md#class-atomicuint64) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 原子类型的初始值。

### func compareAndSwap(UInt64, UInt64)

```cangjie
public func compareAndSwap(old: UInt64, new: UInt64): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与当前原子类型进行比较的值。
- new: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(UInt64, UInt64, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: UInt64, new: UInt64, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(UInt64, UInt64)](#func-compareandswapuint64-uint64) 替代。

参数：

- old: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与当前原子类型进行比较的值。
- new: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func fetchAdd(UInt64)

```cangjie
public func fetchAdd(val: UInt64): UInt64
```

功能：采用默认内存排序方式，将原子类型的值与参数 `val` 进行加操作，将结果写入当前原子类型实例，并返回加操作前的值。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行加操作的值。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行加操作前的值。

### func fetchAdd(UInt64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAdd(val: UInt64, memoryOrder!: MemoryOrder): UInt64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将原子类型的值与参数 `val` 进行加操作。将结果写入当前原子类型实例，并返回加法运算前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAdd(UInt64)](#func-fetchadduint64) 替代。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行加操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行加操作前的值。

### func fetchAnd(UInt64)

```cangjie
public func fetchAnd(val: UInt64): UInt64
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行与操作的值。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行与操作前的值。

### func fetchAnd(UInt64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAnd(val: UInt64, memoryOrder!: MemoryOrder): UInt64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAnd(UInt64)](#func-fetchanduint64) 替代。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行与操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行与操作前的值。

### func fetchOr(UInt64)

```cangjie
public func fetchOr(val: UInt64): UInt64
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行或操作的值。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行或操作前的值。

### func fetchOr(UInt64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchOr(val: UInt64, memoryOrder!: MemoryOrder): UInt64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchOr(UInt64)](#func-fetchoruint64) 替代。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行或操作前的值。

### func fetchSub(UInt64)

```cangjie
public func fetchSub(val: UInt64): UInt64
```

功能：采用默认内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行减操作的值。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行减操作前的值。

### func fetchSub(UInt64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchSub(val: UInt64, memoryOrder!: MemoryOrder): UInt64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchSub(UInt64)](#func-fetchsubuint64) 替代。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行减操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行减操作前的值。

### func fetchXor(UInt64)

```cangjie
public func fetchXor(val: UInt64): UInt64
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行异或操作的值。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行异或操作前的值。

### func fetchXor(UInt64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchXor(val: UInt64, memoryOrder!: MemoryOrder): UInt64
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchXor(UInt64)](#func-fetchxoruint64) 替代。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 与原子类型进行异或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 执行异或操作前的值。

### func load()

```cangjie
public func load(): UInt64
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): UInt64
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-9) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 当前原子类型的值。

### func store(UInt64)

```cangjie
public func store(val: UInt64): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 写入原子类型的值。

### func store(UInt64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: UInt64, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(UInt64)](#func-storeuint64) 替代。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(UInt64)

```cangjie
public func swap(val: UInt64): UInt64
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 写入原子类型的值。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 写入前的值。

### func swap(UInt64, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: UInt64, memoryOrder!: MemoryOrder): UInt64
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(UInt64)](#func-swapuint64) 替代。

参数：

- val: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 写入前的值。

## class AtomicUInt8

```cangjie
public class AtomicUInt8 {
    public init(val: UInt8)
}
```

功能：提供 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型的原子操作相关函数。

### init(UInt8)

```cangjie
public init(val: UInt8)
```

功能：构造一个封装 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 数据类型的原子类型 [AtomicUInt8](sync_package_classes.md#class-atomicuint8) 的实例，其内部数据初始值为入参 `val` 的值。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 原子类型的初始值。

### func compareAndSwap(UInt8, UInt8)

```cangjie
public func compareAndSwap(old: UInt8, new: UInt8): Bool
```

功能：CAS 操作，采用默认内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，则写入参数 `new` 指定的值，并返回 `true`；否则，不写入值，并返回 `false`。

参数：

- old: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与当前原子类型进行比较的值。
- new: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 比较结果相等时，写入原子类型的值。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func compareAndSwap(UInt8, UInt8, MemoryOrder, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func compareAndSwap(old: UInt8, new: UInt8, successOrder!: MemoryOrder, failureOrder!: MemoryOrder): Bool
```

功能：CAS 操作，成功时使用 `successOrder` 指定的内存排序方式，失败时则使用 `failureOrder` 指定的内存排序方式。

比较当前原子类型的值与参数 `old` 指定的值是否相等。若相等，写入参数 `new` 指定的值，返回 `true`；否则，不写入值，并返回 `false`。

> **注意：**
>
> 未来版本即将废弃，使用 [compareAndSwap(UInt8, UInt8)](#func-compareandswapuint8-uint8) 替代。

参数：

- old: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与当前原子类型进行比较的值。
- new: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 比较结果相等时，写入原子类型的值。
- successOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作成功时，执行“读 > 修改 > 写”操作需要的内存排序方式。
- failureOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - CAS 操作失败时，执行“读”操作需要的内存排序方式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 比较后交换成功返回 `true`，否则返回 `false`。

### func fetchAdd(UInt8)

```cangjie
public func fetchAdd(val: UInt8): UInt8
```

功能：采用默认内存排序方式，将原子类型的值与参数 `val` 进行加操作，将结果写入当前原子类型实例，并返回加操作前的值。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行加操作的值。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行加操作前的值。

### func fetchAdd(UInt8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAdd(val: UInt8, memoryOrder!: MemoryOrder): UInt8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将原子类型的值与参数 `val` 进行加操作。将结果写入当前原子类型实例，并返回加法运算前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAdd(UInt8)](#func-fetchadduint8) 替代。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行加操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行加操作前的值。

### func fetchAnd(UInt8)

```cangjie
public func fetchAnd(val: UInt8): UInt8
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行与操作的值。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行与操作前的值。

### func fetchAnd(UInt8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchAnd(val: UInt8, memoryOrder!: MemoryOrder): UInt8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行与操作。将结果写入当前原子类型实例，并返回与操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchAnd(UInt8)](#func-fetchanduint8) 替代。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行与操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行与操作前的值。

### func fetchOr(UInt8)

```cangjie
public func fetchOr(val: UInt8): UInt8
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行或操作的值。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行或操作前的值。

### func fetchOr(UInt8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchOr(val: UInt8, memoryOrder!: MemoryOrder): UInt8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行或操作。将结果写入当前原子类型实例，并返回或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchOr(UInt8)](#func-fetchoruint8) 替代。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行或操作前的值。

### func fetchSub(UInt8)

```cangjie
public func fetchSub(val: UInt8): UInt8
```

功能：采用默认内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行减操作的值。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行减操作前的值。

### func fetchSub(UInt8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchSub(val: UInt8, memoryOrder!: MemoryOrder): UInt8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，以原子类型的值为被减数，参数 `val` 为减数，做减操作。将结果写入当前原子类型实例，并返回减操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchSub(UInt8)](#func-fetchsubuint8) 替代。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行减操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行减操作前的值。

### func fetchXor(UInt8)

```cangjie
public func fetchXor(val: UInt8): UInt8
```

功能：采用默认内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行异或操作的值。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行异或操作前的值。

### func fetchXor(UInt8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func fetchXor(val: UInt8, memoryOrder!: MemoryOrder): UInt8
```

功能：采用参数 `memoryOrder` 指定的内存排序方式，将当前原子类型实例的值与参数 `val` 进行异或操作。将结果写入当前原子类型实例，并返回异或操作前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [fetchXor(UInt8)](#func-fetchxoruint8) 替代。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 与原子类型进行异或操作的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 执行异或操作前的值。

### func load()

```cangjie
public func load(): UInt8
```

功能：读取操作，采用默认内存排序方式，读取原子类型的值。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 当前原子类型的值。

### func load(MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func load(memoryOrder!: MemoryOrder): UInt8
```

功能：读取操作，采用参数 `memoryOrder` 指定的内存排序方式，读取原子类型的值。

> **注意：**
>
> 未来版本即将废弃，使用 [load()](#func-load-10) 替代。

参数：

- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 当前原子类型的值。

### func store(UInt8)

```cangjie
public func store(val: UInt8): Unit
```

功能：写入操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 写入原子类型的值。

### func store(UInt8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func store(val: UInt8, memoryOrder!: MemoryOrder): Unit
```

功能：写入操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型。

> **注意：**
>
> 未来版本即将废弃，使用 [store(UInt8)](#func-storeuint8) 替代。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

### func swap(UInt8)

```cangjie
public func swap(val: UInt8): UInt8
```

功能：交换操作，采用默认内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 写入原子类型的值。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 写入前的值。

### func swap(UInt8, MemoryOrder) <sup>(deprecated)</sup>

```cangjie
public func swap(val: UInt8, memoryOrder!: MemoryOrder): UInt8
```

功能：交换操作，采用参数 `memoryOrder` 指定的内存排序方式，将参数 `val` 指定的值写入原子类型，并返回写入前的值。

> **注意：**
>
> 未来版本即将废弃，使用 [swap(UInt8)](#func-swapuint8) 替代。

参数：

- val: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 写入原子类型的值。
- memoryOrder!: [MemoryOrder <sup>(deprecated)</sup>](sync_package_enums.md#enum-memoryorder-deprecated) - 当前操作的内存排序方式。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 写入前的值。

## class Barrier

```cangjie
public class Barrier {
    public init(count: Int64)
}
```

功能：提供协调多个线程一起执行到某一个程序点的功能。

率先达到程序点的线程将进入阻塞状态，当所有线程都达到程序点后，才一起继续执行。

### init(Int64)

```cangjie
public init(count: Int64)
```

功能：创建 [Barrier](sync_package_classes.md#class-barrier) 对象。

参数：

- count: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 表示需要协调的线程数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数 [count](../../collection/collection_package_api/collection_package_function.md#func-counttiterablet) 为负数。

### func wait(Duration)

```cangjie
public func wait(timeout!: Duration = Duration.Max): Unit
```

功能：线程进入 [Barrier](sync_package_classes.md#class-barrier) 等待点。

如果 [Barrier](sync_package_classes.md#class-barrier) 对象所有调用 `wait` 的次数（即进入等待点的线程数）等于初始值，那么唤醒所有等待的线程；如果调用 `wait` 方法次数仍小于初始值，那么当前线程进入阻塞状态直到被唤醒或者等待时间超过 `timeout`；如果调用 `wait` 次数已大于初始值，那么线程继续执行。

参数：

- timeout!: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 阻塞时等待的最大时长，其默认值为 [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)。

## class Monitor <sup>(deprecated)</sup>

```cangjie
public class Monitor <: ReentrantMutex {
    public init()
}
```

功能：提供使线程阻塞并等待来自另一个线程的信号以恢复执行的功能。

这是一种利用共享变量进行线程同步的机制，当一些线程因等待共享变量的某个条件成立而挂起时，另一些线程改变共享的变量，使条件成立，
然后执行唤醒操作。这使得挂起的线程被唤醒后可以继续执行。

> **注意：**
>
> 未来版本即将废弃，使用 [Condition](./sync_package_interfaces.md#interface-condition) 替代。

父类型：

- [ReentrantMutex <sup>(deprecated)</sup>](#class-reentrantmutex-deprecated)

### init()

```cangjie
public init()
```

功能：通过默认构造函数创建 [Monitor <sup>(deprecated)</sup>](sync_package_classes.md#class-monitor-deprecated)。

### func notify()

```cangjie
public func notify(): Unit
```

功能：唤醒一个等待在该 `Montior` 上的线程。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

### func notifyAll()

```cangjie
public func notifyAll(): Unit
```

功能：唤醒所有等待在该 `Montior` 上的线程。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

### func wait(Duration)

```cangjie
public func wait(timeout!: Duration = Duration.Max): Bool
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

## class MultiConditionMonitor <sup>(deprecated)</sup>

```cangjie
public class MultiConditionMonitor <: ReentrantMutex {
    public init()
}
```

功能：提供对同一个互斥锁绑定多个条件变量的功能。

> **注意：**
>
> - 未来版本即将废弃，使用 [Mutex](#class-mutex) 替代。
> - 该类应仅当在 [Monitor <sup>(deprecated)</sup>](sync_package_classes.md#class-monitor-deprecated) 类不足以实现高级并发算法时被使用。
> - 初始化时，[MultiConditionMonitor <sup>(deprecated)</sup>](sync_package_classes.md#class-multiconditionmonitor-deprecated) 没有与之相关的条件变量。
> - 每次调用 `newCondition` 将创建一个新的等待队列并与当前对象关联，并返回[ConditionID <sup>(deprecated)</sup>](sync_package_structs.md#struct-conditionid-deprecated)类型实例作为唯一标识符。

父类型：

- [ReentrantMutex <sup>(deprecated)</sup>](#class-reentrantmutex-deprecated)

### init()

```cangjie
public init()
```

功能：通过默认构造函数创建 [MultiConditionMonitor <sup>(deprecated)</sup>](sync_package_classes.md#class-multiconditionmonitor-deprecated)。

### func newCondition()

```cangjie
public func newCondition(): ConditionID
```

功能：创建一个与该 [Monitor <sup>(deprecated)</sup>](sync_package_classes.md#class-monitor-deprecated) 相关的 [ConditionID <sup>(deprecated)</sup>](sync_package_structs.md#struct-conditionid-deprecated)，可能被用来实现 “单互斥体多等待队列” 的并发原语。

返回值：

- [ConditionID](sync_package_structs.md#struct-conditionid-deprecated) - 新的 [ConditionID <sup>(deprecated)</sup>](sync_package_structs.md#struct-conditionid-deprecated)。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

### func notify(ConditionID)

```cangjie
public func notify(condID: ConditionID): Unit
```

功能：唤醒等待在所指定的条件变量的线程（如果有）。

参数：

- condID: [ConditionID](sync_package_structs.md#struct-conditionid-deprecated) - 条件变量。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，或 `condID` 不是由该 [MultiConditionMonitor <sup>(deprecated)</sup>](sync_package_classes.md#class-multiconditionmonitor-deprecated) 实例通过 `newCondition` 函数创建时，抛出异常。

### func notifyAll(ConditionID)

```cangjie
public func notifyAll(condID: ConditionID): Unit
```

功能：唤醒所有等待在所指定的条件变量的线程（如果有）。

参数：

- condID: [ConditionID](sync_package_structs.md#struct-conditionid-deprecated) - 条件变量。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，或 `condID` 不是由该 [MultiConditionMonitor <sup>(deprecated)</sup>](sync_package_classes.md#class-multiconditionmonitor-deprecated) 实例通过 `newCondition` 函数创建时，抛出异常。

### func wait(ConditionID, Duration)

```cangjie
public func wait(condID: ConditionID, timeout!: Duration = Duration.Max): Bool
```

功能：当前线程挂起，直到对应的 `notify` 函数被调用。

> **说明：**
>
> 线程在进入等待时会释放对应的互斥锁，被唤醒后再次持有互斥锁。

参数：

- condID: [ConditionID](sync_package_structs.md#struct-conditionid-deprecated) - 条件变量。
- timeout!: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 挂起时间，其默认值为 [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该 [Monitor <sup>(deprecated)</sup>](sync_package_classes.md#class-monitor-deprecated) 指定的条件变量被其他线程唤醒，返回 `true`；如果超时，则返回 `false`。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，或者挂起时间超过 `timeout` 或 `condID` 不是由该 [MultiConditionMonitor <sup>(deprecated)</sup>](sync_package_classes.md#class-multiconditionmonitor-deprecated) 实例通过 `newCondition` 函数创建时，抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 `timeout` 小于等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero)，抛出异常。

## class Mutex

```cangjie
public class Mutex <: UniqueLock {
    public init()
}
```

功能：提供可重入互斥锁相关功能。

可重入互斥锁的作用是对临界区加以保护，使得任意时刻最多只有一个线程能够执行临界区的代码。
当一个线程试图获取一个已被其他线程持有的锁时，该线程会被阻塞，直到锁被释放，该线程才会被唤醒，可重入是指线程获取该锁后可再次获得该锁。

> **注意：**
>
> - 在访问共享数据之前，必须尝试获取锁。
> - 处理完共享数据后，必须进行解锁，以便其他线程可以获得锁。

父类型：

- [UniqueLock](./sync_package_interfaces.md#interface-uniquelock)

### init()

```cangjie
public init()
```

功能：创建可重入互斥锁。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 当出现系统错误时，抛出异常。

### func condition()

```cangjie
public func condition(): Condition
```

功能：创建一个与该 [Mutex](#class-mutex) 相关的 [Condition](./sync_package_interfaces.md#interface-condition)。

可能被用来实现 “单 Lock 多等待队列” 的并发原语。

返回值：

- [Condition](./sync_package_interfaces.md#interface-condition) - 创建的与该 [Mutex](#class-mutex) 相关的 [Condition](./sync_package_interfaces.md#interface-condition) 实例。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

### func lock()

```cangjie
public func lock(): Unit
```

功能：锁定互斥体，如果互斥体已被锁定，则阻塞。

### func tryLock()

```cangjie
public func tryLock(): Bool
```

功能：尝试锁定互斥体。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果互斥体已被锁定，则返回 `false`；反之，则锁定互斥体并返回 `true`。

### func unlock()

```cangjie
public func unlock(): Unit
```

功能：解锁互斥体。

如果互斥体被重复加锁了 N 次，那么需要调用 N 次该函数来完全解锁，一旦互斥体被完全解锁，如果有其他线程阻塞在此锁上，那么唤醒它们中的一个。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

## class ReadWriteLock

```cangjie
public class ReadWriteLock {
    public init(fair!: Bool = false)
}
```

功能：提供可重入读写锁相关功能。

它和普通互斥锁的差异在于：读写锁同时携带两个互斥锁，分别为“读锁”以及“写锁”，并且它允许多个线程同时持有读锁。

读写锁的特殊性质说明：

- 写互斥性：只有唯一的线程能够持有写锁。当一个线程持有写锁，而其他线程再次获取锁（读锁或是写锁）时将被阻塞。
- 读并发性：允许多个线程同时持有读锁。当一个线程持有读锁，其他线程仍然可以获取读锁。但其他线程获取写锁时将被阻塞。
- 可重入性：一个线程可以重复获取锁。
    - 当线程已持有写锁时，它可以继续获取写锁或者读锁。只有当锁释放操作和获取操作一一对应时，锁才被完全释放。
    - 当线程已持有读锁时，它可以继续获取读锁。当锁释放操作和获取操作一一对应时，锁才被完全释放。注意，不允许在持有读锁的情况下获取写锁，这将抛出异常。
- 锁降级：一个线程在经历“持有写锁--持有读锁--释放写锁”后，它持有的是读锁而不再是写锁。
- 读写公平性：读写锁支持两种不同的模式，分别为“公平”及“非公平”模式。
    - 在非公平模式下，读写锁对线程获取锁的顺序不做任何保证。
    - 在公平模式下，当线程获取读锁时（当前线程未持有读锁），如果写锁已被获取或是存在线程等待写锁，那么当前线程无法获取读锁并进入等待。
    - 在公平模式下，写锁释放会优先唤醒所有读线程、读锁释放会优先唤醒一个等待写锁的线程。当存在多个线程等待写锁，它们之间被唤醒的先后顺序并不做保证。

### prop readLock

```cangjie
public prop readLock: Lock
```

功能：获取读锁。

类型：[Lock](./sync_package_interfaces.md#interface-lock)

### prop writeLock

```cangjie
public prop writeLock: UniqueLock
```

功能：获取写锁。

类型：[UniqueLock](./sync_package_interfaces.md#interface-uniquelock)

### init(Bool)

```cangjie
public init(fair!: Bool = false)
```

功能：构造读写锁。

参数：

- fair!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 读写锁是否为公平模式，默认值为 `false`，即构造 “非公平” 的读写锁。

### func isFair()

```cangjie
public func isFair(): Bool
```

功能：获取读写锁是否为 “公平” 模式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - `true` 表示 “公平” 模式，否则表示 “非公平” 模式。

## class ReentrantMutex <sup>(deprecated)</sup>

```cangjie
public open class ReentrantMutex <: Lock {
    public init()
}
```

功能：提供可重入锁相关功能。

可重入互斥锁的作用是对临界区加以保护，使得任意时刻最多只有一个线程能够执行临界区的代码。
当一个线程试图获取一个已被其他线程持有的锁时，该线程会被阻塞，直到锁被释放，该线程才会被唤醒，可重入是指线程获取该锁后可再次获得该锁。

> **注意：**
>
> - 未来版本即将废弃，使用 [Mutex](#class-mutex) 替代。
> - [ReentrantMutex <sup>(deprecated)</sup>](sync_package_classes.md#class-reentrantmutex-deprecated) 是内置的互斥锁，开发者需要保证不继承它。
> - 在访问共享数据之前，必须尝试获取锁。
> - 处理完共享数据后，必须进行解锁，以便其他线程可以获得锁。

父类型：

- [Lock](sync_package_interfaces.md#interface-lock)

### init()

```cangjie
public init()
```

功能：创建可重入互斥锁。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 当出现系统错误时，抛出异常。

### func lock()

```cangjie
public open func lock(): Unit
```

功能：锁定互斥体，如果互斥体已被锁定，则阻塞。

### func tryLock()

```cangjie
public open func tryLock(): Bool
```

功能：尝试锁定互斥体。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果互斥体已被锁定，则返回 `false`；反之，则锁定互斥体并返回 `true`。

### func unlock()

```cangjie
public open func unlock(): Unit
```

功能：解锁互斥体。

如果互斥体被重复加锁了 N 次，那么需要调用 N 次该函数来完全解锁，一旦互斥体被完全解锁，如果有其他线程阻塞在此锁上，那么唤醒它们中的一个。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 如果当前线程没有持有该互斥体，抛出异常。

## class ReentrantReadMutex <sup>(deprecated)</sup>

```cangjie
public class ReentrantReadMutex <: ReentrantMutex {}
```

功能：提供可重入读写锁中的读锁类型。

> **注意：**
>
> 未来版本即将废弃，使用 [Lock](./sync_package_interfaces.md#interface-lock) 替代。

父类型：

- [ReentrantMutex <sup>(deprecated)</sup>](#class-reentrantmutex-deprecated)

### func lock()

```cangjie
public func lock(): Unit
```

功能：获取读锁。

> **注意：**
>
> - 在公平模式下，如果没有其他线程持有或等待写锁，或是当前线程已持有读锁，则立即持有读锁；否则，当前线程进入等待状态。
> - 在非公平模式下，如果没有其他线程持有或等待写锁，则立即持有读锁；如果有其他线程持有写锁，当前线程进入等待状态；否则，线程是否能立即持有读锁不做保证。
> - 多个线程可以同时持有读锁并且一个线程可以重复多次持有读锁；如果一个线程持有写锁，那么它仍可以持有读锁。

### func tryLock()

```cangjie
public func tryLock(): Bool
```

功能：尝试获取读锁。该方法获取读锁时并不遵循公平模式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 若成功获取读锁，返回 `true`；若未能获取读锁，返回 `false`。

### func unlock()

```cangjie
public func unlock(): Unit
```

功能：释放读锁。如果一个线程多次持有读锁，那么仅当释放操作和获取操作数量相同时才释放读锁；如果读锁被释放并且存在线程等待写锁，那么唤醒其中一个线程。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 当前线程未持有读锁，那么将抛出异常。

## class ReentrantReadWriteMutex <sup>(deprecated)</sup>

```cangjie
public class ReentrantReadWriteMutex {
    public init(mode!: ReadWriteMutexMode = ReadWriteMutexMode.Unfair)
}
```

功能：提供可重入读写锁相关功能。

它和普通互斥锁的差异在于：读写锁同时携带两个互斥锁，分别为“读锁”以及“写锁”，并且它允许多个线程同时持有读锁。

> **注意：**
>
> 未来版本即将废弃，使用 [ReadWriteLock](#class-readwritelock) 替代。

读写锁的特殊性质说明：

- 写互斥性：只有唯一的线程能够持有写锁。当一个线程持有写锁，而其他线程再次获取锁（读锁或是写锁）时将被阻塞。
- 读并发性：允许多个线程同时持有读锁。当一个线程持有读锁，其他线程仍然可以获取读锁。但其他线程获取写锁时将被阻塞。
- 可重入性：一个线程可以重复获取锁。
    - 当线程已持有写锁时，它可以继续获取写锁或者读锁。只有当锁释放操作和获取操作一一对应时，锁才被完全释放。
    - 当线程已持有读锁时，它可以继续获取读锁。当锁释放操作和获取操作一一对应时，锁才被完全释放。注意，不允许在持有读锁的情况下获取写锁，这将抛出异常。
- 锁降级：一个线程在经历“持有写锁--持有读锁--释放写锁”后，它持有的是读锁而不再是写锁。
- 读写公平性：读写锁支持两种不同的模式，分别为“公平”及“非公平”模式。
    - 在非公平模式下，读写锁对线程获取锁的顺序不做任何保证。
    - 在公平模式下，当线程获取读锁时（当前线程未持有读锁），如果写锁已被获取或是存在线程等待写锁，那么当前线程无法获取读锁并进入等待。
    - 在公平模式下，写锁释放会优先唤醒所有读线程、读锁释放会优先唤醒一个等待写锁的线程。当存在多个线程等待写锁，它们之间被唤醒的先后顺序并不做保证。

### prop readMutex

```cangjie
public prop readMutex: ReentrantReadMutex
```

功能：获取读锁。

类型：[ReentrantReadMutex <sup>(deprecated)</sup>](sync_package_classes.md#class-reentrantreadmutex-deprecated)

### prop writeMutex

```cangjie
public prop writeMutex: ReentrantWriteMutex
```

功能：获取写锁。

类型：[ReentrantWriteMutex <sup>(deprecated)</sup>](sync_package_classes.md#class-reentrantwritemutex-deprecated)

### init(ReadWriteMutexMode)

```cangjie
public init(mode!: ReadWriteMutexMode = ReadWriteMutexMode.Unfair)
```

功能：构造读写锁。

参数：

- mode!: [ReadWriteMutexMode <sup>(deprecated)</sup>](sync_package_enums.md#enum-readwritemutexmode-deprecated) - 读写锁模式，默认值为 `Unfair`，即构造“非公平”的读写锁。

## class ReentrantWriteMutex <sup>(deprecated)</sup>

```cangjie
public class ReentrantWriteMutex <: ReentrantMutex {}
```

功能：提供可重入读写锁中的写锁类型。

> **注意：**
>
> 未来版本即将废弃，使用 [UniqueLock](./sync_package_interfaces.md#interface-uniquelock) 替代。

父类型：

- [ReentrantMutex <sup>(deprecated)</sup>](#class-reentrantmutex-deprecated)

### func lock()

```cangjie
public func lock(): Unit
```

功能：获取写锁。只允许唯一线程能够持有写锁，且该线程能多次重复持有写锁。如果存在其他线程持有写锁或是读锁，那么当前线程进入等待状态。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 当前线程已持有读锁。

### func tryLock()

```cangjie
public func tryLock(): Bool
```

功能：尝试获取写锁。该方法获取读锁时并不遵循公平模式。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 若成功获取写锁，返回 `true`；若未能获取写锁，返回 `false`。

### func unlock()

```cangjie
public func unlock(): Unit
```

功能：释放写锁。

> **注意：**
>
> - 如果一个线程多次持有读锁，那么仅当释放操作和获取操作数量相同时才释放读锁；如果读锁被释放并且存在线程等待写锁，那么唤醒其中一个线程。
> - 在公平模式下，如果写锁被释放并且存在线程等待读锁，那么优先唤醒这些等待线程；如果没有线程等待读锁，但存在线程等待写锁，那么唤醒其中一个线程。
> - 在非公平模式下，如果写锁被释放，优先唤醒等待写锁的线程还是等待读锁的线程不做保证，交由具体实现决定。

异常：

- [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) - 当前线程未持有写锁。

## class Semaphore

```cangjie
public class Semaphore {
    public init(count: Int64)
}
```

功能：提供信号量相关功能。

[Semaphore](sync_package_classes.md#class-semaphore) 可以被视为携带计数器的 [Monitor <sup>(deprecated)</sup>](sync_package_classes.md#class-monitor-deprecated)，常用于控制并发访问共享资源的线程数量。

### prop count

```cangjie
public prop count: Int64
```

功能：返回当前内部计数器的值。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init(Int64)

```cangjie
public init(count: Int64)
```

功能：创建一个 [Semaphore](sync_package_classes.md#class-semaphore) 对象并初始化内部计数器的值。

参数：

- [count](../../collection/collection_package_api/collection_package_function.md#func-counttiterablet): [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 计数器初始值, 取值范围 [0, [Int64](../../core/core_package_api/core_package_intrinsics.md#int64).Max]。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数 [count](../../collection/collection_package_api/collection_package_function.md#func-counttiterablet) 为负数时抛出异常。

### func acquire(Int64)

```cangjie
public func acquire(amount!: Int64 = 1): Unit
```

功能：向 [Semaphore](sync_package_classes.md#class-semaphore) 对象获取指定值。

如果当前计数器小于要求的数值，那么当前线程将被阻塞，直到获取满足数量的值后才被唤醒。

参数：

- amount!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 向对象内部计数器中获取的数值，默认值为 1。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数 `amount` 为负数，或大于初始值。

### func release(Int64)

```cangjie
public func release(amount!: Int64 = 1): Unit
```

功能：向 [Semaphore](sync_package_classes.md#class-semaphore) 对象释放指定值。

如果内部计数器在累加释放值后能够满足当前阻塞在 [Semaphore](sync_package_classes.md#class-semaphore) 对象的线程，那么将得到满足的线程唤醒；内部计数器的值不会大于初始值，即如果计数器的值在累加后大于初始值，那么仍被设置为初始值。所有在调用 `release` 之前的操作都先发生于调用 `acquire/tryAcquire` 之后的操作。

参数：

- amount!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 向对象内部计数器中释放的数值，默认值为 1。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数 `amount` 为负数，或大于初始值。

### func tryAcquire(Int64)

```cangjie
public func tryAcquire(amount!: Int64 = 1): Bool
```

功能：尝试向 [Semaphore](sync_package_classes.md#class-semaphore) 对象获取指定值。

该方法不会阻塞线程。如果有多个线程并发执行获取操作，则无法保证线程间的获取顺序。

参数：

- amount!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 向对象内部计数器中获取的数值，默认值为 1。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果当前计数器小于要求的数值，则获取失败并返回 `false`；成功获取值时返回 `true`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数 `amount` 为负数，或大于初始值。

## class SyncCounter

```cangjie
public class SyncCounter {
    public init(count: Int64)
}
```

功能：提供倒数计数器功能。

线程可以等待计数器变为零。

### prop count

```cangjie
public prop count: Int64
```

功能：获取计数器的当前值。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init(Int64)

```cangjie
public init(count: Int64)
```

功能：创建倒数计数器。

参数：

- [count](../../collection/collection_package_api/collection_package_function.md#func-counttiterablet): [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 倒数计数器的初始值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果参数 [count](../../collection/collection_package_api/collection_package_function.md#func-counttiterablet) 为负数。

### func dec()

```cangjie
public func dec(): Unit
```

功能：计数器减一。

如果计数器变为零，那么唤醒所有等待的线程；如果计数器已经为零，那么数值保持不变。

### func waitUntilZero(Duration)

```cangjie
public func waitUntilZero(timeout!: Duration = Duration.Max): Unit
```

功能：当前线程等待直到计数器变为零，或等待时间超过 `timeout`。

参数：

- timeout!: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 阻塞时等待的最大时长，其默认值为 [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)。

## class Timer

```cangjie
public class Timer <: Equatable<Timer> & Hashable {}
```

功能：提供定时器功能。

用于在指定时间点或指定时间间隔后，执行指定任务一次或多次。

> **注意：**
>
> - [Timer](sync_package_classes.md#class-timer) 隐式包含了 `spawn` 操作，即，每个 [Timer](sync_package_classes.md#class-timer) 会创建一个线程用于执行该 [Timer](sync_package_classes.md#class-timer) 关联的 Task。
> - 每个 [Timer](sync_package_classes.md#class-timer) 只能在初始化时绑定一个 Task，初始化完成后，无法重置关联的 Task。
> - 只有关联 Task 执行完毕，或 使用 `cancel` 接口主动取消 [Timer](sync_package_classes.md#class-timer)，[Timer](sync_package_classes.md#class-timer) 的生命周期才会结束，之后才能被 [GC](../../runtime/runtime_package_api/runtime_package_funcs.md#func-gcbool) 回收。换句话说，在 [Timer](sync_package_classes.md#class-timer) 关联的 Task 执行完毕或 [Timer](sync_package_classes.md#class-timer) 被主动取消前，[Timer](sync_package_classes.md#class-timer) 实例均不会被 [GC](../../runtime/runtime_package_api/runtime_package_funcs.md#func-gcbool) 回收，从而确保关联 Task 可以被正常执行。
> - 系统繁忙时，Task 的触发时间可能会被影响。[Timer](sync_package_classes.md#class-timer) 不保证 Task 的触发时间一定准时。[Timer](sync_package_classes.md#class-timer) 保证 Task 的触发时间小于等于当前时间。
> - [Timer](sync_package_classes.md#class-timer) 不会主动捕获关联 Task 抛出的异常。只要 Task 有未被捕获的异常，[Timer](sync_package_classes.md#class-timer) 就会失效。
> - [Timer](sync_package_classes.md#class-timer) 通常按使用方式分为 一次性任务定时器 和 重复性任务定时器两种，一次性任务定时器 Task 只会执行一次，重复性任务定时器 Task 会按指定周期执行, 直到使用 `cancel` 接口主动取消 或者 达到 [Timer](sync_package_classes.md#class-timer) 创建时指定的结束条件。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[Timer](#class-timer)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)

### static func after(Duration, ()->Option\<Duration>)

```cangjie
public static func after(delay: Duration, task: () -> Option<Duration>): Timer
```

功能：初始化一个 [Timer](sync_package_classes.md#class-timer)，关联的 Task 被调度执行的次数取决于它的返回值。如果定时器第一次触发的时间点小于当前时间，关联的 Task 会立刻被调度执行。如果关联 Task 的返回值为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont).None，该 [Timer](sync_package_classes.md#class-timer) 将会失效，并停止调度关联 Task。如果关联 Task 的返回值为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont).Some(v) 且 `v` 大于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero)，下次运行前的最小时间间隔将被设置为 v。否则，关联 Task 会立刻再次被调度执行。

参数：

- delay: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 从现在开始到关联 Task 首次被调度执行的时间间隔
- task: () ->[Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)> - 该 [Timer](sync_package_classes.md#class-timer) 调度执行的 Task

返回值：

- [Timer](sync_package_classes.md#class-timer) - 一个 [Timer](sync_package_classes.md#class-timer) 实例

### static func once(Duration, ()->Unit)

```cangjie
public static func once(delay: Duration, task: ()->Unit): Timer
```

功能：设置并启动一次性定时任务，返回控制这个任务的 [Timer](sync_package_classes.md#class-timer) 对象实例。

参数：

- delay: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 从现在开始到 Task 被执行的时间间隔。取值范围 [[Duration.Min](../../core/core_package_api/core_package_structs.md#static-const-min), [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)]，小于或等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero) 时 Task 将立即被执行。
- task: ()->Unit - 待定时执行的任务。

返回值：

- [Timer](sync_package_classes.md#class-timer) - 生成的对象实例。

示例：

<!-- run -->

```cangjie
import std.time.MonoTime
import std.sync.Timer

main() {
    let start = MonoTime.now()
    Timer.once(Duration.second, {=>
        println("Tick at: ${MonoTime.now() - start}")
    })

    sleep(Duration.second * 2)
    0
}
```

可能的运行结果：

```text
Tick at: 1s2ms74us551ns
```

### static func repeat(Duration, Duration, ()->Unit, CatchupStyle)

```cangjie
public static func repeat(delay: Duration, interval: Duration, task: ()->Unit, style!: CatchupStyle = Burst): Timer
```

功能：设置并启动重复性定时任务，返回控制这个任务的 [Timer](sync_package_classes.md#class-timer) 对象实例。

参数：

- delay: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 从现在开始到 Task 被执行的时间间隔。取值范围 [[Duration.Min](../../core/core_package_api/core_package_structs.md#static-const-min), [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)]，小于或等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero) 时 Task 将立即被执行。
- interval: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 两次 Task 之间的时间间隔。取值范围 ([Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero), [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)]。
- task: ()->Unit - 待定时执行的任务。
- style!: [CatchupStyle](./sync_package_enums.md#enum-catchupstyle) - 追平策略，默认 Burst。当 Task 执行时间过长时，后续任务执行时间点可能发生延迟，不同的追平策略适用于不同的场景，详见 [CatchupStyle](sync_package_enums.md#enum-catchupstyle) 说明。

返回值：

- [Timer](sync_package_classes.md#class-timer) - 生成的对象实例。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 `interval` 小于等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero) 时，抛出异常。

示例:

<!-- run -->

```cangjie
import std.sync.Timer
import std.time.MonoTime

main() {
    let start = MonoTime.now()
    let timer = Timer.repeat(Duration.second, Duration.second, {=>
        println("Tick at: ${MonoTime.now() - start}")
    })

    sleep(Duration.second * 5)
    timer.cancel()
    0
}
```

可能的运行结果：

```text
Tick at: 1s2ms72us188ns
Tick at: 2s4ms185us160ns
Tick at: 3s6ms275us464ns
Tick at: 4s8ms18us399ns
```

### static func repeatDuring(Duration, Duration, Duration, ()->Unit, CatchupStyle)

```cangjie
public static func repeatDuring(period: Duration, delay: Duration, interval: Duration, task: () -> Unit, style!: CatchupStyle = Burst): Timer
```

功能：设置并启动重复性定时任务，指定重复周期的最大持续时间，返回控制这个任务的 [Timer](sync_package_classes.md#class-timer) 对象实例。

参数：

- period: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 重复周期的最大持续时间，从 delay 之后开始计时。取值范围 ([Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero), [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)]。
- delay: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 从现在开始到 Task 被执行的时间间隔。取值范围 [Duration.Min, [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)]，小于或等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero)时 Task 将立即被执行。
- interval: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 两次 Task 之间的时间间隔。取值范围 ([Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero), [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)]。
- task: ()->Unit - 待定时执行的任务。
- style!: [CatchupStyle](./sync_package_enums.md#enum-catchupstyle) - 追平策略，默认 Burst。当 Task 执行时间过长时，后续任务执行时间点可能发生延迟，不同的追平策略适用于不同的场景，详见 [CatchupStyle](sync_package_enums.md#enum-catchupstyle) 说明。

返回值：

- [Timer](sync_package_classes.md#class-timer) - 生成的对象实例。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception): 当 period 小于等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero) 或 interval 小于等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero) 时，抛出异常。

示例：

<!-- run -->

```cangjie
import std.sync.Timer
import std.time.MonoTime

main() {
    let start = MonoTime.now()
    Timer.repeatDuring(Duration.second * 5, Duration.second, Duration.second, {=>
        println("Tick at: ${MonoTime.now() - start}")
    })

    sleep(Duration.second * 7)
    0
}
```

可能的运行结果：

```text
Tick at: 1s2ms372us626ns
Tick at: 2s4ms714us879ns
Tick at: 3s6ms769us623ns
Tick at: 4s8ms780us235ns
Tick at: 5s660us104ns
Tick at: 6s3ms257us508ns
```

### static func repeatTimes(Int64, Duration, Duration, ()->Unit, CatchupStyle)

```cangjie
public static func repeatTimes(count: Int64, delay: Duration, interval: Duration, task: () -> Unit, style!: CatchupStyle = Burst): Timer
```

功能：设置并启动重复性定时任务，指定 Task 最大执行次数，返回控制这个任务的 [Timer](sync_package_classes.md#class-timer) 对象实例。

参数：

- count: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - Task 最大执行次数。取值范围 (0, [Int64](../../core/core_package_api/core_package_intrinsics.md#int64).Max]。
- delay: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 从现在开始到 Task 被执行的时间间隔。取值范围 [Duration.Min, [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)]，小于或等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero) 时 Task 将立即被执行。
- interval: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 两次 Task 之间的时间间隔。取值范围 ([Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero), [Duration.Max](../../core/core_package_api/core_package_structs.md#static-const-max)]。
- task: ()->Unit - 待定时执行的任务。
- style!: [CatchupStyle](./sync_package_enums.md#enum-catchupstyle) - 追平策略，默认 Burst。当 Task 执行时间过长时，后续任务执行时间点可能发生延迟，不同的追平策略适用于不同的场景，详见 [CatchupStyle](sync_package_enums.md#enum-catchupstyle) 说明。

返回值：

- [Timer](sync_package_classes.md#class-timer) - 生成的对象实例。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 [count](../../collection/collection_package_api/collection_package_function.md#func-counttiterablet) <= 0 或 interval 小于等于 [Duration.Zero](../../core/core_package_api/core_package_structs.md#static-const-zero) 时，抛出异常。

示例：

<!-- run -->

```cangjie
import std.sync.Timer
import std.time.MonoTime

main() {
    let start = MonoTime.now()
    Timer.repeatTimes(3, Duration.second, Duration.second, {=>
        println("Tick at: ${MonoTime.now() - start}")
    })

    sleep(Duration.second * 4)
    0
}
```

可能的运行结果：

```text
Tick at: 1s2ms855us251ns
Tick at: 2s5ms390us18ns
Tick at: 3s7ms935us552ns
```

### func cancel()

```cangjie
public func cancel(): Unit
```

功能：取消该 [Timer](sync_package_classes.md#class-timer)，关联 Task 将不再被调度执行。

如果调用该函数时关联 Task 正在执行，不会打断当前运行。该函数不会阻塞当前线程。调用该函数多次等同于只调用一次。

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取 [Timer](sync_package_classes.md#class-timer) 对象的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 对象的哈希值。

### operator func !=(Timer)

```cangjie
public operator func !=(rhs: Timer): Bool
```

功能：判断当前 [Timer](sync_package_classes.md#class-timer) 与入参 `rhs` 指定的 [Timer](sync_package_classes.md#class-timer) 是否不是同一个实例。

参数：

- rhs: [Timer](#class-timer) - 待比较的另一个 [Timer](#class-timer) 对象。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 若两个 [Timer](sync_package_classes.md#class-timer) 不是同一个实例，则返回 `true`，否则返回 `false`。

### operator func ==(Timer)

```cangjie
public operator func ==(rhs: Timer): Bool
```

功能：判断当前 [Timer](sync_package_classes.md#class-timer) 与入参 `rhs` 指定的 [Timer](sync_package_classes.md#class-timer) 是否是同一个实例。

参数：

- rhs: [Timer](#class-timer) - 待比较的另一个 [Timer](#class-timer) 对象。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 若两个 [Timer](sync_package_classes.md#class-timer) 是同一个实例，则返回 `true`，否则返回 `false`。
