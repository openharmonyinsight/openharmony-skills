# File 示例

## File 常规操作：创建、删除、读写、关闭

代码如下：
<!-- verify -->

```cangjie
import std.fs.*
import std.io.*

main() {
    let filePath: Path = Path("./tempFile.txt")
    if (exists(filePath)) {
        remove(filePath)
    }

    /* 在当前目录以 只写模式 创建新文件 'tempFile.txt'，写入三遍 "123456789\n" 并关闭文件 */
    var file: File = File(filePath, Write)
    if (exists(filePath)) {
        println("The file 'tempFile.txt' is created successfully in current directory.\n")
    }
    let bytes: Array<Byte> = "123456789\n".toArray()
    for (_ in 0..3) {
        file.write(bytes)
    }
    file.close()

    /* 以 追加模式 打开文件 './tempFile.txt'，写入 "abcdefghi\n" 并关闭文件 */
    file = File(filePath, Append)
    file.write("abcdefghi\n".toArray())
    file.close()

    /* 以 只读模式 打开文件 './tempFile.txt'，按要求读出数据并关闭文件 */
    file = File(filePath, Read)
    let bytesBuf: Array<Byte> = Array<Byte>(10, repeat: 0)
    // 从文件头开始的第 10 个字节后开始读出 10 个字节的数据
    file.seek(SeekPosition.Begin(10))
    file.read(bytesBuf)
    println("Data of the 10th byte after the 10th byte: ${String.fromUtf8(bytesBuf)}")
    // 读出文件尾的 10 个字节的数据
    file.seek(SeekPosition.End(-10))
    file.read(bytesBuf)
    println("Data of the last 10 bytes: ${String.fromUtf8(bytesBuf)}")
    file.close()

    /* 以 读+写模式 打开文件 './tempFile.txt'，按要求进行操作后关闭文件 */
    file = File(filePath, ReadWrite)
    // 截断文件大小为 0
    file.setLength(0)
    // 向文件中写入新内容
    file.write("The file was truncated to an empty file!".toArray())
    // 重置游标到文件头
    file.seek(SeekPosition.Begin(0))
    // 读取文件内容
    let allBytes: Array<Byte> = readToEnd(file)
    // 关闭文件
    file.close()
    println("Data written newly: ${String.fromUtf8(allBytes)}")

    remove(filePath)
    return 0
}
```

运行结果：

```text
The file 'tempFile.txt' is created successfully in current directory.

Data of the 10th byte after the 10th byte: 123456789

Data of the last 10 bytes: abcdefghi

Data written newly: The file was truncated to an empty file!
```

## File 的一些 static 函数演示

代码如下：
<!-- verify -->

```cangjie
import std.fs.*

main() {
    let filePath: Path = Path("./tempFile.txt")
    if (exists(filePath)) {
        remove(filePath)
    }

    /* 以 只写模式 创建文件，并写入 "123456789\n" 并关闭文件 */
    var file: File = File.create(filePath)
    file.write("123456789\n".toArray())
    file.close()

    /* 以 追加模式 写入 "abcdefghi\n" 到文件 */
    File.appendTo(filePath, "abcdefghi".toArray())

    /* 直接读取文件中所有数据 */
    let allBytes: Array<Byte> = File.readFrom(filePath)
    println(String.fromUtf8(allBytes))

    remove(filePath)
    return 0
}
```

运行结果：

```text
123456789
abcdefghi
```
