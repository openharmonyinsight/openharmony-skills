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

#include <string>

#undef LOG_DOMAIN
#undef LOG_TAG
#define LOG_DOMAIN 0xD003200
#define LOG_TAG "HilogNapiTest"

static napi_value OhLogPrintNormalParam(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    int retLen = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "string for hilog normal param test");
    bool ret = (retLen >= 0) ? true : false;
    napi_get_boolean(env, ret, &res);
    return res;
}

static napi_value OhLogPrintAllLevels(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    int ret1 = OH_LOG_Print(LOG_APP, LOG_DEBUG, 0x3200, "testTag", "debug level test");
    int ret2 = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "info level test");
    int ret3 = OH_LOG_Print(LOG_APP, LOG_WARN, 0x3200, "testTag", "warn level test");
    int ret4 = OH_LOG_Print(LOG_APP, LOG_ERROR, 0x3200, "testTag", "error level test");
    int ret5 = OH_LOG_Print(LOG_APP, LOG_FATAL, 0x3200, "testTag", "fatal level test");
    bool ret = (ret1 >= 0 && ret2 >= 0 && ret3 >= 0 && ret4 >= 0 && ret5 >= 0) ? true : false;
    napi_get_boolean(env, ret, &res);
    return res;
}

static napi_value OhLogPrintReturn(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    int retLen = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "return value test");
    napi_create_int32(env, retLen, &res);
    return res;
}

static napi_value OhLogPrintDomainBoundary(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    int ret1 = OH_LOG_Print(LOG_APP, LOG_INFO, 0x0, "testTag", "domain min boundary");
    int ret2 = OH_LOG_Print(LOG_APP, LOG_INFO, 0xFFFF, "testTag", "domain max boundary");
    bool ret = (ret1 >= 0 && ret2 >= 0) ? true : false;
    napi_get_boolean(env, ret, &res);
    return res;
}

static napi_value OhLogIsLoggableTrue(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG);
    napi_get_boolean(env, isLoggable, &res);
    return res;
}

static napi_value OhLogIsLoggableFalse(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    OH_LOG_SetMinLogLevel(LOG_FATAL);
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", LOG_DEBUG);
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    napi_get_boolean(env, isLoggable, &res);
    return res;
}

static napi_value OhLogIsLoggableEmptyTag(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "", LOG_DEBUG);
    napi_get_boolean(env, isLoggable, &res);
    return res;
}

static napi_value OhLogIsLoggableInvalidLevel(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    bool isLoggable = OH_LOG_IsLoggable(0x3200, "testTag", (LogLevel)100);
    napi_get_boolean(env, isLoggable, &res);
    return res;
}

static napi_value OhLogSetMinLogLevelInfo(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    OH_LOG_SetMinLogLevel(LOG_INFO);
    int retLen = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "print after set info level");
    bool ret = (retLen >= 0) ? true : false;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    napi_get_boolean(env, ret, &res);
    return res;
}

static napi_value OhLogSetMinLogLevelFatal(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    OH_LOG_SetMinLogLevel(LOG_FATAL);
    int retLen = OH_LOG_Print(LOG_APP, LOG_INFO, 0x3200, "testTag", "blocked by fatal level");
    bool ret = (retLen < 0) ? true : false;
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    napi_get_boolean(env, ret, &res);
    return res;
}

static napi_value OhLogSetMinLogLevelRestore(napi_env env, napi_callback_info info)
{
    napi_value res = nullptr;
    OH_LOG_SetMinLogLevel(LOG_FATAL);
    bool blocked = OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO);
    OH_LOG_SetMinLogLevel(LOG_DEBUG);
    bool restored = OH_LOG_IsLoggable(0x3200, "testTag", LOG_INFO);
    bool ret = (!blocked && restored) ? true : false;
    napi_get_boolean(env, ret, &res);
    return res;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        { "ohLogPrintNormalParam", nullptr, OhLogPrintNormalParam,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogPrintAllLevels", nullptr, OhLogPrintAllLevels,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogPrintReturn", nullptr, OhLogPrintReturn,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogPrintDomainBoundary", nullptr, OhLogPrintDomainBoundary,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogIsLoggableTrue", nullptr, OhLogIsLoggableTrue,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogIsLoggableFalse", nullptr, OhLogIsLoggableFalse,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogIsLoggableEmptyTag", nullptr, OhLogIsLoggableEmptyTag,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogIsLoggableInvalidLevel", nullptr, OhLogIsLoggableInvalidLevel,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogSetMinLogLevelInfo", nullptr, OhLogSetMinLogLevelInfo,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogSetMinLogLevelFatal", nullptr, OhLogSetMinLogLevelFatal,
            nullptr, nullptr, nullptr, napi_default, nullptr },
        { "ohLogSetMinLogLevelRestore", nullptr, OhLogSetMinLogLevelRestore,
            nullptr, nullptr, nullptr, napi_default, nullptr },
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
    .reserved = { 0 },
};

extern "C" __attribute__((constructor)) void RegisterEntryModule(void)
{
    napi_module_register(&demoModule);
}
