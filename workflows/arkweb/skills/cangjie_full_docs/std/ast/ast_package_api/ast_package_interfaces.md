# 接口

## interface ToBytes

```cangjie
public interface ToBytes {
    func toBytes(): Array<UInt8>
}
```

功能：提供对应类型的序列化功能。

### func toBytes()

```cangjie
func toBytes(): Array<UInt8>
```

功能：提供对应类型的序列化功能。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 序列化后的字节序列。

## interface ToTokens

```cangjie
public interface ToTokens {
    func toTokens(): Tokens
}
```

功能：实现对应类型的实例到 [Tokens](ast_package_classes.md#class-tokens) 类型转换的接口，作为支持 `quote` 插值操作必须实现的接口。

### func toTokens()

```cangjie
func toTokens(): Tokens
```

功能：实现对应类型的实例到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend\<T> Array\<T> <: ToTokens

```cangjie
extend<T> Array<T> <: ToTokens
```

功能：实现 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换，仅支持数值类型、[Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型、[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型、[String](../../core/core_package_api/core_package_structs.md#struct-string) 类型。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend\<T> ArrayList\<T> <: ToTokens

```cangjie
extend<T> ArrayList<T> <: ToTokens
```

功能：实现 [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt)\<T> 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [ArrayList](../../collection/collection_package_api/collection_package_class.md#class-arraylistt) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换，目前支持的类型有 [Decl](ast_package_classes.md#class-decl)、[Node](ast_package_classes.md#class-node)、[Constructor](ast_package_classes.md#class-constructor)、[Argument](ast_package_classes.md#class-argument)、[FuncParam](ast_package_classes.md#class-funcparam)、[MatchCase](ast_package_classes.md#class-matchcase)、[Modifier](ast_package_classes.md#class-modifier)、[Annotation](ast_package_classes.md#class-annotation)、[ImportList](ast_package_classes.md#class-importlist)、[Pattern](ast_package_classes.md#class-pattern)、[TypeNode](ast_package_classes.md#class-typenode) 等。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Bool <: ToTokens

```cangjie
extend Bool <: ToTokens
```

功能：实现 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Float16 <: ToTokens

```cangjie
extend Float16 <: ToTokens
```

功能：实现 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Float16](../../core/core_package_api/core_package_intrinsics.md#float16) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Float32 <: ToTokens

```cangjie
extend Float32 <: ToTokens
```

功能：实现 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Float64 <: ToTokens

```cangjie
extend Float64 <: ToTokens
```

功能：实现 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Int16 <: ToTokens

```cangjie
extend Int16 <: ToTokens
```

功能：实现 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Int32 <: ToTokens

```cangjie
extend Int32 <: ToTokens
```

功能：实现 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Int64 <: ToTokens

```cangjie
extend Int64 <: ToTokens
```

功能：实现 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Int8 <: ToTokens

```cangjie
extend Int8 <: ToTokens
```

功能：实现 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Rune <: ToTokens

```cangjie
extend Rune <: ToTokens
```

功能：实现 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Rune](../../core/core_package_api/core_package_intrinsics.md#rune) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend String <: ToTokens

```cangjie
extend String <: ToTokens
```

功能：实现 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Token <: ToTokens

```cangjie
extend Token <: ToTokens
```

功能：实现 [Token](ast_package_structs.md#struct-token) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Token](ast_package_structs.md#struct-token) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend Tokens <: ToTokens

```cangjie
extend Tokens <: ToTokens
```

功能：实现 [Tokens](ast_package_classes.md#class-tokens) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [Tokens](ast_package_classes.md#class-tokens) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend UInt16 <: ToTokens

```cangjie
extend UInt16 <: ToTokens
```

功能：实现 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [UInt16](../../core/core_package_api/core_package_intrinsics.md#uint16) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend UInt32 <: ToTokens

```cangjie
extend UInt32 <: ToTokens
```

功能：实现 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend UInt64 <: ToTokens

```cangjie
extend UInt64 <: ToTokens
```

功能：实现 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [UInt64](../../core/core_package_api/core_package_intrinsics.md#uint64) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。

### extend UInt8 <: ToTokens

```cangjie
extend UInt8 <: ToTokens
```

功能：实现 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

父类型：

- [ToTokens](#interface-totokens)

#### func toTokens()

```cangjie
public func toTokens(): Tokens
```

功能：实现 [UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8) 类型到 [Tokens](ast_package_classes.md#class-tokens) 类型的转换。

返回值：

- [Tokens](ast_package_classes.md#class-tokens) - 转换后的 [Tokens](ast_package_classes.md#class-tokens)。
