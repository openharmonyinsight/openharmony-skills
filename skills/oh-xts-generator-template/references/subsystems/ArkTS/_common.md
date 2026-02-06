# ArkTS 子系统通用配置

> **子系统信息**
> - 名称: ArkTS（ArkUI编程语言）
> - 测试路径: test/xts/acts/arkts/
> - 版本: 1.0.0
> - 更新日期: 2025-02-02
> - 参考文档: `.claude/skills/oh-xts-generator-template/references/ArkTS_Dynamic_Syntax_Rules.md`

## 一、子系统通用配置

### 1.1 ArkTS 语法规则概述

ArkTS 是 OpenHarmony 的官方开发语言，基于 TypeScript 扩展并进行了严格的语法限制。**重要**：为 ArkTS 子系统生成测试用例时，必须遵守 ArkTS 语法规则，**级别为"错误"的规则会导致编译失败，因此无需为这些场景生成测试用例**。

### 1.2 编译错误级别规则（无需生成用例）

以下规则级别为**错误**，违反这些规则会导致编译失败，**不应为这些场景生成测试用例**：

#### 类型系统限制（7条规则）

| 规则 | 错误码 | 限制内容 | 无需测试场景 |
|-----|-------|---------|------------|
| `arkts-no-any-unknown` | 10605008 | 禁用 any 和 unknown 类型 | 测试 any/unknown 类型参数 |
| `arkts-no-structural-typing` | 10605030 | 不支持结构化类型 | 测试不同类互相赋值 |
| `arkts-no-conditional-types` | 10605022 | 不支持条件类型 | 测试条件类型 `type X<T> = T extends number ? T : never` |
| `arkts-no-mapped-types` | 10605083 | 不支持映射类型 | 测试映射类型 `type OptionsFlags<Type> = { [Property in keyof Type]: boolean }` |
| `arkts-no-aliases-by-index` | 10605028 | 不支持索引访问类型 | 测试索引访问类型 `type T = SomeType[key]` |
| `arkts-no-typing-with-this` | 10605021 | 不支持 this 类型 | 测试 `function foo(): this` |
| `arkts-no-type-query` | 10605060 | typeof 只能用于表达式 | 测试 `let x: typeof y` |
| `arkts-no-intersection-types` | 10605019 | 不支持交叉类型 | 测试 `type Employee = Identity & Contact` |

#### 对象和属性限制（11条规则）

| 规则 | 错误码 | 限制内容 | 无需测试场景 |
|-----|-------|---------|------------|
| `arkts-no-props-by-index` | 10605029 | 不支持通过索引访问字段 | 测试 `obj['propertyName']`、`obj[key]` |
| `arkts-identifiers-as-prop-names` | 10605001 | 属性名必须是合法的标识符 | 测试数字属性名 `{ 1: 'value' }`、字符串属性名 `{ 'name': 'value' }` |
| `arkts-no-symbol` | 10605002 | 不支持 Symbol() API | 测试 `Symbol()`（Symbol.iterator 除外） |
| `arkts-no-private-identifiers` | 10605003 | 不支持 # 私有字段 | 测试 `class C { #field: number }` |
| `arkts-no-delete` | 10605059 | 不支持 delete 运算符 | 测试 `delete obj.property` |
| `arkts-no-in` | 10605066 | 不支持 in 运算符 | 测试 `'prop' in obj` |
| `arkts-no-untyped-obj-literals` | 10605038 | 对象字面量必须显式标注类型 | 测试无类型注解的对象字面量 `let o = { x: 1, y: 2 }` |
| `arkts-no-obj-literals-as-types` | 10605040 | 对象字面量不能用于类型声明 | 测试 `function foo(): { x: number, y: number }` |
| `arkts-no-noninferrable-arr-literals` | 10605043 | 数组字面量必须仅包含可推断类型的元素 | 测试 `let a = [{n: 1}, {n: 2}]` |
| `arkts-no-method-reassignment` | 10605052 | 不支持修改对象的方法 | 测试 `obj.method = newFunc` |

#### 运算符限制（4条规则）

| 规则 | 错误码 | 限制内容 | 无需测试场景 |
|-----|-------|---------|------------|
| `arkts-no-polymorphic-unops` | 10605055 | 一元运算符 +、-、~ 仅适用于数值类型 | 测试 `+'123'`（字符串转数字） |
| `arkts-no-comma-outside-loops` | 10605071 | 不支持逗号运算符（除了 for 循环） | 测试 `let x = (a += 1, a)`（for 循环除外） |
| `arkts-instanceof-ref-types` | 10605065 | instanceof 只能用于引用类型 | 测试 `5 instanceof Number`（原始值） |
| `arkts-no-spread` | 10605099 | 部分支持展开运算符 | 测试展开对象 `{ ...obj }`、展开元组到函数参数 |

#### 函数限制（12条规则）

| 规则 | 错误码 | 限制内容 | 无需测试场景 |
|-----|-------|---------|------------|
| `arkts-no-func-expressions` | 10605046 | 不支持函数表达式 | 测试 `let f = function() {}` |
| `arkts-no-nested-funcs` | 10605092 | 不支持在函数内声明函数 | 测试嵌套函数声明 |
| `arkts-no-destruct-params` | 10605091 | 不支持参数解构 | 测试 `function foo({a, b}) {}` |
| `arkts-no-destruct-assignment` | 10605069 | 不支持解构赋值 | 测试 `let {a, b} = obj;`、`let [x, y] = arr;` |
| `arkts-no-destruct-decls` | 10605074 | 不支持解构变量声明 | 测试 `const {x, y} = point;` |
| `arkts-no-implicit-return-types` | 10605090 | 限制省略函数返回类型标注 | 测试省略返回类型注解的场景（某些场景必须显式标注） |
| `arkts-no-generators` | 10605094 | 不支持生成器函数 | 测试 `function* gen() {}` |
| `arkts-no-func-props` | 10605139 | 不支持对函数声明属性 | 测试 `foo.property = value` |
| `arkts-no-func-apply-call` | 10605152 | 不支持 Function.apply/call | 测试 `fn.apply(this, args)`、`fn.call(this, arg1, arg2)` |
| `arkts-no-func-bind` | 10605140 | 不支持 Function.bind | 测试 `fn.bind(this)` |
| `arkts-no-standalone-this` | 10605093 | 不支持在独立函数和静态方法中使用 this | 测试独立函数中使用 `this` |
| `arkts-no-call-signatures` | 10605014 | 不支持具有 call signature 的类型 | 测试 `type DescribableFunction = { (someArg: string): string }` |
| `arkts-no-ctor-signatures-type` | 10605015 | 不支持具有构造签名的类型 | 测试 `type SomeConstructor = { new (s: string): SomeObject }` |

#### 控制流限制（5条规则）

| 规则 | 错误码 | 限制内容 | 无需测试场景 |
|-----|-------|---------|------------|
| `arkts-no-for-in` | 10605080 | 不支持 for...in | 测试 `for (let key in obj) {}` |
| `arkts-no-with` | 10605084 | 不支持 with 语句 | 测试 `with (Math) { ... }` |
| `arkts-limited-throw` | 10605087 | throw 只能抛出 Error 类实例 | 测试 `throw 4;`、`throw 'error';` |
| - | - | finally 块不能非正常结束 | 测试 finally 中使用 return、break、continue、throw |
| `arkts-no-types-in-catch` | 10605079 | catch 语句不能标注类型 | 测试 `catch (e: Error) {}` |

#### 类和接口限制（16条规则）

| 规则 | 错误码 | 限制内容 | 无需测试场景 |
|-----|-------|---------|------------|
| `arkts-no-class-literals` | 10605050 | 不支持类表达式 | 测试 `const C = class {}` |
| `arkts-implements-only-iface` | 10605051 | 类不允许 implements 类 | 测试 `class A implements B {}`（B是类） |
| `arkts-no-ctor-prop-decls` | 10605025 | 不支持在 constructor 中声明字段 | 测试 `constructor(public name: string) {}` |
| `arkts-no-indexed-signatures` | 10605017 | 不支持 index signature | 测试 `interface I { [key: string]: number }` |
| `arkts-extends-only-class` | 10605104 | 接口不能继承类 | 测试 `interface I extends MyClass {}` |
| `arkts-no-extend-same-prop` | 10605102 | 接口不能继承具有相同方法的两个接口 | 测试继承冲突的方法 |
| `arkts-no-decl-merging` | 10605103 | 不支持声明合并 | 测试多次声明同一个 interface |
| `arkts-no-ctor-signatures-iface` | 10605027 | 接口中不支持构造签名 | 测试 `interface I { new (): I }` |
| `arkts-no-ctor-signatures-funcs` | 10605106 | 不支持构造函数类型 | 测试 `type Ctor = new () => T` |
| `arkts-no-enum-mixed-types` | 10605111 | 不支持枚举混合类型 | 测试 `enum E { A = 1, B = 'str' }` |
| `arkts-no-enum-merging` | 10605113 | 不支持枚举声明合并 | 测试多次声明同一个 enum |
| `arkts-no-prototype-assignment` | 10605136 | 不支持在原型上赋值 | 测试 `Class.prototype.method = func` |
| `arkts-no-multiple-static-blocks` | 10605016 | 仅支持一个静态块 | 测试类中存在多个 static {} |
| `arkts-no-is` | 10605096 | 不支持 is 类型保护 | 测试 `function isFoo(arg): arg is Foo` |
| `arkts-no-new-target` | 10605132 | 不支持 new.target | 测试使用 `new.target` |

#### 模块和导入限制（8条规则）

| 规则 | 错误码 | 限制内容 | 无需测试场景 |
|-----|-------|---------|------------|
| `arkts-no-misplaced-imports` | 10605150 | import 语句必须在文件顶部 | 测试 import 语句在其他语句之后 |
| `arkts-no-require` | 10605121 | 不支持 require | 测试 `import m = require('mod')` |
| `arkts-no-export-assignment` | 10605126 | 不支持 export = 语法 | 测试 `export = MyClass` |
| `arkts-no-ambient-decls` | 10605128 | 不支持 ambient module 声明 | 测试 `declare module 'mod' {}` |
| `arkts-no-module-wildcards` | 10605129 | 不支持模块名通配符 | 测试 `declare module '!*text' {}` |
| `arkts-no-umd` | 10605130 | 不支持 UMD 格式 | 测试通用模块定义 |
| `arkts-no-ts-deps` | 10605147 | .ts/.js 文件不能 import .ets | 测试 .ts/.js import .ets |
| `arkts-no-ns-statements` | 10605116 | 命名空间中不能包含非声明语句 | 测试命名空间中包含非声明语句 |
| `arkts-no-ns-as-obj` | 10605114 | 不能将命名空间作为对象使用 | 测试将命名空间作为对象使用 |

#### 标准库限制（大量方法禁用）

**禁用的全局对象**：
- ❌ `eval` - 无需测试

**禁用的 Object 方法**（28个）：
- ❌ `__proto__`, `__defineGetter__`, `__defineSetter__`, `__lookupGetter__`, `__lookupSetter__`
- ❌ `assign`, `create`, `defineProperties`, `defineProperty`, `freeze`, `fromEntries`
- ❌ `getOwnPropertyDescriptor`, `getOwnPropertyDescriptors`, `getOwnPropertySymbols`
- ❌ `getPrototypeOf`, `hasOwnProperty`, `is`, `isExtensible`, `isFrozen`, `isPrototypeOf`, `isSealed`
- ❌ `preventExtensions`, `propertyIsEnumerable`, `seal`, `setPrototypeOf`

**禁用的 Reflect 方法**（12个）：
- ❌ 所有 Reflect 方法均不支持

**禁用的 Proxy handler**（13个）：
- ❌ 所有 Proxy handler 均不支持

#### 编程规范（6条错误级别规则）

| 规则 | 错误码 | 限制内容 | 无需测试场景 |
|-----|-------|---------|------------|
| `arkts-no-var` | 10605005 | 使用 let 而非 var | 测试 `var x = 1;` |
| `arkts-unique-names` | 10605004 | 类型、命名空间的命名必须唯一 | 测试类型名与变量名重复 |
| `arkts-no-as-const` | 10605142 | 不支持 as const 断言 | 测试 `let x = 'hello' as const;` |
| `arkts-no-import-assertions` | 10605143 | 不支持导入断言 | 测试 `import { obj } from 'something.json' assert { type: 'json' }` |
| `arkts-as-casts` | 10605053 | 类型转换仅支持 as T 语法 | 测试 `<type>value` |
| `arkts-no-jsx` | 10605054 | 不支持 JSX 表达式 | 测试使用 JSX |

### 1.3 通用配置继承

本子系统继承全局通用配置（`references/subsystems/_common.md`）：

- **测试路径规范**: 见 `_common.md` 第 1.1 节
- **测试级别定义**: 见 `_common.md` 第 1.2 节
- **测试类型定义**: 见 `_common.md` 第 1.3 节
- **测试粒度定义**: 见 `_common.md` 第 1.4 节
- **错误码测试规则**: 见 `_common.md` 第 3.2 节
- **断言使用规则**: 见 `_common.md` 第 3.3 节
- **代码规范要求**: 见 `_common.md` 第 3.4 节

### 1.4 ArkTS 特有测试规则

1. **语法规则遵守**：
   - 所有生成的测试用例必须符合 ArkTS 语法规范
   - 不得使用"错误"级别的语法特性

2. **测试用例范围**：
   - ✅ 测试 ArkTS **支持的**语法特性
   - ✅ 测试 ArkTS API 的正常功能
   - ✅ 测试业务逻辑和边界场景
   - ❌ **不测试** ArkTS **不支持的**语法特性（会导致编译失败）

3. **对象字面量测试**：
   - 必须先定义接口或类，再创建对象实例
   - 使用类型断言（`{} as TypeName`）或空对象+属性赋值
   - 参考模板：
     ```typescript
     interface Point {
       x: number;
       y: number;
     }

     // 方式1：类型断言
     const p1: Point = { x: 1, y: 2 };

     // 方式2：空对象+属性赋值
     const p2: Point = {} as Point;
     p2.x = 1;
     p2.y = 2;
     ```

4. **异步测试**：
   - 优先使用 async/await 而非 .then()/.catch()
   - 使用 async 时必须标注返回类型 `Promise<void>`

5. **错误处理**：
   - 使用 `BusinessError` 类型
   - 异常场景断言优先使用 `err.code`

6. **类型注解**：
   - 所有变量必须显式标注类型
   - 禁止使用 `any` 和 `unknown`
   - 函数返回类型必须显式标注

### 1.5 测试路径规范

- 测试用例目录: `test/xts/acts/arkts/test/`
- 历史用例参考: `${OH_ROOT}/test/xts/acts/arkts/`
- API声明文件: N/A（ArkTS 是语言本身，非 API）

## 二、ArkTS 代码模板

### 2.1 对象字面量标准模板

```typescript
// 1. 先定义接口
interface Point {
  x: number;
  y: number;
}

// 2. 创建对象（两种方式）
// 方式1：直接初始化
const p1: Point = { x: 1, y: 2 };

// 方式2：空对象+属性赋值
const p2: Point = {} as Point;
p2.x = 1;
p2.y = 2;
```

### 2.2 测试用例标准模板

```typescript
/**
 * @tc.name ArkTSFeatureTest001
 * @tc.number SUB_ARKTS_LANGUAGE_FEATURE_001
 * @tc.desc 测试 ArkTS 支持的语言特性
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testArkTSFeature001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 准备测试数据
  let value: number = 42;
  let text: string = 'Hello';

  // 2. 执行测试
  let result: string = `${text} ${value}`;

  // 3. 验证结果
  expect(result).assertEqual('Hello 42');
});
```

### 2.3 错误码测试模板

```typescript
/**
 * @tc.name ArkTSErrorCode401Test001
 * @tc.number SUB_ARKTS_ERROR_CODE_401_001
 * @tc.desc 测试 ArkTS 错误码 401 - 参数错误
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testArkTSErrorCode401001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, () => {
  // 1. 准备测试数据
  let apiObject: APIName = new APIName();
  let invalidParam: ParamType = /* 触发错误的参数 */;

  // 2. 执行测试并捕获异常
  try {
    apiObject.methodName(invalidParam);
    expect().assertFail(); // 如果没有抛出异常，测试失败
  } catch (err: BusinessError) {
    // 3. 验证错误码（优先使用 err.code）
    expect(err.code).assertEqual(401);
  }
});
```

### 2.4 异步测试模板

```typescript
/**
 * @tc.name ArkTSAsyncFeatureTest001
 * @tc.number SUB_ARKTS_ASYNC_FEATURE_001
 * @tc.desc 测试 ArkTS 异步特性
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testArkTSAsyncFeature001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (): Promise<void> => {
  // 1. 准备测试数据
  let apiObject: APIName = new APIName();
  let paramValue: ParamType = /* 测试参数 */;

  // 2. 执行异步测试（使用 await）
  try {
    let result: ReturnType = await apiObject.methodName(paramValue);
    // 3. 验证结果
    expect(result).assertEqual(expectedValue);
  } catch (err: BusinessError) {
    expect().assertFail();
  }
});
```

## 三、测试注意事项

1. **语法规则优先级**：
   - ArkTS 语法规则 > 通用测试规则 > 子系统测试规则
   - 生成测试用例前，必须检查是否符合 ArkTS 语法规范

2. **编译错误避免**：
   - 严格遵循第 1.2 节列出的"编译错误级别规则"
   - 这些规则对应的场景**不应生成测试用例**

3. **类型安全**：
   - 所有变量必须显式标注类型
   - 禁止使用类型推断（除有限场景）
   - 对象字面量必须对应显式声明的类或接口

4. **测试用例命名**：
   - 禁止使用特殊标点符号（如 `[]`、`.` 等）
   - 使用驼峰命名法：`testArkTSFeature001`

5. **断言使用**：
   - 异常场景优先使用 `err.code` 断言
   - 代码逻辑走不到的分支使用 `expect().assertFail()`

6. **异步处理**：
   - 仅在测试业务中存在异步场景时使用 `async`
   - 优先使用 `async/await` 而非 `.then()/.catch()`

## 四、参考资源

| 资源类型 | 路径 | 说明 |
|---------|------|------|
| ArkTS 语法规则 | `/mnt/data/c00810129/.claude/skills/ArkTS_Dyn_Syntax_Rules_Complete.md` | 完整的 ArkTS 语法规则 |
| 通用配置 | `references/subsystems/_common.md` | 全局通用配置 |

## 五、版本历史

- **v1.0.0** (2025-02-02):
  - 初始版本
  - 定义 ArkTS 子系统通用配置
  - 整理 ArkTS 编译错误级别规则（共 70+ 条规则）
  - 明确无需生成测试用例的场景
  - 提供 ArkTS 特有代码模板
