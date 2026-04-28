# 沉浸式布局完全指南

## 目录

1. [沉浸式布局概述](#沉浸式布局概述)
2. [实现方案对比](#实现方案对比)
3. [方案一: 状态栏透明 + expandSafeArea 延伸背景](#方案一-状态栏透明--expandsafearea-延伸背景)
4. [方案二: 全屏布局 + padding](#方案二-全屏布局--padding)
5. [常见问题](#常见问题)
6. [最佳实践](#最佳实践)
   - [场景1：列表页滚动沉浸浏览](#场景1列表页滚动沉浸浏览上滑隐藏下滑恢复标题栏与底部导航栏)

---

## 沉浸式布局概述

沉浸式布局是指应用内容延伸到屏幕边缘，提供全屏沉浸的视觉体验。

### 沉浸式布局特点

- 背景延伸到状态栏、导航栏区域
- 重要内容保持在安全区域内
- 提供更沉浸的视觉体验

### 适用场景

- 视频播放
- 图片浏览
- 游戏
- 阅读应用

---

## 实现方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|-----|------|------|-------|
| padding + getWindowAvoidArea | 兼容性好 | 需要手动计算 | ⭐⭐⭐⭐⭐|
| expandSafeArea | 代码简洁，系统自动处理 | 需要API支持 | ⭐⭐⭐⭐ |

---

## 方案一: 状态栏透明 + expandSafeArea 延伸背景

> **适用场景：** 背景色或图片需要铺满状态栏和导航栏区域，但页面内容（标题栏、操作栏等）保持在安全区内。
> 此方案不需要动态获取避让区域高度，仅通过 expandSafeArea 实现背景延伸。

### EntryAbility 设置系统栏透明

```typescript
// EntryAbility.ets
import window from '@ohos.window';

export default class EntryAbility extends UIAbility {
  onWindowStageCreate(windowStage: window.WindowStage): void {
     windowStage.getMainWindow((err: BusinessError, win:window.Window) => {
      if (err.code) {
        console.error(`Failed to obtain main window. Code: ${err.code}, Message: ${err.message}`);
        return;
      }
      win.setWindowSystemBarProperties({
        statusBarColor: '#00000000',
        navigationBarColor: '#00000000',
        isStatusBarLightIcon: false,
        isNavigationBarLightIcon: false
      }).catch(() => {
        // TODO: Implement error handling.
      });
    });

    windowStage.loadContent('pages/Index');
  }
}
```

### 页面中使用 expandSafeArea 延伸背景

详见 [safe_area_api.md — 背景色延伸](./safe_area_api.md#背景色延伸) 和 [图片延伸](./safe_area_api.md#图片延伸)

---

## 方案二: 全屏布局 + padding

> **前提：** 需要先在 EntryAbility 中调用 `mainWindow.setWindowLayoutFullScreen(true)` 开启全屏布局，否则 `getWindowAvoidArea` 返回的系统栏高度可能与实际不一致。

### 获取避让区域高度

```typescript
// AvoidAreaManager.ets
import window from '@ohos.window';

export class AvoidAreaManager {
  private static instance: AvoidAreaManager;
  private windowClass?: window.Window;
  private statusBarHeight: number = 0;
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
    if (!this.windowClass) {
      return;
    }
    try {
      const systemArea = this.windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
      const navigationArea = this.windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);

      if (systemArea) {
        this.statusBarHeight = this.windowClass.getUIContext().px2vp(systemArea.topRect.height);
      }
      if (navigationArea) {
        this.navigationBarHeight = this.windowClass.getUIContext().px2vp(navigationArea.bottomRect.height);
      }

      AppStorage.setOrCreate('statusBarHeight', this.statusBarHeight);
      AppStorage.setOrCreate('navigationBarHeight', this.navigationBarHeight);
    } catch (e) {
      // TODO: Implement error handling.
    }
  }
}
```

### 页面使用

```typescript
import { AvoidAreaManager } from '../managers/AvoidAreaManager';
import common from '@ohos.app.ability.common';

@Entry
@Component
struct ImmersivePaddingPage {
  @StorageProp('statusBarHeight') statusBarHeight: number = 0;
  @StorageProp('navigationBarHeight') navigationBarHeight: number = 0;

  async aboutToAppear() {
    const context = this.getUIContext().getHostContext() as common.UIAbilityContext;
    await AvoidAreaManager.getInstance().init(context);
  }

  build() {
    Column() {
      // 标题栏 - 添加状态栏高度的 padding
      Row() {
        Text('标题')
      }
      .width('100%')
      .height(56)
      .padding({ top: this.statusBarHeight })

      // 内容区域
      List() {
        // 列表内容
      }
      .layoutWeight(1)

      // 底部操作栏 - 添加导航栏高度的 padding
      Row() {
        Button('操作')
      }
      .width('100%')
      .height(56)
      .padding({ bottom: this.navigationBarHeight })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#007AFF')
  }
}
```

> **完整示例：** [FullScreenLayoutExample.ets](../assets/FullScreenLayoutExample.ets) — 在页面 `aboutToAppear` 中调用 `setWindowLayoutFullScreen(true)` 并动态获取状态栏、导航栏高度设置 padding 的完整页面实现。

---

> **开发场景方案**：列表页滚动沉浸浏览等完整开发场景方案，请参阅 [scenario-development-cases.md](./scenario-development-cases.md)。

---

## 常见问题

### Q: 全屏后内容被状态栏遮挡？
使用方案二的 `getWindowAvoidArea` 动态获取状态栏高度，并设置顶部 padding。

### Q: expandSafeArea 设置了但背景没有延伸？
确保组件设置了 `backgroundColor` 或背景图，且父容器没有限制尺寸。

### Q: padding 应该加在外层容器还是标题栏容器上？
如果标题栏有独立背景色，padding 应加在标题栏容器上，避免出现色差间隙（详见最佳实践场景2）。

---