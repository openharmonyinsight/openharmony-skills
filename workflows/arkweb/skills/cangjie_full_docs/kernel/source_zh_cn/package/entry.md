# 程序入口

仓颉程序入口为 `main`，源文件根目录下的包的顶层最多只能有一个 `main`。

如果模块采用生成可执行文件的编译方式，编译器只在源文件根目录下的顶层查找 `main`。如果没有找到，编译器将会报错；如果找到 `main`，编译器会进一步对其参数和返回值类型进行检查。需要注意的是，`main` 不可被访问修饰符修饰，当一个包被导入时，包中定义的 `main` 不会被导入。

作为程序入口的 `main` 可以没有参数或参数类型为 `Array<String>`，返回值类型为 `Unit` 或整数类型。

没有参数的 `main`：

<!-- run -->

```cangjie
// main.cj
main(): Int64 { // OK.
    return 0
}
```

参数类型为 `Array<String>` 的 `main`：

<!-- run -->

```cangjie
// main.cj
main(args: Array<String>): Unit { // OK.
    for (arg in args) {
        println(arg)
    }
}
```

使用 `cjc main.cj` 编译完成后，通过命令行执行：`./main Hello, World`，将会得到如下输出：

```text
Hello,
World
```

以下是一些错误示例：

<!-- compile.error  -->

```cangjie
// main.cj
main(): String { // Error, return type of 'main' is not 'Integer' or 'Unit'.
    return ""
}
```

<!-- compile.error  -->

```cangjie
// main.cj
main(args: Array<Int8>): Int64 { // Error, 'main' cannot be defined with parameter whose type is not Array<String>.
    return 0
}
```

<!-- compile.error  -->

```cangjie
// main.cj
// Error, multiple 'main's are found in source files.
main(args: Array<String>): Int32 {
    return 0
}

main(): Int8 {
    return 0
}
```
