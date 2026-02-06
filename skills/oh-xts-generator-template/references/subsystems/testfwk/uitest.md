# UiTest 模块配置

> **模块信息**
> - 模块名称: UiTest（UI 自动化测试框架）
> - 所属子系统: testfwk
> - Kit包: @kit.TestKit
> - API 声明文件: @ohos.uitest.d.ts
> - 版本: 1.0.0
> - 更新日期: 2026-02-05

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

## 参考资料配置

**参考文档路径**：
```
API 参考: ${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-test-kit/uitest.md
开发指南: ${OH_ROOT}/docs/zh-cn/application-dev/application-test/
错误码文档: ${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-test-kit/errorcode-uitest.md
```

**查找方式**：
```bash
# 方式1：从配置读取
使用本配置文件中指定的参考资料路径

# 方式2：在 docs 仓中查找
grep -r "Driver" ${OH_ROOT}/docs/ | grep -i "test"
grep -r "UiComponent" ${OH_ROOT}/docs/
grep -r "UiDriver" ${OH_ROOT}/docs/
```

## UiTest 错误码测试经验总结

### UiTest 模块特有错误码

UiTest 模块定义了以下特有错误码（详见 `errorcode-uitest.md`）：

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
- @tc.number 格式：`{describe名}_{序号}`，序号从 001 开始

## 代码模板

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

  // 2. 查找 UI 元素
  let element = await driver.findComponent(BY.id('buttonId'));

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

2. **测试稳定性**
   - 注意界面加载时间
   - 使用合理的等待策略
   - 避免硬编码等待时间

3. **错误处理**
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

## 版本历史

- **v1.0.0** (2026-02-05): 从 _common.md 拆分，初始版本
