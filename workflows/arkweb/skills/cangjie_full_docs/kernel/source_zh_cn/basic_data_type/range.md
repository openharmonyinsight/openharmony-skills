# 区间类型

区间类型用于表示拥有固定步长的序列，区间类型是一个[泛型](../generic/generic_overview.md)，使用 `Range<T>` 表示。当 `T` 被实例化为不同类型时，要求此类型必须支持关系操作符，并且可以和 `Int64` 类型的值做加法，这会得到不同的区间类型。例如，最常用的 `Range<Int64>` 用于表示整数区间。

每个区间类型的实例都会包含 `start`、`end` 和 `step` 三个值。其中，`start` 和 `end` 分别表示序列的起始值和终止值，`step` 表示序列中前后两个元素之间的差值（即步长）；`start` 和 `end` 的类型相同（即 `T` 被实例化的类型），`step` 类型是 `Int64`，并且它的值不能等于 `0`。

下面的例子给出了区间类型的实例化方式（关于区间类型定义和其中的属性，详见《仓颉编程语言库 API》）：

<!-- compile -->

```cangjie
// Range<T>(start: T, end: T, step: Int64, hasStart: Bool, hasEnd: Bool, isClosed: Bool)
let r1 = Range<Int64>(0, 10, 1, true, true, true) // r1 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
let r2 = Range<Int64>(0, 10, 1, true, true, false) // r2 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
let r3 = Range<Int64>(10, 0, -2, true, true, false) // r3 contains 10, 8, 6, 4, 2
```

## 区间类型字面量

区间字面量有两种形式：“左闭右开”区间和“左闭右闭”区间。

- “左闭右开”区间的格式是 `start..end : step`，它表示一个从 `start` 开始，以 `step` 为步长，到 `end`（不包含 `end`）为止的区间；
- “左闭右闭”区间的格式是 `start..=end : step`，它表示一个从 `start` 开始，以 `step` 为步长，到 `end`（包含 `end`）为止的区间。

下面的例子定义了若干区间类型的变量：

<!-- compile -->

```cangjie
let n = 10
let r1 = 0..10 : 1   // r1 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
let r2 = 0..=n : 1   // r2 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
let r3 = n..0 : -2   // r3 contains 10, 8, 6, 4, 2
let r4 = 10..=0 : -2 // r4 contains 10, 8, 6, 4, 2, 0
```

区间字面量中，可以不写 `step`，此时 `step` 默认等于 `1`，但是`step` 的值不能等于 `0`。另外，区间也有可能是空的（即不包含任何元素的空序列），举例如下：
<!-- compile.error -->

```cangjie
let r5 = 0..10   // the step of r5 is 1, and r5 contains 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
let r6 = 0..10 : 0 // Error, step cannot be 0

let r7 = 10..0 : 1 // r7 to r10 are empty ranges
let r8 = 0..10 : -1
let r9 = 10..=0 : 1
let r10 = 0..=10 : -1
```

> **注意：**
>
> - 表达式 `start..end : step` 中，当 `step > 0` 且 `start >= end`，或者 `step < 0` 且 `start <= end` 时，`start..end : step` 是一个空区间；
> - 表达式 `start..=end : step` 中，当 `step > 0` 且 `start > end`，或者 `step < 0` 且 `start < end` 时，`start..=end : step` 是一个空区间。
