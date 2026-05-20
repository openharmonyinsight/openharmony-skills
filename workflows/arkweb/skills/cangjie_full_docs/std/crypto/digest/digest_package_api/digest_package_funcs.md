# 函数

## func digest\<T>(T, Array\<Byte>) where T <: Digest

```cangjie
public func digest<T>(algorithm: T, data: Array<Byte>): Array<Byte> where T <: Digest
```

功能：提供 digest 泛型函数，实现用指定的摘要算法进行摘要运算。

参数：

- algorithm: T - 具体的摘要算法。
- data: [Array](../../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../../core/core_package_api/core_package_types.md#type-byte)> - 待进行摘要运算的数据。

返回值：

- [Array](../../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../../core/core_package_api/core_package_types.md#type-byte)> - 摘要运算结果。

示例：

<!-- verify -->
```cangjie
import std.crypto.digest.*

main() {
    let data: Array<Byte> = [1, 2, 3, 4, 5]
    let mydigest = MyDigest()
    let digestBytes = digest<MyDigest>(mydigest, data)
    println(digestBytes)
}

// 自定义 Digest
class MyDigest <: Digest {
    public prop size: Int64 {
        get() { 0 }
    }
    public prop blockSize: Int64 {
        get() { 0 }
    }
    public prop algorithm: String {
        get() { "" }
    }
    public func write(buffer: Array<Byte>): Unit {
        println("buffer = ${buffer}")
    }
    public func finish(to!: Array<Byte>): Unit {
        println("to = ${to}")
    }
    public func finish(): Array<Byte> {
        [3, 2, 1]
    }
    public func reset(): Unit {}
}
```

运行结果：

```text
buffer = [1, 2, 3, 4, 5]
[3, 2, 1]
```

## func digest\<T>(T, InputStream) where T <: Digest

```cangjie
public func digest<T>(algorithm: T, input: InputStream): Array<Byte> where T <: Digest
```

功能：提供 digest 泛型函数，实现用指定的摘要算法对 InputStream 里的数据进行摘要运算。

参数：

- algorithm: T - 具体的摘要算法。
- input: [InputStream](../../../io/io_package_api/io_package_interfaces.md#interface-inputstream) - 待进行摘要运算的 InputStream。

返回值：

- [Array](../../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../../core/core_package_api/core_package_types.md#type-byte)> - 摘要运算结果。

示例：

<!-- verify -->

```cangjie
import std.crypto.digest.*
import std.io.*

main() {
    /* 将原始的字节数组 data 转换为一个输入流 BufferedInputStream */
    let data: Array<Byte> = [1, 2, 3, 4, 5]
    let byteBuffer = ByteBuffer(data)
    let bufferedInputStream = BufferedInputStream(byteBuffer)
    let mydigest = MyDigest()
    let digestBytes = digest<MyDigest>(mydigest, bufferedInputStream)
    println(digestBytes)
}

// 自定义 Digest
class MyDigest <: Digest {
    public prop size: Int64 {
        get() { 0 }
    }
    public prop blockSize: Int64 {
        get() { 2 }
    }
    public prop algorithm: String {
        get() { "" }
    }
    public func write(buffer: Array<Byte>): Unit {
        println("buffer = ${buffer}")
    }
    public func finish(to!: Array<Byte>): Unit {
        println("to = ${to}")
    }
    public func finish(): Array<Byte> {
        [3, 2, 1]
    }
    public func reset(): Unit {}
}
```

运行结果：

```text
buffer = [1, 2]
buffer = [3, 4]
buffer = [5]
[3, 2, 1]
```

## func digest\<T>(T, String) where T <: Digest <sup>(deprecated)</sup>

```cangjie
public func digest<T>(algorithm: T, data: String): Array<Byte> where T <: Digest
```

功能：提供 digest 泛型函数，实现用指定的摘要算法进行摘要运算。

> **注意：**
>
> 未来版本即将废弃不再使用，可使用 [digest\<T>(T, Array\<Byte>) where T <: Digest](./digest_package_funcs.md#func-digesttt-arraybyte-where-t--digest) 替代。

参数：

- algorithm: T - 具体的摘要算法。
- data: [String](../../../core/core_package_api/core_package_structs.md#struct-string) - 待进行摘要运算的数据。

返回值：

- [Array](../../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../../core/core_package_api/core_package_types.md#type-byte)> - 摘要运算结果。
