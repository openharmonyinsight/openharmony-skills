# std.unicode

## 功能介绍

unicode 包提供了按 unicode 编码标准处理字符的能力。

`Unicode` 是一种字符编码标准，旨在为所有语言和符号提供一个统一的编码方案，以便在计算机系统中交换和处理文本。

`Unicode` 编码标准将每个字符用唯一的码点表示，同时为每个字符定义了若干属性，如类别（字母、数字、标点等）、脚本（拉丁字母、希腊字母、汉字等）、大小写映射（大写或小写映射关系）、变音符号（是否带有变音符号，如重音符号）。

本包提供了 `UnicodeRuneExtension` 和 `UnicodeStringExtension` 接口类型，为 `Rune`、`String` 类型实现了若干扩展方法，包括字符类型判断、字符大小写转换等。

## API 列表

### 接口

|                 接口名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [UnicodeRuneExtension](./unicode_package_api/unicode_package_interfaces.md#interface-unicoderuneextension) | `Unicode` 字符集相关扩展的接口，用于为 `Rune` 类型扩展 `Unicode` 字符集相关的操作。    |
| [UnicodeStringExtension](./unicode_package_api/unicode_package_interfaces.md#interface-unicodestringextension) | `Unicode` 字符集相关扩展的接口，用于为 `String` 类型扩展 `Unicode` 字符集相关的操作。    |

### 枚举

|                 枚举              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [CasingOption](./unicode_package_api/unicode_package_enums.md#enum-casingoption) | 大小写转换时根据不同语言所需要的枚举类。 |