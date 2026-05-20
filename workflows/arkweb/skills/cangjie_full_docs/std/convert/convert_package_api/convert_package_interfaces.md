# 接口

## interface Formattable

```cangjie
public interface Formattable {
    func format(fmt: String): String
}
```

功能：该接口定义了格式化函数，即根据格式化参数将指定类型实例转换为对应格式的字符串。

格式化参数相关的说明请参见 convert 包中的[功能介绍](./../convert_package_overview.md#功能介绍)。

其他类型可通过实现该接口提供格式化功能。

### func format(String)

```cangjie
func format(fmt: String): String
```

功能：根据格式化参数将当前实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前实例格式化后得到的字符串。

### extend Float16 <: Formattable

```cangjie
extend Float16 <: Formattable
```

功能：为 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend Float32 <: Formattable

```cangjie
extend Float32 <: Formattable
```

功能：为 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend Float64 <: Formattable

```cangjie
extend Float64 <: Formattable
```

功能：为 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend Int16 <: Formattable

```cangjie
extend Int16 <: Formattable
```

功能：为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend Int32 <: Formattable

```cangjie
extend Int32 <: Formattable
```

功能：为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend Int64 <: Formattable

```cangjie
extend Int64 <: Formattable
```

功能：为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend Int8 <: Formattable

```cangjie
extend Int8 <: Formattable
```

功能：为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend Rune <: Formattable

```cangjie
extend Rune <: Formattable
```

功能：为 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend UInt16 <: Formattable

```cangjie
extend UInt16 <: Formattable
```

功能：为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend UInt32 <: Formattable

```cangjie
extend UInt32 <: Formattable
```

功能：为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend UInt64 <: Formattable

```cangjie
extend UInt64 <: Formattable
```

功能：为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

### extend UInt8 <: Formattable

```cangjie
extend UInt8 <: Formattable
```

功能：为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 扩展 [Formattable](convert_package_interfaces.md#interface-formattable) 接口，以实现将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 实例转换为格式化字符串。

父类型：

- [Formattable](#interface-formattable)

#### func format(String)

```cangjie
public func format(fmt: String): String
```

功能：根据格式化参数将当前 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型实例格式化为对应格式的字符串。

参数：

- fmt: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化参数。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将当前 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型实例格式化后得到的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 fmt 不合法时抛出异常。

## interface Parsable\<T>

```cangjie
public interface Parsable<T> {
    static func parse(value: String): T
    static func tryParse(value: String): Option<T>
}
```

功能：本接口提供了统一的方法，以支持将字符串解析为特定类型。

本接口提供了 parse 和 tryParse 两套方法，parse 方法将在解析失败时抛出异常，tryParse 方法将返回值用 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 包裹，解析失败时将返回 None。
本包内已经为 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool)，[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)，[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)，[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 等基础类型实现该接口，可用于将字符串转换为这些类型。

### static func parse(String)

```cangjie
static func parse(value: String): T
```

功能：从字符串中解析特定类型。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待解析的字符串。

返回值：

- T - 转换后的值。

### static func tryParse(String)

```cangjie
static func tryParse(value: String): Option<T>
```

功能：从字符串中解析特定类型。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待解析的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 转换后值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T>.None。

### extend Bool <: Parsable\<Bool>

```cangjie
extend Bool <: Parsable<Bool>
```

功能：此扩展主要用于实现将 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型字面量的字符串转换为 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)>

#### static func parse(String)

```cangjie
public static func parse(data: String): Bool
```

功能：将 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型字面量的字符串转换为 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回转换后 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空或转换失败时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<Bool>
```

功能：将 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)>.None。

### extend Float16 <: Parsable\<Float16>

```cangjie
extend Float16 <: Parsable<Float16>
```

功能：此扩展主要用于实现将 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型字面量的字符串转换为 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值的相关操作函数。

> **注意：**
>
> 目前不支持二进制和八进制的浮点数转换。

父类型：

- [Parsable](#interface-parsablet)\<[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)>

#### static func parse(String)

```cangjie
public static func parse(data: String): Float16
```

功能：将 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型字面量的字符串转换为 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - 返回转换后 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串不符合浮点数语法时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<Float16>
```

功能：将 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)>.None。

### extend Float32 <: Parsable\<Float32>

```cangjie
extend Float32 <: Parsable<Float32>
```

功能：此扩展主要用于实现将 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型字面量的字符串转换为 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值的相关操作函数。

> **注意：**
>
> 目前不支持二进制和八进制的浮点数转换。

父类型：

- [Parsable](#interface-parsablet)\<[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)>

#### static func parse(String)

```cangjie
public static func parse(data: String): Float32
```

功能：将 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型字面量的字符串转换为 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - 返回转换后 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串不符合浮点数语法时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<Float32>
```

功能：将 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)>.None。

### extend Float64 <: Parsable\<Float64>

```cangjie
extend Float64 <: Parsable<Float64>
```

功能：此扩展主要用于实现将 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型字面量的字符串转换为 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值的相关操作函数。

> **注意：**
>
> 目前不支持二进制和八进制的浮点数转换。

父类型：

- [Parsable](#interface-parsablet)\<[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)>

#### static func parse(String)

```cangjie
public static func parse(data: String): Float64
```

功能：将 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型字面量的字符串转换为 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 返回转换后 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串不符合浮点数语法时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<Float64>
```

功能：将 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)>.None。

### extend Int16 <: Parsable\<Int16>

```cangjie
extend Int16 <: Parsable<Int16>
```

功能：此扩展主要用于实现将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型字面量的字符串转换为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### static func parse(String)

```cangjie
public static func parse(data: String): Int16
```

功能：将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型字面量的字符串转换为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 返回转换后 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，首位为 `+` ，转换失败，或转换后超出 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 范围，或字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<Int16>
```

功能：将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>.None。

### extend Int32 <: Parsable\<Int32>

```cangjie
extend Int32 <: Parsable<Int32>
```

功能：此扩展主要用于实现将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型字面量的字符串转换为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### static func parse(String)

```cangjie
public static func parse(data: String): Int32
```

功能：将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型字面量的字符串转换为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回转换后 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，首位为 `+` ，转换失败，或转换后超出 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 范围，或字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<Int32>
```

功能：将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>.None。

### extend Int64 <: Parsable\<Int64>

```cangjie
extend Int64 <: Parsable<Int64>
```

功能：此扩展主要用于实现将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型字面量的字符串转换为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>

#### static func parse(String)

```cangjie
public static func parse(data: String): Int64
```

功能：将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型字面量的字符串转换为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回转换后 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，首位为 `+` ，转换失败，或转换后超出 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 范围，或字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<Int64>
```

功能：将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>.None。

### extend Int8 <: Parsable\<Int8>

```cangjie
extend Int8 <: Parsable<Int8>
```

功能：此扩展主要用于实现将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型字面量的字符串转换为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### static func parse(String)

```cangjie
public static func parse(data: String): Int8
```

功能：将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型字面量的字符串转换为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 返回转换后 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，首位为 `+` ，转换失败，或转换后超出 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 范围，或字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<Int8>
```

功能：将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>.None。

### extend Rune <: Parsable\<Rune>

```cangjie
extend Rune <: Parsable<Rune>
```

功能：此扩展主要用于实现将 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型字面量的字符串转换为 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)>

#### static func parse(String)

```cangjie
public static func parse(data: String): Rune
```

功能：将 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型字面量的字符串转换为 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) - 返回转换后 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，或转换失败时，或字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<Rune>
```

功能：将 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)>.None。

### extend UInt16 <: Parsable\<UInt16>

```cangjie
extend UInt16 <: Parsable<UInt16>
```

功能：此扩展主要用于实现将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型字面量的字符串转换为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### static func parse(String)

```cangjie
public static func parse(data: String): UInt16
```

功能：将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型字面量的字符串转换为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 返回转换后 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，首位为 `+` 或 `-`，转换失败，或转换后超出 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 范围，或字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<UInt16>
```

功能：将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>.None。

### extend UInt32 <: Parsable\<UInt32>

```cangjie
extend UInt32 <: Parsable<UInt32>
```

功能：此扩展主要用于实现将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型字面量的字符串转换为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### static func parse(String)

```cangjie
public static func parse(data: String): UInt32
```

功能：将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型字面量的字符串转换为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 返回转换后 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，首位为 `+` 或 `-`，转换失败，或转换后超出 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 范围，或字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<UInt32>
```

功能：将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>.None。

### extend UInt64 <: Parsable\<UInt64>

```cangjie
extend UInt64 <: Parsable<UInt64>
```

功能：此扩展主要用于实现将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型字面量的字符串转换为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### static func parse(String)

```cangjie
public static func parse(data: String): UInt64
```

功能：将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型字面量的字符串转换为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 返回转换后 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，首位为 `+` 或 `-`，转换失败，或转换后超出 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 范围，或字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<UInt64>
```

功能：将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>.None。

### extend UInt8 <: Parsable\<UInt8>

```cangjie
extend UInt8 <: Parsable<UInt8>
```

功能：此扩展主要用于实现将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型字面量的字符串转换为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值的相关操作函数。

父类型：

- [Parsable](#interface-parsablet)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### static func parse(String)

```cangjie
public static func parse(data: String): UInt8
```

功能：将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型字面量的字符串转换为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 返回转换后 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，首位为 `+` 或 `-`，转换失败，或转换后超出 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 范围，或字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String)

```cangjie
public static func tryParse(data: String): Option<UInt8>
```

功能：将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> 值。

参数：

- data: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>.None。

## interface RadixConvertible\<T>

```cangjie
public interface RadixConvertible<T> {
    
    static func parse(value: String, radix!: Int64): T

    static func tryParse(value: String, radix!: Int64): Option<T>

    func toString(radix!: Int64): String
}
```

功能：本接口提供了统一的方法，以支持将指定进制的字符串解析为特定类型。

进制将以参数指定，不按字符串前缀指定，进制表示范围必须在 2-36 之间，否则会抛异常，超过十进制的表示按大或者小写英文字母序表示，即 10 个数字 + 26 个英文字母 = 36 进制，Int 系列的字符串可以以 `+`、`-` 开头，如果不以这两个符号开头则处理成 `+`，UInt 系列的字符串可以以 `+` 开头，如果以 `-` 开头会抛出异常。返回指定进制形式字符串，超过十进制的表示按小写英文字母序表示，即 10 个数字 + 26 个小写英文字母 = 36 进制。

本接口提供了 parse 和 tryParse 两套方法，parse 方法将在解析失败时抛出异常，tryParse 方法将返回值用 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 包裹，解析失败时将返回 None。
本包内已经为[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)，[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 等基础类型实现该接口，可用于将字符串转换为这些类型。

### static func parse(String, Int64)

```cangjie
static func parse(value: String, radix!: Int64): T
```

功能：从指定进制字符串中解析特定类型。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待解析的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- T - 转换后的值。

### static func tryParse(String, Int64)

```cangjie
static func tryParse(value: String, radix!: Int64): Option<T>
```

功能：从指定进制字符串中解析特定类型。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待解析的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 转换后值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T>.None。

### func toString(Int64)

```cangjie
func toString(radix!: Int64): String
```

功能：返回指定进制形式字符串。

参数：

- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定进制形式字符串。

### extend Int16 <: RadixConvertible\<Int16>

```cangjie
extend Int16 <: RadixConvertible<Int16>
```

功能：此扩展主要用于实现将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型字面量的字符串转换为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值的相关操作函数。

父类型：

- [RadixConvertible](#interface-radixconvertiblet)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### static func parse(String, Int64)

```cangjie
public static func parse(value: String, radix!: Int64): Int16
```

功能：将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型字面量的字符串转换为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 返回转换后 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空、进制超出范围、转换后超出 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 范围、字符串中含有无效的 UTF-8 字符、转换失败时，抛出异常。

#### static func tryParse(String, Int64)

```cangjie
public static func tryParse(value: String, radix!: Int64): Option<Int16>
```

功能：将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)> 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>.None。

#### func toString(Int64)

```cangjie
public func toString(radix!: Int64): String
```

功能：返回指定进制形式字符串。

参数：

- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定进制形式字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当进制不合规时，抛出异常。

### extend Int32 <: RadixConvertible\<Int32>

```cangjie
extend Int32 <: RadixConvertible<Int32>
```

功能：此扩展主要用于实现将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型字面量的字符串转换为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值的相关操作函数。

父类型：

- [RadixConvertible](#interface-radixconvertiblet)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### static func parse(String, Int64)

```cangjie
public static func parse(value: String, radix!: Int64): Int32
```

功能：将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型字面量的字符串转换为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回转换后 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空、进制超出范围、转换后超出 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 范围、字符串中含有无效的 UTF-8 字符、转换失败时，抛出异常。

#### static func tryParse(String, Int64)

```cangjie
public static func tryParse(value: String, radix!: Int64): Option<Int32>
```

功能：将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)> 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>.None。

#### func toString(Int64)

```cangjie
public func toString(radix!: Int64): String
```

功能：返回指定进制形式字符串。

参数：

- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定进制形式字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当进制不合规时，抛出异常。

### extend Int64 <: RadixConvertible\<Int64>

```cangjie
extend Int64 <: RadixConvertible<Int64>
```

功能：此扩展主要用于实现将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型字面量的字符串转换为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值的相关操作函数。

父类型：

- [RadixConvertible](#interface-radixconvertiblet)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>

#### static func parse(String, Int64)

```cangjie
public static func parse(value: String, radix!: Int64): Int64
```

功能：将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型字面量的字符串转换为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回转换后 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空、进制超出范围、转换后超出 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 范围、字符串中含有无效的 UTF-8 字符、转换失败时，抛出异常。

#### static func tryParse(String, Int64)

```cangjie
public static func tryParse(value: String, radix!: Int64): Option<Int64>
```

功能：将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>.None。

#### func toString(Int64)

```cangjie
public func toString(radix!: Int64): String
```

功能：返回指定进制形式字符串。

参数：

- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定进制形式字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当进制不合规时，抛出异常。

### extend Int8 <: RadixConvertible\<Int8>

```cangjie
extend Int8 <: RadixConvertible<Int8>
```

功能：此扩展主要用于实现将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型字面量的字符串转换为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值的相关操作函数。

父类型：

- [RadixConvertible](#interface-radixconvertiblet)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### static func parse(String, Int64)

```cangjie
public static func parse(value: String, radix!: Int64): Int8
```

功能：将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型字面量的字符串转换为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 返回转换后 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空，进制超出范围，转换后超出 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 范围或字符串中含有无效的 UTF-8 字符，转换失败时，抛出异常。

#### static func tryParse(String, Int64)

```cangjie
public static func tryParse(value: String, radix!: Int64): Option<Int8>
```

功能：将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)> 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>.None。

#### func toString(Int64)

```cangjie
public func toString(radix!: Int64): String
```

功能：返回指定进制形式字符串。

参数：

- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定进制形式字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当进制不合规时，抛出异常。

### extend UInt16 <: RadixConvertible\<UInt16>

```cangjie
extend UInt16 <: RadixConvertible<UInt16>
```

功能：此扩展主要用于实现将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型字面量的字符串转换为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值的相关操作函数。

父类型：

- [RadixConvertible](#interface-radixconvertiblet)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### static func parse(String, Int64)

```cangjie
public static func parse(value: String, radix!: Int64): UInt16
```

功能：将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型字面量的字符串转换为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 返回转换后 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空、进制超出范围、首位为 `-`、转换后超出 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 范围、字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String, Int64)

```cangjie
public static func tryParse(value: String, radix!: Int64): Option<UInt16>
```

功能：将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)> 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>.None。

#### func toString(Int64)

```cangjie
public func toString(radix!: Int64): String
```

功能：返回指定进制形式字符串。

参数：

- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定进制形式字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当进制不合规时，抛出异常。

### extend UInt32 <: RadixConvertible\<UInt32>

```cangjie
extend UInt32 <: RadixConvertible<UInt32>
```

功能：此扩展主要用于实现将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型字面量的字符串转换为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值的相关操作函数。

父类型：

- [RadixConvertible](#interface-radixconvertiblet)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### static func parse(String, Int64)

```cangjie
public static func parse(value: String, radix!: Int64): UInt32
```

功能：将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型字面量的字符串转换为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 返回转换后 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空、进制超出范围、首位为 `-`、转换后超出 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 范围、字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String, Int64)

```cangjie
public static func tryParse(value: String, radix!: Int64): Option<UInt32>
```

功能：将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)> 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>.None。

#### func toString(Int64)

```cangjie
public func toString(radix!: Int64): String
```

功能：返回指定进制形式字符串。

参数：

- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定进制形式字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当进制不合规时，抛出异常。

### extend UInt64 <: RadixConvertible\<UInt64>

```cangjie
extend UInt64 <: RadixConvertible<UInt64>
```

功能：此扩展主要用于实现将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型字面量的字符串转换为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值的相关操作函数。

父类型：

- [RadixConvertible](#interface-radixconvertiblet)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### static func parse(String, Int64)

```cangjie
public static func parse(value: String, radix!: Int64): UInt64
```

功能：将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型字面量的字符串转换为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 返回转换后 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空、进制超出范围、首位为 `-`、转换后超出 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 范围、字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String, Int64)

```cangjie
public static func tryParse(value: String, radix!: Int64): Option<UInt64>
```

功能：将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)> 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>.None。

#### func toString(Int64)

```cangjie
public func toString(radix!: Int64): String
```

功能：返回指定进制形式字符串。

参数：

- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定进制形式字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当进制不合规时，抛出异常。

### extend UInt8 <: RadixConvertible\<UInt8>

```cangjie
extend UInt8 <: RadixConvertible<UInt8>
```

功能：此扩展主要用于实现将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型字面量的字符串转换为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值的相关操作函数。

父类型：

- [RadixConvertible](#interface-radixconvertiblet)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### static func parse(String, Int64)

```cangjie
public static func parse(value: String, radix!: Int64): UInt8
```

功能：将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型字面量的字符串转换为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 返回转换后 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串为空、进制超出范围、首位为 `-`、转换后超出 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 范围、字符串中含有无效的 UTF-8 字符时，抛出异常。

#### static func tryParse(String, Int64)

```cangjie
public static func tryParse(value: String, radix!: Int64): Option<UInt8>
```

功能：将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型字面量的字符串转换为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> 值。

参数：

- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要转换的字符串。
- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 返回转换后 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> 值，转换失败返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>.None。

#### func toString(Int64)

```cangjie
public func toString(radix!: Int64): String
```

功能：返回指定进制形式字符串。

参数：

- radix!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的进制。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定进制形式字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当进制不合规时，抛出异常。
