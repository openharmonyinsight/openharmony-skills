# 文件内容相关操作

下面是文件内容相关操作示例。

代码如下:

<!-- run -->

```cangjie
import std.posix.*

main(): Int64 {
    var fd = `open`("textcase.txt", O_RDWR | O_APPEND | O_CREAT, S_IRWXU)
    println("fd ==> ${fd}")
    close(fd)
    var fd2 = `open`("textcase.txt", O_RDWR)
    var len = lseek(fd2, 0, SEEK_END)
    println("len ==> ${len}")
    close(fd2)
    var str1 = unsafe { LibC.mallocCString(" ") }
    var buf = str1.getChars()
    var fd3 = `open`("textcase.txt", O_RDWR)
    var readNum = unsafe { read(fd3, buf, 2) }
    unsafe { LibC.free(str1) }
    println("readNum ==> ${readNum}")
    close(fd3)
    var str2 = unsafe { LibC.mallocCString("123456") }
    var buf2 = str2.getChars()

    var fd4 = `open`("textcase.txt", O_RDWR)
    var fd5 = dup(fd4)
    var writeNum = unsafe { write(fd5, buf2, UIntNative(str2.size())) }
    unsafe { LibC.free(str2) }
    println("writeNum ==> ${writeNum}")
    close(fd4)
    return 0
}
```

可能出现的运行结果：

```text
fd ==> 3
len ==> 6
readNum ==> 2
writeNum ==> 6
```
