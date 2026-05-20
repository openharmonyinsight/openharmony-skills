# 函数

## func emptyIterable\<T>()

```cangjie
public func emptyIterable<T>(): Iterable<T>
```

功能：创建一个空的迭代器。

返回值：

- [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 空迭代器。

## func random\<T>() where T <: Arbitrary\<T>

```cangjie
public func random<T>(): RandomDataStrategy<T> where T <: Arbitrary<T>
```

功能：该函数生成 T 类型的随机数据，其中 T 必须实现接口 [Arbitrary](./unittest_prop_test_package_interfaces.md#interface-arbitraryt)\<T> 。该函数的返回值是参数化测试的一种参数源。

返回值：

- [RandomDataStrategy](./unittest_prop_test_package_classes.md#class-randomdatastrategyt)\<T> - 使用随机数据生成的 RandomDataStrategy 接口的实例。

## func randomInRange\<T>(Option\<T>, Option\<T>)

```cangjie
public func randomInRange<T>(min!: Option<T> = None, max!: Option<T> = None): RandomDataStrategyRange<T> where T <: ArbitraryRange<T>
```

功能：创建一个 [RandomDataStrategyRange\<T>](../unittest_prop_test_package_api/unittest_prop_test_package_classes.md#class-randomdatastrategyranget)

参数：

- min: T - 最小值（包含）。
- max: T - 最大值（不包含）。

返回值：

- [RandomDataStrategyRange\<T>](../unittest_prop_test_package_api/unittest_prop_test_package_classes.md#class-randomdatastrategyranget) - 随机数据策略器。
