---
name: cangjie-reflect-and-annotation
description: 仓颉语言反射与注解。当需要了解仓颉语言的整数溢出注解(@OverflowThrowing/@OverflowWrapping/@OverflowSaturating)、自定义注解(@Annotation)、反射(TypeInfo)等特性时，应使用此
  Skill。
descriptionZH: 仓颉语言反射与注解。当需要了解仓颉语言的整数溢出注解(@OverflowThrowing/@OverflowWrapping/@OverflowSaturating)、自定义注解(@Annotation)、反射(TypeInfo)等特性时，应使用此
  Skill。
tags:
  - 仓颉
  - 反射
  - 注解
---

# 仓颉语言反射与注解 Skill

## 1. 注解

### 1.1 整数溢出注解
三种内置注解控制函数的溢出策略：
- **`@OverflowThrowing`**（默认）：溢出时抛出 `ArithmeticException`。尽可能在编译时检测
- **`@OverflowWrapping`**：截断高位（模运算）
- **`@OverflowSaturating`**：饱和到类型最小/最大值

可溢出的运算符：`+`、`-`、`*`、`/`、`**`、`++`、`--`、`<<`、`+=`、`-=`、`*=`、`/=`、`**=`、`<<=`

### 1.2 测试框架注解
- `@EnsurePreparedToMock` 为静态/顶层声明准备 mock
- 仅在 `--test`/`--mock=on` 编译时允许

### 1.3 自定义注解
- 通过用 `@Annotation` 标记 `class` 创建
- 类不能为 `abstract`/`open`/`sealed`，须提供至少一个 `const init`
- 使用方式：`@MyAnnotation[args]` 应用于类型、成员、构造函数、参数、属性
- 通过 `TypeInfo.of(obj).findAnnotation<T>()` 获取

#### 规则
- 同一注解不能两次应用于同一目标
- 注解**不被**子类继承
- `@Annotation[target: [AnnotationKind...]]` 限制有效目标
- 有效目标种类：`Type`、`Parameter`、`Init`、`MemberProperty`、`MemberFunction`、`MemberVariable`
- 参数须为 `const` 表达式
- 无参注解可省略 `[]`

---

## 2. 反射（动态特性）

### 2.1 TypeInfo
- 核心反射类型
- 获取方式：
  - `TypeInfo.of(instance: Any)` — 从实例
  - `TypeInfo.of(obj: Object)` → `ClassTypeInfo` — 从对象
  - `TypeInfo.of<T>()` — 从类型参数
  - `TypeInfo.get(qualifiedName)` — 从限定名（如 `"std.socket.TcpSocket"`）
- 内置类型使用裸名（如 `"Int64"`）
- 不能获取未实例化泛型类型的 TypeInfo

### 2.2 访问成员
- 仅 `public` 成员对反射可见
- **访问变量**：
  - `getInstanceVariable(name)` / `getStaticVariable(name)` → `getValue()` / `setValue()`
- **访问属性**：
  - `getInstanceProperty(name)` → `getValue(obj)` / `setValue(obj, val)`
  - 使用 `isMutable()` 检查是否可变
- **调用函数**：
  - `getStaticFunction(name, paramTypeInfos...)` → `funcInfo.apply(typeInfo, [args])`
