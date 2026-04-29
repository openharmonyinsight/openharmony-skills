# 相机旋转角度适配指南（官方基线）

## 目标

在预览、拍照、录像等不同场景下，正确适配相机旋转角度，确保图像在合适的方向显示。

来源：[华为开发者文档 - 相机旋转角度适配](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/camera-rotation)

## 官方 API

- `previewOutput.getPreviewRotation(displayRotation)`：获取预览旋转角度（需在 `commitConfig` 后调用）。
- `previewOutput.setPreviewRotation({ previewRotation, isDisplayLocked })`：设置预览旋转。
- `display.getDefaultDisplaySync().rotation`：获取屏幕旋转角度（枚举值 ×90° = 角度）。
- `sensor.on(sensor.SensorId.GRAVITY, callback)`：监听重力传感器。
- `sensor.once(sensor.SensorId.GRAVITY, callback)`：单次获取重力数据。
- `xComponentController.setXComponentSurfaceRect(...)`：设置 Surface 尺寸。
- `xComponentController.setXComponentSurfaceRotation({ lock })`：设置 Surface 旋转锁定。

## 预览旋转适配

### 最小代码骨架

```typescript
import { camera } from '@kit.CameraKit';
import { display } from '@kit.ArkUI';

function updatePreviewRotation(previewOutput: camera.PreviewOutput): void {
  const displayRotation = display.getDefaultDisplaySync().rotation * 90;
  const previewRotation = previewOutput.getPreviewRotation(displayRotation);
  previewOutput.setPreviewRotation({
    previewRotation: previewRotation,
    isDisplayLocked: false
  });
}
```

### Surface 宽高比计算

```typescript
function calculateSurfaceSize(
  rotation: number,
  previewWidth: number,
  previewHeight: number,
  containerWidth: number,
  containerHeight: number
): { width: number; height: number } {
  if (rotation === 0 || rotation === 180) {
    return {
      width: containerWidth,
      height: containerWidth * previewWidth / previewHeight
    };
  } else {
    return {
      width: containerHeight * previewHeight / previewWidth,
      height: containerHeight
    };
  }
}
```

## 拍照旋转适配

### 设备旋转角度计算

```typescript
import { sensor } from '@kit.SensorServiceKit';

const OVERLOOKING_GRAVITY_OF_Z_AXIS: number = 8.487;

function getCalDegree(x: number, y: number, z: number): number {
  if ((x * x + y * y) * 3 < z * z) {
    return 0;
  }
  let degree = 90 - Math.round(Math.atan2(y, -x) / Math.PI * 180);
  return degree >= 0 ? degree % 360 : degree % 360 + 360;
}

function getRotationForCapture(
  isFront: boolean,
  gravityData: sensor.GravityResponse,
  lastRotation: number
): number {
  if (Math.abs(gravityData.z) > OVERLOOKING_GRAVITY_OF_Z_AXIS) {
    return lastRotation;
  }
  const degree = getCalDegree(gravityData.x, gravityData.y, gravityData.z);
  if ((degree >= 0 && degree <= 30) || degree >= 300) {
    return camera.ImageRotation.ROTATION_0;
  } else if (degree > 30 && degree <= 120) {
    return isFront ? camera.ImageRotation.ROTATION_270 : camera.ImageRotation.ROTATION_90;
  } else if (degree > 120 && degree <= 210) {
    return camera.ImageRotation.ROTATION_180;
  } else {
    return isFront ? camera.ImageRotation.ROTATION_90 : camera.ImageRotation.ROTATION_270;
  }
}
```

## 使用场景

| 场景 | 触发条件 | 推荐用法 | 为什么要判断 | 不判断的风险 |
| --- | --- | --- | --- | --- |
| 预览旋转初始化 | 相机会话启动后 | `getPreviewRotation` + `setPreviewRotation` | 确保预览方向正确。 | 预览方向与设备持握方向不一致。 |
| 窗口旋转更新 | 设备旋转 | `onAreaChange` / `windowSizeChange` | 旋转后需重新计算。 | 旋转后预览拉伸。 |
| Surface 宽高比 | 预览启动/旋转变化 | 按 `display.rotation` 判断 | 0°/180° 和 90°/270° 规则不同。 | 画面压缩或拉伸。 |
| 拍照角度 | 用户点击拍照 | `sensor.once(GRAVITY)` + `capture(setting)` | 照片方向需与持握方向一致。 | 照片旋转 90°/180°/270°。 |
| 录像角度 | 开始录像 | `sensor.once(GRAVITY)` + `AVMetadata.videoOrientation` | 录像画面方向需正确。 | 录像画面方向错误。 |
| 自绘制预览 | ImageReceiver 二次处理 | 先旋转再镜像（前置） | 前置存在水平/垂直镜像差异。 | 前置预览方向异常。 |

## 约束

- `getPreviewRotation` 必须在 `commitConfig` 之后调用。
- `isDisplayLocked: false`（默认）表示跟随窗口变化；`true` 表示 Surface 旋转锁定。
- 拍照旋转角度：后置 `镜头安装角度(90°) + 重力方向`，前置 `镜头安装角度(270°) - 重力方向`。
- 录像 `AVMetadata.videoOrientation` 仅接受 0、90、180、270，非合理值 `prepare` 接口将报错。
- 自绘制场景前置摄像头：推荐"先旋转再镜像"，需考虑水平镜像和垂直镜像的区别。
- 术语统一：本文件中的"屏幕旋转角度"对应 `Display.rotation × 90°`；"预览旋转角度"通过 `getPreviewRotation()` 获取；"拍照旋转角度"通过重力传感器手动计算。详见 `camera-rotation-terms.md`。

## 验证清单

- 四方向预览（0°/90°/180°/270°）方向正确，无拉伸。
- 四方向拍照方向与设备持握方向一致。
- 录像画面方向与录像时持握方向一致。
- 窗口旋转后预览自动更新。
- 前后置相机切换后旋转角度正确。

## 官方来源

- [相机旋转角度适配（官方）](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/camera-rotation)
