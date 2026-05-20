# 接口

## interface BigEndianOrder\<T>

```cangjie
public interface BigEndianOrder<T> {
    func writeBigEndian(buffer: Array<UInt8>): Int64
    static func readBigEndian(buffer: Array<UInt8>): T
}
```

功能：大端序字节序列转换接口。

### static func readBigEndian(Array\<UInt8>)

```cangjie
static func readBigEndian(buffer: Array<UInt8>): T
```

功能：从字节数组中以大端序的方式读取一个 T 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- T - T 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 T 值时，抛出异常。

### func writeBigEndian(Array\<UInt8>)

```cangjie
func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 T 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 T 值时，抛出异常。

### extend Bool <: BigEndianOrder\<Bool>

```cangjie
extend Bool <: BigEndianOrder<Bool>
```

功能：为 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): Bool
```

功能：从字节数组中以大端序的方式读取一个 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.binary.*

main() {
    let buffer: Array<UInt8> = [0x1]
    let n = Bool.readBigEndian(buffer)
    println(n)
}
```

运行结果：

```text
true
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.binary.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = true.writeBigEndian(buffer)
    println(n == 1)
    println(buffer[0] == 0x01u8)
}
```

运行结果：

```text
true
true
```

### extend Float16 <: BigEndianOrder\<Float16>

```cangjie
extend Float16 <: BigEndianOrder<Float16>
```

功能：为 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): Float16
```

功能：从字节数组中以大端序的方式读取一个 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.binary.*

main() {
    /* 12.5的IEEE 754表示为0x4A40 */
    let buffer: Array<UInt8> = [0x4A, 0x40]
    let n = Float16.readBigEndian(buffer)
    println(n == 12.5)
}
```

运行结果：

```text
true
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.binary.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let len = 12.5f16.writeBigEndian(buffer)
    println(len)

    /* 0x4A的十进制表示为74,0x40的十进制表示为64 */
    println(buffer[0..len])
}
```

运行结果：

```text
2
[74, 64]
```

### extend Float32 <: BigEndianOrder\<Float32>

```cangjie
extend Float32 <: BigEndianOrder<Float32>
```

功能：为 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): Float32
```

功能：从字节数组中以大端序的方式读取一个 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.binary.*

main() {
    let buffer: Array<UInt8> = [0x41, 0x48, 0x00, 0x00]
    let n = Float32.readBigEndian(buffer)
    println(n)
}
```

运行结果：

```text
12.500000
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.binary.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let len = 12.5f32.writeBigEndian(buffer)
    println(len)

    /* 12.5的IEEE 754的单精度浮点表示为 0x4148 ,0x41的十进制表示为65，0x48的十进制表示为72 */
    println(buffer[0..len])
}
```

运行结果：

```text
4
[65, 72, 0, 0]
```

### extend Float64 <: BigEndianOrder\<Float64>

```cangjie
extend Float64 <: BigEndianOrder<Float64>
```

功能：为 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): Float64
```

功能：从字节数组中以大端序的方式读取一个 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x40, 0x29, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    let n = Float64.readBigEndian(buffer)
    @Assert(n, 12.5)
}
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 12.5f64.writeBigEndian(buffer)
    @Assert(n, 8)
    @Assert(buffer[..n] == [0x40, 0x29, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
}
```

### extend Int16 <: BigEndianOrder\<Int16>

```cangjie
extend Int16 <: BigEndianOrder<Int16>
```

功能：为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): Int16
```

功能：从字节数组中以大端序的方式读取一个 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12, 0x34]
    let n = Int16.readBigEndian(buffer)
    @Assert(n, 0x1234)
}
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x1234i16.writeBigEndian(buffer)
    @Assert(n, 2)
    @Assert(buffer[..n] == [0x12, 0x34])
}
```

### extend Int32 <: BigEndianOrder\<Int32>

```cangjie
extend Int32 <: BigEndianOrder<Int32>
```

功能：为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): Int32
```

功能：从字节数组中以大端序的方式读取一个 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12, 0x34, 0x56, 0x78]
    let n = Int32.readBigEndian(buffer)
    @Assert(n, 0x12345678)
}
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    var buffer: Array<UInt8> = Array<UInt8>(8, repeat: 0)
    let n = 0x12345678i32.
    writeBigEndian(buffer)
    @Assert(n, 4)
    @Assert(buffer[..n] == [0x12u8, 0x34u8, 0x56u8, 0x78u8])
}
```

### extend Int64 <: BigEndianOrder\<Int64>

```cangjie
extend Int64 <: BigEndianOrder<Int64>
```

功能：为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): Int64
```

功能：从字节数组中以大端序的方式读取一个 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12, 0x34, 0x56, 0x78, 0x90, 0x12, 0x34, 0x56]
    let n = Int64.readBigEndian(buffer)
    @Assert(n, 0x1234567890123456)
}
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x1234567890123456i64.writeBigEndian(buffer)
    @Assert(n, 8)
    @Assert(buffer[..n] == [0x12, 0x34, 0x56, 0x78, 0x90, 0x12, 0x34, 0x56])
}
```

### extend Int8 <: BigEndianOrder\<Int8>

```cangjie
extend Int8 <: BigEndianOrder<Int8>
```

功能：为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): Int8
```

功能：从字节数组中以大端序的方式读取一个 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12]
    let n = Int8.readBigEndian(buffer)
    @Assert(n, 0x12)
}
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x12i8.writeBigEndian(buffer)
    @Assert(n, 1)
    @Assert(buffer[..n] == [0x12])
}
```

### extend UInt16 <: BigEndianOrder\<UInt16>

```cangjie
extend UInt16 <: BigEndianOrder<UInt16>
```

功能：为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): UInt16
```

功能：从字节数组中以大端序的方式读取一个 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12, 0x34]
    let n = UInt16.readBigEndian(buffer)
    @Assert(n, 0x1234)
}
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x1234u16.writeBigEndian(buffer)
    @Assert(n, 2)
    @Assert(buffer[..n] == [0x12, 0x34])
}
```

### extend UInt32 <: BigEndianOrder\<UInt32>

```cangjie
extend UInt32 <: BigEndianOrder<UInt32>
```

功能：为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): UInt32
```

功能：从字节数组中以大端序的方式读取一个 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12, 0x34, 0x56, 0x78]
    let n = UInt32.readBigEndian(buffer)
    @Assert(n, 0x12345678)
}
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x12345678u32.writeBigEndian(buffer)
    @Assert(n, 4)
    @Assert(buffer[..n] == [0x12, 0x34, 0x56, 0x78])
}
```

### extend UInt64 <: BigEndianOrder\<UInt64>

```cangjie
extend UInt64 <: BigEndianOrder<UInt64>
```

功能：为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): UInt64
```

功能：从字节数组中以大端序的方式读取一个 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12, 0x34, 0x56, 0x78, 0x90, 0x12, 0x34, 0x56]
    let n = UInt64.readBigEndian(buffer)
    @Assert(n, 0x1234567890123456)
}
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x1234567890123456u64.writeBigEndian(buffer)
    @Assert(n, 8)
    @Assert(buffer[..n] == [0x12, 0x34, 0x56, 0x78, 0x90, 0x12, 0x34, 0x56])
}
```

### extend UInt8 <: BigEndianOrder\<UInt8>

```cangjie
extend UInt8 <: BigEndianOrder<UInt8>
```

功能：为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 扩展 [BigEndianOrder](binary_package_interfaces.md#interface-bigendianordert) 接口，以实现将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值和大端序字节序列的转换。

父类型：

- [BigEndianOrder](#interface-bigendianordert)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### static func readBigEndian(Array\<UInt8>)

```cangjie
public static func readBigEndian(buffer: Array<UInt8>): UInt8
```

功能：从字节数组中以大端序的方式读取一个 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12]
    let n = UInt8.readBigEndian(buffer)
    @Assert(n, 0x12)
}
```

#### func writeBigEndian(Array\<UInt8>)

```cangjie
public func writeBigEndian(buffer: Array<UInt8>): Int64
```

功能：将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值以大端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x12u8.writeBigEndian(buffer)
    @Assert(n, 1)
    @Assert(buffer[..n] == [0x12])
}
```

## interface LittleEndianOrder\<T>

```cangjie
public interface LittleEndianOrder<T> {
    func writeLittleEndian(buffer: Array<UInt8>): Int64
    static func readLittleEndian(buffer: Array<UInt8>): T
}
```

功能：小端序字节序列转换接口。

### static func readLittleEndian(Array\<UInt8>)

```cangjie
static func readLittleEndian(buffer: Array<UInt8>): T
```

功能：从字节数组中以小端序的方式读取一个 T 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- T - T 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 T 值时，抛出异常。

### func writeLittleEndian(Array\<UInt8>)

```cangjie
func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 T 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 T 值时，抛出异常。

### extend Bool <: LittleEndianOrder\<Bool>

```cangjie
extend Bool <: LittleEndianOrder<Bool>
```

功能：为 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): Bool
```

功能：从字节数组中以小端序的方式读取一个 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x1]
    let n = Bool.readLittleEndian(buffer)
    @Assert(n, true)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = true.writeLittleEndian(buffer)
    @Assert(n, 1)
    @Assert(buffer[..n] == [0x01])
}
```

### extend Float16 <: LittleEndianOrder\<Float16>

```cangjie
extend Float16 <: LittleEndianOrder<Float16>
```

功能：为 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): Float16
```

功能：从字节数组中以小端序的方式读取一个 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x40, 0x4A]
    let n = Float16.readLittleEndian(buffer)
    @Assert(n, 12.5)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 12.5f16.writeLittleEndian(buffer)
    @Assert(n, 2)
    @Assert(buffer[..n] == [0x40, 0x4A])
}
```

### extend Float32 <: LittleEndianOrder\<Float32>

```cangjie
extend Float32  <: LittleEndianOrder<Float32>
```

功能：为 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): Float32
```

功能：从字节数组中以小端序的方式读取一个 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x00, 0x00, 0x48, 0x41]
    let n = Float32.readLittleEndian(buffer)
    @Assert(n, 12.5)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 12.5f32.writeLittleEndian(buffer)
    @Assert(n, 4)
    @Assert(buffer[..n] == [0x00, 0x00, 0x48, 0x41])
}
```

### extend Float64 <: LittleEndianOrder\<Float64>

```cangjie
extend Float64 <: LittleEndianOrder<Float64>
```

功能：为 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): Float64
```

功能：从字节数组中以小端序的方式读取一个 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x29, 0x40]
    let n = Float64.readLittleEndian(buffer)
    @Assert(n, 12.5)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 12.5f64.writeLittleEndian(buffer)
    @Assert(n, 8)
    @Assert(buffer[..n] == [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x29, 0x40])
}
```

### extend Int16 <: LittleEndianOrder\<Int16>

```cangjie
extend Int16 <: LittleEndianOrder<Int16>
```

功能：为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): Int16
```

功能：从字节数组中以小端序的方式读取一个 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x34, 0x12]
    let n = Int16.readLittleEndian(buffer)
    @Assert(n, 0x1234i16)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x1234i16.writeLittleEndian(buffer)
    @Assert(n, 2)
    @Assert(buffer[..n] == [0x34, 0x12])
}
```

### extend Int32 <: LittleEndianOrder\<Int32>

```cangjie
extend Int32 <: LittleEndianOrder<Int32>
```

功能：为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): Int32
```

功能：从字节数组中以小端序的方式读取一个 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x78, 0x56, 0x34, 0x12]
    let n = Int32.readLittleEndian(buffer)
    @Assert(n, 0x12345678)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x12345678i32.writeLittleEndian(buffer)
    @Assert(n, 4)
    @Assert(buffer[..n] == [0x78, 0x56, 0x34, 0x12])
}
```

### extend Int64 <: LittleEndianOrder\<Int64>

```cangjie
extend Int64 <: LittleEndianOrder<Int64>
```

功能：为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): Int64
```

功能：从字节数组中以小端序的方式读取一个 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x56, 0x34, 0x12, 0x90, 0x78, 0x56, 0x34, 0x12]
    let n = Int64.readLittleEndian(buffer)
    @Assert(n, 0x1234567890123456)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x1234567890123456i64.writeLittleEndian(buffer)
    @Assert(n, 8)
    @Assert(buffer[..n] == [0x56, 0x34, 0x12, 0x90, 0x78, 0x56, 0x34, 0x12])
}
```

### extend Int8 <: LittleEndianOrder\<Int8>

```cangjie
extend Int8 <: LittleEndianOrder<Int8>
```

功能：为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): Int8
```

功能：从字节数组中以小端序的方式读取一个 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12]
    let n = Int8.readLittleEndian(buffer)
    @Assert(n, 0x12)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x12i8.writeLittleEndian(buffer)
    @Assert(n, 1)
    @Assert(buffer[..n] == [0x12])
}
```

### extend UInt16 <: LittleEndianOrder\<UInt16>

```cangjie
extend UInt16 <: LittleEndianOrder<UInt16>
```

功能：为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): UInt16
```

功能：从字节数组中以小端序的方式读取一个 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x34, 0x12]
    let n = UInt16.readLittleEndian(buffer)
    @Assert(n, 0x1234u16)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x1234u16.writeLittleEndian(buffer)
    @Assert(n, 2)
    @Assert(buffer[..n] == [0x34, 0x12])
}
```

### extend UInt32 <: LittleEndianOrder\<UInt32>

```cangjie
extend UInt32 <: LittleEndianOrder<UInt32>
```

功能：为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): UInt32
```

功能：从字节数组中以小端序的方式读取一个 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x78, 0x56, 0x34, 0x12]
    let n = UInt32.readLittleEndian(buffer)
    @Assert(n, 0x12345678)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x12345678u32.writeLittleEndian(buffer)
    @Assert(n, 4)
    @Assert(buffer[..n] == [0x78, 0x56, 0x34, 0x12])
}
```

### extend UInt64 <: LittleEndianOrder\<UInt64>

```cangjie
extend UInt64 <: LittleEndianOrder<UInt64>
```

功能：为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): UInt64
```

功能：从字节数组中以小端序的方式读取一个 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x56, 0x34, 0x12, 0x90, 0x78, 0x56, 0x34, 0x12]
    let n = UInt64.readLittleEndian(buffer)
    @Assert(n, 0x1234567890123456)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x1234567890123456u64.writeLittleEndian(buffer)
    @Assert(n, 8)
    @Assert(buffer[..n] == [0x56, 0x34, 0x12, 0x90, 0x78, 0x56, 0x34, 0x12])
}
```

### extend UInt8 <: LittleEndianOrder\<UInt8>

```cangjie
extend UInt8 <: LittleEndianOrder<UInt8>
```

功能：为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 扩展 [LittleEndianOrder](binary_package_interfaces.md#interface-littleendianordert) 接口，以实现将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值和小端序字节序列的转换。

父类型：

- [LittleEndianOrder](#interface-littleendianordert)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### static func readLittleEndian(Array\<UInt8>)

```cangjie
public static func readLittleEndian(buffer: Array<UInt8>): UInt8
```

功能：从字节数组中以小端序的方式读取一个 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待读取的数据。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以读出 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer: Array<UInt8> = [0x12]
    let n = UInt8.readLittleEndian(buffer)
    @Assert(n, 0x12)
}
```

#### func writeLittleEndian(Array\<UInt8>)

```cangjie
public func writeLittleEndian(buffer: Array<UInt8>): Int64
```

功能：将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值以小端序的方式写入字节数组中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区，用于存放待写入的数据。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 写入的数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 太小，不足以存储 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值时，抛出异常。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let buffer = Array<UInt8>(8, repeat: 0)
    let n = 0x12u8.writeLittleEndian(buffer)
    @Assert(n, 1)
    @Assert(buffer[..n] == [0x12])
}
```

## interface SwapEndianOrder\<T>

```cangjie
public interface SwapEndianOrder<T> {
    func swapBytes(): T
}
```

功能：反转字节顺序接口。

### func swapBytes()

```cangjie
func swapBytes(): T
```

功能：反转 T 值的字节顺序。

返回值：

- T - T 值。

### extend Int16 <: SwapEndianOrder\<Int16>

```cangjie
extend Int16 <: SwapEndianOrder<Int16>
```

功能：为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 扩展 [SwapEndianOrder](binary_package_interfaces.md#interface-swapendianordert) 接口，以实现将 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值的字节顺序反转。

父类型：

- [SwapEndianOrder](#interface-swapendianordert)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### func swapBytes()

```cangjie
public func swapBytes(): Int16
```

功能：反转 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值的字节顺序。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 值。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let n = 0x1234i16
    let m = n.swapBytes()
    @Assert(m, 0x3412)
}
```

### extend Int32 <: SwapEndianOrder\<Int32>

```cangjie
extend Int32 <: SwapEndianOrder<Int32>
```

功能：为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 扩展 [SwapEndianOrder](binary_package_interfaces.md#interface-swapendianordert) 接口，以实现将 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值的字节顺序反转。

父类型：

- [SwapEndianOrder](#interface-swapendianordert)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### func swapBytes()

```cangjie
public func swapBytes(): Int32
```

功能：反转 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值的字节顺序。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 值。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let n = 0x12345678i32
    let m = n.swapBytes()
    @Assert(m, 0x78563412)
}
```

### extend Int64 <: SwapEndianOrder\<Int64>

```cangjie
extend Int64 <: SwapEndianOrder<Int64>
```

功能：为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 扩展 [SwapEndianOrder](binary_package_interfaces.md#interface-swapendianordert) 接口，以实现将 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值的字节顺序反转。

父类型：

- [SwapEndianOrder](#interface-swapendianordert)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>

#### func swapBytes()

```cangjie
public func swapBytes(): Int64
```

功能：反转 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值的字节顺序。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 值。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let n = 0x1234567890123456i64
    let m = n.swapBytes()
    @Assert(m, 0x5634129078563412)
}
```

### extend Int8 <: SwapEndianOrder\<Int8>

```cangjie
extend Int8 <: SwapEndianOrder<Int8>
```

功能：为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 扩展 [SwapEndianOrder](binary_package_interfaces.md#interface-swapendianordert) 接口，以实现将 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值的字节顺序反转。

父类型：

- [SwapEndianOrder](#interface-swapendianordert)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### func swapBytes()

```cangjie
public func swapBytes(): Int8
```

功能：反转 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值的字节顺序。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 值。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let n = 0x12i8
    let m = n.swapBytes()
    @Assert(m, 0x12)
}
```

### extend UInt16 <: SwapEndianOrder\<UInt16>

```cangjie
extend UInt16 <: SwapEndianOrder<UInt16>
```

功能：为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 扩展 [SwapEndianOrder](binary_package_interfaces.md#interface-swapendianordert) 接口，以实现将 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值的字节顺序反转。

父类型：

- [SwapEndianOrder](#interface-swapendianordert)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### func swapBytes()

```cangjie
public func swapBytes(): UInt16
```

功能：反转 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值的字节顺序。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 值。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let n = 0x1234u16
    let m = n.swapBytes()
    @Assert(m, 0x3412)
}
```

### extend UInt32 <: SwapEndianOrder\<UInt32>

```cangjie
extend UInt32 <: SwapEndianOrder<UInt32>
```

功能：为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 扩展 [SwapEndianOrder](binary_package_interfaces.md#interface-swapendianordert) 接口，以实现将 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值的字节顺序反转。

父类型：

- [SwapEndianOrder](#interface-swapendianordert)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### func swapBytes()

```cangjie
public func swapBytes(): UInt32
```

功能：反转 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值的字节顺序。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 值。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let n = 0x12345678u32
    let m = n.swapBytes()
    @Assert(m, 0x78563412)
}
```

### extend UInt64 <: SwapEndianOrder\<UInt64>

```cangjie
extend UInt64 <: SwapEndianOrder<UInt64>
```

功能：为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 扩展 [SwapEndianOrder](binary_package_interfaces.md#interface-swapendianordert) 接口，以实现将 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值的字节顺序反转。

父类型：

- [SwapEndianOrder](#interface-swapendianordert)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### func swapBytes()

```cangjie
public func swapBytes(): UInt64
```

功能：反转 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值的字节顺序。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 值。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let n = 0x1234567890123456u64
    let m = n.swapBytes()
    @Assert(m, 0x5634129078563412)
}
```

### extend UInt8 <: SwapEndianOrder\<UInt8>

```cangjie
extend UInt8 <: SwapEndianOrder<UInt8>
```

功能：为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 扩展 [SwapEndianOrder](binary_package_interfaces.md#interface-swapendianordert) 接口，以实现将 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值的字节顺序反转。

父类型：

- [SwapEndianOrder](#interface-swapendianordert)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### func swapBytes()

```cangjie
public func swapBytes(): UInt8
```

功能：反转 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)  值的字节顺序。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 值。

示例：

<!-- run -->
```cangjie
import std.binary.*
import std.unittest.*
import std.unittest.testmacro.*

main() {
    let n = 0x12u8
    let m = n.swapBytes()
    @Assert(m, 0x12)
}
```
