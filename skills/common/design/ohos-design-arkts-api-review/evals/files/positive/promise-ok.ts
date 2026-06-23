// Eval file for rule: Promise 方式的异步方法禁止通过 Promise 的 then 方法中 resolve 函数返回方法执行失败
// 正例1：Promise resolve 仅返回成功时的业务数据，失败通过 reject 返回
/**
 * Renames the file from oldPath to newPath.
 * @param {string} oldPath - Old path.
 * @param {string} newPath - New path.
 * @throws {BusinessError} 401 - if oldPath or newPath is not a valid path.
 * @throws {BusinessError} 2020001 - if rename failed.
 * @returns {Promise<void>} Promise that resolves when rename succeeds.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function rename(oldPath: string, newPath: string): Promise<void>;

// 使用示例：
rename(oldPath, newPath).then(() => {
  console.log('Rename successful');
}).catch((err: BusinessError) => {
  console.error('Rename failed:', err.code, err.message);
});

// 正例2：返回具体业务数据，失败通过 reject
/**
 * Creates a new file.
 * @param {string} path - File path.
 * @param {string} content - File content.
 * @throws {BusinessError} 401 - if parameter is invalid.
 * @throws {BusinessError} 2020001 - if create failed.
 * @returns {Promise<number>} Promise that resolves to file size when create succeeds.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 7
 */
declare function createFile(path: string, content: string): Promise<number>;

// 正例3：返回复杂业务对象，失败通过 reject
/**
 * Reads user information.
 * @param {string} userId - User ID.
 * @throws {BusinessError} 401 - if userId is invalid.
 * @throws {BusinessError} 2010001 - if user not found.
 * @returns {Promise<User>} Promise that resolves to user info when read succeeds.
 * @syscap SystemCapability.UserAccount.User
 * @since 8
 */
declare function getUserInfo(userId: string): Promise<User>;

// 正例4：返回数组，失败通过 reject
/**
 * Queries all contacts.
 * @throws {BusinessError} 401 - if permission denied.
 * @throws {BusinessError} 2020001 - if query failed.
 * @returns {Promise<Contact[]>} Promise that resolves to contact list when query succeeds.
 * @syscap SystemCapability.Contacts.Contact
 * @since 7
 */
declare function queryContacts(): Promise<Contact[]>;

// 正例5：返回可选结果（业务上的无结果），失败仍通过 reject
/**
 * Searches for a file by name.
 * @param {string} fileName - File name to search.
 * @throws {BusinessError} 401 - if fileName is invalid.
 * @throws {BusinessError} 2020001 - if search operation failed.
 * @returns {Promise<string | null>} Promise that resolves to file path when found, null when not found.
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 8
 */
declare function searchFile(fileName: string): Promise<string | null>;
