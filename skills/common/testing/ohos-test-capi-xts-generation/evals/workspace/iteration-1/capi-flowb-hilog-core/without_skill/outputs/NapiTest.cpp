/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
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
#include "hilog/log.h"

#include <cstring>

#undef LOG_DOMAIN
#undef LOG_TAG
#define LOG_DOMAIN 0xD003200
#define LOG_TAG "HilogNdkTest"

static napi_value OHLogPrint(napi_env env, napi_callback_info info)
{
    size_t argc = 5;
    napi_value args[5] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    int32_t logType = 0;
    napi_get_value_int32(env, args[0], &logType);

    int32_t logLevel = 0;
    napi_get_value_int32(env, args[1], &logLevel);

    uint32_t domain = 0;
    napi_get_value_uint32(env, args[2], &domain);

    size_t tagLen = 0;
    napi_get_value_string_utf8(env, args[3], nullptr, 0, &tagLen);
    char *tag = new char[tagLen + 1];
    napi_get_value_string_utf8(env, args[3], tag, tagLen + 1, &tagLen);

    size_t fmtLen = 0;
    napi_get_value_string_utf8(env, args[4], nullptr, 0, &fmtLen);
    char *fmt = new char[fmtLen + 1];
    napi_get_value_string_utf8(env, args[4], fmt, fmtLen + 1, &fmtLen);

    int ret = OH_LOG_Print(static_cast<LogType>(logType), static_cast<LogLevel>(logLevel),
        domain, tag, "%{public}s", fmt);

    delete[] tag;
    delete[] fmt;

    napi_value result = nullptr;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value OHLogPrintWithArgs(napi_env env, napi_callback_info info)
{
    size_t argc = 6;
    napi_value args[6] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    int32_t logType = 0;
    napi_get_value_int32(env, args[0], &logType);

    int32_t logLevel = 0;
    napi_get_value_int32(env, args[1], &logLevel);

    uint32_t domain = 0;
    napi_get_value_uint32(env, args[2], &domain);

    size_t tagLen = 0;
    napi_get_value_string_utf8(env, args[3], nullptr, 0, &tagLen);
    char *tag = new char[tagLen + 1];
    napi_get_value_string_utf8(env, args[3], tag, tagLen + 1, &tagLen);

    size_t fmtLen = 0;
    napi_get_value_string_utf8(env, args[4], nullptr, 0, &fmtLen);
    char *fmt = new char[fmtLen + 1];
    napi_get_value_string_utf8(env, args[4], fmt, fmtLen + 1, &fmtLen);

    size_t argLen = 0;
    napi_get_value_string_utf8(env, args[5], nullptr, 0, &argLen);
    char *argStr = new char[argLen + 1];
    napi_get_value_string_utf8(env, args[5], argStr, argLen + 1, &argLen);

    int ret = OH_LOG_Print(static_cast<LogType>(logType), static_cast<LogLevel>(logLevel),
        domain, tag, fmt, argStr);

    delete[] tag;
    delete[] fmt;
    delete[] argStr;

    napi_value result = nullptr;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value OHLogPrintDebugLevel(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_DEBUG, 0x3200, "testTag", "%{public}s", "debug level log");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintInfoLevel(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "%{public}s", "info level log");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintWarnLevel(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_WARN, 0x3200, "testTag", "%{public}s", "warn level log");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintErrorLevel(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_ERROR, 0x3200, "testTag", "%{public}s", "error level log");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintFatalLevel(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_FATAL, 0x3200, "testTag", "%{public}s", "fatal level log");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintPrivateArg(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "private arg:%{private}s", "secret");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintPublicArg(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "public arg:%{public}s", "visible");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintBoundaryDomain0(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0x0000, "testTag", "%{public}s", "domain 0");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintBoundaryDomainFFFF(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0xFFFF, "testTag", "%{public}s", "domain FFFF");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintEmptyTag(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "", "%{public}s", "empty tag");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogPrintEmptyFmt(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    int ret = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "");
    napi_get_boolean(env, ret >= 0, &result);
    return result;
}

static napi_value OHLogIsLoggable(napi_env env, napi_callback_info info)
{
    size_t argc = 3;
    napi_value args[3] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    uint32_t domain = 0;
    napi_get_value_uint32(env, args[0], &domain);

    size_t tagLen = 0;
    napi_get_value_string_utf8(env, args[1], nullptr, 0, &tagLen);
    char *tag = new char[tagLen + 1];
    napi_get_value_string_utf8(env, args[1], tag, tagLen + 1, &tagLen);

    int32_t level = 0;
    napi_get_value_int32(env, args[2], &level);

    bool isLoggable = OH_LOG_IsLoggable(domain, tag, static_cast<LogLevel>(level));

    delete[] tag;

    napi_value result = nullptr;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogIsLoggableDebug(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool ret = OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG);
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogIsLoggableInfo(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool ret = OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO);
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogIsLoggableWarn(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool ret = OH_LOG_IsLoggable(0x3200, "testTag", LOG_WARN);
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogIsLoggableError(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool ret = OH_LOG_IsLoggable(0x3200, "testTag", LOG_ERROR);
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogIsLoggableFatal(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool ret = OH_LOG_IsLoggable(0x3200, "testTag", LOG_FATAL);
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogIsLoggableInvalidLevel(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    bool ret = OH_LOG_IsLoggable(0x3200, "testTag", static_cast<LogLevel>(100));
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogIsLoggableEmptyTag(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool ret = OH_LOG_IsLoggable(0x3200, "", LOG_INFO);
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogIsLoggableBoundaryDomain0(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool ret = OH_LOG_IsLoggable(0x0000, "testTag", LOG_INFO);
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogIsLoggableBoundaryDomainFFFF(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool ret = OH_LOG_IsLoggable(0xFFFF, "testTag", LOG_INFO);
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogSetMinLogLevel(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    int32_t level = 0;
    napi_get_value_int32(env, args[0], &level);

    OH_LOG_SetMinLogLevel(static_cast<LogLevel>(level));

    napi_value result = nullptr;
    napi_get_undefined(env, &result);
    return result;
}

static napi_value OHLogSetMinLogLevelAndCheck(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    int32_t setLevel = 0;
    napi_get_value_int32(env, args[0], &setLevel);

    int32_t checkLevel = 0;
    napi_get_value_int32(env, args[1], &checkLevel);

    OH_LOG_SetMinLogLevel(static_cast<LogLevel>(setLevel));
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", static_cast<LogLevel>(checkLevel));

    napi_value result = nullptr;
    napi_get_boolean(env, isLoggable, &result);
    return result;
}

static napi_value OHLogSetMinLogLevelDebug(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool debugLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG);
    napi_get_boolean(env, debugLoggable, &result);
    return result;
}

static napi_value OHLogSetMinLogLevelInfo(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_INFO);
    bool debugLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG);
    bool infoLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO);
    bool ret = !debugLoggable && infoLoggable;
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogSetMinLogLevelWarn(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_WARN);
    bool infoLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO);
    bool warnLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_WARN);
    bool ret = !infoLoggable && warnLoggable;
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogSetMinLogLevelError(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_ERROR);
    bool warnLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_WARN);
    bool errorLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_ERROR);
    bool ret = !warnLoggable && errorLoggable;
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogSetMinLogLevelFatal(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_FATAL);
    bool errorLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_ERROR);
    bool fatalLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_FATAL);
    bool ret = !errorLoggable && fatalLoggable;
    napi_get_boolean(env, ret, &result);
    return result;
}

static napi_value OHLogSetMinLogLevelThenPrint(napi_env env, napi_callback_info info)
{
    napi_value result = nullptr;
    OH_LOG_SetMinLogLevel(LOG_ERROR);
    int printBelowRet = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "%{public}s", "should be filtered");
    int printAboveRet = OH_LOG_Print(LOG_APP, LOG_ERROR, 0x3200, "testTag", "%{public}s", "should pass");
    bool ret = printAboveRet >= 0;
    napi_get_boolean(env, ret, &result);
    return result;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        { "oHLogPrint", nullptr, OHLogPrint, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintWithArgs", nullptr, OHLogPrintWithArgs, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintDebugLevel", nullptr, OHLogPrintDebugLevel, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintInfoLevel", nullptr, OHLogPrintInfoLevel, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintWarnLevel", nullptr, OHLogPrintWarnLevel, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintErrorLevel", nullptr, OHLogPrintErrorLevel, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintFatalLevel", nullptr, OHLogPrintFatalLevel, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintPrivateArg", nullptr, OHLogPrintPrivateArg, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintPublicArg", nullptr, OHLogPrintPublicArg, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintBoundaryDomain0", nullptr, OHLogPrintBoundaryDomain0, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintBoundaryDomainFFFF", nullptr, OHLogPrintBoundaryDomainFFFF, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintEmptyTag", nullptr, OHLogPrintEmptyTag, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogPrintEmptyFmt", nullptr, OHLogPrintEmptyFmt, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggable", nullptr, OHLogIsLoggable, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggableDebug", nullptr, OHLogIsLoggableDebug, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggableInfo", nullptr, OHLogIsLoggableInfo, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggableWarn", nullptr, OHLogIsLoggableWarn, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggableError", nullptr, OHLogIsLoggableError, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggableFatal", nullptr, OHLogIsLoggableFatal, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggableInvalidLevel", nullptr, OHLogIsLoggableInvalidLevel, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggableEmptyTag", nullptr, OHLogIsLoggableEmptyTag, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggableBoundaryDomain0", nullptr, OHLogIsLoggableBoundaryDomain0, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogIsLoggableBoundaryDomainFFFF", nullptr, OHLogIsLoggableBoundaryDomainFFFF, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogSetMinLogLevel", nullptr, OHLogSetMinLogLevel, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogSetMinLogLevelAndCheck", nullptr, OHLogSetMinLogLevelAndCheck, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogSetMinLogLevelDebug", nullptr, OHLogSetMinLogLevelDebug, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogSetMinLogLevelInfo", nullptr, OHLogSetMinLogLevelInfo, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogSetMinLogLevelWarn", nullptr, OHLogSetMinLogLevelWarn, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogSetMinLogLevelError", nullptr, OHLogSetMinLogLevelError, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogSetMinLogLevelFatal", nullptr, OHLogSetMinLogLevelFatal, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "oHLogSetMinLogLevelThenPrint", nullptr, OHLogSetMinLogLevelThenPrint, nullptr, nullptr, nullptr, napi_default, nullptr },
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
    .nm_modname = "libhilogndk",
    .nm_priv = ((void *)0),
    .reserved = { 0 },
};

extern "C" __attribute__((constructor)) void RegisterModule(void)
{
    napi_module_register(&demoModule);
}
