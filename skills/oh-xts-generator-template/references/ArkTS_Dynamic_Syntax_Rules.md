# ArkTS（鸿蒙开发语言）动态语法检查规则全集

> 基于华为官方文档整理，更新时间：2026-01-26

---

## 📋 目录
1. [类型系统限制](#类型系统限制)
2. [对象和属性限制](#对象和属性限制)
3. [运算符限制](#运算符限制)
4. [函数限制](#函数限制)
5. [控制流限制](#控制流限制)
6. [类和接口限制](#类和接口限制)
7. [模块和导入限制](#模块和导入限制)
8. [标准库限制](#标准库限制)
9. [编程规范](#编程规范)

---

## 🔴 类型系统限制

### 1. 禁用 any 和 unknown 类型
- **规则**: `arkts-no-any-unknown`
- **级别**: 错误
- **错误码**: 10605008
- ❌ 不支持 `any` 类型
- ❌ 不支持 `unknown` 类型
- ✅ 必须使用具体类型或 `Object`

**示例:**
```typescript
// ❌ 不支持
let value1: any;
let value2: unknown;

// ✅ 支持
let value_b: boolean = true;
let value_n: number = 42;
let value_o: Object = true;
```

### 2. 不支持 structural typing（结构化类型）
- **规则**: `arkts-no-structural-typing`
- **级别**: 错误
- **错误码**: 10605030
- ❌ 不同类即使属性相同也不能互相赋值
- ✅ 使用继承或接口实现类型兼容

### 3. 不支持条件类型
- **规则**: `arkts-no-conditional-types`
- **级别**: 错误
- **错误码**: 10605022
- ❌ `type X<T> = T extends number ? T : never`
- ❌ 不支持 `infer` 关键字
- ✅ 使用显式类型约束或使用Object

### 4. 不支持映射类型
- **规则**: `arkts-no-mapped-types`
- **级别**: 错误
- **错误码**: 10605083
- ❌ `type OptionsFlags<Type> = { [Property in keyof Type]: boolean }`
- ✅ 手动定义新的类

### 5. 不支持索引访问类型
- **规则**: `arkts-no-aliases-by-index`
- **级别**: 错误
- **错误码**: 10605028
- ❌ `type T = SomeType[key]`
- ✅ 使用明确的类型定义

### 6. 不支持 this 类型
- **规则**: `arkts-no-typing-with-this`
- **级别**: 错误
- **错误码**: 10605021
- ❌ `function foo(): this`
- ✅ 使用具体的类名

### 7. typeof 只能用于表达式
- **规则**: `arkts-no-type-query`
- **级别**: 错误
- **错误码**: 10605060
- ❌ `let x: typeof y`
- ✅ `let x: number`（使用具体类型）

### 8. 不支持 intersection type（交叉类型）
- **规则**: `arkts-no-intersection-types`
- **级别**: 错误
- **错误码**: 10605019
- ❌ `type Employee = Identity & Contact`
- ✅ 使用继承 `interface Employee extends Identity, Contact {}`

---

## 🔴 对象和属性限制

### 1. 对象布局固定（运行时不可变更）
- ❌ 运行时不能添加新属性
- ❌ 运行时不能删除属性
- ❌ 不能将任意类型的值赋值给对象属性

### 2. 不支持通过索引访问字段
- **规则**: `arkts-no-props-by-index`
- **级别**: 错误
- **错误码**: 10605029
- ❌ `obj['propertyName']`
- ❌ 使用变量作为属性名 `obj[key]`
- ✅ `obj.propertyName`（只能用点操作符）
- ✅ 支持通过索引访问TypedArray（例如Int32Array）

### 3. 属性名必须是合法的标识符
- **规则**: `arkts-identifiers-as-prop-names`
- **级别**: 错误
- **错误码**: 10605001
- ❌ 数字属性名 `{ 1: 'value' }`
- ❌ 字符串属性名 `{ 'name': 'value' }`
- ✅ 使用字符串字面量或枚举值（仅限Record类型）
- ✅ 数组使用索引访问

### 4. 不支持 Symbol() API
- **规则**: `arkts-no-symbol`
- **级别**: 错误
- **错误码**: 10605002
- ❌ `Symbol()`
- ✅ 仅支持 `Symbol.iterator`

### 5. 不支持 # 私有字段
- **规则**: `arkts-no-private-identifiers`
- **级别**: 错误
- **错误码**: 10605003
- ❌ `class C { #field: number }`
- ✅ `class C { private field: number }`

### 6. 不支持 delete 运算符
- **规则**: `arkts-no-delete`
- **级别**: 错误
- **错误码**: 10605059
- ❌ `delete obj.property`
- ✅ 使用可空类型 `property: Type | null`

### 7. 不支持 in 运算符
- **规则**: `arkts-no-in`
- **级别**: 错误
- **错误码**: 10605066
- ❌ `'prop' in obj`
- ✅ `obj instanceof ClassName`

### 8. 对象字面量必须显式标注类型
- **规则**: `arkts-no-untyped-obj-literals`
- **级别**: 错误
- **错误码**: 10605038
- **说明**: 对象字面量必须对应一个显式声明的类或接口，不允许直接使用无类型注解的对象字面量

**规则详解：**

在 ArkTS 中，所有对象字面量必须明确指定其类型，类型推断仅限于有限场景。这确保了类型安全，避免了运行时类型错误。

#### ❌ 不支持的用法（无类型注解的对象字面量）

```typescript
// 1. 直接使用对象字面量，无法推断类型
let o = { x: 1, y: 2 };  // ❌ 错误

// 2. 数组中的无类型对象字面量
let a = [{ n: 1 }, { n: 2 }];  // ❌ 错误

// 3. 函数参数中的对象字面量类型
function foo(obj: { x: number, y: number }) { }  // ❌ 错误

// 4. 返回类型中的对象字面量
function bar(): { x: number, y: number } {  // ❌ 错误
  return { x: 1, y: 2 };
}

// 5. 解构赋值中的对象字面量
const { x, y } = { x: 1, y: 2 };  // ❌ 错误
```

#### ✅ 支持的用法（显式类型声明）

```typescript
// 1. 先定义接口，然后使用对象字面量
interface Point {
  x: number;
  y: number;
}

let o: Point = { x: 1, y: 2 };  // ✅ 正确

// 2. 数组元素使用显式类型
let points: Point[] = [
  { x: 1, y: 2 },
  { x: 3, y: 4 }
];  // ✅ 正确

// 3. 使用类型断言（符合 ArkTS 规范）
const o1 = {} as Point;  // ✅ 正确
o1.x = 1;
o1.y = 2;

// 4. 使用空对象+属性赋值（推荐用于复杂对象）
const o2: Point = {} as Point;  // ✅ 正确
o2.x = 1;
o2.y = 2;

// 5. 嵌套对象类型
interface Rectangle {
  position: Point;
  size: Point;
}

const rect: Rectangle = {
  position: { x: 0, y: 0 },
  size: { x: 100, y: 100 }
};  // ✅ 正确（嵌套对象也会被推断）

// 6. 可选属性必须在接口中声明
interface Config {
  required: string;
  optional?: number;
}

const config: Config = { required: 'value' };  // ✅ 正确
```

#### 特殊场景说明

**对象字面量作为函数参数：**
```typescript
// ❌ 错误：对象字面量直接作为参数类型
function processData(data: { id: number; value: string }) { }

// ✅ 正确：先定义接口
interface ProcessData {
  id: number;
  value: string;
}

function processData(data: ProcessData) { }
```

**对象字面量作为返回值：**
```typescript
// ❌ 错误：对象字面量作为返回类型
function getResult(): { success: boolean; code: number } {
  return { success: true, code: 200 };
}

// ✅ 正确：先定义接口
interface Result {
  success: boolean;
  code: number;
}

function getResult(): Result {
  return { success: true, code: 200 };
}
```

**不支持的上下文（必须显式声明类型）：**
- 初始化具有 `any`、`Object` 或 `object` 类型的任何对象
- 初始化带有方法的类或接口
- 初始化包含自定义含参数的构造函数的类
- 初始化带 `readonly` 字段的类
- 初始化具有私有字段的类
- 函数参数中的对象字面量类型（必须使用预定义接口）
- 返回类型中的对象字面量类型（必须使用预定义接口）

#### 类型推断的例外情况

ArkTS 仅在以下有限场景中支持类型推断：

```typescript
// 1. 空对象类型（但需要后续赋值才能使用）
const empty = {};  // ❌ 错误：无法推断空对象的类型

// 2. 字面量类型用于变量声明
// ❌ 错误：对象字面量不能作为类型
type MyType = { a: string };  // ❌ 错误：应使用 interface
```

#### 最佳实践建议

1. **始终先定义接口或类**，再创建对象实例
2. **使用类型断言**（`{} as TypeName`）进行快速开发
3. **避免在接口中直接使用对象字面量作为类型定义**
4. **为嵌套对象也定义完整的接口类型**
5. **使用可选属性**（`?`）来表示可能不存在的属性

**完整的对象创建模式：**
```typescript
// 推荐模式：空对象+属性赋值
interface User {
  id: number;
  name: string;
  email?: string;
}

function createUser(id: number, name: string): User {
  const user: User = {} as User;
  user.id = id;
  user.name = name;
  // user.email 未设置，保持可选
  return user;
}
```

### 9. 对象字面量不能用于类型声明
- **规则**: `arkts-no-obj-literals-as-types`
- **级别**: 错误
- **错误码**: 10605040
- ❌ `function foo(): { x: number, y: number }`
- ✅ 使用 interface 或 class 定义类型

### 10. 数组字面量必须仅包含可推断类型的元素
- **规则**: `arkts-no-noninferrable-arr-literals`
- **级别**: 错误
- **错误码**: 10605043
- ❌ `let a = [{n: 1}, {n: 2}]`
- ✅ `let a: MyClass[] = [{n: 1}, {n: 2}]`

### 11. 不支持修改对象的方法
- **规则**: `arkts-no-method-reassignment`
- **级别**: 错误
- **错误码**: 10605052
- ❌ `obj.method = newFunc`
- ✅ 使用继承重写方法

---

## 🔴 运算符限制

### 1. 一元运算符 +、-、~ 仅适用于数值类型
- **规则**: `arkts-no-polymorphic-unops`
- **级别**: 错误
- **错误码**: 10605055
- ❌ `+'123'`（字符串转数字）
- ❌ `-'456'`
- ❌ `~'789'`
- ✅ 必须显式转换 `parseInt('123')`

### 2. 不支持逗号运算符（除了 for 循环）
- **规则**: `arkts-no-comma-outside-loops`
- **级别**: 错误
- **错误码**: 10605071
- ❌ `let x = (a += 1, a)`
- ✅ 分开执行 `a += 1; let x = a;`
- ✅ for循环中支持：`for (let i = 0, j = 0; i < 10; ++i, j += 2) {}`

### 3. instanceof 只能用于引用类型
- **规则**: `arkts-instanceof-ref-types`
- **级别**: 错误
- **错误码**: 10605065
- ❌ `5 instanceof Number`（原始值）
- ✅ `obj instanceof MyClass`（对象实例）

### 4. 部分支持展开运算符
- **规则**: `arkts-no-spread`
- **级别**: 错误
- **错误码**: 10605099
- ✅ 可以展开数组到数组字面量
- ✅ 可以展开到剩余参数
- ✅ 支持展开TypedArray（Int32Array等）
- ❌ 不能展开对象 `{ ...obj }`
- ❌ 不能展开元组到函数参数

---

## 🔴 函数限制

### 1. 不支持函数表达式
- **规则**: `arkts-no-func-expressions`
- **级别**: 错误
- **错误码**: 10605046
- ❌ `let f = function() {}`
- ✅ `let f = () => {}`（箭头函数）

### 2. 不支持在函数内声明函数
- **规则**: `arkts-no-nested-funcs`
- **级别**: 错误
- **错误码**: 10605092
- ❌ 嵌套函数声明
- ✅ 使用 lambda/箭头函数

### 3. 不支持参数解构
- **规则**: `arkts-no-destruct-params`
- **级别**: 错误
- **错误码**: 10605091
- ❌ `function foo({a, b}) {}`
- ✅ `function foo(obj: MyClass) {}`

### 4. 不支持解构赋值
- **规则**: `arkts-no-destruct-assignment`
- **级别**: 错误
- **错误码**: 10605069
- ❌ `let {a, b} = obj;`
- ❌ `let [x, y] = arr;`
- ✅ `let a = obj.a; let b = obj.b;`

### 5. 不支持解构变量声明
- **规则**: `arkts-no-destruct-decls`
- **级别**: 错误
- **错误码**: 10605074
- ❌ `const {x, y} = point;`
- ✅ `const x = point.x; const y = point.y;`

### 6. 限制省略函数返回类型标注
- **规则**: `arkts-no-implicit-return-types`
- **级别**: 错误
- **错误码**: 10605090
- ⚠️ 某些场景必须显式标注返回类型

### 7. 不支持生成器函数
- **规则**: `arkts-no-generators`
- **级别**: 错误
- **错误码**: 10605094
- ❌ `function* gen() {}`
- ✅ 使用 async/await

### 8. 不支持对函数声明属性
- **规则**: `arkts-no-func-props`
- **级别**: 错误
- **错误码**: 10605139
- ❌ `foo.property = value`
- ✅ 使用类

### 9. 不支持 Function.apply/call/bind
- **规则**: `arkts-no-func-apply-call`, `arkts-no-func-bind`
- **级别**: 错误/警告
- **错误码**: 10605152, 10605140
- ❌ `fn.apply(this, args)`
- ❌ `fn.call(this, arg1, arg2)`
- ❌ `fn.bind(this)`
- ✅ 直接调用或使用箭头函数

### 10. 不支持在独立函数和静态方法中使用 this
- **规则**: `arkts-no-standalone-this`
- **级别**: 错误
- **错误码**: 10605093
- ❌ 独立函数中使用 `this`
- ✅ `this` 只能在类实例方法中使用

### 11. 不支持具有 call signature 的类型
- **规则**: `arkts-no-call-signatures`
- **级别**: 错误
- **错误码**: 10605014
- ❌ `type DescribableFunction = { (someArg: string): string }`
- ✅ 使用 class

### 12. 不支持具有构造签名的类型
- **规则**: `arkts-no-ctor-signatures-type`
- **级别**: 错误
- **错误码**: 10605015
- ❌ `type SomeConstructor = { new (s: string): SomeObject }`
- ✅ 使用 class

---

## 🔴 控制流限制

### 1. 不支持 for...in
- **规则**: `arkts-no-for-in`
- **级别**: 错误
- **错误码**: 10605080
- ❌ `for (let key in obj) {}`
- ✅ `for (let i = 0; i < arr.length; i++) {}`

### 2. 不支持 with 语句
- **规则**: `arkts-no-with`
- **级别**: 错误
- **错误码**: 10605084
- ❌ `with (Math) { ... }`
- ✅ `Math.PI` 直接访问

### 3. throw 只能抛出 Error 类实例
- **规则**: `arkts-limited-throw`
- **级别**: 错误
- **错误码**: 10605087
- ❌ `throw 4;`
- ❌ `throw 'error';`
- ✅ `throw new Error('message');`

### 4. finally 块不能非正常结束
- ❌ finally 中使用 return、break、continue、throw
- ✅ 保证 finally 正常执行完毕

### 5. catch 语句不能标注类型
- **规则**: `arkts-no-types-in-catch`
- **级别**: 错误
- **错误码**: 10605079
- ❌ `catch (e: Error) {}`
- ✅ `catch (e) {}`

---

## 🔴 类和接口限制

### 1. 不支持类表达式
- **规则**: `arkts-no-class-literals`
- **级别**: 错误
- **错误码**: 10605050
- ❌ `const C = class {}`
- ✅ `class C {}`

### 2. 类不允许 implements 类
- **规则**: `arkts-implements-only-iface`
- **级别**: 错误
- **错误码**: 10605051
- ❌ `class A implements B {}`（B是类）
- ✅ `class A implements IB {}`（IB是接口）

### 3. 不支持在 constructor 中声明字段
- **规则**: `arkts-no-ctor-prop-decls`
- **级别**: 错误
- **错误码**: 10605025
- ❌ `constructor(public name: string) {}`
- ✅ 字段必须在类体中声明

### 4. 不支持 index signature
- **规则**: `arkts-no-indexed-signatures`
- **级别**: 错误
- **错误码**: 10605017
- ❌ `interface I { [key: string]: number }`
- ✅ 使用 Map 或具体属性

### 5. 接口不能继承类
- **规则**: `arkts-extends-only-class`
- **级别**: 错误
- **错误码**: 10605104
- ❌ `interface I extends MyClass {}`
- ✅ `interface I extends OtherInterface {}`

### 6. 接口不能继承具有相同方法的两个接口
- **规则**: `arkts-no-extend-same-prop`
- **级别**: 错误
- **错误码**: 10605102
- ❌ 继承冲突的方法
- ✅ 重命名方法

### 7. 不支持声明合并
- **规则**: `arkts-no-decl-merging`
- **级别**: 错误
- **错误码**: 10605103
- ❌ 多次声明同一个 interface
- ✅ 合并到一个声明中

### 8. 接口中不支持构造签名
- **规则**: `arkts-no-ctor-signatures-iface`
- **级别**: 错误
- **错误码**: 10605027
- ❌ `interface I { new (): I }`
- ✅ 使用工厂方法

### 9. 不支持构造函数类型
- **规则**: `arkts-no-ctor-signatures-funcs`
- **级别**: 错误
- **错误码**: 10605106
- ❌ `type Ctor = new () => T`
- ✅ 使用工厂函数类型

### 10. 不支持枚举混合类型
- **规则**: `arkts-no-enum-mixed-types`
- **级别**: 错误
- **错误码**: 10605111
- ❌ `enum E { A = 1, B = 'str' }`
- ✅ 所有成员必须是相同类型（全是数字或全是字符串）

### 11. 不支持枚举声明合并
- **规则**: `arkts-no-enum-merging`
- **级别**: 错误
- **错误码**: 10605113
- ❌ 多次声明同一个 enum
- ✅ 合并到一个声明中

### 12. 不支持在原型上赋值
- **规则**: `arkts-no-prototype-assignment`
- **级别**: 错误
- **错误码**: 10605136
- ❌ `Class.prototype.method = func`
- ✅ 在类定义中声明方法

### 13. class 不能被用作对象
- **规则**: `arkts-no-classes-as-obj`
- **级别**: 警告
- **错误码**: 10605149
- ⚠️ class 是类型，不是值

### 14. 仅支持一个静态块
- **规则**: `arkts-no-multiple-static-blocks`
- **级别**: 错误
- **错误码**: 10605016
- ❌ 类中存在多个 static {}
- ✅ 合并到一个静态块中

### 15. 不支持 is 类型保护
- **规则**: `arkts-no-is`
- **级别**: 错误
- **错误码**: 10605096
- ❌ `function isFoo(arg): arg is Foo`
- ✅ 使用 `instanceof` 和 `as`

### 16. 不支持 new.target
- **规则**: `arkts-no-new-target`
- **级别**: 错误
- **错误码**: 10605132
- ❌ 使用 `new.target`

---

## 🔴 模块和导入限制

### 1. import 语句必须在文件顶部
- **规则**: `arkts-no-misplaced-imports`
- **级别**: 错误
- **错误码**: 10605150
- ❌ 其他语句在前，import 在后
- ✅ 所有 import 在最前面（动态 import 除外）

### 2. 不支持 require
- **规则**: `arkts-no-require`
- **级别**: 错误
- **错误码**: 10605121
- ❌ `import m = require('mod')`
- ✅ `import * as m from 'mod'`

### 3. 不支持 export = 语法
- **规则**: `arkts-no-export-assignment`
- **级别**: 错误
- **错误码**: 10605126
- ❌ `export = MyClass`
- ✅ `export { MyClass }`

### 4. 不支持 ambient module 声明
- **规则**: `arkts-no-ambient-decls`
- **级别**: 错误
- **错误码**: 10605128
- ❌ `declare module 'mod' {}`
- ✅ 直接 import

### 5. 不支持模块名通配符
- **规则**: `arkts-no-module-wildcards`
- **级别**: 错误
- **错误码**: 10605129
- ❌ `declare module '!*text' {}`

### 6. 不支持 UMD 格式
- **规则**: `arkts-no-umd`
- **级别**: 错误
- **错误码**: 10605130
- ❌ 通用模块定义
- ✅ 使用 ES6 模块

### 7. .ets 文件和 .ts/.js 文件的依赖规则
- **规则**: `arkts-no-ts-deps`
- **级别**: 错误
- **错误码**: 10605147
- ✅ .ets 可以 import .ets/.ts/.js
- ❌ .ts/.js 不能 import .ets

### 8. 命名空间限制
- ❌ 命名空间中不能包含非声明语句
- ❌ 不能将命名空间作为对象使用
- **规则**: `arkts-no-ns-statements`, `arkts-no-ns-as-obj`
- **错误码**: 10605116, 10605114

---

## 🔴 标准库限制

### 禁用的全局对象
- ❌ `eval`

### 禁用的 Object 方法
- ❌ `__proto__`
- ❌ `__defineGetter__`
- ❌ `__defineSetter__`
- ❌ `__lookupGetter__`
- ❌ `__lookupSetter__`
- ❌ `assign`
- ❌ `create`
- ❌ `defineProperties`
- ❌ `defineProperty`
- ❌ `freeze`
- ❌ `fromEntries`
- ❌ `getOwnPropertyDescriptor`
- ❌ `getOwnPropertyDescriptors`
- ❌ `getOwnPropertySymbols`
- ❌ `getPrototypeOf`
- ❌ `hasOwnProperty`
- ❌ `is`
- ❌ `isExtensible`
- ❌ `isFrozen`
- ❌ `isPrototypeOf`
- ❌ `isSealed`
- ❌ `preventExtensions`
- ❌ `propertyIsEnumerable`
- ❌ `seal`
- ❌ `setPrototypeOf`

### 禁用的 Reflect 方法
- ❌ `Reflect.apply`
- ❌ `Reflect.construct`
- ❌ `Reflect.defineProperty`
- ❌ `Reflect.deleteProperty`
- ❌ `Reflect.get`
- ❌ `Reflect.getOwnPropertyDescriptor`
- ❌ `Reflect.getPrototypeOf`
- ❌ `Reflect.has`
- ❌ `Reflect.isExtensible`
- ❌ `Reflect.ownKeys`
- ❌ `Reflect.preventExtensions`
- ❌ `Reflect.set`
- ❌ `Reflect.setPrototypeOf`

### 禁用的 Proxy handler
- ❌ `handler.apply()`
- ❌ `handler.construct()`
- ❌ `handler.defineProperty()`
- ❌ `handler.deleteProperty()`
- ❌ `handler.get()`
- ❌ `handler.getOwnPropertyDescriptor()`
- ❌ `handler.getPrototypeOf()`
- ❌ `handler.has()`
- ❌ `handler.isExtensible()`
- ❌ `handler.ownKeys()`
- ❌ `handler.preventExtensions()`
- ❌ `handler.set()`
- ❌ `handler.setPrototypeOf()`

### 限制使用的 Utility Types
- ✅ 仅支持：`Partial<T>`, `Required<T>`, `Readonly<T>`, `Record<K, T>`
- ❌ 其他 Utility Types 不支持

---

## 📝 编程规范

### 1. 命名规则
- **类名、枚举名、命名空间名**: UpperCamelCase（大驼峰）
- **变量名、方法名、参数名**: lowerCamelCase（小驼峰）
- **常量名、枚举值名**: UPPER_SNAKE_CASE（全大写下划线分隔）
- 布尔变量名加前缀：`is`, `has`, `can`, `should`
- 避免否定的布尔变量名

### 2. 代码格式
- 使用 2 个空格缩进（禁止使用 Tab）
- 行宽不超过 120 字符
- 建议字符串使用单引号
- 条件语句和循环语句必须使用大括号
- 大括号与语句同行
- 表达式换行时运算符放行末

### 3. 强制严格类型检查
- noImplicitReturns
- strictFunctionTypes
- strictNullChecks
- strictPropertyInitialization

### 4. 不允许关闭类型检查
- ❌ `@ts-ignore`
- ❌ `@ts-nocheck`
- ❌ `@ts-expect-error`

### 5. 其他编程实践
- 数组遍历优先使用 Array 对象方法（forEach, map, filter, reduce等）
- 判断 NaN 必须使用 `Number.isNaN()`
- 不要在控制性条件表达式中执行赋值操作
- 在 finally 代码块中，不要使用 return、break、continue 或抛出异常
- 避免使用 ESObject 类型（除非跨语言调用）
- 使用 `T[]` 表示数组类型

### 6. 使用 let 而非 var
- **规则**: `arkts-no-var`
- **级别**: 错误
- **错误码**: 10605005
- ❌ `var x = 1;`
- ✅ `let x = 1;`

### 7. 类型、命名空间的命名必须唯一
- **规则**: `arkts-unique-names`
- **级别**: 错误
- **错误码**: 10605004
- ❌ 类型名与变量名重复

### 8. 不支持确定赋值断言
- **规则**: `arkts-no-definite-assignment`
- **级别**: 警告
- **错误码**: 10605134
- ⚠️ `let v!: T` 会产生警告
- ✅ 在声明变量的同时为变量赋值

### 9. 不支持 globalThis
- **规则**: `arkts-no-globalthis`
- **级别**: 警告
- **错误码**: 10605137
- ❌ 使用 `globalThis`
- ✅ 使用模块导入导出

### 10. 不支持 as const 断言
- **规则**: `arkts-no-as-const`
- **级别**: 错误
- **错误码**: 10605142
- ❌ `let x = 'hello' as const;`
- ✅ `let x: string = 'hello';`

### 11. 不支持导入断言
- **规则**: `arkts-no-import-assertions`
- **级别**: 错误
- **错误码**: 10605143
- ❌ `import { obj } from 'something.json' assert { type: 'json' }`
- ✅ 使用常规 import

### 12. 类型转换仅支持 as T 语法
- **规则**: `arkts-as-casts`
- **级别**: 错误
- **错误码**: 10605053
- ❌ `<type>value`
- ✅ `value as Type`

### 13. 不支持 JSX 表达式
- **规则**: `arkts-no-jsx`
- **级别**: 错误
- **错误码**: 10605054
- ❌ 使用 JSX

### 14. 限制使用 ESObject 类型
- **规则**: `arkts-limited-esobj`
- **级别**: 警告
- **错误码**: 10605151
- ⚠️ 仅用于跨语言调用场景

---

## 📚 参考文档

- [从TypeScript到ArkTS的适配规则](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/typescript-to-arkts-migration-guide)
- [ArkTS编程规范](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides-v5/arkts-coding-style-guide-V5)
- [ArkTS语言介绍](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts)

---

**最后更新时间**: 2026-01-26
**文档版本**: v1.0
