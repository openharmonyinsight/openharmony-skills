# 扩展概述

扩展可以为在当前 `package` 中可见的类型（除函数、元组、接口）添加新功能。

当不能破坏被扩展类型的封装性，但希望添加额外的功能时，可以使用扩展。

可以添加的功能包括：

- 添加成员函数
- 添加操作符重载函数
- 添加成员属性
- 实现接口

上述具体添加的功能方式可参考如下示例，具体使用语法请参考后续介绍：

<!-- compile -->

```cangjie
interface Foo {
    func printValue(a: Int64): Unit
}

class Boo {
    var boo: Int64 =2
}

extend Boo {
    public prop x: Int64 { // 添加成员属性
        get() {
            123
        }
    }

    func newMember(): Unit {
        println("This is a member function of a new extension.") // 添加成员函数
    }

    public operator func -() {
        println("Overload the operator addition function.") // 添加操作符重载函数
        -x
    }
}

// 接口扩展，实现接口
extend<T> Array<T> <: Foo {
    public func printValue(a: Int64) {
        println("The is ${a}.")
    }
}
```

扩展虽然可以添加额外的功能，但不能变更被扩展类型的封装性，因此扩展不支持以下功能：

1. 扩展不能增加成员变量。
2. 扩展的函数和属性必须拥有实现。
3. 扩展的函数和属性不能使用 `open`、`override`、 `redef`修饰。
4. 扩展不能访问被扩展类型中 `private` 修饰的成员。

根据扩展有没有实现新的接口，扩展可以分为**直接扩展**和**接口扩展**两种用法。直接扩展即不包含额外接口的扩展；接口扩展即包含接口的扩展，接口扩展可以用来为现有的类型添加新功能并实现接口，增强抽象灵活性。
