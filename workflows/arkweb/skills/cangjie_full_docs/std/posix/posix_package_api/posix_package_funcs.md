# 函数

## func \`open`(String, Int32) <sup>(deprecated)</sup>

```cangjie
public func `open`(path: String, oflag: Int32): Int32
```

功能：打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。

当文件打开方式参数 `oflag` 设置为 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 时，可以通过参数设置文件权限。

[O_RDONLY](posix_package_constants_vars.md#const-o_rdonly-deprecated)、[O_RDWR](posix_package_constants_vars.md#const-o_rdwr-deprecated)、[O_WRONLY](posix_package_constants_vars.md#const-o_wronly-deprecated) 作为 `oflag` 取值为互斥关系，但可以与其他操作标识一起使用，如 [O_APPEND](posix_package_constants_vars.md#const-o_append-deprecated) 。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- oflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件打开的方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回新的文件描述符，执行失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func \`open`(String, Int32, UInt32) <sup>(deprecated)</sup>

```cangjie
public func `open`(path: String, oflag: Int32, flag: UInt32): Int32
```

功能：打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。path 代表文件路径，oflag 代表文件打开的方式，其中 [O_RDONLY](posix_package_constants_vars.md#const-o_rdonly-deprecated)、[O_RDWR](posix_package_constants_vars.md#const-o_rdwr-deprecated)、[O_WRONLY](posix_package_constants_vars.md#const-o_wronly-deprecated) 作为 oflag 取值为互斥关系，但可以与其他操作标识一起使用，如 [O_APPEND](posix_package_constants_vars.md#const-o_append-deprecated) 操作。

当文件打开方式参数 `oflag` 设置为 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 时，可以通过参数设置文件权限。

[O_RDONLY](posix_package_constants_vars.md#const-o_rdonly-deprecated)、[O_RDWR](posix_package_constants_vars.md#const-o_rdwr-deprecated)、[O_WRONLY](posix_package_constants_vars.md#const-o_wronly-deprecated) 作为 `oflag` 取值为互斥关系，但可以与其他操作标识一起使用，如 [O_APPEND](posix_package_constants_vars.md#const-o_append-deprecated) 。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- oflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件打开的方式。
- flag: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 如果 `oflag` 设置了 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 并且需要创建新文件，则 `flag` 参数标识对新文件的权限，否则 `flag` 不改变文件权限。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回新的文件描述符，执行失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func access(String, Int32) <sup>(deprecated)</sup>

```cangjie
public func access(path: String, mode: Int32): Int32
```

功能：判断某个文件是否具有某种权限，具有返回 `0`，否则返回 `-1`。

`mode` 为指定权限，传入类型 [R_OK](posix_package_constants_vars.md#const-r_ok-deprecated)、`W_OK`、[X_OK](posix_package_constants_vars.md#const-x_ok-deprecated)、[F_OK](posix_package_constants_vars.md#const-f_ok-deprecated)。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- mode: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 待检查的权限。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件具有待检查的权限返回 `0`，否则返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func chdir(String) <sup>(deprecated)</sup>

```cangjie
public func chdir(path: String): Int32
```

功能：通过指定路径的方式，更改调用进程的当前工作目录。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 改变后的路径。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 设置成功，返回 `0`，设置失败, 返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func chmod(String, UInt32) <sup>(deprecated)</sup>

```cangjie
public func chmod(path: String, mode: UInt32): Int32
```

功能：修改文件访问权限。

在 `Windows` 环境下：

- 所有文件和目录都是可读的，[chmod](posix_package_funcs.md#func-chmodstring-uint32-deprecated)() 不能更改文件的可读权限；
- 在 `Windows` 环境下，文件的可执行权限通过文件扩展名设置，所有目录都是可执行的，[chmod](posix_package_funcs.md#func-chmodstring-uint32-deprecated)() 不能更改文件和目录的可执行权限。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- mode: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 要修改的权限。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 操作成功时返回 `0`，失败时返回 `-1`。当 `mode` 为非法参数时，[chmod](posix_package_funcs.md#func-chmodstring-uint32-deprecated) 会忽略该参数，返回 `0`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func chown(String, UInt32, UInt32) <sup>(deprecated)</sup>

```cangjie
public func chown(path: String, owner: UInt32, group: UInt32): Int32
```

功能：修改文件所有者和文件所有者所属组。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- owner: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 所有者 `uid`。
- group: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 指定 `gid` 参数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 操作成功时返回 `0`，失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func close(Int32) <sup>(deprecated)</sup>

```cangjie
public func close(fd: Int32): Int32
```

功能：关闭文件，[close](posix_package_funcs.md#func-closeint32-deprecated) 将会触发数据写回磁盘，并释放文件占用的资源。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功时返回 `0`，失败时返回 `-1`。

## func creat(String, UInt32) <sup>(deprecated)</sup>

```cangjie
public func creat(path: String, flag: UInt32): Int32
```

功能：创建文件并为其返回文件描述符，或在失败时返回 `-1`。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- flag: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 创建文件的权限。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回文件描述符，执行失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func dup(Int32) <sup>(deprecated)</sup>

```cangjie
public func dup(fd: Int32): Int32
```

功能：用于复制旧 `fd` 参数指定的文件描述符并返回。此新文件描述符和旧的参数 `fd` 引用同一文件，共享文件各种状态。共享所有的锁定、读写位置和各项权限或标志等。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回最小且未使用的文件描述符，执行失败时返回 `-1`。

## func dup2(Int32, Int32) <sup>(deprecated)</sup>

```cangjie
public func dup2(fd: Int32, fd2: Int32): Int32
```

功能：用于复制 `oldfd` 参数指定的文件描述符，并将其返回到 `newfd` 参数。如果参数 `newfd` 是打开的文件描述符，则 `newfd` 指定的文件将首先关闭。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - `oldfd` 参数指定的文件描述符。
- fd2: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - `newfd` 参数指定的文件描述符。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - `fd2` 文件描述符。

## func faccessat(Int32, String, Int32, Int32) <sup>(deprecated)</sup>

```cangjie
public func faccessat(fd: Int32, path: String, mode: Int32, flag: Int32): Int32
```

功能：判断 `fd` 对应的文件是否具有某种权限，具有返回 `0`，否则返回 `-1`。

`mode` 为指定权限，传入类型 [R_OK](posix_package_constants_vars.md#const-r_ok-deprecated)、`W_OK`、[X_OK](posix_package_constants_vars.md#const-x_ok-deprecated)、[F_OK](posix_package_constants_vars.md#const-f_ok-deprecated)。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- mode: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 待检查的权限。
- flag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 将以下一个或多个值按位或运算获取。`(512)`使用有效的用户和组 `ID` 执行访问检查，默认情况下使用有效 `ID`；`(256)` 如果路径名是符号链接，不会取消引用而是返回有关链接本身信息。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件具有待检查的权限返回 `0`，否则返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func fchdir(Int32) <sup>(deprecated)</sup>

```cangjie
public func fchdir(fd: Int32): Int32
```

功能：通过指定文件路径的描述符，更改调用进程的当前工作目录。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 改变后的文件路径的描述符。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 设置成功，返回 `0`，设置失败, 返回 `-1`。

## func fchmod(Int32, UInt32) <sup>(deprecated)</sup>

```cangjie
public func fchmod(fd: Int32, mode: UInt32): Int32
```

功能：修改文件描述符对应的文件访问权限。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- mode: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 要修改的权限。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 操作成功时返回 `0`，失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func fchmodat(Int32, String, UInt32, Int32) <sup>(deprecated)</sup>

```cangjie
public func fchmodat(fd: Int32, path: String, mode: UInt32, flag: Int32): Int32
```

功能：修改文件描述符对应的文件访问权限。

- `path` 为相对路径且 `fd` 为特殊值 `AT_FDCWD` 时，则路径将相对于调用进程的当前工作目录。
- `path` 为相对路径且 `fd` 非 `AT_FDCWD` 时，则路径将相对于 `fd` 引用的文件所属目录。
- `path` 为绝对路径时 `fd` 参数将被忽略。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- mode: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 要修改的权限。
- flag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 取值可为 `0`，或 `(256)` 如果路径名是符号链接，不会取消引用它，而是返回有关链接本身的信息。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 操作成功时返回 `0`，失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func fchown(Int32, UInt32, UInt32) <sup>(deprecated)</sup>

```cangjie
public func fchown(fd: Int32, owner: UInt32, group: UInt32): Int32
```

功能：修改 `fd` 对应的文件所有者和文件所有者所属组。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- owner: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 所有者 `uid`。
- group: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 指定 `gid` 参数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 操作成功时返回 `0`，失败时返回 `-1`。

## func fchownat(Int32, String, UInt32, UInt32, Int32) <sup>(deprecated)</sup>

```cangjie
public func fchownat(fd: Int32, path: String, owner: UInt32, group: UInt32, flag: Int32): Int32
```

功能：修改文件描述符对应的文件所有者和文件所有者所属组。

- `path` 为相对路径且 `fd` 为特殊值 `AT_FDCWD` 时，则路径将相对于调用进程的当前工作目录。
- `path` 为相对路径且 `fd` 非 `AT_FDCWD` 时，则路径将相对于 `fd` 引用的文件所属目录。
- `path` 为绝对路径时 `fd` 参数将被忽略。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- owner: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 所有者 `uid`。
- group: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 指定 `gid` 参数。
- flag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 取值可为 `0`，或 `(256)` 如果路径名是符号链接，不会取消引用它，而是返回有关链接本身的信息。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 操作成功时返回 `0`，失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func getcwd() <sup>(deprecated)</sup>

```cangjie
public func getcwd(): String
```

功能：获取当前执行进程工作目录的绝对路径。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 操作成功，返回包含路径信息的字符串，操作失败则返回空字符串。

## func getgid() <sup>(deprecated)</sup>

```cangjie
public func getgid(): UInt32
```

功能：获取用户组 `ID`。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 当前用户组 `ID`。

## func getgroups(Int32, CPointer\<UInt32>) <sup>(deprecated)</sup>

```cangjie
public unsafe func getgroups(size: Int32, gidArray: CPointer<UInt32>): Int32
```

功能：获取当前用户所属组的代码。

如果 `gidArray` 参数大小的值为零，则函数仅返回表示用户所属的组数，不会向 `gidArray` 中放入 `gid`。

> **注意：**
>
> 未来版本即将废弃。

参数：

- size: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - `gidArray` 可以容纳的 `gid` 的数量。
- gidArray: [CPointer](../../core/core_package_api/core_package_intrinsics.md#cpointert)\<[UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32)> - 存放 `gid` 信息。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行成功，返回组代码，执行失败, 返回 `-1`。

## func gethostname() <sup>(deprecated)</sup>

```cangjie
public func gethostname(): String
```

功能：获取主机名称，此名称通常是 `TCP`/`IP` 网络上主机的名称。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 获取到的主机的名称字符串, 获取失败则返回空字符串。

## func getlogin() <sup>(deprecated)</sup>

```cangjie
public func getlogin(): String
```

功能：获取当前登录名。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 操作成功时返回登录名，失败时返回空字串。

## func getos() <sup>(deprecated)</sup>

```cangjie
public func getos(): String
```

功能：从 `/proc/version` 文件中获取 `Linux` 系统的信息。例如: `Linux version 4.15.0-142-generic (buildd@lgw01-amd64-036) (gcc version 7.5.0 (Ubuntu 7.5.0-3ubuntu1~18.04)) #146-Ubuntu SMP Tue Apr 13 01:11:19 UTC 2021`。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 获取到的 Linux 系统的信息字符串。

## func getpgid(Int32) <sup>(deprecated)</sup>

```cangjie
public func getpgid(pid: Int32): Int32
```

功能：获取 `pid` 指定的进程的 `PGID`，如果 `pid` 为零，返回调用进程的进程 `ID`。

> **注意：**
>
> 未来版本即将废弃。

参数：

- pid: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 目标进程 `ID`。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行成功，返回进程组 `ID`，执行失败, 返回 `-1`。

## func getpgrp() <sup>(deprecated)</sup>

```cangjie
public func getpgrp(): Int32
```

功能：获取调用进程的父进程 `ID`。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回调用进程的父进程 `ID`。

## func getpid() <sup>(deprecated)</sup>

```cangjie
public func getpid(): Int32
```

功能：获取调用进程的进程 `ID(PID)`。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回调用进程的进程 `ID(PID)`。

## func getppid() <sup>(deprecated)</sup>

```cangjie
public func getppid(): Int32
```

功能：获取调用进程的父进程 `ID`。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回调用进程的父进程 `ID`。

## func getuid() <sup>(deprecated)</sup>

```cangjie
public func getuid(): UInt32
```

功能：获取调用进程的真实用户 `ID`。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 当前真实用户 `ID`。

## func isatty(Int32) <sup>(deprecated)</sup>

```cangjie
public func isatty(fd: Int32): Bool
```

功能：用于测试文件描述符是否引用终端，成功时返回 `true`，否则返回 `false`。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 操作成功时返回 `true`，否则返回 `false`。

## func isBlk(String) <sup>(deprecated)</sup>

```cangjie
public func isBlk(path: String): Bool
```

功能：检查传入对象是否为块设备，并返回布尔类型。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果是，返回 `true`，否则返回 `false`。

## func isChr(String) <sup>(deprecated)</sup>

```cangjie
public func isChr(path: String): Bool
```

功能：检查传入对象是否为字符设备，返回布尔类型。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果是，返回 `true`，否则返回 `false`。

## func isDir(String) <sup>(deprecated)</sup>

```cangjie
public func isDir(path: String): Bool
```

功能：检查传入对象是否为文件夹，返回布尔类型。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果是，返回 `true`，否则返回 `false`。

## func isFIFO(String) <sup>(deprecated)</sup>

```cangjie
public func isFIFO(path: String): Bool
```

功能：检查传入对象是否为 `FIFO` 文件，返回布尔类型。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果是，返回 `true`，否则返回 `false`。

## func isLnk(String) <sup>(deprecated)</sup>

```cangjie
public func isLnk(path: String): Bool
```

功能：检查传入对象是否为软链路，返回布尔类型。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果是，返回 `true`，否则返回 `false`。

## func isReg(String) <sup>(deprecated)</sup>

```cangjie
public func isReg(path: String): Bool
```

功能：检查传入对象是否为普通文件，返回布尔类型。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果是，返回 `true`，否则返回 `false`。

## func isSock(String) <sup>(deprecated)</sup>

```cangjie
public func isSock(path: String): Bool
```

功能：检查传入对象是否为套接字文件，返回布尔类型。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果是，返回 `true`，否则返回 `false`。

## func isType(String, UInt32) <sup>(deprecated)</sup>

```cangjie
public func isType(path: String, mode: UInt32): Bool
```

功能：检查文件是否为指定模式的文件。如果是，返回 `ture`，否则返回 `false`。根据模式的不同值确定不同的类型。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- mode: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 判断参数。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 如果是指定模式的文件，返回 `true`，否则返回 `false`。

## func kill(Int32, Int32) <sup>(deprecated)</sup>

```cangjie
public func kill(pid: Int32, sig: Int32): Int32
```

功能：系统调用可用于向任何进程组或进程发送任何信号。

- 如果 `pid` 大于 `0`，则信号 `sig` 将发送到 `pid` 对应的进程。
- 如果 `pid` 等于 `0`，然后 `sig` 被发送到调用进程的进程组中的每个进程。
- 如果 `pid` 等于 `-1`，则 `sig` 被发送到调用进程有权发送信号的每个进程。
- 如果 `pid` 小于 `-1`，则将 `sig` 发送到 `ID` 为 `-pid` 的进程组中的每个进程。

> **注意：**
>
> 未来版本即将废弃。

参数：

- pid: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 进程 `ID`。
- sig: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 信号 `ID`。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 操作成功时返回 `0`，否则返回 `-1`。

## func killpg(Int32, Int32) <sup>(deprecated)</sup>

```cangjie
public func killpg(pgid: Int32, sig: Int32): Int32
```

功能：将信号 `sig` 发送到进程组 `pgrp`，如果 `pgrp` 为 `0`，则 [killpg](posix_package_funcs.md#func-killpgint32-int32-deprecated)() 将信号发送到调用进程的进程组。

> **注意：**
>
> 未来版本即将废弃。

参数：

- pgid: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 组 `ID`。
- sig: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 信号 `ID`。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 操作成功时返回 `0`，否则返回 `-1`。

## func lchown(String, UInt32, UInt32) <sup>(deprecated)</sup>

```cangjie
public func lchown(path: String, owner: UInt32, group: UInt32): Int32
```

功能：修改文件链接本身所有者和所有者所属组。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串类型的文件路径。
- owner: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 所有者 `uid`。
- group: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 指定 `gid` 参数。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 操作成功时返回 `0`，失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func link(String, String) <sup>(deprecated)</sup>

```cangjie
public func link(path: String, newpath: String): Int32
```

功能：为存在的文件创建链接，一个文件可以有多个指向其 `i-node` 的目录条目。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- newpath: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 其他文件路径。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功返回 `0`，错误返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 或 `newPath` 包含空字符时，抛出异常。

## func linkat(Int32, String, Int32, String, Int32) <sup>(deprecated)</sup>

```cangjie
public func linkat(fd: Int32, path: String, nfd: Int32, newPath: String, lflag: Int32): Int32
```

功能：创建相对于目录文件描述符的文件链接。

- `path` 为相对路径且 `fd` 为特殊值 `AT_FDCWD` 时，则路径将相对于调用进程的当前工作目录。
- `path` 为相对路径且 `fd` 非 `AT_FDCWD` 时，则路径将相对于 `fd` 引用的文件所属目录。
- `path` 为绝对路径时 `fd` 参数将被忽略。
- `newPath` 的场景与 `path` 相同，只是当 `newPath` 为相对路径时是相对于 `nfd` 引用的文件所属目录。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- nfd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 其他文件描述符。
- newPath: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 其他文件路径，如果 `newpath` 存在，则不会覆盖。
- lflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - [AT_EMPTY_PATH](posix_package_constants_vars.md#const-at_empty_path-deprecated) 或 `AT_SYMLINK_FOLLOW` 或 `0`。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功返回 `0`，错误返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 或 `newPath` 包含空字符时，抛出异常。

## func lseek(Int32, Int64, Int32) <sup>(deprecated)</sup>

```cangjie
public func lseek(fd: Int32, offset: Int64, whence: Int32): Int64
```

功能：当文件进行读或写时，读或写位置相应增加。本函数用于控制文件的读或写位置。调用成功时，返回当前读写位置，即从文件开头开始的字节数。如果发生错误，返回 -1。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 打开文件的文件描述符。
- offset: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 偏移量。
- whence: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 表示控制模式。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 调用成功时，返回当前读写位置，即从文件开头开始的字节数。

## func nice(Int32) <sup>(deprecated)</sup>

```cangjie
public func nice(inc: Int32): Int32
```

功能：更改当前线程的优先级。

成功时返回新值，失败时返回 `-1`。 `inc` 在值大于 `19` 时，返回最大值 `19`。

只有超级用户才能使用负的 `inc` 值，表示优先级高，进程执行得更快。 `inc` 代表当前进程的优先级，取值的范围是 `+19`（低优先级）到 `-20`。

> **注意：**
>
> 未来版本即将废弃。

参数：

- inc: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 当前进程的优先级, 值的范围是 `+19`（低优先级）到 `-20`。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回新优先级值。

## func open64(String, Int32) <sup>(deprecated)</sup>

```cangjie
public func open64(path: String, oflag: Int32): Int32
```

功能：打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。

- 当文件打开方式参数 `oflag` 设置为 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 时，可以通过参数设置文件权限。
- [O_RDONLY](posix_package_constants_vars.md#const-o_rdonly-deprecated)、[O_RDWR](posix_package_constants_vars.md#const-o_rdwr-deprecated)、[O_WRONLY](posix_package_constants_vars.md#const-o_wronly-deprecated) 作为 `oflag` 取值为互斥关系，但可以与其他操作标识一起使用，如 [O_APPEND](posix_package_constants_vars.md#const-o_append-deprecated) 。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- oflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件打开的方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回新的文件描述符，执行失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func open64(String, Int32, UInt32) <sup>(deprecated)</sup>

```cangjie
public func open64(path: String, oflag: Int32, flag: UInt32): Int32
```

功能：打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。

- 当文件打开方式参数 `oflag` 设置为 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 时，可以通过参数设置文件权限。
- [O_RDONLY](posix_package_constants_vars.md#const-o_rdonly-deprecated)、[O_RDWR](posix_package_constants_vars.md#const-o_rdwr-deprecated)、[O_WRONLY](posix_package_constants_vars.md#const-o_wronly-deprecated) 作为 `oflag` 取值为互斥关系，但可以与其他操作标识一起使用，如 [O_APPEND](posix_package_constants_vars.md#const-o_append-deprecated) 。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- oflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件打开的方式。
- flag: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 如果 `oflag` 设置了 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 并且需要创建新文件，则 `flag` 参数标识对新文件的权限，否则 `flag` 不改变文件权限。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回新的文件描述符，执行失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func openat(Int32, String, Int32) <sup>(deprecated)</sup>

```cangjie
public func openat(fd: Int32, path: String, oflag: Int32): Int32
```

功能：打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。

- 当文件打开方式参数 `oflag` 设置为 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 时，可以通过参数设置文件权限。
- [O_RDONLY](posix_package_constants_vars.md#const-o_rdonly-deprecated)、[O_RDWR](posix_package_constants_vars.md#const-o_rdwr-deprecated)、[O_WRONLY](posix_package_constants_vars.md#const-o_wronly-deprecated) 作为 `oflag` 取值为互斥关系，但可以与其他操作标识一起使用，如 [O_APPEND](posix_package_constants_vars.md#const-o_append-deprecated) 。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 路径的文件描述符。
- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- oflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件打开的方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回新的文件描述符，执行失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func openat(Int32, String, Int32, UInt32) <sup>(deprecated)</sup>

```cangjie
public func openat(fd: Int32, path: String, oflag: Int32, flag: UInt32): Int32
```

功能：打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。

- 当文件打开方式参数 `oflag` 设置为 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 时，可以通过参数设置文件权限。
- [O_RDONLY](posix_package_constants_vars.md#const-o_rdonly-deprecated)、[O_RDWR](posix_package_constants_vars.md#const-o_rdwr-deprecated)、[O_WRONLY](posix_package_constants_vars.md#const-o_wronly-deprecated) 作为 `oflag` 取值为互斥关系，但可以与其他操作标识一起使用，如 [O_APPEND](posix_package_constants_vars.md#const-o_append-deprecated) 。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 路径的文件描述符。
- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- oflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件打开的方式。
- flag: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 如果 `oflag` 设置了 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 并且需要创建新文件，则 `flag` 参数标识对新文件的权限，否则 `flag` 不改变文件权限。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回新的文件描述符，执行失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func openat64(Int32, String, Int32) <sup>(deprecated)</sup>

```cangjie
public func openat64(fd: Int32, path: String, oflag: Int32): Int32
```

功能：打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。

- 当文件打开方式参数 `oflag` 设置为 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 时，可以通过参数设置文件权限。
- [O_RDONLY](posix_package_constants_vars.md#const-o_rdonly-deprecated)、[O_RDWR](posix_package_constants_vars.md#const-o_rdwr-deprecated)、[O_WRONLY](posix_package_constants_vars.md#const-o_wronly-deprecated) 作为 `oflag` 取值为互斥关系，但可以与其他操作标识一起使用，如 [O_APPEND](posix_package_constants_vars.md#const-o_append-deprecated) 。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 路径的文件描述符。
- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- oflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件打开的方式。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回新的文件描述符，执行失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func openat64(Int32, String, Int32, UInt32) <sup>(deprecated)</sup>

```cangjie
public func openat64(fd: Int32, path: String, oflag: Int32, flag: UInt32): Int32
```

功能：打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。

- 当文件打开方式参数 `oflag` 设置为 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 时，可以通过参数设置文件权限。
- [O_RDONLY](posix_package_constants_vars.md#const-o_rdonly-deprecated)、[O_RDWR](posix_package_constants_vars.md#const-o_rdwr-deprecated)、[O_WRONLY](posix_package_constants_vars.md#const-o_wronly-deprecated) 作为 `oflag` 取值为互斥关系，但可以与其他操作标识一起使用，如 [O_APPEND](posix_package_constants_vars.md#const-o_append-deprecated) 。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 路径的文件描述符。
- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- oflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件打开的方式。
- flag: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 如果 `oflag` 设置了 [O_CREAT](posix_package_constants_vars.md#const-o_creat-deprecated) 并且需要创建新文件，则 `flag` 参数标识对新文件的权限，否则 `flag` 不改变文件权限。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 返回新的文件描述符，执行失败时返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func pread(Int32, CPointer\<UInt8>, UIntNative, Int32) <sup>(deprecated)</sup>

```cangjie
public unsafe func pread(fd: Int32, buffer: CPointer<UInt8>, nbyte: UIntNative, offset: Int32): IntNative
```

功能：将 `fd` 指向的文件的 `nbyte` 字节传输到 `buffer` 指向的内存中。如果 `nbyte` 为 `0`，则函数无效果，并返回 `0`。返回值是实际读取的字节数。返回值为 `0` 表示到达文件末尾或无法读取数据。此外，文件的读写位置随着读取字节的变化而变化。

建议 `nbyte` 的大小与 `buffer` 的大小相同，且 `buffer` 的大小小于或等于 `150000` 字节。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 待读取文件的文件描述符。
- buffer: [CPointer](../../core/core_package_api/core_package_intrinsics.md#cpointert)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区容器。
- nbyte: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 读取字节数，建议采用 `buffer.size`。
- offset: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 读取位置的偏移量。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 返回实际读取字节数，读取无效时返回 `-1`。

## func pwrite(Int32, CPointer\<UInt8>, UIntNative, Int32) <sup>(deprecated)</sup>

```cangjie
public unsafe func pwrite(fd: Int32, buffer: CPointer<UInt8>, nbyte: UIntNative, offset: Int32): IntNative
```

功能：将 `buffer` 指向的内存中 `nbyte` 字节从指定偏移位置开始写入到 `fd` 指向的文件。指定文件的读写位置会随之移动。

建议 `nbyte` 的大小与 `buffer` 的大小相同，且 `buffer` 的大小小于或等于 `150000` 字节。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 待读取文件的文件描述符。
- buffer: [CPointer](../../core/core_package_api/core_package_intrinsics.md#cpointert)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区容器。
- nbyte: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 读取字节数，建议采用 `buffer.size`。
- offset: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 读取位置的偏移量。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 返回实际写入数，执行失败时返回 `-1`。

## func read(Int32, CPointer\<UInt8>, UIntNative) <sup>(deprecated)</sup>

```cangjie
public unsafe func read(fd: Int32, buffer: CPointer<UInt8>, nbyte: UIntNative): IntNative
```

功能：将 `fd` 指向的文件的 `nbyte` 字节传输到 `buffer` 指向的内存中。如果 `nbyte` 为 `0`，则函数无效果，并返回 `0`。返回值是实际读取的字节数。返回值为 `0` 表示到达文件末尾或无法读取数据。此外，文件的读写位置随着读取字节的变化而变化。

建议 `nbyte` 的大小与 `buffer` 的大小相同，且 `buffer` 的大小小于或等于 `150000` 字节。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 待读取文件的文件描述符。
- buffer: [CPointer](../../core/core_package_api/core_package_intrinsics.md#cpointert)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区容器。
- nbyte: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 读取字节数，建议采用 `buffer.size`。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 返回实际读取字节数，读取无效时返回 `-1`。

## func remove(String) <sup>(deprecated)</sup>

```cangjie
public func remove(path: String): Int32
```

功能：删除文件或目录。

- 对于文件，[remove](posix_package_funcs.md#func-removestring-deprecated)() 等同于 [unlink](posix_package_funcs.md#func-unlinkstring-deprecated)()。
- 对于目录，[remove](posix_package_funcs.md#func-removestring-deprecated)() 等同于 rmdir()。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功返回 `0`，错误返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func rename(String, String) <sup>(deprecated)</sup>

```cangjie
public func rename(oldName: String, newName: String): Int32
```

功能：重命名文件，如果需要将会移动文件所在目录。文件的任何其他硬链接不受影响。旧路径打开的文件描述符也不受影响。

各种限制将决定重命名操作是否成功，具体场景如下：

- 如果 `newName` 已经存在，它将被原子替换，这样另一个尝试访问 `newName` 的进程就不会发现它丢失，但是可能会有一个窗口，其中旧路径和新路径都引用要重命名的文件。
- 如果旧路径和新路径是引用同一文件的现有硬链接，则重命名不做任何操作，并返回成功状态。
- 如果 `newName` 存在，但操作因某种原因失败，则重命名保证保留 `newName` 的实例。
- `oldName` 可以指定目录。在这种情况下，`newName` 必须不存在，或者它必须指定空目录。
- 如果旧路径引用符号链接，则链接将重命名；如果新路径引用符号链接，则链接将被覆盖。

> **注意：**
>
> 未来版本即将废弃。

参数：

- oldName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件名(含路径)。
- newName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件名(含路径)。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功返回 `0`，错误返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `oldName` 或 `newName` 包含空字符时，抛出异常。

## func renameat(Int32, String, Int32, String) <sup>(deprecated)</sup>

```cangjie
public func renameat(oldfd: Int32, oldName: String, newfd: Int32, newName: String): Int32
```

功能：重命名文件，如果需要将会移动文件所在目录。

[renameat](posix_package_funcs.md#func-renameatint32-string-int32-string-deprecated)() 与 [rename](posix_package_funcs.md#func-renamestring-string-deprecated)() 处理相同，此处仅描述两者差异点：

- `oldName` 为相对路径且 `oldfd` 为特殊值 `AT_FDCWD` 时，则路径将相对于调用进程的当前工作目录。
- `oldName` 为相对路径且 `oldfd` 非 `AT_FDCWD` 时，则路径将相对于 `oldfd` 引用的文件所属目录。
- `oldName` 为绝对路径时 `oldfd` 参数将被忽略。
- `newName` 的场景与 `oldName` 相同，只是当 `newName` 为相对路径时是相对于 `newfd` 引用的文件所属目录。

> **注意：**
>
> 未来版本即将废弃。

参数：

- oldfd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- oldName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件名。
- newfd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- newName: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件名。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功返回 `0`，错误返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `oldName` 或 `newName` 包含空字符时，抛出异常。

## func setgid(UInt32) <sup>(deprecated)</sup>

```cangjie
public func setgid(id: UInt32): Int32
```

功能：设置调用进程的有效组 `ID`，需要适当的权限。

> **注意：**
>
> 未来版本即将废弃。

参数：

- id: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 调用进程的有效组 `ID` 号。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 设置成功，返回 `0`，设置失败, 返回 `-1`。

## func sethostname(String) <sup>(deprecated)</sup>

```cangjie
public func sethostname(buf: String): Int32
```

功能：设置主机名，仅超级用户可以调用。

> **注意：**
>
> 未来版本即将废弃。

参数：

- buf: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 需要设置的主机名。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 设置成功，返回 `0`，设置失败, 返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果参数 `buf` 包含空字符则抛出异常。

## func setpgid(Int32, Int32) <sup>(deprecated)</sup>

```cangjie
public func setpgid(pid: Int32, pgrp: Int32): Int32
```

功能：此函数将参数 `pid` 指定的组 `ID` 设置为参数 `pgrp` 指定的组 `ID`。 如果 `pid` 为 `0`，则使用当前进程的组 `ID`。

> **注意：**
>
> 未来版本即将废弃。

参数：

- pid: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 进程 `ID`。
- pgrp: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 进程组 `ID`。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行成功，返回组 `ID`，执行失败, 返回 `-1`。

## func setpgrp() <sup>(deprecated)</sup>

```cangjie
public func setpgrp(): Int32
```

功能：将当前进程所属的组 `ID` 设置为当前进程的进程 `ID`，此函数等同于调用 [setpgid](posix_package_funcs.md#func-setpgidint32-int32-deprecated)(0, 0)。

> **注意：**
>
> 未来版本即将废弃。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 执行成功，返回当前进程的组 `ID`，执行失败, 返回 `-1`。

## func setuid(UInt32) <sup>(deprecated)</sup>

```cangjie
public func setuid(id: UInt32): Int32
```

功能：设置调用进程的有效用户 `ID`，需要适当的权限。

> **注意：**
>
> 未来版本即将废弃。

参数：

- id: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 调用进程的有效用户 `ID` 号。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 设置成功，返回 `0`，设置失败, 返回 `-1`。

## func symlink(String, String) <sup>(deprecated)</sup>

```cangjie
public func symlink(path: String, symPath: String): Int32
```

功能：创建一个名为 `symPath` 链接到 `path` 所指定的文件。

- 符号链接在运行时被解释为链接的内容已被替换到要查找文件或目录的路径中。
- 符号链接可能包含..路径组件，这些组件（如果在链接的开头使用）引用链接所在目录的父目录。
- 符号链接（也称为软链接）可以指向现有文件或不存在的文件，后者被称为悬空链接。
- 符号链接的权限是不相关的，在跟踪链接时，所有权将被忽略，但当请求删除或重命名链接并且链接位于设置了粘滞位的目录中时，所有权将被检查。
- 如果 symPath 已存在，则不会被覆盖。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- symPath: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 链接文件路径。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功返回 `0`，错误返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 或 `symPath` 包含空字符时，抛出异常。

## func symlinkat(String, Int32, String) <sup>(deprecated)</sup>

```cangjie
public func symlinkat(path: String, fd: Int32, symPath: String): Int32
```

功能：创建一个名为 `symPath` 链接到 `path` 与 `fd` 所指定的文件。

- `symPath` 为相对路径且 `fd` 为特殊值 `AT_FDCWD` 时，则路径将相对于调用进程的当前工作目录。
- `symPath` 为相对路径且 `fd` 非 `AT_FDCWD` 时，则路径将相对于 `fd` 引用的文件所属目录。
- `symPath` 为绝对路径时 `fd` 参数将被忽略。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- symPath: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 链接文件路径。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功返回 `0`，错误返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 或 `symPath` 包含空字符时，抛出异常。

## func ttyname(Int32) <sup>(deprecated)</sup>

```cangjie
public func ttyname(fd: Int32): String
```

功能：返回终端名称。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。

返回值：

- [String](../../core/core_package_api/core_package_structs.md#struct-string) - 操作成功时返回路径名，失败时，返回 `NULL`。

## func umask(UInt32) <sup>(deprecated)</sup>

```cangjie
public func umask(cmask: UInt32): UInt32
```

功能：设置权限掩码。

> **注意：**
>
> 未来版本即将废弃。

参数：

- cmask: [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 文件权限参数。

返回值：

- [UInt32](../../core/core_package_api/core_package_intrinsics.md#uint32) - 返回文件上一个掩码的值。

## func unlink(String) <sup>(deprecated)</sup>

```cangjie
public func unlink(path: String): Int32
```

功能：从文件系统中删除文件。

- 如果 `path` 是指向文件的最后一个链接，并且没有进程打开该文件，则该文件将被删除，它使用的空间可供重复使用。
- 如果 `path` 是指向文件的最后一个链接，但仍然有进程打开该文件，该文件将一直存在，直到引用它的最后一个文件描述符关闭。
- 如果 `path` 引用了符号链接，则该链接将被删除。
- 如果 `path` 引用了套接字、FIFO 或设备，则该文件将被删除，但打开对象的进程可能会继续使用它。

> **注意：**
>
> 未来版本即将废弃。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功返回 `0`，错误返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func unlinkat(Int32, String, Int32) <sup>(deprecated)</sup>

```cangjie
public func unlinkat(fd: Int32, path: String, ulflag: Int32): Int32
```

功能：从文件系统中删除文件。

该函数系统调用的操作方式与 [unlink](posix_package_funcs.md#func-unlinkstring-deprecated) 函数完全相同，但此处描述的差异除外：

- `path` 为相对路径且 `fd` 为特殊值 `AT_FDCWD` 时，则路径将相对于调用进程的当前工作目录。
- `path` 为相对路径且 `fd` 非 `AT_FDCWD` 时，则路径将相对于 `fd` 引用的文件所属目录。
- `path` 为绝对路径时 `fd` 参数将被忽略。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 文件描述符。
- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径。
- ulflag: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 可以指定为 `0`，或者可以设置为控制 [unlinkat](posix_package_funcs.md#func-unlinkatint32-string-int32-deprecated)() 操作的标志值按位或运算。标志值当前取值仅支持 [AT_REMOVEDIR](posix_package_constants_vars.md#const-at_removedir-deprecated)。

返回值：

- [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 成功返回 `0`，错误返回 `-1`。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当函数参数 `path` 包含空字符时，抛出异常。

## func write(Int32, CPointer\<UInt8>, UIntNative) <sup>(deprecated)</sup>

```cangjie
public unsafe func write(fd: Int32, buffer: CPointer<UInt8>, nbyte: UIntNative): IntNative
```

功能：将 `buffer` 指向的内存中 `nbyte` 字节写入到 `fd` 指向的文件。指定文件的读写位置会随之移动。

建议 `nbyte` 的大小与 `buffer` 的大小相同，且 `buffer` 的大小小于或等于 `150000` 字节。

> **注意：**
>
> 未来版本即将废弃。

参数：

- fd: [Int32](../../core/core_package_api/core_package_intrinsics.md#int32) - 待写入文件的文件描述符。
- buffer: [CPointer](../../core/core_package_api/core_package_intrinsics.md#cpointert)\<[UInt8](../../core/core_package_api/core_package_intrinsics.md#uint8)> - 缓冲区容器。
- nbyte: [UIntNative](../../core/core_package_api/core_package_intrinsics.md#uintnative) - 读取字节数，建议采用 `buffer.size`。

返回值：

- [IntNative](../../core/core_package_api/core_package_intrinsics.md#intnative) - 返回实际读取字节数，读取无效时返回 `-1`。
