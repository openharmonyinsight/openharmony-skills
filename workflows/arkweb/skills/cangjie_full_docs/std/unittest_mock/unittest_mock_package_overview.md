# std.unittest.mock

## 功能介绍

unittest.mock 包提供仓颉单元测试的**mock 框架**，提供 API 用于创建和配置**mock 对象**（以及独立声明，例如顶层或静态函数和顶层或静态变量），这些 mock 对象与真实对象拥有签名一致的 API 。mock 测试技术支持隔离测试代码，测试用例使用 mock 对象编码，实现外部依赖消除。

**mock 框架**具有以下特性：

* 创建 mock 对象和 spy 对象：测试时无需修改生产代码。配置独立声明（例如顶层函数或变量、静态函数或变量）时不需要此步骤。
* 简单的[配置 API](./unittest_mock_samples/mock_framework_basics.md#配置-api) ：可配置 mock/spy 对象（或独立声明）的行为。
* 单元测试框架部分：无缝集成单元测试框架的其他特性，错误输出可读。
* 自动验证配置行为：大多数情况下不需要多余的验证代码。
* 提供[验证 API](./unittest_mock_samples/mock_framework_verification.md)：用于测试系统内部的复杂交互。

用户使用场景包括：

* 简化测试设置和代码。
* 测试异常场景。
* 用轻量级 mock 对象替换*代价高的*依赖，提高测试性能。
* 验证测试复杂场景，如调用的顺序/数量。

用户可通过[快速入门](./unittest_mock_samples/mock_framework_getting_started.md)写出第一个带 mock 的测试程序。同时文档对于一些[基础概念及用法](./unittest_mock_samples/mock_framework_basics.md)做了说明并附有示例代码，另外，针对配置 API （[桩](./unittest_mock_samples/mock_framework_stubs.md)）的高阶用法做了进一步说明。

## API 列表

### 函数

|              函数名          |           功能           |
| --------------------------- | ------------------------ |
| [mock\<T>()](./unittest_mock_package_api/unittest_mock_package_functions.md#func-mockt) | 创建类型 T 的 [`mock object`](./unittest_mock_samples/mock_framework_basics.md#创建-mock-对象)， 这个对象默认情况下，所有的成员函数、属性或运算符重载函数没有任何具体实现。 |
| [mock\<T>(Array\<StubMode>)](./unittest_mock_package_api/unittest_mock_package_functions.md#func-mocktarraystubmode) | 创建类型 T 的 [`mock object`](../unittest_mock/unittest_mock_samples/mock_framework_basics.md#创建-mock-对象) ， 参数指定了[桩的模式](../unittest_mock/unittest_mock_samples/mock_framework_stubs.md#桩的模式)。 |
| [spy\<T>(T)](./unittest_mock_package_api/unittest_mock_package_functions.md#func-spytt) | 创建类型 T 的 `spy object` ( `mock object` 的扩展，对象的成员拥有默认实现的“骨架”对象)。 这个对象包装了所传入的对象，并且默认情况下成员函数、属性或运算符重载函数实现为对这个传入的实例对象的对应成员函数、属性或运算符重载函数的调用。 |

### 接口

|              接口名          |           功能           |
| --------------------------- | ------------------------ |
| [ValueListener\<T>](./unittest_mock_package_api/unittest_mock_package_interfaces.md#interface-valuelistenert) | 此接口提供了多个成员函数以支持“监听”传入给桩签名的参数。 |

### 类

|              类名          |           功能           |
| --------------------------- | ------------------------ |
| [ActionSelector](./unittest_mock_package_api/unittest_mock_package_classes.md#class-actionselector) | 此抽象类提供了为成员函数指定一个[操作 API](../unittest_mock/unittest_mock_samples/mock_framework_basics.md#操作-api) ，并允许链式调用的方法。 |
| [AnyMatcher](./unittest_mock_package_api/unittest_mock_package_classes.md#class-anymatcher) | 任意参数匹配器，即桩签名允许任意的参数。 |
| [ArgumentMatcher](./unittest_mock_package_api/unittest_mock_package_classes.md#class-argumentmatcher) |参数匹配器抽象类，该类与其子类可作为桩签名的入参类型。 |
| [CardinalitySelector\<A>](./unittest_mock_package_api/unittest_mock_package_classes.md#class-cardinalityselectora) | 此接口提供了可定义桩签名的最近一次行为的执行次数的 API 。 |
| [ConfigureMock](./unittest_mock_package_api/unittest_mock_package_classes.md#class-configuremock) | 配置 `mock object` 。 |
| [Continuation\<A>](./unittest_mock_package_api/unittest_mock_package_classes.md#class-continuationa) | 此类提供了可继续定义桩签名的行为的 API 。 |
| [GetterActionSelector\<TRet>](./unittest_mock_package_api/unittest_mock_package_classes.md#class-getteractionselectortret) | 此类提供了为属性 `Getter` 函数指定一个[操作 API](../unittest_mock/unittest_mock_samples/mock_framework_basics.md#操作-api) ，并允许链式调用的方法。 |
| [Matchers](./unittest_mock_package_api/unittest_mock_package_classes.md#class-matchers) | 该类提供生成[匹配器](./unittest_mock_samples/mock_framework_basics.md#参数匹配器)的静态函数。匹配器对象仅可通过此处的静态函数生成。匹配器可在[桩链](./unittest_mock_samples/mock_framework_basics.md#桩链)中使用。 |
| [MethodActionSelector\<TRet>](./unittest_mock_package_api/unittest_mock_package_classes.md#class-methodactionselectortret) | 此类提供了为成员函数指定一个[操作 API](../unittest_mock/unittest_mock_samples/mock_framework_basics.md#操作-api) ，并允许链式调用。 |
| [MockFramework](./unittest_mock_package_api/unittest_mock_package_classes.md#class-mockframework) | 提供用例执行所需的框架准备与结束回收阶段的函数。 |
| [NoneMatcher](./unittest_mock_package_api/unittest_mock_package_classes.md#class-nonematcher) | 参数值为 `None` 的匹配器。 |
| [OrderedVerifier](./unittest_mock_package_api/unittest_mock_package_classes.md#class-orderedverifier) | 此类型用于收集 “验证语句”， 可在 ordered 函数中动态传入验证行为。|
| [SetterActionSelector\<TRet>](./unittest_mock_package_api/unittest_mock_package_classes.md#class-setteractionselectortret) | 此类提供了为属性 `Setter` 函数指定一个[操作 API](../unittest_mock/unittest_mock_samples/mock_framework_basics.md#操作-api) ，并允许链式调用的方法。 |
| [SyntheticField\<T>](./unittest_mock_package_api/unittest_mock_package_classes.md#class-syntheticfieldt) | 合成字段。 |
| [TypedMatcher\<T>](./unittest_mock_package_api/unittest_mock_package_classes.md#class-typedmatchert) | 参数类型匹配器。 |
| [UnorderedVerifier](./unittest_mock_package_api/unittest_mock_package_classes.md#class-unorderedverifier) | 此类型用于收集 “验证语句”， 可在 unordered 函数中动态传入验证行为。 |
| [Verify](./unittest_mock_package_api/unittest_mock_package_classes.md#class-verify) | `Verify` 提供了一系列静态方法来支持定义所需验证的动作，如 `that` 、 `ordered` 以及 `unorder` 。 |
| [VerifyStatement](./unittest_mock_package_api/unittest_mock_package_classes.md#class-verifystatement) | 此类型表示对“桩签名”在验证范围内的单个验证验证语句（即上文中的“验证语句”），提供了成员函数指定“桩签名”的执行次数。 |

### 枚举

|              枚举名          |           功能           |
| --------------------------- | ------------------------ |
| [Exhaustiveness](./unittest_mock_package_api/unittest_mock_package_enums.md#enum-exhaustiveness) | 此枚举类型用于指定 `unordered` 函数的验证模式，包含两种模式。 |
| [MockSessionKind](./unittest_mock_package_api/unittest_mock_package_enums.md#enum-mocksessionkind) | 控制允许在 MockSession 使用的[桩](../unittest_mock/unittest_mock_samples/mock_framework_basics.md#配置-api)的类型。 |
| [StubMode](./unittest_mock_package_api/unittest_mock_package_enums.md#enum-stubmode) | 控制[桩的模式](../unittest_mock/unittest_mock_samples/mock_framework_stubs.md#桩的模式)。 |
