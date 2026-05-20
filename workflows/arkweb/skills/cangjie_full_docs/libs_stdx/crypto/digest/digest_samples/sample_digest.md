# digest 使用

## MD5 算法示例

### 调用 MD5 成员函数

示例：

<!-- verify -->
```cangjie
import stdx.crypto.digest.*
import std.convert.*
import std.crypto.digest.*
import stdx.encoding.hex.*

main() {
    var str: String = "helloworld"
    var md5Instance = MD5()
    md5Instance.write(str.toArray())
    var md: Array<Byte> = md5Instance.finish()
    var result: String = toHexString(md)
    println(result)
    return 0
}
```

运行结果：

```text
fc5e038d38a57032085441e7fe7010b0
```

## SHA1 算法示例

### 调用 SHA1 成员函数

示例：

<!-- verify -->
```cangjie
import stdx.crypto.digest.*
import std.convert.*
import std.crypto.digest.*
import stdx.encoding.hex.*

main() {
    var str: String = "helloworld"
    var sha1Instance = SHA1()
    sha1Instance.write(str.toArray())
    var md: Array<Byte> = sha1Instance.finish()
    var result: String = toHexString(md)
    println(result)
    return 0
}
```

运行结果：

```text
6adfb183a4a2c94a2f92dab5ade762a47889a5a1
```

## SHA224 算法示例

### 调用 SHA224 成员函数

示例：

<!-- verify -->
```cangjie
import stdx.crypto.digest.*
import std.convert.*
import std.crypto.digest.*
import stdx.encoding.hex.*

main() {
    var str: String = "helloworld"
    var sha224Instance = SHA224()
    sha224Instance.write(str.toArray())
    var md: Array<Byte> = sha224Instance.finish()
    var result: String = toHexString(md)
    println(result)
    return 0
}
```

运行结果：

```text
b033d770602994efa135c5248af300d81567ad5b59cec4bccbf15bcc
```

## SHA256 算法示例

### 调用 SHA256 成员函数

示例：

<!-- verify -->
```cangjie
import stdx.crypto.digest.*
import std.convert.*
import std.crypto.digest.*
import stdx.encoding.hex.*

main() {
    var str: String = "helloworld"
    var sha256Instance = SHA256()
    sha256Instance.write(str.toArray())
    var md: Array<Byte> = sha256Instance.finish()
    var result: String = toHexString(md)
    println(result)
    return 0
}
```

运行结果：

```text
936a185caaa266bb9cbe981e9e05cb78cd732b0b3280eb944412bb6f8f8f07af
```

## SHA384 算法示例

### 调用 SHA384 成员函数

示例：

<!-- verify -->
```cangjie
import stdx.crypto.digest.*
import std.convert.*
import std.crypto.digest.*
import stdx.encoding.hex.*

main() {
    var str: String = "helloworld"
    var sha384Instance = SHA384()
    sha384Instance.write(str.toArray())
    var md: Array<Byte> = sha384Instance.finish()
    var result: String = toHexString(md)
    println(result)
    return 0
}
```

运行结果：

```text
97982a5b1414b9078103a1c008c4e3526c27b41cdbcf80790560a40f2a9bf2ed4427ab1428789915ed4b3dc07c454bd9
```

## SHA512 算法示例

### 调用 SHA512 成员函数

示例：

<!-- verify -->
```cangjie
import stdx.crypto.digest.*
import std.convert.*
import std.crypto.digest.*
import stdx.encoding.hex.*

main() {
    var str: String = "helloworld"
    var sha512Instance = SHA512()
    sha512Instance.write(str.toArray())
    var md: Array<Byte> = sha512Instance.finish()
    var result: String = toHexString(md)
    println(result)
    return 0
}
```

运行结果：

```text
1594244d52f2d8c12b142bb61f47bc2eaf503d6d9ca8480cae9fcf112f66e4967dc5e8fa98285e36db8af1b8ffa8b84cb15e0fbcf836c3deb803c13f37659a60
```

## HMAC 算法示例

> **说明**
>
> 目前只支持 HMAC-SHA512。

### 调用 HMAC-SHA512 成员函数

示例：

<!-- verify -->
```cangjie
import stdx.crypto.digest.*
import stdx.encoding.hex.*

main() {
    var algorithm: HashType = HashType.SHA512
    var key: Array<UInt8> = "cangjie".toArray()
    var data1: Array<UInt8> = "123".toArray()
    var data2: Array<UInt8> = "456".toArray()
    var data3: Array<UInt8> = "789".toArray()
    var data4: Array<UInt8> = "123456789".toArray()
    var hmac = HMAC(key, algorithm)
    hmac.write(data1)
    hmac.write(data2)
    hmac.write(data3)
    var md1: Array<Byte> = hmac.finish()
    var result1: String = toHexString(md1)
    println(result1)

    hmac.reset()
    hmac.write(data4)
    var md2: Array<Byte> = hmac.finish()
    var result2: String = toHexString(md2)
    println(result2)
    println(HMAC.equal(md1, md2))
    return 0
}
```

运行结果：

```text
2bafeb53b60a119d38793a886c7744f5027d7eaa3702351e75e4ff9bf255e3ce296bf41f80adda2861e81bd8efc52219df821852d84a17fb625e3965ebf2fdd9
2bafeb53b60a119d38793a886c7744f5027d7eaa3702351e75e4ff9bf255e3ce296bf41f80adda2861e81bd8efc52219df821852d84a17fb625e3965ebf2fdd9
true
```

## SM3 算法示例

### 调用 SM3 成员函数

示例：

<!-- verify -->
```cangjie
import stdx.crypto.digest.*
import std.convert.*
import std.crypto.digest.*
import stdx.encoding.hex.*

main() {
    var str: String = "helloworld"
    var sm3Instance = SM3()
    sm3Instance.write(str.toArray())
    var md: Array<Byte> = sm3Instance.finish()
    var result: String = toHexString(md)
    println(result)
    return 0
}
```

运行结果：

```text
c70c5f73da4e8b8b73478af54241469566f6497e16c053a03a0170fa00078283
```
