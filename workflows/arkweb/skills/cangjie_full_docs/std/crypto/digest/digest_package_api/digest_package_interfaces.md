# 接口

## interface Digest

```cangjie
public interface Digest {
    prop size: Int64
    prop blockSize: Int64
    prop algorithm: String
    func write(buffer: Array<Byte>): Unit
    func finish(to!: Array<Byte>): Unit
    func finish(): Array<Byte>
    func reset(): Unit
}
```

功能：摘要算法接口，继承该接口的 class、interface、struct 也需要遵守该接口中函数的入参及返回值定义。

### prop algorithm

```cangjie
prop algorithm: String
```

功能：获取摘要算法的算法名称。

类型：[String](../../../core/core_package_api/core_package_structs.md#struct-string)

### prop blockSize

```cangjie
prop blockSize: Int64
```

功能：返回 [Block](../../../ast/ast_package_api/ast_package_classes.md#class-block) 块长度，单位字节。

类型：[Int64](../../../core/core_package_api/core_package_intrinsics.md#int64)

### prop size

```cangjie
prop size: Int64
```

功能：返回生成的摘要信息长度，单位字节。

类型：[Int64](../../../core/core_package_api/core_package_intrinsics.md#int64)

### func finish()

```cangjie
func finish(): Array<Byte>
```

功能：返回生成的 digest 值。

返回值：

- [Array](../../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../../core/core_package_api/core_package_types.md#type-byte)> - 返回生成摘要值。

### func finish(Array\<Byte>)

```cangjie
func finish(to!: Array<Byte>): Unit
```

功能：获取生成的信息摘要值，注意调用 finish 后不可以再进行摘要计算，如重新计算需要 reset 重置上下文。

参数：

- to!: [Array](../../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../../core/core_package_api/core_package_types.md#type-byte)> - 目标数组。

### func reset()

```cangjie
func reset(): Unit
```

功能：重置 digest 对象到初始状态。

### func write(Array\<Byte>)

```cangjie
func write(buffer: Array<Byte>): Unit
```

功能：使用给定的 buffer 更新 digest 对象。

参数：

- buffer: [Array](../../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../../core/core_package_api/core_package_types.md#type-byte)> - 给定的数组。
