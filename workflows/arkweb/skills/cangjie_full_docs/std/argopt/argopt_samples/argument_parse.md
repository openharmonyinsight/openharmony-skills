# 命令行参数解析

## 不带回调

示例：

<!-- run -->
```cangjie
import std.env.*
import std.argopt.*

main(args: Array<String>): Unit {
    let argSpecs = [
        Short(r'a', NoValue),
        Long("test1", RequiredValue),
        Full("test2", r'c', OptionalValue)
    ]
    try {
        var result = parseArguments(args, argSpecs)
        println("Got a: ${result.options.contains('a')}")
        println("Test1: ${result.options.get("test1")}")
        println("Test2: ${result.options.get("test2")}")
        println("c: ${result.options.get('c')}")
        println("NonOptions: ${result.nonOptions}")
    } catch (e: ArgumentParseException) {
        println("Usage: error")
        return
    }
}
```

运行结果：

```bash
$ cjc main.cj && ./main -a --test1 t1val
Got a: true
Test1: Some(t1val)
Test2: None
c: None
NonOptions: []

$ cjc main.cj && ./main -a --test1
Usage: error

$ cjc main.cj && ./main -a --test1 t1val --test2
Got a: true
Test1: Some(t1val)
Test2: Some()
c: None
NonOptions: []

$ cjc main.cj && ./main -a --test1 t1val --test2 t2val
Got a: true
Test1: Some(t1val)
Test2: Some()
c: None
NonOptions: [t2val]

$ cjc main.cj && ./main -a --test1 t1val -ct2val
Got a: true
Test1: Some(t1val)
Test2: None
c: Some(t2val)
NonOptions: []
```

### 带回调

示例：

<!-- run -->
```cangjie
import std.argopt.*

main(args: Array<String>): Unit {
    let argSpecs = [
        Short(r'a', NoValue) {_ => println("Got a")},
        Long("test1", RequiredValue) {v => println("Got test1: `${v}`")},
        Full("test2", r'c', OptionalValue) {v => println("Got test2: `${v}`")},
        NonOptions {v => println("Got NonOptions: ${v}")}
    ]
    try {
        parseArguments(args, argSpecs)
    } catch (e: ArgumentParseException) {
        println("Usage: xxxx")
    }
}
```

运行结果：

```bash
$ cjc main.cj && ./main -a --test1 t1val --test2 t2val
Got a
Got test1: `t1val`
Got test2: ``
Got NonOptions: [t2val]
```
