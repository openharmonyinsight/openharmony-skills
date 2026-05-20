# 函数

## func parseArguments(Array\<String>, Array\<ArgumentSpec>)

```cangjie
public func parseArguments(args: Array<String>, specs: Array<ArgumentSpec>): ParsedArguments
```

功能：根据提供的参数规范 `specs` 解析命令行参数 `args`，返回一个结构化的对象，包含解析后的选项和非选项参数。

该函数将 `args` 中的每个参数与 `specs` 中定义的选项进行匹配。对于匹配成功的选项，它会将选项名称和对应的值加入到 [options](./argopt_package_struct.md#prop-options) 中，未匹配的参数会被当作非选项参数处理，并添加到 [nonOptions](./argopt_package_struct.md#prop-nonoptions) 中。此外，当解析到 `--` 时，将提前终止选项扫描，其后的所有参数都将被视作`非选项`。

该函数支持 `短选项`、`长选项`、`短前缀长选项`、`短选项组合`、`非选项`、`非法选项` 的解析处理。

`specs` 的每个 [ArgumentSpec](./argopt_package_enums.md#enum-argumentspec) 持有的 [ArgumentMode](./argopt_package_enums.md#enum-argumentmode) 决定了参数的处理方式。

- 对于长选项，根据不同的 [ArgumentMode](./argopt_package_enums.md#enum-argumentmode) 仅可以处理以下格式：
    - [RequiredValue](./argopt_package_enums.md#requiredvalue): `--option=value` or `--option value`
    - [OptionalValue](./argopt_package_enums.md#optionalvalue): `--option=value` or `--option`
    - [NoValue](./argopt_package_enums.md#novalue): `--option`

- 对于短选项，根据不同的 [ArgumentMode](./argopt_package_enums.md#enum-argumentmode) 仅可以处理以下格式：
    - [RequiredValue](./argopt_package_enums.md#requiredvalue): `-ov` or `-o v`
    - [OptionalValue](./argopt_package_enums.md#optionalvalue): `-ov` or `-o`
    - [NoValue](./argopt_package_enums.md#novalue): `-o`

对于短选项组合的场景：

- 当解析到第一个非 [NoValue](./argopt_package_enums.md#novalue) 的选项时:
    - 如果该选项为 [OptionalValue](./argopt_package_enums.md#optionalvalue)，紧随选项后的内容若存在，则会被作为该选项的值来解析。
    - 如果该选项为 [RequiredValue](./argopt_package_enums.md#requiredvalue)，紧随选项后的内容会被作为该选项的值来解析。
- 如果一组短选项可以组合成长选项的字面值，那么视为长选项而非短选项组合，如 -abc 同时已定义了 `abc` 的长选项和 `a` `b` `c` 三个短选项，会被视作长选项解析。

如果 [ArgumentSpec](./argopt_package_enums.md#enum-argumentspec) 提供了 `lambda` 回调函数，该回调会在解析成功后被调用，处理解析到的参数值。

如果传入的 `args` 存在对同一选项多次赋值的情况，则以最后一次的值作为该选项的值。

参数：

- args: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 被解析的参数。

- specs: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[ArgumentSpec](./argopt_package_enums.md#enum-argumentspec)> - 参数的规范。

返回值：

- [ParsedArguments](./argopt_package_struct.md#struct-parsedarguments) - 参数解析的结果。

异常：

- [ArgumentParseException](./argopt_package_exception.md#class-argumentparseexception) - 当参数解析失败或解析到`非法选项`时，抛出异常。

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当定义了相同 `name` 的 [ArgumentSpec](./argopt_package_enums.md#enum-argumentspec) 时，抛出异常。
