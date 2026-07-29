# UiTest 模块配置

> **模块信息**
> - 模块名称: UiTest（UI 自动化测试框架）
> - 所属子系统: testfwk
> - Kit包: @kit.TestKit
> - API 声明文件: ${OH_ROOT}/interface/sdk-js/api/@ohos.UiTest.d.ts
> - 版本: 1.3.0
> - 更新日期: 2026-04-02

## 模块概述

UiTest 是 OpenHarmony 的 UI 自动化测试框架，用于测试应用的 UI 交互和界面元素。

### 主要功能

- UI 自动化测试
- 组件交互测试
- 界面元素查找和操作
- 属性验证

### 核心 API

| API 名称 | 类型 | 说明 |
|---------|------|------|
| `Driver` | 类 | UI 驱动类 |
| `DriverStatic` | 接口 | 静态 UI 驱动方法 |
| `UiComponent` | 类 | UI 组件类 |
| `UiDriver` | 接口 | UI 驱动接口 |

### 测试特点

- 需要 UI 环境
- 支持元素定位和操作
- 支持属性验证
- 支持异步操作
- **依赖辅助包**：通过辅助包提供 UI 界面进行接口功能验证

## 辅助包配置

### 辅助包信息

uitest 接口的功能验证通常需要依赖 UI 界面中显示的内容，因此测试套需要与辅助包搭配使用。

#### 辅助包路径
- **动态测试套辅助包**：`OH_ROOT/test/xts/acts/testfwk/uitestScene`
- **静态测试套辅助包**：`OH_ROOT/test/xts/acts/testfwk/uitestScene`
- **说明**：动静态语法测试套使用同一个辅助包

#### 辅助包启动方法
测试用例中通过以下方法拉起辅助包：
```typescript
await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility')
```

#### 辅助包使用场景
- 对辅助包界面中的控件进行查找和操作
- 验证 uitest 接口功能
- 提供标准化的 UI 界面用于测试

#### 辅助包操作示例
```typescript
// 1. 启动辅助包（使用封装的 startAbility 方法）
await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility');

// 2. 等待界面加载
await driver.delayMs(2000);

// 3. 查找辅助包中的控件
let button = await driver.findComponent(ON.id('test_button'));
let text = await driver.findComponent(ON.text('测试文本'));

// 4. 执行操作验证 uitest 接口
if (button) {
    await button.click();
    // 验证操作结果
}

// 5. 关闭辅助包（使用封装的 stopApplication 方法）
await stopApplication('com.uitestScene.acts');
```

#### 注意事项
- 辅助包提供标准化的测试界面，确保测试环境一致性
- 测试用例需要正确处理辅助包的启动和关闭
- 建议在测试前后添加适当的等待时间，确保界面加载完成
- **重要**: 启动辅助包必须使用封装的 `startAbility` 方法，而不是系统自带的 startAbility
- **重要**: 关闭辅助包必须使用封装的 `stopApplication` 方法，而不是 `stopAbility`

## 参考资料配置

**参考文档路径**：
```
API 参考: ${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-test-kit/UiTest.md
开发指南: ${OH_ROOT}/docs/zh-cn/application-dev/application-test/
错误码文档: ${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-test-kit/errorcode-UiTest.md
辅助包文档: ${OH_ROOT}/test/xts/acts/testfwk/uitestScene/README.md
```

**查找方式**：
```bash
# 方式1：从配置读取
使用本配置文件中指定的参考资料路径

# 方式2：在 docs 仓中查找
grep -r "Driver" ${OH_ROOT}/docs/ | grep -i "test"
grep -r "UiComponent" ${OH_ROOT}/docs/
grep -r "UiDriver" ${OH_ROOT}/docs/
grep -r "uitestScene" ${OH_ROOT}/test/ | grep -i "uitest"

# 方式3：查找辅助包方法
grep -r "stopApplication" ${OH_ROOT}/test/xts/acts/testfwk/ | grep -i "test"
grep -r "startAbility" ${OH_ROOT}/test/xts/acts/testfwk/ | grep -i "test"
grep -r "delegator.executeShellCommand" ${OH_ROOT}/test/xts/acts/testfwk/ | grep -i "test"
```

## UiTest 错误码测试经验总结

> UiTest 错误码测试经验（错误码表、场景示例、触发条件要点）详见独立文件 [UiTest_error_codes.md](UiTest_error_codes.md)。

## 代码模板

> **⚠️ UiTest 导入规范**: 必须使用 `import {Driver, ON} from '@ohos.UiTest'`（大写 T）。详见 `references/conventions/uitest_framework.md` 第二章。

### 基础 UiTest 测试模板

> **语法模式**：ArkTS-Dyn（动态语法）

```typescript
/**
 * @tc.name testDriverTest001
 * @tc.number SUB_ARKXTEST_UITEST_DRIVER_TEST_0100
 * @tc.desc 测试 UiTest Driver 功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testDriverTest001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  // 1. 创建 Driver 实例
  let driver = Driver.create();

  // 2. 查找 UI 元素
  let element = await driver.findComponent(ON.id('buttonId'));

  // 3. 验证元素存在
  expect(element).not().assertNull();

  // 4. 执行操作
  await element.click();
});
```

### 元素定位和操作模板

> **语法模式**：ArkTS-Dyn（动态语法）

```typescript
/**
 * @tc.name testComponentOperation001
 * @tc.number SUB_ARKXTEST_UITEST_COMPONENT_0100
 * @tc.desc 测试 UI 组件定位和操作
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testComponentOperation001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  // 1. 创建 Driver
  let driver = Driver.create();

  // 2. 多种定位方式
  let byId = ON.id('buttonId');
  let byText = ON.text('按钮文本');
  let byType = ON.type('Button');
  let byCombined = ON.id('buttonId').type('Button');

  // 3. 查找组件
  let component = await driver.findComponent(byId);

  // 4. 验证组件存在
  if (component) {
    // 5. 获取组件属性
    let text = await component.getText();
    let enabled = await component.isEnabled();

    // 6. 执行操作
    await component.click();
    await component.setInputText('test input');

    // 7. 验证结果
    expect(text).assertEqual('预期文本');
    expect(enabled).assertTrue();
  } else {
    console.log('Component not found');
  }
});
```

## 辅助包启动和使用方法

### 1. 辅助包启动

在 uitest 测试用例中通过以下方法启动辅助包：

```typescript
await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility')
```

**重要**: 必须使用封装的 `startAbility` 方法，而不是系统自带的 startAbility。

### 2. 界面等待

启动辅助包后，需要等待界面加载完成：

```typescript
await driver.delayMs(2000) // 等待2秒确保界面加载完成
```

### 3. 元素定位和操作

#### 定位方式示例：

> **语法模式**：ArkTS-Dyn（动态语法）

```typescript
// 通过ID定位
let button = await driver.findComponent(ON.id('toastBtn'))
let input = await driver.findComponent(ON.id('changTest'))

// 通过文本定位
let buttonText = await driver.findComponent(ON.text('toast'))

// 通过类型定位
let buttons = await driver.findComponent(ON.type('Button'))

// 组合定位
let specificButton = await driver.findComponent(ON.id('toastBtn').type('Button'))
```

#### 操作示例：

```typescript
// 点击按钮
await button.click()

// 输入文本
await input.setInputText('测试文本')

// 获取文本
let text = await button.getText()

// 获取状态
let enabled = await button.isEnabled()
let visible = await button.isVisible()
```

### 4. 页面跳转

```typescript
// 跳转到其他页面
await button.click() // 点击跳转按钮

// 返回主页面
await router.back()
```

### 5. 辅助包关闭

测试完成后关闭辅助包：

```typescript
await stopApplication('com.uitestScene.acts')
```

### 6. startAbility 和 stopApplication 方法说明

#### startAbility 方法

**重要**: 启动辅助包使用封装的 `startAbility` 方法，而不是系统自带的 startAbility。

```typescript
async function startAbility(bundleName: string, abilityName: string) {
    await delegator.executeShellCommand(`aa start -b ${bundleName} -a ${abilityName}`).then(result => {
        console.info(`ComponentTest, start abilityFinished: ${result}`)
    }).catch((err: BusinessError) => {
        console.error(`ComponentTest, start abilityFailed: ${err}`)
    })
}
```

**参数**:
- `bundleName` - 要启动的应用包名
- `abilityName` - 要启动的能力名称

**功能**: 通过 shell 命令启动指定应用的能力

#### stopApplication 方法

**重要**: 关闭辅助包使用封装的 `stopApplication` 方法，而不是 `stopAbility`。

```typescript
async function stopApplication(bundleName: string) {
    await delegator.executeShellCommand(`aa force-stop ${bundleName} `).then(result => {
        console.info(`ComponentTest, stop application finished: ${result}`)
    }).catch((err: BusinessError) => {
        console.error(`ComponentTest,stop application failed: ${err}`)
    })
}
```

**参数**: `bundleName` - 要关闭的应用包名

**功能**: 通过 shell 命令强制关闭指定应用

## UI操作接口功能验证方式

### 验证原则

当测试用例需要验证UI操作接口功能时，必须验证交互后的页面状态变化，以确保接口操作确实产生了预期效果。

### 验证方法

1. **借助辅助包中其他页面的控件内容进行验证**
   - 可以通过定位其他页面中的控件来验证页面状态变化
   - 不局限于主页面（如 Index.ets）
   - 可以在不同页面间跳转并验证多个页面状态

2. **与 index.ets 中的控件进行交互验证**
   - 可以在辅助包的 index.ets 页面中查找并操作控件
   - 验证操作后的界面变化或控件属性变化

3. **多页面交互验证流程**
   ```typescript
   // 示例：验证点击按钮后跳转到新页面并验证新页面内容
   it('testUIOperation001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
     // 1. 启动辅助包
     await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility');
     await driver.delayMs(2000);

     // 2. 在当前页面操作
      let button = await driver.findComponent(ON.id('nextPageBtn'));
      expect(button).not().assertNull();
     await button.click();
     await driver.delayMs(1000);

     // 3. 验证页面跳转后状态变化（查找新页面中的控件）
      let newPageTitle = await driver.findComponent(ON.text('新页面标题'));
      expect(newPageTitle).not().assertNull();

     // 4. 验证新页面中控件的状态
     let newButton = await driver.findComponent(ON.id('newButton'));
     if (newButton) {
       let enabled = await newButton.isEnabled();
       expect(enabled).assertTrue();
     }

     // 5. 关闭辅助包
     await stopApplication('com.uitestScene.acts');
   });
   ```

### 实现参考

- 具体实现方式可以参考历史用例中的UI操作验证模式
- 参考用例位置：${OH_ROOT}/test/xts/acts/testfwk/uitestScene/
- 重点查看：
  - 多页面交互用例
  - 页面状态验证用例
  - 控件属性变化验证用例

### 注意事项

- 页面跳转后需要适当等待界面加载完成
- 验证时要确保找到的控件确实是目标控件（使用唯一ID或组合定位）
- 可以结合多个控件的状态变化来综合验证接口功能
- 对于涉及页面变化的操作，建议验证操作前后两个页面的状态

## 设备行为差异

| API | 有效设备 | 其他设备行为 |
|-----|---------|------------|
| drag, dragBetween, Component.dragTo | Phone, Tablet, PC/2in1, TV | 无效 |
| setDisplayRotation, setDisplayRotationEnabled, pressHome | Phone, Tablet, PC/2in1, TV | 无效 |
| crownRotate | 仅 Smartwatch | 其他设备返回 17000005 |
| touchPadMultiFingerSwipe | 仅 PC/2in1 | 其他设备返回 17000005 |

## 废弃 API

以下 API 自 API 9 起废弃，仅保留用于错误码测试：

| 废弃 API | 替代 API | 说明 |
|---------|---------|------|
| `By` / `BY` | `On` / `ON` | 组件选择器 |
| `UiComponent` | `Component` | UI 组件类 |
| `UiDriver` | `Driver` | UI 驱动类 |
| `@ohos.application.abilityDelegatorRegistry` | `@ohos.app.ability.abilityDelegatorRegistry` | AbilityDelegator 注册 |

废弃 API 不应在新测试用例中使用，仅用于错误码测试覆盖。
