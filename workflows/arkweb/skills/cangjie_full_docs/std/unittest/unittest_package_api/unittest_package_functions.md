# 函数

## func assertCaughtUnexpectedE(String, String, String, ?AssertionCtx)

```cangjie
public func assertCaughtUnexpectedE(
    message: String,
    expectedExceptions: String,
    caughtException: String,
    optParentCtx!: ?AssertionCtx = None
): Nothing
```

功能：捕获的异常不符合预期，记录信息，抛出异常。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 不符合预期时的提示信息。
- expectedExceptions: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 期望的捕获的异常。
- caughtException: [String](../../core/core_package_api/core_package_structs.md#struct-string)  - 实际捕获的异常。
- optParentCtx!: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[AssertionCtx](./unittest_package_classes.md#class-assertionctx)> - 存储嵌套断言失败消息的上下文。

## func assertEqual\<T>(String, String, T, T, ?AssertionCtx)

```cangjie
public func assertEqual<T>(
    leftStr: String,
    rightStr: String,
    expected: T,
    actual: T,
    optParentCtx!: ?AssertionCtx = None
): Unit where T <: Equatable<T>
```

功能：比较 `expected` 和 `actual` 值是否相等。若不等，直接抛出异常。

参数：

- leftStr: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 期望的表达式的字符串。
- rightStr: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际的表达式的字符串。
- expected: T - 期望的值。
- actual: T - 实际值。
- optParentCtx!: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[AssertionCtx](./unittest_package_classes.md#class-assertionctx)> - 存储嵌套断言失败消息的上下文。

## func assertEqual\<T>(String, String, T, T, Bool, ?AssertionCtx)

```cangjie
public func assertEqual<T>(
    leftStr: String,
    rightStr: String,
    expected: T,
    actual: T,
    isDelta!: Bool = false,
    optParentCtx!: ?AssertionCtx = None
): Unit where T <: Equatable<T>
```

功能：比较 `expected` 和 `actual` 值是否相等。若不等，直接抛出异常。

参数：

- leftStr: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 期望的表达式的字符串。
- rightStr: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际的表达式的字符串。
- expected: T - 期望的值。
- actual: T - 实际值。
- isDelta!: Bool - 是否使用近似相等。默认不使能。
- optParentCtx!: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[AssertionCtx](./unittest_package_classes.md#class-assertionctx)> - 存储嵌套断言失败消息的上下文。

## func defaultConfiguration()

```cangjie
public func defaultConfiguration(): Configuration
```

功能：生成默认的配置信息。

返回值：

- [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 配置信息。

## func entryMain(TestPackage)

```cangjie
public func entryMain(testPackage: TestPackage): Int64
```

功能：提供给 `cjc --test` 使用，框架执行测试用例的入口函数。

参数：

- testPackage: [TestPackage](./unittest_package_classes.md#class-testpackage) - 测试包对象。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行结果。

## func expectCaughtUnexpectedE(String, String, String, ?AssertionCtx)

```cangjie
public func expectCaughtUnexpectedE(
    message: String,
    expectedExceptions: String,
    caughtException: String,
    optParentCtx!: ?AssertionCtx = None
): Unit
```

功能：捕获的异常不符合预期，记录信息，不抛出异常。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 不符合预期时的提示信息。
- expectedExceptions: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 期望的捕获的异常。
- caughtException: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际捕获的异常。
- optParentCtx!: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[AssertionCtx](./unittest_package_classes.md#class-assertionctx)> - 存储嵌套断言失败消息的上下文。

## func expectEqual\<T>(String, String, T, T, ?AssertionCtx)

```cangjie
public func expectEqual<T>(
    leftStr: String,
    rightStr: String,
    expected: T,
    actual: T,
    optParentCtx!: ?AssertionCtx
): Unit where T <: Equatable<T>
```

功能：比较 `expected` 和 `actual` 值是否相等。记录比较结果，不抛出异常。

参数：

- leftStr: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 期望的表达式的字符串。
- rightStr: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际的表达式的字符串。
- expected: T - 期望的值。
- actual: T  - 实际值。
- optParentCtx!: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[AssertionCtx](./unittest_package_classes.md#class-assertionctx)> - 存储嵌套断言失败消息的上下文。

## func expectEqual\<T>(String, String, T, T, Bool, ?AssertionCtx)

```cangjie
public func expectEqual<T>(
    leftStr: String,
    rightStr: String,
    expected: T,
    actual: T,
    isDelta!: Bool = false,
    optParentCtx!: ?AssertionCtx
): Unit where T <: Equatable<T>
```

功能：比较 `expected` 和 `actual` 值是否相等。记录比较结果，不抛出异常。

参数：

- leftStr: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 期望的表达式的字符串。
- rightStr: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际的表达式的字符串。
- expected: T - 期望的值。
- actual: T  - 实际值。
- isDelta!: Bool - 是否使用近似相等。默认不使能。
- optParentCtx!: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[AssertionCtx](./unittest_package_classes.md#class-assertionctx)> - 存储嵌套断言失败消息的上下文。

## func fail(String)

```cangjie
public func fail(message: String): Nothing
```

功能：使该用例失败，直接抛出异常。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 失败信息。

## func failExpect(String)

```cangjie
public func failExpect(message: String): Unit
```

功能：使该用例失败，记录信息，不抛出异常。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 失败信息。

## func invokeCustomAssert\<T>(Array\<String>, String, (AssertionCtx) -> T, ?AssertionCtx)

```cangjie
public func invokeCustomAssert<T>(
    passerdArgs: Array<String>,
    caller: String,
    assert: (AssertionCtx) -> T,
    optParentCtx!: ?AssertionCtx = None
): T
```

功能：运行在 [`@Test`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#test-宏), [`@TestCase`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#testcase-宏)，或 [`@CustomAssertion`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#customassertion-宏) 宏中使用的 [`@Assert\[caller\](passerArgs)`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏) 指定的用户定义断言函数。

参数：

- passedArgs: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 未处理的已传递参数。
- caller: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 调用的自定义断言的名称。
- assert: ([AssertionCtx](./unittest_package_classes.md#class-assertionctx)) -> T - 捕获带有正确参数的断言调用。
- optParentCtx!: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[AssertionCtx](./unittest_package_classes.md#class-assertionctx)> - 存储嵌套断言失败消息的上下文。

返回值：

- T - 由用户定义的断言返回的值。

## func invokeCustomExpect(Array\<String>, String, (AssertionCtx) -> Any, ?AssertionCtx)

```cangjie
public func invokeCustomExpect(
    passerdArgs: Array<String>,
    caller: String,
    expect: (AssertionCtx) -> Any,
    optParentCtx!: ?AssertionCtx = None
): Unit
```

功能：运行在 [`@Test`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#test-宏), [`@TestCase`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#testcase-宏), 或 [`@CustomAssertion`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#customassertion-宏) 宏中使用的 [`@Expect\[caller\](passerArgs)`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) 指定的用户定义断言函数。

参数：

- passedArgs: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 未处理的已传递参数。
- caller: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 调用的自定义断言的名称。
- expect: ([AssertionCtx](./unittest_package_classes.md#class-assertionctx)) -> [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 捕获带有正确参数的断言调用。
- optParentCtx!: [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[AssertionCtx](./unittest_package_classes.md#class-assertionctx)> - 存储嵌套断言失败消息的上下文。

## func isNearExpansion\<CT, D>(CT, CT, D, String)

```cangjie
public func isNearExpansion<CT, D>(
    l: CT,
    r: CT,
    delta!: D,
    cmpType!: String
): Bool where CT <: NearEquatable<CT, D> & Comparable<CT>
```

功能：判断两个参数是否近似相等。在 [PowerAssert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#powerassert-宏) 宏展开时使用。用户不应使用。

参数：

- l: CT - 待判断近似相等的参数。
- r: CT - 待判断近似相等的参数。
- delta!: D - 待判断近似相等时使用的 delta。
- cmpType!: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 判断的类型。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否近似相等。

## func isNearExpansion\<CT, D>(CT, CT, D, String, Bool)

```cangjie
public func isNearExpansion<CT, D>(
    l: CT,
    r: CT,
    delta!: D,
    cmpType!: String,
    overloadHack!: Bool = true
): Bool where CT <: NearEquatable<CT, D>
```

功能：判断两个参数是否近似相等。在 [PowerAssert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#powerassert-宏) 宏展开时使用。用户不应使用。

参数：

- l: CT - 待判断近似相等的参数。
- r: CT - 待判断近似相等的参数。
- delta!: D - 待判断近似相等时使用的 delta。
- cmpType!: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 判断的类型。
- overloadHack!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 为使能函数重载使用新增的参数，默认值为 true 。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否近似相等。
