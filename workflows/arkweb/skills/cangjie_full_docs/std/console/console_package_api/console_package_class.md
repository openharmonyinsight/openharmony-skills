# 类

## class Console <sup>(deprecated)</sup>

```cangjie
public class Console {}
```

功能：此类提供标准输入、标准输出和标准错误流的获取接口。

> **注意：**
>
> 未来版本即将废弃，使用 [env](../../env/env_package_overview.md#函数) 包中相应函数替代。

### static prop stdErr

```cangjie
public static prop stdErr: ConsoleWriter
```

功能：该成员属性为 [ConsoleWriter](console_package_class.md#class-consolewriter-deprecated) 类型，它提供标准错误的获取功能。

类型：[ConsoleWriter](console_package_class.md#class-consolewriter-deprecated)

### static prop stdIn

```cangjie
public static prop stdIn: ConsoleReader
```

功能：该成员属性为 [ConsoleReader](console_package_class.md#class-consolereader-deprecated) 类型，它提供标准输入的获取功能。

类型：[ConsoleReader](console_package_class.md#class-consolereader-deprecated)

### static prop stdOut

```cangjie
public static prop stdOut: ConsoleWriter
```

功能：该成员属性为 [ConsoleWriter](console_package_class.md#class-consolewriter-deprecated) 类型，它提供标准输出的获取功能。

类型：[ConsoleWriter](console_package_class.md#class-consolewriter-deprecated)

## class ConsoleReader <sup>(deprecated)</sup>

```cangjie
public class ConsoleReader <: InputStream {}
```

功能：提供从控制台读出数据并转换成字符或字符串的功能。

该类型无法构造实例，只能通过 [Console.stdIn](console_package_class.md#static-prop-stdin) 获取实例。
读操作是同步的，内部设有缓存区来保存控制台输入的内容，当到达控制台输入流的结尾时，控制台读取函数将返回`None`。

[ConsoleReader](console_package_class.md#class-consolereader-deprecated) 只有一个实例，所有方法共享同一个缓存区，相关`read`方法返回`None`的情形有：

- 将标准输入重定向到文件时，读取到文件结尾 EOF。
- Linux 环境，按下 `Ctrl+D`。
- Windows 环境，按下 `Ctrl+Z` 后加回车。

> **注意：**
>
> 未来版本即将废弃，使用 [ConsoleReader](../../env/env_package_api/env_package_classes.md#class-consolereader) 替代。

父类型：

- [InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### func read()

```cangjie
public func read(): ?Rune
```

功能：从标准输入中读取下一个字符。

返回值：

- ?[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)  - 读取到字符，返回 ?[Rune](../../core/core_package_api/core_package_intrinsics.md#rune) ，否则返回 `None`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception)：当输入不符合`UTF-8`编码的字符串时，抛此异常。

### func read(Array\<Byte>)

```cangjie
public func read(arr: Array<Byte>): Int64
```

功能：从标准输入中读取并放入 `arr` 中。

> **注意：**
>
> 该函数存在风险，可能读取出来的结果恰好把 `UTF-8 code point` 从中截断，如果发生截断，将导致该 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> 转换成字符串的结果不正确或抛出异常。

参数：

- arr: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 目标 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回读取到的字节长度。

### func readln()

```cangjie
public func readln(): ?String
```

功能：从标准输入中读取一行字符串。

读取到字符，返回 ?[String](../../core/core_package_api/core_package_structs.md#struct-string)，结果不包含末尾换行符。该接口不会抛出异常，即使输入不符合`UTF-8`编码的字符串，也会构造出一个 [String](../../core/core_package_api/core_package_structs.md#struct-string) 并返回，其行为等同于 [String](../../core/core_package_api/core_package_structs.md#struct-string).fromUtf8Uncheck([Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>)。

返回值：

- ?[String](../../core/core_package_api/core_package_structs.md#struct-string) - 读取到的行数据，读取失败返回 `None`。

### func readToEnd()

```cangjie
public func readToEnd(): ?String
```

功能：从标准输入中读取所有字符。

直到读取到文件结束符 `EOF`，或者在 Linux 上键入 `Ctrl+D` 或在 Windows 上键入 `Ctrl+Z` + 回车结束。读取到字符，返回 ?[String](../../core/core_package_api/core_package_structs.md#struct-string)，否则返回 `None`。读取失败时会返回 `None`，该接口不会抛出异常，即使输入不符合 `UTF-8` 编码的字符串，也会构造出一个 [String](../../core/core_package_api/core_package_structs.md#struct-string) 并返回，其行为等同于 [String](../../core/core_package_api/core_package_structs.md#struct-string).[fromUtf8Uncheck](../../core/core_package_api/core_package_structs.md#static-func-fromutf8uncheckedarrayuint8)([Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>)。

返回值：

- ?[String](../../core/core_package_api/core_package_structs.md#struct-string) - 将读取到的所有数据以 ?[String](../../core/core_package_api/core_package_structs.md#struct-string) 的形式返回。

### func readUntil((Rune) -> Bool)

```cangjie
public func readUntil(predicate: (Rune) -> Bool): ?String
```

功能：从标准输入中读取数据直到读取到的字符满足`predicate`条件结束。

满足 predicate: (Rune) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 条件的字符包含在结果中，读取失败时会返回`None`。

参数：

- predicate: (Rune) ->[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 终止读取的条件。

返回值：

- ?[String](../../core/core_package_api/core_package_structs.md#struct-string) - 将读取到的数据以 ?[String](../../core/core_package_api/core_package_structs.md#struct-string) 的形式返回。

### func readUntil(Rune)

```cangjie
public func readUntil(ch: Rune): ?String
```

功能：从标准输入中读取数据直到读取到字符 `ch` 结束。

`ch`包含在结果中，如果读取到文件结束符 EOF，将返回读取到的所有信息，读取失败时会返回 `None`。

参数：

- ch: [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) - 终止字符。

返回值：

- ?[String](../../core/core_package_api/core_package_structs.md#struct-string) - 将读取到的数据以 ?[String](../../core/core_package_api/core_package_structs.md#struct-string) 的形式返回。

## class ConsoleWriter <sup>(deprecated)</sup>

```cangjie
public class ConsoleWriter <: OutputStream {}
```

功能：此类提供保证线程安全的标准输出功能。

每次 write 调用写到控制台的结果是完整的，不同的 write 函数调用的结果不会混合到一起。
该类型无法构造实例，只能通过 [Console.stdOut](console_package_class.md#static-prop-stdout) 获取标准输出实例或者 [Console.stdErr](console_package_class.md#static-prop-stderr) 获取标准错误的实例。

> **注意：**
>
> 未来版本即将废弃，使用 [ConsoleWriter](../../env/env_package_api/env_package_classes.md#class-consolewriter) 替代。

父类型：

- [OutputStream](../../io/io_package_api/io_package_interfaces.md#interface-outputstream)

### func flush()

```cangjie
public func flush(): Unit
```

功能：刷新输出流。

### func write(Array\<Byte>)

```cangjie
public func write(buffer: Array<Byte>): Unit
```

功能：指定的将字节数组 buffer 写入标准输出或标准错误流中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 要被写入的字节数组。

### func write(Bool)

```cangjie
public func write(v: Bool): Unit
```

功能：将指定的布尔值的文本表示形式写入标准输出或标准错误流中。

参数：

- v: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 要写入的值。

### func write(Float16)

```cangjie
public func write(v: Float16): Unit
```

功能：将指定的 16 位浮点数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - 要写入的值。

### func write(Float32)

```cangjie
public func write(v: Float32): Unit
```

功能：将指定的 32 位浮点数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - 要写入的值。

### func write(Float64)

```cangjie
public func write(v: Float64): Unit
```

功能：将指定的 64 位浮点数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 要写入的值。

### func write(Int16)

```cangjie
public func write(v: Int16): Unit
```

功能：将指定的 16 位有符号整数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 要写入的值。

### func write(Int32)

```cangjie
public func write(v: Int32): Unit
```

功能：将指定的 32 位有符号整数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 要写入的值。

### func write(Int64)

```cangjie
public func write(v: Int64): Unit
```

功能：将指定的 64 位有符号整数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 要写入的值。

### func write(Int8)

```cangjie
public func write(v: Int8): Unit
```

功能：将指定的 8 位有符号整数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 要写入的值。

### func write(Rune)

```cangjie
public func write(v: Rune): Unit
```

功能：将指定的 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 的 Unicode 字符值写入标准输出或标准错误流中。

参数：

- v: [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) - 要写入的值。

### func write(String)

```cangjie
public func write(v: String): Unit
```

功能：将指定的字符串值写入标准输出或标准错误流中。

参数：

- v: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要写入的值。

### func write(UInt16)

```cangjie
public func write(v: UInt16): Unit
```

功能：将指定的 16 位无符号整数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 要写入的值。

### func write(UInt32)

```cangjie
public func write(v: UInt32): Unit
```

功能：将指定的 32 位无符号整数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 要写入的值。

### func write(UInt64)

```cangjie
public func write(v: UInt64): Unit
```

功能：将指定的 64 位无符号整数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 要写入的值。

### func write(UInt8)

```cangjie
public func write(v: UInt8): Unit
```

功能：将指定的 8 位无符号整数值的文本表示写入标准输出或标准错误流中。

参数：

- v: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 要写入的值。

### func write\<T>(T) where T <: ToString

```cangjie
public func write<T>(v: T): Unit where T <: ToString
```

功能：将实现了 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 接口的数据类型写入标准输出或标准错误流中。

参数：

- v: T - 要被写入的 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 类型的实例。

### func writeln(Array\<Byte>)

```cangjie
public func writeln(buffer: Array<Byte>): Unit
```

功能：指定的将字节数组 buffer （后跟换行符）写入标准输出或标准错误流中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 要写入的值。

### func writeln(Bool)

```cangjie
public func writeln(v: Bool): Unit
```

功能：将指定的布尔值的文本表示形式（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 要写入的值。

### func writeln(Float16)

```cangjie
public func writeln(v: Float16): Unit
```

功能：将指定的 16 位浮点数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - 要写入的值。

### func writeln(Float32)

```cangjie
public func writeln(v: Float32): Unit
```

功能：将指定的 32 位浮点数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - 要写入的值。

### func writeln(Float64)

```cangjie
public func writeln(v: Float64): Unit
```

功能：将指定的 64 位浮点数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 要写入的值。

### func writeln(Int16)

```cangjie
public func writeln(v: Int16): Unit
```

功能：将指定的 16 位有符号整数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 要写入的值。

### func writeln(Int32)

```cangjie
public func writeln(v: Int32): Unit
```

功能：将指定的 32 位有符号整数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 要写入的值。

### func writeln(Int64)

```cangjie
public func writeln(v: Int64): Unit
```

功能：将指定的 64 位有符号整数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 要写入的值。

### func writeln(Int8)

```cangjie
public func writeln(v: Int8): Unit
```

功能：将指定的 8 位有符号整数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 要写入的值。

### func writeln(Rune)

```cangjie
public func writeln(v: Rune): Unit
```

功能：将指定的 Unicode 字符值（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: Rune - 要写入的值。

### func writeln(String)

```cangjie
public func writeln(v: String): Unit
```

功能：将指定的字符串值（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要写入的值。

### func writeln(UInt16)

```cangjie
public func writeln(v: UInt16): Unit
```

功能：将指定的 16 位无符号整数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 要写入的值。

### func writeln(UInt32)

```cangjie
public func writeln(v: UInt32): Unit
```

功能：将指定的 32 位无符号整数值的文本表示（后跟换行符）写入标准输出或标准错误流中。
参数：

- v: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 要写入的值。

### func writeln(UInt64)

```cangjie
public func writeln(v: UInt64): Unit
```

功能：将指定的 64 位无符号整数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 要写入的值。

### func writeln(UInt8)

```cangjie
public func writeln(v: UInt8): Unit
```

功能：将指定的 8 位无符号整数值的文本表示（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 要写入的值。

### func writeln\<T>(T) where T <: ToString

```cangjie
public func writeln<T>(v: T): Unit where T <: ToString
```

功能：将实现了 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 接口的数据类型转换成的字符串（后跟换行符）写入标准输出或标准错误流中。

参数：

- v: T - 要写入的值。
