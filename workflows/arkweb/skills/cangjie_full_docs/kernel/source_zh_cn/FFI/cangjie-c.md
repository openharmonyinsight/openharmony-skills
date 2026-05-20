# 仓颉-C 互操作

为了兼容已有的生态，仓颉支持调用 C 语言的函数，也支持 C 语言调用仓颉的函数。

## 仓颉调用 C 的函数

在仓颉中要调用 C 的函数，需要在仓颉语言中用 `@C` 和 `foreign` 关键字声明这个函数，但 `@C` 在修饰 `foreign` 声明的时候，可以省略。

举个例子，假设要调用 C 的 `rand` 和 `printf` 函数，它的函数签名如下：

```c
// stdlib.h
int rand();

// stdio.h
int printf (const char *fmt, ...);
```

那么在仓颉中调用这两个函数的方式如下：

```cangjie
// declare the function by `foreign` keyword, and omit `@C`
foreign func rand(): Int32
foreign func printf(fmt: CString, ...): Int32

main() {
    // call this function by `unsafe` block
    let r = unsafe { rand() }
    println("random number ${r}")
    unsafe {
        var fmt = LibC.mallocCString("Hello, No.%d\n")
        printf(fmt, 1)
        LibC.free(fmt)
    }
}
```

需要注意的是：

1. `foreign` 修饰函数声明，代表该函数为外部函数。被 `foreign` 修饰的函数只能有函数声明，不能有函数实现。
2. `foreign` 声明的函数，参数和返回类型必须符合 C 和仓颉数据类型之间的映射关系，详情请参见[类型映射](./cangjie-c.md#类型映射)。
3. 由于 C 侧函数很可能产生不安全操作，所以调用 `foreign` 修饰的函数需要被 `unsafe` 块包裹，否则会发生编译错误。
4. `@C` 修饰的 `foreign` 关键字只能用来修饰函数声明，不可用来修饰其他声明，否则会发生编译错误。
5. `@C` 只支持修饰 `foreign` 函数、顶层作用域中的非泛型函数和 `struct` 类型。
6. `foreign` 函数不支持命名参数和参数默认值。`foreign` 函数允许变长参数，使用 `...` 表达，只能用于参数列表的最后。变长参数均需要满足 `CType` 约束，但不必是同一类型。
7. 仓颉（CJNative 后端）虽然提供了栈扩容能力，但是由于 C 侧函数实际使用栈大小仓颉无法感知，所以 ffi 调用进入 C 函数后，仍然存在栈溢出的风险（可能导致程序运行时崩溃或者产生不可预期的行为），需要开发者根据实际情况，修改 `cjStackSize` 的配置。

一些不合法的 `foreign` 声明的示例代码如下：

```cangjie
foreign func rand(): Int32 { // compiler error
    return 0
}
@C
foreign var a: Int32 = 0 // compiler error
@C
foreign class A{} // compiler error
@C
foreign interface B{} // compiler error
```

## CFunc

仓颉中的 `CFunc` 指可以被 C 语言代码调用的函数，共有以下三种形式：

1. `@C` 修饰的 `foreign` 函数
2. `@C` 修饰的仓颉函数
3. 类型为 `CFunc` 的 `lambda` 表达式，与普通的 lambda 表达式不同，`CFunc lambda` 不能捕获变量。

<!-- run -->

```cangjie
// Case 1
foreign func free(ptr: CPointer<Int8>): Unit

// Case 2
@C
func callableInC(ptr: CPointer<Int8>) {
    print("This function is defined in Cangjie.")
}

// Case 3
let f1: CFunc<(CPointer<Int8>) -> Unit> = { ptr =>
    print("This function is defined with CFunc lambda.")
}
```

以上三种形式声明/定义的函数的类型均为 `CFunc<(CPointer<Int8>) -> Unit>`。`CFunc` 对应 C 语言的函数指针类型。这个类型为泛型类型，其泛型参数表示该 `CFunc` 入参和返回值类型，使用方式如下：

<!-- run -->

```cangjie
foreign func atexit(cb: CFunc<() -> Unit>): Int32
```

与 `foreign` 函数一样，其他形式的 `CFunc` 的参数和返回类型必须满足 `CType` 约束，且不支持命名参数和参数默认值。

`CFunc` 在仓颉代码中被调用时，需要处在 `unsafe` 上下文中。

仓颉语言支持将一个 `CPointer<T>` 类型的变量类型转换为一个具体的 `CFunc`，其中 `CPointer` 的泛型参数 `T` 可以是满足 `CType` 约束的任意类型，使用方式如下：

<!-- compile -->

```cangjie
main() {
    var ptr = CPointer<Int8>()
    var f = CFunc<() -> Unit>(ptr)
    unsafe { f() } // core dumped when running, because the pointer is nullptr.
}
```

> **注意：**
>
> 将一个指针强制类型转换为 `CFunc` 并进行函数调用是危险行为，需要用户保证指针指向的是一个切实可用的函数地址，否则将发生运行时错误。

## inout 参数

在仓颉中调用 `CFunc` 时，其实参可以使用 `inout` 关键字修饰，组成引用传值表达式，此时，该参数按引用传递。引用传值表达式的类型为 `CPointer<T>`，其中 `T` 为 `inout` 修饰的表达式的类型。

引用传值表达式具有以下约束：

- 仅可用于对 `CFunc` 的调用处。
- 其修饰对象的类型必须满足 `CType` 约束，但不可以是 `CString`。
- 其修饰对象不可以是用 `let` 定义的，不可以是字面量、入参、其他表达式的值等临时变量。
- 通过仓颉侧引用传值表达式传递到 C 侧的指针，仅保证在函数调用期间有效，即此种场景下 C 侧不应该保存指针以留作后用。

`inout` 修饰的变量，可以是定义在顶层作用域中的变量、局部变量、`struct` 中的成员变量，但不能直接或间接来源于 `class` 的实例成员变量。

下面是一个例子：

```cangjie
foreign func foo1(ptr: CPointer<Int32>): Unit

@C
func foo2(ptr: CPointer<Int32>): Unit {
    let n = unsafe { ptr.read() }
    println("*ptr = ${n}")
}

let foo3: CFunc<(CPointer<Int32>) -> Unit> = { ptr =>
    let n = unsafe { ptr.read() }
    println("*ptr = ${n}")
}

struct Data {
    var n: Int32 = 0
}

class A {
    var data = Data()
}

main() {
    var n: Int32 = 0
    unsafe {
        foo1(inout n)  // OK
        foo2(inout n)  // OK
        foo3(inout n)  // OK
    }
    var data = Data()
    var a = A()
    unsafe {
        foo1(inout data.n)   // OK
        foo1(inout a.data.n) // Error, n is derived indirectly from instance member variables of class A
    }
}
```

> **注意：**
>
> 使用宏扩展特性时，在宏的定义中，暂时不能使用 `inout` 参数特性。

## unsafe

在引入与 C 语言的互操作过程中，同时也引入了 C 的许多不安全因素，因此在仓颉中使用 `unsafe` 关键字，用于对跨 C 调用的不安全行为进行标识。

关于 unsafe 关键字，有以下几点说明：

- `unsafe` 可以修饰函数、表达式，也可以修饰一段作用域。
- 被 `@C` 修饰的函数，被调用处需要在 `unsafe` 上下文中。
- 在调用 `CFunc` 时，使用处需要在 `unsafe` 上下文中。
- `foreign` 函数在仓颉中进行调用，被调用处需要在 `unsafe` 上下文中。
- 当被调用函数被 `unsafe` 修饰时，被调用处需要在 `unsafe` 上下文中。

使用方式如下：

<!-- run -->

```cangjie
foreign func rand(): Int32

@C
func foo(): Unit {
    println("foo")
}

var foo1: CFunc<() -> Unit> = { =>
    println("foo1")
}

main(): Int64 {
    unsafe {
        rand()           // Call foreign func.
        foo()            // Call @C func.
        foo1()           // Call CFunc var.
    }
    0
}
```

需要注意的是，普通 `lambda` 无法传递 `unsafe` 属性，当 `unsafe` 的 `lambda` 逃逸后，可以不在 `unsafe` 上下文中直接调用而未产生任何编译错误。当需要在 `lambda` 中调用 `unsafe` 函数时，建议在 `unsafe` 块中进行调用，参考如下用例：

<!-- run -->

```cangjie
unsafe func A(){}
unsafe func B(){
    var f = { =>
        unsafe { A() } // Avoid calling A() directly without unsafe in a normal lambda.
    }
    return f
}
main() {
    var f = unsafe{ B() }
    f()
    println("Hello World")
}
```

## 调用约定

函数调用约定描述调用者和被调用者双方如何进行函数调用（如参数如何传递、栈由谁清理等），函数调用和被调用双方必须使用相同的调用约定才能正常运行。仓颉编程语言通过 `@CallingConv` 来表示各种调用约定，支持的调用约定如下：

- **CDECL**：`CDECL` 表示 clang 的 C 编译器在不同平台上默认使用的调用约定。
- **STDCALL**：`STDCALL` 表示 Win32 API 使用的调用约定。

通过 C 语言互操作机制调用的 C 函数，未指定调用约定时将采用默认的 `CDECL` 调用约定。如下调用 C 标准库函数 `rand` 示例：

<!-- run -->

```cangjie
@CallingConv[CDECL]   // Can be omitted in default.
foreign func rand(): Int32

main() {
    println(unsafe { rand() })
}
```

`@CallingConv` 只能用于修饰 `foreign` 块、单个 `foreign` 函数和顶层作用域中的 `CFunc` 函数。当 `@CallingConv` 修饰 `foreign` 块时，会为 `foreign` 块中的每个函数分别加上相同的 `@CallingConv` 修饰。

## 使用说明

- 操作系统线程局部变量使用约束

  仓颉和 C 语言互操作时，使用操作系统线程的局部变量存在风险，说明如下：

  1. 线程局部变量包括 C 语言提供的 `thread_local` 定义的变量和使用 `pthread_key_create` 创建的变量。
  2. 仓颉具备仓颉线程调度能力，支持仓颉线程的切换和恢复，仓颉线程被调度到哪个操作系统线程是随机的，从而在仓颉线程上调用其他语言的线程局部变量是有风险的。

  如下示例中，仓颉调用 C 语言的线程局部变量存在风险：

  ```c
  // C language logic using thread_local
  static thread_local int64_t count = 0;
  int64_t getCount() {
      count++;
      return count;
  }
  ```

  ```cangjie
  foreign func getCount(): Int64
  // Cangjie invokes the preceding C language logic
  spawn {
      let r1 = unsafe { getCount() }  // r1 equals 1
      sleep(Duration.second * 10)
      let r2 = unsafe { getCount() }  // r2 may not be equal to 2
  }
  ```

- 线程绑定使用约束

  仓颉调用 C 语言执行互操作逻辑时，仓颉线程调度到哪个操作系统线程是随机的，线程优先级和线程亲和性等与线程绑定的行为不建议使用。

- 同步原语使用说明

  仓颉调用 C 语言执行互操作逻辑时，当前这个仓颉线程会等待互操作逻辑执行结束，不建议在其他语言中出现可能导致长时间等待的阻塞性行为。

- 对进程 fork 场景的支持说明

  仓颉调用 C 语言执行互操作逻辑时，如果在 C 语言中以 `fork()` 方式创建子进程，子进程中不支持执行仓颉逻辑。同一进程中其他操作系统线程不受影响。

- 进程退出时的说明

  仓颉调用 C 语言执行互操作逻辑时，如果在 C 语言中退出进程，进程内共享的资源已经释放，可能导致非法访问等错误。

## 类型映射

### 基础类型

仓颉与 C 语言支持基本数据类型的映射，总体原则是：

1. 仓颉的类型不包含指向托管内存的引用类型；
2. 仓颉的类型和 C 的类型具有同样的内存布局。

比如说，一些基本的类型映射关系如下：

| Cangjie Type |   C Type   |    Size (byte)     |
|:------------:|:----------:|:------------------:|
|    `Unit`    |   `void`   |         0          |
|    `Bool`    |   `bool`   |         1          |
|   `UInt8`    |   `char`   |         1          |
|    `Int8`    |  `int8_t`  |         1          |
|   `UInt8`    | `uint8_t`  |         1          |
|   `Int16`    | `int16_t`  |         2          |
|   `UInt16`   | `uint16_t` |         2          |
|   `Int32`    | `int32_t`  |         4          |
|   `UInt32`   | `uint32_t` |         4          |
|   `Int64`    | `int64_t`  |         8          |
|   `UInt64`   | `uint64_t` |         8          |
| `IntNative`  | `ssize_t`  | platform dependent |
| `UIntNative` |  `size_t`  | platform dependent |
|  `Float32`   |  `float`   |         4          |
|  `Float64`   |  `double`  |         8          |

> **说明：**
>
> `int` 类型、`long` 类型等由于其在不同平台上的不确定性，需要程序员自行指定对应仓颉编程语言类型。在 C 互操作场景中，与 C 语言类似，`Unit` 类型仅可作为 `CFunc` 中的返回类型和 `CPointer` 的泛型参数。

仓颉也支持与 C 语言的结构体和指针类型的映射。

### 结构体

对于结构体类型，仓颉用 `@C` 修饰的 `struct` 来对应。比如说 C 语言里面有这样的一个结构体：

```c
typedef struct {
    long long x;
    long long y;
    long long z;
} Point3D;
```

那么它对应的仓颉类型可以这样定义：

<!-- run -example00-->

```cangjie
@C
struct Point3D {
    var x: Int64 = 0
    var y: Int64 = 0
    var z: Int64 = 0
}
```

如果 C 语言里有这样的一个函数：

```c
Point3D addPoint(Point3D p1, Point3D p2);
```

那么对应的，在仓颉里面可以这样声明这个函数：

<!-- run -example00-->

```cangjie
foreign func addPoint(p1: Point3D, p2: Point3D): Point3D
```

用 `@C` 修饰的 `struct` 必须满足以下限制：

- 成员变量的类型必须满足 `CType` 约束
- 不能实现或者扩展 `interfaces`
- 不能作为 `enum` 的关联值类型
- 不允许被闭包捕获
- 不能具有泛型参数

用 `@C` 修饰的 `struct` 自动满足 `CType` 约束。

### 指针

对于指针类型，仓颉提供 `CPointer<T>` 类型来对应 C 侧的指针类型，其泛型参数 `T` 需要满足 `CType` 约束。比如对于 malloc 函数，在 C 里面的签名为：

```c
void* malloc(size_t size);
```

那么在仓颉中，它可以声明为：

<!-- run -->

```cangjie
foreign func malloc(size: UIntNative): CPointer<Unit>
```

`CPointer` 可以进行读写、偏移计算、判空以及转为指针的整型形式等，详细 API 可以参考《仓颉编程语言库 API》。其中读写和偏移计算为不安全行为，当不合法的指针调用这些函数时，可能发生未定义行为，这些 unsafe 函数需要在 unsafe 块中调用。

`CPointer` 的使用示例如下：

<!-- run -->

```cangjie
foreign func malloc(size: UIntNative): CPointer<Unit>
foreign func free(ptr: CPointer<Unit>): Unit

@C
struct Point3D {
    var x: Int64
    var y: Int64
    var z: Int64

    init(x: Int64, y: Int64, z: Int64) {
        this.x = x
        this.y = y
        this.z = z
    }
}

main() {
    let p1 = CPointer<Point3D>() // create a CPointer with null value
    if (p1.isNull()) {  // check if the pointer is null
        print("p1 is a null pointer")
    }

    let sizeofPoint3D: UIntNative = 24
    var p2 = unsafe { malloc(sizeofPoint3D) }    // malloc a Point3D in heap
    var p3 = unsafe { CPointer<Point3D>(p2) }    // pointer type cast

    unsafe { p3.write(Point3D(1, 2, 3)) } // write data through pointer

    let p4: Point3D = unsafe { p3.read() } // read data through pointer

    let p5: CPointer<Point3D> = unsafe { p3 + 1 } // offset of pointer

    unsafe { free(p2) }
}
```

仓颉语言支持 `CPointer` 之间的强制类型转换，转换前后的 `CPointer` 的泛型参数 `T` 均需要满足 `CType` 的约束，使用方式如下：

<!-- run -->

```cangjie
main() {
    var pInt8 = CPointer<Int8>()
    var pUInt8 = CPointer<UInt8>(pInt8) // CPointer<Int8> convert to CPointer<UInt8>
}
```

仓颉语言支持将一个 `CFunc` 类型的变量类型转换为一个具体的 `CPointer`，其中 `CPointer` 的泛型参数 `T` 可以是满足 `CType` 约束的任意类型，使用方式如下：

<!-- run -->

```cangjie
foreign func rand(): Int32
main() {
    var ptr = CPointer<Int8>(rand)
}
```

> **注意：**
>
> 将一个 `CFunc` 强制类型转换为指针通常是安全的，但是不应该对转换后的指针执行任何的 `read`，`write` 操作，可能会导致运行时错误。

### 数组

仓颉使用 `VArray` 类型与 C 的数组类型映射，`VArray` 可以作为函数参数和 `@C struct` 成员。当 `VArray<T, $N>` 中的元素类型 `T` 满足 `CType` 约束时， `VArray<T, $N>` 类型也满足 `CType` 约束。

**作为函数参数类型：**

当 `VArray` 作为 `CFunc` 的参数时， `CFunc` 的函数签名仅可以是 `CPointer<T>` 类型或 `VArray<T, $N>` 类型。当函数签名中的参数类型为 `VArray<T, $N>` 时，传递的参数仍以 `CPointer<T>` 形式传递。

`VArray` 作为参数的使用示例如下：

```cangjie
foreign func cfoo1(a: CPointer<Int32>): Unit
foreign func cfoo2(a: VArray<Int32, $3>): Unit
```

对应的 C 侧函数定义可以是：

```c
void cfoo1(int *a) { ... }
void cfoo2(int a[3]) { ... }
```

调用 `CFunc` 时，需要通过 `inout` 修饰 `VArray` 类型变量：

```cangjie
var a: VArray<Int32, $3> = [1, 2, 3]
unsafe {
    cfoo1(inout a)
    cfoo2(inout a)
}
```

`VArray` 不允许作为 `CFunc` 的返回值类型。

**作为 @C struct 成员：**

当 `VArray` 作为 `@C struct` 成员时，它的内存布局与 C 侧的结构体排布一致，需要保证仓颉侧声明长度与类型也与 C 完全一致：

```c
struct S {
    int a[2];
    int b[0];
}
```

在仓颉中，可以声明为如下结构体与 C 代码对应：

<!-- run -->

```cangjie
@C
struct S {
    var a = VArray<Int32, $2>(repeat: 0)
    var b = VArray<Int32, $0>(repeat: 0)
}
```

> **注意：**
>
> C 语言中允许结构体的最后一个字段为未指明长度的数组类型，该数组被称为柔性数组（flexible array），仓颉不支持包含柔性数组的结构体的映射。

### 字符串

特别地，对于 C 语言中的字符串类型，仓颉中设计了一个 `CString` 类型来对应。为简化为 C 语言字符串的操作，`CString` 提供了以下成员函数：

- `init(p: CPointer<UInt8>)`  通过 CPointer 构造一个 CString
- `func getChars()` 获取字符串的地址，类型为 `CPointer<UInt8>`
- `func size(): Int64`  计算该字符串的长度
- `func isEmpty(): Bool`  判断该字符串的长度是否为 0，如果字符串的指针为空返回 true
- `func isNotEmpty(): Bool`  判断该字符串的长度是否不为 0，如果字符串的指针为空返回 false
- `func isNull(): Bool`  判断该字符串的指针是否为 null
- `func startsWith(str: CString): Bool`  判断该字符串是否以 str 开头
- `func endsWith(str: CString): Bool`  判断该字符串是否以 str 结尾
- `func equals(rhs: CString): Bool`  判断该字符串是否与 rhs 相等
- `func equalsLower(rhs: CString): Bool`  判断该字符串是否与 rhs 相等，忽略大小写
- `func subCString(start: UInt64): CString`  从 start 开始截取子串，返回的子串存储在新分配的空间中
- `func subCString(start: UInt64, len: UInt64): CString`  从 start 开始截取长度为 len 的子串，返回的子串存储在新分配的空间中
- `func compare(str: CString): Int32`  该字符串与 str 比较，返回结果与 C 语言的 `strcmp(this, str)` 一样
- `func toString(): String`  用该字符串构造一个新的 String 对象
- `func asResource(): CStringResource` 获取 CString 的 Resource 类型

另外，将 `String` 类型转换为 `CString` 类型，可以通过调用 LibC 中的 `mallocCString` 接口，使用完成后需要对 `CString` 进行释放。

`CString` 的使用示例如下：

<!-- run -->

```cangjie
foreign func strlen(s: CString): UIntNative

main() {
    var s1 = unsafe { LibC.mallocCString("hello") }
    var s2 = unsafe { LibC.mallocCString("world") }

    let t1: Int64 = s1.size()
    let t2: Bool = s2.isEmpty()
    let t3: Bool = s1.equals(s2)
    let t4: Bool = s1.startsWith(s2)
    let t5: Int32 = s1.compare(s2)

    let length = unsafe { strlen(s1) }

    unsafe {
        LibC.free(s1)
        LibC.free(s2)
    }
}
```

### sizeOf/alignOf

仓颉还提供了 `sizeOf` 和 `alignOf` 两个函数，用于获取上述 C 互操作类型的内存占用和内存对齐数值（单位：字节），函数声明如下：

```cangjie
public func sizeOf<T>(): UIntNative where T <: CType
public func alignOf<T>(): UIntNative where T <: CType
```

使用示例：

<!-- run -->

```cangjie
@C
struct Data {
    var a: Int64 = 0
    var b: Float32 = 0.0
}

main() {
    println(sizeOf<Data>())
    println(alignOf<Data>())
}
```

在 64 位机器上运行，将输出：

```text
16
8
```

## CType

除类型映射一节提供的与 C 侧类型进行映射的类型外，仓颉还提供了一个 `CType` 接口，接口本身不包含任何方法，它可以作为所有 C 互操作支持的类型的父类型，便于在泛型约束中使用。

需要注意的是：

1. `CType` 接口是仓颉中的一个接口类型，它本身不满足 `CType` 约束；
2. `CType` 接口不允许被继承、扩展；
3. `CType` 接口不会突破子类型的使用限制。

`CType` 的使用示例如下：

<!-- verify -->

```cangjie
func foo<T>(x: T): Unit where T <: CType {
    match (x) {
        case i32: Int32 => println(i32)
        case ptr: CPointer<Int8> => println(ptr.isNull())
        case f: CFunc<() -> Unit> => unsafe { f() }
        case _ => println("match failed")
    }
}

main() {
    var i32: Int32 = 1
    var ptr = CPointer<Int8>()
    var f: CFunc<() -> Unit> = { => println("Hello") }
    var f64 = 1.0
    foo(i32)
    foo(ptr)
    foo(f)
    foo(f64)
}
```

执行结果如下：

```text
1
true
Hello
match failed
```

## C 调用仓颉的函数

仓颉提供 `CFunc` 类型来对应 C 侧的函数指针类型。C 侧的函数指针可以传递到仓颉，仓颉也可以构造出对应 C 的函数指针的变量传递到 C 侧。

假设一个 C 的库 API 如下：

```c
typedef void (*callback)(int);
void set_callback(callback cb);
```

对应的，在仓颉里面这个函数可以声明为：

```cangjie
foreign func set_callback(cb: CFunc<(Int32) -> Unit>): Unit
```

CFunc 类型的变量可以从 C 侧传递过来，也可以在仓颉侧构造出来。在仓颉侧构造 CFunc 类型有两种办法，一个是用 `@C` 修饰的函数，另外一个是标记为 CFunc 类型的闭包。

`@C` 修饰的函数，表明它的函数签名是满足 C 的调用规则的，定义还是写在仓颉这边。`foreign` 修饰的函数定义是在 C 侧的。

> **注意：**
>
> `foreign` 修饰的函数与 `@C` 修饰的函数，这两种 `CFunc` 的命名不建议使用 `CJ_`（不区分大小写）作为前缀，否则可能与标准库及运行时等编译器内部符号出现冲突，导致未定义行为。

示例如下：

```cangjie
@C
func myCallback(s: Int32): Unit {
    println("handle ${s} in callback")
}

main() {
    // the argument is a function qualified by `@C`
    unsafe { set_callback(myCallback) }

    // the argument is a lambda with `CFunc` type
    let f: CFunc<(Int32) -> Unit> = { i => println("handle ${i} in callback") }
    unsafe { set_callback(f) }
}
```

假设 C 函数编译出来的库是 "libmyfunc.so"，那么需要使用 `cjc -L. -lmyfunc test.cj -o test.out` 编译命令，使仓颉编译器去链接这个库。最终就能生成想要的可执行程序。

另外，在编译 C 代码时，请打开 `-fstack-protector-all/-fstack-protector-strong` 栈保护选项，仓颉侧代码默认拥有溢出检查与栈保护功能。在引入 C 代码后，需要同步保证 unsafe 块中的溢出的安全性。

## 编译选项

使用 C 互操作通常需要手动链接 C 的库，仓颉编译器提供了相应的编译选项。

- `--library-path <value>`, `-L <value>`, `-L<value>`：指定要链接的库文件所在的目录。

  `--library-path <value>` 指定的路径会被加入链接器的库文件搜索路径。另外环境变量 `LIBRARY_PATH` 中指定的路径也会被加入链接器的库文件搜索路径中，通过 `--library-path` 指定的路径会比 `LIBRARY_PATH` 中的路径拥有更高的优先级。

- `--library <value>`, `-l <value>`, `-l<value>`：指定要链接的库文件。

  给定的库文件会被直接传给链接器，库文件名的格式应为 `lib[arg].[extension]`。

关于仓颉编译器支持的所有编译选项，详情请参见 "附录 > cjc 编译选项"。

## 示例

这里演示如何使用 C 互操作以及 `write/read` 接口对一个结构体进行赋值和读取值。

C 代码如下：

```c
// draw.c
#include<stdio.h>
#include<stdint.h>

typedef struct {
    int64_t x;
    int64_t y;
} Point;

typedef struct {
    float x;
    float y;
    float z;
} Cube;

void drawPicture(Point* point, Cube* cube) {
    point->x = 1;
    point->y = 2;
    printf("Draw Point finished.\n");

    printf("Before draw cube\n");
    printf("%f\n", cube->x);
    printf("%f\n", cube->y);
    printf("%f\n", cube->z);
    cube->x = 4.4;
    cube->y = 5.5;
    cube->z = 6.6;
    printf("Draw Cube finished.\n");
}
```

仓颉代码如下：

```cangjie
// main.cj
@C
struct Point {
    var x: Int64 = 0
    var y: Int64 = 0
}

@C
struct Cube {
    var x: Float32 = 0.0
    var y: Float32 = 0.0
    var z: Float32 = 0.0

    init(x: Float32, y: Float32, z: Float32) {
        this.x = x
        this.y = y
        this.z = z
    }
}

foreign func drawPicture(point: CPointer<Point>, cube: CPointer<Cube>): Int32

main() {
    let pPoint = unsafe { LibC.malloc<Point>() }
    let pCube = unsafe { LibC.malloc<Cube>() }

    var cube = Cube(1.1, 2.2, 3.3)
    unsafe {
        pCube.write(cube)
        drawPicture(pPoint, pCube)   // in which x, y will be changed

        println(pPoint.read().x)
        println(pPoint.read().y)
        println(pCube.read().x)
        println(pCube.read().y)
        println(pCube.read().z)

        LibC.free(pPoint)
        LibC.free(pCube)
    }
}
```

编译仓颉代码的命令如下（以 CJNative 后端为例）：

```shell
cjc -L . -l draw ./main.cj
```

其中编译命令中 `-L .` 表示链接库时从当前目录查找（假设 `libdraw.so` 存在于当前目录），`-l draw` 表示链接的库的名字，编译成功后默认生成二进制文件 `main`，执行二进制文件的命令如下：

```shell
LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH ./main
```

运行结果如下：

```shell
Draw Point finished.
Before draw cube
1.100000
2.200000
3.300000
Draw Cube finished.
1
2
4.400000
5.500000
6.600000
```
