# 注解

仓颉中提供了一些内置编译标记用来支持一些特殊情况的处理。

## 确保正确使用整数运算溢出策略的内置编译标记

仓颉中提供三种内置编译标记来控制整数溢出的处理策略，即 `@OverflowThrowing`，`@OverflowWrapping` 和 `@OverflowSaturating` ，这些编译标记当前只能标记于函数声明之上，作用于函数内的整数运算和整型转换。它们分别对应以下三种溢出处理策略：

1. 抛出异常（throwing）：当整数运算溢出时，抛出异常。

    <!-- compile -->

    ```cangjie
    @OverflowThrowing
    func add(a: Int8, b: Int8){
        return a + b
    }
    main() {
        add(100,29)
        /* 100 + 29 在数学上等于 129，
        * 在 Int8 的表示范围上发生了上溢出，
        * 程序抛出异常
        */
    }
    ```

    需要注意的是，对于整数溢出行为是 throwing 的场景，若整数溢出可提前在编译期检测出来，则编译器会直接给出报错。

    <!-- compile.error -->

    ```cangjie
    @OverflowThrowing
    main() {
        let res: Int8 = Int8(100) + Int8(29) // Error, arithmetic operation '+' overflow
        // 100 + 29 在数学上等于 129，在 Int8 的表示范围上发生了上溢出，编译器检测出来并报错
        let con: UInt8 = UInt8(-132) // Error, integer type conversion overflow
        /* -132 在 UInt8 的表示范围上发生了下溢出，
        * 程序抛出异常
        */
    }
    ```

2. 高位截断（wrapping）：当整数运算的结果超出用于接收它的内存空间所能表示的数据范围时，则截断超出该内存空间的部分。

    <!-- compile -->

    ```cangjie
    @OverflowWrapping
    main() {
        let res: Int8 = Int8(105) * Int8(4)
        /* 105 * 4 在数学上等于 420，
        * 对应的二进制为 1 1010 0100，
        * 超过了用于接收该结果的 8 位内存空间，
        * 截断后的结果在二进制上表示为 1010 0100，
        * 对应为有符号整数 -92
        */
        let temp: Int16 = Int16(-132)
        let con: UInt8 = UInt8(temp)
        /* -132 对应的二进制为 1111 1111 0111 1100，
        * 超过了用于接收该结果的 8 位内存空间，
        * 截断后的结果在二进制上表示为 0111 1100
        * 对应为有符号整数 124
        */
    }
    ```

3. 饱和（saturating）：当整数运算溢出时，选择对应固定精度的极值作为结果。

    <!-- compile -->

    ```cangjie
    @OverflowSaturating
    main() {
        let res: Int8 = Int8(-100) - Int8(45)
        /* -100 - 45 在数学上等于 -145，
        * 在 Int8 的表示范围上发生了下溢出，
        * 选择 Int8 的最小值 -128 作为结果
        */
        let con: Int8 = Int8(1024)
        /* 1024 在 Int8 的表示范围上发生了上溢出，
        * 选择 Int8 的最大值 127 作为结果
        */
    }
    ```

默认情况下（即未标注该类内置编译标记时），采取抛出异常（`@OverflowThrowing`）的处理策略。

实际情况下需要根据业务场景的需求正确选择溢出策略。例如要在 `Int32` 上实现某种安全运算，使得计算结果和计算过程在数学上相等，就需要使用抛出异常的策略。

【反例】

<!-- compile -->

```cangjie
// 计算结果被高位截断
@OverflowWrapping
func operation(a: Int32, b: Int32): Int32 {
    a + b // No exception will be thrown when overflow occurs
}
```

该错误例子使用了高位截断的溢出策略，比如当传入的参数 `a` 和 `b` 较大导致结果溢出时，会产生高位截断的情况，导致函数返回结果和计算表达式 `a + b` 在数学上不是相等关系。

【正例】

<!-- run -->

```cangjie
// 安全
@OverflowThrowing
func operation(a: Int32, b: Int32): Int32 {
    a + b
}

main(): Int64 {
    try {
        operation(Int32.Max, 1)
    } catch (e: ArithmeticException) {
        println(e.message)
        //Handle error
    }
    0
}
```

该正确例子使用了抛出异常的溢出策略，当传入的参数 `a` 和 `b` 较大导致整数溢出时，`operation` 函数会抛出异常。

以下表格汇总了仓颉中各类操作符是否可能会引发整数溢出的情况。

|        操作符类型        |        操作符        | 是否可能引发整数溢出 |
| :------------------: | :------------------: | -------------------- |
|    算术操作符      |         +          |          是           |
|         算术操作符     |         -          |          是           |
|         算术操作符     |         *          |          是           |
|         算术操作符     |         /          |          是           |
|         算术操作符     |         %          |          否           |
| 算术操作符 | ** | 是 |
| 自增操作符 | ++ | 是 |
| 自减操作符 | -- | 是 |
| 位操作符       | !                    |          否          |
|         位操作符      |         &          |          否           |
| 位操作符 | <code>&vert;</code>  |          否           |
|         位操作符      |         ^          |          否           |
| 位操作符       | <<                   |          是          |
| 位操作符 | >> | 否 |
|         关系操作符         |         !=         |          否           |
|         关系操作符     |         <          |          否           |
|         关系操作符     |         >          |          否           |
|         关系操作符         |         >=         |          否           |
|         关系操作符         |         <=         |          否           |
|         关系操作符         |         ==         |          否           |
| 赋值操作符 | = | 否 |
| 复合赋值操作符 | += | 是 |
| 复合赋值操作符 | -= | 是 |
| 复合赋值操作符 | *= | 是 |
| 复合赋值操作符 | /= | 是 |
| 复合赋值操作符 | %= | 否 |
| 复合赋值操作符 | **= | 是 |
| 复合赋值操作符 | <<= | 是 |
| 复合赋值操作符 | >>= | 否 |
| 复合赋值操作符 | &= | 否 |
| 复合赋值操作符 | <code>&vert;=</code> | 否 |
| 复合赋值操作符 | ^= | 否 |

## 测试框架内置编译标记

在测试中使用 mock 时，当 mock 的对象是与静态和顶级声明相关内容时，需要通过测试框架内置编译标记来指示编译器做一些准备工作，才能正常使用 mock。

测试框架内置编译标记 `@EnsurePreparedToMock` 只能在 lambda 表达式上使用，lambda 表达式调用静态和顶级声明作为其最后一个表达式，然后编译器将准备这个声明以供 mock。

例如：

<!-- run -pkg1 -->
<!-- cfg="-p prod --mock=on --output-type=dylib" -->

```cangjie
package prod

public func test(a: String, b: String): String {
    a + b
}
```

<!-- run -pkg1 -->
<!-- cfg="-lprod -L . --test" -->

```cangjie
package test

import prod.*
import std.unittest.mock.*

@Test
public class TestA {
    @TestCase
    func case1(): Unit {
        { =>
            let matcher0 = Matchers.eq("z")
            let matcher1 = Matchers.eq("y")
            let stubCall = @EnsurePreparedToMock { => return(test(matcher0.value(), matcher1.value())) }
            ConfigureMock.stubFunction(stubCall,[matcher0.withDescription(#"eq("z")"#), matcher1.withDescription(#"eq("y")"#)], Option<String>.None, "test", #"test("z", "y")"#, 15)
        }().returns("mocked value")
        println(test("z", "y")) // prints "mocked value"
    }
}
```

上述示例中，`ConfigureMock.stubFunction` 为函数 `test` 注册了一个桩，`returns` 为定义的桩设置返回值。

> **注意：**
>
> 通常，标准库的 mock 接口可用于定义 mock 声明，并且在常规情况下不应直接使用此内置注释。相反，应该使用相应的标准库函数。这些标准库函数在内部使用 `@EnsurePreparedToMock`。

使用 `@EnsurePreparedToMock` 注解的约束：

- 仅当使用测试和 mock 相关编译选项进行编译时才允许使用（使用 `--test`/`--test-only` 和 `--mock=on`/`--mock=runtime-error` 编译选项）。
- 只能应用于具有合适的最后一个表达式的 lambda。
- lambda 的最后一个表达式应该是调用、成员访问或引用表达式，要求是：
    - 顶级函数或变量；
    - 静态函数、属性或字段；
    - foreign 声明​​；
    - 不是局部函数或变量；
    - 非私有声明；
    - 不是 const 表达式或声明；
    - 必须是来自通过 mock 模式构建的包的声明。

## 自定义注解

自定义注解机制用来让反射（详见[反射章节](dynamic_feature.md)）获取标注内容，目的是在类型元数据之外提供更多的有用信息，以支持更复杂的逻辑。

开发者可以通过自定义类型标注 `@Annotation` 方式创建自己的自定义注解。`@Annotation` 只能修饰 `class`，并且不能是 `abstract` 或 `open` 或 `sealed` 修饰的 `class`。当一个 `class` 声明它标注了 `@Annotation`，那么它必须要提供至少一个 `const init` 函数，否则编译器会报错。

下面的例子定义了一个自定义注解 `@Version`，并用其修饰 `A`, `B` 和 `C`。在 `main` 中，通过反射获取到类上的 `@Version` 注解信息，并将其打印出来。

<!-- verify -->

```cangjie
package pkg

import std.reflect.TypeInfo

@Annotation
public class Version {
    let code: String
    const init(code: String) {
        this.code = code
    }
}

@Version["1.0"]
class A {}

@Version["1.1"]
class B {}

main() {
    let objects = [A(), B()]
    for (obj in objects) {
        let annOpt = TypeInfo.of(obj).findAnnotation<Version>()
        if (let Some(ann) <- annOpt) {
            println(ann.code)
        }
    }
}
```

编译并执行上述代码，输出结果为：

```text
1.0
1.1
```

注解信息需要在编译时生成信息并绑定到类型上，自定义注解在使用时必须使用 `const init` 构建出合法的实例。注解声明语法与声明宏语法一致，后面的 `[]` 括号中需要按顺序或命名参数规则传入参数，且参数必须是 const 表达式，详见[常量求值章节](../function/const_func_and_eval.md)。对于拥有无参构造函数的注解类型，声明时允许省略中括号。

下面的例子中定义了一个拥有无参 `const init` 的自定义注解 `@Marked`，使用时 `@Marked` 和 `@Marked[]` 这两种写法均可。

<!-- verify -->

```cangjie
package pkg

import std.reflect.TypeInfo

@Annotation
public class Marked {
    const init() {}
}

@Marked
class A {}

@Marked[]
class B {}

main() {
    if (TypeInfo.of(A()).findAnnotation<Marked>().isSome()) {
        println("A is Marked")
    }
    if (TypeInfo.of(B()).findAnnotation<Marked>().isSome()) {
        println("B is Marked")
    }
}
```

编译并执行上述代码，输出结果为：

```text
A is Marked
B is Marked
```

对于同一个注解目标，同一个注解类不允许声明多次，即不可重复。

<!-- verify.error -->
<!-- cfg="--Marked" -->

```cangjie
@Marked
@Marked // Error
class A {}
```

`Annotation` 不会被继承，因此一个类型的注解元数据只会来自它定义时声明的注解。如果需要父类型的注解元数据信息，需要开发者自己用反射接口查询。

下面的例子中，`A` 被 `@Marked` 注解修饰，`B` 继承 `A`，但是 `B` 没有 `A` 的注解。

<!-- verify -->

```cangjie
package pkg

import std.reflect.TypeInfo

@Annotation
public class Marked {
    const init() {}
}

@Marked
open class A {}

class B <: A {}

main() {
    if (TypeInfo.of(A()).findAnnotation<Marked>().isSome()) {
        println("A is Marked")
    }
    if (TypeInfo.of(B()).findAnnotation<Marked>().isSome()) {
        println("B is Marked")
    }
}
```

编译并执行上述代码，输出结果为：

```text
A is Marked
```

自定义注解可以用在类型声明（`class`、`struct`、`enum`、`interface`）、成员函数/构造函数中的参数、构造函数声明、成员函数声明、成员变量声明、成员属性声明。也可以限制自己可以使用的位置，这样可以减少开发者的误用，这类注解需要在声明 `@Annotation` 时标注 `target` 参数，参数类型为 `Array<AnnotationKind>`。其中，`AnnotationKind` 是标准库中定义的 `enum`。当没有限定 target 的时候，该自定义注解可以用在以上全部位置。当限定 target 时，只能用在声明的列表中。

<!-- compile -->

```cangjie
public enum AnnotationKind {
    | Type
    | Parameter
    | Init
    | MemberProperty
    | MemberFunction
    | MemberVariable
}
```

下面的例子中，自定义注解通过 `target` 限定只能用在成员函数上，用在其他位置会编译报错。

<!--compile.error -->

```cangjie
@Annotation[target: [MemberFunction]]
public class Marked {
    const init() {}
}

class A {
    @Marked // OK, member funciton
    func marked() {}
}

@Marked // Error, type
class B {}
```
