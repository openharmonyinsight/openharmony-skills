# 使用 CString 与 C 代码交互示例

C 代码中分别提供两个函数： `getCString` 函数，用于返回一个 C 侧的字符串指针； `printCString` 函数，用于打印来自仓颉侧 CString 。

```c
#include <stdio.h>

char *str = "CString in C code.";

char *getCString() { return str; }

void printCString(char *s) { printf("%s\n", s); }
```

在仓颉代码中，创建一个 CString 对象，传递给 C 侧打印。并且获取 C 侧字符串，在仓颉侧打印：

示例：

<!-- special -->

```cangjie
foreign func getCString(): CString
foreign func printCString(s: CString): Unit

main() {
    // 仓颉侧构造 CString 实例，传递到 C 侧
    unsafe {
        let s: CString = LibC.mallocCString("CString in Cangjie code.")
        printCString(s)
        LibC.free(s)
    }

    unsafe {
        // C 侧申请字符串指针，传递到仓颉侧成为 CString 实例，再转换为仓颉字符串 String 类型
        let cs = getCString()
        println(cs.toString())
    }

    // 在 try-with-resource 语法上下文中使用 CStringResource 自动管理 CString 内存
    let cs = unsafe { LibC.mallocCString("CString in Cangjie code.") }
    try (csr = cs.asResource()) {
        unsafe { printCString(csr.value) }
    }

    0
}
```

运行结果：

```text
CString in Cangjie code.
CString in C code.
CString in Cangjie code.
```

> **说明：**
>
> 编译方式：先将 C 代码编译成静态库或动态库，然后编译仓颉代码并链接 C 库。
> 假设 C 文件为 test.c，仓颉文件为 test.cj，编译过程如下：
>
> 1. 使用 gcc 命令 `gcc -fPIC -shared test.c -o libtest.so`，编出 C 库 `libtest.so`。
> 2. 使用 cjc 命令 `cjc -L . -l test test.cj`，编出可执行文件 `main`。
