# 参数化测试

## 参数化测试入门

仓颉 unittest 框架支持参数化测试，格式为*数据 DSL* ，测试中框架自动插入输入参数。

以对标准库的 sort 接口测试为例：

<!-- run -->
```cangjie
import std.sort.*

@Test
func testSort() {
    let arr = [45, 5, -1, 0, 1, 2]
    sort(arr)
    @Expect(arr, [-1, 0, 1, 2, 5, 45])
}
```

测试结果显示，函数在单个输入的情况下可用。
接下来测试，如果数组只包含等值元素，排序函数还是否可用。

<!-- run -->
```cangjie
import std.sort.*

@Test
func testAllEqual() {
    let arr = [0, 0, 0, 0]
    let expected = [0, 0, 0, 0]
    sort(arr)
    @Expect(expected, arr)
}
```

测试结果显示函数可用，但还是不能确认是否适用于所有大小的数组。
接下来测试参数化数组的大小。

<!-- run -->
```cangjie
import std.sort.*

@Test[size in [ 0, 1, 50, 100, 1000 ]]
func testAllEqual(size: Int64) {
    let arr = Array(size, repeat: 0)
    let expected = Array(size, repeat: 0)
    sort(arr)
    @Expect(expected, arr)
}
```

至此，参数化测试已完成。
这种是最简单的参数化测试，即值驱动测试，直接在代码中列出测试运行的值。
参数化测试的参数可以不止一个。
不仅可以指定排序函数的大小，还可以指定待测试的元素。

<!-- run -->
```cangjie
import std.sort.*

@Test[size in [ 0, 1, 50, 100, 1000 ],
 item in(- 1 .. 20)
]
func testAllEqual(size: Int64, item: Int64) {
    let arr = Array(size, repeat: item)
    let expected = Array(size, repeat: item)
    sort(arr)
    @Expect(expected, arr)
}
```

注意，`item` 的取值范围为 `-1..20` ，不是一个数组。
那么，运行这个测试，结果会如何？
参数 `size` 和 `item` 的取值会进行组合再测试和返回结果。
因此，测试函数时，不要配置过多参数；否则组合数量过大，导致测试变慢。
上述例子中，`size` 参数值有 5 个，`item` 参数值有 21 个，共有 21×5=105 种组合。

注意，值驱动测试不限于整型或内置类型。
也可以和任何仓颉类型一起使用。
参考如下测试：

<!-- run -->
```cangjie
@Test[array in [
 [ ],
 [ 1, 2, 3 ],
 [ 1, 2, 3, 4, 5 ],
 [ 5, 4, 3, 2, 1 ],
 [ -1, 0 ],
 [ -20 ]
 ]
]
func testDifferentArrays(array: Array<Int64>) {
    // 测试数组是否已排序
    for (i in 0..(array.size - 1)) {
        @Expect(array[i] <= array[i + 1])
    }
}
```

这里，直接以参数的形式提供测试的数据。

当然，用数组来测试代码可能过于笨重。
有时，对于这样的泛型函数，随机生成数据可能会更容易些。
接下来看一种更高级的参数化测试：随机测试。
通过调用函数 `unittest.random<T>()` 替换值驱动测试的数组或范围来创建随机测试：

<!-- run -->
```cangjie
@Test[array in random()]
func testRandomArrays(array: Array<Int64>) {
    // 测试数组是否已排序
    for (i in 0..(array.size - 1)) {
        @Expect(array[i] <= array[i + 1])
    }
}
```

这个测试本质上是生成大量完全随机的数值（默认为 200 个），用这些值来测试代码。
数值并不完全随机，偏向于边界值，如特定类型的零、最大值和最小值、空集合等。

特别注明：通常建议随机化测试与手工编写的测试**混用**，实践表明可以互为补充。

为了更好地描述随机测试，先把排序函数放一边，编写下面这样一个测试：

<!-- run -->
```cangjie
@Test[array in random()]
func testNonsense(array: Array<Int64>) {
    if (array.size < 2) {
        return
    }
    @Expect(array[0] <= array[1] + 500)
}
```

运行后，会生成如下类似输出：

```text
[ FAILED ] CASE: testNonsense (1159229 ns)
    REASON: After 4 generation steps and 200 reduction steps:
        array = [0, -453923686263, 0]
    with randomSeed = 1702373121372171563

    Expect Failed: `(array [ 0 ] <= array [ 1 ] + 500 == true)`
       left: false
      right: true
```

结果可见，数组`[0, -453923686263, 0]`测试失败。
再运行一次：

```text
[ FAILED ] CASE: testNonsense (1904718 ns)
    REASON: After 5 generation steps and 200 reduction steps:
        array = [0, -1196768422]
    with randomSeed = 1702373320782980551

    Expect Failed: `(array [ 0 ] <= array [ 1 ] + 500 == true)`
       left: false
      right: true
```

同样，测试失败，但值都不同。
为什么会这样呢？
因为随机测试本质上是随机的，所以每次都会生成新的随机值。
在各种不同的数据上测试函数，可能很好用；但是对于某些测试，这意味着多次运行中，有时成功，有时失败，不利于共享测试结果。
随机测试是一个强大的工具，但在使用时也需要了解这些弊端。

测试结果每次都不一样，如何向其他开发者展示结果呢？
答案很简单，就在运行测试时得到的输出中：

```text
with randomSeed = 1702373320782980551
```

以上提供了一个*随机种子*，可以在测试中用作配置项。
改写测试如下：

<!-- run -->
```cangjie
@Test[array in random()]
@Configure[randomSeed: 1702373320782980551]
func testNonsense(array: Array<Int64>) {
    if (array.size < 2) {
        return
    }
    @Expect(array[0] <= array[1] + 500)
}
```

运行结果如下：

```text
[ FAILED ] CASE: testNonsense (1910109 ns)
    REASON: After 5 generation steps and 200 reduction steps:
        array = [0, -1196768422]
    with randomSeed = 1702373320782980551

    Expect Failed: `(array [ 0 ] <= array [ 1 ] + 500 == true)`
       left: false
      right: true
```

注意，此次运行生成的值、生成值所用的步骤和随机种子与上次运行完全相同。
这种机制让随机测试*可重复*，可以保存在测试套件中与其他开发人员共享。
您也可以只从随机测试中获取数据（如本例中的数组值`[0, -1196768422]`），用这些值编写新测试。

快速看看失败的测试生成的输出。

```text
    REASON: After 5 generation steps and 200 reduction steps:
        array = [0, -1196768422]
    with randomSeed = 1702373320782980551
```

输出中包含几个重要信息：

- 测试失败前数据生成的步骤数：即测试失败前运行的迭代次数。
- 数据减量的步骤数：随机测试有缩减测试数据的机制，数据量减小后更方便操作，且提升了可读性。
- 导致测试失败的实际数据：按顺序列出所有参数（在本例中，只有一个参数 `array` ）以及它们实际导致测试失败的值。其中参数应实现 ToString 接口，否则将只打印占位符。
- 以及前面提到的随机种子，用于重现随机测试。

有些测试比较棘手，需要调整随机生成的步骤数。
可以通过如下两个配置项控制：`generationSteps` 和 `reductionSteps` 。
随机测试一个最大的优点是，只要设置了足够多的步骤，它可以运行很长时间，这样就可以检查数百万个值。

为了不使测试太耗时，默认 `generationSteps` 和 `reductionSteps` 的最大值都是 200。
通过这两个配置参数，就可以设置框架的最大步骤数。
例如，对于上面的这个小测试，参数设置为一个大的数值可能没有多大意义。之前的运行已经表明，通常不到 10 步，测试就会失败。

## 类型参数化测试

虽然当前排序的测试仅针对整型数组排序，但函数本身支持对其他任何类型排序。但元素必须是可比较的，这样才能排序。

用示例中的 `testDifferentArrays` 编写一个新的测试，对其他类型（如字符串）进行测试：

<!-- run -->
```cangjie
import std.sort.*

@Test[array in [
 [ ],
 [ "1","2","3" ],
 [ "1","2","3","4","5" ],
 [ "5","4","3","2","1" ]
 ]
]
func testDifferentArraysString(array: Array<String>) {
    // 测试数组是否已排序
    let sorted = array.clone()
    sort(sorted)
    for (i in 0..(sorted.size - 1)) {
        @Expect(sorted[i] <= sorted[i + 1])
    }
}
```

运行测试可知，测试正常。
注意，两个测试的主体和断言完全相同。
试想，如果泛型函数的测试也可以泛型，不是更方便吗？

回到之前的随机测试示例：

<!-- run -->
```cangjie
import std.sort.*

@Test[array in random()]
func testRandomArrays(array: Array<Int64>) {
    let sorted = array.clone()
    sort(sorted)
    for (i in 0..(sorted.size - 1)) {
        @Expect(sorted[i] <= sorted[i + 1])
    }
}
```

测试是广泛适用的，可以看到元素类型不限于 `Int64` ，也可以是任何类型 `T` ，例如：

比较：需要实现 Comparable\<T>。

将这个测试改写为一个泛型函数：

<!-- compile-error -->
```cangjie
import std.sort.*

@Test[array in random()]
func testRandomArrays<T>(array: Array<T>) where T <: Comparable<T> {
    let sorted = array.clone()
    sort(sorted)
    for (i in 0..(sorted.size - 1)) {
        @Expect(sorted[i] <= sorted[i + 1])
    }
}
```

编译运行后，遇到了一个问题：

```text
An exception has occurred:
MacroException: Generic function testRandomArrays requires a @Types macro to set up generic arguments
```

当然，要运行测试某些类型，需要先有这些类型。
用 `@Types` 宏设置测试，这样就可以运行测试 `Int64`、 `Float64` 和 `String` 这些类型了。

<!-- run -->
```cangjie
import std.sort.*

@Test[array in random()]
@Types[T in<Int64, Float64, String>]
func testRandomArrays<T>(array: Array<T>) where T <: Comparable<T> {
    let sorted = array.clone()
    sort(sorted)
    for (i in 0..(sorted.size - 1)) {
        // 我们更改检查，使其支持 NaN
        @Expect(!(sorted[i] > sorted[i + 1]))
    }
}
```

现在，运行测试，将编译并生成以下输出：

```text
    TCS: TestCase_testRandomArrays, time elapsed: 2491737752 ns, RESULT:
    [ PASSED ] CASE: testRandomArrays<Int64> (208846446 ns)
    [ PASSED ] CASE: testRandomArrays<Float64> (172845910 ns)
    [ PASSED ] CASE: testRandomArrays<String> (2110037787 ns)
```

注意，每个类型，测试都是单独运行的，因为行为可能大不相同。
`@Types` 宏可以用于任何参数化的测试用例，包括测试函数和测试类。

## 重用、组合和映射参数策略

现在以 `HashSet` 为例。从测试 `contains` 开始。

<!-- run -->
```cangjie
import std.collection.*

@Test[data in random()]
func testHashSetContains(data: Array<Int64>) {
    let hashSet = HashSet<Int64>()
    hashSet.add(all: data)

    for (element in data) {
        @Assert(hashSet.contains(element))
    }
}
```

效果很好。现在尝试测试 `remove` 。

<!-- run -->
```cangjie
import std.collection.*

@Test[data in random()]
func testHashSetRemove(data: Array<Int64>) {
    let hashSet = HashSet<Int64>()
    hashSet.add(all: data)

    for (element in data) {
        @Assert(hashSet.remove(element))
    }
}
```

表面上看应该可以正常工作。然而很快就可以注意到它无法正常工作，因为随机生成的数组可能包含重复项，这会导致第二次删除调用失败。所以这里想要的是生成一些没有重复的数组。

<!-- run -->
```cangjie
import std.collection.*
import std.random.*

var counter = 0

@OverflowWrapping
func generateUniqArray(len: Int64, start: UInt64) {
    if (len < 1) {
        return Array<Int64>()
    }
    let rng = Random(start)
    let step = Int64.Max / len
    counter = 0
    Array(
        len,
        {
            _ =>
            counter += rng.nextInt64() % step
            counter
        }
    )
}

@Test[start in random<UInt64>()]
func testHashSetRemove(start: UInt64) {
    let len = 1000
    let data = generateUniqArray(len, start)
    let hashSet = HashSet<Int64>()
    hashSet.add(all: data)

    for (element in data) {
        @Assert(hashSet.remove(element))
    }
}
```

然而，即使将数据生成转移到一个单独的函数中，如果想在多个不同的测试之间重用它，它仍然会有相当多的重复。此外，在准备代码和测试代码之间的界限非常不明确。因此，为了解决上述问题，测试框架以 `@Strategy` 宏的形式提供了方便的 API，允许组合和映射现有策略。

<!-- run -->
```cangjie
import std.collection.*
import std.random.*

var counter = 0

@Strategy[start in random<UInt64>()]
@OverflowWrapping
func generateUniqArray(start: UInt64): ArrayList<Int64> {
    let len = 1000
    let rng = Random(start)
    let step = Int64.Max / len
    counter = 0
    ArrayList(
        len,
        {
            _ =>
            counter += rng.nextInt64() % step
            counter
        }
    )
}

// 现在，只需要这样的输入，就可以使用该策略：

@Test[data in generateUniqArray]
func testHashSetRemove(data: ArrayList<Int64>) {
    let hashSet = HashSet<Int64>()
    hashSet.add(all: data)

    for (element in data) {
        @Assert(hashSet.remove(element))
    }
}

@Test[data in generateUniqArray]
func testHashSetToArray(data: ArrayList<Int64>) {
    let hashSet = HashSet<Int64>()
    hashSet.add(all: data)

    let result = ArrayList(hashSet.toArray())
    result.sort()
    data.sort()
    @Assert(result == data)
}
```

对于测试来说，使用此类自定义策略的用例很少。但由于它们在相应章节中描述的基准测试中的使用，它们仍然是框架的重要组成部分。

## 覆盖率引导的随机参数化测试

如上所述，随机测试对于有能力的人来说是一个强大的工具，但它们也有一些局限性。
例如：

<!-- run -->
```cangjie
import std.random.*

@Test[x in random()]
func testX(x: Int64) {
    @Expect(x != 1234567)
}
```

虽然这样的测试看起来很简单，但如果运行它，可能不会得到预期的结果：

```text
--------------------------------------------------------------------------------------------------
TP: default, time elapsed: 1393856 ns, RESULT:
    TCS: TestCase_testX, time elapsed: 1393856 ns, RESULT:
    [ PASSED ] CASE: testX (1378439 ns)
Summary: TOTAL: 1
    PASSED: 1, SKIPPED: 0, ERROR: 0
    FAILED: 0
--------------------------------------------------------------------------------------------------
```

而且即使你将生成步骤的数量增加到几百万，这个测试也可能不会失败，因为随机测试是随机的，生成精确的非常规数字的概率极低。
虽然此测试看起来是自动生成的，并且不能真正代表生产代码，但它显示了随机代码在更现实的场景中可能面临的相同问题，从而大大减少了其在更高级用途中的应用，例如查找代码中的安全缺陷。

为解决这个问题，仓颉单元测试框架引入了一项基于 security-fuzzing 测试技术的高级特性：覆盖率引导的随机参数化单元测试。该特性针对的是那些希望对其代码进行更细致的测试，同时仍然享受随机测试的可用性和易用性的用户。

使用覆盖率引导的单元测试，需要执行以下步骤：

- 该项目必须在编译器支持 `SanitizerCoverage` 的情况下进行编译。具体需要以下两个选项：`--sanitizer-coverage-trace-pc-guard` 和 `--sanitizer-coverage-trace-compares` 。
- 用例可执行文件必须配置 [--coverage-guided](./unittest_basics.md#--coverage-guided) 选项。
- 测试的生成步骤参数必须根据代码的复杂性增加，以允许覆盖引导算法继续进行。

如果我们使用编译器选项 `--sanitizer-coverage-trace-pc-guard` 和 `--sanitizer-coverage-trace-compares` 编译上面的示例，然后使用 `--coverage-guided` 选项运行它，我们得到类似于以下内容的结果：

```text
--------------------------------------------------------------------------------------------------
TP: default, time elapsed: 2004749 ns, RESULT:
    TCS: TestCase_testX, time elapsed: 2004749 ns, RESULT:
    [ FAILED ] CASE: testX (17380 ns)
    REASON: After 48 generation steps and 3 reduction steps:
        x = 1234567
    with randomSeed = 1721033700363557083
    Expect Failed: `(x != 1234567 == true)`
       left: false
      right: true

Summary: TOTAL: 1
    PASSED: 0, SKIPPED: 0, ERROR: 0
    FAILED: 1, listed below:
            TCS: TestCase_testX, CASE: testX
--------------------------------------------------------------------------------------------------
```

正如我们所看到的，测试在极少数生成步骤中失败（本例中为 48 个，但是，由于总是随机测试，结果可能会有所不同），但一般来说，建议至少将测试的生成步骤配置为数十万步。因此用例的执行时间可能会很长。