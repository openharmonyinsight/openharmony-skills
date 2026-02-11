# ArkTS静态语言规范常见陷阱和解决方案

本文档记录了在编写ArkTS静态语言XTS测试用例时常见的规范违反问题和解决方案，帮助避免重复犯错。

## 目录

1. [类型定义位置](#类型定义位置)
2. [类型兼容性问题](#类型兼容性问题)
3. [特殊类型处理](#特殊类型处理)
4. [编译错误代码](#编译错误代码)

---

## 类型定义位置

### 规则1: 不允许在函数内部定义类

**错误代码**: ESE0087 - Property 'xxx' does not exist on type

**❌ 错误示例**:
```typescript
it('test001', TestType.FUNCTION, () => {
  class MyClass {
    constructor(public value: number) {}
  }
  // 使用MyClass
});
```

**✅ 正确示例**:
```typescript
// 在文件最外层定义类
class MyClass {
  public value: number;

  constructor(value: number) {
    this.value = value;
  }
}

it('test001', TestType.FUNCTION, () => {
  // 使用MyClass
});
```

**说明**:
- ArkTS静态语言要求所有类定义必须在文件最外层
- 不允许在函数、方法或其他嵌套作用域中定义类
- 如果需要自引用类型（如链表节点），必须显式声明属性，不能使用构造函数参数简写

---

### 规则2: 不允许在函数内部定义函数

**错误代码**: ESE0143 - Unresolved reference 'xxx'

**❌ 错误示例**:
```typescript
it('test002', TestType.FUNCTION, () => {
  function f() {}
  function g() {}

  expect(f == f).assertEqual(true);
  expect(f == g).assertEqual(false);
});
```

**✅ 正确示例**:
```typescript
// 在文件最外层定义函数
function f(): void {}
function g(): void {}

it('test002', TestType.FUNCTION, () => {
  expect(f == f).assertEqual(true);
  expect(f == g).assertEqual(false);
});
```

**说明**:
- ArkTS静态语言要求所有函数定义必须在文件最外层
- 不允许在函数内部定义嵌套函数
- 辅助函数应该定义在主导出函数之前

---

### 规则3: 不允许在函数内部定义枚举

**错误代码**: ESE0143 - Unresolved reference 'xxx'

**❌ 错误示例**:
```typescript
it('test003', TestType.FUNCTION, () => {
  enum E { A = 1, B = 2 }
  enum S { A = "x", B = "y" }

  expect(E.A == E.A).assertEqual(true);
  expect(S.A == S.B).assertEqual(false);
});
```

**✅ 正确示例**:
```typescript
// 在文件最外层定义枚举
enum E { A = 1, B = 2 }
enum S { A = "x", B = "y" }

it('test003', TestType.FUNCTION, () => {
  expect(E.A == E.A).assertEqual(true);
  expect(S.A == S.B).assertEqual(false);
});
```

**说明**:
- ArkTS静态语言要求所有枚举定义必须在文件最外层
- 包括数值枚举和字符串枚举
- 枚举命名应该清晰明确

---

### 规则4: 不允许在函数内部定义类型别名

**错误代码**: ESE0371 - Cannot find type 'xxx'

**❌ 错误示例**:
```typescript
it('test004', TestType.FUNCTION, () => {
  type T = number | string;
  type U = boolean | string;

  let x: T = "hello";
  let y: U = "world";
});
```

**✅ 正确示例**:
```typescript
// 在文件最外层定义类型别名
type T = number | string;
type U = boolean | string;

it('test004', TestType.FUNCTION, () => {
  let x: T = "hello";
  let y: U = "world";
});
```

**说明**:
- ArkTS静态语言要求所有类型别名必须在文件最外层定义
- 包括联合类型、交叉类型等复杂类型别名
- 类型别名命名应该具有描述性

---

## 类型兼容性问题

### 问题1: 不同预定义类型之间的比较

**错误代码**: ESE0105 - Operator '==' cannot be applied to types 'xxx' and 'yyy'

**❌ 错误示例**:
```typescript
// int 与 string 比较
let a: int = 5;
let b: string = "hello";
expect(a == b).assertEqual(false);  // 编译错误

// number 与 boolean 比较
let x: number = 1;
let y: boolean = true;
expect(x == y).assertEqual(false);  // 编译错误

// bigint 与 number 比较
let big: bigint = 10n;
let num: number = 10;
expect(big == num).assertEqual(false);  // 编译错误
```

**✅ 正确示例**:
```typescript
// 1. 只比较相同类型
let a: int = 5;
let b: int = 10;
expect(a == b).assertEqual(false);  // ✓

// 2. 使用联合类型声明
function compare<T>(a: T, b: T): boolean {
  return a == b;
}
expect(compare<number>(5, 10)).assertEqual(false);

// 3. 显式类型转换（如果语义上合理）
let big: bigint = 10n;
let num: number = 10;
expect(big == BigInt(num)).assertEqual(true);  // 转换为bigint
expect(Number(big) == num).assertEqual(true);  // 转换为number
```

**说明**:
- ArkTS静态语言不允许不同预定义类型之间直接使用相等运算符
- 包括：int vs string, number vs boolean, bigint vs number等
- 如果必须比较，应使用显式类型转换

---

### 问题2: Object类型的装箱值比较

**错误代码**: ESE0105 - Operator '==' cannot be applied to types 'Int' and '"hello"'

**❌ 错误示例**:
```typescript
it('testObjectComparison', TestType.FUNCTION, () => {
  let obj1: Object = 5;          // number装箱
  let obj2: Object = 5;          // number装箱
  let obj3: Object = "hello";    // string装箱

  expect(obj1 == obj3).assertEqual(false);  // 编译错误!
});
```

**✅ 正确示例**:
```typescript
it('testObjectComparison', TestType.FUNCTION, () => {
  // 只比较相同类型的Object
  let numObj1: Object = 5;
  let numObj2: Object = 5;
  let strObj1: Object = "hello";
  let strObj2: Object = "hello";

  expect(numObj1 == numObj2).assertEqual(false);  // 不同引用
  expect(strObj1 == strObj2).assertEqual(false);  // 不同引用
  // 注意: 不比较number Object与string Object
});
```

**说明**:
- 虽然变量声明为Object类型，但编译器会检查装箱后的实际类型
- 不同基本类型的装箱值不能直接比较
- Object类型比较实际是比较引用，不是值

---

### 问题3: null和undefined的比较

**错误代码**: ESE0105 - Operator '==' cannot be applied to types 'null' and 'undefined'

**❌ 错误示例**:
```typescript
it('testNullUndefined', TestType.FUNCTION, () => {
  expect(null == undefined).assertEqual(true);   // 可能编译错误
  expect(null === undefined).assertEqual(false); // 可能编译错误
});
```

**✅ 正确示例**:
```typescript
it('testNullUndefined', TestType.FUNCTION, () => {
  // 使用联合类型
  let x: null | undefined = null;
  let y: null | undefined = undefined;

  expect(x == y).assertEqual(true);
  expect(x === y).assertEqual(false);
});
```

**说明**:
- null和undefined是不同的类型，直接比较可能违反类型规范
- 应使用联合类型 `null | undefined` 进行比较
- 或使用可空类型 `T | null` 和 `T | undefined`

---

### 问题4: 联合类型的交集检查

**❌ 错误示例**:
```typescript
// 无交集的联合类型比较 - 编译错误
function test1(x: number | string, y: boolean | null) {
  return x == y;  // 编译错误: number|string 与 boolean|null 无交集
}
```

**✅ 正确示例**:
```typescript
// 有交集的联合类型比较
function test2(x: number | string, y: boolean | string) {
  return x == y;  // ✓ 有string交集
}

// 使用类型守卫
function test3(x: number | string, y: boolean | null) {
  if (typeof x === 'boolean' && typeof y === 'boolean') {
    return x == y;  // 在类型守卫内比较
  }
  return false;
}
```

**说明**:
- ArkTS要求比较的联合类型必须有交集
- 如果无交集，应该使用类型守卫或分开处理

---

## 特殊类型处理

### NaN的特殊行为

**说明**:
- NaN是number类型的特殊值
- `NaN == NaN` 返回 `false`（number类型行为）
- 但如果装箱为Object，`a == a` 返回 `true`（引用相等）

**示例**:
```typescript
it('testNaN', TestType.FUNCTION, () => {
  // number类型的NaN
  let nan: number = NaN;
  expect(nan == nan).assertEqual(false);   // NaN的特殊性质

  // Object类型的NaN（装箱后）
  let objNan: Object = NaN;
  expect(objNan == objNan).assertEqual(true);  // 同一引用

  // 两个Object类型的NaN比较
  let a: Object = NaN;
  let b: Object = NaN;
  expect(a == b).assertEqual(false);  // 不同引用
});
```

---

### 数值类型的自动提升

**✅ 正确示例**:
```typescript
it('testNumericPromotion', TestType.FUNCTION, () => {
  let byteVal: byte = 5;
  let intVal: int = 5;
  let doubleVal: double = 5.0;

  // 数值类型之间可以比较（自动提升）
  expect(byteVal == intVal).assertEqual(true);
  expect(intVal == doubleVal).assertEqual(true);
});
```

**说明**:
- ArkTS允许数值类型之间的比较（byte, short, int, long, float, double）
- 比较时会自动进行类型提升
- 但number与bigint、number与boolean不能直接比较

---

## 推荐的文件结构

为了符合ArkTS静态语言规范，测试文件应该遵循以下结构：

```typescript
// 1. Import语句
import { describe, it, expect, TestType, Size, Level } from '../../hypium/index';

// 2. 辅助函数定义（最外层）
async function sleep(time: int): Promise<int> {
  // 实现
}

// 3. 类定义（最外层）
class TestClass {
  public value: number;
  constructor(value: number) {
    this.value = value;
  }
}

// 4. 接口定义（最外层）
interface ITestInterface {}

// 5. 枚举定义（最外层）
enum TestEnum { A = 1, B = 2 }

// 6. 类型别名（最外层）
type TestType = number | string;

// 7. 测试函数（最外层，如果需要）
function testHelper(): void {}

// 8. 主导出函数
export default function FeatureTest() {
  describe('FeatureName', () => {
    // beforeAll, beforeEach等

    it('test001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
      // 测试代码，使用上面定义的类型、函数、类
    });

    // 更多测试用例...
  });
}
```

---

## 编译错误代码速查表

| 错误代码 | 错误描述 | 常见原因 | 解决方案 |
|---------|---------|---------|---------|
| **ESE0087** | Property 'xxx' does not exist on type | 类中自引用类型未正确声明 | 显式声明属性，不使用构造函数参数简写 |
| **ESE0105** | Operator '==' cannot be applied to types 'X' and 'Y' | 不同预定义类型比较 | 使用类型转换或联合类型 |
| **ESE0143** | Unresolved reference 'xxx' | 函数/枚举定义在函数内部 | 移到文件最外层 |
| **ESE0371** | Cannot find type 'xxx' | 类型别名定义在函数内部 | 移到文件最外层 |

---

## 检查清单

在提交测试代码前，请检查：

- [ ] 所有类定义都在文件最外层
- [ ] 所有函数定义都在文件最外层（除了主导出函数内的it回调）
- [ ] 所有枚举定义都在文件最外层
- [ ] 所有类型别名都在文件最外层
- [ ] 没有不同预定义类型之间的直接比较（int vs string等）
- [ ] Object类型比较时，实际类型是兼容的
- [ ] null和undefined比较使用联合类型
- [ ] 联合类型比较时有类型交集
- [ ] 所有类型注解都是显式的（不使用any）

---

## 参考资源

- **ArkTS静态语言规范**: [references/arkts-static-spec/](references/arkts-static-spec/)
- **XTS格式规范**: [references/xts-format-spec.md](references/xts-format-spec.md)
- **构建工作流**: [references/build-workflow.md](references/build-workflow.md)
