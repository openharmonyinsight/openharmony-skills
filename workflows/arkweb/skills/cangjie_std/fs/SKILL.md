---
name: cangjie-std-fs
description: "仓颉文件系统用法。"
---

# 仓颉语言文件系统 Skill

## 1. File 类

- 来自 `std.fs.*`
- 实现 `Resource & IOStream & Seekable`
- 构造：`File(path, OpenMode)` 或 `File(Path, OpenMode)`

| 打开模式 | 行为 |
|---------|------|
| `Read` | 只读，文件不存在抛异常 |
| `Write` | 只写，存在则截断，不存在则创建 |
| `Append` | 追加写，不存在则创建 |
| `ReadWrite` | 读写，不存在则创建，不截断 |

- **静态方法**：

| 方法 | 说明 |
|------|------|
| `File.create(path)` | 创建文件，返回只写 File |
| `File.createTemp(dirPath)` | 创建临时文件 |
| `File.readFrom(path): Array<Byte>` | 一次性读取整个文件 |
| `File.writeTo(path, data)` | 一次性写入整个文件 |
| `File.appendTo(path, data)` | 追加写入 |

- 使用 `try-with-resource` 自动关闭

```cangjie
import std.fs.*
import std.io.*

main() {
    let path = Path("./demo.txt")

    // 写入文件
    try (f = File(path, Write)) {
        f.write("Hello 仓颉\n".toArray())
    }

    // 追加
    File.appendTo(path, "第二行\n".toArray())

    // 读取整个文件
    let data = File.readFrom(path)
    println(String.fromUtf8(data))

    // 随机读取
    try (f = File(path, Read)) {
        f.seek(SeekPosition.Begin(6))
        let buf = Array<Byte>(6, repeat: 0)
        f.read(buf)
        println(String.fromUtf8(buf))
    }

    remove(path)
}
```

---

## 2. 文件系统函数

| 函数 | 说明 |
|------|------|
| `exists(path): Bool` | 检查文件/目录是否存在 |
| `copy(src, to: dst, overwrite)` | 复制文件或目录 |
| `rename(src, to: dst, overwrite)` | 重命名/移动 |
| `remove(path, recursive)` | 删除文件或目录 |
| `removeIfExists(path, recursive)` | 安全删除（不存在不报错） |

---

## 3. Directory 操作

| 方法 | 说明 |
|------|------|
| `Directory.create(path, recursive)` | 创建目录，`recursive: true` 递归创建 |
| `Directory.createTemp(dirPath)` | 创建临时目录 |
| `Directory.isEmpty(path): Bool` | 检查目录是否为空 |
| `Directory.readFrom(path): Array<FileInfo>` | 列出目录内容 |
| `Directory.walk(path, callback)` | 遍历目录（回调返回 false 停止） |

```cangjie
import std.fs.*

main() {
    let dir = Path("./mydir/sub")
    Directory.create(dir, recursive: true)

    File.create(dir.join("test.txt")).close()

    let entries = Directory.readFrom(Path("./mydir"))
    for (e in entries) {
        println("${e.name} - ${e.size} bytes")
    }

    remove(Path("./mydir"), recursive: true)
}
```

---

## 4. Path 操作

- `Path` 是路径结构体，支持路径拼接和解析
- 关键属性：`parent`、`fileName`、`extensionName`、`fileNameWithoutExtension`、`isAbsolute()`
- `path.join(subPath)` — 拼接子路径
- `canonicalize(path)` — 解析为绝对规范路径（处理 `.`、`..`、符号链接）

```cangjie
import std.fs.*

main() {
    let p = Path("/home/user/docs/readme.md")
    println(p.parent)                     // "/home/user/docs"
    println(p.fileName)                   // "readme.md"
    println(p.extensionName)              // "md"
    println(p.fileNameWithoutExtension)   // "readme"
    println(p.isAbsolute())               // true
    println(p.join("../notes"))           // "/home/user/docs/readme.md/../notes"
    println(canonicalize(Path(".")))      // 当前目录的绝对路径
}
```

---

## 5. FileInfo

- 通过 `File.info` 或 `Directory.readFrom()` 获取
- 属性：`name`、`path`、`size`、`creationTime`、`lastAccessTime`、`lastModificationTime`、`parentDirectory`
- **注意**：每次访问属性都从文件系统实时获取，注意并发竞态

---

## 6. 异常类型

| 异常 | 说明 |
|------|------|
| `FSException` | 文件系统错误（继承自 `IOException`） |

---

## 7. 关键规则速查

1. 文件使用 `try-with-resource` 自动关闭
2. `File.readFrom` / `File.writeTo` / `File.appendTo` 是便捷的一次性读写方法
3. `FileInfo` 每次属性访问都是实时文件系统查询，注意并发竞态
4. `Directory.create` 需要 `recursive: true` 才能递归创建多级目录
5. `remove` 删除目录时需要 `recursive: true`
