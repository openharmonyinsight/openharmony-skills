# 函数

## func fromBase64String(String)

```cangjie
public func fromBase64String(data: String): Option<Array<Byte>>
```

功能：此函数用于 Base64 编码的字符串的解码。

参数：

- data: String - 要解码的 Base64 编码的字符串。

返回值：

- Option\<Array\<Byte>> - 输入空字符串会返回 Option\<Array\<Byte>>.Some(Array\<Byte>())，解码失败会返回 Option\<Array\<Byte>>.None。

## func toBase64String(Array\<Byte>)

```cangjie
public func toBase64String(data: Array<Byte>): String
```

功能：此函数用于将 Byte 数组转换成 Base64 编码的字符串。

参数：

- data: Array\<Byte> - 要编码的 Byte 数组。

返回值：

- String - 返回编码后的字符串。
