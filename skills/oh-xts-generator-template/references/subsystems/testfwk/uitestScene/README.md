# UiTestScene 辅助包文档

> **OpenHarmony UiTest 接口功能验证辅助包**

## 概述

UiTestScene 是专为 OpenHarmony UiTest 接口功能验证设计的辅助包，提供标准化的 UI 界面元素，用于测试各种 UI 自动化操作和交互功能。该辅助包与动静态语法测试套配合使用，确保 uitest 接口功能验证的准确性和一致性。

## 基本信息

| 属性 | 值 |
|------|-----|
| 包名 | `com.uitestScene.acts` |
| 启动能力 | `com.uitestScene.acts.MainAbility` |
| 版本 | 1.0.0 |
| 用途 | 为 uitest 接口提供标准化的 UI 界面进行功能验证 |

## 目录结构

```
uitestScene/
├── AppScope/
│   ├── app.json5                 # 应用配置
│   └── resources/
├── entry/
│   ├── src/
│   │   ├── main/
│   │   │   ├── ets/
│   │   │   │   ├── entryability/   # 能力入口
│   │   │   │   │   └── EntryAbility.ts
│   │   │   │   └── pages/          # 页面文件 **重点**
│   │   │   │       ├── Index.ets   # 主页面（主要测试界面）
│   │   │   │       ├── second.ets  # 第二页面
│   │   │   │       ├── third.ets   # 第三页面
│   │   │   │       ├── fourth.ets  # 第四页面
│   │   │   │       ├── scroll.ets  # 滚动测试页面
│   │   │   │       ├── drag.ets    # 拖拽测试页面
│   │   │   │       ├── pinch.ets   # 捏合测试页面
│   │   │   │       ├── wearList.ets # 穿戴设备列表页面
│   │   │   │       └── five.ets    # 并行测试页面
│   │   │   ├── resources/         # 资源文件
│   │   │   └── module.json5       # 模块配置
│   │   └── ohosTest/
│   │       └── ets/test/         # 测试代码（无需修改）
│   ├── hvigor/                   # 构建配置
│   └── signature/                # 签名文件
└── BUILD.gn                      # 构建脚本
```

## 界面内容详情

### 主页面 (Index.ets)

#### 主要测试元素

| 元素类型 | ID/Key | 用途 |
|---------|--------|------|
| Toast 测试按钮 | `id='toastBtn'` | 测试 toast 显示功能 |
| Dialog 测试按钮 | `id='dialogBtn'` | 测试 dialog 弹窗功能 |
| 下一页按钮 | `key='my-key'` | 跳转到第二页面 |
| 双击测试按钮 | `id='twiceBtn'` | 双击跳转测试 |
| 悬停测试按钮 | `key='jump'` | 悬停状态变化测试 |
| 滚动测试按钮 | `id='scrollBtn'` | 跳转到滚动测试页面 |
| 并行测试按钮 | `id='to5'` | 跳转到并行测试页面 |

#### 输入框测试

| 元素类型 | ID | 用途 |
|---------|-----|------|
| 文本输入框 | `id='changTest'` | 可编辑的文本输入框 |
| 上下文输入框 | `id='changContext'` | 另一个文本输入框 |

#### 复选框测试

| 元素类型 | ID | 状态 |
|---------|-----|------|
| 复选框1 | `id='hi'` | 未选中 |
| 复选框2 | `id='go'` | 已选中 |

#### 禁用元素测试

| 元素类型 | ID | 状态 |
|---------|-----|------|
| 禁用按钮 | `id='enableFalse'` | 禁用状态 |

#### 滚动容器

| 元素类型 | ID | 用途 |
|---------|-----|------|
| 滚动区域 | `id='parentScroll'` | 垂直滚动容器 |

### 第二页面 (second.ets)

| 元素类型 | ID | 用途 |
|---------|-----|------|
| 返回按钮 | - | 返回主页面 |
| 文本输入框 | `id='changTest'` | 可编辑文本框 |
| 上下文输入框 | `id='changContext'` | 另一个文本输入框 |

### 其他功能页面

| 页面文件 | 功能描述 |
|---------|---------|
| third.ets | 长按双击跳转测试 |
| fourth.ets | 长按跳转测试 |
| scroll.ets | 滚动功能测试 |
| drag.ets | 拖拽操作测试 |
| pinch.ets | 捏合手势测试 |
| wearList.ets | 穿戴设备界面测试 |
| five.ets | 并行测试场景 |

## 辅助包使用方法

### 启动辅助包

```typescript
await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility')
```

### 关闭辅助包

```typescript
await stopApplication('com.uitestScene.acts')
```

### 完整使用示例

```typescript
/**
 * @tc.name testUiTestHelperExample
 * @tc.number SUB_TESTFWK_UITEST_HELPER_001
 * @tc.desc 辅助包使用示例
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testUiTestHelperExample', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, async () => {
  console.log(`${TestTag}, test start`);
  try {
    // 1. 创建 Driver 实例
    let driver = Driver.create();
    
    // 2. 启动辅助包
    await startAbility('com.uitestScene.acts', 'com.uitestScene.acts.MainAbility');
    
    // 3. 等待界面加载
    await driver.delayMs(2000);
    
    // 4. 查找控件
    let toastBtn = await driver.findComponent(ON.id('toastBtn'));
    expect(toastBtn).assertNotNull();
    
    // 5. 执行操作
    await toastBtn.click();
    
    // 6. 验证结果
    let enabled = await toastBtn.isEnabled();
    expect(enabled).assertTrue();
    
  } catch (error) {
    console.log(`${TestTag}, error: ${JSON.stringify(error)}`);
    expect().assertFail();
  } finally {
    // 7. 关闭辅助包
    await stopApplication('com.uitestScene.acts');
  }
  console.log(`${TestTag}, test end`);
});
```

## 辅助包扩展指南

### 添加新页面

#### 1. 创建页面文件

在 `entry/src/main/ets/pages/` 目录下创建新的页面文件：

```typescript
/**
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
import router from '@system.router';

@Entry
@Component
struct NewFeaturePage {
  @State featureText: string = '初始文本'

  build() {
    Flex({ direction: FlexDirection.Column, alignItems: ItemAlign.Center }) {
      Text('新功能测试页面')
        .fontWeight(FontWeight.Bold)
        .margin({ top: 20 })

      Button('测试按钮')
        .id('testButton')
        .margin({ top: 10 })
        .onClick(() => {
          // 按钮点击处理
        })

      TextInput({ placeholder: '请输入', text: '' })
        .id('testInput')
        .width(200)
        .height(50)
        .margin({ top: 10 })

      Button('返回')
        .margin({ top: 20 })
        .onClick(() => {
          router.back()
        })
    }
    .width('100%')
    .height('100%')
  }
}
```

#### 2. 注册新页面

在 `entry/src/main/resources/base/profile/main_pages.json` 中注册：

```json
{
  "src": [
    "pages/Index",
    "pages/second",
    "pages/third",
    "pages/NewFeaturePage"
  ]
}
```

#### 3. 添加跳转入口

在 `Index.ets` 中添加跳转按钮：

```typescript
Button() {
  Text('新功能测试')
    .fontWeight(FontWeight.Bold)
}
.id('newFeatureBtn')
.type(ButtonType.Capsule)
.margin({ top: 5 })
.onClick(() => {
  console.info('jump to new feature page')
  router.push({ uri: 'pages/NewFeaturePage' })
})
```

### ID 命名规范

为测试元素添加 ID 时，应遵循以下规范：

- **唯一性**: 确保每个 ID 在整个应用中是唯一的
- **描述性**: ID 应该描述元素的用途或功能
- **一致性**: 使用一致的命名风格（建议 camelCase）
- **可读性**: 避免使用缩写，使用完整的描述性名称

**示例**：
```typescript
// ✅ 良好的 ID 命名
Button('Toast测试').id('toastTestButton')
TextInput({}).id('emailInputField')
Checkbox({}).id('termsCheckbox')

// ❌ 不好的 ID 命名
Button('Toast测试').id('btn1')
TextInput({}).id('input2')
Checkbox({}).id('cb3')
```

### 添加新组件

#### 组件属性设置

```typescript
Button('测试按钮')
  .id('testButton')              // 测试ID（必需）
  .enabled(true)                 // 启用状态
  .visibility(Visibility.Visible) // 可见性
  .width(200)                    // 宽度
  .height(50)                    // 高度
  .onClick(() => {
    // 事件处理
  })
```

#### 状态管理

```typescript
@Entry
@Component
struct TestPage {
  @State isToggled: boolean = false
  @State inputText: string = ''
  @State selectedIndex: number = 0

  build() {
    Column() {
      Toggle({ type: ToggleType.Switch, isOn: this.isToggled })
        .id('toggleSwitch')
        .onChange((isOn: boolean) => {
          this.isToggled = isOn
        })

      TextInput({ text: this.inputText })
        .id('textInput')
        .onChange((value: string) => {
          this.inputText = value
        })
    }
  }
}
```

#### 手势支持

```typescript
Text('手势测试')
  .id('gestureText')
  .width(200)
  .height(200)
  .backgroundColor(Color.Blue)
  .gesture(
    TapGesture()
      .onAction(() => {
        console.info('Tap detected')
      })
  )
  .gesture(
    LongPressGesture()
      .onAction(() => {
        console.info('Long press detected')
      })
  )
```

## 常见测试场景

### 基础点击测试

```typescript
let button = await driver.findComponent(ON.id('toastBtn'))
expect(button).assertNotNull()
await button.click()
```

### 文本输入测试

```typescript
let input = await driver.findComponent(ON.id('changTest'))
expect(input).assertNotNull()
await input.setInputText('测试输入文本')
let text = await input.getText()
expect(text).assertEqual('测试输入文本')
```

### 禁用状态验证

```typescript
let disabledBtn = await driver.findComponent(ON.id('enableFalse'))
expect(disabledBtn).assertNotNull()
let enabled = await disabledBtn.isEnabled()
expect(enabled).assertFalse()
```

### 页面跳转测试

```typescript
let nextBtn = await driver.findComponent(ON.key('my-key'))
expect(nextBtn).assertNotNull()
await nextBtn.click()
await driver.delayMs(1000)
// 验证新页面
let newPageElement = await driver.findComponent(ON.text('新页面'))
expect(newPageElement).assertNotNull()
```

## 注意事项

### 界面加载时间

- 辅助包启动后需要等待界面完全加载
- 建议使用 `driver.delayMs(2000)` 确保界面稳定
- 避免立即操作未加载完成的元素

### 元素查找

- 始终检查 `findComponent` 返回值是否为空
- 使用合适的定位策略（ID、文本、类型等）
- 组合定位可以提高定位准确性

### 资源清理

- 测试完成后必须关闭辅助包
- 避免多个辅助包同时运行
- 确保系统资源正确释放

## 版本信息

| 属性 | 值 |
|------|-----|
| 当前版本 | 1.0.0 |
| 兼容性 | OpenHarmony API 10+ |
| 更新日期 | 2026-03-23 |

## 相关文档

- [uitest 模块配置](../UiTest.md) - 详细的模块配置和使用说明
- [OpenHarmony UiTest API 参考](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-test-kit/UiTest.md)
- [OpenHarmony UI 组件开发指南](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/application-test/)
- [OpenHarmony UiTest 错误码文档](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-test-kit/errorcode-UiTest.md)
