# 函数

## func execute(String, Array\<String>, ?Path, ?Map\<String, String>, ProcessRedirect, ProcessRedirect,ProcessRedirect, ?Duration)

```cangjie
public func execute(command: String,
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
> 在 `Windows` 平台上，在子进程执行完成后立即删除子进程的可执行文件可能删除失败并抛出异常，异常信息为 `Access is denied`，如果遇到该问题，可以在一小段延迟后重新尝试删除该文件，详细实现可参考示例。

参数：

- command: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 指定子进程命令，`command` 不允许包含空字符。
- arguments: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[String](../../core/core_package_api/core_package_structs.md#struct-string)> - 指定子进程参数，`arguments` 不允许数组中字符串中包含空字符。
- workingDirectory!: ?[Path](../../fs/fs_package_api/fs_package_structs.md#struct-path) - 命名可选参数，指定子进程的工作路径，默认继承当前进程工作路径，路径必须为存在的目录且不允许为空路径或包含空字符。
- environment!: ?[Map](../../collection/collection_package_api/collection_package_interface.md#interface-mapk-v)\<[String](../../core/core_package_api/core_package_structs.md#struct-string), [String](../../core/core_package_api/core_package_structs.md#struct-string)> - 命名可选参数，指定子进程环境变量，默认继承当前进程环境变量，`key` 不允许字符串中包含空字符或 `'='`，value 不允许字符串中包含空字符。
- stdIn!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准输入，默认继承当前进程标准输入。
- stdOut!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准输出，默认继承当前进程标准输出。
- stdErr!: [ProcessRedirect](process_package_enums.md#enum-processredirect) - 命名可选参数，指定子进程重定向标准错误，默认继承当前进程标准错误。
- timeout!: ?[Duration](../../core/core_package_api/core_package_structs.md#struct-duration) - 命名可选参数，指定等待子进程超时时间，默认为不超时, `timeout` 指定为 `0` 或负值时表示不超时。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回子进程退出状态，若子进程正常退出，返回子进程退出码，若子进程被信号杀死，返回导致子进程终止的信号编号。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception)

    - 当入参 `command` 包含空字符
    - 或者 `arguments` 数组中字符串中包含空字符
    - 或者 `workingDirectory` 不是存在的目录或为空路径或包含空字符
    - 或者 `environment` 表中 `key` 字符串中包含空字符或 `'='`
    - 或者 `value` 字符串中包含空字符
    - 或者 `stdIn`、`stdOut`、`stdErr` 输入为文件模式，输入的文件已被关闭或删除时，抛出异常。

- [ProcessException](process_package_exceptions.md#class-processexception) - 当内存分配失败或 `command` 对应的命令不存在或等待超时，抛出异常。

## func executeWithOutput(String, Array\<String>, ?Path, ?Map\<String, String>, ProcessRedirect, ProcessRedirect, ProcessRedirect)

```cangjie
public func executeWithOutput(command: String,
                            arguments: Array<String>,
                            workingDirectory!: ?Path = None,
                            environment!: ?Map<String, String> = None,
                            stdIn!: ProcessRedirect = Inherit,
                            stdOut!: ProcessRedirect = Pipe,
                            stdErr!: ProcessRedirect = Pipe): (Int64, Array<Byte>, Array<Byte>)
```

功能：根据输入参数创建并运行一个子进程，等待该子进程运行完毕并返回子进程退出状态、标准输出和标准错误。输出流、错误流中包含大量输出的场景不适用于本函数，建议通过 [SubProcess](process_package_classes.md#class-subprocess) 中提供的标准流属性结合 `wait` 函数自行处理。

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

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception)
    - 当入参 `command` 包含空字符
    - 或者 `arguments` 数组中字符串中包含空字符
    - 或者 `workingDirectory` 不是存在的目录或为空路径或包含空字符
    - 或者 `environment` 表中 `key` 字符串中包含空字符或 `'='`
    - 或者 `value` 字符串中包含空字符
    - 或者 `stdIn`、`stdOut`、`stdErr` 输入为文件模式，输入的文件已被关闭或删除时，抛出异常。
- [ProcessException](process_package_exceptions.md#class-processexception)
    - 当内存分配失败
    - 或者 `command` 对应的命令不存在
    - 或者子进程不存在
    - 或者标准流读取异常时，抛出异常。

## func findProcess(Int64)

```cangjie
public func findProcess(pid: Int64): Process
```

功能：根据输入进程 `id` 绑定一个进程实例。

参数：

- pid: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 进程 `id`。

返回值：

- [Process](process_package_classes.md#class-process) - 返回进程 `id` 对应的进程实例。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当输入进程 `id` 大于 [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) 最大值或小于 `0`时，抛出异常。
- [ProcessException](process_package_exceptions.md#class-processexception) - 当内存分配失败或 `pid` 对应的进程不存在时，抛出异常。

## func launch(String, Array\<String>, ?Path, ?Map\<String, String>, ProcessRedirect, ProcessRedirect, ProcessRedirect)

```cangjie
public func launch(command: String,
                        arguments: Array<String>,
                        workingDirectory!: ?Path = None,
                        environment!: ?Map<String, String> = None,
                        stdIn!: ProcessRedirect = Inherit,
                        stdOut!: ProcessRedirect = Inherit,
                        stdErr!: ProcessRedirect = Inherit): SubProcess
```

功能：根据输入参数创建并运行一个子进程，并返回一个子进程实例。调用该函数创建子进程后，需要调用 `wait` 或 `waitOutput` 函数，否则该子进程结束后成为的僵尸进程的资源不会被回收。

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

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception)
    - 当入参 `command` 包含空字符
    - 或者 `arguments` 数组中字符串中包含空字符
    - 或者 `workingDirectory` 不是存在的目录或为空路径或包含空字符
    - 或者 `environment` 表中 `key` 字符串中包含空字符或 `'='`
    - 或者 `value` 字符串中包含空字符
    - 或者 `stdIn`、`stdOut`、`stdErr` 输入为文件模式，输入的文件已被关闭或删除时，抛出异常。
- [ProcessException](process_package_exceptions.md#class-processexception) - 当内存分配失败或 `command` 对应的命令不存在时，抛出异常。
