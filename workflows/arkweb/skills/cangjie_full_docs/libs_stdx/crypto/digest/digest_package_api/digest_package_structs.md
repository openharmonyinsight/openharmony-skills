# 结构体

## struct HashType

```cangjie
public struct HashType <: ToString & Equatable<HashType>
```

功能：此类为 Hash 算法类别结构体，[MD5](digest_package_classes.md#class-md5)、[SHA1](digest_package_classes.md#class-sha1)、[SHA224](digest_package_classes.md#class-sha224)、[SHA256](digest_package_classes.md#class-sha256)、[SHA384](digest_package_classes.md#class-sha384)、[SHA512](digest_package_classes.md#class-sha512) 均为常用摘要算法。

父类型：

- ToString
- Equatable\<[HashType](#struct-hashtype)>

### prop MD5

```cangjie
public static prop MD5: HashType
```

功能：返回 [MD5](digest_package_classes.md#class-md5) 类型。

类型：[HashType](digest_package_structs.md#struct-hashtype)

### prop SHA1

```cangjie
public static prop SHA1: HashType
```

功能：返回 [SHA1](digest_package_classes.md#class-sha1) 类型。

类型：[HashType](digest_package_structs.md#struct-hashtype)

### prop SHA224

```cangjie
public static prop SHA224: HashType
```

功能：返回 [SHA224](digest_package_classes.md#class-sha224) 类型。

类型：[HashType](digest_package_structs.md#struct-hashtype)

### prop SHA256

```cangjie
public static prop SHA256: HashType
```

功能：返回 [SHA256](digest_package_classes.md#class-sha256) 类型。

类型：[HashType](digest_package_structs.md#struct-hashtype)

### prop SHA384

```cangjie
public static prop SHA384: HashType
```

功能：返回 [SHA384](digest_package_classes.md#class-sha384) 类型。

类型：[HashType](digest_package_structs.md#struct-hashtype)

### prop SHA512

```cangjie
public static prop SHA512: HashType
```

功能：返回 [SHA512](digest_package_classes.md#class-sha512) 类型。

类型：[HashType](digest_package_structs.md#struct-hashtype)

### prop SM3

```cangjie
public static prop SM3: HashType
```

功能：返回 [SM3](digest_package_classes.md#class-sm3) 类型。

类型：[HashType](digest_package_structs.md#struct-hashtype)

### func toString()

```cangjie
public func toString(): String
```

功能：获取 Hash 算法名称。

返回值：

- String - Hash 算法名称。

### operator func ==(HashType)

```cangjie
public override operator func ==(other: HashType): Bool
```

功能：判断两 [HashType](digest_package_structs.md#struct-hashtype) 是否引用同一实例。

参数：

- other: [HashType](digest_package_structs.md#struct-hashtype) - 对比的 HashType。

返回值：

- Bool - 相同返回 `true`；否则，返回 `false`。

### operator func !=(HashType)

```cangjie
public override operator func !=(other: HashType): Bool
```

功能：判断两 [HashType](digest_package_structs.md#struct-hashtype) 是否引用不同实例。

参数：

- other: [HashType](digest_package_structs.md#struct-hashtype) - 对比的 HashType。

返回值：

- Bool - 不相同返回 `true`；否则，返回 `false`。