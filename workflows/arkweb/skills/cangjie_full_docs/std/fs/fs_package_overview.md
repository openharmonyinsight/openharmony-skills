# std.fs

## 功能介绍

fs（file system）包提供对文件、文件夹、路径、文件元数据信息的一些操作函数。

目前支持 Linux，macOS，Windows 平台下使用。

## API 列表

### 函数

|                 函数名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [canonicalize(Path)](./fs_package_api/fs_package_funcs.md#func-canonicalizepath) | 将 [Path](./fs_package_api/fs_package_structs.md#struct-path) 实例规范化，获取绝对路径形式的规范化路径。  |
| [canonicalize(String)](./fs_package_api/fs_package_funcs.md#func-canonicalizestring) | 用 path 字符串构造 [Path](./fs_package_api/fs_package_structs.md#struct-path) 实例，并进行规范化，获取绝对路径形式的规范化路径。   |
| [copy(Path, Path, Bool)](./fs_package_api/fs_package_funcs.md#func-copypath-path-bool)| 实现文件系统的拷贝功能，用于于复制文件或目录。|
| [copy(String, String, Bool)](./fs_package_api/fs_package_funcs.md#func-copystring-string-bool)| 实现文件系统的拷贝功能，用于于复制文件或目录。|
| [exists(Path)](./fs_package_api/fs_package_funcs.md#func-existspath) | 判断目标地址是否存在。 |
| [exists(String)](./fs_package_api/fs_package_funcs.md#func-existsstring) | 判断目标地址是否存在。 |
| [rename(Path, Path, Bool)](./fs_package_api/fs_package_funcs.md#func-renamepath-path-bool)|重命名文件。|
| [rename(String, String, Bool)](./fs_package_api/fs_package_funcs.md#func-renamestring-string-bool)|重命名文件。|
| [remove(Path, Bool)](./fs_package_api/fs_package_funcs.md#func-removepath-bool)|删除文件或目录。|
| [remove(String, Bool)](./fs_package_api/fs_package_funcs.md#func-removestring-bool)|删除文件或目录。|
| [removeIfExists(Path, Bool)](./fs_package_api/fs_package_funcs.md#func-removeifexistspath-bool)|判断目标是否存在，如果存在则删除。|
| [removeIfExists(String, Bool)](./fs_package_api/fs_package_funcs.md#func-removeifexistsstring-bool)|判断目标是否存在，如果存在则删除。|

### 类

|                 类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [Directory](./fs_package_api/fs_package_classes.md#class-directory) | 对应文件系统中的目录，它提供创建、查询属性以及遍历目录等能力。  |
| [File](./fs_package_api/fs_package_classes.md#class-file) | 提供一些对文件进行操作的函数，包括文件的打开、创建、关闭、文件的流式读写操作、查询属性以及一些其他函数。   |
| [HardLink](./fs_package_api/fs_package_classes.md#class-hardlink) | 提供处理文件系统硬链接相关接口。 |
| [SymbolicLink](./fs_package_api/fs_package_classes.md#class-symboliclink) | 提供处理文件系统符号链接相关接口。 |

### 枚举

|              枚举名          |           功能           |
| --------------------------- | ------------------------ |
| [OpenMode](./fs_package_api/fs_package_enums.md#enum-openmode) | 表示不同的文件打开模式。 |

### 结构体

|              结构体名          |           功能           |
| --------------------------- | ------------------------ |
| [FileDescriptor](./fs_package_api/fs_package_structs.md#struct-filedescriptor) | 用于获取文件句柄信息。 |
| [FileInfo](./fs_package_api/fs_package_structs.md#struct-fileinfo) | 对应文件系统中的文件元数据，提供一些文件属性的查询和设置等函数。 |
| [Path](./fs_package_api/fs_package_structs.md#struct-path) | 提供路径相关的函数。 |

### 异常类

|              异常类名          |           功能           |
| --------------------------- | ------------------------ |
| [FSException](./fs_package_api/fs_package_exceptions.md#class-fsexception) | 文件流异常类，继承了 IO 流异常类。 |
