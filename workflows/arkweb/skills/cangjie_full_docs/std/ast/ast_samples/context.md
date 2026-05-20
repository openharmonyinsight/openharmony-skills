# Macro With Context

宏定义如下：

```cangjie
// macro_definition.cj
macro package macro_definition

import std.ast.*

public macro Outter(input: Tokens): Tokens {
    return input
}

public macro Inner(input: Tokens): Tokens {
    assertParentContext("Outter")
    return input
}
```

宏调用如下：

```cangjie
// macro_call.cj
package macro_calling

import macro_definition.*

main() {
    @Outter var a = 0
    @Inner var b = 0 // error: The macro call 'Inner' should with the surround code contains a call 'Outter'.
}
```

编译命令如下：

```text
# 先编译宏定义文件
cjc macro_definition.cj --compile-macro

# 编译使用宏的文件
cjc macro_call.cj -o demo
```

如上代码所示，`Inner` 宏在定义时使用了 `assertParentContext` 函数用于检查其在调用阶段是否位于 `Outter` 宏中，在代码示例的宏调用场景下，由于 `Outter` 和 `Inner` 在调用时不存在这样的嵌套关系，因此编译器将报告一个错误。

宏定义如下：

```cangjie
// macro_definition.cj
macro package macro_definition

import std.ast.*

public macro Outter(input: Tokens): Tokens {
    let messages = getChildMessages("Inner")
    for (m in messages) {
        let value1 = m.getString("key1") // get value: "value1"
        let value2 = m.getString("key2") // get value: "value2"
        println("value1: ${value1}  value2: ${value2}")
    }
    return input
}

public macro Inner(input: Tokens): Tokens {
    assertParentContext("Outter")
    setItem("key1", "value1")
    setItem("key2", "value2")
    return input
}
```

宏调用如下：

```cangjie
// macro_call.cj
import std.ast.*
import macro_definition.*

main() {
    @Outter(
        @Inner var cnt = 0
    )
    println(cnt)
}
```

编译命令如下：

```text
# 先编译宏定义文件
cjc macro_definition.cj --compile-macro

# 编译使用宏的文件
cjc macro_call.cj -o demo
```

编译阶段输出：

```text
value1: value1  value2: value2
```

在上面的代码中，内层宏 `Inner` 通过 `setItem` 向外层宏发送信息；`Outter` 宏通过 `getChildMessages` 函数接收到 `Inner` 发送的一组信息对象（`Outter` 中可以调用多次 `Inner`）；最后通过该信息对象的 `getString` 函数接收对应的值。
