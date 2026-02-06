# 代码模板库

> **模块信息**
> - 层级：L3_Generation
> - 优先级：按需加载
> - 适用范围：测试代码模板
> - 依赖：L1_Framework

---

## 一、模板概述

本模块提供各种测试用例的代码模板，包括基础测试文件模板、参数测试模板、错误码测试模板、返回值测试模板、异步测试模板等。

---

## 二、测试文件头模板

### 2.1 Apache 2.0 许可证头部

```typescript
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
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
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
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

import {describe, it, expect, Level} from '@ohos/hypium';
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
 * @tc.name test{MethodName}{ParamType}{Scenario}001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_{PARAM}_{SCENARIO}_001
 * @tc.desc 测试 {API} 的 {method} 方法 - {scenario}场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}{ParamType}{Scenario}001', Level.LEVEL1, () => {
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

  try {
    apiObject.methodName(null);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(expectedErrorCode);
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

  try {
    apiObject.methodName(undefined);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(expectedErrorCode);
  }
});
```

---

## 五、错误码测试模板

> **重要**：错误码测试模板中的 `{expectedErrorCode}` 必须从 API 的 `@throws` 标记中提取，**不能假设所有参数错误都抛出 401**。

### 5.1 同步方法错误码测试

```typescript
/**
 * @tc.name test{MethodName}Error{Code}001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ERROR_{CODE}_001
 * @tc.desc 测试 {API} 的 {method} 方法 - 错误码 {Code}：{触发条件}
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Error{Code}001', Level.LEVEL2, () => {
  let apiObject = new APIName();

  // 准备触发错误码的条件

  try {
    apiObject.methodName(invalidParam);
    expect().assertFail();
  } catch (error) {
    // 验证错误码
    expect(error.code).assertEqual(errorCode);
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

### 7.1 Promise.then/.catch 测试

```typescript
/**
 * @tc.name test{AsyncMethod}001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_001
 * @tc.desc 测试 {API} 的 {asyncMethod} 方法 - 正常场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{AsyncMethod}001', Level.LEVEL1, async (done: Function) => {
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
 * @tc.name test{AsyncMethod}Error{Code}001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ERROR_{CODE}_001
 * @tc.desc 测试 {API} 的 {asyncMethod} 方法 - 错误码 {code}
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{AsyncMethod}Error{Code}001', Level.LEVEL2, async (done: Function) => {
  let apiObject = new APIName();
  let invalidParam: ParamType = invalidValue;

  apiObject.asyncMethod(invalidParam)
    .then((result: ReturnType) => {
      expect().assertFail();
      done();
    })
    .catch((error: BusinessError) => {
      expect(error.code).assertEqual(expectedErrorCode);
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

使用模板时需要替换以下变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| {APIName} | API 名称 | TreeSet |
| {MethodName} | 方法名称 | add, popFirst |
| {ParamType} | 参数类型 | String, Number, Null |
| {Scenario} | 测试场景 | Normal, Null, Undefined, Boundary |
| {子系统} | 子系统名 | UTILS, NETWORK |
| {模块} | 模块名 | UTIL, HTTP |
| {Code} | 错误码 | 401, 10200010, 8300001 |
| {ReturnType} | 返回值类型 | boolean, string, T \| undefined |
| {ParamType} | 参数类型 | string, number, boolean |
| {expectedValue} | 期望值 | 具体值 |
| {expectedErrorCode} | 期望错误码（从 @throws 提取） | 401, 10200010, 8300001 |

> **重要说明**：
> - `{Code}` 和 `{expectedErrorCode}` 必须从 API 的 `@throws` 标记中提取
> - 不同 API 的错误码可能不同，不能假设所有参数错误都抛出 401
> - 错误码参考：通用错误码（`docs/en/application-dev/onlyfortest/reference/errorcode-universal.md`）和子系统特有错误码（`docs/zh-cn/application-dev/reference/apis-xxx/errorcode-xxx.md`）

---

## 十、模板使用示例

### 10.1 完整示例

输入：
- API: TreeSet
- Method: add
- Param Type: string
- Scenario: normal

替换后：

```typescript
/**
 * @tc.name testAddStringNormal001
 * @tc.number SUB_UTILS_UTIL_TREESET_ADD_STRING_NORMAL_001
 * @tc.desc 测试 TreeSet 的 add 方法 - string类型正常值场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testAddStringNormal001', Level.LEVEL1, () => {
  let treeSet = new TreeSet<string>();
  let paramValue: string = "hello";

  let result: boolean = treeSet.add(paramValue);

  expect(result).assertTrue();
});
```

---

## 十一、UiTest 测试模板

> 本章节提供 UiTest 框架相关的测试模板，用于测试 UI 界面相关的 API。

### 11.1 UiTest 测试文件结构

```typescript
/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
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

import {describe, beforeAll, afterAll, it, expect, Level} from '@ohos/hypium';
import {Driver, ON} from '@ohos.UiTest';
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

  afterAll(async (done: Function) => {
    await driver.close();
    done();
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

### 12.1 始终使用 waitForComponent

```typescript
// ✅ 正确 - 使用 waitForComponent
const component = await driver.waitForComponent(ON.id('test-id'), 2000);
if (component) {
  // 测试逻辑
}

// ❌ 错误 - 使用固定延时
await Utils.sleep(1000);
const component = await driver.findComponent(ON.id('test-id'));
```

### 12.2 必须判空

```typescript
// ✅ 正确 - 所有 findComponent 必须判空
const component = await driver.findComponent(ON.id('xxx'));
if (component) {
  await component.click();
} else {
  expect().assertFail();
}

// ❌ 错误 - 不判空
const component = await driver.findComponent(ON.id('xxx'));
await component.click();
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

### 12.4 测试套件内共享 Driver

```typescript
// ✅ 正确 - 共享 Driver
describe('Test', () => {
  let driver: Driver;

  beforeEach(async () => {
    driver = await Driver.create();
  });

  it('test1', async () => {
    await driver!.findComponent(ON.id('xxx'));
  });
});

// ❌ 错误 - 多个 Driver 实例
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
