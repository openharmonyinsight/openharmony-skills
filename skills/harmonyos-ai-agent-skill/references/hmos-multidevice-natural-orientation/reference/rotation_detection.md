# 旋转检测指南


## 目录

1. [传感器概述](#传感器概述)
2. [基于重力传感器计算旋转角度](#基于重力传感器计算旋转角度)
3. [监听屏幕/窗口变化](#监听屏幕窗口变化)
4. [最佳实践](#最佳实践)

---

## 传感器概述

当需要获取**连续角度**而非离散四方向时，需要使用传感器。HarmonyOS 提供多种方向相关传感器：

| 传感器 | SensorId | 适用场景 |
|-------|---------|---------|
| 加速度传感器 | ACCELEROMETER | 屏幕旋转、摇一摇 |
| 重力传感器 | GRAVITY | 屏幕旋转（去除加速度干扰） |

> 注意: 通常推荐使用**窗口旋转策略**（`setPreferredOrientation`）实现自动旋转。仅当系统策略无法满足需求时（如需要精确角度做动画），才自定义传感器检测。

---

## 基于重力传感器计算旋转角度

### 获取设备握持角度

```arkts
import { sensor } from '@kit.SensorServiceKit';

queryDegree(): void {
  sensor.on(sensor.SensorId.GRAVITY, (data: sensor.GravityResponse) => {
    const degree = this.getCalDegree(data.x, data.y, data.z);
  });
}

getCalDegree(x: number, y: number, z: number): number {
  let degree: number = 0;
  // 有效角度变化阈值系数
  if ((x * x + y * y) * 3 < z * z) {
    return degree;
  }
  degree = 90 - Math.round(Math.atan2(y, -x) / Math.PI * 180);
  return degree >= 0 ? degree % 360 : degree % 360 + 360;
}
```


### 重要注意事项

- 通过 sensor 获取的是设备角度，**不能据此直接推断显示方向**，因为不同设备 0 度对应的显示方向不同。
- 只能监听到屏幕的显示方向，不能直接判断横竖握持方向。
- 如需推断，需要先记录 0 度时的设备方向，再根据旋转判断。

---

## 监听屏幕/窗口变化

### 方式一：display.on('change')（获取 rotation/orientation）

```arkts
import { display, Callback } from '@kit.ArkUI';

const changeCallback: Callback<number> = (displayId: number) => {
  const info = display.getDefaultDisplaySync();
  console.log(`rotation: ${info.rotation}, orientation: ${info.orientation}`);
};

// 注册监听
display.on('change', changeCallback);

// 取消监听（必须传入同一引用）
display.off('change', changeCallback);
```

> 重要: `display.on('change')` 回调中**不要通过 Window 实例获取宽高**（存在时序问题），应通过 Display 实例获取。

### 方式二：windowSizeChange（判断横竖屏）

```arkts
import { window, Callback } from '@kit.ArkUI';

// 在 @Component 中推荐使用 this.getUIContext().px2vp()
// 此处为独立代码片段示例，使用全局 px2vp()
const sizeCallback: Callback<window.Size> = (size: window.Size) => {
  const width = px2vp(size.width);
  const height = px2vp(size.height);
  const isLandscape = width > height;
};

windowClass.on('windowSizeChange', sizeCallback);
// 取消时: windowClass.off('windowSizeChange', sizeCallback);
```

> 注意: 窗口旋转 180° 时宽高不变，`windowSizeChange` 不会触发。需要结合 `display.on('change')` 监听。

### 方式三：媒体查询（仅判断横/竖）

```arkts
import { mediaquery } from '@kit.ArkUI';

const listener = this.getUIContext().getMediaQuery().matchMediaSync('(orientation: landscape)');
listener.on('change', (result: mediaquery.MediaQueryResult) => {
  const isLandscape = result.matches;
});
```

> 注意: 媒体查询只能判断横屏/竖屏，无法判断反向横屏/反向竖屏。

---

## 最佳实践

### 1. 优先使用窗口旋转策略而非传感器

```arkts
// ✅ 推荐：使用系统旋转策略
windowClass.setPreferredOrientation(window.Orientation.AUTO_ROTATION_RESTRICTED);

// ❌ 不推荐：手动通过传感器控制旋转（复杂且容易出错）
sensor.on(sensor.SensorId.GRAVITY, (data) => { /* 手动计算并旋转 */ });
```

### 2. 传感器数据需要防抖和平滑

```arkts
private lastUpdateTime: number = 0;
private readonly UPDATE_INTERVAL: number = 100; // ms

// 防抖
if (Date.now() - this.lastUpdateTime < this.UPDATE_INTERVAL) return;
this.lastUpdateTime = Date.now();

// 低通滤波平滑
private smoothedX: number = 0;
private smoothedY: number = 0;
private readonly ALPHA: number = 0.2;
smoothedX = ALPHA * x + (1 - ALPHA) * smoothedX;
```

### 3. 回调必须使用命名引用

```arkts
// ✅ 正确：保存引用，可正确取消
private callback = (data: sensor.GravityResponse) => { /* ... */ };
sensor.on(sensor.SensorId.GRAVITY, this.callback);
sensor.off(sensor.SensorId.GRAVITY, this.callback);

// ❌ 错误：匿名函数会导致内存泄漏
sensor.on(sensor.SensorId.GRAVITY, (data) => { /* ... */ });
```

---

## 调试方法

### 通过 hdc 命令获取屏幕旋转状态

```bash
# 查看当前屏幕属性（包含 rotation、orientation、width、height）
hdc shell hidumper -s DisplayManagerService

# 获取窗口信息（包含方向设置）
hdc shell hidumper -s WindowManagerService
```

### 通过 hdc 模拟屏幕旋转

UITest 框架提供 `setDisplayRotation` 命令模拟屏幕旋转：

```bash
# 屏幕顺时针旋转 90 度
hdc shell uitest uiInput keyEvent 2055  # KEYCODE_ROTATE_90

# 通过 ArkTS API（在测试用例中）
# await driver.setDisplayRotation(DisplayRotation.ROTATION_90);
```

### 日志过滤

```bash
# 过滤窗口旋转相关日志
hdc shell hilog | grep -i "rotation\|orientation\|windowSize"

# 过滤 display 变化回调
hdc shell hilog | grep -i "display.*change"
```

### 通过 hdc 截图验证

```bash
# 截取当前屏幕保存到设备
hdc shell uitest screenCap -p /data/local/tmp/rotation_test.png

# 拉取截图到本地
hdc file recv /data/local/tmp/rotation_test.png ./rotation_test.png
```

> 来源: [UI测试框架使用指导](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/uitest-guidelines)

---

## API 版本要求

方向适配涉及的关键 API 及其最低版本要求：

| API | 最低版本 | 说明 |
|-----|---------|------|
| `display.getDefaultDisplaySync()` | API 9 | 获取默认 Display 对象 |
| `display.isFoldable()` | API 10 | 判断是否可折叠设备 |
| `display.getFoldStatus()` | API 10 | 获取折叠状态 |
| `display.on('foldStatusChange')` | API 10 | 监听折叠状态变化 |
| `display.getCurrentFoldCreaseRegion()` | API 10 | 获取折痕区域 |
| `display.getFoldDisplayMode()` | API 10 | 获取折叠显示模式 |
| `window.setPreferredOrientation()` | API 9 | 设置窗口旋转策略 |
| `window.on('windowSizeChange')` | API 7 | 监听窗口尺寸变化 |
| `FOLLOW_DESKTOP` (Orientation) | API 12 | 跟随桌面旋转策略 |
| `USER_ROTATION_*` (Orientation) | API 12 | 临时方向类型 |
| `getWindowWidthBreakpoint()` | API 13 | 获取宽度断点 |
| `getWindowHeightBreakpoint()` | API 13 | 获取高度断点 |
| `FOLD_STATUS_EXPANDED_WITH_SECOND_EXPANDED` | API 15 | 三折叠双轴展开态 |

> 注意：使用 `FOLLOW_DESKTOP` 和 `USER_ROTATION_*` 系列策略需确保目标设备系统版本不低于 API 12。
