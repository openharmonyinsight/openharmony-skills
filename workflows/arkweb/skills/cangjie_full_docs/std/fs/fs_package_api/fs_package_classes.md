# 类

## class Directory

```cangjie
public class Directory {}
```

功能：对应文件系统中的目录，它提供创建、移动、复制、删除、查询属性以及遍历目录等能力。

> **说明：**
>
> 非法路径指的是以下情况之一：
>
> - 路径中包含非法字符，例如空格、制表符、换行符等；
> - 路径中包含不合法的字符，例如特殊字符、控制字符等；
> - 路径中包含不存在的目录或文件；
> - 路径中包含无法访问的目录或文件，例如权限不足或被锁定等。

在输入路径时，应该避免使用非法字符，确保路径的合法性，以便正确地访问目标文件或目录。

### static func create(Path, Bool)

```cangjie
public static func create(path: Path, recursive!: Bool = false): Unit
```

功能：创建目录。

可指定是否递归创建，如果需要递归创建，将逐级创建路径中不存在的目录。

参数：

- path: [Path](fs_package_structs.md#struct-path) - 待创建的目录路径。
- recursive!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否递归创建目录，true 代表递归创建，false 代表不递归创建，默认 false。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 目录已存在、非递归创建时中间有不存在的目录、权限不足或其他原因导致无法创建目录时，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 目录为空、目录为当前目录、目录为根目录或目录中存在空字符时抛出异常。

### static func create(String, Bool)

```cangjie
public static func create(path: String, recursive!: Bool = false): Unit
```

功能：创建目录。

可指定是否递归创建，如果需要递归创建，将逐级创建路径中不存在的目录。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待创建的目录路径。
- recursive!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否递归创建目录，true 代表递归创建，false 代表不递归创建，默认 false。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 目录已存在、非递归创建时中间有不存在的目录、权限不足或其他原因导致无法创建目录时，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 目录为空、目录为当前目录、目录为根目录或目录中存在空字符时抛出异常。

### static func createTemp(Path)

```cangjie
public static func createTemp(directoryPath: Path): Path
```

功能：在指定目录下创建临时目录。

参数：

- directoryPath: [Path](fs_package_structs.md#struct-path) - [Path](fs_package_structs.md#struct-path) 形式的目录路径。

返回值：

- [Path](./fs_package_structs.md#struct-path) - 临时目录对应的路径。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 目录不存在或其他原因导致创建失败时抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 目录为空或包含空字符时抛出异常。

### static func createTemp(String)

```cangjie
public static func createTemp(directoryPath: String): Path
```

功能：在指定目录下创建临时目录。

参数：

- directoryPath: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 字符串形式的目录路径。

返回值：

- [Path](./fs_package_structs.md#struct-path) - 临时目录对应的路径。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 目录不存在或其他原因导致创建失败时抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 目录为空或包含空字符时抛出异常。

### static func isEmpty(Path)

```cangjie
public static func isEmpty(path: Path): Bool
```

功能：判断指定目录是否为空。

参数：

- path: [Path](./fs_package_structs.md#struct-path) - 待判断是否为空的目录对应的路径。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 为 true 时目录为空，为 false 时不为空。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 如果指定路径不存在、指定路径不是目录或判断过程中底层接口发生错误，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当指定路径为空或包含空字符时，抛出异常。

### static func isEmpty(String)

```cangjie
public static func isEmpty(path: String): Bool
```

功能：判断指定目录是否为空。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待判断是否为空的目录对应的路径。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 为 true 时目录为空，为 false 时不为空。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 如果指定路径不存在、指定路径不是目录或判断过程中底层接口发生错误，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当指定路径为空或包含空字符时，抛出异常。

### static func readFrom(Path)

```cangjie
public static func readFrom(path: Path): Array<FileInfo>
```

功能：获取当前目录的子项目列表。

子项目在数组中的顺序取决于文件在系统中的排序。

参数：

- path: [Path](./fs_package_structs.md#struct-path) - 待读取其子项的目录对应的路径。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[FileInfo](fs_package_structs.md#struct-fileinfo)> - 当前目录的子项目列表。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 当指定路径不存在、指定路径不是目录或获取目录的成员信息失败时，抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当指定路径为空或包含空字符时，抛出异常。

### static func readFrom(String)

```cangjie
public static func readFrom(path: String): Array<FileInfo>
```

功能：获取当前目录的子项目列表。

子项目在数组中的顺序取决于文件在系统中的排序。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待读取其子项目的目录对应的路径。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[FileInfo](./fs_package_structs.md#struct-fileinfo)> - 当前目录的子项目列表。

异常：

- [FSException](./fs_package_exceptions.md#class-fsexception) - 当指定路径不存在、指定路径不是目录或获取目录的成员信息失败时，抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当指定路径为空或包含空字符时，抛出异常。

### static func walk(Path, (FileInfo)->Bool)

```cangjie
public static func walk(path: Path, f: (FileInfo)->Bool): Unit
```

功能：遍历 path 对应的目录下的子项目（非递归，即不包含子目录的子项目），对每一个子项目执行回调函数。

walk 函数退出条件为遍历结束或回调函数 f 返回 false。遍历顺序取决于文件在系统中的排序。

参数：

- path: [Path](./fs_package_structs.md#struct-path) - 待遍历的目录对应的路径。
- f: ([FileInfo](./fs_package_structs.md#struct-fileinfo)) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 对每一个子项目执行的回调函数，入参为子项目对应的元信息，返回值表示是否继续遍历。

异常：

- [FSException](./fs_package_exceptions.md#class-fsexception) - 当指定路径不存在、指定路径不是目录或获取目录的成员信息失败时，抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当指定路径为空或包含空字符时，抛出异常。

### static func walk(String, (FileInfo)->Bool)

```cangjie
public static func walk(path: String, f: (FileInfo)->Bool): Unit
```

功能：遍历 path 对应的目录下的子项目（非递归，即不包含子目录的子项目），对每一个子项目执行回调函数。

walk 函数退出条件为遍历结束或回调函数 f 返回 false。遍历顺序取决于文件在系统中的排序。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待遍历的目录对应的路径。
- f: ([FileInfo](./fs_package_structs.md#struct-fileinfo)) -> [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 对每一子项目执行的回调函数，入参为子项目对应的元信息，返回值表示是否继续遍历。

异常：

- [FSException](./fs_package_exceptions.md#class-fsexception) - 当指定路径不存在、指定路径不是目录或获取目录的成员信息失败时，抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 当指定路径为空或包含空字符时，抛出异常。

## class File

```cangjie
public class File <: Resource & IOStream & Seekable {
    public init(path: String, mode: OpenMode)
    public init(path: Path, mode: OpenMode)
}
```

功能：提供一些对文件进行操作的函数，包括文件的打开、创建、关闭、移动、复制、删除，文件的流式读写操作，查询属性以及一些其他函数。

> **说明：**
>
> 非法路径指的是以下情况之一：
>
> - 路径中包含非法字符，例如空格、制表符、换行符等；
> - 路径中包含不合法的字符，例如特殊字符、控制字符等；
> - 路径中包含不存在的目录或文件；
> - 路径中包含无法访问的目录或文件，例如权限不足或被锁定等。

在输入路径时，应该避免使用非法字符，确保路径的合法性，以便正确地访问目标文件或目录。

> **注意：**
>
> 创建的 [File](fs_package_classes.md#class-file) 对象会默认打开对应的文件，当使用结束后需要及时调用 [close](fs_package_classes.md#func-close) 函数关闭文件，否则会造成资源泄露。

父类型：

- [Resource](../../core/core_package_api/core_package_interfaces.md#interface-resource)
- [IOStream](../../io/io_package_api/io_package_interfaces.md#interface-iostream)
- [Seekable](../../io/io_package_api/io_package_interfaces.md#interface-seekable)

### prop fileDescriptor

```cangjie
public prop fileDescriptor: FileDescriptor
```

功能：获取文件描述符信息。

类型：[FileDescriptor](fs_package_structs.md#struct-filedescriptor)

### prop info

```cangjie
public prop info: FileInfo
```

功能：获取文件元数据信息。

类型：[FileInfo](fs_package_structs.md#struct-fileinfo)

### prop length

```cangjie
public prop length: Int64
```

功能：获取文件头至文件尾的数据字节数。

类型：[Int64](../../core/core_package_api/core_package_intrinsics.md#int64)

### init(Path, OpenMode)

```cangjie
public init(path: Path, mode: OpenMode)
```

功能：创建一个 [File](fs_package_classes.md#class-file) 对象。

需指定文件路径和文件打开方式（读写权限），路径支持相对路径和绝对路径。

参数：

- path: [Path](fs_package_structs.md#struct-path) - 文件路径。
- mode: [OpenMode](fs_package_enums.md#enum-openmode) - 文件打开模式。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 如果以只读方式打开文件但文件不存在、文件的父目录不存在或其他原因导致无法打开文件，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 path 为空路径或者 path 路径中包含空字符，则抛出异常。

### init(String, OpenMode)

```cangjie
public init(path: String, mode: OpenMode)
```

功能：创建 [File](fs_package_classes.md#class-file) 对象。

需指定文件路径和文件打开方式（读写权限），路径支持相对路径和绝对路径。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径字符串。
- mode: [OpenMode](fs_package_enums.md#enum-openmode) - 文件打开模式。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 如果以只读方式打开文件但文件不存在、文件的父目录不存在或其他原因导致无法打开文件，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 path 是空字符串或者 path 包含空字符，则抛出异常。

### static func appendTo(Path, Array\<Byte>)

```cangjie
public static func appendTo(path: Path, buffer: Array<Byte>): Unit
```

功能：打开指定路径的文件并将 buffer 以追加的方式写入，文件不存在则将创建文件。

参数：

- path: [Path](fs_package_structs.md#struct-path) - 文件路径。
- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 待写入的 bytes。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 文件打开失败或写入失败，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果文件路径为空或包含空字符，则抛出异常。

### static func appendTo(String, Array\<Byte>)

```cangjie
public static func appendTo(path: String, buffer: Array<Byte>): Unit
```

功能：打开指定路径的文件并将 buffer 以追加的方式写入，文件不存在则将创建文件。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径字符串。
- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 待写入的 bytes。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 文件打开失败或写入失败，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果文件路径为空或包含空字符，则抛出异常。

### static func create(Path)

```cangjie
public static func create(path: Path): File
```

功能：创建指定路径的文件并返回只写模式的 [File](#class-file) 实例。

参数：

- path: [Path](fs_package_structs.md#struct-path) - 文件路径。

返回值：

- [File](fs_package_classes.md#class-file) - [File](fs_package_classes.md#class-file) 实例。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 如果路径指向的文件的上级目录不存在或文件已存在，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果文件路径为空或包含空字符，则抛出异常。

### static func create(String)

```cangjie
public static func create(path: String): File
```

功能：创建指定路径的文件并返回只写模式的 [File](#class-file) 实例。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径字符串。

返回值：

- [File](fs_package_classes.md#class-file) - [File](fs_package_classes.md#class-file) 实例。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 如果路径指向的文件的上级目录不存在或文件已存在，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果文件路径为空字符串或包含空字符，则抛出异常。

### static func createTemp(Path)

```cangjie
public static func createTemp(directoryPath: Path): File
```

功能：在指定目录下创建临时文件。

创建的文件名称是 tmpFileXXXXXX 形式，不使用的临时文件应手动删除。

参数：

- directoryPath: [Path](fs_package_structs.md#struct-path) - 目录路径。

返回值：

- [File](fs_package_classes.md#class-file) - 临时文件 [File](fs_package_classes.md#class-file) 实例。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 创建文件失败或路径不存在则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果文件路径为空或包含空字符，则抛出异常。

### static func createTemp(String)

```cangjie
public static func createTemp(directoryPath: String): File
```

功能：在指定目录下创建临时文件。

创建的文件名称是 tmpFileXXXXXX 形式，不使用的临时文件应手动删除。

参数：

- directoryPath: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 目录路径字符串。

返回值：

- [File](fs_package_classes.md#class-file) - 临时文件 [File](fs_package_classes.md#class-file) 实例。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 创建文件失败或路径不存在则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果文件路径为空字符串或包含空字符，则抛出异常。

### static func readFrom(Path)

```cangjie
public static func readFrom(path: Path): Array<Byte>
```

功能：根据指定路径读取文件全部内容，以字节数组的形式返回其内容。

参数：

- path: [Path](fs_package_structs.md#struct-path) - 文件路径。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 字节数组形式的文件全部内容。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 文件路径为空、文件不可读、文件读取失败，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 文件路径包含空字符则抛出异常。

### static func readFrom(String)

```cangjie
public static func readFrom(path: String): Array<Byte>
```

功能：根据指定路径读取文件全部内容，以字节数组的形式返回其内容。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径字符串。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 字节数组形式的文件全部内容。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 文件读取失败、文件关闭失败、文件路径为空、文件不可读，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 文件路径包含空字符则抛出异常。

### static func writeTo(Path, Array\<Byte>)

```cangjie
public static func writeTo(path: Path, buffer: Array<Byte>): Unit
```

功能：打开指定路径的文件并将 buffer 以覆盖的方式写入，即文件存在时会将该文件截断为零字节大小，文件不存在则将创建文件。

参数：

- path: [Path](fs_package_structs.md#struct-path) - 文件路径。
- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 待写入的 bytes。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 文件打开失败或写入失败，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果文件路径为空或包含空字符，则抛出异常。

### static func writeTo(String, Array\<Byte>)

```cangjie
public static func writeTo(path: String, buffer: Array<Byte>): Unit
```

功能：打开指定路径的文件并将 buffer 以覆盖的方式写入，即文件存在时会将该文件截断为零字节大小，文件不存在则将创建文件。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 文件路径字符串。
- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 待写入的 bytes。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 文件打开失败或写入失败，则抛出异常。
- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果文件路径为空字符串或包含空字符，则抛出异常。

### func canRead()

```cangjie
public func canRead(): Bool
```

功能：判断当前 [File](fs_package_classes.md#class-file) 对象是否可读。

该函数返回值由创建文件对象的 openMode 所决定，文件对象关闭后返回 false。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回 true 表示可读，返回 false 表示不可读或文件对象已关闭。

### func canWrite()

```cangjie
public func canWrite(): Bool
```

功能：判断当前 [File](fs_package_classes.md#class-file) 对象是否可写。

该函数返回值由创建文件对象的 openMode 所决定，文件对象关闭后返回 false。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 返回 true 表示可写，false 表示不可写或文件对象已关闭。

### func close()

```cangjie
public func close(): Unit
```

功能：关闭当前 [File](fs_package_classes.md#class-file) 对象。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 如果关闭失败，则抛出异常。

### func flush()

```cangjie
public func flush(): Unit
```

功能：将缓冲区数据写入流。由于 [File](fs_package_classes.md#class-file) 不存在缓冲区，所以该函数没有具体作用。

### func isClosed()

```cangjie
public func isClosed(): Bool
```

功能：判断当前 [File](fs_package_classes.md#class-file) 对象是否已关闭。

返回值：

- [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - true 表示已关闭，false 表示未关闭。

### func read(Array\<Byte>)

```cangjie
public func read(buffer: Array<Byte>): Int64
```

功能：从文件中读出数据到 buffer 中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 读取数据存放的缓冲区。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 读取成功，返回读取字节数，如果文件被读完，返回 0。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 如果 buffer 为空，则抛出异常。
- [FSException](fs_package_exceptions.md#class-fsexception) - 读取失败、文件已关闭或文件不可读，则抛出异常。

### func seek(SeekPosition)

```cangjie
public func seek(sp: SeekPosition): Int64
```

功能：将光标跳转到指定位置。

指定的位置不能位于文件头部之前，指定位置可以超过文件末尾，但指定位置到文件头部的最大偏移量不能超过当前文件系统允许的最大值，这个最大值接近当前文件系统的所允许的最大文件大小，一般为最大文件大小减去 4096 个字节。

参数：

- sp: [SeekPosition](../../io/io_package_api/io_package_enums.md#enum-seekposition) - 指定光标跳转后的位置。

返回值：

- [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 返回文件头部到跳转后位置的偏移量（以字节为单位）。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 指定位置不满足以上情况时或文件不能 seek 时均会抛出异常。

### func setLength(Int64)

```cangjie
public func setLength(length: Int64): Unit
```

功能：将当前文件截断为指定长度。当 length 大于当前文件长度时，则将使用 0 填充文件直到目标长度。此方法不会改变文件光标的位置。

参数：

- length: [Int64](../../core/core_package_api/core_package_intrinsics.md#int64) - 指定截断的长度。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 指定的长度为负数时抛出异常。
- [FSException](fs_package_exceptions.md#class-fsexception) - 文件截断操作失败时，抛出异常。

### func write(Array\<Byte>)

```cangjie
public func write(buffer: Array<Byte>): Unit
```

功能：将 buffer 中的数据写入到文件中。

参数：

- buffer: [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<[Byte](../../core/core_package_api/core_package_types.md#type-byte)> - 待写入数据的缓冲区，若 buffer 为空则直接返回。

异常：

- [FSException](fs_package_exceptions.md#class-fsexception) - 如果写入失败、只写入了部分数据、文件已关闭或文件不可写则抛出异常。

## class HardLink

```cangjie
public class HardLink {}
```

功能：提供处理文件系统硬链接相关接口。

### static func create(Path, Path)

```cangjie
public static func create(link: Path, to!: Path): Unit
```

功能：创建一个新的硬链接到现有路径。如果新的路径存在，则不会覆盖。

参数：

- link: [Path](fs_package_structs.md#struct-path) - 新路径的名称。
- to!: [Path](fs_package_structs.md#struct-path) - 现有路径的名称。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数中路径为空、或者包含空字符时抛出异常。
- [FSException](fs_package_exceptions.md#class-fsexception) - 创建硬链接失败时，抛出异常。

### static func create(String, String)

```cangjie
public static func create(link: String, to!: String): Unit
```

功能：创建一个新的硬链接到现有路径。如果新的路径存在，则不会覆盖。

参数：

- link: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 新路径的名称。
- to!: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 现有路径的名称。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数中路径为空、或者包含空字符时抛出异常。
- [FSException](fs_package_exceptions.md#class-fsexception) - 创建硬链接失败时，抛出异常。

## class SymbolicLink

```cangjie
public class SymbolicLink {}
```

功能：提供处理文件系统符号链接相关接口。

### static func create(Path, Path)

```cangjie
public static func create(link: Path, to!: Path): Unit
```

功能：创建一个新的符号链接到现有路径。

> **说明：**
>
> 在 Windows 上，创建一个目标不存在的符号链接时，会创建一个文件符号链接，如果目标路径后来被创建为目录，则符号链接将不起作用。

参数：

- link: [Path](fs_package_structs.md#struct-path) - 待创建的符号链接。
- to!: [Path](fs_package_structs.md#struct-path) - 待创建的符号链接的目标的路径。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数中路径为空、或者包含空字符时抛出异常。
- [FSException](fs_package_exceptions.md#class-fsexception) - 创建符号链接失败时，抛出异常。

### static func create(String, String)

```cangjie
public static func create(link: String, to!: String): Unit
```

功能：创建一个新的符号链接到现有路径。

> **说明：**
>
> 在 Windows 上，创建一个目标不存在的符号链接时，会创建一个文件符号链接，如果目标路径后来被创建为目录，则符号链接将不起作用。

参数：

- link: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待创建的符号链接。
- to!: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 待创建的符号链接的目标的路径。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数中路径为空、或者包含空字符时抛出异常。
- [FSException](fs_package_exceptions.md#class-fsexception) - 创建符号链接失败时，抛出异常。

### static func readFrom(Path, Bool)

```cangjie
public static func readFrom(path: Path, recursive!: Bool = false): Path
```

功能：获取指定符号链接的目标。当指定 'recursive' 为 'true' 时，表示跟踪指向最终目标的链接，并且返回目标的全路径，当指定 'recursive' 为 'false' 时，读取当前目标链接并且返回。

参数：

- path: [Path](fs_package_structs.md#struct-path) - 符号链接的地址。
- recursive!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否递归读取目标地址，默认为 'false'。

返回值：

- [Path](fs_package_structs.md#struct-path) - 符号链接的目标地址。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数中路径为空、或者包含空字符时抛出异常。
- [FSException](fs_package_exceptions.md#class-fsexception) - 读取符号链接失败时，抛出异常。

### static func readFrom(String, Bool)

```cangjie
public static func readFrom(path: String, recursive!: Bool = false): Path
```

功能：获取指定符号链接的目标。当指定 'recursive' 为 'true' 时，表示跟踪指向最终目标的链接，并且返回目标的全路径，当指定 'recursive' 为 'false' 时，读取当前目标链接并且返回。

参数：

- path: [String](../../core/core_package_api/core_package_structs.md#struct-string) - 符号链接的地址。
- recursive!: [Bool](../../core/core_package_api/core_package_intrinsics.md#bool) - 是否递归读取目标地址，默认为 'false'。

返回值：

- [Path](fs_package_structs.md#struct-path) - 符号链接的目标地址。

异常：

- [IllegalArgumentException](../../core/core_package_api/core_package_exceptions.md#class-illegalargumentexception) - 参数中路径为空、或者包含空字符时抛出异常。
- [FSException](fs_package_exceptions.md#class-fsexception) - 读取符号链接失败时，抛出异常。
