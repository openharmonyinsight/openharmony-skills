# 操作符函数

下表列出了仓颉支持的所有操作符函数。

| 操作符函数               | 函数签名                                                           | 示例                                  |
|:--------------------|:---------------------------------------------------------------|:------------------------------------|
| `[]`   **（索引取值）**   | `operator func [](index1: T1, index2: T2, ...): R`             | `this[index1, index2, ...]`         |
| `[]`   **（索引赋值）**   | `operator func [](index1: T1, index2: T2, ..., value!: TN): R` | `this[index1, index2, ...] = value` |
| `()`                | `operator func ()(param1: T1, param2: T2, ...): R`             | `this(param1, param2, ...)`         |
| `!`                 | `operator func !(): R`                                         | `!this`                             |
| `**`                | `operator func **(other: T): R`                                | `this ** other`                     |
| `*`                 | `operator func *(other: T): R`                                 | `this * other`                      |
| `/`                 | `operator func /(other: T): R`                                 | `this / other`                      |
| `%`                 | `operator func %(other: T): R`                                 | `this % other`                      |
| `+`                 | `operator func +(other: T): R`                                 | `this + other`                      |
| `-`                 | `operator func -(other: T): R`                                 | `this - other`                      |
| `<<`                | `operator func <<(other: T): R`                                | `this << other`                     |
| `>>`                | `operator func >>(other: T): R`                                | `this >> other`                     |
| `<`                 | `operator func <(other: T): R`                                 | `this < other`                      |
| `<=`                | `operator func <=(other: T): R`                                | `this <= other`                     |
| `>`                 | `operator func >(other: T): R`                                 | `this > other`                      |
| `>=`                | `operator func >=(other: T): R`                                | `this >= other`                     |
| `==`                | `operator func ==(other: T): R`                                | `this == other`                     |
| `!=`                | `operator func !=(other: T): R`                                | `this != other`                     |
| `&`                 | `operator func &(other: T): R`                                 | `this & other`                      |
| `^`                 | `operator func ^(other: T): R`                                 | `this ^ other`                      |
| <code>&vert;</code> | <code>operator func &vert;(other: T): R</code>                 | <code>this &vert; other</code>      |
