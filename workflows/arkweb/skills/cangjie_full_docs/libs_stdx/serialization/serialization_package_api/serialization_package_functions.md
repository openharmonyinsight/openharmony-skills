# 函数

## func field\<T>(String, T) where T <: Serializable\<T>

```cangjie
public func field<T>(name: String, data: T) : Field where T <: Serializable<T>
```

功能：此函数用于将一组数据 `name` 和 `data` 封装到 [Field](serialization_package_classes.md#class-field) 对象中。处理一组数据 `name` 和 `data`，将 `data` 序列化为 [DataModel](serialization_package_classes.md#class-datamodel) 类型，并将二者封装到 [Field](serialization_package_classes.md#class-field) 对象中。

参数：

- name: String - String 类型，`name` 字段为 `""` 时行为与为其它字符串时一致。
- data: T - `T` 类型，`T` 类型必须实现 [Serializable](serialization_package_interfaces.md#interface-serializable)\<T> 接口。

返回值：

- [Field](serialization_package_classes.md#class-field) - 封装了 `name` 和 `data` 的 [Field](serialization_package_classes.md#class-field) 对象。
