# 类

## class DataModel

```cangjie
public abstract class DataModel
```

功能：此类为中间数据层。

## class DataModelBool

```cangjie
public class DataModelBool <: DataModel {
    public init(bv: Bool)
}
```

功能：此类为 [DataModel](serialization_package_classes.md#class-datamodel) 的子类，实现对 Bool 类型数据的封装。

父类型：

- [DataModel](#class-datamodel)

### init(Bool)

```cangjie
public init(bv: Bool)
```

功能：构造一个具有初始数据的 [DataModelBool](serialization_package_classes.md#class-datamodelbool) 实例。

参数：

- bv: Bool - 传入的 Bool 类型的数据。

### func getValue()

```cangjie
public func getValue(): Bool
```

功能：获取 [DataModelBool](serialization_package_classes.md#class-datamodelbool) 中的数据。

返回值：

- Bool - [DataModelBool](serialization_package_classes.md#class-datamodelbool) 中类型为 Bool 的 `value` 数值。

## class DataModelFloat

```cangjie
public class DataModelFloat <: DataModel {
    public init(fv: Float64)
    public init(v: Int64)
}
```

功能：此类为 [DataModel](serialization_package_classes.md#class-datamodel) 的子类，实现对 Float64 类型数据的封装。

父类型：

- [DataModel](#class-datamodel)

### init(Float64)

```cangjie
public init(fv: Float64)
```

功能：构造一个具有初始数据的 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat) 实例。

参数：

- fv: Float64 - 传入的 Float64 类型的数据。

### init(Int64)

```cangjie
public init(v: Int64)
```

功能：构造一个具有初始数据的 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat) 实例。

参数：

- v: Int64 - 传入的 Int64 类型的数据。

### func getValue()

```cangjie
public func getValue(): Float64
```

功能：获取 [DataModelFloat](serialization_package_classes.md#class-datamodelfloat) 中的数据。

返回值：

- Float64 - [DataModelFloat](serialization_package_classes.md#class-datamodelfloat) 中类型为 Float64 的 `value` 数值。

## class DataModelInt

```cangjie
public class DataModelInt <: DataModel {
    public init(iv: Int64)
}
```

功能：此类为 [DataModel](serialization_package_classes.md#class-datamodel) 的子类，实现对 Int64 类型数据的封装。

父类型：

- [DataModel](#class-datamodel)

### init(Int64)

```cangjie
public init(iv: Int64)
```

功能：构造一个具有初始数据的 [DataModelInt](serialization_package_classes.md#class-datamodelint) 实例。

参数：

- iv: Int64 - 传入的 Int64 类型的数据。

### func getValue()

```cangjie
public func getValue(): Int64
```

功能：获取 [DataModelInt](serialization_package_classes.md#class-datamodelint) 中的数据。

返回值：

- Int64 - [DataModelInt](serialization_package_classes.md#class-datamodelint) 中类型为 Int64 的 `value` 数值。

## class DataModelNull

```cangjie
public class DataModelNull <: DataModel
```

功能：此类为 [DataModel](serialization_package_classes.md#class-datamodel) 的子类，实现对 `Null` 类型数据的封装。

父类型：

- [DataModel](#class-datamodel)

## class DataModelSeq

```cangjie
public class DataModelSeq <: DataModel {
    public init()
    public init(list: ArrayList<DataModel>)
}
```

功能：此类为 [DataModel](serialization_package_classes.md#class-datamodel) 的子类，实现对 ArrayList\<[DataModel](serialization_package_classes.md#class-datamodel)> 类型数据的封装。

父类型：

- [DataModel](#class-datamodel)

### init()

```cangjie
public init()
```

功能：构造一个参数为空的 [DataModelSeq](serialization_package_classes.md#class-datamodelseq) 实例。其中的数据默认为空的 ArrayList\<[DataModel](serialization_package_classes.md#class-datamodel)>。

### init(ArrayList\<DataModel>)

```cangjie
public init(list: ArrayList<DataModel>)
```

功能：构造一个具有初始数据的 [DataModelSeq](serialization_package_classes.md#class-datamodelseq) 实例。

参数：

- list: ArrayList\<[DataModel](serialization_package_classes.md#class-datamodel)> - 传入的 ArrayList\<[DataModel](serialization_package_classes.md#class-datamodel)> 类型的数据。

### func add(DataModel)

```cangjie
public func add(dm: DataModel): Unit 
```

功能：在 [DataModelSeq](serialization_package_classes.md#class-datamodelseq) 末尾增加一个 [DataModel](serialization_package_classes.md#class-datamodel) 数据。

参数：

- dm: [DataModel](serialization_package_classes.md#class-datamodel) - 传入的 [DataModel](serialization_package_classes.md#class-datamodel) 类型的数据。

### func getItems()

```cangjie
public func getItems(): ArrayList<DataModel>
```

功能：获取 [DataModelSeq](serialization_package_classes.md#class-datamodelseq) 中的数据。

返回值：

- ArrayList\<[DataModel](serialization_package_classes.md#class-datamodel)> - [DataModelSeq](serialization_package_classes.md#class-datamodelseq) 中的数据，类型为 ArrayList\<[DataModel](serialization_package_classes.md#class-datamodel)>。

## class DataModelString

```cangjie
public class DataModelString <: DataModel {
    public init(sv: String)
}
```

功能：此类为 [DataModel](serialization_package_classes.md#class-datamodel) 的子类，实现对 String 类型数据的封装。

父类型：

- [DataModel](#class-datamodel)

### init(String)

```cangjie
public init(sv: String)
```

功能：构造一个具有初始数据的 [DataModelString](serialization_package_classes.md#class-datamodelstring)。

参数：

- sv: String - 传入的 String 类型。

### func getValue()

```cangjie
public func getValue(): String
```

功能：获取 [DataModelString](serialization_package_classes.md#class-datamodelstring) 中的数据。

返回值：

- String - [DataModelString](serialization_package_classes.md#class-datamodelstring) 中类型为 String 的 `value` 数值。

## class DataModelStruct

```cangjie
public class DataModelStruct <: DataModel {
    public init()
    public init(list: ArrayList<Field>)
}
```

功能：此类为 [DataModel](serialization_package_classes.md#class-datamodel) 的子类，用来实现 `class` 对象到 [DataModel](serialization_package_classes.md#class-datamodel) 的转换。

父类型：

- [DataModel](#class-datamodel)

### init()

```cangjie
public init()
```

功能：构造一个空参的 `DataModelStructfields` 默认为空的 ArrayList\<[Field](serialization_package_classes.md#class-field)>。

### init(ArrayList\<Field>)

```cangjie
public init(list: ArrayList<Field>)
```

功能：构造一个具有初始数据的 [DataModelStruct](serialization_package_classes.md#class-datamodelstruct)。

参数：

- list: ArrayList\<[Field](serialization_package_classes.md#class-field)> - 传入的 ArrayList\<[Field](serialization_package_classes.md#class-field)> 类型的数据。

### func add(Field)

```cangjie
public func add(fie: Field): DataModelStruct
```

功能：添加数据 `fie` 到 [DataModelStruct](serialization_package_classes.md#class-datamodelstruct) 中。

参数：

- fie: [Field](serialization_package_classes.md#class-field) - 传入的 [Field](serialization_package_classes.md#class-field) 类型的数据。

返回值：

- [DataModelStruct](serialization_package_classes.md#class-datamodelstruct) - 得到新的 [DataModelStruct](serialization_package_classes.md#class-datamodelstruct)。

### func get(String)

```cangjie
public func get(key: String): DataModel
```

功能：获取 `key` 对应的数据。

参数：

- key: String - 传入的 String 类型。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 类型为 [DataModel](serialization_package_classes.md#class-datamodel)，如未查找到对应值，则返回 [DataModelNull](serialization_package_classes.md#class-datamodelnull)。

### func getFields()

```cangjie
public func getFields(): ArrayList<Field>
```

功能：获取 [DataModelStruct](serialization_package_classes.md#class-datamodelstruct) 的数据集合。

返回值：

- ArrayList\<[Field](serialization_package_classes.md#class-field)> - 类型为 ArrayList\<[Field](serialization_package_classes.md#class-field)> 的数据集合。

## class Field

```cangjie
public class Field {
    public init(name: String, data: DataModel)
}
```

功能：用于存储 [DataModelStruct](serialization_package_classes.md#class-datamodelstruct) 的元素。

### init(String, DataModel)

```cangjie
public init(name: String, data: DataModel)
```

功能：[Field](serialization_package_classes.md#class-field) 的构造函数。

参数：

- name: String - `name` 字段值，`name` 字段为 `""` 时行为与为其它字符串时一致。
- data: [DataModel](serialization_package_classes.md#class-datamodel) - `data` 字段值。

### func getData()

```cangjie
public func getData(): DataModel
```

功能：获取 `data` 字段。

返回值：

- [DataModel](serialization_package_classes.md#class-datamodel) - 获取到的 `data` 字段，类型为 [DataModel](serialization_package_classes.md#class-datamodel)。

### func getName()

```cangjie
public func getName(): String
```

功能：获取 `name` 字段。

返回值：

- String - 获取到的 `name` 字段，类型为 String。
