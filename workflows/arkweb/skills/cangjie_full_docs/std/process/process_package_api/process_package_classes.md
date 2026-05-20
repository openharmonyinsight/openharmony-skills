# 类

## class CurrentProcess <sup>(deprecated)</sup>

```cangjie
public class CurrentProcess <: Process {}
```

功能：此类为当前进程类，继承 [Process](process_package_classes.md#class-process) 类，提供对当前进程操作相关功能。

提供功能具体如下：

- 提供获取当前进程标准流（`stdIn`、`stdOut`、`stdErr`）机制。
- 提供当前进程退出注册回调函数机制。
- 提供当前进程退出机制，允许设置退出状态码。

> **注意：**
>
> 未来版本即将废弃。

父类型：

- [Process](#class-process)

### prop arguments

```cangjie
public prop arguments: Array<String>
```

功能：返回当前进程参数列表，例如当前进程命令行为 `a.out ab cd ef`，其中 `a.out` 是程序名，则返回的列表包含三个元素 ab cd ef。

> **说明：**
>
> - 使用 C 语言调用仓颉动态库方式时，通过 int SetCJCommandLineArgs(int argc, const char* argv[]) 设置的命令行参数，在使用当前进程的 `arguments` 获取时，将会被舍弃掉第一个参数。

类型：[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>

### prop homeDirectory

```cangjie
public prop homeDirectory: Path
```

功能：获取 `home` 目录的路径。

类型：[Path](../../fs/fs_package_api/fs_package_structs.md#struct-path)

### prop stdErr

```cangjie
public prop stdErr: OutputStream
```

功能：获取当前进程标准错误流。

类型：[OutputStream](../../io/io_package_api/io_package_interfaces.md#interface-outputstream)

### prop stdIn

```cangjie
public prop stdIn: InputStream
```

功能：获取当前进程标准输入流。

类型：[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### prop stdOut

```cangjie
public prop stdOut: OutputStream
```

功能：获取当前进程标准输出流。

类型：[OutputStream](../../io/io_package_api/io_package_interfaces.md#interface-outputstream)

### prop tempDirectory

```cangjie
public prop tempDirectory: Path
```

功能：获取临时目录的路径。从环境变量中获取 `TMPDIR`、`TMP`、`TEMP` 和 `TEMPDIR` 环境变量。如果以上值在环境变量中均不存在，则默认返回 `/tmp` 目录。

类型：[Path](../../fs/fs_package_api/fs_package_structs.md#struct-path)

### func atExit(() -> Unit)

```cangjie
public func atExit(callback: () -> Unit): Unit
```

功能：注册回调函数，当前进程退出时执行注册函数。

> **注意：**
>
> 请不要使用 C 语言 atexit 函数，避免出现非预期问题。

参数：

- callback: () ->[Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 需要被注册回调的函数。

### func exit(Int64)

```cangjie
public func exit(code: Int64): Nothing
```

功能：进程退出函数，执行到此函数直接结束当前进程，并且通过入参 `code` 设置返回状态码。

参数：

- code: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 当前进程退出状态码。

### func getEnv(String)

```cangjie
public func getEnv(key: String): Option<String>
```

功能：获取指定名称的环境变量值。

参数：

- key: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 环境变量名称。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 指定名称对应的环境变量值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数入参包含空字符时，抛出异常。

### func removeEnv(String)

```cangjie
public func removeEnv(k: String): Unit
```

功能：通过指定环境变量名称移除环境变量。

参数：

- k: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 环境变量名称。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `k` 包含空字符时，抛出异常。

### func setEnv(String, String)

```cangjie
public func setEnv(k: String, v: String): Unit
```

功能：用于设置一对环境变量。如果设置了同名环境变量，原始环境变量值将被覆盖。

> **说明：**
>
> Windows 下如果传入的参数 v 是空字符串，那么会从环境中移除变量 k。

参数：

- k: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 环境变量名称。
- v: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 环境变量值。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `k` 或 `v` 中包含空字符时，抛出异常。

## class Process

```cangjie
public open class Process
```

功能：此类为进程类，提供进程操作相关功能。

> **说明：**
>
> 提供功能具体如下：
>
> - 提供获取当前进程实例的功能。
> - 提供根据进程 `id` 绑定进程实例的功能。
> - 提供根据输入信息创建子进程的功能。
> - 提供获取进程信息的功能。
> - 提供关闭进程的功能，允许设置是否强制关闭进程。

### static prop current <sup>(deprecated)</sup>

```cangjie
public static prop current: CurrentProcess
```

功能：获取当前进程实例。

> **注意：**
>
> 未来版本即将废弃，使用 [env](../../env/env_package_overview.md#函数) 包的全局函数替代。

类型：[CurrentProcess](process_package_classes.md#class-currentprocess-deprecated)

### prop arguments <sup>(deprecated)</sup>

```cangjie
public open prop arguments: Array<String>
```

功能：获取进程参数。`Windows` 平台下无法在非特权 `API` 下获取到本属性。

> **注意：**
>
> 未来版本即将废弃。

类型：[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>

异常：

- [ProcessException](process_package_exceptions.md#class-processexception) - 当进程不存在或对应进程为僵尸进程，或在 `Windows` 平台不支持场景下获取进程参数时，抛出异常。

### prop command

```cangjie
public prop command: String
```

功能：获取进程命令。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

异常：

- [ProcessException](process_package_exceptions.md#class-processexception) - 当进程不存在或对应进程为僵尸进程，无法获取进程命令时，抛出异常。

### prop commandLine <sup>(deprecated)</sup>

```cangjie
public prop commandLine: Array<String>
```

功能：获取当前进程命令行。对于 Windows 平台，只能获取当前进程的命令行，其他场景下无法在非特权 API 下获取到本属性。

> **注意：**
>
> 未来版本即将废弃，使用 [getcommandline()](../../env/env_package_api/env_package_funcs.md#func-getcommandline) 替代。

类型：[Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)>

异常：

- [ProcessException](process_package_exceptions.md#class-processexception) - 当进程不存在、对应进程为僵尸进程或在其他不支持的场景下无法获取进程命令行时，抛出异常。

### prop environment <sup>(deprecated)</sup>

```cangjie
public prop environment: Map<String, String>
```

功能：获取当前进程环境变量。对于 Windows 平台，只能获取当前进程的环境变量，其他场景下无法在非特权 API 下获取到本属性。

> **注意：**
>
> 未来版本即将废弃，使用 [getVariables()](../../env/env_package_api/env_package_funcs.md#func-getvariables) 替代。

类型：[Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v)\<[String](../../core/core_package_api/core_package_structs.md#struct-string), [String](../../core/core_package_api/core_package_structs.md#struct-string)>

异常：

- [ProcessException](process_package_exceptions.md#class-processexception) - 当进程不存在、对应进程为僵尸进程或在其他不支持的场景下无法获取进程环境变量时，抛出异常。

### prop name

```cangjie
public prop name: String
```

功能：获取进程名。

类型：[String](../../core/core_package_api/core_package_structs.md#struct-string)

异常：

- [ProcessException](process_package_exceptions.md#class-processexception) - 当进程不存在或对应进程为僵尸进程，无法获取进程名时，抛出异常。

### prop pid

```cangjie
public prop pid: Int64
```

功能：获取进程 `id`。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### prop startTime

```cangjie
public prop startTime: DateTime
```

功能：获取进程启动时间，获取失败时返回 [DateTime.UnixEpoch](../../time/time_package_api/time_package_structs.md#static-prop-unixepoch)。

类型：[DateTime](../../time/time_package_api/time_package_structs.md#struct-datetime)

### prop systemTime

```cangjie
public prop systemTime: Duration
```

功能：获取进程启动时间，获取失败时返回 -1ms。

类型：[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

### prop userTime

```cangjie
public prop userTime: Duration
```

功能：获取进程启动时间，获取失败时返回 -1ms。

类型：[Duration](../../core/core_package_api/core_package_structs.md#struct-duration)

### prop workingDirectory <sup>(deprecated)</sup>

```cangjie
public prop workingDirectory: Path
```

功能：获取进程工作路径。对于 `Windows` 平台，仅对当前进程生效，其他场景下无法在非特权 `API` 下获取到本属性。

> **注意：**
>
> 未来版本即将废弃，使用 [getHomeDirectory()](../../env/env_package_api/env_package_funcs.md#func-gethomedirectory) 替代。

类型：[Path](../../fs/fs_package_api/fs_package_structs.md#struct-path)

异常：

- [ProcessException](process_package_exceptions.md#class-processexception) - 当进程不存在或对应进程为僵尸进程，或在 `Windows` 平台的不支持的场景下无法获取进程工作路径时，抛出异常。

### static func of(Int64) <sup>(deprecated)</sup>

```cangjie
public static func of(pid: Int64): Process
```

功能：根据输入进程 `id` 绑定一个进程实例。

> **注意：**
>
> 未来版本即将废弃，使用 [findProcess](./process_package_funcs.md#func-findprocessint64) 替代。

参数：

- pid: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 进程 `id`。

返回值：

- [Process](process_package_classes.md#class-process) - 返回进程 `id` 对应的进程实例。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当输入进程 `id` 大于 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 最大值或小于 `0`时，抛出异常。
- [ProcessException](process_package_exceptions.md#class-processexception) - 当内存分配失败或 `pid` 对应的进程不存在时，抛出异常。

### static func run(String, Array\<String>, ?Path, ?Map\<String, String>, ProcessRedirect, ProcessRedirect,ProcessRedirect, ?Duration) <sup>(deprecated)</sup>

```cangjie
public static func run(command: String,
                      arguments: Array<String>,
                      workingDirectory!: ?Path = None,
                      environment!: ?Map<String, String> = None,
                      stdIn!: ProcessRedirect = Inherit,
                      stdOut!: ProcessRedirect = Inherit,
                      stdErr!: ProcessRedirect = Inherit,
                      timeout!: ?Duration = None): Int64
```

功能：根据输入参数创建并运行一个子进程，等待该子进程运行完毕并返回子进程退出状态。

> **注意：**
>
> - 未来版本即将废弃，使用 [execute](./process_package_funcs.md#func-executestring-arraystring-path-mapstring-string-processredirect-processredirectprocessredirect-duration) 替代。
> - 在 `Windows` 平台上，在子进程执行完成后立即删除子进程的可执行文件可能删除失败并抛出异常，异常信息为 `Access is denied`，如果遇到该问题，可以在一小段延迟后重新尝试删除该文件，详细实现可参考示例。

参数：

- command: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定子进程命令，`command` 不允许包含空字符。
- arguments: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 指定子进程参数，`arguments` 不允许数组中字符串中包含空字符。
- workingDirectory!: ?[Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 命名可选参数，指定子进程的工作路径，默认继承当前进程工作路径，路径必须为存在的目录且不允许为空路径或包含空字符。
- environment!: ?[Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v)\<[String](../../core/core_package_api/core_package_structs.md#struct-string), [String](../../core/core_package_api/core_package_structs.md#struct-string)> - 命名可选参数，指定子进程环境变量，默认继承当前进程环境变量，`key` 不允许字符串中包含空字符或 `'='`，value 不允许字符串中包含空字符。
- stdIn!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准输入，默认继承当前进程标准输入。
- stdOut!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准输出，默认继承当前进程标准输出。
- stdErr!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准错误，默认继承当前进程标准错误。
- timeout!: ?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 命名可选参数，指定等待子进程超时时间，默认为不超时，`timeout` 指定为 `0` 或负值时表示不超时。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回子进程退出状态，若子进程正常退出，返回子进程退出码，若子进程被信号杀死，返回导致子进程终止的信号编号。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当入参 `command` 包含空字符，或者 `arguments` 数组中字符串中包含空字符，或者 `workingDirectory` 不是存在的目录或为空路径或包含空字符，或者 `environment` 表中 `key` 字符串中包含空字符或 `'='`，或 `value` 字符串中包含空字符，或者 `stdIn`、`stdOut`、`stdErr` 输入为文件模式，输入的文件已被关闭或删除时，抛出异常。
- [ProcessException](process_package_exceptions.md#class-processexception) - 当内存分配失败或 `command` 对应的命令不存在或等待超时，抛出异常。

### static func runOutput(String, Array\<String>, ?Path, ?Map\<String, String>, ProcessRedirect, ProcessRedirect, ProcessRedirect) <sup>(deprecated)</sup>

```cangjie
public static func runOutput(command: String,
                            arguments: Array<String>,
                            workingDirectory!: ?Path = None,
                            environment!: ?Map<String, String> = None,
                            stdIn!: ProcessRedirect = Inherit,
                            stdOut!: ProcessRedirect = Pipe,
                            stdErr!: ProcessRedirect = Pipe): (Int64, Array<Byte>, Array<Byte>)
```

功能：根据输入参数创建并运行一个子进程，等待该子进程运行完毕并返回子进程退出状态、标准输出和标准错误。输出流、错误流中包含大量输出的场景不适用于本函数，建议通过 [SubProcess](process_package_classes.md#class-subprocess) 中提供的标准流属性结合 `wait` 函数自行处理。

> **注意：**
>
> 未来版本即将废弃，使用 [executeWithOutput](./process_package_funcs.md#func-executewithoutputstring-arraystring-path-mapstring-string-processredirect-processredirect-processredirect) 替代。

参数：

- command: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定子进程命令，`command` 不允许包含空字符。
- arguments: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 指定子进程参数，`arguments` 不允许数组中字符串中包含空字符。
- workingDirectory!: ?[Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 命名可选参数，指定子进程的工作路径，默认继承当前进程工作路径，路径必须为存在的目录且不允许为空路径或包含空字符。
- environment!: ?[Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v)\<[String](../../core/core_package_api/core_package_structs.md#struct-string), [String](../../core/core_package_api/core_package_structs.md#struct-string)> - 命名可选参数，指定子进程环境变量，默认继承当前进程环境变量，`key` 不允许字符串中包含空字符或 `'='`，value 不允许字符串中包含空字符。
- stdIn!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准输入，默认继承当前进程标准输入。
- stdOut!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准输出，默认继承当前进程标准输出。
- stdErr!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准错误，默认继承当前进程标准错误。

返回值：

- ([Int64](../../core/core_package_api/core_package_intrinsics.md#int64), [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>, [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>) - 子进程执行返回结果，包含子进程退出状态（若子进程正常退出，返回子进程退出码，若子进程被信号杀死，返回导致子进程终止的信号编号），进程标准输出结果和进程错误结果。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当入参 `command` 包含空字符，或者 `arguments` 数组中字符串中包含空字符，或者 `workingDirectory` 不是存在的目录或为空路径或包含空字符，或者 `environment` 表中 `key` 字符串中包含空字符或 `'='`，或 `value` 字符串中包含空字符，或者 `stdIn`、`stdOut`、`stdErr` 输入为文件模式，输入的文件已被关闭或删除时，抛出异常。
- [ProcessException](process_package_exceptions.md#class-processexception) - 当内存分配失败，或者 `command` 对应的命令不存在，或者子进程不存在，或者标准流读取异常时，抛出异常。

### static func start(String, Array\<String>, ?Path, ?Map\<String, String>, ProcessRedirect, ProcessRedirect, ProcessRedirect) <sup>(deprecated)</sup>

```cangjie
public static func start(command: String,
                        arguments: Array<String>,
                        workingDirectory!: ?Path = None,
                        environment!: ?Map<String, String> = None,
                        stdIn!: ProcessRedirect = Inherit,
                        stdOut!: ProcessRedirect = Inherit,
                        stdErr!: ProcessRedirect = Inherit): SubProcess
```

功能：根据输入参数创建并运行一个子进程，并返回一个子进程实例。调用该函数创建子进程后，需要调用 `wait` 或 `waitOutput` 函数，否则该子进程结束后成为的僵尸进程的资源不会被回收。

> **注意：**
>
> 未来版本即将废弃，使用 [launch](./process_package_funcs.md#func-launchstring-arraystring-path-mapstring-string-processredirect-processredirect-processredirect) 替代。

参数：

- command: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定子进程命令，`command` 不允许包含空字符。
- arguments: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 指定子进程参数，`arguments` 不允许数组中字符串中包含空字符。
- workingDirectory!: ?[Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 命名可选参数，指定子进程的工作路径，默认继承当前进程工作路径，路径必须为存在的目录且不允许为空路径或包含空字符。
- environment!: ?[Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v)\<[String](../../core/core_package_api/core_package_structs.md#struct-string), [String](../../core/core_package_api/core_package_structs.md#struct-string)> - 命名可选参数，指定子进程环境变量，默认继承当前进程环境变量，`key` 不允许字符串中包含空字符或 `'='`，value 不允许字符串中包含空字符。
- stdIn!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准输入，默认继承当前进程标准输入。
- stdOut!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准输出，默认继承当前进程标准输出。
- stdErr!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准错误，默认继承当前进程标准错误。

返回值：

- [SubProcess](process_package_classes.md#class-subprocess) - 返回一个子进程实例。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当入参 `command` 包含空字符，或者 `arguments` 数组中字符串中包含空字符，或者 `workingDirectory` 不是存在的目录或为空路径或包含空字符，或者 `environment` 表中 `key` 字符串中包含空字符或 `'='`，或 `value` 字符串中包含空字符，或者 `stdIn`、`stdOut`、`stdErr` 输入为文件模式，输入的文件已被关闭或删除时，抛出异常。
- [ProcessException](process_package_exceptions.md#class-processexception) - 当内存分配失败或 `command` 对应的命令不存在时，抛出异常。

### func isAlive()

```cangjie
public func isAlive(): Bool
```

功能：返回进程是否存活。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 进程存活则为`true`，否则为`false`。

### func terminate(Bool)

```cangjie
public func terminate(force!: Bool = false): Unit
```

功能：终止进程，子进程执行返回结果，包含子进程退出状态（若子进程正常退出，返回子进程退出码，若子进程被信号杀死，返回导致子进程终止的信号编号），进程标准输出结果和进程错误结果。

参数：

- force!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 命名可选参数，指定是否强制关闭进程，默认为 `false`，若设置为 `false`，对应进程可以在释放资源后结束；若设置为 `true`，对应进程将被直接杀死。`Windows` 平台实现为强制关闭进程。

异常：

- [ProcessException](process_package_exceptions.md#class-processexception) - 如果进程不存在，不允许终止，则抛出异常。

## class SubProcess

```cangjie
public class SubProcess <: Process {}
```

功能：此类为子进程类，继承 [Process](process_package_classes.md#class-process) 类，提供对子进程操作相关功能。

> **说明：**
>
> 提供功能具体如下：
>
> - 提供获取子进程标准流（`stdIn`、`stdOut`、`stdErr`）机制。
> - 提供等待子进程执行返回退出状态码机制，允许设置等待超时时长。
> - 提供等待子进程执行返回输出结果（包含运行正常、异常结果）机制，允许设置等待超时时长。

父类型：

- [Process](#class-process)

### prop stdErr <sup>(deprecated)</sup>

```cangjie
public prop stdErr: InputStream
```

功能：获取输入流，连接到子进程标准错误流。

> **注意：**
>
> 未来版本即将废弃，使用 [stdErrPipe](./process_package_classes.md#prop-stderrpipe) 替代。

类型：[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### prop stdErrPipe

```cangjie
public prop stdErrPipe: InputStream
```

功能：获取输入流，连接到子进程标准错误流。

类型：[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### prop stdIn <sup>(deprecated)</sup>

```cangjie
public prop stdIn: OutputStream
```

功能：获取输出流，连接到子进程标准输入流。

> **注意：**
>
> 未来版本即将废弃，使用 [stdInPipe](./process_package_classes.md#prop-stdinpipe) 替代。

类型：[OutputStream](../../io/io_package_api/io_package_interfaces.md#interface-outputstream)

### prop stdInPipe

```cangjie
public prop stdInPipe: OutputStream
```

功能：获取输出流，连接到子进程标准输入流。

类型：[OutputStream](../../io/io_package_api/io_package_interfaces.md#interface-outputstream)

### prop stdOut <sup>(deprecated)</sup>

```cangjie
public prop stdOut: InputStream
```

功能：获取输入流，连接到子进程标准输出流。

> **注意：**
>
> 未来版本即将废弃，使用 [stdOutPipe](./process_package_classes.md#prop-stdoutpipe) 替代。

类型：[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### prop stdOutPipe

```cangjie
public prop stdOutPipe: InputStream
```

功能：获取输入流，连接到子进程标准输出流。

类型：[InputStream](../../io/io_package_api/io_package_interfaces.md#interface-inputstream)

### func wait(?Duration)

```cangjie
public func wait(timeout!: ?Duration = None): Int64
```

功能：阻塞当前进程等待子进程任务执行完成并返回子进程退出状态码，允许指定等待超时时间。对于需要操作标准流的场景（Pipe 模式），使用者需要优先处理标准流，避免子进程标准流缓冲区满后调用本函数产生死锁。

> **说明：**
>
> 超时时间处理机制：
>
> - 未传参、 `timeout` 值为 `None` 或值小于等于 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration).Zero 时，阻塞等待直至子进程执行返回。
> - `timeout` 值大于 [Duration](../../core/core_package_api/core_package_structs.md#struct-duration).Zero 时，阻塞等待子进程执行返回或等待超时后抛出超时异常。

参数：

- timeout!: ?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 命名可选参数，设置等待子进程超时时间，默认为 `None`。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回子进程退出状态。若子进程正常退出，返回子进程退出码，若子进程被信号杀死，返回导致子进程终止的信号编号。

异常：

- [TimeoutException](../../core/core_package_api/core_package_exceptions.md#class-timeoutexception) - 当等待超时，子进程未退出时，抛出异常。

### func waitOutput()

```cangjie
public func waitOutput(): (Int64, Array<Byte>, Array<Byte>)
```

功能：阻塞当前进程等待子进程任务执行完成，并返回子进程退出状态码、返回结果（包含输出流和错误流返回结果）。输出流、错误流中包含大量输出的场景不适用于本函数，建议通过 [SubProcess](process_package_classes.md#class-subprocess) 中提供的标准流属性结合 wait 函数自行处理。

返回值：

- ([Int64](../../core/core_package_api/core_package_intrinsics.md#int64), [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>, [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)>) - 子进程执行返回结果，包含子进程退出状态（若子进程正常退出，返回子进程退出码，若子进程被信号杀死，返回导致子进程终止的信号编号），进程标准输出结果和进程错误结果。

异常：

- [ProcessException](process_package_exceptions.md#class-processexception) - 当子进程不存在，或者标准流读取异常时，抛出异常。
