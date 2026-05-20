# 枚举

## enum OverflowStrategy

```cangjie
public enum OverflowStrategy <: Equatable<OverflowStrategy> & ToString {
    | Saturating
    | Throwing
    | Wrapping
}
```

功能：溢出策略枚举类，共包含 3 种溢出策略。[BigInt](math_numeric_package_structs.md#struct-bigint) 类型、[Decimal](math_numeric_package_structs.md#struct-decimal) 类型转换为整数类型时，允许指定不同的溢出处理策略。

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[OverflowStrategy](#enum-overflowstrategy)>
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### Saturating

```cangjie
Saturating
```

功能：出现溢出，当前值大于目标类型的 MAX 值，返回目标类型 MAX 值，当前值小于目标类型的 MIN 值，返回目标类型 MIN 值。

### Throwing

```cangjie
Throwing
```

功能：出现溢出，抛出异常。

### Wrapping

```cangjie
Wrapping
```

功能：出现溢出，高位截断。

### func toString()

```cangjie
public func toString(): String
```

功能：生成溢出策略名称字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 溢出策略名称字符串。

### operator func ==(OverflowStrategy)

```cangjie
public operator func ==(that: OverflowStrategy): Bool
```

功能：判等。

参数：

- that: [OverflowStrategy](#enum-overflowstrategy) - 被比较的溢出策略。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 溢出策略相同，返回 true；否则，返回 false。
