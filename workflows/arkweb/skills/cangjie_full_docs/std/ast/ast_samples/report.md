# 自定义报错接口

仓颉 ast 包提供了自定义报错接口 [diagReport](../ast_package_api/ast_package_funcs.md#func-diagreportdiagreportlevel-tokens-string-string)。方便定义宏的用户，在解析传入 [Tokens](../ast_package_api/ast_package_classes.md#class-tokens) 时，对错误 [Tokens](../ast_package_api/ast_package_classes.md#class-tokens) 内容进行自定义报错。

自定义报错接口提供同原生编译器报错一样的输出格式，允许用户报 `WARNING` 和 `ERROR` 两类错误提示信息。

## 正确使用示例

宏定义如下：

```cangjie
// macro_definition.cj
macro package macro_definition

import std.ast.*

public macro testDef(input: Tokens): Tokens {
    for (i in 0..input.size) {
        if (input[i].kind == IDENTIFIER) {
            diagReport(DiagReportLevel.ERROR, input[i..(i + 1)], "This expression is not allowed to contain identifier",
                "Here is the illegal identifier")
        }
    }
    return input
}
```

宏调用如下：

```cangjie
// macro_call.cj
package macro_calling

import std.ast.*
import macro_definition.*

main(): Int64 {
    let a = @testDef(1)
    let b = @testDef(a)
    let c = @testDef(1 + a)
    return 0
}
```

编译命令如下：

```text
# 先编译宏定义文件
cjc macro_definition.cj --compile-macro

# 编译使用宏的文件
cjc macro_call.cj -o demo
```

报错提示信息如下：

```text
error: This expression is not allowed to contain identifier
 ==> call.cj:9:22:
  |
9 |     let b = @testDef(a)
  |                      ^ Here is the illegal identifier
  |

error: This expression is not allowed to contain identifier
  ==> call.cj:10:26:
   |
10 |     let c = @testDef(1 + a)
   |                          ^ Here is the illegal identifier
   |

2 errors generated, 2 errors printed.
```

## 非宏展开过程中调用示例

```cangjie
import std.ast.*

func A(input: Tokens) {
    diagReport(DiagReportLevel.ERROR, input, "Message", "Hint") // 该调用处在普通函数 A 中，diagReport 实际不会执行任何操作
}

main() {
    let tokens = quote(var a = 0)
    A(tokens)
}
```
