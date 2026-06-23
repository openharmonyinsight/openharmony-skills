// Eval file for rule: 提供异常描述和异常处理建议
// 反例1：异常描述缺少Why要素，未说明错误原因
/**
 * Executes a Nearlink core operation
 *
 * @return { Promise<void> } Returns the promise object
 * @throws { BusinessError } 201 - Permission denied.
 * @syscap SystemCapability.Communication.Nearlink.Core
 * @since 23
 */
function executeNearLinkOperation(): Promise<void>;

// 反例2：异常描述过于宽泛，没有具体信息
/**
 * Gets the system status
 *
 * @return { Promise<SystemStatus> } Returns the system status
 * @throws { BusinessError } 100001 - Status is abnormal.
 * @throws { BusinessError } 100002 - Operation meets some error.
 * @syscap SystemCapability.Utils.Lang
 * @since 10
 */
function getSystemStatus(): Promise<SystemStatus>;

// 反例3：异常描述缺少处理建议
/**
 * Opens a file for reading
 *
 * @param { string } filePath - The file path
 * @return { Promise<File> } Returns the file handle
 * @throws { BusinessError } 13900001 - File not found. The specified file does not exist.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 10
 */
function openFile(filePath: string): Promise<File>;

// 反例4：异常描述缺少What要素
/**
 * Connects to a remote server
 *
 * @param { string } serverUrl - The server URL
 * @return { Promise<Connection> } Returns the connection
 * @throws { BusinessError } 2300001 - Due to network instability.
 * @syscap SystemCapability.Communication.NetStack
 * @since 8
 */
function connectToServer(serverUrl: string): Promise<Connection>;

// 反例5：多个接口使用完全相同的错误描述
/**
 * Reads data from Bluetooth device A
 *
 * @return { Promise<ArrayBuffer> } Returns the read data
 * @throws { BusinessError } 201 - Permission denied. The application lacks the `ohos.permission.ACCESS_BLUETOOTH` permission.
 *         Declare the permission in `module.json5` and ensure it has been granted by the user.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function readBluetoothDataA(): Promise<ArrayBuffer>;

/**
 * Writes data to Bluetooth device B
 *
 * @param { ArrayBuffer } data - The data to write
 * @return { Promise<number> } Returns the bytes written
 * @throws { BusinessError } 201 - Permission denied. The application lacks the `ohos.permission.ACCESS_BLUETOOTH` permission.
 *         Declare the permission in `module.json5` and ensure it has been granted by the user.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function writeBluetoothDataB(data: ArrayBuffer): Promise<number>;

// 反例6：处理建议不够具体，没有可操作性
/**
 * Creates a network connection
 *
 * @return { Promise<NetworkConnection> } Returns the connection
 * @throws { BusinessError } 2100001 - Connection failed. Network error occurred.
 *         Please fix the network issue.
 * @syscap SystemCapability.Communication.NetStack
 * @since 9
 */
function createNetworkConnection(): Promise<NetworkConnection>;

// 反例7：异常描述要素不完整，同时缺少处理建议
/**
 * Sends a message to a remote peer
 *
 * @param { string } message - The message to send
 * @return { Promise<void> } Returns the promise object
 * @throws { BusinessError } 3100001 - Failed.
 * @syscap SystemCapability.Communication.SoftBus.Core
 * @since 8
 */
function sendMessage(message: string): Promise<void>;

// 反例8：错误描述模糊，没有说明具体错误原因
/**
 * Configures the WiFi settings
 *
 * @param { WiFiConfig } config - The WiFi configuration
 * @return { Promise<void> } Returns the promise object
 * @throws { BusinessError } 2500001 - WiFi operation failed. Something went wrong.
 * @syscap SystemCapability.Communication.WiFi.Core
 * @since 10
 */
function configureWiFi(config: WiFiConfig): Promise<void>;

// 反例9：参数错误描述没有列出可能的具体原因
/**
 * Validates user input
 *
 * @param { string } input - The user input
 * @return { Promise<boolean> } Returns true if valid
 * @throws { BusinessError } 401 - Parameter error. Invalid parameter.
 *         Please check the parameter.
 * @syscap SystemCapability.Utils.Lang
 * @since 9
 */
function validateInput(input: string): Promise<boolean>;

// 反例10：缺少对超时错误的重试建议
/**
 * Downloads a file from a remote server
 *
 * @param { string } url - The download URL
 * @return { Promise<string> } Returns the local file path
 * @throws { BusinessError } 2200001 - Download failed. Connection timed out.
 * @syscap SystemCapability.MiscServices.Download
 * @since 8
 */
function downloadFile(url: string): Promise<string>;
