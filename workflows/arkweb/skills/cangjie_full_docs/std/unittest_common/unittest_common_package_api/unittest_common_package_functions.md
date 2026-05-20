# 函数

## func registerOptionValidator(String, (Any) -> OptionValidity)

```cangjie
public func registerOptionValidator(name: String, validator: (Any) -> OptionValidity): Unit
```

功能：用于注册自定义选项验证器。大多数情况下，用户应该使用  [@UnittestOption](../../unittest_testmacro/unittest_testmacro_package_api/unittest_testmacro_package_macros.md#unittestoption-宏) 宏，而不是直接使用这个函数。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 选项名称。
- validator: ([Any](../../core/core_package_api/core_package_interfaces.md#interface-any)) -> [OptionValidity](./unittest_common_package_enums.md#enum-optionvalidity) - 检查选项是否合法的函数。

## func setOptionInfo(String, Array\<String\>, ?String)

```cangjie
public func setOptionInfo(
    name: String,
    types: Array<String>,
    description!: ?String = None
): Unit
```

功能：用于设置选项的描述的函数。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 选项名称。
- types: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 可以表示的选项值的有效类型
- description: ?[String](../../core/core_package_api/core_package_structs.md#struct-string) - 选项描述。

## func setOrUpdateOptionInfo(String, ?String, String, String)

```cangjie
public func setOrUpdateOptionInfo(
    name: String,
    description: ?String,
    ty: String,
    typeDescription: String
): Unit
```

功能：用于设置具体类型的选项的描述。

参数：

- name: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 选项名称。
- description: ?[String](../../core/core_package_api/core_package_structs.md#struct-string) - 选项的描述。如果值不为 None ，则覆盖先前的值。
- ty: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 类型的字符串形式。
- typeDescription: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 选项的类型描述。
