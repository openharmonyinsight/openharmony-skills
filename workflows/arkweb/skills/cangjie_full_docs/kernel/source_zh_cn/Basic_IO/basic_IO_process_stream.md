# I/O 处理流

处理流是指代理其他数据流进行处理的流。

仓颉编程语言中常见的处理流包含 `BufferedInputStream`、`BufferedOutputStream`、`StringReader`、`StringWriter`、`ChainedInputStream` 等。

本章介绍缓冲流和字符串流。

## 缓冲流

由于涉及磁盘的 I/O 操作相比内存的 I/O 操作要慢很多，所以对于高频次且小数据量的读写操作来说，不带缓冲的数据流效率很低，每次读取和写入数据都会带来大量的 I/O 耗时。而带缓冲的数据流，可以多次读写数据，但不触发磁盘 I/O 操作，只是先放到内存里。等凑够了缓冲区大小的时候再一次性操作磁盘，这种方式可以显著减少磁盘操作次数，从而提升性能表现。

仓颉编程语言标准库提供了 `BufferedInputStream` 和 `BufferedOutputStream` 这两个类型用来提供缓冲功能。

使用 `BufferedInputStream` 和 `BufferedOutputStream` 类型需要导入 `io` 包。

导入 io 包示例：

<!-- run -->

```cangjie
import std.io.*
```

`BufferedInputStream` 的作用是为另一个输入流添加缓冲的功能。本质上 `BufferedInputStream` 是通过一个内部缓冲数组实现的。

当通过 `BufferedInputStream` 来读取流的数据时，`BufferedInputStream` 会一次性读取整个缓冲区大小的数据，再使用 `read` 函数就可以分多次读取更小规模的数据；当缓冲区中的数据被读完之后，输入流就会再次填充缓冲区；如此反复，直到读完数据流的所有数据。

如果构造一个 `BufferedInputStream`，只需要在构造函数中传入另一个输入流。如果需要指定缓冲区的大小，也可以额外传入 `capacity` 参数进行指定。

BufferedInputStream 构造示例：

<!-- run -->

```cangjie
import std.io.{ByteBuffer, BufferedInputStream}

main(): Unit {
    let arr1 = "0123456789".toArray()
    let byteBuffer = ByteBuffer()
    byteBuffer.write(arr1)
    let bufferedInputStream = BufferedInputStream(byteBuffer)
    let arr2 = Array<Byte>(20, repeat: 0)

    /* 读取流中数据，返回读取到的数据的长度 */
    let readLen = bufferedInputStream.read(arr2)
    println(String.fromUtf8(arr2[..readLen])) // 0123456789
}
```

`BufferedOutputStream` 的作用是为另一个输出流添加缓冲的功能。BufferedOutputStream 也是通过一个内部缓冲数组实现的。

当通过 `BufferedOutputStream` 来向输出流写入数据时，`write` 的数据会先写入内部缓冲数组中；当缓冲区中的数据被填满之后，`BufferedOutputStream` 会将缓冲区的数据一次性写入输出流中，然后清空缓冲区再次被写入；如此反复，直到写完所有的数据。

需要注意的是，由于没写够缓冲区时不会触发输出流的写入操作，所以当往 `BufferedOutputStream` 写完所有的数据后，需要额外调用 `flush` 函数来最终完成写入。

如果构造一个 `BufferedOutputStream`，只需要在构造函数中传入另一个输出流。如果需要指定缓冲区的大小，也可以额外传入 `capacity` 参数指定。

BufferedOutputStream 构造示例：

<!-- run -->

```cangjie
import std.io.{ByteBuffer, BufferedOutputStream, readToEnd}

main(): Unit {
    let arr1 = "01234".toArray()
    let byteBuffer = ByteBuffer()
    byteBuffer.write(arr1)
    let bufferedOutputStream = BufferedOutputStream(byteBuffer)
    let arr2 = "56789".toArray()

    /* 向流中写入数据，此时数据在外部流的缓冲区中 */
    bufferedOutputStream.write(arr2)

    /* 调用 flush 函数，真正将数据写入内部流中 */
    bufferedOutputStream.flush()
    println(String.fromUtf8(readToEnd(byteBuffer))) // 0123456789
}
```

## 字符串流

由于仓颉编程语言的输入流和输出流是基于字节数据来抽象的（拥有更好的性能），在部分以字符串为主的场景中使用起来不太友好，例如往文件里写入大量的文本内容时，需要将文本内容转换成字节数据，再写入文件。

为了提供友好的字符串操作能力，仓颉编程语言提供了 `StringReader` 和 `StringWriter` 来添加字符串处理能力。

使用 `StringReader` 和 `StringWriter` 类型需要导入 `io` 包：

导入 io 包示例：

<!-- run -->

```cangjie
import std.io.*
```

`StringReader` 提供了按行读、按筛选条件读的能力，相比将字节数据读出来再手动转换成字符串，具有更好的性能表现和易用性。

如果构造 `StringReader`，传入另一个输入流即可。

StringReader 使用示例：

<!-- run -->

```cangjie
import std.io.{ByteBuffer, StringReader}

main(): Unit {
    let arr1 = "012\n346789".toArray()
    let byteBuffer = ByteBuffer()
    byteBuffer.write(arr1)
    let stringReader = StringReader(byteBuffer)

    /* 读取一行数据 */
    let line = stringReader.readln()
    println(line ?? "error") // 012
}
```

`StringWriter` 提供了直接写字符串、按行直接写字符串的能力，相比将字节数据手动转换成字符串再写入，具有更好的性能表现和易用性。

如果构造 `StringWriter`，传入另一个输出流即可。

StringWriter 使用示例：

<!-- run -->

```cangjie
import std.io.{ByteBuffer, StringWriter, readToEnd}

main(): Unit {
    let byteBuffer = ByteBuffer()
    let stringWriter = StringWriter(byteBuffer)

    /* 写入字符串 */
    stringWriter.write("number")

    /* 写入字符串并自动转行 */
    stringWriter.writeln(" is:")

    /* 写入数字 */
    stringWriter.write(100.0f32)

    stringWriter.flush()

    println(String.fromUtf8(readToEnd(byteBuffer))) // number is:\n100.000000
}
```
