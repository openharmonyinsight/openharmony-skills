# StringWriter 示例

下面是 StringWriter 向流中写入数据示例。
<!-- verify -->

```cangjie
import std.io.*

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

    println(String.fromUtf8(readToEnd(byteBuffer)))
}
```

运行结果：

```text
number is:
100.000000
```
