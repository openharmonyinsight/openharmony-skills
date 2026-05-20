---
name: cangjie-toolchains
description: 提供仓颉语言编译器cjc/调试器cjdb/覆盖率检测工具cjcov/代码格式化工具cjfmt/静态检查工具cjlint/性能分析工具cjprof的使用文档
descriptionZH: 提供仓颉语言编译器cjc/调试器cjdb/覆盖率检测工具cjcov/代码格式化工具cjfmt/静态检查工具cjlint/性能分析工具cjprof的使用文档
tags:
  - 仓颉
  - 工具链
---

请按需查询当前目录下的工具文档：

[cjc](./cjc/SKILL.md)：仓颉编译器 cjc 核心用法，包括基本编译、输出类型、包编译、模块管理、链接库、调试、测试、宏编译、条件编译、优化、交叉编译等。

[cjdb](./cjdb/SKILL.md)：仓颉调试工具 cjdb 核心用法，包括启动调试、设置断点（源码断点/函数断点/条件断点）、单步执行、查看和修改变量、表达式计算、观察点、仓颉线程调试、launch/attach 调试方式等。

[cjcov](./cjcov/SKILL.md)：仓颉覆盖率统计工具 cjcov 核心用法，包括生成仓颉程序的代码覆盖率报告、编译选项(--coverage)、分支覆盖率、源文件过滤(include/exclude)、与 cjpm 集成等。

[cjfmt](./cjfmt/SKILL.md)：仓颉格式化工具 cjfmt 核心用法，包括单文件格式化、目录格式化、片段格式化、格式化配置文件(cangjie-format.toml)、格式化规则（缩进、大括号、空格、空行、分号、修饰符排序、注释）等。

[cjlint](./cjlint/SKILL.md)：仓颉静态检查工具 cjlint 核心用法，包括规则级告警屏蔽、源代码注释告警屏蔽、文件级告警屏蔽、支持的规范列表（命名/格式/声明/函数/类/接口/操作符/枚举/变量/表达式/错误处理/包/并发/安全等）、语法禁用检查等。

[cjprof](./cjprof/SKILL.md)：仓颉性能分析工具 cjprof 核心用法，包括 CPU 热点函数采样(record)、生成性能报告和火焰图(report)、导出和分析堆内存(heap)，包括采样频率设置、文本报告/火焰图生成、堆内存对象引用关系分析、仓颉线程栈查看等。

