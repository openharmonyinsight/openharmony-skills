# 成员信息的使用
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
    let a = Rectangular()
    let ty = TypeInfo.of(a)
    const zl = 3
    let members = ty.instanceVariables.toArray()
    println((members[0].getValue(a) as Int64).getOrThrow())
    println((members[1].getValue(a) as Int64).getOrThrow())
    members[0].setValue(a, zl)
    members[1].setValue(a, zl)
    println((members[0].getValue(a) as Int64).getOrThrow())
    println((members[1].getValue(a) as Int64).getOrThrow())
    println(a.area())
    let funcs = ty.instanceFunctions.toArray()
    if (funcs[0].returnType.name == "Int64") {
        println("The area of the square is ${zl ** 2}")
    }
    return
}
```

运行结果：

```text
4
5
3
3
9
The area of the square is 9
```
