# TokenKind 类型

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
    SYNCHRONIZED|             /*  "synchronized */
    UPPERBOUND|               /*  "<:"          */
    MAIN|                     /*  "main"        */
    IDENTIFIER|               /*  "x"           */
    PACKAGE_IDENTIFIER|       /*  "x-y"         */
    INTEGER_LITERAL|          /*  e.g. "1"      */
    RUNE_BYTE_LITERAL|        /*  e.g. "b'x'"   */
    FLOAT_LITERAL|            /*  e.g. "'1.0'"  */
    COMMENT|                  /*  e.g. "//xx"     */
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
    HANDLE|                   /*  "handle"           */
    PERFORM|                  /*  "perform"          */
    RESUME|                   /*  "resume"           */
    THROWING|                 /*  "throwing"         */
    ...
}
```
