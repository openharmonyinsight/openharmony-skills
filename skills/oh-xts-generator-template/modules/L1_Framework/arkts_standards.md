# ArkTS 语法规范

> **模块信息**
> - 层级：L1_Framework
> - 优先级：必须加载
> - 适用范围：所有XTS测试
> - 依赖：无

---

## 一、ArkTS 语法要求

### 1.1 禁用的语法特性

| 语法特性 | 状态 | 说明 |
|---------|------|------|
| 函数表达式 `function() {}` | ❌ 禁用 | 使用箭头函数 |
| `any`、`unknown` 类型 | ❌ 禁用 | 必须指定具体类型 |
| 同步 catch 的类型注解 | ❌ 禁用 | `catch (error)` 而非 `catch (error: Error)` |
| `null as unknown` | ❌ 禁用 | 直接使用 `null` |

### 1.2 强制要求的语法

| 语法特性 | 说明 |
|---------|------|
| 箭头函数 | 必须使用箭头函数 |
| 显式类型注解 | 所有变量、函数参数必须有类型 |
| 回调函数类型 | `done: Function` |
| 异步 catch 类型 | `(error: BusinessError)` |
| 业务错误类型 | `import { BusinessError } from '@kit.BasicServicesKit'` |

---

## 二、导入语句规范

### 2.1 标准导入

```typescript
// 测试框架导入（必需）
import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';

// 根据测试类型选择性导入
import {Driver, ON} from '@ohos.UiTest';  // ArkUI 组件测试
import {BusinessError} from '@kit.BasicServicesKit';  // 错误处理
import {APIName} from '@kit.BaseKitName';  // 被测 API

// 工具类
import Utils from '../common/Utils';
```

### 2.2 模块导入合并

如果被测对象涉及的导入模块在同一包名中，请做合并：

```typescript
// ✅ 正确 - 合并导入
import {TreeSet, TreeMap, List} from '@kit.ArkTS';

// ❌ 错误 - 分散导入
import {TreeSet} from '@kit.ArkTS';
import {TreeMap} from '@kit.ArkTS';
import {List} from '@kit.ArkTS';
```

---

## 三、函数语法要求

### 3.1 使用箭头函数

```typescript
// ✅ 正确 - 使用箭头函数
it('test001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
  let value: number = 10;
  expect(value).assertEqual(10);
});

// ❌ 错误 - 使用函数表达式
it('test001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, function() {
  let value = 10;
  expect(value).assertEqual(10);
});
```

### 3.2 显式类型注解

```typescript
// ✅ 正确 - 显式类型注解
let numValue: number = 10;
let strValue: string = "test";
let boolValue: boolean = true;
let objValue: Object = {};

// 回调函数类型
beforeAll((done: Function) => {
  // 测试准备
  done();
});

// ❌ 错误 - 类型推导或any
let numValue = 10;  // 缺少类型注解
let anyValue: any = 10;  // 使用了any
```

---

## 四、null/undefined 处理

### 4.1 传入 null/undefined

```typescript
// ✅ 正确 - 直接传入
api.methodName(null);
api.methodName(undefined);

// ❌ 错误 - 类型转换
api.methodName(null as unknown);  // 不要这样做
api.methodName(undefined as SomeType);  // 不要这样做
```

### 4.2 判断 null/undefined

```typescript
// ✅ 正确
if (result !== null && result !== undefined) {
  expect(result).assertEqual(expected);
}

// ✅ 使用断言取反
expect(result).not().assertNull();
expect(result).not().assertUndefined();

// ❌ 错误 - 使用不存在的断言方法
expect(result).assertNotNull();  // 不存在此方法
expect(result).assertNotUndefined();  // 不存在此方法
```

---

## 五、异步操作处理

### 5.1 异步方法（Promise）

```typescript
// ✅ 正确 - Promise.then/.catch
it('asyncMethodTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: Function) => {
  api.asyncMethod(param)
    .then((result) => {
      expect(result).assertEqual(expected);
      done();
    })
    .catch((error: BusinessError) => {
      expect(error.code).assertEqual(expectedCode);
      done();
    });
});

// ✅ 正确 - async/await
it('asyncMethodTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: Function) => {
  try {
    let result: ReturnType = await api.asyncMethod(param);
    expect(result).assertEqual(expected);
    done();
  } catch (error) {
    // await 的 catch 不带类型注解
    expect(error.code).assertEqual(expectedCode);
    done();
  }
});
```

### 5.2 同步方法（try/catch）

```typescript
// ✅ 正确 - 同步方法的 catch 不带类型注解
it('syncMethodTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
  try {
    api.syncMethod(param);
    expect().assertFail();  // 不应该到达
  } catch (error) {
    // 同步 catch 不带类型
    expect(error.code).assertEqual(expectedCode);
  }
});

// ❌ 错误 - 同步方法 catch 带类型注解
it('syncMethodTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
  try {
    api.syncMethod(param);
  } catch (error: BusinessError) {  // ❌ 同步catch不要带类型
    expect(error.code).assertEqual(expectedCode);
  }
});
```

---

## 六、测试套组织

### 6.1 测试套件命名

```typescript
// ✅ 正确
export default function TreeSetTest() { }
export default function TreeSetCompleteTest() { }

// ArkUI 组件测试必须以 Acts 开头
export default function ActsTextTest() { }
```

### 6.2 测试套件组织

```typescript
export default function APINameTest() {
  describe('APINameParameterTest', () => {
    // 参数测试用例
  });

  describe('APINameErrorCodeTest', () => {
    // 错误码测试用例
  });

  describe('APINameReturnValueTest', () => {
    // 返回值测试用例
  });

  describe('APINameBoundaryTest', () => {
    // 边界值测试用例
  });
}
```

---

## 七、接口调用规范

### 7.1 静态方法 vs 实例方法

```typescript
// 静态方法 - 直接通过模块名调用
import {StaticAPI} from '@kit.SomeKit';
let result = StaticAPI.staticMethod();

// 实例方法 - 需要先创建实例
import {InstanceAPI} from '@kit.SomeKit';
let api = new InstanceAPI();
let result = api.instanceMethod();
```

### 7.2 模块导入示例

```typescript
// 根据实际API所在的模块修改导入语句
import {TreeSet, TreeMap, List} from '@kit.ArkTS';
import {http} from '@kit.NetworkKit';
import {relationalStore} from '@kit.ArkData';
import {picker} from '@kit.CoreFileKit';
```
