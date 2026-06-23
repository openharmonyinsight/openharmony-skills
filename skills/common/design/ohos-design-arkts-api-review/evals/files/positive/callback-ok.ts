// Eval file for rule: Callback方式的异步方法禁止通过Callback回调函数中的第二个参数返回方法执行是否成功
// 正例1：文件重命名通过第一个参数error返回失败，无业务数据返回时使用 AsyncCallback<void>
/**
 * Renames the file from oldPath to newPath.
 *
 * @param { string } oldPath - Old file path.
 * @param { string } newPath - New file path.
 * @param { AsyncCallback<void> } callback - Callback used to return the result.
 * @throws { BusinessError } 401 - Parameter error. Possible causes:
 * <br>1. Mandatory parameters are left unspecified.
 * <br>2. Incorrect parameter types.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function rename(oldPath: string, newPath: string, callback: AsyncCallback<void>): void;

// 正例2：通过error返回失败，业务数据通过第二个参数返回
/**
 * Read data from the file.
 *
 * @param { number } fd - File descriptor.
 * @param { AsyncCallback<ArrayBuffer> } callback - Callback used to return the result.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function read(fd: number, callback: AsyncCallback<ArrayBuffer>): void;

// 正例3：无业务返回值时使用 AsyncCallback<void>
/**
 * Close the file.
 *
 * @param { number } fd - File descriptor.
 * @param { AsyncCallback<void> } callback - Callback used to return the result.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function close(fd: number, callback: AsyncCallback<void>): void;

// 正例4：boolean表示业务结果（非执行状态），属于合规用法
/**
 * Check whether the file exists.
 *
 * @param { string } path - File path.
 * @param { AsyncCallback<boolean> } callback - Callback used to return whether the file exists.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function access(path: string, callback: AsyncCallback<boolean>): void;
// 注：此处的 boolean 表示"文件是否存在"这个业务查询结果，而非"接口执行是否成功"

// 正例5：boolean表示功能是否启用，属于合规用法
/**
 * Check whether the network interface is enabled.
 *
 * @param { string } iface - Network interface name.
 * @param { AsyncCallback<boolean> } callback - Callback used to return whether the interface is enabled.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.Communication.NetManager.Core
 * @since 10
 */
declare function isInterfaceEnabled(iface: string, callback: AsyncCallback<boolean>): void;
// 注：此处的 boolean 表示"网络接口是否启用"这个业务查询结果，而非"接口执行是否成功"

// 正例6：通过Promise方式不返回boolean状态，错误通过reject返回
/**
 * Renames the file from oldPath to newPath.
 *
 * @param { string } oldPath - Old file path.
 * @param { string } newPath - New file path.
 * @returns { Promise<void> }
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function rename(oldPath: string, newPath: string): Promise<void>;
