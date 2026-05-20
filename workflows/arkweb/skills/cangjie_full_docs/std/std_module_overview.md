# 仓颉编程语言标准库概述

仓颉编程语言标准库（std）是安装仓颉 SDK 时默认自带的库。标准库预先定义了一组函数、类、结构体等，旨在提供常用的功能和工具，以便开发者能够更快速、更高效地编写程序。

仓颉标准库有其三项特点和追求：

- 使用方便：标准库随编译器、工具链一起发布，不需要用户另外下载，开箱即用。
- 功能通用：标准库提供了开发者最常使用的一些库能力，旨在为开发者解决大部分基础问题。
- 质量标杆：标准库追求在性能、代码风格等方面为其他仓颉库树立范例和标杆。

## 使用指导

在仓颉编程语言中，标准库包含了若干包（package），而包是编译的最小单元。每个包可以单独输出 AST（Abstract Syntax Trees，抽象语法树）文件、静态库文件、动态库文件等产物。包可以定义子包，从而构成树形结构。没有父包的包称为 root 包，root 包及其子包（包括子包的子包）构成的整棵树称为模块（module）。模块的名称与 root 包相同，是开发者发布的最小单元。

包的导入规则如下：

- 可以导入某个包中的一个顶层声明或定义，语法如下：

    ```cangjie
    import fullPackageName.itemName
    ```

    其中 fullPackageName 为完整路径包名，itemName 为声明的名字，例如：

    ```cangjie
    import std.collection.ArrayList
    ```

- 如果要导入的多个 itemName 同属于一个 fullPackageName，可以使用：

    ```cangjie
    import fullPackageName.{itemName[, itemName]*}
    ```

    例如：

    ```cangjie
    import std.collection.{ArrayList, HashMap}
    ```

- 还可以将 fullPackageName 包中所有 public 修饰的顶层声明或定义全部导入，语法如下：

    ```cangjie
    import fullPackageName.*
    ```

    例如：

    ```cangjie
    import std.collection.*
    ```

## 包列表

std 含若干包，提供丰富的基础功能：

|                              包名                              |    功能    |
| -------------------------------------------------------------- | --------- |
| [core](./core/core_package_overview.md)                        | core 包是标准库的核心包，提供了适用仓颉语言编程最基本的一些 API 能力。 |
| [argopt](./argopt/argopt_package_overview.md)                        | argopt 包提供从命令行参数字符串解析出参数名和参数值的相关能力。 |
| [ast](./ast/ast_package_overview.md)                        | ast 包主要包含了仓颉源码的语法解析器和仓颉语法树节点，提供语法解析函数。 |
| [binary](./binary/binary_package_overview.md)                        | binary 包提供了基础数据类型和二进制字节数组的不同端序转换接口，以及端序反转接口。 |
| [collection](./collection/collection_package_overview.md)                        | collection 包提供了常见数据结构的高效实现、相关抽象的接口的定义以及在集合类型中常用的函数功能。 |
| [collection.concurrent](./collection_concurrent/collection_concurrent_package_overview.md)                        | collection.concurrent 包提供了并发安全的集合类型实现。 |
| [console](./console/console_package_overview.md)                        | console 包提供和标准输入、标准输出、标准错误进行交互的方法。 |
| [convert](./convert/convert_package_overview.md)                        | convert 包提供从字符串转到特定类型的 Convert 系列函数以及提供格式化能力，主要为将仓颉类型实例转换为格式化字符串。 |
| [crypto.cipher](./crypto/cipher/cipher_package_overview.md)                        | crypto.cipher 包提供对称加解密通用接口。 |
| [crypto.digest](./crypto/digest/digest_package_overview.md)                        | crypto.digest 包提供常用摘要算法的通用接口，包括 MD5、SHA1、SHA224、SHA256、SHA384、SHA512、HMAC、SM3。 |
| [database.sql](./database_sql/database_sql_package_overview.md)                        | database.sql 包提供仓颉访问数据库的接口。 |
| [deriving](./deriving/deriving_package_overview.md)                        | deriving 包提供一组宏来自动生成接口实现。 |
| [env](./env/env_package_overview.md)                        | env 包提供当前进程的相关信息与功能、包括环境变量、命令行参数、标准流、退出程序。 |
| [fs](./fs/fs_package_overview.md)                        | fs（file system）包提供对文件、文件夹、路径、文件元数据信息的一些操作函数。 |
| [io](./io/io_package_overview.md)                        | io 包提供程序与外部设备进行数据交换的能力。 |
| [math](./math/math_package_overview.md)                        | math 包提供常见的数学运算，常数定义，浮点数处理等功能。 |
| [math.numeric](./math_numeric/math_numeric_package_overview.md)                        | math.numeric 包对基础类型可表达范围之外提供扩展能力。 |
| [net](./net/net_package_overview.md)                        | net 包提供常见的网络通信功能。 |
| [objectpool](./objectpool/objectpool_package_overview.md)                        | objectpool 包提供了对象缓存和复用的功能。 |
| [overflow](./overflow/overflow_package_overview.md)                        | overflow 包提供了溢出处理相关能力。 |
| [posix](./posix/posix_package_overview.md)                        | posix 包封装 POSIX 系统调用，提供跨平台的系统操作接口。 |
| [process](./process/process_package_overview.md)                        | process 包主要提供 Process 进程操作接口，主要包括进程创建，标准流获取，进程等待，进程信息查询等。 |
| [random](./random/random_package_overview.md)                        | random 包提供生成伪随机数的能力。 |
| [reflect](./reflect/reflect_package_overview.md)                        | reflect 包提供了反射功能，使得程序在运行时能够获取到各种实例的类型信息，并进行各种读写和调用操作。 |
| [regex](./regex/regex_package_overview.md)                        | regex 包使用正则表达式分析处理文本的能力（支持 UTF-8 编码的 Unicode 字符串），支持查找、分割、替换、验证等功能。 |
| [runtime](./runtime/runtime_package_overview.md)                        | runtime 包的作用是与程序的运行时环境进行交互，提供了一系列函数和变量，用于控制、管理和监视程序的执行。 |
| [sort](./sort/sort_package_overview.md)                        | sort 包提供数组类型的排序函数。 |
| [sync](./sync/sync_package_overview.md)                        | sync 包提供并发编程相关的能力。 |
| [time](./time/time_package_overview.md)                        | time 包提供了与时间相关的类型，包括日期时间，时间间隔，单调时间和时区等，并提供了计算和比较的功能。 |
| [unicode](./unicode/unicode_package_overview.md)                        | unicode 包提供了按 unicode 编码标准处理字符的能力。 |
| [unittest](./unittest/unittest_package_overview.md)                        | unittest 包用于编写仓颉项目单元测试代码，提供包括代码编写、运行和调测在内的基本功能。 |
| [unittest.mock](./unittest_mock/unittest_mock_package_overview.md)                        |unittest.mock 包提供仓颉单元测试的 mock 框架，提供 API 用于创建和配置 mock 对象，这些 mock 对象与真实对象拥有签名一致的 API 。 |
| [unittest.testmacro](./unittest_testmacro/unittest_testmacro_package_overview.md)                        | unittest.testmacro 为单元测试框架提供了用户所需的宏。 |
| [unittest.mock.mockmacro](./unittest_mock_mockmacro/unittest_mock_mockmacro_package_overview.md)                        | unittest.mock.mockmacro 为 mock 框架提供了用户所需的宏。 |
| [unittest.common](./unittest_common/unittest_common_package_overview.md)                        | unittest.common 为单元测试框架提供了打印所需的类型和一些通用方法。 |
| [unittest.diff](./unittest_diff/unittest_diff_package_overview.md)                        | unittest.diff 为单元测试框架提供了打印差异对比信息所需的 API 。 |
| [unittest.prop_test](./unittest_prop_test/unittest_prop_test_package_overview.md)                        | unittest.prop_test 为单元测试框架提供了参数化测试所需的类型和一些通用方法。 |
