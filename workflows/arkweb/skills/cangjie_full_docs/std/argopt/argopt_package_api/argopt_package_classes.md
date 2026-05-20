# 类

## class ArgOpt <sup>(deprecated)</sup>

```cangjie
public class ArgOpt {
    public init(shortArgFormat: String)
    public init(longArgList: Array<String>)
    public init(shortArgFormat: String, longArgList: Array<String>)
    public init(args: Array<String>, shortArgFormat: String, longArgList: Array<String>)
}
```

功能：用于解析命令行参数，并提供了获取解析结果的功能。

一个命令行参数是由前缀符号、参数名及参数值组成。

其中， "-" 表示短参（短命令行参数）的前缀，"--" 表示长参（长命令行参数）的前缀。可解析的短参参数名只能是字母，可解析长参参数名字符串需满足：以字母开头，参数名中不能包含 "="。

例如："-a123" 和 "--target=abc.txt" 为两个命令行参数，"a" 为短参名，"target" 为长参名。而 "-123" 和 "--tar=get=abc.txt" 则是错误的命令行参数。

该类允许用户指定参数名和参数字符串，并提供根据参数名解析字符串的方法。

用户指定短参名和长参名时格式如下：

- 短参名字符串的参数，格式为："a:"，规范为：一位字母和 ":" 的组合，例如："ab:"，该例仅解析 "b" 作为短参名。
- 长参名字符串数组参数，字符串格式为："--testA=" 或 "testA="，规范为："--" + 长参参数名 + "="（前缀"--"可省略）。

根据参数名解析命令行参数时，若命令行参数格式正确且有对应的参数名，可正确解析并被用户获取，否则不会解析。

例如：参数名为 "a:b:"，命令行参数为 "-a123 -cofo"，将解析出参数名为 "a"，参数值为 "123" 的命令行参数。"-cofo" 则不会解析。

> **注意：**
>
> 未来版本即将废弃，使用 [parseArguments](./argopt_package_function.md#func-parseargumentsarraystring-arrayargumentspec) 代替。

### init(Array\<String>)

```cangjie
public init(longArgList: Array<String>)
```

功能：构造 `ArgOpt` 实例，并从列表的字符串中解析长参名。

参数：

- longArgList: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 包含长参名的字符串数组。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当字符串数组中的长参名字符串不符合规范，或字符串不符合 UTF-8 编码，或不存在该 Unicode 字符时，抛出异常。

### init(Array\<String>, String, Array\<String>)

```cangjie
public init(args: Array<String>, shortArgFormat: String, longArgList: Array<String>)
```

功能：构造 `ArgOpt` 实例，并从短参名字符串中解析短参名，从列表的字符串中解析长参名。若解析成功，则依据解析出的参数名从参数 `args` 指定的命令行参数中解析参数名的对应取值。

参数：

- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 待解析的命令行参数字符串数组。
- shortArgFormat: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 包含短参名的字符串。
- longArgList: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 包含长参名的字符串数组。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当短参名字符串不符合规范，或字符串数组中的长参名字符串不符合规范，或字符串不符合 UTF-8 编码，或不存在该 Unicode 字符时，抛出异常。

### init(String)

```cangjie
public init(shortArgFormat: String)
```

功能：构造 `ArgOpt` 实例，并从短参名字符串中解析短参名。

参数：

- shortArgFormat: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 包含短参名的字符串。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当短参名字符串不符合规范，或字符串不符合 UTF-8 编码，或不存在该 Unicode 字符时，抛出异常。

### init(String, Array\<String>)

```cangjie
public init(shortArgFormat: String, longArgList: Array<String>)
```

功能：构造 `ArgOpt` 实例，并从短参名字符串中解析短参名，从列表的字符串中解析长参名。

参数：

- shortArgFormat: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 包含短参名的字符串。
- longArgList: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 包含长参名的字符串数组。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当短参名字符串不符合规范，或字符串数组中的长参名字符串不符合规范，或字符串不符合 UTF-8 编码，或不存在该 Unicode 字符时，抛出异常。

### func getArg(String)

```cangjie
public func getArg(arg: String): Option<String>
```

功能：返回参数 `arg` 指定参数的解析值。

参数：

- arg: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 前缀和参数名组成的字符串（可省略前缀）。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 参数解析值。

### func getArgumentsMap()

```cangjie
public func getArgumentsMap(): HashMap<String, String>
```

功能：获取所有已解析的参数名和参数值，以哈希表的形式返回。

返回值：

- [HashMap](../../collection/collection_package_api/collection_package_class.md#class-hashmapk-v-where-k--hashable--equatablek)\<[String](../../core/core_package_api/core_package_structs.md#struct-string), [String](../../core/core_package_api/core_package_structs.md#struct-string)> - 已解析的参数名为键，参数值为值的哈希表。

### func getUnparseArgs()

```cangjie
public func getUnparseArgs(): Array<String>
```

功能：返回未被解析的命令行参数。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 存放没有被解析的字符串的数组。
