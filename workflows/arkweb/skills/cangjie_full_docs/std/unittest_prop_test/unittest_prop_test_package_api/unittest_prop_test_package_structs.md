# 结构体

## struct Function0Wrapper\<R>

```cangjie
public struct Function0Wrapper<R> {
    public Function0Wrapper(public let function: () -> R)
}
```

功能：将闭包封装为结构体。

### Function0Wrapper(() -> R)

```cangjie
public Function0Wrapper(public let function: () -> R)
```

功能：Function0Wrapper 构造器。

参数：

- function: () -> R - 被封装的闭包。

### let function

```cangjie
public let function: () -> R
```

功能：函数对象自身。

类型：()->R

### operator func ()()

```cangjie
public operator func () (): R
```

功能：调用操作符函数。将闭包转换为结构体的调用操作符函数。

返回值：

- R - 同闭包的返回值。

### extend\<R> Function0Wrapper\<R> <: Arbitrary\<Function0Wrapper\<R>> where R <: Arbitrary\<R>

```cangjie
extend<R> Function0Wrapper<R> <: Arbitrary<Function0Wrapper<R>> where R <: Arbitrary<R>
```

功能：为 [Function0Wrapper](#struct-function0wrapperr) 扩展 [Arbitrary](./unittest_prop_test_package_interfaces.md#interface-arbitraryt) 实现。

父类型：

- [Arbitrary](unittest_prop_test_package_interfaces.md#interface-arbitraryt)\<[Function0Wrapper](#struct-function0wrapperr)\<R>>

#### static func arbitrary(RandomSource)

```cangjie
public static func arbitrary(random: RandomSource): Generator<Function0Wrapper<R>>
```

功能：获取生成 [Function0Wrapper](#struct-function0wrapperr)\<R> 类型随机值生成器。

返回值：

- [Generator](../unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-generatort)\<[Function0Wrapper](../unittest_prop_test_package_api/unittest_prop_test_package_structs.md#struct-function0wrapperr)\<R>> - 生成器。

## struct KeyRandom

```cangjie
public struct KeyRandom <: KeyFor<RandomSource> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 创建键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)<[RandomSource](./unittest_prop_test_package_interfaces.md#interface-randomsource)>

### prop random

```cangjie
public static prop random: KeyRandom
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct TupleWrapper2\<T0, T1>

```cangjie
public struct TupleWrapper2<T0, T1> {
    public TupleWrapper2(public let tuple: (T0, T1))
}
```

功能：将闭包封装为结构体。闭包带两个参数。

### TupleWrapper2((T0, T1))

```cangjie
public TupleWrapper2(public let tuple: (T0, T1))
```

功能：TupleWrapper2 构造器。

参数：

- tuple: (T0, T1) - 闭包的两个入参。

### let tuple

```cangjie
public let tuple: (T0, T1)
```

功能：元组自身。

类型：(T0, T1)

### func apply\<R>((T0, T1) -> R)

```cangjie
public func apply<R>(f: (T0, T1) -> R): R
```

功能：执行闭包函数。

参数：

- f: (T0, T1) -> R - 待执行的闭包。

返回值：

- R - 闭包的执行结果。

### extend\<T0, T1> TupleWrapper2\<T0, T1> <: ToString

```cangjie
extend<T0, T1> TupleWrapper2<T0, T1> <: ToString
```

功能：为 [TupleWrapper2](#struct-tuplewrapper2t0-t1) 扩展 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 实现。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

#### func toString()

```cangjie
public func toString()
```

功能：[TupleWrapper2](#struct-tuplewrapper2t0-t1) 的字符串表达。

### extend\<T0, T1> TupleWrapper2\<T0, T1> <: Equatable\<TupleWrapper2\<T0, T1>>

```cangjie
extend<T0, T1> TupleWrapper2<T0, T1> <: Equatable<TupleWrapper2<T0, T1>>
```

功能：为 [TupleWrapper2](#struct-tuplewrapper2t0-t1) 扩展 [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet) 实现。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[TupleWrapper2](#struct-tuplewrapper2t0-t1)\<T0, T1>>

#### operator func ==(TupleWrapper2\<T0, T1>)

```cangjie
public operator func ==(other: TupleWrapper2<T0, T1>): Bool
```

功能：比较两个二元元组。

参数：

- other: [TupleWrapper2](#struct-tuplewrapper2t0-t1)\<T0, T1> - 待比较的元组。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 相等时返回 `true` ，否则返回 `false` 。

#### operator func !=(TupleWrapper2\<T0, T1>)

```cangjie
public operator func !=(other: TupleWrapper2<T0, T1>): Bool
```

功能：比较两个二元元组。

参数：

- other: [TupleWrapper2](#struct-tuplewrapper2t0-t1)\<T0, T1> - 待比较的元组。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 不相等时返回 `true` ，否则返回 `false` 。

### extend\<T0, T1> TupleWrapper2\<T0, T1> <: IndexAccess

```cangjie
extend<T0, T1> TupleWrapper2<T0, T1> <: IndexAccess
```

功能：为 [TupleWrapper2](#struct-tuplewrapper2t0-t1) 扩展 [IndexAccess](./unittest_prop_test_package_interfaces.md#interface-indexaccess) 实现。

父类型：

- [IndexAccess](unittest_prop_test_package_interfaces.md#interface-indexaccess)

#### func getElementAsAny(Int64)

```cangjie
public func getElementAsAny(index: Int64): ?Any
```

功能：按索引获取元组内的值。

参数：

- index: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 索引值。

返回值：

- ?[Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 获取到的元组内的值。索引不合法时返回 `None` 。

### extend\<T0, T1> TupleWrapper2\<T0, T1> <: Arbitrary\<TupleWrapper2\<T0, T1>> where T0 <: Arbitrary\<T0>,T1 <: Arbitrary\<T1>

```cangjie
extend<T0, T1> TupleWrapper2<T0, T1> <: Arbitrary<TupleWrapper2<T0, T1>> where T0 <: Arbitrary<T0>,T1 <: Arbitrary<T1>
```

功能：为 [TupleWrapper2](#struct-tuplewrapper2t0-t1) 扩展 [Arbitrary](./unittest_prop_test_package_interfaces.md#interface-arbitraryt) 实现。

父类型：

- [Arbitrary](unittest_prop_test_package_interfaces.md#interface-arbitraryt)\<[TupleWrapper2](#struct-tuplewrapper2t0-t1)\<T0, T1>>

#### static func arbitrary(RandomSource)

```cangjie
public static func arbitrary(random: RandomSource): Generator<TupleWrapper2<T0, T1>>
```

功能：获取生成 [TupleWrapper2](#struct-tuplewrapper2t0-t1)\<T0, T1> 类型随机值生成器。

返回值：

- [Generator](../unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-generatort)\<[TupleWrapper2](#struct-tuplewrapper2t0-t1)\<T0, T1>> - 生成器。

### extend\<T0, T1> TupleWrapper2\<T0, T1> <: Shrink\<TupleWrapper2\<T0, T1>> where T0 <: Shrink\<T0>,T1 <: Shrink\<T1>

```cangjie
extend<T0, T1> TupleWrapper2<T0, T1> <: Shrink<TupleWrapper2<T0, T1>>
        where T0 <: Shrink<T0>,
              T1 <: Shrink<T1> {
    public func shrink(): Iterable<TupleWrapper2<T0, T1>>
}
```

#### func shrink()

```cangjie
override func shrink(): Iterable<TupleWrapper2<T0, T1>>
```

功能：缩减元组。

返回值：

- [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<TupleWrapper2<T0, T1> - 数据迭代器。

## struct TupleWrapper3\<T0, T1, T2>

```cangjie
public struct TupleWrapper3<T0, T1, T2> {
    public TupleWrapper3(public let tuple: (T0, T1,T2))
}
```

功能：将闭包封装为结构体。闭包带两个参数。

### TupleWrapper3((T0, T1, T2))

```cangjie
public TupleWrapper3(public let tuple: (T0, T1, T2))
```

功能：TupleWrapper3 构造器。

参数：

- tuple: (T0, T1, T2) - 闭包的三个入参。

### let tuple

```cangjie
public let tuple: (T0, T1, T2)
```

功能：元组自身。

类型：(T0, T1, T2)

### func apply\<R>((T0, T1, T2) -> R)

```cangjie
public func apply<R>(f: (T0, T1,T2) -> R): R
```

功能：执行闭包函数。

参数：

- f: (T0, T1,T2) -> R - 待执行的闭包。

返回值：

- R - 闭包的执行结果。

### extend\<T0, T1, T2> TupleWrapper3\<T0, T1, T2> <: ToString

```cangjie
extend<T0, T1, T2> TupleWrapper3<T0, T1, T2> <: ToString
```

功能：为 [TupleWrapper3](#struct-tuplewrapper3t0-t1-t2) 扩展 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 实现。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

#### func toString()

```cangjie
public func toString()
```

功能：[TupleWrapper3](#struct-tuplewrapper3t0-t1-t2) 的字符串表达。

### extend\<T0, T1, T2> TupleWrapper3\<T0, T1, T2> <: Equatable\<TupleWrapper3\<T0, T1, T2>>

```cangjie
extend<T0, T1, T2> TupleWrapper3<T0, T1, T2> <: Equatable<TupleWrapper3<T0, T1, T2>>
```

功能：为 [TupleWrapper3](#struct-tuplewrapper3t0-t1-t2) 扩展 [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet) 实现。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[TupleWrapper3](#struct-tuplewrapper3t0-t1-t2)\<T0, T1, T2>>

#### operator func ==(TupleWrapper3\<T0, T1, T2>)

```cangjie
public operator func ==(other: TupleWrapper3<T0, T1, T2>): Bool
```

功能：比较两个元组。

参数：

- other: [TupleWrapper3](#struct-tuplewrapper3t0-t1-t2)\<T0, T1, T2> - 待比较的元组。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 相等时返回 `true` ，否则返回 `false` 。

#### operator func !=(TupleWrapper3\<T0, T1, T2>)

```cangjie
public operator func !=(other: TupleWrapper3<T0, T1, T2>): Bool
```

功能：比较两个元组。

参数：

- other: [TupleWrapper3](#struct-tuplewrapper3t0-t1-t2)\<T0, T1, T2> - 待比较的元组。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 不相等时返回 `true` ，否则返回 `false` 。

### extend\<T0, T1, T2> TupleWrapper3\<T0, T1, T2> <: IndexAccess

```cangjie
extend<T0, T1, T2> TupleWrapper3<T0, T1, T2> <: IndexAccess
```

功能：为 [TupleWrapper3](#struct-tuplewrapper3t0-t1-t2) 扩展 [IndexAccess](./unittest_prop_test_package_interfaces.md#interface-indexaccess) 实现。

父类型：

- [IndexAccess](unittest_prop_test_package_interfaces.md#interface-indexaccess)

#### func getElementAsAny(Int64)

```cangjie
public func getElementAsAny(index: Int64): ?Any
```

功能：按索引获取元组内的值。

参数：

- index: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 索引值。

返回值：

- ?[Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 获取到的元组内的值。索引不合法时返回 `None` 。

### extend\<T0, T1, T2> TupleWrapper3\<T0, T1, T2> <: Arbitrary\<TupleWrapper3\<T0, T1, T2>>  where T0 <: Arbitrary\<T0>,T1 <: Arbitrary\<T1>,T2 <: Arbitrary\<T2>

```cangjie
extend<T0, T1, T2> TupleWrapper3<T0, T1, T2> <: Arbitrary<TupleWrapper3<T0, T1, T2>>  where T0 <: Arbitrary<T0>,T1 <: Arbitrary<T1>,T2 <: Arbitrary<T2>
```

功能：为 [TupleWrapper3](#struct-tuplewrapper3t0-t1-t2) 扩展 [Arbitrary](./unittest_prop_test_package_interfaces.md#interface-arbitraryt) 实现。

父类型：

- [Arbitrary](unittest_prop_test_package_interfaces.md#interface-arbitraryt)\<[TupleWrapper3](#struct-tuplewrapper3t0-t1-t2)\<T0, T1, T2>>

#### static func arbitrary(RandomSource)

```cangjie
public static func arbitrary(random: RandomSource): Generator<TupleWrapper3<T0, T1, T2>>
```

功能：获取生成 [TupleWrapper3](#struct-tuplewrapper3t0-t1-t2)\<T0, T1, T2> 类型随机值生成器。

返回值：

- [Generator](../unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-generatort)\<[TupleWrapper3](#struct-tuplewrapper3t0-t1-t2)\<T0, T1, T2>> - 生成器。

### extend\<T0, T1, T2> TupleWrapper3\<T0, T1, T2> <: Shrink\<TupleWrapper3\<T0, T1, T2>> where T0 <: Shrink\<T0>,T1 <: Shrink\<T1>,T2 <: Shrink\<T2>

```cangjie
extend<T0, T1, T2> TupleWrapper3<T0, T1, T2> <: Shrink<TupleWrapper3<T0, T1, T2>>
        where T0 <: Shrink<T0>,
              T1 <: Shrink<T1>,
              T2 <: Shrink<T2> {
    public func shrink(): Iterable<TupleWrapper3<T0, T1, T2>>
}
```

### func shrink()

```cangjie
override func shrink(): Iterable<TupleWrapper3<T0, T1, T2>>
```

功能：缩减元组。

返回值：

- [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<TupleWrapper3<T0, T1, T2> -  数据迭代器。

## struct TupleWrapper4\<T0, T1, T2, T3>

```cangjie
public struct TupleWrapper4<T0, T1, T2, T3> {
    public TupleWrapper4(public let tuple: (T0, T1, T2, T3))
}
```

功能：将闭包封装为结构体。闭包带两个参数。

### TupleWrapper4((T0, T1, T2, T3))

```cangjie
public TupleWrapper4(public let tuple: (T0, T1, T2, T3))
```

功能：TupleWrapper4 构造器。

参数：

- tuple: (T0, T1, T2, T3) - 闭包的 4 个入参。

### let tuple

```cangjie
public let tuple: (T0, T1, T2, T3)
```

功能：元组自身。

类型：(T0, T1, T2, T3)

### func apply\<R>((T0, T1, T2, T3) -> R)

```cangjie
public func apply<R>(f: (T0, T1, T2, T3) -> R): R
```

功能：执行闭包函数。

参数：

- f: (T0, T1, T2, T3) -> R - 待执行的闭包。

返回值：

- R - 闭包的执行结果。

### extend\<T0, T1, T2, T3> TupleWrapper4\<T0, T1, T2, T3> <: ToString

```cangjie
extend<T0, T1, T2, T3> TupleWrapper4<T0, T1, T2, T3> <: ToString
```

功能：为 [TupleWrapper4](#struct-tuplewrapper4t0-t1-t2-t3) 扩展 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 实现。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

#### func toString()

```cangjie
public func toString()
```

功能：[TupleWrapper4](#struct-tuplewrapper4t0-t1-t2-t3) 的字符串表达。

### extend\<T0, T1, T2, T3> TupleWrapper4\<T0, T1, T2, T3> <: Equatable\<TupleWrapper4\<T0, T1, T2, T3>>

```cangjie
extend<T0, T1, T2> TupleWrapper3<T0, T1, T2> <: Equatable<TupleWrapper3<T0, T1, T2>>
```

功能：为 [TupleWrapper4](#struct-tuplewrapper4t0-t1-t2-t3) 扩展 [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet) 实现。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[TupleWrapper3](#struct-tuplewrapper3t0-t1-t2)\<T0, T1, T2>>

#### operator func ==(TupleWrapper4\<T0, T1, T2, T3>)

```cangjie
public operator func ==(other: TupleWrapper4<T0, T1, T2, T3>): Bool
```

功能：比较两个元组。

参数：

- other: TupleWrapper4\<T0, T1, T2, T3> - 待比较的元组。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 相等时返回 `true` ，否则返回 `false` 。

#### operator func !=(TupleWrapper4\<T0, T1, T2, T3>)

```cangjie
public operator func !=(other: TupleWrapper4<T0, T1, T2, T3>): Bool
```

功能：比较两个元组。

参数：

- other: [TupleWrapper4](#struct-tuplewrapper4t0-t1-t2-t3)\<T0, T1, T2, T3> - 待比较的元组。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 不相等时返回 `true` ，否则返回 `false` 。

### extend\<T0, T1, T2, T3> TupleWrapper4\<T0, T1, T2, T3> <: IndexAccess

```cangjie
extend<T0, T1, T2, T3> TupleWrapper4<T0, T1, T2, T3> <: IndexAccess
```

功能：为 [TupleWrapper4](#struct-tuplewrapper4t0-t1-t2-t3) 扩展 [IndexAccess](./unittest_prop_test_package_interfaces.md#interface-indexaccess) 实现。

父类型：

- [IndexAccess](unittest_prop_test_package_interfaces.md#interface-indexaccess)

#### func getElementAsAny(Int64)

```cangjie
public func getElementAsAny(index: Int64): ?Any
```

功能：按索引获取元组内的值。

参数：

- index: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 索引值。

返回值：

- ?[Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 获取到的元组内的值。索引不合法时返回 `None` 。

### extend\<T0, T1, T2, T3> TupleWrapper4\<T0, T1, T2, T3><: Arbitrary\<TupleWrapper4\<T0, T1, T2, T3>> where where T0 <: Arbitrary\<T0>,T1 <: Arbitrary\<T1>,T2 <: Arbitrary\<T2>,T3 <: Arbitrary\<T3>

```cangjie
extend<T0, T1, T2, T3> TupleWrapper4<T0, T1, T2, T3><: Arbitrary<TupleWrapper4<T0, T1, T2, T3>> where where T0 <: Arbitrary<T0>,T1 <: Arbitrary<T1>,T2 <: Arbitrary<T2>,T3 <: Arbitrary<T3>
```

功能：为 [TupleWrapper4](#struct-tuplewrapper4t0-t1-t2-t3) 扩展 [Arbitrary](./unittest_prop_test_package_interfaces.md#interface-arbitraryt) 实现。

父类型：

- [Arbitrary](unittest_prop_test_package_interfaces.md#interface-arbitraryt)\<[TupleWrapper4](#struct-tuplewrapper4t0-t1-t2-t3)\<T0, T1, T2, T3>>

#### static func arbitrary(RandomSource)

```cangjie
public static func arbitrary(random: RandomSource): Generator<TupleWrapper2<T0, T1, T2, T3>>
```

功能：获取生成 [TupleWrapper4](#struct-tuplewrapper4t0-t1-t2-t3)\<T0, T1, T2, T3> 类型随机值生成器。

返回值：

- [Generator](../unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-generatort)\<[TupleWrapper4](#struct-tuplewrapper4t0-t1-t2-t3)\<T0, T1, T2, T3>> - 生成器。

### extend\<T0, T1, T2, T3> TupleWrapper4\<T0, T1, T2, T3> <: Shrink\<TupleWrapper4\<T0, T1, T2, T3>> where T0 <: Shrink\<T0>,T1 <: Shrink\<T1>,T2 <: Shrink\<T2>, T3 <: Shrink\<T3>

```cangjie
extend<T0, T1, T2, T3> TupleWrapper4<T0, T1, T2, T3> <: Shrink<TupleWrapper4<T0, T1, T2, T3>>
        where T0 <: Shrink<T0>,
              T1 <: Shrink<T1>,
              T2 <: Shrink<T2>,
              T3 <: Shrink<T3> {
    public func shrink(): Iterable<TupleWrapper4<T0, T1, T2, T3>>
}
```

### func shrink()

```cangjie
override func shrink(): Iterable<TupleWrapper4<T0, T1, T2, T3>>
```

功能：缩减元组。

返回值：

- [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<TupleWrapper4<T0, T1, T2, T3>> -  数据迭代器。

## struct TupleWrapper5\<T0, T1, T2, T3, T4>

```cangjie
public struct TupleWrapper5<T0, T1, T2, T3, T4> {
    public TupleWrapper5(public let tuple: (T0, T1, T2, T3, T4))
}
```

功能：将闭包封装为结构体。闭包带两个参数。

### TupleWrapper5((T0, T1, T2, T3, T4))

```cangjie
public TupleWrapper5(public let tuple: (T0, T1, T2, T3, T4))
```

功能：TupleWrapper5 构造器。

参数：

- tuple: (T0, T1, T2, T3, T4) - 闭包的 5 个入参。

### let tuple

```cangjie
public let tuple: (T0, T1, T2, T3, T4)
```

功能：元组自身。

类型：(T0, T1, T2, T3, T4)

### func apply\<R>((T0, T1, T2, T3, T4) -> R)

```cangjie
public func apply<R>(f: (T0, T1, T2, T3, T4) -> R): R
```

功能：执行闭包函数。

参数：

- f: (T0, T1, T2, T3, T4) -> R - 待执行的闭包。

返回值：

- R - 闭包的执行结果。

### extend\<T0, T1, T2, T3, T4> TupleWrapper5\<T0, T1, T2, T3, T4> <: ToString

```cangjie
extend<T0, T1, T2, T3, T4> TupleWrapper5<T0, T1, T2, T3, T4> <: ToString
```

功能：为 [TupleWrapper5](#struct-tuplewrapper5t0-t1-t2-t3-t4) 扩展 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 实现。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

#### func toString()

```cangjie
public func toString()
```

功能：[TupleWrapper5](#struct-tuplewrapper5t0-t1-t2-t3-t4) 的字符串表达。

### extend\<T0, T1, T2, T3, T4> TupleWrapper5\<T0, T1, T2, T3, T4> <: Equatable\<TupleWrapper5\<T0, T1, T2, T3, T4>>

```cangjie
extend<T0, T1, T2> TupleWrapper3<T0, T1, T2> <: Equatable<TupleWrapper3<T0, T1, T2>>
```

功能：为 [TupleWrapper5](#struct-tuplewrapper5t0-t1-t2-t3-t4) 扩展 [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet) 实现。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[TupleWrapper3](#struct-tuplewrapper3t0-t1-t2)\<T0, T1, T2>>

#### operator func ==(TupleWrapper5\<T0, T1, T2, T3, T4>)

```cangjie
public operator func ==(other: TupleWrapper5<T0, T1, T2, T3, T4>): Bool
```

功能：比较两个二元元组。

参数：

- other: [TupleWrapper5](#struct-tuplewrapper5t0-t1-t2-t3-t4)\<T0, T1, T2, T3> - 待比较的元组。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 相等时返回 `true` ，否则返回 `false` 。

#### operator func !=(TupleWrapper5\<T0, T1, T2, T3, T4>)

```cangjie
public operator func !=(other: TupleWrapper2<T0, T1, T2, T3, T4>): Bool
```

功能：比较两个元组。

参数：

- other: [TupleWrapper5](#struct-tuplewrapper5t0-t1-t2-t3-t4)\<T0, T1, T2, T3, T4> - 待比较的元组。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 不相等时返回 `true` ，否则返回 `false` 。

### extend\<T0, T1, T2, T3, T4> TupleWrapper5\<T0, T1, T2, T3, T4> <: IndexAccess

```cangjie
extend<T0, T1, T2, T3, T4> TupleWrapper5<T0, T1, T2, T3, T4> <: IndexAccess
```

功能：为 [TupleWrapper5](#struct-tuplewrapper5t0-t1-t2-t3-t4) 扩展 [IndexAccess](./unittest_prop_test_package_interfaces.md#interface-indexaccess) 实现。

父类型：

- [IndexAccess](unittest_prop_test_package_interfaces.md#interface-indexaccess)

#### func getElementAsAny(Int64)

```cangjie
public func getElementAsAny(index: Int64): ?Any
```

功能：按索引获取元组内的值。

参数：

- index: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 索引值。

返回值：

- ?[Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 获取到的元组内的值。索引不合法时返回 `None` 。

### extend\<T0, T1, T2, T3, T4> TupleWrapper5\<T0, T1, T2, T3, T4> <: Arbitrary\<TupleWrapper2\<T0, T1, T2, T3, T4>> where T0 <: Arbitrary\<T0>,T1 <: Arbitrary\<T1>,T2 <: Arbitrary\<T2>,T3 <: Arbitrary\<T3>,T4 <: Arbitrary\<T4>

```cangjie
extend<T0, T1, T2, T3, T4> TupleWrapper5<T0, T1, T2, T3, T4> <: Arbitrary<TupleWrapper2<T0, T1, T2, T3, T4>> where T0 <: Arbitrary<T0>,T1 <: Arbitrary<T1>,T2 <: Arbitrary<T2>,T3 <: Arbitrary<T3>,T4 <: Arbitrary<T4>
```

功能：为 [TupleWrapper5](#struct-tuplewrapper5t0-t1-t2-t3-t4) 扩展 [Arbitrary](./unittest_prop_test_package_interfaces.md#interface-arbitraryt) 实现。

父类型：

- [Arbitrary](unittest_prop_test_package_interfaces.md#interface-arbitraryt)\<[TupleWrapper2](#struct-tuplewrapper2t0-t1)\<T0, T1, T2, T3, T4>>

#### static func arbitrary(RandomSource)

```cangjie
public static func arbitrary(random: RandomSource): Generator<TupleWrapper5<T0, T1, T2, T3, T4>>
```

功能：获取生成 [TupleWrapper5](#struct-tuplewrapper5t0-t1-t2-t3-t4)\<T0, T1, T2, T3, T4> 类型随机值生成器。

返回值：

- [Generator](../unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-generatort)\[TupleWrapper5](#struct-tuplewrapper5t0-t1-t2-t3-t4)\<T0, T1, T2, T3, T4>> - 生成器。

### extend\<T0, T1, T2, T3, T4> TupleWrapper5\<T0, T1, T2, T3, T4> <: Shrink\<TupleWrapper5\<T0, T1, T2, T3, T4>> where T0 <: Shrink\<T0>,T1 <: Shrink\<T1>,T2 <: Shrink\<T2>, T3 <: Shrink\<T3>, T4 <: Shrink\<T4>

```cangjie
extend<T0, T1, T2, T3, T4> TupleWrapper5<T0, T1, T2, T3, T4> <: Shrink<TupleWrapper5<T0, T1, T2, T3, T4>>
        where T0 <: Shrink<T0>,
              T1 <: Shrink<T1>,
              T2 <: Shrink<T2>,
              T3 <: Shrink<T3>,
              T4 <: Shrink<T4> {
    public func shrink(): Iterable<TupleWrapper5<T0, T1, T2, T3, T4>>
}
```

### func shrink()

```cangjie
override func shrink(): Iterable<TupleWrapper5<T0, T1, T2, T3, T4>>
```

功能：缩减元组。

返回值：

- [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<TupleWrapper5<T0, T1, T2, T3, T4>> -  数据迭代器。
