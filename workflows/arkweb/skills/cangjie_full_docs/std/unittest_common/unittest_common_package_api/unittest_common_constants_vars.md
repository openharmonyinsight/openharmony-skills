# 常量&变量

## let optionsInfo

```cangjie
public let optionsInfo: HashMap<String, OptionInfo> = HashMap()
```

功能：保存有关单元测试选项的信息的注册表。仅在框架内使用，不建议用户使用。

类型：[HashMap](../../collection/collection_package_api/collection_package_class.md#class-hashmapk-v-where-k--hashable--equatablek)\<[String](../../core/core_package_api/core_package_structs.md#struct-string), [OptionInfo](../unittest_common_package_api/unittest_common_package_structs.md#struct-optioninfo)>

## var unittestOptionsRegistryClosed

```cangjie
public var unittestOptionsRegistryClosed = false
```

功能：用于标记选项是否可以注册的内部标志。仅在框架内使用，不建议用户使用。

类型：[Bool](../../core/core_package_api/core_package_intrinsics.md#bool)
