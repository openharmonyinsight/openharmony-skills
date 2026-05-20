# `cjc` 编译选项

本章介绍常用的 `cjc` 编译选项。若某一选项同时适用于 `cjc-frontend`，则该选项会有 <sup>[frontend]</sup> 上标；若该选项在 `cjc-frontend` 下行为与 `cjc` 不同，选项会有额外说明。

- 两个横杠开头的选项为长选项，如 `--xxxx`。
  如果长选项有可选参数，那么选项和参数之间需要用等号连接，如 `--xxxx=<value>`。
  如果长选项有必选参数，那么选项和参数之间既可以用空格隔开，也可以用等号连接，如 `--xxxx <value>` 与 `--xxxx=<value>` 等价。

- 一个横杠开头的选项为短选项，如 `-x`。
  对于短选项，如果其后有参数，选项和参数之间可以用空格隔开，也可以不隔开，如 `-x <value>` 与 `-x<value>` 等价。

## 基本选项

### `--output-type=[exe|staticlib|dylib]` <sup>[frontend]</sup>

指定输出文件的类型。`exe` 模式下会生成可执行文件，`staticlib` 模式下会生成静态库文件（ `.a` 文件），`dylib` 模式下会生成动态库文件（Linux 平台为 `.so` 文件、Windows 平台为 `.dll` 文件，macOS 平台为 `.dylib` 文件）。

`cjc` 默认为 `exe` 模式。

除了可以将 `.cj` 文件编译成一个可执行文件以外，也可以将其编译成一个静态或者是动态的链接库，例如使用：

```shell
$ cjc tool.cj --output-type=dylib
```

可以将 `tool.cj` 编译成一个动态链接库，在 Linux 平台上，`cjc` 会生成一个名为 `libtool.so` 的动态链接库文件。

**值得注意的是**，若编译可执行程序时链接了仓颉的动态库文件，必须同时指定 `--dy-std` 与 `--dy-libs` 选项，详情请见 [`--dy-std` 选项说明](#--dy-std)。

<sup>[frontend]</sup> 在 `cjc-frontend` 中，编译流程仅进行至 `LLVM IR`，因此输出总是 `.bc` 文件，但不同的 `--output-type` 类型仍会影响前端编译的策略。

### `--package`, `-p` <sup>[frontend]</sup>

编译包，使用此选项时需要指定一个目录作为输入，目录中的源码文件需要属于同一个包。

假设有文件 `log/printer.cj`：

```cangjie
package log

public func printLog(message: String) {
    println("[Log]: ${message}")
}
```

与文件 `main.cj`:

```cangjie
import log.*

main() {
    printLog("Everything is great")
}
```

可以使用

```shell
$ cjc -p log --output-type=staticlib
```

来编译 `log` 包，`cjc` 会在当前目录下生成一个 `liblog.a` 文件。

可以使用 `liblog.a` 文件来编译 `main.cj` ，编译命令如下：

```shell
$ cjc main.cj liblog.a
```

`cjc` 会将 `main.cj` 与 `liblog.a` 一同编译成一个可执行文件 `main` 。

### `--module-name <value>` <sup>[frontend]</sup>

指定要编译的模块的名称。

假设有文件 `my_module/src/log/printer.cj`：

```cangjie
package log

public func printLog(message: String) {
    println("[Log]: ${message}")
}
```

与文件 `main.cj`:

```cangjie
import my_module.log.*

main() {
    printLog("Everything is great")
}
```

可以使用

```shell
$ cjc -p my_module/src/log --module-name my_module --output-type=staticlib -o my_module/liblog.a
```

来编译 `log` 包并指定其模块名为 `my_module`，`cjc` 会在 `my_module` 目录下生成一个 `my_module/liblog.a` 文件。

然后可以使用 `liblog.a` 文件来编译导入了 `log` 包的 `main.cj` ，编译命令如下：

```shell
$ cjc main.cj my_module/liblog.a
```

`cjc` 会将 `main.cj` 与 `liblog.a` 一同编译成一个可执行文件 `main` 。

### `--output <value>`, `-o <value>`, `-o<value>` <sup>[frontend]</sup>

指定输出文件的路径，编译器的输出将被写入指定文件。

例如，以下命令会将输出的可执行文件名称指定为 `a.out`。

```shell
cjc main.cj -o a.out
```

### `--library <value>`, `-l <value>`, `-l<value>`

指定要链接的库文件。

给定的库文件会被直接传给链接器，此编译选项一般需要和 `--library-path <value>` 配合使用。

文件名的格式应为 `lib[arg].[extension]`。当需要链接库 `a` 时，可以使用选项 `-l a`，库文件搜索目录下的 `liba.a`、`liba.so`（或链接 Windows 目标程序时会搜索 `liba.dll`）等文件会被链接器搜索到并根据需要被链接至最终输出中。

### `--library-path <value>`, `-L <value>`, `-L<value>`

指定要链接的库文件所在的目录。

使用 `--library <value>` 选项时，通常也需要使用此选项来指定要链接的库文件所在的目录。

`--library-path <value>` 指定的路径会被加入链接器的库文件搜索路径。此外，环境变量 `LIBRARY_PATH` 中指定的路径也会被加入链接器的库文件搜索路径中，通过 `--library-path` 指定的路径会比 `LIBRARY_PATH` 中的路径拥有更高的优先级。

假设有从以下 C 语言源文件通过 C 语言编译器编译得到的动态库文件 `libcProg.so`，

```c
#include <stdio.h>

void printHello() {
    printf("Hello World\n");
}
```

仓颉文件 `main.cj`：

```cangjie
foreign func printHello(): Unit

main(): Int64 {
  unsafe {
    printHello()
  }
  return 0
}
```

可以使用

```shell
cjc main.cj -L . -l cProg
```

来编译 `main.cj` 并指定要链接的 `cProg` 库，这里 `cjc` 会输出一个可执行文件 `main`。

执行 `main` 会有如下输出：

```shell
$ LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH ./main
Hello World
```

**值得注意的是**，由于使用了动态库文件，这里需要将库文件所在目录加入 `$LD_LIBRARY_PATH` 以保证 `main` 能够在执行时进行动态链接。

### `-g` <sup>[frontend]</sup>

生成带有调试信息的可执行文件或库文件。

> **注意：**
>
> `-g` 只能配合 `-O0` 使用，如果使用更高的优化级别可能会导致调试功能出现异常。

### `--trimpath <value>` <sup>[frontend]</sup>

移除调试信息中源文件路径信息的前缀。

编译仓颉代码时，`cjc` 会保存源文件（`.cj` 文件）的绝对路径信息以在运行时提供调试与异常信息。

使用此选项可以将指定的路径前缀从源文件路径信息中移除，`cjc` 的输出文件中的源文件路径信息不会包含用户指定的部分。

可以多次使用 `--trimpath` 指定多个不同的路径前缀；对于每个源文件路径，编译器会将第一个匹配到的前缀从路径中移除。

### `--coverage` <sup>[frontend]</sup>

生成支持统计代码覆盖率的可执行程序。编译器会为每一个编译单元生成一个后缀名为 `gcno` 的代码信息文件。在执行程序后，每一个编译单元都会生成一个后缀名为 `gcda` 的执行统计文件。根据这两个文件，配合使用 `cjcov` 工具可以生成本次执行下的代码覆盖率报表。

> **注意：**
>
> `--coverage` 只能配合 `-O0` 使用，如果使用更高的优化级别，编译器将告警并强制使用 `-O0`。`--coverage` 用于编译生成可执行程序，如果用于生成静态库或者动态库，那么在最终使用该库时可能出现链接错误。

### `--int-overflow=[throwing|wrapping|saturating]` <sup>[frontend]</sup>

指定固定精度整数运算的溢出策略，默认为 `throwing`。

- `throwing` 策略下，整数运算溢出时会抛出异常。
- `wrapping` 策略下，整数运算溢出时会回转至对应固定精度整数的另一端。
- `saturating` 策略下，整数运算溢出时会选择对应固定精度的极值作为结果。

### `--diagnostic-format=[default|noColor|json]` <sup>[frontend]</sup>

> **注意：**
>
> Windows 版本暂不支持输出带颜色渲染的错误信息。

指定错误信息的输出格式，默认为 `default` 。

- `default` 错误信息默认格式输出（带颜色）
- `noColor` 错误信息默认格式输出（无颜色）
- `json` 错误信息`json`格式输出

### `--verbose`, `-V` <sup>[frontend]</sup>

`cjc` 会打印出编译器版本信息、工具链依赖的相关信息以及编译过程中执行的命令。

### `--help`, `-h` <sup>[frontend]</sup>

打印可用的编译选项。

使用此选项时，编译器仅会打印编译选项相关信息，不会对任何输入文件进行编译。

### `--version`, `-v` <sup>[frontend]</sup>

打印编译器版本信息。

使用此选项时，编译器仅会打印版本信息，不会对任何输入文件进行编译。

### `--save-temps <value>`

保留编译过程中生成的中间文件并保存至 `<value>` 路径下。

编译器会保留编译过程中生成的 `.bc`、`.o` 等中间文件。

### `--import-path <value>` <sup>[frontend]</sup>

指定导入模块的 AST 文件的搜索路径。

假设已有以下目录结构，`libs/myModule` 目录中包含 `myModule` 模块的库文件和 `log` 包的 AST 导出文件：

```text
.
├── libs
|   └── myModule
|       ├── log.cjo
|       └── libmyModule.a
└── main.cj
```

且有如下 `main.cj` 文件：

```cangjie
import myModule.log.printLog

main() {
    printLog("Everything is great")
}
```

可以通过使用 `--import-path ./libs` 来将 `./libs` 加入导入模块的 AST 文件搜索路径，`cjc` 会使用 `./libs/myModule/log.cjo` 文件来对 `main.cj` 文件进行语义检查与编译。

`--import-path` 提供与 `CANGJIE_PATH` 环境变量相同的功能，但通过 `--import-path` 设置的路径拥有更高的优先级。

### `--scan-dependency` <sup>[frontend]</sup>

通过 `--scan-dependency` 指令可以获得指定包源码或者一个包的 `cjo` 文件对于其他包的直接依赖以及其他信息，以 `json` 格式输出。

```cangjie
// this file is placed under directory pkgA
macro package pkgA
import pkgB.*
import std.io.*
import pkgB.subB.*
```

```shell
cjc --scan-dependency --package pkgA
```

或

```shell
cjc --scan-dependency pkgA.cjo
```

```json
{
  "package": "pkgA",
  "isMacro": true,
  "dependencies": [
    {
      "package": "pkgB",
      "isStd": false,
      "imports": [
        {
          "file": "pkgA/pkgA.cj",
          "begin": {
            "line": 2,
            "column": 1
          },
          "end": {
            "line": 2,
            "column": 14
          }
        }
      ]
    },
    {
      "package": "pkgB.subB",
      "isStd": false,
      "imports": [
        {
          "file": "pkgA/pkgA.cj",
          "begin": {
            "line": 4,
            "column": 1
          },
          "end": {
            "line": 4,
            "column": 19
          }
        }
      ]
    },
    {
      "package": "std.io",
      "isStd": true,
      "imports": [
        {
          "file": "pkgA/pkgA.cj",
          "begin": {
            "line": 3,
            "column": 1
          },
          "end": {
            "line": 3,
            "column": 16
          }
        }
      ]
    }
  ]
}
```

### `--no-sub-pkg` <sup>[frontend]</sup>

表明当前编译包没有子包。

开启该选项后，编译器可以进一步缩减 code size 大小。

### `--warn-off`, `-Woff <value>` <sup>[frontend]</sup>

关闭编译期出现的全部或部分警告。

`<value>` 可以为 `all` 或者一个设定好的警告组别。当参数为 `all` 时，对于编译过程中生成的所有警告，编译器都不会打印；当参数为其他设定好的组别时，编译器将不会打印编译过程中生成的该组别警告。

在打印每个警告时，会有一行 `#note` 提示该警告属于什么组别并如何关闭它，可以通过 `--help` 打印所有可用的编译选项参数，来查阅具体的组别名称。

### `--warn-on`, `-Won <value>` <sup>[frontend]</sup>

开启编译期出现的全部或部分警告。

`--warn-on` 的 `<value>` 与 `--warn-off` 的 `<value>` 取值范围相同，`--warn-on` 通常与 `--warn-off` 组合使用；比如，可以通过设定 `-Woff all -Won <value>` 来仅允许组别为 `<value>` 的警告被打印。

**特别要注意的是**，`--warn-on` 与 `--warn-off` 在使用上顺序敏感；针对同一组别，后设定的选项会覆盖之前选项的设定，比如，调换上例中两个编译选项的位置，使其变为 `-Won <value> -Woff all`，其效果将变为关闭所有警告。

### `--error-count-limit <value>` <sup>[frontend]</sup>

限制编译器打印错误个数的上限。

参数 `<value>` 可以为 `all` 或一个非负整数。当参数为 `all` 时，编译器会打印编译过程中生成的所有错误；当参数为非负整数 `N` 时，编译器最多会打印 `N` 个错误。此选项默认值为 8。

### `--output-dir <value>` <sup>[frontend]</sup>

控制编译器生成的中间文件与最终文件的保存目录。

控制编译器生成的中间文件的保存目录，例如 `.cjo` 文件。当指定 `--output-dir <path1>` 时也指定了 `--output <path2>`，则中间文件会被保存至 `<path1>`，最终输出会被保存至 `<path1>/<path2>` 。

> **注意：**
>
> 同时指定此选项与 `--output` 选项时，`--output` 选项的参数必须是一个相对路径。

### `--static`

静态链接仓颉库。

此选项仅在编译可执行文件时生效。

**值得注意的是：**

`--static` 选项仅适用于 Linux 平台，在其他平台不生效。

### `--static-std`

静态链接仓颉库的 std 模块。

此选项仅在编译动态链接库或可执行文件时生效。

当编译可执行程序时（即指定了 `--output-type=exe` 时），`cjc` 默认静态链接仓颉库的 std 模块。

### `--dy-std`

动态链接仓颉库的 std 模块。

此选项仅在编译动态链接库或可执行文件时生效。

当编译动态库时（即指定了 `--output-type=dylib` 时），`cjc` 默认动态链接仓颉库的 std 模块。

**值得注意的是：**

1. `--static-std` 和 `--dy-std` 选项一起使用时，仅最后一个选项生效。
2. `--dy-std` 与 `--static-libs` 选项不可一起使用，否则会报错。
3. 当编译可执行程序时链接了仓颉动态库（即通过 `--output-type=dylib` 选项编译的产物），必须显式指定 `--dy-std` 选项动态链接标准库，否则可能导致程序集中出现多份标准库，最终可能会导致运行时问题。

### `--static-libs`

静态链接仓颉库中除 std 及运行时模块外的其他模块。

此选项仅在编译动态链接库或可执行文件时生效。`cjc` 默认静态链接仓颉库中除 std 及运行时模块外的其他模块。

### `--dy-libs`

动态链接仓颉库非 std 的其他模块。

此选项仅在编译动态链接库或可执行文件时生效。

**值得注意的是：**

1. `--static-libs` 和 `--dy-libs` 选项一起使用时，仅最后一个选项生效；
2. `--static-std` 与 `--dy-libs` 选项不可一起使用，否则会报错；
3. `--dy-std` 单独使用时，会默认生效 `--dy-libs` 选项，并有相关告警信息提示；
4. `--dy-libs` 单独使用时，会默认生效 `--dy-std` 选项，并有相关告警信息提示。

### `--stack-trace-format=[default|simple|all]`

指定异常调用栈打印格式，用来控制异常抛出时的栈帧信息显示，默认为 `default` 格式。

异常调用栈的格式说明如下：

- `default` 格式：`省略泛型参数的函数名 (文件名:行号)`
- `simple` 格式： `文件名:行号`
- `all` 格式：`完整的函数名 (文件名:行号)`

### `--lto=[full|thin]`

使能且指定 `LTO` （`Link Time Optimization` 链接时优化）优化编译模式。

**值得注意的是：**

1. `Windows` 以及 `macOS` 平台不支持该功能；
2. 当使能且指定 `LTO` （`Link Time Optimization` 链接时优化）优化编译模式时，不允许同时使用如下优化编译选项：`-Os`、`-Oz`。

`LTO` 优化支持两种编译模式：

- `--lto=full`：`full LTO` 将所有编译模块合并到一起，在全局上进行优化，这种方式可以获得最大的优化潜力，同时也需要更长的编译时间。
- `--lto=thin`：相比于 `full LTO`，`thin LTO` 在多模块上使用并行优化，同时默认支持链接时增量编译，编译时间比 `full LTO` 短，因为失去了更多的全局信息，所以优化效果不如 `full LTO`。

    - 通常情况下优化效果对比：`full LTO` **>** `thin LTO` **>** 常规静态链接编译。
    - 通常情况下编译时间对比：`full LTO` **>** `thin LTO` **>** 常规静态链接编译。

`LTO` 优化使用场景：

1. 使用以下命令编译可执行文件。

    ```shell
    $ cjc test.cj --lto=full
    or
    $ cjc test.cj --lto=thin
    ```

2. 使用以下命令编译 `LTO` 模式下需要的静态库（`.bc` 文件），并且使用该库文件参与可执行文件编译。

    ```shell
    # 生成的静态库为 .bc 文件
    $ cjc pkg.cj --lto=full --output-type=staticlib -o libpkg.bc
    # .bc 文件和源文件一起输入给仓颉编译器编译可执行文件
    $ cjc test.cj libpkg.bc --lto=full
    ```

    > **注意：**
    >
    > `LTO` 模式下的静态库（`.bc` 文件）输入时需要将该文件的路径输入仓颉编译器。

3. 在 `LTO` 模式下，静态链接标准库（`--static-std` & `--static-libs`）时，标准库的代码也会参与 `LTO` 优化，并静态链接到可执行文件；动态链接标准库（`--dy-std` & `--dy-libs`）时，在 `LTO` 模式下依旧使用标准库中的动态库参与链接。

    ```shell
    # 静态链接，标准库代码也参与 LTO 优化
    $ cjc test.cj --lto=full --static-std
    # 动态链接，依旧使用动态库参与链接，标准库代码不会参与 LTO 优化
    $ cjc test.cj --lto=full --dy-std
    ```

### `--pgo-instr-gen`

使能插桩编译，生成携带插桩信息的可执行程序。

编译 macOS 与 Windows 目标时暂不支持使用该功能。

`PGO`（全称 `Profile-Guided Optimization`）是一种常用的编译优化技术，通过使用运行时 profiling 信息进一步提升程序性能。`Instrumentation-based PGO` 是使用插桩信息的一种 `PGO` 优化手段，它通常包含三个步骤：

1. 编译器对源码插桩编译，生成插桩后的可执行程序（instrumented program）；
2. 运行插桩后的可执行程序，生成配置文件；
3. 编译器使用配置文件，再次对源码进行编译。

```shell
# 生成支持源码执行信息统计（携带插桩信息）的可执行程序 test
$ cjc test.cj --pgo-instr-gen -o test
# 运行可执行程序 test 结束后，生成 default.profraw 配置文件
$ ./test
```

### `--pgo-instr-use=<.profdata>`

使用指定 `profdata` 配置文件指导编译并生成优化后的可执行程序。

编译 macOS 目标时暂不支持使用该功能。

> **注意：**
>
> `--pgo-instr-use` 编译选项仅支持格式为 `profdata` 的配置文件。可使用 `llvm-profdata` 工具可将 `profraw` 配置文件转换为 `profdata` 配置文件。

```shell
# 将 `profraw` 文件转换为 `profdata` 文件。
$ LD_LIBRARY_PATH=$CANGJIE_HOME/third_party/llvm/lib:$LD_LIBRARY_PATH $CANGJIE_HOME/third_party/llvm/bin/llvm-profdata merge default.profraw -o default.profdata
# 使用指定 `default.profdata` 配置文件指导编译并生成优化后的可执行程序 `testOptimized`
$ cjc test.cj --pgo-instr-use=default.profdata -o testOptimized
```

### `--target <value>` <sup>[frontend]</sup>

指定编译的目标平台的 triple。

参数 `<value>` 一般为符合以下格式的字符串：`<arch>(-<vendor>)-<os>(-<env>)`。其中：

- `<arch>` 表示目标平台的系统架构，例如 `aarch64`，`x86_64` 等；
- `<vendor>` 表示开发目标平台的厂商，常见的例如 `apple` 等，在没有明确平台厂商或厂商不重要的情况下也经常写作 `unknown` 或直接省略；
- `<os>` 表示目标平台的操作系统，例如 `Linux`，`Win32` 等；
- `<env>` 表示目标平台的 ABI 或标准规范，用于更细粒度地区分同一操作系统的不同运行环境，例如 `gnu`，`musl` 等。在操作系统不需要根据 `<env>` 进行更细地区分的时候，此项也可以省略。

目前，`cjc` 已支持交叉编译的本地平台和目标平台如下表所示：

| 本地平台 (host)    | 目标平台 (target)   |
| ------------------ | ------------------ |
| x86_64-linux-gnu   | x86_64-windows-gnu     |
| aarch64-linux-gnu   | x86_64-windows-gnu     |

在使用 `--target` 指定目标平台进行交叉编译之前，请准备好对应目标平台的交叉编译工具链，以及可以在本地平台上运行的、向该目标平台编译的对应 Cangjie SDK 版本。

### `--target-cpu <value>`

> **注意：**
>
> 该选项为实验性功能，使用该功能生成的二进制可能存在潜在的运行时问题，请注意使用该选项的风险。此选项必须配合 `--experimental` 选项一同使用。

指定编译目标的 CPU 类型。

指定编译目标的 CPU 类型时，编译器在生成二进制时会尝试使用该 CPU 类型特有的扩展指令集，并尝试应用适用于该 CPU 类型的优化。为某个特定 CPU 类型生成的二进制通常会失去可移植性，该二进制可能无法在其他（拥有相同架构指令集的）CPU 上运行。

该选项支持以下经过测试的 CPU 类型：

**x86-64 架构：**

- generic

**aarch64 架构：**

- generic
- tsv110

`generic` 为通用 CPU 类型，指定 `generic` 时编译器会生成适用于该架构的通用指令，这样生成的二进制在操作系统和二进制本身的动态依赖一致的前提下，可以在基于该架构的各种 CPU 上运行，无关于具体的 CPU 类型。`--target-cpu` 选项的默认值为 `generic`。

该选项还支持以下 CPU 类型，但以下 CPU 类型未经过测试验证，请注意使用以下 CPU 类型生成的二进制可能会存在运行时问题。

**x86-64 架构：**

- alderlake
- amdfam10
- athlon
- athlon-4
- athlon-fx
- athlon-mp
- athlon-tbird
- athlon-xp
- athlon64
- athlon64-sse3
- atom
- barcelona
- bdver1
- bdver2
- bdver3
- bdver4
- bonnell
- broadwell
- btver1
- btver2
- c3
- c3-2
- cannonlake
- cascadelake
- cooperlake
- core-avx-i
- core-avx2
- core2
- corei7
- corei7-avx
- geode
- goldmont
- goldmont-plus
- haswell
- i386
- i486
- i586
- i686
- icelake-client
- icelake-server
- ivybridge
- k6
- k6-2
- k6-3
- k8
- k8-sse3
- knl
- knm
- lakemont
- nehalem
- nocona
- opteron
- opteron-sse3
- penryn
- pentium
- pentium-m
- pentium-mmx
- pentium2
- pentium3
- pentium3m
- pentium4
- pentium4m
- pentiumpro
- prescott
- rocketlake
- sandybridge
- sapphirerapids
- silvermont
- skx
- skylake
- skylake-avx512
- slm
- tigerlake
- tremont
- westmere
- winchip-c6
- winchip2
- x86-64
- x86-64-v2
- x86-64-v3
- x86-64-v4
- yonah
- znver1
- znver2
- znver3

**aarch64 架构：**

- a64fx
- ampere1
- apple-a10
- apple-a11
- apple-a12
- apple-a13
- apple-a14
- apple-a7
- apple-a8
- apple-a9
- apple-latest
- apple-m1
- apple-s4
- apple-s5
- carmel
- cortex-a34
- cortex-a35
- cortex-a510
- cortex-a53
- cortex-a55
- cortex-a57
- cortex-a65
- cortex-a65ae
- cortex-a710
- cortex-a72
- cortex-a73
- cortex-a75
- cortex-a76
- cortex-a76ae
- cortex-a77
- cortex-a78
- cortex-a78c
- cortex-r82
- cortex-x1
- cortex-x1c
- cortex-x2
- cyclone
- exynos-m3
- exynos-m4
- exynos-m5
- falkor
- kryo
- neoverse-512tvb
- neoverse-e1
- neoverse-n1
- neoverse-n2
- neoverse-v1
- saphira
- thunderx
- thunderx2t99
- thunderx3t110
- thunderxt81
- thunderxt83
- thunderxt88

除以上可选 CPU 类型外，该选项还可以使用 `native` 作为当前 CPU 类型。编译器会尝试识别当前机器的 CPU 类型，并使用该 CPU 类型作为目标类型生成二进制文件。

### `--toolchain <value>`, `-B <value>`, `-B<value>`

指定编译工具链中，二进制文件存放的路径。

这些二进制文件包括编译器、链接器、工具链提供的 C 运行时目标文件（如 `crt0.o`、 `crti.o` 等）。

在准备好编译工具链后，可以在将其存放在一个自定义路径，然后通过 `--toolchain <value>` 向编译器传入该路径，即可让编译器调用到该路径下的二进制文件进行交叉编译。

### `--sysroot <value>`

指定编译工具链的根目录路径。

对于目录结构固定的交叉编译工具链，如果没有指定该目录以外的二进制和动态库、静态库文件路径的需求，可以直接使用 `--sysroot <value>` 向编译器传入工具链的根目录路径，编译器会根据目标平台种类分析对应的目录结构，自动搜索所需的二进制文件和动态库、静态库文件。使用该选项后，无需再指定 `--toolchain`、`--library-path` 参数。

如果向 `triple` 为 `arch-os-env` 的平台进行交叉编译，且交叉编译工具链有以下目录结构：

```text
/usr/sdk/arch-os-env
├── bin
|   ├── arch-os-env-gcc (交叉编译器)
|   ├── arch-os-env-ld  (链接器)
|   └── ...
├── lib
|   ├── crt1.o          (C 运行时目标文件)
|   ├── crti.o
|   ├── crtn.o
|   ├── libc.so         (动态库)
|   ├── libm.so
|   └── ...
└── ...
```

对于仓颉源文件 `hello.cj` ，可以使用以下命令，将 `hello.cj` 交叉编译至 `arch-os-env` 平台：

```shell
cjc --target=arch-os-env --toolchain /usr/sdk/arch-os-env/bin --toolchain /usr/sdk/arch-os-env/lib --library-path /usr/sdk/arch-os-env/lib hello.cj -o hello
```

也可以使用简写的参数：

```shell
cjc --target=arch-os-env -B/usr/sdk/arch-os-env/bin -B/usr/sdk/arch-os-env/lib -L/usr/sdk/arch-os-env/lib hello.cj -o hello
```

如果该工具链的目录符合惯例的目录结构，可以不使用 `--toolchain`、`--library-path` 参数，直接使用以下命令：

```shell
cjc --target=arch-os-env --sysroot /usr/sdk/arch-os-env hello.cj -o hello
```

### `--strip-all`, `-s`

编译可执行文件或动态库时，指定该选项以删除输出文件中的符号表。

### `--discard-eh-frame`

编译可执行文件或动态库时，指定该选项可以删除 eh_frame 段以及 eh_frame_hdr 段中的部分信息（涉及到 crt 的相关信息不作处理），减少可执行文件或动态库的大小，但会影响调试信息。

编译 macOS 目标时暂不支持使用该功能。

### `--set-runtime-rpath`

将仓颉运行时库所在目录的绝对路径写入到二进制的 RPATH/RUNPATH 段中，使用该选项后在构建所在环境中运行该仓颉程序时无需再使用 LD_LIBRARY_PATH (适用于 Linux 平台) 或 DYLD_LIBRARY_PATH (适用于 macOS 平台) 设置仓颉运行时库目录。

编译 Windows 目标时不支持使用该功能。

### `--link-options <value>`<sup>1</sup>

指定链接器选项。

`cjc` 会将该选项的多个参数透传给链接器, 参数之间用空格分隔。可用的参数会因（系统或指定的）链接器的不同而不同。可以多次使用 `--link-options` 指定多个链接器选项。

<sup>1</sup> 上标表示链接器透传选项可能会因为链接器的不同而不同，具体支持的选项请查阅链接器文档。

### `--disable-reflection`

关闭反射选项，即编译过程中不生成相关反射信息。

> **注意：**
>
> 交叉编译至 aarch64-linux-ohos 目标时，默认关闭反射信息，该选项不生效。

### `--profile-compile-time` <sup>[frontend]</sup>

打印各编译阶段的时间消耗数据。

### `--profile-compile-memory` <sup>[frontend]</sup>

打印各编译阶段的内存消耗数据。

## 单元测试选项

### `--test` <sup>[frontend]</sup>

`unittest` 测试框架提供的入口，由宏自动生成。当使用 `cjc --test` 选项编译时，程序入口不再是 `main`，而是 `test_entry`。unittest 测试框架的使用方法请参见《仓颉编程语言标准库 API》文档。

对于 `pkgc` 目录下的仓颉文件 `a.cj`:
<!-- run -->

```cangjie
import std.unittest.*
import std.unittest.testmacro.*

@Test
public class TestA {
    @TestCase
    public func case1(): Unit {
        print("case1\n")
    }
}
```

可以在 `pkgc` 目录下使用：

```shell
cjc a.cj --test
```

来编译 `a.cj` ，执行 `main` 会有如下输出：

> **注意：**
>
> 不保证用例每次执行的用时都相同。

```cangjie
case1
--------------------------------------------------------------------------------------------------
TP: default, time elapsed: 29710 ns, Result:
    TCS: TestA, time elapsed: 26881 ns, RESULT:
    [ PASSED ] CASE: case1 (16747 ns)
Summary: TOTAL: 1
    PASSED: 1, SKIPPED: 0, ERROR: 0
    FAILED: 0
--------------------------------------------------------------------------------------------------
```

对于如下目录结构：

```text
application
├── src
├── pkgc
|   ├── a1.cj
|   └── a2.cj
└── a3.cj
```

可以在 `application`目录下使用 `-p` 编译选项配合编译整包：

```shell
cjc pkgc --test -p
```

来编译整个 `pkgc` 包下的测试用例 `a1.cj` 和 `a2.cj`。

```cangjie
/*a1.cj*/
package a

import std.unittest.*
import std.unittest.testmacro.*

@Test
public class TestA {
    @TestCase
    public func caseA(): Unit {
        print("case1\n")
    }
}
```

```cangjie
/*a2.cj*/
package a

import std.unittest.*
import std.unittest.testmacro.*

@Test
public class TestB {
    @TestCase
    public func caseB(): Unit {
        throw IndexOutOfBoundsException()
    }
}
```

执行 `main` 会有如下输出（**输出信息仅供参考**）：

```cangjie
case1
--------------------------------------------------------------------------------------------------
TP: a, time elapsed: 367800 ns, Result:
    TCS: TestA, time elapsed: 16802 ns, RESULT:
    [ PASSED ] CASE: caseA (14490 ns)
    TCS: TestB, time elapsed: 347754 ns, RESULT:
    [ ERROR  ] CASE: caseB (345453 ns)
    REASON: An exception has occurred:IndexOutOfBoundsException
        at std/core.Exception::init()(std/core/exception.cj:23)
        at std/core.IndexOutOfBoundsException::init()(std/core/index_out_of_bounds_exception.cj:9)
        at a.TestB::caseB()(/home/houle/cjtest/application/pkgc/a2.cj:7)
        at a.lambda.1()(/home/houle/cjtest/application/pkgc/a2.cj:7)
        at std/unittest.TestCases::execute()(std/unittest/test_case.cj:92)
        at std/unittest.UT::run(std/unittest::UTestRunner)(std/unittest/test_runner.cj:194)
        at std/unittest.UTestRunner::doRun()(std/unittest/test_runner.cj:78)
        at std/unittest.UT::run(std/unittest::UTestRunner)(std/unittest/test_runner.cj:200)
        at std/unittest.UTestRunner::doRun()(std/unittest/test_runner.cj:78)
        at std/unittest.UT::run(std/unittest::UTestRunner)(std/unittest/test_runner.cj:200)
        at std/unittest.UTestRunner::doRun()(std/unittest/test_runner.cj:75)
        at std/unittest.entryMain(std/unittest::TestPackage)(std/unittest/entry_main.cj:11)
Summary: TOTAL: 2
    PASSED: 1, SKIPPED: 0, ERROR: 1
    FAILED: 0
--------------------------------------------------------------------------------------------------
```

### `--test-only` <sup>[frontend]</sup>

`--test-only` 选项用于单独编译包的测试部分。

如果启用此选项，编译器将仅编译包中的测试文件（以 `_test.cj` 结尾）。

> **注意：**
>
> 使用此选项时，应单独以常规模式编译相同的包，然后通过 `-L`/`-l` 链接选项添加依赖，或在使用 `LTO` 选项时添加依赖的 `.bc` 文件。否则，编译器将报缺少依赖的符号的错误。

示例:

```cangjie
/*main.cj*/
package my_pkg

func concatM(s1: String, s2: String): String {
    return s1 + s2
}

main() {
    println(concatM("a", "b"))
    0
}
```

```cangjie
/*main_test.cj*/
package my_pkg

@Test
class Tests {
    @TestCase
    public func case1(): Unit {
        @Expect("ac", concatM("a", "c"))
    }
}
```

使用编译器编译的命令如下：

```shell
# Compile the production part of the package first, only `main.cj` file would be compiled here
cjc -p my_pkg --output-type=static -o=output/libmain.a
# Compile the test part of the package, Only `main_test.cj` file would be compiled here
cjc -p my_pkg --test-only -L output -lmain
```

### `--mock <on|off|runtime-error>` <sup>[frontend]</sup>

如果传递了 `on` ，则该包将使能 mock 编译，该选项允许在测试用例中 mock 该包中的类。`off` 是一种显式禁用 mock 的方法。

> **注意：**
>
> 在测试模式下（当使能 `--test` ）自动启用对此包的 mock 支持，不需要显式传递 `--mock` 选项。

`runtime-error` 仅在测试模式下可用（当使能 `--test` 时），它允许编译带有 mock 代码的包，但不在编译器中做任何 mock 相关的处理（这些处理可能会造成一些开销并影响测试的运行时性能）。这对于带有 mock 代码用例进行基准测试时可能是有用的。使用此编译选项时，避免编译带有 mock 代码的用例并运行测试，否则将抛出运行时异常。

## 宏选项

`cjc` 支持以下宏选项，关于宏的更多内容请参见[“宏的简介”](../Macro/macro_introduction.md)章节。

### `--compile-macro` <sup>[frontend]</sup>

编译宏定义文件，生成默认的宏定义动态库文件。

### `--debug-macro` <sup>[frontend]</sup>

生成宏展开后的仓颉代码文件。该选项可用于调试宏展开功能。

### `--parallel-macro-expansion` <sup>[frontend]</sup>

开启宏展开并行。该选项可用于缩短宏展开编译时间。

## 条件编译选项

`cjc` 支持以下条件编译选项，关于条件编译的更多内容请参见[“条件编译”](../compile_and_build/conditional_compilation.md)。

### `--cfg <value>` <sup>[frontend]</sup>

指定自定义编译条件。

## 并行编译选项

`cjc` 支持以下并行编译选项，以获得更高的编译效率。

### `--jobs <value>`, `-j <value>` <sup>[frontend]</sup>

设置并行编译时所允许的最大并行数。其中 `value` 必须是一个合理的非负整数，当 `value` 大于硬件支持的最大并行能力时，编译器将以硬件支持的最大并行能力执行并行编译。

如果该编译选项未设置，编译器会基于硬件能力自动计算最大并行数。

> **注意：**
>
> `--jobs 1` 表示完全使用串行方式进行编译。

### `--aggressive-parallel-compile`, `--apc`, `--aggressive-parallel-compile=<value>`, `--apc=<value>` <sup>[frontend]</sup>

开启此选项后，编译器会采用更加激进的策略（可能会对优化造成影响，从而导致程序运行性能下降）执行激进并行编译，以便获得更高的编译效率。其中 `value` 是一个可选参数，表示激进并行编译部分允许的最大并行数：

- 如果使用 `value`，则 `value` 必须是一个合理的非负整数，当 `value` 大于硬件支持的最大并行能力时，编译器会基于硬件能力自动计算最大并行数。建议将 `value` 设置为小于硬件的物理核数的非负整数。
- 如果不使用 `value`，则激进并行编译默认开启，且激进并行编译部分的并行数与 `--jobs` 一致。

此外，如果两次编译同一份代码时此选项的 `value` 值不同，或此选项的开关状态不同，编译器不保证这两次编译的产物的二进制一致性。

激进并行编译的开启或关闭规则如下：

- 在以下场景中，激进并行编译将由编译器强制关闭，无法启用：

    - `--fobf-string`
    - `--fobf-const`
    - `--fobf-layout`
    - `--fobf-cf-flatten`
    - `--fobf-cf-bogus`
    - `--lto`
    - `--coverage`
    - 编译 Windows 目标
    - 编译 macOS 目标

- 若使用 `--aggressive-parallel-compile=<value>` 或 `--apc=<value>`，则激进并行编译的开关由 `value` 控制：

    - `value <= 1`：关闭激进并行编译。
    - `value > 1`：开启激进并行编译，且激进并行编译的并行数取决于 `value`。

- 若使用 `--aggressive-parallel-compile` 或 `--apc`，则激进并行编译默认开启，且激进并行编译的并行数与 `--jobs` 一致。

- 若该编译选项未设置，编译器将根据场景默认开启或关闭激进并行编译：

    - `-O0` 或 `-g`：激进并行编译将由编译器默认开启，且激进并行编译的并行数与 `--jobs` 一致；可以通过 `--aggressive-parallel-compile=<value>` 或 `--apc=<value>` 且 `value <= 1` 关闭激进并行编译。
    - 非 `-O0` 且非 `-g`：激进并行编译将由编译器默认关闭；可以通过 `--aggressive-parallel-compile=<value>` 或 `--apc=<value>` 且 `value > 1` 开启激进并行编译。

## 优化选项

### `--fchir-constant-propagation` <sup>[frontend]</sup>

开启 chir 常量传播优化。

### `--fno-chir-constant-propagation` <sup>[frontend]</sup>

关闭 chir 常量传播优化。

### `--fchir-function-inlining` <sup>[frontend]</sup>

开启 chir 函数内联优化。

### `--fno-chir-function-inlining` <sup>[frontend]</sup>

关闭 chir 函数内联优化。

### `--fchir-devirtualization` <sup>[frontend]</sup>

开启 chir 去虚函数调用优化。

### `--fno-chir-devirtualization` <sup>[frontend]</sup>

关闭 chir 去虚函数调用优化。

### `--fast-math` <sup>[frontend]</sup>

开启此选项后，编译器会对浮点数作一些激进且有可能损失精度的假设，以便优化浮点数运算。

### `-O<N>` <sup>[frontend]</sup>

使用参数指定的代码优化级别。

指定越高的优化级别，编译器会越多地进行代码优化以生成更高效的程序，同时也可能会需要更长的编译时间。

`cjc` 默认使用 O0 级别的代码优化。当前 `cjc` 支持如下优化级别：O0、O1、O2、Os、Oz。

当优化等级等于 2 时，`cjc` 除了进行对应的优化外，还会开启以下选项：

- `--fchir-constant-propagation`
- `--fchir-function-inlining`
- `--fchir-devirtualization`

当优化等级等于 s 时， `cjc`除了进行 O2 级别优化外，将针对 code size 进行优化。

当优化等级等于 z 时， `cjc`除了进行 Os 级别优化外，还将进一步缩减 code size 大小。

> **注意：**
>
> 当优化等级等于 s 或 z 时，不允许同时使用链接时优化编译选项 `--lto=[full|thin]`。

### `-O` <sup>[frontend]</sup>

使用 O1 级别的代码优化，等价于 `-O1`。

## 代码混淆选项

`cjc` 支持代码混淆功能，以提供对代码的额外安全保护，默认不开启。

`cjc` 支持以下代码混淆选项：

### `--fobf-string`

开启字符串混淆。

混淆代码中出现的字符串常量，攻击者无法静态直接读取二进制程序中的字符串数据。

### `--fno-obf-string`

关闭字符串混淆。

### `--fobf-const`

开启常量混淆。

混淆代码中使用的数值常量，将数值运算指令替换成等效的、更复杂的数值运算指令序列。

### `--fno-obf-const`

关闭常量混淆。

### `--fobf-layout`

开启外形混淆。

外形混淆功能会混淆代码中的符号（包括函数名和全局变量名）、路径名、代码行号和函数排布顺序。使用该编译选项后，`cjc` 会在当前目录生成符号映射输出文件 `*.obf.map`。如果配置了 `--obf-sym-output-mapping` 选项，则 `--obf-sym-output-mapping` 的参数值将作为 `cjc` 生成的符号映射输出文件名。符号映射输出文件中包含混淆前后符号的映射关系，使用符号映射输出文件可以解混淆被混淆过的符号。

> **注意：**
>
> 外形混淆功能和并行编译功能相互冲突，请勿同时开启。如果和并行编译同时开启，并行编译将失效。

### `--fno-obf-layout`

关闭外形混淆。

### `--obf-sym-prefix <string>`

指定外形混淆功能在混淆符号时添加的前缀字符串。

设置该选项后，所有被混淆符号都会加上该前缀。在编译混淆多个仓颉包时可能出现符号冲突的问题，可以使用该选项给不同的包指定不同的前缀，避免符号冲突。

### `--obf-sym-output-mapping <file>`

指定外形混淆的符号映射输出文件。

符号映射输出文件记录了符号的原始名称、混淆后的名称和所属文件路径。使用符号映射输出文件可以解混淆被混淆过的符号。

### `--obf-sym-input-mapping <file,...>`

指定外形混淆的符号映射输入文件。

外形混淆功能会使用这些文件中的映射关系对符号进行混淆。因此在编译存在调用关系的仓颉包，请使用被调用包的符号映射输出文件作为调用包混淆时的 `--obf-sym-input-mapping` 选项的参数，以此保证同一个符号在调用包和被调用包两者混淆时混淆结果一致。

### `--obf-apply-mapping-file <file>`

提供自定义的外形混淆符号映射关系文件，外形混淆功能将按照文件里的映射关系混淆符号。

文件格式如下：

```text
<original_symbol_name> <new_symbol_name>
```

其中 `original_symbol_name` 是混淆前的名称，`new_symbol_name` 是混淆后的名称。`original_symbol_name` 由多个 `field` 组成。`field` 表示字段名，可以是模块名、包名、类名、结构体名、枚举名、函数名或变量名。`field` 之间用分隔符 `'.'` 分隔。如果 `field` 是函数名，则需要将函数的参数类型用括号 `'()'` 修饰并附加在函数名后面。对于无参函数括号内的内容为空。如果 `field` 存在泛型参数，也需要用括号 `'<>'` 将具体的泛型参数附加在 `field` 后面。

外形混淆功能会将仓颉应用中的 `original_symbol_name` 替换为 `new_symbol_name`。对于不在该文件中的符号，外形混淆功能会正常使用随机名称进行替换。如果该文件中指定的映射关系和 `--obf-sym-input-mapping` 中的映射关系相冲突，编译器会抛出异常并停止编译。

### `--fobf-export-symbols`

允许外形混淆功能混淆导出符号，该选项在开启外形混淆功能时默认开启。

开启该选项后，外形混淆功能会对导出符号进行混淆。

### `--fno-obf-export-symbols`

禁止外形混淆功能混淆导出符号。

### `--fobf-source-path`

允许外形混淆功能混淆符号的路径信息，该选项在开启外形混淆功能时默认开启。

开启该选项后，外形混淆功能会混淆异常堆栈信息中的路径信息，将路径名替换为字符串 `"SOURCE"`。

### `--fno-obf-source-path`

禁止外形混淆功能混淆堆栈信息中的路径信息。

### `--fobf-line-number`

允许外形混淆功能混淆堆栈信息中的行号信息。

开启该选项后，外形混淆功能会混淆异常堆栈信息中的行号信息，将行号替换为 `0`。

### `--fno-obf-line-number`

禁止外形混淆功能混淆堆栈信息中的行号信息。

### `--fobf-cf-flatten`

开启控制流平坦化混淆。

混淆代码中既存的控制流，使其转移逻辑变得复杂。

### `--fno-obf-cf-flatten`

关闭控制流平坦化混淆。

### `--fobf-cf-bogus`

开启虚假控制流混淆。

在代码中插入虚假的控制流，使代码逻辑变得复杂。

### `--fno-obf-cf-bogus`

关闭虚假控制流混淆。

### `--fobf-all`

开启所有混淆功能。

指定该选项等同于同时指定以下选项：

- `--fobf-string`
- `--fobf-const`
- `--fobf-layout`
- `--fobf-cf-flatten`
- `--fobf-cf-bogus`

### `--obf-config <file>`

指定代码混淆配置文件路径。

在配置文件中可以禁止混淆工具对某些函数或者符号进行混淆。

配置文件的具体格式如下：

```text
obf_func1 name1
obf_func2 name2
...
```

第一个参数 `obf_func` 是具体的混淆功能：

- `obf-cf-bogus`：虚假控制流混淆
- `obf-cf-flatten`：控制流平坦化混淆
- `obf-const`：常数混淆
- `obf-layout`：外形混淆

第二个参数 `name` 是需要被保留的对象，由多个 `field` 组成。`field` 表示字段名，可以是包名、类名、结构体名、枚举名、函数名或变量名。

`field` 之间用分隔符 `'.'` 分隔。如果 `field` 是函数名，则需要将函数的参数类型用括号 `'()'` 修饰并附加在函数名后面。对于无参函数括号内的内容为空。

例如，假设在包 `packA` 中有以下代码：

```cangjie
package packA
class MyClassA {
    func funcA(a: String, b: Int64): String {
        return a
    }
}
```

如果要禁止控制流平坦化功能混淆 `funcA`，用户可以编写如下规则：

```text
obf-cf-flatten packA.MyClassA.funcA(std.core.String, Int64)
```

用户也可以使用通配符编写更加灵活的规则，达到一条规则保留多个对象的效果。目前支持的通配符包含以下 3 类：

混淆功能通配符：

| 混淆功能通配符 | 说明                     |
| :-------------- | :----------------------- |
| `?`            | 匹配名称中的单个字符     |
| `*`            | 匹配名称中的任意数量字符 |

字段名通配符：

| 字段名通配符 | 说明                                                         |
| :------------ | :------------------------------------------------------------ |
| `?`          | 匹配字段名中单个非分隔符 `'.'` 的字符                        |
| `*`          | 匹配字段名中的不包含分隔符 `'.'` 和参数的任意数量字符        |
| `**`         | 匹配字段名中的任意数量字符，包括字段之间的分隔符 `'.'` 和参数。`'**'` 只有在单独作为一个 `field` 时才生效，否则会被当作 `'*'` 处理 |

函数的参数类型通配符：

| 参数类型通配符 | 说明                   |
| :-------------- | :---------------------- |
| `...`          | 匹配任意数量的参数     |
| `***`          | 匹配一个任意类型的参数 |

> **说明：**
>
> 参数类型也由字段名组成，因此也可以使用字段名通配符对单个参数类型进行匹配。

以下是通配符使用示例：

例子 1：

```text
obf-cf-flatten pro?.myfunc()
```

该规则表示禁止 `obf-cf-flatten` 功能混淆函数 `pro?.myfunc()`，`pro?.myfunc()` 可以匹配 `pro0.myfunc()`，但不能匹配 `pro00.myfunc()`。

例子 2：

```text
* pro0.**
```

该规则表示禁止任何混淆功能混淆包 `pro0` 下的任何函数和变量。

例子 3：

```text
* pro*.myfunc(...)
```

该规则表示禁止任何混淆功能混淆函数 `pro*.myfunc(...)`，`pro*.myfunc(...)` 可以匹配以 `pro` 开头的任意单层包内的 `myfunc` 函数，且可以为任意参数。

如果需要匹配多层包名，比如 `pro0.mypack.myfunc()`，请使用 `pro*.**.myfunc(...)`。请注意 `'**'` 只有单独作为字段名时才生效，因此 `pro**.myfunc(...)` 和 `pro*.myfunc(...)` 等价，无法匹配多层包名。如果要匹配以 `pro` 开头的所有包下的所有 `myfunc` 函数（包括类中名为 `myfunc` 的函数），请使用 `pro*.**.myfunc(...)`。

例子 4：

```text
obf-cf-* pro0.MyClassA.myfunc(**.MyClassB, ***, ...)
```

该规则表示禁止 `obf-cf-*` 功能混淆函数 `pro0.MyClassA.myfunc(**.MyClassB, ***, ...)`，其中 `obf-cf-*` 会匹配 `obf-cf-bogus` 和 `obf-cf-flatten` 两种混淆功能，`pro0.MyClassA.myfunc(**.MyClassB, ***, ...)` 会匹配函数 `pro0.MyClassA.myfunc`，且函数的第一个参数可以是任意包下的 `MyClassB` 类型，第二个参数可以是任意类型，后面可以接零至多个任意参数。

### `--obf-level <value>`

指定混淆功能强度级别。

可指定 1-9 强度级别。默认强度级别为 5。级别数字越大，强度则越高，该选项会影响输出文件的大小以及执行开销。

### `--obf-seed <value>`

指定混淆算法的随机数种子。

通过指定混淆算法的随机数种子，可以使同一份仓颉代码在不同构建时有不同的混淆结果。默认场景下，对于同一份仓颉代码，在每次混淆后都拥有相同的混淆结果。

## 安全编译选项

`cjc` 默认生成地址无关代码，在编译可执行文件时默认生成地址无关可执行文件。

在构建 Release 版本时，建议根据以下规则打开/关闭编译选项以提高安全性。

### 启用 `--trimpath <value>` <sup>[frontend]</sup>

从调试与异常信息中将指定的绝对路径前缀移除，使用该选项可以避免构建路径信息被写入二进制程序中。

使用该选项后，二进制中的源码路径信息通常不再完整，可能影响调试体验，建议在构建调试版本时关闭该选项。

### 启用 `--strip-all`, `-s`

移除二进制中的符号表，使用该选项可以删除运行时不需要的符号相关信息。

使用该选项后，二进制将无法调试，请在构建调试版本时关闭该选项。

### 禁用 `--set-runtime-rpath`

若可执行程序会被分发至不同环境运行，或其他普通用户对当前正在使用的仓颉运行时库目录拥有写权限，使用该选项可能导致安全风险，因此禁用该选项。

编译 Windows 目标时不涉及该选项。

### 启用 `--link-options "-z noexecstack"`<sup>1</sup>

设置线程栈不可执行。

仅编译 Linux 目标时可用。

### 启用 `--link-options "-z relro"`<sup>1</sup>

设置 GOT 表重定位只读。

仅编译 Linux 目标时可用。

### 启用 `--link-options "-z now"`<sup>1</sup>

设置立即绑定。

仅编译 Linux 目标时可用。

## 代码覆盖率插桩选项

> **注意：**
>
> Windows 和 macOS 版本目前不支持代码覆盖率插桩选项。

仓颉支持对代码覆盖率插桩（SanitizerCoverage，以下简称 SanCov），提供与 LLVM 的 SanitizerCoverage 一致的接口，编译器在函数级或 BasicBlock 级插入覆盖率反馈函数，用户只需要实现约定好的回调函数即可在运行过程中感知程序运行状态。

仓颉提供的 SanCov 功能以 package 为单位，即整个 package 只有全部插桩和全部不插桩两种情况。

### `--sanitizer-coverage-level=0/1/2`

插桩级别：

- 0 表示不插桩；
- 1 表示函数级插桩，仅在函数入口处插入回调函数；
- 2 表示 BasicBlock 级插桩，在各个 BasicBlock 处插入回调函数。

如果不指定，默认值为 2。

该编译选项仅影响 `--sanitizer-coverage-trace-pc-guard`、`--sanitizer-coverage-inline-8bit-counters` 和 `--sanitizer-coverage-inline-bool-flag` 的插桩级别。

### `--sanitizer-coverage-trace-pc-guard`

开启该选项，会在每个 Edge 插入函数调用 `__sanitizer_cov_trace_pc_guard(uint32_t *guard_variable)`，受 `sanitizer-coverage-level` 影响。

**值得注意的是**，该功能存在与 gcc/llvm 实现不一致的地方：不会在 constructor 插入 `void __sanitizer_cov_trace_pc_guard_init(uint32_t *start, uint32_t *stop)`，而是在 package 初始化阶段插入函数调用 `uint32_t *__cj_sancov_pc_guard_ctor(uint64_t edgeCount)`。

`__cj_sancov_pc_guard_ctor` 回调函数需要开发者自行实现，开启 SanCov 的 package 会尽可能早地调用该回调函数，入参是该 Package 的 Edge 个数，返回值是通常是 calloc 创建的内存区域。

如果需要调用 `__sanitizer_cov_trace_pc_guard_init`，建议在 `__cj_sancov_pc_guard_ctor` 中调用，使用动态创建的缓冲区计算该函数的入参和返回值。

一个标准的 `__cj_sancov_pc_guard_ctor` 参考实现如下：

```cpp
uint32_t *__cj_sancov_pc_guard_ctor(uint64_t edgeCount) {
    uint32_t *p = (uint32_t *) calloc(edgeCount, sizeof(uint32_t));
    __sanitizer_cov_trace_pc_guard_init(p, p + edgeCount);
    return p;
}
```

### `--sanitizer-coverage-inline-8bit-counters`

开启该选项后，会在每个 Edge 插入一个累加器，每经历过一次，该累加器加一，受 `sanitizer-coverage-level` 影响。

**值得注意的是**，该功能存在与 gcc/llvm 实现不一致的地方：不会在 constructor 插入 `void __sanitizer_cov_8bit_counters_init(char *start, char *stop)`，而是在 package 初始化阶段插入函数调用 `uint8_t *__cj_sancov_8bit_counters_ctor(uint64_t edgeCount)`。

`__cj_sancov_pc_guard_ctor` 回调函数需要开发者自行实现，开启 SanCov 的 package 会尽可能早地调用该回调函数，入参是该 Package 的 Edge 个数，返回值是通常是 calloc 创建的内存区域。

如果需要调用 `__sanitizer_cov_8bit_counters_init`，建议在 `__cj_sancov_8bit_counters_ctor` 中调用，使用动态创建的缓冲区计算该函数的入参和返回值。

一个标准的 `__cj_sancov_8bit_counters_ctor` 参考实现如下：

```cpp
uint8_t *__cj_sancov_8bit_counters_ctor(uint64_t edgeCount) {
    uint8_t *p = (uint8_t *) calloc(edgeCount, sizeof(uint8_t));
    __sanitizer_cov_8bit_counters_init(p, p + edgeCount);
    return p;
}
```

### `--sanitizer-coverage-inline-bool-flag`

开启该选项后，会在每个 Edge 插入布尔值，经历过的 Edge 对应的布尔值会被设置为 True，受 `sanitizer-coverage-level` 影响。

**值得注意的是**，该功能存在与 gcc/llvm 实现不一致的地方：不会在 constructor 插入 `void __sanitizer_cov_bool_flag_init(bool *start, bool *stop)`，而是在 package 初始化阶段插入函数调用 `bool *__cj_sancov_bool_flag_ctor(uint64_t edgeCount)`。

`__cj_sancov_bool_flag_ctor` 回调函数需要开发者自行实现，开启 SanCov 的 package 会尽可能早地调用该回调函数，入参是该 Package 的 Edge 个数，返回值是通常是 calloc 创建的内存区域。

如果需要调用 `__sanitizer_cov_bool_flag_init`，建议在 `__cj_sancov_bool_flag_ctor` 中调用，使用动态创建的缓冲区计算该函数的入参和返回值。

一个标准的 `__cj_sancov_bool_flag_ctor` 参考实现如下：

```cpp
bool *__cj_sancov_bool_flag_ctor(uint64_t edgeCount) {
    bool *p = (bool *) calloc(edgeCount, sizeof(bool));
    __sanitizer_cov_bool_flag_init(p, p + edgeCount);
    return p;
}
```

### `--sanitizer-coverage-pc-table`

该编译选项用于提供插桩点和源码之间的对应关系，当前只提供精确到函数级的对应关系。需要与 `--sanitizer-coverage-trace-pc-guard`、`--sanitizer-coverage-inline-8bit-counters`、`--sanitizer-coverage-inline-bool-flag` 共用，至少需要开启其中一项，可以同时开启多项。

**值得注意的是**，该功能存在与 gcc/llvm 实现不一致的地方：不会在 constructor 插入 `void __sanitizer_cov_pcs_init(const uintptr_t *pcs_beg, const uintptr_t *pcs_end);`，而是在 package 初始化阶段插入函数调用 `void __cj_sancov_pcs_init(int8_t *packageName, uint64_t n, int8_t **funcNameTable, int8_t **fileNameTable, uint64_t *lineNumberTable)`，各入参含义如下：

- `int8_t *packageName`: 字符串，表示包名（插桩用 c 风格的 int8 数组作为入参来表达字符串，下同）。
- `uint64_t n`: 共有 n 个函数被插桩。
- `int8_t **funcNameTable`: 长度为 n 的字符串数组，第 i 个插桩点对应的函数名为 funcNameTable\[i\]。
- `int8_t **fileNameTable`: 长度为 n 的字符串数组，第 i 个插桩点对应的文件名为 fileNameTable\[i\]。
- `uint64_t *lineNumberTable`: 长度为 n 的 uint64 数组，第 i 个插桩点对应的行号为 lineNumberTable\[i\]。

如果需要调用 `__sanitizer_cov_pcs_init`，需要自行完成仓颉 pc-table 到 C 语言 pc-table 的转化。

### `--sanitizer-coverage-stack-depth`

开启该编译选项后，由于仓颉无法获取 SP 指针的值，因此只能在每个函数入口处插入调用 `__updateSancovStackDepth`，在 C 侧实现该函数即可获得 SP 指针。

一个标准的 `updateSancovStackDepth` 实现如下：

```cpp
thread_local void* __sancov_lowest_stack;

void __updateSancovStackDepth()
{
    register void* sp = __builtin_frame_address(0);
    if (sp < __sancov_lowest_stack) {
        __sancov_lowest_stack = sp;
    }
}
```

### `--sanitizer-coverage-trace-compares`

开启该选项后，会在所有的 compare 指令和 match 指令调用前插入函数回调函数，具体列表如下，与 LLVM 系的 API 功能一致。参考 Tracing data flow。

```cpp
void __sanitizer_cov_trace_cmp1(uint8_t Arg1, uint8_t Arg2);
void __sanitizer_cov_trace_const_cmp1(uint8_t Arg1, uint8_t Arg2);
void __sanitizer_cov_trace_cmp2(uint16_t Arg1, uint16_t Arg2);
void __sanitizer_cov_trace_const_cmp2(uint16_t Arg1, uint16_t Arg2);
void __sanitizer_cov_trace_cmp4(uint32_t Arg1, uint32_t Arg2);
void __sanitizer_cov_trace_const_cmp4(uint32_t Arg1, uint32_t Arg2);
void __sanitizer_cov_trace_cmp8(uint64_t Arg1, uint64_t Arg2);
void __sanitizer_cov_trace_const_cmp8(uint64_t Arg1, uint64_t Arg2);
void __sanitizer_cov_trace_switch(uint64_t Val, uint64_t *Cases);
```

### `--sanitizer-coverage-trace-memcmp`

该编译选项用于在 String 、 Array 等比较中反馈前缀比较信息。开启该选项后，会对 String 和 Array 的比较函数前插入函数回调函数。具体对于以下对各 String 和 Array 的 API，分别插入对应桩函数：

- String==: __sanitizer_weak_hook_memcmp
- String.startsWith: __sanitizer_weak_hook_memcmp
- String.endsWith: __sanitizer_weak_hook_memcmp
- String.indexOf: __sanitizer_weak_hook_strstr
- String.replace: __sanitizer_weak_hook_strstr
- String.contains: __sanitizer_weak_hook_strstr
- CString==: __sanitizer_weak_hook_strcmp
- CString.startswith: __sanitizer_weak_hook_memcmp
- CString.endswith: __sanitizer_weak_hook_strncmp
- CString.compare: __sanitizer_weak_hook_strcmp
- CString.equalsLower: __sanitizer_weak_hook_strcasecmp
- Array==: __sanitizer_weak_hook_memcmp
- ArrayList==: __sanitizer_weak_hook_memcmp

## 实验性功能选项

### `--enable-eh` <sup>[frontend]</sup>

启用该选项后，仓颉将支持效应处理器（Effect Handlers），Effect Handlers 是一种先进的控制流机制，用于实现模块化、可恢复的副作用处理。

Effect Handler 允许程序员将副作用操作与其处理逻辑解耦，从而编写出更清晰、更具可组合性的代码。这种机制有助于提高抽象层次，尤其适用于处理日志记录、输入输出、状态变更等操作，从而避免主流程被副作用逻辑污染。

效应的工作机制类似异常处理，但不使用 `throw` 和 `catch`，而是通过 `perform` 执行效应，使用 `handle` 进行捕获与处理。每个效应需通过继承 `stdx.effect.Command` 类来定义。

与传统异常机制不同，Effect Handler 在处理效应后可以选择 恢复执行（`resume`），即向原始调用点注入一个值并继续运行。这种“恢复”能力使得程序员可以对控制流进行更精细的操作，特别适合用于构建模拟器、解释器或协作式多任务系统等需要高度控制的场景。

示例：

```cangjie
import stdx.effect.Command

// 定义一个名为 GetNumber 的 Command
class GetNumber <: Command<Int64> {}

main() {
    try {
        println("About to perform")

        // 执行 GetNumber 效应
        let a = perform GetNumber()

        // handler 恢复后将从此处继续执行
        println("It is resumed, a = ${a}")
    } handle(e: GetNumber) {
        // 处理 GetNumber 效应
        println("It is performed")

        // 恢复执行，并注入值 9
        resume with 9
    }
    0
}
```

在上述示例中，定义了一个新的 `Command` 的子类 `GetNumber`。

- 在 `main` 函数中，使用 `try-handle` 结构来处理该效应。
- 在 `try` 块中，首先打印一行提示信息（`"About to perform"`），然后使用 `perform GetNumber()` 执行效应，`perform` 表达式的返回值会被赋给变量 `a`，执行一个效应会将执行流跳转到捕获这个效应的 `handle` 块。
- 在 `handle` 块中，捕获并处理 `GetNumber` 效应，先打印一条信息（`"It is performed"`），然后使用 `resume with 9` 将常数 `9` 注入回原始调用点，然后恢复 `perform`  之后的执行流，打印（`"It is resumed, a = 9"`）。

输出结果如下：

```shell
About to perform
It is performed
It is resumed, a = 9
```

> **注意：**
>
> - Effect Handler 当前仍属于实验性特性，该选项可能在未来版本中发生变化，请谨慎使用。
> - 使用 Effect Handler 需引入 `stdx.effect` 库。

### `--experimental` <sup>[frontend]</sup>

启用实验性功能，允许在命令行使用其他实验性功能选项。

> **注意：**
>
> 使用实验性功能生成的二进制文件可能存在潜在的运行时问题，请注意使用该选项的风险。

## 编译插件选项

### `--plugin <value>` <sup>[frontend]</sup>

提供编译器插件能力，但作为实验特性，仅做内部验证，暂不支持开发者自定义插件使用，否则可能报错。

## 其他功能

### 编译器报错信息显示颜色

对于 Windows 版本的仓颉编译器，仅在运行于 Windows 10 version 1511 (Build 10586) 或更高版本的系统时，编译器报错信息才会显示颜色，否则不显示颜色。

### 设置 build-id

通过 `--link-options "--build-id=<arg>"`<sup>1</sup> 可以透传链接器选项以设置 build-id。

编译 Windows 目标时不支持此功能。

### 设置 rpath

通过 `--link-options "-rpath=<arg>"`<sup>1</sup> 可以透传链接器选项以设置 rpath。

编译 Windows 目标时不支持此功能。

### 增量编译

通过 `--incremental-compile` <sup>[frontend]</sup> 开启增量编译。开启后，`cjc`会在编译时根据前次编译的缓存文件加快此次编译的速度。

> **注意：**
>
> 该选项为实验性功能，使用该功能生成的二进制有可能会存在潜在的运行时问题，请注意使用该选项的风险。此选项必须配合 `--experimental` 选项一同使用。
> 指定此选项时会保存增量编译缓存及日志到输出文件路径下的 `.cached`目录。

### 输出 CHIR

通过 `--emit-chir=[raw|opt]` <sup>[frontend]</sup> 指定输出 CHIR 编译阶段的序列化产物，`raw` 输出编译器优化前的 CHIR，`opt` 输出编译器优化后的 CHIR。使用 `--emit-chir` 则默认输出编译器优化后的 CHIR。

### `--no-prelude` <sup>[frontend]</sup>

关闭标准库 core 包自动导入功能。

> **注意：**
>
> 该选项仅能用于编译仓颉标准库 core 包，不能用于编译其他仓颉代码的场景。

### 打印 AST

可通过 `--dump-ast` <sup>[frontend]</sup> 打印 AST。默认输出到文件，产物目录会创建以包名（或使用 `-o` 指定的产物名）命名的 *_AST 目录，文件命名为 `编号_阶段名称_ast.txt`。加上 `--dump-to-screen` <sup>[frontend]</sup> 可输出到屏幕。

### 打印 CHIR

可通过 `--dump-chir` <sup>[frontend]</sup> 打印 CHIR。默认输出到文件，产物目录会创建以包名（或使用 `-o` 指定的产物名）命名的 *_CHIR 目录，文件命名为 `编号_阶段名称.chirtxt`。加上 `--dump-to-screen` <sup>[frontend]</sup> 可输出到屏幕。

### 打印 LLVM IR

可通过 `--dump-ir` <sup>[frontend]</sup> 打印 LLVM IR。默认输出到文件，产物目录会创建以包名（或使用 `-o` 指定的产物名）命名的 *_IR 目录并在 *_IR 目录下创建 `编号_阶段名称` 子文件夹，文件名为 `子模块编号-包名.ll`，子模块的编号和数量与编译并发度相关。加上 `--dump-to-screen` <sup>[frontend]</sup> 可输出到屏幕。

### 打印 AST, CHIR, LLVM IR

可通过 `--dump-all` <sup>[frontend]</sup> 打印 AST, CHIR, LLVM IR。默认输出到文件，产物目录会创建以包名（或使用 `-o` 指定的产物名）命名的 *_AST, *_CHIR, *_IR 目录。加上 `--dump-to-screen` <sup>[frontend]</sup> 可输出到屏幕。

### 将 dump 内容打印到屏幕上

可通过 `--dump-to-screen` <sup>[frontend]</sup> 配合前端相关的转储选项（如 `--dump-ast` <sup>[frontend]</sup>， `--dump-chir` <sup>[frontend]</sup>, `--dump-ir` <sup>[frontend]</sup> 和 `--dump-all` <sup>[frontend]</sup>）将相应的中间表示文本内容打印到屏幕上。

> **注意：**
>
> 输出到屏幕时仅显示最终结果；输出到文件时会在产物目录下创建以 `_AST`, `_CHIR`, `_IR` 为后缀的目录，用以保存中间过程的详细信息。

## `cjc` 用到的环境变量

这里介绍一些仓颉编译器在编译代码的过程中可能使用到的环境变量。

### `TMPDIR` 或者 `TMP`

仓颉编译器会将编译过程中生成的临时文件放置在临时目录中。默认情况下，`Linux` 和 `macOS` 操作系统会将其放在 `/tmp` 目录下，而 `Windows` 操作系统则会将其放在 `C:\Windows\Temp` 目录下。仓颉编译器还支持自定义临时文件存放目录，在 `Linux` 和 `macOS` 操作系统上，可以通过设置环境变量 `TMPDIR` 来更改临时文件目录，而在 `Windows` 操作系统上，则可以通过设置环境变量 `TMP` 来更改临时文件目录。

例如：
在 Linux shell 中

```shell
export TMPDIR=/home/xxxx
```

在 Windows cmd 中

```shell
set TMP=D:\\xxxx
```
