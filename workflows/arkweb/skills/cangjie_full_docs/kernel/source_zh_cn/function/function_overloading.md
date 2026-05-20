# 函数重载

## 函数重载定义

在仓颉编程语言中，如果一个作用域中，一个函数名对应多个函数定义，这种现象称为函数重载。

- 函数名相同，函数参数不同（是指参数个数不同，或者参数个数相同但参数类型不同）的两个函数构成重载。示例如下：

  <!-- compile -->

  ```cangjie
  // Scenario 1

  func f(a: Int64): Unit {}
  func f(a: Float64): Unit {}
  func f(a: Int64, b: Float64): Unit {}
  ```

- 对于两个同名泛型函数 (详见[泛型函数](../generic/generic_function.md)章节），如果重命名一个函数的泛型形参后（使泛型参数顺序相同），其非泛型部分与另一个函数的非泛型部分函数参数不同，则两个函数构成重载，否则这两个泛型函数构成重复定义错误（类型变元的约束不参与判断）。示例如下：

  <!-- compile.error -->

  ```cangjie
  // Scenario 2

  interface I1{}
  interface I2{}

  func f1<X, Y>(a: X, b: Y) {}
  func f1<Y, X>(a: X, b: Y) {} // OK: after rename generic type parameter, it will be 'func f1<X, Y>(a: Y, b: X)'

  func f2<T>(a: T) where T <: I1 {} // Error, not overloading
  func f2<T>(a: T) where T <: I2 {} // Error, not overloading
  ```

- 同一个类内的两个构造函数参数不同，构成重载。示例如下：

  <!-- compile -->

  ```cangjie
  // Scenario 3

  class C {
      var a: Int64
      var b: Float64

      public init(a: Int64, b: Float64) {
          this.a = a
          this.b = b
      }

      public init(a: Int64) {
          b = 0.0
          this.a = a
      }
  }
  ```

- 同一个类内的主构造函数和 `init` 构造函数参数不同，构成重载（认为主构造函数和 `init` 函数具有相同的名字）。示例如下：

  <!-- compile -->

  ```cangjie
  // Scenario 4

  class C {
      C(var a!: Int64, var b!: Float64) {
          this.a = a
          this.b = b
      }

      public init(a: Int64) {
          b = 0.0
          this.a = a
      }
  }
  ```

- 两个函数名相同，参数不同的函数定义在不同的作用域，在两个函数都可见的作用域中构成重载。示例如下：

  <!-- compile -->

  ```cangjie
  // Scenario 5

  func f(a: Int64): Unit {}

  func g() {
      func f(a: Float64): Unit {}
  }
  ```

- 如果子类中存在与父类同名的函数，并且函数的参数类型不同，则构成函数重载。示例如下：

  <!-- compile -->

  ```cangjie
  // Scenario 6
  open class Base {
      public func f(a: Int64): Unit {}
  }

  class Sub <: Base {
      public func f(a: Float64): Unit {}
  }
  ```

只允许函数声明引入的函数重载，但是以下情形不构成重载，不构成重载的两个名字不能定义或声明在同一个作用域内：

- class、interface、struct 类型的静态成员函数和实例成员函数之间不能重载
- enum 类型的 constructor、静态成员函数和实例成员函数之间不能重载

如下示例，两个变量均为函数类型且函数参数类型不同，但由于它们不是函数声明所以不能重载，如下示例将编译报错（重定义错）：

<!-- compile.error -->

```cangjie
main() {
    var f: (Int64) -> Unit
    var f: (Float64) -> Unit
}
```

如下示例，虽然变量 `f` 为函数类型，但由于变量和函数之间不能同名，如下示例将编译报错（重定义错）：

<!-- compile.error -->

```cangjie
main() {
    var f: (Int64) -> Unit
    func f(a: Float64): Unit {} // Error, functions and variables cannot have the same name
}
```

如下示例，静态成员函数 `f` 与实例成员函数 `f` 的参数类型不同，但由于类内静态成员函数和实例成员函数之间不能重载，如下示例将编译报错：

<!-- compile.error -->

```cangjie
class C {
    public static func f(a: Int64): Unit {}
    public func f(a: Float64): Unit {}
}
```

## 函数重载决议

函数调用时，所有可被调用的函数（是指当前作用域可见且能通过类型检查的函数）构成候选集，候选集中有多个函数，究竟选择候选集中哪个函数，需要进行函数重载决议，有如下规则：

- 优先选择作用域级别高的作用域内的函数。在嵌套的表达式或函数中，越是内层作用域级别越高。

  如下示例中在 `inner` 函数体内调用 `g(Sub())` 时，候选集包括 `inner` 函数内定义的函数 `g` 和 `inner` 函数外定义的函数 `g`，函数决议选择作用域级别更高的 `inner` 函数内定义的函数 `g`。

    <!-- compile -->

    ```cangjie
    open class Base {}
    class Sub <: Base {}

    func outer() {
        func g(a: Sub) {
            print("1")
        }

        func inner() {
            func g(a: Base) {
                print("2")
            }

            g(Sub())   // Output: 2
        }
    }
    ```

- 如果作用域级别相对最高的仍有多个函数，则需要选择最匹配的函数（对于函数 f 和 g 以及给定的实参，如果 f 可以被调用时 g 也总是可以被调用的，但反之不然，则称 f 比 g 更匹配）。如果不存在唯一最匹配的函数，则报错。

  如下示例中，两个函数 `g` 定义在同一作用域，选择更匹配的函数 `g(a: Sub): Unit`。

    <!-- compile -->

    ```cangjie
    open class Base {}
    class Sub <: Base {}

    func outer() {
        func g(a: Sub) {
            print("1")
        }
        func g(a: Base) {
            print("2")
        }

        g(Sub())   // Output: 1

    }
    ```

- 子类和父类认为是同一作用域。如下示例中，一个函数 `g` 定义在父类中，另一个函数 `g` 定义在子类中，在调用 `s.g(Sub())` 时，两个函数 `g` 当成同一作用域级别决议，则选择更匹配的父类中定义的函数 `g(a: Sub): Unit`。

    <!-- compile -->

    ```cangjie
    open class Base {
        public func g(a: Sub) {
            print("1")
        }
    }

    class Sub <: Base {
        public func g(a: Base) {
            print("2")
        }
    }

    func outer() {
        let s: Sub = Sub()
        s.g(Sub()) // Output: 1
    }
    ```
