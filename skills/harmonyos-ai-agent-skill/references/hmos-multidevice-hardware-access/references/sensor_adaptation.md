# 传感器适配指南

## 目录

1. [传感器类型](#传感器类型)
2. [传感器检测](#传感器检测)
3. [数据订阅](#数据订阅)
4. [常用传感器示例](#常用传感器示例)
5. [最佳实践](#最佳实践)

---

## 传感器类型

### 常用传感器

| 传感器 | API | 数据类型 | 适用场景 |
|-------|-----|---------|---------|
| 加速度 | `subscribeAccelerometer` | AccelerometerResponse | 屏幕旋转、摇一摇 |
| 陀螺仪 | `subscribeGyroscope` | GyroscopeResponse | 游戏、VR/AR |
| 方向 | `subscribeOrientationSensor` | OrientationResponse | 导航、指南针 |
| 磁力计 | `subscribeMagneticSensor` | MagneticResponse | 指南针 |
| 光线 | `subscribeAmbientLight` | AmbientLightResponse | 自动亮度 |
| 距离 | `subscribeProximity` | ProximityResponse | 通话息屏 |
| 计步 | `subscribeStepCounter` | StepCounterResponse | 健康应用 |
| 重力 | `subscribeGravitySensor` | GravityResponse | 屏幕旋转 |

---

## 传感器检测

### 使用 canIUse 检测

```typescript
// 检测加速度传感器
if (canIUse('SystemCapability.Sensors.Sensor.Accelerometer')) {
  // 加速度传感器可用
}

// 检测陀螺仪
if (canIUse('SystemCapability.Sensors.Sensor.Gyroscope')) {
  // 陀螺仪可用
}
```

### 封装传感器检测

```typescript
export class SensorChecker {
  static isAccelerometerAvailable(): boolean {
    return canIUse('SystemCapability.Sensors.Sensor.Accelerometer');
  }

  static isGyroscopeAvailable(): boolean {
    return canIUse('SystemCapability.Sensors.Sensor.Gyroscope');
  }

  static isCompassAvailable(): boolean {
    return canIUse('SystemCapability.Sensors.Sensor.Compass');
  }

  static isLightSensorAvailable(): boolean {
    return canIUse('SystemCapability.Sensors.Sensor.LightSensor');
  }
}
```

---

## 数据订阅

### 基本订阅模式

```typescript
import sensor from '@ohos.sensor';

@Entry
@Component
struct SensorExample {
  private subscriber?: sensor.SensorSubscriber;

  aboutToAppear() {
    this.subscribeSensor();
  }

  aboutToDisappear() {
    this.unsubscribeSensor();
  }

  subscribeSensor() {
    try {
      this.subscriber = sensor.subscribeAccelerometer({
        interval: 'normal' // game/ui/normal
      }, (data: sensor.AccelerometerResponse) => {
        // 处理传感器数据
        console.log(`x: ${data.x}, y: ${data.y}, z: ${data.z}`);
      });
    } catch (error) {
      console.error('Subscribe failed:', error);
    }
  }

  unsubscribeSensor() {
    if (this.subscriber) {
      sensor.unsubscribeAccelerometer(this.subscriber);
    }
  }
}
```

### 订阅频率选项

| 频率 | 说明 | 适用场景 |
|-----|------|---------|
| game | 高频 (约20ms) | 游戏、实时交互 |
| ui | 中频 (约60ms) | UI响应 |
| normal | 低频 (约200ms) | 一般场景 |

---

## 常用传感器示例

### 加速度传感器 - 屏幕旋转检测

```typescript
import sensor from '@ohos.sensor';

class ScreenRotationDetector {
  private subscriber?: sensor.SensorSubscriber;
  private currentRotation: number = 0;

  startListening(callback: (rotation: number) => void) {
    this.subscriber = sensor.subscribeAccelerometer({
      interval: 'ui'
    }, (data: sensor.AccelerometerResponse) => {
      const rotation = this.calculateRotation(data.x, data.y);
      if (Math.abs(rotation - this.currentRotation) > 30) {
        this.currentRotation = rotation;
        callback(rotation);
      }
    });
  }

  private calculateRotation(x: number, y: number): number {
    const radians = Math.atan2(y, x);
    return radians * (180 / Math.PI);
  }

  stopListening() {
    if (this.subscriber) {
      sensor.unsubscribeAccelerometer(this.subscriber);
    }
  }
}
```

### 方向传感器 - 指南针

```typescript
import sensor from '@ohos.sensor';

class CompassHelper {
  private subscriber?: sensor.SensorSubscriber;

  startListening(callback: (azimuth: number) => void) {
    this.subscriber = sensor.subscribeOrientationSensor({
      interval: 'ui'
    }, (data: sensor.OrientationResponse) => {
      // azimuth: 方位角 (0-360)
      callback(data.alpha);
    });
  }

  stopListening() {
    if (this.subscriber) {
      sensor.unsubscribeOrientationSensor(this.subscriber);
    }
  }

  getDirectionText(azimuth: number): string {
    if (azimuth >= 337.5 || azimuth < 22.5) return '北';
    if (azimuth >= 22.5 && azimuth < 67.5) return '东北';
    if (azimuth >= 67.5 && azimuth < 112.5) return '东';
    if (azimuth >= 112.5 && azimuth < 157.5) return '东南';
    if (azimuth >= 157.5 && azimuth < 202.5) return '南';
    if (azimuth >= 202.5 && azimuth < 247.5) return '西南';
    if (azimuth >= 247.5 && azimuth < 292.5) return '西';
    return '西北';
  }
}
```

### 光线传感器 - 自动亮度

```typescript
import sensor from '@ohos.sensor';

class LightSensorHelper {
  private subscriber?: sensor.SensorSubscriber;

  startListening(callback: (lux: number) => void) {
    this.subscriber = sensor.subscribeAmbientLight({
      interval: 'normal'
    }, (data: sensor.AmbientLightResponse) => {
      // lightLux: 光照强度 (勒克斯)
      callback(data.lightLux);
    });
  }

  stopListening() {
    if (this.subscriber) {
      sensor.unsubscribeAmbientLight(this.subscriber);
    }
  }

  // 根据光照强度建议主题
  suggestTheme(lux: number): 'dark' | 'light' {
    return lux < 50 ? 'dark' : 'light';
  }
}
```

---

## 最佳实践

### 1. 检测能力再使用

```typescript
// ✅ 正确
if (canIUse('SystemCapability.Sensors.Sensor.Accelerometer')) {
  sensor.subscribeAccelerometer(...);
}

// ❌ 错误: 直接调用可能失败
sensor.subscribeAccelerometer(...);
```

### 2. 及时取消订阅

```typescript
aboutToDisappear() {
  // 重要: 取消订阅避免内存泄漏
  if (this.subscriber) {
    sensor.unsubscribeAccelerometer(this.subscriber);
  }
}
```

### 3. 使用防抖处理数据

```typescript
private lastUpdateTime: number = 0;
private readonly THROTTLE_MS: number = 100;

private handleSensorData(data: sensor.AccelerometerResponse): void {
  const now = Date.now();
  if (now - this.lastUpdateTime < this.THROTTLE_MS) {
    return;
  }
  this.lastUpdateTime = now;
  // 处理数据
}
```

### 4. 处理异常

```typescript
subscribeSensor() {
  try {
    this.subscriber = sensor.subscribeAccelerometer({
      interval: 'normal'
    }, (data) => {
      // 处理数据
    });
  } catch (error) {
    console.error('Sensor subscribe failed:', error);
    // 提示用户或降级
  }
}
```
