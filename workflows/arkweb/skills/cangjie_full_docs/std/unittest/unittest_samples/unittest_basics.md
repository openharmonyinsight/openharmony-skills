# Unittest 基础概念及用法

## 测试及测试用例

测试是用 `@Test` 宏标记的实体，会在测试过程中执行。
仓颉 unittest 框架中有两种测试：测试类和测试函数。
测试函数相对简单，每个函数包含全部测试运行的代码。
测试类适用于为测试引入更深层次的结构，或者覆盖[测试生命周期行为](#测试生命周期)的场景。

每个测试类由若干个测试用例组成，每个测试用例用 `@TestCase` 宏标记。
每个测试用例都是测试类内部的一个函数。
上一节中的示例，相同的测试可以改写为如下所示的测试类：

<!-- run -->
```cangjie
func add(a: Int64, b: Int64) {
    a + b
}
@Test
class AddTests {
    @TestCase
    func addTest() {
        @Expect(add(2, 3), 5)
    }

    @TestCase
    func addZero() {
        @Expect(add(2, 0), 2)
    }
}
```

测试函数即函数中包含单个测试用例的测试。这种情况下不需要使用 `@TestCase` 宏。

`cjpm test` 中运行这个新的测试类会生成如下类似输出：

```text
--------------------------------------------------------------------------------------------------
TP: example/example, time elapsed: 67369 ns, Result:
    TCS: AddTests, time elapsed: 31828 ns, RESULT:
    [ PASSED ] CASE: addTest (25650 ns)
    [ PASSED ] CASE: addZero (4312 ns)
    Summary: TOTAL: 2
    PASSED: 2, SKIPPED: 0, ERROR: 0
    FAILED: 0
--------------------------------------------------------------------------------------------------
cjpm test success
```

## 断言

断言是在测试用例函数体内执行的单个条件检查，用以判断代码是否正常运行。
断言有两种：`@Expect` 和 `@Assert` 。
创建一个错误的测试来说明两者的区别：

<!-- run -->
```cangjie
func add(a: Int64, b: Int64) {
    a + b
}
@Test
func testAddIncorrect() {
    @Expect(add(3, 3), 5)
}
```

运行测试失败，并生成以下结果（仅展示与此测试相关的部分）：

```text
    TCS: TestCase_testAddIncorrect, time elapsed: 4236 ns, RESULT:
    [ FAILED ] CASE: testAddIncorrect (3491 ns)
    Expect Failed: `(add ( 3 , 3 ) == 5)`
       left: 6
      right: 5
```

在这个例子中，用 `@Assert` 替换 `@Expect` 不会有什么变化。添加一个检查项后，再次运行：

<!-- run -->
```cangjie
func add(a: Int64, b: Int64) {
    a + b
}
@Test
func testAddIncorrect() {
    @Expect(add(3, 3), 5)
    @Expect(add(5, 3), 9)
}
```

运行测试失败，并生成以下结果（仅展示与此测试相关的部分）：

```text
    TCS: TestCase_testAddIncorrect, time elapsed: 5058 ns, RESULT:
    [ FAILED ] CASE: testAddIncorrect (4212 ns)
    Expect Failed: `(add ( 3 , 3 ) == 5)`
       left: 6
      right: 5

    Expect Failed: `(add ( 5 , 3 ) == 9)`
       left: 8
      right: 9
```

可以在输出中看到这两个检查的结果。
但是，如果用 `@Assert` 替换 `@Expect` ：

<!-- run -->
```cangjie
func add(a: Int64, b: Int64) {
    a + b
}
@Test
func testAddIncorrectAssert() {
    @Assert(add(3, 3), 5)
    @Assert(add(5, 3), 9)
}
```

可以得到以下输出：

```text
    TCS: TestCase_testAddIncorrectAssert, time elapsed: 31653 ns, RESULT:
    [ FAILED ] CASE: testAddIncorrectAssert (30893 ns)
    Assert Failed: `(add ( 3 , 3 ) == 5)`
       left: 6
      right: 5
```

可以看到，只有第一个 `@Assert` 检查失败了，其余的测试甚至都没有运行。
这是因为 `@Assert` 宏采用的是快速失败（*fail-fast*）机制：一旦首次断言失败，整个测试用例都失败，后续的断言不再检查。

在涉及大量断言的大型测试中，这一点非常重要，尤其是在循环中使用断言时。
并不需要等到全部失败，首次失败后用户即可感知。

在测试中选择 `@Assert` 还是 `@Expect` 取决于测试场景的复杂程度，以及是否需要采用快速失败机制。

使用 `unittest` 提供的两种断言宏时，可采用如下方式：

- 相等断言，其中 `@Assert(a, b)` 或 `@Expect(a, b)` 的两个参数 `a` 和 `b` ，检查它们的参数值是否相等；假设 `a` 的类型为 `A` ， `b` 的类型为 `B` ， `A` 必须实现了 Equatable\<B> 。
- 布尔断言 `@Assert(c)` 或 `@Expect(c)` ，其参数 `c` 为 `Bool` 类型，参数值 `true` 或 `false` 。

断言的第二种形式 `@Assert(c)` 可以视为 `@Assert(c, true)` 的简写形式。

<!-- TODO: @PowerAssert -->

### 失败断言

失败断言可以让测试用例运行失败。`@Fail` 采用快速失败机制，运行至此断言则整个测试用例失败，后续断言都不再检查。`@FailExpect` 运行至此断言会使得用例失败，但后续断言依然会被检查。
前述宏的参数为描述失败原因的字符串，`@Fail` 的返回值类型为 `Nothing` ， `@FailExpect` 的类型为 `Unit` 。

举例来说：

<!-- run -->
```cangjie
import std.time.*

func generateRandomEven(): Int64 {
    return DateTime.now().nanosecond
}

@Test
func validate_even_number_generator() {
    let even = generateRandomEven()
    if (even % 2 == 1) {
        @Fail("Not even number was generated: ${even}")
    }
}
```

会输出如下错误信息：

```text
    [ FAILED ] CASE: validate_even_number_generator (54313 ns)
    Assert Failed: `(Not even number was generated: 111)`
```

### 预期异常的断言

运行至此断言当预期抛出的异常类型未被抛出时，用例将失败，`@AssertThrows` 将不再进行后续检查，而 `@ExpectThrows` 将继续检查。
前述宏的属性入参为预期抛出的异常类型列表，通过 `|` 隔离不同异常类型，当没有属性入参时预期抛出异常基类 `Exception` 。入参为预期抛出异常的表达式或代码块。

举例来说：

```cangjie
// No.1
@AssertThrows(throw Exception())
 
// 语义上与 No.1 相同
@AssertThrows[Exception](throw Exception())
 
@AssertThrows[IllegalStateException | NoneValueException](random.seed = 42u64)
 
@ExpectThrows[OutOfMemoryError](foo())
 
@ExpectThrows({
    foo()
    boo()
})
 
@ExpectThrows[OutOfMemoryError]({
    for (i in list) {
        foo(i)
    }
})
```

#### `@AssertThrows` 的返回类型

如果指定的异常不超过一个，则返回类型与预期抛出的异常类型相同：

```cangjie
let e: NoneValueException = @AssertThrows[NoneValueException](foo())
```

如果指定的异常超过一个，则返回类型为预期抛出的异常类型的最小公共超类型：

```cangjie
// A <: C
// B <: C
let e: C = @AssertThrows[A | B](foo())
```

#### `@ExpectThrows` 的返回类型

`@ExpectThrows` 检查失败后也会继续执行，在指定的异常不超过一个时，它返回的类型是 Option\<T>，其中 `T` 是预期的异常类型：

```cangjie
let e: ?NoneValueException = @ExpectThrows[NoneValueException](foo())
```

在指定的异常超过一个时，返回的类型是 ?Exception ：

```cangjie
let e: ?Exception = @ExpectThrows[NoneValueException | IllegalMemoryException](foo())
```

#### 近似相等

一些被比较的参数类型可能不能准确计算，例如浮点数，此时我们可以使用近似计算获得其是否相等的结果。

本包提供了近似计算相关的接口 [NearEqutable](../unittest_package_api/unittest_package_interfaces.md#interface-nearequatablect-d) ，对于需要判断近似相等的类型，可通过扩展该接口，并在 `@Assert` `@Expect` `@PowerAssert` 等宏中使用 delta 参数，使能近似相等功能。

近似相等的计算逻辑如下：

```text
a <= b with delta <=> a.isNear(b, delta) || a <= b
a >= b with delta <=> a.isNear(b, delta) || a >= b
a != b with delta <=> !a.isNear(b, delta)
a == b with delta <=> a.isNear(b, delta)
a < b with delta <=> !a.isNear(b, delta) && a < b
a > b with delta <=> !a.isNear(b, delta) && a > b
```

对于浮点类型，还提供了相对的 delta 结构 [RelativeDelta](../unittest_package_api/unittest_package_structs.md#struct-relativedeltat):

示例如下：

<!-- run -->
```cangjie
// 基础类型
@Test
func test1() {
    @Expect(1.0, 1.001, delta: 0.001) // 解糖为 @Expect(1.0 == 1.001, delta: 0.001)
    @Expect(1.0 == 1.001, delta: 0.001)
    @Expect(1.0 != 1.901, delta: RelativeDelta(absoluteDelta: 0.001, relativeDelta: 0.02))
    @Expect(1.0 < 1.401, delta: 0.001)
}
// 自定义类型
class Point <: NearEquatable<Point, Point> {
    Point(let x: Int64, let y: Int64) { }

    public func isNear(obj: Point, delta: Point): Bool {
        if (x < 0 || y < 0) {
            throw IllegalArgumentException("Coordinates must be non negative. Actual: ($x, $y)")
        }
        abs(x - obj.x) < delta.x && abs(y - obj.y) < delta.y
    }
}

// 测试用例
@Test
func test() {
    let p1 = Point(1, 5)
    let p2 = Point(5, 5)
    let delta = Point(1, 1)

    @Expect(p1 != p2, delta: delta)
}
```

## 测试生命周期

测试用例之间有时可以共享创建或清理代码。测试框架支持 4 个生命周期步骤，分别通过相应的宏来设置。只能为 `@Test` 测试类指定生命周期步骤，不能为 `@Test` 顶层函数指定生命周期步骤。

| 宏 | 生命周期 |
| ---  | --- |
| @BeforeAll | 在所有测试用例之前运行 |
| @BeforeEach | 在每个测试用例之前运行一次 |
| @AfterEach | 在每个测试用例之后运行一次 |
| @AfterAll | 在所有测试用例完成后运行 |

这些宏必须配置在 `@Test` 测试类的成员或静态函数上。`@BeforeAll` 和 `@AfterAll` 函数不能声明任何参数。 `@BeforeEach` 和 `@AfterEach` 函数可以声明一个 `String` 类型的参数（或者不声明参数）。

<!-- run -->
```cangjie
@Test
class FooTest {
    @BeforeAll
    func setup() {
        // 在测试执行前运行这段代码。
    }
}
```

每个宏可以应用于单个测试类内的多个函数。可以在单个函数上配置多个生命周期宏。生命周期宏不能配置在标有 `@TestCase` 或类似宏的函数上。

如果多个函数被标记为相同的生命周期步骤，则可以按照它们在代码中声明的顺序（从上到下）执行。

测试框架确保：

1. 标记为 **Before all** 的步骤在所有测试用例运行之前，至少运行一次。
2. 对于测试类中的每个测试用例 `TC` ：
    1） 标记为 **Before each** 的步骤在 `TC` 之前运行一次。
    2） 运行 `TC` 。
    3） 标记为 **After each** 的步骤在 `TC` 之后运行一次。
3. 在测试类中的所有测试用例之后运行标记为 **After all** 的步骤。

> **注意：**
>
> 如果没有运行测试用例，上述并不适用。

简单场景中，标识为 **before all** 和 **after all** 的步骤只运行一次。但也有例外：

<!-- TODO: link parallel running -->
- 对于[类型参数化测试](./unittest_parameterized_tests.md#类型参数化测试)，标识为 **before/after all** 的步骤运行的数量为每个类型参数的组合数。
- 如果多个测试用例在不同的进程中并行执行，则每个进程中标识为 **before/after all** 的步骤都将运行一次。

`@BeforeEach` 和 `@AfterEach` 可以访问正在创建或删除的测试用例，只需要在相应的函数中指定一个 `String` 类型的参数即可。

<!-- run -->
```cangjie
@Test
class Foo {
    @BeforeEach
    func prepareData(testCaseName: String) {
        // 测试用例函数的名称作为参数
        // 本例中的"bar"
    }

    @AfterEach
    func cleanup() {
        // 不指定参数也可以
    }

    @TestCase
    func bar() {}
}
```

为[参数化测试](./unittest_parameterized_tests.md)或参数化性能测试配置生命周期时，注意标识为 **before each** 或 **after each** 的步骤仅在执行测试用例或基准之前或之后为其所有参数执行一次。也就是说，从生命周期的角度看，使用不同参数执行多次的测试主体会被视为单个测试用例。

如果参数化测试的每个参数都需要单独创建清理，需要将相应的代码配置在测试用例主体本身中。此外，还可以访问参数本身。

<!-- TODO: mention and link how to do setup/teardown per parameter in benchmarks -->

## 测试配置

单元测试框架中其他更高级的功能可能需要额外配置。
参考如下三种方式配置测试：

- 使用 `@Configure` 宏
- 直接在运行测试时或在 `cjpm test` 测试中使用命令行参数
- 使用 `cjpm` 配置文件

<!-- TODO: configuration conversion algorithm -->

## 运行配置

### 使用方法

运行 cjc 编译的可执行文件 test ，添加参数选项

```shell
./test --bench --filter=MyTest.*Test,-stringTest
```

### `--bench`

默认情况下，只有被 `@TestCase` 修饰的函数会被执行。在使用 `--bench` 的情况下只执行 `@Bench` 宏修饰的用例。

### `--filter`

如果您希望以测试类和测试用例过滤出测试的子集，可以使用 `--filter=测试类名.测试用例名` 的形式来筛选匹配的用例，例如：

1. `--filter=*` 匹配所有测试类
2. `--filter=*.*` 匹配所有测试类所有测试用例（结果和*相同）
3. `--filter=*.*Test,*.*case*` 匹配所有测试类中以 Test 结尾的用例，或者所有测试类中名字中带有 case 的测试用例
4. `--filter=MyTest*.*Test,*.*case*,-*.*myTest` 匹配所有 MyTest 开头测试类中以 Test 结尾的用例，或者名字中带有 case 的用例，或者名字中不带有 myTest 的测试用例

### `--dry-run`

执行单元测试框架而不实际运行测试。可用于查看测试用例列表。

### `--include-tags`

若需按 [`@Tag`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#tag-宏) 宏中指定的类别选择测试的子集，则可使用 `--include-tags` 或 `--exclude-tags` 运行选项。例如：

1. `--include-tags=Unittest` 运行所有的带有 `@Tag[Unittest]` 的测试用例。
2. `--include-tags=Unittest,Smoke` 运行所有的带有 `@Tag[Unittest]`和/或`@Tag[Smoke]` 的测试用例。
3. `--include-tags=Unittest+Smoke` 运行所有的带有 `@Tag[Unittest]`和`@Tag[Smoke]` 的测试用例。
4. `--include-tags=Unittest+Smoke+JiraTask3271,Backend` 运行所有的带有 `@Tag[Backend]`和/或`@Tag[Unittest, Smoke, JiraTask3271]` 的测试用例。

> **注意：**
>
> 如果没有符合指定标签类别的测试用例。框架将不运行任何内容。
> 可以与 `exclude-tags` 结合。详见 [`--exclude-tags`](./unittest_basics.md#--exclude-tags)。

### `--exclude-tags`

若需按 [`@Tag`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#tag-宏) 宏中指定的类别选择测试的子集，则可使用 `--include-tags` 或 `--exclude-tags` 运行选项。例如：

1. `--exclude-tags=Unittest` 运行所有的**未**带有 `@Tag[Unittest]` 的测试用例。
2. `--exclude-tags=Unittest,Smoke` 运行所有的**未**带有 `@Tag[Unittest]`和/或`@Tag[Smoke]` 的测试用例。
3. `--exclude-tags=Unittest+Smoke` 运行所有的**未**同时带有 `@Tag[Unittest]`、`@Tag[Smoke]` 的测试用例。
4. `--include-tags=Unittest --exclude-tags=Smoke` 运行所有带有 `@Tag[Unittest]` 但不带有 `@Tag[Smoke]` 的测试用例。

> **注意：**
>
> `exclude-tags` 的优先级高于 `include-tags`，如果用例被排除，则必定不会被执行，例如 `--include-tags=Unittest+Smoke --exclude-tags=Smoke` 则带有 `@Tag[Smoke]` 的用例不会被执行。

### `--show-tags`

若需要在测试报告中显示测试用例中 [`@Tag`](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#tag-宏) 的信息，可使用 `--show-tags` 运行选项。

在 `--dry-run` 模式下，并且测试报告为 `xml` 格式时，将始终包含 `Tag` 信息。

### `--timeout-each=timeout`

使用 `--timeout-each=timeout` 选项等同于对所有的测试类使用 `@Timeout[timeout]` 修饰。若代码中已有 `@Timeout[timeout]` ，则将被代码中的超时时间覆盖，即选项的超时时间配置优先级低于代码中超时时间配置。

`timeout` 的值应符合以下语法：
    `number ('millis' | 's' | 'm' | 'h')`
例如： `10s`, `9millis` 等。

- millis: 毫秒
- s: 秒
- m: 分钟
- h: 小时

### `--parallel`

打开 `--parallel` 选项将使测试框架在单独的多个进程中并行执行不同的测试类。
测试类之间应该是相互独立的，不依赖于共享的可变的状态值。
程序静态初始化可能会发生多次。
不允许与 `--bench` 同时使用。由于性能用例对底层资源敏感，用例是否并行执行，将影响性能用例的结果，因此禁止与 `--bench` 同时使用。

- `--parallel=<BOOL>` `<BOOL>` 可为 `true` 或 `false` ，指定为 `true` 时，测试类可被并行运行，并行进程个数将受运行系统上的 CPU 核数控制。另外，`--parallel` 可省略 `=true` 。
- `--parallel=nCores` 指定了并行的测试进程个数应该等于可用的 CPU 核数。
- `--parallel=NUMBER` 指定了并行的测试进程个数值。该数值应该为正整数。
- `--parallel=NUMBERnCores` 指定了并行的测试进程个数值为可用的 CPU 核数的指定数值倍。该数值应该为正数（支持浮点数或整数）。

### `--option=value`

以 `--option=value` 形式提供的任何非上述的选项均按以下规则处理并转换为配置参数（类似于 `@Configure` 宏处理的参数），并按顺序应用：

`option` 与 `value` 为任意自定义的运行配置选项键值对，`option` 可以为任意通过 `-` 连接的英文字符，转换到 `@Configure` 时将转换为小驼峰格式。`value` 的格式规则如下：

注：当前未检查 `option` 与 `value` 的合法性，并且选项的优先级低于代码中 `@Configure` 的优先级。

- 如果省略 `=value` 部分，则该选项被视为 `Bool` 值 `true` ， 例如：`--no-color` 生成配置条目 `noColor = true` 。
- 如果 `value` 严格为 `true` 或 `false` ，则该选项被视为具有相应含义的 `Bool`值：`--no-color=false` 生成配置条目 `noColor = false` 。
- 如果 `value` 是有效的十进制整数，则该选项被视为 `Int64` 值 ， 例如：`--random-seed=42` 生成配置条目 `randomSeed = 42` 。
- 如果 `value` 是有效的十进制小数，则该选项被视为 `Float64` 值 ， 例如：`--angle=42.0` 生成配置条目 `angle = 42` 。
- 如果 `value` 是带引号的字符串文字（被 `"` 符号包围），则该选项将被视为 `String` 类型，并且该值是通过解码 `"` 符号之间的字符串值来生成的，并处理转义符号，例如 `\n`、`\t`、`\"` 作为对应的字符值。例如，选项 `--mode="ABC \"2\""` 生成配置条目 `mode = "ABC \"2\""`；
- 除上述情况外 `value` 值将被视为 `String` 类型，该值从所提供的选项中逐字获取。例如， `--mode=ABC23[1,2,3]` 生成配置条目 `mode = "ABC23[1,2,3]"`。

### `--report-path=path`

该选项用于指定执行后生成测试报告的目录路径。默认情况下，如果不明确指定选项，将不会生成报告。

### `--report-format=value`

该选项用于指定测试执行后生成的报告的格式。

目前，单元测试仅支持默认的 xml 格式。

基准测试支持：

- `csv`：csv 报告中有统计数据。
- `csv-raw`： csv-raw 报告中只有批次的原始测量值。
- `html`：html 报告包含显示的所有结果和各种统计属性。可以在任何浏览器中查看。对于每个基准测试函数，html 报告包含：
    - 每个基准参数的摘要。
    - 执行环境相关信息的汇总，例如硬件信息、操作系统信息、编译信息、环境变量。
    - 每个基准参数的选项卡包含详细的统计信息。
    - 核密度估计图。这是对基准函数的单次执行实际花费的时间的概率估计。
    - 原始测量值及其线性回归图。
    - 具有统计属性（例如平均值、中位数、R 平方、框架开销、标准差）及其置信区间的表。

基准测试的默认使用的格式为：

- `csv`

### `--baseline-path=path`

此选项指定用于比较的性能报告所在的路径。默认情况下，使用 ['--report-path'](#--report-pathpath) 的值。

### `--capture-output`

此选项使能测试用例的打印输出捕获。
默认情况下，在 `cjpm test` 执行时使能捕获，否则禁用捕获。
当测试用例打印输出捕获未使能时，打印输出将立即传播到单元测试输出。否则，单元测试将收集和处理测试用例的打印输出。

需要捕获打印输出的场景如下：

- 使用 `--parallel` 执行时防止测试输出交错。
- 隐藏已通过测试的输出以使单元测试报告更加清晰。
- 将每个测试用例的输出分开，以查看哪个测试用例打印了什么。

### `--no-capture-output`

此选项禁用测试用例打印输出捕获。
默认情况下，在 `cjpm test` 执行中启用捕获，否则禁用捕获。

使测试用例打印输出立即传播到单元测试输出。

### `--show-all-output`

单元测试框架将打印报告中的所有输出，包括通过的测试用例的输出。
如果禁用测试输出捕获，则此选项失效。

### `--coverage-guided`

单元测试框架将使能[覆盖率引导的随机参数化测试](./unittest_parameterized_tests.md#覆盖率引导的随机参数化测试)。

### `--progress-brief`

启用单元测试的简短（单行）动态进度报告。

### `--progress-entries-limit=limit`

限制进度输出中显示的最大条目数。 `limit` 的合法值：非负整数值。
值 `0` 表示没有限制。默认值：无限制。

### `--no-progress`

禁用动态进度报告。
如果指定选项 `--dry-run`，则隐含选项 `--no-progress`。
