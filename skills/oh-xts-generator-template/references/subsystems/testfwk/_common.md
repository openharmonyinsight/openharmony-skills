# testfwk 子系统配置

> **版本**: 2.1.0
> **更新日期**: 2026-03-03
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
      "UiTest": "Driver, DriverStatic, UiComponent",
      "PerfTest": "perfSuite, perfLog, finishBenchmark",
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
        "rule": "必须使用 perfSuite 和 perfLog 记录性能数据",
        "description": "PerfTest 性能测试规则"
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
      "ActsUiTestScene", 
      "ActsUiStaticTest",
      "ActsUiTestErrorCodeTest",
      "ActsUiTestErrorCodeStaticTest",
      "ActsUiTestQuarantineTest",
      "ActsPerfTestTest",
      "ActsPerfTestTestStaticTest",
      "ActsPerfTestScene"
    ],
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
      "apis": ["Driver", "DriverStatic", "UiComponent", "UiDriver"],
      "testScenarios": ["元素查找和交互", "UI状态验证", "用户行为模拟"],
      "specialFeatures": ["错误码处理", "场景测试", "静态测试"],
      "testConfig": ["UiTest.md"]
    },
    "PerfTest": {
      "description": "性能测试框架",
      "apis": ["perfSuite", "perfLog", "finishBenchmark"],
      "testScenarios": ["性能基准测试", "内存使用监控", "CPU占用分析"],
      "specialFeatures": ["性能统计", "阈值验证", "基准测试完成"],
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
      "frameworkCategories": "新增三大框架分类",
      "stringEmptyRule": "新增字符串空规则"
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
// 基础测试结构
import { describe, it, expect, Level } from '@ohos/hypium';
import { TestType, Size } from '@ohos/hypium';
import { Driver } from '@ohos.UiTest';

export default function {Module}{Method}Test() {
  describe('{Module}{Method}Test', () => {
    beforeAll(async () => {
      // 初始化
    });

    it('testCase_001', Level.LEVEL0, async () => {
      // 测试代码
    });
  });
}
```

### 4.2 各框架使用示例

#### UiTest 示例

```typescript
/**
 * @tc.name driverClick_001
 * @tc.number SUB_testfwk_DRIVER_CLICK_PARAM_001
 * @tc.desc Test Driver click method
 * @tc.type FUNCTION
 * @tc.size SMALLTEST
 * @tc.level LEVEL0
 */
it('driverClick_001', Level.LEVEL0, async () => {
  let driver: Driver = await Driver.create();
  let button = await driver.findComponent(ON.id('button_click'));
  await button.click();
  await sleep(500);
});
```

#### PerfTest 示例

```typescript
/**
 * @tc.name perfSuiteMemoryTest_001
 * @tc.number SUB_testfwk_PERFSUITE_MEMORY_TEST_001
 * @tc.desc Test performance suite memory usage
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('perfSuiteMemoryTest_001', Level.LEVEL1, async () => {
  let startTime = performance.now();
  
  // 执行测试代码
  for (let i = 0; i < 1000; i++) {
    await testOperation();
  }
  
  let endTime = performance.now();
  let duration = endTime - startTime;
  
  perfLog(`Test duration: ${duration}ms`);
  expect(duration).assertLessThan(5000);
});
```

#### JsUnit 示例

```typescript
/**
 * @tc.name jsUnitMockTest_001
 * @tc.number SUB_testfwk_JSDUNIT_MOCK_TEST_001
 * @tc.desc Test JsUnit mock functionality
 * @tc.type FUNCTION
 * @tc.size SMALLTEST
 * @tc.level LEVEL0
 */
it('jsUnitMockTest_001', Level.LEVEL0, () => {
  let mockObj = MockKit.mock('testFunction');
  mockObj.mockImplementation(() => 'mocked_value');
  
  let result = testFunction();
  expect(result).assertEqual('mocked_value');
});
```

### 4.3 测试套件注册

```typescript
import DriverTest from './driver/DriverTest';
import PerfTest from './performance/PerfTest';
import JsUnitTest from './unit/JsUnitTest';

export default function testsuite() {
  DriverTest();
  PerfTest();
  JsUnitTest();
}
```