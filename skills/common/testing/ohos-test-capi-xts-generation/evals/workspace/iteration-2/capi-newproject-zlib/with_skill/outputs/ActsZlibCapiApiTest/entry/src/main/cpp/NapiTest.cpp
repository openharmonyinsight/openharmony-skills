/*
 * Copyright (C) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "napi/native_api.h"
#include <cstdlib>
#include <cstring>
#include <zlib.h>

static bool GetArrayBufferData(napi_env env, napi_value arrayBuffer, void **data, size_t *byteLength)
{
    void *bufferData = nullptr;
    napi_status status = napi_get_arraybuffer_info(env, arrayBuffer, &bufferData, byteLength);
    if (status != napi_ok || bufferData == nullptr) {
        return false;
    }
    *data = bufferData;
    return true;
}

static napi_value CreateArrayBufferCopy(napi_env env, void *data, size_t length)
{
    napi_value result;
    void *buffer = nullptr;
    napi_status status = napi_create_arraybuffer(env, length, &buffer, &result);
    if (status != napi_ok || buffer == nullptr) {
        return nullptr;
    }
    if (length > 0 && data != nullptr) {
        memcpy(buffer, data, length);
    }
    return result;
}

/**
 * @tc.name: SUB_ZLIB_Compress_PARAM_001
 * @tc.desc: 测试 compress 函数，正常数据压缩
 * @tc.type: FUNC
 */
static napi_value CompressNormalData(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected ArrayBuffer.");
        return nullptr;
    }

    bool isArrayBuffer = false;
    status = napi_is_arraybuffer(env, args[0], &isArrayBuffer);
    if (status != napi_ok || !isArrayBuffer) {
        napi_throw_error(env, nullptr, "Argument must be an ArrayBuffer");
        return nullptr;
    }

    void *sourceData = nullptr;
    size_t sourceLen = 0;
    if (!GetArrayBufferData(env, args[0], &sourceData, &sourceLen)) {
        napi_throw_error(env, nullptr, "Failed to get source buffer data");
        return nullptr;
    }

    uLong compressedLen = compressBound(sourceLen);
    Bytef *compressed = (Bytef *)malloc(compressedLen);
    if (compressed == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed for compressed data");
        return nullptr;
    }

    int ret = compress(compressed, &compressedLen, (const Bytef *)sourceData, sourceLen);

    napi_value result;
    if (ret == Z_OK) {
        result = CreateArrayBufferCopy(env, compressed, compressedLen);
    } else {
        free(compressed);
        napi_throw_error(env, nullptr, "Compression failed");
        return nullptr;
    }

    free(compressed);
    return result;
}

/**
 * @tc.name: SUB_ZLIB_Compress_PARAM_002
 * @tc.desc: 测试 compress 函数，空数据压缩
 * @tc.type: FUNC
 */
static napi_value CompressEmptyData(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected ArrayBuffer.");
        return nullptr;
    }

    bool isArrayBuffer = false;
    status = napi_is_arraybuffer(env, args[0], &isArrayBuffer);
    if (status != napi_ok || !isArrayBuffer) {
        napi_throw_error(env, nullptr, "Argument must be an ArrayBuffer");
        return nullptr;
    }

    void *sourceData = nullptr;
    size_t sourceLen = 0;
    if (!GetArrayBufferData(env, args[0], &sourceData, &sourceLen)) {
        napi_throw_error(env, nullptr, "Failed to get source buffer data");
        return nullptr;
    }

    uLong compressedLen = compressBound(sourceLen);
    Bytef *compressed = (Bytef *)malloc(compressedLen);
    if (compressed == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed for compressed data");
        return nullptr;
    }

    int ret = compress(compressed, &compressedLen, (const Bytef *)sourceData, sourceLen);

    napi_value result;
    if (ret == Z_OK) {
        result = CreateArrayBufferCopy(env, compressed, compressedLen);
    } else {
        free(compressed);
        napi_throw_error(env, nullptr, "Compression failed");
        return nullptr;
    }

    free(compressed);
    return result;
}

/**
 * @tc.name: SUB_ZLIB_Compress_ERROR_001
 * @tc.desc: 测试 compress 函数，输出缓冲区不足
 * @tc.type: FUNC
 */
static napi_value CompressBufError(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected ArrayBuffer.");
        return nullptr;
    }

    bool isArrayBuffer = false;
    status = napi_is_arraybuffer(env, args[0], &isArrayBuffer);
    if (status != napi_ok || !isArrayBuffer) {
        napi_throw_error(env, nullptr, "Argument must be an ArrayBuffer");
        return nullptr;
    }

    void *sourceData = nullptr;
    size_t sourceLen = 0;
    if (!GetArrayBufferData(env, args[0], &sourceData, &sourceLen)) {
        napi_throw_error(env, nullptr, "Failed to get source buffer data");
        return nullptr;
    }

    uLong compressedLen = 1;
    Bytef *compressed = (Bytef *)malloc(compressedLen);
    if (compressed == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = compress(compressed, &compressedLen, (const Bytef *)sourceData, sourceLen);
    free(compressed);

    if (ret == Z_BUF_ERROR) {
        napi_throw_error(env, "-5", "Z_BUF_ERROR: output buffer too small");
        return nullptr;
    }

    napi_value napiResult;
    napi_create_int32(env, ret, &napiResult);
    return napiResult;
}

/**
 * @tc.name: SUB_ZLIB_Uncompress_PARAM_001
 * @tc.desc: 测试 uncompress 函数，正常数据解压缩往返测试
 * @tc.type: FUNC
 */
static napi_value UncompressRoundTrip(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 2) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected (ArrayBuffer, number).");
        return nullptr;
    }

    bool isArrayBuffer = false;
    status = napi_is_arraybuffer(env, args[0], &isArrayBuffer);
    if (status != napi_ok || !isArrayBuffer) {
        napi_throw_error(env, nullptr, "First argument must be an ArrayBuffer");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[1], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Second argument must be a number (original length)");
        return nullptr;
    }

    int64_t originalLen = 0;
    status = napi_get_value_int64(env, args[1], &originalLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get original length");
        return nullptr;
    }

    void *compressedData = nullptr;
    size_t compressedLen = 0;
    if (!GetArrayBufferData(env, args[0], &compressedData, &compressedLen)) {
        napi_throw_error(env, nullptr, "Failed to get compressed buffer data");
        return nullptr;
    }

    uLongf destLen = (uLongf)originalLen;
    Bytef *decompressed = (Bytef *)malloc(destLen);
    if (decompressed == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed for decompressed data");
        return nullptr;
    }

    int ret = uncompress(decompressed, &destLen, (const Bytef *)compressedData, compressedLen);

    napi_value result;
    if (ret == Z_OK) {
        result = CreateArrayBufferCopy(env, decompressed, destLen);
    } else {
        free(decompressed);
        if (ret == Z_DATA_ERROR) {
            napi_throw_error(env, "-3", "Z_DATA_ERROR: corrupted data");
        } else if (ret == Z_BUF_ERROR) {
            napi_throw_error(env, "-5", "Z_BUF_ERROR: output buffer too small");
        } else if (ret == Z_MEM_ERROR) {
            napi_throw_error(env, "-4", "Z_MEM_ERROR: not enough memory");
        } else {
            napi_throw_error(env, nullptr, "Uncompression failed");
        }
        return nullptr;
    }

    free(decompressed);
    return result;
}

/**
 * @tc.name: SUB_ZLIB_Uncompress_ERROR_001
 * @tc.desc: 测试 uncompress 函数，损坏数据解压
 * @tc.type: FUNC
 */
static napi_value UncompressCorruptData(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 2) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected (ArrayBuffer, number).");
        return nullptr;
    }

    bool isArrayBuffer = false;
    status = napi_is_arraybuffer(env, args[0], &isArrayBuffer);
    if (status != napi_ok || !isArrayBuffer) {
        napi_throw_error(env, nullptr, "First argument must be an ArrayBuffer");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[1], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Second argument must be a number (dest length)");
        return nullptr;
    }

    int64_t destLenValue = 0;
    status = napi_get_value_int64(env, args[1], &destLenValue);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get dest length");
        return nullptr;
    }

    void *corruptData = nullptr;
    size_t corruptLen = 0;
    if (!GetArrayBufferData(env, args[0], &corruptData, &corruptLen)) {
        napi_throw_error(env, nullptr, "Failed to get corrupt buffer data");
        return nullptr;
    }

    uLongf destLen = (uLongf)destLenValue;
    Bytef *dest = (Bytef *)malloc(destLen);
    if (dest == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = uncompress(dest, &destLen, (const Bytef *)corruptData, corruptLen);
    free(dest);

    if (ret == Z_DATA_ERROR) {
        napi_throw_error(env, "-3", "Z_DATA_ERROR: corrupted or incomplete data");
        return nullptr;
    } else if (ret == Z_BUF_ERROR) {
        napi_throw_error(env, "-5", "Z_BUF_ERROR: output buffer too small");
        return nullptr;
    }

    napi_value napiResult;
    napi_create_int32(env, ret, &napiResult);
    return napiResult;
}

/**
 * @tc.name: SUB_ZLIB_CompressBound_RETURN_001
 * @tc.desc: 测试 compressBound 函数，正常数据大小
 * @tc.type: FUNC
 */
static napi_value CompressBoundNormalSize(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_error(env, nullptr, "Invalid arguments. Expected source length (number).");
        return nullptr;
    }

    napi_valuetype valuetype;
    status = napi_typeof(env, args[0], &valuetype);
    if (status != napi_ok || valuetype != napi_number) {
        napi_throw_error(env, nullptr, "Argument must be a number");
        return nullptr;
    }

    int64_t sourceLen = 0;
    status = napi_get_value_int64(env, args[0], &sourceLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get source length");
        return nullptr;
    }

    uLong bound = compressBound((uLong)sourceLen);

    napi_value result;
    napi_create_uint32(env, (uint32_t)bound, &result);
    return result;
}

/**
 * @tc.name: SUB_ZLIB_CompressBound_BOUNDARY_001
 * @tc.desc: 测试 compressBound 函数，零长度
 * @tc.type: FUNC
 */
static napi_value CompressBoundZeroLength(napi_env env, napi_callback_info info)
{
    uLong bound = compressBound(0);

    napi_value result;
    napi_create_uint32(env, (uint32_t)bound, &result);
    return result;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"compressNormalData", nullptr, CompressNormalData, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressEmptyData", nullptr, CompressEmptyData, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressBufError", nullptr, CompressBufError, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"uncompressRoundTrip", nullptr, UncompressRoundTrip, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"uncompressCorruptData", nullptr, UncompressCorruptData, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressBoundNormalSize", nullptr, CompressBoundNormalSize, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressBoundZeroLength", nullptr, CompressBoundZeroLength, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END

static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "entry",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterEntryModule(void)
{
    napi_module_register(&demoModule);
}
