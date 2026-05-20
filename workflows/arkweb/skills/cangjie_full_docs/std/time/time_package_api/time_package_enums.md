# 枚举

## enum DayOfWeek

```cangjie
public enum DayOfWeek <: ToString & Equatable<DayOfWeek> {
    | Sunday
    | Monday
    | Tuesday
    | Wednesday
    | Thursday
    | Friday
    | Saturday
}
```

功能：[DayOfWeek](time_package_enums.md#enum-dayofweek) 表示一周中的某一天，提供了与 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型转换，相等性判别以及获取枚举值的字符串表示的功能。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)
- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[DayOfWeek](time_package_enums.md#enum-dayofweek)>

### Friday

```cangjie
Friday
```

功能：构造一个表示周五的 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

### Monday

```cangjie
Monday
```

功能：构造一个表示周一的 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

### Saturday

```cangjie
Saturday
```

功能：构造一个表示周六的 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

### Sunday

```cangjie
Sunday
```

功能：构造一个表示周日的 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

### Thursday

```cangjie
Thursday
```

功能：构造一个表示周四的 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

### Tuesday

```cangjie
Tuesday
```

功能：构造一个表示周二的 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

### Wednesday

```cangjie
Wednesday
```

功能：构造一个表示周三的 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

### static func of(Int64)

```cangjie
public static func of(dayOfWeek: Int64): DayOfWeek
```

功能：获取参数 `dayOfWeek` 对应的 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

参数：

- dayOfWeek: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 周几的整数表示，合法范围为 [0, 6]。其中，0 表示周日，1 至 6 表示周一至周六。

返回值：

- [DayOfWeek](time_package_enums.md#enum-dayofweek) - 参数 `dayOfWeek` 对应的 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当参数 `dayOfWeek` 不在 [0, 6] 范围内时，抛出异常。

### func toInteger()

```cangjie
public func toInteger(): Int64
```

功能：获取当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例的整数表示，周日表示为 0，周一至周六表示为 1 至 6。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例的整数表示。

### func toString()

```cangjie
public func toString(): String
```

功能：返回当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例的字符串表示，如 "Monday" 表示周一。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例的字符串表示。

### func value() <sup>(deprecated)</sup>

```cangjie
public func value(): Int64
```

功能：获取当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例的整数表示，周日表示为 0，周一至周六表示为 1 至 6。

> **注意：**
>
> 未来版本即将废弃，可使用 [toInteger()](#func-tointeger) 替代。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例的整数表示。

### operator func !=(DayOfWeek)

```cangjie
public operator func !=(r: DayOfWeek): Bool
```

功能：判断当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 和 `r` 是否不为一周中的同一天。

参数：

- r: [DayOfWeek](time_package_enums.md#enum-dayofweek) - [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - `true` 或 `false`。当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例不等于 `r` 时，返回 `true`；否则，返回 `false`。

### operator func +(Int64)

```cangjie
public operator func +(n: Int64): DayOfWeek
```

功能：计算基于当前实例 `n` 天之后（n 为正数时）的表示值。若 `n` 为负数，则表示当天之前。

参数：

- n: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 后多少天。

返回值：

- [DayOfWeek](time_package_enums.md#enum-dayofweek) - `n` 天后的周数值。

### operator func -(Int64)

```cangjie
public operator func -(n: Int64): DayOfWeek
```

功能：计算基于当前实例 `n` 天之前（n 为正数时）的表示值。若 `n` 为负数，则表示当天之后。

参数：

- n: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 前多少天。

返回值：

- [DayOfWeek](time_package_enums.md#enum-dayofweek) - `n` 天前的周数值。

### operator func ==(DayOfWeek)

```cangjie
public operator func ==(r: DayOfWeek): Bool
```

功能：判断当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 和 `r` 是否表示一周中的同一天。

参数：

- r: [DayOfWeek](time_package_enums.md#enum-dayofweek) - [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - `true` 或 `false`。当前 [DayOfWeek](time_package_enums.md#enum-dayofweek) 实例等于 `r` 时，返回 `true`；否则，返回 `false`。

## enum Month

```cangjie
public enum Month <: ToString & Equatable<Month> {
    | January
    | February
    | March
    | April
    | May
    | June
    | July
    | August
    | September
    | October
    | November
    | December
}
```

功能：[Month](time_package_enums.md#enum-month) 用以表示月份，表示一年中的某一月，提供了与 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型转换和计算，相等性判别以及获取枚举值的字符串表示的功能。

父类型：

- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)
- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[Month](time_package_enums.md#enum-month)>

### April

```cangjie
April
```

功能：构造一个表示四月的 [Month](time_package_enums.md#enum-month) 实例。

### August

```cangjie
August
```

功能：构造一个表示八月的 [Month](time_package_enums.md#enum-month) 实例。

### December

```cangjie
December
```

功能：构造一个表示十二月的 [Month](time_package_enums.md#enum-month) 实例。

### February

```cangjie
February
```

功能：构造一个表示二月的 [Month](time_package_enums.md#enum-month) 实例。

### January

```cangjie
January
```

功能：构造一个表示一月的 [Month](time_package_enums.md#enum-month) 实例。

### July

```cangjie
July
```

功能：构造一个表示七月的 [Month](time_package_enums.md#enum-month) 实例。

### June

```cangjie
June
```

功能：构造一个表示六月的 [Month](time_package_enums.md#enum-month) 实例。

### March

```cangjie
March
```

功能：构造一个表示三月的 [Month](time_package_enums.md#enum-month) 实例。

### May

```cangjie
May
```

功能：构造一个表示五月的 [Month](time_package_enums.md#enum-month) 实例。

### November

```cangjie
November
```

功能：构造一个表示十一月的 [Month](time_package_enums.md#enum-month) 实例。

### October

```cangjie
October
```

功能：构造一个表示十月的 [Month](time_package_enums.md#enum-month) 实例。

### September

```cangjie
September
```

功能：构造一个表示九月的 [Month](time_package_enums.md#enum-month) 实例。

### static func of(Int64)

```cangjie
public static func of(mon: Int64): Month
```

功能：获取参数 `mon` 对应 [Month](time_package_enums.md#enum-month) 类型实例。

参数：

- mon: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 整数形式的月，合法范围为 [1, 12]，分别表示一年中的十二个月。

返回值：

- [Month](time_package_enums.md#enum-month) - 参数 `mon` 对应的 [Month](time_package_enums.md#enum-month) 类型实例。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当参数 `mon` 不在 [1, 12] 范围内时，抛出异常。

### func toInteger()

```cangjie
public func toInteger(): Int64
```

功能：获取当前 [Month](time_package_enums.md#enum-month) 实例的整数表示，一月至十二月分别表示为 1 至 12。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前 [Month](time_package_enums.md#enum-month) 实例的整数表示。

### func toString()

```cangjie
public func toString(): String
```

功能：返回当前 [Month](time_package_enums.md#enum-month) 实例的字符串表示，如 "January" 表示一月。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 当前 [Month](time_package_enums.md#enum-month) 实例的字符串表示。

### func value() <sup>(deprecated)</sup>

```cangjie
public func value(): Int64
```

功能：获取当前 [Month](time_package_enums.md#enum-month) 实例的整数表示，一月至十二月分别表示为 1 至 12。

> **注意：**
>
> 未来版本即将废弃，可使用 [toInteger()](#func-tointeger-1) 替代。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前 [Month](time_package_enums.md#enum-month) 实例的整数表示。

### operator func !=(Month)

```cangjie
public operator func !=(r: Month): Bool
```

功能：判断当前 [Month](time_package_enums.md#enum-month) 实例和 `r` 是否不为同一个月。

参数：

- r: [Month](time_package_enums.md#enum-month) - [Month](time_package_enums.md#enum-month) 实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 当前 [Month](time_package_enums.md#enum-month) 实例是否不等于 `r`。

### operator func +(Int64)

```cangjie
public operator func +(n: Int64): Month
```

功能：计算基于当前日历月份 `n` 个月之后（n 为正数时）的日历月份。若 `n` 为负数，则表示当月之前。

参数：

- n: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 后多少月的数量。

返回值：

- [Month](time_package_enums.md#enum-month) - `n` 月后的月份。

### operator func -(Int64)

```cangjie
public operator func -(n: Int64): Month
```

功能：计算基于当前日历月份 `n` 个前之后（n 为正数时）的日历月份。若 `n` 为负数，则表示当月之后。

参数：

- n: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 前多少月的数量。

返回值：

- [Month](time_package_enums.md#enum-month) - `n` 月前的月份。

### operator func ==(Month)

```cangjie
public operator func ==(r: Month): Bool
```

功能：判断当前 [Month](time_package_enums.md#enum-month) 实例和 `r` 是否表示同一个月。

参数：

- r: [Month](time_package_enums.md#enum-month) - [Month](time_package_enums.md#enum-month) 实例。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - `true` 或 `false`。当前 [Month](time_package_enums.md#enum-month) 实例等于 `r` 时，返回 `true`；否则，返回 `false`。
