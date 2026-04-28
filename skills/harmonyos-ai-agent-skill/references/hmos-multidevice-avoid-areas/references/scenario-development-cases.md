# 场景开发案例集

## 目录

1. [场景1：列表页滚动沉浸浏览](#场景1列表页滚动沉浸浏览)
2. [场景2：底部导航栏避让](#场景2底部导航栏避让)
3. [场景3：短视频沉浸](#场景3短视频沉浸)
4. [场景4：挖孔区适配](#场景4挖孔区适配)
5. [场景5：状态栏适配](#场景5状态栏适配)
6. [场景6：键盘易操作](#场景6键盘易操作)

---

## 场景1：列表页滚动沉浸浏览

**场景描述：**
- 列表类页面（商品列表、信息流）
- 上滑浏览内容时逐渐隐藏顶部标题栏和底部导航栏，下滑时恢复
- 多设备断点适配：紧凑型（xs/sm/md）使用底部 TabBar 并支持滚动隐藏，宽屏型（lg/xl/xxl）使用侧边导航栏且不隐藏

**多设备体验标准：**

为方便浏览和获取信息，可采用滑动或点击的方式，将顶部和底部的标题栏、导航栏等空间隐藏，以便提供更大的信息显示量。

**解决方案：** 使用 **setWindowLayoutFullScreen 开启全屏** + **getWindowAvoidArea 获取避让区高度** + **Stack + Tabs(barHeight=0) + 浮层 TabBar 骨架** + **onScrollFrameBegin 累计偏移线性比例驱动隐藏/恢复** + **onBreakpointChange 断点切换重置状态**

### 步骤 1：EntryAbility 开启全屏布局

```ts
const mainWindow = windowStage.getMainWindowSync();
mainWindow.setWindowLayoutFullScreen(true);
```

### 步骤 2：监听避让区，获取状态栏和导航条高度

```ts
private updateAvoidArea(): void {
  const systemArea = this.mainWindow.getWindowAvoidArea(AvoidAreaType.TYPE_SYSTEM);
  this.topAvoidHeight = px2vp(systemArea.topRect.height);
  const navArea = this.mainWindow.getWindowAvoidArea(AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
  this.bottomAvoidHeight = px2vp(navArea.bottomRect.height);
}
```

根容器通过 `padding({ top: this.topAvoidHeight })` 避让状态栏，Scroll 通过 `.expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])` 延伸到导航条区域。

### 步骤 3：布局骨架——Stack 叠加 Tabs + 浮层 TabBar

```
Column（paddingTop = 状态栏高度）
└── Stack
    ├── Tabs（barHeight=0，宽屏时 paddingLeft=80）
    │   └── TabContent → CustomTitleBar + Scroll > GridRow
    └── TabBar（紧凑型底部水平 / 宽屏左侧垂直）
```

### 步骤 4：核心滚动算法——onScrollFrameBegin + 线性比例

定义与标题栏/TabBar 关联的状态变量，通过累计滚动偏移计算 0~1 的 ratio，线性驱动所有属性：

```ts
@State titleBarHeight: number = 56;
@State titleBarOpacity: number = 1;
@State bottomBarHeight: number = 56;
@State bottomBarOpacity: number = 1;
@State bottomBarMarginBottom: number = 8;
private accumulatedOffset: number = 0;
const HIDE_THRESHOLD = 100; // vp

.onScrollFrameBegin((offset: number, state: ScrollState) => {
  if (!this.isCompactBp()) return { offsetRemain: offset }; // 仅紧凑型生效
  this.accumulatedOffset = Math.max(0, Math.min(HIDE_THRESHOLD, this.accumulatedOffset + offset));
  const ratio = this.accumulatedOffset / HIDE_THRESHOLD;
  this.titleBarHeight = 56 * (1 - ratio);
  this.titleBarOpacity = 1 - ratio;
  this.bottomBarHeight  = 56 * (1 - ratio);
  this.bottomBarOpacity = 1 - ratio;
  this.bottomBarMarginBottom = 8 * (1 - ratio);
  return { offsetRemain: offset };
})
```

效果：上滑 0~100vp 线性渐隐，超过 100vp 完全隐藏，下滑线性恢复。

### 步骤 5：断点切换时重置

从紧凑型切到宽屏时恢复初始值：

```ts
.onBreakpointChange((breakpoint: string) => {
  const wasCompact = this.isCompactBp();
  this.currentBp = breakpoint;
  if (wasCompact && !this.isCompactBp()) {
    this.accumulatedOffset = 0;
    this.titleBarHeight = 56; this.titleBarOpacity = 1;
    this.bottomBarHeight = 56; this.bottomBarOpacity = 1;
    this.bottomBarMarginBottom = 8;
  }
})
```

---

## 场景2：底部导航栏避让

**场景描述：**
- 手机、折叠屏、平板等设备屏幕底部有系统导航条，应用需对底部导航条进行适配
- 底部固定空间（TabBar、操作栏、悬浮按钮）需要向上抬高，避免与导航条遮挡，同时背景色延伸到导航条底部实现沉浸效果
- 可滚动内容需要能延伸显示在导航条下方，滚动到底部时最后一项内容不被导航条遮挡
- 弹出框、半模态等控件需要向上避让导航条，避免交互误触
- 沉浸式场景（全屏播放视频、图片查看）导航条可自动隐藏，支持从底部上滑恢复

**多设备体验标准：**

手机、折叠屏、平板等设备屏幕底部有导航条，应用需对底部导航条进行适配。

- 应用内的底部固定控件、输入键盘、应用底部的悬浮按钮等均需要进行向上抬高，避免和导航条互相遮挡，也要避免导航条底部背景色与应用内底部背景色不融合，需要为导航条提供沉浸的背景效果。
- 应用内的可滚动内容，需要能显示在导航条下方。当滚动到最底部时，要避免导航条遮挡导致最底部功能不可用。
- 应用内的弹出框、半模态等控件，需要向上避让导航条，避免交互误触。
- 沉浸式场景，例如游戏、全屏播放视频，导航条可自动隐藏，支持从底部上滑恢复显示导航条。

**解决方案：** 使用 **setWindowLayoutFullScreen 开启全屏** + **AvoidAreaManager 单例监听 avoidAreaChange 获取导航条高度** + **AppStorage + @StorageProp 全局响应** + **padding({ bottom: navBarHeight }) + expandSafeArea 组合实现固定区域避让与背景延伸** + **列表尾部占位 Blank 实现可滚动内容避让** + **bindSheet / AlertDialog 系统组件自带避让** + **setSpecificSystemBarEnabled 动态隐藏/恢复导航条**

### 步骤 1：EntryAbility 开启全屏布局并初始化避让区管理器

```ts
onWindowStageCreate(windowStage: window.WindowStage): void {
  const mainWindow = windowStage.getMainWindowSync();
  mainWindow.setWindowLayoutFullScreen(true);
  mainWindow.setWindowSystemBarProperties({
    statusBarColor: '#00000000',
    navigationBarColor: '#00000000',
    isStatusBarLightIcon: false,
    isNavigationBarLightIcon: false
  });

  AvoidAreaManager.getInstance().init(this.context).then(() => {
    windowStage.loadContent('pages/MainPage', (err) => {
      if (err.code) { return; }
      mainWindow.getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE);
    });
  });
}
```

关键点：全屏布局 + 系统栏透明 + 键盘 RESIZE 模式避免键盘弹起遮挡输入框。

### 步骤 2：AvoidAreaManager 单例监听导航条高度变化

```ts
export class AvoidAreaManager {
  private static instance: AvoidAreaManager;
  private windowClass?: window.Window;
  private navigationBarHeight: number = 0;

  static getInstance(): AvoidAreaManager {
    if (!AvoidAreaManager.instance) {
      AvoidAreaManager.instance = new AvoidAreaManager();
    }
    return AvoidAreaManager.instance;
  }

  async init(context: Context): Promise<void> {
    this.windowClass = await window.getLastWindow(context);
    this.updateAvoidAreas();
    this.windowClass.on('avoidAreaChange', () => {
      this.updateAvoidAreas();
    });
  }

  private updateAvoidAreas(): void {
    if (!this.windowClass) return;
    const navigationArea =
      this.windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
    if (navigationArea) {
      this.navigationBarHeight = px2vp(navigationArea.bottomRect.height);
    }
    AppStorage.setOrCreate('navigationBarHeight', this.navigationBarHeight);
  }

  destroy(): void {
    this.windowClass?.off('avoidAreaChange');
  }

  getWindow(): window.Window | undefined {
    return this.windowClass;
  }
}
```

关键点：
- 通过 `TYPE_NAVIGATION_INDICATOR` 获取底部导航条高度
- 监听 `avoidAreaChange` 事件，设备旋转/折叠屏展开时自动更新
- 通过 `AppStorage.setOrCreate` 全局共享，各组件用 `@StorageProp` 自动响应变化

### 步骤 3：底部固定区域（TabBar / 操作栏）避让 + 背景沉浸

**核心模式：`padding({ bottom: navBarHeight })` + `expandSafeArea`**

padding 将内容上移避免遮挡，expandSafeArea 将背景色延伸到导航条底部实现沉浸效果：

```ts
@Component
export struct CustomTabBar {
  @StorageProp('navigationBarHeight') navigationBarHeight: number = 0;

  build() {
    Row() {
      // Tab 内容...
    }
    .width('100%')
    .height(56 + this.navigationBarHeight)                       // 总高度包含导航条区域
    .padding({ bottom: this.navigationBarHeight })               // 内容上移避让
    .backgroundColor(Color.White)
    .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM]) // 背景色延伸到导航条底部
  }
}
```

其他底部固定操作栏同理（商品详情页底部按钮栏、购物车结算栏、分类页筛选栏）：

```ts
// 商品详情页底部操作栏
Row() { /* 按钮组 */ }
  .padding({ left: 12, right: 12, bottom: this.navigationBarHeight })
  .backgroundColor(Color.White)
  .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])

// 购物车底部结算栏
Row() { /* 全选 + 合计 + 结算 */ }
  .height(52)
  .padding({ left: 12, right: 12, bottom: this.navigationBarHeight })
  .backgroundColor(Color.White)
  .expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM])
```

### 步骤 4：悬浮按钮抬高避让

悬浮按钮需要在底部固定栏之上再加导航条高度的偏移：

```ts
Button({ type: ButtonType.Circle }) { /* ... */ }
  .width(48)
  .height(48)
  .position({ x: '80%', y: '75%' })
  .margin({ bottom: this.navigationBarHeight + 56 + 16 }) // 导航条 + Tab栏 + 间距
```

### 步骤 5：可滚动内容延伸到导航条下方

在 List/Grid 末尾添加占位 ListItem，高度等于导航条 + 底部固定栏，确保最后一项可滚动到可见区域：

```ts
List({ space: 12 }) {
  ForEach(this.products, (product: Product) => {
    ListItem() {
      // 列表内容...
    }
  })

  // 尾部占位：避免最后一项被底部导航条 + TabBar 遮挡
  ListItem() {
    Column() {
      Blank().height(this.navigationBarHeight + 56 + 16) // 导航条高度 + TabBar高度 + 间距
    }
  }
}
.expandSafeArea([SafeAreaType.SYSTEM], [SafeAreaEdge.BOTTOM]) // 列表内容可滚入导航条区域
```

关键点：
- `expandSafeArea` 使列表渲染区域延伸到导航条下方，内容可滑入该区域
- 尾部 `Blank` 占位确保滚动到底时最后一项内容完全可见

### 步骤 6：弹出框 / 半模态避让导航条

使用系统组件，系统自动处理导航条避让：

```ts
// 半模态（bindSheet）- 系统自动避让导航条
.bindSheet($$this.showCouponSheet, this.couponSheetBuilder(), {
  detents: [SheetSize.MEDIUM],
  showClose: true,
  dragBar: true
})

// AlertDialog 居中弹出 - 天然避开底部导航条
AlertDialog.show({
  title: '设置',
  message: '是否退出登录？',
  alignment: DialogAlignment.Center,
  primaryButton: { value: '取消', action: () => {} },
  secondaryButton: { value: '确定', action: () => {} }
});
```

关键点：系统弹窗类组件（AlertDialog、ActionSheet、bindSheet、Menu）由系统管理位置，自动避开导航条区域。

### 步骤 7：沉浸式全屏（导航条动态隐藏/恢复）

通过 `setSpecificSystemBarEnabled` 控制导航条的显示与隐藏：

```ts
// 进入全屏（如点击图片/视频全屏播放）
private async enterFullScreen(): Promise<void> {
  this.isFullScreen = true;
  const win = AvoidAreaManager.getInstance().getWindow();
  if (win) {
    await win.setSpecificSystemBarEnabled('status', false);              // 隐藏状态栏
    await win.setSpecificSystemBarEnabled('navigationIndicator', false); // 隐藏导航条
  }
}

// 退出全屏（如点击屏幕/按返回键）
private async exitFullScreen(): Promise<void> {
  this.isFullScreen = false;
  const win = AvoidAreaManager.getInstance().getWindow();
  if (win) {
    await win.setSpecificSystemBarEnabled('status', true);               // 恢复状态栏
    await win.setSpecificSystemBarEnabled('navigationIndicator', true);  // 恢复导航条
  }
}
```

全屏模式下页面布局铺满整个屏幕：

```ts
build() {
  Stack() {
    if (this.isFullScreen) {
      // 全屏内容
      Image(this.product.image).width('100%').height('100%').objectFit(ImageFit.Cover)
      Text('点击屏幕退出全屏').position({ x: '50%', y: '90%' }).translate({ x: '-50%' })
    } else {
      // 正常页面（含避让逻辑）
    }
  }
}
```

关键点：隐藏导航条后系统会自动支持从底部上滑手势恢复导航条显示。

---

## 场景3：短视频沉浸

**场景描述：**
- 短视频类应用，视频画面铺满全屏，延伸到状态栏和导航条后方实现沉浸
- 浮层 TabBar 叠加在视频上，交互区域避让导航条防止误触
- 多设备适配：手机（sm/md）底部水平 TabBar + 避让导航条，平板（lg）左侧垂直侧边栏 + 无需底部避让

**多设备体验标准：**

针对短视频场景，在确保核心信息完整的情况下，尽量减少边距缩进。

**解决方案：** 使用 **setWindowLayoutFullScreen 开启全屏** + **getWindowAvoidArea + avoidAreaChange 获取并监听避让区** + **AppStorage + @StorageProp 全局响应避让高度** + **Stack 叠 Tabs(barHeight=0) + 浮层 TabBar（padding 避让导航条）** + **BreakpointObserver 断点系统驱动多设备布局切换**

### 步骤 1：EntryAbility 开启全屏 + 避让区监听

```ts
onWindowStageCreate(windowStage: window.WindowStage): void {
  windowStage.loadContent('pages/Index', (err) => {
    if (err.code) { return; }
    let windowClass = windowStage.getMainWindowSync();

    windowClass.setWindowLayoutFullScreen(true);

    // 获取初始避让区高度并通过 AppStorage 全局共享
    let avoidArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
    AppStorage.setOrCreate('topRectHeight', avoidArea.topRect.height);
    avoidArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
    AppStorage.setOrCreate('bottomRectHeight', avoidArea.bottomRect.height);

    // 初始化断点观察者
    BreakpointObserver.getInstance().init(windowClass);

    // 动态监听避让区变化（旋转/折叠/系统栏切换时自动更新）
    windowClass.on('avoidAreaChange', (data) => {
      if (data.type === window.AvoidAreaType.TYPE_SYSTEM) {
        AppStorage.setOrCreate('topRectHeight', data.area.topRect.height);
      } else if (data.type === window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR) {
        AppStorage.setOrCreate('bottomRectHeight', data.area.bottomRect.height);
      }
    });
  });
}
```

### 步骤 2：Stack 叠加布局 + 浮层 TabBar 避让导航条


主页面核心代码：

```ts
@Entry
@Component
struct Index {
  @StorageProp('currentBreakpoint') currentBreakpoint: string = 'sm';
  @StorageProp('bottomRectHeight') bottomRectHeight: number = 0;

  private isSmallScreen(): boolean {
    return this.currentBreakpoint === 'sm' || this.currentBreakpoint === 'md';
  }

  build() {
    Stack({ alignContent: this.isSmallScreen() ? Alignment.Bottom : Alignment.TopStart }) {
      Tabs({ controller: this.tabsController }) {
        TabContent() { this.VideoTab() }
        // ...其他 TabContent
      }
      .width('100%').height('100%').barHeight(0)

      this.CustomTabBar()  // 浮层 TabBar
    }
    .width('100%').height('100%').backgroundColor(Color.Black)
  }
}
```

### 步骤 3：浮层 TabBar 避让核心逻辑

```ts
@Builder
CustomTabBar() {
  Column() {
    Flex({ direction: this.isSmallScreen() ? FlexDirection.Row : FlexDirection.Column }) {
      // ...Tab 项
    }
    .width(this.isSmallScreen() ? '100%' : 64)
    .height(this.isSmallScreen() ? 56 : '100%')
    .backgroundColor('#00000000')
    // 核心：紧凑型底部 padding 避让导航条，宽屏型无需避让
    .padding({ bottom: this.isSmallScreen() ? this.getUIContext().px2vp(this.bottomRectHeight) : 0 })
  }
}
```

关键点：
- 紧凑型：`padding({ bottom: px2vp(bottomRectHeight) })` 将 TabBar 内容上移避开导航条
- 宽屏型：左侧垂直侧边栏不受底部导航条影响，无需 padding
- `bottomRectHeight` 通过 `@StorageProp` 响应式绑定，避让区变化时 UI 自动刷新
- TabBar 背景透明，不遮挡视频内容
---

## 场景4：挖孔区适配

**场景描述：**
- 竖屏挖孔在顶部，横屏挖孔在左/右侧边，需动态切换避让边
- 固定交互元素（标题栏、搜索框、Tab栏、底部导航栏）需避开挖孔区且背景延伸不留间隙
- 可滚动内容（列表/卡片）和悬浮控件（弹窗/侧边栏）无需避让

**多设备体验标准：**

- 界面布局需要适配摄像头的挖孔区域，若重要信息或交互操作 (例如底部页签/顶部页签、工具栏、标题栏、搜索框、输入框、悬浮按钮、横幅通知等) 和挖孔区之间有遮挡，则需要局部避开挖孔区显示。

- 若重要信息或交互操作和挖孔区无遮挡，则无需避开挖孔区显示；悬浮类控件或功能 (例如弹出框、侧边栏等)，无需避开挖孔区显示；可以上下滚动的内容，例如列表、卡片等无需避开挖孔区显示。

- 若应用支持横竖屏旋转，则横竖屏的界面布局均需满足以上挖孔适配要求。

**解决方案：** **setWindowLayoutFullScreen + setWindowSystemBarEnable([])** + **getWindowAvoidArea(TYPE_CUTOUT) 同步获取四边挖孔** + **avoidAreaChange 旋转时自动更新** + **各固定组件 padding 避让 + expandSafeArea 背景沉浸**

### 步骤 1：EntryAbility 全屏 + 隐藏系统栏

```ts
windowStage.getMainWindow((err, mainWindow) => {
  mainWindow.setWindowLayoutFullScreen(true);
  mainWindow.setWindowSystemBarEnable([]); // 隐藏状态栏和导航栏
  mainWindow.setPreferredOrientation(window.Orientation.AUTO_ROTATION_RESTRICTED);
});
```

### 步骤 2：getWindowAvoidArea(TYPE_CUTOUT) 同步获取四边挖孔

```ts
private updateCutout(): void {
  const area = this.mainWindow!.getWindowAvoidArea(window.AvoidAreaType.TYPE_CUTOUT)
  const ctx = this.mainWindow!.getUIContext()
  if (area.topRect.height > 0)    p.top = ctx.px2vp(area.topRect.height + area.topRect.top)
  if (area.leftRect.width > 0)    p.left = ctx.px2vp(area.leftRect.left + area.leftRect.width)
  if (area.rightRect.width > 0)   p.right = ctx.px2vp(screenWidth - area.rightRect.left)
  if (area.bottomRect.height > 0) p.bottom = ctx.px2vp(screenHeight - area.bottomRect.top)
  this.cutoutPadding = p
}
```

关键点：同步返回，旋转时系统自动映射到对应边（竖屏 topRect → 横屏 leftRect/rightRect），无需手动判断方向。`avoidAreaChange` 旋转时自动触发。

### 步骤 3：固定组件 padding 避让 + expandSafeArea 背景延伸

```ts
// 标题栏：padding 避让内容 + expandSafeArea 延伸白色背景到挖孔区
Row().padding({ top: p.top, left: p.left, right: p.right })
  .backgroundColor('#FFFFFF')
  .expandSafeArea([SafeAreaType.CUTOUT], [SafeAreaEdge.TOP, SafeAreaEdge.START, SafeAreaEdge.END])

// 底部导航栏：同理
Row().padding({ bottom: p.bottom, left: p.left, right: p.right })
  .expandSafeArea([SafeAreaType.CUTOUT], [SafeAreaEdge.BOTTOM, SafeAreaEdge.START, SafeAreaEdge.END])
```

关键点：`expandSafeArea` 延伸背景色到挖孔区，`padding` 避让文字内容——**背景沉浸 + 内容避让**分离。

### 避让规则

| 元素类型 | 避让 | 方式 |
|---------|-----|------|
| 标题栏/搜索框/Tab栏/底部导航栏 | ✅ | padding + expandSafeArea |
| 列表/卡片（可滚动） | ❌ | 随 Scroll 自然滚动 |
| 弹窗/侧边栏（悬浮） | ❌ | Stack 独立层 |

---

## 场景5：状态栏适配

**场景描述：**
- 阅读类、工具类等常规页面，内容区域需避让顶部状态栏，防止文字/控件被状态栏遮挡
- 背景色延伸到状态栏后方实现沉浸，同时顶部标题栏/内容通过 padding 下移
- 状态栏高度随设备变化（折叠屏展开/旋转），需动态响应

**多设备体验标准：**

应用需要对状态栏进行适配显示。

- 采用沉浸一体化的背景设计，保证效果的整体性，避免状态栏区域被单独切割。

- 根据页面内状态栏区域的背景色选择合适的状态栏颜色 (黑/白)，保证状态栏信息的易读性。

- 避免在状态栏背景区域内采用左右半区对比差异过大的颜色，导致部分状态栏信息无法阅读。

**解决方案：** 使用 **setWindowLayoutFullScreen 开启全屏** + **WindowUtil 单例封装 getWindowAvoidArea + avoidAreaChange** + **监听器回调模式驱动页面状态更新** + **根容器 padding({ top: topAvoidHeight }) 避让状态栏**

### 步骤 1：EntryAbility 开启全屏布局并初始化 WindowUtil

```ts
onWindowStageCreate(windowStage: window.WindowStage): void {
  windowStage.loadContent('pages/Index', (err) => {
    if (err.code) { return; }
    const mainWindow = windowStage.getMainWindowSync();
    mainWindow.setWindowLayoutFullScreen(true);
    WindowUtil.getInstance().init(mainWindow);
  });
}
```

### 步骤 2：WindowUtil 单例——获取并监听避让区

```ts
export interface AvoidAreaInfo { topHeight: number; bottomHeight: number; }

export class WindowUtil {
  private static instance: WindowUtil | null = null;
  private mainWindow: window.Window | null = null;
  private avoidAreaInfo: AvoidAreaInfo = { topHeight: 0, bottomHeight: 0 };
  private listeners: Set<(info: AvoidAreaInfo) => void> = new Set();

  static getInstance(): WindowUtil { /* 单例 */ }

  init(mainWindow: window.Window): void {
    this.mainWindow = mainWindow;
    this.updateAvoidArea();
    this.mainWindow.on('avoidAreaChange', () => { this.updateAvoidArea(); });
  }

  private updateAvoidArea(): void {
    const systemArea = this.mainWindow!.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
    const navArea = this.mainWindow!.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
    this.avoidAreaInfo = {
      topHeight: px2vp(systemArea.topRect.height),
      bottomHeight: px2vp(navArea.bottomRect.height)
    };
    this.listeners.forEach(cb => cb(this.avoidAreaInfo));
  }

  registerListener(cb: (info: AvoidAreaInfo) => void): void {
    this.listeners.add(cb);
    cb(this.avoidAreaInfo); // 立即回传当前值
  }

  unregisterListener(cb: (info: AvoidAreaInfo) => void): void { this.listeners.delete(cb); }

  destroy(): void {
    this.mainWindow?.off('avoidAreaChange');
    this.listeners.clear();
    this.mainWindow = null;
    WindowUtil.instance = null;
  }
}
```

关键点：
- 通过 `TYPE_SYSTEM` 获取状态栏高度，`TYPE_NAVIGATION_INDICATOR` 获取导航条高度
- `avoidAreaChange` 监听折叠屏展开、旋转等场景的高度变化，自动通知所有注册页面
- 注册时立即回传当前值，确保页面初始化即拿到正确高度

### 步骤 3：页面消费避让高度——根容器 padding 避让

```ts
@Entry
@Component
struct Index {
  @State topAvoidHeight: number = 0;

  aboutToAppear(): void {
    WindowUtil.getInstance().registerListener((info) => {
      this.topAvoidHeight = info.topHeight;
    });
  }

  build() {
    Stack() {
      Column() {
        TopBar()
        Scroll() {
          // 页面内容...
        }.layoutWeight(1)
        BottomBar()
      }
    }
    .padding({ top: this.topAvoidHeight })  // 根容器顶部 padding 避让状态栏
  }
}
```

关键点：
- 根容器通过 `padding({ top: topAvoidHeight })` 整体下移，所有子组件自动避开状态栏
- `topAvoidHeight` 为 `@State` 变量，避让区变化时 UI 自动刷新
- 页面销毁时调用 `unregisterListener` 避免泄漏

---

## 场景6：键盘易操作

**场景描述：**
- 含表单输入、操作按钮、列表的页面，需适配折叠屏/平板大屏双手操作易达性
- 软键盘弹出时不遮挡输入框、底部操作按钮和弹窗
- 大屏设备操作按钮置于底部两侧拇指热区，小屏居中排列
- 支持键盘 Tab 焦点导航、方向键网格导航和快捷键操作

**多设备体验标准：**

页面布局满足折叠屏/平板等大屏设备双手操作易操作性，键盘输入时，键盘上的按键操作要避开难交互区域。

**解决方案：** 使用 **WindowUtil 单例监听 TYPE_SYSTEM + TYPE_NAVIGATION_INDICATOR + TYPE_KEYBOARD 三类避让区** + **BreakpointManager 断点系统驱动布局切换** + **外层 Column padding({ bottom: keyboardHeight }) 缩小可视区域** + **操作栏放入 Scroll 内部随内容滚动避开键盘** + **弹窗用独立 padding({ bottom: keyboardHeight }) 上推** + **tabIndex + nextFocus + KeyboardShortcutManager 实现键盘导航**

### 步骤 1：WindowUtil 监听三类避让区（状态栏 + 导航条 + 键盘）

```ts
export interface AvoidAreaInfo { topHeight: number; bottomHeight: number; keyboardHeight: number; }

private updateAvoidArea(): void {
  const systemArea = this.mainWindow!.getWindowAvoidArea(AvoidAreaType.TYPE_SYSTEM);
  const navArea = this.mainWindow!.getWindowAvoidArea(AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
  const kbArea = this.mainWindow!.getWindowAvoidArea(AvoidAreaType.TYPE_KEYBOARD);
  const ctx = this.mainWindow!.getUIContext();
  this.avoidAreaInfo = {
    topHeight: ctx.px2vp(systemArea.topRect.height),
    bottomHeight: ctx.px2vp(navArea.bottomRect.height),
    keyboardHeight: ctx.px2vp(kbArea.bottomRect.height)
  };
  this.notifyListeners();
}
```

关键点：`TYPE_KEYBOARD` 返回键盘占据的底部高度，键盘收起时为 0。`avoidAreaChange` 在键盘弹出/收起/焦点切换时自动触发。

### 步骤 2：外层 Column 用 keyboardHeight 缩小可视区域

```ts
private getBottomPadding(): number {
  let padding = this.keyboardHeight;
  if (this.currentBp === 'sm') { padding += this.bottomAvoidHeight; }
  return padding;
}

// 根容器
Column() {
  TopBar()
  Scroll() { /* 表单 + 列表 + 操作栏 */ }
}
.padding({ top: this.topAvoidHeight, bottom: this.getBottomPadding() })
```

关键点：`keyboardHeight` 加入根容器 bottom padding，Scroll 可视区域等比缩小，内容整体上移至键盘上方，系统自动滚动到焦点输入框。

### 步骤 3：操作栏放入 Scroll 内部——键盘弹出时可滚达

```
Column（paddingBottom = keyboardHeight + bottomAvoidHeight）
├── TopBar（固定顶部）
└── Scroll
    ├── FormSection（表单输入）
    ├── GridSection（列表卡片）
    └── BottomBar（取消 + 提交按钮）  ← 在 Scroll 内部，可滚动触达
```

关键点：操作栏在 Scroll 内部而非固定底部，键盘弹出后用户向下滚动即可找到按钮，不会因可视区域缩小而丢失。

### 步骤 4：弹窗独立避让——padding 上推而非压缩高度

```ts
// 弹窗作为 Stack 兄弟节点，不受 Column padding 影响
Column()  // 弹窗外层遮罩
  .width('100%')
  .height('100%')
  .padding({ bottom: this.keyboardHeight })  // 底部留出键盘空间
  .justifyContent(FlexAlign.Center)          // 居中区域自动缩小到键盘上方
```

关键点：弹窗是 Stack 中的独立层，用自身 `padding({ bottom: keyboardHeight })` 上推居中区域，不影响主内容层布局。

### 步骤 5：断点系统驱动大屏双手易达性

```ts
// BreakpointManager 监听 WidthBreakpoint 系统枚举
private getFormColumns(): number {
  if (this.currentBp === 'lg') return 3;   // 平板三列
  if (this.currentBp === 'md') return 2;   // 折叠屏展开两列
  return 1;                                 // 手机单列
}
private getSideMargin(): number {
  if (this.currentBp === 'lg') return 48;  // 大屏两侧留白，内容居中
  if (this.currentBp === 'md') return 32;
  return 0;
}
// 操作栏：大屏按钮在底部两侧（拇指热区）
Row() {
  Button('取消').width(sm ? 100 : 120)
  Blank()
  Button('提交').width(sm ? 100 : 120)
}
.padding({ left: sm ? 16 : sideMargin + 16, right: sm ? 16 : sideMargin + 16 })
```

关键点：sm 单列全宽、md 两列 + 侧边距、lg 三列 + 大侧边距，操作按钮始终在底部两侧拇指易达区域。

### 步骤 6：键盘焦点导航与快捷键

```ts
// Tab 顺序：顶栏 → 表单 → 列表 → 底部按钮 → 弹窗
TextInput().tabIndex(3).id('input_username')
TextInput().tabIndex(4).id('input_email')
// 卡片方向键网格导航
Column().focusable(true).tabIndex(10 + index)
  .nextFocus({
    left: `card_${index - 1}`, right: `card_${index + 1}`,
    up: `card_${index - columns}`, down: `card_${index + columns}`
  })
// 全局快捷键
this.shortcutManager.registerAll([
  { key: KeyCode.KEYCODE_S, ctrl: true, action: () => this.onSubmit() },
  { key: KeyCode.KEYCODE_ESCAPE, action: () => this.handleEscape() },
]);
// 弹窗内焦点隔离 + 默认焦点
Button('确认').tabIndex(31).defaultFocus(true)
```

关键点：tabIndex 按视觉阅读顺序编号，nextFocus 基于列数动态计算上下左右目标，弹窗内 tabIndex 独立编号段，`defaultFocus(true)` 确保弹窗打开时焦点落在确认按钮上。

---
