# 系统能力机制 (SysCap) 指南

## 目录

1. [SysCap概述](#syscap概述)
2. [能力检测](#能力检测)
3. [module.json5配置](#modulejson5配置)
4. [常用SysCap列表](#常用syscap列表)
5. [最佳实践](#最佳实践)

---

## SysCap概述

系统能力 (SystemCapability，缩写为SysCap) 指操作系统中每一个相对独立的特性，如蓝牙、WiFi、NFC、摄像头等。

### 核心概念

- 每个系统能力对应多个API
- 能力随目标设备是否支持而存在或消失
- 应用需要检测能力可用性再使用

### 能力集

| 能力集类型 | 说明 |
|-----------|------|
| 支持能力集 | 设备实际支持的SysCap集合 |
| 要求能力集 | 应用要求设备必须支持的SysCap集合 |
| 联想能力集 | 开发时可用于联想的SysCap集合 |

---

## 能力检测

### canIUse API

```typescript
// 检测单个能力
if (canIUse('SystemCapability.Multimedia.Camera.Core')) {
  // 支持相机
} else {
  // 不支持，提示用户或降级
}

// 检测能力中的特定接口
if (canIUse('SystemCapability.Multimedia.Camera.Core.takePicture')) {
  // 支持拍照
}
```

### 常用检测示例

```typescript
// 检测NFC
if (canIUse('SystemCapability.Communication.NFC.Core')) {
  // NFC可用
}

// 检测蓝牙
if (canIUse('SystemCapability.Communication.Bluetooth.Core')) {
  // 蓝牙可用
}

// 检测GPS
if (canIUse('SystemCapability.Location.Location.Core')) {
  // 定位可用
}

// 检测指纹
if (canIUse('SystemCapability.Security.Fingerprint')) {
  // 指纹可用
}

// 检测面部识别
if (canIUse('SystemCapability.Security.Face')) {
  // 面部识别可用
}
```

---

## module.json5配置

### 声明要求能力集

```json
{
  "module": {
    "name": "entry",
    "type": "entry",
    "deviceTypes": ["default", "tablet"],
    "abilities": [...],
    "reqSysCapabilities": [
      "SystemCapability.Multimedia.Camera.Core",
      "SystemCapability.Location.Location.Core"
    ]
  }
}
```

### 配置说明

| 字段 | 说明 |
|-----|------|
| reqSysCapabilities | 应用要求设备必须支持的能力列表 |
| deviceTypes | 应用支持的设备类型 |

---

## 常用SysCap列表

### 多媒体

| SysCap | 说明 |
|--------|------|
| SystemCapability.Multimedia.Camera.Core | 相机核心能力 |
| SystemCapability.Multimedia.Audio.Core | 音频核心能力 |
| SystemCapability.Multimedia.Media.Core | 媒体核心能力 |
| SystemCapability.Multimedia.Image.Core | 图像核心能力 |

### 通信

| SysCap | 说明 |
|--------|------|
| SystemCapability.Communication.WiFi.Core | WiFi |
| SystemCapability.Communication.Bluetooth.Core | 蓝牙 |
| SystemCapability.Communication.NFC.Core | NFC |
| SystemCapability.Communication.NetStack.Core | 网络栈 |

### 定位

| SysCap | 说明 |
|--------|------|
| SystemCapability.Location.Location.Core | 定位核心 |
| SystemCapability.Location.Location.Gnss | GPS定位 |
| SystemCapability.Location.Location.Network | 网络定位 |

### 传感器

| SysCap | 说明 |
|--------|------|
| SystemCapability.Sensors.Sensor.Core | 传感器核心 |
| SystemCapability.Sensors.Sensor.Accelerometer | 加速度传感器 |
| SystemCapability.Sensors.Sensor.Gyroscope | 陀螺仪 |
| SystemCapability.Sensors.Sensor.Compass | 罗盘 |

### 安全

| SysCap | 说明 |
|--------|------|
| SystemCapability.Security.Fingerprint | 指纹 |
| SystemCapability.Security.Face | 面部识别 |
| SystemCapability.Security.ScreenLock | 屏幕锁 |

---

## 最佳实践

### 1. 使用前检测

```typescript
// ✅ 正确: 先检测再使用
if (canIUse('SystemCapability.Communication.NFC.Core')) {
  // 使用NFC
} else {
  // 提示用户或降级
}

// ❌ 错误: 直接使用可能崩溃
// 直接调用NFC API
```

### 2. 优雅降级

```typescript
async function getLocation(): Promise<Location> {
  if (canIUse('SystemCapability.Location.Location.Gnss')) {
    // 使用GPS定位
    return await this.getGnssLocation();
  } else if (canIUse('SystemCapability.Location.Location.Network')) {
    // 降级到网络定位
    return await this.getNetworkLocation();
  } else {
    // 让用户手动选择位置
    return await this.showManualLocationPicker();
  }
}
```

### 3. UI提示

```typescript
@Entry
@Component
struct FeaturePage {
  @State nfcAvailable: boolean = false;

  aboutToAppear() {
    this.nfcAvailable = canIUse('SystemCapability.Communication.NFC.Core');
  }

  build() {
    Column() {
      if (this.nfcAvailable) {
        Button('使用NFC')
          .onClick(() => this.useNFC())
      } else {
        Text('您的设备不支持NFC功能')
          .fontColor('#999')
      }
    }
  }
}
```

### 4. 合理声明reqSysCapabilities

```json
// ✅ 正确: 只声明核心必需的能力
"reqSysCapabilities": [
  "SystemCapability.Multimedia.Camera.Core"
]

// ❌ 错误: 声明过多限制设备范围
"reqSysCapabilities": [
  "SystemCapability.Multimedia.Camera.Core",
  "SystemCapability.Communication.NFC.Core",  // 非必需
  "SystemCapability.Location.Location.Gnss"   // 非必需
]
```
