---
name: cangjie-basic-programming-concepts
description: 仓颉编程语言基本概念和规则，当需要了解关键字、标识符、程序结构、变量定义(let/var/const)、值类型与引用类型、作用域规则、表达式(if/while/for-in/break/continue)、函数等基本概念时，应使用此
  Skill
descriptionZH: 仓颉编程语言基本概念和规则，当需要了解关键字、标识符、程序结构、变量定义(let/var/const)、值类型与引用类型、作用域规则、表达式(if/while/for-in/break/continue)、函数等基本概念时，应使用此
  Skill
tags:
  - 仓颉
  - 基础
  - 概念
---

# 仓颉编程语言基本概念和规则

## 0. 关键字

以下标识符是仓颉语言的关键字，不要用作程序元素命名（如有特殊情况需要，请用反引号 `` ` `` 转义为原始标识符）：

- **类型关键字**：`Bool`、`Rune`、`Float16`、`Float32`、`Float64`、`Int8`、`Int16`、`Int32`、`Int64`、`IntNative`、`UInt8`、`UInt16`、`UInt32`、`UInt64`、`UIntNative`、`Array`、`VArray`、`String`、`Nothing`、`Unit`
- **控制流关键字**：`break`、`case`、`catch`、`continue`、`do`、`else`、`finally`、`for`、`if`、`match`、`return`、`spawn`、`try`、`throw`、`while`
- **声明关键字**：`as`、`abstract`、`class`、`const`、`enum`、`extend`、`func`、`foreign`、`import`、`init`、`interface`、`let`、`macro`、`main`、`mut`、`open`、`operator`、`override`、`package`、`private`、`prop`、`protected`、`public`、`redef`、`static`、`struct`、`super`、`synchronized`、`this`、`This`、`type`、`unsafe`、`where`
- **布尔关键字**：`false`、`true`
- **其他**：`quote`

---

## 1. 标识符

### 1.1 普通标识符
- 以 `XID_Start` 字符（包括中英文字母）开头，后跟 `XID_Continue` 字符；或以 `_` 开头后跟至少一个 `XID_Continue` 字符
- 不能是仓颉关键字
- 使用 Unicode 15.0.0 标准，NFC 规范化
- 示例：`abc`、`_abc`、`仓颉`

### 1.2 原始标识符
- 用反引号包裹普通标识符或关键字：`` `while` ``、`` `if` ``
- 用于将关键字作为标识符使用

---

## 2. 程序结构

### 2.1 顶层作用域
- 允许声明：全局变量、全局函数、自定义类型（`struct`、`class`、`enum`、`interface`）、`main` 入口函数
- 非顶层作用域允许局部变量和局部函数
- `enum`/`interface` 仅支持成员函数（不支持成员变量）

### 2.2 变量定义
- 语法：`修饰符 名称: 类型 = 值`
- 修饰符：
  - `let`：不可变，只能赋值一次
  - `var`：可变，可多次赋值
  - `const`：编译时常量
- 类型标注可省略（当可推断时）
- 全局/静态变量须初始化
- 局部变量可延迟初始化，但使用前必须赋值

### 2.3 const 变量
- 语法：`const G = 6.674e-11`
- 不能省略初始化器
- 可用于全局、局部或静态成员
- 支持 `const init` 和 `const func`

### 2.4 值类型与引用类型
- **值类型**（基础类型，`struct`，`VArray`...）：赋值拷贝数据，`let` 阻止所有修改。一般存放在栈空间。
- **引用类型**（`class`，`String`，`Array`...）：赋值共享引用，`let` 阻止重新赋值但不阻止修改引用对象的数据。存放在托管内存，涉及 GC。

> **注意**：`Array` 是用 `struct` 定义的，但把数组数据存放在托管内存中（结构体中一个引用类型成员），赋值后两个变量共享底层存储，修改互相可见

### 2.5 作用域规则
- `{}` 创建作用域
- 内层作用域可遮蔽外层同名变量
- 顶层作用域为最外层

---

## 3. 表达式

### 3.1 基本规则
- 仓颉中所有可求值的程序元素都是表达式，包括算术表达式和 if/match 等复合表达式
- 每个表达式建议写在不同行，特殊情况下可以在同一行用分号分隔多个表达式（如简单的 lambda 定义）
- 如无特殊说明，文档中使用 **exprs** 表示一组表达式（0~N 个）
- 代码块 `{exprs}`：代码块只是便于文档描述而提出的概念，仓颉**不允许独立的 `{exprs}` 块**作为表达式（如 `let r = { let x = 2; x ** 3 }` 不合法）。代码块只能依附于 if/while/for-in/match/函数等表达式使用（构造这些复合表达式），一般情况下，含有代码块结构的表达式，其值/类型为所执行代码块（分支）中最后一个表达式的值/类型（空块类型为 `Unit`，值为 `()`）

### 3.2 if 条件判断
- 语法：`if (cond) { exprs1 } else { exprs2 }`，`cond` 是 `Bool` 类型表达式
- 支持 `else if` 链式使用
- 用作值时：有 `else` 时类型由上下文或各分支最小公共父类型决定，值为所执行分支最后一个表达式的值，无 `else` 时类型始终为 `Unit`
- 条件表达式可以用 `let pattern <- expr` 做模式匹配，详见 `cangjie-pattern-match` Skill

### 3.3 while / do-while 循环
- 语法：`while (cond) { exprs }` 和 `do { exprs } while (cond)`，`cond` 是 `Bool` 类型表达式
- 返回类型始终为 `Unit`
- 条件表达式可以用 `let pattern <- expr` 做模式匹配

### 3.4 for-in 循环
- 语法：`for (item in sequence) { exprs }`，其中 `sequence` 类型须实现 `Iterable<T>`
- 迭代变量 item 不可变，如果循环体中不引用迭代变量，可用通配符 `_` 占位
- 支持元组解构：`for ((x, y) in arr)`
- `where` 子句过滤迭代：`for (i in 0..8 where i % 2 == 1)`
- String，Range（1..=100），Array/HashMap 等集合类型都已实现 `Iterable<T>`，可直接用 for-in 遍历
- 详见 `cangjie-for` Skill

### 3.5 break / continue
- `break` 退出循环，`continue` 跳至下一次迭代
- 二者的类型均为 `Nothing`

### 3.6 match 模式匹配
- 语法：`match(expr) { case pattern => exprs ... }`，`expr` 是待匹配值，`pattern` 是候选模式
- `=>` 左侧模式被匹配后，将执行右侧的 `exprs` 并跳过后续 `case` 分支
- 注意，exprs 不需要被大括号包裹，多个表达式各占一行
- 详见 `cangjie-pattern-match` Skill

---

## 4. 函数（基本概念）

- 使用 `func name(params): ReturnType { exprs }` 定义
- 参数以逗号分隔，格式为 `name: Type`
- 函数体 exprs 最后一个表达式默认作为返回值（可以省略 return），但一般情况下建议写 return
- 详见 `cangjie-function` Skill

---

## 5. 创建、编译和运行仓颉项目

- 创建项目：`cjpm init`
- 构建项目: `cjpm build`
- 运行项目（生成可执行文件的项目）：`cjpm run`
- 测试项目：`cjpm test`
- 更多用法详见 `cangjie-project-management` Skill

