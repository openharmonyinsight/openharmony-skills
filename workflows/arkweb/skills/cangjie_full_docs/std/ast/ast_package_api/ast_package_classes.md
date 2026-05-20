# 类

## class Annotation

```cangjie
public class Annotation <: Node {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示编译器内置的注解节点。

一个 [Annotation](ast_package_classes.md#class-annotation) 节点：`@CallingConv[xxx]`, `@Attribute[xxx]`, `@When[condition]`等。

父类型：

- [Node](#class-node)

### prop arguments

```cangjie
public mut prop arguments: ArrayList<Argument>
```

功能：获取或设置 [Annotation](ast_package_classes.md#class-annotation) 中的参数序列，如 `@CallingConv[xxx]` 中的 `xxx`。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Argument](ast_package_classes.md#class-argument)>

### prop at

```cangjie
public mut prop at: Token
```

功能：获取或设置 [Annotation](ast_package_classes.md#class-annotation) 节点中的 `@` 操作符或 `@!` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `@` 操作符或 `@!` 操作符时，抛出异常。

### prop attributes

```cangjie
public mut prop attributes: Tokens
```

功能：获取或设置 `Attribute` 中设置的属性值，仅用于 `@Attribute`，如 `@Attribute[xxx]` 中的 `xxx`。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop condition

```cangjie
public mut prop condition: Expr
```

功能：获取或设置条件编译中的条件表达式，用于 `@When`，如 `@When[xxx]` 中的 `xxx`。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [Annotation](ast_package_classes.md#class-annotation) 节点中没有条件表达式时，抛出异常。

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置 [Annotation](ast_package_classes.md#class-annotation) 节点的标识符，如 `@CallingConv[xxx]` 中的 `CallingConv`。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Annotation](ast_package_classes.md#class-annotation) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：根据输入的词法单元，构造一个 [Annotation](ast_package_classes.md#class-annotation) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [Annotation](ast_package_classes.md#class-annotation) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [Annotation](ast_package_classes.md#class-annotation) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Argument

```cangjie
public class Argument <: Node {
    public init()
}
```

功能：表示函数调用的实参节点。

例如 `foo(arg:value)` 中的 `arg:value`。

父类型：

- [Node](#class-node)

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [Argument](ast_package_classes.md#class-argument) 节点中的操作符 ":"，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ":" 操作符时，抛出异常。

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [Argument](ast_package_classes.md#class-argument) 节点中的表达式，如 `arg:value` 中的 `value`。

类型：[Expr](ast_package_classes.md#class-expr)

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置 [Argument](ast_package_classes.md#class-argument) 节点中的标识符，如 `arg:value` 中的 `arg`，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当获取和设置的 [Token](ast_package_structs.md#struct-token) 类型不是 [IDENTIFIER](ast_package_enums.md#identifier) 标识符或 [Token](ast_package_structs.md#struct-token) 的字面量值是空时，抛出异常。

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [Argument](ast_package_classes.md#class-argument) 节点中的关键字 `inout`，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Argument](ast_package_classes.md#class-argument) 对象。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ArrayLiteral

```cangjie
public class ArrayLiteral <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt) 字面量节点。

[ArrayLiteral](ast_package_classes.md#class-arrayliteral) 节点：使用格式 `[element1, element2, ... , elementN]` 表示， 每个 `element` 是一个表达式。

父类型：

- [Expr](#class-expr)

### prop elements

```cangjie
public mut prop elements: ArrayList<Expr>
```

功能：获取或设置 [ArrayLiteral](ast_package_classes.md#class-arrayliteral) 中的表达式列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Expr](ast_package_classes.md#class-expr)>

### prop lSquare

```cangjie
public mut prop lSquare: Token
```

功能：获取或设置 [ArrayLiteral](ast_package_classes.md#class-arrayliteral) 中的 "["。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "[" 时，抛出异常。

### prop rSquare

```cangjie
public mut prop rSquare: Token
```

功能：获取或设置 [ArrayLiteral](ast_package_classes.md#class-arrayliteral) 中的 "]"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "]" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ArrayLiteral](ast_package_classes.md#class-arrayliteral) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ArrayLiteral](ast_package_classes.md#class-arrayliteral) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ArrayLiteral](ast_package_classes.md#class-arrayliteral) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ArrayLiteral](ast_package_classes.md#class-arrayliteral) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class AsExpr

```cangjie
public class AsExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个类型检查表达式。

一个 [AsExpr](ast_package_classes.md#class-asexpr) 表达式：`e as T`，类型为 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T>。其中 e 可以是任何类型的表达式，T 可以是任何类型。

父类型：

- [Expr](#class-expr)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [AsExpr](ast_package_classes.md#class-asexpr) 节点中的表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [AsExpr](ast_package_classes.md#class-asexpr) 节点中的 `as` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `as` 操作符时，抛出异常。

### prop shiftType

```cangjie
public mut prop shiftType: TypeNode
```

功能：获取或设置 [AsExpr](ast_package_classes.md#class-asexpr) 节点中的目标类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [AsExpr](ast_package_classes.md#class-asexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [AsExpr](ast_package_classes.md#class-asexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [AsExpr](ast_package_classes.md#class-asexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [AsExpr](ast_package_classes.md#class-asexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class AssignExpr

```cangjie
public class AssignExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示赋值表达式节点。

用于将左操作数的值修改为右操作数的值。一个 [AssignExpr](ast_package_classes.md#class-assignexpr) 节点：`a = b`。

父类型：

- [Expr](#class-expr)

### prop assign

```cangjie
public mut prop assign: Token
```

功能：获取或设置 [AssignExpr](ast_package_classes.md#class-assignexpr) 节点中的赋值操作符（如 `=` 等）。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是赋值操作符时，抛出异常。

### prop leftExpr

```cangjie
public mut prop leftExpr: Expr
```

功能：获取或设置 [AssignExpr](ast_package_classes.md#class-assignexpr) 节点中的左操作数。

类型：[Expr](ast_package_classes.md#class-expr)

### prop rightExpr

```cangjie
public mut prop rightExpr: Expr
```

功能：获取或设置 [AssignExpr](ast_package_classes.md#class-assignexpr) 节点中的右操作数。

类型：[Expr](ast_package_classes.md#class-expr)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [AssignExpr](ast_package_classes.md#class-assignexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [AssignExpr](ast_package_classes.md#class-assignexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [AssignExpr](ast_package_classes.md#class-assignexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [AssignExpr](ast_package_classes.md#class-assignexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class BinaryExpr

```cangjie
public class BinaryExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个二元操作表达式节点。

一个 [BinaryExpr](ast_package_classes.md#class-binaryexpr) 节点：`a + b`, `a - b` 等。

父类型：

- [Expr](#class-expr)

### prop leftExpr

```cangjie
public mut prop leftExpr: Expr
```

功能：获取或设置 [BinaryExpr](ast_package_classes.md#class-binaryexpr) 节点中操作符左侧的表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

### prop op

```cangjie
public mut prop op: Token
```

功能：获取或设置 [BinaryExpr](ast_package_classes.md#class-binaryexpr) 节点中的二元操作符。

类型：[Token](ast_package_structs.md#struct-token)

### prop rightExpr

```cangjie
public mut prop rightExpr: Expr
```

功能：获取或设置 [BinaryExpr](ast_package_classes.md#class-binaryexpr) 节点中操作符右侧的表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [BinaryExpr](ast_package_classes.md#class-binaryexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [BinaryExpr](ast_package_classes.md#class-binaryexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [BinaryExpr](ast_package_classes.md#class-binaryexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [BinaryExpr](ast_package_classes.md#class-binaryexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Block

```cangjie
public class Block <: Expr {
    public init()
}
```

功能：表示块节点。

[Block](ast_package_classes.md#class-block) 由一对匹配的大括号及其中可选的表达式声明序列组成的结构，简称 “块”。

父类型：

- [Expr](#class-expr)

### prop lBrace

```cangjie
public mut prop lBrace: Token
```

功能：获取或设置 [Block](ast_package_classes.md#class-block) 的 "{"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "{" 时，抛出异常。

### prop nodes

```cangjie
public mut prop nodes: ArrayList<Node>
```

功能：获取或设置 [Block](ast_package_classes.md#class-block) 中的表达式或声明序列。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Node](ast_package_classes.md#class-node)>

### prop rBrace

```cangjie
public mut prop rBrace: Token
```

功能：获取或设置 [Block](ast_package_classes.md#class-block) 的 "}"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "}" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Block](ast_package_classes.md#class-block) 对象。

> **说明：**
>
> [Block](ast_package_classes.md#class-block) 节点无法脱离表达式或声明节点单独存在，因此不提供其他的构造函数。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Body

```cangjie
public class Body <: Node {
    public init()
    public init(decls: ArrayList<Decl>)
}
```

功能：表示 Class 类型、 Struct 类型、 Interface 类型以及扩展中由 `{}` 和内部的一组声明节点组成的结构。

父类型：

- [Node](#class-node)

### prop decls

```cangjie
public mut prop decls: ArrayList<Decl>
```

功能：获取或设置 [Body](ast_package_classes.md#class-body) 内的声明节点集合。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Decl](ast_package_classes.md#class-decl)>

### prop lBrace

```cangjie
public mut prop lBrace: Token
```

功能：获取或设置 `{` 词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `{` 词法单元时，抛出异常。

### prop rBrace

```cangjie
public mut prop rBrace: Token
```

功能：获取或设置 `}` 词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `}` 词法单元时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Body](ast_package_classes.md#class-body) 对象。

### init(ArrayList\<Decl>)

```cangjie
public init(decls: ArrayList<Decl>)
```

功能：构造一个 [Body](ast_package_classes.md#class-body) 对象。

参数：

- decls: [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Decl](ast_package_classes.md#class-decl)> - 将要构造 [Body](ast_package_classes.md#class-body) 类型的声明列表。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class CallExpr

```cangjie
public class CallExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示函数调用节点节点。

一个 [CallExpr](ast_package_classes.md#class-callexpr) 节点包括一个表达式后面紧跟参数列表，例如 `foo(100)`。

父类型：

- [Expr](#class-expr)

### prop arguments

```cangjie
public mut prop arguments: ArrayList<Argument>
```

功能：获取或设置 [CallExpr](ast_package_classes.md#class-callexpr) 节点中函数参数。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Argument](ast_package_classes.md#class-argument)>

### prop callFunc

```cangjie
public mut prop callFunc: Expr
```

功能：获取或设置 [CallExpr](ast_package_classes.md#class-callexpr) 节点中的函数调用节点。

类型：[Expr](ast_package_classes.md#class-expr)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [CallExpr](ast_package_classes.md#class-callexpr) 节点中的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [CallExpr](ast_package_classes.md#class-callexpr) 节点中的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [CallExpr](ast_package_classes.md#class-callexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [CallExpr](ast_package_classes.md#class-callexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [CallExpr](ast_package_classes.md#class-callexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [CallExpr](ast_package_classes.md#class-callexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ClassDecl

```cangjie
public class ClassDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：类定义节点。

类的定义使用 `class` 关键字，定义依次为：可缺省的修饰符、class 关键字、class 名、可选的类型参数、是否指定父类或父接口、可选的泛型约束、类体的定义。

父类型：

- [Decl](#class-decl)

### prop body

```cangjie
public mut prop body: Body
```

功能：获取或设置 [ClassDecl](ast_package_classes.md#class-classdecl) 节点的类体。

类型：[Body](ast_package_classes.md#class-body)

### prop superTypeBitAnds

```cangjie
public mut prop superTypeBitAnds: Tokens
```

功能：获取或设置 [ClassDecl](ast_package_classes.md#class-classdecl) 节点的父类或父接口声明中的 `&` 操作符的词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 `&` 词法单元序列时，抛出异常。

### prop superTypes

```cangjie
public mut prop superTypes: ArrayList<TypeNode>
```

功能：获取或设置 [ClassDecl](ast_package_classes.md#class-classdecl) 节点的父类或者父接口。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### prop upperBound

```cangjie
public mut prop upperBound: Token
```

功能：获取或设置 `<:` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `<:` 操作符时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ClassDecl](ast_package_classes.md#class-classdecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ClassDecl](ast_package_classes.md#class-classdecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ClassDecl](ast_package_classes.md#class-classdecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ClassDecl](ast_package_classes.md#class-classdecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ConstPattern

```cangjie
public class ConstPattern <: Pattern {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示常量模式节点。

常量模式可以是整数字面量、字符字节字面量、浮点数字面量、字符字面量、布尔字面量、字符串字面量等字面量，如 `case 1 => 0` 中的 `1`。

父类型：

- [Pattern](#class-pattern)

### prop litConstExpr

```cangjie
public mut prop litConstExpr: LitConstExpr
```

功能：获取或设置 [ConstPattern](ast_package_classes.md#class-constpattern) 节点中的字面量表达式。

类型：[LitConstExpr](ast_package_classes.md#class-litconstexpr)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ConstPattern](ast_package_classes.md#class-constpattern) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ConstPattern](ast_package_classes.md#class-constpattern) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ConstPattern](ast_package_classes.md#class-constpattern) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ConstPattern](ast_package_classes.md#class-constpattern) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Constructor

```cangjie
public class Constructor <: Node {
    public init()
}
```

功能：表示 `enum` 类型中的 [Constructor](ast_package_classes.md#class-constructor) 节点。

一个 [Constructor](ast_package_classes.md#class-constructor) 节点：enum TimeUnit { Year | Month([Float32](../../core/core_package_api/core_package_intrinsics.md#float32), [Float32](../../core/core_package_api/core_package_intrinsics.md#float32))} 中的 Year 和 Month([Float32](../../core/core_package_api/core_package_intrinsics.md#float32), [Float32](../../core/core_package_api/core_package_intrinsics.md#float32))。

> **说明：**
>
> [Constructor](ast_package_classes.md#class-constructor) 可以没有参数，也可以有一组不同类型的参数。

父类型：

- [Node](#class-node)

### prop annotations

```cangjie
public mut prop annotations: ArrayList<Annotation>
```

功能：获取或设置作用于 [Constructor](ast_package_classes.md#class-constructor) 节点的注解列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Annotation](ast_package_classes.md#class-annotation)>

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置 [Constructor](ast_package_classes.md#class-constructor) 的标识符词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [Constructor](ast_package_classes.md#class-constructor) 节点中的 "(" 词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [Constructor](ast_package_classes.md#class-constructor) 节点中的 ")" 词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop typeArguments

```cangjie
public mut prop typeArguments: ArrayList<TypeNode>
```

功能：获取或设置 [Constructor](ast_package_classes.md#class-constructor) 节点可选的参数类型节点的集合。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Constructor](ast_package_classes.md#class-constructor) 对象。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Decl

```cangjie
public open class Decl <: Node
```

功能：所有声明节点的父类，继承自 [Node](ast_package_classes.md#class-node) 节点，提供了所有声明节点的通用接口。

> **说明：**
>
> 类定义、接口定义、函数定义、变量定义、枚举定义、结构体定义、扩展定义、类型别名定义、宏定义等都属于 [Decl](ast_package_classes.md#class-decl) 节点。

父类型：

- [Node](#class-node)

### var identifier_

```cangjie
protected var identifier_: Token
```

功能：获取或设置声明节点的标识符，如 `class foo {}` 中的 `foo`。

类型：[Token](ast_package_structs.md#struct-token)

### var keyword_

```cangjie
protected var keyword_: Token
```

功能：获取或设置声明节点的关键字。

类型：[Token](ast_package_structs.md#struct-token)

### var modifiers_

```cangjie
protected var modifiers_: ArrayList<Modifier>
```

功能：获取或设置节点的修饰符列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Modifier](ast_package_classes.md#class-modifier)>

### var node

```cangjie
protected var node: Node
```

功能：获取或设置[Decl](ast_package_classes.md#class-decl) 节点的形参节点。

类型：[Node](ast_package_classes.md#class-node)

### prop annotations

```cangjie
public mut prop annotations: ArrayList<Annotation>
```

功能：获取或设置作用于 [Decl](ast_package_classes.md#class-decl) 节点的注解列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Annotation](ast_package_classes.md#class-annotation)>

### prop constraintCommas

```cangjie
public mut prop constraintCommas: Tokens
```

功能：获取或设置 [Decl](ast_package_classes.md#class-decl) 节点中的 "," 词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "," 词法单元序列时，抛出异常。

### prop genericConstraint

```cangjie
public mut prop genericConstraint: ArrayList<GenericConstraint>
```

功能：获取或设置声明节点的泛型约束，可能为空，如 `func foo<T>() where T <: Comparable<T> {}` 中的 `where T <: Comparable<T>`。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[GenericConstraint](ast_package_classes.md#class-genericconstraint)>

### prop genericParam

```cangjie
public mut prop genericParam: GenericParam
```

功能：获取或设置形参列表，类型形参列表由 `<>` 括起，多个类型形参之间用逗号分隔。

类型：[GenericParam](ast_package_classes.md#class-genericparam)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当节点未定义类型形参列表时，抛出异常。

### prop identifier

```cangjie
public mut open prop identifier: Token
```

功能：获取或设置声明节点的标识符，如 `class foo {}` 中的 `foo`。

类型：[Token](ast_package_structs.md#struct-token)

### prop isGenericDecl

```cangjie
public mut prop isGenericDecl: Bool
```

功能：判断是否是一个泛型节点。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是一个泛型节点为 true；反之为 false。

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置声明节点的关键字。

类型：[Token](ast_package_structs.md#struct-token)

### prop modifiers

```cangjie
public mut prop modifiers: ArrayList<Modifier>
```

功能：获取或设置节点的修饰符列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Modifier](ast_package_classes.md#class-modifier)>

### func dump(UInt16)

```cangjie
protected open func dump(indent: UInt16): String
```

功能：将当前语法树节点转化为树形结构的形态并进行打印。语法树节点的树形结构将按照以下形式进行输出：

- `-` 字符串：表示当前节点的公共属性， 如 `-keyword` , `-identifier`。
- 节点属性后紧跟该节点的具体类型， 如 `-declType: PrimitiveType` 表示节点类型是一个 [PrimitiveType](ast_package_classes.md#class-primitivetype) 节点。
- 每个类型使用大括号表示类型的作用区间。

语法树输出的详细格式请参见[语法树节点打印](../ast_samples/dump.md)。

参数：

- indent: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 格式化输出的缩进空格数量。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化输出内容。

### func getAttrs()

```cangjie
public func getAttrs(): Tokens
```

功能：获取当前节点的属性（一般通过内置的 `Attribute` 来设置某个声明设置属性值）。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 当前节点的属性。

### func hasAttr(String)

```cangjie
public func hasAttr(attr: String): Bool
```

功能：判断当前节点是否具有某个属性（一般通过内置的 `Attribute` 来设置某个声明的属性值）。

参数：

- attr: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 将要判断是否存在于该节点的属性。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当前节点具有该属性时，返回 true；反之，返回 false。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class DoWhileExpr

```cangjie
public class DoWhileExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `do-while` 表达式。

父类型：

- [Expr](#class-expr)

### prop block

```cangjie
public mut prop block: Block
```

功能：获取或设置 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 中的块表达式。

类型：[Block](ast_package_classes.md#class-block)

### prop condition

```cangjie
public mut prop condition: Expr
```

功能：获取或设置关键字 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 中的条件表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop keywordD

```cangjie
public mut prop keywordD: Token
```

功能：获取或设置 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 节点中 `do` 关键字，其中 keywordD 中的 D 为关键字 `do` 的首字母大写，代表关键字 `do` 。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `do` 关键字时，抛出异常。

### prop keywordW

```cangjie
public mut prop keywordW: Token
```

功能：获取或设置 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 节点中 `while` 关键字，其中 keywordW 中的 W 为关键字 `while` 的首字母大写，代表关键字 `while` 。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `while` 关键字时，抛出异常。

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 中 `while` 关键字之后的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 中 `while` 关键字之后的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class EnumDecl

```cangjie
public class EnumDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个 `Enum` 定义节点。

Enum 的定义使用 `enum` 关键字，定义依次为：可缺省的修饰符、enum 关键字、enum 名、可选的类型参数、是否指定父接口、可选的泛型约束、enum 体的定义。

父类型：

- [Decl](#class-decl)

### prop constructors

```cangjie
public mut prop constructors: ArrayList<Constructor>
```

功能：获取或设置 [EnumDecl](ast_package_classes.md#class-enumdecl) 节点内 constructor 的成员。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Constructor](ast_package_classes.md#class-constructor)>

### prop decls

```cangjie
public mut prop decls: ArrayList<Decl>
```

功能：获取或设置 [EnumDecl](ast_package_classes.md#class-enumdecl) 节点内除 constructor 的其他成员。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Decl](ast_package_classes.md#class-decl)>

### prop ellipsis

```cangjie
public mut prop ellipsis: Token
```

功能：获取或设置 [EnumDecl](ast_package_classes.md#class-enumdecl) 节点中可选的 `...` 词法单元，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元类型。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `...` 词法单元时，抛出异常。

### prop lBrace

```cangjie
public mut prop lBrace: Token
```

功能：获取或设置 [EnumDecl](ast_package_classes.md#class-enumdecl) 节点的 `{` 词法单元类型。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `{` 词法单元类型时，抛出异常。

### prop rBrace

```cangjie
public mut prop rBrace: Token
```

功能：获取或设置 [EnumDecl](ast_package_classes.md#class-enumdecl) 节点的 `}` 词法单元类型。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `}` 词法单元类型时，抛出异常。

### prop superTypeBitAnds

```cangjie
public mut prop superTypeBitAnds: Tokens
```

功能：获取或设置 [EnumDecl](ast_package_classes.md#class-enumdecl) 节点的父接口声明中的 `&` 操作符的词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 `&` 词法单元序列时，抛出异常。

### prop superTypes

```cangjie
public mut prop superTypes: ArrayList<TypeNode>
```

功能：获取或设置 [EnumDecl](ast_package_classes.md#class-enumdecl) 节点的父接口。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### prop upperBound

```cangjie
public mut prop upperBound: Token
```

功能：获取或设置 `<:` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `<:` 操作符时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [EnumDecl](ast_package_classes.md#class-enumdecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [EnumDecl](ast_package_classes.md#class-enumdecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [EnumDecl](ast_package_classes.md#class-enumdecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [EnumDecl](ast_package_classes.md#class-enumdecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class EnumPattern

```cangjie
public class EnumPattern <: Pattern {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 enum 模式节点。

用于匹配 enum 的 `constructor`， 如 `case Year(n) => 1` 中的 `Year(n)`。

父类型：

- [Pattern](#class-pattern)

### prop commas

```cangjie
public mut prop commas: Tokens
```

功能：获取或设置 [EnumPattern](ast_package_classes.md#class-enumpattern) 节点中的 "," 词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "," 词法单元序列时，抛出异常。

### prop constructor

```cangjie
public mut prop constructor: Expr
```

功能：获取或设置 [EnumPattern](ast_package_classes.md#class-enumpattern) 节点中的构造器表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [EnumPattern](ast_package_classes.md#class-enumpattern) 节点中的 "(" 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop patterns

```cangjie
public mut prop patterns: ArrayList<Pattern>
```

功能：获取或设置 [EnumPattern](ast_package_classes.md#class-enumpattern) 节点中有参构造器内的模式节点列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Pattern](ast_package_classes.md#class-pattern)>

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [EnumPattern](ast_package_classes.md#class-enumpattern) 节点中的 ")" 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [EnumPattern](ast_package_classes.md#class-enumpattern) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [EnumPattern](ast_package_classes.md#class-enumpattern) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [EnumPattern](ast_package_classes.md#class-enumpattern) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [EnumPattern](ast_package_classes.md#class-enumpattern) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ExceptTypePattern

```cangjie
public class ExceptTypePattern <: Pattern {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个用于异常模式状态下的节点。

例如 `e: Exception1 | Exception2`。

父类型：

- [Pattern](#class-pattern)

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [ExceptTypePattern](ast_package_classes.md#class-excepttypepattern) 节点中的 ":" 操作符的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ":" 操作符时，抛出异常。

### prop pattern

```cangjie
public mut prop pattern: Pattern
```

功能：获取或设置 [ExceptTypePattern](ast_package_classes.md#class-excepttypepattern) 节点中的模式节点。

类型：[Pattern](ast_package_classes.md#class-pattern)

### prop types

```cangjie
public mut prop types: ArrayList<TypeNode>
```

功能：获取或设置 [ExceptTypePattern](ast_package_classes.md#class-excepttypepattern) 节点中有类型列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ExceptTypePattern](ast_package_classes.md#class-excepttypepattern) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ExceptTypePattern](ast_package_classes.md#class-excepttypepattern) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ExceptTypePattern](ast_package_classes.md#class-excepttypepattern) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ExceptTypePattern](ast_package_classes.md#class-excepttypepattern) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Expr

```cangjie
public open class Expr <: Node
```

功能：所有表达式节点的父类，继承自 [Node](ast_package_classes.md#class-node) 节点。

表达式节点的 `toTokens` 方法会根据操作符优先级添加括号，例如已有一个 [BinaryExpr](ast_package_classes.md#class-binaryexpr) 节点 a \* b, 用户将左表达式内容 a 修改为 a + 1，修改后 `toTokens` 方法会为左表达式添加括号，`toTokens` 输出为 (a + 1) \* b。

父类型：

- [Node](#class-node)

### func dump(UInt16)

```cangjie
protected open func dump(_: UInt16): String
```

功能：将当前语法树节点转化为树形结构的形态并进行打印，需要被子类重写。

参数：

- _: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 格式化输出的缩进空格数量。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化输出内容。

### func precedence()

```cangjie
protected open func precedence(): Int64
```

功能：返回当前表达式节点的优先级。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ExtendDecl

```cangjie
public class ExtendDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个扩展定义节点。

扩展的定义使用 `extend` 关键字，扩展定义依次为：extend 关键字、扩展类型、是否指定父接口、可选的泛型约束、扩展体的定义。

父类型：

- [Decl](#class-decl)

### prop body

```cangjie
public mut prop body: Body
```

功能：获取或设置 [ExtendDecl](ast_package_classes.md#class-extenddecl) 节点的类体。

类型：[Body](ast_package_classes.md#class-body)

### prop extendType

```cangjie
public mut prop extendType: TypeNode
```

功能：获取或设置被扩展的类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### prop identifier

```cangjie
public mut override prop identifier: Token
```

功能：[ExtendDecl](ast_package_classes.md#class-extenddecl) 节点继承 [Decl](ast_package_classes.md#class-decl) 节点，但是不支持 `identifier` 属性，使用时会抛出异常。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当使用 `identifier` 属性时，抛出异常。

### prop superTypeBitAnds

```cangjie
public mut prop superTypeBitAnds: Tokens
```

功能：获取或设置 [ExtendDecl](ast_package_classes.md#class-extenddecl) 节点的父接口声明中的 `&` 操作符的词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 `&` 词法单元序列时，抛出异常。

### prop superTypes

```cangjie
public mut prop superTypes: ArrayList<TypeNode>
```

功能：获取或设置 [ExtendDecl](ast_package_classes.md#class-extenddecl) 节点的父接口。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### prop upperBound

```cangjie
public mut prop upperBound: Token
```

功能：获取或设置 `<:` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `<:` 操作符时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ExtendDecl](ast_package_classes.md#class-extenddecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ExtendDecl](ast_package_classes.md#class-extenddecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ExtendDecl](ast_package_classes.md#class-extenddecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ExtendDecl](ast_package_classes.md#class-extenddecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ForInExpr

```cangjie
public class ForInExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `for-in` 表达式。

[ForInExpr](ast_package_classes.md#class-forinexpr) 类型中，关键字 `for` 之后是 [Pattern](ast_package_classes.md#class-pattern), 此后是一个 `in` 关键字和表达式节点，最后是一个执行循环体 [Block](ast_package_classes.md#class-block)。

父类型：

- [Expr](#class-expr)

### prop block

```cangjie
public mut prop block: Block
```

功能：获取或设置 [ForInExpr](ast_package_classes.md#class-forinexpr) 中的循环体。

类型：[Block](ast_package_classes.md#class-block)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [ForInExpr](ast_package_classes.md#class-forinexpr) 中的表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop keywordF

```cangjie
public mut prop keywordF: Token
```

功能：获取或设置 [ForInExpr](ast_package_classes.md#class-forinexpr) 中的关键字 `for`。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `for` 关键字时，抛出异常。

### prop keywordI

```cangjie
public mut prop keywordI: Token
```

功能：获取或设置 [ForInExpr](ast_package_classes.md#class-forinexpr) 中的关键字 `in`。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `in` 关键字时，抛出异常。

### prop keywordW

```cangjie
public mut prop keywordW: Token
```

功能：获取或设置 [ForInExpr](ast_package_classes.md#class-forinexpr) 中的关键字 `where`。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `where` 关键字时，抛出异常。

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [ForInExpr](ast_package_classes.md#class-forinexpr) 中关键字 `for` 后的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop pattern

```cangjie
public mut prop pattern: Pattern
```

功能：获取或设置 [ForInExpr](ast_package_classes.md#class-forinexpr) 中的 [Pattern](ast_package_classes.md#class-pattern) 节点。

类型：[Pattern](ast_package_classes.md#class-pattern)

### prop patternGuard

```cangjie
public mut prop patternGuard: Expr
```

功能：获取或设置 [ForInExpr](ast_package_classes.md#class-forinexpr) 中的 `patternGuard` 条件表达式。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [ForInExpr](ast_package_classes.md#class-forinexpr) 节点中不存在 `patternGuard` 表达式时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [ForInExpr](ast_package_classes.md#class-forinexpr) 中的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ForInExpr](ast_package_classes.md#class-forinexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ForInExpr](ast_package_classes.md#class-forinexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ForInExpr](ast_package_classes.md#class-forinexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ForInExpr](ast_package_classes.md#class-forinexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class FuncDecl

```cangjie
public class FuncDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个函数定义节点。

由可选的函数修饰符，关键字 `func` ，函数名，可选的类型形参列表，函数参数，可缺省的函数返回类型来定义一个函数，函数定义时必须有函数体，函数体是一个块。

父类型：

- [Decl](#class-decl)

### prop block

```cangjie
public mut prop block: Block
```

功能：获取或设置 [FuncDecl](ast_package_classes.md#class-funcdecl) 节点的函数体。

类型：[Block](ast_package_classes.md#class-block)

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [FuncDecl](ast_package_classes.md#class-funcdecl) 节点的冒号。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是冒号时，抛出异常。

### prop declType

```cangjie
public mut prop declType: TypeNode
```

功能：获取或设置 [FuncDecl](ast_package_classes.md#class-funcdecl) 节点的函数返回类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [FuncDecl](ast_package_classes.md#class-funcdecl) 节点的函数返回类型是一个缺省值时，抛出异常。

### prop funcParams

```cangjie
public mut prop funcParams: ArrayList<FuncParam>
```

功能：获取或设置 [FuncDecl](ast_package_classes.md#class-funcdecl) 节点的函数参数。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[FuncParam](ast_package_classes.md#class-funcparam)>

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [FuncDecl](ast_package_classes.md#class-funcdecl) 节点的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop overloadOp

```cangjie
public mut prop overloadOp: Tokens
```

功能：获取或设置 [FuncDecl](ast_package_classes.md#class-funcdecl) 节点的重载操作符。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [FuncDecl](ast_package_classes.md#class-funcdecl) 节点的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [FuncDecl](ast_package_classes.md#class-funcdecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [FuncDecl](ast_package_classes.md#class-funcdecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [FuncDecl](ast_package_classes.md#class-funcdecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [FuncDecl](ast_package_classes.md#class-funcdecl) 节点时，抛出异常。

### func isConst()

```cangjie
public func isConst(): Bool
```

功能：判断是否是一个 `Const` 类型的节点。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是一个 `Const` 类型的节点返回 true；反之，返回 false。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class FuncParam

```cangjie
public open class FuncParam <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示函数参数节点，包括非命名参数和命名参数。

一个 [FuncParam](ast_package_classes.md#class-funcparam) 节点： `func foo(a: Int64, b: Float64) {...}` 中的 `a: Int64` 和 `b: Float64`。

父类型：

- [Decl](#class-decl)

### prop assign

```cangjie
public mut prop assign: Token
```

功能：获取或设置具有默认值的函数参数中的 `=`。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `=` 时，抛出异常。

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置置形参中的 ":"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ":" 时，抛出异常。

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置具有默认值的函数参数的变量初始化节点。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当函数参数没有进行初始化时，抛出异常。

### prop not

```cangjie
public mut prop not: Token
```

功能：获取或设置命名形参中的 `!`。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `!` 时，抛出异常。

### prop paramType

```cangjie
public mut prop paramType: TypeNode
```

功能：获取或设置函数参数的类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [FuncParam](ast_package_classes.md#class-funcparam) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [FuncParam](ast_package_classes.md#class-funcparam) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [FuncParam](ast_package_classes.md#class-funcparam) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [FuncParam](ast_package_classes.md#class-funcparam) 节点时，抛出异常。

### func dump(UInt16)

```cangjie
protected open func dump(indent: UInt16): String
```

功能：将当前语法树节点转化为树形结构的形态并进行打印。

参数：

- indent: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 格式化输出的缩进空格数量。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化输出内容。

### func isMemberParam()

```cangjie
public func isMemberParam(): Bool
```

功能：当前的函数参数是否是主构造函数中的参数。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 布尔类型，如果是主构造函数中的参数，返回 `true`。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class FuncType

```cangjie
public class FuncType <: TypeNode {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示函数类型节点。

由函数的参数类型和返回类型组成，参数类型与返回类型之间用 `->` 分隔，如：`(Int32) -> Unit`。

父类型：

- [TypeNode](#class-typenode)

### prop arrow

```cangjie
public mut prop arrow: Token
```

功能：获取或设置 [FuncType](ast_package_classes.md#class-functype) 节点参数类型与返回类型之间的 `->`的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `->`的词法单元时，抛出异常。

### prop commas

```cangjie
public mut prop commas: Tokens
```

功能：获取或设置 [FuncType](ast_package_classes.md#class-functype) 节点中的 "," 词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "," 词法单元序列时，抛出异常。

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [FuncType](ast_package_classes.md#class-functype) 节点的中的关键字 `CFunc` 的词法单元，若不是一个 `CFunc` 类型，则获取一个 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [FuncType](ast_package_classes.md#class-functype) 节点的 "(" 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [FuncType](ast_package_classes.md#class-functype) 节点的 ")" 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop returnType

```cangjie
public mut prop returnType: TypeNode
```

功能：获取或设置 [FuncType](ast_package_classes.md#class-functype) 返回类型节点。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### prop types

```cangjie
public mut prop types: ArrayList<TypeNode>
```

功能：获取或设置 [FuncType](ast_package_classes.md#class-functype) 节点中函数的参数类型列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [FuncType](ast_package_classes.md#class-functype) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [FuncType](ast_package_classes.md#class-functype) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [FuncType](ast_package_classes.md#class-functype) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [FuncType](ast_package_classes.md#class-functype) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class GenericConstraint

```cangjie
public class GenericConstraint <: Node {
    public init()
}
```

功能：表示一个泛型约束节点。

一个 [GenericConstraint](ast_package_classes.md#class-genericconstraint) 节点：`interface Enumerable<U> where U <: Bounded {}` 中的 `where U <: Bounded`。

> **说明：**
>
> 通过 `where` 之后的 `<:` 运算符来声明，由一个下界与一个上界来组成。其中 `<:` 左边称为约束的下界，下界只能为类型变元。`<:` 右边称为约束上界，约束上界可以为类型。

父类型：

- [Node](#class-node)

### prop bitAnds

```cangjie
public mut prop bitAnds: Tokens
```

功能：获取或设置 [GenericConstraint](ast_package_classes.md#class-genericconstraint) 节点中的 `&` 操作符的词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 `&` 词法单元序列时，抛出异常。

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [GenericConstraint](ast_package_classes.md#class-genericconstraint) 节点中关键字 `where` 词法单元，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `where` 关键字时，抛出异常。

### prop typeArgument

```cangjie
public mut prop typeArgument: TypeNode
```

功能：获取或设置 [GenericConstraint](ast_package_classes.md#class-genericconstraint) 节点中的约束下界。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### prop upperBound

```cangjie
public mut prop upperBound: Token
```

功能：获取或设置 [GenericConstraint](ast_package_classes.md#class-genericconstraint) 节点中的 `<:` 运算符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `<:` 运算符时，抛出异常。

### prop upperBounds

```cangjie
public mut prop upperBounds: ArrayList<TypeNode>
```

功能：获取或设置 [GenericConstraint](ast_package_classes.md#class-genericconstraint) 节点约束上界的 [TypeNode](ast_package_classes.md#class-typenode) 类型节点的集合。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [GenericConstraint](ast_package_classes.md#class-genericconstraint) 对象。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class GenericParam

```cangjie
public class GenericParam <: Node {
    public init()
    public init(parameters: Tokens)
}
```

功能：表示一个类型形参节点。

一个 [GenericParam](ast_package_classes.md#class-genericparam) 节点：`<T1, T2, T3>`。

> **说明：**
>
> 类型形参用 `<>` 括起并用 "," 分隔多个类型形参名称。

父类型：

- [Node](#class-node)

### prop lAngle

```cangjie
public mut prop lAngle: Token
```

功能：获取或设置 [GenericParam](ast_package_classes.md#class-genericparam) 节点中的左尖括号词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是左尖括号时，抛出异常。

### prop parameters

```cangjie
public mut prop parameters: Tokens
```

功能：获取或设置 [GenericParam](ast_package_classes.md#class-genericparam) 节点中的类型形参的 [Tokens](ast_package_classes.md#class-tokens) 类型，可能为空，如 `<T1, T2, T3>` 中的 `T1` `T2` 和 `T3`。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop rAngle

```cangjie
public mut prop rAngle: Token
```

功能：获取或设置 [GenericParam](ast_package_classes.md#class-genericparam) 节点中的右尖括号词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是右尖括号时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [GenericParam](ast_package_classes.md#class-genericparam) 对象。

### init(Tokens)

```cangjie
public init(parameters: Tokens)
```

功能：构造一个 [GenericParam](ast_package_classes.md#class-genericparam) 对象。

参数：

- parameters: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [GenericParam](ast_package_classes.md#class-genericparam) 的类型形参的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class IfExpr

```cangjie
public class IfExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示条件表达式。

可以根据判定条件是否成立来决定执行哪条代码分支。一个 [IfExpr](ast_package_classes.md#class-ifexpr) 节点中 `if` 是关键字，`if` 之后是一个小括号，小括号内可以是一个表达式或者一个 `let` 声明的解构匹配，接着是一个 [Block](ast_package_classes.md#class-block)，[Block](ast_package_classes.md#class-block) 之后是可选的 `else` 分支。 `else` 分支以 `else` 关键字开始，后接新的 `if` 表达式或一个 [Block](ast_package_classes.md#class-block)。

父类型：

- [Expr](#class-expr)

### prop condition

```cangjie
public mut prop condition: Expr
```

功能：获取或设置 [IfExpr](ast_package_classes.md#class-ifexpr) 节点中的 `if` 后的条件表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop elseExpr

```cangjie
public mut prop elseExpr: Expr
```

功能：获取或设置 [IfExpr](ast_package_classes.md#class-ifexpr) 节点中 `else` 分支节点。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当前 [IfExpr](ast_package_classes.md#class-ifexpr) 节点没有 else 分支节点。

### prop ifBlock

```cangjie
public mut prop ifBlock: Block
```

功能：获取或设置 [IfExpr](ast_package_classes.md#class-ifexpr) 节点中的 `if` 后的 block 节点。

类型：[Block](ast_package_classes.md#class-block)

### prop keywordE

```cangjie
public mut prop keywordE: Token
```

功能：获取或设置 [IfExpr](ast_package_classes.md#class-ifexpr) 节点中 `else` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `else` 关键字时，抛出异常。

### prop keywordI

```cangjie
public mut prop keywordI: Token
```

功能：获取或设置 [IfExpr](ast_package_classes.md#class-ifexpr) 节点中的 `if` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `if` 关键字时，抛出异常。

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [IfExpr](ast_package_classes.md#class-ifexpr) 节点中的 `if` 后的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [IfExpr](ast_package_classes.md#class-ifexpr) 节点中的 `if` 后的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [IfExpr](ast_package_classes.md#class-ifexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [IfExpr](ast_package_classes.md#class-ifexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [IfExpr](ast_package_classes.md#class-ifexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [IfExpr](ast_package_classes.md#class-ifexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ImportContent

```cangjie
public class ImportContent <: Node {
    public init()
}
```

父类型：

- [Node](#class-node)

### prop commas

```cangjie
public mut prop commas: Tokens
```

功能：获取或设置 [ImportContent](ast_package_classes.md#class-importcontent) 节点中的 "," 词法单元序列，只有 `importKind` 为 `ImportKind.Multi` 时非空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "," 词法单元序列时，抛出异常。

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置 [ImportContent](ast_package_classes.md#class-importcontent) 节点中被导入的项，它可能是包中的顶层定义或声明，也可能是子包的名字。

类型：[Token](ast_package_structs.md#struct-token)

### prop importAlias

```cangjie
public mut prop importAlias: Tokens
```

功能：获取或设置 [ImportContent](ast_package_classes.md#class-importcontent) 节点中导入的定义或声明的别名词法单元序列，只有 `importKind` 为 `ImportKind.Alias` 时非空。如：`import packageName.xxx as yyy` 中的 `as yyy`。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop importKind

```cangjie
public mut prop importKind: ImportKind
```

功能：获取或设置 [ImportContent](ast_package_classes.md#class-importcontent) 节点中导入类型。

类型：[ImportKind](ast_package_enums.md#enum-importkind)

### prop items

```cangjie
public mut prop items: ArrayList<ImportContent>
```

功能：获取或设置 [ImportContent](ast_package_classes.md#class-importcontent) 节点中被导入的所有项，只有 `importKind` 为 `ImportKind.Multi` 时非空。

类型：ArrayList\<[ImportContent](ast_package_classes.md#class-importcontent)>

### prop lBrace

```cangjie
public mut prop lBrace: Token
```

功能：获取或设置 [ImportContent](ast_package_classes.md#class-importcontent) 节点中的 `{` 操作符词法单元，只有 `importKind` 为 `ImportKind.Multi` 时非空。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `{` 操作符时，抛出异常。

### prop prefixPaths

```cangjie
public mut prop prefixPaths: Tokens
```

功能：获取或设置 [ImportContent](ast_package_classes.md#class-importcontent) 节点中完整包名的前缀部分的词法单元序列，可能为空。如 `import a.b.c` 中的 `a` 和 `b`。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop prefixDots

```cangjie
public mut prop prefixDots: Tokens
```

功能：获取或设置 [ImportContent](ast_package_classes.md#class-importcontent) 节点中完整包名中用于分隔每层子包的词法单元序列，可能为空。如 `import a.b.c` 中的两个 "."。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "." 词法单元序列时，抛出异常。

### prop rBrace

```cangjie
public mut prop rBrace: Token
```

功能：获取或设置 [ImportContent](ast_package_classes.md#class-importcontent) 节点中的 `}` 操作符词法单元，只有 `importKind` 为 `ImportKind.Multi` 时非空。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `}` 操作符时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ImportContent](ast_package_classes.md#class-importcontent) 对象。

### func isImportAlias()

```cangjie
public func isImportAlias(): Bool
```

功能：判断 [ImportContent](ast_package_classes.md#class-importcontent) 节点是否对导入项取了别名。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [ImportContent](ast_package_classes.md#class-importcontent) 节点是否对导入项取了别名。

### func isImportAll()

```cangjie
public func isImportAll(): Bool
```

功能：判断 [ImportContent](ast_package_classes.md#class-importcontent) 节点是否为全导入。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [ImportContent](ast_package_classes.md#class-importcontent) 节点是否为全导入。

### func isImportMulti()

```cangjie
public func isImportMulti(): Bool
```

功能：判断 [ImportContent](ast_package_classes.md#class-importcontent) 节点是否导入了多个顶级定义或声明。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [ImportContent](ast_package_classes.md#class-importcontent) 节点是否导入了多个顶级定义或声明。

### func isImportSingle()

```cangjie
public func isImportSingle(): Bool
```

功能：判断 [ImportContent](ast_package_classes.md#class-importcontent) 节点是否为单导入。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - [ImportContent](ast_package_classes.md#class-importcontent) 节点是否为单导入。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ImportList

```cangjie
public class ImportList <: Node {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示包导入节点。

一个 [ImportList](ast_package_classes.md#class-importlist) 节点: `import moduleName.packageName.foo as bar`。

> **说明：**
>
> 导入节点以可选的访问性修饰符（`public/protected/internal/private`）加关键字 `import` 开头。以 `import pkga.pkgb.item` 为例，`pkga.pkgb` 为导入的顶级定义或声明所在的包的名字，`item` 为导入的顶级定义或声明。

父类型：

- [Node](#class-node)

### prop content

```cangjie
public mut prop content: ImportContent
```

功能：获取或设置 [ImportList](ast_package_classes.md#class-importlist) 节点中的被导入的具体项。如 `import a.b.c` 中的 `a.b.c` 部分。

类型：[ImportContent](ast_package_classes.md#class-importcontent)

### prop keywordI

```cangjie
public mut prop keywordI: Token
```

功能：获取或设置 [ImportList](ast_package_classes.md#class-importlist) 节点中的 `import` 关键字的词法单元，`I` 为关键字首字母。

类型：[Token](ast_package_structs.md#struct-token)

### prop modifier

```cangjie
public mut prop modifier: Token
```

功能：获取或设置 [ImportList](ast_package_classes.md#class-importlist) 节点中的修饰符，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ImportList](ast_package_classes.md#class-importlist) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ImportList](ast_package_classes.md#class-importlist) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ImportList](ast_package_classes.md#class-importlist) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens)) 序列。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ImportList](ast_package_classes.md#class-importlist) 节点时，抛出异常。

### func isImportMulti()

```cangjie
public func isImportMulti(): Bool
```

功能：判断 [ImportList](ast_package_classes.md#class-importlist) 节点是否导入了多个顶级定义或声明。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果 [ImportList](ast_package_classes.md#class-importlist) 节点导入了多个顶级定义或声明，返回 true；反之，返回 false。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class IncOrDecExpr

```cangjie
public class IncOrDecExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示包含自增操作符（`++`）或自减操作符（`--`）的表达式。

父类型：

- [Expr](#class-expr)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [IncOrDecExpr](ast_package_classes.md#class-incordecexpr) 中的表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop op

```cangjie
public mut prop op: Token
```

功能：获取或设置 [IncOrDecExpr](ast_package_classes.md#class-incordecexpr) 中的操作符。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [IncOrDecExpr](ast_package_classes.md#class-incordecexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [IncOrDecExpr](ast_package_classes.md#class-incordecexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [IncOrDecExpr](ast_package_classes.md#class-incordecexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [IncOrDecExpr](ast_package_classes.md#class-incordecexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class InterfaceDecl

```cangjie
public class InterfaceDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示接口定义节点。

接口的定义使用 `interface` 关键字，接口定义依次为：可缺省的修饰符、interface 关键字、接口名、可选的类型参数、是否指定父接口、可选的泛型约束、接口体的定义。

父类型：

- [Decl](#class-decl)

### prop body

```cangjie
public mut prop body: Body
```

功能：获取或设置 [InterfaceDecl](ast_package_classes.md#class-interfacedecl) 节点的类体。

类型：[Body](ast_package_classes.md#class-body)

### prop superTypeBitAnds

```cangjie
public mut prop superTypeBitAnds: Tokens
```

功能：获取或设置 [InterfaceDecl](ast_package_classes.md#class-interfacedecl) 节点的父接口声明中的 `&` 操作符的词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 `&` 词法单元序列时，抛出异常。

### prop superTypes

```cangjie
public mut prop superTypes: ArrayList<TypeNode>
```

功能：获取或设置 [InterfaceDecl](ast_package_classes.md#class-interfacedecl) 节点的父接口。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### prop upperBound

```cangjie
public mut prop upperBound: Token
```

功能：获取或设置 `<:` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `<:` 操作符时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [InterfaceDecl](ast_package_classes.md#class-interfacedecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [InterfaceDecl](ast_package_classes.md#class-interfacedecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [InterfaceDecl](ast_package_classes.md#class-interfacedecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [InterfaceDecl](ast_package_classes.md#class-interfacedecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class IsExpr

```cangjie
public class IsExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个类型检查表达式。

一个 [IsExpr](ast_package_classes.md#class-isexpr) 表达式：`e is T`，类型为 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool)。其中 e 可以是任何类型的表达式，T 可以是任何类型。

父类型：

- [Expr](#class-expr)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [IsExpr](ast_package_classes.md#class-isexpr) 节点中的表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [IsExpr](ast_package_classes.md#class-isexpr) 节点中的 `is` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `is` 操作符时，抛出异常。

### prop shiftType

```cangjie
public mut prop shiftType: TypeNode
```

功能：获取或设置 [IsExpr](ast_package_classes.md#class-isexpr) 节点中的目标类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [IsExpr](ast_package_classes.md#class-isexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [IsExpr](ast_package_classes.md#class-isexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [IsExpr](ast_package_classes.md#class-isexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [IsExpr](ast_package_classes.md#class-isexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class JumpExpr

```cangjie
public class JumpExpr <: Expr {
    public init()
    public init(kind: Tokens)
}
```

功能：表示循环表达式的循环体中的 `break` 和 `continue`。

父类型：

- [Expr](#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置关键字。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [JumpExpr](ast_package_classes.md#class-jumpexpr) 对象。

### init(Tokens)

```cangjie
public init(kind: Tokens)
```

功能：构造一个 [JumpExpr](ast_package_classes.md#class-jumpexpr) 对象。

参数：

- kind: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [JumpExpr](ast_package_classes.md#class-jumpexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [JumpExpr](ast_package_classes.md#class-jumpexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class LambdaExpr

```cangjie
public class LambdaExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `Lambda` 表达式，是一个匿名的函数。

一个 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 节点有两种形式，一种是有形参的，例如 `{a: Int64 => e1; e2 }`，另一种是无形参的，例如 `{ => e1; e2 }`。

父类型：

- [Expr](#class-expr)

### prop doubleArrow

```cangjie
public mut prop doubleArrow: Token
```

功能：获取或设置 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 中的 `=>`。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `=>` 操作符时，抛出异常。

### prop funcParams

```cangjie
public mut prop funcParams:  ArrayList<FuncParam>
```

功能：获取或设置 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 中的参数列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[FuncParam](ast_package_classes.md#class-funcparam)>

### prop lBrace

```cangjie
public mut prop lBrace: Token
```

功能：获取或设置 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 中的 "{"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "{" 时，抛出异常。

### prop nodes

```cangjie
public mut prop nodes: ArrayList<Node>
```

功能：获取或设置 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 中的表达式或声明节点。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Node](ast_package_classes.md#class-node)>

### prop rBrace

```cangjie
public mut prop rBrace: Token
```

功能：获取或设置 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 中的 "}"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "}" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class LetPatternExpr

```cangjie
public class LetPatternExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `let` 声明的解构匹配节点。

一个 [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 节点：`if (let Some(v) <- x)` 中的 `let Some(v) <- x`。

父类型：

- [Expr](#class-expr)

### prop backArrow

```cangjie
public mut prop backArrow: Token
```

功能：获取或设置 [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 节点中 `<-` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `<-` 操作符时，抛出异常。

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 节点中 `<-` 操作符之后的表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 节点中 `let` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `let` 关键字时，抛出异常。

### prop pattern

```cangjie
public mut prop pattern: Pattern
```

功能：获取或设置 [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 节点中 `let` 之后的 pattern。

类型：[Pattern](ast_package_classes.md#class-pattern)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class LitConstExpr

```cangjie
public class LitConstExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个常量表达式节点。

一个 [LitConstExpr](ast_package_classes.md#class-litconstexpr) 表达式：`"abc"`，`123` 等。

父类型：

- [Expr](#class-expr)

### prop literal

```cangjie
public mut prop literal: Token
```

功能：获取或设置 [LitConstExpr](ast_package_classes.md#class-litconstexpr) 节点中的字面量。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [LitConstExpr](ast_package_classes.md#class-litconstexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [LitConstExpr](ast_package_classes.md#class-litconstexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [LitConstExpr](ast_package_classes.md#class-litconstexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ParenExpr](ast_package_classes.md#class-parenexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class MacroDecl

```cangjie
public class MacroDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个宏定义节点。

一个 [MacroDecl](ast_package_classes.md#class-macrodecl) 节点：`public macro M(input: Tokens): Tokens {...}`。

父类型：

- [Decl](#class-decl)

### prop block

```cangjie
public mut prop block: Block
```

功能：获取或设置 [MacroDecl](ast_package_classes.md#class-macrodecl) 节点的函数体。

类型：[Block](ast_package_classes.md#class-block)

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [MacroDecl](ast_package_classes.md#class-macrodecl) 节点的冒号。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是冒号时，抛出异常。

### prop declType

```cangjie
public mut prop declType: TypeNode
```

功能：获取或设置 [MacroDecl](ast_package_classes.md#class-macrodecl) 节点的函数返回类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [MacroDecl](ast_package_classes.md#class-macrodecl) 节点的函数返回类型是一个缺省值时，抛出异常。

### prop funcParams

```cangjie
public mut prop funcParams: ArrayList<FuncParam>
```

功能：获取或设置 [MacroDecl](ast_package_classes.md#class-macrodecl) 节点的参数。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[FuncParam](ast_package_classes.md#class-funcparam)>

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [MacroDecl](ast_package_classes.md#class-macrodecl) 节点的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [MacroDecl](ast_package_classes.md#class-macrodecl) 节点的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [MacroDecl](ast_package_classes.md#class-macrodecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [MacroDecl](ast_package_classes.md#class-macrodecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [MacroDecl](ast_package_classes.md#class-macrodecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [MacroDecl](ast_package_classes.md#class-macrodecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class MacroExpandDecl

```cangjie
public class MacroExpandDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示宏调用节点。

一个 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 节点： `@M class A {}`。

父类型：

- [Decl](#class-decl)

### prop fullIdentifier

```cangjie
public mut prop fullIdentifier: Token
```

功能：获取或设置宏调用节点的完整标识符。

类型：[Token](ast_package_structs.md#struct-token)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 宏调用的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop lSquare

```cangjie
public mut prop lSquare: Token
```

功能：获取或设置 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 属性宏调用的 "["。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "[" 时，抛出异常。

### prop macroAttrs

```cangjie
public mut prop macroAttrs: Tokens
```

功能：获取或设置 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 属性宏调用的输入。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop macroInputDecl

```cangjie
public mut prop macroInputDecl: Decl
```

功能：获取或设置 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 中的声明节点。

类型：[Decl](ast_package_classes.md#class-decl)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [MacroExpandDecl](ast_package_classes.md#class-macrodecl) 节点中没有声明节点时，抛出异常。

### prop macroInputs

```cangjie
public mut prop macroInputs: Tokens
```

功能：获取或设置 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 宏调用的输入。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 宏调用的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop rSquare

```cangjie
public mut prop rSquare: Token
```

功能：获取或设置 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 属性宏调用的 "]"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "]" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class MacroExpandExpr

```cangjie
public class MacroExpandExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示宏调用节点。

一个 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 节点： `@M (a is Int64)`。

父类型：

- [Expr](#class-expr)

### prop at

```cangjie
public mut prop at: Token
```

功能：获取或设置 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 节点中的 `@` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `@` 操作符时，抛出异常。

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置宏调用节点的标识符。

类型：[Token](ast_package_structs.md#struct-token)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 宏调用的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop lSquare

```cangjie
public mut prop lSquare: Token
```

功能：获取或设置 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 属性宏调用的 "["。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "[" 时，抛出异常。

### prop macroAttrs

```cangjie
public mut prop macroAttrs: Tokens
```

功能：获取或设置 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 属性宏调用的输入。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop macroInputs

```cangjie
public mut prop macroInputs: Tokens
```

功能：获取或设置 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 宏调用的输入。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 宏调用的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop rSquare

```cangjie
public mut prop rSquare: Token
```

功能：获取或设置 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 属性宏调用的 "]"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "]" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class MacroExpandParam

```cangjie
public class MacroExpandParam <: FuncParam {
    public init()
}
```

功能：表示宏调用节点。

一个 [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 节点： `func foo (@M a: Int64)` 中的 `@M a: Int64`。

父类型：

- [FuncParam](#class-funcparam)

### prop fullIdentifier

```cangjie
public mut prop fullIdentifier: Token
```

功能：获取或设置宏调用节点的完整标识符。

类型：[Token](ast_package_structs.md#struct-token)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [MacroExpandParam](ast_package_classes.md#class-macroexpandparam) 宏调用的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop lSquare

```cangjie
public mut prop lSquare: Token
```

功能：获取或设置 [MacroExpandParam](ast_package_classes.md#class-macroexpandparam) 属性宏调用的 "["。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "[" 时，抛出异常。

### prop macroAttrs

```cangjie
public mut prop macroAttrs: Tokens
```

功能：获取或设置 [MacroExpandParam](ast_package_classes.md#class-macroexpandparam) 属性宏调用的输入。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop macroInputDecl

```cangjie
public mut prop macroInputDecl: Decl
```

功能：获取或设置 [MacroExpandParam](ast_package_classes.md#class-macroexpandparam) 中的声明节点。

类型：[Decl](ast_package_classes.md#class-decl)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [MacroExpandParam](ast_package_classes.md#class-macroexpandparam) 节点中没有声明节点时，抛出异常。

### prop macroInputs

```cangjie
public mut prop macroInputs: Tokens
```

功能：获取或设置 [MacroExpandParam](ast_package_classes.md#class-macroexpandparam) 宏调用的输入。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [MacroExpandParam](ast_package_classes.md#class-macroexpandparam) 宏调用的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop rSquare

```cangjie
public mut prop rSquare: Token
```

功能：获取或设置 [MacroExpandParam](ast_package_classes.md#class-macroexpandparam) 属性宏调用的 "]"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "]" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [MacroExpandParam](ast_package_classes.md#class-macroexpandparam) 对象。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class MacroMessage

```cangjie
public class MacroMessage
```

功能：记录内层宏发送的信息。

### func getBool(String)

```cangjie
public func getBool(key: String): Bool
```

功能：获取对应 key 值的 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型信息。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用于检索的关键字的名字。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回存在 key 值对应的 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型的信息。

异常：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 当不存在 key 值对应的 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型的信息时，抛出异常。

### func getInt64(String)

```cangjie
public func getInt64(key: String): Int64
```

功能：获取对应 key 值的 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型信息。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用于检索的关键字的名字。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回存在 key 值对应的 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型的信息。

异常：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 当不存在 key 值对应的 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型的信息时，抛出异常。

### func getString(String)

```cangjie
public func getString(key: String): String
```

功能：获取对应 key 值的 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型信息。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用于检索的关键字的名字。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 返回存在 key 值对应的 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型的信息。

异常：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 当不存在 key 值对应的 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型的信息时，抛出异常。

### func getTokens(String)

```cangjie
public func getTokens(key: String): Tokens
```

功能：获取对应 key 值的 [Tokens](ast_package_classes.md#class-tokens) 类型信息。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用于检索的关键字的名字。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 返回存在 key 值对应的 [Tokens](ast_package_classes.md#class-tokens) 类型的信息。

异常：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 当不存在 key 值对应的 [Tokens](ast_package_classes.md#class-tokens) 类型的信息时，抛出异常。

### func hasItem(String)

```cangjie
public func hasItem(key: String): Bool
```

功能：检查是否有 key 值对应的相关信息。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 用于检索的关键字名字。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 若存在 key 值对应的相关信息，返回 true；反之，返回 false。

## class MainDecl

```cangjie
public class MainDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个 `main` 函数定义节点。

一个 [MainDecl](ast_package_classes.md#class-maindecl) 节点：`main() {}`。

父类型：

- [Decl](#class-decl)

### prop block

```cangjie
public mut prop block: Block
```

功能：获取或设置 [MainDecl](ast_package_classes.md#class-maindecl) 节点的函数体。

类型：[Block](ast_package_classes.md#class-block)

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [MainDecl](ast_package_classes.md#class-maindecl) 节点的冒号。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是冒号时，抛出异常。

### prop declType

```cangjie
public mut prop declType: TypeNode
```

功能：获取或设置 [MainDecl](ast_package_classes.md#class-maindecl) 节点的函数返回类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [MainDecl](ast_package_classes.md#class-maindecl) 节点的函数返回类型是一个缺省值时，抛出异常。

### prop funcParams

```cangjie
public mut prop funcParams: ArrayList<FuncParam>
```

功能：获取或设置 [MainDecl](ast_package_classes.md#class-maindecl) 节点的函数参数。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[FuncParam](ast_package_classes.md#class-funcparam)>

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [MainDecl](ast_package_classes.md#class-maindecl) 节点的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [MainDecl](ast_package_classes.md#class-maindecl) 节点的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [MainDecl](ast_package_classes.md#class-maindecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [MainDecl](ast_package_classes.md#class-maindecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [MainDecl](ast_package_classes.md#class-maindecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [MainDecl](ast_package_classes.md#class-maindecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class MatchCase

```cangjie
public class MatchCase <: Node {
    public init()
}
```

功能：表示 `match` 表达式中的一个 `case` 节点。

一个 [MatchCase](ast_package_classes.md#class-matchcase) 节点：`case failScore where score > 0 => 0`。

> **说明：**
>
> - [MatchCase](ast_package_classes.md#class-matchcase) 以关键字 `case` 开头，后跟 [Expr](ast_package_classes.md#class-expr) 或者一个或多个由 `|` 分隔的相同种类的 `pattern`，一个可选的 `patternguard`，一个 `=>` 和一系列声明或表达式。
> - 该节点与 [MatchExpr](ast_package_classes.md#class-matchexpr) 存在强绑定关系。

父类型：

- [Node](#class-node)

### prop arrow

```cangjie
public mut prop arrow: Token
```

功能：获取或设置 [MatchCase](ast_package_classes.md#class-matchcase) 中的 `=>` 操作符的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `=>` 操作符时，抛出异常。

### prop bitOrs

```cangjie
public mut prop bitOrs: Tokens
```

功能：获取或设置 [MatchCase](ast_package_classes.md#class-matchcase) 中的 `|` 操作符的词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 `|` 词法单元序列时，抛出异常。

### prop block

```cangjie
public mut prop block: Block
```

功能：获取或设置 [MatchCase](ast_package_classes.md#class-matchcase) 中的一系列声明或表达式节点。

类型：[Block](ast_package_classes.md#class-block)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [MatchCase](ast_package_classes.md#class-matchcase) 中位于 case 后的表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [MatchCase](ast_package_classes.md#class-matchcase) 节点中不存在表达式节点时，抛出异常。

### prop keywordC

```cangjie
public mut prop keywordC: Token
```

功能：获取或设置 [MatchCase](ast_package_classes.md#class-matchcase) 内的 `case` 关键字的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `case` 关键字时，抛出异常。

### prop keywordW

```cangjie
public mut prop keywordW: Token
```

功能：获取或设置 [MatchCase](ast_package_classes.md#class-matchcase) 中可选的关键字 `where` 的词法单元，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `where` 关键字时，抛出异常。

### prop patternGuard

```cangjie
public mut prop patternGuard: Expr
```

功能：获取或设置 [MatchCase](ast_package_classes.md#class-matchcase) 中可选的 pattern guard 表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [MatchCase](ast_package_classes.md#class-matchcase) 节点中不存在 pattern guard 表达式时，抛出异常。

### prop patterns

```cangjie
public mut prop patterns: ArrayList<Pattern>
```

功能：获取或设置 [MatchCase](ast_package_classes.md#class-matchcase) 中位于 case 后的 `pattern` 列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Pattern](ast_package_classes.md#class-pattern)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [MatchCase](ast_package_classes.md#class-matchcase) 对象。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class MatchExpr

```cangjie
public class MatchExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示模式匹配表达式实现模式匹配。

模式匹配表达式分为带 selector 的 `match` 表达式和不带 selector 的 `match` 表达式。

父类型：

- [Expr](#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [MatchExpr](ast_package_classes.md#class-matchexpr) 节点中 `match` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `matcch` 关键字时，抛出异常。

### prop lBrace

```cangjie
public mut prop lBrace: Token
```

功能：获取或设置 [MatchExpr](ast_package_classes.md#class-matchexpr) 之后的 "{"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "{" 时，抛出异常。

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [MatchExpr](ast_package_classes.md#class-matchexpr) 之后的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop matchCases

```cangjie
public mut prop matchCases: ArrayList<MatchCase>
```

功能：获取或设置 [MatchExpr](ast_package_classes.md#class-matchexpr) 内的 `matchCase`, `matchCase` 以关键字 `case` 开头，后跟一个或者多个由 [Pattern](ast_package_classes.md#class-pattern) 或 [Expr](ast_package_classes.md#class-expr)节点，具体见 [MatchCase](ast_package_classes.md#class-matchcase)。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[MatchCase](ast_package_classes.md#class-matchcase)>

### prop rBrace

```cangjie
public mut prop rBrace: Token
```

功能：获取或设置 [MatchExpr](ast_package_classes.md#class-matchexpr) 之后的 "}"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "}" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [MatchExpr](ast_package_classes.md#class-matchexpr) 之后的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop selector

```cangjie
public mut prop selector: Expr
```

功能：获取或设置关键字 `match` 之后的 [Expr](ast_package_classes.md#class-expr)。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当该表达式是一个不带 selector 的 `match` 表达式时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [MatchExpr](ast_package_classes.md#class-matchexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [MatchExpr](ast_package_classes.md#class-matchexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [MatchExpr](ast_package_classes.md#class-matchexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [MatchExpr](ast_package_classes.md#class-matchexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class MemberAccess

```cangjie
public class MemberAccess <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示成员访问表达式。

可以用于访问 class、interface、struct 等类型的成员。一个 [MemberAccess](ast_package_classes.md#class-memberaccess) 节点的形式为 `T.a`，`T` 为成员访问表达式的主体，`a` 表示成员的名字。

父类型：

- [Expr](#class-expr)

### prop baseExpr

```cangjie
public mut prop baseExpr: Expr
```

功能：获取或设置 [MemberAccess](ast_package_classes.md#class-memberaccess) 节点的成员访问表达式主体。

类型：[Expr](ast_package_classes.md#class-expr)

### prop commas

```cangjie
public mut prop commas: Tokens
```

功能：获取或设置 [MemberAccess](ast_package_classes.md#class-memberaccess) 节点中的 "," 词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "," 词法单元序列时，抛出异常。

### prop dot

```cangjie
public mut prop dot: Token
```

功能：获取或设置 [MemberAccess](ast_package_classes.md#class-memberaccess) 节点中的 "."。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "." 词法单元类型时，抛出异常。

### prop field

```cangjie
public mut prop field: Token
```

功能：获取或设置 [MemberAccess](ast_package_classes.md#class-memberaccess) 节点成员的名字。

类型：[Token](ast_package_structs.md#struct-token)

### prop lAngle

```cangjie
public mut prop lAngle: Token
```

功能：获取或设置 [MemberAccess](ast_package_classes.md#class-memberaccess) 节点中的左尖括号。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是左尖括号时，抛出异常。

### prop rAngle

```cangjie
public mut prop rAngle: Token
```

功能：获取或设置 [MemberAccess](ast_package_classes.md#class-memberaccess) 节点中的右尖括号。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是右尖括号时，抛出异常。

### prop typeArguments

```cangjie
public mut prop typeArguments: ArrayList<TypeNode>
```

功能：获取或设置 [MemberAccess](ast_package_classes.md#class-memberaccess) 节点中的实例化类型。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [MemberAccess](ast_package_classes.md#class-memberaccess) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [MemberAccess](ast_package_classes.md#class-memberaccess) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [MemberAccess](ast_package_classes.md#class-memberaccess) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [MemberAccess](ast_package_classes.md#class-memberaccess) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Modifier

```cangjie
public class Modifier <: Node {
    public init()
    public init(keyword: Token)
}
```

功能：表示该定义具备某些特性，通常放在定义处的最前端。

一个 [Modifier](ast_package_classes.md#class-modifier) 节点：`public func foo()` 中的 `public`。

父类型：

- [Node](#class-node)

### prop keyword(Token)

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [Modifier](ast_package_classes.md#class-modifier) 节点中的修饰符词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Modifier](ast_package_classes.md#class-modifier) 对象。

### init(Token)

```cangjie
public init(keyword: Token)
```

功能：构造一个 [Modifier](ast_package_classes.md#class-modifier) 对象。

参数：

- keyword: [Token](ast_package_structs.md#struct-token) - 将要构造 [Modifier](ast_package_classes.md#class-modifier) 类型的词法单元。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Node

```cangjie
abstract sealed class Node <: ToTokens
```

功能：所有仓颉语法树节点的父类。

该类提供了所有数据类型通用的操作接口。

父类型：

- [ToTokens](ast_package_interfaces.md#interface-totokens)

### prop beginPos

```cangjie
public mut prop beginPos: Position
```

功能：获取或设置当前节点的起始的位置信息。

类型：[Position](ast_package_structs.md#struct-position)

### prop endPos

```cangjie
public mut prop endPos: Position
```

功能：获取或设置当前节点的终止的位置信息。

类型：[Position](ast_package_structs.md#struct-position)

### func dump()

```cangjie
public func dump(): Unit
```

功能：将当前语法树节点转化为树形结构的形态并进行打印。

语法树节点的树形结构将按照以下形式进行输出：

- `-` 字符串：表示当前节点的公共属性， 如 `-keyword` , `-identifier`。
- 节点属性后紧跟该节点的具体类型， 如 `-declType: PrimitiveType` 表示节点类型是一个 [PrimitiveType](ast_package_classes.md#class-primitivetype) 节点。
- 每个类型使用大括号表示类型的作用区间。

语法树输出的详细格式请参见[语法树节点打印](../ast_samples/dump.md)。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class OptionalExpr

```cangjie
public class OptionalExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个带有问号操作符的表达式节点。

一个 [OptionalExpr](ast_package_classes.md#class-optionalexpr) 节点：`a?.b, a?(b), a?[b]` 中的 `a?`。

父类型：

- [Expr](#class-expr)

### prop baseExpr

```cangjie
public mut prop baseExpr: Expr
```

功能：获取或设置 [OptionalExpr](ast_package_classes.md#class-optionalexpr) 的表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

### prop quest

```cangjie
public mut prop quest: Token
```

功能：获取或设置 [OptionalExpr](ast_package_classes.md#class-optionalexpr) 中的问号操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是问号操作符时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [OptionalExpr](ast_package_classes.md#class-optionalexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [OptionalExpr](ast_package_classes.md#class-optionalexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [OptionalExpr](ast_package_classes.md#class-optionalexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [OptionalExpr](ast_package_classes.md#class-optionalexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class PackageHeader

```cangjie
public class PackageHeader <: Node {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示包声明节点。

一个 [PackageHeader](ast_package_classes.md#class-packageheader) 节点: `package define` 或者 `macro package define`。

> **说明：**
>
> 包声明以关键字 `package` 或 `macro package` 开头，后面紧跟包名，且包声明必须在源文件的首行。

父类型：

- [Node](#class-node)

### prop accessible

```cangjie
public mut prop accessible: Token
```

功能：获取或设置 [PackageHeader](ast_package_classes.md#class-packageheader) 节点中的访问性修饰符的词法单元，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### prop keywordM

```cangjie
public mut prop keywordM: Token
```

功能：获取或设置 [PackageHeader](ast_package_classes.md#class-packageheader) 节点中的 `macro` 关键字的词法单元（`M` 为关键字首字母，下同），可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `macro` 关键字时，抛出异常。

### prop keywordP

```cangjie
public mut prop keywordP: Token
```

功能：获取或设置 [PackageHeader](ast_package_classes.md#class-packageheader) 节点中的 `package` 关键字的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `package` 关键字时，抛出异常。

### prop prefixPaths

```cangjie
public mut prop prefixPaths: Tokens
```

功能：获取或设置 [PackageHeader](ast_package_classes.md#class-packageheader) 节点中完整包名的前缀部分的词法单元序列，可能为空。如 `package a.b.c` 中的 `a` 和 `b`。

类型：[Tokens](ast_package_classes.md#class-tokens)

### prop prefixDots

```cangjie
public mut prop prefixDots: Tokens
```

功能：获取或设置 [PackageHeader](ast_package_classes.md#class-packageheader) 节点中完整包名中用于分隔每层子包的词法单元序列，可能为空。如 `package a.b.c` 中的两个 "."。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "." 词法单元序列时，抛出异常。

### prop packageIdentifier

```cangjie
public mut prop packageIdentifier: Token
```

功能：获取或设置 [PackageHeader](ast_package_classes.md#class-packageheader) 节点中当前包的名字，如果当前包为 root 包，即为完整包名，若当前包为子包，则为最后一个 "." 后的名字。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [PackageHeader](ast_package_classes.md#class-packageheader) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [PackageHeader](ast_package_classes.md#class-packageheader) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [PackageHeader](ast_package_classes.md#class-packageheader) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens)) 序列。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [PackageHeader](ast_package_classes.md#class-packageheader) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ParenExpr

```cangjie
public class ParenExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个括号表达式节点，是指使用圆括号括起来的表达式。

一个 [ParenExpr](ast_package_classes.md#class-parenexpr) 节点：`(1 + 2)`。

父类型：

- [Expr](#class-expr)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [ParenExpr](ast_package_classes.md#class-parenexpr) 节点中的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop parenthesizedExpr

```cangjie
public mut prop parenthesizedExpr: Expr
```

功能：获取或设置 [ParenExpr](ast_package_classes.md#class-parenexpr) 节点中由圆括号括起来的子表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [ParenExpr](ast_package_classes.md#class-parenexpr) 节点中的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ParenExpr](ast_package_classes.md#class-parenexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ParenExpr](ast_package_classes.md#class-parenexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ParenExpr](ast_package_classes.md#class-parenexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ParenExpr](ast_package_classes.md#class-parenexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ParenType

```cangjie
public class ParenType <: TypeNode {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示括号类型节点。

例如 `var a: (Int64)` 中的 `(Int64)`。

父类型：

- [TypeNode](#class-typenode)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [ParenType](ast_package_classes.md#class-parentype) 节点中的 "(" 词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop parenthesizedType

```cangjie
public mut prop parenthesizedType: TypeNode
```

功能：获取或设置 [ParenType](ast_package_classes.md#class-parentype) 节点中括起来的类型，如 `(Int64)` 中的 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [ParenType](ast_package_classes.md#class-parentype) 节点中的 ")" 词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ParenType](ast_package_classes.md#class-parentype) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ParenType](ast_package_classes.md#class-parentype) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ParenType](ast_package_classes.md#class-parentype) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ParenType](ast_package_classes.md#class-parentype) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Pattern

```cangjie
public open class Pattern <: Node
```

功能：所有模式匹配节点的父类，继承自 [Node](ast_package_classes.md#class-node) 节点。

父类型：

- [Node](#class-node)

### func dump(UInt16)

```cangjie
protected open func dump(_: UInt16): String
```

功能：将当前语法树节点转化为树形结构的形态并进行打印，需要被子类重写。

参数：

- _: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 格式化输出的缩进空格数量。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化输出内容。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class PrefixType

```cangjie
public class PrefixType <: TypeNode {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示带问号的前缀类型节点。

例如 `var a : ?A` 中的 `?A`。

父类型：

- [TypeNode](#class-typenode)

### prop baseType

```cangjie
public mut prop baseType: TypeNode
```

功能：获取或设置 [PrefixType](ast_package_classes.md#class-prefixtype) 节点中的类型节点，如 `var a: ?A` 中的 `A`。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### prop prefixOps

```cangjie
public mut prop prefixOps: Tokens
```

功能：获取或设置 [PrefixType](ast_package_classes.md#class-prefixtype) 节点中前缀操作符集合。

类型：[Tokens](ast_package_classes.md#class-tokens)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [PrefixType](ast_package_classes.md#class-prefixtype) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [PrefixType](ast_package_classes.md#class-prefixtype) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [PrefixType](ast_package_classes.md#class-prefixtype) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [PrefixType](ast_package_classes.md#class-prefixtype) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class PrimaryCtorDecl

```cangjie
public class PrimaryCtorDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个主构造函数节点。

主构造函数节点由修饰符，主构造函数名，形参列表和主构造函数体构成。

父类型：

- [Decl](#class-decl)

### prop block

```cangjie
public mut prop block: Block
```

功能：获取或设置 [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 节点的主构造函数体。

类型：[Block](ast_package_classes.md#class-block)

### prop funcParams

```cangjie
public mut prop funcParams: ArrayList<FuncParam>
```

功能：获取或设置 [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 节点的参数。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[FuncParam](ast_package_classes.md#class-funcparam)>

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 节点的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 节点的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 节点时，抛出异常。

### func isConst()

```cangjie
public func isConst(): Bool
```

功能：判断是否是一个 `Const` 类型的节点。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当前节点为 `Const` 类型的节点时，返回 true；反之，返回 false。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class PrimitiveType

```cangjie
public class PrimitiveType <: TypeNode {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个基本类型节点。

例如数值类型，[Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型，布尔类型等。

父类型：

- [TypeNode](#class-typenode)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置构造 [PrimitiveType](ast_package_classes.md#class-primitivetype) 类型的关键字，如 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [PrimitiveType](ast_package_classes.md#class-primitivetype) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [PrimitiveType](ast_package_classes.md#class-primitivetype) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [PrimitiveType](ast_package_classes.md#class-primitivetype) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [PrimitiveType](ast_package_classes.md#class-primitivetype) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class PrimitiveTypeExpr

```cangjie
public class PrimitiveTypeExpr <: Expr {
    public init()
    public init(kind: Tokens)
}
```

功能：表示基本类型表达式节点。

[PrimitiveTypeExpr](ast_package_classes.md#class-primitivetypeexpr) 节点：编译器内置的基本类型作为表达式出现在节点中。如 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64).toSting() 中的 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)。

父类型：

- [Expr](#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [PrimitiveTypeExpr](ast_package_classes.md#class-primitivetypeexpr) 中的基本类型关键字。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [PrimitiveTypeExpr](ast_package_classes.md#class-primitivetypeexpr) 对象。

### init(Tokens)

```cangjie
public init(kind: Tokens)
```

功能：构造一个 [PrimitiveTypeExpr](ast_package_classes.md#class-primitivetypeexpr) 对象。

参数：

- kind: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [PrimitiveTypeExpr](ast_package_classes.md#class-primitivetypeexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [PrimitiveTypeExpr](ast_package_classes.md#class-primitivetypeexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Program

```cangjie
public class Program <: Node {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个仓颉源码文件节点。

一个仓颉源码文件节点主要包括包定义节点，包导入节点和 TopLevel 作用域内的所有声明节点。

> **说明：**
>
> 任何一个仓颉源码文件都可以被解析为一个 [Program](ast_package_classes.md#class-program) 类型。

父类型：

- [Node](#class-node)

### prop decls

```cangjie
public mut prop decls: ArrayList<Decl>
```

功能：获取或设置仓颉源码文件中 TopLevel 作用域内定义的声明节点列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Decl](ast_package_classes.md#class-decl)>

### prop importLists

```cangjie
public mut prop importLists: ArrayList<ImportList>
```

功能：获取或设置仓颉源码文件中包导入节点 [ImportList](ast_package_classes.md#class-importlist) 的列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[ImportList](ast_package_classes.md#class-importlist)>

### prop packageHeader

```cangjie
public mut prop packageHeader: PackageHeader
```

功能：获取或设置仓颉源码文件中包的声明节点 [PackageHeader](ast_package_classes.md#class-packageheader)。

类型：[PackageHeader](ast_package_classes.md#class-packageheader)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Program](ast_package_classes.md#class-program) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [Program](ast_package_classes.md#class-program) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [Program](ast_package_classes.md#class-program) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens)) 序列。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为一个文件节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class PropDecl

```cangjie
public class PropDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个属性定义节点。

一个 [PropDecl](ast_package_classes.md#class-propdecl) 节点：`prop X: Int64 { get() { 0 } }`。

父类型：

- [Decl](#class-decl)

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [PropDecl](ast_package_classes.md#class-propdecl) 节点的冒号。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是冒号时，抛出异常。

### prop declType

```cangjie
public mut prop declType : TypeNode
```

功能：获取或设置 [PropDecl](ast_package_classes.md#class-propdecl) 节点的返回类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### prop getter

```cangjie
public mut prop getter: FuncDecl
```

功能：获取或设置 [PropDecl](ast_package_classes.md#class-propdecl) 节点的 getter 函数。

类型：[FuncDecl](ast_package_classes.md#class-funcdecl)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [PropDecl](ast_package_classes.md#class-propdecl) 节点不存在 getter 函数时，抛出异常。

### prop lBrace

```cangjie
public mut prop lBrace: Token
```

功能：获取或设置 [PropDecl](ast_package_classes.md#class-propdecl) 节点的 "{"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "{" 时，抛出异常。

### prop rBrace

```cangjie
public mut prop rBrace: Token
```

功能：获取或设置 [PropDecl](ast_package_classes.md#class-propdecl) 节点的 "}"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "}" 时，抛出异常。

### prop setter

```cangjie
public mut prop setter: FuncDecl
```

功能：获取或设置 [PropDecl](ast_package_classes.md#class-propdecl) 节点的 setter 函数。

类型：[FuncDecl](ast_package_classes.md#class-funcdecl)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [PropDecl](ast_package_classes.md#class-propdecl) 节点不存在 setter 函数时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [PropDecl](ast_package_classes.md#class-propdecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [PropDecl](ast_package_classes.md#class-propdecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [PropDecl](ast_package_classes.md#class-propdecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [PropDecl](ast_package_classes.md#class-propdecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class QualifiedType

```cangjie
public class QualifiedType <: TypeNode {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个用户自定义成员类型。

例如 `var a : T.a` 中的 `T.a`, 其中 T 是包名，a 是从 T 包中导入的类型。

父类型：

- [TypeNode](#class-typenode)

### prop baseType

```cangjie
public mut prop baseType: TypeNode
```

功能：获取或设置 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 节点的成员访问类型主体，如 `var a : T.a` 中的 `T`。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### prop commas

```cangjie
public mut prop commas: Tokens
```

功能：获取或设置 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 节点中的 "," 词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "," 词法单元序列时，抛出异常。

### prop dot

```cangjie
public mut prop dot: Token
```

功能：获取或设置 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 节点中的 "." 。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "." 词法单元时，抛出异常。

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 节点成员的标识符，如 `var a : T.a` 中的 `a`。

类型：[Token](ast_package_structs.md#struct-token)

### prop lAngle

```cangjie
public mut prop lAngle: Token
```

功能：获取或设置 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 节点中的左尖括号词法单元，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是左尖括号时，抛出异常。

### prop rAngle

```cangjie
public mut prop rAngle: Token
```

功能：获取或设置 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 节点中的右尖括号词法单元，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是右尖括号时，抛出异常。

### prop typeArguments

```cangjie
public mut prop typeArguments: ArrayList<TypeNode>
```

功能：获取或设置 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 节点中的实例化类型的列表，如 `T.a<Int32>` 中的 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)，列表可能为空。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [QualifiedType](ast_package_classes.md#class-qualifiedtype) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class QuoteExpr

```cangjie
public class QuoteExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `quote` 表达式节点。

一个 [QuoteExpr](ast_package_classes.md#class-quoteexpr) 节点： `quote(var ident = 0)`。

父类型：

- [Expr](#class-expr)

### prop exprs

```cangjie
public mut prop exprs: ArrayList<Expr>
```

功能：获取或设置 [QuoteExpr](ast_package_classes.md#class-quoteexpr) 中由 `()` 括起的内部引用表达式节点。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Expr](ast_package_classes.md#class-expr)>

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [QuoteExpr](ast_package_classes.md#class-quoteexpr) 的 `quote` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `quote` 关键字时，抛出异常。

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [QuoteExpr](ast_package_classes.md#class-quoteexpr) 中的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [QuoteExpr](ast_package_classes.md#class-quoteexpr) 中的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [QuoteExpr](ast_package_classes.md#class-quoteexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [QuoteExpr](ast_package_classes.md#class-quoteexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [QuoteExpr](ast_package_classes.md#class-quoteexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [QuoteExpr](ast_package_classes.md#class-quoteexpr) 节点。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class QuoteToken

```cangjie
public class QuoteToken <: Expr
```

功能：表示 `quote` 表达式节点内任意合法的 `token`。

父类型：

- [Expr](#class-expr)

### prop tokens

```cangjie
public mut prop tokens: Tokens
```

功能：获取 [QuoteToken](ast_package_classes.md#class-quotetoken) 内的 [Tokens](ast_package_classes.md#class-tokens)。

类型：[Tokens](ast_package_classes.md#class-tokens)

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class RangeExpr

```cangjie
public class RangeExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示包含区间操作符的表达式。

[RangeExpr](ast_package_classes.md#class-rangeexpr) 节点：存在两种 [Range](../../core/core_package_api/core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet) 操作符：`..` 和 `..=`，分别用于创建左闭右开和左闭右闭的 [Range](../../core/core_package_api/core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet) 实例。它们的使用方式分别为 `start..end:step` 和 `start..=end:step`。

父类型：

- [Expr](#class-expr)

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [RangeExpr](ast_package_classes.md#class-rangeexpr) 中的 ":" 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ":" 操作符时，抛出异常。

### prop end

```cangjie
public mut prop end: Expr
```

功能：获取或设置 [RangeExpr](ast_package_classes.md#class-rangeexpr) 中的终止值。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 终止表达式省略。只有在 [Range](../../core/core_package_api/core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> 类型的实例用在下标操作符 `[]` 为空的场景。

### prop op

```cangjie
public mut prop op: Token
```

功能：获取或设置 [RangeExpr](ast_package_classes.md#class-rangeexpr) 中的 [Range](../../core/core_package_api/core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet) 的操作符。

类型：[Token](ast_package_structs.md#struct-token)

### prop start

```cangjie
public mut prop start: Expr
```

功能：获取或设置 [RangeExpr](ast_package_classes.md#class-rangeexpr) 中的起始值。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 起始表达式省略。只有在 [Range](../../core/core_package_api/core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> 类型的实例用在下标操作符 `[]` 为空的场景。

### prop step

```cangjie
public mut prop step: Expr
```

功能：获取或设置 [RangeExpr](ast_package_classes.md#class-rangeexpr) 中序列中前后两个元素之间的差值。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [RangeExpr](ast_package_classes.md#class-rangeexpr) 中未设置序列前后两个元素之间的差值时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [RangeExpr](ast_package_classes.md#class-rangeexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [RangeExpr](ast_package_classes.md#class-rangeexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [RangeExpr](ast_package_classes.md#class-rangeexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [RangeExpr](ast_package_classes.md#class-rangeexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class RefExpr

```cangjie
public class RefExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示引用一个声明的表达式节点。

一个 [RefExpr](ast_package_classes.md#class-refexpr) 节点：`var b = a + 1` 中的 `a` 是一个 [RefExpr](ast_package_classes.md#class-refexpr)。

父类型：

- [Expr](#class-expr)

### prop commas

```cangjie
public mut prop commas: Tokens
```

功能：获取或设置 [RefExpr](ast_package_classes.md#class-refexpr) 节点中的 "," 词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "," 词法单元序列时，抛出异常。

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置 [RefExpr](ast_package_classes.md#class-refexpr) 节点中的自定义类型的标识符。

类型：[Token](ast_package_structs.md#struct-token)

### prop lAngle

```cangjie
public mut prop lAngle: Token
```

功能：获取或设置 [RefExpr](ast_package_classes.md#class-refexpr) 节点中的左尖括号。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是左尖括号时，抛出异常。

### prop rAngle

```cangjie
public mut prop rAngle: Token
```

功能：获取或设置 [RefExpr](ast_package_classes.md#class-refexpr) 节点中的右尖括号。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是右尖括号时，抛出异常。

### prop typeArguments

```cangjie
public mut prop typeArguments: ArrayList<TypeNode>
```

功能：获取或设置 [RefExpr](ast_package_classes.md#class-refexpr) 节点中的实例化类型。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [RefExpr](ast_package_classes.md#class-refexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [RefExpr](ast_package_classes.md#class-refexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [RefExpr](ast_package_classes.md#class-refexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [RefExpr](ast_package_classes.md#class-refexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class RefType

```cangjie
public class RefType <: TypeNode {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个非基础类型节点。

例如用户通过 `class`、`struct`、`enum` 等定义的自定义类型，以及 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)、[String](../../core/core_package_api/core_package_structs.md#struct-string) 等内置类型都可以使用 [RefType](ast_package_classes.md#class-reftype) 表示。例如 `var a : A` 中的 `A`。

父类型：

- [TypeNode](#class-typenode)

### prop commas

```cangjie
public mut prop commas: Tokens
```

功能：获取或设置 [RefType](ast_package_classes.md#class-reftype) 节点中的 "," 词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "," 词法单元序列时，抛出异常。

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置构造 [RefType](ast_package_classes.md#class-reftype) 类型的关键字，如 `var a : A = A()` 中的 `A`。

类型：[Token](ast_package_structs.md#struct-token)

### prop lAngle

```cangjie
public mut prop lAngle: Token
```

功能：获取或设置 [RefType](ast_package_classes.md#class-reftype) 节点中的左尖括号词法单元，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是左尖括号时，抛出异常。

### prop rAngle

```cangjie
public mut prop rAngle: Token
```

功能：获取或设置 [RefType](ast_package_classes.md#class-reftype) 节点中的右尖括号词法单元，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是右尖括号时，抛出异常。

### prop typeArguments

```cangjie
public mut prop typeArguments: ArrayList<TypeNode>
```

功能：获取或设置 [RefType](ast_package_classes.md#class-reftype) 节点中的实例化类型的列表，可能为空，如 `var a : Array<Int32>` 中的 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [RefType](ast_package_classes.md#class-reftype) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [RefType](ast_package_classes.md#class-reftype) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [RefType](ast_package_classes.md#class-reftype) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [RefType](ast_package_classes.md#class-reftype) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ReturnExpr

```cangjie
public class ReturnExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `return` 表达式节点。

一个 [ReturnExpr](ast_package_classes.md#class-returnexpr) 节点：`return 1`。

父类型：

- [Expr](#class-expr)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [ReturnExpr](ast_package_classes.md#class-returnexpr) 节点中的表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [ReturnExpr](ast_package_classes.md#class-returnexpr) 节点没有表达式时，抛出异常。

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [ReturnExpr](ast_package_classes.md#class-returnexpr) 节点中的关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `return` 关键字时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ReturnExpr](ast_package_classes.md#class-returnexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ReturnExpr](ast_package_classes.md#class-returnexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ReturnExpr](ast_package_classes.md#class-returnexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ReturnExpr](ast_package_classes.md#class-returnexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class SpawnExpr

```cangjie
public class SpawnExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `Spawn` 表达式。

一个 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 节点由 `spawn` 关键字和一个不包含形参的闭包组成，例如：`spawn { add(1, 2) }`。

父类型：

- [Expr](#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 中的 `spawn` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `spawn` 关键字时，抛出异常。

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 中的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop lambdaExpr

```cangjie
public mut prop lambdaExpr: LambdaExpr
```

功能：获取或设置 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 中的不含形参的闭包。

类型：[LambdaExpr](ast_package_classes.md#class-lambdaexpr)

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 中的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop threadContext

```cangjie
public mut prop threadContext: Expr
```

功能：获取或设置 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 中的线程上下文环境表达式。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 中不含有上下文表达式时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [SpawnExpr](ast_package_classes.md#class-spawnexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class StructDecl

```cangjie
public class StructDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个 `Struct` 节点。

Struct 的定义使用 `struct` 关键字，定义依次为：可缺省的修饰符、struct 关键字、struct 名、可选的类型参数、是否指定父接口、可选的泛型约束、struct 体的定义。

父类型：

- [Decl](#class-decl)

### prop body

```cangjie
public mut prop body: Body
```

功能：获取或设置 [StructDecl](ast_package_classes.md#class-structdecl) 节点的类体。

类型：[Body](ast_package_classes.md#class-body)

### prop superTypeBitAnds

```cangjie
public mut prop superTypeBitAnds: Tokens
```

功能：获取或设置 [StructDecl](ast_package_classes.md#class-structdecl) 节点的父接口声明中的 `&` 操作符的词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 `&` 词法单元序列时，抛出异常。

### prop superTypes

```cangjie
public mut prop superTypes: ArrayList<TypeNode>
```

功能：获取或设置 [StructDecl](ast_package_classes.md#class-structdecl) 节点的父接口。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### prop upperBound

```cangjie
public mut prop upperBound: Token
```

功能：获取或设置 `<:` 操作符。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `<:` 操作符时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [StructDecl](ast_package_classes.md#class-structdecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [StructDecl](ast_package_classes.md#class-structdecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [StructDecl](ast_package_classes.md#class-structdecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [StructDecl](ast_package_classes.md#class-structdecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class SubscriptExpr

```cangjie
public class SubscriptExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示索引访问表达式。

[SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 节点：用于那些支持索引访问的类型（包括 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt) 类型和 `Tuple` 类型）通过下标来访问其具体位置的元素，如 `arr[0]`。

父类型：

- [Expr](#class-expr)

### prop baseExpr

```cangjie
public mut prop baseExpr: Expr
```

功能：获取或设置 [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 中的表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop indexList

```cangjie
public mut prop indexList: ArrayList<Expr>
```

功能：获取或设置 [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 中的索引表达式序列。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Expr](ast_package_classes.md#class-expr)>

### prop lSquare

```cangjie
public mut prop lSquare: Token
```

功能：获取或设置 [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 中的 "["。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "[" 时，抛出异常。

### prop rSquare

```cangjie
public mut prop rSquare: Token
```

功能：获取或设置 [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 中的 "]"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "]" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class SynchronizedExpr

```cangjie
public class SynchronizedExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `synchronized` 表达式。

一个 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 节点由 `synchronized` 关键字和 `StructuredMutex` 对以及后面的代码块组成, 例如 `synchronized(m) { foo() }`。

父类型：

- [Expr](#class-expr)

### prop block

```cangjie
public mut prop block: Block
```

功能：获取或设置 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 修饰的代码块。

类型：[Block](ast_package_classes.md#class-block)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 中的 `synchronized` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `synchronized` 关键字时，抛出异常。

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 中的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 中的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop structuredMutex

```cangjie
public mut prop structuredMutex: Expr
```

功能：获取或设置 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 中的 `StructuredMutex` 的对象。

类型：[Expr](ast_package_classes.md#class-expr)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ThisType

```cangjie
public class ThisType <: TypeNode {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `This` 类型节点。

父类型：

- [TypeNode](#class-typenode)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [ThisType](ast_package_classes.md#class-thistype) 节点关键字 `This` 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ThisType](ast_package_classes.md#class-thistype) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ThisType](ast_package_classes.md#class-thistype) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ThisType](ast_package_classes.md#class-thistype) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ThisType](ast_package_classes.md#class-thistype) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class ThrowExpr

```cangjie
public class ThrowExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `throw` 表达式节点。

一个 [ThrowExpr](ast_package_classes.md#class-throwexpr) 节点：`throw Exception()`。

父类型：

- [Expr](#class-expr)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [ThrowExpr](ast_package_classes.md#class-throwexpr) 节点中的表达式节点。

类型：[Expr](ast_package_classes.md#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [ThrowExpr](ast_package_classes.md#class-throwexpr) 节点中的关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `throw` 关键字时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [ThrowExpr](ast_package_classes.md#class-throwexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [ThrowExpr](ast_package_classes.md#class-throwexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [ThrowExpr](ast_package_classes.md#class-throwexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [ThrowExpr](ast_package_classes.md#class-throwexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Tokens

```cangjie
public open class Tokens <: ToString & Iterable<Token> & ToBytes {
    public init()
    public init(tokArray: Array<Token>)
    public init(tokArrayList: ArrayList<Token>)
}
```

功能：对 [Token](ast_package_structs.md#struct-token) 序列进行封装的类型。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)
- [Iterable](../../core/core_package_api/core_package_interfaces.md#interface-iterablee)\<[Token](ast_package_structs.md#struct-token)>
- [ToBytes](ast_package_interfaces.md#interface-tobytes)

### var tokens

```cangjie
protected var tokens: ArrayList<Token>
```

功能：获取或设置内部以[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Token](ast_package_structs.md#struct-token)>格式存储的全部[Token](ast_package_structs.md#struct-token)。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Token](ast_package_structs.md#struct-token)>

### prop size

```cangjie
public open prop size: Int64
```

功能：获取 [Tokens](ast_package_classes.md#class-tokens) 对象中 [Token](ast_package_structs.md#struct-token) 类型的数量。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Tokens](ast_package_classes.md#class-tokens) 对象。

### init(Array\<Token>)

```cangjie
public init(tokArray: Array<Token>)
```

功能：构造一个 [Tokens](ast_package_classes.md#class-tokens) 对象。

参数：

- tokArray: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Token](ast_package_structs.md#struct-token)> - 一组包含 [Token](ast_package_structs.md#struct-token) 的 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt) 类型。

### init(ArrayList\<Token>)

```cangjie
public init(tokArrayList: ArrayList<Token>)
```

功能：构造一个 [Tokens](ast_package_classes.md#class-tokens) 对象。

参数：

- tokArrayList: [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Token](ast_package_structs.md#struct-token)> - 一组包含 [Token](ast_package_structs.md#struct-token) 的 [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt) 类型。

### func append(Node)

```cangjie
public func append(node: Node): Tokens
```

功能：将当前的 [Tokens](ast_package_classes.md#class-tokens) 与传入节点所转换得到的 [Tokens](ast_package_classes.md#class-tokens) 进行拼接。

参数：

- node: [Node](ast_package_classes.md#class-node) - 待拼接的 [Node](ast_package_classes.md#class-node) 对象。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 拼接后的 [Tokens](ast_package_classes.md#class-tokens) 类型。

### func append(Token)

```cangjie
public open func append(token: Token): Tokens
```

功能：将当前的 [Tokens](ast_package_classes.md#class-tokens) 与传入的 [Token](ast_package_structs.md#struct-token) 进行拼接。

参数：

- token: [Token](ast_package_structs.md#struct-token) - 待拼接的 [Token](ast_package_structs.md#struct-token) 对象。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 拼接后的 [Tokens](ast_package_classes.md#class-tokens) 类型。

### func append(Tokens)

```cangjie
public open func append(tokens: Tokens): Tokens
```

功能：在当前的 [Tokens](ast_package_classes.md#class-tokens) 后追加传入的 [Tokens](ast_package_classes.md#class-tokens) 进行拼接（该接口性能较其他拼接函数表现更好）。

参数：

- tokens: [Tokens](ast_package_classes.md#class-tokens) - 待拼接的 [Tokens](ast_package_classes.md#class-tokens) 对象。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 拼接后的 [Tokens](ast_package_classes.md#class-tokens) 类型。

### func concat(Tokens)

```cangjie
public func concat(tokens: Tokens): Tokens
```

功能：将当前的 [Tokens](ast_package_classes.md#class-tokens) 与传入的 [Tokens](ast_package_classes.md#class-tokens) 进行拼接。

参数：

- tokens: [Tokens](ast_package_classes.md#class-tokens) - 待拼接的 [Tokens](ast_package_classes.md#class-tokens) 对象。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 拼接后的 [Tokens](ast_package_classes.md#class-tokens)。

### func dump()

```cangjie
public func dump(): Unit
```

功能：将 [Tokens](ast_package_classes.md#class-tokens) 内所有 [Token](ast_package_structs.md#struct-token) 的信息打印出来。

### func get(Int64)

```cangjie
public open func get(index: Int64): Token
```

功能：通过索引值获取 [Token](ast_package_structs.md#struct-token) 元素。

参数：

- index: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 待索引的数值。

返回值：

- [Token](ast_package_structs.md#struct-token) - 指定索引的 [Token](ast_package_structs.md#struct-token)。

异常：

- [IndexOutOfBoundsException](../../core/core_package_api/core_package_exceptions.md#class-indexoutofboundsexception) - 当 `index` 无效时，抛出异常。

### func iterator()

```cangjie
public func iterator(): TokensIterator
```

功能：获取 [Tokens](ast_package_classes.md#class-tokens) 对象中的一个迭代器对象。

返回值：

- [TokensIterator](ast_package_classes.md#class-tokensiterator) - [Tokens](ast_package_classes.md#class-tokens) 对象的迭代器对象。

### func remove(Int64)

```cangjie
public func remove(index: Int64): Tokens
```

功能：删除指定位置的 [Token](ast_package_structs.md#struct-token) 对象。

参数：

- index: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 被删除的 [Token](ast_package_structs.md#struct-token) 的索引。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 删除指定位置的 [Token](ast_package_structs.md#struct-token) 后的 [Tokens](ast_package_classes.md#class-tokens) 对象。

### func toBytes()

```cangjie
public func toBytes(): Array<UInt8>
```

功能：Tokens 类型的序列化。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 序列化后的字节序列。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [Tokens](ast_package_classes.md#class-tokens) 转化为 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 转化后的字符串。

### operator func +(Token)

```cangjie
public operator func +(r: Token): Tokens
```

功能：使用当前 [Tokens](ast_package_classes.md#class-tokens) 与另一个 [Token](ast_package_structs.md#struct-token) 相加以获取新的 [Tokens](ast_package_classes.md#class-tokens)。

参数：

- r: [Token](ast_package_structs.md#struct-token) - 待操作的另一个 [Token](ast_package_structs.md#struct-token) 对象。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 新拼接 [Tokens](ast_package_classes.md#class-tokens) 后的词法单元集合。

### operator func +(Tokens)

```cangjie
public operator func +(r: Tokens): Tokens
```

功能：使用当前 [Tokens](ast_package_classes.md#class-tokens) 与 [Tokens](ast_package_classes.md#class-tokens) 相加以获取新的 [Tokens](ast_package_classes.md#class-tokens) 类型。

参数：

- r: [Tokens](ast_package_classes.md#class-tokens) - 待操作的一组 [Tokens](ast_package_classes.md#class-tokens) 对象。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 新拼接 [Tokens](ast_package_classes.md#class-tokens) 后的词法单元集合。

### operator func \[](Int64)

```cangjie
public operator func [](index: Int64): Token
```

功能：操作符重载，通过索引值获取对应 [Token](ast_package_structs.md#struct-token)。

参数：

- index: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 待索引的数值。

返回值：

- [Token](ast_package_structs.md#struct-token) - 返回索引对应的 [Token](ast_package_structs.md#struct-token)。

异常：

- [IndexOutOfBoundsException](../../core/core_package_api/core_package_exceptions.md#class-indexoutofboundsexception) - 当 `index` 无效时，抛出异常。

### operator func \[](Range\<Int64>)

```cangjie
public open operator func [](range: Range<Int64>): Tokens
```

功能：操作符重载，通过 `range` 获取对应 [Tokens](ast_package_classes.md#class-tokens) 切片。

参数：

- range: [Range](../../core/core_package_api/core_package_structs.md#struct-ranget-where-t--countablet--comparablet--equatablet)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)> - 待索引的切片范围。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 返回切片索引对应的 [Tokens](ast_package_classes.md#class-tokens)。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当 `range.step` 不等于 1 时，抛出异常。
- [IndexOutOfBoundsException](../../core/core_package_api/core_package_exceptions.md#class-indexoutofboundsexception) - 当 range 无效时，抛出异常。

## class TokensIterator

```cangjie
public class TokensIterator <: Iterator<Token> {
    public init(tokens: Tokens)
}
```

功能：实现 [Tokens](ast_package_classes.md#class-tokens) 的迭代器功能。

父类型：

- [Iterator](../../core/core_package_api/core_package_classes.md#class-iteratort)\<[Token](ast_package_structs.md#struct-token)>

### init(Tokens)

```cangjie
public init(tokens: Tokens)
```

功能：构造一个 [TokensIterator](ast_package_classes.md#class-tokensiterator) 对象。

参数：

- tokens: [Tokens](ast_package_classes.md#class-tokens) - 传入 [Tokens](ast_package_classes.md#class-tokens)。

### func next()

```cangjie
public func next(): Option<Token>
```

功能：获取迭代器中的下一个值。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Token](ast_package_structs.md#struct-token)> - 返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Token](ast_package_structs.md#struct-token)> 类型，当遍历结束后，返回 None。

### func peek()

```cangjie
public func peek(): Option<Token>
```

功能：获取迭代器中的当前值。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Token](ast_package_structs.md#struct-token)> - 返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Token](ast_package_structs.md#struct-token)> 类型，当遍历结束后，返回 None。

### func seeing(TokenKind)

```cangjie
public func seeing(kind: TokenKind): Bool
```

功能：判断当前节点的 [Token](ast_package_structs.md#struct-token) 类型是否是传入的类型。

参数：

- kind: [TokenKind](ast_package_enums.md#enum-tokenkind) - 需要判断的 [TokenKind](ast_package_enums.md#enum-tokenkind) 类型。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果当前节点的 [TokenKind](ast_package_enums.md#enum-tokenkind) 与传入类型相同，返回 true，否则返回 false。

## class TrailingClosureExpr

```cangjie
public class TrailingClosureExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示尾随 `Lambda` 节点。

一个 [TrailingClosureExpr](ast_package_classes.md#class-trailingclosureexpr) 节点将 lambda 表达式放在函数调用的尾部，括号外面，如 `f(a){ i => i * i }`。

父类型：

- [Expr](#class-expr)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [TrailingClosureExpr](ast_package_classes.md#class-trailingclosureexpr) 中的表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop lambdaExpr

```cangjie
public mut prop lambdaExpr: LambdaExpr
```

功能：获取或设置 [TrailingClosureExpr](ast_package_classes.md#class-trailingclosureexpr) 中的尾随 lambda。

类型：[LambdaExpr](ast_package_classes.md#class-lambdaexpr)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [TrailingClosureExpr](ast_package_classes.md#class-trailingclosureexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [TrailingClosureExpr](ast_package_classes.md#class-trailingclosureexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [TrailingClosureExpr](ast_package_classes.md#class-trailingclosureexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TrailingClosureExpr](ast_package_classes.md#class-trailingclosureexpr) 节点。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class TryExpr

```cangjie
public class TryExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `try` 表达式节点。

`try` 表达式包括三个部分：`try` 块，`catch` 块和 `finally` 块。

父类型：

- [Expr](#class-expr)

### prop catchBlocks

```cangjie
public mut prop catchBlocks: ArrayList<Block>
```

功能：获取或设置 [TryExpr](ast_package_classes.md#class-tryexpr) 中的 Catch 块。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Block](ast_package_classes.md#class-block)>

### prop catchPatterns

```cangjie
public mut prop catchPatterns: ArrayList<Pattern>
```

功能：获取或设置 [TryExpr](ast_package_classes.md#class-tryexpr) 中通过模式匹配的方式匹配待捕获的异常序列。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Pattern](ast_package_classes.md#class-pattern)>

### prop finallyBlock

```cangjie
public mut prop finallyBlock: Block
```

功能：获取或设置 [TryExpr](ast_package_classes.md#class-tryexpr) 中的关键字 `Finally` 块。

类型：[Block](ast_package_classes.md#class-block)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [TryExpr](ast_package_classes.md#class-tryexpr) 节点无 `Finally` 块节点时，抛出异常。

### prop keywordF

```cangjie
public mut prop keywordF: Token
```

功能：获取或设置 [TryExpr](ast_package_classes.md#class-tryexpr) 中的 `finally` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `finally` 关键字时，抛出异常。

### prop keywordT

```cangjie
public mut prop keywordT: Token
```

功能：获取或设置 [TryExpr](ast_package_classes.md#class-tryexpr) 中的 `try` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `try` 关键字时，抛出异常。

### prop keywordsC

```cangjie
public mut prop keywordsC: Tokens
```

功能：获取或设置 [TryExpr](ast_package_classes.md#class-tryexpr) 中的关键字 `catch`。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `catch` 关键字时，抛出异常。

### prop resourceSpec

```cangjie
public mut prop resourceSpec: ArrayList<VarDecl>
```

功能：获取或设置 [TryExpr](ast_package_classes.md#class-tryexpr) 中 Try-with-resources 类型表达式的实例化对象序列。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[VarDecl](ast_package_classes.md#class-vardecl)>

### prop tryBlock

```cangjie
public mut prop tryBlock: Block
```

功能：获取或设置 [TryExpr](ast_package_classes.md#class-tryexpr) 中由表达式与声明组成的块。

类型：[Block](ast_package_classes.md#class-block)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [TryExpr](ast_package_classes.md#class-tryexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [TryExpr](ast_package_classes.md#class-tryexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [TryExpr](ast_package_classes.md#class-tryexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TryExpr](ast_package_classes.md#class-tryexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class TupleLiteral

```cangjie
public class TupleLiteral <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示元组字面量节点。

[TupleLiteral](ast_package_classes.md#class-tupleliteral) 节点：使用格式 `(expr1, expr2, ... , exprN)` 表示，每个 `expr` 是一个表达式。

父类型：

- [Expr](#class-expr)

### prop elements

```cangjie
public mut prop elements: ArrayList<Expr>
```

功能：获取或设置 [TupleLiteral](ast_package_classes.md#class-tupleliteral) 中的表达式列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Expr](ast_package_classes.md#class-expr)>

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [TupleLiteral](ast_package_classes.md#class-tupleliteral) 中的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [TupleLiteral](ast_package_classes.md#class-tupleliteral) 中的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [TupleLiteral](ast_package_classes.md#class-tupleliteral) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [TupleLiteral](ast_package_classes.md#class-tupleliteral) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [TupleLiteral](ast_package_classes.md#class-tupleliteral) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TupleLiteral](ast_package_classes.md#class-tupleliteral) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class TuplePattern

```cangjie
public class TuplePattern <: Pattern {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 Tuple 模式节点。

用于 `tuple` 值的匹配，如 `case ("Bob", age) => 1` 中的 `("Bob", age)`。

父类型：

- [Pattern](#class-pattern)

### prop commas

```cangjie
public mut prop commas: Tokens
```

功能：获取或设置 [TuplePattern](ast_package_classes.md#class-tuplepattern) 节点中的 "," 词法单元序列，可能为空。

类型：[Tokens](ast_package_classes.md#class-tokens)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Tokens](ast_package_classes.md#class-tokens) 不是 "," 词法单元序列时，抛出异常。

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [TuplePattern](ast_package_classes.md#class-tuplepattern) 节点中的 "(" 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop patterns

```cangjie
public mut prop patterns: ArrayList<Pattern>
```

功能：获取或设置 [TuplePattern](ast_package_classes.md#class-tuplepattern) 节点中的一组 [Pattern](ast_package_classes.md#class-pattern) 节点。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Pattern](ast_package_classes.md#class-pattern)>

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [TuplePattern](ast_package_classes.md#class-tuplepattern) 节点中的 ")" 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [TuplePattern](ast_package_classes.md#class-tuplepattern) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [TuplePattern](ast_package_classes.md#class-tuplepattern) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [TuplePattern](ast_package_classes.md#class-tuplepattern) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TuplePattern](ast_package_classes.md#class-tuplepattern) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class TupleType

```cangjie
public class TupleType <: TypeNode {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示元组类型节点。

例如 `var a : (Int64, Int32)` 中的 `(Int64, Int32)`。

父类型：

- [TypeNode](#class-typenode)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [TupleType](ast_package_classes.md#class-tupletype) 节点中的 "(" 词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [TupleType](ast_package_classes.md#class-tupletype) 节点中的 ")" 词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop types

```cangjie
public mut prop types: ArrayList<TypeNode>
```

功能：获取或设置 [TupleType](ast_package_classes.md#class-tupletype) 节点中的类型节点列表。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[TypeNode](ast_package_classes.md#class-typenode)>

### init()

```cangjie
public init()
```

功能：构造一个默认的 [TupleType](ast_package_classes.md#class-tupletype) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [TupleType](ast_package_classes.md#class-tupletype) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [TupleType](ast_package_classes.md#class-tupletype) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TupleType](ast_package_classes.md#class-tupletype) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class TypeAliasDecl

```cangjie
public class TypeAliasDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示类型别名节点。

一个 [TypeAliasDecl](ast_package_classes.md#class-typealiasdecl) 节点： `type Point2D = Float64`。

> **说明：**
>
> 该节点中 `type` 作为关键字，紧跟任意的合法标识符，其后的 `type` 是任意的 top-level 可见的类型，标识符和 `type` 之间使用 `=` 进行连接。

父类型：

- [Decl](#class-decl)

### prop aliasType

```cangjie
public mut prop aliasType: TypeNode
```

功能：获取或设置将要别名的类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### prop assign

```cangjie
public mut prop assign: Token
```

功能：获取或设置标识符和 `type` 之间的 `=`。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `=` 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [TypeAliasDecl](ast_package_classes.md#class-typealiasdecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [TypeAliasDecl](ast_package_classes.md#class-typealiasdecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [TypeAliasDecl](ast_package_classes.md#class-typealiasdecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TypeAliasDecl](ast_package_classes.md#class-typealiasdecl) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class TypeConvExpr

```cangjie
public class TypeConvExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示类型转换表达式。

用于实现若干数值类型间的转换。一个 [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 节点：`Int8(32)`。

父类型：

- [Expr](#class-expr)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 中进行类型转化的原始表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 中的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 中的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop targetType

```cangjie
public mut prop targetType: PrimitiveType
```

功能：获取或设置 [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 中将要转换到的目标类型。

类型：[PrimitiveType](ast_package_classes.md#class-primitivetype)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class TypeNode

```cangjie
public open class TypeNode <: Node
```

功能：所有类型节点的父类，继承自 [Node](ast_package_classes.md#class-node)。

父类型：

- [Node](#class-node)

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [TypeNode](ast_package_classes.md#class-typenode) 节点中的操作符 ":"，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ":" 操作符时，抛出异常。

### prop typeParameterName

```cangjie
public mut prop typeParameterName: Token
```

功能：获取或设置类型节点的参数，如：`(p1:Int64, p2:Int64)` 中的 `p1` 和 `p2`，可能为 [ILLEGAL](ast_package_enums.md#illegal) 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

### func dump(UInt16)

```cangjie
protected open func dump(indent: UInt16): String
```

功能：将当前语法树节点转化为树形结构的形态并进行打印。

参数：

- indent: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 格式化输出的缩进空格数量。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 格式化输出内容。

## class TypePattern

```cangjie
public class TypePattern <: Pattern {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示类型模式节点。

用于判断一个值的运行时类型是否是某个类型的子类型，如 `case b: Base => 0` 中的 `b: Base`。

父类型：

- [Pattern](#class-pattern)

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [TypePattern](ast_package_classes.md#class-typepattern) 节点中的 ":" 操作符的词法单元节点。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ":" 操作符时，抛出异常。

### prop pattern

```cangjie
public mut prop pattern: Pattern
```

功能：获取或设置 [TypePattern](ast_package_classes.md#class-typepattern) 节点中的模式节点。

类型：[Pattern](ast_package_classes.md#class-pattern)

### prop patternType

```cangjie
public mut prop patternType: TypeNode
```

功能：获取或设置 [TypePattern](ast_package_classes.md#class-typepattern) 节点中的待匹配的模式类型节点。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [TypePattern](ast_package_classes.md#class-typepattern) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [TypePattern](ast_package_classes.md#class-typepattern) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [TypePattern](ast_package_classes.md#class-typepattern) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [TypePattern](ast_package_classes.md#class-typepattern) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class UnaryExpr

```cangjie
public class UnaryExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示一个一元操作表达式节点。

父类型：

- [Expr](#class-expr)

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [UnaryExpr](ast_package_classes.md#class-unaryexpr) 节点中的操作数。

类型：[Expr](ast_package_classes.md#class-expr)

### prop op

```cangjie
public mut prop op: Token
```

功能：获取或设置 [UnaryExpr](ast_package_classes.md#class-unaryexpr) 节点中的一元操作符。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [UnaryExpr](ast_package_classes.md#class-unaryexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [UnaryExpr](ast_package_classes.md#class-unaryexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [UnaryExpr](ast_package_classes.md#class-unaryexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [UnaryExpr](ast_package_classes.md#class-unaryexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class VArrayExpr

```cangjie
public class VArrayExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `VArray` 的实例节点。

一个 [VArrayExpr](ast_package_classes.md#class-varrayexpr) 节点：`let arr: VArray<Int64, $5> = VArray<Int64, $5>({ i => i })` 中的 `VArray<Int64, $5>({ i => i })`。

父类型：

- [Expr](#class-expr)

### prop arguments

```cangjie
public mut prop arguments: ArrayList<Argument>
```

功能：获取或设置 [VArrayExpr](ast_package_classes.md#class-varrayexpr) 中的中的初始化参数序列。

类型：[ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<[Argument](ast_package_classes.md#class-argument)>

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [VArrayExpr](ast_package_classes.md#class-varrayexpr) 中的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [VArrayExpr](ast_package_classes.md#class-varrayexpr) 中的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### prop vArrayType

```cangjie
public mut prop vArrayType: VArrayType
```

功能：获取或设置 [VArrayExpr](ast_package_classes.md#class-varrayexpr) 的 VArray 类型节点。

类型：[VArrayType](ast_package_classes.md#class-varraytype)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [VArrayExpr](ast_package_classes.md#class-varrayexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [VArrayExpr](ast_package_classes.md#class-varrayexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [VArrayExpr](ast_package_classes.md#class-varrayexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [VArrayExpr](ast_package_classes.md#class-varrayexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class VArrayType

```cangjie
public class VArrayType <: TypeNode {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `VArray` 类型节点。

使用泛型 `VArray<T, size: Int64>` 表示 `VArray` 类型。

父类型：

- [TypeNode](#class-typenode)

### prop dollar

```cangjie
public mut prop dollar: Token
```

功能：获取或设置 [VArrayType](ast_package_classes.md#class-varraytype) 节点中的操作符 `$` 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `$` 词法单元时，抛出异常。

### prop elementTy

```cangjie
public mut prop elementTy: TypeNode
```

功能：获取或设置 [VArrayType](ast_package_classes.md#class-varraytype) 节点中的类型变元节点，如 `VArray<Int16, $0>` 中的 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)。

类型：[TypeNode](ast_package_classes.md#class-typenode)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [VArrayType](ast_package_classes.md#class-varraytype) 节点的关键字 `VArray` 的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### prop lAngle

```cangjie
public mut prop lAngle: Token
```

功能：获取或设置 [VArrayType](ast_package_classes.md#class-varraytype) 节点左尖括号的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是左尖括号时，抛出异常。

### prop rAngle

```cangjie
public mut prop rAngle: Token
```

功能：获取或设置 [VArrayType](ast_package_classes.md#class-varraytype) 节点右尖括号的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是右尖括号时，抛出异常。

### prop size

```cangjie
public mut prop size: Token
```

功能：获取或设置 [VArrayType](ast_package_classes.md#class-varraytype) 节点中类型长度的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [VArrayType](ast_package_classes.md#class-varraytype) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [VArrayType](ast_package_classes.md#class-varraytype) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [VArrayType](ast_package_classes.md#class-varraytype) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [VArrayType](ast_package_classes.md#class-varraytype) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class VarDecl

```cangjie
public class VarDecl <: Decl {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示变量定义节点。

一个 [VarDecl](ast_package_classes.md#class-vardecl) 节点: `var a: String`，`var b: Int64 = 1`。

> **说明：**
>
> 变量的定义主要包括如下几个部分：修饰符、关键字、patternsMaybeIrrefutable、变量类型和变量初始值。

父类型：

- [Decl](#class-decl)

### prop assign

```cangjie
public mut prop assign: Token
```

功能：获取或设置 [VarDecl](ast_package_classes.md#class-vardecl) 节点中的赋值操作符的位置信息。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是赋值操作符时，抛出异常。

### prop colon

```cangjie
public mut prop colon: Token
```

功能：获取或设置 [VarDecl](ast_package_classes.md#class-vardecl) 节点中的冒号位置信息。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是冒号时，抛出异常。

### prop declType

```cangjie
public mut prop declType: TypeNode
```

功能：获取或设置 [VarDecl](ast_package_classes.md#class-vardecl) 节点的变量类型。

类型：[TypeNode](ast_package_classes.md#class-typenode)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [VarDecl](ast_package_classes.md#class-vardecl) 节点没有声明变量类型时，抛出异常。

### prop expr

```cangjie
public mut prop expr: Expr
```

功能：获取或设置 [VarDecl](ast_package_classes.md#class-vardecl) 节点的变量初始化节点。

类型：[Expr](ast_package_classes.md#class-expr)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [VarDecl](ast_package_classes.md#class-vardecl) 节点没有对变量进行初始化时，抛出异常。

### prop pattern

```cangjie
public mut prop pattern: Pattern
```

功能：获取或设置 [VarDecl](ast_package_classes.md#class-vardecl) 节点的 pattern 节点。

类型：[Pattern](ast_package_classes.md#class-pattern)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当 [VarDecl](ast_package_classes.md#class-vardecl) 节点没有声明 pattern 节点时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [VarDecl](ast_package_classes.md#class-vardecl) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [VarDecl](ast_package_classes.md#class-vardecl) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [VarDecl](ast_package_classes.md#class-vardecl) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [VarDecl](ast_package_classes.md#class-vardecl) 节点时，抛出异常。

### func isConst()

```cangjie
public func isConst(): Bool
```

功能：判断是否是一个 `Const` 类型的节点。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是一个 `Const` 类型的节点返回 true；反之，返回 false。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class VarOrEnumPattern

```cangjie
public class VarOrEnumPattern <: Pattern {
    public init()
    public init(identifier: Token)
}
```

功能：表示当模式的标识符为 `Enum` 构造器时的节点。

例如 `case RED` 中的 `RED` 为 `Enum` 构造器。

父类型：

- [Pattern](#class-pattern)

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置 [VarOrEnumPattern](ast_package_classes.md#class-varorenumpattern) 节点中的标识符的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [VarOrEnumPattern](ast_package_classes.md#class-varorenumpattern) 对象。

### init(Token)

```cangjie
public init(identifier: Token)
```

功能：构造一个 [VarOrEnumPattern](ast_package_classes.md#class-varorenumpattern) 对象。

参数：

- identifier: [Token](ast_package_structs.md#struct-token) - 将要构造 [VarOrEnumPattern](ast_package_classes.md#class-varorenumpattern) 类型的词法单元。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [VarOrEnumPattern](ast_package_classes.md#class-varorenumpattern) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class VarPattern

```cangjie
public class VarPattern <: Pattern {
    public init()
    public init(identifier: Token)
}
```

功能：表示绑定模式节点。

使用一个合法的标识符表示，如 `for (i in 1..10)` 中的 `i`。

父类型：

- [Pattern](#class-pattern)

### prop identifier

```cangjie
public mut prop identifier: Token
```

功能：获取或设置 [VarPattern](ast_package_classes.md#class-varpattern) 节点中的标识符符的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [VarPattern](ast_package_classes.md#class-varpattern) 对象。

### init(Token)

```cangjie
public init(identifier: Token)
```

功能：构造一个 [VarPattern](ast_package_classes.md#class-varpattern) 对象。

参数：

- identifier: [Token](ast_package_structs.md#struct-token) - 将要构造 [VarPattern](ast_package_classes.md#class-varpattern) 类型的词法单元。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [VarPattern](ast_package_classes.md#class-varpattern) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class Visitor

```cangjie
public abstract class Visitor
```

功能：一个抽象类，其内部默认定义了访问不同类型 AST 节点访问（`visit`）函数。

> **说明：**
>
> - `visit` 函数搭配 `traverse` 一起使用，可实现对节点的访问和修改, 所有 `visit` 函数都有默认为空的实现，可以按需实现需要的 `visit` 方法。
> - 该类需要被继承使用，并允许子类重新定义访问函数。

### func breakTraverse()

```cangjie
public func breakTraverse(): Unit
```

功能：用于重写 `visit` 函数中，通过调用该函数来终止继续遍历子节点的行为。

### func needBreakTraverse()

```cangjie
protected func needBreakTraverse(): Bool
```

功能：用于判断是否需要停止遍历。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

### func visit(Annotation)

```cangjie
protected open func visit(_: Annotation): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Annotation](ast_package_classes.md#class-annotation) - [Annotation](ast_package_classes.md#class-annotation) 类型的被遍历节点。

### func visit(Argument)

```cangjie
protected open func visit(_: Argument): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Argument](ast_package_classes.md#class-argument) - [Argument](ast_package_classes.md#class-argument) 类型的被遍历节点。

### func visit(ArrayLiteral)

```cangjie
protected open func visit(_: ArrayLiteral): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ArrayLiteral](ast_package_classes.md#class-arrayliteral) - [ArrayLiteral](ast_package_classes.md#class-arrayliteral) 类型的被遍历节点。

### func visit(AsExpr)

```cangjie
protected open func visit(_: AsExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [AsExpr](ast_package_classes.md#class-asexpr) - [AsExpr](ast_package_classes.md#class-asexpr) 类型的被遍历节点。

### func visit(AssignExpr)

```cangjie
protected open func visit(_: AssignExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [AssignExpr](ast_package_classes.md#class-assignexpr) - [AssignExpr](ast_package_classes.md#class-assignexpr) 类型的被遍历节点。

### func visit(BinaryExpr)

```cangjie
protected open func visit(_: BinaryExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [BinaryExpr](ast_package_classes.md#class-binaryexpr) - [BinaryExpr](ast_package_classes.md#class-binaryexpr) 类型的被遍历节点。

### func visit(Block)

```cangjie
protected open func visit(_: Block): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Block](ast_package_classes.md#class-block) - [Block](ast_package_classes.md#class-block) 类型的被遍历节点。

### func visit(Body)

```cangjie
protected open func visit(_: Body): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Body](ast_package_classes.md#class-body) - [Body](ast_package_classes.md#class-body) 类型的被遍历节点。

### func visit(CallExpr)

```cangjie
protected open func visit(_: CallExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [CallExpr](ast_package_classes.md#class-callexpr) - [CallExpr](ast_package_classes.md#class-callexpr) 类型的被遍历节点。

### func visit(ClassDecl)

```cangjie
protected open func visit(_: ClassDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ClassDecl](ast_package_classes.md#class-classdecl) - [ClassDecl](ast_package_classes.md#class-classdecl) 类型的被遍历节点。

### func visit(ConstPattern)

```cangjie
protected open func visit(_: ConstPattern): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ConstPattern](ast_package_classes.md#class-constpattern) - [ConstPattern](ast_package_classes.md#class-constpattern) 类型的被遍历节点。

### func visit(Constructor)

```cangjie
protected open func visit(_: Constructor): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Constructor](ast_package_classes.md#class-constructor) - [Constructor](ast_package_classes.md#class-constructor) 类型的被遍历节点。

### func visit(Decl)

```cangjie
protected open func visit(_: Decl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Decl](ast_package_classes.md#class-decl) - [Decl](ast_package_classes.md#class-decl) 类型的被遍历节点。

### func visit(DoWhileExpr)

```cangjie
protected open func visit(_: DoWhileExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) - [DoWhileExpr](ast_package_classes.md#class-dowhileexpr) 类型的被遍历节点。

### func visit(EnumDecl)

```cangjie
protected open func visit(_: EnumDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [EnumDecl](ast_package_classes.md#class-enumdecl) - [EnumDecl](ast_package_classes.md#class-enumdecl) 类型的被遍历节点。

### func visit(EnumPattern)

```cangjie
protected open func visit(_: EnumPattern): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [EnumPattern](ast_package_classes.md#class-enumpattern) - [EnumPattern](ast_package_classes.md#class-enumpattern) 类型的被遍历节点。

### func visit(ExceptTypePattern)

```cangjie
protected open func visit(_: ExceptTypePattern): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ExceptTypePattern](ast_package_classes.md#class-excepttypepattern) - [ExceptTypePattern](ast_package_classes.md#class-excepttypepattern) 类型的被遍历节点。

### func visit(Expr)

```cangjie
protected open func visit(_: Expr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Expr](ast_package_classes.md#class-expr) - [Expr](ast_package_classes.md#class-expr) 类型的被遍历节点。

### func visit(ExtendDecl)

```cangjie
protected open func visit(_: ExtendDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ExtendDecl](ast_package_classes.md#class-extenddecl) - [ExtendDecl](ast_package_classes.md#class-extenddecl) 类型的被遍历节点。

### func visit(ForInExpr)

```cangjie
protected open func visit(_: ForInExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ForInExpr](ast_package_classes.md#class-forinexpr) - [ForInExpr](ast_package_classes.md#class-forinexpr) 类型的被遍历节点。

### func visit(FuncDecl)

```cangjie
protected open func visit(_: FuncDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [FuncDecl](ast_package_classes.md#class-funcdecl) - [FuncDecl](ast_package_classes.md#class-funcdecl) 类型的被遍历节点。

### func visit(FuncParam)

```cangjie
protected open func visit(_: FuncParam): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [FuncParam](ast_package_classes.md#class-funcparam) - [FuncParam](ast_package_classes.md#class-funcparam) 类型的被遍历节点。

### func visit(FuncType)

```cangjie
protected open func visit(_: FuncType): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [FuncType](ast_package_classes.md#class-functype) - [FuncType](ast_package_classes.md#class-functype) 类型的被遍历节点。

### func visit(GenericConstraint)

```cangjie
protected open func visit(_: GenericConstraint): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [GenericConstraint](ast_package_classes.md#class-genericconstraint) - [GenericConstraint](ast_package_classes.md#class-genericconstraint) 类型的被遍历节点。

### func visit(GenericParam)

```cangjie
protected open func visit(_: GenericParam): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [GenericParam](ast_package_classes.md#class-genericparam) - [GenericParam](ast_package_classes.md#class-genericparam) 类型的被遍历节点。

### func visit(IfExpr)

```cangjie
protected open func visit(_: IfExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [IfExpr](ast_package_classes.md#class-ifexpr) - [IfExpr](ast_package_classes.md#class-ifexpr) 类型的被遍历节点。

### func visit(ImportContent)

```cangjie
protected open func visit(_: ImportContent): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ImportContent](ast_package_classes.md#class-importcontent) - [ImportContent](ast_package_classes.md#class-importcontent) 类型的被遍历节点。

### func visit(ImportList)

```cangjie
protected open func visit(_: ImportList): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ImportList](ast_package_classes.md#class-importlist) - [ImportList](ast_package_classes.md#class-importlist) 类型的被遍历节点。

### func visit(IncOrDecExpr)

```cangjie
protected open func visit(_: IncOrDecExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [IncOrDecExpr](ast_package_classes.md#class-incordecexpr) - [IncOrDecExpr](ast_package_classes.md#class-incordecexpr) 类型的被遍历节点。

### func visit(InterfaceDecl)

```cangjie
protected open func visit(_: InterfaceDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [InterfaceDecl](ast_package_classes.md#class-interfacedecl) - [InterfaceDecl](ast_package_classes.md#class-interfacedecl) 类型的被遍历节点。

### func visit(IsExpr)

```cangjie
protected open func visit(_: IsExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [IsExpr](ast_package_classes.md#class-isexpr) - [IsExpr](ast_package_classes.md#class-isexpr) 类型的被遍历节点。

### func visit(JumpExpr)

```cangjie
protected open func visit(_: JumpExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [JumpExpr](ast_package_classes.md#class-jumpexpr) - [JumpExpr](ast_package_classes.md#class-jumpexpr) 类型的被遍历节点。

### func visit(LambdaExpr)

```cangjie
protected open func visit(_: LambdaExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [LambdaExpr](ast_package_classes.md#class-lambdaexpr) - [LambdaExpr](ast_package_classes.md#class-lambdaexpr) 类型的被遍历节点。

### func visit(LetPatternExpr)

```cangjie
protected open func visit(_: LetPatternExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) - [LetPatternExpr](ast_package_classes.md#class-letpatternexpr) 类型的被遍历节点。

### func visit(LitConstExpr)

```cangjie
protected open func visit(_: LitConstExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [LitConstExpr](ast_package_classes.md#class-litconstexpr) - [LitConstExpr](ast_package_classes.md#class-litconstexpr) 类型的被遍历节点。

### func visit(MacroDecl)

```cangjie
protected open func visit(_: MacroDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [MacroDecl](ast_package_classes.md#class-macrodecl) - [MacroDecl](ast_package_classes.md#class-macrodecl) 类型的被遍历节点。

### func visit(MacroExpandDecl)

```cangjie
protected open func visit(_: MacroExpandDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) - [MacroExpandDecl](ast_package_classes.md#class-macroexpanddecl) 类型的被遍历节点。

### func visit(MacroExpandExpr)

```cangjie
protected open func visit(_: MacroExpandExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) - [MacroExpandExpr](ast_package_classes.md#class-macroexpandexpr) 类型的被遍历节点。

### func visit(MainDecl)

```cangjie
protected open func visit(_: MainDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [MainDecl](ast_package_classes.md#class-maindecl) - [MainDecl](ast_package_classes.md#class-maindecl) 类型的被遍历节点。

### func visit(MatchCase)

```cangjie
protected open func visit(_: MatchCase): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [MatchCase](ast_package_classes.md#class-matchcase) - [MatchCase](ast_package_classes.md#class-matchcase) 类型的被遍历节点。

### func visit(MatchExpr)

```cangjie
protected open func visit(_: MatchExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [MatchExpr](ast_package_classes.md#class-matchexpr) - [MatchExpr](ast_package_classes.md#class-matchexpr) 类型的被遍历节点。

### func visit(MemberAccess)

```cangjie
protected open func visit(_: MemberAccess): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [MemberAccess](ast_package_classes.md#class-memberaccess) - [MemberAccess](ast_package_classes.md#class-memberaccess) 类型的被遍历节点。

### func visit(Modifier)

```cangjie
protected open func visit(_: Modifier): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Modifier](ast_package_classes.md#class-modifier) - [Modifier](ast_package_classes.md#class-modifier) 类型的被遍历节点。

### func visit(Node)

```cangjie
protected open func visit(_: Node): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Node](ast_package_classes.md#class-node) - [Node](ast_package_classes.md#class-node) 类型的被遍历节点。

### func visit(OptionalExpr)

```cangjie
protected open func visit(_: OptionalExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [OptionalExpr](ast_package_classes.md#class-optionalexpr) - [OptionalExpr](ast_package_classes.md#class-optionalexpr) 类型的被遍历节点。

### func visit(PackageHeader)

```cangjie
protected open func visit(_: PackageHeader): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [PackageHeader](ast_package_classes.md#class-packageheader) - [PackageHeader](ast_package_classes.md#class-packageheader) 类型的被遍历节点。

### func visit(ParenExpr)

```cangjie
protected open func visit(_: ParenExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ParenExpr](ast_package_classes.md#class-parenexpr) - [ParenExpr](ast_package_classes.md#class-parenexpr) 类型的被遍历节点。

### func visit(ParenType)

```cangjie
protected open func visit(_: ParenType): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ParenType](ast_package_classes.md#class-parentype) - [ParenType](ast_package_classes.md#class-parentype) 类型的被遍历节点。

### func visit(Pattern)

```cangjie
protected open func visit(_: Pattern): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Pattern](ast_package_classes.md#class-pattern) - [Pattern](ast_package_classes.md#class-pattern) 类型的被遍历节点。

### func visit(PrefixType)

```cangjie
protected open func visit(_: PrefixType): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [PrefixType](ast_package_classes.md#class-prefixtype) - [PrefixType](ast_package_classes.md#class-prefixtype) 类型的被遍历节点。

### func visit(PrimaryCtorDecl)

```cangjie
protected open func visit(_: PrimaryCtorDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) - [PrimaryCtorDecl](ast_package_classes.md#class-primaryctordecl) 类型的被遍历节点。

### func visit(PrimitiveType)

```cangjie
protected open func visit(_: PrimitiveType): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [PrimitiveType](ast_package_classes.md#class-primitivetype) - [PrimitiveType](ast_package_classes.md#class-primitivetype) 类型的被遍历节点。

### func visit(PrimitiveTypeExpr)

```cangjie
protected open func visit(_: PrimitiveTypeExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [PrimitiveTypeExpr](ast_package_classes.md#class-primitivetypeexpr) - [PrimitiveTypeExpr](ast_package_classes.md#class-primitivetypeexpr) 类型的被遍历节点。

### func visit(Program)

```cangjie
protected open func visit(_: Program): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [Program](ast_package_classes.md#class-program) - [Program](ast_package_classes.md#class-program) 类型的被遍历节点。

### func visit(PropDecl)

```cangjie
protected open func visit(_: PropDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [PropDecl](ast_package_classes.md#class-propdecl) - [PropDecl](ast_package_classes.md#class-propdecl) 类型的被遍历节点。

### func visit(QualifiedType)

```cangjie
protected open func visit(_: QualifiedType): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [QualifiedType](ast_package_classes.md#class-qualifiedtype) - [QualifiedType](ast_package_classes.md#class-qualifiedtype) 类型的被遍历节点。

### func visit(QuoteExpr)

```cangjie
protected open func visit(_: QuoteExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [QuoteExpr](ast_package_classes.md#class-quoteexpr) - [QuoteExpr](ast_package_classes.md#class-quoteexpr) 类型的被遍历节点。

### func visit(RangeExpr)

```cangjie
protected open func visit(_: RangeExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [RangeExpr](ast_package_classes.md#class-rangeexpr) - [RangeExpr](ast_package_classes.md#class-rangeexpr) 类型的被遍历节点。

### func visit(RefExpr)

```cangjie
protected open func visit(_: RefExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [RefExpr](ast_package_classes.md#class-refexpr) - [RefExpr](ast_package_classes.md#class-refexpr) 类型的被遍历节点。

### func visit(RefType)

```cangjie
protected open func visit(_: RefType): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [RefType](ast_package_classes.md#class-reftype) - [RefType](ast_package_classes.md#class-reftype) 类型的被遍历节点。

### func visit(ReturnExpr)

```cangjie
protected open func visit(_: ReturnExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ReturnExpr](ast_package_classes.md#class-returnexpr) - [ReturnExpr](ast_package_classes.md#class-returnexpr) 类型的被遍历节点。

### func visit(SpawnExpr)

```cangjie
protected open func visit(_: SpawnExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [SpawnExpr](ast_package_classes.md#class-spawnexpr) - [SpawnExpr](ast_package_classes.md#class-spawnexpr) 类型的被遍历节点。

### func visit(StructDecl)

```cangjie
protected open func visit(_: StructDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [StructDecl](ast_package_classes.md#class-structdecl) - [StructDecl](ast_package_classes.md#class-structdecl) 类型的被遍历节点。

### func visit(SubscriptExpr)

```cangjie
protected open func visit(_: SubscriptExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) - [SubscriptExpr](ast_package_classes.md#class-subscriptexpr) 类型的被遍历节点。

### func visit(SynchronizedExpr)

```cangjie
protected open func visit(_: SynchronizedExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) - [SynchronizedExpr](ast_package_classes.md#class-synchronizedexpr) 类型的被遍历节点。

### func visit(ThisType)

```cangjie
protected open func visit(_: ThisType): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ThisType](ast_package_classes.md#class-thistype) - [ThisType](ast_package_classes.md#class-thistype) 类型的被遍历节点。

### func visit(ThrowExpr)

```cangjie
protected open func visit(_: ThrowExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [ThrowExpr](ast_package_classes.md#class-throwexpr) - [ThrowExpr](ast_package_classes.md#class-throwexpr) 类型的被遍历节点。

### func visit(TrailingClosureExpr)

```cangjie
protected open func visit(_: TrailingClosureExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [TrailingClosureExpr](ast_package_classes.md#class-trailingclosureexpr) - [TrailingClosureExpr](ast_package_classes.md#class-trailingclosureexpr) 类型的被遍历节点。

### func visit(TryExpr)

```cangjie
protected open func visit(_: TryExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [TryExpr](ast_package_classes.md#class-tryexpr) - [TryExpr](ast_package_classes.md#class-tryexpr) 类型的被遍历节点。

### func visit(TupleLiteral)

```cangjie
protected open func visit(_: TupleLiteral): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [TupleLiteral](ast_package_classes.md#class-tupleliteral) - [TupleLiteral](ast_package_classes.md#class-tupleliteral) 类型的被遍历节点。

### func visit(TuplePattern)

```cangjie
protected open func visit(_: TuplePattern): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [TuplePattern](ast_package_classes.md#class-tuplepattern) - [TuplePattern](ast_package_classes.md#class-tuplepattern) 类型的被遍历节点。

### func visit(TupleType)

```cangjie
protected open func visit(_: TupleType): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [TupleType](ast_package_classes.md#class-tupletype) - [TupleType](ast_package_classes.md#class-tupletype) 类型的被遍历节点。

### func visit(TypeAliasDecl)

```cangjie
protected open func visit(_: TypeAliasDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [TypeAliasDecl](ast_package_classes.md#class-typealiasdecl) - [TypeAliasDecl](ast_package_classes.md#class-typealiasdecl) 类型的被遍历节点。

### func visit(TypeConvExpr)

```cangjie
protected open func visit(_: TypeConvExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) - [TypeConvExpr](ast_package_classes.md#class-typeconvexpr) 类型的被遍历节点。

### func visit(TypeNode)

```cangjie
protected open func visit(_: TypeNode): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [TypeNode](ast_package_classes.md#class-typenode) - [TypeNode](ast_package_classes.md#class-typenode) 类型的被遍历节点。

### func visit(TypePattern)

```cangjie
protected open func visit(_: TypePattern): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [TypePattern](ast_package_classes.md#class-typepattern) - [TypePattern](ast_package_classes.md#class-typepattern) 类型的被遍历节点。

### func visit(UnaryExpr)

```cangjie
protected open func visit(_: UnaryExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [UnaryExpr](ast_package_classes.md#class-unaryexpr) - [UnaryExpr](ast_package_classes.md#class-unaryexpr) 类型的被遍历节点。

### func visit(VArrayExpr)

```cangjie
protected open func visit(_: VArrayExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [VArrayExpr](ast_package_classes.md#class-varrayexpr) - [VArrayExpr](ast_package_classes.md#class-varrayexpr) 类型的被遍历节点。

### func visit(VArrayType)

```cangjie
protected open func visit(_: VArrayType): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [VArrayType](ast_package_classes.md#class-varraytype) - [VArrayType](ast_package_classes.md#class-varraytype) 类型的被遍历节点。

### func visit(VarDecl)

```cangjie
protected open func visit(_: VarDecl): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [VarDecl](ast_package_classes.md#class-vardecl) - [VarDecl](ast_package_classes.md#class-vardecl) 类型的被遍历节点。

### func visit(VarOrEnumPattern)

```cangjie
protected open func visit(_: VarOrEnumPattern): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [VarOrEnumPattern](ast_package_classes.md#class-varorenumpattern) - [VarOrEnumPattern](ast_package_classes.md#class-varorenumpattern) 类型的被遍历节点。

### func visit(VarPattern)

```cangjie
protected open func visit(_: VarPattern): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [VarPattern](ast_package_classes.md#class-varpattern) - [VarPattern](ast_package_classes.md#class-varpattern) 类型的被遍历节点。

### func visit(WhileExpr)

```cangjie
protected open func visit(_: WhileExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [WhileExpr](ast_package_classes.md#class-whileexpr) - [WhileExpr](ast_package_classes.md#class-whileexpr) 类型的被遍历节点。

### func visit(WildcardExpr)

```cangjie
protected open func visit(_: WildcardExpr): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [WildcardExpr](ast_package_classes.md#class-wildcardexpr) - [WildcardExpr](ast_package_classes.md#class-wildcardexpr) 类型的被遍历节点。

### func visit(WildcardPattern)

```cangjie
protected open func visit(_: WildcardPattern): Unit
```

功能：定义访问节点时的操作，需要重写。

参数：

- _: [WildcardPattern](ast_package_classes.md#class-wildcardpattern) - [WildcardPattern](ast_package_classes.md#class-wildcardpattern) 类型的被遍历节点。

## class WhileExpr

```cangjie
public class WhileExpr <: Expr {
    public init()
    public init(inputs: Tokens)
}
```

功能：表示 `while` 表达式。

`while` 是关键字，`while` 之后是一个小括号，小括号内可以是一个表达式或者一个 `let` 声明的解构匹配，接着是一个 [Block](ast_package_classes.md#class-block) 节点。

父类型：

- [Expr](#class-expr)

### prop block

```cangjie
public mut prop block: Block
```

功能：获取或设置 [WhileExpr](ast_package_classes.md#class-whileexpr) 中的块节点。

类型：[Block](ast_package_classes.md#class-block)

### prop condition

```cangjie
public mut prop condition: Expr
```

功能：获取或设置关键字 [WhileExpr](ast_package_classes.md#class-whileexpr) 中的条件表达式。

类型：[Expr](ast_package_classes.md#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取或设置 [WhileExpr](ast_package_classes.md#class-whileexpr) 节点中 `while` 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 `while` 关键字时，抛出异常。

### prop lParen

```cangjie
public mut prop lParen: Token
```

功能：获取或设置 [WhileExpr](ast_package_classes.md#class-whileexpr) 中 `while` 关键字之后的 "("。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "(" 时，抛出异常。

### prop rParen

```cangjie
public mut prop rParen: Token
```

功能：获取或设置 [WhileExpr](ast_package_classes.md#class-whileexpr) 中 `while` 关键字之后的 ")"。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 ")" 时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [WhileExpr](ast_package_classes.md#class-whileexpr) 对象。

### init(Tokens)

```cangjie
public init(inputs: Tokens)
```

功能：构造一个 [WhileExpr](ast_package_classes.md#class-whileexpr) 对象。

参数：

- inputs: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [WhileExpr](ast_package_classes.md#class-whileexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [WhileExpr](ast_package_classes.md#class-whileexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class WildcardExpr

```cangjie
public class WildcardExpr <: Expr {
    public init()
    public init(keyword: Tokens)
}
```

功能：表示通配符表达式节点。

父类型：

- [Expr](#class-expr)

### prop keyword

```cangjie
public mut prop keyword: Token
```

功能：获取 [WildcardExpr](ast_package_classes.md#class-wildcardexpr) 的 "_" 关键字。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "_" 关键字时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [WildcardExpr](ast_package_classes.md#class-wildcardexpr) 对象。

### init(Tokens)

```cangjie
public init(keyword: Tokens)
```

功能：构造一个 [WildcardExpr](ast_package_classes.md#class-wildcardexpr) 对象。

参数：

- keyword: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [WildcardExpr](ast_package_classes.md#class-wildcardexpr) 类型的词法单元集合 ([Tokens](ast_package_classes.md#class-tokens))。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [WildcardExpr](ast_package_classes.md#class-wildcardexpr) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。

## class WildcardPattern

```cangjie
public class WildcardPattern <: Pattern {
    public init()
    public init(keyword: Tokens)
}
```

功能：表示通配符模式节点。

使用下划线 "_" 表示，可以匹配任意值。

父类型：

- [Pattern](#class-pattern)

### prop wildcard

```cangjie
public mut prop wildcard: Token
```

功能：获取或设置 [WildcardPattern](ast_package_classes.md#class-wildcardpattern) 节点中的 "_" 操作符的词法单元。

类型：[Token](ast_package_structs.md#struct-token)

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当设置的 [Token](ast_package_structs.md#struct-token) 不是 "_" 操作符时，抛出异常。

### init()

```cangjie
public init()
```

功能：构造一个默认的 [WildcardPattern](ast_package_classes.md#class-wildcardpattern) 对象。

### init(Tokens)

```cangjie
public init(keyword: Tokens)
```

功能：构造一个 [WildcardPattern](ast_package_classes.md#class-wildcardpattern) 对象。

参数：

- keyword: [Tokens](ast_package_classes.md#class-tokens) - 将要构造 [WildcardPattern](ast_package_classes.md#class-wildcardpattern) 类型的词法单元集合（[Tokens](ast_package_classes.md#class-tokens)）。

异常：

- [ASTException](ast_package_exceptions.md#class-astexception) - 当输入的 [Tokens](ast_package_classes.md#class-tokens) 类型无法构造为 [WildcardPattern](ast_package_classes.md#class-wildcardpattern) 节点时，抛出异常。

### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：将当前语法树节点转化为 [Tokens](ast_package_classes.md#class-tokens) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转化后的 [Tokens](ast_package_classes.md#class-tokens) 类型节点。

### func traverse(Visitor)

```cangjie
public func traverse(v: Visitor): Unit
```

功能：遍历当前语法树节点及其子节点。若提前终止遍历子节点的行为，可重写 `visit` 函数并调用 `breakTraverse` 函数提前终止遍历行为，请参见[自定义访问函数遍历 AST 对象示例](../ast_samples/traverse.md)。

参数：

- v: [Visitor](ast_package_classes.md#class-visitor) - [Visitor](ast_package_classes.md#class-visitor) 类型的实例。
