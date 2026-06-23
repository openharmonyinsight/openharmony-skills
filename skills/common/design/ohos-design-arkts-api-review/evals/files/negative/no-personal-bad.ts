// Eval file for rule: Public接口禁止返回个人敏感数据
// 反例1：Public接口返回设备序列号SN
/**
 * Obtains the device serial number.
 *
 * @returns { string } Device serial number.
 * @syscap SystemCapability.Startup.SystemInfo.Core
 * @since 6
 */
function getSerialNumber(): string;

// 反例2：设备信息接口包含MEID
/**
 * Obtains device information.
 *
 * @returns { DeviceInfo } Device information.
 * @syscap SystemCapability.Startup.SystemInfo.Core
 * @since 6
 */
function getDeviceInfo(): DeviceInfo;

interface DeviceInfo {
  deviceType: string;
  manufacture: string;
  brand: string;
  meid: string;          // 问题：Public接口返回MEID，可唯一标识设备
  marketName: string;
}

// 反例3：Public接口返回手机号
/**
 * Obtains the phone number of the SIM card.
 *
 * @returns { string } Phone number.
 * @syscap SystemCapability.Telephony.CoreService
 * @since 6
 */
function getPhoneNumber(): string;

// 反例4：Public接口返回MAC地址（设备网卡MAC）
/**
 * Obtains the device MAC address.
 *
 * @returns { string } Device MAC address.
 * @syscap SystemCapability.Communication.NetManager.Core
 * @since 6
 */
function getMacAddress(): string;

// 反例5：Public接口返回IMSI
/**
 * Obtains the IMSI of the SIM card.
 *
 * @returns { string } IMSI string.
 * @syscap SystemCapability.Telephony.CoreService
 * @since 6
 */
function getIMSI(): string;

// 反例6：SIM卡信息接口返回ICCID
/**
 * Obtains the SIM card information.
 *
 * @returns { SimInfo } SIM card information.
 * @syscap SystemCapability.Telephony.CoreService
 * @since 10
 */
function getSimInfo(): SimInfo;

interface SimInfo {
  operatorName: string;
  iccid: string;         // 问题：ICCID（SIM卡序列号）可唯一标识用户
  isReady: boolean;
}

// 反例7：返回对象中嵌套包含设备唯一标识
/**
 * Get the full system information.
 *
 * @returns { SystemInfo } System information.
 * @syscap SystemCapability.Startup.SystemInfo.Core
 * @since 10
 */
function getSystemInfo(): SystemInfo;

interface SystemInfo {
  deviceName: string;
  osVersion: string;
  hardwareInfo: {
    model: string;
    serial: string;      // 问题：嵌套对象中包含设备序列号
    mac: string;         // 问题：嵌套对象中包含MAC地址
  };
}

// 反例8：回调参数中泄露手机号
/**
 * Subscribe to call state changes.
 *
 * @param { string } type - Event type.
 * @param { Callback<CallStateInfo> } callback - Callback.
 * @syscap SystemCapability.Telephony.CallManager
 * @since 6
 */
function on(type: string, callback: Callback<CallStateInfo>): void;

interface CallStateInfo {
  state: number;
  phoneNumber: string;   // 问题：回调参数中返回来电/去电手机号
}
