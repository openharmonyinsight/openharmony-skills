# 宏的实现

本章节介绍仓颉宏的定义和使用，仓颉宏可以分为[非属性宏](./implementation_of_macros.md#非属性宏)和[属性宏](./implementation_of_macros.md#属性宏)。同时本章节还会介绍宏出现嵌套时的行为。

## 非属性宏

非属性宏只接受被转换的代码，不接受其他参数（属性），其定义格式如下：

<!-- code_no_check -->

```cangjie
import std.ast.*

public macro MacroName(args: Tokens): Tokens {
    ... // Macro body
}
```

宏的调用格式如下：

<!-- code_no_check -->

```cangjie
@MacroName(...)
```

宏调用使用 `()` 括起来。括号里面可以是任意合法 `Tokens`，也可以是空。

当宏作用于声明时，一般可以省略括号。参考如下示例：

<!-- code_no_check -->

```cangjie
@MacroName func name() {}        // Before a FuncDecl
@MacroName struct name {}        // Before a StructDecl
@MacroName class name {}         // Before a ClassDecl
@MacroName var a = 1             // Before a VarDecl
@MacroName enum e {}             // Before a Enum
@MacroName interface i {}        // Before a InterfaceDecl
@MacroName extend e <: i {}      // Before a ExtendDecl
class C {
    @MacroName prop i: Int64 {   // Before a PropDecl
        get() { 0 }
    }
} 
@MacroName @AnotherMacro(input)  // Before a macro call
```

对于括号里 `Tokens` 的合法性有以下特殊说明：

- 输入的内容必须是由合法的 `Token` 组成的序列，类似 "#"、" \` "、"\\" 等符号单独使用都不是合法的仓颉 `Token`，不支持其作为输入值。

- 输入的内容中，若存在不匹配的小括号则必须使用转义符号 "\\" 对其进行转义。

- 输入的内容中，若希望 "@" 作为输入的 `Token` 则必须使用转义符号 "\\" 对其进行转义。

对于输入的特殊说明，可以参考如下示例：

<!-- code_no_check -->

```cangjie
// Illegal input Tokens
@MacroName(#)    // Not a whole Token
@MacroName(`)    // Not a whole Token
@MacroName(()    // ( and ) not match
@MacroName(\[)   // Escape for unsupported symbol

// Legal input Tokens
@MacroName(#"abc"#)
@MacroName(`class`)
@MacroName([)
@MacroName([])
@MacroName(\()
@MacroName(\@)
```

宏展开过程作用于仓颉语法树，宏展开后，编译器会继续进行后续的编译过程。因此，需要注意以下规则：

- 宏展开后的代码依然是合法的仓颉代码，并且宏展开后的代码不允许出现包的声明与导入语句，否则可能引发编译问题。
- 当宏用于声明时，如果省略括号，宏的输入必须是语法合法的声明。

下面是几个宏应用的典型示例。

- 示例 1

  宏定义文件 `macro_definition.cj`

  <!-- verify -macro6 -->
  <!-- cfg="--compile-macro" -->

  ```cangjie
  macro package macro_definition

  import std.ast.*

  public macro testDef(input: Tokens): Tokens {
      println("I'm in macro body")
      return input
  }
  ```

  宏调用文件 `macro_call.cj`

  <!-- verify -macro6 -->

  ```cangjie
  package macro_calling

  import macro_definition.*

  main(): Int64 {
      println("I'm in function body")
      let a: Int64 = @testDef(1 + 2)
      println("a = ${a}")
      return 0
  }
  ```

  上述代码的编译过程可以参考[宏的编译和使用](./compiling_error_reporting_and_debugging.md#宏的编译和使用)。

  在用例中添加了打印信息，其中宏定义中的 `I'm in macro body` 将在编译 `macro_call.cj` 的期间输出。同时，宏调用点被展开，如编译如下代码：

  <!-- code_no_check -->

  ```cangjie
  let a: Int64 = @testDef(1 + 2)
  ```

  编译器将宏返回的 `Tokens` 更新到调用点的语法树上，得到如下代码：

  <!-- code_no_check -->

  ```cangjie
  let a: Int64 = 1 + 2
  ```

  也就是说，可执行程序中的代码实际变为了：

  <!-- code_no_check -->

  ```cangjie
  main(): Int64 {
      println("I'm in function body")
      let a: Int64 = 1 + 2
      println("a = ${a}")
      return 0
  }
  ```

  `a` 经过计算得到的值为 3，在打印 `a` 的值时插值为 3。至此，上述程序的运行结果为：

  <!-- verify -macro6 -->

  ```text
  I'm in function body
  a = 3
  ```

下面看一个更有意义的用宏处理函数的例子，这个宏 ModifyFunc 宏的作用是给 myFunc 增加 id 参数，并在 `counter++` 前后插入一段代码。

- 示例 2

  宏定义文件 `macro_definition.cj`

  <!-- verify -macro7 -->
  <!-- cfg="--compile-macro" -->

  ```cangjie
  // file macro_definition.cj
  macro package macro_definition

  import std.ast.*

  public macro ModifyFunc(input: Tokens): Tokens {
      println("I'm in macro body")
      let funcDecl = FuncDecl(input)
      return quote(
          func $(funcDecl.identifier)(id: Int64) {
              println("start ${id}")
              $(funcDecl.block.nodes)
              println("end")
          })
  }
  ```

  宏调用文件 `macro_call.cj`

  <!-- verify -macro7 -->

  ```cangjie
  package macro_calling

  import macro_definition.*

  var counter = 0

  @ModifyFunc
  func myFunc() {
      counter++
  }

  func exModifyFunc() {
      println("I'm in function body")
      myFunc(123)
      println("myFunc called: ${counter} times")
      return 0
  }

  main(): Int64 {
      exModifyFunc()
  }
  ```

  同样的，上述两段代码分别位于不同文件中，先编译宏定义文件 `macro_definition.cj`，再编译宏调用 `macro_call.cj` 生成可执行文件。

  这个例子中，ModifyFunc 宏的输入是一个函数声明，因此可以省略括号：

  <!-- code_no_check -->

  ```cangjie
  @ModifyFunc
  func myFunc() {
      counter++
  }
  ```

  经过宏展开后，得到如下代码：

  <!-- code_no_check -->

  ```cangjie
  func myFunc(id: Int64) {
      println("start ${id}")
      counter++
      println("end")
  }
  ```

  myFunc 会在 main 中调用，它接受的实参也是在 main 中定义的，从而形成了一段合法的仓颉程序。运行时打印如下：

  <!-- verify -macro7 -->

  ```text
  I'm in function body
  start 123
  end
  myFunc called: 1 times
  ```

## 属性宏

和非属性宏相比，属性宏的定义会增加一个 Tokens 类型的输入，这个增加的入参可以让开发者输入额外的信息。比如开发者可能希望在不同的调用场景下使用不同的宏展开策略，则可以通过这个属性入参进行标记位设置。同时，这个属性入参也可以传入任意 Tokens，这些 Tokens 可以与被宏修饰的代码进行组合拼接等。下面是一个简单的例子：

<!-- run -macro72 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package define

// Macro definition with attribute
public macro Foo(attrTokens: Tokens, inputTokens: Tokens): Tokens {
    return attrTokens + inputTokens  // Concatenate attrTokens and inputTokens.
}
```

如上面的宏定义，属性宏的入参数量为 2，入参类型为 `Tokens`，在宏定义内，可以对 `attrTokens` 和 `inputTokens` 进行一系列的组合、拼接等变换操作，最后返回新的 `Tokens`。

带属性的宏与不带属性的宏的调用类似，属性宏调用时新增的入参 attrTokens 通过 [] 传入，其调用形式为：

<!-- run -macro72 -->

```cangjie
import define.Foo

// attribute macro with parentheses
var a: Int64 = @Foo[1+](2+3)

// attribute macro without parentheses
@Foo[public]
struct Data {
    var count: Int64 = 100
}

main() {}
```

- 宏 Foo 调用，当参数是 `2+3` 时，与 `[]` 内的属性 `1+` 进行拼接，经过宏展开后，得到 `var a: Int64 = 1+2+3` 。
- 宏 Foo 调用，当参数是 struct Data 时，与 `[]` 内的属性 `public` 进行拼接，经过宏展开后，得到

  <!-- code_no_check -->

  ```cangjie
  public struct Data {
      var count: Int64 = 100
  }
  ```

关于属性宏，需要注意以下几点：

- 带属性的宏，与不带属性的宏相比，能修饰的 AST 是相同的，可以理解为带属性的宏对可传入参数做了增强。

- 属性宏小括号内的参数合法性规则与非属性宏的参数合法性规则一致。

- 属性宏中括号内的参数（属性）的合法性规则有如下特殊说明：

    - 输入的内容必须是由合法的 `Token` 组成的序列，类似 "#"、" \` "、"\\" 等符号单独使用都不是合法的仓颉 `Token`，不支持其作为输入值。

    - 输入的内容中，若存在不匹配的中括号则必须使用转义符号 "\\" 对其进行转义。

    - 输入的内容中，若希望 "@" 作为输入的 `Token` 则必须使用转义符号 "\\" 对其进行转义。

    <!-- code_no_check -->

    ```cangjie
    // Illegal attribute Tokens
    @MacroName[#]()    // Not a whole Token
    @MacroName[`]()    // Not a whole Token
    @MacroName[@]()    // Not escape for @
    @MacroName[[]()    // [ and ] not match
    @MacroName[\(]()   // Escape for unsupported symbol

    // Legal attribute Tokens
    @MacroName[#"abc"#]()
    @MacroName[`class`]()
    @MacroName[(]()
    @MacroName[()]()
    @MacroName[\[]()
    @MacroName[\@]()
    ```

- 宏的定义和调用的类型要保持一致：如果宏定义有两个入参，即为属性宏定义，调用时必须加上 `[]`，且内容可以为空；如果宏定义有一个入参，即为非属性宏定义，调用时不能使用 `[]`。

## 嵌套宏

仓颉语言不支持宏定义的嵌套；有条件地支持在宏定义和宏调用中嵌套宏调用。

### 宏定义中嵌套宏调用

下面是一个宏定义中包含其他宏调用的例子。

宏包 `pkg1` 中定义 `getIdent` 宏：

<!-- compile -macro8 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package pkg1

import std.ast.*

public macro getIdent(attr:Tokens, input:Tokens):Tokens {
    return quote(
        let decl = (parseDecl(input) as VarDecl).getOrThrow()
        let name = decl.identifier.value
        let size = name.size - 1
        let $(attr) = Token(TokenKind.IDENTIFIER, name[0..size])
    )
}
```

宏包 `pkg2` 中定义 `Prop` 宏，其中嵌套了 `getIdent` 宏的调用：

<!-- compile -macro8 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package pkg2

import std.ast.*
import pkg1.*

public macro Prop(input:Tokens):Tokens {
    let v = parseDecl(input)
    @getIdent[ident](input)
    return quote(
        $(input)
        public prop $(ident): $(decl.declType) {
            get() {
                this.$(v.identifier)
            }
        }
    )
}
```

宏调用包 `pkg3`  中调用 `Prop` 宏：

<!-- compile -macro8 -->

```cangjie
package pkg3

import pkg2.*
class A {
    @Prop
    private let a_: Int64 = 1
}

main() {
    let b = A()
    println("${b.a}")
}
```

注意，按照宏定义必须比宏调用点先编译的约束，上述 3 个文件的编译顺序必须是：pkg1 -> pkg2 -> pkg3。pkg2 中的 `Prop` 宏定义：

<!-- code_no_check -->

```cangjie
public macro Prop(input:Tokens):Tokens {
    let v = parseDecl(input)
    @getIdent[ident](input)
    return quote(
        $(input)
        public prop $(ident): $(decl.declType) {
            get() {
                this.$(v.identifier)
            }
        }
    )
}
```

会先被展开成如下代码，再进行编译。

<!-- code_no_check -->

```cangjie
public macro Prop(input: Tokens): Tokens {
    let v = parseDecl(input)

    let decl = (parseDecl(input) as VarDecl).getOrThrow()
    let name = decl.identifier.value
    let size = name.size - 1
    let ident = Token(TokenKind.IDENTIFIER, name[0 .. size])

    return quote(
        $(input)
        public prop $(ident): $(decl.declType) {
            get() {
                this.$(v.identifier)
            }
        }
    )
}
```

### 宏调用中嵌套宏调用

嵌套宏的常见场景，是宏修饰的代码块中，出现了宏调用。一个具体的例子如下：

`pkg1` 包中定义 `Foo` 和 `Bar` 宏：

<!-- run -macro9 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package pkg1

import std.ast.*

public macro Foo(input: Tokens): Tokens {
    return input
}

public macro Bar(input: Tokens): Tokens {
    return input
}
```

`pkg2` 包中定义 `addToMul` 宏：

<!-- run -macro9 -->
<!-- cfg="--compile-macro" -->

```cangjie
macro package pkg2

import std.ast.*

public macro addToMul(inputTokens: Tokens): Tokens {
    var expr: BinaryExpr = match (parseExpr(inputTokens) as BinaryExpr) {
        case Some(v) => v
        case None => throw Exception()
    }
    var op0: Expr = expr.leftExpr
    var op1: Expr = expr.rightExpr
    return quote(($(op0)) * ($(op1)))
}
```

`pkg3` 包中使用上面定义的三个宏：

<!-- run -macro9 -->

```cangjie
package pkg3

import pkg1.*
import pkg2.*
@Foo
struct Data {
    let a = 2
    let b = @addToMul(2+3)

    @Bar
    public func getA() {
        return a
    }

    public func getB() {
        return b
    }
}

main(): Int64 {
    let data = Data()
    var a = data.getA() // a = 2
    var b = data.getB() // b = 6
    println("a: ${a}, b: ${b}")
    return 0
}
```

如上代码所示，宏 `Foo` 修饰了 `struct Data`，而在 `struct Data` 内，出现了宏调用 `addToMul` 和 `Bar`。这种嵌套场景下，代码变换的规则是：将嵌套内层的宏（`addToMul` 和 `Bar`）展开后，再去展开外层的宏（`Foo`）。允许出现多层宏嵌套，代码变换的规则总是由内向外去依次展开宏。

嵌套宏可以出现在带括号和不带括号的宏调用中，二者可以组合，但开发者需要保证没有歧义，且明确宏的展开顺序：

<!-- code_no_check -->

```cangjie
var a = @foo(@foo1(2 * 3)+@foo2(1 + 3))  // foo1, foo2 have to be defined.

@Foo1 // Foo2 expands first, then Foo1 expands.
@Foo2[attr: struct] // Attribute macro can be used in nested macro.
struct Data{
    @Foo3 @Foo4[123] var a = @bar1(@bar2(2 + 3) + 3)  // bar2, bar1, Foo4, Foo3 expands in order.
    public func getA() {
        return @foo(a + 2)
    }
}
```

### 嵌套宏之间的消息传递

这里指的是宏调用的嵌套。

内层宏可以调用库函数 `assertParentContext` 来保证内层宏调用一定嵌套在特定的外层宏调用中。如果内层宏调用这个函数时没有嵌套在给定的外层宏调用中，该函数将抛出一个错误。库函数 `InsideParentContext` 同样用于检查内层宏调用是否嵌套在特定的外层宏调用中，该函数返回一个布尔值。下面是一个简单的例子。

宏定义如下：

<!-- compile.error -macro92 -->
<!-- cfg="--compile-macro" -->

```cangjie
public macro Outer(input: Tokens): Tokens {
    return input
}

public macro Inner(input: Tokens): Tokens {
    assertParentContext("Outer")
    return input
}
```

宏调用如下：

<!-- compile.error -macro92 -->
<!-- cfg="--debug-macro" -->

```cangjie
@Outer var a = 0
@Inner var b = 0 // Error, The macro call 'Inner' should with the surround code contains a call 'Outer'.
```

如上代码所示，`Inner` 宏在定义时使用了 `assertParentContext` 函数用于检查其在调用阶段是否位于 `Outer` 宏中，在代码示例的宏调用场景下，由于 `Outer` 和 `Inner` 在调用时不存在这样的嵌套关系，因此编译器将报告一个错误。

内层宏也可以通过发送键/值对的方式与外层宏通信。当内层宏执行时，通过调用标准库函数 `setItem` 向外层宏发送信息；随后，当外层宏执行时，调用标准库函数 `getChildMessages` 接收每一个内层宏发送的信息（一组键/值对映射）。下面是一个简单的例子。

宏定义如下：

<!-- run -macro10 -->
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
        // let value = m.getString("key")            // 接收多组消息
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
    // setItem("key", "value")                      // 可以通过不同的key值传递多组消息
    return input
}
```

宏调用如下：

<!-- run -macro11 -->
<!-- cfg="--compile-macro" -->

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

在上面的代码中，`Outer` 接收两个 `Inner` 宏发送来的变量名，自动为类添加如下内容：

<!-- code_no_check -->

```cangjie
public func getCnt() {
    state + cnt + 0
}
```

具体流程为：内层宏 `Inner` 通过 `setItem` 向外层宏发送信息；`Outer` 宏通过 `getChildMessages` 函数接收到 `Inner` 发送的一组信息对象（`Outer` 中可以调用多次 `Inner`）；最后通过该信息对象的 `getString` 函数接收对应的值。
