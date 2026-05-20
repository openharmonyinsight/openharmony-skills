---
name: cangjie-std-io
description: "仓颉 I/O 流使用说明。"
---

# 仓颉语言 I/O 流

## 1. I/O 流概述

### 1.1 核心接口
- 仓颉将所有 I/O 建模为**流**，最小数据单元为 `Byte`
- `InputStream`：`read(buffer: Array<Byte>): Int64`，返回实际读取字节数，0 表示流结束
- `OutputStream`：`write(buffer: Array<Byte>): Unit` 和 `flush()`（默认空实现）
- `IOStream`：同时实现 `InputStream & OutputStream`
- `Seekable`：随机访问，提供 `length`、`position`、`remainLength` 属性和 `seek(SeekPosition)` 方法
  - `SeekPosition` 枚举：`Begin(Int64)`、`Current(Int64)`、`End(Int64)`
  - 位置不能移到流起点之前（抛异常），但可以超过流末尾
- `Resource`：支持 `close()` 和 `isClosed()`，配合 `try-with-resource` 自动清理
- 导入：`import std.io.*`

### 1.2 流分类
- **源流**（节点流）：由外部资源支撑（文件/网络/内存）
- **处理流**（代理流）：代理其他流，添加缓冲/编码等能力

---

## 2. ByteBuffer — 内存字节流

- 实现 `IOStream & Seekable`，可同时读写的内存缓冲区
- 构造：`ByteBuffer()`（默认 32 字节）、`ByteBuffer(capacity)`、`ByteBuffer(Array<Byte>)`
- 关键属性：`capacity`、`length`（已写数据量）、`position`、`remainLength`
- 关键方法：
  - `bytes()`：获取未读数据切片（**注意**：修改 ByteBuffer 后切片失效）
  - `clear()`：清空数据但保留容量
  - `clone()`：深拷贝
  - `reserve(additional)`：扩容（取 1.5 倍或 additional+capacity 中较大值）

```cangjie
import std.io.*

main(): Unit {
    let buf = ByteBuffer()
    buf.write("test case".toArray())

    let arr = Array<Byte>(4, repeat: 0)
    buf.read(arr)
    println(String.fromUtf8(arr))  // "test"

    buf.seek(Begin(0))             // 回到起点
    let all = readToEnd(buf)
    println(String.fromUtf8(all))  // "test case"

    buf.seek(End(-4))              // 从末尾往前 4 字节
    println(readString(buf))       // "case"
}
```

---

## 3. 处理流

### 3.1 BufferedInputStream / BufferedOutputStream
- 用内部缓冲区（默认 4096 字节）包装另一个流，减少 I/O 频率
- 构造：传入流 + 可选 `capacity`，或传入自定义缓冲区复用
- `BufferedInputStream` 额外方法：`readByte(): ?Byte`（返回 `None` 表示流结束）
- `BufferedOutputStream` **必须**在写完后显式调用 `flush()`
- `reset(stream)` 可重新绑定到新流，不重置容量
- 实现 `Resource & Seekable`（当包装流支持时）

```cangjie
import std.io.*

main(): Unit {
    let source = ByteBuffer()
    source.write("0123456789".toArray())
    let bis = BufferedInputStream(source)
    let arr = Array<Byte>(20, repeat: 0)
    let n = bis.read(arr)
    println(String.fromUtf8(arr[..n]))  // "0123456789"

    let target = ByteBuffer()
    let bos = BufferedOutputStream(target)
    bos.write("hello".toArray())
    bos.flush()  // 必须 flush
    println(String.fromUtf8(readToEnd(target)))  // "hello"
}
```

### 3.2 StringReader / StringWriter
- 在字节流上添加 UTF-8 字符串读写能力，内部 4096 字节缓冲
- **StringReader** 方法：
  - `read(): ?Rune` — 读取单个字符
  - `readln(): ?String` — 按行读取（自动去除 `\n`、`\r`、`\r\n`）
  - `readToEnd(): String` — 读取全部剩余内容
  - `readUntil(predicate)` / `readUntil(Rune)` — 条件读取
  - `lines()` / `runes()` — 迭代器
  - 遇到无效 UTF-8 抛出 `ContentFormatException`
- **StringWriter** 方法：
  - `write(String)` / `writeln(String)` — 写入字符串
  - `write(数值类型)` — 支持 Bool/Int/UInt/Float 等所有数值类型
  - **必须**调用 `flush()` 刷新内部缓冲

```cangjie
import std.io.*

main(): Unit {
    let buf = ByteBuffer()
    buf.write("第一行\n第二行\n第三行".toArray())
    let reader = StringReader(buf)

    println(reader.readln() ?? "")     // "第一行"
    println(reader.readToEnd())        // "第二行\n第三行"

    let out = ByteBuffer()
    let writer = StringWriter(out)
    writer.write("count=")
    writer.writeln(42)
    writer.flush()
    println(String.fromUtf8(readToEnd(out)))  // "count=42\n"
}
```

### 3.3 ChainedInputStream — 链式读取
- 将多个 `InputStream` 串联，按顺序依次读取，前一个流耗尽自动切换到下一个
- 构造：`ChainedInputStream(Array<InputStream>)`（数组不可为空）

```cangjie
import std.io.*

main() {
    let s1 = ByteBuffer()
    s1.write("Hello ".toArray())
    let s2 = ByteBuffer()
    s2.write("World".toArray())
    let chained = ChainedInputStream([s1, s2])
    let buffer = Array<Byte>(256, repeat: 0)
    chained.read(buffer) // 从 s1 读取
    println(String.fromUtf8(buffer))  // "Hello"
    chained.read(buffer) // s1 耗尽，自动切换到 s2
    println(String.fromUtf8(buffer))  // "World"
}
```

### 3.4 MultiOutputStream — 多路写入
- 同时写入多个 `OutputStream`，`flush()` 刷新全部绑定流

```cangjie
import std.io.*

main(): Unit {
    let buf1 = ByteBuffer()
    let buf2 = ByteBuffer()
    let multi = MultiOutputStream([buf1, buf2])
    multi.write("broadcast".toArray())
    // buf1 和 buf2 都包含 "broadcast"
}
```

---

## 4. 流工具函数

| 函数 | 说明 |
|------|------|
| `copy(input, to: output): Int64` | 流到流数据拷贝，返回拷贝字节数 |
| `readToEnd<T>(stream): Array<Byte>` | 读取流中全部剩余数据为字节数组 |
| `readString<T>(stream): String` | 读取全部剩余数据为 UTF-8 字符串（无效编码抛异常） |
| `readStringUnchecked<T>(stream): String` | 同上但不校验 UTF-8 编码 |

```cangjie
import std.io.*

main(): Unit {
    let src = ByteBuffer(); src.write("Hello!".toArray())
    let dst = ByteBuffer()
    let n = copy(src, to: dst)
    println("Copied ${n} bytes")
    println(String.fromUtf8(readToEnd(dst)))  // "Hello!"
}
```

---

## 5. 标准流

- `getStdIn(): ConsoleReader` — 标准输入（来自 `std.env.*`）
- `getStdOut(): ConsoleWriter` / `getStdErr(): ConsoleWriter` — 标准输出/错误
- `ConsoleReader` / `ConsoleWriter` 是**并发安全**的
- `ConsoleWriter` 使用缓冲 — 调用 `flush()` 确保输出

---

## 6. 异常类型

| 异常 | 说明 |
|------|------|
| `IOException` | 通用 I/O 错误 |
| `ContentFormatException` | 无效 UTF-8 编码（`StringReader`/`readString` 抛出） |

---

## 7. 关键规则速查

1. 所有实现 `Resource` 的流使用 `try-with-resource` 自动清理
2. `BufferedOutputStream` 和 `StringWriter` **必须**显式调用 `flush()`
3. `ByteBuffer.bytes()` 返回的切片在 ByteBuffer 被修改后**失效**
4. `readByte()` 和 `StringReader.read()` 返回 Option 类型（`?Byte` / `?Rune`）
5. `Seekable.position` 不能移到流起点前（抛异常），但可超过末尾
