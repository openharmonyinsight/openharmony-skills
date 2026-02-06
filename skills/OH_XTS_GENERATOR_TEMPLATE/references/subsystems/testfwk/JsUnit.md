# JsUnit 模块配置

> **模块信息**
> - 模块名称: JsUnit（单元测试框架）
> - 所属子系统: testfwk
> - Kit包: @kit.TestKit
> - API 声明文件: test/testfwk/arkxtest/jsunit/index.d.ts
> - 版本: 1.0.0
> - 更新日期: 2026-02-05

## 模块概述

JsUnit 是 OpenHarmony 的单元测试框架，提供标准的 JUnit 风格测试能力。

**重要说明**：
- JsUnit 的 API **不随 interface 仓发布**
- 声明文件位置：`${OH_ROOT}/test/testfwk/arkxtest/jsunit/index.d.ts`

### 主要功能

- 函数单元测试
- 类方法测试
- 模块功能测试
- Mock 对象和行为验证
- 性能测试支持
- Worker 测试支持

### 测试特点

- 标准 JUnit 风格
- 支持前置后置处理
- 支持测试套件组织
- 提供丰富的断言方法（20+）
- 支持复杂的 Mock 功能
- 提供 SysTestKit 和 Hypium 工具类

## 基础测试 API

**基础测试组织、生命周期、断言方法详见框架层配置**：
- **测试框架基础**：`modules/L1_Framework/hypium_framework.md`
- **断言方法列表**：18个基础断言方法（assertEqual, assertTrue, assertFalse等）
- **测试级别**：Level0-Level4
- **测试类型**：Function, Performance, Power等
- **测试粒度**：SmallTest, MediumTest, LargeTest

## JsUnit 特有 API

### 1. 特有生命周期钩子

```typescript
// JsUnit 特有：it级别生命周期
beforeEachIt(callback: Function): void
afterEachIt(callback: Function): void

// JsUnit 特有：条件生命周期（指定用例）
beforeItSpecified(testCaseNames: Array<string> | string, callback: Function): void
afterItSpecified(testCaseNames: Array<string> | string, callback: Function): void
```

**使用场景**：
- `beforeEachIt/afterEachIt`：在特定测试用例前后执行
- `beforeItSpecified/afterItSpecified`：仅对指定的测试用例执行前置/后置操作

### 2. Promise 断言（特有）

```typescript
// Promise 断言（JsUnit 扩展）
assertPromiseIsPending(): Promise<void>
assertPromiseIsRejected(): Promise<void>
assertPromiseIsRejectedWith(expectValue?: any): Promise<void>
assertPromiseIsRejectedWithError(...expectValue): Promise<void>
assertPromiseIsResolved(): Promise<void>
assertPromiseIsResolvedWith(expectValue?: any): Promise<void>
```

### 3. Mock 相关（核心功能）

```typescript
// MockKit 类
class MockKit {
  constructor()
  mockFunc(obj: Object, func: Function): Function
  mockObject(obj: Object): Object
  verify(methodName: String, argsArray: Array<any>): VerificationMode
  ignoreMock(obj: Object, func: Function | String): void
  clear(obj: Object): void
  clearAll(): void
  mockPrivateFunc(originalObject: Object, method: String): Function
  mockProperty(obj: Object, propertyName: String, value: any): void
}

// when 接口
interface when {
  afterReturn(value: any): any
  afterReturnNothing(): undefined
  afterAction(action: any): any
  afterThrow(e_msg: string): string
  (argMatchers?: any): when;
}

// ArgumentMatchers 类
class ArgumentMatchers {
  static any;
  static anyString;
  static anyBoolean;
  static anyNumber;
  static anyObj;
  static anyFunction;
  static matchRegexs(Regex: RegExp): void
}

// VerificationMode 接口
interface VerificationMode {
  times(count: Number): void
  never(): void
  once(): void
  atLeast(count: Number): void
  atMost(count: Number): void
}
```

### 4. 测试工具类（特有）

```typescript
// SysTestKit 类 - 测试辅助工具
class SysTestKit {
  static getDescribeName(): string;
  static getItName(): string;
  static getItAttribute(): TestType | Size | Level
  static actionStart(tag: string): void
  static actionEnd(tag: string): void
  static existKeyword(keyword: string, timeout?: number): boolean
  static clearLog(): boolean
}

// Hypium 类 - 高级测试功能
class Hypium {
  static setData(data: { [key: string]: any }): void
  static setTimeConfig(systemTime: any)
  static hypiumTest(abilityDelegator: any, abilityDelegatorArguments: any, testsuite: Function): void
  static set(key: string, value: any): void
  static get(key: string): any
  static registerAssert(customAssertion: Function): void
  static unregisterAssert(customAssertion: string | Function): void
  static hypiumWorkerTest(abilityDelegator: Object, abilityDelegatorArguments: Object, testsuite: Function, workerPort: Object): void;
  static hypiumInitWorkers(abilityDelegator: Object, scriptURL: string, workerNum: number, params: Object): void;
}
```

### 5. 枚举常量

```typescript
// 测试类型枚举（详见 hypium_framework.md）
enum TestType {
  FUNCTION = 0B1,
  PERFORMANCE = 0B1 << 1,
  POWER = 0B1 << 2,
  RELIABILITY = 0B1 << 3,
  SECURITY = 0B1 << 4,
  GLOBAL = 0B1 << 5,
  COMPATIBILITY = 0B1 << 6,
  USER = 0B1 << 7,
  STANDARD = 0B1 << 8,
  SAFETY = 0B1 << 9,
  RESILIENCE = 0B1 << 10
}

// 测试规模枚举（详见 hypium_framework.md）
enum Size {
  SMALLTEST = 0B1 << 16,
  MEDIUMTEST = 0B1 << 17,
  LARGETEST = 0B1 << 18
}

// 测试级别枚举（详见 hypium_framework.md）
enum Level {
  LEVEL0 = 0B1 << 24,
  LEVEL1 = 0B1 << 25,
  LEVEL2 = 0B1 << 26,
  LEVEL3 = 0B1 << 27,
  LEVEL4 = 0B1 << 28
}
```

## 参考资料配置

**参考文档路径**：
```
API 参考: ${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-test-kit/jsunit.md
开发指南: ${OH_ROOT}/docs/zh-cn/application-dev/application-test/
框架基础: modules/L1_Framework/hypium_framework.md
```

**查找方式**：
```bash
# 方式1：从配置读取
使用本配置文件中指定的参考资料路径

# 方式2：在 docs 仓中查找
grep -r "describe" ${OH_ROOT}/docs/ | grep -i "test"
grep -r "beforeAll" ${OH_ROOT}/docs/
grep -r "MockKit" ${OH_ROOT}/docs/
```

## 代码模板

### 基础测试模板

```typescript
/**
 * @tc.name JsUnitTestSuite001
 * @tc.number SUB_ARKXTEST_JSUNIT_SUITE_001
 * @tc.desc 测试 JsUnit 测试套件功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
describe('JsUnit API Test', () => {
  beforeAll(() => {
    // 测试套初始化
  });

  afterAll(() => {
    // 测试套清理
  });

  /**
   * @tc.name testMethod001
   * @tc.number SUB_ARKXTEST_JSUNIT_METHOD_001
   * @tc.desc 测试 JsUnit 方法功能
   */
  it('testMethod001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
    // 测试代码
    let result = apiObject.methodName();
    expect(result).assertEqual(expectedValue);
  });
});
```

### Mock 测试模板（核心）

```typescript
/**
 * @tc.name testMockVerify001
 * @tc.number SUB_ARKXTEST_JSUNIT_MOCK_001
 * @tc.desc 测试 MockKit 对象验证
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testMockVerify001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, () => {
  // 1. 创建 Mock 对象
  let mockKit = new MockKit();
  let mockObj = mockKit.mockObject(originalObject);

  // 2. 设置 Mock 行为
  when(mockObj.methodName('param')).afterReturn(expectedValue);

  // 3. 执行测试
  let result = mockObj.methodName('param');

  // 4. 验证结果
  expect(result).assertEqual(expectedValue);

  // 5. 验证方法调用
  mockKit.verify(mockObj.methodName, ['param']).times(1);
});
```

### 条件生命周期模板（特有）

```typescript
/**
 * @tc.name testBeforeItSpecified001
 * @tc.number SUB_ARKXTEST_JSUNIT_CONDITIONAL_LIFECYCLE_001
 * @tc.desc 测试条件生命周期钩子
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
describe('Conditional Lifecycle Test', () => {
  // 仅在指定测试用例前执行
  beforeItSpecified(['testSpecialCase'], () => {
    console.log('Setup for special test case');
  });

  it('testNormalCase', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
    // 不会触发 beforeItSpecified
    expect(true).assertTrue();
  });

  it('testSpecialCase', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, () => {
    // 会触发 beforeItSpecified
    expect(true).assertTrue();
  });
});
```

### Promise 断言模板（特有）

```typescript
/**
 * @tc.name testPromiseAssertion001
 * @tc.number SUB_ARKXTEST_JSUNIT_PROMISE_001
 * @tc.desc 测试 Promise 断言
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testPromiseAssertion001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, async () => {
  // 测试 Promise resolved
  await expect(promiseResult).assertPromiseIsResolvedWith(expectedValue);

  // 测试 Promise rejected
  await expect(promiseError).assertPromiseIsRejectedWithError('Error message');
});
```

### SysTestKit 工具类模板

```typescript
/**
 * @tc.name testSysTestKit001
 * @tc.number SUB_ARKXTEST_JSUNIT_SYSTESTKIT_001
 * @tc.desc 测试 SysTestKit 工具类
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('testSysTestKit001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, () => {
  // 获取当前测试信息
  let describeName = SysTestKit.getDescribeName();
  let itName = SysTestKit.getItName();
  let attributes = SysTestKit.getItAttribute();

  console.log(`Describe: ${describeName}, It: ${itName}`);
  console.log(`Attributes: ${JSON.stringify(attributes)}`);

  // 使用 actionStart/actionEnd 标记操作
  SysTestKit.actionStart('API_CALL');
  let result = apiObject.methodName();
  SysTestKit.actionEnd('API_CALL');

  // 验证结果
  expect(result).assertNotNull();
});
```

## 测试覆盖目标

| API 类型 | 最低覆盖率要求 | 推荐覆盖率 |
|---------|--------------|----------|
| JsUnit 核心 API | 90% | 100% |
| Mock 功能 | 85% | 95% |
| Promise 断言 | 80% | 90% |

## 通用配置继承

本模块继承 testfwk/_common.md 的通用配置：
- API Kit 映射
- 测试路径规范
- 参数测试规则
- 错误码测试规则

模块级配置可以覆盖通用配置的特定部分。

## 版本历史

- **v1.1.0** (2026-02-05): 删除重复内容，添加对 hypium_framework.md 的引用
- **v1.0.0** (2026-02-05): 从 _common.md 拆分，初始版本
