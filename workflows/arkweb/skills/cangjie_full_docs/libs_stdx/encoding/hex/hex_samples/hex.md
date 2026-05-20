# Byte 数组和 Hex 互转

示例：

<!-- verify -->
```cangjie
import stdx.encoding.hex.*

main(): Int64 {
    var arr: Array<Byte> = [65, 66, 94, 97]
    var str = toHexString(arr)
    print("${str},")
    var opArr: Option<Array<Byte>> = fromHexString(str)
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
41425e61,65,66,94,97,
```
