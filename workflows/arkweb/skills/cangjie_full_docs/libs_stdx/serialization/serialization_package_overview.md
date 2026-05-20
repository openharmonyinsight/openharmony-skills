# stdx.serialization.serialization

## 功能介绍

serialization 包提供了序列化和反序列化的能力。

序列化（serialization）是指将数据结构或对象状态转换成可取用格式（例如存成文件形式，存于缓冲，或经由网络中发送），以留待后续在相同或另一台计算机环境中，能恢复原先状态的过程。相对地，从一系列字节提取数据结构的反向操作，即反序列化（deserialization）。

用户定义的类型，可以通过实现 `Serializable` 接口，来支持序列化和反序列化。

## API 列表

### 函数

| 函数名                                                       | 功能                                                    |
| ------------------------------------------------------------ | ------------------------------------------------------- |
| [field\<T>(String, T)](./serialization_package_api/serialization_package_functions.md#func-fieldtstring-t-where-t--serializablet) | 用于将一组数据 `name` 和 `data` 封装到 `Field` 对象中。 |

### 接口

| 接口名                                                       | 功能             |
| ------------------------------------------------------------ | ---------------- |
| [Serializable](./serialization_package_api/serialization_package_interfaces.md#interface-serializable) | 用于规范序列化。 |

### 类

| 类名                                                         | 功能                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [DataModel](./serialization_package_api/serialization_package_classes.md#class-datamodel) | 中间数据层。                                                 |
| [DataModelBool](./serialization_package_api/serialization_package_classes.md#class-datamodelbool) | 此类为 `DataModel` 的子类，实现对 `Bool` 类型数据的封装。    |
| [DataModelFloat](./serialization_package_api/serialization_package_classes.md#class-datamodelfloat) | 此类为 `DataModel` 的子类，实现对 `Float64` 类型数据的封装。 |
| [DataModelInt](./serialization_package_api/serialization_package_classes.md#class-datamodelint) | 此类为 `DataModel` 的子类，实现对 `Int64` 类型数据的封装。   |
| [DataModelNull](./serialization_package_api/serialization_package_classes.md#class-datamodelnull) | 此类为 `DataModel` 的子类，实现对 `Null` 类型数据的封装。    |
| [DataModelSeq](./serialization_package_api/serialization_package_classes.md#class-datamodelseq) | 此类为 `DataModel` 的子类，实现对 ArrayList\<DataModel> 类型数据的封装。 |
| [DataModelString](./serialization_package_api/serialization_package_classes.md#class-datamodelstring) | 此类为 `DataModel` 的子类，实现对 `String` 类型数据的封装。  |
| [DataModelStruct](./serialization_package_api/serialization_package_classes.md#class-datamodelstruct) | 此类为 `DataModel` 的子类，用来实现 `class` 对象到 `DataModel` 的转换。 |
| [Field](./serialization_package_api/serialization_package_classes.md#class-field) | 用于存储 `DataModelStruct` 的元素。                          |

### 异常类

| 异常类名                                                     | 功能                   |
| ------------------------------------------------------------ | ---------------------- |
| [DataModelException](./serialization_package_api/serialization_package_exceptions.md#class-datamodelexception) | `DataModel` 的异常类。 |