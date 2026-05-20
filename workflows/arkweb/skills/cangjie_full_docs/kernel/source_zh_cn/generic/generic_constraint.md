# 泛型约束

泛型约束的作用是在 function、class、interface、struct、enum 声明时明确泛型形参所具备的操作与能力。只有声明了这些约束才能调用相应的成员函数。在很多场景下泛型形参是需要加以约束的，以 `id` 函数为例：

<!-- compile -->

```cangjie
func id<T>(a: T) {
    return a
}
```

开发者唯一能做的事情就是将函数形参 `a` 这个值返回，而不能进行 `a + 1`，`println("${a}")` 等操作，因为它可能是一个任意的类型，比如 `(Bool) -> Bool`，这样就无法与整数相加，同样因为是函数类型，也不能通过 `println` 函数来输出在命令行上。而如果这一泛型形参上有了约束，那么就可以做更多操作了。

约束大致分为接口约束与 class 类型约束。在函数或类型的声明体之前，可以使用 `where` 关键字来声明泛型约束。对于声明的泛型形参 `T1, T2`，可以使用 `where T1 <: Interface, T2 <: Class` 这样的方式来声明泛型约束。如果同一个类型变元的多个约束，可以使用 `&` 连接，例如，`where T1 <: Interface1 & Interface2`。

仓颉中的 `println` 函数能接受类型为字符串的参数。如果需要把一个泛型类型的变量转为字符串后打印在命令行上，可以对这个泛型类型变元加以约束，这个约束是 `core` 中定义的 `ToString` 接口，显然它是一个接口约束：

```cangjie
package std.core // `ToString` is defined in core.

public interface ToString {
    func toString(): String
}
```

这样就可以利用这个约束，定义一个名为 `genericPrint` 的函数：

<!-- verify -->

```cangjie
func genericPrint<T>(a: T) where T <: ToString {
    println(a)
}

main() {
    genericPrint<Int64>(10)
}
```

结果为：

```text
10
```

如果 genericPrint 函数的类型实参没有实现 ToString 接口，那么编译器会报错。例如传入一个函数做为参数时：

<!-- compile.error -->

```cangjie
func genericPrint<T>(a: T) where T <: ToString {
    println(a)
}

main() {
    genericPrint<(Int64) -> Int64>({ i => 0 })
}
```

如果对上面的文件进行编译，那么编译器会抛出泛型类型参数不满足约束的错误。因为 `genericPrint` 函数的泛型的类型实参不满足约束 `(Int64) -> Int64 <: ToString`。

除了上述通过接口来表示约束，还可以使用 class 类型来约束一个泛型类型变元。例如：当要声明一个动物园类型 `Zoo<T>`，但是需要这里声明的类型形参 `T` 受到约束，这个约束就是 `T` 需要是动物类型 `Animal` 的子类型， `Animal` 类型中声明了 `run` 成员函数。这里声明两个子类型 `Dog` 与 `Fox` 都实现了 `run` 成员函数，这样在 `Zoo<T>` 的类型中，就可以对于 `animals` 数组列表中存放的动物实例调用 `run` 成员函数：

<!-- verify -->

```cangjie
import std.collection.ArrayList

abstract class Animal {
    public func run(): String
}

class Dog <: Animal {
    public func run(): String {
        return "dog run"
    }
}

class Fox <: Animal {
    public func run(): String {
        return "fox run"
    }
}

class Zoo<T> where T <: Animal {
    var animals: ArrayList<Animal> = ArrayList<Animal>()
    public func addAnimal(a: T) {
        animals.add(a)
    }

    public func allAnimalRuns() {
        for(a in animals) {
            println(a.run())
        }
    }
}

main() {
    var zoo: Zoo<Animal> = Zoo<Animal>()
    zoo.addAnimal(Dog())
    zoo.addAnimal(Fox())
    zoo.allAnimalRuns()
}
```

程序的输出为：

```text
dog run
fox run
```

> **注意：**
>
> 泛型变元的约束只能是具体的 class 类型或 interface，且变元如果存在多个 class 类型的上界时，它们必须在同一继承链路上。
