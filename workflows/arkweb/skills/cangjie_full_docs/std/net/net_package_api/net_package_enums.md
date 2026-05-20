# 枚举

## enum SocketNet

```cangjie
public enum SocketNet <: ToString & Equatable<SocketNet> {
    | TCP
    | UDP
    | UNIX
}
```

功能：传输层协议类型。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)
- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[SocketNet](#enum-socketnet)>

### TCP

```cangjie
TCP
```

功能：代表 TCP 协议。

### UDP

```cangjie
UDP
```

功能：代表 UDP 协议。

### UNIX

```cangjie
UNIX
```

功能：代表 UNIX 协议。

### func toString()

```cangjie
public func toString(): String
```

功能：将枚举值转换为字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 转换后的字符串。

### operator func !=(SocketNet)

```cangjie
public operator func !=(that: SocketNet): Bool
```

功能：判断两个 [SocketNet](net_package_enums.md#enum-socketnet) 是否不相等。

参数：

- that: [SocketNet](net_package_enums.md#enum-socketnet) - 传入的 [SocketNet](net_package_enums.md#enum-socketnet)。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果不相等，则返回 `true`；否则，返回 `false`。

### operator func ==(SocketNet)

```cangjie
public operator func ==(that: SocketNet): Bool
```

功能：判断两个 [SocketNet](net_package_enums.md#enum-socketnet) 是否相等。

参数：

- that: [SocketNet](net_package_enums.md#enum-socketnet) - 的 [SocketNet](net_package_enums.md#enum-socketnet)。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果相等，则返回 `true`；否则，返回 `false`。
