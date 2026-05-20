---
name: cangjie-cffi
description: 仓颉程序与C程序互操作指导，包括foreign声明、CFunc、inout参数、unsafe块、调用约定、类型映射(基础类型/结构体/CPointer/VArray/CString)、C回调仓颉、内存管理等特性时，应使用此
  Skill
descriptionZH: 仓颉程序与C程序互操作指导，包括foreign声明、CFunc、inout参数、unsafe块、调用约定、类型映射(基础类型/结构体/CPointer/VArray/CString)、C回调仓颉、内存管理等特性时，应使用此
  Skill
tags:
  - 仓颉
  - CFFI
  - 互操作
---

# 仓颉 C 互操作 Skill

## 1. 从仓颉调用 C

### 1.1 foreign 函数声明

使用 `@C` 和 `foreign` 修饰符，结合仓颉函数语法声明 C 函数，`@C` 修饰符可省略。调用时须在 `unsafe {}` 块中。

```cangjie
@C
foreign func rand(): Int32
foreign func printf(fmt: CString, ...): Int32  // 变长参数用 ... 表示，须在参数列表末尾

main() {
    let r = unsafe { rand() }
    println("random number ${r}")
    unsafe {
        var fmt = LibC.mallocCString("Hello, No.%d\n")
        printf(fmt, 1)
        LibC.free(fmt)
    }
}
```

规则：

- `foreign` 函数只是声明，不涉及函数体
- 参数和返回类型须满足 `CType` 约束
- 不支持命名参数和参数默认值
- 变长参数（`...`）的各实参须满足 `CType` 约束，但不必是同一类型
- `@C` 只支持修饰 `foreign` 函数、顶层非泛型函数和 `struct`

可使用 `foreign` 块批量声明多个外部函数：

```cangjie
foreign {
    func rand(): Int32
    func printf(fmt: CString, ...): Int32
    func malloc(size: UIntNative): CPointer<Unit>
    func free(ptr: CPointer<Unit>): Unit
}
```

### 1.2 CFunc 类型

`CFunc` 类型用来映射 C 的函数指针，函数实体可能在 C 侧或仓颉侧定义，但两侧都能调用这类函数，有三种方式声明/定义：

```cangjie
// 形式 1：@C foreign 声明的外部 C 函数，定义在 C 侧
foreign func free(ptr: CPointer<Int8>): Unit

// 形式 2：@C 修饰的仓颉函数，定义在仓颉侧
@C
func callableInC(ptr: CPointer<Int8>) {
    println("defined in Cangjie")
}

// 形式 3：CFunc Lambda，定义在仓颉侧，不能捕获变量
let f1: CFunc<(CPointer<Int8>) -> Unit> = { ptr =>
    println("CFunc lambda")
}
```

以上三个示例函数的类型均为 `CFunc<(CPointer<Int8>) -> Unit>`。

`CFunc` 的参数和返回类型须满足 `CType` 约束，调用时须在 `unsafe` 上下文中。

CFunc 和 CPointer 互转：

```cangjie
// CPointer<T> → CFunc 其中 T <: CType
var ptr: CPointer<Int8> = getXXCFuncPtr()
var f = CFunc<() -> Unit>(ptr) // 须确保指针指向有效函数地址

// CFunc → CPointer<T>
foreign func rand(): Int32
var p = CPointer<Int8>(rand) // 安全，但不应对转换后的指针 read/write
```

### 1.3 inout 参数

调用 `CFunc` 时，用 `inout` 修饰实参变量，自动取变量地址转为 `CPointer<T>` 传递：

```cangjie
@C
struct Point {
    var x: Int32 = 0
    var y: Int32 = 0
}

foreign func f(ptr: CPointer<Int32>): Unit
foreign func g(ptr: CPointer<Point>): Unit

main() {
    var n: Int32 = 42 // 值类型，存储在栈上
    unsafe { f(inout n) }  // 取 n 的地址作为 CPointer<Int32> 传递

    var pt = Point() // 值类型，存储在栈上
    unsafe {
        g(inout pt) // 取结构体指针
        f(inout pt.x) // 取结构体可变成员变量的指针
    }
}
```

约束：

- 仅用于 `CFunc` 调用处
- 修饰对象须满足 `CType` 约束，且不能是 `CString`
- 修饰对象只能是 `var` 定义的可变变量（传递指针，可变语义），不能是不可变变量、字面量或临时值
- 不能直接或间接来源于 `class` 实例成员变量
- 指针仅在函数调用期间有效，C 侧不应保存该指针留作后用

### 1.4 unsafe 上下文

标记不安全的 C 互操作代码，可修饰函数、表达式或作用域块：

```cangjie
foreign func rand(): Int32

// 修饰函数
unsafe func doUnsafeWork() {
    return rand()
}

// 修饰作用域块
main() {
    unsafe {
        let r = doUnsafeWork() // unsafe 传染性
        println(r)
    }
    // 修饰单个表达式
    let r = unsafe { rand() }
    println(r)
}
```

调用以下函数须在 `unsafe` 上下文中：`foreign` 函数、`@C` 函数、`CFunc` 变量、`unsafe` 修饰的函数。

> **注意：** 普通 Lambda 不传播 `unsafe` 属性。在 Lambda 中调用 `unsafe` 函数时，须在 Lambda 内部使用 `unsafe {}` 块：
>
> ```cangjie
> unsafe func A() {}
> unsafe func B() {
>     var f = { =>
>         unsafe { A() }  // Lambda 内须使用 unsafe 块
>     }
>     return f
> }
> ```

### 1.5 调用约定

- `@CallingConv[CDECL]`：默认约定，可省略
- `@CallingConv[STDCALL]`：Win32 API 调用约定

适用于 `foreign` 块、单个 `foreign` 函数和顶层 `CFunc` 函数：

```cangjie
@CallingConv[STDCALL]
foreign func MessageBoxA(hwnd: CPointer<Unit>, text: CString, caption: CString, uType: UInt32): Int32
```

---

## 2. 类型映射

### 2.1 基本类型

| 仓颉类型 | C 类型 | 大小(字节) |
|----------|--------|-----------|
| `Unit` | `void` | 0 |
| `Bool` | `bool` | 1 |
| `Int8` / `UInt8` | `int8_t` / `uint8_t` | 1 |
| `Int16` / `UInt16` | `int16_t` / `uint16_t` | 2 |
| `Int32` / `UInt32` | `int32_t` / `uint32_t` | 4 |
| `Int64` / `UInt64` | `int64_t` / `uint64_t` | 8 |
| `IntNative` / `UIntNative` | `ssize_t` / `size_t` | 平台相关 |
| `Float32` | `float` | 4 |
| `Float64` | `double` | 8 |

> **注意：** C 的 `int`、`long` 等类型在不同平台大小不同，需自行指定对应仓颉类型。`Unit` 仅可作为 `CFunc` 返回类型和 `CPointer` 的泛型参数。

### 2.2 @C struct 结构体

用 `@C` 修饰的 `struct` 映射到 C 结构体，内存布局与 C 一致：

```c
// C 侧
typedef struct {
    int64_t x;
    int64_t y;
    int64_t z;
} Point3D;

Point3D addPoint(Point3D p1, Point3D p2);
```

```cangjie
// 仓颉侧
@C
struct Point3D {
    var x: Int64 = 0
    var y: Int64 = 0
    var z: Int64 = 0
}

foreign func addPoint(p1: Point3D, p2: Point3D): Point3D
```

限制：

- 成员类型须满足 `CType` 约束
- 不能实现或扩展接口
- 不能作为 `enum` 关联值类型
- 不允许被闭包捕获
- 不能有泛型参数
- `@C struct` 自动满足 `CType` 约束

### 2.3 CPointer\<T> 指针

`CPointer<T>` 映射到 C 的 `T*` 类型，`T` 须满足 `CType` 约束。

核心 API：

| 方法 | 说明 | 是否 unsafe |
|------|------|------------|
| `CPointer<T>()` | 创建空指针 | 否 |
| `isNull()` / `isNotNull()` | 判空 | 否 |
| `read()` | 读取指针指向的值 | 是 |
| `read(idx: Int64)` | 读取偏移 idx 处的值 | 是 |
| `write(value: T)` | 写入值到指针位置 | 是 |
| `write(idx: Int64, value: T)` | 写入值到偏移 idx 处 | 是 |
| `+ (offset: Int64)` | 指针偏移 | 是 |
| `- (offset: Int64)` | 指针偏移 | 是 |
| `toUIntNative()` | 转为整型地址值 | 否 |
| `asResource()` | 转为 `CPointerResource<T>` 自动管理 | 否 |

```cangjie
foreign func malloc(size: UIntNative): CPointer<Unit>
foreign func free(ptr: CPointer<Unit>): Unit

@C
struct Point {
    var x: Int64 = 0
    var y: Int64 = 0
    init(x: Int64, y: Int64) {
        this.x = x
        this.y = y
    }
}

main() {
    let p1 = CPointer<Point>()       // 空指针
    println(p1.isNull())              // true

    var p2 = unsafe { malloc(16) }    // 分配堆内存
    var p3 = unsafe { CPointer<Point>(p2) }  // 指针类型转换

    unsafe { p3.write(Point(1, 2)) }  // 写入数据
    let pt = unsafe { p3.read() }     // 读取数据
    println("${pt.x}, ${pt.y}")       // 1, 2

    let p4 = unsafe { p3 + 1 }        // 指针偏移

    unsafe { free(p2) }               // 释放内存
}
```

指针类型转换（泛型参数 `T` 均须满足 `CType`）：

```cangjie
var pInt8 = CPointer<Int8>()
var pUInt8 = CPointer<UInt8>(pInt8)  // CPointer<Int8> → CPointer<UInt8>
```

### 2.4 VArray\<T, $N> 数组

`VArray<T, $N>` 映射到 C 的 `T[N]`。`T` 满足 `CType` 时，`VArray<T, $N>` 也满足 `CType`。

**作为函数参数：** 函数签名中参数类型可以是 `CPointer<T>` 或 `VArray<T, $N>`，传递时均以 `CPointer<T>` 形式传递，须用 `inout` 修饰。不能作为返回类型。

```c
// C 侧
void processArray(int a[3]);
```

```cangjie
// 仓颉侧
foreign func processArray(a: VArray<Int32, $3>): Unit

main() {
    var arr: VArray<Int32, $3> = [1, 2, 3]
    unsafe { processArray(inout arr) }
}
```

**作为 @C struct 成员：** 内存布局与 C 一致。

```c
// C 侧
struct S { int a[2]; int b[0]; };
```

```cangjie
// 仓颉侧
@C
struct S {
    var a = VArray<Int32, $2>(repeat: 0)
    var b = VArray<Int32, $0>(repeat: 0)
}
```

> **注意：** 不支持 C 柔性数组（flexible array）的映射。

### 2.5 CString 字符串

`CString` 对应 C 的 `char*` 字符串，由 `LibC.mallocCString()` 创建，使用后须通过 `LibC.free()` 释放。

核心 API：

| 方法 | 说明 |
|------|------|
| `size(): Int64` | 字符串长度 |
| `isEmpty()` / `isNotEmpty()` | 长度判断（指针为 null 时 isEmpty 返回 true） |
| `isNull(): Bool` | 判断指针是否为 null |
| `getChars(): CPointer<UInt8>` | 获取底层字符数组指针 |
| `equals(rhs: CString): Bool` | 相等比较 |
| `equalsLower(rhs: CString): Bool` | 忽略大小写比较 |
| `compare(str: CString): Int32` | 字典序比较（同 C 的 `strcmp`） |
| `startsWith(str: CString): Bool` | 前缀判断 |
| `endsWith(str: CString): Bool` | 后缀判断 |
| `subCString(start: UInt64): CString` | 截取子串（新分配空间） |
| `subCString(start: UInt64, len: UInt64): CString` | 截取指定长度子串 |
| `toString(): String` | 转为仓颉 `String` |
| `asResource(): CStringResource` | 转为自动管理的 Resource |

```cangjie
foreign func strlen(s: CString): UIntNative

main() {
    var s = unsafe { LibC.mallocCString("hello") }

    println(s.size())              // 5
    println(s.isEmpty())           // false
    println(s.toString())          // hello

    let len = unsafe { strlen(s) } // 调用 C 的 strlen
    println(len)                   // 5

    unsafe { LibC.free(s) }        // 须手动释放
}
```

**CString 与 C 代码交互的完整示例：**

```c
// C 侧
char *str = "CString in C code.";
char *getCString() { return str; }
void printCString(char *s) { printf("%s\n", s); }
```

```cangjie
foreign func getCString(): CString
foreign func printCString(s: CString): Unit

main() {
    // 仓颉 → C：构造 CString 传给 C 函数
    unsafe {
        let s = LibC.mallocCString("CString in Cangjie code.")
        printCString(s)
        LibC.free(s)
    }

    // C → 仓颉：获取 C 字符串转为仓颉 String
    unsafe {
        let cs = getCString()
        println(cs.toString())  // "CString in C code."
    }

    // 使用 CStringResource 自动管理内存
    let cs = unsafe { LibC.mallocCString("auto managed") }
    try (csr = cs.asResource()) {
        unsafe { printCString(csr.value) }
    }  // 离开 try 块时自动释放
}
```

### 2.6 sizeOf / alignOf

获取 `CType` 类型的内存大小和对齐值（单位：字节）：

```cangjie
@C
struct Data {
    var a: Int64 = 0
    var b: Float32 = 0.0
}

main() {
    println(sizeOf<Data>())    // 16（64 位机器）
    println(alignOf<Data>())   // 8（64 位机器）
    println(sizeOf<Int32>())   // 4
}
```

### 2.7 CType 接口

`CType` 是空接口，作为所有 C 互操作类型的父类型，用于泛型约束。不能被继承或扩展。

```cangjie
func processAny<T>(x: T): Unit where T <: CType {
    match (x) {
        case i: Int32 => println("Int32: ${i}")
        case p: CPointer<Int8> => println("pointer isNull: ${p.isNull()}")
        case f: CFunc<() -> Unit> => unsafe { f() }
        case _ => println("other CType")
    }
}
```

---

## 3. 内存管理

### 3.1 LibC 工具类

`LibC` 提供 C 互操作的内存分配和释放（所有方法均须在 `unsafe` 上下文中调用）：

| 方法 | 说明 |
|------|------|
| `malloc<T>(count!: Int64 = 1): CPointer<T>` | 分配 `sizeOf<T>() * count` 字节的堆内存 |
| `free<T>(p: CPointer<T>): Unit` | 释放 `CPointer<T>` 指向的内存 |
| `mallocCString(str: String): CString` | 将仓颉 `String` 转为堆分配的 `CString` |
| `free(cstr: CString): Unit` | 释放 `CString` 内存 |

```cangjie
@C
struct Point {
    var x: Int64 = 0
    var y: Int64 = 0
}

main() {
    // 分配单个结构体
    let p = unsafe { LibC.malloc<Point>() }
    unsafe {
        p.write(Point())
        println(p.read().x)
        LibC.free(p)
    }

    // 分配数组（5 个 Int32）
    let arr = unsafe { LibC.malloc<Int32>(count: 5) }
    unsafe {
        for (i in 0..5) { arr.write(i, Int32(i * 10)) }
        for (i in 0..5) { print("${arr.read(i)} ") }  // 0 10 20 30 40
        println()
        LibC.free(arr)
    }
}
```

### 3.2 CPointerResource 与 CStringResource

使用 `try-with-resource` 语法自动管理内存，避免手动释放：

```cangjie
main() {
    // CPointerResource：自动释放 CPointer
    let p = unsafe { LibC.malloc<Int32>() }
    try (res = p.asResource()) {
        unsafe { res.value.write(42) }
        println(unsafe { res.value.read() })  // 42
    }  // 离开 try 块时自动调用 LibC.free

    // CStringResource：自动释放 CString
    let cs = unsafe { LibC.mallocCString("hello") }
    try (csr = cs.asResource()) {
        println(csr.value.toString())  // hello
    }  // 离开 try 块时自动调用 LibC.free
}
```

### 3.3 acquireArrayRawData / releaseArrayRawData

将仓颉 `Array<T>` 的底层数据暴露为 `CPointer<T>` 传递给 C 函数，无需拷贝：

```cangjie
// 函数签名
public unsafe func acquireArrayRawData<T>(arr: Array<T>): CPointerHandle<T> where T <: CType
public unsafe func releaseArrayRawData<T>(handle: CPointerHandle<T>): Unit where T <: CType
```

```cangjie
foreign func processBuffer(buf: CPointer<Int64>, len: Int32): Unit

main() {
    var arr: Array<Int64> = [1, 2, 3, 4, 5]
    unsafe {
        var handle = acquireArrayRawData(arr)
        processBuffer(handle.pointer, Int32(arr.size))  // 直接传底层指针
        releaseArrayRawData(handle)  // 必须配对释放
    }
}
```

> **注意：** `acquireArrayRawData` 和 `releaseArrayRawData` 必须配对使用。在两者之间不应构造仓颉对象或执行复杂逻辑，仅做简单的 C 函数调用。

---

## 4. C 调用仓颉

C 侧通过函数指针调用仓颉函数，仓颉侧用 `@C` 函数或 `CFunc` Lambda 构造：

```c
// C 侧
typedef void (*callback)(int);
void set_callback(callback cb);
```

```cangjie
// 仓颉侧声明
foreign func set_callback(cb: CFunc<(Int32) -> Unit>): Unit

// 方式 1：@C 函数
@C
func myCallback(s: Int32): Unit {
    println("callback: ${s}")
}

// 方式 2：CFunc Lambda
let cbLambda: CFunc<(Int32) -> Unit> = { i =>
    println("lambda callback: ${i}")
}

main() {
    unsafe { set_callback(myCallback) }
    unsafe { set_callback(cbLambda) }
}
```

注意事项：

- `foreign` 和 `@C` 函数的命名不建议使用 `CJ_`（不区分大小写）前缀，避免与编译器内部符号冲突
- 编译 C 代码时应启用 `-fstack-protector-all` 或 `-fstack-protector-strong` 栈保护选项

---

## 5. 编译构建

**编译构建指导**请查阅 `./build/SKILL.md`，包括仓颉 C 互操作项目的配置/构建/运行方法（涵盖动态库、静态库及不同平台的使用指导）

---

## 6. 完整示例

### 6.1 结构体，inout

```c
// native.c
#include <stdio.h>
#include <stdint.h>

typedef struct { int64_t x; int64_t y; } Point;

// windows 平台加上 __declspec(dllexport) 修饰
void drawPoint(Point* point) {
    point->x = 10;
    point->y = 20;
    printf("Draw Point: (%lld, %lld)\n", point->x, point->y);
}
```

```cangjie
// main.cj
@C
struct Point {
    var x: Int64 = 0
    var y: Int64 = 0
}

foreign func drawPoint(point: CPointer<Point>): Unit

main() {
    var pt = Point()  // 须用 var 定义，inout 要求可变变量
    unsafe {
        drawPoint(inout pt)
        println("x = ${pt.x}, y = ${pt.y}")  // x = 10, y = 20
    }
}
```

### 6.2 堆内存分配

```c
// native.c
#include <stdio.h>
#include <stdint.h>

typedef struct { float x; float y; float z; } Cube;

// windows 平台加上 __declspec(dllexport) 修饰
void initCube(Cube* cube) {
    printf("before: %f, %f, %f\n", cube->x, cube->y, cube->z);
    cube->x = 4.4;
    cube->y = 5.5;
    cube->z = 6.6;
}
```

```cangjie
// main.cj
@C
struct Cube {
    var x: Float32 = 0.0
    var y: Float32 = 0.0
    var z: Float32 = 0.0
    init(x: Float32, y: Float32, z: Float32) {
        this.x = x; this.y = y; this.z = z
    }
}

foreign func initCube(cube: CPointer<Cube>): Unit

main() {
    let pCube = unsafe { LibC.malloc<Cube>() }
    unsafe {
        pCube.write(Cube(1.1, 2.2, 3.3))
        initCube(pCube)
        let c = pCube.read()
        println("${c.x}, ${c.y}, ${c.z}")  // 4.4, 5.5, 6.6
        LibC.free(pCube)
    }
}
```

### 6.3 C 回调仓颉函数

```c
// native.c
#include <stdio.h>

typedef int (*transform_fn)(int);

// windows 平台加上 __declspec(dllexport) 修饰
void apply(int* arr, int len, transform_fn fn) {
    for (int i = 0; i < len; i++) {
        arr[i] = fn(arr[i]);
    }
}
```

```cangjie
// main.cj
foreign func apply(arr: CPointer<Int32>, len: Int32, fn: CFunc<(Int32) -> Int32>): Unit

@C
func doubleIt(x: Int32): Int32 { x * 2 }

main() {
    let buf = unsafe { LibC.malloc<Int32>(count: 3) }
    unsafe {
        buf.write(0, 1)
        buf.write(1, 2)
        buf.write(2, 3)
        apply(buf, 3, doubleIt)
        for (i in 0..3) {
            print("${buf.read(i)} ") // 2 4 6
        }
        println()
        LibC.free(buf)
    }
}
```

### 6.4 编译运行

> 完整的编译构建命令请参考 `cangjie-ffi-build` Skill。以下为上述示例的快速编译参考：

**Linux**
```shell
clang -shared -fPIC -fstack-protector-all native.c -o libnative.so
cjc -L . -l native main.cj -o main
./main
```

**Windows**
```shell
clang -shared -fstack-protector-all native.c -o libnative.dll
cjc -L . -l native main.cj -o main.exe
./main.exe
```

---

## 7. 使用约束

- **线程局部变量**：仓颉线程可能被调度到不同 OS 线程，使用 C 的 `thread_local` 或 `pthread_key_create` 变量有风险
- **线程绑定**：不建议使用线程优先级和线程亲和性等与线程绑定的行为
- **阻塞调用**：C 侧长时间阻塞会阻塞对应仓颉线程，不建议在 C 中出现长时间阻塞行为
- **进程 fork**：`fork()` 创建的子进程中不支持执行仓颉逻辑
- **进程退出**：C 中退出进程可能导致共享资源释放后的非法访问
- **栈大小**：C 函数实际使用的栈大小仓颉无法感知，存在栈溢出风险，需根据实际情况调整 `cjStackSize` 配置
