# 语法节点

在仓颉语言的编译过程中，首先通过词法分析将代码转换成 `Tokens`，然后对 `Tokens` 进行语法解析，得到一个语法树。每个语法树的节点可能是一个表达式、声明、类型、模式等。仓颉标准库 `std.ast` 包提供了每种节点对应的类，它们之间具有适当的继承关系。其中，主要的抽象类如下：

- `Node`：所有语法节点的父类
- `TypeNode`：所有类型节点的父类
- `Expr`：所有表达式节点的父类
- `Decl`：所有声明节点的父类
- `Pattern`：所有模式节点的父类

具体节点的类型众多，具体细节请参见《仓颉编程语言库 API》。在下面的案例中，主要使用以下节点：

- `BinaryExpr`：二元运算表达式
- `FuncDecl`：函数的声明

## 节点的解析

通过标准库 `std.ast` 包，基本上每种节点都可以从 `Tokens` 解析。有两种解析 `Tokens` 并构造语法节点的方法。

### 使用解析函数来解析 Tokens

以下函数用于从 `Tokens` 解析并构造任意的语法节点：

- `parseExpr(input: Tokens): Expr`：将输入的 `Tokens` 解析为表达式节点。
- `parseExprFragment(input: Tokens, startFrom!: Int64 = 0): (Expr, Int64)`：将输入 `Tokens` 的一个片段解析为表达式节点，片段从 `startFrom` 索引开始，解析可能只消耗从索引 `startFrom` 开始的片段的一部分，并返回第一个未被消耗的 `Token` 的索引（如果消耗了整个片段，返回值为 `input.size`）。
- `parseDecl(input: Tokens, astKind!: String = "")`：将输入的 `Tokens` 解析为声明节点，`astKind` 为额外的设置，具体请参见《仓颉编程语言库 API》文档。
- `parseDeclFragment(input: Tokens, startFrom!: Int64 = 0): (Decl, Int64)`：将输入 `Tokens` 的一个片段解析为声明节点，`startFrom` 参数和返回索引的含义和 `parseExpr` 相同。
- `parseType(input: Tokens): TypeNode`：将输入的 `Tokens` 解析为类型节点。
- `parseTypeFragment(input: Tokens, startFrom!: Int64 = 0): (TypeNode, Int64)`：将输入 `Tokens` 的一个片段解析为类型节点，`startFrom` 参数和返回索引的含义和 `parseExpr` 相同。
- `parsePattern(input: Tokens): Pattern`：将输入的 `Tokens` 解析为模式节点。
- `parsePatternFragment(input: Tokens, startFrom!: Int64 = 0): (Pattern, Int64)`：将输入 `Tokens` 的一个片段解析为模式节点，`startFrom` 参数和返回索引的含义和 `parseExpr` 相同。

如果解析失败将抛出异常。这种解析方式适用于类型未知的代码片段，如果需要获取具体的子类型节点，需要将解析结果手动转换成具体的子类型。

这些函数的使用如下例所示：

<!-- verify -->

```cangjie
let tks1 = quote(a + b)
let tks2 = quote(u + v, x + y)
let tks3 = quote(
    func f1(x: Int64) { return x + 1 }
)
let tks4 = quote(
    func f2(x: Int64) { return x + 2 }
    func f3(x: Int64) { return x + 3 }
)

let binExpr1 = parseExpr(tks1)
let (binExpr2, mid) = parseExprFragment(tks2)
let (binExpr3, _) = parseExprFragment(tks2, startFrom: mid + 1) // 跳过逗号
println("binExpr1 = ${binExpr1.toTokens()}")
println("binExpr2 = ${binExpr2.toTokens()}, binExpr3 = ${binExpr3.toTokens()}")
let funcDecl1 = parseDecl(tks3)
let (funcDecl2, mid2) = parseDeclFragment(tks4)
let (funcDecl3, _) = parseDeclFragment(tks4, startFrom: mid2)
println("${funcDecl1.toTokens()}")
println("${funcDecl2.toTokens()}")
println("${funcDecl3.toTokens()}")
```

输出结果是：

```text
binExpr1 = a + b
binExpr2 = u + v, binExpr3 = x + y
func f1(x: Int64) {
    return x + 1
}

func f2(x: Int64) {
    return x + 2
}

func f3(x: Int64) {
    return x + 3
}
```

### 使用语法节点的构造函数来解析 Tokens

大多数语法节点都支持 `init(input: Tokens)` 构造函数，将输入的 `Tokens` 解析为相应类型的节点，例如：

<!-- run -->

```cangjie
import std.ast.*

let binExpr = BinaryExpr(quote(a + b))
let funcDecl = FuncDecl(quote(func f1(x: Int64) { return x + 1 }))
```

如果解析失败将抛出异常。这种解析方式适用于类型已知的代码片段，解析后不需要再手动转换成具体的子类型。

## 节点的组成部分

从 `Tokens` 解析出节点之后，可以查看节点的组成部分。作为例子，仅列出 `BinaryExpr` 和 `FuncDecl` 的组成部分，关于其他节点的更详细的解释请参见《仓颉编程语言库 API》文档。

- `BinaryExpr` 节点：
    - `leftExpr: Expr`：运算符左侧的表达式
    - `op: Token`：运算符
    - `rightExpr: Expr`：运算符右侧的表达式
- `FuncDecl` 节点（部分）：
    - `identifier: Token`：函数名
    - `funcParams: ArrayList<FuncParam>`：参数列表
    - `declType: TypeNode`：返回值类型
    - `block: Block`：函数体
- `FuncParam`节点（部分）：
    - `identifier: Token`：参数名
    - `paramType: TypeNode`：参数类型
- `Block`节点（部分）：
    - `nodes: ArrayList<Node>`：块中的表达式和声明

每个组成部分都是 `public mut prop`，因此可以被查看和更新。通过一些例子展示更新的结果。

### BinaryExpr 案例

<!-- verify -->

```cangjie
let binExpr = BinaryExpr(quote(x * y))
binExpr.leftExpr = BinaryExpr(quote(a + b))
println(binExpr.toTokens())

binExpr.op = Token(TokenKind.ADD)
println(binExpr.toTokens())
```

输出结果是：

```text
(a + b) * y
a + b + y
```

首先，通过解析，获得 `binExpr` 为节点 `x * y`，图示如下：

```text
    *
  /   \
 x     y
```

第二步，将左侧的节点（即 `x`）替换为 `a + b`，因此，获得的语法树如下：

```text
      *
    /   \
   +     y
  / \
 a   b
```

当输出这个语法树的时候，必须在 `a + b` 周围添加括号，得到 `(a + b) * y`（如果输出`a + b * y`，含义为先做乘法，再做加法，与语法树的含义不同）。`ast` 库具备在输出语法树时自动添加括号的功能。

第三步，将语法树根部的运算符从 `*` 替换为 `+`，因此得到语法树如下：

```text
      +
    /   \
   +     y
  / \
 a   b
```

这个语法树可以输出为 `a + b + y`，因为加法本身就是左结合的，不需要在左侧添加括号。

### FuncDecl 案例

<!-- verify -->

```cangjie
let funcDecl = FuncDecl(quote(func f1(x: Int64) { x + 1 }))
funcDecl.identifier = Token(TokenKind.IDENTIFIER, "foo")
println("Number of parameters: ${funcDecl.funcParams.size}")
funcDecl.funcParams[0].identifier = Token(TokenKind.IDENTIFIER, "a")
println("Number of nodes in body: ${funcDecl.block.nodes.size}")
let binExpr = (funcDecl.block.nodes[0] as BinaryExpr).getOrThrow()
binExpr.leftExpr = parseExpr(quote(a))
println(funcDecl.toTokens())
```

在这个案例中，首先通过解析构造出了一个 `FuncDecl` 节点，然后分别修改了该节点的函数名、参数名，以及函数体中表达式的一部分。输出结果是：

```text
Number of parameters: 1
Number of nodes in body: 1
func foo(a: Int64) {
    a + 1
}
```

## 使用 quote 插值语法节点

任何语法节点都可以在 `quote` 语句中插值，部分语法节点的 `ArrayList` 列表也可以被插值（主要对应实际情况中会出现这类节点列表的情况）。插值直接通过 `$(node)` 表达即可，其中 `node` 是任意节点类型的实例。

下面，通过一些案例展示节点的插值。

<!-- verify -->

```cangjie
var binExpr = BinaryExpr(quote(1 + 2))
let a = quote($(binExpr))
let b = quote($binExpr)
let c = quote($(binExpr.leftExpr))
let d = quote($binExpr.leftExpr)
println("a: ${a.toTokens()}")
println("b: ${b.toTokens()}")
println("c: ${c.toTokens()}")
println("d: ${d.toTokens()}")
```

输出结果是：

```text
a: 1 + 2
b: 1 + 2
c: 1
d: 1 + 2.leftExpr
```

一般来说，插值运算符后面的表达式使用小括号限定作用域，例如 `$(binExpr)`。但是当后面只跟单个标识符的时候，小括号可省略，即可写为 `$binExpr`。因此，在案例中 `a` 和 `b` 都在 `quote` 中插入了 `binExpr`节点，结果为 `1 + 2`。然而，如果插值运算符后面的表达式更复杂，不加小括号可能造成作用域出错。例如，表达式 `binExpr.leftExpr` 求值为 `1 + 2` 的左表达式，即 `1`，因此 `c` 正确赋值为 `1`。但 `d` 中的插值被解释为 `($binExpr).leftExpr`，因此结果是 `1 + 2.leftExpr`。为了明确插值的作用域，推荐在插值运算符中使用小括号。

下面的案例展示节点列表（`ArrayList`）的插值。

<!-- verify -->

```cangjie
var incrs = ArrayList<Node>()
for (i in 1..=5) {
    incrs.add(parseExpr(quote(x += $(i))))
}
var foo = quote(
    func foo(n: Int64) {
        let x = n
        $(incrs)
        x
    })
println(foo)
```

输出结果是：

```text
func foo(n: Int64) {
    let x = n
    x += 1
    x += 2
    x += 3
    x += 4
    x += 5
    x
}
```

在这个案例中，创建了一个节点列表 `incrs`，包含表达式 `x += 1`，...，`x += 5`。对 `incrs` 的插值将节点依次列出，在每个节点后换行。这适用于插入需要依次执行的表达式和声明的情况。

下面的案例展示在某些情况下，需要在插值周围添加括号，以保证正确性。

<!-- verify -->

```cangjie
var binExpr1 = BinaryExpr(quote(x + y))
var binExpr2 = BinaryExpr(quote($(binExpr1) * z))       // 错误：得到 x + y * z
println("binExpr2: ${binExpr2.toTokens()}")
println("binExpr2.leftExpr: ${binExpr2.leftExpr.toTokens()}")
println("binExpr2.rightExpr: ${binExpr2.rightExpr.toTokens()}")
var binExpr3 = BinaryExpr(quote(($(binExpr1)) * z))     // 正确：得到 (x + y) * z
println("binExpr3: ${binExpr3.toTokens()}")
```

输出结果是：

```text
binExpr2: x + y * z
binExpr2.leftExpr: x
binExpr2.rightExpr: y * z
binExpr3: (x + y) * z
```

首先，构建表达式 `x + y`，然后将该表达式插入到模板 `$(binExpr1) * z` 中。这里的意图是得到一个先计算 `x + y` 再乘 `z` 的表达式，但是，插值的结果是 `x + y * z`，即先计算 `y * z` 再加 `x`。这是因为插值不会自动添加括号以保证被插入的表达式的原子性（这和前一节介绍的 `leftExpr` 的替换不同）。因此，需要在 `$(binExpr1)` 周围添加小括号，保证得到正确的结果。
