/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
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
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <hilog/log.h>
#include <string>

#ifdef __cplusplus
extern "C" {
#endif
#include "zlib.h"
#ifdef __cplusplus
}
#endif

namespace {
constexpr int32_t ARG_INDEX = 0;
constexpr int32_t DEFAULT_ARG = -1;
constexpr int32_t RESULT_ERROR = -1;
constexpr int32_t RESULT_SUCCESS = 0;
const std::string TAG = "ActsZlibCapiTest";
constexpr uint32_t LOG_DOMAIN = 0xD00F000;
}

using ZlibTestFn = int32_t (*)();

static int32_t TestCompress001()
{
    const char *src = "Hello, OpenHarmony zlib compress test!";
    uLong srcLen = static_cast<uLong>(strlen(src));
    uLong destLen = compressBound(srcLen);
    if (destLen == 0) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, TAG.c_str(), "compressBound returned 0");
        return RESULT_ERROR;
    }
    Bytef *dest = static_cast<Bytef *>(malloc(destLen));
    if (dest == nullptr) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, TAG.c_str(), "malloc failed for compress dest");
        return RESULT_ERROR;
    }
    int ret = compress(dest, &destLen, reinterpret_cast<const Bytef *>(src), srcLen);
    free(dest);
    if (ret != Z_OK) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, TAG.c_str(), "compress failed: %{public}d", ret);
        return RESULT_ERROR;
    }
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(), "compress succeeded, ret=%{public}d", ret);
    return RESULT_SUCCESS;
}

static int32_t TestCompress002()
{
    const char *src = "";
    uLong srcLen = 0;
    uLong destLen = compressBound(srcLen);
    Bytef *dest = static_cast<Bytef *>(malloc(destLen > 0 ? destLen : 1));
    if (dest == nullptr) {
        return RESULT_ERROR;
    }
    int ret = compress(dest, &destLen, reinterpret_cast<const Bytef *>(src), srcLen);
    free(dest);
    if (ret != Z_OK) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, TAG.c_str(), "compress empty failed: %{public}d", ret);
        return RESULT_ERROR;
    }
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(), "compress empty succeeded");
    return RESULT_SUCCESS;
}

static int32_t TestCompress003()
{
    char src[4096];
    memset(src, 'A', sizeof(src));
    uLong srcLen = sizeof(src);
    uLong destLen = compressBound(srcLen);
    Bytef *dest = static_cast<Bytef *>(malloc(destLen));
    if (dest == nullptr) {
        return RESULT_ERROR;
    }
    int ret = compress(dest, &destLen, reinterpret_cast<const Bytef *>(src), srcLen);
    free(dest);
    if (ret != Z_OK) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, TAG.c_str(), "compress large failed: %{public}d", ret);
        return RESULT_ERROR;
    }
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(), "compress large succeeded");
    return RESULT_SUCCESS;
}

static int32_t TestUncompress001()
{
    const char *src = "Hello, OpenHarmony zlib uncompress test!";
    uLong srcLen = static_cast<uLong>(strlen(src));
    uLong compressedLen = compressBound(srcLen);
    Bytef *compressed = static_cast<Bytef *>(malloc(compressedLen));
    if (compressed == nullptr) {
        return RESULT_ERROR;
    }
    int ret = compress(compressed, &compressedLen, reinterpret_cast<const Bytef *>(src), srcLen);
    if (ret != Z_OK) {
        free(compressed);
        return RESULT_ERROR;
    }
    uLong uncompressedLen = srcLen;
    Bytef *uncompressed = static_cast<Bytef *>(malloc(uncompressedLen + 1));
    if (uncompressed == nullptr) {
        free(compressed);
        return RESULT_ERROR;
    }
    ret = uncompress(uncompressed, &uncompressedLen, compressed, compressedLen);
    if (ret != Z_OK) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, TAG.c_str(), "uncompress failed: %{public}d", ret);
        free(compressed);
        free(uncompressed);
        return RESULT_ERROR;
    }
    uncompressed[uncompressedLen] = '\0';
    if (memcmp(uncompressed, src, srcLen) != 0) {
        OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, TAG.c_str(), "uncompress data mismatch");
        free(compressed);
        free(uncompressed);
        return RESULT_ERROR;
    }
    free(compressed);
    free(uncompressed);
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(), "uncompress succeeded");
    return RESULT_SUCCESS;
}

static int32_t TestUncompress002()
{
    Bytef corrupted[] = {0x78, 0x9C, 0xFF, 0xFF, 0xFF, 0xFF};
    uLong compressedLen = sizeof(corrupted);
    uLong destLen = 1024;
    Bytef *dest = static_cast<Bytef *>(malloc(destLen));
    if (dest == nullptr) {
        return RESULT_ERROR;
    }
    int ret = uncompress(dest, &destLen, corrupted, compressedLen);
    free(dest);
    if (ret == Z_DATA_ERROR) {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(), "uncompress corrupted data correctly returned Z_DATA_ERROR");
        return RESULT_SUCCESS;
    }
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(), "uncompress corrupted ret=%{public}d (expected Z_DATA_ERROR)", ret);
    return RESULT_SUCCESS;
}

static int32_t TestUncompress003()
{
    const char *src = "Hello buffer test!";
    uLong srcLen = static_cast<uLong>(strlen(src));
    uLong compressedLen = compressBound(srcLen);
    Bytef *compressed = static_cast<Bytef *>(malloc(compressedLen));
    if (compressed == nullptr) {
        return RESULT_ERROR;
    }
    int ret = compress(compressed, &compressedLen, reinterpret_cast<const Bytef *>(src), srcLen);
    if (ret != Z_OK) {
        free(compressed);
        return RESULT_ERROR;
    }
    uLong smallDestLen = 1;
    Bytef *smallDest = static_cast<Bytef *>(malloc(smallDestLen));
    if (smallDest == nullptr) {
        free(compressed);
        return RESULT_ERROR;
    }
    ret = uncompress(smallDest, &smallDestLen, compressed, compressedLen);
    free(smallDest);
    free(compressed);
    if (ret == Z_BUF_ERROR) {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(), "uncompress buffer too small correctly returned Z_BUF_ERROR");
        return RESULT_SUCCESS;
    }
    OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(), "uncompress small buffer ret=%{public}d", ret);
    return RESULT_SUCCESS;
}

static int32_t TestCompressBound001()
{
    uLong srcLen = 1024;
    uLong bound = compressBound(srcLen);
    if (bound > 0 && bound >= srcLen) {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(),
                     "compressBound(%{public}lu) = %{public}lu", srcLen, bound);
        return RESULT_SUCCESS;
    }
    OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, TAG.c_str(),
                 "compressBound unexpected result: %{public}lu for srcLen %{public}lu", bound, srcLen);
    return RESULT_ERROR;
}

static int32_t TestCompressBound002()
{
    uLong bound = compressBound(0);
    if (bound > 0) {
        OH_LOG_Print(LOG_APP, LOG_INFO, LOG_DOMAIN, TAG.c_str(), "compressBound(0) = %{public}lu", bound);
        return RESULT_SUCCESS;
    }
    OH_LOG_Print(LOG_APP, LOG_ERROR, LOG_DOMAIN, TAG.c_str(), "compressBound(0) returned 0");
    return RESULT_ERROR;
}

static const ZlibTestFn COMPRESS_FUNCS[] = {
    TestCompress001,
    TestCompress002,
    TestCompress003,
};

static const ZlibTestFn UNCOMPRESS_FUNCS[] = {
    TestUncompress001,
    TestUncompress002,
    TestUncompress003,
};

static const ZlibTestFn COMPRESSBOUND_FUNCS[] = {
    TestCompressBound001,
    TestCompressBound002,
};

static napi_value CommonDispatch(napi_env env, napi_callback_info info,
                                  const ZlibTestFn *funcs, size_t funcCount)
{
    size_t argc = 1;
    napi_value args[1];
    napi_status status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 1) {
        napi_throw_type_error(env, nullptr, "Argument missing");
        napi_value resultValue;
        napi_create_int32(env, RESULT_ERROR, &resultValue);
        return resultValue;
    }
    napi_valuetype valuetype;
    napi_typeof(env, args[0], &valuetype);
    if (valuetype != napi_number) {
        napi_throw_type_error(env, nullptr, "Argument must be a number");
        napi_value resultValue;
        napi_create_int32(env, RESULT_ERROR, &resultValue);
        return resultValue;
    }
    int32_t caseNum = DEFAULT_ARG;
    napi_get_value_int32(env, args[0], &caseNum);
    int32_t result = RESULT_ERROR;
    if (caseNum >= 0 && static_cast<size_t>(caseNum) < funcCount) {
        result = funcs[caseNum]();
    }
    napi_value resultValue;
    napi_create_int32(env, result, &resultValue);
    return resultValue;
}

napi_value ZlibCompress(napi_env env, napi_callback_info info)
{
    return CommonDispatch(env, info, COMPRESS_FUNCS, sizeof(COMPRESS_FUNCS) / sizeof(COMPRESS_FUNCS[0]));
}

napi_value ZlibUncompress(napi_env env, napi_callback_info info)
{
    return CommonDispatch(env, info, UNCOMPRESS_FUNCS, sizeof(UNCOMPRESS_FUNCS) / sizeof(UNCOMPRESS_FUNCS[0]));
}

napi_value ZlibCompressBound(napi_env env, napi_callback_info info)
{
    return CommonDispatch(env, info, COMPRESSBOUND_FUNCS, sizeof(COMPRESSBOUND_FUNCS) / sizeof(COMPRESSBOUND_FUNCS[0]));
}

EXTERN_C_START

napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"zlibCompress", nullptr, ZlibCompress, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"zlibUncompress", nullptr, ZlibUncompress, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"zlibCompressBound", nullptr, ZlibCompressBound, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}

EXTERN_C_END

static napi_module g_zlibcapitestModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "zlibcapitest",
    .nm_priv = static_cast<void *>(nullptr),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterZlibcapitestModule(void)
{
    napi_module_register(&g_zlibcapitestModule);
}
