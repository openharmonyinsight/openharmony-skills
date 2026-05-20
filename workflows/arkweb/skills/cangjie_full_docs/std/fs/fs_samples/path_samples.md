# Path 示例

## 不同 Path 实例的属性信息展示

打印 Path 实例的目录部分、文件全名（有扩展名）、扩展名、文件名（无扩展名），并判断 Path 实例是绝对路径还是相对路径

代码如下：
<!-- verify -->

```cangjie
import std.fs.Path

main() {
    let pathStrArr: Array<String> = [
        // 绝对路径
        "/a/b/c",
        "/a/b/",
        "/a/b/c.cj",
        "/a",
        "/",
        // 相对路径
        "./a/b/c",
        "./a/b/",
        "./a/b/c.cj",
        "./",
        ".",
        "123."
    ]

    for (i in 0..pathStrArr.size) {
        let path: Path = Path(pathStrArr[i])
        // 打印 path 的整个路径字符串
        println("Path${i}: ${path.toString()}")
        // 打印 path 的目录路径
        println("Path.parent: ${path.parent}")
        // 打印 path 的文件全名（有扩展名）
        println("Path.fileName: ${path.fileName}")
        // 打印 path 的扩展名
        println("Path.extensionName: ${path.extensionName}")
        // 打印 path 的文件名（无扩展名）
        println("Path.fileNameWithoutExtension: ${path.fileNameWithoutExtension}")
        // 打印 path 是否是绝对路径、相对路径
        println("Path.isAbsolute: ${path.isAbsolute()}; Path.isRelative: ${path.isRelative()}")
        println()
    }
    return 0
}
```

运行结果：

```text
Path0: /a/b/c
Path.parent: /a/b
Path.fileName: c
Path.extensionName: 
Path.fileNameWithoutExtension: c
Path.isAbsolute: true; Path.isRelative: false

Path1: /a/b/
Path.parent: /a
Path.fileName: b
Path.extensionName: 
Path.fileNameWithoutExtension: b
Path.isAbsolute: true; Path.isRelative: false

Path2: /a/b/c.cj
Path.parent: /a/b
Path.fileName: c.cj
Path.extensionName: cj
Path.fileNameWithoutExtension: c
Path.isAbsolute: true; Path.isRelative: false

Path3: /a
Path.parent: /
Path.fileName: a
Path.extensionName: 
Path.fileNameWithoutExtension: a
Path.isAbsolute: true; Path.isRelative: false

Path4: /
Path.parent: /
Path.fileName: 
Path.extensionName: 
Path.fileNameWithoutExtension: 
Path.isAbsolute: true; Path.isRelative: false

Path5: ./a/b/c
Path.parent: ./a/b
Path.fileName: c
Path.extensionName: 
Path.fileNameWithoutExtension: c
Path.isAbsolute: false; Path.isRelative: true

Path6: ./a/b/
Path.parent: ./a
Path.fileName: b
Path.extensionName: 
Path.fileNameWithoutExtension: b
Path.isAbsolute: false; Path.isRelative: true

Path7: ./a/b/c.cj
Path.parent: ./a/b
Path.fileName: c.cj
Path.extensionName: cj
Path.fileNameWithoutExtension: c
Path.isAbsolute: false; Path.isRelative: true

Path8: ./
Path.parent: 
Path.fileName: .
Path.extensionName: 
Path.fileNameWithoutExtension: 
Path.isAbsolute: false; Path.isRelative: true

Path9: .
Path.parent: 
Path.fileName: .
Path.extensionName: 
Path.fileNameWithoutExtension: 
Path.isAbsolute: false; Path.isRelative: true

Path10: 123.
Path.parent: 
Path.fileName: 123.
Path.extensionName: 
Path.fileNameWithoutExtension: 123
Path.isAbsolute: false; Path.isRelative: true
```

## Path 的拼接、判等、转规范化路径等操作

代码如下：
<!-- verify -->

```cangjie
import std.fs.*

main() {
    let dirPath: Path = Path("./a/b/c")
    if (!exists(dirPath)) {
        Directory.create(dirPath, recursive: true)
    }

    let filePath: Path = dirPath.join("d.cj") // ./a/b/c/d.cj
    if (filePath == Path("./a/b/c/d.cj")) {
        println("filePath.join: success")
    }
    if (!exists(filePath)) {
        File.create(filePath).close()
    }

    let curCanonicalizedPath: Path = canonicalize(Path("."))
    let fileCanonicalizedPath: Path = canonicalize(Path("././././a/./../a/b/../../a/b/c/.././../../a/b/c/d.cj"))
    if (fileCanonicalizedPath == canonicalize(filePath) && fileCanonicalizedPath.toString() ==
        curCanonicalizedPath.toString() + "/a/b/c/d.cj") {
        println("canonicalize filePath: success")
    }

    remove(dirPath, recursive: true)
    return 0
}
```

运行结果：

```text
filePath.join: success
canonicalize filePath: success
```

## 通过 Path 创建文件和目录

代码如下：
<!-- verify -->

```cangjie
import std.fs.*

main() {
    let curPath: Path = Path("./")
    let dirPath: Path = curPath.join("tempDir")
    let filePath: Path = dirPath.join("tempFile.txt")
    if (exists(dirPath)) {
        remove(dirPath, recursive: true)
    }

    Directory.create(dirPath)
    if (exists(dirPath)) {
        println("Directory 'tempDir' is created successfully.")
    }

    File.create(filePath).close()
    if (exists(filePath)) {
        println("File 'tempFile.txt' is created successfully in directory 'tempDir'.")
    }

    remove(dirPath, recursive: true)
    return 0
}
```

运行结果：

```text
Directory 'tempDir' is created successfully.
File 'tempFile.txt' is created successfully in directory 'tempDir'.
```
