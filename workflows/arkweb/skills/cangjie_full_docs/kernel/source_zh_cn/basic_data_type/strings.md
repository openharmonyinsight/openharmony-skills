# 字符串类型

字符串类型使用 `String` 表示，用于表达文本数据，由一串 Unicode 字符组合而成。

## 字符串字面量

字符串字面量分为三类：单行字符串字面量，多行字符串字面量，多行原始字符串字面量。

**单行字符串字面量**的内容定义在一对单引号或一对双引号之内，引号中的内容可以是任意数量的（除了用于定义字符串字面量的非转义的引号和单独出现的 `\` 之外的）任意字符。单行字符串字面量只能写在同一行，不能跨越多行。举例如下：

<!-- compile -->

```cangjie
let s1: String = ""
let s2 = 'Hello Cangjie Lang'
let s3 = "\"Hello Cangjie Lang\""
let s4 = 'Hello Cangjie Lang\n'
```

**多行字符串字面量**开头结尾需各存在三个双引号（`"""`）或三个单引号（`'''`）。字面量的内容从开头的三个引号换行后的第一行开始，到遇到的第一个非转义的三个引号为止，之间的内容可以是任意数量的（除单独出现的 `\` 之外的）任意字符。不同于单行字符串字面量，多行字符串字面量可以跨越多行。举例如下：

<!-- compile -->

```cangjie
let s1: String = """
    """
let s2 = '''
    Hello,
    Cangjie Lang'''
```

**多行原始字符串字面量**以一个或多个井号（`#`）和一个单引号（`'`）或双引号（`"`）开头，后跟任意数量的合法字符，直到出现与字符串开头相同的引号和与字符串开头相同数量的井号为止。在当前文件结束之前，如果还没遇到匹配的双引号和相同个数的井号，则编译报错。与多行字符串字面量一样，原始多行字符串字面量可以跨越多行。不同之处在于，转义规则不适用于多行原始字符串字面量，字面量中的内容会维持原样（转义字符不会被转义，如下例中 `s2` 中的 `\n` 不是换行符，而是由 `\` 和 `n` 组成的字符串 `\n`）。举例如下：

<!-- compile -->

```cangjie
let s1: String = #""#
let s2 = ##'#'\n'## // 输出结果为：#'\n
let s3 = ###"
    Hello,
    Cangjie
    Lang"### // 该变量当中的换行、缩进等也会被保留
```

对于形如 `left = right` 的赋值操作，如果左操作数的类型是 `Byte`（内置类型 `UInt8` 的别名），并且右操作数是一个表示 ASCII 字符的字符串字面量，那么右操作数的字符串将分别被强制转换为 `Byte` 类型，再进行赋值；如果左操作数的类型是 `Rune`，并且右操作数是一个单字符的字符串字面量，那么右操作数的字符串将分别被强制转换为 `Rune` 类型，再进行赋值。

<!-- verify -->

```cangjie
main() {
    var b: Byte = "0"
    print(b)
    b = "1"
    print(b)
    var r: Rune = "0"
    print(r)
    r = "1"
    print(r)
}
```

编译并执行上述代码，输出结果为：

```text
484901
```

## 插值字符串

插值字符串是一种包含一个或多个插值表达式的字符串字面量（不适用于多行原始字符串字面量），通过将表达式插入到字符串中，可以有效避免字符串拼接的问题。插值字符串经常出现在 `println` 函数中输出非字符串类型的变量值，例如 `println("${x}")`。

插值表达式必须用花括号 `{}` 包起来，并在 `{}` 之前加上 `$` 前缀。`{}` 中可以包含一个或者多个声明或表达式。

当插值字符串求值时，每个插值表达式所在位置会被 `{}` 中的最后一项的值替换，整个插值字符串最终仍是一个字符串。

下面是插值字符串的简单示例：

<!-- verify -->

```cangjie
main() {
    let fruit = "apples"
    let count = 10
    let s = "There are ${count * count} ${fruit}"
    println(s)

    let r = 2.4
    let area = "The area of a circle with radius ${r} is ${let PI = 3.141592; PI * r * r}"
    println(area)
}
```

编译并执行上述代码，输出结果为：

```text
There are 100 apples
The area of a circle with radius 2.400000 is 18.095570
```

## 字符串类型支持的操作

字符串类型支持使用关系操作符进行比较，支持使用 `+` 进行拼接。下面的例子展示了字符串类型的判等和拼接：

<!-- verify -->

```cangjie
main() {
    let s1 = "abc"
    var s2 = "ABC"
    let r1 = s1 == s2
    println("The result of 'abc' == 'ABC' is: ${r1}")
    let r2 = s1 + s2
    println("The result of 'abc' + 'ABC' is: ${r2}")
}
```

编译并执行上述代码，输出结果为：

```text
The result of 'abc' == 'ABC' is: false
The result of 'abc' + 'ABC' is: abcABC
```

字符串还支持其他常见操作，例如拆分、替换等。下面给出部分常见操作：

<!-- run -->

```cangjie
main() {
    var s1 = "abc"
    var s2 = "ABCabc"
    var s3 = "abcyyabcqqabcbc"
    let r1 = s2.contains(s1)    // 判断s2中是否包含字符串s1
    println(r1)                 // true
    let r2 = s3.split(s1)       //对原字符串 s3 按照字符串 s1 分隔符分割，指定是否删除空串
    println(r2[1])              // yy
    s1 = s2
    println(s1)                 // ABCabc
}
```
