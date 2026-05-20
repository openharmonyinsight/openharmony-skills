# 闭包

一个函数或 lambda 从定义它的静态作用域中捕获了变量，函数或 lambda 和捕获的变量一起被称为一个闭包，这样即使脱离了闭包定义所在的作用域，闭包也能正常运行。

函数或 lambda 的定义中对于以下几种变量的访问，称为变量捕获：

- 函数的参数缺省值中访问了本函数之外定义的局部变量；

- 函数或 lambda 内访问了本函数或本 lambda 之外定义的局部变量;

- `class`/`struct` 内定义的不是成员函数的函数或 lambda 访问了实例成员变量或 `this`。

以下情形的变量访问不是变量捕获：

- 对定义在本函数或本 lambda 内的局部变量的访问；

- 对本函数或本 lambda 的形参的访问；

- 对全局变量和静态成员变量的访问；

- 对实例成员变量在实例成员函数或属性中的访问。由于实例成员函数或属性将 `this` 作为参数传入，在实例成员函数或属性内通过 `this` 访问所有实例成员变量。

变量的捕获发生在闭包定义时，因此变量捕获有以下规则：

- 被捕获的变量必须在闭包定义时可见，否则编译报错；

- 被捕获的变量必须在闭包定义时已经完成初始化，否则编译报错。

示例 1：闭包 `add`，捕获了 `let` 声明的局部变量 `num`，之后通过返回值返回到 `num` 定义的作用域之外，调用 `add` 时仍可正常访问 `num`。

<!-- verify -->

```cangjie
func returnAddNum(): (Int64) -> Int64 {
    let num: Int64 = 10

    func add(a: Int64) {
        return a + num
    }
    add
}

main() {
    let f = returnAddNum()
    println(f(10))
}
```

程序输出的结果为：

```text
20
```

示例 2：捕获的变量必须在闭包定义时可见。

<!-- compile.error -->

```cangjie
func f() {
    let x = 99
    func f1() {
        println(x)
    }
    let f2 = { =>
        println(y)  // Error, cannot capture 'y' which is not defined yet
    }
    let y = 88
    f1()            // Print 99
    f2()
}
```

示例 3：捕获的变量必须在闭包定义前完成初始化。

<!-- compile.error -error-->

```cangjie
func f() {
    let x: Int64
    func f1() {
        println(x) // Error, x is not initialized yet
    }
    x = 99
    f1()
}
```

示例 4：如果捕获的变量是引用类型，可修改其可变实例成员变量的值。

<!-- run -->

```cangjie
class C {
    public var num: Int64 = 0
}

func returnIncrementer(): () -> Unit {
    let c: C = C()

    func incrementer() {
        c.num++
    }

    incrementer
}

main() {
    let f = returnIncrementer()
    f() // c.num increases by 1
}
```

示例 5：为了防止捕获了 `var` 声明变量的闭包逃逸，这类闭包只能被调用，不能作为一等公民使用，包括不能赋值给变量，不能作为实参或返回值使用，不能直接将闭包的名字作为表达式使用。其中，闭包逃逸是指在函数执行完毕后仍然可以在函数外部被调用的闭包。

<!-- compile.error -->

```cangjie
func f() {
    var x = 1
    let y = 2

    func g() {
        println(x)  // OK, captured a mutable variable.
    }
    let b = g       // Error, g cannot be assigned to a variable

    g               // Error, g cannot be used as an expression
    g()             // OK, g can be invoked

    g               // Error, g cannot be used as a return value
}
```

示例 6：需要注意的是，捕获具有传递性。如果一个函数 `f` 调用了捕获 `var` 变量的函数 `g`，且 `g` 捕获的 `var` 变量不在函数 `f` 内定义，那么函数 `f` 同样捕获了 `var` 变量，此时，`f` 也不能作为一等公民使用。

示例 6.1：`g` 捕获了 `var` 声明的变量 `x`，`f` 调用了 `g`，且 `g` 捕获的 `x` 不在 `f` 内定义，`f` 同样不能作为一等公民使用：

<!-- compile.error -error-->

```cangjie
func h(){
    var x = 1

    func g() { x }  // captured a mutable variable

    func f() {
        g()         // invoked g
    }
    return f        // Error
}
```

示例 6.2：`g` 捕获了 `var` 声明的变量 `x`，`f` 调用了 `g`。但 `g` 捕获的 `x` 在 `f` 内定义，`f` 没有捕获其他 `var` 声明的变量。因此，`f` 仍作为一等公民使用：

<!-- compile -->

```cangjie
func h(){
    func f() {
        var x = 1
        func g() { x } // captured a mutable variable

        g()
    }
    return f // OK
}
```

示例 7：静态成员变量和全局变量的访问，不属于变量捕获，因此访问了 `var` 修饰的全局变量、静态成员变量的函数或 lambda 仍可作为一等公民使用。

<!-- compile -->

```cangjie
class C {
    static public var a: Int32 = 0
    static public func foo() {
        a++ // OK
        return a
    }
}

var globalV1 = 0

func countGlobalV1() {
    globalV1++
    C.a = 99
    let g = C.foo // OK
}

func g(){
    let f = countGlobalV1 // OK
    f()
}
```
