---
name: cangjie-package
description: 仓颉语言包管理。当需要了解仓颉语言的包声明(package)、程序入口(main)、包导入(import)、重新导出(public
  import)、顶层访问修饰符(private/internal/protected/public)等特性时，应使用此 Skill
descriptionZH: 仓颉语言包管理。当需要了解仓颉语言的包声明(package)、程序入口(main)、包导入(import)、重新导出(public
  import)、顶层访问修饰符(private/internal/protected/public)等特性时，应使用此 Skill
tags:
  - 仓颉
  - 包管理
---

# 仓颉语言包管理 Skill

## 1. 包概述

### 1.1 基本概念
- **包**是最小编译单元，产生 AST/静态/动态库文件
- 每个包有自己的命名空间（顶层名称不允许重复，函数重载除外）
- **模块**是包的集合，是最小分发单元
- 模块的 `main` 入口须在其根目录中

---

## 2. 包声明

### 2.1 语法
- 使用 `package pkg1.sub1` 声明，须与相对于 `src/` 的目录路径匹配
- 须为文件中第一个非空/非注释行
- 同一包中所有文件须有相同的包声明
- 目录名须与包名匹配
- `src/` 根目录的文件如果没有包声明，则默认为 `default` 包
- 子包不能与顶层声明同名
- Windows 上包名仅限 ASCII

### 2.2 目录结构与包声明示例
```text
src
|-- network
|   |-- http
|   |    |-- client.cj   // package default.network.http
|   |    |-- server.cj   // package default.network.http
|   |-- util.cj          // package default.network
|-- main.cj              // 可省略包声明，默认为 default 包
```
```cangjie
// client.cj — 包声明须匹配相对于 src/ 的路径
package default.network.http

public class HttpClient { /* ... */ }
```

### 2.3 子包与顶层声明不能同名
```cangjie
// 错误示例
package a
public class B {}  // ❌ 错误：B 与子包 a.B 冲突
```

---

## 3. 程序入口

### 3.1 `main` 函数
- `main` 是入口点，每个根包最多一个
- 不能有访问修饰符
- 被导入包时不会被导入
- 参数：无参或 `Array<String>`
- 返回类型：`Unit` 或整数类型
- 定义时不使用 `func` 关键字

### 3.2 `main` 函数示例
```cangjie
// 无参 main，返回整数
main(): Int64 {
    return 0
}
```
```cangjie
// 带命令行参数的 main
main(args: Array<String>): Unit {
    for (arg in args) {
        println(arg)
    }
}
```
```cangjie
// ❌ 错误：返回类型不能是 String
main(): String { return "" }
```
```cangjie
// ❌ 错误：参数类型只能是 Array<String>
main(args: Array<Int8>): Int64 { return 0 }
```

---

## 4. 包导入

### 4.1 语法
```cangjie
import fullPkg.item           // 导入单个声明
import fullPkg.{a, b}         // 导入多个声明
import fullPkg.*              // 导入所有可见声明
import {pkg1.*, pkg2.*}       // 同时导入多个包
```

### 4.2 规则
- 须在 `package` 之后、其他声明之前
- 导入成员的作用域优先级低于当前包
- 不允许循环依赖
- 不能导入当前包
- 不能导入不可见的声明

### 4.3 遮蔽与重载
- 导入的名称被同名本地声明遮蔽（除非构成函数重载，此时适用重载解析）
```cangjie
// package pkga
package pkga
public struct R {}
public func f(a: Int32) {}
public func f(a: Bool) {}
```
```cangjie
// package pkgb
package pkgb
import pkga.*

struct R {}                 // 本地 R 遮蔽导入的 R
func f(a: Int32) {}         // 本地 f(Int32) 遮蔽导入的同签名函数

func bar() {
    R()     // 使用本地 R
    f(1)    // 调用本地 f(Int32)
    f(true) // 调用导入的 f(Bool)，构成重载
}
```

### 4.4 隐式 core 导入
- `String`、`Range` 等可用是因为 `core` 包被自动导入

### 4.5 import as（重命名导入）
- 重命名导入以解决冲突：`import pkg.name as newName`、`import pkg as alias`
- 重命名后原名不可用
- 不重命名时，冲突名称在使用处报错（非导入处）
- 也可 `import fullPkg` 用作命名空间限定符
```cangjie
// 用 import as 解决名称冲突
import p1.C as C1
import p2.C as C2

main() {
    let _ = C1()  // 使用 p1 的 C
    let _ = C2()  // 使用 p2 的 C
}
```
```cangjie
// 用包名作为命名空间限定符
import p1
import p2

main() {
    let _ = p1.C()  // 通过包名限定
    let _ = p2.C()  // 通过包名限定
}
```

### 4.6 重新导出
- `public import`、`protected import`、`internal import` 重新导出导入的成员
- `private import`（默认）将导入限制为文件内可见
- 包本身不能被重新导出
```cangjie
// package a — 重新导出子包的声明
package a
public import a.b.f   // 将 a.b 中的 f 重新导出

public let x = 0
```
```cangjie
// package a.b
internal package a.b
public func f(): Int64 { 0 }
```
```cangjie
// 外部包可直接通过 package a 访问 f
import a.f  // OK
let _ = f() // OK
```
```cangjie
// ❌ 错误：包不能被重新导出
public import a.b  // Error
```

---

## 5. 顶层访问修饰符

### 5.1 四个级别
| 修饰符 | 当前文件 | 包及子包 | 当前模块 | 全局 |
|--------|---------|---------|---------|------|
| `private` | ✓ | ✗ | ✗ | ✗ |
| `internal`（默认） | ✓ | ✓ | ✗ | ✗ |
| `protected` | ✓ | ✓ | ✓ | ✗ |
| `public` | ✓ | ✓ | ✓ | ✓ |

### 5.2 默认修饰符
- `package` 声明默认为 `public`
- `import` 默认为 `private`
- 其他顶层声明默认为 `internal`

### 5.3 访问级别约束
- 声明的访问级别不能超过其使用的类型（参数、返回类型、泛型、where 约束）的访问级别
- 但 `public` 声明可在内部（函数体、初始化表达式中）使用非 public 类型
- 内置类型如 `Int64` 为 `public`
- 同包中同名的 `private` 声明在导出时可能导致错误
```cangjie
package a

private func f1() { 1 }   // 仅当前文件可见
func f2() { 2 }           // internal：当前包及子包可见
protected func f3() { 3 } // 当前模块可见
public func f4() { 4 }    // 全局可见
```
```cangjie
// ❌ 错误：public 声明不能使用 internal 类型作为参数/返回值
class C {}  // 默认 internal
public func f1(a: C): Int64 { 0 }  // Error
public let v1: C = C()      // Error
```
