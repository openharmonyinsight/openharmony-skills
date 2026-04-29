# 外接设备处理指南

## 目录

1. [外接设备概述](#外接设备概述)
2. [外接摄像头](#外接摄像头)
3. [外接显示器](#外接显示器)
4. [USB设备](#usb设备)
5. [最佳实践](#最佳实践)

---

## 外接设备概述

PC和部分平板设备可能连接外部硬件，应用需要能够检测和处理这些设备。

### 常见外接设备

| 设备类型 | 说明 | 处理方式 |
|---------|------|---------|
| 外接摄像头 | USB摄像头、专业摄像机 | 枚举可用相机 |
| 外接显示器 | 扩展屏、投影仪 | 多窗口适配 |
| 键盘/鼠标 | 有线或无线输入设备 | 交互适配 |
| USB存储 | U盘、移动硬盘 | 文件访问 |
| 游戏手柄 | 蓝牙或有线手柄 | 输入事件 |

---

## 外接摄像头

### 枚举所有相机

```typescript
import camera from '@ohos.multimedia.camera';

async function listAllCameras(): Promise<camera.CameraDevice[]> {
  const cameraManager = camera.getCameraManager(getContext(this));
  const cameras = cameraManager.getSupportedCameras();

  cameras.forEach((cam, index) => {
    console.log(`Camera ${index}:`);
    console.log(`  ID: ${cam.cameraId}`);
    console.log(`  Position: ${cam.cameraPosition}`);
    console.log(`  Type: ${cam.cameraType}`);
  });

  return cameras;
}
```

### 处理外接摄像头热插拔

```typescript
import camera from '@ohos.multimedia.camera';

class CameraManager {
  private cameraManager: camera.CameraManager;
  private cameras: camera.CameraDevice[] = [];
  private currentCamera?: camera.CameraDevice;

  constructor() {
    this.cameraManager = camera.getCameraManager(getContext(this));
    this.cameras = this.cameraManager.getSupportedCameras();
  }

  // 监听相机状态变化
  listenCameraChange() {
    this.cameraManager.on('cameraStatus', (cameraStatus: camera.CameraStatusInfo) => {
      if (cameraStatus.status === camera.CameraStatus.CAMERA_STATUS_AVAILABLE) {
        console.log(`Camera ${cameraStatus.camera.cameraId} available`);
        this.cameras.push(cameraStatus.camera);
      } else if (cameraStatus.status === camera.CameraStatus.CAMERA_STATUS_UNAVAILABLE) {
        console.log(`Camera ${cameraStatus.camera.cameraId} unavailable`);
        this.cameras = this.cameras.filter(c => c.cameraId !== cameraStatus.camera.cameraId);

        // 如果当前相机被移除，切换到其他相机
        if (this.currentCamera?.cameraId === cameraStatus.camera.cameraId) {
          this.switchToAvailableCamera();
        }
      }
    });
  }

  private switchToAvailableCamera(): void {
    if (this.cameras.length > 0) {
      this.currentCamera = this.cameras[0];
      // 重新打开相机
    } else {
      console.warn('No camera available');
    }
  }
}
```

---

## 外接显示器

### 检测多显示器

```typescript
import display from '@ohos.display';

async function listAllDisplays(): Promise<display.Display[]> {
  const displays = display.getAllDisplays();

  displays.forEach((d, index) => {
    console.log(`Display ${index}:`);
    console.log(`  ID: ${d.id}`);
    console.log(`  Name: ${d.name}`);
    console.log(`  Width: ${px2vp(d.width)}vp`);
    console.log(`  Height: ${px2vp(d.height)}vp`);
    console.log(`  Rotation: ${d.rotation * 90}°`);
  });

  return displays;
}
```

### 监听显示器变化

```typescript
class DisplayManager {
  private displays: display.Display[] = [];

  constructor() {
    this.displays = display.getAllDisplays();
  }

  listenDisplayChange() {
    display.on('add', (displayId: number) => {
      console.log(`Display ${displayId} added`);
      this.displays = display.getAllDisplays();
    });

    display.on('remove', (displayId: number) => {
      console.log(`Display ${displayId} removed`);
      this.displays = display.getAllDisplays();
    });

    display.on('change', (displayId: number) => {
      console.log(`Display ${displayId} changed`);
      // 更新显示器信息
    });
  }
}
```

---

## USB设备

### 检测USB设备

```typescript
import usb from '@ohos.usbManager';

async function listUsbDevices(): Promise<usb.USBDevice[]> {
  const devices = usb.getDevices();

  devices.forEach((device, index) => {
    console.log(`USB Device ${index}:`);
    console.log(`  Vendor ID: ${device.vendorId}`);
    console.log(`  Product ID: ${device.productId}`);
    console.log(`  Name: ${device.name}`);
  });

  return devices;
}
```

---

## 最佳实践

### 1. 设备热插拔处理

```typescript
// 监听设备变化，及时更新UI
cameraManager.on('cameraStatus', (status) => {
  // 更新相机列表UI
  this.updateCameraList();
});
```

### 2. 优雅降级

```typescript
async function getCamera(): Promise<camera.CameraDevice | null> {
  const cameras = await listAllCameras();
  if (cameras.length === 0) {
    // 没有可用相机，显示提示
    this.showNoCameraMessage();
    return null;
  }
  return cameras[0];
}
```

### 3. 用户选择

```typescript
@State cameras: camera.CameraDevice[] = [];
@State selectedCamera: camera.CameraDevice | null = null;

build() {
  Column() {
    if (this.cameras.length > 1) {
      // 多个相机时让用户选择
      List() {
        ForEach(this.cameras, (cam: camera.CameraDevice) => {
          ListItem() {
            Text(`Camera ${cam.cameraId}`)
              .onClick(() => {
                this.selectedCamera = cam;
              })
          }
        })
      }
    }
  }
}
```
