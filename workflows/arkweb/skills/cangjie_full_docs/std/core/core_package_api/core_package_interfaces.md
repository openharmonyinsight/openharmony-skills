# 接口

## interface Any

```cangjie
public interface Any {}
```

功能：[Any](core_package_interfaces.md#interface-any) 是所有类型的父类型，所有 `interface` 都默认继承它，所有非 `interface` 类型都默认实现它。

### extend Byte

```cangjie
extend Byte
```

功能：为 [Byte](core_package_types.md#type-byte) 类型实现一系列扩展方法，主要为在 Ascii 字符集范围内的一些字符判断、转换等操作。

#### func isAscii()

```cangjie
public func isAscii(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 范围内。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 范围内返回 true，否则返回 false。

#### func isAsciiControl()

```cangjie
public func isAsciiControl(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 控制字符范围内。其取值范围为 [00, 1F] 和 {7F} 的并集。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 控制字符范围内返回 true，否则返回 false。

#### func isAsciiGraphic()

```cangjie
public func isAsciiGraphic(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 图形字符范围内。其取值范围为 [21, 7E]。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 图形字符范围内返回 true，否则返回 false。

#### func isAsciiHex()

```cangjie
public func isAsciiHex(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 十六进制数字范围内。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 十六进制数字范围内返回 true，否则返回 false。

#### func isAsciiLetter()

```cangjie
public func isAsciiLetter(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 拉丁字母范围内。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 拉丁字母范围内返回 true，否则返回 false。

#### func isAsciiLowerCase()

```cangjie
public func isAsciiLowerCase(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 小写拉丁字母范围内。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 小写拉丁字母范围内返回 true，否则返回 false。

#### func isAsciiNumber()

```cangjie
public func isAsciiNumber(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 十进制数字范围内。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 十进制数字范围内返回 true，否则返回 false。

#### func isAsciiNumberOrLetter()

```cangjie
public func isAsciiNumberOrLetter(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 十进制数字和拉丁字母范围内。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 十进制数字和拉丁字母范围内返回 true，否则返回 false。

#### func isAsciiOct()

```cangjie
public func isAsciiOct(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 八进制数字范围内。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 八进制数字范围内返回 true，否则返回 false。

#### func isAsciiPunctuation()

```cangjie
public func isAsciiPunctuation(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 标点符号范围内。其取值范围为 [21, 2F]、[3A, 40]、[5B, 60] 和 [7B, 7E] 的并集。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 标点符号范围内返回 true，否则返回 false。

#### func isAsciiUpperCase()

```cangjie
public func isAsciiUpperCase(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 大写拉丁字母范围内。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 大写拉丁字母范围内返回 true，否则返回 false。

#### func isAsciiWhiteSpace()

```cangjie
public func isAsciiWhiteSpace(): Bool
```

功能：判断 [Byte](core_package_types.md#type-byte) 是否是在 Ascii 空白字符范围内。其取值范围为 [09, 0D] 和 {20} 的并集。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果 [Byte](core_package_types.md#type-byte) 在 Ascii 空白字符范围内返回 true，否则返回 false。

#### func toAsciiLowerCase()

```cangjie
public func toAsciiLowerCase(): Byte
```

功能：将 [Byte](core_package_types.md#type-byte) 换为对应的 Ascii 小写字符 [Byte](core_package_types.md#type-byte)，如果无法转换则保持现状。

返回值：

- [Byte](core_package_types.md#type-byte) - 转换后的 [Byte](core_package_types.md#type-byte)，如果无法转换则返回原来的 [Byte](core_package_types.md#type-byte)。

#### func toAsciiUpperCase()

```cangjie
public func toAsciiUpperCase(): Byte
```

功能：将 [Byte](core_package_types.md#type-byte) 换为对应的 Ascii 大写字符 [Byte](core_package_types.md#type-byte)，如果无法转换则保持现状。

返回值：

- [Byte](core_package_types.md#type-byte) - 转换后的 [Byte](core_package_types.md#type-byte)，如果无法转换则返回原来的 [Byte](core_package_types.md#type-byte)。

## interface Collection\<T>

```cangjie
public interface Collection<T> <: Iterable<T> {
    prop size: Int64
    func isEmpty(): Bool
    func toArray(): Array<T>
}
```

功能：该接口用来表示集合，通常容器类型应该实现该接口。

父类型：

- [Iterable](#interface-iterablee)\<T>

### prop size

```cangjie
prop size: Int64
```

功能：获取当前集合的大小，即集合中元素的个数。

类型：[Int64](core_package_intrinsics.md#int64)

### func isEmpty()

```cangjie
func isEmpty(): Bool
```

功能：判断当前集合是否为空。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果为空返回 true，否则返回 false。

### func toArray()

```cangjie
func toArray(): Array<T>
```

功能：将当前集合转为数组类型。

返回值：

- [Array](core_package_structs.md#struct-arrayt)\<T> - 转换得到的数组。

## interface Comparable\<T>

```cangjie
public interface Comparable<T> <: Equatable<T> & Less<T> & Greater<T> & LessOrEqual<T> & GreaterOrEqual<T> {
    func compare(that: T): Ordering
    operator func <(rhs: T): Bool
    operator func <=(rhs: T): Bool
    operator func ==(rhs: T): Bool
    operator func >(rhs: T): Bool
    operator func >=(rhs: T): Bool
}
```

功能：该接口表示比较运算，是等于、不等于、小于、大于、小于等于、大于等于接口的集合体。

该接口中提供运算符 ==、!=、<、<=、>、>= 重载的默认实现，默认实现根据 compare 函数的返回值来确定其返回值。例如：如果 a.compare(b) 的返回值为 EQ，则 a == b 返回 true，否则返回 false。

父类型：

- [Equatable](#interface-equatablet)\<T>
- [Less](#interface-lesst)\<T>
- [Greater](#interface-greatert)\<T>
- [LessOrEqual](#interface-lessorequalt)\<T>
- [GreaterOrEqual](#interface-greaterorequalt)\<T>

### func compare(T)

```cangjie
func compare(that: T): Ordering
```

功能：判断当前 `T` 类型实例与参数指向的 `T` 类型实例的大小关系。

参数：

- that: T - 待与当前实例比较的另一个实例。

返回值：

- [Ordering](core_package_enums.md#enum-ordering) - 如果大于，返回 [Ordering](core_package_enums.md#enum-ordering).GT，如果等于，返回 [Ordering](core_package_enums.md#enum-ordering).EQ，如果小于，返回 [Ordering](core_package_enums.md#enum-ordering).LT。

### operator func <(T)

```cangjie
operator func <(rhs: T): Bool
```

功能：判断当前 `T` 类型实例是否小于参数指向的 `T` 类型实例，该函数是此接口的一个默认实现函数。

参数：

- rhs: T - 待与当前实例比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果小于，返回 true，否则返回 false。

### operator func <=(T)

```cangjie
operator func <=(rhs: T): Bool
```

功能：判断当前 `T` 类型实例是否小于等于参数指向的 `T` 类型实例，该函数是此接口的一个默认实现函数。

参数：

- rhs: T - 待与当前实例比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果小于等于，返回 true，否则返回 false。

### operator func ==(T)

```cangjie
operator func ==(rhs: T): Bool
```

功能：判断两个实例是否相等，该函数是此接口的一个默认实现函数。

参数：

- rhs: T - 待比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果相等，返回 true，否则返回 false。

### operator func >(T)

```cangjie
operator func >(rhs: T): Bool
```

功能：判断当前 `T` 类型实例是否大于参数指向的 `T` 类型实例，该函数是此接口的一个默认实现函数。

参数：

- rhs: T - 待与当前实例比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果大于，返回 true，否则返回 false。

### operator func >=(T)

```cangjie
operator func >=(rhs: T): Bool
```

功能：判断当前 `T` 类型实例是否大于等于参数指向的 `T` 类型实例，该函数是此接口的一个默认实现函数。

参数：

- rhs: T - 待与当前实例比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果大于等于，返回 true，否则返回 false。

## interface Countable\<T>

```cangjie
public interface Countable<T> {
    func next(right: Int64): T
    func position(): Int64
}
```

功能：该接口表示类型可数。

可数类型的每一个实例都对应一个位置信息（[Int64](core_package_intrinsics.md#int64) 值），可以通过往后数数得到其他的该类型实例。

### func next(Int64)

```cangjie
func next(right: Int64): T
```

功能：获取当前实例向右移动 `right` 后对应位置的 `T` 类型实例。

参数：

- right: [Int64](core_package_intrinsics.md#int64) - 往右数的个数。

返回值：

- T - 向右移动 `right` 后对应位置的 `T` 类型实例。

### func position()

```cangjie
func position(): Int64
```

功能：获取当前可数实例的位置信息，即将当前实例转为 [Int64](core_package_intrinsics.md#int64) 类型。

返回值：

- [Int64](core_package_intrinsics.md#int64) - 转换后的 [Int64](core_package_intrinsics.md#int64) 值。

### extend Float64

```cangjie
extend Float64
```

功能：拓展了 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型作为左操作数和 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 类型作为右操作数的乘法运算。

#### operator func *(Duration)

```cangjie
public operator func *(r: Duration): Duration
```

功能：实现 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型和 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 类型的乘法，即 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) * [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 运算。

参数：

- r: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 实例。

返回值：

- [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型实例和 `r` 的乘积。

异常：

- [ArithmeticException](../../core/core_package_api/core_package_exceptions.md#class-arithmeticexception) - 当相乘后的结果超出 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 的表示范围时，抛出异常。

### extend Int64

```cangjie
extend Int64
```

功能：拓展了 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型作为左操作数和 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 类型作为右操作数的乘法运算。

#### operator func *(Duration)

```cangjie
public operator func *(r: Duration): Duration
```

功能：实现 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型和 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 类型的乘法，即 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) * [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 运算。

例如 2 * [Duration](../../core/core_package_api/core_package_structs.md#struct-duration).second 返回表示时间间隔为 2 秒的 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 实例。

参数：

- r: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 乘法的右操作数。

返回值：

- [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型实例和 `r` 的乘积。

异常：

- [ArithmeticException](../../core/core_package_api/core_package_exceptions.md#class-arithmeticexception) - 当相乘后的结果超出 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 的表示范围时，抛出异常。

## interface CType

```cangjie
sealed interface CType
```

功能：表示支持与 C 语言互操作的接口。

[CType](core_package_interfaces.md#interface-ctype) 接口是一个语言内置的空接口，它是 [CType](core_package_interfaces.md#interface-ctype) 约束的具体实现，所有 C 互操作支持的类型都隐式地实现了该接口，因此所有 C 互操作支持的类型都可以作为 [CType](core_package_interfaces.md#interface-ctype) 类型的子类型使用。

> **注意：**
>
> - [CType](core_package_interfaces.md#interface-ctype) 接口是仓颉中的一个接口类型，它本身不满足 [CType](core_package_interfaces.md#interface-ctype) 约束。
> - [CType](core_package_interfaces.md#interface-ctype) 接口不允许被用户继承、扩展。
> - [CType](core_package_interfaces.md#interface-ctype) 接口不会突破子类型的使用限制。

示例：

<!-- run -->
```cangjie
@C
struct Data {}

@C
func foo() {}

main() {
    var c: CType = Data() // ok
    c = 0 // ok
    c = true // ok
    c = CString(CPointer<UInt8>()) // ok
    c = CPointer<Int8>() // ok
    c = foo // ok
}
```

## interface Equal\<T>

```cangjie
public interface Equal<T> {
    operator func ==(rhs: T): Bool
}
```

功能：该接口用于支持判等操作。

### operator func ==(T)

```cangjie
operator func ==(rhs: T): Bool
```

功能：判断两个实例是否相等。

参数：

- rhs: T - 待比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果相等，返回 true，否则返回 false。

## interface Equatable\<T>

```cangjie
public interface Equatable<T> <: Equal<T> & NotEqual<T> {
    operator func !=(rhs: T): Bool
}
```

功能：该接口是判等和判不等两个接口的集合体。

该接口中提供运算符 != 重载的默认实现，默认实现根据 == 运算的返回值来确定其返回值。例如：如果 a == b 的返回值为 true，则 a != b 返回 false，否则返回 true。

已为部分仓颉类型实现该接口，包括：[Unit](core_package_intrinsics.md#unit)、[Bool](core_package_intrinsics.md#bool) 、[Rune](core_package_intrinsics.md#rune)、[Int64](core_package_intrinsics.md#int64)、[Int32](core_package_intrinsics.md#int32)、[Int16](core_package_intrinsics.md#int16)、[Int8](core_package_intrinsics.md#int8)、[UIntNative](core_package_intrinsics.md#uintnative)、[UInt64](core_package_intrinsics.md#uint64)、[UInt32](core_package_intrinsics.md#uint32)、[UInt16](core_package_intrinsics.md#uint16)、[UInt8](core_package_intrinsics.md#uint8)、[Float64](core_package_intrinsics.md#float64)、[Float32](core_package_intrinsics.md#float32)、[Float16](core_package_intrinsics.md#float16)、[String](core_package_structs.md#struct-string)、[Array](core_package_structs.md#struct-arrayt)、[Box](core_package_classes.md#class-boxt)、[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)、[HashSet](../../collection/collection_package_api/collection_package_class.md#class-hashsett-where-t--hashable--equatablet)。

父类型：

- [Equal](#interface-equalt)\<T>
- [NotEqual](#interface-notequalt)\<T>

### operator func !=(T)

```cangjie
operator func !=(rhs: T): Bool
```

功能：判断两个实例是否不相等，该函数是此接口的一个默认实现函数。

参数：

- rhs: T - 待比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果不相等，返回 true，否则返回 false。

## interface Greater\<T>

```cangjie
public interface Greater<T> {
    operator func >(rhs: T): Bool
}
```

功能：该接口表示大于计算。

### operator func >(T)

```cangjie
operator func >(rhs: T): Bool
```

功能：判断当前 `T` 类型实例是否大于参数指向的 `T` 类型实例。

参数：

- rhs: T - 待与当前实例比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果大于，返回 true，否则返回 false。

## interface GreaterOrEqual\<T>

```cangjie
public interface GreaterOrEqual<T> {
    operator func >=(rhs: T): Bool
}
```

功能：该接口表示大于等于计算。

### operator func >=(T)

```cangjie
operator func >=(rhs: T): Bool
```

功能：判断当前 `T` 类型实例是否大于等于参数指向的 `T` 类型实例。

参数：

- rhs: T - 待与当前实例比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果大于等于，返回 true，否则返回 false。

## interface Hashable

```cangjie
public interface Hashable {
    func hashCode(): Int64
}
```

功能：该接口用于计算哈希值。

已为部分仓颉类型实现该接口，包括：[Bool](core_package_intrinsics.md#bool)、[Rune](core_package_intrinsics.md#rune)、[IntNative](core_package_intrinsics.md#intnative)、[Int64](core_package_intrinsics.md#int64)、[Int32](core_package_intrinsics.md#int32)、[Int16](core_package_intrinsics.md#int16)、[Int8](core_package_intrinsics.md#int8)、[UIntNative](core_package_intrinsics.md#uintnative)、[UInt64](core_package_intrinsics.md#uint64)、[UInt32](core_package_intrinsics.md#uint32)、[UInt16](core_package_intrinsics.md#uint16)、[UInt8](core_package_intrinsics.md#uint8)、[Float64](core_package_intrinsics.md#float64)、[Float32](core_package_intrinsics.md#float32)、[Float16](core_package_intrinsics.md#float16)、[String](core_package_structs.md#struct-string)、[Box](core_package_classes.md#class-boxt)。

### func hashCode()

```cangjie
func hashCode(): Int64
```

功能：获得实例类型的哈希值。

返回值：

- [Int64](core_package_intrinsics.md#int64) - 返回实例类型的哈希值。

## interface Hasher

```cangjie
public interface Hasher {
    func finish(): Int64
    mut func reset(): Unit
    mut func write(value: Bool): Unit
    mut func write(value: Rune): Unit
    mut func write(value: Int8): Unit
    mut func write(value: Int16): Unit
    mut func write(value: Int32): Unit
    mut func write(value: Int64): Unit
    mut func write(value: UInt8): Unit
    mut func write(value: UInt16): Unit
    mut func write(value: UInt32): Unit
    mut func write(value: UInt64): Unit
    mut func write(value: Float16): Unit
    mut func write(value: Float32): Unit
    mut func write(value: Float64): Unit
    mut func write(value: String): Unit
}
```

功能：该接口用于处理哈希组合运算。

可以使用一系列 write 函数传入不同数据类型实例，并计算它们的组合哈希值。

### func finish()

```cangjie
func finish(): Int64
```

功能：获取哈希运算的结果。

返回值：

- [Int64](core_package_intrinsics.md#int64) - 经过计算后的哈希值。

### func reset()

```cangjie
mut func reset(): Unit
```

功能：重置哈希值到 0。

### func write(Bool)

```cangjie
mut func write(value: Bool): Unit
```

功能：把想要哈希运算的 [Bool](core_package_intrinsics.md#bool) 值传入，然后进行哈希组合运算。

参数：

- value: [Bool](core_package_intrinsics.md#bool) - 待运算的值。

### func write(Float16)

```cangjie
mut func write(value: Float16): Unit
```

功能：通过该函数把想要哈希运算的 [Float16](core_package_intrinsics.md#float16) 值传入，然后进行哈希组合运算。

参数：

- value: [Float16](core_package_intrinsics.md#float16) - 待运算的值。

### func write(Float32)

```cangjie
mut func write(value: Float32): Unit
```

功能：通过该函数把想要哈希运算的 [Float32](core_package_intrinsics.md#float32) 值传入，然后进行哈希组合运算。

参数：

- value: [Float32](core_package_intrinsics.md#float32) - 待运算的值。

### func write(Float64)

```cangjie
mut func write(value: Float64): Unit
```

功能：通过该函数把想要哈希运算的 [Float64](core_package_intrinsics.md#float64) 值传入，然后进行哈希组合运算。

参数：

- value: [Float64](core_package_intrinsics.md#float64) - 待运算的值。

### func write(Int16)

```cangjie
mut func write(value: Int16): Unit
```

功能：通过该函数把想要哈希运算的 [Int16](core_package_intrinsics.md#int16) 值传入，然后进行哈希组合运算。

参数：

- value: [Int16](core_package_intrinsics.md#int16) - 待运算的值。

### func write(Int32)

```cangjie
mut func write(value: Int32): Unit
```

功能：通过该函数把想要哈希运算的 [Int32](core_package_intrinsics.md#int32) 值传入，然后进行哈希组合运算。

参数：

- value: [Int32](core_package_intrinsics.md#int32) - 待运算的值。

### func write(Int64)

```cangjie
mut func write(value: Int64): Unit
```

功能：通过该函数把想要哈希运算的 [Int64](core_package_intrinsics.md#int64) 值传入，然后进行哈希组合运算。

参数：

- value: [Int64](core_package_intrinsics.md#int64) - 待运算的值。

### func write(Int8)

```cangjie
mut func write(value: Int8): Unit
```

功能：通过该函数把想要哈希运算的 [Int8](core_package_intrinsics.md#int8) 值传入，然后进行哈希组合运算。

参数：

- value: [Int8](core_package_intrinsics.md#int8) - 待运算的值。

### func write(Rune)

```cangjie
mut func write(value: Rune): Unit
```

功能：通过该函数把想要哈希运算的 [Rune](core_package_intrinsics.md#rune) 值传入，然后进行哈希组合运算。

参数：

- value: [Rune](core_package_intrinsics.md#rune) - 待运算的值。

### func write(String)

```cangjie
mut func write(value: String): Unit
```

功能：通过该函数把想要哈希运算的 [String](core_package_structs.md#struct-string) 值传入，然后进行哈希组合运算。

参数：

- value: [String](core_package_structs.md#struct-string) - 待运算的值。

### func write(UInt16)

```cangjie
mut func write(value: UInt16): Unit
```

功能：通过该函数把想要哈希运算的 [UInt16](core_package_intrinsics.md#uint16) 值传入，然后进行哈希组合运算。

参数：

- value: [UInt16](core_package_intrinsics.md#uint16) - 待运算的值。

### func write(UInt32)

```cangjie
mut func write(value: UInt32): Unit
```

功能：通过该函数把想要哈希运算的 [UInt32](core_package_intrinsics.md#uint32) 值传入，然后进行哈希组合运算。

参数：

- value: [UInt32](core_package_intrinsics.md#uint32) - 待运算的值。

### func write(UInt64)

```cangjie
mut func write(value: UInt64): Unit
```

功能：通过该函数把想要哈希运算的 [UInt64](core_package_intrinsics.md#uint64) 值传入，然后进行哈希组合运算。

参数：

- value: [UInt64](core_package_intrinsics.md#uint64) - 待运算的值。

### func write(UInt8)

```cangjie
mut func write(value: UInt8): Unit
```

功能：通过该函数把想要哈希运算的 [UInt8](core_package_intrinsics.md#uint8) 值传入，然后进行哈希组合运算。

参数：

- value: [UInt8](core_package_intrinsics.md#uint8) - 待运算的值。

## interface Iterable\<E>

```cangjie
public interface Iterable<E> {
    func iterator(): Iterator<E>
}
```

功能：该接口表示可迭代，实现了该接口的类型（通常为容器类型）可以在 `for-in` 语句中实现迭代，也可以获取其对应的迭代器类型实例，调用 `next` 函数实现迭代。

本包已经为 [Array](core_package_structs.md#struct-arrayt)、[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)、[HashMap](../../collection/collection_package_api/collection_package_class.md#class-hashmapk-v-where-k--hashable--equatablek) 等基础容器类型实现了该接口，用户可以为其他类型实现该接口，使之支持迭代遍历的功能。

### func iterator()

```cangjie
func iterator(): Iterator<E>
```

功能：获取迭代器。

返回值：

- [Iterator](core_package_classes.md#class-iteratort)\<E> - 迭代器。

## interface Less\<T>

```cangjie
public interface Less<T> {
    operator func <(rhs: T): Bool
}
```

功能：该接口表示小于计算。

### operator func <(T)

```cangjie
operator func <(rhs: T): Bool
```

功能：判断当前 `T` 类型实例是否小于参数指向的 `T` 类型实例。

参数：

- rhs: T - 待与当前实例比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果小于，返回 true，否则返回 false。

## interface LessOrEqual\<T>

```cangjie
public interface LessOrEqual<T> {
    operator func <=(rhs: T): Bool
}
```

功能：该接口表示小于等于计算。

### operator func <=(T)

```cangjie
operator func <=(rhs: T): Bool
```

功能：判断当前 `T` 类型实例是否小于等于参数指向的 `T` 类型实例。

参数：

- rhs: T - 待与当前实例比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果小于等于，返回 true，否则返回 false。

## interface NotEqual\<T>

```cangjie
public interface NotEqual<T> {
    operator func !=(rhs: T): Bool
}
```

功能：该接口用于支持判不等操作。

### operator func !=(T)

```cangjie
operator func !=(rhs: T): Bool
```

功能：判断两个实例是否不相等。

参数：

- rhs: T - 待比较的另一个实例。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果不相等，返回 true，否则返回 false。

## interface Resource

```cangjie
public interface Resource {
    func close(): Unit
    func isClosed(): Bool
}
```

功能：该接口用于资源管理，通常用于内存、句柄等资源的关闭和释放。

实现了该接口的类型可以在 `try-with-resource` 语法上下文中实现自动资源释放。

### func close()

```cangjie
func close(): Unit
```

功能：关闭资源。

### func isClosed()

```cangjie
func isClosed(): Bool
```

功能：判断资源是否已经关闭。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果已经关闭返回 true，否则返回 false。

## interface ThreadContext

```cangjie
public interface ThreadContext {
    func end(): Unit
    func hasEnded(): Bool
}
```

功能：仓颉线程上下文接口。

用户创建 `thread` 时，除了缺省 `spawn` 表达式入参，也可以通过传入不同 [ThreadContext](core_package_interfaces.md#interface-threadcontext) 类型的实例，选择不同的线程上下文，然后一定程度上控制并发行为。

目前不允许用户自行实现 [ThreadContext](core_package_interfaces.md#interface-threadcontext) 接口，仓颉语言根据使用场景，提供了 `MainThreadContext`, 具体定义可在终端框架库中查阅。

### func end()

```cangjie
func end(): Unit
```

功能：结束方法，用于向当前 context 发送结束请求。

### func hasEnded()

```cangjie
func hasEnded(): Bool
```

功能：检查方法，用于检查当前 context 是否已结束。

返回值：

- [Bool](core_package_intrinsics.md#bool) - 如果结束返回 true，否则返回 false。

## interface ToString

```cangjie
public interface ToString {
    func toString(): String
}
```

功能：该接口用来提供具体类型的字符串表示。

### func toString()

```cangjie
func toString(): String
```

功能：获取实例类型的字符串表示。

返回值：

- [String](core_package_structs.md#struct-string) - 返回实例类型的字符串表示。
