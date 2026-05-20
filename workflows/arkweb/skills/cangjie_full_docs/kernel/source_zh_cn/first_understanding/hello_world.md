# 运行第一个仓颉程序

万事俱备，开始编写和运行第一个仓颉程序吧！

## 使用 cjc 编译

首先，请在适当目录下新建一个名为 `hello.cj` 的文本文件，并向文件中写入以下仓颉代码：

<!-- verify -->

```cangjie
// hello.cj
main() {
    println("你好，仓颉")
}
```

在这段代码中，使用了仓颉的注释语法，可以在 `//` 符号之后写单行注释，也可以在一对 `/*` 和 `*/` 符号之间写多行注释，这与 C/C++ 等语言的注释语法相同。注释内容不影响程序的编译和运行。

然后，请在此目录下执行如下命令：

```bash
cjc hello.cj -o hello
```

这里仓颉编译器会将 `hello.cj` 中的源代码编译为此平台上的可执行文件 `hello`，在命令行环境中运行此文件，将看到程序输出了如下内容：

```text
你好，仓颉
```

> **注意：**
>
> 以上编译命令是针对 Linux 和 macOS 平台的，如果使用 Windows 平台，只需要将编译命令改为 `cjc hello.cj -o hello.exe` 即可。

## 使用 cjpm 编译运行

除了直接调用 `cjc` 编译器外，您还可以使用仓颉项目管理工具 `cjpm` (Cangjie Project Manager) 来快速创建、管理和运行仓颉项目。

请按照以下步骤创建第一个仓颉项目：

1. 创建一个新的目录 `hello_cjpm` 用于存放项目文件，并进入该目录。

2. 使用 `cjpm init` 命令初始化一个新的仓颉模块。

```bash
cjpm init
```

执行成功后，命令行会提示 `cjpm init success`。此时，`cjpm` 会在当前目录下生成默认的项目结构：

```text
hello_cjpm
├── cjpm.toml // 项目的配置文件
└── src
    └── main.cj // 默认生成的源码文件
```

其中默认生成的源码文件 `main.cj`，其内容如下：

<!-- verify -->

```cangjie
// main.cj
package hello_cjpm  // 声明当前源文件属于 hello_cjpm 包

main(): Int64 {
    println("hello world")
    return 0
}
```

此外执行 `cjpm init --path hello_cjpm`，`cjpm` 会自动创建 `hello_cjpm` 文件夹并在其中完成初始化。

在项目根目录下（即 `cjpm.toml` 所在目录），直接执行以下命令即可编译并运行程序：

```bash
cjpm run
```

`cjpm` 会自动处理依赖检查、编译构建以及运行可执行文件的全过程。命令行将显示如下输出：

```text
hello world

cjpm run finished
```
