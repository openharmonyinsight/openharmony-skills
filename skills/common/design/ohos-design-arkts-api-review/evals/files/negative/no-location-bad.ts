// Eval file for rule: Public接口禁止返回位置信息
// 反例1：Public接口直接返回WiFi BSSID
/**
 * Obtains the currently linked WiFi connection information.
 *
 * @returns { WifiLinkedInfo } WiFi connection information.
 * @syscap SystemCapability.Communication.WiFi.STA
 * @since 6
 */
function getLinkedInfo(): WifiLinkedInfo;

interface WifiLinkedInfo {
  ssid: string;
  bssid: string;       // 问题：Public接口返回BSSID，可被用于位置推算
  rssi: number;
  band: number;
}

// 反例2：WiFi扫描结果中包含BSSID
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
  bssid: string;       // 问题：Public接口返回BSSID
  rssi: number;
  frequency: number;
}

// 反例3：蓝牙扫描结果返回设备真实MAC地址
/**
 * Start a BLE scan and return device results.
 *
 * @param { ScanOptions } options - Scan options.
 * @returns { Promise<Array<ScanResult>> } Scan results with device MAC addresses.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function startBLEScan(options: ScanOptions): Promise<Array<ScanResult>>;

interface ScanResult {
  deviceAddress: string;  // 问题：返回蓝牙设备真实MAC地址，可用于位置推算
  rssi: number;
  data: ArrayBuffer;
}

// 反例4：Public接口返回蜂窝基站信息
/**
 * Get cell information for the current network.
 *
 * @returns { CellInfo } Cell information.
 * @syscap SystemCapability.Telephony.CoreService
 * @since 10
 */
function getCellInfo(): CellInfo;

interface CellInfo {
  cellId: number;        // 问题：Cell ID 可用于位置推算
  lac: number;           // 问题：LAC 可用于位置推算
  mcc: string;           // 问题：MCC + MNC 可辅助定位
  mnc: string;
  signalStrength: number;
}

// 反例5：返回值对象嵌套包含BSSID字段
/**
 * Get the detailed network info.
 *
 * @returns { NetworkDetailInfo } Network detail info.
 * @syscap SystemCapability.Communication.NetManager.Core
 * @since 10
 */
function getNetworkDetailInfo(): NetworkDetailInfo;

interface NetworkDetailInfo {
  networkType: string;
  wifiInfo: {
    ssid: string;
    mac: string;          // 问题：WiFi MAC地址（等同于BSSID）可推算位置
    rssi: number;
  };
  isAvailable: boolean;
}

// 反例6：回调参数中泄露位置信息
/**
 * Subscribe to WiFi connection state changes.
 *
 * @param { string } type - Event type.
 * @param { Callback<WifiLinkedInfo> } callback - Callback with connected WiFi info.
 * @syscap SystemCapability.Communication.WiFi.STA
 * @since 6
 */
function on(type: string, callback: Callback<WifiLinkedInfo>): void;

interface WifiLinkedInfo {
  ssid: string;
  bssid: string;       // 问题：即使是通过回调返回，BSSID也不应在Public接口中暴露
  rssi: number;
}
