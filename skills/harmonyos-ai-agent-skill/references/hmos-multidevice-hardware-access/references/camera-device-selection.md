# 相机设备选择指南（官方基线）

## 目标

在多设备（手机、折叠屏、平板、2in1）环境下，正确选择相机设备并处理折叠状态变化导致的相机设备切换与重建。

## 官方 API

- `camera.getCameraManager(context)`：获取相机管理器。
- `cameraManager.getSupportedCameras()`：获取当前可用相机设备列表。
- `cameraManager.createCameraInput(device)`：创建相机输入。
- `cameraManager.on('foldStatusChange', callback)`：监听折叠状态变化（推荐，可同时获取可用相机列表）。
- `display.on('foldStatusChange', callback)`：监听折叠状态变化（方式二）。
- `FoldStatusInfo.supportedCameras`：折叠后当前可用的相机列表。

## 最小代码骨架

```typescript
import { camera } from '@kit.CameraKit';
import { display } from '@kit.ArkUI';

async function selectCamera(
  cameraManager: camera.CameraManager,
  isFront: boolean
): Promise<camera.CameraDevice> {
  const cameras = cameraManager.getSupportedCameras();
  const target = cameras.find(cam =>
    isFront
      ? cam.cameraPosition === camera.CameraPosition.CAMERA_POSITION_FRONT
      : cam.cameraPosition === camera.CameraPosition.CAMERA_POSITION_BACK
  );
  return target || cameras[0];
}
```

## 使用场景

| 场景 | 触发条件 | 推荐用法 | 为什么要判断 | 不判断的风险 |
| --- | --- | --- | --- | --- |
| 初始化相机 | 页面首次渲染 | `getSupportedCameras()` + `findIndex` | 确保选择到正确位置的相机。 | 使用默认相机可能不是用户期望的。 |
| 折叠状态变化 | 用户折展设备 | `cameraManager.on('foldStatusChange')` | 折叠后旧相机可能不可用。 | 预览黑屏、会话异常。 |
| 阔折叠外屏 | 切换到 PuraX 外屏 | `findIndex` 回退到 `cameras[0]` | 外屏仅有前置相机。 | 后置查找失败导致崩溃。 |
| 2in1 设备 | 平板/笔记本形态 | 检查后置是否存在 | 大部分仅有前置。 | 创建不存在的相机输入报错。 |
| 半折叠与展开切换 | 悬停态 ↔ 展开态 | 判断是否需要重建 | 设备变化不显著时可跳过。 | 不必要的重建导致闪烁。 |
| 热启动恢复 | 从后台切回前台 | `onPageShow` + `photoSession` 判断 | 相机会话可能已被系统回收。 | 黑屏。 |

## 约束

- 相机选择逻辑必须包含回退策略：目标位置不存在时回退到第一个可用相机。
- 折叠状态变化时的完整重建流程：释放旧会话 → 重新选择相机 → 创建 CameraInput → 创建 PreviewOutput → 创建 Session → commitConfig → start。
- XComponent 通过 `reloadXComponentFlag` 双实例切换实现重建。
- 半折叠 ↔ 展开之间可跳过重建（需在回调中判断）。

## 官方来源

- [折叠屏相机适配（官方）](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/camera-foldable-display)
