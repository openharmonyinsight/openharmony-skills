# 实用案例

## 快速幂的计算

通过一个简单的例子展示使用宏进行编译期求值，生成优化代码的应用。在计算幂 `n ^ e` 时，如果 `e` 是一个（比较大的）整数，可以通过重复取平方（而不是迭代相乘）的方式加速计算。这个算法可以直接使用 while 循环实现，例如：

<!-- run -->

```cangjie
func power(n: Int64, e: Int64) {
    var result = 1
    var vn = n
    var ve = e
    while (ve > 0) {
        if (ve % 2 == 1) {
            result *= vn
        }
        ve /= 2
        if (ve > 0) {
            vn *= vn
        }
    }
    result
}
```

然而，这个实现需要每次对 `e` 的值进行分析，在循环和条件判断中多次对 `ve` 进行判断和更新。此外，实现只支持 `n` 的类型为`Int64`的情况，如果要支持其他类型的 `n`，还要处理如何表达 `result = 1` 的问题。如果预先知道 `e` 的具体值，可以将这个代码写的更简单。例如，如果知道 `e` 的值为 10，可以展开整个循环如下：

<!-- run -->

```cangjie
func power_10(n: Int64) {
    var vn = n
    vn *= vn         // vn = n ^ 2
    var result = vn  // result = n ^ 2
    vn *= vn         // vn = n ^ 4
    vn *= vn         // vn = n ^ 8
    result *= vn     // result = n ^ 10
    result
}
```

当然，手动编写这些代码非常繁琐，希望在给定 `e` 的值之后，自动将这些代码生成出来。宏可以做到这一点。使用案例如下：

<!-- code_no_check -->

```cangjie
public func power_10(n: Int64) {
    @power[10](n)
}
```

这个宏展开的代码是（根据 `.macrocall` 文件）：

<!-- code_no_check -->

```cangjie
public func power_10(n: Int64) {
    /* ===== Emitted by MacroCall @power in main.cj:20:5 ===== */
    /* 20.1 */var _power_vn = n
    /* 20.2 */_power_vn *= _power_vn
    /* 20.3 */var _power_result = _power_vn
    /* 20.4 */_power_vn *= _power_vn
    /* 20.5 */_power_vn *= _power_vn
    /* 20.6 */_power_result *= _power_vn
    /* 20.7 */_power_result
/* ===== End of the Emit ===== */
}
```

下面是宏 `@power` 的实现。

<!-- verify -macro13 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*
import std.convert.*

public macro power(attrib: Tokens, input: Tokens) {
    let attribExpr = parseExpr(attrib)
    if (let Some(litExpr) <- (attribExpr as LitConstExpr)) {
        let lit = litExpr.literal
        if (lit.kind != TokenKind.INTEGER_LITERAL) {
            diagReport(DiagReportLevel.ERROR, attrib,
                       "Attribute must be integer literal",
                       "Expected integer literal")
        }
        var n = Int64.parse(lit.value)
        var result = quote(var _power_vn = $(input)
        )
        var flag = false
        while (n > 0) {
            if (n % 2 == 1) {
                if (!flag) {
                    result += quote(var _power_result = _power_vn
                    )
                    flag = true
                } else {
                    result += quote(_power_result *= _power_vn
                    )
                }
            }
            n /= 2
            if (n > 0) {
                result += quote(_power_vn *= _power_vn
                )
            }
        }
        result += quote(_power_result)
        return result
    } else {
        diagReport(DiagReportLevel.ERROR, attrib,
                   "Attribute must be integer literal",
                   "Expected integer literal")
    }
    return input
}
```

这段代码的解释如下：

- 首先，确认输入的属性 `attrib` 是一个整数字面量，否则通过 `diagReport` 报错。将这个字面量解析为整数 `n`。
- 设 `result` 为当前积累的输出代码，首先添加 `var _power_vn` 的声明。这里为了避免变量名冲突，使用不易造成冲突的名字 `_power_vn`。
- 下面进入 while 循环，布尔变量 `flag` 表示 `var _power_result` 是否已经被初始化。其余的代码结构和之前展示的 `power` 函数的实现类似，但区别是使用 while 循环和 if 判断在编译时决定生成的代码是什么，而不是在运行时做这些判断。然后生成由 `_power_result *= _power_vn` 和 `_power_vn *= _power_vn` 适当组合的代码。
- 最后添加返回 `_power_result` 的代码，并将这段代码作为宏的输出值返回。

将这段代码放到 `macros/power.cj` 文件中，并在 `main.cj` 添加如下测试：

<!-- verify -macro13 -->
<!-- cfg="--debug-macro" -->

```cangjie
import define.*

public func power_10(n: Int64) {
    @power[10](n)
}

main() {
    let a = 3
    println(power_10(a))
}
```

输出结果为：

<!-- verify -macro13 -->

```text
59049
```

## Memoize 宏

Memoize（记忆化）是动态规划算法的常用手段。它将已经计算过的子问题的结果存储起来，当同一个子问题再次出现时，可以直接查询表来获取结果，从而避免重复的计算，提高算法的效率。

通常 Memoize 的使用需要开发者手动实现存储和提取的功能。通过宏，可以自动化这一过程。宏的效果如下：

<!-- code_no_check -->

```cangjie
@Memoize[true]
func fib(n: Int64): Int64 {
    if (n == 0 || n == 1) {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}

main() {
    let start = DateTime.now()
    let f35 = fib(35)
    let end = DateTime.now()
    println("fib(35): ${f35}")
    println("execution time: ${(end - start).toMicroseconds()} us")
}
```

在以上代码中，`fib` 函数采用简单的递归方式实现。如果没有 `@Memoize[true]` 标注，这个函数的运行时间将随着 `n` 指数增长。例如，如果在前面的代码中去掉 `@Memoize[true]` 这一行，或者把 `true` 改为 `false`，则 `main` 函数的运行结果为：

```text
fib(35): 9227465
execution time: 199500 us
```

恢复 `@Memoize[true]`，运行结果为：

```text
fib(35): 9227465
execution time: 78 us
```

相同的答案和大幅缩短的计算时间表明，`@Memoize` 的使用确实实现了记忆化。

为了理解 `@Memoize` 的原理，展示对以上 `fib` 函数进行宏展开的结果（来自 `.macrocall` 文件，但是为了提高可读性整理了格式）。

<!-- run -->

```cangjie
import std.collection.*

var memoizeFibMap = HashMap<Int64, Int64>()

func fib(n: Int64): Int64 {
    if (memoizeFibMap.contains(n)) {
        return memoizeFibMap.get(n).getOrThrow()
    }

    let memoizeEvalResult = { =>
        if (n == 0 || n == 1) {
            return n
        }

        return fib(n - 1) + fib(n - 2)
    }()
    memoizeFibMap.add(n, memoizeEvalResult)
    return memoizeEvalResult
}
```

上述代码的执行流程如下：

- 首先，定义 `memoizeFibMap` 为一个从 `Int64` 到 `Int64` 的哈希表，这里第一个 `Int64` 对应 `fib` 的唯一参数的类型，第二个 `Int64` 对应 `fib` 返回值的类型。
- 其次，在函数体中，检查入参是否在 `memoizeFibMap` 中，如果是则立即反馈哈希表中存储的值。否则，使用 `fib` 原来的函数体得到计算结果。这里使用了（不带参数的）匿名函数使 `fib` 的函数体不需要任何改变，并且能够处理任何从 `fib` 函数退出的方式（包括中间的 return，返回最后一个表达式等）。
- 最后，把计算结果存储到 `memoizeFibMap` 中，然后将计算结果返回。

有了这样一个“模板”之后，下面宏的实现就不难理解了。完整的代码如下。

<!-- compile -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro Memoize(attrib: Tokens, input: Tokens) {
    if (attrib.size != 1 || attrib[0].kind != TokenKind.BOOL_LITERAL) {
        diagReport(DiagReportLevel.ERROR, attrib,
                   "Attribute must be a boolean literal (true or false)",
                   "Expected boolean literal (true or false) here")
    }

    let memoized = (attrib[0].value == "true")
    if (!memoized) {
        return input
    }

    let fd = FuncDecl(input)
    if (fd.funcParams.size != 1) {
        diagReport(DiagReportLevel.ERROR, fd.lParen + fd.funcParams.toTokens() + fd.rParen,
                   "Input function to memoize should take exactly one argument",
                   "Expect only one argument here")
    }

    let memoMap = Token(TokenKind.IDENTIFIER, "_memoize_" + fd.identifier.value + "_map")
    let arg1 = fd.funcParams[0]

    return quote(
        var $(memoMap) = HashMap<$(arg1.paramType), $(fd.declType)>()

        func $(fd.identifier)($(arg1)): $(fd.declType) {
            if ($(memoMap).contains($(arg1.identifier))) {
                return $(memoMap).get($(arg1.identifier)).getOrThrow()
            }

            let memoizeEvalResult = { => $(fd.block.nodes) }()
            $(memoMap).add($(arg1.identifier), memoizeEvalResult)
            return memoizeEvalResult
        }
    )
}
```

首先，对属性和输入做合法性检查。属性必须是布尔字面量，如果为 `false` 则直接返回输入。否则，检查输入必须能够解析为函数声明（`FuncDecl`），并且必须包含正好一个参数。下面，产生哈希表的变量，取不容易造成冲突的变量名。最后，通过 `quote`模板生成返回的代码，其中用到哈希表的变量名，以及唯一参数的名称、类型和输入函数的返回类型。

## 一个 dprint 宏的扩展

本节一开始使用了一个打印表达式的宏作为案例，但这个宏一次只能接受一个表达式。希望扩展这个宏，使其能够接受多个表达式，由逗号分开。下面展示如何使用 `parseExprFragment` 来实现这个功能。

宏的实现如下：

<!-- verify -macro15 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro dprint2(input: Tokens) {
    let exprs = ArrayList<Expr>()
    var index: Int64 = 0
    while (true) {
        let (expr, nextIndex) = parseExprFragment(input, startFrom: index)
        exprs.add(expr)
        if (nextIndex == input.size) {
            break
        }
        if (input[nextIndex].kind != TokenKind.COMMA) {
            diagReport(DiagReportLevel.ERROR, input[nextIndex..nextIndex+1],
                       "Input must be a comma-separated list of expressions",
                       "Expected comma")
        }
        index = nextIndex + 1  // 跳过逗号
    }
    let result = quote()
    for (expr in exprs) {
        result.append(quote(
            print($(expr.toTokens().toString()) + " = ")
            println($(expr))
        ))
    }
    return result
}
```

使用案例：

<!-- verify -macro15 -->
<!-- cfg="--debug-macro" -->

```cangjie
import define.*

main() {
    let x = 3
    let y = 2
    @dprint2(x, y, x + y)
}
```

输出结果为：

<!-- verify -macro15 -->

```text
x = 3
y = 2
x + y = 5
```

在宏的实现中，使用 while 循环从索引 0 开始依次解析每个表达式。变量 `index` 保存当前解析的位置。每次调用 `parseExprFragment` 时，从当前位置开始，并返回解析后的位置（以及解析得到的表达式）。如果解析后的位置到达了输入的结尾，则退出循环。否则检查到达的位置是否是一个逗号，如果不是逗号，报错并退出，如果是逗号，跳过这个逗号并开始下一轮的解析。在得到表达式的列表后，依次输出每个表达式。

## 一个简单的 DSL

这个案例展示了如何使用宏实现一个简单的 DSL（Domain Specific Language，领域特定语言）。LINQ（Language Integrated Query，语言集成查询）是微软 .NET 框架的一个组成部分，它提供了一种统一的数据查询语法，允许开发者使用类似 SQL 的查询语句来操作各种数据源。在这里，仅展示一个最简单的 LINQ 语法的支持。

希望支持的语法为：

```text
from <variable> in <list> where <condition> select <expression>
```

其中，`variable` 是一个标识符，`list`、`condition` 和 `expression` 都是表达式。因此，实现宏的策略是先后提取标识符和表达式，同时检查中间的关键字是正确的。最后，生成由提取部分组成的查询结果。

宏的实现如下：

<!-- verify -macro16 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro linq(input: Tokens) {
    let syntaxMsg = "Syntax is \"from <attrib> in <table> where <cond> select <expr>\""
    if (input.size == 0 || input[0].value != "from") {
        diagReport(DiagReportLevel.ERROR, input[0..1], syntaxMsg,
                   "Expected keyword \"from\" here.")
    }
    if (input.size <= 1 || input[1].kind != TokenKind.IDENTIFIER) {
        diagReport(DiagReportLevel.ERROR, input[1..2], syntaxMsg,
                   "Expected identifier here.")
    }
    let attribute = input[1]
    if (input.size <= 2 || input[2].value != "in") {
        diagReport(DiagReportLevel.ERROR, input[2..3], syntaxMsg,
                   "Expected keyword \"in\" here.")
    }
    var index: Int64 = 3
    let (table, nextIndex) = parseExprFragment(input, startFrom: index)
    if (nextIndex == input.size || input[nextIndex].value != "where") {
        diagReport(DiagReportLevel.ERROR, input[nextIndex..nextIndex+1], syntaxMsg,
                   "Expected keyword \"where\" here.")
    }
    index = nextIndex + 1  // 跳过where
    let (cond, nextIndex2) = parseExprFragment(input, startFrom: index)
    if (nextIndex2 == input.size || input[nextIndex2].value != "select") {
        diagReport(DiagReportLevel.ERROR, input[nextIndex2..nextIndex2+1], syntaxMsg,
                   "Expected keyword \"select\" here.")
    }
    index = nextIndex2 + 1  // 跳过select
    let (expr, nextIndex3) = parseExprFragment(input, startFrom: index)

    return quote(
        for ($(attribute) in $(table)) {
            if ($(cond)) {
                println($(expr))
            }
        }
    )
}
```

使用案例：

<!-- verify -macro16 -->
<!-- cfg="--debug-macro" -->

```cangjie
import define.*

main() {
    @linq(from x in 1..=10 where x % 2 == 1 select x * x)
}
```

这个例子从 1, 2, ... 10 列表中筛选出奇数，然后返回所有奇数的平方。输出结果为：

<!-- verify -macro16 -->

```text
1
9
25
49
81
```

可以看到，宏的实现的很大部分用于解析并校验输入的 Tokens，这对宏的可用性至关重要。实际的 LINQ 语言（以及大多数 DSL）的语法更加复杂，需要一整套解析的机制，通过识别不同的关键字或连接符来决定下一步解析的内容。
