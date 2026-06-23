// Eval file for rule: Callback方式的异步方法禁止通过Callback回调函数中的第二个参数返回方法执行是否成功
// 反例1：通过第二个参数boolean返回执行是否成功
/**
 * Renames the file from oldPath to newPath.
 *
 * @param { string } oldPath - Old file path.
 * @param { string } newPath - New file path.
 * @param { AsyncCallback<boolean> } callback - The callback of rename result,
 *   true means rename successfully, false means rename failed.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function rename(oldPath: string, newPath: string, callback: AsyncCallback<boolean>): void;
// 问题：AsyncCallback<boolean> 用于表示"成功/失败"，应用 AsyncCallback<void> + error 代替

// 反例2：删除操作通过第二个参数boolean返回执行是否成功
/**
 * Delete a file.
 *
 * @param { string } path - File path.
 * @param { AsyncCallback<boolean> } callback - The callback of delete result,
 *   true means delete successfully, false means delete failed.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function unlink(path: string, callback: AsyncCallback<boolean>): void;
// 问题：删除操作无业务返回数据，boolean用于表示执行状态，应使用 AsyncCallback<void>

// 反例3：写入操作通过第二个参数boolean返回执行是否成功
/**
 * Write data to the file.
 *
 * @param { number } fd - File descriptor.
 * @param { ArrayBuffer } data - Data to write.
 * @param { AsyncCallback<boolean> } callback - Callback used to return the result.
 *   true means write successfully, false means write failed.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function write(fd: number, data: ArrayBuffer, callback: AsyncCallback<boolean>): void;
// 问题：boolean用于表示"写入是否成功"，应使用 AsyncCallback<void>，失败时通过error返回

// 反例4：创建目录通过第二个参数boolean返回执行是否成功
/**
 * Create a directory.
 *
 * @param { string } path - Directory path.
 * @param { AsyncCallback<boolean> } callback - The callback of mkdir result.
 *   Returns true if the directory is created successfully, false otherwise.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function mkdir(path: string, callback: AsyncCallback<boolean>): void;
// 问题：boolean用于表示"创建是否成功"，应使用 AsyncCallback<void>

// 反例5：连接操作通过第二个参数boolean返回执行是否成功
/**
 * Connect to the server.
 *
 * @param { string } host - Server host.
 * @param { number } port - Server port.
 * @param { AsyncCallback<boolean> } callback - Callback used to return the connect result.
 *   true means connected, false means connection failed.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.Communication.NetStack
 * @since 10
 */
declare function connect(host: string, port: number, callback: AsyncCallback<boolean>): void;
// 问题：boolean用于表示"连接是否成功"，应使用 AsyncCallback<void>，连接失败通过error返回

// 反例6：注释描述中暗示第二个参数表示成功/失败
/**
 * Copy a file.
 *
 * @param { string } srcPath - Source file path.
 * @param { string } destPath - Destination file path.
 * @param { AsyncCallback<boolean> } callback - Callback invoked upon completion.
 *   If the copy is successful, the boolean parameter is true; otherwise, it is false.
 * @throws { BusinessError } 401 - Parameter error.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function copyFile(srcPath: string, destPath: string, callback: AsyncCallback<boolean>): void;
// 问题：虽然注释措辞不同，但boolean仍然表示"操作是否成功"，应使用 AsyncCallback<void>
