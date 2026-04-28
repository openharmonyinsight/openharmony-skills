# 折叠屏相机适配指南（官方基线）

## 目标

折叠屏设备在折叠状态变化时，可用的相机设备可能发生变化。应用必须监听折叠状态变化，在状态切换时重新选择相机设备并重建预览流。

来源：[华为开发者文档 - 折叠屏相机适配](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/camera-foldable-display)

## 官方 API

- `cameraManager.on('foldStatusChange', callback)`：监听折叠状态变化（推荐，回调包含 `FoldStatusInfo`）。
- `display.on('foldStatusChange', callback)`：监听折叠状态变化（方式二，回调仅包含 `FoldStatus`）。
- `display.on('foldDisplayModeChange', callback)`：监听显示模式变化。
- `FoldStatusInfo`：包含 `foldStatus`（当前折叠状态）和 `supportedCameras`（当前可用相机列表）。

## 折叠状态监听

```typescript
import { camera } from '@kit.CameraKit';
import { display } from '@kit.ArkUI';

private foldStatusCallback =
  (err: BusinessError, info: camera.FoldStatusInfo): void => {
    if (err !== undefined && err.code !== 0) {
      return;
    }
    AppStorage.setOrCreate<number>('foldStatus', info.foldStatus);
  };

onFoldStatusChange(): void {
  this.mCameraManager?.on('foldStatusChange', this.foldStatusCallback);
}

offFoldStatusChange(): void {
  this.mCameraManager?.off('foldStatusChange', this.foldStatusCallback);
}
```

## XComponent 重建

通过 `reloadXComponentFlag` 控制双实例切换实现重建：

```typescript
@StorageLink('foldStatus') @Watch('reloadXComponent') foldStatus: number = 0;
private reloadXComponentFlag: boolean = false;

reloadXComponent(): void {
  this.reloadXComponentFlag = !this.reloadXComponentFlag;
}

build() {
  Stack() {
    if (this.reloadXComponentFlag) {
      XComponent(this.mXComponentOptions)
        .onLoad(async () => { await this.loadXComponent(); })
    } else {
      XComponent(this.mXComponentOptions)
        .onLoad(async () => { await this.loadXComponent(); })
    }
  }
}
```

## 使用场景

| 场景 | 触发条件 | 推荐用法 | 为什么要判断 | 不判断的风险 |
| --- | --- | --- | --- | --- |
| 折叠态相机重建 | 用户折展设备 | `foldStatusChange` + 完整重建链路 | 折叠后旧相机可能不可用。 | 黑屏。 |
| 半折叠过滤 | 悬停态 ↔ 展开态 | 判断两个状态间跳过重建 | 设备变化不显著。 | 不必要重建导致闪烁。 |
| 阔折叠外屏 | PuraX 外屏仅有前置 | `findIndex` + 回退策略 | 后置不存在。 | 查找失败崩溃。 |
| 预览分辨率适配 | 折叠后屏幕比例变化 | 按新比例选择 PreviewProfile | 不同折叠态屏幕比例不同。 | 画面拉伸。 |

## 半折叠态（悬停态）处理策略

> 半折叠态是折叠/展开过程中的过渡状态。即使用户不想进入悬停态，在折叠/展开过程中也会触发 `FOLD_STATUS_HALF_FOLDED`。

**默认策略**：在 `foldStatusChange` 回调中，半折叠 ↔ 展开/折叠之间的状态转换应跳过相机重建。原因：
1. 半折叠态是过渡态，设备变化不显著，相机设备通常仍然可用。
2. 跳过重建可避免不必要的闪烁和性能开销。

**仅在以下情况处理半折叠态**：应用明确需要悬停态相机页面适配（HW-02-hover），此时才在半折叠态回调中执行布局调整和旋转策略更新，但仍跳过相机设备重建。

```typescript
display.on('foldStatusChange', (foldStatus: display.FoldStatus) => {
  if ((this.preFoldStatus === display.FoldStatus.FOLD_STATUS_HALF_FOLDED &&
    foldStatus === display.FoldStatus.FOLD_STATUS_EXPANDED) ||
    (this.preFoldStatus === display.FoldStatus.FOLD_STATUS_EXPANDED &&
      foldStatus === display.FoldStatus.FOLD_STATUS_HALF_FOLDED)) {
    this.preFoldStatus = foldStatus;
    return;
  }
  this.preFoldStatus = foldStatus;
  AppStorage.setOrCreate<number>('foldStatus', foldStatus);
});
```

## 约束

- 折叠状态变化的完整重建流程：释放旧会话 → 重新选择相机 → 创建 CameraInput → 创建 PreviewOutput → 创建 Session → commitConfig → start。
- 半折叠态是过渡状态，默认应忽略（跳过重建）；仅在 HW-02-hover 场景下处理悬停态布局调整。
- 所有监听注册必须与对应 `off` 成对出现，页面离场时统一清理。

## 验证清单

- 折叠 → 展开：预览正常无黑屏。
- 展开 → 折叠：预览正常无黑屏。
- 半折叠 ↔ 展开：布局和旋转正确（可跳过重建）。
- PuraX 外屏：后置相机不可用时自动回退前置。
- 页面退出后监听已回收。

## 官方来源

- [折叠屏相机适配（官方）](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/camera-foldable-display)
