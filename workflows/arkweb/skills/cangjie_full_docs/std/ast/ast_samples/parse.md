# 将仓颉源码解析为 AST 对象示例

## 使用 parseDecl 函数将仓颉源码解析为 Decl 对象示例

如下有一个类 Data：

```text
class Data {
    var a: Int32
    init(a_: Int32) {
        a = a_
    }
}
```

利用解析函数将上述代码解析为一个 Decl 对象，代码如下所示：

<!-- verify -->

```cangjie
import std.ast.*

main() {
    let input: Tokens = quote(
        class Data {
            var a: Int32
            init(a_: Int32) {
                a = a_
            }
        }
    )
    let decl = parseDecl(input) // 获取一个 Decl 声明节点
    var classDecl = match (decl as ClassDecl) { // decl 的具体类型为 ClassDecl, 将其进行类型转化。
        case Some(v) => v
        case None => throw Exception()
    }
    classDecl.dump()
}
```

运行结果：

```text
ClassDecl {
  -keyword: Token {
    value: "class"
    kind: CLASS
    pos: 5: 9
  }
  -identifier: Token {
    value: "Data"
    kind: IDENTIFIER
    pos: 5: 15
  }
  -body: Body {
    -decls: 0, VarDecl {
      -keyword: Token {
        value: "var"
        kind: VAR
        pos: 6: 13
      }
      -identifier: Token {
        value: "a"
        kind: IDENTIFIER
        pos: 6: 17
      }
      -declType: PrimitiveType {
        -keyword: Token {
          value: "Int32"
          kind: INT32
          pos: 6: 20
        }
      }
    }
    -decls: 1, FuncDecl {
      -keyword: Token {
        value: "init"
        kind: INIT
        pos: 7: 13
      }
      -identifier: Token {
        value: "init"
        kind: IDENTIFIER
        pos: 7: 13
      }
      -funcParams: 0, FuncParam {
        -identifier: Token {
          value: "a_"
          kind: IDENTIFIER
          pos: 7: 18
        }
        -colon: Token {
          value: ":"
          kind: COLON
          pos: 7: 20
        }
        -paramType: PrimitiveType {
          -keyword: Token {
            value: "Int32"
            kind: INT32
            pos: 7: 22
          }
        }
      }
      -block: Block {
        -nodes: 0, AssignExpr {
          -leftExpr: RefExpr {
            -identifier: Token {
              value: "a"
              kind: IDENTIFIER
              pos: 8: 17
            }
          }
          -assign: Token {
            value: "="
            kind: ASSIGN
            pos: 8: 19
          }
          -rightExpr: RefExpr {
            -identifier: Token {
              value: "a_"
              kind: IDENTIFIER
              pos: 8: 21
            }
          }
        }
      }
    }
  }
}
```

## 使用 parseProgram 函数将仓颉源码解析为 Program 对象示例

待解析仓颉源码文件 test_macro_define.cj 的内容如下：

```text
/**
* 此 cj 文件作为输入参数，用于测试 parseProgram()；
**/
macro package m

internal import std.ast.*
internal import base as mybase

public macro M(input: Tokens) {
    return input
}
```

利用 parseProgram 函数将上述代码解析为一个 Program 节点对象，代码如下所示：

<!-- compile -->

```cangjie
internal import std.ast.*
internal import std.fs.*
internal import std.io.*

main() {
    let path: String = "./test_macro_define.cj"
    let file: File = File(path, Read)
    let reader: StringReader<File> = StringReader(file)
    let code: String = reader.readToEnd() // 读取源码文件内容为字符串

    let tokens: Tokens = cangjieLex(code)
    let fileNode = parseProgram(tokens) // 解析为 Program 节点
    fileNode.dump()

    return 0
}
```

运行结果：

```text
Program {
  -packageHeader: PackageHeader {
      -keywordM: Token {
        value: "macro"
        kind: MACRO
      }
      -keywordP: Token {
        value: "package"
        kind: PACKAGE
      }
      -packageIdentifier: Token {
        value: "m"
        kind: IDENTIFIER
      }
    }
  -importLists: 0, ImportList {
    -modifier: Token {
      value: "internal"
      kind: INTERNAL
    }
    -keywordI: Token {
      value: "import"
      kind: IMPORT
    }
    -importKind: All
    prefixPath: 0: Token {
      value: "std"
      kind: IDENTIFIER
    }
    prefixPath: 1: Token {
      value: "ast"
      kind: IDENTIFIER
    }
    -identifier: Token {
      value: "*"
      kind: MUL
    }
  }
  -importLists: 1, ImportList {
    -modifier: Token {
      value: "internal"
      kind: INTERNAL
    }
    -keywordI: Token {
      value: "import"
      kind: IMPORT
    }
    -importKind: Alias
    -identifier: Token {
      value: "base"
      kind: IDENTIFIER
    }
    -importAlias 0: Token {
      value: "as"
      kind: AS
    }
    -importAlias 1: Token {
      value: "mybase"
      kind: IDENTIFIER
    }
  }
  -decls: 0, MacroDecl {
    -modifiers: 0, Modifier {
      -keyword: Token {
        value: "public"
        kind: PUBLIC
      }
    }
    -keyword: Token {
      value: "macro"
      kind: MACRO
    }
    -identifier: Token {
      value: "M"
      kind: IDENTIFIER
    }
    -funcParams: 0, FuncParam {
      -identifier: Token {
        value: "input"
        kind: IDENTIFIER
      }
      -colon: Token {
        value: ":"
        kind: COLON
      }
      -paramType: RefType {
        -identifier: Token {
          value: "Tokens"
          kind: IDENTIFIER
        }
      }
    }
    -block: Block {
      -nodes: 0, ReturnExpr {
        -keyword: Token {
          value: "return"
          kind: RETURN
        }
        -expr: RefExpr {
          -identifier: Token {
            value: "input"
            kind: IDENTIFIER
          }
        }
      }
    }
  }
}
```