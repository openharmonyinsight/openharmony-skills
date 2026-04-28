# 断点系统完全指南

## 目录

1. [断点设计原理](#断点设计原理)
2. [横向断点](#横向断点)
3. [纵向断点](#纵向断点)
4. [断点监听](#断点监听)

---

## 断点设计原理

断点(Breakpoint)是响应式布局中最常用的特征，用于将窗口宽度或窗口高宽比划分为不同的范围。当窗口尺寸从一个断点变化到另一个断点时，页面布局会相应调整。

### 核心概念

- **横向断点**: 基于窗口宽度(vp)划分，代表窗口的宽度特征
- **纵向断点**: 基于窗口高宽比划分，代表窗口的相对高度特征

### 为什么需要两种断点？

**原则一: 布局拉通**
> 两个宽度相近的窗口，页面布局应保持一致，断点归一。

例如:
- 手机竖屏(374vp宽) 和 折叠屏外屏竖屏(345vp宽) → 都使用sm断点
- 平板横屏(1137vp宽) 和 三折叠G态横屏(1107vp宽) → 都使用lg断点

**原则二: 差异化设计**
> 高度相对宽度较小的窗口(横向窗口或类方形窗口)，页面布局进行差异化设计，增加纵向断点。

---

## 横向断点

横向断点以应用窗口宽度为判断条件，建议划分为5个区间:

| 断点名称 | 窗口宽度(vp) | 典型设备场景 |
|---------|-------------|-------------|
| **xs** | (0, 320) | 智能穿戴设备 |
| **sm** | [320, 600) | 手机竖屏、折叠屏外屏竖屏、三折叠F态竖屏 |
| **md** | [600, 840) | 手机横屏、双折叠展开态、三折叠M态 |
| **lg** | [840, 1440) | 平板、三折叠G态、部分手机横屏 |
| **xl** | [1440, +∞) | 电脑、大尺寸平板 |

### 系统横向断点

优先使用系统接口 getWindowWidthBreakpoint() 获取当前窗口的横向断点值:

```typescript
// 伪代码：获取当前横向断点
let widthBp: WidthBreakpoint = uiContext.getWindowWidthBreakpoint();
// 返回枚举: WIDTH_XS(0) / WIDTH_SM(1) / WIDTH_MD(2) / WIDTH_LG(3) / WIDTH_XL(4)
```

| 名称      | 值  | 说明                                  |
|-----------|-----|---------------------------------------|
| WIDTH_XS  | 0   | 窗口宽度小于320vp                     |
| WIDTH_SM  | 1   | 窗口宽度大于等于320vp，且小于600vp    |
| WIDTH_MD  | 2   | 窗口宽度大于等于600vp，且小于840vp    |
| WIDTH_LG  | 3   | 窗口宽度大于等于840vp，且小于1440vp   |
| WIDTH_XL  | 4   | 窗口宽度大于等于1440vp                |

### 自定义横向断点

仅在需要定义和系统断点枚举值不同的断点区间时使用自定义断点，完整实现见 [assets/BreakpointConstants.ets](../assets/BreakpointConstants.ets):

```typescript
// 伪代码：自定义断点常量（仅在系统断点区间不满足需求时使用）
const BREAKPOINT_XS = 320;  const BREAKPOINT_SM = 600;
const BREAKPOINT_MD = 840;  const BREAKPOINT_LG = 1440;

function getBreakpointByWidth(width) {
  if (width < 320) return 'xs';
  else if (width < 600) return 'sm';
  else if (width < 840) return 'md';
  else if (width < 1440) return 'lg';
  else return 'xl';
}
```

---

## 纵向断点

纵向断点以应用窗口高宽比为判断条件:

| 断点名称   | 高宽比范围 | 窗口类型 |
|--------|-----------|---------|
| **sm** | (0, 0.8) | 横向窗口 |
| **md** | [0.8, 1.2) | 类方形窗口 |
| **lg** | [1.2, +∞) | 纵向窗口 |

### 系统纵向断点

优先使用系统接口 getWindowHeightBreakpoint() 获取当前窗口的纵向断点值:

```typescript
// 伪代码：获取当前纵向断点
let heightBp: HeightBreakpoint = uiContext.getWindowHeightBreakpoint();
// 返回枚举: HEIGHT_SM(0) / HEIGHT_MD(1) / HEIGHT_LG(2)
```

| 名称      | 值  | 说明                                |
|-----------|-----|-------------------------------------|
| HEIGHT_SM | 0   | 窗口高宽比小于0.8                   |
| HEIGHT_MD | 1   | 窗口高宽比大于等于0.8，且小于1.2    |
| HEIGHT_LG | 2   | 窗口高宽比大于等于1.2               |

### 自定义纵向断点

仅在需要定义和系统断点枚举值不同的断点区间时使用，完整实现见 [assets/BreakpointConstants.ets](../assets/BreakpointConstants.ets):

```typescript
// 伪代码：根据高宽比计算纵向断点
function getVerticalBreakpoint(width, height) {
  ratio = height / width;
  if (ratio < 0.8) return 'sm';    // 横向窗口
  else if (ratio < 1.2) return 'md'; // 类方形窗口
  else return 'lg';                  // 纵向窗口
}
```

---

## 断点监听

### ⚠️ 重要原则：断点必须可变化

使用自定义断点逻辑时，必须确保断点能够响应窗口尺寸变化，否则断点值将始终保持初始值，无法实现响应式布局。

```typescript
// ❌ 错误: 断点值固定，不会随窗口变化
@State currentBreakpoint: string = 'sm';  // 永远是 'sm'

// ✅ 推荐方案一: 使用 GridRow 内置断点系统（自动响应窗口变化）
GridRow({ columns: { sm: 2, md: 3, lg: 4 }, breakpoints: { value: ['320vp', '600vp', '840vp'] } }) { ... }

// ✅ 推荐方案二: 使用系统断点 + 窗口监听
let widthBp = uiContext.getWindowWidthBreakpoint();   // 获取初始值
windowClass.on('windowSizeChange', () => { widthBp = uiContext.getWindowWidthBreakpoint(); });

// ✅ 备选方案: 使用自定义断点 + 窗口监听 + AppStorage
windowClass.on('windowSizeChange', (size) => {
  AppStorage.setOrCreate('currentBreakpoint', getBreakpointByWidth(px2vp(size.width)));
});
// 组件中通过 @StorageProp('currentBreakpoint') 获取
```

### 推荐方案二详细用法

使用系统断点枚举 + `windowSizeChange` 监听的完整实现见 [assets/SystemBreakpointExample.ets](../assets/SystemBreakpointExample.ets):

```typescript
// 伪代码：系统断点 + 窗口监听
@StorageProp('currentWidthBreakpoint') widthBp: WidthBreakpoint = WidthBreakpoint.WIDTH_SM;

aboutToAppear() {
  // 初始化 & 注册监听
  windowClass.on('windowSizeChange', () => {
    AppStorage.setOrCreate('currentWidthBreakpoint', uiContext.getWindowWidthBreakpoint());
  });
}
```

### 备选方案详细用法

使用自定义断点常量 + BreakpointObserver 的完整实现见 [assets/BreakpointObserver.ets](../assets/BreakpointObserver.ets):

```typescript
// 伪代码：自定义断点观察者
BreakpointObserver.init(context);  // 初始化，自动监听窗口变化
// 组件中通过 @StorageProp 获取当前断点
@StorageProp('currentBreakpoint') currentBreakpoint: string = 'sm';
```

---

## 注意事项

- 断点回调中只更新 UI 状态（布局切换、显隐切换），不要执行网络请求或复杂计算。

---

## 常见设备断点对照表

| 设备 | 状态 | 窗口宽度(vp) | 横向断点 | 纵向断点(竖屏) |
|-----|------|------------|---------|--------------|
| 手机 | 竖屏 | 360-390 | sm | lg |
| 手机 | 横屏 | 780-844 | md | sm |
| 折叠屏 | 折叠态竖屏 | 345-374 | sm | lg |
| 折叠屏 | 展开态竖屏 | 600-720 | md | lg |
| 三折叠 | F态竖屏 | 351 | sm | lg |
| 三折叠 | M态竖屏 | 702 | md | lg |
| 三折叠 | G态竖屏 | 1053 | lg | lg |
| 三折叠 | G态横屏 | 734 | md | sm |
| 阔折叠 | 折叠态 | 326 | sm | md |
| 阔折叠 | 展开态竖屏 | 440 | sm | lg |
| 阔折叠 | 展开态横屏 | 707 | md | sm |
| 大阔折 | 折叠态竖屏 | 459 | sm | lg |
| 大阔折 | 折叠态横屏 | 672 | md | sm |
| 大阔折 | 展开态竖屏 | 664 | md | lg |
| 大阔折 | 展开态横屏 | 939 | lg | sm |
| 平板 | 竖屏 | 768 | md | lg |
| 平板 | 横屏 | 1024 | lg | md |
| PC | - | 1440+ | xl | - |
