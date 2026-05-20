# std.crypto.digest

## 功能介绍

std.crypto.digest 包提供常用摘要算法的通用接口，包括 MD5、SHA1、SHA224、SHA256、SHA384、SHA512、HMAC、SM3 等。

## API 列表

### 函数

|                 函数名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [digest\<T>(T, Array\<Byte>) where T <: Digest](./digest_package_api/digest_package_funcs.md#func-digesttt-arraybyte-where-t--digest) | 提供 digest 泛型函数，实现用指定的摘要算法进行摘要运算。 |
| [digest\<T>(T, String) where T <: Digest <sup>(deprecated)</sup>](./digest_package_api/digest_package_funcs.md#func-digesttt-string-where-t--digest-deprecated) | 提供 digest 泛型函数，实现用指定的摘要算法进行摘要运算。 |
| [digest\<T>(T, InputStream) where T <: Digest](./digest_package_api/digest_package_funcs.md#func-digesttt-inputstream-where-t--digest) | 提供 digest 泛型函数，实现用指定的摘要算法对 InputStream 里的数据进行摘要运算。 |

### 接口

|                 接口名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [Digest](./digest_package_api/digest_package_interfaces.md#interface-digest) | 此接口是摘要算法的通用接口。 |
