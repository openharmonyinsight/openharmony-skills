# StringReader 示例

下面是 StringReader 从流中读取数据示例。
<!-- verify -->

```cangjie
import std.io.*

main(): Unit {
    let arr1 = "012\n346789".toArray()
    let byteBuffer = ByteBuffer()
    byteBuffer.write(arr1)
    let stringReader = StringReader(byteBuffer)

    /* 读取一个字节 */
    let ch = stringReader.read()
    println(ch ?? 'a')

    /* 读取一行数据 */
    let line = stringReader.readln()
    println(line ?? "error")

    /* 读取数据直到遇到字符6 */
    let until = stringReader.readUntil(r'6')
    println(until ?? "error")

    /* 读取全部数据 */
    let all = stringReader.readToEnd()
    println(all)
}
```

运行结果：

```text
0
12
346
789
```
