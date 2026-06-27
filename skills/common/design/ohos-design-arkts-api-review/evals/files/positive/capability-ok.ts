// Eval file for rule: 针对一系列关联接口或特性是否支持，提供能力查询接口
// 正例1：POI服务提供了能力查询接口，开发者可先查询后使用
/**
 * Check whether the POI service is supported.
 *
 * @returns { boolean } True if the POI service is supported.
 * @syscap SystemCapability.Location.Location.Core
 * @since 12
 */
function isPoiServiceSupported(): boolean;

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

// 正例2：相机管理提供查询支持的相机列表
/**
 * Obtain the list of supported cameras.
 *
 * @returns { Array<CameraDevice> } Supported camera device list.
 * @syscap SystemCapability.Multimedia.Camera.Core
 * @since 10
 */
function getSupportedCameras(): Array<CameraDevice>;

/**
 * Create a camera input.
 *
 * @param { CameraDevice } camera - Camera device.
 * @returns { CameraInput } Camera input.
 * @throws { BusinessError } 801 - Capability not supported on this device.
 * @syscap SystemCapability.Multimedia.Camera.Core
 * @since 10
 */
function createCameraInput(camera: CameraDevice): CameraInput;

// 正例3：蓝牙提供能力查询接口
/**
 * Check whether Bluetooth LE is supported.
 *
 * @returns { boolean } True if Bluetooth LE is supported.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function isBLESupported(): boolean;

/**
 * Start a Bluetooth LE scan.
 *
 * @param { ScanOptions } options - Scan options.
 * @returns { Promise<void> }
 * @throws { BusinessError } 801 - Capability not supported.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function startBLEScan(options: ScanOptions): Promise<void>;

// 正例4：NFC提供能力查询（布尔值+列表两种查询方式配合使用）
/**
 * Check whether NFC is supported.
 *
 * @returns { boolean } True if NFC is supported.
 * @syscap SystemCapability.Communication.NFC.Core
 * @since 10
 */
function isNfcSupported(): boolean;

/**
 * Get the list of supported NFC tag technologies.
 *
 * @returns { Array<NfcTech> } Supported NFC technologies.
 * @syscap SystemCapability.Communication.NFC.Core
 * @since 10
 */
function getSupportedNfcTechs(): Array<NfcTech>;

// 正例5：传感器提供能力查询
/**
 * Check whether a specific sensor type is supported.
 *
 * @param { number } sensorId - Sensor type ID.
 * @returns { boolean } True if the sensor is supported.
 * @syscap SystemCapability.Sensor.Service
 * @since 10
 */
function isSensorSupported(sensorId: number): boolean;

/**
 * Subscribe to sensor data.
 *
 * @param { number } sensorId - Sensor type ID.
 * @param { SensorCallback } callback - Sensor data callback.
 * @throws { BusinessError } 801 - Capability not supported.
 * @syscap SystemCapability.Sensor.Service
 * @since 10
 */
function subscribeSensor(sensorId: number, callback: SensorCallback): void;

// 正例6：使用 canIUse 能力查询（通用能力查询方式）
/**
 * Check whether a specific SysCap is supported.
 *
 * @param { string } syscap - System capability name.
 * @returns { boolean } True if the capability is supported.
 * @syscap SystemCapability.Utils.Lang
 * @since 10
 */
function canIUse(syscap: string): boolean;
