# ByteBuffer 示例

下面是 ByteBuffer 对流进行写入数据，读取数据等操作的示例。
<!-- verify -->

```cangjie
import std.io.*

main(): Unit {
    let arr1 = "test case".toArray()
    let byteBuffer = ByteBuffer()

    /* 将 arr1 中的数据写入到流中 */
    byteBuffer.write(arr1)

    /* 读取前 4 个字节的数据到 arr2 中 */
    let arr2 = Array<Byte>(4, repeat: 0)
    byteBuffer.read(arr2)
    println(String.fromUtf8(arr2))

    /* 将流的索引指向起点 */
    byteBuffer.seek(Begin(0))

    /* 读取流中全部数据 */
    let arr3 = readToEnd(byteBuffer)
    println(String.fromUtf8(arr3))

    /* 将流的索引指向字母 'c' 的位置 */
    byteBuffer.seek(End(-4))

    /* 读取流中剩余数据 */
    let str = readString(byteBuffer)
    println(str)
}
```

运行结果：

```text
test
test case
case
```
