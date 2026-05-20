# ChainedInputStream 示例

下面是 ChainedInputStream 从绑定的流中循环读取数据示例。
<!-- verify -->

```cangjie
import std.io.*
import std.collection.ArrayList

main(): Unit {
    const size = 2

    /* 创建两个 ByteBuffer 并写入数据 */
    let streamArr = Array<InputStream>(size, {_ => ByteBuffer()})
    for (i in 0..size) {
        match (streamArr[i]) {
            case v: OutputStream =>
                let str = "now ${i}"
                v.write(str.toArray())
            case _ => throw Exception()
        }
    }

    /* 将两个 ByteBuffer 绑定到 ChainedInputStream */
    let chainedInputStream = ChainedInputStream(streamArr)
    let res = ArrayList<Byte>()
    let buffer = Array<Byte>(20, repeat: 0)
    var readLen = chainedInputStream.read(buffer)

    /* 循环读取 chainedInputStream 中数据 */
    while (readLen != 0) {
        res.add(all: buffer[..readLen])
        readLen = chainedInputStream.read(buffer)
    }
    println(String.fromUtf8(res.toArray()))
}
```

运行结果：

```text
now 0now 1
```
