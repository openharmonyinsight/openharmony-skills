# `cjc` 使用

`cjc`是仓颉编程语言的编译命令，其提供了丰富的功能及对应的编译选项，本章将对基本使用方法进行介绍。

`cjc-frontend` （仓颉前端编译器）会随 `cjc` 一起通过 `Cangjie SDK` 提供，`cjc-frontend` 能够将仓颉源码编译至仓颉的中间表示 （`LLVM IR`）。 `cjc-frontend` 仅进行仓颉代码的前端编译，虽然 `cjc-frontend` 和 `cjc` 共享部分编译选项，但编译流程会在前端编译结束时中止。使用 `cjc` 时仓颉编译器会自动进行前端、后端的编译以及链接工作。`cjc-frontend` 仅作为前端编译器的实体体现提供，除编译器开发者外，仓颉代码的编译应优先使用 `cjc` 。

## `cjc` 基本使用方法

本节介绍 `cjc` 的基本使用方法。关于编译选项详情，请查阅 [cjc 编译选项](../Appendix/compile_options.md)章节。

`cjc` 的使用方式如下：

```shell
cjc [option] file...
```

假如有一个名为 `hello.cj` 的仓颉文件：

<!-- run -->

```cangjie
main() {
    println("Hello, World!")
}
```

可以使用以下命令来编译此文件：

```shell
$ cjc hello.cj
```

此时工作目录下会新增可执行文件 `main` ，`cjc` 默认会将给定源代码文件编译成可执行文件，并将可执行文件命名为 `main`。

以上为不给任何编译选项时 `cjc` 的默认行为，可以通过使用编译选项来控制 `cjc` 的行为，例如让 `cjc` 进行整包编译，又或者是指定输出文件的名字。
