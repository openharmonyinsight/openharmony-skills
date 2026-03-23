# 02. 布局样式接口测试指南

> 二、布局与样式接口（Layout & Style APIs）- 控制怎么排、长什么样

---

## 接口说明

布局与样式接口用来**控制怎么排、长什么样**，包括布局、对齐、样式等属性。

### 常见接口分类

| 类型 | 示例 |
|------|------|
| 尺寸布局 | `width()`、`height()`、`size()` |
| 内外边距 | `padding()`、`margin()`、`constraintSize()` |
| 对齐方式 | `align()`、`alignContent()`、`justifyContent()`、`alignItems()` |
| 背景样式 | `backgroundColor()`、`backgroundImage()`、`backgroundBlur()` |
| 边框样式 | `border()`、`borderWidth()`、`borderColor()`、`borderRadius()` |
| 透明度 | `opacity()`、`blendMode()` |
| 文本样式 | `fontSize()`、`fontColor()`、`fontWeight()`、`fontStyle()`、`textAlign()` |
| 显示控制 | `visibility()`、`display()` |

---

## 测试重点

### 1. 尺寸属性测试

**测试目的**：验证宽度、高度、内外边距等尺寸属性。

#### 页面侧

```typescript
// 尺寸测试
Text('Size Test')
  .id('text_size')
  .width('200vp')
  .height('5%')
  .padding({ top: 10, bottom: 10, left: 20, right: 20 })

// 百分比尺寸
Text('Percentage Size')
  .id('text_percent')
  .width('50%')
  .height('10%')

// 约束尺寸
Text('Constraint Size')
  .id('text_constraint')
  .constraintSize({ minWidth: 100, maxWidth: 300 })
```

#### 测试侧

```typescript
/**
 * @tc.name   textWidth_0100
 * @tc.number SUB_ARKUI_TEXT_WIDTH_PARAM_0100
 * @tc.desc   测试 Text 的 width 属性 - 200vp
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('textWidth_0100', Level.LEVEL0, async () => {
  let strJson: string = getInspectorByKey('text_size');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  expect(obj.$attrs.width).assertEqual('200.00vp');
  expect(obj.$attrs.height).assertEqual('5.00%');
});
```

### 2. 边框样式测试

**测试目的**：验证边框宽度、颜色、圆角等属性。

#### 页面侧

```typescript
// 完整边框设置
Button('Border Test')
  .id('button_border_full')
  .border({
    width: { left: 2, right: 2, top: 2, bottom: 2 },
    color: '#FF0000',
    radius: 10,
    style: BorderStyle.Solid
  })

// 简化边框设置
Button('Border Simple')
  .id('button_border_simple')
  .borderWidth(2)
  .borderColor('#0000FF')
  .borderRadius(8)
```

#### 测试侧

```typescript
/**
 * @tc.name   buttonBorder_0100
 * @tc.number SUB_ARKUI_BUTTON_BORDER_PARAM_0100
 * @tc.desc   测试 Button 的边框属性
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('buttonBorder_0100', Level.LEVEL0, async () => {
  let strJson: string = getInspectorByKey('button_border_full');
  let obj: Record<string, ESObject> = JSON.parse(strJson);

  // 验证边框宽度
  expect(obj.$attrs.borderLeftWidth).assertEqual('2.00vp');
  expect(obj.$attrs.borderRightWidth).assertEqual('2.00vp');

  // 验证边框颜色（注意 #AARRGGBB 格式）
  let borderColor: string = obj.$attrs.borderLeftColor as string;
  let isRed = borderColor === '#FFFF0000' || borderColor.toLowerCase() === '#ffff0000';
  expect(isRed).assertTrue();

  // 验证圆角
  expect(obj.$attrs.borderRadius).assertEqual('10.00vp');
});
```

### 3. 背景样式测试

**测试目的**：验证背景颜色、图片、透明度等属性。

#### 页面侧

```typescript
// 背景颜色
Column('Background Color')
  .id('column_bg_color')
  .backgroundColor('#0000FF')
  .width('200vp')
  .height('5%')

// 背景透明度
Column('Background Opacity')
  .id('column_bg_opacity')
  .backgroundColor('#FF0000')
  .opacity(0.5)
  .width('200vp')
  .height('5%')

// 圆角背景
Column('Background Radius')
  .id('column_bg_radius')
  .backgroundColor('#00FF00')
  .borderRadius(15)
  .width('200vp')
  .height('5%')
```

#### 测试侧

```typescript
/**
 * @tc.name   columnBackgroundColor_0100
 * @tc.number SUB_ARKUI_COLUMN_BACKGROUNDCOLOR_PARAM_0100
 * @tc.desc   测试 Column 的 backgroundColor 属性
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('columnBackgroundColor_0100', Level.LEVEL0, async () => {
  let strJson: string = getInspectorByKey('column_bg_color');
  let obj: Record<string, ESObject> = JSON.parse(strJson);

  // 验证背景颜色（注意 #AARRGGBB 格式）
  let bgColor: string = obj.$attrs.backgroundColor as string;
  let isBlue = bgColor === '#FF0000FF' || bgColor.toLowerCase() === '#ff0000ff';
  expect(isBlue).assertTrue();
});

/**
 * @tc.name   columnOpacity_0100
 * @tc.number SUB_ARKUI_COLUMN_OPACITY_PARAM_0100
 * @tc.desc   测试 Column 的 opacity 属性
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('columnOpacity_0100', Level.LEVEL0, async () => {
  let strJson: string = getInspectorByKey('column_bg_opacity');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  expect(obj.$attrs.opacity).assertEqual('0.50');
});
```

### 4. 对齐方式测试

**测试目的**：验证容器组件的子元素对齐属性。

#### 页面侧

```typescript
// 水平对齐
Row('Align Test')
  .id('row_align_start')
  .width('100%')
  .height('5%')
  .alignItems(VerticalAlign.Top)

Row('Align Test')
  .id('row_align_center')
  .width('100%')
  .height('5%')
  .alignItems(VerticalAlign.Center)

Row('Align Test')
  .id('row_align_end')
  .width('100%')
  .height('5%')
  .alignItems(VerticalAlign.Bottom)

// 主轴对齐
Column('Justify Test')
  .id('column_justify_start')
  .width('100%')
  .height('10%')
  .justifyContent(FlexAlign.Start)

Column('Justify Test')
  .id('column_justify_center')
  .width('100%')
  .height('10%')
  .justifyContent(FlexAlign.Center)

Column('Justify Test')
  .id('column_justify_end')
  .width('100%')
  .height('10%')
  .justifyContent(FlexAlign.End)
```

#### 测试侧

```typescript
/**
 * @tc.name   rowAlignItems_0100
 * @tc.number SUB_ARKUI_ROW_ALIGNITEMS_PARAM_0100
 * @tc.desc   测试 Row 的 alignItems 属性 - VerticalAlign.Top
 * @tc.type   FUNCTION
 * @tc.size   SMALLTEST
 * @tc.level  LEVEL0
 */
it('rowAlignItems_0100', Level.LEVEL0, async () => {
  let strJson: string = getInspectorByKey('row_align_start');
  let obj: Record<string, ESObject> = JSON.parse(strJson);
  expect(obj.$attrs.alignItems).assertEqual('VerticalAlign.Top');
});
```

---

## CSS 概念对应

布局样式接口与 CSS 有相似的对应关系：

| ArkUI | CSS | 说明 |
|-------|-----|------|
| `width()` | `width` | 宽度 |
| `height()` | `height` | 高度 |
| `padding()` | `padding` | 内边距 |
| `margin()` | `margin` | 外边距 |
| `backgroundColor()` | `background-color` | 背景色 |
| `border()` | `border` | 边框 |
| `borderRadius()` | `border-radius` | 圆角 |
| `opacity()` | `opacity` | 透明度 |
| `fontSize()` | `font-size` | 字号 |
| `fontColor()` | `color` | 文字颜色 |
| `textAlign()` | `text-align` | 文字对齐 |

---

## 测试注意事项

### 布局样式接口特定注意事项

#### 1. 尺寸返回值格式

尺寸属性返回值通常带单位：

```typescript
// 设置 .width('200vp')
// 返回 '200.00vp'

// 设置 .height('5%')
// 返回 '5.00%'

// 设置 .padding(10)
// 返回 '10.00vp'
```

#### 2. 边框属性名称

边框属性在组件树中以独立属性存在：

```typescript
// 设置 .border({ width: 2, color: '#FF0000' })
// 返回属性：
// - borderLeftWidth: '2.00vp'
// - borderRightWidth: '2.00vp'
// - borderLeftColor: '#FFFF0000'
// - borderRightColor: '#FFFF0000'
```

### 通用规范引用

| 规范项 | 说明 | 参考文档 |
|--------|------|---------|
| 颜色格式断言 | 组件树返回 `#AARRGGBB` 格式 | [_common.md](./_common.md) |
| 等价类参数精简 | 同类型参数只需选择2个代表性值 | [_common.md](./_common.md) |

---

## 参考文档

- ArkUI 子系统通用配置：[_common.md](./_common.md)
- ArkUI 接口分类概览：[arkui.md](./arkui.md)
