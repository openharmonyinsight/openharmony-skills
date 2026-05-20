# std.argopt

## 功能介绍

argopt 包提供从命令行参数字符串解析出参数名和参数值的相关能力。

命令行参数是在命令行中传递给程序的参数，它们用于指定程序的配置或行为。例如，一个命令行程序可能有一个参数来指定它要处理的文件的名称，或者一个参数来指定使用的数据库。这些参数通常会被解析并传递给程序的代码，以便程序可以根据这些参数正确地执行其功能。

命令行参数：通常以是否由 `-` 为前缀区分，可以分为选项和非选项。

- 选项：以 `-` 为前缀。
    - 短选项：以单个 `-` 为前缀且仅含单个字符的选项。
    - 长选项：以 `--` 为前缀的选项，一般包含多个字符。
    - 短前缀长选项：以单个 `-` 为前缀但包含多个字符的选项。
    - 短选项组合：以 `-` 为前缀，将多个短选项以任意顺序组合的选项。
- 非选项：不以 `-` 为前缀。

> **注意：**
>
> 单独的 "--" 后面出现的所有参数也会被视作非选项，如 "-f -- a -b --cde"中，"a"、 "-b"、 "--cde" 都是非选项。

## API 列表

### 函数

|  函数名 | 功能  |
| ------------ | ------------ |
| [parseArguments](./argopt_package_api/argopt_package_function.md#func-parseargumentsarraystring-arrayargumentspec) | 根据给定的输入和规格，解析出对应的参数。|

### 类

|                 类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [ArgOpt <sup>(deprecated)</sup>](./argopt_package_api/argopt_package_classes.md#class-argopt-deprecated) | `ArgOpt` 用于解析命令行参数，并提供了获取解析结果的功能。 |

### 枚举

|                 枚举名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [ArgumentMode](./argopt_package_api/argopt_package_enums.md#enum-argumentmode) | 参数模式。      |
| [ArgumentSpec](./argopt_package_api/argopt_package_enums.md#enum-argumentspec) | 参数规格。    |

### 结构体

| 结构体名                                                                                |           功能           |
|-------------------------------------------------------------------------------------| ------------------------ |
| [ParsedArguments](./argopt_package_api/argopt_package_struct.md#struct-parsedarguments) | 参数解析结果。 |

### 异常类

|                 异常类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [ArgumentParseException](./argopt_package_api/argopt_package_exception.md#class-argumentparseexception) | 解析出错时抛出此异常。|
