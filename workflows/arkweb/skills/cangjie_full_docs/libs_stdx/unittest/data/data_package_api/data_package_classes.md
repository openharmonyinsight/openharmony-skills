# 类

## class CsvStrategy

```cangjie
public class CsvStrategy<T> <: DataStrategy<T> where T <: Serializable<T> {}
```

功能：DataStrategy 对 CSV 数据格式的序列化实现。

父类型：

- DataStrategy\<T>

### func provider(Configuration)

```cangjie
public override func provider(configuration: Configuration): SerializableProvider<T>
```

功能：生成序列化数据迭代器。

参数：

- configuration: Configuration - 数据配置信息。

返回值：

- [SerializableProvider](#class-serializableprovider)\<T> - 序列化迭代器对象。

## class JsonStrategy

```cangjie
public class JsonStrategy<T> <: DataStrategy<T> where T <: Serializable<T> {}
```

功能：DataStrategy 对 JSON 数据格式的序列化实现。

父类型：

- DataStrategy\<T>

### func provider(Configuration)

```cangjie
public override func provider(configuration: Configuration): SerializableProvider<T>
```

功能：生成序列化数据迭代器。

参数：

- configuration: Configuration - 数据配置信息。

返回值：

- SerializableProvider\<T> - 序列化迭代器对象。

## class SerializableProvider

```cangjie
public class SerializableProvider<T> <: DataProvider<T> where T <: Serializable<T> {}
```

功能：获取序列化数据 DataProvider 接口的实现。

父类型：

- DataProvider\<T>

### prop isInfinite

```cangjie
public prop isInfinite: Bool
```

功能：是否生成无限的数据。

Bool。

### func provide()

```cangjie
public override func provide(): Iterable<T> 
```

功能：获取数据迭代器。

返回值：

- Iterable\<T> - 数据迭代器。
