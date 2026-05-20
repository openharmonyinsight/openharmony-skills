# 结构体

## struct Position

```cangjie
public struct Position <: ToBytes {
    public let column: Int32
    public let fileID: UInt32
    public let line: Int32
    public init()
    public init(fileID: UInt32, line: Int32, column: Int32)
}
```

功能：表示位置信息的数据结构，包含文件 ID、行号和列号。

父类型：

- [ToBytes](ast_package_interfaces.md#interface-tobytes)

### let column

```cangjie
public let column: Int32
```

功能：获取列号信息。

类型：[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)

### let fileID

```cangjie
public let fileID: UInt32
```

功能：获取文件 ID 信息。

类型：[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)

### let line

```cangjie
public let line: Int32
```

功能：获取行号信息。

类型：[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Position](ast_package_structs.md#struct-position) 实例，其中 `fileID`、`line`、`column` 成员变量均为 `0`。

### init(UInt32, Int32, Int32)

```cangjie
public init(fileID: UInt32, line: Int32, column: Int32)
```

功能：构造一个 [Position](ast_package_structs.md#struct-position) 实例。

参数：

- fileID: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 文件 ID。
- line: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 行号。
- column: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 列号。

### func dump()

```cangjie
public func dump(): Unit
```

功能：将 [Position](ast_package_structs.md#struct-position) 的信息打印出来。

### func isEmpty()

```cangjie
public func isEmpty(): Bool
```

功能：判断行号和列号是否同时为 `0`。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当行号和列号为 `0` 时返回 true。

### func toBytes()

```cangjie
public func toBytes(): Array<UInt8>
```

功能：Position 类型的序列化。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 序列化后的字节序列。

### operator func !=(Position)

```cangjie
public operator func !=(r: Position): Bool
```

功能：比较两个 [Position](ast_package_structs.md#struct-position) 实例是否不等。

参数：

- r: [Position](ast_package_structs.md#struct-position) - 与当前位置比较的另一个位置实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当两个 [Position](ast_package_structs.md#struct-position) 实例不完全相等时返回 true。

### operator func ==(Position)

```cangjie
public operator func ==(r: Position): Bool
```

功能：比较两个 [Position](ast_package_structs.md#struct-position) 实例是否相等。

参数：

- r: [Position](ast_package_structs.md#struct-position) - 与当前位置比较的另一个位置实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当两个 [Position](ast_package_structs.md#struct-position) 实例完全相等时返回 true。

## struct Token

```cangjie
public struct Token <: ToBytes {
    public let kind: TokenKind
    public let pos: Position
    public let value: String
    public var delimiterNum: UInt16 = 1
    public init()
    public init(kind: TokenKind)
    public init(kind: TokenKind, value: String)
}
```

功能：词法单元类型。

词法单元是构成仓颉源码的最小单元，一组合法的词法单元列表经过语法解析后可生成一个语法树节点。

父类型：

- [ToBytes](ast_package_interfaces.md#interface-tobytes)

### let kind

```cangjie
public let kind: TokenKind
```

功能：词法单元的类型。词法单元类型有关键字、标识符、运算符、常量值等，具体见 [TokenKind](ast_package_enums.md#enum-tokenkind) 章节。

类型：[TokenKind](ast_package_enums.md#enum-tokenkind)

### let pos

```cangjie
public let pos: Position
```

功能：词法单元在源码中的位置信息。

类型：[Position](ast_package_structs.md#struct-position)

### let value

```cangjie
public let value: String
```

功能：词法单元的字面量值。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### var delimiterNum

```cangjie
public var delimiterNum: UInt16 = 1
```

功能：多行字符串的 '#' 符号个数。

类型：[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)

### init()

```cangjie
public init()
```

功能：构造一个默认的 [Token](ast_package_structs.md#struct-token) 对象，其中 [TokenKind](ast_package_enums.md#enum-tokenkind) 类型为 `ILLEGAL`，`value` 为空字符串，[Position](ast_package_structs.md#struct-position) 成员变量均为 0。

### init(TokenKind)

```cangjie
public init(kind: TokenKind)
```

功能：根据词法单元类型，构造一个默认的 [Token](ast_package_structs.md#struct-token) 对象。

参数：

- kind: [TokenKind](ast_package_enums.md#enum-tokenkind) - 构建词法单元的类型。

### init(TokenKind, String)

```cangjie
public init(kind: TokenKind, value: String)
```

功能：根据词法单元类型 `kind` 和词法单元值 `value`，构造一个 [Token](ast_package_structs.md#struct-token) 对象。

参数：

- kind: [TokenKind](ast_package_enums.md#enum-tokenkind) - 要构建词法单元的类型。
- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 要构建词法单元的 `value` 值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当输入的 `kind` 与 `value` 不匹配时，抛出异常点。

### func addPosition(UInt32, Int32, Int32)

```cangjie
public func addPosition(fileID: UInt32, line: Int32, colum: Int32): Token
```

功能：补充词法单元的位置信息。

参数：

- fileID: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - [Token](ast_package_structs.md#struct-token) 所在的 fileID。
- line: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - [Token](ast_package_structs.md#struct-token) 所在的行号。
- colum: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - [Token](ast_package_structs.md#struct-token) 所在的列号。

返回值：

- [Token](ast_package_structs.md#struct-token) - 补充完位置信息后的 [Token](ast_package_structs.md#struct-token) 对象。

### func dump()

```cangjie
public func dump(): Unit
```

功能：将 [Token](ast_package_structs.md#struct-token) 的信息打印出来。

### func toBytes()

```cangjie
public func toBytes(): Array<UInt8>
```

功能：Token 类型的序列化。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 序列化后的字节序列。

### operator func !=(Token)

```cangjie
public operator func !=(r: Token): Bool
```

功能：判断两个 [Token](ast_package_structs.md#struct-token) 对象是否不相等。

参数：

- r: [Token](ast_package_structs.md#struct-token) - 待比较的另一个 [Token](ast_package_structs.md#struct-token) 对象。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 两个词法单元的种类 `ID`、值、位置不相同时，返回 true。

### operator func +(Token)

```cangjie
public operator func +(r: Token): Tokens
```

功能：使用当前 [Token](ast_package_structs.md#struct-token) 添加一个 [Token](ast_package_structs.md#struct-token) 以获取新的 [Tokens](ast_package_classes.md#class-tokens)。

参数：

- r: [Token](ast_package_structs.md#struct-token) - 待添加的另一个 [Token](ast_package_structs.md#struct-token) 对象。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 添加新的 [Tokens](ast_package_classes.md#class-tokens) 后的词法单元集合。

### operator func +(Tokens)

```cangjie
public operator func +(r: Tokens): Tokens
```

功能：使用当前 [Token](ast_package_structs.md#struct-token) 添加一个 [Tokens](ast_package_classes.md#class-tokens) 以获取新的 [Tokens](ast_package_classes.md#class-tokens)。

参数：

- r: [Tokens](ast_package_classes.md#class-tokens) - 待添加的另一组 [Token](ast_package_structs.md#struct-token) 对象集合。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 添加新的 [Tokens](ast_package_classes.md#class-tokens) 后的词法单元集合。

### operator func ==(Token)

```cangjie
public operator func ==(r: Token): Bool
```

功能：判断两个 [Token](ast_package_structs.md#struct-token) 对象是否相等。

参数：

- r: [Token](ast_package_structs.md#struct-token) - 待比较的另一个 [Token](ast_package_structs.md#struct-token) 对象。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 两个词法单元的种类 `ID`、值、位置相同时，返回 true。
