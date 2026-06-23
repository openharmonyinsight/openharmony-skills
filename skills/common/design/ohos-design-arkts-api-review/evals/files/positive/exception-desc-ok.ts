// Eval file for rule: 提供异常描述和异常处理建议
// 正例1：异常描述包含What和Why两个核心要素，并提供处理建议
/**
 * Executes a Nearlink core operation
 *
 * @return { Promise<void> } Returns the promise object
 * @throws { BusinessError } 201 - Permission denied. The application lacks the `ohos.permission.ACCESS_NEARLINK` permission.
 *         Ensure the permission is declared in the `module.json5` file.
 * @syscap SystemCapability.Communication.Nearlink.Core
 * @since 23
 */
function executeNearLinkOperation(): Promise<void>;

// 正例2：异常描述完整，What明确，Why具体，提供处理建议
/**
 * Opens a file for reading or writing
 *
 * @param { string } filePath - The path to the file to open
 * @return { Promise<File> } Returns the file handle
 * @throws { BusinessError } 401 - Parameter error. The file path is invalid or empty.
 *         Please check if the filePath parameter is a valid non-empty string.
 * @throws { BusinessError } 13900001 - File not found. The specified file does not exist in the given path.
 *         Please verify the file path and ensure the file exists.
 * @throws { BusinessError } 13900002 - Permission denied. The application does not have read/write permission for this file.
 *         Request the required permissions from the user or check if the file is read-only.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 10
 */
function openFile(filePath: string): Promise<File>;

// 正例3：错误类型和原因完全对应时，只描述What
/**
 * Checks if the device supports NFC
 *
 * @return { Promise<boolean> } Returns true if NFC is supported, false otherwise
 * @throws { BusinessError } 801 - Capability not supported. This device does not support NFC functionality.
 * @syscap SystemCapability.Communication.NFC.Core
 * @since 8
 */
function isNfcSupported(): Promise<boolean>;

// 正例4：提供具体的错误原因和可操作的处理建议
/**
 * Establishes a Bluetooth connection
 *
 * @param { string } deviceId - The target device identifier
 * @return { Promise<void> } Returns the promise object
 * @throws { BusinessError } 2900001 - Bluetooth disabled. Bluetooth is currently turned off on this device.
 *         Please call enableBluetooth() to enable Bluetooth before attempting connection.
 * @throws { BusinessError } 2900099 - Operation failed. The connection attempt timed out or the target device is out of range.
 *         Ensure the target device is powered on, within range, and try again. If the problem persists, restart Bluetooth.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function connectBluetooth(deviceId: string): Promise<void>;

// 正例5：相同错误码在不同接口有共性但描述更具体
/**
 * Writes data to a connected Bluetooth device
 *
 * @param { ArrayBuffer } data - The data to write
 * @return { Promise<number> } Returns the number of bytes written
 * @throws { BusinessError } 201 - Permission denied. The application lacks the `ohos.permission.ACCESS_BLUETOOTH` permission.
 *         Add the permission declaration in `module.json5` and request user authorization.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function writeBluetoothData(data: ArrayBuffer): Promise<number>;

// 正例6：相同错误码在不同接口有共性但描述更具体
/**
 * Reads data from a connected Bluetooth device
 *
 * @return { Promise<ArrayBuffer> } Returns the read data
 * @throws { BusinessError } 201 - Permission denied. The application lacks the `ohos.permission.ACCESS_BLUETOOTH` permission.
 *         Declare the permission in `module.json5` and ensure it has been granted by the user.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function readBluetoothData(): Promise<ArrayBuffer>;

// 正例7：为非开发者问题导致的错误提供重启建议
/**
 * Initializes the media playback engine
 *
 * @return { Promise<void> } Returns the promise object
 * @throws { BusinessError } 5400101 - Media engine initialization failed. The media service encountered an internal error.
 *         Please release unused resources and try again. If the problem persists, consider restarting the application.
 * @throws { BusinessError } 5400102 - Codec not supported. The device does not have a hardware decoder for this media format.
 *         Use a supported media format or install the necessary codec pack.
 * @syscap SystemCapability.Multimedia.Media.Core
 * @since 10
 */
function initMediaEngine(): Promise<void>;

// 正例8：参数校验错误提供具体的参数检查建议
/**
 * Creates a database connection
 *
 * @param { DatabaseConfig } config - The database configuration
 * @return { Promise<Database> } Returns the database connection
 * @throws { BusinessError } 401 - Parameter error. Possible causes: 1. Database name exceeds 128 characters;
 *         2. Invalid port number (must be 1-65535); 3. Username or password contains special characters.
 *         Please check the DatabaseConfig parameters and ensure all values are within valid ranges.
 * @throws { BusinessError } 14800000 - Connection failed. The database server is unreachable or the credentials are incorrect.
 *         Verify the server address and port, check network connectivity, and confirm the username and password.
 * @syscap SystemCapability.DistributedDataManager.RelationalStore.Core
 * @since 9
 */
function createDatabase(config: DatabaseConfig): Promise<Database>;

// 正例9：提供资源释放建议
/**
 * Allocates a large memory buffer
 *
 * @param { number } size - The buffer size in bytes
 * @return { Promise<ArrayBuffer> } Returns the allocated buffer
 * @throws { BusinessError } 1900001 - Memory allocation failed. Insufficient system memory available.
 *         Release unused memory buffers and cached data, then retry the operation.
 * @syscap SystemCapability.Utils.Lang
 * @since 8
 */
function allocateBuffer(size: number): Promise<ArrayBuffer>;

// 正例10：业务场景错误提供使用约束检查建议
/**
 * Starts a foreground service
 *
 * @param { ForegroundServiceConfig } config - The service configuration
 * @return { Promise<void> } Returns the promise object
 * @throws { BusinessError } 16000001 - Service start failed. The service has already been started.
 *         Check if the service is already running before calling start again, or call stopService() first.
 * @throws { BusinessError } 16000002 - Service start failed. The maximum number of foreground services (3) has been reached.
 *         Stop an existing foreground service before starting a new one.
 * @syscap SystemCapability.Ability.AbilityRuntime.Core
 * @since 9
 */
function startForegroundService(config: ForegroundServiceConfig): Promise<void>;
