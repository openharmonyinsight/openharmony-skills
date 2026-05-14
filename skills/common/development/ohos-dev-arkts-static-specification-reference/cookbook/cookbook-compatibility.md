# ArkTS - TypeScript 兼容性详细说明

## 概述

本文档详细说明了 ArkTS 和 TypeScript 之间的行为差异和兼容性问题。

---

## 核心行为差异

### 1. undefined 不是通用值

**状态**：`frontend_status: Done`

TypeScript 中运行时值 `undefined` 的许多场景在 ArkTS 中会导致编译时或运行时错误。

#### 示例

```typescript
// TypeScript
let array = new Array<number>(3)
let x = array[1234]  // x 被赋值为 undefined
console.log(x)  // undefined

// ArkTS
let array = new Array<number>(3)
let x = array[1234]  // 编译时错误（如果可检测）或运行时错误 ArrayOutOfBounds
```

---

### 2. 数值语义差异

**状态**：`frontend_status: Done`

TypeScript 有单一的数值类型 `number` 处理整数和实数。ArkTS 将 `number` 解释为多种类型，根据上下文产生不同结果。

#### 示例

```typescript
let n = 1
// TypeScript: n 的类型是 number
// ArkTS: n 的类型是 int（为了最大化性能）

console.log(n / 2)
// TypeScript: 输出 0.5（浮点除法）
// ArkTS: 输出 0（整数除法）
```

#### 类型推断规则

| 字面量 | TypeScript | ArkTS |
|--------|-----------|-------|
| `1` | `number` | `int` |
| `1.0` | `number` | `double` |
| `2147483647` | `number` | `int` |
| `2147483648` | `number` | `long` |

---

### 3. 协变重写禁止

**状态**：`frontend_status: Done`

TypeScript 的对象运行时模型允许处理运行时访问不存在的属性。ArkTS 依赖于编译时已知的对象布局来生成高效代码。协变重写破坏类型安全，因此被禁止。

#### 示例

```typescript
class Base {
   foo(p: Base) {}
}
class Derived extends Base {
   override foo(p: Derived)  // ArkTS 编译时错误 - 不正确的重写
   {
       console.log("p.field unassigned = ", p.field)  // TS: undefined
       p.field = 42  // 访问字段
       p.method()  // TS: 运行时错误 p.method is not a function
   }
   method() {}
   field: number = 0
}

let base: Base = new Derived
base.foo(new Base)  // TypeScript: 可能运行时错误
```

#### 原因

- 基类引用可能指向派生类实例
- 调用 `base.foo(new Base)` 时，`p` 实际是 `Base` 类型
- 但 `Derived.foo` 期望 `Derived` 类型，可能访问不存在的成员

---

### 4. 函数类型兼容性

**状态**：`frontend_status: Done`

TypeScript 允许相当宽松的函数类型赋值。ArkTS 使用更严格的规则。

#### 示例

```typescript
type FuncType = (p: string) => void

// ArkTS 编译时错误
let f1: FuncType = (p: string): number => { return 0 }
let f2: FuncType = (p: string): string => { return "" }
```

#### 规则

- 返回类型必须完全匹配
- 参数类型必须完全匹配
- 不允许协变或逆变

---

### 5. 工具类型兼容性

**状态**：`frontend_status: Done`

TypeScript 中 `Partial<T>` 可赋值给 `T`。ArkTS 中 `Partial<T>` 不可赋值给 `T`，只能用对象字面量初始化。

#### 示例

```typescript
function foo<T>(t: T, part_t: Partial<T>) {
    part_t = t  // ArkTS 编译时错误
}
```

#### 正确用法

```typescript
function foo<T>(t: T, part_t: Partial<T>) {
    // Partial<T> 只能用对象字面量初始化
    let partial: Partial<T> = { /* 部分属性 */ }
}
```

---

### 6. 函数重载签名

**状态**：`frontend_status: Done`

TypeScript 支持多个函数签名后跟单个实现。ArkTS 不支持，每个重载必须有独立实现。

#### TypeScript 风格（不支持）

```typescript
function foo(): void
function foo(x: string): void
function foo(x?: string): void {
    /* 单个实现 */
}
```

#### ArkTS 风格

```typescript
function foo(): void {
    /* 实现 1 */
}
function foo(x: string): void {
    /* 实现 2 */
}
```

---

### 7. 继承时的类字段

**状态**：`frontend_status: None`

TypeScript 允许子类用协变类型覆盖父类字段。ArkTS 仅允许不变类型覆盖。

#### 不变类型覆盖（两者都支持）

```typescript
class Base {
  field: number = 123
}
class Derived extends Base {
  field: number = 456  // OK，类型相同
}
let b: Base = new Derived()
console.log(b.field)  // 456
```

#### 协变类型覆盖（仅 TypeScript 支持）

```typescript
class Parent {
    field: Object
}
class Child extends Parent {
    field: Number  // ArkTS 编译时错误
}
```

---

### 8. void 类型兼容性

**状态**：`frontend_status: Done`

TypeScript 允许 `void` 用于联合类型。ArkTS 不允许。

#### 示例

```typescript
type UnionWithVoid = void | number
// TypeScript: OK
// ArkTS: 编译时错误
```

---

### 9. 数组赋值

**状态**：`frontend_status: None`

TypeScript 允许协变数组赋值。ArkTS 仅允许不变数组赋值。

#### TypeScript 风格

```typescript
let a: Object[] = [1, 2, 3]
let b = [1, 2, 3]  // 类型: number[]
a = b  // TypeScript: OK
```

#### ArkTS 风格

```typescript
let a: Object[] = [1, 2, 3]
let b = [1, 2, 3]  // 类型推断为 double[]
a = b  // ArkTS: 编译时错误

let a: Object[] = ["a", "b", "c"]
let b: string[] = ["a", "b", "c"]
a = b  // ArkTS: 编译时错误
```

---

### 10. 元组和数组

**状态**：`frontend_status: None`

TypeScript 允许将元组赋值给数组。ArkTS 将元组和数组视为不同类型，不允许相互赋值。

#### 示例

```typescript
const tuple: [number, number, boolean] = [1, 3.14, true]
const array: (number | boolean)[] = tuple
// TypeScript: 接受
// ArkTS: 编译时错误
```

---

### 11. 扩展 Object 类

**状态**：`frontend_status: Done`

TypeScript 要求显式列出 `extends Object` 才能使用 `super` 和 `override`。ArkTS 允许隐式继承。

#### TypeScript 风格

```typescript
class A {
   override toString() {  // 编译错误
       return super.toString()  // 编译错误
   }
}

class A extends Object {  // 正确形式
   override toString() {
       return super.toString()
   }
}
```

#### ArkTS 风格

```typescript
class A {
   override toString() {  // OK
       return super.toString()  // OK
   }
}
```

---

### 12. extends 和 implements 子句语法

**状态**：`frontend_status: Done`

TypeScript 将 `extends` 和 `implements` 中的实体作为表达式处理。ArkTS 在编译时处理，只允许类型引用，不允许表达式。

#### 示例

```typescript
class B {}
class A extends (B) {}  // TypeScript: OK，ArkTS: 编译时错误
```

---

### 13. 函数对象的唯一性

**状态**：`frontend_status: Done`

TypeScript 和 ArkTS 对函数对象的相等性测试可能产生不同结果。

#### 示例

```typescript
function foo() {}

foo == foo   // TypeScript: true
            // ArkTS: 可能为 false

const f1 = foo
const f2 = foo
f1 == f2    // TypeScript: true
            // ArkTS: 可能为 false
```

---

### 14. 方法的函数对象

**状态**：`frontend_status: None`

TypeScript 和 ArkTS 对函数对象的处理不同，`this` 的语义也不同。

#### 示例

```typescript
class A {
  method() { console.log(this) }
}
const a = new A
const method = a.method
method()  // TypeScript: undefined
         // ArkTS: 对象 'a' 的内容

const aa = new A
a.method == aa.method  // TypeScript: true
                      // ArkTS: false
```

**说明**：
- TypeScript 不绑定 `this` 与函数对象
- ArkTS 绑定 `this` 与函数对象
- TypeScript 支持 `this` 为 `undefined`
- ArkTS 中 `this` 总是附加到有效对象

---

### 15. 命名空间差异

**状态**：`frontend_status: Done`

TypeScript 允许在多个不同的命名空间声明中拥有同名的非导出实体，因为这些实体对特定的命名空间声明是局部的。ArkTS 禁止这种情况，因为所有声明合并为一个，声明变得不可区分。

#### 示例

```typescript
// TypeScript: 接受
// ArkTS: 编译时错误
namespace A {
   function foo() { console.log("foo() from 1st A") }
   export function bar() { foo() }
}
namespace A {
   function foo() { console.log("foo() from 2nd A") }
   export function bar_bar() { foo() }
}
```

---

### 16. Math.pow 差异

**状态**：`frontend_status: Done`

TypeScript 的 `Math.pow()` 遵循过时的 IEEE 754-2008 标准（有一些例外）。ArkTS 的 `Math.pow` 遵循最新的 IEEE 754-2019 标准。

#### 差异对照表

| 函数调用 | TypeScript 结果 | ArkTS 结果 |
|---------|---------------|-----------|
| `pow(-1, +Infinity)` | `NaN` | `1` |
| `pow(-1, -Infinity)` | `NaN` | `1` |
| `pow(+1, y)` | `1`（除 `y` 为 `NaN` 或 `Infinity`）<br>`NaN`（`y` 为 `NaN` 或 `Infinity`） | `1`（任何 `y`） |

#### 共同支持的 IEEE 754-2019 新增语句

- `pow(x, +Infinity)` 是 `+0`，当 `-1 < x < 1`
- `pow(x, +Infinity)` 是 `+Infinity`，当 `x < -1` 或 `x > 1`（包括 `+/-Infinity`）
- `pow(x, -Infinity)` 是 `+Infinity`，当 `-1 < x < 1`
- `pow(x, -Infinity)` 是 `+0`，当 `x < -1` 或 `x > 1`（包括 `+/-Infinity`）
- `pow(+Infinity, y)` 是 `+0`，当 `y < 0`
- `pow(+Infinity, y)` 是 `+Infinity`，当 `y > 0`
- `pow(-Infinity, y)` 是 `-0`，当有限 `y < 0` 且为奇整数
- `pow(-Infinity, y)` 是 `-Infinity`，当有限 `y > 0` 且为奇整数
- `pow(-Infinity, y)` 是 `+0`，当有限 `y < 0` 且非奇整数
- `pow(-Infinity, y)` 是 `+Infinity`，当有限 `y > 0` 且非奇整数

---

### 17. 构造函数体差异

#### 调用 super() 的限制

ArkTS 要求派生类中的 `super()` 调用必须是构造函数体的第一条语句。TypeScript 没有此限制。

##### TypeScript 风格（不支持）

```typescript
class Base {
   constructor(p: number) {}
}

let some_condition = true

class Derived extends Base {
   constructor(p: number) {
       if (some_condition) { super(1) }
       else { super(2) }
   }
}
```

##### ArkTS 风格

```typescript
class Base {
   constructor(p: number) {}
}

let some_condition = true

class Derived extends Base {
   constructor(p: number) {
       super(some_condition ? 1 : 2)  // 使用三元表达式
   }
}
```

#### 调用 this() 的限制

TypeScript 不支持多个构造函数。ArkTS 支持，通过调用 `this()`，一个构造函数可以调用同一类的另一个构造函数。

如果使用 `this()`，它必须是次要构造函数体的第一条语句。

##### 示例

```typescript
let flag: boolean = false

class A {
   num: number
   constructor(p: number) {
      this.num = p
   }
   constructor(p: number, s: string) {
      this(flag ? p : -p)
      console.log(this.num, " ", s)
   }
}

new A(1, " for flag false")  // 输出: '-1 for flag false'
flag = true
new A(1, " for flag true")   // 输出: '1 for flag true'
```

---

### 18. 静态字段初始化差异

TypeScript 和 ArkTS 的静态字段初始化顺序不同。

#### 初始化顺序

```typescript
class Base1 {
    static field: number = Base1.init_in_base_1()
    private static init_in_base_1() {
       console.log("Base1 static field initialization")
       return 321
    }
}

class Base2 extends Base1 {
    static override field: number = Base2.init_in_base_2()
    private static init_in_base_2() {
       console.log("Base2 static field initialization")
       return 777
    }
}
console.log(Base1.field, Base2.field)
```

#### 输出差异

**ArkTS 输出**：
```
Base1 static field initialization
321
Base2 static field initialization
777
```

**TypeScript 输出**：
```
Base1 static field initialization
Base2 static field initialization
321
777
```

**说明**：
- TypeScript：按源代码顺序处理，模块加载时初始化所有静态字段
- ArkTS：在编译时或首次使用前初始化静态字段

#### 初始化要求差异

```typescript
class AClass {
    static field: string  // ArkTS: 编译时错误
}
console.log(AClass.field)  // TypeScript: undefined
```

**说明**：TypeScript 允许省略初始化表达式，ArkTS 确保静态字段被初始化。

---

### 19. 重写属性差异

ArkTS 对字段和属性（访问器对）的处理不同。因此，ArkTS 中不允许混合字段和属性，而 TypeScript 的对象模型不同，允许这种混合。

#### 示例

```typescript
class C {
    num: number = 1
}
interface I {
    num: number
}
class D extends C implements I {
    num: number = 2  // ArkTS: 编译时错误，重写冲突
                      // TypeScript: 接受
}
```

---

### 20. 导出一致性

ArkTS 强制导出一致性，即导出声明、公共类或接口成员签名中使用的所有类型也必须导出。TypeScript 允许此类声明。

#### 示例

```typescript
class C {}  // 未导出
export function foo(): C { return new C }  // 导出函数返回非导出类型
// ArkTS: 编译时错误，强制 C 导出
// TypeScript: 接受
```

---

### 21. 类型别名导出状态

ArkTS 强制导出一致性，即在别名情况下，非导出类型保持非导出。TypeScript 允许此类声明。

#### 示例

```typescript
class B {}
export type A = B
// ArkTS: 编译时错误，B 未导出
// TypeScript: 接受
```

---

### 22. 环境常量声明

ArkTS 强制精确的常量类型注解，而不是像 TypeScript 那样从常量值推断类型。

#### 示例

```typescript
declare const a = 1
// ArkTS: 编译时错误，未指定类型
// TypeScript: 接受，假定 a 的类型为 number
```

---

### 23. TypeScript 确定赋值断言

TypeScript 在类和接口中都支持*确定赋值断言*（`!:`）。ArkTS 不使用术语*确定赋值断言*来表示 `!:`，但有类似的概念称为*延迟初始化*。ArkTS 仅在类中允许它。

#### 示例

```typescript
class A {
   f!: number  // ArkTS: OK
}

interface I {
   field!: number  // ArkTS: 编译时错误
}
```

---

### 24. TypeScript 元组 length 属性

TypeScript 中元组具有 `length` 属性，ArkTS 中没有。

#### 示例

```typescript
let tuple: [number, string] = [1, ""]

for (let index = 0; index < tuple.length; index++) {
   let element: Object = tuple[index]
}
// TypeScript: OK
// ArkTS: 编译时错误
```

---

### 25. TypeScript 联合类型的 rest 参数不支持

TypeScript 支持*联合类型*的 *rest 参数*，ArkTS 不支持。

#### 示例

```typescript
type U = Array<number> | Array<string>

function bar(...u: U) {
   console.log(u)
}
bar(1, 2, 3)     // TypeScript: OK
bar("a", "bb", "ccc")  // TypeScript: OK
// ArkTS: 编译时错误 - rest 不能有联合类型
```

---

### 26. 对象字面量属性状态

如果接口只有某个属性的 set 访问器，TypeScript 允许尽管没有定义 getter 也获取该属性的值。这种代码模式在 ArkTS 中导致编译时错误。

#### 示例

```typescript
interface I {
  set attr(attr: number)
}

function foo(i: I) {
  console.log(i.attr)      // ArkTS: 编译时错误
  i.attr = i.attr + 1      // ArkTS: 编译时错误
  console.log(i.attr)      // ArkTS: 编译时错误
}
foo({attr: 123})
```

---

### 27. Record 键的枚举类型不支持

TypeScript 支持以多种格式使用 `enum` 类型作为 record 的键集。ArkTS 不支持 `enum` 类型的 record 键。

#### 示例

```typescript
enum Test { A = 'a', B = 'b' }

let r1: Record<Test, number> = { a: 0, b: 1 }
let r2: Record<Test, number> = { 'a': 0, 'b': 1 }
let r3: Record<Test, number> = { [Test.A]: 0, [Test.B]: 1 }
// TypeScript: 全部 OK
// ArkTS: 全部编译时错误
```

---

### 28. Boolean({}) 不同结果

TypeScript 中 `Boolean({})` 返回 `true`，ArkTS 中返回 `false`。

#### 示例

```typescript
let b = new Boolean({})
console.log(b)  // TypeScript: true
               // ArkTS: false
```

---

### 29. 私有成员和子类

TypeScript 中基类的私有成员名称不能在子类中使用。ArkTS 中，基类的私有成员名称可以在子类中无限制地重用。

#### 示例

```typescript
class Base {
  private foo() {}
  private x: number = 1
}

class Derived extends Base {
  x: number = 10
  foo() { console.log(this.x) }
}
// TypeScript: 错误 "Class 'Derived' incorrectly extends base class 'Base'"
// ArkTS: 编译通过，无错误
```

---

## 完整兼容性清单

### 已实现（Done）

| 差异 | 状态 |
|------|------|
| undefined 不是通用值 | ✅ Done |
| 数值语义差异 | ✅ Done |
| 协变重写禁止 | ✅ Done |
| 函数类型兼容性 | ✅ Done |
| 工具类型兼容性 | ✅ Done |
| 函数重载签名 | ✅ Done |
| void 类型兼容性 | ✅ Done |
| 扩展 Object 类 | ✅ Done |
| extends/implements 子句语法 | ✅ Done |
| 函数对象的唯一性 | ✅ Done |
| 命名空间差异 | ✅ Done |
| Math.pow 差异 | ✅ Done |
| 构造函数体差异 | ✅ Done |
| 导出一致性 | ✅ Done |
| 类型别名导出状态 | ✅ Done |
| 环境常量声明 | ✅ Done |
| 确定赋值断言 | ✅ Done |
| 元组 length 属性 | ✅ Done |
| rest 参数联合类型 | ✅ Done |
| 对象字面量属性状态 | ✅ Done |
| Record enum 键 | ✅ Done |
| Boolean({}) 差异 | ✅ Done |
| 私有成员子类 | ✅ Done |

### 未实现（None）

| 差异 | 状态 |
|------|------|
| 继承时的类字段 | ❌ None |
| 数组赋值 | ❌ None |
| 元组和数组 | ❌ None |
| 方法的函数对象 | ❌ None |
| 静态字段初始化 | ❌ None |
| 重写属性差异 | ❌ None |

---

## 参考资源

- **原始文档**：`D:\arkcompiler\runtime_core\static_core\plugins\ets\doc\cookbook\TS_compatibility.rst`
- **迁移指南**：[cookbook.md](cookbook.md)
- **详细食谱**：[cookbook-recipes.md](cookbook-recipes.md)
