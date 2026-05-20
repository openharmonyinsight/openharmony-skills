# 字符类型

字符类型使用 `Rune` 表示，可以表示 Unicode 字符集中的所有字符。

## 字符类型字面量

字符类型字面量有三种形式：单个字符、转义字符和通用字符。一个 `Rune` 字面量由字符 `r` 开头，后跟一个由一对单引号或双引号包含的字符。

**单个字符**的字符字面量举例：

<!-- compile -->

```cangjie
let a: Rune = r'a'
let b: Rune = r"b"
```

**转义字符**是指在一个字符序列中对后面的字符进行另一种解释的字符。转义字符使用转义符号 `\` 开头，后面加需要转义的字符。举例如下：

<!-- compile -->

```cangjie
let slash: Rune = r'\\'
let newLine: Rune = r'\n'
let tab: Rune = r'\t'
```

**通用字符**以 `\u` 开头，后面加上定义在一对花括号中的 1~8 个十六进制数，即可表示对应的 Unicode 值代表的字符。举例如下：

<!-- verify -->

```cangjie
main() {
    let he: Rune = r'\u{4f60}'
    let llo: Rune = r'\u{597d}'
    print(he)
    print(llo)
}
```

编译并执行上述代码，输出结果为：

```text
你好
```

## 字符类型支持的操作

字符类型支持的操作符包括：关系操作符，即小于（`<`）、大于（`>`）、小于等于（`<=`）、大于等于（`>=`）、相等（`==`）、不等（`!=`）。比较的是字符的 Unicode 值。

`Rune` 可以转换为 `UInt32`，整数类型可以转换为 `Rune`，具体的类型转换语法及规则请参见[`Rune` 到 `UInt32` 和整数类型到 `Rune` 的转换](../class_and_interface/typecast.md#rune-到-uint32-和整数类型到-rune-的转换)。
