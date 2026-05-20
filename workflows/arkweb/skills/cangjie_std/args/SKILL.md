---
name: cangjie-std-args
description: "仓颉命令行参数处理用法。"
---

# 仓颉语言命令行参数处理 Skill

## 1. main 函数获取命令行参数

### 1.1 基本规则

- 仓颉的 `main` 函数可以接收一个 `Array<String>` 类型的参数，用于获取命令行参数
- 每个包只允许定义**一个** `main` 函数
- `main` 函数不能有访问修饰符
- 参数类型**必须**是 `Array<String>`，不支持其他类型
- 返回类型可以是 `Unit` 或整数类型（如 `Int64`）

### 1.2 有效的 main 函数签名

```cangjie
// 无参数
main(): Unit { }
main(): Int64 { return 0 }

// 带命令行参数
main(args: Array<String>): Unit { }
main(args: Array<String>): Int64 { return 0 }
```

### 1.3 使用示例

```cangjie
main(args: Array<String>): Unit {
    println("参数个数: ${args.size}")
    for (arg in args) {
        println(arg)
    }
}
```

运行：

```bash
$ cjc main.cj && ./main Hello World
参数个数: 2
Hello
World
```

> **注意**：`args` 不包含可执行文件名本身，只包含传递给程序的参数。

---

## 2. std.argopt — 命令行参数解析

**导入**：`import std.argopt.*`

`std.argopt` 包提供了结构化的命令行参数解析能力，支持短选项、长选项、组合选项、可选值和必选值，适合开发 CLI 工具。

### 2.1 核心 API

| 类型 / 函数 | 签名 | 说明 |
|-------------|------|------|
| `parseArguments` | `parseArguments(args: Array<String>, specs: Array<ArgumentSpec>): ParsedArguments` | 解析命令行参数 |
| `ParsedArguments` | `options: ReadOnlyMap<String, String>`, `nonOptions: Array<String>` | 解析结果 |
| `ArgumentParseException` | — | 解析失败时抛出的异常 |

### 2.2 参数规范（ArgumentSpec）

| 构造器 | 说明 |
|--------|------|
| `Short(Rune, ArgumentMode)` | 短选项（如 `-v`） |
| `Short(Rune, ArgumentMode, (String) -> Unit)` | 短选项 + 回调 |
| `Long(String, ArgumentMode)` | 长选项（如 `--verbose`） |
| `Long(String, ArgumentMode, (String) -> Unit)` | 长选项 + 回调 |
| `Full(String, Rune, ArgumentMode)` | 同时定义长短选项（如 `--output` / `-o`） |
| `Full(String, Rune, ArgumentMode, (String) -> Unit)` | 同时定义长短选项 + 回调 |
| `NonOptions((Array<String>) -> Unit)` | 非选项参数回调 |

### 2.3 参数模式（ArgumentMode）

| 模式 | 说明 | 长选项格式 | 短选项格式 |
|------|------|-----------|-----------|
| `NoValue` | 不接受值（开关标志） | `--flag` | `-f` |
| `RequiredValue` | 必须提供值 | `--name=value` 或 `--name value` | `-n value` 或 `-nvalue` |
| `OptionalValue` | 值可选 | `--name=value` 或 `--name` | `-nvalue` 或 `-n` |

### 2.4 特殊规则

- `--`（双横线）终止选项扫描，其后所有参数都被视为非选项
- 短选项可以组合：如 `-abc` 等价于 `-a -b -c`（当 a、b、c 均为 `NoValue` 时）
- 组合短选项中遇到非 `NoValue` 选项时，剩余部分作为该选项的值
- 如果组合短选项字面值与某个长选项名相同，优先作为长选项解析
- 同一选项多次赋值时，以最后一次的值为准

---

## 3. CLI 工具开发实战

### 3.1 基本参数解析（不带回调）

```cangjie
import std.argopt.*

main(args: Array<String>): Unit {
    let specs = [
        Short(r'v', NoValue),                     // -v 开关
        Long("output", RequiredValue),             // --output <file>
        Full("help", r'h', NoValue)                // --help 或 -h
    ]

    try {
        let result = parseArguments(args, specs)

        // 检查开关选项
        if (result.options.contains("help") || result.options.contains('h')) {
            println("Usage: mytool [-v] [--output <file>] <input>...")
            return
        }

        let verbose = result.options.contains('v')
        let output = result.options.get("output")  // ?String

        if (verbose) {
            println("Verbose mode enabled")
        }

        if (let Some(outFile) <- output) {
            println("Output file: ${outFile}")
        }

        // 非选项参数（如输入文件列表）
        println("Input files: ${result.nonOptions}")
    } catch (e: ArgumentParseException) {
        println("Error: ${e}")
        println("Usage: mytool [-v] [--output <file>] <input>...")
    }
}
```

运行：

```bash
$ ./mytool -v --output result.txt file1.txt file2.txt
Verbose mode enabled
Output file: result.txt
Input files: [file1.txt, file2.txt]

$ ./mytool --help
Usage: mytool [-v] [--output <file>] <input>...
```

### 3.2 带回调的参数解析

回调方式适合在解析时立即处理每个参数。注意：回调 lambda 中不能捕获外部 `var` 变量（仓颉语言限制），可通过 `parseArguments` 返回的结果获取选项值：

```cangjie
import std.argopt.*

main(args: Array<String>): Unit {
    let specs = [
        Short(r'v', NoValue),
        Long("output", RequiredValue),
        Full("config", r'c', RequiredValue) { v =>
            println("Loading config: ${v}")
        },
    ]

    try {
        let result = parseArguments(args, specs)
        let verbose = result.options.contains('v')
        let output = result.options.get("output") ?? ""

        println("Verbose: ${verbose}, Output: ${output}")
        println("Inputs: ${result.nonOptions}")
    } catch (e: ArgumentParseException) {
        println("Error: ${e}")
    }
}
```

### 3.3 完整 CLI 工具示例

```cangjie
import std.argopt.*
import std.fs.*
import std.io.*
import std.env.*

main(args: Array<String>): Unit {
    let specs = [
        Full("help", r'h', NoValue),
        Full("version", r'V', NoValue),
        Full("output", r'o', RequiredValue),
        Full("format", r'f', RequiredValue),
    ]

    var result: ParsedArguments
    try {
        result = parseArguments(args, specs)
    } catch (e: ArgumentParseException) {
        eprintln("Error: ${e}")
        eprintln("Try '--help' for more information.")
        exit(1)
    }

    let showHelp = result.options.contains("help") || result.options.contains('h')
    let showVersion = result.options.contains("version") || result.options.contains('V')
    let outputPath = result.options.get("output") ?? ""
    let format = result.options.get("format") ?? "text"
    let inputFiles = result.nonOptions

    if (showVersion) {
        println("mytool 1.0.0")
        return
    }

    if (showHelp || inputFiles.isEmpty()) {
        println("Usage: mytool [OPTIONS] <files>...")
        println("")
        println("Options:")
        println("  -h, --help              Show help message")
        println("  -V, --version           Show version")
        println("  -o, --output <file>     Output file (default: stdout)")
        println("  -f, --format <fmt>      Output format: text|json (default: text)")
        return
    }

    // 处理输入文件
    for (file in inputFiles) {
        if (!exists(file)) {
            eprintln("Error: file not found: ${file}")
            continue
        }
        let content = File.readFrom(file)
        println("Processing: ${file} (${content.size} bytes)")
    }
}
```

运行：

```bash
$ ./mytool --version
mytool 1.0.0

$ ./mytool -o out.json -f json input.txt
Processing: input.txt (1024 bytes)

$ ./mytool --help
Usage: mytool [OPTIONS] <files>...

Options:
  -h, --help              Show help message
  -V, --version           Show version
  -o, --output <file>     Output file (default: stdout)
  -f, --format <fmt>      Output format: text|json (default: text)
```

---

## 4. 快速参考

| 需求 | 做法 |
|------|------|
| 获取原始命令行参数 | `main(args: Array<String>)` |
| 解析结构化选项 | `import std.argopt.*` + `parseArguments()` |
| 定义开关标志（如 `-v`） | `Short(r'v', NoValue)` |
| 定义必选值选项（如 `--output file`） | `Long("output", RequiredValue)` |
| 同时支持长短选项（如 `-o` / `--output`） | `Full("output", r'o', RequiredValue)` |
| 获取非选项参数（如文件列表） | `result.nonOptions` 或 `NonOptions { files => ... }` |
| 处理解析错误 | `try { ... } catch (e: ArgumentParseException) { ... }` |
| 终止选项扫描 | 命令行中使用 `--`，之后的参数都视为非选项 |
