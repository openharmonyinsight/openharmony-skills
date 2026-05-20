# Byte 数组和 Base64 互转

示例：

<!-- verify -->
```cangjie
import stdx.encoding.base64.*

main(): Int64 {
    var arr: Array<Byte> = [77, 97, 110]
    var str = toBase64String(arr)
    print("${str},")
    var opArr: Option<Array<Byte>> = fromBase64String(str)
    var arr2: Array<Byte> = match (opArr) {
        case Some(s) => s
        case None => Array<Byte>()
    }
    for (i in 0..arr2.size) {
        print("${arr2[i]},")
    }
    return 0
}
```

运行结果：

```text
TWFu,77,97,110,
```
