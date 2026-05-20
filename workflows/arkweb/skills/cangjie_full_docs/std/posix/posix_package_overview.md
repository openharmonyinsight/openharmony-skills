# std.posix

## 功能介绍

posix 包封装 POSIX 系统调用，提供跨平台的系统操作接口。

本包提供多平台统一操控能力，目前支持 Linux 平台，macOS 平台，Windows 平台。

> **注意：**
>
> 未来版本即将废弃本包全部内容。

## API 列表

### 函数

|  函数名 | 功能  | 支持平台 |
| ------------ | ------------ | ----------- |
| [open(String, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-openstring-int32-deprecated) | 打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。 | `Linux` `Windows` `macOS` |
| [open(String, Int32, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-openstring-int32-uint32-deprecated) | 打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。 | `Linux` `Windows` `macOS` |
| [access(String, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-accessstring-int32-deprecated) | 判断某个文件是否具有某种权限，具有返回 `0`，否则返回 `-1`。 | `Linux` `Windows` `macOS` |
| [chdir(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-chdirstring-deprecated) | 通过指定路径的方式，更改调用进程的当前工作目录。 | `Linux` `Windows` `macOS` |
| [chmod(String, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-chmodstring-uint32-deprecated) | 修改文件访问权限。 | `Linux` `Windows` `macOS` |
| [chown(String, UInt32, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-chownstring-uint32-uint32-deprecated) | 修改文件所有者和文件所有者所属组。 | `Linux` `macOS` |
| [close(Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-closeint32-deprecated) | 关闭文件，`close` 将会触发数据写回磁盘，并释放文件占用的资源。 | `Linux` `Windows` `macOS` |
| [creat(String, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-creatstring-uint32-deprecated) | 创建文件并为其返回文件描述符，或在失败时返回 `-1`。 | `Linux` `Windows` `macOS` |
| [dup(Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-dupint32-deprecated) | 用于复制旧 `fd` 参数指定的文件描述符并返回。 | `Linux` `Windows` `macOS` |
| [dup2(Int32, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-dup2int32-int32-deprecated) | 用于复制 `oldfd` 参数指定的文件描述符，并将其返回到 `newfd` 参数。 | `Linux` `Windows` `macOS` |
| [faccessat(Int32, String, Int32, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-faccessatint32-string-int32-int32-deprecated) | 判断 `fd` 对应的文件是否具有某种权限，具有返回 `0`，否则返回 `-1`。 | `Linux` `macOS` |
| [fchdir(Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-fchdirint32-deprecated) | 通过指定文件路径的描述符，更改调用进程的当前工作目录。 | `Linux` `macOS` |
| [fchmod(Int32, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-fchmodint32-uint32-deprecated) | 修改文件描述符对应的文件访问权限。 | `Linux` `Windows` `macOS` |
| [fchmodat(Int32, String, UInt32, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-fchmodatint32-string-uint32-int32-deprecated) | 修改文件描述符对应的文件访问权限。 | `Linux` `Windows` `macOS` |
| [fchown(Int32, UInt32, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-fchownint32-uint32-uint32-deprecated) | 修改 `fd` 对应的文件所有者和文件所有者所属组。 | `Linux` `macOS` |
| [fchownat(Int32, String, UInt32, UInt32, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-fchownatint32-string-uint32-uint32-int32-deprecated) | 修改文件描述符对应的文件所有者和文件所有者所属组。 | `Linux` `macOS` |
| [getcwd() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getcwd-deprecated) | 获取当前执行进程工作目录的绝对路径。 | `Linux` `Windows` `macOS` |
| [getgid() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getgid-deprecated) | 获取用户组 `ID`。 | `Linux` `macOS` |
| [getgroups(Int32, CPointer\<UInt32>) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getgroupsint32-cpointeruint32-deprecated) | 获取当前用户所属组的代码。 | `Linux` `macOS` |
| [gethostname() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-gethostname-deprecated) | 获取主机名称，此名称通常是 `TCP/IP` 网络上主机的名称。 | `Linux` `macOS` |
| [getlogin() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getlogin-deprecated) | 获取当前登录名。 | `Linux` `macOS` |
| [getos() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getos-deprecated) | 从 `/proc/version` 文件中获取 `Linux` 系统的信息。 | `Linux` |
| [getpgid(Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getpgidint32-deprecated) | 获取 `pid` 指定的进程的 `PGID`，如果 `pid` 为零，返回调用进程的进程 `ID`。 | `Linux` `macOS` |
| [getpgrp() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getpgrp-deprecated) | 获取调用进程的父进程 `ID`。 | `Linux` `macOS` |
| [getpid() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getpid-deprecated) | 获取调用进程的进程 `ID(PID)`。 | `Linux` `Windows` `macOS` |
| [getppid() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getppid-deprecated) | 获取调用进程的父进程 `ID`。 | `Linux` `macOS` |
| [getuid() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-getuid-deprecated) | 获取调用进程的真实用户 `ID`。 | `Linux` `macOS` |
| [isBlk(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-isblkstring-deprecated) | 检查传入对象是否为块设备，并返回布尔类型。 | `Linux` `Windows` `macOS` |
| [isChr(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-ischrstring-deprecated) | 检查传入对象是否为字符设备，返回布尔类型。 | `Linux` `Windows` `macOS` |
| [isDir(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-isdirstring-deprecated) | 检查传入对象是否为文件夹，返回布尔类型。 | `Linux` `Windows` `macOS` |
| [isFIFO(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-isfifostring-deprecated) | 检查传入对象是否为 `FIFO` 文件，返回布尔类型。 | `Linux` `macOS` |
| [isLnk(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-islnkstring-deprecated) | 检查传入对象是否为软链路，返回布尔类型。 | `Linux` `macOS` |
| [isReg(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-isregstring-deprecated) | 检查传入对象是否为普通文件，返回布尔类型。 | `Linux` `Windows` `macOS` |
| [isSock(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-issockstring-deprecated) | 检查传入对象是否为套接字文件，返回布尔类型。 | `Linux` `macOS` |
| [isType(String, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-istypestring-uint32-deprecated) | 检查文件是否为指定模式的文件。 | `Linux` `macOS` |
| [isatty(Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-isattyint32-deprecated) | 用于测试文件描述符是否引用终端，成功时返回 `true`，否则返回 `false`。 | `Linux` `Windows` `macOS` |
| [kill(Int32, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-killint32-int32-deprecated) | 系统调用可用于向任何进程组或进程发送任何信号。 | `Linux` `macOS` |
| [killpg(Int32, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-killpgint32-int32-deprecated) | 将信号 `sig` 发送到进程组 `pgrp`，如果 `pgrp` 为 `0`，则 killpg() 将信号发送到调用进程的进程组。 | `Linux` `macOS` |
| [lchown(String, UInt32, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-lchownstring-uint32-uint32-deprecated) | 修改文件链接本身所有者和所有者所属组。 | `Linux` `macOS` |
| [link(String, String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-linkstring-string-deprecated) | 为存在的文件创建链接，一个文件可以有多个指向其 `i-node` 的目录条目。 | `Linux` `macOS` |
| [linkat(Int32, String, Int32, String, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-linkatint32-string-int32-string-int32-deprecated) | 创建相对于目录文件描述符的文件链接。 | `Linux` `macOS` |
| [lseek(Int32, Int64, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-lseekint32-int64-int32-deprecated) | 当文件进行读或写时，读或写位置相应增加。 | `Linux` `Windows` `macOS` |
| [nice(Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-niceint32-deprecated) | 更改当前线程的优先级。 | `Linux` `macOS` |
| [open64(String, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-openstring-int32-deprecated) | 打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。 | `Linux` |
| [open64(String, Int32, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-openstring-int32-uint32-deprecated) | 打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。 | `Linux` |
| [openat(Int32, String, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-openatint32-string-int32-deprecated) | 打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。 | `Linux` `macOS` |
| [openat(Int32, String, Int32, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-openatint32-string-int32-uint32-deprecated) | 打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。 | `Linux` `macOS` |
| [openat64(Int32, String, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-openatint32-string-int32-deprecated) | 打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。 | `Linux` `macOS` |
| [openat64(Int32, String, Int32, UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-openatint32-string-int32-uint32-deprecated) | 打开文件并为其返回新的文件描述符，或在失败时返回 `-1`。 | `Linux` `macOS` |
| [pread(Int32, CPointer\<UInt8>, UIntNative, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-preadint32-cpointeruint8-uintnative-int32-deprecated) | 将 `fd` 指向的文件的 `nbyte` 字节传输到 `buffer` 指向的内存中。 | `Linux` `macOS` |
| [pwrite(Int32, CPointer\<UInt8>, UIntNative, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-pwriteint32-cpointeruint8-uintnative-int32-deprecated) | 将 `buffer` 指向的内存中 `nbyte` 字节从指定偏移位置开始写入到 `fd` 指向的文件。 | `Linux` `macOS` |
| [read(Int32, CPointer\<UInt8>, UIntNative) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-readint32-cpointeruint8-uintnative-deprecated) | 将 `fd` 指向的文件的 `nbyte` 字节传输到 `buffer` 指向的内存中。 | `Linux` `Windows` `macOS` |
| [remove(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-removestring-deprecated) | 删除文件或目录。 | `Linux` `Windows` `macOS` |
| [rename(String, String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-renamestring-string-deprecated) | 重命名文件，如果需要将会移动文件所在目录。 | `Linux` `Windows` `macOS` |
| [renameat(Int32, String, Int32, String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-renameatint32-string-int32-string-deprecated) | 重命名文件，如果需要将会移动文件所在目录。 | `Linux` `macOS` |
| [setgid(UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-setgiduint32-deprecated) | 设置调用进程的有效组 `ID`，需要适当的权限。 | `Linux` `macOS` |
| [sethostname(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-sethostnamestring-deprecated) | 设置主机名，仅超级用户可以调用。 | `Linux` `macOS` |
| [setpgid(Int32, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-setpgidint32-int32-deprecated) | 此函数将参数 `pid` 指定的组 `ID` 设置为参数 `pgrp` 指定的组 `ID`。 | `Linux` `macOS` |
| [setpgrp() <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-setpgrp-deprecated) | 将当前进程所属的组 `ID` 设置为当前进程的进程 `ID`，此函数等同于调用 setpgid(0, 0)。 | `Linux` `macOS` |
| [setuid(UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-setuiduint32-deprecated) | 设置调用进程的有效用户 `ID`，需要适当的权限。 | `Linux` `macOS` |
| [symlink(String, String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-symlinkstring-string-deprecated) | 创建一个名为 `symPath` 链接到 `path` 所指定的文件。 | `Linux` `macOS` |
| [symlinkat(String, Int32, String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-symlinkatstring-int32-string-deprecated) | 创建一个名为 `symPath` 链接到 `path` 与 `fd` 所指定的文件。 | `Linux` `macOS` |
| [ttyname(Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-ttynameint32-deprecated) | 返回终端名称。 | `Linux` `Windows` `macOS` |
| [umask(UInt32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-umaskuint32-deprecated) | 设置权限掩码。 | `Linux` `Windows` `macOS` |
| [unlink(String) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-unlinkstring-deprecated) | 从文件系统中删除文件。 | `Linux` `macOS` |
| [unlinkat(Int32, String, Int32) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-unlinkatint32-string-int32-deprecated) | 从文件系统中删除文件。 | `Linux` `macOS` |
| [write(Int32, CPointer\<UInt8>, UIntNative) <sup>(deprecated)</sup>](./posix_package_api/posix_package_funcs.md#func-writeint32-cpointeruint8-uintnative-deprecated) | 将 `buffer` 指向的内存中 `nbyte` 字节写入到 `fd` 指向的文件。 | `Linux` `Windows` `macOS` |

### 常量

| 常量名 | 功能 | 支持平台 |
| ------------ | ------------ | ----------- |
| [AT_EMPTY_PATH <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-at_empty_path-deprecated) | 表示在文件系统中空路径（即没有指定任何文件或目录）时返回的文件描述符，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `Windows` |
| [AT_FDCWD <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-at_fdcwd-deprecated) | 表示在文件系统中相对路径操作的特殊文件描述符常量，用于在使用 `*at()` 系列系统调用时指定相对路径的解析起点。主要用于 `fchmodat`、 `fchownat`、`linkat`、`renameat`、`symlinkat`、`unlinkat` 等函数，所属函数参数 `fd`。 | `Linux` `Windows` `macOS` |
| [AT_REMOVEDIR <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-at_removedir-deprecated) | 如果指定了 `AT_REMOVEDIR` 标志，则对 `pathname` 执行等效于 `rmdir(2)` 的操作，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `Windows` `macOS` |
| [AT_SYMLINK_FOLLOW <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-at_symlink_follow-deprecated) | 表示一个用于控制符号链接解析行为的标志，指定在操作符号链接时是否跟随链接指向的目标文件。通常与 `AT_FDCWD` 结合使用。若无该标志，大多数系统调用会直接操作符号链接本身（如读取链接路径）。使用该标志后，系统调用会先解析符号链接，然后操作其指向的目标文件。主要用于 `linkat`、`unlinkat` 等函数，所属函数参数 `fd`。 | `Linux` `Windows` `macOS` |
| [O_CLOEXEC <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_cloexec-deprecated) | 在某些多线程程序中，使用此标志是必不可少的。因为在一个线程同时打开文件描述符，而另一个线程执行 `fork(2)` 加 `execve(2)` 场景下使用单独的 `fcntl(2)` `F_SETFD` 操作设置 `FD_CLOEXEC` 标志并不足以避免竞争条件，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `macOS` |
| [O_DIRECTORY <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_directory-deprecated) | 如果 `pathname` 指定的文件不是目录，则打开文件失败，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `macOS` |
| [O_CREAT <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_creat-deprecated) | 如果要打开的文件不存在，则自动创建该文件，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `Windows` `macOS` |
| [O_DSYNC <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_dsync-deprecated) | 每次写入都会等待物理 `I/O` 完成，但如果写操作不影响读取刚写入的数据，则不等待文件属性更新，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `macOS` |
| [O_EXCL <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_excl-deprecated) | 如同时设置 `O_CREAT`，则此指令检查文件是否存在。如果文件不存在，则创建文件。否则，打开文件出错。此外，如果同时设置了 `O_CREAT` 和 `O_EXCL`，并且要打开的文件是符号链接，则打开文件失败，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `Windows` `macOS` |
| [O_NOCTTY <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_noctty-deprecated) | 如要打开的文件是终端设备，则该文件不会成为这个进程的控制终端，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `macOS` |
| [O_NOFOLLOW <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_nofollow-deprecated) | 如 `pathname` 指定的文件是单符号链接，则打开文件失败，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `macOS` |
| [O_NONBLOCK <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_nonblock-deprecated) | 以非阻塞的方式打开文件，即 `I/O` 操作不会导致调用进程等待，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `macOS` |
| [O_SYNC <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_sync-deprecated) | 同步打开文件，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `macOS` |
| [O_RDONLY <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_rdonly-deprecated) | 以只读方式打开文件，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `Windows` `macOS` |
| [O_RDWR <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_rdwr-deprecated) | 以读写模式打开文件，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `Windows` `macOS` |
| [O_WRONLY <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_wronly-deprecated) | 以只写方式打开文件，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `Windows` `macOS` |
| [O_APPEND <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_append-deprecated) | 读取或写入文件时，数据将从文件末尾移动。即写入的数据将附加到文件的末尾，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `Windows` `macOS` |
| [O_RSYNC <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_rsync-deprecated) | 此标志仅影响读取操作，必须与 `O_SYNC` 或 `O_DSYNC` 结合使用。如果有必要，它将导致读取调用阻塞，直到正在读取的数据（可能还有元数据）刷新到磁盘，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` |
| [O_TRUNC <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-o_trunc-deprecated) | 如果文件存在且打开可写，则此标志将文件长度清除为 0，文件中以前存储的数据消失，适用函数 `open`、`open64`、`openat`、`openat64`，所属函数参数 `oflag`。 | `Linux` `Windows` `macOS` |
| [R_OK <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-r_ok-deprecated) | 测试文件读权限，适用函数 `access`，`faccessat`，所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [W_OK <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-w_ok-deprecated) | 测试文件写权限，适用函数 `access`，`faccessat`，所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [X_OK <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-x_ok-deprecated) | 测试文件执行权限，适用函数 `access`，`faccessat`，所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [F_OK <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-f_ok-deprecated) | 测试文件是否存在，适用函数 `access`，`faccessat`，所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [SEEK_SET <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-seek_set-deprecated) | 偏移参数表示新的读写位置，适用函数 `lseek`，所属函数参数 `whence`。 | `Linux` `Windows` `macOS` |
| [SEEK_CUR <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-seek_cur-deprecated) | 向当前读或写位置添加偏移量，适用函数 `lseek`，所属函数参数 `whence`。 | `Linux` `Windows` `macOS` |
| [SEEK_END <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-seek_end-deprecated) | 将读写位置设置为文件末尾，并添加偏移量，适用函数 `lseek`，所属函数参数 `whence`。 | `Linux` `Windows` `macOS` |
| [SIGABRT <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigabrt-deprecated) | 异常终止，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGBUS <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigbus-deprecated) | 硬件故障，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGFPE <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigfpe-deprecated) | 算术错误，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGKILL <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigkill-deprecated) | 终止，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGCONT <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigcont-deprecated) | 暂停过程的继续，默认操作继续或忽略，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGHUP <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sighup-deprecated) | 连接已断开，默认操作已终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGINT <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigint-deprecated) | 终端中断字符，默认动作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGQUIT <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigquit-deprecated) | 终端退出字符，默认动作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGILL <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigill-deprecated) | 硬件指令无效，默认动作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGTRAP <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigtrap-deprecated) | 硬件故障，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGIOT <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigiot-deprecated) | 硬件故障，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGIO <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigio-deprecated) | 异步 `IO`，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGPIPE <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigpipe-deprecated) | 写入未读进程的管道，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGALRM <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigalrm-deprecated) | 计时器到期，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGPWR <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigpwr-deprecated) | 电源故障或重启，系统调用无效，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` |
| [SIGSEGV <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigsegv-deprecated) | 内存引用无效，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGSTOP <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigstop-deprecated) | 停止，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGSYS <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigsys-deprecated) | 终止，默认操作终止进程并生成核心转储文件（core dump），用于调试分析，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGTERM <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigterm-deprecated) | 终止，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGSTKFLT <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigstkflt-deprecated) | 协处理器堆栈故障，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` |
| [SIGCHLD <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigchld-deprecated) | 子进程状态更改，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGTSTP <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigtstp-deprecated) | 终端停止符号，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGTTIN <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigttin-deprecated) | 后台读取控件 `tty`，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGTTOU <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigttou-deprecated) | 后台写控制 `tty`，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGURG <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigurg-deprecated) | 紧急情况（套接字），忽略默认操作，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGUSR1 <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigusr1-deprecated) | 用户定义的信号，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGUSR2 <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigusr2-deprecated) | 用户定义的信号，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGVTALRM <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigvtalrm-deprecated) | 虚拟时间警报，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGPROF <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigprof-deprecated) | 摘要超时，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGWINCH <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigwinch-deprecated) | 终端窗口大小更改，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGXCPU <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigxcpu-deprecated) | `CPU` 占用率超过上限，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [SIGXFSZ <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-sigxfsz-deprecated) | 文件长度超过上限，默认操作终止，适用函数 `kill`，`killpg`，所属函数参数 `sig`。 | `Linux` `Windows` `macOS` |
| [S_IRUSR <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_irusr-deprecated) | 表示文件所有者具有读权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IWUSR <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_iwusr-deprecated) | 表示文件所有者具有写权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IRGRP <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_iwgrp-deprecated) | 表示文件用户组具有读权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IWGRP <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_iwgrp-deprecated) | 表示文件用户组具有写权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IFREG <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_ifreg-deprecated) | 文件类型为一般文件，适用函数 `isType`， 所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [S_IFBLK <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_ifblk-deprecated) | 文件类型为块设备，适用函数 `isType`， 所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [S_IFDIR <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_ifdir-deprecated) | 文件类型为目录，适用函数 `isType`， 所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [S_IFCHR <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_ifchr-deprecated) | 文件类型为字符设备，适用函数 `isType`， 所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [S_IFIFO <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_ififo-deprecated) | 文件类型为 `FIFO` 文件，适用函数 `isType`， 所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [S_IFLNK <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_iflnk-deprecated) | 文件类型为软连接，适用函数 `isType`， 所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [S_IFSOCK <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_ifsock-deprecated) | 文件类型为套接字文件，适用函数 `isType`， 所属函数参数 `mode`。 | `Linux` `Windows` `macOS` |
| [S_IROTH <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_iroth-deprecated) | 表示其他用户对文件具有读权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IRWXG <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_irwxg-deprecated) | 表示文件用户组具有读、写、执行权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IRWXU <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_irwxu-deprecated) | 表示文件所有者具有读、写和执行权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IWOTH <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_iwoth-deprecated) | 表示其他用户对文件具有写权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IXOTH <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_ixoth-deprecated) | 表示其他用户对文件具有执行权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IRWXO <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_irwxo-deprecated) | 表示其他用户对文件具有读、写和执行权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IXGRP <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_ixgrp-deprecated) | 表示文件用户组具有执行权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
| [S_IXUSR <sup>(deprecated)</sup>](./posix_package_api/posix_package_constants_vars.md#const-s_ixusr-deprecated) | 表示文件所有者具有执行权限，适用函数 `open`，`open64`，`openat`，`openat64`，`chmod(mode)`，`fchmod(mode)`，`fchmodat(mode)`，`creat`， 所属函数参数 `flag`。 | `Linux` `Windows` `macOS` |
