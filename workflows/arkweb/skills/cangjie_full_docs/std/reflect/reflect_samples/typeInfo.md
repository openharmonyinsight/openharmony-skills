# TypeInfo 的使用
<!-- verify -->

```cangjie
package Demo

import std.reflect.*

public class Foo {
    public let item = 0

    public func f() {}
}

main() {
    let a = Foo()
    let ty: TypeInfo = TypeInfo.of(a)
    println(ty.name)
    println(ty.qualifiedName)
    println(ty.instanceFunctions.size)
}
```

运行结果：

```text
Foo
Demo.Foo
1
```
