# std.math

## 功能介绍

math 包提供常见的数学运算，常数定义，浮点数处理等功能。

包括了以下能力：

1. 科学常数与类型常数定义；
2. 浮点数的判断，规整；
3. 常用的位运算；
4. 通用的数学函数，如绝对值，三角函数，指数，对数计算；
5. 最大公约数与最小公倍数。

## API 列表

### 函数

|              函数名            |             功能           |
| ----------------------------- | -------------------------- |
| [abs(Float16)](./math_package_api/math_package_funcs.md#func-absfloat16) | 求一个半精度浮点数的绝对值。|
| [abs(Float32)](./math_package_api/math_package_funcs.md#func-absfloat32) | 求一个单精度浮点数的绝对值。|
| [abs(Float64)](./math_package_api/math_package_funcs.md#func-absfloat64) | 求一个双精度浮点数的绝对值。|
| [abs(Int16)](./math_package_api/math_package_funcs.md#func-absint16) | 求一个 16 位有符号整数的绝对值。|
| [abs(Int32)](./math_package_api/math_package_funcs.md#func-absint32) | 求一个 32 位有符号整数的绝对值。|
| [abs(Int64)](./math_package_api/math_package_funcs.md#func-absint64) | 求一个 64 位有符号整数的绝对值。|
| [abs(Int8)](./math_package_api/math_package_funcs.md#func-absint8) | 求一个 8 位有符号整数的绝对值。|
| [acos(Float16)](./math_package_api/math_package_funcs.md#func-acosfloat16) | 计算半精度浮点数的反余弦函数值，单位为弧度。|
| [acos(Float32)](./math_package_api/math_package_funcs.md#func-acosfloat32) | 计算单精度浮点数的反余弦函数值，单位为弧度。|
| [acos(Float64)](./math_package_api/math_package_funcs.md#func-acosfloat64) | 计算双精度浮点数的反余弦函数值，单位为弧度。|
| [acosh(Float16)](./math_package_api/math_package_funcs.md#func-acoshfloat16) | 计算半精度浮点数的反双曲余弦函数值。|
| [acosh(Float32)](./math_package_api/math_package_funcs.md#func-acoshfloat32) | 计算单精度浮点数的反双曲余弦函数值。|
| [acosh(Float64)](./math_package_api/math_package_funcs.md#func-acoshfloat64) | 计算双精度浮点数的反双曲余弦函数值。|
| [asin(Float16)](./math_package_api/math_package_funcs.md#func-asinfloat16) | 计算半精度浮点数的反正弦函数值，单位为弧度。|
| [asin(Float32)](./math_package_api/math_package_funcs.md#func-asinfloat32) | 计算单精度浮点数的反正弦函数值，单位为弧度。|
| [asin(Float64)](./math_package_api/math_package_funcs.md#func-asinfloat64) | 计算双精度浮点数的反正弦函数值，单位为弧度。|
| [asinh(Float16)](./math_package_api/math_package_funcs.md#func-asinhfloat16) | 计算半精度浮点数的反双曲正弦函数值。|
| [asinh(Float32)](./math_package_api/math_package_funcs.md#func-asinhfloat32) | 计算单精度浮点数的反双曲正弦函数值。|
| [asinh(Float64)](./math_package_api/math_package_funcs.md#func-asinhfloat64) | 计算双精度浮点数的反双曲正弦函数值。|
| [atan(Float16)](./math_package_api/math_package_funcs.md#func-atanfloat16) | 计算半精度浮点数的反正切函数值，单位为弧度。|
| [atan(Float32)](./math_package_api/math_package_funcs.md#func-atanfloat32) | 计算单精度浮点数的反正切函数值，单位为弧度。|
| [atan(Float64)](./math_package_api/math_package_funcs.md#func-atanfloat64) | 计算双精度浮点数的反正切函数值，单位为弧度。|
| [atan2(Float16, Float16)](./math_package_api/math_package_funcs.md#func-atan2float16-float16) | 计算两个半精度浮点数的反正切函数值，单位为弧度。|
| [atan2(Float32, Float32)](./math_package_api/math_package_funcs.md#func-atan2float32-float32) | 计算两个单精度浮点数的反正切函数值，单位为弧度。|
| [atan2(Float64, Float64)](./math_package_api/math_package_funcs.md#func-atan2float64-float64) | 计算两个双精度浮点数的反正切函数值，单位为弧度。|
| [atanh(Float16)](./math_package_api/math_package_funcs.md#func-asinhfloat16) | 计算半精度浮点数的反双曲正切函数值。|
| [atanh(Float32)](./math_package_api/math_package_funcs.md#func-atanhfloat32) | 计算单精度浮点数的反双曲正切函数值。|
| [atanh(Float64)](./math_package_api/math_package_funcs.md#func-atanhfloat64) | 计算双精度浮点数的反双曲正切函数值。|
| [cbrt(Float16)](./math_package_api/math_package_funcs.md#func-cbrtfloat16) | 求半精度浮点数的立方根。|
| [cbrt(Float32)](./math_package_api/math_package_funcs.md#func-cbrtfloat32) | 求单精度浮点数的立方根。|
| [cbrt(Float64)](./math_package_api/math_package_funcs.md#func-cbrtfloat64) | 求双精度浮点数的立方根。|
| [ceil(Float16)](./math_package_api/math_package_funcs.md#func-ceilfloat16) | 求半精度浮点数的向上取整值。|
| [ceil(Float32)](./math_package_api/math_package_funcs.md#func-ceilfloat32) | 求单精度浮点数的向上取整值。|
| [ceil(Float64)](./math_package_api/math_package_funcs.md#func-ceilfloat64) | 求双精度浮点数的向上取整值。|
| [checkedAbs(Int16)](./math_package_api/math_package_funcs.md#func-checkedabsint16) | 检查并求一个 16 位有符号整数的绝对值。如果入参是 16 位有符号整数的最小值，函数返回 `None`；否则，返回 `Some(abs(x))`。|
| [checkedAbs(Int32)](./math_package_api/math_package_funcs.md#func-checkedabsint32) | 检查并求一个 32 位有符号整数的绝对值。如果入参是 32 位有符号整数的最小值，函数返回 `None`；否则，返回 `Some(abs(x))`。|
| [checkedAbs(Int64)](./math_package_api/math_package_funcs.md#func-checkedabsint64) | 检查并求一个 64 位有符号整数的绝对值。如果入参是 64 位有符号整数的最小值，函数返回 `None`；否则，返回 `Some(abs(x))`。|
| [checkedAbs(Int8)](./math_package_api/math_package_funcs.md#func-checkedabsint8) | 检查并求一个 8 位有符号整数的绝对值。如果入参是 8 位有符号整数的最小值，函数返回 `None`；否则，返回 `Some(abs(x))`。|
| [clamp(Float16, Float16, Float16)](./math_package_api/math_package_funcs.md#func-clampfloat16-float16-float16) | 求浮点数的范围区间数。如果此浮点数在该范围区间则返回此浮点数；如果此浮点数小于这个范围区间，则返回该范围区间的最小值；如果此浮点数大于这个范围区间，则返回该范围区间的最大值；如果是 `NaN` 则返回 `NaN`。|
| [clamp(Float32, Float32, Float32)](./math_package_api/math_package_funcs.md#func-clampfloat32-float32-float32) | 求浮点数的范围区间数。如果此浮点数在该范围区间则返回此浮点数；如果此浮点数小于这个范围区间，则返回该范围区间的最小值；如果此浮点数大于这个范围区间，则返回该范围区间的最大值；如果是 `NaN` 则返回 `NaN`。 |
| [clamp(Float64, Float64, Float64)](./math_package_api/math_package_funcs.md#func-clampfloat64-float64-float64) | 求浮点数的范围区间数。如果此浮点数在该范围区间则返回此浮点数；如果此浮点数小于这个范围区间，则返回该范围区间的最小值；如果此浮点数大于这个范围区间，则返回该范围区间的最大值；如果是 `NaN` 则返回 `NaN`。 |
| [cos(Float16)](./math_package_api/math_package_funcs.md#func-cosfloat16) | 计算半精度浮点数的余弦函数值，入参单位为弧度。 |
| [cos(Float32)](./math_package_api/math_package_funcs.md#func-cosfloat32) | 计算单精度浮点数的余弦函数值，入参单位为弧度。 |
| [cos(Float64)](./math_package_api/math_package_funcs.md#func-cosfloat64) | 计算双精度浮点数的余弦函数值，入参单位为弧度。 |
| [cosh(Float16)](./math_package_api/math_package_funcs.md#func-coshfloat16) | 计算半精度浮点数的双曲余弦函数值。 |
| [cosh(Float32)](./math_package_api/math_package_funcs.md#func-coshfloat32) | 计算单精度浮点数的双曲余弦函数值。 |
| [cosh(Float64)](./math_package_api/math_package_funcs.md#func-coshfloat64) | 计算双精度浮点数的双曲余弦函数值。 |
| [countOne(Int16) <sup>(deprecated)</sup>](./math_package_api/math_package_funcs.md#func-countoneint16-deprecated) | 求 16 位整型的二进制表达中的 1 的位的个数。 |
| [countOne(Int32) <sup>(deprecated)</sup>](./math_package_api/math_package_funcs.md#func-countoneint32-deprecated) | 求 32 位整型的二进制表达中的 1 的位的个数。 |
| [countOne(Int64) <sup>(deprecated)</sup>](./math_package_api/math_package_funcs.md#func-countoneint64-deprecated) | 求 64 位整型的二进制表达中的 1 的位的个数。 |
| [countOne(Int8) <sup>(deprecated)</sup>](./math_package_api/math_package_funcs.md#func-countoneint8-deprecated) | 求 8 位整型的二进制表达中的 1 的位的个数。 |
| [countOne(UInt16) <sup>(deprecated)</sup>](./math_package_api/math_package_funcs.md#func-countoneuint16-deprecated) | 求 16 位无符号整型的二进制表达中的 1 的位的个数。 |
| [countOne(UInt32) <sup>(deprecated)</sup>](./math_package_api/math_package_funcs.md#func-countoneuint32-deprecated) | 求 32 位无符号整型的二进制表达中的 1 的位的个数。 |
| [countOne(UInt64) <sup>(deprecated)</sup>](./math_package_api/math_package_funcs.md#func-countoneuint64-deprecated) | 求 64 位无符号整型的二进制表达中的 1 的位的个数。 |
| [countOne(UInt8) <sup>(deprecated)</sup>](./math_package_api/math_package_funcs.md#func-countoneuint8-deprecated) | 求 8 位无符号整型的二进制表达中的 1 的位的个数。 |
| [countOnes(Int16)](./math_package_api/math_package_funcs.md#func-countonesint16) | 求 16 位整型的二进制表达中的 1 的位的个数。 |
| [countOnes(Int32)](./math_package_api/math_package_funcs.md#func-countonesint32) | 求 32 位整型的二进制表达中的 1 的位的个数。 |
| [countOnes(Int64)](./math_package_api/math_package_funcs.md#func-countonesint64) | 求 64 位整型的二进制表达中的 1 的位的个数。 |
| [countOnes(Int8)](./math_package_api/math_package_funcs.md#func-countonesint8) | 求 8 位整型的二进制表达中的 1 的位的个数。 |
| [countOnes(UInt16)](./math_package_api/math_package_funcs.md#func-countonesuint16) | 求 16 位无符号整型的二进制表达中的 1 的位的个数。 |
| [countOnes(UInt32)](./math_package_api/math_package_funcs.md#func-countonesuint32) | 求 32 位无符号整型的二进制表达中的 1 的位的个数。 |
| [countOnes(UInt64)](./math_package_api/math_package_funcs.md#func-countonesuint64) | 求 64 位无符号整型的二进制表达中的 1 的位的个数。 |
| [countOnes(UInt8)](./math_package_api/math_package_funcs.md#func-countonesuint8) | 求 8 位无符号整型的二进制表达中的 1 的位的个数。 |
| [erf(Float16)](./math_package_api/math_package_funcs.md#func-erffloat16) | 求半精度浮点数的误差值。 |
| [erf(Float32)](./math_package_api/math_package_funcs.md#func-erffloat32) | 求单精度浮点数的误差值。 |
| [erf(Float64)](./math_package_api/math_package_funcs.md#func-erffloat64) | 求双精度浮点数的误差值。 |
| [exp(Float16)](./math_package_api/math_package_funcs.md#func-expfloat16) | 求自然常数 e 的 `x` 次幂。 |
| [exp(Float32)](./math_package_api/math_package_funcs.md#func-expfloat32) | 求自然常数 e 的 `x` 次幂。 |
| [exp(Float64)](./math_package_api/math_package_funcs.md#func-expfloat64) | 求自然常数 e 的 `x` 次幂。 |
| [exp2(Float16)](./math_package_api/math_package_funcs.md#func-expfloat16) | 求 2 的 `x` 次幂。 |
| [exp2(Float32)](./math_package_api/math_package_funcs.md#func-expfloat32) | 求 2 的 `x` 次幂。 |
| [exp2(Float64)](./math_package_api/math_package_funcs.md#func-expfloat64) | 求 2 的 `x` 次幂。 |
| [floor(Float16)](./math_package_api/math_package_funcs.md#func-floorfloat16) | 求浮点数的向下取整值。 |
| [floor(Float32)](./math_package_api/math_package_funcs.md#func-floorfloat32) | 求浮点数的向下取整值。 |
| [floor(Float64)](./math_package_api/math_package_funcs.md#func-floorfloat64) | 求浮点数的向下取整值。 |
| [fmod(Float16, Float16)](./math_package_api/math_package_funcs.md#func-fmodfloat16-float16) | 求两个半精度浮点数相除的余数。 |
| [fmod(Float32, Float32)](./math_package_api/math_package_funcs.md#func-fmodfloat32-float32) | 求两个单精度浮点数相除的余数。 |
| [fmod(Float64, Float64)](./math_package_api/math_package_funcs.md#func-fmodfloat64-float64) | 求两个双精度浮点数相除的余数。 |
| [gamma(Float16)](./math_package_api/math_package_funcs.md#func-gammafloat16) | 求浮点数的 Gamma 值。 |
| [gamma(Float32)](./math_package_api/math_package_funcs.md#func-gammafloat32) | 求浮点数的 Gamma 值。 |
| [gamma(Float64)](./math_package_api/math_package_funcs.md#func-gammafloat64) | 求浮点数的 Gamma 值。 |
| [gcd(Int16, Int16)](./math_package_api/math_package_funcs.md#func-gcdint16-int16) | 求两个 16 位有符号整数的最大公约数。 |
| [gcd(Int32, Int32)](./math_package_api/math_package_funcs.md#func-gcdint32-int32) | 求两个 32 位有符号整数的最大公约数。 |
| [gcd(Int64, Int64)](./math_package_api/math_package_funcs.md#func-gcdint64-int64) | 求两个 64 位有符号整数的最大公约数。 |
| [gcd(Int8, Int8)](./math_package_api/math_package_funcs.md#func-gcdint8-int8) | 求两个 8 位有符号整数的最大公约数。 |
| [gcd(UInt16, UInt16)](./math_package_api/math_package_funcs.md#func-gcduint16-uint16) | 求两个 16 位无符号整数的最大公约数。 |
| [gcd(UInt32, UInt32)](./math_package_api/math_package_funcs.md#func-gcduint32-uint32) | 求两个 32 位无符号整数的最大公约数。 |
| [gcd(UInt64, UInt64)](./math_package_api/math_package_funcs.md#func-gcduint64-uint64) | 求两个 64 位无符号整数的最大公约数。 |
| [gcd(UInt8, UInt8)](./math_package_api/math_package_funcs.md#func-gcduint8-uint8) | 求两个 8 位无符号整数的最大公约数。 |
| [lcm(Int16, Int16)](./math_package_api/math_package_funcs.md#func-lcmint16-int16) | 求两个 16 位有符号整数的最小的非负的公倍数，当入参有 0 时才返回 0。 |
| [lcm(Int32, Int32)](./math_package_api/math_package_funcs.md#func-lcmint32-int32) | 求两个 32 位有符号整数的最小的非负的公倍数，当入参有 0 时才返回 0。 |
| [lcm(Int64, Int64)](./math_package_api/math_package_funcs.md#func-lcmint64-int64) | 求两个 64 位有符号整数的最小的非负的公倍数，当入参有 0 时才返回 0。 |
| [lcm(Int8, Int8)](./math_package_api/math_package_funcs.md#func-lcmint8-int8) | 求两个 8 位有符号整数的最小的非负的公倍数，当入参有 0 时才返回 0。 |
| [lcm(UInt16, UInt16)](./math_package_api/math_package_funcs.md#func-lcmuint16-uint16) | 求两个 16 位无符号整数的最小的非负的公倍数，当入参有 0 时才返回 0。 |
| [lcm(UInt32, UInt32)](./math_package_api/math_package_funcs.md#func-lcmuint32-uint32) | 求两个 32 位无符号整数的最小的非负的公倍数，当入参有 0 时才返回 0。 |
| [lcm(UInt64, UInt64)](./math_package_api/math_package_funcs.md#func-lcmuint64-uint64) | 求两个 64 位无符号整数的最小的非负的公倍数，当入参有 0 时才返回 0。 |
| [lcm(UInt8, UInt8)](./math_package_api/math_package_funcs.md#func-lcmuint8-uint8) | 求两个 8 位无符号整数的最小的非负的公倍数，当入参有 0 时才返回 0。 |
| [leadingZeros(Int16)](./math_package_api/math_package_funcs.md#func-leadingzerosint16) | 求 16 位有符号整数的二进制表达中的从最高位算起，连续位为 0 的个数。如果最高位不是 0，则返回 0。 |
| [leadingZeros(Int32)](./math_package_api/math_package_funcs.md#func-leadingzerosint32) | 求 32 位有符号整数的二进制表达中的从最高位算起，连续位为 0 的个数。如果最高位不是 0，则返回 0。 |
| [leadingZeros(Int64)](./math_package_api/math_package_funcs.md#func-leadingzerosint64) | 求 64 位有符号整数的二进制表达中的从最高位算起，连续位为 0 的个数。如果最高位不是 0，则返回 0。 |
| [leadingZeros(Int8)](./math_package_api/math_package_funcs.md#func-leadingzerosint8) | 求 8 位有符号整数的二进制表达中的从最高位算起，包含符号位，连续位为 0 的个数。如果最高位不是 0，则返回 0。 |
| [leadingZeros(UInt16)](./math_package_api/math_package_funcs.md#func-leadingzerosuint16) | 求 16 位无符号整数的二进制表达中的从最高位算起，连续位为 0 的个数。 |
| [leadingZeros(UInt32)](./math_package_api/math_package_funcs.md#func-leadingzerosuint32) | 求 32 位无符号整数的二进制表达中的从最高位算起，连续位为 0 的个数。 |
| [leadingZeros(UInt64)](./math_package_api/math_package_funcs.md#func-leadingzerosuint64) | 求 64 位无符号整数的二进制表达中的从最高位算起，连续位为 0 的个数。 |
| [leadingZeros(UInt8)](./math_package_api/math_package_funcs.md#func-leadingzerosuint8) | 求 8 位无符号整数的二进制表达中的从最高位算起，连续位为 0 的个数。 |
| [log(Float16)](./math_package_api/math_package_funcs.md#func-logfloat16) | 求以 e 为底 `x` 的对数。 |
| [log(Float32)](./math_package_api/math_package_funcs.md#func-logfloat32) | 求以 e 为底 `x` 的对数。 |
| [log(Float64)](./math_package_api/math_package_funcs.md#func-logfloat64) | 求以 e 为底 `x` 的对数。 |
| [log10(Float16)](./math_package_api/math_package_funcs.md#func-log10float16) | 求以 10 为底 `x` 的对数。 |
| [log10(Float32)](./math_package_api/math_package_funcs.md#func-log10float32) | 求以 10 为底 `x` 的对数。 |
| [log10(Float64)](./math_package_api/math_package_funcs.md#func-log10float64) | 求以 10 为底 `x` 的对数。 |
| [log2(Float16)](./math_package_api/math_package_funcs.md#func-logfloat16) | 求以 2 为底 `x` 的对数。 |
| [log2(Float32)](./math_package_api/math_package_funcs.md#func-logfloat32) | 求以 2 为底 `x` 的对数。 |
| [log2(Float64)](./math_package_api/math_package_funcs.md#func-logfloat64) | 求以 2 为底 `x` 的对数。 |
| [logBase(Float16, Float16)](./math_package_api/math_package_funcs.md#func-logbasefloat16-float16) | 求以 `base` 为底 `x` 的对数。 |
| [logBase(Float32, Float32)](./math_package_api/math_package_funcs.md#func-logbasefloat32-float32) | 求以 `base` 为底 `x` 的对数。 |
| [logBase(Float64, Float64)](./math_package_api/math_package_funcs.md#func-logbasefloat64-float64) | 求以 `base` 为底 `x` 的对数。 |
| [pow(Float32, Float32)](./math_package_api/math_package_funcs.md#func-powfloat32-float32) | 求浮点数 `base` 的 `exponent` 次幂。 |
| [pow(Float32, Int32)](./math_package_api/math_package_funcs.md#func-powfloat32-int32) | 求浮点数 `base` 的 `exponent` 次幂。 |
| [pow(Float64, Float64)](./math_package_api/math_package_funcs.md#func-powfloat64-float64) | 求浮点数 `base` 的 `exponent` 次幂。 |
| [pow(Float64, Int64)](./math_package_api/math_package_funcs.md#func-powfloat64-int64) | 求浮点数 `base` 的 `exponent` 次幂。 |
| [reverse(UInt16)](./math_package_api/math_package_funcs.md#func-reverseuint16) | 求无符号整数按位反转后的数。 |
| [reverse(UInt32)](./math_package_api/math_package_funcs.md#func-reverseuint32) | 求无符号整数按位反转后的数。 |
| [reverse(UInt64)](./math_package_api/math_package_funcs.md#func-reverseuint64) | 求无符号整数按位反转后的数。 |
| [reverse(UInt8)](./math_package_api/math_package_funcs.md#func-reverseuint8) | 求无符号整数按位反转后的数。 |
| [rotate(Int16, Int8)](./math_package_api/math_package_funcs.md#func-rotateint16-int8) | 求整数的按位旋转后的结果。 |
| [rotate(Int32, Int8)](./math_package_api/math_package_funcs.md#func-rotateint32-int8) | 求整数的按位旋转后的结果。 |
| [rotate(Int64, Int8)](./math_package_api/math_package_funcs.md#func-rotateint64-int8) | 求整数的按位旋转后的结果。 |
| [rotate(Int8, Int8)](./math_package_api/math_package_funcs.md#func-rotateint8-int8) | 求整数的按位旋转后的结果。 |
| [rotate(UInt16, Int8)](./math_package_api/math_package_funcs.md#func-rotateuint16-int8) | 求整数的按位旋转后的结果。 |
| [rotate(UInt32, Int8)](./math_package_api/math_package_funcs.md#func-rotateuint32-int8) | 求整数的按位旋转后的结果。 |
| [rotate(UInt64, Int8)](./math_package_api/math_package_funcs.md#func-rotateuint64-int8) | 求整数的按位旋转后的结果。 |
| [rotate(UInt8, Int8)](./math_package_api/math_package_funcs.md#func-rotateuint8-int8) | 求整数的按位旋转后的结果。 |
| [round(Float16)](./math_package_api/math_package_funcs.md#func-roundfloat16) | 此函数采用 IEEE-754 的向最近舍入规则，计算浮点数的舍入值。 |
| [round(Float32)](./math_package_api/math_package_funcs.md#func-roundfloat32) | 此函数采用 IEEE-754 的向最近舍入规则，计算浮点数的舍入值。 |
| [round(Float64)](./math_package_api/math_package_funcs.md#func-roundfloat64) | 此函数采用 IEEE-754 的向最近舍入规则，计算浮点数的舍入值。 |
| [sin(Float16)](./math_package_api/math_package_funcs.md#func-sinfloat16) | 计算半精度浮点数的正弦函数值，入参单位为弧度。 |
| [sin(Float32)](./math_package_api/math_package_funcs.md#func-sinfloat32) | 计算单精度浮点数的正弦函数值，入参单位为弧度。 |
| [sin(Float64)](./math_package_api/math_package_funcs.md#func-sinfloat64) | 计算双精度浮点数的正弦函数值，入参单位为弧度。 |
| [sinh(Float16)](./math_package_api/math_package_funcs.md#func-sinhfloat16) | 计算半精度浮点数的双曲正弦函数值。 |
| [sinh(Float32)](./math_package_api/math_package_funcs.md#func-sinhfloat32) | 计算单精度浮点数的双曲正弦函数值。 |
| [sinh(Float64)](./math_package_api/math_package_funcs.md#func-sinhfloat64) | 计算双精度浮点数的双曲正弦函数值。 |
| [sqrt(Float16)](./math_package_api/math_package_funcs.md#func-sqrtfloat16) | 求浮点数的算术平方根。 |
| [sqrt(Float32)](./math_package_api/math_package_funcs.md#func-sqrtfloat32) | 求浮点数的算术平方根。 |
| [sqrt(Float64)](./math_package_api/math_package_funcs.md#func-sqrtfloat64) | 求浮点数的算术平方根。 |
| [tan(Float16)](./math_package_api/math_package_funcs.md#func-tanfloat16) | 计算半精度浮点数的正切函数值，入参单位为弧度。 |
| [tan(Float32)](./math_package_api/math_package_funcs.md#func-tanfloat32) | 计算单精度浮点数的正切函数值，入参单位为弧度。 |
| [tan(Float64)](./math_package_api/math_package_funcs.md#func-tanfloat64) | 计算双精度浮点数的正切函数值，入参单位为弧度。 |
| [tanh(Float16)](./math_package_api/math_package_funcs.md#func-tanhfloat16) | 计算半精度浮点数的双曲正切函数值。 |
| [tanh(Float32)](./math_package_api/math_package_funcs.md#func-tanhfloat32) | 计算单精度浮点数的双曲正切函数值。 |
| [tanh(Float64)](./math_package_api/math_package_funcs.md#func-tanhfloat64) | 计算双精度浮点数的双曲正切函数值。 |
| [trailingZeros(Int16)](./math_package_api/math_package_funcs.md#func-trailingzerosint16) | 求 16 位有符号整数的二进制表达中的从最低位算起，连续位为 0 的个数。如果最低位不是 0，则返回 0。 |
| [trailingZeros(Int32)](./math_package_api/math_package_funcs.md#func-trailingzerosint32) | 求 32 位有符号整数的二进制表达中的从最低位算起，连续位为 0 的个数。如果最低位不是 0，则返回 0。 |
| [trailingZeros(Int64)](./math_package_api/math_package_funcs.md#func-trailingzerosint64) | 求 64 位有符号整数的二进制表达中的从最低位算起，连续位为 0 的个数。如果最低位不是 0，则返回 0。 |
| [trailingZeros(Int8)](./math_package_api/math_package_funcs.md#func-trailingzerosint8) | 求 16 位有符号整数的二进制表达中的从最低位算起，连续位为 0 的个数。如果最低位不是 0，则返回 0。 |
| [trailingZeros(UInt16)](./math_package_api/math_package_funcs.md#func-trailingzerosuint16) | 求 16 位无符号整数的二进制表达中的从最低位算起，连续位为 0 的个数。如果最低位不是 0，则返回 0。 |
| [trailingZeros(UInt32)](./math_package_api/math_package_funcs.md#func-trailingzerosuint32) | 求 32 位无符号整数的二进制表达中的从最低位算起，连续位为 0 的个数。如果最低位不是 0，则返回 0。 |
| [trailingZeros(UInt64)](./math_package_api/math_package_funcs.md#func-trailingzerosuint64) | 求 64 位无符号整数的二进制表达中的从最低位算起，连续位为 0 的个数。如果最低位不是 0，则返回 0。 |
| [trailingZeros(UInt8)](./math_package_api/math_package_funcs.md#func-trailingzerosuint8) | 求 8 位无符号整数的二进制表达中的从最低位算起，连续位为 0 的个数。如果最低位不是 0，则返回 0。 |
| [trunc(Float16)](./math_package_api/math_package_funcs.md#func-truncfloat16) | 求浮点数的截断取整值。 |
| [trunc(Float32)](./math_package_api/math_package_funcs.md#func-truncfloat32) | 求浮点数的截断取整值。 |
| [trunc(Float64)](./math_package_api/math_package_funcs.md#func-truncfloat64) | 求浮点数的截断取整值。 |

### 接口

|  接口名 | 功能  |
| ------------ | ------------ |
| [FloatingPoint\<T>](./math_package_api/math_package_interfaces.md#interface-floatingpointt)| 本接口提供了浮点数相关的方法。|
| [Integer\<T>](./math_package_api/math_package_interfaces.md#interface-integert)| 本接口提供了整数类型相关的方法。|
| [MathExtension <sup>(deprecated)</sup>](./math_package_api/math_package_interfaces.md#interface-mathextensiont-deprecated)| 为了导出 prop 而作辅助接口，浮点数导出 PI，E 属性。|
| [MaxMinValue\<T>](./math_package_api/math_package_interfaces.md#interface-maxminvaluet)| 提供获取最大值和最小值的方法。|
| [Number\<T>](./math_package_api/math_package_interfaces.md#interface-numbert)| 提供数值类型相关的方法。|

### 枚举

|                 枚举              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [RoundingMode](./math_package_api/math_package_enums.md#enum-roundingmode) | 舍入规则枚举类，共包含 6 种舍入规则。除包含 IEEE 754 浮点数规定约定的 5 种舍入规则外，提供使用较多的 “四舍五入” 舍入规则。 |
