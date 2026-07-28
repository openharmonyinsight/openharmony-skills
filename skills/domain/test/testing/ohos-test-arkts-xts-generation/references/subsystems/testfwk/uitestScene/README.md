# UiTestScene 辅助包文档

> **OpenHarmony UiTest 接口功能验证辅助包**

## 概述

UiTestScene 是专为 OpenHarmony UiTest 接口功能验证设计的辅助包，提供标准化的 UI 界面元素，用于测试各种 UI 自动化操作和交互功能。该辅助包与动静态语法测试套配合使用，确保 uitest 接口功能验证的准确性和一致性。

## 基本信息

- **包名**: `com.uitestScene.acts`
- **启动能力**: `com.uitestScene.acts.MainAbility`
- **版本**: 1.0.0
- **用途**: 为 uitest 接口提供标准化的 UI 界面进行功能验证

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
│   │   │   │   └── pages/          # 页面文件
│   │   │   │       ├── Index.ets   # 主页面（主要测试界面）
│   │   │   │       ├── second.ets  # 第二页面
│   │   │   │       ├── third.ets   # 第三页面
│   │   │   │       ├── fourth.ets  # 第四页面
│   │   │   │       ├── scroll.ets   # 滚动测试页面
│   │   │   │       ├── drag.ets     # 拖拽测试页面
│   │   │   │       ├── pinch.ets    # 捏合测试页面
│   │   │   │       ├── wearList.ets  # 穿戴设备列表页面
│   │   │   │       └── five.ets    # 并行测试页面
│   │   │   ├── resources/         # 资源文件
│   │   │   │   └── base/
│   │   │   │       ├── element/    # 字符串资源
│   │   │   │       ├── media/      # 媒体资源
│   │   │   │       └── profile/    # 配置文件
│   │   │   └── module.json5       # 模块配置
│   │   └── ohosTest/
│   │       └── ets/test/         # 测试代码
│   ├── hvigor/                   # 构建配置
│   └── signature/                # 签名文件
└── BUILD.gn                      # 构建脚本
```

## 当前界面内容

### 1. 主页面 (Index.ets)

**主要测试元素：**
- **Toast 测试按钮**: `id='toastBtn'` - 测试 toast 显示功能
- **Dialog 测试按钮**: `id='dialogBtn'` - 测试 dialog 弹窗功能
- **下一页按钮**: `key='my-key'` - 跳转到第二页面
- **双击测试按钮**: `id='twiceBtn'` - 双击跳转测试
- **悬停测试按钮**: `key='jump'` - 悬停状态变化测试
- **滚动测试按钮**: `id='scrollBtn'` - 跳转到滚动测试页面
- **并行测试按钮**: `id='to5'` - 跳转到并行测试页面

**输入框测试：**
- **文本输入框**: `id='changTest'` - 可编辑的文本输入框
- **上下文输入框**: `id='changContext'` - 另一个文本输入框

**复选框测试：**
- **复选框1**: `id='hi'` - 未选中的复选框
- **复选框2**: `id='go'` - 已选中的复选框

**禁用元素测试：**
- **禁用按钮**: `id='enableFalse'` - 禁用状态的按钮

**滚动容器：**
- **滚动区域**: `id='parentScroll'` - 垂直滚动容器

### 2. 第二页面 (second.ets)

**主要测试元素：**
- **返回按钮**: 返回主页面
- **文本输入框**: `id='changTest'` - 可编辑文本框
- **上下文输入框**: `id='changContext'` - 另一个文本输入框

### 3. 其他功能页面

- **第三页面**: 长按双击跳转测试
- **第四页面**: 长按跳转测试
- **滚动页面**: 滚动功能测试
- **拖拽页面**: 拖拽操作测试
- **捏合页面**: 捏合手势测试
- **穿戴列表页面**: 穿戴设备界面测试
- **并行测试页面**: 并行测试场景

## 辅助包扩展指南

### 添加新页面的方式和思路

#### 1. 确定测试需求

在添加新页面之前，需要明确：
- 需要测试的 uitest 接口功能
- 需要验证的 UI 组件类型
- 需要测试的交互场景
- 特定设备的适配需求

#### 2. 创建新页面文件

在 `entry/src/main/ets/pages/` 目录下创建新的页面文件：

```
entry/src/main/ets/pages/
├── Index.ets          # 主页面
├── second.ets         # 第二页面
├── NewFeaturePage.ets  # 新功能页面（示例）
```

#### 3. 页面文件结构

新页面文件应遵循以下结构：

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
  // 状态变量
  @State featureText: string = '初始文本'

  build() {
    // 页面布局
    Flex({ direction: FlexDirection.Column, alignItems: ItemAlign.Center }) {
      Text('新功能测试页面')
        .fontWeight(FontWeight.Bold)
        .margin({ top: 20 })

      // 测试组件
      Button('测试按钮')
        .id('testButton')  // 重要：为测试添加唯一的ID
        .margin({ top: 10 })
        .onClick(() => {
          // 按钮点击处理
        })

      TextInput({ placeholder: '请输入', text: '' })
        .id('testInput')   // 重要：为测试添加唯一的ID
        .width(200)
        .height(50)
        .margin({ top: 10 })

      // 返回按钮
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

#### 4. 注册新页面

在 `entry/src/main/resources/base/profile/main_pages.json` 中注册新页面：

```json
{
  "src": [
    "pages/Index",
    "pages/second",
    "pages/third",
    "pages/NewFeaturePage"  // 添加新页面
  ]
}
```

#### 5. 在主页面添加跳转按钮

在 `Index.ets` 中添加跳转到新页面的按钮：

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
  console.info('jump to new feature page over')
})
```

#### 6. ID 命名规范

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

### 添加新组件的方式和思路

#### 1. 确定组件类型

根据测试需求，确定需要添加的组件类型：

- **基础组件**: Button, Text, TextInput, Checkbox, Radio, etc.
- **容器组件**: Flex, Column, Row, Stack, Grid, List, etc.
- **媒体组件**: Image, Video, etc.
- **画布组件**: Canvas, etc.
- **高级组件**: Web, XComponent, etc.

#### 2. 组件属性设置

为测试组件设置必要的属性：

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

#### 3. 状态管理

使用 `@State` 装饰器管理组件状态：

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

#### 4. 交互事件处理

为组件添加交互事件，以便测试验证：

```typescript
Button('点击测试')
  .id('clickTestButton')
  .onClick(() => {
    console.info('Button clicked')
    // 触发状态变化
    this.clickCount++
  })
  .onHover((isHover: boolean) => {
    console.info(`Button hover: ${isHover}`)
  })
  .onTouch((event: TouchEvent) => {
    console.info(`Button touch: ${event.type}`)
  })
```

#### 5. 手势支持

为需要手势测试的组件添加手势支持：

```typescript
Text('手势测试')
  .id('gestureText')
  .width(200)
  .height(200)
  .backgroundColor(Color.Blue)
  .gesture(
    // 点击手势
    TapGesture()
      .onAction(() => {
        console.info('Tap detected')
      })
  )
  .gesture(
    // 长按手势
    LongPressGesture()
      .onAction(() => {
        console.info('Long press detected')
      })
  )
  .gesture(
    // 滑动手势
    SwipeGesture({ direction: SwipeDirection.Horizontal })
      .onAction(() => {
        console.info('Swipe detected')
      })
  )
```

#### 6. 复杂布局示例

对于复杂的测试场景，可以创建复杂的布局：

```typescript
Column() {
  // 标题
  Text('复杂布局测试')
    .fontSize(20)
    .margin({ bottom: 10 })

  // 行布局
  Row() {
    Button('按钮1').id('button1').margin({ right: 10 })
    Button('按钮2').id('button2').margin({ right: 10 })
    Button('按钮3').id('button3')
  }
  .margin({ bottom: 10 })

  // 网格布局
  Grid() {
    ForEach([1, 2, 3, 4, 5, 6], (item: number) => {
      GridItem() {
        Text(`Item ${item}`)
          .id(`gridItem${item}`)
      }
    })
  }
  .columnsTemplate('1fr 1fr 1fr')
  .rowsTemplate('1fr 1fr')
  .columnsGap(10)
  .rowsGap(10)
  .margin({ bottom: 10 })

  // 列表布局
  List() {
    ForEach(['Item 1', 'Item 2', 'Item 3'], (item: string) => {
      ListItem() {
        Text(item)
          .id(`listItem${item.replace(' ', '')}`)
      }
    })
  }
  .width('100%')
  .height(200)
}
```

### 辅助包测试支持

#### 1. 设备适配

针对不同设备类型进行适配：

```typescript
// 平板设备适配
@Entry
@Component
struct TestPage {
  @State deviceType: string = 'default'

  aboutToAppear() {
    // 检测设备类型
    this.deviceType = this.detectDeviceType()
  }

  build() {
    if (this.deviceType === 'tablet') {
      TabletLayout()
    } else {
      PhoneLayout()
    }
  }

  detectDeviceType(): string {
    // 设备检测逻辑
    return 'phone'
  }
}
```

#### 2. 状态记录

为测试提供状态记录功能：

```typescript
@Entry
@Component
struct TestPage {
  @State testLogs: string[] = []

  private addLog(message: string) {
    this.testLogs.push(`${new Date().toLocaleTimeString()}: ${message}`)
    console.info(`[TEST LOG] ${message}`)
  }

  build() {
    Column() {
      Button('测试操作')
        .id('testButton')
        .onClick(() => {
          this.addLog('Button clicked')
        })

      // 显示测试日志
      ForEach(this.testLogs, (log: string) => {
        Text(log).fontSize(12).margin({ top: 2 })
      })
    }
  }
}
```

#### 3. 测试数据重置

提供测试数据重置功能：

```typescript
@Entry
@Component
struct TestPage {
  @State testCounter: number = 0
  @State testText: string = ''

  resetTestData() {
    this.testCounter = 0
    this.testText = ''
    console.info('Test data reset')
  }

  build() {
    Column() {
      Text(`计数: ${this.testCounter}`)
        .id('counterText')

      Button('增加计数')
        .id('incrementButton')
        .onClick(() => {
          this.testCounter++
        })

      Button('重置数据')
        .id('resetButton')
        .onClick(() => {
          this.resetTestData()
        })
    }
  }
}
```

## 版本信息

- **当前版本**: 1.0.0
- **兼容性**: OpenHarmony API 10+
- **更新日期**: 2026-02-26

## 相关文档

- [uitest 模块配置](../UiTest.md) - 详细的模块配置和使用说明
- [OpenHarmony UiTest API 参考](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-test-kit/UiTest.md)
- [OpenHarmony UI 组件开发指南](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/application-test/)
- [OpenHarmony UiTest 错误码文档](https://gitee.com/openharmony/docs/blob/master/zh-cn/application-dev/reference/apis-test-kit/errorcode-UiTest.md)