---
name: cangjie-error-handle
description: 仓颉语言错误处理。当需要了解仓颉语言的异常层次(Error/Exception)、自定义异常、throw、try/catch/finally、try-with-resources、CatchPattern、Option类型错误处理(?./??/getOrThrow)、内置运行时异常等特性时，应使用此
  Skill。
descriptionZH: 仓颉语言错误处理。当需要了解仓颉语言的异常层次(Error/Exception)、自定义异常、throw、try/catch/finally、try-with-resources、CatchPattern、Option类型错误处理(?./??/getOrThrow)、内置运行时异常等特性时，应使用此
  Skill。
tags:
  - 仓颉
  - 错误处理
---

# 仓颉语言错误处理 Skill

## 1. 异常层次与定义

### 1.1 两种基础异常类型
- **`Error`** — 内部系统/资源耗尽错误。应用程序**不应**抛出或继承 `Error`。仅用于安全终止程序
- **`Exception`** — 逻辑错误、IO 错误、数组越界等。这些**须**被捕获处理。开发者**可以**继承 `Exception` 创建自定义异常

### 1.2 自定义异常规则
- ❌ 不能继承 `Error` 或其子类
- ✅ 可使用 `<:` 继承 `Exception` 或其子类
- 使用 `open class` 允许进一步继承；使用 `class` 表示最终异常

### 1.3 `Exception` API
| 类型 | 签名 | 说明 |
|------|------|------|
| 构造函数 | `init()` | 默认构造函数 |
| 构造函数 | `init(message: String)` | 带消息构造函数 |
| 属性 | `open prop message: String` | 详细消息 |
| 方法 | `open func toString(): String` | 类型名 + 消息 |
| 方法 | `func getClassName(): String` | 类名；子类须重写 |
| 方法 | `func printStackTrace(): Unit` | 打印堆栈跟踪到 stderr |

### 1.4 `Error` API
| 类型 | 签名 | 说明 |
|------|------|------|
| 属性 | `open prop message: String` | 详细消息 |
| 方法 | `open func toString(): String` | 类型名 + 消息 |
| 方法 | `func printStackTrace(): Unit` | 堆栈跟踪到 stderr |

---

## 2. 抛出与处理异常

### 2.1 `throw` 关键字
- `throw <expr>` 其中 `<expr>` 须为 `Exception` 子类型（不能抛出 `Error`）
- 未处理的异常调用默认处理器，或通过以下方式注册自定义处理器：
  ```cangjie
  Thread.handleUncaughtExceptionBy(exHandler: (Thread, Exception) -> Unit): Unit
  ```

### 2.2 普通 `try` 表达式

三个块：**try**、**catch**（0+）、**finally**（有 catch 时可选，无 catch 时须有）

#### 语法示例
```cangjie
try {
    throw NegativeArraySizeException("error!")
} catch (e: NegativeArraySizeException) {
    println(e)
} catch (e: IllegalArgumentException | ArithmeticException) {
    println("Other exception: ${e}")
} catch (_) {
    println("Unknown exception")
} finally {
    println("cleanup")
}
```

#### 规则
- `try` 块：包含可能抛出异常的代码。定义独立作用域
- `catch` 块：使用 **catchPattern** 通过模式匹配捕获异常。首个匹配的 catch 执行；后续 catch 被跳过。编译器在 catch 不可达（被前面的 catch 遮蔽）时发出警告
- `finally` 块：无论是否有异常始终执行。用于清理。避免在 finally 中抛出异常。即使异常未被捕获也会执行（然后重新抛出）
- 每个 `try`/`catch` 块有**独立作用域**

#### try 表达式类型
- try 块 + 所有 catch 块的最小公共父类型（**不包括** finally）
- 若 try 表达式的值未使用，类型为 `Unit`

### 2.3 `try-with-resources` 表达式

用于**自动资源管理**。资源声明在 `try` 和 `{}` 之间。

#### 关键规则
- `catch` 和 `finally` 块**可选**
- 资源须实现 **`Resource` 接口**：
  ```cangjie
  interface Resource {
      func isClosed(): Bool
      func close(): Unit
  }
  ```
- 多个资源用 `,` 分隔
- 资源变量作用域 = 体作用域
- try-with-resources 表达式的类型始终为 **`Unit`**

#### 语法
```cangjie
try (r = Worker("Tom")) {
    r.getTools()
    r.work()
}  // 若 r.isClosed() == false 则自动调用 r.close()
```

### 2.4 CatchPattern

#### 类型模式
1. **单类型**：`Identifier: ExceptionClass` — 捕获该类及子类，绑定到 `Identifier`
2. **联合类型**：`Identifier: E1 | E2 | ... | En` — 捕获任意列出的类型。绑定变量类型为所有列出类型的**最小公共父类型**

#### 通配符模式
- `_` — 捕获**任何**异常（等价于 `e: Exception`）。无绑定

---

## 3. 使用 Option 处理错误

`Option<T>`（简写 `?T`）表示值的**存在（`Some(v)`）或缺失（`None`）**

### 3.1 四种解构/使用方式

#### (a) 模式匹配（`match`）
```cangjie
match (p) {
    case Some(x) => "${x}"
    case None => "none"
}
```

#### (b) 合并运算符 `??`
- `e1 ?? e2` — 若 `e1` 为 `Some(v)` 返回解包值，否则返回 `e2`

#### (c) 问号运算符 `?`（可选链）
- 配合 `.`、`()`、`[]`、`{}`（尾随 Lambda）使用
- `e?.b` → 若 `e == Some(v)` 则 `Some(v.b)`，否则 `None`
- 支持**多级链式调用**：`a?.b.c?.d` — 首个 `None` 处短路
- 支持可选链上的**赋值**：`c1?.item = 200`（`None` 时为空操作）

#### (d) `getOrThrow()` 函数
- `Some(v)` 时返回解包值
- `None` 时抛出 `NoneValueException`

---

## 4. 内置运行时异常

| 异常 | 说明 |
|------|------|
| `ConcurrentModificationException` | 并发修改错误 |
| `IllegalArgumentException` | 非法或不正确的参数 |
| `NegativeArraySizeException` | 以负数大小创建数组 |
| `NoneValueException` | 值不存在 |
| `OverflowException` | 算术溢出 |
