# Tokens 相关类型和 quote 表达式

## Token 类型

宏操作的基本类型是 `Tokens`，代表一个程序片段。`Tokens` 由若干个 `Token` 组成，每个 `Token` 可以理解为用户可操作的词法单元。一个 `Token` 可能是一个标识符（例如变量名等）、字面量（例如整数、浮点数、字符串）、关键字或运算符。每个 `Token` 包含它的类型、内容和位置信息。

`Token` 的类型取值为 enum `TokenKind` 中的元素。`TokenKind` 的可用值详见《仓颉编程语言库 API》文档。通过提供 `TokenKind` 和 `Token` 的值（`TokenKind` 对应的标识符或字面量），可以直接构造任何 `Token`。具体的构造函数如下：

<!-- code_no_check -->

```cangjie
Token(k: TokenKind)
Token(k: TokenKind, v: String)
```

下面给出一些`Token`构造的例子：

<!-- compile -->

```cangjie
import std.ast.*

let tk1 = Token(TokenKind.ADD)   // '+' 运算符
let tk2 = Token(TokenKind.FUNC)   // func 关键字
let tk3 = Token(TokenKind.IDENTIFIER, "x")   // x 标识符
let tk4 = Token(TokenKind.INTEGER_LITERAL, "3")  // 整数字面量
let tk5 = Token(TokenKind.STRING_LITERAL, "xyz")  // 字符串字面量
```

## Tokens 类型

一个 `Tokens` 代表由多个 `Token` 组成的序列。可以通过 `Token` 数组直接构造 `Tokens`。下面是 3 种基本的构造 `Tokens` 实例的方式：

<!-- code_no_check -->

```cangjie
Tokens()   // 构造空列表
Tokens(tks: Array<Token>)
Tokens(tks: ArrayList<Token>)
```

此外，`Tokens` 类型支持以下功能：

- `size`：返回 `Tokens` 中包含 `Token` 的数量
- `get(index: Int64)`：获取指定下标的 `Token` 元素
- `[]`：获取指定下标的 `Token` 元素
- `+`：拼接两个 `Tokens`，或者直接拼接 `Tokens` 和 `Token`
- `dump()`：打印包含的所有 `Token`，供调试使用
- `toString()`：打印 `Tokens` 对应的程序片段

在下面的案例中，使用构造函数直接构造 `Token` 和 `Tokens`，然后打印详细的调试信息：

<!-- run -->

```cangjie
import std.ast.*

let tks = Tokens([
    Token(TokenKind.INTEGER_LITERAL, "1"),
    Token(TokenKind.ADD),
    Token(TokenKind.INTEGER_LITERAL, "2")
])
main() {
    println(tks)
    tks.dump()
}
```

预期输出如下（具体的位置信息可能不同）：

```text
1 + 2
description: integer_literal, token_id: 140, token_literal_value: 1, fileID: 1, line: 4, column: 5
description: add, token_id: 12, token_literal_value: +, fileID: 1, line: 5, column: 5
description: integer_literal, token_id: 140, token_literal_value: 2, fileID: 1, line: 6, column: 5
```

在 dump 信息中，包含了每个 `Token` 的类型（`description`）和值（`token_literal_value`），最后打印每个 `Token` 的位置信息。

## quote 表达式和插值

在大多数情况下，直接构造和拼接 `Tokens` 会比较繁琐。因此，仓颉语言提供了 `quote` 表达式来从代码模板构造 `Tokens`。之所以说是代码模板，因为在 `quote` 中可以使用 `$(...)` 来插入上下文中的表达式。插入的表达式的类型需要支持被转换为 `Tokens`（具体来说，实现了 `ToTokens` 接口）。在标准库中，以下类型实现了 `ToTokens` 接口：

- 所有的节点类型（节点将在[语法节点](./syntax_node.md)中讨论）
- `Token` 和 `Tokens` 类型
- 所有基础数据类型：整数、浮点数、`Bool`、`Rune` 和 `String`
- `Array<T>` 和 `ArrayList<T>`，这里对 `T` 的类型有限制，并根据 `T` 的类型不同，输出不同的分隔符，详细请见《仓颉编程语言库 API》文档。

下面的例子展示 `Array` 和基础数据类型的插值：

<!-- verify -->

```cangjie
import std.ast.*

let intList: Array<Int64> = [1, 2, 3, 4, 5]
let float: Float64 = 1.0
let str: String = "Hello"
let tokens = quote(
    arr = $(intList)
    x = $(float)
    s = $(str)
)

main() {
    println(tokens)
}
```

输出结果是：

```text

arr =[1, 2, 3, 4, 5]
x = 1.0
s = "Hello"

```

更多插值的用法可以参考  [使用 quote 插值语法节点](./syntax_node.md#使用-quote-插值语法节点)。

特别地，当 `quote` 表达式包含某些特殊 `Token` 时，需要进行转义：

- `quote` 表达式中不允许出现不匹配的小括号，但是通过 `\` 转义的小括号，不计入小括号的匹配规则。
- 当 `$` 表示一个普通 `Token`，而非用于代码插值时，需要通过 `\` 进行转义。
- 除以上情况外，`quote` 表达式中出现 `\` 会编译报错。

> **注意：**
>
> `#` 符号仅能用于构造多行原始字符串字面量，不支持单独使用。

下面是一些 `quote` 表达式内包含这些特殊 `Token` 的例子：

<!-- compile.error -->

```cangjie
import std.ast.*

let tks1 = quote((x))       // ok
let tks2 = quote(\()        // ok
let tks3 = quote( ( \) ) )  // ok
let tks4 = quote())         // error: unmatched delimiter: ')'
let tks5 = quote( ( \) )    // error: unclosed delimiter: '('
let tks6 = quote(\$(1))     // ok
let tks7 = quote(\x)        // error: unknown start of token: \
let tks8 = quote(#)         // error: expected '#' or '"' in raw string
```
