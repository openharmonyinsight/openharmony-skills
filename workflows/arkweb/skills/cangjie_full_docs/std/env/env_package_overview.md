# std.env

## 功能介绍

env 包提供当前进程的相关信息与功能、包括环境变量、命令行参数、标准流、退出程序。也提供标准输入、标准输出、标准错误进行交互的方法。

本包提供多平台统一操控能力，目前支持 Linux 平台，macOS 平台，Windows 平台。

本包提供 [getStdErr()](./env_package_api/env_package_funcs.md#func-getstderr)、[getStdIn()](./env_package_api/env_package_funcs.md#func-getstdin) 、[getStdOut()](./env_package_api/env_package_funcs.md#func-getstdout)，用于获取这三个标准流。

- [ConsoleReader](./env_package_api/env_package_classes.md#class-consolereader) 封装了标准输入流的相关功能，可以通过相关的 `read` 方法从标准输入中读取数据。
- [ConsoleWriter](./env_package_api/env_package_classes.md#class-consolewriter) 封装了标准输出、标准错误流的相关功能，[ConsoleWriter](./env_package_api/env_package_classes.md#class-consolewriter) 封装了一系列的 `write` 方法，提供了向标准输出、标准错误写入数据的能力。

标准输入（stdin）、标准输出（stdout）和标准错误（stderr）是计算机操作系统中常见的三个流。

标准输入是程序从用户获取输入数据的流，通常是键盘输入。标准输出是程序向用户输出结果的流，通常是屏幕输出。标准错误是程序在发生错误时输出错误信息的流，通常也是屏幕输出。

在 Unix/Linux 系统中，标准输入、标准输出和标准错误分别对应文件描述符 0、1 和 2。程序可以使用这些文件描述符来读取和写入数据。例如，可以使用重定向符号将标准输出重定向到文件中，或将标准错误输出重定向到另一个程序的标准输入中。

## API 列表

### 类

| 类名 | 功能 |
| :------------ | :------------ |
| [ConsoleReader](./env_package_api/env_package_classes.md#class-consolereader) |  提供从标准输入读取字符或者字符串的功能。 |
| [ConsoleWriter](./env_package_api/env_package_classes.md#class-consolewriter)  |  提供向标准输出或者标准错误流写入字符或者字符串的功能。 |

### 函数

|  函数 | 功能  |
| ------------ | ------------ |
| [atExit()](./env_package_api/env_package_funcs.md#func-atexit---unit) | 注册回调函数，当前进程退出时执行注册函数。 |
| [exit()](./env_package_api/env_package_funcs.md#func-exitint64) | 进程退出函数。 |
| [getCommand()](./env_package_api/env_package_funcs.md#func-getcommand) | 获取当前进程命令。 |
| [getCommandLine()](./env_package_api/env_package_funcs.md#func-getcommandline) | 获取当前进程命令行。 |
| [getHomeDirectory()](./env_package_api/env_package_funcs.md#func-gethomedirectory) | 获取当前进程 home 目录的路径。 |
| [getProcessId()](./env_package_api/env_package_funcs.md#func-getprocessid) | 获取当前进程 id。 |
| [getStdErr()](./env_package_api/env_package_funcs.md#func-getstderr) | 获取当前进程标准错误流。 |
| [getStdIn()](./env_package_api/env_package_funcs.md#func-getstdin) | 获取当前进程标准错误流。 |
| [getStdOut()](./env_package_api/env_package_funcs.md#func-getstdout) | 获取当前进程标准输出流。 |
| [getTempDirectory()](./env_package_api/env_package_funcs.md#func-gettempdirectory) | 获取当前进程临时目录的路径。 |
| [getVariable()](./env_package_api/env_package_funcs.md#func-getvariablestring) | 获取当前进程指定名称的环境变量值。 |
| [getVariables()](./env_package_api/env_package_funcs.md#func-getvariables) | 获取当前进程进程环境变量。 |
| [getWorkingDirectory()](./env_package_api/env_package_funcs.md#func-getworkingdirectory) | 获取当前进程工作路径。 |
| [removeVariable()](./env_package_api/env_package_funcs.md#func-removevariablestring) | 通过指定环境变量名称移除环境变量。 |
| [setVariable()](./env_package_api/env_package_funcs.md#func-setvariablestring-string) | 设置当前进程一对环境变量。 |

### 异常类

| 异常类名 | 功能 |
| --------------------------- | ------------------------ |
| [EnvException](./env_package_api/env_package_exceptions.md#class-envexception) | `env` 包的异常类。 |
