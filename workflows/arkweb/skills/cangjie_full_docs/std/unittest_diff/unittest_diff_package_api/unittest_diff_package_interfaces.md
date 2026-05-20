# 接口

## interface AssertPrintable

```cangjie
public interface AssertPrintable<T> {
    prop hasNestedDiff: Bool
    func pprintForAssertion(
        pp: PrettyPrinter, that: T, thisPrefix: String, thatPrefix: String, level: Int64
    ): PrettyPrinter
}
```

功能：提供打印 [@Assert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏)/[@Expect](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) 的检查结果的方法。

### prop hasNestedDiff

```cangjie
prop hasNestedDiff: Bool
```

功能：获取是否有嵌套 diff 层级。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

### func pprintForAssertion(PrettyPrinter, T, String, String, Int64)

```cangjie
func pprintForAssertion(
    pp: PrettyPrinter, that: T, thisPrefix: String, thatPrefix: String, level: Int64
): PrettyPrinter
```

功能：打印 [@Assert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏)/[@Expect](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) 的检查结果的方法。

参数：

- pp: [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) - 打印器。
- that: T - 待打印的信息。
- thisPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 预期内容的前缀。
- thatPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际内容的前缀。
- level: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 嵌套层级。

返回值：

- PrettyPrinter - 打印器。

### extend Float16 <: AssertPrintable\<Float16>

```cangjie
extend Float16 <: AssertPrintable<Float16>
```

功能：对 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 的扩展。

#### prop hasNestedDiff

```cangjie
public prop hasNestedDiff: Bool
```

功能：获取是否有嵌套 diff 层级。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

#### func pprintForAssertion(PrettyPrinter, Float16, String, String, Int64)

```cangjie
public func pprintForAssertion(
    pp: PrettyPrinter, that: Float16, thisPrefix: String, thatPrefix: String, level: Int64
): PrettyPrinter
```

功能：打印 [@Assert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏)/[@Expect](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) 的检查结果的方法。

参数：

- pp: [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) - 打印器。
- that: [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - 待打印的信息。
- thisPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 预期内容的前缀。
- thatPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际内容的前缀。
- level: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 嵌套层级。

返回值：

- PrettyPrinter - 打印器。

### extend Float32 <: AssertPrintable\<Float32>

```cangjie
extend Float32  <: AssertPrintable<Float32>
```

功能：对 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 的扩展。

#### prop hasNestedDiff

```cangjie
public prop hasNestedDiff: Bool
```

功能：获取是否有嵌套 diff 层级。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

#### func pprintForAssertion(PrettyPrinter, Float32, String, String, Int64)

```cangjie
public func pprintForAssertion(
    pp: PrettyPrinter, that: Float32, thisPrefix: String, thatPrefix: String, level: Int64
): PrettyPrinter
```

功能：打印 [@Assert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏)/[@Expect](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) 的检查结果的方法。

参数：

- pp: [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) - 打印器。
- that: [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - 待打印的信息。
- thisPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 预期内容的前缀。
- thatPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际内容的前缀。
- level: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 嵌套层级。

返回值：

- PrettyPrinter - 打印器。

### extend Float64 <: AssertPrintable\<Float64>

```cangjie
extend Float64 <: AssertPrintable<Float64>
```

功能：对 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 的扩展。

#### prop hasNestedDiff

```cangjie
public prop hasNestedDiff: Bool
```

功能：获取是否有嵌套 diff 层级。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

#### func pprintForAssertion(PrettyPrinter, Float64, String, String, Int64)

```cangjie
public func pprintForAssertion(
    pp: PrettyPrinter, that: Float64, thisPrefix: String, thatPrefix: String, level: Int64
): PrettyPrinter
```

功能：打印 [@Assert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏)/[@Expect](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) 的检查结果的方法。

参数：

- pp: [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) - 打印器。
- that: [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 待打印的信息。
- thisPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 预期内容的前缀。
- thatPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际内容的前缀。
- level: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 嵌套层级。

返回值：

- PrettyPrinter - 打印器。

### extend\<T> Option\<T> <: AssertPrintable\<Option\<T>> where T <: Equatable\<T>

```cangjie
extend<T> Option<T> <: AssertPrintable<Option<T>> where T <: Equatable<T> 
```

功能：对 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> 的扩展。

#### prop hasNestedDiff

```cangjie
public prop hasNestedDiff: Bool
```

功能：获取是否有嵌套 diff 层级。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

#### func pprintForAssertion(PrettyPrinter,  Option\<T>, String, String, Int64)

```cangjie
public func pprintForAssertion(
    pp: PrettyPrinter, that:  Option<T>, thisPrefix: String, thatPrefix: String, level: Int64
): PrettyPrinter
```

功能：打印 [@Assert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏)/[@Expect](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) 的检查结果的方法。

参数：

- pp: [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) - 打印器。
- that:  [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 待打印的信息。
- thisPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 预期内容的前缀。
- thatPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际内容的前缀。
- level: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 嵌套层级。

返回值：

- PrettyPrinter - 打印器。

### extend String <: AssertPrintable\<String>

```cangjie
extend String <: AssertPrintable<String>
```

功能：对 [String](../../core/core_package_api/core_package_structs.md#struct-string) 的扩展。

#### prop hasNestedDiff

```cangjie
public prop hasNestedDiff: Bool
```

功能：获取是否有嵌套 diff 层级。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

#### func pprintForAssertion(PrettyPrinter, String, String, String, Int64)

```cangjie
public func pprintForAssertion(
    pp: PrettyPrinter, that: String, thisPrefix: String, thatPrefix: String, level: Int64
): PrettyPrinter
```

功能：打印 [@Assert](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#assert-宏)/[@Expect](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#expect-宏) 的检查结果的方法。

参数：

- pp: [PrettyPrinter](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-prettyprinter) - 打印器。
- that: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待打印的信息。
- thisPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 预期内容的前缀。
- thatPrefix: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 实际内容的前缀。
- level: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 嵌套层级。

返回值：

- PrettyPrinter - 打印器。
