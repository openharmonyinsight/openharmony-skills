# 枚举

## enum RoundingMode

```cangjie
public enum RoundingMode <: Equatable<RoundingMode> & ToString {
    | Ceiling
    | Down
    | Floor
    | HalfEven
    | HalfUp
    | Up
}
```

功能：舍入规则枚举类，共包含 6 种舍入规则。除包含 IEEE 754 浮点数规定约定的 5 种舍入规则外，提供使用较多的 “四舍五入” 舍入规则。

|十进制数|Up|Down|Ceiling|Floor|HalfUp|HalfEven|
|:----|:----:|:----:|:----:|:----:|:----:|:----:|
|7.5|8|7|8|7|8|8|
|4.5|5|4|5|4|5|4|
|-1.1|-2|-1|-1|-2|-1|-1|
|-4.5|-5|-4|-4|-5|-5|-4|
|-7.5|-8|-7|-7|-8|-8|-8|

父类型：

- [Equatable](../../core/core_package_api/core_package_interfaces.md#interface-equatablet)\<[RoundingMode](#enum-roundingmode)>
- [ToString](../../core/core_package_api/core_package_interfaces.md#interface-tostring)

### Ceiling

```cangjie
Ceiling
```

功能：向正无穷方向舍入。

### Down

```cangjie
Down
```

功能：向靠近零的方向舍入。

### Floor

```cangjie
Floor
```

功能：向负无穷方向舍入。

### HalfEven

```cangjie
HalfEven
```

功能：四舍六入五取偶，又称 “银行家舍入”。

### HalfUp

```cangjie
HalfUp
```

功能：四舍五入。

### Up

```cangjie
Up
```

功能：向远离零的方向舍入。

### func toString()

```cangjie
public func toString(): String
```

功能：生成舍入规则名称字符串。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 舍入规则名称字符串。

### operator func ==(RoundingMode)

```cangjie
public operator func ==(that: RoundingMode): Bool
```

功能：判等。

参数：

- that: [RoundingMode](#enum-roundingmode) - 被比较的舍入规则。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 若舍入规则相同，返回 true；否则，返回 false。
