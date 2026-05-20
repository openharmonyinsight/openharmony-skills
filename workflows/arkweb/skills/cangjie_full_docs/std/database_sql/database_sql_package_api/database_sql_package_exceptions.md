# 异常类

## class SqlException

```cangjie
public open class SqlException <: Exception {
    public init()
    public init(message: String)
    public init(message: String, sqlState: String, errorCode: Int64)
}
```

功能：用于处理 sql 相关的异常。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### prop errorCode

```cangjie
public prop errorCode: Int64
```

功能：数据库供应商返回的整数错误代码。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### prop message

```cangjie
public override prop message: String
```

功能：获取异常信息字符串。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### prop sqlState

```cangjie
public prop sqlState: String
```

功能：长度为五个字符的字符串，是数据库系统返回的最后执行的 sql 语句状态。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### init()

```cangjie
public init()
```

功能：无参构造函数。

### init(String)

```cangjie
public init(message: String)
```

功能：根据异常信息创建 [SqlException](database_sql_package_exceptions.md#class-sqlexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。

### init(String, String, Int64)

```cangjie
public init(message: String, sqlState: String, errorCode: Int64)
```

功能：根据异常信息、SQL 语句状态、错误码信息，创建 [SqlException](database_sql_package_exceptions.md#class-sqlexception) 实例。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 异常信息。
- sqlState: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 长度为五个字符的字符串，是数据库系统返回的最后执行的 sql 语句状态。
- errorCode: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 数据库供应商返回的整数错误代码。
