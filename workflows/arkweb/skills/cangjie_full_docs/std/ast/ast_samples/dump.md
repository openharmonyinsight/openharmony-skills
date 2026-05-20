# 语法树节点打印

仓颉 ast 包提供了丰富的语法树节点用于表示仓颉源码。由于节点种类丰富、不同节点间属性不同，使用过程可能会发生混淆不清的情况，为此我们为每个 AST 节点实现了 `dump` 函数方便实时查看语法树节点的整体结构，避免重复查看该手册带来的困扰。

示例：

<!-- verify -->

```cangjie
import std.ast.*

main() {
    let input = quote(var demo: Int64 = 1) // 假设当前代码所在行数为：4
    let varDecl = parseDecl(input)
    varDecl.dump()
}
```

运行结果：

```text
VarDecl {
  -keyword: Token {
    value: "var"
    kind: VAR
    pos: 4: 23
  }
  -identifier: Token {
    value: "demo"
    kind: IDENTIFIER
    pos: 4: 27
  }
  -declType: PrimitiveType {
    -keyword: Token {
      value: "Int64"
      kind: INT64
      pos: 4: 33
    }
  }
  -assign: Token {
    value: "="
    kind: ASSIGN
    pos: 4: 39
  }
  -expr: LitConstExpr {
    -literal: Token {
      value: "1"
      kind: INTEGER_LITERAL
      pos: 4: 41
    }
  }
}
```
