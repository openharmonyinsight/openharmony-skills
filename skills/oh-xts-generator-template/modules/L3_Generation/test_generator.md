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
 * @tc.name {MethodName}{ParamType}{Scenario}0001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_{PARAM}_{SCENARIO}_0001
 * @tc.desc 测试 {API} 的 {method} 方法 - {scenario}场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}{ParamType}{Scenario}0001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
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
 * @tc.name test{MethodName}Error{Code}0001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ERROR_{CODE}_0001
 * @tc.desc 测试 {API} 的 {method} 方法 - 错误码 {code}：{触发条件}
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Error{Code}0001', Level.LEVEL2, () => {
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

## 七、测试设计文档生成

### 7.1 测试设计文档同步生成原则

在生成测试用例的同时，**必须**同步生成测试设计文档，确保：

1. **一一对应关系**：每个测试用例都有对应的测试设计文档
2. **内容一致性**：设计文档内容必须与测试用例实现保持一致
3. **版本同步**：测试用例修改时，设计文档必须同步更新
4. **命名规范**：设计文档文件名为 `{测试文件名}.design.md`

### 7.2 测试设计文档生成流程

```
生成测试用例
    ↓
提取测试用例关键信息
    ├─ 测试用例编号
    ├─ 测试用例名称
    ├─ 测试类型和级别
    ├─ 测试步骤
    └─ 预期结果
    ↓
生成测试设计文档
    ├─ 填充测试场景描述
    ├─ 补充前置条件
    ├─ 详述测试步骤
    ├─ 明确预期结果
    └─ 生成变更记录
    ↓
输出测试设计文档
    └─ 保存为 {测试文件名}.design.md
```

### 7.3 测试设计文档生成模板

```markdown
# {API名称} 测试设计文档

## 测试概述

### 测试对象
- **API名称**: {完整API路径}
- **API类型**: {类/接口/函数}
- **测试文件**: {测试文件路径}
- **测试设计文档**: {设计文档路径}

### 测试目标
[测试目标和预期成果说明]

## 测试场景设计

### 场景1: {场景名称}

| 项目 | 内容 |
|------|------|
| **场景描述** | {场景详细描述} |
| **测试用例编号** | SUB_{子系统}_{模块}_{API}_{METHOD}_{TYPE}_{序号} |
| **测试用例名称** | {testCaseName} |
| **前置条件** | {前置条件说明} |
| **测试步骤** | 1. 步骤1<br>2. 步骤2<br>3. 步骤3 |
| **预期结果** | {预期结果说明} |
| **测试类型** | {FUNCTION/PERFORMANCE/SECURITY/COMPATIBILITY} |
| **测试级别** | {Level0/Level1/Level2/Level3/Level4} |
| **测试数据** | {测试输入数据说明} |

### 场景2: {场景名称}
[重复上述格式]

## 测试覆盖分析

| 测试类型 | 测试用例数 | 覆盖说明 |
|---------|-----------|---------|
| 参数测试 | XX | {说明} |
| 错误码测试 | XX | {说明} |
| 返回值测试 | XX | {说明} |
| 边界值测试 | XX | {说明} |

## 测试依赖关系

### 依赖的测试用例
- [ ] {依赖用例1}
- [ ] {依赖用例2}

### 被依赖的测试用例
- [ ] {被依赖用例1}

## 测试环境要求

- **系统版本**: OpenHarmony API {版本}
- **子系统**: {子系统名称}
- **设备类型**: {设备类型}
- **网络环境**: {网络环境说明}

## 注意事项

[测试执行过程中的注意事项和风险说明]

## 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|---------|------|
| 1.0 | YYYY-MM-DD | 初始版本 | {作者} |
```

### 7.4 测试设计文档内容生成规则

#### 7.4.1 场景描述生成规则

根据测试用例类型生成场景描述：

| 测试类型 | 场景描述模板 |
|---------|------------|
| **参数测试** | 测试 {API} 的 {method} 方法在 {参数类型}={参数值} 场景下的行为 |
| **错误码测试** | 测试 {API} 的 {method} 方法在 {触发条件} 时抛出错误码 {code} |
| **返回值测试** | 测试 {API} 的 {method} 方法的返回值类型和值 |
| **边界值测试** | 测试 {API} 的 {method} 方法在 {边界值} 边界下的行为 |

#### 7.4.2 测试步骤生成规则

从测试用例代码中提取测试步骤：

```typescript
// 示例测试用例代码
it('testAddStringNormal001', Level.LEVEL1, () => {
  let treeSet = new TreeSet<string>();
  let result = treeSet.add("hello");
  expect(result).assertTrue();
});
```

生成测试步骤：

```
1. 创建 TreeSet<string> 实例
2. 调用 add() 方法，参数为 "hello"
3. 验证返回值为 true
```

#### 7.4.3 预期结果生成规则

从测试用例代码中提取预期结果：

```typescript
expect(result).assertTrue();  // 预期结果：返回值为 true
expect(error.code).assertEqual(401);  // 预期结果：抛出错误码 401
expect(typeof result).assertEqual('string');  // 预期结果：返回值类型为 string
```

### 7.5 测试设计文档生成示例

#### 7.5.1 示例 1：参数测试设计文档

```markdown
### 场景1: 正常字符串参数

| 项目 | 内容 |
|------|------|
| **场景描述** | 测试 TreeSet 的 add 方法在参数为正常字符串时的行为 |
| **测试用例编号** | SUB_UTILS_UTIL_TREESET_ADD_PARAM_001 |
| **测试用例名称** | testAddStringNormal001 |
| **前置条件** | TreeSet 实例已创建，容器为空 |
| **测试步骤** | 1. 创建 TreeSet<string> 实例<br>2. 调用 add() 方法，参数为 "hello"<br>3. 验证返回值为 true |
| **预期结果** | 方法执行成功，返回值为 true，元素成功添加到集合中 |
| **测试类型** | FUNCTION |
| **测试级别** | Level1 |
| **测试数据** | 参数: "hello" |
```

#### 7.5.2 示例 2：错误码测试设计文档

```markdown
### 场景2: 容器为空时调用 popFirst

| 项目 | 内容 |
|------|------|
| **场景描述** | 测试 TreeSet 的 popFirst 方法在容器为空时抛出错误码 401 |
| **测试用例编号** | SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_401_001 |
| **测试用例名称** | testPopFirstError401001 |
| **前置条件** | TreeSet 实例已创建，容器为空 |
| **测试步骤** | 1. 创建 TreeSet<number> 实例<br>2. 调用 popFirst() 方法<br>3. 捕获异常并验证错误码 |
| **预期结果** | 抛出 BusinessError 异常，错误码为 401 |
| **测试类型** | FUNCTION |
| **测试级别** | Level2 |
| **测试数据** | 无需参数 |
```

### 7.6 测试设计文档更新机制

#### 7.6.1 初始生成

- 版本号：1.0
- 日期：当前日期
- 变更内容：初始版本
- 作者：生成者

#### 7.6.2 测试用例修改时更新

当测试用例修改时，必须更新测试设计文档：

```markdown
## 变更记录

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|---------|------|
| 1.0 | 2026-02-10 | 初始版本 | System |
| 1.1 | 2026-02-11 | 修改场景2的测试步骤，增加参数验证步骤 | User |
```

#### 7.6.3 新增测试用例时更新

当新增测试用例时，在测试设计文档中添加新的场景：

```markdown
### 场景3: 新增的测试场景

| 项目 | 内容 |
|------|------|
| **场景描述** | ... |
| **测试用例编号** | ... |
| ... | ... |
```

同时在变更记录中添加：

```markdown
| 1.1 | 2026-02-11 | 新增场景3：xxx测试 | User |
```

### 7.7 测试设计文档质量检查

在生成测试设计文档后，必须进行质量检查：

- ✅ 所有测试用例都有对应的设计文档
- ✅ 设计文档内容与测试用例实现一致
- ✅ 测试步骤清晰、可执行
- ✅ 预期结果明确、可验证
- ✅ 文档格式符合模板要求
- ✅ 变更记录完整

---

## 八、生成输出格式

### 8.1 完整测试文件

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

### 8.2 测试用例清单

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

### 8.3 测试设计文档输出

生成测试用例的同时，必须生成测试设计文档：

```markdown
# 生成的测试设计文档

## 测试文件: TreeSet.test.ets
## 设计文档: TreeSet.test.design.md

### 测试场景统计

| 场景类型 | 场景数 | 对应测试用例数 |
|---------|-------|--------------|
| 参数测试场景 | 5 | 5 |
| 错误码测试场景 | 2 | 2 |
| 返回值测试场景 | 3 | 3 |

### 测试设计文档内容

文档包含以下章节：
- 测试概述（测试对象、测试目标）
- 测试场景设计（所有场景的详细说明）
- 测试覆盖分析（覆盖统计）
- 测试依赖关系
- 测试环境要求
- 注意事项
- 变更记录
```
