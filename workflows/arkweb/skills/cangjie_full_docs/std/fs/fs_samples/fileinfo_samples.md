# FileInfo 示例

## FileInfo 一些基础操作演示

代码如下：
<!-- verify -->

```cangjie
import std.fs.*
import std.time.DateTime

main() {
    // 在当前目录下创建一个临时文件，以便下面 FileInfo 的演示
    let curDirPath: Path = canonicalize(Path("./"))
    let file: File = File.createTemp(curDirPath)
    file.write("123456789\n".toArray())
    let fileInfo: FileInfo = file.info

    file.close()

    /* 获得这个文件父级目录的 FileInfo，这个文件的父目录是当前目录 */
    let parentDirectory: Option<FileInfo> = fileInfo.parentDirectory
    checkResult(parentDirectory == Some(FileInfo(curDirPath)), "The 'parentFileInfo' is obtained successfully.")

    /* 获得这个文件的路径 */
    /*
    let filePath: Path = fileInfo.path
     */

    /* 获取这个文件的创建时间、最后访问时间、最后修改时间 */
    /*
    let creationTime: DateTime = fileInfo.creationTime
    let lastAccessTime: DateTime = fileInfo.lastAccessTime
    let lastModificationTime: DateTime = fileInfo.lastModificationTime
     */

    /*
     * 获取这个文件的 length
     * 如果是文件代表这个文件占用磁盘空间的大小
     * 如果是目录代表这个目录的所有文件占用磁盘空间的大小(不包含子目录)
     */
    /*
    let length: Int64 = fileInfo.size
     */

    /* 判断这个文件是否是软链接、普通文件、目录 */
    checkResult(fileInfo.isSymbolicLink(), "The file is a symbolic link.")
    checkResult(fileInfo.isRegular(), "The file is a regular file.")
    checkResult(fileInfo.isDirectory(), "The file is a directory.")

    /* 判断这个文件对于当前用户是否是只读、隐藏、可执行、可读、可写 */
    checkResult(fileInfo.isReadOnly(), "This file is read-only.")
    checkResult(fileInfo.isHidden(), "The file is hidden.")
    checkResult(fileInfo.canExecute(), "The file is executable.")
    checkResult(fileInfo.canRead(), "The file is readable.")
    checkResult(fileInfo.canWrite(), "The file is writable.")

    /* 修改当前用户对这个文件的权限，这里设置为对当前用户只读 */
    checkResult(fileInfo.setExecutable(false), "The file was successfully set to executable.")
    checkResult(fileInfo.setReadable(true), "The file was successfully set to readable.")
    checkResult(fileInfo.setWritable(false), "The file was successfully set to writable.")
    checkResult(fileInfo.isReadOnly(), "This file is now read-only.")

    return 0
}

func checkResult(result: Bool, message: String): Unit {
    if (result) {
        println(message)
    }
}
```

运行结果：

```text
The 'parentFileInfo' is obtained successfully.
The file is a regular file.
The file is readable.
The file is writable.
The file was successfully set to executable.
The file was successfully set to readable.
The file was successfully set to writable.
This file is now read-only.
```
