# 泛型枚举

在仓颉编程语言的泛型 enum 类型设计中，`Option` 类型是一个典型的示例，关于 `Option` 详细描述请参见 [Option 类型](../enum_and_pattern_match/option_type.md)章节。 `Option` 类型用于表示在某一类型上的值可能是个空的值。这样，`Option` 就可以用来表示在某种类型上计算的失败。这里是何种类型上的失败是不确定的，所以很明显，`Option` 是一个泛型类型，需要声明类型形参。

```cangjie
package std.core // `Option` is defined in std.core.

public enum Option<T> {
      Some(T)
    | None

    public func getOrThrow(): T {
        match (this) {
            case Some(v) => v
            case None => throw NoneValueException()
        }
    }
    // ...
}
```

可以看到，`Option<T>` 分成两种情况，一种是 `Some(T)`，用来表示一个有值的返回结果，另一种是 `None` 用来表示一个空的结果。其中的 `getOrThrow` 函数会是将 `Some(T)` 内部的值返回出来的函数，返回的结果就是 `T` 类型，而如果参数是 None，那么直接抛出异常。

例如，如果想定义一个安全的除法，因为在除法上的计算是可能失败的。如果除数为 0，那么返回 `None` ，否则返回一个用 `Some` 包装过的结果：

<!-- compile -->

```cangjie
func safeDiv(a: Int64, b: Int64): Option<Int64> {
    var res: Option<Int64> = match (b) {
                case 0 => None
                case _ => Some(a/b)
            }
    return res
}
```

这样，在除数为 0 时，程序运行的过程中不会因除以 0 而抛出算术运算异常。
