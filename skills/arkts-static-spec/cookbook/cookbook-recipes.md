# ArkTS Cookbook - 迁移食谱（Recipes）

## 概述

本文档包含从 TypeScript 迁移到 ArkTS 的详细食谱。每个食谱说明一个需要调整的 TypeScript 特性，并提供正确写法。

**严重性级别**：
- `|CB_ERROR|`：必须遵循，否则编译失败
- `|CB_WARNING|`：强烈建议遵循

---

## 目录

### 语法相关
- [R001: 非标识符属性名](#r001)
- [R002: Symbol() API](#r002)
- [R003: 私有 # 标识符](#r003)
- [R004: 类型和命名空间名称唯一性](#r004)
- [R005: 使用 let 代替 var](#r005)
- [R008: 禁止 any/unknown](#r008)

### 类型系统
- [R014: 调用签名类型](#r014)
- [R015: 构造签名类型](#r015)
- [R068: in 运算符](#r068)
- [R069: 解构赋值](#r069)
- [R074: 解构变量声明](#r074)

### 模块和导入
- [R121: require 导入](#r121)
- [R126: export = 语法](#r126)
- [R128: 环境模块声明](#r128)

### 其他重要限制
- [结构化类型不支持](#结构化类型)
- [动态属性访问限制](#动态属性访问)

### 常见编译错误修复实战
- [R201: 不支持 long 字面量 L 后缀](#r201-不支持-long-字面量-l-后缀)
- [R202: 不支持内联对象类型声明](#r202-不支持内联对象类型声明)
- [R203: 不支持构造函数参数属性](#r203-不支持构造函数参数属性)
- [R204: Promise\<T\> 返回类型中的数值类型转换](#r204-promiset-返回类型中的数值类型转换)
- [R205: 不支持 .toDouble() 转换方法](#r205-不支持-todouble-转换方法)
- [R206: 数组字面量类型推断](#r206-数组字面量类型推断)
- [R207: 不支持嵌套的 Promise 类型](#r207-不支持嵌套的-promise-类型)
- [R208: 不支持交集类型](#r208-不支持交集类型)
- [R209: 不支持声明合并](#r209-不支持声明合并)

---

## 语法相关食谱

### R001: 不支持非标识符属性名

**规则**：`arkts-identifiers-as-prop-names`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持使用数字、字符串或计算值作为属性名。

#### 错误示例

```typescript
// 数字键
var x = {"name": 1, 2: 3}

// 字符串键字典
const colors = {
    "red": "#FF0000",
    "green": "#00FF00"
}

// 动态键
function createConfig(key: string) {
    return {[key]: true}
}
```

#### 正确示例

```typescript
// 使用类声明属性
class X {
    name: number = 1
    two: number = 2
}

// 使用数组存储数字索引数据
let y = [1, 2, 3]
console.log(y[2])

// 使用 Map 存储动态键值对
let z = new Map<Object, number>()
z.set("name", 1)
z.set(2, 2)

// 颜色字典使用类
class Colors {
    red: string = "#FF0000"
    green: string = "#00FF00"
}

// 动态配置使用 Map
function createConfig(key: string) {
    const config = new Map<string, boolean>()
    config.set(key, true)
    return config
}
```

#### 迁移策略

1. **简单对象**：使用类和属性声明
2. **数字索引**：使用数组
3. **动态键**：使用 `Map<Object, T>`
4. **混合情况**：考虑拆分为多个结构

---

### R002: 不支持 Symbol() API

**规则**：`arkts-no-symbol`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持 `Symbol()` API，因为对象布局在编译时确定，不能运行时修改。

**例外**：支持 `Symbol.iterator` 用于可迭代接口。

#### 错误示例

```typescript
const sym = Symbol()
let o = {
   [sym]: "value"
}
```

#### 正确示例

```typescript
class SomeClass {
    someProperty: string = ""
}
let o = new SomeClass()
```

#### 迁移策略

1. **审查代码库**：找到所有 `Symbol()` 使用
2. **区分迭代器和其他用途**：保留迭代器，转换其他
3. **重构模式**：
   - 将 symbol 属性转换为类成员
   - 用注解系统替换元数据 symbol
   - 保留有效的迭代器 symbol

---

### R003: 不支持私有 # 标识符

**规则**：`arkts-no-private-identifiers`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不使用 `#` 开头的私有标识符，使用 `private` 关键字。

#### 错误示例

```typescript
class C {
    #foo: number = 42
}
```

#### 正确示例

```typescript
class C {
    private foo: number = 42
}
```

---

### R004: 类型和命名空间名称必须唯一

**规则**：`arkts-unique-names`

**严重性**：`|CB_ERROR|`

**说明**：所有类型（类、接口、枚举）和命名空间的名称在同一作用域级别必须唯一，且不能与其他名称（变量、函数）重复。

#### 错误示例

```typescript
// 变量与类型冲突
let DataProcessor: string
class DataProcessor {}  // 编译错误

// 命名空间与接口冲突
namespace Utilities {
    export function log() {}
}
interface Utilities {}  // 编译错误
```

#### 正确示例

```typescript
// 使用唯一名称
let dataProcessor: string
class DataHandler {}

// 不同作用域可以重名
namespace Network {
    export function send() {}
}
namespace FileSystem {
    export interface Network {}  // 不同作用域，允许
}
```

---

### R005: 使用 let 代替 var

**规则**：`arkts-no-var`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持 `var`，必须使用 `let`。

**注意**：`var` 和 `let` 的作用域不同，需要调整变量声明位置。

#### 错误示例

```typescript
function f(shouldInitialize: boolean) {
    if (shouldInitialize) {
       var x = 10  // var 函数作用域
    }
    return x  // 可以访问
}

let upper_let = 0
{
    var scoped_var = 0  // 同上层作用域
    let scoped_let = 0  // 块级作用域
}
scoped_var = 5  // 可见
scoped_let = 5  // 编译错误
```

#### 正确示例

```typescript
function f(shouldInitialize: boolean): number | undefined {
    let x: number | undefined = undefined
    if (shouldInitialize) {
        x = 10
    }
    return x
}

let upper_let = 0
let scoped_var = 0
{
    let scoped_let = 0
    upper_let = 5
}
scoped_var = 5
scoped_let = 5  // 编译错误
```

---

### R008: 禁止 any 和 unknown

**规则**：`arkts-no-any-unknown`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持 `any` 和 `unknown`，必须显式指定类型。

**特殊情况**：与标准 TS/JS 互操作时，可使用 `ESObject` 类型（会产生警告）。

#### 错误示例

```typescript
let value1: any
value1 = true
value1 = 42

let value2: unknown
value2 = true
value2 = 42

let something: any = external_function()
console.log(something.someProperty)
```

#### 正确示例

```typescript
let value_b: boolean = true
let value_n: number = 42
let value_o1: Object = true
let value_o2: Object = 42

// 与 JS 互操作（必要时）
let something: ESObject = external_function()
console.log(something.someProperty)
```

#### 迁移策略

1. **定义明确的类型接口**：
```typescript
interface ApiResult {
    code: number
    message: string
    data: Object
}
let result: ApiResult = apiCall()
```

2. **使用联合类型**：
```typescript
// ❌ let value: any
// ✅ let value: string | number | boolean
let value: string | number | boolean = "hello"
```

---

## 类型系统食谱

### R014: 不支持调用签名类型

**规则**：`arkts-no-call-signatures`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持对象类型中的调用签名，使用类代替。

#### 错误示例

```typescript
type DescribableFunction = {
    description: string
    (someArg: number): string  // 调用签名
}

function doSomething(fn: DescribableFunction) {
    console.log(fn.description + " returned " + fn(6))
}
```

#### 正确示例

```typescript
class DescribableFunction {
    description: string
    invoke(someArg: number): string {
        return someArg.toString()
    }
    constructor() {
        this.description = "desc"
    }
}

function doSomething(fn: DescribableFunction) {
    console.log(fn.description + " returned " + fn.invoke(6))
}
```

---

### R015: 不支持构造签名类型

**规则**：`arkts-no-ctor-signatures-type`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持对象类型中的构造签名，使用类代替。

#### 错误示例

```typescript
type Constructable = {
    new (name: string): Object
}

function create(ctor: Constructable, name: string) {
    return new ctor(name)
}
```

#### 正确示例

```typescript
interface Constructable {
    create(name: string): Object
}

function create(ctor: Constructable, name: string) {
    return ctor.create(name)
}
```

---

### R068: 不支持 in 运算符

**规则**：`arkts-no-in-operator`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持 `in` 运算符，因为对象属性在编译时确定。

#### 错误示例

```typescript
class Person {
    name: string = ""
}
let p = new Person()
let b = "name" in p  // true
```

#### 正确示例

```typescript
class Person {
    name: string = ""
}
let p = new Person()
let b = p instanceof Person  // true，且保证 "name" 存在
```

---

### R069: 解构赋值部分支持

**规则**：`arkts-no-destruct-assignment`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 支持数组和元组的解构赋值，但不支持：
- 展开运算符
- 对象解构

#### 错误示例

```typescript
let head, tail
[head, ...tail] = [1, 2, 3, 4]  // 不支持展开

class Point {
    x: number = 0.0
    y: number = 0.0
}
let x: number, y: number
({x, y} = new Point())  // 不支持对象解构
```

#### 正确示例

```typescript
// 数组解构（无展开）
let one: number, two: number
[one, two] = [1, 2]

// 手动提取剩余元素
let data: number[] = [1, 2, 3, 4]
let head = data[0]
let tail: number[] = []
for (let i = 1; i < data.length; ++i) {
    tail.push(data[i])
}

// 手动提取对象属性
class Point {
    x: number = 0.0
    y: number = 0.0
}
let p = new Point()
let x = p.x
let y = p.y
```

---

### R074: 不支持解构变量声明

**规则**：`arkts-no-destruct-decls`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持解构变量声明。

#### 错误示例

```typescript
let [one, two] = [1, 2]

class Point {
    x: number = 0.0
    y: number = 0.0
}
function returnZeroPoint(): Point {
    return new Point()
}
let {x, y} = returnZeroPoint()
```

#### 正确示例

```typescript
// 先声明，再解构赋值
let one: number, two: number
[one, two] = [1, 2]

// 创建中间对象
class Point {
    x: number = 0.0
    y: number = 0.0
}
function returnZeroPoint(): Point {
    return new Point()
}
let zp = returnZeroPoint()
let x = zp.x
let y = zp.y
```

---

## 模块和导入食谱

### R121: 不支持 require 和 import 赋值

**规则**：`arkts-no-require`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持 `require` 和 `import` 赋值，使用标准 `import`。

#### 错误示例

```typescript
import m = require("mod")
```

#### 正确示例

```typescript
import * as m from "mod"
```

---

### R126: 不支持 export = 语法

**规则**：`arkts-no-export-assignment`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持 `export = ...` 语法，使用标准 `export` / `import`。

#### 错误示例

```typescript
// module1
export = Point

class Point {
    constructor(x: number, y: number) {}
    static origin = new Point(0, 0)
}

// module2
import Pt = require("module1")
let p = Pt.origin
```

#### 正确示例

```typescript
// module1
export class Point {
    constructor(x: number, y: number) {}
    static origin = new Point(0, 0)
}

// module2
import * as Pt from "module1"
let p = Pt.origin
```

---

### R128: 不支持环境模块声明

**规则**：`arkts-no-ambient-decls`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持环境模块声明，因为它有自己的 JS 互操作机制。

#### 错误示例

```typescript
declare module "some-module" {
    export function someFunction(): string
}
```

#### 正确示例

```typescript
// 使用 .d.ts 文件或 ArkTS 的互操作机制
// 参考具体平台的互操作文档
```

---

## 其他重要限制

### 结构化类型不支持

ArkTS 当前不支持结构化类型（鸭子类型），仅支持名义类型。

#### TypeScript（结构化类型）

```typescript
class T {
    name: string = ""
}
class U {
    name: string = ""
}
let u: U = new T()  // OK，结构兼容
```

#### ArkTS（名义类型）

```typescript
class T {
    name: string = ""
}
class U {
    name: string = ""
}
let u: U = new T()  // ❌ 编译错误
```

#### 解决方案

```typescript
// 使用接口定义共同契约
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

### 动态属性访问限制

ArkTS 严格限制动态属性访问，以维护类型安全。

#### 错误示例

```typescript
class Point {
    x: number = 0
    y: number = 0
}

let p = new Point()
let propName = "x"
let value = p[propName]  // ❌ 编译错误
```

#### 正确示例

```typescript
class Point {
    x: number = 0
    y: number = 0
}

let p = new Point()
let value = p.x  // ✅ 静态访问
```

#### 替代方案：使用 Map

```typescript
// 如果确实需要动态属性访问
let data = new Map<string, number>()
data.set("x", 0)
data.set("y", 0)
let propName = "x"
let value = data.get(propName)  // ✅ OK
```

---

## 迁移检查清单

### 优先级 1：必须修复（ERROR 级别）

- [ ] 替换所有 `var` 为 `let`
- [ ] 移除所有 `any` / `unknown` 类型
- [ ] 移除 `Symbol()` API 使用
- [ ] 移除私有 `#` 标识符
- [ ] 确保类型和命名空间名称唯一
- [ ] 移除非标识符属性名
- [ ] 移除调用签名和构造签名类型
- [ ] 移除 `in` 运算符
- [ ] 移除对象解构
- [ ] 替换 `require` 为标准 `import`
- [ ] 移除 `export =` 语法
- [ ] 移除 long 字面量的 `L` 后缀（R201）
- [ ] 将内联对象类型改为接口声明（R202）
- [ ] 构造函数参数改为类体字段声明（R203）
- [ ] `Promise<number>` 返回值使用浮点字面量（R204）
- [ ] 避免使用 `.toDouble()` 等不存在的方法（R205）
- [ ] 数组字面量类型与返回类型匹配（R206）
- [ ] 移除嵌套的 `Promise<Promise<T>>` 类型（R207）
- [ ] 将交集类型 `A & B` 改为接口继承（R208）
- [ ] 避免重复声明相同的接口、类、枚举（R209）

### 优先级 2：代码改进建议（WARNING 级别）

- [ ] 检查字段初始化
- [ ] 审查对象属性访问模式
- [ ] 确保类型安全

---

## 常见编译错误修复实战

本节记录从实际 ArkTS 开发中遇到的常见编译错误及其修复方法，帮助开发者快速定位和解决问题。

### R201: 不支持 long 字面量 L 后缀

**规则**：`arkts-no-long-l-suffix`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持在整数字面量后使用 `L` 后缀表示 long 类型。在 ArkTS 中，整数类型会根据值自动推断 `int` 或 `long`，无需后缀。

#### 错误示例

```typescript
// ❌ 编译错误: Syntax error ESY0227: Unexpected token 'L'
let maxLong: long = 9223372036854775807L

// ❌ 编译错误: 数组中的 long 值使用 L 后缀
let longArray: long[] = [1000000L, 2000000L, 3000000L]
```

#### 正确示例

```typescript
// ✅ 直接使用字面量，类型自动推断
let maxLong: long = 9223372036854775807

// ✅ 数组中无需后缀
let longArray: long[] = [1000000, 2000000, 3000000]

// ✅ 需要显式类型时，使用类型注解
let value: long = 123456789
```

#### 类型推断规则

| 字面量范围 | 推断类型 |
|-----------|---------|
| -2³¹ ~ 2³¹-1 | `int` |
| 超出 int 范围 | `long` |

#### 注意事项

- `f` 后缀仍然用于 `float` 类型（如 `3.14f`）
- `n` 后缀用于 `bigint` 类型（如 `123n`）
- 仅 `L` 后缀不支持

---

### R202: 不支持内联对象类型声明

**规则**：`arkts-no-inline-object-types`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持在函数参数或返回值类型中使用内联对象类型（如 `{ name: string, age: number }`）。必须先声明接口，然后在类型注解中使用接口名。

#### 错误示例

```typescript
// ❌ 编译错误: Using object literals to declare types in place is not supported
function processUser(user: { name: string, age?: number }): string {
    return `${user.name} is ${user.age} years old`
}

// ❌ 编译错误: 返回值类型使用内联对象
function getConfig(): { readonly id: number, value: string } {
    return { id: 1, value: "test" }
}

// ❌ 编译错误: Promise 返回值中使用内联类型
async function fetchData(): Promise<{ id: number, name: string, active: boolean }> {
    return { id: 1, name: "item", active: true }
}
```

#### 正确示例

```typescript
// ✅ 先声明接口，然后使用
interface UserType {
    name: string
    age?: number
}

function processUser(user: UserType): string {
    return `${user.name} is ${user.age} years old`
}

// ✅ 配置接口
interface ConfigType {
    readonly id: number
    value: string
}

function getConfig(): ConfigType {
    return { id: 1, value: "test" }
}

// ✅ 数据接口
interface DataType {
    id: number
    name: string
    active: boolean
}

async function fetchData(): Promise<DataType> {
    return { id: 1, name: "item", active: true }
}

// ✅ 嵌套接口
interface NestedDataType {
    value: number
    label: string
}

interface NestedType {
    data: NestedDataType
}

function getNested(): NestedType {
    return {
        data: { value: 42, label: "answer" }
    }
}
```

#### 迁移步骤

1. **识别内联类型**：查找 `{ ... }` 形式的类型声明
2. **创建接口**：为每个内联类型创建命名的 interface
3. **替换引用**：将所有内联类型替换为接口名
4. **验证编译**：确保没有遗漏的内联类型

---

### R203: 不支持构造函数参数属性

**规则**：`arkts-no-param-properties`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持在构造函数参数中声明字段（如 `constructor(public x: number)`）。必须在类体中显式声明字段，然后在构造函数中赋值。

#### 错误示例

```typescript
// ❌ 编译错误: Declaring fields in parameter list is not supported
class Point {
    constructor(public x: number, public y: number) {}
}

// ❌ 编译错误: 混合访问修饰符
class Person {
    constructor(private name: string, public age: number) {}
}

// ❌ 编译错误: 只读参数属性
class Circle {
    constructor(private readonly radius: number) {}
}
```

#### 正确示例

```typescript
// ✅ 显式声明字段 + 构造函数赋值
class Point {
    public x: number = 0
    public y: number = 0

    constructor(x: number, y: number) {
        this.x = x
        this.y = y
    }
}

// ✅ 私有字段 + 公共字段
class Person {
    private name: string = ""
    public age: number = 0

    constructor(name: string, age: number) {
        this.name = name
        this.age = age
    }
}

// ✅ 只读字段
class Circle {
    private radius: number = 0

    constructor(radius: number) {
        this.radius = radius
    }
}

// ✅ 带继承的类
class Circle extends Shape {
    private radius: number = 0

    constructor(radius: number) {
        super()  // 必须先调用 super()
        this.radius = radius
    }

    area(): number {
        return Math.PI * this.radius * this.radius
    }
}
```

#### 迁移对照表

| TypeScript | ArkTS |
|-----------|-------|
| `constructor(public x: number)` | `x: number = 0; constructor(x: number) { this.x = x }` |
| `constructor(private name: string)` | `private name: string = ""; constructor(name: string) { this.name = name }` |
| `constructor(readonly id: number)` | `readonly id: number = 0; constructor(id: number) { this.id = id }` |

---

### R204: Promise<T> 返回类型中的数值类型转换

**规则**：`arkts-promise-number-conversion`

**严重性**：`|CB_ERROR|`

**说明**：当函数返回类型为 `Promise<number>` 时，`number` 是 `double` 的别名。整数字面量 `42` 会被推断为 `int` 类型，在 `Promise<number>` 上下文中需要显式转换为 `double`。使用浮点字面量（如 `42.0`）可以确保类型匹配。

#### 错误示例

```typescript
// ❌ 编译错误: Type 'Int' is not compatible with return type 'Promise<Double>'
async function fetchNumber(): Promise<number> {
    return 42  // int 不能隐式转换为 Promise<double>
}

// ❌ 编译错误: Promise.resolve 中的类型不匹配
async function fetchPromiseOfPromise(): Promise<Promise<number>> {
    return Promise.resolve(42)  // int 不能隐式转换为 double
}

// ❌ 编译错误: 联合类型中的 int 不兼容
async function fetchUnion(): Promise<string | number> {
    return Math.random() > 0.5 ? "hello" : 42  // 42 是 int，不是 double
}
```

#### 正确示例

```typescript
// ✅ 使用浮点字面量确保类型为 double
async function fetchNumber(): Promise<number> {
    return 42.0  // double 类型
}

// ✅ Promise.resolve 使用浮点字面量
async function fetchPromiseOfPromise(): Promise<Promise<number>> {
    return Promise.resolve(42.0)  // double 类型
}

// ✅ 联合类型中使用浮点字面量
async function fetchUnion(): Promise<string | number> {
    return Math.random() > 0.5 ? "hello" : 42.0  // 42.0 是 double
}

// ✅ 异步函数返回数值
async function fetchNumberAsync(): Promise<number> {
    return 42.0
}

// ✅ 箭头函数返回数值
let returnNumberArrow = (): number => 42.0

// ✅ 对比：普通 number 类型的赋值（不需要转换）
function getNumber(): number {
    return 42  // OK：int 是 number 的子类型
}
```

#### 类型转换对比

| 场景 | 代码 | 类型匹配 |
|------|------|---------|
| 直接返回 `number` | `return 42` | ✅ int 是 number 的子类型 |
| 返回 `Promise<number>` | `return 42` | ❌ int 不能隐式转换为 Promise<double> |
| 返回 `Promise<number>` | `return 42.0` | ✅ double 匹配 Promise<double> |
| 普通 `number` 变量赋值 | `let x: number = 42` | ✅ int 是 number 的子类型 |

#### 原因说明

`Promise<number>` 对返回值有更严格的类型检查，要求类型完全匹配，而普通 `number` 类型允许 `int` 作为子类型赋值。

---

### R205: 不支持 .toDouble() 转换方法

**规则**：`arkts-no-to-double`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持 `.toDouble()` 等内置类型转换方法。需要类型转换时，应使用目标类型的字面量或显式类型注解。

#### 错误示例

```typescript
// ❌ 编译错误: Syntax error ESY0227: Unexpected token 'toDouble'
async function fetchNumber(): Promise<number> {
    return 42.toDouble()  // 不支持 .toDouble() 方法
}

// ❌ 编译错误: 数组元素上使用 .toDouble()
async function fetchArray(): Promise<number[]> {
    return [1.toDouble(), 2.toDouble(), 3.toDouble()]
}

// ❌ 编译错误: 表达式上使用 .toDouble()
async function fetchUnion(): Promise<string | number> {
    return Math.random() > 0.5 ? "hello" : 42.toDouble()
}
```

#### 正确示例

```typescript
// ✅ 使用浮点字面量
async function fetchNumber(): Promise<number> {
    return 42.0  // 直接使用浮点字面量
}

// ✅ 数组使用浮点字面量
async function fetchArray(): Promise<number[]> {
    return [1.0, 2.0, 3.0]
}

// ✅ 联合类型使用浮点字面量
async function fetchUnion(): Promise<string | number> {
    return Math.random() > 0.5 ? "hello" : 42.0
}

// ✅ 使用变量时，在声明时使用浮点字面量
let value: number = 42.0
async function returnStored(): Promise<number> {
    return value  // OK：value 已是 double 类型
}

// ✅ 对比：有效的类型转换使用 toInt() 等标准库方法
let d: double = 3.14
let i: int = d.toInt()  // ✅ toInt() 是标准库方法，可用
```

#### 不支持的方法

| 方法 | 说明 | 替代方案 |
|------|------|---------|
| `.toDouble()` | 转换为 double | 使用浮点字面量 `42.0` |
| `.toFloat()` | 转换为 float | 使用浮点字面量 `3.14f` |
| `.toLong()` | 转换为 long | 无简单替代，使用类型注解 |

#### 支持的标准库转换方法

```typescript
// ✅ 这些方法来自标准库，是可用的
let d: double = 3.99
let i: int = d.toInt()      // 结果：3（向零取整）
let b: byte = d.toByte()    // 结果：3
let s: short = d.toShort()  // 结果：3
let l: long = d.toLong()    // 结果：3
```

---

### R206: 数组字面量类型推断

**规则**：`arkts-array-literal-inference`

**严重性**：`|CB_ERROR|`

**说明**：数组字面量的类型推断基于元素的类型。`[1, 2, 3]` 被推断为 `int[]`，而 `Promise<number[]>` 需要 `Array<double>`。使用浮点字面量可以确保数组被推断为 `number[]`。

#### 错误示例

```typescript
// ❌ 编译错误: Type 'Array<Int>' is not compatible with return type 'Promise<Array<Double>>'
async function fetchArray(): Promise<number[]> {
    return [1, 2, 3]  // 推断为 int[]，但需要 double[]
}

// ❌ 编译错误: 相同问题
async function fetchArrayAsync(): Promise<number[]> {
    return [1, 2, 3]
}
```

#### 正确示例

```typescript
// ✅ 使用浮点字面量确保推断为 number[]
async function fetchArray(): Promise<number[]> {
    return [1.0, 2.0, 3.0]  // 推断为 double[] = number[]
}

// ✅ 混合数值类型
async function fetchMixed(): Promise<number[]> {
    return [1.0, 2.5, 3.0]  // 都是 double 类型
}

// ✅ 对比：显式 int 类型的函数
function getIntArray(): int[] {
    return [1000, 2000, 3000]  // ✅ OK：推断为 int[]，匹配返回类型
}

// ✅ 对比：显式 float 类型的函数
function getFloatArray(): float[] {
    return [1.0f, 2.0f, 3.0f]  // ✅ OK：使用 f 后缀
}

// ✅ 对比：显式 double 类型的函数
function getDoubleArray(): double[] {
    return [1.1, 2.2, 3.3]  // ✅ OK：浮点字面量推断为 double[]
}
```

#### 数组字面量类型推断规则

| 字面量 | 推断类型 | 匹配返回类型 |
|--------|---------|-------------|
| `[1, 2, 3]` | `int[]` | ✅ `Promise<int[]>` / `int[]` |
| `[1.0, 2.0, 3.0]` | `double[]` (即 `number[]`) | ✅ `Promise<number[]>` / `number[]` |
| `[1.0f, 2.0f, 3.0f]` | `float[]` | ✅ `Promise<float[]>` / `float[]` |
| `[1.1, 2.2, 3.3]` | `double[]` (即 `number[]`) | ✅ `Promise<number[]>` / `number[]` |

#### 关键区别

```typescript
// number 是 double 的别名
// Promise<number[]> 等价于 Promise<double[]>

// ✅ 这些是等效的
let a: number[] = [1.0, 2.0, 3.0]
let b: double[] = [1.0, 2.0, 3.0]

// ❌ 这些类型不兼容
let c: number[] = [1, 2, 3]      // int[] 不能赋值给 double[]
let d: int[] = [1.0, 2.0, 3.0]    // double[] 不能赋值给 int[]
```

---

### R207: 不支持嵌套的 Promise 类型

**规则**：`arkts-no-nested-promise`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS async 函数的返回类型必须是 `Promise<T>` 的形式，不支持嵌套的 `Promise<Promise<T>>` 类型。与 TypeScript 不同，ArkTS 不会自动解包嵌套的 Promise 类型。

#### 错误示例

```typescript
// ❌ 编译错误: Return type of async function must be 'Promise'
async function fetchPromiseOfPromise(): Promise<Promise<number>> {
    return Promise.resolve(42.0)
}

// ❌ 编译错误: 嵌套 Promise 作为泛型参数
async function fetchNested(): Promise<Promise<string>> {
    return Promise.resolve("hello")
}
```

#### 正确示例

```typescript
// ✅ 使用标准的 Promise<T> 返回类型
async function fetchNumber(): Promise<number> {
    return 42.0
}

// ✅ Promise.resolve 返回 Promise<T>
async function fetchResolved(): Promise<number> {
    return Promise.resolve(42.0)
}

// ✅ 直接返回值，async 自动包装为 Promise
async function fetchDirect(): Promise<string> {
    return "hello"
}

// ✅ 对比：在 TypeScript 中，Promise<Promise<T>> 会被自动解包为 Promise<T>
// 但在 ArkTS 中必须显式使用 Promise<T>
```

#### ArkTS vs TypeScript

| 特性 | TypeScript | ArkTS |
|------|-----------|-------|
| 嵌套 Promise 类型 | 允许，自动解包 | 不允许，编译错误 |
| `Promise<Promise<T>>` | 等价于 `Promise<T>` | ❌ 语法错误 |
| async 返回类型推断 | 自动解包 | 必须是 `Promise<T>` |

#### TypeScript 行为（仅供参考）

```typescript
// TypeScript：以下两种写法是等效的
async function tsStyle1(): Promise<Promise<number>> {
    return Promise.resolve(42)
}

async function tsStyle2(): Promise<number> {
    return Promise.resolve(42)
}

// TypeScript 会自动将 Promise<Promise<T>> 解包为 Promise<T>
```

#### ArkTS 要求

```typescript
// ArkTS：必须使用 Promise<T> 形式
async function arktsStyle(): Promise<number> {
    return 42.0  // ✅ 正确
}
```

#### 迁移指南

1. **查找嵌套 Promise**：搜索 `Promise<Promise<`
2. **移除内层 Promise**：将 `Promise<Promise<T>>` 改为 `Promise<T>`
3. **验证类型**：确保返回值与 Promise 的泛型参数匹配

---

### R208: 不支持交集类型

**规则**：`arkts-no-intersection-types`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持交集类型（Intersection Types）语法 `A & B`。需要创建新的接口来继承多个接口，然后使用这个新接口作为类型注解或泛型约束。

#### 错误示例

```typescript
// ❌ 编译错误: Intersection types are not supported, use inheritance instead!
interface Named {
    name: string
}
interface Aged {
    age: number
}

// 交集类型作为返回类型
function getPerson(): Named & Aged {
    return { name: "Alice", age: 30 }
}

// ❌ 多重交集类型
interface Person {
    name: string
}
interface Employable {
    job: string
}
interface Addressable {
    city: string
}

function getEmployee(): Person & Employable & Addressable {
    return {
        name: "Bob",
        job: "developer",
        city: "Beijing"
    }
}

// ❌ 交集类型作为泛型约束
interface A { methodA(): void }
interface B { methodB(): void }

function combine<T extends A & B>(obj: T): void {
    obj.methodA()
    obj.methodB()
}
```

#### 正确示例

```typescript
// ✅ 使用继承创建组合接口
interface Named {
    name: string
}
interface Aged {
    age: number
}

// 创建继承多个接口的新接口
interface NamedAged extends Named, Aged {}

function getPerson(): NamedAged {
    return { name: "Alice", age: 30 }
}

// ✅ 多重接口继承
interface Person {
    name: string
}
interface Employable {
    job: string
}
interface Addressable {
    city: string
}

// 创建继承多个接口的新接口
interface Employee extends Person, Employable, Addressable {}

function getEmployee(): Employee {
    return {
        name: "Bob",
        job: "developer",
        city: "Beijing"
    }
}

// ✅ 泛型约束使用继承
interface A { methodA(): void }
interface B { methodB(): void }

// 创建继承多个接口的新接口作为约束
interface AB extends A, B {}

function combine<T extends AB>(obj: T): void {
    obj.methodA()
    obj.methodB()
}

// ✅ 带类型参数的泛型函数
interface NamedInterface {
    name: string
}
interface AgedInterface {
    age: number
}

// 创建组合接口
interface NamedAgedInterface extends NamedInterface, AgedInterface {}

function describe<T extends NamedAgedInterface>(person: T): string {
    return `${person.name} is ${person.age} years old`
}
```

#### 迁移对照表

| TypeScript | ArkTS |
|-----------|-------|
| `function foo(): A & B` | `interface AB extends A, B {}; function foo(): AB` |
| `function foo(): A & B & C` | `interface ABC extends A, B, C {}; function foo(): ABC` |
| `function foo<T extends A & B>()` | `interface AB extends A, B {}; function foo<T extends AB>()` |

#### ArkTS vs TypeScript

| 特性 | TypeScript | ArkTS |
|------|-----------|-------|
| 交集类型 `A & B` | 支持 | ❌ 不支持 |
| 多重交集 `A & B & C` | 支持 | ❌ 不支持 |
| 泛型约束中使用交集 | 支持 | ❌ 不支持 |
| 接口继承 `extends A, B` | 支持 | ✅ 支持 |
| 类继承多接口 | `implements A, B` | `implements A, B` |

#### 注意事项

1. **接口继承 vs 类继承**：
   - 接口可以继承多个接口：`interface C extends A, B {}`
   - 类只能继承一个类，但可以实现多个接口：`class D extends E implements A, B {}`

2. **组合接口命名**：
   - 建议使用描述性命名：`NamedAged` 比 `Person` 更明确
   - 对于临时组合类型，使用 `AB`、`ABC` 等简洁命名

3. **泛型约束中的继承**：
   - 必须先声明组合接口，再在泛型中使用
   - 不能在泛型参数列表中直接使用继承语法

#### 迁移步骤

1. **识别交集类型**：搜索 ` & ` 模式（注意前后有空格）
2. **创建组合接口**：对每个交集类型创建继承接口
3. **替换类型引用**：将 `A & B` 替换为组合接口名称
4. **验证实现**：确保返回值或参数符合新接口的要求

#### TypeScript 中的交集类型（仅供参考）

```typescript
// TypeScript：交集类型可以用于类型别名
type Person = Named & Aged
let p: Person = { name: "Alice", age: 30 }

// TypeScript：可以在函数签名中直接使用交集类型
function greet(person: Named & Aged): string {
    return `Hello ${person.name}, you are ${person.age} years old`
}
```

#### ArkTS 要求

```typescript
// ArkTS：必须使用接口继承
interface Person extends Named, Aged {}
let p: Person = { name: "Alice", age: 30 }

// ArkTS：返回类型必须使用已声明的接口
function greet(person: Person): string {
    return `Hello ${person.name}, you are ${person.age} years old`
}
```

---

### R209: 不支持声明合并

**规则**：`arkts-no-declaration-merging`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持声明合并（Declaration Merging）。在 TypeScript 中，同一个接口或类可以多次声明，它们会自动合并为一个定义。但在 ArkTS 中，每个接口、类和枚举只能声明一次。

#### 错误示例

```typescript
// ❌ 编译错误: Merging declarations is not supported
// 第一次声明
interface PersonInterface {
    name: string
    age: number
}

// 第二次声明 - TypeScript 会自动合并，ArkTS 不支持
interface PersonInterface {
    name: string  // 重复声明
}

// ❌ 类的重复声明
class MyUtil {
    static methodA(): void {}
}

class MyUtil {  // 重复声明
    static methodB(): void {}
}

// ❌ 枚举的重复声明
enum Color {
    Red,
    Green
}

enum Color {  // 重复声明
    Blue
}
```

#### 正确示例

```typescript
// ✅ 接口只声明一次，包含所有成员
interface PersonInterface {
    name: string
    age: number
    email?: string  // 所有属性在一个声明中
}

// ✅ 如果需要不同的接口，使用不同的名称
interface PersonBasic {
    name: string
    age: number
}

interface PersonContact extends PersonBasic {
    email: string
    phone?: string
}

// ✅ 类只声明一次，包含所有成员
class MyUtil {
    static methodA(): void {
        console.log("methodA")
    }
    static methodB(): void {
        console.log("methodB")
    }
}

// ✅ 枚举只声明一次，包含所有值
enum Color {
    Red = 1,
    Green = 2,
    Blue = 3
}
```

#### 常见场景：不同上下文中的相同接口名

##### 场景 1：测试不同属性组合

**错误做法**：
```typescript
// ❌ 相同接口名重复声明
interface PersonInterface {
    name: string
    age: number
}

function getPerson(): PersonInterface {
    return { name: "Alice", age: 30 }
}

// 重复声明用于不同测试
interface PersonInterface {
    name: string
}

function getEmployee(): PersonInterface {
    return { name: "Bob" }
}
```

**正确做法**：
```typescript
// ✅ 使用不同的接口名
interface PersonWithAge {
    name: string
    age: number
}

function getPerson(): PersonWithAge {
    return { name: "Alice", age: 30 }
}

interface PersonBasic {
    name: string
}

function getEmployee(): PersonBasic {
    return { name: "Bob" }
}
```

##### 场景 2：模块化添加功能

**TypeScript 做法**（不支持）：
```typescript
// TypeScript：声明合并添加功能
interface String {
    toTitleCase(): string
}

String.prototype.toTitleCase = function(): string {
    return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase()
}
```

**ArkTS 做法**：
```typescript
// ✅ 创建工具类而不是扩展原型
class StringUtil {
    static toTitleCase(str: string): string {
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
    }
}

// 使用
let title: string = StringUtil.toTitleCase("hello world")
```

#### ArkTS vs TypeScript

| 特性 | TypeScript | ArkTS |
|------|-----------|-------|
| 接口多次声明（合并） | 支持 | ❌ 不支持 |
| 类多次声明 | 不支持 | ❌ 不支持 |
| 枚举多次声明（合并） | 支持 | ❌ 不支持 |
| 命名空间合并 | 支持 | ❌ 不支持 |
| 扩展全局类型（如 `String`） | 支持 | ❌ 不支持 |

#### TypeScript 声明合并示例（仅供参考）

```typescript
// TypeScript：多次声明会自动合并
interface Box {
    height: number
    width: number
}

interface Box {
    depth: number  // 合并到上面的 Box
}

// 等价于：
interface Box {
    height: number
    width: number
    depth: number
}

// TypeScript：函数重载
function greet(name: string): string
function greet(name: string, age: number): string
function greet(name: string, age?: number): string {
    if (age !== undefined) {
        return `Hello ${name}, you are ${age} years old`
    }
    return `Hello ${name}`
}
```

#### ArkTS 要求

```typescript
// ✅ ArkTS：所有声明必须紧凑
interface Box {
    height: number
    width: number
    depth: number
}

// ✅ ArkTS：函数重载使用显式语法
function greet(name: string): string {
    return `Hello ${name}`
}

function greetAge(name: string, age: number): string {
    return `Hello ${name}, you are ${age} years old`
}
```

#### 迁移步骤

1. **识别重复声明**：搜索相同名称的接口、类或枚举
2. **分析用途**：确定是否应该合并为一个声明，或使用不同名称
3. **重构方案**：
   - 如果表示同一概念：合并到一个声明中
   - 如果表示不同概念：使用不同的命名
4. **验证所有引用**：更新所有使用旧名称的地方

#### 注意事项

1. **接口命名策略**：
   - 使用描述性后缀区分变体：`PersonBasic`、`PersonExtended`
   - 使用继承建立关系：`PersonContact extends PersonBasic`
   - 避免在全局作用域使用通用名称如 `Data`、`Item`

2. **模块组织**：
   - 将相关接口放在同一文件中
   - 使用导出/导入明确边界
   - 避免隐式全局命名空间

3. **全局扩展**：
    - TypeScript 中的 `interface String { ... }` 扩展在 ArkTS 中不可用
    - 创建工具类或工具函数替代
    - 使用继承创建自定义类型

---

### R210: 不支持函数返回类型中的泛型箭头函数

**规则**：`arkts-no-generic-arrow-return-type`

**严重性**：`|CB_ERROR|`

**说明**：ArkTS 不支持在函数或方法的返回类型中使用泛型箭头函数（Generic Arrow Function）。TypeScript 允可以通过 `(): <T>(...) => T` 语法声明泛型函数类型，但 ArkTS 会将其编译错误。

#### 错误示例

```typescript
// ❌ 编译错误: Semantic error ESE0017: Only abstract or native methods can't have body.
// 函数返回类型中使用泛型箭头函数
function getMapper(): <T, U>(items: T[], fn: (item: T) => U) => U[] {
    return <T, U>(items: T[], fn: (item: T) => U): U[] => items.map(fn)
}

// ❌ 方法返回类型中使用箭头函数类型
class Counter {
    private count: number = 0

    increment(): () => void {
        return (): void => {
            this.count++
            console.log(this.count)
        }
    }
}

// ❌ 泛型箭头函数作为返回类型
function getProcessor(): <T>(value: T) => T {
    return <T>(value: T): T => value
}
```

#### 正确示例

```typescript
// ✅ 使用类型别名定义泛型函数类型
type MapperFunc<T, U> = (items: T[], fn: (item: T) => U) => U[]

function getMapper(): MapperFunc<number, string> {
    return (items: number[], fn: (item: number) => string): string[] => items.map(fn)
}

// ✅ 使用类型别名定义回调类型
type Callback = () => void

class Counter {
    private count: number = 0

    increment(): Callback {
        return (): void => {
            this.count++
            console.log(this.count)
        }
    }
}

// ✅ 使用类型别名定义泛型处理器
type Processor<T> = (value: T) => T

function getProcessor(): Processor<number> {
    return (value: number): number => value
}
```

#### 对比：变量声明 vs 函数返回类型

**变量声明 - 支持**：
```typescript
// ✅ 这些是正确的：变量赋值中使用泛型箭头函数
let identityArrow = <T>(value: T): T => value
let firstArrow = <T>(items: T[]): T => items[0]
let pairArrow = <T, U>(first: T, second: U): [T, U] => [first, second]
```

**函数返回类型 - 不支持**：
```typescript
// ❌ 这些是错误的：函数返回类型中使用泛型箭头函数
function getIdentity(): <T>(value: T) => T {
    return <T>(value: T): T => value
}

function getFirst(): <T>(items: T[]): T {
    return <T>(items: T[]): T => items[0]
}
```

#### ArkTS vs TypeScript

| 特性 | TypeScript | ArkTS |
|------|-----------|-------|
| 变量赋值中的泛型箭头函数 | 支持 | ✅ 支持 |
| 函数返回类型中的泛型箭头函数 | 支持 | ❌ 不支持 |
| 方法返回类型中的箭头函数 | 支持 | ❌ 不支持 |
| 类型别名中的泛型箭头函数 | 支持 | ✅ 支持 |

#### TypeScript 示例（仅供参考）

```typescript
// TypeScript：函数返回类型中使用泛型箭头函数
function getMapper(): <T, U>(items: T[], fn: (item: T) => U) => U[] {
    return (items, fn) => items.map(fn)
}

// 使用
const mapper = getMapper()
const result = mapper([1, 2, 3], (x) => x.toString())  // ["1", "2", "3"]
```

#### ArkTS 要求

```typescript
// ✅ ArkTS：必须使用类型别名
type MapperFunc<T, U> = (items: T[], fn: (item: T) => U) => U[]

function getMapper(): MapperFunc<number, string> {
    return (items, fn) => items.map(fn)
}

// 使用
const mapper = getMapper()
const result = mapper([1, 2, 3], (x: number): string => x.toString())  // ["1", "2", "3"]
```

#### 迁移步骤

1. **识别问题代码**：搜索 `function ...(): <T>(...) =>` 模式
2. **创建类型别名**：为每个泛型箭头函数类型创建类型别名
3. **替换返回类型**：将泛型箭头函数替换为类型别名
4. **指定具体类型参数**：在函数返回类型中指定具体的类型参数

#### 迁移对照表

| TypeScript | ArkTS |
|-----------|-------|
| `function foo(): <T>(x: T) => T` | `type Foo<T> = (x: T) => T; function foo(): Foo<number>` |
| `method(): () => void` | `type Callback = () => void; method(): Callback` |
| `function get(): <T, U>(x: T) => U` | `type Func<T, U> = (x: T) => U; function get(): Func<number, string>` |

#### 注意事项

1. **类型参数范围**：
   - 在类型别名中定义的类型参数在类型内部有效
   - 函数返回类型中需要指定具体的类型参数

2. **变量声明仍然可用**：
   - 变量赋值中继续使用泛型箭头函数
   - 只有函数/方法返回类型需要使用类型别名

3. **类型别名命名**：
   - 使用描述性名称：`MapperFunc`、`Callback`、`Processor`
   - 避免过于通用的名称：`Func`、`Type`

---

### 编译错误快速修复索引

| 编译错误 | 关键词 | 解决方案 | 食谱编号 |
|---------|--------|---------|---------|
| `Unexpected token 'L'` | `L`, long 后缀 | 移除 L 后缀 | R201 |
| `object literals to declare types` | `{}`, 内联类型 | 声明接口 | R202 |
| `Declaring fields in parameter` | `constructor(public x)` | 显式声明字段 | R203 |
| `Type 'Int' is not compatible with 'Promise<Double>'` | `Promise<number>`, 返回值 | 使用浮点字面量 | R204 |
| `Unexpected token 'toDouble'` | `.toDouble()` | 使用浮点字面量 | R205 |
| `Type 'Array<Int>' is not compatible` | 数组, `Promise<number[]>` | 使用浮点字面量数组 | R206 |
| `Return type of async function must be 'Promise'` | `Promise<Promise<T>>` | 使用 `Promise<T>` | R207 |
| `Intersection types are not supported` | ` & `, `A & B` | 使用接口继承 | R208 |
| `Merging declarations is not supported` | 重复声明 | 使用不同名称或合并 | R209 |
| `Only abstract or native methods can't have body` | `(): <T>`, 返回类型 | 使用类型别名 | R210 |

---

## 完整食谱索引

| 编号 | 主题 | 规则名 |
|------|------|--------|
| R001 | 非标识符属性名 | `arkts-identifiers-as-prop-names` |
| R002 | Symbol() API | `arkts-no-symbol` |
| R003 | 私有 # 标识符 | `arkts-no-private-identifiers` |
| R004 | 名称唯一性 | `arkts-unique-names` |
| R005 | 使用 let 代替 var | `arkts-no-var` |
| R008 | 禁止 any/unknown | `arkts-no-any-unknown` |
| R014 | 调用签名类型 | `arkts-no-call-signatures` |
| R015 | 构造签名类型 | `arkts-no-ctor-signatures-type` |
| R068 | in 运算符 | `arkts-no-in-operator` |
| R069 | 解构赋值 | `arkts-no-destruct-assignment` |
| R074 | 解构变量声明 | `arkts-no-destruct-decls` |
| R121 | require 导入 | `arkts-no-require` |
| R126 | export = 语法 | `arkts-no-export-assignment` |
| R128 | 环境模块声明 | `arkts-no-ambient-decls` |

### 常见编译错误修复实战（从实际开发中总结）

| R201 | long 字面量 L 后缀 | `arkts-no-long-l-suffix` |
| R202 | 内联对象类型声明 | `arkts-no-inline-object-types` |
| R203 | 构造函数参数属性 | `arkts-no-param-properties` |
| R204 | Promise<number> 类型转换 | `arkts-promise-number-conversion` |
| R205 | .toDouble() 转换方法 | `arkts-no-to-double` |
| R206 | 数组字面量类型推断 | `arkts-array-literal-inference` |
| R207 | 嵌套的 Promise 类型 | `arkts-no-nested-promise` |
| R208 | 交集类型 | `arkts-no-intersection-types` |
| R209 | 声明合并 | `arkts-no-declaration-merging` |
 R210 | 函数返回类型中的泛型箭头函数 | `arkts-no-generic-arrow-return-type` |
| R211 | 类实现同名接口 | `arkts-no-same-interface-implementation` |

**完整 144+ 个食谱**，参考原始文档：
`D:\arkcompiler\runtime_core\static_core\plugins\ets\doc\cookbook\recipes.rst`
