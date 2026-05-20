# BufferedOutputStream 示例

下面是 BufferedOutputStream 向流中写入数据示例。
<!-- verify -->

```cangjie
import std.io.*

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
    println(String.fromUtf8(readToEnd(byteBuffer)))
}
```

运行结果：

```text
0123456789
```
