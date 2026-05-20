# 结构体

## struct BatchInputProvider\<T>

```cangjie
public struct BatchInputProvider<T> <: BenchInputProvider<T> {
    public BatchInputProvider(let builder: () -> T)
}
```

功能：输入提供程序，在执行之前在缓冲区中生成整个基准批次的输入。

父类型：

- [BenchInputProvider](unittest_package_interfaces.md#interface-benchinputprovider)\<T>

### BatchInputProvider(() -> T)

```cangjie
public BatchInputProvider(let builder: () -> T)
```

功能：BatchInputProvider 构造函数。

参数：

- builder: () -> T - 用于生成基准测试输入的闭包。

### func get(Int64)

```cangjie
public mut func get(idx: Int64): T
```

功能：获取元素，该函数的执行时间包含在基准测量中，然后作为框架开销计算的一部分从结果中排除。

参数：

- idx: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 元素索引值。

返回值：

- T - 元素值。

### func reset(Int64)

```cangjie
public mut func reset(max: Int64)
```

功能：在基准测量之前调用。调用此函数后，后续的 `get(i)` 调用必须成功获取 [0, max) 中的 `i` 。

参数：

- max: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 最大值。

## struct BatchSizeOneInputProvider\<T>

```cangjie
public struct BatchSizeOneInputProvider<T> <: BenchInputProvider<T>{
    public BatchSizeOneInputProvider(let builder: () -> T)
}
```

功能：基准输入提供程序，在每次执行基准之前生成输入。
与 `GenerateEachInputProvider` 的区别在于，当批量大小为 1 时，我们可以测量。
每个基准测试调用都是独立的，因此输入生成永远不会包含在测量中。
如果 `GenerateEachInputProvider` 给出的结果质量较差，则应使用。 这种情况可能会发生，因为生成输入所需的时间比实际基准要多得多，或者如果输入生成的执行时间非常不稳定。

父类型：

- [BenchInputProvider](unittest_package_interfaces.md#interface-benchinputprovider)\<T>

### BatchSizeOneInputProvider(() -> T)

```cangjie
public BatchSizeOneInputProvider(let builder: () -> T)
```

功能：BatchSizeOneInputProvider 构造函数。

参数：

- builder: () -> T - 用于生成基准测试输入的 lambda 。

### func get(Int64)

```cangjie
public mut func get(idx: Int64): T
```

功能：获取元素，该函数的执行时间包含在基准测量中，然后作为框架开销计算的一部分从结果中排除。

参数：

- idx: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 元素索引值。

返回值：

- T - 元素值。

### func reset(Int64)

```cangjie
public mut func reset(max: Int64)
```

功能：在基准测量之前调用。调用此函数后，后续的 `get(i)` 调用必须成功获取 [0, max) 中的 `i` 。

参数：

- max: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 最大值。

## struct CpuCycles

```cangjie
public struct CpuCycles <: Measurement {}
```

功能：使用本机 `rdtscp` 指令测量 CPU 周期数。仅适用于 x86 平台。

父类型：

- [Measurement](unittest_package_interfaces.md#interface-measurement)

### prop conversionTable

```cangjie
prop conversionTable: MeasurementUnitTable
```

功能：提供当前时间的单位换算表。
例如 `[(1.0, "cycles")]`。

类型：[MeasurementUnitTable](../unittest_package_api/unittest_package_types.md#type-measurementunittable)。

### prop name

```cangjie
prop name: String
```

功能：提供当前时间单位唯一的显示名称，例如：`CpuCycles`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### prop textDescription

```cangjie
prop textDescription: String
```

功能：描述此测量的简单文本将显示在某些报告中。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### func measure()

```cangjie
public func measure(): Float64
```

功能：返回执行了多少个 CPU 周期。

返回值：

- [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 计算得到的数据，用于统计分析。

### func setup()

```cangjie
public func setup()
```

功能：在测量前执行的配置动作。

## struct GenerateEachInputProvider\<T>

```cangjie
public struct GenerateEachInputProvider<T> <: BenchInputProvider<T>{
    public GenerateEachInputProvider(let builder: () -> T)
}
```

功能：基准输入提供程序，在每次执行基准之前生成输入。
生成时间包含在基准测量中，然后作为框架开销计算的一部分从最终结果中排除。

父类型：

- [BenchInputProvider](unittest_package_interfaces.md#interface-benchinputprovider)\<T>

### GenerateEachInputProvider(() -> T)

```cangjie
public GenerateEachInputProvider(let builder: () -> T)
```

功能：GenerateEachInputProvider 构造函数。

参数：

- builder: () -> T - 用于生成基准测试输入的闭包。

### func get(Int64)

```cangjie
public mut func get(idx: Int64): T
```

功能：获取元素，该函数的执行时间包含在基准测量中，然后作为框架开销计算的一部分从结果中排除。

参数：

- idx: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 元素索引值。

返回值：

- T - 元素值。

### func reset(Int64)

```cangjie
public mut func reset(max: Int64)
```

功能：在基准测量之前调用。调用此函数后，后续的 `get(i)` 调用必须成功获取 [0, max) 中的 `i` 。

参数：

- max: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 最大值。

## struct ImmutableInputProvider\<T>

```cangjie
public struct ImmutableInputProvider<T> <: BenchInputProvider<T> {
    public ImmutableInputProvider(let data: T)
}
```

功能：最简单的输入提供程序，只需为基准测试的每次调用复制数据。适用于基准测试不会改变输入的情况。它在框架内默认使用。

父类型：

- [BenchInputProvider](unittest_package_interfaces.md#interface-benchinputprovider)\<T>

### ImmutableInputProvider(T)

```cangjie
public ImmutableInputProvider(let data: T)
```

功能：ImmutableInputProvider 构造函数。

参数：

- data: T - 基准测试的输入。

### func get(Int64)

```cangjie
public mut func get(idx: Int64): T
```

功能：获取元素，该函数的执行时间包含在基准测量中，然后作为框架开销计算的一部分从结果中排除。

参数：

- idx: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 元素索引值。

返回值：

- T - 元素值。

### static func createOrExisting(T, Int64)

```cangjie
public static func createOrExisting(arg: T, x!:Int64=0): ImmutableInputProvider<T>
```

功能：创建或获取一个 ImmutableInputProvider 对象。

参数：

- arg: T - 提供器需复制的参数。
- x!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 为实现重载而增加的参数。

返回值：

- ImmutableInputProvider\<T> - 输入提供器。

### static func createOrExisting\<U>(U)

```cangjie
public static func createOrExisting<U>(arg: U): U where U <: BenchInputProvider<T>
```

功能：创建或获取一个 BenchInputProvider 的子类型对象。

参数：

- arg: T - 提供器需复制的参数。

返回值：

- U - 输入提供器。

## struct KeyBaseline

```cangjie
public struct KeyBaseline <: KeyFor<String> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

例如：

<!-- compile -->
```cangjie
let conf = Configuration()
conf.set(KeyBaseline.baseline, "baseline")
```

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop baseline

```cangjie
public static prop baseline: Baseline
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyBaselinePath

```cangjie
public struct KeyBaselinePath <: KeyFor<String> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop baselinePath

```cangjie
public static prop baselinePath: BaselinePath
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyBatchSize

```cangjie
public struct KeyBatchSize <: KeyFor<Int64> & KeyFor<Range<Int64>> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop batchSize

```cangjie
public static prop batchSize: BatchSize
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyBench

```cangjie
public struct KeyBench <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop bench

```cangjie
public static prop bench: Bench
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyCaptureOutput

```cangjie
public struct KeyCaptureOutput <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop captureOutput

```cangjie
public static prop captureOutput: CaptureOutput
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyCoverageGuided

```cangjie
public struct KeyCoverageGuided <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop coverageGuided

```cangjie
public static prop coverageGuided: CoverageGuided
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyCoverageGuidedBaselineScore

```cangjie
public struct KeyCoverageGuidedBaselineScore <: KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop coverageGuidedBaselineScore

```cangjie
public static prop coverageGuidedBaselineScore: CoverageGuidedBaselineScore
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyCoverageGuidedInitialSeeds

```cangjie
public struct KeyCoverageGuidedInitialSeeds <: KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop coverageGuidedInitialSeeds

```cangjie
public static prop coverageGuidedInitialSeeds: CoverageGuidedInitialSeeds
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyCoverageGuidedMaxCandidates

```cangjie
public struct KeyCoverageGuidedMaxCandidates <: KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop coverageGuidedMaxCandidates

```cangjie
public static prop coverageGuidedMaxCandidates: CoverageGuidedMaxCandidates
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyCoverageGuidedNewCoverageBonus

```cangjie
public struct KeyCoverageGuidedNewCoverageBonus <: KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop coverageGuidedNewCoverageBonus

```cangjie
public static prop coverageGuidedNewCoverageBonus: CoverageGuidedNewCoverageBonus
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyCoverageGuidedNewCoverageScore

```cangjie
public struct KeyCoverageGuidedNewCoverageScore <: KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop coverageGuidedNewCoverageScore

```cangjie
public static prop coverageGuidedNewCoverageScore: CoverageGuidedNewCoverageScore
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyDeathAware

```cangjie
public struct KeyDeathAware <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop deathAware

```cangjie
public static prop deathAware: DeathAware
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyDryRun

```cangjie
public struct KeyDryRun <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop dryRun

```cangjie
public static prop dryRun: DryRun
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyExcludeTags

```cangjie
public struct KeyExcludeTags <: KeyFor<String> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop excludeTags

```cangjie
public static prop excludeTags: ExcludeTags
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyExplicitGC

```cangjie
public struct KeyExplicitGC <: KeyFor<ExplicitGcType> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop explicitGC

```cangjie
public static prop explicitGC: ExplicitGC
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyFilter

```cangjie
public struct KeyFilter <: KeyFor<String> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop filter

```cangjie
public static prop filter: Filter
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyFromTopLevel

```cangjie
public struct KeyFromTopLevel <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop fromTopLevel

```cangjie
public static prop fromTopLevel: FromTopLevel
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyGenerationSteps

```cangjie
public struct KeyGenerationSteps <: KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop generationSteps

```cangjie
public static prop generationSteps: GenerationSteps
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyHelp

```cangjie
public struct KeyHelp <: KeyFor<Bool> {}
```

功能：用于在配置信息中指定是否打印帮助信息。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop help

```cangjie
public static prop help: KeyHelp
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyIncludeTags

```cangjie
public struct KeyIncludeTags <: KeyFor<String> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop includeTags

```cangjie
public static prop includeTags: IncludeTags
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyInternalTestrunnerInputPath

```cangjie
public struct KeyInternalTestrunnerInputPath <: KeyFor<String> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop internalTestrunnerInputPath

```cangjie
public static prop internalTestrunnerInputPath: InternalTestrunnerInputPath
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyMeasurement

```cangjie
public struct KeyMeasurement <: KeyFor<Measurement> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop measurement

```cangjie
public static prop measurement: Measurement
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyMeasurementInfo

```cangjie
public struct KeyMeasurementInfo <: KeyFor<MeasurementInfo> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop measurementInfo

```cangjie
public static prop measurementInfo: MeasurementInfo
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyMinBatches

```cangjie
public struct KeyMinBatches <: KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop minBatches

```cangjie
public static prop minBatches: MinBatches
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyMinDuration

```cangjie
public struct KeyMinDuration <: KeyFor<Duration> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop minDuration

```cangjie
public static prop minDuration: MinDuration
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyNoCaptureOutput

```cangjie
public struct KeyNoCaptureOutput <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop noCaptureOutput

```cangjie
public static prop noCaptureOutput: NoCaptureOutput
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyNoColor

```cangjie
public struct KeyNoColor <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop noColor

```cangjie
public static prop noColor: NoColor
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyOptimizeMocksForBench

```cangjie
public struct KeyOptimizeMocksForBench <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop optimizeMocksForBench

```cangjie
public static prop optimizeMocksForBench: OptimizeMocksForBench
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyParallel

```cangjie
public struct KeyParallel <: KeyFor<Bool> & KeyFor<String> & KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop parallel

```cangjie
public static prop parallel: Parallel
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyRandomSeed

```cangjie
public struct KeyRandomSeed <: KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop randomSeed

```cangjie
public static prop randomSeed: RandomSeed
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyReductionSteps

```cangjie
public struct KeyReductionSteps <: KeyFor<Int64> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop reductionSteps

```cangjie
public static prop reductionSteps: ReductionSteps
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyReportFormat

```cangjie
public struct KeyReportFormat <: KeyFor<String> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop reportFormat

```cangjie
public static prop reportFormat: ReportFormat
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyReportPath

```cangjie
public struct KeyReportPath <: KeyFor<String> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop reportPath

```cangjie
public static prop reportPath: ReportPath
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyShowAllOutput

```cangjie
public struct KeyShowAllOutput <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop showAllOutput

```cangjie
public static prop showAllOutput: ShowAllOutput
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyShowTags

```cangjie
public struct KeyShowTags <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop showTags

```cangjie
public static prop showTags: ShowTags
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeySkip

```cangjie
public struct KeySkip <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop skip

```cangjie
public static prop skip: Skip
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyTimeout

```cangjie
public struct KeyTimeout <: KeyFor<Duration> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop timeout

```cangjie
public static prop timeout: Timeout
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyTimeoutEach

```cangjie
public struct KeyTimeoutEach <: KeyFor<String> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop timeoutEach

```cangjie
public static prop timeoutEach: TimeoutEach
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyTimeoutHandler

```cangjie
public struct KeyTimeoutHandler <: KeyFor<(TestCaseInfo) -> Unit> {}
```

功能：支持在配置信息中指定超时处理的句柄。

例如：

<!-- compile -->
```cangjie
let conf = Configuration()
conf.set(KeyTimeoutHandler.timeoutHandler, { info => /*...*/ })
```

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop timeoutHandler

```cangjie
public static prop timeoutHandler: KeyTimeoutHandler
```

功能：超时处理句柄。

类型：[KeyTimeoutHandler](#struct-keytimeouthandler)。

### prop name

```cangjie
public prop name: String
```

功能：超时处理句柄的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

## struct KeyVerbose

```cangjie
public struct KeyVerbose <: KeyFor<Bool> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop verbose

```cangjie
public static prop verbose: Verbose
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct KeyWarmup

```cangjie
public struct KeyWarmup <: KeyFor<Int64> & KeyFor<Duration> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 中作为对应配置项的键值。

父类型：

- [KeyFor](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop warmup

```cangjie
public static prop warmup: Warmup
```

功能：配置项的键值。

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

## struct MeasurementInfo

```cangjie
public struct MeasurementInfo {
    public let conversionTable: MeasurementUnitTable,
    public let name: String,
    public let textDescription: String
}
```

功能：存储测量信息的结构体。

### prop conversionTable

```cangjie
prop conversionTable: MeasurementUnitTable
```

功能：用于在性能测试报告中构建测量值的表示。
包含测量单位的边界对。
根据值的边界，使用最合适的单位。
对于 CSV 格式报告，始终选择下限以简化结果处理。
默认值为 `[(1.0, "")]`。

类型：[MeasurementUnitTable](../unittest_package_api/unittest_package_types.md#type-measurementunittable)。

### prop name

```cangjie
prop name: String
```

功能：当前 `Measurement` 类型的唯一显示名称。
有助于区分报告表中的不同测量类型。
默认值为 `Measurement`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### prop textDescription

```cangjie
prop textDescription: String
```

功能：描述此测量的简单文本将显示在某些报告中。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

## struct Perf

```cangjie
public struct Perf <: Measurement {
    public init()
    public Perf(counter: PerfCounter)
}
```

功能：使用 Linux 系统调用 `perf_event_open` 测量各种硬件和软件 CPU 计数器。仅在 Linux 上可用。

父类型：

- [Measurement](unittest_package_interfaces.md#interface-measurement)

### prop conversionTable

```cangjie
prop conversionTable: MeasurementUnitTable
```

功能：提供对应 CPU 计数器的换算表。

类型：[MeasurementUnitTable](../unittest_package_api/unittest_package_types.md#type-measurementunittable)。

### prop name

```cangjie
prop name: String
```

功能：为当前 CPU 计数器提供唯一的显示名称，例如：`Perf(cycles)`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### prop textDescription

```cangjie
prop textDescription: String
```

功能：描述此测量的简单文本将显示在某些报告中。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### init()

```cangjie
public init()
```

功能：使用 CPU 周期计数器的默认构造函数。

### Perf(PerfCounter)

```cangjie
public Perf(counter: PerfCounter)
```

功能：指定要测量的 CPU 计数器的构造函数。

参数：

- counter: [PerfCounter](../unittest_package_api/unittest_package_enums.md#enum-perfcounter) - 指定计数器。

### func measure()

```cangjie
public func measure(): Float64
```

功能：返回指定 CPU 计数器的值。

返回值：

- [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 计算得到的数据，用于统计分析。

### func setup()

```cangjie
func setup()
```

功能：此 CPU 计数器的初始化例程。在每个基准步骤之前调用。

## struct RelativeDelta\<T>

```cangjie
public struct RelativeDelta<T> {
    public RelativeDelta(let absolute!: T, let relative!: T) {}
}
```

功能：对于浮点类型，提供相对的 delta 数据类型来做近似相等的计算。计算公式如下。

$$|x - y| \le absolute + relative * max(abs(x), abs(y))$$

### RelativeDelta(T, T)

```cangjie
public RelativeDelta(let absolute!: T, let relative!: T)
```

功能：RelativeDelta 的主构造函数。

参数：

- absolute!: T - 绝对比较部分的 delta 值。
- relative!: T - 相对比较部分的 delta 值。

## struct TestCaseInfo

```cangjie
public struct TestCaseInfo {
    public let groupName: String
    public let suiteName: String
    public let caseName: String
}
```

功能：当前正在运行的测试用例的信息。通常在动态 API 的超时处理句柄中被使用。

### let caseName

```cangjie
public let caseName: String
```

功能：用例名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### let groupName

```cangjie
public let groupName: String
```

功能：用例的测试组名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### let suiteName

```cangjie
public let suiteName: String
```

功能：用例的测试套名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

## struct TimeNow

```cangjie
public struct TimeNow <: Measurement {
    public init()
    public init(unit: ?TimeUnit)
}
```

功能：[Measurement](../../unittest/unittest_package_api/unittest_package_interfaces.md#interface-measurement) 的实现，用于测量执行一个函数所花费的时间。

父类型：

- [Measurement](unittest_package_interfaces.md#interface-measurement)

### prop conversionTable

```cangjie
prop conversionTable: MeasurementUnitTable
```

功能：提供当前时间的单位换算表。
例如 `[(1.0, "ns"), (1e3, "us"), (1e6, "ms"), (1e9, "s")]`。

类型：[MeasurementUnitTable](../unittest_package_api/unittest_package_types.md#type-measurementunittable)。

### prop name

```cangjie
prop name: String
```

功能：提供当前时间单位唯一的显示名称，例如：`Duration(ns)` 或 `Duration(s)`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### prop textDescription

```cangjie
prop textDescription: String
```

功能：描述此测量的简单文本将显示在某些报告中。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)。

### init()

```cangjie
public init()
```

功能：自动选择输出格式的默认构造函数。

### init(?TimeUnit)

```cangjie
public init(unit: ?TimeUnit)
```

功能： `unit` 参数用于指定打印结果时将使用的时间单位。

参数：

- unit: ?[TimeUnit](unittest_package_enums.md#enum-timeunit) - 指定的时间单位。

### func measure()

```cangjie
public func measure(): Float64
```

功能：获取当前时间用于统计分析。

返回值：

- [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 计算得到的数据，用于统计分析。
