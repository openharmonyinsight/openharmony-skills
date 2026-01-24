# @ohos.application.testRunner (TestRunner)

**模块**: TestRunner
**API 版本**: 8+
**导入方式**: `import { TestRunner } from '@kit.TestKit';`

## 概述

基础测试框架接口。实现此类以创建具有特定环境设置和测试执行逻辑的自定义测试运行器。

## 必需方法

### onPrepare()

```typescript
onPrepare(): void
```

在运行测试用例之前准备单元测试环境。

**用途**: 初始化测试资源、设置测试环境、配置 mock。

**示例**:
```typescript
import { TestRunner } from '@kit.TestKit';

export default class UserTestRunner implements TestRunner {
  onPrepare() {
    console.info('触发 onPrepare');
    // 在此处设置测试环境
  }

  onRun() {
    console.info('触发 onRun');
  }
}
```

### onRun()

```typescript
onRun(): void
```

在环境准备完成后运行测试用例。

**用途**: 执行测试逻辑、运行测试套件、报告结果。

**示例**:
```typescript
import { TestRunner } from '@kit.TestKit';

export default class UserTestRunner implements TestRunner {
  onPrepare() {
    // 设置完成
  }

  onRun() {
    console.info('触发 onRun');
    // 在此处运行测试用例
  }
}
```

## 实现示例

```typescript
import { TestRunner } from '@kit.TestKit';

export default class CustomTestRunner implements TestRunner {
  private testSuites: string[] = [];

  onPrepare() {
    console.info('准备测试环境');
    // 初始化测试资源
    // 配置测试设置
    // 加载测试配置
  }

  onRun() {
    console.info('运行测试');
    // 执行测试套件
    for (const suite of this.testSuites) {
      this.runTestSuite(suite);
    }
  }

  private runTestSuite(suiteName: string): void {
    // 自定义测试执行逻辑
    console.info(`运行测试套件: ${suiteName}`);
  }
}
```

## 在测试配置中使用

在测试配置文件中配置自定义测试运行器：

```json
{
  "testRunner": "entry/src/ohosTest/ets/testRunner/CustomTestRunner"
}
```

## 系统能力

- **SystemCapability.Ability.AbilityRuntime.Core**
- **原子服务 API**: API 11 起支持
