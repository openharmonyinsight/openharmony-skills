# 基准测试

## 基准测试入门

仓颉单元测试框架为灵活创建基准测试提供了强大的支持。

为保证结果的可靠性，大部分工作都在仓颉单元测试框架内部完成，包括：

- 管理预热
- 重复执行
- 减少垃圾回收（garbage collection，GC）导致的噪音和离群值
- 测试框架开销
- 提供统计分析结果

通过在相应示例中使用`@Bench`宏即可构建一个简单的基准测试。

<!-- run -->
```cangjie
@Test
class Foo {
    var x = 0
    @Bench
    func foo() {
        x += 1
    }
}
```

要运行基准测试，您可以通过向测试可执行文件传入 `--bench` 选项来实现，或者在 cjpm 项目中，使用 `cjpm bench` 命令。

## 参数化基准测试

基准测试 API 的语法与单元测试相似，并且尽可能地与现有单元测试特性集成。
`@Bench` 宏支持参数化用例和数据策略，与 `@TestCase` 宏相同。
除此之外，其他大多数宏（如 `@BeforeEach`、`@AfterEach`、`@BeforeAll`、`@AfterAll`、`@Types`、`@Configure`）在基准测试中均以相同的方式工作。

例如，可以为默认的哈希方法编写一个简单的基准测试。注意，数据创建在基准测试外，确保在基准测试开始之前只创建一次。

<!-- run -->
```cangjie
@Test
class Foo {
    var hash = 0
    let data = String(Array(1000, repeat: r'a'))

    @Bench
    func hashCode() {
        hash = data.hashCode()
    }
}
```

接下来，若要在不同数据上运行此基准测试，最直接的方法如下：

<!-- run -->
```cangjie
@Test
class Foo {
    var hash = 0
    let data_1 = String(Array(1000, repeat: r'a'))
    let data_2 = String(Array(10000, repeat: r'a'))

    @Bench[data in [ data_1, data_2 ]]
    func hashCode(data: String) {
        hash = data.hashCode()
    }
}
```

尽管该方法有效，但你会发现最终报告将输入参数命名为 `data[0]` 和 `data[1]`，因为对于任意的输入参数，框架并不知道在我们的基准测试中哪个属性最重要。此外，该方法还存在不必要的代码冗余问题。甚至，这种方法还存在一个更大的潜在问题：如果数据类型不是简单的字符串，而是更为复杂的形式，如字符串数组，那么就会分配大量活跃对象，其中大部分对象仅用于执行特定基准测试。

<!-- run -->
```cangjie
@Test
class ArrayBenchmarks {
    var hash = 0
    let data_1 = Array(1000) {i => i.toString()}
    let data_2 = Array(10000) {i => i.toString()}

    @Bench[data in [ data_1, data_2 ]]
    func hashCode(data: Array<String>) {
        var hasher = DefaultHasher()
        for (e in data) {
            hasher.write(e)
        }
        hash = hasher.finish()
    }

    @Bench
    func createArray() {
        Array(10, repeat: 0)
    }
}

```

当对 `createArray` 进行基准测试时，每次触发 GC 都会涉及到遍历 `data_1` 和 `data_2` 元素，即便它们与除 `hashCode` 基准测试外的其他测试都无关。特别是在处理大量对象时，可能会导致基准测试不稳定，从而影响最终结果的准确性。

如前所述的问题及更复杂的问题，都可通过定义特定策略并应用 `@Strategy` 宏来解决。该宏能够接收与 `@Bench` 和 `@TestCase` 宏相同的数据领域特定语言（domain specific language，DSL），进而生成一种新策略，以扁平化方式映射输入。因此，本示例可进行如下演变：

<!-- run -->
```cangjie
@Test
class ArrayBenchmarks {
    var hash = 0

    @Strategy[len in [ 1000, 10000 ]]
    func arrays(len: Int64): Array<String> {
        Array(10000) {i => i.toString()}
    }

    @Bench[data in arrays]
    func hashCodeArray(data: Array<String>) {
        var hasher = DefaultHasher()
        for (e in data) {
            hasher.write(e)
        }
        hash = hasher.finish()
    }

    @Strategy[len in [ 1000, 10000 ]]
    func strings(len: Int64): String {
        String(Array(len, repeat: r'a'))
    }

    @Bench[data in strings]
    func hashCodeString(data: String) {
        hash = data.hashCode()
    }
}
```

得到的输出如下：

```text
TP: package, time elapsed: 18438985580 ns, RESULT:
    TCS: ArrayBenchmarks, time elapsed: 18438962951 ns, RESULT:
    | Case           | Args   |   Median |         Err |   Err% |     Mean |
    |:---------------|:-------|---------:|------------:|-------:|---------:|
    | hashCodeArray  | 1000   | 10.68 us |  ±0.0832 us |  ±0.8% | 10.57 us |
    | hashCodeArray  | 10000  | 104.3 us |   ±0.504 us |  ±0.5% | 103.8 us |
    |                |        |          |             |        |          |
    | hashCodeString | 1000   | 165.7 ns |   ±0.513 ns |  ±0.3% | 165.6 ns |
    | hashCodeString | 10000  | 1.576 us | ±0.00644 us |  ±0.4% | 1.563 us |
Summary: TOTAL: 2
    PASSED: 2, SKIPPED: 0, ERROR: 0
    FAILED: 0
```

此时，框架将长度作为初始输入参数。在基准测试开始前，只为特定基准生成相关数据，因此不会影响后续基准测试。此处减少了代码冗余，甚至可以将 `[1000, 10000]` 数组移动到独立变量中来进一步减少冗余。此外，由于数据在框架内部处理，编译器无法直接获取精确的参数值进行优化。

现在，我们假设输入数据不能被基准测试改变，以确保每次函数调用接收的数据版本都是相同的。本框架同样支持那些允许修改输入数据的基准测试，详见[每次调用前的设置](#每次调用前的设置)小节。

## 如何取得理想结果

本框架主要用于减少各种因素对执行时间方差的影响，旨在获得可靠且可复现的结果。
结果表中的 `Err%` 列是衡量测试结果可靠性的主要指标。通常，如果 `Err%` 小于 3%，则认为结果可靠，如果大于 10%，则需深入探究原因并降低方差。这并不是普适的衡量标准，但可以用于初步判断。某些基准测试中，执行时间差异可能较大，导致方差变大，但均值仍趋于稳定。

然而，仍然有一些我们无法控制的外部因素，这些因素需要由用户自行管理。具体包括：

- 编译器优化选项。通常，除非你想测试特定优化的效果，否则应该启用大多数优化。建议至少启用仓颉编译器的 `-O2` 选项。
- 后台 CPU 工作。如果操作系统在基准测试期间突然切换任务，可能会显著影响测试结果。因此，所有消耗 CPU 的后台任务应在启动基准测试前完成或暂停。也可以为这些务设置明确的 CPU 亲和性，以确保基准测试和其他 CPU 密集型任务运行在不同的 CPU 核上。
- 使用外部 I/O。用户可能会不小心测试到 I/O 操作的性能和延迟，而非后续处理的性能。建议单独对 I/O 部分或处理部分进行基准测试。
- 不必要的优化。如需测试某个函数在特定参数值下的性能，编译器可能会将这些参数值当作常量进行优化。使用参数化基准测试可以避免这种情况。未来还将提供“黑盒”内方法，帮助更好地控制此类优化。
- 副作用。框架中的所有分析都假设经过基准测试的函数尽可能纯净，即执行过程中的代码路径仅依赖于输入参数。因此，在编写基准测试时，必须确保副作用（例如修改全变量或测试类字段）不会影响每次基准测试迭代时代码的执行方式。注意，默认情况下，每次调用待基准测试的函数时，参数值是相同的。如果参数修改了，则意味着下一次调会使用修改后的值。不建议如此操作，因为每次调用都需要再设置一次。
- 冗余静态分配。如果在基准测试之前分配了大量对象（无论是静态分配还是在 `@Before*` 方法中分配），需要确保这些对象在相关基准测试结束后被及时释放。否则，可能会增加 GC 负担，因为 GC 仍然需要遍历这些不再使用但仍然可达的对象，影响后续基准测试的准确性。

本框架会尽力检测是否存在这些因素且影响了基准测试结果，并在相应情况下发出警告。但这仅作为一种提醒，而非可靠的解决方案。也就是说，即使没有产生警告，也并不能保证已正确排除了所有这些因素的影响。此外，在一些情况下，例如启用编译优化选项，也可能无法准确知道用户究竟想要基准测试的是什么。

## 框架的测试方式

框架的核心算法可以用以下伪代码表示：

<!-- compile-error -->
```cangjie

// 由@Bench[arg in dataStrategy] 宏在 someFunc(arg: Arg) 函数上生成

let measurement = TimeNow()  // 或者使用通过 @Measure 宏提供的其他 Measurement 实现
func measureBatchSomeFunc(
    parameter: ImmutableInputProvider<Arg>, // 或任何由策略返回的其他 BenchInputProvider 实现
    batchSize: Int64,
    maxBatchSize: Int64
): Float64 {

    parameter.reset(maxBatchSize)   // 如果需要批量预生成输入数据，则重置 BatchInputProvider

    measurement.setup()
    let start = measurement.measure()

    for(i in 0..maxBatchSize) {     // 循环始终执行到 maxBatchSize，这样我们可以将循环本身所需的时间从最终结果中排除
        let arg = parameter.get(i)
        if (i < batchSize) {
            /*
            body of someFunc
            */
        }
    }

    measurement.measure() - start
}
Framework.addBenchmark(dataStrategy, Benchmark(measureBatchSomeFunc))

// 框架内部

for (data in dataStrategy) {
    benchmark.runBench(data)
}

doStatisticalAnalisys(benchmark.results)

class Benchmark<T> {
    let results = ArrayList<(BatchSize, BatchResult)>
    Benchmark(let runBatch: (T, Int64, Int64) -> Float64) {}

    func runBench(data: T) {
        let estimation = warmup(data)

        let batchSizes = calcBatchSizes(estimation)
        for (i in batchSizes) {
            let resultBatch = runBatch(data, i, batchSizes.end)
            results.append(i, resultBatch)

            // 根据 explicitGC 配置参数运行 GC
            explicitGC.invoke()
        }
    }

    func warmup(data: T) {
        // 根据 warmup 配置参数进行预热
    }

    func calcBatchSizes(estimation: Duration) {
        // 根据预热估计选择最合适的批处理量和批处理大小
    }

}
```

这里的主要逻辑是，`measureBatchSomeFunc(data, i, maxBatchSize)` 和 `measureBatchSomeFunc(data, i+n, maxBatchSize)` 的执行时间差正好是执行 `n` 次 `someFunc` 的时间。

这意味着，通过估算这两次执行时间的差异，我们可以精确地估算出单次执行 `someFunc` 所需的时间。而这样的估算不包括测试本身、批量循环或获取下一份输入数据所带来的开销。

## 高级特性

某些基准测试需要特殊配置，以便准确地判断预期结果或深入了解测试结果。本框架提供了多种 API，旨在覆盖尽可能多的复杂用例。

### 详细报告

当基准测试结果存在显著的不稳定性时，单纯查看聚合的统计参数往往不足以帮助分析。而打印所有原始数据虽然能提供详细信息，但打印信息过多，不便于人工分析。为了解决这一问题，我们提供了一种基于 HTML 的报告，其中包含各种图表，展示原始测试数据及其统计分析结果。要生成此报告，需使用 `--report-format=html` 选项。该报告包含一个导航页面，列出所有执行过的测试用例，并且为每个用例提供详细报告，展示所有参数和执行的测试数据。每条测试数据还将附带一个概率分布的内核密度估计图以及一个展示所有原始测试数据的图表。目前，本框架使用 Gnuplot 工具绘制图表，需要用户自行安装该工具。

如果用户具备统计学背景，可自行进行数据的统计分析。为方便分析，我们支持使用 `--report-format=csv-raw` 选项将原始测试数据导出为 CSV 格式。

### 自定义测试源

默认情况下，框架测试的是时间，通常这已经足够。然而，在某些情况下，为了更详细地调查性能问题，可能需要其他的性能特征。为了实现这样的测试，我们提供了 `Measurement` 接口。此外，我们还支持一些常见的高级测试源。要启用这些测试源，可以使用一个特殊的 `@Measure` 类来注释这样一个测试源列表。

<!-- run -->
```cangjie
@Test
@Measure[TimeNow(Nanos), CpuCycles(), Perf(), Perf(HW_CACHE_MISSES)]
class Bench {
    var x = 0
    @Bench
    func foo() {
        x += 1
    }
}
```

框架提供的开箱即用的测试工具包括：

- `TimeNow`：使用 `DateTime.now` 测试实时时间。可以配置特定的时间单位，以便所有结果都使用相同的时间单位打印。
- `CpuCycles`：用于测试裸机 CPU 指令的 CPU 使用周期数。仅在有此类指令的平台上可用，并且可以在用户空间中执行。
- `Perf`：使用 Linux 的 `perf_event_open` 系统调用，测试各种软硬件的 CPU 计数器。

### 每次调用前的设置

假设我们要对 `ArrayList.sort` 函数进行基准测试。该函数会修改其输入数据，导致基准测试结果不同，因为除第一次外，后续每次调用 `sort` 函数都是在已排序的数组上进行测试。因此，为了解决这个问题，我们需要在每次调用函数之前都重新生成数据。我们提供了 `BenchInputProvider` 接口实现器，可以通过 `@Strategy` 注解的函数返回数据。

<!-- run -->
```cangjie
import std.unittest.*
import std.collection.*

@Test
class Foo {
    @Strategy[len in [ 1000, 10000 ]]
    func strings(len: Int64): GenerateEachInputProvider<ArrayList<Int64>> {
        GenerateEachInputProvider {=> ArrayList<Int64>()}
    }

    @Bench[data in strings]
    func sort(data: ArrayList<Int64>) {
        data.sort()
    }
}
```

本框架提供了如下四种实现，基本可以覆盖所有可能的使用场景：

- `ImmutableInputProvider`：每次仅复制原始数据。当返回常规策略类型（未实现 `BenchInputProvider` 接口）时，默认采用此实现。
- `GenerateEachInputProvider`：每次在调用待基准测试函数之前生成数据。这样测试过程中生成数据，框架从总测试时间中减去生成开销。这种方法要求生成函数的执行应该尽可能纯净且稳定。此外，数据生成的时间应小于实际基准测试的时间，否则实际基准测试时间可能会因为生成函数的差异而不准确。每次调用前都建议如此设置，但如果前述条件不满足，或者方差仍然较大，可考虑其他方法。
- `BatchSizeOneInputProvider`：每次在调用待基准测试函数之前生成数据。但这种方法特殊要求批处理大小为 1，框架不会将数据生成时间计入总测试时间中。在这种模式下，框架会单独测试每次函数基准测试的执行时间。这种模式没有了批量执行的优势，因此主要缺点是精度较低。精度是否成为问题取决于硬件配置，但一般来说，如果基准测试时间小于 1 微秒，应注意；如果基准测试时间小于 100 纳秒，则强烈不建议采用此模式。
- `BatchInputProvider`：每次批处理开始之前，在缓冲区中生成多个数据副本。理论上，这具有批量执行的优势。然而，它也有一系列问题。首先，它会导致冗余分配，如果批处理大小足够大，可能会带来大量的 GC 工作。其次，测试结果可能会略有不同，因为之前数据生成后立即交给待基准测试的函数，而现在数据很可能仍在缓存中。这种情况下，所有数据生成完成后，生成的第一个元素才可能会从缓存中移出。

### 高级配置参数

有许多与基准测试相关的配置参数可以通过 `@Configue` 宏进行设置。当前支持的配置参数包括：

- `batchSize`：用于指定当批处理大小与执行时间之间存在非线性关系时的精确批处理大小范围。默认情况下，框架会根据预热结果自动选择批处理大小。
- `minBatches`：指定工作负载拆分后的最小批处理量。默认情况下，框架会根据预热结果在 10 到 200 之间选择最合适的值。注意，指定过大的值可能导致统计分析时间过长。
- `warmup`：指定框架调用函数执行基准测试的预热时间。
- `minDuration`：指定基准测试的目标持续时间。框架会选择批处理大小和批处理量，使整个基准测试阶段的执行时间略微超过`minDuration`的目标值。
- `explicitGC`：指定批处理之间如何执行 GC。默认情况下，框架会在批处理之间触发 GC，尝试均匀分配 GC 工作负载。否则，对于内存分配密集型的基准测试，可能会出现不可知的 GC 波动，影响测试结果。但对于一些没有内存分配的基准测试，这种行为可能会导致结果不准确或不稳定。若要禁用此行为，可以将该参数设置为 `Disable`。

此外，有时可能需要迭代多个不同值的参数，以验证其是否影响结果。为了支持这种需求，框架提供了数据 DSL 的特殊语法形式：`config.<parameter> in <strategy>`。

<!-- run -->
```cangjie
@Test
class Foo {
    var x = 0
    @Bench[config.warmup in [ Duration.second * 0.1, Duration.second ]]
    func foo() {
        x += 1
    }
}
```

### 避免不必要的优化

在基准测试复杂代码时，通常代码会包含一些能够影响其行为的参数。因此，为了执行一个确定性的基准测试，你可能需要为这些参数指定具体的值。基准测试代码可能如下所示：

<!-- run -->
```cangjie
@Bench
@Test
func foo(): Unit {
    /* complexCode(param: arg) */
}
```

但是，可能存在这样的情况：这个函数在真实程序中并不是这么调用的。也就是说，`param` 的值在真实程序中是运行时计算出来的，而在这里我们使用了字面常量，允许编译器在优化时利用这些信息。问题在于，我们希望基准测试的 `complexCode` 能够准确模拟它在真实程序中的表现。因此，解决这个问题的方法是使用策略来隐藏编译器看到的确切值。

<!-- run -->
```cangjie
@Bench[arg in [ 1 ]]
@Test
func foo(arg: Int64): Unit {
    /* complexCode(param: arg) */
}
```

然而，这里依然存在另一个问题。`complexCode` 的返回值没有被使用。如果编译器检测到它可以部分或完全移除这个函数调用，将会发生优化。为了解决这个问题，应该通过黑盒处理返回值。这个功能仍在开发中，所以目前的临时解决方法是将返回值存储在全局变量中。

<!-- 待办：黑盒 -->
