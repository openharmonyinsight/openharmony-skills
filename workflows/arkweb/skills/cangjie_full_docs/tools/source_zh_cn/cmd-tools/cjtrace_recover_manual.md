# 异常堆栈信息还原工具

## 功能简介

`cjtrace-recover` 是仓颉语言的异常堆栈信息还原工具。

如果开发者在编译仓颉应用时开启了外形混淆，那么仓颉应用在运行时如果遇到问题，抛出的异常信息中的堆栈信息也是被混淆的状态，这导致开发者难以定位问题发生原因。`cjtrace-recover` 可以帮助开发者还原混淆过的异常堆栈信息，从而更好地定位和排查问题原因。具体来说，`cjtrace-recover` 可以还原异常堆栈信息中的以下两种信息：

- 被混淆的函数名
- 被混淆的路径名

## 使用说明

通过 `cjtrace-recover -h` 即可查看命令使用方法：

```text
cjtrace-recover -h
Usage: cjtrace-recover OPTION

Use symbol mapping files to recover obfuscated exception stacktrace. The supported options are:
    -f <file>       path to the obfuscated exception stacktrace file
    -m <file,...>   path to the symbol mapping files
    -h              display this help and exit
    -v              print version of cjtrace-recover
```

开发者可以通过 `-f` 选项指定异常堆栈信息保存的文件，通过 `-m` 选项指定符号映射文件，`cjtrace-recover` 会根据符号映射文件中的映射关系还原异常堆栈信息中的符号名和路径名，并将还原后的异常堆栈信息通过标准输出（`stdout`）输出。

## 使用样例

假设有经过外形混淆的仓颉程序抛出的异常堆栈信息如下：

```text
An exception has occurred:
MyException: this is myexception
     at a0(SOURCE:0)
     at ah(SOURCE:0)
     at c3(SOURCE:0)
     at cm0(SOURCE:0)
     at cm1(SOURCE:0)
     at ci0(:0)
```

并且在混淆编译时输出的符号映射文件 `test.obf.map` 的内容如下：

```text
_ZN10mymod.mod111MyException6<init>ER_ZN8std.core6StringE a0 mymod/mod1/mod1.cj
_ZN10mymod.mod115my_common_func1Ev ah mymod/mod1/mod1.cj
_ZN10mymod.mod18MyClassA7myfunc1Eld c3 mymod/mod1/mod1.cj
_ZN7default6<main>Ev cm0 test1/test.cj
user.main cm1
cj_entry$ ci0
```

开发者需要将异常堆栈信息保存在文件中，假设为 `test_stacktrace`。然后通过以下指令还原异常堆栈信息：

```shell
cjtrace-recover -f test_stacktrace -m test.obf.map
```

运行该指令后，会得到如下输出：

```text
An exception has occurred:
MyException: this is myexception
     at mymod.mod1.MyException::init(std.core::String)(mymod/mod1/mod1.cj)
     at mymod.mod1.my_common_func1()(mymod/mod1/mod1.cj)
     at mymod.mod1.MyClassA::myfunc1(Int64, Float64)(mymod/mod1/mod1.cj)
     at default.main()(/home/zzx/repos/obf_test/test1/test.cj)
```

`cjtrace-recover` 会根据符号映射文件还原异常堆栈信息，并通过标准输出流（`stdout`）输出。
