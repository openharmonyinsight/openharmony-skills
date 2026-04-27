# 多设备适配规格要求

## 目录

1. [核心概念](#核心概念)
2. [规格清单](#规格清单)
   - [SPEC-01 宫格图片信息量适中](#spec-01-宫格图片信息量适中)
   - [SPEC-02 单图信息量适中](#spec-02-单图信息量适中)
   - [SPEC-03 上下图文信息量适中](#spec-03-上下图文信息量适中)
   - [SPEC-04 外屏高度较小的阔折叠底部页签左右结构适配](#spec-04-外屏高度较小的阔折叠底部页签左右结构适配)
   - [SPEC-05 视频类场景使用画中画能力](#spec-05-视频类场景使用画中画能力)
   - [SPEC-06 大屏设备上信息聚合](#spec-06-大屏设备上信息聚合)
   - [SPEC-07 信息流边距控制](#spec-07-信息流边距控制)
   - [SPEC-08 宽屏/折叠屏设备平行视界分栏适配](#spec-08-宽屏折叠屏设备平行视界分栏适配)
   - [SPEC-09 宽屏场景底部导航侧边化与能力扩展（推荐）](#spec-09-宽屏场景底部导航侧边化与能力扩展推荐)
   - [SPEC-10 大屏设备页面/控件留白比例约束（推荐）](#spec-10-大屏设备页面控件留白比例约束推荐)
   - [SPEC-11 小高度阔折叠设备标题栏与搜索入口形态优化（推荐）](#spec-11-小高度阔折叠设备标题栏与搜索入口形态优化推荐)
   - [SPEC-12 字体大小合规](#spec-12-字体大小合规)
   - [SPEC-13 界面图标大小合规](#spec-13-界面图标大小合规)
   - [SPEC-14 大屏设备图标文字大小适中](#spec-14-大屏设备图标文字大小适中)
   - [SPEC-15 弹出框大小适中](#spec-15-弹出框大小适中)

---

## 核心概念

### 什么是多设备适配规格

多设备适配规格是 HarmonyOS 官方定义的 UI 布局在不同设备形态上必须/推荐遵守的约束条件。这些规格基于**屏幕高度占比**、**图片放大倍数**、**结构切换**等可量化指标，确保应用在手机、折叠屏、平板、PC 等设备上都能提供良好的用户体验。

规格要求与具体实现无关，关注"约束什么"而非"如何实现"。例如：规格要求"宫格图片高度不超过屏幕高度的 50%"，但不强制规定使用 `layoutWeight`、固定高度还是断点约束。

### 优先级说明

- **[P0]** 条款为强制要求，不遵守会导致应用在部分设备上出现严重体验问题。
- **[P1]** 条款为推荐做法，建议遵循以获得更好的用户体验。

---

## 规格清单

### SPEC-01 宫格图片信息量适中

**适用场景**

宫格布局或瀑布流布局中展示图片的场景，包括但不限于：独立宫格浏览、瀑布流图片列表、信息流中的宫格聚合配图。

**规范要求**

1. **[P0] 高度占比约束**：宫格布局或瀑布流布局的图片单行高度不要低于屏幕高度的 10%，不要超过屏幕高度的 50%。

**关键代码**

- 获取屏幕高度（vp）— Ability 侧监听 + AppStorage 传递（详见 [窗口尺寸监听指南](./window_size_detection.md)）
```typescript
// EntryAbility.onWindowStageCreate → loadContent 回调内
const initHeight: number = px2vp(this.mainWindow!.getWindowProperties().windowRect.height);
AppStorage.setOrCreate('screenHeightVp', initHeight);
this.mainWindow!.on('windowSizeChange', (size: window.Size) => {
  const heightVp: number = px2vp(size.height);
  AppStorage.setOrCreate('screenHeightVp', heightVp);
});
```

- 组件侧通过 `@StorageProp` 消费，使用 `constraintSize` 约束高度占比
```typescript
@StorageProp('screenHeightVp') screenHeightVp: number = 0

Image($r('app.media.startIcon'))
  .width('100%')
  .aspectRatio(1)
  // SPEC-01: 高度占比 10%~50%
  .constraintSize({
    minHeight: this.screenHeightVp > 0 ? this.screenHeightVp * 0.1 : 0,
    maxHeight: this.screenHeightVp > 0 ? this.screenHeightVp * 0.5 : undefined
  })
  .objectFit(ImageFit.Cover)
```

> **约束模式说明**：使用 `constraintSize` 而非固定 `height`，这样图片在满足占比约束的前提下仍可由 `aspectRatio` + 宽度自适应撑开，不会强制拉伸或压缩。

---

### SPEC-02 单图信息量适中

**适用场景**

单张图片在页面中横向撑满时（包括内容区全宽、轮播卡片顶满内容区、沉浸式顶满窗口边缘等），需约束其高度占比，确保图片下方留有充足空间展示文字或其他信息，兼顾视觉冲击力与信息获取效率。


**规范要求**

1. **[P0] 内容区全宽图片高度上限**：单张图片或轮播卡片宽度顶满内容区时，图片高度不超过屏幕高度的 50%。

2. **[P1] 沉浸式全窗口图片高度上限**：沉浸式单张图片顶满窗口边缘时，图片高度不超过屏幕高度的 60%。

**关键代码**

- 获取屏幕物理尺寸 — Ability 侧监听 + AppStorage 传递（详见 [窗口尺寸监听指南](./window_size_detection.md)）
```typescript
// AppStorage 已在 EntryAbility 中设置 screenHeightVp
```

- 组件侧消费 — 使用 `constraintSize` 约束高度占比
```typescript
@StorageProp('screenHeightVp') screenHeightVp: number = 0

// 内容区全宽图片 → 高度上限 50%
Image(src)
  .width('100%')
  .constraintSize({
    maxHeight: this.screenHeightVp > 0 ? this.screenHeightVp * 0.5 : undefined
  })
  .objectFit(ImageFit.Cover)

// 沉浸式全窗口图片 → 高度上限 60%
Image(src)
  .width('100%')
  .constraintSize({
    maxHeight: this.screenHeightVp > 0 ? this.screenHeightVp * 0.6 : undefined
  })
  .objectFit(ImageFit.Cover)
```


---

### SPEC-03 上下图文信息量适中

**适用场景**

上下图文结构（上图下文 / 上文下图）是应用中最常见的布局形式之一，需合理控制图片尺寸和占比，确保信息量适中。典型场景包括：首页入口型卡片（应用首页功能入口、推荐卡片）、信息流（新闻列表、社交动态流）、内容详情页（新闻详情、文章阅读）。


**规范要求**

1. **[P0/P1] 约束满足方式**：图片放大倍数不超过规范要求或控件高度占比满足规范要求（至少满足其一，P0）；推荐同时满足两个约束（P1）。

2. **[P0] 放大倍数约束**：
   - 双折叠/三折叠设备展开态上图片等比放大时，放大倍数不超过 1.2 倍。
   - 平板上图片比直板机放大不超过 1.5 倍。

3. **[P1] 对齐方式**：上下图文结构中，信息流场景的图片建议左对齐，阅读场景的图片建议居中对齐。

4. **[P1] 宽屏设备布局优化**：在平板、双折叠/三折叠设备展开态、电脑设备最大化窗口等宽屏设备上，建议通过延伸布局、挪移布局等方式让图文进行合理布局，避免图片过大。

5. **[P0] 高度占比约束**：
   - 信息流场景：非宫格聚合图片高度不要超过屏幕高度的 40%，长图或宫格聚合图片整体高度不要超过屏幕高度的 60%。
   - 内容详情页：图片高度不要超过屏幕高度的 60%。

**关键代码**

- 获取屏幕物理尺寸 — Ability 侧监听 + AppStorage 传递（详见 [窗口尺寸监听指南](./window_size_detection.md)）
```typescript
// AppStorage 已在 EntryAbility 中设置 screenHeightVp
```

- 组件侧消费 — 使用 `constraintSize` 约束高度占比
```typescript
@StorageProp('screenHeightVp') screenHeightVp: number = 0

// 首页入口型 → 高度上限 1/3
Image(src)
  .width('100%')
  .constraintSize({
    maxHeight: this.screenHeightVp > 0 ? this.screenHeightVp * (1 / 3) : undefined
  })
  .objectFit(ImageFit.Cover)

// 信息流非宫格 → 高度上限 40%，左对齐
Image(src)
  .width('100%')
  .constraintSize({
    maxHeight: this.screenHeightVp > 0 ? this.screenHeightVp * 0.4 : undefined
  })
  .objectFit(ImageFit.Cover)
  .align(Alignment.Start)

// 信息流宫格聚合/长图 → 高度上限 60%，左对齐
Image(src)
  .width('100%')
  .constraintSize({
    maxHeight: this.screenHeightVp > 0 ? this.screenHeightVp * 0.6 : undefined
  })
  .objectFit(ImageFit.Cover)
  .align(Alignment.Start)

// 内容详情页 → 高度上限 60%，居中对齐
Image(src)
  .width('100%')
  .constraintSize({
    maxHeight: this.screenHeightVp > 0 ? this.screenHeightVp * 0.6 : undefined
  })
  .objectFit(ImageFit.Cover)
  .align(Alignment.Center)
```

- 放大倍数约束 — 同样使用 `constraintSize` 综合限制

```typescript
@StorageProp('screenHeightVp') screenHeightVp: number = 0

// 图片高度需同时满足：高度占比约束 + 放大倍数约束
// 以信息流非宫格为例：占比上限 40%，放大倍数上限 1.5x
const heightByRatio: number = this.screenHeightVp * 0.4;  // 场景占比上限
const heightByScale: number = baseHeight * 1.5;            // 放大倍数上限
const finalMaxHeight: number = Math.min(heightByRatio, heightByScale);

Image(src)
  .width('100%')
  .constraintSize({
    maxHeight: this.screenHeightVp > 0 ? finalMaxHeight : undefined
  })
  .objectFit(ImageFit.Cover)
```

- 延伸布局（首页入口型、信息流）

```typescript
GridRow({
  columns: { sm: 2, md: 3, lg: 4 },
  gutter: { x: 12, y: 12 },
}) {
  ForEach(dataList, (item) => {
    GridCol({ span: 1 }) {
      // 卡片内容
    }
  })
}
```

- 挪移布局（详情页，sm 单列，md/lg 左右分栏）

```typescript
GridRow({ columns: { sm: 1, md: 6, lg: 12 } }) {
  GridCol({ span: { sm: 12, md: 4, lg: 8 } }) { /* 文章内容 */ }
  GridCol({ span: { sm: 12, md: 2, lg: 4 } }) { /* 侧边推荐 */ }
}
```


---

### SPEC-04 外屏高度较小的阔折叠底部页签左右结构适配

**适用场景**

应用主界面使用底部页签栏（TabBar）承载主导航的场景，包括但不限于：首页多 Tab 切换、底部导航 + 内容列表的经典布局。


核心适配对象：外屏高度较小的阔折叠设备——折叠态外屏宽高断点组合为 **sm + md** 的小方形屏幕（宽高比接近 1:1，宽度 < 600vp）。当折叠态外屏高度不足以上下结构容纳底部页签栏与内容区域时，须将页签栏迁移至左侧，以左右结构替代上下结构，保障内容区域可用空间。

**规范要求**

1. **[P1] 断点检测与判定**：应用应同时检测窗口宽度和高度两个维度的断点值（宽度断点为 xs/sm/md/lg/xl，高度断点为 sm/md/lg）；当宽度断点为 **sm** 且高度断点为 **md** 时，判定为外屏高度较小的阔折叠折叠态。

2. **[P1] 布局结构切换**：
   - 外屏高度较小的阔折叠折叠态：页签栏从底部水平排列切换为左侧垂直排列，形成左右结构（页签在左、内容在右）。
   - 其余所有屏幕形态（含阔折叠内屏展开态）：保持上下结构（内容在上、页签在底部）。

3. **[P0] 页签栏结构与尺寸**：页签项内部始终保持垂直排列（图标在上，文字在下），不得因屏幕变化改为左右排列；左右结构中侧边导航栏宽度固定，各页签项等高分配；上下结构中底部页签栏高度固定，各页签项等宽分配。

4. **[P0] 内容区域一致性**：内容区域在两种布局结构中保持一致，随页签切换而变化；在左右结构中占据导航栏以外的全部空间，在上下结构中占据页签栏以上的全部空间。

5. **[P0] 实时更新与状态保持**：窗口尺寸变化时（折叠/展开/旋转）须实时更新断点并刷新布局，切换过程无闪烁，当前选中页签保持不变。



**关键代码**

- 在 Ability 生命周期中初始化断点检测，注册窗口尺寸变化监听：

```typescript
// onWindowStageCreate 中初始化
const mainWindow = windowStage.getMainWindowSync();
breakpointUtils.init(mainWindow);
```

- 通过 UIContext 获取宽高断点，转换为可读字符串并写入 AppStorage：

```typescript
const widthBp = this.uiContext.getWindowWidthBreakpoint();   // 返回数值
const heightBp = this.uiContext.getWindowHeightBreakpoint();  // 返回数值
AppStorage.setOrCreate('widthBreakpointStr', widthBpToStr(Number(widthBp)));
AppStorage.setOrCreate('heightBreakpointStr', heightBpToStr(Number(heightBp)));
```

- 监听窗口尺寸变化，驱动断点实时更新：

```typescript
mainWindow.on('windowSizeChange', () => {
  this.updateBreakpoints();
});
```

- 在页面中通过 @StorageProp 响应断点变化，判定小方形屏：

```typescript
@StorageProp('widthBreakpointStr') @Watch('onBreakpointChange')
currentWidthBp: string = '';
@StorageProp('heightBreakpointStr') @Watch('onBreakpointChange')
currentHeightBp: string = '';
@State isSmallSquare: boolean = false;

onBreakpointChange(): void {
  this.isSmallSquare = (widthBp === 'sm' && heightBp === 'md');
}
```

- 根据判定结果条件渲染不同布局结构：

```typescript
build() {
  if (this.isSmallSquare) {
    Row() {
      SideNavBar()    // 左侧垂直页签栏
      ContentArea()   // 右侧内容区域
    }
  } else {
    Column() {
      ContentArea()     // 上方内容区域
      BottomTabBar()    // 底部水平页签栏
    }
  }
}
```

---

### SPEC-05 视频类场景使用画中画能力

**适用场景**

视频播放、视频会议、视频通话、直播等需要持续展示视频画面的场景。用户在这些场景中可能需要临时切换到其他页面或应用操作，此时应通过画中画（Picture-in-Picture）能力保持视频画面的持续可见，确保用户在执行多任务操作时不中断视频观看或通话体验。


**规范要求**

1. **[P1] 启用画中画能力**：在视频播放、视频会议、视频通话、直播场景中，应接入系统画中画能力，支持用户在离开当前页面时将视频画面缩小为悬浮窗继续播放/展示。

---

### SPEC-06 大屏设备上信息聚合

**适用场景**

大屏设备上，页签搜索场景中建议搜索框，子页签与标题栏聚合显示；音乐类应用建议播放条与底部页签聚合显示


**规范要求**

1. **[P1] 搜索框与子页签和标题栏聚合显示**：在信息搜索，信息展示，新闻阅读，商品浏览等场景，建议大屏设备上顶部的搜索框和子页签和标题栏放在同一行。

2. **[P1] 音乐播放类界面播放条与底部页签聚合显示**：在音乐播放类界面，建议大屏设备上页面底部的播放条和底部页签聚合显示，放在同一行或者同一区间中。

---

### SPEC-07 信息流边距控制

**适用场景**

信息流列表通过左右边距控制卡片或内容区域的水平显示宽度，避免内容在宽屏设备上横向过度拉伸，保持阅读舒适度。典型场景包括：新闻信息流、社交动态流、商品推荐列表等使用边距来收窄内容宽度的信息流布局。


**规范要求**

1. **[P0] 左边距强制上限**：信息流场景中，左边距不超过屏幕宽度的 20%。

**关键代码**

- 获取屏幕宽度(vp) — Ability 侧监听 + AppStorage 传递（详见 [窗口尺寸监听指南](./window_size_detection.md)）
```typescript
// EntryAbility.onWindowStageCreate → loadContent 回调内，同时监听宽度
const initWidth: number = px2vp(this.mainWindow!.getWindowProperties().windowRect.width);
AppStorage.setOrCreate('screenWidthVp', initWidth);

this.mainWindow!.on('windowSizeChange', (size: window.Size) => {
  const widthVp: number = px2vp(size.width);
  AppStorage.setOrCreate('screenWidthVp', widthVp);
});
```

- 组件侧消费 — 使用 `@StorageProp` 获取宽度，计算合规边距
```typescript
@StorageProp('screenWidthVp') screenWidthVp: number = 0

List() {
  // 信息流内容
}
.padding({
  left: this.screenWidthVp > 0 ? Math.min(this.screenWidthVp * 0.2, 72) : 16,
  right: this.screenWidthVp > 0 ? Math.min(this.screenWidthVp * 0.2, 72) : 16
})
```

- 参数化模板（与上面的具体实现等价，便于统一复用）

```typescript
.padding({
  left: Math.min(screenWidth * maxPaddingRatio, fixedPaddingCap),
  right: Math.min(screenWidth * maxPaddingRatio, fixedPaddingCap)
})
```

---

### SPEC-08 宽屏/折叠屏设备平行视界分栏适配

**适用场景**

应用在宽屏/大屏设备（折叠屏展开态、平板横屏）上需要以分栏方式同时显示主页和详情页，提升多任务处理效率。典型场景包括：邮件列表与邮件详情、商品列表与商品详情、新闻列表与新闻内容、IM 会话列表与聊天窗口等"列表-详情"类应用。

**核心概念**

平行视界（EasyGo）是 HarmonyOS 的系统级兼容方案，通过标准化配置文件让未适配分栏布局的应用在宽屏设备上自动实现分栏显示。左侧固定为主页，路由跳转只发生在右侧，两个页面共享同一个 UIAbility 窗口实例。

> 注意：平行视界（EasyGo 分栏）与应用内分屏（`startAbility` + `StartOptions` 启动另一个 UIAbility）是不同的多窗口方案，不要混淆。

**规范要求**

1. **[P0] 配置文件声明**：在 entry 模块 `resources/base/profile/` 下创建 `easy_go.json`，并在 `module.json5` 中添加 `"easyGo": "$profile:easy_go"` 字段。

2. **[P0] 同时配置 wideWindowMode 和 squareWindowMode**：折叠屏展开态屏幕接近方形（如 1:1），仅配置 `wideWindowMode`（要求高/宽 <= 1.2）可能无法触发分栏，必须同时配置 `squareWindowMode` 确保覆盖。

3. **[P1] 根据导航模式选择 Split 类型**：
   - Navigation 导航 → `navigationSplit` + `navigationSplitOptions`
   - Router 导航 → `routerSplit` + `routerSplitOptions`
   - 两种 SplitOptions 不能同时存在。

4. **[P1] 分栏后 UI 截断处理**：分栏后页面宽度减半，元素仍按全宽布局会导致截断。优先使用系统组件的自适应布局能力/断点系统能力；必要时开启虚拟容器（`enableReducedContainerSize: true`）。

**关键代码**

- `easy_go.json` — 折叠屏展开态 + Navigation 分栏（推荐配置）

```json
{
  "common": {
    "displayModeOptions": {
      "wideWindowMode": "navigationSplit",
      "squareWindowMode": "navigationSplit",
      "navigationSplitOptions": {
        "homePage": "navBar",
        "relatedPage": "DetailPage"
      }
    }
  }
}
```

- `module.json5` — 声明 easyGo 引用

```json5
{
  "module": {
    "name": "entry",
    "type": "entry",
    "easyGo": "$profile:easy_go"
  }
}
```

- `easy_go.json` 配置字段说明

| 字段 | 说明 | 类型 |
|------|------|------|
| `homePage` | 主页名称。Navigation 用 `"navBar"`；Router 用页面路径（如 `"pages/index"`） | string |
| `relatedPage` | 关联页名称，路由跳转到此页时分栏显示 | string |
| `enableReducedContainerSize` | 开启虚拟容器，让宽度按一半计算，解决分栏截断（默认 false） | boolean |
| `fullScreenPages` | 全屏页数组，跳转到这些页面时退出分栏 | string[] |
| `supportLandscapeFullScreen` | 应用请求横屏时是否全屏（默认 true） | boolean |
| `disablePlaceholder` | 是否隐藏占位页（默认 false，仅 navigationSplit） | boolean |
| `disableDivider` | 是否隐藏分割线（默认 false，仅 navigationSplit） | boolean |

- 多设备差异化配置示例

```json
{
  "common": {
    "displayModeOptions": {
      "wideWindowMode": "navigationSplit",
      "squareWindowMode": "navigationSplit",
      "navigationSplitOptions": {
        "homePage": "navBar",
        "relatedPage": "DetailPage"
      }
    }
  },
  "tablet": {
    "displayModeOptions": {
      "wideWindowMode": "navigationSplit",
      "navigationSplitOptions": {
        "homePage": "navBar",
        "relatedPage": "DetailPage",
        "enableReducedContainerSize": true
      }
    }
  }
}
```

- 页面大小监听（分栏/全屏切换时动态调整 UI）

```typescript
// Navigation 模式
navPathStack.on('navDestinationUpdate', (info) => { /* NavDestination 状态变化 */ })
navPathStack.onNavDestinationSizeChange((info) => { /* 大小变化回调 */ })

// Router 模式
uiContext.getRouter().on('routerPageUpdate', (info) => { /* 页面状态变化 */ })
uiContext.getRouter().onRouterPageSizeChange((info) => { /* 大小变化回调 */ })
```

**常见问题**

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 折叠屏展开态不分栏 | `wideWindowMode` 要求高/宽 <= 1.2，折叠屏展开态接近方形可能超阈值 | 同时配置 `squareWindowMode` |
| 分栏后 UI 截断 | 页面宽度减半但元素按全宽布局 | 开启 `enableReducedContainerSize: true` 或自适应布局 |
| 左右页共享 UI 资源 | NodeContainer 复用机制 | 左右页面使用独立资源 |
| 横竖屏设置不生效 | 平行视界要求左右页面方向一致 | 使用 window 接口设置窗口策略 |

---

### SPEC-09 宽屏场景底部导航侧边化与能力扩展（推荐）

**适用场景**

应用主界面使用底部导航（Bottom Tab）承载一级导航，且存在平板、折叠屏展开态、桌面窗口化等宽屏使用场景。

适用设备：phone / tablet / 2in1。

**规范要求**

1. **[P1] 宽屏结构切换推荐**：当应用窗口宽度 **>= 840vp**（`lg` 及以上断点）时，建议将底部导航从上下结构切换为左侧垂直结构，以提升主内容区的纵向可用空间与导航可达性。

2. **[P1] 侧边导航能力扩展**：底部 Tab 切换为侧边导航栏时，建议同步扩展导航能力，而非仅做位置迁移。可采用以下一种或多种方式：
   - 扩展导航层级（例如加入分组、二级入口或导航分区）。
   - 增加导航选项（例如补充宽屏场景下的功能入口）。
   - 增加高频功能直达（例如侧边快捷操作区、常用功能固定入口）。

3. **[P1] 组件选型建议**：若导航选项与信息架构保持不变，仅进行位置变化（底部改左侧），建议使用**侧边 Tab**形态；仅在需要承载扩展信息架构或增强交互能力时，使用**侧边导航栏**形态。

4. **[P1] 状态连续性**：结构切换过程中应保持当前选中项、页面路由与滚动状态连续，避免因布局切换导致上下文丢失。

5. **[P1] 术语对齐建议**：设计、产品、研发评审时应明确区分“侧边 Tab”和“侧边导航栏”，避免将两者混用为同一种交互模式。

**术语说明：侧边 Tab 与 侧边导航栏**

1. **侧边 Tab（Side Tab）含义**：底部 Tab 的“位置迁移形态”，核心是将原有一级导航从底部横排改为左侧竖排；信息架构通常不变，导航项数量和层级尽量与底部 Tab 一致。
2. **侧边导航栏（Side Navigation）含义**：面向宽屏的信息架构增强形态，除位置变化外，通常伴随导航能力扩展（分组、层级、补充入口、快捷区等）。
3. **侧边 Tab 与侧边导航栏的区别**：
   - 目标不同：侧边 Tab 以“迁移”为主，侧边导航栏以“扩展”为主。
   - 架构不同：侧边 Tab 倾向保持原有一级结构，侧边导航栏可引入分组或二级层级。
   - 交互不同：侧边 Tab 强调与底部 Tab 的状态连续，侧边导航栏可新增高频操作与功能入口。
   - 适用边界不同：仅位置变更优先侧边 Tab；需要增强信息架构与效率时优先侧边导航栏。

**关键代码**

- 宽度 `>= 840vp` 监听并切换侧边模式：

```typescript
import mediaquery from '@ohos.mediaquery';
import { UIContext } from '@kit.ArkUI';

private uiContext: UIContext = this.getUIContext();
private lgListener: mediaquery.MediaQueryListener =
  this.uiContext.getMediaQuery().matchMediaSync('(min-width: 840vp)');

@State useSideMode: boolean = false;

aboutToAppear(): void {
  this.useSideMode = this.lgListener.matches;
  this.lgListener.on('change', () => {
    this.useSideMode = this.lgListener.matches;
  });
}

aboutToDisappear(): void {
  this.lgListener.off('change');
}
```

- 根据是否扩展导航能力选择“侧边 Tab”或“侧边导航栏”：

```typescript
private readonly bottomTabs: string[] = ['首页', '消息', '我的'];
private readonly sideNavItems: string[] = ['首页', '消息', '工作台', '收藏', '我的'];

private hasNavExtension(): boolean {
  return this.sideNavItems.length !== this.bottomTabs.length;
}
```

- 结构渲染与选中状态保持：

```typescript
@State currentIndex: number = 0;

private normalizeCurrentIndex(): void {
  const maxIndex = this.useSideMode ? this.sideNavItems.length - 1 : this.bottomTabs.length - 1;
  if (this.currentIndex > maxIndex) {
    this.currentIndex = maxIndex;
  }
}

build() {
  this.normalizeCurrentIndex();
  if (this.useSideMode) {
    Row() {
      if (this.hasNavExtension()) {
        SideNavigationBar({ selected: this.currentIndex });
      } else {
        SideTabBar({ selected: this.currentIndex });
      }
      ContentArea();
    }
  } else {
    Column() {
      ContentArea();
      BottomTabBar({ selected: this.currentIndex });
    }
  }
}
```

---

### SPEC-10 大屏设备页面/控件留白比例约束（推荐）

**适用场景**

在平板、2in1、折叠屏展开态或桌面窗口化等大屏设备上，页面容器或核心业务控件出现大面积空白区域的场景。

适用设备：phone / tablet / 2in1。

**规范要求**

1. **[P1] 留白比例推荐值**：大屏设备上，页面或关键控件的留白比例建议不超过 **60%**，以保证信息密度和可读性。

2. **[P0] 留白比例强制上限**：大屏设备上，页面或关键控件的留白比例不得超过 **70%**；超过该阈值视为适配不合规。

3. **[P1] 优化优先级建议**：当留白比例在 `(60%, 70%]` 区间时，建议优先通过延伸布局、分栏布局、补充次级信息模块等方式降低留白，而非单纯放大主内容组件。

**关键代码**

- 判定是否为大屏断点（宽度 `>= 840vp`）：

```typescript
const widthBp = this.getUIContext().getWindowWidthBreakpoint();
const isLargeScreen = Number(widthBp) >= WidthBreakpoint.WIDTH_LG;
```

- 计算页面/控件留白比例：

```typescript
const containerArea = containerWidth * containerHeight;
const contentArea = contentWidth * contentHeight;
const whitespaceRatio = containerArea <= 0 ? 0 : (containerArea - contentArea) / containerArea;
```

- 按 60%（推荐）与 70%（必须）阈值判定：

```typescript
if (isLargeScreen && whitespaceRatio > 0.7) {
  // P0 不合规：必须修复
} else if (isLargeScreen && whitespaceRatio > 0.6) {
  // P1 建议优化：推荐修复
}
```

---

### SPEC-11 小高度阔折叠设备标题栏与搜索入口形态优化（推荐）

**适用场景**

在屏幕高度较小的阔折叠设备场景中，页面顶部标题栏与搜索入口占用较多垂直空间，导致核心内容区域被压缩的场景。

适用设备：phone。

**规范要求**

1. **[P1] 标题栏留白优化建议**：针对屏幕高度较小的阔折叠设备，建议适当缩小标题栏字号与垂直占位，减少顶部留白区域，增加核心内容显示空间。

2. **[P1] 搜索入口形态建议**：针对屏幕高度较小的阔折叠设备，建议将独立搜索框切换为搜索图标，并与标题栏同行显示，以减少顶部垂直占位并增加核心内容显示空间；点击图标进入搜索页或展开搜索面板。

**关键代码**

- 小高度阔折叠设备下联动调整标题字号与搜索入口形态：

```typescript
@State titleFontSize: number = 24;
@State useSearchIcon: boolean = false;
@State isWideFoldable: boolean = false;

onBreakpointChange(): void {
  const isLowHeight = (this.currentHeightBp === 'md' || this.currentHeightBp === 'sm');
  const enableCompactHeader = this.isWideFoldable && isLowHeight;
  this.titleFontSize = enableCompactHeader ? 18 : 24;
  this.useSearchIcon = enableCompactHeader;
}
```

- 标题栏与搜索图标同行显示（小高度阔折叠设备时）：

```typescript
import router from '@ohos.router';

Row() {
  Text('联系人')
    .fontSize(this.titleFontSize)
    .fontWeight(FontWeight.Bold)

  Blank()

  if (this.useSearchIcon) {
    Image($r('app.media.ic_search'))
      .width(20)
      .height(20)
      .onClick(() => {
        router.pushUrl({ url: 'pages/SearchPage' });
      })
  } else {
    Search({ value: this.keyword, placeholder: '搜索' })
      .width('56%')
      .height(36)
  }
}
.width('100%')
.height(56)
.padding({ left: 12, right: 12 })
```

---

### SPEC-12 字体大小合规

**适用场景**

应用内所有展示文字的场景，包括但不限于：标签、按钮、列表项、正文内容、标题等文本元素。确保文字在不同设备类型上具备足够的可读性。

适用设备：phone / foldable / tablet / 2in1 / tv / wearable。

**规范要求**

1. **[P0] 手机/折叠屏/平板文本字号**：文本字号不小于 8 vp（推荐不小于 12 vp）。

2. **[P0] 电脑文本字号**：文本字号不小于 10 vp（推荐不小于 14 vp）。

3. **[P0] 智慧屏文本字号**：文本字号不小于 14 vp（推荐不小于 16 vp），其中正文字号建议 22～26 vp。

4. **[P0] 智能穿戴文本字号**：文本字号不小于 10 vp（推荐不小于 13 vp）。

| 设备类型 | 最小字号（必须） | 推荐字号 |
|---------|----------------|---------|
| 手机/折叠屏/平板 | 8 vp | 12 vp |
| 电脑 | 10 vp | 14 vp |
| 智慧屏 | 14 vp | 16 vp（正文 22～26 vp） |
| 智能穿戴 | 10 vp | 13 vp |

**关键代码**

- 根据设备类型获取最小字号约束：

```typescript
import { deviceInfo } from '@kit.BasicServicesKit';

function getMinFontSize(): number {
  const deviceType = deviceInfo.deviceType;
  switch (deviceType) {
    case 'phone':
    case 'tablet':
      return 12; // 推荐 12vp，最小 8vp
    case '2in1':
      return 14; // 推荐 14vp，最小 10vp
    case 'tv':
      return 16; // 推荐 16vp，最小 14vp
    case 'wearable':
      return 13; // 推荐 13vp，最小 10vp
    default:
      return 12;
  }
}
```

- 文本组件字号约束：

```typescript
Text('示例文本')
  .fontSize(Math.max(userFontSize, getMinFontSize()))
```

---

### SPEC-13 界面图标大小合规

**适用场景**

应用内所有界面图标（非启动图标）的尺寸约束，包括但不限于：导航图标、工具栏图标、列表项图标、功能入口图标等。确保图标在不同设备类型上具备足够的可点击性和辨识度。

适用设备：phone / foldable / tablet / 2in1 / tv / wearable。

**规范要求**

1. **[P0] 手机/折叠屏/平板界面图标**：图标大小不小于 8 vp（推荐不小于 12 vp）。

2. **[P0] 电脑界面图标**：图标大小不小于 10 vp（推荐不小于 14 vp）。

3. **[P0] 智慧屏界面图标**：图标大小不小于 22 vp（推荐不小于 26 vp）。

4. **[P0] 智能穿戴界面图标**：图标大小不小于 16 vp（推荐不小于 20 vp）。

| 设备类型 | 最小图标尺寸（必须） | 推荐图标尺寸 |
|---------|---------------------|-------------|
| 手机/折叠屏/平板 | 8 vp | 12 vp |
| 电脑 | 10 vp | 14 vp |
| 智慧屏 | 22 vp | 26 vp |
| 智能穿戴 | 16 vp | 20 vp |

**关键代码**

- 根据设备类型获取最小图标尺寸约束：

```typescript
import { deviceInfo } from '@kit.BasicServicesKit';

function getMinIconSize(): number {
  const deviceType = deviceInfo.deviceType;
  switch (deviceType) {
    case 'phone':
    case 'tablet':
      return 12; // 推荐 12vp，最小 8vp
    case '2in1':
      return 14; // 推荐 14vp，最小 10vp
    case 'tv':
      return 26; // 推荐 26vp，最小 22vp
    case 'wearable':
      return 20; // 推荐 20vp，最小 16vp
    default:
      return 12;
  }
}
```

- 图标组件尺寸约束：

```typescript
Image($r('app.media.icon'))
  .width(Math.max(iconSize, getMinIconSize()))
  .height(Math.max(iconSize, getMinIconSize()))
  .objectFit(ImageFit.Contain)
```

---

### SPEC-14 大屏设备图标文字大小适中

**适用场景**

折叠屏设备（双折叠/三折叠）展开态、平板、电脑、智慧屏等大屏设备上，文字和图标随屏幕放大时的尺寸约束。需确保展开态或大屏上的文字/图标物理大小合理，避免信息过密。

适用设备：foldable / tablet / 2in1 / tv。

**规范要求**

1. **[P0] 放大倍数约束**：
   - 双折叠/三折叠设备展开态文字、图标大小为折叠态的 1～1.2 倍，放大倍数不超过 1.2 倍。
   - 平板上文字/图标大小为直板机的 1～1.5 倍，放大倍数不超过 1.5 倍。

2. **[P1] 一排图标数量约束**：
   - 双折叠设备展开态横竖屏/三折叠设备双屏态横竖屏/三折叠设备三屏态竖屏/平板竖屏：一排不超过 8 个图标。
   - 三折叠设备三屏态横屏/平板横屏：一排不超过 13 个图标。
   - 智慧屏：一排不超过 12 个图标。

**关键代码**

- 根据断点计算文字/图标缩放倍数：

```typescript
const baseFontSize: number = 14;
const baseIconSize: number = 24;

function getScaleFactor(breakpoint: string, isFoldable: boolean): number {
  if (isFoldable) {
    return Math.min(1.2, breakpoint === 'lg' || breakpoint === 'xl' ? 1.2 : 1.0);
  }
  // 平板
  return Math.min(1.5, breakpoint === 'lg' || breakpoint === 'xl' ? 1.5 : 1.0);
}

const scaledFontSize = baseFontSize * getScaleFactor(currentBp, isFoldableDevice);
const scaledIconSize = baseIconSize * getScaleFactor(currentBp, isFoldableDevice);
```

- 一排图标数量约束：

```typescript
function getMaxIconsPerRow(deviceType: string, orientation: string): number {
  if (deviceType === 'tv') return 12;
  if (orientation === 'landscape') return 13; // 横屏
  return 8; // 竖屏
}

// 使用 Grid 布局约束每行列数
Grid() {
  ForEach(iconList, (item) => {
    GridItem() {
      // 图标项
    }
  })
}
.columnsTemplate(`1fr `.repeat(Math.min(iconList.length, getMaxIconsPerRow(deviceType, orientation))))
```

---

### SPEC-15 弹出框大小适中

**适用场景**

折叠屏设备（双折叠/三折叠）展开态、平板、电脑、智慧屏等大屏设备上弹出框（Dialog / Popup / Modal）的尺寸约束。需确保弹出框在不同设备形态下大小适中，不会因屏幕放大而过度拉伸。

适用设备：foldable / tablet / 2in1 / tv。

**规范要求**

1. **[P0] 折叠屏弹出框高度约束**：
   - 双折叠/三折叠设备展开态弹出框高度为折叠态的 1～1.2 倍，放大倍数不超过 1.2 倍。
   - 阔折叠设备弹出框高度位于 65%～90% 屏幕总高度。

2. **[P0] 平板弹出框高度约束**：弹出框高度为直板机的 1～1.2 倍，放大倍数不超过 1.2 倍。

3. **[P0] 电脑弹出框尺寸约束**：弹出框最小不低于 360×240 vp，最大不超过当前应用窗口尺寸。

4. **[P0] 智慧屏弹出框尺寸约束**：弹出框宽度 < 36% 屏幕总宽度，高度 < 80% 屏幕总高度。

**关键代码**

- 使用自定义弹出框组件，采用栅格化布局进行约束：

```typescript
// 自定义弹窗组件
@CustomDialog
struct MyDialog {
  // 控制器，用于关闭弹窗
  controller?: CustomDialogController

  build() {
    // ...
  }
}

@Component
struct DialogComponent {
  dialogController: CustomDialogController = new CustomDialogController({
    // 引入弹窗组件
    builder: MyDialog(),
    // 弹窗宽度占栅格数（4表示占4列，总共12列）
    gridCount: 4,
  })
  
  build() {
    // ...
  }
}
```