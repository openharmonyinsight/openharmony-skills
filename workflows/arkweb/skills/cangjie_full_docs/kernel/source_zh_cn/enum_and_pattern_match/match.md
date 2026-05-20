# match 表达式

## match 表达式的定义

仓颉支持两种 `match` 表达式，第一种是包含待匹配值的 `match` 表达式，第二种是不含待匹配值的 `match` 表达式。

**含匹配值的 match 表达式**：

<!-- verify -->

```cangjie
main() {
    let x = 0
    match (x) {
        case 1 => let r1 = "x = 1"
                  print(r1)
        case 0 => let r2 = "x = 0" // Matched.
                  print(r2)
        case _ => let r3 = "x != 1 and x != 0"
                  print(r3)
    }
}
```

`match` 表达式以关键字 `match` 开头，后跟要匹配的值，如上例中的 `x`，`x` 可以是任意表达式。接着是定义在一对花括号内的若干 `case` 分支，每个 `case` 分支以关键字 `case` 开头，`case` 之后是一个模式或多个由 `|` 连接的相同种类的模式，上例中的 `1`、`0`、`_` 均为模式，详见[模式概述](../enum_and_pattern_match/pattern_overview.md)章节。后面紧跟 `=>`，`=>` 之后即本条 `case` 分支匹配成功后需要执行的操作，可以是一系列表达式、变量和函数定义。其中，新定义的变量或函数的作用域从其定义处开始到下一个 `case` 之前结束，如上例中的变量定义和 `print` 函数调用。

上例中，因为 `x` 的值等于 `0`，所以会和第二条 `case` 分支匹配（此处使用的是常量模式，匹配的是值是否相等，详见[常量模式](../enum_and_pattern_match/pattern_overview.md#常量模式)章节），最后输出 `x = 0`。

编译并执行上述代码，输出结果为：

```text
x = 0
```

`match` 表达式要求所有匹配必须是穷尽（exhaustive）的，意味着待匹配表达式的所有可能取值都应该被考虑到。当 `match` 表达式非穷尽，或者编译器判断不出是否穷尽时，均会编译报错，换言之，所有 `case` 分支（包含 pattern guard）所覆盖的取值范围的并集，应该包含待匹配表达式的所有可能取值。常用的确保 `match` 表达式穷尽的方式是在最后一个 `case` 分支中使用通配符模式 `_`，因为 `_` 可以匹配任何值。

`match` 表达式的穷尽性保证了一定存在和待匹配值相匹配的 `case` 分支。下面的例子将编译报错，因为所有的 `case` 并没有覆盖 `x` 的所有可能取值：

<!-- compile.error -->

```cangjie
func nonExhaustive(x: Int64) {
    match (x) {
        case 0 => print("x = 0")
        case 1 => print("x = 1")
        case 2 => print("x = 2")
    }
}
```

如果被匹配值的类型包含 `enum` 类型且该 `enum` 为 `non-exhaustive enum`，则其在匹配时需要使用可匹配所有构造器的模式，如通配符模式 `_` 和绑定模式。

<!-- compile -->

```cangjie
enum T {
    | Red | Green | Blue | ...
}
func foo(a: T) {
    match (a) {
        case Red => 0
        case Green => 1
        case Blue => 2
        case _ => -1
    }
}

func bar(a: T) {
    match (a) {
        case Red => 0
        case k => -1 // simple binding pattern
    }
}

func baz(a: T) {
    match (a) {
        case Red => 0
        case k: T => -1 // binding pattern with nested type pattern
    }
}
```

在 `case` 分支的模式之后，可以使用 `pattern guard`（模式守卫）进一步对匹配出来的结果进行判断，此为可选内容。

`pattern guard` 表示本条 `case` 匹配成功后额外需要满足的条件，其使用 `where cond`（语法格式） 表示，要求表达式 `cond` 的类型为 `Bool`。

`match` 表达式执行时，会依次将 `match` 之后的表达式与每个 `case` 中的模式进行匹配。如果有 `pattern guard`，需要 `where` 之后的表达式的值为 `true`；如果 `case` 中有多个由 `|` 连接的模式，只要待匹配值和其中一个模式匹配则认为匹配成功。一旦匹配成功，将执行 `=>` 之后的代码，然后退出 `match` 表达式的执行，这意味着不会再去匹配它之后的 `case`。如果匹配不成功，会继续与它之后的 `case` 中的模式进行匹配，直到匹配成功。`match` 表达式可以保证一定存在匹配的 `case` 分支。

在下面的例子中，使用到了 `enum` 模式，详见 [enum 模式](../enum_and_pattern_match/pattern_overview.md#enum-模式)章节。当 `RGBColor` 的构造器的参数值大于等于 `0` 时，输出它们的值；当参数值小于 `0` 时，即满足第一个 `case` 的 `where cond`，则认为它们的值等于 `0`：

<!-- verify -->

```cangjie
enum RGBColor {
    | Red(Int16) | Green(Int16) | Blue(Int16)
}
main() {
    let c = RGBColor.Green(-100)
    let cs = match (c) {
        case Red(r) where r < 0 => "Red = 0"
        case Red(r) => "Red = ${r}"
        case Green(g) where g < 0 => "Green = 0" // Matched.
        case Green(g) => "Green = ${g}"
        case Blue(b) where b < 0 => "Blue = 0"
        case Blue(b) => "Blue = ${b}"
    }
    print(cs)
}
```

编译执行上述代码，输出结果为：

```text
Green = 0
```

**没有匹配值的 match 表达式**：

<!-- verify -->

```cangjie
main() {
    let x = -1
    match {
        case x > 0 => print("x > 0")
        case x < 0 => print("x < 0") // Matched.
        case _ => print("x = 0")
    }
}
```

与包含待匹配值的 `match` 表达式相比，关键字 `match` 之后并没有待匹配的表达式，并且 `case` 之后不再是 `pattern`，而是类型为 `Bool` 的表达式（上述代码中的 `x > 0` 和 `x < 0`）或者 `_`（表示 `true`），当然，`case` 中也不再有 `pattern guard`。

无匹配值的 `match` 表达式执行时依次判断 `case` 之后的表达式的值，直到遇到值为 `true` 的 `case` 分支；一旦某个 `case` 之后的表达式值等于 `true`，则执行此 `case` 中 `=>` 之后的代码，然后退出 `match` 表达式的执行（意味着不会再去判断该 `case` 之后的其他 `case`）。

上例中，因为 `x` 的值等于 `-1`，所以第二条 `case` 分支中的表达式（即 `x < 0`）的值等于 `true`，执行 `print("x < 0")`。

编译并执行上述代码，输出结果为：

```text
x < 0
```

## match 表达式的类型

对于 `match` 表达式（无论是否有匹配值）：

- 在上下文有明确的类型要求时，要求每个 `case` 分支中 `=>` 之后的代码块的类型是上下文所要求的类型的子类型。

- 在上下文没有明确的类型要求时，`match` 表达式的类型是每个 `case` 分支中 `=>` 之后的代码块的类型的最小公共父类型。

- 当 `match` 表达式的值没有被使用时，其类型为 `Unit`，不要求各分支的类型有最小公共父类型。

下面分别举例说明。

<!-- compile -->

```cangjie
let x = 2
let s: String = match (x) {
    case 0 => "x = 0"
    case 1 => "x = 1"
    case _ => "x != 0 and x != 1" // Matched.
}
```

上面的例子中，定义变量 `s` 时，显式地标注了其类型为 `String`，属于上下文类型信息明确的情况，因此要求每个 `case` 的 `=>` 之后的代码块的类型均是 `String` 的子类型，显然上例中 `=>` 之后的字符串类型的字面量均满足要求。

再来看一个没有上下文类型信息的例子：

<!-- compile -->

```cangjie
let x = 2
let s = match (x) {
    case 0 => "x = 0"
    case 1 => "x = 1"
    case _ => "x != 0 and x != 1" // Matched.
}
```

上例中，定义变量 `s` 时，未显式标注其类型，因为每个 `case` 的 `=>` 之后的代码块的类型均是 `String`，所以 `match` 表达式的类型是 `String`，进而可确定 `s` 的类型也是 `String`。
