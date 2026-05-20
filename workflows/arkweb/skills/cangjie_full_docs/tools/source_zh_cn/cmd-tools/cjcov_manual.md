# 覆盖率统计工具

## 功能简介

`cjcov`（Cangjie Coverage）是一款面向仓颉语言的覆盖率统计工具，用于生成仓颉语言程序的覆盖率报告。

## 使用说明

`cjcov -h` 获取帮助信息，选项介绍如下：

```text
Usage: cjcov [options]

A tool used to summarize the coverage in html reports.

Options:
  -v, --version                 Print the version number, then exit.
  -h, --help                    Show this help message, then exit.
  -r ROOT, --root=ROOT          The root directories of your source files, defaults to '.', the current directory.
                                File names are reported relative to this root.
  -o OUTPUT, --output=OUTPUT    The output directories of html reports, defaults to '.', the current directory.
  -b, --branches                Report the branch coverage. (It is an experimental feature and may generate imprecise branch coverage.)
  --verbose                     Print some detail messages, including parsing data for the gcov file.
  --html-details                Generate html reports for each source file.
  -x, --xml                     Generate a xml report.
  -j, --json                    Generate a json report.
  -k, --keep                    Keep gcov files after processing.
  -s SOURCE, --source=SOURCE    The directories of cangjie source files.
  -e EXCLUDE, --exclude=EXCLUDE
                                The cangjie source files starts with EXCLUDE will not be showed in coverage reports.
  -i INCLUDE, --include=INCLUDE
                                The cangjie source files starts with INCLUDE will be showed in coverage reports.
```

基本的命令使用方法如下所示，`cjcov` 为主程序名称，`--version` 表示为显示 `cjcov` 的版本号。部分配置项支持长短选项两种写法，效果相同，具体可以使用 `cjcov --help` 命令参考用法。

```text
cjcov -version 或者 cjcov -v
```

### 使用步骤

#### 单文件场景

仓颉版本包准备 --> 仓颉源码准备 -->  使用 `--coverage` 编译选项构建仓颉源码，生成二进制文件 --> 执行二进制文件 --> `cjcov` 生成覆盖率统计结果

以 `hello world` 为例（假设当前目录是 `WORKPATH`）：

1. 仓颉版本包准备

    对于 `Linux` 平台，假设仓颉版本包解压在 `WORKPATH` 目录下，则执行 `source WORKPATH/cangjie/envsetup.sh` 命令即可。

2. 仓颉源码准备

    源码目录结构如下：

    ```text
    src/
    └── main.cj
    ```

    `main.cj` 源码内容如下：

    <!-- compile -->

    ```cangjie
    main(): Int64 {
        print("hello world\n")
        return 0
    }
    ```

3. 编译源码

    在 `WORKPATH` 目录下执行以下命令：

    ```shell
    cjc --coverage main.cj
    ```

    编译完成之后在 `WORKPATH` 目录下会生成 `default.gcno` 和 `main` 文件。

4. 运行编译出来的二进制

    在 `WORKPATH` 目录下执行 `./main` 命令，运行完成之后 `WORKPATH` 目录下会生成 `default.gcda` 文件。

5. `cjcov` 生成 `html`

    在 `WORKPATH` 目录执行 `cjcov -o output --html-details`，更多 `cjcov` 参数使用可参考[命令说明](#命令说明)章节。

执行完 `cjcov` 命令之后，在 `WORKPATH/output` 目录会有以下文件：

```text
output
├── cjcov_logs （该目录存放一些 cjcov 执行过程的详细日志，可不用关注）
│   ├── cjcov.log
│   └── gcov_parse.log
├── index.html （总的覆盖率报告，通过浏览器打开）
└── src_main.cj.html （单个文件的覆盖率，可以通过打开 index.html 自动跳转到该文件）
```

#### 多文件场景

对于多文件场景，推荐使用项目管理工具的命令`cjpm build --coverage` 或 `cjpm test --coverage`，具体用法请参见[项目管理工具](./cjpm_manual.md)。

## 命令说明

### cjcov -h | --help

显示 `cjcov` 基本使用方法。

### cjcov -v | --version

显示 `cjcov` 的版本号。指定 `-v` 或者 `--version` 参数后，输入其他任何选项参数都不生效，只会显示版本号。如 `--version` 和 `--help` 同时使用，则显示版本号信息后退出。

### cjcov --verbose

指定该选项后会将一些日志信息生成到 `cjcov_logs` 目录中，该参数默认不生效，即默认不会打印中间信息。`gcov` 文件是 `cjcov` 工具生成的中间文件，`cjcov` 解析 `gcov` 文件的格式如下：

```text
==================== start: main.cj.gcov =====================

noncode line numbers:
[0, 0, 0, 0, 1, 2, 6, 7, 9, 10, 11, 15, 17, 18]

uncovered line numbers:
[5]

covered data:
[(16, 1), (3, 1), (4, 1), (8, 1), (12, 1), (13, 1), (14, 1)]

branches data:
line number:    4  ==>  data: [(0, 0), (1, 1)]

===================== end: main.cj.gcov =======================

```

指定该选项参数，会显示每个 `gcov` 文件的详细覆盖率数据。

具体字段解释如下：

- `start: xxx.gcov, end: xxx.gcov`：两行中间的文本是对应 `xxx.gcov` 文件解析到的覆盖率数据。
- `noncode line numbers`：显示的是不统计到总代码行的行号，在 `html` 中是以白色底呈现，对应 `gcov` 中的以 `-` 开头的行数。
- `uncovered line numbers`：显示的是没有覆盖到的数据，在 `html` 中是以红色底呈现，对应 `gcov` 文件中以 `#####` 开头的行数。
- `covered data`：显示的是覆盖到的数据，以（代码行数, 覆盖次数）呈现，在对应 `html` 中以绿色呈现，只要覆盖次数大于 0，在 `html` 中的 `Exec` 一列中显示为 `Y`，对应于 `gcov` 文件以数字开头的行数。
- `branches data`：显示的分支覆盖数据，以（代码行数, 分支覆盖次数）呈现，在对应 `html` 中的 `Branch` 一列中，有一个倒三角形，显示的是分支覆盖数/总分支数。该数据对应于 `gcov` 文件中以 `branch` 开头的数据。

### cjcov --html-details

如果指定该参数，表示会生成源代码文件对应的 `html` 覆盖报告。在总的 `index` 文件里面会有每个子 `html` 的索引。子 `html` 文件和 `index.html` 放在同一个目录。

子 `html` 文件名由目录名和文件名通过下划线拼接而成。例如，源文件为 `src/main.cj` 时，生成的 `html` 文件名为 `src_main.cj.html`。如果源文件路径包含特殊字符，这些字符将被替换为 `=`。有关详细信息，请参见[文件名包含特殊字符](#文件名包含特殊字符)章节。

如果没有指定该参数，表示不会生成子 `html`。在总的 `index` 文件里面会显示每个子 `html` 的覆盖率数据，但是不能跳转到对应的子 `html` 文件。

该参数默认不生效。即默认只会生成一个 `index.html`, 不会生成子 `html` 文件。

### cjcov -x | --xml

如果指定该参数，则会在指定输出路径生成 `coverage.xml` 文件，`coverage.xml` 记录的是所有文件的覆盖率数据。

### cjcov -j | --json

如果指定该参数，则会在指定输出路径生成 `coverage.json` 文件，`coverage.json` 记录的是所有文件的覆盖率数据。

### cjcov -k |  --keep

指定该参数后则会保留生成的 `gcov` 中间文件。如果保留这些文件，后续测试运行时会重复计算覆盖率数据，可能导致最终覆盖率结果不准确。

默认该参数不生效，即默认会删除 `gcov` 中间文件。

### cjcov -b | --branches

指定该参数后则会生成分支覆盖率信息。

默认该参数不生效，即默认不生成分支的覆盖率信息，此时在 `html` 报告中的分支覆盖率数据百分比显示为 `-`。

### cjcov -r ROOT | --root=ROOT

该参数指定的 `ROOT` 参数表示在 `ROOT` 目录或其递归子目录中查找 `gcda` 文件。`gcda` 和 `gcno` 文件默认会生成在一起，请不要手动将 `gcda` 文件和 `gcno` 文件分开存放，否则可能导致程序无法运行。

参数指定的 `ROOT` 目录如果不存在，`cjcov` 工具会有报错提示。

不指定该参数，默认会以当前目录为 `ROOT` 目录。

### cjcov -o OUTPUT |  --output=OUTPUT

该参数指定的 `OUTPUT` 参数，表示 `html` 覆盖率报告的输出路径。

如果 `OUTPUT` 目录及其父目录均不存在，`cjcov` 工具将显示错误提示。若 `OUTPUT` 目录不存在但其父目录存在，`cjcov` 工具将自动创建 `OUTPUT` 目录。

不指定该参数，默认会以当前目录为 `OUTPUT` 目录来存放 `html` 文件。

### -s SOURCE | --source=SOURCE

该参数指定的 `SOURCE` 参数，表示仓颉源文件的代码路径，`html` 总覆盖率报告 `index.html` 会有各个源文件的索引，这些文件路径记录的是一个相对路径。如果指定 `-s SOURCE |--source SOURCE` 参数，优先以 `SOURCE` 路径列表中的路径作为相对路径的参考路径，如果没有指定该参数，则以 `-r ROOT | --root=ROOT` 作为相对路径的参考路径，如果都没有指定，则以当前路径作为相对路径的参考路径。

示例：

仓颉代码目录结构如下：

```text
/work/cangjie/tests/API/test01/src/1.cj
/work/cangjie/tests/API/test01/src/2.cj
/work/cangjie/tests/cjnative/test02/src/3.cj
/work/cangjie-tools/tests/cjnative/test01/src/4.cj
/work/cangjie-tools/tests/cjnative/test02/src/5.cj
```

1. 在 `/work` 目录执行命令：

    ```shell
    cjcov --root=./ -s "/work/cangjie /work/cangjie-tools/tests" --html-details --output=html_output
    ```

    最后 html 中呈现的源文件相对路径是：

    ```text
    tests/API/test01/src/1.cj
    tests/API/test01/src/2.cj
    tests/cjnative/test02/src/3.cj
    cjnative/test01/src/4.cj
    cjnative/test02/src/5.cj
    ```

2. 在 `/work` 目录执行命令, 没有指定 `--root` 参数和 `--source` 参数，默认当前所在路径为相对路径的参考路径，执行命令如下：

    ```shell
    cjcov --html-details --output=html_output
    ```

    最后 html 中呈现的源文件相对路径是：

    ```text
    cangjie/tests/API/test01/src/1.cj
    cangjie/tests/API/test01/src/2.cj
    cangjie/tests/cjnative/test02/src/3.cj
    cangjie-tools/tests/cjnative/test01/src/4.cj
    cangjie-tools/tests/cjnative/test02/src/5.cj
    ```

### -e EXCLUDE | --exclude=EXCLUDE

该参数指定的 `EXCLUDE` 参数，表示不需要生成覆盖率信息的源文件列表，支持指定目录和文件。

示例：

仓颉代码目录结构如下：

```text
/usr1/cangjie/tests/API/test01/src/1.cj
/usr1/cangjie/tests/API/test01/src/2.cj
/usr1/cangjie/tests/cjnative/test02/src/3.cj
/usr1/cangjie-tools/tests/cjnative/test01/src/4.cj
/usr1/cangjie-tools/tests/cjnative/test02/src/5.cj
```

在 `/usr1` 目录执行命令：

```shell
cjcov --root=./ -s "/usr1/cangjie" -e "/usr1/cangjie-tools/tests/cjnative" --html-details --output=html_output
```

在生成的 HTML 报告中，源文件的相对路径会被呈现，但以 `/usr1/cangjie-tools/tests/cjnative` 开头的路径不会出现在文件列表中。

```text
tests/API/test01/src/1.cj
tests/API/test01/src/2.cj
tests/cjnative/test02/src/3.cj
```

### -i INCLUDE | --include=INCLUDE

该参数指定的 `INCLUDE` 参数，表示以 `INCLUDE` 开头的文件会显示在 `index.html` 的文件列表中，支持指定目录和文件。如果 `-e | --exclude` 和 `-i | --include` 指定的参数有路径重复，会有报错提示。

示例：

仓颉代码目录 `/usr1/cangjie/tests` 结构如下：

```text
├── API
│   └── test01
│       └── src
│           ├── 1.cj
│           └── 2.cj
└── cjnative
    └── test02
        └── src
            └── 3.cj
```

在 `/usr1` 目录执行命令, 其中 `-i` 参数表示需要体现在覆盖率报告 `index.html` 的文件，命令如下：

```shell
cjcov --root=./ -s "/usr1/cangjie" -i "/usr1/cangjie/tests/API/test01/src/1.cj /usr1/cangjie/tests/cjnative/test02" --html-details --output=html_output
```

上面命令执行后, 在 `index.html` 中文件路径列表如下(`tests/API/test01/src/2.cj` 不在 `-i` 参数指定的列表里面，所以不会出现在 `html` 的文件列表中):

```text
tests/API/test01/src/1.cj
tests/cjnative/test02/src/3.cj
```

## 特殊场景

### 二进制无法正常执行结束

对于常驻的网络服务程序无法正常结束二进制文件并生成 `gcda` 覆盖率数据的场景，需要手动执行退出脚本生成 `gcda` 覆盖率数据。

1）将以下脚本内容保存为 `stop.sh`（此脚本执行依赖 `gdb`）

```shell
#!/bin/sh
SERVER_NAME=$1

pid=`ps -ef | grep $SERVER_NAME | grep -v "grep" | awk '{print $2}'`
echo $pid
gdb -q attach $pid <<__EOF__
p exit(0)
__EOF__
```

2）常驻服务程序完成业务逻辑操作覆盖后，执行 `stop.sh {service_name}`，如通过 `./main` 启动常驻服务进程，通过如下方式停止进程产生 `gcda` 数据

```shell
sh stop.sh ./main
```

### 文件名包含特殊字符

`cjcov` 在 Windows 平台不支持源码文件名包含中文字符的场景。

建议遵循仓颉编程规范命名文件，不建议包含除 [0-9a-zA-Z_] 之外的字符，特殊字符会被替换成 `=`。

如果文件名有特殊字符，为保证 `html` 跳转正确，`index.html` 中呈现的 `html` 名字和 `html` 本身文件名会不一致，`html` 文件名的特殊字符都会被替换成 `=`。

示例如下：

代码结构：

```text
src
├── 1file#.cj
├── file10_abc.cj
├── file11_.aaa-bbb.cj
├── file12!#aaa!bbb.cj
├── file13~####.cj
├── file14*aa.cj
├── file15`.cj
├── file16(#).cj
├── file2;aa.cj
├── file3,?.cj
├── file4@###.cj
├── file5&cc.cj
├── file6=.cj
├── file7+=.cj
├── file8$.cj
├── file9-aaa.cj
└── main.cj
```

生成 html 文件名，其中除了 `[0-9a-zA-Z_.=]` 之外，其他特殊字符都被替换成了 `'='`：

```text
.
├── index.html
├── src_1file=.cj.html
├── src_file10_abc.cj.html
├── src_file11_.aaa=bbb.cj.html
├── src_file12==aaa=bbb.cj.html
├── src_file13=####.cj.html
├── src_file14=aa.cj.html
├── src_file15=.cj.html
├── src_file16===.cj.html
├── src_file2=aa.cj.html
├── src_file3==.cj.html
├── src_file4=###.cj.html
├── src_file5=cc.cj.html
├── src_file6=.cj.html
├── src_file7==.cj.html
├── src_file8=.cj.html
├── src_file9=aaa.cj.html
└── src_main.cj.html
```

### 分支覆盖率功能

分支覆盖率是一个试验阶段的功能，会出现分支覆盖率数据不准确的情况。

目前已知会出现分支覆盖率数据不准确的场景包含以下几种表达式：

- `try-catch-finally` 表达式
- 循环表达式（包括 `for` 表达式、`while` 表达式）
- `if-else` 表达式

### 部分代码未记录到行覆盖率数据中

部分代码不会记录到行覆盖率数据中，属于正常情况。整体而言，如果一行代码*仅包含定义、声明*而没有实际的可执行代码，那么这一行代码不会被统计到覆盖率中。目前已知不会统计的场景有：

- 全局变量的定义，示例如下：

    <!-- compile -->

    ```cangjie
    let HIGH_1_UInt8: UInt8 = 0b10000000;
    ```

- 成员变量仅声明未初始化赋值，示例如下：

    <!-- code_no_check -->

    ```cangjie
    public class StringBuilder <: Collection & ToString {
        private var myData: Array
        private var mySize: Int64
        private var endIndex: Int64
    }
    ```

- 仅有函数声明未包含函数体（包括 `foreign` 函数等），示例如下：

    <!-- code_no_check -->

    ```cangjie
    foreign func cj_core_free(p: CPointer): Unit
    ```

- 枚举类型定义，示例如下：

    <!-- compile -->

    ```cangjie
    enum Numeric {
        NumDay | NumYearDay | NumYearWeek | NumHour12 | NumHour24 | NumMinute | NumSecond
    }
    ```

- class、extend 等定义，其中 extend 和 class 所在的一行不会记录到覆盖率数据中，示例如下：

    <!-- code_no_check -->

    ```cangjie
    extend Int8 <: Formatter { // This line wil not account for the coverage.
      ...
    }

    public class StringBuilder <: Collection & ToString { // This line will not account for the coverage.
       ...
    }
    ```

### 源代码中的 `main` 函数未被覆盖

**原因：** 使用 `cjc --test` 编译，仓颉测试框架会生成一个新的 `main` 作为程序入口，源代码中的 `main` 不再作为程序入口并且不会被执行。

**建议：** 在使用 `cjc --test` 之后，建议不用再手写多余的 `main`。

## FAQ

### 报错找不到 `llvm-cov` 命令

**解决方法：**

方法 1：设置 `CANGJIE_HOME` 环境变量，`cjcov` 可通过 `CANGJIE_HOME` 环境变量找到 `llvm-cov` 命令，设置方法如下：
假设 `which cjc` 显示 `/work/cangjie/bin/cjc`, 并且 `/work/cangjie/third_party/llvm/bin` 和 `/work/cangjie/third_party/llvm/lib` 目录都存在，则可设置：

```shell
export CANGJIE_HOME=/work/cangjie
```

方法 2：在 `/root/.bashrc` 里面直接设置环境变量，如 `cjc` 放在 `/work/cangjie/bin/cjc` 目录下，则设置方法如下：

```shell
export PATH=/work/cangjie/third_party/llvm/bin:$PATH
export LIBRARY_PATH=/work/cangjie/third_party/llvm/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/work/cangjie/third_party/llvm/lib:$LD_LIBRARY_PATH
```

方法 3：手动安装 `llvm-cov` 命令，如 `ubuntu` 上可执行命令：

```shell
apt install llvm-cov
```

### 出现 VirtualMachineError OutOfMemoryError

**问题现象：**

```text
An exception has occurred:
Error VirtualMachineError OutOfMemoryError
```

**解决方法：** 仓颉默认规格  stack 1MB，heap 256 MB，建议根据文件数量大小将堆内存调到合适的大小。通常 2GB 的内存能够满足大多数情况，如果不够用则根据具体情况再增加内存大小。

示例：

```text
把堆内存扩大到2GB：
export cjHeapSize=2GB
```
