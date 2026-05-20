# 接口

## interface BenchInputProvider

```cangjie
public interface BenchInputProvider<T> <: BenchmarkInputMarker  {
    mut func get(idx: Int64): T
    mut func reset(max: Int64)
}
```

功能：当某些代码需要在性能测试执行前执行，或当输入变化就需要重新执行一段代码时，可实现本接口。同时 [DataStrategy](../../unittest_common/unittest_common_package_api/unittest_common_package_interfaces.md#interface-datastrategy) 的实现类型应返回此接口的实现类型。

用户一般不需要自行实现该接口，可直接使用 [@Strategy](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#strategy-宏) 宏。

父类型：

- [BenchmarkInputMarker](#interface-benchmarkinputmarker)

### func get(Int64)

```cangjie
mut func get(idx: Int64): T
```

功能：获取元素。该函数的执行时间包含在基准测量中，然后作为框架开销计算的一部分从结果中排除。

参数：

- idx: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 元素索引值。

返回值：

- T - 元素值。

### func reset(Int64)

```cangjie
mut func reset(max: Int64)
```

功能：在基准测量之前调用。调用此函数后，后续的 `get(i)` 调用必须成功获取 [0, max) 中的 `i` 。

参数：

- max: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 最大值。

## interface BenchmarkConfig

```cangjie
public interface BenchmarkConfig {
    func batchSize(b: Int64): Unit
    func batchSize(x: Range<Int64>): Unit
    func warmup(x: Int64): Unit
    func warmup(x: Duration): Unit
    func minDuration(x: Duration): Unit
    func explicitGC(x: ExplicitGcType): Unit
    func minBatches(x: Int64): Unit
}
```

功能：该接口提供为 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 宏配置性能测试相关信息的函数签名。

### func batchSize(Int64)

```cangjie
func batchSize(b: Int64): Unit
```

功能：可实现该函数，为 `@Configuration` 宏配置批次的大小。

参数：

- b: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 需配置的批次大小值。

### func batchSize(Range\<Int64>): Unit

```cangjie
func batchSize(x: Range<Int64>): Unit
```

功能：可实现该函数，为 `@Configuration` 宏配置批次的大小。

参数：

- x: [Range](../../core/core_package_api/core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet)<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> - 需配置的批次大小范围值。

### func explicitGC(ExplicitGcType)

```cangjie
func explicitGC(x: ExplicitGcType): Unit
```

功能：可实现该函数，为 `@Configuration` 宏配置 GC 的类型。

参数：

- x: [ExplicitGcType](../unittest_package_api/unittest_package_enums.md#enum-explicitgctype) - 需配置的 GC 类型值。

### func minBatches(Int64)

```cangjie
func minBatches(x: Int64): Unit
```

功能：可实现该函数，为 `@Configuration` 宏配置最小批次个数。

参数：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 需配置的最小批次个数。

### func minDuration(Duration)

```cangjie
func minDuration(x: Duration): Unit
```

功能：可实现该函数，为 `@Configuration` 宏配置性能测试最小执行时间。

参数：

- x: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 需配置的性能测试最小执行时间。

### func warmup(Int64)

```cangjie
func warmup(x: Int64): Unit
```

功能：可实现该函数，为 `@Configuration` 宏配置预热期的执行次数。

参数：

- x: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 需配置的预热期的执行次数。

### func warmup(Duration)

```cangjie
func warmup(x: Duration): Unit
```

功能：可实现该函数，为 `@Configuration` 宏配置预热期的执行时间。

参数：

- x: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 需配置的预热期的执行时间。

### extend Configuration <: BenchmarkConfig

```cangjie
extend Configuration <: BenchmarkConfig {}
```

功能：为 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 扩展 [BenchmarkConfig](../../unittest/unittest_package_api/unittest_package_interfaces.md#interface-benchmarkconfig) 接口。

父类型：

- [BenchmarkConfig](../../unittest/unittest_package_api/unittest_package_interfaces.md#interface-benchmarkconfig)

#### func batchSize(Int64)

```cangjie
public func batchSize(b: Int64)
```

功能：配置性能测试时一个批次的执行次数。

参数：

- b: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 执行次数。

#### func batchSize(Range\<Int64>)

```cangjie
public func batchSize(x: Range<Int64>)
```

功能：配置性能测试时一个批次的执行次数范围。

参数：

- b: [Range](../../core/core_package_api/core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet)\<Int64> - 执行次数范围。

#### func explicitGC(ExplicitGcType)

```cangjie
public func explicitGC(x: ExplicitGcType)
```

功能：配置性能测试时执行 GC 的方式。

参数：

- x: [ExplicitGcType](../../unittest/unittest_package_api/unittest_package_enums.md#enum-explicitgctype) - GC 执行的方式。

#### func minBatches(Int64)

```cangjie
public func minBatches(x: Int64)
```

功能：配置性能测试时最少的批次数。

参数：

- x: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 最少的批次数。

#### func minDuration(Duration)

```cangjie
public func minDuration(x: Duration)
```

功能：配置性能测试时最短的执行时长。

参数：

- x: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 最短的执行时长。

#### func warmup(Int64)

```cangjie
public func warmup(x: Int64)
```

功能：配置性能测试时预热的秒数。

参数：

- x: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 预热的秒数。

#### func warmup(Duration)

```cangjie
public func warmup(x: Duration)
```

功能：配置性能测试时预热的时长。

参数：

- x: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 预热的时长。

## interface BenchmarkInputMarker

```cangjie
public interface BenchmarkInputMarker
```

功能：当我们不知道 `T` 时，该接口能够检测 `BenchInputProvider<T>` 。

## interface Measurement

```cangjie
public interface Measurement {
    prop conversionTable: MeasurementUnitTable
    prop name: String
    prop textDescription: String
    func setup(): Unit
    func measure(): Float64
    prop info: MeasurementInfo
}
```

功能：该接口指定如何在性能测试期间测量数据以及如何在报告中显示数据。
实现接口的实例可以作为宏 `@Measure` 的属性传递。

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

### func measure()

```cangjie
func measure(): Float64
```

功能：将用于统计分析的测量运行时间的方法。

返回值：

- [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 测量得到的数据。

### func setup()

```cangjie
func setup()
```

功能：此测量的初始化例程。在每个基准步骤之前调用。

### prop info

功能：具体测量的汇总信息。

类型: [MeasurementInfo](../unittest_package_api/unittest_package_structs.md#struct-measurementinfo)

## interface NearEquatable\<CT, D>

```cangjie
public interface NearEquatable<CT, D> {
    func isNear(obj: CT, delta!: D): Bool
} 
```

功能：判断某个对象是否基于这个 delta 近似相等。

### func isNear(CT, D)

```cangjie
public func isNear(obj: CT, delta!: D): Bool
```

功能：判断某个对象是否基于这个 delta 近似相等。

参数：

- obj: CT - 被比较的对象。
- delta!: D - 判断近似相等的 delta。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否近似相等。

### extend Float16 <: NearEquatable\<Float16, Float16>

功能：对类型 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 扩展接口 [NearEquatable](#interface-nearequatablect-d)。

#### func isNear(Float16, Float16)

```cangjie
public func isNear(obj: Float16, delta!: Float16): Bool
```

功能：判断某个对象是否基于这个 delta 近似相等。

参数：

- obj: [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - 被比较的对象。
- delta!: [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - 判断近似相等的 delta。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否近似相等。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - delta 值不能为负数，且不是 NaN, 否则将抛出该异常。

### extend Float16 <: NearEquatable\<Float16, RelativeDelta\<Float16>>

功能：对类型 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 扩展接口 [NearEquatable](#interface-nearequatablect-d)，且使用 [RelativeDelta](../unittest_package_api/unittest_package_structs.md#struct-relativedeltat) 做近似计算。

#### func isNear(Float16, RelativeDelta\<Float16>)

```cangjie
public func isNear(obj: Float16, delta!: RelativeDelta<Float16>): Bool
```

功能：判断某个对象是否基于这个 delta 近似相等。

参数：

- obj: [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - 被比较的对象。
- delta!: [RelativeDelta](../unittest_package_api/unittest_package_structs.md#struct-relativedeltat)\<[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)> - 判断近似相等的 delta。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否近似相等。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - delta 值不能为负数，且不是 NaN，否则将抛出该异常。

### extend Float32 <: NearEquatable\<Float32, Float32>

功能：对类型 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 扩展接口 [NearEquatable](#interface-nearequatablect-d)。

#### func isNear(Float32, Float32)

```cangjie
public func isNear(obj: Float32, delta!: Float32): Bool
```

功能：判断某个对象是否基于这个 delta 近似相等。

参数：

- obj: [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - 被比较的对象。
- delta!: [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - 判断近似相等的 delta。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否近似相等。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - delta 值不能为负数，且不是 NaN，否则将抛出该异常。

### extend Float32 <: NearEquatable\<Float32, RelativeDelta\<Float32>>

功能：对类型 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 扩展接口 [NearEquatable](#interface-nearequatablect-d)，且使用 [RelativeDelta](../unittest_package_api/unittest_package_structs.md#struct-relativedeltat) 做近似计算。

#### func isNear(Float32, RelativeDelta\<Float32>)

```cangjie
public func isNear(obj: Float32, delta!: RelativeDelta<Float32>): Bool
```

功能：判断某个对象是否基于这个 delta 近似相等。

参数：

- obj: [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - 被比较的对象。
- delta!: [RelativeDelta](../unittest_package_api/unittest_package_structs.md#struct-relativedeltat)\<[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)> - 判断近似相等的 delta。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否近似相等。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - delta 值不能为负数，且不是 NaN，否则将抛出该异常。

### extend Float64 <: NearEquatable\<Float64, Float64>

功能：对类型 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 扩展接口 [NearEquatable](#interface-nearequatablect-d)。

#### func isNear(Float64, Float64)

```cangjie
public func isNear(obj: Float64, delta!: Float64): Bool
```

功能：判断某个对象是否基于这个 delta 近似相等。

参数：

- obj: [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 被比较的对象。
- delta!: [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 判断近似相等的 delta。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否近似相等。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - delta 值不能为负数，且不是 NaN，否则将抛出该异常。

### extend Float64 <: NearEquatable\<Float64, RelativeDelta\<Float64>>

功能：对类型 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 扩展接口 [NearEquatable](#interface-nearequatablect-d)，且使用 [RelativeDelta](../unittest_package_api/unittest_package_structs.md#struct-relativedeltat) 做近似计算。

#### func isNear(Float64, RelativeDelta\<Float64>)

```cangjie
public func isNear(obj: Float64, delta!: RelativeDelta<Float64>): Bool
```

功能：判断某个对象是否基于这个 delta 近似相等。

参数：

- obj: [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 被比较的对象。
- delta!: [RelativeDelta](../unittest_package_api/unittest_package_structs.md#struct-relativedeltat)\<[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)> - 判断近似相等的 delta。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否近似相等。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - delta 值不能为负数，且不是 NaN，否则将抛出该异常。

## interface Reporter

```cangjie
sealed interface Reporter <TReport, TReturn>
```

功能：报告器基础接口。

## interface TestClass

```cangjie
public interface TestClass {
    func asTestSuite(): TestSuite
}
```

功能：提供创建 [TestSuite](./unittest_package_classes.md#class-testsuite) 的方法。

### func asTestSuite()

```cangjie
func asTestSuite(): TestSuite
```

功能：创建 [TestSuite](./unittest_package_classes.md#class-testsuite) 的方法。

返回值：

- [TestSuite](./unittest_package_classes.md#class-testsuite) - 测试套对象。
