# API 特征 → ArkTS 动态语法约束速查表

> Phase 3 解析 .d.ts 时，根据 API 签名中的特征模式，查表获取对应的 ArkTS 动态语法约束。
> Phase 5 生成代码时，从 Phase 3 输出的 `arkts_constraints` 字段读取约束，无需重新查表。
> 本表仅适用于 **ArkTS-Dyn（动态）** 项目。ArkTS-Sta（静态）项目使用 `ohos-dev-arkts-static-specification-reference` 技能。

## 使用方式

Phase 3 解析每个 API 的 .d.ts 签名后，检测下表「检测模式」列中的特征。命中则将「约束」内容写入该 API 知识库条目的 `arkts_constraints` 数组。多个特征可同时命中，约束叠加。

---

## 1. Promise\<T> / 异步返回值

**检测模式**：方法签名返回 `Promise<T>` 或参数含 `AsyncCallback<T>`

**约束**：
- 使用 `async/await` 模式调用，不使用 `.then()` 链（ArkTS 限制链式调用的上下文推断）
- `catch (e)` 不标注类型：禁止 `catch (e: Error)`，使用 `catch (e)` 后通过 `instanceof` 判断类型
- `throw` 只能抛出 `Error` 实例：`throw new Error('msg')`，禁止 `throw 'string'` 或 `throw 123`
- `finally` 块中禁止使用 `return`、`throw`、`break`、`continue`
- `done: () => void` 回调参数禁止写成 `done: Function`（错误码 10605008）
- `resolve` 参数禁止写成 `resolve: Function`，使用 `resolve: (value: void | PromiseLike<void>) => void`
- async 函数返回类型需显式标注（ArkTS-Sta 强制，ArkTS-Dyn 推荐）

**相关规则**：`arkts-no-types-in-catch`、`arkts-limited-throw`、`arkts-no-implicit-return-types`、`arkts-no-any-unknown`

**典型错误码**：10605079（catch 标注类型）、10605087（throw 非 Error）、10605008（any/Function 类型）

---

## 2. 泛型参数 \<T>

**检测模式**：方法签名含泛型 `<T>`、`<K, V>` 等

**约束**：
- 不支持条件类型 `T extends U ? X : Y`（规则 `arkts-no-conditional-types`，错误码 10605022）
- 不支持映射类型 `{ [K in keyof T]: V }`（规则 `arkts-no-mapped-types`，错误码 10605083）
- 不支持索引访问类型 `T[K]`（规则 `arkts-no-aliases-by-index`，错误码 10605028）
- 不支持 `infer` 关键字
- 不支持交叉类型 `T & U`（规则 `arkts-no-intersection-types`，错误码 10605019），用继承替代 `interface X extends A, B {}`
- 不支持 `this` 类型（规则 `arkts-no-typing-with-this`，错误码 10605021）
- 仅支持 `Partial<T>`、`Required<T>`、`Readonly<T>`、`Record<K, T>` 四个 Utility Types

**相关规则**：`arkts-no-conditional-types`、`arkts-no-mapped-types`、`arkts-no-intersection-types`

**典型错误码**：10605022、10605083、10605028、10605019

---

## 3. 回调函数 callback: (err, data) => void

**检测模式**：参数含回调函数类型 `(err: Error, data: T) => void` 或 `AsyncCallback<T>`

**约束**：
- 使用箭头函数 `() => {}` 作为回调，禁止 `function() {}` 函数表达式（规则 `arkts-no-func-expressions`，错误码 10605046）
- 禁止嵌套函数声明，回调内需要辅助函数时用箭头函数（规则 `arkts-no-nested-funcs`，错误码 10605092）
- 禁止参数解构 `function foo({a, b})`（规则 `arkts-no-destruct-params`，错误码 10605091）
- 禁止 `Function.apply/call/bind`（规则 `arkts-no-func-apply-call`、`arkts-no-func-bind`，错误码 10605152/10605140）
- 禁止 call signature 类型 `type F = { (arg: string): string }`（规则 `arkts-no-call-signatures`，错误码 10605014）
- 禁止构造 signature 类型 `type Ctor = { new (): T }`（规则 `arkts-no-ctor-signatures-type`，错误码 10605015）
- 回调参数类型必须显式标注，禁止隐式 `any`（错误码 10605008）

**相关规则**：`arkts-no-func-expressions`、`arkts-no-nested-funcs`、`arkts-no-func-apply-call`

**典型错误码**：10605046、10605092、10605152

---

## 4. 集合类型 Array\<T> / Map\<K,V> / Set\<T>

**检测模式**：参数或返回值使用 `Array<T>`、`Map<K,V>`、`Set<T>`、`Collections.Array<T>` 等

**约束**：
- 禁止 `for...in` 遍历（规则 `arkts-no-for-in`，错误码 10605080），使用 `for...of` 或索引 `for` 循环
- 禁止索引访问字段 `obj[key]`（规则 `arkts-no-props-by-index`，错误码 10605029），使用点操作符 `obj.key`
- 展开运算符仅限数组场景：`[...arr]` 合法，`{...obj}` 非法（规则 `arkts-no-spread`，错误码 10605099）
- 数组字面量必须可推断类型：`let a = [{n:1}]` 需改为 `let a: MyType[] = [{n:1}]`（规则 `arkts-no-noninferrable-arr-literals`，错误码 10605043）
- 禁止修改对象方法 `obj.method = newFunc`（规则 `arkts-no-method-reassignment`，错误码 10605052）

**相关规则**：`arkts-no-for-in`、`arkts-no-props-by-index`、`arkts-no-spread`

**典型错误码**：10605080、10605029、10605099

---

## 5. 对象/Record 类型参数

**检测模式**：参数类型为 `Record<string, T>`、`ESObject`、自定义 interface，或方法接受对象字面量参数

**约束**：
- 对象字面量必须显式标注类型（规则 `arkts-no-untyped-obj-literals`，错误码 10605038）
- 对象字面量不能用于类型声明 `function foo(): { x: number }`（规则 `arkts-no-obj-literals-as-types`，错误码 10605040），必须先定义 interface
- 不支持 index signature `interface I { [key: string]: number }`（规则 `arkts-no-indexed-signatures`，错误码 10605017），使用 `Map` 或具体属性
- 不支持解构赋值 `const {a, b} = obj`（规则 `arkts-no-destruct-assignment`，错误码 10605069），改为逐个赋值 `const a = obj.a`
- 不支持解构变量声明 `const {x, y} = point`（规则 `arkts-no-destruct-decls`，错误码 10605074）
- 对象布局固定，运行时不能添加/删除属性
- 禁止 `delete obj.property`（规则 `arkts-no-delete`，错误码 10605059），用可空类型 `property: Type | null`
- 禁止 `'prop' in obj`（规则 `arkts-no-in`，错误码 10605066），用 `instanceof`
- 禁止 `Symbol()`（规则 `arkts-no-symbol`，错误码 10605002），仅支持 `Symbol.iterator`
- `ESObject` 仅用于跨语言调用场景（规则 `arkts-limited-esobj`），JSON.parse 结果可用 `ESObject`

**相关规则**：`arkts-no-untyped-obj-literals`、`arkts-no-destruct-assignment`、`arkts-no-delete`

**典型错误码**：10605038、10605040、10605069、10605059

---

## 6. 类/接口/枚举相关

**检测模式**：API 涉及 class 实例化、implements 接口、enum 参数

**约束**：
- 不支持类表达式 `const C = class {}`（规则 `arkts-no-class-literals`，错误码 10605050），使用 `class C {}` 声明
- 类 implements 只能跟接口，不能跟类 `class A implements B {}`（B 是类则非法，规则 `arkts-implements-only-iface`，错误码 10605051）
- 不支持 constructor 中声明字段 `constructor(public name: string)`（规则 `arkts-no-ctor-prop-decls`，错误码 10605025）
- 接口不能继承类 `interface I extends MyClass {}`（规则 `arkts-extends-only-class`，错误码 10605104）
- 不支持声明合并（多次声明同名 interface）
- 枚举所有成员必须是相同类型（全数字或全字符串，规则 `arkts-no-enum-mixed-types`，错误码 10605111）
- 不支持 is 类型保护 `function isFoo(arg): arg is Foo`（规则 `arkts-no-is`，错误码 10605096），用 `instanceof` + `as`
- 类型转换仅支持 `as T` 语法，禁止 `<Type>value`（规则 `arkts-as-casts`，错误码 10605053）

**相关规则**：`arkts-no-class-literals`、`arkts-implements-only-iface`、`arkts-no-is`

**典型错误码**：10605050、10605051、10605025、10605111

---

## 7. 模块导入

**检测模式**：需要 import 模块（所有 API 均涉及）

**约束**：
- import 语句必须在文件顶部（规则 `arkts-no-misplaced-imports`，错误码 10605150）
- 不支持 `require`（规则 `arkts-no-require`，错误码 10605121），用 `import * as m from 'mod'`
- 不支持 `export =` 语法（规则 `arkts-no-export-assignment`，错误码 10605126）
- 不支持 ambient module 声明 `declare module 'mod' {}`
- `.ets` 可以 import `.ets/.ts/.js`，但 `.ts/.js` 不能 import `.ets`
- Kit 路径用点号：`@ohos.router` 不是 `@ohos/router`

**相关规则**：`arkts-no-misplaced-imports`、`arkts-no-require`

**典型错误码**：10605150、10605121、10505001

---

## 8. 类型系统通用约束（所有 API 均适用）

**检测模式**：始终适用

**约束**：
- 禁止 `any` 和 `unknown` 类型（规则 `arkts-no-any-unknown`，错误码 10605008）
- 不支持 structural typing（结构化类型），不同类即使属性相同也不能互相赋值
- `typeof` 只能用于表达式，不能用于类型查询 `let x: typeof y`（规则 `arkts-no-type-query`，错误码 10605060）
- 禁止 `var`，使用 `let` 或 `const`（规则 `arkts-no-var`，错误码 10605005）
- 不支持 `as const` 断言（规则 `arkts-no-as-const`，错误码 10605142）
- 不支持确定赋值断言 `let v!: T`（规则 `arkts-no-definite-assignment`，警告 10605134）
- 禁止 `@ts-ignore`、`@ts-nocheck`、`@ts-expect-error`
- 不支持 `globalThis`（规则 `arkts-no-globalthis`，警告 10605137）
- 不支持 JSX 表达式

**相关规则**：`arkts-no-any-unknown`、`arkts-no-var`

**典型错误码**：10605008、10605005

---

## 9. @Sendable 装饰器

**检测模式**：API 或类标注了 `@Sendable` 装饰器

**约束**：
- `@Sendable` 函数只能带 `@Sendable` 装饰器
- sendable 函数不允许任意访问函数对象属性
- `@Sendable` 类型别名只能声明为函数类型
- 非 sendable 函数不能通过 `as` 断言转换成 sendable 函数类型
- 传给 taskpool 相关 API 的函数必须是普通函数并带 `@Concurrent` 装饰器

---

## 10. 标准库禁用项（测试代码中易误用）

**检测模式**：生成的测试代码中可能使用标准库方法

**约束**：
- 禁用 `eval`
- 禁用 `Object.assign`、`Object.create`、`Object.freeze`、`Object.defineProperty` 等
- 禁用所有 `Reflect.*` 方法
- 禁用所有 `Proxy` handler
- 一元运算符 `+`、`-`、`~` 仅适用于数值类型，禁止 `+'123'`（规则 `arkts-no-polymorphic-unops`，错误码 10605055），用 `parseInt('123')`
- `instanceof` 只能用于引用类型，禁止 `5 instanceof Number`
- 不支持 `with` 语句
- 判断 NaN 必须使用 `Number.isNaN()`

---

## Phase 3 查表流程

```
解析 .d.ts 签名 → 检测特征模式 → 查本表命中约束 → 写入 API 知识库条目 arkts_constraints[]
                                         ↓ 未命中
                              保持 arkts_constraints: []
```

## Phase 8 编译失败兜底

编译失败的错误码若不在本表覆盖范围内，调用 `arkts-skill` 的 `search_docs.py` 兜底查询：

```bash
python3 {arkts_skill_root}/scripts/search_docs.py --query "ESE0046 arkts type not compatible fix"
```

返回结果包含 `source_kind`（official-guide / openharmony-arkts-api / linter-summary）和精准修复方案。
