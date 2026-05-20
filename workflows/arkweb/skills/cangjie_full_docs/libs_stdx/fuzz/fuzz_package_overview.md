# stdx.fuzz.fuzz

## 功能介绍

Fuzz 技术是一种自动化软件测试方法，旨在发现软件中的漏洞和错误。它通过持续输入随机的或经过变异的测试用例来执行软件程序，并根据程序的覆盖率信息来指导测试的方向。

fuzz 包为开发者提供基于覆盖率反馈的仓颉 fuzz 引擎及对应的接口，开发者可以编写代码对 API 进行测试。当前支持通过传入 fuzz 引擎变异的字节流 (Array\<UInt8>) 或符合仓颉的标准数据类型（FuzzDataProvider）进行 fuzz 测试。

使用此包需要配合覆盖率反馈插桩（SanitizerCoverage）功能使用，需要开发者对 fuzz 测试有一定的了解，初学者建议先学习 C 语言的 Fuzz 工具。

使用本包需要外部依赖 LLVM 套件 `compiler-rt` 提供的 `libclang_rt.fuzzer_no_main.a` 静态库，当前支持 Linux 以及 macOS，不支持 Windows。

通常使用包管理工具即可完成安装，例如 `Ubuntu 22.04` 系统上可使用 `sudo apt install clang` 进行安装，安装后可以在 `clang -print-runtime-dir` 指向的目录下找到对应的 `libclang_rt.fuzzer_no_main.a` 文件，例如 `/usr/lib/llvm-14/lib/clang/14.0.0/lib/linux/libclang_rt.fuzzer_no_main-x86_64.a`，将来在链接时会用到它。

## API 列表

### 类

|                 类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [Fuzzer](./fuzz_package_api/fuzz_package_classes.md#class-fuzzer) | Fuzzer 类提供了 fuzz 工具的创建。           |
| [FuzzerBuilder](./fuzz_package_api/fuzz_package_classes.md#class-fuzzerbuilder) | 此类用于 Fuzzer 类的构建。    |
| [FuzzDataProvider](./fuzz_package_api/fuzz_package_classes.md#class-fuzzdataprovider) | FuzzDataProvider 是一个工具类，目的是将变异数据的字节流转化为标准的仓颉基本数据。  |
| [DebugDataProvider](./fuzz_package_api/fuzz_package_classes.md#class-debugdataprovider) | 此类继承了 FuzzDataProvider 类型，额外增加了调试信息。          |

### 异常类

|               异常类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [ExhaustedException](./fuzz_package_api/fuzz_package_exceptions.md#class-exhaustedexception) | 此异常为转换数据时，剩余数据不足以转换时抛出的异常。    |
