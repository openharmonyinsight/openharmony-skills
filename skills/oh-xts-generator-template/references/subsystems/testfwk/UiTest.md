# UiTest 模块配置

> **模块信息**
> - 模块名称: UiTest（UI 自动化测试框架）
> - 所属子系统: testfwk
> - Kit包: @kit.TestKit
> - API 声明文件: ${OH_ROOT}/interface/sdk-js/api/@ohos.UiTest.d.ts
> - 版本: 1.2.0
> - 更新日期: 2026-02-27

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

## UiTest 错误码测试经验总结

### UiTest 模块特有错误码

UiTest 模块定义了以下特有错误码（详见 `errorcode-UiTest.md`）：

| 错误码 | 错误描述 | 是否可稳定测试 | 触发条件 | 说明 |
|--------|---------|---------------|---------|------|
| **17000001** | 初始化失败 | ❌ 不可稳定测试 | - | 测试环境默认已启用测试模式 |
| **17000002** | 异步调用未使用 await | ✅ 可测试 | 所有异步 API | 需要故意不使用 await |
| **17000003** | 断言失败 | ✅ 可测试 | assertComponentExist | **仅在此 API 失败时抛出** |
| **17000004** | 目标控件/窗口丢失 | ✅ 可测试 | Component/UiWindow 方法 | 对已消失的 UI 对象操作时触发 |
| **17000005** | 操作不支持 | ⚠️ 条件可测试 | **设备相关的 API** | 在不支持该操作的设备上调用时触发 |
| **17000007** | 参数不合法 | ✅ 可测试 | 所有 API | 传入 null、undefined、非法参数时触发 |

### 错误码测试场景示例

#### 1. 17000002 - 异步调用未使用 await

```typescript
/**
 * @tc.name testScrollToTop17000002
 * @tc.number UitestComponentErrorTest_001
 * @tc.desc scrollToTop 17000002 test.
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL3
 */
it('testScrollToTop17000002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  console.log(`${TestTag}, test_scrollToTop_17000002 start`);
  try {
    const driver = Driver.create();
    await startAbility('com.example.app', 'MainAbility');
    let button = await driver.findComponent(ON.type('Scroll'));
    // ❌ 故意不使用 await
    button.scrollToTop();
    expect().assertFail();
  }catch (e) {
    console.log(`${TestTag}, test_scrollToTop_17000002 error is: ${JSON.stringify(e)}`);
    expect(e.code).assertEqual(17000002);
  } finally {
    await stopApplication('com.example.app');
  }
  console.log(`${TestTag}, test_scrollToTop_17000002 end`);
})
```

#### 2. 17000004 - 目标控件/窗口丢失

**Component 示例**：

```typescript
/**
 * @tc.name testComponentClickInvisible17000004
 * @tc.number UitestMiscErrorTest_001
 * @tc.desc Component.click 17000004 test when component is invisible.
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL3
 */
it('testComponentClickInvisible17000004', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  console.log(`${TestTag}, test_Component_Click_Invisible_17000004 start`);
  try {
    const driver = Driver.create();
    await driver.delayMs(1000);

    try {
      // findComponent 返回组件或空，不抛异常
      const button = await driver.findComponent(ON.id('button'));
      if (button) {
        // 界面变化导致 button 不可见，这里会抛出 17000004
        await button.click();
        expect().assertFail();
      } else {
        // 组件不存在，无法测试 17000004 场景
        console.log(`${TestTag}, Component not found, skip test`);
      }
    } catch (error) {
      console.log(`${TestTag}, error is: ${JSON.stringify(error)}`);
      if (error instanceof BusinessError && error.code === InvisibleErrorCode) {
        // 控件不可见，操作失败 - 预期的错误码
        expect(true).assertTrue();
      } else {
        // 其他错误，测试失败
        console.log(`${TestTag}, Unexpected error: ${JSON.stringify(error)}`);
        expect().assertFail();
      }
    }
  } catch (error) {
    console.log(`${TestTag}, setup error: ${JSON.stringify(error)}`);
  }
  console.log(`${TestTag}, test_Component_Click_Invisible_17000004 end`);
})
```

**UiWindow 示例**：

```typescript
/**
 * @tc.name testUiWindowSetScreenRotationInvisible17000004
 * @tc.number UitestMiscErrorTest_002
 * @tc.desc UiWindow.setScreenRotation 17000004 test when window is closed.
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL3
 */
it('testUiWindowSetScreenRotationInvisible17000004', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  console.log(`${TestTag}, test_UiWindow_SetScreenRotation_Invisible_17000004 start`);
  try {
    const driver = Driver.create();
    await driver.delayMs(1000);

    try {
      const uiWindow = await driver.findWindow({ bundleName: 'com.example.app' });
      if (uiWindow) {
        // Window 已关闭，这里会抛出 17000004
        await uiWindow.setScreenRotation(0);
        expect().assertFail();
      } else {
        console.log(`${TestTag}, Window not found, skip test`);
      }
    } catch (error) {
      console.log(`${TestTag}, error is: ${JSON.stringify(error)}`);
      if (error instanceof BusinessError && error.code === InvisibleErrorCode) {
        expect(true).assertTrue();
      } else {
        console.log(`${TestTag}, Unexpected error: ${JSON.stringify(error)}`);
        expect().assertFail();
      }
    }
  } catch (error) {
    console.log(`${TestTag}, setup error: ${JSON.stringify(error)}`);
  }
  console.log(`${TestTag}, test_UiWindow_SetScreenRotation_Invisible_17000004 end`);
})
```

#### 3. 17000005 - 操作不支持（设备相关）

> **重要说明**：17000005 主要在**设备不支持**某些 API 时抛出，而不是对组件调用不支持的操作时抛出。

```typescript
/**
 * @tc.name testTouchPadMultiFingerSwipeUnsupported17000005
 * @tc.number UitestMiscErrorTest_003
 * @tc.desc touchPadMultiFingerSwipe 17000005 test on unsupported device.
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL3
 */
it('testTouchPadMultiFingerSwipeUnsupported17000005', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  console.log(`${TestTag}, test_TouchPadMultiFingerSwipe_Unsupported_17000005 start`);
  try {
    const driver = Driver.create();
    await driver.delayMs(1000);

    try {
      // touchPadMultiFingerSwipe 仅在 PC/2in1 设备上支持
      // 在 Phone 或其他设备上调用会抛出 17000005
      await driver.touchPadMultiFingerSwipe(3, UiDirection.UP);
      expect().assertFail();
    } catch (error) {
      console.log(`${TestTag}, error is: ${JSON.stringify(error)}`);
      if (error instanceof BusinessError) {
        if (error.code === UnsupportedErrorCode) {
          // 设备不支持该操作 - 预期的错误码
          expect(true).assertTrue();
        } else if (error.code === InvisibleErrorCode) {
          // UiWindow 不可见，也是可接受的结果
          console.log(`${TestTag}, UiWindow not visible (${error.code}), acceptable`);
          expect(true).assertTrue();
        } else {
          // 其他错误码，测试失败
          console.log(`${TestTag}, Unexpected error code: ${error.code}`);
          expect().assertFail();
        }
      } else {
        // 非 BusinessError，运行时异常
        console.log(`${TestTag}, Runtime error, not error code: ${JSON.stringify(error)}`);
        expect().assertFail();
      }
    }
  } catch (error) {
    console.log(`${TestTag}, setup error: ${JSON.stringify(error)}`);
  }
  console.log(`${TestTag}, test_TouchPadMultiFingerSwipe_Unsupported_17000005 end`);
})
```

#### 4. 17000003 - 断言失败

```typescript
/**
 * @tc.name testAssertComponentExistFail17000003
 * @tc.number UitestMiscErrorTest_004
 * @tc.desc assertComponentExist 17000003 test when component does not exist.
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL3
 */
it('testAssertComponentExistFail17000003', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, async () => {
  console.log(`${TestTag}, test_AssertComponentExist_Fail_17000003 start`);
  try {
    const driver = Driver.create();
    await driver.delayMs(1000);

    try {
      // 断言不存在的控件，会抛出 17000003
      await driver.assertComponentExist(ON.id('non_existent_component'));
      expect().assertFail();
    } catch (error) {
      console.log(`${TestTag}, error is: ${JSON.stringify(error)}`);
      if (error instanceof BusinessError && error.code === 17000003) {
        // 断言失败 - 预期的错误码
        expect(true).assertTrue();
      } else {
        // 其他错误码，测试失败
        console.log(`${TestTag}, Unexpected error code: ${error.code}`);
        expect().assertFail();
      }
    }
  } catch (error) {
    console.log(`${TestTag}, setup error: ${JSON.stringify(error)}`);
  }
  console.log(`${TestTag}, test_AssertComponentExist_Fail_17000003 end`);
})
```

### 错误码测试要点

#### 1. 17000001 不需要测试
- XTS 测试环境默认已启用测试模式
- `Driver.create()` 在测试环境中会成功初始化
- 无法稳定触发初始化失败场景

#### 2. 17000004 触发条件（重要）
- ⚠️ **对已消失的 UI 对象操作时触发**
- 触发场景：
  - 对已不在当前界面的 Component 调用 click、inputText 等方法
  - 对已关闭的 UiWindow 调用 setScreenRotation、getProperties 等方法
- ✅ **Component 示例**：
  ```typescript
  const component = await driver.findComponent(ON.id('button'));
  // 界面发生变化，button 已不可见
  await component.click(); // 抛出 17000004
  ```
- ✅ **UiWindow 示例**：
  ```typescript
  const uiWindow = await driver.findWindow({ bundleName: 'com.example.app' });
  // Window 已关闭
  await uiWindow.setScreenRotation(0); // 抛出 17000004
  ```
- ❌ **错误理解**：
  - 对 `null` 调用 click() 等方法**不会抛出错误码**，而是运行时异常
  - `null.click()` 会导致 TypeError，不是 UiTest 错误码

#### 3. 401 错误码触发条件（重要）
- ⚠️ **仅在入参错误时抛出**
- 触发场景：
  - 参数类型错误（如传入字符串但需要数字）
  - 参数缺失（必需参数未传）
  - 参数个数错误（参数数量不匹配）
- ❌ **不会触发 401 的场景**：
  - 控件不存在（findComponent 返回空，不抛异常）
  - 控件不可见（抛出 17000004）
  - 对 null/undefined 调用方法（运行时异常，非错误码）

#### 4. findComponent 行为说明（重要）
- ⚠️ **找不到控件时返回空，不抛异常**
- `driver.findComponent()` 找不到控件时**不会抛出异常**
- 返回值：空字符串 `''` 或 `null`（需要验证具体返回类型）
- **必须对返回值进行校验**后才能调用组件方法
- ✅ **正确用法**：
  ```typescript
  const component = await driver.findComponent(ON.id('button'));
  if (component) {  // 必须先检查返回值
    await component.click();
  }
  ```
- ❌ **错误用法**：
  ```typescript
  const component = await driver.findComponent(ON.id('button'));
  await component.click();  // 如果 component 为空会报错
  ```

#### 5. 17000003 错误码触发条件（重要）
- ⚠️ **仅在 assertComponentExist 失败时抛出**
- 触发场景：`assertComponentExist(on: On)` 断言失败
- **17000003 仅用于断言失败**
- ✅ **示例**：
  ```typescript
  try {
    await driver.assertComponentExist(ON.id('non_existent'));
  } catch (error) {
    // error.code === 17000003
  }
  ```

#### 6. 17000005 错误码触发条件（重要）
- ⚠️ **设备相关的 API 不支持时抛出**
- **触发场景**：在**不支持该操作的设备**上调用 API 时抛出 17000005
- **文档中的"设备行为差异"说明**：
  - 某些 API 仅在特定设备类型上生效（如 Phone、Tablet、PC/2in1、TV）
  - 在不支持的设备上调用会返回 17000005
  - 示例：`touchPadMultiFingerSwipe` 仅在 PC/2in1 设备上生效，其他设备返回 17000005
- **❌ 不会触发 17000005 的场景**：
  - 对不支持 pinch 的 Text 组件调用 pinch() - 不会抛异常，只是没有效果
  - 对不支持 rotate 的组件调用 rotate() - 不会抛异常，只是没有效果
- **测试建议**：
  - 17000005 测试需要**真实设备环境**
  - 无法在模拟环境中稳定测试
  - 建议通过检查设备类型来决定是否跳过测试

#### 7. 测试用例结构
- 使用 try-catch 包裹测试代码
- 内层 try-catch 捕获目标错误
- 外层 try-catch 处理初始化等设置错误
- 使用 `expect().assertFail()` 确保错误路径被执行

#### 8. 错误码断言
- UiTest 框架抛出的错误都是 BusinessError 类型，**无需判断 error 类型**
- 直接使用 `error.code` 获取错误码
- 避免使用 `error.message` 进行断言（可能不稳定）
- ✅ **正确用法**：
  ```typescript
  } catch (error) {
    expect(error.code).assertEqual(17000004);
  }
  ```
- ❌ **错误用法**：
  ```typescript
  } catch (error) {
    if (error instanceof BusinessError) {  // 不必要的类型检查
      expect(error.code).assertEqual(17000004);
    }
  }
  ```

#### 9. 测试编号规则
- 按错误码组织测试文件（如 UitestMiscErrorCode.test.ets）
- describe 名称反映错误码类型（如 UitestMiscErrorTest）
- @tc.number 格式：`{describe名}_{序号}`，序号从 0001 开始

## 代码模板

> **⚠️ 重要提示：UiTest 导入格式规范**
>
> - ✅ **正确格式**：`import {Driver, ON} from '@ohos.UiTest';`（大写的 T）
> - ❌ **错误格式**：`import {Driver, ON} from '@ohos.uitest';`（小写的 t）
>
> **编译错误**：使用小写的 `@ohos.uitest` 会导致以下编译错误：
> ```
> Cannot find module '@ohos.uitest' or its corresponding type declarations.
> ```
>
> **原因**：OpenHarmony SDK 中 UiTest 模块的正确导入路径为 `@ohos.UiTest`（大写 T），不是 `@ohos.uitest`（小写 t）。

### 基础 UiTest 测试模板

```typescript
/**
 * @tc.name testDriverTest001
 * @tc.number SUB_ARKXTEST_UITEST_DRIVER_TEST_001
 * @tc.desc 测试 UiTest Driver 功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testDriverTest001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  // 1. 创建 Driver 实例
  let driver = Driver.create();

  // 2. 查找 UI 元素， BY从api version 9开始废弃，不再维护
  let element = await driver.findComponent(BY.id('buttonId'));

  // 3. 验证元素存在
  expect(element).assertNotNull();

  // 4. 执行操作
  await element.click();
});
```

```typescript
/**
 * @tc.name testDriverTest001
 * @tc.number SUB_ARKXTEST_UITEST_DRIVER_TEST_001
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
  expect(element).assertNotNull();

  // 4. 执行操作
  await element.click();
});
```

### 元素定位和操作模板

```typescript
/**
 * @tc.name testComponentOperation001
 * @tc.number SUB_ARKXTEST_UITEST_COMPONENT_001
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

### 使用辅助包的测试模板

```typescript
/**
 * @tc.name testUiTestWithHelper001
 * @tc.number SUB_ARKXTEST_UITEST_HELPER_001
 * @tc.desc 使用辅助包测试 UiTest 接口功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testUiTestWithHelper001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  console.log(`${TestTag}, test_UiTest_With_Helper_001 start`);
  try {
    // 1. 创建 Driver 实例
    let driver = Driver.create();
    
    // 2. 启动辅助包
    await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility');
    
    // 3. 等待界面加载
    await driver.delayMs(2000);
    
    // 4. 查找辅助包中的控件
    let testButton = await driver.findComponent(ON.id('test_button'));
    let testText = await driver.findComponent(ON.text('测试文本'));
    
    // 5. 验证控件存在
    expect(testButton).assertNotNull();
    expect(testText).assertNotNull();
    
    // 6. 执行操作验证 uitest 接口
    await testButton.click();
    
    // 7. 获取操作结果
    let buttonEnabled = await testButton.isEnabled();
    let buttonText = await testButton.getText();
    
    // 8. 验证结果
    expect(buttonEnabled).assertTrue();
    expect(buttonText).assertEqual('点击后');
    
    // 9. 输入文本测试
    if (testButton) {
      await testButton.setInputText('测试输入');
      let inputText = await testButton.getText();
      expect(inputText).assertEqual('测试输入');
    }
    
  } catch (error) {
    console.log(`${TestTag}, test_UiTest_With_Helper_001 error is: ${JSON.stringify(error)}`);
    expect().assertFail();
  } finally {
    // 10. 关闭辅助包
    await stopApplication('com.uitestScene.acts');
  }
  console.log(`${TestTag}, test_UiTest_With_Helper_001 end`);
});
```

### 辅助包控件操作测试模板

```typescript
/**
 * @tc.name testUiTestComponentOperation001
 * @tc.number SUB_ARKXTEST_UITEST_COMPONENT_OPERATION_001
 * @tc.desc 测试辅助包中组件的定位和操作
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testUiTestComponentOperation001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  console.log(`${TestTag}, test_UiTest_Component_Operation_001 start`);
  try {
    // 1. 创建 Driver
    let driver = Driver.create();
    
    // 2. 启动辅助包
    await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility');
    await driver.delayMs(2000);
    
    // 3. 多种定位方式测试
    let byId = ON.id('test_button');
    let byText = ON.text('测试文本');
    let byType = ON.type('Button');
    let byCombined = ON.id('test_button').type('Button');
    
    // 4. 查找组件
    let component = await driver.findComponent(byId);
    
    // 5. 验证组件存在
    if (component) {
      // 6. 获取组件属性
      let text = await component.getText();
      let enabled = await component.isEnabled();
      let visible = await component.isVisible();
      
      // 7. 执行操作
      await component.click();
      await component.setInputText('辅助包测试');
      
      // 8. 验证操作结果
      expect(text).assertEqual('测试文本');
      expect(enabled).assertTrue();
      expect(visible).assertTrue();
      
      // 9. 验证输入文本
      let inputResult = await component.getText();
      expect(inputResult).assertEqual('辅助包测试');
      
    } else {
      console.log(`${TestTag}, Component not found in helper package`);
      expect().assertFail();
    }
    
  } catch (error) {
    console.log(`${TestTag}, test_UiTest_Component_Operation_001 error is: ${JSON.stringify(error)}`);
    expect().assertFail();
  } finally {
    // 10. 关闭辅助包
    await stopApplication('com.uitestScene.acts');
  }
  console.log(`${TestTag}, test_UiTest_Component_Operation_001 end`);
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

### 7. 完整使用流程示例

```typescript
/**
 * @tc.name testUiTestHelperCompleteFlow001
 * @tc.number SUB_ARKXTEST_UITEST_HELPER_COMPLETE_001
 * @tc.desc 完整的辅助包使用流程示例
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testUiTestHelperCompleteFlow001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  console.log(`${TestTag}, test_UiTest_Helper_Complete_Flow_001 start`);
  try {
    // 1. 启动辅助包（使用封装的 startAbility 方法）
    await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility');

    // 2. 等待界面加载
    await driver.delayMs(2000);

    // 3. 创建 Driver 实例
    let driver = Driver.create();

    // 4. 查找辅助包中的控件
    let testButton = await driver.findComponent(ON.id('toastBtn'));
    expect(testButton).assertNotNull();

    // 5. 执行操作
    await testButton.click();

    // 6. 验证操作结果
    let enabled = await testButton.isEnabled();
    expect(enabled).assertTrue();

    // 7. 其他测试操作...
    // ...

  } catch (error) {
    console.log(`${TestTag}, error is: ${JSON.stringify(error)}`);
    expect().assertFail();
  } finally {
    // 8. 关闭辅助包（使用封装的 stopApplication 方法）
    await stopApplication('com.uitestScene.acts');
  }
  console.log(`${TestTag}, test_UiTest_Helper_Complete_Flow_001 end`);
});
```

## 辅助包典型测试场景

### 1. 基础UI操作测试

```typescript
// 1. 启动辅助包
await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility')
await driver.delayMs(2000)

// 2. 查找并点击按钮
let toastBtn = await driver.findComponent(ON.id('toastBtn'))
expect(toastBtn).assertNotNull()
await toastBtn.click()

// 3. 验证操作结果
let enabled = await toastBtn.isEnabled()
expect(enabled).assertTrue()

// 4. 关闭辅助包
await stopApplication('com.uitestScene.acts')
```

### 2. 文本输入测试

```typescript
// 1. 启动辅助包
await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility')
await driver.delayMs(2000)

// 2. 查找输入框
let input = await driver.findComponent(ON.id('changTest'))
expect(input).assertNotNull()

// 3. 输入文本
await input.setInputText('测试输入文本')

// 4. 验证输入结果
let text = await input.getText()
expect(text).assertEqual('测试输入文本')

// 5. 关闭辅助包
await stopApplication('com.uitestScene.acts')
```

### 3. 禁用状态测试

```typescript
// 1. 启动辅助包
await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility')
await driver.delayMs(2000)

// 2. 查找禁用按钮
let disabledBtn = await driver.findComponent(ON.id('enableFalse'))
expect(disabledBtn).assertNotNull()

// 3. 验证禁用状态
let enabled = await disabledBtn.isEnabled()
expect(enabled).assertFalse()

// 4. 关闭辅助包
await stopApplication('com.uitestScene.acts')
```

### 4. 页面跳转测试

```typescript
// 1. 启动辅助包
await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility')
await driver.delayMs(2000)

// 2. 查找跳转按钮
let nextBtn = await driver.findComponent(ON.key('my-key'))
expect(nextBtn).assertNotNull()

// 3. 点击跳转
await nextBtn.click()
await driver.delayMs(1000)

// 4. 验证跳转成功（检查第二页面元素）
let secondInput = await driver.findComponent(ON.id('changTest'))
expect(secondInput).assertNotNull()

// 5. 返回主页面
await driver.pressBack()
await driver.delayMs(1000)

// 6. 关闭辅助包
await stopApplication('com.uitestScene.acts')
```

## 辅助包使用注意事项

### 1. 界面加载时间
- 辅助包启动后需要等待界面完全加载
- 建议使用 `driver.delayMs(2000)` 确保界面稳定
- 避免立即操作未加载完成元素

### 2. 元素查找
- 始终检查 `findComponent` 返回值是否为空
- 使用合适的定位策略（ID、文本、类型等）
- 组合定位可以提高定位准确性

### 3. 操作时序
- 某些操作可能需要等待时间（如动画）
- 避免连续快速操作导致界面响应异常
- 使用合理的间隔时间

### 4. 错误处理
- 始终使用 try-catch 包裹测试代码
- 正确处理元素不存在的情况
- 记录详细的错误信息用于调试

### 5. 资源清理
- 测试完成后必须关闭辅助包
- 避免多个辅助包同时运行
- 确保系统资源正确释放

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
     expect(button).assertNotNull();
     await button.click();
     await driver.delayMs(1000);

     // 3. 验证页面跳转后状态变化（查找新页面中的控件）
     let newPageTitle = await driver.findComponent(ON.text('新页面标题'));
     expect(newPageTitle).assertNotNull();

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

## 辅助包错误处理

### 常见错误及解决方案

1. **元素未找到**
   - 检查元素ID是否正确
   - 确认界面已完全加载
   - 增加等待时间

2. **操作超时**
   - 检查元素是否可见
   - 确认元素是否启用
   - 增加等待时间

3. **界面未响应**
   - 检查是否有其他应用干扰
   - 重启辅助包
   - 检查系统资源占用

## 辅助包测试最佳实践

1. **测试稳定性**
   - 使用固定的等待时间确保测试稳定性
   - 避免硬编码的数值，使用常量定义
   - 添加充分的日志输出用于调试

2. **测试覆盖**
   - 覆盖所有主要UI控件类型
   - 测试各种交互场景
   - 验证边界条件

3. **性能考虑**
   - 避免不必要的重复操作
   - 及时释放资源
   - 合理组织测试用例

## 测试覆盖目标

| API 类型 | 最低覆盖率要求 | 推荐覆盖率 |
|---------|--------------|----------|
| UiTest 核心 API | 90% | 100% |
| Driver API | 90% | 100% |
| UiComponent API | 85% | 95% |

## 测试注意事项

1. **UI 环境要求**
    - 需要 UI 环境支持
    - 元素查找需要正确的定位策略
    - 支持异步操作

2. **辅助包使用要求**
     - 必须正确启动和关闭辅助包
     - 使用封装的 `startAbility` 方法启动辅助包：`await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility')`
     - 使用封装的 `stopApplication` 方法关闭辅助包：`await stopApplication('com.uitestScene.acts')`
     - 确保在测试前后添加适当的等待时间，确保界面加载完成

3. **UI操作接口功能验证要求**（重要）
     - **强制要求**：验证UI操作接口功能时，必须验证交互后的页面状态变化
     - 可以借助辅助包中其他页面中控件的内容进行验证
     - 无需局限于 Index.ets，可以使用辅助包中的任意页面
     - 可以与 index.ets 中的控件进行交互并验证结果
     - 建议通过页面跳转、控件属性变化等多维度验证接口功能
     - 具体实现方式可参考历史用例
     - 详见：[UI操作接口功能验证方式](#ui操作接口功能验证方式)

4. **测试稳定性**
    - 注意界面加载时间
    - 使用合理的等待策略
    - 避免硬编码等待时间

5. **错误处理**
    - 始终检查 findComponent 返回值
    - 正确处理异步操作错误
    - 使用合适的错误码断言

## 通用配置继承

本模块继承 testfwk/_common.md 的通用配置：
- API Kit 映射
- 测试路径规范
- 参数测试规则
- 错误码测试规则

模块级配置可以覆盖通用配置的特定部分。
