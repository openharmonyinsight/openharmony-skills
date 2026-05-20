# 枚举

## enum DiagReportLevel

```cangjie
public enum DiagReportLevel {
    ERROR|
    WARNING
}
```

功能：表示报错接口的信息等级，支持 `ERROR` 和 `WARNING` 两种等级。

### ERROR

```cangjie
ERROR
```

功能：构造一个表示 ERROR 的枚举实例。

### WARNING

```cangjie
WARNING
```

功能：构造一个表示 WARNING 的枚举实例。

### func level()

```cangjie
public func level(): Int32
```

功能：返回枚举值对应的整型。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 枚举值对应的整型。`ERROR` 返回 0，`WARNING` 返回 1。

## enum ImportKind

```cangjie
public enum ImportKind <: ToString {
    Single | Alias | All | Multi
}
```

功能：表示导入语句的类型。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### Single

```cangjie
Single
```

功能：表示单导入，如 `import a.b`。

### Alias

```cangjie
Alias
```

功能：表示别名导入，如 `import a.b as c`。

### All

```cangjie
All
```

功能：表示全导入，如 `import a.b.*`。

### Multi

```cangjie
Multi
```

功能：表示多导入，如 `import a.{b, c, d}`。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [ImportKind](ast_package_enums.md#enum-importkind) 类型转化为字符串类型表示。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - [ImportKind](ast_package_enums.md#enum-importkind) 转换后的字符串值。

## enum TokenKind

```cangjie
public enum TokenKind <: ToString {
    DOT|                      /*  "."           */
    COMMA|                    /*  ","           */
    LPAREN|                   /*  "("           */
    RPAREN|                   /*  ")"           */
    LSQUARE|                  /*  "["           */
    RSQUARE|                  /*  "]"           */
    LCURL|                    /*  "{"           */
    RCURL|                    /*  "}"           */
    EXP|                      /*  "**"          */
    MUL|                      /*  "*"           */
    MOD|                      /*  "%"           */
    DIV|                      /*  "/"           */
    ADD|                      /*  "+"           */
    SUB|                      /*  "-"           */
    INCR|                     /*  "++"          */
    DECR|                     /*  "--"          */
    AND|                      /*  "&&"          */
    OR|                       /*  "||"          */
    COALESCING|               /*  "??"          */
    PIPELINE|                 /*  "|>"          */
    COMPOSITION|              /*  "~>"          */
    NOT|                      /*  "!"           */
    BITAND|                   /*  "&"           */
    BITOR|                    /*  "|"           */
    BITXOR|                   /*  "^"           */
    BITNOT|                   /*  "~"           */
    LSHIFT|                   /*  "<<"          */
    RSHIFT|                   /*  ">>"          */
    COLON|                    /*  ":"           */
    SEMI|                     /*  ";"           */
    ASSIGN|                   /*  "="           */
    ADD_ASSIGN|               /*  "+="          */
    SUB_ASSIGN|               /*  "-="          */
    MUL_ASSIGN|               /*  "*="          */
    EXP_ASSIGN|               /*  "**="         */
    DIV_ASSIGN|               /*  "/="          */
    MOD_ASSIGN|               /*  "%="          */
    AND_ASSIGN|               /*  "&&="         */
    OR_ASSIGN|                /*  "||="         */
    BITAND_ASSIGN|            /*  "&="          */
    BITOR_ASSIGN|             /*  "|="          */
    BITXOR_ASSIGN|            /*  "^="          */
    LSHIFT_ASSIGN|            /*  "<<="         */
    RSHIFT_ASSIGN|            /*  ">>="         */
    ARROW|                    /*  "->"          */
    BACKARROW|                /*  "<-"          */
    DOUBLE_ARROW|             /*  "=>"          */
    RANGEOP|                  /*  ".."          */
    CLOSEDRANGEOP|            /*  "..="         */
    ELLIPSIS|                 /*  "..."         */
    HASH|                     /*  "#"           */
    AT|                       /*  "@"           */
    QUEST|                    /*  "?"           */
    LT|                       /*  "<"           */
    GT|                       /*  ">"           */
    LE|                       /*  "<="          */
    GE|                       /*  ">="          */
    IS|                       /*  "is"          */
    AS|                       /*  "as"          */
    NOTEQ|                    /*  "!="          */
    EQUAL|                    /*  "=="          */
    WILDCARD|                 /*  "_"           */
    INT8|                     /*  "Int8"        */
    INT16|                    /*  "Int16"       */
    INT32|                    /*  "Int32"       */
    INT64|                    /*  "Int64"       */
    INTNATIVE|                /*  "IntNative"   */
    UINT8|                    /*  "UInt8"       */
    UINT16|                   /*  "UInt16"      */
    UINT32|                   /*  "UInt32"      */
    UINT64|                   /*  "UInt64"      */
    UINTNATIVE|               /*  "UIntNative"  */
    FLOAT16|                  /*  "Float16"     */
    FLOAT32|                  /*  "Float32"     */
    FLOAT64|                  /*  "Float64"     */
    RUNE|                     /*  "Rune"        */
    BOOLEAN|                  /*  "Bool"        */
    NOTHING|                  /*  "Nothing"     */
    UNIT|                     /*  "Unit"        */
    STRUCT|                   /*  "struct"      */
    ENUM|                     /*  "enum"        */
    VARRAY|                   /*  "VArray"      */
    THISTYPE|                 /*  "This"        */
    PACKAGE|                  /*  "package"     */
    IMPORT|                   /*  "import"      */
    CLASS|                    /*  "class"       */
    INTERFACE|                /*  "interface"   */
    FUNC|                     /*  "func"        */
    MACRO|                    /*  "macro"       */
    QUOTE|                    /*  "quote"       */
    DOLLAR|                   /*  "$"           */
    LET|                      /*  "let"         */
    VAR|                      /*  "var"         */
    CONST|                    /*  "const"       */
    TYPE|                     /*  "type"        */
    INIT|                     /*  "init"        */
    THIS|                     /*  "this"        */
    SUPER|                    /*  "super"       */
    IF|                       /*  "if"          */
    ELSE|                     /*  "else"        */
    CASE|                     /*  "case"        */
    TRY|                      /*  "try"         */
    CATCH|                    /*  "catch"       */
    FINALLY|                  /*  "finally"     */
    FOR|                      /*  "for"         */
    DO|                       /*  "do"          */
    WHILE|                    /*  "while"       */
    THROW|                    /*  "throw"       */
    RETURN|                   /*  "return"      */
    CONTINUE|                 /*  "continue"    */
    BREAK|                    /*  "break"       */
    IN|                       /*  "in"          */
    NOT_IN|                   /*  "!in"         */
    MATCH|                    /*  "match"       */
    WHERE|                    /*  "where"       */
    EXTEND|                   /*  "extend"      */
    WITH|                     /*  "with"        */
    PROP|                     /*  "prop"        */
    STATIC|                   /*  "static"      */
    PUBLIC|                   /*  "public"      */
    PRIVATE|                  /*  "private"     */
    INTERNAL|                 /*  "internal"    */
    PROTECTED|                /*  "protected"   */
    OVERRIDE|                 /*  "override"    */
    REDEF|                    /*  "redef"       */
    ABSTRACT|                 /*  "abstract"    */
    SEALED|                   /*  "sealed"      */
    OPEN|                     /*  "open"        */
    FOREIGN|                  /*  "foreign"     */
    INOUT|                    /*  "inout"       */
    MUT|                      /*  "mut"         */
    UNSAFE|                   /*  "unsafe"      */
    OPERATOR|                 /*  "operator"    */
    SPAWN|                    /*  "spawn"       */
    SYNCHRONIZED|             /*  "synchronized" */
    UPPERBOUND|               /*  "<:"          */
    MAIN|                     /*  "main"        */
    IDENTIFIER|               /*  "x"           */
    PACKAGE_IDENTIFIER|       /*  e.g. "x-y"  */
    INTEGER_LITERAL|          /*  e.g. "1"      */
    RUNE_BYTE_LITERAL|        /*  e.g. "b'x'"   */
    FLOAT_LITERAL|            /*  e.g. "'1.0'"  */
    COMMENT|                  /*  e.g. "/*xx*/" */
    NL|                       /*  newline         */
    END|                      /*  end of file     */
    SENTINEL|                 /*  ";"             */
    RUNE_LITERAL|             /*  e.g. "r'x'"      */
    STRING_LITERAL|           /*  e.g. ""xx""     */
    SINGLE_QUOTED_STRING_LITERAL|
                              /*  e.g. "'xx'"    */
    JSTRING_LITERAL|          /*  e.g. "J"xx""     */
    MULTILINE_STRING|         /*  e.g. """"aaa""""   */
    MULTILINE_RAW_STRING|     /*  e.g. "#"aaa"#"     */
    BOOL_LITERAL|             /*  "true" or "false"  */
    UNIT_LITERAL|             /*  "()"               */
    DOLLAR_IDENTIFIER|        /*  e.g. "$x"          */
    ANNOTATION|               /*  e.g. "@When"       */
    AT_EXCL|                  /*  e.g. "@!"          */
    ILLEGAL|
    ...
}
```

功能：表示仓颉编译内部所有的词法结构，包括符号、关键字、标识符、换行等。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### ABSTRACT

```cangjie
ABSTRACT
```

功能：构造一个表示 `abstract` 的枚举实例。

### ADD

```cangjie
ADD
```

功能：构造一个表示 `+` 的枚举实例。

### ADD_ASSIGN

```cangjie
ADD_ASSIGN
```

功能：构造一个表示 `+=` 的枚举实例。

### AND

```cangjie
AND
```

功能：构造一个表示 `&&` 的枚举实例。

### AND_ASSIGN

```cangjie
AND_ASSIGN
```

功能：构造一个表示 `&&=` 的枚举实例。

### ANNOTATION

```cangjie
ANNOTATION
```

功能：构造一个表示*注解*的枚举实例。

### ARROW

```cangjie
ARROW
```

功能：构造一个表示 `->` 的枚举实例。

### AS

```cangjie
AS
```

功能：构造一个表示 `as` 的枚举实例。

### ASSIGN

```cangjie
ASSIGN
```

功能：构造一个表示 `=` 的枚举实例。

### AT

```cangjie
AT
```

功能：构造一个表示 `@` 的枚举实例。

### AT_EXCL

```cangjie
AT_EXCL
```

功能：构造一个表示 `@!` 的枚举实例。

### BACKARROW

```cangjie
BACKARROW
```

功能：构造一个表示 `<-` 的枚举实例。

### BITAND

```cangjie
BITAND
```

功能：构造一个表示 `&` 的枚举实例。

### BITAND_ASSIGN

```cangjie
BITAND_ASSIGN
```

功能：构造一个表示 `&=` 的枚举实例。

### BITNOT

```cangjie
BITNOT
```

功能：构造一个表示 `~` 的枚举实例。

### BITOR

```cangjie
BITOR
```

功能：构造一个表示 `|` 的枚举实例。

### BITOR_ASSIGN

```cangjie
BITOR_ASSIGN
```

功能：构造一个表示 `|=` 的枚举实例。

### BITXOR

```cangjie
BITXOR
```

功能：构造一个表示 `^` 的枚举实例。

### BITXOR_ASSIGN

```cangjie
BITXOR_ASSIGN
```

功能：构造一个表示 `^=` 的枚举实例。

### BOOLEAN

```cangjie
BOOLEAN
```

功能：构造一个表示 `bool` 的枚举实例。

### BOOL_LITERAL

```cangjie
BOOL_LITERAL
```

功能：构造一个表示*布尔类型字面量*的枚举实例。

### BREAK

```cangjie
BREAK
```

功能：构造一个表示 `break` 的枚举实例。

### CASE

```cangjie
CASE
```

功能：构造一个表示 `case` 的枚举实例。

### CATCH

```cangjie
CATCH
```

功能：构造一个表示 `catch` 的枚举实例。

### CLASS

```cangjie
CLASS
```

功能：构造一个表示 `class` 的枚举实例。

### CLOSEDRANGEOP

```cangjie
CLOSEDRANGEOP
```

功能：构造一个表示 `..=` 的枚举实例。

### COALESCING

```cangjie
COALESCING
```

功能：构造一个表示 `??` 的枚举实例。

### COLON

```cangjie
COLON
```

功能：构造一个表示 `:` 的枚举实例。

### COMMA

```cangjie
COMMA
```

功能：构造一个表示 `,` 的枚举实例。

### COMMENT

```cangjie
COMMENT
```

功能：构造一个表示*注释*的枚举实例。

### COMPOSITION

```cangjie
COMPOSITION
```

功能：构造一个表示 `~>` 的枚举实例。

### CONST

```cangjie
CONST
```

功能：构造一个表示 `const` 的枚举实例。

### CONTINUE

```cangjie
CONTINUE
```

功能：构造一个表示 `continue` 的枚举实例。

### DECR

```cangjie
DECR
```

功能：构造一个表示 `--` 的枚举实例。

### DIV

```cangjie
DIV
```

功能：构造一个表示 `/` 的枚举实例。

### DIV_ASSIGN

```cangjie
DIV_ASSIGN
```

功能：构造一个表示 `/=` 的枚举实例。

### DO

```cangjie
DO
```

功能：构造一个表示 `do` 的枚举实例。

### DOLLAR

```cangjie
DOLLAR
```

功能：构造一个表示 `$` 的枚举实例。

### DOLLAR_IDENTIFIER

```cangjie
DOLLAR_IDENTIFIER
```

功能：构造一个表示*插值字符串*的枚举实例。

### DOT

```cangjie
DOT
```

功能：构造一个表示 `.` 的枚举实例。

### DOUBLE_ARROW

```cangjie
DOUBLE_ARROW
```

功能：构造一个表示 `=>` 的枚举实例。

### ELLIPSIS

```cangjie
ELLIPSIS
```

功能：构造一个表示 `...` 的枚举实例。

### ELSE

```cangjie
ELSE
```

功能：构造一个表示 `else` 的枚举实例。

### END

```cangjie
END
```

功能：构造一个表示 `EOF` 的枚举实例。

### ENUM

```cangjie
ENUM
```

功能：构造一个表示 `enum` 的枚举实例。

### EQUAL

```cangjie
EQUAL
```

功能：构造一个表示 `==` 的枚举实例。

### EXP

```cangjie
EXP
```

功能：构造一个表示 `**` 的枚举实例。

### EXP_ASSIGN

```cangjie
EXP_ASSIGN
```

功能：构造一个表示 `**=` 的枚举实例。

### EXTEND

```cangjie
EXTEND
```

功能：构造一个表示 `extend` 的枚举实例。

### FINALLY

```cangjie
FINALLY
```

功能：构造一个表示 `finally` 的枚举实例。

### FLOAT16

```cangjie
FLOAT16
```

功能：构造一个表示 `float16` 的枚举实例。

### FLOAT32

```cangjie
FLOAT32
```

功能：构造一个表示 `float32` 的枚举实例。

### FLOAT64

```cangjie
FLOAT64
```

功能：构造一个表示 `float64` 的枚举实例。

### FLOAT_LITERAL

```cangjie
FLOAT_LITERAL
```

功能：构造一个表示*浮点字面量*的枚举实例。

### FOR

```cangjie
FOR
```

功能：构造一个表示 `for` 的枚举实例。

### FOREIGN

```cangjie
FOREIGN
```

功能：构造一个表示 `foreign` 的枚举实例。

### FUNC

```cangjie
FUNC
```

功能：构造一个表示 `func` 的枚举实例。

### GE

```cangjie
GE
```

功能：构造一个表示 `>=` 的枚举实例。

### GT

```cangjie
GT
```

功能：构造一个表示 `>` 的枚举实例。

### HASH

```cangjie
HASH
```

功能：构造一个表示 `#` 的枚举实例。

### IDENTIFIER

```cangjie
IDENTIFIER
```

功能：构造一个表示*标识符*的枚举实例。

### PACKAGE_IDENTIFIER

```cangjie
PACKAGE_IDENTIFIER
```

功能：构造一个表示*包标识符*的枚举实例。

### IF

```cangjie
IF
```

功能：构造一个表示 `if` 的枚举实例。

### ILLEGAL

```cangjie
ILLEGAL
```

功能：构造一个表示*非法*的枚举实例。

### IMPORT

```cangjie
IMPORT
```

功能：构造一个表示 `import` 的枚举实例。

### IN

```cangjie
IN
```

功能：构造一个表示 `in` 的枚举实例。

### INCR

```cangjie
INCR
```

功能：构造一个表示 `++` 的枚举实例。

### INIT

```cangjie
INIT
```

功能：构造一个表示 `init` 的枚举实例。

### INOUT

```cangjie
INOUT
```

功能：构造一个表示 `inout` 的枚举实例。

### INT16

```cangjie
INT16
```

功能：构造一个表示 `int16` 的枚举实例。

### INT32

```cangjie
INT32
```

功能：构造一个表示 `int32` 的枚举实例。

### INT64

```cangjie
INT64
```

功能：构造一个表示 `int64` 的枚举实例。

### INT8

```cangjie
INT8
```

功能：构造一个表示 `int8` 的枚举实例。

### INTEGER_LITERAL

```cangjie
INTEGER_LITERAL
```

功能：构造一个表示*整型字面量*的枚举实例。

### INTERFACE

```cangjie
INTERFACE
```

功能：构造一个表示 `interface` 的枚举实例。

### INTERNAL

```cangjie
INTERNAL
```

功能：构造一个表示 `internal` 的枚举实例。

### INTNATIVE

```cangjie
INTNATIVE
```

功能：构造一个表示 `intnative` 的枚举实例。

### IS

```cangjie
IS
```

功能：构造一个表示 `is` 的枚举实例。

### JSTRING_LITERAL

```cangjie
JSTRING_LITERAL
```

功能：构造一个表示 Java String 字面量的枚举实例。

### LCURL

```cangjie
LCURL
```

功能：构造一个表示 `{` 的枚举实例。

### LE

```cangjie
LE
```

功能：构造一个表示 `<=` 的枚举实例。

### LET

```cangjie
LET
```

功能：构造一个表示 `let` 的枚举实例。

### LPAREN

```cangjie
LPAREN
```

功能：构造一个表示 `(` 的枚举实例。

### LSHIFT

```cangjie
LSHIFT
```

功能：构造一个表示 `<<` 的枚举实例。

### LSHIFT_ASSIGN

```cangjie
LSHIFT_ASSIGN
```

功能：构造一个表示 `<<=` 的枚举实例。

### LSQUARE

```cangjie
LSQUARE
```

功能：构造一个表示 `[` 的枚举实例。

### LT

```cangjie
LT
```

功能：构造一个表示 `<` 的枚举实例。

### MACRO

```cangjie
MACRO
```

功能：构造一个表示 `macro` 的枚举实例。

### MAIN

```cangjie
MAIN
```

功能：构造一个表示 `main` 的枚举实例。

### MATCH

```cangjie
MATCH
```

功能：构造一个表示 `match` 的枚举实例。

### MOD

```cangjie
MOD
```

功能：构造一个表示 `%` 的枚举实例。

### MOD_ASSIGN

```cangjie
MOD_ASSIGN
```

功能：构造一个表示 `%=` 的枚举实例。

### MUL

```cangjie
MUL
```

功能：构造一个表示 `*` 的枚举实例。

### MULTILINE_RAW_STRING

```cangjie
MULTILINE_RAW_STRING
```

功能：构造一个表示*多行原始字符串字面量*的枚举实例。

### MULTILINE_STRING

```cangjie
MULTILINE_STRING
```

功能：构造一个表示*多行字符串字面量*的枚举实例。

### MUL_ASSIGN

```cangjie
MUL_ASSIGN
```

功能：构造一个表示 `*=` 的枚举实例。

### MUT

```cangjie
MUT
```

功能：构造一个表示 `mut` 的枚举实例。

### NL

```cangjie
NL
```

功能：构造一个表示*换行符*的枚举实例。

### NOT

```cangjie
NOT
```

功能：构造一个表示 `!` 的枚举实例。

### NOTEQ

```cangjie
NOTEQ
```

功能：构造一个表示 `!=` 的枚举实例。

### NOTHING

```cangjie
NOTHING
```

功能：构造一个表示 `nothing` 的枚举实例。

### NOT_IN

```cangjie
NOT_IN
```

功能：构造一个表示 `!in` 的枚举实例。

### OPEN

```cangjie
OPEN
```

功能：构造一个表示 `open` 的枚举实例。

### OPERATOR

```cangjie
OPERATOR
```

功能：构造一个表示 `operator` 的枚举实例。

### OR

```cangjie
OR
```

功能：构造一个表示 `||` 的枚举实例。

### OR_ASSIGN

```cangjie
OR_ASSIGN
```

功能：构造一个表示 `||=` 的枚举实例。

### OVERRIDE

```cangjie
OVERRIDE
```

功能：构造一个表示 `override` 的枚举实例。

### PACKAGE

```cangjie
PACKAGE
```

功能：构造一个表示 `package` 的枚举实例。

### PIPELINE

```cangjie
PIPELINE
```

功能：构造一个表示 `|>` 的枚举实例。

### PRIVATE

```cangjie
PRIVATE
```

功能：构造一个表示 `private` 的枚举实例。

### PROP

```cangjie
PROP
```

功能：构造一个表示 `prop` 的枚举实例。

### PROTECTED

```cangjie
PROTECTED
```

功能：构造一个表示 `protected` 的枚举实例。

### PUBLIC

```cangjie
PUBLIC
```

功能：构造一个表示 `public` 的枚举实例。

### QUEST

```cangjie
QUEST
```

功能：构造一个表示 `?` 的枚举实例。

### QUOTE

```cangjie
QUOTE
```

功能：构造一个表示 `quote` 的枚举实例。

### RANGEOP

```cangjie
RANGEOP
```

功能：构造一个表示 `..` 的枚举实例。

### RCURL

```cangjie
RCURL
```

功能：构造一个表示 `}` 的枚举实例。

### REDEF

```cangjie
REDEF
```

功能：构造一个表示 `redef` 的枚举实例。

### RETURN

```cangjie
RETURN
```

功能：构造一个表示 `return` 的枚举实例。

### RPAREN

```cangjie
RPAREN
```

功能：构造一个表示 `)` 的枚举实例。

### RSHIFT

```cangjie
RSHIFT
```

功能：构造一个表示 `>>` 的枚举实例。

### RSHIFT_ASSIGN

```cangjie
RSHIFT_ASSIGN
```

功能：构造一个表示 `>>=` 的枚举实例。

### RSQUARE

```cangjie
RSQUARE
```

功能：构造一个表示 `]` 的枚举实例。

### RUNE

```cangjie
RUNE
```

功能：构造一个表示 `Rune` 的枚举实例。

### RUNE_BYTE_LITERAL

```cangjie
RUNE_BYTE_LITERAL
```

功能：构造一个表示*字符字节字面量*的枚举实例。

### RUNE_LITERAL

```cangjie
RUNE_LITERAL
```

功能：构造一个表示*字符字面量*的枚举实例。

### SEALED

```cangjie
SEALED
```

功能：构造一个表示 `sealed` 的枚举实例。

### SEMI

```cangjie
SEMI
```

功能：构造一个表示 `;` 的枚举实例。

### SENTINEL

```cangjie
SENTINEL
```

功能：构造一个表示 `;` 的枚举实例。

### SINGLE_QUOTED_STRING_LITERAL

```cangjie
SINGLE_QUOTED_STRING_LITERAL
```

功能：构造一个表示*单引号字符串字面量*的枚举实例。

### SPAWN

```cangjie
SPAWN
```

功能：构造一个表示 `spawn` 的枚举实例。

### STATIC

```cangjie
STATIC
```

功能：构造一个表示 `static` 的枚举实例。

### STRING_LITERAL

```cangjie
STRING_LITERAL
```

功能：构造一个表示*双引号字符串字面量*的枚举实例。

### STRUCT

```cangjie
STRUCT
```

功能：构造一个表示 `struct` 的枚举实例。

### SUB

```cangjie
SUB
```

功能：构造一个表示 `-` 的枚举实例。

### SUB_ASSIGN

```cangjie
SUB_ASSIGN
```

功能：构造一个表示 `-=` 的枚举实例。

### SUPER

```cangjie
SUPER
```

功能：构造一个表示 `super` 的枚举实例。

### SYNCHRONIZED

```cangjie
SYNCHRONIZED
```

功能：构造一个表示 `synchronized` 的枚举实例。

### THIS

```cangjie
THIS
```

功能：构造一个表示 `this` 的枚举实例。

### THISTYPE

```cangjie
THISTYPE
```

功能：构造一个表示 `This` 的枚举实例。

### THROW

```cangjie
THROW
```

功能：构造一个表示 `throw` 的枚举实例。

### TRY

```cangjie
TRY
```

功能：构造一个表示 `try` 的枚举实例。

### TYPE

```cangjie
TYPE
```

功能：构造一个表示 `type` 的枚举实例。

### UINT16

```cangjie
UINT16
```

功能：构造一个表示 `uint16` 的枚举实例。

### UINT32

```cangjie
UINT32
```

功能：构造一个表示 `uint32` 的枚举实例。

### UINT64

```cangjie
UINT64
```

功能：构造一个表示 `uint64` 的枚举实例。

### UINT8

```cangjie
UINT8
```

功能：构造一个表示 `uint8` 的枚举实例。

### UINTNATIVE

```cangjie
UINTNATIVE
```

功能：构造一个表示 `uintnative` 的枚举实例。

### UNIT

```cangjie
UNIT
```

功能：构造一个表示 `unit` 的枚举实例。

### UNIT_LITERAL

```cangjie
UNIT_LITERAL
```

功能：构造一个表示 `unit` 字面量的枚举实例。

### UNSAFE

```cangjie
UNSAFE
```

功能：构造一个表示 `unsafe` 的枚举实例。

### UPPERBOUND

```cangjie
UPPERBOUND
```

功能：构造一个表示 `<:` 的枚举实例。

### VAR

```cangjie
VAR
```

功能：构造一个表示 `var` 的枚举实例。

### VARRAY

```cangjie
VARRAY
```

功能：构造一个表示 `varray` 的枚举实例。

### WHERE

```cangjie
WHERE
```

功能：构造一个表示 `where` 的枚举实例。

### WHILE

```cangjie
WHILE
```

功能：构造一个表示 `while` 的枚举实例。

### WILDCARD

```cangjie
WILDCARD
```

功能：构造一个表示 `_` 的枚举实例。

### WITH

```cangjie
WITH
```

功能：构造一个表示 `with` 的枚举实例。

### func !=(TokenKind)

```cangjie
public operator func !=(right: TokenKind): Bool
```

功能：重载不等号操作符，用于比较两个 [TokenKind](ast_package_enums.md#enum-tokenkind) 是否相等。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 布尔类型。

### func ==(TokenKind)

```cangjie
public operator func ==(right: TokenKind): Bool
```

功能：重载等号操作符，用于比较两个 [TokenKind](ast_package_enums.md#enum-tokenkind) 是否相等。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 布尔类型。

### func toString()

```cangjie
public func toString(): String
```

功能：将 [TokenKind](ast_package_enums.md#enum-tokenkind) 类型转化为字符串类型表示。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - [TokenKind](ast_package_enums.md#enum-tokenkind) 转换后的字符串值。
