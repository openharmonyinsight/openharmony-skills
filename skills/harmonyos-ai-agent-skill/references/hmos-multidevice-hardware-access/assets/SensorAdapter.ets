/**
 * SensorAdapter.ets
 * 传感器适配器
 */

import sensor from '@ohos.sensor';

/**
 * 传感器类型
 */
export enum SensorType {
  ACCELEROMETER = 'Accelerometer',
  GYROSCOPE = 'Gyroscope',
  ORIENTATION = 'Orientation',
  MAGNETIC = 'Magnetic',
  AMBIENT_LIGHT = 'AmbientLight',
  PROXIMITY = 'Proximity',
  STEP_COUNTER = 'StepCounter',
  GRAVITY = 'Gravity'
}

/**
 * 传感器数据接口
 */
export interface SensorData {
  x?: number;
  y?: number;
  z?: number;
  lightLux?: number;
  distance?: number;
  steps?: number;
  alpha?: number;
  beta?: number;
  gamma?: number;
}

/**
 * 传感器监听器类型
 */
export type SensorListener = (data: SensorData) => void;

/**
 * 传感器适配器
 */
export class SensorAdapter {
  private static instance: SensorAdapter;
  private subscribers: Map<SensorType, sensor.SensorSubscriber> = new Map();
  private listeners: Map<SensorType, SensorListener[]> = new Map();
  private lastData: Map<SensorType, SensorData> = new Map();

  private constructor() {}

  static getInstance(): SensorAdapter {
    if (!SensorAdapter.instance) {
      SensorAdapter.instance = new SensorAdapter();
    }
    return SensorAdapter.instance;
  }

  /**
   * 检测传感器是否可用
   */
  isSensorAvailable(type: SensorType): boolean {
    const sysCapName = this.getSysCapName(type);
    return canIUse(`SystemCapability.Sensors.Sensor.${sysCapName}`);
  }

  /**
   * 获取系统能力名称
   */
  private getSysCapName(type: SensorType): string {
    switch (type) {
      case SensorType.ACCELEROMETER:
        return 'Accelerometer';
      case SensorType.GYROSCOPE:
        return 'Gyroscope';
      case SensorType.ORIENTATION:
        return 'Compass';
      case SensorType.AMBIENT_LIGHT:
        return 'LightSensor';
      case SensorType.PROXIMITY:
        return 'Proximity';
      case SensorType.STEP_COUNTER:
        return 'StepCounter';
      default:
        return type;
    }
  }

  /**
   * 订阅传感器
   */
  subscribe(type: SensorType, listener: SensorListener, interval: 'game' | 'ui' | 'normal' = 'ui'): boolean {
    if (!this.isSensorAvailable(type)) {
      console.warn(`Sensor ${type} is not available`);
      return false;
    }

    // 添加监听器
    if (!this.listeners.has(type)) {
      this.listeners.set(type, []);
    }
    this.listeners.get(type)!.push(listener);

    // 如果已经订阅，直接返回
    if (this.subscribers.has(type)) {
      return true;
    }

    try {
      let subscriber: sensor.SensorSubscriber;

      switch (type) {
        case SensorType.ACCELEROMETER:
          subscriber = sensor.subscribeAccelerometer({ interval }, this.handleAccelerometer.bind(this));
          break;
        case SensorType.GYROSCOPE:
          subscriber = sensor.subscribeGyroscope({ interval }, this.handleGyroscope.bind(this));
          break;
        case SensorType.ORIENTATION:
          subscriber = sensor.subscribeOrientationSensor({ interval }, this.handleOrientation.bind(this));
          break;
        case SensorType.AMBIENT_LIGHT:
          subscriber = sensor.subscribeAmbientLight({ interval }, this.handleAmbientLight.bind(this));
          break;
        case SensorType.PROXIMITY:
          subscriber = sensor.subscribeProximity({ interval }, this.handleProximity.bind(this));
          break;
        case SensorType.STEP_COUNTER:
          subscriber = sensor.subscribeStepCounter({ interval }, this.handleStepCounter.bind(this));
          break;
        case SensorType.GRAVITY:
          subscriber = sensor.subscribeGravitySensor({ interval }, this.handleGravity.bind(this));
          break;
        default:
          return false;
      }

      this.subscribers.set(type, subscriber);
      return true;
    } catch (error) {
      console.error(`Failed to subscribe ${type}:`, error);
      return false;
    }
  }

  /**
   * 取消订阅传感器
   */
  unsubscribe(type: SensorType, listener?: SensorListener): void {
    if (listener) {
      // 移除特定监听器
      const listeners = this.listeners.get(type);
      if (listeners) {
        const index = listeners.indexOf(listener);
        if (index > -1) {
          listeners.splice(index, 1);
        }
        // 如果还有监听器，不取消订阅
        if (listeners.length > 0) {
          return;
        }
      }
    }

    // 取消订阅
    const subscriber = this.subscribers.get(type);
    if (subscriber) {
      try {
        switch (type) {
          case SensorType.ACCELEROMETER:
            sensor.unsubscribeAccelerometer(subscriber);
            break;
          case SensorType.GYROSCOPE:
            sensor.unsubscribeGyroscope(subscriber);
            break;
          case SensorType.ORIENTATION:
            sensor.unsubscribeOrientationSensor(subscriber);
            break;
          case SensorType.AMBIENT_LIGHT:
            sensor.unsubscribeAmbientLight(subscriber);
            break;
          case SensorType.PROXIMITY:
            sensor.unsubscribeProximity(subscriber);
            break;
          case SensorType.STEP_COUNTER:
            sensor.unsubscribeStepCounter(subscriber);
            break;
          case SensorType.GRAVITY:
            sensor.unsubscribeGravitySensor(subscriber);
            break;
        }
      } catch (error) {
        console.error(`Failed to unsubscribe ${type}:`, error);
      }
      this.subscribers.delete(type);
      this.listeners.delete(type);
    }
  }

  /**
   * 获取最后一次传感器数据
   */
  getLastData(type: SensorType): SensorData | undefined {
    return this.lastData.get(type);
  }

  /**
   * 通知所有监听器
   */
  private notifyListeners(type: SensorType, data: SensorData): void {
    this.lastData.set(type, data);
    const listeners = this.listeners.get(type);
    if (listeners) {
      listeners.forEach(listener => {
        try {
          listener(data);
        } catch (error) {
          console.error(`Sensor listener error for ${type}:`, error);
        }
      });
    }
  }

  // 传感器数据处理方法
  private handleAccelerometer(data: sensor.AccelerometerResponse): void {
    this.notifyListeners(SensorType.ACCELEROMETER, { x: data.x, y: data.y, z: data.z });
  }

  private handleGyroscope(data: sensor.GyroscopeResponse): void {
    this.notifyListeners(SensorType.GYROSCOPE, { x: data.x, y: data.y, z: data.z });
  }

  private handleOrientation(data: sensor.OrientationResponse): void {
    this.notifyListeners(SensorType.ORIENTATION, { alpha: data.alpha, beta: data.beta, gamma: data.gamma });
  }

  private handleAmbientLight(data: sensor.AmbientLightResponse): void {
    this.notifyListeners(SensorType.AMBIENT_LIGHT, { lightLux: data.lightLux });
  }

  private handleProximity(data: sensor.ProximityResponse): void {
    this.notifyListeners(SensorType.PROXIMITY, { distance: data.distance });
  }

  private handleStepCounter(data: sensor.StepCounterResponse): void {
    this.notifyListeners(SensorType.STEP_COUNTER, { steps: data.steps });
  }

  private handleGravity(data: sensor.GravityResponse): void {
    this.notifyListeners(SensorType.GRAVITY, { x: data.x, y: data.y, z: data.z });
  }

  /**
   * 销毁所有订阅
   */
  destroy(): void {
    this.subscribers.forEach((_, type) => {
      this.unsubscribe(type);
    });
    this.listeners.clear();
    this.lastData.clear();
  }
}

/**
 * 使用示例:
 *
 * const adapter = SensorAdapter.getInstance();
 *
 * // 检测传感器可用性
 * if (adapter.isSensorAvailable(SensorType.ACCELEROMETER)) {
 *   // 订阅加速度传感器
 *   adapter.subscribe(SensorType.ACCELEROMETER, (data) => {
 *     console.log(`x: ${data.x}, y: ${data.y}, z: ${data.z}`);
 *   });
 * }
 *
 * // 组件销毁时取消订阅
 * aboutToDisappear() {
 *   adapter.unsubscribe(SensorType.ACCELEROMETER);
 * }
 */
