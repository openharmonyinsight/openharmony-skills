---
name: cangjie-std
description: 提供仓颉语言标准库常用功能速查文档，包括类型转换/格式化字串/文件系统/IO流/标准输入输出/命令行参数处理/单元测试框架等
descriptionZH: 提供仓颉语言标准库常用功能速查文档，包括类型转换/格式化字串/文件系统/IO流/标准输入输出/命令行参数处理/单元测试框架等
tags:
  - 仓颉
  - 标准库
---

请按需查询当前目录下的工具文档：

[ std.convert](./convert/)：提供[常用类型转换操作](./convert/parsable.md)，包括将字符串解析为基础类型（整数/浮点/布尔等），将整数在不同进制间转换等。提供[常用格式化操作](./convert/formattable.md)，将数值类型格式化为指定格式的字符串，如指定宽度、对齐、精度、进制显示等。

[std.fs](./fs/SKILL.md)：提供文件系统操作能力，包括文件读写、目录操作、路径处理、获取文件信息等。

[std.io](./io/SKILL.md)：提供I/O流模型(InputStream/OutputStream)、ByteBuffer、缓冲流(Buffered)、字符串流(StringReader/StringWriter)、链式流(Chained/Multi)、标准流(Console)、流工具函数(copy/readString/readToEnd)等。

[std.unittest](./unittest/SKILL.md)：仓颉单元测试框架，包括声明测试用例（@Test/@TestCase）、断言（@Assert/@Expect/@PowerAssert）、生命周期（@BeforeAll/@AfterAll/@BeforeEach/@AfterEach）、参数化测试、基准测试(@Bench)、动态测试(@TestBuilder)、测试模板(@TestTemplate)、Mock/Spy 对象、桩配置(@On)、验证(@Called/Verify)等。

[stdio](./stdio/SKILL.md)：仓颉语言的标准输出(print/println)、标准错误输出(eprint/eprintln)、标准输入(readln/read)、控制台读写、标准流获取(getStdIn/getStdOut/getStdErr)等。

[args](./args/SKILL.md)：命令行参数处理指导，包括如何通过 main 函数参数接收命令行参数，如何使用 std.argopt 包解析短选项/长选项/组合选项，如何开发 CLI 工具等。

[others](./table.md)：标准库其他包和 API 功能速查表。

