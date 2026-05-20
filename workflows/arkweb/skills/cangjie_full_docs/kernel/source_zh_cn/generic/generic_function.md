# 泛型函数

如果一个函数声明了一个或多个类型形参，则将其称为泛型函数。语法上，类型形参紧跟在函数名后，并用 `<>` 括起，如果有多个类型形参，则用 `,` 分离。

## 全局泛型函数

在声明全局泛型函数时，只需要在函数名后使用尖括号声明类型形参，然后就可以在函数形参、返回类型及函数体中对这一类型形参进行引用。例如 `id` 函数定义为：

<!-- compile -->

```cangjie
func id<T>(a: T): T {
    return a
}
```

其中， `(a: T)` 是函数声明的形参，它使用到了 `id` 函数声明的类型形参 `T`，并且在 `id` 函数的返回类型使用。

再比如另一个复杂的例子，定义如下一个泛型函数 `composition`，该函数声明了 3 个类型形参，分别是 `T1, T2, T3`，其功能是把两个函数 `f: (T1) -> T2, g: (T2) -> T3` 复合成类型为 `(T1) -> T3` 的函数。

<!-- verify -composition -->

```cangjie
func composition<T1, T2, T3>(f: (T1) -> T2, g: (T2) -> T3): (T1) -> T3 {
    return {x: T1 => g(f(x))}
}
```

因为可以被用来复合的函数是任意类型，例如可以是 `(Int32) -> Bool, (Bool) -> Int64` 的复合，也可以是 `(Int64) -> Rune, (Rune) -> Int8` 的复合，所以才需要使用泛型函数。

<!-- verify -composition -->

```cangjie
func times2(a: Int64): Int64 {
    return a * 2
}

func plus10(a: Int64): Int64 {
    return a + 10
}

func times2plus10(a: Int64) {
    return composition<Int64, Int64, Int64>(times2, plus10)(a)
}

main() {
  println(times2plus10(9))
}
```

这里，复合两个 `(Int64) -> Int64` 的函数，将 9 先乘以 2，再加 10，结果会是 28。

<!-- verify -composition -->

```text
28
```

## 局部泛型函数

局部函数也可以是泛型函数。例如泛型函数 `id` 可以嵌套定义在其他函数中：

<!-- verify -->

```cangjie
func foo(a: Int64) {
    func id<T>(a: T): T { a }

    func double(a: Int64): Int64 { a + a }

    return (id<Int64> ~> double)(a) == (double ~> id<Int64>)(a)
}

main() {
    println(foo(1))
}
```

这里由于 `id` 的单位元性质，函数 `id<Int64> ~> double` 和 `double ~> id<Int64>` 是等价的，结果是 `true`。

```text
true
```

## 泛型成员函数

class、struct 与 enum 的成员函数可以是泛型的。例如：

<!-- verify -->

```cangjie
class A {
    func foo<T>(a: T): Unit where T <: ToString {
        println("${a}")
    }
}

struct B {
    func bar<T>(a: T): Unit where T <: ToString {
        println("${a}")
    }
}

enum C {
    | X | Y

    func coo<T>(a: T): Unit where T <: ToString {
        println("${a}")
    }
}

main() {
    var a = A()
    var b = B()
    var c = C.X
    a.foo<Int64>(10)
    b.bar<String>("abc")
    c.coo<Bool>(false)
}
```

程序输出的结果为：

```text
10
abc
false
```

在为类型使用 extend 声明进行扩展时，扩展中的函数也可以是泛型的，例如可以为 `Int64` 类型增加一个泛型成员函数：

<!-- verify -->

```cangjie
extend Int64 {
    func printIntAndArg<T>(a: T) where T <: ToString {
        println(this)
        println("${a}")
    }
}

main() {
    var a: Int64 = 12
    a.printIntAndArg<String>("twelve")
}
```

程序输出的结果将为：

```text
12
twelve
```

## 静态泛型函数

interface、class、struct、enum 与 extend 中可以定义静态泛型函数，例如下例 `ToPair` class 中从 `ArrayList` 中返回一个元组：

<!-- run -->

```cangjie
import std.collection.ArrayList

class ToPair {
    public static func fromArray<T>(l: ArrayList<T>): (T, T) {
        return (l[0], l[1])
    }
}

main() {
    var res: ArrayList<Int64> = ArrayList([1,2,3,4])
    var a: (Int64, Int64) = ToPair.fromArray<Int64>(res)
}
```
