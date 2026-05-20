# std.overflow

## 功能介绍

overflow 包提供了整数运算溢出时的处理能力。

在整数运算时，若运算结果大于其类型最大值或小于其类型最小值即是溢出。默认情况下，出现溢出时会抛出异常。

overflow 包提供了四种溢出处理策略，并定义了对应的接口，列举如下：

| 策略                   | 接口                          | 描述                                           |
| ---------------------- | ----------------------------- | --------------------------------------------- |
| 返回 Option         | [CheckedOp](./overflow_package_api/overflow_package_interfaces.md#interface-checkedopt)    | 当整数运算出现溢出，返回 `None`。                  |
| 饱和                    | [SaturatingOp](./overflow_package_api/overflow_package_interfaces.md#interface-saturatingopt) | 当计算结果大于目标类型的 MAX 值，返回 MAX 值；当计算结果小于目标类型的 MIN 值，返回 MIN 值。 |
| 抛出异常                | [ThrowingOp](./overflow_package_api/overflow_package_interfaces.md#interface-throwingopt)   | 当整数运算出现溢出，抛出异常。                              |
| 高位截断                | [WrappingOp](./overflow_package_api/overflow_package_interfaces.md#interface-wrappingopt)   | 当整数运算出现溢出，将运算结果中超出目标类型位数的高位截断。                              |

overflow 包中通过扩展为所有的整数类型提供了这些接口的实现，用户可以用同样的方式为其他类型实现 overflow 接口。

## API 列表

### 接口

|              接口名          |           功能           |
| --------------------------- | ------------------------ |
| [CarryingOp](./overflow_package_api/overflow_package_interfaces.md#interface-carryingopt)    | 提供返回整数运算是否发生了截断以及运算结果的接口。                        |
| [CarryingPow](./overflow_package_api/overflow_package_interfaces.md#interface-carryingpow)    | 提供使用 [wrapping](./overflow_package_api//overflow_package_interfaces.md#interface-wrappingopt) 策略的幂运算接口。                        |
| [CheckedOp](./overflow_package_api/overflow_package_interfaces.md#interface-checkedopt)    | 当整数运算出现溢出，返回 `None`。                        |
| [CheckedPow](./overflow_package_api/overflow_package_interfaces.md#interface-checkedpow)    | 提供返回 [Option](../core/core_package_api/core_package_enums.md#enum-optiont) 策略的幂运算接口。                        |
| [SaturatingOp](./overflow_package_api/overflow_package_interfaces.md#interface-saturatingopt) | 当整数运算出现溢出，饱和处理。                           |
| [SaturatingPow](./overflow_package_api/overflow_package_interfaces.md#interface-saturatingpow) | 提供饱和策略的幂运算接口。                           |
| [ThrowingOp](./overflow_package_api/overflow_package_interfaces.md#interface-throwingopt)   | 当整数运算出现溢出，抛出异常。                           |
| [ThrowingPow](./overflow_package_api/overflow_package_interfaces.md#interface-throwingpow)   | 提供使用抛出异常策略的幂运算接口。                           |
| [WrappingOp](./overflow_package_api/overflow_package_interfaces.md#interface-wrappingopt)   | 当整数运算出现溢出，将运算结果中超出目标类型位数的高位截断。                           |
| [WrappingPow](./overflow_package_api/overflow_package_interfaces.md#interface-wrappingpow)   | 提供使用高位截断策略的幂运算接口。                           |

### 异常类

|                 类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [OvershiftException](./overflow_package_api/overflow_package_exceptions.md#class-overshiftexception) | 移位运算时移位位数超过操作数位数时抛出的异常。       |
| [UndershiftException](./overflow_package_api/overflow_package_exceptions.md#class-undershiftexception) | 移位运算时移位位数小于 0 时抛出的异常。          |
