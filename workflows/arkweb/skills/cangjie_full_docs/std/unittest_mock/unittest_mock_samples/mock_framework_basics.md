# mock 基础概念及用法

## 创建 mock 对象

**mock 构造函数**可以通过调用 `mock<T>` 和 `spy<T>` 函数来创建两种对象：**mock** 和 **spy**，其中 `T` 表示被 mock 的类或接口。

```cangjie
public func mock<T>(): T
public func spy<T>(objectToSpyOn: T): T
```

<!-- 链接至 mock/spy 构造函数 -->

**mock** 作为骨架对象，默认不对成员进行任何操作。

**spy** 作为一种特殊的 mock 对象用于封装某个类或接口的当前实例。默认情况下，spy 对象将其成员调用委托给底层对象。
其他方面，spy 和 mock 对象非常相似。

只有**类**（包括 final 类和 sealed 类）和**接口**支持通过这种方式 mock 。

参阅[使用 mock 和 spy 对象](#使用-spy-和-mock-对象)。

参阅[顶级和静态声明](#顶级和静态声明) 了解如何 mock 顶级和静态声明。

## 配置 API

**配置 API** 是框架的核心，可以定义 mock/spy 对象成员（或顶层/静态声明）的行为（或重新定义 spy 对象（或顶层/静态声明））。

**配置 API** 的入口是 `@On` 宏调用。

<!--compile.onlyformat-->
```cangjie
@On(storage.getComments(testId)).returns(testComments)
```

示例中，如果 mock 对象 `storage` *接收*到 `getComments` 方法的调用，并且指定了参数 `testId` ，则返回 `testComment` 。

如上行为即为**打桩**，桩（Stub， 模拟还未实现或无法在测试环境中执行的组件）需在测试用例主体内部先定义。

如下声明类型可以被打桩：

* 类和接口的实例成员（包括 final 成员）
* 静态函数、属性和字段
* 顶层函数和变量

以下声明**不能**打桩：

* 扩展成员
* Foreign 函数
* 局部函数和变量
* 构造器
* 常量
* 任意私有声明

一个完整的**桩声明**包含以下部分：

1. `@On` 宏调用中描述的**桩签名**。
2. 用于描述桩行为的[操作](#操作-api)。
3. （可选）用于设置[预期](#预期)的基数说明符（cardinality specifier， 指定预期执行次数的表达式）。
4. （可选）[续体](#桩链)（continuation， 支持链式调用的表达式）。

mock 框架拦截匹配桩签名的调用，并执行桩声明中指定的操作。

### 顶级和静态声明

与类或接口的成员不同，要打桩静态成员或顶层函数或变量时，不需要创建模拟对象。这些声明应该直接使用配置 API （例如 `@On` 宏）进行打桩。

如下是一个为顶层函数打桩的示例：

<!--run -->
```cangjie
import std.unittest.mock.*
import std.unittest.mock.mockmacro.*

public class Entry {
    Entry(let id: Int64, let title: String, let description: String) {}
    static func parse(): Entry {
        Entry(1, "1", "1")
    }
}

public func loadLastEntryInCatalog(): Entry {
    return Entry.parse()
}

public func drawLastEntryWidget() {
    let lastEntry = loadLastEntryInCatalog()
    // drawing...
}

@Test
class RightsTest {
    @TestCase
    func removeLastEntry() {
        @On(loadLastEntryInCatalog()).returns(Entry(1, "Test entry", "Test description"))
        drawLastEntryWidget()
    }
}
```

### 桩签名

**桩签名**定义了与特定调用子集匹配的一组条件，包括以下部分：

* mock/spy 对象的引用，必须是单个标识符。（独立声明（顶层或静态函数、变量）不需要此部分）
* 成员以及独立声明的调用。
* 特定格式的参数调用，参见[参数匹配器](#参数匹配器)。

签名可以匹配以下实体：

* 方法
* 属性 getter
* 属性 setter
* 字段读操作
* 字段写操作
* 静态函数
* 静态属性 getter
* 静态 属性 setter
* 静态字段读操作
* 静态字段写操作
* 顶层函数
* 顶层字段读操作
* 顶层字段写操作

只要对应声明被调用，并且所有参数（若有）都与相应的参数匹配器匹配时，桩签名就会匹配调用。

方法的桩的签名结构：`<mock object name>.<method name>(<argument matcher>*)`。

<!--compile.onlyformat-->
```cangjie
@On(foo.method(0, 1)) // 带参数 0 和 1 的方法调用
@On(foo.method(param1: 0, param2: 1)) // 带命名参数的方法调用
```

当桩属性 getter/setter 或字段读/写操作时，使用 `<mock object name>.<property or field name>` 或 `<mock object name>.<property or field name> = <argument matcher>` 。

<!--compile.onlyformat-->
```cangjie
@On(foo.prop) // 属性 getter
@On(foo.prop = 3) // 参数为 3 的属性 setter
```

对于顶层函数和静态函数，签名是类似的：

* 顶层函数：`<function name>(<argument matcher>*)`
* 静态函数：`<class name>.<static method name>(<argument matcher>*)`

顶层变量和静态属性或字段的签名如下：

* 顶层变量：`<top-level variable name>` 或 `<top-level variable name> = <argument matcher>`
* 静态属性或字段：`<class name>.<static property/field name>` 或 `<class name>.<static property/field name> = <argument matcher>`

对运算符函数打桩时，运算符的接收者必须是对 mock/spy 对象的单个引用，而运算符的参数必须是参数匹配器。

<!--compile.onlyformat-->
```cangjie
@On(foo + 3) // 'operator func +'，参数为 3
@On(foo[0]) // 'operator func []'，参数为 0
```

### 参数匹配器

每个桩签名必须包含所有参数的**参数匹配器**。单个参数匹配器定义了一个条件，用于接受所有可能参数值的某个子集。
每个匹配器都是通过调用 `Matchers` 类的静态方法来定义的。
例如 Matchers.any() 是一个允许任何参数的有效匹配器。为了方便起见，提供省略 `Matcher.` 前缀的语法糖。

预定义的匹配器包括：

| 匹配器| 描述| 语法糖|
| ---- | --- | ---- |
| any() | 任何参数| `_` 符号|
| `eq(value: Equatable)` | `value` 结构相等（ structural equality ，对象的值相等，不一定内存相同）的参数| 允许使用单个 `identifier` 和常量字面量|
| `same(reference: Object)` | `reference` 引用相等（referential equality， 对象的引用相等，内存相同）的参数| 允许单个`identifier`|
| `ofType<T>()` | 仅匹配 `T` 类型的值| - |
| `argThat(predicate: (T) -> Bool)` | 仅匹配由 `predicate` 筛选出的 `T` 类型的值| - |
| none()   | 匹配选项类型的 `None` 值| - |

如果使用单个标识符作为参数匹配器，则优先选择结构相等的参数。

如果方法有默认参数，并且没有显式指定该参数，则使用 any() 匹配器。

示例：

<!--compile.onlyformat-->
```cangjie
let p = mock<Printer>() // 假设 print 采用 ToString 类型的单个参数。

@On(p.print(_)) // 可以使用“_”特殊字符代替 any() 。

@On(p.print(eq("foo"))) // 只匹配“foo”参数。
@On(p.print("foo")) // 常量字符串可以省略显式匹配器。

let predefined = "foo" // 可以传递单个标识符，而不是参数匹配器。
@On(p.print(predefined)) // 如果类型相等，则使用结构相等来匹配。

@On(p.print(ofType<Bar>())) // 仅匹配 Bar 类型的参数。

// 对于更复杂的匹配器，鼓励使用以下模式。
let hasQuestionMark = { arg: String => arg.contains("?") }
@On(p.print(argThat(hasQuestionMark))) // 只匹配包含问号的字符串。
```

正确选择函数重载依赖仓颉类型推断机制。可以使用 `ofType` 来解决与类型推断有关的编译时问题。
<!-- 待办：在《桩使用指南》中添加桩重载部分 -->

重要规则：函数调用作为**参数匹配器**时，会视为对匹配器的调用。

```cangjie
@On(foo.bar(calculateArgument())) // 不正确，calculateArgument() 不是匹配器。

let expectedArgument = calculateArgument()
@On(foo.bar(expectedArgument)) // 正确，只要 'expectedArgument' 是可等价的和/或引用类型。
```

### 操作 API

mock 框架提供 API 来指定桩操作。触发桩后，打桩声明会执行指定的操作。如果调用与相应的 `@On` 宏调用指定的签名匹配，则会触发桩。

每个桩函数**必须**指定一个操作。
`@On` 宏调用返回的 `ActionSelector` 子类型会定义可用操作。操作列表取决于所打桩的实体。

<!-- 链接至操作文档 -->

#### 通用（操作）

适用于所有桩的操作。

* `throws(exception: Exception)`：抛出 `exception` 。
* `throws(exceptionFactory: () -> Exception)`：调用 `exceptionFactory` 去构造桩触发时抛出的异常。
* `fails()`：如果触发了桩，则测试失败。

> **注意：**
>
> `throws` 用于测试桩声明抛出异常时的系统行为。`fails` 用于测试桩声明是否未被调用。

<!--compile.onlyformat-->
```cangjie
@On(service.request()).throws(TimeoutException())
```

#### 函数和属性/字段 Getter 和顶层变量读操作

**R** 表示对应成员的返回类型。

* `returns()`：不做任何操作并返回 `()`，仅当 `R` 为 `Unit` 时可用。
* `returns(value: R)`：返回 `value` 。
* `returns(valueFactory: () -> R)`：调用 `valueFactory` 去构造桩触发时抛出的异常。
* `returnsConsecutively(values: Array<R>)`, `returnsConsecutively(values: ArrayList<R>)`：触发桩时，返回 `values` 中的下一个元素。

```cangjie
@On(foo.bar()).returns(2) // 返回 0
@On(foo.bar()).returnsConsecutively(1, 2, 3) // 依次返回 1，2，3
```

#### 属性/字段 Setter 和顶层变量写操作

* `doesNothing()`：忽略调用，不做任何操作。类似于返回 Unit 的函数的 `returns()`。
更多信息详见[这里](./mock_framework_stubs.md#设置属性和字段和顶层变量)。

#### spy 操作

对于 spy 对象，可以使用其他操作来委托监控实例。

* `callsOriginal()` ：调用原始方法。
* `getsOriginal()` ：调用原始属性 getter 或获取原始实例中的字段值。
* `setsOriginal()` ：调用原始属性 setter 或设置原始实例中的字段值。

### 预期

定义桩时会隐式或显式地向桩附加预期。桩**可以**定义期望的基数。**操作**（ `fails` 和 `returnsConcesecutively` 除外）返回`CardinalitySelector` 的实例，该实例可以使用**基数说明符**自定义预期。

**CardinalitySelector** 定义了如下函数：

* `once()`
* `atLeastOnce()`
* `anyTimes()`
* `times(expectedTimes: Int64)`
* `times(min!: Int64, max!: Int64)`
* `atLeastTimes(minTimesExpected: Int64)`

`anyTimes` 说明符用于提升预期，即如果桩从未被触发，测试也不会失败。其他说明符都暗示了测试代码中特定桩的调用次数上下限。只要桩被触发的次数比预期的多，测试就会立即失败。下限在测试代码执行完毕后进行检查。

示例：

<!--run -->
```cangjie
import std.unittest.mock.*
import std.unittest.mock.mockmacro.*

class Foo {
    func bar() { }
}

@Test
func tooFewInvocations() {
    let foo = mock<Foo>()
    @On(foo.bar()).returns().times(2)
    foo.bar()
}
```

输出：

```text
Expectation failed
    Too few invocations for stub foo.bar() declared at example_test.cj:9.
        Required: exactly 2 times
        Actual: 1
        Invocations handled by this stub occured at:
            example_test.cj:6
```

如果没有自定义预期，mock 框架使用默认预期：

| 操作| 默认期望基数| 允许自定义基数|
| ----   |  ---                |  ---                      |
| fails | 不可调用| 否                      |
| returns | atLeastOnce        | 是                      |
| returnsConsecutively | times(values.size)        | 否          |
| throws | atLeastOnce        | 是                       |
| doesNothing | atLeastOnce        | 是                  |
| (calls/gets/sets)Original | atLeastOnce        | 是    |

### 桩链

**returnsConsecutively** 操作，**once** 和 **times(n)** 基数说明符返回一个**续体**实例。顾名思义，**续体**表示可以继续使用链，即指定某操作在前一个操作完全完成时立即执行。

<!-- 链接至续体 -->

**续体**本身只提供了一个返回新 `ActionSelector` 的 `then()` 函数。链上的所有操作都适用相同的规则。如果调用了 `then()` ，则**必须**指定新的操作。

总预期为各个链预期之和。如果在测试中指定了一个复杂的链，那么链的所有部分都会被触发。

<!--compile.onlyformat-->
```cangjie
@On(foo.bar()).returnsConsecutively(1, 2, 3, 4)
// 同下
@On(foo.bar()).returnsConsecutively(1, 2).then().returnsConsecutively(3, 4)
```

```cangjie
// 指定了一个桩，总共必须调用 NUM_OF_RETRIES 次
@On(service.request()).throws(TimeoutException()).times(NUM_OF_RETRIES - 1). // 请求会先超时几次
    then().returns(response).once() // 第一个成功响应之后，停止发送请求
```

## 使用 spy 和 mock 对象

**spy** 对象和 **mock** 对象在配置上是类似的，只不过 spy 对象监控的是当前实例。

主要区别如下：成员调用没有触发任何桩时，spy 对象调用底层实例的原始实现，mock 对象抛出运行时错误（并且测试失败）。

mock 对象无需创建真正的依赖来测试 API ，只需配置特定测试场景所需的行为。

spy 对象支持重写真实实例的可观察行为。只有通过 spy 对象引用的调用才会被拦截。创建 spy 对象对原始 spy 实例的引用无影响。spy 调用自己的方法不会被拦截。

<!--compile.onlyformat-->
```cangjie
let serviceSpy = spy(service)
// 模拟超时，继续使用真正的实现
@On(serviceSpy.request()).throws(TimeoutException()).once().then().callsOriginal()
// 测试代码必须使用'serviceSpy'引用
```

> **注意：**
>
> 静态成员或顶级函数/变量的打桩行为类似于 spy，即对于未打桩的声明，将调用原始成员或原顶级函数/变量，而不是像 mock 中那样抛出异常。

## mock 依赖

接口始终可以被 mock 。从另一个包 mock 一个类时，类本身和它的超类必须按特定方式编译，
即只能 mock 预编译库（如 **stdlib** ）中的接口，不能 mock 类。

### 使用 cjc 编译

对于 **cjc** 来说，mock 是通过 `--mock` 标志来控制的。
如果想 mock 特定包中的类 `p` ，添加 `--mock=on` 标志到 cjc 进行调用。

> **说明：**
>
> 在编译依赖 `p` 的包时，也必须添加此标志。

在测试中使用 mock 对象（ `cjc --test` ）不需要额外的标志。

### 使用 cjpm 编译

**cjpm** 会自动检测 mock 使用，并生成正确的 **cjc** 调用，确保可以从任何从源代码编译的包中 mock 类。

还可以使用 cjpm 配置文件控制哪些包支持 mock 。

<!-- 待办：添加关于默认 mock 行为的章节。-->

<!-- 待办：添加对其他文档的引用。-->