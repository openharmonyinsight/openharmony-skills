# I/O 节点流

节点流是指直接提供数据源的流，节点流的构造方式通常是依赖某种直接的外部资源（如文件、网络等）。

仓颉编程语言中常见的节点流包含标准流（ConsoleReader、ConsoleWriter）、文件流（File）、网络流（Socket）等。

本章介绍标准流和文件流。

## 标准流

标准流包含标准输入流、标准输出流和标准错误输出流。

标准流是程序与外部数据交互的标准接口。程序运行的时候从输入流读取数据，作为程序的输入，程序运行过程中输出的信息被传送到输出流，类似的，错误信息被传送到错误流。

在仓颉编程语言中可以使用 `getStdIn`、`getStdOut`、`getStdErr` 全局函数来分别获取这三个标准流。

使用上面的函数需要导入 `env` 包：

导入 env 包示例：

<!-- run -->

```cangjie
import std.env.*
```

`env` 包内的 `ConsoleReader` 和 `ConsoleWriter` 类型对这三个标准流都进行了易用性封装（标准错误输出流也是输出流，所以一共是两个类型），提供了更方便的基于 `String` 的扩展操作，并且对于很多常见类型都提供了丰富的重载来优化性能。

其中最重要的是 `ConsoleReader` 和 `ConsoleWriter` 类型提供了并发安全的保证，可以在任意线程中安全地通过该类型提供的接口来读写内容。

默认情况下标准输入流来源于键盘输入的信息，例如在命令行界面中输入的文本。

当需要从标准输入流中获取数据时，可以通过 `getStdIn` 全局函数获取 `ConsoleReader` 类型，再通过该类型的 `readln` 函数获取命令行的输入。

标准输入流读取示例：

<!-- run -->

```cangjie
import std.env.getStdIn

main() {
    let consoleReader = getStdIn()
    let txt = consoleReader.readln()
    println(txt ?? "")
}
```

运行上面的代码，在命令行上输入一些文字，然后换行结束，即可看到输入的内容。

输出流分为标准输出流和标准错误流，默认情况下，它们都会输出到屏幕，例如在命令行界面中看到的文本。

当需要往标准输出流中写入数据时，可以通过 `getStdOut`/`getStdErr` 全局函数获取 `ConsoleWriter` 来写入，例如通过 `write` 函数来向控制台打印内容。

使用 `ConsoleWriter` 和直接使用 `print` 函数的差别是，`ConsoleWriter` 是并发安全的，并且由于 `ConsoleWriter` 使用了缓存技术，在输入内容较多时拥有更好的性能表现。

需要注意的是，写完数据后需要对 `ConsoleWriter` 调用 `flush` 才能保证内容被完整写到标准流中。

标准输出流写入示例：

<!-- run -->

```cangjie
import std.env.getStdOut

main() {
    let consoleWriter = getStdOut()
    for (_ in 0..1000) {
        consoleWriter.writeln("hello, world!")
    }
    consoleWriter.flush()
}
```

## 文件流

仓颉编程语言提供了 `fs` 包来支持通用文件系统任务。不同的操作系统对于文件系统提供的接口有所不同。仓颉编程语言抽象出以下一些共通的功能，通过统一的功能接口，屏蔽不同操作系统之间的差异，来简化使用。

常规操作任务包括：创建文件/目录、读写文件、重命名或移动文件/目录、删除文件/目录、复制文件/目录、获取文件/目录元数据、检查文件/目录是否存在。具体 API 可以查阅库文档。

使用文件系统相关的功能需要导入 `fs` 包：

导入 fs 包示例：

<!-- run -->

```cangjie
import std.fs.*
```

本章会着重介绍 `File` 相关的使用，对于 `Path` 和 `Directory` 的使用可以查阅对应的 API 文档。

`File` 类型在仓颉编程语言中同时提供了常规文件操作和文件流两类功能。

### 常规文件操作

对于常规的文件操作，可以使用一系列静态函数来完成快捷的操作。

例如如果要检查某个路径对应的文件是否存在，可以使用 `exists` 函数。当 `exists` 函数返回 `true` 时表示文件存在，反之不存在。

exists 函数使用示例：

<!-- run -->

```cangjie
import std.fs.exists

main() {
    let exist = exists("./tempFile.txt")
    println("exist: ${exist}")
}
```

移动文件、拷贝文件和删除文件也非常简单，`File` 同样提供了对应的静态函数 `move`、`copy`、`delete`。

move、copy、delete 函数使用示例：

<!-- compile -->

```cangjie
import std.fs.{copy, rename, remove}

main() {
    copy("./tempFile.txt", to: "./tempFile2.txt", overwrite: false)
    rename("./tempFile2.txt",  to: "./tempFile3.txt", overwrite: false)
    remove("./tempFile3.txt")
}
```

如果需要直接将文件的所有数据读出来，或者一次性将数据写入文件里，可以使用 `File` 提供的 `readFrom`、`writeTo` 函数直接读写文件。在数据量较少的情况下它们既简单易用又能提供较好的性能表现，无需手动处理数据流。

readFrom、writeTo 函数使用示例：

<!-- compile -->

```cangjie
import std.fs.File

main() {
    let bytes = File.readFrom("./tempFile.txt") // 一次性读取了所有的数据
    File.writeTo("./otherFile.txt", bytes) // 把数据一次性写入另一个文件中
}
```

### 文件流操作

除了上述的常规文件操作之外，`File` 类型也被设计为一种数据流类型，因此 `File` 类型本身实现了 `IOStream` 接口。当创建了一个 `File` 的实例，可以把这个实例当成数据流来使用。

File 类定义：

```cangjie
public class File <: Resource & IOStream & Seekable {
    ...
}
```

`File` 提供了两种构造方式，一种是通过方便的静态函数 `create` 直接创建新文件的实例，另一种是通过构造函数传入完整的打开文件模式来构造新实例。

其中 `create` 创建的文件是只写的，不能对实例进行读操作，否则会抛出运行时异常。

File 构造示例：

<!-- compile -->

```cangjie
// 创建
internal import std.fs.*
internal import std.io.*

main() {
    let file = File.create("./tempFile.txt")
    file.write("hello, world!".toArray())

    // 打开
    let file2 = File("./tempFile.txt", Read)
    let bytes = readToEnd(file2) // 读取所有数据
    println(bytes)
}
```

当需要更精细的打开模式时，可以使用构造函数传入一个 `OpenMode` 值。`OpenMode` 是一个 `enum` 类型，它提供了丰富的文件打开模式，包含 `Read`、`Write`、`Append` 和 `ReadWrite` 模式。

File 打开模式使用示例：

```cangjie
// 使用指定选项打开模式
let file = File("./tempFile.txt", Write)
```

因为打开 `File` 的实例会占用宝贵的系统资源，所以使用完 `File` 的实例之后需要注意及时关闭 `File`，以释放系统资源。

`File` 实现了 `Resource` 接口，在大多数时候都可以使用 try-with-resource 语法来简化使用。

try-with-resource 语法使用示例：

```cangjie
try (file2 = File("./tempFile.txt", Read)) {
    ...
    // 结束使用后自动释放文件
}
```
