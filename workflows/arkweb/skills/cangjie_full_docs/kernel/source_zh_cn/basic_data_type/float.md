# 浮点类型

浮点类型包括 `Float16`、 `Float32` 和 `Float64`，分别用于表示编码长度为 `16-bit`、 `32-bit` 和 `64-bit` 的浮点数（带小数部分的数字，如 3.14159、8.24 和 0.1 等）的类型。`Float16`、 `Float32` 和 `Float64` 分别对应 IEEE 754 中的半精度格式（即 binary16）、单精度格式（即 binary32）和双精度格式（即 binary64）。

`Float64` 的精度（有效数字位）约为 15 位，`Float32` 的精度（有效数字位）约为 6 位，`Float16` 的精度（有效数字位）约为 3 位。使用哪种浮点类型，取决于代码中需要处理的浮点数的性质和范围。在多种浮点类型都适合的情况下，首选精度高的浮点类型，因为精度低的浮点类型的累计计算误差很容易扩散，并且它能精确表示的整数范围也很有限。

## 浮点类型字面量

浮点类型字面量有两种进制表示形式：十进制、十六进制。在十进制表示中，一个浮点字面量至少要包含一个整数部分或一个小数部分，没有小数部分时必须包含指数部分（以 `e` 或 `E` 为前缀，底数为 10）。在十六进制表示中，一个浮点字面量除了至少要包含一个整数部分或小数部分（以 `0x` 或 `0X` 为前缀），同时必须包含指数部分（以 `p` 或 `P` 为前缀，底数为 2）。

下面的例子展示了浮点字面量的使用：

<!-- compile -->

```cangjie
let a: Float32 = 3.14       // a is 3.140000 with type Float32
let b: Float32 = 2e3        // b is 2000.000000 with type Float32
let c: Float32 = 2.4e-1     // c is 0.240000 with type Float32
let d: Float64 = .123e2     // d is 12.300000 with type Float64
let e: Float64 = 0x1.1p0    // e is 1.062500 with type Float64
let f: Float64 = 0x1p2      // f is 4.000000 with type Float64
let g: Float64 = 0x.2p4     // g is 2.000000 with type Float64
```

在使用十进制浮点数字面量时，可以通过加入后缀来明确浮点数字面量的类型，后缀与类型的对应为：

|  后缀 | 类型    |
| :---- | :------ |
| f16   | Float16 |
| f32   | Float32 |
| f64   | Float64 |

加入了后缀的浮点数字面量可以像下面的方式来使用：

<!-- compile -->

```cangjie
let a = 3.14f32   // a is 3.140000 with type Float32
let b = 2e3f32    // b is 2000.000000 with type Float32
let c = 2.4e-1f64 // c is 0.240000 with type Float64
let d = .123e2f64 // d is 12.300000 with type Float64
```

## 浮点类型支持的操作

浮点类型默认支持的操作符包括：算术操作符、关系操作符、复合赋值操作符。浮点类型不支持自增和自减操作符。

浮点类型之间、浮点类型和整数类型之间可以互相转换，具体的类型转换语法及规则请参见[数值类型之间的转换](../class_and_interface/typecast.md#数值类型之间的转换)。
