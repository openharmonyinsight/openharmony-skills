# 避让区域类型完全指南

## 目录

1. [避让区域概述](#避让区域概述)
2. [API 参考](#api-参考)
3. [基本用法](#基本用法)
4. [各区域说明](#各区域说明)
5. [常见问题](#常见问题)

---

## 避让区域概述

避让区域 (Avoid Area) 是指应用不应放置重要内容的屏幕区域，这些区域通常被系统 UI 占用。安全区域 (Safe Area) 是除去避让区域后的可用区域。

HarmonyOS 提供四种避让区域类型：系统状态栏 (`TYPE_SYSTEM`)、导航栏 (`TYPE_NAVIGATION_INDICATOR`)、挖孔区 (`TYPE_CUTOUT`) 和软键盘 (`TYPE_KEYBOARD`)，详见下方 [API 参考](#api-参考) 和 [各区域说明](#各区域说明)。

---

## API 参考

> 以下为 `window` 模块中避让区相关的核心系统类型

### window.AvoidAreaType

| 枚举值 | 说明 |
|--------|------|
| `TYPE_SYSTEM` | 系统状态栏区域 |
| `TYPE_NAVIGATION_INDICATOR` | 底部导航指示条区域 |
| `TYPE_CUTOUT` | 挖孔/刘海区域 |
| `TYPE_KEYBOARD` | 软键盘区域 |

### window.AvoidArea

`getWindowAvoidArea` 的返回类型：

| 字段 | 类型 | 说明 |
|------|------|------|
| topRect | `window.Rect` | 顶部避让区域（px） |
| bottomRect | `window.Rect` | 底部避让区域（px） |
| leftRect | `window.Rect` | 左侧避让区域（px） |
| rightRect | `window.Rect` | 右侧避让区域（px） |
| visible | `boolean` | 该避让区域是否可见 |

### window.AvoidAreaOptions

`avoidAreaChange` 回调的参数类型：

| 字段 | 类型 | 说明 |
|------|------|------|
| type | `window.AvoidAreaType` | 触发变化的避让区域类型 |
| area | `window.AvoidArea` | 变化后的避让区域信息 |

### window.Rect

矩形区域（所有数值单位为 px，使用时需 `px2vp` 转换）：

| 字段 | 类型 | 说明 |
|------|------|------|
| left | `number` | 左边界（px） |
| top | `number` | 上边界（px） |
| width | `number` | 宽度（px） |
| height | `number` | 高度（px） |

---

## 基本用法

### 获取避让区域

> **完整示例：** [getAvoidAreas.ets](../assets/getAvoidAreas.ets) — 在组件中获取状态栏、导航栏、挖孔区和键盘区域高度的完整实现。

```typescript
import window from '@ohos.window';

async function getAvoidAreas(context: Context) {
  const windowClass = await window.getLastWindow(context);

  const systemArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_SYSTEM);
  console.info(`状态栏高度: ${px2vp(systemArea.topRect.height)}vp`);

  const navigationArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR);
  console.info(`导航栏高度: ${px2vp(navigationArea.bottomRect.height)}vp`);

  const cutoutArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_CUTOUT);
  console.info(`挖孔区: ${JSON.stringify(cutoutArea.topRect)}`);

  const keyboardArea = windowClass.getWindowAvoidArea(window.AvoidAreaType.TYPE_KEYBOARD);
  console.info(`键盘高度: ${px2vp(keyboardArea.bottomRect.height)}vp`);
}
```

### 监听避让区域变化

> **完整示例：** [AvoidAreaExample.ets](../assets/AvoidAreaExample.ets) — 在组件中监听 avoidAreaChange 并动态更新状态栏和导航栏高度、响应式更新 UI 的完整实现。

```typescript
import window from '@ohos.window';

async function listenAvoidAreaChange(context: Context) {
  const windowClass = await window.getLastWindow(context);

  windowClass.on('avoidAreaChange', (data: window.AvoidAreaOptions) => {
    switch (data.type) {
      case window.AvoidAreaType.TYPE_SYSTEM:
        console.log('状态栏区域变化');
        break;
      case window.AvoidAreaType.TYPE_NAVIGATION_INDICATOR:
        console.log('导航栏区域变化');
        break;
      case window.AvoidAreaType.TYPE_CUTOUT:
        console.log('挖孔区域变化');
        break;
      case window.AvoidAreaType.TYPE_KEYBOARD:
        console.log('键盘区域变化');
        break;
    }
  });
}
```

**注意事项：**
- 所有返回值的单位为 px，需使用 `px2vp()` 转换
- 在 `aboutToDisappear()` 中调用 `windowClass.off('avoidAreaChange')` 取消监听
- 折叠屏展开/折叠、横竖屏切换会触发避让区域变化

---

## 各区域说明

### 系统状态栏

**位置：** 屏幕顶部，显示时间、电量、信号、通知图标等。

**避让要点：**
- 通过 `TYPE_SYSTEM` 获取，高度因设备和系统栏配置不同而有差异
- 通常使用顶部 padding 避让：`.padding({ top: statusBarHeight })`
- 折叠屏展开/折叠、横竖屏切换时高度可能变化，需监听 `avoidAreaChange`

### 导航栏

**位置：** 屏幕底部，用于手势导航或虚拟按键。

**避让要点：**
- 通过 `TYPE_NAVIGATION_INDICATOR` 获取
- 通常使用底部 padding 避让：`.padding({ bottom: navigationBarHeight })`
- 手势导航和虚拟按键导航的导航栏高度不同

### 挖孔区/刘海

**位置：** 前置摄像头、传感器等占据的屏幕区域。形状可能是矩形、圆形、药丸形。

**避让要点：**
- 通过 `TYPE_CUTOUT` 获取
- 不同设备挖孔位置和尺寸不同，必须动态获取，不能硬编码
- 横竖屏切换时挖孔位置会旋转（竖屏顶部 → 横屏侧边），必须监听 `avoidAreaChange`

#### 常见挖孔类型

| 类型 | 说明 | 示例设备 |
|-----|------|---------|
| 居中单孔 | 顶部中央圆形挖孔 | 多数手机 |
| 左侧单孔 | 顶部左侧圆形挖孔 | 部分手机 |
| 药丸形 | 顶部药丸形挖孔 | 部分手机 |
| 刘海 | 顶部矩形区域 | 旧款设备 |

#### 使用 expandSafeArea 避让挖孔区

当背景色或图片需要延伸到挖孔区域时，可使用 `expandSafeArea`：

```typescript
Column() {
  // 内容
}
.width('100%')
.height('100%')
.backgroundColor('#FF9500')
.expandSafeArea([SafeAreaType.CUTOUT], [SafeAreaEdge.TOP])
```

> 如果需要精确控制内容避开挖孔区（如游戏、全屏应用），推荐使用下方四方向检测方案。

#### 四方向挖孔避让

某些设备可能在四个角落都有挖孔，需要四方向检测。以下为核心逻辑：

> `px2vp` 为全局函数；`screenWidth` / `screenHeight` 需通过 `display.getDefaultDisplaySync().width / height` 获取或从组件中传入。

```typescript
interface CutoutPadding {
  top?: number;
  bottom?: number;
  left?: number;
  right?: number;
}

private updateAvoidPadding(area: window.AvoidArea): CutoutPadding {
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

  return padding;
}
```

> **替代方案示例：** [CutoutAvoidanceExample.ets](../assets/CutoutAvoidanceExample.ets) — 通过 `display.getCutoutInfo()` API 获取挖孔矩形数组并计算顶部避让距离的完整页面实现。

> **完整示例：** [CutoutAvoidance4DirExample.ets](../assets/CutoutAvoidance4DirExample.ets) — 在页面组件中获取四方向挖孔区域并动态设置 padding 的完整实现。

> **完整实现：** [CutoutAvoidanceManager.ets](../assets/CutoutAvoidanceManager.ets) — 单例管理器，封装了四方向挖孔检测、avoidAreaChange 监听、listener 回调模式、全屏/系统栏控制及 destroy 清理的完整实现，可直接集成到项目中使用。

### 软键盘

**位置：** 输入法弹出时占据的屏幕底部区域，动态显示/隐藏。

**避让要点：**
- 通过 `TYPE_KEYBOARD` 获取，高度随输入法不同而变化
- 详细的键盘避让方案请参阅 [keyboard_handling.md](./keyboard_handling.md)

---

## 常见问题

### Q: 为什么获取到的避让区域高度为 0？
确保在页面 `aboutToAppear` 之后调用 `getWindowAvoidArea`，且窗口已完成创建。

### Q: 折叠屏展开/折叠后避让区域没有更新？
需要监听 `avoidAreaChange` 事件，在回调中重新获取避让区域高度。

### Q: 如何选择 padding、margin、offset 还是 expandSafeArea？
- `expandSafeArea`：背景/图片延伸到系统区域，系统自动处理
- `padding`/`margin`/`offset`：需要精确控制内容位置，手动计算避让距离

---
