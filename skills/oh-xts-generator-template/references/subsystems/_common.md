# 通用配置

> **适用范围**: 所有子系统
> **版本**: 1.8.0
> **更新日期**: 2026-02-05

## 一、通用测试规范

### 1.1 测试用例编号格式

```
格式: SUB_[子系统]_[模块]_[API]_[类型]_[序号]

类型标识：
- PARAM    参数测试
- ERROR    错误码测试
- RETURN   返回值测试
- BOUNDARY 边界值测试

示例：
SUB_UTILS_UTIL_TREESET_ADD_PARAM_001
SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_401_001
SUB_ARKUI_COMPONENT_ONCLICK_RETURN_001
```

**重要命名规范** ⭐ **强制要求**：

1. **it() 函数第一个参数（用例名称）**：
   - ✅ **必须使用小驼峰命名（camelCase）**
   - ❌ **禁止使用大写下划线命名**
   - ❌ **禁止使用特殊标点符号**（如 `[]`、`.` 等）

   **正确示例**：
   - ✅ `uitestOnText401`
   - ✅ `testScrollToTop17000002`
   - ✅ `testClick17000004`

   **错误示例**：
   - ❌ `UiTest_On_text_401`（大写下划线）
   - ❌ `testScrollToTop_17000002`（下划线分隔）
   - ❌ `test[MethodName].Param.001`（特殊标点）

2. **it() 函数第二个参数（测试类型）**：
   - ✅ **必须使用**：`TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3`
   - ❌ **禁止使用**：`0` 或其他简写形式

   **正确示例**：
   ```typescript
   it('uitestOnText401', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: Function) => {
   ```

   **错误示例**：
   ```typescript
   it('UiTest_On_text_401', 0, async (done: Function) => {
   ```

**命名转换规则**：

| 原命名格式（错误） | 正确命名格式 | 转换规则 |
|----------------|-----------|---------|
| `UiTest_On_text_401` | `uitestOnText401` | 全部小写 + 驼峰 + 移除下划线 |
| `UiTest_By_key_401` | `uitestByKey401` | 全部小写 + 驼峰 + 移除下划线 |
| `UiTest_Component_scrollToTop_speed_401` | `uitestComponentScrollToTopSpeed401` | 全部小写 + 驼峰 + 移除下划线 |
| `testScrolltotop17000004` | `testScrollToTop17000004` | 小驼峰（单词首字母大写） |
| `testDoubleclick17000002` | `testDoubleClick17000002` | 小驼峰（单词首字母大写） |
| `testGetid17000002` | `testGetId17000002` | 小驼峰（缩写词首字母大写） |

### 1.2 测试级别定义

| 级别 | 名称 | 说明 | 适用场景 |
|-----|------|------|---------|
| Level0 | 冒烟测试 | 基本功能验证 | 核心API的基本功能 |
| Level1 | 基础测试 | 常用输入场景 | 常用参数组合 |
| Level2 | 主要测试 | 常用+错误场景 | 正常+异常场景 |
| Level3 | 常规测试 | 所有功能 | 完整功能覆盖 |
| Level4 | 罕见测试 | 极端场景 | 边界值、极端输入 |

### 1.3 测试类型定义

| 类型 | 说明 | 标识 |
|-----|------|------|
| Function | 功能测试 | TestType.FUNCTION |
| Performance | 性能测试 | TestType.PERFORMANCE |
| Reliability | 可靠性测试 | TestType.RELIABILITY |
| Security | 安全测试 | TestType.SECURITY |

### 1.4 测试粒度定义

| 粒度 | 说明 | 执行时间 | 标识 |
|-----|------|---------|------|
| SmallTest | 小型测试 | < 5秒 | Size.SMALLTEST |
| MediumTest | 中型测试 | 5-30秒 | Size.MEDIUMTEST |
| LargeTest | 大型测试 | > 30秒 | Size.LARGETEST |

### 1.5 ArkTS 语法类型

OpenHarmony 的 ArkTS API 包含两种接口类型，生成测试用例前需要识别：

#### 1.5.1 API 类型判断

**判断方法**：解析 API 声明文件（`.d.ts`）中**最后一段 JSDOC** 的 `@since` 标签。

| since标签内容 | API类型 | 说明 |
|-------------|---------|------|
| 仅包含 `dynamiconly` | **动态API** | ArkTS动态语法独有接口 |
| 仅包含 `staticonly` | **静态API** | ArkTS静态语法独有接口 |
| 仅包含 `dynamic` | **动态API** | 动态语法接口，存在对应的静态语法接口 |
| 仅包含 `static` | **静态API** | 静态语法接口，存在对应的动态语法接口 |
| 多标签：同时包含 `static` 和 `dynamic` | **动态API&静态API** | 动态和静态语法中接口声明一致 |
| 单标签：包含 `dynamic&static` | **动态API&静态API** | 起始版本相同，同时支持两种语法 |

#### 1.5.2 工程语法类型识别

**识别方法**：读取工程根目录下的 `build-profile.json5` 配置文件。

**详细内容**：参见 `modules/L2_Analysis/project_parser.md` 中的"二、工程语法类型识别"章节。

```json5
{
  "app": {
    "products": [
      {
        "arkTSVersion": "1.2"  // ← 静态语法标识
      }
    ]
  }
}
```

| 配置项 | 工程类型 | 说明 |
|--------|---------|------|
| 存在 `"arkTSVersion": "1.2"` | **静态语法工程** | 使用 ArkTS 静态语法 |
| 不存在 `arkTSVersion` 字段 | **动态语法工程** | 使用 ArkTS 动态语法 |

#### 1.5.3 测试用例生成策略

| 工程类型 | API类型 | 生成策略 |
|---------|---------|---------|
| 静态语法工程 | 静态API | ✅ 直接生成 |
| 静态语法工程 | 动态API | ⚠️ 不兼容，需提示或跳过 |
| 静态语法工程 | 混合API | ✅ 生成静态调用方式 |
| 动态语法工程 | 动态API | ✅ 直接生成 |
| 动态语法工程 | 静态API | ⚠️ 不兼容，需提示或跳过 |
| 动态语法工程 | 混合API | ✅ 生成动态调用方式 |

#### 1.5.4 文件命名规则

| 工程类型 | 文件命名规则 | 用例命名规则 | 示例 |
|---------|-------------|-------------|------|
| **动态语法工程** | 保持原始文件名 | 保持原始用例名 | 文件：`uitest.test.ets`<br>用例：`it('testApi', ...)` |
| **静态语法工程** | 保持原始文件名（**无后缀**） | 用例名 + `_static` 后缀 | 文件：`uitest.test.ets`<br>用例：`it('testApi_static', ...)` |

**重要**：
- 静态语法工程的 ets 文件命名**不需要**添加 `static` 后缀
- 仅在 `it()` 中定义的用例名后添加 `_static` 后缀

### 1.6 错误码参考

> **重要**：API 在入参异常时抛出的错误码**并非相同**，必须参考 API 的 jsdoc 中 `@throws { BusinessError }` 标记的具体内容。
>
> **更新时间**: 2026-01-14 17:55

#### 1.6.1 错误码分类

OpenHarmony 的错误码分为两类：

| 错误码类型 | 说明 | 文档位置 |
|-----------|------|---------|
| **通用错误码** | 所有子系统共享的错误码 | `docs/en/application-dev/onlyfortest/reference/errorcode-universal.md` |
| **子系统特有错误码** | 特定子系统独有的错误码 | `docs/zh-cn/application-dev/reference/apis-xxx/errorcode-xxx.md` |

#### 1.6.2 通用错误码

OpenHarmony 通用错误码包括以下 5 个：

---

**201 权限校验失败**

**错误信息**
```
Permission verification failed. The application does not have the permission required to call the API.
```

**错误描述**
权限校验失败，应用无权限使用该API，需要申请权限。

**可能原因**
该错误码表示权限校验失败，通常为没有权限，却调用了需要权限的API。

**处理步骤**
请检查是否有调用API的权限。

---

**202 系统API权限校验失败**

**错误信息**
```
Permission verification failed. A non-system application calls a system API.
```

**错误描述**
权限校验失败，非系统应用使用了系统API。

**可能原因**
非系统应用，使用了系统API，请校验是否使用了系统API。

**处理步骤**
请检查是否调用了系统API，并且去掉。

---

**203 企业管理策略禁止使用此系统功能** ⭐ NEW

**错误信息**
```
This function is prohibited by enterprise management policies.
```

**错误描述**
企业管理策略禁止使用此系统功能。

**可能原因**
试图操作已被设备管理应用禁用的系统功能。

**处理步骤**
请使用 getDisallowedPolicy 接口检查该系统功能是否被禁用，并使用 setDisallowedPolicy 接口解除禁用状态。

---

**401 参数检查失败**

**错误信息**
```
Parameter error. Possible causes: 1. Mandatory parameters are left unspecified; 2. Incorrect parameter types; 3. Parameter verification failed.
```

**错误描述**
- 必填参数为空
- 参数类型不正确
- 参数校验失败

无论是同步还是异步接口，此类异常大部分都通过同步的方式抛出。

**可能原因**
- 必选参数没有传入
- 参数类型错误 (Type Error)
- 参数数量错误 (Argument Count Error)
- 空参数错误 (Null Argument Error)
- 参数格式错误 (Format Error)
- 参数值范围错误 (Value Range Error)

**处理步骤**
请检查必选参数是否传入，或者传入的参数类型是否错误。对于参数校验失败，阅读参数规格约束，按照可能原因进行排查。

---

**801 该设备不支持此API**

**错误信息**
```
Capability not supported. Failed to call the API due to limited device capabilities.
```

**错误描述**
该设备不支持此API，因此无法正常调用。

**可能原因**
可能出现该错误码的场景为：该设备已支持该API所属的Syscap，但是并不支持此API。

**处理步骤**
应避免在该设备上使用此API，或在代码中通过判断来规避异常场景下应用在不同设备上运行所产生的影响。

---

**通用错误码速查表**

| 错误码 | 错误名称 | 简要描述 |
|-------|---------|---------|
| **201** | Permission Denied | 权限校验失败，应用无权限 |
| **202** | System API Permission Failed | 非系统应用使用系统API |
| **203** | Enterprise Policy Prohibited | 企业管理策略禁止使用此功能 |
| **401** | Parameter Check Failed | 参数错误（类型、数量、格式、范围等） |
| **801** | Capability Not Supported | 设备不支持此API |

#### 1.6.3 子系统特有错误码示例

| 子系统 | 错误码范围 | 示例 | 文档 |
|-------|----------|------|------|
| **Utils** | 10200001-10200301 | 10200001: 参数范围越界<br>10200010: 容器为空 | `errorcode-utils.md` |
| **Network** | 2100001-2100003 | 2100001: Invalid parameter value<br>2100003: System internal error | `errorcode-network.md` |
| **Telephony** | 8300001-8300999 | 8300001: Invalid parameter value<br>8300002: Operation failed | `errorcode-telephony.md` |
| **Window** | 1300001-1309999 | 1300001: 重复操作<br>1300002: 窗口状态异常 | `errorcode-window.md` |

#### 1.6.4 错误码解析方法

**从 .d.ts 文件中提取**：

```typescript
/**
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 401 - Parameter error. Possible causes: 1. Mandatory parameters are left unspecified; 2. Incorrect parameter types.
 * @throws { BusinessError } 10200010 - Container is empty.
 * @throws { BusinessError } 8300001 - Invalid parameter value.
 */
function methodName(param: ParamType): ReturnType;
```

**提取信息**：
1. 读取 API 的 JSDOC 注释中的 `@throws` 标记
2. 提取所有声明的错误码及其描述
3. 根据错误码描述确定触发条件
4. 为每个错误码生成对应的测试用例

**注意事项**：
- ❌ **错误**：假设所有参数错误都抛出 401
- ✅ **正确**：读取 `@throws` 标记，使用该 API 声明的具体错误码
- 不同的 API 可能有不同的错误码，即使触发条件相似
- 生成测试用例时，必须在断言中使用从 `@throws` 中提取的实际错误码

#### 1.6.5 不同 API 的不同错误码示例

```typescript
// 示例 1：Utils TreeSet API - 参数错误抛出 401
/**
 * @throws { BusinessError } 401 - Parameter error.
 */
function popFirst(): T;

// 示例 2：Utils API - 容器为空抛出 10200010
/**
 * @throws { BusinessError } 10200010 - Container is empty.
 */
function popLast(): T;

// 示例 3：Network API - 多种错误码
/**
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 202 - Non-system applications use system APIs.
 * @throws { BusinessError } 401 - Parameter error.
 * @throws { BusinessError } 2100001 - Invalid parameter value.
 */
function createNetConnection(): void;

// 示例 4：Telephony SMS API - 多种错误码
/**
 * @throws { BusinessError } 201 - Permission denied.
 * @throws { BusinessError } 202 - Non-system applications use system APIs.
 * @throws { BusinessError } 401 - Parameter error.
 * @throws { BusinessError } 8300001 - Invalid parameter value.
 * @throws { BusinessError } 8300002 - Operation failed.
 * @throws { BusinessError } 8300003 - System internal error.
 */
function sendSms(): void;
```

## 二、通用代码模板

### 2.1 测试文件头部模板

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

import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium'
import {hilog} from '@kit.PerformanceAnalysisKit';
import {BusinessError} from '@kit.BasicServicesKit';
```

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
it('test{MethodName}{ParamType}{Scenario}001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 准备测试数据
  let apiObject = new APIName();
  let paramValue = /* 根据场景设置 */;

  // 2. 执行测试
  let result = apiObject.methodName(paramValue);

  // 3. 验证结果
  expect(result).assertEqual(expectedValue);
});
```

### 2.3 错误码测试用例模板

```typescript
/**
 * @tc.name {MethodName}Error{ErrorCode}001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ERROR_{ErrorCode}_001
 * @tc.desc 测试 {API} 的 {method} 方法 - 错误码{errorCode}场景
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Error{ErrorCode}001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, () => {
  // 1. 准备测试数据
  let apiObject = new APIName();
  let invalidParam = /* 触发错误的参数 */;

  // 2. 执行测试并捕获异常
  try {
    apiObject.methodName(invalidParam);
    expect().assertFail(); // 如果没有抛出异常，测试失败
  } catch (error) {
    // 3. 验证错误码（优先使用 err.code）
    expect(error.code).assertEqual(errorCode);
    // 可选：验证错误信息（不推荐作为主要断言）
    // expect(error.message).assertContain(expectedErrorMessage);
  }
});
```

### 2.4 异步API测试模板

#### 方式1：使用 async/await（推荐）

```typescript
/**
 * @tc.name {MethodName}Async001
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ASYNC_001
 * @tc.desc 测试 {API} 的异步方法
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}Async001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async (): Promise<void> => {
  // 1. 准备测试数据
  let apiObject = new APIName();
  let paramValue = /* 测试参数 */;

  // 2. 执行异步测试（使用 await）
  try {
    let result = await apiObject.methodName(paramValue);
    // 3. 验证结果
    expect(result).assertEqual(expectedValue);
  } catch (error: BusinessError) {
    expect().assertFail();
  }
});
```

**说明**：
- 使用 `async` 修饰：因为测试代码中使用了 `await` 关键字
- 不使用 `done()` 回调：async/await 会自动处理异步结束
- 使用 `try/catch` 进行错误捕获

#### 方式2：使用 .then()/.catch() + done()

```typescript
/**
 * @tc.name {MethodName}Async002
 * @tc.number SUB_[子系统]_[模块]_{API}_{METHOD}_ASYNC_002
 * @tc.desc 测试 {API} 的异步方法
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}Async002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, (done: Function) => {
  // 1. 准备测试数据
  let apiObject = new APIName();
  let paramValue = /* 测试参数 */;

  // 2. 执行异步测试（使用 .then()/.catch()）
  apiObject.methodName(paramValue).then((result) => {
    // 3. 验证结果
    expect(result).assertEqual(expectedValue);
    done(); // 测试结束，必须调用
  }).catch((error: BusinessError) => {
    expect().assertFail();
    done(); // 测试结束，必须调用
  });
});
```

**说明**：
- 不使用 `async` 修饰：因为测试代码中没有使用 `await` 关键字
- 使用 `done()` 回调：在 `.then()` 或 `.catch()` 中必须调用 `done()` 标识测试结束
- 使用 `.then()/.catch()` 进行异步处理

#### 使用原则

| 场景 | 使用 async | 使用 await | 使用 done() |
|-----|-----------|-----------|------------|
| 代码中有 `await` | ✅ 是 | ✅ 是 | ❌ 否 |
| 代码中无 `await`，使用 `.then()/.catch()` | ❌ 否 | ❌ 否 | ✅ 是 |
| 完全同步代码 | ❌ 否 | ❌ 否 | ❌ 否 |

## 三、通用测试规则

### 3.1 参数类型测试规则

| 参数类型 | 必须测试的场景 | 生成的测试用例数 |
|---------|---------------|----------------|
| **string** | 正常值、空字符串、null、undefined、超长字符串 | 5-6 个 |
| **number** | 正数、负数、0、null、undefined、边界值 | 6-7 个 |
| **boolean** | true、false、null、undefined | 4 个 |
| **枚举** | 每个枚举值、null、undefined、无效值 | 枚举值+2 个 |
| **数组** | 空数组、非空数组、null、undefined、边界长度 | 5-6 个 |
| **对象** | 正常对象、null、undefined、缺少属性、类型错误 | 5-6 个 |

### 3.2 错误码测试规则

- 所有声明了 `@throws` 的 API 必须有对应的错误码测试
- 错误码必须是 number 类型，禁止 string 类型
- 每个错误码至少需要一个测试用例
- **异常场景断言优先使用 `err.code`**，而非 `err.message`
  - ✅ 推荐：`expect(err.code).assertEqual(401)`
  - ⚠️ 可选：`expect(err.message).assertContain('Parameter error')`
  - 原因：错误码更稳定，错误信息可能变化

### 3.3 断言使用规则

**Hypium 支持的断言方法**（共18个）：

1. `assertClose` - 检验接近程度
2. `assertContain` - 检验包含关系
3. `assertEqual` - 检验相等
4. `assertFail` - 抛出错误
5. `assertFalse` - 检验为 false
6. `assertTrue` - 检验为 true
7. `assertInstanceOf` - 检验类型（仅基础类型）
8. `assertLarger` - 检验大于
9. `assertLess` - 检验小于
10. `assertNull` - 检验为 null
11. `assertThrowError` - 检验抛出的错误
12. `assertUndefined` - 检验为 undefined
13. `assertNaN` - 检验为 NaN
14. `assertNegUnlimited` - 检验为负无穷
15. `assertPosUnlimited` - 检验为正无穷
16. `assertDeepEquals` - 检验深度相等
17. `not` - 断言取反
18. `message` - 自定义断言信息

**重要**：
- ❌ 不要使用 `assertNotX` 形式的断言（如 `assertNotNull`）
- ✅ 使用 `not()` 方法：`expect(actualValue).not().assertNull()`
- ❌ 不要编造断言方法名
- ✅ 只使用上述18个断言方法

**代码逻辑走不到的分支断言**：
- 对于理论上不会执行到的代码分支，使用 `expect().assertFail()` 做断言终结
- 应用场景：
  - try-catch 中 catch 不应该被执行到
  - 条件分支中不应该进入的分支
  - 默认处理分支
- 示例：
  ```typescript
  // 场景1：异常捕获中的正常分支
  try {
    apiObject.method(validParam);
  } catch (err) {
    // 不应该抛出异常
    expect().assertFail();
  }

  // 场景2：条件分支
  if (result === expected) {
    expect(result).assertEqual(expected);
  } else {
    // 不应该进入此分支
    expect().assertFail();
  }

  // 场景3：默认分支
  switch (type) {
    case 'A':
      expect(type).assertEqual('A');
      break;
    case 'B':
      expect(type).assertEqual('B');
      break;
    default:
      // 不应该进入此分支
      expect().assertFail();
      break;
  }
  ```

### 3.4 代码规范要求

1. **类型注解**：ArkTS 要求显式类型注解，禁止使用 any/unknown
2. **异步处理**：
   - **async 的用法**：仅在测试业务中存在异步场景时修饰
     - ✅ 使用 async：当测试代码中使用 `await` 关键字时
     - ❌ 不使用 async：当测试代码完全是同步执行时
   - **done() 回调**：仅在不使用 `await` 的业务异步中做回调结束标识
     - ✅ 使用 done：当使用 `.then()/.catch()` 且不使用 `await` 时
     - ❌ 不使用 done：当使用 `await` 时（async/await 会自动处理）
   - 异步方法用 `.then/.catch` 或 `async/await`
   - 同步方法用 `try/catch`
3. **错误处理**：
   - 错误对象类型：`BusinessError`
   - 错误码类型：`number`
4. **命名规范**：
   - 文件名：`{APIName}.test.ets`
   - 用例名：`test{MethodName}{Scenario}{序号}`
   - 用例名称**禁止**使用特殊标点符号（如 `[]`、`.` 等）

### 3.5 测试覆盖目标

| API 类型 | 最低覆盖率要求 | 推荐覆盖率 |
|---------|--------------|----------|
| 核心API | 90% | 100% |
| 常用API | 80% | 95% |
| 普通API | 70% | 90% |
| 辅助API | 60% | 80% |

## 四、通用路径规范

### 4.1 测试路径模板

```
测试用例目录: test/xts/acts/{子系统}/test/
历史用例参考: ${OH_ROOT}/test/xts/acts/{子系统}/
API声明文件: ${OH_ROOT}/interface/sdk-js/api/@ohos.{子系统}.d.ts
文档资料: ${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-*
```

### 4.2 API 文档路径 ⭐ NEW

**强制要求**：解析 API 时，**必须**同时参考 API 声明文件（.d.ts）和 API 文档资料。

**文档路径配置**：
```
主文档路径: ${OH_ROOT}/docs/
备用文档路径: /mnt/data/c00810129/oh_0130/docs/
当前工作目录: ./docs/
```

**路径优先级**：
```
OH_ROOT 文档路径 > 备用文档路径 > 当前目录文档路径
```

**文档查找方式**：

**方式1：按子系统配置读取**（推荐）

在子系统配置文件中指定参考资料位置：

```markdown
# {子系统}/_common.md

## 参考资料配置

### 文档路径
- API 参考文档：`${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-arkui/`
- 错误码文档：`${OH_ROOT}/docs/zh-cn/application-dev/reference/errorcodes/errorcode-arkui.md`

### 重点参考文件
- `component.md` - 组件详细说明
- `container.md` - 容器组件说明
- `animator.md` - 动画接口说明
```

**优点**：
- ✅ 精确匹配子系统文档
- ✅ 可配置重点参考文件
- ✅ 提高查找效率

**方式2：根据 API 名称在 docs 仓中查找**（兜底）

```
步骤：
1. 确定要查找的 API 名称
2. 在文档路径下搜索包含该 API 名称的文件
3. 分析搜索结果，提取相关内容
```

**查找命令示例**：
```bash
# 在文档路径下搜索 API 名称
grep -r "API名称" ${OH_ROOT}/docs/

# 搜索 API 可能所在的文件
find ${OH_ROOT}/docs/ -name "*API关键字*.md"
```

**文档内容参考清单**：
1. **错误码说明**：详细的错误码描述、触发条件、处理方式
2. **使用场景**：API 的适用场景和典型用例
3. **使用限制**：API 的约束条件、权限要求、版本限制
4. **使用示例**：官方示例代码和最佳实践

### 4.3 文档查找和配置 ⭐ NEW

**策略1：从子系统配置读取**（推荐）

如果子系统配置文件中指定了参考资料：

```
步骤：
1. 读取子系统配置文件 ({Subsystem}/_common.md)
2. 查找"参考资料配置"章节
3. 获取配置的文档路径和重点参考文件
4. 加载指定的文档内容
```

**示例配置**（ArkUI 子系统）：
```markdown
# ArkUI/_common.md

## 参考资料配置

### 文档路径
- API 参考文档：`${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-arkui/`
- 错误码文档：`${OH_ROOT}/docs/zh-cn/application-dev/reference/errorcodes/errorcode-arkui.md`

### 重点参考文件
- `component.md` - 组件详细说明
- `container.md` - 容器组件说明
- `animator.md` - 动画接口说明
```

**优点**：
- ✅ 配置明确，查找高效
- ✅ 可针对子系统定制
- ✅ 支持重点参考文件

**策略2：根据 API 名称在 docs 仓中查找**（兜底）

如果子系统配置未指定，则使用全文搜索：

```
步骤：
1. 确定要查找的 API 名称（如：Column, onClick, showToast）
2. 在文档路径下搜索包含该 API 名称的文件
3. 分析搜索结果，提取相关内容
```

**查找命令示例**：
```bash
# 搜索 API 名称
grep -r "Column" ${OH_ROOT}/docs/ | grep -i "arkui"

# 搜索可能的文档文件
find ${OH_ROOT}/docs/ -name "*column*.md" -o -name "*component*.md"

# 搜索包含关键字的文档
grep -r "onClick" ${OH_ROOT}/docs/ --include="*.md"
```

**搜索结果分析**：
1. 收集所有包含 API 名称的文档文件
2. 按相关度排序（文件名包含 > 内容包含）
3. 选择最相关的文档进行解析
4. 提取错误码、使用场景、限制、示例

**策略3：按 Kit 包名查找**（辅助）

如果 API 包含 Kit 包信息：

```
步骤：
1. 确定Kit包名（如：@kit.ArkUI）
2. 在文档中搜索该 Kit 包相关的文档
3. 查找包含目标 API 的文档章节
```

**查找命令示例**：
```bash
# 搜索 Kit 包
grep -r "@kit.ArkUI" ${OH_ROOT}/docs/ --include="*.md"

# 结合 API 名称搜索
grep -r "@kit.ArkUI" ${OH_ROOT}/docs/ --include="*.md" | grep "Column"
```

### 4.4 编译路径规范

```
编译脚本: ${OH_ROOT}/test/xts/acts/build.sh
输出目录: ${OH_ROOT}/out/{product_name}/suites/acts/acts/testcases/
```

## 五、通用注意事项

1. **XTS Wiki 规范优先级**：
   - Wiki 文档规范 > 通用配置 > 子系统配置
   - 生成测试用例时，必须参考 XTS ACTS Wiki 文档

2. **测试套注册**：
   - 新增测试文件时，必须在 `List.test.ets` 中注册
   - 添加 import 语句和函数调用

3. **测试文件结构**：
   ```typescript
   describe('APIName Test', () => {
     beforeAll(() => {
       // 测试套初始化
     });

     afterAll(() => {
       // 测试套清理
     });

     it('testCase001', Level.LEVEL0, () => {
       // 测试用例
     });
   });
   ```

4. **禁止模式**：
   - ❌ 禁止使用 getSync 系统接口
   - ❌ 禁止错误码使用 string 类型
   - ❌ 禁止恒真断言
   - ❌ 禁止缺少断言

5. **ArkTS 语法类型识别**：
   - **API 类型判断**：必须读取 `.d.ts` 文件中**最后一段 JSDOC** 的 `@since` 标签
   - 一个接口可能有多条 `@since` 标签（如 `@since 11 dynamic` 和 `@since 23 static`）
   - 需要收集所有 `@since` 标签进行综合判断
   - **工程类型识别**：在已有工程中增加用例时，必须先读取 `build-profile.json5` 识别工程语法类型
   - 检查 `arkTSVersion` 字段判断是静态还是动态语法工程
   - **兼容性检查**：生成测试用例前，必须检查工程语法类型与 API 类型是否匹配
   - **文件命名**：
     - 静态语法工程的测试文件名保持原始命名（无 `_static` 后缀）
     - 静态语法工程的测试用例名需添加 `_static` 后缀
     - 动态语法工程的测试文件名和用例名均保持原始命名

6. **新增测试工程**：
   - 新增测试工程时，必须确认工程语法类型（静态/动态/两者都创建）
   - 如果 API 同时支持静态和动态语法，默认应询问用户选择
   - 如果 API 仅支持一种语法，可直接生成对应类型的工程

7. **参考已有用例** ⭐ NEW：
   - **强制要求**：生成新用例时，**必须**参考已有用例的代码风格和规范
   - **默认参考路径**：
     - 主路径：`${OH_ROOT}/test/xts/acts/`
     - 如果 `OH_ROOT` 未设置，使用：`./test/xts/acts/`
   - **指定测试套**：
     - 如果使用者指定了用例生成位置（如：`test/xts/acts/arkui/test/`）
     - 则**优先**参考该测试套中的已有用例
     - 分析该测试套的代码风格、命名规范、测试模式
   - **参考内容**：
     1. **代码风格**：缩进、命名格式、注释风格
     2. **测试结构**：describe/it 嵌套方式、beforeAll/afterAll 使用
     3. **用例编号**：SUB_xxx 格式、序号规则
     4. **断言方式**：expect 的使用模式、断言类型
     5. **错误处理**：try-catch 结构、错误码验证方式
     6. **导入语句**：import 顺序、导入方式
   - **工作流程**：
     1. 扫描指定路径（或默认路径）的已有测试文件
     2. 提取共性模式（命名、结构、断言等）
     3. 生成符合该模式的新用例
     4. 保持风格一致性
   - **示例**：
     ```
     用户指定路径: test/xts/acts/arkui/test/
     → 扫描该目录下的所有 .test.ets 文件
     → 分析代码风格和规范
     → 生成符合该风格的新用例

     用户未指定路径:
     → 使用默认路径: ${OH_ROOT}/test/xts/acts/
     → 或: ./test/xts/acts/
     → 扫描对应子系统的测试文件
     → 生成符合规范的新用例
     ```

8. **参考 API 文档** ⭐ NEW：
   - **强制要求**：解析 API 时，**必须**同时参考 API 声明文件（.d.ts）和 API 文档资料
   - **文档查找方式**：
     - **方式1**：从子系统配置读取（推荐）
       - 读取 `{Subsystem}/_common.md` 中的"参考资料配置"
       - 获取配置的文档路径和重点参考文件
       - 加载指定的文档内容
     - **方式2**：根据 API 名称在 docs 仓中查找（兜底）
       - 在文档路径下搜索包含 API 名称的文件
       - 分析搜索结果，提取相关内容
     - **方式3**：按 Kit 包名查找（辅助）
       - 搜索 Kit 包相关的文档
       - 查找包含目标 API 的文档章节
   - **文档路径**：
     - 主路径：`${OH_ROOT}/docs/`
     - 备用路径：`/mnt/data/c00810129/oh_0130/docs/`
     - 当前目录：`./docs/`
   - **路径优先级**：OH_ROOT 文档路径 > 备用文档路径 > 当前目录文档路径
   - **参考内容**：
     1. **错误码说明**：详细的错误码描述、触发条件、处理方式
     2. **使用场景**：API 的适用场景和典型用例
     3. **使用限制**：API 的约束条件、权限要求、版本限制
     4. **使用示例**：官方示例代码和最佳实践
   - **工作流程**：
     1. 解析 .d.ts 文件，获取 API 声明
     2. 优先从子系统配置读取参考资料
     3. 如果配置未指定，则根据 API 名称搜索文档
     4. 提取文档中的错误码、使用场景、限制、示例
     5. 结合文档内容生成更完善的测试用例
   - **重要性**：
     - .d.ts 文件提供 API 类型签名
     - 文档提供 API 语义和使用上下文
     - 结合两者才能生成准确的测试用例

## 六、@tc 注释块规范 ⭐ NEW

> **强制要求**：所有测试用例（`it()` 函数）**必须**在前面添加标准的 `@tc` 注释块。
>
> **参考项目**：`testfwk/uitest_errorcode`
>
> **更新日期**：2026-02-05

### 6.1 @tc 注释块标准格式

每个 `it()` 函数**必须**在前面添加以下格式的注释块：

```typescript
/**
 * @tc.name   testDelayMs17000002
 * @tc.number uitestDriverErrorTest_001
 * @tc.desc   delayMs 17000002 test.
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL3
 */
it('testDelayMs17000002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  // 测试代码
})
```

### 6.2 @tc 注释块字段说明

| 字段 | 说明 | 格式 | 示例 |
|------|------|------|------|
| `@tc.name` | 测试用例名称 | 小驼峰命名（camelCase） | `testDelayMs17000002` |
| `@tc.number` | 测试用例编号 | `{describe名}_{序号}` | `uitestDriverErrorTest_001` |
| `@tc.desc` | 测试用例描述 | `{API名} {错误码/场景} test.` | `delayMs 17000002 test.` |
| `@tc.type` | 测试类型 | `FUNCTION` / `PERFORMANCE` 等 | `FUNCTION` |
| `@tc.size` | 测试规模 | `SMALLTEST` / `MEDIUMTEST` / `LARGETEST` | `MEDIUMTEST` |
| `@tc.level` | 测试级别 | `LEVEL0` ~ `LEVEL4` | `LEVEL3` |

### 6.3 @tc.name 命名规范

**命名规则**：
- ✅ **必须使用小驼峰命名（camelCase）**
- ✅ **必须与 `it()` 函数的第一个参数完全一致**
- ✅ 格式：`test{MethodName}{ErrorCode/Scenario}{序号}`

**正确示例**：
```typescript
/**
 * @tc.name   testDelayMs17000002
 * @tc.number uitestDriverErrorTest_001
 * @tc.desc   delayMs 17000002 test.
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL3
 */
it('testDelayMs17000002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  // @tc.name 和 it() 的第一个参数完全一致
})
```

**错误示例**：
```typescript
/**
 * @tc.name   test_delay_ms_17000002
 * ...
 */
it('testDelayMs17000002', ...)  // ❌ @tc.name 使用了下划线，与 it() 参数不一致

/**
 * @tc.name   TestDelayMs17000002
 * ...
 */
it('testDelayMs17000002', ...)  // ❌ @tc.name 使用了大写开头
```

### 6.4 @tc.number 编号规范

**格式**：`{describe名}_{序号}`

**规则**：
- 序号从 001 开始，依次递增
- 序号必须补零对齐（3位数字）
- describe 名通常与 `describe()` 函数的第一个参数一致

**示例**：
```typescript
describe('uitestDriverErrorTest', () => {
  /**
   * @tc.name   testDelayMs17000002
   * @tc.number uitestDriverErrorTest_001  // ← describe 名 + 序号
   * ...
   */
  it('testDelayMs17000002', ...)

  /**
   * @tc.name   testFindComponent17000002
   * @tc.number uitestDriverErrorTest_002  // ← 序号递增
   * ...
   */
  it('testFindComponent17000002', ...)
})
```

### 6.5 @tc.desc 描述规范

**格式**：`{API名} {错误码/场景} test.`

**规则**：
- 描述必须以 `. ` 结尾（句点 + 空格）
- API 名使用小驼峰命名
- 错误码使用数字格式
- 简洁明了，一句话说明测试内容

**示例**：
```typescript
// ✅ 正确格式
@tc.desc   delayMs 17000002 test.
@tc.desc   scrollToTop 17000004 test.
@tc.desc   injectMultiPointerAction 401 test.

// ❌ 错误格式
@tc.desc   Test delayMs function.                    // ❌ 缺少错误码
@tc.desc   delayms 17000002 test                      // ❌ API 名未使用小驼峰
@tc.desc   delayMs 17000002                           // ❌ 缺少结尾的 ". "
```

### 6.6 字段值对照关系

**重要**：`@tc` 注释块的字段值必须与 `it()` 函数的参数值保持一致：

| @tc 字段 | it() 参数 | 说明 |
|----------|-----------|------|
| `@tc.name` | 第一个参数（用例名） | **必须完全一致** |
| `@tc.type` | 第二个参数中的 `TestType.XXX` | 必须一致 |
| `@tc.size` | 第二个参数中的 `Size.XXX` | 必须一致 |
| `@tc.level` | 第二个参数中的 `Level.XXX` | 必须一致 |

**示例**：
```typescript
/**
 * @tc.name   testDelayMs17000002
 * @tc.number uitestDriverErrorTest_001
 * @tc.desc   delayMs 17000002 test.
 * @tc.type   FUNCTION                           ← 对应 TestType.FUNCTION
 * @tc.size   MEDIUMTEST                         ← 对应 Size.MEDIUMTEST
 * @tc.level  LEVEL3                             ← 对应 Level.LEVEL3
 */
it('testDelayMs17000002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  // ↑ 第一参数与 @tc.name 一致
})
```

### 6.7 实际项目示例

**示例1：参数错误测试（401错误码）**
```typescript
/**
 * @tc.name   testByText401
 * @tc.number UitestBy401ErrorCode_001
 * @tc.desc   uitestByText401 test.
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL3
 */
it('testByText401', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: Function) => {
  try {
    BY.text(null);
    expect(false).assertFail();
  } catch (error) {
    expect(error.code).assertEqual(401);
  }
  done();
});
```

**示例2：异步错误测试（17000002错误码）**
```typescript
/**
 * @tc.name   testDelayMs17000002
 * @tc.number uitestDriverErrorTest_001
 * @tc.desc   delayMs 17000002 test.
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL3
 */
it('testDelayMs17000002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  console.log(`${TestTag}, test_delayMs_17000002 start`);
  try {
    driver.delayMs(waitUiReadyMs * 3);
    await sleep(100);
    await driver.delayMs(waitUiReadyMs);
    expect().assertFail();
  } catch (e) {
    console.log(`${TestTag}, test_delayMs_17000002 error is: ${JSON.stringify(e)}`);
    expect(e.code).assertEqual(AsyncErrorCode);
  }
  await sleep(waitUiReadyMs * 5);
  console.log(`${TestTag}, test_delayMs_17000002 end`);
})
```

## 七、hypium 导入规范 ⭐ NEW

> **强制要求**：所有测试文件**必须**正确导入 hypium 所需的模块和类型。
>
> **更新日期**：2026-02-05

### 7.1 标准 hypium 导入

**完整导入格式**：
```typescript
import { describe, it, expect, TestType, Level, Size } from '@ohos/hypium';
```

**包含 beforeAll 的导入**：
```typescript
import { describe, beforeAll, it, expect, TestType, Level, Size } from '@ohos/hypium';
```

### 7.2 导入项说明

| 导入项 | 用途 | 必需性 |
|--------|------|--------|
| `describe` | 定义测试套 | ✅ 必需 |
| `it` | 定义测试用例 | ✅ 必需 |
| `expect` | 断言 | ✅ 必需 |
| `TestType` | 测试类型（FUNCTION等） | ✅ 必需 |
| `Level` | 测试级别（LEVEL0-4） | ✅ 必需 |
| `Size` | 测试规模（SMALLTEST等） | ✅ 必需 |
| `beforeAll` | 测试套初始化钩子 | 条件必需 |

### 7.3 导入检查清单

生成测试文件时，必须检查并确保：

1. **基本导入**：
   - ✅ 包含 `describe, it, expect`
   - ✅ 包含 `TestType, Level, Size`

2. **条件导入**：
   - ✅ 如果测试套使用了 `beforeAll()`，必须导入 `beforeAll`
   - ✅ 如果测试套使用了 `afterAll()`，必须导入 `afterAll`
   - ✅ 如果测试套使用了 `beforeEach()`，必须导入 `beforeEach`
   - ✅ 如果测试套使用了 `afterEach()`，必须导入 `afterEach`

3. **导入顺序**：
   ```typescript
   // 推荐顺序（符合项目规范）
   import { describe, beforeAll, afterAll, it, expect, TestType, Level, Size } from '@ohos/hypium';
   ```

### 7.4 常见错误及修复

**错误1：缺少 TestType, Level, Size**
```typescript
// ❌ 错误：缺少必要的类型导入
import { describe, it, expect } from '@ohos/hypium';

it('testApi401', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  // 编译错误：TestType, Size, Level 未定义
})

// ✅ 正确：导入所有必要的类型
import { describe, it, expect, TestType, Level, Size } from '@ohos/hypium';

it('testApi401', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  // 正常工作
})
```

**错误2：缺少 beforeAll**
```typescript
// ❌ 错误：缺少 beforeAll 导入
import { describe, it, expect, TestType, Level, Size } from '@ohos/hypium';

describe('testSuite', () => {
  beforeAll(async (done: Function) => {  // 编译错误：beforeAll 未定义
    // 初始化代码
  });

  it('testCase', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
    // 测试代码
  });
})

// ✅ 正确：导入 beforeAll
import { describe, beforeAll, it, expect, TestType, Level, Size } from '@ohos/hypium';

describe('testSuite', () => {
  beforeAll(async (done: Function) => {  // 正常工作
    // 初始化代码
  });

  it('testCase', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
    // 测试代码
  });
})
```

### 7.5 自动检测和修复

**检测方法**：
```python
# 检查是否需要 TestType, Level, Size
needs_test_type = 'TestType.FUNCTION' in content or 'TestType.' in content
needs_level = 'Level.LEVEL' in content or 'Level.' in content
needs_size = 'Size.MEDIUMTEST' in content or 'Size.' in content
needs_before_all = 'beforeAll' in content
```

**修复逻辑**：
```python
# 根据代码内容确定需要导入的项
all_items = ['describe', 'it', 'expect']

if needs_test_type:
    all_items.append('TestType')
if needs_level:
    all_items.append('Level')
if needs_size:
    all_items.append('Size')
if needs_before_all:
    all_items.insert(1, 'beforeAll')  # 在 describe 后插入

# 生成导入语句
import_statement = f"import {{ {', '.join(all_items)} }} from '@ohos/hypium';"
```

## 八、版本历史

- **v1.8.0** (2026-02-05):
  - **重要更新**：@tc 注释块规范（强制要求）
  - **新增**：第六章 - @tc 注释块规范
    - 6.1 @tc 注释块标准格式
    - 6.2 @tc 注释块字段说明
    - 6.3 @tc.name 命名规范（小驼峰命名）
    - 6.4 @tc.number 编号规范
    - 6.5 @tc.desc 描述规范
    - 6.6 字段值对照关系
    - 6.7 实际项目示例
  - **新增**：第七章 - hypium 导入规范
    - 7.1 标准 hypium 导入格式
    - 7.2 导入项说明
    - 7.3 导入检查清单
    - 7.4 常见错误及修复
    - 7.5 自动检测和修复逻辑
  - **原因**：确保所有测试用例都符合 XTS 规范，包含完整的 @tc 注释块和正确的 hypium 导入
  - **参考**：基于实际项目 `testfwk/uitest_errorcode` 的规范化经验
- **v1.7.0** (2026-02-05):
  - **重要更新**：测试用例命名规范（强制要求）
  - **新增**：it() 函数第一个参数必须使用小驼峰命名（camelCase）
  - **新增**：禁止使用大写下划线命名（如 `UiTest_On_text_401`）
  - **新增**：it() 函数第二个参数必须使用完整格式
  - **新增**：禁止使用 `0` 作为第二个参数
  - **新增**：命名转换规则表（包含 6 个转换示例）
  - **完善**：1.1 测试用例编号格式章节
    - 添加详细的命名规范说明
    - 添加正确示例和错误示例对比
    - 添加代码示例展示正确的 it() 函数用法
  - **原因**：统一测试用例命名规范，提高代码可读性和一致性
  - **参考**：基于实际项目 `testfwk/uitest_errorcode` 的命名规范修改经验
- **v1.6.0** (2026-01-14):
  - **新增**：参考 API 文档功能（强制要求）
  - **新增**：解析 API 时必须同时参考 .d.ts 文件和 API 文档资料
  - **新增**：API 文档路径配置（主路径、备用路径、当前目录）
  - **新增**：文档查找方式（3种）
    - 方式1：从子系统配置读取（推荐）
    - 方式2：根据 API 名称在 docs 仓中查找（兜底）
    - 方式3：按 Kit 包名查找（辅助）
  - **新增**：文档内容参考清单（错误码、使用场景、使用限制、使用示例）
  - **新增**：通用路径规范 4.2 - API 文档路径
  - **新增**：通用路径规范 4.3 - 文档查找和配置
  - **完善**：通用注意事项第8条 - 参考 API 文档
- **v1.5.0** (2026-01-14):
  - **新增**：参考已有用例功能（强制要求）
  - **新增**：生成新用例时必须参考已有用例的代码风格和规范
  - **新增**：支持指定测试套路径，优先分析该测试套的已有用例
  - **新增**：默认参考路径配置（${OH_ROOT}/test/xts/acts/）
  - **新增**：参考内容清单（代码风格、测试结构、用例编号、断言方式、错误处理、导入语句）
  - **新增**：参考已有用例的工作流程
  - **完善**：通用注意事项第7条 - 参考已有用例
- **v1.4.0** (2026-01-14):
  - **更新**：通用错误码参考（更新时间: 2026-01-14 17:55）
  - **新增**：203 错误码 - 企业管理策略禁止使用此系统功能
  - **完善**：201 错误码 - 添加详细错误描述、可能原因、处理步骤
  - **完善**：202 错误码 - 添加详细错误描述、可能原因、处理步骤
  - **完善**：401 错误码 - 添加详细的可能原因（6种）
  - **完善**：801 错误码 - 更新错误描述和可能原因
  - **新增**：通用错误码速查表，方便快速查阅
- **v1.3.0** (2025-02-02):
  - **更新**：异常场景断言优先使用 `err.code` 而非 `err.message`
  - **更新**：用例名称禁止使用特殊标点符号（如 `[]`、`.` 等）
  - **新增**：代码逻辑走不到的分支使用 `expect().assertFail()` 做断言终结
  - **完善**：async 的用法，仅在测试业务中存在异步场景时修饰
  - **完善**：done() 的用法，仅在不使用 await 的业务异步中做回调结束标识
  - **重构**：异步API测试模板，提供 async/await 和 .then()/.catch() 两种方式
- **v1.2.0** (2025-01-31):
  - **新增**：对 `modules/L2_Analysis/project_parser.md` 的引用
  - **优化**：工程语法类型识别详细内容移至 project_parser.md 模块
  - **改进**：模块化架构，L2_Analysis 层包含完整的解析功能
- **v1.1.0** (2025-01-31):
  - **新增**：1.5 ArkTS 语法类型章节
  - **新增**：API 类型判断方法（动态 API vs 静态 API）
  - **新增**：工程语法类型识别方法
  - **新增**：测试用例生成策略
  - **新增**：文件命名规则
  - **更新**：通用注意事项，添加 ArkTS 语法类型识别注意事项
- **v1.0.0** (2025-01-31): 初始版本，定义通用测试规范和模板
