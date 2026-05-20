# std.unittest.testmacro

## 功能介绍

unittest.testmacro 为单元测试框架提供了用户所需的宏。

## API 列表

### 宏

|              宏名          |           功能           |
| --------------------------- | ------------------------ |
| [AfterAll](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#afterall-宏) | 声明测试类中的函数为[测试生命周期](../unittest/unittest_samples/unittest_basics.md#测试生命周期)函数。被该宏修饰的函数在所有测试用例之后运行一次。 |
| [AfterEach](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#aftereach-宏) | 声明测试类中的函数为[测试生命周期](../unittest/unittest_samples/unittest_basics.md#测试生命周期)函数。被该宏修饰的函数在每个测试用例之后运行一次。 |
| [Assert](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏) | 声明 Assert 断言，测试函数内部使用，断言失败停止用例。 |
| [AssertThrows](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assertthrows-宏) | 声明[预期异常的断言](../unittest/unittest_samples/unittest_basics.md#预期异常的断言)，测试函数内部使用，断言失败停止用例。 |
| [BeforeAll](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#beforeall-宏) | 声明测试类中的函数为[测试生命周期](../unittest/unittest_samples/unittest_basics.md#测试生命周期)函数。被该宏修饰的函数在所有测试用例之前运行一次。 |
| [BeforeEach](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#beforeeach-宏) | 声明测试类中的函数为[测试生命周期](../unittest/unittest_samples/unittest_basics.md#测试生命周期)函数。被该宏修饰的函数在每个测试用例之前运行一次。 |
| [Bench](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#bench-宏) | 宏用于标记要执行多次的函数并计算该函数的预期执行时间。 |
| [Configure](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#configure-宏) | 为测试类或测试函数提供配置参数。它可以放置在测试类或测试函数上。 |
| [CustomAssertion](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#customassertion-宏) | `@CustomAssertions` 将函数指定为用户自定义断言。 |
| [Expect](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) | 声明 Expect 断言，测试函数内部使用，断言失败继续执行用例。 |
| [ExpectThrows](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expectthrows-宏) | 声明[预期异常的断言](../unittest/unittest_samples/unittest_basics.md#预期异常的断言)，测试函数内部使用，断言失败继续执行用例。 |
| [Fail](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#fail-宏) | 声明[预期失败的断言](../unittest/unittest_samples/unittest_basics.md#失败断言)，测试函数内部使用，断言失败停止用例。 |
| [FailExpect](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#failexpect-宏) | 声明[预期失败的断言](../unittest/unittest_samples/unittest_basics.md#失败断言)，测试函数内部使用，断言失败继续执行用例。 |
| [Measurement](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#measure-宏) | 用于为性能测试指定 [Measurement](../unittest/unittest_package_api/unittest_package_interfaces.md#interface-measurement) 实例。只能应用于标有 `@Test` 宏的类或顶级函数的范围内。 |
| [Parallel](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#parallel-宏) | 可以修饰测试类。被 `@Parallel` 修饰的测试类中的测试用例可并行执行。 |
| [PowerAssert](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#powerassert-宏) | 检查传递的表达式是否为真，并显示包含传递表达式的中间值和异常的详细图表。 |
| [Skip](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#skip-宏) | 修饰已经被 `@TestCase` / `@Bench` 修饰的函数，使该测试用例被跳过。 |
| [Strategy](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#strategy-宏) | 用于组合、映射和重用各种数据策略。|
| [Tag](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#tag-宏) | `@Tag` 宏可以应用于 `@Test` 类和 `@Test` 或 `@TestCase` 函数，提供测试实体的元信息。|
| [Test](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#test-宏) | 宏应用于顶级函数或顶级类，使该函数或类转换为单元测试类。 |
| [TestBuilder](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#testbuilder-宏) | 声明一个[动态测试](../unittest/unittest_samples/unittest_dynamic_tests.md)套。|
| [TestCase](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#testcase-宏) | 宏用于标记单元测试类内的函数，使这些函数成为单元测试的测试用例。 |
| [Timeout](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#timeout-宏) | 指示测试应在指定时间后终止。它有助于测试可能运行很长时间或陷入无限循环的复杂算法。 |
| [Types](./unittest_testmacro_package_api/unittest_testmacro_package_macros.md#types-宏) |  宏为测试类或测试函数提供类型参数。它可以放置在测试类或测试函数上。 |
