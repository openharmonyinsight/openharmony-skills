# 接口

## interface CarryingOp\<T>

```cangjie
public interface CarryingOp<T> {
  func carryingAdd(y: T): (Bool, T)
  func carryingSub(y: T): (Bool, T)
  func carryingMul(y: T): (Bool, T)
  func carryingDiv(y: T): (Bool, T)
  func carryingMod(y: T): (Bool, T)
  func carryingInc(): (Bool, T)
  func carryingDec(): (Bool, T)
  func carryingNeg(): (Bool, T)
  func carryingShl(y: UInt64): (Bool, T)
  func carryingShr(y: UInt64): (Bool, T)
}
```

功能：提供返回整数运算是否发生了截断以及运算结果的接口。

### func carryingAdd(T)

```cangjie
func carryingAdd(y: T): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示加法运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

参数：

- y: T - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 加法运算是否发生截断以及运算的结果。

### func carryingDec()

```cangjie
func carryingDec(): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示自减运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 自减运算是否发生截断以及运算的结果。

### func carryingDiv(T)

```cangjie
func carryingDiv(y: T): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示除法运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

参数：

- y: T - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 除法运算是否发生截断以及运算的结果。

### func carryingInc()

```cangjie
func carryingInc(): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示自增运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 自增运算是否发生截断以及运算的结果。

### func carryingMod(T)

```cangjie
func carryingMod(y: T): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示取余运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

参数：

- y: T - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 取余运算是否发生截断以及运算的结果。

### func carryingMul(T)

```cangjie
func carryingMul(y: T): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示乘法运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

参数：

- y: T - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 乘法运算是否发生截断以及运算的结果。

### func carryingNeg()

```cangjie
func carryingNeg(): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示负号运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 负号运算是否发生截断以及运算的结果。

### func carryingShl(UInt64)

```cangjie
func carryingShl(y: UInt64): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示左移运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 左移运算是否发生截断以及运算的结果。

### func carryingShr(UInt64)

```cangjie
func carryingShr(y: UInt64): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示右移运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 右移运算是否发生截断以及运算的结果。

### func carryingSub(T)

```cangjie
func carryingSub(y: T): (Bool, T)
```

功能：返回一个元组，元组的第一个元素表示减法运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

参数：

- y: T - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), T) - 减法运算是否发生截断以及运算的结果。

### extend Int16 <: CarryingOp\<Int16>

```cangjie
extend Int16 <: CarryingOp<Int16>
```

功能：为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 实现 [CarryingOp](./overflow_package_interfaces.md#interface-carryingopt) 接口。

父类型：

- [CarryingOp](./overflow_package_interfaces.md#interface-carryingopt)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### func carryingAdd(Int16)

```cangjie
public func carryingAdd(y: Int16): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(Int16)

```cangjie
public func carryingDiv(y: Int16): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(Int16)

```cangjie
public func carryingMod(y: Int16): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(Int16)

```cangjie
public func carryingMul(y: Int16): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(Int16)

```cangjie
public func carryingSub(y: Int16): (Bool, Int16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int16](../../core/core_package_api/core_package_intrinsics.md#int16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

### extend Int32 <: CarryingOp\<Int32>

```cangjie
extend Int32 <: CarryingOp<Int32>
```

功能：为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 实现 [CarryingOp](#interface-carryingopt) 接口。

父类型：

- [CarryingOp](#interface-carryingopt)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### func carryingAdd(Int32)

```cangjie
public func carryingAdd(y: Int32): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(Int32)

```cangjie
public func carryingDiv(y: Int32): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(Int32)

```cangjie
public func carryingMod(y: Int32): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(Int32)

```cangjie
public func carryingMul(y: Int32): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(Int32)

```cangjie
public func carryingSub(y: Int32): (Bool, Int32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int32](../../core/core_package_api/core_package_intrinsics.md#int32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

### extend Int64 <: CarryingOp\<Int64> & CarryingPow

```cangjie
extend Int64 <: CarryingOp<Int64> & CarryingPow
```

功能：为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 实现 [CarryingOp](#interface-carryingopt) 接口和 [CarryingPow](#interface-carryingpow) 接口。

父类型：

- [CarryingOp](#interface-carryingopt)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>
- [CarryingPow](#interface-carryingpow)

#### func carryingAdd(Int64)

```cangjie
public func carryingAdd(y: Int64): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(Int64)

```cangjie
public func carryingDiv(y: Int64): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(Int64)

```cangjie
public func carryingMod(y: Int64): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(Int64)

```cangjie
public func carryingMul(y: Int64): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingPow(UInt64)

```cangjie
public func carryingPow(y: UInt64): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的幂运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(Int64)

```cangjie
public func carryingSub(y: Int64): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

### extend Int8 <: CarryingOp\<Int8>

```cangjie
extend Int8 <: CarryingOp<Int8>
```

功能：为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 实现 [CarryingOp](#interface-carryingopt) 接口。

父类型：

- [CarryingOp](#interface-carryingopt)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### func carryingAdd(Int8)

```cangjie
public func carryingAdd(y: Int8): (Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(Int8)

```cangjie
public func carryingDiv(y: Int8): (Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(Int8)

```cangjie
public func carryingMod(y: Int8): (Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(Int8)

```cangjie
public func carryingMul(y: Int8): (Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(Int8)

```cangjie
public func carryingSub(y: Int8):(Bool, Int8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int8](../../core/core_package_api/core_package_intrinsics.md#int8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

### extend IntNative <: CarryingOp\<IntNative>

```cangjie
extend IntNative <: CarryingOp<IntNative>
```

功能：为 [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) 实现 [CarryingOp](#interface-carryingopt) 接口。

父类型：

- [CarryingOp](#interface-carryingopt)\<[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)>

#### func carryingAdd(IntNative)

```cangjie
public func carryingAdd(y: IntNative): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(IntNative)

```cangjie
public func carryingDiv(y: IntNative): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(IntNative)

```cangjie
public func carryingMod(y: IntNative): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(IntNative)

```cangjie
public func carryingMul(y: IntNative): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(IntNative)

```cangjie
public func carryingSub(y: IntNative): (Bool, IntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

### extend UInt16 <: CarryingOp\<UInt16>

```cangjie
extend UInt16 <: CarryingOp<UInt16>
```

功能：为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 实现 [CarryingOp](#interface-carryingopt) 接口。

父类型：

- [CarryingOp](#interface-carryingopt)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### func carryingAdd(UInt16)

```cangjie
public func carryingAdd(y: UInt16): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(UInt16)

```cangjie
public func carryingDiv(y: UInt16): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(UInt16)

```cangjie
public func carryingMod(y: UInt16): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(UInt16)

```cangjie
public func carryingMul(y: UInt16): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(UInt16)

```cangjie
public func carryingSub(y: UInt16): (Bool, UInt16)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

### extend UInt32 <: CarryingOp\<UInt32>

```cangjie
extend UInt32 <: CarryingOp<UInt32>
```

功能：为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 实现 [CarryingOp](#interface-carryingopt) 接口。

父类型：

- [CarryingOp](#interface-carryingopt)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### func carryingAdd(UInt32)

```cangjie
public func carryingAdd(y: UInt32): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(UInt32)

```cangjie
public func carryingDiv(y: UInt32): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(UInt32)

```cangjie
public func carryingMod(y: UInt32): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(UInt32)

```cangjie
public func carryingMul(y: UInt32): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(UInt32)

```cangjie
public func carryingSub(y: UInt32): (Bool, UInt32)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

### extend UInt64 <: CarryingOp\<UInt64>

```cangjie
extend UInt64 <: CarryingOp<UInt64>
```

功能：为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 实现 [CarryingOp](#interface-carryingopt) 接口。

父类型：

- [CarryingOp](#interface-carryingopt)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### func carryingAdd(UInt64)

```cangjie
public func carryingAdd(y: UInt64): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(UInt64)

```cangjie
public func carryingDiv(y: UInt64): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(UInt64)

```cangjie
public func carryingMod(y: UInt64): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(UInt64)

```cangjie
public func carryingMul(y: UInt64): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(UInt64)

```cangjie
public func carryingSub(y: UInt64): (Bool, UInt64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

### extend UInt8 <: CarryingOp\<UInt8>

```cangjie
extend UInt8 <: CarryingOp<UInt8>
```

功能：为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 实现 [CarryingOp](#interface-carryingopt) 接口。

父类型：

- [CarryingOp](#interface-carryingopt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### func carryingAdd(UInt8)

```cangjie
public func carryingAdd(y: UInt8): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(UInt8)

```cangjie
public func carryingDiv(y: UInt8): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(UInt8)

```cangjie
public func carryingMod(y: UInt8): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(UInt8)

```cangjie
public func carryingMul(y: UInt8): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(UInt8)

```cangjie
public func carryingSub(y: UInt8): (Bool, UInt8)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

### extend UIntNative <: CarryingOp\<UIntNative>

```cangjie
extend UIntNative <: CarryingOp<UIntNative>
```

功能：为 [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) 实现 [CarryingOp](#interface-carryingopt) 接口。

父类型：

- [CarryingOp](#interface-carryingopt)\<[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)>

#### func carryingAdd(UIntNative)

```cangjie
public func carryingAdd(y: UIntNative): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的加法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 加数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDec()

```cangjie
public func carryingDec(): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自减运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingDiv(UIntNative)

```cangjie
public func carryingDiv(y: UIntNative): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的除法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingInc()

```cangjie
public func carryingInc(): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的自增运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMod(UIntNative)

```cangjie
public func carryingMod(y: UIntNative): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的取余运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingMul(UIntNative)

```cangjie
public func carryingMul(y: UIntNative): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的乘法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 乘数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingNeg()

```cangjie
public func carryingNeg(): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的负号运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShl(UInt64)

```cangjie
public func carryingShl(y: UInt64): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的左移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingShr(UInt64)

```cangjie
public func carryingShr(y: UInt64): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的右移运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

#### func carryingSub(UIntNative)

```cangjie
public func carryingSub(y: UIntNative): (Bool, UIntNative)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的减法运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 减数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

## interface CarryingPow

```cangjie
public interface CarryingPow {
  func carryingPow(y: UInt64): (Bool, Int64)
}
```

功能：提供使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的幂运算接口。

### func carryingPow(UInt64)

```cangjie
func carryingPow(y: UInt64): (Bool, Int64)
```

功能：使用 [wrapping](./overflow_package_interfaces.md#interface-wrappingopt) 策略的幂运算。

当运算出现溢出时，返回 `true` 和运算结果，否则返回 `false` 和运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- ([Bool](../../core/core_package_api/core_package_intrinsics.md#bool), [Int64](../../core/core_package_api/core_package_intrinsics.md#int64)) - 返回一个元组，元组的第一个元素表示运算是否发生了截断，发生截断时为 `true`，元组的第二个元素是运算的结果。

## interface CheckedOp\<T>

```cangjie
public interface CheckedOp<T> {
    func checkedAdd(y: T): ?T
    func checkedDec(): ?T
    func checkedDiv(y: T): ?T
    func checkedInc(): ?T
    func checkedMod(y: T): ?T
    func checkedMul(y: T): ?T
    func checkedNeg(): ?T
    func checkedShl(y: UInt64): ?T
    func checkedShr(y: UInt64): ?T
    func checkedSub(y: T): ?T
}
```

功能：当整数运算出现溢出，返回 `None`。

### func checkedAdd(T)

```cangjie
func checkedAdd(y: T): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 `?T.None`，否则返回运算结果。

参数：

- y: T - 加数。

返回值：

- ?T - 加法运算结果。

### func checkedDec()

```cangjie
func checkedDec(): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 `?T.None`，否则返回运算结果。

返回值：

- ?T - 自减运算结果。

### func checkedDiv(T)

```cangjie
func checkedDiv(y: T): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 `?T.None`，否则返回运算结果。

参数：

- y: T - 除数。

返回值：

- ?T - 除法运算结果。

### func checkedInc()

```cangjie
func checkedInc(): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 `?T.None`，否则返回运算结果。

返回值：

- ?T - 自增运算结果。

### func checkedMod(T)

```cangjie
func checkedMod(y: T): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 `?T.None`，否则返回运算结果。

参数：

- y: T - 除数。

返回值：

- ?T - 取余运算结果。

### func checkedMul(T)

```cangjie
func checkedMul(y: T): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 `?T.None`，否则返回运算结果。

参数：

- y: T - 乘数。

返回值：

- ?T - 乘法运算结果。

### func checkedNeg()

```cangjie
func checkedNeg(): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 `?T.None`，否则返回运算结果。

返回值：

- ?T - 负号运算结果。

### func checkedShl(UInt64)

```cangjie
func checkedShl(y: UInt64): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 `?T.None`，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?T - 左移运算结果。

### func checkedShr(UInt64)

```cangjie
func checkedShr(y: UInt64): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 `?T.None`，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?T - 右移运算结果。

### func checkedSub(T)

```cangjie
func checkedSub(y: T): ?T
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 `?T.None`，否则返回运算结果。

参数：

- y: T - 减数。

返回值：

- ?T - 减法运算结果。

### extend Int16 <: CheckedOp\<Int16>

```cangjie
extend Int16 <: CheckedOp<Int16>
```

功能：为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 实现 [CheckedOp](#interface-checkedopt) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### func checkedAdd(Int16)

```cangjie
public func checkedAdd(y: Int16): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 加数。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 自减运算结果。

#### func checkedDiv(Int16)

```cangjie
public func checkedDiv(y: Int16): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 自增运算结果。

#### func checkedMod(Int16)

```cangjie
public func checkedMod(y: Int16): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 取余运算结果。

#### func checkedMul(Int16)

```cangjie
public func checkedMul(y: Int16): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 乘数。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 负号运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 右移运算结果。

#### func checkedSub(Int16)

```cangjie
public func checkedSub(y: Int16): ?Int16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16).None，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 减数。

返回值：

- ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 减法运算结果。

### extend Int32 <: CheckedOp\<Int32>

```cangjie
extend Int32 <: CheckedOp<Int32>
```

功能：为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 实现 [CheckedOp](#interface-checkedopt) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### func checkedAdd(Int32)

```cangjie
public func checkedAdd(y: Int32): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 加数。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 自减运算结果。

#### func checkedDiv(Int32)

```cangjie
public func checkedDiv(y: Int32): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 自增运算结果。

#### func checkedMod(Int32)

```cangjie
public func checkedMod(y: Int32): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 取余运算结果。

#### func checkedMul(Int32)

```cangjie
public func checkedMul(y: Int32): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 乘数。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 负号运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 右移运算结果。

#### func checkedSub(Int32)

```cangjie
public func checkedSub(y: Int32): ?Int32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32).None，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 减数。

返回值：

- ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 减法运算结果。

### extend Int64 <: CheckedOp\<Int64> & CheckedPow

```cangjie
extend Int64 <: CheckedOp<Int64> & CheckedPow
```

功能：为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 实现 [CheckedOp](#interface-checkedopt) 和 [CheckedPow](#interface-checkedpow) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>
- [CheckedPow](#interface-checkedpow)

#### func checkedAdd(Int64)

```cangjie
public func checkedAdd(y: Int64): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 加数。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 自减运算结果。

#### func checkedDiv(Int64)

```cangjie
public func checkedDiv(y: Int64): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 自增运算结果。

#### func checkedMod(Int64)

```cangjie
public func checkedMod(y: Int64): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 取余运算结果。

#### func checkedMul(Int64)

```cangjie
public func checkedMul(y: Int64): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 乘数。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 负号运算结果。

#### func checkedPow(UInt64)

```cangjie
public func checkedPow(y: UInt64): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的幂运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 幂运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 右移运算结果。

#### func checkedSub(Int64)

```cangjie
public func checkedSub(y: Int64): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 减数。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 减法运算结果。

### extend Int8 <: CheckedOp\<Int8>

```cangjie
extend Int8 <: CheckedOp<Int8>
```

功能：为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 实现 [CheckedOp](#interface-checkedopt) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### func checkedAdd(Int8)

```cangjie
public func checkedAdd(y: Int8): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 加数。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 自减运算结果。

#### func checkedDiv(Int8)

```cangjie
public func checkedDiv(y: Int8): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 自增运算结果。

#### func checkedMod(Int8)

```cangjie
public func checkedMod(y: Int8): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 取余运算结果。

#### func checkedMul(Int8)

```cangjie
public func checkedMul(y: Int8): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 乘数。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 负号运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 右移运算结果。

#### func checkedSub(Int8)

```cangjie
public func checkedSub(y: Int8): ?Int8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8).None，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 减数。

返回值：

- ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 减法运算结果。

### extend IntNative <: CheckedOp\<IntNative>

```cangjie
extend IntNative <: CheckedOp<IntNative>
```

功能：为 [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) 实现 [CheckedOp](#interface-checkedopt) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)>

#### func checkedAdd(IntNative)

```cangjie
public func checkedAdd(y: IntNative): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 加数。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 自减运算结果。

#### func checkedDiv(IntNative)

```cangjie
public func checkedDiv(y: IntNative): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 自增运算结果。

#### func checkedMod(IntNative)

```cangjie
public func checkedMod(y: IntNative): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 取余运算结果。

#### func checkedMul(IntNative)

```cangjie
public func checkedMul(y: IntNative): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 乘数。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 负号运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 右移运算结果。

#### func checkedSub(IntNative)

```cangjie
public func checkedSub(y: IntNative): ?IntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative).None，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 减数。

返回值：

- ?[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 减法运算结果。

### extend UInt16 <: CheckedOp\<UInt16>

```cangjie
extend UInt16 <: CheckedOp<UInt16>
```

功能：为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 实现 [CheckedOp](#interface-checkedopt) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### func checkedAdd(UInt16)

```cangjie
public func checkedAdd(y: UInt16): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 加数。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 自减运算结果。

#### func checkedDiv(UInt16)

```cangjie
public func checkedDiv(y: UInt16): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 自增运算结果。

#### func checkedMod(UInt16)

```cangjie
public func checkedMod(y: UInt16): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 取余运算结果。

#### func checkedMul(UInt16)

```cangjie
public func checkedMul(y: UInt16): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 乘数。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 负号运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 右移运算结果。

#### func checkedSub(UInt16)

```cangjie
public func checkedSub(y: UInt16): ?UInt16
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16).None，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 减数。

返回值：

- ?[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 减法运算结果。

### extend UInt32 <: CheckedOp\<UInt32>

```cangjie
extend UInt32 <: CheckedOp<UInt32>
```

功能：为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 实现 [CheckedOp](#interface-checkedopt) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### func checkedAdd(UInt32)

```cangjie
public func checkedAdd(y: UInt32): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 加数。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 自减运算结果。

#### func checkedDiv(UInt32)

```cangjie
public func checkedDiv(y: UInt32): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 自增运算结果。

#### func checkedMod(UInt32)

```cangjie
public func checkedMod(y: UInt32): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 取余运算结果。

#### func checkedMul(UInt32)

```cangjie
public func checkedMul(y: UInt32): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 乘数。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 负号运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 右移运算结果。

#### func checkedSub(UInt32)

```cangjie
public func checkedSub(y: UInt32): ?UInt32
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32).None，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 减数。

返回值：

- ?[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 减法运算结果。

### extend UInt64 <: CheckedOp\<UInt64>

```cangjie
extend UInt64 <: CheckedOp<UInt64>
```

功能：为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 实现 [CheckedOp](#interface-checkedopt) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### func checkedAdd(UInt64)

```cangjie
public func checkedAdd(y: UInt64): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 加数。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 自减运算结果。

#### func checkedDiv(UInt64)

```cangjie
public func checkedDiv(y: UInt64): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 自增运算结果。

#### func checkedMod(UInt64)

```cangjie
public func checkedMod(y: UInt64): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 取余运算结果。

#### func checkedMul(UInt64)

```cangjie
public func checkedMul(y: UInt64): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 乘数。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 负号运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 右移运算结果。

#### func checkedSub(UInt64)

```cangjie
public func checkedSub(y: UInt64): ?UInt64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 减数。

返回值：

- ?[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 减法运算结果。

### extend UInt8 <: CheckedOp\<UInt8>

```cangjie
extend UInt8 <: CheckedOp<UInt8>
```

功能：为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 实现 [CheckedOp](#interface-checkedopt) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### func checkedAdd(UInt8)

```cangjie
public func checkedAdd(y: UInt8): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 加数。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 自减运算结果。

#### func checkedDiv(UInt8)

```cangjie
public func checkedDiv(y: UInt8): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 自增运算结果。

#### func checkedMod(UInt8)

```cangjie
public func checkedMod(y: UInt8): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 取余运算结果。

#### func checkedMul(UInt8)

```cangjie
public func checkedMul(y: UInt8): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 乘数。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 负号运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 右移运算结果。

#### func checkedSub(UInt8)

```cangjie
public func checkedSub(y: UInt8): ?UInt8
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8).None，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 减数。

返回值：

- ?[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 减法运算结果。

### extend UIntNative <: CheckedOp\<UIntNative>

```cangjie
extend UIntNative <: CheckedOp<UIntNative>
```

功能：为 [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) 实现 [CheckedOp](#interface-checkedopt) 接口。

父类型：

- [CheckedOp](#interface-checkedopt)\<[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)>

#### func checkedAdd(UIntNative)

```cangjie
public func checkedAdd(y: UIntNative): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的加法运算。

当运算出现溢出时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 加数。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 加法运算结果。

#### func checkedDec()

```cangjie
public func checkedDec(): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自减运算。

当运算出现溢出时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 自减运算结果。

#### func checkedDiv(UIntNative)

```cangjie
public func checkedDiv(y: UIntNative): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的除法运算。

当运算出现溢出时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除法运算结果。

#### func checkedInc()

```cangjie
public func checkedInc(): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的自增运算。

当运算出现溢出时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 自增运算结果。

#### func checkedMod(UIntNative)

```cangjie
public func checkedMod(y: UIntNative): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的取余运算。

当运算出现溢出时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 取余运算结果。

#### func checkedMul(UIntNative)

```cangjie
public func checkedMul(y: UIntNative): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的乘法运算。

当运算出现溢出时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 乘数。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 乘法运算结果。

#### func checkedNeg()

```cangjie
public func checkedNeg(): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的负号运算。

当运算出现溢出时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 负号运算结果。

#### func checkedShl(UInt64)

```cangjie
public func checkedShl(y: UInt64): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的左移运算。

当移位位数大于等于操作数位数时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 左移运算结果。

#### func checkedShr(UInt64)

```cangjie
public func checkedShr(y: UInt64): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的右移运算。

当移位位数大于等于操作数位数时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 右移运算结果。

#### func checkedSub(UIntNative)

```cangjie
public func checkedSub(y: UIntNative): ?UIntNative
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的减法运算。

当运算出现溢出时，返回 ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative).None，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 减数。

返回值：

- ?[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 减法运算结果。

## interface CheckedPow

```cangjie
public interface CheckedPow {
    func checkedPow(y: UInt64): ?Int64
}
```

功能：提供返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的幂运算接口。

### func checkedPow(UInt64)

```cangjie
func checkedPow(y: UInt64): ?Int64
```

功能：使用返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 策略的幂运算。

当运算出现溢出时，返回 ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64).None，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 幂运算结果。

## interface SaturatingOp\<T>

```cangjie
public interface SaturatingOp<T> {
    func saturatingAdd(y: T): T
    func saturatingDec(): T
    func saturatingDiv(y: T): T
    func saturatingInc(): T
    func saturatingMod(y: T): T
    func saturatingMul(y: T): T
    func saturatingNeg(): T
    func saturatingShl(y: UInt64): T
    func saturatingShr(y: UInt64): T
    func saturatingSub(y: T): T
}
```

功能：当整数运算出现溢出，饱和处理。

### func saturatingAdd(T)

```cangjie
func saturatingAdd(y: T): T
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: T - 加数。

返回值：

- T - 加法运算结果。

### func saturatingDec()

```cangjie
func saturatingDec(): T
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- T - 自减运算结果。

### func saturatingDiv(T)

```cangjie
func saturatingDiv(y: T): T
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: T - 除数。

返回值：

- T - 除法运算结果。

### func saturatingInc()

```cangjie
func saturatingInc(): T
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- T - 自增运算结果。

### func saturatingMod(T)

```cangjie
func saturatingMod(y: T): T
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: T - 除数。

返回值：

- T - 取余运算结果。

### func saturatingMul(T)

```cangjie
func saturatingMul(y: T): T
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: T - 乘数。

返回值：

- T - 乘法运算结果。

### func saturatingNeg()

```cangjie
func saturatingNeg(): T
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- T - 负号运算结果。

### func saturatingShl(UInt64)

```cangjie
func saturatingShl(y: UInt64): T
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- T - 左移运算结果。

### func saturatingShr(UInt64)

```cangjie
func saturatingShr(y: UInt64): T
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- T - 右移运算结果。

### func saturatingSub(T)

```cangjie
func saturatingSub(y: T): T
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: T - 减数。

返回值：

- T - 减法运算结果。

### extend Int16 <: SaturatingOp\<Int16>

```cangjie
extend Int16 <: SaturatingOp<Int16>
```

功能：为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 实现 [SaturatingOp](#interface-saturatingopt) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### func saturatingAdd(Int16)

```cangjie
public func saturatingAdd(y: Int16): Int16
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 加数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): Int16
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 自减运算结果。

#### func saturatingDiv(Int16)

```cangjie
public func saturatingDiv(y: Int16): Int16
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): Int16
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 自增运算结果。

#### func saturatingMod(Int16)

```cangjie
public func saturatingMod(y: Int16): Int16
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 取余运算结果。

#### func saturatingMul(Int16)

```cangjie
public func saturatingMul(y: Int16): Int16
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 乘数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): Int16
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 负号运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): Int16
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): Int16
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 右移运算结果。

#### func saturatingSub(Int16)

```cangjie
public func saturatingSub(y: Int16): Int16
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 减数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 减法运算结果。

### extend Int32 <: SaturatingOp\<Int32>

```cangjie
extend Int32 <: SaturatingOp<Int32>
```

功能：为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 实现 [SaturatingOp](#interface-saturatingopt) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### func saturatingAdd(Int32)

```cangjie
public func saturatingAdd(y: Int32): Int32
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 加数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): Int32
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 自减运算结果。

#### func saturatingDiv(Int32)

```cangjie
public func saturatingDiv(y: Int32): Int32
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): Int32
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 自增运算结果。

#### func saturatingMod(Int32)

```cangjie
public func saturatingMod(y: Int32): Int32
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 取余运算结果。

#### func saturatingMul(Int32)

```cangjie
public func saturatingMul(y: Int32): Int32
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 乘数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): Int32
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 负号运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): Int32
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): Int32
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 右移运算结果。

#### func saturatingSub(Int32)

```cangjie
public func saturatingSub(y: Int32): Int32
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 减数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 减法运算结果。

### extend Int64 <: SaturatingOp\<Int64> & SaturatingPow

```cangjie
extend Int64 <: SaturatingOp<Int64> & SaturatingPow
```

功能：为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 实现 [SaturatingOp](#interface-saturatingopt) 和 [SaturatingPow](#interface-saturatingpow) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>
- [SaturatingPow](#interface-saturatingpow)

#### func saturatingAdd(Int64)

```cangjie
public func saturatingAdd(y: Int64): Int64
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 加数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): Int64
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 自减运算结果。

#### func saturatingDiv(Int64)

```cangjie
public func saturatingDiv(y: Int64): Int64
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): Int64
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 自增运算结果。

#### func saturatingMod(Int64)

```cangjie
public func saturatingMod(y: Int64): Int64
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 取余运算结果。

#### func saturatingMul(Int64)

```cangjie
public func saturatingMul(y: Int64): Int64
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 乘数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): Int64
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 负号运算结果。

#### func saturatingPow(UInt64)

```cangjie
public func saturatingPow(y: UInt64): Int64
```

功能：使用饱和策略的幂运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 幂运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): Int64
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): Int64
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 右移运算结果。

#### func saturatingSub(Int64)

```cangjie
public func saturatingSub(y: Int64): Int64
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 减数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 减法运算结果。

### extend Int8 <: SaturatingOp\<Int8>

```cangjie
extend Int8 <: SaturatingOp<Int8>
```

功能：为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 实现 [SaturatingOp](#interface-saturatingopt) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### func saturatingAdd(Int8)

```cangjie
public func saturatingAdd(y: Int8): Int8
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 加数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): Int8
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 自减运算结果。

#### func saturatingDiv(Int8)

```cangjie
public func saturatingDiv(y: Int8): Int8
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): Int8
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 自增运算结果。

#### func saturatingMod(Int8)

```cangjie
public func saturatingMod(y: Int8): Int8
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 取余运算结果。

#### func saturatingMul(Int8)

```cangjie
public func saturatingMul(y: Int8): Int8
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 乘数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): Int8
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 负号运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): Int8
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): Int8
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 右移运算结果。

#### func saturatingSub(Int8)

```cangjie
public func saturatingSub(y: Int8): Int8
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 减数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 减法运算结果。

### extend IntNative <: SaturatingOp\<IntNative>

```cangjie
extend IntNative <: SaturatingOp<IntNative>
```

功能：为 [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) 实现 [SaturatingOp](#interface-saturatingopt) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)>

#### func saturatingAdd(IntNative)

```cangjie
public func saturatingAdd(y: IntNative): IntNative
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 加数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): IntNative
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 自减运算结果。

#### func saturatingDiv(IntNative)

```cangjie
public func saturatingDiv(y: IntNative): IntNative
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): IntNative
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 自增运算结果。

#### func saturatingMod(IntNative)

```cangjie
public func saturatingMod(y: IntNative): IntNative
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 取余运算结果。

#### func saturatingMul(IntNative)

```cangjie
public func saturatingMul(y: IntNative): IntNative
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 乘数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): IntNative
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 负号运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): IntNative
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): IntNative
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 右移运算结果。

#### func saturatingSub(IntNative)

```cangjie
public func saturatingSub(y: IntNative): IntNative
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 减数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 减法运算结果。

### extend UInt16 <: SaturatingOp\<UInt16>

```cangjie
extend UInt16 <: SaturatingOp<UInt16>
```

功能：为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 实现 [SaturatingOp](#interface-saturatingopt) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### func saturatingAdd(UInt16)

```cangjie
public func saturatingAdd(y: UInt16): UInt16
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 加数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): UInt16
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 自减运算结果。

#### func saturatingDiv(UInt16)

```cangjie
public func saturatingDiv(y: UInt16): UInt16
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): UInt16
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 自增运算结果。

#### func saturatingMod(UInt16)

```cangjie
public func saturatingMod(y: UInt16): UInt16
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 取余运算结果。

#### func saturatingMul(UInt16)

```cangjie
public func saturatingMul(y: UInt16): UInt16
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 乘数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): UInt16
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 负号运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): UInt16
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): UInt16
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 右移运算结果。

#### func saturatingSub(UInt16)

```cangjie
public func saturatingSub(y: UInt16): UInt16
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 减数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 减法运算结果。

### extend UInt32 <: SaturatingOp\<UInt32>

```cangjie
extend UInt32 <: SaturatingOp<UInt32>
```

功能：为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 实现 [SaturatingOp](#interface-saturatingopt) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### func saturatingAdd(UInt32)

```cangjie
public func saturatingAdd(y: UInt32): UInt32
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 加数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): UInt32
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 自减运算结果。

#### func saturatingDiv(UInt32)

```cangjie
public func saturatingDiv(y: UInt32): UInt32
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): UInt32
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 自增运算结果。

#### func saturatingMod(UInt32)

```cangjie
public func saturatingMod(y: UInt32): UInt32
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 取余运算结果。

#### func saturatingMul(UInt32)

```cangjie
public func saturatingMul(y: UInt32): UInt32
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 乘数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): UInt32
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 负号运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): UInt32
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): UInt32
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 右移运算结果。

#### func saturatingSub(UInt32)

```cangjie
public func saturatingSub(y: UInt32): UInt32
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 减数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 减法运算结果。

### extend UInt64 <: SaturatingOp\<UInt64>

```cangjie
extend UInt64 <: SaturatingOp<UInt64>
```

功能：为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 实现 [SaturatingOp](#interface-saturatingopt) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### func saturatingAdd(UInt64)

```cangjie
public func saturatingAdd(y: UInt64): UInt64
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 加数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): UInt64
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 自减运算结果。

#### func saturatingDiv(UInt64)

```cangjie
public func saturatingDiv(y: UInt64): UInt64
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): UInt64
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 自增运算结果。

#### func saturatingMod(UInt64)

```cangjie
public func saturatingMod(y: UInt64): UInt64
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 取余运算结果。

#### func saturatingMul(UInt64)

```cangjie
public func saturatingMul(y: UInt64): UInt64
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 乘数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): UInt64
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 负号运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): UInt64
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): UInt64
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 右移运算结果。

#### func saturatingSub(UInt64)

```cangjie
public func saturatingSub(y: UInt64): UInt64
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 减数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 减法运算结果。

### extend UInt8 <: SaturatingOp\<UInt8>

```cangjie
extend UInt8 <: SaturatingOp<UInt8>
```

功能：为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 实现 [SaturatingOp](#interface-saturatingopt) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### func saturatingAdd(UInt8)

```cangjie
public func saturatingAdd(y: UInt8): UInt8
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 加数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): UInt8
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 自减运算结果。

#### func saturatingDiv(UInt8)

```cangjie
public func saturatingDiv(y: UInt8): UInt8
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): UInt8
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 自增运算结果。

#### func saturatingMod(UInt8)

```cangjie
public func saturatingMod(y: UInt8): UInt8
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 取余运算结果。

#### func saturatingMul(UInt8)

```cangjie
public func saturatingMul(y: UInt8): UInt8
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 乘数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): UInt8
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 负号运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): UInt8
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): UInt8
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 右移运算结果。

#### func saturatingSub(UInt8)

```cangjie
public func saturatingSub(y: UInt8): UInt8
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 减数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 减法运算结果。

### extend UIntNative <: SaturatingOp\<UIntNative>

```cangjie
extend UIntNative <: SaturatingOp<UIntNative>
```

功能：为 [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) 实现 [SaturatingOp](#interface-saturatingopt) 接口。

父类型：

- [SaturatingOp](#interface-saturatingopt)\<[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)>

#### func saturatingAdd(UIntNative)

```cangjie
public func saturatingAdd(y: UIntNative): UIntNative
```

功能：使用饱和策略的加法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 加数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 加法运算结果。

#### func saturatingDec()

```cangjie
public func saturatingDec(): UIntNative
```

功能：使用饱和策略的自减运算。

当运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 自减运算结果。

#### func saturatingDiv(UIntNative)

```cangjie
public func saturatingDiv(y: UIntNative): UIntNative
```

功能：使用饱和策略的除法运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除法运算结果。

#### func saturatingInc()

```cangjie
public func saturatingInc(): UIntNative
```

功能：使用饱和策略的自增运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 自增运算结果。

#### func saturatingMod(UIntNative)

```cangjie
public func saturatingMod(y: UIntNative): UIntNative
```

功能：使用饱和策略的取余运算。

当运算出现上溢时，返回操作数类型的最大值，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 取余运算结果。

#### func saturatingMul(UIntNative)

```cangjie
public func saturatingMul(y: UIntNative): UIntNative
```

功能：使用饱和策略的乘法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 乘数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 乘法运算结果。

#### func saturatingNeg()

```cangjie
public func saturatingNeg(): UIntNative
```

功能：使用饱和策略的负号运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 负号运算结果。

#### func saturatingShl(UInt64)

```cangjie
public func saturatingShl(y: UInt64): UIntNative
```

功能：使用饱和策略的左移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 左移运算结果。

#### func saturatingShr(UInt64)

```cangjie
public func saturatingShr(y: UInt64): UIntNative
```

功能：使用饱和策略的右移运算。

当移位位数大于等于操作数位数时，将移位位数置为操作数位数 - 1，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 右移运算结果。

#### func saturatingSub(UIntNative)

```cangjie
public func saturatingSub(y: UIntNative): UIntNative
```

功能：使用饱和策略的减法运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 减数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 减法运算结果。

## interface SaturatingPow

```cangjie
public interface SaturatingPow {
    func saturatingPow(y: UInt64): Int64
}
```

功能：提供饱和策略的幂运算接口。

### func saturatingPow(UInt64)

```cangjie
func saturatingPow(y: UInt64): Int64
```

功能：使用饱和策略的幂运算。

当运算出现上溢时，返回操作数类型的最大值，运算出现下溢时，返回操作数类型的最小值，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 幂运算结果。

## interface ThrowingOp\<T>

```cangjie
public interface ThrowingOp<T> {
    func throwingAdd(y: T): T
    func throwingSub(y: T): T
    func throwingMul(y: T): T
    func throwingDiv(y: T): T
    func throwingMod(y: T): T
    func throwingInc(): T
    func throwingDec(): T
    func throwingNeg(): T
    func throwingShl(y: UInt64): T
    func throwingShr(y: UInt64): T
}
```

功能：当整数运算出现溢出，抛出异常。

### func throwingAdd(T)

```cangjie
func throwingAdd(y: T): T
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: T - 加数。

返回值：

- T - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

### func throwingDec()

```cangjie
func throwingDec(): T
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- T - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

### func throwingDiv(T)

```cangjie
func throwingDiv(y: T): T
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: T - 除数。

返回值：

- T - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

### func throwingInc()

```cangjie
func throwingInc(): T
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- T - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

### func throwingMod(T)

```cangjie
func throwingMod(y: T): T
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: T - 除数。

返回值：

- T - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

### func throwingMul(T)

```cangjie
func throwingMul(y: T): T
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: T - 乘数。

返回值：

- T - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

### func throwingNeg()

```cangjie
func throwingNeg(): T
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- T - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

### func throwingShl(UInt64)

```cangjie
func throwingShl(y: UInt64): T
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- T - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

### func throwingShr(UInt64)

```cangjie
func throwingShr(y: UInt64): T
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- T - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

### func throwingSub(T)

```cangjie
func throwingSub(y: T): T
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: T - 减数。

返回值：

- T - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend Int16 <: ThrowingOp\<Int16>

```cangjie
extend Int16 <: ThrowingOp<Int16>
```

功能：为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 实现 [ThrowingOp](#interface-throwingopt) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### func throwingAdd(Int16)

```cangjie
public func throwingAdd(y: Int16): Int16
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 加数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): Int16
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(Int16)

```cangjie
public func throwingDiv(y: Int16): Int16
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): Int16
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(Int16)

```cangjie
public func throwingMod(y: Int16): Int16
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(Int16)

```cangjie
public func throwingMul(y: Int16): Int16
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 乘数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): Int16
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): Int16
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): Int16
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(Int16)

```cangjie
public func throwingSub(y: Int16): Int16
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 减数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend Int32 <: ThrowingOp\<Int32>

```cangjie
extend Int32 <: ThrowingOp<Int32>
```

功能：为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 实现 [ThrowingOp](#interface-throwingopt) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### func throwingAdd(Int32)

```cangjie
public func throwingAdd(y: Int32): Int32
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 加数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): Int32
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(Int32)

```cangjie
public func throwingDiv(y: Int32): Int32
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): Int32
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(Int32)

```cangjie
public func throwingMod(y: Int32): Int32
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(Int32)

```cangjie
public func throwingMul(y: Int32): Int32
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 乘数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): Int32
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): Int32
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): Int32
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(Int32)

```cangjie
public func throwingSub(y: Int32): Int32
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 减数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend Int64 <: ThrowingOp\<Int64> & ThrowingPow

```cangjie
extend Int64 <: ThrowingOp<Int64> & ThrowingPow
```

功能：为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 实现 [ThrowingOp](#interface-throwingopt) 和 [ThrowingPow](#interface-throwingpow) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>
- [ThrowingPow](#interface-throwingpow)

#### func throwingAdd(Int64)

```cangjie
public func throwingAdd(y: Int64): Int64
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 加数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): Int64
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(Int64)

```cangjie
public func throwingDiv(y: Int64): Int64
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): Int64
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(Int64)

```cangjie
public func throwingMod(y: Int64): Int64
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(Int64)

```cangjie
public func throwingMul(y: Int64): Int64
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 乘数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): Int64
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingPow(UInt64)

```cangjie
public func throwingPow(y: UInt64): Int64
```

功能：使用抛出异常策略的幂运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 幂运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当幂运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): Int64
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): Int64
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(Int64)

```cangjie
public func throwingSub(y: Int64): Int64
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 减数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend Int8 <: ThrowingOp\<Int8>

```cangjie
extend Int8 <: ThrowingOp<Int8>
```

功能：为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 实现 [ThrowingOp](#interface-throwingopt) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### func throwingAdd(Int8)

```cangjie
public func throwingAdd(y: Int8): Int8
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 加数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): Int8
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(Int8)

```cangjie
public func throwingDiv(y: Int8): Int8
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): Int8
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(Int8)

```cangjie
public func throwingMod(y: Int8): Int8
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(Int8)

```cangjie
public func throwingMul(y: Int8): Int8
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 乘数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): Int8
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): Int8
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): Int8
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(Int8)

```cangjie
public func throwingSub(y: Int8): Int8
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 减数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend IntNative <: ThrowingOp\<IntNative>

```cangjie
extend IntNative <: ThrowingOp<IntNative>
```

功能：为 [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) 实现 [ThrowingOp](#interface-throwingopt) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)>

#### func throwingAdd(IntNative)

```cangjie
public func throwingAdd(y: IntNative): IntNative
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 加数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): IntNative
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(IntNative)

```cangjie
public func throwingDiv(y: IntNative): IntNative
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): IntNative
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(IntNative)

```cangjie
public func throwingMod(y: IntNative): IntNative
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(IntNative)

```cangjie
public func throwingMul(y: IntNative): IntNative
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 乘数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): IntNative
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): IntNative
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): IntNative
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(IntNative)

```cangjie
public func throwingSub(y: IntNative): IntNative
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 减数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend UInt16 <: ThrowingOp\<UInt16>

```cangjie
extend UInt16 <: ThrowingOp<UInt16>
```

功能：为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 实现 [ThrowingOp](#interface-throwingopt) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### func throwingAdd(UInt16)

```cangjie
public func throwingAdd(y: UInt16): UInt16
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 加数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): UInt16
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(UInt16)

```cangjie
public func throwingDiv(y: UInt16): UInt16
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): UInt16
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(UInt16)

```cangjie
public func throwingMod(y: UInt16): UInt16
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(UInt16)

```cangjie
public func throwingMul(y: UInt16): UInt16
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 乘数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): UInt16
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): UInt16
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): UInt16
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(UInt16)

```cangjie
public func throwingSub(y: UInt16): UInt16
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 减数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend UInt32 <: ThrowingOp\<UInt32>

```cangjie
extend UInt32 <: ThrowingOp<UInt32>
```

功能：为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 实现 [ThrowingOp](#interface-throwingopt) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### func throwingAdd(UInt32)

```cangjie
public func throwingAdd(y: UInt32): UInt32
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 加数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): UInt32
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(UInt32)

```cangjie
public func throwingDiv(y: UInt32): UInt32
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): UInt32
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(UInt32)

```cangjie
public func throwingMod(y: UInt32): UInt32
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(UInt32)

```cangjie
public func throwingMul(y: UInt32): UInt32
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 乘数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): UInt32
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): UInt32
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): UInt32
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(UInt32)

```cangjie
public func throwingSub(y: UInt32): UInt32
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 减数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend UInt64 <: ThrowingOp\<UInt64>

```cangjie
extend UInt64 <: ThrowingOp<UInt64>
```

功能：为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 实现 [ThrowingOp](#interface-throwingopt) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### func throwingAdd(UInt64)

```cangjie
public func throwingAdd(y: UInt64): UInt64
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 加数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): UInt64
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(UInt64)

```cangjie
public func throwingDiv(y: UInt64): UInt64
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): UInt64
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(UInt64)

```cangjie
public func throwingMod(y: UInt64): UInt64
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(UInt64)

```cangjie
public func throwingMul(y: UInt64): UInt64
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 乘数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): UInt64
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): UInt64
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): UInt64
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(UInt64)

```cangjie
public func throwingSub(y: UInt64): UInt64
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 减数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend UInt8 <: ThrowingOp\<UInt8>

```cangjie
extend UInt8 <: ThrowingOp<UInt8>
```

功能：为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 实现 [ThrowingOp](#interface-throwingopt) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### func throwingAdd(UInt8)

```cangjie
public func throwingAdd(y: UInt8): UInt8
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 加数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): UInt8
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(UInt8)

```cangjie
public func throwingDiv(y: UInt8): UInt8
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): UInt8
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(UInt8)

```cangjie
public func throwingMod(y: UInt8): UInt8
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(UInt8)

```cangjie
public func throwingMul(y: UInt8): UInt8
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 乘数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): UInt8
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): UInt8
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): UInt8
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(UInt8)

```cangjie
public func throwingSub(y: UInt8): UInt8
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 减数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

### extend UIntNative <: ThrowingOp\<UIntNative>

```cangjie
extend UIntNative <: ThrowingOp<UIntNative>
```

功能：为 [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) 实现 [ThrowingOp](#interface-throwingopt) 接口。

父类型：

- [ThrowingOp](#interface-throwingopt)\<[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)>

#### func throwingAdd(UIntNative)

```cangjie
public func throwingAdd(y: UIntNative): UIntNative
```

功能：使用抛出异常策略的加法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 加数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 加法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当加法运算出现溢出时，抛出异常。

#### func throwingDec()

```cangjie
public func throwingDec(): UIntNative
```

功能：使用抛出异常策略的自减运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 自减运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自减运算出现溢出时，抛出异常。

#### func throwingDiv(UIntNative)

```cangjie
public func throwingDiv(y: UIntNative): UIntNative
```

功能：使用抛出异常策略的除法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当除法运算出现溢出时，抛出异常。

#### func throwingInc()

```cangjie
public func throwingInc(): UIntNative
```

功能：使用抛出异常策略的自增运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 自增运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当自增运算出现溢出时，抛出异常。

#### func throwingMod(UIntNative)

```cangjie
public func throwingMod(y: UIntNative): UIntNative
```

功能：使用抛出异常策略的取余运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 取余运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当取余运算出现溢出时，抛出异常。

#### func throwingMul(UIntNative)

```cangjie
public func throwingMul(y: UIntNative): UIntNative
```

功能：使用抛出异常策略的乘法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 乘数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 乘法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当乘法运算出现溢出时，抛出异常。

#### func throwingNeg()

```cangjie
public func throwingNeg(): UIntNative
```

功能：使用抛出异常策略的负号运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 负号运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当负号运算出现溢出时，抛出异常。

#### func throwingShl(UInt64)

```cangjie
public func throwingShl(y: UInt64): UIntNative
```

功能：使用抛出异常策略的左移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 左移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingShr(UInt64)

```cangjie
public func throwingShr(y: UInt64): UIntNative
```

功能：右移运算。

当移位位数大于等于操作数位数时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 右移运算结果。

异常：

- [OvershiftException](overflow_package_exceptions.md#class-overshiftexception) - 当移位位数大于等于操作数位数时，抛出异常。

#### func throwingSub(UIntNative)

```cangjie
public func throwingSub(y: UIntNative): UIntNative
```

功能：使用抛出异常策略的减法运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 减数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 减法运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当减法运算出现溢出时，抛出异常。

## interface ThrowingPow

```cangjie
public interface ThrowingPow {
    func throwingPow(y: UInt64): Int64
}
```

功能：提供使用抛出异常策略的幂运算接口。

### func throwingPow(UInt64)

```cangjie
func throwingPow(y: UInt64): Int64
```

功能：使用抛出异常策略的幂运算。

当运算出现溢出时，抛出异常，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 幂运算结果。

异常：

- [OverflowException](../../core/core_package_api/core_package_exceptions.md#class-overflowexception) - 当幂运算出现溢出时，抛出异常。

## interface WrappingOp\<T>

```cangjie
public interface WrappingOp<T> {
    func wrappingAdd(y: T): T
    func wrappingDec(): T
    func wrappingDiv(y: T): T
    func wrappingInc(): T
    func wrappingMod(y: T): T
    func wrappingMul(y: T): T
    func wrappingNeg(): T
    func wrappingShl(y: UInt64): T
    func wrappingShr(y: UInt64): T
    func wrappingSub(y: T): T
}
```

功能：当整数运算出现溢出，高位截断。

### func wrappingAdd(T)

```cangjie
func wrappingAdd(y: T): T
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: T - 加数。

返回值：

- T - 加法运算结果。

### func wrappingDec()

```cangjie
func wrappingDec(): T
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- T - 自减运算结果。

### func wrappingDiv(T)

```cangjie
func wrappingDiv(y: T): T
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: T - 除数。

返回值：

- T - 除法运算结果。

### func wrappingInc()

```cangjie
func wrappingInc(): T
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- T - 自增运算结果。

### func wrappingMod(T)

```cangjie
func wrappingMod(y: T): T
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: T - 除数。

返回值：

- T - 取余运算结果。

### func wrappingMul(T)

```cangjie
func wrappingMul(y: T): T
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: T - 乘数。

返回值：

- T - 乘法运算结果。

### func wrappingNeg()

```cangjie
func wrappingNeg(): T
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- T - 负号运算结果。

### func wrappingShl(UInt64)

```cangjie
func wrappingShl(y: UInt64): T
```

功能：使用高位截断策略的左移运算。

当移位位数大于等于操作数位数时，高位截断。例如，对 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型的数进行移位，当 y（移位位数）超大于等于 8 时，仅取 y 的低 3 位作为移位位数，以此保证移位位数在 0 到 7 之间。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- T - 左移运算结果。

### func wrappingShr(UInt64)

```cangjie
func wrappingShr(y: UInt64): T
```

功能：使用高位截断策略的右移运算。

当移位位数大于等于操作数位数时，高位截断。例如，对 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型的数进行移位，当 y （移位位数）超大于等于 8 时，仅取 y 的低 3 位作为移位位数，以此保证移位位数在 0 到 7 之间。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- T - 右移运算结果。

### func wrappingSub(T)

```cangjie
func wrappingSub(y: T): T
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: T - 减数。

返回值：

- T - 减法运算结果。

### extend Int16 <: WrappingOp\<Int16>

```cangjie
extend Int16 <: WrappingOp<Int16>
```

功能：为 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 实现 [WrappingOp](#interface-wrappingopt) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)>

#### func wrappingAdd(Int16)

```cangjie
public func wrappingAdd(y: Int16): Int16
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 加数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): Int16
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 自减运算结果。

#### func wrappingDiv(Int16)

```cangjie
public func wrappingDiv(y: Int16): Int16
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): Int16
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 自增运算结果。

#### func wrappingMod(Int16)

```cangjie
public func wrappingMod(y: Int16): Int16
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 除数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 取余运算结果。

#### func wrappingMul(Int16)

```cangjie
public func wrappingMul(y: Int16): Int16
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 乘数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): Int16
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 负号运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): Int16
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 4 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): Int16
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 4 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 右移运算结果。

#### func wrappingSub(Int16)

```cangjie
public func wrappingSub(y: Int16): Int16
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 减数。

返回值：

- [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 减法运算结果。

### extend Int32 <: WrappingOp\<Int32>

```cangjie
extend Int32 <: WrappingOp<Int32>
```

功能：为 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 实现 [WrappingOp](#interface-wrappingopt) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)>

#### func wrappingAdd(Int32)

```cangjie
public func wrappingAdd(y: Int32): Int32
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 加数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): Int32
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 自减运算结果。

#### func wrappingDiv(Int32)

```cangjie
public func wrappingDiv(y: Int32): Int32
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): Int32
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 自增运算结果。

#### func wrappingMod(Int32)

```cangjie
public func wrappingMod(y: Int32): Int32
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 除数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 取余运算结果。

#### func wrappingMul(Int32)

```cangjie
public func wrappingMul(y: Int32): Int32
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 乘数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): Int32
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 负号运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): Int32
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 5 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): Int32
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 5 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 右移运算结果。

#### func wrappingSub(Int32)

```cangjie
public func wrappingSub(y: Int32): Int32
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 减数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 减法运算结果。

### extend Int64 <: WrappingOp\<Int64> & WrappingPow

```cangjie
extend Int64 <: WrappingOp<Int64> & WrappingPow
```

功能：为 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 实现 [WrappingOp](#interface-wrappingopt) 和 [WrappingPow](#interface-wrappingpow) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)>
- [WrappingPow](#interface-wrappingpow)

#### func wrappingAdd(Int64)

```cangjie
public func wrappingAdd(y: Int64): Int64
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 加数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): Int64
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 自减运算结果。

#### func wrappingDiv(Int64)

```cangjie
public func wrappingDiv(y: Int64): Int64
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): Int64
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 自增运算结果。

#### func wrappingMod(Int64)

```cangjie
public func wrappingMod(y: Int64): Int64
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 除数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 取余运算结果。

#### func wrappingMul(Int64)

```cangjie
public func wrappingMul(y: Int64): Int64
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 乘数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): Int64
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 负号运算结果。

#### func wrappingPow(UInt64)

```cangjie
public func wrappingPow(y: UInt64): Int64
```

功能：使用高位截断策略的幂运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 幂运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): Int64
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 6 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): Int64
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 6 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 右移运算结果。

#### func wrappingSub(Int64)

```cangjie
public func wrappingSub(y: Int64): Int64
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 减数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 减法运算结果。

### extend Int8 <: WrappingOp\<Int8>

```cangjie
extend Int8 <: WrappingOp<Int8>
```

功能：为 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 实现 [WrappingOp](#interface-wrappingopt) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)>

#### func wrappingAdd(Int8)

```cangjie
public func wrappingAdd(y: Int8): Int8
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 加数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): Int8
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 自减运算结果。

#### func wrappingDiv(Int8)

```cangjie
public func wrappingDiv(y: Int8): Int8
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): Int8
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 自增运算结果。

#### func wrappingMod(Int8)

```cangjie
public func wrappingMod(y: Int8): Int8
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 除数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 取余运算结果。

#### func wrappingMul(Int8)

```cangjie
public func wrappingMul(y: Int8): Int8
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 乘数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): Int8
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 负号运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): Int8
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 3 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): Int8
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 3 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 右移运算结果。

#### func wrappingSub(Int8)

```cangjie
public func wrappingSub(y: Int8): Int8
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 减数。

返回值：

- [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 减法运算结果。

### extend IntNative <: WrappingOp\<IntNative>

```cangjie
extend IntNative <: WrappingOp<IntNative>
```

功能：为 [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) 实现 [WrappingOp](#interface-wrappingopt) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative)>

#### func wrappingAdd(IntNative)

```cangjie
public func wrappingAdd(y: IntNative): IntNative
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 加数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): IntNative
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 自减运算结果。

#### func wrappingDiv(IntNative)

```cangjie
public func wrappingDiv(y: IntNative): IntNative
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): IntNative
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 自增运算结果。

#### func wrappingMod(IntNative)

```cangjie
public func wrappingMod(y: IntNative): IntNative
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 除数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 取余运算结果。

#### func wrappingMul(IntNative)

```cangjie
public func wrappingMul(y: IntNative): IntNative
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 乘数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): IntNative
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 负号运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): IntNative
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低位作为移位位数，具体取的位数取决于当前系统下 [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) 的位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): IntNative
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低位作为移位位数，具体取的位数取决于当前系统下 [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) 的位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 右移运算结果。

#### func wrappingSub(IntNative)

```cangjie
public func wrappingSub(y: IntNative): IntNative
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 减数。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 减法运算结果。

### extend UInt16 <: WrappingOp\<UInt16>

```cangjie
extend UInt16 <: WrappingOp<UInt16>
```

功能：为 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 实现 [WrappingOp](#interface-wrappingopt) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16)>

#### func wrappingAdd(UInt16)

```cangjie
public func wrappingAdd(y: UInt16): UInt16
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 加数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): UInt16
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 自减运算结果。

#### func wrappingDiv(UInt16)

```cangjie
public func wrappingDiv(y: UInt16): UInt16
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): UInt16
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 自增运算结果。

#### func wrappingMod(UInt16)

```cangjie
public func wrappingMod(y: UInt16): UInt16
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 除数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 取余运算结果。

#### func wrappingMul(UInt16)

```cangjie
public func wrappingMul(y: UInt16): UInt16
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 乘数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): UInt16
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 负号运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): UInt16
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 4 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): UInt16
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 4 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 右移运算结果。

#### func wrappingSub(UInt16)

```cangjie
public func wrappingSub(y: UInt16): UInt16
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 减数。

返回值：

- [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) - 减法运算结果。

### extend UInt32 <: WrappingOp\<UInt32>

```cangjie
extend UInt32 <: WrappingOp<UInt32>
```

功能：为 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 实现 [WrappingOp](#interface-wrappingopt) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)>

#### func wrappingAdd(UInt32)

```cangjie
public func wrappingAdd(y: UInt32): UInt32
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 加数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): UInt32
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 自减运算结果。

#### func wrappingDiv(UInt32)

```cangjie
public func wrappingDiv(y: UInt32): UInt32
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): UInt32
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 自增运算结果。

#### func wrappingMod(UInt32)

```cangjie
public func wrappingMod(y: UInt32): UInt32
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 除数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 取余运算结果。

#### func wrappingMul(UInt32)

```cangjie
public func wrappingMul(y: UInt32): UInt32
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 乘数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): UInt32
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 负号运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): UInt32
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 5 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): UInt32
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 5 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 右移运算结果。

#### func wrappingSub(UInt32)

```cangjie
public func wrappingSub(y: UInt32): UInt32
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 减数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 减法运算结果。

### extend UInt64 <: WrappingOp\<UInt64>

```cangjie
extend UInt64 <: WrappingOp<UInt64>
```

功能：为 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 实现 [WrappingOp](#interface-wrappingopt) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64)>

#### func wrappingAdd(UInt64)

```cangjie
public func wrappingAdd(y: UInt64): UInt64
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 加数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): UInt64
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 自减运算结果。

#### func wrappingDiv(UInt64)

```cangjie
public func wrappingDiv(y: UInt64): UInt64
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): UInt64
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 自增运算结果。

#### func wrappingMod(UInt64)

```cangjie
public func wrappingMod(y: UInt64): UInt64
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 除数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 取余运算结果。

#### func wrappingMul(UInt64)

```cangjie
public func wrappingMul(y: UInt64): UInt64
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 乘数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): UInt64
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 负号运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): UInt64
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 6 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): UInt64
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 6 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 右移运算结果。

#### func wrappingSub(UInt64)

```cangjie
public func wrappingSub(y: UInt64): UInt64
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 减数。

返回值：

- [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 减法运算结果。

### extend UInt8 <: WrappingOp\<UInt8>

```cangjie
extend UInt8 <: WrappingOp<UInt8>
```

功能：为 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 实现 [WrappingOp](#interface-wrappingopt) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)>

#### func wrappingAdd(UInt8)

```cangjie
public func wrappingAdd(y: UInt8): UInt8
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 加数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): UInt8
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 自减运算结果。

#### func wrappingDiv(UInt8)

```cangjie
public func wrappingDiv(y: UInt8): UInt8
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): UInt8
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 自增运算结果。

#### func wrappingMod(UInt8)

```cangjie
public func wrappingMod(y: UInt8): UInt8
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 除数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 取余运算结果。

#### func wrappingMul(UInt8)

```cangjie
public func wrappingMul(y: UInt8): UInt8
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 乘数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): UInt8
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 负号运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): UInt8
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 3 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): UInt8
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低 3 位作为移位位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 右移运算结果。

#### func wrappingSub(UInt8)

```cangjie
public func wrappingSub(y: UInt8): UInt8
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 减数。

返回值：

- [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) - 减法运算结果。

### extend UIntNative <: WrappingOp\<UIntNative>

```cangjie
extend UIntNative <: WrappingOp<UIntNative>
```

功能：为 [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) 实现 [WrappingOp](#interface-wrappingopt) 接口。

父类型：

- [WrappingOp](#interface-wrappingopt)\<[UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative)>

#### func wrappingAdd(UIntNative)

```cangjie
public func wrappingAdd(y: UIntNative): UIntNative
```

功能：使用高位截断策略的加法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 加数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 加法运算结果。

#### func wrappingDec()

```cangjie
public func wrappingDec(): UIntNative
```

功能：使用高位截断策略的自减运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 自减运算结果。

#### func wrappingDiv(UIntNative)

```cangjie
public func wrappingDiv(y: UIntNative): UIntNative
```

功能：使用高位截断策略的除法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除法运算结果。

#### func wrappingInc()

```cangjie
public func wrappingInc(): UIntNative
```

功能：使用高位截断策略的自增运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 自增运算结果。

#### func wrappingMod(UIntNative)

```cangjie
public func wrappingMod(y: UIntNative): UIntNative
```

功能：使用高位截断策略的取余运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 除数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 取余运算结果。

#### func wrappingMul(UIntNative)

```cangjie
public func wrappingMul(y: UIntNative): UIntNative
```

功能：使用高位截断策略的乘法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 乘数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 乘法运算结果。

#### func wrappingNeg()

```cangjie
public func wrappingNeg(): UIntNative
```

功能：使用高位截断策略的负号运算。

当运算出现溢出时，高位截断，否则返回运算结果。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 负号运算结果。

#### func wrappingShl(UInt64)

```cangjie
public func wrappingShl(y: UInt64): UIntNative
```

功能：使用高位截断策略的左移运算。

当右操作数大于等于左操作数位数时，取右操作数的低位作为移位位数，具体取的位数取决于当前系统下 UIntNative 的位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 左移运算结果。

#### func wrappingShr(UInt64)

```cangjie
public func wrappingShr(y: UInt64): UIntNative
```

功能：使用高位截断策略的右移运算。

当右操作数大于等于左操作数位数时，取右操作数的低位作为移位位数，具体取的位数取决于当前系统下 UIntNative 的位数。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 移位位数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 右移运算结果。

#### func wrappingSub(UIntNative)

```cangjie
public func wrappingSub(y: UIntNative): UIntNative
```

功能：使用高位截断策略的减法运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 减数。

返回值：

- [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 减法运算结果。

## interface WrappingPow

```cangjie
public interface WrappingPow {
    func wrappingPow(y: UInt64): Int64
}
```

功能：提供使用高位截断策略的幂运算接口。

### func wrappingPow(UInt64)

```cangjie
func wrappingPow(y: UInt64): Int64
```

功能：使用高位截断策略的幂运算。

当运算出现溢出时，高位截断，否则返回运算结果。

参数：

- y: [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) - 指数。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 幂运算结果。
