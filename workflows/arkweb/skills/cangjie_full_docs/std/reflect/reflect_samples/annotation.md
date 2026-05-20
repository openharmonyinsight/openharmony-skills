# 注解的使用

通过反射获取实例上注解的值。

代码如下：
<!-- verify -->

```cangjie
import std.reflect.*

main() {
    let ti = TypeInfo.of(Test())
    let annotation = ti.findAnnotation<A>()
    if (let Some(a) <- annotation) {
        println(a.name)
    }
}

@A["Annotation"]
public class Test {}

@Annotation
public class A {
    const A(let name: String) {}
}
```

运行结果：

```text
Annotation
```
