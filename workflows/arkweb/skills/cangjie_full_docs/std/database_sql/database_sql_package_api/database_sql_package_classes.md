# 类

## class DriverManager

```cangjie
public class DriverManager {}
```

功能：支持运行时根据驱动名获取数据库驱动实例。

### static func deregister(String)

```cangjie
public static func deregister(driverName: String): Unit
```

功能：按名称取消注册数据库驱动（如果存在）。本函数并发安全。

参数：

- driverName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 驱动名称。

### static func drivers()

```cangjie
public static func drivers(): Array<String>
```

功能：返回已注册数据库驱动名称的列表（名称已按照字典序排序）。本方法并发安全。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 数据库驱动名称的列表。

### static func getDriver(String)

```cangjie
public static func getDriver(driverName: String): Option<Driver>
```

功能：按名称获取已注册的数据库驱动，如果不存在返回 `None`。本函数并发安全。

参数：

- driverName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 驱动名称。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[Driver](database_sql_package_interfaces.md#interface-driver)> - 若驱动存在则返回 [Option](../../core/core_package_api/core_package_enums.md#enum-optiont) 包装的驱动实例，否则返回 `None`。

### static func register(String, Driver)

```cangjie
public static func register(driverName: String, driver: Driver): Unit
```

功能：按名称和驱动实例注册数据库驱动，名称和实例一一对应。本方法并发安全。

参数：

- driverName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 驱动名称。
- driver: [Driver](database_sql_package_interfaces.md#interface-driver) - 驱动实例。

异常：

- [SqlException](database_sql_package_exceptions.md#class-sqlexception) - 当指定的驱动名称已经存在时，抛出异常。

## class PooledDatasource

```cangjie
public class PooledDatasource <: Datasource {
    public init(datasource: Datasource)
}
```

功能：数据库连接池类，提供数据库连接池能力。

父类型：

- [Datasource](database_sql_package_interfaces.md#interface-datasource)

### prop connectionTimeout

```cangjie
public mut prop connectionTimeout: Duration
```

功能：从池中获取连接的超时时间。

类型：[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

异常：

- [ArithmeticException](../../core/core_package_api/core_package_exceptions.md#class-arithmeticexception) - 当该属性被设置为 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration).Max 或 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration).Min 时，抛此异常。
- [SqlException](database_sql_package_exceptions.md#class-sqlexception) - 当获取连接超时后，抛出此异常。

### prop idleTimeout

```cangjie
public mut prop idleTimeout: Duration
```

功能：允许连接在池中闲置的最长时间，超过这个时间的空闲连接可能会被回收。

类型：[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

### prop keepaliveTime

```cangjie
public mut prop keepaliveTime: Duration
```

功能：检查空闲连接健康状况的间隔时间，防止它被数据库或网络基础设施超时。

类型：[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

### prop maxIdleSize

```cangjie
public mut prop maxIdleSize: Int32
```

功能：最大空闲连接数量，超过这个数量的空闲连接会被关闭，负数或 0 表示无限制。

类型：[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)

### prop maxLifeTime

```cangjie
public mut prop maxLifeTime: Duration
```

功能：自连接创建以来的最大持续时间，在该持续时间之后，连接将自动关闭。

类型：[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

### prop maxSize

```cangjie
public mut prop maxSize: Int32
```

功能：连接池最大连接数量，负数或 0 表示无限制。

类型：[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)

### init(Datasource)

```cangjie
public init(datasource: Datasource)
```

功能：通过数据源 datasource 构造一个 [PooledDatasource](database_sql_package_classes.md#class-pooleddatasource) 实例，入参必须为 [Datasource](database_sql_package_interfaces.md#interface-datasource) 对象。

参数：

- datasource: [Datasource](database_sql_package_interfaces.md#interface-datasource) - 数据源。

### func close()

```cangjie
public func close(): Unit
```

功能：关闭连接池中的所有连接并阻止其他连接请求。调用该方法会阻塞至所有连接关闭并归还到连接池。

### func connect()

```cangjie
public func connect(): Connection
```

功能：获取一个连接。

返回值：

- [Connection](./database_sql_package_interfaces.md#interface-connection) - 获取到的连接。

### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：判断连接是否关闭。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 连接是否关闭。

### func setOption(String, String)

```cangjie
public func setOption(key: String, value: String): Unit
```

功能：设置数据库驱动连接选项（公钥在 [SqlOption](database_sql_package_classes.md#class-sqloption) 中预定义）。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 连接选项名称。
- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 连接选项的值。

## class SqlBigInt <sup>(deprecated)</sup>

```cangjie
public class SqlBigInt <: SqlDbType {
    public init(v: Int64)
}
```

功能：大整数，对应仓颉 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlBigInt <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlbigint-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Int64
```

功能：该数据的值。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init(Int64)

```cangjie
public init(v: Int64)
```

功能：根据传入参数 v 构造一个 [SqlBigInt <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlbigint-deprecated) 实例。

参数：

- v: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 传入的数据。

## class SqlBinary <sup>(deprecated)</sup>

```cangjie
public class SqlBinary <: SqlDbType {
    public init(v: Array<Byte>)
}
```

功能：定长二进制字符串，对应仓颉 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlBinary <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlbinary-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Array<Byte>
```

功能：该数据的值。

类型：[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>

### init(Array\<Byte>)

```cangjie
public init(v: Array<Byte>)
```

功能：根据传入参数 v 构造一个 [SqlBinary <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlbinary-deprecated) 实例。

参数：

- v: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 传入的数据。

## class SqlBlob <sup>(deprecated)</sup>

```cangjie
public class SqlBlob <: SqlDbType {
    public init(v: InputStream)
}
```

功能：变长超大二进制字符串（BINARY LARGE OBJECT），对应仓颉 [InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlBlob <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlblob-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: InputStream
```

功能：该数据的值。

类型：[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### init(InputStream)

```cangjie
public init(v: InputStream)
```

功能：根据传入参数 v 构造一个 [SqlBlob <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlblob-deprecated) 实例。

参数：

- v: [InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream) - 传入的数据。

## class SqlBool <sup>(deprecated)</sup>

```cangjie
public class SqlBool <: SqlDbType {
    public init(v: Bool)
}
```

功能：布尔类型，对应仓颉 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlBool<sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlbool-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Bool
```

功能：该数据的值。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

### init(Bool)

```cangjie
public init(v: Bool)
```

功能：根据传入参数 v 构造一个 [SqlBool<sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlbool-deprecated) 实例。

参数：

- v: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 传入的数据。

## class SqlByte <sup>(deprecated)</sup>

```cangjie
public class SqlByte <: SqlDbType {
    public init(v: Int8)
}
```

功能：字节，对应仓颉 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlByte <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlbyte-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Int8
```

功能：该数据的值。

类型：[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)

### init(Int8)

```cangjie
public init(v: Int8)
```

功能：根据传入参数 v 构造一个 [SqlByte <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlbyte-deprecated) 实例。

参数：

- v: [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 传入的数据。

## class SqlChar <sup>(deprecated)</sup>

```cangjie
public class SqlChar <: SqlDbType {
    public init(v: String)
}
```

功能：定长字符串，对应仓颉 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlChar <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlchar-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: String
```

功能：该数据的值。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### init(String)

```cangjie
public init(v: String)
```

功能：根据传入参数 v 构造一个 [SqlChar <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlchar-deprecated) 实例。

参数：

- v: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 传入的数据。

## class SqlClob <sup>(deprecated)</sup>

```cangjie
public class SqlClob <: SqlDbType {
    public init(v: InputStream)
}
```

功能：变长超大字符串（RUNE LARGE OBJECT），对应仓颉 [InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlClob](database_sql_package_classes.md#class-sqlclob-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: InputStream
```

功能：该数据的值。

类型：[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### init(InputStream)

```cangjie
public init(v: InputStream)
```

功能：根据传入参数 v 构造一个 [SqlClob](database_sql_package_classes.md#class-sqlclob-deprecated) 实例。

参数：

- v: [InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream) - 传入的数据。

## class SqlDate <sup>(deprecated)</sup>

```cangjie
public class SqlDate <: SqlDbType {
    public init(v: DateTime)
}
```

功能：日期，仅年月日有效，对应仓颉 [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlDate <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqldate-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: DateTime
```

功能：该数据的值。

类型：[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime)

### init(DateTime)

```cangjie
public init(v: DateTime)
```

功能：根据传入参数 v 构造一个 [SqlDate <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqldate-deprecated) 实例。

参数：

- v: [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) - 传入的数据。

## class SqlDecimal <sup>(deprecated)</sup>

```cangjie
public class SqlDecimal <: SqlDbType {
    public init(v: Decimal)
}
```

功能：高精度数，对应仓颉 [Decimal](../../math_numeric/math_numeric_package_api/math_numeric_package_structs.md#struct-decimal) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlDecimal <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqldecimal-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Decimal
```

功能：该数据的值。

类型：[Decimal](../../math_numeric/math_numeric_package_api/math_numeric_package_structs.md#struct-decimal)

### init(Decimal)

```cangjie
public init(v: Decimal)
```

功能：根据传入参数 v 构造一个 [SqlDecimal <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqldecimal-deprecated) 实例。

参数：

- v: [Decimal](../../math_numeric/math_numeric_package_api/math_numeric_package_structs.md#struct-decimal) - 传入的数据。

## class SqlDouble <sup>(deprecated)</sup>

```cangjie
public class SqlDouble <: SqlDbType {
    public init(v: Float64)
}
```

功能：双精度数，对应仓颉 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlDouble <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqldouble-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Float64
```

功能：该数据的值。

类型：[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)

### init(Float64)

```cangjie
public init(v: Float64)
```

功能：根据传入参数 v 构造一个 [SqlDouble <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqldouble-deprecated) 实例。

参数：

- v: [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 传入的数据。

## class SqlInteger <sup>(deprecated)</sup>

```cangjie
public class SqlInteger <: SqlDbType {
    public init(v: Int32)
}
```

功能：中整数，对应仓颉 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlInteger <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlinteger-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Int32
```

功能：该数据的值。

类型：[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)

### init(Int32)

```cangjie
public init(v: Int32)
```

功能：根据传入参数 v 构造一个 [SqlInteger <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlinteger-deprecated) 实例。

参数：

- v: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 传入的数据。

## class SqlInterval <sup>(deprecated)</sup>

```cangjie
public class SqlInterval <: SqlDbType {
    public init(v: Duration)
}
```

功能：时间间隔，对应仓颉 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlInterval <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlinterval-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Duration
```

功能：该数据的值。

类型：[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

### init(Duration)

```cangjie
public init(v: Duration)
```

功能：根据传入参数 v 构造一个 [SqlInterval <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlinterval-deprecated) 实例。

参数：

- v: [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 传入的数据。

## class SqlNullableBigInt <sup>(deprecated)</sup>

```cangjie
public class SqlNullableBigInt <: SqlNullableDbType {
    public init(v: ?Int64)
}
```

功能：大整数，对应仓颉 [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableBigInt <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablebigint-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Int64
```

功能：该数据的值。

类型：?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init(?Int64)

```cangjie
public init(v: ?Int64)
```

功能：根据传入参数 v 构造一个 [SqlNullableBigInt <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablebigint-deprecated) 实例。

参数：

- v: ?[Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 传入的数据。

## class SqlNullableBinary <sup>(deprecated)</sup>

```cangjie
public class SqlNullableBinary <: SqlNullableDbType {
    public init(v: ?Array<Byte>)
}
```

功能：定长二进制字符串，对应仓颉 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableBinary <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablebinary-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Array<Byte>
```

功能：该数据的值。

类型：?[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>

### init(?Array\<Byte>)

```cangjie
public init(v: ?Array<Byte>)
```

功能：根据传入参数 v 构造一个 [SqlNullableBinary <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablebinary-deprecated) 实例。

参数：

- v: ?[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 传入的数据。

## class SqlNullableBlob <sup>(deprecated)</sup>

```cangjie
public class SqlNullableBlob <: SqlNullableDbType {
    public init(v: ?InputStream)
}
```

功能：变长超大二进制字符串（BINARY LARGE OBJECT），对应仓颉 [InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableBlob <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullableblob-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?InputStream
```

功能：该数据的值。

类型：?[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### init(?InputStream)

```cangjie
public init(v: ?InputStream)
```

功能：根据传入参数 v 构造一个 [SqlNullableBlob <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullableblob-deprecated) 实例。

参数：

- v: ?[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream) - 传入的数据。

## class SqlNullableBool <sup>(deprecated)</sup>

```cangjie
public class SqlNullableBool <: SqlNullableDbType {
    public init(v: ?Bool)
}
```

功能：布尔类型，对应仓颉 [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableBool <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablebool-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Bool
```

功能：该数据的值。

类型：?[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)

### init(?Bool)

```cangjie
public init(v: ?Bool)
```

功能：根据传入参数 v 构造一个 [SqlNullableBool <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablebool-deprecated) 实例。

参数：

- v: ?[Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 传入的数据。

## class SqlNullableByte <sup>(deprecated)</sup>

```cangjie
public class SqlNullableByte <: SqlNullableDbType {
    public init(v: ?Int8)
}
```

功能：字节，对应仓颉 [Int8](../../core/core_package_api/core_package_intrinsics.md#int8) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableByte <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablebyte-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Int8
```

功能：该数据的值。

类型：?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8)

### init(?Int8)

```cangjie
public init(v: ?Int8)
```

功能：根据传入参数 v 构造一个 [SqlNullableByte <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablebyte-deprecated) 实例。

参数：

- v: ?[Int8](../../core/core_package_api/core_package_intrinsics.md#int8) - 传入的数据。

## class SqlNullableChar <sup>(deprecated)</sup>

```cangjie
public class SqlNullableChar <: SqlNullableDbType {
    public init(v: ?String)
}
```

功能：定长字符串，对应仓颉 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableChar <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablechar-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?String
```

功能：该数据的值。

类型：?[String](../../core/core_package_api/core_package_structs.md#struct-string)

### init(?String)

```cangjie
public init(v: ?String)
```

功能：根据传入参数 v 构造一个 [SqlNullableChar <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablechar-deprecated) 实例。

参数：

- v: ?[String](../../core/core_package_api/core_package_structs.md#struct-string) - 传入的数据。

## class SqlNullableClob <sup>(deprecated)</sup>

```cangjie
public class SqlNullableClob <: SqlNullableDbType {
    public init(v: ?InputStream)
}
```

功能：变长超大字符串（RUNE LARGE OBJECT），对应仓颉 [InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableClob <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullableclob-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?InputStream
```

功能：该数据的值。

类型：?[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### init(?InputStream)

```cangjie
public init(v: ?InputStream)
```

功能：根据传入参数 v 构造一个 [SqlNullableClob <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullableclob-deprecated) 实例。

参数：

- v: ?[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream) - 传入的数据。

## class SqlNullableDate <sup>(deprecated)</sup>

```cangjie
public class SqlNullableDate <: SqlNullableDbType {
    public init(v: ?DateTime)
}
```

功能：日期，仅年月日有效，对应仓颉 [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableDate <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabledate-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?DateTime
```

功能：该数据的值。

类型：?[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime)

### init(?DateTime)

```cangjie
public init(v: ?DateTime)
```

功能：根据传入参数 v 构造一个 [SqlNullableDate <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabledate-deprecated) 实例。

参数：

- v: ?[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) - 传入的数据。

## class SqlNullableDecimal <sup>(deprecated)</sup>

```cangjie
public class SqlNullableDecimal <: SqlNullableDbType {
    public init(v: ?Decimal)
}
```

功能：高精度数，对应仓颉 [Decimal](../../math_numeric/math_numeric_package_api/math_numeric_package_structs.md#struct-decimal) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableDecimal <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabledecimal-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Decimal
```

功能：该数据的值。

类型：?[Decimal](../../math_numeric/math_numeric_package_api/math_numeric_package_structs.md#struct-decimal)

### init(?Decimal)

```cangjie
public init(v: ?Decimal)
```

功能：根据传入参数 v 构造一个 [SqlNullableDecimal <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabledecimal-deprecated) 实例。

参数：

- v: ?[Decimal](../../math_numeric/math_numeric_package_api/math_numeric_package_structs.md#struct-decimal) - 传入的数据。

## class SqlNullableDouble <sup>(deprecated)</sup>

```cangjie
public class SqlNullableDouble <: SqlNullableDbType {
    public init(v: ?Float64)
}
```

功能：双精度数，对应仓颉 [Float64](../../core/core_package_api/core_package_intrinsics.md#float64) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableDouble <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabledouble-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Float64
```

功能：该数据的值。

类型：?[Float64](../../core/core_package_api/core_package_intrinsics.md#float64)

### init(?Float64)

```cangjie
public init(v: ?Float64)
```

功能：根据传入参数 v 构造一个 [SqlNullableDouble <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabledouble-deprecated) 实例。

参数：

- v: ?[Float64](../../core/core_package_api/core_package_intrinsics.md#float64) - 传入的数据。

## class SqlNullableInteger <sup>(deprecated)</sup>

```cangjie
public class SqlNullableInteger <: SqlNullableDbType {
    public init(v: ?Int32)
}
```

功能：中整数，对应仓颉 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableInteger <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullableinteger-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Int32
```

功能：该数据的值。

类型：?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32)

### init(?Int32)

```cangjie
public init(v: ?Int32)
```

功能：根据传入参数 v 构造一个 [SqlNullableInteger <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullableinteger-deprecated) 实例。

参数：

- v: ?[Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 传入的数据。

## class SqlNullableInterval <sup>(deprecated)</sup>

```cangjie
public class SqlNullableInterval <: SqlNullableDbType {
    public init(v: ?Duration)
}
```

功能：时间间隔，对应仓颉 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableInterval <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullableinterval-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Duration
```

功能：该数据的值。

类型：?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

### init(?Duration)

```cangjie
public init(v: ?Duration)
```

功能：根据传入参数 v 构造一个 [SqlNullableInterval <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullableinterval-deprecated) 实例。

参数：

- v: ?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 传入的数据。

## class SqlNullableReal <sup>(deprecated)</sup>

```cangjie
public class SqlNullableReal <: SqlNullableDbType {
    public init(v: ?Float32)
}
```

功能：浮点数，对应仓颉 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableReal <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablereal-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Float32
```

功能：该数据的值。

类型：?[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)

### init(?Float32)

```cangjie
public init(v: ?Float32)
```

功能：根据传入参数 v 构造一个 [SqlNullableReal <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablereal-deprecated) 实例。

参数：

- v: ?[Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - 传入的数据。

## class SqlNullableSmallInt <sup>(deprecated)</sup>

```cangjie
public class SqlNullableSmallInt <: SqlNullableDbType {
    public init(v: ?Int16)
}
```

功能：小整数，对应仓颉 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableSmallInt <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablesmallint-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Int16
```

功能：该数据的值。

类型：?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)

### init(?Int16)

```cangjie
public init(v: ?Int16)
```

功能：根据传入参数 v 构造一个 [SqlNullableSmallInt <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablesmallint-deprecated) 实例。

参数：

- v: ?[Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 传入的数据。

## class SqlNullableTime <sup>(deprecated)</sup>

```cangjie
public class SqlNullableTime <: SqlNullableDbType {
    public init(v: ?DateTime)
}
```

功能：时间，仅时分秒毫秒有效，对应仓颉 [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableTime <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabletime-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?DateTime
```

功能：该数据的值。

类型：?[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime)

### init(?DateTime)

```cangjie
public init(v: ?DateTime)
```

功能：根据传入参数 v 构造一个 [SqlNullableTime <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabletime-deprecated) 实例。

参数：

- v: ?[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) - 传入的数据。

## class SqlNullableTimestamp <sup>(deprecated)</sup>

```cangjie
public class SqlNullableTimestamp <: SqlNullableDbType {
    public init(v: ?DateTime)
}
```

功能：时间戳，对应仓颉 [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableTimestamp <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabletimestamp-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?DateTime
```

功能：该数据的值。

类型：?[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime)

### init(?DateTime)

```cangjie
public init(v: ?DateTime)
```

功能：根据传入参数 v 构造一个 [SqlNullableTimestamp <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabletimestamp-deprecated) 实例。

参数：

- v: ?[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) - 传入的数据。

## class SqlNullableTimeTz <sup>(deprecated)</sup>

```cangjie
public class SqlNullableTimeTz <: SqlNullableDbType {
    public init(v: ?DateTime)
}
```

功能：带时区的时间，仅时分秒毫秒时区有效，对应仓颉 [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableTimeTz <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabletimetz-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?DateTime
```

功能：该数据的值。

类型：?[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime)

### init(?DateTime)

```cangjie
public init(v: ?DateTime)
```

功能：根据传入参数 v 构造一个 [SqlNullableTimeTz <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullabletimetz-deprecated) 实例。

参数：

- v: ?[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) - 传入的数据。

## class SqlNullableVarBinary <sup>(deprecated)</sup>

```cangjie
public class SqlNullableVarBinary <: SqlNullableDbType {
    public init(v: ?Array<Byte>)
}
```

功能：变长二进制字符串，对应仓颉 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableVarBinary <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablevarbinary-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?Array<Byte>
```

功能：该数据的值。

类型：?[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>

### init(?Array\<Byte>)

```cangjie
public init(v: ?Array<Byte>)
```

功能：根据传入参数 v 构造一个 [SqlNullableVarBinary <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablevarbinary-deprecated) 实例。

参数：

- v: ?[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 传入的数据。

## class SqlNullableVarchar <sup>(deprecated)</sup>

```cangjie
public class SqlNullableVarchar <: SqlNullableDbType {
    public init(v: ?String)
}
```

功能：变长字符串，对应仓颉 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型，可为数据库 `Null` 值。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlNullableDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlNullableVarchar <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablevarchar-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: ?String
```

功能：该数据的值。
类型：?[String](../../core/core_package_api/core_package_structs.md#struct-string)

### init(?String)

```cangjie
public init(v: ?String)
```

功能：根据传入参数 v 构造一个 [SqlNullableVarchar <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlnullablevarchar-deprecated) 实例。

参数：

- v: ?[String](../../core/core_package_api/core_package_structs.md#struct-string) - 传入的数据。

## class SqlOption

```cangjie
public class SqlOption {
    public static const URL: String = "url"
    public static const Host: String = "host"
    public static const Username: String = "username"
    public static const Password: String = "password"
    public static const Driver: String = "driver"
    public static const Database: String = "database"
    public static const Encoding: String = "encoding"
    public static const ConnectionTimeout: String = "connection_timeout"
    public static const UpdateTimeout: String = "update_timeout"
    public static const QueryTimeout: String = "query_timeout"
    public static const FetchRows: String = "fetch_rows"
    public static const SSLMode: String = "ssl.mode"
    public static const SSLModePreferred: String = "ssl.mode.preferred"
    public static const SSLModeDisabled: String = "ssl.mode.disabled"
    public static const SSLModeRequired: String = "ssl.mode.required"
    public static const SSLModeVerifyCA: String = "ssl.mode.verify_ca"
    public static const SSLModeVerifyFull: String = "ssl.mode.verify_full"
    public static const SSLCA: String = "ssl.ca"
    public static const SSLCert: String = "ssl.cert"
    public static const SSLKey: String = "ssl.key"
    public static const SSLKeyPassword: String = "ssl.key.password"
    public static const SSLSni: String = "ssl.sni"
    public static const Tls12Ciphersuites: String = "tls1.2.ciphersuites"
    public static const Tls13Ciphersuites: String = "tls1.3.ciphersuites"
    public static const TlsVersion: String = "tls.version"
}
```

功能：预定义的 sql 选项名称和值。如果需要扩展，请不要与这些名称和值冲突。

### static const ConnectionTimeout

```cangjie
public static const ConnectionTimeout: String = "connection_timeout"
```

功能：获取 connect 操作的超时时间，单位 ms。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const Database

```cangjie
public static const Database: String = "database"
```

功能：获取数据库名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const Driver

```cangjie
public static const Driver: String = "driver"
```

功能：获取数据库驱动名称，比如 postgres，opengauss。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const Encoding

```cangjie
public static const Encoding: String = "encoding"
```

功能：获取数据库字符集编码类型。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const FetchRows

```cangjie
public static const FetchRows: String = "fetch_rows"
```

功能：获取每次获取额外数据时从数据库中提取的行数。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const Host

```cangjie
public static const Host: String = "host"
```

功能：获取数据库服务器主机名或者 IP 地址。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const Password

```cangjie
public static const Password: String = "password"
```

功能：获取连接数据库的密码。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const QueryTimeout

```cangjie
public static const QueryTimeout: String = "query_timeout"
```

功能：获取 query 操作的超时时间，单位 ms。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLCA

```cangjie
public static const SSLCA: String = "ssl.ca"
```

功能：证书颁发机构（ CA ）证书文件的路径名。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLCert

```cangjie
public static const SSLCert: String = "ssl.cert"
```

功能：客户端 SSL 公钥证书文件的路径名。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLKey

```cangjie
public static const SSLKey: String = "ssl.key"
```

功能：客户端 SSL 私钥文件的路径名。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLKeyPassword

```cangjie
public static const SSLKeyPassword: String = "ssl.key.password"
```

功能：客户端 SSL 私钥文件的密码。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLMode

```cangjie
public static const SSLMode: String = "ssl.mode"
```

功能：获取 SSLMode 传输层加密模式。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLModeDisabled

```cangjie
public static const SSLModeDisabled: String = "ssl.mode.disabled"
```

功能：建立未加密的连接。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLModePreferred

```cangjie
public static const SSLModePreferred: String = "ssl.mode.preferred"
```

功能：如果服务器支持加密连接，则建立加密连接；如果无法建立加密连接，则回退到未加密连接，这是 SSLMode 的默认值。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLModeRequired

```cangjie
public static const SSLModeRequired: String = "ssl.mode.required"
```

功能：如果服务器支持加密连接，则建立加密连接。如果无法建立加密连接，则连接失败。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLModeVerifyCA

```cangjie
public static const SSLModeVerifyCA: String = "ssl.mode.verify_ca"
```

功能：SSLModeVerifyCA 和 SSLModeRequired 类似，但是增加了校验服务器证书，如果校验失败，则连接失败。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLModeVerifyFull

```cangjie
public static const SSLModeVerifyFull: String = "ssl.mode.verify_full"
```

功能：SSLModeVerifyFull 和 SSLModeVerifyCA 类似，但通过验证服务器证书中的标识与客户端连接的主机名是否匹配，来执行主机名身份验证。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const SSLSni

```cangjie
public static const SSLSni: String = "ssl.sni"
```

功能：客户端通过该标识在握手过程开始时试图连接到哪个主机名。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const Tls12Ciphersuites

```cangjie
public static const Tls12Ciphersuites: String = "tls1.2.ciphersuites"
```

功能：此选项指定客户端允许使用 TLSv1.2 及以下的加密连接使用哪些密码套件。
值为冒号分隔的字符串，比如 `TLS_ECDHE_ECDSA_WITH_AES_128_GCM_[SHA256]():TLS_DHE_RSA_WITH_AES_128_CBC_SHA`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const Tls13Ciphersuites

```cangjie
public static const Tls13Ciphersuites: String = "tls1.3.ciphersuites"
```

功能：此选项指定客户端允许使用 TLSv1.3 的加密连接使用哪些密码套件。
值为冒号分隔的字符串，比如 `TLS_AES_256_GCM_[SHA384]():TLS_CHACHA20_POLY1305_[SHA256]()`。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const TlsVersion

```cangjie
public static const TlsVersion: String = "tls.version"
```

功能：支持的 TLS 版本号，值为逗号分隔的字符串，比如 "TLSv1.2,TLSv1.3"。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const UpdateTimeout

```cangjie
public static const UpdateTimeout: String = "update_timeout"
```

功能：获取 update 操作的超时时间，单位 ms。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const URL

```cangjie
public static const URL: String = "url"
```

功能：获取数据库连接 URL 字符串。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### static const Username

```cangjie
public static const Username: String = "username"
```

功能：获取连接数据库的用户名。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

## class SqlReal <sup>(deprecated)</sup>

```cangjie
public class SqlReal <: SqlDbType {
    public init(v: Float32)
}
```

功能：浮点数，对应仓颉 [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlReal <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlreal-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Float32
```

功能：该数据的值。

类型：[Float32](../../core/core_package_api/core_package_intrinsics.md#float32)

### init(Float32)

```cangjie
public init(v: Float32)
```

功能：根据传入参数 v 构造一个 [SqlReal <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlreal-deprecated) 实例。

参数：

- v: [Float32](../../core/core_package_api/core_package_intrinsics.md#float32) - 传入的数据。

## class SqlSmallInt <sup>(deprecated)</sup>

```cangjie
public class SqlSmallInt <: SqlDbType {
    public init(v: Int16)
}
```

功能：小整数，对应仓颉 [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlSmallInt <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlsmallint-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Int16
```

功能：该数据的值。

类型：[Int16](../../core/core_package_api/core_package_intrinsics.md#int16)

### init(Int16)

```cangjie
public init(v: Int16)
```

功能：根据传入参数 v 构造一个 [SqlSmallInt <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlsmallint-deprecated) 实例。

参数：

- v: [Int16](../../core/core_package_api/core_package_intrinsics.md#int16) - 传入的数据。

## class SqlTime <sup>(deprecated)</sup>

```cangjie
public class SqlTime <: SqlDbType {
    public init(v: DateTime)
}
```

功能：时间，仅时分秒毫秒有效，对应仓颉 [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlTime <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqltime-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: DateTime
```

功能：该数据的值。

类型：[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime)

### init(DateTime)

```cangjie
public init(v: DateTime)
```

功能：根据传入参数 v 构造一个 [SqlTime <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqltime-deprecated) 实例。

参数：

- v: [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) - 传入的数据。

## class SqlTimestamp <sup>(deprecated)</sup>

```cangjie
public class SqlTimestamp <: SqlDbType {
    public init(v: DateTime)
}
```

功能：时间戳，对应仓颉 [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlTimestamp <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqltimestamp-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: DateTime
```

功能：该数据的值。

类型：[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime)

### init(DateTime)

```cangjie
public init(v: DateTime)
```

功能：根据传入参数 v 构造一个 [SqlTimestamp <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqltimestamp-deprecated) 实例。

参数：

- v: [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) - 传入的数据。

## class SqlTimeTz <sup>(deprecated)</sup>

```cangjie
public class SqlTimeTz <: SqlDbType {
    public init(v: DateTime)
}
```

功能：带时区的时间，仅时分秒毫秒时区有效，对应仓颉 [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlTimeTz <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqltimetz-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: DateTime
```

功能：该数据的值。

类型：[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime)

### init(DateTime)

```cangjie
public init(v: DateTime)
```

功能：根据传入参数 v 构造一个 [SqlTimeTz <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqltimetz-deprecated) 实例。

参数：

- v: [DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime) - 传入的数据。

## class SqlVarBinary <sup>(deprecated)</sup>

```cangjie
public class SqlVarBinary <: SqlDbType {
    public init(v: Array<Byte>)
}
```

功能：变长二进制字符串，对应仓颉 [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlVarBinary <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlvarbinary-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: Array<Byte>
```

功能：该数据的值。

类型：[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>

### init(Array\<Byte>)

```cangjie
public init(v: Array<Byte>)
```

功能：根据传入参数 v 构造一个 [SqlVarBinary <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlvarbinary-deprecated) 实例。

参数：

- v: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 传入的数据。

## class SqlVarchar <sup>(deprecated)</sup>

```cangjie
public class SqlVarchar <: SqlDbType {
    public init(v: String)
}
```

功能：变长字符串，对应仓颉 [String](../../core/core_package_api/core_package_structs.md#struct-string) 类型。

> **注意：**
>
> 未来版本即将废弃不再使用，使用仓颉原生类型替代。

父类型：

- [SqlDbType <sup>(deprecated)</sup>](database_sql_package_interfaces.md#interface-sqldbtype-deprecated)

### prop name

```cangjie
public prop name: String
```

功能：类型名称，即 [SqlVarchar  <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlvarchar-deprecated)。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop value

```cangjie
public mut prop value: String
```

功能：该数据的值。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### init(String)

```cangjie
public init(v: String)
```

功能：根据传入参数 v 构造一个 [SqlVarchar  <sup>(deprecated)</sup>](database_sql_package_classes.md#class-sqlvarchar-deprecated) 实例。

参数：

- v: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 传入的数据。
