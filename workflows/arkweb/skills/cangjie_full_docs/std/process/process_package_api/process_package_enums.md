# 枚举

## enum ProcessRedirect

```cangjie
public enum ProcessRedirect {
    | Inherit
    | Pipe
    | FromFile(File)
    | Discard
}
```

功能：该枚举类型用于在创建进程时设置子进程标准流的重定向模式。

### Discard

```cangjie
Discard
```

功能：构造一个标准流重定向枚举实例，表示子进程标准流将被丢弃。此模式下标准流属性不可读取或写入。

### FromFile(File)

```cangjie
FromFile(File)
```

功能：构造一个标准流重定向枚举实例，表示子进程标准流将被重定向至指定的文件。重定向标准输入流将从指定文件读取，重定向标准输出流或标准错误流将写入至指定文件。重定向文件需保证存在且未关闭，否则不允许重定向。此模式下标准流属性不可读取或写入。参数 [File](../../fs/fs_package_api/fs_package_classes.md#class-file) 为指定存在且未关闭文件实例，创建子进程时，重定向标准流至该指定文件。

### Inherit

```cangjie
Inherit
```

功能：构造一个标准流重定向枚举实例，表示子进程标准流将继承当前进程的标准流。此模式下标准流属性不可读取或写入。

### Pipe

```cangjie
Pipe
```

功能：构造一个标准流重定向枚举实例，表示子进程标准流将被重定向至管道，并通过管道与当前进程连接。重定向标准输入流可通过管道向子进程写入数据，重定向标准输出流或标准错误流可通过管道读取子进程输出结果。此模式下可通过标准流属性读取或写入数据。
