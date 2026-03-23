# Hypium 测试框架基础

> **模块信息**
> - 层级：L1_Framework
> - 优先级：必须加载
> - 适用范围：所有XTS测试
> - 依赖：无

---

## 一、Hypium 框架概述

Hypium 是 OpenHarmony 的官方测试框架，它的语法和常见开源测试框架基本相同，但是**不具备 Mock Functions 功能**。因此，对未实现的接口，不能使用 Mock 相关的能力。

---

## 二、断言方法列表

> **重要提示**：Hypium断言库当前只有以下断言方法，生成脚本时，请从以下列表中选择，**不要编造方法名**

- 断言功能列表：

| No.  | API                              | 功能说明                                                                                       |
| :--- | :------------------------------- | ---------------------------------------------------------------------------------------------- |
| 1    | assertClose                      | 检验actualvalue和expectvalue(0)的接近程度是否是expectValue(1)                                  |
| 2    | assertContain                    | 检验actualvalue中是否包含expectvalue                                                           |
| 3    | assertDeepEquals                 | @since1.0.4 检验actualvalue和expectvalue(0)是否是同一个对象                                    |
| 4    | assertEqual                      | 检验actualvalue是否等于expectvalue[0]                                                          |
| 5    | assertFail                       | 抛出一个错误                                                                                   |
| 6    | assertFalse                      | 检验actualvalue是否是false                                                                     |
| 7    | assertTrue                       | 检验actualvalue是否是true                                                                      |
| 8    | assertInstanceOf                 | 检验actualvalue是否是expectvalue类型                                                           |
| 9    | assertLarger                     | 检验actualvalue是否大于expectvalue                                                             |
| 10   | assertLess                       | 检验actualvalue是否小于expectvalue                                                             |
| 11   | assertNaN                        | @since1.0.4 检验actualvalue是否是NaN                                                           |
| 12   | assertNegUnlimited               | @since1.0.4 检验actualvalue是否等于Number.NEGATIVE_INFINITY                                    |
| 13   | assertNull                       | 检验actualvalue是否是null                                                                      |
| 14   | assertPosUnlimited               | @since1.0.4 检验actualvalue是否等于Number.POSITIVE_INFINITY                                    |
| 15   | assertPromiseIsPending           | @since1.0.4 检验actualvalue是否处于Pending状态【actualvalue为promse对象】                      |
| 16   | assertPromiseIsRejected          | @since1.0.4 检验actualvalue是否处于Rejected状态【同15】                                        |
| 17   | assertPromiseIsRejectedWith      | @since1.0.4 检验actualvalue是否处于Rejected状态，并且比较执行的结果值【同15】                  |
| 18   | assertPromiseIsRejectedWithError | @since1.0.4 检验actualvalue是否处于Rejected状态并有异常，同时比较异常的类型和message值【同15】 |
| 19   | assertPromiseIsResolved          | @since1.0.4 检验actualvalue是否处于Resolved状态【同15】                                        |
| 20   | assertPromiseIsResolvedWith      | @since1.0.4 检验actualvalue是否处于Resolved状态，并且比较执行的结果值【同15】                  |
| 21   | assertThrowError                 | 检验actualvalue抛出Error内容是否是expectValue                                                  |
| 22   | assertUndefined                  | 检验actualvalue是否是undefined                                                                 |
| 23   | not                              | @since1.0.4 断言结果取反                                                                       |


## 三、使用规则

### 3.1 断言方法选择

- ✅ Hypium框架的断言方法只能在上述列表中选择，**不要编造断言方法**
- ✅ Hypium框架的断言方法断言的使用方法请参考对应方法的使用方法示例
- ✅ 请关注使用方法示例中传递的参数，不要少传或多传参数

### 3.2 assertNotX 形式断言（重要！）

- ❌ **Hypium测试框架没有 `assertNotX` 这种断言方法**
- ❌ 不要编造使用 `assertNotNull`、`assertNotEqual` 等 `assertNotX` 形式的断言方法
- ✅ 如需判断不为空或不等于等情况，请采用 `assertX.not()` 形式：
  - 断言判断不为空：`expect(actualValue).not().assertNull()`
  - 断言判断不等于：`expect(actualValue).not().assertEqual(expectedValue)`

### 3.3 断言方法大小写

- ✅ Hypium测试框架的断言方法是区分大小写的
- ✅ 如 `assertInstanceOf`，不能写成 `assertInstanceof`

### 3.4 assertInstanceOf 的限制

- ✅ 只支持基础数据类型（如 `Number`、`String`、`Boolean`、`Object` 等基础类型）
- ❌ 不支持自定义的复杂结构体类型
- ❌ 请不要传入类似于 `"BusinessError"` 这样的自定义的复杂结构体类型
- ✅ 只支持传入类型名的字符串，不能直接传入类型

---

## 四、导入语句规范

```typescript
//测试框架导入
import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium'
//公共模块引入，按kit导入
import {hilog} from '@kit.PerformanceAnalysisKit';
import {BusinessError} from '@kit.BasicServicesKit';
//被测对象接口和参数类型对象引入
import {xx} from 'kit.xxxKit'
```

### 框架模块说明

- **describe**: 定义测试套件
- **beforeAll**: 在所有测试用例执行前执行一次
- **beforeEach**: 在每个测试用例执行前执行
- **afterEach**: 在每个测试用例执行后执行
- **afterAll**: 在所有测试用例执行后执行一次
- **it**: 定义测试用例
- **expect**: 断言期望值
- **TestType**: 测试类型枚举
- **Size**: 测试粒度枚举
- **Level**: 测试级别枚举

---

## 五、测试级别说明

- **Level0**: 冒烟测试 - 基本功能，常用输入
- **Level1**: 基础测试 - 基本功能，常用输入
- **Level2**: 主要测试 - 常用输入和错误场景
- **Level3**: 常规测试 - 所有功能，常用/非常用输入
- **Level4**: 罕见测试 - 极端异常条件下的功能

---

## 六、测试类型说明

- **Function**: 功能测试
- **Performance**: 性能测试
- **Power**: 功耗测试
- **Reliability**: 可靠性测试
- **Security**: 安全测试
- **Compatibility**: 兼容性测试

---

## 七、测试粒度说明

- **SmallTest**: 单元测试，本地 PC 运行，使用 mock
- **MediumTest**: 模块/子系统测试，真实设备运行
- **LargeTest**: 服务级别测试，类设备环境运行

---

## 八、TypeScript 类型断言规范（重要！）

### 8.1 禁止使用 as any

> **重要**：测试代码中**禁止使用** `as any` 类型断言。

| 规则 | 说明 | 示例 |
|------|------|------|
| **禁止 as any** | 不要使用 `as any` 绕过类型检查 | ❌ `await driver.method(param, null as any)` |
| **直接传入** | null 和 undefined 可以直接传入，不需要类型转换 | ✅ `await driver.method(param, null)` |
| **TypeScript 严格模式** | 遵循 TypeScript 严格类型检查 | ✅ 代码更安全、更易维护 |

### 8.2 as any 错误示例

```typescript
// ❌ 错误：使用 as any 转换
it('testMethodNull001', Level.LEVEL2, async () => {
    try {
        const driver = Driver.create();
        await driver.swipeBetween(startPoint, endPoint, null as any); // ❌ 错误：as any
        expect().assertFail();
    } catch (e) {
        expect(e.code).assertEqual(401);
    }
})
```

### 8.3 as any 正确示例

```typescript
// ✅ 正确：直接传入 null
it('testMethodNull001', Level.LEVEL2, async () => {
    try {
        const driver = Driver.create();
        await driver.swipeBetween(startPoint, endPoint, null); // ✅ 正确：直接传入 null
        expect().assertFail();
    } catch (e) {
        expect(e.code).assertEqual(401);
    }
})

// ✅ 正确：直接传入 undefined
it('testMethodUndefined002', Level.LEVEL2, async () => {
    try {
        const driver = Driver.create();
        await driver.dragBetween(startPoint, endPoint, 1000, undefined); // ✅ 正确：直接传入 undefined
        expect().assertFail();
    } catch (e) {
        expect(e.code).assertEqual(401);
    }
})
```

### 8.4 为什么禁止 as any

1. **绕过类型检查**：`as any` 会绕过 TypeScript 的类型检查，隐藏潜在的类型错误
2. **降低代码质量**：绕过类型检查会导致代码质量下降，增加运行时错误
3. **不符合最佳实践**：TypeScript 的设计目的是提供静态类型安全，`as any` 违背了这一设计
4. **测试框架规范**：XTS 测试规范要求遵循 TypeScript 最佳实践
5. **ArkTS 静态模式**：在静态模式下，`as any` 会导致编译错误

---

## 九、错误码测试断言规范（重要！）

### 8.1 错误码断言必须遵循的规则

> **重要**：错误码测试时，必须明确断言特定的错误码，而不是使用范围判断或"或"表达。

| 规则 | 说明 | 示例 |
|------|------|------|
| **使用 assertEqual** | 必须使用 `assertEqual` 明确断言特定错误码 | `expect(e.code).assertEqual(401)` |
| **不要使用范围断言** | 不要使用 `assertLessThanOrEqual`、`assertLarger` 等范围断言 | ❌ `expect(e.code).assertLessThanOrEqual(401)` |
| **不要使用"或"表达** | 不要在测试描述中使用"或"表达多个错误码 | ❌ "预期结果: 抛出 401 或 17000007" |
| **明确错误码** | 必须从 @throws 标记中提取并明确声明错误码 | ✅ "预期结果: 抛出错误码 401" |

### 8.2 错误码测试正确示例

```typescript
/**
 * @tc.name testMethodError401001
 * @tc.number SUB_MODULE_API_METHOD_ERROR_401_001
 * @tc.desc 测试 API 的 method 方法 - 参数为null时抛出错误码401
 * @tc.type   FUNCTION
 * @tc.size   MEDIUMTEST
 * @tc.level  LEVEL3
 */
it('testMethodError401001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
    try {
        const driver = Driver.create();
        await driver.method(param, null);
        expect().assertFail();
    } catch (e) {
        console.log(`error is: ${JSON.stringify(e)}`);
        expect(e.code).assertEqual(401); // ✅ 正确：明确断言401错误码
    }
})
```

### 8.3 错误码测试错误示例

```typescript
// ❌ 错误1：使用不存在的断言方法
it('testMethodError001', Level.LEVEL2, async () => {
    try {
        const driver = Driver.create();
        await driver.method(param, null);
        expect().assertFail();
    } catch (e) {
        expect(e.code).assertLessThanOrEqual(401); // ❌ 错误：方法不存在
    }
})

// ❌ 错误2：使用"或"表达不明确
/**
 * @tc.desc 测试 API 的 method 方法 - 参数为null
 * 预期结果: 抛出 401 或 17000007 错误码  // ❌ 错误：错误码不明确
 */
it('testMethodError002', Level.LEVEL2, async () => {
    try {
        const driver = Driver.create();
        await driver.method(param, null);
        expect().assertFail();
    } catch (e) {
        // 未明确断言特定错误码
        expect(e.code).assertEqual(401); // ❌ 错误：与描述中的"或"矛盾
    }
})
```

### 8.4 从覆盖率报告提取错误码的规范

当从覆盖率报告中提取错误码时：

1. **读取错误码列**：例如 "401/17000002/17000007"
2. **从 @throws 标记验证**：检查 .d.ts 文件中的 @throws 标记
3. **确定实际的错误码**：根据参数类型和触发条件确定具体错误码
4. **生成测试时明确声明**：
   ```markdown
   - **预期结果**: 抛出错误码 401  # 明确
   - **断言方法**: `expect(e.code).assertEqual(ErrorCode)`  # 正确
   ```
