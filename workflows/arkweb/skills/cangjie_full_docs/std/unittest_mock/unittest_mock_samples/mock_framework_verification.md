# mock 框架验证 API

验证 API 是 mock 框架的一部分，其功能如下：

* 验证是否进行了某些调用。
* 验证特定调用的次数。
* 验证是否使用特定参数进行调用。
* 验证调用是否按特定顺序进行。

验证通过检查在执行测试期间构建的调用日志来运行断言。调用日志涵盖让 **mock** 和 **spy** 对象（以及静态成员和顶层函数和顶层变量）在测试中可访问的所有调用。只能验证在 mock/spy 对象（以及静态成员和顶层函数和顶层变量）上进行的调用。

`Verify` 类是验证 API 的入口。
**@Called** 宏用于构建关于代码的断言。

<!-- 链接至验证 API 手册 中的 Verify 类介绍 （自动生成）-->

**@Called** 宏调用构造了一个 **验证语句** ，即根据调用日志检查代码的单个断言。

**Verify** 类本身是静态方法的集合。诸如 `that` 、 `ordered` 、 `unordered` 等方法可构造**验证块**。

## 示例

<!--compile.onlyformat-->
```cangjie
let foo = mock<Foo>()
// 配置 foo
@On(foo.bar()).returns()
foo.bar()
Verify.that(@Called(foo.bar())) // 验证 bar 至少被调用一次
```

## 验证语句和 `@Called` 宏

验证语句由 `VerifyStatement` 类表示。 `VerifyStatement` 实例由 `@Called` 宏创建。

`@Called` 宏调用接受[桩签名](./mock_framework_basics.md#桩签名)，类似于 `@On` 宏，并且适用[参数匹配器](./mock_framework_basics.md#参数匹配器)的规则。

示例：

<!--compile.onlyformat-->
```cangjie
@Called(foo.bar(1, _)) // 匹配 bar 方法调用的验证语句，其中第一个参数为 '1'
@Called(Foo.baz)       // 匹配 baz 静态属性 getter 调用的验证语句
```

`VerifyStatement` 类提供的 API 类似于桩配置时可用的基数说明符。

基数函数为：

* `once()`
* `atLeastOnce()`
* `times(expectedTimes: Int64)`
* `times(min!: Int64, max!: Int64)`
* `atLeastTimes(minTimesExpected: Int64)`
* `never()`

调用这些函数会返回相同的 `VerifyStatement` 实例。同一语句不能重置基数，且必须在语句传递到验证块生成器函数之前设置基数。如果没有显式设置基数，则使用默认基数。

<!--compile.onlyformat-->
```cangjie
Verify.that(@Called(foo.bar()).atLeastOnce())
Verify.that(@Called(foo.bar()).once())
```

## 验证块

验证块通常包含一个或多个验证语句，且检查块中的语句会构成更复杂的断言。

在调用验证块时会立即验证，不验证之后发生的任何调用。

验证块不会改变调用日志的状态：日志中的每个调用都可以被任意数量的块检查。独立检查各个块，前后块之间没有依赖关系。除非在块之间发生了一些调用，或者手动清除了调用日志，否则调用验证块的顺序并不重要。

验证语句本身不执行任何类型的验证，必须传递到验证块中进行验证。

单个验证块仅检查在块内验证语句中提到的 mock/spy 对象上的调用，忽略对其他对象的调用。

`Verify` 类包含几个构建验证块的静态方法。**有序**验证块用于检查调用的确切顺序。**无序**验证块只验证调用的次数。

### 有序

如需检查一个或多个对象的调用顺序，使用 `ordered` 验证块生成器。

`ordered` 静态函数接收一个验证语句数组。

<!--compile.onlyformat-->
```cangjie
for (i in 0..4) {
    foo.bar(i % 2)
}

Verify.ordered(
    @Called(foo.bar(0)),
    @Called(foo.bar(1)),
    @Called(foo.bar(0)),
    @Called(foo.bar(1))
)
```

允许检查多个对象的调用顺序。

<!--compile.onlyformat-->
```cangjie
for (i in 0..4) {
    if (i % 2 == 0) {
        fooEven.bar(i)
    } else {
        forOdd.bar(i)
    }
}

Verify.ordered(
    @Called(fooEven.bar(0)),
    @Called(fooOdd.bar(1)),
    @Called(fooEven.bar(2)),
    @Called(fooOdd.bar(3)),
)
```

**有序**验证的默认基数说明符是 `once()` 。如有需要，可使用其他基数说明符。

<!--compile.onlyformat-->
```cangjie
for (i in 0..4) {
    foo1.bar(i)
}

for (i in 0..4) {
    foo2.bar(i)
}

Verify.ordered(
    @Called(foo1.bar(_).times(4)),
    @Called(foo2.bar(_).times(4))
)
```

对于**有序**验证，须列出对（块中提到的） mock/spy 对象的所有调用。任何未列出的调用都会导致验证失败。

<!--compile.onlyformat-->
```cangjie
foo.bar(0)
foo.bar(10)
foo.bar(1000)

Verify.ordered(
    @Called(foo.bar(0)),
    @Called(foo.bar(10))
)
```

输出：

```text
验证失败
    以下调用未匹配到任何语句：
        foo.bar(...) at example_test.cj:6
```

### 无序

无序验证只检查其验证语句的调用次数。

对于**无序**验证，除非显式指定，否则使用 `atLeastOnce()` 基数，即检查至少进行了一次的调用。

<!--compile.onlyformat-->
```cangjie
for (i in 0..4) {
    foo.bar(i % 2)
}

// 验证是否至少调用了一次使用参数 0 和参数 1 的 bar
Verify.unordered(
    @Called(foo.bar(0)),
    @Called(foo.bar(1))
)

// 验证是否调用了两次使用参数 0 和参数 1 的 bar
Verify.unordered(
    @Called(foo.bar(0)).times(2),
    @Called(foo.bar(1)).times(2)
)

// 验证是否总共调用了四次 bar
Verify.unordered(@Called(foo.bar(_)).times(4))
```

**无序**验证包括 **Partial** 和 **Exhaustive** 。

默认为 **Exhaustive** ，需要列出验证语句所提到的 mock/spy 对象的所有调用。
**Partial** 只列出**部分**调用。

<!--compile.onlyformat-->
```cangjie
for (i in 0..4) {
    foo.bar(i)
}

// 失败，foo.bar() 的两次调用未在块中列出
Verify.unordered(
    @Called(foo.bar(0)).once(),
    @Called(foo.bar(1)).once()
)

// 忽略无关调用
Verify.unordered(
    Partial,
    @Called(foo.bar(0)).once(),
    @Called(foo.bar(1)).once()
)
```

### 动态构建验证块

`ordered` 和 `unordered` 函数为接受 lambda 的重载函数。可使用 `checkThat(statement: VerifyStatement)` 函数动态添加语句。

示例：

<!--compile.onlyformat-->
```cangjie
let totalTimes = 40
for (i in 0..totalTimes) {
    foo.bar(i % 2)
}

Verify.ordered {
    v => for (j in 0..totalTimes) {
        v.checkThat(@Called(foo.bar(eq(j % 2))))
    }
}
```

## 其他 API

另外，`Verify` 类还提供了以下工具。

* that(statement: VerifyStatement) 为 Verify.unordered(Paritial, statement) 的别名，用于检查单个语句，不需要列出对应 mock/spy 对象的所有调用。
* noInteractions(mocks: Array\<Object>) 用于检查没有进行调用的 mock/spy 对象。
* `clearInvocationLog()` 将日志重置为空状态。这会影响后面的所有验证块，但并不影响桩预期。

示例：

<!--compile.onlyformat-->
```cangjie
foo.bar()
Verify.that(@Called(foo.bar())) // OK
Verify.noInteractions(foo)      // 失败，foo.bar() 调用在日志中
Verify.clearInvocationLog()     // 清除日志
Verify.noInteractions(foo)      // 从日志中清除所有与 foo 的交互
Verify.that(@Called(foo.bar())) // 失败
```

## `Verify` 类 API

<!--compile.onlyformat-->
```cangjie
public class Verify {
    public static func that(statement: VerifyStatement): Unit

    public static func unordered(
        exhaustive: Exhaustiveness,
        collectStatements: (UnorderedVerifier) -> Unit
    ): Unit

    public static func unordered(
        collectStatements: (UnorderedVerifier) -> Unit
    ): Unit

    public static func unordered(statements: Array<VerifyStatement>): Unit

    public static func unordered(
        exhaustive: Exhaustiveness,
        statements: Array<VerifyStatement>
    ): Unit

    public static func ordered(
        collectStatements: (OrderedVerifier) -> Unit
    ): Unit

    public static func ordered(statements: Array<VerifyStatement>): Unit

    public static func clearInvocationLog(): Unit

    public static func noInteractions(mocks: Array<Object>): Unit
}
```

## 验证错误

验证失败时，会抛出 `VerificationFailedException` ，mock 框架会给出报告。不要捕获该异常。

失败类型如下：

* **调用次数太少**或**调用次数太多**：调用次数与块中的语句不匹配。
* **语句不匹配**：块中存在与日志中的调用不匹配的语句。
* **调用不匹配**：日志中存在与块中的语句不匹配的调用。
* **意外调用**：**有序**验证块需要的是其他的调用。
* **无用交互**： **noInteractions** 检测到意外调用。

还有另一种失败类型**不相交的语句**，不一定是测试代码本身有问题。调用匹配到多个语句时，就会上报这种失败类型。在单个验证块中使用具有不相交参数匹配器的语句可能会导致此错误。不允许在语句和调用之间进行模糊匹配。

## 示例和模式

使用验证 API 的常见模式是验证测试代码（无论是函数、类还是整个包）与外部对象之间的交互。
如下所示：

* 创建 **spy** 对象。
* 将这些 spy 对象传递给测试代码。
* 验证代码和 spy 对象之间的交互。

### 验证调用数量

<!--compile.onlyformat-->
```cangjie
import std.unittest.mock.*
import std.unittest.mock.mockmacro.*

func testDataCaching() {
    // 创建必要的 spy 或 mock 对象
    let uncachedRepo = spy(Repository())
    let invalidationTracker = mock<InvalidationTracker>()
    @On(invalidationTracker.getTimestamp()).returns(0)

    // 准备测试数据
    let cachedRepo = CachedRepistory(uncachedRepo, invalidationTracker)

    // 运行测试代码
    for (i in 0..10) {
        cachedRepo.get(TEST_ID)
    }

    // 验证得出只查询了一次基础 repo，没有对未缓存 repo 的其他调用
    Verify.unordered(
        Exhaustive,
        @Called(uncachedRepo.get(TEST_ID)).once()
    )

    // 清除日志
    Verify.clearInvocationLog()

    // 设置其他行为
    @On(invalidationTracker.getTimestamp()).returns(1)

    for (i in 0..10) {
        cachedRepo.get(TEST_ID)
    }

    // 自上次清除后只进行了一次调用
    Verify.unordered(
        Exhaustive,
        @Called(uncachedRepo.get(TEST_ID)).once()
    )
}
```

### 验证带特定参数的调用

<!--compile.onlyformat-->
```cangjie
import std.unittest.mock.*
import std.unittest.mock.mockmacro.*

func testDrawingTriangle() {
    // 创建必要的 spy 或 mock 对象
    let canvas = spy(Canvas())

    // 运行代码
    canvas.draw(Triangle())

    // 测试三角形由 3 条线和 3 个点组成

    // 使用 'that' 块
    Verify.that(@Called(canvas.draw(ofType<Dot>())).times(3))
    Verify.that(@Called(canvas.draw(ofType<Line>())).times(3))

    // 或者使用部分无序验证块

    Verify.unordered(
        Partial, // 未知线条和点实际绘制的顺序
        @Called(canvas.draw(ofType<Dot>())).times(3),
        @Called(canvas.draw(ofType<Line>())).times(3)
    )

    // 使用枚举块时，必须枚举出所有调用
    Verify.unordered(
        Exhaustive,
        @Called(canvas.draw(ofType<Triangle>())).once(),
        @Called(canvas.draw(ofType<Dot>())).times(3),
        @Called(canvas.draw(ofType<Line>())).times(3)
    )

    // 验证用例从未调用入参为 Square 类型的 draw 函数
    Verify.that(@Called(canvas.draw(ofType<Square>)).never())

    // 如果想通过更复杂的条件来区分参数
    // 可以使用下面的模式
    let isDot = {
        f: Figure => f is Dot // 此为更复杂的逻辑
    }

    Verify.that(@Called(canvas.draw(argThat(isDot))).times(3))

    // 注意，属于同一个块的语句必须明确只匹配了一个调用
    // 以下为反例，有些调用匹配了两个语句
    Verify.unordered(
        @Called(canvas.draw(_)).times(7),
        @Called(canvas.draw(ofType<Dot>())).times(3)
    )
}
```

### 验证调用顺序

<!--compile.onlyformat-->
```cangjie
import std.unittest.mock.*
import std.unittest.mock.mockmacro.*

func testBuildFlight() {
    let plane = spy(Plane())

    FlightBuilder(plane).planFlight(Shenzhen, Shanghai, Beijing).execute()

    Verify.ordered(
        @Called(plane.takeOffAt(Shenzhen)),
        @Called(plane.landAt(Shanghai)),
        @Called(plane.takeOffAt(Shanghai)),
        @Called(plane.landAt(Beijing))
    )
}
```

## 预期与验证 API

配置桩时，可以设置**预期**和验证 API 覆盖测试代码的一些断言。这种情况别无他法，只能选择更能反映测试意图的方法。

一般情况下，建议避免重复验证块中的配置步骤。

<!--compile.onlyformat-->
```cangjie
let foo = mock<Foo>()
@On(foo.bar(_)).returns() // 如果从未使用此桩，测试失败

foo.bar(1)
foo.bar(2)

Verify.that(
    // 不需要，自动验证
    @Called(foo.bar(_)).atLeastOnce()
)

// 但可以检查调用的数量和具体的参数
Verify.unordered(
    @Called(foo.bar(1)).once(),
    @Called(foo.bar(2)).once()
)
```

上面的示例可以使用预期重写：

<!--compile.onlyformat-->
```cangjie
let foo = mock<Foo>()
@On(foo.bar(1)).returns().once() // 预期只被调用一次，参数为`1`
@On(foo.bar(2)).returns().once() // 预期只被调用一次，参数为`2`

foo.bar(1)
foo.bar(2)

// 如果没有桩被触发，则测试失败
```
