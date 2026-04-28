# 问题修复案例集

## 目录

1. [场景1：阅读器应用顶部内容被状态栏遮挡](#场景1阅读器应用顶部内容被状态栏遮挡)
2. [场景2：全屏应用挖孔区内容遮挡或交互失效](#场景2全屏应用挖孔区内容遮挡或交互失效)
3. [场景3：短视频底部没有适配沉浸式布局](#场景3短视频底部没有适配沉浸式布局)
4. [场景4：顶部 padding 位置错误导致背景色间隙](#场景4顶部-padding-位置错误导致背景色间隙)
5. [场景5：输入法键盘拉起导致引用视图截断](#场景5输入法键盘拉起导致引用视图截断)
6. [场景6：底部工具栏整体高度限制导致输入法区域压缩异常](#场景6底部工具栏整体高度限制导致输入法区域压缩异常)
7. [场景7：全屏应用底部内容被系统导航指示器遮挡](#场景7全屏应用底部内容被系统导航指示器遮挡)
8. [场景8：输入法弹起导致页面内容被键盘遮挡](#场景8输入法弹起导致页面内容被键盘遮挡)
9. [场景9：消息列表页标题栏与底部导航栏未实现沉浸式滚动隐藏](#场景9消息列表页标题栏与底部导航栏未实现沉浸式滚动隐藏)
10. [场景10：windowSizeChange 回调中 getWindowAvoidArea 获取到旧避让值（时序问题）](#场景10windowsizechange-回调中-getwindowavoidarea-获取到旧避让值时序问题)
11. [场景11：仅在启动时读取一次避让区域，折叠/展开后标题栏与状态栏重叠](#场景11仅在启动时读取一次避让区域折叠展开后标题栏与状态栏重叠)

---

## 场景1：阅读器应用顶部内容被状态栏遮挡

**问题描述：**
- 多设备适配场景（手机、折叠屏、平板）
- 应用全屏显示
- 顶部有固定内容（如标题栏、工具栏）
- 顶部内容被状态栏遮挡
- 不同设备遮挡程度不同（状态栏高度 32–48vp），折叠屏、平板设备遮挡更严重

**根因分析：**
1. 未动态获取状态栏高度
2. 缺少顶部避让处理
3. 硬编码无法适配多设备

**Badcase：**

```typescript
@Entry
@Component
struct Index {

  build() {
    Column() {
      TopBar() 
      // ...页面内容
    }
    // ❌ 未设置 .padding({ top: this.topAvoidHeight })
  }
}
```

**解决方案：** 使用 **getWindowAvoidArea() 获取避让区域** + **监听 avoidAreaChange** + **动态设置 padding**

### 步骤 1：获取避让区域高度

```typescript
const systemArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
this.statusBarHeight = px2vp(systemArea.topRect.height);

const navigationArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
this.navigationBarHeight = px2vp(navigationArea.bottomRect.height);
```

**关键点：**
- `TYPE_SYSTEM`: 系统状态栏避让区域
- `TYPE_NAVIGATION_INDICATOR`: 导航栏避让区域
- 使用 `px2vp()` 将像素转换为 vp

### 步骤 2：监听避让区域变化

```typescript
windowClass.on('avoidAreaChange', (data: window.AvoidAreaOptions) => {
  if (data.type === window.AvoidAreaType.TYPE_SYSTEM) {
    this.statusBarHeight = px2vp(data.area.topRect.height);
  }
});
```

**关键点：**
- 监听折叠屏、横竖屏等导致的避让区域变化
- 在 `aboutToDisappear()` 中取消监听

### 步骤 3：动态设置避让

```typescript
@Entry
@Component
struct Index {
  @State statusBarHeight: number = 0;

  build() {
    Column() {
      // 页面内容
    }
    .padding({ top: this.statusBarHeight })
  }
}
```

**关键点：**
- 在根容器设置 `padding({ top: this.statusBarHeight })`
- 通过 `@State` 实现响应式更新

---

## 场景2：全屏应用挖孔区内容遮挡或交互失效

**问题描述：**
- 全屏游戏或沉浸式应用
- 使用 `ignoreLayoutSafeArea()` 全屏显示
- 设备有挖孔（前置摄像头、传感器等）
- 横竖屏切换场景
- 顶部内容被挖孔遮挡（居中单孔、左侧单孔、药丸形挖孔）
- 横屏时左右挖孔遮挡关键 UI
- 使用 `ignoreLayoutSafeArea()` 后无法自动避让

**根因分析：**
1. `ignoreLayoutSafeArea()` 会忽略安全区域，导致内容延伸到挖孔区
2. 未获取 `TYPE_CUTOUT` 避让区域信息
3. 缺少四方向挖孔检测和避让逻辑
4. 没有监听横竖屏切换导致的挖孔区域变化

**Badcase：**

```typescript
build() {
  Column() {
    // ...顶部栏、内容区
  }
  .width('100%')
  .height('100%')
  .ignoreLayoutSafeArea([LayoutSafeAreaType.SYSTEM], [LayoutSafeAreaEdge.TOP, LayoutSafeAreaEdge.BOTTOM])
  // ❌ ignoreLayoutSafeArea 忽略安全区域，但未获取 TYPE_CUTOUT 挖孔避让区域
}
```

**解决方案：** 使用 **CutoutAvoidanceManager 管理器** + **监听 avoidAreaChange** + **动态设置 padding**

### 步骤 1：初始化管理器并监听变化

```typescript
async init(context: common.UIAbilityContext): Promise<void> {
  this.mainWindow = await window.getLastWindow(context);

  this.mainWindow.on('avoidAreaChange', (data: window.AvoidAreaOptions) => {
    if (data.type === window.AvoidAreaType.TYPE_CUTOUT) {
      this.updateAvoidPadding(data.area);
    }
  });

  const cutoutArea = this.mainWindow.getWindowAvoidArea(window.AvoidAreaType.TYPE_CUTOUT);
  this.updateAvoidPadding(cutoutArea);
}
```

### 步骤 2：四方向挖孔检测

```typescript
private updateAvoidPadding(area: window.AvoidArea): void {
  const padding: CutoutPadding = {};

  if (area.topRect.height > 0) {
    padding.top = px2vp(area.topRect.height + area.topRect.top);
  }
  if (area.leftRect.width > 0) {
    padding.left = px2vp(area.leftRect.left + area.leftRect.width);
  }
  if (area.rightRect.width > 0) {
    padding.right = px2vp(screenWidth - area.rightRect.left);
  }
  if (area.bottomRect.height > 0) {
    padding.bottom = px2vp(screenHeight - area.bottomRect.top);
  }

  this.currentPadding = padding;
  this.notifyListeners();
}
```

### 步骤 3：页面中使用

```typescript
@Entry
@Component
struct GamePage {
  @State cutoutPadding: CutoutPadding = {};
  private cutoutManager: CutoutAvoidanceManager = CutoutAvoidanceManager.getInstance();

  aboutToAppear(): void {
    const context = this.getUIContext().getHostContext() as common.UIAbilityContext;
    this.cutoutManager.init(context);
    this.cutoutManager.onPaddingChange((padding) => {
      this.cutoutPadding = padding;
    });
  }

  build() {
    Column() {
      // 游戏内容
    }
    .padding(this.cutoutPadding)
    .ignoreLayoutSafeArea([LayoutSafeAreaType.SYSTEM], [LayoutSafeAreaEdge.TOP, LayoutSafeAreaEdge.BOTTOM])
  }
}
```

---

## 场景3：短视频底部没有适配沉浸式布局

**问题描述：**
- 全屏沉浸式视频播放场景
- 使用自定义底部 Tab 栏替代系统 Tab 栏
- 视频播放器底部有进度条等交互元素
- 底部内容区域被系统导航栏上推，未延伸到屏幕底部
- 底部自定义 Tab 栏和进度条未延伸到导航栏区域
- 视频内容未实现真正的沉浸式效果

**根因分析：**
1. Tabs 组件的默认栏（barHeight: 56）占用底部空间，导致内容区域被压缩
2. 在 Stack 外层添加 `padding({ bottom: bottomRectHeight })`，将整个内容区域上推，只是避开了导航栏而非沉浸式适配
3. 底部交互元素未采用沉浸式布局方式，只是简单避让

**Badcase：**

```typescript
Stack({ alignContent: Alignment.Bottom }) {
  Tabs({ barPosition: BarPosition.End, controller: this.tabController }) {
    // TabContent内容...
  }
  .vertical(false)
  .barHeight(56)  // ← 默认栏占用底部空间
  .height('100%')
  .width('100%')

  this.CustomTabBar()
}
.width('100%')
.height('100%')
.padding({ bottom: px2vp(this.bottomRectHeight) })  // ← 外层 padding 上推整体内容
```

**解决方案：** 隐藏 Tabs 默认栏 + 移除外层 padding 实现背景延伸 + 为底部交互元素添加 padding 保持在安全区域

### 步骤 1：隐藏 Tabs 默认栏

```typescript
Tabs({ barPosition: BarPosition.End, controller: this.tabController }) {
  // TabContent内容...
}
.vertical(false)
.barHeight(0)  // ✅ 隐藏Tabs默认栏
.height('100%')
.width('100%')
```

**关键点：**
- 将 `barHeight` 从 56 改为 0
- 避免 Tabs 默认栏占用底部空间

### 步骤 2：移除 Stack 外层的 padding

```typescript
Stack({ alignContent: Alignment.Bottom }) {
  Tabs({ barPosition: BarPosition.End, controller: this.tabController }) {
    // TabContent内容...
  }

  this.CustomTabBar()
}
.width('100%')
.height('100%')
// ✅ 移除外层padding，避免整体布局偏移
```

**关键点：**
- 移除 `.padding({ bottom: px2vp(this.bottomRectHeight) })`
- 避免内容区域整体上移

### 步骤 3：为底部交互元素添加自定义 Tab 栏高度 padding

```typescript
Column() {
  Row() {
    Slider({
      value: this.currentTime,
      min: 0,
      max: this.duration,
      step: 1,
      style: SliderStyle.OutSet
    })
      .blockColor('#FF6600')
      .trackColor('#33FFFFFF')
      .selectedColor('#FF6600')
      .layoutWeight(1)
  }
  .width('100%')
  .padding({ left: 16, right: 16, bottom: 56 })  // ✅ 添加底部padding避免被Tab栏遮挡
  .backgroundColor('#33000000')
}
```

**关键点：**
- 为底部所有交互元素（进度条、点赞评论按钮、视频描述等）添加 `.padding({ bottom: 56 })`
- **56vp 是自定义 Tab 栏的高度**，确保底部内容不被 Tab 栏遮挡
- **适用原则**：任何位于页面底部、需要保持可见的交互元素，都应添加与自定义 Tab 栏等高的底部 padding

---

## 场景4：顶部 padding 位置错误导致背景色间隙 & 底部 padding 位置错误导致列表无法沉浸式滚动

**问题描述：**
- 全屏沉浸式布局，顶部标题栏白色背景，外层容器灰色背景
- 问题一（顶部）：状态栏与标题栏之间出现灰色间隙，白色背景未延伸到状态栏
- 问题二（底部）：底部列表内容被导航指示器遮挡，无法滚动到最后几条数据

**根因分析：**
1. 顶部 padding 加在外层灰色容器上而非标题栏上，白色标题栏未延伸到状态栏，产生色差间隙
2. 顶部使用了错误变量 `navBarHeight`，应使用 `statusBarHeight`
3. 底部 padding 加在外层 Stack 上而非 Scroll 上，仅压缩了布局高度，滚动到底部时内容仍被导航指示器遮挡

**Badcase：**

```typescript
Column() {
  Column() { this.HeaderArea() }
    .backgroundColor(Color.White)

  Stack() { this.ContentArea() }
    .layoutWeight(1)
}
.backgroundColor('#ffe5e4e4')
.padding({ top: this.navBarHeight })  // ❌ 顶部：外层灰色容器加 padding，且变量错误

// ContentArea 内部：
Stack() { /* ... */ }
  .padding({ bottom: this.navBarHeight })  // ❌ 底部：padding 在外层 Stack，Scroll 内容无避让
```

**解决方案：** padding 加在需要延伸背景色的子组件上，而非外层容器

```typescript
Column() {
  Column() { this.HeaderArea() }
    .backgroundColor(Color.White)
    .padding({ top: this.statusBarHeight })  // ✅ 顶部：padding 在标题栏，白色延伸到状态栏

  Stack() { this.ContentArea() }
    .layoutWeight(1)
}
.backgroundColor('#ffe5e4e4')

// ContentArea 内部：
Scroll() { /* ... */ }
  .padding({ bottom: this.navBarHeight })  // ✅ 底部：padding 在 Scroll 上，滚动内容正确避让导航指示器
```

**关键点：**
- **顶部**：padding 加在标题栏容器上（`statusBarHeight`），让标题栏背景延伸到状态栏，消除间隙
- **底部**：padding 加在 Scroll 组件上（`navBarHeight`），让滚动内容在底部留出导航指示器避让空间

---

## 场景5：输入法键盘拉起导致引用视图截断

**问题描述：**
- 竖折叠模式（xs 断点）
- 输入框位于页面底部
- 引用视图在输入框上方
- 竖折时屏幕高度有限
- 输入法拉起占用底部空间
- 引用视图在输入框上方，空间压缩导致截断

**根因分析：**
1. 竖折时屏幕高度有限
2. 输入法拉起占用底部空间
3. 引用视图无高度限制，空间压缩时直接截断

**Badcase：**

```typescript
Column() {
  // ...消息列表
  Column() {
    Row() {
       // 引用视图内容（图片/文本等）
     }
     .padding({ left: 16, right: 16, top: 8, bottom: 8 })
     // ❌ 未使用 Scroll 包裹，未设置 constraintSize({ maxHeight }) 限制高度
     // ❌ xs 断点时无高度限制，输入法拉起后引用内容被截断
     
    Row() {
     // 输入法工具栏
    }
  }
}
```

**解决方案：** 基于 **xs 断点判断** + **Scroll 包裹** + **constraintSize 动态限制高度**

### 步骤 1：复用应用中已有断点系统

```typescript
// 假设应用已有断点变量，如：
// @State currentBreakpoint: string = 'md';

private getReferenceMaxHeight(): number | string {
  return this.currentBreakpoint === 'xs' ? 80 : 'auto';
}
```

**关键点：**
- 不修改现有断点监听逻辑
- 仅需添加一个高度计算方法
- 断点名称需与应用现有定义保持一致

### 步骤 2：修改引用视图布局结构

```typescript
Scroll() {
  // 引用视图内容
}
.width('100%')
.scrollBar(BarState.Auto)
.constraintSize({ maxHeight: this.getReferenceMaxHeight() })
```

**关键点：**
- 用 `Scroll` 组件包裹引用区域
- 添加 `constraintSize({ maxHeight })` 属性
- `maxHeight` 通过 `getReferenceMaxHeight()` 方法动态获取

---

## 场景6：底部工具栏整体高度限制导致输入法区域压缩异常

**问题描述：**
- 竖折叠模式（xs 断点）
- 引用视图和输入框组合成底部工具栏
- 底部工具栏整体设置了固定高度限制
- 输入法拉起时，底部工具栏整体高度被限制
- 引用视图和输入框空间分配不合理
- 引用视图可能被压缩或截断，用户体验差

**根因分析：**
1. 对整个底部工具栏设置了 `constraintSize({ maxHeight })`
2. 引用视图和输入框共享固定高度空间
3. 输入法拉起时，没有优先保证输入框可见性

**Badcase：**

```typescript
Column() {
  // 引用视图
  Scroll() { /* 引用内容 */ }

  // 输入框和按钮
  Row({ space: 10 }) {
    TextInput()
    Button('发送')
  }
}
.constraintSize({ maxHeight: 200 })  // ❌ 整体限制导致输入框空间不足
```

**解决方案：** 将高度限制从底部工具栏移到引用视图，用 **Scroll 包裹引用视图** + **constraintSize 限制引用视图高度**

### 步骤 1：调整断点高度配置

```typescript
private bottomBarMaxHeight: BreakpointType<string> = new BreakpointType(
  '80',    // xs: 竖折模式，限制引用视图高度避免挤压输入框
  'auto',  // sm:
  'auto',  // md:
  'auto',  // lg:
  'auto'   // xl:
);
```

**关键点：**
- 在 xs 断点时，引用视图高度限制为 80vp
- 其他断点时，引用视图高度自适应（'auto'）
- 底部工具栏整体不设置高度限制，让输入框有足够空间

### 步骤 2：修改引用视图布局结构

```typescript
Column() {
  Scroll() {
    // 引用视图模块
  }
  .scrollBar(BarState.Off)
  .constraintSize({ maxHeight: this.bottomBarMaxHeight.getValue(this.currentBreakpoint) })

  // 输入框和按钮
  Row({ space: 10 }) {

  }
}
// 注意：底部工具栏本身不设置高度，如 constraintSize 或者 height
```

**关键点：**
- 用 `Scroll` 组件包裹引用区域
- 添加 `constraintSize({ maxHeight })` 属性到 Scroll 组件
- `maxHeight` 通过断点系统动态获取
- 底部工具栏整体不设置高度限制，让输入框自适应

---

## 场景7：全屏应用底部内容被系统导航指示器遮挡

**问题描述：**
- 应用使用 `setWindowLayoutFullScreen(true)` 开启全屏沉浸式布局
- 页面底部有交互元素（如协议勾选、反馈链接、底部按钮等）
- 底部内容被系统导航指示器（手势条）遮挡
- 不同设备导航指示器高度不同（约 28–34vp），平板设备遮挡可能更严重
- 用户无法正常点击底部按钮或查看底部文字

**根因分析：**
1. 在 `EntryAbility` 中调用 `setWindowLayoutFullScreen(true)` 开启全屏布局，页面内容延伸到导航指示器区域
2. 页面未获取 `TYPE_NAVIGATION_INDICATOR` 避让区域高度
3. 未对底部内容设置相应的 padding 避让，导致内容被系统导航指示器覆盖

**Badcase：**

```typescript
@Entry
@Component
struct Index {
  // ❌ 缺少 @State bottomSafeHeight: number = 0;
  // ❌ 缺少 aboutToAppear 中获取导航指示器高度的逻辑

  Flex({ direction: FlexDirection.Column, alignItems: ItemAlign.Center }) {
    // 顶部内容...
    Blank()
    // 底部交互元素（协议勾选、反馈链接等）
    Row() { /* 底部内容 */ }
    Text('反馈')
  }
  .width('100%')
  .height('100%')
  // ❌ 未设置 .padding({ bottom: bottomSafeHeight })，底部内容被导航指示器遮挡
}
```

**解决方案：** 使用 **getWindowAvoidArea() 获取导航指示器高度** + **动态设置底部 padding**

### 步骤 1：声明底部安全区域高度状态变量

```typescript
@Entry
@Component
struct Index {
  @State bottomSafeHeight: number = 0;
  // ...
}
```

### 步骤 2：在 aboutToAppear 中获取导航指示器高度

```typescript
aboutToAppear(): void {
  let context = this.getUIContext().getHostContext() as common.UIAbilityContext;
  window.getLastWindow(context).then((win: window.Window) => {
    try {
      let avoidArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
      this.bottomSafeHeight = this.getUIContext().px2vp(avoidArea.bottomRect.height);
    } catch (e) {
      console.error(`getWindowAvoidArea error:${JSON.stringify(e)}`);
    }
  }).catch((err: BusinessError) => {
    console.error(`getLastWindow error:${JSON.stringify(err)}`);
  });
}
```

**关键点：**
- 使用 `TYPE_NAVIGATION_INDICATOR` 获取系统导航指示器避让区域
- 通过 `px2vp()` 将像素值转换为 vp
- 使用 `@State` 变量存储高度值，实现响应式更新

### 步骤 3：为底部内容添加动态 padding

```typescript
Flex({ direction: FlexDirection.Column, alignItems: ItemAlign.Center }) {
  // 顶部内容...

  Blank()

  Row() {
    Toggle({ type: ToggleType.Checkbox, isOn: this.agreed })
    Text('已阅读并同意 服务条款、隐私政策和华为账号服务须知')
  }
  .margin({ bottom: 12 })

  Text('反馈')
}
.width('100%')
.height('100%')
.padding({ bottom: this.bottomSafeHeight })  // ✅ 动态底部 padding 避让导航指示器
```

**关键点：**
- 在内容容器上添加 `.padding({ bottom: this.bottomSafeHeight })`
- 确保底部所有交互元素（协议勾选、反馈链接等）不被导航指示器遮挡
- 高度值从系统动态获取，自动适配不同设备

---

## 场景8：输入法弹起导致页面内容被键盘遮挡

**问题描述：**
- 页面包含可编辑区域（如笔记发布页、表单填写页），底部有固定工具栏
- 用户点击输入框拉起键盘后，页面内容和底部工具栏被键盘遮挡，无法操作

**根因分析：**
1. 使用 `RelativeContainer` 嵌套 + `alignRules` 锚定布局，输入法弹起时布局容器不会自动调整
2. 未设置 `KeyboardAvoidMode.RESIZE`，默认模式不会压缩页面可视区域
3. 内容区域使用固定高度，超出部分不可滚动

**Badcase：**

```typescript
// EntryAbility.ets ❌ 未设置键盘避让模式
onWindowStageCreate(windowStage: window.WindowStage): void {
  windowStage.loadContent('pages/Index', (err) => {
    // ❌ 缺少 setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)
  });
}

// Index.ets ❌ RelativeContainer 锚定布局，内容不可滚动
RelativeContainer() {
  RelativeContainer() {
    Column() { /* 内容 */ }
    Column() { this.SettingsList() }  // ❌ 固定高度 350，超出不可滚动
  }
  .alignRules({ bottom: { anchor: 'row2', align: VerticalAlign.Top } })

  Column() { this.BottomBar() }  // ❌ 锚定在容器底部，被键盘遮挡
  .alignRules({ bottom: { anchor: '__container__', align: VerticalAlign.Bottom } })
}
```

**解决方案：** 使用 **setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE)** + **Column + Scroll 替代 RelativeContainer**

### 步骤 1：在 EntryAbility 中设置键盘避让模式

```typescript
import { KeyboardAvoidMode, window } from '@kit.ArkUI';

onWindowStageCreate(windowStage: window.WindowStage): void {
  windowStage.loadContent('pages/Index', (err) => {
    windowStage.getMainWindowSync().getUIContext().setKeyboardAvoidMode(KeyboardAvoidMode.RESIZE);
  });
}
```

### 步骤 2：将 RelativeContainer 替换为 Column + Scroll 布局

```typescript
Column() {
  Scroll() {
    Column() {
      this.MediaSection()
      this.TitleSection()
      this.ContentSection()
      // ...
    }
  }
  .layoutWeight(1)  // ✅ 自适应剩余高度，键盘弹起时自动缩小

  Column() { this.BottomBar() }  // ✅ 底部栏固定在 Scroll 外部，始终可见
}
```

**关键点：**
- `KeyboardAvoidMode.RESIZE`：键盘弹起时系统自动压缩页面可视区域，必须在 `loadContent` 回调之后调用
- 用 `Column + Scroll` 替代 `RelativeContainer`，内容可自由滚动
- `Scroll` 使用 `layoutWeight(1)` 自适应高度，底部栏固定在 Scroll 外部始终可见

---

## 场景9：消息列表页标题栏与底部导航栏未实现沉浸式滚动隐藏

**问题描述：**
- 消息列表类应用（如钉钉、微信），页面由顶部标题栏、可滚动内容区域、底部导航栏三部分组成
- 标题栏固定高度（如 56vp），未延伸到状态栏区域，状态栏与标题栏之间存在视觉割裂
- 底部导航栏固定在屏幕底部，未为系统导航指示器留出避让空间，底部导航栏被手势条遮挡
- 用户上下滑动消息列表时，标题栏和底部导航栏始终占据屏幕空间，无法实现沉浸式浏览（滚动时自动隐藏、停止滚动时恢复显示）
- 折叠屏折叠/展开、窗口模式切换等设备状态改变时，避让参数未及时更新

**根因分析：**
1. `EntryAbility` 未调用 `setWindowLayoutFullScreen(true)`，页面内容未延伸到系统状态栏和导航指示器区域
2. 标题栏使用固定高度 `.height(56)`，未动态计算 `标题栏内容高度 + 顶部避让区高度`
3. 底部导航栏未设置底部 margin 避让系统导航指示器
4. 未监听窗口尺寸和避让区域变化，设备状态切换时参数不会刷新
5. 未使用 `onScrollFrameBegin` 监听列表滚动方向，无法根据滚动行为动态调整标题栏/底部导航栏的显示状态

**Badcase：**

```typescript
// EntryAbility.ets ❌ 未设置全屏布局，未导出窗口引用
export default class EntryAbility extends UIAbility {
  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/Index', (err) => {
      // ❌ 缺少 setWindowLayoutFullScreen(true)
      // ❌ 缺少 mainWindowRef 导出，页面无法获取窗口实例
    });
  }
}

// Index.ets ❌ 固定高度标题栏和底部导航栏，无避让和沉浸式滚动
@Entry
@Component
struct Index {
  build() {
    Column() {
      this.TitleBar()        // ❌ .height(56) 固定高度，无顶部避让 padding

      List({ space: 0 }) {
        // 消息列表内容...
      }
      .layoutWeight(1)
      .scrollBar(BarState.Off)  // ❌ 无 onScrollFrameBegin 滚动监听

      this.BottomTabBar()    // ❌ 无底部 margin 避让导航指示器
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#FFF2F2F6')
  }

  @Builder TitleBar() {
    Row() {
      // 标题栏内容...
    }
    .width('100%')
    .height(56)                        // ❌ 固定高度，未包含状态栏避让
    .padding({ left: 16, right: 8 })   // ❌ 无 top: topAvoidHeight
    .backgroundColor(Color.White)
  }

  @Builder BottomTabBar() {
    Row() {
      // 底部导航内容...
    }
    .width('100%')
    .backgroundColor(Color.White)      // ❌ 无 .height(this.tabsBarHeight)
    // ❌ 无 .margin({ bottom: this.barBottomMargin })
    // ❌ 无 .opacity(this.headerOpacity)
  }
}
```

**解决方案：** 使用 **setWindowLayoutFullScreen 全屏布局** + **动态避让区域监听** + **onScrollFrameBegin 滚动隐藏/恢复** + **窗口条件判断控制沉浸式开关**

### 步骤 1：EntryAbility 设置全屏布局并导出窗口引用

```typescript
// EntryAbility.ets
import { window } from '@kit.ArkUI';

export let mainWindowRef: window.Window | null = null  // ✅ 导出窗口引用供页面使用

export default class EntryAbility extends UIAbility {
  onWindowStageCreate(windowStage: window.WindowStage): void {
    try {
      mainWindowRef = windowStage.getMainWindowSync()
      mainWindowRef.setWindowLayoutFullScreen(true)  // ✅ 开启全屏沉浸式布局
    } catch (err) {
      hilog.error(DOMAIN, 'testTag', 'Failed to set full screen. Cause: %{public}s', JSON.stringify(err));
    }

    windowStage.loadContent('pages/Index', (err) => {
      // ...
    });
  }
}
```

**关键点：**
- `setWindowLayoutFullScreen(true)` 使页面内容延伸到状态栏和导航指示器区域
- 导出 `mainWindowRef` 供页面组件在 `aboutToAppear` 中获取窗口实例

### 步骤 2：定义常量、断点枚举和窗口条件判断函数

```typescript
// Index.ets
import { window } from '@kit.ArkUI'
import { mainWindowRef } from '../entryability/EntryAbility'

enum WidthBreakpoint {
  WIDTH_SM = 'sm',
  WIDTH_MD = 'md',
  WIDTH_LG = 'lg'
}

enum HeightBreakpoint {
  HEIGHT_SM = 'sm',
  HEIGHT_MD = 'md',
  HEIGHT_LG = 'lg'
}

class CommonConstants {
  static readonly DEFAULT_HEADER_HEIGHT: number = 56
  static readonly DEFAULT_TABS_HEIGHT: number = 54
  static readonly DEFAULT_BAR_BOTTOM_MARGIN: number = 0
  static readonly SCROLL_THRESHOLD: number = 100
}

// ✅ 触发沉浸浏览的窗口条件：横向断点SM且宽高比>0.5，或横向MD+纵向SM
function checkWindowCondition(widthBp: WidthBreakpoint, heightBp: HeightBreakpoint, windowSize: window.Size): boolean {
  const RATIO_THRESHOLD = 0.5;
  const width = windowSize?.width || 0;
  const height = windowSize?.height || 0;
  if (height === 0) {
    return false;
  }
  const isSmallWidth = widthBp === WidthBreakpoint.WIDTH_SM;
  const isNarrowRatio = (width / height) <= RATIO_THRESHOLD;
  const isMediumWidthLandscape = widthBp === WidthBreakpoint.WIDTH_MD && heightBp === HeightBreakpoint.HEIGHT_SM;

  if (isSmallWidth && !isNarrowRatio) {
    return true;
  }
  if (isMediumWidthLandscape) {
    return true;
  }
  return false;
}
```

**关键点：**
- `checkWindowCondition` 判断当前窗口是否满足沉浸式浏览条件
- `CommonConstants` 集中管理默认高度和滚动阈值

### 步骤 3：声明沉浸式相关状态变量，在 aboutToAppear 中获取避让区域并监听变化

```typescript
@Entry
@Component
struct Index {
  @State headerTitleHeight: number = CommonConstants.DEFAULT_HEADER_HEIGHT
  @State headerOpacity: number = 1
  @State tabsBarHeight: number = CommonConstants.DEFAULT_TABS_HEIGHT
  @State barBottomMargin: number = CommonConstants.DEFAULT_BAR_BOTTOM_MARGIN

  private topAvoidHeight: number = 0
  private bottomAvoidHeight: number = 0
  private defaultHeaderHeight: number = CommonConstants.DEFAULT_HEADER_HEIGHT
  private currentYOffset: number = 0
  private isHiding: boolean = false
  private immersionEnabled: boolean = false

  aboutToAppear(): void {
    const win = mainWindowRef
    if (!win) {
      return
    }

    // ✅ 获取顶部状态栏避让高度
    const topAvoidArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM)
    this.topAvoidHeight = this.getUIContext().px2vp(topAvoidArea.topRect.height)

    // ✅ 获取底部导航指示器避让高度
    const bottomAvoidArea = win.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR)
    this.bottomAvoidHeight = this.getUIContext().px2vp(bottomAvoidArea.bottomRect.height)

    // ✅ 初始化标题栏高度 = 内容高度 + 状态栏高度
    this.headerTitleHeight = this.defaultHeaderHeight + this.topAvoidHeight
    this.barBottomMargin = this.bottomAvoidHeight || CommonConstants.DEFAULT_BAR_BOTTOM_MARGIN

    // ✅ 计算断点并判断是否满足沉浸式条件
    const winSize = win.getWindowProperties().windowRect
    const vpWidth = this.getUIContext().px2vp(winSize.width)
    const vpHeight = this.getUIContext().px2vp(winSize.height)
    const widthBp = getWidthBreakpoint(vpWidth)
    const heightBp = getHeightBreakpoint(vpHeight)
    this.immersionEnabled = checkWindowCondition(widthBp, heightBp,
      { width: vpWidth, height: vpHeight } as window.Size)

    // ✅ 监听避让区域变化（折叠屏、横竖屏等）
    win.on('avoidAreaChange', (data: window.AvoidAreaOptions) => {
      if (data.type === window.AvoidAreaType.TYPE_SYSTEM) {
        this.topAvoidHeight = this.getUIContext().px2vp(data.area.topRect.height)
        if (!this.isHiding) {
          this.headerTitleHeight = this.defaultHeaderHeight + this.topAvoidHeight
        }
      }
      if (data.type === window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR) {
        this.bottomAvoidHeight = this.getUIContext().px2vp(data.area.bottomRect.height)
        if (!this.isHiding) {
          this.barBottomMargin = this.bottomAvoidHeight || CommonConstants.DEFAULT_BAR_BOTTOM_MARGIN
        }
      }
    })

    // ✅ 监听窗口尺寸变化（分屏、折叠等），重新判断沉浸式条件
    win.on('windowSizeChange', (size: window.Size) => {
      const vpW = this.getUIContext().px2vp(size.width)
      const vpH = this.getUIContext().px2vp(size.height)
      const wBp = getWidthBreakpoint(vpW)
      const hBp = getHeightBreakpoint(vpH)
      this.immersionEnabled = checkWindowCondition(wBp, hBp,
        { width: vpW, height: vpH } as window.Size)
      if (!this.immersionEnabled && this.isHiding) {
        this.restoreDefaults()
      }
    })
  }

  aboutToDisappear(): void {
    const win = mainWindowRef
    if (win) {
      win.off('avoidAreaChange')
      win.off('windowSizeChange')
    }
  }
}
```

**关键点：**
- `aboutToAppear` 获取初始避让区域并设置监听
- `aboutToDisappear` 中取消监听防止内存泄漏
- `avoidAreaChange` 监听覆盖折叠屏、横竖屏等设备状态变化
- `windowSizeChange` 监听覆盖分屏、窗口模式切换等场景

### 步骤 4：在 List 上使用 onScrollFrameBegin 实现滚动隐藏/恢复

```typescript
build() {
  Column() {
    this.TitleBar()

    Stack({ alignContent: Alignment.Bottom }) {  // ✅ Stack 包裹 List 和 BottomTabBar
      List({ space: 0 }) {
        // 消息列表内容...
      }
      .height('100%')
      .width('100%')
      .scrollBar(BarState.Off)
      .edgeEffect(EdgeEffect.Spring)
      .onScrollFrameBegin((offset: number, state: ScrollState) => {
        if (this.immersionEnabled) {
          if (offset > 0) {  // ✅ 向上滚动：线性隐藏标题栏和底部导航栏
            this.currentYOffset += offset
            if (this.currentYOffset <= CommonConstants.SCROLL_THRESHOLD) {
              this.tabsBarHeight =
                CommonConstants.DEFAULT_TABS_HEIGHT * (1 - this.currentYOffset / CommonConstants.SCROLL_THRESHOLD)
              this.barBottomMargin = (this.bottomAvoidHeight || CommonConstants.DEFAULT_BAR_BOTTOM_MARGIN) *
                (1 - this.currentYOffset / CommonConstants.SCROLL_THRESHOLD)
              this.headerTitleHeight = (this.defaultHeaderHeight + this.topAvoidHeight) *
                (1 - this.currentYOffset / CommonConstants.SCROLL_THRESHOLD)
              this.headerOpacity = 1 - this.currentYOffset / CommonConstants.SCROLL_THRESHOLD
            } else {
              this.tabsBarHeight = 0
              this.barBottomMargin = 0
              this.headerTitleHeight = 0
              this.headerOpacity = 0
            }
            this.isHiding = true
          }
          if (offset < 0 && this.isHiding) {  // ✅ 向下滚动：动画恢复标题栏和底部导航栏
            this.getUIContext().animateTo({ duration: 300 }, () => {
              this.tabsBarHeight = CommonConstants.DEFAULT_TABS_HEIGHT
              this.headerTitleHeight = this.defaultHeaderHeight + this.topAvoidHeight
              this.barBottomMargin = this.bottomAvoidHeight || CommonConstants.DEFAULT_BAR_BOTTOM_MARGIN
              this.headerOpacity = 1
              this.currentYOffset = 0
              this.isHiding = false
            })
          }
        }
        return { offsetRemain: offset }
      })

      this.BottomTabBar()  // ✅ 底部导航栏浮在 List 上方，隐藏时不占空间
    }
    .layoutWeight(1)
  }
  .width('100%')
  .height('100%')
  .backgroundColor('#FFF2F2F6')
}
```

**关键点：**
- 用 `Stack({ alignContent: Alignment.Bottom })` 包裹 List 和 BottomTabBar，底部导航栏浮在内容上方
- 向上滚动 100vp 范围内，标题栏高度、底部导航栏高度、底部边距、透明度线性递减至 0
- 超过 100vp 后直接归零，完全隐藏
- 向下滚动时用 `animateTo({ duration: 300 })` 动画恢复，视觉过渡平滑

### 步骤 5：将动态变量绑定到标题栏和底部导航栏组件

```typescript
@Builder TitleBar() {
  Row() {
    // 标题栏内容...
  }
  .width('100%')
  .height(this.headerTitleHeight)            // ✅ 动态高度（含状态栏避让）
  .padding({ left: 16, right: 8, top: this.topAvoidHeight })  // ✅ 顶部避让 padding
  .backgroundColor(Color.White)
  .opacity(this.headerOpacity)               // ✅ 动态透明度
  .alignItems(VerticalAlign.Bottom)           // ✅ 内容对齐到底部（标题栏内容在避让区下方）
}

@Builder BottomTabBar() {
  Row() {
    // 底部导航内容...
  }
  .width('100%')
  .height(this.tabsBarHeight)                // ✅ 动态高度
  .margin({ bottom: this.barBottomMargin })  // ✅ 动态底部边距（避让导航指示器）
  .backgroundColor(Color.White)
  .opacity(this.headerOpacity)               // ✅ 动态透明度
}
```

**关键点：**
- 标题栏 `.height(this.headerTitleHeight)` = 默认内容高度 + 状态栏避让高度，滚动时线性递减
- 标题栏 `.padding({ top: this.topAvoidHeight })` 确保内容不被状态栏遮挡
- 标题栏 `.alignItems(VerticalAlign.Bottom)` 让标题内容在避让区下方显示
- 底部导航栏 `.margin({ bottom: this.barBottomMargin })` 避让系统导航指示器
- 两者共享 `this.headerOpacity` 实现同步透明度变化

---

## 场景10：windowSizeChange 回调中 getWindowAvoidArea 获取到旧避让值（时序问题）

**问题描述：**
- 聊天类应用，使用 `setWindowLayoutFullScreen(true)` 开启全屏沉浸式布局
- 顶部标题栏需要避让状态栏，底部输入栏需要避让系统导航指示器
- 设备折叠/展开、横竖屏切换等场景下，避让区域未正确更新
- 底部输入栏被导航指示器遮挡，或顶部标题栏被状态栏遮挡
- 问题在折叠屏设备上尤为明显（折叠/展开时系统 UI 尺寸变化幅度大）

**根因分析：**
1. 在 `windowSizeChange` 回调中通过 `getWindowAvoidArea()` **主动查询**避让区域
2. `windowSizeChange` 触发时机早于系统 UI（状态栏、导航指示器）布局更新完成
3. 此时调用 `getWindowAvoidArea()` 拿到的仍是折叠/展开前的**旧值**
4. 应使用专有的 `avoidAreaChange` 监听接口，回调中的数据由系统保证是最新的

**Badcase：**

```typescript
// EntryAbility.ets
windowClass.on('windowSizeChange', () => {
  // ❌ windowSizeChange 回调中主动查询避让区域
  // ❌ 折叠/展开时系统 UI 可能还没更新完，拿到的是旧值
  const systemAvoidArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
  const navAvoidArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
  const topPadding = px2vp(systemAvoidArea.topRect.height);
  const bottomPadding = px2vp(navAvoidArea.bottomRect.height);
  AppStorage.setOrCreate('topPadding', topPadding);
  AppStorage.setOrCreate('bottomPadding', bottomPadding);
});
```

**解决方案：** 使用 **avoidAreaChange 专有监听接口**替代 windowSizeChange + getWindowAvoidArea 组合

### 步骤 1：将 windowSizeChange + getWindowAvoidArea 替换为 avoidAreaChange

```typescript
// EntryAbility.ets
// ✅ 通过 avoidAreaChange 专有监听接口获取避让区域变化
// ✅ 回调中的数据总是最新的、准确的，不存在时序问题
windowClass.on('avoidAreaChange', (data) => {
  if (data.type === window.AvoidAreaType.TYPE_SYSTEM) {
    const topPadding = windowClass.getUIContext().px2vp(data.area.topRect.height);
    AppStorage.setOrCreate('topPadding', topPadding);
  } else if (data.type === window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR) {
    const bottomPadding = windowClass.getUIContext().px2vp(data.area.bottomRect.height);
    AppStorage.setOrCreate('bottomPadding', bottomPadding);
  }
});
```

**关键点：**
- `avoidAreaChange` 是系统专有的避让区域变化监听接口，回调参数 `data.area` 由系统直接提供，保证数据准确
- `windowSizeChange` 仅表示窗口尺寸变化，不代表系统 UI 元素已完成布局更新，存在时序竞争
- 回调中通过 `data.type` 区分避让区域类型（`TYPE_SYSTEM` / `TYPE_NAVIGATION_INDICATOR`），按需更新
- 使用 `getUIContext().px2vp()` 而非全局 `px2vp()` 进行像素转换，确保上下文正确

---

## 场景11：仅在启动时读取一次避让区域，折叠/展开后标题栏与状态栏重叠

**问题描述：**
- 应用使用 `setWindowLayoutFullScreen(true)` 开启全屏沉浸式布局
- 页面顶部标题栏需要避让系统状态栏
- 启动时避让区域显示正常
- 折叠屏折叠/展开后，状态栏高度发生变化，但标题栏的顶部 padding 仍是启动时的旧值
- 导致标题栏与状态栏重叠或间距异常

**根因分析：**
1. 仅在 `onWindowStageCreate` 中通过 `getWindowAvoidArea()` 读取一次避让区域高度并存入 `AppStorage`
2. 未注册 `avoidAreaChange` 监听，折叠/展开后状态栏高度变化无法传递到页面
3. `@StorageLink` 变量不会自动更新，因为 `AppStorage` 中的值从未被刷新

**Badcase：**

```typescript
// EntryAbility.ets
let mainWindow = windowStage.getMainWindowSync();
mainWindow.setWindowLayoutFullScreen(true);

// ❌ 只在启动时读取一次，之后不再更新
let avoidArea = mainWindow.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
let topHeight = avoidArea.topRect.height;
AppStorage.setOrCreate('topAvoidHeight', topHeight);
// ❌ 缺少 avoidAreaChange 监听

windowStage.loadContent('pages/Index', (err) => { /* ... */ });
```

```typescript
// Index.ets
@StorageLink('topAvoidHeight') topAvoidHeight: number = 0;

build() {
  Column() {
    Row() { Text('首页') }
      .padding({ top: this.getUIContext().px2vp(this.topAvoidHeight) })
      // ❌ 折叠/展开后 topAvoidHeight 不变，标题栏与状态栏重叠

    // ...内容区
  }
}
```

**解决方案：** 注册 **avoidAreaChange 监听**，实时更新避让区域高度

### 步骤 1：将启动时一次性读取替换为 avoidAreaChange 持续监听

```typescript
// EntryAbility.ets
let mainWindow = windowStage.getMainWindowSync();
mainWindow.setWindowLayoutFullScreen(true);

// ✅ 注册 avoidAreaChange 回调，实时监听避让区变化
mainWindow.on('avoidAreaChange', (data: window.AvoidAreaOptions) => {
  if (data.type === window.AvoidAreaType.TYPE_SYSTEM) {
    let topHeight = data.area.topRect.height;
    AppStorage.setOrCreate('topAvoidHeight', topHeight);
  }
});

windowStage.loadContent('pages/Index', (err) => { /* ... */ });
```

**关键点：**
- `getWindowAvoidArea()` 是一次性快照查询，只在调用时刻返回当前值，不会跟随设备状态变化
- `avoidAreaChange` 是持续监听，折叠/展开、横竖屏切换等场景下自动回调最新避让区域数据
- 页面通过 `@StorageLink` 绑定 `AppStorage`，`avoidAreaChange` 回调更新 `AppStorage` 后页面自动刷新
- 避让区域高度存储原始 px 值，在页面中通过 `getUIContext().px2vp()` 转换为 vp 使用
