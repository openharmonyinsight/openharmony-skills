// Eval file for rule: Promise 方式的异步方法禁止通过 Promise 的 then 方法中 resolve 函数返回方法执行失败
// 反例1：通过返回布尔值表示执行是否成功
/**
 * Renames the file from oldPath to newPath.
 * @param {string} oldPath - Old path.
 * @param {string} newPath - New path.
 * @throws {BusinessError} 401 - if oldPath or newPath is not a valid path.
 * @returns {Promise<boolean>} Rename result. true means rename successfully, false means rename failed.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function rename(oldPath: string, newPath: string): Promise<boolean>;

// 使用时需要判断 resolve 的返回值来区分成功/失败，这是错误的设计
rename(oldPath, newPath).then((success: boolean) => {
  if (success) {
    console.log('Rename successful');
  } else {
    console.error('Rename failed'); // 应该在 catch 中处理
  }
});

// 反例2：通过返回包含 success 字段的对象表示执行是否成功
/**
 * Deletes a file.
 * @param {string} path - File path.
 * @throws {BusinessError} 401 - if path is invalid.
 * @returns {Promise<{ success: boolean; error?: string }>} Delete result.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function deleteFile(path: string): Promise<{ success: boolean; error?: string }>;

// 反例3：通过返回 null 或 undefined 表示执行失败
/**
 * Reads a file.
 * @param {string} path - File path.
 * @throws {BusinessError} 401 - if path is invalid.
 * @returns {Promise<string | null>} File content, null if read failed.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function readFile(path: string): Promise<string | null>;

// 反例4：通过返回错误码表示执行失败
/**
 * Copies a file.
 * @param {string} srcPath - Source path.
 * @param {string} destPath - Destination path.
 * @throws {BusinessError} 401 - if path is invalid.
 * @returns {Promise<number>} 0 means success, negative means failed.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function copyFile(srcPath: string, destPath: string): Promise<number>;

// 反例5：混合返回类型表示不同的错误情况
/**
 * Creates a directory.
 * @param {string} path - Directory path.
 * @throws {BusinessError} 401 - if path is invalid.
 * @returns {Promise<boolean | Error>} true if success, Error if failed.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function mkdir(path: string): Promise<boolean | Error>;
