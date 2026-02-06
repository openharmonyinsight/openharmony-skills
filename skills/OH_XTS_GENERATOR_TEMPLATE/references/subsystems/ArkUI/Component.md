# Component 模块配置

> **模块信息**
> - 所属子系统: ArkUI
> - 模块名称: Component
> - API 声明文件: @ohos.arkui.d.ts
> - 主要 API: Component, Column, Row, Text, Button, Image, List, Grid, Stack 等
> - 版本: 1.0.0
> - 更新日期: 2025-01-31

## 一、模块特有配置

### 1.1 模块概述

Component 模块包含 ArkUI 的基础组件和容器组件，是 ArkUI 子系统的核心模块。

### 1.2 API 声明文件

```
API声明文件: ${OH_ROOT}/interface/sdk-js/api/@ohos.arkui.d.ts
```

### 1.3 通用配置继承

本模块继承 ArkUI 子系统通用配置：

- **测试路径规范**: 见 `ArkUI/_common.md` 第 1.2 节
- **组件测试规则**: 见 `ArkUI/_common.md` 第 1.3.1 节
- **辅助工程配置**: 见 `ArkUI/_common.md` 第 2.2 节

## 二、模块特有 API 列表

### 2.1 核心组件API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| Column | 列容器组件 | LEVEL0 | 布局、对齐、间距 |
| Row | 行容器组件 | LEVEL0 | 布局、对齐、间距 |
| Text | 文本组件 | LEVEL0 | 内容、样式、事件 |
| Button | 按钮组件 | LEVEL0 | 点击、状态、样式 |
| Image | 图片组件 | LEVEL1 | 加载、缩放、事件 |
| List | 列表组件 | LEVEL1 | 滚动、渲染、性能 |
| Grid | 网格组件 | LEVEL1 | 布局、滚动、嵌套 |
| Stack | 堆叠容器 | LEVEL2 | 层叠、对齐、定位 |

### 2.2 核心属性API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| width | 宽度属性 | LEVEL0 | 数值、百分比、计算 |
| height | 高度属性 | LEVEL0 | 数值、百分比、计算 |
| padding | 内边距属性 | LEVEL1 | 统一设置、分别设置 |
| margin | 外边距属性 | LEVEL1 | 统一设置、分别设置 |
| backgroundColor | 背景颜色 | LEVEL1 | 颜色值、渐变 |
| opacity | 透明度 | LEVEL2 | 数值范围、动画 |

### 2.3 核心事件API

| API名称 | 说明 | 优先级 | 测试要点 |
|---------|------|--------|---------|
| onClick | 点击事件 | LEVEL0 | 触发、参数、冒泡 |
| onTouch | 触摸事件 | LEVEL1 | 触发、类型、坐标 |
| onAppear | 出现事件 | LEVEL1 | 触发时机、次数 |
| onDisAppear | 消失事件 | LEVEL1 | 触发时机、次数 |

## 三、模块特有测试规则

### 3.1 容器组件测试规则

#### 3.1.1 Column 组件测试

1. **布局测试**：
   - 测试子组件垂直排列
   - 验证对齐方式（alignItems）
   - 测试间距设置（space）

2. **尺寸测试**：
   - 测试 width/height 设置
   - 验证自适应内容
   - 测试约束条件

#### 3.1.2 Row 组件测试

1. **布局测试**：
   - 测试子组件水平排列
   - 验证对齐方式（alignItems、justifyContent）
   - 测试间距设置（space）

### 3.2 内容组件测试规则

#### 3.2.1 Text 组件测试

1. **内容测试**：
   - 测试普通文本
   - 测试富文本（span）
   - 测试超长文本截断

2. **样式测试**：
   - 测试字体大小
   - 测试字体颜色
   - 测试字体粗细

#### 3.2.2 Button 组件测试

1. **交互测试**：
   - 测试点击事件
   - 测试按钮状态
   - 测试禁用状态

2. **样式测试**：
   - 测试按钮类型
   - 测试自定义样式

### 3.3 列表组件测试规则

#### 3.3.1 List 组件测试

1. **渲染测试**：
   - 测试列表项渲染
   - 测试 ForEach 渲染
   - 测试 LazyForEach 渲染

2. **滚动测试**：
   - 测试列表滚动
   - 测试滚动位置
   - 测试滚动边界

3. **性能测试**：
   - 测试大列表性能
   - 测试列表项复用
   - 测试内存占用

## 四、模块特有代码模板

### 4.1 Column 组件测试模板

```typescript
/**
 * @tc.name ArkUI Column Layout Test
 * @tc.number SUB_ARKUI_COMPONENT_COLUMN_LAYOUT_001
 * @tc.desc 测试 Column 组件布局功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testColumnLayout001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 创建 Column 组件
  let column = new Column();

  // 2. 添加子组件
  column.appendChild(new Text());
  column.appendChild(new Button());

  // 3. 验证布局
  expect(column.children.length).assertEqual(2);

  // 4. 验证垂直排列
});
```

### 4.2 Text 组件测试模板

```typescript
/**
 * @tc.name ArkUI Text Content Test
 * @tc.number SUB_ARKUI_COMPONENT_TEXT_CONTENT_001
 * @tc.desc 测试 Text 组件内容功能
 * @tc.type FUNCTION
 * @tc.size MEDIUMTEST
 * @tc.level LEVEL1
 */
it('testTextContent001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
  // 1. 创建 Text 组件
  let text = new Text();

  // 2. 设置文本内容
  text.content = 'Hello World';

  // 3. 验证内容
  expect(text.content).assertEqual('Hello World');

  // 4. 验证渲染
});
```

## 五、待补充API

1. **动画相关API**：animate、animateTo、transition
2. **手势相关API**：gestureHandler、priorityGesture
3. **渲染控制API**：if、ForEach、LazyForEach
4. **路由相关API**：router、Navigator

## 六、版本历史

- **v1.0.0** (2025-01-31): 初始版本，定义 Component 模块配置
