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

| No. | API | 功能说明 | 使用方法示例 |
|-----|-----|----------|--------------|
| 1 | `assertClose` | 检验 actualValue 和 expectedValue[0] 的接近程度是否是 expectedValue[1] | `expect(actualValue).assertClose(expectedValue[0], expectedValue[1])` |
| 2 | `assertContain` | 检验 actualValue 中是否包含 expectedValue | `expect(actualValue).assertContain(expectedValue)` |
| 3 | `assertEqual` | 检验 actualValue 是否等于 expectedValue | `expect(actualValue).assertEqual(expectedValue)` |
| 4 | `assertFail` | 抛出一个错误 | `expect(actualValue).assertFail()` |
| 5 | `assertFalse` | 检验 actualValue 是否是 false | `expect(actualValue).assertFalse()` |
| 6 | `assertTrue` | 检验 actualValue 是否是 true | `expect(actualValue).assertTrue()` |
| 7 | `assertInstanceOf` | 检验 actualValue 是否是 expectedValue 类型，只支持基础类型（如Number、String、Boolean、Object等类型），不支持自定义类型，且只支持传入类型名的字符串，不能直接传入类型 | `expect(actualValue).assertInstanceOf(expectedValue)` |
| 8 | `assertLarger` | 检验 actualValue 是否大于 expectedValue | `expect(actualValue).assertLarger(expectedValue)` |
| 9 | `assertLess` | 检验 actualValue 是否小于 expectedValue | `expect(actualValue).assertLess(expectedValue)` |
| 10 | `assertNull` | 检验 actualValue 是否是 null | `expect(actualValue).assertNull()` |
| 11 | `assertThrowError` | 检验 actualValue 抛出 Error 内容是否是 expectedValue | `expect(actualValue).assertThrowError(expectedValue)` |
| 12 | `assertUndefined` | 检验 actualValue 是否是 undefined | `expect(actualValue).assertUndefined()` |
| 13 | `assertNaN` | 检验 actualValue 是否是一个 NaN | `expect(actualValue).assertNaN()` |
| 14 | `assertNegUnlimited` | 检验 actualValue 是否等于 Number.NEGATIVE_INFINITY | `expect(actualValue).assertNegUnlimited()` |
| 15 | `assertPosUnlimited` | 检验 actualValue 是否等于 Number.POSITIVE_INFINITY | `expect(actualValue).assertPosUnlimited()` |
| 16 | `assertDeepEquals` | 检验 actualValue 和 expectedValue 是否完全相等 | `expect(actualValue).assertDeepEquals(expectedValue)` |
| 17 | `not` | 断言取反，支持上面所有的断言功能 | `expect(actualValue).not().assertX(expectedValue)` |
| 18 | `message` | 自定义断言异常信息 | `expect(actualValue).message('custom message').assertX(expectedValue)` |

---

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

## 四、测试框架导入

```typescript
//测试框架导入
import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Size, Level} from '@ohos/hypium'
//公共模块引入
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
