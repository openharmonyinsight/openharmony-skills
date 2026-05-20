# 类

## class BufferedInputStream\<T> where T <: InputStream

```cangjie
public class BufferedInputStream<T> <: InputStream where T <: InputStream {
    public init(input: T)
    public init(input: T, buffer: Array<Byte>)
    public init(input: T, capacity: Int64)
}
```

功能：提供带缓冲区的输入流。

可将其他 [InputStream](io_package_interfaces.md#interface-inputstream) 类型的输入流（如 [ByteBuffer](io_package_classes.md#class-bytebuffer)）绑定到 [BufferedInputStream](io_package_classes.md#class-bufferedinputstreamt-where-t--inputstream) 实例，从该实例读取数据时，先把数据从被绑定的流读入缓冲区暂存，再从缓冲区读取用户需要的数据。

父类型：

- [InputStream](io_package_interfaces.md#interface-inputstream)

### init(T)

```cangjie
public init(input: T)
```

功能：创建 [BufferedInputStream](io_package_classes.md#class-bufferedinputstreamt-where-t--inputstream) 实例，缓冲区容量取默认值 4096。

参数：

- input: T - 绑定指定输入流。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedInputStream

main(): Unit {
    let inputData = "Hello World".toArray()
    let inputStream = ByteBuffer(inputData)
    /* 绑定指定输入流 */
    let bufferedStream = BufferedInputStream(inputStream)

    /* 从输入流中读取数据 */
    let data = Array<Byte>(inputData.size, repeat: 0)
    bufferedStream.read(data)
    println(String.fromUtf8(data))
}
```

运行结果：

```text
Hello World
```

### init(T, Array\<Byte>)

```cangjie
public init(input: T, buffer: Array<Byte>)
```

功能：创建 [BufferedInputStream](io_package_classes.md#class-bufferedinputstreamt-where-t--inputstream) 实例。

其内部使用的缓存区由入参决定，在注重性能的场景下，通过复用传入的 `buffer`，可以减少内存分配次数，提高性能。

参数：

- input: T - 绑定一个输入流。
- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - [BufferedInputStream](io_package_classes.md#class-bufferedinputstreamt-where-t--inputstream) 使用的内部缓存区。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 大小等于 0 时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedInputStream

main(): Unit {
    let inputStream = ByteBuffer()

    /* 使用合法的内部缓冲区创建 BufferedInputStream 实例，不会抛出异常 */
    try {
        let buffer = Array<Byte>(1024, repeat: 0)
        let bufferedStream = BufferedInputStream(inputStream, buffer)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }

    /* 内部缓冲区大小被定义为 0 的情况 */
    try {
        let invalidBuffer = Array<Byte>()
        let bufferedStream = BufferedInputStream(inputStream, invalidBuffer)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }
}
```

运行结果：

```text
Error: The buffer cannot be empty.
```

### init(T, Int64)

```cangjie
public init(input: T, capacity: Int64)
```

功能：创建 [BufferedInputStream](io_package_classes.md#class-bufferedinputstreamt-where-t--inputstream) 实例。

参数：

- input: T - 绑定指定输入流。
- capacity: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 内部缓冲区容量。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 capacity 小于等于 0 时，抛出异常。

### func read(Array\<Byte>)

```cangjie
public func read(buffer: Array<Byte>): Int64
```

功能：从绑定的输入流读出数据到 `buffer` 中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 存放读取的数据的缓冲区。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 读取数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 为空时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedInputStream

main(): Unit {
    let inputStream = ByteBuffer()

    /* 使用合法的内部缓冲区容量创建 BufferedInputStream 实例，不会抛出异常 */
    try {
        let capacity = 2048
        let bufferedStream = BufferedInputStream(inputStream, capacity)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }

    /* 当内部缓冲区被设置成 0 时，抛出异常 */
    try {
        let zeroCapacity = 0
        let bufferedStream = BufferedInputStream(inputStream, zeroCapacity)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }

    /* 当内部缓冲区被设置成负数时，抛出异常 */
    try {
        let negativeCapacity = -1024
        let bufferedStream = BufferedInputStream(inputStream, negativeCapacity)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }
}
```

运行结果：

```text
Error: Invalid capacity size: capacity = 0.
Error: Invalid capacity size: capacity = -1024.
```

### func readByte()

```cangjie
public func readByte(): ?Byte
```

功能：从输入流中读取一个字节。

返回值：

- ?[Byte](../../core/core_package_api/core_package_types.md#type-byte) - 读取到的数据。读取失败时会返回 `None`。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedInputStream

main(): Unit {
    /* 创建输入流并写入数据 */
    let inputStream = ByteBuffer()
    let sourceData = "abc".toArray()
    inputStream.write(sourceData)
    let bufferedStream = BufferedInputStream(inputStream)

    /* 依次读取所有字节 */
    while (true) {
        let byte = bufferedStream.readByte()
        if (byte == None) {
            break
        }
        println(String.fromUtf8(byte.getOrThrow()))
    }
}
```

运行结果：

```text
a
b
c
```

### func reset(T)

```cangjie
public func reset(input: T): Unit
```

功能：绑定新的输入流，重置状态，但不重置 `capacity`。

参数：

- input: T - 待绑定的输入流。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedInputStream
import std.io.IOException

main(): Unit {
    /* 创建第一个输入流并写入数据 */
    let inputStream1 = ByteBuffer()
    let sourceData1 = "First message: Hello".toArray()
    inputStream1.write(sourceData1)

    /* 创建第二个输入流并写入数据 */
    let inputStream2 = ByteBuffer()
    let sourceData2 = "Second message: World".toArray()
    inputStream2.write(sourceData2)

    /* 使用 BufferedInputStream 包装第一个输入流 */
    let bufferedStream = BufferedInputStream(inputStream1)

    /* 读取第一个输入流的部分数据 */
    var result1 = ""
    for (_ in 0..sourceData1.size) {
        let byte = bufferedStream.readByte()
        if (byte == None) {
            break
        }
        result1 += String.fromUtf8(byte.getOrThrow())
    }
    println(result1)

    /* 重置输入流为第二个输入流 */
    bufferedStream.reset(inputStream2)
    var result2 = ""
    for (_ in 0..sourceData2.size) {
        let byte = bufferedStream.readByte()
        if (byte == None) {
            break
        }
        result2 += String.fromUtf8(byte.getOrThrow())
    }
    println(result2)
}
```

运行结果：

```text
First message: Hello
Second message: World
```

### extend\<T> BufferedInputStream\<T> <: Resource where T <: Resource

```cangjie
extend<T> BufferedInputStream<T> <: Resource where T <: Resource
```

功能：为 [BufferedInputStream](./io_package_classes.md#class-bufferedinputstreamt-where-t--inputstream) 实现 [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource) 接口，该类型对象可在 `try-with-resource` 语法上下文中实现自动资源释放。

父类型：

- [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource)

#### func close()

```cangjie
public func close(): Unit
```

功能：关闭当前流。

> **注意：**
>
> 调用此方法后不可再调用 [BufferedInputStream](io_package_classes.md#class-bufferedinputstreamt-where-t--inputstream) 的其他接口，否则会造成非预期现象。

#### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：判断当前流是否关闭。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果当前流已经被关闭，返回 true，否则返回 false。

示例：

<!-- verify -->
```cangjie
import std.io.BufferedInputStream
import std.io.InputStream
import std.io.ByteBuffer

/**
 * 自定义实现 InputStream 和 Resource 接口的类 A
 */
public class A <: InputStream & Resource {
    private var closed: Bool = false

    public func read(buffer: Array<Byte>): Int64 {
        let inputData = "Hello World".toArray()
        let inputStream = ByteBuffer(inputData)
        let num = inputStream.read(buffer)
        return num
    }

    public func isClosed(): Bool {
        return closed
    }

    public func close(): Unit {
        println("Resource is closed")
        closed = true
    }
}

main(): Unit {
    let bufferedStream = BufferedInputStream(A())

    /* 使用 try-with-resource 语法获取资源 */
    try (r = bufferedStream) {
        println("Get the resource")
        let data = Array<Byte>(11, repeat: 0)
        r.read(data)
        println(r.isClosed())
        println(String.fromUtf8(data))
    }

    /* 自动调用 close() 函数释放资源 */
    println(bufferedStream.isClosed())
}
```

运行结果：

```text
Get the resource
false
Hello World
Resource is closed
true
```

### extend\<T> BufferedInputStream\<T> <: Seekable where T <: Seekable

```cangjie
extend<T> BufferedInputStream<T> <: Seekable where T <: Seekable
```

功能：为 [BufferedInputStream](./io_package_classes.md#class-bufferedinputstreamt-where-t--inputstream) 实现 [Seekable](./io_package_interfaces.md#interface-seekable) 接口，支持查询数据长度，移动光标等操作。

父类型：

- [Seekable](io_package_interfaces.md#interface-seekable)

#### prop length

```cangjie
public prop length: Int64
```

功能：返回当前流中的总数据量（以字节为单位）。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

#### prop position

```cangjie
public prop position: Int64
```

功能：返回当前光标位置。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

#### prop remainLength

```cangjie
public prop remainLength: Int64
```

功能：返回当前流中未读的数据量（以字节为单位）。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

#### func seek(SeekPosition)

```cangjie
public func seek(sp: SeekPosition): Int64
```

功能：移动光标到指定的位置。

> **说明：**
>
> - 指定的位置不能位于流中数据头部之前。
> - 指定位置可以超过流中数据末尾。
> - 调用该函数会先清空缓存区，再移动光标的位置。

参数：

- sp: [SeekPosition](io_package_enums.md#enum-seekposition) - 指定光标移动后的位置。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回流中数据的起点到移动后位置的偏移量（以字节为单位）。

异常：

- [IOException](io_package_exceptions.md#class-ioexception) - 当指定的位置位于流中数据头部之前时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.BufferedInputStream
import std.io.InputStream
import std.io.ByteBuffer
import std.io.Seekable
import std.io.SeekPosition
import std.io.IOException
import std.io.readToEnd

/**
 * 自定义实现 InputStream 和 Seekable 接口的类 A
 */
public class A <: InputStream & Seekable {
    public var inputStream: ByteBuffer = ByteBuffer()

    public func read(buffer: Array<Byte>): Int64 {
        let inputData = "Hello World".toArray()
        inputStream = ByteBuffer(inputData)
        let num = inputStream.read(buffer)
        return num
    }

    public func seek(sp: SeekPosition): Int64 {
        return inputStream.seek(sp)
    }
}

main(): Unit {
    let seekableStream = A()
    let bufferedStream = BufferedInputStream(seekableStream)
    let buffer = Array<Byte>(11, repeat: 0)
    bufferedStream.read(buffer)

    /* 输出当前流中总数据量，当前光标位置，当前流中未读的数据量 */
    println("Length : " + bufferedStream.length.toString())
    println("Position : " + bufferedStream.position.toString())
    println("Remain Length : " + bufferedStream.remainLength.toString())

    /* 移动光标到指定位置，虽然超过了流中数据末尾但是合法的 */
    println("Position after seek() : " + bufferedStream.seek(SeekPosition.Current(11)).toString())

    /* 尝试移动到数据头部之前，抛出异常 */
    try {
        bufferedStream.seek(SeekPosition.Begin(-1))
    } catch (e: IOException) {
        println("Error: " + e.message)
    }

    /* 将光标移动到第一个单词之后，读取后续的数据 */
    bufferedStream.seek(SeekPosition.Begin(6))
    println(String.fromUtf8(readToEnd(seekableStream.inputStream)))
}
```

运行结果：

```text
Length : 11
Position : 11
Remain Length : 0
Position after seek() : 22
Error: Can't move the position before the beginning of the stream.
World
```

## class BufferedOutputStream\<T> where T <: OutputStream

```cangjie
public class BufferedOutputStream<T> <: OutputStream where T <: OutputStream {
    public init(output: T)
    public init(output: T, buffer: Array<Byte>)
    public init(output: T, capacity: Int64)
}
```

功能：提供带缓冲区的输出流。

可将其他 [OutputStream](io_package_interfaces.md#interface-outputstream) 类型的输入流（如 [ByteBuffer](io_package_classes.md#class-bytebuffer)）绑定到 [BufferedOutputStream](io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream) 实例，从该实例写入数据时，先把数据写入缓冲区暂存，再从缓冲区写入数据到流中。

父类型：

- [OutputStream](io_package_interfaces.md#interface-outputstream)

### init(T)

```cangjie
public init(output: T)
```

功能：创建 [BufferedOutputStream](io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream) 实例，缓冲区容量取默认值 4096。

参数：

- output: T - 绑定指定输出流。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedOutputStream
import std.io.readToEnd

main(): Unit {
    let outputStream = ByteBuffer()
    /* 绑定指定输出流 */
    let bufferedStream = BufferedOutputStream(outputStream)

    /* 将输出数据写入缓冲流 bufferedStream 并刷新内部绑定的输出流 outputStream */
    let outputData = "Hello World".toArray()
    bufferedStream.write(outputData)
    bufferedStream.flush()
    println(String.fromUtf8(readToEnd(outputStream)))
}
```

运行结果：

```text
Hello World
```

### init(T, Array\<Byte>)

```cangjie
public init(output: T, buffer: Array<Byte>)
```

功能：创建 [BufferedOutputStream](io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream) 实例。

其内部使用的缓存区由入参决定，在注重性能的场景下，通过复用传入的 `buffer`，可以减少内存分配次数，提高性能。

参数：

- output: T - 绑定一个输出流。
- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - [BufferedOutputStream](io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream) 使用的内部缓存区。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 大小等于 0 时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedOutputStream

main(): Unit {
    let outputStream = ByteBuffer()

    /* 使用合法的内部缓冲区创建 BufferedOutputStream 实例，不会抛出异常 */
    try {
        let buffer = Array<Byte>(1024, repeat: 0)
        let bufferedStream = BufferedOutputStream(outputStream, buffer)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }

    /* 内部缓冲区大小被定义为 0 的情况 */
    try {
        let invalidBuffer = Array<Byte>()
        let bufferedStream = BufferedOutputStream(outputStream, invalidBuffer)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }
}
```

运行结果：

```text
Error: The buffer cannot be empty.
```

### init(T, Int64)

```cangjie
public init(output: T, capacity: Int64)
```

功能：创建 [BufferedOutputStream](io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream) 实例。

参数：

- output: T - 绑定指定输出流。
- capacity: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 内部缓冲区容量。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 capacity 小于等于 0 时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedOutputStream

main(): Unit {
    let outputStream = ByteBuffer()

    /* 使用合法的内部缓冲区容量创建 BufferedoutputStream 实例，不会抛出异常 */
    try {
        let capacity = 2048
        let bufferedStream = BufferedOutputStream(outputStream, capacity)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }

    /* 当内部缓冲区被设置成 0 时，抛出异常 */
    try {
        let zeroCapacity = 0
        let bufferedStream = BufferedOutputStream(outputStream, zeroCapacity)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }

    /* 当内部缓冲区被设置成负数时，抛出异常 */
    try {
        let negativeCapacity = -1024
        let bufferedStream = BufferedOutputStream(outputStream, negativeCapacity)
    } catch (e: IllegalArgumentException) {
        println("Error: ${e.message}")
    }
}
```

运行结果：

```text
Error: Invalid capacity size: capacity = 0.
Error: Invalid capacity size: capacity = -1024.
```

### func flush()

```cangjie
public func flush(): Unit
```

功能：刷新 [BufferedOutputStream](io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream)：将内部缓冲区的剩余数据写入绑定的输出流，并刷新 [BufferedOutputStream](io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream)。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedOutputStream
import std.io.readToEnd

main(): Unit {
    let outputStream = ByteBuffer()
    /* 绑定指定输出流 */
    let bufferedStream = BufferedOutputStream(outputStream)

    /* 将输出数据写入缓冲流 bufferedStream 并刷新内部绑定的输出流 outputStream */
    let outputData = "Hello World".toArray()
    bufferedStream.write(outputData)
    bufferedStream.flush()
    println(String.fromUtf8(readToEnd(outputStream)))
}
```

运行结果：

```text
Hello World
```

### func reset(T)

```cangjie
public func reset(output: T): Unit
```

功能：绑定新的输出流，重置状态，但不重置 `capacity`。

参数：

- output: T - 待绑定的输出流。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedOutputStream
import std.io.IOException
import std.io.readToEnd

main(): Unit {
    /* 创建第一个输出流 */
    let outputStream1 = ByteBuffer()
    let sourceData1 = "First message: Hello".toArray()

    /* 创建第二个输出流 */
    let outputStream2 = ByteBuffer()
    let sourceData2 = "Second message: World".toArray()

    /* 使用 BufferedOutputStream 包装第一个输出流 */
    let bufferedStream = BufferedOutputStream(outputStream1)

    /* 将第一个源数据写入到绑定的第一个输出流中并刷新 */
    bufferedStream.write(sourceData1)
    bufferedStream.flush()
    println(String.fromUtf8(readToEnd(outputStream1)))

    /* 重置输出流为第二个输出流，将第二个源数据写入到绑定的第二个输出流中并刷新 */
    bufferedStream.reset(outputStream2)
    bufferedStream.write(sourceData2)
    bufferedStream.flush()
    println(String.fromUtf8(readToEnd(outputStream2)))
}
```

运行结果：

```text
First message: Hello
Second message: World
```

### func write(Array\<Byte>)

```cangjie
public func write(buffer: Array<Byte>): Unit
```

功能：将 `buffer` 中的数据写入到绑定的输出流中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 待写入数据的缓冲区。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedOutputStream
import std.io.readToEnd

main(): Unit {
    let outputStream = ByteBuffer()
    /* 绑定指定输出流 */
    let bufferedStream = BufferedOutputStream(outputStream)

    /* 将输出数据写入缓冲流 bufferedStream 并刷新内部绑定的输出流 outputStream */
    let outputData = "Hello World".toArray()
    bufferedStream.write(outputData)
    bufferedStream.flush()
    println(String.fromUtf8(readToEnd(outputStream)))
}
```

运行结果：

```text
Hello World
```

### func writeByte(Byte)

```cangjie
public func writeByte(v: Byte): Unit
```

功能：写入一个字节到绑定的输出流中。

参数：

- v: [Byte](../../core/core_package_api/core_package_types.md#type-byte) - 待写入的字节。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.BufferedOutputStream
import std.io.readToEnd

main(): Unit {
    let outputStream = ByteBuffer()
    /* 绑定指定输出流 */
    let bufferedStream = BufferedOutputStream(outputStream)

    /* 将输出数据逐个写入缓冲流 bufferedStream 并刷新内部绑定的输出流 outputStream */
    let outputData = "Hello World".toArray()
    for (byte in outputData) {
        bufferedStream.writeByte(byte)
    }
    bufferedStream.flush()
    println(String.fromUtf8(readToEnd(outputStream)))
}
```

运行结果：

```text
Hello World
```

### extend\<T> BufferedOutputStream\<T> <: Resource where T <: Resource

```cangjie
extend<T> BufferedOutputStream<T> <: Resource where T <: Resource
```

功能：为 [BufferedOutputStream](./io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream) 实现 [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource) 接口，该类型对象可在 `try-with-resource` 语法上下文中实现自动资源释放。

父类型：

- [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource)

#### func close()

```cangjie
public func close(): Unit
```

功能：关闭当前流。

> **注意：**
>
> 调用此方法后不可再调用 [BufferedOutputStream](io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream) 的其他接口，否则会造成非预期现象。

#### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：判断当前流是否关闭。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果当前流已经被关闭，返回 true，否则返回 false。

示例：

<!-- verify -->
```cangjie
import std.io.BufferedOutputStream
import std.io.OutputStream
import std.io.ByteBuffer
import std.io.readToEnd

/**
 * 自定义实现 OutputStream 和 Resource 接口的类 A
 */
public class A <: OutputStream & Resource {
    private var closed: Bool = false
    public var outputStream = ByteBuffer()

    public func write(buffer: Array<Byte>): Unit {
        this.outputStream = ByteBuffer(buffer)
    }

    public func isClosed(): Bool {
        return closed
    }

    public func close(): Unit {
        println("Resource is closed")
        closed = true
    }
}

main(): Unit {
    let resourceStream = A()
    let bufferedStream = BufferedOutputStream(resourceStream)

    /* 使用 try-with-resource 语法获取资源 */
    try (r = bufferedStream) {
        println("Get the resource")
        let data = "Hello World".toArray()
        r.write(data)
        r.flush()
        println(r.isClosed())
        println(String.fromUtf8(readToEnd(resourceStream.outputStream)))
    }

    /* 自动调用 close() 函数释放资源 */
    println(bufferedStream.isClosed())
}
```

运行结果：

```text
Get the resource
false
Hello World
Resource is closed
true
```

### extend\<T> BufferedOutputStream\<T> <: Seekable where T <: Seekable

```cangjie
extend<T> BufferedOutputStream<T> <: Seekable where T <: Seekable
```

功能：为 [BufferedOutputStream](./io_package_classes.md#class-bufferedoutputstreamt-where-t--outputstream) 实现 [Seekable](./io_package_interfaces.md#interface-seekable) 接口，支持查询数据长度，移动光标等操作。

父类型：

- [Seekable](io_package_interfaces.md#interface-seekable)

#### prop length

```cangjie
public prop length: Int64
```

功能：返回当前流中的总数据量（以字节为单位）。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

#### prop position

```cangjie
public prop position: Int64
```

功能：返回当前光标位置。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

#### prop remainLength

```cangjie
public prop remainLength: Int64
```

功能：返回当前流中未读的数据量（以字节为单位）。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

#### func seek(SeekPosition)

```cangjie
public func seek(sp: SeekPosition): Int64
```

功能：移动光标到指定的位置。

> **说明：**
>
> - 指定的位置不能位于流中数据头部之前。
> - 指定位置可以超过流中数据末尾。
> - 调用该函数会先将缓存区内的数据写到绑定的输出流里，再移动光标的位置。

参数：

- sp: [SeekPosition](io_package_enums.md#enum-seekposition) - 指定光标移动后的位置。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回流中数据的起点到移动后位置的偏移量（以字节为单位）。

异常：

- [IOException](io_package_exceptions.md#class-ioexception) - 当指定的位置位于流中数据头部之前时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.BufferedOutputStream
import std.io.OutputStream
import std.io.ByteBuffer
import std.io.Seekable
import std.io.SeekPosition
import std.io.IOException
import std.io.readToEnd

/**
 * 自定义实现 OutputStream 和 Seekable 接口的类 A
 */
public class A <: OutputStream & Seekable {
    public var outputStream: ByteBuffer = ByteBuffer()

    public func write(buffer: Array<Byte>): Unit {
        this.outputStream = ByteBuffer(buffer)
    }

    public func seek(sp: SeekPosition): Int64 {
        return outputStream.seek(sp)
    }
}

main(): Unit {
    let seekableStream = A()
    let bufferedStream = BufferedOutputStream(seekableStream)
    let data = "Hello World".toArray()
    bufferedStream.write(data)
    bufferedStream.flush()

    /* 输出当前流中总数据量，当前光标位置，当前流中未读的数据量 */
    println("Length : " + bufferedStream.length.toString())
    println("Position : " + bufferedStream.position.toString())
    println("Remain Length : " + bufferedStream.remainLength.toString())

    /* 移动光标到指定位置，虽然超过了流中数据末尾但是合法的 */
    println("Position after seek() : " + bufferedStream.seek(SeekPosition.Current(11)).toString())

    /* 尝试移动到数据头部之前，抛出异常 */
    try {
        bufferedStream.seek(SeekPosition.Begin(-1))
    } catch (e: IOException) {
        println("Error: " + e.message)
    }

    /* 将光标移动到第一个单词之后，读取后续的数据 */
    bufferedStream.seek(SeekPosition.Begin(6))
    println(String.fromUtf8(readToEnd(seekableStream.outputStream)))
}
```

运行结果：

```text
Length : 11
Position : 0
Remain Length : 11
Position after seek() : 11
Error: Can't move the position before the beginning of the stream.
World
```

## class ByteBuffer

```cangjie
public class ByteBuffer <: IOStream & Seekable {
    public init()
    public init(capacity: Int64)
    public init(source: Array<Byte>)
}
```

功能：基于 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> 数据类型，提供对字节流的写入、读取等操作。

父类型：

- [IOStream](io_package_interfaces.md#interface-iostream)
- [Seekable](io_package_interfaces.md#interface-seekable)

### prop capacity

```cangjie
public prop capacity: Int64
```

功能：获取当前缓冲区容量。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前缓冲区容量。

### init()

```cangjie
public init()
```

功能：创建 [ByteBuffer](io_package_classes.md#class-bytebuffer) 实例，默认的初始容量是 32。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let buffer = ByteBuffer()
    println(buffer.capacity)
}
```

运行结果：

```text
32
```

### init(Array\<Byte>)

```cangjie
public init(source: Array<Byte>)
```

功能：根据传入的数组构造 [ByteBuffer](io_package_classes.md#class-bytebuffer) 实例。

参数：

- source: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 传入的数组。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let inputData = "Hello World".toArray()
    let buffer = ByteBuffer(inputData)
    println(buffer.capacity)

    /* 从缓冲区中读取数据 */
    println(String.fromUtf8(buffer.bytes()))
}
```

运行结果：

```text
11
Hello World
```

### init(Int64)

```cangjie
public init(capacity: Int64)
```

功能：创建 [ByteBuffer](io_package_classes.md#class-bytebuffer) 实例。

参数：

- capacity: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定的初始容量。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 capacity 小于 0 时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let buffer = ByteBuffer(1024)
    println(buffer.capacity)

    try {
        let errorBuffer = ByteBuffer(-1024)
        println(errorBuffer.capacity)
    } catch (e: Exception) {
        println("Error: ${e.message}")
    }
}
```

运行结果：

```text
1024
Error: The capacity must be greater than or equal to 0: -1024.
```

### func bytes()

```cangjie
public func bytes(): Array<Byte>
```

功能：获取当前 [ByteBuffer](io_package_classes.md#class-bytebuffer) 中未被读取的数据的切片。

> **注意：**
>
> - 缓冲区进行读取，写入或重置等修改操作会导致这个切片失效。
> - 对切片的修改会影响缓冲区的内容。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 当前流中未被读取的数据的切片。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let inputData = "Hello World".toArray()
    let buffer = ByteBuffer(inputData)

    /* 从缓冲区中读取数据 */
    println(String.fromUtf8(buffer.bytes()))
}
```

运行结果：

```text
Hello World
```

### func clear()

```cangjie
public func clear(): Unit
```

功能：清除当前 [ByteBuffer](io_package_classes.md#class-bytebuffer) 中所有数据。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let inputData = "Hello World".toArray()
    let buffer = ByteBuffer(inputData)
    println(buffer.capacity)

    /* 读取原始数据 */
    println(String.fromUtf8(buffer.bytes()))

    /* 清除缓冲区 */
    buffer.clear()

    /* 读取清除后的缓冲区 */
    println("buffer after clear: " + String.fromUtf8(buffer.bytes()))
    println("capacity after clear: ${buffer.capacity}")
}
```

运行结果：

```text
11
Hello World
buffer after clear: 
capacity after clear: 11
```

### func clone()

```cangjie
public func clone(): ByteBuffer
```

功能：用当前 [ByteBuffer](io_package_classes.md#class-bytebuffer) 中的数据来构造一个新的 [ByteBuffer](io_package_classes.md#class-bytebuffer)。

返回值：

- [ByteBuffer](io_package_classes.md#class-bytebuffer) - 新构造的 [ByteBuffer](io_package_classes.md#class-bytebuffer) 对象。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let inputData = "Hello World".toArray()
    let originalBuffer = ByteBuffer(inputData)

    /* 克隆原始缓冲区 */
    let clonedBuffer = originalBuffer.clone()

    println("originalBuffer: " + String.fromUtf8(originalBuffer.bytes()))
    println("clonedBuffer: " + String.fromUtf8(clonedBuffer.bytes()))

    /* 修改原始缓冲区的数据 */
    originalBuffer.write(" New Data".toArray())

    println("originalBuffer: " + String.fromUtf8(originalBuffer.bytes()))
    println("clonedBuffer: " + String.fromUtf8(clonedBuffer.bytes()))
}
```

运行结果：

```text
originalBuffer: Hello World
clonedBuffer: Hello World
originalBuffer: Hello World New Data
clonedBuffer: Hello World
```

### func read(Array\<Byte>)

```cangjie
public func read(buffer: Array<Byte>): Int64
```

功能：从输入流中读取数据放到 buffer 中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 存放读取的数据的缓冲区。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 读取数据的字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 为空时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let inputData = "Hello World".toArray()
    let buffer = ByteBuffer(inputData)

    /* 创建一个目标缓冲区，读取数据到目标缓冲区 */
    let targetBuffer = Array<Byte>(5, repeat: 0)
    buffer.read(targetBuffer)
    println(String.fromUtf8(targetBuffer))

    /* 尝试读取空缓冲区 */
    try {
        let emptyBuffer = Array<Byte>()
        buffer.read(emptyBuffer)
    } catch (e: IllegalArgumentException) {
        println("Error: " + e.message)
    }
}
```

运行结果：

```text
Hello
Error: The buffer is empty.
```

### func readByte()

```cangjie
public func readByte(): ?Byte
```

功能：从输入流中读取一个字节。

返回值：

- ?[Byte](../../core/core_package_api/core_package_types.md#type-byte) - 读取到的数据。读取失败时会返回 `None`。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let inputData = "Hello World".toArray()
    let buffer = ByteBuffer(inputData)

    for (_ in 0..inputData.size) {
        print(String.fromUtf8(buffer.readByte().getOrThrow()))
    }
    println()

    /* 尝试读取下一个不存在的字节 */
    let nextByte = buffer.readByte()
    match (nextByte) {
        case None => println("nextByte: None")
        case _ => println("nextByte: ${nextByte.getOrThrow()}")
    }
}
```

运行结果：

```text
Hello World
nextByte: None
```

### func reserve(Int64)

```cangjie
public func reserve(additional: Int64): Unit
```

功能：将缓冲区扩容指定大小。

> **说明：**
>
> - 当缓冲区剩余字节数大于等于 `additional` 时不发生扩容。
> - 当缓冲区剩余字节数量小于 `additional` 时，取（`additional` + `capacity`）与（`capacity`的 1.5 倍向下取整）两个值中的最大值进行扩容。

参数：

- additional: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 将要扩容的大小。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 additional 小于 0 时，抛出异常。
- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当扩容后的缓冲区大小超过 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 的最大值时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let buffer = ByteBuffer(11)
    println("initial capacity: " + buffer.capacity.toString())
    buffer.write("Hello World".toArray())

    /* 尝试扩容，需要增加的容量大于剩余空间，发生扩容 */
    buffer.reserve(5)
    println("reserve 5: " + buffer.capacity.toString())

    /* 尝试扩容，需要增加的容量小于剩余空间，不发生扩容 */
    buffer.reserve(2)
    println("reserve 2: " + buffer.capacity.toString())

    /* 尝试扩容，additional 为负数 */
    try {
        buffer.reserve(-1)
    } catch (e: IllegalArgumentException) {
        println("Error: " + e.message)
    }

    /* 尝试扩容，导致容量超过 Int64 最大值 */
    try {
        buffer.reserve(Int64.Max - buffer.capacity + 1)
    } catch (e: OverflowException) {
        println("Error: " + e.message)
    }
}
```

运行结果：

```text
initial capacity: 11
reserve 5: 16
reserve 2: 16
Error: The additional must be greater than or equal to 0.
Error: The maximum value for capacity expansion cannot exceed the maximum value of Int64.
```

### func seek(SeekPosition)

```cangjie
public func seek(sp: SeekPosition): Int64
```

功能：将光标跳转到指定位置。

> **说明：**
>
> - 指定的位置不能位于流中数据头部之前。
> - 指定位置可以超过流中数据末尾。

参数：

- sp: [SeekPosition](io_package_enums.md#enum-seekposition) - 指定光标跳转后的位置。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 流中数据的头部到跳转后位置的偏移量（以字节为单位）。

异常：

- [IOException](io_package_exceptions.md#class-ioexception) - 当指定的位置位于流中数据头部之前时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer
import std.io.SeekPosition
import std.io.IOException

main(): Unit {
    let buffer = ByteBuffer("Hello World".toArray())
    println("initial position: ${buffer.position}")

    /* 移动到当前位置之后 6 个字节 */
    buffer.seek(SeekPosition.Current(6))
    println(String.fromUtf8(buffer.bytes()))

    /* 移动位置超过流中数据末尾，为合法操作 */
    println(buffer.seek(SeekPosition.End(1)))

    /* 尝试移动到数据头部之前，抛出异常 */
    try {
        buffer.seek(SeekPosition.Begin(-1))
    } catch (e: IOException) {
        println("Error: " + e.message)
    }
}
```

运行结果：

```text
initial position: 0
World
12
Error: Can't move the position before the beginning of the stream.
```

### func setLength(Int64)

```cangjie
public func setLength(length: Int64): Unit
```

功能：将当前数据修改为指定长度。该操作不会改变 seek 的偏移。

参数：

- length: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 要修改的长度。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 `length` 小于 0 时，抛此异常。
- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当 length 过大导致扩容后的缓冲区大小超过 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 的最大值时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let buffer = ByteBuffer("Hello World".toArray())
    println("initial length: " + buffer.length.toString())

    /* 设置长度为 5，并读取缓冲区中所有的内容 */
    buffer.setLength(5)
    println("set length to 5: " + String.fromUtf8(buffer.bytes()))

    /* 尝试设置扩容后的缓冲区大小超过 Int64 的最大值时，抛出异常 */
    try {
        buffer.setLength(Int64.Max + 1)
    } catch (e: OverflowException) {
        println("Error: " + e.message)
    }

    /* 尝试设置长度为-1，抛出异常 */
    try {
        buffer.setLength(-1)
    } catch (e: IllegalArgumentException) {
        println("Error: " + e.message)
    }
}
```

运行结果：

```text
initial length: 11
set length to 5: Hello
Error: add
Error: The length must be greater than or equal to 0.
```

### func write(Array\<Byte>)

```cangjie
public func write(buffer: Array<Byte>): Unit
```

功能：将 `buffer` 中的数据写入到输出流中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 待写入数据的缓冲区。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let buffer = ByteBuffer()
    let dataToWrite = "Hello World".toArray()

    /* 写入数据 */
    buffer.write(dataToWrite)
    println(String.fromUtf8(buffer.bytes()))
}
```

运行结果：

```text
Hello World
```

### func writeByte(Byte)

```cangjie
public func writeByte(v: Byte): Unit
```

功能：将一个字节写入到输出流中。

参数：

- v: [Byte](../../core/core_package_api/core_package_types.md#type-byte) - 待写入的字节。

示例：

<!-- verify -->
```cangjie
import std.io.ByteBuffer

main(): Unit {
    let buffer = ByteBuffer()
    let dataToWrite: Array<Byte> = "Hello World".toArray()

    /* 每次写入单个字节 */
    for (i in 0..dataToWrite.size) {
        buffer.writeByte(dataToWrite[i])
    }

    println(String.fromUtf8(buffer.bytes()))
}
```

运行结果：

```text
Hello World
```

## class ChainedInputStream\<T> where T <: InputStream

```cangjie
public class ChainedInputStream<T> <: InputStream where T <: InputStream {
    public init(input: Array<T>)
}
```

功能：提供顺序从 [InputStream](io_package_interfaces.md#interface-inputstream) 数组中读取数据的能力。

父类型：

- [InputStream](io_package_interfaces.md#interface-inputstream)

### init(Array\<T>)

```cangjie
public init(input: Array<T>)
```

功能：创建 [ChainedInputStream](io_package_classes.md#class-chainedinputstreamt-where-t--inputstream) 实例。

参数：

- input: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 绑定指定输入流数组。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 input 为空时，抛出异常。

### func read(Array\<Byte>)

```cangjie
public func read(buffer: Array<Byte>): Int64
```

功能：依次从绑定 [InputStream](io_package_interfaces.md#interface-inputstream) 数组中读出数据到 buffer 中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 存储读出数据的缓冲区。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 读取字节数。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 buffer 为空时，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.io.*

main(): Unit {
    let inputData = "Hello World".toArray()
    let bufferInput = ByteBuffer(inputData)
    let cis = ChainedInputStream(bufferInput)

    // 缓冲区容量是 7
    let bufferOutput = Array<Byte>(7, repeat: 0)
    cis.read(bufferOutput)
    let result = String.fromUtf8(bufferOutput)
    println(result)
}
```

运行结果：

```text
Hello W
```

## class MultiOutputStream\<T> where T <: OutputStream

```cangjie
public class MultiOutputStream<T> <: OutputStream where T <: OutputStream {
    public init(output: Array<T>)
}
```

功能：提供将数据同时写入到 [OutputStream](io_package_interfaces.md#interface-outputstream) 数组中每个输出流中的能力。

父类型：

- [OutputStream](io_package_interfaces.md#interface-outputstream)

### init(Array\<T>)

```cangjie
public init(output: Array<T>)
```

功能：创建 [MultiOutputStream](io_package_classes.md#class-multioutputstreamt-where-t--outputstream) 实例。

参数：

- output: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 绑定指定输出流数组。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 output 为空时，抛出异常。

### func flush()

```cangjie
public func flush(): Unit
```

功能：刷新绑定的输出流数组里的每个输出流。

### func write(Array\<Byte>)

```cangjie
public func write(buffer: Array<Byte>): Unit
```

功能：将 buffer 同时写入到绑定的 [OutputStream](io_package_interfaces.md#interface-outputstream) 数组里的每个输出流中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 存储待写入数据的缓冲区。

## class StringReader\<T> where T <: InputStream

```cangjie
public class StringReader<T> where T <: InputStream {
    public init(input: T)
}
```

功能：提供从 [InputStream](io_package_interfaces.md#interface-inputstream) 输入流中读出数据并转换成字符或字符串的能力。

> **说明：**
>
> - [StringReader](io_package_classes.md#class-stringreadert-where-t--inputstream) 内部默认有缓冲区，缓冲区容量 4096 个字节。
> - [StringReader](io_package_classes.md#class-stringreadert-where-t--inputstream) 目前仅支持 UTF-8 编码，暂不支持 UTF-16、UTF-32。

### init(T)

```cangjie
public init(input: T)
```

功能：创建 [StringReader](io_package_classes.md#class-stringreadert-where-t--inputstream) 实例。

参数：

- input: T - 待读取数据的输入流。

### func lines()

```cangjie
public func lines(): Iterator<String>
```

功能：获得 [StringReader](io_package_classes.md#class-stringreadert-where-t--inputstream) 的行迭代器。

相当于循环调用 `func readln()`，内部遇到非法字符时也会抛出异常。

> **说明：**
>
> - 每行都由换行符进行分隔。
> - 换行符是 `\n` `\r` `\r\n` 之一。
> - 每行不包括换行符。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 字符串的行迭代器。

异常：

- [ContentFormatException](io_package_exceptions.md#class-contentformatexception) - 当`for-in`或者调用`next()`方法时读取到非法字符，抛出异常。

### func read()

```cangjie
public func read(): ?Rune
```

功能：按字符读取流中的数据。

返回值：

- ?[Rune](../../core/core_package_api/core_package_intrinsics.md#rune) - 读取成功，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)>.Some(c)，c 为该次读出的字符；否则返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)>.None。

异常：

- [ContentFormatException](io_package_exceptions.md#class-contentformatexception) - 当读取到非法字符时，抛出异常。

### func readln()

```cangjie
public func readln(): Option<String>
```

功能：按行读取流中的数据。

> **说明：**
>
> - 读取的数据会去掉原换行符。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 读取成功，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>.Some(str)，str 为该次读出的字符串；否则返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>.None。

异常：

- [ContentFormatException](io_package_exceptions.md#class-contentformatexception) - 当读取到非法字符时，抛出异常。

### func readToEnd()

```cangjie
public func readToEnd(): String
```

功能：读取流中所有剩余数据。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 流中所有剩余数据。

异常：

- [ContentFormatException](io_package_exceptions.md#class-contentformatexception) - 当读取到非法字符时，抛出异常。

### func readUntil((Rune)->Bool)

```cangjie
public func readUntil(predicate: (Rune)->Bool): Option<String>
```

功能：从流内读取到使 `predicate` 返回 true 的字符位置（包含这个字符）或者流结束位置的数据。

参数：

- predicate: ([Rune](../../core/core_package_api/core_package_intrinsics.md#rune))->Bool - 满足一定条件返回 `true` 的表达式。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 读取成功，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>.Some(str)，str 为该次读出的字符串；否则返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>.None。

异常：

- [ContentFormatException](io_package_exceptions.md#class-contentformatexception) - 当读取到非法字符时，抛出异常。

### func readUntil(Rune)

```cangjie
public func readUntil(v: Rune): Option<String>
```

功能：从流内读取到指定字符（包含指定字符）或者流结束位置的数据。

参数：

- v: [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) - 指定字符。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 读取成功，返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>.Some(str)，str 为该次读出的字符串；否则返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>.None。

异常：

- [ContentFormatException](io_package_exceptions.md#class-contentformatexception) - 当读取到非法字符时，抛出异常。

### func runes()

```cangjie
public func runes(): Iterator<Rune>
```

功能：获得 [StringReader](io_package_classes.md#class-stringreadert-where-t--inputstream) 的 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 迭代器。

返回值：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)> - 字符串的 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 迭代器。

异常：

- [ContentFormatException](io_package_exceptions.md#class-contentformatexception) - 当`for-in`或者调用`next()`方法时读取到非法字符，抛出异常。

### extend\<T> StringReader\<T> <: Resource where T <: Resource

```cangjie
extend<T> StringReader<T> <: Resource where T <: Resource
```

功能：为 [StringReader](./io_package_classes.md#class-stringreadert-where-t--inputstream) 实现 [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource) 接口，该类型对象可在 `try-with-resource` 语法上下文中实现自动资源释放。

父类型：

- [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource)

#### func close()

```cangjie
public func close(): Unit
```

功能：关闭当前流。

> **注意：**
>
> 调用此方法后不可再调用 [StringReader](io_package_classes.md#class-stringreadert-where-t--inputstream) 的其他接口，否则会造成非预期现象。

#### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：判断当前流是否关闭。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果当前流已经被关闭，返回 true，否则返回 false。

### extend\<T> StringReader\<T> <: Seekable where T <: Seekable

```cangjie
extend<T> StringReader<T> <: Seekable where T <: Seekable
```

功能：为 [StringReader](./io_package_classes.md#class-stringreadert-where-t--inputstream) 实现 [Seekable](./io_package_interfaces.md#interface-seekable) 接口，支持查询数据长度，移动光标等操作。

父类型：

- [Seekable](io_package_interfaces.md#interface-seekable)

#### prop position

```cangjie
public prop position: Int64
```

功能：返回当前光标位置。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

#### func seek(SeekPosition)

```cangjie
public func seek(sp: SeekPosition): Int64
```

功能：移动光标到指定的位置。

> **说明：**
>
> - 指定的位置不能位于流中数据头部之前。
> - 指定位置可以超过流中数据末尾。

参数：

- sp: [SeekPosition](io_package_enums.md#enum-seekposition) - 指定光标移动后的位置。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回流中数据的起点到移动后位置的偏移量（以字节为单位）。

异常：

- [IOException](io_package_exceptions.md#class-ioexception) - 当指定的位置位于流中数据头部之前时，抛出异常。

## class StringWriter\<T> where T <: OutputStream

```cangjie
public class StringWriter<T> where T <: OutputStream {
    public init(output: T)
}
```

功能：提供将 [String](../../core/core_package_api/core_package_structs.md#struct-string) 以及一些 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 类型转换成指定编码格式和字节序配置的字符串并写入到输出流的能力。

> **说明：**
>
> - [StringWriter](io_package_classes.md#class-stringwritert-where-t--outputstream) 内部默认有缓冲区，缓冲区容量 4096 个字节。
> - [StringWriter](io_package_classes.md#class-stringwritert-where-t--outputstream) 目前仅支持 UTF-8 编码，暂不支持 UTF-16、UTF-32。

### init(T)

```cangjie
public init(output: T)
```

功能：创建 [StringWriter](io_package_classes.md#class-stringwritert-where-t--outputstream) 实例。

参数：

- output: T - 待写入数据的输出流。

### func flush()

```cangjie
public func flush(): Unit
```

功能：刷新内部缓冲区，将缓冲区数据写入 output 中，并刷新 output。

### func write(Bool)

```cangjie
public func write(v: Bool): Unit
```

功能：写入 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型。

参数：

- v: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型的实例。

### func write(Float16)

```cangjie
public func write(v: Float16): Unit
```

功能：写入 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型。

参数：

- v: [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型的实例。

### func write(Float32)

```cangjie
public func write(v: Float32): Unit
```

功能：写入 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型。

参数：

- v: [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型的实例。

### func write(Float64)

```cangjie
public func write(v: Float64): Unit
```

功能：写入 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型。

参数：

- v: [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型的实例。

### func write(Int16)

```cangjie
public func write(v: Int16): Unit
```

功能：写入 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型。

参数：

- v: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型的实例。

### func write(Int32)

```cangjie
public func write(v: Int32): Unit
```

功能：写入 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型。

参数：

- v: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型的实例。

### func write(Int64)

```cangjie
public func write(v: Int64): Unit
```

功能：写入 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型。

参数：

- v: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型的实例。

### func write(Int8)

```cangjie
public func write(v: Int8): Unit
```

功能：写入 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型。

参数：

- v: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型的实例。

### func write(Rune)

```cangjie
public func write(v: Rune): Unit
```

功能：写入 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型。

参数：

- v: [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) - [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型的实例。

### func write(String)

```cangjie
public func write(v: String): Unit
```

功能：写入字符串。

参数：

- v: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待写入的字符串。

### func write(UInt16)

```cangjie
public func write(v: UInt16): Unit
```

功能：写入 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型。

参数：

- v: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型的实例。

### func write(UInt32)

```cangjie
public func write(v: UInt32): Unit
```

功能：写入 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型。

参数：

- v: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型的实例。

### func write(UInt64)

```cangjie
public func write(v: UInt64): Unit
```

功能：写入 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型。

参数：

- v: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型的实例。

### func write(UInt8)

```cangjie
public func write(v: UInt8): Unit
```

功能：写入 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型。

参数：

- v: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型的实例。

### func write\<T>(T) where T <: ToString

```cangjie
public func write<T>(v: T): Unit where T <: ToString
```

功能：写入 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 类型。

参数：

- v: T - [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 类型的实例。

### func writeln()

```cangjie
public func writeln(): Unit
```

功能：写入换行符。

### func writeln(Bool)

```cangjie
public func writeln(v: Bool): Unit
```

功能：写入 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型 + 换行符。

参数：

- v: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型的实例。

### func writeln(Float16)

```cangjie
public func writeln(v: Float16): Unit
```

功能：写入 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型 + 换行符。

参数：

- v: [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) - [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型的实例。

### func writeln(Float32)

```cangjie
public func writeln(v: Float32): Unit
```

功能：写入 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型 + 换行符。

参数：

- v: [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型的实例。

### func writeln(Float64)

```cangjie
public func writeln(v: Float64): Unit
```

功能：写入 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型 + 换行符。

参数：

- v: [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型的实例。

### func writeln(Int16)

```cangjie
public func writeln(v: Int16): Unit
```

功能：写入 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型 + 换行符。

参数：

- v: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型的实例。

### func writeln(Int32)

```cangjie
public func writeln(v: Int32): Unit
```

功能：写入 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型 + 换行符。

参数：

- v: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型的实例。

### func writeln(Int64)

```cangjie
public func writeln(v: Int64): Unit
```

功能：写入 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型 + 换行符。

参数：

- v: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型的实例。

### func writeln(Int8)

```cangjie
public func writeln(v: Int8): Unit
```

功能：写入 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型 + 换行符。

参数：

- v: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型的实例。

### func writeln(Rune)

```cangjie
public func writeln(v: Rune): Unit
```

功能：写入 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型 + 换行符。

参数：

- v: [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) - [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型的实例。

### func writeln(String)

```cangjie
public func writeln(v: String): Unit
```

功能：写入字符串 + 换行符。

参数：

- v: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待写入的字符串。

### func writeln(UInt16)

```cangjie
public func writeln(v: UInt16): Unit
```

功能：写入 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型 + 换行符。

参数：

- v: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型的实例。

### func writeln(UInt32)

```cangjie
public func writeln(v: UInt32): Unit
```

功能：写入 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型 + 换行符。

参数：

- v: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型的实例。

### func writeln(UInt64)

```cangjie
public func writeln(v: UInt64): Unit
```

功能：写入 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型 + 换行符。

参数：

- v: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型的实例。

### func writeln(UInt8)

```cangjie
public func writeln(v: UInt8): Unit
```

功能：写入 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型 + 换行符。

参数：

- v: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型的实例。

### func writeln\<T>(T) where T <: ToString

```cangjie
public func writeln<T>(v: T): Unit where T <: ToString
```

功能：写入 [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 类型 + 换行符。

参数：

- v: T - [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring) 类型的实例。

### extend\<T> StringWriter\<T> <: Resource where T <: Resource

```cangjie
extend<T> StringWriter<T> <: Resource where T <: Resource
```

功能：为 [StringWriter](./io_package_classes.md#class-stringwritert-where-t--outputstream) 实现 [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource) 接口，该类型对象可在 `try-with-resource` 语法上下文中实现自动资源释放。

父类型：

- [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource)

#### func close()

```cangjie
public func close(): Unit
```

功能：关闭当前流。

> **注意：**
>
> 调用此方法后不可再调用 [StringWriter](io_package_classes.md#class-stringwritert-where-t--outputstream) 的其他接口，否则会造成非预期现象。

#### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：判断当前流是否关闭。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果当前流已经被关闭，返回 true，否则返回 false。

### extend\<T> StringWriter\<T> <: Seekable where T <: Seekable

```cangjie
extend<T> StringWriter<T> <: Seekable where T <: Seekable
```

功能：为 [StringWriter](./io_package_classes.md#class-stringwritert-where-t--outputstream) 实现 [Seekable](./io_package_interfaces.md#interface-seekable) 接口，支持查询数据长度，移动光标等操作。

父类型：

- [Seekable](io_package_interfaces.md#interface-seekable)

#### func seek(SeekPosition)

```cangjie
public func seek(sp: SeekPosition): Int64
```

功能：移动光标到指定的位置。

> **说明：**
>
> - 指定的位置不能位于流中数据头部之前。
> - 指定位置可以超过流中数据末尾。

参数：

- sp: [SeekPosition](io_package_enums.md#enum-seekposition) - 指定光标移动后的位置。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回流中数据的起点到移动后位置的偏移量（以字节为单位）。

异常：

- [IOException](io_package_exceptions.md#class-ioexception) - 当指定的位置位于流中数据头部之前时，抛出异常。
