// Eval file for rule: 接口实现抛出异常或C接口返回错误码时，实际返回的错误码和定义一致
// 正例：接口声明了错误码，实现中返回该错误码，且场景匹配
/**
 * @brief Reads a file and returns its contents.
 *
 * @param filePath Path of the file to read.
 * @param buffer Output buffer to store file contents.
 * @param bufferSize Size of the output buffer.
 * @param bytesRead Output number of bytes actually read.
 * @return Returns 0 on success.
 * @retval 0 Success
 * @retval ERR_NO_PERMISSION(13900001) No read permission on the file.
 * @retval ERR_FILE_NOT_FOUND(13900002) The file does not exist.
 * @since 9
 */
int ReadFile(const char* filePath, uint8_t* buffer, size_t bufferSize, size_t* bytesRead);

// Implementation example: error codes match declarations
int ReadFile(const char* filePath, uint8_t* buffer, size_t bufferSize, size_t* bytesRead) {
    if (!CheckFileExists(filePath)) {
        // OK: ERR_FILE_NOT_FOUND matches declared error code 13900002
        return ERR_FILE_NOT_FOUND;
    }

    if (!CheckReadPermission(filePath)) {
        // OK: ERR_NO_PERMISSION matches declared error code 13900001
        return ERR_NO_PERMISSION;
    }

    return DoReadFile(filePath, buffer, bufferSize, bytesRead);
}

// 正例2：C接口返回错误码与声明一致
/**
 * @brief Opens a database connection.
 *
 * @param dbPath Path to the database file.
 * @param handle Output database handle.
 * @return Returns 0 on success.
 * @retval 0 Success
 * @retval ERR_INVALID_PARAM Parameter error.
 * @retval ERR_NOT_FOUND Database file not found.
 * @retval ERR_NO_PERMISSION Permission denied.
 * @since 10
 */
int OpenDatabase(const char* dbPath, DatabaseHandle* handle);

int OpenDatabase(const char* dbPath, DatabaseHandle* handle) {
    if (dbPath == NULL || handle == NULL) {
        // OK: parameter validation uses declared error code
        return ERR_INVALID_PARAM;
    }

    if (!FileExists(dbPath)) {
        // OK: file not found uses declared error code
        return ERR_NOT_FOUND;
    }

    if (!HasPermission(dbPath)) {
        // OK: permission error uses declared error code
        return ERR_NO_PERMISSION;
    }

    return DoOpen(dbPath, handle);
}
