# 结构体

## struct ParsedArguments

```cangjie
public struct ParsedArguments {
}
```

功能：存储参数解析的结果。

### prop nonOptions

```cangjie
public prop nonOptions: Array<String>
```

功能：存储参数解析得到的非选项。

类型：[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>

### prop options

```cangjie
public prop options: ReadOnlyMap<String, String>
```

功能：存储参数解析得到的选项。

类型：[ReadOnlyMap](../../collection/collection_package_api/collection_package_interface.md#interface-readonlymapk-v)
