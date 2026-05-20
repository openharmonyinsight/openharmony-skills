---
name: cangjie-std-libs
description: "仓颉标准库核心接口速查。当需要了解仓颉标准库各包的功能，包括各包提供的核心 API 功能时，应使用此 Skill"
---

# 仓颉标准库速查指南 Skill

> **说明**：本 Skill 仅用于**速查**目的，以表格形式列出各包的核心接口，方便快速定位 API。表格并未覆盖每个包的全部接口和细节信息，如果存在信息不足或接口遗漏，可以引用拆解标准库能力的特定 Skill，如果暂无相关细分 Skill，则请查阅标准库原始文档。

## 1. 概述

- 标准库（std）随 SDK 一起发布，开箱即用
- 核心包 `std.core` **自动导入**，无需显式 `import`
- 其他包使用 `import std.xxx.*` 导入

```cangjie
import std.collection.*                    // 导入整个包
import std.collection.{ArrayList, HashMap} // 按需导入 API
```

---

## 2. 标准库包功能总表

| 包名 | 功能简介 |
|------|----------|
| **core** | 核心包（自动导入）。基本类型（Int/Float/Bool/String/Array/Range/Option 等）、print/println/readln、核心接口（Iterable/Comparable/Hashable/ToString 等）、Duration、Thread/Future/spawn、异常基类等 |
| **collection** | 集合数据结构：ArrayList、HashMap、HashSet、TreeMap、TreeSet、LinkedList、ArrayDeque、ArrayQueue、ArrayStack，以及 List/Map/Set 等接口和函数式迭代操作 |
| **collection.concurrent** | 并发安全集合：ConcurrentHashMap、ConcurrentLinkedQueue、ArrayBlockingQueue、LinkedBlockingQueue |
| **io** | I/O 流抽象：InputStream/OutputStream 接口、缓冲流、StringReader/StringWriter、ByteBuffer 等 |
| **fs** | 文件系统：File 读写、Directory 操作、Path 处理、exists/copy/rename/remove 等 |
| **env** | 进程环境：标准流、环境变量读写、工作目录、进程 ID、exit 等 |
| **net** | 网络通信：TcpSocket/TcpServerSocket、UdpSocket、UnixSocket、IP 地址处理 |
| **sync** | 并发同步：Atomic 原子操作、Mutex 互斥锁、Monitor、Timer、SyncCounter |
| **time** | 时间日期：DateTime、Duration、MonoTime、TimeZone、格式化与解析 |
| **math** | 数学运算：三角函数、abs/sqrt/pow/log/ceil/floor、GCD/LCM 等 |
| **math.numeric** | 扩展数值：BigInt（任意精度整数）、Decimal（任意精度十进制数） |
| **random** | 伪随机数：Random 类 |
| **regex** | 正则表达式：Regex 类，查找/分割/替换/验证 |
| **sort** | 排序：对 Array/ArrayList 进行稳定/不稳定排序 |
| **convert** | 类型转换与格式化：Parsable（字符串→数值）、Formattable（格式化输出） |
| **process** | 进程管理：execute/launch 创建子进程、等待与信息查询 |
| **reflect** | 反射：TypeInfo 获取类型信息、动态访问成员 |
| **ast** | 语法树：源码解析器和 AST 节点，用于宏编程 |
| **argopt** | 命令行参数解析：parseArguments 函数，短/长/组合选项 |
| **binary** | 二进制端序转换：BigEndianOrder/LittleEndianOrder |
| **crypto.digest** | 摘要算法：MD5、SHA 系列、HMAC、SM3 |
| **crypto.cipher** | 对称加解密通用接口 |
| **database.sql** | 数据库接口：连接、查询、事务 |
| **deriving** | 自动派生宏：@Derive 生成 ToString/Hashable/Equatable/Comparable |
| **unicode** | Unicode 字符处理 |
| **overflow** | 整数溢出处理（Option/饱和/异常/截断） |
| **ref** | 弱引用：WeakRef 类 |
| **objectpool** | 对象池：ObjectPool 缓存与复用 |
| **posix** | POSIX 系统调用封装 |
| **runtime** | 运行时环境控制与监视 |
| **console** | ⚠️ 已弃用，请用 std.env |
| **unittest** | 单元测试框架（详见 unittest Skill） |
| **unittest.mock** | Mock 测试框架 |
| **unittest.testmacro** | 单元测试宏 |
| **unittest.mock.mockmacro** | Mock 框架宏 |
| **unittest.common** | 单元测试通用类型 |
| **unittest.diff** | 测试差异对比 |
| **unittest.prop_test** | 参数化测试 |

---

## 3. core — 核心包（自动导入）

### 3.1 核心接口

| 接口 | 关键方法 | 说明 |
|------|----------|------|
| `Any` | — | 所有类型的父接口 |
| `ToString` | `toString(): String` | 字符串表示 |
| `Hashable` | `hashCode(): Int64` | 哈希值 |
| `Hasher` | `write(Int64)`, `finish(): Int64` | 哈希计算器 |
| `Equatable<T>` | `==(T): Bool`, `!=(T): Bool` | 相等比较 |
| `Equal<T>` / `NotEqual<T>` | `==(T): Bool` / `!=(T): Bool` | 单向相等比较 |
| `Comparable<T>` | `compare(T): Ordering`, `<`, `>`, `<=`, `>=` | 大小比较（核心方法为 `compare`） |
| `Less<T>` / `Greater<T>` | `<(T): Bool` / `>(T): Bool` | 单向大小比较 |
| `LessOrEqual<T>` / `GreaterOrEqual<T>` | `<=(T): Bool` / `>=(T): Bool` | 单向大小比较 |
| `Iterable<E>` | `iterator(): Iterator<E>` | 支持 for-in 迭代 |
| `Collection<T>` | `size: Int64`, `isEmpty(): Bool`, `toArray(): Array<T>` | 集合基础 |
| `Resource` | `isClosed(): Bool`, `close(): Unit` | try-with-resources |
| `Countable<T>` | `next(Int64): T`, `position(): Int64` | 可计数类型（用于 Range） |
| `ThreadContext` | — | 线程上下文标记 |
| `CType` | — | 可与 C 交互的类型标记 |

### 3.2 核心类型

| 类型 | 说明 |
|------|------|
| `Int8`/`Int16`/`Int32`/`Int64` | 有符号整数（`Int` = `Int64`） |
| `UInt8`/`UInt16`/`UInt32`/`UInt64` | 无符号整数（`Byte` = `UInt8`，`UInt` = `UInt64`） |
| `IntNative`/`UIntNative` | 平台相关的整数 |
| `Float16`/`Float32`/`Float64` | 浮点数 |
| `Bool` | `true` / `false` |
| `Unit` | 表示无操作 |
| `Rune` | Unicode 字符 |
| `String` | UTF-8 字符串 |
| `Array<T>` | 固定长度的数组 |
| `Range<T>` | 区间，数值/字符范围 |
| `Option<T>` | 可空类型包装，`Some(T)` / `None`，等效写法 `?T` |
| `Ordering` | 比较大小，`LT` / `EQ` / `GT` |
| `Endian` | 字节序，`Big` / `Little` |
| `Duration` | 表示时间间隔 |
| `DefaultHasher` | 默认哈希计算器 |
| `StringBuilder` | 高效字符串拼接 |
| `Object` | 所有 class 类型的父类 |
| `Iterator<T>` | 迭代器接口 |
| `Box<T>` | 值类型装箱 |
| `Future<T>` | spawn 表达式的返回类型，表示一个异步执行任务 |
| `Thread` | 线程信息 |
| `ThreadLocal<T>` | 线程本地存储 |
| `StackTraceElement` | 异常栈帧信息 |
| `CString` | C 字符串包装，原始堆存储，用于 CFFI |
| `CPointer<T>` | C 指针包装，用于 CFFI |
| `CPointerHandle<T>` | C 指针管理器，用于 CFFI |

### 3.3 String 常用方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `size` | `size: Int64` | 字节长度 |
| `isEmpty` | `isEmpty(): Bool` | 是否为空字符串 |
| `contains` | `contains(String): Bool` | 是否包含子串 |
| `startsWith` | `startsWith(String): Bool` | 是否以指定前缀开头 |
| `endsWith` | `endsWith(String): Bool` | 是否以指定后缀结尾 |
| `indexOf` | `indexOf(String): Option<Int64>` | 查找子串首次出现位置 |
| `lastIndexOf` | `lastIndexOf(String): Option<Int64>` | 查找子串最后出现位置 |
| `count` | `count(String): Int64` | 统计子串出现次数 |
| `split` | `split(String, removeEmpty!: Bool = false): Array<String>` | 按分隔符拆分 |
| `lazySplit` | `lazySplit(String, removeEmpty!: Bool = false): Iterator<String>` | 惰性拆分 |
| `replace` | `replace(String, String): String` | 替换子串 |
| `trimAscii` | `trimAscii(): String` | 去除首尾 ASCII 空白 |
| `trimAsciiStart` | `trimAsciiStart(): String` | 去除开头 ASCII 空白 |
| `trimAsciiEnd` | `trimAsciiEnd(): String` | 去除结尾 ASCII 空白 |
| `removePrefix` | `removePrefix(String): String` | 去除前缀 |
| `removeSuffix` | `removeSuffix(String): String` | 去除后缀 |
| `toAsciiUpper` | `toAsciiUpper(): String` | ASCII 转大写 |
| `toAsciiLower` | `toAsciiLower(): String` | ASCII 转小写 |
| `equalsIgnoreAsciiCase` | `equalsIgnoreAsciiCase(String): Bool` | ASCII 大小写不敏感比较 |
| `padStart` | `padStart(Int64, padding!: String = " "): String` | 左填充至指定宽度 |
| `padEnd` | `padEnd(Int64, padding!: String = " "): String` | 右填充至指定宽度 |
| `lines` | `lines(): Iterator<String>` | 按行迭代 |
| `toArray` | `toArray(): Array<Byte>` | 转为字节数组 |
| `*` | `*(Int64): String` | 重复字符串 n 次 |
| `[]` | `[Range<Int64>]: String` | 按字节范围切片 |

### 3.4 Option 常用方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `isSome` | `isSome(): Bool` | 是否为 Some |
| `isNone` | `isNone(): Bool` | 是否为 None |
| `getOrDefault` | `getOrDefault(() -> T): T` | 获取值或执行默认闭包 |
| `getOrThrow` | `getOrThrow(): T` | 获取值或抛 NoneValueException |

### 3.5 常用全局函数

#### I/O 函数

| 函数 | 签名 | 说明 |
|------|------|------|
| `print` | `print(String)`, `print<T>(T) where T <: ToString` | 输出（不换行） |
| `println` | `println()`, `println(String)`, `println<T>(T) where T <: ToString` | 输出（换行） |
| `eprint` | `eprint(String)`, `eprint<T>(T) where T <: ToString` | 输出到 stderr |
| `eprintln` | `eprintln(String)`, `eprintln<T>(T) where T <: ToString` | 输出到 stderr（换行） |
| `readln` | `readln(): String` | 读取一行标准输入 |

#### 数学函数

| 函数 | 签名 | 说明 |
|------|------|------|
| `min` | `min<T>(T, T, Array<T>): T where T <: Comparable<T>` | 返回较小值（支持多参数） |
| `max` | `max<T>(T, T, Array<T>): T where T <: Comparable<T>` | 返回较大值（支持多参数） |

#### 并发函数

| 函数 | 签名 | 说明 |
|------|------|------|
| `sleep` | `sleep(Duration): Unit` | 当前线程休眠 |
| `spawn` | `spawn { => ... }` | 创建新线程，返回 `Future<T>` |
| `synchronized` | `synchronized(lock) { ... }` | 自动加锁/解锁的临界区 |

#### 工具函数

| 函数 | 签名 | 说明 |
|------|------|------|
| `refEq` | `refEq(Object, Object): Bool` | 引用相等比较 |
| `sizeOf` | `sizeOf<T>(): Int64` | 获取类型大小 |
| `alignOf` | `alignOf<T>(): Int64` | 获取类型对齐 |
| `zeroValue` | `zeroValue<T>(): T` | 获取类型零值 |

### 3.6 异常层次

#### Error（系统错误，不应捕获）

| 异常类型 | 说明 |
|----------|------|
| `OutOfMemoryError` | 内存不足 |
| `StackOverflowError` | 栈溢出 |

#### Exception（可捕获处理）

| 异常类型 | 说明 |
|----------|------|
| `ArithmeticException` | 算术运算错误（如除零） |
| `IllegalArgumentException` | 非法参数 |
| `IllegalFormatException` | 格式化字符串错误 |
| `IllegalMemoryException` | 非法内存访问 |
| `IllegalStateException` | 非法状态 |
| `IncompatiblePackageException` | 包不兼容 |
| `IndexOutOfBoundsException` | 索引越界 |
| `NegativeArraySizeException` | 数组大小为负 |
| `NoneValueException` | 访问 None 值 |
| `OverflowException` | 溢出 |
| `SpawnException` | 线程创建异常 |
| `UnsupportedException` | 不支持的操作 |
| `TimeoutException` | 超时 |

### 3.7 Duration 常用单位

| 单位 | 构造示例 |
|------|----------|
| `Duration.nanosecond` | `500 * Duration.nanosecond` |
| `Duration.microsecond` | `100 * Duration.microsecond` |
| `Duration.millisecond` | `200 * Duration.millisecond` |
| `Duration.second` | `Duration.second * 5` |
| `Duration.minute` | `Duration.minute * 10` |
| `Duration.hour` | `Duration.hour * 2` |

### 3.8 StringBuilder

| 方法 | 签名 | 说明 |
|------|------|------|
| `init` | `StringBuilder()` | 构造空 Builder |
| `append` | `append(String): Unit` | 追加字符串（也支持 Rune/Bool/整数/浮点/Array\<Rune>/CString/ToString） |
| `toString` | `toString(): String` | 转为 String |

---

## 4. collection — 集合

**导入**：`import std.collection.*`

### 4.1 集合类型

| 类型 | 构造函数 | 说明 |
|------|----------|------|
| `ArrayList<T>` | `ArrayList<T>()`, `ArrayList<T>(Int64)`, `ArrayList<T>(Collection<T>)`, `ArrayList<T>(Int64, (Int64) -> T)` | 动态数组 |
| `HashMap<K, V>` | `HashMap<K, V>()`, `HashMap<K, V>(Int64)`, `HashMap<K, V>(Array<(K, V)>)`, `HashMap<K, V>(Int64, (Int64) -> (K, V))` | 哈希映射（K <: Hashable & Equatable\<K>） |
| `HashSet<T>` | `HashSet<T>()`, `HashSet<T>(Int64)`, `HashSet<T>(Collection<T>)`, `HashSet<T>(Int64, (Int64) -> T)` | 哈希集合（T <: Hashable & Equatable\<T>） |
| `TreeMap<K, V>` | `TreeMap<K, V>()`, `TreeMap<K, V>(Array<(K, V)>)`, `TreeMap<K, V>(Int64, (Int64) -> (K, V))` | 红黑树有序映射（K <: Comparable\<K>） |
| `TreeSet<T>` | `TreeSet<T>()`, `TreeSet<T>(Collection<T>)`, `TreeSet<T>(Int64, (Int64) -> T)` | 红黑树有序集合（T <: Comparable\<T>） |
| `LinkedList<T>` | `LinkedList<T>()`, `LinkedList<T>(Collection<T>)`, `LinkedList<T>(Int64, (Int64) -> T)` | 双向链表 |
| `ArrayDeque<T>` | `ArrayDeque<T>()`, `ArrayDeque<T>(Int64)` | 双端队列 |
| `ArrayQueue<T>` | `ArrayQueue<T>()`, `ArrayQueue<T>(Int64)` | 环形队列 |
| `ArrayStack<T>` | `ArrayStack<T>()`, `ArrayStack<T>(Int64)` | 栈 |

### 4.2 集合接口

| 接口 | 关键方法 |
|------|----------|
| `Collection<T>` | `size`, `isEmpty()`, `toArray()` |
| `List<T>` | `get(Int64)`, `set(Int64, T)`, `add(T)`, `remove(at: Int64)` |
| `ReadOnlyList<T>` | `get(Int64)`, `size` |
| `Map<K, V>` | `get(K)`, `add(K, V)`, `contains(K)`, `remove(K)` |
| `ReadOnlyMap<K, V>` | `get(K)`, `contains(K)`, `size` |
| `Set<T>` | `add(T)`, `contains(T)`, `remove(T)` |
| `ReadOnlySet<T>` | `contains(T)`, `size` |
| `Queue<T>` | `enqueue(T)`, `dequeue()` |
| `Deque<T>` | `addFirst(T)`, `addLast(T)`, `removeFirst()`, `removeLast()` |
| `Stack<T>` | `push(T)`, `pop()`, `top()` |
| `OrderedMap<K, V>` | 有序映射接口 |
| `OrderedSet<T>` | 有序集合接口 |
| `EquatableCollection<T>` | 支持相等比较的集合 |

### 4.3 函数式迭代操作（应用于 Iterator\<T>）

#### 过滤与转换

| 函数 | 签名 | 说明 |
|------|------|------|
| `filter` | `filter(predicate: (T) -> Bool): Iterator<T>` | 过滤元素 |
| `map` | `map<R>(transform: (T) -> R): Iterator<R>` | 转换元素 |
| `flatMap` | `flatMap<R>(transform: (T) -> Iterator<R>): Iterator<R>` | 转换并展平 |
| `flatten` | `flatten(): Iterator<T>` | 展平嵌套迭代器 |
| `inspect` | `inspect(action: (T) -> Unit): Iterator<T>` | 不修改元素的调试操作 |

#### 聚合与查询

| 函数 | 签名 | 说明 |
|------|------|------|
| `fold` | `fold<R>(initial: R, operation: (R, T) -> R): R` | 累积计算（带初始值） |
| `reduce` | `reduce(operation: (T, T) -> T): Option<T>` | 累积计算（无初始值） |
| `forEach` | `forEach(action: (T) -> Unit): Unit` | 遍历执行 |
| `count` | `count(): Int64` | 计数 |
| `any` / `all` / `none` | `any(predicate: (T) -> Bool): Bool` | 谓词检查 |
| `first` / `last` | `first(): Option<T>` | 首/尾元素 |

#### 迭代控制

| 函数 | 签名 | 说明 |
|------|------|------|
| `take` / `skip` | `take(count: Int64): Iterator<T>` | 取前 n 个 / 跳过前 n 个 |
| `step` | `step(count: Int64): Iterator<T>` | 按步长取元素 |
| `enumerate` | `enumerate(): Iterator<(Int64, T)>` | 带索引遍历 |
| `zip` | `zip<R>(Iterator<R>): Iterator<(T, R)>` | 配对两个迭代器 |
| `concat` | `concat(Iterator<T>): Iterator<T>` | 连接两个迭代器 |

#### 收集函数

| 函数 | 签名 | 说明 |
|------|------|------|
| `collectArray` | `collectArray<T>(Iterable<T>): Array<T>` | 收集为 Array |
| `collectArrayList` | `collectArrayList<T>(Iterable<T>): ArrayList<T>` | 收集为 ArrayList |
| `collectHashMap` | `collectHashMap<K, V>(Iterable<(K, V)>): HashMap<K, V>` | 收集为 HashMap |
| `collectHashSet` | `collectHashSet<T>(Iterable<T>): HashSet<T>` | 收集为 HashSet |
| `collectString` | `collectString(Iterable<String>): String` | 收集为 String |

---

## 5. collection.concurrent — 并发安全集合

**导入**：`import std.collection.concurrent.*`

| 类型 | 构造函数 | 关键方法 |
|------|----------|----------|
| `ConcurrentHashMap<K, V>` | `ConcurrentHashMap<K, V>()` （K <: Hashable & Equatable\<K>） | `add(K, V)`, `get(K): ?V`, `contains(K)`, `remove(K)` |
| `ConcurrentLinkedQueue<T>` | `ConcurrentLinkedQueue<T>()` | `add(T)`, `remove(): ?T`, `peek(): ?T` |
| `ArrayBlockingQueue<T>` | `ArrayBlockingQueue<T>(Int64)` | `add(T)`, `remove(): T`（阻塞） |
| `LinkedBlockingQueue<T>` | `LinkedBlockingQueue<T>()` | `add(T)`, `remove(): T`（阻塞） |

---

## 6. io — I/O 流

**导入**：`import std.io.*`

### 6.1 接口

| 接口 | 关键方法 | 说明 |
|------|----------|------|
| `InputStream` | `read(Array<Byte>): Int64` | 输入流 |
| `OutputStream` | `write(Array<Byte>): Unit`, `flush(): Unit` | 输出流 |
| `IOStream` | 继承 InputStream + OutputStream | 双向流 |
| `Seekable` | `seek(SeekPosition): Int64` | 可定位流 |

### 6.2 类

| 类 | 构造函数 | 说明 |
|------|----------|------|
| `BufferedInputStream<T>` | `BufferedInputStream<T>(T)` | 缓冲输入流 |
| `BufferedOutputStream<T>` | `BufferedOutputStream<T>(T)` | 缓冲输出流 |
| `StringReader<T>` | `StringReader<T>(T)` | 字符串级别读取：`readln(): ?String`, `readToEnd(): String` |
| `StringWriter<T>` | `StringWriter<T>(T)` | 字符串级别写入：`write(String)`, `writeln(String)` |
| `ByteBuffer` | `ByteBuffer(Int64)` | 字节缓冲区 |
| `ChainedInputStream` | `ChainedInputStream(Array<InputStream>)` | 串联多个输入流 |
| `MultiOutputStream` | `MultiOutputStream(Array<OutputStream>)` | 同时写入多个输出流 |

---

## 7. fs — 文件系统

**导入**：`import std.fs.*`

### 7.1 全局函数

| 函数 | 签名 | 说明 |
|------|------|------|
| `exists` | `exists(String): Bool` | 检查路径是否存在 |
| `copy` | `copy(String, to!: String, overwrite!: Bool = false): Unit` | 复制文件 |
| `rename` | `rename(String, to!: String, overwrite!: Bool = false): Unit` | 重命名/移动 |
| `remove` | `remove(String, recursive!: Bool = false): Unit` | 删除文件或目录 |
| `canonicalize` | `canonicalize(String): Path` | 获取规范化绝对路径 |

### 7.2 File

| 方法 | 签名 | 说明 |
|------|------|------|
| 构造 | `File(String, OpenMode)`, `File(Path, OpenMode)` | 打开文件 |
| `readFrom` | `File.readFrom(String): Array<Byte>` | 快捷读文件 |
| `writeTo` | `File.writeTo(String, Array<Byte>): Unit` | 快捷写文件 |

**打开模式**：`OpenMode.Read` | `OpenMode.Write` | `OpenMode.Append` | `OpenMode.ReadWrite`

### 7.3 Directory

| 方法 | 签名 | 说明 |
|------|------|------|
| `create` | `Directory.create(String, recursive!: Bool = false)` | 创建目录 |
| `list` | `Directory.list(String): Array<FileInfo>` | 列出目录内容 |
| `delete` | `Directory.delete(String)` | 删除空目录 |

### 7.4 其他类型

| 类型 | 说明 |
|------|------|
| `Path` | 路径处理（拼接、分解、扩展名等） |
| `FileInfo` | 文件元信息（大小、时间、权限等） |
| `FileDescriptor` | 文件描述符 |

---

## 8. env — 进程环境

**导入**：`import std.env.*`

### 8.1 标准流

| 函数 | 签名 | 说明 |
|------|------|------|
| `getStdIn` | `getStdIn(): ConsoleReader` | 标准输入 |
| `getStdOut` | `getStdOut(): ConsoleWriter` | 标准输出 |
| `getStdErr` | `getStdErr(): ConsoleWriter` | 标准错误 |

### 8.2 环境变量

| 函数 | 签名 | 说明 |
|------|------|------|
| `getVariable` | `getVariable(String): ?String` | 读取环境变量 |
| `setVariable` | `setVariable(String, String): Unit` | 设置环境变量 |
| `removeVariable` | `removeVariable(String): Unit` | 删除环境变量 |
| `getVariables` | `getVariables(): Array<(String, String)>` | 获取所有环境变量 |

### 8.3 目录与路径

| 函数 | 签名 | 说明 |
|------|------|------|
| `getWorkingDirectory` | `getWorkingDirectory(): Path` | 当前工作目录 |
| `getHomeDirectory` | `getHomeDirectory(): Path` | 用户主目录 |
| `getTempDirectory` | `getTempDirectory(): Path` | 临时目录 |

### 8.4 进程信息与控制

| 函数 | 签名 | 说明 |
|------|------|------|
| `getCommand` | `getCommand(): String` | 当前可执行文件路径 |
| `getCommandLine` | `getCommandLine(): Array<String>` | 命令行参数 |
| `getProcessId` | `getProcessId(): Int64` | 进程 ID |
| `atExit` | `atExit(() -> Unit): Unit` | 注册进程退出回调 |
| `exit` | `exit(Int64): Nothing` | 退出进程 |

---

## 9. net — 网络通信

**导入**：`import std.net.*`

| 类型 | 构造函数 | 关键方法 |
|------|----------|----------|
| `TcpSocket` | `TcpSocket(String, UInt16)` | `connect()`, `read(Array<Byte>): Int64`, `write(Array<Byte>)`, `close()` |
| `TcpServerSocket` | `TcpServerSocket(bindAt: UInt16)` | `bind()`, `accept(): TcpSocket`, `close()` |
| `UdpSocket` | `UdpSocket(bindAt: UInt16)` | `sendTo(Array<Byte>, SocketAddress)`, `receiveFrom(Array<Byte>)`, `close()` |
| `UnixSocket` | `UnixSocket(String)` | Unix Domain Socket 通信 |

---

## 10. sync — 并发同步

**导入**：`import std.sync.*`

### 10.1 原子类型

| 类型 | 构造函数 | 关键方法 |
|------|----------|----------|
| `AtomicInt8` ~ `AtomicInt64` | `AtomicInt64(Int64)` | `load()`, `store(v)`, `swap(v)`, `compareAndSwap(old, new)`, `fetchAdd(v)`, `fetchSub(v)`, `fetchAnd(v)`, `fetchOr(v)`, `fetchXor(v)` |
| `AtomicUInt8` ~ `AtomicUInt64` | `AtomicUInt64(UInt64)` | 同上 |
| `AtomicBool` | `AtomicBool(Bool)` | `load()`, `store(v)`, `swap(v)`, `compareAndSwap(old, new)` |
| `AtomicReference<T>` | `AtomicReference<T>(T)` | `load()`, `store(v)`, `swap(v)`, `compareAndSwap(old, new)` |
| `AtomicOptionReference<T>` | `AtomicOptionReference<T>(?T)` | `load()`, `store(v)`, `swap(v)`, `compareAndSwap(old, new)` |

### 10.2 锁与同步

| 类型 | 构造函数 | 关键方法 | 备注 |
|------|----------|----------|------|
| `Mutex` | `Mutex()` | `lock()`, `unlock()`, `tryLock(): Bool` | 互斥锁 |
| `Barrier` | `Barrier(Int64)` | `wait()` | 屏障同步 |
| `Semaphore` | `Semaphore(Int64)` | `acquire()`, `release()`, `tryAcquire(): Bool` | 信号量 |
| `ReadWriteLock` | `ReadWriteLock()` | `readLock()`, `readUnlock()`, `writeLock()`, `writeUnlock()` | 读写锁 |
| `SyncCounter` | `SyncCounter(Int64)` | `dec()`, `waitUntilZero()` | 同步计数器 |
| `Timer` | `Timer()` | — | 定时器 |
| `Monitor` | `Monitor()` | `enter()`, `leave()`, `wait()`, `notify()`, `notifyAll()` | ⚠️ 已弃用 |
| `ReentrantMutex` | `ReentrantMutex()` | `lock()`, `unlock()`, `tryLock(): Bool`（可重入） | ⚠️ 已弃用 |

### 10.3 同步接口

| 接口 | 说明 |
|------|------|
| `Lock` | 锁接口（`lock()`, `unlock()`, `tryLock()`） |
| `Condition` | 条件变量接口 |

---

## 11. time — 时间日期

**导入**：`import std.time.*`

| 类型 | 分类 | 构造函数 / 工厂方法 | 关键方法 |
|------|------|----------------------|----------|
| `DateTime` | 结构体 | `DateTime.now()`, `DateTime.of(year, month, dayOfMonth, ...)` | `toString(String)`, `+/-` Duration 运算, `year`/`month`/`dayOfMonth` 等属性 |
| `MonoTime` | — | `MonoTime.now()` | 单调时间，适合计时（`MonoTime.now() - start` 返回 Duration） |
| `TimeZone` | — | `TimeZone.local`, `TimeZone.utc`, `TimeZone.of(String)` | 时区 |
| `DateTimeFormat` | — | `DateTimeFormat(String)` | 日期时间格式化/解析 |

---

## 12. math — 数学运算

**导入**：`import std.math.*`

| 函数 | 签名 | 说明 |
|------|------|------|
| `abs` | `abs<T>(T): T` | 绝对值 |
| `sqrt` | `sqrt(Float64): Float64` | 平方根 |
| `pow` | `pow(Float64, Float64): Float64` | 幂 |
| `log` / `log2` / `log10` | `log(Float64): Float64` | 对数 |
| `ceil` / `floor` / `round` | `ceil(Float64): Float64` | 取整 |
| `sin` / `cos` / `tan` | `sin(Float64): Float64` | 三角函数 |
| `asin` / `acos` / `atan` | `asin(Float64): Float64` | 反三角函数 |
| `gcd` | `gcd(Int64, Int64): Int64` | 最大公约数 |
| `lcm` | `lcm(Int64, Int64): Int64` | 最小公倍数 |
| `clamp` | `clamp(T, T, T): T` | 限制在范围内 |

### math.numeric — 扩展数值

**导入**：`import std.math.numeric.*`

| 类型 | 构造函数 | 说明 |
|------|----------|------|
| `BigInt` | `BigInt(String)`, `BigInt(Int64)` | 任意精度整数，支持 `+`/`-`/`*`/`/`/`%` |
| `Decimal` | `Decimal(String)`, `Decimal(Float64)` | 任意精度十进制数 |

---

## 13. random — 随机数

**导入**：`import std.random.*`

| 方法 | 签名 | 说明 |
|------|------|------|
| 构造 | `Random()`, `Random(seed: UInt64)` | 无种子 / 指定种子 |
| `nextInt8` ~ `nextInt64` | `nextInt64(): Int64` | 随机有符号整数 |
| `nextUInt8` ~ `nextUInt64` | `nextUInt64(): UInt64` | 随机无符号整数 |
| `nextFloat16` ~ `nextFloat64` | `nextFloat64(): Float64` | [0.0, 1.0) 随机浮点 |
| `nextGaussianFloat64` | `nextGaussianFloat64(Float64, Float64): Float64` | 高斯分布随机数（均值、标准差） |
| `nextBool` | `nextBool(): Bool` | 随机布尔 |

---

## 14. regex — 正则表达式

**导入**：`import std.regex.*`

| 方法 | 签名 | 说明 |
|------|------|------|
| 构造 | `Regex(String)` | 编译正则表达式 |
| `find` | `find(String): ?MatchData` | 查找第一个匹配 |
| `findAll` | `findAll(String): Iterator<MatchData>` | 查找所有匹配 |
| `fullMatch` | `fullMatch(String): Bool` | 完整匹配检查 |
| `replace` | `replace(String, String): String` | 替换匹配内容 |
| `split` | `split(String): Array<String>` | 按匹配分割 |

---

## 15. sort — 排序

**导入**：`import std.sort.*`

| 函数 | 签名 | 说明 |
|------|------|------|
| `sort` | `sort<T>(Array<T>) where T <: Comparable<T>` | 默认排序（默认不稳定） |
| `sort` | `sort<T>(Array<T>, (T, T) -> Ordering)` | 自定义比较器排序 |
| `sort` | `sort<T>(Array<T>, (T, T) -> Bool)` | 自定义 lessThan 排序 |
| `sort` | `sort<T, K>(Array<T>, key!: (T) -> K) where K <: Comparable<K>` | 按键排序 |
| `sort` | 同上各形式也支持 `ArrayList<T>` 和 `List<T>` | 稳定排序可传 `stable!: true` |

---

## 16. convert — 类型转换与格式化

**导入**：`import std.convert.*`

| 接口 / 方法 | 签名 | 说明 |
|-------------|------|------|
| `Parsable<T>` | `T.parse(String): T` | 字符串→数值（失败抛 IllegalArgumentException） |
| `Parsable<T>` | `T.tryParse(String): ?T` | 字符串→数值（失败返回 None） |
| `Formattable` | `format(String): String` | 数值格式化（十六进制 `"x"`、对齐 `">10"` 等） |

支持的类型：`Bool`、`Int8`~`Int64`、`UInt8`~`UInt64`、`Float16`~`Float64`、`Rune`

---

## 17. process — 进程管理

**导入**：`import std.process.*`

| 函数 / 类 | 签名 | 说明 |
|-----------|------|------|
| `execute` | `execute(String, Array<String>): Int64` | 执行命令并等待，返回退出码 |
| `executeWithOutput` | `executeWithOutput(String, Array<String>): (Int64, Array<Byte>, Array<Byte>)` | 执行命令并捕获 stdout/stderr（字节数组） |
| `launch` | `launch(String, Array<String>): SubProcess` | 异步启动子进程 |
| `findProcess` | `findProcess(Int64): Process` | 按 PID 查找进程 |
| `Process` | `pid`, `name`, `command`, `isAlive()` | 进程信息类 |
| `SubProcess` | `stdInPipe`, `stdOutPipe`, `stdErrPipe`, `wait()`, `waitOutput()` | 子进程类（继承 Process） |

---

## 18. argopt — 命令行参数解析

**导入**：`import std.argopt.*`

| 类型 / 函数 | 签名 | 说明 |
|-------------|------|------|
| `parseArguments` | `parseArguments(Array<String>, Array<ArgumentSpec>): ParsedArguments` | 解析命令行参数 |
| `ArgumentSpec.Short` | `Short(Rune, ArgumentMode)` | 短选项规范（如 `-v`） |
| `ArgumentSpec.Long` | `Long(String, ArgumentMode)` | 长选项规范（如 `--verbose`） |
| `ArgumentSpec.Full` | `Full(String, Rune, ArgumentMode)` | 同时定义长短选项 |
| `ArgumentMode` | `NoValue` / `RequiredValue` / `OptionalValue` | 选项参数模式 |
| `ParsedArguments` | `options: ReadOnlyMap<String, String>`, `nonOptions: Array<String>` | 解析结果 |

---

## 19. deriving — 自动派生

**导入**：`import std.deriving.*`

| 宏 | 用法 | 说明 |
|------|------|------|
| `@Derive` | `@Derive[ToString, Hashable, Equatable]` | 自动生成接口实现，适用于 struct/class/enum |
| `@DeriveExclude` | 标注成员 | 排除某些成员不参与派生 |
| `@DeriveInclude` | 标注成员 | 仅包含某些成员参与派生 |
| `@DeriveOrder` | 标注成员 | 指定成员参与派生的顺序 |

可派生的接口：`ToString`、`Hashable`、`Equatable`、`Comparable`

---

## 20. reflect — 反射

**导入**：`import std.reflect.*`

| 类型 | 关键方法 | 说明 |
|------|----------|------|
| `TypeInfo` | `name`, `qualifiedName` | 类型元信息基类 |
| `ClassTypeInfo` | `members`, `methods`, `properties` | 类的类型信息 |
| `StructTypeInfo` | `members`, `methods`, `properties` | 结构体的类型信息 |
| `InterfaceTypeInfo` | `methods` | 接口的类型信息 |
| `InstanceVariableInfo` | `name`, `type`, `getValue(Any)`, `setValue(Any, Any)` | 实例变量信息 |
| `InstanceFunctionInfo` | `name`, `parameters`, `apply(Any, ...)` | 实例方法信息 |
| `InstancePropertyInfo` | `name`, `type`, `getValue(Any)`, `setValue(Any, Any)` | 实例属性信息 |
| `ConstructorInfo` | `name`, `parameters`, `apply(...)` | 构造函数信息 |
| `PackageInfo` | `name`, `types` | 包信息 |

---

## 21. 其他包速查

### binary — 二进制端序

**导入**：`import std.binary.*`

| 接口 | 说明 |
|------|------|
| `BigEndianOrder` | 大端序 |
| `LittleEndianOrder` | 小端序 |

---

### crypto.digest — 摘要算法

**导入**：`import std.crypto.digest.*`

| 接口 / 类型 | 说明 |
|-------------|------|
| `Digest` | 摘要接口：`write(Array<Byte>)`, `finish(): Array<Byte>`, `reset()`, `size`, `blockSize` |
| `MD5` | MD5 摘要 |
| `SHA1` | SHA-1 摘要 |
| `SHA256` | SHA-256 摘要 |
| `SHA512` | SHA-512 摘要 |
| `SM3` | 国密 SM3 |
| `HMAC` | HMAC 消息认证码 |

---

### overflow — 溢出处理

**导入**：`import std.overflow.*`

| 策略 | 说明 |
|------|------|
| Option 返回 | 溢出返回 None |
| 饱和（saturating） | 溢出取边界值 |
| 抛异常（throwing） | 溢出抛 OverflowException |
| 截断（truncating） | 溢出截断 |

---

### ref — 弱引用

**导入**：`import std.ref.*`

| 类型 | 说明 |
|------|------|
| `WeakRef<T>` (where T <: Object) | 弱引用。属性：`value: Option<T>`（获取引用对象），`clear()` 清除引用 |

---

### objectpool — 对象池 ⚠️ 已弃用

**导入**：`import std.objectpool.*`

| 类型 | 说明 |
|------|------|
| `ObjectPool<T>` | 缓存与复用对象，减少分配开销 |

---

## 22. 最佳实践

| 场景 | 建议 |
|------|------|
| 资源管理 | 使用 `try (res = ...) { }` 自动关闭 File 等 Resource 对象 |
| 集合选择 | 随机访问用 ArrayList，键值查找用 HashMap，有序映射用 TreeMap，有序集合用 TreeSet，并发用 ConcurrentHashMap |
| 并发编程 | 优先 `synchronized(mtx) { }`；简单计数用 Atomic；用 Future.get() 等待结果 |
| 错误处理 | 用 `?T` 表示可缺失值，`??` 提供默认值，`?.` 安全链式调用 |
| I/O 性能 | 用 BufferedInputStream/BufferedOutputStream 包装原始流，写完调 flush() |
| 字符串 | 用 `"${expr}"` 插值；大量拼接用 StringBuilder；`for (c in s.runes())` 迭代字符 |
