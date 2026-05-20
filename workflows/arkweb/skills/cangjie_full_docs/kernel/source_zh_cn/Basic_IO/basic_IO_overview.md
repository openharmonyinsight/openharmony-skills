# I/O 流概述

本章介绍基本的 I/O 概念和文件操作。

仓颉编程语言将与应用程序外部载体交互的操作称为 I/O 操作。I 对应输入（Input），O 对应输出（Output）。

仓颉编程语言所有的 I/O 机制都是基于数据流进行输入输出，这些数据流表示了字节数据的序列。数据流是一串连续的数据集合，它就像承载数据的管道，在管道的一端输入数据，在管道的另一端就可以输出数据。

仓颉编程语言将输入输出抽象为流（Stream）。

- 将数据从外存中读取到内存中的称为输入流（InputStream），输入端可以一段一段地向管道中写入数据，这些数据段会按先后顺序形成一个长的数据流。
- 将数据从内存写入外存中的称为输出流（OutputStream），输出端也可以一段一段地从管道中读出数据，每次可以读取其中的任意长度的数据（不需要跟输入端匹配），但只能读取先输入的数据，再读取后输入的数据。

有了这一层抽象，仓颉编程语言就可以使用统一的接口来实现与外部数据的交互。

仓颉编程语言将标准输入输出、文件操作、网络数据流、字符串流、加密流、压缩流等形式的操作，统一用 Stream 描述。

Stream 主要面向处理原始二进制数据，Stream 中最小的数据单元是 `Byte`。

仓颉编程语言将 Stream 定义成了 `interface`，它让不同的 Stream 可以用装饰器模式进行组合，极大地提升了可扩展性。

## 输入流

程序从输入流读取数据源（数据源包括外界的键盘、文件、网络等），即输入流是将数据源读入到程序的通信通道。

仓颉编程语言用 `InputStream` 接口类型来表示输入流，它提供了 `read` 函数，这个函数会将可读的数据写入到 `buffer` 中，返回值表示了该次读取的字节总数。

InputStream 接口定义：

<!-- run -->

```cangjie
interface InputStream {
    func read(buffer: Array<Byte>): Int64
}
```

当拥有一个输入流的时候，就可以像下面的代码那样去读取字节数据，读取的数据会被写到 `read` 的入参数组中。

输入流读取示例：

```cangjie
import std.io.InputStream

main() {
    let input: InputStream = ...
    let buf = Array<Byte>(256, repeat: 0)
    while (input.read(buf) > 0) {
        println(buf)
    }
}
```

## 输出流

程序向输出流写入数据。输出流是将程序中的数据输出到外界（显示器、打印机、文件、网络等）的通信通道。

仓颉编程语言用 `OutputStream` 接口类型来表示输出流，它提供了 `write` 函数，这个函数会将 `buffer` 中的数据写入到绑定的流中。

特别的，有一些输出流的 `write` 不会立即写到外存中，而是有一定的缓冲策略，只有当符合条件或主动调用 `flush` 时才会真实写入，目的是提高性能。

为了统一处理这些 `flush` 操作，在 `OutputStream` 中有一个 `flush` 的默认实现，它有助于抹平 API 调用的差异性。

OutputStream 接口定义：

```cangjie
interface OutputStream {
    func write(buffer: Array<Byte>): Unit

    func flush(): Unit {
        // 空实现
    }
}
```

当拥有一个输出流时，可以写入字节数据。

输出流写入示例：

```cangjie
import std.io.OutputStream

main() {
    let output: OutputStream = ...
    let buf = Array<Byte>(256, repeat: 111)
    output.write(buf)
    output.flush()
}
```

## 数据流分类

按照数据流职责上的差异，可以将 Stream 简单分成两类：

- 节点流：直接提供数据源，节点流的构造方式通常是依赖某种直接的外部资源（如文件、网络等）。
- 处理流：只能代理其他数据流进行处理，处理流的构造方式通常是依赖其他的流。
