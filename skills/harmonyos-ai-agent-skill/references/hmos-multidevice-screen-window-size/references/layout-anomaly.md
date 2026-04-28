# 布局异常修复指南

## 类别定义

**布局异常**是指组件的布局方式或布局容器选择不当，导致在不同屏幕尺寸或设备类型上出现组件堆叠、遮挡、截断等显示问题。

### 核心特征

- 布局容器（`Stack`、`Column`、`Row`、`Flex`、`GridRow` 等）选择或配置不当
- 组件之间出现非预期的堆叠、遮挡或截断
- 问题通常与布局容器的特性、断点参考系或嵌套结构相关

### 常见现象

| 现象 | 描述 | 典型场景 |
|-----|------|---------|
| 组件堆叠 | 组件之间发生重叠，而不是按预期排列 | Stack 层叠布局误用 |
| 组件遮挡 | 某个组件挡住了其他组件的内容 | z-index 问题或布局容器选择错误 |
| 组件截断 | 组件内容超出容器边界被裁剪 | 滚动容器缺失或高度限制错误 |
| 布局错乱 | 组件排列顺序或位置不符合预期 | Flex/栅格断点配置错误 |

### 根因分类

1. **容器选择问题**：误用 `Stack` 层叠布局实现本应垂直/水平排列的组件
2. **断点参考问题**：`GridRow` 等响应式组件的断点参考系配置错误
3. **滚动缺失问题**：可滚动内容未使用 `Scroll` 容器或滚动容器高度设置错误
4. **嵌套结构问题**：布局容器嵌套过深或嵌套方式不当

---

## Bug 修复场景

### 场景 1：局部容器变窄时，GridRow 没有随之降列

#### 问题描述

当局部容器（如侧边栏、抽屉、底部面板）宽度发生变化时，内部的 `GridRow` 仍保持原来的列数，导致子项被挤压、重叠或堆叠。

#### 根因分析

`GridRow` 的断点参考系错误地绑定到了窗口宽度，而非组件自身宽度：

```typescript
// 问题代码
GridRow({ 
  breakpoints: { reference: BreakpointsReference.WindowSize }  // 错误：参考窗口尺寸
}) {
  // 子项
}
```

这样会导致：
- 局部容器变窄时断点不切换
- 栅格仍维持大宽度下的列数
- 子项被挤压、重叠或堆叠

#### 修复方案

如果响应式对象是局部组件，而不是整个窗口，应改为参考组件尺寸：

```typescript
// 修复后
GridRow({ 
  breakpoints: { reference: BreakpointsReference.ComponentSize }  // 正确：参考组件尺寸
}) {
  // 子项
}
```

---

### 场景 2：Stack 层叠布局导致底部元素遮挡主内容

#### 问题描述

页面底部有导航栏或工具栏，但主内容区域被底部栏遮挡，无法完整显示。

#### 根因分析

使用 `Stack` 作为根容器，配合 `alignContent: Alignment.BottomStart` 定位底部元素时，底部元素会层叠覆盖在上层元素上方：

```typescript
// 问题代码
Stack({ alignContent: Alignment.BottomStart }) {
  ContentArea()  // 被遮挡
  BottomBar()    // 覆盖在 ContentArea 底部区域
}
```

#### 修复方案

如果预期是垂直排列、互不遮挡，应改用 `Column`：

```typescript
// 修复后
Column() {
  ContentArea()
  BottomBar()
}
```

---

### 场景 3：Row/Column 子组件溢出截断

#### 问题描述

线性容器（`Row`/`Column`）内子组件总尺寸超出容器宽度时，子组件被截断而非按需隐藏，导致内容显示不完整。

#### 根因分析

子组件缺少 `displayPriority` 属性，容器无法在空间不足时按优先级自动隐藏低优先级组件：

```typescript
// 问题代码
ForEach(items, (item, index) => {
  Text(item)
    .fontSize(14)
})
```

#### 修复方案

为容器内每个子组件添加 `.displayPriority()` 优先级，并确保容器设置了明确尺寸约束：

```typescript
// 子组件上设置优先级，值越大越优先显示
Text(item)
  .displayPriority(totalCount - index)

// 容器必须设置宽度约束
Row({ space: 12 }) { /* ... */ }
  .width('100%')
```

---

## 场景 4：分屏模式下应用界面出现图片截断、文字挤压、组件遮挡等

#### 问题描述

应用未对分屏模式做适配，导致在分屏模式下，图片，文字和组件出现截断，挤压，遮挡等问题

#### 根因分析

未根据断点动态调整布局和设置小窗口布局。
```typescript
// 以设置图片的高度为例，在小窗口布局中高度为24vp，手机全屏时高度为48vp。使用横纵向断点判断，设置具体的属性值。
Image($r('app.media.background'))
  .height(200)
  .aspectRatio(1)
```

#### 修复方案

根据断点动态调整布局并设置小窗口布局。保证页面布局能够完整显示，避免出现截断、挤压、堆叠等现象。

```typescript
// 以设置图片的高度为例，在小窗口布局中高度为24vp，手机全屏时高度为48vp。使用横纵向断点判断，设置具体的属性值。
Image($r('app.media.background'))
  .height(this.currentWidthBreakpoint === WidthBreakpoint.WIDTH_SM  &&
    (this.currentHeightBreakpoint === HeightBreakpoint.HEIGHT_SM  ||
     this.currentHeightBreakpoint === HeightBreakpoint.HEIGHT_MD) ? 50 : 200)
  .aspectRatio(1)
```

### 场景 5：横屏模式下相机预览偏移截断

#### 问题描述

相机预览使用 `XComponent` + `.position()` 定位，横屏切换后预览画面未居中，偏移到屏幕左侧导致右侧出现黑边或画面截断。

#### 根因分析

使用 `.position()` 绝对定位组件时，仅按短边计算了组件尺寸，横屏时未计算长边方向的居中偏移，导致组件始终贴左上角：

```typescript
// 问题代码：position 固定为 (0, 0)
XComponent({}).position({ x: 0, y: 0 })
```

#### 修复方案

获取屏幕长短边尺寸，横屏时通过 `(longSide - componentWidth) / 2` 计算居中偏移量：

```typescript
const shortSide = this.getUIContext().px2lpx(Math.min(screenWidthPx, screenHeightPx));
const longSide = this.getUIContext().px2lpx(Math.max(screenWidthPx, screenHeightPx));
const ratio = 9 / 16;
 const isPortrait = screenWidthPx < screenHeightPx;
  if (isPortrait) {
    this.cameraWidth = shortSide;
    this.cameraHeight = shortSide / ratio;
    this.cameraScreenOffsetX = 0;
    this.cameraScreenOffsetY = 0;
  } else {
    this.cameraWidth = shortSide / ratio;
    this.cameraHeight = shortSide;
    // 横屏时计算居中偏移
    this.cameraScreenOffsetX = (longSide - this.cameraWidth) / 2;
    this.cameraScreenOffsetY = 0;
  }
```
position 使用动态偏移
```typescript
XComponent({}).position({ x: this.cameraScreenOffsetX + 'lpx', y: 0 })
```

---

## AI 判断规则

1. **检查容器选择**：如果页面需要"轮播图/主内容 + 底部固定栏"垂直排列，使用 `Column`；如果需要"背景 + 悬浮按钮/浮层"层叠效果，使用 `Stack`。

2. **检查 GridRow 参考系**：如果变化的是整个页面或窗口，使用 `BreakpointsReference.WindowSize`；如果变化的是局部面板、卡片、抽屉、底部区域等组件宽度，使用 `BreakpointsReference.ComponentSize`。

3. **检查遮挡关系**：发现底部区域遮挡主内容时，检查根容器是否为 `Stack` + `Alignment.Bottom/Top`。

4. **检查子组件溢出截断**：当 `Row` 中横向排列多个固定宽度子组件（标签、按钮、徽章等），且未设置 `displayPriority` 时，在小宽度设备上会出现截断。`Row` 容器必须设置 `.width('100%')` 或固定宽度，`displayPriority` 才能正确触发按需隐藏。优先级值设计：靠前的项目给更高的值（如 `totalCount - index`），确保重要内容优先展示。

