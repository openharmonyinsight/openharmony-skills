# 方向适配实际案例

实际项目中遇到的设备方向适配问题及解决方案，供类似场景参考复用。

---

## 案例 1：折叠屏展开态横屏使用应用时被强制切为竖屏

**场景标签**：折叠屏 · 屏幕方向 · deviceType · 方向锁定

### 问题描述

在折叠屏设备（如 Mate X5）展开态下横屏使用应用时，进入某个特定页面（如写邮件、编辑文档等表单类页面）后，屏幕方向被自动强制切换为竖屏，与用户当前持握方向不一致，导致体验中断。

具体表现：将折叠屏展开至展开态 → 横向持握确认处于横屏 → 进入目标页面 → 屏幕自动旋转为竖屏（预期应保持横屏）。

### 问题根因

开发者在特定页面中，通常会在页面生命周期（如 `aboutToAppear`）里，使用 `deviceInfo.deviceType === 'phone'` 判断当前是否为手机设备，若是则调用 `setPreferredOrientation(PORTRAIT)` 强制竖屏：

```typescript
const isPhone = deviceInfo.deviceType === 'phone';
if (isPhone) {
  win.setPreferredOrientation(window.Orientation.PORTRAIT);
}
```

关键知识点：HarmonyOS 中折叠屏设备（包括普通折叠屏和纵向折叠屏）的 `deviceInfo.deviceType` 均返回 `'phone'`，与普通直板手机一致。因此折叠屏展开态下也会命中该条件，被错误地强制竖屏。

> 参考：手机设备（包括普通手机和折叠屏手机）的 `deviceType()` 接口均返回 `phone`。可通过 `display.isFoldable()` 判断是否为可折叠设备。

### 解决方案

在强制竖屏逻辑前，增加折叠屏设备及折叠状态的判断。折叠屏展开态和悬停态拥有大屏空间，不应强制竖屏，应保持用户当前方向。

**修复前决策逻辑：**

```
deviceType === 'phone' ? → 强制竖屏
```

**修复后决策逻辑：**

```
deviceType === 'phone' ?
  ├─ display.isFoldable() === false → 强制竖屏（普通手机）
  └─ display.isFoldable() === true
       ├─ 折叠态 (FOLD_STATUS_FOLDED) → 强制竖屏（等同普通手机）
       └─ 展开态/悬停态 (EXPANDED / HALF_FOLDED) → 不强制，保持当前方向
deviceType !== 'phone' ?
  └─ 不强制竖屏（平板等）
```

**关键代码：**

```typescript
import { window } from '@kit.ArkUI';
import { deviceInfo } from '@kit.BasicServicesKit';
import { display } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';

aboutToAppear(): void {
  const ctx = this.getUIContext()?.getHostContext() as common.UIAbilityContext;
  const win = ctx.windowStage.getMainWindowSync();
  const isPhone = deviceInfo.deviceType === 'phone';
  if (isPhone) {
    // 折叠屏展开态不强制竖屏，保持用户当前方向
    const isFoldable = display.isFoldable();
    if (isFoldable) {
      const foldStatus = display.getFoldStatus();
      if (foldStatus === display.FoldStatus.FOLD_STATUS_EXPANDED ||
        foldStatus === display.FoldStatus.FOLD_STATUS_HALF_FOLDED) {
        return; // 保持当前方向
      }
    }
    // 普通手机 或 折叠屏折叠态：强制竖屏
    win.setPreferredOrientation(window.Orientation.PORTRAIT);
    this.didForcePortrait = true;
  }
}
```

涉及 API：
- `display.isFoldable()` — 判断设备是否为可折叠设备
- `display.getFoldStatus()` — 获取当前折叠状态（`FOLD_STATUS_FOLDED` / `FOLD_STATUS_EXPANDED` / `FOLD_STATUS_HALF_FOLDED`）

### 注意事项

1. **Pocket 系列特殊性**：纵向折叠屏（如 Pocket 2）的 `isFoldable()` 可能返回 `false`（需实际设备验证），如需特殊处理需额外适配
2. **退出页面时恢复方向**：页面生命周期（如 `aboutToDisappear`）中仅在 `didForcePortrait === true` 时才恢复自动旋转，折叠屏展开态因未强制竖屏，退出时不会触发不必要的方向重置
3. **页面布局适配**：该修复仅解决方向锁定问题。折叠屏展开态横屏下的页面 UI 布局适配应通过断点系统（BreakPoint）和响应式布局实现，而非通过折叠状态接口判断

---

## 案例 2：Tabs + Swiper 场景下短视频页方向锁定 Bug

**场景标签**：Tabs 生命周期 · Swiper · 短视频 · 方向锁定 · 折叠屏 · 平板

### 问题背景

在 HarmonyOS 折叠屏/平板设备上，应用使用 `Tabs` 组件实现"主页"和"短视频"两个 tab 页。`module.json5` 配置了 `orientation: "auto_rotation"`（自动旋转）。短视频 tab 内嵌套了垂直 `Swiper`（上下滑动切换视频）和水平 `Swiper`（左右滑动切换作者页）。

期望行为：主页和短视频页均跟随设备传感器自动旋转。但实际在折叠屏/平板设备上出现异常的方向锁定。

### 问题描述

在折叠屏/平板设备上，短视频 tab 的方向控制出现异常——**首次进入或滑动切换视频时被非预期锁定竖屏，而离开后再进入反而正常**。核心表现如下：

| 操作时机 | 方向行为 | 说明 |
|---|---|---|
| 首次进入短视频 tab | 被锁定竖屏 | 横屏进入时自动旋转为竖屏，无法手动旋转 |
| 离开后再次进入 | 跟随传感器 | 方向正常响应设备旋转 |
| 滑动切换视频时 | 重新锁定竖屏 | 每次 Swiper onChange 都触发竖屏锁定 |

典型复现路径：横屏打开应用 → 点击短视频 tab → 屏幕自动旋转为竖屏；切回主页再切回短视频 → 方向恢复正常；但在短视频页内滑动 → 又被锁定竖屏。

### 问题根因

根因涉及两个层面：**Tabs 生命周期陷阱**和**错误的方向控制时机**。

#### 1. Tabs 懒创建导致 `aboutToAppear` 只触发一次

HarmonyOS 的 `Tabs` 组件采用懒创建机制——子组件的 `aboutToAppear()` 仅在 tab 首次被选中时调用一次，后续的 tab 切换只是显示/隐藏，不会再次触发。同样，`aboutToDisappear()` 在 tab 被隐藏时也不会触发（仅在组件被真正销毁时才触发）。

```typescript
// ❌ 错误示范：依赖组件生命周期控制方向
@Component
struct VideoPage {
  private windowClass?: window.Window; // 假设已通过其他方式获取

  aboutToAppear(): void {
    // 只在 tab 首次创建时执行一次！
    this.windowClass?.setPreferredOrientation(window.Orientation.PORTRAIT);
  }

  aboutToDisappear(): void {
    // Tab 切换时根本不会触发！
    this.windowClass?.setPreferredOrientation(window.Orientation.AUTO_ROTATION);
  }
}
```

**结果：** 首次进入短视频时锁定竖屏生效，但切回主页时恢复代码不执行，导致整个应用被"卡"在竖屏状态。第二次进入短视频时 `aboutToAppear` 不再触发，表现看似正常——但这只是巧合。

#### 2. Swiper onChange 重复锁定方向

垂直 Swiper 的 `onChange` 回调中再次调用 `setPreferredOrientation(PORTRAIT)`，导致每次滑动切换视频都重新锁定竖屏：

```typescript
// ❌ 错误示范：在 Swiper 滑动时重复锁定
Swiper()
  .vertical(true)
  .onChange(() => {
    // 每次滑动都重新锁定竖屏！
    this.windowClass?.setPreferredOrientation(window.Orientation.PORTRAIT);
  })
```

#### 3. 未区分设备类型

代码对所有设备统一调用 `setPreferredOrientation(PORTRAIT)`，没有区分直板机和折叠屏/平板。直板机需要锁定竖屏（短视频为竖屏内容），但折叠屏/平板应保持自动旋转以适配大屏体验。

### 解决方案

核心思路：**将方向控制逻辑从子组件生命周期上移到 `Tabs.onChange`，并按设备类型条件执行。**

```typescript
import { window, display } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';

@Entry
@Component
struct Index {
  private windowClass?: window.Window;
  private isBarPhone: boolean = false;

  aboutToAppear(): void {
    const ctx = this.getUIContext()?.getHostContext() as common.UIAbilityContext;
    this.windowClass = ctx.windowStage.getMainWindowSync();
    // 推荐使用系统断点 API 判断设备类型，而非手动计算像素值
    const widthBp = this.getUIContext().getWindowWidthBreakpoint();
    const heightBp = this.getUIContext().getWindowHeightBreakpoint();
    // 直板机竖屏：横向 sm + 纵向 lg；折叠屏展开态/平板：横向 md/lg
    this.isBarPhone = widthBp === WidthBreakpoint.WIDTH_SM && heightBp === HeightBreakpoint.HEIGHT_LG;
  }

  build() {
    Tabs({ barPosition: BarPosition.End }) {
      TabContent() { /* 主页 */ }.tabBar('主页')
      TabContent() { VideoPage() }.tabBar('短视频')
    }
    .onChange((index: number) => {
      if (!this.windowClass || !this.isBarPhone) {
        return; // 折叠屏/平板：不做任何方向干预
      }
      if (index === 1) {
        // 直板机进入短视频：锁定竖屏
        this.windowClass.setPreferredOrientation(window.Orientation.PORTRAIT);
      } else {
        // 直板机离开短视频：恢复自动旋转
        this.windowClass.setPreferredOrientation(window.Orientation.AUTO_ROTATION);
      }
    })
  }
}

@Component
struct VideoPage {
  // ✅ 子组件不包含任何方向控制逻辑
  build() {
    Stack() {
      // 水平 Swiper + 垂直 Swiper ...
    }
  }
}
```

### 关键要点总结

| 要点 | 说明 |
|---|---|
| **不要在 Tabs 子组件中用生命周期控制方向** | `aboutToAppear` 只触发一次，`aboutToDisappear` 在 tab 隐藏时不触发 |
| **方向控制应放在 `Tabs.onChange`** | 每次 tab 切换都可靠触发 |
| **必须区分设备类型** | 直板机需要锁定竖屏，折叠屏/平板应保持自动旋转 |
| **子组件不应持有方向逻辑** | 方向控制属于窗口级别的全局状态，应在父组件统一管理 |
| **不要在 Swiper onChange 中重复锁定方向** | 滑动是高频操作，会导致方向被反复锁定 |

### 设备类型检测方法

```typescript
// 推荐方法：使用系统断点 API（WidthBreakpoint / HeightBreakpoint 枚举）
const widthBp = this.getUIContext().getWindowWidthBreakpoint();
const heightBp = this.getUIContext().getWindowHeightBreakpoint();
const isBarPhone = widthBp === WidthBreakpoint.WIDTH_SM && heightBp === HeightBreakpoint.HEIGHT_LG;
```

> 不推荐通过 `display.getDefaultDisplaySync()` 手动计算像素值判断设备类型。使用系统断点 API 更准确，且能自动适配分屏、自由窗口等场景。

典型设备断点参考：

- 直板手机竖屏：横向 sm（[320, 600) vp）+ 纵向 lg（高宽比 ≥ 1.2）
- 折叠屏展开态：横向 md（[600, 840) vp）+ 纵向 md（高宽比 [0.8, 1.2)）
- 平板竖屏：横向 md（[600, 840) vp）+ 纵向 lg（高宽比 ≥ 1.2）

---

## 案例 3：分屏/悬浮窗下旋转策略失效

**场景标签**：分屏 · 悬浮窗 · 旋转策略 · 窗口模式 · 平板

### 问题描述

应用在平板上配置了 `auto_rotation_restricted` 策略，全屏模式下横竖屏旋转正常。但当用户进入分屏或悬浮窗模式后，应用的方向不再响应设备旋转，即使调用 `setPreferredOrientation()` 也无法改变方向。

| | 说明 |
|---|---|
| **预期行为** | 分屏/悬浮窗下布局应适配窗口尺寸变化，无需旋转 |
| **实际行为** | 开发者试图在分屏下控制旋转，调用不生效，布局也未适配窗口变化 |

### 问题根因

HarmonyOS 系统在分屏、悬浮窗、自由多窗场景下，会**忽略**应用的旋转策略。`setPreferredOrientation()` 在这些模式下调用不会报错，但不会生效。这是系统级行为，无法绕过。

> 参考：分屏/悬浮窗场景下，系统忽略旋转策略，应用显示方向不会改变。退出这些场景后才根据策略重新调整。

### 解决方案

不要在分屏/悬浮窗场景下尝试控制方向，而是通过响应式布局适配不同窗口尺寸。

**核心思路**：

1. 监听 `windowSizeChange`，在回调中根据窗口宽高比调整布局
2. 通过断点系统（`WidthBreakpoint` / `HeightBreakpoint`）而非方向判断布局形态
3. 不要在分屏模式下调用 `setPreferredOrientation()`

```typescript
// ✅ 正确：通过断点适配不同窗口尺寸
private sizeCallback: Callback<window.Size> = (size: window.Size) => {
  const uiContext = this.getUIContext();
  const width = uiContext.px2vp(size.width);
  const height = uiContext.px2vp(size.height);
  this.isLandscape = width > height;
  // 根据窗口尺寸调整布局，而非控制旋转
};

// ❌ 错误：在分屏下尝试控制旋转（不生效）
this.windowClass.setPreferredOrientation(window.Orientation.AUTO_ROTATION_RESTRICTED);
```

### 关键要点

| 要点 | 说明 |
|---|---|
| **分屏/悬浮窗下旋转策略无效** | 系统级行为，无法通过 API 绕过 |
| **应通过响应式布局适配** | 使用断点系统 + `windowSizeChange` 监听 |
| **调用不会报错** | `setPreferredOrientation()` 静默失败，容易误以为生效 |

---

## 案例 4：视频全屏退出后方向未恢复

**场景标签**：视频播放 · 全屏 · 方向恢复 · Navigation · 页面跳转

### 问题描述

视频播放应用在首页使用竖屏，进入视频播放页后调用 `setPreferredOrientation(USER_ROTATION_LANDSCAPE)` 切换为横屏全屏。退出播放页返回首页后，屏幕方向仍停留在横屏，没有恢复为竖屏。

| | 说明 |
|---|---|
| **预期行为** | 退出视频页后恢复竖屏 |
| **实际行为** | 退出后仍为横屏 |

### 问题根因

`setPreferredOrientation()` 影响的是整个应用窗口，窗口将一直保持最后一次设置的方向，即使发生页面跳转也不会自动恢复。开发者只在进入视频页时设置了横屏，但退出时未调用恢复。

> 参考：setPreferredOrientation 方法调用的是窗口的显示方向，是整个应用窗口级别都发生了旋转，窗口将一直保持最后一次设置窗口方向的效果，即使发生页面跳转等行为窗口方向也不会发生变化。

### 解决方案

进入特定方向页面时保存当前方向，退出时（`aboutToDisappear`）恢复。

```typescript
import { window } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';

@Component
struct VideoPlayPage {
  private context = this.getUIContext()?.getHostContext() as common.UIAbilityContext;
  private windowClass = this.context.windowStage.getMainWindowSync();
  private lastOrientation: number = window.Orientation.PORTRAIT;

  aboutToAppear(): void {
    // 保存进入前的方向
    this.lastOrientation = this.windowClass.getPreferredOrientation();
    // 切换为横屏
    this.windowClass.setPreferredOrientation(window.Orientation.USER_ROTATION_LANDSCAPE);
  }

  aboutToDisappear(): void {
    // 退出时恢复之前保存的方向
    this.windowClass.setPreferredOrientation(this.lastOrientation);
  }
}
```

> 注意：如果使用 Navigation 组件进行页面导航，需要在每个需要特定方向的页面的 `onShown`/`onHidden` 中处理方向切换，因为 Navigation 页面切换时不会触发 `aboutToAppear`/`aboutToDisappear`（与 Tabs 的懒创建机制类似）。

### Navigation 场景的适配

```typescript
// Navigation 场景下使用 onShown / onHidden 替代 aboutToAppear / aboutToDisappear
NavDestination() {
  // 页面内容
}
.onShown(() => {
  this.lastOrientation = this.windowClass.getPreferredOrientation();
  this.windowClass.setPreferredOrientation(window.Orientation.USER_ROTATION_LANDSCAPE);
})
.onHidden(() => {
  this.windowClass.setPreferredOrientation(this.lastOrientation);
})
```

### 关键要点

| 要点 | 说明 |
|---|---|
| **进入时保存、退出时恢复** | 必须成对调用 `setPreferredOrientation()` |
| **窗口方向是全局状态** | 页面跳转不会自动恢复，需手动处理 |
| **Navigation 场景用 `onShown`/`onHidden`** | Navigation 页面不触发 `aboutToAppear`/`aboutToDisappear` |
| **Tabs 场景用 `onChange`** | 参考 [案例 2](#案例-2tabs--swiper-场景下短视频页方向锁定-bug) |

---

## 案例 5：折叠屏开合时布局异常闪烁

**场景标签**：折叠屏 · 开合连续 · 布局闪烁 · windowSizeChange · foldStatusChange

### 问题描述

折叠屏设备在折叠→展开（或展开→折叠）过程中，应用布局出现短暂的异常闪烁或内容跳变。例如列表滚动位置偏移、页面切换到其他页面、输入焦点丢失等。

| | 说明 |
|---|---|
| **预期行为** | 开合前后页面内容连续，无闪烁跳变 |
| **实际行为** | 开合瞬间布局抖动，焦点偏移 |

### 问题根因

折叠屏开合过程中，系统回调的触发时序如下：

- **展开态→折叠态**：`foldStatusChange`(悬停态) → `foldStatusChange`(折叠态) → `foldDisplayModeChange` → `windowSizeChange`
- **折叠态→展开态**：`foldStatusChange`(悬停态) → `foldDisplayModeChange` → `windowSizeChange` → `foldStatusChange`(展开态)

开发者在 `foldStatusChange` 回调中更新布局，但此时窗口尺寸还未变化，导致布局基于旧尺寸计算后又因 `windowSizeChange` 重新计算，产生两次布局刷新。

> 参考：应用页面和功能相关的开合连续能力建议使用断点实现，并通过 `window.on('windowSizeChange')` 接口监听。display 提供的折叠状态监听接口不建议用于页面布局的响应式适配，避免在窗口变化但折叠状态未改变的场景下布局未能及时调整。

### 解决方案

页面布局的响应式适配应通过 `windowSizeChange` + 断点实现，而非 `foldStatusChange`。

```typescript
// ✅ 正确：通过 windowSizeChange + 断点适配布局
private onWindowSizeChange: Callback<window.Size> = () => {
  const widthBp = this.getUIContext().getWindowWidthBreakpoint();
  const heightBp = this.getUIContext().getWindowHeightBreakpoint();
  // 根据断点更新布局（只触发一次）
};

// ❌ 错误：通过 foldStatusChange 更新布局（时序不对，导致二次刷新）
display.on('foldStatusChange', () => {
  this.updateLayout(); // 此时窗口尺寸可能还未更新
});
```

### 关键要点

| 要点 | 说明 |
|---|---|
| **布局适配用 `windowSizeChange`** | 而非 `foldStatusChange` |
| **折叠状态接口用于特殊功能** | 如悬停态适配、相机切换，不用于布局 |
| **开合时序有先后** | `foldStatusChange` 和 `windowSizeChange` 不在同一时机触发 |

> 来源：[折叠屏应用开发 - 适配应用界面开合连续](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-foldable-guide)

---

## 案例 6：显示大小缩放调大后应用被强制竖屏

**场景标签**：显示大小缩放 · px2vp · DPI · vp 阈值 · 直板手机

### 问题描述

用户在系统设置中将 **显示和亮度 → 显示大小缩放** 调到较大或最大值后，应用冷启动被强制锁定为竖屏，旋转手机只能在竖屏和反向竖屏之间切换，无法旋转到横屏。

| | 说明 |
|---|---|
| **预期行为** | 应用正常支持横竖屏自动旋转 |
| **实际行为** | 应用被强制竖屏，无法进入横屏 |

**受影响设备**：直板手机（Mate 60 Pro、Pura 70、Nova 等），min(vp) 接近 348 阈值的设备。折叠屏、平板不受影响（min(vp) 远大于阈值）。

### 问题根因

应用使用了官方最佳实践推荐的 vp 阈值判断逻辑，在 `onWindowStageCreate` 中根据窗口最小 vp 维度决定旋转策略：

```typescript
// 官方最佳实践推荐代码
let windowWidthVp = this.uiContext.px2vp(windowRect.width);
let windowHeightVp = this.uiContext.px2vp(windowRect.height);
let minDimVp = Math.min(windowWidthVp, windowHeightVp);

if (minDimVp > 348) {
  win.setPreferredOrientation(window.Orientation.AUTO_ROTATION_RESTRICTED);
} else {
  win.setPreferredOrientation(window.Orientation.PORTRAIT); // 强制竖屏
}
```

问题在于 `px2vp()` 的转换依赖 DPI：

```
vp = px / (DPI / 160)
```

当用户调大显示大小缩放时，系统 DPI 随之升高，导致同样的物理像素数转换为更少的 vp 值，使 min(vp) 跌破 348 阈值：

```
用户调大显示大小缩放
  → 系统DPI升高（如 Mate60 Pro: 480→630）
  → px2vp()转换比变大（同样物理像素 = 更少的vp）
  → 窗口最小维度 vp 值降低（如 min(vp): 390→320）
  → 低于348vp阈值
  → 触发强制竖屏分支
```

**关键数据**（Mate 60 Pro 真机）：

| 指标 | 默认缩放 | 最大缩放 |
|---|:---:|:---:|
| DPI | ~480 | **630** |
| 窗口尺寸(px) | 2720×1260 | 2720×1260（不变） |
| min(vp) | ~390 > 348 ✓ | **320 < 348** ✗ |
| 旋转策略 | AUTO_ROTATION（正常） | **强制竖屏** |

### 解决方案

使用物理像素（px）替代 vp 作为旋转判断阈值。物理像素不随系统显示大小缩放变化，判断结果稳定可靠。

```typescript
import { window, display } from '@kit.ArkUI';

// 物理像素阈值：手机短边通常 > 720px，远高于此阈值
const PX_THRESHOLD = 520;

updateOrientation(): void {
  let windowRect = this.windowObj!.getWindowProperties().windowRect;
  let minDimPx = Math.min(windowRect.width, windowRect.height);

  // 物理像素不受 DPI/显示缩放影响，判断稳定
  if (minDimPx > PX_THRESHOLD) {
    this.windowObj!.setPreferredOrientation(window.Orientation.AUTO_ROTATION_RESTRICTED);
  } else {
    this.windowObj!.setPreferredOrientation(window.Orientation.AUTO_ROTATION_PORTRAIT);
  }
}
```

**阈值选择依据**：手机短边物理像素通常 > 720px，远高于 520px 阈值（余量 38%+），即使极端 DPI 缩放也不会误判。穿戴设备短边 < 500px，命中强制竖屏分支。

### 其他可选方案

| 方案 | 描述 | 适用场景 |
|---|---|---|
| 固定旋转策略 | 直接在 `module.json5` 配置 `orientation: "auto_rotation_restricted"`，不动态判断 | 只需手机旋转的简单应用 |
| 断点检测 | 使用 `getWindowWidthBreakpoint()` / `getWindowHeightBreakpoint()` 替代 vp 阈值 | 已使用断点系统的应用 |
| **物理像素（推荐）** | **使用 px 替代 vp 阈值** | **需要区分设备形态的通用应用** |

### 关键要点

| 要点 | 说明 |
|---|---|
| **`px2vp()` 依赖 DPI** | 显示大小缩放改变 DPI 后，vp 值会随之变化，不适合用作稳定的设备形态判断 |
| **物理像素（px）不受显示缩放影响** | 窗口的 px 尺寸是硬件像素数，不随任何系统缩放设置改变 |
| **348vp 阈值余量过小** | 手机默认 min(vp) ≈ 390，仅比 348 多 12%，DPI 轻微升高即跌破 |
| **影响无障碍用户** | 调大显示大小的用户多为视力不佳群体，强制竖屏进一步损害体验 |

> 参考：[HarmonyOS 窗口方向最佳实践](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-multi-device-window-direction)

---

## 案例 7：XComponent 相机预览旋转后画面方向错乱与黑屏

**场景标签**：XComponent · SURFACE · 相机预览 · 旋转锁定 · SurfaceRect · windowSizeChange

### 问题描述

应用使用 `XComponent(SURFACE)` 实现后置摄像头预览，`module.json5` 配置 `orientation: "auto_rotation"`。竖屏启动时预览正常，旋转到横屏后出现两种异常：

| 异常类型 | 表现 | 出现时机 |
|---|---|---|
| **预览方向错乱** | 横屏预览画面相对屏幕顺时针旋转 90° | 旋转到横屏/反横屏时 |
| **旋转后黑屏** | 预览区域完全黑屏，无画面 | 第二次旋转回同一方向时 |

**可复现设备**：HOP 模拟器、Mate X5 真机等。部分设备（如 XTS 模拟器）因 HAL 层额外补偿不复现。

### 问题根因

根因涉及三个层面：**缺少 Surface 旋转锁定**、**未动态调整 Surface 渲染区域**、**旋转锁定的生命周期误解**。

#### 1. 未调用 `setXComponentSurfaceRotation({ lock: true })`

后置摄像头传感器物理安装角度统一为 90°，输出的原始图像相对设备自然方向是横向的。XComponent 的 Surface 在屏幕旋转时默认跟随旋转，但摄像头预览流的旋转角度不匹配，导致画面叠加了一个额外的 90° 旋转。

`setXComponentSurfaceRotation({ lock: true })` 可在旋转过渡期间锁定 Surface 方向，防止旋转动画期间画面错乱。**关键：该锁在每次旋转完成后会被系统自动释放**，必须在每次旋转后重新设置才能为下一次旋转提供保护。

#### 2. 未监听窗口尺寸变化并更新 SurfaceRect

旋转后窗口宽高互换，Surface 宽高比需要与当前屏幕方向匹配：

| 屏幕方向 | Surface 宽高比 | 说明 |
|---|---|---|
| 竖屏 (rotation 0°/180°) | 3:4 | 与预览流 4:3 互为倒数 |
| 横屏 (rotation 90°/270°) | 4:3 | 与预览流一致 |

不调用 `setXComponentSurfaceRect()` 调整渲染区域，旋转后 Surface 尺寸不变，画面被拉伸或出现黑屏。

#### 3. 旋转锁定仅调用一次导致后续旋转黑屏

`setXComponentSurfaceRotation({ lock: true })` 的锁在每次旋转完成后被系统自动释放。若仅在 `XComponent.onLoad` 中调用一次，第一次旋转受保护正常，但第二次旋转时锁已失效，Surface 跟随屏幕旋转导致方向不匹配，表现为黑屏。**必须在每次 `windowSizeChange` 回调中重新调用。**

#### 4. 页面组件中注册 windowSizeChange 监听不可靠

官方 MultiDeviceCamera 示例在 `EntryAbility.onWindowStageCreate` 中通过 `windowStage.getMainWindow()` 注册 `windowSizeChange` 监听。在页面组件中通过 `context.windowStage.getMainWindowSync()` 注册的监听，在不同设备上行为不一致——首次旋转正常，后续旋转事件丢失或回调中获取到的 display rotation 不准确。

### 解决方案

核心思路：**在 EntryAbility 注册窗口尺寸监听并通过 AppStorage 传递给页面；每次旋转后重新锁定 Surface 并更新渲染区域。**

#### 修改 1：EntryAbility 中注册 windowSizeChange

```typescript
// EntryAbility.ets
import { window } from '@kit.ArkUI';

export default class EntryAbility extends UIAbility {
  onWindowStageCreate(windowStage: window.WindowStage): void {
    // 在 Ability 层注册监听（官方推荐位置）
    windowStage.getMainWindow().then((win: window.Window) => {
      win.on('windowSizeChange', (data: window.Size) => {
        AppStorage.setOrCreate('windowSize', data);
      });
    });
    windowStage.loadContent('pages/Index', (err) => { /* ... */ });
  }
}
```

#### 修改 2：XComponent onLoad 中初始锁定

```typescript
XComponent({ type: XComponentType.SURFACE, controller: this.xComponentController })
  .onLoad(() => {
    this.surfaceId = this.xComponentController.getXComponentSurfaceId();
    this.xComponentController.setXComponentSurfaceRotation({ lock: true });
    this.requestPermissionAndStartCamera();
  })
```

#### 修改 3：页面通过 @StorageProp + @Watch 响应旋转，每次重新锁定

```typescript
@StorageProp('windowSize') @Watch('onWindowSizeChange') windowSize: window.Size = { width: 0, height: 0 };

onWindowSizeChange(): void {
  if (this.windowSize.width > 0 && this.windowSize.height > 0 && this.surfaceId !== '') {
    const displayRotation = display.getDefaultDisplaySync().rotation * 90;

    // 关键：每次旋转后必须重新锁定，系统会自动释放上一次的锁
    this.xComponentController.setXComponentSurfaceRotation({ lock: true });

    // 根据 display.rotation 计算 SurfaceRect（4:3 预览流为例）
    const w = this.windowSize.width;
    const h = this.windowSize.height;
    const rect: SurfaceRect = { surfaceWidth: w, surfaceHeight: h };

    if (displayRotation === 0 || displayRotation === 180) {
      // 竖屏：Surface 宽高比取 3:4
      if (h * 3 / 4 > w) {
        rect.surfaceHeight = w / 3 * 4;
      } else {
        rect.surfaceWidth = h / 4 * 3;
      }
    } else {
      // 横屏：Surface 宽高比取 4:3
      if (w * 3 / 4 > h) {
        rect.surfaceWidth = h / 3 * 4;
      } else {
        rect.surfaceHeight = w / 4 * 3;
      }
    }

    this.xComponentController.setXComponentSurfaceRect(rect);
  }
}
```

### 修复原理总结

| 修复点 | API | 调用时机 | 作用 |
|---|---|---|---|
| 锁定 Surface 旋转 | `setXComponentSurfaceRotation({ lock: true })` | onLoad + 每次旋转回调 | 防止旋转过渡期间 Surface 跟随旋转 |
| 调整渲染区域 | `setXComponentSurfaceRect(rect)` | 每次旋转回调 | 根据当前屏幕方向重新设置宽高比 |
| 窗口监听位置 | `windowStage.getMainWindow()` | EntryAbility.onWindowStageCreate | 确保监听可靠注册 |

**两个 API 缺一不可，且都必须在每次旋转后调用**：
- 仅锁定旋转不调整宽高比 → 旋转后画面拉伸
- 仅调整宽高比不锁定旋转 → 旋转过渡期间画面闪烁
- 锁定仅调用一次 → 第二次旋转失去保护，黑屏

### 验证方法

1. 竖屏启动应用，确认预览方向正确
2. 旋转到横屏，确认预览方向与屏幕一致
3. 旋转回竖屏，确认恢复正常
4. **再次旋转到横屏，确认不会黑屏**（验证锁定重新生效）
5. 旋转到反横屏，确认预览方向正确

### 关键要点

| 要点 | 说明 |
|---|---|
| **Surface 旋转锁每次自动释放** | `setXComponentSurfaceRotation({ lock: true })` 仅保护当次旋转，完成后自动释放，必须在每次旋转回调中重新调用 |
| **windowSizeChange 应在 EntryAbility 注册** | 页面组件中的注册在不同设备上行为不一致，首次正常但后续可能失效 |
| **两个 API 缺一不可** | `setXComponentSurfaceRotation` 管过渡期防闪烁，`setXComponentSurfaceRect` 管旋转后宽高比适配 |
| **Surface 宽高比随方向变化** | 竖屏时 3:4（预览流倒数），横屏时 4:3（预览流一致） |

> 参考：[多设备相机适配最佳实践](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-multi-device-camera)、[XComponent 组件参考](https://developer.huawei.com/consumer/cn/doc/harmonyos-references/ts-basic-components-xcomponent)

---

## 案例 8：折叠屏内屏竖屏下 Navigation Split 分栏布局拥挤

**场景标签**：折叠屏 · 竖屏 · Navigation · Split · 分栏 · 动态模式切换

### 问题描述

在折叠屏设备（如 Mate X5）展开态下，当用户将设备旋转至竖屏方向时，`Navigation` 组件的 `Split` 模式仍按宽度条件触发分栏——左侧导航栏与右侧内容区水平并排。但竖屏下垂直空间本就有限，再被水平 50/50 分割后，右侧内容区域的阅读空间严重不足，文本频繁换行，图片显示空间受限，整体体验拥挤。

| | 说明 |
|---|---|
| **预期行为** | 竖屏时自动切换为单栏（Stack）模式，充分利用全屏宽度展示内容 |
| **实际行为** | 竖屏时仍保持 Split 分栏，内容被压缩在 50% 宽度内 |

典型复现路径：折叠屏展开态 → 竖向持握 → 应用使用 `NavigationMode.Split` 或 `NavigationMode.Auto` → 界面左右分栏，右侧内容拥挤。

### 问题根因

`Navigation` 组件的 `Split` 模式（以及 `Auto` 模式下触发 Split 的条件）基于屏幕**宽度**判断——当宽度达到一定阈值即启用分栏。折叠屏内屏竖屏时，屏幕宽度依然较大（如 Mate X5 内屏展开态约 2204px），满足 Split 触发条件，但此时竖屏的**高度**才是限制因素，分栏导致本就有限的垂直空间被进一步压缩。

```typescript
// ❌ 问题代码：固定使用 Split 模式，不区分横竖屏
Navigation(this.pathStack) {
  // ...
}
.mode(NavigationMode.Split)
.navBarWidth('50%')
```

核心矛盾：Split 模式适合横屏（宽度充裕、高度充足），但折叠屏内屏竖屏的宽度虽大、垂直空间却不足以支撑分栏布局。

### 解决方案

根据窗口宽高比动态切换 Navigation 模式：横屏时使用 Split 分栏，竖屏/方屏时切换为 Stack 单栏。

**核心思路**：

1. 在 `EntryAbility` 中监听 `windowSizeChange`，通过宽高比判断方向并写入 `AppStorage`
2. 页面通过 `@StorageProp` 响应式读取方向状态
3. 根据方向动态设置 `Navigation.mode` 和 `navBarWidth`

**修改 1：EntryAbility 监听方向变化**

```typescript
// EntryAbility.ets
export default class EntryAbility extends UIAbility {
  private updateOrientation(size: window.Size): void {
    const isLandscape = size.width > size.height;
    AppStorage.setOrCreate('isLandscape', isLandscape);
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    // 允许应用随屏幕旋转
    windowStage.getMainWindow().then((win: window.Window) => {
      win.setPreferredOrientation(window.Orientation.AUTO_ROTATION);
    });

    windowStage.loadContent('pages/Index', () => {
      windowStage.getMainWindow().then((win: window.Window) => {
        // 初始获取方向
        const properties = win.getWindowProperties();
        this.updateOrientation(properties.windowRect);
        // 监听窗口尺寸变化，实时更新方向
        win.on('windowSizeChange', (size: window.Size) => {
          this.updateOrientation(size);
        });
      });
    });
  }
}
```

**修改 2：页面动态切换 Navigation 模式**

```typescript
// Index.ets
@Entry
@Component
struct Index {
  // 从 AppStorage 读取屏幕方向
  @StorageProp('isLandscape') isLandscape: boolean = false;
  private pathStack: NavPathStack = new NavPathStack();

  build() {
    Navigation(this.pathStack) {
      // 导航栏内容（分类标签 + 文章列表）
    }
    // 横屏 → Split 分栏；竖屏 → Stack 单栏
    .mode(this.isLandscape ? NavigationMode.Split : NavigationMode.Stack)
    .navBarWidth(this.isLandscape ? '40%' : '0')
    .navDestination(this.buildNavDestination)
    .onAppear(() => {
      // Split 模式下默认右侧显示详情
      if (this.isLandscape) {
        this.pathStack.pushPathByName('ArticleDetail', this.articleList[0], false);
      }
    })
  }
}
```

**修复前后对比：**

```
修复前：
  折叠屏内屏竖屏 → 宽度满足 Split 条件 → 固定分栏 → 内容拥挤

修复后：
  折叠屏内屏竖屏 → width < height → isLandscape=false → Stack 单栏 → 全屏宽度展示
  折叠屏内屏横屏 → width > height → isLandscape=true → Split 分栏 → 左右布局正常
```

### 关键要点

| 要点 | 说明 |
|---|---|
| **Split 模式仅基于宽度触发** | 折叠屏内屏竖屏宽度仍大，会误触分栏，需主动根据宽高比判断 |
| **方向状态应由 Ability 层统一管理** | 通过 `windowSizeChange` + `AppStorage` 确保方向状态全局一致且实时更新 |
| **`@StorageProp` 实现声明式响应** | 方向变化自动触发 UI 刷新，无需手动管理状态同步 |
| **`navBarWidth` 需同步调整** | Stack 模式下设为 `'0'`，Split 模式下设为合适比例（如 `'40%'`） |
| **Split 下需主动 push 初始详情页** | 分栏模式右侧默认为空，`onAppear` 中应 push 默认内容 |

---

## 案例 9：折叠屏外屏看直播切内屏后返回主页自动转竖屏

**场景标签**：折叠屏 · 直播 · 保存恢复方向 · 设备形态变化 · UNSPECIFIED

### 问题描述

折叠屏设备上，用户在外屏（折叠态）竖屏观看直播，展开手机切换到内屏（横屏）继续观看，点击返回按钮回到主页后，**屏幕被强制旋转为竖屏**，与用户当前持握方向不一致。

| 操作步骤 | 方向行为 | 说明 |
|---|---|---|
| 外屏（折叠态）进入直播 | 竖屏 | 正常 |
| 展开手机切到内屏 | 横屏 | `AUTO_ROTATION_UNSPECIFIED` 允许旋转，正常 |
| 点击返回主页 | **强制转竖屏** | 异常，应保持横屏 |

典型复现路径：折叠态外屏打开直播 → 展开手机至内屏横屏观看 → 点击返回 → 屏幕自动旋转为竖屏。

### 问题根因

开发者使用"保存→切换→恢复"模式管理窗口方向：进入直播页时通过 `display.getDefaultDisplaySync().rotation` 获取当前物理方向并保存，退出时恢复保存的方向。

```typescript
// ❌ 问题代码：保存进入时的方向快照，退出时恢复
aboutToAppear(): void {
  const rotation = display.getDefaultDisplaySync().rotation; // 外屏竖屏 → rotation=0
  if (rotation === 0 || rotation === 2) {
    this.lastOrientation = window.Orientation.PORTRAIT;  // 保存 PORTRAIT
  }
  this.windowObj.setPreferredOrientation(window.Orientation.AUTO_ROTATION_UNSPECIFIED);
}

aboutToDisappear(): void {
  // 设备可能已从折叠态展开为内屏（横屏），但恢复的仍是进入时的 PORTRAIT
  this.windowObj.setPreferredOrientation(this.lastOrientation); // 恢复 PORTRAIT → 强制竖屏
}
```

问题链路：

```
外屏进入直播 → display.rotation=0 → 保存 PORTRAIT
       ↓
展开到内屏 → AUTO_ROTATION_UNSPECIFIED 允许旋转 → 横屏（正常）
       ↓
点击返回 → aboutToDisappear 恢复 PORTRAIT → 在内屏横屏态强制竖屏 ❌
```

核心矛盾：**保存的是"进入时的方向快照"，恢复时设备形态可能已经变了**（折叠→展开，竖屏→横屏）。`setPreferredOrientation()` 设置的是窗口级全局状态，不会因页面跳转自动恢复，必须手动处理。而折叠屏开合会导致设备自然方向改变，恢复旧快照会与当前设备状态冲突。

### 解决方案

退出直播页时，不恢复进入时保存的固定方向，改为设置 `UNSPECIFIED`——让系统根据当前设备状态（折叠/展开、传感器方向）自适应决定方向。

```typescript
// ✅ 修复：退出时恢复 UNSPECIFIED，让系统自适应当前设备状态
aboutToDisappear(): void {
  if (this.windowObj) {
    this.windowObj.setPreferredOrientation(window.Orientation.UNSPECIFIED);
  }
}
```

修复前后对比：

| 场景 | 修复前 | 修复后 |
|---|---|---|
| 直板机竖屏进→竖屏出 | 恢复 PORTRAIT → 竖屏 ✅ | UNSPECIFIED → 系统保持竖屏 ✅ |
| 外屏竖屏进→外屏竖屏出 | 恢复 PORTRAIT → 竖屏 ✅ | UNSPECIFIED → 系统保持竖屏 ✅ |
| 外屏竖屏进→展开内屏横屏→返回 | 恢复 PORTRAIT → 强制竖屏 ❌ | UNSPECIFIED → 系统保持横屏 ✅ |

### 关键要点

| 要点 | 说明 |
|---|---|
| **不要在折叠屏场景下保存恢复固定方向** | 设备形态在页面活跃期间可能改变（折叠↔展开），保存的方向快照会过期 |
| **用 `UNSPECIFIED` 替代固定方向恢复** | 系统会根据当前设备状态和传感器自动选择合适方向 |
| **"保存→恢复"模式在直板机安全，在折叠屏危险** | 直板机设备形态不变，保存的方向始终有效；折叠屏设备形态可变，快照会过期 |
| **`setPreferredOrientation` 是窗口级状态** | 不因页面跳转自动恢复，退出页面时必须显式重置 |
