# 标识符

在仓颉编程语言中，开发者可以给一些程序元素命名，这些名字被称为“标识符”。

学习标识符之前，需要了解一些 Unicode 字符集概念。在 Unicode 标准中，`XID_Start` 和 `XID_Continue` 属性用于标记可以作为 Unicode 标识符（Identifier）的起始字符和后续字符，其详细定义请参见 [Unicode 标准文档](https://www.unicode.org/reports/tr31/tr31-37.html)。其中， `XID_Start` 包含中文和英文等字符，`XID_Continue` 包含中文、英文和阿拉伯数字等字符。仓颉语言使用 Unicode 标准 15.0.0 。

仓颉编程语言的标识符分为普通标识符和原始标识符两类，它们遵从不同的命名规则。

**普通标识符**不能和仓颉关键字相同，其取自以下两类字符序列：

- 由 `XID_Start` 字符开头，后接任意长度的 `XID_Continue` 字符。
- 由一个`_`开头，后接至少一个 `XID_Continue` 字符。

仓颉把所有标识符识别为 [Normalization Form C (NFC)](https://www.unicode.org/reports/tr15/tr15-53.html) 后的形式。两个标识符如果在 NFC 后相等，则被认为是相同的标识符。

例如，以下每行字符串都是合法的普通标识符：

```text
abc
_abc
abc_
a1b2c3
a_b_c
a1_b2_c3
仓颉
__こんにちは
```

以下每行字符串都是不合法的普通标识符：

```text
ab&c  // & 不是 XID_Continue 字符
3abc  // 阿拉伯数字不是 XID_Start 字符，因此，数字不能作为起始字符
_     // _ 后至少需要有一个 XID_Continue 字符
while // while 是仓颉关键字，普通标识符不能使用仓颉关键字
```

**原始标识符**是在普通标识符或仓颉关键字的首尾加上一对反引号，主要用于将仓颉关键字作为标识符的场景。

例如，以下每行字符串都是合法的原始标识符：

```text
`abc`
`_abc`
`a1b2c3`
`if`
`while`
`à֮̅̕b`
```

以下每行字符串，由于反引号内的部分是不合法的普通标识符，所以它们整体也是不合法的原始标识符：

```text
`ab&c`
`3abc`
```
