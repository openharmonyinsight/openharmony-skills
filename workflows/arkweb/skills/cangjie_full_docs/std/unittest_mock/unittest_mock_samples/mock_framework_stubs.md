# 桩使用指南

mock/spy 对象和桩的使用方法多种多样。本文介绍了不同的模式和用例，便于用户编写 **mock 框架**的可维护且简洁的测试用例。

## 桩的工作原理

[桩](./mock_framework_basics.md#配置-api) 通过在测试用例内部调用 `@On` 宏来声明，该声明在特定测试用例执行完成之前有效。多个测试用例之间可以[共享桩](#共享-mock-对象和桩)。

mock 框架处理 mock/spy 对象成员（或静态成员或顶层函数或顶层变量）调用时的顺序如下：

* 查找特定声明的桩。后声明的桩优先于之前声明的桩。测试用例主体内部声明的桩优先于共享桩。
* 应用每个桩的**参数匹配器**。如果所有参数都成功匹配，则执行该桩定义的操作。
* 如果找不到桩，或者没有与实际参数匹配的桩，则应用默认行为：
    * 对于 mock 对象，上报**未打桩调用**错误；
    * 对于 spy 对象，调用被监视实例的原始成员；
    * 对于静态成员或顶层函数或顶层变量，调用原始对应声明。

无论是否为单个成员定义了多个桩，每个桩都有自己的预期，需要满足这些[预期](./mock_framework_basics.md#预期)才能通过测试。

!--compile.onlyformat-->
```cangjie
@On(foo.bar(1)).returns(1)
@On(foo.bar(2)).returns(2)

foo.bar(2)
// 第一个桩已定义但从未使用，测试失败
```

## 重新定义桩

如果希望在测试中更改桩的行为，可以重新定义桩。

<!--compile.onlyformat-->
```cangjie
@On(service.request()).returns(testData)
// 使用服务

@On(service.request()).throws(Exception())
// 测试服务开始失败时会发生什么事情
```

## 同一声明定义多个桩

根据不同参数，可以使用多个桩来定义不同的行为。

示例：

<!--compile.onlyformat-->
```cangjie
@On(storage.get(_)).returns(None) // 1
@On(storage.get(TEST_ID)).returns(Some(TEST_DATA)) // 2
```

示例中，`storage` 为除 `TEST_ID` 之外的所有参数返回 `None` 。
如果从未使用 `TEST_ID` 参数调用 `get` ，则测试失败，因为桩 **2** 未使用。如果始终使用 `TEST_ID` 参数调用 `get` ，则测试失败，因为桩 **1** 未使用。这些限制确保测试代码是纯净的，让开发人员知道桩何时变为未使用。如果用例不需要此功能，则使用 `anyTimes()` 基数说明符来提升这些预期。

<!--compile.onlyformat-->
```cangjie
// 实现经常更改，但不希望测试中断
// 使用 anyTimes 提升与测试本身无关的预期
@On(storage.get(_)).returns(None).anyTimes()
@On(storage.get(TEST_ID)).returns(Some(TEST_DATA)) // 测试必须调用正在测试的内容
```

鉴于桩优先级是**从下到上**，以下用法都不正确。

<!--compile.onlyformat-->
```cangjie
@On(storage.get(TEST_ID)).returns(Some(TEST_DATA)) // 不正确，这个桩永远不会被触发
@On(storage.get(_)).returns(None) // 在上面的桩始终会被隐藏
```

您还可以使用预期来检查调用的参数。

<!--compile.onlyformat-->
```cangjie
let renderer = spy(Renderer())

@On(renderer.render(_)).fails()
let isVisible = { c: Component => c.isVisible }
@On(renderer.render(argThat(isVisible))).callsOriginal() // 只允许可见的组件
```

## 共享 mock 对象和桩

测试需要大量使用 mock 对象时可以多个测试用例共享 mock 对象和/或桩。
可以在任何位置创建 mock 或 spy 对象。然而，如果误将 mock 对象从一个测试用例泄漏到另一个测试用例，可能导致顺序依赖问题或测试不稳定。因此，不建议这样操作，mock 框架也会检测这类情况。
在同一测试类下的测试用例之间共享 mock 或 spy 对象时，可以将它们放在该类的实例变量中。

桩声明中隐含了预期，因此更难处理共享桩。测试用例之间不能共享预期。
可以声明桩的位置：

* 测试用例主体（无论是 `@Test` 函数还是`@Test`类中的`@TestCase`）：检查预期。
* 在 `@Test` 类的 `BeforeAll` 宏修饰的函数或者 `beforeAll` 函数中：在测试用例之间共享桩。这样的桩不能声明预期，预期也不会被检查。不允许使用基数说明符。只允许 `returns(value)`、`throws(exception)`、`fails()`、`callsOriginal()` 等*无状态*操作。可以将这些桩视为具有隐式 `anyTimes()` 基数。
* 如果测试用例的预期相同，则可以在测试用例主体中提取和调用函数（测试类中非测试用例的成员函数）。

> **说明：**
>
> 不要在测试类构造函数中声明桩。否则可能导致框架运行内部错误。

在测试用例主体（`@Test`类中的`@TestCase`）中声明桩的示例：

<!--compile-testBar0-->
```cangjie
import std.unittest.mock.*
import std.unittest.mock.mockmacro.*

class Foo {
    public func bar(x: Int64): String {
        match (x) {
            case 0 => "zero"
            case 1 => "one"
            case _ => "default"
        }
    }
}

@Test
class TestFoo {
    let foo = mock<Foo>()

    func setupDefaultStubs() {
        @On(foo.bar(_)).returns("default")
    }

    @TestCase
    func testZero() {
        setupDefaultStubs()
        @On(foo.bar(0)).returns("zero")

        foo.bar(0) // 返回"zero"
        foo.bar(1) // 返回"default"
    }

    @TestCase
    func testOne() {
        setupDefaultStubs()
        @On(foo.bar(0)).returns("zero")
        foo.bar(0) // 返回"zero"

        // 预期失败，桩已声明但从未使用
    }
}
```

在 `@Test` 类的 `beforeAll` 函数中使用的示例：

<!--compile-testBar1-->
```cangjie
import std.unittest.mock.*
import std.unittest.mock.mockmacro.*

@Test
class TestFoo2 {
    let foo = mock<Foo>()

    // 单元测试框架会在执行测试用例之前调用以下内容
    @BeforeAll
    public func beforeAll(): Unit {
        // 在所有测试用例之间共享默认行为
        // 此桩无需在每个测试用例中使用
        @On(foo.bar(_)).returns("default")
    }

    @TestCase
    func testZero() {
        @On(foo.bar(0)).returns("zero") // 本测试用例中需要使用此桩
        foo.bar(0) // 返回 "zero"
        foo.bar(1) // 返回 "default"
    }

    @TestCase
    func testOne() {
        @On(foo.bar(0)).returns("one")
        foo.bar(0) // 返回 "one"
    }
}
```

## 捕获参数
<!-- 链接至值侦听器API （自动生成的 API 手册） -->

mock 框架使用 `captor(ValueListener)` 参数匹配器**捕获**参数来检查传递到桩声明的实际参数。只要触发了桩，`ValueListener` 就会拦截相应的参数，并检查参数和/或添加验证参数。

每次调用时，还可以使用 ValueListener.onEach 静态函数来验证某个条件。接受 lambda 后，触发桩时都会调用这个 lambda 。lambda 用于接收参数的值。

<!--compile.onlyformat-->
```cangjie
let renderer = spy(TextRenderer())
let markUpRenderer = MarkupRenderer(renderer)

// 创建验证器
let validator = ValueListener.onEach {
    str: String => @Assert(str == "must be bold")
}

// 使用 'capture' 参数匹配器绑定参数到验证器
@On(renderer.renderBold(capture(validator))).callsOriginal() // 如果从来没有调用过，则测试失败

markUpRenderer.render("text inside tag <b>must be bold</b>")
```

另外 `ValueListener` 还提供了 `allValues()` 和 `lastValue()` 函数来检查参数。模式如下：

<!--compile.onlyformat-->
```cangjie
// 创建捕获器
let captor = ValueListener<String>.new()

// 使用'capture'参数匹配器绑定参数到捕获器
@On(renderer.renderBold(capture(captor))).callsOriginal()

markUpRenderer.render("text inside tag <b>must be bold</b>")

let argumentValues = captor.allValues()
@Assert(argumentValues.size == 1 && argumentValues[0] == "must be bold")
```

`argThat` 匹配器是一个结合了参数过滤和捕获的重载函数。`argThat(listener, filter)` 接受 `ValueListener` 实例和 `filter` 谓词。`listener` 只收集通过 `filter` 检查的参数。

<!-- 链接至argThat匹配器 （自动生成的 API 手册） -->

<!--compile.onlyformat-->
```cangjie
let filter = { arg: String => arg.contains("bold") }
let captor = ValueListener<String>.new()

// 失败，除非参数被拦截，但下面已经声明了桩
@On(renderer.renderBold(_)).fails()
// 只收集包含 "bold" 的字符串
@On(renderer.renderBold(argThat(captor, filter))).callsOriginal()

markUpRenderer.render("text inside tag <b>must be bold</b>")

// 可以使用 'captor' 对象检查所有过滤参数
@Assert(captor.lastValue() == "must be bold")
```

参数捕获器可以与 mock 和 spy 对象一起使用。但是，在 [@Called](./mock_framework_verification.md#验证语句和-called-宏) 宏中不允许使用此类参数匹配器。

<!--链接至@Called宏并验证API （自动生成的 API 手册） -->

## 自定义和使用参数匹配器

为了避免重复使用相同的**参数匹配器**，可以自定义参数匹配器。

如下示例为在测试用例之间共享匹配器：

<!--compile.onlyformat-->
```cangjie
@On(foo.bar(oddNumbers())).returns("Odd")
@On(foo.bar(evenNumbers())).returns("Even")
foo.bar(0) // "Even"
foo.bar(1) // "Odd"
```

由于每个匹配器都只是 `Matchers` 类的静态函数，因此可以使用**扩展**来自定义参数匹配器。新参数匹配器需要调用现有的（实例）。

<!-- 链接至Matchers类 （自动生成的 API 手册） -->
<!--compile-->
```cangjie
import std.unittest.mock.*

extend Matchers {
    static func evenNumbers(): TypedMatcher<Int> {
        argThat {arg: Int => arg % 2 == 0}
    }

    static func oddNumbers(): TypedMatcher<Int> {
        argThat {arg: Int => arg % 2 == 1}
    }
}
```

函数参数匹配器可以包含参数。
<!--compile-->
```cangjie
import std.unittest.mock.*

extend Matchers {
    // 只接受Int参数。
    static func isDivisibleBy(n: Int): TypedMatcher<Int> {
        argThat {arg: Int => arg % n == 0}
    }
}
```

大多数匹配器函数都指定了返回类型 `TypedMatcher<T>` 。这样的匹配器只接受类型为 `T` 。在桩声明中使用参数匹配器调用时，类型为 `T` 的值应该是被打桩函数或属性 setter 的有效参数。换句话说，类型 `T` 应该是参数子类型或与参数实际类型相同。

## 设置属性和字段和顶层变量

字段和属性和顶层变量打桩的方式与函数相同，可以依[相同操作](./mock_framework_basics.md#操作-api)来配置返回值。

setter 类似于返回 `Unit` 的函数。特殊操作 `doesNothing()` 可用于 setter。

可变属性打桩的常用模式如下：

```cangjie
@On(foo.prop).returns("value")  // 配置getter
@On(foo.prop = _).doesNothing() // 忽略setter调用
```

极少场景下，我们期望可变属性的行为与字段的行为相同。要创建**合成字段**（框架生成的字段），请使用 `SyntheticField.create` 静态函数。合成字段存储由 mock 框架来管理。适用于 mock 含有可变属性和字段的接口或抽象类的场景。

<!-- 链接至SyntheticField类 （自动生成的 API 手册）-->

执行 `getsField` 和 `setsField` 桩操作将字段或顶层变量绑定到特定的调用，这些操作可以将预期配置为任何其他操作。

<!-- 待办：链接至字段操作 -->

<!--compile-->
```cangjie
import std.unittest.mock.*
import std.unittest.mock.mockmacro.*

interface Foo {
    mut prop bar: String
}

@Test
func test() {
    let foo = mock<Foo>()
    let syntheticField = SyntheticField.create(initialValue: "initial")
    @On(foo.bar).getsField(syntheticField) // 对属性的读取访问即为读取合成字段
    @On(foo.bar = _).setsField(syntheticField) // 为属性写入新值

    // 此时'bar'属性表现为字段
}
```

> **注意:**
>
> 如果多个测试用例之间共享 `SyntheticField` 对象，则该字段本身的值会在每个测试用例之前重置为 `initialValue` ，避免在测试之间共享可变状态。

## 桩的模式

通常，当一些调用匹配不到任何桩时将抛出异常。但是，对于某些常见情况，mock 对象可以配置增加默认行为，此时，当匹配不到任何桩时，将执行默认行为。这通过启用**桩模式**来实现。

有两种可用的模式 `ReturnsDefaults` 和 `SyntheticFields` 。这些模式通过枚举类型 `StubMode` 表示。可以通过在创建 mock 对象时将其传递给 `mock` 函数来为特定的 mock 对象启用桩模式。

```cangjie
public func mock<T>(modes: Array<StubMode>): T
```

桩模式可用于在配置 mock 对象时减少代码，并且它们可以与显式桩自由组合。显式的桩始终优先于其默认行为。

> **注意：**
>
> 使用桩模式不会对 mock 对象的成员强加任何期望。
> 当用例是检查是否仅调用 mock 对象的某些特定成员，则应谨慎使用桩模式。被测对象的行为可能会以不期望的方式发生变化，但测试仍可能通过。
> 当前桩模式不支持打桩静态成员和顶级函数/变量。

### ReturnsDefaults 模式

在此模式下，当成员的返回类型在如下表格中时，无需显式配置桩，即可调用。

<!--compile.onlyformat-->
```cangjie
let foo = mock<Foo>(ReturnsDefaults)
@Assert(foo.isPretty(), false)
```

此类成员返回的默认值也如如下表格所示。

| 类型 | 默认值 |
| ---  | --- |
| Bool | false |
| numbers | 0 |
| String | empty string |
| Option | None |
| ArrayList, HashSet, Array | new empty collection |
| HashMap | new empty map |

`ReturnsDefaults` 模式仅对如下成员生效：

* 返回值为支持类型（如上表）的成员函数。
* 类型为支持类型（如上表）的属性读取器和字段。

### SyntheticFields 模式

`SyntheticFields` 模式可简化对 `SyntheticField` 的配置动作，详见 [设置属性和字段和顶层变量](#设置属性和字段和顶层变量) 章节。

`SyntheticFields` 将通过 mock 框架为所有属性和字段隐式创建对应类型的合成字段。但是，这些字段只能在被赋值后读取。仅对可变属性和字段生效。

<!--compile.onlyformat-->
```cangjie
let foo = mock<Foo>(SyntheticFields)
// can simply assign a value to a mutable property
foo.bar = "Hello"
@Assert(foo.bar, "Hello")
```

赋给属性和字段的值仅在相应的测试用例中可见。

当同时启用 `SyntheticFields` 和 `ReturnsDefaults` 时，赋的值优先于默认值。但是，只要字段或属性尚未被赋值，就可以使用默认值。

<!--compile.onlyformat-->
```cangjie
let foo = mock<Foo>(ReturnsDefaults, SyntheticFields)
@Assert(foo.bar, "")
foo.bar = "Hello"
@Assert(foo.bar, "Hello")
```
