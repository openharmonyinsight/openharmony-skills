// Eval file for rule: 针对一系列关联接口或特性是否支持，提供能力查询接口
// 反例1：POI服务接口没有提供能力查询接口，开发者无法提前判断设备是否支持
/**
 * Obtain POI information near the current location.
 *
 * @param { PoiRequest } request - POI query request.
 * @returns { Promise<Array<PoiInfo>> } POI information list.
 * @throws { BusinessError } 801 - Capability not supported.
 * @syscap SystemCapability.Location.Location.Core
 * @since 12
 */
function getPoiInfo(request: PoiRequest): Promise<Array<PoiInfo>>;
// 问题：缺少 isPoiServiceSupported() 查询接口


// 反例2：能力查询接口命名不规范
/**
 * Check whether Bluetooth LE is supported.
 *
 * @returns { boolean } True if Bluetooth LE is supported.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function checkBLESupport(): boolean;
// 问题：布尔值能力查询接口应命名为 isXXXSupported，而非 checkXXXSupport

// 反例3：返回列表的能力查询接口命名不规范
/**
 * Get supported camera list.
 *
 * @returns { Array<CameraDevice> } Supported camera devices.
 * @syscap SystemCapability.Multimedia.Camera.Core
 * @since 10
 */
function queryCameras(): Array<CameraDevice>;
// 问题：返回列表的接口应命名为 getSupportedXXX（如 getSupportedCameras），而非 queryCameras
