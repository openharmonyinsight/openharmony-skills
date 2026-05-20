# 模式的 Refutability

模式可以分为两类：`refutable` 模式和 `irrefutable` 模式。在类型匹配的前提下，当一个模式有可能和待匹配值不匹配时，称此模式为 `refutable` 模式；反之，当一个模式总是可以和待匹配值匹配时，称此模式为 `irrefutable` 模式。

对于上述介绍的各种模式，规定如下：

常量模式是 `refutable` 模式。例如，下例中第一个 case 中的 `1` 和第二个 case 中的 `2` 都有可能和 `x` 的值不相等。

<!-- compile -->

```cangjie
func constPat(x: Int64) {
    match (x) {
        case 1 => "one"
        case 2 => "two"
        case _ => "_"
    }
}
```

通配符模式是 `irrefutable` 模式。例如，下例中无论 `x` 的值是多少，`_` 总能和其匹配。

<!-- compile -->

```cangjie
func wildcardPat(x: Int64) {
    match (x) {
        case _ => "_"
    }
}
```

绑定模式是 `irrefutable` 模式。例如，下例中无论 `x` 的值是多少，绑定模式 `a` 总能和其匹配。

<!-- compile -->

```cangjie
func varPat(x: Int64) {
    match (x) {
        case a => "x = ${a}"
    }
}
```

Tuple 模式是 `irrefutable` 模式，当且仅当其包含的每个模式都是 `irrefutable` 模式。例如，下例中 `(1, 2)` 和 `(a, 2)` 都有可能和 `x` 的值不匹配，所以它们是 `refutable` 模式，而 `(a, b)` 可以匹配任何 `x` 的值，所以它是 `irrefutable` 模式。

<!-- compile -->

```cangjie
func tuplePat(x: (Int64, Int64)) {
    match (x) {
        case (1, 2) => "(1, 2)"
        case (a, 2) => "(${a}, 2)"
        case (a, b) => "(${a}, ${b})"
    }
}
```

类型模式是 `refutable` 模式。例如，下例中（假设 `Base` 是 `Derived` 的父类，并且 `Base` 实现了接口 `I`），`x` 的运行时类型有可能既不是 `Base` 也不是 `Derived`，所以 `a: Derived` 和 `b: Base` 均是 `refutable` 模式。

<!-- compile -->

```cangjie
interface I {}
open class Base <: I {}
class Derived <: Base {}

func typePat(x: I) {
    match (x) {
        case a: Derived => "Derived"
        case b: Base => "Base"
        case _ => "Other"
    }
}
```

enum 模式是 `irrefutable` 模式，当且仅当它对应的 `enum` 类型中只有一个有参构造器，且 enum 模式中包含的其他模式也是 `irrefutable` 模式。例如，对于下例中的 `E1` 和 `E2` 定义，函数 `enumPat1` 中的 `A(1)` 是 `refutable` 模式，`A(a)` 是 `irrefutable` 模式；而函数 `enumPat2` 中的 `B(b)` 和 `C(c)` 均是 `refutable` 模式。

<!-- compile -->

```cangjie
enum E1 {
    A(Int64)
}

enum E2 {
    B(Int64) | C(Int64)
}

func enumPat1(x: E1) {
    match (x) {
        case A(1) => "A(1)"
        case A(a) => "A(${a})"
    }
}

func enumPat2(x: E2) {
    match (x) {
        case B(b) => "B(${b})"
        case C(c) => "C(${c})"
    }
}
```
