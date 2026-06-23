// Eval file for rule: 接口实现抛出异常或C接口返回错误码时，实际返回的错误码和定义一致
// 反例1：实现中返回了错误码13900001，但接口声明中只声明了错误码13900002，未声明13900001
/**
 * @brief Reads a file and returns its contents.
 *
 * @param filePath Path of the file to read.
 * @param buffer Output buffer to store file contents.
 * @param bufferSize Size of the output buffer.
 * @param bytesRead Output number of bytes actually read.
 * @return Returns 0 on success.
 * @retval ERR_FILE_NOT_FOUND(13900002) The file does not exist.
 * @since 9
 */
int ReadFile(const char* filePath, uint8_t* buffer, size_t bufferSize, size_t* bytesRead);

int ReadFile(const char* filePath, uint8_t* buffer, size_t bufferSize, size_t* bytesRead) {
    if (!CheckFileExists(filePath)) {
        return ERR_FILE_NOT_FOUND;  // OK: declared
    }

    if (!CheckReadPermission(filePath)) {
        // 问题：返回了 ERR_NO_PERMISSION(13900001)，但接口声明中未声明该错误码
        return ERR_NO_PERMISSION;
    }

    return DoReadFile(filePath, buffer, bufferSize, bytesRead);
}

// 反例2：实现中返回了声明的错误码13900002，但场景不匹配
/**
 * @brief Reads a file and returns its contents.
 *
 * @param filePath Path of the file to read.
 * @param buffer Output buffer to store file contents.
 * @param bufferSize Size of the output buffer.
 * @param bytesRead Output number of bytes actually read.
 * @return Returns 0 on success.
 * @retval ERR_FILE_NOT_FOUND(13900002) The file does not exist.
 * @since 9
 */
int ReadFileBad(const char* filePath, uint8_t* buffer, size_t bufferSize, size_t* bytesRead);

int ReadFileBad(const char* filePath, uint8_t* buffer, size_t bufferSize, size_t* bytesRead) {
    if (!CheckReadPermission(filePath)) {
        // 问题：实际场景是"无读权限"，但返回了 ERR_FILE_NOT_FOUND(文件不存在)，场景不匹配
        return ERR_FILE_NOT_FOUND;
    }

    return DoReadFile(filePath, buffer, bufferSize, bytesRead);
}

// 反例3：对参数做了业务逻辑校验（取值范围），却使用了401错误码
/**
 * @brief Sets the audio volume.
 *
 * @param volume Volume level to set.
 * @return Returns 0 on success.
 * @since 10
 */
int SetVolume(int volume);

int SetVolume(int volume) {
    if (volume < 0 || volume > 100) {
        // 问题：取值范围校验属于业务逻辑校验，不应该使用401错误码
        // 应该使用自定义业务错误码
        return ERR_INVALID_PARAM;  // 401
    }

    return DoSetVolume(volume);
}

// 反例4：抛出的错误码为空
int SetVolumeEmpty(int volume) {
    if (volume < 0 || volume > 100) {
        // 问题：错误码为空，无法定位问题
        return -1;  // 无具体错误码
    }

    return DoSetVolume(volume);
}
