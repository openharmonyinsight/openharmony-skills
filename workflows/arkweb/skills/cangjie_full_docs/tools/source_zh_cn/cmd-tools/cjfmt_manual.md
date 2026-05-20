# 格式化工具

## 功能简介

`CJFMT(Cangjie Formatter)` 仓颉格式化工具是一款基于仓颉语言编程规范开发的代码自动格式化工具。

## 使用说明

使用命令行操作 `cjfmt [option] file [option] file`

`cjfmt -h` 帮助信息，选项介绍

```text
Usage:
     cjfmt -f fileName [-o fileName] [-l start:end]
     cjfmt -d fileDir [-o fileDir]
Options:
   -h            Show usage
                     eg: cjfmt -h
   -v            Show version
                     eg: cjfmt -v
   -f            Specifies the file in the required format. The value can be a relative path or an absolute path.
                     eg: cjfmt -f test.cj
   -d            Specifies the file directory in the required format. The value can be a relative path or an absolute path.
                     eg: cjfmt -d test/
   -o <value>    Output. If a single file is formatted, '-o' is followed by the file name. Relative and absolute paths are supported;
                 If a file in the file directory is formatted, a path must be added after -o. The path can be a relative path or an absolute path.
                     eg: cjfmt -f a.cj -o ./fmta.cj
                     eg: cjfmt -d ~/testsrc -o ./testout
   -c <value>    Specify the format configuration file, relative and absolute paths are supported.
                 If the specified configuration file fails to be read, cjfmt will try to read the default configuration file in CANGJIE_HOME.
                 If the default configuration file also fails to be read, will use the built-in configuration.
                     eg: cjfmt -f a.cj -c ./config/cangjie-format.toml
                     eg: cjfmt -d ~/testsrc -c ~/home/project/config/cangjie-format.toml
   -l <region>   Only format lines in the specified region for the provided file. Only valid if a single file was specified.
                 Region has a format of [start:end] where 'start' and 'end' are integer numbers representing first and last lines to be formated in the specified file.
                 Line count starts with 1.
                     eg: cjfmt -f a.cj -o ./fmta.cj -l 1:25
```

### 文件格式化

`cjfmt -f`

- 格式化并覆盖源文件，支持相对路径和绝对路径。

```shell
cjfmt -f ../../../test/uilang/Thread.cj
```

- 选项 `-o` 新建一个 `.cj` 文件导出格式化后的代码，源文件和输出文件支持相对路径和绝对路径。

```shell
cjfmt -f ../../../test/uilang/Thread.cj -o ../../../test/formated/Thread.cj
```

### 目录格式化

`cjfmt -d`

- 选项 `-d` 让开发者指定扫描仓颉源代码目录，对文件夹下的仓颉源码格式化，支持相对路径和绝对路径。

```shell
cjfmt -d test/              # 源文件目录为相对目录

cjfmt -d /home/xxx/test     # 源文件目录为绝对目录
```

- 选项 `-o` 为输出目录，可以是已存在的路径，若不存在则会创建相关的目录结构，支持相对路径和绝对路径；目录的最大长度 MAX_PATH 不同的系统之间存在差异，如 `Windows` 上这个值一般不能超过 260；在 `Linux` 上这个值一般建议不能超过 4096。

```shell
cjfmt -d test/ -o /home/xxx/testout

cjfmt -d /home/xxx/test -o ../testout/

cjfmt -d testsrc/ -o /home/../testout   # 源文件文件夹testsrc/不存在；报错：error: Source file path not exist!
```

### 格式化配置文件

`cjfmt -c`

- 选项 `-c` 允许开发者指定客制化的格式化工具配置文件。

```shell
cjfmt -f a.cj -c ./cangjie-format.toml
```

默认 cangjie-format.toml 所含配置文件如下，其值也为 `cjfmt` 工具内置配置选项的值：

```toml
# indent width
indentWidth = 4 # Range of indentWidth: [0, 8]

# limit length
linelimitLength = 120 # Range of indentWidth: [1, 120]

# line break type
lineBreakType = "LF" # "LF" or "CRLF"

# allow Multi-line Method Chain when it's level equal or greater than multipleLineMethodChainLevel
allowMultiLineMethodChain = false

# if allowMultiLineMethodChain's value is true,
# and method chain's level is equal or greater than multipleLineMethodChainLevel,
# method chain will be formatted to multi-line method chain.
# e.g. A.b().c() level is 2, A.b().c().d() level is 3
# ObjectA.b().c().d().e().f() =>
# ObjectA
#     .b()
#     .c()
#     .d()
#     .e()
#     .f()
multipleLineMethodChainLevel = 5 # Range of multipleLineMethodChainLevel: [2, 10]

# allow Multi-line Method Chain when it's length greater than linelimitLength
multipleLineMethodChainOverLineLength = true
```

> **说明：**
>
> 若客制化的格式化工具配置文件读取失败，则读取 CANGJIE_HOME 环境下的默认格式化工具配置文件 `cangjie-format.toml`。
> CANGJIE_HOME 环境下的默认格式化工具配置文件路径为 `CANGJIE_HOME/tools/config` 。
> 若 CANGJIE_HOME 内置的默认格式化工具配置文件 `cangjie-format.toml` 同样读取失败，则使用 `cjfmt` 内置格式化配置选项。
> 若格式化工具配置文件中的某个配置选项读取失败，则该配置选项使用 `cjfmt` 内置格式化配置选项。

### 片段格式化

`cjfmt -l`

- 选项 `-l` 允许开发者指定应格式化文件的某一部分进行格式化，格式化程序将仅对提供的行范围内的源代码应用规则。
- `-l` 选项仅适用于格式化单个文件（选项 `-f`）。如果指定了目录（选项 `-d`），则 `-l` 选项无效。

```shell
cjfmt -f a.cj -o b.cj -l 10:25 // 仅格式化第10行至第25行
```

## 格式化规则

- 一个源文件按顺序包含版权、package、import、顶层元素，且用空行分隔。

【正例】

```cangjie
// 第一部分，版权信息
/*
 * Copyright (c) [Year of First Pubication]-[Year of Latest Update]. [Company Name]. All rights reserved.
 */

// 第二部分，package 声明
package com.myproduct.mymodule

// 第三部分，import 声明
import std.collection.HashMap   // 标准库

// 第四部分，public 元素定义
public class ListItem <: Component {
    // CODE
}

// 第五部分，internal 元素定义
class Helper {
    // CODE
}
```

> **说明：**
>
> 仓颉格式化工具不会强制用空行将版权信息部分与其他部分分隔，若开发者在版权信息下方留有一个或多个空行，则格式化工具会保留一个空行。

- 采用一致的空格缩进，每次缩进 4 个空格。

【正例】

```cangjie
class ListItem {
    var content: Array<Int64> // 符合：相对类声明缩进 4 个空格
    init(
        content: Array<Int64>, // 符合：函数参数相对函数声明缩进 4 个空格
        isShow!: Bool = true,
        id!: String = ""
    ) {
        this.content = content
    }
}
```

- 使用统一的大括号换行风格，对于非空块状结构，大括号使用 K&R 风格。

【正例】

```cangjie
enum TimeUnit { // 符合：跟随声明放行末，前置 1 空格
    Year | Month | Day | Hour
} // 符合：右大括号独占一行

class A { // 符合：跟随声明放行末，前置 1 空格
    var count = 1
}

func fn(a: Int64): Unit { // 符合：跟随声明放行末，前置 1 空格
    if (a > 0) { // 符合：跟随声明放行末，前置 1 空格
    // CODE
    } else { // 符合：右大括号和 else 在同一行
        // CODE
    } // 符合：右大括号独占一行
}

// lambda 函数
let add = {
    base: Int64, bonus: Int64 => // 符合: lambda 表达式中非空块遵循 K&R 风格
    print("符合 news")
    base + bonus
}

```

- 按照仓颉语言编程规范中的规则 G.FMT.10，使用空格突出关键字和重要信息。

【正例】

```cangjie
var isPresent: Bool = false  // 符合：变量声明冒号之后有一个空格
func method(isEmpty!: Bool): RetType { ... } // 符合：函数定义（命名参数 / 返回类型）中的冒号之后有一个空格

method(isEmpty: isPresent) // 符合: 命名参数传值中的冒号之后有一个空格

0..MAX_COUNT : -1 // 符合: range 操作符区间前后没有空格，步长冒号前后两侧有一个空格

var hundred = 0
do { // 符合：关键字 do 和后面的括号之间有一个空格
    hundred++
} while (hundred < 100) // 符合：关键字 while 和前面的括号之间有一个空格

func fn(paramName1: ArgType, paramName2: ArgType): ReturnType { // 符合：圆括号和内部相邻字符之间不出现空格
    ...
    for (i in 1..4) { // 符合：range 操作符左右两侧不留空格
        ...
    }
}

let listOne: Array<Int64> = [1, 2, 3, 4] // 符合：方括号和圆括号内部两侧不出现空格

let salary = base + bonus // 符合：二元操作符左右两侧留空格

x++ // 符合：一元操作符和操作数之间不留空格
```

- 减少不必要的空行，保持代码紧凑。

【反例】

```cangjie
class MyApp <: App {
    let album = albumCreate()
    let page: Router
    // 空行
    // 空行
    // 空行
    init() {           // 不符合：类型定义内部使用连续空行
        this.page = Router("album", album)
    }

    override func onCreate(): Unit {

        println( "album Init." )  // 不符合：大括号内部首尾存在空行

    }
}
```

- 减少不必要的分号，以代码简洁优先。

【格式化前】

```cangjie
package demo.analyzer.filter.impl; // 冗余的分号

internal import demo.analyzer.filter.StmtFilter; // 冗余的分号
internal import demo.analyzer.CJStatment; // 冗余的分号

func fn(a: Int64): Unit {
    println( "album Init." );
}
```

【格式化后】

```cangjie
package demo.analyzer.filter.impl // 冗余的分号

internal import demo.analyzer.filter.StmtFilter // 冗余的分号
internal import demo.analyzer.CJStatment // 冗余的分号

func fn(a: Int64): Unit {
    println("album Init.");
}
```

- 按照仓颉语言编程规范中的规则 G.FMT.12 规定的优先级排列修饰符关键字。

以下是推荐的顶层元素的修饰符排列优先级：

```cangjie
public
open/abstract
```

以下是推荐的实例成员函数或实例成员属性的修饰符排序优先级：

```cangjie
public/protected/private
open
override
```

以下是推荐的静态成员函数的修饰符排序优先级：

```cangjie
public/protected/private
static
redef
```

以下是推荐的成员变量的修饰符排序优先级：

```cangjie
public/protected/private
static
```

- 多行注释的格式化行为

以 `*` 开头的注释，`*` 会互相对齐，不以 `*` 开头的注释，则会保持注释原样。若 `*` 后存在多余空格，则会将多余空格删除。

```cangjie
// 格式化前
/*
      * comment
      */

/*
        comment
        */

// 格式化后
/*
 * comment
 */

/*
        comment
 */
```

## 注意事项

- 仓颉格式化工具暂不支持语法错误的代码的格式化。

- 仓颉格式化工具暂不支持元编程的格式化。
