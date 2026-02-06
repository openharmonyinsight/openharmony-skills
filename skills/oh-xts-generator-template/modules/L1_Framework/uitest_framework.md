# UiTest 测试框架基础

> **模块信息**
> - 层级：L1_Framework
> - 优先级：按需加载
> - 适用范围：UI界面相关的API测试
> - 依赖：hypium_framework.md

---

## 一、UiTest 框架概述

UiTest 通过简洁易用的API提供查找和操作界面控件的能力，支持用户开发基于界面操作的自动化测试脚本。

### 1.1 核心能力

- **控件查找** - 支持多种方式定位UI控件
- **控件操作** - 提供点击、滑动、输入等操作方法
- **属性获取** - 获取控件的属性值和状态
- **事件模拟** - 模拟用户交互事件

### 1.2 适用场景

- ✅ ArkUI 组件测试
- ✅ UI 界面交互测试
- ✅ 控件属性验证
- ✅ 页面跳转测试
- ❌ 纯API接口测试（不需要UiTest）

---

## 二、导入语句规范

### 2.1 标准导入

```typescript
import { Driver, ON, BY, Component } from '@ohos.UiTest';
```

### 2.2 模块说明

| 类/接口 | 说明 |
|---------|------|
| **Driver** | 测试驱动类，提供创建测试驱动实例的方法 |
| **ON** | 控件定位器，用于查找控件 |
| **BY** | 定位策略枚举，提供多种定位方式 |
| **Component** | 控件类，提供控件操作和属性获取方法 |

---

## 三、Driver 创建和使用

### 3.1 创建 Driver 实例

```typescript
import { Driver } from '@ohos.UiTest';

let driver: Driver = await Driver.create();
```

### 3.2 Driver 生命周期

```typescript
describe('ComponentTest', () => {
  let driver: Driver;

  beforeAll(async (done: Function) => {
    // 在所有测试前创建 Driver
    driver = await Driver.create();
    done();
  });

  afterAll(async (done: Function) => {
    // 在所有测试后清理资源
    await driver.close();
    done();
  });
});
```

### 3.3 Driver 重要方法

| 方法 | 说明 |
|------|------|
| `create()` | 创建 Driver 实例 |
| `close()` | 关闭 Driver 并释放资源 |
| `findComponent()` | 查找单个控件 |
| `findComponents()` | 查找多个控件 |
| `waitForComponent()` | 轮询等待控件出现（推荐） |

---

## 四、控件定位 (ON)

### 4.1 常用定位方法

```typescript
import { ON } from '@ohos.UiTest';

// 1. 按 id 定位（推荐）
ON.id('component-id')

// 2. 按 text 定位
ON.text('button text')

// 3. 按 type 定位
ON.type('Button')

// 4. 组合定位
ON.id('component-id').type('Button')
```

### 4.2 定位策略说明

| 策略 | 说明 | 使用场景 |
|------|------|---------|
| `id()` | 按组件id定位 | 最准确，推荐使用 |
| `text()` | 按组件文本定位 | 适用于Text、Button等 |
| `type()` | 按组件类型定位 | 用于查找特定类型的组件 |
| `key()` | 按key属性定位 | 使用key唯一标识组件 |

---

## 五、控件查找最佳实践

### 5.1 waitForComponent（强烈推荐）

```typescript
// ✅ 正确 - 使用 waitForComponent 轮询查找
const component = await driver.waitForComponent(ON.id('test-id'), 2000);

if (component) {
  // 执行测试逻辑
  const text = await component.getProperty('text');
  expect(text).assertEqual('expected');
} else {
  console.error('Test FAILED: Component not found!');
  expect().assertFail();
}
```

### 5.2 组件判空处理

```typescript
// ✅ 正确 - 所有 findComponent 必须判空
const component = await driver.findComponent(ON.id('xxx'));

if (component) {
  // 使用组件
  await component.click();
} else {
  expect().assertFail();
}

// ❌ 错误 - 不判空直接使用
const component = await driver.findComponent(ON.id('xxx'));
await component.click(); // 可能为null，导致崩溃
```

### 5.3 waitForComponent 参数说明

```typescript
driver.waitForComponent(
  ON.id('component-id'),  // 定位器
  2000                     // 超时时间（毫秒）
)
```

- **第1个参数**：控件定位器（ON 对象）
- **第2个参数**：等待超时时间，单位毫秒，建议 2000ms
- **返回值**：找到返回 Component 对象，超时返回 null

---

## 六、Component 操作方法

### 6.1 常用操作方法

| 方法 | 说明 | 返回值类型 |
|------|------|-----------|
| `click()` | 点击控件 | Promise\<void\> |
| `doubleClick()` | 双击控件 | Promise\<void\> |
| `longClick()` | 长按控件 | Promise\<void\> |
| `setText()` | 设置文本内容 | Promise\<void\> |
| `getProperty()` | 获取属性值 | Promise\<string\> |
| `getBounds()` | 获取控件边界 | Promise\<Bounds\> |

### 6.2 操作示例

```typescript
// 点击操作
await component.click();

// 设置文本
await component.setText('new text');

// 获取属性
const text = await component.getProperty('text');
const enabled = await component.getProperty('enabled');
const visible = await component.getProperty('visible');

// 验证属性
expect(text).assertEqual('expected text');
expect(enabled).assertEqual('true');
```

---

##七、UiTest API 返回值类型与断言匹配

### 7.1 getProperty 返回值类型

```typescript
// getProperty 总是返回 string 类型
const text = await component.getProperty('text');      // "hello"
const enabled = await component.getProperty('enabled'); // "true"
const width = await component.getProperty('width');     // "100.00vp"
```

### 7.2 断言方法匹配

```typescript
// ✅ 正确 - 使用 assertEqual 比较字符串
const text = await component.getProperty('text');
expect(text).assertEqual('expected text');

const enabled = await component.getProperty('enabled');
expect(enabled).assertEqual('true');

// ✅ 正确 - 布尔属性转换为字符串比较
const visible = await component.getProperty('visible');
expect(visible).assertEqual('true');
expect(visible).assertEqual('false');

// ❌ 错误 - 不要使用 assertTrue/assertFalse
const enabled = await component.getProperty('enabled');
expect(enabled).assertTrue(); // 错误！enabled 是字符串 "true"，不是布尔值
```

### 7.3 数值属性断言

```typescript
// 获取数值属性（string 类型）
const width = await component.getProperty('width'); // "100.00vp"

// 方法1：字符串比较
expect(width).assertEqual('100.00vp');

// 方法2：使用 assertContain
expect(width).assertContain('100');

// 方法3：提取数值后比较（需要转换）
const widthValue = parseFloat(width);
expect(widthValue).assertEqual(100);
```

---

## 八、UiTest 并发调用注意事项

### 8.1 问题说明

UiTest API 不支持多个 Driver 实例并发执行。如果在多个测试套件中同时创建 Driver，会导致冲突。

### 8.2 正确做法

```typescript
// ✅ 正确 - 测试套件内共享 Driver
describe('ComponentTest', () => {
  let driver: Driver;

  beforeEach(async () => {
    driver = await Driver.create();
    await Utils.sleep(500);
  });

  it('test1', async () => {
    const comp = await driver!.findComponent(ON.id('xxx')); // ✅ 使用共享 driver
  });

  it('test2', async () => {
    const comp = await driver!.findComponent(ON.id('yyy')); // ✅ 使用共享 driver
  });
});
```

### 8.3 错误做法

```typescript
// ❌ 错误 - 多个测试套件并发执行
export default function testsuite() {
  textBasicTest();      // 创建共享 Driver
  textStyleTest();      // 并发创建！（冲突）
}
```

---

## 九、测试页面配置

### 9.1 Test.json 配置

```json
{
  "description": "Configuration for UI Component Tests",
  "driver": {
    "type": "OHJSUnitTest",
    "test-timeout": "600000",
    "bundle-name": "com.example.xts.test",
    "module-name": "entry_test",
    "shell-timeout": "600000"
  },
  "kits": [
    {
      "test-file-name": ["TestHap.hap"],
      "type": "AppInstallKit",
      "cleanup-apps": true
    }
  ]
}
```

### 9.2 测试页面导入

```typescript
import Utils from '../common/Utils';

beforeAll(async (done: Function) => {
  await Utils.pushPage('MainAbility/pages/ComponentTestPage', done);
  await Utils.sleep(1000);
  driver = await Driver.create();
  await Utils.sleep(1000);
  done();
});
```

---

## 十、常见测试场景

### 10.1 组件属性测试

```typescript
it('testComponentProperty001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: Function) => {
  const component = await driver.waitForComponent(ON.id('text-id'), 2000);

  if (component) {
    const fontSize = await component.getProperty('fontSize');
    expect(fontSize).assertEqual('16.00fp');
  } else {
    expect().assertFail();
  }

  done();
});
```

### 10.2 组件点击测试

```typescript
it('testComponentClick001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: Function) => {
  const component = await driver.waitForComponent(ON.id('button-id'), 2000);

  if (component) {
    await component.click();
    await Utils.sleep(500);

    const clicked = await component.getProperty('clicked');
    expect(clicked).assertEqual('true');
  } else {
    expect().assertFail();
  }

  done();
});
```

### 10.3 文本输入测试

```typescript
it('testTextInput001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async (done: Function) => {
  const component = await driver.waitForComponent(ON.id('input-id'), 2000);

  if (component) {
    await component.setText('test input');
    await Utils.sleep(500);

    const text = await component.getProperty('text');
    expect(text).assertEqual('test input');
  } else {
    expect().assertFail();
  }

  done();
});
```

---

## 十一、UiTest 参考文档

### 11.1 官方文档位置

```
docs/zh-cn/application-dev/application-test/uitest-guidelines.md
docs/zh-cn/application-dev/reference/apis-test-kit/js-apis-uitest.md
```

### 11.2 文档阅读建议

1. **uitest-guidelines.md** - UiTest 测试框架使用指南
   - 测试框架使用方法
   - 测试用例编写规范
   - 测试最佳实践

2. **js-apis-uitest.md** - UiTest API 参考
   - Driver API 详细说明
   - ON 定位器完整列表
   - Component 操作方法参考
