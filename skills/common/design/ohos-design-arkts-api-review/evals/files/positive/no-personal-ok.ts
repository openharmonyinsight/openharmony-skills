// Eval file for rule: Public接口禁止返回个人敏感数据
// 正例1：设备信息接口不返回SN、MEID等唯一标识
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
  marketName: string;
  osFullName: string;
  displayVersion: string;
  // 不包含 serial、meid、deviceId 等唯一标识字段
}

// 正例2：SIM卡信息只返回运营商名称，不返回IMSI或ICCID
/**
 * Obtains the SIM operator name.
 *
 * @returns { string } SIM operator name.
 * @syscap SystemCapability.Telephony.CoreService
 * @since 6
 */
function getSimOperatorName(): string;

// 正例3：网络信息不返回MAC地址
/**
 * Obtains the current network type.
 *
 * @returns { string } Network type, e.g., "WiFi", "LTE".
 * @syscap SystemCapability.Communication.NetManager.Core
 * @since 6
 */
function getNetworkType(): string;

// 正例4：电话相关接口通过系统接口+权限控制开放（经过TMG评审）
/**
 * Obtains the phone number of the SIM card.
 *
 * @permission ohos.permission.GET_PHONE_NUMBERS
 * @returns { string } Phone number.
 * @syscap SystemCapability.Telephony.CoreService
 * @systemapi
 * @since 10
 */
function getPhoneNumber(): string;

// 正例5：使用应用级标识符替代设备级标识符
/**
 * Get an application-scoped anonymous device identifier.
 *
 * @returns { string } Anonymous device identifier scoped to the calling application.
 * @syscap SystemCapability.DeviceAuthentication.DeviceAuthentication
 * @since 12
 */
function getAppAnonymousId(): string;
