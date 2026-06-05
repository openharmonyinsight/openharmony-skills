/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
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

#include <hilog/log.h>
#include <napi/native_api.h>
#include <cstring>

static napi_value NapiOHLogPrintMsg(napi_env env, napi_callback_info info)
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

    size_t msgLen = 0;
    napi_get_value_string_utf8(env, args[4], nullptr, 0, &msgLen);
    char *message = new char[msgLen + 1];
    napi_get_value_string_utf8(env, args[4], message, msgLen + 1, &msgLen);

    int ret = OH_LOG_PrintMsg(static_cast<LogType>(logType), static_cast<LogLevel>(logLevel),
        domain, tag, message);

    delete[] tag;
    delete[] message;

    napi_value result = nullptr;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value NapiOHLogPrintMsgByLen(napi_env env, napi_callback_info info)
{
    size_t argc = 7;
    napi_value args[7] = {nullptr};
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

    size_t tagLenParam = 0;
    napi_get_value_uint32(env, args[4], &tagLenParam);

    size_t msgLen = 0;
    napi_get_value_string_utf8(env, args[5], nullptr, 0, &msgLen);
    char *message = new char[msgLen + 1];
    napi_get_value_string_utf8(env, args[5], message, msgLen + 1, &msgLen);

    size_t messageLenParam = 0;
    napi_get_value_uint32(env, args[6], &messageLenParam);

    int ret = OH_LOG_PrintMsgByLen(static_cast<LogType>(logType), static_cast<LogLevel>(logLevel),
        domain, tag, tagLenParam, message, messageLenParam);

    delete[] tag;
    delete[] message;

    napi_value result = nullptr;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value NapiOHLogVPrint(napi_env env, napi_callback_info info)
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

    va_list ap;
    va_start(ap, fmt);

    int ret = OH_LOG_VPrint(static_cast<LogType>(logType), static_cast<LogLevel>(logLevel),
        domain, tag, fmt, ap);

    va_end(ap);

    delete[] tag;
    delete[] fmt;
    delete[] argStr;

    napi_value result = nullptr;
    napi_create_int32(env, ret, &result);
    return result;
}

static napi_value NapiOHLogSetLogLevel(napi_env env, napi_callback_info info)
{
    size_t argc = 2;
    napi_value args[2] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    int32_t logLevel = 0;
    napi_get_value_int32(env, args[0], &logLevel);

    int32_t preferStrategy = 0;
    napi_get_value_int32(env, args[1], &preferStrategy);

    OH_LOG_SetLogLevel(static_cast<LogLevel>(logLevel), static_cast<PreferStrategy>(preferStrategy));

    napi_value result = nullptr;
    napi_get_undefined(env, &result);
    return result;
}

EXTERN_C_START
napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"OHLogPrintMsg", nullptr, NapiOHLogPrintMsg, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogPrintMsgByLen", nullptr, NapiOHLogPrintMsgByLen, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogVPrint", nullptr, NapiOHLogVPrint, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"OHLogSetLogLevel", nullptr, NapiOHLogSetLogLevel, nullptr, nullptr, nullptr, napi_default, nullptr},
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
    .nm_modname = "hilog_napi",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterModule(void)
{
    napi_module_register(&demoModule);
}
