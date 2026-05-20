# 函数

## func atExit(() -> Unit)

```cangjie
public func atExit(callback: () -> Unit): Unit
```

功能：注册回调函数，当前进程退出时执行注册函数。

> **注意：**
>
> 请不要使用 C 语言 atexit 函数，避免出现非预期问题。

参数：

- callback: () ->[Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 需要被注册回调的函数。

## func exit(Int64)

```cangjie
public func exit(code: Int64): Nothing
```

功能：立即终止当前进程，并返回指定的退出状态码。

参数：

- code: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前进程退出状态码。

## func getCommand()

```cangjie
public func getCommand(): String
```

功能：获取进程命令。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 当前进程命令。

异常：

- [EnvException](./env_package_exceptions.md#class-envexception) - 当进程不存在或对应进程为僵尸进程，无法获取进程名时，抛出异常。

## func getCommandLine()

```cangjie
public func getCommandLine(): Array<String>
```

功能：获取当前进程命令行。对于 Windows 平台，只能获取当前进程的命令行，其他场景下无法在非特权 API 下获取到本属性。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 当前进程命令行。

异常：

- [EnvException](./env_package_exceptions.md#class-envexception) - 当进程不存在、对应进程为僵尸进程或在其他不支持的场景下无法获取进程命令行时，抛出异常。

## func getHomeDirectory()

```cangjie
public func getHomeDirectory(): Path
```

功能：获取当前进程 home 目录的路径。

返回值：

- [Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 当前进程 home 目录的路径。

## func getProcessId()

```cangjie
public func getProcessId(): Int64
```

功能：获取当前进程 id。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前进程 id。

## func getStdErr()

```cangjie
public func getStdErr(): ConsoleWriter
```

功能：获取当前进程标准错误流。

返回值：

- [ConsoleWriter](./env_package_classes.md#class-consolewriter) - 进程标准错误流。

## func getStdIn()

```cangjie
public func getStdIn(): ConsoleReader
```

功能：获取当前进程标准输入流。

返回值：

- [ConsoleReader](./env_package_classes.md#class-consolereader) - 进程标准输入流。

## func getStdOut()

```cangjie
public func getStdOut(): ConsoleWriter
```

功能：获取当前进程标准输出流。

返回值：

- [ConsoleWriter](./env_package_classes.md#class-consolewriter) - 进程标准输出流。

## func getTempDirectory()

```cangjie
public func getTempDirectory(): Path
```

功能：获取当前进程临时目录的路径。从环境变量中获取 TMPDIR、TMP、TEMP 和 TEMPDIR 环境变量。如果以上值在环境变量中均不存在，则默认返回 /tmp 目录。

返回值：

- [Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 当前进程临时目录的路径。

## func getVariable(String)

```cangjie
public func getVariable(key: String): ?String
```

功能：获取当前进程指定名称的环境变量值。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定名称。

返回值：

- ?[String](../../core/core_package_api/core_package_structs.md#struct-string) - 当前进程指定名称的环境变量值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 key 包含空字符时，抛出异常。

## func getVariables()

```cangjie
public func getVariables(): Array<(String, String)>
```

功能：获取当前进程环境变量。对于 Windows 平台，只能获取当前进程的环境变量，其他场景下无法在非特权 API 下获取到本属性。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<([String](../../core/core_package_api/core_package_structs.md#struct-string), [String](../../core/core_package_api/core_package_structs.md#struct-string))> - 当前进程环境变量。

异常：

- [EnvException](./env_package_exceptions.md#class-envexception) - 当进程不存在、对应进程为僵尸进程或在其他不支持的场景下无法获取进程环境变量时，抛出异常。

## func getWorkingDirectory()

```cangjie
public func getWorkingDirectory(): Path
```

功能：获取当前进程工作路径。对于 Windows 平台，只能获取当前进程的工作路径，其他场景下无法在非特权 API 下获取到本属性。

返回值：

- [Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 当前进程工作路径。

异常：

- [EnvException](./env_package_exceptions.md#class-envexception) - 当进程不存在、对应进程为僵尸进程或在其他不支持的场景下无法获取进程工作路径时，抛出异常。

## func removeVariable(String)

```cangjie
public func removeVariable(key: String): Unit
```

功能：通过指定环境变量名称移除环境变量。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 环境变量名称。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 key 包含空字符时，抛出异常。

## func setVariable(String, String)

```cangjie
public func setVariable(key: String, value: String): Unit
```

功能：用于设置一对环境变量。如果设置了同名环境变量，原始环境变量值将被覆盖。

> **说明：**
>
> Windows 下如果传入的参数 v 是空字符串，那么会从环境中移除变量 k。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 环境变量名称。
- value: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 环境变量值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 key 或 value 中包含空字符时，抛出异常。
