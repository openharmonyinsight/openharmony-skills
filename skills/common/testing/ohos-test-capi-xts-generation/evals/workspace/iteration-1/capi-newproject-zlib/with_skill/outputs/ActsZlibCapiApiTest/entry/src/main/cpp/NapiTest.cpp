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
#include "zlib.h"

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
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Compress_PARAM_001
 * @tc.desc: Test compress function with normal data
 * @tc.type: FUNC
 */
static napi_value CompressNormalData_napi(napi_env env, napi_callback_info info)
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
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = compress(compressed, &compressedLen, (const Bytef *)sourceData, sourceLen);
    if (ret != Z_OK) {
        free(compressed);
        napi_throw_error(env, std::to_string(ret).c_str(), "Compress failed");
        return nullptr;
    }

    napi_value result = CreateArrayBufferCopy(env, compressed, compressedLen);
    free(compressed);
    return result;
}

/**
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Compress_BOUNDARY_001
 * @tc.desc: Test compress function with empty data
 * @tc.type: FUNC
 */
static napi_value CompressEmptyData_napi(napi_env env, napi_callback_info info)
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
    Bytef *compressed = (Bytef *)malloc(compressedLen > 0 ? compressedLen : 1);
    if (compressed == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = compress(compressed, &compressedLen, (const Bytef *)sourceData, sourceLen);
    if (ret != Z_OK) {
        free(compressed);
        napi_throw_error(env, std::to_string(ret).c_str(), "Compress empty data failed");
        return nullptr;
    }

    napi_value result = CreateArrayBufferCopy(env, compressed, compressedLen);
    free(compressed);
    return result;
}

/**
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Compress_PARAM_002
 * @tc.desc: Test compress function with large data
 * @tc.type: FUNC
 */
static napi_value CompressLargeData_napi(napi_env env, napi_callback_info info)
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
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = compress(compressed, &compressedLen, (const Bytef *)sourceData, sourceLen);
    if (ret != Z_OK) {
        free(compressed);
        napi_throw_error(env, std::to_string(ret).c_str(), "Compress large data failed");
        return nullptr;
    }

    napi_value result = CreateArrayBufferCopy(env, compressed, compressedLen);
    free(compressed);
    return result;
}

/**
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Uncompress_PARAM_001
 * @tc.desc: Test uncompress function with normal compressed data
 * @tc.type: FUNC
 */
static napi_value UncompressNormalData_napi(napi_env env, napi_callback_info info)
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
        napi_throw_error(env, nullptr, "Second argument must be a number");
        return nullptr;
    }

    int64_t originalSize = 0;
    status = napi_get_value_int64(env, args[1], &originalSize);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get original size");
        return nullptr;
    }

    void *compressedData = nullptr;
    size_t compressedLen = 0;
    if (!GetArrayBufferData(env, args[0], &compressedData, &compressedLen)) {
        napi_throw_error(env, nullptr, "Failed to get compressed buffer data");
        return nullptr;
    }

    uLongf destLen = (uLongf)originalSize;
    Bytef *decompressed = (Bytef *)malloc(destLen);
    if (decompressed == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = uncompress(decompressed, &destLen, (const Bytef *)compressedData, compressedLen);
    if (ret != Z_OK) {
        free(decompressed);
        napi_throw_error(env, std::to_string(ret).c_str(), "Uncompress failed");
        return nullptr;
    }

    napi_value result = CreateArrayBufferCopy(env, decompressed, destLen);
    free(decompressed);
    return result;
}

/**
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Uncompress_ERROR_001
 * @tc.desc: Test uncompress function with corrupted data
 * @tc.type: FUNC
 */
static napi_value UncompressCorruptedData_napi(napi_env env, napi_callback_info info)
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
        napi_throw_error(env, nullptr, "Second argument must be a number");
        return nullptr;
    }

    int64_t originalSize = 0;
    status = napi_get_value_int64(env, args[1], &originalSize);

    void *corruptedData = nullptr;
    size_t dataLen = 0;
    if (!GetArrayBufferData(env, args[0], &corruptedData, &dataLen)) {
        napi_throw_error(env, nullptr, "Failed to get buffer data");
        return nullptr;
    }

    uLongf destLen = (uLongf)originalSize;
    Bytef *dest = (Bytef *)malloc(destLen > 0 ? destLen : 1);
    if (dest == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = uncompress(dest, &destLen, (const Bytef *)corruptedData, dataLen);
    free(dest);

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

/**
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Uncompress_ERROR_002
 * @tc.desc: Test uncompress function with insufficient buffer
 * @tc.type: FUNC
 */
static napi_value UncompressSmallBuffer_napi(napi_env env, napi_callback_info info)
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
        napi_throw_error(env, nullptr, "Second argument must be a number");
        return nullptr;
    }

    int64_t smallSize = 0;
    status = napi_get_value_int64(env, args[1], &smallSize);

    void *compressedData = nullptr;
    size_t compressedLen = 0;
    if (!GetArrayBufferData(env, args[0], &compressedData, &compressedLen)) {
        napi_throw_error(env, nullptr, "Failed to get compressed buffer data");
        return nullptr;
    }

    uLongf destLen = (uLongf)smallSize;
    Bytef *dest = (Bytef *)malloc(destLen > 0 ? destLen : 1);
    if (dest == nullptr) {
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = uncompress(dest, &destLen, (const Bytef *)compressedData, compressedLen);
    free(dest);

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

/**
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_CompressBound_RETURN_001
 * @tc.desc: Test compressBound function with normal source length
 * @tc.type: FUNC
 */
static napi_value CompressBoundNormalLength_napi(napi_env env, napi_callback_info info)
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
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_CompressBound_BOUNDARY_001
 * @tc.desc: Test compressBound function with zero source length
 * @tc.type: FUNC
 */
static napi_value CompressBoundZeroLength_napi(napi_env env, napi_callback_info info)
{
    uLong bound = compressBound(0);

    napi_value result;
    napi_create_uint32(env, (uint32_t)bound, &result);
    return result;
}

/**
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_CompressBound_BOUNDARY_002
 * @tc.desc: Test compressBound function with large source length
 * @tc.type: FUNC
 */
static napi_value CompressBoundLargeLength_napi(napi_env env, napi_callback_info info)
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
 * @tc.name: SUB_BUNDLEMANAGER_ZLIB_CompressUncompress_RETURN_001
 * @tc.desc: Test compress then uncompress round trip
 * @tc.type: FUNC
 */
static napi_value CompressUncompressRoundTrip_napi(napi_env env, napi_callback_info info)
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
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    int ret = compress(compressed, &compressedLen, (const Bytef *)sourceData, sourceLen);
    if (ret != Z_OK) {
        free(compressed);
        napi_throw_error(env, std::to_string(ret).c_str(), "Compress failed in round trip");
        return nullptr;
    }

    uLongf decompressedLen = sourceLen;
    Bytef *decompressed = (Bytef *)malloc(decompressedLen);
    if (decompressed == nullptr) {
        free(compressed);
        napi_throw_error(env, nullptr, "Memory allocation failed");
        return nullptr;
    }

    ret = uncompress(decompressed, &decompressedLen, compressed, compressedLen);
    free(compressed);

    if (ret != Z_OK) {
        free(decompressed);
        napi_throw_error(env, std::to_string(ret).c_str(), "Uncompress failed in round trip");
        return nullptr;
    }

    bool match = (decompressedLen == sourceLen) &&
                 (memcmp(decompressed, sourceData, sourceLen) == 0);
    free(decompressed);

    if (!match) {
        napi_throw_error(env, nullptr, "Round trip data mismatch");
        return nullptr;
    }

    napi_value result;
    napi_create_int32(env, 0, &result);
    return result;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"compressNormalData", nullptr, CompressNormalData_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressEmptyData", nullptr, CompressEmptyData_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressLargeData", nullptr, CompressLargeData_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"uncompressNormalData", nullptr, UncompressNormalData_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"uncompressCorruptedData", nullptr, UncompressCorruptedData_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"uncompressSmallBuffer", nullptr, UncompressSmallBuffer_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressBoundNormalLength", nullptr, CompressBoundNormalLength_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressBoundZeroLength", nullptr, CompressBoundZeroLength_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressBoundLargeLength", nullptr, CompressBoundLargeLength_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"compressUncompressRoundTrip", nullptr, CompressUncompressRoundTrip_napi, nullptr, nullptr, nullptr, napi_default, nullptr},
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
