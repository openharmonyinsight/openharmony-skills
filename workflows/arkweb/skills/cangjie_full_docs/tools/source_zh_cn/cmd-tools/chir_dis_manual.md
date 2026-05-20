# CHIR 反序列化工具

## 功能简介

`chir-dis` 是仓颉提供的 CHIR 反序列化工具，用于将编译器输出的 CHIR 序列化信息反序列化为可读的文本文件并保存。

## 使用说明

通过 `chir-dis -h` 即可查看命令使用方法：

```text
A tool used to deserialize and dump CHIR.

Overview: chir-dis xxx.chir -> xxx.chirtxt

Usage:
  chir-dis [option] file

Options:
  -v                      print compiler version information.
  -h                      print this help.
```

开发者可以使用该工具将单个 CHIR 序列化文件反序列化并保存到当前目录，保存的文件后缀为 `.chirtxt`。使用 `-v` 选项时，可以查看对应的编译器版本。

## 使用样例

将编译器输出的 CHIR 序列化信息文件 `package.chir` 反序列化为可读的文本文件进行查看时，可以通过如下指令将其反序列化：

```shell
chir-dis package.chir
```

运行完上面的指令后则在当前目录生成一个 `package.chirtxt` 的文本文件。
