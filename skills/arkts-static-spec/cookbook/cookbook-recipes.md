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

### 优先级 2：代码改进建议（WARNING 级别）

- [ ] 检查字段初始化
- [ ] 审查对象属性访问模式
- [ ] 确保类型安全

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

**完整 144+ 个食谱**，参考原始文档：
`D:\arkcompiler\runtime_core\static_core\plugins\ets\doc\cookbook\recipes.rst`
