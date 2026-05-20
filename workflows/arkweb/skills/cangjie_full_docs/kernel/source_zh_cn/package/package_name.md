# 包的声明

在仓颉编程语言中，包声明以关键字 `package` 开头，后接 root 包至当前包由 `.` 分隔路径上所有包的包名。包名必须是合法的普通标识符（不含原始标识符）。例如：

```cangjie
package pkg1      // root 包 pkg1
package pkg1.sub1 // root 包 pkg1 的子包 sub1
```

> **注意：**
>
> 当前 Windows 平台版本，包名暂不支持使用 Unicode 字符，包名必须是一个仅含 ASCII 字符的合法的普通标识符。

包声明必须在源文件的非空非注释的首行，且同一个包中的不同源文件的包声明必须保持一致。

<!-- compile.error -->
<!-- cfg="-p test --output-type=staticlib" -->

```cangjie
// file 1
// Comments are accepted
package test
// declarations...

// file 2
let a = 1 // Error, package declaration must appear first in a file
package test
// declarations...
```

仓颉的包名需反映当前源文件相对于项目源码根目录 `src` 的路径，并将其中的路径分隔符替换为小数点。例如包的源代码位于 `src/directory_0/directory_1` 下，root 包名为 `pkg` 则其源代码中的包声明应为 `package pkg.directory_0.directory_1`。

需要注意的是：

- 包所在的文件夹名必须与包名一致。
- 源码根目录默认名为 `src`。
- 源码根目录下的包可以没有包声明，此时编译器将默认为其指定包名 `default`。

假设源代码目录结构如下：

```text
// The directory structure is as follows:
src
|-- directory_0
    |-- directory_1
    |    |-- a.cj
    |    |-- b.cj
    |-- c.cj
|-- main.cj
```

则 `a.cj`、`b.cj`、`c.cj`、`main.cj` 中的包声明可以为:

```cangjie
// a.cj
// in file a.cj, the declared package name must correspond to relative path directory_0/directory_1.

package default.directory_0.directory_1
```

```cangjie
// b.cj
// in file b.cj, the declared package name must correspond to relative path directory_0/directory_1.

package default.directory_0.directory_1
```

```cangjie
// c.cj
// in file c.cj, the declared package name must correspond to relative path directory_0.

package default.directory_0
```

```cangjie
// main.cj
// file main.cj is in the module root directory and may omit package declaration.

main(): Int64 {
    return 0
}
```

另外，包声明不能引起命名冲突：子包不能和当前包的顶层声明同名。

以下是一些错误示例：

```cangjie
// a.cj
package a
public class B { // Error, 'B' is conflicted with sub-package 'a.B'
    public static func f() {}
}
```

<!-- compile.error -->
<!-- cfg="-p a/B --output-type=staticlib" -->

```cangjie
// b.cj
package a.B
public func f {}
```

<!-- compile.error -->
<!-- cfg="liba.a liba.B.a" -->

```cangjie
// main.cj
import a.B // ambiguous use of 'a.B'

main() {
    a.B.f()
}
```
