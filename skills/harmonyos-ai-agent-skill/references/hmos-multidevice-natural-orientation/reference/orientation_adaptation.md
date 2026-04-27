# 多设备方向适配指南（一多）


## 目录

1. [一多方向适配核心思路](#一多方向适配核心思路)
2. [主流设备旋转能力一览](#主流设备旋转能力一览)
3. [348vp 旋转阈值与断点判断](#348vp-旋转阈值与断点判断)
4. [推荐旋转策略](#推荐旋转策略)
5. [module.json5 配置](#modulejson5-配置)
6. [运行时动态策略切换](#运行时动态策略切换)
7. [三折叠设备适配](#三折叠设备适配)
8. [常见方向适配问题](#常见方向适配问题)

---

## 一多方向适配核心思路

同一应用在不同形态设备上，旋转行为应有所差异：

- **直板机**：默认竖屏，仅特定页面（如视频播放）才需要横屏。
- **折叠屏折叠态**：等同于直板机。
- **折叠屏展开态**：类似平板，应支持自动旋转。
- **平板**：默认支持四方向自动旋转。
- **PC/2in1**：不支持旋转策略，窗口由用户自由调整。
- **三折叠 G 态**：自然方向为横屏，rotation=0 对应 LANDSCAPE_INVERTED。

### 适配方式选择

实际开发中有两种常见的多设备旋转适配方式。在 Bug 修复场景中，**优先尊重开发者原有的适配方式**，在其方案基础上修复问题，不要强制切换方案。开发者可能有定制的业务需求或历史兼容考虑。仅在从零开始适配或开发者主动要求重构时，才推荐采用更优方案。

**方式一：基于设备类型 + 折叠状态（修复场景中常见）**

通过 `deviceInfo.deviceType` 结合 `display.isFoldable()` 和 `display.getFoldStatus()` 判断。这是很多厂商实际使用的方案，逻辑直观、针对性强。修复问题时保持原有方式，只需补全遗漏的设备形态判断即可。

优先使用断点方案

```typescript
import { display } from '@kit.ArkUI';
import { deviceInfo } from '@kit.BasicServicesKit';

// 方式一示例：针对特定场景使用设备类型+折叠状态
function shouldLockPortrait(): boolean {
  const isPhone = deviceInfo.deviceType === 'phone';
  if (!isPhone) return false; // 非手机设备不强制竖屏
  const isFoldable = display.isFoldable();
  if (!isFoldable) return true; // 直板手机：强制竖屏
  const foldStatus = display.getFoldStatus();
  // 折叠屏展开态/悬停态不强制竖屏
  return foldStatus === display.FoldStatus.FOLD_STATUS_FOLDED;
}
```


**方式二：基于窗口尺寸断点（从零适配或重构时推荐）**

通过系统提供的 `WidthBreakpoint` / `HeightBreakpoint` 类型判断当前窗口形态。这种方式面向窗口而非设备，同一设备在不同窗口形态（全屏、分屏、自由窗口）下自动适配，设备种类增多时维护成本更低。

> 参考: [Code Linter 规则 `@cross-device-app-dev/one-multi-breakpoint-check`](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-one-multi-breakpoint-check) — 官方 lint 规则建议使用断点判断，而非 `deviceInfo.deviceType`。
>
> 注意: 折叠屏设备的 `deviceInfo.deviceType` 返回 `'phone'`，与直板机一致，因此通过 deviceType 无法区分折叠屏和直板机。

### 三层适配策略

无论选择哪种方式，推荐的分层策略为：

1. **默认策略**（module.json5）：配置 `follow_desktop`，让系统根据桌面行为决定应用默认方向
2. **全局动态调整**（EntryAbility）：监听 `windowSizeChange`，基于断点或设备状态动态切换 `AUTO_ROTATION_RESTRICTED` / `PORTRAIT`
3. **页面级覆盖**（特定页面）：进入视频全屏等页面时用 `USER_ROTATION_LANDSCAPE`，退出时恢复

---

## 主流设备旋转能力一览


| 产品类型 | 窗口全屏尺寸 (vp) | 最小边 > 348vp | 默认是否支持旋转 |
|---------|------------------|---------------|----------------|
| 直板机 (Mate60) | 374 × 827 | 是 | 否 |
| 阔折叠 (Pura X) 内屏 | 440 × 797 | 是 | 否 |
| 阔折叠 (Pura X) 外屏 | 326 × 326 | 否 | 否 |
| 双折叠 (Mate X5) 内屏 | 711 × 798 | 是 | 否 |
| 双折叠 (Mate X5) 外屏 | 345 × 801 | 否 | 否 |
| 三折叠 F 态 | 350 × 776 | 是 | 否 |
| 三折叠 M 态 | 712 × 776 | 是 | 否 |
| 三折叠 G 态 | 776 × 1107 | 是 | **是** |
| 平板 (MatePad Pro) | 711 × 1137 | 是 | **是** |
| PC/2in1 | — | — | 不支持旋转策略 |

---

## 348vp 旋转阈值与断点判断

### 348vp 参考阈值

官方推荐的旋转适配参考标准：窗口高度和宽度中的**较小值**大于 348vp 时，横竖屏旋转后通常有足够的显示区域。这不是强制限制，而是一个基础参考值 — 应用实际的旋转策略应根据自身需求决定。例如 Pura X 外屏（326×326）最小边虽不足 348vp，但如业务需要也可通过断点条件支持旋转。

### 基于断点动态设置旋转策略

使用系统提供的 `WidthBreakpoint` / `HeightBreakpoint` 枚举类型（而非字符串）判断断点：

```typescript
import { window } from '@kit.ArkUI';
import { UIAbility, AbilityConstant } from '@kit.AbilityKit';

export default class EntryAbility extends UIAbility {
  windowObj?: window.Window;
  uiContext?: UIContext;

  onWindowSizeChange: Callback<window.Size> = () => {
    this.setDefaultOrientation();
  };

  setDefaultOrientation(): void {
    const windowRect = this.windowObj!.getWindowProperties().windowRect;
    const windowWidthVp = this.uiContext!.px2vp(windowRect.width);
    const windowHeightVp = this.uiContext!.px2vp(windowRect.height);

    // 最小边 > 348vp: 支持旋转（受控制中心开关控制）
    if (Math.min(windowWidthVp, windowHeightVp) > 348) {
      this.windowObj?.setPreferredOrientation(window.Orientation.AUTO_ROTATION_RESTRICTED);
    } else {
      this.windowObj?.setPreferredOrientation(window.Orientation.PORTRAIT);
    }
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.getMainWindow().then((windowObj) => {
      this.windowObj = windowObj;
    });
    windowStage.loadContent('pages/Index', () => {
      this.uiContext = this.windowObj!.getUIContext();
      this.setDefaultOrientation();
      this.windowObj!.on('windowSizeChange', this.onWindowSizeChange);
    });
  }
}
```

### 结合横向 + 纵向断点的精细判断

当需要更精细的设备适配（如区分双折叠展开态、平板竖屏、手机横屏等），使用 `getWindowWidthBreakpoint()` 和 `getWindowHeightBreakpoint()` 获取系统断点类型：

```typescript
import { window } from '@kit.ArkUI';

// 使用系统断点类型（WidthBreakpoint / HeightBreakpoint），而非字符串
const widthBp: WidthBreakpoint = this.uiContext!.getWindowWidthBreakpoint();
const heightBp: HeightBreakpoint = this.uiContext!.getWindowHeightBreakpoint();

// 示例：双折叠展开态 + 平板竖屏 + 三折叠M/G态 支持旋转
// 手机竖屏(横sm,纵lg) → 不旋转；手机横屏(横md,纵sm) → 退出全屏时竖屏
if ((widthBp === WidthBreakpoint.WIDTH_MD && heightBp !== HeightBreakpoint.HEIGHT_SM) ||
  widthBp === WidthBreakpoint.WIDTH_LG) {
  // 大屏设备：自动旋转
  this.windowObj?.setPreferredOrientation(window.Orientation.AUTO_ROTATION_RESTRICTED);
} else if (widthBp === WidthBreakpoint.WIDTH_SM && heightBp === HeightBreakpoint.HEIGHT_LG) {
  // 手机竖屏：锁定竖屏（全屏播放时可切换为 AUTO_ROTATION_LANDSCAPE_RESTRICTED）
  this.windowObj?.setPreferredOrientation(window.Orientation.PORTRAIT);
}
```

断点类型对照：

| 类型 | 枚举值 | 含义 |
|------|-------|------|
| `WidthBreakpoint.WIDTH_SM` | sm | 窗口宽度 [320, 600) vp |
| `WidthBreakpoint.WIDTH_MD` | md | 窗口宽度 [600, 840) vp |
| `WidthBreakpoint.WIDTH_LG` | lg | 窗口宽度 [840, 1440) vp |
| `HeightBreakpoint.HEIGHT_SM` | sm | 高宽比 < 0.8（横向窗口） |
| `HeightBreakpoint.HEIGHT_MD` | md | 高宽比 [0.8, 1.2)（类方形窗口） |
| `HeightBreakpoint.HEIGHT_LG` | lg | 高宽比 ≥ 1.2（纵向窗口） |


---

## 推荐旋转策略

| 应用类型 | 推荐 module.json5 配置 | 说明 |
|---------|----------------------|------|
| 纯竖屏应用 | `portrait` | 大多数非视频类应用 |
| 纯横屏应用（游戏） | `landscape` | 横屏游戏 |
| 横屏游戏（支持反向横屏） | `auto_rotation_landscape` | 随握持方向旋转 |
| 可旋转应用 | `auto_rotation_restricted` | 受控制中心开关控制 |
| 一多应用（手机竖屏/平板可旋转） | `follow_desktop` | **推荐**：直板机桌面不可旋转=竖屏，平板桌面可旋转=跟随旋转 |

### `follow_desktop` 策略详解

`follow_desktop` 是一多场景的推荐策略：

| 设备形态 | 桌面行为 | 应用行为 |
|---------|---------|---------|
| 直板机 | 固定竖屏，不可旋转 | 竖屏，不可旋转 |
| 折叠屏折叠态 | 固定竖屏，不可旋转 | 竖屏，不可旋转 |
| 折叠屏展开态 | 可旋转 | 跟随旋转 |
| 平板 | 可旋转 | 跟随旋转 |
| PC/2in1 | 不支持旋转策略 | 不受影响 |

---

## module.json5 配置

```json
{
  "module": {
    "abilities": [
      {
        "name": "EntryAbility",
        "orientation": "follow_desktop"
      }
    ]
  }
}
```

常见 orientation 配置值与窗口 Orientation 枚举的对应关系：

| module.json5 值 | 窗口 Orientation |
|----------------|-----------------|
| `portrait` | PORTRAIT (1) |
| `landscape` | LANDSCAPE (2) |
| `auto_rotation` | AUTO_ROTATION (5) |
| `auto_rotation_restricted` | AUTO_ROTATION_RESTRICTED (8) |
| `auto_rotation_landscape` | AUTO_ROTATION_LANDSCAPE (7) |
| `follow_desktop` | FOLLOW_DESKTOP (17) |

---

## 运行时动态策略切换

### 不同页面不同旋转策略

```typescript
import { window } from '@kit.ArkUI';

@Component
struct LandscapePage {
  @StorageLink('mainWindow') mainWindow?: window.Window = undefined;
  private lastOrientation?: window.Orientation;

  aboutToAppear(): void {
    if (!this.mainWindow) return;
    // 保存当前方向
    this.lastOrientation = this.mainWindow.getPreferredOrientation();
    // 切换为横屏
    this.mainWindow.setPreferredOrientation(window.Orientation.USER_ROTATION_LANDSCAPE);
  }

  aboutToDisappear(): void {
    // 恢复之前的方向
    if (this.mainWindow && this.lastOrientation !== undefined) {
      this.mainWindow.setPreferredOrientation(this.lastOrientation);
    }
  }
}
```

### 通过窗口尺寸变化判断当前横竖屏

```typescript
import { window } from '@kit.ArkUI';

// 在 aboutToAppear 中注册（保存回调引用，确保可取消）
private sizeCallback: Callback<window.Size> | null = null;

this.sizeCallback = (size: window.Size) => {
  const uiContext = this.getUIContext();
  const width = uiContext.px2vp(size.width);
  const height = uiContext.px2vp(size.height);
  const isLandscape = width > height;
  // 根据横竖屏状态更新 UI
};
this.windowClass.on('windowSizeChange', this.sizeCallback);

// 在 aboutToDisappear 中取消
if (this.sizeCallback) {
  this.windowClass.off('windowSizeChange', this.sizeCallback);
  this.sizeCallback = null;
}
```

---

## 三折叠设备适配

### 折叠状态检测

```typescript
import { display } from '@kit.ArkUI';

function getTriFoldState(): 'F' | 'M' | 'G' | 'not_trifold' {
  if (!display.isFoldable()) return 'not_trifold';
  const foldStatus = display.getFoldStatus();
  // 双折轴展开态 = G 态
  if (foldStatus === display.FoldStatus.FOLD_STATUS_EXPANDED_WITH_SECOND_EXPANDED) {
    return 'G';
  }
  // 单轴展开态 = M 态
  if (foldStatus === display.FoldStatus.FOLD_STATUS_EXPANDED) {
    return 'M';
  }
  // 折叠态 = F 态
  return 'F';
}
```

### G 态方向特殊性

三折叠 G 态的自然方向是横屏，但 **rotation=0 对应 LANDSCAPE_INVERTED**（反向横屏）。

| rotation | G 态对应的屏幕方向 |
|----------|-----------------|
| 0 | LANDSCAPE_INVERTED |
| 1 | LANDSCAPE |
| 2 | PORTRAIT |
| 3 | PORTRAIT_INVERTED |

> 重要: 窗口的 orientation 和屏幕 rotation 并没有直接关联关系。在 rotation=0 的情况下，窗口的 orientation 可能是竖屏也可能是横屏（取决于设备和形态），不能通过 rotation 推断窗口方向。

### G 态旋转策略建议

G 态下应用默认支持旋转（桌面可旋转），使用 `follow_desktop` 策略即可自然适配，无需特殊处理。

---

## 常见方向适配问题

### 1. 折叠屏展开态被强制竖屏

**根因**: 用 `deviceInfo.deviceType === 'phone'` 判断后强制 `PORTRAIT`，但折叠屏的 deviceType 也是 `phone`。

**解法**: 增加折叠状态判断，展开态/悬停态不强制竖屏。详见 [case_example.md 案例 1](./case_example.md)。

### 2. display.on('change') 中获取窗口信息有延迟

**根因**: display 和 window 在不同进程，display 更新先于 window 更新完成。

**解法**: 在 `display.on('change')` 回调中通过 `display.getDefaultDisplaySync()` 获取屏幕信息，不要通过 Window 实例获取宽高。

### 3. 使用 `window.getLastWindow` 获取窗口有延迟

**根因**: `getLastWindow` 底层需要查找实例，有性能损耗。

**解法**: 使用 `windowStage.getMainWindowSync()` 同步方法获取窗口实例。

```typescript
const windowClass = context.windowStage.getMainWindowSync();
```

### 4. PC/2in1 上设置旋转策略不生效

**原因**: PC/2in1 不支持窗口旋转策略，调用 `setPreferredOrientation()` 不会报错但不生效。

**解法**: PC/2in1 场景不做旋转控制，通过响应式布局适配不同窗口尺寸。
