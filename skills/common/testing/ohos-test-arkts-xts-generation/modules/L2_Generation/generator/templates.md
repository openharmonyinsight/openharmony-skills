# 代码模板库

> **模块信息**
> - 层级：L2_Generation
> - 优先级：按需加载
> - 适用范围：测试代码模板
> - 依赖：conventions

---

## 一、模板概述

本模块提供各种测试用例的代码模板，包括基础测试文件模板、参数测试模板、错误码测试模板、返回值测试模板、异步测试模板等。

---

## 二、测试文件头模板

### 2.1 Apache 2.0 许可证头部

```typescript
/*
 * Copyright (c) {YEAR} Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
```

---

## 三、完整测试文件模板

### 3.1 API 测试文件

```typescript
// ... Apache 2.0 license header (see §2.1) ...

import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';
import {APIName} from '@kit.BaseKitName'; // 根据实际模块修改

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
}
```

---

## 四、参数测试模板

### 4.1 基础参数测试

```typescript
/**
 * @tc.name test{MethodName}{ParamType}{Scenario}0001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_{PARAM}_{SCENARIO}_0001
 * @tc.desc 测试 {API} 的 {method} 方法 - {scenario}场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}{ParamType}{Scenario}0001', Level.LEVEL1, () => {
  // 1. 准备测试数据
  let apiObject = new APIName();
  let paramValue: ParamType = normalValue;

  // 2. 执行测试
  let result: ReturnType = apiObject.methodName(paramValue);

  // 3. 验证结果
  expect(result).assertEqual(expectedValue);
});
```

### 4.2 null 参数测试

```typescript
/**
 * @tc.name test{MethodName}Null001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_NULL_001
 * @tc.desc 测试 {API} 的 {method} 方法 - null参数场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Null001', Level.LEVEL2, () => {
  let apiObject = new APIName();
  let errCode{CodeName} = {Code};

  try {
    apiObject.methodName(null);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(errCode{CodeName});
  }
});
```

### 4.3 undefined 参数测试

```typescript
/**
 * @tc.name test{MethodName}Undefined001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_UNDEFINED_001
 * @tc.desc 测试 {API} 的 {method} 方法 - undefined参数场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Undefined001', Level.LEVEL2, () => {
  let apiObject = new APIName();
  let errCode{CodeName} = {Code};

  try {
    apiObject.methodName(undefined);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(errCode{CodeName});
  }
});
```

---

## 五、错误码测试模板

> **重要**：错误码测试模板中的 `{expectedErrorCode}` 必须从 API 的 `@throws` 标记中提取，**不能假设所有参数错误都抛出 401**。

### 5.1 同步方法错误码测试

```typescript
/**
 * @tc.name test{MethodName}Error{Code}0001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ERROR_{CODE}_0001
 * @tc.desc 测试 {API} 的 {method} 方法 - 错误码 {Code}：{触发条件}
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Error{Code}0001', Level.LEVEL2, () => {
  let apiObject = new APIName();
  let errCode{CodeName} = {Code};

  // 准备触发错误码的条件

  try {
    apiObject.methodName(invalidParam);
    expect().assertFail();
  } catch (error) {
    // 验证错误码
    expect(error.code).assertEqual(errCode{CodeName});
  }
});
```

---

## 六、返回值测试模板

### 6.1 基础返回值测试

```typescript
/**
 * @tc.name test{MethodName}Return001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_RETURN_001
 * @tc.desc 测试 {API} 的 {method} 方法 - 返回值验证
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}Return001', Level.LEVEL1, () => {
  let apiObject = new APIName();
  let result: ReturnType = apiObject.methodName(validParam);

  // 验证返回值类型
  expect(typeof result).assertEqual('string');

  // 验证返回值
  expect(result).assertEqual(expectedValue);
});
```

### 6.2 联合类型返回值测试

```typescript
/**
 * @tc.name test{MethodName}ReturnUnion001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_RETURN_UNION_001
 * @tc.desc 测试 {API} 的 {method} 方法 - 联合类型返回值
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}ReturnUnion001', Level.LEVEL1, () => {
  let apiObject = new APIName();
  let result: ReturnType = apiObject.methodName(validParam);

  // 验证可能的类型
  if (result !== null && result !== undefined) {
    expect(typeof result).assertEqual('string');
  }
});
```

---

## 七、异步方法测试模板

> **重要**：所有异步模板必须使用 `async (done: Function)` 回调形式，且 `.then` 和 `.catch` 分支都必须调用 `done()`。（缺少 `done()` 的分支会导致测试无限挂起直到超时，测试运行器资源被占用，且超时错误掩盖了真实的测试意图）

### 7.0.1 异步模板通用反模式

```typescript
// ❌ 反模式1：缺少 async 关键字（Promise 可能未执行完就退出）
it('testAsync001', Level.LEVEL1, (done: Function) => {  // 缺少 async！
  api.method(param)
    .then((result) => { expect(result); done(); })
    .catch((error: BusinessError) => { expect().assertFail(); done(); });
});

// ❌ 反模式2：使用 function 表达式（ArkTS 禁止）
it('testAsync001', Level.LEVEL1, async function(done: Function) { ... });

// ❌ 反模式3：同步 catch 带类型注解（ArkTS 不允许）
it('testSync001', Level.LEVEL1, () => {
  try { api.method(); } catch (error: BusinessError) { ... }  // 同步 catch 不能带类型
});
// ✅ 异步 .catch 可以带类型：(error: BusinessError) => { ... }
// ✅ 同步 catch 不能带类型：catch (error) { ... }

// ❌ 反模式4：同步 it() 中使用 done 参数（导致并发问题）
it('testSync001', Level.LEVEL1, (done: Function) => {  // 同步回调不需要 done
  let result = api.syncMethod();
  expect(result).assertEqual(expected);
  done();  // 多余！可能导致并发问题
});
// ✅ 正确：同步 it() 不要声明 done 参数
it('testSync001', Level.LEVEL1, () => {
  let result = api.syncMethod();
  expect(result).assertEqual(expected);
});
```

### 7.1 Promise.then/.catch 测试

```typescript
/**
 * @tc.name test{AsyncMethod}0001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_0001
 * @tc.desc 测试 {API} 的 {asyncMethod} 方法 - 正常场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{AsyncMethod}0001', Level.LEVEL1, async (done: Function) => {
  let apiObject = new APIName();
  let param: ParamType = validParam;

  apiObject.asyncMethod(param)
    .then((result: ReturnType) => {
      // 验证返回值
      expect(result).assertEqual(expectedValue);
      done();
    })
    .catch((error: BusinessError) => {
      console.error('Test FAILED: ' + error.message);
      expect().assertFail();
      done();
    });
});
```

### 7.2 异步方法错误码测试

```typescript
/**
 * @tc.name test{AsyncMethod}Error{Code}0001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ERROR_{CODE}_0001
 * @tc.desc 测试 {API} 的 {asyncMethod} 方法 - 错误码 {code}
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{AsyncMethod}Error{Code}0001', Level.LEVEL2, async (done: Function) => {
  let apiObject = new APIName();
  let errCode{CodeName} = {Code};
  let invalidParam: ParamType = invalidValue;

  apiObject.asyncMethod(invalidParam)
    .then((result: ReturnType) => {
      expect().assertFail();
      done();
    })
    .catch((error: BusinessError) => {
      expect(error.code).assertEqual(errCode{CodeName});
      done();
    });
});
```

---

## 八、边界值测试模板

### 8.1 最小边界值测试

```typescript
/**
 * @tc.name test{MethodName}BoundaryMin001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_BOUNDARY_MIN_001
 * @tc.desc 测试 {API} 的 {method} 方法 - 最小边界值
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}BoundaryMin001', Level.LEVEL2, () => {
  let apiObject = new APIName();
  let minValue: number = Number.MIN_SAFE_INTEGER;
  let result: ReturnType = apiObject.methodName(minValue);
  expect(result).assertEqual(expectedValue);
});
```

### 8.2 最大边界值测试

```typescript
/**
 * @tc.name test{MethodName}BoundaryMax001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_BOUNDARY_MAX_001
 * @tc.desc 测试 {API} 的 {method} 方法 - 最大边界值
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}BoundaryMax001', Level.LEVEL2, () => {
  let apiObject = new APIName();
  let maxValue: number = Number.MAX_SAFE_INTEGER;
  let result: ReturnType = apiObject.methodName(maxValue);
  expect(result).assertEqual(expectedValue);
});
```

---

## 九、模板变量说明

> **重要说明**：
> - `{Code}` 和 `{expectedErrorCode}` 必须从 API 的 `@throws` 标记中提取
> - 不同 API 的错误码可能不同，不能假设所有参数错误都抛出 401
> - 错误码参考：通用错误码（`docs/en/application-dev/onlyfortest/reference/errorcode-universal.md`）和子系统特有错误码（`docs/zh-cn/application-dev/reference/apis-xxx/errorcode-xxx.md`）

---

## 十一、UiTest 测试模板

> 本章节提供 UiTest 框架相关的测试模板，用于测试 UI 界面相关的 API。

### 11.1 UiTest 测试文件结构

```typescript
// ... Apache 2.0 license header (see §2.1) ...

import {describe, beforeAll, afterAll, it, expect, Level} from '@ohos/hypium';
import {Driver, ON} from '@ohos.UiTest';  // ⚠️ 注意：必须使用大写 T
import Utils from '../common/Utils';

export default function UiTestApiTest() {
  let driver: Driver;

  beforeAll(async (done: Function) => {
    await Utils.pushPage('MainAbility/pages/TestPage', done);
    await Utils.sleep(1000);
    driver = await Driver.create();
    await Utils.sleep(1000);
    done();
  });

  afterAll(() => {
    // Driver 使用完成后自动销毁，无需手动关闭
  });

  describe('UiTestApiTest', () => {
    // UiTest API 测试用例
  });
}
```

### 11.2 Driver.findComponent 测试模板

```typescript
/**
 * @tc.name testFindComponentById001
 * @tc.number SUB_UTILS_UITEST_DRIVER_FINDCOMPONENT_ID_001
 * @tc.desc 测试 Driver 的 findComponent 方法 - 按id查找控件
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testFindComponentById001', Level.LEVEL1, async (done: Function) => {
  const component = await driver.findComponent(ON.id('test-id'));

  if (component) {
    const text = await component.getProperty('text');
    expect(text).assertEqual('expected text');
  } else {
    expect().assertFail();
  }

  done();
});
```

### 11.3 Driver.waitForComponent 测试模板（推荐）

```typescript
/**
 * @tc.name testWaitForComponent001
 * @tc.number SUB_UTILS_UITEST_DRIVER_WAITFORCOMPONENT_001
 * @tc.desc 测试 Driver 的 waitForComponent 方法 - 轮询等待控件出现
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testWaitForComponent001', Level.LEVEL1, async (done: Function) => {
  // 使用 waitForComponent 在 2000ms 内轮询查找组件
  const component = await driver.waitForComponent(ON.id('test-id'), 2000);

  if (component) {
    const text = await component.getProperty('text');
    expect(text).assertEqual('expected text');
  } else {
    console.error('Test FAILED: Component not found!');
    expect().assertFail();
  }

  done();
});
```

### 11.4 Component.getProperty 测试模板

```typescript
/**
 * @tc.name testGetProperty001
 * @tc.number SUB_UTILS_UITEST_COMPONENT_GETPROPERTY_001
 * @tc.desc 测试 Component 的 getProperty 方法 - 获取字符串属性
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testGetProperty001', Level.LEVEL1, async (done: Function) => {
  const component = await driver.waitForComponent(ON.id('text-id'), 2000);

  if (component) {
    // getProperty 返回 string 类型
    const text = await component.getProperty('text');
    const fontSize = await component.getProperty('fontSize');
    const enabled = await component.getProperty('enabled');

    // 使用 assertEqual 比较字符串
    expect(text).assertEqual('expected text');
    expect(fontSize).assertEqual('16.00fp');
    expect(enabled).assertEqual('true');
  } else {
    expect().assertFail();
  }

  done();
});
```

### 11.5 Component 操作测试模板

```typescript
/**
 * @tc.name testComponentClick001
 * @tc.number SUB_UTILS_UITEST_COMPONENT_CLICK_001
 * @tc.desc 测试 Component 的 click 方法
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testComponentClick001', Level.LEVEL1, async (done: Function) => {
  const component = await driver.waitForComponent(ON.id('button-id'), 2000);

  if (component) {
    await component.click();
    await Utils.sleep(500);

    const clicked = await component.getProperty('clicked');
    expect(clicked).assertEqual('true');
  } else {
    expect().assertFail();
  }

  done();
});
```

---

## 十二、UiTest 测试最佳实践

> Driver 共享规范（beforeAll 创建、禁止 close 等）详见 `references/conventions/uitest_framework.md` 第八章。

### 12.1 `@tc` 注释块与 `it()` 之间禁止空行

（`@tc` 注解解析器通过紧邻关系将注释块与 `it()` 关联。空行会导致 `@tc` 元数据不被识别，测试报告中心无法匹配用例编号和描述）

```typescript
// ❌ 错误 - */ 和 it() 之间有空行（@tc 块不会被识别）
/**
 * @tc.name testMethod001
 * @tc.number SUB_MODULE_API_METHOD_PARAM_001
 * @tc.desc 测试描述
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */

it('testMethod001', Level.LEVEL1, () => { ... });

// ✅ 正确 - */ 紧跟 it()
/**
 * @tc.name testMethod001
 * @tc.number SUB_MODULE_API_METHOD_PARAM_001
 * @tc.desc 测试描述
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testMethod001', Level.LEVEL1, () => { ... });
```

### 12.3 getProperty 返回值是字符串

```typescript
// ✅ 正确 - 使用 assertEqual 比较字符串
const enabled = await component.getProperty('enabled');
expect(enabled).assertEqual('true');

// ❌ 错误 - 不要使用 assertTrue
const enabled = await component.getProperty('enabled');
expect(enabled).assertTrue(); // 错误！enabled 是字符串
```

### 12.4 禁止多个 describe 创建多个 Driver 实例

```typescript
// ❌ 错误 - 多个 Driver 实例会冲突
describe('Test1', () => {
  let driver = await Driver.create();
});
describe('Test2', () => {
  let driver = await Driver.create(); // 冲突！
});
```

---

## 十三、UiTest 测试模板变量说明

使用 UiTest 模板时需要替换以下变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| {组件id} | 组件的唯一标识 | 'button-id', 'text-input' |
| {组件类型} | 组件的类型 | 'Button', 'Text', 'TextInput' |
| {属性名} | 组件的属性名 | 'text', 'fontSize', 'enabled' |
| {属性值} | 期望的属性值（字符串） | 'hello', '16.00fp', 'true' |
| {子系统} | UiTest 子系统 | UTILS |
| {模块} | UiTest 模块 | UITEST |
