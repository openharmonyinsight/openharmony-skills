// Eval file for rule: 约束限制合理
// 正例1：文件名约束符合行业惯例，允许常见的文件名字符
/**
 * Save content to a file.
 *
 * @param { string } fileName - Name of the file. Supports common characters including letters, digits, hyphens, and underscores.
 * @param { string } content - Content to write.
 * @returns { Promise<void> }
 * @throws { BusinessError } 401 - Parameter error. Possible causes:
 * <br>1. Mandatory parameters are left unspecified.
 * <br>2. Incorrect parameter types.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 10
 */
function saveFile(fileName: string, content: string): Promise<void>;

// 正例2：图片上传大小限制合理，满足大多数业务场景
/**
 * Upload an image to the server.
 *
 * @param { string } uri - Image URI.
 * @param { ImageUploadOptions } options - Upload options.
 * @returns { Promise<UploadResult> } Upload result.
 * @syscap SystemCapability.Multimedia.Image
 * @since 12
 */
function uploadImage(uri: string, options?: ImageUploadOptions): Promise<UploadResult>;

// 正例3：约束条件数量适中（2条），每条都有明确的技术必要性
/**
 * Connect to a Bluetooth device.
 *
 * @param { string } deviceId - Device ID, in MAC address format (e.g., "XX:XX:XX:XX:XX:XX").
 * @param { ConnectOptions } options - Connection options.
 * @returns { Promise<void> }
 * @throws { BusinessError } 401 - Parameter error. Mandatory parameters are left unspecified.
 * @throws { BusinessError } 2900001 - Bluetooth is disabled.
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
function connect(deviceId: string, options?: ConnectOptions): Promise<void>;

// 正例4：参数约束合理，不过度限制合法需求
/**
 * Set the window brightness.
 *
 * @param { number } brightness - Window brightness. The value ranges from 0 to 1.
 * @syscap SystemCapability.WindowManager.WindowManager.Core
 * @since 9
 */
setBrightness(brightness: number): void;
