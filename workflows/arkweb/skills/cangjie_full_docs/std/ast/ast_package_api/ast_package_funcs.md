# 函数

## func assertParentContext(String)

```cangjie
public func assertParentContext(parentMacroName: String): Unit
```

功能：检查当前宏调用是否在特定的宏调用内。若检查不符合预期，编译器出现一个错误提示。

> **注意：**
>
> 该函数只能作为函数被直接调用，不能作为赋值给变量，不能作为实参或返回值使用。

参数：

- parentMacroName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待检查的外层宏调用的名字。

## func cangjieLex(String)

```cangjie
public func cangjieLex(code: String): Tokens
```

功能：将字符串转换为 [Tokens](ast_package_classes.md#class-tokens) 对象。

参数：

- code: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待词法解析的字符串。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 词法解析得到的 [Tokens](ast_package_classes.md#class-tokens)。

异常：

- [IllegalMemoryException](../../core/core_package_api/core_package_exceptions.md#class-illegalmemoryexception) - 当申请内存失败时，抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当输入的 code 无法被正确的解析为 [Tokens](ast_package_classes.md#class-tokens) 时，抛出异常。

## func cangjieLex(String, Bool)

```cangjie
public func cangjieLex(code: String, truncated: Bool): Tokens
```

功能：将字符串转换为 [Tokens](ast_package_classes.md#class-tokens) 对象。

参数：

- code: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待词法解析的字符串。
- truncated: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否删减解析后 [Tokens](ast_package_classes.md#class-tokens) 中的 Token([END](ast_package_enums.md#end))。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 词法解析得到的 [Tokens](ast_package_classes.md#class-tokens)。

异常：

- [IllegalMemoryException](../../core/core_package_api/core_package_exceptions.md#class-illegalmemoryexception) - 当申请内存失败时，抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当输入的 code 无法被正确的解析为 [Tokens](ast_package_classes.md#class-tokens) 时，抛出异常。

## func compareTokens(Tokens, Tokens)

```cangjie
public func compareTokens(tokens1: Tokens, tokens2: Tokens): Bool
```

功能：用于比较两个 [Tokens](ast_package_classes.md#class-tokens) 是否一致。

参数：

- tokens1: [Tokens](ast_package_classes.md#class-tokens) - 需要比较的第一个 [Tokens](ast_package_classes.md#class-tokens)。
- tokens2: [Tokens](ast_package_classes.md#class-tokens) - 需要比较的第二个 [Tokens](ast_package_classes.md#class-tokens)。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果两个 [Tokens](ast_package_classes.md#class-tokens) 内容相同（除了换行符、结束符和位置信息）则返回 `true`。

## func diagReport(DiagReportLevel, Tokens, String, String)

```cangjie
public func diagReport(level: DiagReportLevel, tokens: Tokens, message: String, hint: String): Unit
```

功能：报错接口，在编译过程的宏展开阶段输出错误提示信息，支持 `WARNING` 和 `ERROR` 两个等级的报错。

> **注意：**
>
> - 该接口在 错误等级为 `ERROR` 时会终止编译过程，但不会终止宏展开过程，建议用户调用接口后直接 return 或者抛出异常来终止宏展开过程。
> - 该接口会按照 cjc 标准报错的接口，将传入的 tokens 所在行的代码列出，并对 tokens 的内容用波浪线进行标注， message 信息将展示在首行， hint 信息将紧跟波浪线进行展示。
> - 报错引用的源码内容目前仅依据第一个 [Token](ast_package_structs.md#struct-token) 的开始位置和最后一个 [Token](ast_package_structs.md#struct-token) 的结束位置确定，不校验中间 [Token](ast_package_structs.md#struct-token) 位置信息的一致性。
> - 该接口在非宏展开过程中调用无效，参见[示例代码](../ast_samples/report.md#非宏展开过程中调用示例)。

参数：

- level: [DiagReportLevel](ast_package_enums.md#enum-diagreportlevel) - 报错信息等级。
- tokens: [Tokens](ast_package_classes.md#class-tokens) - 报错信息中所引用源码内容对应的 [Tokens](ast_package_classes.md#class-tokens)。
- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 报错的主信息。
- hint: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 辅助提示信息。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 存在以下错误时，抛出异常。

    - 输入的 [Tokens](ast_package_classes.md#class-tokens) 为空；
    - 输入的 [Tokens](ast_package_classes.md#class-tokens) 中的 [Token](ast_package_structs.md#struct-token) 来自于不同的源文件；
    - 输入的 [Tokens](ast_package_classes.md#class-tokens) 中首位 [Token](ast_package_structs.md#struct-token) 位置早于末位 [Token](ast_package_structs.md#struct-token) 位置；
    - 输入的 [Tokens](ast_package_classes.md#class-tokens) 中的 [Token](ast_package_structs.md#struct-token) 位置范围超出了宏调用的位置范围。

## func getChildMessages(String)

```cangjie
public func getChildMessages(children:String): ArrayList<MacroMessage>
```

功能：获取特定内层宏发送的信息。

> **注意：**
>
> 该函数只能作为函数被直接调用，不能作为赋值给变量，不能作为实参或返回值使用。

参数：

- children: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待接收信息的内层宏名称。

返回值：

- [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[MacroMessage](ast_package_classes.md#class-macromessage)> - 返回一组 [MacroMessage](ast_package_classes.md#class-macromessage) 的对象。

## func getTokenKind(UInt16)

```cangjie
public func getTokenKind(no: UInt16): TokenKind
```

功能：将词法单元种类序号转化为 [TokenKind](ast_package_enums.md#enum-tokenkind)。

参数：

- no: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 需要转换的序号。

返回值：

- [TokenKind](ast_package_enums.md#enum-tokenkind) - 词法单元种类序号对应的 [TokenKind](ast_package_enums.md#enum-tokenkind)。

> **注意：**
>
> 当前 [SINGLE_QUOTED_STRING_LITERAL](ast_package_enums.md#single_quoted_string_literal) 和 [STRING_LITERAL](ast_package_enums.md#string_literal) 共用序号 147，输入序号 147 只能获得 [STRING_LITERAL](ast_package_enums.md#string_literal)，其他 [TokenKind](ast_package_enums.md#enum-tokenkind) 无共用序号情况。

## func insideParentContext(String)

```cangjie
public func insideParentContext(parentMacroName: String): Bool
```

功能：检查当前宏调用是否在特定的宏调用内，返回一个布尔值。

> **注意：**
>
> - 在嵌套宏场景下，内层宏也可以通过发送键/值对的方式与外层宏通信。当内层宏执行时，通过调用标准库函数 [setItem](ast_package_funcs.md#func-setitemstring-bool) 向外层宏发送信息；随后，当外层宏执行时，调用标准库函数 [getChildMessages](ast_package_funcs.md#func-getchildmessagesstring) 接收每一个内层宏发送的信息（一组键/值对映射）。
> - 该函数只能作为函数被直接调用，不能作为赋值给变量，不能作为实参或返回值使用。

参数：

- parentMacroName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待检查的外层宏调用的名字。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 若当前宏嵌套在特定的宏调用内，返回 true。

## func parseDecl(Tokens, String)

```cangjie
public func parseDecl(input: Tokens, astKind!: String = ""): Decl
```

功能：用于解析一组词法单元，获取一个 [Decl](ast_package_classes.md#class-decl) 类型的节点。

> **注意：**
>
> 该函数不支持解析 [FuncParam](ast_package_classes.md#class-funcparam) 类型。

参数：

- input: [Tokens](ast_package_classes.md#class-tokens) - 待解析源码的词法单元。
- astKind!: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用于指定解析特定的节点类型，有效支持的值为：`PrimaryCtorDecl` 和 `PropMemberDecl`。
    - `PrimaryCtorDecl`: 解析主构造函数。
    - `PropMemberDecl`: 解析 prop 声明的 getter 和 setter 函数。

返回值：

- [Decl](ast_package_classes.md#class-decl) - 一个 [Decl](ast_package_classes.md#class-decl) 类型的节点。

异常：

- [ParseASTException](ast_package_exceptions.md#class-parseastexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [Decl](ast_package_classes.md#class-decl) 节点时，抛出异常，异常中包含报错提示信息。

示例：

1. 以下代码展示 `astKind` 设为 `PropMemberDecl` 的案例。在这个参数下，可以使用 `parseDecl` 解析 `prop` 的 getter 和 setter 函数，解析结果为 `FuncDecl` 类型（如果不设置`astKind`，则会因为没有 `func` 关键字而无法解析）。

<!-- verify -->

```cangjie
import std.ast.*

main() {
    let getter = quote( get() { _val } )
    let setter = quote( set(v) { _val = v })
    let getterDecl = parseDecl(getter, astKind: "PropMemberDecl")
    let setterDecl = parseDecl(setter, astKind: "PropMemberDecl")
    println((getterDecl as FuncDecl).getOrThrow().block.toTokens())
    println((setterDecl as FuncDecl).getOrThrow().block.toTokens())
}
```

运行结果：

```text
{
    _val
}

{
    _val = v
}
```

1. 以下代码展示 `astKind` 设为 `PrimaryCtorDecl` 的案例。在这个参数下，可以使用 `parseDecl` 解析主构造函数节点，解析结果为 `PrimaryCtorDecl` 类型（如果不设置 `astKind`，则会因为没有 `func` 关键字而无法解析）。

<!-- verify -->

```cangjie
import std.ast.*

main() {
    let ctor = quote(
        Point(var x: Int32, var y: Int32) {}
    )
    let ctorDecl = parseDecl(ctor, astKind: "PrimaryCtorDecl")
    println(ctorDecl is PrimaryCtorDecl)
    println(ctorDecl.toTokens())
}
```

运行结果：

```text
true
Point(var x: Int32, var y: Int32) {
}
```

## func parseDeclFragment(Tokens, Int64)

```cangjie
public func parseDeclFragment(input: Tokens, startFrom !: Int64 = 0): (Decl, Int64)
```

功能：用于解析一组词法单元，获取一个 [Decl](ast_package_classes.md#class-decl) 类型的节点和继续解析节点的索引。

> **注意：**
>
> 该函数不支持解析 [FuncParam](ast_package_classes.md#class-funcparam)、 [PropDecl](ast_package_classes.md#class-propdecl)、[PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 类型。

参数：

- input: [Tokens](ast_package_classes.md#class-tokens) - 待解析源码的词法单元。
- startFrom!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 起始位置。

返回值：

- ([Decl](ast_package_classes.md#class-decl), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 语法树节点，继续解析的位置。

异常：

- [ParseASTException](ast_package_exceptions.md#class-parseastexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [Decl](ast_package_classes.md#class-decl) 节点时，抛出异常，异常中包含报错提示信息。

## func parseExpr(Tokens)

```cangjie
public func parseExpr(input: Tokens): Expr
```

功能：用于解析一组词法单元，获取一个 [Expr](ast_package_classes.md#class-expr) 类型的节点。

参数：

- input: [Tokens](ast_package_classes.md#class-tokens) - 待解析源码的词法单元。

返回值：

- [Expr](ast_package_classes.md#class-expr) - 一个 [Expr](ast_package_classes.md#class-expr) 类型的节点。

异常：

- [ParseASTException](ast_package_exceptions.md#class-parseastexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [Expr](ast_package_classes.md#class-expr) 节点时，抛出异常，异常中包含报错提示信息。

## func parseExprFragment(Tokens, Int64)

```cangjie
public func parseExprFragment(input: Tokens, startFrom !: Int64 = 0): (Expr, Int64)
```

功能：用于解析一组词法单元，获取一个 [Expr](ast_package_classes.md#class-expr) 类型的节点和继续解析节点的索引。

参数：

- input: [Tokens](ast_package_classes.md#class-tokens) - 待解析源码的词法单元。
- startFrom!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 起始位置。

返回值：

- ([Expr](ast_package_classes.md#class-expr), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 语法树节点，继续解析的位置。

异常：

- [ParseASTException](ast_package_exceptions.md#class-parseastexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [Expr](ast_package_classes.md#class-expr) 节点时，抛出异常，异常中包含报错提示信息。

## func parsePattern(Tokens)

```cangjie
public func parsePattern(input: Tokens): Pattern
```

功能：用于解析一组词法单元，获取一个 [Pattern](ast_package_classes.md#class-pattern) 类型的节点。

参数：

- input: [Tokens](ast_package_classes.md#class-tokens) - 待解析源码的词法单元。

返回值：

- [Pattern](ast_package_classes.md#class-pattern) - 一个 [Pattern](ast_package_classes.md#class-pattern) 类型的节点。

异常：

- [ParseASTException](ast_package_exceptions.md#class-parseastexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [Pattern](ast_package_classes.md#class-pattern) 节点时，抛出异常，异常中包含报错提示信息。

## func parsePatternFragment(Tokens, Int64)

```cangjie
public func parsePatternFragment(input: Tokens, startFrom !: Int64 = 0): (Pattern, Int64)
```

功能：用于解析一组词法单元，获取一个 [Pattern](ast_package_classes.md#class-pattern) 类型的节点和继续解析节点的索引。

参数：

- input: [Tokens](ast_package_classes.md#class-tokens) - 待解析源码的词法单元。
- startFrom!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 起始位置。

返回值：

- ([Pattern](ast_package_classes.md#class-pattern), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 语法树节点，继续解析的位置。

异常：

- [ParseASTException](ast_package_exceptions.md#class-parseastexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [Pattern](ast_package_classes.md#class-pattern) 节点时，抛出异常，异常中包含报错提示信息。

## func parseProgram(Tokens)

```cangjie
public func parseProgram(input: Tokens): Program
```

功能：用于解析单个仓颉文件的源码，获取一个 [Program](ast_package_classes.md#class-program) 类型的节点。

> **注意：**
>
> 仓颉宏展开后的代码不允许出现包的声明和包导入语句。使用该函数时，若输入的源码中包含包声明或包导入语句，输出的 [Program](ast_package_classes.md#class-program) 节点中也会包含（在 [packageHeader](ast_package_classes.md#prop-packageheader) 和 [importLists](ast_package_classes.md#prop-importlists) 属性中），因此不能在宏函数中直接将该节点返回为 [Tokens](ast_package_classes.md#class-tokens)。

参数：

- input: [Tokens](ast_package_classes.md#class-tokens) - 待解析源码的词法单元。

返回值：

- [Program](ast_package_classes.md#class-program) - 一个 [Program](ast_package_classes.md#class-program) 类型的节点。

异常：

- [ParseASTException](ast_package_exceptions.md#class-parseastexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [Program](ast_package_classes.md#class-program) 节点时，抛出异常，异常中包含报错提示信息。

## func parseType(Tokens)

```cangjie
public func parseType(input: Tokens): TypeNode
```

功能：用于解析一组词法单元，获取一个 [TypeNode](ast_package_classes.md#class-typenode) 类型的节点。

参数：

- input: [Tokens](ast_package_classes.md#class-tokens) - 待解析源码的词法单元。

返回值：

- [TypeNode](ast_package_classes.md#class-typenode) - 一个 [TypeNode](ast_package_classes.md#class-typenode) 类型的节点。

异常：

- [ParseASTException](ast_package_exceptions.md#class-parseastexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TypeNode](ast_package_classes.md#class-typenode) 节点时，抛出异常。

## func parseTypeFragment(Tokens, Int64)

```cangjie
public func parseTypeFragment(input: Tokens, startFrom !: Int64 = 0): (TypeNode, Int64)
```

功能：用于解析一组词法单元，获取一个 [TypeNode](ast_package_classes.md#class-typenode) 类型的节点和继续解析节点的索引。

参数：

- input: [Tokens](ast_package_classes.md#class-tokens) - 待解析源码的词法单元。
- startFrom!: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 起始位置。

返回值：

- ([TypeNode](ast_package_classes.md#class-typenode), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 语法树节点，继续解析的位置。

异常：

- [ParseASTException](ast_package_exceptions.md#class-parseastexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TypeNode](ast_package_classes.md#class-typenode) 节点时，抛出异常。

## func setItem(String, Bool)

```cangjie
public func setItem(key: String, value: Bool): Unit
```

功能：内层宏通过该接口发送 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型的信息到外层宏。

> **注意：**
>
> 该函数只能作为函数被直接调用，不能作为赋值给变量，不能作为实参或返回值使用。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 发送的关键字，用于检索信息。
- value: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 要发送的 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型的信息。

## func setItem(String, Int64)

```cangjie
public func setItem(key: String, value: Int64): Unit
```

功能：内层宏通过该接口发送 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型的信息到外层宏。

> **注意：**
>
> 该函数只能作为函数被直接调用，不能作为赋值给变量，不能作为实参或返回值使用。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 发送的关键字，用于检索信息。
- value: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 要发送的 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型的信息。

## func setItem(String, String)

```cangjie
public func setItem(key: String, value: String): Unit
```

功能：内层宏通过该接口发送 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型的信息到外层宏。

> **注意：**
>
> 该函数只能作为函数被直接调用，不能作为赋值给变量，不能作为实参或返回值使用。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 发送的关键字，用于检索信息。
- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要发送的 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型的信息。

## func setItem(String, Tokens)

```cangjie
public func setItem(key: String, value: Tokens): Unit
```

功能：内层宏通过该接口发送 [Tokens](ast_package_classes.md#class-tokens) 类型的信息到外层宏。

> **注意：**
>
> 该函数只能作为函数被直接调用，不能作为赋值给变量，不能作为实参或返回值使用。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 发送的关键字，用于检索信息。
- value: [Tokens](ast_package_classes.md#class-tokens) - 要发送的 [Tokens](ast_package_classes.md#class-tokens) 类型的信息。
