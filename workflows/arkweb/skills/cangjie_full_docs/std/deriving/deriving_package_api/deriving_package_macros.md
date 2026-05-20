# 宏

## `@Derive` 宏

功能：`Derive` 是一个核心宏，其仅可修饰结构体、类或枚举等声明，对被修饰的声明[自动扩展接口](../deriving_samples/deriving_user_guide.md)。

## `@DeriveExclude` 宏

功能：`DeriveExclude` 可为已被 [@Derive 宏](#derive-宏)修饰的声明[排除不需要处理的字段](../deriving_samples/deriving_user_guide.md#包含和排除)，字段默认被 Deriving 处理。

## `@DeriveInclude` 宏

功能：`DeriveInclude` 可为已被 [@Derive 宏](#derive-宏)修饰的声明[增加需要处理的属性](../deriving_samples/deriving_user_guide.md#包含和排除)，属性默认情况不会被 Deriving 处理。

## `@DeriveOrder` 宏

功能：`DeriveOrder` 可为已被 [@Derive 宏](#derive-宏)修饰的声明[指定处理字段和属性的顺序](../deriving_samples/deriving_user_guide.md#变更顺序)，通常对 `Comparable` 接口有意义。
