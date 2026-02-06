# testfwk 子系统通用配置

> **子系统信息**
> - 名称: testfwk（OpenHarmony 测试框架）
> - Kit包: @kit.TestKit（统一测试框架）
> - 测试路径: test/xts/acts/testfwk/
> - 版本: 1.7.0
> - 更新日期: 2026-02-06

## 目录

- [一、子系统通用配置](#一子系统通用配置)
- [二、子系统通用测试规则](#二子系统通用测试规则)
- [三、模块特有配置](#三模块特有配置)（详见各模块独立文件）
- [四、子系统通用代码模板](#四子系统通用代码模板)
- [五、已知问题和注意事项](#五已知问题和注意事项)
- [六、编译配置](#六编译配置) ⭐ NEW
- [七、参考示例](#七参考示例)
- [八、版本历史](#八版本历史)

---

## 一、子系统通用配置

### 1.1 API Kit 映射

```typescript
// TestKit 统一测试框架导入
import { Driver, DriverStatic, UiComponent } from '@kit.TestKit';
import {describe, beforeAll, beforeEach, afterEach, afterAll, it, expect} from '@kit.TestKit';
import {perfSuite, perfLog} from '@kit.TestKit';
```

**重要说明**：
- testfwk 子系统包含三个测试子模块，均归属 **TestKit** 框架
- uitest、perftest 统一使用 `@kit.TestKit` 导入
- **UiTest 详细配置**：详见 `uitest.md`
- **PerfTest 详细配置**：详见 `perftest.md`
- **JsUnit 详细配置**：详见 `JsUnit.md`

### 1.2 测试路径规范

```
测试用例目录: test/xts/acts/testfwk/test/
历史用例参考: ${OH_ROOT}/test/xts/acts/testfwk/
```

### 1.3 模块映射配置

testfwk 子系统包含三个测试子模块：

| 模块名称 | API 声明文件 | 主要 API | 说明 |
|---------|-------------|---------|------|
| **UiTest** | @ohos.uitest.d.ts | Driver, DriverStatic, UiComponent, UiDriver | UI 测试框架（详见 `uitest.md`） |
| **PerfTest** | @ohos.perftest.d.ts | perfSuite, perfLog, finishBenchmark | 性能测试框架（详见 `perftest.md`） |
| **JsUnit** | test/testfwk/arkxtest/jsunit/index.d.ts | describe, it, expect, beforeAll, MockKit, SysTestKit, Hypium | 单元测试框架（详见 `JsUnit.md`） |

**模块解析说明**：
- **模块级解析**：可以解析某个模块的所有 API（如解析 UiTest 模块的所有方法）
- **API 级解析**：可以解析单个 API（如 Driver.on()）
- **批量解析**：可以解析整个子系统的所有模块和 API

**重要说明 - JsUnit 模块**：
- **API 特殊性**：JsUnit 的 API **不随 interface 仓发布**
- **声明文件位置**：`/mnt/data/c00810129/oh_0130/test/testfwk/arkxtest/jsunit/index.d.ts`
- **完整 API 列表**：
  - **测试组织**：describe, it, xdescribe, xit
  - **生命周期**：beforeAll, afterAll, beforeEach, beforeEachIt, afterEach, afterEachIt
  - **条件生命周期**：beforeItSpecified, afterItSpecified
  - **断言**：expect, Assert 接口（20+ 断言方法）
  - **Mock**：MockKit 类, when 接口, ArgumentMatchers 类
  - **测试工具**：SysTestKit 类, Hypium 类
  - **枚举**：TestType, Size, Level

### 1.4 参考资料配置 ⭐ NEW

**文档类型和位置**：

| 文档类型 | 路径 | 说明 |
|---------|------|------|
| **TestKit API 参考** | `docs/zh-cn/application-dev/reference/apis-test-kit/` | TestKit 统一 API 文档 |
| **UiTest 参考** | `docs/zh-cn/application-dev/reference/apis-test-kit/uitest.md` | UiTest 模块文档（详见 `uitest.md`） |
| **PerfTest 参考** | `docs/zh-cn/application-dev/reference/apis-test-kit/perftest.md` | PerfTest 模块文档（详见 `perftest.md`） |
| **JsUnit 参考** | `docs/zh-cn/application-dev/reference/apis-test-kit/jsunit.md` | JsUnit 模块文档（详见 `JsUnit.md`） |
| **测试开发指南** | `docs/zh-cn/application-dev/application-test/` | 测试用例开发指南 |


**查找方式**：
```
方式1：从子系统配置读取（推荐）
  → 使用本配置文件中指定的参考资料路径

方式2：根据 API 名称在 docs 仓中查找（兜底）
  → grep -r "Driver" ${OH_ROOT}/docs/ | grep -i "test"
  → grep -r "describe" ${OH_ROOT}/docs/ | grep -i "test"

方式3：查看模块详细配置
  → UiTest 详细配置见 uitest.md
  → PerfTest 详细配置见 perftest.md
  → JsUnit 详细配置见 JsUnit.md
```

## 二、子系统通用测试规则

### 2.1 字符串参数特殊规则（重要）

**testfwk 子系统特有规则**：入参类型为 `string` 的场景中，**空字符串 `''` 是合法参数，不会抛出系统错误码 401**。

**与其他子系统的区别**：

| 子系统 | string 空字符串行为 | 错误码 |
|-------|-------------------|-------|
| **通用规则** | 空字符串通常视为参数错误 | 抛出 401 |
| **testfwk** | 空字符串是合法参数 | 不抛出 401 |

**测试用例生成规则**：

```typescript
/**
 * ✅ testfwk 子系统 - string 参数测试规则
 *
 * 对于入参类型为 string 的 API：
 *
 * 1. 正常值测试（必须）
 *    - 有效字符串值
 *    - 示例：'validString'
 *
 * 2. 空字符串测试（必须，合法）
 *    - 空字符串 '' 是合法参数
 *    - 不会抛出错误码 401
 *    - 示例：''
 *
 * 3. null 测试（按 API 定义）
 *    - 如果 API 允许 null，则不抛出错误
 *    - 如果 API 不允许 null，可能抛出 401
 *
 * 4. undefined 测试（按 API 定义）
 *    - 如果 API 允许 undefined，则不抛出错误
 *    - 如果 API 不允许 undefined，可能抛出 401
 *
 * ❌ 错误示例（不要生成）：
 * it('testMethodEmptyStringError401', ...); // 空字符串不会抛出 401
 *
 * ✅ 正确示例：
 * it('testMethodEmptyStringValid', ...);  // 空字符串是合法参数
 */
```

**代码模板示例**：

```typescript
/**
 * @tc.name testfwk StringParam EmptyString001
 * @tc.number SUB_testfwk_{MODULE}_{METHOD}_PARAM_EMPTYSTRING_001
 * @tc.desc 测试 testfwk API 的 string 参数 - 空字符串是合法参数
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('test{MethodName}EmptyString001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 准备测试数据 - 空字符串是合法参数
  let apiObject = new APIName();
  let emptyString = '';

  // 2. 执行测试 - 不会抛出错误码 401
  try {
    let result = apiObject.methodName(emptyString);
    // 3. 验证结果 - 正常返回
    expect(result).assertEqual(expectedValue);
  } catch (err) {
    // 不应该抛出 401 错误码
    expect(err.code).not().assertEqual(401);
    expect().assertFail(); // 如果抛出任何错误，测试失败
  }
});
```

### 2.2 参数类型测试规则（testfwk 特有版本）

| 参数类型 | 必须测试的场景 | 特殊说明 | 生成的测试用例数 |
|---------|---------------|---------|----------------|
| **string** | 正常值、空字符串（合法）、null、undefined、超长字符串 | ⭐ 空字符串不抛出 401 | 5-6 个 |
| **number** | 正数、负数、0、null、undefined、边界值 | 同通用规则 | 6-7 个 |
| **boolean** | true、false、null、undefined | 同通用规则 | 4 个 |
| **枚举** | 每个枚举值、null、undefined、无效值 | 同通用规则 | 枚举值+2 个 |
| **数组** | 空数组、非空数组、null、undefined、边界长度 | 同通用规则 | 5-6 个 |
| **对象** | 正常对象、null、undefined、缺少属性、类型错误 | 同通用规则 | 5-6 个 |

**重要**：
- 生成 string 参数测试用例时，**不要**为空字符串场景生成 ERROR_401 测试用例
- 空字符串应作为 PARAM 测试用例，验证其合法性和正确性
- 仅当 API 的 `@throws` 标记明确声明了空字符串会抛出错误时，才生成对应的错误码测试

### 2.3 错误码测试规则

**基础规则**：
- 读取 API 的 JSDOC 中 `@throws` 标记
- 为每个声明的错误码生成测试用例
- **异常场景断言优先使用 `err.code`**，而非 `err.message`

**特殊规则**：
- 对于 string 参数，如果 `@throws` 中没有明确说明空字符串会抛出错误码，则**不生成**空字符串的错误码测试
- 错误码必须是 number 类型

**示例**：

```typescript
// 示例 API 定义
/**
 * @param name - 测试名称
 * @throws { BusinessError } 401 - 参数类型错误（当 name 为 null 或 undefined 时）
 */
function setTestName(name: string): void;

// ✅ 生成的测试用例
// 1. 正常值测试
it('testSetTestNameNormal001', ...);

// 2. 空字符串测试（合法，不抛出 401）
it('testSetTestNameEmptyString001', ...);

// 3. null 测试（抛出 401）
it('testSetTestNameError401Null001', ...);

// 4. undefined 测试（抛出 401）
it('testSetTestNameError401Undefined001', ...);

// ❌ 不生成的测试用例
// it('testSetTestNameError401EmptyString001', ...); // 空字符串不抛出 401
```

## 三、模块特有配置

### 3.1 模块概述

testfwk 包含三个测试子模块，每个模块有不同的测试目的和使用场景：

**详细的模块配置请查看各模块的独立文件**：

- **UiTest 模块**：详见 `uitest.md`
  - UI 自动化测试框架
  - 核心错误码测试经验（17000001-17000007）
  - Driver、UiComponent、UiDriver API
  - 完整的测试模板和示例

- **PerfTest 模块**：详见 `perftest.md`
  - 性能测试框架
  - perfSuite、perfLog、finishBenchmark API
  - 性能测试最佳实践

- **JsUnit 模块**：详见 `JsUnit.md`
  - 单元测试框架
  - 完整的 API 列表（测试组织、生命周期、断言、Mock、工具类）
  - describe、it、expect、MockKit、SysTestKit、Hypium


### 3.2 模块通用配置继承

本配置（testfwk/_common.md）适用于所有三个子模块：
- **UiTest** 模块继承本配置，详见 `uitest.md`
- **PerfTest** 模块继承本配置，详见 `perftest.md`
- **JsUnit** 模块继承本配置，详见 `JsUnit.md`

模块级配置可以覆盖本配置的特定部分。
## 四、子系统通用代码模板

### 4.1 String 参数错误码测试模板（null/undefined）

```typescript
/**
 * @tc.name testfwk StringParam Error401Null001
 * @tc.number SUB_testfwk_{MODULE}_{METHOD}_ERROR_401_NULL_001
 * @tc.desc 测试 testfwk API 的 string 参数 - null 抛出 401
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL2
 */
it('test{MethodName}Error401Null001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, () => {
  // 1. 准备测试数据
  let apiObject = new APIName();
  let nullParam: string = null;

  // 2. 执行测试并捕获异常
  try {
    apiObject.methodName(nullParam);
    expect().assertFail(); // 如果没有抛出异常，测试失败
  } catch (err) {
    // 3. 验证错误码
    expect(err.code).assertEqual(401);
  }
});
```

**注**：各模块的详细测试模板请查看独立配置文件：
- UiTest 测试模板：详见 `uitest.md`
- PerfTest 测试模板：详见 `perftest.md`
- JsUnit 测试模板：详见 `JsUnit.md`

## 五、已知问题和注意事项

### 5.1 字符串参数测试注意事项

1. **空字符串是合法参数**：
   - 空字符串不会触发 401 错误码
   - 需要验证空字符串的业务逻辑正确性
   - 不要为空字符串生成 ERROR_401 测试用例

2. **null 和 undefined 处理**：
   - 如果 API 的 `@throws` 标记声明了 null 或 undefined 会抛出 401
   - 则必须生成对应的错误码测试用例
   - 如果没有声明，则视为合法参数

3. **超长字符串测试**：
   - 测试边界情况（如超长字符串）
   - 验证是否有长度限制
   - 检查是否会抛出其他错误码

### 5.3 测试注意事项

**通用注意事项**：
1. **框架依赖**：
   - 三个子模块均归属 TestKit 框架
   - 统一使用 `@kit.TestKit` 导入
   - 注意框架版本的兼容性

**模块特定注意事项**：
2. **UiTest 特性**：详见 `uitest.md`
3. **PerfTest 特性**：详见 `perftest.md`
4. **JsUnit 特性**：详见 `JsUnit.md`

## 六、编译配置

### 6.1 测试框架编译套件名称

**重要说明**：当要求编译测试框架（testfwk）的所有测试套时，使用以下配置：

#### 6.1.1 编译命令

```bash
# 编译测试框架的所有测试套
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=testfwk
```

#### 6.1.2 配置依据

**BUILD.gn 配置文件**：
- 文件路径：`/test/xts/acts/testfwk/BUILD.gn`
- 关键配置：第17行定义了 `group("testfwk")`

```gni
# testfwk/BUILD.gn (第17-47行)
group("testfwk") {
  testonly = true
  if (ace_engine_feature_wearable) {
    deps = [
      "uitest:ActsUiTest",
      "uitestScene:ActsUiTestScene",
      "uitestStatic:ActsUiStaticTest",
    ]
  } else {
    deps = [
      "perftest:ActsPerfTestTest",
      "perftestStatic:ActsPerfTestTestStaticTest",
      "perftestScene:ActsPerfTestScene",
      "uitest:ActsUiTest",
      "uitestScene:ActsUiTestScene",
      "uitestStatic:ActsUiStaticTest",
      "uitest_errorcode:ActsUiTestErrorCodeTest",
      "uitest_errorcode_static:ActsUiTestErrorCodeStaticTest",
      "uitestQuarantine:ActsUiTestQuarantineTest",
      "uitest_quarantine_static:ActsUiTestQuarStaticTest",
    ]
  }
  if (arkxtest_product_feature == "pc") {
    deps += [
      "uitestScene:ActsUiTestScene",
      "uitest_pc:ActsUiPCTest",
      "uitest_pc_static:ActsUiPCStaticTest",
    ]
  }
}
```

#### 6.1.3 suite=testfwk 说明

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **suite 参数** | `testfwk` | 测试框架子系统在 BUILD.gn 中定义的 group 名称 |
| **编译范围** | 测试框架的所有测试套 | 包括 uitest、perftest 等所有子模块 |
| **配置依据** | `testfwk/BUILD.gn` | 第17行 `group("testfwk")` 定义 |

**重要说明**：
- `testfwk` 不是某个具体的测试套名称，而是 BUILD.gn 中定义的 group 名称
- 使用 `suite=testfwk` 会编译该 group 下所有依赖的测试套
- 根据 `ace_engine_feature_wearable` 和 `arkxtest_product_feature` 的不同值，编译的测试套列表会有所不同
- 标准系统（非 wearble、非 pc）会编译 8 个测试套

#### 6.1.4 编译产物

```bash
# 编译输出位置
out/rk3568/suites/acts/acts/testcases/
├── ActsPerfTestTest.hap
├── ActsPerfTestTestStaticTest.hap
├── ActsPerfTestScene.hap
├── ActsUiTest.hap
├── ActsUiTestScene.hap
├── ActsUiStaticTest.hap
├── ActsUiTestErrorCodeTest.hap
├── ActsUiTestErrorCodeStaticTest.hap
├── ActsUiTestQuarantineTest.hap
└── ActsUiTestQuarStaticTest.hap
```

### 6.2 单个测试套编译

如果只需要编译某个特定的测试套，直接使用测试套名称作为 `suite` 参数：

```bash
# 编译单个测试套（例如 uitest）
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest
```

**测试套名称映射**（参考 BUILD.gn 中的 deps）：

| 测试套名称 | 说明 |
|-----------|------|
| `ActsUiTest` | UI 测试套 |
| `ActsUiTestScene` | UI 场景测试套 |
| `ActsUiStaticTest` | UI 静态测试套 |
| `ActsUiTestErrorCodeTest` | UI 错误码测试套 |
| `ActsUiTestErrorCodeStaticTest` | UI 错误码静态测试套 |
| `ActsPerfTestTest` | 性能测试套 |
| `ActsPerfTestTestStaticTest` | 性能测试静态套 |
| `ActsPerfTestScene` | 性能测试场景套 |

---

## 七、参考示例

### 7.1 历史用例参考

```
${OH_ROOT}/test/xts/acts/testfwk/
```

### 7.2 测试用例示例

**参考历史用例**：`${OH_ROOT}/test/xts/acts/testfwk/`

**代码模板**：详见上文第四章节"子系统通用代码模板"

---

## 八、版本历史

### v1.7.0 (2026-02-06)

**新增内容**：
- ⭐ **新增"六、编译配置"章节**：
  - 新增 6.1 测试框架编译套件名称
    - 编译命令：`suite=testfwk`
    - 配置依据：`/test/xts/acts/testfwk/BUILD.gn` 第17行 `group("testfwk")`
    - 完整的 BUILD.gn 配置说明
    - suite=testfwk 参数详细说明表格
    - 编译产物列表
  - 新增 6.2 单个测试套编译
    - 单个测试套编译命令示例
    - 测试套名称映射表（8个测试套）

**改进原因**：
- 明确测试框架编译时的套件名称规范
- 提供完整的 BUILD.gn 配置依据
- 说明 group("testfwk") 与 suite 参数的关系
- 方便用户快速查找测试套名称

**更新文件**：
- `/mnt/data/c00810129/.claude/skills/OH_XTS_GENERATOR_TEMPLATE/references/subsystems/testfwk/_common.md`
- 更新日期：2026-02-06

---

### v1.6.0 (2026-02-05)

- 初始版本，包含 testfwk 子系统基础配置
- 三个测试子模块（UiTest、PerfTest、JsUnit）通用配置
- 字符串参数特殊规则（空字符串不抛出 401）
- 参数类型测试规则和错误码测试规则