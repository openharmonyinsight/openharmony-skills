# 测试用例生成策略

> **模块信息**
> - 层级：L3_Generation
> - 优先级：按需加载
> - 适用范围：测试用例生成
> - 依赖：L1_Framework, L2_Analysis

---

## 一、模块概述

测试用例生成器根据 API 定义和测试策略，自动生成符合 XTS 规范的测试用例代码。

---

## 二、参数测试用例生成

### 2.1 参数类型测试规则

| 参数类型 | 必须测试的场景 | 生成的测试用例数 |
|---------|---------------|----------------|
| **string** | 正常值、空字符串、null、undefined、超长字符串 | 5-6 个 |
| **number** | 正数、负数、0、null、undefined、边界值 | 6-7 个 |
| **boolean** | true、false、null、undefined | 4 个 |
| **枚举** | 每个枚举值、null、undefined、无效值 | 枚举值+2 个 |
| **数组** | 空数组、非空数组、null、undefined、边界长度 | 5-6 个 |
| **对象** | 正常对象、null、undefined、缺少属性、类型错误 | 5-6 个 |

### 2.2 参数测试用例模板

```typescript
/**
 * @tc.name {MethodName}{ParamType}{Scenario}001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_{PARAM}_{SCENARIO}_001
 * @tc.desc 测试 {API} 的 {method} 方法 - {scenario}场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}{ParamType}{Scenario}001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
  // 1. 准备测试数据
  let apiObject = new APIName();
  let paramValue = /* 根据场景设置 */;

  // 2. 执行测试
  let result = apiObject.methodName(paramValue);

  // 3. 验证结果
  expect(result).assertEqual(expectedValue);
});
```

### 2.3 参数测试场景示例

#### string 类型

```typescript
// 正常值
it('testAddStringNormal001', Level.LEVEL1, () => {
  let treeSet = new TreeSet<string>();
  let result = treeSet.add("hello");
  expect(result).assertTrue();
});

// 空字符串
it('testAddStringEmpty002', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  let result = treeSet.add("");
  expect(result).assertTrue();
});

// null - 必须根据 API 的 @throws 标记确定实际的错误码
it('testAddStringNull003', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  try {
    treeSet.add(null);
    expect().assertFail();
  } catch (error) {
    // 从 @throws 标记中提取实际的错误码
    expect(error.code).assertEqual({actualErrorCode});
  }
});

// undefined - 必须根据 API 的 @throws 标记确定实际的错误码
it('testAddStringUndefined004', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  try {
    treeSet.add(undefined);
    expect().assertFail();
  } catch (error) {
    // 从 @throws 标记中提取实际的错误码
    expect(error.code).assertEqual({actualErrorCode});
  }
});
```

#### number 类型

```typescript
// 正常值
it('testAddNumberNormal001', Level.LEVEL1, () => {
  let treeSet = new TreeSet<number>();
  let result = treeSet.add(100);
  expect(result).assertTrue();
});

// 零值
it('testAddNumberZero002', Level.LEVEL1, () => {
  let treeSet = new TreeSet<number>();
  let result = treeSet.add(0);
  expect(result).assertTrue();
});

// 负数
it('testAddNumberNegative003', Level.LEVEL1, () => {
  let treeSet = new TreeSet<number>();
  let result = treeSet.add(-100);
  expect(result).assertTrue();
});

// 边界值
it('testAddNumberBoundary004', Level.LEVEL2, () => {
  let treeSet = new TreeSet<number>();
  let result = treeSet.add(Number.MAX_SAFE_INTEGER);
  expect(result).assertTrue();
});
```

---

## 三、错误码测试用例生成

### 3.1 错误码触发条件

> **重要**：必须从 API 的 `@throws` 标记中提取**实际的错误码**，而不是假设所有参数错误都抛出 401。

从 `@throws` 标记中提取错误码及其触发条件：

```typescript
/**
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 401 - Parameter error. Possible causes: 1. Mandatory parameters are left unspecified; 2. Incorrect parameter types.
 * @throws { BusinessError } 10200010 - Container is empty.
 * @throws { BusinessError } 8300001 - Invalid parameter value.
 */
method(param: ParamType): ReturnType;
```

**错误码解析原则**：
1. 读取 `.d.ts` 文件中该 API 的 `@throws` 标记
2. 提取所有声明的错误码及其触发条件
3. 根据触发条件设计测试场景
4. 每个错误码生成对应的测试用例

**错误码参考**：
- **通用错误码**：`docs/en/application-dev/onlyfortest/reference/errorcode-universal.md`
  - 201: Permission Denied
  - 202: Permission Verification Failed for Calling a System API
  - 401: Parameter Check Failed
  - 801: API Not Supported
- **子系统特有错误码**：`docs/zh-cn/application-dev/reference/apis-xxx/errorcode-xxx.md`

### 3.2 错误码测试模板

```typescript
/**
 * @tc.name test{MethodName}Error{Code}001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ERROR_{CODE}_001
 * @tc.desc 测试 {API} 的 {method} 方法 - 错误码 {code}：{触发条件}
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Error{Code}001', Level.LEVEL2, () => {
  try {
    // 1. 准备会触发错误码的条件
    let apiObject = new APIName();
    // 设置会触发错误码的状态或参数（根据 @throws 中的触发条件）

    // 2. 执行会触发错误码的操作
    apiObject.methodName(invalidParam);

    // 3. 如果没有抛出错误，测试失败
    expect().assertFail();
  } catch (error) {
    // 4. 验证错误码（使用从 @throws 中提取的实际错误码）
    expect(error.code).assertEqual({actualErrorCode}); // 使用实际错误码，而非固定的 401
  }
});
```

### 3.3 错误码测试示例

#### 3.3.1 示例 1：Utils API - 401 参数错误

```typescript
/**
 * API 声明：
 * @throws { BusinessError } 401 - Parameter error.
 */
function popFirst(): T;

/**
 * @tc.name testPopFirstError401001
 * @tc.number SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_401_001
 * @tc.desc 测试 TreeSet 的 popFirst 方法 - 容器为空时抛出 401
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testPopFirstError401001', Level.LEVEL2, () => {
  let treeSet = new TreeSet<number>();

  try {
    // 空容器调用 popFirst，触发 401 错误
    let result = treeSet.popFirst();
    expect().assertFail();
  } catch (error) {
    // 验证错误码 401（从 @throws 中提取）
    expect(error.code).assertEqual(401);
  }
});
```

#### 3.3.2 示例 2：Utils API - 10200010 容器为空

```typescript
/**
 * API 声明：
 * @throws { BusinessError } 10200010 - Container is empty.
 */
function popLast(): T;

/**
 * @tc.name testPopLastError10200010001
 * @tc.number SUB_UTILS_UTIL_TREESET_POPLAST_ERROR_10200010_001
 * @tc.desc 测试 TreeSet 的 popLast 方法 - 容器为空时抛出 10200010
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testPopLastError10200010001', Level.LEVEL2, () => {
  let treeSet = new TreeSet<number>();

  try {
    // 空容器调用 popLast，触发 10200010 错误
    let result = treeSet.popLast();
    expect().assertFail();
  } catch (error) {
    // 验证错误码 10200010（从 @throws 中提取）
    expect(error.code).assertEqual(10200010);
  }
});
```

#### 3.3.3 示例 3：Network API - 多种错误码

```typescript
/**
 * API 声明：
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 202 - Non-system applications use system APIs.
 * @throws { BusinessError } 401 - Parameter error.
 * @throws { BusinessError } 2100001 - Invalid parameter value.
 */
function createNetConnection(): void;

/**
 * @tc.name testCreateNetConnectionError201001
 * @tc.number SUB_NETWORK_NETCONNECTION_CREATENETCONNECTION_ERROR_201_001
 * @tc.desc 测试 createNetConnection - 权限被拒绝时抛出 201
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testCreateNetConnectionError201001', Level.LEVEL2, () => {
  try {
    // 无权限调用，触发 201 错误
    let connection = connection.createNetConnection();
    expect().assertFail();
  } catch (error) {
    // 验证错误码 201
    expect(error.code).assertEqual(201);
  }
});

/**
 * @tc.name testCreateNetConnectionError401001
 * @tc.number SUB_NETWORK_NETCONNECTION_CREATENETCONNECTION_ERROR_401_001
 * @tc.desc 测试 createNetConnection - 参数错误时抛出 401
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testCreateNetConnectionError401001', Level.LEVEL2, () => {
  try {
    // 参数错误，触发 401 错误
    let connection = connection.createNetConnection(invalidParam);
    expect().assertFail();
  } catch (error) {
    // 验证错误码 401
    expect(error.code).assertEqual(401);
  }
});
```

### 3.4 参数测试中的错误码处理

在参数测试中，对于 null/undefined 等异常参数，**必须根据 API 的 @throws 标记确定实际的错误码**：

```typescript
// ❌ 错误：假设所有参数错误都抛出 401
it('testAddStringNull003', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  try {
    treeSet.add(null);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(401); // 错误：假设了固定错误码
  }
});

// ✅ 正确：根据 @throws 标记使用实际错误码
/**
 * API 声明：
 * @throws { BusinessError } 401 - Parameter error.
 */
it('testAddStringNull003', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  try {
    treeSet.add(null);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(401); // 正确：从 @throws 中提取
  }
});

// ✅ 正确：如果 API 抛出不同的错误码
/**
 * API 声明：
 * @throws { BusinessError } 10200001 - The value of ${param} is out of range.
 */
it('testAddInvalidParam004', Level.LEVEL2, () => {
  let treeSet = new TreeSet<string>();
  try {
    treeSet.add(invalidValue);
    expect().assertFail();
  } catch (error) {
    expect(error.code).assertEqual(10200001); // 正确：使用实际的错误码
  }
});
```

---

## 四、返回值测试用例生成

### 4.1 返回值类型验证

```typescript
// 基础类型
it('test{MethodName}Return001', Level.LEVEL1, () => {
  let apiObject = new APIName();
  let result = apiObject.methodName();

  // 验证类型
  expect(typeof result).assertEqual('string');

  // 验证值
  expect(result).assertEqual(expectedValue);
});

// 联合类型
it('test{MethodName}Return002', Level.LEVEL1, () => {
  let apiObject = new APIName();
  let result = apiObject.methodName();

  // 验证可能的类型
  if (result !== null && result !== undefined) {
    expect(typeof result).assertEqual('string');
    expect(result.length).assertLarger(0);
  }
});

// Promise 类型
it('test{MethodName}Return003', Level.LEVEL1, async (done: Function) => {
  let apiObject = new APIName();

  apiObject.methodName()
    .then((result) => {
      expect(result).assertEqual(expectedValue);
      done();
    })
    .catch((error: BusinessError) => {
      expect().assertFail();
      done();
    });
});
```

### 4.2 返回值测试场景

| 返回值类型 | 测试场景 |
|-----------|---------|
| string | 返回空字符串、返回非空字符串、返回特定格式 |
| number | 返回0、返回正数、返回负数、返回边界值 |
| boolean | 返回 true、返回 false |
| 数组 | 返回空数组、返回单元素数组、返回多元素数组 |
| 对象 | 返回 null、返回包含所有属性的对象、返回部分属性的对象 |
| T \| undefined | 返回有效值、返回 undefined |

---

## 五、边界值测试用例生成

### 5.1 边界值识别

| 参数类型 | 边界值 |
|---------|-------|
| number | Number.MIN_SAFE_INTEGER, Number.MAX_SAFE_INTEGER, 0, -1, 1 |
| string | 空字符串、最大长度、特殊字符 |
| 数组 | 空数组、单元素、最大长度 |
| 集合 | 空集合、单元素、最大容量 |

### 5.2 边界值测试模板

```typescript
/**
 * @tc.name test{MethodName}Boundary001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_BOUNDARY_001
 * @tc.desc 测试 {API} 的 {method} 方法 - 最小边界值
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Boundary001', Level.LEVEL2, () => {
  let minValue = /* 计算最小边界值 */;
  let apiObject = new APIName();
  let result = apiObject.methodName(minValue);
  expect(result).assertEqual(expectedValue);
});
```

---

## 六、完整测试套件生成

### 6.1 测试套件组织

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

### 6.2 生成优先级

1. **Level0/Level1**：基本功能和常用输入（优先）
2. **Level2**：错误场景（次优先）
3. **Level3/Level4**：边缘场景（可选）

---

## 七、生成输出格式

### 7.1 完整测试文件

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
import {APIName} from '@kit.BaseKitName';

export default function APINameTest() {
  describe('APINameParameterTest', () => {
    // 参数测试用例...
  });

  describe('APINameErrorCodeTest', () => {
    // 错误码测试用例...
  });

  describe('APINameReturnValueTest', () => {
    // 返回值测试用例...
  });
}
```

### 7.2 测试用例清单

生成测试用例后，应输出清单：

```markdown
# 生成的测试用例清单

## 参数测试 (5 个)
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_001 - 正常值
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_002 - null
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_003 - undefined
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_004 - 边界值
- SUB_UTILS_UTIL_TREESET_ADD_PARAM_005 - 超长字符串

## 错误码测试 (2 个)
- SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_401_001 - 容器为空
- SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_402_001 - 参数无效

## 返回值测试 (3 个)
- SUB_UTILS_UTIL_TREESET_GETFIRST_RETURN_001 - 返回有效值
- SUB_UTILS_UTIL_TREESET_GETFIRST_RETURN_002 - 返回 undefined
- SUB_UTILS_UTIL_TREESET_GETFIRST_RETURN_003 - 返回值类型验证

总计: 10 个测试用例
```
