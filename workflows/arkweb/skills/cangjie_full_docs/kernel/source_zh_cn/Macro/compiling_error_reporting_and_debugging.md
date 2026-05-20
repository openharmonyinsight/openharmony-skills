# 编译、报错与调试

## 宏的编译和使用

当前编译器约束宏的定义与宏的调用不允许在同一包里。宏包必须首先被编译，然后再编译宏调用的包。在宏调用的包中，不允许出现宏的定义。由于宏需在包中导出给另一个包使用，因此编译器约束宏定义必须使用 `public` 修饰。

下面介绍一个简单的例子。

源码目录结构如下：

```text
// Directory layout.
root_path
├── macros
│    └── m.cj
├── src
│    └── demo.cj
└─ target
```

宏定义放在 _macros_ 子目录下：

<!-- run -macro0 -->
<!-- cfg="--compile-macro" -->

```cangjie
// macros/m.cj
// In this file, we define the macro Inner, Outer.
macro package define
import std.ast.*

public macro Inner(input: Tokens) {
    return input
}

public macro Outer(input: Tokens) {
    return input
}

```

宏调用放在 _src_ 子目录下：

<!-- run -macro0 -->

```cangjie
// src/demo.cj
import define.*
@Outer
class Demo {
    @Inner var state = 1
    @Inner var cnt = 42
}

main() {
    println("test macro")
}
```

当宏定义文件的编译产物和使用宏的文件不在同一目录下时，需要通过添加 `--import-path` 编译选项来指定宏定义文件编译产物的路径。以下为 Linux 平台的编译命令（具体编译选项会随着 cjc 更新而演进，以最新 cjc 的编译选项为准）：

```shell
# 先编译宏定义文件在指定目录产生默认的动态库文件（允许指定动态库的路径，但不能指定动态库的名字）
cjc macros/m.cj --compile-macro --output-dir ./target

# 编译使用宏的文件，宏替换完成，产生可执行文件
cjc src/demo.cj -o demo --import-path ./target --output-dir ./target

# 运行可执行文件
./target/demo
```

在 Linux 平台上，将生成用于包管理的 `macro_define.cjo` 和实际的动态库文件。

若在 Windows 平台：

```shell
# 当前目录: src

# 先编译宏定义文件在指定目录产生默认的动态库文件（允许指定动态库的路径，但不能指定动态库的名字）
cjc macros/m.cj --compile-macro --output-dir ./target

# 编译使用宏的文件，宏替换完成，产生可执行文件
cjc src/demo.cj -o demo.exe --import-path ./target --output-dir ./target
```

如果宏包还依赖其他动态库，则需要保证宏包在运行态（宏展开依赖宏包内方法的执行）下能够找到这些依赖。在 Linux 下可以通过设置 `LD_LIBRAYR_PATH`（Windows 下设置 `PATH`）环境变量添加所依赖动态库的路径。

> **说明：**
>
> 宏替换过程依赖仓颉 runtime ，宏替换过程中仓颉 runtime 的初始化配置采用宏提供的默认配置，配置参数支持使用仓颉 runtime 运维日志进行查询，其中 cjHeapSize 与 cjStackSize 支持用户修改，其余暂不支持。注意所有配置参数在 OpenHarmonyOS 平台下均无效，OpenHarmonyOS 平台下仓颉运行时使用默认值。仓颉 runtime 初始化配置可参见[runtime 初始化可选配置](../Appendix/runtime_env.md#runtime-初始化可选配置)章节。

## 并行宏展开

可以在编译宏调用文件时添加 `--parallel-macro-expansion` 选项，启用并行宏展开的能力。编译器会自动分析宏调用之间的依赖关系，无依赖关系的宏调用可以并行执行，如上述例子中的两个 `@Inner` 就可以并行展开，如此可以缩短整体编译时间。

> **注意：**
>
> 如果宏函数依赖一些全局变量，使用并行宏展开会存在风险。

<!-- compile -macro1 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define
import std.ast.*
import std.collection.HashMap

var Counts = HashMap<String, Int64>()

public macro Inner(input: Tokens) {
    for (t in input) {
        if (t.value.size == 0) {
            continue
        }
        // 统计所有有效token value的出现次数
        if (!Counts.contains(t.value)) {
            Counts[t.value] = 0
        }
        Counts[t.value] = Counts[t.value] + 1
    }
    return input
}

public macro B(input: Tokens) {
    return input
}
```

参考上述代码，如果 `@Inner` 的宏调用出现在多处，并且启用了并行宏展开选项，则访问全局变量 `Counts` 就可能存在冲突，导致最后获取的结果不正确。

建议不要在宏函数中使用全局变量，如果必须使用，要么关闭并行宏展开选项，或者可以通过仓颉线程锁对全局变量进行保护。

## diagReport 报错机制

仓颉标准库 `std.ast` 包提供了自定义报错接口 `diagReport`。方便定义宏的用户，在解析传入 Tokens 时，对错误 Tokens 内容进行自定义报错。

自定义报错接口提供同原生编译器报错一样的输出格式，允许用户报 warning 和 error 两类错误提示信息。

`diagReport` 的函数原型如下：

<!-- code_no_check -->

```cangjie
public func diagReport(level: DiagReportLevel, tokens: Tokens, message: String, hint: String): Unit
```

其参数含义如下：

- level: 报错信息等级
- tokens: 报错信息中所引用源码内容对应的 Tokens
- message: 报错的主信息
- hint: 辅助提示信息

参考如下使用示例。

宏定义文件：

<!-- compile.error -macro2 -->
<!-- cfg="--compile-macro" -->

```cangjie
// macro_definition.cj
macro package macro_definition

import std.ast.*

public macro testDef(input: Tokens): Tokens {
    for (i in 0..input.size) {
        if (input[i].kind == IDENTIFIER) {
            diagReport(DiagReportLevel.ERROR, input[i..(i + 1)],
                       "This expression is not allowed to contain identifier",
                       "Here is the illegal identifier")
        }
    }
    return input
}
```

宏调用文件：

<!-- compile.error -macro2 -->

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

编译宏调用文件过程中，会出现如下报错信息：

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

## 使用 --debug-macro 输出宏展开结果

借助宏在编译期做代码生成时，如果发生错误，处理起来十分棘手，这是开发者经常遇到但一般很难定位的问题。这是因为，开发者写的源码，经过宏的变换后变成了不同的代码片段。编译器抛出的错误信息是基于宏最终生成的代码进行提示的，但这些代码在开发者的源码中没有体现。

为了解决这个问题，仓颉宏提供 debug 模式，在这个模式下，开发者可以从编译器为宏生成的 debug 文件中看到完整的宏展开后的代码，如下所示。

宏定义文件：

<!-- compile -macro3 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

import std.ast.*

public macro Outer(input: Tokens): Tokens {
    let messages = getChildMessages("Inner")

    let getTotalFunc = quote(public func getCnt() {
                       )
    for (m in messages) {
        let identName = m.getString("identifierName")
        getTotalFunc.append(Token(TokenKind.IDENTIFIER, identName))
        getTotalFunc.append(quote(+))
    }
    getTotalFunc.append(quote(0))
    getTotalFunc.append(quote(}))
    let funcDecl = parseDecl(getTotalFunc)

    let decl = (parseDecl(input) as ClassDecl).getOrThrow()
    decl.body.decls.add(funcDecl)
    return decl.toTokens()

}

public macro Inner(input: Tokens): Tokens {
    assertParentContext("Outer")
    let decl = parseDecl(input)
    setItem("identifierName", decl.identifier.value)
    return input
}
```

宏调用文件 `demo.cj`：

<!-- compile -macro3 -->
<!-- cfg="--debug-macro" -->

```cangjie
import define.*

@Outer
class Demo {
    @Inner var state = 1
    @Inner var cnt = 42
}

main(): Int64 {
    let d = Demo()
    println("${d.getCnt()}")
    return 0
}

```

在编译使用宏的文件时，在选项中，增加 `--debug-macro`，即使用仓颉宏的 _debug_ 模式。

```shell
cjc --debug-macro demo.cj --import-path ./target
```

> **注意：**
>
> 如果使用仓颉的 `CJPM` 项目管理工具进行编译，可在配置文件 `cjpm.toml` 中添加 `--debug-macro` 的编译选项来使用宏的 _debug_ 模式。
>
> ```text
> compile-option = "--debug-macro"
> ```

在 _debug_ 模式下，会生成临时文件 _demo.cj.macrocall_，对应宏展开的部分如下：

<!-- code_no_check -->

```cangjie
// demo.cj.macrocall
/* ===== Emitted by MacroCall @Outer in demo.cj:3:1 ===== */
/* 3.1 */class Demo {
/* 3.2 */    var state = 1
/* 3.3 */    var cnt = 42
/* 3.4 */    public func getCnt() {
/* 3.5 */        state + cnt + 0
/* 3.6 */    }
/* 3.7 */}
/* 3.8 */
/* ===== End of the Emit ===== */
```

如果宏展开后的代码有语义错误，则编译器的错误信息会溯源到宏展开后代码的具体行列号。仓颉宏的 _debug_ 模式有以下注意事项：

- 宏的 _debug_ 模式会重排源码的行列号信息，不适用于某些特殊的换行场景。例如：

  <!-- code_no_check -->

  ```cangjie
  // before expansion
  @M{} - 2 // macro M return 2

  // after expansion
  // ===== Emmitted my Macro M at line 1 ===
  2
  // ===== End of the Emit =====
  - 2
  ```

  这些因换行符导致语义改变的情形，不应使用 _debug_ 模式。

- 不支持宏调用在宏定义内的调试，会编译报错。

  <!-- code_no_check -->

  ```cangjie
  public macro M(input: Tokens) {
      let a = @M2(1+2) // M2 is in macro M, not suitable for debug mode.
      return input + quote($a)
  }
  ```

- 不支持带括号宏的调试。

  <!-- code_no_check -->

  ```cangjie
  // main.cj

  main() {
      // For macro with parenthesis, newline introduced by debug will change the semantics
      // of the expression, so it is not suitable for debug mode.
      let t = @M(1+2)
  }
  ```
