# 函数

## func mock\<T>()

```cangjie
public func mock<T>(): T
```

功能：创建类型 T 的 [`mock object`](../unittest_mock_samples/mock_framework_basics.md#创建-mock-对象)， 这个对象默认情况下，所有的成员函数、属性或运算符重载函数没有任何具体实现。
可以通过 `@On` 指定这个对象的成员函数、属性或运算符重载函数的行为。

返回值：

- T - 类型 T 的 `mock object` 。

## func mock\<T>(Array\<StubMode>)

```cangjie
public func mock<T>(modes: Array<StubMode>): T
```

功能：创建类型 T 的 [`mock object`](../unittest_mock_samples/mock_framework_basics.md#创建-mock-对象) ， 参数指定了[桩的模式](../unittest_mock_samples/mock_framework_stubs.md#桩的模式)。

参数：

- modes: Array\<StubMode> - 指定桩的模式，可以为多个。

返回值：

- T - 类型 T 的 `mock object` 。

## func spy\<T>(T)

```cangjie
public func spy<T>(objectToSpyOn: T): T
```

功能：创建类型 T 的 `spy object` （ `mock object` 的扩展，对象的成员拥有默认实现的“骨架”对象）。 这个对象包装了所传入的对象，并且默认情况下成员函数、属性或运算符重载函数实现为对这个传入的实例对象的对应成员函数、属性或运算符重载函数的调用。
可以通过 `@On` 重载这个对象的成员函数、属性或运算符重载函数的行为。

参数：

- objectToSpyOn: T - 传入实例对象，默认情况下，使用该对象的实现。

返回值：

- T - 类型 T 的 `spy object` 。
