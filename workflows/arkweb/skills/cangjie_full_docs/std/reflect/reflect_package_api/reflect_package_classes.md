# 类

## class ClassTypeInfo

```cangjie
public class ClassTypeInfo <: TypeInfo {}
```

功能：描述 `class` 类型的类型信息。

父类型：

- [TypeInfo](#class-typeinfo)

### prop constructors

```cangjie
public prop constructors: Collection<ConstructorInfo>
```

功能：获取该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 的所有 `public` 构造函数信息，返回对应集合。

> **注意：**
>
> - 如果该 `class` 类型无任何 `public` 构造函数，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ConstructorInfo](reflect_package_classes.md#class-constructorinfo)>

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public var myName = ""
    public init() {}
    public init(name: String) {
        myName = name
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")
    // 获取 constructors
    for (i in ty.constructors) {
        println(i)
    }
    return
}
```

运行结果：

```text
init()
init(String)
```

### prop instanceVariables

```cangjie
public prop instanceVariables: Collection<InstanceVariableInfo>
```

功能：获取该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 的所有 `public` 实例成员变量信息，返回对应集合。

> **注意：**
>
> - 如果该 `class` 类型无任何 `public` 实例成员变量，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 该集合不包含任何继承而来的 `public` 实例成员变量。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo)>

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
    public var myName = ""
    public init() {}
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")
    // 获取 instanceVariables
    for (i in ty.instanceVariables) {
        println(i)
    }
    return
}
```

运行结果：

```text
length: Int64
width: Int64
myName: String
```

### prop sealedSubclasses

```cangjie
public prop sealedSubclasses: Collection<ClassTypeInfo>
```

功能：如果该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 类型拥有 `sealed` 语义，则获取该 `class` 类型所在包内的所有子类的类型信息，返回对应集合。

> **注意：**
>
> - 如果该 `class` 类型不拥有 `sealed` 语义，则返回空集合。
> - 如果该 `class` 类型拥有 `sealed` 语义，那么获得的集合必不可能是空集合，因为该 `class` 类型本身就是自己的子类。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo)>

### prop staticVariables

```cangjie
public prop staticVariables: Collection<StaticVariableInfo>
```

功能：获取该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 的所有 `public` 静态成员变量信息，返回对应集合。

> **注意：**
>
> - 如果该 `class` 类型无任何 `public` 静态成员变量，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 该集合不包含任何继承而来的 `public` 静态成员变量。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo)>

### prop superClass

```cangjie
public prop superClass: Option<ClassTypeInfo>
```

功能：获取该 `class` 类型信息所对应的 `class` 类型的直接父类。

> **注意：**
>
> 理论上只有 class [Object](../../core/core_package_api/core_package_classes.md#class-object) 没有直接父类。

类型：[Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo)>

### static func get(String)

```cangjie
public redef static func get(qualifiedName: String): ClassTypeInfo
```

功能：获取给定限定名称所对应类型的 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo)。

参数：

- qualifiedName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 类型的限定名称。

返回值：

- [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) - 类型的限定名称 `qualifiedName` 所对应的类型的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获取与给定类型的限定名称 `qualifiedName` 匹配的类型所对应的类型信息，则抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {}

main(): Unit {
    let ty = ClassTypeInfo.get("default.Rectangular")
    println(ty)
    return
}
```

运行结果：

```text
default.Rectangular
```

### static func of(Any)

```cangjie
public redef static func of(a: Any): ClassTypeInfo
```

功能：获取给定的任意类型的实例的运行时类型所对应的类型信息。

运行时类型是指在程序运行时，通过动态绑定确定的类型，运行时类型与实例对象相绑定。在继承等场景下运行时类型和静态类型可能不一致。

参数：

- a: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 任意类型的实例。

返回值：

- [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) - 实例 `a` 的运行时类型所对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得实例 `a` 的运行时类型所对应的类型信息，则抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {}

main(): Unit {
    var r = Rectangular()
    let ty = ClassTypeInfo.of(r)
    println(ty)
    return
}
```

运行结果：

```text
test.Rectangular
```

### static func of(Object)

```cangjie
public static func of(a: Object): ClassTypeInfo
```

功能：获取给定的 `class` 类型的实例的运行时类型所对应的 `class` 类型信息。

参数：

- a: [Object](../../core/core_package_api/core_package_classes.md#class-object) - `class` 类型的实例。

返回值：

- [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) - `class` 类型的实例 `a` 的运行时类型所对应的 `class` 类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得实例 `a` 的运行时类型所对应的 `class` 类型信息，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {}

main(): Unit {
    var r = Rectangular()
    let ty = ClassTypeInfo.of(r)
    println(ty)
    return
}
```

运行结果：

```text
test.Rectangular
```

### static func of\<T>()

```cangjie
public redef static func of<T>(): ClassTypeInfo
```

功能：获取给定类型 `T` 对应的类型信息。

返回值：

- [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) - `T` 类型对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得类型 T 所对应的类型信息，抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {}

main(): Unit {
    let ty = ClassTypeInfo.of<Rectangular>()
    println(ty)
    return
}
```

运行结果：

```text
default.Rectangular
```

### func construct(Array\<Any>)

```cangjie
public func construct(args: Array<Any>): Any
```

功能：在该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 类型中根据实参列表搜索匹配的构造函数并调用，传入实参列表，返回调用结果。

参数：

- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Any](../../core/core_package_api/core_package_interfaces.md#interface-any)> - 实参列表。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该 `class` 类型的实例。

异常：

- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果该 `class` 类型拥有 `abstract` 语义，调用 `construct` 则抛出异常，因为抽象类不可被实例化。
- [MisMatchException](reflect_package_exceptions.md#class-mismatchexception) - 如果 `args` 未能成功匹配任何该 `class` 类型的可见性为 `public` 的构造函数，则抛出异常。
- [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) - 在被调用的构造函数内部抛出的任何异常均将被封装为 [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) 异常并抛出。

示例：

<!-- run -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
    public var myName = ""
    public init() {}
    public init(name: String) {
        myName = name
    }
    public init(name: String, length: Int64, width: Int64) {
        myName = name
        this.length = length
        this.width = width
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 通过不同入参构造实例
    ty.construct()
    ty.construct("Small rectangular")
    ty.construct("Big rectangular", 1, 1)
    return
}
```

### func getConstructor(Array\<TypeInfo>)

```cangjie
public func getConstructor(parameterTypes: Array<TypeInfo>): ConstructorInfo
```

功能：尝试在该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 类型中获取与给定形参类型信息列表匹配的 `public` 构造函数的信息。

参数：

- parameterTypes: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[TypeInfo](reflect_package_classes.md#class-typeinfo)> - 形参类型信息列表。

返回值：

- [ConstructorInfo](reflect_package_classes.md#class-constructorinfo) - 如果成功匹配则返回该 `public` 构造函数的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应 `public` 构造函数，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
    public var myName = ""
    public init() {}
    public init(name: String) {
        myName = name
    }
    public init(name: String, length: Int64, width: Int64) {
        myName = name
        this.length = length
        this.width = width
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取指定构造函数信息
    let ci01 = ty.getConstructor(StructTypeInfo.get("String"))
    println(ci01)

    // 获取指定构造函数信息
    let ci02 = ty.getConstructor(StructTypeInfo.get("String"), PrimitiveTypeInfo.get("Int64"),
        PrimitiveTypeInfo.get("Int64"))
    println(ci02)
    return
}
```

运行结果：

```text
init(String)
init(String, Int64, Int64)
```

### func getInstanceVariable(String)

```cangjie
public func getInstanceVariable(name: String): InstanceVariableInfo
```

功能：给定变量名称，尝试获取该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 所对应的 `class` 类型中匹配的实例成员变量的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 变量名称。

返回值：

- [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) - 如果成功匹配则返回该实例成员变量的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应实例成员变量，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
    public var myName = ""
    public init() {}
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取类实例成员信息
    let ivi = ty.getInstanceVariable("myName")
    println(ivi)
    return
}
```

运行结果：

```text
myName: String
```

### func getStaticVariable(String)

```cangjie
public func getStaticVariable(name: String): StaticVariableInfo
```

功能：给定变量名称，尝试获取该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 所对应的 `class` 类型中匹配的静态成员变量的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 变量名称。

返回值：

- [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) - 如果成功匹配则返回该静态成员变量的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应静态成员变量，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public static var area: Int64 = 10
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取静态变量
    let sv = ty.getStaticVariable("area")
    println(sv)
    return
}
```

运行结果：

```text
static area: Int64
```

### func isAbstract()

```cangjie
public func isAbstract(): Bool
```

功能：判断该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 类型是否是抽象类。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 类型是抽象类则返回 `true`，否则返回 `false`。

### func isOpen()

```cangjie
public func isOpen(): Bool
```

功能：判断该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 类型是否拥有 `open` 语义。

> **注意：**
>
> 并不是只有被 `open` 修饰符所修饰的 `class` 类型定义才拥有 `open` 语义，如：`abstract class` 无论是否被 `open` 修饰符修饰都会拥有 `open` 语义。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 类型拥有 `open` 语义则返回 `true`，否则返回 `false`。

### func isSealed()

```cangjie
public func isSealed(): Bool
```

功能：判断该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 类型是否拥有 `sealed` 语义。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 对应的 `class` 类型拥有 `sealed` 语义则返回 `true`，否则返回 `false`。

## class ConstructorInfo

```cangjie
public class ConstructorInfo <: Equatable<ConstructorInfo> & Hashable & ToString {}
```

功能：描述构造函数信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[ConstructorInfo](#class-constructorinfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [ConstructorInfo](reflect_package_classes.md#class-constructorinfo) 对应的构造函数的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该构造函数信息所对应的构造函数，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop parameters

```cangjie
public prop parameters: ReadOnlyList<ParameterInfo>
```

功能：获取该 [ConstructorInfo](reflect_package_classes.md#class-constructorinfo) 所对应的构造函数的参数类型列表。

> **注意：**
>
> 不保证参数顺序，可根据 `ParameterInfo`的 `index` 属性确定参数实际位置。

类型：[ReadOnlyList](../../collection/collection_package_api/collection_package_interface.md#interface-readonlylistt)\<[ParameterInfo](reflect_package_classes.md#class-parameterinfo)>

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
    public var myName = ""
    public init() {}
    public init(name: String) {
        myName = name
    }
    public init(name: String, length: Int64, width: Int64) {
        myName = name
        this.length = length
        this.width = width
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")
    // 获取 constructors
    for (i in ty.constructors) {
        // 获取 parameters
        for (j in i.parameters) {
            println("${i} 的入参有 ${j}")
        }
    }
    return
}
```

运行结果：

```text
init(String) 的入参有 String
init(String, Int64, Int64) 的入参有 String
init(String, Int64, Int64) 的入参有 Int64
init(String, Int64, Int64) 的入参有 Int64
```

### func apply(Array\<Any>)

```cangjie
public func apply(args: Array<Any>): Any
```

功能：调用该 [ConstructorInfo](reflect_package_classes.md#class-constructorinfo) 对应的构造函数，传入实参列表，并返回调用结果。

参数：

- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Any](../../core/core_package_api/core_package_interfaces.md#interface-any)> - 实参列表。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 由该构造函数构造得到的类型实例。

异常：

- [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) - 如果该构造函数信息所对应的构造函数所属的类型是抽象类，则会抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果实参列表 `args` 中的实参的数目与该构造函数信息所对应的构造函数的形参列表中的形参的数目不等，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实参列表 `args` 中的任何一个实参的运行时类型不是该构造函数信息所对应的构造函数的对应形参的声明类型的子类型，则抛出异常。
- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 如果被调用的构造函数信息所对应的构造函数内部抛出异常，则该异常将被封装为 [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) 异常并抛出。

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该构造器信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该构造器信息的哈希值。

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该构造函数信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该构造函数信息。

### operator func !=(ConstructorInfo)

```cangjie
public operator func !=(that: ConstructorInfo): Bool
```

功能：判断该构造器信息与给定的另一个构造器信息是否不等。

参数：

- that: [ConstructorInfo](reflect_package_classes.md#class-constructorinfo) - 被比较相等性的另一个构造器信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该构造器信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(ConstructorInfo)

```cangjie
public operator func ==(that: ConstructorInfo): Bool
```

功能：判断该构造器信息与给定的另一个构造器信息是否相等。

参数：

- that: [ConstructorInfo](reflect_package_classes.md#class-constructorinfo) - 被比较相等性的另一个构造器信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该构造器信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class GenericTypeInfo

```cangjie
public class GenericTypeInfo <: TypeInfo & Equatable<GenericTypeInfo> {}
```

功能：描述泛型类型信息。

父类型：

- [TypeInfo](./reflect_package_classes.md#class-typeinfo)
- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[GenericTypeInfo](./reflect_package_classes.md#class-generictypeinfo)>

### operator func ==(GenericTypeInfo)

```cangjie
public operator func ==(that: GenericTypeInfo): Bool
```

功能：判断该泛型类型信息与给定的另一个泛型类型信息是否相等。

参数：

- that: [GenericTypeInfo](reflect_package_classes.md#class-generictypeinfo) - 被比较相等性的另一个泛型类型信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该泛型类型信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class GlobalFunctionInfo

```cangjie
public class GlobalFunctionInfo <: Equatable<GlobalFunctionInfo> & Hashable & ToString {}
```

功能：描述全局函数信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[GlobalFunctionInfo](#class-globalfunctioninfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有 [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 对应的全局函数的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该全局函数信息所对应全局函数，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop genericParams

```cangjie
public prop genericParams: Collection<GenericTypeInfo>
```

功能：获取该 [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 对应的实例成员函数的泛型参数信息列表。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[GenericTypeInfo](reflect_package_classes.md#class-generictypeinfo)>

异常：

- [InfoNotFoundException](./reflect_package_exceptions.md#class-infonotfoundexception) - [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 没有泛型参数时抛出异常。

### prop name

```cangjie
public prop name: String
```

功能：获取该 [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 对应的全局函数的名称。

> **注意：**
>
> 构成重载的所有全局函数将拥有相同的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop parameters

```cangjie
public prop parameters: ReadOnlyList<ParameterInfo>
```

功能：获取该 [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 对应的全局函数的参数信息列表。

> **注意：**
>
> 不保证参数顺序，可根据 `ParameterInfo`的 `index` 属性确定参数实际位置。

类型：[ReadOnlyList](../../collection/collection_package_api/collection_package_interface.md#interface-readonlylistt)\<[ParameterInfo](reflect_package_classes.md#class-parameterinfo)>

### prop returnType

```cangjie
public prop returnType: TypeInfo
```

功能：获取该 [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 对应的全局函数的返回类型的类型信息。

类型：[TypeInfo](reflect_package_classes.md#class-typeinfo)

### func apply(Array\<Any>)

```cangjie
public func apply(args: Array<Any>): Any
```

功能：调用该 [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 对应的全局函数，传入实参列表，返回调用结果。

> **注意：**
>
> `args` 的类型确保和函数入参类型完全一致，否则会导致参数检查失败。

参数：

- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Any](../../core/core_package_api/core_package_interfaces.md#interface-any)> - 实参列表。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该全局函数的调用结果。

异常：

- [InvocationTargetException](../reflect_package_api/reflect_package_exceptions.md#class-invocationtargetexception) - 如果存在泛型参数的函数调用了该方法，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果实参列表 `args` 中的实参的数目与该全局函数信息 `GlobalFunctionInfo` 所对应的全局函数的形参列表中的形参的数目不等，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实参列表 `args` 中的任何一个实参的运行时类型不是该全局函数信息所对应的全局函数的对应形参的声明类型的子类型，则抛出异常。
- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 如果被调用的全局函数信息所对应全局函数内部抛出异常，则该异常将被封装为 [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) 异常并抛出。

### func apply(Array\<TypeInfo>, Array\<Any>)

```cangjie
public func apply(genericTypeArgs: Array<TypeInfo>, args: Array<Any>): Any
```

功能：调用该 [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 对应的全局泛型函数，传入泛型参数类型列表和实参列表，返回调用结果。

> **注意：**
>
> `args` 的类型确保和函数入参类型完全一致，否则会导致参数检查失败。

参数：

- genericTypeArgs: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[TypeInfo](./reflect_package_classes.md#class-typeinfo)> - 泛型参数类型列表。
- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Any](../../core/core_package_api/core_package_interfaces.md#interface-any)> - 实参列表。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该全局函数的调用结果。

异常：

- [InvocationTargetException](../reflect_package_api/reflect_package_exceptions.md#class-invocationtargetexception) - 如果非泛型函数调用了该方法，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果实参列表 `args` 中的实参的数目与该全局函数信息 `GlobalFunctionInfo` 所对应的全局函数的形参列表中的形参的数目不等，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果函数泛型参数列表 `genericTypeArgs` 中的参数数目与该全局函数信息所对应的全局函数的泛型参数列表 `genericParams` 中的参数数目不等，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实参列表 `args` 中的任何一个实参的运行时类型不是该全局函数信息所对应的全局函数的对应形参的声明类型的子类型，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果传入的参数列表 `args` 和泛型参数类型列表 `genericTypeArgs` 不满足该全局函数信息所对应的全局函数的参数的类型约束，则抛出异常。
- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 如果被调用的全局函数信息所对应全局函数内部抛出异常，则该异常将被封装为 [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) 异常并抛出。

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该全局函数信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该全局函数信息的哈希值。

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该全局函数信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该全局函数信息。

### operator func !=(GlobalFunctionInfo)

```cangjie
public operator func !=(that: GlobalFunctionInfo): Bool
```

功能：判断该全局函数信息与给定的另一个全局函数信息是否不等。

参数：

- that: [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) - 被比较相等性的另一个全局函数信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该全局函数信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(GlobalFunctionInfo)

```cangjie
public operator func ==(that: GlobalFunctionInfo): Bool
```

功能：判断该全局函数信息与给定的另一个全局函数信息是否相等。

参数：

- that: [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) - 被比较相等性的另一个全局函数信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该全局函数信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class GlobalVariableInfo

```cangjie
public class GlobalVariableInfo <: Equatable<GlobalVariableInfo> & Hashable & ToString {}
```

功能：描述全局变量信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[GlobalVariableInfo](#class-globalvariableinfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo) 对应的全局变量的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该全局变量信息所对应的全局变量，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop name

```cangjie
public prop name: String
```

功能：获取该 [GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo) 对应的全局变量的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop typeInfo

```cangjie
public prop typeInfo: TypeInfo
```

功能：获取该 [GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo) 对应的全局变量的声明类型的类型信息。

类型：[TypeInfo](reflect_package_classes.md#class-typeinfo)

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func getValue()

```cangjie
public func getValue(): Any
```

功能：获取该 [GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo) 对应的全局变量的值。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该全局变量的值。

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该全局变量信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该全局变量信息的哈希值。

### func isMutable()

```cangjie
public func isMutable(): Bool
```

功能：判断该 [GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo) 对应的全局变量是否可修改。

> **注意：**
>
> - 如果实例成员变量被 `var` 修饰符所修饰，则该全局变量可被修改。
> - 如果实例成员变量被 `let` 修饰符所修饰，则该全局变量不可被修改。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该全局变量可被修改则返回 `true` ，否则返回 `false`。

### func setValue(Any)

```cangjie
public func setValue(newValue: Any): Unit
```

功能：设置该 [GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo) 对应的全局变量的值。

参数：

- newValue: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 新的值。

异常：

- [IllegalSetException](reflect_package_exceptions.md#class-illegalsetexception) - 如果该全局变量信息所对应的全局变量不可修改，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果新值 `newValue` 的运行时类型不是全局变量信息所对应的全局变量的声明类型的子类型，则抛出异常。

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该全局变量信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该全局变量信息。

### operator func !=(GlobalVariableInfo)

```cangjie
public operator func !=(that: GlobalVariableInfo): Bool
```

功能：判断该全局变量信息与给定的另一个全局变量信息是否不等。

参数：

- that: [GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo) - 被比较相等性的另一个全局变量信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该全局变量信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(GlobalVariableInfo)

```cangjie
public operator func ==(that: GlobalVariableInfo): Bool
```

功能：判断该全局变量信息与给定的另一个全局变量信息是否相等。

参数：

- that: [GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo) - 被比较相等性的另一个全局变量信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该全局变量信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class InstanceFunctionInfo

```cangjie
public class InstanceFunctionInfo <: Equatable<InstanceFunctionInfo> & Hashable & ToString {}
```

功能：描述实例成员函数信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[InstanceFunctionInfo](#class-instancefunctioninfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 对应的实例成员函数的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该实例成员函数信息所对应的实例成员函数，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop genericParams

```cangjie
public prop genericParams: Collection<GenericTypeInfo>
```

功能：获取该 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 对应的实例成员函数的泛型参数信息列表。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[GenericTypeInfo](reflect_package_classes.md#class-generictypeinfo)>

异常：

- [InfoNotFoundException](./reflect_package_exceptions.md#class-infonotfoundexception) - [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 没有泛型参数时抛出异常。

### prop modifiers

```cangjie
public prop modifiers: Collection<ModifierInfo>
```

功能：获取该 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 对应的实例成员函数所拥有的所有修饰符的信息，返回对应集合。

> **注意：**
>
> - 如果该实例成员函数无任何修饰符，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 即便未被某修饰符修饰，如果拥有该修饰符的语义，该修饰符信息也将被包括在该集合中。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ModifierInfo](reflect_package_enums.md#enum-modifierinfo)>

### prop name

```cangjie
public prop name: String
```

功能：获取该 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 对应的实例成员函数的名称。

> **注意：**
>
> - 构成重载的所有实例成员函数将拥有相同的名称。
> - 操作符重载函数的名称就是该操作符本身的符号内容，如"`+`"，"`*`"，"`[]`"。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop parameters

```cangjie
public prop parameters: ReadOnlyList<ParameterInfo>
```

功能：获取该 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 对应的实例成员函数的参数信息列表。

> **说明：**
>
> 不保证参数顺序，可根据 `ParameterInfo`的 `index` 属性确定参数实际位置。

类型：[ReadOnlyList](../../collection/collection_package_api/collection_package_interface.md#interface-readonlylistt)\<[ParameterInfo](reflect_package_classes.md#class-parameterinfo)>

### prop returnType

```cangjie
public prop returnType: TypeInfo
```

功能：获取该 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 对应的实例成员函数的返回值类型的类型信息。

类型：[TypeInfo](reflect_package_classes.md#class-typeinfo)

### func apply(Any, Array\<Any>)

```cangjie
public func apply(instance: Any, args: Array<Any>): Any
```

功能：调用该 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 对应实例成员函数，指定实例并传入实参列表，返回调用结果。

> **注意：**
>
> `args` 的类型确保和函数入参类型完全一致。

参数：

- instance: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 实例。
- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Any](../../core/core_package_api/core_package_interfaces.md#interface-any)> - 实参列表。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该实例成员函数的调用结果。

异常：

- [InvocationTargetException](../reflect_package_api/reflect_package_exceptions.md#class-invocationtargetexception) - 如果存在泛型参数的函数调用了该方法，则抛出异常。
- [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) - 如果该实例成员函数信息所对应的实例成员函数是抽象的，或不存在相应的函数实现，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果实参列表 `args` 中的实参的数目与该实例成员函数信息所对应的实例成员函数的形参列表中的形参的数目不等，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实例 `instance` 的运行时类型与该实例成员函数信息所对应的实例成员函数所属的类型不相同，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实参列表 `args` 中的任何一个实参的运行时类型不是该实例成员函数信息所对应的实例成员函数的对应形参的声明类型的子类型，则抛出异常。
- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 如果被调用的实例成员函数信息所对应的实例成员函数内部抛出异常，则该异常将被封装为 [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) 异常并抛出。

### func apply(Any, Array\<TypeInfo>, Array\<Any>)

```cangjie
public func apply(instance: Any, genericTypeArgs: Array<TypeInfo>, args: Array<Any>): Any
```

功能：调用该 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 对应泛型成员函数，指定实例并传入泛型参数的类型列表和参数列表，返回调用结果。

> **注意：**
>
> `args` 的类型确保和函数入参类型完全一致。

参数：

- instance: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 实例。
- genericTypeArgs: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[TypeInfo](./reflect_package_classes.md#class-typeinfo)> - 泛型参数类型信息列表。
- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Any](../../core/core_package_api/core_package_interfaces.md#interface-any)> - 泛型参数列表。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该实例泛型函数的调用结果。

异常：

- [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) - 如果该函数信息对应的成员函数是 `abstract` 或不存在函数体，则会抛出异常。
- [InvacationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) - 如果非泛型函数调用了此方法，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实例 `instance` 的运行时类型与该成员函数信息所对应的成员函数所属的类型不相同，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果实参列表 `args` 中的实参的数目与该成员函数信息所对应的成员函数的形参列表中的形参的数目不等，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果函数泛型参数列表 `genericTypeArgs` 中的参数数目与该成员函数信息所对应的成员函数的泛型参数列表 `genericParams` 中的参数数目不等，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果参数列表 `args` 中的任何一个参数的运行时类型不是该实例成员函数信息所对应的实例成员函数的对应形参的声明类型的子类型，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果传入的参数列表 `args` 和泛型参数类型列表 `genericTypeArgs` 不满足该成员函数信息所对应的成员函数的参数的类型约束，则抛出异常。
- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 如果被调用的实例成员函数信息所对应的实例成员函数内部抛出异常，则该异常将被封装为 [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) 异常并抛出。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
    public func area(): Int64 {
        return length * width
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("default.Rectangular")
    // 获取 InstanceFunctionInfo
    var gif = ty.getInstanceFunction("area")

    // 调用反射函数
    var r = Rectangular()
    var result = gif.apply(r) as Int64
    println(result)
    return
}
```

运行结果：

```text
Some(20)
```

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该实例成员函数信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该实例成员函数信息的哈希值。

### func isAbstract()

```cangjie
public func isAbstract(): Bool
```

功能：判断 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 所对应的实例成员函数是否拥有 `abstract` 语义。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员函数拥有 `abstract` 语义则返回 `true`，否则返回 `false`。

### func isOpen()

```cangjie
public func isOpen(): Bool
```

功能：判断该 [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) 对应的实例成员函数是否拥有 `open` 语义。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员函数拥有 `open` 语义则返回 `true`，否则返回 `false`。

> **注意：**
>
> `interface` 类型中的实例成员函数默认均拥有 `open` 语义。

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该实例成员函数信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该实例成员函数信息。

### operator func !=(InstanceFunctionInfo)

```cangjie
public operator func !=(that: InstanceFunctionInfo): Bool
```

功能：判断该实例成员函数信息与给定的另一个实例成员函数信息是否不等。

参数：

- that: [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) - 被比较相等性的另一个实例成员函数信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员函数信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(InstanceFunctionInfo)

```cangjie
public operator func ==(that: InstanceFunctionInfo): Bool
```

功能：判断该实例成员函数信息与给定的另一个实例成员函数信息是否相等。

参数：

- that: [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) - 被比较相等性的另一个实例成员函数信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员函数信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class InstancePropertyInfo

```cangjie
public class InstancePropertyInfo <: Equatable<InstancePropertyInfo> & Hashable & ToString {}
```

功能：描述实例成员属性信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[InstancePropertyInfo](#class-instancepropertyinfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该实例成员属性信息所对应的实例成员属性，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop modifiers

```cangjie
public prop modifiers: Collection<ModifierInfo>
```

功能：获取该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性所拥有的所有修饰符的信息，返回对应集合。

> **注意：**
>
> - 如果该实例成员属性无任何修饰符，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 即便未被某修饰符修饰，如果拥有该修饰符的语义，该修饰符信息也将被包括在该集合中。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ModifierInfo](reflect_package_enums.md#enum-modifierinfo)>

### prop name

```cangjie
public prop name: String
```

功能：获取该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop typeInfo

```cangjie
public prop typeInfo: TypeInfo
```

功能：获取该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性的声明类型的类型信息。

类型：[TypeInfo](reflect_package_classes.md#class-typeinfo)

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func getValue(Any)

```cangjie
public func getValue(instance: Any): Any
```

功能：获取该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性在给定实例中的值。

参数：

- instance: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 实例。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该实例成员属性在实例 `instance` 中的值。

异常：

- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实例 `instance` 的运行时类型与该实例成员属性信息所对应的实例成员属性所属的类型不严格相同，则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {
    public var length = 4
    public prop width: Int64 {
        get() {
            5
        }
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("default.Rectangular")
    // 获取 InstancePropertyInfo
    var gip = ty.getInstanceProperty("width")

    // 获取实例值
    var r = Rectangular()
    var result = gip.getValue(r) as Int64
    println(result)
    return
}
```

运行结果：

```text
Some(5)
```

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该实例成员属性信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该实例成员属性信息的哈希值。

### func isAbstract()

```cangjie
public func isAbstract(): Bool
```

功能：判断该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性是否是抽象的。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性是抽象的，则返回 `true`，否则返回 `false`。

### func isMutable()

```cangjie
public func isMutable(): Bool
```

功能：判断该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性是否可修改。

> **注意：**
>
> 如果实例成员属性被 `mut` 修饰符所修饰，则该实例成员属性可被修改，否则不可被修改。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员属性信息所对应的实例成员属性可被修改则返回 `true` ，否则返回 `false`。

### func isOpen()

```cangjie
public func isOpen(): Bool
```

功能：判断该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性是否拥有 `open` 语义。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性拥有 `open` 语义则返回 `true`，否则返回 `false`。

### func setValue(Any, Any)

```cangjie
public func setValue(instance: Any, newValue: Any): Unit
```

功能：设置该 [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) 对应的实例成员属性在给定实例中的值。

参数：

- instance: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 实例。
- newValue: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 新值。

异常：

- [IllegalSetException](reflect_package_exceptions.md#class-illegalsetexception) - 如果该实例成员属性信息所对应的实例成员属性不可修改，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实例 `instance` 的运行时类型与该实例成员属性信息所对应的实例成员属性所属的类型不严格相同，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果新值 `newValue` 的运行时类型不是该实例成员属性信息所对应的实例成员属性的声明类型的子类型，则抛出异常。

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该实例成员属性信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该实例成员属性信息。

### operator func !=(InstancePropertyInfo)

```cangjie
public operator func !=(that: InstancePropertyInfo): Bool
```

功能：判断该实例成员属性信息与给定的另一个实例成员属性信息是否不等。

参数：

- that: [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) - 被比较相等性的另一个实例成员属性信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员属性信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(InstancePropertyInfo)

```cangjie
public operator func ==(that: InstancePropertyInfo): Bool
```

功能：判断该实例成员属性信息与给定的另一个实例成员属性信息是否相等。

参数：

- that: [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) - 被比较相等性的另一个实例成员属性信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员属性信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class InstanceVariableInfo

```cangjie
public class InstanceVariableInfo <: Equatable<InstanceVariableInfo> & Hashable & ToString {}
```

功能：描述实例成员变量信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[InstanceVariableInfo](#class-instancevariableinfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) 对应的实例成员变量的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该实例成员变量信息所对应的实例成员变量，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop modifiers

```cangjie
public prop modifiers: Collection<ModifierInfo>
```

功能：获取该 [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) 对应的实例成员变量所拥有的所有修饰符的信息，返回对应集合。

> **注意：**
>
> - 如果该实例成员变量无任何修饰符，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 即便未被某修饰符修饰，如果拥有该修饰符的语义，该修饰符信息也将被包括在该集合中。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ModifierInfo](reflect_package_enums.md#enum-modifierinfo)>

### prop name

```cangjie
public prop name: String
```

功能：获取该 [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) 对应的实例成员变量的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop typeInfo

```cangjie
public prop typeInfo: TypeInfo
```

功能：获取该 [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) 对应的实例成员变量的声明类型的类型信息。

类型：[TypeInfo](reflect_package_classes.md#class-typeinfo)

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func getValue(Any)

```cangjie
public func getValue(instance: Any): Any
```

功能：获取该 [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) 对应的实例成员变量在给定实例中的值。

参数：

- instance: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 实例。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该实例成员变量在实例 `instance` 中的值。

异常：

- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实例 `instance` 的运行时类型与该实例成员变量信息所对应的实例成员变量所属的类型不严格相同，则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("default.Rectangular")
    // 获取 InstanceVariableInfo
    var gip = ty.getInstanceVariable("width")
    // 获取实例值
    var r = Rectangular()
    let v = gip.getValue(r) as Int64
    println(v)
    return
}
```

运行结果：

```text
Some(5)
```

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该实例成员变量信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该实例成员变量信息的哈希值。

### func isMutable()

```cangjie
public func isMutable(): Bool
```

功能：判断该 [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) 对应的实例成员变量是否可修改。

> **注意：**
>
> - 如果实例成员变量被 `var` 修饰符所修饰，则该实例成员变量可被修改。
> - 如果实例成员变量被 `let` 修饰符所修饰，则该实例成员变量不可被修改。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员变量信息所对应的实例成员变量可被修改则返回 `true` ，否则返回 `false`。

### func setValue(Any, Any)

```cangjie
public func setValue(instance: Any, newValue: Any): Unit
```

功能：设置该 [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) 对应的实例成员变量在给定实例中的值。

参数：

- instance: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 实例。
- newValue: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 新值。

异常：

- [IllegalSetException](reflect_package_exceptions.md#class-illegalsetexception) - 如果该实例成员变量信息所对应的实例成员变量不可修改，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实例 `instance` 的运行时类型与该实例成员变量信息所对应的实例成员变量所属的类型不严格相同，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果新值 `newValue` 的运行时类型不是该实例成员变量信息所对应的实例成员变量的声明类型的子类型，则抛出异常。

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该实例成员变量信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该实例成员变量信息。

### operator func !=(InstanceVariableInfo)

```cangjie
public operator func !=(that: InstanceVariableInfo): Bool
```

功能：判断该实例成员变量信息与给定的另一个实例成员变量信息是否不等。

参数：

- that: [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) - 被比较相等性的另一个实例成员变量信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员变量信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(InstanceVariableInfo)

```cangjie
public operator func ==(that: InstanceVariableInfo): Bool
```

功能：判断该实例成员变量信息与给定的另一个实例成员变量信息是否相等。

参数：

- that: [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) - 被比较相等性的另一个实例成员变量信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该实例成员变量信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class InterfaceTypeInfo

```cangjie
public class InterfaceTypeInfo <: TypeInfo {}
```

功能：`interface` 类型的类型信息。

父类型：

- [TypeInfo](#class-typeinfo)

### prop sealedSubtypes

```cangjie
public prop sealedSubtypes: Collection<TypeInfo>
```

功能：如果该 [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo) 所对应的 `interface` 类型拥有 `sealed` 语义，则获取该 `interface` 类型所在包内的所有子类型的类型信息，返回对应集合。

> **注意：**
>
> - 如果该 `interface` 类型不拥有 `sealed` 语义，则返回空集合。
> - 如果该 `interface` 类型拥有 `sealed` 语义，那么获得的集合必不可能是空集合，因为该 `interface` 类型本身就是自己的子类型。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[TypeInfo](reflect_package_classes.md#class-typeinfo)>

### static func get(String)

```cangjie
public redef static func get(qualifiedName: String): InterfaceTypeInfo
```

功能：获取给定 `qualifiedName` 所对应的类型的 [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo)。

参数：

- qualifiedName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 类型的限定名称。

返回值：

- [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo) - 类型的限定名称 `qualifiedName` 所对应的 `Interface` 类型的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获取与给定类型的限定名称 `qualifiedName` 匹配的类型所对应的类型信息，则抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public interface Rectangular {}

main(): Unit {
    let ty = InterfaceTypeInfo.get("default.Rectangular")
    println(ty)
    return
}
```

运行结果：

```text
default.Rectangular
```

### static func of(Any)

```cangjie
public redef static func of(a: Any): InterfaceTypeInfo
```

功能：获取给定的任意类型实例的运行时类型所对应的类型信息。

运行时类型是指在程序运行时，通过动态绑定确定的类型，运行时类型与实例对象相绑定。在继承等场景下运行时类型和静态类型可能不一致。

参数：

- a: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 任意类型的实例。

返回值：

- [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo) - 实例 `a` 的运行时类型所对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得实例 `a` 的运行时类型所对应的类型信息，则抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo)， 则抛出异常。

### static func of\<T>()

```cangjie
public redef static func of<T>(): InterfaceTypeInfo
```

功能：获取给定 `T` 类型对应的类型信息。

返回值：

- [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo) - `T` 类型对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得类型 T 所对应的类型信息，抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo)， 则抛出异常。

### func isSealed()

```cangjie
public func isSealed(): Bool
```

功能：判断该 [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo) 所对应的 `interface` 类型是否拥有 `sealed` 语义。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该 `interface` 类型拥有 `sealed` 语义则返回 `true`，否则返回 `false`。

## class PackageInfo

```cangjie
public class PackageInfo <: Equatable<PackageInfo> & Hashable & ToString {}
```

功能：描述包信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[PackageInfo](#class-packageinfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop variables

```cangjie
public prop variables: Collection<GlobalVariableInfo>
```

功能：获取该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的包中所有 `public` 全局变量的信息所组成的列表。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo)>

### prop functions

```cangjie
public prop functions: Collection<GlobalFunctionInfo>
```

功能：获取该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的包中所有 `public` 全局函数的信息所组成的列表。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo)>

### prop name

```cangjie
public prop name: String
```

功能：获取该包信息所对应的包的名称。

> **注意：**
>
> 包的名称不包含其所在的模块名称和其父包的名称，例如限定名称为 `a/b.c.d` 的包的名称是 `d` 。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop parentPackage

```cangjie
public prop parentPackage: PackageInfo
```

功能：获取该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的父包的 [PackageInfo](reflect_package_classes.md#class-packageinfo)。

类型：[PackageInfo](reflect_package_classes.md#class-packageinfo)

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果父包未被加载，则会抛出异常。

### prop qualifiedName

```cangjie
public prop qualifiedName: String
```

功能：获取该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的包的限定名称。

> **注意：**
>
> 包的限定名称的格式是 `(module_name/)?(default|package_name)(.package_name)*`，例如限定名称为 `a/b.c.d` 的包位于模块 `a` 下的 `b` 包里的 `c` 包里。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop rootPackage

```cangjie
public prop rootPackage: PackageInfo
```

功能：获取该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的 `root` 包的 [PackageInfo](reflect_package_classes.md#class-packageinfo)。

> **注意：**
>
> 如果包本身就是 `root` 包，那么其 `rootPackage` 属性返回的是其本身。例如，限定名称为 `a.b.c` 的包，`rootPackage` 返回的是 `a`; 限定名称为 `a` 的包，`rootpackage` 返回的是 `a`。

类型：[PackageInfo](reflect_package_classes.md#class-packageinfo)

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果 `root` 包未被加载，则会抛出异常。

### prop subPackages

```cangjie
public prop subPackages: Collection<PackageInfo>
```

功能：获取该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的所有子包的 [PackageInfo](reflect_package_classes.md#class-packageinfo) 集合。

> **注意：**
>
> - 该属性只会返回已被加载的子包。
> - 不保证返回结果的顺序。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[PackageInfo](reflect_package_classes.md#class-packageinfo)>

### prop typeInfos

```cangjie
public prop typeInfos: Collection<TypeInfo>
```

功能：获取该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的包中所有全局定义的 `public` 类型的类型信息，返回对应集合。

> **注意：**
>
> 目前该列表不包含所有反射尚未支持的类型。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[TypeInfo](reflect_package_classes.md#class-typeinfo)>

### prop version

```cangjie
public prop version: String
```

功能：获取该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的包的版本号。

> **注意：**
>
> 由于目前动态库中尚无版本信息，获取到的版本号总是空字符串。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static func get(String)

```cangjie
public static func get(qualifiedName: String): PackageInfo
```

功能：获取给定 `qualifiedName` 所对应的 [PackageInfo](./reflect_package_classes.md#class-packageinfo)。

参数：

- qualifiedName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 类型的限定名称。

返回值：

- [PackageInfo](./reflect_package_classes.md#class-packageinfo) - 类型的限定名称 `qualifiedName` 所对应的包信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获取与给定类型的限定名称 `qualifiedName` 所对应的类型信息，则抛出异常。

### static func load(String)

```cangjie
public static func load(path: String): PackageInfo
```

功能：运行时动态加载指定路径下的一个仓颉动态库模块并获得该模块的信息。

> **注意：**
>
> - 为了提升兼容性，路径 `path` 中的共享库文件名不需要后缀名（如 `.so` 和 `.dll` 等）。
> - 如果某个 `package` 通过静态加载方式（如：`import`）已经导入过，那么动态加载该 `package` 会抛出异常。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 共享库文件的绝对路径或相对路径。

返回值：

- [PackageInfo](reflect_package_classes.md#class-packageinfo) - 指定仓颉动态库的包信息。

异常：

- [ReflectException](reflect_package_exceptions.md#class-reflectexception) - 如果共享库加载失败，则会抛出异常。
- [ReflectException](reflect_package_exceptions.md#class-reflectexception) - 如果具有相同包名称或相同文件名的共享库被重复加载，则会抛出异常。
- [ReflectException](reflect_package_exceptions.md#class-reflectexception) - 如果动态库内部存在多个 Package，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当路径不合法时，抛出异常。

### func getFunction(String, Array\<TypeInfo>)

```cangjie
public func getFunction(name: String, parameterTypes: Array<TypeInfo>): GlobalFunctionInfo
```

功能：尝试在该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的包中获取拥有给定函数名称且与给定形参类型信息列表匹配的 `public` 全局函数的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 全局函数的名称。
- parameterTypes: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[TypeInfo](reflect_package_classes.md#class-typeinfo)> - 形参类型信息列表。

返回值：

- [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) - 如果成功匹配则返回该全局定义的 `public` 类型的函数信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应全局定义的 `public` 全局函数，则抛出异常。

### func getFunctions(String)

```cangjie
public func getFunctions(name: String): Array<GlobalFunctionInfo>
```

功能：尝试在该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的包中获取拥有给定函数名称的所有 `public` 全局函数的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 全局函数的名称。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo)> - 拥有给定函数名称的所有 `public` 全局函数的信息数组。

### func getSubPackage(String)

```cangjie
public func getSubPackage(qualifiedName: String): PackageInfo
```

功能：尝试获取该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应限定名称为 `qualifiedName` 的子包的信息。

参数：

- qualifiedName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 子包的限定名称。

返回值：

- [PackageInfo](reflect_package_classes.md#class-packageinfo) - 该子包的包信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果该子包不存在或者未加载，则会抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 `qualifiedName` 不符合规范，则抛出异常。

### func getTypeInfo(String)

```cangjie
public func getTypeInfo(qualifiedTypeName: String): TypeInfo
```

功能：尝试在该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的包中获取拥有给定类型名称的全局定义的 `public` 类型的类型信息。

参数：

- qualifiedTypeName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 类型的限定名称

返回值：

- [TypeInfo](reflect_package_classes.md#class-typeinfo) - 如果成功匹配则返回该全局定义的 `public` 类型的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应全局定义的 `public` 类型，则抛出异常。

### func getVariable(String)

```cangjie
public func getVariable(name: String): GlobalVariableInfo
```

功能：尝试在该 [PackageInfo](reflect_package_classes.md#class-packageinfo) 对应的包中获取拥有给定变量名称的 `public` 全局变量的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 全局变量的名称。

返回值：

- [GlobalVariableInfo](reflect_package_classes.md#class-globalvariableinfo) - 如果成功匹配则返回该全局定义的 `public` 类型的变量信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应全局定义的 `public` 全局变量，则抛出异常。

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该包信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该包信息的哈希值。

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该包信息。

> **注意：**
>
> 内部实现为该包信息的限定名称字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该包信息。

### operator func !=(PackageInfo)

```cangjie
public operator func !=(that: PackageInfo): Bool
```

功能：判断该包信息与给定的另一个包信息是否不等。

> **注意：**
>
> 内部实现为比较两个包信息的限定名称是否相等。

参数：

- that: [PackageInfo](reflect_package_classes.md#class-packageinfo) - 被比较相等性的另一个包信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该包信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(PackageInfo)

```cangjie
public operator func ==(that: PackageInfo): Bool
```

功能：判断该包信息与给定的另一个包信息是否相等。

> **注意：**
>
> 内部实现为比较两个包信息的限定名称是否相等。

参数：

- that: [PackageInfo](reflect_package_classes.md#class-packageinfo) - 被比较相等性的另一个包信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该包信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class ParameterInfo

```cangjie
public class ParameterInfo <: Equatable<ParameterInfo> & Hashable & ToString {}
```

功能：描述函数形参信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[ParameterInfo](#class-parameterinfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [ParameterInfo](reflect_package_classes.md#class-parameterinfo) 对应的函数形参的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该函数形参信息所对应的函数形参，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop index

```cangjie
public prop index: Int64
```

功能：获知该 [ParameterInfo](reflect_package_classes.md#class-parameterinfo) 对应的形参是其所在函数的第几个形参。

> **注意：**
>
> `index` 从 0 开始计数。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### prop name

```cangjie
public prop name: String
```

功能：获取该 [ParameterInfo](reflect_package_classes.md#class-parameterinfo) 对应的形参的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop typeInfo

```cangjie
public prop typeInfo: TypeInfo
```

功能：获取该 [ParameterInfo](reflect_package_classes.md#class-parameterinfo) 对应的函数形参的声明类型所对应的类型信息。

类型：[TypeInfo](reflect_package_classes.md#class-typeinfo)

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该函数形参信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该函数形参信息的哈希值。

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该函数形参信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该函数形参信息。

### operator func !=(ParameterInfo)

```cangjie
public operator func !=(that: ParameterInfo): Bool
```

功能：判断该函数形参信息与给定的另一个函数形参信息是否不等。

参数：

- that: [ParameterInfo](reflect_package_classes.md#class-parameterinfo) - 被比较相等性的另一个函数形参信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该函数形参信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(ParameterInfo)

```cangjie
public operator func ==(that: ParameterInfo): Bool
```

功能：判断该函数形参信息与给定的另一个函数形参信息是否相等。

参数：

- that: [ParameterInfo](reflect_package_classes.md#class-parameterinfo) - 被比较相等性的另一个函数形参信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该函数形参信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class PrimitiveTypeInfo

```cangjie
public class PrimitiveTypeInfo <: TypeInfo {}
```

功能：描述原始数据类型的类型信息。

原始数据类型包括无类型（`Nothing`）、单元类型（[Unit](../../core/core_package_api/core_package_intrinsics.md#unit)）、字符类型（[Rune](../../core/core_package_api/core_package_intrinsics.md#rune)）、布尔类型（[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)），整形类型（[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)，[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)，[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)，[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)，[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)，[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)，[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)，[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)，[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)，[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)）和浮点类型（[Float16](../../core/core_package_api/core_package_intrinsics.md#float16)，[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)，[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)）。

> **注意：**
>
> 目前尚不支持 `Nothing` 原始数据类型。

父类型：

- [TypeInfo](#class-typeinfo)

### static func get(String)

```cangjie
public static redef func get(qualifiedName: String): PrimitiveTypeInfo
```

功能：获取给定的类型的限定名称所对应类型的 [PrimitiveTypeInfo](reflect_package_classes.md#class-primitivetypeinfo)。

参数：

- qualifiedName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 类型的限定名称。

返回值：

- [PrimitiveTypeInfo](reflect_package_classes.md#class-primitivetypeinfo) - 类型的限定名称 `qualifiedName` 所对应的类型的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获取与给定类型的限定名称 `qualifiedName` 匹配的类型所对应的类型信息，则抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [PrimitiveTypeInfo](reflect_package_classes.md#class-primitivetypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

main(): Unit {
    var pti = PrimitiveTypeInfo.get("Int64")
    println(pti)
    return
}
```

运行结果：

```text
Int64
```

### static func of(Any)

```cangjie
public static redef func of(a: Any): PrimitiveTypeInfo
```

功能：获取给定的任意类型实例的运行时类型所对应的类型信息。

运行时类型是指在程序运行时，通过动态绑定确定的类型，运行时类型与实例对象相绑定。在继承等场景下运行时类型和静态类型可能不一致。

参数：

- a: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 任意类型的实例。

返回值：

- [PrimitiveTypeInfo](reflect_package_classes.md#class-primitivetypeinfo) - 实例 `a` 的运行时类型所对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得实例 `a` 的运行时类型所对应的类型信息，则抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [PrimitiveTypeInfo](reflect_package_classes.md#class-primitivetypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

main(): Unit {
    var a = 10
    var pti = PrimitiveTypeInfo.of(a)
    println(pti)
    return
}
```

运行结果：

```text
Int64
```

### static func of\<T>()

```cangjie
public static redef func of<T>(): PrimitiveTypeInfo
```

功能：获取给定 `T` 类型对应的类型信息。

返回值：

- [PrimitiveTypeInfo](reflect_package_classes.md#class-primitivetypeinfo) - `T` 类型对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得类型 T 所对应的类型信息，抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [PrimitiveTypeInfo](reflect_package_classes.md#class-primitivetypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

main(): Unit {
    var pti = PrimitiveTypeInfo.of<Int64>()
    println(pti)
    return
}
```

运行结果：

```text
Int64
```

## class StaticFunctionInfo

```cangjie
public class StaticFunctionInfo <: Equatable<StaticFunctionInfo> & Hashable & ToString {}
```

功能：描述静态成员函数信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[StaticFunctionInfo](#class-staticfunctioninfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) 对应的静态成员函数的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该 [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) 对应的静态成员函数，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop genericParams

```cangjie
public prop genericParams: Collection<GenericTypeInfo>
```

功能：获取该 [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) 对应的实例成员函数的泛型参数信息列表。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[GenericTypeInfo](reflect_package_classes.md#class-generictypeinfo)>

异常：

- [InfoNotFoundException](./reflect_package_exceptions.md#class-infonotfoundexception) - [GlobalFunctionInfo](reflect_package_classes.md#class-globalfunctioninfo) 没有泛型参数时抛出异常。

### prop modifiers

```cangjie
public prop modifiers: Collection<ModifierInfo>
```

功能：获取该 [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) 对应的静态成员函数所拥有的所有修饰符的信息，返回对应集合。

> **注意：**
>
> - 如果该静态成员函数无任何修饰符，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 即便未被某修饰符修饰，如果拥有该修饰符的语义，该修饰符信息也将被包括在该集合中。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ModifierInfo](reflect_package_enums.md#enum-modifierinfo)>

### prop name

```cangjie
public prop name: String
```

功能：获取该 [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) 对应的静态成员函数的名称。

> **注意：**
>
> 构成重载的所有静态成员函数将拥有相同的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop parameters

```cangjie
public prop parameters: ReadOnlyList<ParameterInfo>
```

功能：获取该 [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) 对应的静态成员函数的参数信息列表。

> **注意：**
>
> 不保证参数顺序，可根据 `ParameterInfo`的 `index` 属性确定参数实际位置。

类型：[ReadOnlyList](../../collection/collection_package_api/collection_package_interface.md#interface-readonlylistt)\<[ParameterInfo](reflect_package_classes.md#class-parameterinfo)>

### prop returnType

```cangjie
public prop returnType: TypeInfo
```

功能：获取该 [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) 对应的静态成员函数的返回值类型的类型信息。

类型：[TypeInfo](reflect_package_classes.md#class-typeinfo)

### func apply(TypeInfo, Array\<Any>)

```cangjie
public func apply(thisType: TypeInfo, args: Array<Any>): Any
```

功能：调用该 [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) 对应静态成员函数，传入方法所属的类型信息和实参列表并返回调用结果。

> **注意：**
>
> `args` 的类型确保和函数入参类型完全一致，否则会导致参数检查失败。

参数：

- thisType: [TypeInfo](./reflect_package_classes.md#class-typeinfo) - 该方法所属的类。
- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Any](../../core/core_package_api/core_package_interfaces.md#interface-any)> - 实参列表。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该静态成员函数的调用结果。

异常：

- [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) - 如果该函数信息对应的静态成员函数存在泛型参数，则会抛出异常。
- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果该函数信息对应的静态成员函数的函数体未实现，则会抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果实参列表 `args` 中的实参的数目与该静态成员函数信息所对应的静态成员函数的形参列表中的形参的数目不等，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 `thisType` 和该静态函数的函数签名不一致，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实参列表 `args` 中的任何一个实参的运行时类型不是该静态成员函数信息所对应的静态成员函数的对应形参的声明类型的子类型，则抛出异常。
- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 如果被调用的静态成员函数信息所对应的静态成员函数内部抛出异常，则该异常将被封装为 [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) 异常并抛出。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public static func myName(): String {
        "my name is Rectangular"
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取静态函数
    let sf = ty.getStaticFunction("myName")

    let result = sf.apply(ty) as String
    println(result)
    return
}
```

运行结果：

```text
Some(my name is Rectangular)
```

### func apply(TypeInfo, Array\<TypeInfo>, Array\<Any>)

```cangjie
public func apply(thisType: TypeInfo, genericTypeArgs: Array<TypeInfo>, args: Array<Any>): Any
```

功能：调用该 [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) 对应静态成员函数，传入方法所属的类型信息和实参列表并返回调用结果。

> **注意：**
>
> `args` 的类型确保和函数入参类型完全一致，否则会导致参数检查失败。

参数：

- thisType: [TypeInfo](./reflect_package_classes.md#class-typeinfo) - 该方法所属的类。
- genericTypeArgs: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[TypeInfo](./reflect_package_classes.md#class-typeinfo)> - 泛型参数类型列表。
- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Any](../../core/core_package_api/core_package_interfaces.md#interface-any)> - 实参列表。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该静态成员函数的调用结果。

异常：

- [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) -  如果该函数信息对应的静态成员函数是非泛型函数，则抛出异常。
- [InfoNotFoundException](../reflect_package_api/reflect_package_exceptions.md#class-infonotfoundexception) - 如果该函数信息对应的静态成员函数的函数体未实现，则会抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果实参列表 `args` 中的实参的数目与该静态成员函数信息所对应的静态成员函数的形参列表中的形参的数目不等，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果实参列表 `args` 中的泛型参数的数目与该静态成员函数信息所对应的泛型参数的数目不等，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 `thisType` 和该静态函数的函数签名不一致，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果实参列表 `args` 中的任何一个实参的运行时类型不是该静态成员函数信息所对应的静态成员函数的对应形参的声明类型的子类型，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果传入的参数列表 `args` 和泛型参数类型列表 `genericTypeArgs` 不满足该静态成员函数信息所对应的静态成员函数的参数的类型约束，则抛出异常。
- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) - 如果被调用的静态成员函数信息所对应的静态成员函数内部抛出异常，则该异常将被封装为 [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception) 异常并抛出。

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该静态成员函数信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该静态成员函数信息的哈希值。

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该静态成员函数信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该静态成员函数信息。

### operator func !=(StaticFunctionInfo)

```cangjie
public operator func !=(that: StaticFunctionInfo): Bool
```

功能：判断该静态成员函数信息与给定的另一个静态成员函数信息是否不等。

参数：

- that: [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) - 被比较相等性的另一个静态成员函数信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该静态成员函数信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(StaticFunctionInfo)

```cangjie
public operator func ==(that: StaticFunctionInfo): Bool
```

功能：判断该静态成员函数信息与给定的另一个静态成员函数信息是否相等。

参数：

- that: [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) - 被比较相等性的另一个静态成员函数信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该静态成员函数信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class StaticPropertyInfo

```cangjie
public class StaticPropertyInfo <: Equatable<StaticPropertyInfo> & Hashable & ToString {}
```

功能：描述静态成员属性信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[StaticPropertyInfo](#class-staticpropertyinfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo) 所对应的静态成员属性的注解所组成的集合。

> **注意：**
>
> - 如果无任何注解作用于该静态成员属性信息所对应的静态成员属性，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop modifiers

```cangjie
public prop modifiers: Collection<ModifierInfo>
```

功能：获取该 [StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo) 对应的静态成员属性所拥有的所有修饰符的信息，返回对应集合。

> **注意：**
>
> - 如果该静态成员属性无任何修饰符，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 目前获取到的修饰符集合内容较为混乱，尚未统一。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ModifierInfo](reflect_package_enums.md#enum-modifierinfo)>

### prop name

```cangjie
public prop name: String
```

功能：获取该 [StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo) 对应的静态成员属性的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop typeInfo

```cangjie
public prop typeInfo: TypeInfo
```

功能：获取该 [StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo) 对应的静态成员属性的声明类型的类型信息。

类型：[TypeInfo](reflect_package_classes.md#class-typeinfo)

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func getValue()

```cangjie
public func getValue(): Any
```

功能：获取该 [StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo) 对应的静态成员属性的值。

> **注意：**
>
> 如果该静态成员属性缺少合法实现，如 `interface` 类型中的抽象静态成员属性，则应抛出 [UnsupportedException](../../core/core_package_api/core_package_exceptions.md#class-unsupportedexception) 异常，但由于后端尚未支持，故尚未实现。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该静态成员属性的值。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public static prop sides: Int64 {
        get() { 4 }
    }
    public static prop angles: Int64 {
        get() { 4 }
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取静态属性
    let sp = ty.getStaticProperty("sides")

    let result = sp.getValue() as Int64
    println(result)
    return
}
```

运行结果：

```text
Some(4)
```

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该静态成员属性信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该静态成员属性信息的哈希值。

### func isMutable()

```cangjie
public func isMutable(): Bool
```

功能：判断该静态成员属性信息所对应的静态成员属性是否可修改。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该静态成员属性信息所对应的静态成员属性可被修改则返回 `true` ，否则返回 `false`。

> **注意：**
>
> 如果静态成员属性被 `mut` 修饰符所修饰，则该静态成员属性可被修改，否则不可被修改。

### func setValue(Any)

```cangjie
public func setValue(newValue: Any): Unit
```

功能：设置该 [StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo) 对应的静态成员属性的值。

> **注意：**
>
> 如果该静态成员属性缺少合法实现，如 `interface` 类型中的抽象静态成员属性，则应抛出 [UnsupportedException](../../core/core_package_api/core_package_exceptions.md#class-unsupportedexception) 异常，但由于后端尚未支持，故尚未实现。

参数：

- newValue: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 新值。

异常：

- [IllegalSetException](reflect_package_exceptions.md#class-illegalsetexception) - 如果该静态成员属性信息所对应的静态成员属性不可修改，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果新值 `newValue` 的运行时类型不是该静态成员属性信息所对应的静态成员属性的声明类型的子类型，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    private static var valueArea = 0
    public static mut prop area: Int64 {
        get() { valueArea }
        set(v) { valueArea = v }
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取静态属性
    let sp = ty.getStaticProperty("area")

    // 设置静态成员属性的值
    sp.setValue(10)
    let result = sp.getValue() as Int64
    println(result)
    return
}
```

运行结果：

```text
Some(10)
```

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该静态成员属性信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该静态成员属性信息。

### operator func !=(StaticPropertyInfo)

```cangjie
public operator func !=(that: StaticPropertyInfo): Bool
```

功能：判断该静态成员属性信息与给定的另一个静态成员属性信息是否不等。

参数：

- that: [StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo) - 被比较相等性的另一个静态成员属性信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该静态成员属性信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(StaticPropertyInfo)

```cangjie
public operator func ==(that: StaticPropertyInfo): Bool
```

功能：判断该静态成员属性信息与给定的另一个静态成员属性信息是否相等。

参数：

- that: [StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo) - 被比较相等性的另一个静态成员属性信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该静态成员属性信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class StaticVariableInfo

```cangjie
public class StaticVariableInfo <: Equatable<StaticVariableInfo> & Hashable & ToString {}
```

功能：描述静态成员变量信息。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[StaticVariableInfo](#class-staticvariableinfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) 对应的静态成员变量的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该 [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) 对应的静态成员变量，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop modifiers

```cangjie
public prop modifiers: Collection<ModifierInfo>
```

功能：获取该 [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) 对应的静态成员变量所拥有的所有修饰符的信息，返回对应集合。

> **注意：**
>
> - 如果该静态成员变量无任何修饰符，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 目前获取到的修饰符集合内容较为混乱，尚未统一。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ModifierInfo](reflect_package_enums.md#enum-modifierinfo)>

### prop name

```cangjie
public prop name: String
```

功能：获取该 [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) 对应的静态成员变量的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop typeInfo

```cangjie
public prop typeInfo: TypeInfo
```

功能：获取该 [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) 对应的静态成员变量的声明类型的类型信息。

类型：[TypeInfo](reflect_package_classes.md#class-typeinfo)

### func findAnnotation\<T>() where T <: Annotation

```cangjie
public func findAnnotation<T>(): Option<T> where T <: Annotation
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func getValue()

```cangjie
public func getValue(): Any
```

功能：获取该 [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) 对应的静态成员变量的值。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该静态成员变量的值。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public static var area: Int64 = 10
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取静态变量
    let sv = ty.getStaticVariable("area")
    // 获取值
    println(sv.getValue() as Int64)
    return
}
```

运行结果：

```text
Some(10)
```

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该静态成员变量信息的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该静态成员变量信息的哈希值。

### func isMutable()

```cangjie
public func isMutable(): Bool
```

功能：判断该 [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) 对应的静态成员变量是否可修改。

> **注意：**
>
> - 如果静态成员变量被 `var` 修饰符所修饰，则该静态成员变量可被修改。
> - 如果静态成员变量被 `let` 修饰符所修饰，则该静态成员变量不可被修改。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该静态成员变量信息所对应的静态成员变量可被修改则返回 `true` ，否则返回 `false`。

### func setValue(Any)

```cangjie
public func setValue(newValue: Any): Unit
```

功能：设置该 [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) 对应的静态成员变量的值。

参数：

- newValue: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 新值。

异常：

- [IllegalSetException](reflect_package_exceptions.md#class-illegalsetexception) - 如果该 [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) 对应的静态成员变量不可修改，则抛出异常。
- [IllegalTypeException](reflect_package_exceptions.md#class-illegaltypeexception) - 如果新值 `newValue` 的运行时类型不是该静态成员变量信息所对应的静态成员变量的声明类型的子类型，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public static var area: Int64 = 10
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取静态变量
    let sv = ty.getStaticVariable("area")

    // 设置值
    sv.setValue(20)
    println(sv.getValue() as Int64)
    return
}
```

运行结果：

```text
Some(20)
```

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该静态成员变量信息。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该静态成员变量信息。

### operator func !=(StaticVariableInfo)

```cangjie
public operator func !=(that: StaticVariableInfo): Bool
```

功能：判断该静态成员变量信息与给定的另一个静态成员变量信息是否不等。

参数：

- that: [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) - 被比较相等性的另一个静态成员变量信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该静态成员变量信息与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(StaticVariableInfo)

```cangjie
public operator func ==(that: StaticVariableInfo): Bool
```

功能：判断该静态成员变量信息与给定的另一个静态成员变量信息是否相等。

参数：

- that: [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) - 被比较相等性的另一个静态成员变量信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该静态成员变量信息与 `that` 相等则返回 `true`，否则返回 `false`。

## class StructTypeInfo

```cangjie
public class StructTypeInfo <: TypeInfo {}
```

功能：描述 `struct` 类型的类型信息。

父类型：

- [TypeInfo](#class-typeinfo)

由于实现限制，目前 `Struct` 类型的变量/属性修改需要参考如下代码手动 box/unbox。

```cangjie
import std.reflect.*

public struct SA {
    public var v1 = 11
}

main() {
    var sa = SA()
    let saObj: Any = sa
    StructTypeInfo.of<SA>().getInstanceVariable("v1").setValue(saObj, 22)
    sa = (saObj as SA).getOrThrow()
    println(sa.v1) // should be 22
}
```

### prop constructors

```cangjie
public prop constructors: Collection<ConstructorInfo>
```

功能：获取该 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) 对应的 `struct` 的所有 `public` 构造函数信息，返回对应集合。

> **注意：**
>
> - 如果该 `struct` 类型无任何 `public` 构造函数，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ConstructorInfo](reflect_package_classes.md#class-constructorinfo)>

### prop instanceVariables

```cangjie
public prop instanceVariables: Collection<InstanceVariableInfo>
```

功能：获取该 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) 对应的 `struct` 的所有 `public` 实例成员变量信息，返回对应集合。

> **注意：**
>
> - 如果该 `struct` 类型无任何 `public` 实例成员变量，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo)>

### prop staticVariables

```cangjie
public prop staticVariables: Collection<StaticVariableInfo>
```

功能：获取该 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) 对应的 `struct` 的所有 `public` 静态成员变量信息，返回对应集合。

> **注意：**
>
> - 如果该 `struct` 类型无任何 `public` 静态成员变量，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo)>

### static func get(String)

```cangjie
public static redef func get(qualifiedName: String): StructTypeInfo
```

功能：获取给定 `qualifiedName` 所对应的类型的 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo)。

参数：

- qualifiedName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 类型的限定名称。

返回值：

- [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) - 类型的限定名称 `qualifiedName` 所对应的 `Struct` 类型的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获取与给定类型的限定名称 `qualifiedName` 匹配的类型所对应的类型信息，则抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public struct Rectangular {}

main(): Unit {
    let ty = StructTypeInfo.get("default.Rectangular")
    println(ty)
    return
}
```

运行结果：

```text
default.Rectangular
```

### static func of(Any)

```cangjie
public static redef func of(a: Any): StructTypeInfo
```

功能：获取给定的任意类型实例的运行时类型所对应的类型信息。

运行时类型是指在程序运行时，通过动态绑定确定的类型，运行时类型与实例对象相绑定。在继承等场景下运行时类型和静态类型可能不一致。

参数：

- a: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 任意类型的实例。

返回值：

- [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) - 实例 `a` 的运行时类型所对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得实例 `a` 的运行时类型所对应的类型信息，则抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public struct Rectangular {}

main(): Unit {
    var r = Rectangular()
    let ty = StructTypeInfo.of(r)
    println(ty)
    return
}
```

运行结果：

```text
test.Rectangular
```

### static func of\<T>()

```cangjie
public static redef func of<T>(): StructTypeInfo
```

功能：获取给定 `T` 类型对应的类型信息。

返回值：

- [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) - `T` 类型对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得类型 T 所对应的类型信息，抛出异常。
- [IllegalTypeException](./reflect_package_exceptions.md#class-illegaltypeexception) - 如果获取到的类型信息不是 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo)， 则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public struct Rectangular {}

main(): Unit {
    let ty = StructTypeInfo.of<Rectangular>()
    println(ty)
    return
}
```

运行结果：

```text
default.Rectangular
```

### func construct(Array\<Any>)

```cangjie
public func construct(args: Array<Any>): Any
```

功能：在该 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) 对应的 `struct` 类型中根据实参列表搜索匹配的构造函数并调用，传入实参列表，返回调用结果。

参数：

- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Any](../../core/core_package_api/core_package_interfaces.md#interface-any)> - 实参列表。

返回值：

- [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 该 `struct` 类型的实例。

异常：

- [MisMatchException](reflect_package_exceptions.md#class-mismatchexception) - 如果 `args` 未能成功匹配任何该 `struct` 类型的 `public` 构造函数，则抛出异常
- [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) - 在被调用的构造函数内部抛出的任何异常均将被封装为 [InvocationTargetException](reflect_package_exceptions.md#class-invocationtargetexception) 异常并抛出。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public struct Rectangular {
    public var length = 4
    public var width = 5
    public init() {}
    public init(length: Int64, width: Int64) {
        this.length = length
        this.width = width
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 StructTypeInfo，也可以通过实例获取 StructTypeInfo
    let ty = StructTypeInfo.get("default.Rectangular")
    // 匹配构造函数并调用
    let v = ty.construct(2, 3) as Rectangular
    println(v.getOrThrow().length)
    return
}
```

运行结果：

```text
2
```

### func getConstructor(Array\<TypeInfo>)

```cangjie
public func getConstructor(parameterTypes: Array<TypeInfo>): ConstructorInfo
```

功能：尝试在该 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) 对应的 `struct` 类型中获取与给定形参类型信息列表匹配的 `public` 构造函数的信息。

参数：

- parameterTypes: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[TypeInfo](reflect_package_classes.md#class-typeinfo)> - 形参类型信息列表。

返回值：

- [ConstructorInfo](reflect_package_classes.md#class-constructorinfo) - 如果成功匹配则返回该 `public` 构造函数的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应 `public` 构造函数，则抛出异常。

### func getInstanceVariable(String)

```cangjie
public func getInstanceVariable(name: String): InstanceVariableInfo
```

功能：给定变量名称，尝试获取该 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) 对应的 `struct` 类型中匹配的实例成员变量的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 变量名称。

返回值：

- [InstanceVariableInfo](reflect_package_classes.md#class-instancevariableinfo) - 如果成功匹配则返回该实例成员变量的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应 `public` 实例成员变量，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
    public var myName = ""
    public init() {}
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 ClassTypeInfo，也可以通过实例获取 ClassTypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取结构实例成员变量信息
    let ivi = ty.getInstanceVariable("myName")
    println(ivi)
    return
}
```

运行结果：

```text
myName: String
```

### func getStaticVariable(String)

```cangjie
public func getStaticVariable(name: String): StaticVariableInfo
```

功能：给定变量名称，尝试获取该 [StructTypeInfo](reflect_package_classes.md#class-structtypeinfo) 对应的 `struct` 类型中匹配的静态成员变量的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 变量名称。

返回值：

- [StaticVariableInfo](reflect_package_classes.md#class-staticvariableinfo) - 如果成功匹配则返回该静态成员变量的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应 `public` 静态成员变量，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public struct Rectangular {
    public static var area: Int64 = 10
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 StructTypeInfo，也可以通过实例获取 StructTypeInfo
    let ty = StructTypeInfo.get("test.Rectangular")

    // 获取静态变量
    let sv = ty.getStaticVariable("area")
    println(sv)
    return
}
```

运行结果：

```text
static area: Int64
```

## class TypeInfo

```cangjie
sealed abstract class TypeInfo <: Equatable<TypeInfo> & Hashable & ToString
```

功能：[TypeInfo](reflect_package_classes.md#class-typeinfo) 提供了所有数据类型通用的操作接口。开发者通常无需向下转型为更具体的数据类型，如 [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 等，就能进行反射操作。

[TypeInfo](reflect_package_classes.md#class-typeinfo) 的子类包括 [PrimitiveTypeInfo](reflect_package_classes.md#class-primitivetypeinfo)、[StructTypeInfo](reflect_package_classes.md#class-structtypeinfo)、[ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) 和 [InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo)，分别对应基本数据类型，`struct` 数据类型，`class` 数据类型和 `interface` 数据类型的类型信息。

> **说明：**
>
> 类型的限定名称为`(module_name/)?(default|package_name)(.package_name)*.(type_name)`。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[TypeInfo](#class-typeinfo)>
- [Hashable](../../core/core_package_api/core_package_interfaces.md#interface-hashable)
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### prop annotations

```cangjie
public prop annotations: Collection<Annotation>
```

功能：获取所有作用于该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型的注解，返回对应集合。

> **注意：**
>
> - 如果无任何注解作用于该类型信息所对应的类型，则返回空集合。
> - 该集合不保证遍历顺序恒定。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[Annotation](../../ast/ast_package_api/ast_package_classes.md#class-annotation)>

### prop instanceFunctions

```cangjie
public prop instanceFunctions: Collection<InstanceFunctionInfo>
```

功能：获取该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应类型的所有 `public` 实例成员函数信息，返回对应集合。

> **注意：**
>
> - 如果该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型无任何 `public` 实例成员函数，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 如果该类型信息所对应的类型是 `struct` 或 `class` 类型，则该集合不包含继承而来的实例成员函数的信息。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo)>

### prop instanceProperties

```cangjie
public prop instanceProperties: Collection<InstancePropertyInfo>
```

功能：获取该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应类型的所有 `public` 实例成员属性信息，返回对应集合。

> **注意：**
>
> - 如果该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型无任何 `public` 实例成员属性，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 如果该类型信息所对应的类型是 `struct` 或 `class` 类型，则该集合不包含继承而来的实例成员属性的信息。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo)>

### prop modifiers

```cangjie
public prop modifiers: Collection<ModifierInfo>
```

功能：获取该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型拥有的所有修饰符的信息，返回对应集合。

> **注意：**
>
> - 如果该类型无任何修饰符，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - `interface` 类型默认拥有 `open` 语义，故返回的集合总是包含 `open` 修饰符。
> - 由于反射功能只能对所有被 `public` 访问控制修饰符所修饰的类型进行操作，故将忽略所有访问控制修饰符。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[ModifierInfo](reflect_package_enums.md#enum-modifierinfo)>

### prop name

```cangjie
public prop name: String
```

功能：获取该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型的名称。

> **注意：**
>
> - 该名称不包含任何模块名和包名前缀。
> - 类型别名的类型信息就是实际类型其本身的类型信息，所以该函数并不会返回类型别名本身的名称而是实际类型的名称，如类型别名 [Byte](../../core/core_package_api/core_package_types.md#type-byte) 的类型信息的名称是 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 而不是 [Byte](../../core/core_package_api/core_package_types.md#type-byte)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop qualifiedName

```cangjie
public prop qualifiedName: String
```

功能：获取该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型的限定名称。

> **注意：**
>
> - 限定名称包含模块名和包名前缀。
> - 特别的，仓颉内置数据类型，以及位于 `std` 模块 `core` 包下的所有类型的限定名称都是不带有任何模块名和包名前缀的。
> - 在缺省模块名和包名的上下文中定义的所有类型，均无模块名前缀，但拥有包名前缀"`default`"，如："`default.MyType`"。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop staticFunctions

```cangjie
public prop staticFunctions: Collection<StaticFunctionInfo>
```

功能：获取该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应类型的所有 `public` 静态成员函数信息，返回对应集合。

> **注意：**
>
> - 如果该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型无任何 `public` 静态成员函数，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 如果该类型信息所对应的类型是 `struct` 、`class` 或 `interface` 类型，则该集合不包含继承而来的静态成员函数的信息。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo)>

### prop staticProperties

```cangjie
public prop staticProperties: Collection<StaticPropertyInfo>
```

功能：获取该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应类型的所有 `public` 静态成员属性信息，返回对应集合。

> **注意：**
>
> - 如果该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型无任何 `public` 静态成员属性，则返回空集合。
> - 该集合不保证遍历顺序恒定。
> - 如果该类型信息所对应的类型是 `struct` 、`class` 或 `interface` 类型，则该集合不包含继承而来的静态成员属性的信息。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo)>

### prop superInterfaces

```cangjie
public prop superInterfaces: Collection<InterfaceTypeInfo>
```

功能：获取该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型直接实现的所有 `interface` 类型的信息，返回对应集合。

> **注意：**
>
> - 所有类型均默认直接实现 interface [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) 类型。
> - 该集合不保证遍历顺序恒定。
> - 目前， `struct` 类型只支持获取到 interface [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) 类型。

类型：[Collection](../../core/core_package_api/core_package_interfaces.md#interface-collectiont)\<[InterfaceTypeInfo](reflect_package_classes.md#class-interfacetypeinfo)>

### static func get(String)

```cangjie
public static func get(qualifiedName: String): TypeInfo
```

功能：获取给定 `qualifiedName` 所对应的类型的 [TypeInfo](reflect_package_classes.md#class-typeinfo)。

> **注意：**
>
> 目前， 类型的限定名称 `qualifiedName` 不支持 `Nothing` 类型、函数类型、元组类型和`enum` 类型的限定名称。

参数：

- qualifiedName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 类型的限定名称。

返回值：

- [TypeInfo](reflect_package_classes.md#class-typeinfo) - 类型的限定名称 `qualifiedName` 所对应的类型的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获取与给定类型的限定名称 `qualifiedName` 匹配的类型所对应的类型信息，则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {}

main(): Unit {
    let ty = TypeInfo.get("default.Rectangular")
    println(ty)
    return
}
```

运行结果：

```text
default.Rectangular
```

### static func of(Any)

```cangjie
public static func of(a: Any): TypeInfo
```

功能：获取给定的任意类型实例的运行时类型所对应的类型信息。

运行时类型是指在程序运行时，通过动态绑定确定的类型，运行时类型与实例对象相绑定。在继承等场景下运行时类型和静态类型可能不一致。

> **注意：**
>
> 目前，实例 `a` 不支持运行时类型为函数类型、元组类型、`enum` 类型。

参数：

- a: [Any](../../core/core_package_api/core_package_interfaces.md#interface-any) - 任意类型的实例。

返回值：

- [TypeInfo](reflect_package_classes.md#class-typeinfo) - 实例 `a` 的运行时类型所对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得实例 `a` 的运行时类型所对应的类型信息，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {}

main(): Unit {
    var r: Any = Rectangular()
    let ty = TypeInfo.of(r)
    println(ty)
    return
}
```

运行结果：

```text
test.Rectangular
```

### static func of(Object) <sup>(deprecated)</sup>

```cangjie
public static func of(a: Object): ClassTypeInfo
```

功能：获取给定的 `class` 类型的实例的运行时类型所对应的 `class` 类型信息。

> **注意：**
>
> 未来版本即将废弃，使用 [ClassTypeInfo](#class-classtypeinfo) 的 [static func of(Object)](#static-func-ofobject) 函数替代。

参数：

- a: [Object](../../core/core_package_api/core_package_classes.md#class-object) - `class` 类型的实例。

返回值：

- [ClassTypeInfo](reflect_package_classes.md#class-classtypeinfo) - `class` 类型的实例 `a` 的运行时类型所对应的 `class` 类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得实例 `a` 的运行时类型所对应的 `class` 类型信息，则抛出异常。

### static func of\<T>()

```cangjie
public static func of<T>(): TypeInfo
```

功能：获取给定 `T` 类型对应的类型信息。

> **注意：**
>
> - 目前，泛型 `T` 不支持 `Nothing` 类型、函数类型、元组类型和`enum` 类型。
> - `T` 支持传入类型别名，包括内置类型别名（如 [Int](../../core/core_package_api/core_package_types.md#type-int)、[UInt](../../core/core_package_api/core_package_types.md#type-uint) 和 `Rune` 等）与用户自定义类型别名。

返回值：

- [TypeInfo](reflect_package_classes.md#class-typeinfo) - `T` 类型对应的类型信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果无法获得类型 T 所对应的类型信息，抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {}

main(): Unit {
    let ty = TypeInfo.of<Rectangular>()
    println(ty)
    return
}
```

运行结果：

```text
default.Rectangular
```

### func findAnnotation\<T>()

```cangjie
public func findAnnotation<T>(): Option<T>
```

功能：尝试获取拥有给定限定名称且作用于该对象的注解。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 如果成功匹配则返回该注解，重复标注或者无法匹配时返回 `None`。

### func getInstanceFunction(String, Array\<TypeInfo>)

```cangjie
public func getInstanceFunction(name: String, parameterTypes: Array<TypeInfo>): InstanceFunctionInfo
```

功能：给定函数名称与函数形参类型列表所对应的类型信息列表，尝试获取该类型中匹配的实例成员函数的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 函数名称。
- parameterTypes: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[TypeInfo](reflect_package_classes.md#class-typeinfo)> - 函数形参类型列表所对应的类型信息列表。

返回值：

- [InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo) - 如果成功匹配则返回该实例成员函数的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应 `public` 实例成员函数，则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
    public func area(): Int64 {
        return length * width
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 TypeInfo，也可以通过实例获取 TypeInfo
    let ty = TypeInfo.get("default.Rectangular")
    // 获取 InstanceFunctionInfo
    var gif = ty.getInstanceFunction("area")

    println(gif)
    return
}
```

运行结果：

```text
func area(): Int64
```

### func getInstanceFunctions(String)

```cangjie
public func getInstanceFunctions(name: String): Array<InstanceFunctionInfo>
```

功能：给定函数名称，尝试获取该类型中所有匹配的实例成员函数的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 函数名称。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[InstanceFunctionInfo](reflect_package_classes.md#class-instancefunctioninfo)> - 如果成功匹配则返回所有匹配到的实例成员函数信息。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {
    public var length = 4
    public var width = 5
    public func area(): Int64 {
        return length * width
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 TypeInfo，也可以通过实例获取 TypeInfo
    let ty = TypeInfo.get("default.Rectangular")
    // 获取 InstanceFunctionInfo
    var gif = ty.getInstanceFunctions("area")

    println(gif)
    return
}
```

运行结果：

```text
[func area(): Int64]
```

### func getInstanceProperty(String)

```cangjie
public func getInstanceProperty(name: String): InstancePropertyInfo
```

功能：尝试获取该类型中与给定属性名称匹配的实例成员属性的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 属性名称。

返回值：

- [InstancePropertyInfo](reflect_package_classes.md#class-instancepropertyinfo) - 如果成功匹配则返回该实例成员属性的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应 `public` 实例成员属性，则抛出异常。

示例：

<!-- verify -->
```cangjie
import std.reflect.*

public class Rectangular {
    public var length = 4
    public prop width: Int64 {
        get() {
            5
        }
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 TypeInfo，也可以通过实例获取 TypeInfo
    let ty = TypeInfo.get("default.Rectangular")
    // 获取 InstancePropertyInfo
    var gip = ty.getInstanceProperty("width")

    println(gip)
    return
}
```

运行结果：

```text
prop width: Int64
```

### func getStaticFunction(String, Array\<TypeInfo>)

```cangjie
public func getStaticFunction(name: String, parameterTypes: Array<TypeInfo>): StaticFunctionInfo
```

功能：通过给定函数名称与函数形参类型列表所对应的类型信息列表，尝试获取该类型中匹配的静态成员函数的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 函数名称。
- parameterTypes: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[TypeInfo](reflect_package_classes.md#class-typeinfo)> - 函数形参类型列表所对应的类型信息列表。

返回值：

- [StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo) - 如果成功匹配则返回该静态成员函数的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应 `public` 静态成员函数，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public static func myName(): String { "" }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 TypeInfo，也可以通过实例获取 TypeInfo
    let ty = ClassTypeInfo.get("test.Rectangular")

    // 获取静态函数
    let sf = ty.getStaticFunction("myName")

    println(sf)
    return
}
```

运行结果：

```text
static func myName(): String
```

### func getStaticFunctions(String)

```cangjie
public func getStaticFunctions(name: String): Array<StaticFunctionInfo>
```

功能：给定函数名称，尝试获取该类型中所有匹配的静态成员函数的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 函数名称。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[StaticFunctionInfo](reflect_package_classes.md#class-staticfunctioninfo)> - 如果成功匹配则返回所有匹配到的静态成员函数信息。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    public static func myName(): String { "" }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 TypeInfo，也可以通过实例获取 TypeInfo
    let ty = TypeInfo.get("test.Rectangular")

    // 获取静态函数
    let sf = ty.getStaticFunctions("myName")

    println(sf)
    return
}
```

运行结果：

```text
[static func myName(): String]
```

### func getStaticProperty(String)

```cangjie
public func getStaticProperty(name: String): StaticPropertyInfo
```

功能：尝试获取该类型中与给定属性名称匹配的静态成员属性的信息。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 属性名称。

返回值：

- [StaticPropertyInfo](reflect_package_classes.md#class-staticpropertyinfo) - 如果成功匹配则返回该静态成员属性的信息。

异常：

- [InfoNotFoundException](reflect_package_exceptions.md#class-infonotfoundexception) - 如果没找到对应 `public` 静态成员属性，则抛出异常。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public class Rectangular {
    private static var valueArea = 0
    public static mut prop area: Int64 {
        get() { valueArea }
        set(v) { valueArea = v }
    }
}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 TypeInfo，也可以通过实例获取 TypeInfo
    let ty = TypeInfo.get("test.Rectangular")

    // 获取静态属性
    let sp = ty.getStaticProperty("area")

    println(sp)
    return
}
```

运行结果：

```text
static mut prop area: Int64
```

### func hashCode()

```cangjie
public func hashCode(): Int64
```

功能：获取该类型信息的哈希值。

> **注意：**
>
> 内部实现为该类型信息的限定名称字符串的哈希值。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 该类型信息的哈希值。

### func isSubtypeOf(TypeInfo)

```cangjie
public func isSubtypeOf(supertype: TypeInfo): Bool
```

功能：判断当前 [TypeInfo](reflect_package_classes.md#class-typeinfo) 实例对应的类型是否是参数中指定的 [TypeInfo](reflect_package_classes.md#class-typeinfo) 实例表示的类型的子类型。

参数：

- supertype: [TypeInfo](reflect_package_classes.md#class-typeinfo) - 目标类型的类型信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该 [TypeInfo](reflect_package_classes.md#class-typeinfo) 对应的类型是 `supertype` 所对应的类型的子类型则返回 `true`，否则返回 `false`。

示例：

<!-- verify -->
```cangjie
package test

import std.reflect.*

public abstract class Rectangular {}

public class Square <: Rectangular {}

main(): Unit {
    // 此处是通过 Rectangular 的类型的限定名称获取 TypeInfo，也可以通过实例获取 TypeInfo
    let tyr = ClassTypeInfo.get("test.Rectangular")
    let tys = ClassTypeInfo.get("test.Square")
    println(tys.isSubtypeOf(tyr))
    return
}
```

运行结果：

```text
true
```

### func toString()

```cangjie
public func toString(): String
```

功能：获取字符串形式的该类型信息。

> **注意：**
>
> 内部实现为该类型信息的限定名称字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的该类型信息。

### operator func !=(TypeInfo)

```cangjie
public operator func !=(that: TypeInfo): Bool
```

功能：判断该类型信息与给定的另一个类型信息是否不等。

参数：

- that: [TypeInfo](reflect_package_classes.md#class-typeinfo) - 被比较相等性的另一个类型信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该类型信息的限定名称与 `that` 不等则返回 `true`，否则返回 `false`。

### operator func ==(TypeInfo)

```cangjie
public operator func ==(that: TypeInfo): Bool
```

功能：判断该类型信息与给定的另一个类型信息是否相等。

参数：

- that: [TypeInfo](reflect_package_classes.md#class-typeinfo) - 被比较相等性的另一个类型信息。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果该类型信息的限定名称与 `that` 相等则返回 `true`，否则返回 `false`。
