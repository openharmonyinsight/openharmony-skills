# 测试约定和命名规范

> **模块信息**
> - 层级：conventions（跨层共享）
> - 优先级：按需加载
> - 适用范围：所有XTS测试
> - 依赖：无

---

## 一、测试用例编号规范

### 1.1 编号格式

```
SUB_[子系统]_[模块]_[API]_[类型]_[序号]
```

> **重要**：`@tc.number` 必须在全局（跨文件）唯一。生成前应检查目标目录中已有测试文件的编号，避免冲突。（重复的 @tc.number 会导致测试报告系统中后注册的用例覆盖先注册的，覆盖率统计丢失实际测试数据）

### 1.1.1 编号全局唯一性反模式

```typescript
// ❌ 反模式：不同文件中复用 @tc.number
// FileA.test.ets
* @tc.number SUB_UTILS_UTIL_TREESET_ADD_PARAM_0001

// FileB.test.ets（另一个文件）
* @tc.number SUB_UTILS_UTIL_TREESET_ADD_PARAM_0001  // 重复！

// ✅ 正确：确保全局唯一，检查已有文件后从新序号开始
```

### 1.2 类型标识

| 标识 | 说明 | 示例 |
|------|------|------|
| PARAM | 参数测试 | SUB_UTILS_UTIL_TREESET_ADD_PARAM_0001 |
| ERROR | 错误码测试 | SUB_UTILS_UTIL_TREESET_POPFIRST_ERROR_401_0001 |
| RETURN | 返回值测试 | SUB_UTILS_UTIL_TREESET_GETFIRST_RETURN_0001 |
| BOUNDARY | 边界值测试 | SUB_UTILS_UTIL_TREESET_ADD_BOUNDARY_0001 |

### 1.3 子系统和模块识别

> **重要**：严禁仅根据 API 名称推测子系统归属，必须通过 SDK 分析确认（错误的子系统归属会导致：测试文件放在错误目录无法编译、@tc.number 前缀错误导致报告归档失败、覆盖率统计无法正确归属）

识别方法：
1. 在 `interface` 目录下查找 API 定义文件
2. 参考 `docs` 目录下对应子系统的开发指南
3. 确认 API 所属的 Kit 模块

常见子系统：
- UTILS - 工具类（@kit.ArkTS）
- NETWORK - 网络（@kit.NetworkKit）
- DATA - 数据（@kit.ArkData）
- FILE - 文件（@kit.CoreFileKit）
- GRAPHICS - 图形（@kit.ArkGraphics）
- UI - UI组件（@kit.ArkUI）

---

## 二、测试用例命名规范

### 2.1 测试函数命名

```typescript
// 格式: test[MethodName][Scenario][Number]
it('testAdd001', Level.LEVEL1, () => {});
it('testAddNull002', Level.LEVEL2, () => {});
it('testPopFirstError401001', Level.LEVEL2, () => {});
```

### 2.1.1 测试命名描述性反模式

```typescript
// ❌ 反模式：无描述性命名（纯编号）
it('test001', Level.LEVEL1, () => { ... });
it('test002', Level.LEVEL1, () => { ... });

// ❌ 反模式：过于通用的命名
it('testMethod001', Level.LEVEL1, () => { ... });

// ✅ 正确：描述性命名（包含方法名和场景）
it('testAddStringNormal001', Level.LEVEL1, () => { ... });
it('testAddStringNull002', Level.LEVEL2, () => { ... });
```

### 2.2 测试套件命名

```typescript
// API 测试
describe('APINameParameterTest', () => {});
describe('APINameErrorCodeTest', () => {});
describe('APINameReturnValueTest', () => {});

// ArkUI 组件测试（必须以 Acts 开头）
describe('ActsComponentNamePropertyTest', () => {});
describe('ActsComponentNameMethodTest', () => {});
describe('ActsComponentNameEventTest', () => {});
```

---

## 三、JSDoc 注释规范

### 3.1 标准注释模板

```typescript
/**
 * @tc.name [测试名称]
 * @tc.number [用例编号]
 * @tc.desc [测试描述]
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
  // 测试逻辑
});
```

### 3.2 注释字段说明

| 字段 | 可选值 |
|------|------|
| @tc.type | FUNCTION, PERFORMANCE, RELIABILITY, SECURITY, COMPATIBILITY |
| @tc.size | SMALLTEST, MEDIUMTEST, LARGETEST |
| @tc.level | LEVEL0, LEVEL1, LEVEL2, LEVEL3, LEVEL4 |

---

## 四、测试文件命名和组织

### 4.1 测试文件命名

```typescript
// API 测试文件
APIName.test.ets          // 示例：TreeSet.test.ets
APINameTest.test.ets      // 示例：TreeSetTest.test.ets

// ArkUI 组件测试文件
Acts[Component]Test.test.ets  // 示例：ActsTextTest.test.ets
```

### 4.2 测试文件结构

```typescript
/*
 * Copyright (c) {YEAR} Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * ...
 */

import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';
import {APIName} from '@kit.BaseKitName';

export default function APINameTest() {
  describe('APINameParameterTest', () => {
    // 参数测试
  });

  describe('APINameErrorCodeTest', () => {
    // 错误码测试
  });

  describe('APINameReturnValueTest', () => {
    // 返回值测试
  });
}
```

### 4.2.1 测试文件大小反模式

> 单个 `.test.ets` 文件建议不超过 30-50 个 `it()` 用例。超过时应按方法/功能拆分为多个文件。

```
// ❌ 反模式：单个文件包含 100+ 个 it() 用例
TreeSetAll.test.ets（2000+ 行）

// ✅ 正确：按功能拆分
TreeSetAdd.test.ets      — add 方法测试
TreeSetRemove.test.ets   — remove 方法测试
TreeSetQuery.test.ets    — 查询方法测试
```

---

## 五、测试场景覆盖要求

### 5.1 参数测试场景

| 参数类型 | 必须测试的场景 |
|---------|---------------|
| string | 正常值、空字符串、null、undefined、超长字符串 |
| number | 正数、负数、0、null、undefined、边界值 |
| boolean | true、false、null、undefined |
| 枚举 | 每个枚举值、null、undefined、无效值 |
| 数组 | 空数组、非空数组、null、undefined、边界长度 |
| 对象 | 正常对象、null、undefined、缺少属性、类型错误 |

### 5.2 测试用例检查点

- **正常场景**：检查调用该接口后，能完成接口描述的功能
- **异常场景**：检查能抛出对应场景的错误码

---

## 六、测试覆盖率要求

### 6.1 方法覆盖

对所有方法均需要设计测试用例进行覆盖。

### 6.2 参数场景覆盖

根据接口的不同参数类型设计测试场景，确保：
- 每个参数类型都有对应的测试用例
- 边界值和异常值都有覆盖
- null 和 undefined 都有测试

### 6.3 错误码覆盖

获取每个接口的错误码，一个错误码需构造一条独立的测试用例。

---

## 七、输出文件规范

### 7.1 代码格式

2 空格缩进，120 字符行宽，测试用例间空一行。

### 7.2 导入语句顺序

```typescript
// 1. 单元测试框架导入
import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium';

// 2. 测试框架相关导入（如 UiTest）
import {Driver, ON} from '@ohos.UiTest';

// 3. 公共模块导入
import {BusinessError} from '@kit.BasicServicesKit';
import {hilog} from '@kit.PerformanceAnalysisKit';

// 4. 被测API导入
import {APIName} from '@kit.BaseKitName';

// 5. 工具类导入
import Utils from '../common/Utils';
```
### 7.3 测试文件头部版权

每个测试文件**必须**包含 Apache 2.0 许可证头部，Copyright (c) {YEAR} Huawei Device Co., Ltd.（完整文本见 `templates.md` §2.1）。
