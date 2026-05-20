# 接口

## interface Serializable

```cangjie
public interface Serializable<T> {
    func serialize(): DataModel
    static func deserialize(dm: DataModel): T
}
```

功能：用于规范序列化。

### static func deserialize(DataModel)

```cangjie
static func deserialize(dm: DataModel): T
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为对象。

> **说明：**
>
> 支持实现 [Serializable](serialization_package_interfaces.md#interface-serializable) 的类型包括：
>
> - 基本数据类型：整数类型、浮点类型、布尔类型、字符类型、字符串类型。
> - Collection 类型：Array、ArrayList、HashSet、HashMap、Option。
> - 用户自定义的实现了 [Serializable](serialization_package_interfaces.md#interface-serializable)\<T> 的类型。

参数：

- dm: [DataModel](./serialization_package_classes.md#class-datamodel) - 待反序列化的数据。

返回值：

- T - 反序列化的对象。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不支持反序列化到 T 类型时，抛出异常。

### func serialize()

```cangjie
func serialize(): DataModel
```

功能：将自身序列化为 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

### extend\<T> Array\<T> <: Serializable\<Array\<T>> where T <: Serializable\<T>

```cangjie
extend<T> Array<T> <: Serializable<Array<T>> where T <: Serializable<T>
```

功能：为 Array\<T> 类型实现 [Serializable](#interface-serializable)\<Array\<T>> 接口。

父类型：

- [Serializable](#interface-serializable)\<Array\<T>>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Array<T>
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Array\<T>。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Array\<T> - 反序列化后的 Array\<T>。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelSeq](serialization_package_classes.md#class-datamodelseq) 时，则抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Array\<T> 序列化为 [DataModelSeq](serialization_package_classes.md#class-datamodelseq)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelSeq](serialization_package_classes.md#class-datamodelseq)。

### extend\<T> ArrayList\<T> <: Serializable\<ArrayList\<T>> where T <: Serializable\<T>

```cangjie
extend<T> ArrayList<T> <: Serializable<ArrayList<T>> where T <: Serializable<T>
```

功能：为 ArrayList\<T> 类型实现 [Serializable](#interface-serializable)\<ArrayList\<T>> 接口。

父类型：

- [Serializable](#interface-serializable)\<ArrayList\<T>>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): ArrayList<T>
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 ArrayList\<T>。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- ArrayList\<T> - 反序列化后的 ArrayList\<T>。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelSeq](serialization_package_classes.md#class-datamodelseq) 时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 ArrayList\<T> 序列化为 [DataModelSeq](serialization_package_classes.md#class-datamodelseq)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelSeq](serialization_package_classes.md#class-datamodelseq)。

### extend Bool <: Serializable

```cangjie
extend Bool <: Serializable<Bool>
```

功能：为 Bool 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<Bool>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Bool
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Bool。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Bool - 反序列化后的 Bool。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelBool](serialization_package_classes.md#class-datamodelbool) 时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Bool 序列化为 [DataModelBool](serialization_package_classes.md#class-datamodelbool)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelBool](serialization_package_classes.md#class-datamodelbool)。

### extend Float16 <: Serializable

```cangjie
extend Float16 <: Serializable<Float16>
```

功能：为 Float16 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<Float16>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Float16
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Float16。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Float16 - 反序列化后的 Float16。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat) 或者 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Float16 序列化为 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat)。

### extend Float32 <: Serializable

```cangjie
extend Float32 <: Serializable<Float32>
```

功能：为 Float32 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<Float32>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Float32
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Float32。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Float32 - 反序列化后的 Float32。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat) 或者 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Float32 序列化为 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat)。

### extend Float64 <: Serializable

```cangjie
extend Float64 <: Serializable<Float64>
```

功能：为 Float64 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<Float64>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Float64
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Float64。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Float64 - 反序列化后的 Float64。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat) 或者 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Float64 序列化为 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat)。

### extend\<K, V> HashMap\<K, V> <: Serializable\<HashMap\<K, V>> where K <: Serializable\<K> & Hashable & Equatable\<K>, V <: Serializable\<V>

```cangjie
extend<K, V> HashMap<K, V> <: Serializable<HashMap<K, V>> where K <: Serializable<K> & Hashable & Equatable<K>, V <: Serializable<V>
```

功能：为 HashMap\<K, V> 类型实现 [Serializable](#interface-serializable)\<HashMap\<K, V>> 接口。

父类型：

- [Serializable](#interface-serializable)\<HashMap\<K, V>>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): HashMap<K, V>
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 HashMap\<K, V>。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- HashMap\<K, V> - 反序列化后的 HashMap\<K, V>。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 不是 [DataModelStruct](serialization_package_classes.md#class-datamodelstruct) 类型，或者 [DataModelStruct](serialization_package_classes.md#class-datamodelstruct) 类型的 `dm` 中的 [Field](serialization_package_classes.md#class-field) 不是 String 类型时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 HashMap\<K, V> 序列化为 [DataModelSeq](serialization_package_classes.md#class-datamodelseq)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelSeq](serialization_package_classes.md#class-datamodelseq)。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当前 HashMap 实例中的 Key 不是 String 类型时，抛出异常。

### extend\<T> HashSet\<T> <: Serializable\<HashSet\<T>> where T <: Serializable\<T> & Hashable & Equatable\<T>

```cangjie
extend<T> HashSet<T> <: Serializable<HashSet<T>> where T <: Serializable<T> & Hashable & Equatable<T>
```

功能：为 HashSet\<T> 类型实现 [Serializable](#interface-serializable)\<HashSet\<T>> 接口。

父类型：

- [Serializable](#interface-serializable)\<HashSet\<T>>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): HashSet<T>
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 HashSet\<T>。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- HashSet\<T> - 反序列化后的 HashSet\<T>。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelSeq](serialization_package_classes.md#class-datamodelseq) 时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 HashSet\<T> 序列化为 [DataModelSeq](serialization_package_classes.md#class-datamodelseq)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelSeq](serialization_package_classes.md#class-datamodelseq)。

### extend Int16 <: Serializable

```cangjie
extend Int16 <: Serializable<Int16>
```

功能：为 Int16 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<Int16>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Int16
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Int16。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Int16 - 反序列化后的 Int16。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，则抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Int16 序列化为 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

### extend Int32 <: Serializable

```cangjie
extend Int32 <: Serializable<Int32>
```

功能：为 Int32 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<Int32>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Int32
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Int32。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Int32 - 反序列化后的 Int32。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，抛出异常

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Int32 序列化为 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

### extend Int64 <: Serializable

```cangjie
extend Int64 <: Serializable<Int64>
```

功能：为 Int64 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<Int64>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Int64
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Int64。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Int64 - 反序列化后的 Int64。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Int64 序列化为 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

### extend Int8 <: Serializable

```cangjie
extend Int8 <: Serializable<Int8>
```

功能：为 Int8 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<Int8>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Int8
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Int8。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Int8 - 反序列化后的 Int8。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Int8 序列化为 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

### extend\<T> Option\<T> <: Serializable\<Option\<T>> where T <: Serializable\<T>

```cangjie
extend<T> Option<T> <: Serializable<Option<T>> where T <: Serializable<T>
```

功能：为 Option\<T> 类型实现 [Serializable](#interface-serializable)\<Option\<T>> 接口。

父类型：

- [Serializable](#interface-serializable)\<Option\<T>>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Option<T>
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Option\<T>。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Option\<T> - 反序列化后的 Option\<T>。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不支持反序列化到 T 类型时，抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Option\<T> 中的 `T` 序列化为 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

### extend Rune <: Serializable

```cangjie
extend Rune <: Serializable<Rune>
```

功能：为 Rune 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<Rune>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): Rune
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 Rune。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- Rune - 反序列化后的字符。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelString](serialization_package_classes.md#class-datamodelstring) 时，则抛出此异常。
- Exception - 当 `dm` 的类型不是 Rune 时，则抛出此异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 Rune 序列化为 [DataModelString](serialization_package_classes.md#class-datamodelstring)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelString](serialization_package_classes.md#class-datamodelstring)。

### extend String <: Serializable

```cangjie
extend String <: Serializable<String>
```

功能：为 String 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<String>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): String
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 String。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- String - 反序列化后的 String。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelString](serialization_package_classes.md#class-datamodelstring) 时，则抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 String 序列化为 [DataModelString](serialization_package_classes.md#class-datamodelstring)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelString](serialization_package_classes.md#class-datamodelstring)。

### extend UInt16 <: Serializable

```cangjie
extend UInt16 <: Serializable<UInt16>
```

功能：为 UInt16 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<UInt16>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): UInt16
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 UInt16。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- UInt16 - 反序列化后的 UInt16。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，则抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 UInt16 序列化为 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

### extend UInt32 <: Serializable

```cangjie
extend UInt32 <: Serializable<UInt32>
```

功能：为 UInt32 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<UInt32>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): UInt32
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 UInt32。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- UInt32 - 反序列化后的 UInt32。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，则抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 UInt32 序列化为 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

### extend UInt64 <: Serializable

```cangjie
extend UInt64 <: Serializable<UInt64>
```

功能：为 UInt64 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<UInt64>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): UInt64
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 UInt64。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- UInt64 - 反序列化后的 UInt64。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，则抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 UInt64 序列化为 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

### extend UInt8 <: Serializable

```cangjie
extend UInt8 <: Serializable<UInt8>
```

功能：为 UInt8 类型实现 [Serializable](#interface-serializable) 接口。

父类型：

- [Serializable](#interface-serializable)\<UInt8>

#### static func deserialize(DataModel)

```cangjie
public static func deserialize(dm: DataModel): UInt8
```

功能：将 [DataModel](serialization_package_classes.md#class-datamodel) 反序列化为 UInt8。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 需要被反序列化的 [DataModel](serialization_package_classes.md#class-datamodel)。

返回值：

- UInt8 - 反序列化后的 UInt8。

异常：

- [DataModelException](serialization_package_exceptions.md#class-datamodelexception) - 当 `dm` 的类型不是 [DataModelInt](serialization_package_classes.md#class-datamodelint) 时，则抛出异常。

#### func serialize()

```cangjie
public func serialize(): DataModel
```

功能：将 UInt8 序列化为 [DataModelInt](serialization_package_classes.md#class-datamodelint)。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 序列化的 [DataModelInt](serialization_package_classes.md#class-datamodelint)。
