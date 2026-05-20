# 宏的简介

宏可以理解为一种特殊的函数。一般的函数在输入的值上进行计算，然后输出一个新的值，而宏的输入和输出都是程序本身。在输入一段程序后，输出一段新的程序，这段输出的程序随后用于编译和执行。为了把宏的调用和函数调用区分开来，在调用宏时需使用 `@` 加上宏的名称。

如下示例代码希望实现在调试过程中打印某个表达式的值，同时打印出表达式本身。

<!-- code_no_check -->

```cangjie
let x = 3
let y = 2
@dprint(x)        // 打印 "x = 3"
@dprint(x + y)    // 打印 "x + y = 5"
```

显然，`dprint` 不能被写为常规的函数，因为函数只能获得输入表达式的值，不能获得输入表达式本身。但是，可以将 `dprint` 实现为一个宏来获取输入表达式的程序片段。一个基本的实现如下：

<!-- verify -macro12 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro dprint(input: Tokens): Tokens {
    let inputStr = input.toString()
    let result = quote(
        print($(inputStr) + " = ")
        println($(input)))
    return result
}
```

在解释每行代码之前，先测试这个宏可以达到预期的效果。首先，在当前目录下创建一个 `define` 文件夹，并在 `define` 文件夹中创建 `dprint.cj` 文件，将以上内容复制到 `dprint.cj` 文件中。另外在当前目录下创建 `main.cj`，包含以下测试代码：

<!-- verify -macro12 -->

```cangjie
import define.*

main() {
    let x = 3
    let y = 2
    @dprint(x)
    @dprint(x + y)
}
```

得到的目录结构如下：

```text
// Directory layout.
src
|-- define
|     |-- dprint.cj
|-- main.cj
```

在当前目录（`src`）下，运行编译命令：

```bash
cjc define/*.cj --compile-macro
cjc main.cj -o main
```

然后运行 `./main`，可以看到如下输出：

<!-- verify -macro12 -->

```text
x = 3
x + y = 5
```

依次查看代码的每个部分：

- 第 1 行：`macro package define`

  宏必须声明在独立的包中（不能和其他 public 函数一起），含有宏的包使用 `macro package` 来声明。这里声明了一个名为 `define` 的宏包。

- 第 2 行：`import std.ast.*`

  实现宏需要的数据类型，例如 `Tokens` 和后面会讲到的语法节点类型，位于仓颉标准库的 `ast` 包中，因此任何宏的实现都需要首先引入 `ast` 包。

- 第 3 行：`public macro dprint(input: Tokens): Tokens`

  在这里声明一个名为 `dprint` 的宏。由于这个宏是一个非属性宏（之后会解释这个概念），它接受一个类型为 `Tokens` 的参数。该输入代表传给宏的程序片段。宏的返回值也是一个程序片段。

- 第 4 行：`let inputStr = input.toString()`

  在宏的实现中，首先将输入的程序片段转化为字符串。在前面的测试案例中，`inputStr` 成为 `"x"` 或 `"x + y"`

- 第 5-7 行：`let result = quote(...)`

  这里 [`quote` 表达式](./Tokens_types_and_quote_expressions.md#quote-表达式和插值)是用于构造 [`Tokens`](./Tokens_types_and_quote_expressions.md#tokens-类型) 的一种表达式，它将括号内的程序片段转换为 `Tokens`。在 `quote` 的输入中，可以使用插值 `$(...)` 来将括号内的表达式转换为 `Tokens`，然后插入到 `quote` 构建的 `Tokens` 中。对于以上代码，`$(inputStr)` 中插入了 `inputStr` 字符串的值（包含字符串两端的引号），`$(input)` 中插入了 `input`，即输入的程序片段。因此，如果输入的表达式是 `x + y`，那么形成的`Tokens`为：

  <!-- code_no_check -->

  ```cangjie
  print("x + y" + " = ")
  println(x + y)
  ```

- 第 8 行：`return result`

  最后，将构造出来的代码片段返回，这两行代码片段将被编译，运行时将输出 `x + y = 5`。

回顾 `dprint` 宏的定义，`dprint` 使用 `Tokens` 作为入参，并使用 `quote` 和插值构造了另一个 `Tokens` 作为返回值。为了使用宏，需要详细了解 `Tokens`、`quote` 和插值的概念，下面将分别介绍它们。
