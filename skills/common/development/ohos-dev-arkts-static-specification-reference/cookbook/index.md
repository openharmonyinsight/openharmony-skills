# ArkTS Cookbook - TypeScript 迁移指南

## 概述

ArkTS Cookbook 提供从标准 TypeScript 迁移到 ArkTS 的实用指南和"食谱"（recipes）。ArkTS 设计上接近 TypeScript，但为提升性能添加了一些限制。

---

## TypeScript 特性分类

| 分类 | 说明 | 代码保持率 |
|------|------|-----------|
| **完全支持** | 无需修改原代码 | 90% - 97% |
| **部分支持** | 需要少量代码重构 | 例如：`var` → `let` |
| **不支持** | 需要大量代码重构 | 例如：`any` 类型 |

**注意**：即使经过部分支持的特性重写，代码仍然是有效的 TypeScript。

---

## 为什么从 TypeScript 迁移到 ArkTS

### 1. 程序稳定性提升

**问题**：动态类型语言（如 JS）容易出现运行时错误

**TypeScript 的局限**：
- 允许"宽松"的类型注解
- `undefined` 可能作为隐式值

**ArkTS 的改进**：
- 强制严格类型检查
- 字段必须初始化（类似 TS 的 `strictPropertyInitialization`）
- `null` 和 `undefined` 不能赋值给非空类型

**示例**：

```typescript
// TypeScript - 可能运行时错误
class Person {
    name: string  // 隐式为 undefined
    getName(): string {
        return this.name  // 可能返回 undefined
    }
}

// ArkTS - 编译时捕获错误
class Person {
    name: string = ""  // 必须初始化
    getName(): string {
        return this.name  // 保证返回 string
    }
}
```

### 2. 程序性能提升

**TypeScript 编译为 JavaScript**：
- 需要运行时类型检查
- 无法完全消除类型检查开销
- 字符串拼接时需要检查 `null`/`undefined`

**ArkTS 编译为字节码**：
- 类型在编译时确定
- 消除运行时类型检查
- 执行效率更高

---

## ArkTS 核心设计原则

### 静态类型强制执行

| 原则 | 说明 |
|------|------|
| 禁止 `any` | 必须使用显式类型 |
| 禁止 `unknown` | 必须使用显式类型 |
| 类型编译时确定 | 所有类型在编译时已知 |
| 使用 `ESObject` 与 JS 互操作 | 仅在必要时使用，会有性能开销 |

**示例**：

```typescript
// ❌ 错误
let value: any = someFunction()

// ✅ 正确
interface Result {
    succeeded(): boolean
    errorMessage(): string
}
let value: Result = someFunction()
```

### 运行时对象布局不可变

| 禁止操作 | 原因 |
|---------|------|
| 添加新属性/方法 | 破坏静态类型 |
| 删除现有属性/方法 | 破坏对象结构确定性 |
| 任意类型赋值给属性 | 破坏类型安全 |

**示例**：

```typescript
class Point {
    x: number = 0
    y: number = 0
}

let p = new Point()

// ❌ TypeScript 允许（用 as any 绕过），ArkTS 禁止
delete (p as any).x
p.z = "Label"
(p as any).x = "Hello!"

// ✅ ArkTS 保证对象布局不变
// Point 对象永远只有 x 和 y 属性，类型永远为 number
```

### 运算符语义收窄

为了更清晰的代码和更好的性能，ArkTS 收窄了部分运算符的语义。

**示例**：

```typescript
// ❌ 错误：一元 + 仅对数字有效
console.log(+"42")  // 编译错误

// ✅ 正确
console.log(+42)    // OK
console.log(parseInt("42"))  // 转换字符串为数字
```

### 不支持结构化类型（暂缓）

**TypeScript**（结构化类型）：
```typescript
class T {
    name: string = ""
}
class U {
    name: string = ""
}
let u: U = new T()  // OK，因为结构兼容
```

**ArkTS**（名义类型）：
```typescript
class T {
    name: string = ""
}
class U {
    name: string = ""
}
let u: U = new T()  // ❌ 编译错误，T 和 U 不兼容
```

**解决方案**：
```typescript
interface Nameable {
    name: string
}
class T implements Nameable {
    name: string = ""
}
class U implements Nameable {
    name: string = ""
}
let u: Nameable = new T()  // ✅ OK
```

---

## 使用 Cookbook 指南

### 严重性级别

每个食谱都有严重性标记：

| 级别 | 符号 | 说明 |
|------|------|------|
| ERROR | `|CB_ERROR|` | 必须遵循，否则编译失败 |
| WARNING | `|CB_WARNING|` | 强烈建议遵循，未来版本可能导致编译失败 |

### 食谱格式

每个食谱包含以下部分：

```rst
|CB_R| [标题]
|CB_RULE| [规则名称]

|CB_ERROR| 或 |CB_WARNING|

[说明]

|CB_BAD|
[错误代码示例]

|CB_OK|
[正确代码示例]

|CB_SEE|
[相关食谱引用]
```

### 查找策略

1. **如果特性未列出**：视为完全支持
2. **查看相关食谱**：每个食谱末尾有相关食谱链接
3. **优先处理 ERROR 级别**：确保代码能编译通过

---

## 主要差异总结

### 1. 字段必须初始化

```typescript
// ❌ TypeScript
class Person {
    name: string
}

// ✅ ArkTS
class Person {
    name: string = ""
}
```

### 2. null 安全

```typescript
// ❌ 编译错误
function notify(who: string, what: string) {
    console.log(`Dear ${who}, ${what}`)
}
notify(null, undefined)  // ArkTS 编译错误

// ✅ 使用联合类型显式允许
function notifyNullable(who: string | null, what: string | null) {
    console.log(`Dear ${who ?? "someone"}, ${what ?? "something"}`)
}
```

### 3. 对象属性不能动态添加/删除

```typescript
class Point {
    x: number = 0
    y: number = 0
}

let p = new Point()

// ❌ 全部编译错误
delete p.x
p.z = "label"
(p as any).newProp = 123

// ✅ 使用类定义所有属性
class Point {
    x: number = 0
    y: number = 0
    label: string = ""
}
```

---

## 不支持的主要特性概览

| 特性 | 食谱编号 | 严重性 |
|------|---------|--------|
| `any` / `unknown` 类型 | R008 | ERROR |
| `var` 声明 | R005 | ERROR |
| 非标识符属性名 | R001 | ERROR |
| `Symbol()` API | R002 | ERROR |
| 私有 `#` 标识符 | R003 | ERROR |
| 调用签名类型 | R014 | ERROR |
| 构造签名类型 | R015 | ERROR |
| `in` 运算符 | R068 | ERROR |
| 对象解构 | R069, R074 | ERROR |
| `require` 导入 | R121 | ERROR |
| `export =` 语法 | R126 | ERROR |

---

## 兼容性说明

### 数值语义差异

```typescript
let n = 1

// TypeScript: 0.5 (浮点除法)
// ArkTS: 0 (整数除法)
console.log(n / 2)
```

### Math.pow 差异

| 调用 | TypeScript | ArkTS |
|------|-----------|-------|
| `pow(-1, Infinity)` | `NaN` | `1` |
| `pow(1, NaN)` | `NaN` | `1` |

ArkTS 符合最新的 IEEE 754-2019 标准。

---

## 迁移建议

1. **优先处理 ERROR 级别食谱**：确保代码能编译
2. **保持 TypeScript 兼容性**：食谱的解决方案仍然是有效 TS 代码
3. **利用类型系统**：使用接口和类明确类型关系
4. **避免动态特性**：减少运行时反射和动态属性访问
5. **参考详细食谱**：见 [cookbook-recipes.md](cookbook-recipes.md)
6. **查看兼容性详情**：见 [cookbook-compatibility.md](cookbook-compatibility.md)

---

## 参考资源

- **详细食谱列表**：[cookbook-recipes.md](cookbook-recipes.md) - 144+ 个详细迁移食谱
- **兼容性说明**：[cookbook-compatibility.md](cookbook-compatibility.md) - TypeScript vs ArkTS 详细差异
- **原始规范**：`D:\arkcompiler\runtime_core\static_core\plugins\ets\doc\cookbook\`
