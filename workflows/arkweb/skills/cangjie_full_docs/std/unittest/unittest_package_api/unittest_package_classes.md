# 类

## class AssertionCtx

```cangjie
public class AssertionCtx {}
```

功能：存储用户定义的断言的状态。提供用于编写​​用户定义断言的方法。

### prop args

```cangjie
public prop args: String
```

功能：返回以逗号分隔的未解析的用户定义断言参数的字符串。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### prop caller

```cangjie
public prop caller: String
```

功能：获取用户定义的断言函数的标识符。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### prop hasErrors

```cangjie
public prop hasErrors: Bool
```

功能：如果用户定义内的任何断言失败，则为 `true` 。否则为 `false`。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

### func arg(String)

```cangjie
public func arg(key: String): String
```

功能：返回表示原始传递的标识符的参数值的字符串表达，与参数列表中的标识符匹配。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 函数参数列表中的标识符。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 对应标识符的参数值字符串表达。

### func fail(String)

```cangjie
public func fail(message: String): Nothing 
```

功能：存储失败信息，在用户定义的断言函数中提供并抛出 [`AssertExpection`](./unittest_package_exceptions.md#class-assertexception)。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 失败信息。

### func fail\<PP>(PP)

```cangjie
public func fail<PP>(pt: PP): Nothing where PP <: PrettyPrintable
```

功能：存储失败信息，在用户定义的断言函数中提供并抛出 [`AssertExpection`](./unittest_package_exceptions.md#class-assertexception)。

参数：

- pt: PP <: [PrettyPrintable](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-prettyprintable) - 失败信息。

### func failExpect(String)

```cangjie
public func failExpect(message: String): Unit 
```

功能：存储失败信息，在用户定义的断言函数内提供并继续函数执行。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 失败信息。

### func failExpect\<PP>(PP)

```cangjie
public func failExpect<PP>(pt: PP): Unit where PP <: PrettyPrintable
```

功能：存储失败信息，在用户定义的断言函数内提供并继续函数执行。

参数：

- pt: PP <: [PrettyPrintable](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-prettyprintable) - 失败信息。

### func setArgsAliases(Array\<String>)

```cangjie
public func setArgsAliases(aliases: Array<String>): Unit
```

功能：设置别名以通过函数 [`arg`](#func-argstring) 访问未解析的用户定义的断言函数参数。框架内部使用，用户无需使用该函数。

参数：

- aliases: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 标识符数组。数组的大小应与参数列表匹配（除 [`AssertionCtx`](#class-assertionctx) 外）。

## class Benchmark

```cangjie
public class Benchmark {}
```

功能：该类提供创建和运行单个性能测试用例的方法。

### prop name

```cangjie
public prop name: String
```

功能：获取用例名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### func run()

```cangjie
public func run(): BenchReport
```

功能：运行该性能用例。

返回值：

- [BenchReport](#class-benchreport) - 运行结果报告。

### static func create(String, Configuration, Measurement, () -> Unit)

```cangjie
public static func create(
    name: String,
    configuration!: Configuration = Configuration(),
    measurement!: Measurement = TimeNow(),
    body!: () -> Unit
): Benchmark
```

功能：创建一个性能测试用例对象。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- configuration!: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 用例配置信息。
- measurement: [Measurement](unittest_package_interfaces.md#interface-measurement) - 测量方法信息。
- body: () -> Unit - 用例执行体。

返回值：

- [Benchmark](#class-benchmark) - 性能测试用例对象。

### static func createParameterized\<T>(String, DataStrategy\<T>, Configuration, Measurement, (T) -> Unit)

```cangjie
public static func createParameterized<T>(
    name: String,
    strategy: DataStrategy<T>,
    configuration!: Configuration = Configuration(),
    measurement!: Measurement = TimeNow(),
    body!: (T) -> Unit
): Benchmark
```

功能：创建一个参数化的性能测试用例对象。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- strategy: [DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy) - 参数数据策略。
- configuration: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 用例配置信息。
- measurement!: [Measurement](unittest_package_interfaces.md#interface-measurement) 测量方法信息。
- body: () -> Unit - 用例执行体。

返回值：

- [Benchmark](#class-benchmark) - 性能测试用例对象。

### static func createParameterized\<T>(String, DataStrategyProcessor\<T>, Configuration, Measurement, (T) -> Unit)

```cangjie
public static func createParameterized<T>(
    name: String,
    strategy: DataStrategyProcessor<T>,
    configuration!: Configuration = Configuration(),
    measurement!: Measurement = TimeNow(),
    body!: (T) -> Unit
): Benchmark
```

功能：创建一个参数化的性能测试用例对象。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- strategy: [DataStrategyProcessor](#class-datastrategyprocessort) - 参数数据处理器。
- configuration: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 用例配置信息。
- measurement: [Measurement](unittest_package_interfaces.md#interface-measurement) - 测量方法信息。
- body: () -> Unit - 用例执行体。

返回值：

- [Benchmark](#class-benchmark) - 性能测试用例对象。

## class BenchReport

```cangjie
public class BenchReport <: Report {}
```

功能：提供性能用例执行结果报告处理能力。

父类型：

- [Report](#class-report)

### func reportTo\<T>(Reporter\<BenchReport, T>)

```cangjie
public func reportTo<T>(reporter: Reporter<BenchReport, T>): T
```

功能：打印性能用例结果报告。

参数：

- reporter: [Reporter](#class-report)\<[BenchReport](#class-benchreport), T> - 性能用例结果报告。

返回值：

- T - 打印结果返回值。一般为 Unit 类型。

## class CartesianProductProcessor\<T0,T1>

```cangjie
public class CartesianProductProcessor<T0, T1> <: DataStrategyProcessor<(T0, T1)> {
    public CartesianProductProcessor(let left: DataStrategyProcessor<T0>, let right: DataStrategyProcessor<T1>)
}
```

功能：笛卡尔积处理器。

父类型：

- [DataStrategyProcessor](#class-datastrategyprocessort)\<(T0, T1)>

### CartesianProductProcessor(DataStrategyProcessor\<T0>, DataStrategyProcessor\<T1>)

```cangjie
public CartesianProductProcessor(let left: DataStrategyProcessor<T0>, let right: DataStrategyProcessor<T1>)
```

功能：CartesianProductProcessor 构造函数。

参数：

- left: [DataStrategyProcessor](#class-datastrategyprocessort)\<T0> - 数据策略处理器。
- right: [DataStrategyProcessor](#class-datastrategyprocessort)\<T1> - 数据策略处理器。

## class ConsoleReporter

```cangjie
public class ConsoleReporter <: Reporter<TestReport, Unit> & Reporter<BenchReport, Unit>{
    public ConsoleReporter(let colored!: Bool = true)
}
```

功能：打印单元测试用例结果或者性能测试用例结果到控制台。

父类型：

- [Reporter](unittest_package_interfaces.md#interface-reporter)\<[TestReport](#class-testreport), [Unit](../../core/core_package_api/core_package_intrinsics.md#unit)>
- [Reporter](unittest_package_interfaces.md#interface-reporter)\<[BenchReport](#class-benchreport), [Unit](../../core/core_package_api/core_package_intrinsics.md#unit)>

### ConsoleReporter(Bool)

```cangjie
public ConsoleReporter(let colored!: Bool = true)
```

功能：ConsoleReporter 构造函数。

参数：

- colored!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用带颜色的打印，默认带颜色。

## class TextReporter\<PP>

```cangjie
public class TextReporter<PP> <: Reporter<TestReport, PP> & Reporter<BenchReport, PP> where PP <: PrettyPrinter {
    public TextReporter(let into!: PP)
}
```

功能：将单元测试用例结果或性能测试结果打印到 [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) 的子类。格式与 [ConsoleReporter](#class-consolereporter) 相同。

父类型：

- [Reporter](unittest_package_interfaces.md#interface-reporter)\<[TestReport](#class-testreport), PP>
- [Reporter](unittest_package_interfaces.md#interface-reporter)\<[BenchReport](#class-benchreport), PP>

### TextReporter(PP)

```cangjie
public TextReporter(let into!: PP)
```

功能：TextReporter 构造函数。

参数：

- into!: PP - [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) 的子类。打印报告。

## class CsvReporter

```cangjie
public class CsvReporter <: Reporter<BenchReport, Unit> {
    public CsvReporter(let directory: Path)
}
```

功能：打印性能测试用例结果数据到 CSV 文件上。

父类型：

- [Reporter](unittest_package_interfaces.md#interface-reporter)\<[BenchReport](#class-benchreport), [Unit](../../core/core_package_api/core_package_intrinsics.md#unit)>

### CsvReporter(Path)

```cangjie
public CsvReporter(let directory: Path)
```

功能：CsvReporter 构造函数。

参数：

- directory: [Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 打印文件生成地址。

## class CsvRawReporter

```cangjie
public class CsvRawReporter <: Reporter<BenchReport, Unit> {
    public CsvRawReporter(let directory: Path)
}
```

功能：打印性能测试用例结果数据，该数据只有批次的原始测量值，到 CSV 文件上。

父类型：

- [Reporter](unittest_package_interfaces.md#interface-reporter)\<[BenchReport](#class-benchreport), [Unit](../../core/core_package_api/core_package_intrinsics.md#unit)>

### CsvRawReporter(Path)

```cangjie
public CsvRawReporter(let directory: Path)
```

功能：CsvRawReporter 构造函数。

参数：

- directory: [Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 打印文件生成地址。

## class DataStrategyProcessor\<T>

```cangjie
abstract sealed class DataStrategyProcessor<T> {}
```

功能：所有 [DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy) 组件的基类。该类的实例由 [@Strategy](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#strategy-宏) 宏或成员函数创建。

### prop isInfinite

```cangjie
protected prop isInfinite: Bool
```

功能：获取该策略是否为无限。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)。

### func intoBenchmark(String, Configuration, (T, Int64, Int64) -> Float64)

```cangjie
public func intoBenchmark(
    caseName!: String,
    configuration!: Configuration,
    doRun!: (T, Int64, Int64) -> Float64
): Benchmark
```

功能：宏生成的代码使用的辅助函数。用于创建使用该策略的性能测试用例。

参数：

- caseName!: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- configuration!: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 配置信息。
- doRun!: (T, Int64, Int64) -> Float64 - 性能测试用例执行体。

返回值：

- [Benchmark](#class-benchmark) - 性能测试用例对象。

### func intoUnitTestCase(String, Configuration, (T) -> Unit)

```cangjie
public func intoUnitTestCase(
    caseName!: String,
    configuration!: Configuration,
    doRun!: (T) -> Unit
): UnitTestCase
```

功能：宏生成的代码使用的辅助函数。用于创建使用该策略的测试用例。

参数：

- caseName!: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- configuration!: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 配置信息。
- doRun!: (T) -> Unit - 性能测试用例执行体。

返回值：

- [UnitTestCase](#class-unittestcase) - 测试用例对象。

### func lastItemInfo()

```cangjie
protected func lastItemInfo(): Array<InputParameter>
```

功能：获取上一个处理条目的信息。

返回值：

- Array\<[InputParameter](./unittest_package_classes.md#class-inputparameter)> - 上一个处理条目的信息。

### func lastItem(Configuration)

```cangjie
protected func lastItem(configuration: Configuration): T
```

功能：获取上一个处理条目。

参数：

- configuration: [Configuration](./../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 处理策略配置信息。

返回值：

- T - 上一个处理条目。

### func provide(Configuration)

```cangjie
protected func provide(configuration: Configuration): Iterable<T>
```

功能：生成依据配置信息和数据策略生成的数据迭代器。

参数：

- configuration: [Configuration](./../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 处理策略配置信息。

返回值：

- [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 数据迭代器。

### func shrinkLastItem(Configuration, LazyCyclicNode)

```cangjie
protected func shrinkLastItem(configuration: Configuration, engine: LazyCyclicNode): Iterable<T>
```

功能：收缩上一个条目。

参数：

- configuration: [Configuration](./../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 配置信息。
- engine: [LazyCyclicNode](./unittest_package_classes.md#class-lazycyclicnode) - 惰性节点。

返回值：

- [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<T> - 收缩后的数据迭代器。

### static func start(DataStrategy\<T>, String)

```cangjie
public static func start(s: DataStrategy<T>, name: String): SimpleProcessor<T>
```

功能：[DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy) 的组合和映射的起点。

参数：

- s: [DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy)\<T> - 数据策略。
- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。

返回值：

- [SimpleProcessor\<T>](#class-simpleprocessort) - 测试用例处理器。

### static func start\<U>(() -> DataStrategy\<U>, String)

```cangjie
public static func start<U>(
    f: () -> DataStrategy<U>,
    name: String
): DataStrategyProcessor<U> where U <: BenchInputProvider < T >
```

功能：[DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy) 的组合和映射的起点。

参数：

- s: () -> [DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy)\<U> - 生成数据策略的闭包。
- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。

返回值：

- [DataStrategyProcessor](#class-datastrategyprocessort)\<T> - 数据策略处理器。

### static func start(() -> DataStrategy\<T>, String, Int64)

```cangjie
public static func start(
    f: () -> DataStrategy<T>,
    name: String,
    x!: Int64 = 0
): SimpleProcessor<T>
```

功能：[DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy) 的组合和映射的起点。

参数：

- s: () -> [DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy)\<T> - 生成数据策略的闭包。
- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- x!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 为实现不同返回值的重构增加的参数。

返回值：

- [SimpleProcessor\<T>](#class-simpleprocessort) - 测试用例处理器。

### static func start(() -> DataStrategyProcessor\<T>, String)

```cangjie
public static func start(f: () -> DataStrategyProcessor<T>, name: String): DataStrategyProcessor<T>
```

功能：[DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy) 的组合和映射的起点。

参数：

- s: () -> [DataStrategyProcessor](#class-datastrategyprocessort)\<T> - 生成数据策略处理器的闭包。
- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。

返回值：

- [DataStrategyProcessor](#class-datastrategyprocessort)\<T> - 数据策略处理器。

### static func start\<U>(() -> DataStrategyProcessor\<U>, String, Int64)

```cangjie
public static func start<U>(
    f: () -> DataStrategyProcessor<U>,
    name: String,
    x!: Int64 = 0
): DataStrategyProcessor<U> where U <: BenchInputProvider<T>
```

功能：[DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy) 的组合和映射的起点。

参数：

- s: () -> [DataStrategyProcessor](#class-datastrategyprocessort)\<U> - 生成数据策略处理器的闭包。
- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- x!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 为实现不同返回值的重构增加的参数。

返回值：

- [DataStrategyProcessor](#class-datastrategyprocessort)\<U> where U <: [BenchInputProvider](./unittest_package_interfaces.md#interface-benchinputprovider)\<T> - 数据策略处理器。

### extend \<T> DataStrategyProcessor\<T>

```cangjie
extend <T> DataStrategyProcessor<T> {}
```

#### func map\<R>((T) -> R)

```cangjie
public func map<R>(f: (T) -> R): MapProcessor<T, R>
```

功能：简单地将 `f` 应用于原始数据策略的每个项目。 [Shrink](../../unittest_prop_test/unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-shrinkt) 也会发生在原始输入上，然后进行映射。

参数：

- f: (T) -> R - 需要增加的处理逻辑函数。

返回值：

- [MapProcessor\<T, R>](#class-mapprocessortr) - 应用 `f` 后的处理器。

#### func mapWithConfig\<R>((T, Configuration) -> R)

```cangjie
public func mapWithConfig<R>(f: (T, Configuration) -> R): MapProcessor<T, R>
```

功能：可以访问当前的 [Configuration](./../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) ，只需将 `f` 应用于原始数据策略的每个项目。 [Shrink](../../unittest_prop_test/unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-shrinkt) 也会发生在原始输入上，然后进行映射。

参数：

- f: (T, Configuration) -> R - 需要增加的处理逻辑函数。

返回值：

- [MapProcessor\<T, R>](#class-mapprocessortr) - 应用 `f` 后的处理器。

#### func flatMap\<R>((T) -> DataProvider\<R>)

```cangjie
public func flatMap<R>(f: (T) -> DataProvider<R>): FlatMapProcessor<T, R>
```

功能：简单地将 `f` 应用于原始数据策略的每个项目，然后展平结果。 [Shrink](../../unittest_prop_test/unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-shrinkt)  也会发生在原始输入上，然后进行 [flatMap](../../collection/collection_package_api/collection_package_function.md#func-flatmapt-rt---iterabler) 。

参数：

- f: (T) -> [DataProvider](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy)\<R> - 需要增加的处理逻辑函数。

返回值：

- [FlatMapProcessor\<T, R>](#class-flatmapprocessortr) - 应用 `f` 后的处理器。

#### func flatMapStrategy((T) -> DataStrategy\<R>)

```cangjie
public func flatMapStrategy<R>(f: (T) -> DataStrategy<R>): FlatMapStrategyProcessor<T, R>
```

功能：简单地将 `f` 应用于原始数据策略的每个项目，然后展平结果。 [Shrink](../../unittest_prop_test/unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-shrinkt) 是通过返回的策略而不是原始输入来完成的。

参数：

- f: (T) -> [DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy)\<R> - 需要增加的处理逻辑函数。

返回值：

- [FlatMapStrategyProcessor\<T, R>](#class-flatmapstrategyprocessortr) - 应用 `f` 后的处理器。

#### func product(DataStrategyProcessor\<R>)

```cangjie
public func product<R>(p: DataStrategyProcessor<R>): CartesianProductProcessor<T, R>
```

功能：笛卡尔积组合器创建包含原始策略中元素的所有可能排列的数据策略。
对于无限策略，它首先迭代所有有限的子策略，然后才推进无限的子策略。
[Shrink](../../unittest_prop_test/unittest_prop_test_package_api/unittest_prop_test_package_interfaces.md#interface-shrinkt)  独立且统一地发生在原始策略的每个元素上。

参数：

- p: [DataStrategyProcessor](#class-datastrategyprocessort)\<R> - 数据策略处理器。

返回值：

- [CartesianProductProcessor\<T, R>](#class-cartesianproductprocessort0t1) - 笛卡尔积处理器。

#### func productWithUnit\<P>(P): MapProcessor\<(T, Unit), T>

```cangjie
public func productWithUnit<P>(p: P): MapProcessor<(T, Unit), T> where P <: DataStrategyProcessor<Unit>
```

功能：[DataStrategyProcessor](#class-datastrategyprocessort) 的便捷适配器。

参数：

- p: [P](#class-datastrategyprocessort) -  数据策略处理器。

返回值：

- | [MapProcessor\<(T, Unit),R>](../unittest_package_api/unittest_package_classes.md#class-mapprocessortr) - 处理器。

## class FlatMapProcessor\<T,R>

```cangjie
public class FlatMapProcessor<T,R> <: DataStrategyProcessor<R> {}
```

功能：对参数数据进行 [FlatMap](../../collection/collection_package_api/collection_package_function.md#func-flatmapt-rt---iterabler) 的处理器。

父类型：

- [DataStrategyProcessor](#class-datastrategyprocessort)\<R>

## class FlatMapStrategyProcessor\<T,R>

```cangjie
public class FlatMapStrategyProcessor<T,R> <: DataStrategyProcessor<R> {}
```

功能：对参数数据进行 [FlatMap](../../collection/collection_package_api/collection_package_function.md#func-flatmapt-rt---iterabler) 的处理器。

父类型：

- [DataStrategyProcessor](#class-datastrategyprocessort)\<R>

## class InputParameter

```cangjie
public class InputParameter {}
```

功能：入参对象类型。

## class LazyCyclicNode

```cangjie
public open class LazyCyclicNode {}
```

功能：用于在一个循环中一个接一个地推进类型擦除的内部惰性迭代器。

### func advance()

```cangjie
protected open func advance(): ?Unit
```

功能：前进一个值。

返回值：

- ?Unit - 当无法前进时返回 None ，否则返回 Unit 。

### func recover()

```cangjie
protected open func recover(): Unit
```

功能：恢复或后退一个值。

## class MapProcessor\<T,R>

```cangjie
public class MapProcessor<T,R> <: DataStrategyProcessor<R> {}
```

功能：对参数数据进行 [Map](../../collection/collection_package_api/collection_package_function.md#func-mapt-rt---r) 的处理器。

父类型：

- [DataStrategyProcessor](#class-datastrategyprocessort)\<R>

## class PowerAssertDiagramBuilder

```cangjie
public class PowerAssertDiagramBuilder {
    public init(expression: String)
}
```

功能：[PowerAssert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#powerassert-宏) 输出结果构造器。

### init(String)

```cangjie
public init(expression: String)
```

功能：构造函数。

参数：

- expression: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 表达式字符串。

### func r\<T>(T, String, Int64)

```cangjie
public func r<T>(
    value: T,
    exprAsText: String,
    position: Int64
): T 
```

功能：记录对比数据。

参数：

- value: T - 被记录的数据。
- exprAsText: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 表达式字符串。
- position: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 位置信息。

返回值：

- T - 被记录的数据。

### func r(String, String, Int64)

```cangjie
public func r(
    value: String,
    exprAsText: String,
    position: Int64
): String
```

功能：记录对比数据。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 被记录的数据。
- exprAsText: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 表达式字符串。
- position: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 位置信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 被记录的数据。

### func r(Rune, String, Int64)

```cangjie
public func r(
    value: Rune,
    exprAsText: String,
    position: Int64
): Rune
```

功能：记录对比数据。

参数：

- value: [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) - 被记录的数据。
- exprAsText: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 表达式字符串。
- position: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 位置信息。

返回值：

- [Rune](../../core/core_package_api/core_package_structs.md#struct-string) - 被记录的数据。

### func h(Exception, String, Int64)

```cangjie
public func h(
    exception: Exception,
    exprAsText: String,
    position: Int64
): Nothing
```

功能：处理异常。

参数：

- exception: Exception - 需要被处理的异常。
- exprAsText: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 表达式字符串。
- position: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 位置信息。

### func w(Bool)

```cangjie
public func w(passed: Bool): Unit
```

功能：当用例通过时返回成功结果，失败时抛出异常并打印对比结果。

参数：

- passed: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 用例是否通过。

## class Report

```cangjie
sealed abstract class Report {}
```

功能：打印测试用例结果报告的基类。

### prop errorCount

```cangjie
public prop errorCount: Int64
```

功能：获取错误的用例个数。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)。

### prop caseCount

```cangjie
public prop caseCount: Int64
```

功能：获取用例个数。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)。

### prop passedCount

```cangjie
public prop passedCount:   Int64
```

功能：获取通过的用例个数。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)。

### prop failedCount

```cangjie
public prop failedCount:   Int64
```

功能：获取失败的用例个数。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)。

### prop skippedCount

```cangjie
public prop skippedCount:   Int64
```

功能：获取跳过的用例个数。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)。

## class RawStatsReporter

```cangjie
public class RawStatsReporter <: Reporter<BenchReport, HashMap<String, (Float64, Float64)>> {
    public RawStatsReporter()
}
```

功能：未处理的性能测试数据报告器。仅给框架内部使用。

父类型：

- [Reporter](unittest_package_interfaces.md#interface-reporter)\<[BenchReport](#class-benchreport), [HashMap](../../collection/collection_package_api/collection_package_class.md#class-hashmapk-v-where-k--hashable--equatablek)\<[String](../../core/core_package_api/core_package_structs.md#struct-string), ([Float64](../../core/core_package_api/core_package_intrinsics.md#float64), [Float64](../../core/core_package_api/core_package_intrinsics.md#float64))>>

### RawStatsReporter()

```cangjie
public RawStatsReporter()
```

功能：RawStatsReporter 构造函数。

## class SimpleProcessor\<T>

```cangjie
public class SimpleProcessor<T> <: DataStrategyProcessor<T> {
    public SimpleProcessor(let buildDelegate:() -> DataStrategy<T>, let name: String)
}
```

功能：简单的数据策略处理器。对 [DataStrategyProcessor](#class-datastrategyprocessort) 的一种实现。

父类型：

- [DataStrategyProcessor](#class-datastrategyprocessort)\<T>

### SimpleProcessor(() -> DataStrategy\<T>, String)

```cangjie
public SimpleProcessor(let buildDelegate:() -> DataStrategy<T>, let name: String)
```

功能：SimpleProcessor 构造函数。

参数：

- buildDelegate: () -> [DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy)\<T> - 生成数据策略的闭包。
- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 处理器名称。

## class TestGroup

```cangjie
public class TestGroup {}
```

功能：提供构建和运行测试组合方法的类。

### prop name

```cangjie
public prop name: String
```

功能：获取测试组合名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### func runBenchmarks()

```cangjie
public func runBenchmarks(): BenchReport
```

功能：运行所有性能测试用例。

返回值：

- [BenchReport](#class-benchreport) - 性能测试用例报告。

### func runBenchmarks(Configuration)

```cangjie
public func runBenchmarks(Configuration): BenchReport
```

功能：带运行配置得执行所有性能测试用例。

参数：

- configuration: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 运行配置。

返回值：

- [BenchReport](#class-benchreport) - 性能测试用例报告。

### func runTests()

```cangjie
public func runTests(): TestReport
```

功能：执行所有单元测试用例。

返回值：

- [TestReport](#class-testreport) - 单元测试用例报告。

### func runTests(Configuration)

```cangjie
public func runTests(configuration: Configuration): TestReport
```

功能：带运行配置得执行所有单元测试用例。

参数：

- configuration: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 运行配置。

返回值：

- [TestReport](#class-testreport) - 单元测试用例报告。

### static func builder(String)

```cangjie
public static func builder(name: String): TestGroupBuilder
```

功能：创建测试组合构造器。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 测试组合名称。

返回值：

- [TestGroupBuilder](#class-testgroupbuilder) - 测试组合构造器。

### static func builder(TestGroup)

```cangjie
public static func builder(group: TestGroup): TestGroupBuilder
```

功能：创建测试组合构造器。

参数：

- group: [TestGroup](#class-testgroup) - 测试组合。

返回值：

- [TestGroupBuilder](#class-testgroupbuilder) - 测试组合构造器。

## class TestGroupBuilder

```cangjie
public class TestGroupBuilder {}
```

功能：提供配置测试组合的方法的构造器。

### func add(Benchmark)

```cangjie
public func add(benchmark: Benchmark): TestGroupBuilder
```

功能：为测试组合增加性能测试用例。

参数：

- benchmark: [Benchmark](#class-benchmark) - 性能测试用例。

返回值：

- [TestGroupBuilder](#class-testgroupbuilder)  - 测试组合构造器。

### func add(TestSuite)

```cangjie
public func add(suite: TestSuite): TestGroupBuilder
```

功能：为测试组合增加单元测试套。

参数：

- suite: [TestSuite](#class-testsuite) - 单元测试套。

返回值：

- [TestGroupBuilder](#class-testgroupbuilder)  - 测试组合构造器。

### func add(UnitTestCase)

```cangjie
public func add(test: UnitTestCase): TestGroupBuilder
```

功能：为测试组合增加单元测试用例。

参数：

- test: [UnitTestCase](#class-unittestcase) - 单元测试用例。

返回值：

- [TestGroupBuilder](#class-testgroupbuilder) - 测试组合构造器。

### func build()

```cangjie
public func build(): TestGroup
```

功能：配置完成后，构建测试组合对象。

返回值：

- [TestGroup](#class-testgroup) - 测试组合。

### func configure(Configuration)

```cangjie
public func configure(configuration: Configuration): TestGroupBuilder
```

功能：为测试组合配置配置信息。

参数：

- configuration: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 配置信息。

返回值：

- [TestGroupBuilder](#class-testgroupbuilder) - 测试组合构造器。

### func setName(String)

```cangjie
public func setName(name: String): TestGroupBuilder
```

功能：为测试组合设置名称。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 名称。

返回值：

- [TestGroupBuilder](#class-testgroupbuilder) - 测试组合构造器。

## class TestPackage

```cangjie
public class TestPackage {
    public TestPackage(let name: String)
}
```

功能：用例包对象。

### TestPackage(String)

```cangjie
public TestPackage(let name: String)
```

功能：TestPackage 构造函数。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例包名称。

### func registerCase(() -> UnitTestCase)

```cangjie
public func registerCase(testCase: () -> UnitTestCase): Unit
```

功能：注册单元测试用例。

参数：

- testCase: () -> [UnitTestCase](#class-unittestcase) - 单元测试用例生成闭包。

### func registerSuite(() -> TestSuite)

```cangjie
public func registerSuite(suite: () -> TestSuite): Unit
```

功能：注册测试套。

参数：

- suite: () -> [TestSuite](#class-testsuite) - 测试套生成闭包。

### func registerBench(() -> Benchmark)

```cangjie
public func registerBench(bench: () -> Benchmark): Unit
```

功能：注册性能用例。

参数：

- bench: () -> [Benchmark](#class-benchmark) - 性能用例生成闭包。

### func enableOptimizedMockForBench()

```cangjie
public func enableOptimizedMockForBench(): Unit
```

功能：启用优化以在测试中同时使用模拟和基准测试。

## class TestReport

```cangjie
public class TestReport <: Report {}
```

功能：单元测试执行结果报告。

父类型：

- [Report](#class-report)

### func reportTo\<T>(Reporter\<TestReport, T>)

```cangjie
public func reportTo<T>(reporter: Reporter<TestReport, T>): T
```

功能：打印单元测试执行报告。

参数：

- reporter: [Reporter](#class-report)\<[TestReport](#class-testreport), T> - 单元测试报告打印器。

返回值：

- T - 打印返回值，一般为 Unit 。

## class TestSuite

```cangjie
public class TestSuite {}
```

功能：提供构建和执行测试套方法的类。

### prop name

```cangjie
public prop name: String
```

功能：获取测试套名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### func runBenchmarks()

```cangjie
public func runBenchmarks(): BenchReport
```

功能：运行所有性能测试用例。

返回值：

- [BenchReport](#class-benchreport) - 性能测试运行结果。

### func runBenchmarks(Configuration)

```cangjie
public func runBenchmarks(configuration: Configuration): BenchReport
```

功能：带配置信息得运行所有性能测试用例。

参数：

- configuration: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 运行配置信息。

返回值：

- [BenchReport](#class-benchreport) - 性能测试用例运行结果。

### func runTests()

```cangjie
public func runTests(): TestReport
```

功能：运行测试套。

返回值：

- [TestReport](#class-testreport) - 测试套运行结果。

### func runTests(Configuration)

```cangjie
public func runTests(configuration: Configuration): TestReport
```

功能：带配置信息得运行测试套。

参数：

- configuration: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 运行配置信息。

返回值：

- [TestReport](#class-testreport) - 测试套运行结果。

### static func builder(String)

```cangjie
public static func builder(name: String): TestSuiteBuilder
```

功能：创建测试套构建器。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 测试套名称。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试套构造器。

### static func builder(TestSuite)

```cangjie
public static func builder(suite: TestSuite): TestSuiteBuilder
```

功能：创建测试套构建器。

参数：

- suite: [TestSuite](#class-testsuite) - 测试套。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试套构造器。

## class TestSuiteBuilder

```cangjie
public class TestSuiteBuilder {}
```

功能：提供配置测试套方法的测试套构造器。

### func add(Benchmark)

```cangjie
public func add(benchmark: Benchmark): TestSuiteBuilder
```

功能：为测试套添加性能用例。

参数：

- benchmark: [Benchmark](#class-benchmark) - 性能测试用例。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func add(UnitTestCase)

```cangjie
public func add(test: UnitTestCase): TestSuiteBuilder
```

功能：为测试套添加单元测试用例。

参数：

- test: [UnitTestCase](#class-unittestcase) - 单元测试用例。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func afterAll(() -> Unit)

```cangjie
public func afterAll(body: () -> Unit): TestSuiteBuilder
```

功能：为测试套添加在所有用例执行完成后执行的生命周期管理闭包。

参数：

- body: () -> Unit - 执行体。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func afterEach(() -> Unit)

```cangjie
public func afterEach(body: () -> Unit): TestSuiteBuilder
```

功能：为测试套添加在每个用例执行完成后执行的生命周期管理闭包。

参数：

- body: () -> Unit - 执行体。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func afterEach((String) -> Unit)

```cangjie
public func afterEach(body: (String) -> Unit): TestSuiteBuilder
```

功能：为测试套添加在每个用例执行完成后执行的生命周期管理闭包。

参数：

- body: (String) -> Unit - 执行体。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func beforeAll(() -> Unit)

```cangjie
public func beforeAll(body: () -> Unit): TestSuiteBuilder
```

功能：为测试套添加在所有用例执行前执行的生命周期管理闭包。

参数：

- body: () -> Unit - 执行体。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func beforeEach(() -> Unit)

```cangjie
public func beforeEach(body: () -> Unit): TestSuiteBuilder
```

功能：为测试套添加在每个用例执行前执行的生命周期管理闭包。

参数：

- body: () -> Unit - 执行体。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func beforeEach((String) -> Unit)

```cangjie
public func beforeEach(body: (String) -> Unit): TestSuiteBuilder
```

功能：为测试套添加在每个用例执行前执行的生命周期管理闭包。

参数：

- body: (String) -> Unit - 执行体。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func template(TestSuite)

```cangjie
public func template(template: TestSuite): TestSuiteBuilder
```

功能：执行此方法可为测试套件设置模板。

参数

- template: TestSuite - 将作为模板的测试套件。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func build()

```cangjie
public func build(): TestSuite
```

功能：配置完成后构造测试套。

返回值：

- [TestSuite](#class-testsuite) - 测试套。

### func configure(Configuration)

```cangjie
public func configure(configuration: Configuration): TestSuiteBuilder
```

功能：为测试套添加配置信息。

参数：

- configuration: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 测试配置信息。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

### func setName(String)

```cangjie
public func setName(name: String): TestSuiteBuilder
```

功能：为测试套设置名称。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 测试套名称。

返回值：

- [TestSuiteBuilder](#class-testsuitebuilder) - 测试组合构造器。

## class UnitTestCase

```cangjie
public class UnitTestCase {}
```

功能：提供创建和执行单元测试用例的方法的类。

### prop name

```cangjie
public prop name: String
```

功能：获取单元测试名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### func run()

```cangjie
public func run(): TestReport
```

功能：运行单元测试用例。

返回值：

- [TestReport](#class-testreport) - 单元测试执行结果报告。

### static func create(String, Configuration, () -> Unit)

```cangjie
public static func create(
    name: String,
    configuration!: Configuration = Configuration(),
    body!: () -> Unit
): UnitTestCase
```

功能：创建单元测试用例。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- configuration!: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 用例配置信息。
- body!: () -> Unit - 用例执行体。

返回值：

- [UnitTestCase](#class-unittestcase) - 单元测试用例对象。

### static func createParameterized\<T>(String, DataStrategy\<T>, Configuration, (T) -> Unit)

```cangjie
public static func createParameterized<T>(
    name: String,
    strategy: DataStrategy<T>,
    configuration!: Configuration = Configuration(),
    body!: (T) -> Unit
): UnitTestCase
```

功能：创建参数化的单元测试用例。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- strategy: [DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy) - 参数数据策略。
- configuration!: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 用例配置信息。
- body!: () -> Unit - 用例执行体。

返回值：

- [UnitTestCase](#class-unittestcase) - 单元测试用例对象。

### static func createParameterized\<T>(String, DataStrategyProcessor\<T>, Configuration, (T) -> Unit)

```cangjie
public static func createParameterized<T>(
    name: String,
    strategy: DataStrategyProcessor<T>,
    configuration!: Configuration = Configuration(),
    body!: (T) -> Unit
): UnitTestCase
```

功能：创建参数化的单元测试用例。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用例名称。
- strategy: [DataStrategyProcessor](#class-datastrategyprocessort) - 参数数据处理器。
- configuration!: [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) - 用例配置信息。
- body!: () -> Unit - 用例执行体。

返回值：

- [UnitTestCase](#class-unittestcase) - 单元测试用例对象。

## class XmlReporter

```cangjie
public class XmlReporter <: Reporter<TestReport, Unit> {
    public XmlReporter(let directory: Path)
}
```

功能：打印单元测试用例结果数据到 Xml 文件上。

父类型：

- [Reporter](unittest_package_interfaces.md#interface-reporter)\<[TestReport](#class-testreport), [Unit](../../core/core_package_api/core_package_intrinsics.md#unit)>

### XmlReporter(Path)

```cangjie
public XmlReporter(let directory: Path)
```

功能：XmlReporter 构造函数。

参数：

- directory: [Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 打印文件生成地址。
