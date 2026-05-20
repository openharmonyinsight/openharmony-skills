# 异常类

## class IllegalSynchronizationStateException

```cangjie
public class IllegalSynchronizationStateException <: Exception {
    public init()
    public init(message: String)
}
```

功能：此类为非法同步状态异常。

父类型：

- [Exception](../../core/core_package_api/core_package_exceptions.md#class-exception)

### init()

```cangjie
public init()
```

功能：创建一个 [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) 实例。

### init(String)

```cangjie
public init(message: String)
```

功能：创建一个 [IllegalSynchronizationStateException](sync_package_exceptions.md#class-illegalsynchronizationstateexception) 实例，其信息由参数 `message` 指定。

参数：

- message: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 预定义消息。
