# 相机问题修复场景库（通用）

## 目的

统一沉淀相机相关问题修复方法，所有修复场景使用同一结构输出：
- 问题描述
- 根因分析
- 通用修复方案

本文件只保留通用方案，不绑定特定页面、业务或产品案例。

## 使用方式

1. 先识别问题类型，定位到对应场景。
2. 按"问题描述 -> 根因分析 -> 通用修复方案"执行。
3. 修复后按统一验证矩阵回归。

## 场景 A：折叠态切换后黑屏

### 问题描述

- 折叠屏设备在折叠/展开切换后，相机预览页面出现黑屏。
- 页面可见但 XComponent 无画面输出。

### 根因分析

- 折叠前选择的相机设备在折叠后不再可用（如外屏仅有前置相机）。
- 未监听 `foldStatusChange` 事件，或监听后未完整重建相机会话。
- 半折叠与展开之间的切换可能不需要重建相机，但未做过滤导致不必要的重建失败。

### 反例：未监听折叠状态变化

> 来源：`BlackScreen.ets`

```typescript
aboutToAppear(): void {
  this.requestCameraPermission();
  this.setupRotationListener();
  this.getCurrentFoldStatus();
}

setupFoldStatusListener(): void {
  display.on('foldStatusChange', (foldStatus: display.FoldStatus) => {
    this.currentFoldStatus = foldStatus;
    this.handleFoldStatusChange();
  });
}
```

**问题点**：`aboutToAppear` 中调用了 `setupRotationListener` 但未调用 `setupFoldStatusListener`，折叠状态变化后无法感知和响应。

### 反例：热启动未恢复相机

> 来源：`BlackScreen.ets`

```typescript
aboutToAppear(): void {
  this.requestCameraPermission();
  this.setupFoldStatusListener();
  this.setupRotationListener();
  this.getCurrentFoldStatus();
}
```

**问题点**：缺少 `onPageShow` 生命周期回调，页面热启动（从后台恢复）时不会重新初始化相机，导致黑屏。

### 正例：完整生命周期管理

> 来源：`CameraPhoto.ets`（GoodCase）

```typescript
onPageShow(): void {
  if (this.photoSession) {
    this.initCamera();
  }
}

aboutToAppear(): void {
  this.requestCameraPermission();
  this.setupFoldStatusListener();
  this.setupRotationListener();
  this.getCurrentFoldStatus();
}

aboutToDisappear(): void {
  display.off('foldStatusChange');
  display.off('change');
  this.releaseCamera();
}
```

### 通用修复方案

- 在 `aboutToAppear` 中注册 `foldStatusChange` 监听。
- 在 `onPageShow` 中判断 `photoSession` 是否存在，若存在则重新初始化相机（覆盖热启动场景）。
- 折叠状态变化时完整执行：释放旧会话 → 重新选择相机 → 创建 CameraInput → 创建 PreviewOutput → 创建 Session → commitConfig → start。
- 半折叠 ↔ 展开之间的切换可跳过重建（设备变化不显著时）。

## 场景 B：开合后相机设备未切换

### 问题描述

- 折叠屏折叠/展开后，相机仍使用旧设备（如外屏仍在使用后置相机）。
- 阔折叠外屏（如 PuraX）仅有前置相机，切换到外屏后后置相机查找失败。

### 根因分析

- 监听了 `foldStatusChange`，但回调中仅重新选择预览分辨率，未重新选择相机设备。
- 相机选择逻辑未考虑目标位置相机不存在的情况，缺少回退策略。

### 反例：仅更新预览流未重建相机设备

> 来源：`CameraNoSwitch.ets`

```typescript
async reinitCameraForFoldChange(): Promise<void> {
  if (this.cameraManager && this.cameraInput) {
    const cameras = this.cameraManager.getSupportedCameras();
    const currentCamera = cameras.find(cam => cam.cameraPosition === this.cameraPosition) || cameras[0];

    const cameraOutputCapability = this.cameraManager.getSupportedOutputCapability(
      currentCamera, camera.SceneMode.NORMAL_PHOTO
    );

    const newPreviewProfile = this.selectPreviewProfileForFold(
      cameraOutputCapability.previewProfiles, this.displayRatio
    );

    if (newPreviewProfile && this.previewOutput) {
      this.photoSession?.beginConfig();
      this.photoSession?.removeOutput(this.previewOutput);
      this.previewOutput = this.cameraManager.createPreviewOutput(newPreviewProfile, this.surfaceId);
      this.photoSession?.addOutput(this.previewOutput);
      await this.photoSession?.commitConfig();
      await this.photoSession?.start();
      this.updateSurfaceSize();
    }
  }
}
```

**问题点**：折叠状态变化后仅更新了 PreviewOutput，未释放旧的 CameraInput 和 Session 并重新选择相机设备。当折叠前的相机不再可用时，`getSupportedCameras()` 返回的列表中可能不包含旧相机。

### 正例：完整重建相机链路

> 来源：`CameraPhoto.ets`（GoodCase）

```typescript
async initCamera(): Promise<void> {
  await this.releaseCamera();

  this.cameraManager = camera.getCameraManager(this.context);
  const cameras: Array<camera.CameraDevice> = this.cameraManager.getSupportedCameras();

  let targetCamera: camera.CameraDevice | undefined = undefined;
  for (const cam of cameras) {
    if (cam.cameraPosition === this.cameraPosition) {
      targetCamera = cam;
      break;
    }
  }
  if (!targetCamera) {
    targetCamera = cameras[0];
  }

  this.cameraInput = this.cameraManager.createCameraInput(targetCamera);
  await this.cameraInput.open();

  const cameraOutputCapability = this.cameraManager.getSupportedOutputCapability(
    targetCamera, camera.SceneMode.NORMAL_PHOTO
  );

  const previewProfile = this.selectPreviewProfileForFold(
    cameraOutputCapability.previewProfiles, this.displayRatio
  );
  this.previewWidth = previewProfile.size.width;
  this.previewHeight = previewProfile.size.height;

  this.previewOutput = this.cameraManager.createPreviewOutput(previewProfile, this.surfaceId);

  this.photoSession = this.cameraManager.createSession<camera.PhotoSession>(camera.SceneMode.NORMAL_PHOTO);
  this.photoSession.beginConfig();
  this.photoSession.addInput(this.cameraInput);
  this.photoSession.addOutput(this.previewOutput);
  await this.photoSession.commitConfig();
  await this.photoSession.start();
  this.updateSurfaceSize();
}
```

### 通用修复方案

- 折叠状态变化时，完整执行 `releaseCamera()` → `initCamera()`，不尝试增量更新。
- 相机选择时使用 `findIndex` 查找目标位置相机，未找到时回退到 `cameras[0]`。
- 阔折叠外屏（如 PuraX）只有前置相机，`findIndex` 返回 -1 时自动回退到第一个可用相机。

## 场景 C：拍照后画面旋转

### 问题描述

- 拍摄完成后，照片的实际内容与预期方向不符，发生 90°、180° 或 270° 的旋转。
- 设备旋转后拍照，照片方向未跟随设备持握方向。

### 根因分析

- 拍照时未设置 `rotation` 参数，或 `capture()` 调用未传入 `PhotoCaptureSetting`。
- 未监听重力传感器数据，无法获取设备当前持握方向。
- 前后置相机的旋转角度计算公式不同（前置用减法，后置用加法），混淆导致角度错误。

### 反例：拍照未设置旋转角度

> 来源：`PhotoRotated.ets`

```typescript
Button('拍照')
  .onClick(() => {
    if (this.photoOutput) {
      this.photoOutput.capture();
    }
  })
```

**问题点**：直接调用 `capture()` 未传入 `PhotoCaptureSetting`，照片旋转角度使用默认值，与设备实际持握方向不一致。

### 正例：基于重力传感器的拍照旋转

> 来源：`CameraPhoto.ets`（GoodCase）

```typescript
getCalDegree(x: number, y: number, z: number): number {
  let degree: number = 0;
  if ((x * x + y * y) * 3 < z * z) {
    return degree;
  }
  degree = 90 - (Number)(Math.round(Math.atan2(y, -x) / Math.PI * 180));
  return degree >= 0 ? degree % 360 : degree % 360 + 360;
}

capture(): void {
  let rotation: number = 0;
  let isFront: boolean | undefined = AppStorage.get('isFront');
  try {
    sensor.once(sensor.SensorId.GRAVITY, (data: sensor.GravityResponse) => {
      if (Math.abs(data.z) > OVERLOOKING_GRAVITY_OF_Z_AXIS) {
        rotation = this.lastRotation;
      } else {
        let degree: number = this.getCalDegree(data.x, data.y, data.z);
        if ((degree >= 0 && degree <= 30) || degree >= 300) {
          rotation = camera.ImageRotation.ROTATION_0;
        } else if (degree > 30 && degree <= 120) {
          rotation = isFront
            ? camera.ImageRotation.ROTATION_270
            : camera.ImageRotation.ROTATION_90;
        } else if (degree > 120 && degree <= 210) {
          rotation = camera.ImageRotation.ROTATION_180;
        } else if (degree > 210 && degree <= 300) {
          rotation = isFront
            ? camera.ImageRotation.ROTATION_90
            : camera.ImageRotation.ROTATION_270;
        }
      }

      let setting: camera.PhotoCaptureSetting = {
        quality: camera.QualityLevel.QUALITY_LEVEL_HIGH,
        rotation: rotation,
        mirror: isFront
      }
      this.photoOutput?.capture(setting);
    })
  } catch (error) {
    let err = error as BusinessError;
    console.error('MultiDeviceCamera', `Capture failed. Code: ${err.code}, message: ${err.message}`);
  }
}
```

### 通用修复方案

- 在拍照时使用 `sensor.once(sensor.SensorId.GRAVITY, callback)` 获取当前重力数据。
- 通过 `getCalDegree()` 计算设备持握角度，区分前后置相机的旋转映射。
- 使用 `photoOutput.capture(setting)` 传入 `PhotoCaptureSetting`，包含 `rotation` 和 `mirror` 参数。
- 前置相机需额外设置 `mirror: true` 实现镜像效果。

## 场景 D：预览画面旋转/拉伸

### 问题描述

- 相机预览画面方向与设备持握方向不一致。
- 预览画面出现拉伸或压缩变形。
- 窗口旋转后预览画面未跟随更新。

### 根因分析

- XComponent `onLoad` 中未调用 `setXComponentSurfaceRotation({ lock: true })` 解锁 Surface 旋转。
- `setupRotationListener` 中监听了 `display.on('change')` 但回调仅打印日志，未重新计算预览旋转角度和 Surface 宽高比。
- 未在 `commitConfig` 后调用 `getPreviewRotation` 获取预览旋转角度，或未调用 `setPreviewRotation` 设置旋转。
- Surface 宽高比与预览流旋转后的宽高比不一致。
- 未在 `onAreaChange` 或 `windowSizeChange` 回调中重新设置预览旋转角度和 Surface 尺寸。

### 反例：未设置预览旋转

> 来源：`PreviewRotated.ets`

```typescript
XComponent({
  id: 'cameraPreview',
  type: XComponentType.SURFACE,
  controller: this.xComponentController
}).onLoad(async () => {
  this.surfaceId = this.xComponentController.getXComponentSurfaceId();
  await this.initCamera();
})
```

**问题点**：`onLoad` 中未调用 `setXComponentSurfaceRotation` 解锁 Surface 旋转，也未设置预览旋转角度。

### 反例：未监听窗口变化

> 来源：`PreviewRotated.ets`

```typescript
setupRotationListener(): void {
  display.on('change', (rotation: number) => {
    console.info(TAG, `Rotation changed to: ${rotation * 90} degrees`);
  });
}
```

**问题点**：监听了 `display.on('change')` 但回调中仅打印日志，未重新计算和设置预览旋转角度。

### 正例：完整预览旋转适配

> 来源：`CameraPhoto.ets`（GoodCase）

```typescript
XComponent({
  id: 'cameraPreview',
  type: XComponentType.SURFACE,
  controller: this.xComponentController
}).onLoad(async () => {
  this.surfaceId = this.xComponentController.getXComponentSurfaceId();
  this.xComponentController.setXComponentSurfaceRotation({ lock: true });
  await this.initCamera();
})

updateSurfaceSize(): void {
  if (this.xComponentController && this.surfaceId) {
    let displayRotation: number = display.getDefaultDisplaySync().rotation * camera.ImageRotation.ROTATION_90;
    try {
      let previewRotation = this.previewOutput?.getPreviewRotation(displayRotation);
      if (previewRotation === 0 || previewRotation === 180) {
        this.xComponentController.setXComponentSurfaceRect({
          surfaceWidth: this.previewWidth,
          surfaceHeight: this.previewHeight
        });
      } else {
        this.xComponentController.setXComponentSurfaceRect({
          surfaceWidth: this.previewHeight,
          surfaceHeight: this.previewWidth
        });
      }
    } catch (error) {
      let err = error as BusinessError;
      console.error(`getPreviewRotation call failed. error code: ${err.code}`);
    }
  }
}
```

### 通用修复方案

- 在 XComponent `onLoad` 中调用 `setXComponentSurfaceRotation({ lock: true })` 解锁 Surface 旋转。
- 在 `commitConfig` 后调用 `getPreviewRotation(displayRotation)` 获取旋转角度，并调用 `setPreviewRotation` 设置。
- 监听窗口变化事件（通过 `onAreaChange`），在变化时重新计算 Surface 宽高比。
- Surface 宽高比计算规则：`display.rotation` 为 0°/180° 时 Surface 比例是预览比例的倒数；90°/270° 时与预览比例相同。

## 场景 E：录像/直播画面旋转

### 问题描述

- 录像开始后画面方向与设备持握方向不一致。
- 录像过程中旋转设备，录制画面方向未更新。

### 根因分析

- 录像开始时未获取当前重力传感器数据计算旋转角度。
- `AVMetadata.videoOrientation` 未设置或设置值不合理。
- 录像输出流与预览输出流分辨率宽高比不一致。

### 反例：录像未设置旋转角度

> 来源：`VideoRotated.ets`

```typescript
async prepareVideo(videoProfile: camera.VideoProfile, rotation: number): Promise<camera.VideoOutput | undefined> {
  if (this.videoFile) {
    let avMetadata: media.AVMetadata = {
      videoOrientation: rotation.toString(),
    }
    this.recordSurfaceId = await this.getVideoSurfaceId({
      videoSourceType: media.VideoSourceType.VIDEO_SOURCE_TYPE_SURFACE_YUV,
      profile: {
        fileFormat: media.ContainerFormatType.CFT_MPEG_4,
        videoBitrate: 100000,
        videoCodec: media.CodecMimeType.VIDEO_AVC,
        videoFrameWidth: videoProfile.size.width,
        videoFrameHeight: videoProfile.size.height,
        videoFrameRate: this.cameraPosition === camera.CameraPosition.CAMERA_POSITION_BACK ? 60 : 30,
      },
      url: `fd://${this.videoFile.fd}`,
      metadata: avMetadata
    })
  }
  return
}
```

**问题点**：`prepareVideo` 接收 `rotation` 参数但该参数来自 `this.sensorRotation`，而 `sensorRotation` 在 `setupRotationListener` 中为空实现，未被正确赋值。

### 正例：录像前获取重力传感器角度

> 来源：`CameraVideo.ets`（GoodCase）

```typescript
async startVideo(): Promise<void> {
  sensor.once(sensor.SensorId.GRAVITY, async (data: sensor.GravityResponse) => {
    let isFront = this.cameraPosition === camera.CameraPosition.CAMERA_POSITION_FRONT;
    if (Math.abs(data.z) > OVERLOOKING_GRAVITY_OF_Z_AXIS) {
      this.sensorRotation = this.lastRotation;
    } else {
      let degree: number = this.getCalDegree(data.x, data.y, data.z);
      if ((degree >= 0 && degree <= 30) || degree >= 300) {
        this.sensorRotation = isFront
          ? camera.ImageRotation.ROTATION_270
          : camera.ImageRotation.ROTATION_90;
      } else if (degree > 30 && degree <= 120) {
        this.sensorRotation = isFront
          ? camera.ImageRotation.ROTATION_180
          : camera.ImageRotation.ROTATION_180;
      }
    }
    await this.prepareVideo(this.videoProfile!, this.sensorRotation);
  });
}
```

### 通用修复方案

- 录像开始前使用 `sensor.once(sensor.SensorId.GRAVITY)` 获取当前重力数据。
- 计算设备持握角度，区分前后置相机映射到正确的 `ImageRotation` 值。
- 将旋转角度传入 `AVMetadata.videoOrientation`（合理值为 0、90、180、270）。
- 预览流与录像输出流的分辨率宽高比必须保持一致。

## 场景 F：预览画面花屏堆叠

### 问题描述

- 通过 ImageReceiver 获取预览帧数据后送显，画面出现花屏堆叠状。
- 花屏表现为图像行偏移、内容错位。

### 根因分析

- stride（图像一行在内存中实际占用字节数）通常因内存对齐大于 width。
- 直接按 `width × height` 读取图像数据，将无效填充字节当作有效像素，导致行偏移。
- stride 值因平台而异，不可硬编码。

### 反例：未处理 stride

```typescript
imageReceiver.on('imageArrival', () => {
  imageReceiver.readNextImage((err, image) => {
    let component = image.getComponent(image.ComponentType.JPEG, (err, component) => {
      let pixelMap = image.createPixelMap(component.byteBuffer, {
        size: { width: 1080, height: 1080 }
      });
      this.stridePixel = pixelMap;
    });
  });
});
```

**问题点**：直接使用 `component.byteBuffer` 创建 PixelMap，未检查 `rowStride` 是否与 `width` 一致。

### 正例一：拷贝有效像素到新 buffer

```typescript
imageReceiver.on('imageArrival', () => {
  imageReceiver.readNextImage((err, image) => {
    let component = image.getComponent(image.ComponentType.JPEG, (err, component) => {
      let width = component.size.width;
      let height = component.size.height;
      let stride = component.rowStride;

      if (stride === width) {
        let pixelMap = image.createPixelMap(component.byteBuffer, {
          size: { width: width, height: height }
        });
        this.stridePixel = pixelMap;
      } else {
        let srcArr = new Uint8Array(component.byteBuffer);
        let dstArr = new Uint8Array(width * height);
        for (let row = 0; row < height; row++) {
          let srcOffset = row * stride;
          let dstOffset = row * width;
          for (let col = 0; col < width; col++) {
            dstArr[dstOffset + col] = srcArr[srcOffset + col];
          }
        }
        let pixelMap = image.createPixelMap(dstArr.buffer, {
          size: { width: width, height: height }
        });
        this.stridePixel = pixelMap;
      }
    });
  });
});
```

### 正例二：使用 cropSync 裁剪

```typescript
if (stride !== width) {
  let pixelMap = image.createPixelMap(component.byteBuffer, {
    size: { width: stride, height: height }
  });
  pixelMap.cropSync({ x: 0, y: 0, size: { width: width, height: height } });
  this.stridePixel = pixelMap;
}
```

### 通用修复方案

- 通过 `component.rowStride` 获取实际 stride 值（运行时获取，不可硬编码）。
- stride = width 时可直接使用；stride ≠ width 时需去除无效像素。
- 方案一（buffer 拷贝）：逐行拷贝有效像素到新 buffer，用 `width × height` 创建 PixelMap。适用于需要精确像素数据的场景。
- 方案二（cropSync）：按 `stride × height` 创建 PixelMap，调用 `cropSync()` 裁剪多余像素。适用于快速修复场景。

## 场景 G：2in1/阔折叠设备后置相机不可用

### 问题描述

- 在 2in1 设备或阔折叠外屏上选择后置相机失败。
- 相机初始化抛出异常或预览黑屏。

### 根因分析

- 2in1 设备大部分仅有前置内置相机。
- 阔折叠外屏（如 PuraX）仅有前置相机。
- 相机选择逻辑未考虑目标位置相机不存在的情况。

### 通用修复方案

- 选择相机时使用 `findIndex` 查找目标位置相机。
- 未找到（`deviceIndex === -1`）时回退到 `cameras[0]`（第一个可用相机）。
- 切换前后相机时同理，若目标位置不存在则保持当前相机不变。

## 统一验证矩阵

- 设备维度：手机、双折叠（折叠/展开）、阔折叠（外屏/内屏）、三折叠（F/M/G 态）、平板、2in1。
- 状态维度：折叠态、展开态、悬停态（半折叠）。
- 方向维度：竖屏（0°）、横屏（90°）、反向竖屏（180°）、反向横屏（270°）。
- 功能维度：
  - 预览显示正常（无花屏、无拉伸、方向正确）。
  - 拍照方向正确（与设备持握方向一致）。
  - 录像方向正确（与录像时持握方向一致）。
  - 前后相机切换正常。
  - 折叠态切换无黑屏、相机设备正确重建。
  - 各断点按钮布局正常。
- 生命周期维度：
  - 冷启动相机初始化正常。
  - 热启动（`onPageShow`）相机恢复正常。
  - 页面退出后监听已回收、无残留。
- stride 维度：
  - 各平台 stride 值记录。
  - stride ≠ width 时像素处理验证。
- 证据维度：截图 + 日志 + 设备/折叠状态信息同时具备，禁止只看单一日志下结论。
