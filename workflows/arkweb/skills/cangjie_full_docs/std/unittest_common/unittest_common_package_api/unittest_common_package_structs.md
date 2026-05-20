# 结构体

## struct KeyTags

```cangjie
public struct KeyTags <: KeyFor<Array<String>> {}
```

功能：用于在 [Configuration](../../unittest_common/unittest_common_package_api/unittest_common_package_classes.md#class-configuration) 配置键值。

父类型：

- [KeyFor](../unittest_common_package_api/unittest_common_package_interfaces.md#interface-keyfor)

### prop tags

```cangjie
public static prop tags: KeyTags
```

功能：配置项的键值。

类型：[KeyTags](#struct-keytags)

### prop name

```cangjie
public prop name: String
```

功能：配置项的键值的名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

## struct OptionInfo

```cangjie
public struct OptionInfo {
    public let description: ?String
    public let name: String
    public let types!: HashMap<String, ?String> = HashMap()
    public let userDefined: Bool
}
```

功能：打印帮助页面时可以使用的选项的信息。

### let description

```cangjie
public let description: ?String
```

功能：选项描述信息。

类型：?[String](../../core/core_package_api/core_package_structs.md#struct-string)

### let name

```cangjie
public let name: String
```

功能：选项名称。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

### let types

```cangjie
public let types!: HashMap<String, ?String> = HashMap()
```

功能：从选项类型名称映射到值的含义。

类型： HashMap<[String](../../core/core_package_api/core_package_structs.md#struct-string), ?[String](../../core/core_package_api/core_package_structs.md#struct-string)>

### let userDefined

```cangjie
public let userDefined: Bool
```

功能：选项是否已被定义。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)
