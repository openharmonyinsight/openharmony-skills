# std.database.sql

## 功能介绍

database.sql 包提供仓颉访问数据库的接口。

本包提供 SQL/CLI 的通用接口，配合数据库驱动 Driver 完成对数据库的各项操作。

> **注意：**
>
> 当前仅支持 SQL/CLI 接口。

SQL 数据类型和仓颉数据类型对应表如下：

| SQL         | CDBC/Cangjie     | SqlDataType    | 说明                                                  |
| ----------- | ---------------- | -------------- | ----------------------------------------------------- |
| `RUNE`      | `String`         | `SqlChar`      | -                                                    |
| `VARCHAR`   | `String`         | `SqlVarchar`   | -                                                    |
| `CLOB`      | `io.InputStream` | `SqlClob`      | -                                                    |
| `BINARY`    | `Array<Byte>`    | `SqlBinary`    | -                                                    |
| `VARBINARY` | `Array<Byte>`    | `SqlVarBinary` | -                                                    |
| `BLOB`      | `io.InputStream` | `SqlBlob`      | -                                                    |
| `NUMERIC`   | `Decimal`        | `SqlDecimal`   | -                                                    |
| `DECIMAL`   | `Decimal`        | `SqlDecimal`   | -                                                    |
| `BOOLEAN`   | `Bool`           | `SqlBool`      | -                                                    |
| `TINYINT`   | `Int8`           | `SqlByte`      | -                                                    |
| `SMALLINT`  | `Int16`          | `SqlSmallInt`  | -                                                    |
| `INTEGER`   | `Int32`          | `SqlInteger`   | -                                                    |
| `BIGINT`    | `Int64`          | `SqlBigInt`    | -                                                    |
| `REAL`      | `Float32`        | `SqlReal`      | -                                                    |
| `DOUBLE`    | `Float64`        | `SqlDouble`    | -                                                    |
| `DATE`      | `time.DateTime`  | `SqlDate`      | 值支持 `YEAR`，`MONTH`，`DAY`。                        |
| `TIME`      | `time.DateTime`  | `SqlTime`      | 值支持 `HOUR`，`MINUTE`，`SECOND`（不包括 `TIME ZONE`）。|
| `TIMETZ`    | `time.DateTime`  | `SqlTimeTz`    | 值支持 `HOUR`，`MINUTE`，`SECOND`（包括 `TIME ZONE`）。  |
| `TIMESTAMP` | `time.DateTime`  | `SqlTimestamp` | 值支持 `YEAR`，`MONTH`，`DAY`，`HOUR`，`MINUTE`，`SECOND`，`TIME ZONE`。 |
| `INTERVAL`  | `time.Duration`  | `SqlInterval`  | 年-月间隔或者日-时间隔。                                 |

## API 列表

### 接口

| 接口名                                                       | 功能                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [ColumnInfo](./database_sql_package_api/database_sql_package_interfaces.md#interface-columninfo) | 执行 Select/Query 语句返回结果的列信息。                     |
| [Connection](./database_sql_package_api/database_sql_package_interfaces.md#interface-connection) | 数据库连接接口。                                             |
| [Datasource](./database_sql_package_api/database_sql_package_interfaces.md#interface-datasource) | 数据源接口。                                                 |
| [Driver](./database_sql_package_api/database_sql_package_interfaces.md#interface-driver) | 数据库驱动接口。                                             |
| [QueryResult](./database_sql_package_api/database_sql_package_interfaces.md#interface-queryresult) | 执行 Select 语句产生的结果接口。                             |
| [SqlDbType <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_interfaces.md#interface-sqldbtype-deprecated) | 所有 sql 数据类型的父类。 |
| [SqlNullableDbType <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_interfaces.md#interface-sqlnullabledbtype-deprecated) | 允许 `null` 值的 sql 数据类型父类。 |
| [Statement](./database_sql_package_api/database_sql_package_interfaces.md#interface-statement) | sql 语句预执行接口。                                         |
| [Transaction](./database_sql_package_api/database_sql_package_interfaces.md#interface-transaction) | 定义数据库事务的核心行为。                                   |
| [UpdateResult](./database_sql_package_api/database_sql_package_interfaces.md#interface-updateresult) | 执行 Insert、Update、Delete 语句产生的结果接口。             |

### 类

| 类名                                                         | 功能                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [DriverManager](./database_sql_package_api/database_sql_package_classes.md#class-drivermanager) | 支持运行时根据驱动名获取数据库驱动实例。                     |
| [PooledDatasource](./database_sql_package_api/database_sql_package_classes.md#class-pooleddatasource) | 数据库连接池类，提供数据库连接池能力。                       |
| [SqlOption](./database_sql_package_api/database_sql_package_classes.md#class-sqloption) | 预定义的 sql 选项名称和值。                                  |
| [SqlBigInt <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlbigint-deprecated) | 大整数，对应仓颉 `Int64` 类型。                              |
| [SqlBinary <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlbinary-deprecated) | 定长二进制字符串，对应仓颉 `Array<Byte>` 类型。              |
| [SqlBlob <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlblob-deprecated) | 变长超大二进制字符串（BINARY LARGE OBJECT），对应仓颉 `InputStream` 类型。 |
| [SqlBool <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlbool-deprecated) | 布尔类型，对应仓颉 `Bool` 类型。                             |
| [SqlByte <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlbyte-deprecated) | 字节，对应仓颉 `Int8` 类型。                                 |
| [SqlChar <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlchar-deprecated) | 定长字符串，对应仓颉 `String` 类型。                         |
| [SqlClob <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlclob-deprecated) | 变长超大字符串（RUNE LARGE OBJECT），对应仓颉 `InputStream` 类型。 |
| [SqlDate <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqldate-deprecated) | 日期，仅年月日有效，对应仓颉 `DateTime` 类型。               |
| [SqlDecimal <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqldecimal-deprecated) | 高精度数，对应仓颉 `Decimal` 类型。                          |
| [SqlDouble <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqldouble-deprecated) | 双精度数，对应仓颉 `Float64` 类型。    |
| [SqlInteger <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlinteger-deprecated) | 中整数，对应仓颉 `Int32` 类型。                              |
| [SqlInterval <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlinterval-deprecated) | 时间间隔，对应仓颉 `Duration` 类型。                         |
| [SqlReal <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlreal-deprecated) | 浮点数，对应仓颉 `Float32` 类型。                            |
| [SqlSmallInt <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlsmallint-deprecated) | 小整数，对应仓颉 `Int16` 类型。                              |
| [SqlTime <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqltime-deprecated) | 时间，仅时分秒毫秒有效，对应仓颉 `DateTime` 类型。           |
| [SqlTimestamp <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqltimestamp-deprecated) | 时间戳，对应仓颉 `DateTime` 类型。                           |
| [SqlTimeTz <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqltimetz-deprecated) | 带时区的时间，仅时分秒毫秒时区有效，对应仓颉 `DateTime` 类型。 |
| [SqlVarBinary <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlvarbinary-deprecated) | 变长二进制字符串，对应仓颉 `Array<Byte>` 类型。              |
| [SqlVarchar <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlvarchar-deprecated) | 变长字符串，对应仓颉 `String` 类型。                         |
| [SqlNullableBigInt <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullablebigint-deprecated) | 大整数，对应仓颉 `Int64` 类型，可为数据库 `Null` 值。        |
| [SqlNullableBinary <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullablebinary-deprecated) | 定长二进制字符串，对应仓颉 `Array<Byte>` 类型，可为数据库 `Null` 值。 |
| [SqlNullableBlob <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullableblob-deprecated) | 变长超大二进制字符串（BINARY LARGE OBJECT），对应仓颉 `InputStream` 类型，可为数据库 `Null` 值。 |
| [SqlNullableBool <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullablebool-deprecated) | 布尔类型，对应仓颉 `Bool` 类型，可为数据库 `Null` 值。       |
| [SqlNullableByte <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullablebyte-deprecated) | 字节，对应仓颉 `Int8` 类型，可为数据库 `Null` 值。           |
| [SqlNullableChar <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullablechar-deprecated) | 定长二进制字符串，对应仓颉 `String` 类型，可为数据库 `Null` 值。 |
| [SqlNullableClob <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullableclob-deprecated) | 变长超大字符串（RUNE LARGE OBJECT），对应仓颉 `InputStream` 类型，可为数据库 `Null` 值。 |
| [SqlNullableDate <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullabledate-deprecated) | 日期，仅年月日有效，对应仓颉 `DateTime` 类型，可为数据库 `Null` 值。 |
| [SqlNullableDecimal <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullabledecimal-deprecated) | 高精度数，对应仓颉 `Decimal` 类型，可为数据库 `Null` 值。    |
| [SqlNullableDouble <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullabledouble-deprecated) | 双精度数，对应仓颉 `Float64` 类型，可为数据库 `Null` 值。    |
| [SqlNullableInteger <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullableinteger-deprecated) | 中整数，对应仓颉 `Int32` 类型，可为数据库 `Null` 值。        |
| [SqlNullableInterval <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullableinterval-deprecated) | 时间间隔，对应仓颉 `Duration` 类型，可为数据库 `Null` 值。   |
| [SqlNullableReal <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullablereal-deprecated) | 浮点数，对应仓颉 `Float32` 类型，可为数据库 `Null` 值。      |
| [SqlNullableSmallInt <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullablesmallint-deprecated) | 小整数，对应仓颉 `Int16` 类型，可为数据库 `Null` 值。        |
| [SqlNullableTime <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullabletime-deprecated) | 时间，仅时分秒毫秒有效，对应仓颉 `DateTime` 类型，可为数据库 `Null` 值。 |
| [SqlNullableTimestamp <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullabletimestamp-deprecated) | 时间戳，对应仓颉 `DateTime` 类型，可为数据库 `Null` 值。     |
| [SqlNullableTimeTz <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullabletimetz-deprecated) | 带时区的时间，仅时分秒毫秒时区有效，对应仓颉 `DateTime` 类型，可为数据库 `Null` 值。 |
| [SqlNullableVarBinary <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullablevarbinary-deprecated) | 变长二进制字符串，对应仓颉 `Array<Byte>` 类型，可为数据库 `Null` 值。 |
| [SqlNullableVarchar <sup>(deprecated)</sup>](./database_sql_package_api/database_sql_package_classes.md#class-sqlnullablevarchar-deprecated) | 变长字符串，对应仓颉 `String` 类型，可为数据库 `Null` 值。   |

### 枚举

| 枚举名                                                       | 功能                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [ConnectionState](./database_sql_package_api/database_sql_package_enums.md#enum-connectionstate) | 描述与数据源连接的当前状态。                                 |
| [TransactionAccessMode](./database_sql_package_api/database_sql_package_enums.md#enum-transactionaccessmode) | 事务的读写模式。                                               |
| [TransactionDeferrableMode](./database_sql_package_api/database_sql_package_enums.md#enum-transactiondeferrablemode) | 事务的延迟模式。                                             |
| [TransactionIsoLevel](./database_sql_package_api/database_sql_package_enums.md#enum-transactionisolevel) | 定义了数据库系统中，一个事务中操作的结果在何时以何种方式对其他并发事务操作可见。 |

### 异常类

| 异常类名                                                     | 功能                      |
| ------------------------------------------------------------ | ------------------------- |
| [SqlException](./database_sql_package_api/database_sql_package_exceptions.md#class-sqlexception) | 用于处理 sql 相关的异常。 |
