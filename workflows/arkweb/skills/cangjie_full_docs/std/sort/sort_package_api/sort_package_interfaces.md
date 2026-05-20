# 接口

## interface SortByExtension\<T> <sup>(deprecated)</sup>

```cangjie
public interface SortByExtension<T> {
    func sortBy(comparator!: (T, T) -> Ordering): Unit
    func sortBy(stable!: Bool, comparator!: (T, T) -> Ordering): Unit
}
```

功能：此接口作为排序相关的辅助接口，通过传入的比较函数，根据其返回值 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) 类型的结果，可对 T 进行自定义排序。

> **注意：**
>
> 未来版本即将废弃。

### func sortBy((T, T) -> Ordering) <sup>(deprecated)</sup>

```cangjie
func sortBy(comparator!: (T, T) -> Ordering): Unit
```

功能：通过传入的比较函数，根据其返回值 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) 类型的结果，可对 T 进行自定义排序。

> **注意：**
>
> 未来版本即将废弃。

参数：

- comparator!: (T, T) ->[Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) - 用户传入的比较函数。

### func sortBy(Bool, (T, T) -> Ordering) <sup>(deprecated)</sup>

```cangjie
func sortBy(stable!: Bool, comparator!: (T, T) -> Ordering): Unit
```

功能：通过传入的比较函数，根据其返回值 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) 类型的结果和稳定排序标志位，可对 T 进行自定义排序。

> **注意：**
>
> 未来版本即将废弃。

参数：

- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序。
- comparator!: (T, T) ->[Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) - 用户传入的比较函数。

> **注意：**
>
> 未来版本即将废弃。

### extend\<T> Array\<T> <: SortByExtension\<T> <sup>(deprecated)</sup>

```cangjie
extend<T> Array<T> <: SortByExtension<T>
```

功能：此扩展用于实现 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt) 的 `sortBy` 函数。

> **注意：**
>
> 未来版本即将废弃。

父类型：

- [SortByExtension](sort_package_interfaces.md#interface-sortbyextensiont-deprecated)

#### func sortBy((T, T) -> Ordering) <sup>(deprecated)</sup>

```cangjie
public func sortBy(comparator!: (T, T) -> Ordering): Unit
```

功能：通过传入的比较函数，根据其返回值 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) 类型的结果，可对数组进行自定义排序。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-t-t---ordering-bool-bool) 替代。

参数：

- comparator!: (T, T) ->[Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) - 用户传入的比较函数，如，comparator: (t1: T, t2: T) -> [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering)，如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).GT，排序后 `t1` 在 `t2` 后；如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).LT，排序后 `t1` 在 `t2` 前；如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).EQ，且为稳定排序那么 `t1` 与 `t2` 的位置较排序前保持不变； 如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).EQ，且为不稳定排序，那么 `t1`，`t2` 顺序不确定。

#### func sortBy(Bool, (T, T) -> Ordering) <sup>(deprecated)</sup>

```cangjie
public func sortBy(stable!: Bool, comparator!: (T, T) -> Ordering): Unit
```

功能：通过传入的比较函数，根据其返回值 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) 类型的结果，可对数组进行自定义排序。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-t-t---ordering-bool-bool) 替代。

参数：

- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序。
- comparator!: (T, T) ->[Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering) - 用户传入的比较函数，如，comparator: (t1: T, t2: T) -> [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering)，如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).GT，排序后 `t1` 在 `t2` 后；如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).LT，排序后 `t1` 在 `t2` 前；如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).EQ，且为稳定排序那么 `t1` 与 `t2` 的位置较排序前保持不变； 如果 `comparator` 的返回值为 [Ordering](../../core/core_package_api/core_package_enums.md#enum-ordering).EQ，且为不稳定排序，那么 `t1`，`t2` 顺序不确定。

## interface SortExtension <sup>(deprecated)</sup>

```cangjie
public interface SortExtension {
    func sort(): Unit
    func sort(stable!: Bool): Unit
    func sortDescending(): Unit
    func sortDescending(stable!: Bool): Unit
}
```

功能：此接口作为排序相关的辅助接口。

### func sort() <sup>(deprecated)</sup>

```cangjie
func sort(): Unit
```

功能：实现对应类型的排序。

> **注意：**
>
> 未来版本即将废弃。

### func sort(Bool) <sup>(deprecated)</sup>

```cangjie
func sort(stable!: Bool): Unit
```

功能：依据传入的参数，实现对应类型的稳定或非稳定排序。

> **注意：**
>
> 未来版本即将废弃。

参数：

- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序。

### func sortDescending() <sup>(deprecated)</sup>

```cangjie
func sortDescending(): Unit
```

功能：实现对应类型的降序方式排序。

> **注意：**
>
> 未来版本即将废弃。

### func sortDescending(Bool) <sup>(deprecated)</sup>

```cangjie
func sortDescending(stable!: Bool): Unit
```

功能：依据传入的参数，实现对应类型的稳定或非稳定降序排序。

参数：

- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序。

> **注意：**
>
> 未来版本即将废弃。

### extend\<T> Array\<T> <: SortExtension where T <: Comparable\<T> <sup>(deprecated)</sup>

```cangjie
extend<T> Array<T> <: SortExtension where T <: Comparable<T>
```

功能：此扩展用于实现 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt) 的 `sort/sortDescending` 函数。

> **注意：**
>
> 未来版本即将废弃。

父类型：

- [SortExtension](sort_package_interfaces.md#interface-sortextension-deprecated)

#### func sort() <sup>(deprecated)</sup>

```cangjie
public func sort(): Unit
```

功能：以升序的方式非稳定排序 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-bool-bool-where-t--comparablet) 替代。

#### func sort(Bool) <sup>(deprecated)</sup>

```cangjie
public func sort(stable!: Bool): Unit
```

功能：以升序的方式排序 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-bool-bool-where-t--comparablet) 替代。

参数：

- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序。

#### func sortDescending() <sup>(deprecated)</sup>

```cangjie
public func sortDescending(): Unit
```

功能：以降序的方式排序 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-bool-bool-where-t--comparablet) 替代。

#### func sortDescending(Bool) <sup>(deprecated)</sup>

```cangjie
public func sortDescending(stable!: Bool): Unit
```

功能：以降序的方式排序 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)。

> **注意：**
>
> 未来版本即将废弃，使用 [sort](sort_package_funcs.md#func-sorttarrayt-bool-bool-where-t--comparablet) 替代。

参数：

- stable!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否使用稳定排序。
