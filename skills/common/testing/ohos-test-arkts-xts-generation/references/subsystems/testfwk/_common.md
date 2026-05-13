# testfwk 子系统配置

> **版本**: 2.2.0
> **更新日期**: 2026-04-02
> **基于核心配置**: _common.md v2.0.0

---

## 一、基础信息

```json
{
  "name": "testfwk",
  "kitPackage": "@kit.TestKit",
  "testPath": "test/xts/acts/testfwk/",
  "documentationPath": "docs/zh-cn/application-dev/reference/apis-test-kit/",
  "apiType": "dynamic&static"
}
```

---

## 二、差异化配置

### 2.1 路径差异化

```json
{
  "paths": {
    "testPath": "test/xts/acts/testfwk/",
    "assistPath": "test/xts/acts/testfwk/uitestScene/",
    "buildConfig": "test/xts/acts/testfwk/BUILD.gn"
  }
}
```

### 2.2 命名差异化

```json
{
  "naming": {
    "testFilePattern": "{Module}{Method}.test.ets",
    "testSuitePattern": "{Module}{Method}Test",
    "sceneFilePattern": "{Module}Scene.ets",
    "staticTestPattern": "{Module}Static.test.ets",
    "errorCodePattern": "{Module}ErrorCode.test.ets"
  }
}
```

### 2.3 导入差异化

```json
{
  "imports": {
    "kitPackage": "@kit.TestKit",
    "basicImports": [
      "describe, it, expect"
    ],
    "typeImports": [
      "TestType, Level, Size"
    ],
    "moduleImports": {
      "UiTest": "Driver, Component, On, UiWindow, MatchPattern, PointerMatrix",
      "PerfTest": "PerfTest, PerfMetric, PerfTestStrategy, PerfMeasureResult",
      "JsUnit": "describe, it, expect, beforeAll, MockKit, SysTestKit, Hypium"
    },
    "conditionalImports": [
      "beforeAll, afterAll, beforeEach, afterEach"
    ]
  }
}
```

### 2.4 特殊规则

#### 2.4.1 testfwk 特有规则

```json
{
  "specialRules": {
    "stringEmptyRule": "空字符串 '' 是合法参数，不会抛出错误码 401",
    "testTypeExtensions": ["EVENT"],
    "namingExtensions": [
      {
        "type": "测试用例编号",
        "rule": "SUB_testfwk_{模块}_{方法}_{类型}_{序号}",
        "example": "SUB_testfwk_DRIVER_CLICK_PARAM_001"
      }
    ],
    "apiSpecific": [
      {
        "api": "string参数",
        "rule": "空字符串不生成 ERROR_401 测试用例，只生成 PARAM 测试用例",
        "description": "testfwk 字符串参数特殊规则"
      },
      {
        "api": "UiTest",
        "rule": "必须使用 Driver.findComponent() 和 ON.id() 查找组件",
        "description": "UiTest 特殊交互规则"
      },
      {
        "api": "PerfTest",
        "rule": "必须遵循 create(strategy) → run() → getMeasureResult(metric) → destroy() 顺序",
        "description": "PerfTest 状态机约束，actionCode 必须调用 finish 回调"
      },
      {
        "api": "JsUnit",
        "rule": "必须使用 MockKit 进行 Mock 测试",
        "description": "JsUnit Mock 测试规则"
      }
    ],
     "parameterRules": {
       "string": ["正常值", "空字符串(合法)", "null", "undefined", "超长字符串"],
       "number": ["正数", "负数", "0", "null", "undefined", "边界值"],
       "boolean": ["true", "false", "null", "undefined"],
       "enum": ["每个枚举值", "null", "undefined", "无效值"],
       "array": ["空数组", "非空数组", "null", "undefined", "边界长度"],
       "object": ["正常对象", "null", "undefined", "缺少属性", "类型错误"]
     },
     "parameterTestingRules": {
       "stringEmpty": {
         "rule": "空字符串 '' 是合法参数，不会抛出错误码 401",
         "description": "testfwk 子系统的字符串参数，空字符串是合法参数",
         "testAction": "只需要生成空字符串的合法参数测试用例，不生成 ERROR 测试用例"
       }
     }
  }
}
```

#### 2.4.2 编译配置

```json
{
  "compileConfig": {
    "suiteName": "testfwk",
    "compileCommand": "./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=testfwk",
    "buildGnPath": "test/xts/acts/testfwk/BUILD.gn",
    "testSuites": [
      "ActsUiTest",
      "ActsUiStaticTest",
      "ActsUiTestScene",
      "ActsUiTestErrorCodeTest",
      "ActsUiTestErrorCodeStaticTest",
      "ActsUiTestQuarantineTest",
      "ActsPerfTestTest",
      "ActsPerfTestTestStaticTest",
      "ActsPerfTestScene",
      "ActsUiPCTest",
      "ActsUiPCStaticTest"
    ],
    "conditionalSuites": {
      "wearable": ["ActsUiTest", "ActsUiTestScene", "ActsUiStaticTest"],
      "pc": ["ActsUiPCTest", "ActsUiPCStaticTest", "ActsUiTestScene"]
    },
    "outputPath": "out/rk3568/suites/acts/acts/testcases/"
  }
}
```

### 2.5 测试框架分类

```json
{
  "Modules": {
    "UiTest": {
      "description": "UI 自动化测试框架",
      "apis": ["Driver", "Component", "On", "UiWindow", "UIEventObserver", "PointerMatrix"],
      "testScenarios": ["元素查找和交互", "UI状态验证", "用户行为模拟"],
      "specialFeatures": ["错误码处理", "场景测试", "静态测试", "多屏操作"],
      "testConfig": ["UiTest.md"]
    },
    "PerfTest": {
      "description": "性能测试框架",
      "apis": ["PerfTest", "PerfMetric", "PerfTestStrategy", "PerMeasureResult"],
      "testScenarios": ["代码段耗时", "CPU/内存占用", "应用启动耗时", "页面切换耗时", "列表滑动帧率"],
      "specialFeatures": ["状态机约束", "多次迭代取平均", "多指标同时采集"],
      "testConfig": ["PerfTest.md"]
    },
    "JsUnit": {
      "description": "单元测试框架",
      "apis": ["describe", "it", "expect", "beforeAll", "MockKit"],
      "testScenarios": ["单元测试", "Mock测试", "集成测试"],
      "specialFeatures": ["Mock工具", "断言扩展", "生命周期管理"],
      "testConfig": ["JsUnit.md"]
    }
  }
}
```

---

## 三、核心配置继承

本配置继承自核心配置文件 `references/subsystems/_common.md`，在此基础上添加以下差异化配置：

### 3.1 继承关系

```json
{
  "inheritance": {
    "baseConfig": "references/subsystems/_common.md",
    "overrides": {
      "testFramework": "testfwk",
      "specialRules": "testfwk 特有规则",
      "compileSupport": "专门的编译配置"
    },
    "extensions": {
      "frameworkCategories": "三大框架分类（UiTest, PerfTest, JsUnit）",
      "stringEmptyRule": "字符串空规则",
      "crossSubsystemDeps": "跨子系统依赖"
    }
  }
}
```

### 3.2 配置优先级

```
用户自定义配置 > testfwk/_common.md > references/subsystems/_common.md
```

---

## 四、使用指南

### 4.1 基本使用

```typescript
import { describe, it, expect, Level, Size, TestType } from '@ohos/hypium';
import { Driver, ON, Component } from '@ohos.UiTest';

export default function {Module}{Method}Test() {
  describe('{Module}{Method}Test', () => {
    let driver = Driver.create();

    beforeAll(async (done: Function) => {
      await driver.delayMs(1000);
      done();
    });

    it('testCase_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
      // 测试代码
    });
  });
}
```

### 4.2 各框架使用示例

#### UiTest 示例

来源：`test/xts/acts/testfwk/uitest/entry/src/ohosTest/ets/test/uitest.test.ets`

```typescript
import { describe, beforeAll, it, expect, TestType, Level, Size } from '@ohos/hypium';
import { Driver, ON, Component } from '@ohos.UiTest';

export default function uitest() {
  describe('uitest', () => {
    let driver: Driver
    beforeAll(async (done: Function) => {
      driver = Driver.create()
      await driver.delayMs(1000)
      done()
    })

    it('test_click_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
      await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility');
      let button = await driver.findComponent(ON.type('Button'));
      if (button) {
        await button.click();
      }
    });
  });
}
```

#### PerfTest 示例

来源：`test/xts/acts/testfwk/perftest/entry/src/ohosTest/ets/test/PerfTest.test.ets`

```typescript
import { describe, beforeAll, it, expect, TestType, Level, Size } from '@ohos/hypium';
import { PerfMetric, PerfTest, PerfTestStrategy } from '@kit.TestKit';
import { BusinessError, Callback } from '@kit.BasicServicesKit';

export default function PerfTestTest() {
  describe('PerfTestTest', () => {
    it('testPerfTestCalculate', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: Function) => {
      let metrics: Array<PerfMetric> = [PerfMetric.DURATION, PerfMetric.CPU_LOAD];
      let actionCode = async (finish: Callback<boolean>) => {
        finish(true);
      };
      let perfTestStrategy: PerfTestStrategy = { metrics, actionCode, iterations: 5, timeout: 30000 };
      try {
        let perfTest: PerfTest = PerfTest.create(perfTestStrategy);
        await perfTest.run();
        let res = perfTest.getMeasureResult(PerfMetric.DURATION);
        perfTest.destroy();
        expect(res.average).assertLargerOrEqual(0);
      } catch (error) {
        expect(false).assertTrue();
      }
      done();
    })
  })
}
```

### 4.3 测试套件注册

来源：`test/xts/acts/testfwk/uitest/entry/src/ohosTest/ets/test/List.test.ets`

```typescript
import UiTest from './uitest.test'
import uitestEnumTest from './UitestEnum.test';
import uitestUiWindowTest from './UitestUiWindow.test'
export default function testsuite() {
  UiTest();
  uitestEnumTest();
  uitestUiWindowTest();
}
```

---

## 五、API 关联关系（跨模块共享）

| 共享类型 | 使用该类型的模块 | 说明 |
|---------|----------------|------|
| `Point` (interface) | UiTest (Component, Driver, UiWindow, PointerMatrix) | 坐标点，x/y/displayId |
| `Rect` (interface) | UiTest (Component, UiWindow, UIElementInfo) | 矩形区域，left/top/right/bottom |

---

## 六、跨子系统依赖

### 6.1 强依赖

| 本子系统模块 | 依赖的外部子系统 | 外部类型 | 导入语句 | 测试处理方式 |
|-------------|----------------|---------|---------|------------|
| UiTest | @ohos.display | display 模块 | `import display from '@ohos.display'` | `display.getDefaultDisplaySync().id` 获取 displayId |
| UiTest/PerfTest | @ohos.base | BusinessError | `import { BusinessError } from '@ohos.base'` | 仅类型依赖，catch 中使用 |
| PerfTest | @kit.BasicServicesKit | BusinessError, Callback | `import { BusinessError, Callback } from '@kit.BasicServicesKit'` | 仅类型依赖 |
| UiTest/PerfTest | @ohos.app.ability.abilityDelegatorRegistry | AbilityDelegatorRegistry | `import AbilityDelegatorRegistry from '@ohos.app.ability.abilityDelegatorRegistry'` | 启动/停止测试应用 |

### 6.2 弱依赖

| 本子系统模块 | 交互机制 | 关联子系统 | 说明 |
|-------------|---------|-----------|------|
| UiTest | 仅 1 个文件 | @kit.ArkUI | UitestUiWindow.test.ets 导入 display |
| UiTest/PerfTest | 日志 | @ohos.hilog | 仅静态测试变体使用 |
| PerfTest | 应用启动 | @ohos.ability.featureAbility | 少量文件使用，可能为冗余导入 |

### 6.3 依赖处理规则

- 外部子系统无 ohos-test-arkts-xts-generation 配置时（如 display）：使用最小构造方式，注释标注依赖来源
- BusinessError 仅作为类型导入，不构造实例
- 禁止 mock 强依赖的类型

---

## 七、版本历史

- **v2.2.0** (2026-04-02):
  - 修正 PerfTest API（perfSuite/perfLog/finishBenchmark → PerfTest.create/run/getMeasureResult/destroy）
  - 修正 UiTest API（DriverStatic/UiComponent → Component/On）
  - 新增 PC 测试套（ActsUiPCTest, ActsUiPCStaticTest）
  - 新增条件编译说明（wearable/pc 模式）
  - 新增 API 关联关系章节
  - 新增跨子系统依赖章节
  - 替换使用示例为真实测试代码
- **v2.1.0** (2026-03-03):
  - 初始结构化配置