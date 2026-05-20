---
name: cangjie-std-stdio
description: "仓颉标准输入输出用法。"
---

# 仓颉语言标准输入输出

## 1. 最基本的输入输出

仓颉语言提供了开箱即用的标准输入输出函数，最常用的是 `println` 和 `readln`。

### 1.1 println — 输出一行文本

`println` 是 `std.core` 包中的内置函数，**无需导入**即可直接使用，输出字符串并自动换行。

```cangjie
main() {
    println("你好，仓颉！")
    println("1 + 2 = ${1 + 2}")
}
```

运行结果：

```text
你好，仓颉！
1 + 2 = 3
```

### 1.2 readln — 读取一行输入

`readln` 同样是 `std.core` 包中的内置函数，**无需导入**即可直接使用。它从控制台读取一行文本，直到遇到换行或 EOF 结束，返回类型为 `String`。

```cangjie
main() {
    print("请输入你的名字：")
    let name = readln()
    println("你好，${name}！")
}
```

运行结果：

```text
请输入你的名字：仓颉
你好，仓颉！
```

---

## 2. 标准输入输出函数

以下函数来自 `std.core` 包，**无需导入**。

| 函数 | 签名 | 说明 |
|------|------|------|
| `readln` | `readln(): String` | 从控制台读取一行文本 |
| `print` | `print(str: String, flush!: Bool = false): Unit` | 输出字符串，不换行 |
| `println` | `println(str: String): Unit` | 输出字符串并换行 |
| `eprint` | `eprint(str: String, flush!: Bool = true): Unit` | 输出到标准错误流，不换行 |
| `eprintln` | `eprintln(str: String): Unit` | 输出到标准错误流并换行 |

- `print` 和 `println` 输出到标准输出（stdout）
- `eprint` 和 `eprintln` 输出到标准错误（stderr），适用于错误信息和调试日志
- `print` 的 `flush!` 参数默认为 `false`；`eprint` 的 `flush!` 参数默认为 `true`

```cangjie
main() {
    print("姓名：")         // 不换行
    println("仓颉")         // 换行
    eprintln("这是一条错误信息") // 输出到 stderr
}
```

---

## 3. 标准流获取

通过 `std.env` 包提供的函数获取标准输入/输出/错误流对象，需要 `import std.env.*`。

| 函数 | 返回类型 | 说明 |
|------|---------|------|
| `getStdIn()` | `ConsoleReader` | 获取标准输入流 |
| `getStdOut()` | `ConsoleWriter` | 获取标准输出流 |
| `getStdErr()` | `ConsoleWriter` | 获取标准错误流 |

```cangjie
import std.env.*

main() {
    let stdin = getStdIn()
    let stdout = getStdOut()
    let stderr = getStdErr()

    stdout.write("请输入信息：")
    let input = stdin.readln() ?? ""
    stdout.writeln("你输入了：" + input)
    stderr.writeln("程序执行完毕")
}
```

---

## 4. ConsoleReader — 标准输入读取

`ConsoleReader` 实现了 `InputStream` 接口，通过 `getStdIn()` 获取实例。读操作是同步的，内部设有缓冲区，所有方法共享同一个缓冲区。`ConsoleReader` 是**并发安全**的。

### 4.1 方法一览

| 方法 | 签名 | 说明 |
|------|------|------|
| `read()` | `read(): ?Rune` | 读取单个字符，返回 `?Rune` |
| `read(Array<Byte>)` | `read(arr: Array<Byte>): Int64` | 读取字节到数组，返回字节数 |
| `readln()` | `readln(): ?String` | 读取一行，结果不含换行符 |
| `readToEnd()` | `readToEnd(): ?String` | 读取全部输入直到 EOF |
| `readUntil(Rune)` | `readUntil(ch: Rune): ?String` | 读取直到遇到指定字符（包含该字符） |
| `readUntil((Rune) -> Bool)` | `readUntil(predicate: (Rune) -> Bool): ?String` | 读取直到满足条件（包含满足条件的字符） |

### 4.2 返回 None 的情形

- 将标准输入重定向到文件时，读取到文件结尾 EOF
- Linux 环境按下 `Ctrl+D`
- Windows 环境按下 `Ctrl+Z` 后加回车

### 4.3 示例

```cangjie
import std.env.*

main() {
    // 读取一行
    getStdOut().write("请输入一行文本：")
    let line = getStdIn().readln()
    println(line.getOrThrow())

    // 读取单个字符
    getStdOut().write("请输入一个字符：")
    let ch = getStdIn().read()
    println(ch.getOrThrow())

    // 读取直到指定字符
    getStdOut().write("请输入文本（遇到 # 停止）：")
    let text = getStdIn().readUntil(r'#')
    println(text.getOrThrow())
}
```

---

## 5. ConsoleWriter — 标准输出写入

`ConsoleWriter` 实现了 `OutputStream` 接口，通过 `getStdOut()` 或 `getStdErr()` 获取实例。`ConsoleWriter` 是**并发安全**的，使用内部缓冲，必要时调用 `flush()` 确保输出。

### 5.1 方法一览

| 方法 | 说明 |
|------|------|
| `write(String)` | 写入字符串，不换行 |
| `writeln(String)` | 写入字符串并换行 |
| `write(Bool/Int/UInt/Float/Rune)` | 写入各种基本类型的文本表示 |
| `writeln(Bool/Int/UInt/Float/Rune)` | 写入各种基本类型的文本表示并换行 |
| `write<T>(T) where T <: ToString` | 写入任意实现 `ToString` 接口的类型 |
| `writeln<T>(T) where T <: ToString` | 写入任意实现 `ToString` 接口的类型并换行 |
| `write(Array<Byte>)` | 写入字节数组 |
| `writeln(Array<Byte>)` | 写入字节数组并换行 |
| `flush()` | 刷新输出缓冲区 |

### 5.2 示例

```cangjie
import std.env.*

main() {
    let out = getStdOut()
    out.write("数量：")
    out.writeln(42)
    out.write("比例：")
    out.writeln(3.14)
    out.write("结果：")
    out.writeln(true)
    out.flush()
}
```

运行结果：

```text
数量：42
比例：3.140000
结果：true
```

---

## 6. 综合示例

### 6.1 交互式输入输出

```cangjie
import std.convert.*

main() {
    print("请输入你的年龄：")
    let input = readln()
    let age = Int64.parse(input)
    if (age >= 18) {
        println("你已成年，年龄：${age}")
    } else {
        println("你未成年，年龄：${age}")
    }
}
```

### 6.2 逐行读取处理

```cangjie
import std.env.*

main() {
    println("请输入多行文本（Ctrl+D 结束）：")
    var line = getStdIn().readln()
    while (line != None) {
        println(">>> ${line.getOrThrow()}")
        line = getStdIn().readln()
    }
    println("输入结束")
}
```

---

## 7. 关键规则速查

1. `readln`/`print`/`println`/`eprint`/`eprintln` 属于 `std.core`，**无需导入**即可使用
2. 内置 `readln()` 返回 `String`，是最简单的读取一行输入方式
3. `getStdIn()`/`getStdOut()`/`getStdErr()` 来自 `std.env`，需要 `import std.env.*`
4. `ConsoleReader.readln()` 返回 `?String`（Option 类型），使用前需解包（`getOrThrow()` 或 `??` 默认值）
5. `ConsoleReader.read()` 返回 `?Rune`（Option 类型），同样需要解包
6. `ConsoleReader` 和 `ConsoleWriter` 均为**并发安全**的
7. `ConsoleWriter` 使用缓冲，必要时调用 `flush()` 确保数据输出
8. 旧版 `std.console` 包中的 `Console.stdIn`/`Console.stdOut`/`Console.stdErr` 已废弃，请使用 `std.env` 中的 `getStdIn()`/`getStdOut()`/`getStdErr()` 替代
9. 更底层的 I/O 流操作详见 `cangjie-iostream` Skill
