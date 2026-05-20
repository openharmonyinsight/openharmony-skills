# 类型别名

当某个类型的名字比较复杂或者在特定场景中不够直观时，可以选择使用类型别名的方式为此类型设置一个别名。

```cangjie
type I64 = Int64
```

类型别名的定义以关键字 `type` 开头，接着是类型的别名（如上例中的 `I64`），然后是等号 `=`，最后是原类型（即被取别名的类型，如上例中的 `Int64`）。

只能在源文件顶层定义类型别名，并且原类型必须在别名定义处可见。例如，下例中 `Int64` 的别名定义在 `main` 中将报错，`LongNameClassB` 类型在为其定义别名时不可见，同样报错。

<!-- compile.error  -->

```cangjie
main() {
    type I64 = Int64 // Error, type aliases can only be defined at the top level of the source file
}

class LongNameClassA { }
type B = LongNameClassB // Error, type 'LongNameClassB' is not defined
```

一个（或多个）类型别名定义中禁止出现（直接或间接的）循环引用。

<!-- compile.error  -->

```cangjie
type A = (Int64, A) // Error, 'A' refered itself
type B = (Int64, C) // Error, 'B' and 'C' are circularly refered
type C = (B, Int64)
```

类型别名并不会定义一个新的类型，它仅仅是为原类型定义了另外一个名字，它有如下几种使用场景：

1. 作为类型使用，例如：

    <!-- compile -->

    ```cangjie
    type A = B
    class B {}
    var a: A = B() // Use typealias A as type B
    ```

2. 当类型别名实际指向的类型为 class、struct 时，可以作为构造器名称使用：

    <!-- compile -->

    ```cangjie
    type A = B
    class B {}
    func foo() { A() }  // Use type alias A as constructor of B
    ```

3. 当类型别名实际指向的类型为 class、interface、struct 时，可以作为访问内部静态成员变量或函数的类型名：

    <!-- compile -->

    ```cangjie
    type A = B
    class B {
        static var b : Int32 = 0
        static func foo() {}
    }
    func foo() {
        A.foo() // Use A to access static method in class B
        A.b
    }
    ```

4. 当类型别名实际指向的类型为 enum 时，可以作为 enum 声明的构造器的类型名：

    <!-- compile -->

    ```cangjie
    enum TimeUnit {
        Day | Month | Year
    }
    type Time = TimeUnit
    var a = Time.Day  
    var b = Time.Month   // Use type alias Time to access constructors in TimeUnit
    ```

需要注意的是，当前用户自定义的类型别名暂不支持在类型转换表达式中使用，参考如下示例：

<!-- compile.error  -->

```cangjie
type MyInt = Int32
MyInt(0)  // Error, no matching function for operator '()' function call
```

## 泛型别名

类型别名也是可以声明类型形参的，但是不能对其形参使用 `where` 声明约束，对于泛型变元的约束会在后面给出解释。

当一个泛型类型的名称过长时，可以使用类型别名来为其声明一个更短的别名。例如，有一个类型为 `RecordData` ，可以把他用类型别名简写为 `RD` ：

<!-- compile -->

```cangjie
struct RecordData<T> {
    var a: T
    public init(x: T) {
        a = x
    }
}

type RD<T> = RecordData<T>

main(): Int64 {
    var struct1: RD<Int32> = RecordData<Int32>(2)
    return 1
}
```

在使用时就可以用 `RD<Int32>` 来代指 `RecordData<Int32>` 类型。
