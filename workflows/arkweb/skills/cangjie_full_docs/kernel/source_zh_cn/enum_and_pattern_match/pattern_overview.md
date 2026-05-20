# 模式概述

对于包含匹配值的 `match` 表达式，`case` 之后支持哪些模式决定了 `match` 表达式的表达能力。本节中将依次介绍仓颉支持的模式，包括：常量模式、通配符模式、绑定模式、tuple 模式、类型模式和 enum 模式。

## 常量模式

常量模式可以是整数字面量、浮点数字面量、字符字面量、布尔字面量、字符串字面量（不支持字符串插值）、Unit 字面量。

在包含匹配值的 `match` 表达式（参见[match 表达式](./match.md)）中使用常量模式时，要求常量模式表示的值的类型与待匹配值的类型相同，匹配成功的条件是待匹配的值与常量模式表示的值相等。

下面的例子中，根据 `score` 的值（假设 `score` 只能取 `0` 到 `100` 间被 `10` 整除的值），输出考试成绩的等级：

<!-- verify -->

```cangjie
main() {
    let score = 90
    let level = match (score) {
        case 0 | 10 | 20 | 30 | 40 | 50 => "D"
        case 60 => "C"
        case 70 | 80 => "B"
        case 90 | 100 => "A" // Matched.
        case _ => "Not a valid score"
    }
    println(level)
}
```

编译执行上述代码，输出结果为：

```text
A
```

- 在模式匹配的目标是静态类型为 `Rune` 的值时，`Rune` 字面量和单字符字符串字面量都可用于表示 `Rune` 类型字面量的常量 pattern。

  <!-- verify -->

  ```cangjie
  func translate(n: Rune) {
      match (n) {
          case "A" => 1
          case "B" => 2
          case "C" => 3
          case _ => -1
      }
  }

  main() {
      println(translate(r"C"))
  }
  ```

  编译执行上述代码，输出结果为：

  ```text
  3
  ```

- 在模式匹配的目标是静态类型为 `Byte` 的值时，一个表示 ASCII 字符的字符串字面量可用于表示 `Byte` 类型字面量的常量 pattern。

  <!-- verify -->

  ```cangjie
  func translate(n: Byte) {
      match (n) {
          case "1" => 1
          case "2" => 2
          case "3" => 3
          case _ => -1
      }
  }

  main() {
      println(translate(51)) // UInt32(r'3') == 51
  }
  ```

  编译执行上述代码，输出结果为：

  ```text
  3
  ```

## 通配符模式

通配符模式使用下划线 `_` 表示，可以匹配任意值。通配符模式通常作为最后一个 `case` 中的模式，用来匹配其他 `case` 未覆盖到的情况，如[常量模式](./pattern_overview.md#常量模式)中匹配 `score` 值的示例中，最后一个 `case` 中使用 `_` 来匹配无效的 `score` 值。

## 绑定模式

绑定模式使用 `id` 表示，`id` 是一个合法的标识符。与通配符模式相比，绑定模式同样可以匹配任意值，但绑定模式会将匹配到的值与 `id` 进行绑定，在 `=>` 之后可以通过 `id` 访问其绑定的值。

下面的例子中，最后一个 `case` 中使用了绑定模式。其中，变量 `n` 属于 `id` 标识，用于绑定非 `0` 值：

<!-- verify -->

```cangjie
main() {
    let x = -10
    let y = match (x) {
        case 0 => "zero"
        case n => "x is not zero and x = ${n}" // Matched.
    }
    println(y)
}
```

编译执行上述代码，输出结果为：

```text
x is not zero and x = -10
```

使用 `|` 连接多个模式时不能使用绑定模式，也不可嵌套出现在其他模式中，否则会报错：

<!-- compile.error -->

```cangjie
main() {
    let opt = Some(0)
    match (opt) {
        case x | x => {} // Error, variable cannot be introduced in patterns connected by '|'
        case Some(x) | Some(x) => {} // Error, variable cannot be introduced in patterns connected by '|'
        case x: Int64 | x: String => {} // Error, variable cannot be introduced in patterns connected by '|'
    }
}
```

绑定模式 `id` 相当于新定义了一个名为 `id` 的不可变变量（其作用域从引入处开始到该 `case` 结尾处），因此在 `=>` 之后无法对 `id` 进行修改。例如，下例中最后一个 `case` 中对 `n` 的修改是不允许的。

<!-- compile.error -->

```cangjie
main() {
    let x = -10
    let y = match (x) {
        case 0 => "zero"
        case n => n = n + 0 // Error, 'n' cannot be modified.
                  "x is not zero"
    }
    println(y)
}
```

对于每个 `case` 分支，`=>` 之后变量作用域级别与 `case` 后 `=>` 前引入的变量作用域级别相同，在 `=>` 之后再次引入相同名字会触发重定义错误。例如：

<!-- compile.error -->

```cangjie
main() {
    let x = -10
    let y = match (x) {
        case 0 => "zero"
        case n => let n = 0 // Error, redefinition
                  println(n)
                  "x is not zero"
    }
    println(y)
}
```

> **注意：**
>
> 当模式的 identifier 为 enum 构造器时，该模式会被当成 enum 模式进行匹配，而不是绑定模式（关于 enum 模式，详见 [enum 模式](#enum-模式)章节）。

<!-- verify -->

```cangjie
enum RGBColor {
    | Red | Green | Blue
}

main() {
    let x = Red
    let y = match (x) {
        case Red => "red" // The 'Red' is enum mode here.
        case _ => "not red"
    }
    println(y)
}
```

编译执行上述代码，输出结果为：

```text
red
```

## Tuple 模式

Tuple 模式用于 tuple 值的匹配，它的定义和 tuple 字面量类似：`(p_1, p_2, ..., p_n)`，区别在于这里的 `p_1` 到 `p_n`（`n` 大于等于 `2`）是模式（可以是本章节中介绍的任何模式，多个模式间使用逗号分隔）而不是表达式。

例如，`(1, 2, 3)` 是一个包含三个常量模式的 tuple 模式，`(x, y, _)` 是一个包含两个绑定模式，一个通配符模式的 tuple 模式。

给定一个 tuple 值 `tv` 和一个 tuple 模式 `tp`，当且仅当 `tv` 每个位置处的值均能与 `tp` 中对应位置处的模式相匹配，才称 `tp` 能匹配 `tv`。例如，`(1, 2, 3)` 仅可以匹配 tuple 值 `(1, 2, 3)`，`(x, y, _)` 可以匹配任何三元 tuple 值。

下面的例子中，展示了 tuple 模式的使用：

<!-- verify -->

```cangjie
main() {
    let tv = ("Alice", 24)
    let s = match (tv) {
        case ("Bob", age) => "Bob is ${age} years old"
        case ("Alice", age) => "Alice is ${age} years old" // Matched, "Alice" is a constant pattern, and 'age' is a variable pattern.
        case (name, 100) => "${name} is 100 years old"
        case (_, _) => "someone"
    }
    println(s)
}
```

编译执行上述代码，输出结果为：

```text
Alice is 24 years old
```

同一个 tuple 模式中不允许引入多个名称相同的绑定模式。例如，下例中最后一个 `case` 中的 `case (x, x)` 是不合法的。

<!-- compile.error -->

```cangjie
main() {
    let tv = ("Alice", 24)
    let s = match (tv) {
        case ("Bob", age) => "Bob is ${age} years old"
        case ("Alice", age) => "Alice is ${age} years old"
        case (name, 100) => "${name} is 100 years old"
        case (x, x) => "someone" // Error, Cannot introduce a variable pattern with the same name, which will be a redefinition error.
    }
    println(s)
}
```

## 类型模式

类型模式用于判断一个值的运行时类型是否是某个类型的子类型。类型模式有两种形式：`_: Type`（嵌套一个通配符模式 `_`）和 `id: Type`（嵌套一个绑定模式 `id`），它们的区别是后者会发生变量绑定，而前者不会。

对于待匹配值 `v` 和类型模式 `id: Type`（或 `_: Type`），首先判断 `v` 的运行时类型是否是 `Type` 的子类型，若成立则视为匹配成功，否则视为匹配失败；如匹配成功，则将 `v` 的类型转换为 `Type` 并与 `id` 进行绑定（对于 `_: Type`，不存在绑定这一操作）。

假设有如下两个类，`Base` 和 `Derived`，并且 `Derived` 是 `Base` 的子类，`Base` 的无参构造函数中将 `a` 的值设置为 `10`，`Derived` 的无参构造函数中将 `a` 的值设置为 `20`：

<!-- verify -mergeCase -->

```cangjie
open class Base {
    var a: Int64
    public init() {
        a = 10
    }
}

class Derived <: Base {
    public init() {
        a = 20
    }
}
```

下面的代码展示了使用类型模式并匹配成功的例子：

<!-- verify -mergeCase -->

```cangjie
func test1() {
    var d = Derived()
    var r = match (d) {
        case b: Base => b.a // Matched.
        case _ => 0
    }
    println("r = ${r}")
}
```

下面的代码展示了使用类型模式但类型模式匹配失败的例子：

<!-- verify -mergeCase -->

```cangjie
func test2() {
    var b = Base()
    var r = match (b) {
        case d: Derived => d.a  // Type pattern match failed.
        case _ => 0             // Matched.
    }
    println("r = ${r}")
}
```

<!-- verify -mergeCase -->

```cangjie
main() {
    test1()
    test2()
}
```

编译执行上述代码，输出结果为（第一行为 test1 的输出结果，第二行则是 test2 的输出结果）：

<!-- verify -mergeCase -->

```text
r = 20
r = 0
```

## enum 模式

enum 模式用于匹配 `enum` 类型的实例，它的定义和 `enum` 的构造器类似：无参构造器 `C` 或有参构造器 `C(p_1, p_2, ..., p_n)`，构造器的类型前缀可以省略，区别在于这里的 `p_1` 到 `p_n`（`n` 大于等于 `1`）是模式。例如，`Some(1)` 是一个包含一个常量模式的 enum 模式，`Some(x)` 是一个包含一个绑定模式的 enum 模式。

给定一个 enum 实例 `ev` 和一个 enum 模式 `ep`，当且仅当 `ev` 的构造器名字和 `ep` 的构造器名字相同，且 `ev` 参数列表中每个位置处的值均能与 `ep` 中对应位置处的模式相匹配，才称 `ep` 能匹配 `ev`。例如，`Some("one")` 仅可以匹配 `Option<String>` 类型的`Some` 构造器 `Option<String>.Some("one")`，`Some(x)` 可以匹配任何 Option 类型的 `Some` 构造器。

下面的例子中，展示了 enum 模式的使用，因为 `x` 的构造器是 `Year`，所以会和第一个 `case` 匹配：

<!-- verify -->

```cangjie
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

main() {
    let x = Year(2)
    let s = match (x) {
        case Year(n) => "x has ${n * 12} months" // Matched.
        case TimeUnit.Month(n) => "x has ${n} months"
    }
    println(s)
}
```

编译执行上述代码，输出结果为：

```text
x has 24 months
```

当使用 `|` 连接多个 enum 模式时，每个模式必须独立且不能引入新的变量。这是因为 `|` 表示“或”的关系，而变量的引入需要明确的上下文，不能在多个模式之间共享。下面示例为反例示范，其中第五、六个 `case` 不符合该条规则：

<!-- compile.error -->

```cangjie
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

main() {
    let x = Year(2)
    let s = match (x) {
        case Year(5) => "1:OK"
        case Month(m) => "2:OK"
        case Year(0) | Year(1) | Month(_) => "3:OK"
        case Year(_) => "4:OK"
        case Year(2) | Month(m) => "5:invalid" // Error, Variable cannot be introduced in patterns connected by '|'
        case Year(n: UInt64) | Month(n: UInt64) => "6:invalid" // Error, Variable cannot be introduced in patterns connected by '|'
    }
    println(s)
}
```

上述示例中，第二个 `case` 引入了一个新变量 `m`，但没有使用 `|` 连接其他模式，故此是合法的。

使用 `match` 表达式匹配 `enum` 值时，要求 `case` 之后的模式要覆盖待匹配 `enum` 类型中的所有构造器，如果未做到完全覆盖，编译器将报错：

<!-- compile.error -->

```cangjie
enum RGBColor {
    | Red | Green | Blue
}

main() {
    let c = Green
    let cs = match (c) { // Error, Not all constructors of RGBColor are covered.
        case Red => "Red"
        case Green => "Green"
    }
    println(cs)
}
```

可以通过加上 `case Blue` 来实现完全覆盖，也可以在 `match` 表达式的最后通过使用 `case _` 来覆盖其他 `case` 未覆盖的到的情况，如：

<!-- verify -->

```cangjie
enum RGBColor {
    | Red | Green | Blue
}

main() {
    let c = Blue
    let cs = match (c) {
        case Red => "Red"
        case Green => "Green"
        case _ => "Other" // Matched.
    }
    println(cs)
}
```

上述代码的执行结果为：

```text
Other
```

## 模式的嵌套组合

Tuple 模式和 enum 模式可以嵌套任意模式。下面的代码展示了不同模式嵌套组合使用：

<!-- verify -->

```cangjie
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

enum Command {
    | SetTimeUnit(TimeUnit)
    | GetTimeUnit
    | Quit
}

main() {
    let command = (SetTimeUnit(Year(2022)), SetTimeUnit(Year(2024)))
    match (command) {
        case (SetTimeUnit(Year(year)), _) => println("Set year ${year}")
        case (_, SetTimeUnit(Month(month))) => println("Set month ${month}")
        case _ => ()
    }
}
```

编译并执行上述代码，输出结果为：

```text
Set year 2022
```
