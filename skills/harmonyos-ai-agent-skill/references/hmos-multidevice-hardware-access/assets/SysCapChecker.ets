/**
 * SysCapChecker.ets
 * 系统能力检测工具
 */

/**
 * 系统能力类型
 */
export type SysCapName = string;

/**
 * 系统能力检测结果
 */
export interface SysCapCheckResult {
  name: SysCapName;
  available: boolean;
  message?: string;
}

/**
 * 系统能力检测器
 */
export class SysCapChecker {
  private static instance: SysCapChecker;
  private cache: Map<string, boolean> = new Map();

  private constructor() {}

  static getInstance(): SysCapChecker {
    if (!SysCapChecker.instance) {
      SysCapChecker.instance = new SysCapChecker();
    }
    return SysCapChecker.instance;
  }

  /**
   * 检测单个系统能力
   */
  canIUse(sysCap: SysCapName): boolean {
    if (this.cache.has(sysCap)) {
      return this.cache.get(sysCap)!;
    }

    const result = canIUse(`SystemCapability.${sysCap}`);
    this.cache.set(sysCap, result);
    return result;
  }

  /**
   * 检测多个系统能力
   */
  checkMultiple(sysCaps: SysCapName[]): SysCapCheckResult[] {
    return sysCaps.map(name => ({
      name,
      available: this.canIUse(name)
    }));
  }

  /**
   * 检测并返回第一个可用的能力
   */
  findFirstAvailable(sysCaps: SysCapName[]): SysCapName | null {
    for (const sysCap of sysCaps) {
      if (this.canIUse(sysCap)) {
        return sysCap;
      }
    }
    return null;
  }

  /**
   * 检测是否所有能力都可用
   */
  areAllAvailable(sysCaps: SysCapName[]): boolean {
    return sysCaps.every(sysCap => this.canIUse(sysCap));
  }

  /**
   * 清除缓存
   */
  clearCache(): void {
    this.cache.clear();
  }
}

/**
 * 常用系统能力常量
 */
export class SysCapConstants {
  // 多媒体
  static readonly CAMERA_CORE = 'Multimedia.Camera.Core';
  static readonly AUDIO_CORE = 'Multimedia.Audio.Core';
  static readonly MEDIA_CORE = 'Multimedia.Media.Core';
  static readonly IMAGE_CORE = 'Multimedia.Image.Core';

  // 通信
  static readonly WIFI_CORE = 'Communication.WiFi.Core';
  static readonly BLUETOOTH_CORE = 'Communication.Bluetooth.Core';
  static readonly NFC_CORE = 'Communication.NFC.Core';
  static readonly NET_STACK_CORE = 'Communication.NetStack.Core';

  // 定位
  static readonly LOCATION_CORE = 'Location.Location.Core';
  static readonly LOCATION_GNSS = 'Location.Location.Gnss';
  static readonly LOCATION_NETWORK = 'Location.Location.Network';

  // 传感器
  static readonly SENSOR_ACCELEROMETER = 'Sensors.Sensor.Accelerometer';
  static readonly SENSOR_GYROSCOPE = 'Sensors.Sensor.Gyroscope';
  static readonly SENSOR_COMPASS = 'Sensors.Sensor.Compass';
  static readonly SENSOR_LIGHT = 'Sensors.Sensor.LightSensor';

  // 安全
  static readonly FINGERPRINT = 'Security.Fingerprint';
  static readonly FACE = 'Security.Face';
  static readonly SCREEN_LOCK = 'Security.ScreenLock';
}

/**
 * 使用示例:
 *
 * const checker = SysCapChecker.getInstance();
 *
 * // 检测单个能力
 * if (checker.canIUse(SysCapConstants.NFC_CORE)) {
 *   // NFC 可用
 * }
 *
 * // 检测多个能力
 * const results = checker.checkMultiple([
 *   SysCapConstants.CAMERA_CORE,
 *   SysCapConstants.LOCATION_GNSS,
 *   SysCapConstants.NFC_CORE
 * ]);
 *
 * // 查找第一个可用的定位方式
 * const locationMethod = checker.findFirstAvailable([
 *   SysCapConstants.LOCATION_GNSS,
 *   SysCapConstants.LOCATION_NETWORK
 * ]);
 */
