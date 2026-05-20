# 枚举

## enum OpenMode

```cangjie
public enum OpenMode <: ToString & Equatable<OpenMode> {
    | Read
    | Write
    | Append
    | ReadWrite
}
```

功能：表示不同的文件打开模式。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)
- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[OpenMode](./fs_package_enums.md#enum-openmode)>

### Append

```cangjie
Append
```

功能：构造一个 [OpenMode](fs_package_enums.md#enum-openmode) 实例，指定以追加写入的方式打开文件。如果文件不存在，则将创建文件。

### Read

```cangjie
Read
```

功能：构造一个 [OpenMode](fs_package_enums.md#enum-openmode) 实例，指定以只读的方式打开文件。如果文件不存在，则将引发 [FSException](fs_package_exceptions.md#class-fsexception) 异常。

### ReadWrite

```cangjie
ReadWrite
```

功能：构造一个 [OpenMode](fs_package_enums.md#enum-openmode) 实例，指定以可读可写的方式打开文件。如果文件不存在，则将创建文件。

> **注意：**
>
> ReadWrite 模式不会使文件被截断为零字节大小。

### Write

```cangjie
Write
```

功能：构造一个 [OpenMode](fs_package_enums.md#enum-openmode) 实例，指定以只写的方式打开文件，即文件存在时会将该文件截断为零字节大小，文件不存在则将创建文件。

### func toString()

```cangjie
public func toString(): String
```

功能：文件打开模式的字符串表示。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件打开模式名称。

### operator func !=(OpenMode)

```cangjie
public operator func !=(that: OpenMode): Bool
```

功能：比较 [OpenMode](fs_package_enums.md#enum-openmode) 实例是否不等。

参数：

- that: [OpenMode](fs_package_enums.md#enum-openmode) - 待比较的 [OpenMode](fs_package_enums.md#enum-openmode) 实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果不相等，则返回 true，否则返回 false。

### operator func ==(OpenMode)

```cangjie
public operator func ==(that: OpenMode): Bool
```

功能：比较 [OpenMode](fs_package_enums.md#enum-openmode) 实例是否相等。

参数：

- that: [OpenMode](fs_package_enums.md#enum-openmode) - 待比较的 [OpenMode](fs_package_enums.md#enum-openmode) 实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果相等，则返回 true，否则返回 false。
