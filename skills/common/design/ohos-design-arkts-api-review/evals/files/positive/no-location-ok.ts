// Eval file for rule: Public接口禁止返回位置信息
// 正例1：WiFi接口返回信息中不含BSSID等位置敏感信息
/**
 * Obtains the currently linked WiFi connection information.
 *
 * @returns { WifiLinkedInfo } WiFi connection information.
 * @syscap SystemCapability.Communication.WiFi.STA
 * @since 6
 */
function getLinkedInfo(): WifiLinkedInfo;

// WifiLinkedInfo 中只包含安全字段，不包含 BSSID
interface WifiLinkedInfo {
  ssid: string;
  rssi: number;
  band: number;
  linkSpeed: number;
  frequency: number;
  isHidden: boolean;
  isRestricted: boolean;
  chload: number;
  score: number;
}

// 正例2：蓝牙扫描结果不暴露设备MAC地址（使用匿名标识替代）
/**
 * Start a BLE scan.
 *
 * @param { ScanOptions } options - Scan options.
 * @returns { Promise<Array<ScanResult>> } Scan results.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function startBLEScan(options: ScanOptions): Promise<Array<ScanResult>>;

interface ScanResult {
  deviceId: string;       // 匿名化的设备ID，非真实MAC地址
  rssi: number;
  data: ArrayBuffer;
}

// 正例3：位置信息接口通过系统接口+权限控制开放（经过TMG评审）
/**
 * Get the current location.
 *
 * @permission ohos.permission.LOCATION
 * @returns { Location } Current location.
 * @syscap SystemCapability.Location.Location.Core
 * @systemapi
 * @since 10
 */
function getCurrentLocation(): Location;

// 正例4：WiFi扫描结果不包含BSSID
/**
 * Obtain the scan result of the WiFi.
 *
 * @returns { Array<WifiScanInfo> } WiFi scan information list.
 * @syscap SystemCapability.Communication.WiFi.STA
 * @since 6
 */
function getScanResults(): Array<WifiScanInfo>;

interface WifiScanInfo {
  ssid: string;
  rssi: number;
  band: number;
  frequency: number;
  linkSpeed: number;
  // 不包含 bssid 字段
}
