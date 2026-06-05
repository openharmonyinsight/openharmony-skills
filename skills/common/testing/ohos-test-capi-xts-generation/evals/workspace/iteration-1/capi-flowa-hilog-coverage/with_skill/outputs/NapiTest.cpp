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

#include <napi/native_api.h>
#include <hilog/log.h>
#include <string.h>
#include <stdlib.h>
#include <stdarg.h>

#define LOG_DOMAIN 0xFF00
#define LOG_TAG "NapiTest"

/**
 * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_PARAM_001
 * @tc.desc: Test OH_LOG_PrintMsg with normal parameters
 * @tc.type: FUNC
 */
static napi_value OH_LOG_PrintMsg_ParamTest_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 5;
    napi_value args[5];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 5) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    int32_t type;
    int32_t level;
    uint32_t domain;

    status = napi_get_value_int32(env, args[0], &type);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get type");
        return nullptr;
    }

    status = napi_get_value_int32(env, args[1], &level);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get level");
        return nullptr;
    }

    status = napi_get_value_uint32(env, args[2], &domain);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get domain");
        return nullptr;
    }

    size_t tagLen = 0;
    status = napi_get_value_string_utf8(env, args[3], nullptr, 0, &tagLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get tag length");
        return nullptr;
    }
    char *tag = (char *)malloc(tagLen + 1);
    if (tag == nullptr) {
        napi_throw_error(env, nullptr, "Failed to allocate memory for tag");
        return nullptr;
    }
    status = napi_get_value_string_utf8(env, args[3], tag, tagLen + 1, &tagLen);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get tag");
        return nullptr;
    }

    size_t msgLen = 0;
    status = napi_get_value_string_utf8(env, args[4], nullptr, 0, &msgLen);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get message length");
        return nullptr;
    }
    char *message = (char *)malloc(msgLen + 1);
    if (message == nullptr) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to allocate memory for message");
        return nullptr;
    }
    status = napi_get_value_string_utf8(env, args[4], message, msgLen + 1, &msgLen);
    if (status != napi_ok) {
        free(tag);
        free(message);
        napi_throw_error(env, nullptr, "Failed to get message");
        return nullptr;
    }

    int ret = OH_LOG_PrintMsg((LogType)type, (LogLevel)level, domain, tag, message);

    free(tag);
    free(message);

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

/**
 * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_PARAM_001
 * @tc.desc: Test OH_LOG_PrintMsgByLen with normal parameters
 * @tc.type: FUNC
 */
static napi_value OH_LOG_PrintMsgByLen_ParamTest_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 5;
    napi_value args[5];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 5) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    int32_t type;
    int32_t level;
    uint32_t domain;

    status = napi_get_value_int32(env, args[0], &type);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get type");
        return nullptr;
    }

    status = napi_get_value_int32(env, args[1], &level);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get level");
        return nullptr;
    }

    status = napi_get_value_uint32(env, args[2], &domain);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get domain");
        return nullptr;
    }

    size_t tagLen = 0;
    status = napi_get_value_string_utf8(env, args[3], nullptr, 0, &tagLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get tag length");
        return nullptr;
    }
    char *tag = (char *)malloc(tagLen + 1);
    if (tag == nullptr) {
        napi_throw_error(env, nullptr, "Failed to allocate memory for tag");
        return nullptr;
    }
    status = napi_get_value_string_utf8(env, args[3], tag, tagLen + 1, &tagLen);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get tag");
        return nullptr;
    }

    size_t msgLen = 0;
    status = napi_get_value_string_utf8(env, args[4], nullptr, 0, &msgLen);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get message length");
        return nullptr;
    }
    char *message = (char *)malloc(msgLen + 1);
    if (message == nullptr) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to allocate memory for message");
        return nullptr;
    }
    status = napi_get_value_string_utf8(env, args[4], message, msgLen + 1, &msgLen);
    if (status != napi_ok) {
        free(tag);
        free(message);
        napi_throw_error(env, nullptr, "Failed to get message");
        return nullptr;
    }

    int ret = OH_LOG_PrintMsgByLen((LogType)type, (LogLevel)level, domain, tag, tagLen, message, msgLen);

    free(tag);
    free(message);

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

/**
 * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_BOUNDARY_001
 * @tc.desc: Test OH_LOG_PrintMsgByLen with boundary length values
 * @tc.type: FUNC
 */
static napi_value OH_LOG_PrintMsgByLen_BoundaryTest_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 7;
    napi_value args[7];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 7) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    int32_t type;
    int32_t level;
    uint32_t domain;

    status = napi_get_value_int32(env, args[0], &type);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get type");
        return nullptr;
    }

    status = napi_get_value_int32(env, args[1], &level);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get level");
        return nullptr;
    }

    status = napi_get_value_uint32(env, args[2], &domain);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get domain");
        return nullptr;
    }

    size_t tagStrLen = 0;
    status = napi_get_value_string_utf8(env, args[3], nullptr, 0, &tagStrLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get tag length");
        return nullptr;
    }
    char *tag = (char *)malloc(tagStrLen + 1);
    if (tag == nullptr) {
        napi_throw_error(env, nullptr, "Failed to allocate memory for tag");
        return nullptr;
    }
    status = napi_get_value_string_utf8(env, args[3], tag, tagStrLen + 1, &tagStrLen);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get tag");
        return nullptr;
    }

    int32_t tagLenParam;
    status = napi_get_value_int32(env, args[4], &tagLenParam);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get tagLen param");
        return nullptr;
    }

    size_t msgStrLen = 0;
    status = napi_get_value_string_utf8(env, args[5], nullptr, 0, &msgStrLen);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get message length");
        return nullptr;
    }
    char *message = (char *)malloc(msgStrLen + 1);
    if (message == nullptr) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to allocate memory for message");
        return nullptr;
    }
    status = napi_get_value_string_utf8(env, args[5], message, msgStrLen + 1, &msgStrLen);
    if (status != napi_ok) {
        free(tag);
        free(message);
        napi_throw_error(env, nullptr, "Failed to get message");
        return nullptr;
    }

    int32_t messageLenParam;
    status = napi_get_value_int32(env, args[6], &messageLenParam);
    if (status != napi_ok) {
        free(tag);
        free(message);
        napi_throw_error(env, nullptr, "Failed to get messageLen param");
        return nullptr;
    }

    int ret = OH_LOG_PrintMsgByLen((LogType)type, (LogLevel)level, domain, tag,
        (size_t)tagLenParam, message, (size_t)messageLenParam);

    free(tag);
    free(message);

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

static int CallVPrintHelper(LogType type, LogLevel level, unsigned int domain,
    const char *tag, const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    int ret = OH_LOG_VPrint(type, level, domain, tag, fmt, ap);
    va_end(ap);
    return ret;
}

/**
 * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_PARAM_001
 * @tc.desc: Test OH_LOG_VPrint with normal parameters
 * @tc.type: FUNC
 */
static napi_value OH_LOG_VPrint_ParamTest_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 6;
    napi_value args[6];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 6) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    int32_t type;
    int32_t level;
    uint32_t domain;

    status = napi_get_value_int32(env, args[0], &type);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get type");
        return nullptr;
    }

    status = napi_get_value_int32(env, args[1], &level);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get level");
        return nullptr;
    }

    status = napi_get_value_uint32(env, args[2], &domain);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get domain");
        return nullptr;
    }

    size_t tagLen = 0;
    status = napi_get_value_string_utf8(env, args[3], nullptr, 0, &tagLen);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get tag length");
        return nullptr;
    }
    char *tag = (char *)malloc(tagLen + 1);
    if (tag == nullptr) {
        napi_throw_error(env, nullptr, "Failed to allocate memory for tag");
        return nullptr;
    }
    status = napi_get_value_string_utf8(env, args[3], tag, tagLen + 1, &tagLen);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get tag");
        return nullptr;
    }

    size_t fmtLen = 0;
    status = napi_get_value_string_utf8(env, args[4], nullptr, 0, &fmtLen);
    if (status != napi_ok) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to get fmt length");
        return nullptr;
    }
    char *fmt = (char *)malloc(fmtLen + 1);
    if (fmt == nullptr) {
        free(tag);
        napi_throw_error(env, nullptr, "Failed to allocate memory for fmt");
        return nullptr;
    }
    status = napi_get_value_string_utf8(env, args[4], fmt, fmtLen + 1, &fmtLen);
    if (status != napi_ok) {
        free(tag);
        free(fmt);
        napi_throw_error(env, nullptr, "Failed to get fmt");
        return nullptr;
    }

    size_t msgArgLen = 0;
    status = napi_get_value_string_utf8(env, args[5], nullptr, 0, &msgArgLen);
    if (status != napi_ok) {
        free(tag);
        free(fmt);
        napi_throw_error(env, nullptr, "Failed to get message arg length");
        return nullptr;
    }
    char *msgArg = (char *)malloc(msgArgLen + 1);
    if (msgArg == nullptr) {
        free(tag);
        free(fmt);
        napi_throw_error(env, nullptr, "Failed to allocate memory for message arg");
        return nullptr;
    }
    status = napi_get_value_string_utf8(env, args[5], msgArg, msgArgLen + 1, &msgArgLen);
    if (status != napi_ok) {
        free(tag);
        free(fmt);
        free(msgArg);
        napi_throw_error(env, nullptr, "Failed to get message arg");
        return nullptr;
    }

    int ret = CallVPrintHelper((LogType)type, (LogLevel)level, domain, tag, fmt, msgArg);

    free(tag);
    free(fmt);
    free(msgArg);

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

/**
 * @tc.name: SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_001
 * @tc.desc: Test PreferStrategy enum values via OH_LOG_SetLogLevel
 * @tc.type: FUNC
 */
static napi_value PreferStrategy_ParamTest_napi(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2];
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok || argc < 2) {
        napi_throw_error(env, nullptr, "Invalid arguments");
        return nullptr;
    }

    int32_t level;
    int32_t strategy;

    status = napi_get_value_int32(env, args[0], &level);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get level");
        return nullptr;
    }

    status = napi_get_value_int32(env, args[1], &strategy);
    if (status != napi_ok) {
        napi_throw_error(env, nullptr, "Failed to get strategy");
        return nullptr;
    }

    OH_LOG_SetLogLevel((LogLevel)level, (PreferStrategy)strategy);

    int ret = OH_LOG_PrintMsg(LOG_APP, LOG_DEBUG, 0xFF00, "PreferTest", "verify log after set level");

    napi_value result;
    napi_create_int32(env, ret, &result);
    return result;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        DECLARE_NAPI_FUNCTION("OH_LOG_PrintMsg_ParamTest", OH_LOG_PrintMsg_ParamTest_napi),
        DECLARE_NAPI_FUNCTION("OH_LOG_PrintMsgByLen_ParamTest", OH_LOG_PrintMsgByLen_ParamTest_napi),
        DECLARE_NAPI_FUNCTION("OH_LOG_PrintMsgByLen_BoundaryTest", OH_LOG_PrintMsgByLen_BoundaryTest_napi),
        DECLARE_NAPI_FUNCTION("OH_LOG_VPrint_ParamTest", OH_LOG_VPrint_ParamTest_napi),
        DECLARE_NAPI_FUNCTION("PreferStrategy_ParamTest", PreferStrategy_ParamTest_napi),
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
